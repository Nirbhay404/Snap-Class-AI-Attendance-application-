import time
import streamlit as st
from src.database.db import enroll_student_to_subject
from src.database.config import supabase


@st.dialog("Enroll in Subject")
def enroll_dialog():
    st.write("Enter the subject code provided by your teacher to enroll:")
    join_code = st.text_input("Subject Code", placeholder="e.g. CS101")

    if st.button("Enroll Now", type="primary", use_container_width=True):
        code = (join_code or "").strip().upper()
        if not code:
            st.warning("Please enter a subject code.")
            return

        student_data = st.session_state.get("student_data")
        if not student_data:
            st.error("Student session not found. Please log in first.")
            return

        student_id = student_data["student_id"]

        try:
            res = (
                supabase.table("subjects")
                .select("subject_id, name, subject_code")
                .eq("subject_code", code)
                .execute()
            )
            if not res.data:
                st.error(f"Subject with code '{code}' not found.")
                return

            subject = res.data[0]
            check = (
                supabase.table("subject_students")
                .select("*")
                .eq("subject_id", subject["subject_id"])
                .eq("student_id", student_id)
                .execute()
            )

            if check.data:
                st.warning(f"You are already enrolled in {subject.get('name', code)}.")
            else:
                enroll_student_to_subject(student_id, subject["subject_id"])
                st.success(f"Successfully enrolled in {subject.get('name', code)}!")
                time.sleep(1)
                st.rerun()
        except Exception as e:
            st.error(f"Enrollment error: {e}")
