import streamlit as st
from PIL import Image
import base64
from io import BytesIO


# Set page config (optional)
st.set_page_config(page_title="Placely", page_icon="🎓", layout="centered")


# Optional: Logout in sidebar
if st.session_state.get("logged_in"):
    st.sidebar.markdown("### Account")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.success("Logged out!")
        st.switch_page("pages/1_login_Page.py")

# Load & Center Logo Function
def display_center_logo(path, width=80):
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

# Show centered logo
display_center_logo("icons/Logo.png")

# Welcome Text
st.markdown(
    """
    <h1 style='text-align: center; color: #4CAF50;'>Welcome to Placely 🎓</h1>
    <p style='text-align: center; font-size: 18px; color: #555;'>
        Your one-stop platform for tracking, filtering, and unlocking placement opportunities with ease.
    </p>
    <p style='text-align: center; font-size: 16px; color: #777;'>
        Explore student insights, filter eligibility, and access curated placement data — all in one place
    </p>
    <hr style='width: 60%; margin: auto;'>
    """,
    unsafe_allow_html=True
)

