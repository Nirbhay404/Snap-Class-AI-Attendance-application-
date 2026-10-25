import streamlit as st
from src.components.header import header_home
from src.components.footer import footer_home
from src.ui.base_layout import style_base_layout, style_background_home


def home_screen():
    header_home()
    style_background_home()
    style_base_layout()

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown(
            """
            <div class="home-portal-card">
                <h2 class="portal-card-title">I'm Student</h2>
                <div class="portal-mascot-box">
                    <img src="https://i.ibb.co/844D9Lrt/mascot-student.png" alt="Student Mascot" />
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Student Portal  ↗", type="primary", key="btn_student_portal", use_container_width=True):
            st.session_state["login_type"] = "student"
            st.rerun()

    with col2:
        st.markdown(
            """
            <div class="home-portal-card">
                <h2 class="portal-card-title">I'm Teacher</h2>
                <div class="portal-mascot-box">
                    <img src="https://i.ibb.co/CsmQQV6X/mascot-prof.png" alt="Teacher Mascot" />
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Teacher Portal  ↗", type="primary", key="btn_teacher_portal", use_container_width=True):
            st.session_state["login_type"] = "teacher"
            st.rerun()

    footer_home()