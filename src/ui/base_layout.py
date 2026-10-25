import streamlit as st


def style_background_home():
    st.markdown(
        """
        <style>
            /* Overall page background */
            .stApp {
                background: #5865F2 !important;
            }

            /* Student & Teacher Column Cards on Home Page */
            .stApp div[data-testid="stColumn"] {
                background-color: #E0E3FF !important;
                border-radius: 2.5rem !important;
                padding: 2.5rem 1.8rem 2rem 1.8rem !important;
                display: flex !important;
                flex-direction: column !important;
                align-items: center !important;
                justify-content: space-between !important;
                text-align: center !important;
                min-height: 420px !important;
                box-shadow: 0 12px 32px rgba(0, 0, 0, 0.12) !important;
                transition: transform 0.25s ease, box-shadow 0.25s ease !important;
            }

            .stApp div[data-testid="stColumn"]:hover {
                transform: translateY(-4px) !important;
                box-shadow: 0 18px 40px rgba(0, 0, 0, 0.18) !important;
            }

            /* Portal card content wrapper */
            .home-portal-card {
                width: 100% !important;
                display: flex !important;
                flex-direction: column !important;
                align-items: center !important;
                justify-content: flex-start !important;
                flex-grow: 1 !important;
            }

            /* Clean readable card titles */
            .portal-card-title {
                font-family: 'Outfit', sans-serif !important;
                font-weight: 800 !important;
                font-size: 2.1rem !important;
                color: #1A1C24 !important;
                margin: 0 0 1rem 0 !important;
                text-align: center !important;
                letter-spacing: -0.5px !important;
                line-height: 1.2 !important;
            }

            /* Standardized mascot container for equal vertical height */
            .portal-mascot-box {
                height: 160px !important;
                display: flex !important;
                align-items: center !important;
                justify-content: center !important;
                margin-bottom: 1.5rem !important;
            }

            .portal-mascot-box img {
                max-height: 140px !important;
                max-width: 150px !important;
                width: auto !important;
                height: auto !important;
                object-fit: contain !important;
            }

            /* Home Portal Pill Buttons */
            div[data-testid="stColumn"] button {
                background-color: #5865F2 !important;
                color: #FFFFFF !important;
                border-radius: 9999px !important;
                padding: 0.75rem 1.8rem !important;
                border: none !important;
                font-family: 'Outfit', sans-serif !important;
                font-size: 1.05rem !important;
                font-weight: 700 !important;
                width: 100% !important;
                min-height: 48px !important;
                box-shadow: 0 4px 14px rgba(88, 101, 242, 0.35) !important;
                transition: transform 0.2s ease, background-color 0.2s ease, box-shadow 0.2s ease !important;
                cursor: pointer !important;
            }

            div[data-testid="stColumn"] button:hover {
                transform: translateY(-2px) scale(1.02) !important;
                background-color: #4351d8 !important;
                box-shadow: 0 6px 20px rgba(88, 101, 242, 0.45) !important;
            }

            /* Isolate dialogs and modals from home column styling */
            div[data-testid="stModal"] div[data-testid="stColumn"],
            div[role="dialog"] div[data-testid="stColumn"],
            .stDialog div[data-testid="stColumn"] {
                background-color: transparent !important;
                border-radius: 0 !important;
                padding: 0 0.5rem !important;
                min-height: auto !important;
                box-shadow: none !important;
                display: block !important;
                transform: none !important;
            }
        </style>  
        """,
        unsafe_allow_html=True,
    )


def style_background_dashboard():
    st.markdown(
        """
        <style>
            /* Dashboard background */
            .stApp {
                background: #E0E3FF !important;
            }

            /* Reset column card styling on dashboard */
            .stApp div[data-testid="stColumn"] {
                background-color: transparent !important;
                border-radius: 0 !important;
                padding: 0 !important;
                box-shadow: none !important;
                display: block !important;
                min-height: auto !important;
                transform: none !important;
            }

            /* Input labels */
            div[data-testid="stTextInput"] label, 
            div[data-testid="stTextInput"] [data-testid="stWidgetLabel"] p {
                color: #1A1C24 !important;
                font-family: 'Outfit', sans-serif !important;
                font-size: 0.95rem !important;
                font-weight: 600 !important;
                margin-bottom: 0.35rem !important;
            }

            /* Input container - single unified box with no inner nesting */
            div[data-testid="stTextInputRootElement"],
            div[data-testid="stTextInput"] div[data-baseweb="base-input"] {
                border: none !important;
                background: transparent !important;
                box-shadow: none !important;
                padding: 0 !important;
            }

            /* The single crisp input box */
            div[data-testid="stTextInput"] div[data-baseweb="input"] {
                background-color: #F7F8FC !important;
                background: #F7F8FC !important;
                border: 1.5px solid rgba(195, 208, 240, 0.8) !important;
                border-radius: 8px !important;
                min-height: 48px !important;
                padding: 0 4px 0 14px !important;
                display: flex !important;
                align-items: center !important;
                box-shadow: none !important;
                transition: border-color 0.18s ease, background-color 0.18s ease, box-shadow 0.18s ease !important;
            }

            /* Focused input: Pink outline matching user screenshot */
            div[data-testid="stTextInput"] div[data-baseweb="input"]:focus-within {
                border: 1.5px solid #EE4989 !important;
                background-color: #FFFFFF !important;
                background: #FFFFFF !important;
                box-shadow: 0 0 0 1px #EE4989 !important;
            }

            div[data-testid="stTextInput"] input {
                background-color: transparent !important;
                background: transparent !important;
                color: #1A1C24 !important;
                font-family: 'Outfit', sans-serif !important;
                font-size: 1.05rem !important;
                font-weight: 500 !important;
                border: none !important;
                outline: none !important;
                box-shadow: none !important;
                padding: 0 !important;
            }

            div[data-testid="stTextInput"] input::placeholder {
                color: #8F97AB !important;
                opacity: 1 !important;
                font-family: 'Outfit', sans-serif !important;
            }

            /* Password toggle eye pill button */
            div[data-testid="stTextInput"] button[aria-label*="password"],
            div[data-testid="stTextInput"] button[data-testid*="PasswordToggle"],
            div[data-testid="stTextInput"] button[aria-label="Show password"],
            div[data-testid="stTextInput"] button[aria-label="Hide password"] {
                background-color: #5865F2 !important;
                color: #FFFFFF !important;
                border-radius: 9999px !important;
                height: 32px !important;
                min-width: 52px !important;
                border: none !important;
                display: flex !important;
                align-items: center !important;
                justify-content: center !important;
                box-shadow: 0 2px 8px rgba(88, 101, 242, 0.3) !important;
                cursor: pointer !important;
                margin-right: 4px !important;
                transition: background-color 0.2s ease, transform 0.15s ease !important;
            }

            div[data-testid="stTextInput"] button[aria-label*="password"]:hover,
            div[data-testid="stTextInput"] button[data-testid*="PasswordToggle"]:hover {
                background-color: #4351d8 !important;
                transform: scale(1.04) !important;
            }

            div[data-testid="stTextInput"] button[aria-label*="password"] svg,
            div[data-testid="stTextInput"] button[data-testid*="PasswordToggle"] svg {
                fill: #FFFFFF !important;
                stroke: #FFFFFF !important;
                color: #FFFFFF !important;
            }

            /* Climate Crisis Display Titles */
            .climate-title,
            h2.climate-title {
                font-family: 'Climate Crisis', cursive, sans-serif !important;
                font-size: 2.3rem !important;
                line-height: 1.15 !important;
                text-align: center !important;
                color: #1E1E24 !important;
                margin-top: 1.5rem !important;
                margin-bottom: 2rem !important;
            }

            /* Top right Go back to Home / Logout button */
            .st-key-loginbackbtn button,
            .st-key-student_logout_btn button,
            .st-key-teacher_logout_btn button {
                background-color: #EE4989 !important;
                color: #FFFFFF !important;
                border-radius: 9999px !important;
                border: none !important;
                font-family: 'Outfit', sans-serif !important;
                font-size: 0.95rem !important;
                font-weight: 600 !important;
                padding: 0.6rem 1.6rem !important;
                float: right !important;
                box-shadow: 0 4px 12px rgba(238, 73, 137, 0.28) !important;
                transition: transform 0.2s ease, background-color 0.2s ease !important;
            }

            .st-key-loginbackbtn button:hover,
            .st-key-student_logout_btn button:hover,
            .st-key-teacher_logout_btn button:hover {
                background-color: #d63375 !important;
                transform: scale(1.03) !important;
                color: #FFFFFF !important;
            }

            /* Divider */
            hr {
                border: none !important;
                border-top: 1.5px solid rgba(180, 190, 225, 0.6) !important;
                margin: 1.75rem 0 1.5rem 0 !important;
            }
        </style>  
        """,
        unsafe_allow_html=True,
    )


def style_base_layout():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Climate+Crisis:YEAR@1979&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&display=swap');

            /* Hide default Streamlit top bar, header, and footer */
            #MainMenu, footer, header {
                visibility: hidden;
            }
                
            .block-container {
                padding-top: 1.5rem !important;
                padding-bottom: 2rem !important;
                max-width: 860px !important;
            }

            /* Main Header Title */
            h1 {
                font-family: 'Climate Crisis', cursive, sans-serif !important;
                font-size: 3.8rem !important;
                line-height: 1.0 !important;
                margin-bottom: 1.5rem !important;
                text-align: center !important;
                color: #FFFFFF !important;
                letter-spacing: 1px !important;
            }

            h2, h3, h4, p, label {
                font-family: 'Outfit', sans-serif !important;    
            }

            /* Standardized Button Styling */
            button {
                border-radius: 9999px !important;
                background-color: #5865F2 !important;
                color: white !important;
                padding: 10px 22px !important;
                border: none !important;
                font-family: 'Outfit', sans-serif !important;
                font-weight: 600 !important;
                transition: transform 0.2s ease-in-out, background-color 0.2s ease !important;
            }

            button[kind="secondary"] {
                border-radius: 9999px !important;
                background-color: #EB459E !important;
                color: white !important;
                padding: 10px 22px !important;
                border: none !important;
                font-family: 'Outfit', sans-serif !important;
                font-weight: 600 !important;
            }

            button[kind="tertiary"] {
                border-radius: 9999px !important;
                background-color: #1e1e1e !important;
                color: white !important;
                padding: 10px 22px !important;
                border: none !important;
                font-family: 'Outfit', sans-serif !important;
                font-weight: 600 !important;
            }

            button:hover {
                transform: scale(1.03) !important;
            }

            /* Modal and Dialog Window Balance and Orientation */
            div[data-testid="stModal"],
            div[role="dialog"] {
                border-radius: 24px !important;
                background-color: #FFFFFF !important;
                border: 1px solid rgba(210, 220, 245, 0.9) !important;
                box-shadow: 0 25px 60px rgba(0, 0, 0, 0.25) !important;
            }

            div[data-testid="stModal"] > div {
                border-radius: 24px !important;
                padding: 1.25rem 1.5rem 1.75rem 1.5rem !important;
            }

            div[data-testid="stModal"] h2,
            div[data-testid="stModal"] h3,
            div[role="dialog"] h2,
            div[role="dialog"] h3 {
                font-family: 'Outfit', sans-serif !important;
                font-weight: 700 !important;
                color: #1A1C24 !important;
                margin-top: 0 !important;
                margin-bottom: 0.75rem !important;
            }

            div[data-testid="stModal"] div[data-testid="stHorizontalBlock"] {
                gap: 1rem !important;
                align-items: center !important;
            }

            div[data-testid="stModal"] div[data-testid="stColumn"] {
                background: transparent !important;
                padding: 0 !important;
                box-shadow: none !important;
                border-radius: 0 !important;
                min-height: auto !important;
            }

            div[data-testid="stModal"] button {
                width: 100% !important;
                min-height: 44px !important;
            }

            /* Full Coverage Camera Viewfinder */
            div[data-testid="stCameraInput"] {
                width: 100% !important;
                margin-top: 0.5rem !important;
            }

            div[data-testid="stCameraInput"] [data-testid="stCameraInputWebcamStyledBox"],
            div[data-testid="stCameraInput"] [data-testid="stCameraInputWebcamComponent"],
            div[data-testid="stCameraInput"] [data-testid="stCameraInputWebcamStyledBox"] > div,
            div[data-testid="stCameraInput"] div[data-testid*="Webcam"] {
                width: 100% !important;
                max-width: 100% !important;
                border-radius: 16px 16px 0 0 !important;
                overflow: hidden !important;
                background-color: #0F1117 !important;
            }

            /* Make camera video cover the entire frame edge-to-edge without pillarbox sidebars */
            div[data-testid="stCameraInput"] video {
                width: 100% !important;
                min-width: 100% !important;
                height: 480px !important;
                max-height: 520px !important;
                object-fit: cover !important;
                display: block !important;
                border-radius: 16px 16px 0 0 !important;
            }

            /* When captured photo is displayed */
            div[data-testid="stCameraInput"] img {
                width: 100% !important;
                min-width: 100% !important;
                height: 480px !important;
                max-height: 520px !important;
                object-fit: cover !important;
                display: block !important;
                border-radius: 16px 16px 0 0 !important;
            }

            /* Take Photo Button attached flush below the camera */
            div[data-testid="stCameraInput"] button,
            div[data-testid="stCameraInput"] [data-testid="stCameraInputButton"] {
                border-radius: 0 0 16px 16px !important;
                min-height: 50px !important;
                background-color: #5865F2 !important;
                color: #FFFFFF !important;
                font-family: 'Outfit', sans-serif !important;
                font-size: 1.05rem !important;
                font-weight: 700 !important;
                box-shadow: 0 4px 14px rgba(88, 101, 242, 0.3) !important;
                width: 100% !important;
                margin-top: 0 !important;
            }

            div[data-testid="stCameraInput"] button:hover,
            div[data-testid="stCameraInput"] [data-testid="stCameraInputButton"]:hover {
                background-color: #4351d8 !important;
                transform: none !important;
            }

            /* Inside modal dialogs: slightly more compact height */
            div[data-testid="stModal"] div[data-testid="stCameraInput"] video,
            div[data-testid="stModal"] div[data-testid="stCameraInput"] img {
                height: 380px !important;
                max-height: 420px !important;
                object-fit: cover !important;
            }
        </style>  
        """,
        unsafe_allow_html=True,
    )