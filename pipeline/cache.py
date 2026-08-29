"""Immutable extraction cache, keyed (doc_id, extractor_id).

Design rule (brief): extraction output is written once and never mutated;
downstream stages re-derive cheaply. extractor_id pins provider, model
version, prompt version, and schema version — any change is a NEW extractor_id
and a parallel cache namespace, never an overwrite.

Layout: data/extractions/{extractor_id}/{doc_id % 1000:03d}/{doc_id}.json
(shard dirs keep directory fan-out sane at millions of docs).
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.join(ROOT, "data", "extractions")


def _path(extractor_id: str, doc_id: int) -> str:
    return os.path.join(CACHE, extractor_id, f"{doc_id % 1000:03d}", f"{doc_id}.json")


def has(extractor_id: str, doc_id: int) -> bool:
    return os.path.exists(_path(extractor_id, doc_id))


def get(extractor_id: str, doc_id: int) -> dict | None:
    try:
        with open(_path(extractor_id, doc_id)) as f:
            return json.load(f)
    except FileNotFoundError:
        return None


def put(extractor_id: str, doc_id: int, extraction: dict) -> None:
    """Write once; refuse to overwrite (immutability guard)."""
    path = _path(extractor_id, doc_id)
    if os.path.exists(path):
        raise FileExistsError(
            f"extraction cache is immutable: {path} exists; "
            "a changed extractor needs a new extractor_id"
        )
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        json.dump(extraction, f, ensure_ascii=False, separators=(",", ":"))
    os.replace(tmp, path)


def missing(extractor_id: str, doc_ids: list[int]) -> list[int]:
    return [d for d in doc_ids if not has(extractor_id, d)]
