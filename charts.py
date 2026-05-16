# ============================================================
# charts.py  –  All Matplotlib visualisations
# Nike Sentiment Analysis Dashboard
# CAPACITI AI Bootcamp | Week 3 | 2026
# ============================================================

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec
import pandas as pd
import numpy as np

# ── Theme palettes ───────────────────────────────────────────
SENTIMENT_COLORS = {
    "Positive": "#00C896",
    "Negative": "#FF4560",
    "Neutral" : "#FEB019",
}

DARK_THEME = {
    "bg"      : "#0D0D0F",
    "surface" : "#18181C",
    "border"  : "#2A2A35",
    "text"    : "#F0F0F5",
    "subtext" : "#8888A0",
}

LIGHT_THEME = {
    "bg"      : "#F8F8FC",
    "surface" : "#FFFFFF",
    "border"  : "#E0E0EC",
    "text"    : "#111118",
    "subtext" : "#555568",
}


def _theme(dark: bool) -> dict:
    return DARK_THEME if dark else LIGHT_THEME


def _style_ax(ax, fig, dark: bool):
    """Apply common dark/light theme to an axis."""
    t = _theme(dark)
    fig.patch.set_facecolor(t["bg"])
    ax.set_facecolor(t["surface"])
    ax.tick_params(colors=t["text"], labelsize=9)
    ax.xaxis.label.set_color(t["text"])
    ax.yaxis.label.set_color(t["text"])
    ax.title.set_color(t["text"])
    for spine in ax.spines.values():
        spine.set_edgecolor(t["border"])


# ── 1. Donut chart ────────────────────────────────────────────
def donut_chart(df: pd.DataFrame, dark: bool = True) -> plt.Figure:
    t = _theme(dark)
    counts = df["Sentiment"].value_counts()
    labels = counts.index.tolist()
    sizes  = counts.values.tolist()
    colors = [SENTIMENT_COLORS.get(l, "#AAA") for l in labels]

    fig, ax = plt.subplots(figsize=(5, 5))
    fig.patch.set_facecolor(t["bg"])
    ax.set_facecolor(t["bg"])

    wedges, _, autotexts = ax.pie(
        sizes, labels=None, autopct="%1.1f%%",
        colors=colors, startangle=90,
        wedgeprops=dict(width=0.55, edgecolor=t["bg"], linewidth=3),
        pctdistance=0.78,
    )
    for at in autotexts:
        at.set_color(t["bg"])
        at.set_fontweight("bold")
        at.set_fontsize(10)

    # Centre label
    total = sum(sizes)
    ax.text(0, 0.08, str(total), ha="center", va="center",
            fontsize=22, fontweight="bold", color=t["text"])
    ax.text(0, -0.22, "reviews", ha="center", va="center",
            fontsize=10, color=t["subtext"])

    legend_patches = [mpatches.Patch(color=SENTIMENT_COLORS[l], label=f"{l}  {c}")
                      for l, c in zip(labels, sizes)]
    ax.legend(handles=legend_patches, loc="lower center", bbox_to_anchor=(0.5, -0.08),
              ncol=3, frameon=False,
              labelcolor=t["text"], fontsize=9)
    ax.set_title("Sentiment Split", color=t["text"], fontsize=13, fontweight="bold", pad=10)
    plt.tight_layout()
    return fig


# ── 2. Horizontal bar chart ───────────────────────────────────
def bar_chart(df: pd.DataFrame, dark: bool = True) -> plt.Figure:
    t = _theme(dark)
    counts = df["Sentiment"].value_counts().reindex(
        ["Positive", "Neutral", "Negative"], fill_value=0)

    fig, ax = plt.subplots(figsize=(6, 3.2))
    _style_ax(ax, fig, dark)

    for i, (label, val) in enumerate(counts.items()):
        color = SENTIMENT_COLORS[label]
        ax.barh(label, val, color=color, height=0.5,
                edgecolor=t["bg"], linewidth=1.5)
        ax.text(val + 0.4, i, str(val), va="center",
                color=t["text"], fontweight="bold", fontsize=10)

    ax.set_xlim(0, counts.max() * 1.18)
    ax.set_xlabel("Number of Reviews", fontsize=9)
    ax.set_title("Reviews by Sentiment", fontsize=12, fontweight="bold", pad=8)
    ax.grid(axis="x", color=t["border"], linestyle="--", linewidth=0.6, alpha=0.5)
    plt.tight_layout()
    return fig


# ── 3. Scatter: polarity vs subjectivity ─────────────────────
def polarity_scatter(df: pd.DataFrame, dark: bool = True) -> plt.Figure:
    t = _theme(dark)
    fig, ax = plt.subplots(figsize=(6, 4.5))
    _style_ax(ax, fig, dark)

    for label, grp in df.groupby("Sentiment"):
        ax.scatter(grp["Polarity"], grp["Subjectivity"],
                   color=SENTIMENT_COLORS.get(label, "#AAA"),
                   label=label, alpha=0.75, s=55, edgecolors="none", zorder=3)

    ax.axvline(0, color=t["border"], linestyle="--", linewidth=1)
    ax.axhline(0.5, color=t["border"], linestyle="--", linewidth=1)
    ax.set_xlabel("Polarity  (–1 negative → +1 positive)", fontsize=9)
    ax.set_ylabel("Subjectivity  (0 objective → 1 subjective)", fontsize=9)
    ax.set_title("Polarity vs Subjectivity", fontsize=12, fontweight="bold", pad=8)
    ax.legend(frameon=False, labelcolor=t["text"], fontsize=9)
    ax.grid(color=t["border"], linestyle="--", linewidth=0.5, alpha=0.4)
    plt.tight_layout()
    return fig


# ── 4. Polarity histogram ─────────────────────────────────────
def polarity_histogram(df: pd.DataFrame, dark: bool = True) -> plt.Figure:
    t = _theme(dark)
    fig, ax = plt.subplots(figsize=(6, 3.5))
    _style_ax(ax, fig, dark)

    n, bins, patches = ax.hist(df["Polarity"], bins=20,
                                edgecolor=t["bg"], linewidth=1.2, alpha=0.9)
    # Colour each bar by its polarity position
    for patch, left in zip(patches, bins[:-1]):
        mid = left + (bins[1] - bins[0]) / 2
        patch.set_facecolor(
            SENTIMENT_COLORS["Positive"] if mid > 0.05
            else SENTIMENT_COLORS["Negative"] if mid < -0.05
            else SENTIMENT_COLORS["Neutral"]
        )

    mean_val = df["Polarity"].mean()
    ax.axvline(mean_val, color="#FFFFFF" if dark else "#111",
               linestyle="--", linewidth=1.5,
               label=f"Mean  {mean_val:+.3f}")
    ax.set_xlabel("Polarity Score", fontsize=9)
    ax.set_ylabel("Frequency", fontsize=9)
    ax.set_title("Polarity Distribution", fontsize=12, fontweight="bold", pad=8)
    ax.legend(frameon=False, labelcolor=t["text"], fontsize=9)
    ax.grid(axis="y", color=t["border"], linestyle="--", linewidth=0.5, alpha=0.4)
    plt.tight_layout()
    return fig


# ── 5. Category stacked bar ───────────────────────────────────
def category_stacked_bar(df: pd.DataFrame, dark: bool = True) -> plt.Figure:
    t = _theme(dark)
    pivot = df.groupby(["category", "Sentiment"]).size().unstack(fill_value=0)
    for col in ["Positive", "Neutral", "Negative"]:
        if col not in pivot:
            pivot[col] = 0
    pivot = pivot[["Positive", "Neutral", "Negative"]]

    fig, ax = plt.subplots(figsize=(7, 4))
    _style_ax(ax, fig, dark)

    bottom = np.zeros(len(pivot))
    for sentiment in ["Positive", "Neutral", "Negative"]:
        vals = pivot[sentiment].values
        ax.bar(pivot.index, vals, bottom=bottom,
               color=SENTIMENT_COLORS[sentiment], label=sentiment,
               edgecolor=t["bg"], linewidth=1.2, width=0.55)
        bottom += vals

    ax.set_ylabel("Review Count", fontsize=9)
    ax.set_title("Sentiment by Product Category", fontsize=12, fontweight="bold", pad=8)
    ax.tick_params(axis="x", rotation=20, labelsize=8)
    ax.legend(frameon=False, labelcolor=t["text"], fontsize=9,
              loc="upper right")
    ax.grid(axis="y", color=t["border"], linestyle="--", linewidth=0.5, alpha=0.4)
    plt.tight_layout()
    return fig


# ── 6. Rating vs polarity line ────────────────────────────────
def rating_vs_polarity(df: pd.DataFrame, dark: bool = True) -> plt.Figure:
    t = _theme(dark)
    if "rating" not in df.columns:
        return None
    grouped = df.groupby("rating")["Polarity"].mean().reset_index()

    fig, ax = plt.subplots(figsize=(6, 3.5))
    _style_ax(ax, fig, dark)

    ax.plot(grouped["rating"], grouped["Polarity"],
            color="#00C896", linewidth=2.5, marker="o",
            markersize=8, markerfacecolor="#0D0D0F" if dark else "#FFF",
            markeredgecolor="#00C896", markeredgewidth=2)
    ax.fill_between(grouped["rating"], grouped["Polarity"],
                    alpha=0.12, color="#00C896")
    ax.set_xlabel("Star Rating", fontsize=9)
    ax.set_ylabel("Avg Polarity", fontsize=9)
    ax.set_title("Avg Polarity by Star Rating", fontsize=12, fontweight="bold", pad=8)
    ax.set_xticks([1, 2, 3, 4, 5])
    ax.grid(color=t["border"], linestyle="--", linewidth=0.5, alpha=0.4)
    plt.tight_layout()
    return fig


# ── 7. Polarity gauge (single text) ──────────────────────────
def polarity_gauge(polarity: float, dark: bool = True) -> plt.Figure:
    t = _theme(dark)
    fig, ax = plt.subplots(figsize=(6, 1.6))
    _style_ax(ax, fig, dark)

    ax.barh([0], [2], left=-1, color=t["border"], height=0.35)
    color = (SENTIMENT_COLORS["Positive"] if polarity > 0.05
             else SENTIMENT_COLORS["Negative"] if polarity < -0.05
             else SENTIMENT_COLORS["Neutral"])
    ax.barh([0], [abs(polarity)],
            left=0 if polarity >= 0 else polarity,
            color=color, height=0.35)
    ax.axvline(0, color=t["text"], linewidth=1.5)
    ax.set_xlim(-1, 1)
    ax.set_xticks([-1, -0.5, 0, 0.5, 1])
    ax.set_xticklabels(["-1.0", "-0.5", "0", "+0.5", "+1.0"])
    ax.set_yticks([])
    ax.set_title(f"Polarity Gauge  ({polarity:+.3f})", fontsize=11,
                 fontweight="bold", color=t["text"], pad=6)
    for spine in ["top", "right", "left"]:
        ax.spines[spine].set_visible(False)
    plt.tight_layout()
    return fig
