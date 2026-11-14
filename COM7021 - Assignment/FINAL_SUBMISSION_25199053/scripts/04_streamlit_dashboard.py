import sys
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from style.palette import (
    FONT_FAMILY, GRID, LINE, MIDNIGHT, MIDNIGHT_SOFT, MIST, MUTE, PAPER, TEAL,
    TIFFANY, TIFFANY_DEEP, WHITE,
)

DATA_CSV = ROOT / "data" / "ecomove_cleaned.csv"
C_MODE, C_ROUTE, C_WEATHER = "Transport_Mode", "Route_Type", "Weather"
C_PAX, C_DELAY, C_RATING = "Passengers", "Average_Delay_Minutes", "Customer_Rating"
C_COMP, C_REV, C_COST = "Accessibility_Complaints", "Ticket_Revenue_EUR", "Operating_Cost_EUR"

MODES = ["Metro", "Tram", "Bus", "Park and Ride", "Bike Share", "E-Scooter"]
DELAY_MODES = ["Bus", "Park and Ride", "Tram", "Metro", "E-Scooter", "Bike Share"]
WEATHERS = ["Clear", "Cloudy", "Windy", "Heatwave", "Rain", "Snow"]
ROUTES = ["Suburban Feeder", "Commuter Corridor", "University Area", "Airport Connector", "Central Route", "Tourist Zone"]
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

PRESETS = {
    "1. Full Network Baseline (Fig 9)": ("1. Full Baseline", "Full 12-city network (N = 5,000, 2024–2025).", {}),
    "2. Adverse Weather Surface (Fig 10)": ("2. Rain & Snow", "Surface transit under Rain & Snow (n = 583): delay +69.7%, recovery 113.2%.", {"modes": ["Bus", "Tram", "Park and Ride"], "weathers": ["Rain", "Snow"]}),
    "3. Micromobility Subsidy Audit": ("3. Micromobility", "Shared micromobility (24.64% of records, 1.06% of pax): -€19.98 to -€20.84/pax.", {"modes": ["Bike Share", "E-Scooter"]}),
    "4. Major Event Day Surge": ("4. Event Surge", "Event days (n = 510): +26.2% ridership with +31.0% delay escalation.", {"event": "Yes"}),
    "5. Suburban Accessibility Audit": ("5. Suburban Access", "Suburban Feeder corridors (n = 817): peak 16.79 complaints per 10k pax.", {"routes": ["Suburban Feeder"]}),
    "6. Electric Rail Backbone": ("6. Rail Backbone", "Metro & Tram lines: 78.6% of ridership and 86.7% of CO2 savings.", {"modes": ["Metro", "Tram"]}),
}


@st.cache_data(show_spinner=False)
def load_dataset() -> pd.DataFrame:
    df = pd.read_csv(DATA_CSV, parse_dates=["Date_ISO"])
    df["Date_Only"] = df["Date_ISO"].dt.date
    df["DayOfWeek"] = df["Day_Name"] if "Day_Name" in df.columns else df["Date_ISO"].dt.day_name()
    df["Day_Type"] = df["Is_Weekend"] if "Is_Weekend" in df.columns else np.where(df["Date_ISO"].dt.dayofweek >= 5, "Weekend", "Weekday")
    return df


def compute_metrics(sub: pd.DataFrame, base: pd.DataFrame) -> dict[str, float]:
    n = len(sub)
    if not n:
        return {"n_rec": 0}
    pax, base_pax = float(sub[C_PAX].sum()), float(base[C_PAX].sum())
    rev, cost = float(sub[C_REV].sum()), float(sub[C_COST].sum())
    kwh, co2_kg = float(sub["Energy_Consumption_KWh"].sum()), float(sub["CO2_Saved_KG"].sum())
    comp = int(sub[C_COMP].sum())

    base_co2 = float(base["CO2_Saved_KG"].sum() / base["Energy_Consumption_KWh"].sum())
    base_comp = float(base[C_COMP].sum() / base_pax * 10000.0)
    q1, q3 = sub[C_DELAY].quantile([0.25, 0.75])
    overall_rec = (rev / cost * 100.0) if cost > 0 else 0.0
    co2_kwh = (co2_kg / kwh) if kwh > 0 else 0.0
    w_comp = (comp / pax * 10000.0) if pax > 0 else 0.0

    return {
        "n_rec": n, "rec_share_pct": n / len(base) * 100.0,
        "total_pax": pax, "pax_share_pct": pax / base_pax * 100.0,
        "mean_pax": float(sub[C_PAX].mean()), "median_pax": float(sub[C_PAX].median()),
        "mean_ontime": float(sub["On_Time_Percentage"].mean()),
        "delta_ontime_pp": float(sub["On_Time_Percentage"].mean() - base["On_Time_Percentage"].mean()),
        "mean_delay": float(sub[C_DELAY].mean()), "median_delay": float(sub[C_DELAY].median()),
        "iqr_delay": float(q3 - q1),
        "delta_delay_pct": float((sub[C_DELAY].mean() - base[C_DELAY].mean()) / base[C_DELAY].mean() * 100.0),
        "total_rev": rev, "total_cost": cost, "net_margin": rev - cost,
        "mean_rev_rec": rev / n, "mean_cost_rec": cost / n, "mean_margin_rec": (rev - cost) / n,
        "fare_per_pax": rev / pax if pax > 0 else 0.0, "cost_per_pax": cost / pax if pax > 0 else 0.0,
        "overall_recovery": overall_rec, "record_mean_recovery": float(sub["Cost_Recovery_Pct"].mean()),
        "record_median_recovery": float(sub["Cost_Recovery_Pct"].median()),
        "total_co2_t": co2_kg / 1000.0, "agg_co2_kwh": co2_kwh, "delta_co2_kwh": co2_kwh - base_co2,
        "mean_rating": float(sub[C_RATING].mean()), "delta_rating": float(sub[C_RATING].mean() - base[C_RATING].mean()),
        "weighted_comp_10k": w_comp, "delta_comp_10k": w_comp - base_comp,
    }


def compute_city_table(sub: pd.DataFrame, base: pd.DataFrame) -> pd.DataFrame:
    weights = base[C_MODE].value_counts(normalize=True)
    fallback = base.groupby(C_MODE)["Net_Margin_EUR"].mean()
    piv = sub.pivot_table(index="City", columns=C_MODE, values="Net_Margin_EUR", aggfunc="mean").reindex(columns=weights.index)
    adj_margin = piv.fillna(fallback).mul(weights, axis=1).sum(axis=1)
    micro_share = sub.assign(_m=sub[C_MODE].isin(["Bike Share", "E-Scooter"])).groupby("City")["_m"].mean() * 100.0

    tbl = sub.groupby(["City", "Country"], as_index=False).agg(
        Records=("Record_ID", "count"), Total_Pax=(C_PAX, "sum"), Mean_Delay=(C_DELAY, "mean"),
        On_Time_Pct=("On_Time_Percentage", "mean"), Total_Rev=(C_REV, "sum"),
        Total_Cost=(C_COST, "sum"), Net_Margin=("Net_Margin_EUR", "sum"),
        Raw_Margin_Rec=("Net_Margin_EUR", "mean"), Rec_Mean_Recovery=("Cost_Recovery_Pct", "mean"),
        Mean_Rating=(C_RATING, "mean"), Total_Comp=(C_COMP, "sum"),
    )
    tbl["Overall_Recovery_Pct"] = tbl["Total_Rev"] / tbl["Total_Cost"] * 100.0
    tbl["Mix_Adj_Margin_Rec"] = tbl["City"].map(adj_margin)
    tbl["Micromobility_Share_Pct"] = tbl["City"].map(micro_share)
    tbl["Comp_per_10k_Pax"] = tbl["Total_Comp"] / tbl["Total_Pax"] * 10000.0
    tbl["Raw_Rank"] = tbl["Raw_Margin_Rec"].rank(ascending=False, method="min").astype(int)
    tbl["Adj_Rank"] = tbl["Mix_Adj_Margin_Rec"].rank(ascending=False, method="min").astype(int)
    tbl["Rank_Shift"] = tbl["Raw_Rank"] - tbl["Adj_Rank"]
    return tbl.sort_values("Total_Pax", ascending=False).reset_index(drop=True)


def _theme(
    fig: go.Figure, title: str, subtitle: str = "", h: int = 360, l: int = 60, r: int = 40,
    x_title: str | None = None, y_title: str | None = None, x_range=None, y_range=None,
    x_grid: bool = False, y_grid: bool = True, y_rev: bool = False, show_legend: bool = True,
) -> go.Figure:
    heading = f"{title} — {subtitle}" if subtitle else title
    fig.update_layout(
        title={"text": heading, "font": {"family": FONT_FAMILY, "size": 13.5, "color": MIDNIGHT}, "x": 0.01, "y": 0.95},
        font={"family": FONT_FAMILY, "size": 11.5, "color": MIDNIGHT},
        paper_bgcolor=WHITE, plot_bgcolor=PAPER, height=h, margin={"l": l, "r": r, "t": 58, "b": 44},
        showlegend=show_legend,
        legend={"orientation": "h", "yanchor": "bottom", "y": 1.02, "xanchor": "right", "x": 1.0},
        xaxis={"title": x_title, "range": x_range, "showgrid": x_grid, "gridcolor": GRID, "linecolor": LINE, "tickfont": {"color": MUTE, "size": 10.5}},
        yaxis={"title": y_title, "range": y_range, "showgrid": y_grid, "gridcolor": GRID, "linecolor": LINE, "autorange": "reversed" if y_rev else True, "tickfont": {"color": MUTE, "size": 10.5}},
    )
    return fig


def _render_panel(col, fig: go.Figure, note: str | None = None) -> None:
    with col, st.container(border=True):
        if note:
            st.caption(note)
        st.plotly_chart(fig, width="stretch")


def chart_monthly_trend(sub: pd.DataFrame, h: int = 340) -> go.Figure:
    fig = go.Figure()
    if sub["Day_Type"].nunique() > 1:
        for label, col, dash in (("Weekday", MIDNIGHT, None), ("Weekend", TEAL, "dot")):
            g = sub[sub["Day_Type"] == label].groupby("YearMonth", as_index=False)[C_PAX].mean().sort_values("YearMonth")
            fig.add_trace(go.Scatter(x=g["YearMonth"], y=g[C_PAX].round(0), mode="lines+markers", name=f"{label} Service", line={"color": col, "width": 2.4, "dash": dash}))
    else:
        g = sub.groupby("YearMonth", as_index=False)[C_PAX].mean().sort_values("YearMonth")
        fig.add_trace(go.Scatter(x=g["YearMonth"], y=g[C_PAX].round(0), mode="lines+markers", name="Mean Demand", line={"color": MIDNIGHT, "width": 2.4}))
    avg = float(sub[C_PAX].mean())
    fig.add_hline(y=avg, line_dash="dash", line_color=MUTE, annotation_text=f"Mean: {avg:,.0f}")
    return _theme(fig, "Monthly Demand Trajectory (2024–2025)", "Weekday commute vs Weekend regime", h=h, y_title="Mean Passengers / Record")


def chart_mode_recovery(sub: pd.DataFrame, h: int = 340) -> go.Figure:
    g = sub.groupby(C_MODE, as_index=False).agg(Rev=(C_REV, "sum"), Cost=(C_COST, "sum"))
    g["Rec"] = np.where(g["Cost"] > 0, g["Rev"] / g["Cost"] * 100.0, 0.0)
    g = g.sort_values("Rec")
    fig = go.Figure(go.Bar(x=g["Rec"].round(1), y=g[C_MODE], orientation="h", marker_color=[TIFFANY if v < 100 else MIDNIGHT_SOFT for v in g["Rec"]], text=[f"{v:.1f}%" for v in g["Rec"]], textposition="outside"))
    fig.add_vline(x=100.0, line_dash="dash", line_color=MIDNIGHT, annotation_text="100% Break-Even")
    hi = max(float(g["Rec"].max()) * 1.24, 130.0) if len(g) else 135.0
    return _theme(fig, "Cost Recovery Ratio (%) by Mode", "Cumulative Revenue ÷ Cost", h=h, l=105, r=55, x_title="Overall Cost Recovery (%)", x_range=[0, hi], x_grid=True, y_grid=False)


def chart_weather_delay(sub: pd.DataFrame, h: int = 340) -> go.Figure:
    g = sub.groupby(C_WEATHER, as_index=False)[C_DELAY].mean().set_index(C_WEATHER).reindex([w for w in WEATHERS if w in sub[C_WEATHER].unique()]).reset_index()
    fig = go.Figure(go.Bar(x=g[C_WEATHER], y=g[C_DELAY].round(2), marker_color=[TIFFANY if w in ("Rain", "Snow") else MIDNIGHT_SOFT for w in g[C_WEATHER]], text=[f"{v:.2f}m" for v in g[C_DELAY]], textposition="outside"))
    hi = max(float(g[C_DELAY].max()) * 1.25, 6.0) if len(g) else 9.5
    return _theme(fig, "Mean Delay (min) by Weather", "Snow & Rain trigger surface delay surges", h=h, y_title="Mean Delay (min)", y_range=[0, hi])


def chart_route_complaints(sub: pd.DataFrame, metric_mode: str = "weighted", h: int = 340) -> go.Figure:
    g = sub.groupby(C_ROUTE, as_index=False).agg(Comp=(C_COMP, "sum"), Pax=(C_PAX, "sum"), Rec_Rate=("Complaints_per_10k_Pax", "mean"))
    g["Weighted_Rate"] = np.where(g["Pax"] > 0, g["Comp"] / g["Pax"] * 10000.0, 0.0)
    col, xlabel, fmt = {"raw": ("Comp", "Total Raw Complaints", "{:,.0f}"), "record_mean": ("Rec_Rate", "Record-Mean Rate / 10k", "{:.2f}")}.get(metric_mode, ("Weighted_Rate", "Complaints per 10,000 Pax", "{:.2f}"))
    g = g.sort_values(col)
    top_v = float(g[col].max()) if len(g) else 1.0
    fig = go.Figure(go.Bar(x=g[col], y=g[C_ROUTE], orientation="h", marker_color=[TIFFANY if v == top_v else MIDNIGHT_SOFT for v in g[col]], text=[fmt.format(v) for v in g[col]], textposition="outside"))
    return _theme(fig, "Accessibility Complaint Intensity by Route", xlabel, h=h, l=130, r=55, x_title=xlabel, x_range=[0, top_v * 1.24 if top_v > 0 else 20], x_grid=True, y_grid=False)


def chart_modal_share_discrepancy(sub: pd.DataFrame) -> go.Figure:
    g = sub.groupby(C_MODE, as_index=False).agg(Records=("Record_ID", "count"), Pax=(C_PAX, "sum"), Cost=(C_COST, "sum"))
    for k, col in (("Record_Share", "Records"), ("Pax_Share", "Pax"), ("Cost_Share", "Cost")):
        g[k] = g[col] / max(g[col].sum(), 1) * 100.0
    g = g.set_index(C_MODE).reindex([m for m in MODES if m in g[C_MODE].values]).reset_index()
    fig = go.Figure()
    for name, col, tint in (("Record Share (%)", "Record_Share", MUTE), ("Passenger Share (%)", "Pax_Share", MIDNIGHT), ("Cost Share (%)", "Cost_Share", TIFFANY_DEEP)):
        fig.add_trace(go.Bar(name=name, x=g[C_MODE], y=g[col].round(1), marker_color=tint, text=[f"{v:.1f}%" for v in g[col]], textposition="outside"))
    hi = max(float(g[["Record_Share", "Pax_Share", "Cost_Share"]].max().max()) * 1.24, 30.0) if len(g) else 75.0
    fig.update_layout(barmode="group")
    return _theme(fig, "Compositional Discrepancy: Record vs Ridership vs Cost Share", "Explains 84.12% vs 99.58% recovery gap", h=370, y_title="Share (%)", y_range=[0, hi])


def chart_simpsons_paradox_dumbbell(cdf: pd.DataFrame) -> go.Figure:
    d = cdf.sort_values("Raw_Margin_Rec").reset_index(drop=True)
    fig = go.Figure()
    for r in d.itertuples():
        fig.add_trace(go.Scatter(x=[r.Raw_Margin_Rec, r.Mix_Adj_Margin_Rec], y=[r.City, r.City], mode="lines", line={"color": LINE, "width": 3.0}, showlegend=False, hoverinfo="skip"))
    fig.add_trace(go.Scatter(x=d["Raw_Margin_Rec"].round(2), y=d["City"], mode="markers+text", name="Raw Mean (€/rec)", marker={"color": MIDNIGHT, "size": 10}, text=[f"#{r}" for r in d["Raw_Rank"]], textposition="middle left"))
    fig.add_trace(go.Scatter(x=d["Mix_Adj_Margin_Rec"].round(2), y=d["City"], mode="markers+text", name="Mix-Adjusted (€/rec)", marker={"color": TIFFANY, "size": 11, "symbol": "diamond", "line": {"color": MIDNIGHT, "width": 1.1}}, text=[f"#{r}" for r in d["Adj_Rank"]], textposition="middle right"))
    fig.add_vline(x=0.0, line_dash="dash", line_color=MIDNIGHT, annotation_text="Break-Even (€0)")
    return _theme(fig, "Figure 2 — Simpson's Paradox in City Financial Rankings", "Raw vs direct modal-mix standardised margin", h=410, l=95, x_title="Mean Net Margin (€ / Record)", x_grid=True, y_grid=False)


def chart_unit_economics(sub: pd.DataFrame) -> go.Figure:
    g = sub.groupby(C_MODE, as_index=False).agg(Rev=(C_REV, "sum"), Cost=(C_COST, "sum"), Pax=(C_PAX, "sum"), CO2=("CO2_Saved_KG", "sum"))
    g["Fare"] = np.where(g["Pax"] > 0, g["Rev"] / g["Pax"], 0.0)
    g["UnitCost"] = np.where(g["Pax"] > 0, g["Cost"] / g["Pax"], 0.0)
    g["CO2_Ret"] = np.where(g["CO2"] > 0, (g["Rev"] - g["Cost"]) / (g["CO2"] / 1000.0), 0.0)
    g = g.set_index(C_MODE).reindex([m for m in MODES if m in g[C_MODE].values]).reset_index()

    fig = make_subplots(rows=1, cols=2, subplot_titles=("Fare vs Cost / Pax (€)", "Net Return / tCO2 (€)"), horizontal_spacing=0.18)
    fig.add_trace(go.Bar(y=g[C_MODE], x=g["Fare"].round(2), orientation="h", name="Fare (€/pax)", marker_color=MIDNIGHT, text=[f"€{v:.2f}" for v in g["Fare"]], textposition="outside"), row=1, col=1)
    fig.add_trace(go.Bar(y=g[C_MODE], x=g["UnitCost"].round(2), orientation="h", name="Cost (€/pax)", marker_color=TIFFANY, text=[f"€{v:.2f}" for v in g["UnitCost"]], textposition="outside"), row=1, col=1)
    fig.add_trace(go.Bar(y=g[C_MODE], x=g["CO2_Ret"].round(0), orientation="h", showlegend=False, marker_color=[MIDNIGHT_SOFT if v >= 0 else TIFFANY for v in g["CO2_Ret"]], text=[f"€{v:,.0f}/t" for v in g["CO2_Ret"]], textposition="outside"), row=1, col=2)
    _theme(fig, "Figure 3 — Unit Economics & Carbon Abatement Return", "Transit cross-subsidises micromobility", h=410, l=100, r=60)
    fig.update_layout(barmode="group", xaxis={"title": "€ / Passenger", "range": [0, 29], "showgrid": True, "gridcolor": GRID}, xaxis2={"title": "€ / tCO2", "range": [min(float(g["CO2_Ret"].min()) * 1.3, -1000.0) if len(g) else -120000.0, max(float(g["CO2_Ret"].max()) * 1.35, 5000.0) if len(g) else 15000.0], "showgrid": True, "gridcolor": GRID})
    return fig


def chart_delay_violin(sub: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    for m in [x for x in DELAY_MODES if x in sub[C_MODE].unique()]:
        vals = sub.loc[sub[C_MODE] == m, C_DELAY]
        col = TIFFANY if m == "Bus" else (TIFFANY_DEEP if m in ("Tram", "Park and Ride") else MIDNIGHT_SOFT)
        fig.add_trace(go.Violin(x=vals, y=[m] * len(vals), name=m, orientation="h", box_visible=True, meanline_visible=True, fillcolor=col, line_color=MIDNIGHT, points=False))
    return _theme(fig, "Figure 4 — Delay Distribution by Mode", "Bus shows widest dispersion (6.58m mean)", h=380, l=105, x_title="Average Delay (min)", x_grid=True, y_grid=False, show_legend=False)


def chart_delay_vs_satisfaction_joint(sub: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    ok = len(sub) > 1 and sub[C_DELAY].std() > 0
    r_val = float(sub[C_DELAY].corr(sub[C_RATING])) if ok else 0.0
    slope, intercept = np.polyfit(sub[C_DELAY], sub[C_RATING], 1) if ok else (0.0, 4.0)

    for ev, label, col, sz in (("No", "Standard Day", MIDNIGHT_SOFT, 5.5), ("Yes", "Event Day", TIFFANY, 7.5)):
        s = sub[sub["Event_Day"] == ev]
        if not s.empty:
            fig.add_trace(go.Scattergl(x=s[C_DELAY], y=s[C_RATING], mode="markers", name=f"{label} (n={len(s):,})", marker={"color": col, "size": sz, "opacity": 0.65}))
    if len(sub) > 1:
        xl = np.linspace(float(sub[C_DELAY].min()), float(sub[C_DELAY].max()), 50)
        fig.add_trace(go.Scatter(x=xl, y=slope * xl + intercept, mode="lines", name=f"OLS (r={r_val:.3f})", line={"color": MIDNIGHT, "width": 2.4}))
    fig.add_vline(x=6.0, line_dash="dot", line_color=TIFFANY_DEEP, annotation_text="6.0m Threshold")
    fig.add_hline(y=3.5, line_dash="dot", line_color=MUTE, annotation_text="3.5★ Floor")
    return _theme(fig, f"Figure 5 — Delay vs Customer Rating (r = {r_val:.3f})", f"OLS slope {slope:.3f} pts/min (observational)", h=380, x_title="Average Delay (min)", y_title="Customer Rating (1–5)", y_range=[0.8, 5.2], x_grid=True)


def chart_weather_mode_heatmap(sub: pd.DataFrame, metric: str = "abs") -> go.Figure:
    p_d = sub.pivot_table(index=C_MODE, columns=C_WEATHER, values=C_DELAY, aggfunc="mean")
    p_o = sub.pivot_table(index=C_MODE, columns=C_WEATHER, values="On_Time_Percentage", aggfunc="mean")
    rows = [m for m in DELAY_MODES if m in p_d.index]
    cols = [w for w in WEATHERS if w in p_d.columns]
    p_d, p_o = p_d.reindex(index=rows, columns=cols), p_o.reindex(index=rows, columns=cols)

    if metric == "pct" and "Clear" in p_d.columns:
        z, fmt, title, ctitle = p_d.divide(p_d["Clear"].replace(0, np.nan), axis=0).sub(1.0).mul(100.0), "{:+.0f}%", "Figure 6 — Delay Escalation (%) vs Clear", "Δ% vs Clear"
    elif metric == "ontime":
        z, fmt, title, ctitle = p_o, "{:.1f}%", "Figure 6 — Mean On-Time Performance (%)", "On-Time %"
    else:
        z, fmt, title, ctitle = p_d, "{:.2f}m", "Figure 6 — Mean Delay (min) across Weather × Mode", "Delay (min)"

    txt = [[fmt.format(v) if pd.notna(v) else "-" for v in row] for row in z.values]
    fig = go.Figure(go.Heatmap(z=z.values, x=cols, y=rows, text=txt, texttemplate="%{text}", colorscale=[[0.0, MIST], [0.5, TIFFANY], [1.0, MIDNIGHT]], colorbar={"title": ctitle}))
    return _theme(fig, title, "Surface modes spike under Snow and Rain", h=380, l=105, y_grid=False, y_rev=True, show_legend=False)


def chart_accessibility_route_mode_heatmap(sub: pd.DataFrame, norm_mode: str = "weighted") -> go.Figure:
    rows = [r for r in ROUTES if r in sub[C_ROUTE].unique()]
    cols = [m for m in MODES if m in sub[C_MODE].unique()]
    if norm_mode == "raw":
        piv = sub.pivot_table(index=C_ROUTE, columns=C_MODE, values=C_COMP, aggfunc="sum").reindex(index=rows, columns=cols)
        fmt, title, ctitle = "{:,.0f}", "Figure 7 — Raw Accessibility Complaints (r = 0.866 with volume)", "Raw Count"
    elif norm_mode == "record_mean":
        piv = sub.pivot_table(index=C_ROUTE, columns=C_MODE, values="Complaints_per_10k_Pax", aggfunc="mean").reindex(index=rows, columns=cols)
        fmt, title, ctitle = "{:.1f}", "Figure 7 — Record-Mean Complaints / 10k Pax", "Mean / 10k"
    else:
        c_p = sub.pivot_table(index=C_ROUTE, columns=C_MODE, values=C_COMP, aggfunc="sum").reindex(index=rows, columns=cols)
        p_p = sub.pivot_table(index=C_ROUTE, columns=C_MODE, values=C_PAX, aggfunc="sum").reindex(index=rows, columns=cols)
        piv = (c_p / p_p.replace(0, np.nan)) * 10000.0
        fmt, title, ctitle = "{:.1f}", "Figure 7 — Weighted Complaints / 10k Pax", "Rate / 10k"

    txt = [[fmt.format(v) if pd.notna(v) else "-" for v in row] for row in piv.values]
    fig = go.Figure(go.Heatmap(z=piv.values, x=cols, y=rows, text=txt, texttemplate="%{text}", colorscale=[[0.0, MIST], [0.45, TIFFANY], [1.0, MIDNIGHT]], colorbar={"title": ctitle}))
    return _theme(fig, title, "Isolates Suburban Feeder micromobility friction", h=380, l=130, y_grid=False, y_rev=True, show_legend=False)


def chart_carbon_efficiency(sub: pd.DataFrame) -> go.Figure:
    g = sub.groupby(C_MODE, as_index=False).agg(CO2=("CO2_Saved_KG", "sum"), KWh=("Energy_Consumption_KWh", "sum"), Pax=(C_PAX, "sum"))
    g["CO2_kWh"] = np.where(g["KWh"] > 0, g["CO2"] / g["KWh"], 0.0)
    g["kWh_Pax"] = np.where(g["Pax"] > 0, g["KWh"] / g["Pax"], 0.0)
    g["Tonnes"] = g["CO2"] / 1000.0

    fig = go.Figure()
    for r in g.itertuples():
        col = TIFFANY if r.Transport_Mode in ("Metro", "Tram") else (MUTE if r.Transport_Mode == "Bus" else MIDNIGHT_SOFT)
        sz = max(min(np.sqrt(r.Tonnes) * 1.15, 54.0), 18.0)
        fig.add_trace(go.Scatter(x=[r.kWh_Pax], y=[r.CO2_kWh], mode="markers+text", name=r.Transport_Mode, text=[f"{r.Transport_Mode} ({r.CO2_kWh:.2f})"], textposition="top center", marker={"size": sz, "color": col, "opacity": 0.88, "line": {"color": MIDNIGHT, "width": 1.4}}))
    return _theme(fig, "Figure 8 — Carbon Efficiency (kg CO2 / kWh) vs Energy Intensity", "Bubble area reflects total tonnes saved", h=380, x_title="Energy / Passenger (kWh / Pax)", y_title="kg CO2 Saved per kWh", x_grid=True, y_range=[0.5, 4.3], show_legend=False)


def _col_cfg(specs):
    cc = st.column_config
    builders = {
        "prog": lambda t, f, lo, hi: cc.ProgressColumn(t, format=f, min_value=lo, max_value=hi),
        "num": lambda t, f, lo, hi: cc.NumberColumn(t, format=f),
        "txt": lambda t, f, lo, hi: cc.TextColumn(t, width="small"),
    }
    return {key: builders[kind](title, fmt, lo, hi) for key, kind, title, fmt, lo, hi in specs}


def _apply_preset(key):
    st.session_state["active_preset"] = key
    if key in PRESETS:
        filters = PRESETS[key][2]
        st.session_state["f_countries"] = []
        st.session_state["f_cities"] = []
        st.session_state["f_modes"] = list(filters.get("modes", []))
        st.session_state["f_routes"] = list(filters.get("routes", []))
        st.session_state["f_weathers"] = list(filters.get("weathers", []))
        st.session_state["f_event"] = filters.get("event", "All")
        st.session_state["f_regime"] = filters.get("regime", "All Days")


def main():
    st.set_page_config(page_title="EcoMove Mobility — Executive Dashboard (25199053)", layout="wide", initial_sidebar_state="expanded")
    df_base = load_dataset()
    preset_keys = list(PRESETS) + ["7. Custom Filter Exploration"]
    if "active_preset" not in st.session_state:
        _apply_preset(preset_keys[0])

    min_d, max_d = df_base["Date_Only"].min(), df_base["Date_Only"].max()
    with st.sidebar:
        st.subheader("Filter & Scenario Console")
        st.caption("COM7021 · Student ID: 25199053")
        st.button("Reset to Baseline", width="stretch", on_click=_apply_preset, args=(preset_keys[0],))
        chosen = st.selectbox("Scenario Preset", options=preset_keys, key="active_preset", on_change=lambda: _apply_preset(st.session_state["active_preset"]))
        with st.expander("Geography & Mode", expanded=True):
            countries = st.multiselect("Country", sorted(df_base["Country"].unique()), key="f_countries")
            city_pool = sorted(df_base[df_base["Country"].isin(countries)]["City"].unique()) if countries else sorted(df_base["City"].unique())
            st.session_state["f_cities"] = [c for c in st.session_state.get("f_cities", []) if c in city_pool]
            cities = st.multiselect("City", city_pool, key="f_cities")
            modes = st.multiselect("Transport Mode", [m for m in MODES if m in df_base[C_MODE].unique()], key="f_modes")
            routes = st.multiselect("Route Type", sorted(df_base[C_ROUTE].unique()), key="f_routes")
        with st.expander("Weather, Events & Calendar", expanded=True):
            weathers = st.multiselect("Weather", [w for w in WEATHERS if w in df_base[C_WEATHER].unique()], key="f_weathers")
            ev = st.selectbox("Event Day", ["All", "No", "Yes"], key="f_event")
            regime = st.selectbox("Day Regime", ["All Days", "Weekday", "Weekend"], key="f_regime")
            dates = st.date_input("Date Window", value=(min_d, max_d), min_value=min_d, max_value=max_d, key="f_dates")

    mask = pd.Series(True, index=df_base.index)
    if len(dates) == 2:
        mask &= (df_base["Date_Only"] >= dates[0]) & (df_base["Date_Only"] <= dates[1])
    if regime != "All Days":
        mask &= df_base["Day_Type"] == regime
    if ev != "All":
        mask &= df_base["Event_Day"] == ev
    for col, vals in (("Country", countries), ("City", cities), (C_MODE, modes), (C_ROUTE, routes), (C_WEATHER, weathers)):
        if vals:
            mask &= df_base[col].isin(vals)
    df_sub = df_base[mask].copy()

    st.title("EcoMove Mobility — Executive Decision Dashboard")
    st.caption("European Urban Mobility Network (12 Cities · 6 Countries · 2024–2025) · COM7021 ID: 25199053")

    for col, (i, pk) in zip(st.columns(6), enumerate(PRESETS)):
        with col:
            st.button(PRESETS[pk][0], key=f"pbtn_{i}", type="primary" if chosen == pk else "secondary", width="stretch", help=PRESETS[pk][1], on_click=_apply_preset, args=(pk,))

    if df_sub.empty:
        st.warning("No records match the active filter combination.")
        return

    m = compute_metrics(df_sub, df_base)
    city_tbl = compute_city_table(df_sub, df_base)
    st.info(f"**Active View:** {PRESETS[chosen][1] if chosen in PRESETS else 'Custom filter slice.'} — `{m['n_rec']:,}` / 5,000 records ({m['rec_share_pct']:.1f}%), `{m['total_pax']/1e6:.2f}M` pax ({m['pax_share_pct']:.1f}%).")

    kpi_specs = [
        ("Ridership", f"{m['total_pax']/1e6:.2f}M", f"Mean {m['mean_pax']:,.0f}/rec"),
        ("On-Time Rate", f"{m['mean_ontime']:.1f}%", f"{m['delta_ontime_pp']:+.1f}pp vs base"),
        ("Mean Delay", f"{m['mean_delay']:.2f} min", f"{m['delta_delay_pct']:+.1f}% vs base"),
        ("Cost Recovery", f"{m['overall_recovery']:.1f}%", f"Rec mean {m['record_mean_recovery']:.1f}%"),
        ("CO2 Saved", f"{m['total_co2_t']:,.1f} t", f"{m['agg_co2_kwh']:.2f} kg/kWh"),
        ("Customer Rating", f"{m['mean_rating']:.2f} / 5", f"{m['weighted_comp_10k']:.2f} comp/10k"),
    ]
    for col, (lbl, val, delta) in zip(st.columns(6), kpi_specs):
        with col, st.container(border=True):
            st.metric(lbl, val, delta)

    tabs = st.tabs([
        "1. Overview (Figs 9–10)", "2. Demand & Regimes (Fig 1)", "3. Financials & Simpson's Paradox (Figs 2–3)",
        "4. Reliability & Weather (Figs 4–6)", "5. Accessibility, Carbon & Data (Figs 7–8)",
    ])

    with tabs[0]:
        for fig_a, fig_b in ((chart_monthly_trend(df_sub), chart_mode_recovery(df_sub)), (chart_weather_delay(df_sub), chart_route_complaints(df_sub))):
            c1, c2 = st.columns(2)
            _render_panel(c1, fig_a)
            _render_panel(c2, fig_b)

        with st.container(border=True):
            st.subheader("12-City Scorecard (Mix-Adjusted Margins)")
            cols = ["City", "Country", "Records", "Total_Pax", "Mean_Delay", "On_Time_Pct", "Overall_Recovery_Pct", "Rec_Mean_Recovery", "Net_Margin", "Raw_Margin_Rec", "Mix_Adj_Margin_Rec", "Mean_Rating", "Comp_per_10k_Pax"]
            st.dataframe(city_tbl[cols], column_config=_col_cfg([
                ("City", "txt", "City", None, None, None), ("Country", "txt", "Country", None, None, None),
                ("Records", "num", "Records", "%d", None, None), ("Total_Pax", "num", "Passengers", "%d", None, None),
                ("Mean_Delay", "num", "Delay (m)", "%.2f m", None, None), ("On_Time_Pct", "prog", "On-Time", "%.1f%%", 50.0, 100.0),
                ("Overall_Recovery_Pct", "prog", "Recovery", "%.1f%%", 0.0, 130.0), ("Rec_Mean_Recovery", "num", "Rec Mean", "%.1f%%", None, None),
                ("Net_Margin", "num", "Net Margin", "€%.0f", None, None), ("Raw_Margin_Rec", "num", "Raw /rec", "€%.2f", None, None),
                ("Mix_Adj_Margin_Rec", "num", "Mix-Adj /rec", "€%.2f", None, None), ("Mean_Rating", "prog", "Rating", "%.2f / 5", 1.0, 5.0),
                ("Comp_per_10k_Pax", "num", "Comp / 10k", "%.2f", None, None),
            ]), width="stretch", hide_index=True)

    with tabs[1]:
        c1, c2 = st.columns([1.1, 1.0])
        _render_panel(c1, chart_monthly_trend(df_sub, h=370), "Weekdays show a +34.1% commute premium; the October trough (-27.2%) is ideal for maintenance.")
        _render_panel(c2, chart_modal_share_discrepancy(df_sub), "Metro carries 62.96% of passengers on 20.94% of records; shared micromobility carries 1.06%.")

        with st.container(border=True):
            st.subheader("Day-of-Week Regime Profile")
            dow = df_sub.groupby(["DayOfWeek", "Day_Type"], as_index=False).agg(Records=("Record_ID", "count"), Total_Pax=(C_PAX, "sum"), Mean_Pax=(C_PAX, "mean"), Mean_Delay=(C_DELAY, "mean"), Rev=(C_REV, "sum"), Cost=(C_COST, "sum"))
            dow["Overall_Rec"] = np.where(dow["Cost"] > 0, dow["Rev"] / dow["Cost"] * 100.0, 0.0)
            dow["Ord"] = dow["DayOfWeek"].apply(lambda x: DAYS.index(x) if x in DAYS else 99)
            dow = dow.sort_values("Ord").drop(columns=["Ord", "Rev", "Cost"])
            st.dataframe(dow, column_config=_col_cfg([
                ("DayOfWeek", "txt", "Day", None, None, None), ("Day_Type", "txt", "Regime", None, None, None),
                ("Records", "num", "Records", "%d", None, None), ("Total_Pax", "num", "Passengers", "%d", None, None),
                ("Mean_Pax", "prog", "Mean Pax", "%.0f", 0.0, 11000.0), ("Mean_Delay", "num", "Delay", "%.2f m", None, None),
                ("Overall_Rec", "prog", "Recovery", "%.1f%%", 0.0, 120.0),
            ]), width="stretch", hide_index=True)

    with tabs[2]:
        f1, f2 = st.columns([1.0, 1.15])
        _render_panel(f1, chart_simpsons_paradox_dumbbell(city_tbl), "Simpson's Paradox: mix standardisation shifts Berlin from Rank #4 to #11.")
        _render_panel(f2, chart_unit_economics(df_sub), "Park & Ride (121.5%), Tram (117.3%), and Metro (106.2%) cross-subsidise micromobility.")

        with st.container(border=True):
            st.subheader("Reconciled Modal Financial Ledger")
            mfin = df_sub.groupby(C_MODE, as_index=False).agg(Records=("Record_ID", "count"), Passengers=(C_PAX, "sum"), Total_Rev=(C_REV, "sum"), Total_Cost=(C_COST, "sum"), Total_Net=("Net_Margin_EUR", "sum"), Net_per_Rec=("Net_Margin_EUR", "mean"), Unweighted_Rec=("Cost_Recovery_Pct", "mean"))
            mfin["Weighted_Rec"] = np.where(mfin["Total_Cost"] > 0, mfin["Total_Rev"] / mfin["Total_Cost"] * 100.0, 0.0)
            mfin["Net_per_Pax"] = np.where(mfin[C_PAX] > 0, mfin["Total_Net"] / mfin[C_PAX], 0.0)
            mfin = mfin.set_index(C_MODE).reindex([x for x in MODES if x in mfin[C_MODE].values]).reset_index()
            st.dataframe(mfin, column_config=_col_cfg([
                (C_MODE, "txt", "Mode", None, None, None), ("Records", "num", "Records", "%d", None, None),
                (C_PAX, "num", "Passengers", "%d", None, None), ("Total_Rev", "num", "Revenue", "€%.0f", None, None),
                ("Total_Cost", "num", "Cost", "€%.0f", None, None), ("Total_Net", "num", "Net Margin", "€%.0f", None, None),
                ("Net_per_Rec", "num", "Net / rec", "€%.2f", None, None), ("Net_per_Pax", "num", "Net / pax", "€%+.2f", None, None),
                ("Weighted_Rec", "prog", "Weighted Rec", "%.2f%%", 0.0, 130.0), ("Unweighted_Rec", "num", "Rec Mean", "%.2f%%", None, None),
            ]), width="stretch", hide_index=True)

    with tabs[3]:
        c_v, c_s = st.columns(2)
        _render_panel(c_v, chart_delay_violin(df_sub), "Bus shows the highest mean delay (6.58m) vs grade-separated Metro (3.73m).")
        _render_panel(c_s, chart_delay_vs_satisfaction_joint(df_sub), "Delay and customer rating correlate strongly (r = -0.821).")

        with st.container(border=True):
            hm_map = {"abs": "Mean Delay (min)", "pct": "Delta % vs Clear", "ontime": "On-Time Rate (%)"}
            hm_choice = st.radio("Heatmap Metric:", options=list(hm_map), format_func=hm_map.get, horizontal=True)
            st.plotly_chart(chart_weather_mode_heatmap(df_sub, metric=hm_choice), width="stretch")

    with tabs[4]:
        with st.container(border=True):
            norm_map = {"weighted": "Weighted Rate / 10k Pax", "record_mean": "Record-Mean / 10k Pax", "raw": "Raw Counts (Volume Confounded)"}
            norm_choice = st.radio("Accessibility Normalisation:", options=list(norm_map), format_func=norm_map.get, horizontal=True)
            ca, cb = st.columns(2)
            ca.plotly_chart(chart_accessibility_route_mode_heatmap(df_sub, norm_mode=norm_choice), width="stretch")
            cb.plotly_chart(chart_carbon_efficiency(df_sub), width="stretch")

        with st.container(border=True):
            d1, d2 = st.columns([2.2, 1.0])
            d1.subheader(f"Record Explorer (top 200 of {len(df_sub):,} rows)")
            d2.download_button(f"Export CSV ({len(df_sub):,} rows)", data=df_sub.to_csv(index=False).encode("utf-8"), file_name="ecomove_filtered_25199053.csv", mime="text/csv", width="stretch")
            skip = {"Date", "Date_ISO", "Year", "Month", "Month_Name", "YearMonth", "Day_Name", "Is_Weekend", "DayOfWeek", "Day_Type"}
            show_cols = [c for c in df_sub.columns if c not in skip]
            st.dataframe(df_sub[show_cols].head(200), width="stretch", hide_index=True)


if __name__ == "__main__":
    main()
