# header.py
import streamlit as st

def render_header(logo_path: str = "assets/icons/logo.png"):
    st.markdown('<div class="cp-header">', unsafe_allow_html=True)

    # LEFT SIDE
    st.markdown('<div class="cp-header-left">', unsafe_allow_html=True)
    st.image(logo_path, width=210)
    st.markdown(
        '<p class="cp-header-tagline">Precision insights through biomarker-driven prediction</p>',
        unsafe_allow_html=True
    )
    st.markdown('</div>', unsafe_allow_html=True)  # closes cp-header-left

    st.markdown('</div>', unsafe_allow_html=True)  # closes cp-header
