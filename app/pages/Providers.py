import streamlit as st

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.utils import fetch_data, load_theme, page_header

load_theme()

page_header(
    "Directory",
    "Providers & Receivers",
    "Directory and contact details for donation coordination."
)

tab1, tab2, tab3 = st.tabs(
    [
        "Provider Directory",
        "Provider Contacts",
        "Receiver Contacts"
    ]
)

with tab1:
    query = """
    SELECT Provider_ID,
           Name,
           Type,
           City,
           Contact
    FROM providers
    """

    df = fetch_data(query)

    city_options = ["All"] + sorted(df["City"].dropna().unique().tolist())

    city = st.selectbox(
        "Filter City",
        city_options
    )

    if city != "All":
        df = df[df["City"] == city]

    st.dataframe(df, width="stretch")

with tab2:
    search_city = st.text_input(
        "Enter City",
        key="provider_city_search"
    )

    contact_query = """
    SELECT Name,
           Type,
           City,
           Contact
    FROM providers
    WHERE City LIKE %s
    """

    contact_df = fetch_data(
        contact_query,
        params=(f"%{search_city}%",)
    )

    st.dataframe(contact_df, width="stretch")

with tab3:
    search_city_r = st.text_input(
        "Enter City",
        key="receiver_city_search"
    )

    receiver_query = """
    SELECT Name,
           Type,
           City,
           Contact
    FROM receivers
    WHERE City LIKE %s
    """

    receiver_df = fetch_data(
        receiver_query,
        params=(f"%{search_city_r}%",)
    )

    st.dataframe(receiver_df, width="stretch")
