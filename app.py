import streamlit as st

st.set_page_config(
    page_title="Spotify Insights",
    page_icon="🎵",
)

pages = {
    "Pages": [
        st.Page("pages/home.py", title="Home", icon="🏠", default=True),
        st.Page("pages/database.py", title="Database", icon="📊"),
        st.Page("pages/analytics.py", title="Analytics", icon="🧠"),
        st.Page("pages/favourites.py", title="Favourites", icon="⭐️"),
    ]
}

pg = st.navigation(pages, position="hidden")

st.session_state.setdefault("data_loaded", False)
with st.sidebar:
    st.image("logo.png")

    st.header("Pages")

    st.page_link("pages/home.py", label="Home", icon="🏠")
    st.page_link("pages/database.py", label="Database", icon="📊", disabled=not st.session_state.data_loaded)
    st.page_link("pages/analytics.py", label="Analytics", icon="🧠", disabled=not st.session_state.data_loaded)
    st.page_link("pages/favourites.py", label="Favourites", icon="⭐️", disabled=not st.session_state.data_loaded)

    st.divider()

    st.write(
        "With Spotify Insights, you can explore synthetic Spotify data with 50 users and 3,000 listens. "
        "The app shows insights about users, demographics, songs, artists, popularity, average duration, "
        "and factors that may affect listening behaviour. You can also favourite songs and artists to "
        "follow their performance in a Favourites dashboard."
    )

pg.run()