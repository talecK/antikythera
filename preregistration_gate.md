# Variant gate registration — Reddit finance discourse (2026-08-30)

## STATUS: DRAFT — design frozen below; census numbers appended pre-eval.
(`eval/run_gate.py` refuses to run in eval mode until this line reads
"STATUS: REGISTERED".)

Question the gate answers: does financial discourse have the structure the
instrument needs? Specifically (Q1) do author-space suppressed ticker pairs
exist and form at a usable rate, and (Q2) does connection-seeking culture
close gaps faster than reactive culture — the first CONTROLLED test of the
mechanism story that runs 5/6 and Tier A built.

Calibration ladder from prior registered work (reports/tier_a.md,
reports/pilot1_runs.md): Science4Cast 67% / HN author-space ~20% (19.2%,
23.6%; exposed-vocabulary 23.1%) / HN thread-space 0.6%.

## Corpus and provenance (disclosed seams)
- Subreddits: DD stratum = SecurityAnalysis, ValueInvesting, StockMarket,
  stocks, investing. MEME stratum = wallstreetbets.
- Fold A data comes from the Arctic Shift API; fold B from the monthly
  Pushshift/Arctic-Shift dumps (torrent). Seam is ALIGNED WITH FOLDS, so it
  confounds A-vs-B comparisons but NOT the within-fold DD-vs-MEME test,
  which is the registered mechanism question.
- Dumps before 2023-04 are Pushshift collection, later months are Arctic
  Shift's own crawler; that seam sits inside fold B.
- Deleted/removed authors and AutoModerator are dropped; items appearing in
  both tracks are de-duplicated by item id.

## Units (frozen in pipeline/extract_tickers.py, committed 2026-08-30)
- PRIMARY LENS "union": $CASHTAG plus uppercase 2-5 letter bare symbols,
  both required to resolve in the SEC company_tickers table, bare symbols
  filtered by the committed STOPLIST (forum/finance jargon that is also a
  registered symbol: OP, IRS, DD, FCF, DRS, ATH, ...). Stoplist was built
  from an OUTCOME-BLIND audit of the top-100 bare hits on a 200K-item
  sample and is frozen as committed.
- SENSITIVITY LENS "cashtag": cashtags only (noise-free by construction).
  Outcome-blind smoke test shows this lens is ~10x sparser; if it yields no
  eligible pairs it is reported as UNINFORMATIVE, never as a negative.
- Index/vol ETFs (SPY, QQQ, VIX) are excluded as macro hubs, matching the
  run-6 finding that promiscuous nodes swamp suppressed-pair sets.
- Known bias: the SEC table lists CURRENT registrants, so symbols delisted
  before the snapshot are invisible (survivorship). This shrinks the
  universe; it does not bias whether an observed suppressed pair forms.

## Formulation (identical to registered runs 5/6, units swapped)
- Document = (author, calendar quarter); hub guard drops author-quarters
  with > 50 distinct tickers.
- Frequency floor F >= 20 distinct build-window author-docs per ticker
  (fallback F >= 10 ONLY if the outcome-blind census yields < 200 eligible
  pairs in a stratum; the choice is recorded below before eval).
- Eligible ("suppressed") pair: E_build = f_i * f_j / N_docs >= 2 AND zero
  observed build co-mentions.
- Formation: >= 2 eval author-docs co-mention AND >= 2 distinct authors AND
  eval-window z >= 2.

## Folds
- A: build 2017-01-01..2018-12-31, eval 2019 (pre-GME, pre-COVID).
- B: build 2022-01-01..2023-12-31, eval 2024 (post-GME regime).
- 2020-2021 excluded entirely: COVID + GME are regime breaks, and the
  project's own lesson is that folds must not straddle them.

## Registered readouts
1. **Q1 HEADLINE** — suppressed-pair formation rate, ALL stratum, union
   lens, both folds, with Wilson 95% CIs.
   - >= 10% in BOTH folds: financial discourse has the needed structure;
     the variant graduates to a funded registered run.
   - < 2% in BOTH folds: thread-like; the variant is DEAD and the project
     closes on a clean negative.
   - Otherwise: indeterminate; report, no interpretation stretch.
2. **Q2 MECHANISM (the controlled test)** — DD vs MEME formation rates
   within each fold. Registered prediction: DD > MEME.
   - Reported twice: raw, and with MEME author-quarters randomly
     subsampled (seed 20260830) to match the DD document count, because
     document count enters both E and z.
   - DD > MEME in both folds (non-overlapping CIs in at least one):
     mechanism story survives its first controlled test.
   - DD ~= MEME: the ~20% author-space rate is likely a generic property of
     dense forums, and run 5's result means less than claimed — a finding
     we commit to reporting as such.
   - MEME > DD: the instrument is a hype-propagation sensor, not an
     insight sensor; redirects the design, does not kill it.
3. **Q3 SCOUT (secondary, per the run-7 scope correction)** — run-7's
   split-half persistence test on ticker bridges, ALL stratum. Reported
   with the same overdispersion diagnostic; no pass/fail bar attached.
4. **Q4 HYGIENE** — duplicate/copypasta rate by stratum; WSB pre-2021
   (fold A) vs post-2021 (fold B) as a within-community mechanism-shift
   observation.

## Out of scope for the gate (belongs to the variant proper, if it opens)
- Any price or return analysis. The gate tests discourse structure only.
- Cross-validation against analyst co-coverage / EDGAR co-search peers
  (Ali-Hirshleifer 2020; Lee-Ma-Wang 2015) as economic ground truth — a
  designed follow-up, not part of this decision.

## Census (outcome-blind, appended before eval)
- [to be filled from `eval/run_gate.py --census` when acquisition completes]
