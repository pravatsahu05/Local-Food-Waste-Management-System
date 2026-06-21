import sys
from pathlib import Path

import pandas as pd
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from database.db_connection import get_connection


def fetch_data(query, params=None):
    conn = get_connection()

    try:
        df = pd.read_sql(query, conn, params=params)
    finally:
        conn.close()

    return df


def load_theme():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

        :root {
            --bg: #070b12;
            --panel: #101722;
            --panel-2: #141e2c;
            --text: #edf6f9;
            --muted: #9fb2c7;
            --green: #42d392;
            --cyan: #37c6ff;
            --amber: #f6c453;
            --danger: #ff6b7a;
            --border: rgba(255, 255, 255, 0.11);
        }

        html, body, [data-testid="stAppViewContainer"] {
            background:
                radial-gradient(circle at 12% 12%, rgba(66, 211, 146, 0.16), transparent 28rem),
                radial-gradient(circle at 88% 4%, rgba(55, 198, 255, 0.13), transparent 24rem),
                linear-gradient(135deg, #070b12 0%, #0b111b 46%, #090d14 100%);
            color: var(--text);
            font-family: 'Inter', sans-serif;
        }

        [data-testid="stHeader"] {
            background: rgba(7, 11, 18, 0.72);
            backdrop-filter: blur(16px);
        }

        .block-container {
            padding-top: 2.3rem;
            padding-bottom: 3rem;
            max-width: 1180px;
        }

        h1, h2, h3, h4 {
            color: var(--text);
            letter-spacing: 0;
        }

        p, label, span, div {
            font-family: 'Inter', sans-serif;
        }

        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0b111b 0%, #081019 100%);
            border-right: 1px solid var(--border);
            min-width: 300px;
        }

        [data-testid="stSidebar"] * {
            color: var(--text);
        }

        [data-testid="stSidebarNav"] {
            padding-top: 1rem;
        }

        .app-hero {
            min-height: 330px;
            padding: 3rem 2.5rem;
            border: 1px solid var(--border);
            border-radius: 18px;
            background:
                linear-gradient(90deg, rgba(7, 11, 18, 0.88) 0%, rgba(7, 11, 18, 0.62) 48%, rgba(7, 11, 18, 0.16) 100%),
                url('https://images.unsplash.com/photo-1488521787991-ed7bbaae773c?auto=format&fit=crop&w=1600&q=80');
            background-size: cover;
            background-position: center;
            box-shadow: 0 24px 70px rgba(0, 0, 0, 0.38);
            display: flex;
            align-items: center;
        }

        .app-hero h1 {
            font-size: clamp(2.25rem, 5vw, 4.8rem);
            line-height: 1;
            margin: 0 0 1rem 0;
            max-width: 760px;
        }

        .app-hero p {
            color: var(--muted);
            font-size: 1.06rem;
            line-height: 1.7;
            max-width: 660px;
            margin: 0;
        }

        .eyebrow {
            color: var(--green);
            font-weight: 800;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            font-size: 0.78rem;
            margin-bottom: 1rem;
        }

        .page-header {
            padding: 1.25rem 0 0.75rem 0;
            border-bottom: 1px solid var(--border);
            margin-bottom: 1.4rem;
        }

        .page-header h1 {
            margin: 0;
            font-size: 2.2rem;
        }

        .page-header p {
            margin: 0.45rem 0 0 0;
            color: var(--muted);
            font-size: 1rem;
        }

        [data-testid="stMetric"] {
            background: linear-gradient(145deg, rgba(20, 30, 44, 0.96), rgba(12, 18, 28, 0.96));
            border: 1px solid var(--border);
            border-radius: 14px;
            padding: 1rem;
            box-shadow: 0 14px 36px rgba(0, 0, 0, 0.28);
            transition: transform 180ms ease, border-color 180ms ease, box-shadow 180ms ease;
        }

        [data-testid="stMetric"]:hover {
            transform: translateY(-3px);
            border-color: rgba(66, 211, 146, 0.42);
            box-shadow: 0 20px 52px rgba(0, 0, 0, 0.36);
        }

        [data-testid="stMetricLabel"] p {
            color: var(--muted);
            font-weight: 700;
        }

        [data-testid="stMetricValue"] {
            color: var(--green);
        }

        div[data-testid="stDataFrame"],
        div[data-testid="stTable"],
        div[data-testid="stPlotlyChart"] {
            border: 1px solid var(--border);
            border-radius: 14px;
            overflow: hidden;
            background: rgba(16, 23, 34, 0.9);
            box-shadow: 0 16px 44px rgba(0, 0, 0, 0.26);
        }

        .stTabs [data-baseweb="tab-list"] {
            gap: 0.5rem;
            border-bottom: 1px solid var(--border);
        }

        .stTabs [data-baseweb="tab"] {
            background: rgba(16, 23, 34, 0.9);
            border: 1px solid var(--border);
            border-bottom: 0;
            border-radius: 10px 10px 0 0;
            color: var(--muted);
            font-weight: 700;
        }

        .stTabs [aria-selected="true"] {
            color: var(--green);
            background: rgba(66, 211, 146, 0.11);
        }

        .stTextInput input,
        .stNumberInput input,
        [data-baseweb="select"] > div,
        textarea {
            background: #0d1520;
            border: 1px solid var(--border);
            color: var(--text);
            border-radius: 10px;
        }

        .stButton button,
        .stDownloadButton button {
            background: linear-gradient(135deg, var(--green), var(--cyan));
            color: #04100b;
            border: 0;
            border-radius: 10px;
            font-weight: 800;
            box-shadow: 0 12px 30px rgba(66, 211, 146, 0.23);
        }

        .stAlert {
            background: rgba(20, 30, 44, 0.95);
            border: 1px solid var(--border);
            border-radius: 12px;
        }

        .feature-grid {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 1rem;
            margin-top: 1rem;
        }

        .feature-card {
            background: rgba(16, 23, 34, 0.82);
            border: 1px solid var(--border);
            border-radius: 14px;
            padding: 1rem;
            transition: transform 180ms ease, border-color 180ms ease, background 180ms ease;
        }

        .feature-card:hover {
            transform: translateY(-4px);
            border-color: rgba(55, 198, 255, 0.42);
            background: rgba(20, 30, 44, 0.94);
        }

        .feature-card strong {
            display: block;
            color: var(--text);
            margin-bottom: 0.35rem;
        }

        .feature-card span {
            color: var(--muted);
            font-size: 0.92rem;
            line-height: 1.5;
        }

        .insight-grid {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 1rem;
            margin: 1.1rem 0 1.4rem 0;
        }

        .insight-card {
            position: relative;
            overflow: hidden;
            min-height: 126px;
            background: linear-gradient(145deg, rgba(20, 30, 44, 0.96), rgba(9, 16, 26, 0.96));
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 1rem;
            box-shadow: 0 18px 48px rgba(0, 0, 0, 0.27);
            transition: transform 180ms ease, border-color 180ms ease;
        }

        .insight-card:hover {
            transform: translateY(-4px);
            border-color: rgba(66, 211, 146, 0.45);
        }

        .insight-card::after {
            content: "";
            position: absolute;
            right: -42px;
            top: -42px;
            width: 110px;
            height: 110px;
            border-radius: 50%;
            background: rgba(66, 211, 146, 0.14);
        }

        .insight-label {
            color: var(--muted);
            font-size: 0.75rem;
            font-weight: 800;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            margin-bottom: 0.6rem;
        }

        .insight-value {
            color: var(--text);
            font-size: 1.85rem;
            font-weight: 850;
            line-height: 1.05;
            margin-bottom: 0.4rem;
        }

        .insight-note {
            color: var(--muted);
            font-size: 0.88rem;
            line-height: 1.45;
        }

        .priority-list {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 1rem;
            margin: 1rem 0 1.4rem 0;
        }

        .priority-card {
            background: linear-gradient(145deg, rgba(246, 196, 83, 0.12), rgba(20, 30, 44, 0.9));
            border: 1px solid rgba(246, 196, 83, 0.3);
            border-radius: 16px;
            padding: 1rem;
        }

        .priority-card strong {
            display: block;
            color: var(--text);
            font-size: 1rem;
            margin-bottom: 0.45rem;
        }

        .priority-card span {
            display: block;
            color: var(--muted);
            font-size: 0.88rem;
            line-height: 1.45;
        }

        .app-footer {
            margin-top: 2rem;
            padding: 1rem;
            border: 1px solid var(--border);
            border-radius: 14px;
            background: rgba(16, 23, 34, 0.72);
            color: var(--muted);
            text-align: center;
            font-size: 0.9rem;
        }

        @media (max-width: 800px) {
            .app-hero {
                min-height: 420px;
                padding: 2rem 1.25rem;
                align-items: flex-end;
            }

            .feature-grid {
                grid-template-columns: 1fr;
            }

            .insight-grid,
            .priority-list {
                grid-template-columns: 1fr;
            }
        }
        </style>
        """,
        unsafe_allow_html=True
    )


def page_header(icon, title, subtitle):
    st.markdown(
        f"""
        <div class="page-header">
            <div class="eyebrow">{icon} Local Food Waste Management</div>
            <h1>{title}</h1>
            <p>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True
    )


def chart_theme(fig):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#edf6f9", family="Inter"),
        title=dict(font=dict(size=20, color="#edf6f9")),
        legend=dict(bgcolor="rgba(0,0,0,0)"),
        margin=dict(l=20, r=20, t=58, b=20)
    )
    return fig


def component_styles():
    return """
    <style>
    body {
        margin: 0;
        background: transparent;
        color: #edf6f9;
        font-family: Inter, Arial, sans-serif;
    }

    .insight-grid {
        display: grid;
        grid-template-columns: repeat(4, minmax(0, 1fr));
        gap: 1rem;
    }

    .insight-card {
        position: relative;
        overflow: hidden;
        min-height: 112px;
        background: linear-gradient(145deg, rgba(20, 30, 44, 0.96), rgba(9, 16, 26, 0.96));
        border: 1px solid rgba(255, 255, 255, 0.11);
        border-radius: 16px;
        padding: 1rem;
        box-shadow: 0 18px 48px rgba(0, 0, 0, 0.27);
        transition: transform 180ms ease, border-color 180ms ease;
    }

    .insight-card:hover {
        transform: translateY(-4px);
        border-color: rgba(66, 211, 146, 0.45);
    }

    .insight-card::after {
        content: "";
        position: absolute;
        right: -42px;
        top: -42px;
        width: 110px;
        height: 110px;
        border-radius: 50%;
        background: rgba(66, 211, 146, 0.14);
    }

    .insight-label {
        color: #9fb2c7;
        font-size: 0.75rem;
        font-weight: 800;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin-bottom: 0.6rem;
    }

    .insight-value {
        color: #edf6f9;
        font-size: 1.75rem;
        font-weight: 850;
        line-height: 1.05;
        margin-bottom: 0.4rem;
    }

    .insight-note {
        color: #9fb2c7;
        font-size: 0.88rem;
        line-height: 1.45;
    }

    .priority-list {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 1rem;
    }

    .priority-card {
        background: linear-gradient(145deg, rgba(246, 196, 83, 0.12), rgba(20, 30, 44, 0.9));
        border: 1px solid rgba(246, 196, 83, 0.3);
        border-radius: 16px;
        padding: 1rem;
    }

    .priority-card strong {
        display: block;
        color: #edf6f9;
        font-size: 1rem;
        margin-bottom: 0.45rem;
    }

    .priority-card span {
        display: block;
        color: #9fb2c7;
        font-size: 0.88rem;
        line-height: 1.45;
    }

    .app-footer {
        padding: 1rem;
        border: 1px solid rgba(255, 255, 255, 0.11);
        border-radius: 14px;
        background: rgba(16, 23, 34, 0.72);
        color: #9fb2c7;
        text-align: center;
        font-size: 0.9rem;
    }

    @media (max-width: 800px) {
        .insight-grid,
        .priority-list {
            grid-template-columns: 1fr;
        }
    }
    </style>
    """


def insight_cards(cards):
    items = []

    for card in cards:
        items.append(
            f"""
            <div class="insight-card">
                <div class="insight-label">{card["label"]}</div>
                <div class="insight-value">{card["value"]}</div>
                <div class="insight-note">{card["note"]}</div>
            </div>
            """
        )

    st.markdown(
        f"""
        <div class="insight-grid">
            {''.join(items)}
        </div>
        """,
        unsafe_allow_html=True
    )


def priority_food_cards(df):
    if df.empty:
        st.info("No urgent expiring food found.")
        return

    cards = []

    for row in df.head(3).itertuples(index=False):
        cards.append(
            f"""
            <div class="priority-card">
                <strong>{row.Food_Name}</strong>
                <span>Quantity: {int(row.Quantity)} | Expires: {row.Expiry_Date}</span>
                <span>{row.Location} | {row.Provider_Type} | {row.Meal_Type}</span>
            </div>
            """
        )

    st.markdown(
        f"""
        <div class="priority-list">
            {''.join(cards)}
        </div>
        """,
        unsafe_allow_html=True
    )


def app_footer():
    st.markdown(
        """
        <div class="app-footer">
            Built for food redistribution, waste reduction, and community impact.
        </div>
        """,
        unsafe_allow_html=True
    )
