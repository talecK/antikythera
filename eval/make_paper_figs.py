#!/usr/bin/env python3
"""Paper 1 data figures, on the shared style module (eval/paper2_figstyle.py)
so the two papers' figures read as one set.

Figure 2 (fig1.*): observed vs shuffled. (a, b) the placebo histograms
    (robustness R1, author space, both folds); (c) the pooled co-occurrence
    totals as a fraction of the shuffled expectation, all four cells (run 8).
Figure 3 (fig2.*): formation rate by criterion, all four cells.
Figure 4 (fig3.*): registration and result commit timeline.
File names are unchanged from the first draft (fig1-3); the paper numbers
them 2-4 because Figure 1 is the schematic (eval/make_paper1_schematic.py).

Inputs are the committed v2 deterministic artifacts:
    data/registry/run5_author/robustness_r1.json
    data/registry/run5_author/run8_author.json
    data/registry/pilot1_concepts/run8_thread.json
"""
import json
import os
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np

from paper2_figstyle import (BLUE, ORANGE, RED, GREY, BAND, INK, MUTED,
                             FIG_W, panel_label, save)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R1 = json.load(open(os.path.join(ROOT, "data/registry/run5_author/robustness_r1.json")))
R8A = json.load(open(os.path.join(ROOT, "data/registry/run5_author/run8_author.json")))
R8T = json.load(open(os.path.join(ROOT, "data/registry/pilot1_concepts/run8_thread.json")))

FOLDS = [("fold1", "fold 1 (evaluate 2017)"),
         ("fold2", "fold 2 (evaluate 2016)")]


def fig_observed_vs_shuffled():
    fig = plt.figure(figsize=(FIG_W, 5.6))
    gs = fig.add_gridspec(3, 2, height_ratios=[1, 0.42, 1.05],
                          hspace=0.0, wspace=0.28)
    for i, (fold, label) in enumerate(FOLDS):
        ax = fig.add_subplot(gs[0, i])
        d = R1[fold]
        ax.hist(d["null_counts"], bins=15, color=GREY, alpha=0.7)
        ax.axvline(d["observed"], color=RED, lw=1.5)
        ax.text(d["observed"] - 2, ax.get_ylim()[1] * 0.97,
                f"observed {d['observed']}", color=RED, ha="right",
                va="top", fontsize=7)
        ax.text(np.mean(d["null_counts"]), ax.get_ylim()[1] * 0.97,
                f"100 label shuffles\nmean {np.mean(d['null_counts']):.0f}",
                color=MUTED, ha="center", va="top", fontsize=7)
        ax.set_xlim(0, max(d["null_counts"]) * 1.15)
        ax.set_title(f"author space, {label}", loc="left")
        ax.set_xlabel("eligible pairs formed under the z-criterion")
        if i == 0:
            ax.set_ylabel("shuffle replicates")
        panel_label(ax, "ab"[i])

    ax = fig.add_subplot(gs[2, :])
    cells = [("author\nfold 1", R8A["fold1"]), ("author\nfold 2", R8A["fold2"]),
             ("thread\nfold 1", R8T["fold1"]), ("thread\nfold 2", R8T["fold2"])]
    xs = np.arange(len(cells))
    ratios = [c["obs_total"] / c["null_total_mean"] for _, c in cells]
    band = [2 * c["null_total_sd"] / c["null_total_mean"] for _, c in cells]
    ax.axhline(1.0, color=GREY, lw=0.8, ls="--")
    ax.errorbar(xs, [1.0] * 4, yerr=band, fmt="none", ecolor=GREY,
                capsize=4, lw=1, label="shuffled mean, plus or minus 2 sd")
    ax.bar(xs, ratios, 0.5, color=BLUE, label="observed / shuffled mean")
    for x, r, (_, c) in zip(xs, ratios, cells):
        ax.text(x, r + 0.04, f"z = {c['z_total']:.0f}", ha="center",
                fontsize=8, color=INK)
    ax.set_xticks(xs, [n for n, _ in cells])
    ax.set_ylim(0, 1.25)
    ax.set_ylabel("co-occurrence over eligible pairs,\nfraction of chance")
    ax.set_title("suppressed pairs co-occur below chance in every cell",
                 loc="left")
    ax.legend(loc="upper right", bbox_to_anchor=(1.0, 0.74))
    panel_label(ax, "c")
    return save(fig, "fig1")


def fig_rate_by_criterion():
    cells = ["author\nfold 1", "author\nfold 2", "thread\nfold 1", "thread\nfold 2"]
    zrate = [70 / 364, 26 / 110, 0.0060, 0.0068]
    crate = [2 / 364, 0.0, 22 / 25161, 12 / 7505]   # v2 deterministic rerun
    xs = np.arange(4)
    fig, ax = plt.subplots(figsize=(FIG_W * 0.72, 3.0))
    floor_plot = 0.03   # bottom of the log axis; a zero bar is drawn to it and labelled
    ax.bar(xs - 0.18, [r * 100 for r in zrate], 0.36, color=ORANGE,
           label="z-criterion (retired)")
    ax.bar(xs + 0.18, [max(r * 100, floor_plot) for r in crate], 0.36,
           color=BLUE, label="per-pair permutation criterion")
    for x, r in zip(xs, crate):
        if r == 0:
            ax.text(x + 0.18, floor_plot * 1.15, "0", ha="center",
                    va="bottom", fontsize=7, color=INK)
    ax.axhline(1.0, color=GREY, ls="--", lw=0.8)
    ax.text(3.55, 1.12, "1 percent false-positive floor", fontsize=7,
            color=MUTED, ha="right", va="bottom")
    ax.set_yscale("log")
    ax.set_ylim(floor_plot, 60)
    ax.set_ylabel("eligible pairs formed (percent)")
    ax.set_xticks(xs, cells)
    ax.set_title("formation rate by criterion", loc="left")
    ax.legend(loc="upper right", bbox_to_anchor=(1.0, 1.0))
    return save(fig, "fig2")


def fig_registration_timeline():
    events = [  # (registration commit, result commit, label)
        ("2026-08-29 18:33", "2026-08-29 18:48", "runs 1-2: units, first evaluation"),
        ("2026-08-29 18:56", "2026-08-29 19:45", "runs 3-4: suppressed pairs,\nexposed vocabulary (thesis closed)"),
        ("2026-08-29 23:00", "2026-08-29 23:00", "positive control* (Science4Cast)"),
        ("2026-08-29 23:08", "2026-08-29 23:10", "run 5: author space (19-24 percent)"),
        ("2026-08-29 23:33", "2026-08-29 23:35", "run 6: exposed pairs, author space (23 percent)"),
        ("2026-08-29 23:48", "2026-08-29 23:58", "run 7: bridging as a trait (not found)"),
        ("2026-08-30 13:19", "2026-08-30 13:28", "placebo and sensitivity checks:\nthe author-space rate fails"),
        ("2026-08-30 13:41", "2026-08-30 13:56", "run 8: permutation criterion\n(floor everywhere; z at or below -9)"),
    ]
    fig, ax = plt.subplots(figsize=(FIG_W, 3.4))
    t0 = datetime.fromisoformat("2026-08-29 18:00")
    for y, (reg, res, label) in enumerate(events):
        tr = (datetime.fromisoformat(reg) - t0).total_seconds() / 3600
        ts = (datetime.fromisoformat(res) - t0).total_seconds() / 3600
        yy = len(events) - y
        ax.plot([tr, ts], [yy, yy], color=GREY, lw=1)
        ax.plot(tr, yy, "o", mfc="white", mec=BLUE, ms=5, mew=1.0)
        ax.plot(ts, yy, "o", color=BLUE, ms=5, mec="white", mew=0.6)
        ax.text(ts + 0.35, yy, label, va="center", fontsize=7, color=INK)
    ax.plot([], [], "o", mfc="white", mec=BLUE, ms=5, label="registration committed")
    ax.plot([], [], "o", color=BLUE, ms=5, label="result committed")
    ax.set_yticks([])
    ax.spines["left"].set_visible(False)
    ax.set_xlabel("hours from the first registration (repository commit timestamps)")
    ax.set_xlim(-0.5, 33)
    ax.set_ylim(0.3, len(events) + 0.7)
    ax.set_title("every registration precedes its result "
                 "(*the control's single joint commit; re-executed later)",
                 loc="left")
    ax.legend(loc="lower left", bbox_to_anchor=(0.30, 0.04))
    return save(fig, "fig3")


if __name__ == "__main__":
    for f in (fig_observed_vs_shuffled, fig_rate_by_criterion,
              fig_registration_timeline):
        print("wrote", f() + ".{png,pdf}")
