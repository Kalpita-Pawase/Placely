from streamlit.commands.page_config import set_page_config as set_page_config
from streamlit.commands.execution_control import (
    stop as stop,
    rerun as rerun,
    switch_page as switch_page,
)

import streamlit as st
import pandas as pd
import random
from faker import Faker
from sqlalchemy import create_engine
from PIL import Image


st.title(":blue[Query Page]")
st.markdown("Ask any query")

def app():
    if not st.session_state.get("logged_in"):
        st.warning("Please login first.")
        st.session_state.page = "login"
        return



st.set_page_config(page_title="Query Insights", layout="wide")

# Connect to MySQL database (placely)
engine = create_engine("mysql+mysqlconnector://root:KK1923@localhost/placely")

# Load data from MySQL
@st.cache_data
def load_data():
    return pd.read_sql("SELECT * FROM students", engine)

df = load_data()


# All Query Options
def run_query(selected):
    if selected == "Top 5 Students":
        filtered_df = df[
            (df["Placement Ready"] == "Yes") &
            (df["Programming Score"] > 80) &
            (df["CGPA"] > 8) &
            (df["Soft Skills Score"] > 40)
            ]
        return filtered_df.sort_values( by=["Programming Score", "CGPA", "Soft Skills Score"], ascending=False ).head(5)

    elif selected == "Average CGPA by Batch":
        return df.groupby("Batch")["CGPA"].mean().reset_index(name="Avg CGPA")

    elif selected == "Students with CGPA > 9":
        return df[df["CGPA"] > 9]

    elif selected == "Low Soft Skills (<20)":
        return df[df["Soft Skills Score"] < 20]
    
    elif selected == "Student Contact Details":
        return df[["Name", "Email", "Contact"]]

    elif selected == "Batch-wise Placement Ready Count":
        return df[df["Placement Ready"] == "Yes"].groupby("Batch").size().reset_index(name="Ready Count")

    elif selected == "Average Soft Skills per Batch":
        return df.groupby("Batch")["Soft Skills Score"].mean().reset_index()

    elif selected == "Programming > Soft Skills":
        return df[df["Programming Score"] > df["Soft Skills Score"]]

    elif selected == "Not Placement Ready":
        return df[df["Placement Ready"] == "NO"]

    elif selected == "Emails of 2023 Batch":
        return df[df["Batch"] == "2023"][["Name", "Email"]]

    elif selected == "Emails of 2024 Batch":
        return df[df["Batch"] == "2024"][["Name", "Email"]]

    elif selected == "Emails of 2025 Batch":
        return df[df["Batch"] == "2025"][["Name", "Email"]]

    elif selected == "Students with Soft Skills > 40 and CGPA > 8":
        return df[(df["Soft Skills Score"] > 40) & (df["CGPA"] > 8)][["Name", "Soft Skills Score","CGPA", "Email", "Contact"]]

    elif selected == "Count by CGPA Range":
        bins = [0, 7, 8, 9, 10]
        labels = ['<7', '7-8', '8-9', '9-10']
        df["CGPA Range"] = pd.cut(df["CGPA"], bins=bins, labels=labels, right=False)
        return df.groupby("CGPA Range").size().reset_index(name="Total")

    else:
        return pd.DataFrame()


query_options = [
    "-- Select One --",
    "Top 5 Students",
    "Average CGPA by Batch",
    "Students with CGPA > 9",
    "Low Soft Skills (<20)",
    "Student Contact Details",
    "Batch-wise Placement Ready Count",
    "Average Soft Skills per Batch",
    "Programming > Soft Skills",
    "Not Placement Ready",
    "Emails of 2023 Batch",
    "Emails of 2024 Batch",
    "Emails of 2025 Batch",
    "Students with Soft Skills > 40 and CGPA > 8",
    "Count by CGPA Range"
]

selected_query = st.selectbox("", query_options)

if selected_query:
    result_df = run_query(selected_query)
    st.dataframe(result_df, use_container_width=True, hide_index=True)

@st.cache_data
def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')

csv = convert_df(result_df)

st.download_button(
    label="Download data as CSV ↓",
    data=csv,
    file_name='query_results.csv',
    mime='text/csv',
)