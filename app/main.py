# Entry point for ClarityPredict 2.0

import os
import sys
import streamlit as st
from PIL import Image

# Ensure project root is in Python path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from app.layout.style import inject_global_styles
from app.components.header import render_header
from app.components.footer import render_footer
from app.components.hero import hero_section
from app.components.metrics import metric_card


def main():
    # --- Load favicon using absolute path ---
    favicon_path = os.path.join(PROJECT_ROOT, "assets", "icons", "ico_logo.png")
    logo = Image.open(favicon_path)

    st.set_page_config(
        page_title="ClarityPredict",
        layout="wide",
        page_icon=logo
    )

    inject_global_styles()

    # MAIN CONTAINER
    st.markdown("<div class='cp-container'>", unsafe_allow_html=True)

    # HEADER
    render_header()

    # HERO SECTION
    hero_section()

    # INTRODUCTION CARD
    st.markdown("<div class='cp-section'><div class='cp-card'>", unsafe_allow_html=True)

    st.markdown(
        """
        <h2>Welcome to ClarityPredict</h2>
        <p>
            ClarityPredict is a streamlined, clinically oriented machine‑learning platform for
            biomarker‑based risk assessment and data exploration. The system combines modern
            predictive modeling with transparent, SHAP‑based explainability.
        </p>
        <p>
            Every prediction is accompanied by clear, interpretable insights, enabling clinicians
            and researchers to understand how each biomarker contributes to the model’s output.
            The platform is built with a modular architecture and a clean, distraction‑free UI
            designed for confident decision support.
        </p>

        """,
        unsafe_allow_html=True
    )

    st.markdown("</div></div>", unsafe_allow_html=True)

    # FEATURE HIGHLIGHTS
    st.subheader("What You Can Do")
    st.markdown("<div class='cp-section'>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    # --- Load icons using absolute paths ---
    explore_icon = os.path.join(PROJECT_ROOT, "assets", "icons", "explore.png")
    predict_icon = os.path.join(PROJECT_ROOT, "assets", "icons", "predict.png")
    docu_icon = os.path.join(PROJECT_ROOT, "assets", "icons", "docu.png")

    with col1:
        metric_card(
            title="Explore Data",
            image_path=explore_icon,
            description="Interactive visualizations of biomarker distributions and relationships"
        )

    with col2:
        metric_card(
            title="Predict Risk",
            image_path=predict_icon,
            description="Model‑based predictions with full SHAP explainability"
        )

    with col3:
        metric_card(
            title="Understand the System",
            image_path=docu_icon,
            description="Documentation, methodology, and architecture overview"
        )

    st.markdown("</div>", unsafe_allow_html=True)

    # CALL TO ACTION
    st.markdown("<div class='cp-section'><div class='cp-card'>", unsafe_allow_html=True)



    st.markdown("</div></div>", unsafe_allow_html=True)

    # FOOTER
    render_footer()

    st.markdown("</div>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()
