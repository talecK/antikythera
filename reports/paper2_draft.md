# Watching the walls go up: r/wallstreetbets segregated in the quarter after the GameStop squeeze

**Author:** Kevin Quiring (independent researcher)

**Draft v0.4, 2026-09-01. Registered study (preregistration_paper2.md,
commit 99ffd9e, amendments V1-V4). All numbers are from the
registration-conforming run (commit 21a9dc7); a disclosed implementation
deviation and its rule-bound correction are reported in Methods.
Commit references for every quantity are collected in the provenance
appendix. Structured as Introduction, Results, Discussion, Methods.
Author prose pass in progress.**

---

## Abstract

Online communities keep ideas apart. Across Hacker News and Reddit,
concept pairs that should co-occur but never have stay apart at rates
far below chance. We call this a wall. The exception was
r/wallstreetbets: at chance before 2020, walled by 2024 like everywhere
else. Here we report a registered study of when that happened, using
rolling quarterly windows over a fresh single-source corpus of 98.1
million Reddit posts and comments, 2019 to 2024. Three predictions
committed in advance all pass. The community moves from chance-level
mixing to persistent walls, onset 2021-04-01, with zero reversions. In
the two windows straddling the January 2021 GameStop episode,
suppressed ticker pairs co-mention 28.6 and 30.9 standard deviations
above their shuffle nulls. It is the only above-chance excursion this
research program has observed, and shuffled data never produce it.
Analysis-oriented control communities stay walled through the squeeze,
so the excursion is specific to r/wallstreetbets. Two causes were in
play, thirty-fold growth during the squeeze and a moderation overhaul
after it, and we decided in advance that a mid-2021 onset could point
to either. Segregation transitions in online communities can be
measured and dated, but their timing alone cannot identify the
mechanisms behind them.

---

## Introduction

Online communities sort attention. People who discuss one idea tend
not to discuss another, and the structure of who talks about what is
among the most stable features of a platform (McPherson, Smith-Lovin
and Cook 2001; Cinelli et al. 2021; Waller and Anderson 2021). The
companion paper to this study measured a specific form of that sorting
(Quiring 2026). It borrowed the machinery of literature-based
discovery, which finds concept pairs that statistically should have met
but have not and treats them as latent connections (Swanson 1986), and
asked whether that machinery transfers from scientific corpora to
ordinary discourse. It found no formation signal on either of two
platforms, and it found that suppressed pairs actively co-occur far
below chance, at magnitudes their marginal popularities cannot explain.
The stable result was segregation: the communities of attention around
two never-connected ideas stay apart, on every platform and at every
granularity measured. Throughout this paper we call that persistent
below-chance separation a wall, and a community whose suppressed pairs
sit far below chance walled.

There was one exception. The companion paper's replication corpus is
Reddit financial discussion, where the concept unit is the stock
ticker, regex-extracted with no language model in the loop. It splits
six financial subreddits into two strata: MEME (r/wallstreetbets alone,
hereafter WSB) and DD (the union of five analysis-oriented subreddits:
r/SecurityAnalysis, r/ValueInvesting, r/StockMarket, r/stocks,
r/investing). The document is one author's ticker mentions within one
calendar quarter. A pair of frequently mentioned tickers is *eligible*
("suppressed") in a build window if its expected joint document count
is at least 2 while its observed co-mention count is zero. The
segregation statistic is the total observed eval-window co-mention
count over all eligible pairs, standardized against a label-shuffle
null (Methods). Two temporal folds bracket the 2020-2021 regime break:
build 2017-2018 with evaluation 2019 (fold A), and build 2022-2023 with
evaluation 2024 (fold B). The post-review gate table (companion paper,
"A second platform"; gate v2 run) reads:

| stratum | fold A (eval 2019) | fold B (eval 2024) |
|---------|-------------------:|-------------------:|
| ALL (pooled) | -8.8 | -17.7 |
| DD | -10.1 | -17.1 |
| WSB | **-0.1** | **-9.0** |

(The registration for the present study, drafted from the pre-review
gate run, quotes the earlier values -0.2 and -8.7 for the WSB cells.
The difference is the gate's post-review exclusion fix plus Monte Carlo
noise and is immaterial to every bar here.)

WSB's fold-A chance reading is well measured: the registered
subsampling control matched to DD's document counts leaves it at chance
(z = -0.0), so it is not a power artifact. A DD-sized effect would have
shown near z = -7. In the post-2021 fold WSB was strongly walled, like
every other stratum. The companion paper reported this as a described
observation and declined to interpret it, for three stated reasons. The
two folds sit on opposite sides of the 2020-2021 market regime break
(era confound). They differ in acquisition provenance, with the source
seam aligned to the fold boundary (provenance confound). And the
community split itself was exploratory, with no registered prediction
attached (post-hoc). The observation nevertheless stands out. Across
twenty years of Hacker News at two granularities, six financial
subreddits, and a science benchmark control, it is the only case in
which a measured community changed segregation state at all.
Everything else is static. The one wall-free community ever measured in
this program grew walls somewhere between 2019 and 2024. The companion
paper is final on that observation; this study cites it and does not
reopen it. The question here is *when* the walls went up, at quarterly
resolution, and whether the timing, read against a pre-committed list
of dated governance events, can order the candidate mechanisms.

The candidate mechanisms, stated before any window was computed
(registration; seed document in the code release):

- **Scale/fragmentation.** WSB grew roughly 30-fold in weeks around the
  January 2021 GameStop squeeze, from about 1.8 million to over 9
  million subscribers (anchor A2; dated sources in Methods). If walls
  are internal tribalization of a suddenly enormous community, onset
  should track the subscriber explosion: fast, in or immediately after
  2021Q1.
- **Governance.** After the squeeze, WSB's moderation regime changed
  wholesale: a mod-team regime change, automated ticker filtering,
  containment-by-megathread, and a market-cap floor on discussable
  tickers (anchors A4-A8; dated sources in Methods). If walls are
  topicality policing, onset should lag the event by months, tracking
  the datable rule changes through 2021.
- **Era narratives.** Market-wide sector stories sort attention
  everywhere at once; this predicts a parallel discontinuity in the DD
  control stratum. P3 is its test.

Four literatures border this study; none measures what it measures.
The GameStop episode itself has a substantial computational and
financial literature. Lucchini et al. (2022) show that a committed
minority of WSB users grew before the price surge and occupied central
network positions. Mancini et al. (2022) model the squeeze as
self-reinforcing consensus formation in WSB conversations. Semenova
and Winkler (2021) document social contagion in WSB asset discussions,
where engagement with a discussed asset raises a user's probability of
starting new discussions of it. Pedersen (2022) builds the equilibrium
theory: a social network propagating an investment idea produces
exactly the frenzy, bubble, and burst observed. All of this work
studies the cascade as the outcome: how coordination formed and how it
moved prices. The present study measures the other side of the event:
what the cascade did to the community's idea-structure, before, during,
and after, under a registered design. To our knowledge no prior work
tracks a community's co-attention structure through the episode.

Moderation interventions on Reddit have a causal-inference literature.
Chandrasekharan et al. (2017) measured the effects of the 2015
subreddit bans on hate speech; Trujillo and Cresci (2022) measured the
escalating quarantine-restrict-ban sequence applied to r/The_Donald.
These study platform-administered interventions and behavioral
outcomes (activity, toxicity). Our governance mechanism concerns
interventions from inside the community (a mod-team regime change,
automated ticker filtering, containment-by-megathread; anchors A3-A8),
and the outcome is the structure of the community's idea space rather
than the behavior of its users. Newcomer floods are a classic concern
of online-community research. Kiene, Monroy-Hernandez and Hill (2016)
found that r/NoSleep absorbed a large newcomer surge without major
incident; Lin et al. (2017) found that ten subreddits hit by
default-listing growth shocks stayed recognizably themselves. Both
studies find resilience, at growth scales far below WSB's roughly
30-fold explosion in weeks. Whether the transition we measure is what a
growth shock beyond that scale does to a community is exactly the scale
mechanism above, and the Discussion explains why this design cannot
settle it. Cascade theory, finally, predicts that a system's
susceptibility to global cascades depends on its connectivity
structure: cascades require enough overlap for a story to jump between
audiences (Watts 2002), and behaviors that need social reinforcement
spread only across wide bridges (Centola and Macy 2007), with
information cascades supplying the individual-level mechanism
(Bikhchandani, Hirshleifer and Welch 1992). The cascade-susceptibility
reading of our results, labelled speculative in the Discussion, is the
empirical cousin of this theory: chance-level mixing is the
connectivity substrate, and the walls are its removal. What this paper
adds to all four shelves is a registered, longitudinal measurement of
one community's idea-segregation state through a cascade, with a
calibrated null (the companion paper's machinery), a dated onset, and a
same-platform control.

This paper is the registered study of that transition. It asks three
questions, frozen as predictions before any statistic was computed.
Does the transition resolve into a localizable event at quarterly
resolution, rather than an artifact of comparing two distant endpoints
(P1)? Does its onset fall within calendar 2021, the year of the
GameStop short squeeze and the moderation overhaul that followed it
(P2)? And is the transition specific to r/wallstreetbets, rather than
an era-wide shift that any finance community of the period would show
(P3)?

The design addresses the three confounds in order. A fresh corpus of
98.1 million posts and comments covers r/wallstreetbets and five
analysis-oriented control subreddits continuously from 2019 through
2024, acquired from a single source in a single pull era. That removes
the provenance seam entirely, and a confirmatory Part A verifies that
the companion paper's walled endpoint survives on uniform provenance.
A rolling-window design over continuous time, with the control stratum
computed identically alongside, answers (though cannot eliminate) the
era confound: there is no fold boundary for a regime break to hide in,
and an era-wide effect would move both strata. The registration removes
the post-hoc character of the original observation: window definitions,
thresholds, onset rule, and primary cell were frozen and committed
before any outcome was computed, with outcome-blind census gates in
between.

All three registered predictions pass. The transition is real, sharp,
and dated: onset 2021-04-01, with chance-level mixing before it and
walls in every window after it, with zero reversions. The result we
consider most important, however, was not one of the bets. Between the
chance-level regime and the walls, in exactly the two evaluation
windows that straddle the GameStop episode, the suppressed pairs of
r/wallstreetbets co-mention at 28.6 and 30.9 standard deviations above
their calibrated nulls. In every other window this program has
measured, on any platform, co-mention over suppressed pairs sits at or
below chance; these two windows are the only exception. The control
stratum, measured through the same windows by the same machinery,
stayed below chance throughout. After the excursion recedes, the walls
appear and persist. r/wallstreetbets is the test case. The general
object is the transition between segregation states in a discourse
community, which no measurement in this program had previously caught
in progress. One community and one transition cannot say how common
such transitions are, and the Discussion returns to that limit.

## Results

All numbers in this section are from the registration-conforming run
(window series and results document listed in the provenance
appendix). Throughout, every z series is tabulated with its
eligible-pair counts, per the registered display rule (Methods):
between-window z magnitudes are different-powered tests, and the pair
counts are the power context.

### Measurement summary

The unit of observation is one author's set of ticker mentions within
one calendar quarter, as everywhere in this program. A ticker is
frequent in a build period if 20 or more distinct author-quarters
mention it. Among frequent tickers, a pair is eligible, or suppressed,
if its expected joint document count under independence is at least 2
while its observed co-mention count in the build period is zero: two
tickers each popular enough that chance alone should have put them in
the same author's quarter at least twice, yet never did. The
segregation statistic z for a window counts the documents in the
following evaluation period in which any eligible pair is co-mentioned,
and standardizes that total against a label-shuffle null that permutes
ticker labels over the document-ticker incidences of the frequent set,
with 100 replicates and a fixed seed. A z near zero means suppressed
pairs are co-mentioned about as often as chance predicts. A strongly
negative z means they are kept apart; a positive z means they are
brought together beyond chance. Windows roll over the 24 quarters of
2019 through 2024, stepped one quarter, with a build period of four
quarters and an evaluation period of the following two quarters, the
build length having been chosen by an outcome-blind census rule. Both
strata, WSB and DD, are computed identically and independently, under
a primary union lens and a cashtag sensitivity lens. Every window
definition, threshold, and rule was registered before any statistic
existed; full specifications are in Methods.

### Registered predictions and pre-committed readings

The registration fixed three predictions and, in a separate amendment
committed before any window statistic existed, fixed in advance how
each possible onset date would be read against the candidate
mechanisms. Both are summarized here; the verbatim rules are in
Methods.

| Registered item | Pre-committed reading | Observed |
|---|---|---|
| P1, existence: at least two consecutive chance-level windows before the onset window and at least two consecutive walled windows at or after it | The transition is visible and localizable at quarterly resolution, not an artifact of the fold endpoints | PASS: +1.5, +1.5 before; -10.7, -9.0 at and after |
| P2, timing: onset time within calendar 2021 | The transition belongs to the year of the squeeze and the moderation overhaul | PASS: onset 2021-04-01 |
| P3, control specificity: no chance-to-wall cliff anywhere in the DD series, 2020 through 2022 | The transition is a property of WSB, not of the era | PASS: every DD window between -6.7 and -15.7 |
| Onset in 2021Q1 | Favors scale/fragmentation (anchor A2) | Not observed |
| Onset in late 2021 | Favors governance (anchors A4-A8) | Not observed |
| Onset in 2021Q2 | Non-separable: both mechanism families active, supports neither over the other | Observed |

### The endpoint survives uniform provenance (Part A)

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
(-8.5/-10.1/-3.1; results document in the provenance appendix). The
companion paper's walled endpoint is therefore not a provenance
artifact; the provenance confound is removed from that observation, and
the transition study below runs on ground whose far end is secured.

### The transition: onset 2021-04-01, all three predictions pass

The primary cell (WSB stratum, union lens, B = 4, nineteen rolling
windows with two-quarter evaluation intervals from 2020Q1 through
2024Q4) produces this series, with evaluation windows labelled by
starting quarter:

| eval start | 20Q1 | 20Q2 | 20Q3 | 20Q4 | 21Q1 | 21Q2 | 21Q3 | 21Q4 | 22Q1 | 22Q2 | 22Q3 | 22Q4 | 23Q1 | 23Q2 | 23Q3 | 23Q4 | 24Q1 | 24Q2 | 24Q3 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| z | -3.7 | +1.5 | +1.5 | **+28.6** | **+30.9** | -10.7 | -9.0 | -8.6 | -5.9 | -7.3 | -4.9 | -9.7 | -4.6 | -7.7 | -6.7 | -7.2 | -11.0 | -5.3 | -6.3 |
| eligible pairs | 45 | 77 | 64 | 124 | 318 | 498 | 391 | 373 | 397 | 225 | 146 | 115 | 99 | 94 | 103 | 78 | 71 | 93 | 131 |

Applying the frozen onset rule mechanically: the onset window is the
one whose evaluation interval begins 2021Q2 (z = -10.7), because every
one of the thirteen subsequent windows also has z ≤ -3, with zero
reversions where the rule allowed one. **The onset time is
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

### The central finding: the cascade excursion

Between the chance-level regime and the walls sit two windows already
visible in the series above. In the two evaluation windows straddling
the GameStop episode (eval 2020Q4-2021Q1 and eval 2021Q1-2021Q2), the
suppressed pairs of WSB co-mention at 28.6 and 30.9 standard deviations
*above* their label-shuffle nulls:

| cell (B=4, union) | eligible pairs | observed co-mentions | null mean | z | formed (secondary) | binomial p |
|---|---:|---:|---:|---:|---:|---|
| WSB eval 2020Q4-2021Q1 | 124 | 1,125 | 485.3 | **+28.6** | 24 | 1e-23 |
| WSB eval 2021Q1-2021Q2 | 318 | 2,891 | 1,707.9 | **+30.9** | 61 | 1e-57 |
| DD eval 2020Q4-2021Q1 | 145 | 570 | 780.9 | -7.7 | 1 | 0.77 |
| DD eval 2021Q1-2021Q2 | 211 | 522 | 771.4 | -8.6 | 0 | 1.0 |

The excursion claim rests on the primary z, which is the same
statistic, same null, and same seed as every other window in the
series. The formation counts are the registered secondary readout and
point the same way: 24 of 124 and 61 of 318 eligible pairs newly
co-mention beyond their per-pair permutation thresholds, against a
1-percent-per-pair floor (binomial p of about 1e-23 and 1e-57). For
context: across two platforms, two unit vocabularies, and every
ordinary window ever measured in this program, formation sat at the
false-positive floor; these two windows are the only place it has ever
risen above it. No registered bar attaches to formation here, by
design. The claim is z-first, and the z is unambiguous.

**The placebo.** A result this far above chance calls for the same
scrutiny the companion paper applied to its own false positive: its
central cautionary finding was a formation effect manufactured by the
measuring stick, caught by a label-shuffle placebo. The same pattern
was applied to this excursion, as a post-registration robustness check
in the registered placebo's mold. Forty truth-null replicates ask
whether the machinery can produce the excursion from GME-era document
structure alone. Each replicate applies an *outer* label shuffle that
destroys any real author-ticker association, then recomputes the full
registered statistic from scratch (eligibility construction, inner
shuffle null, R = 100), with 20 replicates per excursion window and
per-replicate seeds documented:

| window (eval) | placebo z mean | sd | min | max | placebo formed max | real z / formed |
|---|---:|---:|---:|---:|---:|---|
| 2020Q4-2021Q1 | +0.47 | 1.18 | -1.45 | +3.25 | 4 | **+28.6** / 24 |
| 2021Q1-2021Q2 | +0.30 | 0.99 | -1.71 | +2.53 | 7 | **+30.9** / 61 |

Under truth-null the statistic behaves like a standard normal, as a
calibrated instrument should; the real values sit roughly 24 and 31
placebo standard deviations outside their placebo distributions. The
excursion is in the data, not the machinery. This answers, for this
specific regime, the densification concern that killed the companion
paper's author-space formation result: extreme document-size and
volume heterogeneity in the GME-era windows does not, by itself,
produce anything resembling the observed values.

In concrete terms: for two overlapping half-year evaluation windows,
the same authors co-mentioned, in thousands of documents, ticker pairs
at two to three times their expected rates. These were pairs the
preceding year of WSB discourse had kept fully apart: zero
co-mentions, despite ample independent popularity. The mixing deficit
inverted. Every other measurement in this program, including WSB itself
one quarter later, sits at or far below chance.

### Specificity: the control stays walled through the squeeze

The DD stratum, computed identically through the same calendar:

| eval start | 20Q1 | 20Q2 | 20Q3 | 20Q4 | 21Q1 | 21Q2 | 21Q3 | 21Q4 | 22Q1 | 22Q2 | 22Q3 | 22Q4 | 23Q1 | 23Q2 | 23Q3 | 23Q4 | 24Q1 | 24Q2 | 24Q3 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| z | -8.1 | -9.8 | -8.9 | -7.7 | -8.6 | -11.6 | -10.7 | -10.3 | -9.6 | -9.4 | -7.2 | -8.0 | -6.7 | -10.2 | -10.1 | -10.6 | -11.2 | -12.1 | -15.7 |
| eligible pairs | 63 | 104 | 151 | 145 | 211 | 345 | 272 | 281 | 290 | 250 | 179 | 158 | 150 | 139 | 128 | 143 | 120 | 127 | 161 |

- **P3 PASS.** Every DD window in the registered range (and in fact
  every DD window, period) sits between -6.7 and -15.7: no window pair
  anywhere shows the registered cliff pattern (chance-level then
  z ≤ -5), because no DD window is ever above -6.7 to begin with.

This contrast carries the paper's specificity claim. In the two
excursion windows, at the height of the squeeze, the analysis-oriented
communities' suppressed pairs stayed *below* chance (-7.7, -8.6). The
DD authors lived through the same news cycle and the same market, in
the same corpus, under the same statistic, and their idea-communities
did not fuse. The fusion and the subsequent wall-building are
properties of one community, not of the era. DD's own deepening over
the five years (from about -8 toward -15.7) is gradual, as predicted.

### Sensitivity, consistency, and power context

**Window length.** The registered sensitivity curves reproduce the
shape at both alternative window lengths. At B = 6 the excursion
windows read +32.2 and +46.0 and the flip to walls occurs at the same
eval window (2021Q2, z = -8.9, all subsequent windows ≤ -5). At B = 8
the single in-range excursion window reads +27.3 with the flip likewise
at 2021Q2 (-7.6). No bar attaches to these curves; they are reported
regardless of outcome so that the ladder's choice of B = 4 cannot be
what makes the transition appear. (Longer builds start later in the
calendar, so the B = 6 and B = 8 series begin at eval 2020Q3 and 2021Q1
respectively; full series with pair counts in the released window
table.)

**Lens.** The cashtag lens is registered sensitivity with an
informativeness floor: windows under 20 eligible pairs are reported
UNINFORMATIVE, which claims several early windows (and most DD cashtag
windows). Where informative, the cashtag series shows the same
signature: elevated in the excursion windows (+2.0, +2.5 at B = 4, with
formation 9/63 and 14/117, binomial p of about 1e-8 and 1e-11). From
2021Q2 onward every informative window is negative. The cashtag
excursion z is far smaller than the union value on a far smaller
eligible universe; it is reported as directional sensitivity, not as a
second measurement of the magnitude.

**Census consistency.** The corrected census's first B = 4 window
(build year 2019) counts 44,013 WSB/union build documents; the gate v2
census counts 44,012 fold-A MEME eval documents over the same year by
the same construction. Two corpora pulled independently, months apart,
agree to one document in 44 thousand. The agreement is near-exact, not
identical, and is reported as such (Amendment V4 addendum; the
superseded V3 anchor had matched two pre-exclusion values exactly).

**Power context.** Eligible-pair counts range 45-498 across the
primary series. The deep-wall z values of 2021-2022 sit on the largest
universes (373-498 pairs) and the pre-onset chance readings on the
smallest (45-77). The registered display rule (Methods) exists for
exactly this reason: threshold verdicts are per-window calibrated,
cross-window magnitude comparisons are not, and so we do not read -11.0
(2024Q1, 71 pairs) as deeper than -9.0 (2021Q3, 391 pairs).

## Discussion

With P1, P2, and P3 all passing, the registered claim stands as
designed: **a WSB-specific structural transition, onset 2021-04-01**.
The community moved from the only chance-level mixing state this
program has observed, through its only above-chance excursion, to
walls indistinguishable from every other measured community. The
control stratum moved gradually and monotonically the whole time.

What the timing does *not* do is pick a mechanism, and the registration
constrains what we may conclude here. The anchors amendment froze the
discrimination rule before any window existed. Onset in 2021Q1 would
have favored scale/fragmentation (the subscriber explosion, A2). Onset
in late 2021 would have favored governance (the mod-team regime change,
ticker-filter bot, megathread containment, and market-cap ban, A4-A8).
Onset in 2021Q2 was named, in advance, as the non-separable case: both
mechanism families active, and the design supporting neither over the
other. The measured onset is 2021Q2. The ordering evidence is still
worth recording: the onset follows the squeeze and the governance
regime change rather than preceding them, and its first evaluation
quarter contains the containment-by-megathread anchors (A6, A7,
mid-April 2021). But the scale shock is only one quarter older, and at
two-quarter evaluation resolution the design cannot cut between them.
Separating the mechanisms would need a different instrument, not a
sharper reading of this one. Engagement-stratified or
cohort-stratified readouts on the same corpus are the natural
candidates; the acquisition deliberately collected the `score` field
for exactly this follow-up, under a separate registration.

Likewise stated directly: the era confound is answered by design, not
eliminated. A continuous within-community series under uniform
provenance, with a control stratum that shows no discontinuity, rules
out the confound's most natural expressions: a fold-boundary artifact,
a source seam, or an era-wide narrative shift moving all finance
discourse at once. It cannot rule out an era interaction that touches
only WSB, because WSB's era exposure (being the epicenter of the
squeeze) is inseparable from WSB's identity in exactly the way the
anchors amendment describes.

Nothing in the next three paragraphs is a registered claim; these are
the readings the registered results invite, offered with their status
marked (recorded pre-publication in the results document's discussion
notes).

**The three-regime arc (descriptive, non-registered).** One community,
five years, all three states this program's statistic can express:
chance-level mixing (through 2020Q3), cascade fusion (2020Q4-2021Q2),
and walls (2021Q2 onward). No other measured community has occupied
more than one state. WSB traversed all three in eighteen months, and
the ordering is not arbitrary: the fusion sits exactly at the cascade,
and the walls begin exactly as it ends.

**Cascade susceptibility (interpretive, non-registered, speculative).**
The arc is consistent with a reading in which chance-level mixing is
the *substrate* of the cascade rather than its casualty. A community
whose idea-audiences freely overlap is one where a single story can
recruit everyone. That recruitment is what the excursion measures
directly: during the squeeze, previously never-connected tickers were
being discussed by the same people at multiples of chance. On this
reading the walls are the scar. The event triggered governance and
structural responses (megathread containment, ticker filtering,
spin-off fragmentation) that removed the conditions for its own
repetition. This is the connectivity condition of threshold-cascade
models (Watts 2002; Centola and Macy 2007), read empirically. The
registered results *describe* every step of that sentence (the
substrate state, the fusion, the walls, and their order), but the
causal links between the steps are not claimed, as stated above. We
note the reading because it inverts the usual valence of this program's
segregation statistic. Chance-level mixing looks "healthy" by the
lights of the discovery framing the companion paper tested; yet here,
the one mixing community was the one that produced the cascade.

**Pre-cascade generality (inferential, non-registered).** The companion
paper could not say whether WSB's fold-A chance reading was a property
of the community or of the single year 2019. The rolling series answers
this: chance-level mixing holds in the last two windows evaluated
wholly before the cascade (evals beginning 2020Q2 and 2020Q3, both
+1.5; the series' opening window reads -3.7 on its smallest universe,
45 pairs, its least-powered cell). The wall-free state was WSB's
standing condition through at least mid-2020, not a 2019 anomaly. The
companion paper cites this inference to the present study, and the
inference belongs here.

Five limitations bound these claims. First, quarterly resolution with
two-quarter evaluations: the onset time is the start of an evaluation
interval, so events inside a quarter (the squeeze itself spans weeks)
are unresolvable. The excursion's two windows overlap by one quarter,
so they are not independent measurements of the same phenomenon. They
were not treated as such; the placebo nulls each separately. Second,
different-powered windows: eligible-pair universes range 45-498 across
the primary series. Threshold verdicts are per-window calibrated;
cross-window magnitude comparisons are not (the display rule in Methods
and the power context in Results). Third, one community, one platform,
one transition: this is a case study of the only transition the program
has observed. Nothing here establishes how often discourse communities
transition, in either direction, or whether fusion-then-walls is the
generic cascade signature. That requires deliberately surveying for
transitions, which the mixing-deficit instrument makes possible.
Fourth, the excursion placebo is post-registration. It follows the
companion paper's registered placebo pattern and its per-replicate
seeds and code are committed, but it was designed after the excursion
was seen, as a robustness check on a result the registration did not
predict. The registered claims (P1-P3) do not depend on it. Fifth, the
V4 deviation: the first run omitted a registered exclusion filter, and
its outcomes were seen before correction (Methods). The correction was
rule-bound, both runs are released, and every verdict is identical
across them. Even so, the first run did not meet the strict
outcome-blind standard, and we say so rather than netting the two runs
into one clean story.

The companion paper established that in ordinary discourse,
expected-but-absent concept pairs are walls that persist. This paper
measured, at quarterly resolution and under a frozen design, how the
one known exception ended. r/wallstreetbets mixed at chance through
mid-2020. In the two windows around the GameStop squeeze its
suppressed pairs co-mentioned at 28 to 31 standard deviations above
chance. This is the only above-chance excursion in the program on any
platform at any granularity, and one the machinery cannot produce from
shuffled data. From April 2021 to the end of the data the community is
walled in every window, with no reversion, while the analysis-oriented
control stayed below chance for the entire five years, squeeze
included. The registered timing bet resolved inside 2021 as predicted,
and the onset falls where the pre-committed anchor list said the scale
and governance mechanisms cannot be told apart. The study can say when
the walls went up, but not the exact mechanism that built them. What
can be stated as measurement rather than story: the community that
cascaded was the one without walls, and after the cascade the walls
went up.

## Methods

### Corpus acquisition

The corpus is a fresh, single-source pull: the Arctic Shift API,
acquired 2026-08-31 in one fleet run (pull script and runbook in the
code release), landing 864 shard files. These cover 72 monthly shards
of WSB posts and comments spanning 2019-01 through 2024-12, plus the
same 72 months for each of the five DD subreddits, totaling 98,084,631
rows (about 5.6 GB compressed). The corpus is never mixed with the
companion paper's corpus: one source, one pull era, uniform fields for
treatment and control strata alike. This uniformity is the design
answer to the provenance confound. There is no archival/API seam
anywhere in the data, and in particular none co-located with the
phenomenon under study.

Hygiene follows the program's frozen rules: deleted/removed authors and
AutoModerator dropped; deduplication by item id; ticker extraction by
the gate's frozen extractor (union lens primary, cashtag lens
sensitivity, committed stoplist, SEC registrant-table resolution,
macro-hub tickers excluded, hub guard at 50 tickers per document).
Extraction yields 11,200,484 ticker mentions. The exclusion-filter
deviation and correction affecting the downstream loaders is disclosed
below. The 2020-2021 regime-break years are deliberately *included*:
prior studies in this program excluded them as a confound, but here the
transition is the object of study (registration, gate decision 2).

### Outcome-blind integrity checks

Before any census or statistic was computed, every shard passed a
full-parse integrity check (validation script in the code release): no
missing shard, no unparseable line, no month with more than 1%
out-of-span timestamps, no month at zero or below 5% of its neighbours.
The complete per-shard volume table was committed as a dated amendment
to the registration (Amendment V1; volume table in the provenance
appendix) before any window census existed. Spot-checks against the
prior acquisition era's runbook match exactly (for example, 2022-06 =
1.13M, 2023-09 = 510K, 2024-03 = 962K WSB comments).

Two observations were recorded in that amendment, before any outcome
existed, precisely because a result could later be blamed on them.
First, the WSB volume series itself shows the era plainly: monthly
comments run around 300 thousand through 2019, spike to 2.6 million in
March 2020 (COVID) and 8.0 million in January 2021 (GameStop), then
decay to under a million by 2023. Volume is not the studied statistic,
and the shuffle null conditions on the realized documents of each
window. Second, one control subreddit (r/SecurityAnalysis) decays to a
few thousand comments per year by 2023-24. The DD control is
registered as the union of five subreddits, so this changes nothing,
but the per-sub sparsity was noted before anyone saw a result it could
explain.

### Registration

The full registration (preregistration_paper2.md) was frozen and
committed, with the owner's explicit go recorded, before any outcome
statistic was computed; its amendments V1-V4 are dated appendices,
never rewordings. The study has two parts sharing one acquisition.

### Part B: rolling windows and the primary statistic

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
pairs, standardized against a label-shuffle null. The null permutes
concept labels over the (document, ticker) incidences of the frequent
set, with within-document duplicates collapsed, using R = 100
replicates and numpy default_rng seed 20260831. The evaluation script
imports the gate's machinery, so the statistic is identical by
construction. A registered determinism rule, carried over from the
gate's adversarial review, requires every incidence list to be sorted
before permutation, so no set or dict iteration order can feed the
seeded RNG. The script refuses to run unless the registration status
is REGISTERED. Formation counts per window (eligible pairs newly
co-mentioning beyond their per-pair permutation thresholds) are a
registered *secondary* readout with no bar attached: the gate's power
table shows them underpowered at these window sizes.

Both strata (WSB treatment, DD control) are computed identically and
independently, under both lenses (union primary, cashtag sensitivity;
a cashtag window with fewer than 20 eligible pairs is reported
UNINFORMATIVE, never as a negative).

### Outcome-blind census gate and the window-length ladder

Window length B was chosen from {4, 6, 8} quarters by a registered
ladder: the shortest B whose per-window census gives a median
eligible-pair count of at least 100 in the WSB/union cell. The ladder
makes the choice a census property rather than a researcher degree of
freedom. The census covers eligibility structure only; the census
script imports the document builder but structurally cannot compute
the statistic. It was computed, committed as a dated amendment, and
owner-reviewed before the first segregation z existed (Amendment V3;
corrected census under the disclosed deviation below). The ladder chose
**B = 4**: on the corrected census the B=4 WSB/union cell has a median
of 115 eligible pairs per window, with range 45-498 over 19 windows. No
window at any B, in either stratum under the union lens, falls below
the registered LOW-POWER floor of 30 eligible pairs, so every window
enters the onset rule. B = 6 and B = 8 become registered sensitivity
curves, computed and reported regardless of outcome, so that the
window-length choice cannot be what makes a transition appear.

One census property was recorded in the amendment before any z existed,
and it binds how results are displayed: eligible-pair counts co-move
with era volume, so between-window z magnitudes are different-powered
tests. Per-window z values are each internally calibrated, because the
null conditions on that window's realized documents, and the onset rule
uses only per-window threshold crossings. But a reader comparing raw z
magnitudes across windows is comparing tests whose eligible universes
differ by up to a factor of ten. For this reason every z series in this
paper, in every figure and every table, carries its eligible-pair
counts alongside, and the figures plot the pair-count series directly
beneath the z series.

### Registered predictions, onset rule, and primary cell

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
  anywhere in eval range 2020-01 through 2022-12; that is, no cliff.
  DD's deepening (fold A -10.1 to fold B -17.1) is predicted gradual.

P1 and P2 are scored on the WSB stratum, union lens, at the
ladder-chosen B = 4; P3 on the DD stratum, union lens, same B. No other
cell scores any bar (primary-cell clause, committed pre-outcome). A
secondary one-break step fit on the primary z series (least-squares,
all interior candidate breaks, near-tie set within 10% of minimum SSE)
was registered pre-census as an uncertainty band on the onset date. No
bar attaches to it.

The registration also states its own epistemic position: the two
fold-level endpoints were known and could not be un-seen, so what is
registered as pre-outcome is everything between and around them. No
rolling-window statistic, no rebuilt-fold cell, and no per-window
census existed at registration time. The predictions bet on the shape
and timing of the transition, not on its existence at the endpoints.

### Part A: provenance-hardening of the endpoint

Part A rebuilds the companion paper's fold B with the archival-dump
months replaced by API months from this pull, giving uniform API
provenance in both folds. It then recomputes the WSB-dependent gate
cells under the frozen gate criterion, reusing the gate evaluation
code verbatim: same per-pair label-shuffle p99, R = 100, seed
20260831, formation floor, and segregation z. The registered
expectation is that fold-B MEME segregation z stays ≤ -3, i.e., that
the walled endpoint is real and not a provenance artifact. Part A
removes the provenance confound only; it says nothing about timing.

### Causal anchors, committed before any window

Because "the onset matches event X" is cheap after the fact, a list of
dated WSB governance events was collected and committed before any
rolling-window statistic existed (Amendment V2; anchors file in the
provenance appendix). Eight anchors A1-A8 span April 2020 through
August 2021: the pre-event removal of the subreddit's founder (A1,
2020-04; Reimann 2023); the GameStop squeeze and roughly 30x
subscriber explosion (A2, 2021-01; Bloomberg News 2021; Newsweek
2021); the Discord ban and brief private-mode flip as moderation was
overwhelmed (A3, 2021-01-27; Sandler 2021; Kotaku 2021); the mod-team
regime change (A4, 2021-02-04/05; Business Insider 2021; HotHardware
2021); the automod ticker-filter bot, publicized by a WSB moderator
(A5, 2021-02, posted 2021-02-27; Hacker News item 26281147);
containment-by-daily-thread demonstrated on crypto and reversed within
a day (A6, 2021-04-14/15; Decrypt 2021; Bitcoin.com News 2021); the
final GME megathread, pushing single-ticker attention out to spin-off
subreddits (A7, 2021-04-16; Shacknews 2021); and the sub-$1B
market-cap discussion ban (A8, in force by 2021-08; wallstbets101.com
mirror; its introduction date is flagged in the amendment as unpinned
and unusable for timing claims). The committed anchors file remains
the pre-commitment record; its sources are itemized in the reference
list.

The amendment freezes the discrimination reading in advance: onset in
2021Q1 favors scale/fragmentation (A2); onset in late 2021 favors
governance (A4-A8); **onset in 2021Q2 is the non-separable case, with
both mechanism families active, and supports neither over the other**.
Any timing comparison against an event not on this list is labelled
exploratory. The DD subreddits share none of A3-A8, which is what gives
P3 its power against era-wide narratives.

### Disclosed deviation and rule-bound correction (Amendment V4)

The first full run of the three paper-2 scripts (census, rolling
windows, Part A) deviated from the registered spec. The scripts loaded
mention rows directly from the extraction parquet and omitted the
load-time excluded-tickers filter (SPY, QQQ, VIX, BTC, ETH). The gate
applies that filter as its frozen macro-hub exclusion, and this
registration incorporates it by reference ("identical to the gate").
The omission was found by a code diff during cross-checking against
the gate's tables, *after* first-run outcomes had been seen, and is
disclosed as Amendment V4.

The correction path is rule-bound. The filter was added to the three
loaders. The census was re-derived and the window-length ladder
re-decided by the unchanged registered rule; B = 4 stands, and the
re-decision was committed before any corrected z existed. Parts A and
B were then re-run under the unchanged bars, seeds, and window
definitions. No bar, threshold, seed, window definition, or onset rule
changed at any point.

Because first-run outcomes were seen before the correction, the
protection is exactly that every re-derivation step is a frozen rule
with no free parameter. Both runs are released: the first-run outputs
are retained as superseded artifacts, and the conforming run's outputs
are the operative tables (file names in the provenance appendix). **The
two runs agree on every verdict**: same onset window, same P1/P2/P3
outcomes, same excursion and control readings. Every number in Results
is from the conforming run. A related target correction is disclosed
in the same amendment: the census consistency anchor recorded in
Amendment V3 compared two pre-exclusion quantities; the agreement was
real but old-vs-old. The operative target is the gate v2 census value,
and the corrected comparison is reported in Results under census
consistency.

### AI assistance

Analysis code, evaluations, and manuscript drafting were performed with
a large-language-model assistant operating under the author's
direction. All designs, thresholds, and interpretation rules were
registered and committed before evaluation; the version-control
history documents the full sequence, including the implementation
deviation and its correction (Amendment V4).

## Data availability

Raw Reddit content is public and retrievable via the Arctic Shift API;
the release includes exact pull specifications. Raw data files stay out
of the repository. The released derivations (per-shard volume table,
window census, window z series for all 204 cells, Part A cells,
excursion placebo replicates, and the superseded first-run outputs) are
committed at https://github.com/talecK/antikythera (private during
review; public at publication), with the commit references listed in
the provenance appendix.

## Code availability

All pipeline code (pull, validation, ticker extraction), the evaluation
script, the census and placebo scripts, the figure generator, and the
registration with its amendments V1-V4 are released in the same
repository, whose version-control history timestamps every
registration ahead of its result.

## Competing interests

This research program originated in a commercial signal-research effort
by the author; the studied hypothesis failed its registered tests in
the companion paper, and no product, trading activity, or financial
position resulted or exists. The author declares no other competing
interests.

## Author contributions

K.Q. conceived the study, wrote and registered the design, acquired
the corpus, ran the analyses, and wrote the manuscript.

## Figure legends

Figures are generated from the committed window and placebo tables
only (figure generator in the code release). Per the registered display
rule, **every z-series panel carries an eligible-pair-count panel
directly beneath it, sharing its x-axis.**

**Figure 1** (p2_fig1.png/.pdf). The transition and the excursion. Top:
the primary segregation z for r/wallstreetbets (union lens, four-quarter
build) over the nineteen rolling evaluation windows, labelled by
starting quarter. z is the count of evaluation-window documents
co-mentioning any suppressed ticker pair, standardized against a
label-shuffle null; values near zero mean suppressed pairs co-mention
about as often as chance predicts, strongly negative values mean they
are kept apart, and positive values mean they are brought together
beyond chance. The shaded band marks |z| < 3, the chance region; the
dashed line marks the registered wall threshold z = -5; the vertical
marker is the onset, 2021-04-01; the two labelled points are the
excursion windows straddling the GameStop squeeze. Bottom: the DD
control stratum over the same calendar. Beneath each z panel, the
number of eligible pairs in that window, which sets the power of that
window's test.

**Figure 2** (p2_fig2.png/.pdf). The excursion placebo. For each
excursion window, the 20 truth-null placebo z values as a histogram,
each obtained by shuffling ticker labels across authors and recomputing
the full registered statistic from scratch, with the real value marked.
Annotations carry the secondary formation counts (real 24 and 61
versus placebo maxima 4 and 7).

**Figure 3** (p2_fig3.png/.pdf). Sensitivity. Top: r/wallstreetbets
union-lens z at build lengths of four, six, and eight quarters on a
common calendar, with grouped pair counts beneath. Bottom: the cashtag
sensitivity lens at a four-quarter build, with windows under 20
eligible pairs shown as open markers (reported UNINFORMATIVE, never as
negative), pair counts beneath.

## Appendix: provenance of every number

All artifacts live in the same repository as the companion paper's
(https://github.com/talecK/antikythera; private during review, public
at publication), whose commit history timestamps every registration
ahead of its result. The numbers in this paper trace as follows:

| quantity | artifact | commit |
|---|---|---|
| Registration + amendments V1-V4 | preregistration_paper2.md | 99ffd9e (registered); f004bfc (primary-cell + determinism clauses); 63b7f6e (V1), 3fa0d73 (V2), b86c378 (V3), fbf3ace + 7cb1109 (V4) |
| Candidate mechanisms, stated pre-window | reports/paper2_seed.md | 516a158 (first); 231573b (last edit) |
| Ticker extraction (frozen unit rules) | pipeline extractor | 8db5012 |
| Corpus pull and validation | pipeline/pull_reddit_paper2.py, pipeline/validate_paper2.py | e4b61ef; f367637 |
| Evaluation code (registration-checked, gate machinery) | eval/run_paper2.py | 35914d2 |
| Corrected census + B-ladder re-decision (pre-outcome) | reports/paper2_window_census.tsv | 80b3b37 |
| Conforming-run z series, all 204 cells | reports/paper2_windows_z.tsv | 21a9dc7 |
| Verdicts, Part A, excursion, census cell | reports/paper2_results.md | 21a9dc7 |
| Excursion placebo (40 reps, per-rep seeds) | eval/placebo output, commit log; reports/paper2_placebo_reps.tsv | 7bef4a2; 2c41bbf (per-replicate table) |
| First run (superseded, disclosed) | reports/paper2_windows_z_v1_superseded.tsv, paper2_window_census_v1_superseded.tsv | fbf3ace; first-run verdicts 9487884 |
| Anchors A1-A8 + frozen discrimination reading | reports/paper2_anchors.md | 3fa0d73 |
| Volume table + integrity pass | reports/paper2_volume_table.tsv | 63b7f6e |
| Discussion notes (non-registered readings) | reports/paper2_results.md | d184472 |
| Figures 1-3 | eval/make_paper2_figs.py, reports/figures/p2_fig1-3 | 4360746 |
| Gate v2 comparison values (companion paper) | gate table / gate_rerun_v2.log | f89cb2b, 1386fc0 |

## References (DOIs marked [verify] to be confirmed at submission)

- Quiring, K. (2026). The gaps that don't close: idea segregation
  persists in twenty years of online discourse. Draft in the same
  repository (reports/paper1_draft.md); the source observation is its
  section "A second platform".
- McPherson, M., Smith-Lovin, L., Cook, J.M. (2001). Birds of a
  feather: Homophily in social networks. *Annual Review of Sociology*
  27, 415-444. doi:10.1146/annurev.soc.27.1.415 [verify]
- Cinelli, M., De Francisci Morales, G., Galeazzi, A., Quattrociocchi,
  W., Starnini, M. (2021). The echo chamber effect on social media.
  *PNAS* 118(9), e2023301118. doi:10.1073/pnas.2023301118 [verify]
- Waller, I., Anderson, A. (2021). Quantifying social organization and
  political polarization in online platforms. *Nature* 600, 264-268.
  doi:10.1038/s41586-021-04167-x
- Swanson, D.R. (1986). Fish oil, Raynaud's syndrome, and undiscovered
  public knowledge. *Perspectives in Biology and Medicine* 30(1), 7-18.
  doi:10.1353/pbm.1986.0087 [verify]
- Lucchini, L., Aiello, L.M., Alessandretti, L., De Francisci Morales,
  G., Starnini, M., Baronchelli, A. (2022). From Reddit to Wall Street:
  the role of committed minorities in financial collective action.
  *Royal Society Open Science* 9(4), 211488. doi:10.1098/rsos.211488
- Mancini, A., Desiderio, A., Di Clemente, R., Cimini, G. (2022).
  Self-induced consensus of Reddit users to characterise the GameStop
  short squeeze. *Scientific Reports* 12, 13866.
  doi:10.1038/s41598-022-17925-2
- Semenova, V., Winkler, J. (2021). Social contagion and asset prices:
  Reddit's self-organised bull runs. INET Oxford Working Paper
  No. 2021-04; arXiv:2104.01847.
- Pedersen, L.H. (2022). Game on: Social networks and markets.
  *Journal of Financial Economics* 146(3), 1097-1119. doi [verify]
- Chandrasekharan, E., Pavalanathan, U., Srinivasan, A., Glynn, A.,
  Eisenstein, J., Gilbert, E. (2017). You can't stay here: The efficacy
  of Reddit's 2015 ban examined through hate speech. *Proceedings of
  the ACM on Human-Computer Interaction* 1(CSCW), 31.
  doi:10.1145/3134666
- Trujillo, A., Cresci, S. (2022). Make Reddit great again: Assessing
  community effects of moderation interventions on r/The_Donald.
  *Proceedings of the ACM on Human-Computer Interaction* 6(CSCW2), 526.
  doi:10.1145/3555639
- Kiene, C., Monroy-Hernandez, A., Hill, B.M. (2016). Surviving an
  "Eternal September": How an online community managed a surge of
  newcomers. *Proceedings of CHI 2016*, 1152-1156.
  doi:10.1145/2858036.2858356
- Lin, Z., Salehi, N., Yao, B., Chen, Y., Bernstein, M. (2017). Better
  when it was smaller? Community content and behavior after massive
  growth. *Proceedings of ICWSM 2017* 11(1), 132-141.
  doi:10.1609/icwsm.v11i1.14884
- Watts, D.J. (2002). A simple model of global cascades on random
  networks. *PNAS* 99(9), 5766-5771. doi [verify]
- Centola, D., Macy, M. (2007). Complex contagions and the weakness of
  long ties. *American Journal of Sociology* 113(3), 702-734.
  doi [verify]
- Bikhchandani, S., Hirshleifer, D., Welch, I. (1992). A theory of
  fads, fashion, custom, and cultural change as informational cascades.
  *Journal of Political Economy* 100(5), 992-1026. doi [verify]
- Anchor sources (the anchors file, reports/paper2_anchors.md,
  committed before any window statistic existed, remains the
  pre-commitment record; all URLs accessed 2026-08-31):
  - Reimann, N. (2023). Founder of WallStreetBets, which sparked meme
    stock craze, sues Reddit for ousting him. *Forbes*, February 15,
    2023. (Documents the April 2020 removal.) [A1]
  - Bloomberg News (2021). WallStreetBets gains more than a million new
    members overnight. *Bloomberg*, January 28, 2021. [A2]
  - Newsweek (2021). WallStreetBets subreddit gains 2 million members
    in a day. *Newsweek*, January 2021. [A2]
  - Sandler, R. (2021). Discord bans r/WallStreetBets over "hate
    speech," Reddit forum goes private. *Forbes*, January 27, 2021. [A3]
  - Kotaku (2021). Discord bans r/WallStreetBets server for "hateful"
    content (update: subreddit briefly taken offline). *Kotaku*,
    January 27, 2021. [A3]
  - Business Insider (2021). Reddit banned a group of WallStreetBets
    moderators after they staged an attempted coup. *Business Insider*,
    February 5, 2021. [A4]
  - HotHardware (2021). Reddit stops attempted moderator movie deal
    coup in r/WallStreetBets drama. *HotHardware*, February 2021. [A4]
  - WSB moderator (2021). "Hi all, I am a mod on r/WallStreetBets..."
    *Hacker News*, item 26281147, February 27, 2021.
    https://news.ycombinator.com/item?id=26281147 [A5]
  - Decrypt, via Yahoo Finance (2021). Reddit forum WallStreetBets
    allows crypto conversation, immediately re-bans it. April 2021. [A6]
  - Bitcoin.com News (2021). Wallstreetbets reinstates ban on
    cryptocurrency discussions, citing Bloomberg coverage. April
    2021. [A6]
  - Shacknews (2021). r/wallstreetbets mods announce that today will be
    the final GME megathread. *Shacknews*, April 16, 2021. [A7]
  - wallstbets101.com (2021). Mirror of an August 2021 r/wallstreetbets
    post debating the sub-$1B market-cap rule. [A8; rule introduction
    date unpinned, Wayback pass pending; verify]
- Null-model lineage for the label-shuffle machinery (Connor &
  Simberloff 1979; Gotelli 2000; Gotelli & Ulrich 2012) as discussed in
  the companion paper's Related work and Discussion.
