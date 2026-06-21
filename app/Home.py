import streamlit as st

import importlib
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import app.utils as app_utils

app_utils = importlib.reload(app_utils)

app_footer = app_utils.app_footer
fetch_data = app_utils.fetch_data
load_theme = app_utils.load_theme

st.set_page_config(
    page_title="Local Food Waste Management System",
    layout="wide",
    initial_sidebar_state="expanded"
)

load_theme()

summary = fetch_data("""
SELECT
    (SELECT COUNT(*) FROM providers) AS providers,
    (SELECT COUNT(*) FROM receivers) AS receivers,
    (SELECT COUNT(*) FROM food_listings) AS listings,
    (SELECT COALESCE(SUM(Quantity), 0) FROM food_listings) AS quantity,
    (SELECT COUNT(*) FROM claims WHERE Status = 'Completed') AS completed_claims
""")

summary_row = summary.iloc[0]

st.markdown(
    """
    <section class="app-hero">
        <div>
            <div class="eyebrow">Surplus food, smarter routing</div>
            <h1>Local Food Waste Management System</h1>
            <p>
                Coordinate providers, receivers, claims, and analytics from one
                modern dashboard built to reduce waste and move food where it is needed.
            </p>
        </div>
    </section>
    """,
    unsafe_allow_html=True
)

metric_cols = st.columns(4)
metric_cols[0].metric("Food Available", f"{int(summary_row['quantity']):,}")
metric_cols[1].metric("Providers", f"{int(summary_row['providers']):,}")
metric_cols[2].metric("Receivers", f"{int(summary_row['receivers']):,}")
metric_cols[3].metric("Completed Claims", f"{int(summary_row['completed_claims']):,}")

st.caption(
    "Live values from the connected MySQL database. Use the sidebar pages to explore listings, providers, claims, and analytics."
)

st.markdown(
    """
    <div class="feature-grid">
        <div class="feature-card">
            <strong>Provider Coordination</strong>
            <span>Track restaurants, supermarkets, grocery stores, and catering partners.</span>
        </div>
        <div class="feature-card">
            <strong>Live Food Listings</strong>
            <span>Filter available food by city, food type, meal type, and expiry.</span>
        </div>
        <div class="feature-card">
            <strong>Claim Intelligence</strong>
            <span>Monitor pending, completed, and cancelled claims with visual insights.</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.sidebar.success("Select a page to explore")

app_footer()
