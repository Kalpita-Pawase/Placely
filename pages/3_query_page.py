# -------------------- Imports --------------------
import streamlit as st
import pandas as pd
from PIL import Image
import base64
from io import BytesIO
from db_connection import conn


# -------------------- Set Browser Tab Title --------------------


st.set_page_config(page_title="Query Insights", layout="wide")



# -------------------- MySQL Connection via Streamlit --------------------


conn = st.connection("mysql", type="sql")



# -------------------- Logo Display --------------------


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



# -------------------- Logout Button --------------------


if st.session_state.get("logged_in"):
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.success("You have been logged out!")
        st.switch_page("pages/1_login_Page.py")



# -------------------- Session Check --------------------


if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Please log in first.")
    st.stop()



# -------------------- Page Title --------------------


st.markdown("<h1 style='text-align: center; color: #FFBF00;'>Get Query Insights</h1>", unsafe_allow_html=True)
st.markdown("<h6 style='text-align: center; color: black;'>Ask any query..</h6>", unsafe_allow_html=True)
st.markdown("---")



# -------------------- Show Query Result --------------------


def show_query_results(title, query, csv_name):
    st.subheader(title)
    df = conn.query(query, ttl=0)
    if not df.empty:
        st.dataframe(df.style.set_properties(**{'background-color': "#e8fcfe"}), use_container_width=True, hide_index=True)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("Download_Filtered_Queries ↓", data=csv, file_name=csv_name, mime="text/csv")
    else:
        st.warning("No matching records found!")



# -------------------- All Predefined Queries --------------------


queries = {
    "All Female Students": "SELECT * FROM students WHERE gender = 'Female';",
    "All Male Students": "SELECT * FROM students WHERE gender = 'Male';",
    "All Students with gender = Other": "SELECT * FROM students WHERE gender = 'Other';",
    "Age less than 20": "SELECT * FROM students WHERE age <= 20;",
    "Age between 20 - 22": "SELECT * FROM students WHERE age BETWEEN 20 AND 22;",
    "Age between 22 - 25": "SELECT * FROM students WHERE age BETWEEN 22 AND 25;",
    "Students enrolled in 2019": "SELECT student_id, name, email, phone, enrollment_year FROM students WHERE enrollment_year = 2019;",
    "Students enrolled in 2020": "SELECT student_id, name, email, phone, enrollment_year FROM students WHERE enrollment_year = 2020;",
    "Students graduating in 2020": "SELECT student_id, name, email, phone, graduation_year FROM students WHERE graduation_year = 2020;",
    "Students graduating in 2021": "SELECT student_id, name, email, phone, graduation_year FROM students WHERE graduation_year = 2021;",
    "Students graduating in 2022": "SELECT student_id, name, email, phone, graduation_year FROM students WHERE graduation_year = 2022;",
    "Students graduating in 2023": "SELECT student_id, name, email, phone, graduation_year FROM students WHERE graduation_year = 2023;",
    "Students Grouped by City": "SELECT city, COUNT(*) AS count FROM students GROUP BY city;",
    "Pune - Batch-1 Students": "SELECT * FROM students WHERE city = 'Pune' AND course_batch = 'Batch-1';",
    "Pune - Batch-2 Students": "SELECT * FROM students WHERE city = 'Pune' AND course_batch = 'Batch-2';",
    "Tamil Nadu - Batch-1 Students": "SELECT * FROM students WHERE city = 'Tamil Nadu' AND course_batch = 'Batch-1';",
    "Tamil Nadu - Batch-2 Students": "SELECT * FROM students WHERE city = 'Tamil Nadu' AND course_batch = 'Batch-2';",
    "Count Students by City": "SELECT city, COUNT(*) AS total FROM students GROUP BY city;",
    "Students with Project Score > 80": """
        SELECT s.name, p.language, p.latest_project_score 
        FROM programming p 
        JOIN students s ON s.student_id = p.student_id 
        WHERE p.latest_project_score > 80;
    """,
    "Avg Problems Solved by Language": """
        SELECT language, AVG(problems_solved) 
        FROM programming 
        GROUP BY language;
    """,
    "Students with >=2 Certificates": """
        SELECT s.name, p.problems_solved, p.certifications_earned 
        FROM programming p 
        JOIN students s ON s.student_id = p.student_id 
        WHERE p.certifications_earned >= 2;
    """,
    "All 5 Project Completers": "SELECT * FROM programming WHERE mini_projects = 5;",
    "Language Count": "SELECT language, COUNT(*) FROM programming GROUP BY language;",
    "Communication >= 85 & Teamwork >= 85": """
        SELECT s.name, ss.communication, ss.teamwork 
        FROM soft_skills ss 
        JOIN students s ON s.student_id = ss.student_id 
        WHERE ss.communication >= 85 AND ss.teamwork >= 85;
    """,
    "Avg Leadership & Presentation": "SELECT AVG(leadership), AVG(presentation) FROM soft_skills;",
    "Critical Thinking Between 80 to 100": """
        SELECT s.name, ss.critical_thinking 
        FROM soft_skills ss 
        JOIN students s ON s.student_id = ss.student_id 
        WHERE ss.critical_thinking BETWEEN 80 AND 100;
    """,
    "Strong Interpersonal + Communication": "SELECT * FROM soft_skills WHERE interpersonal_skills > 80 AND communication > 80;",
    "Top 5 Leadership Counts": """
        SELECT leadership, COUNT(*) 
        FROM soft_skills 
        GROUP BY leadership 
        ORDER BY COUNT(*) DESC 
        LIMIT 5;
    """,
    "Placement Status Count": "SELECT placement_status, COUNT(*) FROM placements GROUP BY placement_status;",
    "Placed Students & Score": """
        SELECT s.name, p.company_name, p.mock_interview_score 
        FROM placements p 
        JOIN students s ON s.student_id = p.student_id 
        WHERE p.company_name IS NOT NULL;
    """,
    "Mock Score >= 90": "SELECT * FROM placements WHERE mock_interview_score >= 90;",
    "Python + Good Comm + Placed": """
        SELECT s.name, p.language, ss.communication, pl.company_name 
        FROM students s 
        JOIN programming p ON s.student_id = p.student_id 
        JOIN soft_skills ss ON s.student_id = ss.student_id 
        JOIN placements pl ON s.student_id = pl.student_id 
        WHERE p.language = 'Python' AND ss.communication > 75 AND pl.company_name IS NOT NULL;
    """,
    "High Leadership + Certifications": """
        SELECT s.name, ss.leadership, p.certifications_earned 
        FROM students s 
        JOIN soft_skills ss ON s.student_id = ss.student_id 
        JOIN programming p ON s.student_id = p.student_id 
        WHERE ss.leadership >= 90 AND p.certifications_earned >= 2;
    """,
    "Ready Students Graduating 2023": """
        SELECT COUNT(*) 
        FROM students s 
        JOIN placements p ON s.student_id = p.student_id 
        WHERE s.graduation_year = 2023 AND p.placement_status = 'Ready';
    """,
    "Avg Project Score by Batch": """
        SELECT s.course_batch, AVG(p.latest_project_score) 
        FROM students s 
        JOIN programming p ON s.student_id = p.student_id 
        GROUP BY s.course_batch;
    """,
    "Placed Students per City": """
        SELECT s.city, COUNT(*) as total_students 
        FROM students s 
        JOIN placements p ON s.student_id = p.student_id 
        WHERE p.placement_status = 'Placed' 
        GROUP BY s.city;
    """,
    "Avg Mock Score by Company": """
        SELECT company_name, AVG(mock_interview_score) 
        FROM placements 
        WHERE company_name IS NOT NULL 
        GROUP BY company_name;
    """
}


# -------------------- Query Dropdown --------------------


selected_title = st.selectbox("Select a Query to Run", ["-- Select a Query --"] + list(queries.keys()))

if selected_title != "-- Select a Query --" and st.button("Run Query"):
    st.info("Please hold on while we filter your data…")
    query = queries[selected_title]
    show_query_results(title=selected_title, query=query, csv_name="filtered_query_results.csv")
