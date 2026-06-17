import streamlit as st

import importlib
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import app.utils as app_utils

app_utils = importlib.reload(app_utils)

app_footer = app_utils.app_footer
fetch_data = app_utils.fetch_data
insight_cards = app_utils.insight_cards
load_theme = app_utils.load_theme
page_header = app_utils.page_header

load_theme()

page_header(
    "Claims",
    "Claims",
    "Track receiver claims, linked food listings, current status, and claim timestamps."
)

query = """
SELECT
    c.Claim_ID,
    f.Food_Name,
    r.Name AS Receiver_Name,
    c.Status,
    c.Timestamp
FROM claims c
JOIN food_listings f
    ON c.Food_ID = f.Food_ID
JOIN receivers r
    ON c.Receiver_ID = r.Receiver_ID
"""

df = fetch_data(query)

status_counts = df["Status"].value_counts()

insight_cards(
    [
        {
            "label": "Total Claims",
            "value": f"{len(df):,}",
            "note": "All receiver food claims tracked in the system."
        },
        {
            "label": "Completed",
            "value": f"{int(status_counts.get('Completed', 0)):,}",
            "note": "Claims successfully fulfilled."
        },
        {
            "label": "Pending",
            "value": f"{int(status_counts.get('Pending', 0)):,}",
            "note": "Claims that still need attention."
        },
        {
            "label": "Cancelled",
            "value": f"{int(status_counts.get('Cancelled', 0)):,}",
            "note": "Claims that did not proceed."
        }
    ]
)

status = st.selectbox(
    "Claim Status",
    ["All"] + sorted(df["Status"].dropna().unique().tolist())
)

if status != "All":
    df = df[df["Status"] == status]

def style_status(value):
    if value == "Completed":
        return "background-color: #123d2b; color: #42d392; font-weight: 800;"
    if value == "Pending":
        return "background-color: #3f3215; color: #f6c453; font-weight: 800;"
    if value == "Cancelled":
        return "background-color: #3a1720; color: #ff6b7a; font-weight: 800;"
    return ""


st.dataframe(
    df.style.map(style_status, subset=["Status"]),
    width="stretch"
)

app_footer()
