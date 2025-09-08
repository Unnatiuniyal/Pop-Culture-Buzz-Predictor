import streamlit as st
import pandas as pd
import plotly.express as px
from prophet import Prophet

# -----------------------------
# Page setup
# -----------------------------
st.set_page_config(page_title="PopBuzz Dashboard", layout="wide")

st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://ludo.ai/wp-content/uploads/2022/06/Pop-culture-video-game-header.jpg");
        background-size: cover;
        background-attachment: fixed;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("📊 Pop Culture Buzz Predictor")

# -----------------------------
# Load data (from data/ folder)
# -----------------------------
df = pd.read_csv("data/google_trends_clean.csv")
df["date"] = pd.to_datetime(df["date"], dayfirst=True, errors="coerce")

df_flags = pd.read_csv("data/google_trends_spike_flags.csv")
df_flags["date"] = pd.to_datetime(df_flags["date"], dayfirst=True, errors="coerce")

# Drop bad rows if any
df = df.dropna(subset=["date"])
df_flags = df_flags.dropna(subset=["date"])

artists = [c for c in df.columns if c != "date"]

# -----------------------------
# Sidebar controls
# -----------------------------
artist = st.sidebar.selectbox("Choose artist/show", artists)
horizon = st.sidebar.slider("Forecast horizon (weeks)", 4, 52, 12)
show_share = st.sidebar.checkbox("Show Relative Buzz Share (%)", value=False)
conclusion = st.sidebar.text_area("📝 Conclusion (summary)", "Add final thoughts here...")

# -----------------------------
# Historical + spikes
# -----------------------------
fig_hist = px.line(df, x="date", y=artist, title=f"Buzz Over Time — {artist}")
spikes = df_flags[df_flags[artist] == True]
fig_hist.add_scatter(
    x=spikes["date"],
    y=df.loc[df["date"].isin(spikes["date"]), artist],
    mode="markers",
    marker=dict(size=10, color="red", symbol="star"),
    name="Spikes ⚡"
)
st.plotly_chart(fig_hist, use_container_width=True)

# -----------------------------
# Forecast with Prophet
# -----------------------------
s = df[["date", artist]].rename(columns={"date": "ds", artist: "y"})
s = s.dropna(subset=["ds"])
s["y"] = s["y"].clip(lower=0)

m = Prophet(weekly_seasonality=True, yearly_seasonality=False, changepoint_prior_scale=0.5)
m.fit(s)

future = m.make_future_dataframe(periods=horizon, freq="W")
fcst = m.predict(future)

fig_fcst = px.line(fcst, x="ds", y="yhat", title=f"Forecast — {artist} ({horizon} weeks)")
fig_fcst.add_scatter(x=s["ds"], y=s["y"], mode="lines", name="History")
fig_fcst.add_scatter(x=fcst["ds"], y=fcst["yhat_lower"], mode="lines", line=dict(dash="dot"), name="Lower Bound")
fig_fcst.add_scatter(x=fcst["ds"], y=fcst["yhat_upper"], mode="lines", line=dict(dash="dot"), name="Upper Bound")
st.plotly_chart(fig_fcst, use_container_width=True)

# -----------------------------
# Relative Buzz Share
# -----------------------------
if show_share:
    df_share = df.copy()
    df_share[artists] = df_share[artists].div(df_share[artists].sum(axis=1), axis=0) * 100
    fig_share = px.area(df_share, x="date", y=artists, title="Relative Buzz Share (%)")
    st.plotly_chart(fig_share, use_container_width=True)

# -----------------------------
# Insights Section
# -----------------------------
artist_insights = {
    "Rihanna": "🔺 Buzz: Strong spikes around Fenty launches & appearances. | 💼 Biz: Ideal for product tie-ins timed to drops or fashion events.",
    "Taylor Swift": "🎤 Buzz: Tour announcements drive massive peaks, steady year-round baseline. | 💼 Biz: Best for long-term brand partnerships with event amplification.",
    "Blackpink": "🔥 Buzz: Comeback teasers fuel sharp international surges. | 💼 Biz: High ROI on global campaigns, especially in Asia and touring windows.",
    "BTS": "📈 Buzz: Enlistment/reunion news sparks spikes; fanbase sustains buzz. | 💼 Biz: Reliable long-term engagement; perfect for global loyalty campaigns.",
    "Kendrick Lamar": "🎶 Buzz: Steady niche presence with low volatility. | 💼 Biz: Great for culturally rooted, authenticity-driven brand collaborations.",
    "Travis Scott": "🌍 Buzz: Early 2025 tour + WWE drove spikes, volatility from controversies. | 💼 Biz: Strong short-term marketing play, but risk-sensitive alignment needed.",
    "Doja Cat": "🐆 Buzz: Modest, stable presence; overlaps with TV/film buzz cycles. | 💼 Biz: Works well for cross-media, fashion-forward campaigns.",
    "Olivia Rodrigo": "💜 Buzz: Early 2025 peak from GUTS tour + album teasers. | 💼 Biz: Strong youth engagement—ideal for Gen Z-focused launches.",
    "Zendaya": "⭐ Buzz: Stable mid-tier popularity, boosted by film/TV roles. | 💼 Biz: Consistent brand partner, especially in luxury and fashion markets.",
    "Jenna Ortega": "📺 Buzz: Major spikes around 'Wednesday' Season 2 and new films. | 💼 Biz: Strong crossover potential—youth brands, streaming tie-ins.",
    "Wednesday": "🦇 Buzz: Tightly linked with Ortega; Season 2 drove massive spikes. | 💼 Biz: Great for entertainment collabs & seasonal campaigns (Halloween, fall).",
    "Stranger Things": "👾 Buzz: Explosive late 2025 spikes from Season 5; strong global fanbase. | 💼 Biz: Best for blockbuster tie-ins, retro/cultural nostalgia campaigns."
}

st.subheader(f"🔍 Insights — {artist}")
st.write(artist_insights.get(artist, "No insights added yet."))

