from streamlit.commands.page_config import set_page_config as set_page_config
from streamlit.commands.execution_control import (
    stop as stop,
    rerun as rerun,
    switch_page as switch_page,
)

import streamlit as st
from PIL import Image
import base64
import pandas as pd
from io import BytesIO
from faker import Faker
from PIL import Image

import streamlit as st


st.title(":green[Home Page]")

def app():
    if not st.session_state.get("logged_in"):
        st.warning("Please login first.")
        st.session_state.page = "login"
        return
    
    st.title("Home Page")
    st.write("Welcome to Placely! This is your smart placement assistant.")

# Name of the browser tab in streamlit



st.set_page_config(page_title="Home Page", layout="wide")

st.markdown("---")


# To connect to MySQL database ( Database name - placely)

from sqlalchemy import create_engine
engine = create_engine("mysql+mysqlconnector://root:KK1923@localhost/placely")

def load_data():
    return pd.read_sql("SELECT * FROM students", con=engine)

# Get data from MySQL for filtering, not generating again

df = load_data()



#  >>>>>>>>>>> 1. Show table with full data

st.markdown("<h5 style='text-align:center;'>Placely: Student Placement Dashboard</h5>", unsafe_allow_html=True)

st.dataframe(df, use_container_width=True, hide_index=True)

st.markdown("---")



#  >>>>>>>>>>> 2. Dropdown section for filtering

st.subheader("Apply a Filter")
option = st.selectbox("Choose your option", [
    "-- Select One --",
    "CGPA above 8",
    "Placement Ready: Yes",
    "Programming Score > 70",
    "Batch = 2024",
    "Soft Skills Score < 25"
])



# >>>>>>>>>>> 3. All filters using if elif and else statements

if option == "CGPA above 8":
    filtered_df = df[df["CGPA"] > 8]
elif option == "Placement Ready: Yes":
    filtered_df = df[df["Placement Ready"] == "Yes"]
elif option == "Programming Score > 70":
    filtered_df = df[df["Programming Score"] > 70]
elif option == "Batch = 2024":
    filtered_df = df[df["Batch"] == "2024"]
elif option == "Soft Skills Score < 25":
    filtered_df = df[df["Soft Skills Score"] > 25]
else:
    filtered_df = pd.DataFrame()



# >>>>>>>>>>> 4. Get filtered results to download

if not filtered_df.empty:
    st.subheader("Filtered Student Results")
    st.dataframe(filtered_df, use_container_width=True, hide_index = True)



# >>>>>>>>>>> 5. Get download bitton

    st.download_button(
        label=" Download Filtered CSV ↓",
        data=filtered_df.to_csv(index=False),
        file_name="filtered_students.csv"
    )