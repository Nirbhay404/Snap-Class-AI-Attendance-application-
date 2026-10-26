import time
import numpy as np
from PIL import Image
import streamlit as st

from src.ui.base_layout import style_background_dashboard, style_base_layout
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from src.components.dialog_enroll import enroll_dialog
from src.components.subject_card import subject_card
from src.database.db import (
    get_all_students,
    create_student,
    get_student_subjects,
    get_student_attendance,
    unenroll_student_to_subject,
)
from src.pipelines.face_pipeline import (
    predict_attendance,
    get_face_embeddings,
    train_classifier,
)
from src.pipelines.voice_pipeline import get_voice_embedding


def student_dashboard():
    student_data = st.session_state.student_data
    student_id = student_data["student_id"]

    c1, c2 = st.columns(2, vertical_alignment="center", gap="large")
    with c1:
        header_dashboard()
    with c2:
        st.subheader(f"Welcome, {student_data.get('name', 'Student')} 👋")
        if st.button("Logout", type="secondary", key="student_logout_btn", use_container_width=True):
            st.session_state["is_logged_in"] = False
            st.session_state.pop("student_data", None)
            st.session_state["login_type"] = None
            st.rerun()

    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

    c1, c2 = st.columns(2, vertical_alignment="center")
    with c1:
        st.header("Your Enrolled Subjects")
    with c2:
        if st.button("➕ Enroll in Subject", type="primary", use_container_width=True):
            enroll_dialog()

    st.divider()

    with st.spinner("Loading your enrolled subjects..."):
        subjects = get_student_subjects(student_id)
        logs = get_student_attendance(student_id)

    stats_map = {}
    for log in logs:
        sid = log.get("subject_id")
        if sid:
            if sid not in stats_map:
                stats_map[sid] = {"total": 0, "attended": 0}
            stats_map[sid]["total"] += 1
            if log.get("is_present"):
                stats_map[sid]["attended"] += 1

    if not subjects:
        st.info("You are not enrolled in any subjects yet. Click 'Enroll in Subject' above to join a class!")
    else:
        cols = st.columns(2)
        for i, sub_node in enumerate(subjects):
            sub = sub_node.get("subjects") or {}
            sid = sub.get("subject_id")
            if not sid:
                continue

            stats = stats_map.get(sid, {"total": 0, "attended": 0})
            sub_name = sub.get("name", "Course")

            def make_unenroll_callback(curr_sid=sid, curr_name=sub_name):
                def unenroll_button():
                    if st.button(
                        f"🗑️ Unenroll from {curr_name}",
                        type="tertiary",
                        key=f"unenroll_{curr_sid}",
                        use_container_width=True,
                    ):
                        try:
                            unenroll_student_to_subject(student_id, curr_sid)
                            st.toast(f"Unenrolled from {curr_name} successfully!", icon="👋")
                            time.sleep(0.8)
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error unenrolling: {e}")

                return unenroll_button

            with cols[i % 2]:
                subject_card(
                    name=sub.get("name", "Unknown Subject"),
                    code=sub.get("subject_code", "N/A"),
                    section=sub.get("section", "A"),
                    stats=[
                        ("📅", "Total", stats["total"]),
                        ("✅", "Attended", stats["attended"]),
                    ],
                    footer_callback=make_unenroll_callback(sid, sub_name),
                )

    footer_dashboard()


def student_screen():
    style_background_dashboard()
    style_base_layout()

    if "student_data" in st.session_state:
        student_dashboard()
        return

    c1, c2 = st.columns(2, vertical_alignment="center", gap="large")
    with c1:
        header_dashboard()
    with c2:
        if st.button("Go back to Home ⌘ + Backspace", type="secondary", key="loginbackbtn", use_container_width=True):
            st.session_state["login_type"] = None
            st.rerun()

    st.markdown(
        "<h2 class='climate-title'>Login using FaceID</h2>",
        unsafe_allow_html=True,
    )

    join_code = st.query_params.get("join-code") or st.query_params.get("join_code")
    if join_code:
        st.info(f"🔗 Joining Class **{join_code.strip().upper()}** — Please verify your face or register below to complete your enrollment.")

    show_registration = False
    photo_source = st.camera_input("Position your face in the center")

    if photo_source:
        img = np.array(Image.open(photo_source).convert("RGB"))

        with st.spinner("AI is scanning..."):
            detected, all_ids, num_faces = predict_attendance(img)

            if num_faces == 0:
                st.warning("Face not found! Please adjust lighting and face the camera directly.")
            elif num_faces > 1:
                st.warning("Multiple faces found. Please make sure only one face is visible.")
            else:
                if detected:
                    student_id = list(detected.keys())[0]
                    all_students = get_all_students()
                    student = next(
                        (s for s in all_students if s.get("student_id") == student_id),
                        None,
                    )

                    if student:
                        st.session_state.is_logged_in = True
                        st.session_state.user_role = "student"
                        st.session_state.student_data = student
                        st.toast(f"Welcome back, {student.get('name', 'Student')}! 👋")
                        time.sleep(1)
                        st.rerun()
                else:
                    st.info("Face not recognized! You might be a new student. Register below.")
                    show_registration = True

    if show_registration and photo_source:
        st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
        with st.container(border=True):
            st.header("Register New Student Profile")
            new_name = st.text_input("Enter your name", placeholder="E.g. Hamza Rizvi")

            st.subheader("Optional: Voice Enrollment")
            st.caption("Enroll your voice for audio verification attendance.")

            audio_data = None
            try:
                audio_data = st.audio_input(
                    "Record a short phrase (e.g. 'I am present, my name is Hamza')"
                )
            except Exception:
                pass

            if st.button("Create Account", type="primary", use_container_width=True):
                if new_name and new_name.strip():
                    with st.spinner("Creating profile..."):
                        img = np.array(Image.open(photo_source).convert("RGB"))
                        encodings = get_face_embeddings(img)
                        if encodings:
                            face_emb = encodings[0].tolist()

                            voice_emb = None
                            if audio_data:
                                try:
                                    voice_emb = get_voice_embedding(audio_data.read())
                                except Exception as e:
                                    st.warning(f"Voice embedding skipped: {e}")

                            response_data = create_student(
                                new_name.strip(),
                                face_embedding=face_emb,
                                voice_embedding=voice_emb,
                            )

                            if response_data:
                                train_classifier()
                                st.session_state.is_logged_in = True
                                st.session_state.user_role = "student"
                                st.session_state.student_data = response_data[0]
                                st.toast(f"Profile created! Hi, {new_name}! 👋")
                                time.sleep(1)
                                st.rerun()
                            else:
                                st.error("Failed to save student profile to database.")
                        else:
                            st.error(
                                "Could not capture facial features for registration. Please retake the photo."
                            )
                else:
                    st.warning("Please enter your name!")

    footer_dashboard()