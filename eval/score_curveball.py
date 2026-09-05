"""Score fixed N2/N3 predictions using verified production artifacts only."""
import json
from pathlib import Path
from prepare_curveball import ALL, P1, ROOT
from run_revision_queue import sha256
from score_nulls_amendment import table,key,verdict,score_onset


def checked(path):
    record=json.loads(path.read_text())
    meta=record['matrix']
    if sha256(ROOT/meta['matrix_path'])!=meta['matrix_sha256']: raise ValueError('matrix hash mismatch')
    for phase in ('pilot','production'):
        for stage in record.get(phase,{}).get('stages',[]):
            if sha256(ROOT/stage['raw_path'])!=stage['raw_sha256']: raise ValueError('chain hash mismatch')
    return record


def main():
    original={key(r):r for r in table('paper2_windows_z.tsv')}
    scores={}; all_records={}
    for null in ('N2','N3'):
        records={}
        for cell in ALL:
            path=ROOT/'reports'/f'curveball_{cell}_{null}.json'
            if path.exists(): records[cell]=checked(path)
        usable={c:r for c,r in records.items() if r.get('production',{}).get('status')=='PASS'}
        unavailable={c:('PENDING' if c not in records else records[c].get('production',records[c]['pilot'])['status']) for c in ALL if c not in usable}
        def score(required,predicate,evidence):
            missing={c:unavailable[c] for c in required if c in unavailable}
            if missing:
                return dict(status='UNRESOLVED' if any(v!='PENDING' for v in missing.values()) else 'PENDING',missing=missing)
            return verdict(predicate(),**evidence())
        p2=[c for c in ALL if c.startswith('p2_')]
        def rows():
            return [{**r['matrix'],**r['production']['summary']} for c,r in usable.items() if c.startswith('p2_')]
        def sign_failures():
            return [key(r) for r in rows() if abs(float(original[key(r)]['z_seg']))>=3 and
                    r['z_seg']*float(original[key(r)]['z_seg'])<=0]
        out={}
        sign_required=[c for c in p2 if abs(float(original[
            4,int(c.split('_')[2]),c.split('_')[1],'union']['z_seg']))>=3]
        out['X-a']=score(sign_required,lambda:not sign_failures(),lambda:dict(failures=sign_failures()))
        out['X-b']=score(p2,lambda:score_onset(rows())['window']==5 and all(score_onset(rows())[p] for p in ('P1','P2','P3')),lambda:score_onset(rows()))
        excursion=['p2_WSB_03','p2_WSB_04']
        out['X-c']=score(excursion,lambda:all(usable[c]['production']['summary']['z_seg']>=5 and usable[c]['production']['summary']['ratio']>1 for c in excursion),lambda:dict(cells={c:usable[c]['production']['summary'] for c in excursion}))
        out['X-d']=score(P1,lambda:all(usable[c]['production']['summary']['z_seg']<=-3 and usable[c]['production']['summary']['ratio']<1 for c in P1),lambda:dict(cells={c:usable[c]['production']['summary'] for c in P1}))
        out['X-e']=score(P1,lambda:all(usable[c]['production']['formation']['formed']<=.01*usable[c]['matrix']['eligible'] for c in P1),lambda:dict(counts={c:usable[c]['production']['formation']['formed'] for c in P1}))
        if all(c in usable for c in P1):
            unresolved=[c for c in P1 if not usable[c]['production']['formation']['passed']]
            if unresolved: out['X-e']=dict(status='UNRESOLVED',formation_precision_failures=unresolved,
                  provisional_counts={c:usable[c]['production']['formation']['formed'] for c in P1})
        out['inventory']=dict(completed_attempts=len(records),usable_production=len(usable),unavailable=unavailable)
        scores[null]=out
        all_records.update({f'{c}_{null}':dict(pilot=r['pilot']['status'],production=r.get('production',{}).get('status','NOT_RUN'),
                 pilot_seconds=r['pilot']['seconds'],production_seconds=r.get('production',{}).get('seconds',0),
                 summary=r.get('production',{}).get('summary'),source_sha256=sha256(ROOT/'reports'/f'curveball_{c}_{null}.json')) for c,r in records.items()})
    output=dict(predictions=scores,cells=all_records,public_release_ready=False,
                interpretation='Only production passing registered diagnostics is scored. Pilot and failed-chain outcomes remain archived.')
    (ROOT/'reports/curveball_scores.json').write_text(json.dumps(output,indent=2)+'\n')
    for null,values in scores.items(): print(null,{k:v['status'] for k,v in values.items() if k.startswith('X-')})


if __name__=='__main__': main()
