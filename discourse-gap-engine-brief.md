# Discourse Gap Engine — Project Brief (v2)

## Thesis
LLMs can't answer "tell me something nobody's talking about" because they sample the mode of human discourse. Science solved the equivalent problem: map which concepts co-occur in papers, then predict which never-connected pairs get connected next (literature-based discovery; Swanson 1986; Krenn & Zeilinger 2020 SemNet; Science4Cast benchmark, Nature MI 2023). This machinery has never been pointed at general discourse, because discourse lacks self-indexing (citations, discrete units). The project: build the missing index and run the complement query on everyday conversation.

## Core claim to falsify
High-affinity / negative-z co-occurrence edges (two ideas both frequent, semantically adjacent, never mentioned together) predict future edge formation better than baselines:
1. Random eligible pairs
2. Pure embedding-affinity ranking (no co-occurrence null)
3. Frequency-growth extrapolation

Metric: precision-at-k on 12-month edge formation. Rare-event regime; never accuracy.

## Key intellectual anchors
1. Uzzi & Jones 2013: hit papers = conventional core + one atypical combination. Valuable novelty = mostly-mode + one tail edge, not pure tail.
2. Literature-based discovery: gap prediction proven on scientific corpora (SemNet quantum physics; Science4Cast 143K AI papers / 64K concept nodes; Tshitoyan 2019 predicted thermoelectric materials years early).
3. Narrative-intelligence industry (Pulsar, PeakMetrics, etc.) built the corpus layer (500M posts/day, podcasts, 100+ languages) but only runs the forward query (what's spreading), never the complement.
4. Unclaimed territory = the corpus, not the predictor. Entire technical risk: does gap prediction survive noisy unitization (paraphrase soup) and a fast clock?

## Architecture
1. Corpus: free sources — HN (Firebase API / BigQuery public dataset, ~45M items, 30–50GB), Bluesky firehose, GDELT, Podcast Index + Whisper, YouTube captions. One vertical at a time.
2. Claim resolution (core IP): batch LLM extraction of discrete idea statements → embeddings → FAISS kNN + incremental clustering → LLM adjudication of borderline merges → registry of stable idea IDs (canonical phrasing, aliases, first-seen date).
3. Stats: per-doc idea-ID sets → pairwise co-occurrence in ClickHouse, exponential time decay (half-life in days) → z-score vs marginal-frequency null.
4. Amplification deconfounding v1: MinHash dedup, unique authors not posts, per-author caps, bot-cadence filtering.
5. Endpoints: score(claim) → frequency percentile + z. gaps(domain) → high-freq, high-affinity, deep-negative-z pairs ranked by (freq × affinity × |z|), LLM re-rank.

### Control plane vs data plane
- Control plane (Claude Code/agents): write pipeline, build gold set, orchestrate, adjudicate borderline merges (~50–100K calls), re-rank top-k gaps, eval analysis. High judgment, low volume.
- Data plane (pinned budget model, batch API): the 150M-token extraction conveyor belt. Never run bulk extraction through agent sessions: 20–50x cost, cap limits, and unpinned model versions = granularity drift mid-corpus.
- Design rule: extraction output is immutable, cached per (doc, extractor). Downstream stages re-derive cheaply; granularity iterations then cost hours, not a re-paid extraction day.

## Extraction model decision (Aug 2026)
- No formal bakeoff — prices collapsed the cost question. Instead: schema-hygiene smoke test (100 docs/candidate, drop sloppy JSON), then run Pilot 1 on 2–3 extractors in parallel (~$50 total). Cross-extractor agreement = robustness check on the paraphrase-noise risk (open question #2). If the result flips between extractors, the "signal" was a clustering artifact.
- Pre-register ONE extractor's registry as the primary result before looking at outcomes; others are robustness.
- Candidates + Pilot-1 cost (150M in / 30M out): Qwen3.7 Flash $0.03/$0.13 ≈ $8; Gemini Flash-Lite $0.10/$0.40 ≈ $14 batched; DeepSeek V4 Flash $0.14/$0.28 (cache $0.07) ≈ $25–29, flaky availability, needs fallback; Kimi K2.5 ~$0.3–0.6/$2–3 ≈ $100–170 (verify; heavy output price); Haiku 4.5 $1/$5, 50% batch ≈ $150 (quality anchor).
- Pinnability tiebreaker: DeepSeek/Qwen/K2 have open checkpoints (freeze forever via DeepInfra/Fireworks); Gemini/Haiku deprecate on vendor clock. Version drift mid-corpus = invisible confound in a longitudinal instrument.
- Ontology leakage: any 2026 extractor imports 2026 concepts into 2018 docs. Unavoidable; mitigate with ONE pinned extractor per registry so distortion is uniform, not time-varying.
- Endgame: distill a small open model (Qwen 8B + LoRA) from frontier labels once schema stabilizes.

## Experiment protocol (HN backtest)
- Filter: stories ≥5 points or ≥3 comments (~150K/yr). Document = title + top ~20 comments (edges form in comments).
- Pilot 0: titles-only, full archive (~$50 at old estimate, now trivial) — registry sanity only.
- Pilot 1: one fold, 2 build years + 1 eval year, comments included, 2–3 extractors in parallel.
- Full: 6–8 years, 3–4 non-overlapping folds. Total LLM spend on budget tier: $25–50.
- Leakage controls: embedding model must predate eval window; no lookahead anywhere; timestamped ingestion.
- Granularity is the make-or-break knob: too coarse = all edges exist; too fine = graph all zeros. Expect 3–5 registry rebuilds.

## Timing
- Pilot 0: one evening. Pilot 1 first pass: a weekend (2–3 days wall-clock, ~6h attention; extraction ≈ 1 day of batch queue, adjudication +1 day — the 2-batch chain is the floor).
- Pilot 1 converged (granularity tuned): 1–2 weeks part-time. Full multi-fold: +2–3 days on cached extractions.
- Whole experiment: ~a month of evenings. No hardware, no meaningful money.

## Scoreboards (three, decoupled — different mechanisms, success on one ≠ success on others)
1. Edge formation (PRIMARY; independent-author adoption; immune to viral one-offs). Log as primary from day one or the pipeline silently optimizes the wrong thesis.
2. Engagement (Reddit upvotes usable; X views measure the recommender; use as feature not eval; interventional version = post gap-derived content, measure lift).
3. Price (small/mid-cap equities; external reality check; harsh, noisy; precedent: Cohen & Frazzini economic-links lag).

## Niche ranking (buyer criterion removed)
1. HN/dev tooling — best archive, cleanest engagement, fastest eval. Run first regardless.
2. Small/mid-cap equities — all three scoreboards; tickers pre-resolve entities; requires point-in-time discipline.
3. Security/infosec — clean discourse; disclosure-embargo confound.
Eliminated: crypto (bots break independent-author counting), consumer health (no truth filter + ethics).
Generality claim requires 2 domains, same untouched pipeline.

## What it is / isn't
- Telescope: predict which idea-connections form next, months early.
- Foundry: hand gap edges to an LLM ("connect A to B") — manufactures the Uzzi-Jones signature on demand; fixes the original LLM-novelty failure via constraint.
- Predicts pre-discoveries in the adjacent possible (first of the Merton multiple-discoverers, systematically).
- Combinational only: cannot produce new conceptual primitives (Boden transformational).
- Truth/interestingness unguarded except where markets adjudicate.
- Reflexivity: publishing a gap closes it. Freeze a never-touched holdout set to keep the eval honest.

## Value capture (if signal real; decision variable = signal strength)
1. Trade it (strong + price-linked; track record is the asset)
2. License point-in-time feed to funds (after/instead of 1, never before)
3. Content foundry as own media portfolio (works if discourse-only)
4. SaaS telescope (worst: shovels vs Pulsar-class incumbents)
5. Floor: registry = OpenAlex-for-discourse, acquirable infrastructure
Personal use (one execution slot): detector as selection + timing instrument over existing idea backlog — build 6 months before the edge forms. Run privately = batch pipeline in cron, not a company.

## Decisions made
1. HN backtest first, before any product/niche commitment
2. Edge formation = primary eval; price/engagement secondary
3. No selling until signal strength known
4. Two-domain validation for generality
5. Crypto and health excluded
6. No formal bakeoff: smoke test + 2–3 parallel extractors, pre-registered primary
7. Control plane (Claude) / data plane (pinned batch model) split; never bulk-extract via agent sessions
8. Cache raw extractions immutably; iterate granularity downstream only

## Open questions
1. Optimal idea-ID granularity (the make-or-break knob)
2. Minimum claim-resolution quality before paraphrase noise drowns the null (now measured via cross-extractor agreement)
3. Eligible-pair spec (affinity threshold, frequency floor)
4. Time-decay half-life per corpus
5. Does Science4Cast's method zoo port directly, or does discourse need new features?

## Action items (ordered)
1. Create Claude Project; add this brief to project knowledge; paste "Decisions made" into project instructions
2. Pull HN BigQuery public dataset; export filtered slice (≥5 pts or ≥3 comments)
3. Claude Code: scaffold repo — ingestion, extraction prompt + JSON schema, cache layer keyed (doc, extractor), ClickHouse schema, eval harness with 3 baselines + precision-at-k
4. Draft extraction schema (claim statement format, granularity v1) + adjudication prompt
5. Schema-hygiene smoke test: 100 docs × candidates (Qwen3.7 Flash, DeepSeek V4 Flash, Gemini Flash-Lite, + Haiku anchor); drop sloppy JSON emitters
6. Pilot 0: titles-only pass, full archive; eyeball registry sanity
7. Pre-register: primary extractor, eligible-pair spec, k values, fold boundaries — write it down before running eval
8. Pilot 1: one fold, 2–3 extractors parallel; run eval vs baselines
9. Go/no-go: if precision-at-k beats baselines on primary AND survives cross-extractor check → full multi-fold run; else iterate granularity (max 3–5 rebuilds) or kill
10. If pass: freeze holdout gap set; decide second domain (equities vs infosec); revisit value-capture ranking with real signal strength
