import streamlit as st
from src.database.config import supabase


@st.dialog("Attendance Results")
def attendance_result_dialog(results_df, attendance_to_log):
    st.write("Scan complete. Review student attendance before saving.")

    st.dataframe(results_df, use_container_width=True, hide_index=True)

    if st.button("Save Attendance Records", type="primary", use_container_width=True):
        try:
            if attendance_to_log:
                supabase.table("attendance").insert(attendance_to_log).execute()
            st.success("Attendance successfully saved to database!")
            st.session_state.attendance_images = []
            st.rerun()
        except Exception as e:
            st.error(f"Error saving attendance: {str(e)}")
