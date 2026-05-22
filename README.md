# 🎧 SPOTIFY ANALYTICS APP

SpotifyDNA is a data analytics and behavioral profiling system that transforms raw Spotify streaming history into a 
structured listening personality.

Instead of just showing what you listened to, it answers:

> *What kind of listener are you?*

Built with Python and Streamlit, it combines data engineering, behavioral analytics, and visualization to generate 
interpretable listening archetypes.

## ❗ Problem

Spotify provides raw listening history, but it lacks meaningful interpretation.

Users can see:
- Songs played  
- Artists listened to  
- Timestamps and duration  

But cannot easily understand:
- Their listening behavior patterns  
- Whether they are consistent or exploratory listeners  
- How their habits change over time  
- Their listening identity  

Raw data ≠ insight.

## 💡 Solution

SpotifyDNA converts raw streaming logs into behavioral intelligence through a structured pipeline:

1. **Data Cleaning & Normalization**  
   Standardizes Spotify streaming history into usable format

2. **Feature Engineering**  
   Extracts behavioral signals:
   - Skip rate  
   - Listening duration  
   - Artist diversity  
   - Time-of-day patterns  

3. **Behavior Classification Engine**  
   Translates features into interpretable traits:
   - Explorer vs Loyalist  
   - Deep vs Picky listener  
   - Morning / Day / Night behavior  

4. **Personality Archetype Mapping**  
   Combines traits into a final listening identity (e.g. *Night Owl Explorer*)

5. **Interactive Dashboard**  
   Visualized using Streamlit + Plotly

## ✨ Features

### 📊 Listening Overview
- Total streams analyzed  
- Unique artists count  
- Total listening time  
- Top tracks and artists  

### ⚡ Behavioral Analysis
- Skip rate detection  
- Deep / Casual / Picky listener classification  
- Engagement consistency  

### 🌍 Exploration vs Loyalty Engine
- Measures listening diversity  
- Classifies user as Explorer or Loyalist  

### 🌙 Time-Based Profiling
- Morning / Day / Night listening patterns  
- Night Owl / Early Bird detection  

### 🧬 Personality Engine
Generates archetypes such as:
- 🗺️ Explorer  
- ⚡ Loyalist  
- 🎯 Deep Listener  
- ⚡ Picky Listener  
- 🌙 Night Owl  

### 📈 Interactive Dashboard
- Streamlit UI  
- Plotly visualizations  
- Clean KPI metrics  

## 🧠 Key Insight

SpotifyDNA doesn’t just visualize data — it interprets behavior from patterns in listening history.

It bridges:
> raw data → behavioral signals → identity layer


## 🛠️ Tech Stack

- Python  
- Pandas & NumPy  
- Streamlit  
- Plotly / Matplotlib / Seaborn  
- JSON Spotify data

## 🚀 How It Works

1. Upload Spotify streaming history (JSON/CSV)  
2. Data is cleaned and standardized  
3. Features are engineered  
4. Listening personality is computed  
5. Dashboard visualizes insights  

## 📌 Future Improvements

- Spotify API integration for real-time data  
- Advanced clustering-based behavior modeling  
- Mood detection (energy, valence, tempo)  
- Recommendation engine based on personality  
- Social comparison between users  
- Exportable Spotify Wrapped-style reports  

## 🧑‍💻 Author

Built by **Kerubo Bosire**  
Machine Learning | Data Science & Analytics | Actuarial Science background 

