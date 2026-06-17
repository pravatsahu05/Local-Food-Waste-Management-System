import streamlit as st

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.utils import load_theme, page_header
from sql_queries.queries import QUERIES, run_query

load_theme()

page_header(
    "SQL",
    "SQL Analysis",
    "Run curated business queries and download the result as a CSV."
)

selected_query = st.selectbox(
    "Select Query",
    list(QUERIES.keys())
)

result = run_query(
    QUERIES[selected_query]
)

st.dataframe(
    result,
    width="stretch"
)

csv = result.to_csv(index=False)

st.download_button(
    "Download Result",
    csv,
    file_name="query_result.csv",
    mime="text/csv"
)
