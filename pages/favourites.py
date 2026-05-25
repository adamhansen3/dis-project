import altair as alt
import streamlit as st
import pandas as pd

from utils.components import init_page, fetch_sql
from utils.query import get_artists, get_favourites, get_tracks, get_listens_for_tracks, get_listens_for_artists

init_page("Favourites", "Select below to add your favourite tracks and artists!")

def add_favourite(id: str, type: str):
    fetch_sql(
        "INSERT INTO favourites (favourite_id, type) VALUES (:id, :type)",
        {"id": id, "type": type}
    )
    get_favourites.clear()
    st.rerun()

favourites = get_favourites()
tracks = get_tracks()
artists = get_artists()

cols = st.columns(2)
with cols[0]:
    ftype = st.selectbox("Select type", ["artist", "track"])
with cols[1]:
    lst = tracks if ftype == "track" else artists
    new_fav = st.selectbox(f"Select favourite {ftype}", lst, format_func=lambda x: x[1])

if st.button("Add to favourites", disabled=not new_fav, type="primary"):
    add_favourite(new_fav[0], ftype)

st.divider()

if favourites:
    
    if st.button("Clear favourites", type="secondary"):
        fetch_sql("DELETE FROM favourites")
        get_favourites.clear()
        st.rerun()

    st.write(" ")

    track_map = {t[0]: t[1] for t in tracks}
    artist_map = {a[0]: a[1] for a in artists}

    fav_tracks = [track_map[f[0]]  for f in favourites if f[1] == "track"]
    fav_artists = [artist_map[f[0]] for f in favourites if f[1] == "artist"]

    if fav_artists:
        st.write("**Favourite Artists**  \n- " + "  \n- ".join(fav_artists))
    if fav_tracks:
        st.write("**Favourite Tracks**  \n- " + "  \n- ".join(fav_tracks))

    st.divider()

    fav_track_ids = [f[0] for f in favourites if f[1] == "track"]
    fav_artist_ids = [f[0] for f in favourites if f[1] == "artist"]
    track_full = {t[0]: t for t in tracks}
    artist_full = {a[0]: a for a in artists}
    now = pd.Timestamp.now()
    cutoff = now - pd.DateOffset(days=365)
    mid = now - pd.DateOffset(months=6)

    def monthly_chart(sub):
        monthly = sub.groupby("month").size().reset_index()
        monthly.columns = ["month", "Listens"]
        monthly["month"] = monthly["month"].dt.to_timestamp()
        chart = alt.Chart(monthly).mark_line(point=True).encode(
            x=alt.X("month:T", axis=alt.Axis(format="%b %Y", labelAngle=-30, title=None)),
            y=alt.Y("Listens:Q", title="Listens"),
        ).properties(height=220)
        st.altair_chart(chart, use_container_width=True)

    def trend_delta(sub):
        recent = int((sub["timestamp"] >= mid).sum())
        older = int(((sub["timestamp"] >= cutoff) & (sub["timestamp"] < mid)).sum())
        return recent, recent - older

    if fav_artist_ids:
        raw = get_listens_for_artists(tuple(fav_artist_ids))
        df = pd.DataFrame(raw, columns=["artist_id", "timestamp"])
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df["month"] = df["timestamp"].dt.to_period("M")

        for aid in fav_artist_ids:
            sub = df[df["artist_id"] == aid]
            a = artist_full[aid]
            recent, delta = trend_delta(sub)
            img_col, info_col = st.columns([1, 4])
            with img_col:
                if a[2]:
                    st.image(a[2], width=110)
            with info_col:
                st.markdown(f"##### {a[1]}")
                c1, c2, c3 = st.columns(3)
                c1.metric("Total listens", len(sub))
                c2.metric("Last 12 months", int((sub["timestamp"] >= cutoff).sum()))
                c3.metric("Last 6 months", recent, delta=delta)
            if not sub.empty:
                monthly_chart(sub)
            st.divider()

    if fav_track_ids:
        raw = get_listens_for_tracks(tuple(fav_track_ids))
        df = pd.DataFrame(raw, columns=["track_id", "timestamp"])
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df["month"] = df["timestamp"].dt.to_period("M")

        for tid in fav_track_ids:
            sub = df[df["track_id"] == tid]
            t = track_full[tid]
            recent, delta = trend_delta(sub)
            st.markdown(f"##### {t[1]}")
            c1, c2, c3 = st.columns(3)
            c1.metric("Total listens", len(sub))
            c2.metric("Last 12 months", int((sub["timestamp"] >= cutoff).sum()))
            c3.metric("Last 6 months", recent, delta=delta)
            if not sub.empty:
                monthly_chart(sub)
            st.divider()

else:
    st.info("No favourites yet. Click the button above to add one!")
