# About page for ClarityPredict 2.0

import streamlit as st

from app.layout.style import inject_global_styles
from app.components.header import render_header
from app.components.footer import render_footer


def main():
    st.set_page_config(
        page_title="ClarityPredict – About",
        layout="wide",
        page_icon="assets/icons/ico_logo.png"
    )

    inject_global_styles()

    st.markdown("<div class='cp-container'>", unsafe_allow_html=True)
    render_header()

    # ---------------------------------------------------------
    # INTRO CARD
    # ---------------------------------------------------------
    st.markdown("<div class='cp-section'><div class='cp-card'>", unsafe_allow_html=True)

    st.markdown(
        """
        <h2>About ClarityPredict</h2>
        <p>
            ClarityPredict 2.0 is a clinically oriented, explainable machine‑learning platform 
            designed for biomarker‑based risk assessment, interactive data exploration, and 
            transparent model interpretation. The system combines modern predictive modeling 
            with a clean, modular interface tailored for clinical and research workflows.
        </p>
        <p>
            Every prediction is accompanied by SHAP‑based explanations, providing clear insight 
            into how each biomarker contributes to the model’s output. The platform is built 
            with a maintainable architecture that supports extensibility, reproducibility, and 
            future integration into clinical decision‑support environments.
        </p>
        """,
        unsafe_allow_html=True
    )

    st.markdown("</div></div>", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # PROJECT STRUCTURE
    # ---------------------------------------------------------
    st.subheader("Project Structure")
    st.markdown("<div class='cp-section'><div class='cp-card'>", unsafe_allow_html=True)

    st.markdown(
        """
        ClarityPredict follows a clean and modular project layout:

        - <strong>app/components</strong> – Header, footer, metric cards, and UI elements  
        - <strong>app/layout</strong> – Global CSS, branding, and styling  
        - <strong>app/pages</strong> – Streamlit multipage views (Overview, Explore, Prediction, About)  
        - <strong>app/services</strong> – PredictionService, preprocessing, model inference, SHAP logic  
        - <strong>models/</strong> – Trained model and preprocessing artifacts  
        - <strong>data/</strong> – Biomarker dataset used for training  
        - <strong>notebooks/</strong> – Training pipeline and experimentation  

        This structure separates presentation, logic, configuration, and data handling, 
        ensuring maintainability and scalability.
        """,
        unsafe_allow_html=True
    )

    st.markdown("</div></div>", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # MACHINE LEARNING PIPELINE
    # ---------------------------------------------------------
    st.subheader("Machine‑Learning Pipeline")
    st.markdown("<div class='cp-section'><div class='cp-card'>", unsafe_allow_html=True)

    st.markdown(
        """
        ClarityPredict uses a reproducible and transparent ML pipeline:

        <strong>1. Dataset</strong>  
        Biomarker dataset with six numerical features:  
        <em>Age, BMI, Glucose, Insulin, HDL, LDL</em>

        <strong>2. Preprocessing</strong>  
        - Median imputation  
        - Standard scaling  
        - Fixed feature ordering  

        <strong>3. Model Training</strong>  
        - XGBoost Regressor  
        - Hyperparameter tuning  
        - Evaluation and selection  

        <strong>4. Model Artifacts</strong>  
        - <code>model.pkl</code>  
        - <code>scaler.pkl</code>  
        - <code>imputer.pkl</code>  

        <strong>5. PredictionService</strong>  
        - Loads model and preprocessors  
        - Prepares input  
        - Generates prediction  
        - Computes SHAP explanations  

        <strong>6. Streamlit UI</strong>  
        - Prediction page  
        - Explore page  
        - SHAP visualization  
        - Interactive plots  
        """,
        unsafe_allow_html=True
    )

    st.markdown("</div></div>", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # EXPLAINABILITY
    # ---------------------------------------------------------
    st.subheader("Explainability (SHAP)")
    st.markdown("<div class='cp-section'><div class='cp-card'>", unsafe_allow_html=True)

    st.markdown(
        """
        ClarityPredict uses <strong>SHAP (SHapley Additive exPlanations)</strong> to ensure 
        transparent and clinically meaningful model interpretation.

        The system provides:
        - Local explanations for each prediction  
        - Feature contribution bar charts  
        - Waterfall plots for detailed breakdowns  
        - Summary plots for global feature behavior  

        SHAP ensures that every prediction is interpretable and grounded in measurable biomarker contributions.
        """,
        unsafe_allow_html=True
    )

    st.markdown("</div></div>", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # PURPOSE
    # ---------------------------------------------------------
    st.subheader("Purpose")
    st.markdown("<div class='cp-section'><div class='cp-card'>", unsafe_allow_html=True)

    st.markdown(
        """
        ClarityPredict demonstrates:

        - A modular architecture suitable for real‑world ML applications  
        - Clean UI/UX with reusable components  
        - Explainable predictions using SHAP  
        - A structured approach to biomarker exploration  
        - A transparent ML pipeline ready for academic or clinical presentation  

        The platform is intended for educational and demonstration purposes.
        """,
        unsafe_allow_html=True
    )

    st.markdown("</div></div>", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # FOOTER
    # ---------------------------------------------------------
    render_footer()
    st.markdown("</div>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()
