import streamlit as st
from PIL import Image
import base64
from io import BytesIO


st.title("Login")

def get_image_base64(path):
    img = Image.open(path)
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_bytes = buffered.getvalue()
    return base64.b64encode(img_bytes).decode()

def app():
    img_base64 = get_image_base64("icons/Logo.png")
    st.markdown(
        f"""
        <div style='text-align: center;'>
            <img src='data:image/png;base64,{img_base64}' width='100'/>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.set_page_config(page_title="Login Page", layout="wide")
    st.markdown("<h1 style='text-align: center; color: black;'>Placely!</h1>", unsafe_allow_html=True)
    st.markdown("<h5 style='text-align: center; color: green;'>A placement eligibility application</h1>", unsafe_allow_html=True)
    st.markdown("---")

    user = "hr"
    passw = "123"

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if username == user and password == passw:
                st.session_state.logged_in = True
                st.session_state.page = "home"
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Invalid username or password.")
    else:
        st.markdown("<h5 style='text-align: center; color: black;'>Welcome to Placely!</h5>", unsafe_allow_html=True)