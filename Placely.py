import streamlit as st
from streamlit_option_menu import option_menu
from PIL import Image
import base64
from io import BytesIO


def get_image_base64(path):
    img = Image.open(path)
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_bytes = buffered.getvalue()
    return base64.b64encode(img_bytes).decode()

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


# Define pages using relative paths
login_page = st.Page("pages/1_login_page.py", title="Login")
home_page = st.Page("pages/2_home_page.py", title="Home")
query_page = st.Page("pages/3_query_page.py", title="Query")

# Create navigation menu
pg = st.navigation([login_page, home_page, query_page])
pg.run()