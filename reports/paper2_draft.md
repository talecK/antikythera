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

<!-- DRAFT CONTINUES -->
