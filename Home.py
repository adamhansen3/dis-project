import streamlit as st
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

st.title("PostgreSQL + Streamlit")

query = "SELECT version();"

with engine.connect() as connection:
    result = connection.execute(text(query))
    version = result.fetchone()[0]

st.write("Connected to PostgreSQL!")
st.code(version)