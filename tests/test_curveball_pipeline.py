"""Independent diagnostics fixtures and synthetic matrix/pilot plumbing."""
import json
from pathlib import Path
import sys
import tempfile
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'eval'))
from curveball import Curveball
from curveball_diagnostics import describe, aggregate_diagnostics, formation_diagnostics
from prepare_curveball import canonical
from run_curveball import Ensemble, seed, stage

ROOT=Path(__file__).resolve().parents[1]


def test_reference_diagnostics():
    reference=json.loads((ROOT/'tests/fixtures/mcmc_reference.json').read_text())
    with np.load(ROOT/'tests/fixtures/mcmc_reference_inputs.npz') as z:
        for name,expected in reference['cases'].items():
            actual=describe(z[name])
            for key,value in expected.items():
                if name=='bernoulli' and key=='ess_tail':
                    # 95th percentile is 1: its indicator is constant. Our
                    # registered rule does not turn that into ESS=N.
                    assert actual[key] is None
                    continue
                assert np.isclose(actual[key],value,rtol=1e-10,atol=1e-10), (name,key,actual[key],value)
        assert describe(z['iid'])['rhat']<1.01
        assert describe(z['shifted'])['rhat']>1.1
        assert describe(z['scaled'])['rhat_folded']>1.1
        assert describe(z['sticky'])['ess_bulk']<200


def test_constants_and_support():
    d=describe(np.zeros((4,200)))
    assert d['rhat'] is None and d['ess_bulk'] is None and d['mcse_mean'] is None
    counts=np.zeros((4,200,2),dtype=int)
    assert not aggregate_diagnostics(counts,np.zeros((4,200)))['passed']
    # An all-zero sampled tail is unresolved absent a structural bound.
    f=formation_diagnostics(counts,np.array([2,2]),np.array([True,False]),np.array([0,0]),np.array([3,3]))
    assert f['formed']==1 and not f['passed']
    f=formation_diagnostics(counts,np.array([2,2]),np.array([True,False]),np.array([0,0]),np.array([1,1]))
    assert f['formed']==1 and f['passed']


def test_canonical_support_and_zero_rows():
    # Each of a,b is frequent, never build-co-mentioned, E=20*20/40=10.
    bd={i:({'a'} if i<20 else {'b'}) for i in range(40)}
    ed={('same',2020,0):{'a','b'},('same',2020,1):{'a','b'},('other',2020,0):{'z'}}
    a=canonical(bd,ed,lambda d:d[0],lambda d:(d[1],d[2]))
    b=canonical(dict(reversed(list(bd.items()))),dict(reversed(list(ed.items()))),lambda d:d[0],lambda d:(d[1],d[2]))
    assert all(np.array_equal(a[k],b[k]) for k in a)
    assert a['observed'].tolist()==[2] and a['supported'].tolist()==[False]
    assert a['eval_docs']==3 and len(a['quarters'])==2


def test_stratified_ensemble_and_reference():
    blocks={'2020Q1':[[0],[1],[0,2]],'2020Q2':[[2],[0,1],[1]]}
    pairs=np.array([[0,1],[0,2],[1,2]])
    e=Ensemble(blocks,3,pairs,'synthetic','N3','pilot')
    try:
        for _ in range(10): e.step()
        e.check(); counts,dist=e.sample()
        for c,cb in enumerate(e.chains):
            expected=np.zeros(3,dtype=int); delta=0
            for block,ch in cb.items():
                rows=ch.rows()
                expected += [sum(a in r and b in r for r in rows) for a,b in pairs]
                delta+=sum(len(set(r)^set(o)) for r,o in zip(rows,blocks[block]))
            assert np.array_equal(counts[c],expected) and dist[c]==delta
    finally: e.close()
    assert len({seed(ph,'N2','test',c,'all') for ph in ('pilot','production','init-pilot','init-production') for c in range(4)})==16


def test_stage_serialization_and_extension():
    import time
    blocks={'all':[[0],[1],[0,2],[1,2]]}
    e=Ensemble(blocks,3,np.array([[0,1]]),'synthetic','N2','pilot')
    # Stage artifacts must be beneath ROOT to record repository-relative paths.
    with tempfile.TemporaryDirectory(dir=ROOT/'work') as tmp:
        counts=[]; distances=[]
        try:
            a,d,meta=stage(e,counts,distances,8,None,Path(tmp),'pilot',time.monotonic())
            assert a.shape==(4,8,1) and d.shape==(4,8)
            with np.load(ROOT/meta['raw_path']) as saved:
                assert np.array_equal(saved['counts'],a)
            b,_,_=stage(e,counts,distances,12,None,Path(tmp),'pilot',time.monotonic())
            assert np.array_equal(a,b[:,:8,:])
        finally: e.close()


if __name__=='__main__':
    for name,fn in sorted(list(globals().items())):
        if name.startswith('test_'): fn(); print('ok',name,flush=True)
