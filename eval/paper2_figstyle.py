"""Shared style for the paper 2 figures (data figures and the schematic).

One palette, one type scale, one set of margins, so the four figures read
as a set. Categorical slots were validated with the dataviz palette
checker (light surface): blue / orange / green pass lightness, chroma,
normal-vision separation, and 3:1 contrast; the orange-green pair sits in
the CVD warn band, so every multi-series panel also carries a legend and
distinct marker shapes. Red is the highlight (onset, excursion, real
value) and always travels with a text label. Grey is the neutral for
nulls, bands, and reference lines; it is never a series color.
"""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIG_DIR = os.path.join(ROOT, "reports", "figures")
os.makedirs(FIG_DIR, exist_ok=True)

# palette (validated 2026-09-01; see module docstring)
BLUE = "#3b6ea5"      # slot 1: treatment / B = 4 / ticker A
ORANGE = "#b8761c"    # slot 2: B = 6 / ticker B
GREEN = "#3d8f5f"     # slot 3: control / B = 8 / ticker C
RED = "#b0413e"       # highlight only
GREY = "#8a8a8a"      # neutral: nulls, reference lines, uninformative
BAND = "#e6e6e6"      # chance band fill
INK = "#222222"       # primary text
MUTED = "#5a5a5a"     # secondary text
SURFACE = "#ffffff"

MARKERS = {BLUE: "o", ORANGE: "s", GREEN: "^"}   # secondary encoding

FIG_W = 7.0           # inches, full text width
DPI = 300
PAD_X = 64 / DPI      # outer padding at save: 64 px horizontally at 300 dpi
PAD_Y = 48 / DPI      # 48 px vertically
PAD = PAD_Y           # kept for rcParams; save() applies the asymmetric pad

plt.rcParams.update({
    "font.size": 8,
    "font.family": "sans-serif",
    "axes.titlesize": 8.5,
    "axes.titleweight": "normal",
    "axes.titlelocation": "left",
    "axes.titlepad": 6,
    "axes.labelsize": 8,
    "axes.labelcolor": INK,
    "axes.edgecolor": MUTED,
    "axes.linewidth": 0.6,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "xtick.labelsize": 7,
    "ytick.labelsize": 7,
    "xtick.color": MUTED,
    "ytick.color": MUTED,
    "xtick.major.width": 0.6,
    "ytick.major.width": 0.6,
    "legend.fontsize": 7,
    "legend.frameon": False,
    "legend.handlelength": 1.6,
    "legend.columnspacing": 1.2,
    "legend.borderaxespad": 0.0,
    "lines.linewidth": 1.3,
    "lines.markersize": 4,
    "text.color": INK,
    "figure.dpi": 300,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
    "savefig.pad_inches": PAD,
    "savefig.facecolor": SURFACE,
})


def panel_label(ax, letter):
    """Bold panel letter on the same baseline as the axes title (title pad
    is 6 pt above the axes top, va=baseline), 30 pt left of the axes."""
    ax.annotate(letter, xy=(0, 1), xycoords="axes fraction",
                xytext=(-30, plt.rcParams["axes.titlepad"]),
                textcoords="offset points", fontsize=10, fontweight="bold",
                ha="left", va="baseline", color=INK, annotation_clip=False)


def title_and_legend(ax, title, legend=True, ncol=4):
    """Title at left and legend at right, on one line above the axes."""
    ax.set_title(title, loc="left")
    if legend:
        h, l = ax.get_legend_handles_labels()
        if h:
            ax.legend(h, l, loc="lower right", bbox_to_anchor=(1.0, 1.0),
                      ncol=ncol)


def save(fig, name, tight=True):
    """Crop to the drawn content, then pad by PAD_X horizontally and PAD_Y
    vertically, so every figure has the same outer padding regardless of
    how its axes or cards are laid out. (`tight` is accepted for
    compatibility; both paths now use the same rule.)"""
    import numpy as np
    from matplotlib.transforms import Bbox
    from matplotlib.text import Text
    from matplotlib.patches import Patch
    from matplotlib.lines import Line2D
    from matplotlib.collections import Collection
    fig.canvas.draw()
    r = fig.canvas.get_renderer()
    if all(ax.axison for ax in fig.axes):
        px = fig.get_tightbbox(r).transformed(fig.dpi_scale_trans)
    else:
        # axis-off canvases (the schematic): an off axis still reports its
        # spines and ticks at full extent, so union only the drawn artists
        skip = {fig.patch}
        for ax in fig.axes:
            skip.add(ax.patch)
            if not ax.axison:
                for parent in [ax.xaxis, ax.yaxis, *ax.spines.values()]:
                    skip.update(parent.findobj())
        boxes = []
        for a in fig.findobj():
            if a in skip or not a.get_visible():
                continue
            if not isinstance(a, (Text, Patch, Line2D, Collection)):
                continue
            try:
                b = a.get_window_extent(r)
            except Exception:
                continue
            if b.width > 0 and b.height > 0 and np.isfinite(b.extents).all():
                boxes.append(b)
        px = Bbox.union(boxes)                  # display pixels
    bb = Bbox.from_extents(px.x0 / fig.dpi - PAD_X, px.y0 / fig.dpi - PAD_Y,
                           px.x1 / fig.dpi + PAD_X, px.y1 / fig.dpi + PAD_Y)
    kw = dict(bbox_inches=bb, pad_inches=0)
    fig.savefig(os.path.join(FIG_DIR, name + ".png"), **kw)
    fig.savefig(os.path.join(FIG_DIR, name + ".pdf"), **kw)
    plt.close(fig)
    return os.path.join(FIG_DIR, name)
