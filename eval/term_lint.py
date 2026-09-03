#!/usr/bin/env python3
"""Term lint: every coined or hyphenated term in a draft must be accounted
for in reports/term_table.tsv, and every term the table marks REPLACE must
be gone. Run before every render; exits non-zero on any violation.

term_table.tsv columns (tab-separated, one term per row):
  term        lowercase, as it appears in prose (hyphenated compounds, watch
              words, or multi-word phrases)
  papers      1, 2, or 12
  class       S  standard term, keep as is
              D  ours, keep, must be defined at first use (checked by hand)
              Q  quoted registered label, keep where quoted
              R  replace; the lint fails if it is still present
  replacement plain-English replacement (for R and as guidance for D)
  note        evidence or reasoning, one line

What the lint checks mechanically:
  1. every hyphenated compound in the body text is in the table (any class
     but R)
  2. every watch word (eval/term_inventory.WATCH) in the body text is in
     the table
  3. every multi-word phrase listed in the table with class R is absent
  4. every table term with class D or Q that is absent from BOTH papers
     is reported as stale (warning, not failure)

Usage: term_lint.py [paper1|paper2|all]
"""
import csv
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from term_inventory import DRAFTS, WATCH, body_text, paragraphs, sentences, tokens  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TABLE = os.path.join(ROOT, "reports", "term_table.tsv")


def load_table():
    rows = {}
    with open(TABLE) as f:
        for r in csv.DictReader(f, delimiter="\t"):
            rows[r["term"].strip().lower()] = r
    return rows


def prose(paper):
    md = body_text(open(os.path.join(ROOT, DRAFTS[paper])).read())
    out = []
    for sec, para in paragraphs(md):
        for s in sentences(para):
            out.append((sec, s))
    return out


def main():
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    papers = sorted(DRAFTS) if which == "all" else [which]
    table = load_table()
    fails, warns = [], []
    present = set()

    for paper in papers:
        pid = paper[-1]
        for sec, sent in prose(paper):
            low_sent = " " + re.sub(r"\*\*|__|\*|`", "", sent).lower() + " "
            toks = [t.lower() for t in tokens(sent)]
            # 1. hyphenated compounds
            for t in toks:
                if "-" in t and len(t) > 3 and not t.endswith("-") and not re.fullmatch(r"[a-z]-?\d.*", t):
                    key = t[:-2] if t.endswith("'s") else t
                    present.add(key)
                    row = table.get(key) or table.get(t)
                    if row is None:
                        fails.append((paper, sec, f"unlisted compound '{t}'", sent))
                    elif row["class"] == "R":
                        fails.append((paper, sec, f"REPLACE still present '{t}' -> {row['replacement']}", sent))
            # 2. watch words
            for t in toks:
                if t in WATCH:
                    present.add(t)
                    row = table.get(t)
                    if row is None:
                        fails.append((paper, sec, f"unlisted watch word '{t}'", sent))
                    elif row["class"] == "R":
                        fails.append((paper, sec, f"REPLACE still present '{t}' -> {row['replacement']}", sent))
            # 3. multi-word R phrases
            for term, row in table.items():
                if " " in term and pid in row["papers"]:
                    if re.search(r"(?<![a-z])" + re.escape(term) + r"(?![a-z])", low_sent):
                        present.add(term)
                        if row["class"] == "R":
                            fails.append((paper, sec, f"REPLACE still present '{term}' -> {row['replacement']}", sent))

    # 4. stale D/Q entries
    if which == "all":
        for term, row in table.items():
            if row["class"] in ("D", "Q") and term not in present and " " in term:
                warns.append(f"stale table entry (not found in either paper): '{term}'")

    seen = set()
    for paper, sec, msg, sent in fails:
        k = (paper, msg)
        if k in seen:
            continue
        seen.add(k)
        print(f"FAIL {paper} [{sec}] {msg}\n     {sent[:160]}")
    for w in warns:
        print("WARN", w)
    print(f"{len(seen)} failures, {len(warns)} warnings")
    sys.exit(1 if seen else 0)


if __name__ == "__main__":
    main()
