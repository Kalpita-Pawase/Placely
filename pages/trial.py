import streamlit as st

# Setup correct credentials
VALID_USERNAME = "hr"
VALID_PASSWORD = "123"

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Define Home Page
def home_page():
    st.markdown("<h1 style='text-align: center;'>🏠 Welcome to Placely Dashboard</h1>", unsafe_allow_html=True)
    st.write("You are now logged in as:", st.session_state.username)

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""  # Clear username
        st.experimental_rerun()

# Define Login Page
def login_page():
    st.markdown("<h1 style='text-align: center; color: black;'>Placely!</h1>", unsafe_allow_html=True)
    st.markdown("<h5 style='text-align: center; color: green;'>A placement eligibility application</h5>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("<h4 style='text-align: center; color: black;'>Login with your credentials</h4>", unsafe_allow_html=True)

    st.text_input("Username", key="username")
    st.text_input("Password", type="password", key="password")

    if st.button("Login"):
        if st.session_state.username == VALID_USERNAME and st.session_state.password == VALID_PASSWORD:
            st.session_state.logged_in = True
            st.success("Successfully logged in!")
            st.experimental_run()  # move to home
        else:
            st.error("Invalid credentials, please try again :(")
            st.session_state.password = ""  # Clear password field

# Control logic
if st.session_state.logged_in:
    home_page()
else:
    login_page()