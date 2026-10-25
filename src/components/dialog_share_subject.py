import io
import segno
import streamlit as st


@st.dialog("Share Class Link")
def share_subject_dialog(subject_name, subject_code):
    app_domain = "snapclass-main.streamlit.app"
    join_url = f"https://{app_domain}/?join-code={subject_code}"

    st.markdown(
        f"""
        <div style="margin-bottom: 0.75rem;">
            <span style="background: #E0E3FF; color: #5865F2; padding: 0.25rem 0.75rem; border-radius: 9999px; font-weight: 600; font-size: 0.85rem;">
                Course: {subject_name}
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    qr = segno.make(join_url)
    out = io.BytesIO()
    qr.save(out, kind="png", scale=10, border=1)

    col1, col2 = st.columns(2, gap="medium")

    with col1:
        st.markdown("#### Copy Link & Code")
        st.caption("Direct Join Link:")
        st.code(join_url, language="text")
        st.caption("Class Code:")
        st.code(subject_code, language="text")
        st.info("Share this link or QR code with students via WhatsApp or Email.")

    with col2:
        st.markdown("#### Scan to Join")
        st.image(out.getvalue(), caption=f"QR Code for {subject_name}", use_container_width=True)
