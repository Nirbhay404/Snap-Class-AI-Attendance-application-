import time
import streamlit as st
from src.database.db import create_subject


@st.dialog("Create New Subject")
def create_subject_dialog(teacher_id: int):
    st.write("Enter the details of the new subject:")
    sub_id = st.text_input("Subject Code", placeholder="CS101")
    sub_name = st.text_input("Subject Name", placeholder="Introduction to Computer Science")
    sub_section = st.text_input("Section", placeholder="A")

    if st.button("Create Subject Now", type="primary", use_container_width=True):
        if sub_id and sub_name and sub_section:
            try:
                create_subject(
                    sub_id.strip().upper(),
                    sub_name.strip(),
                    sub_section.strip(),
                    teacher_id,
                )
                st.toast("Subject Created Successfully!", icon="🎉")
                time.sleep(0.6)
                st.rerun()
            except Exception as e:
                st.error(f"Error creating subject: {e}")
        else:
            st.warning("Please fill all details before submitting.")
