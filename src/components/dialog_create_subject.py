import streamlit as st
from src.database.config import supabase


@st.dialog("Create New Subject")
def create_subject_dialog(teacher_id):
    st.write("Enter details for the new subject you want to manage.")

    name = st.text_input("Subject Name", placeholder="e.g. Data Structures & Algorithms")
    code = st.text_input("Subject Code", placeholder="e.g. CS201")
    section = st.text_input("Section", placeholder="e.g. Section A")

    if st.button("Create Subject", type="primary", use_container_width=True):
        if not name or not code:
            st.error("Subject Name and Code are required!")
            return

        try:
            res = (
                supabase.table("subjects")
                .insert({
                    "teacher_id": teacher_id,
                    "name": name.strip(),
                    "subject_code": code.strip().upper(),
                    "section": (section or "A").strip(),
                })
                .execute()
            )
            st.success("Subject created successfully!")
            st.rerun()
        except Exception as e:
            st.error(f"Error creating subject: {str(e)}")
