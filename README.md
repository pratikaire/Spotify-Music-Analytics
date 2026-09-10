# 🎵 Spotify Music Analytics Dashboard

A **Spotify Music Analytics Dashboard** built using **Python, Pandas, NumPy, and Streamlit**.

This project analyzes Spotify track data and provides an interactive dashboard where users can **search for artists and tracks, explore popularity, and analyze audio features**.

---

## 📌 Project Overview

The goal of this project is to explore Spotify music data and understand the characteristics of popular songs.

The dashboard allows users to:

* 🔎 Search for artists and tracks
* 🎵 View track details
* 📊 Analyze song popularity
* 🎧 Explore Spotify audio features
* 👨‍🎤 Analyze artists
* 📈 View top popular songs
* 🔗 Analyze correlations between popularity and audio features
* 🎛️ Filter songs by genre and popularity

---

## 🚀 Features

### 🔍 Music Search

Search for a song or artist using the search bar.

The dashboard displays matching tracks along with information such as:

* Artist name
* Track name
* Genre
* Popularity
* Danceability
* Energy
* Valence
* Tempo
* Acousticness
* Loudness
* Duration

### 🎵 Track Analysis

Select a track to view detailed audio characteristics including:

* Popularity
* Danceability
* Energy
* Valence
* Acousticness
* Speechiness
* Tempo
* Duration

### 📊 Top Songs

View the **Top 20 most popular songs** available in the dataset.

### 👨‍🎤 Artist Analysis

Analyze artists based on:

* Number of tracks
* Average popularity
* Maximum popularity

### 🎧 Audio Feature Analysis

Explore average values of Spotify audio features such as:

* Danceability
* Energy
* Acousticness
* Instrumentalness
* Liveness
* Speechiness
* Valence
* Tempo

### 🔗 Correlation Analysis

Analyze the relationship between song popularity and different audio features.

---

## 🗂️ Dataset

The project uses the **Spotify Features dataset**.

The original dataset contains **232,725 tracks** and includes features such as:

* `genre`
* `artist_name`
* `track_name`
* `track_id`
* `popularity`
* `acousticness`
* `danceability`
* `duration_ms`
* `energy`
* `instrumentalness`
* `key`
* `liveness`
* `loudness`
* `mode`
* `speechiness`
* `tempo`
* `time_signature`
* `valence`

During data preprocessing, duplicate and unnecessary records were removed and song duration was converted into minutes.

---

## 🛠️ Technologies Used

| Technology   | Purpose                             |
| ------------ | ----------------------------------- |
| Python       | Programming language                |
| Pandas       | Data manipulation and analysis      |
| NumPy        | Numerical operations                |
| Streamlit    | Interactive dashboard               |
| Git & GitHub | Version control and project hosting |

---

## 📁 Project Structure

```text
Spotify-Music-Analytics/
│
├── app.py
├── SpotifyFeatures.csv
├── requirements.txt
├── README.md
└── .gitignore
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/Spotify-Music-Analytics.git
```

### 2. Navigate to the project

```bash
cd Spotify-Music-Analytics
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Run the Streamlit Dashboard

Run:

```bash
python -m streamlit run app.py
```

The application will open in your browser.

Usually, it will be available at:

```text
http://localhost:8501
```

---

## 📊 Dashboard Workflow

```text
Spotify Dataset
       ↓
Data Cleaning & Preprocessing
       ↓
Exploratory Data Analysis
       ↓
Feature Analysis
       ↓
Streamlit Dashboard
       ↓
Search / Filter / Visualization
       ↓
Insights
```

---

## 💡 Key Insights

The analysis helps understand how different audio characteristics relate to song popularity.

Some features show stronger relationships with popularity than others, allowing users to explore patterns in:

* Danceability
* Energy
* Loudness
* Acousticness
* Instrumentalness
* Speechiness
* Tempo
* Valence

---

## 🎯 Project Objective

This project demonstrates practical skills in:

* Data Cleaning
* Exploratory Data Analysis
* Data Visualization
* Feature Analysis
* Interactive Dashboard Development
* Python Programming
* Streamlit
* Data Analytics

---

## 👨‍💻 Author

**Pratik Aire**

Data Analytics | Python | SQL | Machine Learning | Streamlit

---

## ⭐ If You Like This Project

If you find this project useful, consider giving the repository a ⭐ on GitHub.
