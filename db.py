import streamlit as st
from sqlalchemy import create_engine

secrets = st.secrets["mysql"]

engine = create_engine(
    f"mysql+mysqlconnector://{secrets.user}:{secrets.password}@{secrets.host}:{secrets.port}/{secrets.database}"
)


