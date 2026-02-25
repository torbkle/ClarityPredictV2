# Prediction page for ClarityPredict 2.0

import streamlit as st
import shap
import matplotlib.pyplot as plt
import pandas as pd

from app.layout.style import inject_global_styles
from app.components.header import render_header
from app.components.footer import render_footer
from app.components.metrics import metric_card
from app.services.prediction_service import PredictionService


# ---------------------------------------------------------
# Load PredictionService
# ---------------------------------------------------------
@st.cache_resource
def load_service():
    return PredictionService("models/model.pkl")

service = load_service()


# ---------------------------------------------------------
# MAIN PAGE
# ---------------------------------------------------------
def main():
    st.set_page_config(
        page_title="ClarityPredict – Prediction",
        layout="wide",
        page_icon="assets/icons/ico_logo.png"
    )

    inject_global_styles()

    st.markdown("<div class='cp-container'>", unsafe_allow_html=True)
    render_header()

    # ---------------------------------------------------------
    # INTRO SECTION
    # ---------------------------------------------------------
    st.markdown("<div class='cp-section'><div class='cp-card'>", unsafe_allow_html=True)

    st.markdown(
        """
        ### Model‑Based Risk Estimation  
        This page provides a personalized risk estimate based on six routinely measured biomarkers.  
        The model produces:
        - A **continuous predicted value** representing estimated risk or severity  
        - A **SHAP explanation** showing how each biomarker contributed to the prediction  
        """,
        unsafe_allow_html=True
    )

    st.markdown("</div></div>", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # INPUT + PREDICTION LAYOUT
    # ---------------------------------------------------------
    st.markdown("<div class='cp-section'>", unsafe_allow_html=True)
    col_left, col_right = st.columns([1, 1])

    # ---------------- LEFT COLUMN: INPUT --------------------
    with col_left:
        st.markdown("<div class='cp-card'>", unsafe_allow_html=True)
        st.subheader("Input Biomarkers")

        with st.form("prediction_form"):
            age = st.number_input("Age", min_value=18, max_value=100, value=45)
            bmi = st.number_input("BMI", min_value=10.0, max_value=60.0, value=24.5)
            glucose = st.number_input("Glucose", min_value=50.0, max_value=300.0, value=90.0)
            insulin = st.number_input("Insulin", min_value=0.0, max_value=300.0, value=80.0)
            hdl = st.number_input("HDL Cholesterol", min_value=10.0, max_value=120.0, value=55.0)
            ldl = st.number_input("LDL Cholesterol", min_value=10.0, max_value=300.0, value=120.0)

            submitted = st.form_submit_button("Predict")

        st.markdown("</div>", unsafe_allow_html=True)

    # ---------------- RIGHT COLUMN: PREDICTION --------------
    with col_right:
        st.markdown("<div class='cp-card'>", unsafe_allow_html=True)
        st.subheader("Prediction Result")

        if submitted:
            input_data = {
                "age": age,
                "bmi": bmi,
                "glucose": glucose,
                "insulin": insulin,
                "hdl": hdl,
                "ldl": ldl,
            }

            result = service.run(input_data)

            metric_card(
                title="Predicted Value",
                value=f"{result['prediction']:.3f}",
                description="Model output based on your biomarker inputs"
            )

        else:
            st.info("Enter biomarker values and click **Predict** to see the result.")

        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # SHAP EXPLANATION SECTION
    # ---------------------------------------------------------
    if submitted:
        st.markdown("<div class='cp-section'><div class='cp-card'>", unsafe_allow_html=True)
        st.subheader("Explainability (SHAP)")

        shap_values = result["shap_values"]
        feature_names = result["feature_names"]
        base_value = result["base_value"]

        tab1, tab2, tab3 = st.tabs(["Summary Plot", "Feature Impact", "Waterfall Plot"])

        # --- TAB 1: SUMMARY PLOT ---
        with tab1:
            try:
                plt.figure(figsize=(7, 4))
                shap.summary_plot(
                    shap_values,
                    pd.DataFrame([input_data])[feature_names],
                    plot_type="dot",
                    show=False
                )
                st.pyplot(plt.gcf())
                plt.clf()
            except Exception as e:
                st.error(f"Summary plot failed: {e}")

        # --- TAB 2: BAR CHART ---
        with tab2:
            try:
                shap_df = pd.DataFrame({
                    "Feature": feature_names,
                    "SHAP Value": shap_values[0]
                }).sort_values("SHAP Value", key=abs, ascending=False)

                fig_bar, ax_bar = plt.subplots(figsize=(6, 4))
                ax_bar.barh(shap_df["Feature"], shap_df["SHAP Value"], color="#457B9D")
                ax_bar.set_xlabel("Impact on Prediction")
                ax_bar.set_title("SHAP Feature Importance")
                plt.gca().invert_yaxis()

                st.pyplot(fig_bar)
            except Exception as e:
                st.error(f"Bar chart failed: {e}")

        # --- TAB 3: WATERFALL PLOT ---
        with tab3:
            try:
                shap_expl = shap.Explanation(
                    values=shap_values[0],
                    base_values=base_value,
                    data=pd.DataFrame([input_data])[feature_names].iloc[0],
                    feature_names=feature_names
                )

                plt.figure(figsize=(8, 5))
                shap.plots.waterfall(shap_expl, show=False)
                st.pyplot(plt.gcf())
                plt.clf()

            except Exception as e:
                st.error(f"Waterfall plot failed: {e}")

        st.markdown("</div></div>", unsafe_allow_html=True)

    render_footer()
    st.markdown("</div>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()
