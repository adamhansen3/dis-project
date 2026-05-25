import streamlit as st
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from typing import Literal

load_dotenv()
BASE_URL = os.getenv("DATABASE_URL")
DB_NAME = "spotify-insights"
DB_URL = f"{BASE_URL}/{DB_NAME}"

def init_page(title: str, descr: str | None = None) -> None:
    st.caption("Spotify Insights - A DIS project by kcf105 and mwn201")
    st.title(title)
    if descr:
        st.info(descr)

def get_engine(db_url: Literal['base', 'db'] = 'db'):
    if db_url == 'base':
        return create_engine(BASE_URL, isolation_level="AUTOCOMMIT")
    return create_engine(DB_URL)

def fetch_sql(query: str, params: dict = {}, db_url: Literal['base', 'db'] = 'db', method: Literal["all", "one"] = "all"):
    with get_engine(db_url).begin() as conn:
        res = conn.execute(text(query), params)
        if not res.returns_rows:
            return None
        if method == "all":
            return res.fetchall()
        else:
            return res.fetchone()
