"""Verify an M1 transfer before running the registered queue on native ARM."""
import argparse
import json
from pathlib import Path
import platform
import shutil
import subprocess
import sys

import duckdb
import numpy as np

from prepare_curveball import ROOT, registered, verify_sources
from run_revision_queue import sha256


def relative_path(name):
    path=Path(name)
    if path.is_absolute() or '..' in path.parts:
        raise ValueError(f'unsafe transfer path: {name}')
    return path


def verify(manifest_path,install=False,allow_non_arm=False):
    manifest=json.loads(manifest_path.read_text())
    if platform.machine()!='arm64' and not allow_non_arm:
        raise RuntimeError('MBP queue requires native arm64 Python, not Rosetta')
    actual=dict(python=platform.python_version(),numpy=np.__version__,duckdb=duckdb.__version__)
    if actual!=manifest['versions']:
        raise RuntimeError(f'pinned environment mismatch: {actual}')
    subprocess.run(['git','merge-base','--is-ancestor',manifest['code_commit'],'HEAD'],cwd=ROOT,check=True)
    registered()
    for name,expected in manifest['repository_sha256'].items():
        if sha256(ROOT/relative_path(name))!=expected:
            raise RuntimeError(f'repository checksum mismatch: {name}')
    # Validate the entire payload and every destination before copying anything.
    missing=[]
    for name,expected in manifest['payload_sha256'].items():
        rel=relative_path(name)
        if not rel.parts or rel.parts[0]!='data':
            raise ValueError(f'non-data payload: {name}')
        source=manifest_path.parent/'payload'/rel; target=ROOT/rel
        if sha256(source)!=expected:
            raise RuntimeError(f'transfer checksum mismatch: {name}')
        if target.exists():
            if sha256(target)!=expected:
                raise RuntimeError(f'existing destination differs; preserve and inspect: {name}')
        else: missing.append((source,target,expected))
    if missing and not install:
        raise RuntimeError('payload missing locally; use --install-payload after review')
    for source,target,expected in missing:
        target.parent.mkdir(parents=True,exist_ok=True)
        with source.open('rb') as src,target.open('xb') as dst:
            shutil.copyfileobj(src,dst)
        if sha256(target)!=expected:
            raise RuntimeError(f'installed checksum mismatch: {target}')
    inputs={}
    for cell in ('p2_WSB_04','p1_author_fold1','p1_thread_fold1'):
        inputs.update(verify_sources(cell))
    for name,expected in manifest['extra_input_sha256'].items():
        if sha256(ROOT/relative_path(name))!=expected:
            raise RuntimeError(f'frozen reference checksum mismatch: {name}')
    return dict(status='PASS',architecture=platform.machine(),versions=actual,
                code_commit=manifest['code_commit'],repository_files=len(manifest['repository_sha256']),
                payload_files=len(manifest['payload_sha256']),installed_files=len(missing),
                verified_input_files=len(inputs)+len(manifest['extra_input_sha256']))


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--manifest',type=Path,required=True)
    ap.add_argument('--install-payload',action='store_true')
    ap.add_argument('--allow-non-arm',action='store_true',help='M1 transfer audit only; never use to launch MBP queue')
    args=ap.parse_args()
    print(json.dumps(verify(args.manifest.resolve(),args.install_payload,args.allow_non_arm),indent=2))
