"""Synthetic checks for fresh extension seeds, immutable stages and budget stops."""
from pathlib import Path
import sys
import tempfile
import time

import numpy as np

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'eval'))
import run_curveball_extension as ext
from run_curveball import Ensemble, seed


def test_fresh_seed_namespace():
    blocks={'all':[[0],[1],[0,2]]};pairs=np.array([[0,1]],dtype=np.uint32)
    ens=Ensemble(blocks,3,pairs,'synthetic-extension','N2','extension1-pilot')
    try:
        ens.check()
        for c,entry in enumerate(ens.starts):
            seeds=entry['seeds']['all']
            assert seeds['sampling']==seed('extension1-pilot','N2','synthetic-extension',c,'all')
            assert seeds['sampling']!=seed('pilot','N2','synthetic-extension',c,'all')
            assert seeds['init']==seed('init-extension1-pilot','N2','synthetic-extension',c,'all')
    finally:ens.close()


def test_stage_extension_and_expired_deadline():
    with tempfile.TemporaryDirectory() as td:
        old=ext.ROOT;ext.ROOT=Path(td);raw=ext.ROOT/'raw';raw.mkdir()
        ens=Ensemble({'all':[[0],[1],[0,2]]},3,np.array([[0,1]],dtype=np.uint32),'synthetic-extension','N2','extension1-pilot')
        counts=[];dist=[]
        try:
            start=time.monotonic()
            a,d,r=ext.sample_stage(ens,counts,dist,3,raw,'pilot',start,start+30)
            frozen=(raw/'pilot_00003.npz').read_bytes()
            a2,d2,r2=ext.sample_stage(ens,counts,dist,5,raw,'pilot',start,start+30)
            assert np.array_equal(a,a2[:,:3,:]) and np.array_equal(d,d2[:,:3])
            assert (raw/'pilot_00003.npz').read_bytes()==frozen
            # No new draw after budget expiry and no overwrite of the prior stage.
            assert ext.sample_stage(ens,counts,dist,7,raw,'pilot',start,start-1)==(None,None,None)
            assert len(counts)==5 and len(list(raw.glob('*.npz')))==2
            ens.check()
        finally:ens.close();ext.ROOT=old


def test_expired_phase_is_not_a_pass():
    with tempfile.TemporaryDirectory() as td:
        old=ext.ROOT;ext.ROOT=Path(td);raw=ext.ROOT/'raw';raw.mkdir()
        data=dict(vocabulary=np.array(['a','b','c']),pairs=np.array([[0,1]],dtype=np.uint32),observed=np.array([1]))
        plan=dict(pilot_sweeps=[280],pilot_burn_candidates=[80],production_sweeps=[400])
        try:
            result=ext.phase_run('synthetic-extension','N2',data,{'all':[[0],[1],[0,2]]},raw,'pilot',time.monotonic()-1,plan)
            assert result['status']=='RESOURCE_LIMIT' and result['stages']==[]
            assert (raw/'pilot_starts.json').exists() and not list(raw.glob('*.npz'))
        finally:ext.ROOT=old


def test_fresh_production_summary():
    with tempfile.TemporaryDirectory() as td:
        old=ext.ROOT;ext.ROOT=Path(td);(ext.ROOT/'reports').mkdir();raw=ext.ROOT/'raw';raw.mkdir()
        rows=[sorted([i%8,(i+1)%8]) for i in range(100)]
        pairs=np.array([[0,1],[2,3],[4,5],[6,7]],dtype=np.uint32)
        data=dict(vocabulary=np.arange(8),pairs=pairs,observed=np.array([sum(a in r and b in r for r in rows) for a,b in pairs]))
        plan=dict(pilot_sweeps=[1760],pilot_burn_candidates=[80],production_sweeps=[1600])
        try:
            deadline=time.monotonic()+60
            pilot=ext.phase_run('synthetic-production','N2',data,{'all':rows},raw,'pilot',deadline,plan)
            assert pilot['status']=='PASS'
            prod=ext.phase_run('synthetic-production','N2',data,{'all':rows},raw,'production',deadline,plan,2*pilot['burn'])
            assert prod['status']=='PASS' and prod['burn']==160 and prod['summary']['R']==6400
            with np.load(raw/'production_01600.npz') as z:totals=z['counts'].sum(axis=2)
            assert prod['summary']['null_mean']==totals.mean()
            assert prod['summary']['null_sd']==totals.std()
            assert (raw/'pilot_starts.json').read_bytes()!=(raw/'production_starts.json').read_bytes()
        finally:ext.ROOT=old


if __name__=='__main__':
    for test in (test_fresh_seed_namespace,test_stage_extension_and_expired_deadline,test_expired_phase_is_not_a_pass,test_fresh_production_summary):
        test();print('PASS',test.__name__)
