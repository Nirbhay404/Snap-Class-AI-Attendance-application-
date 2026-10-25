import io
import segno
import streamlit as st


@st.dialog("Share Class Link")
def share_subject_dialog(subject_name: str, subject_code: str):
    app_domain = "snapclass-main.streamlit.app"
    join_url = f"https://{app_domain}/?join-code={subject_code}"

    badge_html = (
        f'<div style="margin-bottom: 1rem;">'
        f'<span style="background: #E0E3FF; color: #5865F2; padding: 4px 12px; border-radius: 9999px; font-weight: 600; font-size: 0.9rem;">'
        f'Course: {subject_name}'
        f'</span>'
        f'</div>'
    )
    st.markdown(badge_html, unsafe_allow_html=True)

    qr = segno.make(join_url)
    out = io.BytesIO()
    qr.save(out, kind="png", scale=10, border=1)

    col1, col2 = st.columns(2, gap="large", vertical_alignment="center")

    with col1:
        st.markdown("#### Copy Link & Code")
        st.caption("Direct Join Link:")
        st.code(join_url, language="text")
        st.caption("Class Code:")
        st.code(subject_code, language="text")
        st.info("Copy this link or code to share with students via WhatsApp or Email.")

    with col2:
        st.markdown("#### Scan to Join")
        st.image(out.getvalue(), caption=f"QR Code for {subject_name}", use_container_width=True)
