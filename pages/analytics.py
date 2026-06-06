from utils.components import init_page, fetch_sql
import streamlit as st
import pandas as pd
import re
import altair as alt

init_page("Analytics")

st.write(
    "The app shows insights about users, demographics, songs, artists, "
    "popularity, average duration, and factors that may affect listening behaviour."
)

# Overview metrics
total_listens = fetch_sql("SELECT COUNT(*) FROM listens", method="one")[0]
total_users = fetch_sql('SELECT COUNT(*) FROM "user"', method="one")[0]
total_tracks = fetch_sql("SELECT COUNT(*) FROM track", method="one")[0]
total_artists = fetch_sql("SELECT COUNT(*) FROM artist", method="one")[0]

c1, c2, c3, c4 = st.columns(4)

c1.metric("Listens", f"{total_listens:,}")
c2.metric("Users", total_users)
c3.metric("Tracks", total_tracks)
c4.metric("Artists", total_artists)

st.divider()

# Top tracks
top_tracks = fetch_sql("""
SELECT t.title, COUNT(*) listens
FROM listens l
JOIN track t ON l.track_id = t.track_id
GROUP BY t.title
ORDER BY listens DESC
LIMIT 10
""")

df_tracks = pd.DataFrame(top_tracks, columns=["Track", "Listens"])
df_tracks = df_tracks.sort_values("Listens", ascending=False)

st.subheader("Top Tracks")
st.bar_chart(df_tracks.set_index("Track"))

# Top artists
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
df_artists = df_artists.sort_values("Listens", ascending=False)

st.subheader("Top Artists")
st.bar_chart(df_artists.set_index("Artist"))

st.divider()

# NATIONALITY
st.subheader("Listens by Nationality")

nationality_listens = fetch_sql("""
SELECT u.nationality,
       COUNT(*) AS listens
FROM listens l
JOIN "user" u ON l.user_id = u.user_id
GROUP BY u.nationality
ORDER BY listens DESC
""")

df_nationality_listens = pd.DataFrame(
    nationality_listens,
    columns=["Nationality", "Listens"]
)

df_nationality_listens["Listens"] = pd.to_numeric(
    df_nationality_listens["Listens"]
)

chart = alt.Chart(df_nationality_listens).mark_bar().encode(
    x=alt.X("Listens:Q"),
    y=alt.Y("Nationality:N", sort="-x")
)

st.altair_chart(chart, width="stretch")

st.divider()

# USERS BY GENDER
st.subheader("Users by Gender")

gender_data = fetch_sql("""
SELECT gender, COUNT(*) AS users
FROM "user"
GROUP BY gender
ORDER BY users DESC
""")

df_gender = pd.DataFrame(
    gender_data,
    columns=["Gender", "Users"]
)

df_gender["Users"] = pd.to_numeric(
    df_gender["Users"]
)

chart = alt.Chart(df_gender).mark_bar().encode(
    x=alt.X("Users:Q"),
    y=alt.Y("Gender:N", sort="-x")
)

st.altair_chart(chart, width="stretch")

# USERS BY AGE
st.subheader("Users by Age")

age_data = fetch_sql("""
SELECT
    EXTRACT(YEAR FROM CURRENT_DATE) - birth_year AS age,
    COUNT(*) AS users
FROM "user"
GROUP BY age
ORDER BY age
""")

df_age = pd.DataFrame(
    age_data,
    columns=["Age", "Users"]
)

df_age["Age"] = pd.to_numeric(df_age["Age"])
df_age["Users"] = pd.to_numeric(df_age["Users"])

st.line_chart(df_age.set_index("Age"))

st.divider()

# Track statistics
avg_duration = fetch_sql("""
SELECT ROUND(AVG(duration_seconds), 2)
FROM track
""", method="one")[0]

avg_listens_per_user = round(total_listens / total_users, 2)
avg_listens_per_track = round(total_listens / total_tracks, 2)

st.subheader("Track Statistics")

c1, c2, c3 = st.columns(3)

c1.metric("Avg Duration (sec)", avg_duration)
c2.metric("Listens / User", avg_listens_per_user)
c3.metric("Listens / Track", avg_listens_per_track)

st.divider()

# Listens by release year
release_year_data = fetch_sql("""
SELECT t.release_year,
       COUNT(*) AS listens
FROM listens l
JOIN track t ON l.track_id = t.track_id
GROUP BY t.release_year
ORDER BY t.release_year
""")

df_year = pd.DataFrame(
    release_year_data,
    columns=["Release Year", "Listens"]
)

df_year["Release Year"] = pd.to_numeric(df_year["Release Year"])
df_year["Listens"] = pd.to_numeric(df_year["Listens"])

st.subheader("Listening Behaviour by Release Year")
st.line_chart(df_year.set_index("Release Year"))

st.divider()

# Most active users
active_users = fetch_sql("""
SELECT u.user_name,
       COUNT(*) AS listens
FROM listens l
JOIN "user" u ON l.user_id = u.user_id
GROUP BY u.user_name
ORDER BY listens DESC
LIMIT 10
""")

df_users = pd.DataFrame(
    active_users,
    columns=["User", "Listens"]
)

df_users["Listens"] = pd.to_numeric(
    df_users["Listens"]
)

st.subheader("Most Active Users")

chart = alt.Chart(df_users).mark_bar().encode(
    x=alt.X("Listens:Q"),
    y=alt.Y("User:N", sort="-x")
)

st.altair_chart(chart, width="stretch")

st.divider()

# Listening Behaviour by Gender
st.subheader("Listening Behaviour by Gender")

gender_listens = fetch_sql("""
SELECT
    u.gender,
    COUNT(*) AS listens
FROM listens l
JOIN "user" u ON l.user_id = u.user_id
GROUP BY u.gender
ORDER BY listens DESC
""")

df_gender_listens = pd.DataFrame(
    gender_listens,
    columns=["Gender", "Listens"]
)

df_gender_listens["Listens"] = pd.to_numeric(
    df_gender_listens["Listens"]
)

chart = alt.Chart(df_gender_listens).mark_bar().encode(
    x=alt.X("Listens:Q"),
    y=alt.Y("Gender:N", sort="-x")
)

st.altair_chart(chart, width="stretch")

st.divider()

# Insights
best_track = df_tracks.iloc[0]["Track"]
best_artist = df_artists.iloc[0]["Artist"]

top10_total = df_tracks["Listens"].sum()
popularity_share = round(top10_total / total_listens * 100, 2)

st.subheader("Insights")

st.success(f"""
🎵 Most popular track: {best_track}

🎤 Most popular artist: {best_artist}

👥 Total users: {total_users}

▶️ Total listens: {total_listens:,}

⏱️ Average track duration: {avg_duration} sec

📈 Top 10 tracks account for {popularity_share}% of all listens

🎧 Average listens per user: {avg_listens_per_user}
""")

st.divider()

# Regex
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
            st.dataframe(
                pd.DataFrame(matches, columns=["Track"])
            )

    except re.error as e:
        st.error(f"Invalid regex: {e}")