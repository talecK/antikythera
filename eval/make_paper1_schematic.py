#!/usr/bin/env python3
"""Paper 1, Figure 1 (schematic): how the instrument is built, the two
readouts it produces, and why one formation criterion had to be retired.

Purely illustrative. No panel is computed from data; every number shown
is a toy value chosen to make the construction legible. Real values live
in Figures 2 to 4 (eval/make_paper_figs.py, from committed artifacts).

Layout and primitives are shared with paper 2's schematic
(eval/make_paper2_schematic.py) so the two figures read as one set:
one axes spanning the figure, coordinates in inches, cards of fixed
size with one inner padding and one header band.

Output: reports/figures/p1_schematic.{png,pdf}
Style: eval/paper2_figstyle.py (shared with the data figures).
"""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle
import numpy as np

from paper2_figstyle import (BLUE, ORANGE, GREEN, RED, GREY, BAND, INK, MUTED,
                             FIG_W, save)
from make_paper2_schematic import (M, G, P, R1, R3, CW, FIG_H, T_BODY, T_SMALL,
                                   lines_h, card, text, chip, audience)


def doc_card(ax, x, y, w, h, title, lines):
    """A rounded card with a title line and rows of (label, chips)."""
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                                boxstyle="round,pad=0,rounding_size=0.06",
                                fc="#f4f4f4", ec=GREY, lw=0.6))
    text(ax, x + 0.08, y + h - 0.05, title, size=T_BODY)
    ry = y + h - 0.35
    for label, chips in lines:
        text(ax, x + 0.08, ry + 0.085, label, size=T_SMALL, color=MUTED,
             va="center")
        for i, (t, c) in enumerate(chips):
            chip(ax, x + 0.62 + i * 0.36, ry, t, c)
        ry -= 0.22


def panel_a(ax, box):
    x, y, w, h = box
    top = y + h
    cw, gap = (w - 0.2) / 2, 0.2
    ch = 0.90
    cy = top - 0.04 - ch
    doc_card(ax, x, cy, cw, ch, "thread: story + comments",
             [("story", [("A", BLUE), ("D", GREY)]),
              ("comment", [("A", BLUE), ("B", ORANGE)]),
              ("comment", [("D", GREY)])])
    doc_card(ax, x + cw + gap, cy, cw, ch, "author-quarter",
             [("post", [("B", ORANGE), ("C", GREEN)]),
              ("post", [("C", GREEN)]),
              ("post", [("B", ORANGE), ("D", GREY)])])
    text(ax, x, y + lines_h(4),
         "Two document definitions. A thread is a story with its top\n"
         "comments; an author-quarter is every concept one person\n"
         "used in three months. Two concepts co-occur when one\n"
         "document holds both.")


def panel_b(ax, box):
    x, y, w, h = box
    top = y + h
    r = 0.36
    cy = top - 0.26 - r
    for cx, c, t, s in [(x + 0.70, BLUE, "A", 1),
                        (x + w - 0.70, ORANGE, "B", 2)]:
        audience(ax, cx, cy, r, c, s)
        text(ax, cx, top, f"documents\nholding {t}", size=T_SMALL,
             color=c, ha="center")
    text(ax, x + w / 2, cy, "0\nshared", size=T_BODY, color=RED, ha="center",
         va="center", fontweight="bold")
    text(ax, x, y + lines_h(4),
         "Both concepts are frequent. Under independence, their\n"
         "expected joint count is at least 2 build-window documents.\n"
         "Observed: none. The pair is eligible, or suppressed:\n"
         "it was expected to co-occur but never did.")


def panel_c(ax, box):
    x, y, w, h = box
    top = y + h
    n = 12
    qw = w / n
    strip_y = top - 0.12 - 0.10
    for i in range(n):
        ax.add_patch(Rectangle((x + i * qw, strip_y), qw * 0.88, 0.10,
                               fc=BAND, ec="none"))
        if i % 4 == 0:
            text(ax, x + i * qw, top, str(2015 + i // 4), size=T_SMALL,
                 color=MUTED, ha="left")
    rows = [strip_y - 0.13, strip_y - 0.13 - 0.22]
    spans = [(8, 4), (4, 4)]       # (build quarters, evaluation quarters)
    for k, (ry, (b, e)) in enumerate(zip(rows, spans)):
        ax.add_patch(Rectangle((x, ry - 0.15), b * qw * 0.97, 0.15, fc=BLUE,
                               alpha=0.35, ec="none"))
        ax.add_patch(Rectangle((x + b * qw, ry - 0.15), e * qw * 0.97, 0.15,
                               fc=RED, alpha=0.40, ec="none"))
        text(ax, x + (b + e) * qw + 0.06, ry - 0.08, f"fold {k + 1}",
             size=T_SMALL, color=MUTED, va="center")
    lx = x + w - 2.05
    ly = rows[1] - 0.15 - 0.16
    for k, (fc, a, s) in enumerate([(BLUE, 0.35, "build window"),
                                    (RED, 0.40, "evaluation year")]):
        ax.add_patch(Rectangle((lx + k * 1.05, ly - 0.06), 0.14, 0.12, fc=fc,
                               alpha=a, ec="none"))
        text(ax, lx + k * 1.05 + 0.19, ly, s, size=T_SMALL, color=INK,
             va="center")
    text(ax, x, y + lines_h(4),
         "Eligible pairs are found in the build window; both readouts are\n"
         "measured in the evaluation year. Fold 1 builds on 2015 to 2016\n"
         "and evaluates 2017; fold 2 builds on 2015 and evaluates 2016.\n"
         "Every fold boundary was registered before the evaluation ran.")


def panel_d(ax, box):
    x, y, w, h = box
    top = y + h
    rng = np.random.default_rng(7)
    null = rng.normal(480, 22, 100)
    bins = np.arange(330, 570, 10)
    hist, edges = np.histogram(null, bins=bins)
    left, span = x + 0.2, w - 0.4
    base = top - 0.16 - 0.62
    hh = hist / hist.max() * 0.55
    for c, e in zip(hh, edges[:-1]):
        ax.add_patch(Rectangle((left + (e - 330) / 240 * span, base),
                               span / len(bins) * 0.88, c, fc=GREY,
                               alpha=0.6, ec="none"))
    ax.plot([left, left + span], [base, base], color=MUTED, lw=0.6)
    ox = left + (360 - 330) / 240 * span
    ax.plot([ox, ox], [base, base + 0.62], color=RED, lw=1.5)
    text(ax, ox + 0.04, base + 0.60, "observed", size=T_SMALL, color=RED)
    text(ax, left + span * 0.62, top, "100 shuffles of concept labels",
         size=T_SMALL, color=MUTED, ha="center")
    text(ax, left, base - 0.03, "fewer co-occurrences", size=T_SMALL,
         color=MUTED)
    text(ax, left + span, base - 0.03, "more", size=T_SMALL, color=MUTED,
         ha="right")
    text(ax, x, y + lines_h(4),
         "Sum document counts separately for every eligible pair. Compare\n"
         "with 100 label shuffles, then deduplicate within documents.\n"
         "Binary margins can change. z = (observed - null mean) /\n"
         "null SD. Negative z means fewer joint occurrences.")


def panel_e(ax, box):
    x, y, w, h = box
    top = y + h
    col = w / 2
    base = top - 0.24 - 0.50
    specs = [("z-criterion (retired)", [("real data", 0.28, BLUE),
                                        ("shuffled data", 0.50, GREY)],
              "Expected count from each concept's own frequency. Large\n"
              "documents make joint counts combinatorially; shuffled data\n"
              "'form' more pairs than the real data."),
             ("per-pair permutation criterion", [("real data", 0.17, BLUE),
                                                 ("shuffled data", 0.15, GREY)],
              "Each pair's threshold is its shuffled 99th percentile.\n"
              "Dashed line: nominal 1 percent count reference, not a\n"
              "calibrated error rate or a guaranteed count bound.")]
    for i, (title, bars, body) in enumerate(specs):
        cx = x + col * i
        text(ax, cx, top - 0.02, title, size=8, color=INK, fontweight="bold")
        bx0 = cx + 0.55
        bw, gap = 0.42, 0.30
        for j, (lab, hgt, c) in enumerate(bars):
            bx = bx0 + j * (bw + gap)
            ax.add_patch(Rectangle((bx, base), bw, hgt, fc=c,
                                   alpha=0.85 if c == BLUE else 0.6, ec="none"))
            text(ax, bx + bw / 2, base - 0.04, lab, size=T_SMALL, color=MUTED,
                 ha="center")
        ax.plot([bx0 - 0.15, bx0 + 2 * bw + gap + 0.15], [base, base],
                color=MUTED, lw=0.6)
        if i == 1:
            fy = base + 0.17
            ax.plot([bx0 - 0.15, bx0 + 2 * bw + gap + 0.15], [fy, fy],
                    color=GREY, lw=0.8, ls="--")
            text(ax, bx0 + 2 * bw + gap + 0.20, fy, "1%", size=T_SMALL,
                 color=MUTED, va="center")
        text(ax, cx + 2.25, base + 0.58, "pairs\nformed", size=T_SMALL,
             color=MUTED, ha="left", va="top")
        text(ax, cx, y + lines_h(3), body)
    # one shared scale: a dotted guide at the height of the real-data bar on
    # the left runs across into the right panel, where both bars sit far below it
    gx0, gx1 = x + 0.55, x + col + 0.55 + 2 * 0.42 + 0.30
    ax.plot([gx0, gx1], [base + 0.28, base + 0.28], ls=":", color=GREY, lw=0.8)
    text(ax, x + col + 0.05, base + 0.31, "same scale", size=T_SMALL,
         color=MUTED, va="bottom")
    ax.add_patch(FancyArrowPatch((x + col - 0.22, base + 0.12),
                                 (x + col + 0.22, base + 0.12),
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
                     "Documents: a thread or an author-quarter"))
    panel_b(ax, card(ax, xr, y1, CW, R1, "b",
                     "An eligible pair: should have met, never did"))
    panel_c(ax, card(ax, xl, y2, CW, R1, "c",
                     "Two folds: build on past years, evaluate the next"))
    panel_d(ax, card(ax, xr, y2, CW, R1, "d",
                     "Segregation: observed counts vs. label shuffles"))
    panel_e(ax, card(ax, xl, y3, 2 * CW + G, R3, "e",
                     "Two criteria for 'this pair formed', and what shuffled "
                     "data do under each"))
    print("wrote", save(fig, "p1_schematic_revision", tight=False) + ".{png,pdf}")


if __name__ == "__main__":
    main()
