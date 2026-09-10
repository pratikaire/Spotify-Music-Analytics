
import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Spotify Music Analytics",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

.main-title {
    font-size: 42px;
    font-weight: 800;
    margin-bottom: 0px;
}

.subtitle {
    color: #777;
    font-size: 17px;
    margin-bottom: 25px;
}

[data-testid="stMetric"] {
    border: 1px solid rgba(128,128,128,0.25);
    padding: 15px;
    border-radius: 12px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# LOAD DATASET
# =========================================================

BASE_DIR = Path(__file__).resolve().parent


@st.cache_data(show_spinner="Loading Spotify dataset...")
def load_data():

    possible_files = [
        BASE_DIR / "SpotifyFeatures.csv",
        BASE_DIR / "SpotifyFeatures(2).csv",
        BASE_DIR / "Cleaned_Spotify_Data.csv",
        BASE_DIR / "Cleaned_Spotify_Data(2).csv"
    ]

    for file in possible_files:

        if file.exists():

            data = pd.read_csv(file)

            # Convert duration
            if "duration_ms" in data.columns:

                data["duration_min"] = (
                    data["duration_ms"] / 60000
                )

            # Remove duplicates
            data = data.drop_duplicates().copy()

            # Handle missing artist
            if "artist_name" in data.columns:

                data["artist_name"] = (
                    data["artist_name"]
                    .fillna("Unknown Artist")
                    .astype(str)
                )

            # Handle missing track
            if "track_name" in data.columns:

                data["track_name"] = (
                    data["track_name"]
                    .fillna("Unknown Track")
                    .astype(str)
                )

            return data, file.name

    raise FileNotFoundError(
        """
        Spotify CSV file not found.

        Put SpotifyFeatures.csv or
        Cleaned_Spotify_Data.csv
        in the same folder as app.py.
        """
    )


try:

    df, loaded_file = load_data()

except Exception as error:

    st.error(str(error))
    st.stop()


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="main-title">🎵 Spotify Music Analytics</div>',
    unsafe_allow_html=True
)

st.markdown(
    f"""
    <div class="subtitle">
        Interactive Spotify Music Explorer
        • Dataset: {loaded_file}
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("🎛️ Dashboard Filters")


# -----------------------------
# Genre Filter
# -----------------------------

if "genre" in df.columns:

    genre_list = sorted(
        df["genre"]
        .dropna()
        .astype(str)
        .unique()
    )

    selected_genres = st.sidebar.multiselect(
        "Select Genre",
        genre_list
    )

else:

    selected_genres = []


# -----------------------------
# Popularity Filter
# -----------------------------

min_popularity = int(
    df["popularity"].min()
)

max_popularity = int(
    df["popularity"].max()
)

popularity_range = st.sidebar.slider(
    "Popularity Range",
    min_popularity,
    max_popularity,
    (min_popularity, max_popularity)
)


# =========================================================
# SEARCH
# =========================================================

st.subheader("🔍 Search Spotify")

search_text = st.text_input(
    "Search Artist or Track",
    placeholder="Example: Eminem, Adele, Shape of You...",
    label_visibility="collapsed"
)

filtered_df = df.copy()


# =========================================================
# APPLY GENRE FILTER
# =========================================================

if selected_genres and "genre" in filtered_df.columns:

    filtered_df = filtered_df[
        filtered_df["genre"].isin(selected_genres)
    ]


# =========================================================
# APPLY POPULARITY FILTER
# =========================================================

filtered_df = filtered_df[
    filtered_df["popularity"].between(
        popularity_range[0],
        popularity_range[1]
    )
]


# =========================================================
# SEARCH ARTIST / TRACK
# =========================================================

if search_text:

    search_text = search_text.strip().lower()

    artist_match = (
        filtered_df["artist_name"]
        .str.lower()
        .str.contains(
            search_text,
            na=False,
            regex=False
        )
    )

    if "track_name" in filtered_df.columns:

        track_match = (
            filtered_df["track_name"]
            .str.lower()
            .str.contains(
                search_text,
                na=False,
                regex=False
            )
        )

        filtered_df = filtered_df[
            artist_match | track_match
        ]

    else:

        filtered_df = filtered_df[
            artist_match
        ]


# =========================================================
# KPI SECTION
# =========================================================

st.divider()

col1, col2, col3, col4 = st.columns(4)


# Tracks
col1.metric(
    "🎵 Tracks",
    f"{len(filtered_df):,}"
)


# Artists
col2.metric(
    "🎤 Artists",
    f"{filtered_df['artist_name'].nunique():,}"
)


# Average popularity
if len(filtered_df) > 0:

    average_popularity = (
        filtered_df["popularity"].mean()
    )

else:

    average_popularity = 0


col3.metric(
    "⭐ Avg Popularity",
    f"{average_popularity:.1f}"
)


# Average danceability
if "danceability" in filtered_df.columns:

    average_danceability = (
        filtered_df["danceability"].mean()
    )

else:

    average_danceability = 0


col4.metric(
    "💃 Avg Danceability",
    f"{average_danceability:.2f}"
)


# =========================================================
# SEARCH RESULTS
# =========================================================

st.divider()

st.subheader("🎧 Search Results")


if len(filtered_df) == 0:

    st.warning(
        "No matching songs found. "
        "Try another artist, track, genre, or popularity range."
    )

else:

    display_columns = []

    possible_columns = [
        "artist_name",
        "track_name",
        "genre",
        "popularity",
        "danceability",
        "energy",
        "valence",
        "tempo",
        "acousticness",
        "loudness",
        "duration_min"
    ]

    for column in possible_columns:

        if column in filtered_df.columns:

            display_columns.append(column)


    results = (
        filtered_df
        .sort_values(
            "popularity",
            ascending=False
        )
        .head(100)
    )


    st.dataframe(
        results[display_columns],
        use_container_width=True,
        hide_index=True
    )


# =========================================================
# TRACK DETAILS
# =========================================================

st.divider()

st.subheader("🎶 Track Details")


if (
    "track_name" in filtered_df.columns
    and len(filtered_df) > 0
):

    track_data = filtered_df.copy()

    track_data["selection"] = (
        track_data["artist_name"].astype(str)
        + " — "
        + track_data["track_name"].astype(str)
    )


    track_options = (
        track_data["selection"]
        .drop_duplicates()
        .head(500)
        .tolist()
    )


    selected_track = st.selectbox(
        "Select a track",
        track_options
    )


    selected_row = track_data[
        track_data["selection"] == selected_track
    ].iloc[0]


    st.markdown(
        f"### 🎵 {selected_row['track_name']}"
    )

    st.caption(
        f"Artist: {selected_row['artist_name']}"
    )


    # =====================================================
    # TRACK METRICS
    # =====================================================

    metric_columns = st.columns(4)


    if "popularity" in selected_row.index:

        metric_columns[0].metric(
            "Popularity",
            f"{selected_row['popularity']:.0f}"
        )


    if "danceability" in selected_row.index:

        metric_columns[1].metric(
            "Danceability",
            f"{selected_row['danceability']:.2f}"
        )


    if "energy" in selected_row.index:

        metric_columns[2].metric(
            "Energy",
            f"{selected_row['energy']:.2f}"
        )


    if "valence" in selected_row.index:

        metric_columns[3].metric(
            "Valence",
            f"{selected_row['valence']:.2f}"
        )


    metric_columns2 = st.columns(4)


    if "acousticness" in selected_row.index:

        metric_columns2[0].metric(
            "Acousticness",
            f"{selected_row['acousticness']:.2f}"
        )


    if "speechiness" in selected_row.index:

        metric_columns2[1].metric(
            "Speechiness",
            f"{selected_row['speechiness']:.2f}"
        )


    if "tempo" in selected_row.index:

        metric_columns2[2].metric(
            "Tempo",
            f"{selected_row['tempo']:.1f} BPM"
        )


    if "duration_min" in selected_row.index:

        metric_columns2[3].metric(
            "Duration",
            f"{selected_row['duration_min']:.2f} min"
        )


    # =====================================================
    # AUDIO FEATURES
    # =====================================================

    st.markdown("#### 🎼 Audio Features")


    audio_features = [
        "acousticness",
        "danceability",
        "energy",
        "instrumentalness",
        "liveness",
        "speechiness",
        "valence"
    ]


    available_features = [
        feature
        for feature in audio_features
        if feature in selected_row.index
    ]


    if available_features:

        feature_values = pd.DataFrame({

            "Feature": available_features,

            "Value": [
                float(selected_row[feature])
                for feature in available_features
            ]

        })


        feature_values = (
            feature_values
            .set_index("Feature")
        )


        st.bar_chart(
            feature_values
        )


# =========================================================
# ANALYTICS TABS
# =========================================================

st.divider()

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "🏆 Top Songs",
        "🎤 Artist Analysis",
        "📊 Audio Features",
        "📈 Correlation"
    ]
)


# =========================================================
# TAB 1 — TOP SONGS
# =========================================================

with tab1:

    st.subheader(
        "🏆 Top 20 Most Popular Songs"
    )


    top_songs = (
        df
        .sort_values(
            "popularity",
            ascending=False
        )
        .head(20)
        .copy()
    )


    if "track_name" in top_songs.columns:

        top_songs["Song"] = (
            top_songs["artist_name"]
            + " — "
            + top_songs["track_name"]
        )

    else:

        top_songs["Song"] = (
            top_songs["artist_name"]
        )


    chart_data = (
        top_songs[
            ["Song", "popularity"]
        ]
        .set_index("Song")
    )


    st.bar_chart(
        chart_data
    )


    table_columns = [
        column
        for column in [
            "artist_name",
            "track_name",
            "genre",
            "popularity"
        ]
        if column in top_songs.columns
    ]


    st.dataframe(
        top_songs[table_columns],
        use_container_width=True,
        hide_index=True
    )


# =========================================================
# TAB 2 — ARTIST ANALYSIS
# =========================================================

with tab2:

    st.subheader(
        "🎤 Artist Performance"
    )


    artist_stats = (
        df
        .groupby("artist_name")
        .agg(
            Tracks=("artist_name", "size"),
            Avg_Popularity=(
                "popularity",
                "mean"
            ),
            Max_Popularity=(
                "popularity",
                "max"
            )
        )
        .sort_values(
            "Avg_Popularity",
            ascending=False
        )
        .head(20)
    )


    artist_stats[
        "Avg_Popularity"
    ] = artist_stats[
        "Avg_Popularity"
    ].round(2)


    st.dataframe(
        artist_stats,
        use_container_width=True
    )


    st.markdown(
        "#### Average Popularity by Artist"
    )


    st.bar_chart(
        artist_stats["Avg_Popularity"]
    )


# =========================================================
# TAB 3 — AUDIO FEATURES
# =========================================================

with tab3:

    st.subheader(
        "📊 Average Audio Features"
    )


    feature_columns = [
        "acousticness",
        "danceability",
        "energy",
        "instrumentalness",
        "liveness",
        "speechiness",
        "valence"
    ]


    available_columns = [
        column
        for column in feature_columns
        if column in df.columns
    ]


    if available_columns:

        feature_average = (
            df[available_columns]
            .mean()
            .sort_values(
                ascending=False
            )
        )


        st.bar_chart(
            feature_average
        )


        st.dataframe(
            feature_average
            .round(3)
            .rename("Average"),
            use_container_width=True
        )


# =========================================================
# TAB 4 — CORRELATION
# =========================================================

with tab4:

    st.subheader(
        "📈 Features Correlated With Popularity"
    )


    numeric_columns = [
        "popularity",
        "acousticness",
        "danceability",
        "energy",
        "instrumentalness",
        "liveness",
        "loudness",
        "speechiness",
        "tempo",
        "valence",
        "duration_min"
    ]


    available_numeric = [
        column
        for column in numeric_columns
        if column in df.columns
    ]


    if len(available_numeric) >= 2:

        correlation = (
            df[available_numeric]
            .corr()["popularity"]
            .sort_values(
                ascending=False
            )
        )


        correlation_without_target = (
            correlation
            .drop(
                "popularity",
                errors="ignore"
            )
        )


        st.bar_chart(
            correlation_without_target
        )


        st.dataframe(
            correlation
            .round(3)
            .rename(
                "Correlation with Popularity"
            ),
            use_container_width=True
        )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "🎵 Spotify Music Analytics Dashboard | "
    "Python • Pandas • Streamlit"
)