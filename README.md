# 🎧 SpotifyDNA
### You Shouldn't Have to Wait Until December to Know Your Own Taste

[![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square&logo=python)](https://python.org) [![Streamlit](https://img.shields.io/badge/Built%20with-Streamlit-ff4b4b?style=flat-square&logo=streamlit)](https://streamlit.io) [![Live Demo](https://img.shields.io/badge/Live-Demo-2ea44f?style=flat-square)](https://the-spotify-data-analysis-m6w3vxjncfcxyx8yaitjkb.streamlit.app/)

**Live Demo:** https://the-spotify-data-analysis-m6w3vxjncfcxyx8yaitjkb.streamlit.app/

---

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

```
Streaming history (JSON/CSV)
        ↓
Clean & normalize
        ↓
Engineer behavioral signals
  skip rate · diversity · time-of-day patterns
        ↓
Classify behavior
  Explorer/Loyalist · Deep/Picky · Morning/Night
        ↓
Map to personality archetype
        ↓
Dashboard
```

No black-box model here — every classification is a rule you could trace by hand if you wanted to. That's intentional. The goal was to make behaviour legible, not to impress with a model nobody (including the listener) could explain.

---

## Tech Stack

Python · Pandas · NumPy · Streamlit · Plotly · Matplotlib · Seaborn

---

## What's Next

- Spotify API integration, so it pulls live data instead of needing a manual export
- Clustering-based behavior modeling — letting listener types emerge from the data instead of being predefined
- Mood detection using audio features like energy and valence
- Personality-based recommendations — taking the archetype and suggesting what to listen to next
- Side-by-side comparison between two listeners' DNA
- A shareable, exportable "Wrapped-style" report

---

## Built By

**Kerubo Bosire** — Machine Learning | Data Science & Analytics | Actuarial Science background
