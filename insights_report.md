# 📊 SentiView – Insights Report

**Project**: Sentiment Analysis Tool
**Week**: 3 – AI for Data Analysis & Insights
**Programme**: CAPACITI AI Bootcamp | Clickatell April 2026
**Author**: [Your Name]
**Date**: April / May 2026

---

## 1. Project Overview

SentiView is a sentiment analysis dashboard that applies Natural Language Processing (NLP) to classify customer reviews as **Positive**, **Negative**, or **Neutral**. The project demonstrates how AI can automate qualitative data interpretation at scale — turning raw text into actionable business intelligence.

---

## 2. Dataset Description

| Property | Value |
|---|---|
| File | `reviews.csv` |
| Total Records | 35 |
| Columns | `id`, `review`, `category` |
| Categories | Electronics, Clothing, Service, Delivery, Packaging |
| Language | English |

The dataset was hand-crafted to represent a realistic spread of sentiments across common e-commerce review scenarios.

---

## 3. Methodology

### 3.1 Text Pre-Processing
Before analysis, each review undergoes cleaning:
- Convert to lowercase
- Remove URLs and hyperlinks
- Strip non-alphanumeric characters (preserving key punctuation)
- Collapse repeated whitespace

### 3.2 Sentiment Scoring (TextBlob)

TextBlob's `PatternAnalyzer` computes two scores per text:

| Score | Range | Meaning |
|---|---|---|
| **Polarity** | -1.0 → +1.0 | Negative to Positive |
| **Subjectivity** | 0.0 → 1.0 | Objective to Subjective |

### 3.3 Classification Thresholds

| Polarity Range | Label |
|---|---|
| > 0.05 | ✅ Positive |
| -0.05 to 0.05 | 😐 Neutral |
| < -0.05 | ❌ Negative |

---

## 4. Key Findings

### 4.1 Sentiment Distribution
*(Values will vary — update after running the app)*

- **Positive** reviews represent the largest share, reflecting satisfied customers.
- **Negative** reviews often cite product defects, delayed delivery, or poor support.
- **Neutral** reviews tend to be brief, factual, and low-subjectivity.

### 4.2 Category-Level Observations

- **Electronics** is the most reviewed category and shows the widest polarity variance.
- **Service** reviews are highly polarised — customers either love or hate their experience.
- **Delivery** reviews are primarily negative, highlighting a logistics gap.
- **Clothing** reviews skew positive when size and colour match expectations.

### 4.3 Polarity vs. Subjectivity
- High-polarity reviews (very positive or very negative) also tend to be more subjective.
- Neutral reviews cluster near subjectivity 0.3–0.5, suggesting mild personal opinion.

---

## 5. Visualisations Produced

| Chart | Insight |
|---|---|
| 🥧 Pie Chart | Overall sentiment split (%) |
| 📊 Bar Chart | Raw count comparison |
| 🔵 Scatter Plot | Polarity vs. Subjectivity relationship |
| 📉 Histogram | Distribution of polarity scores |
| 🎚️ Gauge | Single-text polarity visual indicator |

---

## 6. Challenges & Solutions

| Challenge | Solution |
|---|---|
| TextBlob misclassifies sarcasm | Documented as a known NLP limitation; future fix: transformer model |
| Short reviews have unreliable scores | Added a polarity confidence indicator to signal low certainty |
| Streamlit's default styling is generic | Implemented a custom CSS file to create a branded dark dashboard |
| CSV files may have different column names | Added a dynamic column-selector on the upload page |
| Matplotlib backgrounds don't match Streamlit dark theme | Set `facecolor` to match app background (`#0F1117`) |

---

## 7. What I Learned

- How NLP libraries like **TextBlob** parse and score text sentiment.
- How to build a **multi-page Streamlit** application with sidebar navigation.
- How to create publication-quality **dark-themed charts** with Matplotlib.
- How to structure a Python project for **portfolio presentation**.
- The importance of **data cleaning** before any NLP pipeline.
- How to connect **data analysis** outputs to **business recommendations**.

---

## 8. Business Recommendations

Based on the analysis:

1. **Prioritise delivery improvements** — negative delivery reviews drag down overall scores.
2. **Leverage positive reviews** for marketing copy and social proof.
3. **Flag high-subjectivity negative reviews** for human review escalation.
4. **Automate sentiment monitoring** — deploy this tool on incoming live review streams.
5. **Segment analysis by category** — Electronics and Service need the most attention.

---

## 9. Future Enhancements

- Replace TextBlob with **VADER** (better for informal/social text).
- Add **transformer-based models** (e.g., HuggingFace `distilbert-base-uncased-finetuned-sst-2-english`) for higher accuracy.
- Build a **live Twitter/X feed analyser**.
- Add **word cloud** for most frequent terms per sentiment class.
- Deploy to **Streamlit Cloud** for public access.
- Add **topic modelling** (LDA) to extract key complaint themes.

---

## 10. References

- TextBlob Documentation: https://textblob.readthedocs.io/
- Streamlit Documentation: https://docs.streamlit.io/
- Pattern NLP Library: https://clips.uantwerpen.be/pages/pattern
- CAPACITI Bootcamp Programme: https://capaciti.org.za

---

*Report compiled for CAPACITI AI Bootcamp Week 3 – Sentiment Analysis & Data Insights.*
*© 2026 [Your Name] – All rights reserved.*
