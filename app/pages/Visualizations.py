import sys
from pathlib import Path

import plotly.express as px
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.utils import chart_theme, fetch_data, load_theme, page_header

load_theme()

page_header(
    "Analytics",
    "Food Waste Analytics",
    "EDA views for contribution, availability, demand, expiry, and distribution patterns."
)

tab1, tab2, tab3 = st.tabs(
    [
        "Supply Trends",
        "Claim Demand",
        "Expiry Monitor"
    ]
)

with tab1:
    provider_df = fetch_data("""
    SELECT Provider_Type,
           SUM(Quantity) AS Total_Food
    FROM food_listings
    GROUP BY Provider_Type
    ORDER BY Total_Food DESC
    """)

    fig = px.bar(
        provider_df,
        x="Provider_Type",
        y="Total_Food",
        color="Provider_Type",
        title="Food Contribution by Provider Type",
        color_discrete_sequence=["#42d392", "#37c6ff", "#f6c453", "#ff6b7a"]
    )

    st.plotly_chart(chart_theme(fig), width="stretch")

    city_df = fetch_data("""
    SELECT Location,
           SUM(Quantity) AS Total_Food,
           COUNT(*) AS Listings
    FROM food_listings
    GROUP BY Location
    ORDER BY Total_Food DESC
    LIMIT 15
    """)

    fig_city = px.bar(
        city_df,
        x="Total_Food",
        y="Location",
        color="Listings",
        orientation="h",
        title="Top Cities by Food Quantity",
        color_continuous_scale="Teal"
    )

    st.plotly_chart(chart_theme(fig_city), width="stretch")

with tab2:
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

    st.plotly_chart(chart_theme(fig2), width="stretch")

    food_claims = fetch_data("""
    SELECT f.Food_Name,
           COUNT(*) AS Total_Claims
    FROM claims c
    JOIN food_listings f
        ON c.Food_ID = f.Food_ID
    GROUP BY f.Food_Name
    ORDER BY Total_Claims DESC
    LIMIT 12
    """)

    fig_claims = px.bar(
        food_claims,
        x="Food_Name",
        y="Total_Claims",
        color="Food_Name",
        title="Most Claimed Food Items",
        color_discrete_sequence=["#42d392", "#37c6ff", "#f6c453", "#ff6b7a"]
    )

    st.plotly_chart(chart_theme(fig_claims), width="stretch")

    meal_claims = fetch_data("""
    SELECT f.Meal_Type,
           COUNT(*) AS Claims
    FROM claims c
    JOIN food_listings f
        ON c.Food_ID = f.Food_ID
    GROUP BY f.Meal_Type
    ORDER BY Claims DESC
    """)

    fig_meal = px.bar(
        meal_claims,
        x="Meal_Type",
        y="Claims",
        color="Meal_Type",
        title="Claims by Meal Type",
        color_discrete_sequence=["#42d392", "#37c6ff", "#f6c453", "#ff6b7a"]
    )

    st.plotly_chart(chart_theme(fig_meal), width="stretch")

with tab3:
    expiry_df = fetch_data("""
    SELECT Expiry_Date,
           COUNT(*) AS Listings,
           SUM(Quantity) AS Quantity
    FROM food_listings
    GROUP BY Expiry_Date
    ORDER BY Expiry_Date
    LIMIT 30
    """)

    fig_expiry = px.line(
        expiry_df,
        x="Expiry_Date",
        y="Quantity",
        markers=True,
        title="Quantity by Expiry Date"
    )

    st.plotly_chart(chart_theme(fig_expiry), width="stretch")

    urgent_df = fetch_data("""
    SELECT Food_ID,
           Food_Name,
           Quantity,
           Expiry_Date,
           Location,
           Provider_Type,
           Food_Type,
           Meal_Type
    FROM food_listings
    WHERE Expiry_Date <= CURDATE() + INTERVAL 2 DAY
    ORDER BY Expiry_Date, Quantity DESC
    """)

    st.dataframe(urgent_df, width="stretch")
