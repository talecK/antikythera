# The gaps that don't close: idea segregation persists in twenty years of online discourse

**Author:** Kevin Quiring (independent researcher)

**Draft v0.1, 2026-08-30. Target shape: EPJ Data Science research article.
Gate section (Sec. 6.3 placeholder) pends the Reddit result.**

---

## Abstract

In science, pairs of concepts that frequently appear in the literature but
never together are strong candidates for future discovery: such
"suppressed" pairs later co-occur at high reported rates, and predicting
which pairs connect next is the basis of literature-based discovery. We ask
whether the same machinery applies to general online discourse, using 1.3
million Hacker News discussions spanning 2006 to 2026. Across four
pre-registered evaluations at two document granularities, we find no
predictive signal beyond generic popularity and triadic closure, a null we
certify with a positive control on the Science4Cast benchmark. We then
report a cautionary result. Re-defining the document as an author's
quarterly output produced suppressed-pair "formation" rates of 19 to 24
percent, thirty times the thread-level rate, an apparent revival that
survived two further pre-registered evaluations. A registered placebo test
showed the effect to be an artifact: the standard chance-calibrated
co-occurrence criterion is anti-conservative when document sizes are
heterogeneous, and a label-shuffled null "forms" more pairs than the real
data. Under a corrected per-pair permutation criterion, formation is
indistinguishable from the false-positive floor in every condition. The
real regularity runs in the opposite direction: suppressed pairs co-occur
substantially below chance (9 standard deviations below at the author
level, over 120 at the thread level). Idea communities in discourse do not
drift together; they stay apart. We release all code, data derivations,
and time-stamped pre-registrations.

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
et al. 2023), and word embeddings trained on materials-science abstracts
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
survived two further pre-registered evaluations before a placebo test,
registered with its failure condition stated in advance, revealed that
randomly shuffled data "forms" two to four times more pairs than the
real data. We describe the corrected criterion (a per-pair permutation
null) and suggest the shuffle as a mandatory control for co-occurrence
formation claims generally.

Third, a positive finding we did not seek. Under the corrected
criterion, suppressed pairs do not merely fail to connect. They
co-occur below chance, by 9 standard deviations at the author level
and by more than 120 at the thread level. The communities of attention
around two ideas that have never met tend to stay apart, at rates far
beyond what their sizes explain. In discourse, the gaps that
literature-based discovery hunts for do not close. They are actively
maintained.

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
graph approach on quantum-physics abstracts; the Science4Cast benchmark
(Krenn et al. 2023) turned it into a machine-learning competition on a
64,000-node concept graph, with link-prediction AUCs above 0.99 for the
best models. Tshitoyan et al. (2019) is the flagship prospective result.
Our study is, to our knowledge, the first application of this machinery
to non-scientific discourse, and our positive control reuses
Science4Cast directly.

**Novelty and recombination.** Uzzi, Mukherjee, Stringer and Jones
(2013) showed that high-impact papers combine a conventional core with a
small number of atypical journal pairings, and Foster, Rzhetsky and
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

**Null models for co-occurrence.** Our corrected formation criterion is
a permutation test in the tradition of degree-preserving null models
(Maslov and Sneppen 2002; Gotelli and Graves 1996). The specific failure
we document, chance-calibration against marginal frequencies while
document sizes are heterogeneous, is a bipartite version of the same
family of errors.

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
author's set of concepts within one calendar quarter; author-quarters
with more than 100 distinct concepts are excluded as hubs (a
sensitivity analysis without the guard is reported in the released
materials).

Within a **build window**, a concept is *frequent* if it appears in at
least 20 distinct documents. For frequent concepts i and j with document
frequencies f_i and f_j in N build documents, the pair is **eligible**
("suppressed") if its expected joint count E = f_i f_j / N is at least 2
while its observed build co-occurrence is zero: the pair should have
met, given how often each side is discussed, and has not.

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
committed to version control, and the evaluation code refuses to run
until the registration is in place. Outcome-blind quantities (document
counts, eligible-pair censuses) were appended to registrations before
outcomes were computed. The repository's commit history, released with
the paper, provides independent timestamps for the ordering of every
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
z-criterion only 0.60 and 0.68 percent of them form, and ranking within
the eligible set adds nothing: the only feature family that beats random
ordering is triadic closure (common neighbors), at precision-at-200
around 2.5 percent, roughly 4 times random, exactly the generic
network-science baseline that requires none of the discovery apparatus.
Semantic features (embedding affinity between concept labels) are
indistinguishable from random. Restricting to economically relevant
vocabulary (a registered classification of concepts into exposed versus
generic) leaves 8 formations per year in fold 1 and 1 in fold 2 across
the entire site.

### 4.2 The instrument finds the signal where it exists

A null of this kind is only as credible as its instrument, so we ran the
identical harness, unchanged, on the Science4Cast benchmark where the
signal is known to exist. It finds it: suppressed pairs in the science
corpus form at 67 percent under the same z-criterion (188 of 281
eligible pairs in a 10-million-pair sample), and ranked precision
reaches roughly 105 times random. Two observations from this control
matter later. First, in science as on Hacker News, popularity features
tie or beat closure and semantic features add nothing, consistent with
the degree-bias literature (Aiyappa et al. 2025). Second, the 67 percent
figure is produced by the same z-criterion we later found to be
miscalibrated; we return to this in Section 6.

## 5. The author-level revival and its correction

### 5.1 An apparent thirty-fold effect

Threads are rooms; ideas connect in people. On this reasoning we
re-defined the document as an author-quarter and re-ran the identical
formulation (registered before evaluation, as always). The structure of
the problem changed sharply: eligible suppressed pairs became rare (364
in fold 1, 110 in fold 2, versus tens of thousands in thread space),
resembling the science benchmark, and under the z-criterion they formed
at 19.2 and 23.6 percent, thirty times the thread-space rate. The effect
survived two further registered evaluations: it held at 23.1 percent on
economically relevant vocabulary (6 of 26 exposed pairs, against a
registered bar of 3), and a registered follow-up showed the formations
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
evaluation window's document slots, which preserves every document's
size and every concept's total frequency while destroying any real
association between concepts and people, and measure how many eligible
pairs "form" under the z-criterion in 100 such replicates. The
registration specified the failure condition in advance: a null mean at
or above half the observed count would be reported as a revision of the
result, not a nuance.

The placebo did not merely halve the result. Shuffled data forms more
pairs than the real data: 124.6 on average versus 70 observed in fold 1,
and 52.0 versus 26 in fold 2. The observed counts sit 6.1 and 5.3
standard deviations below their own mechanical nulls. The z-criterion's
internal expectation, built from marginal frequencies, does not account
for the fact that large documents generate joint occurrences
combinatorially; with heterogeneous document sizes, random assignment
clears z ≥ 2 constantly. The 19-to-24-percent rate was an artifact of
the measuring stick. Registered sensitivity analyses confirmed the
artifact lives in the criterion and nowhere else: the rate is stable
under monthly and half-yearly document windows (9.7 to 27.8 percent)
and under a conservative attribution lens that discards all
story-author credits (24.9 and 27.5 percent), yet all of these numbers
are equally below their own shuffled nulls.

### 5.3 Calibrated formation: nothing, anywhere

We then registered and ran the corrected criterion (per-pair permutation
null, Section 3.3) in both document spaces and both folds, with the
interpretation bars again frozen in advance. Formation collapses to the
false-positive floor everywhere:

| space | fold | eligible | formed | 1% floor | binomial p |
|-------|------|---------:|-------:|---------:|-----------:|
| author | 1 | 364 | 3 | 3.6 | 0.71 |
| author | 2 | 110 | 1 | 1.1 | 0.67 |
| thread | 1 | 25,161 | 20 | 251.6 | ~1 |
| thread | 2 | 7,505 | 11 | 75.0 | ~1 |

No cell shows formation above what a 1-percent-per-pair error rate
produces on its own. The handful of "formed" pairs are consistent with
noise, and we make no claims about them individually. At corpus scale,
on this platform, suppressed concept pairs do not connect above chance
at either granularity.

### 5.4 The gaps are held open

The same permutation machinery yields a second, better-powered
statistic: the total number of joint occurrences across all eligible
pairs, observed versus shuffled. Here the data speak loudly, in the
direction opposite to the discovery thesis:

| space | fold | observed total | null mean (sd) | z |
|-------|------|---------------:|---------------:|----:|
| author | 1 | 746 | 1,055 (33) | −9.2 |
| author | 2 | 454 | 651 (21) | −9.3 |
| thread | 1 | 12,098 | 48,373 (224) | −162 |
| thread | 2 | 7,866 | 28,230 (164) | −124 |

Suppressed pairs co-occur at roughly 70 percent of chance in author
space and roughly a quarter of chance in thread space. The registered
claim bar for this statistic (z ≤ −3 in both author folds) is met
overwhelmingly, in both spaces. The interpretation is simple and, we
believe, the paper's most durable finding: two concepts that have never
co-occurred, despite ample independent popularity, are not on their way
to meeting. Their audiences are substantially disjoint and remain so.
Discourse does not slowly mix; its communities of attention actively
fail to overlap, at magnitudes far beyond what topic sizes explain. The
suppressed pairs of literature-based discovery are, in discourse,
markers of persistent segregation rather than latent connection.

Descriptively, the segregation is strongest exactly where the discovery
framing would have looked for opportunity: in thread space, where a
single conversation would have to span both communities, mixing runs
four times below chance; in author space, where one person's quarterly
attention would have to span them, it runs at 70 percent of chance.
Individual minds cross community lines more readily than conversations
do, just not above chance.

## 6. Discussion

### 6.1 A criterion to retire

The z-style chance calibration we began with is not an exotic choice; it
is the natural first implementation of "co-occurs more than expected"
and variants of it appear throughout the co-occurrence, LBD, and trend
detection literatures. Our results show that with heterogeneous document
sizes it can manufacture large, stable, replication-surviving effects
from nothing. The 19-to-24-percent author-space rates passed three
pre-registered evaluations with frozen thresholds before the placebo
caught them. We suggest a label-shuffle placebo, five lines of code and
a few CPU-minutes, as a mandatory control wherever a formation or
emergence rate is computed from co-occurrence counts, and per-pair
permutation thresholds where the claim needs to survive it.

This has one immediate external consequence. Our positive control
reproduced the science-corpus regularity that suppressed pairs form at
67 percent, computed there, as everywhere before Section 5.2, with the
z-criterion. Scientific corpora also have heterogeneous document sizes.
Whether that celebrated number survives a calibrated re-measurement is
an open question, outside this paper's scope and under active
investigation.

### 6.2 What the negative does and does not say

The null is strong but scoped. It says: on a large general-technology
forum, over twenty years, with LLM-extracted concept units at two
granularities, expected-but-absent concept pairs show no above-chance
tendency to connect, and the previously reported positive versions of
this effect on the same data are measurement artifacts. It does not say
that no discourse corpus anywhere shows real gap-closing (a
structurally different corpus is tested in Section 6.3), nor that no
individual pair ever genuinely connects (our per-pair power is limited
by rarity), nor anything about scientific corpora except that their
headline rates deserve re-measurement.

Two limitations deserve emphasis. First, concept units come from a
language-model extraction; although the science control shows the
harness finds real signal through comparable unit noise, and a
registered robustness check shows the results are insensitive to the
attribution path, unit mushiness bounds how sharp any concept-level
claim can be. Second, author histories are truncated by the corpus
design (top-20 comments per thread), so author-space frequencies
undercount true activity; this shrinks the eligible universe but has no
evident mechanism for biasing formation direction.

### 6.3 A second platform [INTERIM — fold B pending; do not submit as is]

Whether these regularities are facts about one forum or about discourse
is testable, and a pre-registered replication is in progress on a
structurally different corpus: Reddit financial discussion (six
subreddits, 2017-2024), where the concept unit is the stock ticker,
regex-extracted and validated against the SEC registrant table rather
than produced by a language model. The design, criterion, folds, power
analysis, and interpretation bars were frozen and committed before any
outcome was computed, with two folds separated by the 2020-2021 market
regime break; conclusions are registered as requiring both folds, and
the first fold's results are therefore reported here as interim.

On the first fold (build 2017-2018, evaluation 2019; 14.6M items), both
headline patterns reproduce. Calibrated formation is null in every cell
(0-1 pairs formed against false-positive floors of 0.2-1.7; the
registered power analysis limits this to "no effect larger than roughly
4 percent," not "no effect"). And below-chance segregation replicates
almost exactly: across all six subreddits, suppressed ticker pairs
co-occur at z = -9.4 versus their shuffled null (341 observed joint
mentions against 555 expected), compared with z = -9.2 and -9.3 on
Hacker News, despite the change of platform, community, unit type, and
extraction method.

For the analysis-oriented stratum, whose source data was complete for
both folds ahead of the rest of the corpus, the second fold is already
final: in build 2022-2023 with evaluation 2024, on the far side of the
2020-2021 market regime break, suppressed pairs co-occur at z = -16.5
(358 observed against 824 expected, 43 percent of chance), with
calibrated formation again null (0 of 281 eligible pairs). In that
stratum the segregation result now stands in both folds on both
platforms: z = -9.2 and -9.3 on Hacker News, -10.0 and -16.5 on Reddit
finance. The effect did not merely survive the regime break; it is
larger after it.

One unregistered, exploratory observation deserves reporting with that
label attached. Splitting by community type, the segregation lives
entirely in the analysis-oriented subreddits (SecurityAnalysis,
ValueInvesting, and similar: z = -10.0, co-mention at 46 percent of
chance), while wallstreetbets sits exactly at chance (z = -0.2, 150
observed versus 152 expected) - and the difference is not a power
artifact, since at the analysis-stratum effect size the meme stratum
would show z near -7. Read plainly: communities organized around
argument keep their topics in lanes; a community organized around
attention co-mentions tickers at chance with respect to prior
structure. Whether this split survives the second fold, which sits on
the other side of the 2021 regime break, is exactly what the
registration will decide.

[FOLD B REMAINDER: wallstreetbets acquisition in progress (~14h). On
completion: the ALL-stratum registered headline cells, the fold-B test
of the exploratory stratum split, and a reproduction check on the
analysis-stratum numbers above (added data cannot enter that stratum;
any drift is an error signal). Section finalizes against the registered
bars then.]

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

## 7. Conclusion

We built the missing co-occurrence index for a twenty-year discourse
corpus and asked science's most romantic question of it: which of the
ideas that should have met will meet next? The answer, secured by a
positive control, a registered placebo that caught our own false
positive, and a corrected permutation criterion, is none of them, at
rates distinguishable from error. The durable fact is the opposite one.
In open discourse, the expected-but-absent pairs are not discoveries
waiting to happen; they are walls, quietly maintained, decade after
decade. Instruments that claim otherwise should first be pointed at
shuffled data.

## Data and code availability

All pipeline code, evaluation harnesses, pre-registration files, and the
derived datasets (concept extraction cache, author-attribution table,
co-occurrence censuses, and per-run result files) are released at
[REPOSITORY URL], including the version-control history that timestamps
every registration ahead of its result. Raw Hacker News content is
public and retrievable via the official API; the release includes exact
pull specifications.

## Statement on AI assistance

Analysis code, evaluations, and manuscript drafting were performed with
a large-language-model assistant operating under the author's direction.
All experimental designs, thresholds, and interpretation rules were
pre-registered and committed before evaluation, by either party; the
version-control history documents the full sequence, including the
registered placebo that overturned an intermediate conclusion.

## References (spine; DOIs marked [verify] to be confirmed at submission)

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
- Gotelli, N.J., Graves, G.R. (1996). *Null Models in Ecology*.
  Smithsonian Institution Press.

---

## Figure plan (to be produced)

1. **Fig. 1 (money figure): observed vs shuffled.** Four panels (space x
   fold): histogram of null formation counts across 100 replicates with
   the observed count as a vertical line far in the left tail; inset,
   the same for total co-mentions. One picture carries Sections 5.2-5.4.
2. **Fig. 2: the trap.** Schematic bipartite illustration: same marginal
   frequencies, homogeneous vs heterogeneous document sizes, why z >= 2
   fires under the latter; alongside, formation rate under z-criterion
   vs calibrated criterion in all four cells.
3. **Fig. 3: pipeline and protocol.** Corpus -> extraction -> attribution
   -> census -> registration -> eval, with commit timestamps for every
   registration/result pair (the reproducibility figure).
4. **Table 1:** corpus and census statistics per space/fold. **Table 2:**
   calibrated formation (Sec. 5.3). **Table 3:** sub-chance totals
   (Sec. 5.4).
