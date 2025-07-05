import streamlit as st

# Use Streamlit's built-in connection (which uses secrets.toml)
conn = st.connection("mysql", type="sql")
