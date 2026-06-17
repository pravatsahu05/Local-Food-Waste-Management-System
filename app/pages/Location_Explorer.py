import sys
from pathlib import Path
import importlib

import plotly.express as px
import streamlit as st

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

load_theme()

page_header(
    "Locator",
    "Location Explorer",
    "Find available food and nearby coordination contacts by city."
)

city_summary = fetch_data("""
SELECT Location,
       COUNT(*) AS Listings,
       SUM(Quantity) AS Total_Quantity,
       MIN(Expiry_Date) AS Nearest_Expiry
FROM food_listings
GROUP BY Location
ORDER BY Listings DESC, Total_Quantity DESC
""")

demand_summary = fetch_data("""
SELECT f.Location,
       COUNT(*) AS Claims
FROM claims c
JOIN food_listings f
    ON c.Food_ID = f.Food_ID
GROUP BY f.Location
ORDER BY Claims DESC
LIMIT 1
""")

top_supply = city_summary.iloc[0]
top_demand = demand_summary.iloc[0] if not demand_summary.empty else None

insight_cards(
    [
        {
            "label": "Top Supply City",
            "value": str(top_supply["Location"]),
            "note": f"{int(top_supply['Listings'])} listings and {int(top_supply['Total_Quantity'])} total quantity."
        },
        {
            "label": "Highest Demand City",
            "value": str(top_demand["Location"]) if top_demand is not None else "N/A",
            "note": f"{int(top_demand['Claims'])} total claims recorded." if top_demand is not None else "No claims available."
        },
        {
            "label": "Cities Covered",
            "value": f"{city_summary['Location'].nunique():,}",
            "note": "Locations with available food listings."
        },
        {
            "label": "Nearest Expiry",
            "value": str(city_summary["Nearest_Expiry"].min()),
            "note": "Soonest expiry date across all listed food."
        }
    ]
)

city = st.selectbox(
    "Choose City",
    sorted(city_summary["Location"].dropna().unique().tolist())
)

selected_city_summary = city_summary[city_summary["Location"] == city]

if not selected_city_summary.empty:
    row = selected_city_summary.iloc[0]
    col1, col2, col3 = st.columns(3)
    col1.metric("Available Listings", int(row["Listings"]))
    col2.metric("Total Quantity", int(row["Total_Quantity"]))
    col3.metric("Nearest Expiry", str(row["Nearest_Expiry"]))

city_rank = city_summary.head(20)

fig = px.bar(
    city_rank,
    x="Listings",
    y="Location",
    color="Total_Quantity",
    orientation="h",
    title="Top Food Availability Locations",
    color_continuous_scale="Teal"
)

st.plotly_chart(chart_theme(fig), width="stretch")

listings = fetch_data(
    """
    SELECT f.Food_ID,
           f.Food_Name,
           f.Quantity,
           f.Expiry_Date,
           f.Food_Type,
           f.Meal_Type,
           p.Name AS Provider_Name,
           p.Type AS Provider_Type,
           p.Contact AS Provider_Contact
    FROM food_listings f
    JOIN providers p
        ON f.Provider_ID = p.Provider_ID
    WHERE f.Location = %s
    ORDER BY f.Expiry_Date, f.Quantity DESC
    """,
    params=(city,)
)

receivers = fetch_data(
    """
    SELECT Name,
           Type,
           City,
           Contact
    FROM receivers
    WHERE City = %s
    ORDER BY Name
    """,
    params=(city,)
)

providers = fetch_data(
    """
    SELECT Name,
           Type,
           City,
           Contact
    FROM providers
    WHERE City = %s
    ORDER BY Name
    """,
    params=(city,)
)

tab1, tab2, tab3 = st.tabs(
    [
        "Food Near This City",
        "Provider Contacts",
        "Receiver Contacts"
    ]
)

with tab1:
    st.dataframe(listings, width="stretch")

with tab2:
    st.dataframe(providers, width="stretch")

with tab3:
    st.dataframe(receivers, width="stretch")

app_footer()
