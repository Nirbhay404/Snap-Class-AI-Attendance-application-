import streamlit as st


def style_background_home():
    st.markdown(
        """
        <style>
            /* Overall page background */
            .stApp {
                background: #5865F2 !important;
            }

            /* Student & Teacher Column Cards */
            div[data-testid="stColumn"] {
                background-color: #E0E3FF !important;
                border-radius: 3rem !important;
                padding: 2.5rem 1.5rem !important;
                display: flex !important;
                flex-direction: column !important;
                align-items: center !important;
                justify-content: center !important;
                text-align: center !important;
            }

            /* Headers inside column cards ("I'm Student" / "I'm Teacher") */
            div[data-testid="stColumn"] h2, 
            div[data-testid="stColumn"] [data-testid="stHeader"] {
                color: #1E1E1E !important;
                font-family: 'Climate Crisis', cursive, sans-serif !important;
                font-size: 2.2rem !important;
                line-height: 1.1 !important;
                margin-bottom: 0.5rem !important;
            }

            /* Image centering within column cards */
            div[data-testid="stColumn"] img {
                margin: 1rem auto !important;
                display: block !important;
            }

            /* Purple Pill Buttons */
            div[data-testid="stColumn"] button {
                background-color: #5865F2 !important;
                color: #FFFFFF !important;
                border-radius: 2rem !important;
                padding: 0.6rem 1.8rem !important;
                border: none !important;
                font-family: 'Outfit', sans-serif !important;
                font-size: 1rem !important;
                font-weight: 600 !important;
                box-shadow: none !important;
                transition: transform 0.2s ease-in-out, background-color 0.2s ease-in-out !important;
            }

            div[data-testid="stColumn"] button:hover {
                transform: scale(1.05) !important;
                background-color: #4752C4 !important;
                color: #FFFFFF !important;
            }

            div[data-testid="stColumn"] button:active,
            div[data-testid="stColumn"] button:focus {
                background-color: #5865F2 !important;
                color: #FFFFFF !important;
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

            /* Reset column card styling on dashboard so columns don't inherit home cards */
            .stApp div[data-testid="stColumn"] {
                background-color: transparent !important;
                border-radius: 0 !important;
                padding: 0 !important;
                box-shadow: none !important;
                display: block !important;
            }

            /* Input labels */
            div[data-testid="stTextInput"] label, 
            div[data-testid="stTextInput"] [data-testid="stWidgetLabel"] p {
                color: #1A1C24 !important;
                font-family: 'Outfit', sans-serif !important;
                font-size: 0.95rem !important;
                font-weight: 500 !important;
                margin-bottom: 0.35rem !important;
            }

            /* Input container - light rounded white/periwinkle background */
            div[data-testid="stTextInputRootElement"],
            div[data-testid="stTextInput"] div[data-baseweb="input"],
            div[data-testid="stTextInput"] div[data-baseweb="base-input"] {
                background-color: #F1F3FA !important;
                background: #F1F3FA !important;
                border: 1px solid rgba(215, 222, 245, 0.7) !important;
                border-radius: 12px !important;
                min-height: 48px !important;
                padding: 0 6px 0 14px !important;
                display: flex !important;
                align-items: center !important;
                box-shadow: none !important;
                transition: border-color 0.2s ease, background-color 0.2s ease !important;
            }

            /* Every wrapper and the input element inside the text input area:
               MUST be light/white background and dark text, NEVER black */
            div[data-testid="stTextInput"] input,
            div[data-testid="stTextInputRootElement"] input,
            div[data-testid="stTextInput"] div[data-baseweb="input"] > div,
            div[data-testid="stTextInput"] div[data-baseweb="base-input"] > div,
            div[data-testid="stTextInputRootElement"] > div {
                background-color: #F1F3FA !important;
                background: #F1F3FA !important;
                color: #1A1C24 !important;
                font-family: 'Outfit', sans-serif !important;
                font-size: 1rem !important;
                border: none !important;
                box-shadow: none !important;
            }

            /* Focus state */
            div[data-testid="stTextInputRootElement"]:focus-within,
            div[data-testid="stTextInput"]:focus-within div[data-baseweb="input"],
            div[data-testid="stTextInput"]:focus-within div[data-baseweb="base-input"],
            div[data-testid="stTextInput"]:focus-within input {
                border-color: #5865F2 !important;
                background-color: #FFFFFF !important;
                background: #FFFFFF !important;
                box-shadow: none !important;
            }

            div[data-testid="stTextInputRootElement"]:focus-within {
                box-shadow: 0 0 0 2px rgba(88, 101, 242, 0.15) !important;
            }

            /* Placeholder styling */
            div[data-testid="stTextInput"] input::placeholder {
                color: #9BA2B5 !important;
                opacity: 1 !important;
                font-family: 'Outfit', sans-serif !important;
            }

            /* Blue pill eye button inside password inputs */
            div[data-testid="stTextInputRootElement"] button,
            div[data-testid="stTextInput"] button,
            button[aria-label="Show password"],
            button[aria-label="Hide password"],
            button[data-testid="stTextInputPasswordToggle"] {
                background-color: #5865F2 !important;
                background: #5865F2 !important;
                color: #FFFFFF !important;
                border-radius: 9999px !important;
                height: 32px !important;
                min-width: 48px !important;
                margin-right: 4px !important;
                border: none !important;
                display: flex !important;
                align-items: center !important;
                justify-content: center !important;
                box-shadow: 0 2px 6px rgba(88, 101, 242, 0.3) !important;
                transition: background-color 0.2s ease, transform 0.15s ease !important;
                cursor: pointer !important;
            }

            div[data-testid="stTextInputRootElement"] button:hover,
            div[data-testid="stTextInput"] button:hover,
            button[aria-label="Show password"]:hover,
            button[aria-label="Hide password"]:hover {
                background-color: #4752C4 !important;
                background: #4752C4 !important;
                transform: scale(1.04) !important;
            }

            div[data-testid="stTextInputRootElement"] button svg,
            div[data-testid="stTextInput"] button svg {
                fill: #FFFFFF !important;
                stroke: #FFFFFF !important;
                color: #FFFFFF !important;
                width: 18px !important;
                height: 18px !important;
            }

            /* Top right 'Go back to Home' pink pill button */
            .st-key-regbackbtn button,
            .st-key-loginbackbtn button,
            .st-key-dashbackbtn button {
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

            .st-key-regbackbtn button:hover,
            .st-key-loginbackbtn button:hover,
            .st-key-dashbackbtn button:hover {
                background-color: #d63375 !important;
                transform: scale(1.03) !important;
                color: #FFFFFF !important;
            }

            .st-key-regbackbtn button p,
            .st-key-loginbackbtn button p,
            .st-key-dashbackbtn button p,
            .st-key-regbackbtn button span,
            .st-key-loginbackbtn button span,
            .st-key-dashbackbtn button span {
                color: #FFFFFF !important;
                font-family: 'Outfit', sans-serif !important;
                font-weight: 600 !important;
            }

            /* Bottom Pink Button (Register now / Login now) */
            .st-key-regnowbtn button,
            .st-key-loginnowbtn button {
                background-color: #EE4989 !important;
                color: #FFFFFF !important;
                border-radius: 9999px !important;
                border: none !important;
                font-family: 'Outfit', sans-serif !important;
                font-size: 1.05rem !important;
                font-weight: 600 !important;
                height: 50px !important;
                width: 100% !important;
                display: flex !important;
                align-items: center !important;
                justify-content: center !important;
                gap: 8px !important;
                box-shadow: 0 4px 14px rgba(238, 73, 137, 0.3) !important;
                transition: transform 0.2s ease, background-color 0.2s ease !important;
            }

            .st-key-regnowbtn button:hover,
            .st-key-loginnowbtn button:hover {
                background-color: #d63375 !important;
                transform: scale(1.02) !important;
                color: #FFFFFF !important;
            }

            .st-key-regnowbtn button p,
            .st-key-loginnowbtn button p,
            .st-key-regnowbtn button span,
            .st-key-loginnowbtn button span {
                color: #FFFFFF !important;
                font-family: 'Outfit', sans-serif !important;
                font-weight: 600 !important;
            }

            /* Bottom Blue Button (Login Instead / Register Instead) */
            .st-key-logininsteadbtn button,
            .st-key-reginsteadbtn button {
                background-color: #5865F2 !important;
                color: #FFFFFF !important;
                border-radius: 9999px !important;
                border: none !important;
                font-family: 'Outfit', sans-serif !important;
                font-size: 1.05rem !important;
                font-weight: 600 !important;
                height: 50px !important;
                width: 100% !important;
                display: flex !important;
                align-items: center !important;
                justify-content: center !important;
                gap: 8px !important;
                box-shadow: 0 4px 14px rgba(88, 101, 242, 0.3) !important;
                transition: transform 0.2s ease, background-color 0.2s ease !important;
            }

            .st-key-logininsteadbtn button:hover,
            .st-key-reginsteadbtn button:hover {
                background-color: #4752C4 !important;
                transform: scale(1.02) !important;
                color: #FFFFFF !important;
            }

            .st-key-logininsteadbtn button p,
            .st-key-reginsteadbtn button p,
            .st-key-logininsteadbtn button span,
            .st-key-reginsteadbtn button span {
                color: #FFFFFF !important;
                font-family: 'Outfit', sans-serif !important;
                font-weight: 600 !important;
            }

            /* Divider */
            hr {
                border: none !important;
                border-top: 1.5px solid rgba(180, 190, 225, 0.6) !important;
                margin: 2rem 0 1.5rem 0 !important;
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
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@100..900&display=swap');

            /* Hide default Streamlit top bar, header, and footer */
            #MainMenu, footer, header {
                visibility: hidden;
            }
                
            .block-container {
                padding-top: 1.5rem !important;
                padding-bottom: 2rem !important;
                max-width: 820px !important;
            }

            /* Main Header Title */
            h1 {
                font-family: 'Climate Crisis', cursive, sans-serif !important;
                font-size: 3.8rem !important;
                line-height: 1.0 !important;
                margin-bottom: 2rem !important;
                text-align: center !important;
                color: #FFFFFF !important;
            }

            h2 {
                font-family: 'Climate Crisis', cursive, sans-serif !important;
            }
                
            h3, h4, p, span {
                font-family: 'Outfit', sans-serif !important;    
            }
        </style>  
        """,
        unsafe_allow_html=True,
    )