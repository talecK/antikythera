# Adversarial review — gate release (commits 500eb49..1386fc0 + 8df5b7b)

Reviewer: independent adversarial pass, 2026-08-31. No edits made; findings only.
Method: everything recomputable was recomputed from the committed code, the
registry JSONs, the run logs under `/Volumes/1TB NVME 1/antikythera/data/reddit_gate/`,
and the mentions parquet. Prose (registration narrative, run log, paper,
commit messages) was treated as claims, not evidence.

**Bottom line up front:** neither headline verdict flips. Q1 formation is null
under every recomputation and every bias found runs *toward* formation (so the
negative survives); Q1b ALL/union z is far below −3 in both folds under every
rerun. But the release has one fabricated empirical claim in the paper, a
non-deterministic harness whose "registered seed" does not pin any published
number, a "FINAL" results table that misreports the final run (including one
primary-outcome count), a registration-vs-code divergence on the unit rules,
and several "pre-outcome / outcome-blind" claims that the git timeline
contradicts in the strict sense. Not release-ready as committed.

---

## SEV-1 — would draw a correctness or integrity challenge in review

### 1.1 Paper §5.2 asserts shuffle-null results that were never computed
Claim (paper1_draft.md:329-334): the R2 window-sensitivity rates and the R4
attribution-lens rates are "equally below their own shuffled nulls."
Evidence against: `eval/run_robustness.py` computes a label-shuffle null in
`r1()` only. `r2()` (line 159) and `r4()` (line 228) compute z-criterion
formation rates and write `{eligible, formed, rate}` — no shuffle, no null.
No artifact in `data/registry/run5_author/` (robustness_r2.json, r4.json)
contains a null. The run log (pilot1_runs.md:179-193) claims only rate
stability for R2/R4 and explicitly notes elsewhere that extra shuffle nulls
were "out of registered scope." The sentence is plausible-but-unmeasured — in
the section of the paper whose whole point is that plausible co-occurrence
claims must be shuffle-tested. Fix: delete the clause or run the nulls.

### 1.2 The registered seed does not determine any published number; the harness is order-nondeterministic
`eval/run_gate.py:138-141` (and identically `run_eval8.py:129-133`) builds the
shuffle incidence list by iterating `edocs[d] & fs` — a Python set, whose
iteration order depends on the per-process hash seed. `rng.permutation` then
acts on that ordering, so with SHUFFLE_SEED=20260831 held fixed the *realized*
null still changes every run. Demonstrated directly (fold A DD/cashtag, same
data, same seed): PYTHONHASHSEED=1 → z=−2.73 (null 12.32, sd 3.05);
PYTHONHASHSEED=2 → z=−2.34 (null 12.60, sd 3.67); PYTHONHASHSEED=1 again →
identical to the first. A same-data rerun of fold B ALL/cashtag gave z=−10.53
vs the committed −9.85. Consequences:
- No z, p99, or formed count in run 8 or the gate is reproducible from the
  registration as written ("R = 100 ... seed 20260831" promises otherwise).
- With R=100 the null-sd estimate carries ~7% relative error, so |z|≈10 to 17
  values carry ±0.5–0.7 run-to-run noise. The run log's own "z −16.3 vs −16.5
  ... shuffle-simulation noise" and the paper's "z within shuffle-simulation
  noise" (paper1_draft.md:491) document the symptom without recognizing that a
  fixed-seed procedure should have none.
- Fix is one line (sort the incidence iteration, or set PYTHONHASHSEED), then
  one clean re-run to regenerate every quoted number.

### 1.3 The "VARIANT GATE — FINAL" table misreports the final run — including a formed count
The final run's own artifacts (`data/registry/gate_eval.json`, 02:21, and
`gate_final.log`) disagree with the FINAL table (pilot1_runs.md:324-337) on
five of six fold-A rows, which were carried over from the superseded 15:37
interim run (`gate_eval.log`):

| cell (fold A) | FINAL table says | final run actually produced |
|---|---|---|
| ALL/union   | z −9.4, null 555 | z −9.58, null 560.5 |
| ALL/cashtag | z −2.4, null 84  | z −2.54, null 84.7 |
| DD/union    | z −10.0, null 358| z −10.17, null 358.7 |
| DD/cashtag  | z −2.7, null 12  | z −2.55, null 12.9 |
| MEME/union  | **formed 1, p=.464**, z −0.2 | **formed 0, p=1**, z −0.19 |
| MEME/cashtag| z −1.4, null 45  | z −1.39, null 44.5 (this row alone IS the final run) |

The MEME/union row misstates a **Q1 primary outcome count** (1 vs 0) in the
official record; the table also mixes two runs without saying so. The paper
inherits the stale values: abstract and §6.3 quote z=−9.4 and "341 ... against
555 expected" (paper1_draft.md:36, 465-466) while the released registry
artifact says −9.58 / 560.5. A referee comparing the paper against
gate_eval.json will find the mismatch in minutes. (Fold-B rows all trace to
gate_eval.json correctly.) Root cause is finding 1.2: the author treated
run-to-run drift as noise and hand-assembled the table.

### 1.4 Registration-vs-code divergence on unit rules: the registered SPY/QQQ/VIX exclusion is not implemented for cashtags
preregistration_gate.md:67-68: "Index/vol ETFs (SPY, QQQ, VIX) are excluded as
macro hubs." Implementation (`pipeline/extract_tickers.py:139-145`): the
STOPLIST is applied to **bare** tokens only; the cashtag branch has no
stoplist check. Measured in the released parquet: **$SPY 16,838 mentions,
$QQQ 2,303** (VIX is absent only because it is not an SEC registrant — the
exclusion is vacuous for it). $BTC (543) and $ETH (108) also resolve (to
Grayscale Bitcoin Mini Trust and Ethan Allen), so the cashtag lens is not
"noise-free by construction" (preregistration_gate.md:64-66) and the settled
"crypto excluded" decision leaks. Materiality: SPY+QQQ are 4.2% of cashtag-lens
eval incidences in fold B (0.23% union), and **two eligible "suppressed" pairs
in the fold-B ALL/cashtag cell involve SPY or QQQ**, carrying 39 of that
cell's 138 observed co-mentions (28%). Rerunning that cell without SPY/QQQ:
eligible 192→190, obs 138→99, z −10.5→−10.8 — conclusion-preserving (slightly
more negative), but the registered spec and the shipped census are not the
same experiment, and the divergence is silent in both the run log and paper.

### 1.5 "Pre-outcome / outcome-blind" claims on the amendments are stronger than the git timeline supports
The FINAL header claims "amendments A1-A6', all committed pre-outcome"
(pilot1_runs.md:317-318); dae3a1c's A1–A5 header claims "Committed BEFORE any
WSB-dependent outcome is computed" (preregistration_gate.md:213-215). The
timeline in evidence:
- 15:37 (`gate_eval.log`, commit 9123b37): the gate ran **all 12 cells**. The
  partial fold-B WSB-dependent cells were computed and printed: ALL/union
  formed 2/441, p=0.935, z=−10.1 (obs 153 vs 358); ALL/cashtag z=−4.7; and
  the fold-A WSB cells (MEME/union z=−0.2) existed from this moment. Only the
  fold-B MEME cells were degenerate (eval docs 0). "Before any WSB-dependent
  outcome is computed" is strictly false; a defensible sentence would have
  been "before any *reportable* WSB eval-window outcome existed."
- 17:15 (b196a5c): the blanket "fold B not reportable" (committed 15:37) was
  selectively reversed **for the DD cells only, after seeing that DD
  replicated** (z=−16.5). That is exactly the choose-after-seeing behavior
  that A3 — written 100 minutes later (18:57) — prohibits. The stated basis,
  "DD is built ENTIRELY from the API pull" (pilot1_runs.md:283), is also
  factually wrong: `dump_filter.py` keeps all six subs, dumps are read first
  in `extract_tickers.iter_items`, so dump-era DD rows are dump-sourced —
  which is why DD build docs crept 122,813→122,815→122,816 across rebuilds.
  The paper repeats the false mechanism ("cannot receive data from the
  amended source," paper1_draft.md:488-489). Mitigation, honestly noted: the
  full-corpus rerun reproduced DD (obs/eligible identical), so the early call
  was validated post hoc.
- A3's majority-missing fallback ("DD-only fold B", preregistration_gate.md:
  254-256) was written when the author already knew DD fold-B replicated and
  fold-A WSB sat at chance. Had 2024 WSB proven unavailable, the "registered"
  procedure would have delivered a favorable DD-only replication while
  dropping the one stratum known to have shown no effect. It never triggered,
  but it was not chosen blind.
- A2 (mandatory eval-year equivalence check) → A2' (vacuous if eval year
  uniformly sourced, committed 2 minutes later) → A6 (eval year *made*
  uniformly sourced by decision) converted a registered mandatory measurement
  into vacuous satisfaction within five hours. No 2024 API-vs-anything overlap
  was ever measured, although A4 concedes per-month torrents exist for
  2024-04+ (using one as a *measurement*, not a corpus source, would not have
  created a third provenance class). The entire provenance case for the
  fold-B eval year rests on one build-era month (2023-03) — **comments only**:
  `provenance_check.py` reads `filtered_RC_*` and `/comments/search`
  exclusively; the RS/posts stream was never compared. Paper §6.3 presents
  this as "the two sources agree at 99.94 percent … the evaluation year is
  uniformly single-source" without the comments-only caveat or the fact that
  the registered eval-year check was amended away rather than performed.

---

## SEV-2 — would embarrass in review

### 2.1 Paper claims a released sensitivity analysis that does not exist
paper1_draft.md:183-185: hub-guard-free "sensitivity analysis … is reported in
the released materials." No `*noguard*` artifact exists (checked
`data/registry/run5_author/`; `grep -r noguard reports/` is empty). The
run-5 registration promised the same thing ("sensitivity WITHOUT the guard
reported alongside", preregistration_run5.md:33) and it was never delivered.
The `--noguard` flag exists in `run_eval5.py` but was apparently never run.

### 2.2 Registered Q2 readout silently not executed; dead seed in the harness
preregistration_gate.md:146-148 registers Q2 "reported twice: raw, and with
MEME author-quarters randomly subsampled (seed 20260830)." The subsampled
analysis exists nowhere; `run_gate.py:49` defines `SEED = 20260830` and never
uses it. The FINAL block's not-run disclosure (pilot1_runs.md:361-362) names
only Q3/Q4; the paper's disclosure (§6.3:455-456) likewise. The "Q2" label in
the FINAL readout was repurposed for the *unregistered* exploratory
segregation split.

### 2.3 The Q1b bar never names its cell, and the passing cell was chosen at reporting time
Q1b is registered "per fold and per stratum" with the bar "z <= -3 in both
folds" (preregistration_gate.md:129-143) — stratum/lens unspecified. Reported
against ALL/union it passes (−9.4/−17.6); read as "every stratum" it fails
(fold A MEME −0.2; three fold-A cashtag cells > −3). ALL/union is the
defensible primary by symmetry with Q1, but the registration should have
pinned it; as written, the "registered bar met" claim resolves an ambiguity
post hoc in the favorable direction. The paper's "Across all six subreddits …
z = −9.4" (§6.3) is the pooled cell doing that work (the split is disclosed
one paragraph later, to its credit).

### 2.4 Fold-B census and MDR were never appended to the registration; the paper calls the fold-B MDR "registered"
The registration promises fold-B census numbers and, if materially different,
a fold-B MDR "appended … reported the same way" (preregistration_gate.md:
123-127, 205-209). The registration still ends with the stale partial fold-B
census; the final fold-B census (487/281/213/192/44/141) exists only in
gate_eval.json, and the fold-B MDR (~2.1%) first appears in the FINAL block
after outcomes were known. It is a mechanical function of the outcome-blind
census, so nothing nefarious — but paper §6.3's "the registered power
analysis licenses 'no effect larger than 3.7 and 2.1 percent'" is wrong for
the second number, and paper §3.4's blanket "outcome-blind quantities were
appended to registrations before outcomes were computed" is contradicted by
the gate. (Arithmetic itself verified: see "What checks out.")

### 2.5 Corpus size misquoted in the paper
extract.log: `items 49207325 | mentions 4548804 | unique items 41519593`.
The 49.2M figure counts raw yielded rows including ~7.7M cross-track
duplicates, non-gate-sub crossposts, and deleted-author items that the
extractor then drops. The analyzed corpus is 41.5M unique items. Paper §6.3
says "49.2M items"; the abstract says "49 million Reddit finance posts" —
wrong count and wrong noun (items are overwhelmingly comments).

### 2.6 Survivorship note is wrong in the direction that matters, and phantom tickers backfill
preregistration_gate.md:69-71 claims the current-registrant SEC snapshot
"does not bias whether an observed suppressed pair forms." False: symbols
listing *during or after* the build window are mechanically un-co-mentionable
early (zero build co-mentions ⇒ auto-suppressed) and mechanically likely to
co-mention in eval. One of the two fold-B "formed" pairs is exactly this:
ARM (IPO 2023-09, inside build) × BBAI, obs 98 — and "ARM" is additionally an
English/architecture word admitted as a bare token corpus-wide because the
2026 SEC table resolves it. The bias inflates formation (anti-conservative
for Q1 — which still came out null, so the negative is safe) and pulls z_seg
toward zero (conservative for Q1b). The registration's reasoning, not the
conclusion, is wrong; the same backfill applies to every post-2019 listing
whose symbol collides with common uppercase tokens in fold A.

### 2.7 A1' full-month equivalence is not reproducible from the committed script
preregistration_gate.md:318 says "Reproduce: pipeline/provenance_check.py";
the committed script hard-codes the 3-day window (LO/HI = 2023-03-14..17) and
cannot produce the 940,021/940,410 full-month numbers. Also worth knowing:
the API-vs-dump deficit it measures (dump-only 389, API-only 0) is plausibly
the puller's own timestamp-cursor pagination (`before = min(created_utc)`
drops same-second boundary records) rather than archive coverage — direction
identical (sparser-never-denser, so the census-inflation defense stands), but
the amendment attributes it to the wrong mechanism.

### 2.8 Interim gate artifacts were overwritten
`run_gate.py` writes `gate_eval.json` unconditionally; the 15:37 interim run's
JSON (including its fold-A formed-pair identities) was destroyed by the final
run. Only `gate_eval.log` preserves the interim numbers. For a project whose
registration leans on immutable audit trails, eval outputs should be
timestamped, not clobbered — this is what made finding 1.3 possible.

---

## SEV-3 — cosmetic / wording

- 713 mention rows sit outside the fold windows (2016-12, 2021-12) — pull
  boundary slop, analytically inert (build/eval filters exclude them).
- The gate registration calls the formulation "identical to registered runs
  5/6, units swapped" while changing HUB_MAX 100→50 (disclosed two lines
  later, but "identical" is false).
- MDR convention (excess rate over the 1% floor) is never stated; a reviewer
  computing MDR@80 naively gets 4.6%, not 3.7%, and must reverse-engineer the
  convention (I did; it is consistent — see below).
- Paper §6.1/abstract count drift: "passed three pre-registered evaluations"
  vs "survived two further" — the 19-24% rate figured in runs 5 and 6; run 7
  failed its own bars and did not test the rate.
- Paper §6.3 still cites the 3-day 99.94% figure that A1' explicitly
  superseded with the stronger full-month 99.959%.
- `extract_tickers.py` dedups by bare item id without the t1/t3 kind prefix;
  comment and post id spaces cannot collide in these year ranges (different
  lengths/leading chars), but the key should include `kind`.
- Q1 "three unit types" counts the degenerate run-1 claims layer as a tested
  unit type; generous.
- HANDOFF.md still says the gate is "UNBLOCKED, still DRAFT" — stale.

---

## What checks out (recomputed or verified, no finding)

- **Every binomial p and floor in both gate tables and run 8**: exact match
  (e.g., P(X≥1|144,.01)=0.7648, P(X≥2|487,.01)=0.9557, P(X≥3|364,.01)=0.7057).
- **The registered power table and both quoted MDRs**, under the (unstated)
  excess-over-floor convention: k-needed 6/6/4/4 exact; MDR@80 4.64−1≈3.7%,
  fold-B 3.02−1≈2.1% — the paper's "3.7 and 2.1 percent" is arithmetically
  right and both are 80%-power figures.
- **Census determinism and honesty**: fold-A census reproduces exactly from
  the current parquet (169/1187/202268 …), the F-sweep reproduces exactly
  (169/184/187/187 — the fallback-not-invoked reasoning is sound), and
  fold-A census numbers were identical across the interim and final corpora.
- **z arithmetic** is internally consistent everywhere ((obs−mean)/sd matches
  every printed z in the JSONs and logs); the fold-B rows of the FINAL table
  trace to gate_eval.json exactly.
- **The interim "MEME would show ~70 vs 152 (z≈−7)" power counter-argument**
  recomputes correctly from the committed sd.
- **Acquisition integrity**: no month missing across both folds (74 mention-
  months, exactly the fold windows plus the 713 stray rows); the API-filled
  WSB 2023-04 shows smooth daily continuity with normal weekend dips (its
  ~22% month-level deficit vs neighbors reads as a genuine lull, not a pull
  hole); dedup is clean (0 duplicate (item_id,ticker) rows; 0 deleted/
  AutoModerator authors); the `.tmp` straggler in dump_filtered is not
  matched by the extractor's glob.
- **dump_filter.py two-format fix** is present, and `validate_month.py`'s
  differential regex-vs-json.loads preflight is a sound guard for exactly the
  bug class that bit (the crosspost over-inclusion is correctly re-filtered
  by the extractor's own-subreddit check).
- **run_gate vs registration** on: fold boundaries, E≥2 eligibility with
  zero build co-mention, F=20, hub guard at 50 on both windows, the
  formed-pair minima (>p99 strict, ≥2 docs, ≥2 distinct authors), the
  shared `binom_sf_ge` import, and the shuffle construction as registered
  (incidences restricted to the frequent set, within-doc duplicates
  collapsed). The descending-frequency early-break in eligible-pair
  enumeration is order-safe under ties.
- **Tier A numbers in paper §4.2** trace to reports/tier_a.md (0.785 vs
  0.0075 ≈ 105×; AUC 0.899 vs 0.851; 188/281 = 67%), and §4.2's
  ground-truth-vs-criterion correction is accurately stated.
- **Paper §5.3/§5.4 tables** match run-8 artifacts; §5.2's placebo numbers
  match R1; R2/R4 rates match their JSONs (the problem is only the
  invented "shuffled nulls" clause, finding 1.1).

---

## Verdict

Not release-ready, but close: nothing found moves either registered verdict —
formation stays null under every recomputation (and the biases found inflate,
not suppress, formation), and ALL/union segregation stays z ≪ −3 in both folds
under every rerun — yet the release currently contains one unsupported
empirical sentence, a results table that contradicts its own final artifact on
a primary count, and reproducibility/outcome-blindness language that the code
and git history do not back. Fix first: **(1)** make the harness deterministic
(sort the incidence iteration or pin PYTHONHASHSEED), re-run the gate once,
and regenerate every quoted number from that single artifact — this
simultaneously repairs the FINAL-table/paper mismatches (−9.4/555, formed
1-vs-0) and makes the registered seed mean something; **(2)** delete or
substantiate the two unsupported paper claims (§5.2 "below their own shuffled
nulls" for R2/R4; §3.3 released no-hub-guard sensitivity) and add the missing
disclosures (Q2 subsample not run; fold-B MDR computed post-census, not
registered); **(3)** reconcile the unit rules with the registration — either
stoplist cashtags for SPY/QQQ/BTC/ETH and re-run (cheap; the measured effect
is conclusion-preserving) or amend the registration text to what the code
does, and quantify it in the paper — and rewrite the outcome-blindness claims
in §6.3 and the FINAL header to the defensible version: interim fold-B cells
were computed but voided in advance, the DD exemption was decided post-hoc and
validated by reproduction, and the eval-year equivalence check was amended
into vacuity rather than performed.
