#!/usr/bin/env python3
"""Step 4 (Streamlit): Comprehensive Interactive Decision Dashboard for EcoMove Mobility.

Launch command:
    .venv/bin/streamlit run "COM7021 - Assignment/scripts/04_streamlit_dashboard.py"

Designed for COM7021 Data Visualisation (Student ID: 25199053, Arden University Berlin).
Implements the locked Arden University palette (#002B49 Midnight, #66C9BA Tiffany, #3AA89A Tiffany Deep),
1-click executive scenario presets (including Figure 9 Baseline and Figure 10 Adverse Weather Surface
Scenario), 6 cascading sidebar filters, a 6-card Executive KPI strip with dual-basis cost recovery
reconciliation, and 5 structured analytical decision tabs covering Figures 1 to 10.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from style.palette import (
    GRID,
    LINE,
    MIDNIGHT,
    MIDNIGHT_SOFT,
    MIST,
    MUTE,
    PAPER,
    TEAL,
    TIFFANY,
    TIFFANY_DEEP,
    WHITE,
)

SLATE = MUTE

DATA_CSV = BASE_DIR / "data" / "ecomove_cleaned.csv"

MODE_ORDER = ["Metro", "Tram", "Bus", "Park and Ride", "Bike Share", "E-Scooter"]
WEATHER_ORDER = ["Clear", "Cloudy", "Windy", "Heatwave", "Rain", "Snow"]
ROUTE_ORDER = [
    "Suburban Feeder",
    "Commuter Corridor",
    "University Area",
    "Airport Connector",
    "Central Route",
    "Tourist Zone",
]

SCENARIO_PRESETS = {
    "1. Full Network Baseline (Figure 9 — N = 5,000)": {
        "desc": "Default unfiltered view across all 12 European cities, 6 modes, and 6 weather conditions (2024–2025).",
        "countries": [],
        "cities": [],
        "modes": [],
        "routes": [],
        "weathers": [],
        "event_day": "All",
        "day_regime": "All Days",
    },
    "2. Adverse Weather Surface Transit (Figure 10 — n = 583)": {
        "desc": "Executive stress-test isolating surface modes (Bus, Tram, Park & Ride) under Rain and Snow conditions.",
        "countries": [],
        "cities": [],
        "modes": ["Bus", "Tram", "Park and Ride"],
        "routes": [],
        "weathers": ["Rain", "Snow"],
        "event_day": "All",
        "day_regime": "All Days",
    },
    "3. Shared Micromobility Subsidy Audit (n = 1,232)": {
        "desc": "Isolates Bike Share and E-Scooter operations to audit per-trip deficits (-€19.98 to -€20.84/pax) and complaint intensity.",
        "countries": [],
        "cities": [],
        "modes": ["Bike Share", "E-Scooter"],
        "routes": [],
        "weathers": [],
        "event_day": "All",
        "day_regime": "All Days",
    },
    "4. Major Event Day Surge & Delay Pressure (n = 510)": {
        "desc": "Isolates Major Event Days (Event_Day = Yes), showing +26.2% ridership surge and +31.0% delay escalation.",
        "countries": [],
        "cities": [],
        "modes": [],
        "routes": [],
        "weathers": [],
        "event_day": "Yes",
        "day_regime": "All Days",
    },
    "5. Suburban Feeder Accessibility Audit (n = 817)": {
        "desc": "Isolates Suburban Feeder corridors, which record the highest normalised accessibility complaint rate (16.79 / 10k pax).",
        "countries": [],
        "cities": [],
        "modes": [],
        "routes": ["Suburban Feeder"],
        "weathers": [],
        "event_day": "All",
        "day_regime": "All Days",
    },
    "6. High-Capacity Electric Rail Backbone (n = 1,683)": {
        "desc": "Isolates grade-separated Metro and electrified Tram corridors driving 81.2% of total ridership and 78.6% of CO2 savings.",
        "countries": [],
        "cities": [],
        "modes": ["Metro", "Tram"],
        "routes": [],
        "weathers": [],
        "event_day": "All",
        "day_regime": "All Days",
    },
}


# ==============================================================================
# DATA LOADING & CACHED COMPUTATIONS
# ==============================================================================
@st.cache_data(show_spinner=False)
def load_dataset() -> pd.DataFrame:
    df = pd.read_csv(DATA_CSV, parse_dates=["Date_ISO"])
    df["Date_Only"] = df["Date_ISO"].dt.date
    if "DayOfWeek" not in df.columns:
        if "Day_of_Week" in df.columns:
            df["DayOfWeek"] = df["Day_of_Week"]
        else:
            df["DayOfWeek"] = df["Date_ISO"].dt.day_name()
    if "Day_Type" not in df.columns:
        if "Is_Weekend" in df.columns:
            df["Day_Type"] = np.where(df["Is_Weekend"].astype(bool), "Weekend", "Weekday")
        else:
            df["Day_Type"] = np.where(df["Date_ISO"].dt.dayofweek >= 5, "Weekend", "Weekday")
    return df


def compute_metrics(df_sub: pd.DataFrame, df_base: pd.DataFrame) -> dict[str, float]:
    """Compute comprehensive volume-weighted and record-mean metrics with baseline deltas."""
    n_rec = len(df_sub)
    base_n = len(df_base)
    if n_rec == 0:
        return {"n_rec": 0}

    total_pax = float(df_sub["Passengers"].sum())
    base_pax = float(df_base["Passengers"].sum())
    mean_pax = float(df_sub["Passengers"].mean())
    median_pax = float(df_sub["Passengers"].median())
    base_mean_pax = float(df_base["Passengers"].mean())

    mean_ontime = float(df_sub["On_Time_Percentage"].mean())
    base_ontime = float(df_base["On_Time_Percentage"].mean())

    mean_delay = float(df_sub["Average_Delay_Minutes"].mean())
    median_delay = float(df_sub["Average_Delay_Minutes"].median())
    iqr_delay = float(df_sub["Average_Delay_Minutes"].quantile(0.75) - df_sub["Average_Delay_Minutes"].quantile(0.25))
    base_delay = float(df_base["Average_Delay_Minutes"].mean())

    total_rev = float(df_sub["Ticket_Revenue_EUR"].sum())
    total_cost = float(df_sub["Operating_Cost_EUR"].sum())
    net_margin = total_rev - total_cost
    mean_rev_rec = total_rev / n_rec
    mean_cost_rec = total_cost / n_rec
    mean_margin_rec = net_margin / n_rec

    fare_per_pax = (total_rev / total_pax) if total_pax > 0 else 0.0
    cost_per_pax = (total_cost / total_pax) if total_pax > 0 else 0.0
    margin_per_pax = fare_per_pax - cost_per_pax

    overall_recovery = (total_rev / total_cost * 100.0) if total_cost > 0 else 0.0
    base_overall_recovery = float(df_base["Ticket_Revenue_EUR"].sum() / df_base["Operating_Cost_EUR"].sum() * 100.0)

    record_mean_recovery = float(df_sub["Cost_Recovery_Pct"].mean())
    record_median_recovery = float(df_sub["Cost_Recovery_Pct"].median())
    base_record_mean_recovery = float(df_base["Cost_Recovery_Pct"].mean())

    total_co2_t = float(df_sub["CO2_Saved_KG"].sum() / 1000.0)
    total_kwh = float(df_sub["Energy_Consumption_KWh"].sum())
    agg_co2_kwh = float(df_sub["CO2_Saved_KG"].sum() / total_kwh) if total_kwh > 0 else 0.0
    base_co2_kwh = float(df_base["CO2_Saved_KG"].sum() / df_base["Energy_Consumption_KWh"].sum())

    mean_rating = float(df_sub["Customer_Rating"].mean())
    base_rating = float(df_base["Customer_Rating"].mean())

    total_comp = int(df_sub["Accessibility_Complaints"].sum())
    weighted_comp_10k = (total_comp / total_pax * 10000.0) if total_pax > 0 else 0.0
    record_mean_comp_10k = float(df_sub["Complaints_per_10k_Pax"].mean())
    base_comp_10k = float(df_base["Accessibility_Complaints"].sum() / base_pax * 10000.0)

    return {
        "n_rec": n_rec,
        "rec_share_pct": n_rec / base_n * 100.0,
        "total_pax": total_pax,
        "pax_share_pct": total_pax / base_pax * 100.0,
        "mean_pax": mean_pax,
        "median_pax": median_pax,
        "delta_pax_pct": (mean_pax - base_mean_pax) / base_mean_pax * 100.0,
        "mean_ontime": mean_ontime,
        "delta_ontime_pp": mean_ontime - base_ontime,
        "mean_delay": mean_delay,
        "median_delay": median_delay,
        "iqr_delay": iqr_delay,
        "delta_delay_min": mean_delay - base_delay,
        "delta_delay_pct": (mean_delay - base_delay) / base_delay * 100.0,
        "total_rev": total_rev,
        "total_cost": total_cost,
        "net_margin": net_margin,
        "mean_rev_rec": mean_rev_rec,
        "mean_cost_rec": mean_cost_rec,
        "mean_margin_rec": mean_margin_rec,
        "fare_per_pax": fare_per_pax,
        "cost_per_pax": cost_per_pax,
        "margin_per_pax": margin_per_pax,
        "overall_recovery": overall_recovery,
        "delta_overall_rec_pp": overall_recovery - base_overall_recovery,
        "record_mean_recovery": record_mean_recovery,
        "record_median_recovery": record_median_recovery,
        "delta_rec_mean_pp": record_mean_recovery - base_record_mean_recovery,
        "total_co2_t": total_co2_t,
        "agg_co2_kwh": agg_co2_kwh,
        "delta_co2_kwh": agg_co2_kwh - base_co2_kwh,
        "mean_rating": mean_rating,
        "delta_rating": mean_rating - base_rating,
        "total_comp": total_comp,
        "weighted_comp_10k": weighted_comp_10k,
        "record_mean_comp_10k": record_mean_comp_10k,
        "delta_comp_10k": weighted_comp_10k - base_comp_10k,
    }


def compute_city_standardised_table(df_sub: pd.DataFrame, df_base: pd.DataFrame) -> pd.DataFrame:
    """Compute city summary table including direct modal-mix standardisation (Simpson's Paradox check)."""
    mode_weights = df_base["Transport_Mode"].value_counts(normalize=True).to_dict()
    global_mode_means = df_base.groupby("Transport_Mode")["Net_Margin_EUR"].mean().to_dict()

    pivot_margin = df_sub.pivot_table(
        index="City", columns="Transport_Mode", values="Net_Margin_EUR", aggfunc="mean"
    )
    std_margins = {}
    for city in pivot_margin.index:
        adj_val = 0.0
        for m, w in mode_weights.items():
            cell_val = pivot_margin.loc[city, m] if m in pivot_margin.columns else np.nan
            if pd.isna(cell_val):
                cell_val = global_mode_means[m]
            adj_val += w * float(cell_val)
        std_margins[city] = adj_val

    micro_share = (
        df_sub.assign(Is_Micro=df_sub["Transport_Mode"].isin(["Bike Share", "E-Scooter"]))
        .groupby("City")["Is_Micro"]
        .mean()
        * 100.0
    ).to_dict()

    city_df = (
        df_sub.groupby(["City", "Country"], as_index=False)
        .agg(
            Records=("Record_ID", "count"),
            Total_Pax=("Passengers", "sum"),
            Mean_Pax=("Passengers", "mean"),
            Mean_Delay=("Average_Delay_Minutes", "mean"),
            On_Time_Pct=("On_Time_Percentage", "mean"),
            Total_Rev=("Ticket_Revenue_EUR", "sum"),
            Total_Cost=("Operating_Cost_EUR", "sum"),
            Net_Margin=("Net_Margin_EUR", "sum"),
            Raw_Margin_Rec=("Net_Margin_EUR", "mean"),
            Rec_Mean_Recovery=("Cost_Recovery_Pct", "mean"),
            CO2_Tonnes=("CO2_Saved_KG", lambda s: s.sum() / 1000.0),
            Mean_Rating=("Customer_Rating", "mean"),
            Total_Comp=("Accessibility_Complaints", "sum"),
        )
    )
    city_df["Overall_Recovery_Pct"] = city_df["Total_Rev"] / city_df["Total_Cost"] * 100.0
    city_df["Mix_Adj_Margin_Rec"] = city_df["City"].map(std_margins)
    city_df["Micromobility_Share_Pct"] = city_df["City"].map(micro_share)
    city_df["Comp_per_10k_Pax"] = city_df["Total_Comp"] / city_df["Total_Pax"] * 10000.0
    city_df["Raw_Rank"] = city_df["Raw_Margin_Rec"].rank(ascending=False, method="min").astype(int)
    city_df["Adj_Rank"] = city_df["Mix_Adj_Margin_Rec"].rank(ascending=False, method="min").astype(int)
    city_df["Rank_Shift"] = city_df["Raw_Rank"] - city_df["Adj_Rank"]
    return city_df.sort_values("Raw_Margin_Rec", ascending=False).reset_index(drop=True)


# ==============================================================================
# PLOTLY CHART BUILDERS (LOCKED ARDEN PALETTE)
# ==============================================================================
def _apply_arden_layout(fig: go.Figure, title: str, subtitle: str = "", height: int = 380) -> go.Figure:
    title_html = f"<b>{title}</b>"
    if subtitle:
        title_html += f"<br><span style='font-size:11.5px;color:{MUTE};font-weight:400;'>{subtitle}</span>"
    fig.update_layout(
        title={"text": title_html, "font": {"family": "Aptos, Helvetica Neue, Arial, sans-serif", "size": 14, "color": MIDNIGHT}, "x": 0.01},
        font={"family": "Aptos, Helvetica Neue, Arial, sans-serif", "size": 11.5, "color": MIDNIGHT},
        paper_bgcolor=WHITE,
        plot_bgcolor=PAPER,
        height=height,
        margin={"l": 55, "r": 35, "t": 68, "b": 48},
        hoverlabel={"bgcolor": MIDNIGHT, "font_size": 11.5, "font_family": "Aptos, sans-serif", "font_color": WHITE},
    )
    fig.update_xaxes(showgrid=False, linecolor=LINE, tickfont={"color": MUTE, "size": 10.5})
    fig.update_yaxes(showgrid=True, gridcolor=GRID, linecolor=LINE, tickfont={"color": MUTE, "size": 10.5})
    return fig


def chart_monthly_trend(df_sub: pd.DataFrame, split_regime: bool = True, height: int = 360) -> go.Figure:
    fig = go.Figure()
    m_all = df_sub.groupby("YearMonth", as_index=False)["Passengers"].mean().sort_values("YearMonth")

    if split_regime and df_sub["Day_Type"].nunique() > 1:
        m_wk = (
            df_sub[df_sub["Day_Type"] == "Weekday"]
            .groupby("YearMonth", as_index=False)["Passengers"]
            .mean()
            .sort_values("YearMonth")
        )
        m_we = (
            df_sub[df_sub["Day_Type"] == "Weekend"]
            .groupby("YearMonth", as_index=False)["Passengers"]
            .mean()
            .sort_values("YearMonth")
        )
        fig.add_trace(
            go.Scatter(
                x=m_wk["YearMonth"],
                y=m_wk["Passengers"].round(0),
                mode="lines+markers",
                name="Weekday Mean",
                line={"color": MIDNIGHT, "width": 2.6},
                marker={"color": TIFFANY_DEEP, "size": 6, "line": {"color": MIDNIGHT, "width": 1}},
                hovertemplate="<b>%{x}</b> (Weekday)<br>Mean Demand: %{y:,.0f} pax<extra></extra>",
            )
        )
        fig.add_trace(
            go.Scatter(
                x=m_we["YearMonth"],
                y=m_we["Passengers"].round(0),
                mode="lines+markers",
                name="Weekend Mean",
                line={"color": TEAL, "width": 2.0, "dash": "dot"},
                marker={"color": TIFFANY, "size": 5},
                hovertemplate="<b>%{x}</b> (Weekend)<br>Mean Demand: %{y:,.0f} pax<extra></extra>",
            )
        )
    else:
        fig.add_trace(
            go.Scatter(
                x=m_all["YearMonth"],
                y=m_all["Passengers"].round(0),
                mode="lines+markers",
                name="Overall Mean Demand",
                line={"color": MIDNIGHT, "width": 2.8},
                marker={"color": TIFFANY_DEEP, "size": 6.5, "line": {"color": MIDNIGHT, "width": 1}},
                hovertemplate="<b>%{x}</b><br>Mean Demand: %{y:,.0f} pax<extra></extra>",
            )
        )

    overall_mean = float(df_sub["Passengers"].mean())
    fig.add_hline(
        y=overall_mean,
        line_dash="dash",
        line_color=SLATE,
        line_width=1.2,
        annotation_text=f"Slice Mean: {overall_mean:,.0f} pax",
        annotation_position="top right",
        annotation_font={"size": 10, "color": MUTE},
    )
    _apply_arden_layout(
        fig,
        title="Monthly Passenger Demand Trajectory (2024–2025)",
        subtitle="Mean daily passengers per service record across months (with weekday vs weekend regime split)",
        height=height,
    )
    fig.update_layout(
        legend={"orientation": "h", "yanchor": "bottom", "y": 1.02, "xanchor": "right", "x": 1.0},
        yaxis_title="Mean Passengers / Record",
    )
    return fig


def chart_mode_recovery(df_sub: pd.DataFrame, height: int = 360) -> go.Figure:
    mode_df = (
        df_sub.groupby("Transport_Mode", as_index=False)
        .agg(
            Rev=("Ticket_Revenue_EUR", "sum"),
            Cost=("Operating_Cost_EUR", "sum"),
            Rec_Mean=("Cost_Recovery_Pct", "mean"),
            Pax=("Passengers", "sum"),
        )
        .assign(Overall_Rec=lambda d: d["Rev"] / d["Cost"] * 100.0)
        .sort_values("Overall_Rec", ascending=True)
    )
    colors = [TIFFANY if r < 100.0 else MIDNIGHT_SOFT for r in mode_df["Overall_Rec"]]
    fig = go.Figure(
        go.Bar(
            x=mode_df["Overall_Rec"].round(1),
            y=mode_df["Transport_Mode"],
            orientation="h",
            marker={"color": colors, "line": {"color": MIDNIGHT, "width": 0.8}},
            text=[f"{r:.1f}%" for r in mode_df["Overall_Rec"]],
            textposition="outside",
            customdata=np.stack([mode_df["Rec_Mean"], mode_df["Rev"] - mode_df["Cost"], mode_df["Pax"]], axis=-1),
            hovertemplate=(
                "<b>%{y}</b><br>"
                "Volume-Weighted Recovery: <b>%{x:.1f}%</b><br>"
                "Unweighted Record Mean: %{customdata[0]:.1f}%<br>"
                "Net Margin: €%{customdata[1]:,.0f}<br>"
                "Total Passengers: %{customdata[2]:,.0f}<extra></extra>"
            ),
        )
    )
    fig.add_vline(
        x=100.0,
        line_dash="dash",
        line_color=MIDNIGHT,
        line_width=1.4,
        annotation_text="100% Break-Even",
        annotation_position="top right",
        annotation_font={"size": 10, "color": MIDNIGHT},
    )
    max_x = max(float(mode_df["Overall_Rec"].max()) * 1.18, 125.0) if not mode_df.empty else 130.0
    _apply_arden_layout(
        fig,
        title="Commercial Cost Recovery Ratio (%) by Transport Mode",
        subtitle="Cumulative Ticket Revenue ÷ Operating Cost (Tiffany bars < 100% require operational subsidy)",
        height=height,
    )
    fig.update_xaxes(range=[0, max_x], title="Cost Recovery (%)", showgrid=True, gridcolor=GRID)
    fig.update_yaxes(showgrid=False)
    return fig


def chart_weather_delay(df_sub: pd.DataFrame, height: int = 360) -> go.Figure:
    w_df = (
        df_sub.groupby("Weather", as_index=False)
        .agg(
            Mean_Delay=("Average_Delay_Minutes", "mean"),
            Median_Delay=("Average_Delay_Minutes", "median"),
            On_Time=("On_Time_Percentage", "mean"),
            Records=("Record_ID", "count"),
        )
        .set_index("Weather")
        .reindex([w for w in WEATHER_ORDER if w in df_sub["Weather"].unique()])
        .reset_index()
    )
    colors = [TIFFANY if w in ("Rain", "Snow") else MIDNIGHT_SOFT for w in w_df["Weather"]]
    fig = go.Figure(
        go.Bar(
            x=w_df["Weather"],
            y=w_df["Mean_Delay"].round(2),
            marker={"color": colors, "line": {"color": MIDNIGHT, "width": 0.8}},
            text=[f"{v:.2f}m" for v in w_df["Mean_Delay"]],
            textposition="outside",
            customdata=np.stack([w_df["Median_Delay"], w_df["On_Time"], w_df["Records"]], axis=-1),
            hovertemplate=(
                "<b>%{x}</b><br>"
                "Mean Delay: <b>%{y:.2f} min</b> (Median: %{customdata[0]:.2f} min)<br>"
                "Mean On-Time Rate: %{customdata[1]:.1f}%<br>"
                "Records: %{customdata[2]:,.0f}<extra></extra>"
            ),
        )
    )
    max_y = max(float(w_df["Mean_Delay"].max()) * 1.22, 6.0) if not w_df.empty else 9.0
    _apply_arden_layout(
        fig,
        title="Mean Service Delay (Minutes) by Weather Condition",
        subtitle="Tiffany accent highlights precipitation-induced delay escalation (Rain & Snow)",
        height=height,
    )
    fig.update_yaxes(range=[0, max_y], title="Mean Delay (Minutes)")
    return fig


def chart_route_complaints(df_sub: pd.DataFrame, metric_mode: str = "weighted", height: int = 360) -> go.Figure:
    r_df = (
        df_sub.groupby("Route_Type", as_index=False)
        .agg(
            Comp=("Accessibility_Complaints", "sum"),
            Pax=("Passengers", "sum"),
            Rec_Rate=("Complaints_per_10k_Pax", "mean"),
        )
        .assign(Weighted_Rate=lambda d: np.where(d["Pax"] > 0, d["Comp"] / d["Pax"] * 10000.0, 0.0))
    )
    if metric_mode == "raw":
        col = "Comp"
        x_label = "Total Raw Accessibility Complaints"
        sub = "Raw count (confounded by passenger volume exposure, r = 0.866)"
        fmt = "{:,.0f}"
    elif metric_mode == "record_mean":
        col = "Rec_Rate"
        x_label = "Unweighted Record-Mean Complaints / 10k Pax"
        sub = "Mean of daily record complaint rates (amplifies small-denominator micromobility trips)"
        fmt = "{:.2f}"
    else:
        col = "Weighted_Rate"
        x_label = "Volume-Weighted Complaints per 10,000 Passengers"
        sub = "Total Route Complaints ÷ Total Route Passengers × 10,000 (removes exposure bias)"
        fmt = "{:.2f}"

    r_df = r_df.sort_values(col, ascending=True)
    max_val = float(r_df[col].max()) if not r_df.empty else 1.0
    colors = [TIFFANY if v == max_val else MIDNIGHT_SOFT for v in r_df[col]]

    fig = go.Figure(
        go.Bar(
            x=r_df[col],
            y=r_df["Route_Type"],
            orientation="h",
            marker={"color": colors, "line": {"color": MIDNIGHT, "width": 0.8}},
            text=[fmt.format(v) for v in r_df[col]],
            textposition="outside",
            customdata=np.stack([r_df["Weighted_Rate"], r_df["Rec_Rate"], r_df["Comp"], r_df["Pax"]], axis=-1),
            hovertemplate=(
                "<b>%{y}</b><br>"
                "Volume-Weighted Rate: <b>%{customdata[0]:.2f} / 10k pax</b><br>"
                "Unweighted Record Mean: %{customdata[1]:.2f} / 10k pax<br>"
                "Raw Complaints: %{customdata[2]:,.0f} (across %{customdata[3]:,.0f} pax)<extra></extra>"
            ),
        )
    )
    _apply_arden_layout(
        fig,
        title="Accessibility Complaint Intensity by Route Topology",
        subtitle=sub,
        height=height,
    )
    fig.update_xaxes(range=[0, max_val * 1.20 if max_val > 0 else 20], title=x_label, showgrid=True, gridcolor=GRID)
    fig.update_yaxes(showgrid=False)
    return fig


def chart_modal_share_discrepancy(df_sub: pd.DataFrame) -> go.Figure:
    """Compare Record Share (%) vs Passenger Share (%) vs Operating Cost Share (%) by Mode."""
    m_df = (
        df_sub.groupby("Transport_Mode", as_index=False)
        .agg(
            Records=("Record_ID", "count"),
            Pax=("Passengers", "sum"),
            Cost=("Operating_Cost_EUR", "sum"),
            Rev=("Ticket_Revenue_EUR", "sum"),
        )
    )
    m_df["Record_Share"] = m_df["Records"] / m_df["Records"].sum() * 100.0
    m_df["Pax_Share"] = m_df["Pax"] / m_df["Pax"].sum() * 100.0
    m_df["Cost_Share"] = m_df["Cost"] / m_df["Cost"].sum() * 100.0
    m_df = m_df.set_index("Transport_Mode").reindex([m for m in MODE_ORDER if m in m_df["Transport_Mode"].values]).reset_index()

    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            name="Share of Daily Records (%)",
            x=m_df["Transport_Mode"],
            y=m_df["Record_Share"].round(2),
            marker_color=SLATE,
            text=[f"{v:.1f}%" for v in m_df["Record_Share"]],
            textposition="outside",
        )
    )
    fig.add_trace(
        go.Bar(
            name="Share of Total Passengers (%)",
            x=m_df["Transport_Mode"],
            y=m_df["Pax_Share"].round(2),
            marker_color=MIDNIGHT,
            text=[f"{v:.1f}%" for v in m_df["Pax_Share"]],
            textposition="outside",
        )
    )
    fig.add_trace(
        go.Bar(
            name="Share of Operating Cost (%)",
            x=m_df["Transport_Mode"],
            y=m_df["Cost_Share"].round(2),
            marker_color=TIFFANY_DEEP,
            text=[f"{v:.1f}%" for v in m_df["Cost_Share"]],
            textposition="outside",
        )
    )
    max_y = max(float(m_df[["Record_Share", "Pax_Share", "Cost_Share"]].max().max()) * 1.20, 30.0) if not m_df.empty else 75.0
    _apply_arden_layout(
        fig,
        title="Compositional Discrepancy: Record Share vs Ridership Share vs Cost Share",
        subtitle="Why unweighted record means (84.12% recovery) diverge from volume-weighted network totals (99.58% recovery)",
        height=390,
    )
    fig.update_layout(
        barmode="group",
        legend={"orientation": "h", "yanchor": "bottom", "y": 1.02, "xanchor": "right", "x": 1.0},
        yaxis={"range": [0, max_y], "title": "Percentage of Network Total (%)"},
    )
    return fig


def chart_simpsons_paradox_dumbbell(city_df: pd.DataFrame) -> go.Figure:
    """Figure 2 Interactive: Connected Dumbbell Chart of Raw vs Modal-Mix-Adjusted City Net Margin."""
    cdf = city_df.sort_values("Raw_Margin_Rec", ascending=True).reset_index(drop=True)
    fig = go.Figure()

    for row in cdf.itertuples():
        fig.add_trace(
            go.Scatter(
                x=[row.Raw_Margin_Rec, row.Mix_Adj_Margin_Rec],
                y=[row.City, row.City],
                mode="lines",
                line={"color": LINE, "width": 3.0},
                showlegend=False,
                hoverinfo="skip",
            )
        )

    fig.add_trace(
        go.Scatter(
            x=cdf["Raw_Margin_Rec"].round(2),
            y=cdf["City"],
            mode="markers+text",
            name="Raw Mean Margin (€/record)",
            marker={"color": MIDNIGHT, "size": 11, "line": {"color": WHITE, "width": 1.2}},
            text=[f"#{r}" for r in cdf["Raw_Rank"]],
            textposition="middle left",
            textfont={"size": 9.5, "color": MIDNIGHT},
            customdata=np.stack([cdf["Raw_Rank"], cdf["Micromobility_Share_Pct"], cdf["Net_Margin"]], axis=-1),
            hovertemplate=(
                "<b>%{y} — Unadjusted Raw</b><br>"
                "Mean Margin: <b>€%{x:,.2f} / record</b> (Rank #%{customdata[0]:.0f})<br>"
                "Cumulative Net Margin: €%{customdata[2]:,.0f}<br>"
                "Micromobility Record Share: %{customdata[1]:.2f}%<extra></extra>"
            ),
        )
    )

    fig.add_trace(
        go.Scatter(
            x=cdf["Mix_Adj_Margin_Rec"].round(2),
            y=cdf["City"],
            mode="markers+text",
            name="Modal-Mix Adjusted Margin (€/record)",
            marker={"color": TIFFANY, "size": 12, "symbol": "diamond", "line": {"color": MIDNIGHT, "width": 1.2}},
            text=[f"#{r}" for r in cdf["Adj_Rank"]],
            textposition="middle right",
            textfont={"size": 9.5, "color": TIFFANY_DEEP},
            customdata=np.stack([cdf["Adj_Rank"], cdf["Rank_Shift"]], axis=-1),
            hovertemplate=(
                "<b>%{y} — Modal-Mix Standardised</b><br>"
                "Adjusted Margin: <b>€%{x:,.2f} / record</b> (Rank #%{customdata[0]:.0f})<br>"
                "Rank Shift: %{customdata[1]:+.0f} positions<extra></extra>"
            ),
        )
    )

    fig.add_vline(x=0.0, line_dash="dash", line_color=MIDNIGHT, line_width=1.3, annotation_text="Break-Even (€0)")
    _apply_arden_layout(
        fig,
        title="Figure 2 Interactive — Simpson’s Paradox in City Financial Rankings",
        subtitle="Raw mean net margin vs direct modal-mix standardised margin (€/record; r = -0.795 confounding with micromobility share)",
        height=430,
    )
    fig.update_layout(
        legend={"orientation": "h", "yanchor": "bottom", "y": 1.02, "xanchor": "right", "x": 1.0},
        xaxis={"title": "Net Operating Margin (€ per Daily Service Record)", "showgrid": True, "gridcolor": GRID},
        yaxis={"showgrid": False},
    )
    return fig


def chart_unit_economics(df_sub: pd.DataFrame) -> go.Figure:
    """Figure 3 Interactive: Fare vs Operating Cost per Passenger (€) & Carbon Return (€/tCO2)."""
    m_df = (
        df_sub.groupby("Transport_Mode", as_index=False)
        .agg(
            Rev=("Ticket_Revenue_EUR", "sum"),
            Cost=("Operating_Cost_EUR", "sum"),
            Pax=("Passengers", "sum"),
            CO2_KG=("CO2_Saved_KG", "sum"),
        )
    )
    m_df["Fare_Pax"] = np.where(m_df["Pax"] > 0, m_df["Rev"] / m_df["Pax"], 0.0)
    m_df["Cost_Pax"] = np.where(m_df["Pax"] > 0, m_df["Cost"] / m_df["Pax"], 0.0)
    m_df["Net_Pax"] = m_df["Fare_Pax"] - m_df["Cost_Pax"]
    m_df["Return_per_tCO2"] = np.where(m_df["CO2_KG"] > 0, (m_df["Rev"] - m_df["Cost"]) / (m_df["CO2_KG"] / 1000.0), 0.0)
    m_df = m_df.set_index("Transport_Mode").reindex([m for m in MODE_ORDER if m in m_df["Transport_Mode"].values]).reset_index()

    fig = make_subplots(
        rows=1,
        cols=2,
        subplot_titles=(
            "Unit Economics: Fare vs Cost per Passenger (€/pax)",
            "Net Financial Return per Tonne of CO2 Saved (€/tCO2)",
        ),
        horizontal_spacing=0.14,
    )

    fig.add_trace(
        go.Bar(
            y=m_df["Transport_Mode"],
            x=m_df["Fare_Pax"].round(2),
            orientation="h",
            name="Fare Revenue / Pax (€)",
            marker_color=MIDNIGHT,
            text=[f"€{v:.2f}" for v in m_df["Fare_Pax"]],
            textposition="outside",
        ),
        row=1,
        col=1,
    )
    fig.add_trace(
        go.Bar(
            y=m_df["Transport_Mode"],
            x=m_df["Cost_Pax"].round(2),
            orientation="h",
            name="Operating Cost / Pax (€)",
            marker_color=TIFFANY,
            text=[f"€{v:.2f}" for v in m_df["Cost_Pax"]],
            textposition="outside",
        ),
        row=1,
        col=1,
    )

    ret_colors = [MIDNIGHT_SOFT if v >= 0 else TIFFANY for v in m_df["Return_per_tCO2"]]
    fig.add_trace(
        go.Bar(
            y=m_df["Transport_Mode"],
            x=m_df["Return_per_tCO2"].round(0),
            orientation="h",
            name="Net Return (€ / tCO2)",
            marker_color=ret_colors,
            showlegend=False,
            text=[f"{'+' if v >= 0 else ''}€{v:,.0f}/t" for v in m_df["Return_per_tCO2"]],
            textposition="outside",
        ),
        row=1,
        col=2,
    )

    _apply_arden_layout(
        fig,
        title="Figure 3 Interactive — Modal Unit Economics & Carbon Abatement Cost-Effectiveness",
        subtitle="Left: Volume-weighted fare vs operating cost per passenger (€/pax) · Right: Net financial surplus/deficit per tonne of CO2 mitigated",
        height=430,
    )
    fig.update_layout(
        barmode="group",
        legend={"orientation": "h", "yanchor": "bottom", "y": 1.04, "xanchor": "right", "x": 1.0},
    )
    fig.update_xaxes(title_text="€ per Passenger", range=[0, 30], row=1, col=1, showgrid=True, gridcolor=GRID)
    fig.update_xaxes(title_text="€ per Tonne CO2 Saved", row=1, col=2, showgrid=True, gridcolor=GRID)
    return fig


def chart_delay_violin(df_sub: pd.DataFrame) -> go.Figure:
    """Figure 4 Interactive: Delay Distribution (Violin + Embedded Boxplot) across Modes."""
    fig = go.Figure()
    modes_present = [m for m in ["Bus", "Tram", "Park and Ride", "E-Scooter", "Bike Share", "Metro"] if m in df_sub["Transport_Mode"].unique()]
    for m in modes_present:
        sub = df_sub[df_sub["Transport_Mode"] == m]["Average_Delay_Minutes"]
        color = TIFFANY if m == "Bus" else (TIFFANY_DEEP if m in ("Tram", "Metro") else MIDNIGHT_SOFT)
        fig.add_trace(
            go.Violin(
                x=sub,
                y=[m] * len(sub),
                name=m,
                orientation="h",
                box_visible=True,
                meanline_visible=True,
                fillcolor=color,
                line_color=MIDNIGHT,
                opacity=0.82,
                points=False,
            )
        )
    _apply_arden_layout(
        fig,
        title="Figure 4 Interactive — Service Delay Distribution by Transport Mode",
        subtitle="Violin density + embedded median/IQR boxplot (Bus exhibits widest right-skewed tail at 6.58 min mean; Metro tightest at 2.13 min)",
        height=400,
    )
    fig.update_layout(showlegend=False)
    fig.update_xaxes(title="Average Service Delay (Minutes)", showgrid=True, gridcolor=GRID)
    fig.update_yaxes(showgrid=False)
    return fig


def chart_delay_vs_satisfaction_joint(df_sub: pd.DataFrame) -> go.Figure:
    """Figure 5 Interactive: Bivariate Scatter & OLS Trendline of Delay vs Customer Rating."""
    fig = go.Figure()
    if len(df_sub) > 1:
        r_val = float(df_sub["Average_Delay_Minutes"].corr(df_sub["Customer_Rating"]))
        slope, intercept = np.polyfit(df_sub["Average_Delay_Minutes"], df_sub["Customer_Rating"], 1)
    else:
        r_val, slope, intercept = 0.0, 0.0, 4.0

    for ev_val, label, col, sz in [("No", "Standard Day (No)", MIDNIGHT_SOFT, 5.5), ("Yes", "Major Event Day (Yes)", TIFFANY, 7.5)]:
        sub = df_sub[df_sub["Event_Day"] == ev_val]
        if sub.empty:
            continue
        fig.add_trace(
            go.Scattergl(
                x=sub["Average_Delay_Minutes"],
                y=sub["Customer_Rating"],
                mode="markers",
                name=f"{label} (n={len(sub):,})",
                marker={"color": col, "size": sz, "opacity": 0.65, "line": {"color": MIDNIGHT, "width": 0.4}},
                customdata=np.stack([sub["City"], sub["Transport_Mode"], sub["Weather"], sub["Passengers"]], axis=-1),
                hovertemplate=(
                    "<b>%{customdata[0]} — %{customdata[1]}</b><br>"
                    "Delay: <b>%{x:.2f} min</b> · Rating: <b>%{y:.2f} / 5.00</b><br>"
                    "Weather: %{customdata[2]} · Passengers: %{customdata[3]:,.0f}<extra></extra>"
                ),
            )
        )

    if len(df_sub) > 1:
        x_line = np.linspace(float(df_sub["Average_Delay_Minutes"].min()), float(df_sub["Average_Delay_Minutes"].max()), 50)
        y_line = slope * x_line + intercept
        fig.add_trace(
            go.Scatter(
                x=x_line,
                y=y_line,
                mode="lines",
                name=f"OLS Linear Fit (r = {r_val:.3f}, R² = {r_val**2:.3f})",
                line={"color": MIDNIGHT, "width": 2.5, "dash": "solid"},
            )
        )

    fig.add_vline(x=6.0, line_dash="dot", line_color=TIFFANY_DEEP, annotation_text="6.0m Threshold")
    fig.add_hline(y=3.5, line_dash="dot", line_color=SLATE, annotation_text="3.5★ Satisfaction Floor")
    _apply_arden_layout(
        fig,
        title=f"Figure 5 Interactive — Service Delay vs Customer Satisfaction (r = {r_val:.3f})",
        subtitle=f"Associative OLS gradient: {slope:.3f} rating points per minute of delay (Non-causal observational association)",
        height=400,
    )
    fig.update_layout(legend={"orientation": "h", "yanchor": "bottom", "y": 1.02, "xanchor": "right", "x": 1.0})
    fig.update_xaxes(title="Average Service Delay (Minutes)", showgrid=True, gridcolor=GRID)
    fig.update_yaxes(title="Customer Rating (1.0 – 5.0 Scale)", range=[0.8, 5.2])
    return fig


def chart_weather_mode_heatmap(df_sub: pd.DataFrame, mode_type: str = "abs") -> go.Figure:
    """Figure 6 Interactive: 6 × 6 Weather × Mode Delay Matrix."""
    piv_delay = df_sub.pivot_table(
        index="Transport_Mode", columns="Weather", values="Average_Delay_Minutes", aggfunc="mean"
    )
    piv_ontime = df_sub.pivot_table(
        index="Transport_Mode", columns="Weather", values="On_Time_Percentage", aggfunc="mean"
    )
    modes = [m for m in ["Bus", "Tram", "Park and Ride", "E-Scooter", "Bike Share", "Metro"] if m in piv_delay.index]
    weathers = [w for w in WEATHER_ORDER if w in piv_delay.columns]
    piv_delay = piv_delay.reindex(index=modes, columns=weathers)
    piv_ontime = piv_ontime.reindex(index=modes, columns=weathers)

    if mode_type == "pct" and "Clear" in piv_delay.columns:
        clear_base = piv_delay["Clear"].replace(0, np.nan)
        z_mat = piv_delay.divide(clear_base, axis=0).subtract(1.0).multiply(100.0)
        text_mat = [[f"{v:+.0f}%" if pd.notna(v) else "-" for v in row] for row in z_mat.values]
        title = "Figure 6 Interactive — Relative Delay Escalation (%) vs Clear-Weather Baseline"
        cbar_title = "Δ% vs Clear"
    elif mode_type == "ontime":
        z_mat = piv_ontime
        text_mat = [[f"{v:.1f}%" if pd.notna(v) else "-" for v in row] for row in z_mat.values]
        title = "Figure 6 Interactive — Mean On-Time Performance (%) across Weather × Mode"
        cbar_title = "On-Time %"
    else:
        z_mat = piv_delay
        text_mat = [[f"{v:.2f}m" if pd.notna(v) else "-" for v in row] for row in z_mat.values]
        title = "Figure 6 Interactive — Mean Service Delay (Minutes) across Weather × Mode"
        cbar_title = "Delay (min)"

    fig = go.Figure(
        go.Heatmap(
            z=z_mat.values,
            x=weathers,
            y=modes,
            text=text_mat,
            texttemplate="<b>%{text}</b>",
            colorscale=[[0.0, MIST], [0.5, TIFFANY], [1.0, MIDNIGHT]],
            colorbar={"title": cbar_title},
            hovertemplate="<b>%{y} · %{x}</b><br>Value: <b>%{text}</b><extra></extra>",
        )
    )
    _apply_arden_layout(
        fig,
        title=title,
        subtitle="Surface modes (Bus 11.49m, Tram 8.95m in Snow) experience severe precipitation shocks vs underground Metro (3.85m)",
        height=400,
    )
    fig.update_yaxes(autorange="reversed", showgrid=False)
    return fig


def chart_accessibility_route_mode_heatmap(df_sub: pd.DataFrame, norm_mode: str = "weighted") -> go.Figure:
    """Figure 7 Interactive: Route × Mode Accessibility Matrix with Exposure-Bias Toggle."""
    routes = [r for r in ROUTE_ORDER if r in df_sub["Route_Type"].unique()]
    modes = [m for m in MODE_ORDER if m in df_sub["Transport_Mode"].unique()]

    if norm_mode == "raw":
        piv = df_sub.pivot_table(
            index="Route_Type", columns="Transport_Mode", values="Accessibility_Complaints", aggfunc="sum"
        ).reindex(index=routes, columns=modes)
        text_mat = [[f"{v:,.0f}" if pd.notna(v) else "-" for v in row] for row in piv.values]
        title = "Figure 7 Interactive — Raw Accessibility Complaint Counts (Confounded by Ridership Volume)"
        sub = "Raw complaint totals correlate with passenger volume (r = 0.866), masking low-volume micromobility friction"
        cbar = "Raw Count"
    elif norm_mode == "record_mean":
        piv = df_sub.pivot_table(
            index="Route_Type", columns="Transport_Mode", values="Complaints_per_10k_Pax", aggfunc="mean"
        ).reindex(index=routes, columns=modes)
        text_mat = [[f"{v:.1f}" if pd.notna(v) else "-" for v in row] for row in piv.values]
        title = "Figure 7 Interactive — Unweighted Record-Mean Complaints per 10,000 Passengers"
        sub = "Average of daily record complaint rates across Route × Mode cells"
        cbar = "Mean / 10k"
    else:
        comp_piv = df_sub.pivot_table(
            index="Route_Type", columns="Transport_Mode", values="Accessibility_Complaints", aggfunc="sum"
        ).reindex(index=routes, columns=modes)
        pax_piv = df_sub.pivot_table(
            index="Route_Type", columns="Transport_Mode", values="Passengers", aggfunc="sum"
        ).reindex(index=routes, columns=modes)
        piv = (comp_piv / pax_piv.replace(0, np.nan)) * 10000.0
        text_mat = [[f"{v:.1f}" if pd.notna(v) else "-" for v in row] for row in piv.values]
        title = "Figure 7 Interactive — Volume-Weighted Accessibility Complaints per 10,000 Passengers"
        sub = "Normalising by cumulative cell ridership reveals high friction on Suburban Feeder E-Scooter (54.0) & Bike Share (49.3)"
        cbar = "Rate / 10k"

    fig = go.Figure(
        go.Heatmap(
            z=piv.values,
            x=modes,
            y=routes,
            text=text_mat,
            texttemplate="<b>%{text}</b>",
            colorscale=[[0.0, MIST], [0.45, TIFFANY], [1.0, MIDNIGHT]],
            colorbar={"title": cbar},
            hovertemplate="<b>%{y} · %{x}</b><br>Metric: <b>%{text}</b><extra></extra>",
        )
    )
    _apply_arden_layout(fig, title=title, subtitle=sub, height=400)
    fig.update_yaxes(autorange="reversed", showgrid=False)
    return fig


def chart_carbon_efficiency(df_sub: pd.DataFrame) -> go.Figure:
    """Figure 8 Interactive: Decarbonisation Efficiency (kg CO2/kWh) vs Energy Intensity (kWh/pax)."""
    m_df = (
        df_sub.groupby("Transport_Mode", as_index=False)
        .agg(
            CO2_KG=("CO2_Saved_KG", "sum"),
            KWh=("Energy_Consumption_KWh", "sum"),
            Pax=("Passengers", "sum"),
            Records=("Record_ID", "count"),
        )
    )
    m_df["CO2_per_kWh"] = np.where(m_df["KWh"] > 0, m_df["CO2_KG"] / m_df["KWh"], 0.0)
    m_df["kWh_per_Pax"] = np.where(m_df["Pax"] > 0, m_df["KWh"] / m_df["Pax"], 0.0)
    m_df["CO2_Tonnes"] = m_df["CO2_KG"] / 1000.0

    fig = go.Figure()
    for row in m_df.itertuples():
        col = TIFFANY if row.Transport_Mode in ("Metro", "Tram") else (SLATE if row.Transport_Mode == "Bus" else MIDNIGHT_SOFT)
        sz = max(min(np.sqrt(row.CO2_Tonnes) * 1.15, 58.0), 16.0)
        fig.add_trace(
            go.Scatter(
                x=[row.kWh_per_Pax],
                y=[row.CO2_per_kWh],
                mode="markers+text",
                name=row.Transport_Mode,
                text=[f"<b>{row.Transport_Mode}</b><br>({row.CO2_per_kWh:.2f} kg/kWh)"],
                textposition="top center",
                marker={"size": sz, "color": col, "opacity": 0.88, "line": {"color": MIDNIGHT, "width": 1.5}},
                hovertemplate=(
                    f"<b>{row.Transport_Mode}</b><br>"
                    f"Carbon Efficiency: <b>{row.CO2_per_kWh:.2f} kg CO2 / kWh</b><br>"
                    f"Energy per Passenger: {row.kWh_per_Pax:.3f} kWh / pax<br>"
                    f"Total CO2 Mitigated: {row.CO2_Tonnes:,.1f} tonnes<br>"
                    f"Total Passengers: {row.Pax:,.0f}<extra></extra>"
                ),
            )
        )

    _apply_arden_layout(
        fig,
        title="Figure 8 Interactive — Decarbonisation Efficiency (kg CO2 / kWh) vs Energy Intensity",
        subtitle="Bubble area proportional to total CO2 saved (Metro saves 2,911.4t at 2.19 kg CO2/kWh — 2.05× Bus at 1.07 kg CO2/kWh)",
        height=400,
    )
    fig.update_xaxes(title="Energy Consumption per Passenger (kWh / Pax)", showgrid=True, gridcolor=GRID)
    fig.update_yaxes(title="Carbon Abatement Efficiency (kg CO2 Saved per kWh)", range=[0.5, 4.3])
    return fig


# ==============================================================================
# STREAMLIT APPLICATION LAYOUT & INTERACTIVITY
# ==============================================================================
def inject_custom_css() -> None:
    st.markdown(
        f"""
        <style>
          .block-container {{
              padding-top: 1.4rem !important;
              padding-bottom: 2.5rem !important;
              max-width: 1440px !important;
          }}
          .arden-banner {{
              background: linear-gradient(135deg, {MIDNIGHT} 0%, {MIDNIGHT_SOFT} 100%);
              color: {WHITE};
              padding: 18px 24px;
              border-radius: 14px;
              border-bottom: 4px solid {TIFFANY};
              margin-bottom: 14px;
              display: flex;
              justify-content: space-between;
              align-items: center;
              box-shadow: 0 3px 10px rgba(0, 43, 73, 0.10);
          }}
          .arden-banner h1 {{
              margin: 0 !important;
              padding: 0 !important;
              font-size: 1.38rem !important;
              font-weight: 700 !important;
              color: {WHITE} !important;
              letter-spacing: -0.2px;
          }}
          .arden-banner .sub {{
              font-size: 0.84rem;
              color: {MIST};
              margin-top: 4px;
          }}
          .arden-badge {{
              background: {TIFFANY_DEEP};
              color: {WHITE};
              padding: 6px 14px;
              border-radius: 20px;
              font-size: 0.78rem;
              font-weight: 700;
              white-space: nowrap;
              border: 1px solid {TIFFANY};
          }}
          .slice-bar {{
              background: {WHITE};
              border: 1.5px solid {LINE};
              border-left: 5px solid {TIFFANY_DEEP};
              border-radius: 10px;
              padding: 10px 16px;
              margin-bottom: 16px;
              display: flex;
              flex-wrap: wrap;
              justify-content: space-between;
              align-items: center;
              gap: 10px;
              font-size: 0.85rem;
          }}
          .filter-pill {{
              display: inline-block;
              background: {MIDNIGHT_SOFT};
              color: {WHITE};
              padding: 3px 10px;
              border-radius: 12px;
              font-size: 0.75rem;
              font-weight: 600;
              margin-right: 6px;
          }}
          .filter-pill.active {{
              background: {TIFFANY_DEEP};
              color: {WHITE};
          }}
          .kpi-grid {{
              display: grid;
              grid-template-columns: repeat(6, 1fr);
              gap: 12px;
              margin-bottom: 18px;
          }}
          @media (max-width: 1100px) {{
              .kpi-grid {{ grid-template-columns: repeat(3, 1fr); }}
          }}
          .kpi-card {{
              background: {WHITE};
              border: 1.5px solid {LINE};
              border-radius: 12px;
              padding: 13px 12px;
              text-align: center;
              box-shadow: 0 2px 6px rgba(0, 43, 73, 0.05);
          }}
          .kpi-card.focal {{
              background: {MIST};
              border: 2px solid {TIFFANY};
          }}
          .kpi-label {{
              font-size: 0.74rem;
              font-weight: 700;
              text-transform: uppercase;
              letter-spacing: 0.4px;
              color: {MUTE};
              margin-bottom: 4px;
          }}
          .kpi-val {{
              font-size: 1.48rem;
              font-weight: 800;
              color: {MIDNIGHT};
              line-height: 1.15;
              font-variant-numeric: tabular-nums;
          }}
          .kpi-sub {{
              font-size: 0.73rem;
              color: {MUTE};
              margin-top: 4px;
              line-height: 1.25;
          }}
          .kpi-delta {{
              display: inline-block;
              margin-top: 4px;
              padding: 1px 7px;
              border-radius: 8px;
              font-size: 0.70rem;
              font-weight: 700;
              background: {PAPER};
              color: {MIDNIGHT_SOFT};
              border: 1px solid {LINE};
          }}
          .note-callout {{
              background: {MIST};
              border-left: 4px solid {TIFFANY_DEEP};
              border-radius: 8px;
              padding: 11px 15px;
              font-size: 0.84rem;
              color: {MIDNIGHT};
              margin: 8px 0 14px 0;
          }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def main() -> None:
    st.set_page_config(
        page_title="EcoMove Mobility — Executive Streamlit Dashboard (25199053)",
        page_icon="🚊",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    inject_custom_css()

    df_base = load_dataset().copy()
    if "DayOfWeek" not in df_base.columns:
        df_base["DayOfWeek"] = (
            df_base["Day_of_Week"] if "Day_of_Week" in df_base.columns else df_base["Date_ISO"].dt.day_name()
        )
    if "Day_Type" not in df_base.columns:
        df_base["Day_Type"] = np.where(df_base["Date_ISO"].dt.dayofweek >= 5, "Weekend", "Weekday")
    all_countries = sorted(df_base["Country"].unique().tolist())
    all_modes = [m for m in MODE_ORDER if m in df_base["Transport_Mode"].unique()]
    all_routes = sorted(df_base["Route_Type"].unique().tolist())
    all_weathers = [w for w in WEATHER_ORDER if w in df_base["Weather"].unique()]
    min_date = df_base["Date_Only"].min()
    max_date = df_base["Date_Only"].max()

    # --------------------------------------------------------------------------
    # SIDEBAR: SCENARIO PRESETS & 6 COORDINATED FILTERS
    # --------------------------------------------------------------------------
    with st.sidebar:
        st.markdown(
            f"<div style='background:{MIDNIGHT};color:{WHITE};padding:12px 14px;border-radius:10px;"
            f"border-left:4px solid {TIFFANY};margin-bottom:12px;'>"
            f"<div style='font-weight:700;font-size:0.95rem;'>🎛️ Executive Filter Console</div>"
            f"<div style='font-size:0.75rem;color:{MIST};'>COM7021 · Student ID: 25199053</div></div>",
            unsafe_allow_html=True,
        )

        preset_names = list(SCENARIO_PRESETS.keys()) + ["7. Custom Interactive Exploration"]

        if "active_preset" not in st.session_state:
            st.session_state["active_preset"] = preset_names[0]
            st.session_state["f_regime"] = "All Days"
            st.session_state["f_countries"] = []
            st.session_state["f_cities"] = []
            st.session_state["f_modes"] = []
            st.session_state["f_routes"] = []
            st.session_state["f_weathers"] = []
            st.session_state["f_event"] = "All"

        def _on_preset_change() -> None:
            chosen = st.session_state["active_preset"]
            if chosen in SCENARIO_PRESETS:
                cfg = SCENARIO_PRESETS[chosen]
                st.session_state["f_regime"] = cfg["day_regime"]
                st.session_state["f_countries"] = list(cfg["countries"])
                st.session_state["f_cities"] = list(cfg["cities"])
                st.session_state["f_modes"] = list(cfg["modes"])
                st.session_state["f_routes"] = list(cfg["routes"])
                st.session_state["f_weathers"] = list(cfg["weathers"])
                st.session_state["f_event"] = cfg["event_day"]

        selected_preset = st.selectbox(
            "1-Click Executive Scenario Preset",
            options=preset_names,
            key="active_preset",
            on_change=_on_preset_change,
            help="Jump directly to the exact report scenarios (Figure 9 Full Baseline or Figure 10 Adverse Weather Surface Scenario) or explore custom slices.",
        )

        if selected_preset in SCENARIO_PRESETS:
            st.caption(f"📌 *{SCENARIO_PRESETS[selected_preset]['desc']}*")
        else:
            st.caption("📌 *Custom exploration mode: combine any filters below.*")

        st.markdown("---")
        st.markdown("**Granular Multi-Dimensional Filters**")

        date_range = st.date_input(
            "1. Date Window (2024–2025)",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date,
            key="f_dates",
        )

        day_regime = st.selectbox(
            "Day Regime (Weekday / Weekend)",
            options=["All Days", "Weekday", "Weekend"],
            key="f_regime",
        )

        sel_countries = st.multiselect(
            "2. Country (Leave empty for All 6)",
            options=all_countries,
            key="f_countries",
            placeholder="All 6 European Countries",
        )

        avail_cities = sorted(
            df_base[df_base["Country"].isin(sel_countries)]["City"].unique().tolist()
            if sel_countries
            else df_base["City"].unique().tolist()
        )
        # Ensure selected cities remain valid if country filter narrowed
        st.session_state["f_cities"] = [c for c in st.session_state.get("f_cities", []) if c in avail_cities]
        sel_cities = st.multiselect(
            "3. City (Leave empty for All)",
            options=avail_cities,
            key="f_cities",
            placeholder=f"All {len(avail_cities)} Cities",
        )

        sel_modes = st.multiselect(
            "4. Transport Mode (Leave empty for All 6)",
            options=all_modes,
            key="f_modes",
            placeholder="All 6 Transport Modes",
        )

        sel_routes = st.multiselect(
            "5. Route Topology (Leave empty for All 6)",
            options=all_routes,
            key="f_routes",
            placeholder="All 6 Route Types",
        )

        sel_weathers = st.multiselect(
            "6. Weather Condition (Leave empty for All 6)",
            options=all_weathers,
            key="f_weathers",
            placeholder="All 6 Weather Regimes",
        )

        sel_event = st.selectbox(
            "Major Event Day",
            options=["All", "No", "Yes"],
            key="f_event",
            format_func=lambda x: "All Days" if x == "All" else ("Event Day (Yes)" if x == "Yes" else "Standard Day (No)"),
        )

        st.markdown("---")
        fin_basis = st.selectbox(
            "Financial Table Basis",
            options=["Per-Record Mean (€/record)", "Cumulative Total (€)", "Per-Passenger Unit Rate (€/pax)"],
            index=0,
            help="Reconciles per-record, cumulative total, and per-passenger financial views.",
        )

    # --------------------------------------------------------------------------
    # APPLY FILTER MASK
    # --------------------------------------------------------------------------
    mask = pd.Series(True, index=df_base.index)
    if isinstance(date_range, (list, tuple)) and len(date_range) == 2:
        start_d, end_d = date_range[0], date_range[1]
        mask &= (df_base["Date_Only"] >= start_d) & (df_base["Date_Only"] <= end_d)
    if day_regime != "All Days":
        mask &= df_base["Day_Type"] == day_regime
    if sel_countries:
        mask &= df_base["Country"].isin(sel_countries)
    if sel_cities:
        mask &= df_base["City"].isin(sel_cities)
    if sel_modes:
        mask &= df_base["Transport_Mode"].isin(sel_modes)
    if sel_routes:
        mask &= df_base["Route_Type"].isin(sel_routes)
    if sel_weathers:
        mask &= df_base["Weather"].isin(sel_weathers)
    if sel_event != "All":
        mask &= df_base["Event_Day"] == sel_event

    df_sub = df_base[mask].copy()

    # --------------------------------------------------------------------------
    # TOP BANNER & ACTIVE FILTER STATUS STRIP
    # --------------------------------------------------------------------------
    st.markdown(
        f"""
        <div class="arden-banner">
          <div>
            <h1>EcoMove City Transport Authority — Executive Decision Dashboard</h1>
            <div class="sub">Interactive Streamlit &amp; Plotly Visualisation Framework · European Urban Mobility Network (2024–2025) · Arden Palette</div>
          </div>
          <div class="arden-badge">Student ID: 25199053 · COM7021</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if df_sub.empty:
        st.warning("No records match the currently selected filter combination. Please broaden one or more sidebar filters.")
        return

    m = compute_metrics(df_sub, df_base)

    chips = [
        ("Country", f"{len(sel_countries)} sel" if sel_countries else "All (6)", bool(sel_countries)),
        ("City", f"{len(sel_cities)} sel" if sel_cities else "All (12)", bool(sel_cities)),
        ("Mode", ", ".join(sel_modes) if len(sel_modes) <= 2 and sel_modes else (f"Surface ({len(sel_modes)})" if sel_modes else "All (6)"), bool(sel_modes)),
        ("Route", ", ".join(sel_routes) if len(sel_routes) == 1 else (f"{len(sel_routes)} sel" if sel_routes else "All (6)"), bool(sel_routes)),
        ("Weather", " + ".join(sel_weathers) if sel_weathers else "All (6)", bool(sel_weathers)),
        ("Event Day", sel_event, sel_event != "All"),
    ]
    pills_html = "".join(
        f'<span class="filter-pill {"active" if act else ""}">{lbl}: {val}</span>'
        for lbl, val, act in chips
    )
    st.markdown(
        f"""
        <div class="slice-bar">
          <div><strong>ACTIVE FILTER SLICE:</strong> &nbsp; {pills_html}</div>
          <div style="color:{MIDNIGHT};font-weight:700;">
            Showing <code>{m['n_rec']:,}</code> / 5,000 records ({m['rec_share_pct']:.1f}%) &nbsp;·&nbsp;
            <code>{m['total_pax']/1e6:.2f}M</code> / 40.91M passengers ({m['pax_share_pct']:.1f}%)
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # --------------------------------------------------------------------------
    # 6-CARD EXECUTIVE KPI STRIP (WITH DUAL-BASIS COST RECOVERY & BASELINE DELTAS)
    # --------------------------------------------------------------------------
    net_sign = "+" if m["net_margin"] >= 0 else "-"
    st.markdown(
        f"""
        <div class="kpi-grid">
          <div class="kpi-card">
            <div class="kpi-label">Total Passengers</div>
            <div class="kpi-val">{m['total_pax']/1e6:.2f}M</div>
            <div class="kpi-sub">Mean: {m['mean_pax']:,.0f}/rec · Med: {m['median_pax']:,.0f}</div>
            <div class="kpi-delta">Δ Mean vs Base: {m['delta_pax_pct']:+.1f}%</div>
          </div>
          <div class="kpi-card">
            <div class="kpi-label">Mean On-Time Rate</div>
            <div class="kpi-val">{m['mean_ontime']:.1f}%</div>
            <div class="kpi-sub">Authority Target: 85.0%</div>
            <div class="kpi-delta">Δ vs Base (82.1%): {m['delta_ontime_pp']:+.1f} pp</div>
          </div>
          <div class="kpi-card focal">
            <div class="kpi-label">Mean Service Delay</div>
            <div class="kpi-val">{m['mean_delay']:.2f} min</div>
            <div class="kpi-sub">Med: {m['median_delay']:.2f}m · IQR: {m['iqr_delay']:.2f}m</div>
            <div class="kpi-delta">Δ vs Base (4.35m): {m['delta_delay_pct']:+.1f}%</div>
          </div>
          <div class="kpi-card focal">
            <div class="kpi-label">Cost Recovery (Overall)</div>
            <div class="kpi-val">{m['overall_recovery']:.1f}%</div>
            <div class="kpi-sub">Record Mean: <b>{m['record_mean_recovery']:.1f}%</b> · {net_sign}€{abs(m['net_margin'])/1e6:.2f}M</div>
            <div class="kpi-delta">Fare €{m['fare_per_pax']:.2f} vs Cost €{m['cost_per_pax']:.2f}/pax</div>
          </div>
          <div class="kpi-card">
            <div class="kpi-label">Total CO2 Mitigated</div>
            <div class="kpi-val">{m['total_co2_t']:,.1f} t</div>
            <div class="kpi-sub">Efficiency: {m['agg_co2_kwh']:.2f} kg CO2/kWh</div>
            <div class="kpi-delta">Δ Efficiency: {m['delta_co2_kwh']:+.2f} kg/kWh</div>
          </div>
          <div class="kpi-card">
            <div class="kpi-label">Customer Satisfaction</div>
            <div class="kpi-val">{m['mean_rating']:.2f} / 5</div>
            <div class="kpi-sub">Complaints: <b>{m['weighted_comp_10k']:.2f} / 10k pax</b></div>
            <div class="kpi-delta">Δ Rating vs Base: {m['delta_rating']:+.2f}★</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # --------------------------------------------------------------------------
    # FIVE STRUCTURED DECISION TABS
    # --------------------------------------------------------------------------
    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        [
            "📊 1. Executive Overview (Figs 9 & 10)",
            "📈 2. Demand & Modal Regimes (Fig 1)",
            "💶 3. Financials & Simpson's Paradox (Figs 2 & 3)",
            "⏱️ 4. Reliability, Weather & Satisfaction (Figs 4–6)",
            "♿ 5. Accessibility, Carbon & Data Explorer (Figs 7 & 8)",
        ]
    )

    city_summary_df = compute_city_standardised_table(df_sub, df_base)

    # === TAB 1: EXECUTIVE OVERVIEW (FIGURES 9 & 10) ===
    with tab1:
        st.markdown(
            f"<div class='note-callout'><strong>Executive Decision Workspace (Figures 9 &amp; 10):</strong> "
            f"Coordinated 4-panel view updating live across all sidebar filters. Use the sidebar preset "
            f"<em>'1. Full Network Baseline'</em> to inspect <strong>Figure 9</strong> (N = 5,000; 99.6% overall recovery, 4.35 min delay, 40.91M pax) "
            f"or <em>'2. Adverse Weather Surface Transit'</em> to inspect <strong>Figure 10</strong> (n = 583; 2.80M pax; 7.38 min delay, +69.7% above baseline; "
            f"72.2% on-time rate; 113.2% overall recovery, +€0.84M net surplus; 17.46 / 10k complaints).</div>",
            unsafe_allow_html=True,
        )
        r1c1, r1c2 = st.columns(2)
        with r1c1:
            st.plotly_chart(chart_monthly_trend(df_sub, split_regime=True, height=340), width="stretch")
        with r1c2:
            st.plotly_chart(chart_mode_recovery(df_sub, height=340), width="stretch")

        r2c1, r2c2 = st.columns(2)
        with r2c1:
            st.plotly_chart(chart_weather_delay(df_sub, height=340), width="stretch")
        with r2c2:
            st.plotly_chart(chart_route_complaints(df_sub, metric_mode="weighted", height=340), width="stretch")

        st.markdown("#### City-Level Executive Decision Summary (Live Filtered Slice)")
        disp_city = city_summary_df[
            [
                "City",
                "Country",
                "Records",
                "Total_Pax",
                "Mean_Delay",
                "On_Time_Pct",
                "Overall_Recovery_Pct",
                "Rec_Mean_Recovery",
                "Net_Margin",
                "Raw_Margin_Rec",
                "Mix_Adj_Margin_Rec",
                "CO2_Tonnes",
                "Mean_Rating",
                "Comp_per_10k_Pax",
            ]
        ].rename(
            columns={
                "Total_Pax": "Passengers",
                "Mean_Delay": "Delay (min)",
                "On_Time_Pct": "On-Time (%)",
                "Overall_Recovery_Pct": "Overall Rec (%)",
                "Rec_Mean_Recovery": "Record Mean Rec (%)",
                "Net_Margin": "Total Net (€)",
                "Raw_Margin_Rec": "Raw Margin (€/rec)",
                "Mix_Adj_Margin_Rec": "Mix-Adj Margin (€/rec)",
                "CO2_Tonnes": "CO2 Saved (t)",
                "Mean_Rating": "Rating (/5)",
                "Comp_per_10k_Pax": "Comp / 10k Pax",
            }
        )
        st.dataframe(
            disp_city.style.format(
                {
                    "Records": "{:,}",
                    "Passengers": "{:,.0f}",
                    "Delay (min)": "{:.2f}",
                    "On-Time (%)": "{:.1f}%",
                    "Overall Rec (%)": "{:.1f}%",
                    "Record Mean Rec (%)": "{:.1f}%",
                    "Total Net (€)": "€{:,.0f}",
                    "Raw Margin (€/rec)": "€{:,.2f}",
                    "Mix-Adj Margin (€/rec)": "€{:,.2f}",
                    "CO2 Saved (t)": "{:,.1f}",
                    "Rating (/5)": "{:.2f}",
                    "Comp / 10k Pax": "{:.2f}",
                }
            ),
            width="stretch",
            hide_index=True,
        )

    # === TAB 2: DEMAND & MODAL REGIMES (FIGURE 1) ===
    with tab2:
        st.markdown(
            "<div class='note-callout'><strong>Temporal Regime &amp; Modal Skewness Analysis (Figure 1 &amp; Section 1.2):</strong> "
            "Weekday commuting generates a <strong>+34.1% demand premium</strong> over weekends (8,802.88 vs 6,562.86 pax/record), while "
            "the recurring <strong>October trough (-27.2% at 6,805.48 pax/record)</strong> identifies the optimal low-disruption window for "
            "capital infrastructure maintenance. Right panel explains why pooling Metro (62.96% of passengers) with shared micromobility "
            "(24.64% of records but 1.06% of passengers) creates severe positive skewness (+1.90).</div>",
            unsafe_allow_html=True,
        )
        c_left, c_right = st.columns([1.15, 1.0])
        with c_left:
            st.plotly_chart(chart_monthly_trend(df_sub, split_regime=True, height=390), width="stretch")
        with c_right:
            st.plotly_chart(chart_modal_share_discrepancy(df_sub), width="stretch")

        # Day of week breakdown table
        dow_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        dow_df = (
            df_sub.groupby(["DayOfWeek", "Day_Type"], as_index=False)
            .agg(
                Records=("Record_ID", "count"),
                Total_Pax=("Passengers", "sum"),
                Mean_Pax=("Passengers", "mean"),
                Median_Pax=("Passengers", "median"),
                Mean_Delay=("Average_Delay_Minutes", "mean"),
                Overall_Rec=("Ticket_Revenue_EUR", lambda s: s.sum() / df_sub.loc[s.index, "Operating_Cost_EUR"].sum() * 100.0),
            )
        )
        dow_df["Order"] = dow_df["DayOfWeek"].apply(lambda d: dow_order.index(d) if d in dow_order else 99)
        dow_df = dow_df.sort_values("Order").drop(columns=["Order"])
        st.markdown("#### Day-of-Week Operational Regime Breakdown")
        st.dataframe(
            dow_df.style.format(
                {
                    "Records": "{:,}",
                    "Total_Pax": "{:,.0f}",
                    "Mean_Pax": "{:,.2f}",
                    "Median_Pax": "{:,.1f}",
                    "Mean_Delay": "{:.2f} min",
                    "Overall_Rec": "{:.2f}%",
                }
            ),
            width="stretch",
            hide_index=True,
        )

    # === TAB 3: FINANCIALS & SIMPSON'S PARADOX (FIGURES 2 & 3) ===
    with tab3:
        st.markdown(
            "<div class='note-callout'><strong>Financial Reconciliation &amp; Simpson’s Paradox (Figures 2 &amp; 3):</strong> "
            "Reconciles <strong>cumulative totals</strong> (€111.64M rev vs €112.11M cost = -€0.47M), <strong>per-record means</strong> "
            "(€22,328.12 vs €22,422.00 = -€93.88/record), and <strong>per-passenger rates</strong> (€2.73 vs €2.74 = -€0.01/pax). "
            "Crucially, <strong>volume-weighted overall cost recovery is 99.58%</strong>, whereas the <strong>unweighted average of daily "
            "record cost-recovery ratios is 84.12%</strong> (median 102.26%) because low-recovery Bike Share (15.13%) and E-Scooter (14.57%) "
            "represent 24.64% of daily records.</div>",
            unsafe_allow_html=True,
        )

        f1, f2 = st.columns([1.05, 1.15])
        with f1:
            st.plotly_chart(chart_simpsons_paradox_dumbbell(city_summary_df), width="stretch")
        with f2:
            st.plotly_chart(chart_unit_economics(df_sub), width="stretch")

        st.markdown(f"#### Multi-Basis Modal Financial Reconciliation Ledger ({fin_basis})")
        mode_fin = (
            df_sub.groupby("Transport_Mode", as_index=False)
            .agg(
                Records=("Record_ID", "count"),
                Passengers=("Passengers", "sum"),
                Total_Rev=("Ticket_Revenue_EUR", "sum"),
                Total_Cost=("Operating_Cost_EUR", "sum"),
                Total_Net=("Net_Margin_EUR", "sum"),
                Rev_per_Rec=("Ticket_Revenue_EUR", "mean"),
                Cost_per_Rec=("Operating_Cost_EUR", "mean"),
                Net_per_Rec=("Net_Margin_EUR", "mean"),
                Unweighted_Rec_Mean_Pct=("Cost_Recovery_Pct", "mean"),
                Unweighted_Rec_Median_Pct=("Cost_Recovery_Pct", "median"),
            )
        )
        mode_fin["Overall_Weighted_Rec_Pct"] = mode_fin["Total_Rev"] / mode_fin["Total_Cost"] * 100.0
        mode_fin["Fare_per_Pax"] = mode_fin["Total_Rev"] / mode_fin["Passengers"]
        mode_fin["Cost_per_Pax"] = mode_fin["Total_Cost"] / mode_fin["Passengers"]
        mode_fin["Net_per_Pax"] = mode_fin["Total_Net"] / mode_fin["Passengers"]
        mode_fin = mode_fin.set_index("Transport_Mode").reindex([m_name for m_name in MODE_ORDER if m_name in mode_fin["Transport_Mode"].values]).reset_index()

        st.dataframe(
            mode_fin[
                [
                    "Transport_Mode",
                    "Records",
                    "Passengers",
                    "Total_Rev",
                    "Total_Cost",
                    "Total_Net",
                    "Rev_per_Rec",
                    "Cost_per_Rec",
                    "Net_per_Rec",
                    "Fare_per_Pax",
                    "Cost_per_Pax",
                    "Net_per_Pax",
                    "Overall_Weighted_Rec_Pct",
                    "Unweighted_Rec_Mean_Pct",
                    "Unweighted_Rec_Median_Pct",
                ]
            ]
            .rename(
                columns={
                    "Transport_Mode": "Mode",
                    "Total_Rev": "Total Rev (€)",
                    "Total_Cost": "Total Cost (€)",
                    "Total_Net": "Total Net (€)",
                    "Rev_per_Rec": "Rev / Rec (€)",
                    "Cost_per_Rec": "Cost / Rec (€)",
                    "Net_per_Rec": "Net / Rec (€)",
                    "Fare_per_Pax": "Fare / Pax (€)",
                    "Cost_per_Pax": "Cost / Pax (€)",
                    "Net_per_Pax": "Net / Pax (€)",
                    "Overall_Weighted_Rec_Pct": "Overall Recovery (%)",
                    "Unweighted_Rec_Mean_Pct": "Record Mean Rec (%)",
                    "Unweighted_Rec_Median_Pct": "Record Median Rec (%)",
                }
            )
            .style.format(
                {
                    "Records": "{:,}",
                    "Passengers": "{:,.0f}",
                    "Total Rev (€)": "€{:,.0f}",
                    "Total Cost (€)": "€{:,.0f}",
                    "Total Net (€)": "€{:,.0f}",
                    "Rev / Rec (€)": "€{:,.2f}",
                    "Cost / Rec (€)": "€{:,.2f}",
                    "Net / Rec (€)": "€{:,.2f}",
                    "Fare / Pax (€)": "€{:.2f}",
                    "Cost / Pax (€)": "€{:.2f}",
                    "Net / Pax (€)": "€{:+.2f}",
                    "Overall Recovery (%)": "{:.2f}%",
                    "Record Mean Rec (%)": "{:.2f}%",
                    "Record Median Rec (%)": "{:.2f}%",
                }
            ),
            width="stretch",
            hide_index=True,
        )

    # === TAB 4: RELIABILITY, WEATHER & SATISFACTION (FIGURES 4, 5 & 6) ===
    with tab4:
        st.markdown(
            "<div class='note-callout'><strong>Service Reliability, Weather Sensitivity &amp; Non-Causal Satisfaction Association (Figures 4–6):</strong> "
            "Average delay correlates strongly and negatively with customer rating (<em>r</em> = -0.821, <em>R</em>² = 0.674, slope = -0.172★/min). "
            "<strong>Statistical Caveat:</strong> Because the dataset is observational, this correlation does not establish direct causation; "
            "unmeasured operational factors (peak crowding, vehicle age, transfer friction) may jointly influence both delays and satisfaction.</div>",
            unsafe_allow_html=True,
        )

        col_v, col_s = st.columns(2)
        with col_v:
            st.plotly_chart(chart_delay_violin(df_sub), width="stretch")
        with col_s:
            st.plotly_chart(chart_delay_vs_satisfaction_joint(df_sub), width="stretch")

        hm_mode = st.radio(
            "Figure 6 Matrix Metric Toggle:",
            options=["abs", "pct", "ontime"],
            format_func=lambda x: (
                "Absolute Mean Delay (Minutes)"
                if x == "abs"
                else ("Relative Delay Escalation vs Clear Weather (%)" if x == "pct" else "Mean On-Time Performance (%)")
            ),
            horizontal=True,
        )
        st.plotly_chart(chart_weather_mode_heatmap(df_sub, mode_type=hm_mode), width="stretch")

    # === TAB 5: ACCESSIBILITY, CARBON & DATA EXPLORER (FIGURES 7 & 8) ===
    with tab5:
        st.markdown(
            "<div class='note-callout'><strong>Accessibility Normalisation (Figure 7) &amp; Decarbonisation Efficiency (Figure 8):</strong> "
            "Raw complaint counts correlate strongly with passenger volume (<em>r</em> = 0.866), creating exposure bias where high-ridership "
            "Metro appears worst (38,248 raw complaints). Normalising per 10,000 passengers reveals that Metro has the lowest complaint rate "
            "(14.85 / 10k pax), whereas <strong>Suburban Feeder corridors (16.79 / 10k)</strong> and <strong>Suburban E-Scooters (54.02 / 10k)</strong> "
            "exhibit the highest passenger-normalised accessibility friction.</div>",
            unsafe_allow_html=True,
        )

        norm_choice = st.radio(
            "Figure 7 Accessibility Matrix Normalisation Toggle (Exposure Bias Demonstration):",
            options=["weighted", "record_mean", "raw"],
            format_func=lambda x: (
                "Volume-Weighted Rate per 10,000 Passengers (Recommended — Removes Exposure Bias)"
                if x == "weighted"
                else (
                    "Unweighted Record-Mean Rate per 10,000 Passengers"
                    if x == "record_mean"
                    else "Raw Complaint Counts (Confounded by Ridership Volume, r = 0.866)"
                )
            ),
            horizontal=True,
        )

        c_acc, c_carb = st.columns(2)
        with c_acc:
            st.plotly_chart(chart_accessibility_route_mode_heatmap(df_sub, norm_mode=norm_choice), width="stretch")
        with c_carb:
            st.plotly_chart(chart_carbon_efficiency(df_sub), width="stretch")

        st.markdown("#### Interactive Record Browser & CSV Export")
        dl_col1, dl_col2 = st.columns([1, 3])
        with dl_col1:
            csv_bytes = df_sub.to_csv(index=False).encode("utf-8")
            st.download_button(
                label=f"⬇️ Download Filtered Records CSV (n = {len(df_sub):,})",
                data=csv_bytes,
                file_name="ecomove_filtered_slice_25199053.csv",
                mime="text/csv",
                width="stretch",
            )
        st.dataframe(
            df_sub[
                [
                    "Record_ID",
                    "Date_Only",
                    "City",
                    "Country",
                    "Transport_Mode",
                    "Route_Type",
                    "Weather",
                    "Event_Day",
                    "Passengers",
                    "Average_Delay_Minutes",
                    "On_Time_Percentage",
                    "Ticket_Revenue_EUR",
                    "Operating_Cost_EUR",
                    "Net_Margin_EUR",
                    "Cost_Recovery_Pct",
                    "CO2_Saved_KG",
                    "Customer_Rating",
                    "Accessibility_Complaints",
                    "Complaints_per_10k_Pax",
                ]
            ].head(250),
            width="stretch",
            hide_index=True,
        )


if __name__ == "__main__":
    main()
