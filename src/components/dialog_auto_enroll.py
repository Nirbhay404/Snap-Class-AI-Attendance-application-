import streamlit as st
import time
from src.database.db import enroll_student_to_subject
from src.database.config import supabase


@st.dialog("Quick Enrollment")
def auto_enroll_dialog(subject_code: str):
    student_data = st.session_state.get("student_data")
    if not student_data:
        st.error("Student session not found. Please log in first.")
        if st.button("Close"):
            st.query_params.clear()
            st.rerun()
        return

    student_id = student_data["student_id"]

    try:
        res = (
            supabase.table("subjects")
            .select("subject_id, name")
            .eq("subject_code", subject_code)
            .execute()
        )
    except Exception as e:
        st.error(f"Error checking subject: {e}")
        if st.button("Close"):
            st.query_params.clear()
            st.rerun()
        return

    if not res.data:
        st.error("Subject code not found!")
        if st.button("Close"):
            st.query_params.clear()
            st.rerun()
        return

    subject = res.data[0]

    try:
        check = (
            supabase.table("subject_students")
            .select("*")
            .eq("subject_id", subject["subject_id"])
            .eq("student_id", student_id)
            .execute()
        )
    except Exception as e:
        st.error(f"Database query error: {e}")
        if st.button("Close"):
            st.query_params.clear()
            st.rerun()
        return

    if check.data:
        st.info("You're already enrolled in this subject!")
        if st.button("Got it!"):
            st.query_params.clear()
            st.rerun()
        return

    st.markdown(f"Would you like to enroll in **{subject['name']}**?")

    col1, col2 = st.columns(2, gap="medium", vertical_alignment="center")

    with col1:
        if st.button("✕ No thanks", type="tertiary", use_container_width=True):
            st.query_params.clear()
            st.rerun()
    with col2:
        if st.button("✓ Yes, enroll now!", type="primary", use_container_width=True):
            try:
                enroll_student_to_subject(student_id, subject["subject_id"])
                st.success("Joined successfully!")
                st.query_params.clear()
                time.sleep(1.2)
                st.rerun()
            except Exception as e:
                st.error(f"Enrollment error: {e}")
