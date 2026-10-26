import io
import segno
import streamlit as st


def get_app_base_url() -> str:
    """Dynamically determine the current running base URL (local dev or Streamlit Cloud deployment)."""
    # 1. Custom configured base URL or domain in secrets.toml (if provided)
    try:
        if "APP_URL" in st.secrets:
            return st.secrets["APP_URL"].rstrip("/")
        if "APP_DOMAIN" in st.secrets:
            domain = st.secrets["APP_DOMAIN"].strip("/")
            proto = "http" if "localhost" in domain or "127.0.0.1" in domain else "https"
            return f"{proto}://{domain}"
    except Exception:
        pass

    # 2. Extract host from active browser request headers
    try:
        if hasattr(st, "context") and hasattr(st.context, "headers"):
            headers = st.context.headers
            host = headers.get("host") or headers.get("Host")
            if host:
                proto = headers.get("x-forwarded-proto") or ("https" if "streamlit.app" in host else "http")
                return f"{proto}://{host}".rstrip("/")
    except Exception:
        pass

    # 3. Fallback to user's real Streamlit Cloud deployment URL
    return "https://nirbhay404-snap-class-ai-attendance-application--app-lpyli0.streamlit.app"


@st.dialog("Share Class Link")
def share_subject_dialog(subject_name: str, subject_code: str):
    base_url = get_app_base_url()
    join_url = f"{base_url}/?join-code={subject_code}"

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
