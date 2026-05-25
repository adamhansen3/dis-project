import streamlit as st
import pandas as pd

from utils.components import init_page, fetch_sql, DB_NAME, get_engine

init_page('Spotify Insights - Home')

st.info('To get started, make sure you have:  \n- PostgreSQL installed and running  \n- A database URL set in your .env file (e.g. `DATABASE_URL=postgresql+psycopg2://localhost`)  \n- Installed all requirements from reqs.txt')

st.divider()

st.info('To begin exploring the data, click the button below to load the Excel file into PostgreSQL. This will create a new database called "spotify-insights" and ensure all data is inserted.')
if st.button("Load data from Excel to PostgreSQL"):
    exists = fetch_sql("SELECT 1 FROM pg_database WHERE datname = :name", {"name": DB_NAME}, db_url='base', method='one')
    if not exists:
        fetch_sql(f'CREATE DATABASE "{DB_NAME}"', db_url='base')

    xl = pd.ExcelFile("data.xlsx")
    with get_engine('db').begin() as conn:
        for sheet in xl.sheet_names:
            df = pd.read_excel(xl, sheet_name=sheet)
            df.to_sql(sheet, conn, if_exists="replace", index=False)

    st.session_state.data_loaded = True
    st.rerun()

if st.session_state.data_loaded:
    st.success(f"Data inserted into '{DB_NAME}'. You can now navigate to the app's pages to explore the insights!")