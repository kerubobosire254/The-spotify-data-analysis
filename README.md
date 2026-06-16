# 🎧 SpotifyDNA — Listening Behavior Intelligence

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.x-FF4B4B?style=flat&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Plotly](https://img.shields.io/badge/Plotly-Interactive-3D4DB7?style=flat&logo=plotly&logoColor=white)](https://plotly.com)

---
Live Demo ; https://the-spotify-data-analysis-m6w3vxjncfcxyx8yaitjkb.streamlit.app/
## The problem

Spotify knows everything about how you listen. You know almost nothing.

You get Wrapped once a year — a handful of top artists, a total minutes count, a vague "you're in the top 1% of listeners" badge. It's surface-level. It doesn't tell you *how* you listen: whether you're a loyal repeater or a chronic explorer, whether you commit to songs or scan through them, whether your late-night playlists are a ritual or random. The behavioral signal is there in your streaming history — Spotify just never surfaces it.

## The solution

SpotifyDNA ingests your raw Spotify streaming export and runs it through a behavioral profiling engine. Instead of counts, it extracts *patterns*:

- **Skip behavior** — do you scan for the right vibe, or do you let songs play through?
- **Artist loyalty** — are you a loyalist circling the same 5 artists, or an explorer constantly expanding?
- **Time-of-day habits** — is music a morning ritual, a late-night companion, or background to your work hours?
- **Listening depth** — what percentage of your plays are genuine listens vs. quick dismissals?

These four signals combine into a listening archetype — *Midnight Voyager*, *The Devoted*, *Taste Architect* — with a description that reads like a personality profile, not a data summary. The kind of thing you actually recognise.

---

## How it works

```
Raw Spotify JSON export  (StreamingHistory*.json)
         │
         ▼
   Data cleaning pipeline
   (dedup, parse timestamps, filter <5s plays, extract features)
         │
         ▼
   Feature engineering
   ┌─────────────────────────────────────────┐
   │  Skip rate      → scanned vs committed  │
   │  Artist diversity ratio → loyalty score │
   │  Time-of-day windows → peak period      │
   │  Long-listen % → depth score            │
   └─────────────────────────────────────────┘
         │
         ▼
   Archetype engine
   (loyalty × peak time → named personality profile)
         │
         ▼
   4-tab Streamlit dashboard
   ┌──────────────┬──────────────┬──────────────┬──────────────┐
   │   Overview   │   Behavior   │  Personality │   Raw Data   │
   │  Heatmap     │  Top artists │  Archetype   │  Full log    │
   │  Monthly vol │  Skip charts │  Trait pills │  200-row     │
   │  Artist evo  │  Platform    │  Score cards │  preview     │
   └──────────────┴──────────────┴──────────────┴──────────────┘
```

### Personality engine logic

The archetype is not a label — it's derived from two independent signals:

| Signal | How it's computed | What it captures |
|---|---|---|
| **Loyalty score** | Unique artist count ÷ total streams | Explorer vs. Loyalist vs. Switcher |
| **Listening depth** | % of plays > 2 minutes | Committed listener vs. scanner |
| **Skip rate** | Skipped streams ÷ total streams | Intentionality |
| **Peak time** | Total minutes across 4 time windows (morning / day / evening / night) | Listening context |

Loyalty score × peak time → archetype. Eight named archetypes, each with a behavioral description. The intersection is what makes it feel personal rather than generic.

---

## Features

### Listening heatmap
Hour × day-of-week grid showing listening intensity across the full year. Immediately surfaces whether someone is a commute listener, a night owl, or a weekend binge listener.

### Behavioral analysis
- Top artists and tracks ranked by total minutes (not just play count — a 30-second skip and a full listen aren't the same)
- Skip rate by hour of day — colour-coded red/amber/green so the pattern is instant
- Platform breakdown — Android, iOS, Web, Desktop
- Day-of-week volume with weekend highlighting

### Personality tab
- Named archetype with a written behavioral profile
- Three score cards: Listening Depth %, Explorer Score %, Peak Time
- Methodology expander — transparent about exactly how each signal is computed

### Demo mode
Fully functional without any upload. Ships with 1,800 synthetic streams drawn from a realistic artist pool (Burna Boy, Tems, Kendrick Lamar, Sauti Sol, Frank Ocean, and others), with hour-weighted timestamps and realistic skip/listen distributions. Every feature is demonstrable in under 30 seconds.

---

## Quickstart

```bash
git clone https://github.com/kerubobosire254/spotifydna.git
cd spotifydna
pip install streamlit pandas numpy plotly
streamlit run app.py
```

To use your own data: go to **Spotify → Account → Privacy Settings → Download your data → Extended Streaming History**, then upload the `StreamingHistory*.json` files. Your data never leaves your browser session.

---

## Technical stack

| Layer | Technology |
|---|---|
| **Data pipeline** | pandas — dedup, timestamp parsing, feature extraction |
| **Analytics** | NumPy — diversity ratio, skip rate, time-window aggregation |
| **Charts** | Plotly — heatmap, bar, line, donut, all custom-styled |
| **UI** | Streamlit — 4-tab layout, custom CSS design system (Syne + DM Sans) |
| **Demo data** | NumPy random generator with hour-weighted distributions and realistic skip probabilities |

---

## Design decisions

**Why minutes, not play count?** Play count treats a 10-second skip equally with a 4-minute full listen. Minutes listened is a far better signal of actual engagement — and it's what makes the loyalty and depth scores meaningful.

**Why named archetypes?** Pure stats (68% explorer score, 0.22 skip rate) don't mean anything to most people. A named archetype with a written description translates behavioral data into something recognisable. The goal is insight, not dashboards.

**Why demo mode with realistic data?** The app has zero utility without data, and asking a recruiter to go export their Spotify history isn't reasonable. The demo mode uses a weighted synthetic dataset — Kenyan and global artists, realistic time distributions — so the full product is immediately explorable.

---

## Author

**Kerubo Bosire**  
BSc Actuarial Science (Upper Second Class Honours), JKUAT  
Python & Data Science Instructor · Pension Analytics · ML Engineering

[![GitHub](https://img.shields.io/badge/GitHub-kerubobosire254-181717?style=flat&logo=github)](https://github.com/kerubobosire254)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-kerubo--bosire-0A66C2?style=flat&logo=linkedin)](https://linkedin.com/in/kerubo-bosire-364523283)

---

> *SpotifyDNA is an independent project with no affiliation with Spotify AB. No audio data or personal listening history is stored, transmitted, or retained beyond the active browser session.*


