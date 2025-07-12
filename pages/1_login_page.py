# Importing
import streamlit as st
from PIL import Image
from sqlalchemy import create_engine
import base64
from io import BytesIO
import time
from db import engine




# ------------------------ Set Page Config ------------------------


st.set_page_config(page_title="Login Page", layout="wide")


# ------------------------ Display Centered Logo ------------------------


def display_center_logo(path, width=100):
    img = Image.open(path)
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_base64 = base64.b64encode(buffered.getvalue()).decode()
    st.markdown(
        f"""
        <div style='text-align: center;'>
            <img src='data:image/png;base64,{img_base64}' width='{width}'/>
        </div>
        """,
        unsafe_allow_html=True
    )

display_center_logo("icons/Logo.png", width=80)



# ------------------------ Title ------------------------


st.markdown("<h1 style='text-align: center; color: #4CAF50;'>Login</h1>", unsafe_allow_html=True)


# ------------------------ If already logged in ------------------------


if st.session_state.get("logged_in"):
    st.success("Already logged in! Redirecting to Home...")
    time.sleep(1)
    st.switch_page("pages/2_home_page.py")



# ------------------------ Logout Button ------------------------


if st.session_state.get("logged_in"):
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.success("You have been logged out!")
        st.switch_page("pages/1_login_Page.py")



# ------------------------ Login Form ------------------------


username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login"):
    if username == "admin" and password == "123":
        st.success("Logged in successfully!")
        st.session_state.logged_in = True
        time.sleep(1)
        st.switch_page("pages/2_home_page.py")
    else:
        st.error("Invalid credentials")
