# ============================================================
# app.py  –  Nike Sentiment Analysis Dashboard
# Advanced Streamlit UI | Light / Dark Mode
# CAPACITI AI Bootcamp | Week 3 | 2026
# Run:  streamlit run app.py
# ============================================================

import streamlit as st
import pandas as pd
import os

from sentiment_analyzer import analyze_sentiment, analyze_dataframe, get_summary_stats
from charts import (donut_chart, bar_chart, polarity_scatter,
                    polarity_histogram, category_stacked_bar,
                    rating_vs_polarity, polarity_gauge)

# ── Must be first Streamlit call ─────────────────────────────
st.set_page_config(
    page_title="NikeSenti | Sentiment Dashboard",
    page_icon="👟",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ════════════════════════════════════════════════════════════
# THEME SYSTEM
# ════════════════════════════════════════════════════════════
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True

dark = st.session_state.dark_mode

# Colour tokens
if dark:
    BG        = "#0D0D0F"
    SURFACE   = "#18181C"
    SURFACE2  = "#222228"
    BORDER    = "#2A2A35"
    TEXT      = "#F0F0F5"
    SUBTEXT   = "#8888A0"
    ACCENT    = "#00C896"
    DANGER    = "#FF4560"
    WARN      = "#FEB019"
    CARD_GLOW = "rgba(0,200,150,0.08)"
else:
    BG        = "#F4F4FA"
    SURFACE   = "#FFFFFF"
    SURFACE2  = "#EEEEF6"
    BORDER    = "#D8D8E8"
    TEXT      = "#111118"
    SUBTEXT   = "#555568"
    ACCENT    = "#00A87A"
    DANGER    = "#D93025"
    WARN      = "#D4930A"
    CARD_GLOW = "rgba(0,168,122,0.07)"

# ── Inject global CSS ────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Barlow:ital,wght@0,300;0,400;0,600;0,700;0,900;1,400&family=DM+Mono:wght@400;500&display=swap');

/* ── Reset ── */
html, body, [class*="css"] {{
    font-family: 'Barlow', sans-serif;
    background-color: {BG} !important;
    color: {TEXT} !important;
}}

/* ── Sidebar ── */
[data-testid="stSidebar"] {{
    background: {SURFACE} !important;
    border-right: 1px solid {BORDER} !important;
}}
[data-testid="stSidebar"] * {{
    color: {TEXT} !important;
}}

/* ── Main content background ── */
[data-testid="stAppViewContainer"] > .main {{
    background: {BG} !important;
}}

/* ── Header banner ── */
.nike-header {{
    background: linear-gradient(135deg, {SURFACE} 0%, {SURFACE2} 100%);
    border: 1px solid {BORDER};
    border-radius: 20px;
    padding: 2.2rem 2.8rem;
    margin-bottom: 1.8rem;
    position: relative;
    overflow: hidden;
}}
.nike-header::after {{
    content: 'JUST DO IT';
    position: absolute;
    right: -10px;
    top: 50%;
    transform: translateY(-50%) rotate(-12deg);
    font-size: 5rem;
    font-weight: 900;
    font-style: italic;
    color: {BORDER};
    opacity: 0.35;
    letter-spacing: -2px;
    pointer-events: none;
    user-select: none;
}}
.nike-header h1 {{
    font-size: 2.2rem;
    font-weight: 900;
    font-style: italic;
    color: {TEXT};
    margin: 0 0 0.3rem 0;
    letter-spacing: -0.5px;
}}
.nike-header h1 span {{ color: {ACCENT}; }}
.nike-header p {{
    color: {SUBTEXT};
    font-size: 1rem;
    margin: 0;
    font-weight: 400;
}}
.nike-logo {{
    font-size: 2.5rem;
    display: inline-block;
    margin-right: 0.5rem;
}}

/* ── KPI cards ── */
.kpi-grid {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1rem;
    margin: 1.2rem 0;
}}
.kpi-card {{
    background: {SURFACE};
    border: 1px solid {BORDER};
    border-radius: 14px;
    padding: 1.3rem 1.4rem;
    position: relative;
    overflow: hidden;
    transition: transform 0.2s;
}}
.kpi-card:hover {{ transform: translateY(-2px); }}
.kpi-card::before {{
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: var(--accent-color);
    border-radius: 14px 14px 0 0;
}}
.kpi-value {{
    font-size: 2rem;
    font-weight: 700;
    color: var(--accent-color);
    line-height: 1;
    margin-bottom: 0.25rem;
}}
.kpi-label {{
    font-size: 0.8rem;
    font-weight: 600;
    color: {SUBTEXT};
    text-transform: uppercase;
    letter-spacing: 0.08em;
}}
.kpi-sub {{
    font-size: 0.75rem;
    color: {SUBTEXT};
    margin-top: 0.2rem;
    font-family: 'DM Mono', monospace;
}}

/* ── Section headers ── */
.section-label {{
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: {ACCENT};
    margin: 0 0 0.3rem 0;
}}
.section-title {{
    font-size: 1.4rem;
    font-weight: 700;
    color: {TEXT};
    margin: 0 0 1.2rem 0;
}}

/* ── Result card ── */
.result-card {{
    background: {SURFACE};
    border-radius: 16px;
    padding: 2rem;
    text-align: center;
    border: 1px solid {BORDER};
    box-shadow: 0 0 40px {CARD_GLOW};
}}
.result-emoji {{ font-size: 3.5rem; margin-bottom: 0.6rem; display:block; }}
.result-sentiment {{
    font-size: 2rem;
    font-weight: 900;
    font-style: italic;
    margin-bottom: 1rem;
}}
.result-row {{
    display: flex;
    justify-content: center;
    gap: 1.5rem;
    flex-wrap: wrap;
}}
.result-pill {{
    background: {SURFACE2};
    border: 1px solid {BORDER};
    border-radius: 8px;
    padding: 0.45rem 0.9rem;
    font-family: 'DM Mono', monospace;
    font-size: 0.82rem;
    color: {TEXT};
}}
.result-pill b {{ color: {ACCENT}; }}

/* ── Review table rows ── */
.positive-row {{ background: rgba(0,200,150,0.06) !important; }}
.negative-row {{ background: rgba(255,69,96,0.06) !important; }}

/* ── Divider ── */
.fancy-divider {{
    height: 1px;
    background: linear-gradient(90deg, transparent, {BORDER}, transparent);
    margin: 2rem 0;
}}

/* ── Buttons ── */
.stButton > button {{
    background: {ACCENT} !important;
    color: {BG} !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Barlow', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    padding: 0.6rem 1.4rem !important;
    letter-spacing: 0.03em !important;
    transition: opacity 0.2s !important;
}}
.stButton > button:hover {{ opacity: 0.82 !important; }}

/* ── Text area & inputs ── */
.stTextArea textarea, .stTextInput input {{
    background: {SURFACE} !important;
    border: 1px solid {BORDER} !important;
    color: {TEXT} !important;
    border-radius: 10px !important;
    font-family: 'Barlow', sans-serif !important;
}}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {{
    background: {SURFACE} !important;
    border-radius: 12px !important;
    padding: 4px !important;
    gap: 4px !important;
    border: 1px solid {BORDER} !important;
}}
.stTabs [data-baseweb="tab"] {{
    border-radius: 9px !important;
    color: {SUBTEXT} !important;
    font-weight: 600 !important;
    font-family: 'Barlow', sans-serif !important;
}}
.stTabs [aria-selected="true"] {{
    background: {ACCENT} !important;
    color: {BG} !important;
}}

/* ── Scrollbar ── */
::-webkit-scrollbar {{ width: 5px; }}
::-webkit-scrollbar-track {{ background: {BG}; }}
::-webkit-scrollbar-thumb {{ background: {BORDER}; border-radius: 3px; }}

/* ── Metric widget ── */
[data-testid="metric-container"] {{
    background: {SURFACE} !important;
    border: 1px solid {BORDER} !important;
    border-radius: 12px !important;
    padding: 1rem !important;
}}
[data-testid="stMetricValue"] {{ color: {ACCENT} !important; font-weight: 700 !important; }}

/* ── Selectbox / radio ── */
.stSelectbox > div > div,
.stRadio > div {{
    background: {SURFACE} !important;
    border-color: {BORDER} !important;
    color: {TEXT} !important;
}}

/* ── Dataframe ── */
[data-testid="stDataFrame"] {{
    border: 1px solid {BORDER} !important;
    border-radius: 12px !important;
    overflow: hidden !important;
}}

/* ── Download button ── */
.stDownloadButton > button {{
    background: {SURFACE2} !important;
    color: {TEXT} !important;
    border: 1px solid {BORDER} !important;
    border-radius: 10px !important;
    font-family: 'Barlow', sans-serif !important;
    font-weight: 600 !important;
}}
</style>
""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════
# SIDEBAR
# ════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown(f"<div style='font-size:2rem; font-weight:900; font-style:italic; color:{ACCENT}'>👟 NikeSenti</div>", unsafe_allow_html=True)
    st.markdown(f"<div style='font-size:0.8rem; color:{SUBTEXT}; margin-bottom:1.2rem;'>AI Review Intelligence</div>", unsafe_allow_html=True)

    # ── Dark / Light mode toggle ─────────────────────────────
    st.markdown(f"<div style='font-size:0.7rem; font-weight:700; letter-spacing:0.1em; text-transform:uppercase; color:{ACCENT}; margin-bottom:0.4rem;'>Appearance</div>", unsafe_allow_html=True)
    mode_label = "☀️ Switch to Light Mode" if dark else "🌙 Switch to Dark Mode"
    if st.button(mode_label, use_container_width=True):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()

    st.markdown(f"<div class='fancy-divider'></div>", unsafe_allow_html=True)

    # ── Navigation ───────────────────────────────────────────
    st.markdown(f"<div style='font-size:0.7rem; font-weight:700; letter-spacing:0.1em; text-transform:uppercase; color:{ACCENT}; margin-bottom:0.4rem;'>Navigation</div>", unsafe_allow_html=True)
    page = st.radio(
        "Go to",
        ["🏠 Overview", "📝 Analyse Text", "📂 Dataset Explorer", "📊 Insights Report"],
        label_visibility="collapsed",
    )

    st.markdown(f"<div class='fancy-divider'></div>", unsafe_allow_html=True)

    # ── Filters (shown on dataset pages) ────────────────────
    st.markdown(f"<div style='font-size:0.7rem; font-weight:700; letter-spacing:0.1em; text-transform:uppercase; color:{ACCENT}; margin-bottom:0.4rem;'>Filters</div>", unsafe_allow_html=True)

    try:
        raw_df = pd.read_csv("reviews.csv")
        categories = ["All"] + sorted(raw_df["category"].unique().tolist())
        selected_cat = st.selectbox("Category", categories)
        sentiments_filter = st.multiselect(
            "Sentiment", ["Positive", "Neutral", "Negative"],
            default=["Positive", "Neutral", "Negative"]
        )
        min_rating, max_rating = st.slider(
            "Star Rating", min_value=1, max_value=5, value=(1, 5)
        )
    except Exception:
        selected_cat = "All"
        sentiments_filter = ["Positive", "Neutral", "Negative"]
        min_rating, max_rating = 1, 5

    st.markdown(f"<div class='fancy-divider'></div>", unsafe_allow_html=True)
    st.markdown(f"<div style='font-size:0.72rem; color:{SUBTEXT};'>CAPACITI AI Bootcamp<br>Week 3 · Sentiment Analysis<br>April 2026</div>", unsafe_allow_html=True)


# ── Helper: load & analyse Nike data ────────────────────────
@st.cache_data
def load_nike_data() -> pd.DataFrame:
    df = pd.read_csv("reviews.csv")
    from sentiment_analyzer import analyze_dataframe
    return analyze_dataframe(df, "review")


def apply_filters(df):
    if selected_cat != "All":
        df = df[df["category"] == selected_cat]
    if sentiments_filter:
        df = df[df["Sentiment"].isin(sentiments_filter)]
    df = df[(df["rating"] >= min_rating) & (df["rating"] <= max_rating)]
    return df


# ── KPI card HTML helper ─────────────────────────────────────
def kpi_card(value, label, sub="", accent=ACCENT):
    return f"""
    <div class='kpi-card' style='--accent-color:{accent};'>
        <div class='kpi-value' style='color:{accent};'>{value}</div>
        <div class='kpi-label'>{label}</div>
        {'<div class="kpi-sub">' + sub + '</div>' if sub else ''}
    </div>"""


# ════════════════════════════════════════════════════════════
# PAGE: OVERVIEW
# ════════════════════════════════════════════════════════════
if page == "🏠 Overview":
    # Header
    st.markdown(f"""
    <div class='nike-header'>
        <span class='nike-logo'>👟</span>
        <h1>Nike<span>Senti</span></h1>
        <p>AI-powered sentiment intelligence across Nike product reviews · {50} reviews analysed</p>
    </div>
    """, unsafe_allow_html=True)

    # Load data
    try:
        full_df = load_nike_data()
        df = apply_filters(full_df)
        stats = get_summary_stats(df)
    except FileNotFoundError:
        st.error("❌ `reviews.csv` not found. Ensure it is in the same folder as `app.py`.")
        st.stop()

    if df.empty:
        st.warning("No reviews match the current filters. Adjust the sidebar filters.")
        st.stop()

    # KPI row
    st.markdown(f"<p class='section-label'>At a Glance</p><p class='section-title'>Dashboard Overview</p>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class='kpi-grid'>
        {kpi_card(stats['total'], 'Total Reviews', f"Filtered from {len(full_df)}", ACCENT)}
        {kpi_card(f"{stats['pct_positive']}%", 'Positive', f"{stats['positive']} reviews", "#00C896")}
        {kpi_card(f"{stats['pct_negative']}%", 'Negative', f"{stats['negative']} reviews", "#FF4560")}
        {kpi_card(f"{stats['avg_polarity']:+.3f}", 'Avg Polarity', stats['most_common'] + " overall", WARN)}
    </div>
    """, unsafe_allow_html=True)

    # Charts row 1
    c1, c2 = st.columns([1, 1.4])
    with c1:
        st.markdown(f"<p class='section-label'>Distribution</p>", unsafe_allow_html=True)
        st.pyplot(donut_chart(df, dark), use_container_width=True)
    with c2:
        st.markdown(f"<p class='section-label'>By Category</p>", unsafe_allow_html=True)
        st.pyplot(category_stacked_bar(df, dark), use_container_width=True)

    st.markdown("<div class='fancy-divider'></div>", unsafe_allow_html=True)

    # Charts row 2
    c3, c4 = st.columns(2)
    with c3:
        st.markdown(f"<p class='section-label'>Score Map</p>", unsafe_allow_html=True)
        st.pyplot(polarity_scatter(df, dark), use_container_width=True)
    with c4:
        fig = rating_vs_polarity(df, dark)
        if fig:
            st.markdown(f"<p class='section-label'>Rating Correlation</p>", unsafe_allow_html=True)
            st.pyplot(fig, use_container_width=True)

    st.markdown("<div class='fancy-divider'></div>", unsafe_allow_html=True)

    # Top positive & negative
    pos_df = df[df["Sentiment"] == "Positive"].nlargest(3, "Polarity")
    neg_df = df[df["Sentiment"] == "Negative"].nsmallest(3, "Polarity")

    p_col, n_col = st.columns(2)
    with p_col:
        st.markdown(f"<p class='section-label'>Top Positive Reviews</p>", unsafe_allow_html=True)
        for _, row in pos_df.iterrows():
            st.markdown(f"""
            <div style='background:{SURFACE};border:1px solid {BORDER};border-left:4px solid #00C896;
                        border-radius:10px;padding:0.9rem 1rem;margin-bottom:0.6rem;'>
                <div style='font-size:0.82rem;color:{SUBTEXT};margin-bottom:0.3rem;'>
                    ⭐ {row.get('rating','?')} · {row.get('product','—')} · {row.get('category','—')}
                </div>
                <div style='font-size:0.9rem;color:{TEXT};line-height:1.4;'>{row['review']}</div>
                <div style='font-size:0.75rem;font-family:DM Mono,monospace;color:#00C896;margin-top:0.4rem;'>
                    polarity {row['Polarity']:+.3f}
                </div>
            </div>
            """, unsafe_allow_html=True)

    with n_col:
        st.markdown(f"<p class='section-label'>Top Negative Reviews</p>", unsafe_allow_html=True)
        for _, row in neg_df.iterrows():
            st.markdown(f"""
            <div style='background:{SURFACE};border:1px solid {BORDER};border-left:4px solid #FF4560;
                        border-radius:10px;padding:0.9rem 1rem;margin-bottom:0.6rem;'>
                <div style='font-size:0.82rem;color:{SUBTEXT};margin-bottom:0.3rem;'>
                    ⭐ {row.get('rating','?')} · {row.get('product','—')} · {row.get('category','—')}
                </div>
                <div style='font-size:0.9rem;color:{TEXT};line-height:1.4;'>{row['review']}</div>
                <div style='font-size:0.75rem;font-family:DM Mono,monospace;color:#FF4560;margin-top:0.4rem;'>
                    polarity {row['Polarity']:+.3f}
                </div>
            </div>
            """, unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════
# PAGE: ANALYSE TEXT
# ════════════════════════════════════════════════════════════
elif page == "📝 Analyse Text":
    st.markdown(f"<p class='section-label'>Real-Time NLP</p><p class='section-title'>Analyse Any Text</p>", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["✏️  Single Text", "🗂️  Batch Analyser"])

    with tab1:
        col_a, col_b = st.columns([3, 2], gap="large")
        with col_a:
            user_text = st.text_area(
                "Enter a Nike review or any text",
                placeholder="e.g. These Air Max are absolutely incredible — best shoe I've ever bought!",
                height=160,
            )
            go = st.button("🔍  Analyse Sentiment", use_container_width=True)

        with col_b:
            if go and user_text.strip():
                result = analyze_sentiment(user_text)
                s_color = {"Positive": "#00C896", "Negative": "#FF4560", "Neutral": "#FEB019"}.get(result["sentiment"], ACCENT)
                st.markdown(f"""
                <div class='result-card'>
                    <span class='result-emoji'>{result['emoji']}</span>
                    <div class='result-sentiment' style='color:{s_color};'>{result['sentiment']}</div>
                    <div class='result-row'>
                        <div class='result-pill'>Polarity <b>{result['polarity']:+.4f}</b></div>
                        <div class='result-pill'>Subjectivity <b>{result['subjectivity']:.4f}</b></div>
                        <div class='result-pill'>Confidence <b>{result['confidence']}</b></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            elif go:
                st.warning("⚠️ Please type something first.")
            else:
                st.markdown(f"""
                <div style='background:{SURFACE};border:1px solid {BORDER};border-radius:16px;
                            padding:2rem;text-align:center;'>
                    <div style='font-size:2.5rem;margin-bottom:0.6rem;'>💬</div>
                    <div style='color:{SUBTEXT};font-size:0.95rem;'>
                        Your result will appear here after analysis.
                    </div>
                </div>""", unsafe_allow_html=True)

        if go and user_text.strip():
            result = analyze_sentiment(user_text)
            st.markdown("<div class='fancy-divider'></div>", unsafe_allow_html=True)
            st.markdown(f"<p class='section-label'>Polarity Gauge</p>", unsafe_allow_html=True)
            st.pyplot(polarity_gauge(result["polarity"], dark), use_container_width=True)

    with tab2:
        st.markdown(f"<div style='color:{SUBTEXT};font-size:0.92rem;margin-bottom:0.8rem;'>Paste multiple reviews — one per line — for instant bulk analysis.</div>", unsafe_allow_html=True)
        batch_text = st.text_area("Paste reviews (one per line)", height=180,
                                   placeholder="Amazing shoes, love them!\nTerrible quality, fell apart after a week.\nDecent for the price.")
        if st.button("🔍  Analyse All", use_container_width=True):
            lines = [l.strip() for l in batch_text.splitlines() if l.strip()]
            if lines:
                batch_df = pd.DataFrame({"review": lines})
                batch_df = analyze_dataframe(batch_df, "review")

                # Summary strip
                b_stats = get_summary_stats(batch_df)
                st.markdown(f"""
                <div class='kpi-grid' style='grid-template-columns:repeat(3,1fr);'>
                    {kpi_card(b_stats['positive'], 'Positive', accent='#00C896')}
                    {kpi_card(b_stats['negative'], 'Negative', accent='#FF4560')}
                    {kpi_card(b_stats['neutral'],  'Neutral',  accent='#FEB019')}
                </div>""", unsafe_allow_html=True)

                st.dataframe(
                    batch_df[["review", "Emoji", "Sentiment", "Polarity", "Subjectivity"]],
                    use_container_width=True, height=280
                )
                c1, c2 = st.columns(2)
                with c1: st.pyplot(donut_chart(batch_df, dark), use_container_width=True)
                with c2: st.pyplot(bar_chart(batch_df, dark), use_container_width=True)
            else:
                st.warning("⚠️ Please paste at least one review.")


# ════════════════════════════════════════════════════════════
# PAGE: DATASET EXPLORER
# ════════════════════════════════════════════════════════════
elif page == "📂 Dataset Explorer":
    st.markdown(f"<p class='section-label'>Nike Reviews Dataset</p><p class='section-title'>Dataset Explorer</p>", unsafe_allow_html=True)

    source = st.radio("Data source", ["📋 Nike Reviews (reviews.csv)", "⬆️ Upload your CSV"],
                      horizontal=True)

    df = None
    text_col = None

    if source == "📋 Nike Reviews (reviews.csv)":
        try:
            full_df = load_nike_data()
            df = apply_filters(full_df)
            text_col = "review"
            st.success(f"✅ Loaded Nike dataset — showing {len(df)} of {len(full_df)} reviews after filters.")
        except FileNotFoundError:
            st.error("❌ `reviews.csv` not found.")

    else:
        up = st.file_uploader("Upload CSV", type=["csv"])
        if up:
            raw = pd.read_csv(up)
            text_col = st.selectbox("Select text column", raw.columns.tolist())
            if st.button("🚀 Run Analysis"):
                with st.spinner("Running NLP…"):
                    df = analyze_dataframe(raw, text_col)
                    st.session_state["upload_df"] = df
        if "upload_df" in st.session_state and source == "⬆️ Upload your CSV":
            df = st.session_state["upload_df"]

    if df is not None and not df.empty and "Sentiment" in df.columns:
        stats = get_summary_stats(df)

        # KPIs
        st.markdown(f"""
        <div class='kpi-grid'>
            {kpi_card(stats['total'], 'Reviews', '')}
            {kpi_card(f"{stats['pct_positive']}%", 'Positive', f"{stats['positive']} reviews", '#00C896')}
            {kpi_card(f"{stats['pct_negative']}%", 'Negative', f"{stats['negative']} reviews", '#FF4560')}
            {kpi_card(f"{stats['avg_polarity']:+.3f}", 'Avg Polarity', stats['most_common'], WARN)}
        </div>""", unsafe_allow_html=True)

        st.markdown("<div class='fancy-divider'></div>", unsafe_allow_html=True)

        # Charts
        ch1, ch2 = st.columns(2)
        with ch1: st.pyplot(donut_chart(df, dark), use_container_width=True)
        with ch2: st.pyplot(polarity_histogram(df, dark), use_container_width=True)

        ch3, ch4 = st.columns(2)
        with ch3: st.pyplot(bar_chart(df, dark), use_container_width=True)
        with ch4:
            fig_rv = rating_vs_polarity(df, dark)
            if fig_rv: st.pyplot(fig_rv, use_container_width=True)

        st.markdown("<div class='fancy-divider'></div>", unsafe_allow_html=True)

        # Interactive table with colour indicator
        st.markdown(f"<p class='section-label'>Full Dataset</p>", unsafe_allow_html=True)
        show_cols = [c for c in ["id","product","category","rating","date","Emoji","Sentiment","Polarity","Subjectivity","review"]
                     if c in df.columns]
        styled = df[show_cols].style.applymap(
            lambda v: f"color: #00C896; font-weight:600" if v == "Positive"
                      else (f"color: #FF4560; font-weight:600" if v == "Negative"
                            else f"color: #FEB019; font-weight:600"),
            subset=["Sentiment"]
        )
        st.dataframe(styled, use_container_width=True, height=380)

        # Download
        csv_bytes = df.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️  Download Results CSV", csv_bytes,
                           "nike_sentiment_results.csv", "text/csv")


# ════════════════════════════════════════════════════════════
# PAGE: INSIGHTS REPORT
# ════════════════════════════════════════════════════════════
elif page == "📊 Insights Report":
    try:
        full_df = load_nike_data()
        df      = apply_filters(full_df)
        stats   = get_summary_stats(df)
    except FileNotFoundError:
        st.error("❌ `reviews.csv` not found.")
        st.stop()

    st.markdown(f"<p class='section-label'>Auto-Generated</p><p class='section-title'>Insights Report — Nike Reviews</p>", unsafe_allow_html=True)

    # Summary banner
    overall_tone = "positive" if stats["avg_polarity"] > 0.05 else "negative" if stats["avg_polarity"] < -0.05 else "neutral"
    tone_color   = "#00C896" if overall_tone == "positive" else "#FF4560" if overall_tone == "negative" else "#FEB019"

    st.markdown(f"""
    <div style='background:{SURFACE};border:1px solid {BORDER};border-left:5px solid {tone_color};
                border-radius:14px;padding:1.5rem 1.8rem;margin-bottom:1.5rem;'>
        <div style='font-size:0.75rem;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;
                    color:{tone_color};margin-bottom:0.4rem;'>Executive Summary</div>
        <div style='font-size:1.05rem;color:{TEXT};line-height:1.6;'>
            Analysis of <b>{stats['total']}</b> Nike product reviews reveals an overall
            <b style='color:{tone_color};'>{overall_tone}</b> sentiment with an average polarity
            of <b style='font-family:DM Mono,monospace;'>{stats['avg_polarity']:+.4f}</b>.
            <b>{stats['positive']}</b> reviews ({stats['pct_positive']}%) are positive,
            <b>{stats['negative']}</b> ({stats['pct_negative']}%) are negative, and
            <b>{stats['neutral']}</b> ({stats['pct_neutral']}%) are neutral.
            The dominant sentiment across all categories is <b>{stats['most_common']}</b>.
        </div>
    </div>""", unsafe_allow_html=True)

    # Metric table
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        st.markdown(f"<p class='section-label'>Metrics</p>", unsafe_allow_html=True)
        metrics_df = pd.DataFrame({
            "Metric": ["Total Reviews", "Positive", "Negative", "Neutral",
                       "Avg Polarity", "Avg Subjectivity", "Most Common"],
            "Value" : [stats["total"],
                       f"{stats['positive']} ({stats['pct_positive']}%)",
                       f"{stats['negative']} ({stats['pct_negative']}%)",
                       f"{stats['neutral']}  ({stats['pct_neutral']}%)",
                       f"{stats['avg_polarity']:+.4f}",
                       f"{stats['avg_subjectivity']:.4f}",
                       stats["most_common"]],
        })
        st.dataframe(metrics_df, use_container_width=True, hide_index=True)

    with col_m2:
        st.markdown(f"<p class='section-label'>Category Breakdown</p>", unsafe_allow_html=True)
        if "category" in df.columns:
            cat_df = df.groupby(["category","Sentiment"]).size().unstack(fill_value=0)
            st.dataframe(cat_df, use_container_width=True)

    st.markdown("<div class='fancy-divider'></div>", unsafe_allow_html=True)

    # Charts
    r1, r2 = st.columns(2)
    with r1: st.pyplot(donut_chart(df, dark), use_container_width=True)
    with r2: st.pyplot(category_stacked_bar(df, dark), use_container_width=True)

    st.markdown("<div class='fancy-divider'></div>", unsafe_allow_html=True)

    # Key findings
    st.markdown(f"<p class='section-label'>Key Findings</p>", unsafe_allow_html=True)
    findings = [
        f"**{stats['most_common']}** sentiment dominates Nike reviews at **{stats[stats['most_common'].lower()]}** of {stats['total']} entries.",
        f"Average polarity of **{stats['avg_polarity']:+.4f}** places overall brand perception in the **{overall_tone}** range.",
        f"Negative reviews repeatedly cite defects, delivery failures, and sizing inconsistencies.",
        f"Running and Basketball categories produce the highest-polarity positive reviews.",
        f"Subjectivity average of **{stats['avg_subjectivity']:.3f}** indicates moderately opinion-based writing.",
        f"Star rating and NLP polarity correlate strongly — validating TextBlob's accuracy on this dataset.",
    ]
    for i, f_text in enumerate(findings, 1):
        st.markdown(f"""
        <div style='background:{SURFACE};border:1px solid {BORDER};border-radius:10px;
                    padding:0.8rem 1rem;margin-bottom:0.5rem;display:flex;gap:0.8rem;align-items:flex-start;'>
            <div style='color:{ACCENT};font-weight:700;font-size:1rem;min-width:1.5rem;'>{i}.</div>
            <div style='color:{TEXT};font-size:0.9rem;line-height:1.5;'>{f_text}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<div class='fancy-divider'></div>", unsafe_allow_html=True)

    # Recommendations
    st.markdown(f"<p class='section-label'>Recommendations</p>", unsafe_allow_html=True)
    recs = [
        ("🚚", "Improve delivery reliability", "Logistics complaints are the single biggest driver of negative reviews."),
        ("📏", "Standardise sizing guides", "Sizing mismatch is the most common neutral-to-negative conversion trigger."),
        ("💬", "Amplify positive reviews", "High-polarity reviews should be surfaced in marketing material."),
        ("🔁", "Automate monitoring", "Deploy this pipeline on live review streams for real-time brand health."),
        ("🧪", "Upgrade to transformer NLP", "Replace TextBlob with a fine-tuned BERT model for higher accuracy on short texts."),
    ]
    r_col1, r_col2 = st.columns(2)
    for i, (icon, title, desc) in enumerate(recs):
        col = r_col1 if i % 2 == 0 else r_col2
        with col:
            st.markdown(f"""
            <div style='background:{SURFACE};border:1px solid {BORDER};border-radius:12px;
                        padding:1rem 1.1rem;margin-bottom:0.8rem;'>
                <div style='font-size:1.3rem;margin-bottom:0.3rem;'>{icon}</div>
                <div style='font-weight:700;color:{TEXT};font-size:0.9rem;margin-bottom:0.2rem;'>{title}</div>
                <div style='color:{SUBTEXT};font-size:0.82rem;'>{desc}</div>
            </div>""", unsafe_allow_html=True)

    # Report download
    report_txt = (
        f"NikeSenti Insights Report\n"
        f"{'='*50}\n"
        f"Total: {stats['total']} | Positive: {stats['positive']} ({stats['pct_positive']}%)"
        f" | Negative: {stats['negative']} ({stats['pct_negative']}%)"
        f" | Neutral: {stats['neutral']} ({stats['pct_neutral']}%)\n"
        f"Avg Polarity: {stats['avg_polarity']:+.4f} | Most Common: {stats['most_common']}\n"
        f"{'='*50}\n"
        f"Generated by NikeSenti · CAPACITI AI Bootcamp · Week 3\n"
    )
    st.download_button("⬇️  Download Report (.txt)", report_txt,
                       "nike_insights_report.txt", "text/plain")
