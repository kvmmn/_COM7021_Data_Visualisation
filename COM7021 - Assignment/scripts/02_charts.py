#!/usr/bin/env python3
"""Step 2: Generate Advanced Data-Science Visualisations (Figures 1 to 7) using Matplotlib.
Strictly follows COM7021 - Assignment/VISUAL_DESIGN_GUIDE.md (Arden Midnight / Tiffany palette).
Incorporates First-Principles statistical decompositions:
- Fig 1: Seasonal Regime & Structural Weekday Premium Ribbon (Time-Series Decomposition)
- Fig 2: Simpson's Paradox Connected Dumbbell Plot (Raw vs Modal-Mix-Adjusted City Margin)
- Fig 3: Two-Panel Unit Economics & Marginal Carbon Abatement Return (OLS Cost Slope & € / tCO2)
- Fig 4: Raincloud Plot (Half-Violin KDE Density + Tukey Boxplot + Jittered Quantile Strip)
- Fig 5: Joint Bivariate OLS & Marginal KDE Density Plot (Delay vs Rating by Event Status)
- Fig 6: Dual-Encoded Weather x Mode Interaction Heatmap (Mean Delay & % Surge vs Clear)
- Fig 7: Multi-Layer Accessibility Interaction Matrix (Route x Mode Complaints per 10k Pax)
"""

from __future__ import annotations

import sys
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.gridspec import GridSpec

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from style.palette import (
    MIDNIGHT,
    TIFFANY,
    TIFFANY_DEEP,
    MIDNIGHT_SOFT,
    TEAL,
    MIST,
    PAPER,
    MUTE,
    GRID,
    WHITE,
    ARDEN_CMAP,
    apply_rcparams,
    style_axes,
    save,
)

DATA_CSV = BASE_DIR / "data" / "ecomove_cleaned.csv"
TABLES_DIR = BASE_DIR / "output" / "tables"
FIG_DIR = BASE_DIR / "output" / "figures"


def gaussian_kde_1d(values: np.ndarray, grid: np.ndarray, bw_factor: float = 1.0) -> np.ndarray:
    """Compute smooth 1D Gaussian KDE using Silverman's rule of thumb (pure NumPy)."""
    x = np.asarray(values, dtype=float)
    n = len(x)
    std = np.std(x, ddof=1)
    iqr = np.percentile(x, 75) - np.percentile(x, 25)
    sigma = min(std, iqr / 1.34) if iqr > 0 else std
    bw = 0.9 * sigma * (n ** (-0.2)) * bw_factor
    bw = max(bw, 1e-3)
    diffs = (grid[:, None] - x[None, :]) / bw
    dens = np.exp(-0.5 * (diffs**2)).sum(axis=1) / (n * bw * np.sqrt(2 * np.pi))
    return dens


def load_data() -> pd.DataFrame:
    return pd.read_csv(DATA_CSV, parse_dates=["Date_ISO"])


def fig01_monthly_demand_trend(df: pd.DataFrame) -> Path:
    """Fig 1: Seasonal Regime Decomposition — Weekday vs Weekend with Structural Premium Ribbon."""
    apply_rcparams()
    fig, ax = plt.subplots(figsize=(10.5, 5.2))
    style_axes(ax, grid_axis="y")

    monthly = (
        df.groupby(["YearMonth", "Is_Weekend"], as_index=False)["Passengers"]
        .mean()
        .assign(YM_Date=lambda d: pd.to_datetime(d["YearMonth"] + "-01"))
        .sort_values("YM_Date")
    )
    piv = monthly.pivot(index="YM_Date", columns="Is_Weekend", values="Passengers").sort_index()
    dates = piv.index
    wkday = piv["Weekday"].values
    wkend = piv["Weekend"].values

    # Highlight Spring Peak windows (Feb-Apr 2024 and Feb-Apr 2025)
    ax.axvspan(pd.Timestamp("2024-02-18"), pd.Timestamp("2024-04-15"), color=TIFFANY, alpha=0.14, zorder=0)
    ax.axvspan(pd.Timestamp("2025-02-18"), pd.Timestamp("2025-04-15"), color=TIFFANY, alpha=0.14, zorder=0)

    # Shaded structural weekday-over-weekend commute premium ribbon
    ax.fill_between(
        dates,
        wkend,
        wkday,
        color=MIST,
        alpha=0.85,
        label="Weekday commute premium (+34.1% mean)",
        zorder=1,
    )

    ax.plot(
        dates,
        wkday,
        color=MIDNIGHT,
        linewidth=2.5,
        solid_capstyle="round",
        label="Weekday service (mean 8,803 pax)",
        zorder=3,
    )
    ax.plot(
        dates,
        wkend,
        color=TEAL,
        linewidth=2.2,
        linestyle="--",
        solid_capstyle="round",
        label="Weekend service (mean 6,563 pax)",
        zorder=3,
    )

    # Mark seasonal extremes on the primary Weekday series
    ext_dates = [
        pd.Timestamp("2024-03-01"),
        pd.Timestamp("2024-10-01"),
        pd.Timestamp("2025-04-01"),
        pd.Timestamp("2025-10-01"),
    ]
    ext_vals = [piv.loc[d, "Weekday"] for d in ext_dates]
    ax.scatter(
        ext_dates,
        ext_vals,
        s=42,
        color=TIFFANY_DEEP,
        edgecolors=MIDNIGHT,
        linewidths=0.9,
        zorder=4,
        label="Seasonal peaks & troughs",
    )

    # Direct annotations on key regime features
    ax.text(
        pd.Timestamp("2024-03-15"),
        11850,
        "Spring peak regime",
        color=MIDNIGHT,
        fontsize=9,
        fontweight="semibold",
        ha="center",
        va="top",
    )
    ax.text(
        pd.Timestamp("2025-04-01"),
        piv.loc[pd.Timestamp("2025-04-01"), "Weekday"] + 280,
        "Apr 2025 peak: 11,452",
        color=MIDNIGHT,
        fontsize=8.8,
        fontweight="semibold",
        ha="center",
        va="bottom",
    )
    ax.text(
        pd.Timestamp("2024-09-18"),
        10650,
        "Oct trough: 7,096 (-27.2% vs Apr peak)",
        color=MIDNIGHT_SOFT,
        fontsize=8.6,
        fontweight="semibold",
        ha="center",
        va="bottom",
    )

    ax.set_ylim(3800, 12400)
    ax.yaxis.set_major_formatter(lambda x, _: f"{int(x):,}")
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    fig.autofmt_xdate(rotation=0, ha="center")

    ax.set_title("Seasonal demand regime and structural weekday commute premium (2024–2025)", pad=14)
    ax.set_xlabel("Month (2024–2025)")
    ax.set_ylabel("Mean passengers per record")
    ax.legend(loc="lower left", ncol=2, frameon=False, fontsize=8.8)

    return save(fig, FIG_DIR / "fig01_monthly_demand_trend.png")


def fig02_city_demand_comparison(df: pd.DataFrame) -> Path:
    """Fig 2: Connected Dumbbell Plot — Simpson's Paradox (Raw vs Modal-Mix-Adjusted City Margin)."""
    apply_rcparams()
    fig, ax = plt.subplots(figsize=(10.5, 5.4))
    style_axes(ax, grid_axis="x")

    mix_df = pd.read_csv(TABLES_DIR / "table04_mix_adjusted_cities.csv")
    # Order from bottom to top by Raw_Mean_Margin_EUR so rank #1 Munich is at the top
    mix_df = mix_df.sort_values("Raw_Mean_Margin_EUR", ascending=True).reset_index(drop=True)
    y_pos = np.arange(len(mix_df))

    # Zero break-even vertical reference line
    ax.axvline(0.0, color=MIDNIGHT, linestyle="--", linewidth=1.3, zorder=1)
    ax.text(
        16,
        5.0,
        "Break-even (€0 / record)",
        color=MIDNIGHT,
        fontsize=8.6,
        fontweight="semibold",
        va="center",
    )

    # Highlight cities with the largest confounding shift (Madrid, Barcelona, Milan, Berlin)
    highlight_cities = {"Madrid", "Barcelona", "Milan", "Berlin"}

    for idx, row in mix_df.iterrows():
        raw_v = row["Raw_Mean_Margin_EUR"]
        adj_v = row["Mix_Adj_Mean_Margin_EUR"]
        city = row["City"]
        is_hi = city in highlight_cities
        line_col = TIFFANY_DEEP if is_hi else GRID
        line_w = 2.6 if is_hi else 1.8

        ax.plot(
            [raw_v, adj_v],
            [idx, idx],
            color=line_col,
            linewidth=line_w,
            solid_capstyle="round",
            zorder=2,
        )

    # Plot Raw means (hollow markers) vs Mix-Adjusted means (solid Tiffany markers)
    ax.scatter(
        mix_df["Raw_Mean_Margin_EUR"],
        y_pos,
        s=58,
        color=WHITE,
        edgecolors=MIDNIGHT_SOFT,
        linewidths=1.8,
        label="Unadjusted raw mean margin (€/record)",
        zorder=3,
    )
    ax.scatter(
        mix_df["Mix_Adj_Mean_Margin_EUR"],
        y_pos,
        s=68,
        color=TIFFANY,
        edgecolors=MIDNIGHT,
        linewidths=1.3,
        label="Modal-mix-adjusted margin (direct standardisation)",
        zorder=4,
    )

    # Direct annotations on the key Simpson's Paradox reversals (placed cleanly in open space)
    for idx, row in mix_df.iterrows():
        city = row["City"]
        raw_v = row["Raw_Mean_Margin_EUR"]
        adj_v = row["Mix_Adj_Mean_Margin_EUR"]
        if city == "Madrid":
            ax.text(
                adj_v + 18,
                idx,
                "Madrid: -€702 raw to -€268 adj. (28.6% micromobility)",
                color=MIDNIGHT,
                fontsize=8.4,
                fontweight="semibold",
                ha="left",
                va="center",
            )
        elif city == "Berlin":
            ax.text(
                adj_v - 18,
                idx,
                "Berlin: Rank #4 to #11 (-€354 adj.)",
                color=MIDNIGHT,
                fontsize=8.5,
                fontweight="semibold",
                ha="right",
                va="center",
            )
        elif city == "Munich":
            ax.text(
                raw_v + 18,
                idx,
                "+€400 raw (+€215 adj., Rank #1)",
                color=MIDNIGHT,
                fontsize=8.5,
                fontweight="semibold",
                ha="left",
                va="center",
            )

    city_labels = [
        f"{r['City']} ({r['Total_Passengers']/1e6:.2f}M pax)"
        for _, r in mix_df.iterrows()
    ]
    ax.set_yticks(y_pos, labels=city_labels)
    ax.set_xlim(-780, 650)
    ax.xaxis.set_major_formatter(lambda x, _: f"€{int(x):,}")

    ax.set_title(
        "Simpson's Paradox in city margins: raw vs modal-mix-adjusted performance",
        pad=14,
    )
    ax.set_xlabel("Mean operating net margin per record (EUR, r = -0.795 with micromobility share)")
    ax.set_ylabel("City (with cumulative 2024–2025 ridership)")
    ax.legend(loc="upper left", frameon=False, fontsize=8.8)

    return save(fig, FIG_DIR / "fig02_city_demand_comparison.png")


def fig03_mode_cost_recovery(df: pd.DataFrame) -> Path:
    """Fig 3: Two-Panel First-Principles Unit Economics & Marginal Carbon Abatement Return."""
    apply_rcparams()
    fig, (ax1, ax2) = plt.subplots(
        1, 2, figsize=(10.8, 5.1), sharey=True, gridspec_kw={"width_ratios": [1.1, 1.0], "wspace": 0.10}
    )
    style_axes(ax1, grid_axis="x")
    style_axes(ax2, grid_axis="x")

    ue = pd.read_csv(TABLES_DIR / "table05_unit_economics_and_carbon_cost.csv")
    # Order from lowest to highest Net_Margin_per_Pax_EUR
    ue = ue.sort_values("Net_Margin_per_Pax_EUR", ascending=True).reset_index(drop=True)
    y_pos = np.arange(len(ue))

    # Panel A: Per-Passenger Unit Economics (Mean Fare vs Variable Cost per Passenger)
    bar_h = 0.34
    ax1.barh(
        y_pos + bar_h / 2,
        ue["Mean_Fare_per_Pax_EUR"],
        height=bar_h,
        color=MIDNIGHT,
        edgecolor=WHITE,
        linewidth=0.8,
        label="Mean ticket fare (€ / pax)",
    )
    ax1.barh(
        y_pos - bar_h / 2,
        ue["Mean_Cost_per_Pax_EUR"],
        height=bar_h,
        color=TIFFANY,
        edgecolor=MIDNIGHT,
        linewidth=0.8,
        label="Mean operating cost (€ / pax)",
    )

    for idx, row in ue.iterrows():
        margin_pax = row["Net_Margin_per_Pax_EUR"]
        cost_pax = row["Mean_Cost_per_Pax_EUR"]
        fare_pax = row["Mean_Fare_per_Pax_EUR"]
        xmax = max(cost_pax, fare_pax)
        if margin_pax < 0:
            ax1.text(
                xmax + 0.5,
                idx,
                f"Net: -€{abs(margin_pax):.2f}/trip\n({row['Mean_Fare_per_Pax_EUR']/row['Mean_Cost_per_Pax_EUR']*100:.1f}% rec.)",
                color=MIDNIGHT,
                fontsize=8.3,
                fontweight="semibold",
                va="center",
            )
        else:
            ax1.text(
                xmax + 0.5,
                idx,
                f"Net: +€{margin_pax:.2f}/pax",
                color=MUTE,
                fontsize=8.3,
                va="center",
            )

    ax1.set_yticks(y_pos, labels=ue["Transport_Mode"])
    ax1.set_xlim(0, 31.0)
    ax1.set_title("A. Unit economics (€ per passenger trip)", pad=10, fontsize=11.5)
    ax1.set_xlabel("EUR per passenger (Fare vs Operating Cost)")
    ax1.set_ylabel("Transport mode")
    ax1.legend(loc="upper right", frameon=False, fontsize=8.4)

    # Panel B: Public-Finance Return per Tonne of CO2 Saved (EUR / tCO2)
    mode_tot = (
        df.groupby("Transport_Mode", as_index=False)
        .agg(
            Margin_M=("Net_Margin_EUR", lambda s: s.sum() / 1e6),
            CO2_t=("CO2_Saved_KG", lambda s: s.sum() / 1000.0),
        )
    )
    mode_tot = ue[["Transport_Mode", "Net_Return_per_Tonne_CO2_EUR"]].merge(mode_tot, on="Transport_Mode")

    ax2.axvline(0.0, color=MIDNIGHT, linestyle="--", linewidth=1.2, zorder=1)
    colors_b = [TIFFANY if m < 0 else MIDNIGHT_SOFT for m in mode_tot["Margin_M"]]
    ax2.barh(
        y_pos,
        mode_tot["Margin_M"],
        height=0.58,
        color=colors_b,
        edgecolor=WHITE,
        linewidth=0.9,
        zorder=2,
    )

    for idx, row in mode_tot.iterrows():
        m_val = row["Margin_M"]
        co2_ret = row["Net_Return_per_Tonne_CO2_EUR"]
        co2_t = row["CO2_t"]
        if m_val < 0:
            # Place label to the right of the 0 line so it never crosses the dashed axis or bar edge
            ax2.text(
                0.20,
                idx,
                f"-€{abs(m_val):.2f}M (-€{abs(co2_ret)/1000:.0f}k / tCO2)",
                color=MIDNIGHT,
                fontsize=8.2,
                fontweight="semibold",
                va="center",
                ha="left",
            )
        else:
            ax2.text(
                m_val + 0.18,
                idx,
                f"+€{m_val:.2f}M (+€{co2_ret:,.0f}/t, {co2_t:,.0f}t)",
                color=MIDNIGHT if row["Transport_Mode"] == "Metro" else MUTE,
                fontsize=8.2,
                fontweight="semibold" if row["Transport_Mode"] == "Metro" else "normal",
                va="center",
                ha="left",
            )

    ax2.set_xlim(-6.2, 9.8)
    ax2.set_title("B. Cumulative margin & carbon abatement return", pad=10, fontsize=11.5)
    ax2.set_xlabel("Cumulative net margin (€M) & net return per tCO2")

    fig.suptitle(
        "First-principles unit economics and marginal carbon abatement return by mode",
        x=0.01,
        ha="left",
        y=0.99,
        fontsize=13,
        fontweight="bold",
        color=MIDNIGHT,
    )
    fig.subplots_adjust(top=0.84)

    return save(fig, FIG_DIR / "fig03_mode_cost_recovery.png")


def fig04_delay_distribution_boxplot(df: pd.DataFrame) -> Path:
    """Fig 4: Raincloud Plot (Half-Violin KDE Density + Tukey Boxplot + Jittered Sample Strip)."""
    apply_rcparams()
    fig, ax = plt.subplots(figsize=(10.5, 5.4))
    style_axes(ax, grid_axis="x")

    order = (
        df.groupby("Transport_Mode")["Average_Delay_Minutes"]
        .median()
        .sort_values(ascending=True)
        .index.tolist()
    )
    rng = np.random.default_rng(42)
    grid_x = np.linspace(0, 12.6, 200)

    for idx, mode in enumerate(order):
        vals = df.loc[df["Transport_Mode"] == mode, "Average_Delay_Minutes"].values
        is_bus = mode == "Bus"
        cloud_col = TIFFANY if is_bus else MIST
        edge_col = MIDNIGHT if is_bus else MIDNIGHT_SOFT

        # 1. Upper half-violin (KDE density cloud)
        dens = gaussian_kde_1d(vals, grid_x, bw_factor=1.05)
        dens_scaled = dens / dens.max() * 0.38
        mask = (grid_x >= vals.min()) & (grid_x <= vals.max())
        gx = grid_x[mask]
        gy = dens_scaled[mask]

        ax.fill_between(
            gx,
            idx + 0.06,
            idx + 0.06 + gy,
            color=cloud_col,
            alpha=0.88 if is_bus else 0.75,
            edgecolor=edge_col,
            linewidth=1.3 if is_bus else 1.0,
            zorder=2,
        )

        # 2. Center line Tukey horizontal boxplot (Q25, Median, Q75, Whiskers)
        q25, med, q75 = np.percentile(vals, [25, 50, 75])
        iqr = q75 - q25
        lo_w = vals[vals >= q25 - 1.5 * iqr].min()
        hi_w = vals[vals <= q75 + 1.5 * iqr].max()

        ax.plot([lo_w, hi_w], [idx, idx], color=MIDNIGHT, linewidth=1.2, zorder=3)
        rect = plt.Rectangle(
            (q25, idx - 0.07),
            iqr,
            0.14,
            facecolor=WHITE if not is_bus else TIFFANY_DEEP,
            edgecolor=MIDNIGHT,
            linewidth=1.3,
            zorder=4,
        )
        ax.add_patch(rect)
        ax.plot(
            [med, med],
            [idx - 0.07, idx + 0.07],
            color=WHITE if is_bus else MIDNIGHT,
            linewidth=2.2,
            zorder=5,
        )

        # 3. Lower raindrop jitter strip (subsampled for crisp visual legibility)
        sample_vals = rng.choice(vals, size=min(180, len(vals)), replace=False)
        jitter_y = idx - 0.18 - rng.uniform(0.0, 0.14, size=len(sample_vals))
        ax.scatter(
            sample_vals,
            jitter_y,
            s=8,
            color=TIFFANY_DEEP if is_bus else MIDNIGHT_SOFT,
            alpha=0.45 if is_bus else 0.25,
            edgecolors="none",
            zorder=2,
        )

        # Direct callout on Bus bottleneck and Metro baseline (positioned clear of KDE tail)
        if is_bus:
            ax.text(
                14.85,
                idx + 0.23,
                f"Bus bottleneck: median {med:.1f}m, mean {vals.mean():.2f}m (74.9% on-time, 3.74/5)",
                color=MIDNIGHT,
                fontsize=8.4,
                fontweight="semibold",
                ha="right",
                va="bottom",
            )
        elif mode == "Metro":
            ax.text(
                8.40,
                idx + 0.16,
                f"Grade-separated Metro: median {med:.1f}m (84.1% on-time)",
                color=MUTE,
                fontsize=8.4,
                va="bottom",
            )

    ax.set_yticks(range(len(order)), labels=order)
    ax.set_xlim(-0.2, 15.2)
    ax.set_ylim(-0.45, len(order) - 0.35)
    ax.set_title(
        "Raincloud distribution of daily service delays across transport modes (KDE, IQR & raindrops)",
        pad=14,
    )
    ax.set_xlabel("Average service delay (minutes)")
    ax.set_ylabel("Transport mode (ordered by median delay)")

    return save(fig, FIG_DIR / "fig04_delay_distribution_boxplot.png")


def fig05_delay_rating_relationship(df: pd.DataFrame) -> Path:
    """Fig 5: Joint Bivariate OLS & Marginal KDE Density Plot (Delay vs Rating by Event Status)."""
    apply_rcparams()
    fig = plt.figure(figsize=(10.5, 5.5))
    gs = GridSpec(
        2,
        2,
        figure=fig,
        width_ratios=[4.3, 1.0],
        height_ratios=[1.0, 4.0],
        wspace=0.06,
        hspace=0.08,
    )
    ax_main = fig.add_subplot(gs[1, 0])
    ax_top = fig.add_subplot(gs[0, 0], sharex=ax_main)
    ax_right = fig.add_subplot(gs[1, 1], sharey=ax_main)

    style_axes(ax_main, grid_axis="y")
    style_axes(ax_top, grid_axis="none")
    style_axes(ax_right, grid_axis="none")

    normal = df[df["Event_Day"] == "No"]
    event = df[df["Event_Day"] == "Yes"]

    # Main scatter + severe delay zone (> 6.0 min)
    ax_main.axvspan(6.0, 12.8, color=TIFFANY, alpha=0.12, zorder=0)
    ax_main.text(
        9.4,
        4.88,
        "Severe delay zone (> 6.0 min)",
        color=MUTE,
        fontsize=8.8,
        ha="center",
        va="top",
    )

    ax_main.scatter(
        normal["Average_Delay_Minutes"],
        normal["Customer_Rating"],
        s=14,
        color=MIDNIGHT_SOFT,
        alpha=0.16,
        edgecolors="none",
        label="Standard days (n = 4,490; mean 4.22m, 4.02/5 rating)",
        zorder=2,
    )
    ax_main.scatter(
        event["Average_Delay_Minutes"],
        event["Customer_Rating"],
        s=24,
        color=TIFFANY_DEEP,
        edgecolors=MIDNIGHT,
        linewidths=0.35,
        alpha=0.82,
        label="Major event days (n = 510; mean 5.53m, 3.87/5 rating)",
        zorder=3,
    )

    # OLS linear fit
    slope, intercept = np.polyfit(df["Average_Delay_Minutes"], df["Customer_Rating"], 1)
    x_line = np.linspace(0, 12.5, 100)
    ax_main.plot(
        x_line,
        slope * x_line + intercept,
        color=MIDNIGHT,
        linewidth=2.4,
        solid_capstyle="round",
        label=f"OLS linear fit (r = -0.821, slope = {slope:.2f} pts/min)",
        zorder=4,
    )

    ax_main.set_xlim(-0.2, 12.8)
    ax_main.set_ylim(2.55, 5.02)
    ax_main.set_xlabel("Average delay (minutes)")
    ax_main.set_ylabel("Customer rating (1.0 to 5.0 scale)")
    ax_main.legend(loc="lower left", frameon=False, fontsize=8.5)

    # Top Marginal KDE: Delay distribution (Standard vs Event days)
    gx = np.linspace(0, 12.5, 200)
    kde_norm_x = gaussian_kde_1d(normal["Average_Delay_Minutes"].values, gx)
    kde_evt_x = gaussian_kde_1d(event["Average_Delay_Minutes"].values, gx)
    ax_top.fill_between(gx, 0, kde_norm_x, color=MIDNIGHT_SOFT, alpha=0.28)
    ax_top.plot(gx, kde_norm_x, color=MIDNIGHT_SOFT, linewidth=1.6)
    ax_top.fill_between(gx, 0, kde_evt_x, color=TIFFANY, alpha=0.45)
    ax_top.plot(gx, kde_evt_x, color=TIFFANY_DEEP, linewidth=1.8)
    ax_top.axvline(normal["Average_Delay_Minutes"].mean(), color=MIDNIGHT_SOFT, linestyle=":", linewidth=1.2)
    ax_top.axvline(event["Average_Delay_Minutes"].mean(), color=TIFFANY_DEEP, linestyle="--", linewidth=1.4)
    ax_top.text(
        event["Average_Delay_Minutes"].mean() + 0.25,
        max(kde_evt_x) * 0.78,
        "Event shift: +31.0% delay",
        color=MIDNIGHT,
        fontsize=8.3,
        fontweight="semibold",
    )
    ax_top.set_yticks([])
    ax_top.spines["left"].set_visible(False)
    plt.setp(ax_top.get_xticklabels(), visible=False)

    # Right Marginal KDE: Rating distribution (Standard vs Event days)
    gy = np.linspace(2.6, 5.0, 200)
    kde_norm_y = gaussian_kde_1d(normal["Customer_Rating"].values, gy)
    kde_evt_y = gaussian_kde_1d(event["Customer_Rating"].values, gy)
    ax_right.fill_betweenx(gy, 0, kde_norm_y, color=MIDNIGHT_SOFT, alpha=0.28)
    ax_right.plot(kde_norm_y, gy, color=MIDNIGHT_SOFT, linewidth=1.6)
    ax_right.fill_betweenx(gy, 0, kde_evt_y, color=TIFFANY, alpha=0.45)
    ax_right.plot(kde_evt_y, gy, color=TIFFANY_DEEP, linewidth=1.8)
    ax_right.axhline(normal["Customer_Rating"].mean(), color=MIDNIGHT_SOFT, linestyle=":", linewidth=1.2)
    ax_right.axhline(event["Customer_Rating"].mean(), color=TIFFANY_DEEP, linestyle="--", linewidth=1.4)
    ax_right.set_xticks([])
    ax_right.spines["bottom"].set_visible(False)
    plt.setp(ax_right.get_yticklabels(), visible=False)

    fig.suptitle(
        "Joint bivariate relationship and marginal density shifts: service delay vs customer rating",
        x=0.01,
        ha="left",
        y=0.99,
        fontsize=13,
        fontweight="bold",
        color=MIDNIGHT,
    )
    fig.subplots_adjust(top=0.90)

    return save(fig, FIG_DIR / "fig05_delay_rating_relationship.png")


def fig06_weather_mode_delay_heatmap(df: pd.DataFrame) -> Path:
    """Fig 6: Dual-Encoded Interaction Matrix Heatmap — Mean Delay (min) & % Surge over Clear."""
    apply_rcparams()
    fig, ax = plt.subplots(figsize=(10.5, 5.2))
    style_axes(ax, grid_axis="none")

    mode_order = ["Bus", "Park and Ride", "Tram", "Metro", "E-Scooter", "Bike Share"]
    weather_order = ["Clear", "Cloudy", "Windy", "Heatwave", "Rain", "Snow"]

    piv = (
        df.pivot_table(
            index="Transport_Mode",
            columns="Weather",
            values="Average_Delay_Minutes",
            aggfunc="mean",
        )
        .reindex(index=mode_order, columns=weather_order)
    )

    im = ax.imshow(piv.values, cmap=ARDEN_CMAP, aspect="auto", vmin=1.0, vmax=10.5)

    ax.set_xticks(range(len(weather_order)), labels=weather_order)
    ax.set_yticks(range(len(mode_order)), labels=mode_order)

    # Direct numeric values + % escalation over Clear baseline inside cells
    for i in range(len(mode_order)):
        clear_base = piv.values[i, 0]
        for j in range(len(weather_order)):
            val = piv.values[i, j]
            pct_surge = (val - clear_base) / clear_base * 100.0
            txt_color = WHITE if val >= 5.2 else MIDNIGHT
            weight = "bold" if (weather_order[j] == "Snow" or mode_order[i] == "Bus") else "normal"
            if j == 0:
                cell_txt = f"{val:.2f}m\n(base)"
            else:
                cell_txt = f"{val:.2f}m\n(+{pct_surge:.0f}%)"
            ax.text(
                j,
                i,
                cell_txt,
                ha="center",
                va="center",
                color=txt_color,
                fontsize=8.6,
                fontweight=weight,
            )

    cbar = fig.colorbar(im, ax=ax, pad=0.02, fraction=0.035)
    cbar.outline.set_edgecolor(GRID)
    cbar.ax.tick_params(colors=MUTE, labelsize=9)
    cbar.set_label("Mean delay (minutes)", color=MIDNIGHT, fontsize=10, fontweight="semibold")

    ax.set_title(
        "Weather × transport mode interaction matrix: mean delay (min) and % escalation over Clear",
        pad=14,
    )
    ax.set_xlabel("Weather condition (ordered by network disruption severity)")
    ax.set_ylabel("Transport mode")

    return save(fig, FIG_DIR / "fig06_weather_mode_delay_heatmap.png")


def fig07_route_accessibility_rate(df: pd.DataFrame) -> Path:
    """Fig 7: Two-Way Interaction Matrix Heatmap — Route Type x Mode Accessibility Complaints per 10k Pax."""
    apply_rcparams()
    fig, (ax1, ax2) = plt.subplots(
        1, 2, figsize=(10.8, 5.1), sharey=True, gridspec_kw={"width_ratios": [1.1, 1.5], "wspace": 0.12}
    )
    style_axes(ax1, grid_axis="x")
    style_axes(ax2, grid_axis="none")

    rt = (
        df.groupby("Route_Type", as_index=False)
        .agg(
            Complaints=("Accessibility_Complaints", "sum"),
            Passengers=("Passengers", "sum"),
            Raw_Mean=("Accessibility_Complaints", "mean"),
        )
        .assign(Rate_10k=lambda d: d["Complaints"] / d["Passengers"] * 10000.0)
        .sort_values("Rate_10k", ascending=True)
        .reset_index(drop=True)
    )
    route_order = rt["Route_Type"].tolist()
    y_pos = np.arange(len(route_order))

    # Panel A: Aggregate Normalised Rate vs Raw Daily Illusion
    is_sub = rt["Route_Type"] == "Suburban Feeder"
    colors_a = [TIFFANY if h else MIDNIGHT_SOFT for h in is_sub]
    ax1.barh(
        y_pos,
        rt["Rate_10k"],
        height=0.62,
        color=colors_a,
        edgecolor=WHITE,
        linewidth=0.9,
    )
    for idx, row in rt.iterrows():
        val = row["Rate_10k"]
        raw = row["Raw_Mean"]
        ax1.text(
            val + 0.30,
            idx,
            f"{val:.2f}/10k (raw {raw:.1f}/d)",
            color=MIDNIGHT if row["Route_Type"] == "Suburban Feeder" else MUTE,
            fontsize=8.2,
            fontweight="semibold" if row["Route_Type"] == "Suburban Feeder" else "normal",
            va="center",
        )
    ax1.set_yticks(y_pos, labels=route_order)
    ax1.set_xlim(0, 27.5)
    ax1.set_title("A. Route-level rate (vs raw/day)", pad=10, fontsize=11.5)
    ax1.set_xlabel("Complaints per 10,000 pax")
    ax1.set_ylabel("Route type")

    # Panel B: 6x6 Route_Type x Transport_Mode Interaction Heatmap (Mean Complaints per 10k Pax)
    mode_cols = ["Metro", "Tram", "Park and Ride", "Bus", "Bike Share", "E-Scooter"]
    piv = (
        df.pivot_table(
            index="Route_Type",
            columns="Transport_Mode",
            values="Complaints_per_10k_Pax",
            aggfunc="mean",
        )
        .reindex(index=route_order, columns=mode_cols)
    )

    im = ax2.imshow(piv.values, cmap=ARDEN_CMAP, aspect="auto", vmin=8.0, vmax=68.0)
    ax2.set_xticks(range(len(mode_cols)), labels=mode_cols)
    plt.setp(ax2.get_xticklabels(), rotation=18, ha="right")

    for i in range(len(route_order)):
        for j in range(len(mode_cols)):
            val = piv.values[i, j]
            txt_color = WHITE if val >= 32.0 else MIDNIGHT
            is_anom = route_order[i] == "Suburban Feeder" and mode_cols[j] in ("Bike Share", "E-Scooter", "Bus")
            ax2.text(
                j,
                i,
                f"{val:.1f}",
                ha="center",
                va="center",
                color=txt_color,
                fontsize=8.6,
                fontweight="bold" if is_anom else "normal",
            )

    cbar = fig.colorbar(im, ax=ax2, pad=0.02, fraction=0.038)
    cbar.outline.set_edgecolor(GRID)
    cbar.ax.tick_params(colors=MUTE, labelsize=8.5)
    cbar.set_label("Mean complaints / 10k pax", color=MIDNIGHT, fontsize=9.5, fontweight="semibold")

    ax2.set_title("B. Route × Mode interaction: Suburban Feeder micromobility spike", pad=10, fontsize=11.5)
    ax2.set_xlabel("Transport mode")

    fig.suptitle(
        "Accessibility complaints per 10,000 passengers: route reversal and Suburban Feeder × Micromobility anomaly",
        x=0.01,
        ha="left",
        y=0.99,
        fontsize=12.5,
        fontweight="bold",
        color=MIDNIGHT,
    )
    fig.subplots_adjust(top=0.84)

    return save(fig, FIG_DIR / "fig07_route_accessibility_rate.png")


def main() -> None:
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    df = load_data()
    fig01_monthly_demand_trend(df)
    fig02_city_demand_comparison(df)
    fig03_mode_cost_recovery(df)
    fig04_delay_distribution_boxplot(df)
    fig05_delay_rating_relationship(df)
    fig06_weather_mode_delay_heatmap(df)
    fig07_route_accessibility_rate(df)
    print("All 7 advanced data-science figures generated successfully.")


if __name__ == "__main__":
    main()

