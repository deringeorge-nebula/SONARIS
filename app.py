"""
app.py

Entry point for the SONARIS Streamlit application. Runs as the top-level UI
shell. At this stage it is a project dashboard showing module status, dataset
acquisition progress, and navigation scaffolding. Module-specific pages are
added here as each module reaches a usable state.

Run locally with: streamlit run app.py
"""

import sys
import os

# Ensure the project root is on sys.path regardless of where Streamlit is
# invoked from. On Hugging Face Spaces, the working directory is the repo root,
# but local invocation from a subdirectory can break relative imports.
# This block resolves that without requiring the user to set PYTHONPATH manually.
_PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

import streamlit as st
from config import settings

# =============================================================================
# Page configuration — must be the first Streamlit call in the script
# =============================================================================

st.set_page_config(
    page_title="SONARIS — Ship-Ocean Noise Acoustic Radiated Intelligence System",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =============================================================================
# Sidebar
# =============================================================================

with st.sidebar:
    st.title(settings.PROJECT_NAME)
    st.caption(f"v{settings.PROJECT_VERSION} | {settings.PROJECT_LICENSE} License")
    st.divider()

    st.subheader("Navigation")
    # Navigation options are placeholders. Each option will route to a dedicated
    # Streamlit page once the corresponding module is built. For now they all
    # render the "under construction" message in the main body.
    nav_selection = st.radio(
        label="Go to",
        options=[
            "Overview",
            "Predict URN",
            "Compliance Check",
            "Bioacoustic Impact",
            "Mitigation Planner",
            "URN Database",
        ],
        index=0,
        label_visibility="collapsed",
    )

    st.divider()
    st.subheader("Resources")
    st.markdown(
        f"""
- [GitHub Repository]({settings.PROJECT_GITHUB})
- [IMO MEPC.1/Circ.906 Rev.1](https://www.imo.org/en/OurWork/Environment/Pages/Underwater-noise.aspx)
- [ShipsEar Dataset](http://www.noiseatsea.es/)
- [QiandaoEar22 Dataset](https://arxiv.org/abs/2406.04354)
        """
    )

    st.divider()
    st.caption(
        "Built by a Naval Architecture student and music composer "
        "working at the intersection of ship engineering and acoustic science."
    )

# =============================================================================
# Main body
# =============================================================================

# Header
st.title("SONARIS")
st.subheader(settings.PROJECT_FULL_NAME)

col_m1, col_m2, col_m3 = st.columns(3)
with col_m1:
    st.metric(label="IMO Guidelines", value=settings.IMO_GUIDELINES_VERSION)
with col_m2:
    st.metric(label="Core Modules", value="6")
with col_m3:
    st.metric(label="Status", value="Active Development")

st.divider()

# =============================================================================
# Routing: non-Overview pages
# =============================================================================

if nav_selection != "Overview":
    st.info(
        f"**{nav_selection}** module is under construction. "
        "Check back as development progresses or follow the "
        f"[GitHub repository]({settings.PROJECT_GITHUB}) for updates."
    )
    st.stop()

# =============================================================================
# Overview page content
# =============================================================================

# Mission statement
st.markdown(
    """
SONARIS predicts a ship's underwater radiated noise spectrum from hull geometry,
propeller parameters, and engine data, then checks the result against IMO
MEPC.1/Circ.906 Rev.1 (2024) limits and calculates the biological interference
caused to five groups of marine mammals. It is designed for shipyards, researchers,
and environmental organisations that need design-stage acoustic assessment and cannot
access proprietary tools. The platform is open-source and free to use, modify, and
deploy anywhere in the world.
"""
)

st.divider()

# =============================================================================
# Module Status Dashboard
# =============================================================================

st.header("Module Status")

# Row 1
row1_col1, row1_col2 = st.columns(2)

with row1_col1:
    st.subheader("Module 1: Design Input Engine")
    st.write(
        "Accepts hull form coefficients, propeller geometry, engine type, "
        "rated RPM, and operational speed in knots."
    )
    st.success("Coming Soon")  # change to st.success("Active") once built
    st.caption("Tech: Python, dataclasses, Pydantic validation")

with row1_col2:
    st.subheader("Module 2: URN Prediction Core")
    st.write(
        "Predicts the full 1/3-octave band noise spectrum from 20 Hz to 20 kHz "
        "using a hybrid physics simulation and deep learning pipeline."
    )
    st.success("Coming Soon")
    st.caption("Tech: PyTorch, OpenFOAM, libAcoustics")

# Row 2
row2_col1, row2_col2 = st.columns(2)

with row2_col1:
    st.subheader("Module 3: IMO Compliance Checker")
    st.write(
        "Checks the predicted URN spectrum against IMO MEPC.1/Circ.906 Rev.1 "
        "(2024) limit tables and generates a downloadable compliance report."
    )
    st.success("Coming Soon")
    st.caption("Tech: IMO limit tables, ReportLab PDF generation")

with row2_col2:
    st.subheader("Module 4: Marine Bioacoustic Impact")
    st.write(
        "Maps ship noise against published audiogram curves for five marine mammal "
        "hearing groups and computes a Biological Interference Score for each."
    )
    st.success("Coming Soon")
    st.caption("Tech: librosa, scipy.signal, MFCC analysis")

# Row 3
row3_col1, row3_col2 = st.columns(2)

with row3_col1:
    st.subheader("Module 5: Mitigation Recommendation Engine")
    st.write(
        "Produces speed reduction targets, geographic routing avoidance zones, "
        "and hull and propeller modification suggestions ranked by expected dB reduction."
    )
    st.success("Coming Soon")
    st.caption("Tech: Rule-based recommendation engine, routing data")

with row3_col2:
    st.subheader("Module 6: Open URN Database")
    st.write(
        "A community-contributed, publicly searchable database of ship acoustic "
        "signatures. The first open-source database of its kind."
    )
    st.success("Coming Soon")
    st.caption("Tech: SQLite (dev), PostgreSQL (prod), public query API")

st.divider()

# =============================================================================
# Dataset Acquisition Status
# =============================================================================

st.header("Dataset Acquisition — Phase 1")

with st.expander("View dataset status", expanded=True):
    dataset_status = {
        "ShipsEar (Santos-Dominguez et al., 2016)": "Acquisition in progress",
        "QiandaoEar22 (arXiv:2406.04354)": "Pending",
        "Marine mammal audiograms (Southall et al., 2019)": "Pending",
        "IMO MEPC.1/Circ.906 Rev.1 limit tables": "Pending",
    }

    for dataset, status in dataset_status.items():
        col_ds, col_st = st.columns([3, 1])
        with col_ds:
            st.write(dataset)
        with col_st:
            if status == "Acquisition in progress":
                st.warning(status)
            else:
                st.info(status)

# =============================================================================
# Footer
# =============================================================================

st.divider()
st.markdown(
    f"<center style='color: grey; font-size: 0.85em;'>"
    f"SONARIS v{settings.PROJECT_VERSION} | "
    f"{settings.PROJECT_LICENSE} License | "
    f"github.com/deringeorge-nebula/SONARIS"
    f"</center>",
    unsafe_allow_html=True,
)