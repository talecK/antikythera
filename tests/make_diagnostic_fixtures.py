import json,sys
from pathlib import Path
import numpy as np
import arviz as az
rng=np.random.default_rng(714209)
cases={}
iid=rng.normal(size=(4,1000)); cases['iid']=iid
cases['shifted']=iid+np.arange(4)[:,None]
cases['scaled']=iid*np.array([1,1,1,4])[:,None]
eps=rng.normal(size=(4,2000)); sticky=eps.copy()
for t in range(1,2000): sticky[:,t]=.98*sticky[:,t-1]+eps[:,t]
cases['sticky']=sticky
cases['discrete']=rng.poisson(2,size=(4,1001))
cases['bernoulli']=rng.binomial(1,.97,size=(4,1000))
np.savez_compressed('tests/fixtures/mcmc_reference_inputs.npz',**cases)
out={}
for name,x in cases.items():
 out[name]=dict(rhat=float(az.rhat(x)),rhat_rank=float(az.rhat(x,method='z_scale')),
   rhat_folded=float(az.rhat(x,method='folded')),ess_bulk=float(az.ess(x,method='bulk')),
   ess_tail=float(az.ess(x,method='tail')),ess_mean=float(az.ess(x,method='mean')),
   ess_sd=float(az.ess(x,method='sd')),mcse_mean=float(az.mcse(x)),mcse_sd=float(az.mcse(x,method='sd')))
Path('tests/fixtures/mcmc_reference.json').write_text(json.dumps(dict(arviz=az.__version__,numpy=np.__version__,seed=714209,cases=out),indent=2)+'\n')
