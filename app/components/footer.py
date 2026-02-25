# footer.py
# Footer component for ClarityPredict 2.0.

import streamlit as st

def render_footer():
    st.markdown(
        """
        <div class="cp-footer">
            <p><strong>ClarityPredict©</strong> – Prototype for explainable biomarker prediction</p>
            <p>
                Developed by <strong>Torbjørn Kleiven</strong><br>
                Bachelor of Science in Computer Science<br>
                Specialization in Machine Learning
            </p>
            <p>
                Moss / Oslo, Norway<br>
                <a href="mailto:tk@infera.no">tk@infera.no</a> |
                <a href="https://github.com/torbkle" target="_blank">GitHub</a> |
                <span style="vertical-align: middle;">MIT License</span>
            </p>
            <p style="margin-top: 10px;">
                © 2026 Torbjørn Kleiven – For demonstration and research purposes only.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

