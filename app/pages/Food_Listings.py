import sys
from pathlib import Path

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.utils import fetch_data, load_theme, page_header

load_theme()

page_header(
    "Listings",
    "Food Listings",
    "Browse available food by name, city, provider, food type, and meal category."
)

df = fetch_data("""
SELECT f.Food_ID,
       f.Food_Name,
       f.Quantity,
       f.Expiry_Date,
       f.Provider_ID,
       p.Name AS Provider_Name,
       f.Provider_Type,
       f.Location,
       f.Food_Type,
       f.Meal_Type
FROM food_listings f
JOIN providers p
    ON f.Provider_ID = p.Provider_ID
ORDER BY f.Expiry_Date, f.Food_ID
""")

search_food = st.text_input("Search Food Name")

if search_food:
    df = df[
        df["Food_Name"].str.contains(
            search_food,
            case=False,
            na=False
        )
    ]

filter_col1, filter_col2, filter_col3, filter_col4 = st.columns(4)

with filter_col1:
    city = st.selectbox(
        "Select City",
        ["All"] + sorted(df["Location"].dropna().unique().tolist())
    )

with filter_col2:
    provider = st.selectbox(
        "Select Provider",
        ["All"] + sorted(df["Provider_Name"].dropna().unique().tolist())
    )

with filter_col3:
    food_type = st.selectbox(
        "Select Food Type",
        ["All"] + sorted(df["Food_Type"].dropna().unique().tolist())
    )

with filter_col4:
    meal_type = st.selectbox(
        "Select Meal Type",
        ["All"] + sorted(df["Meal_Type"].dropna().unique().tolist())
    )

if city != "All":
    df = df[df["Location"] == city]

if provider != "All":
    df = df[df["Provider_Name"] == provider]

if food_type != "All":
    df = df[df["Food_Type"] == food_type]

if meal_type != "All":
    df = df[df["Meal_Type"] == meal_type]

metric_col1, metric_col2, metric_col3 = st.columns(3)
metric_col1.metric("Visible Listings", len(df))
metric_col2.metric("Total Quantity", int(df["Quantity"].sum()) if not df.empty else 0)
metric_col3.metric("Cities Covered", df["Location"].nunique() if not df.empty else 0)

st.dataframe(df, width="stretch")
