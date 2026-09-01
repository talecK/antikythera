#!/usr/bin/env python3
"""Paper 2, Figure 1 (schematic): how the segregation statistic is built
and the three regimes it can express.

Purely illustrative. No panel is computed from data; every number shown
is a toy value chosen to make the construction legible. Real values live
in Figures 2-4 (eval/make_paper2_figs.py, from committed TSVs).

Output: reports/figures/p2_schematic.{png,pdf}
"""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle, FancyArrowPatch
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIG = os.path.join(ROOT, "reports", "figures")
os.makedirs(FIG, exist_ok=True)

plt.rcParams.update({"font.size": 8.5, "figure.dpi": 300})
BLUE, RED, GREY = "#3b6ea5", "#b0413e", "#8a8a8a"
GREEN, ORANGE, INK = "#3d8f5f", "#c98a2b", "#222222"


def off(ax, x0=0, x1=10, y0=0, y1=10):
    ax.set_xlim(x0, x1)
    ax.set_ylim(y0, y1)
    ax.set_aspect("equal")
    ax.axis("off")


def label(ax, letter, title):
    ax.text(0.0, 1.0, letter, transform=ax.transAxes, fontsize=10,
            fontweight="bold", va="bottom", ha="left")
    ax.text(0.09, 1.0, title, transform=ax.transAxes, fontsize=8.5,
            va="bottom", ha="left")


def chip(ax, x, y, text, fc, tc="white"):
    ax.add_patch(FancyBboxPatch((x, y), 1.05, 0.62,
                                boxstyle="round,pad=0.02,rounding_size=0.15",
                                fc=fc, ec="none"))
    ax.text(x + 0.525, y + 0.31, text, ha="center", va="center",
            fontsize=7.5, color=tc, fontweight="bold")


def card(ax, x, y, who, tickers, colors):
    ax.add_patch(FancyBboxPatch((x, y), 4.2, 1.9,
                                boxstyle="round,pad=0.05,rounding_size=0.25",
                                fc="#f4f4f4", ec=GREY, lw=0.8))
    ax.text(x + 0.25, y + 1.45, who, fontsize=7.5, color=INK, va="center")
    for i, (t, c) in enumerate(zip(tickers, colors)):
        chip(ax, x + 0.25 + i * 1.22, y + 0.3, t, c)


def panel_document(ax):
    """(a) the document: one author's tickers in one quarter."""
    off(ax, 0, 10, 0, 10)
    label(ax, "a", "The document: one author, one quarter")
    ax.text(0.3, 9.75, "one quarter, 2020Q2", fontsize=7.5, color=GREY,
            va="top")
    card(ax, 0.3, 7.2, "author 1", ["A", "B", "D"], [BLUE, ORANGE, GREY])
    card(ax, 5.3, 7.2, "author 2", ["B", "C"], [ORANGE, GREEN])
    card(ax, 0.3, 4.7, "author 3", ["A", "D"], [BLUE, GREY])
    card(ax, 5.3, 4.7, "author 4", ["C"], [GREEN])
    ax.text(5.0, 3.8, "...", ha="center", fontsize=10, color=GREY)
    ax.text(0.3, 2.9, "Every ticker an author mentions in a quarter,\n"
                      "across all posts and comments, is one document.\n"
                      "Two tickers co-mention when a document holds both.",
            fontsize=7.2, va="top", color=INK)


def dots_in_circle(ax, cx, cy, r, n, color, seed):
    rng = np.random.default_rng(seed)
    th = rng.uniform(0, 2 * np.pi, n)
    rr = r * 0.85 * np.sqrt(rng.uniform(0, 1, n))
    ax.plot(cx + rr * np.cos(th), cy + rr * np.sin(th), "o", ms=2.2,
            color=color, alpha=0.8, mec="none")


def panel_eligible(ax):
    """(b) an eligible (suppressed) pair in the build period."""
    off(ax, 0, 10, 0, 10)
    label(ax, "b", "An eligible pair: should have met, never did")
    for cx, c, t, s in [(2.4, BLUE, "A", 1), (7.6, ORANGE, "B", 2)]:
        ax.add_patch(Circle((cx, 6.1), 1.7, fc=c, ec=c, alpha=0.12, lw=0))
        ax.add_patch(Circle((cx, 6.1), 1.7, fc="none", ec=c, lw=1.2))
        dots_in_circle(ax, cx, 6.1, 1.7, 60, c, s)
        ax.text(cx, 8.2, f"documents\nmentioning {t}", ha="center",
                fontsize=7, color=c, linespacing=1.1)
    ax.text(5.0, 6.1, "0\nshared", ha="center", va="center", fontsize=8,
            color=RED, fontweight="bold")
    ax.text(0.3, 3.4, "Both tickers are frequent. Had authors picked\n"
                      "tickers independently, at least 2 build-period\n"
                      "documents would hold both. Observed: none.\n"
                      "The pair is eligible. Every window has dozens\n"
                      "to hundreds of such pairs.",
            fontsize=7.2, va="top", color=INK)


def panel_windows(ax):
    """(c) rolling windows: 4-quarter build, 2-quarter evaluation, step 1."""
    off(ax, 0, 10, 0, 10)
    label(ax, "c", "Rolling windows over 2019 to 2024")
    qs = [f"{y % 100}Q{q}" for y in range(2019, 2025) for q in range(1, 5)]
    n = len(qs)
    x0, x1 = 0.4, 9.6
    w = (x1 - x0) / n
    for i, q in enumerate(qs):
        ax.add_patch(FancyBboxPatch((x0 + i * w, 6.9), w * 0.92, 0.55,
                                    boxstyle="square,pad=0", fc="#eeeeee",
                                    ec="none"))
        if i % 4 == 0:
            ax.text(x0 + i * w + w * 0.46, 7.7, f"20{q[:2]}", ha="center",
                    fontsize=6.5, color=GREY)
    for k, (start, y) in enumerate([(0, 5.6), (1, 4.5), (2, 3.4)]):
        bx = x0 + start * w
        ax.add_patch(FancyBboxPatch((bx, y), 4 * w * 0.98, 0.7,
                                    boxstyle="square,pad=0", fc=BLUE,
                                    alpha=0.35, ec="none"))
        ax.add_patch(FancyBboxPatch((bx + 4 * w, y), 2 * w * 0.98, 0.7,
                                    boxstyle="square,pad=0", fc=RED,
                                    alpha=0.45, ec="none"))
        ax.text(bx - 0.15, y + 0.35, f"window {k + 1}", ha="right",
                va="center", fontsize=6.5, color=GREY)
    ax.text(x0, 6.5, "build: 4 quarters", ha="left", fontsize=7,
            color=BLUE, va="center")
    ax.text(x0 + 6 * w + 0.15, 5.95, "evaluate: 2 quarters", ha="left",
            fontsize=7, color=RED, va="center")
    ax.text(x0 + 8.2 * w + 0.15, 4.2, "... step 1 quarter,\n19 windows in all",
            fontsize=7, color=GREY, va="center")
    ax.text(0.4, 2.5, "Eligible pairs are found in the build period. The\n"
                      "statistic counts evaluation-period documents that\n"
                      "hold any eligible pair. Build length was chosen by\n"
                      "an outcome-blind census rule before any result.",
            fontsize=7.5, va="top", color=INK)


def panel_null(ax):
    """(d) the label-shuffle null and z."""
    off(ax, 0, 10, 0, 10)
    label(ax, "d", "The statistic: observed count against a shuffle null")
    rng = np.random.default_rng(7)
    null = rng.normal(480, 22, 100)
    bins = np.arange(400, 570, 10)
    h, edges = np.histogram(null, bins=bins)
    h = h / h.max() * 3.2
    for c, e in zip(h, edges[:-1]):
        ax.add_patch(FancyBboxPatch((1.0 + (e - 400) / 170 * 8.0, 3.2),
                                    8.0 / len(bins) * 0.9, c,
                                    boxstyle="square,pad=0", fc=GREY,
                                    alpha=0.6, ec="none"))
    ax.plot([1.0, 9.0], [3.2, 3.2], color=GREY, lw=0.8)
    obs_x = 1.0 + (525 - 400) / 170 * 8.0
    ax.plot([obs_x, obs_x], [3.2, 6.9], color=RED, lw=2)
    ax.text(obs_x + 0.15, 6.7, "observed", color=RED, fontsize=7.5, va="top")
    ax.text(3.6, 6.95, "100 shuffles of ticker labels\nacross documents",
            ha="center", fontsize=7, color=GREY, va="bottom")
    ax.text(1.0, 2.9, "fewer co-mentions", fontsize=6.5, color=GREY, va="top")
    ax.text(9.0, 2.9, "more", fontsize=6.5, color=GREY, va="top", ha="right")
    ax.text(0.4, 1.9, "z = (observed - shuffle mean) / shuffle sd.\n"
                      "z near 0: suppressed pairs meet as often as chance.\n"
                      "z far below 0: kept apart (a wall). z above 0: pushed\n"
                      "together. Each window's null uses its own documents.",
            fontsize=7.5, va="top", color=INK)


def regime(ax, cx, sep, title, ztxt, when, ca, cb):
    """two audiences drawn as circles, separation encodes the regime."""
    r = 1.15
    for dx, c, s in [(-sep, ca, 3), (sep, cb, 4)]:
        ax.add_patch(Circle((cx + dx, 5.6), r, fc=c, ec=c, alpha=0.12, lw=0))
        ax.add_patch(Circle((cx + dx, 5.6), r, fc="none", ec=c, lw=1.1))
        dots_in_circle(ax, cx + dx, 5.6, r, 28, c, s)
    ax.text(cx, 7.45, title, ha="center", fontsize=8, color=INK,
            fontweight="bold")
    ax.text(cx, 3.95, ztxt, ha="center", fontsize=8, color=INK)
    ax.text(cx, 3.25, when, ha="center", fontsize=7, color=GREY)


def panel_regimes(ax):
    """(e) the three regimes the statistic can express."""
    off(ax, 0, 30, 1.9, 8.5)
    label(ax, "e", "Three regimes, and the order r/wallstreetbets passed through them")
    regime(ax, 5.0, 1.15, "Chance-level mixing", "z near 0",
           "through 2020Q3", BLUE, ORANGE)
    regime(ax, 15.0, 0.35, "Fusion", "z far above 0",
           "the two GameStop windows", BLUE, ORANGE)
    regime(ax, 25.0, 1.75, "Walls", "z far below 0",
           "2021Q2 onward, no reversion", BLUE, ORANGE)
    for x in (9.6, 19.6):
        ax.add_patch(FancyArrowPatch((x, 5.6), (x + 0.8, 5.6),
                                     arrowstyle="-|>", mutation_scale=10,
                                     color=GREY, lw=1))
    ax.text(15.0, 2.35, "Audiences of two suppressed tickers, drawn as the "
                        "documents that mention each. Overlap is co-mention.",
            ha="center", fontsize=7, color=GREY)


def main():
    fig = plt.figure(figsize=(7.0, 7.6))
    gs = fig.add_gridspec(3, 2, height_ratios=[1, 1, 0.78], hspace=0.32,
                          wspace=0.12)
    panel_document(fig.add_subplot(gs[0, 0]))
    panel_eligible(fig.add_subplot(gs[0, 1]))
    panel_windows(fig.add_subplot(gs[1, 0]))
    panel_null(fig.add_subplot(gs[1, 1]))
    panel_regimes(fig.add_subplot(gs[2, :]))
    fig.savefig(os.path.join(FIG, "p2_schematic.png"), bbox_inches="tight")
    fig.savefig(os.path.join(FIG, "p2_schematic.pdf"), bbox_inches="tight")
    print("wrote", os.path.join(FIG, "p2_schematic.{png,pdf}"))


if __name__ == "__main__":
    main()
