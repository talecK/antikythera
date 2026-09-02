# The gaps that don't close: idea segregation persists in twenty years of online discourse

**Author:** Kevin Quiring (independent researcher)

**Draft v0.2, 2026-08-31. Target shape: EPJ Data Science research article.
All results final; awaiting author prose pass.**

---

## Abstract

In science, two well-studied ideas that are never discussed together
make a likely candidate for a future discovery. Predicting which pair
connects next is the aim of literature-based discovery. Whether this
holds in online discussion is untested. Here we test it on 1.3 million
Hacker News discussions over twenty years, with a pre-registered
replication on 41.5 million Reddit finance posts using stock tickers.
Four pre-registered evaluations use threads, then authors, as documents.
Pairs never discussed together, called suppressed pairs, connect no more
than popularity and overlapping topics predict. On the Science4Cast
benchmark of AI papers, where the effect is known, the same method finds
it. The standard test against chance flags connections too easily when
document sizes vary. It reported 19 to 24 percent of pairs connecting
within authors' quarterly output, yet randomly shuffled data connected
more pairs than real data. A per-pair permutation test leaves new
connections no higher than false positives alone produce. Overall,
suppressed pairs appear together far below chance: nearly 9 standard
deviations at author level, over 100 at thread level. Both results
replicate across the 2020-2021 market regime change. Ideas that never
meet online mark communities that stay apart, not future discoveries
waiting to happen.

---

## 1. Introduction

Some discoveries are visible before they are made. Swanson (1986) noticed
that the medical literature on dietary fish oil and the literature on
Raynaud's syndrome shared intermediate findings yet never cited one
another, inferred a connection, and was later proven right. The insight
became literature-based discovery (LBD): map which concepts co-occur in a
corpus, find pairs that statistically should have met but have not, and
treat those pairs as candidate discoveries. On scientific corpora the
approach appears strikingly effective. In the Science4Cast benchmark,
built from 143,000 artificial-intelligence papers, concept pairs can be
ranked by their probability of future connection well above chance (Krenn
et al. 2023). Word embeddings trained on materials-science abstracts
flagged thermoelectric compounds years before their discovery papers
(Tshitoyan et al. 2019).

Scientific literature is a small and unusual corner of written thought.
The bulk of recorded reasoning happens in ordinary discourse: forums,
comment threads, industry discussion. If expected-but-absent concept
pairs predict future connections there, the applications are broad, from
research recommendation to trend analysis. To our knowledge the transfer
has not been tested, chiefly because discourse lacks the self-indexing
that makes science tractable: no citations, no keywords, no discrete
units. This paper builds that index for one large corpus and runs the
test.

Our answer is negative, and the path to it is part of the contribution.
The headline results are three.

First, a certified null. On twenty years of Hacker News, suppressed
concept pairs do not connect above chance at any document granularity we
tested, under evaluations whose designs were frozen and committed before
any outcome was computed. The instrument is not at fault: the identical
harness, pointed at Science4Cast, recovers the known signal at roughly
105 times random precision.

Second, a measurement trap with likely reach beyond this study. The
standard way to score a new co-occurrence as "real" is a
chance-calibrated test: observed joint document count against an
expected count derived from the two concepts' marginal frequencies. We
show this criterion is badly anti-conservative when documents vary in
size, as they do in virtually every real corpus. In our author-level
analysis it manufactured formation rates of 19 to 24 percent that
survived two further pre-registered evaluations. A placebo test,
registered with its failure condition stated in advance, then revealed
that randomly shuffled data "forms" two to four times more pairs than
the real data. We describe the corrected criterion (a per-pair permutation
null) and suggest the shuffle as a mandatory control for co-occurrence
formation claims generally.

Third, a positive finding we did not seek. Under the corrected
criterion, suppressed pairs do not merely fail to connect. They
co-occur below chance, by nearly 9 standard deviations at the author
level and by more than 100 at the thread level. The communities of attention
around two ideas that have never met tend to stay apart, at rates far
beyond what their sizes explain. In discourse, the gaps that
literature-based discovery hunts for do not close. They persist,
far below chance, everywhere we measured.

The rest of the paper proceeds conventionally. Section 2 situates the
work. Section 3 describes the corpus, the extraction pipeline, and the
pre-registration protocol. Section 4 reports the thread-level null and
the positive control. Section 5 reports the author-level revival, the
placebo that killed it, and the corrected analysis. Section 6 discusses
implications and limitations.

## 2. Related work

**Literature-based discovery.** Swanson's fish-oil result (1986) and its
successors established gap-finding on scientific text (Smalheiser and
Swanson 1998). Krenn and Zeilinger (2020) formalized the co-occurrence
graph approach on quantum-physics abstracts. The Science4Cast benchmark
(Krenn et al. 2023) turned it into a machine-learning competition on a
64,000-node concept graph, with link-prediction AUCs above 0.9 for the
best methods on the main task. Tshitoyan et al. (2019) is the flagship prospective result.
Our study is, to our knowledge, the first application of this machinery
to non-scientific discourse, and our positive control reuses
Science4Cast directly.

**Novelty and recombination.** Uzzi, Mukherjee, Stringer and Jones
(2013) showed that high-impact papers combine a conventional core with a
small number of atypical journal pairings. Foster, Rzhetsky and
Evans (2015) documented the risk-reward tradeoff of unconventional
combinations. This literature measures the value of rare combinations;
ours measures whether expected combinations happen at all.

**Link prediction and its pathologies.** Co-occurrence gap prediction is
link prediction on a growing graph (Liben-Nowell and Kleinberg 2007).
Aiyappa et al. (2025) showed that standard link-prediction evaluation
carries an implicit degree bias: a degree-only ranker is near optimal on
many benchmarks. A Science4Cast competition entry demonstrated the same
point in practice, winning with degree features alone (Aghajohari 2021).
Our thread-level findings echo this: the only surviving predictor
families are node popularity and triadic closure. A companion study
(in preparation) examines the Science4Cast benchmark itself in this
light.

**Null models for co-occurrence.** Ecology confronted this exact
problem class decades ago: whether species co-occur more or less than
chance, tested against nulls that hold row and column totals of a
site-by-species matrix to varying degrees. That literature measured
the Type I inflation of partially constrained nulls and settled on
fully constrained ("fixed-fixed") randomizations as the defensible
default (Connor and Simberloff 1979; Gotelli 2000; Gotelli and Ulrich
2012; Gotelli and Graves 1996; see also Maslov and Sneppen 2002 for
the network analog). Our corrected criterion is a member of that
family, implemented as a label permutation on the document-concept
incidence structure, and the failure we document in the standard
text-corpus criterion is the known failure of its partially
constrained analog. We claim no novelty for the fix; the contribution
is the transfer, and the measurement of what not making it costs.

## 3. Data and methods

### 3.1 Corpus

We use Hacker News, a technology discussion forum active since 2007,
chosen for its twenty-year span, stable community norms, and public
archive. The corpus contains 1.32 million discussion threads from 2006
through 2026; each document is a story title plus its top twenty
comments. All items carry source timestamps, and every derived artifact
in the pipeline preserves them (no lookahead at any stage; the sentence
embedding model used for auxiliary features predates the evaluation
windows).

### 3.2 Concept extraction and attribution

Concepts are extracted by a pinned commercial language model (exact model
identifier, prompt version, and decoding configuration are part of the
released cache key; extraction configuration is frozen per run and
cached immutably per document). For 2015 through 2017, the full-document
extraction yields 1.17 million claims, each a paraphrased assertion with
a verbatim supporting quote and a list of lowercased concept strings.

For author-level analyses, each claim is attributed to the person who
wrote it by matching its verbatim quote against the thread's comments
(or the story title and self-text, in which case the story author is
credited). Attribution succeeds for 81 percent of claims (946,648 of
1,166,985), producing 2.5 million (author, concept, timestamp) rows.
Claims with no quote, an unmatched quote, or an ambiguous match are
dropped; Section 5.4 shows the results are not sensitive to the
attribution path.

### 3.3 Documents, suppressed pairs, and formation

Analyses use two document definitions. In **thread space**, a document
is one discussion thread. In **author space**, a document is one
author's set of concepts within one calendar quarter. Author-quarters
with more than 100 distinct concepts are excluded as hubs: without the
guard, hub documents' combinatorial co-occurrence collapses the
suppressed universe to 41 and 9 eligible pairs in the two folds
(released with the artifacts).

Within a **build window**, a concept is *frequent* if it appears in at
least 20 distinct documents. For frequent concepts i and j with document
frequencies f_i and f_j in N build documents, the pair is **eligible**
("suppressed") if its expected joint count E = f_i f_j / N is at least 2
while its observed build co-occurrence is zero. In words: the pair
should have met, given how often each side is discussed, and has not.

We evaluate on two temporal folds: build 2015 to 2016 with evaluation
year 2017 (fold 1), and build 2015 with evaluation year 2016 (fold 2).

A pair **forms** during the evaluation window if it newly co-occurs
beyond chance. The definition of "beyond chance" is the crux of this
paper, and we used two versions:

- **z-criterion (standard, used in Sections 4 and 5.1):** at least 2
  evaluation documents contain both concepts, at least 2 distinct
  authors are involved, and the observed joint document count exceeds
  its marginal expectation by at least 2 standard deviations under a
  Poisson-style null, z = (n_obs − E_eval) / sqrt(E_eval) ≥ 2.
- **Calibrated criterion (Sections 5.2 to 5.3):** the same structural
  minima, but the joint count must strictly exceed the 99th percentile
  of that specific pair's count distribution across 100 label-shuffled
  replicates of the evaluation window (concept labels permuted across
  document slots, preserving every document's size and every concept's
  total frequency). This makes each pair's false-positive rate about 1
  percent by construction, independent of document-size heterogeneity.

### 3.4 Pre-registration protocol

Every evaluation in this paper was registered before it was run: the
unit definition, eligibility rule, fold boundaries, outcome criterion,
and interpretation thresholds were written to a registration file and
committed to version control. The evaluation code refuses to run
until the registration is in place. Outcome-blind quantities (document
counts, eligible-pair censuses) were appended to registrations before
outcomes were computed, with one exception disclosed in Section 6.3:
the replication's second-fold census exists only in released artifacts
and was not appended to its registration. The repository's commit
history, released with the paper, provides independent timestamps
(Figure 3) for the ordering of every
registration and result, including the ones that embarrassed us. One
exception is disclosed: the Science4Cast control's registration and
result were originally committed together in a single commit, so for
that control the ordering rested on the session record rather than on
commit granularity. To close the gap, the control was subsequently
re-executed from a separately pre-committed registration on different
hardware (x86-64 Linux versus the original Apple Silicon; disclosed in
the registration), with MD5-verified inputs; the outputs matched the
originals exactly, byte for byte. Every Hacker News evaluation has a
registration commit that strictly precedes its result commit.

## 4. Thread-level results: a certified null

### 4.1 No signal at any granularity

Four registered evaluations tested the discovery thesis in thread space.
At claim-level granularity nothing repeats: the co-occurrence graph over
paraphrased claims is empty and the analysis is degenerate. At
concept-level granularity the graph is dense and eligible suppressed
pairs are plentiful (25,161 in fold 1; 7,505 in fold 2), but under the
z-criterion only 0.60 and 0.68 percent of them form. Ranking within
the eligible set adds nothing. The only feature family that beats random
ordering is triadic closure (common neighbors), at precision-at-200
around 2.5 percent, roughly 4 times random: exactly the generic
network-science baseline that requires none of the discovery apparatus.
Semantic features (embedding affinity between concept labels) are
indistinguishable from random. Restricting to economically relevant
vocabulary (a registered classification of concepts into exposed versus
generic) leaves 8 formations per year in fold 1 and 1 in fold 2 across
the entire site.

### 4.2 The instrument finds the signal where it exists

A null of this kind is only as credible as its instrument, so we ran
the identical eligibility and ranking harness, unchanged, on the
Science4Cast benchmark where the signal is known to exist. It finds it:
ranked precision reaches roughly 105 times random, and our feature set
reaches AUC 0.899 against the benchmark's published 15-feature baseline
of 0.851. Within the benchmark's suppressed subset (expected joint
count at least 2, no prior co-occurrence), 67 percent of pairs connect
(188 of 281 in a 10-million-pair sample).

One definitional difference matters and is easy to miss, so we state it
plainly. Formation on the benchmark is the benchmark's own ground
truth: the appearance of any edge in the target-year graph. Our
discourse analyses use the chance-calibrated criterion of Section 3.3.
The control therefore certifies the harness (eligibility construction,
ranking, precision measurement) and not the formation criterion, which
the benchmark never exercises. It also means the 67 percent is not
commensurable with any discourse rate in this paper: "any edge appears"
and "co-mention exceeds a calibrated null across two independent
authors" are different events. Early in this project we treated the two
as rungs of one calibration ladder; that comparison was ill-posed and
we withdraw it here. Whether the benchmark's 67 percent is itself
substantially mechanical (the AI concept graph densifies rapidly over
the target years) is a further open question, outside this paper's
scope.

One observation from this control does carry forward: in science as on
Hacker News, popularity features tie or beat closure and semantic
features add nothing, consistent with the degree-bias literature
(Aiyappa et al. 2025).

## 5. The author-level revival and its correction

### 5.1 An apparent thirty-fold effect

Threads are rooms; ideas connect in people. On this reasoning we
re-defined the document as an author-quarter and re-ran the identical
formulation (registered before evaluation, as always). The structure of
the problem changed sharply: eligible suppressed pairs became rare (364
in fold 1, 110 in fold 2, versus tens of thousands in thread space),
resembling the science benchmark. Under the z-criterion they formed
at 19.2 and 23.6 percent, thirty times the thread-space rate. The effect
survived two further registered evaluations: it held at 23.1 percent on
economically relevant vocabulary (6 of 26 exposed pairs, against a
registered bar of 3). A registered follow-up showed the formations
were almost never accompanied by any written claim connecting the two
concepts, suggesting the two audiences were converging before anyone
articulated the link. For roughly one day, the working conclusion of
this project was that thread-level co-occurrence had simply been the
wrong measurement, and that individuals do bridge expected-but-absent
pairs at high rates.

### 5.2 The placebo

Author-quarter documents vary widely in size (median 5 concepts, 90th
percentile 21, maximum 100 under the hub guard). Before drafting any
claims we registered a placebo: shuffle the concept labels across the
evaluation window's document slots, and count how many eligible pairs
"form" under the z-criterion in 100 such replicates. The shuffle
preserves every document's size and every concept's total frequency
while destroying any real association between concepts and people. The
registration specified the failure condition in advance: a null mean at
or above half the observed count would be reported as a revision of the
result, not a nuance.

The placebo did not merely halve the result. Shuffled data forms more
pairs than the real data (Figure 1, top): 125.1 on average versus 70
observed in fold 1,
and 53.0 versus 26 in fold 2. The observed counts sit 5.8 and 5.0
standard deviations below their own mechanical nulls. The z-criterion's
internal expectation, built from marginal frequencies, does not account
for the fact that large documents generate joint occurrences
combinatorially; with heterogeneous document sizes, random assignment
clears z ≥ 2 constantly. The 19-to-24-percent rate was an artifact of
the measuring stick. Registered sensitivity analyses confirmed the
artifact lives in the criterion and nowhere else. The rate is stable
under monthly and half-yearly document windows (9.7 to 27.8 percent)
and under a conservative attribution lens that discards all
story-author credits (24.9 and 27.5 percent). Yet all of these numbers
sit below their own shuffled nulls: in every window and every lens the
observed formation count falls below the minimum of its 100 shuffle
replicates (released artifacts).

### 5.3 Calibrated formation: nothing, anywhere

We then registered and ran the corrected criterion (per-pair permutation
null, Section 3.3) in both document spaces and both folds, with the
interpretation bars again frozen in advance. Formation collapses to the
false-positive floor everywhere (Figure 2):

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

### 5.4 The gaps are held open

The same permutation machinery yields a second, better-powered
statistic: the total number of joint occurrences across all eligible
pairs, observed versus shuffled (Figure 1, bottom). Here the data speak
loudly, in the
direction opposite to the discovery thesis:

| space | fold | observed total | null mean (sd) | z |
|-------|------|---------------:|---------------:|----:|
| author | 1 | 746 | 1,057 (35) | −8.9 |
| author | 2 | 454 | 647 (23) | −8.6 |
| thread | 1 | 12,098 | 48,378 (238) | −152 |
| thread | 2 | 7,866 | 28,274 (166) | −123 |

Suppressed pairs co-occur at roughly 70 percent of chance in author
space and roughly a quarter of chance in thread space. The registered
claim bar for this statistic (z ≤ −3 in both author folds) is met
overwhelmingly, in both spaces. The interpretation is simple and, we
believe, the paper's most durable finding: two concepts that have never
co-occurred, despite ample independent popularity, are not on their way
to meeting. Their audiences are substantially disjoint and remain so.
Discourse does not slowly mix; its communities of attention
persistently fail to overlap, at magnitudes far beyond what topic sizes explain. The
suppressed pairs of literature-based discovery are, in discourse,
markers of persistent segregation rather than latent connection.

Descriptively, the segregation is strongest exactly where the discovery
framing would have looked for opportunity: in thread space, where a
single conversation would have to span both communities, mixing runs
four times below chance. In author space, where one person's quarterly
attention would have to span them, it runs at 70 percent of chance.
Individual minds cross community lines more readily than conversations
do, just not above chance.

## 6. Discussion

### 6.1 A criterion to retire

The z-style chance calibration we began with is not an exotic choice;
it is the natural first implementation of "co-occurs more than
expected" and variants of it appear throughout the co-occurrence, LBD,
and trend detection literatures. Ecologists identified the defect in
this class of test roughly twenty-five years ago and standardized on
fully constrained permutation nulls in response (Section 2); to our
knowledge, text-corpus practice never absorbed that lesson. Our
results measure what the omission costs: with heterogeneous document
sizes the partially constrained criterion manufactures large, stable,
replication-surviving effects from nothing. The 19-to-24-percent author-space rates survived two
further pre-registered evaluations with frozen thresholds before the placebo
caught them. We urge text-corpus practice to adopt what ecology already
settled: a label-shuffle placebo, five lines of code and a few
CPU-minutes, as a mandatory control wherever a formation or emergence
rate is computed from co-occurrence counts, and per-pair permutation
thresholds where the claim needs to survive it.

A related external question remains open. The science-corpus figure of
67 percent rests on the benchmark's own edge-existence ground truth
(Section 4.2), not on the criterion we retire here, so it is not
contaminated by this defect. But scientific corpora share the
structural features that make co-occurrence baselines treacherous:
rapid densification and heavily skewed degree distributions. Whether
that celebrated number is substantially mechanical under a shuffle
null has, to our knowledge, never been tested. The question is outside
this paper's scope and under active investigation.

### 6.2 What the negative does and does not say

The null is strong but scoped. It says: on a large general-technology
forum, over twenty years, with LLM-extracted concept units at two
granularities, expected-but-absent concept pairs show no above-chance
tendency to connect, and the previously reported positive versions of
this effect on the same data are measurement artifacts. It does not say
that no discourse corpus anywhere shows real gap-closing (a
structurally different corpus is tested in Section 6.3). It does not
say that no individual pair ever genuinely connects (our per-pair
power is limited by rarity). And it says nothing about scientific
corpora except that their headline rates deserve re-measurement. Nor does it say formation never
occurs under any conditions. A registered follow-up study on the
replication corpus (in preparation) finds a confined above-floor
formation burst inside the 2021 meme-stock cascade windows (windows
our folds exclude by design as a regime break), with formation at the
floor in every other window of six years. Even then the burst is
confined to the meme community: the analysis-oriented stratum stayed
walled (co-mention far below chance) straight through the event. The negative reported here
is about discourse in its ordinary state; what cascades do is that
study's question.

Two limitations deserve emphasis. First, concept units come from a
language-model extraction. The science control shows the harness finds
real signal through comparable unit noise, and a registered robustness
check shows the results are insensitive to the attribution path, but
unit mushiness still bounds how sharp any concept-level claim can be. Second, author histories are truncated by the corpus
design (top-20 comments per thread), so author-space frequencies
undercount true activity; this shrinks the eligible universe but has no
evident mechanism for biasing formation direction. Third, raised by our
own internal adversarial review and untested: the label-shuffle placebo
preserves marginal frequencies but destroys temporal structure within
the evaluation window, so a null model that additionally preserved
within-window burst timing could in principle calibrate differently.
Constructing one is future work, and the segregation direction (real
data below even our permissive null) is unaffected.

### 6.3 A second platform

Whether these regularities are facts about one forum or about discourse
is testable. We tested it with a pre-registered replication on a
structurally different corpus: Reddit financial discussion (six
subreddits, 41.5 million unique posts and comments, 2017-2024). There
the concept unit is the stock ticker, regex-extracted and validated
against the SEC registrant table rather than produced by a language
model. The design, criterion,
folds, the first fold's power analysis, and all interpretation bars
were frozen and committed before any outcome was computed. The two
folds are separated by the 2020-2021 market regime break (build
2017-2018 with evaluation 2019; build 2022-2023 with evaluation 2024).

The acquisition did not go to plan, and we disclose the sequence
precisely because parts of it fall short of the strict outcome-blind
standard we hold elsewhere. Part of the archival source proved
unavailable mid-acquisition and was replaced by API pulls under dated
amendments. An interim evaluation ran before those amendments; its
partial-fold outcomes existed but had been voided in advance by a
committed interim clause. One stratum's early exemption from that
voiding was decided after seeing its result replicate - a
choose-after-seeing step, later validated when the final corpus
reproduced the stratum's counts exactly. A registered source-
equivalence check on the evaluation year was never performed: it was
rendered moot when we chose to acquire the evaluation year uniformly
from one source. Cross-source equivalence evidence therefore rests on
one build-era month (comments only), where the two sources agree at
99.96 percent. No
month is missing. Separately, a registered unit rule (exclusion of
index ETFs) was found unenforced in one extraction branch by an
internal adversarial review after the first complete run; the final
numbers below enforce it, which changed no conclusion. Registered
secondary readouts not computed: the author-persistence module and
duplicate-rate hygiene counts (no bars attached). The second fold's
minimum-detectable-rate figure is post-hoc arithmetic on the final
census, computed by the registered formula but not itself registered.

Both registered claims resolved. Formation: not significant in either
fold (0 of 166 eligible pairs, then 1 of 478 against a floor of 4.8;
power limits this to "no effect larger than 3.7 and roughly 2 percent
respectively," not "no effect" - the first figure registered, the
second post-hoc as noted above). The single formed pair in the second
fold's pooled cell is itself a disclosed mechanical artifact. A symbol
that listed mid-build (ARM, September 2023) is automatically
"suppressed" early and automatically likely to co-occur later: a
survivorship pattern that inflates formation and therefore cannot
rescue the null.
With Hacker News this closes the discovery hypothesis on a clean
negative spanning two platforms and two independent unit vocabularies.
Segregation: the registered bar (z <= -3 in both folds) is met
decisively in the pooled all-subreddits cell, which we take as primary
for symmetry with the formation readout. The registration left the
cell unspecified, and per-stratum readings vary (one fold-A stratum
sits at chance, below). Suppressed ticker pairs co-occur at z = -8.8
in the pre-regime fold (334 observed joint mentions against 544
expected) and z = -17.7 in the post-regime fold (726 against 1,383),
robust to the ticker-extraction lens (cashtags only: z = -10.6).
Against Hacker News's z = -8.9 and -8.6, the finding generalizes
across platform, community, unit type, extraction method, and a market
regime change - and is larger after the regime break, not smaller.
(Shuffle-based z values are quoted from the registered seed under a
deterministic harness; with 100 shuffle replicates the null-sd
estimate implies roughly plus-minus 0.5 seed-to-seed variation at
these magnitudes, immaterial to every bar.)

One exploratory observation from the first fold did not survive the
second, and we report it as measured. In fold A the segregation lived
entirely in the analysis-oriented subreddits (z = -10.1) while
wallstreetbets sat exactly at chance (z = -0.1; not a power artifact,
since an analysis-stratum effect there would have shown z near -7). In
fold B wallstreetbets is strongly segregated (z = -9.0), like every
other stratum. The registered subsampling control agrees: matched to
the analysis stratum document counts, wallstreetbets remains at chance
in fold A (z = -0.0) and segregated in fold B (z = -5.2), so neither
reading is a document-count artifact. A community-type moderator of segregation is therefore
not a stable property of these data. On its face the pattern is
regime-dependent (the same community at chance before 2020, segregated
after 2021), but that reading is post-hoc and confounded with the
folds' era and provenance differences, so we leave it as a described
observation. The registered, stable result is simpler: in the
post-regime fold, every stratum segregates.

A reproduction check accompanied the amended acquisition: the
analysis-stratum cells were recomputed on successive corpus rebuilds
and match (observed and eligible counts identical; z within the Monte
Carlo noise of the null estimate; build documents differ by one due to
deduplication order, disclosed in the released run log). A follow-up
study's independently acquired corpus (same platform, separate API pull
on a different day, shared unit rules) additionally reproduces the
first fold's wallstreetbets document census to within one document
(44,013 versus 44,012 author-quarters). Its registered confirmatory
run reproduces the second fold's endpoint under uniform single-source
provenance (all strata walled, formation null), so the second fold's
result is not a sourcing artifact.

### 6.4 Segregation as the object of study

Reading the result forward rather than as a failed prediction: the
persistence of suppressed-pair segregation is itself a measurable,
large, stable property of a discourse community, and plausibly varies
across communities, platforms, and time. A forum's "mixing deficit"
(observed joint attention over its shuffled expectation) is computable
with the machinery released here and may prove a more honest instrument
for studying how ideas spread, or fail to, than formation counts that
inherit the criterion trap. We offer it as the constructive replacement
for the discovery framing this paper set out to test.

The finding also supplies a measured mechanism to literatures that have
so far had to assume it. Models of segmented investor attention take
persistent, sticky attention boundaries as a premise: Merton's investor
recognition hypothesis prices assets partly by which investors are
aware of them; Hong and Stein derive momentum from information crossing
investor segments only slowly; and Cohen and Frazzini document returns
diffusing along economic links with a lag attributed to inattention to
connected firms. Our replication corpus is exactly such a setting, and
there the boundaries are directly visible: even analysis-oriented
finance communities co-mention economically adjacent tickers at less
than half chance rates, in both folds, on either side of a market
regime change. Similarly, the returns to brokerage across "structural
holes" (Burt) require that holes persist against the incentive to close
them; co-attention persistently below chance over two decades is
direct evidence of that persistence. We note one implication running the other
way: accounts in which new cross-domain narratives percolate upward
from public conversation sit uneasily with both the timing evidence of
Section 5 and the segregation result. Discourse data alone cannot
settle how narratives interact with prices, however.

## 7. Conclusion

We built the missing co-occurrence index for a twenty-year discourse
corpus and asked science's most romantic question of it: which of the
ideas that should have met will meet next? The answer, secured by a
positive control, a registered placebo that caught our own false
positive, a corrected permutation criterion, and a pre-registered
replication on a second platform with independent units, is none of
them, at rates distinguishable from error. The durable fact is the
opposite one. In open discourse, the expected-but-absent pairs are not
discoveries waiting to happen; they are walls that persist, decade
after decade, on every platform we measured. Instruments that
claim otherwise should first be pointed at shuffled data.

## Data and code availability

All pipeline code, evaluation harnesses, pre-registration files, and the
derived datasets (concept extraction cache, author-attribution table,
co-occurrence censuses, and per-run result files) are released at
https://github.com/talecK/antikythera (private during review; public at
publication), including the version-control history that timestamps
every registration ahead of its result. Raw Hacker News content is
public and retrievable via the official API; the release includes exact
pull specifications.

## Competing interests

This research originated in a commercial signal-research effort by the
author; the studied hypothesis failed its registered tests and no
product, trading activity, or financial position resulted or exists.
The author declares no other competing interests.

## Statement on AI assistance

Analysis code, evaluations, and manuscript drafting were performed with
a large-language-model assistant operating under the author's direction.
All experimental designs, thresholds, and interpretation rules were
pre-registered and committed before evaluation, by either party; the
version-control history documents the full sequence, including the
registered placebo that overturned an intermediate conclusion.

## References

- Swanson, D.R. (1986). Fish oil, Raynaud's syndrome, and undiscovered
  public knowledge. *Perspectives in Biology and Medicine* 30(1), 7-18.
  doi:10.1353/pbm.1986.0087
- Smalheiser, N.R., Swanson, D.R. (1998). Using ARROWSMITH: a
  computer-assisted approach to formulating and assessing scientific
  hypotheses. *Computer Methods and Programs in Biomedicine* 57(3),
  149-153. doi:10.1016/S0169-2607(98)00033-9
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
  *Proceedings of the 42nd International Conference on Machine Learning
  (ICML)*. arXiv:2405.14985.
- Aghajohari, M., Akhondzadeh, M.S., Ashkboos, S., Chitsaz, K. (2021).
  Degree-based feature is all you need: Science4Cast report. *IEEE
  International Conference on Big Data 2021*, 5791-5794.
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

---

## Figures (produced; files in reports/figures/, regenerated from the v2
## deterministic artifacts)

**Figure 1** (fig1.png/.pdf) — Observed versus shuffled. Top: the
placebo result (Section 5.2); histograms of formation counts across
100 label-shuffled replicates in the two author-space folds, with the
observed count as a vertical line far below the null distribution.
Bottom: the sub-chance totals (Section 5.4); observed co-mention over
eligible pairs as a fraction of the shuffled expectation in all four
space-fold cells, with null two-standard-deviation bands. Referenced
from Sections 5.2 and 5.4.

**Figure 2** (fig2.png/.pdf) — Formation rate by criterion. The
retired z-criterion rates versus the calibrated per-pair-permutation
rates in all four cells, log scale, against the one-percent
false-positive floor. The manufactured effect and its collapse in one
panel. Referenced from Section 5.3.

**Figure 3** (fig3.png/.pdf) — Registration protocol. Each
evaluation's registration commit and result commit on a common
timeline, from repository timestamps (asterisk: the positive control's
single joint commit, disclosed in Section 3.4; the subsequent
re-execution and post-review regeneration commits appear in the
repository history). Referenced from Section 3.4.

Tables 1-3 are set inline (census statistics in Section 3; calibrated
formation in Section 5.3; sub-chance totals in Section 5.4; the
replication table in Section 6.3 cites the released gate artifact).
