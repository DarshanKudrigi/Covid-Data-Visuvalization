"""COVID-19 Pandemic Analysis dashboard — premium redesign."""
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import streamlit as st

DATA = Path(__file__).parent / "data" / "processed"

st.set_page_config(
    page_title="COVID-19 Pandemic Analysis",
    page_icon="🦠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ═══════════════════════════════════════════════════════════════════════
# PREMIUM DARK THEME — CSS injection
# ═══════════════════════════════════════════════════════════════════════

THEME_CSS = """
<style>
/* ---- Import premium font ---- */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* ---- Root variables ---- */
:root {
    --bg-primary:    #0a0e17;
    --bg-secondary:  #111827;
    --bg-card:       #1a1f2e;
    --bg-card-hover: #1e2538;
    --border-subtle: rgba(255,255,255,0.06);
    --border-hover:  rgba(99,179,237,0.25);
    --text-primary:  #f1f5f9;
    --text-secondary:#94a3b8;
    --text-muted:    #64748b;
    --accent-blue:   #60a5fa;
    --accent-cyan:   #22d3ee;
    --accent-indigo: #818cf8;
    --accent-rose:   #fb7185;
    --accent-amber:  #fbbf24;
    --accent-emerald:#34d399;
    --gradient-blue: linear-gradient(135deg, #60a5fa 0%, #818cf8 100%);
    --gradient-card: linear-gradient(145deg, rgba(26,31,46,0.95) 0%, rgba(17,24,39,0.98) 100%);
    --shadow-card:   0 4px 24px rgba(0,0,0,0.25), 0 1px 3px rgba(0,0,0,0.15);
    --shadow-hover:  0 8px 40px rgba(0,0,0,0.35), 0 2px 8px rgba(0,0,0,0.2);
    --radius:        14px;
    --radius-sm:     10px;
    --transition:    all 0.25s cubic-bezier(0.4,0,0.2,1);
}

/* ---- Global background ---- */
html, body, [data-testid="stAppViewContainer"],
[data-testid="stApp"] {
    background: var(--bg-primary) !important;
    color: var(--text-primary) !important;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
}

/* Main content area */
.main .block-container {
    padding: 2.5rem 3rem 4rem 3rem !important;
    max-width: 1400px !important;
}

@media (max-width: 768px) {
    .main .block-container {
        padding: 1.5rem 1rem 3rem 1rem !important;
    }
}

/* ---- Scrollbar ---- */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb {
    background: rgba(148,163,184,0.2);
    border-radius: 3px;
}
::-webkit-scrollbar-thumb:hover { background: rgba(148,163,184,0.35); }

/* ═══════════════════ SIDEBAR ═══════════════════ */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f1629 0%, #0a0e17 100%) !important;
    border-right: 1px solid var(--border-subtle) !important;
}

[data-testid="stSidebar"] > div:first-child {
    padding: 2rem 1.5rem !important;
}

[data-testid="stSidebar"] .stMarkdown h2,
[data-testid="stSidebar"] [data-testid="stHeadingWithActionElements"] {
    font-size: 0.75rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    color: var(--accent-blue) !important;
    padding-bottom: 0.75rem !important;
    border-bottom: 1px solid var(--border-subtle) !important;
    margin-bottom: 1.25rem !important;
}

/* Sidebar caption */
[data-testid="stSidebar"] .stCaption,
[data-testid="stSidebar"] [data-testid="stCaptionContainer"] {
    font-size: 0.72rem !important;
    color: var(--text-muted) !important;
    line-height: 1.6 !important;
    margin-top: 1.5rem !important;
    padding-top: 1rem !important;
    border-top: 1px solid var(--border-subtle) !important;
}

/* Sidebar labels */
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stMultiSelect label,
[data-testid="stSidebar"] .stSlider label,
[data-testid="stSidebar"] label {
    font-size: 0.8rem !important;
    font-weight: 500 !important;
    color: var(--text-secondary) !important;
    letter-spacing: 0.02em !important;
}

/* ═══════════════════ MULTISELECT & INPUTS ═══════════════════ */
[data-testid="stSidebar"] [data-baseweb="select"],
[data-testid="stSidebar"] [data-baseweb="input"] {
    background: rgba(17,24,39,0.6) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: var(--radius-sm) !important;
    transition: var(--transition) !important;
}

[data-testid="stSidebar"] [data-baseweb="select"]:hover,
[data-testid="stSidebar"] [data-baseweb="input"]:hover {
    border-color: var(--border-hover) !important;
}

[data-baseweb="tag"] {
    background: rgba(96,165,250,0.15) !important;
    border: 1px solid rgba(96,165,250,0.3) !important;
    border-radius: 6px !important;
    color: var(--accent-blue) !important;
    font-weight: 500 !important;
    font-size: 0.72rem !important;
}

/* Slider */
[data-testid="stSidebar"] .stSlider [data-baseweb="slider"] [role="slider"] {
    background: var(--accent-blue) !important;
    border: 2px solid var(--bg-primary) !important;
    box-shadow: 0 0 8px rgba(96,165,250,0.4) !important;
    width: 16px !important;
    height: 16px !important;
}

[data-testid="stSidebar"] .stSlider [data-baseweb="slider"] > div > div {
    background: var(--accent-blue) !important;
}

/* ═══════════════════ HEADER / TITLE ═══════════════════ */
h1 {
    font-weight: 800 !important;
    font-size: 2rem !important;
    letter-spacing: -0.03em !important;
    background: var(--gradient-blue) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
    padding-bottom: 0.25rem !important;
    line-height: 1.2 !important;
}

/* Page subtitle / caption under title */
.main .block-container > div:first-child .stCaption,
.main .block-container > div:first-child [data-testid="stCaptionContainer"] {
    color: var(--text-muted) !important;
    font-size: 0.78rem !important;
    line-height: 1.65 !important;
    max-width: 800px !important;
}

/* Section headers */
h2, h3 {
    font-weight: 700 !important;
    letter-spacing: -0.02em !important;
    color: var(--text-primary) !important;
}

h2 { font-size: 1.35rem !important; }
h3 { font-size: 1.1rem !important; }

/* ═══════════════════ KPI METRIC CARDS ═══════════════════ */
[data-testid="stMetric"] {
    background: var(--gradient-card) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: var(--radius) !important;
    padding: 1.4rem 1.5rem !important;
    box-shadow: var(--shadow-card) !important;
    transition: var(--transition) !important;
    position: relative !important;
    overflow: hidden !important;
}

[data-testid="stMetric"]::before {
    content: '' !important;
    position: absolute !important;
    top: 0 !important;
    left: 0 !important;
    right: 0 !important;
    height: 3px !important;
    background: var(--gradient-blue) !important;
    border-radius: var(--radius) var(--radius) 0 0 !important;
}

[data-testid="stMetric"]:hover {
    border-color: var(--border-hover) !important;
    box-shadow: var(--shadow-hover) !important;
    transform: translateY(-2px) !important;
}

[data-testid="stMetric"] [data-testid="stMetricLabel"] {
    font-size: 0.72rem !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
    color: var(--text-muted) !important;
}

[data-testid="stMetric"] [data-testid="stMetricValue"] {
    font-size: 1.75rem !important;
    font-weight: 800 !important;
    color: var(--text-primary) !important;
    letter-spacing: -0.02em !important;
}

/* ═══════════════════ DIVIDERS ═══════════════════ */
hr {
    border: none !important;
    border-top: 1px solid var(--border-subtle) !important;
    margin: 2.5rem 0 !important;
}

/* ═══════════════════ TABS ═══════════════════ */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(17,24,39,0.5) !important;
    border-radius: var(--radius-sm) !important;
    padding: 4px !important;
    gap: 4px !important;
    border: 1px solid var(--border-subtle) !important;
}

.stTabs [data-baseweb="tab"] {
    border-radius: 8px !important;
    padding: 0.6rem 1.2rem !important;
    font-size: 0.8rem !important;
    font-weight: 500 !important;
    color: var(--text-muted) !important;
    background: transparent !important;
    border: none !important;
    transition: var(--transition) !important;
}

.stTabs [data-baseweb="tab"]:hover {
    color: var(--text-secondary) !important;
    background: rgba(96,165,250,0.08) !important;
}

.stTabs [aria-selected="true"] {
    background: rgba(96,165,250,0.15) !important;
    color: var(--accent-blue) !important;
    font-weight: 600 !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.15) !important;
}

/* Remove tab highlight bar */
.stTabs [data-baseweb="tab-highlight"] {
    display: none !important;
}

/* Tab border bottom */
.stTabs [data-baseweb="tab-border"] {
    display: none !important;
}

/* ═══════════════════ RADIO (map metric) ═══════════════════ */
.stRadio > label {
    font-size: 0.8rem !important;
    font-weight: 600 !important;
    color: var(--text-secondary) !important;
    margin-bottom: 0.5rem !important;
}

.stRadio [role="radiogroup"] {
    display: flex !important;
    gap: 8px !important;
    margin-top: 0.25rem !important;
}

.stRadio [data-baseweb="radio"] {
    padding: 0 !important;
}

.stRadio [role="radiogroup"] label {
    background: rgba(17,24,39,0.5) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 8px !important;
    padding: 0.5rem 1.1rem !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    color: var(--text-muted) !important;
    cursor: pointer !important;
    transition: var(--transition) !important;
}

.stRadio [role="radiogroup"] label:hover {
    border-color: var(--border-hover) !important;
    color: var(--text-secondary) !important;
}

.stRadio [role="radiogroup"] label:has(input:checked) {
    background: rgba(96,165,250,0.15) !important;
    border-color: rgba(96,165,250,0.4) !important;
    color: var(--accent-blue) !important;
    font-weight: 600 !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.15) !important;
}

/* Hide the radio circle */
.stRadio [data-baseweb="radio"] > div:first-child {
    display: none !important;
}

/* ═══════════════════ SELECT BOXES ═══════════════════ */
.main [data-baseweb="select"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: var(--radius-sm) !important;
    transition: var(--transition) !important;
}

.main [data-baseweb="select"]:hover {
    border-color: var(--border-hover) !important;
}

.main .stSelectbox label {
    font-size: 0.78rem !important;
    font-weight: 500 !important;
    color: var(--text-secondary) !important;
}

/* ═══════════════════ PLOTLY CHARTS ═══════════════════ */
[data-testid="stPlotlyChart"] {
    background: var(--gradient-card) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: var(--radius) !important;
    padding: 1rem !important;
    box-shadow: var(--shadow-card) !important;
    transition: var(--transition) !important;
    overflow: hidden !important;
}

[data-testid="stPlotlyChart"]:hover {
    border-color: var(--border-hover) !important;
    box-shadow: var(--shadow-hover) !important;
}

/* ═══════════════════ DATAFRAME / TABLE ═══════════════════ */
[data-testid="stDataFrame"],
.stDataFrame {
    background: var(--gradient-card) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: var(--radius) !important;
    overflow: hidden !important;
    box-shadow: var(--shadow-card) !important;
}

[data-testid="stDataFrame"]:hover {
    border-color: var(--border-hover) !important;
}

/* ═══════════════════ INFO BOXES ═══════════════════ */
.stAlert {
    background: rgba(96,165,250,0.08) !important;
    border: 1px solid rgba(96,165,250,0.2) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--accent-blue) !important;
    font-size: 0.82rem !important;
}

/* ═══════════════════ CAPTIONS ═══════════════════ */
.stCaption, [data-testid="stCaptionContainer"] {
    color: var(--text-muted) !important;
    font-size: 0.75rem !important;
    line-height: 1.6 !important;
}

/* ═══════════════════ BUTTONS ═══════════════════ */
.stButton > button {
    background: rgba(96,165,250,0.12) !important;
    border: 1px solid rgba(96,165,250,0.25) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--accent-blue) !important;
    font-weight: 600 !important;
    font-size: 0.82rem !important;
    padding: 0.5rem 1.25rem !important;
    transition: var(--transition) !important;
}

.stButton > button:hover {
    background: rgba(96,165,250,0.2) !important;
    border-color: var(--accent-blue) !important;
    box-shadow: 0 4px 16px rgba(96,165,250,0.2) !important;
    transform: translateY(-1px) !important;
}

.stButton > button:active {
    transform: translateY(0) !important;
}

/* ═══════════════════ DROPDOWN MENUS ═══════════════════ */
[data-baseweb="popover"],
[data-baseweb="menu"],
[data-baseweb="listbox"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: var(--radius-sm) !important;
    box-shadow: 0 12px 48px rgba(0,0,0,0.5) !important;
}

[data-baseweb="menu"] [role="option"] {
    color: var(--text-secondary) !important;
    transition: var(--transition) !important;
}

[data-baseweb="menu"] [role="option"]:hover {
    background: rgba(96,165,250,0.1) !important;
    color: var(--text-primary) !important;
}

/* ═══════════════════ FOOTER SOURCE ═══════════════════ */
.main .block-container > div:last-child .stCaption {
    text-align: center !important;
    padding-top: 1.5rem !important;
    border-top: 1px solid var(--border-subtle) !important;
}

/* ═══════════════════ HIDE STREAMLIT BRANDING ═══════════════════ */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header { visibility: hidden; }

/* ═══════════════════ RESPONSIVE ═══════════════════ */
@media (max-width: 1024px) {
    h1 { font-size: 1.6rem !important; }
    [data-testid="stMetric"] [data-testid="stMetricValue"] {
        font-size: 1.35rem !important;
    }
}

@media (max-width: 640px) {
    h1 { font-size: 1.3rem !important; }
    h2 { font-size: 1.1rem !important; }
    [data-testid="stMetric"] {
        padding: 1rem 1.1rem !important;
    }
    [data-testid="stMetric"] [data-testid="stMetricValue"] {
        font-size: 1.15rem !important;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 0.45rem 0.8rem !important;
        font-size: 0.72rem !important;
    }
}
</style>
"""
st.markdown(THEME_CSS, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════
# PLOTLY CHART TEMPLATE — consistent premium dark theme
# ═══════════════════════════════════════════════════════════════════════

_CHART_COLORS = [
    "#60a5fa",  # blue
    "#34d399",  # emerald
    "#fb7185",  # rose
    "#fbbf24",  # amber
    "#818cf8",  # indigo
    "#22d3ee",  # cyan
    "#f472b6",  # pink
    "#a78bfa",  # violet
    "#38bdf8",  # sky
    "#4ade80",  # green
]

_CHART_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(
        family="Inter, -apple-system, BlinkMacSystemFont, sans-serif",
        color="#94a3b8",
        size=12,
    ),
    title_font=dict(size=14, color="#f1f5f9"),
    xaxis=dict(
        gridcolor="rgba(255,255,255,0.04)",
        zerolinecolor="rgba(255,255,255,0.06)",
        linecolor="rgba(255,255,255,0.06)",
        tickfont=dict(size=11, color="#64748b"),
        title_font=dict(size=12, color="#94a3b8"),
    ),
    yaxis=dict(
        gridcolor="rgba(255,255,255,0.04)",
        zerolinecolor="rgba(255,255,255,0.06)",
        linecolor="rgba(255,255,255,0.06)",
        tickfont=dict(size=11, color="#64748b"),
        title_font=dict(size=12, color="#94a3b8"),
    ),
    legend=dict(
        bgcolor="rgba(0,0,0,0)",
        borderwidth=0,
        font=dict(size=11, color="#94a3b8"),
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="left",
        x=0,
    ),
    hoverlabel=dict(
        bgcolor="#1a1f2e",
        bordercolor="rgba(96,165,250,0.3)",
        font=dict(size=12, color="#f1f5f9", family="Inter, sans-serif"),
    ),
    margin=dict(l=0, r=0, t=36, b=0),
    colorway=_CHART_COLORS,
)


_PLOTLY_CONFIG = {
    "displayModeBar": "hover",
    "displaylogo": False,
    "modeBarButtonsToRemove": ["lasso2d", "select2d"],
    "responsive": True,
}


def _apply_theme(fig, height=420, hovermode=None):
    """Apply the premium dark theme to any Plotly figure."""
    layout = dict(**_CHART_LAYOUT, height=height)
    if hovermode:
        layout["hovermode"] = hovermode
    fig.update_layout(**layout)
    # Thinner, smoother lines for line charts
    fig.update_traces(
        selector=dict(type="scatter", mode="lines"),
        line=dict(width=2.5),
    )
    return fig


# ═══════════════════════════════════════════════════════════════════════
# DATA LOADING
# ═══════════════════════════════════════════════════════════════════════

@st.cache_data
def load_data():
    confirmed = pd.read_csv(DATA / "confirmed_cases.csv", parse_dates=["Date"])
    dead = pd.read_csv(DATA / "dead_cases.csv", parse_dates=["Date"])
    daily = pd.read_csv(DATA / "confirmed_cases_daily_change.csv", parse_dates=["Date"])
    since_t0 = pd.read_csv(DATA / "confirmed_cases_since_t0.csv")
    mortality = pd.read_csv(DATA / "mortality_rate.csv", parse_dates=["Date"])
    coords = pd.read_csv(DATA / "coordinates.csv")
    continents = pd.read_csv(DATA / "continents.csv")
    country_stats = pd.read_csv(DATA / "country_stats.csv")
    world_bank = pd.read_csv(DATA / "world_bank.csv")
    return confirmed, dead, daily, since_t0, mortality, coords, continents, country_stats, world_bank


confirmed, dead, daily, since_t0, mortality, coords, continents, country_stats, world_bank = load_data()

all_countries = sorted(c for c in confirmed.columns if c != "Date")
country_to_continent = continents.set_index("Country")["Continent"].to_dict()
latest_date = confirmed["Date"].max()

# ═══════════════════════════════════════════════════════════════════════
# HEADER
# ═══════════════════════════════════════════════════════════════════════

st.title("🦠 COVID-19 Pandemic Analysis")
st.caption(
    "JHU CSSE case data (Jan 2020 – Mar 2023, when JHU discontinued the feed) combined with "
    "World Bank socioeconomic indicators. Recovered-case reporting was discontinued by most "
    "countries in the underlying JHU dataset well before the feed ended, so recovered/active "
    "totals near the end of the series understate reality — treat them as directional, not exact."
)

# ═══════════════════════════════════════════════════════════════════════
# SIDEBAR FILTERS
# ═══════════════════════════════════════════════════════════════════════

st.sidebar.header("Filters")

continent_options = sorted(continents["Continent"].dropna().unique())
selected_continents = st.sidebar.multiselect("Continents", continent_options, default=continent_options)

countries_in_continents = sorted(
    c for c in all_countries if country_to_continent.get(c) in selected_continents
)

default_countries = [c for c in ["US", "India", "Brazil", "United Kingdom", "Germany"] if c in countries_in_continents]
selected_countries = st.sidebar.multiselect(
    "Countries (for trend charts)",
    countries_in_continents,
    default=default_countries or countries_in_continents[:5],
)

date_min, date_max = confirmed["Date"].min().date(), confirmed["Date"].max().date()
date_range = st.sidebar.slider(
    "Date range", min_value=date_min, max_value=date_max, value=(date_min, date_max)
)

st.sidebar.caption(f"Data current as of **{latest_date.date()}** (last JHU CSSE update).")

mask = (confirmed["Date"].dt.date >= date_range[0]) & (confirmed["Date"].dt.date <= date_range[1])

# ═══════════════════════════════════════════════════════════════════════
# KPI HEADER
# ═══════════════════════════════════════════════════════════════════════

latest_stats = country_stats[country_stats["Country"].isin(countries_in_continents)]
total_confirmed = latest_stats["Confirmed"].sum()
total_dead = latest_stats["Dead"].sum()
overall_mortality = total_dead / total_confirmed * 100 if total_confirmed else 0

k1, k2, k3, k4 = st.columns(4)
k1.metric("Confirmed Cases", f"{total_confirmed:,.0f}")
k2.metric("Deaths", f"{total_dead:,.0f}")
k3.metric("Overall Mortality Rate", f"{overall_mortality:.2f}%")
k4.metric("Countries / Regions", f"{len(countries_in_continents)}")

st.divider()

# ═══════════════════════════════════════════════════════════════════════
# CHOROPLETH MAP
# ═══════════════════════════════════════════════════════════════════════

st.subheader("Confirmed Cases by Country")
map_metric = st.radio("Map metric", ["Confirmed", "Dead", "Mortality"], horizontal=True)
map_df = country_stats.merge(coords, on="Country").merge(continents, on="Country")
map_df = map_df[map_df["Continent"].isin(selected_continents)]

# Custom sequential color scale for the dark theme
_map_scale = (
    [[0, "#0f1629"], [0.2, "#1e3a5f"], [0.4, "#3b6cb5"], [0.6, "#60a5fa"], [0.8, "#fb7185"], [1, "#fbbf24"]]
    if map_metric != "Mortality"
    else [[0, "#0f1629"], [0.25, "#3b2042"], [0.5, "#7c3053"], [0.75, "#c44569"], [1, "#fb7185"]]
)

fig_map = px.choropleth(
    map_df,
    locations="Country Code",
    color=map_metric,
    hover_name="Country",
    hover_data={"Confirmed": ":,", "Dead": ":,", "Mortality": ":.2f", "Country Code": False},
    color_continuous_scale=_map_scale,
    labels={"Mortality": "Mortality %"},
)
fig_map.update_layout(
    height=500,
    margin=dict(l=0, r=0, t=10, b=0),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    geo=dict(
        bgcolor="rgba(0,0,0,0)",
        lakecolor="rgba(0,0,0,0)",
        landcolor="#141b2d",
        showframe=False,
        showcoastlines=True,
        coastlinecolor="rgba(255,255,255,0.08)",
        countrycolor="rgba(255,255,255,0.06)",
        showocean=True,
        oceancolor="#0a0e17",
        projection_type="natural earth",
    ),
    coloraxis_colorbar=dict(
        bgcolor="rgba(0,0,0,0)",
        tickfont=dict(color="#64748b", size=11),
        title_font=dict(color="#94a3b8", size=12),
        outlinewidth=0,
        thickness=12,
        len=0.6,
    ),
    hoverlabel=dict(
        bgcolor="#1a1f2e",
        bordercolor="rgba(96,165,250,0.3)",
        font=dict(size=12, color="#f1f5f9", family="Inter, sans-serif"),
    ),
)
st.plotly_chart(fig_map, width="stretch", config=_PLOTLY_CONFIG)

st.divider()

# ═══════════════════════════════════════════════════════════════════════
# CASE TRENDS
# ═══════════════════════════════════════════════════════════════════════

st.subheader("Case Trends Over Time")
tab1, tab2, tab3 = st.tabs(["Cumulative Confirmed", "Daily New Cases", "Mortality Rate"])

with tab1:
    if selected_countries:
        long = confirmed.loc[mask, ["Date"] + selected_countries].melt("Date", var_name="Country", value_name="Confirmed")
        fig = px.line(long, x="Date", y="Confirmed", color="Country")
        _apply_theme(fig, height=440, hovermode="x unified")
        st.plotly_chart(fig, width="stretch", config=_PLOTLY_CONFIG)
    else:
        st.info("Select at least one country in the sidebar.")

with tab2:
    if selected_countries:
        long = daily.loc[mask, ["Date"] + selected_countries].melt("Date", var_name="Country", value_name="New cases")
        long["New cases"] = long["New cases"].clip(lower=0)
        fig = px.line(long, x="Date", y="New cases", color="Country")
        _apply_theme(fig, height=440, hovermode="x unified")
        st.plotly_chart(fig, width="stretch", config=_PLOTLY_CONFIG)
    else:
        st.info("Select at least one country in the sidebar.")

with tab3:
    if selected_countries:
        long = mortality.loc[mortality["Date"].dt.date.between(*date_range), ["Date"] + [c for c in selected_countries if c in mortality.columns]]
        long = long.melt("Date", var_name="Country", value_name="Mortality %")
        fig = px.line(long, x="Date", y="Mortality %", color="Country")
        _apply_theme(fig, height=440, hovermode="x unified")
        st.plotly_chart(fig, width="stretch", config=_PLOTLY_CONFIG)
    else:
        st.info("Select at least one country in the sidebar.")

st.divider()

# ═══════════════════════════════════════════════════════════════════════
# GROWTH TRAJECTORIES
# ═══════════════════════════════════════════════════════════════════════

st.subheader("Growth Trajectories Since the 100th Confirmed Case")
st.caption("Aligns every country to day 0 = the day it recorded its 100th confirmed case, for a fair speed-of-spread comparison.")
t0_cols = [c for c in selected_countries if c in since_t0.columns]
if t0_cols:
    long = since_t0[t0_cols].reset_index().melt("index", var_name="Country", value_name="Confirmed")
    long = long.rename(columns={"index": "Days since 100th case"}).dropna()
    fig = px.line(long, x="Days since 100th case", y="Confirmed", color="Country", log_y=True)
    _apply_theme(fig, height=440, hovermode="x unified")
    st.plotly_chart(fig, width="stretch", config=_PLOTLY_CONFIG)
else:
    st.info("Select at least one country in the sidebar.")

st.divider()

# ═══════════════════════════════════════════════════════════════════════
# SOCIOECONOMIC SCATTER
# ═══════════════════════════════════════════════════════════════════════

st.subheader("Socioeconomic Correlations")
st.caption("Each point is a country with more than 5,000 confirmed cases. Bubble size = population.")

c1, c2 = st.columns(2)
x_axis = c1.selectbox(
    "X axis", ["GDP per capita", "Life expectancy", "Rural population %", "GDP Healthcare %"]
)
y_axis = c2.selectbox("Y axis", ["Cases per mln", "Dead per mln", "Mortality %"])

wb_df = world_bank[world_bank["Continent"].isin(selected_continents)]
wb_df = wb_df.dropna(subset=["Population", x_axis, y_axis])
if wb_df.empty:
    st.info("Select at least one continent in the sidebar.")
else:
    fig_scatter = px.scatter(
        wb_df,
        x=x_axis,
        y=y_axis,
        color="Continent",
        size="Population",
        hover_name="Country",
        size_max=50,
        trendline="ols",
        trendline_scope="overall",
    )
    _apply_theme(fig_scatter, height=500)
    # Make scatter points slightly transparent for depth
    fig_scatter.update_traces(
        selector=dict(type="scatter", mode="markers"),
        marker=dict(opacity=0.85, line=dict(width=1, color="rgba(0,0,0,0.3)")),
    )
    # Style trendline
    fig_scatter.update_traces(
        selector=dict(mode="lines"),
        line=dict(dash="dot", width=2, color="rgba(148,163,184,0.5)"),
    )
    st.plotly_chart(fig_scatter, width="stretch", config=_PLOTLY_CONFIG)

st.divider()

# ═══════════════════════════════════════════════════════════════════════
# COUNTRY LEADERBOARD
# ═══════════════════════════════════════════════════════════════════════

st.subheader("Country Leaderboard")
board = country_stats.merge(continents, on="Country")
board = board[board["Continent"].isin(selected_continents)]
board = board.sort_values("Confirmed", ascending=False).reset_index(drop=True)
board.index += 1

# Format numbers for better readability
display_board = board[["Country", "Continent", "Confirmed", "Dead", "Mortality"]].rename(
    columns={"Mortality": "Mortality %"}
)

st.dataframe(
    display_board,
    width="stretch",
    height=420,
    column_config={
        "Country": st.column_config.TextColumn("Country", width="medium"),
        "Continent": st.column_config.TextColumn("Continent", width="small"),
        "Confirmed": st.column_config.NumberColumn("Confirmed", format="%d"),
        "Dead": st.column_config.NumberColumn("Deaths", format="%d"),
        "Mortality %": st.column_config.NumberColumn("Mortality %", format="%.2f%%"),
    },
)

st.caption("Source: [JHU CSSE COVID-19 Data](https://github.com/CSSEGISandData/COVID-19) · [World Bank Open Data](https://data.worldbank.org/)")
