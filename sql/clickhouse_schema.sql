-- Local ClickHouse schema (co-occurrence store).
-- Registry versioning: every downstream row carries (extractor, registry_version)
-- so granularity rebuilds coexist without re-extraction (brief: cache raw
-- extractions immutably; iterate granularity downstream only).

CREATE DATABASE IF NOT EXISTS antikythera;

-- Resolved idea registry (one row per idea per registry build)
CREATE TABLE IF NOT EXISTS antikythera.idea_registry
(
    extractor        LowCardinality(String),
    registry_version LowCardinality(String),
    idea_id          UInt64,
    canonical        String,
    aliases          Array(String),
    first_seen       DateTime,
    n_instances      UInt32
)
ENGINE = ReplacingMergeTree
ORDER BY (extractor, registry_version, idea_id);

-- Doc -> idea incidence (the co-occurrence source of truth)
CREATE TABLE IF NOT EXISTS antikythera.doc_ideas
(
    extractor        LowCardinality(String),
    registry_version LowCardinality(String),
    doc_id           UInt64,
    doc_time         DateTime,
    idea_id          UInt64,
    authors          Array(String)   -- authors of the doc (story + comments); independent-author eval
)
ENGINE = ReplacingMergeTree
ORDER BY (extractor, registry_version, doc_id, idea_id);

-- Pair statistics are DERIVED per (build_window, half_life) at eval time via
-- queries over doc_ideas — not materialized as a base table, so eligible-pair
-- spec and decay half-life iterations never require re-ingestion.
