from utils.components import init_page, fetch_sql
import streamlit as st
import pandas as pd
import re

init_page("Analytics")

total_listens = fetch_sql("SELECT COUNT(*) FROM listens", method="one")[0]
total_users = fetch_sql("SELECT COUNT(*) FROM \"user\"", method="one")[0]
total_tracks = fetch_sql("SELECT COUNT(*) FROM track", method="one")[0]
total_artists = fetch_sql("SELECT COUNT(*) FROM artist", method="one")[0]

c1, c2, c3, c4 = st.columns(4)

c1.metric("Listens", f"{total_listens:,}")
c2.metric("Users", total_users)
c3.metric("Tracks", total_tracks)
c4.metric("Artists", total_artists)

st.divider()

top_tracks = fetch_sql("""
SELECT t.title, COUNT(*) listens
FROM listens l
JOIN track t ON l.track_id = t.track_id
GROUP BY t.title
ORDER BY listens DESC
LIMIT 10
""")

df_tracks = pd.DataFrame(top_tracks, columns=["Track", "Listens"])

st.subheader("Top Tracks")
st.bar_chart(df_tracks.set_index("Track"))

top_artists = fetch_sql("""
SELECT a.artist_name, COUNT(*) listens
FROM listens l
JOIN track t ON l.track_id = t.track_id
JOIN artist a ON t.artist_id = a.artist_id
GROUP BY a.artist_name
ORDER BY listens DESC
LIMIT 10
""")

df_artists = pd.DataFrame(top_artists, columns=["Artist", "Listens"])

st.subheader("Top Artists")
st.bar_chart(df_artists.set_index("Artist"))

st.divider()

best_track = df_tracks.iloc[0]["Track"]
best_artist = df_artists.iloc[0]["Artist"]

st.subheader("Insights")

st.success(f"""
🎵 Most popular track: {best_track}

🎤 Most popular artist: {best_artist}

👥 Total users: {total_users}

▶️ Total listens: {total_listens:,}
""")

st.divider()
st.subheader("Regex Track Analysis")

pattern = st.text_input(
    "Find tracks using regex",
    placeholder="e.g. love|heart"
)

if pattern:
    try:
        all_tracks = fetch_sql("SELECT title FROM track")

        matches = [
            title[0]
            for title in all_tracks
            if re.search(pattern, title[0], re.IGNORECASE)
        
        ]

        st.write(f"Found {len(matches)} matching tracks")

        if matches:
            st.dataframe(pd.DataFrame(matches, columns=["Track"]))

    except re.error as e:
        st.error(f"Invalid regex: {e}")