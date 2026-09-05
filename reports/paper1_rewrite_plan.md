# Paper 1: substantive manuscript rewrite plan

## Session handoff and intended task

The user reviewed Paper 1's position after its additional null-model tests,
agreed that significant parts of the manuscript need rewriting, and asked
for this plan to be saved for a new session. This session wrote the plan;
it did not execute the manuscript rewrite.

The next writing task is to reconstruct the argument from the completed
evidence while preserving the original PDF's accessible language and useful
narrative. This is a substantive scientific rewrite, not a sentence-level
polish or another appended robustness section.

Read the latest HANDOFF.md before starting: Paper 2 has separate operational
work whose status may have advanced. The operational banner below the
rewrite pointer was not reverified in this planning session. Do not infer
that an old RUNNING banner describes a currently active process.

## Diagnosis agreed with the user

The current manuscript combines two positions: the original argument treats
the discovery question as settled, whereas the new results support robust
aggregate separation and leave most individual-pair formation classifications
unresolved. Targeted corrections and added results have not yet been
integrated throughout the title, abstract, introduction, discussion and
conclusion.

The original narrative remains useful:

1. Expected-but-absent concepts looked like candidates for future connections.
2. An apparent author-level revival seemed to support this idea.
3. A registered placebo overturned that interpretation.
4. Persistent aggregate separation emerged as the durable positive finding.

Preserve this progression and the experimental reversals, but do not retain
unsupported certainty to preserve rhetorical force. No major defensible
result was identified as having been deleted in the comparison; the main
problem is incomplete integration of corrections and new evidence.

## Sources and comparison baseline

- Current manuscript: reports/paper1_draft.md.
- Preserved release PDF:
  data/release/preprints/quiring_2026_ideas_that_never_meet_preprint.pdf.
  It has 26 pages and matched the Downloads copy byte-for-byte during review.
  SHA256: 42329a78ac586b27fbbf0e93e1c54398cea0d01bcb2d3f1c2693743aa0d6def5.
- Pre-revision manuscript source: git show b8908f9:reports/paper1_draft.md.
  Use this as the concrete source comparison, not an assumed exact boundary
  between model authorship. The public remote PDF was not independently
  retrieved during this planning review.
- Current checkout at plan preparation: a8729e1; preserve later work if the
  next session starts from a newer state.
- Completed Paper 1 audit: reports/paper1_curveball_verification.json.
- Literal exact-margin prediction scores: reports/curveball_scores.json.
- Other amendment scores: reports/nulls_amendment_scores.json.
- Pooled thread estimates:
  reports/paper1_nulls_label_R100_thread_seeds10.json and corresponding TSVs.
- Quarter-stratified results: reports/paper1_nulls_stratified_R100.tsv.
- Raw recomputation record: reports/m3_incorporation_verification.json.
- Registrations: preregistration_nulls.md, preregistration_nulls_n2.md,
  preregistration_run8.md, preregistration_robustness.md,
  preregistration_gate.md and original run-specific registrations.
- Historical result record: reports/pilot1_runs.md and original artifacts
  cited by the manuscript's commit appendix.
- Figures/rendering: eval/make_paper_figs.py, eval/make_paper1_schematic.py,
  eval/render_paper_html.py, reports/figures/, reports/paper_polish_playbook.md.
- Existing work/paper1_revision.html is an intermediate, not a finished PDF.
- Read CLAUDE.md for repository rules. Historical "KILLED" summaries are not
  substitutes for the revised evidential distinctions below.

## Evidence boundaries already established

All eight Paper 1 aggregate evaluations (two spaces x two folds x N2/N3)
passed registered production diagnostics. The audit verified 104 transferred
files and recomputed raw moments, stage diagnostics and formation checks.

| Space | Fold | N2 observed/null | N3 observed/null | N3 z |
|---|---|---:|---:|---:|
| author | 1 | 0.6928 | 0.6937 | -10.21 |
| author | 2 | 0.6810 | 0.6834 | -8.37 |
| thread | 1 | 0.2468 | 0.2469 | -167.21 |
| thread | 2 | 0.2738 | 0.2739 | -124.24 |

N2 fixes binary document sizes and concept frequencies; N3 additionally
constrains margins within quarters. The central effect is approximately
31-32% below null expectation within authors' quarterly output and 73-75%
below expectation within threads. Lead with interpretable ratios/deficits.
Large z values are deviations in null-standard-deviation units, not Gaussian
tail probabilities and not population/generalization confidence intervals.

X-d passes under both nulls. X-e, the literal nominal-count prediction,
remains unresolved under both: seven of eight formation precision checks
are unresolved. Only N3 author fold 2 passes, with zero formed pairs.
Diagnostic uncertainty is neither a scientific failure nor evidence that
all flagged pairs are false. Aggregate validity and pair-level precision
must remain separate throughout the paper.

The original label shuffle preserves slot counts and label multiplicities
before repeated labels within documents collapse; it is not an exact binary
margin null. A nominal 99th-percentile criterion with discrete counts and
finite simulations does not establish an exact 1% false-positive rate.
Pair dependence invalidates treating the legacy binomial calculations as
calibrated inference. Preserve them as historical results where useful,
clearly marked; do not quietly erase registered outcomes.

The original placebo finding is still valuable: apparent 19-24% author-level
formation survived additional evaluations, but shuffled data produced more
formations. Scope the criticism to the implemented criterion unless broader
claims are supported by specific prior methods and evidence.

The Science4Cast positive control checks eligibility/ranking and related
pipeline functionality. Its outcome is edge appearance, different from the
discourse formation criterion. It cannot validate that criterion, certify
the concept extractor's errors, or support direct comparison of formation
rates across the two tasks.

The new exact-margin Paper 1 audit covers the four Hacker News cells. Do not
imply it also repeats every historical Reddit gate cell. Check the latest
verified companion results before retaining Paper 2 claims; unfinished
companion work need not block independent Paper 1 writing.

Separation relative to these nulls does not identify a causal mechanism.
Stable topical specialization can produce persistent separation among pairs
selected for earlier absence. Margins and quarter constraints do not control
all topical or audience structure. Co-occurrence is not a measurement of
discovery value, polarization, trading returns or the effectiveness of an
intervention. Different eligible universes also limit causal interpretations
of the author/thread contrast. Sequential prospective registrations informed
by earlier results are not globally outcome-blind independent replications.

## Rewrite sequence

### 1. Build a claim-to-evidence map before drafting

For each major claim, record its actual source, tested population/window,
outcome definition, null, registration timing, status and defensible wording.
Use supported, contradicted, unresolved or exploratory as appropriate.
Include aggregate separation, pair formation, rankers, placebo, positive
control, replication, novelty and downstream implications. This is the
working reference for all subsequent writing.

### 2. Write a plain-language outline

Proposed organizing question:

> When frequently discussed concepts have never appeared together, does that
> absence identify an opportunity for future connection, or a separation
> that persists?

Proposed evidence progression (verify exact ranking statements against their
own evaluations rather than making them consequences of the aggregate test):

- The attempted discovery approach did not establish useful predictive
  enrichment under the tested evaluations.
- A seemingly positive author-level formation signal failed its placebo.
- Aggregate separation survives stricter frequency, document-size and
  quarterly controls.
- Reliable identification of individual emerging connections remains a
  distinct, incompletely resolved question.

A candidate central conclusion is: "Concept pairs that were unexpectedly
absent together remain substantially underrepresented in later online
discussion, even after controlling document sizes, concept frequencies and
quarterly timing." Treat this as a writing proposal, not a required quote.

### 3. Rewrite Results, then Discussion

Integrate controls where they answer plausible alternative explanations.
For each test explain the question, result and implication; avoid organizing
the main text around execution chronology or prediction-code names.
Preserve the intellectual reversal and registration disclosures without
requiring readers to follow the complete lab notebook.

Discussion should explain what persists, what the nulls control, what they
do not explain, the limits of discovery inference, and useful applications
of the measurement. Reassess each original implication on its own evidence.

### 4. Rewrite Introduction, abstract and title

Write these after the Results/Discussion argument is coherent. Narrow claims
about LBD and prior art, foreground the strongest empirical result, and
avoid promises that require unresolved formation classifications.

Possible title direction: "Expected-but-absent concept pairs remain separated
in online discourse." This is optional; preserve accessibility and do not
choose a vague title merely to avoid making a clear supported claim.

### 5. Align figures, tables, Methods and supplement

Prioritize a display of observed/null ratios across nulls, spaces and folds;
keep provisional formation counts visibly distinct from established aggregate
results. Do not portray simulation variability as sampling uncertainty.

Consolidate null definitions and diagnostic requirements in Methods. Put
exhaustive historical tables, seed/batch details, machine transfers, hashes
and audit ledgers in supplementary material or linked reproducibility
records. Keep sufficient methodological information in the main article to
understand and assess the finding. Preserve original figures/artifacts;
create revision versions where needed.

### 6. Run two separate audits and render

- Evidence audit: every abstract claim, conclusion, table, caption and number
  agrees with its source and uses the same outcome definition and scope.
- Preservation audit against b8908f9 and the PDF: account for every substantive
  observation, explanation, disclosure and useful passage as retained,
  revised, moved or removed, with reasons for substantive removals.

Use the PDF skill for rendering/visual QA, and inspect the final full PDF.
Run applicable terminology/figure checks after edits. Do not claim a complete
rewrite or release-ready artifact while captions, appendix provenance or
layout still contradict the revised evidence.

## Known inconsistencies to resolve explicitly

- The concluding "none of them, at rates distinguishable from error" exceeds
  the revised pair-formation evidence.
- The old temporal limitation calls preservation future work; quarter-level
  controls are now complete. Finer within-quarter timing remains distinct.
- The Introduction acknowledges established fixed-margin methods while the
  Discussion still broadly says text-corpus practice has not adopted them.
- The discussion uses pre-articulation audience convergence as positive
  evidence, although that interpretation arose from the overturned formation
  signal. Retain historical context if useful, but reassess the implication.
- The "five lines of code" label-shuffle recommendation is not the same as
  exact-margin inference with diagnostics and reliable pair classification.
- Review all remaining "floor," "calibrated," "everywhere," "exactly at
  chance," "independent," and "no discoveries" wording for intended scope.
- Abstract, historical tables and captions need consistent distinctions
  between sum of pair-document counts and count of unique documents. The
  aggregate statistic sums co-occurrences over eligible pairs, so one document
  can contribute multiple times.

## Prior art found in this session

Bhattacharya and Srinivasan (2012), "A Semantic Approach to Involve Twitter
in LBD Efforts," mines biomedical semantic relationships from Twitter and
checks their presence in PubMed. This is not the present longitudinal test
of expected-but-absent pairs, but broad claims that LBD has never been applied
to online/non-scientific discourse need revision. Cite and distinguish it;
do not present a targeted search as exhaustive novelty verification.

- Author-hosted full text:
  https://homepage.cs.uiowa.edu/~psriniva/Papers/swlbd_2012.pdf
- Author publication listing confirming 2012 workshop context:
  https://homepage.cs.uiowa.edu/~psriniva/newsite/research-page.html
- Established Curveball/bipartite-null prior art already added to revision:
  https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0244363

## Scope, deliverables and completion criteria

This is manuscript work. Do not change frozen registrations, sampling code,
raw results or historical scientific outcomes to fit a preferred story.
No new large compute, Paper 1 formation-precision extension or FDR project
is part of this rewrite. Do not disturb another session's Paper 2 work.
No submission, preprint upload, outreach or absentia/H2 work is authorized
by this plan. Preserve the original release PDF.

Deliver:

1. A coherent revised reports/paper1_draft.md and aligned figures/captions,
   Methods and supplementary material as needed.
2. A rendered, visually checked review PDF, clearly distinguished from the
   already released preprint.
3. A concise change note, suggested path reports/paper1_rewrite_changes.md,
   recording strengthened, narrowed, withdrawn and unresolved claims and
   documenting substantive content moved or removed from the original.

Completion means a new reader encounters one consistent argument without
having to reconstruct the revision history. Scientific uncertainty must be
visible where it matters, while operational detail must not obscure the
finding. Do not stop at the claim map or outline when carrying out the rewrite;
those are intermediate steps toward the full manuscript and review artifact.
