import streamlit as st
from src.database.db import enroll_student_in_subject


@st.dialog("Enroll in Subject")
def enroll_dialog():
    st.write("Enter the Subject Code provided by your teacher to enroll:")

    subject_code = st.text_input("Subject Code", placeholder="e.g. CS201")

    if st.button("Enroll Now", type="primary", use_container_width=True):
        if not subject_code:
            st.error("Please enter a subject code.")
            return

        student = st.session_state.get("student_data")
        if not student:
            st.error("Student session not found. Please log in again.")
            return

        student_id = student["student_id"]
        success, message = enroll_student_in_subject(student_id, subject_code)
        if success:
            st.success(message)
            st.rerun()
        else:
            st.error(message)
