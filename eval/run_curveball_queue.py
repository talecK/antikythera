#!/usr/bin/env python3
"""Run registered N2/N3 cell order, two null workers per prepared matrix.

Uses the same queue lock as the serial runner. Preparation is serial to
avoid races and duplicate corpus loads. No MBP jobs are included.
"""
import argparse
from concurrent.futures import ProcessPoolExecutor
import fcntl
import json
import math
import multiprocessing as mp
from pathlib import Path
import subprocess
import sys
import time
from prepare_curveball import ROOT,BASE,ALL,HEADLINE,P1,prepare,registered
from run_curveball import run_cell,CODE
from run_revision_queue import sha256


def interrupted_worker_seconds():
    """Keep user-interrupted attempts inside the registered global budget."""
    total=0.0
    for path in (ROOT/'reports').glob('curveball_*_interruption.json'):
        record=json.loads(path.read_text())
        seconds=float(record['charged_worker_seconds'])
        if not math.isfinite(seconds) or seconds<0:
            raise ValueError(f'invalid interrupted worker time: {path}')
        total+=seconds
    return total


def job(cell,null):
    # File-level stdout redirection keeps a live, unbuffered progress log.
    import os
    path=ROOT/'logs'/f'curveball_{cell}_{null}.log'
    with path.open('a',buffering=1) as out:
        os.dup2(out.fileno(),1);os.dup2(out.fileno(),2)
        result=run_cell(cell,null)
    return dict(cell=cell,null=null,pilot=result['pilot']['status'],
                production=result.get('production',{}).get('status','NOT_RUN'))


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--cells',choices=['initial','all'],default='all')
    ap.add_argument('--workers',type=int,choices=[1,2],default=2)
    args=ap.parse_args();registered();BASE.mkdir(parents=True,exist_ok=True)
    lock=(BASE/'queue.lock').open('a');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
    report_path=ROOT/'reports/curveball_queue_v1.json'
    previous=json.loads(report_path.read_text()) if report_path.exists() else {'runs':[]}
    run=dict(started_utc=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),
             commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
             code_sha256={n:sha256(ROOT/n) for n in CODE+['eval/run_curveball_queue.py']},
             workers=args.workers,cells=args.cells,completed=[],
             interrupted_worker_seconds=interrupted_worker_seconds())
    previous['runs'].append(run)
    def save():
        temp=report_path.with_suffix('.tmp');temp.write_text(json.dumps(previous,indent=2)+'\n');temp.replace(report_path)
    save()
    cells=ALL if args.cells=='all' else HEADLINE+P1
    with ProcessPoolExecutor(max_workers=args.workers,mp_context=mp.get_context('spawn')) as pool:
        for cell in cells:
            if any(sha256(ROOT/n)!=h for n,h in run['code_sha256'].items()):
                raise RuntimeError('scientific code changed during queue')
            elapsed=interrupted_worker_seconds()
            for p in (ROOT/'reports').glob('curveball_p*_N[23].json'):
                r=json.loads(p.read_text());elapsed+=sum(r.get(ph,{}).get('seconds',0) for ph in ('pilot','production'))
            new=sum(not (ROOT/'reports'/f'curveball_{cell}_{null}.json').exists() for null in ('N2','N3'))
            if elapsed+new*4*3600>72*3600:
                run['status']='GLOBAL_RESOURCE_LIMIT';save();return
            t=time.monotonic();prepare(cell)
            print(f'PREPARED {cell} seconds={time.monotonic()-t:.1f}',flush=True)
            futures=[pool.submit(job,cell,null) for null in ('N2','N3')]
            for future in futures:
                result=future.result();result['sha256']=sha256(ROOT/'reports'/f"curveball_{cell}_{result['null']}.json")
                run['completed'].append(result);save();print(result,flush=True)
    run['status']='COMPLETE';save()


if __name__=='__main__':main()
