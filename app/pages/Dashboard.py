import streamlit as st
import plotly.express as px

import importlib
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import app.utils as app_utils

app_utils = importlib.reload(app_utils)

app_footer = app_utils.app_footer
chart_theme = app_utils.chart_theme
fetch_data = app_utils.fetch_data
insight_cards = app_utils.insight_cards
load_theme = app_utils.load_theme
page_header = app_utils.page_header
priority_food_cards = app_utils.priority_food_cards

load_theme()

page_header(
    "Dashboard",
    "Operations Dashboard",
    "A high-level view of providers, receivers, food listings, claims, and claim status."
)

providers = fetch_data("SELECT COUNT(*) AS total FROM providers")
receivers = fetch_data("SELECT COUNT(*) AS total FROM receivers")
food = fetch_data("SELECT COUNT(*) AS total FROM food_listings")
claims = fetch_data("SELECT COUNT(*) AS total FROM claims")
completed_claims = fetch_data("SELECT COUNT(*) AS total FROM claims WHERE Status = 'Completed'")
total_quantity = fetch_data("SELECT COALESCE(SUM(Quantity), 0) AS total FROM food_listings")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Providers", providers.iloc[0, 0])
c2.metric("Receivers", receivers.iloc[0, 0])
c3.metric("Food Listings", food.iloc[0, 0])
c4.metric("Claims", claims.iloc[0, 0])

insight_cards(
    [
        {
            "label": "Total Food Quantity",
            "value": f"{int(total_quantity.iloc[0, 0]):,}",
            "note": "Aggregate food quantity available across all listings."
        },
        {
            "label": "Completed Claims",
            "value": f"{int(completed_claims.iloc[0, 0]):,}",
            "note": "Confirmed redistributions completed through the platform."
        },
        {
            "label": "Completion Rate",
            "value": f"{(completed_claims.iloc[0, 0] / claims.iloc[0, 0] * 100):.1f}%",
            "note": "Share of claims currently marked as completed."
        },
        {
            "label": "Network Size",
            "value": f"{int(providers.iloc[0, 0] + receivers.iloc[0, 0]):,}",
            "note": "Combined provider and receiver ecosystem."
        }
    ]
)

st.subheader("High Priority Food")

urgent_df = fetch_data("""
SELECT Food_Name,
       Quantity,
       Expiry_Date,
       Location,
       Provider_Type,
       Meal_Type
FROM food_listings
WHERE Expiry_Date <= CURDATE() + INTERVAL 2 DAY
ORDER BY Expiry_Date, Quantity DESC
LIMIT 3
""")

priority_food_cards(urgent_df)

provider_df = fetch_data("""
SELECT Provider_Type,
       SUM(Quantity) AS Total
FROM food_listings
GROUP BY Provider_Type
""")

fig = px.bar(
    provider_df,
    x="Provider_Type",
    y="Total",
    color="Provider_Type",
    title="Food Contribution by Provider Type",
    color_discrete_sequence=["#42d392", "#37c6ff", "#f6c453", "#ff6b7a"]
)

st.plotly_chart(
    chart_theme(fig),
    width="stretch"
)

claim_df = fetch_data("""
SELECT Status,
       COUNT(*) AS Total
FROM claims
GROUP BY Status
""")

fig2 = px.pie(
    claim_df,
    names="Status",
    values="Total",
    title="Claim Status Distribution",
    hole=0.45,
    color_discrete_sequence=["#42d392", "#f6c453", "#ff6b7a"]
)

st.plotly_chart(
    chart_theme(fig2),
    width="stretch"
)

st.markdown(
    """
    <div class="feature-grid">
        <div class="feature-card">
            <strong>City Hotspots</strong>
            <span>Identify cities with the highest food donations and recurring demand.</span>
        </div>
        <div class="feature-card">
            <strong>Claim Health</strong>
            <span>Watch pending claims closely so good food does not sit idle.</span>
        </div>
        <div class="feature-card">
            <strong>Provider Impact</strong>
            <span>Compare contribution volume across provider categories.</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

app_footer()
