                                                                                              # Importing...


import streamlit as st
from PIL import Image
import base64
from io import BytesIO
import time
from db_connection import engine


                                                                                                
                                                                                        # Load and Logo preview above TITLE - LOGIN


def display_center_logo(path, width=100):
    img = Image.open(path)
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_bytes = buffered.getvalue()
    img_base64 = base64.b64encode(img_bytes).decode()

    st.markdown(
        f"""
        <div style='text-align: center;'>
            <img src='data:image/png;base64,{img_base64}' width='{width}'/>
        </div>
        """,
        unsafe_allow_html=True
    )

display_center_logo("icons/Logo.png", width=80)

st.markdown("<h1 style='text-align: center; color: #4CAF50;'>Login</h1>", unsafe_allow_html=True)


                                                                                            # Redirecting after Login


if st.session_state.get("logged_in"):
    st.success("Already logged in! Redirecting to Home...")
    time.sleep(1)  
    st.switch_page("pages/2_home_page.py")


                                                                                            # Logout Button 


if st.session_state.get("logged_in"):
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.success("You have been logged out!")
        st.switch_page("pages/1_login_Page.py")


                                                                                           # ALL ABOUT THE LOGIN LOGIC 


username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login"):
    if username == "admin" and password == "123":
        st.write("You can now access the Home Page and Query Page...")
        st.success("Logged in successfully!")
        st.session_state.logged_in = True
    else:
        st.error("Invalid credentials")


                                                                                           # Centered Logo above the LOGIN TITLE


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


                                                                                          # Name of the browser tab in streamlit


    st.set_page_config(page_title="Login Page", layout="wide")
