#!/usr/bin/env python3
"""Paper 1 figures (reports/paper1_draft.md figure plan).

Fig 1: observed vs shuffled (R1 histograms + sub-chance totals, run 8).
Fig 2: z-criterion vs calibrated formation rates, all four cells.
Fig 3: registration/result commit timeline (protocol figure).
Outputs: reports/figures/fig{1,2,3}.{png,pdf}
"""
import json
import os
from datetime import datetime

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIG = os.path.join(ROOT, "reports", "figures")
os.makedirs(FIG, exist_ok=True)
R1 = json.load(open(os.path.join(ROOT, "data/registry/run5_author/robustness_r1.json")))
R8A = json.load(open(os.path.join(ROOT, "data/registry/run5_author/run8_author.json")))
R8T = json.load(open(os.path.join(ROOT, "data/registry/pilot1_concepts/run8_thread.json")))

plt.rcParams.update({"font.size": 9, "axes.spines.top": False,
                     "axes.spines.right": False, "figure.dpi": 300})
BLUE, RED, GREY = "#3b6ea5", "#b0413e", "#8a8a8a"


def fig1():
    fig = plt.figure(figsize=(7.0, 4.6))
    gs = fig.add_gridspec(2, 2, height_ratios=[1, 1.05], hspace=0.55, wspace=0.3)
    for i, (fold, label) in enumerate([("fold1", "build 2015-16, eval 2017"),
                                       ("fold2", "build 2015, eval 2016")]):
        ax = fig.add_subplot(gs[0, i])
        d = R1[fold]
        ax.hist(d["null_counts"], bins=15, color=GREY, alpha=0.75,
                label="shuffled null (100 reps)")
        ax.axvline(d["observed"], color=RED, lw=2, label="observed")
        ax.set_xlim(0, max(d["null_counts"]) * 1.15)
        ax.set_title(f"author space, {label}\n"
                     f"observed {d['observed']} vs null mean {np.mean(d['null_counts']):.0f}",
                     fontsize=8.5)
        ax.set_xlabel("pairs formed (z-criterion)")
        if i == 0:
            ax.set_ylabel("replicates")
            ax.legend(fontsize=7, frameon=False)

    ax = fig.add_subplot(gs[1, :])
    cells = [("author\nfold 1", R8A["fold1"]), ("author\nfold 2", R8A["fold2"]),
             ("thread\nfold 1", R8T["fold1"]), ("thread\nfold 2", R8T["fold2"])]
    xs = np.arange(len(cells))
    ratios = [c["obs_total"] / c["null_total_mean"] for _, c in cells]
    band = [2 * c["null_total_sd"] / c["null_total_mean"] for _, c in cells]
    ax.axhline(1.0, color=GREY, lw=1, ls="--")
    ax.errorbar(xs, [1.0] * 4, yerr=band, fmt="none", ecolor=GREY,
                capsize=4, lw=1, label="null mean ±2 sd")
    ax.bar(xs, ratios, 0.5, color=BLUE, label="observed / null expectation")
    for x, r, (_, c) in zip(xs, ratios, cells):
        ax.text(x, r + 0.04, f"z = {c['z_total']:.0f}", ha="center", fontsize=8)
    ax.set_xticks(xs, [n for n, _ in cells])
    ax.set_ylim(0, 1.25)
    ax.set_ylabel("co-mentions over eligible pairs,\nfraction of chance")
    ax.set_title("suppressed pairs co-occur below chance in every condition",
                 fontsize=9)
    ax.legend(fontsize=7, frameon=False, loc="center right",
              bbox_to_anchor=(1.0, 0.55))
    fig.savefig(os.path.join(FIG, "fig1.png"), bbox_inches="tight")
    fig.savefig(os.path.join(FIG, "fig1.pdf"), bbox_inches="tight")
    plt.close(fig)


def fig2():
    # rate (%) under each criterion; calibrated floor = 1%
    cells = ["author f1", "author f2", "thread f1", "thread f2"]
    zrate = [70 / 364, 26 / 110, 0.0060, 0.0068]
    crate = [2 / 364, 1e-4, 22 / 25161, 12 / 7505]  # v2 deterministic rerun
    # (author f2 calibrated formed = 0; plotted at 1e-4 for log axis)
    xs = np.arange(4)
    fig, ax = plt.subplots(figsize=(5.2, 3.2))
    ax.bar(xs - 0.18, [r * 100 for r in zrate], 0.36, color=RED,
           label="z-criterion (retired)")
    ax.bar(xs + 0.18, [r * 100 for r in crate], 0.36, color=BLUE,
           label="calibrated (per-pair shuffle p99)")
    ax.axhline(1.0, color=GREY, ls="--", lw=1)
    ax.text(3.45, 1.08, "1% false-positive floor", fontsize=7, color=GREY,
            ha="right")
    ax.set_yscale("log")
    ax.set_ylim(0.03, 60)
    ax.set_ylabel("suppressed pairs formed (%)")
    ax.set_xticks(xs, cells)
    ax.set_title("formation rate by criterion: the z-criterion manufactures "
                 "the effect", fontsize=9)
    ax.legend(fontsize=7.5, frameon=False)
    fig.savefig(os.path.join(FIG, "fig2.png"), bbox_inches="tight")
    fig.savefig(os.path.join(FIG, "fig2.pdf"), bbox_inches="tight")
    plt.close(fig)


def fig3():
    events = [  # (reg dt, res dt, label)
        ("2026-08-29 18:33", "2026-08-29 18:48", "runs 1-2: units, first eval"),
        ("2026-08-29 18:56", "2026-08-29 19:45", "runs 3-4: suppressed pairs,\nexposure lens (KILL)"),
        ("2026-08-29 23:00", "2026-08-29 23:00", "Tier A: positive control*\n(Science4Cast)"),
        ("2026-08-29 23:08", "2026-08-29 23:10", "run 5: author space (19-24%)"),
        ("2026-08-29 23:33", "2026-08-29 23:35", "run 6: exposure x author (23%)"),
        ("2026-08-29 23:48", "2026-08-29 23:58", "run 7: scout class (FAIL)"),
        ("2026-08-30 13:19", "2026-08-30 13:28", "R1-R4: placebo FAILS the\nauthor-space result"),
        ("2026-08-30 13:41", "2026-08-30 13:56", "run 8: calibrated criterion\n(floor everywhere; z<=-9)"),
    ]
    fig, ax = plt.subplots(figsize=(7.0, 3.4))
    t0 = datetime.fromisoformat("2026-08-29 18:00")
    for y, (reg, res, label) in enumerate(events):
        tr = (datetime.fromisoformat(reg) - t0).total_seconds() / 3600
        ts = (datetime.fromisoformat(res) - t0).total_seconds() / 3600
        yy = len(events) - y
        ax.plot([tr, ts], [yy, yy], color=GREY, lw=1)
        ax.plot(tr, yy, "o", mfc="white", mec=BLUE, ms=6)
        ax.plot(ts, yy, "o", color=RED, ms=6)
        ax.text(ts + 0.35, yy, label, va="center", fontsize=7.5)
    ax.plot([], [], "o", mfc="white", mec=BLUE, label="registration committed")
    ax.plot([], [], "o", color=RED, label="result committed")
    ax.set_yticks([])
    ax.set_xlabel("hours from first registration (git commit timestamps)")
    ax.set_xlim(-0.5, 33)
    ax.set_title("registration precedes result in the commit history "
                 "(*Tier A: single joint commit)", fontsize=9)
    ax.legend(fontsize=7.5, frameon=False, loc="center left",
              bbox_to_anchor=(0.28, 0.16))
    fig.savefig(os.path.join(FIG, "fig3.png"), bbox_inches="tight")
    fig.savefig(os.path.join(FIG, "fig3.pdf"), bbox_inches="tight")
    plt.close(fig)


fig1(); fig2(); fig3()
print("figures written to", FIG)
