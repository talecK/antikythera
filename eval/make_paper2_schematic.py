#!/usr/bin/env python3
"""Paper 2, Figure 1 (schematic): how the segregation statistic is built
and the three regimes it can express.

Purely illustrative. No panel is computed from data; every number shown
is a toy value chosen to make the construction legible. Real values live
in Figures 2 to 4 (eval/make_paper2_figs.py, from committed TSVs).

Output: reports/figures/p2_schematic.{png,pdf}
Style: eval/paper2_figstyle.py (shared with the data figures).
"""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle, FancyArrowPatch
import numpy as np

from paper2_figstyle import (BLUE, ORANGE, GREEN, RED, GREY, BAND, INK, MUTED,
                             FIG_W, panel_label, save)

# every panel is drawn on a 10 x 10 canvas with a 0.5 margin on all sides
X0, X1, Y0, Y1 = 0.5, 9.5, 0.5, 9.5
BODY = 7.2       # body text size in panels
SMALL = 6.8      # secondary text size


def canvas(ax, letter, title, w=10, h=10, y0=0):
    ax.set_xlim(0, w)
    ax.set_ylim(y0, h)
    ax.set_aspect("equal")
    ax.axis("off")
    panel_label(ax, letter)
    ax.set_title(title, loc="left")


def body(ax, x, y, text, size=BODY, color=INK):
    ax.text(x, y, text, fontsize=size, va="top", ha="left", color=color,
            linespacing=1.25)


def chip(ax, x, y, text, fc):
    ax.add_patch(FancyBboxPatch((x, y), 1.0, 0.6,
                                boxstyle="round,pad=0.02,rounding_size=0.14",
                                fc=fc, ec="none"))
    ax.text(x + 0.5, y + 0.3, text, ha="center", va="center", fontsize=7,
            color="white", fontweight="bold")


def card(ax, x, y, who, tickers, colors):
    ax.add_patch(FancyBboxPatch((x, y), 4.0, 1.8,
                                boxstyle="round,pad=0.04,rounding_size=0.22",
                                fc="#f4f4f4", ec=GREY, lw=0.7))
    ax.text(x + 0.3, y + 1.35, who, fontsize=BODY, color=INK, va="center")
    for i, (t, c) in enumerate(zip(tickers, colors)):
        chip(ax, x + 0.3 + i * 1.18, y + 0.3, t, c)


def dots_in_circle(ax, cx, cy, r, n, color, seed):
    rng = np.random.default_rng(seed)
    th = rng.uniform(0, 2 * np.pi, n)
    rr = r * 0.85 * np.sqrt(rng.uniform(0, 1, n))
    ax.plot(cx + rr * np.cos(th), cy + rr * np.sin(th), "o", ms=2.0,
            color=color, alpha=0.8, mec="none")


def audience(ax, cx, cy, r, color, seed, n=60):
    ax.add_patch(Circle((cx, cy), r, fc=color, ec=color, alpha=0.12, lw=0))
    ax.add_patch(Circle((cx, cy), r, fc="none", ec=color, lw=1.1))
    dots_in_circle(ax, cx, cy, r, n, color, seed)


def panel_document(ax):
    canvas(ax, "a", "The document: one author, one quarter", y0=1.6)
    ax.text(X0, Y1, "one quarter, 2020Q2", fontsize=SMALL, color=MUTED,
            va="top")
    card(ax, X0, 6.9, "author 1", ["A", "B", "D"], [BLUE, ORANGE, GREY])
    card(ax, 5.3, 6.9, "author 2", ["B", "C"], [ORANGE, GREEN])
    card(ax, X0, 4.6, "author 3", ["A", "D"], [BLUE, GREY])
    card(ax, 5.3, 4.6, "author 4", ["C"], [GREEN])
    ax.text(5.0, 3.85, "...", ha="center", va="center", fontsize=9, color=GREY)
    body(ax, X0, 3.1, "Every ticker an author mentions in a quarter,\n"
                      "across all posts and comments, is one document.\n"
                      "Two tickers co-mention when a document holds both.")


def panel_eligible(ax):
    canvas(ax, "b", "An eligible pair: should have met, never did", y0=1.6)
    audience(ax, 2.3, 6.6, 1.6, BLUE, 1)
    audience(ax, 7.7, 6.6, 1.6, ORANGE, 2)
    ax.text(2.3, 8.45, "documents\nmentioning A", ha="center", va="bottom",
            fontsize=SMALL, color=BLUE, linespacing=1.1)
    ax.text(7.7, 8.45, "documents\nmentioning B", ha="center", va="bottom",
            fontsize=SMALL, color=ORANGE, linespacing=1.1)
    ax.text(5.0, 6.6, "0\nshared", ha="center", va="center", fontsize=7.5,
            color=RED, fontweight="bold", linespacing=1.1)
    body(ax, X0, 4.4, "Both tickers are frequent. Had authors picked\n"
                      "tickers independently, at least 2 build-period\n"
                      "documents would hold both. Observed: none.\n"
                      "The pair is eligible. Every window has dozens\n"
                      "to hundreds of such pairs.")


def panel_windows(ax):
    canvas(ax, "c", "Rolling windows over 2019 to 2024", y0=1.6)
    n = 24
    w = (X1 - X0) / n
    for i in range(n):
        ax.add_patch(FancyBboxPatch((X0 + i * w, 8.2), w * 0.9, 0.5,
                                    boxstyle="square,pad=0", fc=BAND,
                                    ec="none"))
        if i % 4 == 0:
            ax.text(X0 + i * w + w * 0.45, 8.95, str(2019 + i // 4),
                    ha="center", va="bottom", fontsize=SMALL, color=MUTED)
    for k, (start, y) in enumerate([(0, 7.0), (1, 6.0), (2, 5.0)]):
        bx = X0 + start * w
        ax.add_patch(FancyBboxPatch((bx, y), 4 * w * 0.97, 0.7,
                                    boxstyle="square,pad=0", fc=BLUE,
                                    alpha=0.35, ec="none"))
        ax.add_patch(FancyBboxPatch((bx + 4 * w, y), 2 * w * 0.97, 0.7,
                                    boxstyle="square,pad=0", fc=RED,
                                    alpha=0.40, ec="none"))
        ax.text(bx + 6 * w + 0.2, y + 0.35,
                f"window {k + 1}", ha="left",
                va="center", fontsize=SMALL, color=MUTED)
    lx = 6.3
    for y, fc, a, txt in [(7.35, BLUE, 0.35, "build, 4 quarters"),
                          (6.35, RED, 0.40, "evaluate, 2 quarters")]:
        ax.add_patch(FancyBboxPatch((lx, y - 0.18), 0.45, 0.36,
                                    boxstyle="square,pad=0", fc=fc, alpha=a,
                                    ec="none"))
        ax.text(lx + 0.6, y, txt, ha="left", va="center", fontsize=SMALL,
                color=INK)
    ax.text(lx, 5.35, "step 1 quarter, 19 windows", ha="left", va="center",
            fontsize=SMALL, color=MUTED)
    body(ax, X0, 3.9, "Eligible pairs are found in the build period. The\n"
                      "statistic counts evaluation-period documents that\n"
                      "hold any eligible pair. Build length was chosen by\n"
                      "an outcome-blind census rule before any result.")


def panel_null(ax):
    canvas(ax, "d", "The statistic: observed count against a shuffle null",
           y0=1.6)
    rng = np.random.default_rng(7)
    null = rng.normal(480, 22, 100)
    bins = np.arange(400, 570, 10)
    h, edges = np.histogram(null, bins=bins)
    h = h / h.max() * 2.6
    base, left, span = 5.4, X0 + 0.6, 7.6
    for c, e in zip(h, edges[:-1]):
        ax.add_patch(FancyBboxPatch((left + (e - 400) / 170 * span, base),
                                    span / len(bins) * 0.88, c,
                                    boxstyle="square,pad=0", fc=GREY,
                                    alpha=0.6, ec="none"))
    ax.plot([left, left + span], [base, base], color=MUTED, lw=0.6)
    obs_x = left + (525 - 400) / 170 * span
    ax.plot([obs_x, obs_x], [base, base + 3.2], color=RED, lw=1.6)
    ax.text(obs_x + 0.15, base + 3.1, "observed", color=RED, fontsize=SMALL,
            va="top")
    ax.text(left + span * 0.42, base + 3.4, "100 shuffles of ticker labels",
            ha="center", va="bottom", fontsize=SMALL, color=MUTED)
    ax.text(left, base - 0.15, "fewer co-mentions", fontsize=SMALL,
            color=MUTED, va="top")
    ax.text(left + span, base - 0.15, "more", fontsize=SMALL, color=MUTED,
            va="top", ha="right")
    body(ax, X0, 3.9, "z = (observed - shuffle mean) / shuffle sd.\n"
                      "z near 0: suppressed pairs meet as often as chance.\n"
                      "z far below 0: kept apart, a wall. z above 0:\n"
                      "pushed together. Each window has its own null.")


def regime(ax, cx, sep, title, ztxt, when):
    r = 1.15
    audience(ax, cx - sep, 5.4, r, BLUE, 3, n=28)
    audience(ax, cx + sep, 5.4, r, ORANGE, 4, n=28)
    ax.text(cx, 7.1, title, ha="center", va="bottom", fontsize=8, color=INK,
            fontweight="bold")
    ax.text(cx, 3.9, ztxt, ha="center", va="top", fontsize=BODY, color=INK)
    ax.text(cx, 3.2, when, ha="center", va="top", fontsize=SMALL, color=MUTED)


def panel_regimes(ax):
    canvas(ax, "e", "Three regimes, and the order r/wallstreetbets passed "
                    "through them", w=30, h=8.2)
    regime(ax, 5.0, 1.15, "Chance-level mixing", "z near 0", "through 2020Q3")
    regime(ax, 15.0, 0.35, "Fusion", "z far above 0",
           "the two GameStop windows")
    regime(ax, 25.0, 1.75, "Walls", "z far below 0",
           "2021Q2 onward, no reversion")
    for x in (9.4, 19.4):
        ax.add_patch(FancyArrowPatch((x, 5.4), (x + 1.2, 5.4),
                                     arrowstyle="-|>", mutation_scale=9,
                                     color=GREY, lw=0.9))
    ax.text(15.0, 1.9, "Audiences of two suppressed tickers, drawn as the "
                       "documents that mention each. Overlap is co-mention.",
            ha="center", va="top", fontsize=SMALL, color=MUTED)


def main():
    fig = plt.figure(figsize=(FIG_W, 6.6))
    gs = fig.add_gridspec(3, 2, height_ratios=[0.84, 0.84, 0.82], hspace=0.32,
                          wspace=0.10, left=0.06, right=0.99, top=0.95,
                          bottom=0.02)
    panel_document(fig.add_subplot(gs[0, 0]))
    panel_eligible(fig.add_subplot(gs[0, 1]))
    panel_windows(fig.add_subplot(gs[1, 0]))
    panel_null(fig.add_subplot(gs[1, 1]))
    panel_regimes(fig.add_subplot(gs[2, :]))
    print("wrote", save(fig, "p2_schematic") + ".{png,pdf}")


if __name__ == "__main__":
    main()
