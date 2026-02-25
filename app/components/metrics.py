# metrics.py
# Reusable metric card component for ClarityPredict 2.0.

import streamlit as st

def metric_card(title: str, value: str = None, description: str = "", image_path: str = None):
    st.markdown("<div class='cp-metric-card'>", unsafe_allow_html=True)

    # ICON AREA (server-side loading = works reliably)
    if image_path:
        st.image(image_path, width=56)
    elif value:
        st.markdown(
            f"""
            <div class="cp-metric-icon" style="font-size: 42px; margin-bottom: 6px;">
                {value}
            </div>
            """,
            unsafe_allow_html=True
        )

    # TITLE
    st.markdown(f"<div class='cp-metric-title'>{title}</div>", unsafe_allow_html=True)

    # DESCRIPTION
    st.markdown(f"<div class='cp-metric-description'>{description}</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
