import time
import numpy as np
import streamlit as st
import streamlit.components.v1 as components
from PIL import Image

from src.components.dialog_enroll import enroll_dialog
from src.components.footer import footer_dashboard
from src.components.header import header_dashboard
from src.components.subject_card import subject_card
from src.database.db import (
    create_student,
    get_all_students,
    get_student_attendance,
    get_student_subjects,
    unenroll_student_to_subject,
)
from src.pipelines.face_pipeline import (
    get_face_embeddings,
    predict_attendance,
    train_classifier,
)
from src.pipelines.voice_pipeline import get_voice_embedding
from src.ui.base_layout import style_background_dashboard, style_base_layout


def inject_keyboard_shortcuts():
    components.html(
        """
        <script>
        const doc = window.parent.document;
        if (!window._snapclass_shortcuts_attached) {
            window._snapclass_shortcuts_attached = true;
            doc.addEventListener('keydown', function(e) {
                if ((e.metaKey || e.ctrlKey) && (e.key === 'Backspace' || e.code === 'Backspace')) {
                    const backBtn = doc.querySelector('.st-key-loginbackbtn button, .st-key-dashbackbtn button');
                    if (backBtn) {
                        e.preventDefault();
                        backBtn.click();
                    }
                }
            });
        }
        </script>
        """,
        height=0,
        width=0,
    )


def student_dashboard():
    student_data = st.session_state.student_data
    student_id = student_data["student_id"]

    c1, c2 = st.columns([1.3, 1], vertical_alignment="center")
    with c1:
        header_dashboard()
    with c2:
        st.markdown(
            f"""
            <div style="text-align: right;">
                <h3 style="color: #111827; margin: 0; font-family: 'Outfit', sans-serif;">
                    Welcome, {student_data.get('name', 'Student')} 🎓
                </h3>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Logout", key="dashbackbtn"):
            st.session_state["is_logged_in"] = False
            st.session_state.pop("student_data", None)
            st.rerun()

    st.write("")

    col1, col2 = st.columns([2, 1], vertical_alignment="center")
    with col1:
        st.markdown(
            """
            <h2 style='color: #0E1117; font-family: "Outfit", sans-serif; font-size: 1.8rem; font-weight: 700; margin: 0;'>
                Your Enrolled Subjects
            </h2>
            """,
            unsafe_allow_html=True,
        )
    with col2:
        if st.button("Enroll in Subject", type="primary", use_container_width=True):
            enroll_dialog()

    st.markdown("<hr/>", unsafe_allow_html=True)

    with st.spinner("Loading your enrolled subjects..."):
        subjects = get_student_subjects(student_id)
        logs = get_student_attendance(student_id)

    stats_map = {}
    for log in logs:
        sid = log.get("subject_id")
        if sid not in stats_map:
            stats_map[sid] = {"total": 0, "attended": 0}
        stats_map[sid]["total"] += 1
        if log.get("is_present"):
            stats_map[sid]["attended"] += 1

    if not subjects:
        st.info("You haven't enrolled in any subjects yet! Click 'Enroll in Subject' above.")
    else:
        cols = st.columns(2)
        for i, sub_node in enumerate(subjects):
            sub = sub_node.get("subjects") or {}
            sid = sub.get("subject_id")
            stats = stats_map.get(sid, {"total": 0, "attended": 0})

            def make_unenroll(cur_sub_name=sub.get("name", "Subject"), cur_sid=sid):
                def unenroll_button():
                    if st.button(
                        f"Unenroll from {cur_sub_name}",
                        key=f"unenroll_{cur_sid}",
                        use_container_width=True,
                    ):
                        unenroll_student_to_subject(student_id, cur_sid)
                        st.toast(f"Unenrolled from {cur_sub_name} successfully!")
                        st.rerun()
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
                    footer_callback=make_unenroll(sub.get("name", "Subject"), sid),
                )

    footer_dashboard()


def student_screen():
    style_background_dashboard()
    style_base_layout()
    inject_keyboard_shortcuts()

    if "student_data" in st.session_state:
        student_dashboard()
        return

    c1, c2 = st.columns([1.3, 1], vertical_alignment="center")
    with c1:
        header_dashboard()
    with c2:
        if st.button("Go back to Home ⌘ + Backspace", key="loginbackbtn"):
            st.session_state["login_type"] = None
            st.rerun()

    st.markdown(
        """
        <h2 style='text-align: center; color: #0E1117; font-family: "Climate Crisis", cursive, sans-serif; font-size: 2.15rem; margin-top: 1.5rem; margin-bottom: 1.5rem;'>
            Login using FaceID
        </h2>
        """,
        unsafe_allow_html=True,
    )

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
        st.write("")
        with st.container(border=True):
            st.markdown("### Register New Student Profile")
            new_name = st.text_input("Enter your name", placeholder="E.g. Hamza Rizvi")

            st.markdown("#### Optional: Voice Enrollment")
            st.caption("Enroll your voice for audio verification attendance.")

            audio_data = None
            try:
                audio_data = st.audio_input(
                    "Record a short phrase (e.g. 'I am present, my name is Hamza')"
                )
            except Exception:
                pass

            if st.button("Create Account", type="primary", use_container_width=True):
                if new_name:
                    with st.spinner("Creating profile..."):
                        img = np.array(Image.open(photo_source).convert("RGB"))
                        encodings = get_face_embeddings(img)
                        if encodings:
                            face_emb = encodings[0].tolist()

                            voice_emb = None
                            if audio_data:
                                voice_emb = get_voice_embedding(audio_data.read())

                            response_data = create_student(
                                new_name,
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
                            st.error("Couldn't capture your facial features for registration. Please try taking another photo.")
                else:
                    st.warning("Please enter your name!")

    footer_dashboard()