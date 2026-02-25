import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from app.layout.style import inject_global_styles
from app.components.header import render_header
from app.components.footer import render_footer
from app.services.prediction_service import PredictionService


# ---------------------------------------------------------
# Load model + dataset
# ---------------------------------------------------------
@st.cache_resource
def load_service():
    return PredictionService("models/model.pkl")

service = load_service()


@st.cache_data
def load_data():
    return pd.read_csv("data/dataset.csv")


# ---------------------------------------------------------
# MAIN PAGE
# ---------------------------------------------------------
def main():
    st.set_page_config(
        page_title="ClarityPredict – Explore Data",
        layout="wide",
        page_icon="assets/icons/ico_logo.png"
    )

    inject_global_styles()

    st.markdown("<div class='cp-container'>", unsafe_allow_html=True)
    render_header()

    df = load_data()

    # ---------------------------------------------------------
    # INTRO SECTION
    # ---------------------------------------------------------
    st.markdown("<div class='cp-section'><div class='cp-card'>", unsafe_allow_html=True)

    st.markdown(
        """
        ### Explore the Biomarker Dataset  
        This page provides an exploratory overview of the dataset used in ClarityPredict.  
        It helps clinicians and developers understand the structure, distributions, and relationships within the data.

        You will find:
        - Dataset overview  
        - Statistical summaries  
        - Distribution plots  
        - Correlation heatmap  
        - Interactive scatter relationships  
        - Global feature importance  
        """,
        unsafe_allow_html=True
    )

    st.markdown("</div></div>", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # DATASET OVERVIEW
    # ---------------------------------------------------------
    st.subheader("Dataset Overview")
    st.markdown("<div class='cp-section'><div class='cp-card'>", unsafe_allow_html=True)

    st.write(f"**Rows:** {df.shape[0]}")
    st.write(f"**Columns:** {df.shape[1]}")
    st.dataframe(df.head())

    st.markdown("</div></div>", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # STATISTICAL SUMMARY
    # ---------------------------------------------------------
    st.subheader("Statistical Summary")
    st.markdown("<div class='cp-section'><div class='cp-card'>", unsafe_allow_html=True)

    st.dataframe(df.describe().T)

    st.markdown("</div></div>", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # DISTRIBUTION PLOTS
    # ---------------------------------------------------------
    st.subheader("Distribution of Biomarkers")
    st.markdown("<div class='cp-section'><div class='cp-card'>", unsafe_allow_html=True)

    numeric_cols = df.select_dtypes(include=["float64", "int64"]).columns
    selected_col = st.selectbox("Select a biomarker:", numeric_cols)

    fig, ax = plt.subplots(figsize=(6, 4))
    sns.histplot(df[selected_col], kde=True, ax=ax, color="#457B9D")
    ax.set_title(f"Distribution of {selected_col}")
    ax.set_xlabel(selected_col)
    ax.set_ylabel("Count")
    st.pyplot(fig)

    st.markdown("</div></div>", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # CORRELATION HEATMAP
    # ---------------------------------------------------------
    st.subheader("Correlation Heatmap")
    st.markdown("<div class='cp-section'><div class='cp-card'>", unsafe_allow_html=True)

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(df.corr(), annot=False, cmap="Blues", ax=ax)
    ax.set_title("Correlation Between Biomarkers")
    st.pyplot(fig)

    st.markdown("</div></div>", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # INTERACTIVE SCATTER RELATIONSHIPS
    # ---------------------------------------------------------
    st.subheader("Explore Relationships Between Biomarkers")
    st.markdown("<div class='cp-section'><div class='cp-card'>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        x_var = st.selectbox("X‑axis", numeric_cols)

    with col2:
        y_var = st.selectbox("Y‑axis", numeric_cols)

    fig2, ax2 = plt.subplots(figsize=(7, 5))
    sns.scatterplot(data=df, x=x_var, y=y_var, ax=ax2, color="#457B9D")
    sns.regplot(data=df, x=x_var, y=y_var, scatter=False, ax=ax2, color="#1D3557")
    ax2.set_title(f"{x_var} vs {y_var}")
    st.pyplot(fig2)

    st.markdown("</div></div>", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # GLOBAL FEATURE IMPORTANCE
    # ---------------------------------------------------------
    st.subheader("Global Feature Importance")
    st.markdown("<div class='cp-section'><div class='cp-card'>", unsafe_allow_html=True)

    model = service.model

    if hasattr(model, "feature_importances_"):
        importance = model.feature_importances_
        features = service.expected_features

        importance_df = pd.DataFrame({
            "Feature": features,
            "Importance": importance
        }).sort_values("Importance", ascending=False)

        fig3, ax3 = plt.subplots(figsize=(6, 4))
        sns.barplot(data=importance_df, x="Importance", y="Feature", ax=ax3, color="#457B9D")
        ax3.set_title("Feature Importance (Model-Based)")
        st.pyplot(fig3)
    else:
        st.info("This model does not provide built-in feature importance.")

    st.markdown("</div></div>", unsafe_allow_html=True)

    render_footer()
    st.markdown("</div>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()
