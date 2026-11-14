import sys
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.gridspec import GridSpec

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from style.palette import (
    ARDEN_CMAP, GRID, MIDNIGHT, MIDNIGHT_SOFT, MIST, MUTE, TEAL,
    TIFFANY, TIFFANY_DEEP, WHITE, apply_rcparams, save, style_axes,
)

DATA_CSV = ROOT / "data" / "ecomove_cleaned.csv"
TABLES_DIR = ROOT / "output" / "tables"
FIG_DIR = ROOT / "output" / "figures"

C_MODE, C_ROUTE, C_WEATHER = "Transport_Mode", "Route_Type", "Weather"
C_PAX, C_DELAY, C_RATING = "Passengers", "Average_Delay_Minutes", "Customer_Rating"
C_COMP, C_CO2, C_EVT = "Accessibility_Complaints", "CO2_Saved_KG", "Event_Day"


def _setup(w=10.5, h=5.2, grid="y"):
    fig, ax = plt.subplots(figsize=(w, h))
    style_axes(ax, grid)
    return fig, ax


def _kde(sample, grid, scale=1.0):
    vals = np.asarray(sample, dtype=float)
    sd = np.std(vals, ddof=1)
    q1, q3 = np.quantile(vals, [0.25, 0.75])
    sigma = min(sd, (q3 - q1) / 1.34) if q3 > q1 else sd
    bw = max(0.9 * sigma * (len(vals) ** -0.2) * scale, 1e-3)
    diff = (grid[:, None] - vals[None, :]) / bw
    return np.exp(-0.5 * diff * diff).mean(axis=1) / (bw * np.sqrt(2.0 * np.pi))


def _note(ax, x, y, txt, color=MIDNIGHT, bold=False, ha="center", va="center", size=8.4):
    ax.text(x, y, txt, color=color, fontsize=size, fontweight="semibold" if bold else "normal", ha=ha, va=va)


def _colorbar(fig, ax, img, label, fraction=0.036, tick_size=8.8):
    bar = fig.colorbar(img, ax=ax, pad=0.02, fraction=fraction)
    bar.outline.set_edgecolor(GRID)
    bar.ax.tick_params(colors=MUTE, labelsize=tick_size)
    bar.set_label(label, color=MIDNIGHT, fontsize=9.8, fontweight="semibold")


def _heatmap(ax, values, xlabels, ylabels, vmin, vmax, text_fn):
    img = ax.imshow(values, cmap=ARDEN_CMAP, aspect="auto", vmin=vmin, vmax=vmax)
    ax.set_xticks(range(len(xlabels)), labels=xlabels)
    if ylabels is not None:
        ax.set_yticks(range(len(ylabels)), labels=ylabels)
    for r in range(values.shape[0]):
        for c in range(values.shape[1]):
            label, col, weight = text_fn(r, c, values[r, c])
            ax.text(c, r, label, ha="center", va="center", color=col, fontsize=8.6, fontweight=weight)
    return img


def fig01_monthly_demand_trend(df: pd.DataFrame) -> Path:
    fig, ax = _setup(10.5, 5.2, "y")
    piv = (
        df.groupby(["YearMonth", "Is_Weekend"], as_index=False)[C_PAX].mean()
        .assign(YM_Date=lambda d: pd.to_datetime(d["YearMonth"] + "-01"))
        .pivot(index="YM_Date", columns="Is_Weekend", values=C_PAX).sort_index()
    )
    dt, wday, wend = piv.index, piv["Weekday"].values, piv["Weekend"].values

    for start, end in (("2024-02-18", "2024-04-15"), ("2025-02-18", "2025-04-15")):
        ax.axvspan(pd.Timestamp(start), pd.Timestamp(end), color=TIFFANY, alpha=0.14, zorder=0)

    ax.fill_between(dt, wend, wday, color=MIST, alpha=0.85, label="Weekday commute premium (+34.1% mean)", zorder=1)
    ax.plot(dt, wday, color=MIDNIGHT, lw=2.5, label="Weekday service (mean 8,803 pax)", zorder=3)
    ax.plot(dt, wend, color=TEAL, lw=2.2, ls="--", label="Weekend service (mean 6,563 pax)", zorder=3)

    peaks = [pd.Timestamp(s) for s in ("2024-03-01", "2024-10-01", "2025-04-01", "2025-10-01")]
    ax.scatter(peaks, [piv.loc[d, "Weekday"] for d in peaks], s=42, color=TIFFANY_DEEP, edgecolors=MIDNIGHT, linewidths=0.9, zorder=4, label="Seasonal peaks & troughs")

    _note(ax, pd.Timestamp("2024-03-15"), 11850, "Spring peak regime", bold=True, va="top", size=9)
    _note(ax, pd.Timestamp("2025-04-01"), piv.loc[pd.Timestamp("2025-04-01"), "Weekday"] + 280, "Apr 2025 peak: 11,452", bold=True, va="bottom", size=8.8)
    _note(ax, pd.Timestamp("2024-09-18"), 10650, "Oct trough: 7,096 (-27.2% vs Apr peak)", color=MIDNIGHT_SOFT, bold=True, va="bottom", size=8.6)

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
    fig, ax = _setup(10.5, 5.4, "x")
    mix = pd.read_csv(TABLES_DIR / "table04_mix_adjusted_cities.csv").sort_values("Raw_Mean_Margin_EUR").reset_index(drop=True)
    y = np.arange(len(mix))
    ax.axvline(0.0, color=MIDNIGHT, ls="--", lw=1.3, zorder=1)
    _note(ax, 16, 5.0, "Break-even (€0 / record)", bold=True, ha="left", size=8.6)

    focused = {"Madrid", "Barcelona", "Milan", "Berlin"}
    for i, r in mix.iterrows():
        hi = r["City"] in focused
        ax.plot([r["Raw_Mean_Margin_EUR"], r["Mix_Adj_Mean_Margin_EUR"]], [i, i], color=TIFFANY_DEEP if hi else GRID, lw=2.6 if hi else 1.8, zorder=2)

    ax.scatter(mix["Raw_Mean_Margin_EUR"], y, s=58, color=WHITE, edgecolors=MIDNIGHT_SOFT, linewidths=1.8, label="Unadjusted raw mean margin (€/record)", zorder=3)
    ax.scatter(mix["Mix_Adj_Mean_Margin_EUR"], y, s=68, color=TIFFANY, edgecolors=MIDNIGHT, linewidths=1.3, label="Modal-mix-adjusted margin (direct standardisation)", zorder=4)

    notes = {
        "Madrid": (18, "Madrid: -€702 raw to -€268 adj. (28.6% micromobility)", "left", False),
        "Berlin": (None, "Berlin: Rank #4 to #11 (-€354 adj.)", "right", True),
        "Munich": (None, "+€400 raw (+€215 adj., Rank #1)", "left", False),
    }
    for i, r in mix.iterrows():
        if r["City"] in notes:
            xp, txt, ha, use_adj = notes[r["City"]]
            x_val = xp if xp is not None else (r["Mix_Adj_Mean_Margin_EUR"] - 18 if use_adj else r["Raw_Mean_Margin_EUR"] + 18)
            _note(ax, x_val, i, txt, bold=True, ha=ha, size=8.4)

    ax.set_yticks(y, labels=[f"{r['City']} ({r['Total_Passengers']/1e6:.2f}M pax)" for _, r in mix.iterrows()])
    ax.set_xlim(-780, 650)
    ax.xaxis.set_major_formatter(lambda x, _: f"€{int(x):,}")
    ax.set_title("Simpson's Paradox in city margins: raw vs modal-mix-adjusted performance", pad=14)
    ax.set_xlabel("Mean operating net margin per record (EUR, r = -0.795 with micromobility share)")
    ax.set_ylabel("City (with cumulative 2024–2025 ridership)")
    ax.legend(loc="upper left", frameon=False, fontsize=8.8)
    return save(fig, FIG_DIR / "fig02_city_demand_comparison.png")


def fig03_mode_cost_recovery(df: pd.DataFrame) -> Path:
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.8, 5.1), sharey=True, gridspec_kw={"width_ratios": [1.1, 1.0], "wspace": 0.10})
    style_axes(ax1, "x")
    style_axes(ax2, "x")

    ue = pd.read_csv(TABLES_DIR / "table05_unit_economics_and_carbon_cost.csv").sort_values("Net_Margin_per_Pax_EUR").reset_index(drop=True)
    y = np.arange(len(ue))
    h = 0.34
    ax1.barh(y + h / 2, ue["Mean_Fare_per_Pax_EUR"], height=h, color=MIDNIGHT, edgecolor=WHITE, lw=0.8, label="Mean ticket fare (€ / pax)")
    ax1.barh(y - h / 2, ue["Mean_Cost_per_Pax_EUR"], height=h, color=TIFFANY, edgecolor=MIDNIGHT, lw=0.8, label="Mean operating cost (€ / pax)")

    for i, r in ue.iterrows():
        m, x = r["Net_Margin_per_Pax_EUR"], max(r["Mean_Cost_per_Pax_EUR"], r["Mean_Fare_per_Pax_EUR"]) + 0.5
        if m < 0:
            _note(ax1, x, i, f"Net: -€{abs(m):.2f}/trip\n({r['Mean_Fare_per_Pax_EUR']/r['Mean_Cost_per_Pax_EUR']*100:.1f}% rec.)", bold=True, ha="left", size=8.3)
        else:
            _note(ax1, x, i, f"Net: +€{m:.2f}/pax", color=MUTE, ha="left", size=8.3)

    ax1.set_yticks(y, labels=ue[C_MODE])
    ax1.set_xlim(0, 31.0)
    ax1.set_title("A. Unit economics (€ per passenger trip)", pad=10, fontsize=11.5)
    ax1.set_xlabel("EUR per passenger (Fare vs Operating Cost)")
    ax1.set_ylabel("Transport mode")
    ax1.legend(loc="upper right", frameon=False, fontsize=8.4)

    tot = df.groupby(C_MODE, as_index=False).agg(Margin_M=("Net_Margin_EUR", lambda s: s.sum() / 1e6), CO2_t=(C_CO2, lambda s: s.sum() / 1e3))
    panel_b = ue[[C_MODE, "Net_Return_per_Tonne_CO2_EUR"]].merge(tot, on=C_MODE)
    ax2.axvline(0.0, color=MIDNIGHT, ls="--", lw=1.2, zorder=1)
    ax2.barh(y, panel_b["Margin_M"], height=0.58, color=[TIFFANY if m < 0 else MIDNIGHT_SOFT for m in panel_b["Margin_M"]], edgecolor=WHITE, lw=0.9, zorder=2)

    for i, r in panel_b.iterrows():
        m, ret = r["Margin_M"], r["Net_Return_per_Tonne_CO2_EUR"]
        if m < 0:
            _note(ax2, 0.20, i, f"-€{abs(m):.2f}M (-€{abs(ret)/1000:.0f}k / tCO2)", bold=True, ha="left", size=8.2)
        else:
            is_metro = r[C_MODE] == "Metro"
            _note(ax2, m + 0.18, i, f"+€{m:.2f}M (+€{ret:,.0f}/t, {r['CO2_t']:,.0f}t)", color=MIDNIGHT if is_metro else MUTE, bold=is_metro, ha="left", size=8.2)

    ax2.set_xlim(-6.2, 9.8)
    ax2.set_title("B. Cumulative margin & carbon abatement return", pad=10, fontsize=11.5)
    ax2.set_xlabel("Cumulative net margin (€M) & net return per tCO2")
    fig.suptitle("First-principles unit economics and marginal carbon abatement return by mode", x=0.01, ha="left", y=0.99, fontsize=13, fontweight="bold", color=MIDNIGHT)
    fig.subplots_adjust(top=0.84)
    return save(fig, FIG_DIR / "fig03_mode_cost_recovery.png")


def fig04_delay_distribution_boxplot(df: pd.DataFrame) -> Path:
    fig, ax = _setup(10.5, 5.4, "x")
    order = df.groupby(C_MODE)[C_DELAY].median().sort_values().index.tolist()
    rng, gx_full = np.random.default_rng(42), np.linspace(0, 12.6, 200)

    for i, mode in enumerate(order):
        vals = df.loc[df[C_MODE] == mode, C_DELAY].values
        bus = mode == "Bus"
        dens = _kde(vals, gx_full, scale=1.05)
        span = (gx_full >= vals.min()) & (gx_full <= vals.max())
        ax.fill_between(gx_full[span], i + 0.06, i + 0.06 + (dens[span] / dens.max() * 0.38), color=TIFFANY if bus else MIST, alpha=0.88 if bus else 0.75, edgecolor=MIDNIGHT if bus else MIDNIGHT_SOFT, lw=1.3 if bus else 1.0, zorder=2)

        q1, med, q3 = np.percentile(vals, [25, 50, 75])
        iqr = q3 - q1
        lo_w = vals[vals >= q1 - 1.5 * iqr].min()
        hi_w = vals[vals <= q3 + 1.5 * iqr].max()
        ax.plot([lo_w, hi_w], [i, i], color=MIDNIGHT, lw=1.2, zorder=3)
        ax.add_patch(plt.Rectangle((q1, i - 0.07), iqr, 0.14, facecolor=TIFFANY_DEEP if bus else WHITE, edgecolor=MIDNIGHT, lw=1.3, zorder=4))
        ax.plot([med, med], [i - 0.07, i + 0.07], color=WHITE if bus else MIDNIGHT, lw=2.2, zorder=5)

        pts = rng.choice(vals, size=min(180, vals.size), replace=False)
        ax.scatter(pts, i - 0.18 - rng.uniform(0.0, 0.14, size=pts.size), s=8, color=TIFFANY_DEEP if bus else MIDNIGHT_SOFT, alpha=0.45 if bus else 0.25, edgecolors="none", zorder=2)

        if bus:
            _note(ax, 14.85, i + 0.23, f"Bus bottleneck: median {med:.1f}m, mean {vals.mean():.2f}m (74.9% on-time, 3.74/5)", bold=True, ha="right", va="bottom")
        elif mode == "Metro":
            _note(ax, 8.40, i + 0.16, f"Grade-separated Metro: median {med:.1f}m (84.1% on-time)", color=MUTE, ha="left", va="bottom")

    ax.set_yticks(range(len(order)), labels=order)
    ax.set_xlim(-0.2, 15.2)
    ax.set_ylim(-0.45, len(order) - 0.35)
    ax.set_title("Raincloud distribution of daily service delays across transport modes (KDE, IQR & raindrops)", pad=14)
    ax.set_xlabel("Average service delay (minutes)")
    ax.set_ylabel("Transport mode (ordered by median delay)")
    return save(fig, FIG_DIR / "fig04_delay_distribution_boxplot.png")


def fig05_delay_rating_relationship(df: pd.DataFrame) -> Path:
    fig = plt.figure(figsize=(10.5, 5.5))
    gs = GridSpec(2, 2, figure=fig, width_ratios=[4.3, 1.0], height_ratios=[1.0, 4.0], wspace=0.06, hspace=0.08)
    ax_main = fig.add_subplot(gs[1, 0])
    ax_top = fig.add_subplot(gs[0, 0], sharex=ax_main)
    ax_right = fig.add_subplot(gs[1, 1], sharey=ax_main)
    style_axes(ax_main, "y")
    style_axes(ax_top, "none")
    style_axes(ax_right, "none")

    norm, evt = df[df[C_EVT] == "No"], df[df[C_EVT] == "Yes"]
    ax_main.axvspan(6.0, 12.8, color=TIFFANY, alpha=0.12, zorder=0)
    _note(ax_main, 9.4, 4.88, "Severe delay zone (> 6.0 min)", color=MUTE, va="top", size=8.8)

    ax_main.scatter(norm[C_DELAY], norm[C_RATING], s=14, color=MIDNIGHT_SOFT, alpha=0.16, edgecolors="none", label="Standard days (n = 4,490; mean 4.22m, 4.02/5 rating)", zorder=2)
    ax_main.scatter(evt[C_DELAY], evt[C_RATING], s=24, color=TIFFANY_DEEP, edgecolors=MIDNIGHT, linewidths=0.35, alpha=0.82, label="Major event days (n = 510; mean 5.53m, 3.87/5 rating)", zorder=3)

    slope, intercept = np.polyfit(df[C_DELAY], df[C_RATING], 1)
    xl = np.linspace(0, 12.5, 100)
    ax_main.plot(xl, slope * xl + intercept, color=MIDNIGHT, lw=2.4, label=f"OLS linear fit (r = -0.821, slope = {slope:.2f} pts/min)", zorder=4)
    ax_main.set_xlim(-0.2, 12.8)
    ax_main.set_ylim(2.55, 5.02)
    ax_main.set_xlabel("Average delay (minutes)")
    ax_main.set_ylabel("Customer rating (1.0 to 5.0 scale)")
    ax_main.legend(loc="lower left", frameon=False, fontsize=8.5)

    gx = np.linspace(0, 12.5, 200)
    kx_n, kx_e = _kde(norm[C_DELAY].values, gx), _kde(evt[C_DELAY].values, gx)
    ax_top.fill_between(gx, 0, kx_n, color=MIDNIGHT_SOFT, alpha=0.28)
    ax_top.plot(gx, kx_n, color=MIDNIGHT_SOFT, lw=1.6)
    ax_top.fill_between(gx, 0, kx_e, color=TIFFANY, alpha=0.45)
    ax_top.plot(gx, kx_e, color=TIFFANY_DEEP, lw=1.8)
    ax_top.axvline(norm[C_DELAY].mean(), color=MIDNIGHT_SOFT, ls=":", lw=1.2)
    ax_top.axvline(evt[C_DELAY].mean(), color=TIFFANY_DEEP, ls="--", lw=1.4)
    ax_top.set_ylim(0, max(kx_n.max(), kx_e.max()) * 1.24)
    _note(ax_top, evt[C_DELAY].mean() + 2.35, kx_e.max() * 0.88, "Event shift: +31.0% delay", bold=True, ha="left", size=8.3)
    ax_top.axis("off")

    gy = np.linspace(2.6, 5.0, 200)
    ky_n, ky_e = _kde(norm[C_RATING].values, gy), _kde(evt[C_RATING].values, gy)
    ax_right.fill_betweenx(gy, 0, ky_n, color=MIDNIGHT_SOFT, alpha=0.28)
    ax_right.plot(ky_n, gy, color=MIDNIGHT_SOFT, lw=1.6)
    ax_right.fill_betweenx(gy, 0, ky_e, color=TIFFANY, alpha=0.45)
    ax_right.plot(ky_e, gy, color=TIFFANY_DEEP, lw=1.8)
    ax_right.axhline(norm[C_RATING].mean(), color=MIDNIGHT_SOFT, ls=":", lw=1.2)
    ax_right.axhline(evt[C_RATING].mean(), color=TIFFANY_DEEP, ls="--", lw=1.4)
    ax_right.axis("off")

    fig.suptitle("Joint bivariate relationship and marginal density shifts: service delay vs customer rating", x=0.01, ha="left", y=0.99, fontsize=13, fontweight="bold", color=MIDNIGHT)
    fig.subplots_adjust(top=0.90)
    return save(fig, FIG_DIR / "fig05_delay_rating_relationship.png")


def fig06_weather_mode_delay_heatmap(df: pd.DataFrame) -> Path:
    fig, ax = _setup(10.5, 5.2, "none")
    modes = ["Bus", "Park and Ride", "Tram", "Metro", "E-Scooter", "Bike Share"]
    weathers = ["Clear", "Cloudy", "Windy", "Heatwave", "Rain", "Snow"]
    mat = df.pivot_table(index=C_MODE, columns=C_WEATHER, values=C_DELAY, aggfunc="mean").reindex(index=modes, columns=weathers).values

    def fmt(r: int, c: int, v: float):
        pct = (v - mat[r, 0]) / mat[r, 0] * 100.0
        txt = f"{v:.2f}m\n(base)" if c == 0 else f"{v:.2f}m\n(+{pct:.0f}%)"
        return txt, (WHITE if v >= 5.2 else MIDNIGHT), ("bold" if weathers[c] == "Snow" or modes[r] == "Bus" else "normal")

    img = _heatmap(ax, mat, weathers, modes, 1.0, 10.5, fmt)
    _colorbar(fig, ax, img, "Mean delay (minutes)", fraction=0.035, tick_size=9.0)
    ax.set_title("Weather × transport mode interaction matrix: mean delay (min) and % escalation over Clear", pad=14)
    ax.set_xlabel("Weather condition (ordered by network disruption severity)")
    ax.set_ylabel("Transport mode")
    return save(fig, FIG_DIR / "fig06_weather_mode_delay_heatmap.png")


def fig07_route_accessibility_rate(df: pd.DataFrame) -> Path:
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.8, 5.1), sharey=True, gridspec_kw={"width_ratios": [1.1, 1.5], "wspace": 0.12})
    style_axes(ax1, "x")
    style_axes(ax2, "none")

    rt = (
        df.groupby(C_ROUTE, as_index=False)
        .agg(Complaints=(C_COMP, "sum"), Passengers=(C_PAX, "sum"), Raw_Mean=(C_COMP, "mean"))
        .assign(Rate_10k=lambda d: d["Complaints"] / d[C_PAX] * 10000.0)
        .sort_values("Rate_10k").reset_index(drop=True)
    )
    routes = rt[C_ROUTE].tolist()
    y = np.arange(len(routes))
    ax1.barh(y, rt["Rate_10k"], height=0.62, color=[TIFFANY if r == "Suburban Feeder" else MIDNIGHT_SOFT for r in routes], edgecolor=WHITE, lw=0.9)

    for i, row in rt.iterrows():
        sub = row[C_ROUTE] == "Suburban Feeder"
        _note(ax1, row["Rate_10k"] + 0.30, i, f"{row['Rate_10k']:.2f}/10k (raw {row['Raw_Mean']:.1f}/d)", color=MIDNIGHT if sub else MUTE, bold=sub, ha="left", size=8.2)
    ax1.set_yticks(y, labels=routes)
    ax1.set_xlim(0, 27.5)
    ax1.set_title("A. Route-level rate (vs raw/day)", pad=10, fontsize=11.5)
    ax1.set_xlabel("Complaints per 10,000 pax")
    ax1.set_ylabel("Route type")

    modes = ["Metro", "Tram", "Park and Ride", "Bus", "Bike Share", "E-Scooter"]
    mat = (
        df.groupby([C_ROUTE, C_MODE], as_index=False)
        .agg(Complaints=(C_COMP, "sum"), Passengers=(C_PAX, "sum"))
        .assign(Rate_10k=lambda d: d["Complaints"] / d[C_PAX] * 10000.0)
        .pivot(index=C_ROUTE, columns=C_MODE, values="Rate_10k")
        .reindex(index=routes, columns=modes).values
    )

    def fmt(r: int, c: int, v: float):
        anom = routes[r] == "Suburban Feeder" and modes[c] in ("Bike Share", "E-Scooter", "Bus")
        return f"{v:.1f}", (WHITE if v >= 28.0 else MIDNIGHT), ("bold" if anom else "normal")

    img = _heatmap(ax2, mat, modes, None, 10.0, 56.0, fmt)
    plt.setp(ax2.get_xticklabels(), rotation=18, ha="right")
    _colorbar(fig, ax2, img, "Aggregate complaints / 10k pax", fraction=0.038, tick_size=8.5)
    ax2.set_title("B. Route × Mode interaction: Suburban Feeder micromobility spike", pad=10, fontsize=11.5)
    ax2.set_xlabel("Transport mode")
    fig.suptitle("Accessibility complaints per 10,000 passengers: route reversal and Suburban Feeder × Micromobility anomaly", x=0.01, ha="left", y=0.99, fontsize=12.5, fontweight="bold", color=MIDNIGHT)
    fig.subplots_adjust(top=0.84)
    return save(fig, FIG_DIR / "fig07_route_accessibility_rate.png")


def main() -> None:
    apply_rcparams()
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(DATA_CSV, parse_dates=["Date_ISO"])
    for build in (
        fig01_monthly_demand_trend, fig02_city_demand_comparison, fig03_mode_cost_recovery,
        fig04_delay_distribution_boxplot, fig05_delay_rating_relationship,
        fig06_weather_mode_delay_heatmap, fig07_route_accessibility_rate,
    ):
        build(df)
    print("All 7 advanced data-science figures generated successfully.")


if __name__ == "__main__":
    main()
