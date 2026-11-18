"""COVID-19 Pandemic Analysis dashboard."""
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

DATA = Path(__file__).parent / "data" / "processed"

st.set_page_config(page_title="COVID-19 Pandemic Analysis", page_icon="🦠", layout="wide")


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

st.title("🦠 COVID-19 Pandemic Analysis")
st.caption(
    "JHU CSSE case data (Jan 2020 – Mar 2023, when JHU discontinued the feed) combined with "
    "World Bank socioeconomic indicators. Recovered-case reporting was discontinued by most "
    "countries in the underlying JHU dataset well before the feed ended, so recovered/active "
    "totals near the end of the series understate reality — treat them as directional, not exact."
)

# ---------------------------------------------------------------- sidebar --
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

# ------------------------------------------------------------- KPI header --
latest_stats = country_stats[country_stats["Country"].isin(countries_in_continents)]
total_confirmed = latest_stats["Confirmed"].sum()
total_dead = latest_stats["Dead"].sum()
overall_mortality = total_dead / total_confirmed * 100 if total_confirmed else 0

k1, k2, k3, k4 = st.columns(4)
k1.metric("Confirmed cases", f"{total_confirmed:,.0f}")
k2.metric("Deaths", f"{total_dead:,.0f}")
k3.metric("Overall mortality rate", f"{overall_mortality:.2f}%")
k4.metric("Countries/regions tracked", f"{len(countries_in_continents)}")

st.divider()

# ------------------------------------------------------------------- map --
st.subheader("Confirmed cases by country")
map_metric = st.radio("Map metric", ["Confirmed", "Dead", "Mortality"], horizontal=True)
map_df = country_stats.merge(coords, on="Country").merge(continents, on="Country")
map_df = map_df[map_df["Continent"].isin(selected_continents)]

fig_map = px.choropleth(
    map_df,
    locations="Country Code",
    color=map_metric,
    hover_name="Country",
    hover_data={"Confirmed": ":,", "Dead": ":,", "Mortality": ":.2f", "Country Code": False},
    color_continuous_scale="OrRd" if map_metric != "Mortality" else "Reds",
    labels={"Mortality": "Mortality %"},
)
fig_map.update_layout(margin=dict(l=0, r=0, t=10, b=0), height=480)
st.plotly_chart(fig_map, width="stretch")

st.divider()

# --------------------------------------------------------------- trends --
st.subheader("Case trends over time")
tab1, tab2, tab3 = st.tabs(["Cumulative confirmed", "Daily new cases", "Mortality rate"])

with tab1:
    if selected_countries:
        long = confirmed.loc[mask, ["Date"] + selected_countries].melt("Date", var_name="Country", value_name="Confirmed")
        fig = px.line(long, x="Date", y="Confirmed", color="Country")
        fig.update_layout(height=420, margin=dict(l=0, r=0, t=10, b=0))
        st.plotly_chart(fig, width="stretch")
    else:
        st.info("Select at least one country in the sidebar.")

with tab2:
    if selected_countries:
        long = daily.loc[mask, ["Date"] + selected_countries].melt("Date", var_name="Country", value_name="New cases")
        long["New cases"] = long["New cases"].clip(lower=0)
        fig = px.line(long, x="Date", y="New cases", color="Country")
        fig.update_layout(height=420, margin=dict(l=0, r=0, t=10, b=0))
        st.plotly_chart(fig, width="stretch")
    else:
        st.info("Select at least one country in the sidebar.")

with tab3:
    if selected_countries:
        long = mortality.loc[mortality["Date"].dt.date.between(*date_range), ["Date"] + [c for c in selected_countries if c in mortality.columns]]
        long = long.melt("Date", var_name="Country", value_name="Mortality %")
        fig = px.line(long, x="Date", y="Mortality %", color="Country")
        fig.update_layout(height=420, margin=dict(l=0, r=0, t=10, b=0))
        st.plotly_chart(fig, width="stretch")
    else:
        st.info("Select at least one country in the sidebar.")

st.divider()

# ------------------------------------------------------- days-since-t0 --
st.subheader("Growth trajectories since the 100th confirmed case")
st.caption("Aligns every country to day 0 = the day it recorded its 100th confirmed case, for a fair speed-of-spread comparison.")
t0_cols = [c for c in selected_countries if c in since_t0.columns]
if t0_cols:
    long = since_t0[t0_cols].reset_index().melt("index", var_name="Country", value_name="Confirmed")
    long = long.rename(columns={"index": "Days since 100th case"}).dropna()
    fig = px.line(long, x="Days since 100th case", y="Confirmed", color="Country", log_y=True)
    fig.update_layout(height=420, margin=dict(l=0, r=0, t=10, b=0))
    st.plotly_chart(fig, width="stretch")
else:
    st.info("Select at least one country in the sidebar.")

st.divider()

# ------------------------------------------------------ socioeconomic --
st.subheader("Socioeconomic correlations")
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
    fig_scatter.update_layout(height=480, margin=dict(l=0, r=0, t=10, b=0))
    st.plotly_chart(fig_scatter, width="stretch")

st.divider()

# ----------------------------------------------------------- leaderboard --
st.subheader("Country leaderboard")
board = country_stats.merge(continents, on="Country")
board = board[board["Continent"].isin(selected_continents)]
board = board.sort_values("Confirmed", ascending=False).reset_index(drop=True)
board.index += 1
st.dataframe(
    board[["Country", "Continent", "Confirmed", "Dead", "Mortality"]].rename(columns={"Mortality": "Mortality %"}),
    width="stretch",
    height=400,
)

st.caption("Source: [JHU CSSE COVID-19 Data](https://github.com/CSSEGISandData/COVID-19) · [World Bank Open Data](https://data.worldbank.org/)")
