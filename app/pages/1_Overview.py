# Overview page for ClarityPredict 2.0

import streamlit as st

from app.layout.style import inject_global_styles
from app.components.header import render_header
from app.components.footer import render_footer
from app.components.hero import hero_section
from app.components.metrics import metric_card


def main():
    st.set_page_config(
        page_title="ClarityPredict – Overview",
        layout="wide",
        page_icon="assets/icons/ico_logo.png"
    )

    inject_global_styles()

    st.markdown("<div class='cp-container'>", unsafe_allow_html=True)

    render_header()


    # ---------------------------------------------------------
    # METRICS SECTION
    # ---------------------------------------------------------
    st.subheader("System Overview")
    st.markdown("<div class='cp-section'>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        metric_card(
            title="Patients Analyzed",
            value="12,482",
            description="Total number of patient records processed"
        )

    with col2:
        metric_card(
            title="Biomarkers Supported",
            value="18",
            description="CRP, Albumin, BMI, HbA1c, and more"
        )

    with col3:
        metric_card(
            title="Model Accuracy",
            value="92%",
            description="Based on internal validation"
        )

    st.markdown("</div>", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # COMING NEXT SECTION
    # ---------------------------------------------------------
    st.markdown(
        ""
    )

    st.subheader("Coming Next")


    st.markdown(
        """
        ClarityPredict is continuously evolving.  
        Upcoming features include:

        - **Interactive biomarker profiles**  
          Visualize patient‑specific biomarker trajectories.

        - **Risk interpretation modules**  
          Clinically grounded explanations of predicted risk levels.

        - **Patient‑level prediction history**  
          Track changes in predicted risk over time.

        These features are designed to support clinicians in making more informed, data‑driven decisions.
        """,
        unsafe_allow_html=True
    )

    st.markdown("</div></div>", unsafe_allow_html=True)

    render_footer()

    st.markdown("</div>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()
