"""NumPy-only rank/folded R-hat and multichain ESS (Vehtari et al. 2021).

Formulas cross-validated against ArviZ 0.22.0; constants intentionally
return undefined diagnostics instead of ArviZ's convention ESS=N.
"""
from statistics import NormalDist
import numpy as np


def split(x):
    n = x.shape[1] // 2
    return np.concatenate((x[:, :n], x[:, -n:]), axis=0)


def rank_normalize(x):
    _, inverse, counts = np.unique(x, return_inverse=True, return_counts=True)
    ranks = np.cumsum(counts) - (counts-1)/2
    probs = (ranks - 3/8)/(x.size + 1/4)
    z = np.asarray([NormalDist().inv_cdf(float(p)) for p in probs])
    return z[inverse].reshape(x.shape)


def rhat_basic(x):
    w = x.var(axis=1, ddof=1).mean()
    if w == 0:
        return float('nan') if np.ptp(x) == 0 else float('inf')
    return float(np.sqrt((x.shape[1]-1)/x.shape[1] + x.mean(axis=1).var(ddof=1)/w))


def ess(x):
    """Geyer initial-positive/monotone multichain autocorrelation estimate."""
    x = np.asarray(x, dtype=float)
    if np.ptp(x) == 0:
        return float('nan')
    m, n = x.shape
    centered = x - x.mean(axis=1, keepdims=True)
    fft = np.fft.rfft(centered, n=1 << (2*n-1).bit_length(), axis=1)
    ac = np.fft.irfft(fft*np.conjugate(fft), axis=1)[:, :n]/n
    w = ac[:, 0].mean()*n/(n-1)
    vp = w*(n-1)/n + x.mean(axis=1).var(ddof=1)
    rho = 1 - (w - ac.mean(axis=0))/vp
    rho[0] = 1
    # Retain adjacent positive sums, then make them nonincreasing.
    kept = np.zeros(n)
    kept[:2] = rho[:2]
    even, odd, t = rho[0], rho[1], 1
    while t < n-3 and even+odd > 0:
        even, odd = rho[t+1:t+3]
        if even+odd >= 0:
            kept[t+1:t+3] = even, odd
        t += 2
    last = t-2
    if even > 0:
        kept[last+1] = even
    for j in range(1, last-1, 2):
        if kept[j+1:j+3].sum() > kept[j-1:j+1].sum():
            kept[j+1:j+3] = kept[j-1:j+1].sum()/2
    tau = max(-1 + 2*kept[:last+1].sum() + kept[last+1:last+2].sum(),
              1/np.log10(m*n))
    return float(m*n/tau)


def describe(x):
    x = np.asarray(x, dtype=float)
    if x.ndim != 2 or x.shape[0] < 2 or x.shape[1] < 4 or not np.isfinite(x).all():
        raise ValueError('finite chains x draws array, >=2 chains and >=4 draws required')
    out = dict(mean=float(x.mean()), sd=float(x.std()), draws=int(x.size),
               constant=bool(np.ptp(x) == 0))
    if out['constant']:
        return {**out, **dict.fromkeys(('rhat','rhat_rank','rhat_folded','ess_bulk',
                  'ess_tail','ess_mean','ess_sd','mcse_mean','mcse_sd'), None)}
    sx = split(x)
    ranked = rank_normalize(sx)
    rank_r = rhat_basic(ranked)
    folded_r = rhat_basic(rank_normalize(abs(sx-np.median(sx))))
    # A two-valued trace can have a constant fold; the rank component
    # still exists. Preserve undefined fold explicitly, never call it 1.
    rh = rank_r if np.isnan(folded_r) else max(rank_r, folded_r)
    em = ess(sx)
    c2 = (x-x.mean())**2
    es = ess(split(c2))
    tails = [ess(split(x <= np.quantile(x,p))) for p in (.05,.95)]
    out.update(rhat=rh, rhat_rank=rank_r, rhat_folded=folded_r,
               ess_bulk=ess(ranked), ess_tail=min(tails) if all(np.isfinite(tails)) else float('nan'),
               ess_mean=em, ess_sd=es,
               mcse_mean=float(x.std(ddof=1)/np.sqrt(em)),
               mcse_sd=float(np.sqrt(c2.var()/es/(4*c2.mean()))))
    return {k: (None if isinstance(v,float) and not np.isfinite(v) else v) for k,v in out.items()}


def basic_pass(d):
    return d['rhat'] is not None and d['rhat'] < 1.01 and \
        d['ess_bulk'] is not None and d['ess_bulk'] >= 400


def aggregate_diagnostics(counts, distance):
    total = describe(counts.sum(axis=2))
    dist = describe(distance)
    good = basic_pass(total) and basic_pass(dist) and total['ess_tail'] is not None \
        and total['ess_tail'] >= 400 and total['mcse_mean'] is not None \
        and total['mcse_sd'] is not None and total['mcse_mean'] <= .05*total['sd'] \
        and total['mcse_sd'] <= .05*total['sd']
    n = counts.shape[2]
    panel = np.unique(np.linspace(0,n-1,min(16,n)).astype(int)) if n else []
    return dict(passed=bool(good), total=total, distance=dist,
                panel={str(i):describe(counts[:,:,i]) for i in panel})


def formation_diagnostics(counts, observed, supported, lower, upper):
    pooled = counts.reshape(-1, counts.shape[2])
    p99 = np.percentile(pooled,99,axis=0)
    mask = supported & (observed>=2)
    formed = mask & (observed>p99)
    leave = [int(np.sum(mask & (observed > np.percentile(
        np.delete(counts,c,axis=0).reshape(-1,counts.shape[2]),99,axis=0)))) for c in range(4)]
    checks = {}
    for j in np.flatnonzero(mask):
        if upper[j] < observed[j] or lower[j] >= observed[j]:
            expected = upper[j] < observed[j]
            checks[str(j)] = dict(passed=bool(formed[j] == expected), structural=True)
            continue
        d = describe(counts[:,:,j] < observed[j])
        good = basic_pass(d) and d['ess_mean'] is not None and d['ess_mean']>=400
        if good:
            lo,hi = d['mean']-2*d['mcse_mean'],d['mean']+2*d['mcse_mean']
            good = (lo>.99 and formed[j]) or (hi<.99 and not formed[j])
        checks[str(j)] = dict(passed=bool(good), diagnostic=d)
    return dict(formed=int(formed.sum()), formed_indices=np.flatnonzero(formed).tolist(),
                leave_one_chain_out=leave, checks=checks,
                passed=all(d['passed'] for d in checks.values()) and len(set(leave+[int(formed.sum())]))==1)
