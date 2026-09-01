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
PAD = 0.06            # outer padding at save, inches

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
    """tight=True crops to content with PAD on every side (data figures);
    tight=False keeps the figure's own fixed margins (the schematic)."""
    kw = {} if tight else dict(bbox_inches=None, pad_inches=0)
    fig.savefig(os.path.join(FIG_DIR, name + ".png"), **kw)
    fig.savefig(os.path.join(FIG_DIR, name + ".pdf"), **kw)
    plt.close(fig)
    return os.path.join(FIG_DIR, name)
