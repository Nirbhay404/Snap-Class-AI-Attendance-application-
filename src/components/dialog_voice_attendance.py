from datetime import datetime
import pandas as pd
import streamlit as st
from src.database.config import supabase
from src.pipelines.voice_pipeline import process_bulk_audio


@st.dialog("Voice Attendance")
def voice_attendance_dialog(selected_subject_id):
    st.write(
        "Upload or record classroom audio to automatically recognize enrolled students by voice."
    )

    try:
        enrolled_res = (
            supabase.table("subject_students")
            .select("*, students(*)")
            .eq("subject_id", selected_subject_id)
            .execute()
        )
        enrolled_students = [
            node["students"] for node in (enrolled_res.data or []) if node.get("students")
        ]
    except Exception as e:
        enrolled_students = []

    candidates_dict = {
        s["student_id"]: s.get("voice_embedding")
        for s in enrolled_students
        if s.get("voice_embedding")
    }

    if not candidates_dict:
        st.warning(
            "None of the students enrolled in this course have registered voice profiles yet."
        )

    audio_file = st.file_uploader(
        "Upload classroom audio recording",
        type=["wav", "mp3", "m4a", "ogg"],
        key="voice_att_audio_upload",
    )

    if audio_file and st.button(
        "Analyze Voice Attendance",
        type="primary",
        use_container_width=True,
    ):
        with st.spinner("Scanning audio stream for enrolled student voices..."):
            audio_bytes = audio_file.read()
            detected_voices = process_bulk_audio(audio_bytes, candidates_dict)

            results = []
            attendance_to_log = []
            current_timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

            for s in enrolled_students:
                sid = s["student_id"]
                score = detected_voices.get(sid)
                is_present = score is not None

                results.append({
                    "Name": s.get("name", "Student"),
                    "ID": sid,
                    "Voice Match Score": f"{score:.2f}" if is_present else "-",
                    "Status": "✅ Present" if is_present else "❌ Absent",
                })
                attendance_to_log.append({
                    "student_id": sid,
                    "subject_id": selected_subject_id,
                    "timestamp": current_timestamp,
                    "is_present": bool(is_present),
                })

            st.dataframe(pd.DataFrame(results), use_container_width=True, hide_index=True)

            if st.button("Save Voice Attendance", type="primary", use_container_width=True):
                try:
                    if attendance_to_log:
                        supabase.table("attendance").insert(attendance_to_log).execute()
                    st.success("Voice attendance successfully recorded!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error saving attendance: {e}")
