#!/usr/bin/env python3
"""Paper 2 figures (reports/paper2_draft.md figure plan).

Fig 1: the transition and the excursion (WSB + DD primary z series,
       eligible-pair counts beneath each panel per the registered
       display rule).
Fig 2: the excursion placebo (per-replicate truth-null z vs real).
Fig 3: sensitivity (B=6/8 curves + cashtag lens with UNINFORMATIVE
       windows marked), pair counts beneath every z panel.

Inputs are committed artifacts only:
  reports/paper2_windows_z.tsv      (conforming run, 21a9dc7)
  reports/paper2_placebo_reps.tsv   (40 reps, from the 7bef4a2 run)
Outputs: reports/figures/p2_fig{1,2,3}.{png,pdf}
"""
import csv
import os
from collections import defaultdict

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIG = os.path.join(ROOT, "reports", "figures")
os.makedirs(FIG, exist_ok=True)

plt.rcParams.update({"font.size": 9, "axes.spines.top": False,
                     "axes.spines.right": False, "figure.dpi": 300})
BLUE, RED, GREY = "#3b6ea5", "#b0413e", "#8a8a8a"
GREEN, ORANGE = "#3d8f5f", "#c98a2b"

QUARTERS = [f"{y}Q{q}" for y in range(2020, 2025) for q in range(1, 5)][:19]
QIDX = {q: i for i, q in enumerate(QUARTERS)}


def load_windows():
    rows = defaultdict(list)
    with open(os.path.join(ROOT, "reports", "paper2_windows_z.tsv")) as f:
        for r in csv.DictReader(f, delimiter="\t"):
            key = (int(r["B"]), r["stratum"], r["lens"])
            rows[key].append(dict(
                eval_start=r["eval_start"], z=float(r["z_seg"]),
                n=int(r["n_eligible"]), uninf=r["uninformative"] == "1"))
    for v in rows.values():
        v.sort(key=lambda d: QIDX[d["eval_start"]])
    return rows


def qlabels(ax):
    ax.set_xticks(range(0, 19, 2))
    ax.set_xticklabels([QUARTERS[i].replace("20", "'", 1) for i in range(0, 19, 2)],
                       fontsize=7.5)
    ax.set_xlim(-0.6, 18.6)


def z_panel(ax, series, color, title, onset=True):
    xs = [QIDX[d["eval_start"]] for d in series]
    zs = [d["z"] for d in series]
    ax.axhspan(-3, 3, color=GREY, alpha=0.18, lw=0, label="|z| < 3 (chance band)")
    ax.axhline(-5, color=GREY, lw=0.8, ls="--", label="z = -5")
    ax.axhline(0, color=GREY, lw=0.6)
    ax.plot(xs, zs, "-o", color=color, ms=3.5, lw=1.2)
    if onset:
        ax.axvline(QIDX["2021Q2"] - 0.5, color=RED, lw=1, ls=":")
        ax.text(QIDX["2021Q2"] - 0.35, ax.get_ylim()[1] * 0.55,
                "onset 2021-04-01", color=RED, fontsize=7.5, rotation=90,
                va="top")
    ax.set_title(title, fontsize=9)
    ax.set_ylabel("segregation z")
    qlabels(ax)


def pair_panel(ax, series, color):
    xs = [QIDX[d["eval_start"]] for d in series]
    ns = [d["n"] for d in series]
    ax.bar(xs, ns, 0.62, color=color, alpha=0.45)
    ax.set_ylabel("eligible\npairs", fontsize=7.5)
    ax.tick_params(labelsize=7)
    qlabels(ax)


def fig1(W):
    wsb, dd = W[(4, "WSB", "union")], W[(4, "DD", "union")]
    fig = plt.figure(figsize=(7.0, 6.4))
    gs = fig.add_gridspec(4, 1, height_ratios=[2.2, 0.7, 1.6, 0.7], hspace=0.55)

    ax = fig.add_subplot(gs[0])
    z_panel(ax, wsb, BLUE, "r/wallstreetbets (treatment), union lens, B = 4")
    for d in wsb:
        if d["z"] > 5:
            x = QIDX[d["eval_start"]]
            off = (-30, -2) if d["eval_start"] == "2020Q4" else (8, -2)
            ax.annotate(f"+{d['z']:.1f}", (x, d["z"]), textcoords="offset points",
                        xytext=off, fontsize=8, color=RED)
            ax.plot([x], [d["z"]], "o", color=RED, ms=4.5)
    ax.legend(fontsize=7, frameon=False, loc="upper right")
    pair_panel(fig.add_subplot(gs[1]), wsb, BLUE)

    ax = fig.add_subplot(gs[2])
    z_panel(ax, dd, GREEN, "DD control (five analysis subreddits), union lens, B = 4",
            onset=False)
    ax.axvline(QIDX["2021Q2"] - 0.5, color=RED, lw=1, ls=":")
    pair_panel(fig.add_subplot(gs[3]), dd, GREEN)

    fig.align_ylabels()
    fig.savefig(os.path.join(FIG, "p2_fig1.png"), bbox_inches="tight")
    fig.savefig(os.path.join(FIG, "p2_fig1.pdf"), bbox_inches="tight")
    plt.close(fig)


def fig2():
    reps = defaultdict(list)
    with open(os.path.join(ROOT, "reports", "paper2_placebo_reps.tsv")) as f:
        for r in csv.DictReader(f, delimiter="\t"):
            reps[r["eval_start"]].append((float(r["z"]), int(r["formed"])))
    real = {"2020Q4": (28.6, 24), "2021Q1": (30.9, 61)}
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 2.9), sharey=True)
    for ax, (win, label) in zip(axes, [("2020Q4", "eval 2020Q4-2021Q1"),
                                       ("2021Q1", "eval 2021Q1-2021Q2")]):
        zs = [z for z, _ in reps[win]]
        ax.hist(zs, bins=np.arange(-4, 5, 0.75), color=GREY, alpha=0.75,
                label="truth-null placebo (20 reps)")
        rz, rf = real[win]
        ax.axvline(rz, color=RED, lw=2)
        ax.annotate(f"real z = +{rz}\n({rf} pairs formed;\nplacebo max "
                    f"{max(f for _, f in reps[win])})",
                    (rz, 5.2), ha="right", fontsize=7.5, color=RED,
                    xytext=(-6, 0), textcoords="offset points")
        ax.set_xlim(-5, 34)
        ax.set_ylim(0, 6.5)
        ax.set_title(label, fontsize=9)
        ax.set_xlabel("segregation z")
    axes[0].set_ylabel("replicates")
    axes[0].legend(fontsize=7, frameon=False, loc="center")
    fig.savefig(os.path.join(FIG, "p2_fig2.png"), bbox_inches="tight")
    fig.savefig(os.path.join(FIG, "p2_fig2.pdf"), bbox_inches="tight")
    plt.close(fig)


def fig3(W):
    fig = plt.figure(figsize=(7.0, 6.4))
    gs = fig.add_gridspec(4, 1, height_ratios=[2.2, 0.7, 1.6, 0.7], hspace=0.55)

    ax = fig.add_subplot(gs[0])
    ax.axhspan(-3, 3, color=GREY, alpha=0.18, lw=0)
    ax.axhline(0, color=GREY, lw=0.6)
    for B, color in [(4, BLUE), (6, ORANGE), (8, GREEN)]:
        s = W[(B, "WSB", "union")]
        ax.plot([QIDX[d["eval_start"]] for d in s], [d["z"] for d in s],
                "-o", color=color, ms=3, lw=1.1, label=f"B = {B}")
    ax.axvline(QIDX["2021Q2"] - 0.5, color=RED, lw=1, ls=":")
    ax.set_title("window-length sensitivity: WSB union z at B = 4 / 6 / 8",
                 fontsize=9)
    ax.set_ylabel("segregation z")
    ax.legend(fontsize=7, frameon=False, loc="upper right")
    qlabels(ax)

    ax = fig.add_subplot(gs[1])
    for B, color, off in [(4, BLUE, -0.25), (6, ORANGE, 0.0), (8, GREEN, 0.25)]:
        s = W[(B, "WSB", "union")]
        ax.bar([QIDX[d["eval_start"]] + off for d in s], [d["n"] for d in s],
               0.24, color=color, alpha=0.55)
    ax.set_ylabel("eligible\npairs", fontsize=7.5)
    ax.tick_params(labelsize=7)
    qlabels(ax)

    ax = fig.add_subplot(gs[2])
    s = W[(4, "WSB", "cashtag")]
    ax.axhspan(-3, 3, color=GREY, alpha=0.18, lw=0)
    ax.axhline(0, color=GREY, lw=0.6)
    inf = [d for d in s if not d["uninf"]]
    uninf = [d for d in s if d["uninf"]]
    ax.plot([QIDX[d["eval_start"]] for d in s], [d["z"] for d in s],
            "-", color=BLUE, lw=0.9, alpha=0.5)
    ax.plot([QIDX[d["eval_start"]] for d in inf], [d["z"] for d in inf],
            "o", color=BLUE, ms=3.5, label="informative")
    ax.plot([QIDX[d["eval_start"]] for d in uninf], [d["z"] for d in uninf],
            "o", mfc="none", mec=GREY, ms=3.5,
            label="UNINFORMATIVE (< 20 eligible pairs)")
    ax.axvline(QIDX["2021Q2"] - 0.5, color=RED, lw=1, ls=":")
    ax.set_title("lens sensitivity: WSB cashtag z, B = 4", fontsize=9)
    ax.set_ylabel("segregation z")
    ax.legend(fontsize=7, frameon=False, loc="upper right")
    qlabels(ax)

    pair_panel(fig.add_subplot(gs[3]), s, BLUE)

    fig.align_ylabels()
    fig.savefig(os.path.join(FIG, "p2_fig3.png"), bbox_inches="tight")
    fig.savefig(os.path.join(FIG, "p2_fig3.pdf"), bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    W = load_windows()
    fig1(W)
    fig2()
    fig3(W)
    print("wrote", sorted(f for f in os.listdir(FIG) if f.startswith("p2_")))
