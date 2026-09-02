# Ideas that never meet online mark divided communities, not future discoveries

**Author:** Kevin Quiring (independent researcher; ORCID 0009-0001-9034-5533)

**Draft v0.3, 2026-09-01. All results final (post-review regeneration on
deterministic artifacts, commit a67d556). Structured as Introduction,
Results, Discussion, Methods; commit references for every quantity are
collected in the commit appendix. Prose, jargon, and figure passes in
progress.**

---

## Abstract

In science, two well-studied ideas never discussed together
make a likely candidate for a future discovery. Predicting which pair
connects next is the aim of literature-based discovery. Whether this
holds in online discussion is untested. Here we test it on 200 thousand
Hacker News discussions from 2015 to 2017, with a pre-registered
replication on 41.5 million Reddit finance posts, 2017 to 2024, using
stock tickers.
Four pre-registered evaluations use threads, then authors, as documents.
Pairs never discussed together, called suppressed pairs, connect no more
than popularity and overlapping topics predict. On the Science4Cast
benchmark of AI papers, where the effect is known, the same method finds
it. The standard test against chance flags connections too easily when
document sizes vary. It reported 19 to 24 percent of pairs connecting
within authors' quarterly output, yet shuffled data connected
more pairs than real data. A per-pair permutation test leaves new
connections no higher than false positives produce.
Suppressed pairs appear together far below chance: nearly 9 standard
deviations at author level, over 100 at thread level. Both results
replicate across the 2020-2021 market regime change. Ideas that never
meet online mark communities that stay apart, not future discoveries
waiting to happen.

---

## Introduction

Some discoveries are visible before they are made. Swanson (1986a) noticed
that the medical literature on dietary fish oil and the literature on
Raynaud's syndrome shared intermediate findings yet never cited one
another. He inferred a connection and was later proven right. The insight
became literature-based discovery (LBD; Swanson 1986b): map which concepts co-occur in a
corpus, find pairs of concepts that are linked through shared
intermediates but never directly, and treat those pairs as candidate
discoveries. Later work recast the search as link prediction on the
co-occurrence graph itself. The eligibility rule used in this paper,
a pair whose expected co-occurrence under independence is high and
whose observed co-occurrence is zero, is our own operationalization of
that tradition, not a criterion any of these authors proposed. On scientific corpora the
approach appears effective. In the Science4Cast benchmark,
built from 143,000 artificial-intelligence papers, concept pairs can be
ranked by their probability of future connection well above chance (Krenn
et al. 2023). Word embeddings trained on materials-science abstracts
flagged thermoelectric compounds years before their discovery papers
(Tshitoyan et al. 2019).

The method has a lineage, reviewed by Henry and McInnes (2017),
Sebastian, Siew and Orimaye (2017) and Thilakaratne, Falkner and
Atapattu (2019), and a scientometric cousin in co-word analysis
(Callon, Courtial and Laville 1991). Swanson and Smalheiser (1998) turned gap-finding into a working
tool on scientific text; Rzhetsky, Foster, Foster and Evans (2015)
built co-occurrence discovery networks on the biomedical literature;
and Krenn and Zeilinger (2020) built the same kind of graph on
quantum-physics abstracts and predicted its growth. The Science4Cast benchmark turned it into a
machine-learning competition on a 64,000-node concept graph, with
link-prediction scores (area under the receiver operating characteristic curve, AUC) above 0.9 for
the best methods on the main task.
Our study is, to our knowledge, the first application of the
literature-based discovery gap criterion to non-scientific discourse. Our positive control reuses Science4Cast
directly.

Scientific literature is a small and unusual corner of written thought.
The bulk of recorded reasoning happens in ordinary discourse: forums,
comment threads, industry discussion. That discourse is known to sort
itself: people who discuss one thing tend not to discuss another, from
homophily in offline networks (McPherson, Smith-Lovin and Cook 2001)
to the segregated link structure of political blogs and Twitter
(Adamic and Glance 2005; Conover et al. 2011), the echo chambers
measured on Facebook and Twitter (Cinelli et al. 2021), and the
community-level polarization measured on Reddit (Waller and Anderson
2021). If expected-but-absent concept
pairs predict future connections there, the applications are broad, from
research recommendation to trend analysis. To our knowledge the transfer
has not been tested, chiefly because discourse lacks the self-indexing
that makes science tractable: no citations, no keywords, no discrete
units. This paper builds that index for one large corpus, runs the test, and
replicates it on a second platform.

Two adjacent literatures frame what a positive result would and would
not mean. Uzzi, Mukherjee, Stringer and Jones
(2013) showed that high-impact papers combine a conventional core with a
small number of atypical journal pairings. Foster, Rzhetsky and
Evans (2015) documented the risk-reward tradeoff of unconventional
combinations. This literature measures the value of rare combinations;
ours measures whether expected combinations happen at all.

Co-occurrence gap prediction is a case of
link prediction on a growing graph (Liben-Nowell and Kleinberg 2007).
Aiyappa et al. (2025) showed that standard link-prediction evaluation
carries an implicit degree bias: a degree-only ranker is near optimal on
many benchmarks. A Science4Cast competition entry demonstrated the same
point in practice, placing third with degree-based features alone
(Aghajohari et al. 2021).
Our thread-level findings echo this: the only surviving predictor
families are node popularity and triadic closure, the two best-established
generic regularities of growing networks (Newman 2001; Kossinets and
Watts 2006). A separate study
(in preparation) examines the Science4Cast benchmark itself in this
light.

How to calibrate "beyond chance" was worked out in ecology decades
ago, and text-corpus work has not adopted the answer. Ecologists faced
the same question, whether species co-occur more or less than chance,
and tested it against null models that hold row and column totals of a
site-by-species matrix to varying degrees. Those studies measured the
false-positive (Type I) inflation of partially constrained null models
and converged on fully constrained ("fixed-fixed") randomizations as
the safer default (Connor and Simberloff 1979; Gotelli 2000; Gotelli
and Ulrich 2012; Gotelli and Graves 1996; see also Maslov and Sneppen
2002 for the network analog). Our corrected criterion belongs to that
family: a label permutation over the document-concept matrix that
holds every document's size and every concept's frequency fixed. The
standard text-corpus criterion, the z-score against a Poisson
expectation, constrains less. It holds each concept's frequency fixed
but lets document sizes float, which makes it the kind of partially
constrained null that ecology showed to inflate false positives, and
it fails here for the same reason: large documents produce
co-occurrences that the expectation does not anticipate. We claim no
novelty for the fix. Our contribution is to carry it into text corpora
and to measure what leaving it out has cost.

Our answer is negative. Three headline results follow.

First, a null result backed by a positive control. In three years of Hacker News data, 2015 to 2017, suppressed
concept pairs do not connect above chance at any document granularity we
tested, under evaluations whose designs were fixed and committed before
any outcome was computed. The instrument is not at fault: the identical
pipeline, pointed at Science4Cast, recovers the known signal at roughly
105 times random precision.

Second, a measurement trap likely to extend beyond this study. The
standard way to score a new co-occurrence as "real" is a
chance-calibrated test: observed joint document count against an
expected count derived from the two concepts' marginal frequencies,
that is, from how often each appears on its own. We
show this criterion is badly anti-conservative, flagging formation far
too easily, when documents vary in
size, as they do in virtually every real corpus. In our author-level
analysis it produced formation rates of 19 to 24 percent that
survived two further pre-registered evaluations. A placebo test,
registered with its failure condition stated in advance, then revealed
that randomly shuffled data "forms" nearly twice as many pairs as the
real data. We describe the corrected criterion (a per-pair permutation
test) and suggest the shuffle as a mandatory control for co-occurrence
formation claims generally.

Third, a positive finding we did not seek. Under the corrected
criterion, suppressed pairs do not only fail to connect. They
co-occur below chance, by nearly 9 standard deviations at the author
level and by more than 100 at the thread level. Two ideas that have never met
attract separate communities of attention. Those communities stay
apart, at rates their sizes cannot explain. In discourse, the gaps that
literature-based discovery hunts for do not close. They persist,
far below chance, everywhere we measured.

Hacker News is the test case; Reddit financial discussion is the
replication. The general object is the mixing of idea communities in
discourse, which literature-based discovery assumes and this paper
measures. A companion paper (Quiring 2026) follows the one community
in this program that ever changed state.

## Results

All numbers in this section are from the post-review regeneration on
deterministic artifacts; the commit references for every quantity are
collected in the commit appendix.

### Measurement summary

The unit of observation is a document, defined two ways. In thread
space, a document is one Hacker News discussion: a story title plus its
top twenty comments. In author space, a document is the set of concepts
one author used within one calendar quarter. Concepts are short
lowercase strings extracted from each discussion by a language model
(Methods). Within a build window, a concept is frequent if it appears
in at least 20 distinct documents. Among frequent concepts, a pair is
eligible (we also call it suppressed) if two conditions hold: its expected joint
document count under independence is at least 2, and its observed
co-occurrence in the build window is zero. In plain terms, each concept
is discussed often enough that chance alone should have put the two in
the same document at least twice, yet it never happened. Two outcomes
are measured in the following evaluation year. Formation asks, pair by
pair, whether the two concepts now co-occur beyond chance. The paper
uses two definitions of beyond chance, the standard z-criterion and a
per-pair permutation criterion. The difference between them is itself
one of this paper's findings. The segregation statistic z pools all eligible
pairs: it counts the evaluation documents in which any eligible pair
co-occurs and standardizes that total against a permutation null
distribution. The shuffle moves concept labels across document slots,
preserving every document's size and every concept's total frequency,
with 100 replicates and a fixed seed. A z near zero means suppressed
pairs co-occur about as often as chance predicts; a strongly negative z
means they are kept apart. Two temporal folds are used: build 2015 to
2016 with evaluation 2017 (fold 1), and build 2015 with evaluation 2016
(fold 2). Every unit definition, threshold, fold boundary, and
interpretation rule was registered and committed before the
corresponding evaluation ran; full specifications are in Methods.
Figure 1 sketches the construction.

### Registered predictions and pre-committed readings

Each evaluation in this paper was registered with its pass threshold
and with the reading each outcome would receive, before the evaluation
ran. Table 1 lists them in the order they were run, with the observed
result; the verbatim rules are in the registration files listed in the
commit appendix.

**Table 1.** Registered items, the pre-committed reading of each outcome, and the observed result.

| Registered item | Pre-committed reading | Observed |
|---|---|---|
| Thread space, ranking: the suppression-by-affinity or the common-neighbors ranker beats both the frequency-product control and random at k = 200 | The discovery machinery adds predictive signal beyond popularity | Primary ranker at zero; common neighbors cleared the threshold only because the frequency-product control scored zero by construction, which the run log records as a drafting error in the rule and does not claim (thread-level results) |
| Thread space, economically relevant vocabulary (terminal): any ranker beats random and the frequency-product control at k = 200 on exposed pairs in both folds | The machinery works where it would matter; otherwise the thesis closes | Not met in either fold; 8 and 1 formations per year, all rankers at random |
| Positive control: common-neighbors precision at 200 at least 10 times random on the Science4Cast benchmark, and rank-AUC within 0.05 of the benchmark baseline | The pipeline detects known signal, so a Hacker News null result is about the corpus, not the instrument | Met: roughly 105 times random; AUC 0.899 against 0.851 |
| Author space: formation at least 5 percent in both folds under the z-criterion | Threads buried the signal; the author-level document becomes the default | Met at the time: 19.2 and 23.6 percent; revised by the placebo below |
| Author space, exposed pairs: at least 3 of 26 pooled exposed pairs form | The author-space effect survives economically relevant vocabulary | Met at the time: 6 of 26; inherits the revision below |
| Placebo: a shuffled-null mean at or above half the observed formation count in either fold is reported as a revision of the author-space result, not a nuance | The author-space rate is substantially mechanical | Revision fired: shuffled data formed more pairs than the real data, 125.1 against 70 and 53.0 against 26 |
| Window and attribution sensitivity: formation at least 5 percent in both folds under monthly and half-yearly documents and under the conservative attribution rule | The artifact, if any, does not live in the window or the attribution path | Met everywhere (9.7 to 27.8 percent; 24.9 and 27.5 percent), every cell below its own shuffled expectation |
| Calibrated formation: formed count above the 1 percent floor at one-sided binomial p < 0.01 in both author folds | Above-chance formation is real and the author-space result stands | Not met in either fold (p = 0.88 and 1); thread space at the floor likewise |
| Segregation: z at most -3 in both author folds | Suppressed pairs co-occur below chance; segregation persists | Met: -8.9 and -8.6, with thread space at -152 and -123 |
| Replication, formation: calibrated formed count above the floor at p < 0.01 in both folds | Financial discourse shows formation where Hacker News shows none | Not met: 0 of 166 and 1 of 478 |
| Replication, segregation: z at most -3 in both folds | Segregation generalizes beyond one platform and unit type | Met: -8.8 and -17.7 |

### No formation signal at any granularity in thread space

Four registered evaluations tested the discovery thesis in thread space.
At claim-level granularity nothing repeats: the co-occurrence graph over
paraphrased claims is empty and the analysis is degenerate. At
concept-level granularity the graph is dense and eligible suppressed
pairs are plentiful (25,161 in fold 1; 7,505 in fold 2), but under the
z-criterion only 0.60 and 0.68 percent of them form. Ranking within
the eligible set adds nothing. The only feature family that beats random
ordering is triadic closure (common neighbors, meaning the number of
frequent concepts that co-occur with both members of a pair). Its
precision-at-200, the share of the top 200 ranked pairs that formed, is
around 2.5 percent, roughly 4 times random: the generic
network-science baseline, which requires none of the discovery
apparatus.
Semantic features (embedding affinity between concept labels) are
indistinguishable from random. Restricting to economically relevant
vocabulary (a registered classification of concepts into exposed versus
generic) leaves 8 formations per year in fold 1 and 1 in fold 2 across
the entire site.

### The instrument finds the signal where it exists

A null result of this kind is only as credible as its instrument, so we ran
the identical eligibility and ranking pipeline, unchanged, on the
Science4Cast benchmark where the signal is known to exist. The signal
is there: ranked precision reaches roughly 105 times random, and our feature set
reaches an AUC (area under the curve) of 0.899 against the benchmark's published 15-feature baseline
of 0.851. Within the benchmark's suppressed subset (expected joint
count at least 2, no prior co-occurrence), 67 percent of pairs connect
(188 of 281 in a 10-million-pair sample).

One definitional difference matters and is easy to miss. Formation on the benchmark is the benchmark's own ground
truth: the appearance of any edge in the target-year graph. Our
discourse analyses use the chance-calibrated criterion (Methods).
The control therefore certifies the pipeline (eligibility construction,
ranking, precision measurement) and not the formation criterion, which
the benchmark never exercises. It also means the 67 percent is not
comparable with any discourse rate in this paper: "any edge appears"
and "co-occurrence exceeds a calibrated threshold across two independent
authors" are different events. Early in this project we treated the two
as rungs of one calibration ladder; that comparison was ill-posed and
we withdraw it here. Whether the benchmark's 67 percent is itself
substantially mechanical (the AI concept graph grows denser rapidly over
the target years) is a further open question, outside this paper's
scope.

One observation from this control does carry forward: in science as on
Hacker News, popularity features match or exceed closure and semantic
features add nothing, consistent with the degree-bias literature
(Aiyappa et al. 2025).

### An apparent thirty-fold effect in author space

A thread is a room where a story is discussed; a person carries ideas
from room to room. A person can connect two ideas that no single
conversation ever did. On this reasoning we re-defined the document as
one author's concepts within a calendar quarter and re-ran the
identical formulation, registered before evaluation as always. The structure of
the problem changed: eligible suppressed pairs became rare (364
in fold 1, 110 in fold 2, versus tens of thousands in thread space),
resembling the science benchmark. Under the z-criterion they formed
at 19.2 and 23.6 percent, thirty times the thread-space rate. The effect
survived two further registered evaluations: it held at 23.1 percent on
economically relevant vocabulary (6 of 26 exposed pairs, against a
registered pass threshold of 3). A registered follow-up showed the formations
were almost never accompanied by any written claim connecting the two
concepts, suggesting the two audiences were converging before anyone
articulated the link. For roughly one day, the working conclusion of
this project was that thread-level co-occurrence had simply been the
wrong measurement, and that individuals do bridge expected-but-absent
pairs at high rates.

### The placebo

Author-quarter documents vary widely in size (median 5 concepts, 90th
percentile 21, maximum 100 under the hub exclusion described in
Methods). Before drafting any
claims we registered a placebo: shuffle the concept labels across the
evaluation window's document slots, and count how many eligible pairs
"form" under the z-criterion in 100 such replicates. The shuffle
preserves every document's size and every concept's total frequency
while destroying any real association between concepts and people. The
registration specified the failure condition in advance: a shuffled mean
at or above half the observed count would be reported as a revision of the
result, not a nuance.

The placebo did more than halve the result. Shuffled data forms more
pairs than the real data (Figure 2a, b): 125.1 on average versus 70
observed in fold 1,
and 53.0 versus 26 in fold 2. The observed counts sit 5.8 and 5.0
standard deviations below their own shuffled expectations. The z-criterion's
internal expectation, built from marginal frequencies, does not account
for large documents, whose joint occurrences grow with the square of
their size. When document sizes vary widely, random assignment clears
z ≥ 2 constantly. The 19-to-24-percent rate was an artifact of
the measuring stick. Registered sensitivity analyses confirmed the
artifact lives in the criterion and nowhere else. The rate is stable
under monthly and half-yearly document windows (9.7 to 27.8 percent)
and under a conservative attribution rule that discards all
story-author credits (24.9 and 27.5 percent). Yet all of these numbers
sit below their own shuffled expectations: in every window and under both attribution rules the
observed formation count falls below the minimum of its 100 shuffle
replicates (commit appendix).

### Calibrated formation: nothing, anywhere

We then registered and ran the corrected criterion (per-pair permutation
test, Methods) in both document spaces and both folds, with the
interpretation thresholds again fixed in advance. Formation collapses to the
false-positive floor everywhere (Figure 3, Table 2).

**Table 2.** Calibrated formation against the false-positive floor, by space and fold.

| space | fold | eligible | formed | 1% floor | binomial p |
|-------|------|---------:|-------:|---------:|-----------:|
| author | 1 | 364 | 2 | 3.6 | 0.88 |
| author | 2 | 110 | 0 | 1.1 | 1 |
| thread | 1 | 25,161 | 22 | 251.6 | ~1 |
| thread | 2 | 7,505 | 12 | 75.0 | ~1 |

No cell shows formation above what a 1-percent-per-pair error rate
produces on its own. The handful of "formed" pairs are consistent with
noise, and we make no claims about them individually. At corpus scale,
on this platform, suppressed concept pairs do not connect above chance
at either granularity.

### The gaps are held open

The same permutation machinery yields a second, better-powered
statistic: the total number of joint occurrences across all eligible
pairs, observed versus shuffled (Figure 2c). Here the data speak
loudly, in the
direction opposite to the discovery thesis (Table 3).

**Table 3.** Total co-occurrence over eligible pairs, observed against the shuffled expectation.

| space | fold | observed total | null mean (sd) | z |
|-------|------|---------------:|---------------:|----:|
| author | 1 | 746 | 1,057 (35) | −8.9 |
| author | 2 | 454 | 647 (23) | −8.6 |
| thread | 1 | 12,098 | 48,378 (238) | −152 |
| thread | 2 | 7,866 | 28,274 (166) | −123 |

Suppressed pairs co-occur at roughly 70 percent of chance in author
space and roughly a quarter of chance in thread space. The registered
pass threshold for this statistic (z ≤ −3 in both author folds) is met
by a wide margin, in both spaces. The interpretation is simple and, we
believe, the paper's most durable finding: two concepts that have never
co-occurred, despite ample independent popularity, are not on their way
to meeting. Their audiences are substantially disjoint and remain so.
Discourse does not slowly mix; its communities of attention
persistently fail to overlap, at magnitudes far beyond what topic sizes explain. The
suppressed pairs of literature-based discovery are, in discourse,
markers of persistent segregation rather than latent connection.

Descriptively, the segregation is strongest where the discovery
framing would have looked for opportunity: in thread space, where a
single conversation would have to span both communities, mixing runs
four times below chance. In author space, where one person's quarterly
attention would have to span them, it runs at 70 percent of chance.
Individual minds cross community lines more readily than conversations
do, just not above chance.

### A second platform

Whether these regularities are facts about one forum or about discourse
is testable. We tested it with a pre-registered replication on a
structurally different corpus (acquisition and disclosures in Methods): Reddit financial discussion (six
subreddits, 41.5 million unique posts and comments, 2017-2024). There
the concept unit is the stock ticker, extracted by pattern matching and validated
against the SEC registrant table rather than produced by a language
model. The six subreddits are read as two strata, r/wallstreetbets
alone and the five analysis-oriented subreddits pooled, and as one
pooled set of all six. The design, criterion,
folds, the first fold's power analysis, and all interpretation
thresholds were fixed and committed before any outcome was computed.
The two
folds are separated by the 2020-2021 market regime change (build
2017-2018 with evaluation 2019; build 2022-2023 with evaluation 2024).

Both registered claims resolved. Formation was not significant in
either fold: 0 of 166 eligible pairs, then 1 of 478 against a floor of
4.8. Power limits this to "no effect larger than 3.7 and roughly 2
percent respectively", not "no effect"; the first figure was
registered, the second is post-hoc arithmetic disclosed in Methods. The single formed pair in the second
fold's pooled cell is itself a disclosed mechanical artifact. A symbol
that listed mid-build (ARM, September 2023) is automatically
"suppressed" early and automatically likely to co-occur later: a
survivorship pattern that inflates formation and therefore cannot
rescue the null result.
With Hacker News this closes the discovery hypothesis on a clean
negative spanning two platforms and two independent unit vocabularies.
Segregation: the registered pass threshold (z <= -3 in both folds) is met
by a wide margin in the pooled all-subreddits cell, which we take as primary
for symmetry with the formation readout. The registration left the
cell unspecified, and per-stratum readings vary (one fold-A stratum
sits at chance, below). Suppressed ticker pairs co-occur at z = -8.8
in the pre-regime fold (334 observed joint mentions against 544
expected) and z = -17.7 in the post-regime fold (726 against 1,383),
robust to counting only the $-prefixed cashtag form (z = -10.6).
Against Hacker News's z = -8.9 and -8.6, the finding generalizes
across platform, community, unit type, extraction method, and a market
regime change. It is larger after the change, not smaller.
Shuffle-based z values are quoted from the registered seed under
deterministic code; with 100 shuffle replicates the standard deviation of the shuffled
total implies roughly plus-minus 0.5 seed-to-seed variation at
these magnitudes, immaterial to every threshold.

One exploratory observation from the first fold did not survive the
second, and we report it as measured. In fold A the segregation lived
entirely in the analysis-oriented subreddits (z = -10.1) while
r/wallstreetbets sat exactly at chance (z = -0.1; not a power artifact,
since an analysis-stratum effect there would have shown z near -7). In
fold B r/wallstreetbets is strongly segregated (z = -9.0), like every
other stratum. The registered subsampling control agrees: matched to
the analysis stratum document counts, r/wallstreetbets remains at chance
in fold A (z = -0.0) and segregated in fold B (z = -5.2), so neither
reading is a document-count artifact. So community type is not a stable moderator of segregation in these
data. On its face the pattern is
regime-dependent (the same community at chance before 2020, segregated
after 2021), but that reading is post-hoc and confounded with the
folds' era and data-source differences, so we leave it as a described
observation. The registered, stable result is simpler: in the
post-regime fold, every stratum segregates.

A reproduction check accompanied the amended acquisition: the
analysis-stratum cells were recomputed on successive corpus rebuilds
and match (observed and eligible counts identical; z within the Monte
Carlo noise of the shuffled estimate; build documents differ by one due to
deduplication order, disclosed in the released run log). A registered confirmatory
run in the companion paper (Quiring 2026), on a single uniform data
source, reproduces the second fold's endpoint (all strata far below
chance, formation at the floor), so the second fold's result is not a
sourcing artifact; the census agreement between the two corpora is
given in Methods.

## Discussion

**A criterion to retire.** The z-style chance calibration we began with is not an exotic choice;
it is the natural first implementation of "co-occurs more than
expected" and variants of it appear throughout the co-occurrence and LBD
literatures (Church and Hanks 1989). Ecologists identified the defect in
this class of test decades ago and converged on fully constrained
permutation null models as the safer default in response (Introduction); to our
knowledge, text-corpus practice has not adopted that fix. Our
results measure what leaving it out costs: with heterogeneous document
sizes the partially constrained criterion produces large, stable,
replication-surviving effects where no real association exists. The 19-to-24-percent author-space rates survived two
further pre-registered evaluations with thresholds fixed in advance before the placebo
caught them. We urge text-corpus practice to adopt the control ecology
reached: a label-shuffle placebo, five lines of code and a few
CPU-minutes, as a mandatory control wherever a formation or emergence
rate is computed from co-occurrence counts. Where a claim must survive
that placebo, use per-pair permutation thresholds.

A related external question remains open. The science-corpus figure of
67 percent rests on the benchmark's own edge-existence ground truth
(Results), not on the criterion we retire here, so it is not
contaminated by this defect. But scientific corpora share the
structural features that make co-occurrence baselines unreliable:
rapid growth in density and heavily skewed degree distributions. Whether
that widely cited number is substantially mechanical under a permutation
test has, to our knowledge, never been tested. The question is outside
this paper's scope and under active investigation.

**What the negative does and does not say.** The null result is strong but scoped. It says: on a large general-technology
forum, over three years, with language-model-extracted concept units at two
granularities, and on eight years of Reddit financial discussion with
ticker units, expected-but-absent concept pairs show no above-chance
tendency to connect. The previously reported positive versions of
this effect on the same data are measurement artifacts. It does not say
that no discourse corpus anywhere shows real gap-closing (a
structurally different corpus is tested in the replication above). It does not
say that no individual pair ever genuinely connects (our per-pair
power is limited by rarity). And it says nothing about scientific
corpora except that their headline rates deserve re-measurement. Nor does it say formation never
occurs under any conditions. The companion paper's registered study on the
replication corpus (Quiring 2026) finds a confined above-floor
formation burst inside the windows around the January 2021 GameStop squeeze (windows
our folds exclude by design as a regime change), with formation at the
floor in every other window of six years. Even then the burst is
confined to r/wallstreetbets: the analysis-oriented stratum stayed
walled (co-occurrence far below chance) straight through the event. The negative reported here
is about discourse in its ordinary state; what cascades do is that
study's question.

Three limitations stand out. First, concept units come from a
language-model extraction. The science control shows the pipeline finds
real signal through comparable unit noise, and a registered robustness
check shows the results are insensitive to the attribution path, but
unit noise still bounds how sharp any concept-level claim can be. Second, author histories are truncated by the corpus
design (top-20 comments per thread), so author-space frequencies
undercount true activity; this shrinks the eligible universe but has no
evident mechanism for biasing formation direction. Third, raised by our
own internal adversarial review and untested: the label-shuffle placebo
preserves marginal frequencies but destroys temporal structure within
the evaluation window, so a null model that additionally preserved
within-window burst timing could in principle calibrate differently.
Constructing one is future work, and the segregation direction (real
data below even our permissive test) is unaffected.

**Segregation as the object of study.** Reading the result forward rather than as a failed prediction: the
persistence of suppressed-pair segregation is itself a measurable,
large, stable property of a discourse community, and plausibly varies
across communities, platforms, and time. A forum's "mixing deficit"
(observed joint attention over its shuffled expectation) is computable
with the machinery released here and may prove a more honest instrument
for studying how ideas spread, or fail to, than formation counts that
inherit the criterion trap. We offer it as the constructive replacement
for the discovery framing this paper set out to test.

The finding also supplies a measured regularity to literatures that
have so far had to assume it. Models of segmented investor attention take
persistent, sticky attention boundaries as a premise: Merton's (1987)
investor recognition hypothesis prices assets partly by which investors
are aware of them; Hong and Stein (1999) derive momentum from
information crossing investor segments only slowly; and Cohen and
Frazzini (2008) document returns
diffusing along economic links with a lag attributed to inattention to
connected firms. The empirical attention literature measures investor attention
itself and its price effects (Barber and Odean 2008; Da, Engelberg
and Gao 2011). Our replication corpus is such a setting, and
there the boundaries are directly visible: even analysis-oriented
finance communities mention economically adjacent tickers together at
less than half chance rates, in both folds, on either side of a market
regime change. Similarly, the returns to brokerage across "structural
holes" (Burt 2004) require that holes persist against the incentive to close
them; co-attention persistently below chance across a decade of discourse
on two platforms, 2015 to 2024, is consistent with that persistence, though it is measured between
concepts rather than between people. One implication runs the other
way: accounts in which new cross-domain narratives percolate upward
from public conversation are hard to square with both the segregation result and the author-space
timing evidence, in which co-occurrence preceded any written claim
connecting the pair. Discourse data alone cannot
settle how narratives interact with prices, however.

We built the co-occurrence index that literature-based discovery
needs and discourse corpora lack, and asked its defining question. Of
the ideas that should already have met, which will meet next? The answer is none of them, at rates distinguishable from error. That
answer is secured by a positive control, a registered placebo that
caught our own false positive, a corrected permutation criterion, and a
pre-registered replication on a second platform with independent
units. The durable fact is the
opposite one. In open discourse, the expected-but-absent pairs are not
discoveries waiting to happen; they are walls that persist, year
after year, on every platform we measured. Instruments that
claim otherwise should first be pointed at shuffled data.

## Methods

### Corpus

We use Hacker News, a technology discussion forum active since 2007,
whose archive begins in October 2006, chosen for its stable community
norms and public archive. The ingested corpus contains 1.32 million
discussion threads from 2006 through 2026; each document is a story
title plus its top twenty comments. Concept extraction, and therefore
every evaluation in this paper, covers 2015 through 2017, the span the
extraction budget allowed, with the folds placed inside it. All items carry source timestamps, and every derived artifact
in the pipeline preserves them (no lookahead at any stage; the sentence
embedding model used for auxiliary features predates the evaluation
windows).

### Concept extraction and attribution

Concepts are extracted by a pinned commercial language model (exact model
identifier, prompt version, and decoding configuration are part of the
released cache key; extraction configuration is fixed per run and
cached immutably per document). For 2015 through 2017, the full-document
extraction yields 1.17 million claims, each a paraphrased assertion with
a verbatim supporting quote and a list of lowercased concept strings.

For author-level analyses, each claim is attributed to the person who
wrote it by matching its verbatim quote against the thread's comments
(or the story title and the submitter's own text, in which case the
story author is credited). Attribution succeeds for 81 percent of claims (946,648 of
1,166,985), producing 2.5 million (author, concept, timestamp) rows.
Claims with no quote, an unmatched quote, or an ambiguous match are
dropped; a registered robustness check (Results, the placebo) shows the
results are not sensitive to the attribution path.

### Documents, suppressed pairs, and formation

Analyses use two document definitions. In **thread space**, a document
is one discussion thread. In **author space**, a document is one
author's set of concepts within one calendar quarter. Author-quarters
with more than 100 distinct concepts are excluded as hubs: without the
exclusion, hub documents' combinatorial co-occurrence collapses the
suppressed universe to 41 and 9 eligible pairs in the two folds
(commit appendix).

Within a **build window**, a concept is *frequent* if it appears in at
least 20 distinct documents. For frequent concepts i and j with document
frequencies f_i and f_j in N build documents, the pair is **eligible**
("suppressed") if its expected joint count E = f_i f_j / N is at least 2
while its observed build co-occurrence is zero. In words: the pair
should have met, given how often each side is discussed, and has not.

We evaluate on two temporal folds: build 2015 to 2016 with evaluation
year 2017 (fold 1), and build 2015 with evaluation year 2016 (fold 2).

A pair **forms** during the evaluation window if it newly co-occurs
beyond chance. The definition of "beyond chance" is the central question of this
paper, and we used two versions:

- **z-criterion (standard; used for the thread-space results and the
  author-space result):** at least 2
  evaluation documents contain both concepts, at least 2 distinct
  authors are involved, and the observed joint document count exceeds
  its marginal expectation by at least 2 standard deviations under a
  Poisson-style null model, z = (n_obs − E_eval) / sqrt(E_eval) ≥ 2.
- **Calibrated criterion (used for the placebo and the calibrated
  formation results):** the same structural
  minima, but the joint count must strictly exceed the 99th percentile
  of that specific pair's count distribution across 100 label-shuffled
  replicates of the evaluation window (concept labels permuted across
  document slots, preserving every document's size and every concept's
  total frequency). This makes each pair's false-positive rate about 1
  percent by construction, independent of document-size heterogeneity.

### Positive control on the Science4Cast benchmark

The positive control ran the thread-space eligibility and ranking
pipeline, unchanged, on the Science4Cast benchmark's 10-million-pair
sample (Krenn et al. 2023), with the benchmark's own edge-existence
ground truth as the outcome; the consequences of that definitional
difference are stated with the result. Its registration was written
before any ranker was scored against the benchmark's solution vector,
and the control was later re-executed from a separately pre-committed
registration on different hardware (Registration protocol).

### Registration protocol

Every evaluation in this paper was registered before it was run (Nosek
et al. 2018): the
unit definition, eligibility rule, fold boundaries, outcome criterion,
and interpretation thresholds were written to a registration file and
committed to version control. The evaluation code refuses to run
until the registration is in place. Outcome-blind quantities (document
counts, eligible-pair censuses) were appended to registrations before
outcomes were computed, with one exception disclosed under Replication corpus below:
the replication's second-fold census exists only in released artifacts
and was not appended to its registration. The repository's commit
history, released with the paper, provides independent timestamps
(Figure 4) for the ordering of every
registration and result, including the ones that overturned our own conclusions. A
second exception concerns the Science4Cast control: its registration and
result were originally committed together in a single commit, so for
that control the ordering rested on the working log rather than on
commit granularity. To close the gap, the control was subsequently
re-executed from a separately pre-committed registration on different
hardware (x86-64 Linux versus the original Apple Silicon; disclosed in
the registration), with MD5-verified inputs; the outputs matched the
originals exactly, byte for byte. Every Hacker News evaluation has a
registration commit that strictly precedes its result commit. The
registration files use working names that this paper does not: each
pass threshold is a bar, the cross-corpus comparison of formation rates
is the ladder, and the replication study is the gate, whose amended
readouts Q1 and Q1b are the replication's formation and segregation
claims reported here.

### Replication corpus and acquisition

The replication corpus is Reddit financial discussion: six subreddits,
41.5 million unique posts and comments, 2017-2024, with the stock
ticker as the concept unit, extracted by pattern matching and validated
against the SEC registrant table. The design, criterion, folds, the first fold's
power analysis, and all interpretation thresholds were fixed and
committed before any outcome was computed, and the two folds are separated by the
2020-2021 market regime change (build 2017-2018 with evaluation 2019;
build 2022-2023 with evaluation 2024).

The acquisition did not go to plan, and we disclose the sequence
because parts of it fall short of the strict outcome-blind
standard we hold elsewhere. Part of the archival source proved
unavailable mid-acquisition and was replaced by API pulls under dated
amendments. An interim evaluation ran before those amendments; its
partial-fold outcomes existed but had been voided in advance by a
committed interim clause. One stratum's early exemption from that
voiding was decided after its result was seen to replicate; the final
corpus later reproduced the stratum's counts exactly. A registered source-equivalence
check on the evaluation year was never performed: it was
rendered moot when we chose to acquire the evaluation year uniformly
from one source. Cross-source equivalence evidence therefore rests on
one build-era month (comments only), where the two sources agree at
99.96 percent. No
month is missing. The companion paper's independently acquired corpus
(same platform, a separate API pull on a different day, shared unit
rules) reproduces the first fold's r/wallstreetbets document census to
within one document (44,013 versus 44,012 author-quarters). Separately, a registered unit rule (exclusion of
index ETFs) was found unenforced in one extraction branch by an
internal adversarial review after the first complete run; the final
numbers reported in Results enforce it, which changed no conclusion. Two
registered secondary readouts were not computed, the author-persistence
module and the duplicate-rate checks; neither had a threshold attached. The second fold's
minimum-detectable-rate figure is post-hoc arithmetic on the final
census, computed by the registered formula but not itself registered.

### AI assistance

Analysis code, evaluations, and manuscript drafting were performed with
a large-language-model assistant operating under the author's direction.
All designs, thresholds, and interpretation rules were registered and
committed before evaluation; the version-control history documents the full sequence, including the
registered placebo that overturned an intermediate conclusion.

## Data availability

The Hacker News concept atlas (monthly concept frequencies,
co-occurrence edges, first-seen dates, economic-exposure labels, title
claims for the full archive, and the claim-pair paraphrase verdicts) is
deposited at Zenodo, doi:10.5281/zenodo.22262036, together with the
replication program's Reddit ticker-mention panel with hashed authors.
The per-document extraction cache, the author-attribution table, the
co-occurrence censuses, and every per-run result file are released with
the code repository at https://github.com/talecK/antikythera (private
during review; public at publication), with the commit references
listed in the commit appendix. Raw Hacker News content is public and
retrievable via the official API, and raw Reddit content via the
archival and API sources named in the replication registration; the
release includes exact pull specifications.

## Code availability

All pipeline code, evaluation scripts, the figure generator, and every
pre-registration file are released in the same repository, whose
version-control history timestamps every registration ahead of its
result.

## Competing interests

This research originated in a commercial signal-research effort by the
author; the studied hypothesis failed its registered tests and no
product, trading activity, or financial position resulted or exists.
The author declares no other competing interests.

## Funding

This research received no external funding.

## Author contributions

K.Q. conceived the study, wrote and registered the designs, built the
corpus and extraction pipeline, ran the analyses, and wrote the
manuscript.

## Figure legends

**Figure 1** (p1_schematic.png/.pdf). How the instrument is built, the
two readouts it produces, and why one formation criterion was retired.
(a) The document, two ways: a Hacker News thread (story plus top
comments) or one author's concepts within one calendar quarter. (b) An
eligible (we also call it suppressed) pair: two frequent concepts that never share a
document in the build window even though chance alone predicts at
least two shared documents. (c) The two folds: build on 2015 to 2016
and evaluate 2017; build on 2015 and evaluate 2016. (d) The segregation
statistic: the count of evaluation documents holding any eligible pair,
compared with 100 shuffles of concept labels that preserve every
document's size and every concept's frequency, giving z. (e) The two
criteria for calling a pair formed. Under the retired z-criterion,
whose expectation comes from each concept's own frequency, randomly
shuffled data form more pairs than the real data; under the per-pair
permutation criterion, both sit at the one-percent false-positive
floor. The dotted guide carries the left panel's scale into the right.
All values in this figure are illustrative; measured values are in
Figures 2 to 4.

**Figure 2** (fig1.png/.pdf). Observed versus shuffled. (a, b) The
placebo. For each author-space fold, the histogram shows how many
eligible suppressed pairs meet the z-criterion for formation in each of
100 label-shuffled replicates of the evaluation window; the vertical
line is the count observed in the real data. A replicate permutes
concept labels across document slots, preserving every document's size
and every concept's total frequency while destroying any real
association between concepts and people. (c) Segregation. The observed
number of evaluation documents in which any eligible pair co-occurs, as
a fraction of its mean under the same shuffle, in all four
space-by-fold cells; the bars span two standard deviations of the
shuffled total around its mean. Values below one mean suppressed pairs
co-occur less often than chance predicts. Throughout the paper, z is
the observed total minus the shuffled mean, divided by the shuffled
standard deviation.

**Figure 3** (fig2.png/.pdf). Formation rate by criterion. The share of
eligible suppressed pairs that form under the retired z-criterion and
under the per-pair permutation criterion, in all four cells, on a log
scale, against the one-percent false-positive floor that the
permutation criterion produces by construction. The author-space fold 2
cell formed no pairs under the permutation criterion and is marked 0.

**Figure 4** (fig3.png/.pdf). Registration protocol. Each evaluation's
registration commit and result commit on a common timeline, from
repository timestamps. The asterisk marks the positive control, whose
registration and result were originally committed together; its
re-execution from a separately pre-committed registration, and the
post-review regeneration of every number, appear in the repository
history and in the commit appendix.

## Appendix: where every number comes from

All artifacts live in the repository named under Data availability,
whose commit history timestamps every registration ahead of its result.
The numbers in this paper trace as follows.

| quantity | artifact | commit |
|---|---|---|
| Registrations, thread space (runs 1 to 4) | preregistration.md | f692468 (run 1), 12b324c (run 2), f1304dc (run 3), 3ec6bb2 (run 4, terminal) |
| Positive control, registration and result (single commit, disclosed) | preregistration_tier_a.md, reports/tier_a.md | a884a49 |
| Positive control, re-execution | preregistration_tier_a_rerun.md, eval/compare_tier_a_rerun.py | 347e21a (registered), 71a2c4c (result) |
| Author-space registration (run 5) | preregistration_run5.md | ce6d639 |
| Exposed-pair and articulation registration (run 6) | preregistration_run6.md | d3844c1 |
| Robustness suite registration (placebo, window, articulation, attribution) | preregistration_robustness.md | 31bc9ab |
| Calibrated-criterion registration (run 8) | preregistration_run8.md | 63b72d9 |
| Replication registration and amendments | preregistration_gate.md | 5e88c05 (draft), 829383f (registered; segregation co-primary), dbcfed1 (uniform evaluation-year source), a67d556 (dated corrections) |
| Run log: every result in registration order | reports/pilot1_runs.md | c7b1e7c (thread-space kill), 1e98aaa (run 5), b244d65 (run 6), eb4c74a (robustness), 58eb65b (run 8), 1386fc0 (replication final) |
| Post-review regeneration of every number on deterministic artifacts | reports/pilot1_runs.md, gate v2 table | a67d556; 8bcdca9 (power note) |
| Author attribution pipeline | pipeline/build_author_concepts.py | ce6d639; d3844c1 |
| Evaluation code (thread, author, robustness, calibrated, replication) | eval/run_eval3.py, eval/run_eval5.py, eval/run_robustness.py, eval/run_eval8.py, eval/run_gate.py | f89cb2b (deterministic pipeline, review fixes) |
| Internal adversarial review, committed verbatim | reports/adversarial_review_2026-08-31.md | 45455bc |
| Figure 1 (schematic, no data) | eval/make_paper1_schematic.py, reports/figures/p1_schematic | b2ebfd2 |
| Figures 2 to 4 | eval/make_paper_figs.py, reports/figures/fig1-3 (shared style eval/paper2_figstyle.py) | 7a1a118; regenerated a67d556; restyled b2ebfd2 |

## References

- Swanson, D.R. (1986a). Fish oil, Raynaud's syndrome, and undiscovered
  public knowledge. *Perspectives in Biology and Medicine* 30(1), 7-18.
  doi:10.1353/pbm.1986.0087
- Swanson, D.R. (1986b). Undiscovered public knowledge. *The Library
  Quarterly* 56(2), 103-118. doi:10.1086/601720
- Smalheiser, N.R., Swanson, D.R. (1998). Using ARROWSMITH: a
  computer-assisted approach to formulating and assessing scientific
  hypotheses. *Computer Methods and Programs in Biomedicine* 57(3),
  149-153. doi:10.1016/S0169-2607(98)00033-9
- Rzhetsky, A., Foster, J.G., Foster, I.T., Evans, J.A. (2015). Choosing
  experiments to accelerate collective discovery. *PNAS* 112(47),
  14569-14574. doi:10.1073/pnas.1509757112
- Krenn, M., Zeilinger, A. (2020). Predicting research trends with
  semantic and neural networks with an application in quantum physics.
  *PNAS* 117(4), 1910-1916. doi:10.1073/pnas.1914370116
- Krenn, M., Buffoni, L., Coutinho, B., et al. (2023). Forecasting the
  future of artificial intelligence with machine learning-based link
  prediction in an exponentially growing knowledge network. *Nature
  Machine Intelligence* 5, 1326-1335. doi:10.1038/s42256-023-00735-0
- Tshitoyan, V., Dagdelen, J., Weston, L., et al. (2019). Unsupervised
  word embeddings capture latent knowledge from materials science
  literature. *Nature* 571, 95-98. doi:10.1038/s41586-019-1335-8
- Uzzi, B., Mukherjee, S., Stringer, M., Jones, B. (2013). Atypical
  combinations and scientific impact. *Science* 342(6157), 468-472.
  doi:10.1126/science.1240474
- Foster, J.G., Rzhetsky, A., Evans, J.A. (2015). Tradition and
  innovation in scientists' research strategies. *American Sociological
  Review* 80(5), 875-908. doi:10.1177/0003122415601618
- Liben-Nowell, D., Kleinberg, J. (2007). The link-prediction problem
  for social networks. *JASIST* 58(7), 1019-1031. doi:10.1002/asi.20591
- Aiyappa, R., Wang, X., Kim, M., Seckin, O.C., Yoon, J., Ahn, Y.-Y.,
  Kojaku, S. (2025). Implicit degree bias in the link prediction task.
  *Proceedings of the 42nd International Conference on Machine Learning*,
  PMLR 267, 874-908. https://proceedings.mlr.press/v267/aiyappa25a.html
- Aghajohari, M., Akhondzadeh, M.S., Ashkboos, S., Chitsaz, K. (2021).
  Degree-based feature is all you need: Science4Cast report. *IEEE
  International Conference on Big Data 2021*, 5791-5794.
  doi:10.1109/BigData52589.2021.9671530
- Maslov, S., Sneppen, K. (2002). Specificity and stability in topology
  of protein networks. *Science* 296(5569), 910-913.
  doi:10.1126/science.1065103
- Merton, R.C. (1987). A simple model of capital market equilibrium with
  incomplete information. *Journal of Finance* 42(3), 483-510.
  doi:10.1111/j.1540-6261.1987.tb04565.x
- Hong, H., Stein, J.C. (1999). A unified theory of underreaction,
  momentum trading, and overreaction in asset markets. *Journal of
  Finance* 54(6), 2143-2184. doi:10.1111/0022-1082.00184
- Cohen, L., Frazzini, A. (2008). Economic links and predictable
  returns. *Journal of Finance* 63(4), 1977-2011.
  doi:10.1111/j.1540-6261.2008.01379.x
- Burt, R.S. (2004). Structural holes and good ideas. *American Journal
  of Sociology* 110(2), 349-399. doi:10.1086/421787
- Gotelli, N.J., Graves, G.R. (1996). *Null Models in Ecology*.
  Smithsonian Institution Press.
- Connor, E.F., Simberloff, D. (1979). The assembly of species
  communities: chance or competition? *Ecology* 60(6), 1132-1140.
  doi:10.2307/1936961
- Gotelli, N.J. (2000). Null model analysis of species co-occurrence
  patterns. *Ecology* 81(9), 2606-2621.
  doi:10.1890/0012-9658(2000)081[2606:NMAOSC]2.0.CO;2
- Gotelli, N.J., Ulrich, W. (2012). Statistical challenges in null
  model analysis. *Oikos* 121(2), 171-180.
  doi:10.1111/j.1600-0706.2011.20301.x
- Henry, S., McInnes, B.T. (2017). Literature based discovery: models,
  methods, and trends. *Journal of Biomedical Informatics* 74, 20-32.
  doi:10.1016/j.jbi.2017.08.011
- Sebastian, Y., Siew, E.-G., Orimaye, S.O. (2017). Emerging approaches
  in literature-based discovery: techniques and performance review.
  *The Knowledge Engineering Review* 32, e12.
  doi:10.1017/S0269888917000042
- Thilakaratne, M., Falkner, K., Atapattu, T. (2019). A systematic
  review on literature-based discovery. *ACM Computing Surveys* 52(6),
  1-34. doi:10.1145/3365756
- Callon, M., Courtial, J.P., Laville, F. (1991). Co-word analysis as a
  tool for describing the network of interactions between basic and
  technological research: the case of polymer chemistry.
  *Scientometrics* 22(1), 155-205. doi:10.1007/BF02019280
- Newman, M.E.J. (2001). Clustering and preferential attachment in
  growing networks. *Physical Review E* 64(2), 025102.
  doi:10.1103/PhysRevE.64.025102
- Kossinets, G., Watts, D.J. (2006). Empirical analysis of an evolving
  social network. *Science* 311(5757), 88-90.
  doi:10.1126/science.1116869
- McPherson, M., Smith-Lovin, L., Cook, J.M. (2001). Birds of a feather:
  homophily in social networks. *Annual Review of Sociology* 27,
  415-444. doi:10.1146/annurev.soc.27.1.415
- Adamic, L.A., Glance, N. (2005). The political blogosphere and the
  2004 U.S. election: divided they blog. *Proceedings of the 3rd
  International Workshop on Link Discovery (LinkKDD)*, 36-43.
  doi:10.1145/1134271.1134277
- Conover, M., Ratkiewicz, J., Francisco, M., Goncalves, B., Menczer,
  F., Flammini, A. (2011). Political polarization on Twitter.
  *Proceedings of the International AAAI Conference on Web and Social
  Media* 5(1), 89-96. doi:10.1609/icwsm.v5i1.14126
- Cinelli, M., De Francisci Morales, G., Galeazzi, A., Quattrociocchi,
  W., Starnini, M. (2021). The echo chamber effect on social media.
  *PNAS* 118(9), e2023301118. doi:10.1073/pnas.2023301118
- Waller, I., Anderson, A. (2021). Quantifying social organization and
  political polarization in online platforms. *Nature* 600, 264-268.
  doi:10.1038/s41586-021-04167-x
- Church, K.W., Hanks, P. (1989). Word association norms, mutual
  information, and lexicography. *Proceedings of the 27th Annual Meeting
  of the Association for Computational Linguistics*, 76-83.
  doi:10.3115/981623.981633
- Barber, B.M., Odean, T. (2008). All that glitters: the effect of
  attention and news on the buying behavior of individual and
  institutional investors. *Review of Financial Studies* 21(2),
  785-818. doi:10.1093/rfs/hhm079
- Da, Z., Engelberg, J., Gao, P. (2011). In search of attention.
  *Journal of Finance* 66(5), 1461-1499.
  doi:10.1111/j.1540-6261.2011.01679.x
- Nosek, B.A., Ebersole, C.R., DeHaven, A.C., Mellor, D.T. (2018). The
  preregistration revolution. *PNAS* 115(11), 2600-2606.
  doi:10.1073/pnas.1708274114
- Quiring, K. (2026). Watching the walls go up: r/wallstreetbets
  segregated after the GameStop squeeze. Preprint; SocArXiv DOI
  inserted at posting.
