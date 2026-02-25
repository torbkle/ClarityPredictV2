import streamlit as st

def hero_section():
    from app.layout import branding

    st.markdown(
f"""
<div class="cp-section" style="margin-top: 5px; margin-bottom: 25px;">
<h2 style="
    font-size: 30px;
    font-weight: 600;
    color: {branding.PRIMARY_COLOR};
    margin-bottom: 10px;
">
    Overview
</h2>

<p style="
    font-size: 17px;
    color: {branding.SUBTEXT_COLOR};
    max-width: 750px;
    line-height: 1.6;
    margin-bottom: 0px;
">
    Explore the core features of ClarityPredict, including biomarker analytics,
    interactive data exploration, and explainable machine‑learning predictions.
</p>
</div>
""",
        unsafe_allow_html=True
    )
