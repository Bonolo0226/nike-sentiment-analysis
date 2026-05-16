# ============================================================
# sentiment_analyzer.py
# Core NLP sentiment analysis functions — Nike Reviews Edition
# CAPACITI AI Bootcamp | Week 3 | 2026
# ============================================================

from textblob import TextBlob
import pandas as pd
import re


def analyze_sentiment(text: str) -> dict:
    """
    Analyse a single text string.
    Returns sentiment label, polarity, subjectivity, emoji, confidence.
    """
    if not text or not text.strip():
        return {"sentiment": "Neutral", "polarity": 0.0,
                "subjectivity": 0.0, "emoji": "😐", "confidence": "0%"}

    blob = TextBlob(_clean_text(text))
    polarity      = blob.sentiment.polarity
    subjectivity  = blob.sentiment.subjectivity
    sentiment, emoji = _classify(polarity)

    return {
        "sentiment"   : sentiment,
        "polarity"    : round(polarity, 4),
        "subjectivity": round(subjectivity, 4),
        "emoji"       : emoji,
        "confidence"  : f"{abs(polarity) * 100:.1f}%",
    }


def analyze_dataframe(df: pd.DataFrame, text_column: str) -> pd.DataFrame:
    """Apply sentiment analysis to every row in *text_column*."""
    results        = df[text_column].astype(str).apply(analyze_sentiment)
    df             = df.copy()
    df["Sentiment"]    = results.apply(lambda r: r["sentiment"])
    df["Polarity"]     = results.apply(lambda r: r["polarity"])
    df["Subjectivity"] = results.apply(lambda r: r["subjectivity"])
    df["Emoji"]        = results.apply(lambda r: r["emoji"])
    return df


def get_summary_stats(df: pd.DataFrame) -> dict:
    """High-level statistics for a DataFrame that already has Sentiment columns."""
    counts = df["Sentiment"].value_counts().to_dict()
    total  = len(df)
    return {
        "total"            : total,
        "positive"         : counts.get("Positive", 0),
        "negative"         : counts.get("Negative", 0),
        "neutral"          : counts.get("Neutral",  0),
        "avg_polarity"     : round(df["Polarity"].mean(), 4),
        "avg_subjectivity" : round(df["Subjectivity"].mean(), 4),
        "most_common"      : df["Sentiment"].mode()[0] if total else "N/A",
        "pct_positive"     : round(counts.get("Positive", 0) / total * 100, 1) if total else 0,
        "pct_negative"     : round(counts.get("Negative", 0) / total * 100, 1) if total else 0,
        "pct_neutral"      : round(counts.get("Neutral",  0) / total * 100, 1) if total else 0,
    }


# ── Private helpers ──────────────────────────────────────────
def _clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"http\S+|www\S+", "", text)
    text = re.sub(r"[^a-zA-Z0-9\s'.,!?]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def _classify(polarity: float) -> tuple:
    if polarity > 0.05:
        return "Positive", "😊"
    elif polarity < -0.05:
        return "Negative", "😞"
    return "Neutral", "😐"
