#!/usr/bin/env python3
"""Paper 2 data figures (reports/paper2_draft.md, Figures 2 to 4).

Fig 2: the transition and the excursion (WSB + DD primary z series,
       eligible-pair counts beneath each panel per the registered
       display rule).
Fig 3: the excursion placebo (per-replicate truth-null z vs real).
Fig 4: sensitivity (B=6/8 curves + cashtag lens with UNINFORMATIVE
       windows marked), pair counts beneath every z panel.

Inputs are committed artifacts only:
  reports/paper2_windows_z.tsv      (conforming run, 21a9dc7)
  reports/paper2_placebo_reps.tsv   (40 reps, from the 7bef4a2 run)
Outputs: reports/figures/p2_fig{1,2,3}.{png,pdf}  (file names unchanged
from v0.3; the draft numbers them Figures 2 to 4).
Style: eval/paper2_figstyle.py (shared with the Figure 1 schematic).
"""
import csv
import os
from collections import defaultdict

import matplotlib.pyplot as plt
import numpy as np

from paper2_figstyle import (BLUE, ORANGE, GREEN, RED, GREY, BAND, INK, MUTED,
                             MARKERS, FIG_W, ROOT, panel_label, save)


def titled(ax, title, legend=True, ncol=1):
    """Title alone above the axes; legend inside the empty upper right."""
    ax.set_title(title, loc="left")
    if legend:
        h, l = ax.get_legend_handles_labels()
        if h:
            ax.legend(h, l, loc="upper right", ncol=ncol, borderaxespad=0.4)


GS = dict(height_ratios=[2.4, 0.8, 0.5, 1.8, 0.8], hspace=0.25,
          left=0.11, right=0.99, top=0.95, bottom=0.06)

QUARTERS = [f"{y}Q{q}" for y in range(2020, 2025) for q in range(1, 5)][:19]
QIDX = {q: i for i, q in enumerate(QUARTERS)}
ONSET_X = QIDX["2021Q2"] - 0.5


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


def qaxis(ax, labels=True):
    ax.set_xticks(range(0, 19, 2))
    ax.set_xticklabels([QUARTERS[i].replace("20", "'", 1) for i in range(0, 19, 2)]
                       if labels else [])
    ax.set_xlim(-0.6, 18.6)


def reference_lines(ax, threshold=True):
    ax.axhspan(-3, 3, color=BAND, lw=0, label="|z| < 3, chance band", zorder=0)
    ax.axhline(0, color=GREY, lw=0.6, zorder=1)
    if threshold:
        ax.axhline(-5, color=GREY, lw=0.8, ls=(0, (4, 3)), label="z = -5, wall",
                   zorder=1)


def onset_line(ax, label_y=None, label=True):
    ax.axvline(ONSET_X, color=RED, lw=1, ls=(0, (1.5, 2.5)), zorder=2,
               label="onset 2021-04-01" if label else None)
    if label_y is not None:
        ax.text(ONSET_X + 0.25, label_y, "onset\n2021-04-01", color=RED,
                fontsize=7, va="center", ha="left", linespacing=1.1)


def series(ax, s, color, label=None, mfc=None):
    xs = [QIDX[d["eval_start"]] for d in s]
    ax.plot(xs, [d["z"] for d in s], "-", color=color, zorder=3)
    ax.plot(xs, [d["z"] for d in s], MARKERS[color], color=color,
            mfc=mfc or color, mec="white", mew=0.6, zorder=4, label=label)


def pair_panel(ax, s, color, offset=0.0, width=0.62, label=None,
               labels=True):
    xs = [QIDX[d["eval_start"]] + offset for d in s]
    ax.bar(xs, [d["n"] for d in s], width, color=color, alpha=0.45, lw=0,
           label=label)
    ax.set_ylabel("eligible\npairs")
    qaxis(ax, labels=labels)


def z_axes(fig, gs_top, gs_bottom):
    ax = fig.add_subplot(gs_top)
    axp = fig.add_subplot(gs_bottom, sharex=ax)
    ax.tick_params(labelbottom=False)
    return ax, axp


def fig1(W):
    """Figure 2 in the draft: transition and excursion."""
    wsb, dd = W[(4, "WSB", "union")], W[(4, "DD", "union")]
    fig = plt.figure(figsize=(FIG_W, 6.4))
    gs = fig.add_gridspec(5, 1, **GS)

    ax, axp = z_axes(fig, gs[0], gs[1])
    reference_lines(ax)
    onset_line(ax, label_y=16)
    series(ax, wsb, BLUE)
    for d in wsb:
        if d["z"] > 5:
            x = QIDX[d["eval_start"]]
            ax.plot([x], [d["z"]], MARKERS[BLUE], color=RED, mec="white",
                    mew=0.6, ms=5.5, zorder=5)
            ax.annotate(f"+{d['z']:.1f}", (x, d["z"]), xytext=(0, 7),
                        textcoords="offset points", ha="center", va="bottom",
                        fontsize=7.5, color=INK)
    ax.set_ylim(-14, 40)
    ax.set_ylabel("segregation z")
    panel_label(ax, "a")
    titled(ax, "r/wallstreetbets, treatment")
    qaxis(ax, labels=False)
    pair_panel(axp, wsb, BLUE, labels=False)

    ax, axp = z_axes(fig, gs[3], gs[4])
    reference_lines(ax)
    onset_line(ax, label_y=None, label=False)
    series(ax, dd, GREEN)
    ax.set_ylim(-18, 5)
    ax.set_ylabel("segregation z")
    panel_label(ax, "b")
    titled(ax, "DD control, five analysis-oriented subreddits", legend=False)
    qaxis(ax, labels=False)
    pair_panel(axp, dd, GREEN)

    fig.align_ylabels()
    return save(fig, "p2_fig1")


def fig2():
    """Figure 3 in the draft: the excursion placebo."""
    reps = defaultdict(list)
    with open(os.path.join(ROOT, "reports", "paper2_placebo_reps.tsv")) as f:
        for r in csv.DictReader(f, delimiter="\t"):
            reps[r["eval_start"]].append((float(r["z"]), int(r["formed"])))
    real = {"2020Q4": (28.6, 24), "2021Q1": (30.9, 61)}
    fig, axes = plt.subplots(1, 2, figsize=(FIG_W, 2.9), sharey=True,
                             gridspec_kw=dict(left=0.09, right=0.99, top=0.86,
                                              bottom=0.19, wspace=0.12))
    for ax, letter, (win, label) in zip(
            axes, "ab", [("2020Q4", "evaluation 2020Q4 to 2021Q1"),
                         ("2021Q1", "evaluation 2021Q1 to 2021Q2")]):
        zs = [z for z, _ in reps[win]]
        ax.hist(zs, bins=np.arange(-4, 4.5, 0.5), color=GREY, alpha=0.7, lw=0,
                edgecolor="white")
        rz, rf = real[win]
        ax.axvline(rz, color=RED, lw=1.6, zorder=3)
        ax.text(rz - 0.8, 6.3, f"real z = +{rz}\n{rf} pairs formed;\n"
                               f"placebo max {max(f for _, f in reps[win])}",
                ha="right", va="top", fontsize=7, color=INK, linespacing=1.15)
        ax.text(4.2, 6.3, "20 truth-null\nplacebo replicates", ha="left",
                va="top", fontsize=7, color=MUTED, linespacing=1.15)
        ax.set_xlim(-5, 34)
        ax.set_ylim(0, 6.6)
        ax.set_xticks([0, 10, 20, 30])
        ax.set_xlabel("segregation z")
        panel_label(ax, letter)
        titled(ax, label, legend=False)
    axes[0].set_ylabel("replicates")
    return save(fig, "p2_fig2")


def fig3(W):
    """Figure 4 in the draft: sensitivity."""
    fig = plt.figure(figsize=(FIG_W, 6.4))
    gs = fig.add_gridspec(5, 1, **GS)

    ax, axp = z_axes(fig, gs[0], gs[1])
    reference_lines(ax, threshold=False)
    ax.get_legend_handles_labels()
    onset_line(ax, label_y=None, label=False)
    for B, color in [(4, BLUE), (6, ORANGE), (8, GREEN)]:
        series(ax, W[(B, "WSB", "union")], color, label=f"B = {B}")
    ax.set_ylim(-16, 52)
    ax.set_ylabel("segregation z")
    panel_label(ax, "a")
    titled(ax, "window-length sensitivity, r/wallstreetbets, union lens")
    qaxis(ax, labels=False)
    for B, color, off in [(4, BLUE, -0.27), (6, ORANGE, 0.0), (8, GREEN, 0.27)]:
        pair_panel(axp, W[(B, "WSB", "union")], color, offset=off, width=0.25,
                   labels=False)

    ax, axp = z_axes(fig, gs[3], gs[4])
    s = W[(4, "WSB", "cashtag")]
    reference_lines(ax, threshold=False)
    onset_line(ax, label_y=None, label=False)
    xs = [QIDX[d["eval_start"]] for d in s]
    ax.plot(xs, [d["z"] for d in s], "-", color=BLUE, zorder=3)
    inf = [d for d in s if not d["uninf"]]
    uninf = [d for d in s if d["uninf"]]
    ax.plot([QIDX[d["eval_start"]] for d in inf], [d["z"] for d in inf],
            MARKERS[BLUE], color=BLUE, mec="white", mew=0.6, zorder=4,
            label="informative")
    ax.plot([QIDX[d["eval_start"]] for d in uninf], [d["z"] for d in uninf],
            MARKERS[BLUE], mfc="white", mec=GREY, mew=1.0, zorder=4,
            label="uninformative, under 20 eligible pairs")
    ax.set_ylim(-10, 8)
    ax.set_ylabel("segregation z")
    panel_label(ax, "b")
    titled(ax, "lens sensitivity, r/wallstreetbets, cashtag lens")
    qaxis(ax, labels=False)
    pair_panel(axp, s, BLUE)

    fig.align_ylabels()
    return save(fig, "p2_fig3")


if __name__ == "__main__":
    W = load_windows()
    for p in (fig1(W), fig2(), fig3(W)):
        print("wrote", p + ".{png,pdf}")
