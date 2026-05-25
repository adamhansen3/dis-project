import streamlit as st
from utils.components import fetch_sql

@st.cache_data
def get_favourites():
    return fetch_sql("SELECT * FROM favourites")

@st.cache_data
def get_tracks():
    return fetch_sql("SELECT * FROM track")

@st.cache_data
def get_artists():
    return fetch_sql("SELECT * FROM artist")

@st.cache_data
def get_listens_for_tracks(track_ids: tuple):
    if not track_ids:
        return []
    return fetch_sql(
        "SELECT track_id, timestamp FROM listens WHERE track_id = ANY(:ids)",
        {"ids": list(track_ids)}
    )

@st.cache_data
def get_listens_for_artists(artist_ids: tuple):
    if not artist_ids:
        return []
    return fetch_sql(
        """SELECT t.artist_id, l.timestamp FROM listens l
           JOIN track t ON l.track_id = t.track_id
           WHERE t.artist_id = ANY(:ids)""",
        {"ids": list(artist_ids)}
    )
