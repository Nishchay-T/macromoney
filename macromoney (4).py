import streamlit as st
import pandas as pd
import numpy as np

# ---------------- CONFIG ---------------- #
st.set_page_config(
    page_title="MacroMoney",
    layout="wide",
)

# ---------------- UI HEADER ---------------- #
st.markdown("""
# 📊 MacroMoney  
**Macro-aware portfolio intelligence (Demo)**  

Understand how global events *should* affect your portfolio.
""")

# ---------------- USER INPUTS ---------------- #
st.sidebar.header("Investor Profile")

capital = st.sidebar.number_input(
    "💰 Capital Amount ($)",
    min_value=1000,
    step=1000,
    value=10000
)

time_horizon = st.sidebar.selectbox(
    "⏳ Investment Horizon",
    ["< 1 year", "1–3 years", "> 3 years"]
)

risk_tolerance = st.sidebar.selectbox(
    "⚖️ Risk Tolerance",
    ["Low", "Medium", "High"]
)

st.sidebar.markdown("---")

st.sidebar.header("Asset Allocation (%)")

assets = ["Equities", "Bonds", "Gold", "Crypto", "Commodities", "ETFs"]
weights = {}

for asset in assets:
    weights[asset] = st.sidebar.slider(asset, 0, 100, int(100/len(assets)))

# Normalize weights
total_weight = sum(weights.values())
weights = {k: v/total_weight for k, v in weights.items()}

# ---------------- NEWS INPUT ---------------- #
st.markdown("## 📰 Enter News Headline")
news = st.text_input(
    "Paste a market-related news headline",
    placeholder="Example: Gold prices hit all-time high amid geopolitical tensions"
)

# ---------------- MACRO INTELLIGENCE ---------------- #

macro_event_map = {
    "geopolitical": ["assassination", "war", "conflict", "attack", "military"],
    "monetary": ["interest rate", "inflation", "fed", "central bank"],
    "commodity": ["gold", "oil", "commodity", "prices hit"],
    "corporate": ["earnings", "profit", "loss", "quarter"],
    "political": ["election", "prime minister", "president", "resigns"],
}

asset_sensitivity = {
    "Equities": {"geopolitical": 0.8, "monetary": 0.9, "commodity": 0.4, "corporate": 1.0, "political": 0.7},
    "Bonds": {"geopolitical": 0.6, "monetary": 1.0, "commodity": 0.3, "corporate": 0.2, "political": 0.6},
    "Gold": {"geopolitical": 1.0, "monetary": 0.7, "commodity": 1.0, "corporate": 0.1, "political": 0.8},
    "Crypto": {"geopolitical": 0.5, "monetary": 0.8, "commodity": 0.2, "corporate": 0.3, "political": 0.6},
    "Commodities": {"geopolitical": 0.7, "monetary": 0.5, "commodity": 1.0, "corporate": 0.2, "political": 0.6},
    "ETFs": {"geopolitical": 0.7, "monetary": 0.8, "commodity": 0.5, "corporate": 0.6, "political": 0.6},
}

severity_keywords = {
    "major": ["assassinated", "war", "invasion", "crisis"],
    "medium": ["hits", "surge", "fall", "cuts", "raises"],
    "mild": ["reports", "announces", "expects"]
}

def detect_macro_event(text):
    text = text.lower()
    detected = []
    for theme, keywords in macro_event_map.items():
        if any(k in text for k in keywords):
            detected.append(theme)
    return detected

def detect_severity(text):
    text = text.lower()
    for level, keys in severity_keywords.items():
        if any(k in text for k in keys):
            return level
    return "mild"

severity_multiplier = {
    "mild": 0.5,
    "medium": 1.0,
    "major": 1.5
}

horizon_threshold = {
    "< 1 year": 0.3,
    "1–3 years": 0.6,
    "> 3 years": 0.9
}

# ---------------- ANALYSIS ---------------- #
if news:
    themes = detect_macro_event(news)
    severity = detect_severity(news)

    if not themes:
        st.warning("🚫 This appears to be **local or irrelevant news**. No macro impact detected.")
    else:
        st.success(f"📌 Detected Macro Themes: **{', '.join(themes)}**")
        st.info(f"⚠️ Severity Level: **{severity.upper()}**")

        impact_scores = {}

        for asset in assets:
            sensitivity = np.mean([asset_sensitivity[asset][t] for t in themes])
            impact = sensitivity * severity_multiplier[severity]
            impact_scores[asset] = impact

        overall_impact = np.mean(list(impact_scores.values()))

        st.markdown("### 📈 Asset Impact Scores")
        df = pd.DataFrame.from_dict(impact_scores, orient="index", columns=["Impact Score"])
        st.bar_chart(df)

        if overall_impact >= horizon_threshold[time_horizon]:
            st.success("✅ **Rebalancing Recommended** based on your time horizon.")
        else:
            st.warning("ℹ️ Impact detected, but **not strong enough** to rebalance for your horizon.")

# ---------------- FOOTER ---------------- #
st.markdown("---")
st.caption("MacroMoney • Demo Version • No real trades executed")
