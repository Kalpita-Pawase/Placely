import streamlit as st
from PIL import Image
import base64
from io import BytesIO
import time

if st.session_state.get("logged_in"):
    st.success("Already logged in! Redirecting to Home...")
    time.sleep(1)  # Small pause to show the message
    st.switch_page("pages/2_home_page.py")
    


st.markdown(
    "<h1 style='text-align: center; color: #FFBF00;'>Login Page</h1>",
    unsafe_allow_html=True
)

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login"):
    if username == "admin" and password == "123":
        st.success("Logged in successfully!")
        st.session_state.logged_in = True
    else:
        st.error("Invalid credentials")




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
