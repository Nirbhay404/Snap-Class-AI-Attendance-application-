from html import escape

import streamlit as st


def subject_card(name, code, section, stats=None, footer_callback=None):
    # Subject details are typed by teachers and shown to students, so escape before injecting as HTML.
    name, code, section = escape(str(name)), escape(str(code)), escape(str(section))
    stats_pills = ""
    if stats:
        pills = []
        for icon, label, value in stats:
            pills.append(
                f'<span style="background: rgba(235, 69, 158, 0.12); color: #1e293b; padding: 6px 14px; border-radius: 12px; font-size: 0.88rem; font-weight: 600; display: inline-flex; align-items: center; gap: 6px;">'
                f'{icon} <b>{escape(str(value))}</b> {escape(str(label))}'
                f'</span>'
            )
        stats_pills = f'<div style="margin-top: 14px; margin-bottom: 16px; display: flex; flex-wrap: wrap; gap: 8px;">{"".join(pills)}</div>'

    card_html = (
        f'<div style="background: #FFFFFF; border-left: 8px solid #EB459E; padding: 22px 24px 20px 24px; border-radius: 18px; border: 1px solid rgba(210, 220, 245, 0.85); box-shadow: 0 4px 16px rgba(0,0,0,0.04); margin-bottom: 12px; font-family: \'Outfit\', sans-serif;">'
        f'<h3 style="margin: 0; color: #1e293b; font-size: 1.45rem; font-weight: 700; line-height: 1.25;">{name}</h3>'
        f'<p style="color: #64748b; margin: 8px 0 0 0; font-size: 0.95rem;">'
        f'Code: <span style="background: #E0E3FF; color: #5865F2; padding: 3px 10px; border-radius: 6px; font-weight: 600;">{code}</span>'
        f'&nbsp;&nbsp;|&nbsp;&nbsp;Section: <b style="color: #1e293b;">{section}</b>'
        f'</p>'
        f'{stats_pills}'
        f'</div>'
    )

    st.markdown(card_html, unsafe_allow_html=True)

    if footer_callback:
        footer_callback()
