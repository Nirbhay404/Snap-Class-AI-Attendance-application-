from datetime import datetime
import pandas as pd
import streamlit as st
from src.components.dialog_attendance_results import show_attendance_result
from src.database.config import supabase
from src.pipelines.voice_pipeline import process_bulk_audio


@st.dialog("Voice Attendance")
def voice_attendance_dialog(selected_subject_id):
    st.write(
        "Record audio of students saying 'I am present'. The AI will recognize enrolled students by voice."
    )

    audio_data = st.audio_input("Record classroom audio")

    if st.button("Analyze Audio", type="primary", use_container_width=True):
        if not audio_data:
            st.warning("Please record classroom audio first.")
            return

        with st.spinner("Processing audio data..."):
            try:
                enrolled_res = (
                    supabase.table("subject_students")
                    .select("*, students(*)")
                    .eq("subject_id", selected_subject_id)
                    .execute()
                )
                enrolled_students = [
                    node for node in (enrolled_res.data or []) if node.get("students")
                ]
            except Exception as e:
                st.error(f"Error fetching enrolled students: {e}")
                return

            if not enrolled_students:
                st.warning("No students enrolled in this course.")
                return

            candidates_dict = {
                node["students"]["student_id"]: node["students"].get("voice_embedding")
                for node in enrolled_students
                if node.get("students") and node["students"].get("voice_embedding")
            }

            if not candidates_dict:
                st.error("No enrolled students have voice profiles registered yet.")
                return

            audio_bytes = audio_data.read()
            detected_scores = process_bulk_audio(audio_bytes, candidates_dict)

            results = []
            attendance_to_log = []
            current_timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

            for node in enrolled_students:
                student = node["students"]
                sid = student["student_id"]
                score = detected_scores.get(sid, 0.0)
                is_present = bool(score > 0)

                results.append({
                    "Name": student.get("name", "Unknown"),
                    "ID": sid,
                    "Match Score": f"{score:.2f}" if is_present else "-",
                    "Status": "✅ Present" if is_present else "❌ Absent",
                })

                attendance_to_log.append({
                    "student_id": sid,
                    "subject_id": selected_subject_id,
                    "timestamp": current_timestamp,
                    "is_present": bool(is_present),
                })

            st.session_state.voice_attendance_results = (pd.DataFrame(results), attendance_to_log)

    if st.session_state.get("voice_attendance_results"):
        st.divider()
        df_results, logs = st.session_state.voice_attendance_results
        show_attendance_result(df_results, logs)
