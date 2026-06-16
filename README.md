# 🎧 SpotifyDNA
### You Shouldn't Have to Wait Until December to Know Your Own Taste

[![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square&logo=python)](https://python.org) [![Streamlit](https://img.shields.io/badge/Built%20with-Streamlit-ff4b4b?style=flat-square&logo=streamlit)](https://streamlit.io) [![Live Demo](https://img.shields.io/badge/Live-Demo-2ea44f?style=flat-square)](https://the-spotify-data-analysis-m6w3vxjncfcxyx8yaitjkb.streamlit.app/)

**Live Demo:** https://the-spotify-data-analysis-m6w3vxjncfcxyx8yaitjkb.streamlit.app/

### Snippet of the App

<img width="1349" height="584" alt="image" src="https://github.com/user-attachments/assets/de8c7077-2eb9-4e83-9bf2-15d235328eba" />


## The Problem

Spotify knows everything about how you listen. You know almost nothing.

You get Wrapped once a year — a handful of top artists, a total minutes count, a vague "you're in the top 1% of listeners" badge. It's surface-level. It doesn't tell you *how* you listen: whether you're a loyal repeater or a chronic explorer, whether you commit to songs or scan through them, whether your late-night playlists are a ritual or random. The behavioral signal is there in your streaming history — Spotify just never surfaces it..

---

## Try It in Five Seconds

Open the app and you're not staring at an empty upload box. It loads straight into a full demo — Kenyan artists like Sauti Sol, Bien, Bensoul, and Nviiri sitting alongside global names, because that's what a real East African listening history actually looks like, not a sanitised stock placeholder.

No login. No uploading your private data to a stranger's app. Every chart is already alive the moment the page loads.

---

## What You'll See

**Overview** — the headline numbers. Total streams, unique artists, total time, your top tracks. Orientation before interpretation.

**Behavior** — this is the tab that does the real work. Skip rate. Exploration vs. loyalty. And the centrepiece: a heatmap of *when* you listen, hour by hour, day by day. Most listening-history projects stop at "your top 5 artists." This one shows you the shape of your habits — the Sunday-morning lull, the Friday-night spike — which is a different and harder thing to build than a leaderboard.

**Personality** — your archetype: Night Owl, Explorer, Deep Listener, and combinations like *Night Owl Explorer*. Click "How your personality is calculated" and you get the actual logic behind it, not just a label. Showing your reasoning, not just your output, is the part most people skip.

**Raw Data** — the receipts, for anyone who wants to check the work.

---

## How It Works

## The Pipeline Behind It

```
Spotify Streaming History (JSON/CSV)
        ↓
Data Cleaning & Normalization
        ↓
Feature Engineering
  → Skip rate
  → Listening duration
  → Artist diversity
  → Time-of-day distribution
        ↓
Behavior Classification
  → Explorer vs Loyalist
  → Deep vs Picky listener
  → Morning / Day / Night profile
        ↓
Personality Archetype Mapping
  → e.g. "Night Owl Explorer"
        ↓
Interactive Dashboard (Streamlit + Plotly)
```

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Language | Python |
| Data Processing | Pandas, NumPy |
| Frontend | Streamlit |
| Visualisation | Plotly, Matplotlib, Seaborn |
| Data Format | Spotify JSON export |

---

## What's Next

- **Spotify API integration** — pulling live listening data directly instead of requiring a manual JSON export, removing the biggest friction point for real (non-demo) usage
- **Clustering-based behaviour modeling** — moving from rule-based archetypes to unsupervised clustering on the engineered features, letting listener types emerge from the data rather than being predefined
- **Mood detection** — incorporating audio features like energy, valence, and tempo (available via the Spotify API) to add an emotional dimension alongside the current behavioural one
- **Personality-based recommendations** — using the archetype as an input to suggest new artists or tracks, closing the loop from "here's who you are" to "here's what that suggests you'd like"
- **Social comparison** — letting two users compare listening DNA side by side, which turns a solo analytics tool into something inherently shareable
- **Exportable Wrapped-style report** — a shareable visual summary, since the format Spotify's own "Wrapped" popularised is exactly what this kind of personality and behaviour data is suited to present

---

## Built By

**Kerubo Bosire** — Machine Learning | Data Science & Analytics | Actuarial Science background

