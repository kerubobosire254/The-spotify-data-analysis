"""
SpotifyDNA — Listening Behavior Intelligence
=============================================
Transforms raw Spotify streaming history into a behavioral profile.
Supports JSON upload (from Spotify's data export) and a built-in demo mode.

Requirements:
    pip install streamlit pandas numpy plotly
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import json
from datetime import datetime, timedelta

# ─── PAGE CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SpotifyDNA",
    page_icon="🎧",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── THEME (LIGHT) ────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;0,600;1,400&display=swap');

  html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
  h1, h2, h3, h4 { font-family: 'Syne', sans-serif; }

  .stApp {
    background-color: #f5f5f0;
    color: #1a1a1a;
  }

  /* ── Sidebar ── */
  [data-testid="stSidebar"] {
    background-color: #ffffff !important;
    border-right: 1px solid #e0e0e0;
  }
  [data-testid="stSidebar"] label,
  [data-testid="stSidebar"] p,
  [data-testid="stSidebar"] span { color: #555555 !important; }

  /* ── Tabs ── */
  .stTabs [data-baseweb="tab-list"] {
    gap: 4px;
    background-color: #ebebeb;
    border-radius: 12px;
    padding: 4px;
    border: 1px solid #d5d5d5;
  }
  .stTabs [data-baseweb="tab"] {
    color: #888888;
    font-family: 'DM Sans', sans-serif;
    font-size: 13px;
    font-weight: 500;
    border-radius: 8px;
    padding: 8px 18px;
  }
  .stTabs [aria-selected="true"] {
    background-color: #1DB954 !important;
    color: #000000 !important;
    font-weight: 600 !important;
  }

  /* ── Metric override ── */
  div[data-testid="stMetric"] {
    background: #ffffff;
    border: 1px solid #e0e0e0;
    border-radius: 14px;
    padding: 16px 20px;
  }
  div[data-testid="stMetric"] label {
    color: #888888 !important;
    font-size: 11px !important;
    font-family: 'DM Sans', monospace !important;
    text-transform: uppercase !important;
    letter-spacing: 0.1em !important;
  }
  div[data-testid="stMetricValue"] {
    color: #1DB954 !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 28px !important;
  }

  /* ── Stat card ── */
  .stat-card {
    background: #ffffff;
    border: 1px solid #e0e0e0;
    border-radius: 14px;
    padding: 20px 24px;
    text-align: center;
  }
  .stat-label {
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: #888888;
    margin-bottom: 8px;
  }
  .stat-value {
    font-family: 'Syne', sans-serif;
    font-size: 32px;
    font-weight: 700;
    color: #1DB954;
  }
  .stat-sub {
    font-size: 12px;
    color: #aaaaaa;
    margin-top: 4px;
  }

  /* ── Archetype card ── */
  .archetype-card {
    background: linear-gradient(135deg, #e8f7ee 0%, #d4f0e0 50%, #c5ebd4 100%);
    border: 1px solid #1DB954;
    border-radius: 24px;
    padding: 48px 40px;
    text-align: center;
    position: relative;
    overflow: hidden;
  }
  .archetype-card::before {
    content: '';
    position: absolute;
    top: -60%;
    left: 50%;
    transform: translateX(-50%);
    width: 500px;
    height: 500px;
    background: radial-gradient(circle, rgba(29,185,84,0.12) 0%, transparent 65%);
  }
  .archetype-eyebrow {
    font-size: 10px;
    letter-spacing: 0.3em;
    text-transform: uppercase;
    color: #1DB954;
    margin-bottom: 16px;
    font-family: 'DM Sans', monospace;
  }
  .archetype-name {
    font-family: 'Syne', sans-serif;
    font-size: 52px;
    font-weight: 800;
    color: #1a1a1a;
    line-height: 1.1;
    margin-bottom: 20px;
  }
  .archetype-desc {
    font-size: 16px;
    line-height: 1.7;
    color: #444444;
    max-width: 600px;
    margin: 0 auto;
  }

  /* ── Trait pill ── */
  .trait-pill {
    display: inline-block;
    background: #ffffff;
    border: 1px solid #d0d0d0;
    border-radius: 100px;
    padding: 10px 22px;
    font-size: 15px;
    font-weight: 500;
    color: #1a1a1a;
    margin: 6px;
  }

  /* ── Track / artist row ── */
  .list-row {
    display: flex;
    align-items: center;
    background: #ffffff;
    border: 1px solid #e8e8e8;
    border-radius: 12px;
    padding: 14px 18px;
    margin-bottom: 8px;
    transition: border-color 0.2s;
  }
  .list-row:hover { border-color: #1DB954; }
  .list-rank {
    font-family: 'Syne', sans-serif;
    font-size: 22px;
    font-weight: 800;
    color: #cccccc;
    width: 36px;
    flex-shrink: 0;
  }
  .list-name { font-weight: 600; color: #1a1a1a; font-size: 15px; }
  .list-sub  { font-size: 12px; color: #888888; margin-top: 2px; }
  .list-bar-wrap {
    flex: 1;
    background: #eeeeee;
    border-radius: 4px;
    height: 6px;
    margin: 0 16px;
  }
  .list-bar {
    background: #1DB954;
    height: 6px;
    border-radius: 4px;
  }

  /* ── Section header ── */
  .section-header {
    font-family: 'Syne', sans-serif;
    font-size: 13px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    color: #888888;
    margin-bottom: 18px;
    padding-bottom: 12px;
    border-bottom: 1px solid #e0e0e0;
  }

  /* ── Demo badge ── */
  .demo-badge {
    display: inline-block;
    background: rgba(29,185,84,0.1);
    border: 1px solid rgba(29,185,84,0.4);
    border-radius: 20px;
    padding: 3px 12px;
    font-size: 11px;
    color: #1DB954;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-left: 8px;
  }

  /* ── Buttons ── */
  .stButton > button {
    background: #1DB954 !important;
    color: #000000 !important;
    border: none !important;
    border-radius: 100px !important;
    font-weight: 700 !important;
    font-family: 'DM Sans', sans-serif !important;
    padding: 10px 28px !important;
    letter-spacing: 0.02em !important;
  }
  .stButton > button:hover {
    background: #1ed760 !important;
    transform: scale(1.02);
  }

  /* ── Expander ── */
  .streamlit-expanderHeader {
    background: #ffffff !important;
    color: #555555 !important;
    border-radius: 10px !important;
  }

  footer, #MainMenu { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# ─── DEMO DATA GENERATOR ─────────────────────────────────────────────────────
@st.cache_data
def generate_demo_data() -> pd.DataFrame:
    """Synthesise realistic Spotify streaming history for demo mode."""
    rng = np.random.default_rng(42)

    artists = [
        "Burna Boy", "Tems", "Rema", "Ayra Starr", "Wizkid",
        "Kendrick Lamar", "SZA", "Bad Bunny", "The Weeknd", "Beyoncé",
        "Sauti Sol", "Bien", "Bensoul", "Nviiri the Storyteller", "Jovial",
        "Frank Ocean", "Tyler the Creator", "Jorja Smith", "Simi", "Davido",
    ]
    tracks_by_artist = {
        "Burna Boy": ["Last Last", "Ye", "Love Damini", "Outside", "Kilometer"],
        "Tems": ["Free Mind", "Higher", "Essence", "Replay", "Me & U"],
        "Rema": ["Calm Down", "Iron Man", "FYN", "Holiday", "Bad Commando"],
        "Ayra Starr": ["Rush", "Bloody Samaritan", "Sability", "Woman", "COMMAS"],
        "Wizkid": ["Essence", "Joro", "Ojuelegba", "Come Closer", "Fever"],
        "Kendrick Lamar": ["Not Like Us", "HUMBLE.", "DNA.", "Alright", "Money Trees"],
        "SZA": ["Kill Bill", "Snooze", "Good Days", "I Hate U", "Supermodel"],
        "Bad Bunny": ["Tití Me Preguntó", "Dakiti", "Me Porto Bonito", "Callaíta", "Ojitos Lindos"],
        "The Weeknd": ["Blinding Lights", "Save Your Tears", "Starboy", "Die For You", "Earned It"],
        "Beyoncé": ["TEXAS HOLD 'EM", "CUFF IT", "ALIEN SUPERSTAR", "Formation", "Lemonade"],
        "Sauti Sol": ["Extravaganza", "Suzanna", "Melanin", "Nairobi", "Short and Sweet"],
        "Bien": ["Unapologetic", "Shade", "Mtoto Wa Mboga", "Wangu", "Raha"],
        "Bensoul": ["Favourite", "Salome", "Nairobi", "Lullaby", "Ninanoki"],
        "Nviiri the Storyteller": ["Method", "Hennessy", "Beige", "So Nice", "Kabiria"],
        "Jovial": ["Kairo", "Sawa", "Tonight", "Cheki", "Wangu"],
        "Frank Ocean": ["Nights", "Pink + White", "Ivy", "Self Control", "Chanel"],
        "Tyler the Creator": ["EARFQUAKE", "See You Again", "MASSA", "IFHY", "Garden Shed"],
        "Jorja Smith": ["Blue Lights", "On My Mind", "Teenage Fantasy", "Little Things", "Gone"],
        "Simi": ["Duduke", "By You", "Owanbe", "Joromi", "Smile for Me"],
        "Davido": ["Fall", "IF", "FEM", "Assurance", "Wonder Woman"],
    }

    n = 1800
    base_date = datetime(2025, 1, 1)
    rows = []

    for _ in range(n):
        hour_weights = np.concatenate([
            np.ones(6) * 0.3,
            np.ones(5) * 0.8,
            np.ones(6) * 1.2,
            np.ones(7) * 2.0,
        ])
        hour_weights /= hour_weights.sum()

        artist = rng.choice(artists, p=rng.dirichlet(np.ones(len(artists)) * 0.6))
        track  = rng.choice(tracks_by_artist[artist])
        hour   = rng.choice(24, p=hour_weights)
        day    = int(rng.integers(0, 365))
        ts     = base_date + timedelta(days=day, hours=int(hour), minutes=int(rng.integers(0, 60)))

        ms_played = int(rng.choice([
            rng.integers(5000, 25000),
            rng.integers(60000, 240000),
        ], p=[0.22, 0.78]))

        rows.append({
            "ts": ts,
            "master_metadata_album_artist_name": artist,
            "master_metadata_track_name": track,
            "ms_played": ms_played,
            "skipped": ms_played < 30000,
            "platform": rng.choice(["Android", "iOS", "Web", "Desktop"], p=[0.4, 0.3, 0.2, 0.1]),
        })

    df = pd.DataFrame(rows)
    df["hour"]           = df["ts"].dt.hour
    df["day"]            = df["ts"].dt.day_name()
    df["month"]          = df["ts"].dt.month_name()
    df["year"]           = df["ts"].dt.year
    df["year_month"]     = df["ts"].dt.to_period("M").astype(str)
    df["minutes_played"] = df["ms_played"] / 60000
    return df


# ─── DATA LOADING ─────────────────────────────────────────────────────────────
@st.cache_data
def load_json_files(file_bytes_list: list) -> pd.DataFrame:
    all_data = []
    for name, data in file_bytes_list:
        if name.endswith(".json"):
            records = json.loads(data)
            all_data.append(pd.DataFrame(records))
        else:
            import io
            all_data.append(pd.read_csv(io.BytesIO(data)))
    return pd.concat(all_data, ignore_index=True)


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["ts"]             = pd.to_datetime(df["ts"], errors="coerce")
    df                   = df.drop_duplicates().dropna(subset=["ts"])
    df                   = df[df["ms_played"] > 5000]
    df["hour"]           = df["ts"].dt.hour
    df["day"]            = df["ts"].dt.day_name()
    df["month"]          = df["ts"].dt.month_name()
    df["year"]           = df["ts"].dt.year
    df["year_month"]     = df["ts"].dt.to_period("M").astype(str)
    df["minutes_played"] = df["ms_played"] / 60000
    return df


# ─── ANALYTICS ENGINE ─────────────────────────────────────────────────────────
def compute_stats(df: pd.DataFrame) -> dict:
    total_streams  = len(df)
    unique_artists = df["master_metadata_album_artist_name"].nunique()
    unique_tracks  = df["master_metadata_track_name"].nunique()
    total_hours    = df["minutes_played"].sum() / 60
    skip_rate      = df["skipped"].mean() * 100 if "skipped" in df.columns else None
    avg_session    = df["minutes_played"].mean()
    top_artist     = df.groupby("master_metadata_album_artist_name")["minutes_played"].sum().idxmax()

    return {
        "total_streams":  total_streams,
        "unique_artists": unique_artists,
        "unique_tracks":  unique_tracks,
        "total_hours":    total_hours,
        "skip_rate":      skip_rate,
        "avg_session":    avg_session,
        "top_artist":     top_artist,
    }


def build_personality(df: pd.DataFrame) -> dict:
    unique_artists = df["master_metadata_album_artist_name"].nunique()
    total          = len(df)
    diversity      = unique_artists / total if total else 0

    morning = df[df["hour"].between(5, 10)]["minutes_played"].sum()
    day     = df[df["hour"].between(11, 16)]["minutes_played"].sum()
    evening = df[df["hour"].between(17, 21)]["minutes_played"].sum()
    night   = df[(df["hour"] >= 22) | (df["hour"] < 5)]["minutes_played"].sum()

    tod_map  = {"🌅 Morning": morning, "☀️ Day": day, "🌆 Evening": evening, "🌙 Night": night}
    peak_tod = max(tod_map, key=tod_map.get)

    skip_rate       = df["skipped"].mean() if "skipped" in df.columns else 0.2
    long_listen_pct = (df["ms_played"] > 120000).mean()

    if diversity > 0.12:
        loyalty = "🗺️ Explorer"
    elif diversity > 0.06:
        loyalty = "🔄 Switcher"
    else:
        loyalty = "💎 Loyalist"

    if skip_rate < 0.15 and long_listen_pct > 0.45:
        depth = "🎯 Deep Listener"
    elif skip_rate > 0.40:
        depth = "⚡ Picky Listener"
    else:
        depth = "🎲 Casual Listener"

    traits = [loyalty, depth, peak_tod]

    archetypes = {
        ("🗺️ Explorer",  "🌙 Night"):    ("Midnight Voyager",         "You move through music like a city at 3am — always searching, never settling. New artists, odd hours, always the one with the obscure recommendation."),
        ("💎 Loyalist",  "🎯 Deep Listener"): ("The Devoted",          "When you find your sound, you commit. Your top 5 artists have probably occupied that spot for years. Skipping a song feels personal."),
        ("🗺️ Explorer",  "☀️ Day"):       ("The Curator",              "Intentional, wide-ranging, taste-forward. You probably have a playlist for every micro-mood and you update it religiously."),
        ("⚡ Picky Listener", "🗺️ Explorer"): ("Taste Architect",      "High bar, wide net. You'll scan through ten songs to find the one that's exactly right — and when you do, it plays on repeat."),
        ("💎 Loyalist",  "🌙 Night"):     ("The Devotee",              "Same artists, late nights, full albums. Music isn't background noise for you — it's ritual."),
        ("🗺️ Explorer",  "🌆 Evening"):   ("The After-Hours Curator",  "Your evenings have a soundtrack and it changes weekly. Explorer energy with just enough consistency to have a signature sound."),
        ("💎 Loyalist",  "🌅 Morning"):   ("The Ritual Keeper",        "Every morning, same playlist, same artists. Your listening is meditative — music as anchor, not discovery."),
    }

    archetype_name = "The Audiophile"
    archetype_desc = "Your listening defies easy categorization. Wide taste, intentional choices, and a relationship with music that's genuinely your own."

    for (l, t), (name, desc) in archetypes.items():
        if loyalty == l and t in peak_tod:
            archetype_name = name
            archetype_desc = desc
            break

    return {
        "traits":          traits,
        "archetype":       archetype_name,
        "desc":            archetype_desc,
        "diversity":       diversity,
        "skip_rate":       skip_rate,
        "long_listen_pct": long_listen_pct,
        "tod":             tod_map,
        "peak_tod":        peak_tod,
    }


# ─── SHARED LAYOUT BASE (no xaxis/yaxis — each chart sets its own) ────────────
LAYOUT_BASE = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="#ffffff",
    font=dict(family="DM Sans, sans-serif", color="#888888", size=11),
    margin=dict(l=0, r=0, t=32, b=0),
    hovermode="x unified",
    legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor="#e0e0e0", borderwidth=1),
)

AXIS_DEFAULTS = dict(gridcolor="#eeeeee", zeroline=False, showline=False)

DAYS_ORDERED = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


# ─── CHARTS ───────────────────────────────────────────────────────────────────
def chart_heatmap(df: pd.DataFrame) -> go.Figure:
    pivot = (
        df.groupby(["day", "hour"])["minutes_played"]
        .sum()
        .reset_index()
        .pivot(index="day", columns="hour", values="minutes_played")
        .reindex(DAYS_ORDERED)
        .fillna(0)
    )
    fig = go.Figure(go.Heatmap(
        z=pivot.values,
        x=[f"{h:02d}:00" for h in pivot.columns],
        y=pivot.index.tolist(),
        colorscale=[[0, "#f5f5f0"], [0.3, "#c5ebd4"], [0.7, "#5dd68a"], [1, "#1DB954"]],
        showscale=False,
        hovertemplate="<b>%{y} %{x}</b><br>%{z:.0f} min<extra></extra>",
    ))
    fig.update_layout(
        **LAYOUT_BASE,
        title=dict(text="Listening Heatmap — Hour × Day", font=dict(size=13, color="#888888")),
        height=300,
        xaxis=dict(**AXIS_DEFAULTS),
        yaxis=dict(
            **AXIS_DEFAULTS,
            categoryorder="array",
            categoryarray=list(reversed(DAYS_ORDERED)),
        ),
    )
    return fig


def chart_monthly(df: pd.DataFrame) -> go.Figure:
    monthly = df.groupby("year_month")["minutes_played"].sum().reset_index()
    monthly["hours"] = monthly["minutes_played"] / 60
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=monthly["year_month"], y=monthly["hours"],
        marker_color="#1DB954", marker_line_width=0,
        hovertemplate="%{x}<br><b>%{y:.1f} hrs</b><extra></extra>",
        name="Hours",
    ))
    fig.update_layout(
        **LAYOUT_BASE,
        title=dict(text="Monthly Listening Volume (hours)", font=dict(size=13, color="#888888")),
        height=260,
        xaxis=dict(**AXIS_DEFAULTS),
        yaxis=dict(**AXIS_DEFAULTS),
    )
    return fig


def chart_top_artists_evolution(df: pd.DataFrame) -> go.Figure:
    top5 = df.groupby("master_metadata_album_artist_name")["minutes_played"].sum().nlargest(5).index
    monthly = (
        df[df["master_metadata_album_artist_name"].isin(top5)]
        .groupby(["year_month", "master_metadata_album_artist_name"])
        .size().reset_index(name="streams")
    )
    colors = ["#1DB954", "#17a04a", "#2d8a55", "#5dd68a", "#a8ff78"]
    fig = go.Figure()
    for i, artist in enumerate(top5):
        a_df = monthly[monthly["master_metadata_album_artist_name"] == artist]
        fig.add_trace(go.Scatter(
            x=a_df["year_month"], y=a_df["streams"],
            name=artist,
            line=dict(color=colors[i % len(colors)], width=2),
            mode="lines+markers",
            marker=dict(size=5),
            hovertemplate=f"<b>{artist}</b><br>%{{x}}: %{{y}} plays<extra></extra>",
        ))
    fig.update_layout(
        **LAYOUT_BASE,
        title=dict(text="Top Artists — Play Count Over Time", font=dict(size=13, color="#888888")),
        height=320,
        xaxis=dict(**AXIS_DEFAULTS),
        yaxis=dict(**AXIS_DEFAULTS),
    )
    return fig


def chart_tod_donut(tod: dict) -> go.Figure:
    labels = list(tod.keys())
    values = [tod[k] / 60 for k in labels]
    fig = go.Figure(go.Pie(
        labels=labels, values=values,
        hole=0.65,
        marker=dict(
            colors=["#fbbf24", "#60a5fa", "#f97316", "#1DB954"],
            line=dict(color="#f5f5f0", width=3),
        ),
        textinfo="percent",
        textfont=dict(size=11, color="white"),
        hovertemplate="<b>%{label}</b><br>%{value:.1f} hrs<extra></extra>",
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=True,
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#666666", size=11)),
        height=280,
        margin=dict(l=0, r=0, t=0, b=0),
    )
    return fig


def chart_skip_rate(df: pd.DataFrame) -> go.Figure:
    if "skipped" not in df.columns:
        return None
    hourly = df.groupby("hour").agg(
        skip_rate=("skipped", "mean"),
        volume=("ms_played", "count"),
    ).reset_index()
    hourly["skip_pct"] = hourly["skip_rate"] * 100
    colors = ["#f87171" if s > 35 else "#facc15" if s > 20 else "#1DB954"
              for s in hourly["skip_pct"]]
    fig = go.Figure(go.Bar(
        x=hourly["hour"], y=hourly["skip_pct"],
        marker_color=colors, marker_line_width=0,
        hovertemplate="Hour %{x}:00<br>Skip rate: <b>%{y:.1f}%</b><extra></extra>",
    ))
    fig.update_layout(
        **LAYOUT_BASE,
        title=dict(text="Skip Rate by Hour of Day", font=dict(size=13, color="#888888")),
        height=240,
        xaxis=dict(
            **AXIS_DEFAULTS,
            tickvals=list(range(0, 24, 2)),
            ticktext=[f"{h:02d}:00" for h in range(0, 24, 2)],
        ),
        yaxis=dict(**AXIS_DEFAULTS),
    )
    return fig


def chart_platform(df: pd.DataFrame) -> go.Figure:
    if "platform" not in df.columns:
        return None
    plat = df.groupby("platform")["minutes_played"].sum().reset_index()
    plat["hours"] = plat["minutes_played"] / 60
    fig = px.bar(
        plat, x="platform", y="hours",
        color="hours",
        color_continuous_scale=[[0, "#c5ebd4"], [1, "#1DB954"]],
        text=plat["hours"].apply(lambda x: f"{x:.0f}h"),
    )
    fig.update_traces(textposition="outside", textfont_color="#555555", marker_line_width=0)
    fig.update_layout(
        **LAYOUT_BASE,
        title=dict(text="Listening by Platform", font=dict(size=13, color="#888888")),
        height=240,
        coloraxis_showscale=False,
        xaxis=dict(**AXIS_DEFAULTS, title=""),
        yaxis=dict(**AXIS_DEFAULTS, title=""),
    )
    return fig


# ─── RENDER TOP LIST ──────────────────────────────────────────────────────────
def render_top_list(series: pd.Series, unit: str, is_minutes: bool = True):
    max_val = series.max()
    for i, (name, val) in enumerate(series.items()):
        display = f"{val/60:.1f} hrs" if is_minutes else f"{int(val)} plays"
        pct = (val / max_val) * 100
        st.markdown(f"""
        <div class="list-row">
          <div class="list-rank">#{i+1}</div>
          <div style="flex:1;min-width:0;">
            <div class="list-name">{name}</div>
            <div class="list-sub">{display}</div>
          </div>
          <div class="list-bar-wrap">
            <div class="list-bar" style="width:{pct}%;"></div>
          </div>
        </div>
        """, unsafe_allow_html=True)


# ─── SIDEBAR ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="margin-bottom:28px;">
      <div style="font-size:22px;font-family:'Syne',sans-serif;font-weight:800;
                  color:#1DB954;letter-spacing:-0.02em;">SpotifyDNA</div>
      <div style="font-size:12px;color:#888;margin-top:2px;">Listening Behavior Intelligence</div>
    </div>
    """, unsafe_allow_html=True)

    use_demo = st.checkbox("Use demo data", value=True,
                           help="Explore with synthetic data — no upload needed")

    if not use_demo:
        uploaded_files = st.file_uploader(
            "Upload your Spotify JSON files",
            type=["json", "csv"],
            accept_multiple_files=True,
        )
    else:
        uploaded_files = None

    st.markdown("---")
    st.markdown("""
    <div style="font-size:12px;color:#888;line-height:1.8;">
      <b style="color:#555;">Get your data from Spotify:</b><br>
      Account → Privacy Settings<br>
      → Download your data<br>
      → Extended Streaming History<br><br>
      Upload the <code style="color:#1DB954;">StreamingHistory*.json</code> files here.
    </div>
    """, unsafe_allow_html=True)


# ─── LOAD DATA ────────────────────────────────────────────────────────────────
df = None
demo_mode = False

if use_demo:
    df = generate_demo_data()
    demo_mode = True
elif uploaded_files:
    raw = load_json_files([(f.name, f.read()) for f in uploaded_files])
    df  = clean_data(raw)


# ─── HERO ─────────────────────────────────────────────────────────────────────
demo_badge = '<span class="demo-badge">Demo Mode</span>' if demo_mode else ""
st.markdown(f"""
<div style="margin-bottom:32px;">
  <div style="font-size:11px;letter-spacing:0.25em;color:#1DB954;
              text-transform:uppercase;margin-bottom:10px;font-family:'DM Sans',monospace;">
    Listening Intelligence
  </div>
  <div style="font-family:'Syne',sans-serif;font-size:40px;font-weight:800;
              color:#1a1a1a;line-height:1.1;margin-bottom:12px;">
    What does your<br>music say about you?
  </div>
  <div style="font-size:14px;color:#777;max-width:520px;line-height:1.7;">
    SpotifyDNA turns raw streaming history into behavioral signals —
    skip patterns, time-of-day habits, artist loyalty — and maps them
    to a listening personality you'll actually recognise.
    {demo_badge}
  </div>
</div>
""", unsafe_allow_html=True)


# ─── MAIN CONTENT ─────────────────────────────────────────────────────────────
if df is None:
    st.markdown("""
    <div style="background:#ffffff;border:1px dashed #d0d0d0;border-radius:16px;
                padding:48px;text-align:center;color:#aaaaaa;">
      <div style="font-size:40px;margin-bottom:16px;">🎧</div>
      <div style="font-family:'Syne',sans-serif;font-size:18px;color:#888;
                  margin-bottom:8px;">Upload your Spotify data to begin</div>
      <div style="font-size:13px;color:#aaa;">Or enable Demo Mode in the sidebar to explore instantly</div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()


stats   = compute_stats(df)
persona = build_personality(df)

# ─── KPI STRIP ────────────────────────────────────────────────────────────────
k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Total Streams",  f"{stats['total_streams']:,}")
k2.metric("Unique Artists", f"{stats['unique_artists']:,}")
k3.metric("Unique Tracks",  f"{stats['unique_tracks']:,}")
k4.metric("Hours Listened", f"{stats['total_hours']:.0f}")
k5.metric("Skip Rate",
          f"{stats['skip_rate']:.1f}%" if stats["skip_rate"] is not None else "N/A")

st.markdown("<br>", unsafe_allow_html=True)

# ─── TABS ─────────────────────────────────────────────────────────────────────
tab_overview, tab_behavior, tab_personality, tab_data = st.tabs([
    "📊  Overview", "⚡  Behavior", "🧬  Personality", "📋  Raw Data"
])


# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════
with tab_overview:
    st.markdown("<div class='section-header'>Listening Heatmap</div>", unsafe_allow_html=True)
    st.plotly_chart(chart_heatmap(df), use_container_width=True, config={"displayModeBar": False})

    st.markdown("<br>", unsafe_allow_html=True)

    col_monthly, col_tod = st.columns([3, 2], gap="large")

    with col_monthly:
        st.markdown("<div class='section-header'>Monthly Volume</div>", unsafe_allow_html=True)
        st.plotly_chart(chart_monthly(df), use_container_width=True, config={"displayModeBar": False})

    with col_tod:
        st.markdown("<div class='section-header'>Time of Day Split</div>", unsafe_allow_html=True)
        st.plotly_chart(chart_tod_donut(persona["tod"]), use_container_width=True,
                        config={"displayModeBar": False})

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div class='section-header'>Artist Evolution — Top 5</div>", unsafe_allow_html=True)
    st.plotly_chart(chart_top_artists_evolution(df), use_container_width=True,
                    config={"displayModeBar": False})


# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — BEHAVIOR
# ══════════════════════════════════════════════════════════════════════════════
with tab_behavior:
    col_artists, col_tracks = st.columns(2, gap="large")

    with col_artists:
        st.markdown("<div class='section-header'>Top Artists by Minutes</div>", unsafe_allow_html=True)
        top_artists = (
            df.groupby("master_metadata_album_artist_name")["minutes_played"]
            .sum().sort_values(ascending=False).head(8)
        )
        render_top_list(top_artists, "hrs")

    with col_tracks:
        st.markdown("<div class='section-header'>Top Tracks by Minutes</div>", unsafe_allow_html=True)
        top_tracks = (
            df.groupby("master_metadata_track_name")["minutes_played"]
            .sum().sort_values(ascending=False).head(8)
        )
        render_top_list(top_tracks, "min")

    st.markdown("<br>", unsafe_allow_html=True)

    col_skip, col_plat = st.columns(2, gap="large")

    with col_skip:
        st.markdown("<div class='section-header'>Skip Behavior</div>", unsafe_allow_html=True)
        skip_fig = chart_skip_rate(df)
        if skip_fig:
            st.plotly_chart(skip_fig, use_container_width=True, config={"displayModeBar": False})
            st.markdown(f"""
            <div style="background:#f0faf4;border-left:3px solid #1DB954;border-radius:0 8px 8px 0;
                        padding:12px 16px;font-size:13px;color:#555;line-height:1.7;margin-top:8px;">
              Your overall skip rate is <b style="color:#1a1a1a;">
              {persona['skip_rate']*100:.1f}%</b>.
              {'High skip rate suggests you scan for the right vibe rather than committing.' if persona['skip_rate'] > 0.35
               else 'Low skip rate — you tend to let songs play through. Committed listener.' if persona['skip_rate'] < 0.15
               else 'Average skip rate — balanced between exploring and committing.'}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("Skip data not available in your export.")

    with col_plat:
        st.markdown("<div class='section-header'>Platform Breakdown</div>", unsafe_allow_html=True)
        plat_fig = chart_platform(df)
        if plat_fig:
            st.plotly_chart(plat_fig, use_container_width=True, config={"displayModeBar": False})
        else:
            st.info("Platform data not available in your export.")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div class='section-header'>Listening by Day of Week</div>", unsafe_allow_html=True)
    dow = (
        df.groupby("day")["minutes_played"].sum()
        .reindex(DAYS_ORDERED).fillna(0) / 60
    )
    fig_dow = go.Figure(go.Bar(
        x=dow.index, y=dow.values,
        marker_color=["#1DB954" if d in ["Friday", "Saturday", "Sunday"] else "#c5ebd4"
                      for d in dow.index],
        marker_line_width=0,
        hovertemplate="%{x}<br><b>%{y:.1f} hrs</b><extra></extra>",
    ))
    fig_dow.update_layout(
        **LAYOUT_BASE,
        title=dict(text="Total Hours by Day", font=dict(size=13, color="#888888")),
        height=240,
        xaxis=dict(**AXIS_DEFAULTS),
        yaxis=dict(**AXIS_DEFAULTS),
    )
    st.plotly_chart(fig_dow, use_container_width=True, config={"displayModeBar": False})


# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — PERSONALITY
# ══════════════════════════════════════════════════════════════════════════════
with tab_personality:

    st.markdown(f"""
    <div class="archetype-card">
      <div class="archetype-eyebrow">Your SpotifyDNA</div>
      <div class="archetype-name">{persona['archetype']}</div>
      <div class="archetype-desc">{persona['desc']}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("<div class='section-header'>Your Listening Traits</div>", unsafe_allow_html=True)
    trait_html = "".join([f'<span class="trait-pill">{t}</span>' for t in persona["traits"]])
    st.markdown(f'<div style="text-align:center;padding:8px 0 24px;">{trait_html}</div>',
                unsafe_allow_html=True)

    col_depth, col_exp, col_clock = st.columns(3, gap="large")

    with col_depth:
        depth_pct = persona["long_listen_pct"] * 100
        st.markdown(f"""
        <div style="background:#ffffff;border:1px solid #e0e0e0;border-radius:14px;padding:24px;">
          <div style="font-size:11px;letter-spacing:0.12em;text-transform:uppercase;
                      color:#888;margin-bottom:12px;">Listening Depth</div>
          <div style="font-family:'Syne',sans-serif;font-size:36px;font-weight:800;color:#1DB954;">
            {depth_pct:.0f}%
          </div>
          <div style="font-size:13px;color:#888;margin-top:4px;">of plays are full listens (2+ min)</div>
          <div style="background:#eeeeee;border-radius:6px;height:6px;margin-top:16px;">
            <div style="background:#1DB954;width:{depth_pct}%;height:6px;border-radius:6px;"></div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    with col_exp:
        exp_pct = min(persona["diversity"] * 500, 100)
        st.markdown(f"""
        <div style="background:#ffffff;border:1px solid #e0e0e0;border-radius:14px;padding:24px;">
          <div style="font-size:11px;letter-spacing:0.12em;text-transform:uppercase;
                      color:#888;margin-bottom:12px;">Explorer Score</div>
          <div style="font-family:'Syne',sans-serif;font-size:36px;font-weight:800;color:#1DB954;">
            {exp_pct:.0f}%
          </div>
          <div style="font-size:13px;color:#888;margin-top:4px;">artist diversity relative to streams</div>
          <div style="background:#eeeeee;border-radius:6px;height:6px;margin-top:16px;">
            <div style="background:#1DB954;width:{exp_pct}%;height:6px;border-radius:6px;"></div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    with col_clock:
        st.markdown(f"""
        <div style="background:#ffffff;border:1px solid #e0e0e0;border-radius:14px;padding:24px;">
          <div style="font-size:11px;letter-spacing:0.12em;text-transform:uppercase;
                      color:#888;margin-bottom:12px;">Peak Listening Time</div>
          <div style="font-family:'Syne',sans-serif;font-size:36px;font-weight:800;color:#1DB954;">
            {persona['peak_tod'].split(' ')[1]}
          </div>
          <div style="font-size:13px;color:#888;margin-top:4px;">
            {persona['peak_tod']} is when you're most in it
          </div>
          <div style="font-size:30px;margin-top:16px;">{persona['peak_tod'].split(' ')[0]}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    with st.expander("🔬 How your personality is calculated", expanded=False):
        st.markdown(f"""
        <div style="color:#555;font-size:13px;line-height:1.8;padding:8px 0;">
          <b style="color:#1DB954;">Explorer Score</b> is your unique artist count divided by total streams.
          A higher ratio means you're actively seeking out new music rather than looping favourites.<br><br>
          <b style="color:#1DB954;">Listening Depth</b> is the percentage of plays longer than 2 minutes —
          a proxy for intentional, committed listening versus scanning behaviour.<br><br>
          <b style="color:#1DB954;">Skip Rate</b> tracks how often you move on before a track ends.
          High skip rate + high explorer score = Taste Architect energy.
          Low skip rate + high loyalty = Devoted Listener.<br><br>
          <b style="color:#1DB954;">Peak Time</b> is determined by comparing total listening minutes across
          four time windows. It feeds directly into archetype assignment.<br><br>
          Your archetype (<b style="color:#1a1a1a;">{persona['archetype']}</b>) is the intersection
          of your loyalty pattern and your peak listening window.
        </div>
        """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — RAW DATA
# ══════════════════════════════════════════════════════════════════════════════
with tab_data:
    st.markdown("<div class='section-header'>Recent Streams</div>", unsafe_allow_html=True)
    display_cols = [c for c in [
        "ts", "master_metadata_album_artist_name",
        "master_metadata_track_name", "minutes_played", "skipped", "platform"
    ] if c in df.columns]
    display_df = df[display_cols].sort_values("ts", ascending=False).head(200).copy()
    display_df["minutes_played"] = display_df["minutes_played"].round(1)
    if "ts" in display_df.columns:
        display_df["ts"] = display_df["ts"].dt.strftime("%Y-%m-%d %H:%M")
    display_df.columns = [
        c.replace("master_metadata_", "").replace("_name", "")
         .replace("album_artist", "artist").replace("track", "track")
         .title().replace("_", " ")
        for c in display_df.columns
    ]
    st.dataframe(display_df, use_container_width=True, hide_index=True)

    st.markdown(f"""
    <div style="font-size:12px;color:#aaaaaa;margin-top:12px;font-family:'DM Sans',monospace;">
      Showing 200 of {len(df):,} total records ·
      {'Demo data — no real personal data stored' if demo_mode else 'Your personal data stays in your browser session only'}
    </div>
    """, unsafe_allow_html=True)


# ─── FOOTER ───────────────────────────────────────────────────────────────────
st.markdown("""
<div style="margin-top:60px;padding:24px 0;border-top:1px solid #e0e0e0;
            display:flex;justify-content:space-between;align-items:center;">
  <div style="font-size:11px;color:#cccccc;font-family:'DM Sans',monospace;">
    SpotifyDNA · Behavioral Listening Intelligence
  </div>
  <div style="font-size:11px;color:#cccccc;font-family:'DM Sans',monospace;">
    Built by Kerubo Bosire · Python · Streamlit · Plotly
  </div>
</div>
""", unsafe_allow_html=True)