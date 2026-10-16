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
            .stApp {
                background: #E0E3FF !important;
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
                padding-top: 2rem !important;
                max-width: 850px !important;
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