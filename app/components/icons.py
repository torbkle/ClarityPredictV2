# icons.py
# Reusable icon component for ClarityPredict 2.0.

import streamlit as st

def show_icon(icon: str, label: str = "", size: int = 24):
    st.markdown(
        f"""
        <div style="display: flex; align-items: center; gap: 10px;">
            <span style="font-size: {size}px;">{icon}</span>
            <span style="font-size: 16px;">{label}</span>
        </div>
        """,
        unsafe_allow_html=True
    )
