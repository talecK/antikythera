"""Verify imported M3 artifacts in a local directory; never accesses its checkout."""
import argparse
import csv
import json
from pathlib import Path
import subprocess
import numpy as np
from run_revision_queue import ROOT, sha256, plan
from run_paper2 import HEADLINE
from run_eval8_nulls import summarize_counts

ROOT=Path(ROOT)


def read_table(path):
    with path.open() as f: return list(csv.DictReader(f,delimiter='\t'))


def verify(directory):
    directory=Path(directory).resolve()
    manifest_path=directory/'reports/revision_queue_m3.json'
    state=json.loads(manifest_path.read_text())
    source_hash=sha256(ROOT/'reports/revision_input_checksums.json')
    required={j for j,_,_ in plan(1)}
    if set(state['jobs'])!=required: raise ValueError('missing or unexpected queue jobs')
    verified={}; all_outputs={}
    for job,_,outputs in plan(1):
        rec=state['jobs'][job]
        if rec['status']!='complete': raise ValueError(f'{job}: incomplete')
        if rec['source_manifest_sha256']!=source_hash: raise ValueError('source manifest mismatch')
        if set(rec['outputs'])!=set(outputs): raise ValueError('output inventory mismatch')
        for name,h in rec['outputs'].items():
            if sha256(directory/name)!=h: raise ValueError(f'output mismatch {name}')
            all_outputs[name]=h
        # Compare recorded source bytes to the declared git commit, not the
        # coordinator's evolving HEAD. The commit must already be available.
        for name,h in rec['code_sha256'].items():
            import hashlib
            blob=subprocess.check_output(['git','show',f"{rec['commit_at_start']}:{name}"],cwd=ROOT)
            if hashlib.sha256(blob).hexdigest()!=h: raise ValueError(f'code mismatch: {name}')
        expected_code={'eval/run_revision_queue.py','eval/run_paper2.py','eval/run_eval8_nulls.py',
                       'eval/nulls.py','eval/run_eval8.py','eval/run_gate.py','preregistration_nulls.md'}
        if set(rec['code_sha256'])!=expected_code: raise ValueError('code inventory incomplete')
        command=list(rec['command']); expected=next(c for j,c,_ in plan(1) if j==job)
        actual=command[1:]
        if '--workers' in actual:
            wi=actual.index('--workers')+1
            if int(actual[wi])<1: raise ValueError('invalid worker count')
            actual[wi]=expected[expected.index('--workers')+1]
        if actual!=expected: raise ValueError('queue arguments differ from registered plan')
        rows=read_table(directory/outputs[0])
        if any(int(r['R'])!=1000 for r in rows): raise ValueError('wrong draw count')
        if job.startswith('paper2'):
            keys={(int(r['B']),int(r['window']),r['stratum'],r['lens']) for r in rows}
            if len(rows)!=8 or keys!=set(HEADLINE): raise ValueError('headline scope differs')
            kind='stratified' if 'stratified' in job else 'label'
            if any(r['null_kind']!=kind for r in rows): raise ValueError('wrong null')
            baseline={(int(r['B']),int(r['window']),r['stratum'],r['lens']):r
                      for r in read_table(ROOT/'reports/paper2_windows_z.tsv')}
            for r in rows:
                ref=baseline[int(r['B']),int(r['window']),r['stratum'],r['lens']]
                if any(r[k]!=ref[k] for k in ('build_docs','eval_docs','n_eligible','obs_total')):
                    raise ValueError('Paper 2 frozen structure differs')
        else:
            if len(rows)!=2 or {(r['space'],r['fold']) for r in rows}!={('thread','fold1'),('thread','fold2')}:
                raise ValueError('thread scope differs')
            summary=json.loads((directory/'reports/paper1_nulls_label_R100_thread_seeds10.json').read_text())
            if len(summary['cells'])!=2 or {(c['space'],c['fold']) for c in summary['cells']}!={('thread','fold1'),('thread','fold2')}:
                raise ValueError('pooled JSON scope differs')
            if summary['commit']!=rec['commit_at_start']:
                raise ValueError('child/queue commits differ')
            for name,h in summary['code_sha256'].items():
                if rec['code_sha256'].get(name)!=h: raise ValueError('child/queue code hashes differ')
            for c in summary['cells']:
                fold=c['fold']; ci=2 if fold=='fold1' else 3
                path=directory/f'data/registry/nulls_revisions/label_R100_thread_seeds10/thread_{fold}.npz'
                with np.load(path,allow_pickle=False) as z:
                    if z['null_counts'].shape!=(1000,len(z['observed'])): raise ValueError('raw draw shape')
                    if not np.array_equal(z['seeds'],[[20260831,ci,b] for b in range(10)]): raise ValueError('seed stream')
                    primary,formed=summarize_counts(z['observed'],z['null_counts'],z['eligible'],z['supported'])
                    reference=json.loads((ROOT/'data/registry/pilot1_concepts/run8_thread.json').read_text())[fold]
                    if len(z['observed'])!=reference['eligible'] or int(z['observed'].sum())!=reference['obs_total']:
                        raise ValueError('Paper 1 frozen structure differs')
                    tsv=next(r for r in rows if r['fold']==fold)
                    for k in ('null_mean','null_sd','z_seg','ratio'):
                        if not np.isclose(primary[k],c[k],rtol=1e-10,atol=1e-12): raise ValueError(f'pooled {k} mismatch')
                        if not np.isclose(primary[k],float(tsv[k]),rtol=1e-10,atol=1e-12): raise ValueError(f'TSV pooled {k} mismatch')
                    if len(formed)!=c['formed']: raise ValueError('pooled formation mismatch')
                    if len(formed)!=int(tsv['formed']): raise ValueError('TSV pooled formation mismatch')
                    if len(c['batches'])!=10: raise ValueError('incomplete batches')
                    for b in range(10):
                        bs,bf=summarize_counts(z['observed'],z['null_counts'][100*b:100*(b+1)],z['eligible'],z['supported'])
                        reported=c['batches'][b]
                        if any(not np.isclose(bs[k],reported[k],rtol=1e-10,atol=1e-12) for k in ('null_mean','null_sd','z_seg','ratio')) or len(bf)!=reported['formed']:
                            raise ValueError('batch summary mismatch')
        verified[job]=dict(commit=rec['commit_at_start'],architecture=rec['architecture'],outputs=rec['outputs'])
    return dict(status='VERIFIED',artifact_root=str(directory),manifest_sha256=sha256(manifest_path),
                source_manifest_sha256=source_hash,jobs=verified,outputs_sha256=all_outputs,
                limitation='Manifest verifies supplied records and bytes; it is not remote machine telemetry.')


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--artifact-root',type=Path,default=ROOT)
    ap.add_argument('--out',type=Path,default=ROOT/'reports/m3_import_verification.json')
    args=ap.parse_args(); report=verify(args.artifact_root)
    with args.out.open('x') as f: json.dump(report,f,indent=2); f.write('\n')
    print('Verified completed M3 artifact set')


if __name__=='__main__': main()
