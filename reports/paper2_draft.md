# Watching the walls go up: a registered study of the 2021 segregation transition in r/wallstreetbets

**Author:** Kevin Quiring (independent researcher)

**Draft v0.1, 2026-08-31. Registered study (preregistration_paper2.md,
commit 99ffd9e, amendments V1-V4). All numbers are from the
registration-conforming run (commit 21a9dc7); a disclosed implementation
deviation and its rule-bound correction are reported in Section 4.5.
Awaiting author prose pass.**

---

## Abstract

A companion study of idea segregation in online discourse (Quiring 2026,
"The gaps that don't close") found that concept pairs which should
co-occur but never have — suppressed pairs — stay apart at rates far
below chance in every community measured, on two platforms, with a
single exception: r/wallstreetbets before 2020 sat exactly at chance,
and by 2024 it was walled like everywhere else. That is the only
transition observed anywhere in this research program. Here we report a
registered study of when it happened and what the timing can and cannot
say about why. On a fresh single-source corpus of 98.1 million Reddit
posts and comments (2019-2024, one API, one pull era, never mixed with
the earlier corpus), rolling quarterly windows with a fully
pre-committed design test three registered predictions: that a
transition is visible and localizable at quarterly resolution (P1), that
its onset falls within 2021 (P2), and that the analysis-oriented control
stratum shows no comparable discontinuity (P3). All three pass.
r/wallstreetbets moves from chance-level mixing (z = +1.5, +1.5 in
consecutive pre-onset windows) to persistent walls (z between -4.6 and
-11.0 in all fourteen windows from onset onward, zero reversions), with
onset 2021-04-01. The central finding lies between those regimes: in the
two evaluation windows straddling the January 2021 GameStop episode,
suppressed ticker pairs co-mention 28.6 and 30.9 standard deviations
*above* their shuffle nulls — the only above-chance excursion in five
years of windows and the only one this program has observed at any
granularity on any platform. A forty-replicate truth-null placebo
running the full registered statistic confirms the machinery cannot
manufacture the excursion from its own mechanics: placebo z values are
distributed approximately as N(0,1), and the real values sit roughly 24
to 31 placebo standard deviations outside them. The control stratum
stays walled straight through the squeeze (z = -7.7, -8.6 in the same
two windows), so the fusion is community-specific, not era-wide. The
measured onset lands in the registered non-separable case — the
subscriber explosion and the governance overhaul were both active in
that quarter — so the timing is reported as ordering evidence, not as
mechanism identification. An implementation deviation caught after the
first run (an omitted ticker-exclusion filter) was corrected by
re-running the unchanged frozen rules; both runs are disclosed, their
outputs are both released, and they agree on every verdict.

---

## 1. Introduction

The companion paper to this study asked whether the machinery of
literature-based discovery — find concept pairs that statistically
should have met but have not, and treat them as latent connections —
transfers from scientific corpora to ordinary discourse. Its answer was
no, twice over: suppressed pairs do not connect above chance on either
of two platforms, and they actively co-occur far *below* chance, at
magnitudes their marginal popularities cannot explain (Quiring 2026).
The durable finding was the walls, not the bridges: communities of
attention around two never-connected ideas stay apart, decade after
decade, everywhere measured.

Everywhere except one place, once. In the replication corpus — Reddit
financial discussion, where the concept unit is the stock ticker,
regex-extracted with no language model in the loop — the meme-oriented
community r/wallstreetbets sat exactly at chance in the pre-2020 fold
(segregation z = -0.1, where an effect of the size seen in the
analysis-oriented subreddits would have registered near -7), and was
strongly walled in the post-2021 fold (z = -9.0), like every other
stratum. The companion paper reported this as a described observation
and declined to interpret it, for three stated reasons: the two folds
sit on opposite sides of the 2020-2021 market regime break (era
confound); they differ in acquisition provenance, with the source seam
aligned to the fold boundary (provenance confound); and the community
split itself was exploratory, with no registered prediction attached
(post-hoc). The observation nevertheless stands out in this program:
across twenty years of Hacker News at two granularities, six financial
subreddits, and the Science4Cast control, it is the only case in which
a measured discourse community changed segregation state at all.
Everything else is static. Walls, where we found them, persisted; the
one community without them grew them somewhere between 2019 and 2024.

This paper is the registered study of that transition. It asks three
questions, frozen as predictions before any statistic was computed:
does the transition resolve into a localizable event at quarterly
resolution, rather than an artifact of comparing two distant endpoints
(P1)? Does its onset fall within calendar 2021, the year of the
GameStop short squeeze and the moderation overhaul that followed it
(P2)? And is the transition specific to r/wallstreetbets, rather than
an era-wide shift that any finance community of the period would show
(P3)?

The design neutralizes the three confounds in order. A fresh corpus —
98.1 million posts and comments covering r/wallstreetbets and five
analysis-oriented control subreddits continuously from 2019 through
2024, acquired from a single source in a single pull era — removes the
provenance seam entirely, and a confirmatory Part A verifies that the
companion paper's walled endpoint survives on uniform provenance. A
rolling-window design over continuous time, with the control stratum
computed identically alongside, answers (though cannot eliminate) the
era confound: there is no fold boundary for a regime break to hide in,
and an era-wide effect would move both strata. And the registration —
committed, with its window definitions, thresholds, onset rule, and
primary cell frozen before any outcome was computed, with outcome-blind
census gates in between — removes the post-hoc character of the
original observation.

All three registered predictions pass. The transition is real, sharp,
and dated: onset 2021-04-01, with chance-level mixing before it and
walls in every window after it, zero reversions allowed or needed. But
the result we believe matters most was not one of the bets. Between the
chance-level regime and the walls, in exactly the two evaluation
windows that straddle the GameStop episode, the suppressed pairs of
r/wallstreetbets do not merely drift together — they fuse, co-mentioning
at 28.6 and 30.9 standard deviations above their calibrated nulls. In a
research program whose every other measurement on every platform sits
at or far below chance, this is the only above-chance excursion ever
observed. The control stratum, measured through the same windows by the
same machinery, stays walled throughout. A cascade, it appears, can do
in one quarter what years of ordinary discourse never does — and when
it recedes, it leaves walls where there were none.

The rest of the paper proceeds as follows. Section 2 states the source
observation and the question. Section 3 describes the corpus and its
outcome-blind integrity checks. Section 4 gives the registered design:
the rolling-window statistic, the outcome-blind census and window-length
ladder, the three predictions, the causal-anchor list, and the disclosed
deviation and correction. Section 5 reports the results: the endpoint
hardening (5.1), the transition (5.2), the excursion and its placebo
(5.3), the control contrast (5.4), and sensitivity (5.5). Section 6
discusses what the timing can and cannot identify, and clearly labels
the non-registered readings. Section 7 concludes.

## 2. The source observation and the question

The companion paper's replication corpus splits six financial
subreddits into two strata: MEME (r/wallstreetbets alone, hereafter
WSB) and DD (the union of five analysis-oriented subreddits:
r/SecurityAnalysis, r/ValueInvesting, r/StockMarket, r/stocks,
r/investing). The document is one author's ticker mentions within one
calendar quarter; a pair of frequently mentioned tickers is *eligible*
("suppressed") in a build window if its expected joint document count
is at least 2 while its observed co-mention count is zero; and the
segregation statistic is the total observed eval-window co-mention
count over all eligible pairs, standardized against a label-shuffle
null (Section 4.1). Two temporal folds bracket the 2020-2021 regime
break: build 2017-2018 with evaluation 2019 (fold A), and build
2022-2023 with evaluation 2024 (fold B).

The post-review gate table (companion paper Section 6.3; gate v2 run,
commit f89cb2b there) reads:

| stratum | fold A (eval 2019) | fold B (eval 2024) |
|---------|-------------------:|-------------------:|
| ALL (pooled) | -8.8 | -17.7 |
| DD | -10.1 | -17.1 |
| WSB | **-0.1** | **-9.0** |

(The registration for the present study, drafted from the pre-review
gate run, quotes the earlier values -0.2 and -8.7 for the WSB cells;
the difference is the gate's post-review exclusion fix plus Monte Carlo
noise and is immaterial to every bar here.)

WSB's fold-A chance reading is well measured: the registered
subsampling control matched to DD's document counts leaves it at chance
(z = -0.0), so it is not a power artifact, and a DD-sized effect would
have shown near z = -7. So the observation is: the one wall-free
community ever measured in this program grew walls somewhere between
2019 and 2024. The companion paper is final on that observation; this
study cites it and does not reopen it (its Section 6.3, gate table
commit 1386fc0). The question here is *when* the walls went up, at
quarterly resolution, and whether the timing — read against a
pre-committed list of dated governance events — can order the candidate
mechanisms.

The candidate mechanisms, stated before any window was computed
(registration; reports/paper2_seed.md):

- **Scale/fragmentation.** WSB grew roughly 30-fold in weeks around the
  January 2021 GameStop squeeze. If walls are internal tribalization of
  a suddenly enormous community, onset should track the subscriber
  explosion: fast, in or immediately after 2021Q1.
- **Governance.** After the squeeze, WSB's moderation regime changed
  wholesale — a mod-team regime change, automated ticker filtering,
  containment-by-megathread, and a market-cap floor on discussable
  tickers. If walls are topicality policing, onset should lag the event
  by months, tracking the datable rule changes through 2021.
- **Era narratives.** Market-wide sector stories sort attention
  everywhere at once; this predicts a parallel discontinuity in the DD
  control stratum. P3 is its test.

## 3. Corpus

### 3.1 Acquisition

The corpus is a fresh, single-source pull: the Arctic Shift API,
acquired 2026-08-31 in one fleet run (pipeline/pull_reddit_paper2.py;
runbook in the repository), landing 864 shard files — 72 monthly shards
of WSB posts and comments spanning 2019-01 through 2024-12, plus the
same 72 months for each of the five DD subreddits — totaling
98,084,631 rows (~5.6 GB compressed). It is never mixed with the
companion paper's corpus: one source, one pull era, uniform fields for
treatment and control strata alike. This uniformity is the design
answer to the provenance confound: there is no archival/API seam
anywhere in the data, and in particular none co-located with the
phenomenon under study.

Hygiene follows the program's frozen rules: deleted/removed authors and
AutoModerator dropped; deduplication by item id; ticker extraction by
the gate's frozen extractor (union lens primary, cashtag lens
sensitivity, committed stoplist, SEC registrant-table resolution,
macro-hub tickers excluded, hub guard at 50 tickers per document).
Extraction yields 11,200,484 ticker mentions (commit 8db5012; the
exclusion-filter deviation and correction affecting the downstream
loaders is disclosed in Section 4.5). The 2020-2021 regime-break years
are deliberately *included*: prior studies in this program excluded
them as a confound, but here the transition is the object of study
(registration, gate decision 2).

### 3.2 Outcome-blind integrity checks

Before any census or statistic was computed, every shard passed a
full-parse integrity check (pipeline/validate_paper2.py): no missing
shard, no unparseable line, no month with more than 1% out-of-span
timestamps, no month at zero or below 5% of its neighbours. The
complete per-shard volume table was committed as a dated amendment to
the registration (Amendment V1, commit 63b7f6e;
reports/paper2_volume_table.tsv) before any window census existed.
Spot-checks against the prior acquisition era's runbook match exactly
(e.g., 2022-06 = 1.13M, 2023-09 = 510K, 2024-03 = 962K WSB comments).

Two observations were recorded in that amendment, before any outcome
existed, precisely because a result could later be blamed on them. The
WSB volume series itself shows the era plainly — monthly comments run
around 300 thousand through 2019, spike to 2.6 million in March 2020
(COVID) and 8.0 million in January 2021 (GameStop), then decay to under
a million by 2023 — but volume is not the studied statistic, and the
shuffle null conditions on the realized documents of each window.
Second, one control subreddit (r/SecurityAnalysis) decays to a few
thousand comments per year by 2023-24; the DD control is registered as
the union of five subreddits, so this changes nothing, but the per-sub
sparsity was noted before anyone saw a result it could explain.

## 4. Registered design

The full registration (preregistration_paper2.md) was frozen and
committed, with the owner's explicit go recorded, before any outcome
statistic was computed (commit 99ffd9e); its amendments V1-V4 are dated
appendices, never rewordings. The study has two parts sharing one
acquisition.

### 4.1 Part B: rolling windows and the primary statistic

The document is one author's ticker set within one calendar quarter, as
everywhere in this program. Windows roll over the 24 quarters
2019Q1-2024Q4, stepped one quarter: window k has a build period of B
quarters and an evaluation period of the following 2 quarters (eval
length fixed). Eligibility per window is identical to the companion
paper's gate: a ticker is frequent at 20 or more distinct build
author-quarters; an eligible ("suppressed") pair has expected joint
count E = f_i·f_j/N ≥ 2 with zero observed build co-mentions.

The primary statistic per window is the program's run-8 segregation z:
the total observed eval co-mention document count over all eligible
pairs, standardized against a label-shuffle null (concept labels
permuted over the (document, ticker) incidences of the frequent set,
within-document duplicates collapsed; R = 100 replicates, numpy
default_rng seed 20260831). The evaluation script imports the gate's
machinery, so the statistic is identical by construction, and a
registered determinism rule (from the gate's adversarial review)
requires every incidence list to be sorted before permutation so that
no set or dict iteration order can feed the seeded RNG. The script
refuses to run unless the registration status is REGISTERED (commit
35914d2). Formation counts per window — eligible pairs newly
co-mentioning beyond their per-pair permutation threshold — are a
registered *secondary* readout with no bar attached: the gate's power
table shows them underpowered at these window sizes.

Both strata (WSB treatment, DD control) are computed identically and
independently, under both lenses (union primary, cashtag sensitivity;
a cashtag window with fewer than 20 eligible pairs is reported
UNINFORMATIVE, never as a negative).

### 4.2 Outcome-blind census gate and the window-length ladder

Window length B was chosen from {4, 6, 8} quarters by a registered
ladder — the shortest B whose per-window census gives a median
eligible-pair count of at least 100 in the WSB/union cell — so that the
choice is a census property, not a researcher degree of freedom. The
census (eligibility structure only; the census script imports the
document builder but structurally cannot compute the statistic) was
computed, committed as a dated amendment, and owner-reviewed before the
first segregation z existed (Amendment V3, commit b86c378; corrected
census, Section 4.5, commit 80b3b37). The ladder chose **B = 4**: on
the corrected census the B=4 WSB/union cell has median 115 eligible
pairs per window (range 45-498 over 19 windows), and *no* window in any
B, either stratum, union lens, falls below the registered LOW-POWER
floor of 30 eligible pairs — every window enters the onset rule. B = 6
and B = 8 become registered sensitivity curves, computed and reported
regardless of outcome, so that the window-length choice cannot be what
makes a transition appear.

One census property was recorded in the amendment before any z existed,
and it binds how results are displayed: eligible-pair counts co-move
with era volume, so between-window z magnitudes are different-powered
tests. Per-window z values are each internally calibrated (the null
conditions on that window's realized documents), and the onset rule
uses only per-window threshold crossings; but any reader comparing raw
z magnitudes across windows is comparing tests whose eligible universes
differ by up to a factor of ten. For this reason every z series in this
paper — every figure and every table — carries its eligible-pair counts
alongside, and the figures plot the pair-count series directly beneath
the z series.

### 4.3 Registered predictions, onset rule, and primary cell

The onset rule, frozen verbatim: the onset window is the earliest
window w with z_w ≤ -3 such that every later window also has z ≤ -3,
allowing at most one later exception; the onset *time* is the start of
w's evaluation interval. If no such window exists, there is no onset.

- **P1 (existence):** at least 2 consecutive non-LOW-POWER windows with
  |z| < 3 before the onset window, and at least 2 consecutive windows
  with z ≤ -5 at or after it. Both halves required. The known endpoints
  make P1 the bet that the transition is visible and localizable at
  quarterly resolution rather than an artifact of the fold endpoints.
- **P2 (timing):** the onset time lies within [2021-01-01, 2021-12-31].
- **P3 (control specificity):** the DD/union series contains no window
  pair (w, w+1), both non-LOW-POWER, with z_w > -3 and z_{w+1} ≤ -5,
  anywhere in eval range 2020-01 through 2022-12 — no cliff. DD's
  deepening (fold A -10.1 to fold B -17.1) is predicted gradual.

P1 and P2 are scored on the WSB stratum, union lens, at the
ladder-chosen B = 4; P3 on the DD stratum, union lens, same B. No other
cell scores any bar (primary-cell clause, committed pre-outcome,
commit f004bfc). A secondary one-break step fit on the primary z series
(least-squares, all interior candidate breaks, near-tie set within 10%
of minimum SSE) was registered pre-census as an uncertainty band on the
onset date; no bar attaches to it.

The registration also states its own epistemic position plainly: the
two fold-level endpoints were known and could not be un-seen, so what
is registered as pre-outcome is everything between and around them — no
rolling-window statistic, no rebuilt-fold cell, and no per-window
census existed at registration time. The predictions bet on the shape
and timing of the transition, not on its existence at the endpoints.

### 4.4 Part A: provenance-hardening of the endpoint

Part A rebuilds the companion paper's fold B with the archival-dump
months replaced by API months from this pull — uniform API provenance
in both folds — and recomputes the WSB-dependent gate cells under the
frozen gate criterion, reusing the gate evaluation code verbatim (same
per-pair label-shuffle p99, R = 100, seed 20260831, formation floor,
and segregation z). Registered expectation: fold-B MEME segregation z
stays ≤ -3, i.e., the walled endpoint is real and not a provenance
artifact. Part A removes the provenance confound only; it says nothing
about timing.

### 4.5 Causal anchors, committed before any window

Because "the onset matches event X" is cheap after the fact, a list of
dated WSB governance events was collected and committed before any
rolling-window statistic existed (Amendment V2, commit 3fa0d73;
reports/paper2_anchors.md). Eight anchors A1-A8 span April 2020 through
August 2021: the pre-event removal of the subreddit's founder (A1,
2020-04); the GameStop squeeze and ~30x subscriber explosion (A2,
2021-01); the Discord ban and brief private-mode flip as moderation was
overwhelmed (A3, 2021-01-27); the mod-team regime change (A4,
2021-02-04/05); the automod ticker-filter bot, publicized by a WSB
moderator (A5, 2021-02); containment-by-daily-thread demonstrated on
crypto and reversed within a day (A6, 2021-04-14/15); the final GME
megathread, pushing single-ticker attention out to spin-off subreddits
(A7, 2021-04-16); and the sub-$1B market-cap discussion ban (A8, in
force by 2021-08; its introduction date is flagged in the amendment as
unpinned and unusable for timing claims).

The amendment freezes the discrimination reading in advance: onset in
2021Q1 favors scale/fragmentation (A2); onset in late 2021 favors
governance (A4-A8); **onset in 2021Q2 is the non-separable case, with
both mechanism families active, and supports neither over the other**.
Any timing comparison against an event not on this list is labelled
exploratory. The DD subreddits share none of A3-A8, which is what gives
P3 its bite against era-wide narratives.

### 4.6 Disclosed deviation and rule-bound correction (Amendment V4)

The first full run of the three paper-2 scripts (census, rolling
windows, Part A) deviated from the registered spec: the scripts loaded
mention rows directly from the extraction parquet and omitted the
load-time excluded-tickers filter (SPY, QQQ, VIX, BTC, ETH) that the
gate applies as its frozen macro-hub exclusion and that this
registration incorporates by reference ("identical to the gate"). The
omission was found by a code diff during cross-checking against the
gate's tables, *after* first-run outcomes had been seen, and is
disclosed as Amendment V4 (commit fbf3ace) with a rule-bound correction
path: the filter was added to the three loaders; the census was
re-derived and the window-length ladder re-decided by the unchanged
registered rule (B = 4 stands; committed before any corrected z
existed, commit 80b3b37); Parts A and B were re-run under the unchanged
bars, seeds, and window definitions. No bar, threshold, seed, window
definition, or onset rule changed at any point.

Because first-run outcomes were seen before the correction, the
protection is exactly that every re-derivation step is a frozen rule
with no free parameter. Both runs are released: the first-run outputs
are retained as superseded artifacts
(reports/paper2_windows_z_v1_superseded.tsv,
reports/paper2_window_census_v1_superseded.tsv), the conforming run's
outputs are the operative tables (reports/paper2_windows_z.tsv,
reports/paper2_window_census.tsv), and **the two runs agree on every
verdict**: same onset window, same P1/P2/P3 outcomes, same excursion
and control readings. Every number in Section 5 is from the conforming
run (commit 21a9dc7). A related target correction is disclosed in the
same amendment: the census consistency anchor recorded in Amendment V3
compared two pre-exclusion quantities (their agreement was real but
old-vs-old); the operative target is the gate v2 census value, and the
corrected comparison is reported in Section 5.5.

## 5. Results

All numbers in this section are from the registration-conforming run
(reports/paper2_windows_z.tsv and reports/paper2_results.md, commit
21a9dc7). Throughout, every z series is tabulated with its eligible-pair
counts, per the registered display rule (Section 4.2): between-window z
magnitudes are different-powered tests, and the pair counts are the
power context.

### 5.1 The endpoint survives uniform provenance (Part A)

Rebuilt with uniform API provenance in both folds, the fold-B endpoint
cells read (frozen gate criterion; gate v2 mixed-provenance values in
parentheses for comparison):

| cell | eligible pairs | z (uniform API) | z (gate v2, mixed) | formed | binomial p |
|------|---------------:|----------------:|-------------------:|-------:|-----------:|
| WSB (MEME)/union | 210 | **-9.40** | -9.0 | 0 | 1.00 |
| ALL/union | 479 | **-21.57** | -17.7 | 2 | 0.95 |
| DD/union | 281 | **-16.41** | -17.1 | 0 | 1.00 |

The registered expectation (WSB fold-B z ≤ -3) is met with a wide
margin, and the eligible-pair counts track the gate v2 census (210
versus 209). The cashtag sensitivity lens is directionally consistent
(-8.5/-10.1/-3.1; reports/paper2_results.md). The companion paper's
walled endpoint is therefore not a provenance artifact; the provenance
confound is removed from that observation, and the transition study
below runs on ground whose far end is secured.

### 5.2 The transition: onset 2021-04-01, all three predictions pass

The primary cell — WSB stratum, union lens, B = 4, nineteen rolling
windows with two-quarter evaluation intervals from 2020Q1 through
2024Q4 — produces this series (eval labelled by starting quarter):

| eval start | 20Q1 | 20Q2 | 20Q3 | 20Q4 | 21Q1 | 21Q2 | 21Q3 | 21Q4 | 22Q1 | 22Q2 | 22Q3 | 22Q4 | 23Q1 | 23Q2 | 23Q3 | 23Q4 | 24Q1 | 24Q2 | 24Q3 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| z | -3.7 | +1.5 | +1.5 | **+28.6** | **+30.9** | -10.7 | -9.0 | -8.6 | -5.9 | -7.3 | -4.9 | -9.7 | -4.6 | -7.7 | -6.7 | -7.2 | -11.0 | -5.3 | -6.3 |
| eligible pairs | 45 | 77 | 64 | 124 | 318 | 498 | 391 | 373 | 397 | 225 | 146 | 115 | 99 | 94 | 103 | 78 | 71 | 93 | 131 |

Applying the frozen onset rule mechanically: the onset window is the
one whose evaluation interval begins 2021Q2 (z = -10.7), because every
one of the thirteen subsequent windows also has z ≤ -3 — zero
reversions, where the rule allowed one. **The onset time is
2021-04-01.** (The first window, at -3.7, does not start an onset: the
rule requires persistence, and the four windows after it include two at
chance and two far above it.)

- **P1 PASS.** Two consecutive windows with |z| < 3 precede the onset
  (eval 2020Q2 and 2020Q3, both +1.5), and two consecutive windows with
  z ≤ -5 sit at and after it (-10.7, -9.0). The transition is visible
  and localizable at quarterly resolution.
- **P2 PASS.** The onset time 2021-04-01 lies within the registered
  interval [2021-01-01, 2021-12-31].

The registered secondary step fit agrees and adds no uncertainty band:
the least-squares one-break fit places the break immediately before the
2021Q2 evaluation window, and the near-tie set (breaks within 10% of
minimum SSE) contains that break alone. At this resolution the
transition is as sharp as the design can express: chance-level mixing
through 2020Q3, and walls in every window from 2021Q2 to the end of the
data, three and a half years without a single reversion.

### 5.3 The central finding: the cascade excursion

Between the chance-level regime and the walls sit two windows the
series above already shows. They deserve to be read slowly. In the two
evaluation windows straddling the GameStop episode — eval 2020Q4-2021Q1
and eval 2021Q1-2021Q2 — the suppressed pairs of WSB co-mention not at
chance, and not below it, but at **+28.6 and +30.9 standard deviations
above** their label-shuffle nulls:

| cell (B=4, union) | eligible pairs | observed co-mentions | null mean | z | formed (secondary) | binomial p |
|---|---:|---:|---:|---:|---:|---|
| WSB eval 2020Q4-2021Q1 | 124 | 1,125 | 485.3 | **+28.6** | 24 | 1e-23 |
| WSB eval 2021Q1-2021Q2 | 318 | 2,891 | 1,707.9 | **+30.9** | 61 | 1e-57 |
| DD eval 2020Q4-2021Q1 | 145 | 570 | 780.9 | -7.7 | 1 | 0.77 |
| DD eval 2021Q1-2021Q2 | 211 | 522 | 771.4 | -8.6 | 0 | 1.0 |

The excursion claim rests on the primary z — the same statistic, same
null, same seed as every other window in the series. The formation
counts are the registered secondary readout and point the same way: 24
of 124 and 61 of 318 eligible pairs newly co-mention beyond their
per-pair permutation thresholds, against a 1-percent-per-pair floor
(binomial p ≈ 1e-23 and 1e-57). In the companion paper's terms: across
two platforms, two unit vocabularies, and every ordinary window ever
measured, formation sat at the false-positive floor; these two windows
are the only place in the program it has ever risen above it. But no
registered bar attaches to formation here, by design — the claim is
z-first, and the z is unambiguous.

**The placebo.** An excursion this large, in this program, triggers
reflexive suspicion: the companion paper's central cautionary result
was a formation effect manufactured by the measuring stick, caught by a
label-shuffle placebo. The same pattern was therefore turned on this
excursion (post-registration robustness check, in the registered
placebo's mold; commit 7bef4a2). Forty truth-null replicates — an
*outer* label shuffle that destroys any real author-ticker association,
with the full registered statistic (eligibility construction, inner
shuffle null, R = 100) recomputed from scratch per replicate, 20
replicates per excursion window, per-replicate seeds documented — ask
whether the machinery can produce the excursion from GME-era document
structure alone:

| window (eval) | placebo z mean | sd | min | max | placebo formed max | real z / formed |
|---|---:|---:|---:|---:|---:|---|
| 2020Q4-2021Q1 | +0.47 | 1.18 | -1.45 | +3.25 | 4 | **+28.6** / 24 |
| 2021Q1-2021Q2 | +0.30 | 0.99 | -1.71 | +2.53 | 7 | **+30.9** / 61 |

Under truth-null the statistic behaves like a standard normal, exactly
as a calibrated instrument should; the real values sit roughly 24 and
31 placebo standard deviations outside their placebo distributions. The
excursion is in the data, not the machinery. This answers, for this
specific regime, the densification concern that killed the companion
paper's author-space formation result: extreme document-size and
volume heterogeneity in the GME-era windows does not, by itself,
produce anything resembling the observed values.

What the excursion says, in the measured terms of this program: for two
overlapping half-year evaluation windows, ticker pairs that the
preceding year of WSB discourse had kept fully apart — never one
co-mention, despite ample independent popularity — were co-mentioned
by the same authors at two to three times their expected rates, in
thousands of documents. The walls did not merely pause; the mixing
deficit inverted. Everything this program measured before and after —
including WSB itself, one quarter later — sits at or far below chance.

### 5.4 Specificity: the control stays walled through the squeeze

The DD stratum, computed identically through the same calendar:

| eval start | 20Q1 | 20Q2 | 20Q3 | 20Q4 | 21Q1 | 21Q2 | 21Q3 | 21Q4 | 22Q1 | 22Q2 | 22Q3 | 22Q4 | 23Q1 | 23Q2 | 23Q3 | 23Q4 | 24Q1 | 24Q2 | 24Q3 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| z | -8.1 | -9.8 | -8.9 | -7.7 | -8.6 | -11.6 | -10.7 | -10.3 | -9.6 | -9.4 | -7.2 | -8.0 | -6.7 | -10.2 | -10.1 | -10.6 | -11.2 | -12.1 | -15.7 |
| eligible pairs | 63 | 104 | 151 | 145 | 211 | 345 | 272 | 281 | 290 | 250 | 179 | 158 | 150 | 139 | 128 | 143 | 120 | 127 | 161 |

- **P3 PASS.** Every DD window in the registered range (and in fact
  every DD window, period) sits between -6.7 and -15.7: no window pair
  anywhere shows the registered cliff pattern (chance-level then
  z ≤ -5), because no DD window is ever above -6.7 to begin with.

The contrast carries the paper's specificity claim, and it is starkest
exactly where it matters. In the two excursion windows — the squeeze
itself, the period when GameStop was the front page of the financial
internet — the analysis-oriented communities' suppressed pairs stayed
*below* chance (-7.7, -8.6). Whatever fused WSB's idea-communities in
those quarters was not the era, not the news cycle, and not the
market-wide meme-stock narrative, all of which DD's authors lived
through in the same corpus under the same statistic. The fusion and the
subsequent wall-building are properties of one community. DD's own
deepening over the five years (from around -8 toward -15.7) is gradual,
as predicted.

### 5.5 Sensitivity, consistency, and power context

**Window length.** The registered sensitivity curves reproduce the
shape at both alternative window lengths. At B = 6 the excursion
windows read +32.2 and +46.0 and the flip to walls occurs at the same
eval window (2021Q2, z = -8.9, all subsequent windows ≤ -5); at B = 8
the single in-range excursion window reads +27.3 with the flip likewise
at 2021Q2 (-7.6). No bar attaches to these curves; they are reported
regardless of outcome so that the ladder's choice of B = 4 cannot be
what makes the transition appear. (Longer builds start later in the
calendar, so the B = 6 and B = 8 series begin at eval 2020Q3 and 2021Q1
respectively; full series with pair counts in
reports/paper2_windows_z.tsv.)

**Lens.** The cashtag lens is registered sensitivity with an
informativeness floor: windows under 20 eligible pairs are reported
UNINFORMATIVE, which claims several early windows (and most DD cashtag
windows). Where informative, the cashtag series shows the same
signature: elevated in the excursion windows (+2.0, +2.5 at B = 4, with
formation 9/63 and 14/117, binomial p ≈ 1e-8 and 1e-11), then negative
in every window from 2021Q2 onward. The cashtag excursion z is far
smaller than the union value on a far smaller eligible universe; it is
reported as directional sensitivity, not as a second measurement of the
magnitude.

**Census consistency.** The corrected census's first B = 4 window
(build year 2019) counts 44,013 WSB/union build documents; the gate v2
census counts 44,012 fold-A MEME eval documents over the same year by
the same construction. Two corpora pulled independently, months apart,
agree to one document in 44 thousand — near-exact, not identical, and
reported as such (Amendment V4 addendum; the superseded V3 anchor had
matched two pre-exclusion values exactly).

**Power context, restated.** Eligible-pair counts range 45-498 across
the primary series; the deep-wall z values of 2021-2022 sit on the
largest universes (373-498 pairs) and the pre-onset chance readings on
the smallest (45-77). The onset rule is threshold-based and per-window
calibrated, so this cannot move a verdict, but it is why the figures
place the pair-count series directly under every z panel, and why we
do not interpret, e.g., -11.0 (2024Q1, 71 pairs) as deeper than -9.0
(2021Q3, 391 pairs).

<!-- DRAFT CONTINUES -->
