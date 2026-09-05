"""Render archived first-cell diagnostics without starting or altering chains."""
import argparse,json,hashlib
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[1]


def main():
    ap=argparse.ArgumentParser();ap.add_argument('cell');ap.add_argument('null',choices=['N2','N3'])
    a=ap.parse_args();record_path=ROOT/'reports'/f'curveball_{a.cell}_{a.null}.json'
    record=json.loads(record_path.read_text());phase=record.get('production',record['pilot'])
    st=phase['stages'][-1];raw=ROOT/st['raw_path']
    if hashlib.sha256(raw.read_bytes()).hexdigest()!=st['raw_sha256']:raise ValueError('raw hash mismatch')
    with np.load(raw,allow_pickle=False) as z:
        total=z['counts'].sum(axis=2);distance=z['distance']
    fig,ax=plt.subplots(2,2,figsize=(10,6.5),layout='constrained')
    colors=['#315a89','#bd642f','#2e7964','#8c5982']
    for c,color in enumerate(colors):
        ax[0,0].plot(np.arange(1,total.shape[1]+1),total[c],alpha=.6,lw=.6,color=color,label=f'Chain {c+1}')
        ax[0,1].plot(np.arange(1,distance.shape[1]+1),distance[c],alpha=.6,lw=.6,color=color)
        ax[1,0].hist(total[c],bins=24,density=True,histtype='step',color=color)
    ax[0,0].set(title='Total eligible-pair document count',xlabel='Saved sweep',ylabel='Count')
    ax[0,0].legend(ncol=4,fontsize=8,loc='upper right')
    ax[0,1].set(title='Distance from the observed matrix',xlabel='Saved sweep',ylabel='Changed binary entries')
    ax[1,0].set(title='Agreement across production chains',xlabel='Total count',ylabel='Density')
    values=[]
    for stage in phase['stages']:
        d=stage['diagnostics'][0]
        values.append([stage['sweeps'],d['total']['ess_bulk'],d['total']['ess_tail'],d['distance']['ess_bulk']])
    values=np.asarray(values)
    for i,label in enumerate(['Total: bulk ESS','Total: tail ESS','Distance: bulk ESS'],1):
        ax[1,1].plot(values[:,0],values[:,i],'o-',label=label)
    ax[1,1].axhline(400,color='#777777',ls='--',lw=.9,label='Registered minimum')
    ax[1,1].set(title='Stage diagnostics (failed stages retained)',xlabel='Saved sweeps per chain',ylabel='Effective sample size')
    ax[1,1].legend(fontsize=8)
    for aa in ax.flat:
        aa.spines[['top','right']].set_visible(False);aa.grid(alpha=.15)
    d=st['diagnostics'][0]['total']
    fig.suptitle(f"{a.cell} / {a.null}: {phase['status']} aggregate diagnostics\n"
                 f"rank/folded R-hat {d['rhat']:.4f}; mean MCSE {d['mcse_mean']:.3f}; SD MCSE {d['mcse_sd']:.3f}",fontsize=12)
    out=ROOT/'reports/figures'/f'curveball_{a.cell}_{a.null}_diagnostics.png'
    fig.savefig(out,dpi=180);plt.close(fig)
    out.with_suffix('.json').write_text(json.dumps(dict(source=str(record_path.relative_to(ROOT)),
        source_sha256=hashlib.sha256(record_path.read_bytes()).hexdigest(),raw_sha256=st['raw_sha256'],
        output_sha256=hashlib.sha256(out.read_bytes()).hexdigest(),
        note='Finite diagnostics are evidence, not proof of mixing.'),indent=2)+'\n')
    print(out)


if __name__=='__main__':main()
