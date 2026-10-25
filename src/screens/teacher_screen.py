import time
from datetime import datetime
import numpy as np
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

from src.components.footer import footer_dashboard
from src.components.header import header_dashboard
from src.components.subject_card import subject_card
from src.components.dialog_create_subject import create_subject_dialog
from src.components.dialog_share_subject import share_subject_dialog
from src.components.dialog_add_photo import add_photos_dialog
from src.components.dialog_attendance_results import attendance_result_dialog
from src.components.dialog_voice_attendance import voice_attendance_dialog
from src.database.config import supabase
from src.database.db import (
    check_teacher_exists,
    create_teacher,
    teacher_login,
    get_teacher_subjects,
    get_attendance_for_teacher,
)
from src.pipelines.face_pipeline import predict_attendance
from src.ui.base_layout import style_background_dashboard, style_base_layout


def inject_keyboard_shortcuts():
    components.html(
        """
        <script>
        const doc = window.parent.document;
        if (!window._snapclass_shortcuts_attached) {
            window._snapclass_shortcuts_attached = true;
            doc.addEventListener('keydown', function(e) {
                // Cmd + Backspace (or Ctrl + Backspace) -> Go back to Home / Logout
                if ((e.metaKey || e.ctrlKey) && (e.key === 'Backspace' || e.code === 'Backspace')) {
                    const backBtn = doc.querySelector('.st-key-regbackbtn button, .st-key-loginbackbtn button, .st-key-dashbackbtn button');
                    if (backBtn) {
                        e.preventDefault();
                        backBtn.click();
                    }
                }
                // Cmd + Enter (or Ctrl + Enter) -> Register now / Login now
                if ((e.metaKey || e.ctrlKey) && (e.key === 'Enter' || e.code === 'Enter')) {
                    const actionBtn = doc.querySelector('.st-key-regnowbtn button, .st-key-loginnowbtn button');
                    if (actionBtn) {
                        e.preventDefault();
                        actionBtn.click();
                    }
                }
            });
        }
        </script>
        """,
        height=0,
        width=0,
    )


def teacher_screen():
    style_background_dashboard()
    style_base_layout()
    inject_keyboard_shortcuts()

    if "teacher_data" in st.session_state:
        teacher_dashboard()
    elif (
        "teacher_login_type" not in st.session_state
        or st.session_state.teacher_login_type == "login"
    ):
        teacher_screen_login()
    elif st.session_state.teacher_login_type == "register":
        teacher_screen_register()


def login_teacher(username, password):
    if not username or not password:
        return False

    teacher = teacher_login(username, password)
    if teacher:
        st.session_state.user_role = "teacher"
        st.session_state.teacher_data = teacher
        st.session_state.is_logged_in = True
        return True

    return False


def register_teacher(teacher_username, teacher_name, teacher_pass, teacher_pass_confirm):
    teacher_username = (teacher_username or "").strip().lower()
    teacher_name = (teacher_name or "").strip()

    if not teacher_username or not teacher_name or not teacher_pass:
        return False, "All fields are required!"
    if len(teacher_username) < 3:
        return False, "Username must be at least 3 characters long!"
    if check_teacher_exists(teacher_username):
        return False, "Username already taken. Please choose another."
    if teacher_pass != teacher_pass_confirm:
        return False, "Passwords do not match!"

    try:
        created = create_teacher(teacher_username, teacher_pass, teacher_name)
        if created and len(created) > 0:
            st.session_state.teacher_data = created[0]
            st.session_state.is_logged_in = True
            st.session_state.user_role = "teacher"
        return True, "Successfully registered! Logging in..."
    except Exception as e:
        return False, f"Unexpected error during registration: {str(e)}"


def teacher_screen_register():
    # Top Header Row: Logo on left, 'Go back to Home' pink pill on right
    c1, c2 = st.columns([1.3, 1], vertical_alignment="center")
    with c1:
        header_dashboard()
    with c2:
        if st.button("Go back to Home ⌘ + Backspace", key="regbackbtn"):
            st.session_state["login_type"] = None
            st.rerun()

    st.markdown(
        """
        <h2 style='text-align: left; color: #0E1117; font-family: "Climate Crisis", cursive, sans-serif; font-size: 2.15rem; margin-top: 1.8rem; margin-bottom: 1.6rem; letter-spacing: -0.5px;'>
            Register your teacher profile
        </h2>
        """,
        unsafe_allow_html=True,
    )

    teacher_username = st.text_input("Enter username", placeholder="ananyaroy", key="reg_user")
    teacher_name = st.text_input("Enter name", placeholder="Ananya Roy", key="reg_name")
    teacher_pass = st.text_input(
        "Enter password", type="password", placeholder="Enter password", key="reg_pass"
    )
    teacher_pass_confirm = st.text_input(
        "Confirm your password",
        type="password",
        placeholder="Enter password",
        key="reg_pass_confirm",
    )

    st.markdown("<hr/>", unsafe_allow_html=True)

    btnc1, btnc2 = st.columns(2, gap="medium")

    with btnc1:
        if st.button(
            "👤 Register now ⌘ + Enter",
            key="regnowbtn",
            use_container_width=True,
        ):
            success, message = register_teacher(
                teacher_username,
                teacher_name,
                teacher_pass,
                teacher_pass_confirm,
            )
            if success:
                st.success(message)
                time.sleep(1.2)
                st.rerun()
            else:
                st.error(message)

    with btnc2:
        if st.button(
            "👤 Login Instead",
            key="logininsteadbtn",
            use_container_width=True,
        ):
            st.session_state.teacher_login_type = "login"
            st.rerun()

    footer_dashboard()


def teacher_screen_login():
    # Top Header Row: Logo on left, 'Go back to Home' pink pill on right
    c1, c2 = st.columns([1.3, 1], vertical_alignment="center")
    with c1:
        header_dashboard()
    with c2:
        if st.button("Go back to Home ⌘ + Backspace", key="loginbackbtn"):
            st.session_state["login_type"] = None
            st.rerun()

    st.markdown(
        """
        <h2 style='text-align: left; color: #0E1117; font-family: "Climate Crisis", cursive, sans-serif; font-size: 2.15rem; margin-top: 1.8rem; margin-bottom: 1.6rem; letter-spacing: -0.5px;'>
            Login using password
        </h2>
        """,
        unsafe_allow_html=True,
    )

    teacher_username = st.text_input("Enter username", placeholder="ananyaroy", key="login_user")
    teacher_pass = st.text_input(
        "Enter password", type="password", placeholder="Enter password", key="login_pass"
    )

    st.markdown("<hr/>", unsafe_allow_html=True)

    btnc1, btnc2 = st.columns(2, gap="medium")

    with btnc1:
        if st.button(
            "👤 Login now ⌘ + Enter",
            key="loginnowbtn",
            use_container_width=True,
        ):
            if login_teacher(teacher_username, teacher_pass):
                st.toast("Welcome back!", icon="👋")
                time.sleep(1)
                st.rerun()
            else:
                st.error("Invalid username and password combo")

    with btnc2:
        if st.button(
            "👤 Register Instead",
            key="reginsteadbtn",
            use_container_width=True,
        ):
            st.session_state.teacher_login_type = "register"
            st.rerun()

    footer_dashboard()


def teacher_dashboard():
    teacher_data = st.session_state.get("teacher_data", {})
    c1, c2 = st.columns(2, vertical_alignment="center", gap="large")
    with c1:
        header_dashboard()
    with c2:
        st.markdown(
            f"""
            <div style="text-align: right;">
                <h3 style="color: #111827; margin: 0; font-family: 'Outfit', sans-serif;">
                    Welcome, {teacher_data.get('name', 'Professor')} 👋
                </h3>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Logout", key="dashbackbtn"):
            st.session_state["is_logged_in"] = False
            st.session_state.pop("teacher_data", None)
            st.session_state.teacher_login_type = "login"
            st.rerun()

    st.write("")

    if "current_teacher_tab" not in st.session_state:
        st.session_state.current_teacher_tab = "take_attendance"

    tab1, tab2, tab3 = st.columns(3)

    with tab1:
        type1 = "primary" if st.session_state.current_teacher_tab == "take_attendance" else "secondary"
        if st.button("📸 Take Attendance", type=type1, use_container_width=True):
            st.session_state.current_teacher_tab = "take_attendance"
            st.rerun()

    with tab2:
        type2 = "primary" if st.session_state.current_teacher_tab == "manage_subjects" else "secondary"
        if st.button("📚 Manage Subjects", type=type2, use_container_width=True):
            st.session_state.current_teacher_tab = "manage_subjects"
            st.rerun()

    with tab3:
        type3 = "primary" if st.session_state.current_teacher_tab == "attendance_records" else "secondary"
        if st.button("📊 Attendance Records", type=type3, use_container_width=True):
            st.session_state.current_teacher_tab = "attendance_records"
            st.rerun()

    st.markdown("<hr/>", unsafe_allow_html=True)

    if st.session_state.current_teacher_tab == "take_attendance":
        teacher_tab_take_attendance()
    elif st.session_state.current_teacher_tab == "manage_subjects":
        teacher_tab_manage_subjects()
    elif st.session_state.current_teacher_tab == "attendance_records":
        teacher_tab_attendance_records()

    footer_dashboard()


def teacher_tab_take_attendance():
    teacher_id = st.session_state.teacher_data.get("teacher_id")
    st.markdown(
        """
        <h2 style='color: #0E1117; font-family: "Outfit", sans-serif; font-size: 1.8rem; font-weight: 700; margin-bottom: 1rem;'>
            Take AI Attendance
        </h2>
        """,
        unsafe_allow_html=True,
    )

    if "attendance_images" not in st.session_state:
        st.session_state.attendance_images = []

    subjects = get_teacher_subjects(teacher_id)

    if not subjects:
        st.warning("You haven't created any subjects yet! Please create one in 'Manage Subjects' to begin.")
        return

    subject_options = {f"{s['name']} - {s.get('subject_code', '')}": s.get("subject_id") for s in subjects}

    col1, col2 = st.columns([3, 1], vertical_alignment="bottom")

    with col1:
        selected_subject_label = st.selectbox("Select Subject", options=list(subject_options.keys()))

    with col2:
        if st.button("Add Photos", type="primary", use_container_width=True):
            add_photos_dialog()

    selected_subject_id = subject_options[selected_subject_label]

    st.write("")

    if st.session_state.attendance_images:
        st.markdown("### Added Photos")
        gallery_cols = st.columns(4)
        for idx, img in enumerate(st.session_state.attendance_images):
            with gallery_cols[idx % 4]:
                st.image(img, use_container_width=True, caption=f"Photo {idx+1}")

    has_photos = bool(st.session_state.attendance_images)
    c1, c2, c3 = st.columns(3)

    with c1:
        if st.button(
            "Clear all photos",
            use_container_width=True,
            disabled=not has_photos,
        ):
            st.session_state.attendance_images = []
            st.rerun()

    with c2:
        if st.button(
            "Run Face Analysis",
            use_container_width=True,
            type="primary",
            disabled=not has_photos,
        ):
            with st.spinner("Deep scanning classroom photos..."):
                all_detected_ids = {}

                for idx, img in enumerate(st.session_state.attendance_images):
                    img_np = np.array(img.convert("RGB"))
                    detected, _, _ = predict_attendance(img_np)

                    if detected:
                        for sid in detected.keys():
                            student_id = int(sid)
                            all_detected_ids.setdefault(student_id, []).append(f"Photo {idx+1}")

                try:
                    enrolled_res = (
                        supabase.table("subject_students")
                        .select("*, students(*)")
                        .eq("subject_id", selected_subject_id)
                        .execute()
                    )
                    enrolled_students = enrolled_res.data
                except Exception as e:
                    enrolled_students = []

                if not enrolled_students:
                    st.warning("No students enrolled in this course yet.")
                else:
                    results, attendance_to_log = [], []
                    current_timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

                    for node in enrolled_students:
                        student = node.get("students", {})
                        if not student:
                            continue
                        sid = int(student.get("student_id", 0))
                        sources = all_detected_ids.get(sid, [])
                        is_present = len(sources) > 0

                        results.append({
                            "Name": student.get("name", "Student"),
                            "ID": sid,
                            "Source": ", ".join(sources) if is_present else "-",
                            "Status": "✅ Present" if is_present else "❌ Absent",
                        })

                        attendance_to_log.append({
                            "student_id": sid,
                            "subject_id": selected_subject_id,
                            "timestamp": current_timestamp,
                            "is_present": bool(is_present),
                        })

                    attendance_result_dialog(pd.DataFrame(results), attendance_to_log)

    with c3:
        if st.button("Use Voice Attendance", type="secondary", use_container_width=True):
            voice_attendance_dialog(selected_subject_id)


def teacher_tab_manage_subjects():
    teacher_id = st.session_state.teacher_data.get("teacher_id")
    col1, col2 = st.columns([2, 1], vertical_alignment="center")
    with col1:
        st.markdown(
            """
            <h2 style='color: #0E1117; font-family: "Outfit", sans-serif; font-size: 1.8rem; font-weight: 700; margin: 0;'>
                Manage Subjects
            </h2>
            """,
            unsafe_allow_html=True,
        )
    with col2:
        if st.button("+ Create New Subject", type="primary", use_container_width=True):
            create_subject_dialog(teacher_id)

    st.write("")

    # List all subjects
    subjects = get_teacher_subjects(teacher_id)
    if subjects:
        for sub in subjects:
            stats = [
                ("👥", "Students", sub.get("total_students", 0)),
                ("🗓️", "Classes", sub.get("total_classes", 0)),
            ]

            def share_btn(sub_name=sub["name"], sub_code=sub.get("subject_code", "")):
                if st.button(
                    f"Share Code: {sub_name}",
                    key=f"share_{sub_code}_{sub.get('subject_id', 0)}",
                ):
                    share_subject_dialog(sub_name, sub_code)

            subject_card(
                name=sub["name"],
                code=sub.get("subject_code", "N/A"),
                section=sub.get("section", "A"),
                stats=stats,
                footer_callback=share_btn,
            )
    else:
        st.info("No subjects found yet. Click '+ Create New Subject' above to add your first course!")


def teacher_tab_attendance_records():
    st.markdown(
        """
        <h2 style='color: #0E1117; font-family: "Outfit", sans-serif; font-size: 1.8rem; font-weight: 700; margin-bottom: 1rem;'>
            Attendance Records
        </h2>
        """,
        unsafe_allow_html=True,
    )

    teacher_id = st.session_state.teacher_data.get("teacher_id")
    records = get_attendance_for_teacher(teacher_id)

    if not records:
        st.info("No attendance sessions recorded yet. Run a session in 'Take Attendance' to see records here.")
        return

    data = []
    for r in records:
        ts = r.get("timestamp")
        sub_info = r.get("subjects") or {}

        data.append({
            "ts_group": ts.split(".")[0] if ts else None,
            "Time": datetime.fromisoformat(ts).strftime("%Y-%m-%d %I:%M %p") if ts else "N/A",
            "Subject": sub_info.get("name", "Unknown Subject"),
            "Subject Code": sub_info.get("subject_code", "N/A"),
            "is_present": bool(r.get("is_present", False)),
        })

    df = pd.DataFrame(data)

    if df.empty or "ts_group" not in df.columns:
        st.info("No formatted attendance data found.")
        return

    summary = (
        df.groupby(["ts_group", "Time", "Subject", "Subject Code"])
        .agg(
            Present_Count=("is_present", "sum"),
            Total_Count=("is_present", "count"),
        )
        .reset_index()
    )

    summary["Attendance Stats"] = (
        "✅ "
        + summary["Present_Count"].astype(str)
        + " / "
        + summary["Total_Count"].astype(str)
        + " Students"
    )

    display_df = summary.sort_values(by="ts_group", ascending=False)[
        ["Time", "Subject", "Subject Code", "Attendance Stats"]
    ]

    st.dataframe(display_df, use_container_width=True, hide_index=True)