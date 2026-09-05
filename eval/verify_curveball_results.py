"""Audit transferred Curveball results from frozen matrices and raw chains."""
import argparse
import csv
from functools import lru_cache
import json
from pathlib import Path
import shutil
import subprocess

import numpy as np

from prepare_curveball import ROOT, unpack
from curveball_diagnostics import aggregate_diagnostics, formation_diagnostics
from run_revision_queue import sha256
from verify_curveball_handoff import relative_path


@lru_cache(None)
def digest(path):
    return sha256(Path(path))


def equal(actual,expected,where):
    if isinstance(expected,dict):
        if set(actual)!=set(expected): raise ValueError(f'keys differ: {where}')
        for key,value in expected.items():equal(actual[key],value,f'{where}.{key}')
    elif isinstance(expected,list):
        if len(actual)!=len(expected):raise ValueError(f'length differs: {where}')
        for i,(a,b) in enumerate(zip(actual,expected)):equal(a,b,f'{where}[{i}]')
    elif isinstance(expected,float):
        if not np.isclose(actual,expected,rtol=1e-10,atol=1e-10):raise ValueError(f'number differs: {where}')
    elif actual!=expected:raise ValueError(f'value differs: {where}')


def audit_record(payload,path):
    record=json.loads(path.read_text());meta=record['matrix']
    for name,h in meta['input_sha256'].items():
        if digest(str(ROOT/relative_path(name)))!=h:raise ValueError(f'input mismatch: {name}')
    for name,h in record['code_sha256'].items():
        import hashlib
        raw=subprocess.check_output(['git','show',f"{record['commit']}:{name}"],cwd=ROOT)
        if hashlib.sha256(raw).hexdigest()!=h:raise ValueError(f'code provenance mismatch: {name}')
    matrix=payload/relative_path(meta['matrix_path'])
    if digest(str(matrix))!=meta['matrix_sha256']:raise ValueError('matrix checksum mismatch')
    data,blocks=unpack(matrix,record['null'])
    import hashlib
    for name,h in meta['arrays_sha256'].items():
        if hashlib.sha256(data[name].tobytes()).hexdigest()!=h:raise ValueError(f'array mismatch: {name}')
    obs=int(data['observed'].sum())
    if obs!=meta['obs_total'] or len(data['pairs'])!=meta['eligible']:raise ValueError('census mismatch')
    if meta['cell'].startswith('p1_'):
        source='data/registry/run5_author/run8_author.json' if meta['space']=='author' else 'data/registry/pilot1_concepts/run8_thread.json'
        frozen=json.loads((ROOT/source).read_text())[meta['fold']]
        if obs!=frozen['obs_total'] or meta['eligible']!=frozen['eligible']:raise ValueError('frozen observed census mismatch')
    else:
        with (ROOT/'reports/paper2_windows_z.tsv').open() as f:
            frozen=next(r for r in csv.DictReader(f,delimiter='\t') if
                (int(r['B']),int(r['window']),r['stratum'],r['lens'])==
                (meta['B'],meta['window'],meta['stratum'],meta['lens']))
        for a,b in [('obs_total','obs_total'),('eligible','n_eligible'),('build_docs','build_docs'),('eval_docs','eval_docs')]:
            if meta[a]!=int(frozen[b]):raise ValueError(f'frozen Paper 2 census mismatch: {a}')
    production=None;stage_count=0
    for phase in ('pilot','production'):
        result=record.get(phase)
        if result is None:continue
        first_pass=None
        for st in result['stages']:
            raw=payload/relative_path(st['raw_path'])
            if digest(str(raw))!=st['raw_sha256']:raise ValueError('raw checksum mismatch')
            with np.load(raw,allow_pickle=False) as z:
                counts=z['counts'];distance=z['distance']
            if counts.shape!=(4,st['sweeps'],meta['eligible']) or distance.shape!=counts.shape[:2]:
                raise ValueError('raw shape mismatch')
            if not np.issubdtype(counts.dtype,np.unsignedinteger):raise ValueError('counts are not unsigned integers')
            for d in st['diagnostics']:
                burn=d['burn'];actual=aggregate_diagnostics(counts[:,burn:,:],distance[:,burn:])
                equal(actual,{k:v for k,v in d.items() if k!='burn'},f'{meta["cell"]}.{record["null"]}.{phase}.{st["sweeps"]}.burn{burn}')
                if actual['passed'] and first_pass is None:first_pass=(st['sweeps'],burn)
            stage_count+=1
        if result['status']=='PASS':
            if first_pass is None or first_pass[0]!=result['stages'][-1]['sweeps']:raise ValueError('stopping-stage mismatch')
            if phase=='pilot' and first_pass[1]!=result['burn']:raise ValueError('selected burn mismatch')
        elif result['status']=='UNRESOLVED' and first_pass is not None:raise ValueError('unresolved despite passing stage')
        if phase=='production':production=counts
    outcome=dict(cell=meta['cell'],null=record['null'],stages_recomputed=stage_count,
                 pilot=record['pilot']['status'],production=record.get('production',{}).get('status','NOT_RUN'))
    if production is not None and record['production']['status']=='PASS':
        totals=production.sum(axis=2);mean=float(totals.mean());sd=float(totals.std())
        summary=dict(obs_total=obs,null_mean=mean,null_sd=sd,z_seg=(obs-mean)/sd if sd else None,
                     ratio=obs/mean if mean else None,R=int(totals.size),tail_lo=float((totals<=obs).mean()),
                     tail_hi=float((totals>=obs).mean()),chain_means=totals.mean(axis=1).tolist(),
                     chain_sds=totals.std(axis=1).tolist())
        equal(summary,record['production']['summary'],'summary')
        lower=np.zeros(len(data['pairs']),dtype=np.int64);upper=lower.copy()
        for rows in blocks.values():
            c=np.bincount([v for row in rows for v in row],minlength=len(data['vocabulary']))
            ca,cb=c[data['pairs'][:,0]],c[data['pairs'][:,1]]
            lower+=np.maximum(0,ca+cb-len(rows));upper+=np.minimum(ca,cb)
        formation=formation_diagnostics(production,data['observed'],data['supported'],lower,upper)
        equal(formation,record['production']['formation'],'formation')
        outcome.update(summary=summary,formation_passed=formation['passed'],formed=formation['formed'],
                       formation_unresolved_pairs=sum(not d['passed'] for d in formation['checks'].values()))
    return outcome


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--transfer',type=Path,required=True)
    ap.add_argument('--output',type=Path,required=True);ap.add_argument('--install',action='store_true')
    args=ap.parse_args();manifest=json.loads((args.transfer/'manifest.json').read_text());payload=args.transfer/'payload'
    for name,r in manifest['files'].items():
        path=payload/relative_path(name)
        if path.stat().st_size!=r['bytes'] or digest(str(path))!=r['sha256']:raise ValueError(f'transfer mismatch: {name}')
        target=ROOT/relative_path(name)
        if target.exists() and digest(str(target))!=r['sha256']:raise ValueError(f'conflicting local file preserved: {name}')
    results=[]
    for name,h in manifest['reports'].items():
        path=payload/'reports'/f'curveball_{name}.json'
        if digest(str(path))!=h:raise ValueError('queue/report hash mismatch')
        result=audit_record(payload,path);results.append(result)
        print('VERIFIED',name,'aggregate',result['production'],'formation',result.get('formation_passed'),flush=True)
    if args.install:
        for name in manifest['files']:
            source=payload/relative_path(name);target=ROOT/relative_path(name)
            if target.exists():continue
            target.parent.mkdir(parents=True,exist_ok=True)
            with source.open('rb') as src,target.open('xb') as dst:shutil.copyfileobj(src,dst)
            if sha256(target)!=manifest['files'][name]['sha256']:raise ValueError('installed hash mismatch')
    output=dict(status='PASS',transfer_manifest_sha256=sha256(args.transfer/'manifest.json'),
                files_verified=len(manifest['files']),installed=args.install,results=results,
                method='Recomputed raw moments, all archived stage diagnostics and production formation diagnostics using independently reference-tested diagnostic routines; verified frozen input/matrix/code/census and transfer hashes. No sampling rerun.')
    args.output.write_text(json.dumps(output,indent=2)+'\n')


if __name__=='__main__':main()
