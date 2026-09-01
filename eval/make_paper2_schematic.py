#!/usr/bin/env python3
"""Paper 2, Figure 1 (schematic): how the segregation statistic is built
and the three regimes it can express.

Purely illustrative. No panel is computed from data; every number shown
is a toy value chosen to make the construction legible. Real values live
in Figures 2 to 4 (eval/make_paper2_figs.py, from committed TSVs).

Layout: one axes spanning the figure, coordinates in inches. Every panel
is a card of fixed size with the same inner padding; the panel letter
and its title share a baseline; margins and gutters are single constants.
The figure is saved at its own size (no auto-crop), so the outer margin
is the same on all four sides.

Output: reports/figures/p2_schematic.{png,pdf}
Style: eval/paper2_figstyle.py (shared with the data figures).
"""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle, FancyArrowPatch, Rectangle
import numpy as np

from paper2_figstyle import (BLUE, ORANGE, GREEN, RED, GREY, BAND, INK, MUTED,
                             FIG_W, save)

# ---- geometry (inches) --------------------------------------------------
M = 0.0           # outer margin is applied at save (PAD_X / PAD_Y)
G = 0.25          # gutter between cards
P = 0.12          # inner padding of every card
HEAD = 0.24       # header band inside each card (letter + title)
R1 = 2.05         # height of rows 1 and 2
R3 = 1.85         # height of row 3
CW = (FIG_W - 2 * M - G) / 2          # card width, two-column rows
FIG_H = 2 * M + 2 * R1 + R3 + 2 * G   # total height

# ---- type (points) ------------------------------------------------------
T_LETTER, T_TITLE, T_BODY, T_SMALL, T_CHIP = 10, 8.5, 7.2, 6.8, 7
LINE = 1.28       # line spacing multiplier for body text
PT = 1 / 72       # inches per point


def lines_h(n, size=T_BODY):
    """Height in inches of n lines of text at a point size."""
    return n * size * LINE * PT


# ---- primitives ---------------------------------------------------------
def card(ax, x, y, w, h, letter, title):
    """Header inside the card; returns the content box (x0, y0, w, h)."""
    base = y + h - P - 0.15                    # shared baseline of letter and title
    ax.text(x + P, base, letter, fontsize=T_LETTER, fontweight="bold",
            va="baseline", ha="left", color=INK)
    ax.text(x + P + 0.27, base, title, fontsize=T_TITLE, va="baseline",
            ha="left", color=INK)
    return x + P, y + P, w - 2 * P, h - 2 * P - HEAD


def text(ax, x, y, s, size=T_BODY, color=INK, ha="left", va="top", **kw):
    ax.text(x, y, s, fontsize=size, color=color, ha=ha, va=va,
            linespacing=LINE, **kw)


def chip(ax, x, y, label, fc, w=0.30, h=0.17):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                                boxstyle="round,pad=0,rounding_size=0.04",
                                fc=fc, ec="none"))
    ax.text(x + w / 2, y + h / 2, label, ha="center", va="center",
            fontsize=T_CHIP, color="white", fontweight="bold")


def author_card(ax, x, y, w, h, who, tickers, colors):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                                boxstyle="round,pad=0,rounding_size=0.06",
                                fc="#f4f4f4", ec=GREY, lw=0.6))
    text(ax, x + 0.08, y + h - 0.05, who, size=T_BODY)
    for i, (t, c) in enumerate(zip(tickers, colors)):
        chip(ax, x + 0.08 + i * 0.36, y + 0.06, t, c)


def dots(ax, cx, cy, r, n, color, seed, ms=2.0):
    rng = np.random.default_rng(seed)
    th = rng.uniform(0, 2 * np.pi, n)
    rr = r * 0.84 * np.sqrt(rng.uniform(0, 1, n))
    ax.plot(cx + rr * np.cos(th), cy + rr * np.sin(th), "o", ms=ms,
            color=color, alpha=0.8, mec="none")


def audience(ax, cx, cy, r, color, seed, n=60, ms=2.0):
    ax.add_patch(Circle((cx, cy), r, fc=color, ec=color, alpha=0.12, lw=0))
    ax.add_patch(Circle((cx, cy), r, fc="none", ec=color, lw=1.0))
    dots(ax, cx, cy, r, n, color, seed, ms)


# ---- panels -------------------------------------------------------------
def panel_a(ax, box):
    x, y, w, h = box
    top = y + h
    text(ax, x, top, "one quarter, 2020Q2", size=T_SMALL, color=MUTED)
    cw, ch, gap = (w - 0.2) / 2, 0.44, 0.2
    r1 = top - 0.13 - ch
    r2 = r1 - 0.08 - ch
    author_card(ax, x, r1, cw, ch, "author 1", ["A", "B", "D"],
                [BLUE, ORANGE, GREY])
    author_card(ax, x + cw + gap, r1, cw, ch, "author 2", ["B", "C"],
                [ORANGE, GREEN])
    author_card(ax, x, r2, cw, ch, "author 3", ["A", "D"], [BLUE, GREY])
    author_card(ax, x + cw + gap, r2, cw, ch, "author 4", ["C"], [GREEN])
    text(ax, x, y + lines_h(3),
         "Every ticker an author mentions in a quarter, across\n"
         "all posts and comments, is one document. Two tickers\n"
         "co-mention when a document holds both.")


def panel_b(ax, box):
    x, y, w, h = box
    top = y + h
    r = 0.36
    cy = top - 0.26 - r
    for cx, c, t, s in [(x + 0.70, BLUE, "A", 1),
                        (x + w - 0.70, ORANGE, "B", 2)]:
        audience(ax, cx, cy, r, c, s)
        text(ax, cx, top, f"documents\nmentioning {t}", size=T_SMALL,
             color=c, ha="center")
    text(ax, x + w / 2, cy, "0\nshared", size=T_BODY, color=RED, ha="center",
         va="center", fontweight="bold")
    text(ax, x, y + lines_h(4),
         "Both tickers are frequent. Had authors picked tickers\n"
         "independently, at least 2 build-period documents would\n"
         "hold both. Observed: none. The pair is eligible; every\n"
         "window has dozens to hundreds of such pairs.")


def panel_c(ax, box):
    x, y, w, h = box
    top = y + h
    n = 24
    qw = (w * 0.62) / n
    strip_y = top - 0.12 - 0.10
    for i in range(n):
        ax.add_patch(Rectangle((x + i * qw, strip_y), qw * 0.88, 0.10,
                               fc=BAND, ec="none"))
        if i % 4 == 0:
            text(ax, x + i * qw, top, str(2019 + i // 4), size=T_SMALL,
                 color=MUTED, ha="left")
    rows = [strip_y - 0.13 - k * 0.22 for k in range(3)]
    for k, ry in enumerate(rows):
        bx = x + k * qw
        ax.add_patch(Rectangle((bx, ry - 0.15), 4 * qw * 0.97, 0.15, fc=BLUE,
                               alpha=0.35, ec="none"))
        ax.add_patch(Rectangle((bx + 4 * qw, ry - 0.15), 2 * qw * 0.97, 0.15,
                               fc=RED, alpha=0.40, ec="none"))
        text(ax, bx + 6 * qw + 0.06, ry - 0.08, f"window {k + 1}",
             size=T_SMALL, color=MUTED, va="center")
    lx = x + w * 0.62 + 0.15
    for k, (fc, a, s) in enumerate([(BLUE, 0.35, "build, 4 quarters"),
                                    (RED, 0.40, "evaluate, 2 quarters"),
                                    (None, 0, "step 1 quarter, 19 windows")]):
        ry = rows[k] - 0.08
        if fc:
            ax.add_patch(Rectangle((lx, ry - 0.06), 0.14, 0.12, fc=fc,
                                   alpha=a, ec="none"))
        text(ax, lx + (0.19 if fc else 0), ry, s, size=T_SMALL,
             color=INK if fc else MUTED, va="center")
    text(ax, x, y + lines_h(4),
         "Eligible pairs are found in the build period. The statistic\n"
         "counts evaluation-period documents that hold any eligible\n"
         "pair. Build length was chosen by an outcome-blind census\n"
         "rule before any result.")


def panel_d(ax, box):
    x, y, w, h = box
    top = y + h
    rng = np.random.default_rng(7)
    null = rng.normal(480, 22, 100)
    bins = np.arange(400, 570, 10)
    hist, edges = np.histogram(null, bins=bins)
    left, span = x + 0.2, w - 0.4
    base = top - 0.16 - 0.62
    hh = hist / hist.max() * 0.55
    for c, e in zip(hh, edges[:-1]):
        ax.add_patch(Rectangle((left + (e - 400) / 170 * span, base),
                               span / len(bins) * 0.88, c, fc=GREY,
                               alpha=0.6, ec="none"))
    ax.plot([left, left + span], [base, base], color=MUTED, lw=0.6)
    ox = left + (525 - 400) / 170 * span
    ax.plot([ox, ox], [base, base + 0.62], color=RED, lw=1.5)
    text(ax, ox + 0.04, base + 0.60, "observed", size=T_SMALL, color=RED)
    text(ax, left + span * 0.42, top, "100 shuffles of ticker labels",
         size=T_SMALL, color=MUTED, ha="center")
    text(ax, left, base - 0.03, "fewer co-mentions", size=T_SMALL,
         color=MUTED)
    text(ax, left + span, base - 0.03, "more", size=T_SMALL, color=MUTED,
         ha="right")
    text(ax, x, y + lines_h(4),
         "z = (observed - shuffle mean) / shuffle sd. z near 0:\n"
         "suppressed pairs meet as often as chance. z far below 0:\n"
         "kept apart, a wall. z above 0: pushed together. Each\n"
         "window has its own null.")


def panel_e(ax, box):
    x, y, w, h = box
    top = y + h
    r = 0.30
    cy = top - 0.30 - r
    col = w / 3
    specs = [("Chance-level mixing", 0.30, "z near 0", "through 2020Q3"),
             ("Fusion", 0.09, "z far above 0", "the two GameStop windows"),
             ("Walls", 0.46, "z far below 0", "2021Q2 onward, no reversion")]
    for i, (title, sep, ztxt, when) in enumerate(specs):
        cx = x + col * (i + 0.5)
        text(ax, cx, top - 0.06, title, size=8, color=INK, ha="center",
             fontweight="bold")
        audience(ax, cx - sep, cy, r, BLUE, 3, n=28, ms=1.8)
        audience(ax, cx + sep, cy, r, ORANGE, 4, n=28, ms=1.8)
        text(ax, cx, cy - r - 0.05, ztxt, size=T_BODY, ha="center")
        text(ax, cx, cy - r - 0.20, when, size=T_SMALL, color=MUTED,
             ha="center")
        if i < 2:
            ax.add_patch(FancyArrowPatch((cx + col / 2 - 0.16, cy),
                                         (cx + col / 2 + 0.16, cy),
                                         arrowstyle="-|>", mutation_scale=8,
                                         color=GREY, lw=0.9))


def main():
    fig = plt.figure(figsize=(FIG_W, FIG_H))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, FIG_W)
    ax.set_ylim(0, FIG_H)
    ax.set_aspect("equal")
    ax.axis("off")

    y3 = M
    y2 = y3 + R3 + G
    y1 = y2 + R1 + G
    xl, xr = M, M + CW + G
    panel_a(ax, card(ax, xl, y1, CW, R1, "a",
                     "The document: one author, one quarter"))
    panel_b(ax, card(ax, xr, y1, CW, R1, "b",
                     "An eligible pair: should have met, never did"))
    panel_c(ax, card(ax, xl, y2, CW, R1, "c",
                     "Rolling windows over 2019 to 2024"))
    panel_d(ax, card(ax, xr, y2, CW, R1, "d",
                     "The statistic: observed count vs. a shuffle null"))
    panel_e(ax, card(ax, xl, y3, 2 * CW + G, R3, "e",
                     "Three regimes, and the order r/wallstreetbets passed "
                     "through them"))
    print("wrote", save(fig, "p2_schematic", tight=False) + ".{png,pdf}")


if __name__ == "__main__":
    main()
