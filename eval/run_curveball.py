#!/usr/bin/env python3
"""Registered N2/N3 pilot + fresh production. Writes immutable stage artifacts."""
import argparse
import fcntl
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys
import time
import numpy as np
import duckdb
from curveball import Curveball, build_library
from curveball_diagnostics import aggregate_diagnostics, formation_diagnostics
from prepare_curveball import ROOT, BASE, REG, ALL, HEADLINE, P1, prepare, unpack, registered
from run_revision_queue import sha256

CODE = ['eval/run_curveball.py','eval/prepare_curveball.py','eval/curveball.py',
        'eval/curveball_kernel.cpp','eval/curveball_diagnostics.py','eval/run_eval8.py',
        'eval/run_eval8_nulls.py','eval/run_paper2.py','eval/run_gate.py',
        'preregistration_nulls_n2.md']


def seed(phase,null,cell,chain,block):
    name=f'antikythera/n2n3/v1|{phase}|{null}|{cell}|{chain}|{block}'
    return int.from_bytes(hashlib.sha256(name.encode()).digest()[:8],'little')


def write_json(path,value):
    with path.open('x') as f: json.dump(value,f,indent=2,allow_nan=False); f.write('\n')


def verify(chain,rows,ncol):
    if [len(r) for r in chain.rows()] != [len(r) for r in rows] or not np.array_equal(
            chain.margins(),np.bincount([v for r in rows for v in r],minlength=ncol)):
        raise RuntimeError('binary margins changed')


class Ensemble:
    def __init__(self,blocks,ncol,pairs,cell,null,phase):
        self.chains=[]; self.starts=[]; self.blocks=blocks; self.ncol=ncol; self.pairs=pairs
        for c,init_sweeps in enumerate((0,5,20,80)):
            chain_blocks={}; seeds={}; initial_total=np.zeros(len(pairs),dtype=np.uint64)
            distance=0
            for block,rows in blocks.items():
                si=seed('init-'+phase,null,cell,c,block); ss=seed(phase,null,cell,c,block)
                with Curveball(rows,ncol,si) as init:
                    init.step(init_sweeps*len(rows)); verify(init,rows,ncol)
                    initial_total+=init.counts(pairs); distance+=init.diagnostics()['changed_binary_entries']
                    ch=Curveball(init.rows(),ncol,ss); ch.set_reference(rows)
                chain_blocks[block]=ch
                seeds[block]=dict(init=si,sampling=ss,initialization_attempts=init_sweeps*len(rows))
            self.chains.append(chain_blocks)
            self.starts.append(dict(chain=c,seeds=seeds,obs_distance=distance,total=int(initial_total.sum())))

    def step(self):
        for cb in self.chains:
            for block,ch in cb.items(): ch.step(len(self.blocks[block]))

    def sample(self):
        counts=[]; distances=[]
        for cb in self.chains:
            counts.append(sum((ch.counts(self.pairs) for ch in cb.values()),np.zeros(len(self.pairs),dtype=np.uint64)))
            distances.append(sum(ch.diagnostics()['changed_binary_entries'] for ch in cb.values()))
        return np.asarray(counts),np.asarray(distances)

    def check(self):
        for cb in self.chains:
            for b,ch in cb.items(): verify(ch,self.blocks[b],self.ncol)

    def counters(self):
        return [{b:ch.diagnostics() for b,ch in cb.items()} for cb in self.chains]

    def close(self):
        for cb in self.chains:
            for ch in cb.values(): ch.close()


def stage(ens,counts,distances,target,burn,rawdir,phase,started):
    advance=0.; counting=0.
    while len(counts)<target:
        t=time.monotonic(); ens.step(); advance+=time.monotonic()-t
        t=time.monotonic(); co,di=ens.sample(); counting+=time.monotonic()-t
        counts.append(co); distances.append(di)
        if len(counts)%20==0:
            print(f'{rawdir.name} {phase} sweeps={len(counts)}/{target} elapsed={time.monotonic()-started:.1f}s',flush=True)
        if time.monotonic()-started>7200: break
    ens.check()
    a=np.stack(counts,axis=1); d=np.stack(distances,axis=1)
    raw=rawdir/f'{phase}_{len(counts):04d}.npz'
    with raw.open('xb') as f: np.savez_compressed(f,counts=a,distance=d)
    return a,d,dict(raw_path=str(raw.relative_to(ROOT)),raw_sha256=sha256(raw),
                    sweeps=len(counts),trade_seconds=advance,count_seconds=counting,
                    elapsed_seconds=time.monotonic()-started,counters=ens.counters())


def phase_run(cell,null,data,blocks,burn=None):
    phase='pilot' if burn is None else 'production'
    rawdir=BASE/f'{cell}_{null}'; rawdir.mkdir(parents=True,exist_ok=True)
    started=time.monotonic()
    ens=Ensemble(blocks,len(data['vocabulary']),data['pairs'],cell,null,phase)
    write_json(rawdir/f'{phase}_starts.json',ens.starts)
    counts=[]; distances=[]; stages=[]; selected=None; final=None
    try:
        if burn is not None:
            for _ in range(burn): ens.step()
        for target in ((280,480,880) if phase=='pilot' else (400,800,1600)):
            a,d,record=stage(ens,counts,distances,target,burn,rawdir,phase,started)
            tests=[]
            for b in ((5,10,20,40,80) if phase=='pilot' else (0,)):
                if a.shape[1]-b<200: continue
                diag=aggregate_diagnostics(a[:,b:,:],d[:,b:])
                tests.append(dict(burn=b,**diag))
                if selected is None and diag['passed']: selected=b
            record['diagnostics']=tests; stages.append(record)
            write_json(ROOT/'reports'/f'curveball_{cell}_{null}_{phase}_{len(counts):04d}.json',record)
            print(f'{cell} {null} {phase} stage={len(counts)} pass={selected is not None}',flush=True)
            if time.monotonic()-started>7200:
                return dict(status='RESOURCE_LIMIT',stages=stages,seconds=time.monotonic()-started)
            if selected is not None:
                final=a[:,selected:,:]; break
        if selected is None:
            return dict(status='UNRESOLVED',stages=stages,seconds=time.monotonic()-started)
        out=dict(status='PASS',burn=selected if phase=='pilot' else burn,stages=stages,
                 seconds=time.monotonic()-started)
        if phase=='production':
            totals=final.sum(axis=2); mean=float(totals.mean()); sd=float(totals.std())
            obs=int(data['observed'].sum())
            lower=np.zeros(len(data['pairs']),dtype=np.int64); upper=lower.copy()
            for rows in blocks.values():
                c=np.bincount([v for r in rows for v in r],minlength=len(data['vocabulary']))
                ca,cb=c[data['pairs'][:,0]],c[data['pairs'][:,1]]
                lower+=np.maximum(0,ca+cb-len(rows)); upper+=np.minimum(ca,cb)
            out['summary']=dict(obs_total=obs,null_mean=mean,null_sd=sd,z_seg=(obs-mean)/sd if sd else None,
                                ratio=obs/mean if mean else None,R=int(totals.size),
                                tail_lo=float((totals<=obs).mean()),tail_hi=float((totals>=obs).mean()),
                                chain_means=totals.mean(axis=1).tolist(),chain_sds=totals.std(axis=1).tolist())
            out['formation']=formation_diagnostics(final,data['observed'],data['supported'],lower,upper)
        return out
    finally: ens.close()


def run_cell(cell,null):
    report=ROOT/'reports'/f'curveball_{cell}_{null}.json'
    if report.exists():
        old=json.loads(report.read_text())
        for phase in ('pilot','production'):
            for st in old.get(phase,{}).get('stages',[]):
                if sha256(ROOT/st['raw_path'])!=st['raw_sha256']: raise RuntimeError('raw checksum mismatch')
        if sha256(ROOT/old['matrix']['matrix_path'])!=old['matrix']['matrix_sha256']:
            raise RuntimeError('matrix checksum mismatch')
        print(f'SKIP verified completed attempt {cell} {null}',flush=True)
        return old
    rawdir=BASE/f'{cell}_{null}'
    if rawdir.exists(): raise RuntimeError(f'preserved partial run {rawdir}; inspect before restart')
    target,meta=prepare(cell); data,blocks=unpack(target,null)
    library=build_library()
    provenance=dict(cell=cell,null=null,matrix=meta,registration_sha256=sha256(REG),
        code_sha256={n:sha256(ROOT/n) for n in CODE},
        commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
        python=sys.version,numpy=np.__version__,duckdb=duckdb.__version__,architecture=platform.machine(),
        build=json.loads(library.with_suffix('.build.json').read_text()),
        started_utc=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()))
    rawdir.mkdir(parents=True)
    write_json(rawdir/'provenance.json',provenance)
    provenance['pilot']=phase_run(cell,null,data,blocks)
    # Check scientific source integrity before fresh production.
    if any(sha256(ROOT/n)!=h for n,h in provenance['code_sha256'].items()):
        raise RuntimeError('code changed during pilot')
    if provenance['pilot']['status']=='PASS':
        provenance['production']=phase_run(cell,null,data,blocks,2*provenance['pilot']['burn'])
    write_json(report,provenance)
    return provenance


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--cells',default='initial')
    ap.add_argument('--null',choices=['both','N2','N3'],default='both')
    args=ap.parse_args(); registered()
    cells=ALL if args.cells=='all' else HEADLINE+P1 if args.cells=='initial' else args.cells.split(',')
    if any(c not in ALL for c in cells): ap.error('unregistered cell')
    BASE.mkdir(parents=True,exist_ok=True)
    lock=(BASE/'queue.lock').open('a'); fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
    for cell in cells:
        for null in (['N2','N3'] if args.null=='both' else [args.null]):
            elapsed=0
            for p in (ROOT/'reports').glob('curveball_p*_N[23].json'):
                r=json.loads(p.read_text()); elapsed+=sum(r.get(ph,{}).get('seconds',0) for ph in ('pilot','production'))
            # Reserve the maximum four hours for a fresh pilot+production.
            if elapsed+4*3600>72*3600: raise SystemExit('Global worker-hour budget exhausted')
            run_cell(cell,null)


if __name__=='__main__': main()
