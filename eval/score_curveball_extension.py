"""Score unchanged Paper 2 predictions after the single bounded extension."""
import json

from prepare_curveball import ROOT, ALL
from run_revision_queue import sha256
from score_curveball import checked
from score_nulls_amendment import table, key, score_onset, verdict


def main():
    original={key(r):r for r in table('paper2_windows_z.tsv')}
    cells=[c for c in ALL if c.startswith('p2_')]
    output={}
    for null in ('N2','N3'):
        usable={};missing={};sources={}
        for cell in cells:
            path=ROOT/'reports'/f'curveball_{cell}_{null}.json';first=checked(path)
            if first.get('production',{}).get('status')=='PASS':
                usable[cell]=first;sources[cell]=dict(attempt='first_pass',sha256=sha256(path));continue
            extension=ROOT/'reports'/f'curveball_extension1_{cell}_{null}.json'
            if not extension.exists():missing[cell]='PENDING_EXTENSION';continue
            r=json.loads(extension.read_text())
            if r['first_pass_sha256']!=sha256(path):raise ValueError('extension parent checksum mismatch')
            if r.get('production',{}).get('status')!='PASS':
                missing[cell]=r.get('production',r['pilot'])['status'];continue
            checked(extension)
            usable[cell]=r;sources[cell]=dict(attempt='extension1',sha256=sha256(extension))
        rows=[{**r['matrix'],**r['production']['summary']} for r in usable.values()]
        def score(required,fn):
            unavailable={c:missing[c] for c in required if c in missing}
            if unavailable:
                return dict(status='PENDING' if all(v=='PENDING_EXTENSION' for v in unavailable.values()) else 'UNRESOLVED',missing=unavailable)
            return fn()
        def sign():
            failures=[list(key(r)) for r in rows if abs(float(original[key(r)]['z_seg']))>=3 and r['z_seg']*float(original[key(r)]['z_seg'])<=0]
            return verdict(not failures,failures=failures)
        sign_required=[c for c in cells if abs(float(original[4,int(c.split('_')[2]),c.split('_')[1],'union']['z_seg']))>=3]
        def onset():
            o=score_onset(rows);return verdict(o['window']==5 and all(o[p] for p in ('P1','P2','P3')),**o)
        def excursion():
            values={c:usable[c]['production']['summary'] for c in ('p2_WSB_03','p2_WSB_04')}
            return verdict(all(v['z_seg']>=5 and v['ratio']>1 for v in values.values()),cells=values)
        output[null]={'X-a':score(sign_required,sign),'X-b':score(cells,onset),
                      'X-c':score(['p2_WSB_03','p2_WSB_04'],excursion),
                      'usable_cells':len(usable),'missing':missing,'sources':sources}
    result=dict(predictions=output,plan_sha256=sha256(ROOT/'reports/curveball_extension1_plan.json'),
                interpretation='Original first-pass scores are preserved separately. Only passing production is selected; no pooling of old unresolved trajectories, pilots or nulls.',public_release_ready=False)
    (ROOT/'reports/curveball_extension1_scores.json').write_text(json.dumps(result,indent=2)+'\n')
    for null,out in output.items():print(null,{k:v['status'] for k,v in out.items() if k.startswith('X-')})


if __name__=='__main__':main()
