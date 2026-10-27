from datetime import datetime
import time
import numpy as np
import pandas as pd
import streamlit as st

from src.ui.base_layout import style_background_dashboard, style_base_layout
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from src.components.subject_card import subject_card
from src.components.dialog_create_subject import create_subject_dialog
from src.components.dialog_share_subject import share_subject_dialog
from src.components.dialog_add_photo import add_photos_dialog
from src.components.dialog_voice_attendance import voice_attendance_dialog
from src.components.dialog_attendance_results import attendance_result_dialog
from src.database.config import supabase
from src.database.db import (
    check_teacher_exists,
    create_teacher,
    teacher_login,
    get_teacher_subjects,
    get_attendance_for_teacher,
)
from src.pipelines.face_pipeline import predict_attendance


def teacher_screen():
    style_background_dashboard()
    style_base_layout()

    if "teacher_data" in st.session_state:
        teacher_dashboard()
    elif st.session_state.get("teacher_login_type") == "register":
        teacher_screen_register()
    else:
        teacher_screen_login()


def login_teacher(username, password):
    if not username or not password:
        return False

    teacher = teacher_login(username.strip(), password)
    if teacher:
        st.session_state.user_role = "teacher"
        st.session_state.teacher_data = teacher
        st.session_state.is_logged_in = True
        return True
    return False


def register_teacher(teacher_username, teacher_name, teacher_pass, teacher_pass_confirm):
    username = (teacher_username or "").strip()
    name = (teacher_name or "").strip()

    if not username or not name or not teacher_pass:
        return False, "All fields are required!"
    if len(username) < 3:
        return False, "Username must be at least 3 characters long."
    if len(teacher_pass) < 6:
        return False, "Password must be at least 6 characters long."
    if check_teacher_exists(username):
        return False, f"Username '{username}' is already taken."
    if teacher_pass != teacher_pass_confirm:
        return False, "Passwords do not match."

    try:
        create_teacher(username, teacher_pass, name)
        return True, "Successfully registered! Please log in."
    except Exception as e:
        return False, f"Error creating teacher account: {e}"


def teacher_screen_login():
    c1, c2 = st.columns(2, vertical_alignment="center", gap="large")
    with c1:
        header_dashboard()
    with c2:
        if st.button("Go back to Home ⌘ + Backspace", type="secondary", key="loginbackbtn", use_container_width=True):
            st.session_state["login_type"] = None
            st.rerun()

    st.markdown(
        "<h2 class='climate-title'>Login using password</h2>",
        unsafe_allow_html=True,
    )

    teacher_username = st.text_input("Enter username", placeholder="e.g. ananyaroy")
    teacher_pass = st.text_input("Enter password", type="password", placeholder="Enter your password")

    st.divider()

    btnc1, btnc2 = st.columns(2)
    with btnc1:
        if st.button("🔑 Login  ⌘ + Enter", type="secondary", use_container_width=True):
            if login_teacher(teacher_username, teacher_pass):
                st.toast("Welcome back!", icon="👋")
                time.sleep(0.8)
                st.rerun()
            else:
                st.error("Invalid username or password.")

    with btnc2:
        if st.button("👤 Register Instead", type="primary", use_container_width=True):
            st.session_state.teacher_login_type = "register"
            st.rerun()

    footer_dashboard()


def teacher_screen_register():
    c1, c2 = st.columns(2, vertical_alignment="center", gap="large")
    with c1:
        header_dashboard()
    with c2:
        if st.button("Go back to Home ⌘ + Backspace", type="secondary", key="regbackbtn", use_container_width=True):
            st.session_state["login_type"] = None
            st.rerun()

    st.markdown(
        "<h2 class='climate-title'>Register your teacher profile</h2>",
        unsafe_allow_html=True,
    )

    teacher_username = st.text_input("Enter username", placeholder="e.g. ananyaroy")
    teacher_name = st.text_input("Enter full name", placeholder="e.g. Ananya Roy")
    teacher_pass = st.text_input("Enter password", type="password", placeholder="Choose a password")
    teacher_pass_confirm = st.text_input("Confirm password", type="password", placeholder="Re-enter your password")

    st.divider()

    btnc1, btnc2 = st.columns(2)
    with btnc1:
        if st.button("📝 Register now  ⌘ + Enter", type="secondary", use_container_width=True):
            success, message = register_teacher(teacher_username, teacher_name, teacher_pass, teacher_pass_confirm)
            if success:
                st.success(message)
                time.sleep(1.5)
                st.session_state.teacher_login_type = "login"
                st.rerun()
            else:
                st.error(message)

    with btnc2:
        if st.button("🔑 Login Instead", type="primary", use_container_width=True):
            st.session_state.teacher_login_type = "login"
            st.rerun()

    footer_dashboard()


def teacher_dashboard():
    teacher_data = st.session_state.teacher_data
    c1, c2 = st.columns(2, vertical_alignment="center", gap="large")
    with c1:
        header_dashboard()
    with c2:
        st.subheader(f"Welcome, {teacher_data.get('name', 'Teacher')} 👋")
        if st.button("Logout", type="secondary", key="teacher_logout_btn", use_container_width=True):
            st.session_state["is_logged_in"] = False
            st.session_state.pop("teacher_data", None)
            st.session_state["login_type"] = None
            st.rerun()

    st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)

    if "current_teacher_tab" not in st.session_state:
        st.session_state.current_teacher_tab = "take_attendance"

    tab1, tab2, tab3 = st.columns(3)

    with tab1:
        type1 = "primary" if st.session_state.current_teacher_tab == "take_attendance" else "tertiary"
        if st.button("📸 Take Attendance", type=type1, use_container_width=True):
            st.session_state.current_teacher_tab = "take_attendance"
            st.rerun()

    with tab2:
        type2 = "primary" if st.session_state.current_teacher_tab == "manage_subjects" else "tertiary"
        if st.button("📚 Manage Subjects", type=type2, use_container_width=True):
            st.session_state.current_teacher_tab = "manage_subjects"
            st.rerun()

    with tab3:
        type3 = "primary" if st.session_state.current_teacher_tab == "attendance_records" else "tertiary"
        if st.button("📊 Attendance Records", type=type3, use_container_width=True):
            st.session_state.current_teacher_tab = "attendance_records"
            st.rerun()

    st.divider()

    if st.session_state.current_teacher_tab == "take_attendance":
        teacher_tab_take_attendance()
    elif st.session_state.current_teacher_tab == "manage_subjects":
        teacher_tab_manage_subjects()
    elif st.session_state.current_teacher_tab == "attendance_records":
        teacher_tab_attendance_records()

    footer_dashboard()


def teacher_tab_take_attendance():
    teacher_id = st.session_state.teacher_data["teacher_id"]
    st.header("Take AI Attendance")

    if "attendance_images" not in st.session_state:
        st.session_state.attendance_images = []

    subjects = get_teacher_subjects(teacher_id)
    if not subjects:
        st.warning("You haven't created any subjects yet! Please go to 'Manage Subjects' to create one.")
        return

    subject_options = {f"{s['name']} - {s.get('subject_code', 'N/A')}": s["subject_id"] for s in subjects}

    col1, col2 = st.columns([3, 1], vertical_alignment="bottom")
    with col1:
        selected_subject_label = st.selectbox("Select Subject", options=list(subject_options.keys()))
    with col2:
        if st.button("➕ Add Photos", type="primary", use_container_width=True):
            add_photos_dialog()

    selected_subject_id = subject_options[selected_subject_label]

    st.divider()

    if st.session_state.attendance_images:
        st.header("Added Photos")
        gallery_cols = st.columns(4)
        for idx, img in enumerate(st.session_state.attendance_images):
            with gallery_cols[idx % 4]:
                st.image(img, use_container_width=True, caption=f"Photo {idx + 1}")

    has_photos = bool(st.session_state.attendance_images)
    c1, c2, c3 = st.columns(3)

    with c1:
        if st.button(
            "🗑️ Clear all photos",
            use_container_width=True,
            type="tertiary",
            disabled=not has_photos,
        ):
            st.session_state.attendance_images = []
            st.rerun()

    with c2:
        if st.button(
            "⚡ Run Face Analysis",
            use_container_width=True,
            type="secondary",
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
                            all_detected_ids.setdefault(student_id, []).append(f"Photo {idx + 1}")

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
                    enrolled_students = []

                if not enrolled_students:
                    st.warning("No students are enrolled in this subject yet.")
                else:
                    results = []
                    attendance_to_log = []
                    current_timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

                    for node in enrolled_students:
                        student = node["students"]
                        sid = int(student["student_id"])
                        sources = all_detected_ids.get(sid, [])
                        is_present = len(sources) > 0

                        results.append({
                            "Name": student.get("name", "Unknown"),
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
        if st.button("🎙️ Use Voice Attendance", type="primary", use_container_width=True):
            voice_attendance_dialog(selected_subject_id)


def teacher_tab_manage_subjects():
    teacher_id = st.session_state.teacher_data["teacher_id"]
    col1, col2 = st.columns(2, vertical_alignment="center")
    with col1:
        st.header("Manage Subjects")
    with col2:
        if st.button("➕ Create New Subject", type="primary", use_container_width=True):
            create_subject_dialog(teacher_id)

    subjects = get_teacher_subjects(teacher_id)
    if subjects:
        cols = st.columns(2)
        for i, sub in enumerate(subjects):
            stats = [
                ("🫂", "Students", sub.get("total_students", 0)),
                ("🕰️", "Classes", sub.get("total_classes", 0)),
            ]
            sub_name = sub.get("name", "Subject")
            sub_code = sub.get("subject_code", "N/A")

            def make_share_callback(curr_name=sub_name, curr_code=sub_code, idx=i):
                def share_btn():
                    if st.button(
                        f"🔗 Share Code ({curr_code})",
                        key=f"share_{curr_code}_{idx}",
                        type="secondary",
                        use_container_width=True,
                    ):
                        share_subject_dialog(curr_name, curr_code)

                return share_btn

            with cols[i % 2]:
                subject_card(
                    name=sub_name,
                    code=sub_code,
                    section=sub.get("section", "A"),
                    stats=stats,
                    footer_callback=make_share_callback(sub_name, sub_code),
                )
    else:
        st.info("No subjects found yet. Click 'Create New Subject' above to create your first class!")


def teacher_tab_attendance_records():
    st.header("Attendance Records")

    teacher_id = st.session_state.teacher_data["teacher_id"]
    records = get_attendance_for_teacher(teacher_id)

    if not records:
        st.info("No attendance records found yet. Take attendance to see records here.")
        return

    data = []
    for r in records:
        ts = r.get("timestamp")
        sub_info = r.get("subjects") or {}
        time_str = "N/A"
        if ts:
            try:
                time_str = datetime.fromisoformat(ts).strftime("%Y-%m-%d %I:%M %p")
            except Exception:
                time_str = str(ts)

        data.append({
            "ts_group": ts.split(".")[0] if ts else None,
            "Time": time_str,
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