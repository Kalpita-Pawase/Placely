import streamlit as st
from sqlalchemy import create_engine

user = st.secrets["DB_USER"]
password = st.secrets["DB_PASS"]
host = st.secrets["DB_HOST"]
port = st.secrets["DB_PORT"]
db = st.secrets["DB_NAME"]

engine = create_engine(f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{db}")