                                                                                                    # Importing...


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


                                                        # Load and Logo at the top right corner of the web page


def get_image_base64(path):
    img = Image.open(path)
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

img_base64 = get_image_base64("icons/Logo.png")


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


                                                                                                                  # Logout button



if st.session_state.get("logged_in"):
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.success("You have been logged out!")
        st.switch_page("pages/1_login_Page.py")

if "logged_in" not in st.session_state or not st.session_state.logged_in:
        st.warning("Please log in first.")
        st.stop()



                                                        # Title, Sub - Title and adding section the the web page



st.markdown("<h1 style='color: #4CAF50;'>Home Page</h1>", unsafe_allow_html=True)

st.markdown(
    "<h6 style='color: gray;'>Your central dashboard for Placely insights</h6>",
    unsafe_allow_html=True
)

st.markdown("---")



                                                                                           # Request to Login to acess Home Page



def app():
    if not st.session_state.get("logged_in"):
        st.warning("Please login first.")
        st.session_state.page = "login"
        return
    


                                                                                            # Name of the browser tab in streamlit



st.set_page_config(page_title="Home Page", layout="wide")




                                          # Table name - students , Database name - placely



from sqlalchemy import create_engine
engine = create_engine("mysql+mysqlconnector://root:KK1923@localhost/placely")

def load_data():
    return pd.read_sql("SELECT * FROM students", con=engine)



                                                                                       # For fiilteration, pulling data from MySQL 



df = load_data()



                                                                                        #  >>>>>>>>>>> 1. Show table with full data



st.markdown("<h4 style='text-align:center;'>Student's Dashboard</h4>", unsafe_allow_html=True)
st.markdown("<h6 style='text-align:center; color : gray'>- unfiltered data -</h6>", unsafe_allow_html=True)

st.dataframe(df, use_container_width=True, hide_index=True)



                                                                                          #  >>>>>>>>>>> 2. Dropdown for filtering


# 1. Load data from MySQL based on query
@st.cache_data
def load_data(query):
    return pd.read_sql(query, engine)

# 2. Student Filters UI
st.markdown(
    "<h5 style='color: black;'>Filter Student Data</h5>",
    unsafe_allow_html=True
)

batch = st.selectbox("Select Batch", ["-- Select One --","Batch-1", "Batch-2"])
city = st.selectbox("Select City", ["-- Select One --","Pune", "Tamil Nadu"])
gender = st.radio("Select Gender", ["Male", "Female", "Other"])
enroll_year = st.radio("Enrollment Year", [ 2019,2020 ])
grad_year = st.select_slider("Graduation Year", options=list(range(2020, 2023)))

# 3. Query to fetch filtered student data
if st.button("Show Student Results"):
    query = f"""
    SELECT * FROM students
    WHERE course_batch = '{batch}'
    AND city = '{city}'
    AND gender = '{gender}'
    AND graduation_year = {grad_year}
    AND enrollment_year = {enroll_year}
    """
    df = pd.read_sql(query, engine)

    if not df.empty:
        csv = df.to_csv(index=False).encode('utf-8')
        st.dataframe(df.style.set_properties(**{'background-color': "#e8fcfe"}), use_container_width=True, hide_index=True)
        st.download_button("Download Filtered Student as CSV ↓", data=csv, file_name="StudentData_filtered.csv", mime="text/csv")
    else:
        st.warning("No records found for the selected filters.")
else:
    st.info("Set filters and click 'Show Student Results'")



st.markdown("---")

                              # Table name - programming , Database name - placely



from sqlalchemy import create_engine
engine = create_engine("mysql+mysqlconnector://root:KK1923@localhost/placely")

def load_data():
    return pd.read_sql("SELECT * FROM programming", con=engine)



                                                                                       # For fiilteration, pulling data from MySQL 



df = load_data()



                                                                                       #  >>>>>>>>>>> 1. Show table with full data



st.markdown("<h4 style='text-align:center;'>Programming Scores</h4>", unsafe_allow_html=True)
st.markdown("<h6 style='text-align:center; color : gray'>- unfiltered data -</h6>", unsafe_allow_html=True)

st.dataframe(df, use_container_width=True, hide_index=True)




                                                                                          #  >>>>>>>>>>> 2. Dropdown for filtering
@st.cache_data
def load_data(query):
    return pd.read_sql(query, engine)

st.markdown(
    "<h5 style='color: black;'>Filter Programming Data</h5>",
    unsafe_allow_html=True
)

lang = st.selectbox("Programming Language", ["-- Select One --","Python", "Java", "SQL"])
prob_solved = st.slider("Problems Solved", 50, 500, 0)
assess_completed = st.slider("Assessments Completed", 5, 20, 0)
min_projects = st.slider("Minimum Projects Completed", 1, 5, 0)
cert_earned = st.slider("Certificates Earned", 0, 3, 0)
latest_proj_score = st.slider("Latest Project Scores", 50, 100, 0)

                                                                                                        # filters based on query
if st.button("Show Programming Results"):
    query = f"""
    SELECT s.student_id, s.name, p.language, p.problems_solved, p.assessments_completed,
           p.mini_projects, p.certifications_earned, p.latest_project_score
    FROM programming p
    JOIN students s ON s.student_id = p.student_id
    WHERE p.language = '{lang}'
    AND p.problems_solved >= {prob_solved}
    AND p.assessments_completed >= {assess_completed}
    AND p.mini_projects >= {min_projects}
    AND p.certifications_earned >= {cert_earned}
    AND p.latest_project_score >= {latest_proj_score}
    """
    df = pd.read_sql(query, engine)
    
    if not df.empty:
        csv = df.to_csv(index=False).encode('utf-8')
        st.dataframe(df.style.set_properties(**{'background-color': "#e8fcfe"}), use_container_width=True, hide_index=True)
        st.download_button("Download Filtered Programming as CSV ↓", data=csv, file_name="Filtered_ProgrammingData.csv", mime="text/csv")
    else:
        st.warning("No records found for the selected filters.")
else:
    st.info("Set filters and click 'Show Student Results'")


st.markdown("---")


                                       # Table name - soft_skills , Database name - placely



from sqlalchemy import create_engine
engine = create_engine("mysql+mysqlconnector://root:KK1923@localhost/placely")

def load_data():
    return pd.read_sql("SELECT * FROM soft_skills", con=engine)



                                                                                       # For fiilteration, pulling data from MySQL 



df = load_data()



                                                                                       #  >>>>>>>>>>> 1. Show table with full data



st.markdown("<h4 style='text-align:center;'>Soft Skills Scores</h4>", unsafe_allow_html=True)
st.markdown("<h6 style='text-align:center; color : gray'>- unfiltered data -</h6>", unsafe_allow_html=True)

st.dataframe(df, use_container_width=True, hide_index=True)




                                                                                          #  >>>>>>>>>>> 2. Dropdown for filtering
@st.cache_data
def load_data(query):
    return pd.read_sql(query, engine)

st.markdown(
    "<h5 style='color: black;'>Filter Soft Skills Data</h5>",
    unsafe_allow_html=True
)


comm = st.slider("Minimum Communication Score", 60, 100, 0)
teamwork = st.slider("Minimum Teamwork Score", 60, 100, 0)
presentation = st.slider("Presentation", 60, 100, 0)
leadership = st.slider("Minimum Leadership", 60, 100, 0)
critic_thinking = st.slider("Critical Thinking", 60, 100, 0)
interpersonal = st.slider("Interpersonal Skills", 60, 100, 0)


                                                                   # >>>>>>>>>>> 3. Filter Logic using if elif and else statements


if st.button("Show Soft Skill Results"):
    query = f"""
    SELECT s.student_id, s.name, ss.communication, ss.teamwork, ss.presentation,
           ss.leadership, ss.critical_thinking, ss.interpersonal_skills
    FROM soft_skills ss
    JOIN students s ON s.student_id = ss.student_id
    WHERE ss.communication >= {comm}
    AND ss.teamwork >= {teamwork}
    AND ss.presentation >= {presentation}
    AND ss.leadership >= {leadership}
    AND ss.critical_thinking >= {critic_thinking}
    AND ss.interpersonal_skills >= {interpersonal}
    """
    df = pd.read_sql(query, engine)
    
    if not df.empty:
        csv = df.to_csv(index=False).encode('utf-8')
        st.dataframe(df.style.set_properties(**{'background-color': "#e8fcfe"}), use_container_width=True, hide_index=True)
        st.download_button("Download Filtered Soft Skills as CSV ↓", data=csv, file_name="Filtered_SoftSkills_Data.csv", mime="text/csv")
    else:
        st.warning("No records found for the selected filters.")
else:
    st.info("Set filters and click 'Show Student Results'")


st.markdown("---")



                                    # Table name - placements , Database name - placely



from sqlalchemy import create_engine
engine = create_engine("mysql+mysqlconnector://root:KK1923@localhost/placely")

def load_data():
    return pd.read_sql("SELECT * FROM placements", con=engine)



                                                                                       # For fiilteration, pulling data from MySQL 



df = load_data()



                                                                                       #  >>>>>>>>>>> 1. Show table with full data



st.markdown("<h4 style='text-align:center;'>Placement Eligibility</h4>", unsafe_allow_html=True)
st.markdown("<h6 style='text-align:center; color : gray'>- unfiltered data -</h6>", unsafe_allow_html=True)

st.dataframe(df, use_container_width=True, hide_index=True)




                                                                                          #  >>>>>>>>>>> 2. Dropdown for filtering

st.markdown(
    "<h5 style='color: black;'>Filter Placement Data</h5>",
    unsafe_allow_html=True
)


# -------------------- Filter Inputs --------------------

mock_score = st.slider("Minimum Mock Interview Score", 0, 100, 0)
intern_completed = st.slider("Minimum Internships Completed", 0, 3, 0)

# Placement status
placed_input = st.selectbox("Student ready to be placed?", ["-- Select One --", "Ready", "Placed", "Not Ready"])

# Show company dropdown only if Ready or Placed
show_company = placed_input in ["Ready", "Placed"]
company_input = None
if show_company:
    company_input = st.selectbox("Check in which company", ["-- Select One --", "TCS", "Infosys", "Google", "Microsoft", "None"])

# Load data when button clicked
if st.button("Show Placement Results"):
    # SQL Conditions
    status_condition = f"p.placement_status = '{placed_input}'"
    mock_condition = f"p.mock_interview_score >= {mock_score}"
    intern_condition = f"p.internships_completed >= {intern_completed}"
    company_condition = f"AND p.company_name = '{company_input}'" if show_company and company_input != "-- Select One --" else ""

    # Final query
    query = f"""
    SELECT 
        p.placement_id, s.student_id, s.name,
        p.mock_interview_score, p.internships_completed,
        p.placement_status, p.company_name
    FROM placements p
    JOIN students s ON p.student_id = s.student_id
    WHERE {status_condition}
      AND {mock_condition}
      AND {intern_condition}
      {company_condition}
    """

    # Fetch & display data
    df = pd.read_sql(query, engine)

    if not df.empty:
        # Drop company_name column if placement_status is Not Ready
        if placed_input == "Not Ready" and "company_name" in df.columns:
            df = df.drop(columns=["company_name"])

        st.dataframe(df.style.set_properties(**{
            'background-color': '#e8f9fc',
            'color': '#000'
        }), use_container_width=True, hide_index=True)


        # Download option
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download CSV", csv, file_name="filtered_placements.csv", mime="text/csv")
    else:
        st.warning("⚠️ No matching records found.")
else:
    st.info("Set filters and click 'Show Placement Results' to view placement data.")




st.markdown("---")