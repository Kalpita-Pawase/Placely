                                                                                                # Importing...


import streamlit as st
from PIL import Image
import base64
from io import BytesIO
from db_connection import engine


                                                                                               
                                                                                                # Show logout only if logged in
# Connect to MySQL
conn = st.connection("mysql", type="sql")

# Query data
df = conn.query("SELECT * FROM students", ttl=600)
st.dataframe(df)

# Download CSV
csv = df.to_csv(index=False).encode('utf-8')
st.download_button("Download CSV ↓", data=csv, file_name="students.csv", mime="text/csv")




if st.session_state.get("logged_in"):
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.success("You have been logged out!")
        st.switch_page("pages/1_login_Page.py")


                                                                                                # Load and encode logo


def get_image_base64(path):
    img = Image.open(path)
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

img_base64 = get_image_base64("icons/Logo.png")

                                                                                                
                                                                                                 # Inject logo at top-right corner


st.markdown(
    f"""
    <style>
        .corner-logo {{
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 100;
        }}
    </style>
    <div class="corner-logo">
        <img src="data:image/png;base64,{img_base64}" width="60"/>
    </div>
    """,
    unsafe_allow_html=True
)

                                                                                                 # Welcome content


st.markdown(
    """
    <div style='text-align: center;'>
        <h1 style='color: #4CAF50;'>Welcome to Placely 🎓</h1>
        <p style='font-size: 18px; color: #555;'>Your one-stop platform for tracking, filtering, 
        and unlocking placement opportunities with ease.</p>
        <p style='font-size: 16px; color: #777;'>Explore student insights, 
        filter eligibility, and access curated placement data</p>
        <hr style='border: 1px solid #ccc; width: 60%; margin: auto;'>
    </div>
    """,
    unsafe_allow_html=True
)
