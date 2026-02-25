# style.py
# Injects global CSS and defines layout helpers for ClarityPredictV2.

import streamlit as st

def inject_global_styles():
    # Import branding inside the function to avoid NameError
    from app.layout import branding

    css = f"""
    <style>

    /* Remove Streamlit top padding */
    .block-container {{
        padding-top: 0 !important;
    }}

    /* Global content width */
    .cp-container {{
        max-width: 900px;
        margin: 0 auto;
    }}

    /* Global font and background */
    html, body {{
        font-family: {branding.FONT_FAMILY};
        background-color: {branding.BACKGROUND_COLOR};
        color: {branding.TEXT_COLOR};
    }}

    /* Headings */
    h1 {{
        font-size: {branding.FONT_SIZE_TITLE};
        font-weight: 600;
        color: {branding.PRIMARY_COLOR};
        margin-top: 10px;
    }}

    h2 {{
        font-size: {branding.FONT_SIZE_SUBTITLE};
        font-weight: 500;
        color: {branding.TEXT_COLOR};
    }}

    /* Card container */
    .cp-card {{
        background-color: white;
        padding: 20px;
        border-radius: {branding.CARD_RADIUS};
        box-shadow: {branding.CARD_SHADOW};
        margin-bottom: 20px;
    }}

    /* Section spacing */
    .cp-section {{
        margin-top: {branding.SECTION_SPACING};
        margin-bottom: {branding.SECTION_SPACING};
    }}

    /* Footer */
    .cp-footer {{
        text-align: center;
        font-size: 14px;
        color: {branding.SUBTEXT_COLOR};
        margin-top: 40px;
        padding: 20px 0;
    }}

    /* Header */
    .cp-header {{
        display: flex;
        justify-content: flex-start;
        margin: 0;
        padding: 0;
    }}

    .cp-header-left {{
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        margin: 0;
        padding: 0;
    }}

    .cp-header-logo {{
        width: 240px;
        margin-bottom: -5px;
    }}

    .cp-header-tagline {{
        font-size: 16px;
        color: {branding.SUBTEXT_COLOR};
        margin-top: 5px;
    }}

    /* Metric card */
    .cp-metric-card {{
        text-align: center;
        border-top: 4px solid {branding.PRIMARY_COLOR};
        padding: 20px;
        border-radius: {branding.CARD_RADIUS};
        box-shadow: {branding.CARD_SHADOW};
        background-color: white;
    }}

    .cp-metric-value {{
        color: {branding.PRIMARY_COLOR};
        font-size: 28px;
        font-weight: 700;
        margin-bottom: 5px;
    }}

    .cp-metric-title {{
        font-weight: 600;
        margin-top: -10px;
    }}

    .cp-metric-description {{
        color: {branding.SUBTEXT_COLOR};
        margin-top: -5px;
        font-size: 14px;
    }}

    /* Global button styles */
    .stButton > button {{
        background-color: {branding.PRIMARY_COLOR} !important;
        color: white !important;
        border-radius: 6px !important;
        padding: 0.6rem 1.2rem !important;
        border: none !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        cursor: pointer !important;
        transition: background-color 0.2s ease-in-out;
    }}

    .stButton > button:hover {{
        background-color: #3A78C2 !important;
        color: white !important;
    }}

    </style>
    """

    st.markdown(css, unsafe_allow_html=True)
