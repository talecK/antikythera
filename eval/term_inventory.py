#!/usr/bin/env python3
"""Mechanical term inventory for the paper drafts.

Pulls every candidate coined term from a draft's body text (Abstract
through Methods; tables, references, and the commit appendix excluded):

  1. hyphenated compounds            e.g. chance-calibrated, outcome-blind
  2. repeated 2- and 3-word phrases   e.g. mixing deficit, power artifact
     (lowercase content words only, stopwords excluded at the edges,
     occurring at least MIN_COUNT times)
  3. single words with a working-name feel, from a watch list

For each candidate: total count, first section, first sentence.

This is the candidate list, not the verdict. Classification (standard /
define / quoted registered label / replace) lives in
reports/term_table.tsv and is enforced by eval/term_lint.py.

Usage: term_inventory.py paper1 [--min-count 2] [--out path.tsv]
"""
import argparse
import collections
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DRAFTS = {"paper1": "reports/paper1_draft.md", "paper2": "reports/paper2_draft.md"}

STOP = set("""a an the of in on at to for from by with and or but as is are was were be been
being that this these those it its their our we they he she which who whom whose what
than then so if not no nor into onto over under between among across per via about
above below after before during within without through against toward towards up down
out off than such same other another each every all any some both either neither one two
three four five six ten first second third last next new old more most less least very
also only just even still yet here there where when while because since until unless
whether however therefore thus hence do does did done has have had having may might can
could should would will shall must""".split())

# Single words that read as ordinary English but carry a technical sense here.
WATCH = {"wall", "walled", "walls", "excursion", "anchor", "anchors", "cliff", "onset",
         "gate", "bar", "ladder", "lens", "stratum", "strata", "fold", "folds", "cell",
         "cells", "floor", "readout", "readouts", "instrument", "machinery", "suppressed",
         "eligible", "exposed", "formation", "formed", "forms", "segregation", "fusion",
         "mixing", "hub", "hubs", "seam", "regime", "window", "windows", "census",
         "placebo", "armored", "artifact", "artifacts", "deficit", "endpoint", "endpoints",
         "reversion", "reversions", "burst", "cascade", "scar", "substrate"}

SECTION_END = "## Data availability"


def body_text(md):
    if "## Abstract" in md:
        md = md[md.index("## Abstract"):]
    if SECTION_END in md:
        md = md[:md.index(SECTION_END)]
    return md


def paragraphs(md):
    """Yield (section, paragraph_text) for prose paragraphs only."""
    sec = "Abstract"
    for para in md.split("\n\n"):
        p = para.strip()
        if not p:
            continue
        if p.startswith("#"):
            sec = p.lstrip("# ").split("\n")[0].strip()
            continue
        if p.startswith("|") or p.startswith("**Table"):
            continue
        yield sec, " ".join(p.split())


def sentences(text):
    return re.split(r"(?<=[.!?])\s+(?=[A-Z(\"*])", text)


def tokens(text):
    text = re.sub(r"\*\*|__|\*|`", "", text)
    return re.findall(r"[A-Za-z][A-Za-z\-']*", text)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("paper", choices=sorted(DRAFTS))
    ap.add_argument("--min-count", type=int, default=2)
    ap.add_argument("--out", default=None)
    a = ap.parse_args()

    md = body_text(open(os.path.join(ROOT, DRAFTS[a.paper])).read())
    counts = collections.Counter()
    first = {}
    kind = {}

    def seen(term, k, sec, sent):
        counts[term] += 1
        if term not in first:
            first[term] = (sec, sent)
            kind[term] = k

    for sec, para in paragraphs(md):
        for sent in sentences(para):
            toks = tokens(sent)
            low = [t.lower() for t in toks]
            # 1. hyphenated compounds
            for t in low:
                if "-" in t and len(t) > 3 and not t.endswith("-") and not re.fullmatch(r"[a-z]-?\d.*", t):
                    seen(t, "hyphen", sec, sent)
            # 2. n-grams
            for n in (2, 3):
                for i in range(len(low) - n + 1):
                    g = low[i:i + n]
                    if g[0] in STOP or g[-1] in STOP:
                        continue
                    if any(len(w) < 3 for w in g):
                        continue
                    if any(re.search(r"\d", w) for w in g):
                        continue
                    seen(" ".join(g), f"{n}gram", sec, sent)
            # 3. watch words
            for t in low:
                if t in WATCH:
                    seen(t, "watch", sec, sent)

    rows = []
    for term, c in counts.items():
        k = kind[term]
        if k.endswith("gram") and c < a.min_count:
            continue
        sec, sent = first[term]
        rows.append((k, term, c, sec, sent))
    # drop 2-grams wholly contained in a kept 3-gram with the same count
    kept3 = {r[1] for r in rows if r[0] == "3gram"}
    rows = [r for r in rows if not (r[0] == "2gram" and any(r[1] in t3 and counts[t3] == r[2] for t3 in kept3))]
    rows.sort(key=lambda r: (r[0], -r[2], r[1]))

    out = a.out or os.path.join(ROOT, "reports", f"term_inventory_{a.paper}.tsv")
    with open(out, "w") as f:
        f.write("kind\tterm\tcount\tfirst_section\tfirst_sentence\n")
        for k, term, c, sec, sent in rows:
            f.write(f"{k}\t{term}\t{c}\t{sec}\t{sent[:220]}\n")
    by = collections.Counter(r[0] for r in rows)
    print(f"{a.paper}: {len(rows)} candidates ({dict(by)}) -> {out}")


if __name__ == "__main__":
    main()
