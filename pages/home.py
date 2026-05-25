import streamlit as st
import os
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

from utils.components import init_page

init_page()

load_dotenv()
BASE_URL = os.getenv("DATABASE_URL")
DB_NAME = "spotify-insights"
DB_URL = f"{BASE_URL}/{DB_NAME}"

admin_engine = create_engine(BASE_URL, isolation_level="AUTOCOMMIT")

st.info('To get started, make sure you have:  \n- PostgreSQL installed and running  \n- A database URL set in your .env file (e.g. `DATABASE_URL=postgresql+psycopg2://localhost`)  \n- Installed all requirements from reqs.txt')

st.divider()

st.info('To begin exploring the data, click the button below to load the Excel file into PostgreSQL. This will create a new database called "spotify-insights" and ensure all data is inserted.')
if st.button("Load data from Excel to PostgreSQL"):
    with admin_engine.connect() as conn:
        exists = conn.execute(
            text("SELECT 1 FROM pg_database WHERE datname = :name"),
            {"name": DB_NAME}
        ).fetchone()
        if not exists:
            conn.execute(text(f'CREATE DATABASE "{DB_NAME}"'))

    target_engine = create_engine(DB_URL)
    xl = pd.ExcelFile("data.xlsx")
    with target_engine.begin() as conn:
        for sheet in xl.sheet_names:
            df = pd.read_excel(xl, sheet_name=sheet)
            df.to_sql(sheet, conn, if_exists="replace", index=False)

    st.session_state.data_loaded = True
    st.rerun()

if st.session_state.data_loaded:
    st.success(f"Data inserted into '{DB_NAME}'. You can now navigate to the app's pages to explore the insights!")