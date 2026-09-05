"""Canonical frozen matrix preparation; never samples a real-data null."""
import csv
import hashlib
import json
from pathlib import Path
import subprocess
import time
import numpy as np
from curveball import Curveball
from run_eval8 import eligible_set, pair_doc_counts, author_universe, thread_universe, FOLDS
from run_eval8_nulls import thread_doc_quarter
from run_paper2 import build_docs, load_rows, qdate, qlabel
from run_revision_queue import sha256

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT/'data/registry/nulls_revisions/curveball_v1'
REG = ROOT/'preregistration_nulls_n2.md'
HEADLINE = [f'p2_WSB_{k:02d}' for k in (1,2,3,4,5,18)] + ['p2_DD_04','p2_DD_05']
P1 = [f'p1_{s}_{f}' for s in ('author','thread') for f in ('fold1','fold2')]
ALL = HEADLINE + P1 + [f'p2_{s}_{k:02d}' for s in ('WSB','DD') for k in range(19)
                           if f'p2_{s}_{k:02d}' not in HEADLINE]


def registered():
    if not REG.read_text().startswith('# N2/N3 prospective') or 'STATUS: REGISTERED.' not in REG.read_text().split('---')[0]:
        raise RuntimeError('prospective registration missing')
    recorded = subprocess.check_output(['git','show','HEAD:preregistration_nulls_n2.md'],cwd=ROOT)
    if recorded != REG.read_bytes():
        raise RuntimeError('registration must be committed before preparation/chains')


def canonical(bdoc, edoc, author_fn, quarter_fn):
    fs, eligible = eligible_set(bdoc)
    labels = sorted(fs); ix = {v:i for i,v in enumerate(labels)}
    eligible = sorted(eligible)
    obs, docs = pair_doc_counts(edoc,fs,{p:i for i,p in enumerate(eligible)})
    support = np.asarray([len({author_fn(d) for d in docs.get(p,set())})>=2 for p in eligible])
    rows, ids, quarters = [],[],[]
    for d in sorted(edoc):
        row = sorted(ix[c] for c in edoc[d]&fs)
        if row:
            rows.append(row); ids.append(d)
            year,q = quarter_fn(d); quarters.append(f'{year}Q{q+1}')
    pairs = np.asarray([(ix[a],ix[b]) for a,b in eligible],dtype=np.uint32).reshape(-1,2)
    with Curveball(rows,len(labels),0) as kernel:
        if not np.array_equal(kernel.counts(pairs),obs):
            raise RuntimeError('native per-pair observed counts disagree')
    return dict(offsets=np.r_[0,np.cumsum([len(r) for r in rows])].astype(np.uint64),
                labels=np.asarray([c for r in rows for c in r],dtype=np.uint32),
                vocabulary=np.asarray(labels,dtype=str), pairs=pairs, observed=obs,
                supported=support, quarters=np.asarray(quarters,dtype=str),
                document_ids=np.asarray([json.dumps(d,ensure_ascii=False) for d in ids]),
                build_docs=np.asarray(len(bdoc)), eval_docs=np.asarray(len(edoc)))


def verify_sources(cell):
    checks = json.loads((ROOT/'reports/revision_input_checksums.json').read_text())
    selected = {n:h for n,h in checks.items() if
        (n=='data/paper2/ticker_mentions.parquet' if cell.startswith('p2_') else
         n=='data/registry/run5_author/author_concepts.parquet' if '_author_' in cell else
         n.startswith('data/docs/') or n=='data/registry/pilot1_concepts/claims.parquet')}
    for n,h in selected.items():
        if sha256(ROOT/n)!=h: raise RuntimeError(f'input hash mismatch: {n}')
    return selected


def prepare(cell):
    registered()
    if cell not in ALL: raise ValueError('unregistered cell')
    target = BASE/'matrices'/f'{cell}.npz'
    meta_path = ROOT/'reports'/f'curveball_matrix_{cell}.json'
    sources = verify_sources(cell)
    if meta_path.exists():
        meta = json.loads(meta_path.read_text())
        if not target.exists() or sha256(target)!=meta['matrix_sha256']:
            raise RuntimeError(f'matrix mismatch: {cell}')
        return target,meta
    if target.exists(): raise RuntimeError('orphan matrix preserved; inspect before reuse')
    start = time.monotonic()
    if cell.startswith('p2_'):
        _,s,ks = cell.split('_'); k=int(ks)
        rows = load_rows(s,'union')
        bd,ed = build_docs(rows,qdate(k),qdate(k+4)),build_docs(rows,qdate(k+4),qdate(k+6))
        data = canonical(bd,ed,lambda d:d[0],lambda d:(d[1],d[2]))
        with (ROOT/'reports/paper2_windows_z.tsv').open() as f:
            ref = next(r for r in csv.DictReader(f,delimiter='\t') if
                       (r['B'],r['window'],r['stratum'],r['lens'])==('4',str(k),s,'union'))
        expected_n = int(ref['n_eligible'])
        context = dict(B=4,window=k,stratum=s,lens='union',eval_start=qlabel(k+4),eval_end=qlabel(k+5))
    else:
        _,s,fold = cell.split('_')
        be,ee = next((b,e) for f,b,e in FOLDS if f==fold)
        bd,ed,author = (author_universe if s=='author' else thread_universe)(be,ee)
        tq = thread_doc_quarter() if s=='thread' else None
        data = canonical(bd,ed,author,(lambda d:tq[d]) if tq is not None else lambda d:(d[1],d[2]))
        ref_path = 'data/registry/run5_author/run8_author.json' if s=='author' else 'data/registry/pilot1_concepts/run8_thread.json'
        ref = json.loads((ROOT/ref_path).read_text())[fold]; expected_n = ref['eligible']
        context = dict(space=s,fold=fold)
    if len(data['pairs'])!=expected_n or int(data['observed'].sum())!=int(ref['obs_total']):
        raise RuntimeError('frozen observed census mismatch')
    if cell.startswith('p2_') and any(int(data[n])!=int(ref[n]) for n in ('build_docs','eval_docs')):
        raise RuntimeError('frozen document census mismatch')
    target.parent.mkdir(parents=True,exist_ok=True)
    with target.open('xb') as f: np.savez_compressed(f,**data)
    meta = dict(cell=cell,**context,matrix_path=str(target.relative_to(ROOT)),matrix_sha256=sha256(target),
                input_sha256=sources, registration_sha256=sha256(REG),
                code_sha256={n:sha256(ROOT/n) for n in ('eval/prepare_curveball.py',
                    'eval/run_eval8.py','eval/run_paper2.py','eval/run_gate.py','eval/curveball.py',
                    'eval/curveball_kernel.cpp','eval/run_eval8_nulls.py')},
                commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
                native_observed_per_pair_matches=True,eligible=len(data['pairs']),obs_total=int(data['observed'].sum()),
                active_rows=len(data['quarters']),eval_docs=int(data['eval_docs']),build_docs=int(data['build_docs']),
                columns=len(data['vocabulary']),incidences=len(data['labels']),
                arrays_sha256={n:hashlib.sha256(a.tobytes()).hexdigest() for n,a in data.items()},
                prepare_seconds=time.monotonic()-start)
    with meta_path.open('x') as f: json.dump(meta,f,indent=2); f.write('\n')
    return target,meta


def unpack(path,null):
    with np.load(path,allow_pickle=False) as z: data={k:z[k] for k in z.files}
    rows = [data['labels'][a:b].tolist() for a,b in zip(data['offsets'][:-1],data['offsets'][1:])]
    blocks = {'all':rows} if null=='N2' else {
        q:[rows[i] for i in np.flatnonzero(data['quarters']==q)] for q in sorted(set(data['quarters'].tolist()))}
    return data,blocks
