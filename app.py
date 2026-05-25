# STREAMLIT

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import json


st.set_page_config(
    page_title="SpotifyDNA",
    page_icon="🎧",
    layout="wide",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    color: #2b2b2b;
}

h1,h2,h3,h4 {
    font-family: 'Syne', sans-serif;
    color: #2b2b2b;
}

.stApp {
    background: linear-gradient(135deg, #fff7fb 0%, #f3f8ff 50%, #f7fff9 100%);
    min-height: 100vh;
}

/* Soft cards */
.metric-card {
    background: rgba(255,255,255,0.7);
    border: 1px solid rgba(0,0,0,0.05);
    border-radius: 18px;
    padding: 1.3rem 1.5rem;
    margin-bottom: 1rem;
    box-shadow: 0 6px 20px rgba(0,0,0,0.05);
}

/* Metrics */
div[data-testid="stMetricValue"] {
    color: #6c63ff !important;
    font-family: 'Syne', sans-serif;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #ffffff !important;
    border-right: 1px solid rgba(0,0,0,0.05);
}

/* Buttons */
.stButton button {
    background: linear-gradient(90deg, #ffb6c1, #a0c4ff) !important;
    border: none !important;
    color: white !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
}

.stButton button:hover {
    transform: scale(1.02);
}

/* Tabs */
.stTabs [aria-selected="true"] {
    color: #ff6f91 !important;
}

/* Hide noise */
footer { visibility: hidden; }
#MainMenu { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# ─── Sidebar ────────────────────────────────────────────────────────────────
with st.sidebar:

    st.markdown("### Upload Data")

    uploaded_files = st.file_uploader(
        "Files",
        type=["json", "csv"],
        accept_multiple_files=True
    )

st.image('Spotify Snip.png')

# ─── APP TITLE ───────────────────────────────────────────────────────────────
st.title("🎵 Spotify Analytics App")

st.markdown("""
### 🎧 Discover Your SpotifyDNA

Dive deep into your listening behavior and uncover the patterns behind your music taste.

Analyze:
- 🎵 Listening habits & streaming trends
- 🌙 Productivity and peak listening hours
- 🧠 Listening personality & music archetypes
- 🎤 Artist loyalty vs music exploration
- 📈 Taste evolution over time
- 🔥 Top artists, albums, and tracks
- 🎶 Mood and listening consistency

### 📥 How to Get Your Spotify Data

1. Open Spotify
2. Go to:
   **Account → Privacy Settings**
3. Scroll to:
   **Download your data**
4. Request your **Extended Streaming History**
5. Spotify will email you your data when it's ready
   (this may take a few days)
6. Download the ZIP file
7. Upload the JSON files here and let SpotifyDNA do the rest ✨

""")

# ─── DATA LOADING ────────────────────────────────────────────────────────────
@st.cache_data
def load_data(files):
    all_data = []

    for file in files:
        if file.name.endswith(".json"):
            data = json.load(file)
            temp_df = pd.DataFrame(data)
        else:
            temp_df = pd.read_csv(file)

        all_data.append(temp_df)

    return pd.concat(all_data, ignore_index=True)


def clean_data(df):
    df = df.copy()

    df['ts'] = pd.to_datetime(df['ts'], errors='coerce')
    df = df.drop_duplicates()
    df = df[df['ms_played'] > 30000]

    df['hour'] = df['ts'].dt.hour
    df['day'] = df['ts'].dt.day_name()
    df['month'] = df['ts'].dt.month_name()
    df['year'] = df['ts'].dt.year

    df['minutes_played'] = df['ms_played'] / 60000

    return df


# ─── FILE UPLOAD ─────────────────────────────────────────────────────────────
df = None

if uploaded_files:
    raw_df = load_data(uploaded_files)
    df = clean_data(raw_df)
    st.success("Data loaded successfully")


if df is not None and len(df) > 0:

    st.subheader("✨ Your Listening Identity")


    total_streams = len(df)
    unique_artists = df['master_metadata_album_artist_name'].nunique()
    total_hours = round(df['minutes_played'].sum()/60, 2)

    col1, col2, col3 = st.columns(3)

    col1.markdown(f"""
    <div style="background:rgba(255,255,255,0.7);
    padding:18px;border-radius:16px;text-align:center;
    box-shadow:0 6px 18px rgba(0,0,0,0.05)">
    🎧<br><h3>{total_streams}</h3><p>Total Streams</p>
    </div>
    """, unsafe_allow_html=True)

    col2.markdown(f"""
    <div style="background:rgba(255,255,255,0.7);
    padding:18px;border-radius:16px;text-align:center;
    box-shadow:0 6px 18px rgba(0,0,0,0.05)">
    🎤<br><h3>{unique_artists}</h3><p>Unique Artists</p>
    </div>
    """, unsafe_allow_html=True)

    col3.markdown(f"""
    <div style="background:rgba(255,255,255,0.7);
    padding:18px;border-radius:16px;text-align:center;
    box-shadow:0 6px 18px rgba(0,0,0,0.05)">
    ⏳<br><h3>{total_hours}</h3><p>Total Hours</p>
    </div>
    """, unsafe_allow_html=True)


    # ─── TOP ARTISTS ───────────────────────────────────────
    st.markdown("### 🎤 Top Artists You Can’t Escape")

    artist_df = (
        df.groupby("master_metadata_album_artist_name")["minutes_played"]
        .sum()
        .sort_values(ascending=False)
        .head(5)
    )

    for artist, mins in artist_df.items():
        st.markdown(f"""
        <div style="
            background: rgba(255,255,255,0.75);
            padding: 12px 16px;
            border-radius: 14px;
            margin-bottom: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
            font-size: 16px;">
            🎧 <b>{artist}</b><br>
            <span style="color:#6c63ff;">{round(mins/60, 1)} hours with you</span>
        </div>
        """, unsafe_allow_html=True)


    # ─── TOP TRACKS────────────────────────────────────────
    st.markdown("### 🎶 Tracks Living in Your Head Rent-Free")

    track_df = (
        df.groupby("master_metadata_track_name")["minutes_played"]
        .sum()
        .sort_values(ascending=False)
        .head(5)
    )

    for track, mins in track_df.items():
        st.markdown(f"""
        <div style="
            background: rgba(255,255,255,0.75);
            padding: 12px 16px;
            border-radius: 14px;
            margin-bottom: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
            font-size: 16px;">
            🎵 <b>{track}</b><br>
            <span style="color:#ff6f91;">{round(mins, 1)} min played</span>
        </div>
        """, unsafe_allow_html=True)


    # ─── TASTE EVOLUTION─────────────────────
    st.markdown("### 📈 Your Taste Evolution (Top 5 Artists)")

    df["year_month"] = df["ts"].dt.to_period("M").astype(str)

    monthly_artists = (
        df.groupby(["year_month", "master_metadata_album_artist_name"])
        .size()
        .reset_index(name="streams")
    )

    top5 = df["master_metadata_album_artist_name"].value_counts().head(5).index

    monthly_artists = monthly_artists[
        monthly_artists["master_metadata_album_artist_name"].isin(top5)
    ]

    fig = px.line(
        monthly_artists,
        x="year_month",
        y="streams",
        color="master_metadata_album_artist_name",
        title=""
    )

    st.plotly_chart(fig, use_container_width=True)

    # ─── PERSONALITY ────────────────────────────────────────────────────────

    def build_listening_features(df: pd.DataFrame) -> dict:
        df = df.copy()

        unique_artists = df["master_metadata_album_artist_name"].nunique()
        total_streams = len(df)
        diversity_score = unique_artists / total_streams if total_streams else 0

        morning = df[(df["hour"] >= 5) & (df["hour"] < 11)]["minutes_played"].sum()
        day = df[(df["hour"] >= 11) & (df["hour"] < 17)]["minutes_played"].sum()
        night = df[(df["hour"] >= 17) | (df["hour"] < 5)]["minutes_played"].sum()

        skip_rate = df["skipped"].mean() if "skipped" in df.columns else 0
        avg_ms_played = df["ms_played"].mean()

        early_skip_rate = (
            df[(df["skipped"] == True) & (df["ms_played"] < 30000)].shape[0] / len(df)
            if "skipped" in df.columns and len(df) else 0
        )

        long_listen_rate = (
            df[df["ms_played"] > 120000].shape[0] / len(df)
            if len(df) else 0
        )

        return {
            "diversity_score": diversity_score,
            "morning": morning,
            "day": day,
            "night": night,
            "skip_rate": skip_rate,
            "avg_ms_played": avg_ms_played,
            "early_skip_rate": early_skip_rate,
            "long_listen_rate": long_listen_rate
        }


    def classify_core_traits(f: dict) -> list:
        traits = []

        if f["diversity_score"] > 0.15:
            traits.append("🗺️ Explorer")
        else:
            traits.append("💎 Loyalist")

        if f["skip_rate"] < 0.15 and f["long_listen_rate"] > 0.4:
            traits.append("🎯 Deep Listener")
        elif f["skip_rate"] > 0.4 and f["early_skip_rate"] > 0.3:
            traits.append("⚡ Picky Listener")
        else:
            traits.append("🎲 Casual Listener")

        if f["morning"] >= f["day"] and f["morning"] >= f["night"]:
            traits.append("🌅 Morning Listener")
        elif f["day"] >= f["morning"] and f["day"] >= f["night"]:
            traits.append("☀️ Day Listener")
        else:
            traits.append("🌙 Night Listener")

        return traits


    def assign_archetype(traits: list) -> tuple:
        archetypes = [
            (["🗺️ Explorer", "🌙 Night Listener"],
             "Midnight Voyager",
             "You wander through music like a city at 3am, always searching for that song that hits different."),

            (["💎 Loyalist", "🎯 Deep Listener"],
             "The Obsessive Fan",
             "You find your people and ride with them. When you love a song, you LOVE it, playlists on repeat."),

            (["🗺️ Explorer", "☀️ Day Listener"],
              "The Curated Optimist",
              "You soundtrack your days with intention. "
              "Broad taste, bright energy, you probably have a playlist for every mood."),

            (["⚡ Picky Listener", "🗺️ Explorer"],
              "The Taste Architect",
             "High standards, wide radar. "
             "You're curating the perfect soundtrack and you know instantly when something doesn't belong."),

            (["💎 Loyalist", "🌙 Night Listener"],
             "The Midnight Devotee",
             "Late nights with the same familiar sounds. Music as ritual, not background noise.")
        ]

        for match_traits, name, desc in archetypes:
            if all(t in traits for t in match_traits):
                return name, desc

        return "The Audiophile", "Your listening style is layered and unique."


    def generate_personality(df: pd.DataFrame):
        features = build_listening_features(df)
        traits = classify_core_traits(features)
        name, desc = assign_archetype(traits)

        return {
            "traits": traits,
            "archetype": name,
            "description": desc
        }

    results = generate_personality(df)

    st.markdown("### 🎵 Your Music DNA")
    st.markdown("### 🎵 Your Music DNA")

    import time 

    st.markdown("<br>", unsafe_allow_html=True)

    # ANALYSIS LOADING
    with st.spinner("🔍 Analyzing your listening behavior..."):
        time.sleep(2)

    st.markdown("<br>", unsafe_allow_html=True)

# ARCHETYPE
    st.markdown(f"""
    <div style="
    background: linear-gradient(135deg, #1DB954, #121212);
    padding: 40px;
    border-radius: 30px;
    color: white;
    box-shadow: 0 10px 30px rgba(0,0,0,0.4);
    text-align: center;
    margin-bottom: 30px;
    ">

    <h3 style="
    letter-spacing:2px;
    color:#dcdcdc;
    margin-bottom:10px;
    ">
    YOUR SPOTIFY DNA
    </h3>

    <h1 style="
    font-size:50px;
    margin-bottom:20px;
    ">
    {results["archetype"]}
    </h1>

    <p style="
    font-size:20px;
    line-height:1.8;
    color:#e0e0e0;
    max-width:700px;
    margin:auto;
    ">
    {results["description"]}
    </p>

    </div>
    """, unsafe_allow_html=True)

# TRAITS
    st.markdown("""
    <h2 style='margin-bottom:20px;'>
    🧠 Your Listening Traits
    </h2>
    """, unsafe_allow_html=True)

    st.write("**Traits:**")
    for t in results["traits"]:
        st.write(f"• {t}")

        st.markdown(f"""
        <div style="
        background-color:#181818;
        padding:18px;
        border-radius:18px;
        margin-bottom:15px;
        text-align:center;
        color:white;
        font-size:17px;
        font-weight:600;
        border:1px solid rgba(255,255,255,0.08);
        box-shadow: 0 4px 10px rgba(0,0,0,0.2);
        ">
        {t}
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

# EXTRA INSIGHT 
    st.markdown(f"""
    <div style="
    background-color:#111111;
    padding:25px;
    border-radius:25px;
    border:1px solid rgba(255,255,255,0.08);
    ">

    <h3 style='color:white;'>
    🎵 Personality Insight
    </h3>

    <p style="
    color:#d3d3d3;
    font-size:17px;
    line-height:1.8;
    ">
    Your listening history suggests consistent behavioral patterns in how
    you engage with music, from the artists you revisit to the hours you
    listen most. Your SpotifyDNA reflects not just what you play,
    but how you experience music emotionally and behaviorally.
    </p>

    </div>
    """, unsafe_allow_html=True)

 
    st.balloons()
  

else:
    st.warning("Upload your Spotify files to begin analysis")