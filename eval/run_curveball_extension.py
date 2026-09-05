"""One prospectively bounded Paper 2 extension; first-pass files are immutable."""
import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
import fcntl
import json
import multiprocessing as mp
import os
from pathlib import Path
import platform
import subprocess
import sys
import time

import duckdb
import numpy as np

from curveball import build_library
from curveball_diagnostics import aggregate_diagnostics
from prepare_curveball import ROOT, BASE, prepare, unpack
from run_curveball import Ensemble, CODE, write_json
from run_revision_queue import sha256

REG=ROOT/'preregistration_nulls_extension1.md'
CONFIG=ROOT/'reports/curveball_extension1_plan.json'
RAW=ROOT/'data/registry/nulls_revisions/curveball_extension1'
SOURCE=CODE+['eval/run_curveball_extension.py','preregistration_nulls_extension1.md',
             'reports/curveball_extension1_plan.json']


def verify_registration():
    for path in (REG,CONFIG):
        committed=subprocess.check_output(['git','show',f'HEAD:{path.relative_to(ROOT)}'],cwd=ROOT)
        if committed!=path.read_bytes():raise RuntimeError('extension registration/config must be committed')
    if 'STATUS: REGISTERED.' not in REG.read_text().split('---')[0]:raise RuntimeError('extension not registered')
    return json.loads(CONFIG.read_text())


def guard(hashes):
    if any(sha256(ROOT/n)!=h for n,h in hashes.items()):raise RuntimeError('extension source changed')


def sample_stage(ens,counts,distances,target,rawdir,phase,started,deadline):
    previous=len(counts)
    while len(counts)<target and time.monotonic()<deadline:
        ens.step();co,di=ens.sample();counts.append(co);distances.append(di)
        if len(counts)%40==0:
            print(f'{rawdir.name} {phase} sweeps={len(counts)}/{target} elapsed={time.monotonic()-started:.1f}s',flush=True)
    if len(counts)==previous:return None,None,None
    ens.check();a=np.stack(counts,axis=1);d=np.stack(distances,axis=1)
    path=rawdir/f'{phase}_{len(counts):05d}.npz'
    with path.open('xb') as f:np.savez_compressed(f,counts=a,distance=d)
    return a,d,dict(raw_path=str(path.relative_to(ROOT)),raw_sha256=sha256(path),
                    sweeps=len(counts),elapsed_seconds=time.monotonic()-started,
                    counters=ens.counters())


def phase_run(cell,null,data,blocks,rawdir,phase,deadline,plan,burn=None):
    started=time.monotonic()
    ens=Ensemble(blocks,len(data['vocabulary']),data['pairs'],cell,null,'extension1-'+phase)
    write_json(rawdir/f'{phase}_starts.json',ens.starts)
    counts=[];distances=[];stages=[];selected=None
    try:
        for _ in range(burn or 0):
            if time.monotonic()>=deadline:
                return dict(status='RESOURCE_LIMIT',stages=stages,seconds=time.monotonic()-started)
            ens.step()
        targets=plan['pilot_sweeps'] if phase=='pilot' else plan['production_sweeps']
        for target in targets:
            if time.monotonic()>=deadline:break
            a,d,record=sample_stage(ens,counts,distances,target,rawdir,phase,started,deadline)
            if record is None:break
            tests=[]
            for b in (plan['pilot_burn_candidates'] if phase=='pilot' else [0]):
                if a.shape[1]-b<200:continue
                diag=aggregate_diagnostics(a[:,b:,:],d[:,b:]);tests.append(dict(burn=b,**diag))
                if selected is None and diag['passed']:selected=b
            record['diagnostics']=tests;stages.append(record)
            write_json(ROOT/'reports'/f'curveball_extension1_{cell}_{null}_{phase}_{len(counts):05d}.json',record)
            print(f'{cell} {null} {phase} stage={len(counts)} passed={selected is not None}',flush=True)
            # Resource-truncated stages are archived but cannot become passing results.
            if len(counts)!=target or time.monotonic()>=deadline:
                return dict(status='RESOURCE_LIMIT',stages=stages,seconds=time.monotonic()-started)
            if selected is not None:
                result=dict(status='PASS',burn=selected if phase=='pilot' else burn,stages=stages,
                            seconds=time.monotonic()-started)
                if phase=='production':
                    totals=a.sum(axis=2);mean=float(totals.mean());sd=float(totals.std());obs=int(data['observed'].sum())
                    result['summary']=dict(obs_total=obs,null_mean=mean,null_sd=sd,
                        z_seg=(obs-mean)/sd if sd else None,ratio=obs/mean if mean else None,R=int(totals.size),
                        tail_lo=float((totals<=obs).mean()),tail_hi=float((totals>=obs).mean()),
                        chain_means=totals.mean(axis=1).tolist(),chain_sds=totals.std(axis=1).tolist())
                    result['formation']='NOT_EVALUATED: extension targets aggregate Paper 2 predictions only'
                return result
        return dict(status='RESOURCE_LIMIT' if time.monotonic()>=deadline else 'UNRESOLVED',
                    stages=stages,seconds=time.monotonic()-started)
    finally:ens.close()


def run_job(item,global_deadline,hashes,plan):
    cell,null=item['cell'],item['null'];name=f'{cell}_{null}'
    with (ROOT/'logs'/f'curveball_extension1_{name}.log').open('a',buffering=1) as log:
        os.dup2(log.fileno(),1);os.dup2(log.fileno(),2)
        guard(hashes)
        report=ROOT/'reports'/f'curveball_extension1_{name}.json';rawdir=RAW/name
        if report.exists() or rawdir.exists():raise RuntimeError(f'preserved prior extension attempt: {name}')
        first=ROOT/'reports'/f'curveball_{name}.json'
        if sha256(first)!=item['first_pass_sha256']:raise RuntimeError('first-pass result changed')
        if json.loads(first.read_text()).get('production',{}).get('status')=='PASS':
            raise RuntimeError('passing first-pass cell cannot be extended')
        start=time.monotonic();deadline=min(global_deadline,start+plan['per_attempt_seconds'])
        out=dict(cell=cell,null=null,extension=1,first_pass_sha256=item['first_pass_sha256'],
                 code_sha256=hashes,registration_sha256=sha256(REG),
                 commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
                 architecture=platform.machine(),python=platform.python_version(),numpy=np.__version__,duckdb=duckdb.__version__,
                 started_utc=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()))
        if start>=global_deadline:
            out['pilot']=dict(status='NOT_RUN_GLOBAL_BUDGET',stages=[],seconds=0)
        else:
            target,meta=prepare(cell)
            if meta['matrix_sha256']!=item['matrix_sha256']:raise RuntimeError('registered matrix changed')
            data,blocks=unpack(target,null);out['matrix']=meta
            library=build_library();out['build']=json.loads(library.with_suffix('.build.json').read_text())
            rawdir.mkdir(parents=True);write_json(rawdir/'provenance.json',out)
            if time.monotonic()>=deadline:
                out['pilot']=dict(status='RESOURCE_LIMIT',stages=[],seconds=0)
            else:
                out['pilot']=phase_run(cell,null,data,blocks,rawdir,'pilot',deadline,plan)
                if out['pilot']['status']=='PASS':
                    guard(hashes)
                    if time.monotonic()<deadline:
                        out['production']=phase_run(cell,null,data,blocks,rawdir,'production',deadline,plan,2*out['pilot']['burn'])
                    else:out['production']=dict(status='RESOURCE_LIMIT',stages=[],seconds=0)
        out['elapsed_seconds']=time.monotonic()-start
        write_json(report,out)
        return dict(cell=cell,null=null,pilot=out['pilot']['status'],
                    production=out.get('production',{}).get('status','NOT_RUN'),
                    seconds=out['elapsed_seconds'],sha256=sha256(report))


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--preflight-only',action='store_true');args=ap.parse_args()
    plan=verify_registration()
    if platform.machine()!='arm64':raise RuntimeError('extension runs only on native ARM MBP')
    if dict(python=platform.python_version(),numpy=np.__version__,duckdb=duckdb.__version__)!=plan['versions']:
        raise RuntimeError('pinned environment mismatch')
    for item in plan['jobs']:
        p=ROOT/'reports'/f"curveball_{item['cell']}_{item['null']}.json"
        if sha256(p)!=item['first_pass_sha256']:raise RuntimeError('first-pass inventory mismatch')
    if args.preflight_only:print(f"PASS {len(plan['jobs'])} registered extension jobs");return
    BASE.mkdir(parents=True,exist_ok=True)
    lock=(BASE/'queue.lock').open('a');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
    queue=ROOT/'reports/curveball_extension1_queue.json'
    if queue.exists():raise RuntimeError('extension already attempted; preserve and inspect')
    started=time.monotonic();deadline=started+plan['global_wall_seconds']
    hashes={n:sha256(ROOT/n) for n in SOURCE}
    record=dict(started_utc=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),
                code_sha256=hashes,commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
                global_wall_seconds=plan['global_wall_seconds'],per_attempt_seconds=plan['per_attempt_seconds'],
                workers=2,status='RUNNING',completed=[])
    write_json(queue,record)
    def save():
        temp=queue.with_suffix('.tmp');temp.write_text(json.dumps(record,indent=2)+'\n');temp.replace(queue)
    with ProcessPoolExecutor(max_workers=2,mp_context=mp.get_context('spawn')) as pool:
        futures=[pool.submit(run_job,item,deadline,hashes,plan) for item in plan['jobs']]
        for future in as_completed(futures):
            result=future.result();record['completed'].append(result);save();print(result,flush=True)
    record['status']='COMPLETE';record['elapsed_seconds']=time.monotonic()-started
    record['resource_limited_attempts']=sum(r['pilot'] in ('RESOURCE_LIMIT','NOT_RUN_GLOBAL_BUDGET') or r['production']=='RESOURCE_LIMIT' for r in record['completed'])
    save()


if __name__=='__main__':main()
