import streamlit as st


def subject_card(name, code, section, stats, footer_callback=None):
    st.markdown(
        f"""
        <div style="background-color: #FFFFFF; border-radius: 1.25rem; padding: 1.5rem; margin-bottom: 1.25rem; box-shadow: 0 2px 12px rgba(0,0,0,0.04); border: 1px solid rgba(220, 226, 245, 0.6);">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.8rem;">
                <div>
                    <h3 style="color: #111827; font-family: 'Outfit', sans-serif; font-size: 1.35rem; font-weight: 700; margin: 0 0 0.25rem 0;">
                        {name}
                    </h3>
                    <div style="display: flex; gap: 8px; align-items: center;">
                        <span style="background: #E0E3FF; color: #5865F2; padding: 0.2rem 0.65rem; border-radius: 9999px; font-weight: 600; font-size: 0.8rem;">
                            Code: {code}
                        </span>
                        <span style="background: #F3F4F6; color: #4B5563; padding: 0.2rem 0.65rem; border-radius: 9999px; font-weight: 500; font-size: 0.8rem;">
                            Section: {section}
                        </span>
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    stat_cols = st.columns(len(stats) if stats else 1)
    if stats:
        for idx, (icon, label, val) in enumerate(stats):
            with stat_cols[idx]:
                st.markdown(
                    f"""
                    <div style="background: #F8F9FE; border-radius: 0.85rem; padding: 0.6rem 0.8rem; text-align: center; margin-bottom: 0.8rem;">
                        <span style="font-size: 1.1rem;">{icon}</span>
                        <p style="color: #6B7280; font-size: 0.75rem; margin: 0.1rem 0;">{label}</p>
                        <b style="color: #111827; font-size: 1rem;">{val}</b>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    if footer_callback:
        footer_callback()
