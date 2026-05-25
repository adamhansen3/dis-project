import streamlit as st
import os
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()
BASE_URL = os.getenv("DATABASE_URL")
DB_NAME = "spotify-insights"
DB_URL = f"{BASE_URL}/{DB_NAME}"

admin_engine = create_engine(BASE_URL, isolation_level="AUTOCOMMIT")

st.title("Spotify Insights")

with admin_engine.connect() as conn:
    version = conn.execute(text("SELECT version();")).fetchone()[0]
st.write("PostgreSQL works and is running the following version:")
st.code(version)

st.divider()

if st.button("Load data from Excel"):
    with admin_engine.connect() as conn:
        exists = conn.execute(
            text("SELECT 1 FROM pg_database WHERE datname = :name"),
            {"name": DB_NAME}
        ).fetchone()
        if not exists:
            conn.execute(text(f'CREATE DATABASE "{DB_NAME}"'))

    # Insert all sheets as tables into spotify-insights
    target_engine = create_engine(DB_URL)
    xl = pd.ExcelFile("data.xlsx")
    with target_engine.begin() as conn:
        for sheet in xl.sheet_names:
            df = pd.read_excel(xl, sheet_name=sheet)
            df.to_sql(sheet, conn, if_exists="replace", index=False)

    st.success(f"Data inserted into '{DB_NAME}' — tables: {', '.join(xl.sheet_names)}")