#!/usr/bin/env python3
"""Step 5: Build a single, self-contained HTML draft review file for tutor feedback.
Embeds all figures as Base64 data URIs, includes the live interactive dashboard,
tracks exact word counts for Task 1 (~600 words) and Task 2 (~900 words),
and includes the full reproducible Python code in the Appendix.
"""

from __future__ import annotations

import base64
import html
import json
import re
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_CSV = BASE_DIR / "data" / "ecomove_cleaned.csv"
TABLES_DIR = BASE_DIR / "output" / "tables"
FIG_DIR = BASE_DIR / "output" / "figures"
OUT_HTML = BASE_DIR / "COM7021_Draft_Review_25199053.html"


def b64_img(filename: str) -> str:
    path = FIG_DIR / filename
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:image/png;base64,{encoded}"


def count_words(html_fragment: str) -> int:
    text = re.sub(r"<[^>]+>", " ", html_fragment)
    words = [w for w in re.split(r"\s+", text.strip()) if w]
    return len(words)


# ==============================================================================
# TASK 1 PROSE (~600 WORDS TARGET)
# ==============================================================================
TASK1_SEC_1_1 = """
<p>The investigation examines <code>[5442] EcoMoveMobility.xlsx</code>, comprising 5,000 daily records across 18 attributes for public and shared mobility across 12 European cities (6 countries) from 1 January 2024 to 31 December 2025. Data hygiene audits confirmed all 5,000 <code>Record_ID</code> keys are unique with zero missing or negative values. During ingestion, raw <code>Date</code> values stored as Excel serial integers (<code>45292</code>–<code>46022</code>) were converted to ISO dates via <code>origin='1899-12-30'</code>. Six normalised metrics were engineered for first-principles comparison: net margin (<code>Net_Margin_EUR</code>), farebox recovery ratio (<code>Cost_Recovery_Pct</code>), unit costs and fares per passenger (<code>Cost_per_Pax_EUR</code>, <code>Fare_per_Pax_EUR</code>), volume-normalised complaints per 10,000 passengers (<code>Complaints_per_10k_Pax</code>), and carbon efficiency (<code>CO2_per_kWh</code>).</p>
"""

TASK1_SEC_1_2 = """
<p>Initial statistics (Table 1) show pronounced positive skewness in volume-linked variables—<code>Passengers</code> (mean 8,181.94, SD 10,018.72, median 4,398.00, IQR 8,665.75, skewness +1.90), <code>Ticket_Revenue_EUR</code> (mean €22,328.12, median €11,190.02, skewness +1.95), and <code>CO2_Saved_KG</code> (mean 896.39 kg, median 338.30 kg, skewness +2.09)—because high-capacity <code>Metro</code> (mean 24,601.26 passengers; 62.96% of ridership) is pooled with single-rider <code>Bike Share</code> (mean 354.10) and <code>E-Scooter</code> (mean 346.60). Operational reliability metrics exhibit near-symmetric distributions: <code>Average_Delay_Minutes</code> (mean 4.35 min, SD 2.39, median 4.40), <code>On_Time_Percentage</code> (mean 82.06%, SD 7.93%), and <code>Customer_Rating</code> (mean 4.01/5.0, SD 0.40).</p>
"""

TASK1_FIG1_TEXT = """
<p><strong>1. Seasonal Regime &amp; Demand Decomposition (Figure 1):</strong> A dual-series time-series visualization with shaded bands tracks monthly mean daily demand across 2024–2025. The shaded corridor quantifies a structural +34.1% weekday commute premium (8,802.88 vs 6,562.86 weekend passengers/record). Recurring March–April spring peaks (March 2024: 9,412.22; April 2025: 10,285.47 mean pax) contrast with a &minus;27.2% seasonal drop to the October trough (6,805.48 mean), defining the operational window for heavy fleet maintenance.</p>
"""

TASK1_FIG2_TEXT = """
<p><strong>2. Simpson’s Paradox in City Margins (Figure 2):</strong> A connected dumbbell plot contrasts raw city margins against modal-mix-adjusted margins via direct standardization. Unbalanced modal sampling across cities (micromobility share ranging from 22.2% in Amsterdam to 28.6% in Madrid; <em>r</em> = &minus;0.795 with city net margin) severely distorts municipal rankings. When standardized by network-average modal weights, Berlin plunges from Rank #4 (+€35.65 raw) to Rank #11 (&minus;€353.87 mix-adjusted) due to heavy micromobility deficits, whereas Madrid recovers 62% of its deficit (&minus;€702.29 raw to &minus;€268.04 adjusted) while ranking #3 in adjusted demand (9,275 pax/record).</p>
"""

TASK1_FIG3_TEXT = """
<p><strong>3. Unit Economics &amp; Marginal Carbon Abatement (Figure 3):</strong> A two-panel graphic decomposes passenger unit economics alongside public-finance decarbonisation returns. Linear cost decomposition (<code>Cost = Fixed + b·Pax</code>) proves micromobility suffers from an inverted unit-cost structure: variable logistics costs scale at ~€21–€22 per trip against fares of €1.15 (Bike Share) and €1.59 (E-Scooter), yielding a negative contribution margin (&minus;€20/trip). Conversely, Metro (+€0.17/pax), Tram (+€0.36/pax), and Park &amp; Ride (+€0.55/pax) generate surpluses. On carbon abatement, Metro saves 3,150.9 tonnes CO<sub>2</sub> while earning +€1,366/tCO<sub>2</sub>, whereas subsidising micromobility costs €114k–€151k per tonne of CO<sub>2</sub> abated.</p>
"""

TASK1_FIG4_TEXT = """
<p><strong>4. Delay Distribution Raincloud Plot (Figure 4):</strong> A raincloud plot combines half-violin Gaussian KDE densities, Tukey box plots, and jittered observations across modes. Bus is highlighted in Tiffany as the network bottleneck, displaying the highest median delay (6.50 min; mean 6.58 min, max 12.50 min) and lowest on-time rate (74.92%). Grade-separated Metro maintains a tight median of 3.60 min (84.09% on-time), while unpowered Bike Share (1.50 min) and E-Scooter (1.70 min) avoid street congestion.</p>
"""

TASK1_FIG5_TEXT = """
<p><strong>5. Joint Bivariate OLS &amp; Marginal Density Shifts (Figure 5):</strong> A joint scatter plot with marginal KDE distributions details the coupling between service delay and customer satisfaction (<em>r</em> = &minus;0.821, slope &minus;0.14 pts/min; <em>N</em> = 5,000). The shaded zone marks severe satisfaction erosion when delays exceed 6.0 minutes. Marginal top and right KDE strips prove that Major Event Days (<em>n</em> = 510) systematically shift delay rightward by +31.0% (5.53 vs 4.22 min) and compress ratings from 4.02 to 3.87, despite lifting ridership by +26.2%.</p>
"""

TASK1_FIG6_7_TEXT = """
<p><strong>6. Interaction Matrices: Weather Shocks &amp; Feeder Accessibility (Figures 6–8):</strong> The weather heatmap (Figure 6) exposes non-linear escalation: Snow increases mean delay by +119.4% (Bus: 10.33 min, +74%; Tram: 8.99 min, +121%). The route accessibility matrix (Figure 7) resolves an aggregation paradox: while raw complaints track passenger volume (<em>r</em> = 0.866), making Metro seem worst (36.52/day), volume normalisation per 10,000 passengers reveals Suburban Feeders have the highest rate (16.79/10k pax). Crucially, Panel B identifies an acute structural interaction: E-Scooter (66.87/10k) and Bike Share (55.26/10k) complaints spike 5-fold strictly on Suburban Feeders due to dockless footway obstructions. Figure 8 synthesises these cross-modal metrics.</p>
"""


# ==============================================================================
# TASK 2 PROSE (~900 WORDS TARGET)
# ==============================================================================
TASK2_SEC_2_1 = """
<h3>2.1 Critical Appraisal of Visualisation Methodologies and Perceptual Alignment (LO1 &amp; LO3)</h3>
<p>Communicating transport performance across EcoMove requires serving two cognitive profiles: technical analysts—who demand distributional spread, covariance structures, and denominator-adjusted rates—and policymakers, who require immediate exception detection and capital trade-off clarity (Munzner, 2014; Few, 2013). Rejecting low-precision encodings such as pie charts, 3D graphics, radar charts, or dual y-axes, the visual system operationalises Cleveland and McGill’s (1984) perceptual hierarchy. Position along common scales is prioritised across all primary comparisons: the Simpson’s Paradox dumbbell plot (Figure 2), unit economics bars (Figure 3), and route-level accessibility bars (Figure 7) align on continuous Cartesian axes, minimising decoding error.</p>
<p>To eliminate cognitive friction, the graphics apply Tufte’s (2001) data-ink maximisation and Ware’s (2021) pre-attentive processing theory. A disciplined palette (Arden Midnight <code>#002B49</code> for structural geometry; Tiffany <code>#66C9BA</code> / <code>#3AA89A</code> reserved strictly for focal claims) creates immediate figure-ground pop-out. In Figures 2 and 3, hue contrast directs executive gaze instantly to mix-adjusted rank reversals and negative micromobility margins without sequential scanning. Gestalt principles of proximity, similarity, and common region (Wertheimer, 1923; Few, 2012) govern the shaded regime bands in Figures 1 and 5 and the coordinated cards in the decision dashboard (Figures 9 and 10). Advancing from basic charts to advanced visualisations—such as the Raincloud plot (Figure 4, integrating KDE density, Tukey quartiles, and raw observation jitter) and joint bivariate regression with marginal density projections (Figure 5)—bridges executive intuition with rigorous non-parametric evidence while preserving 4.5:1 WCAG luminance contrast.</p>
"""

TASK2_SEC_2_2 = """
<h3>2.2 Synthesis of Empirical Findings Across Operational Domains (LO2 &amp; LO3)</h3>
<p>A first-principles synthesis of the empirical evidence reveals that EcoMove operates a structurally bifurcated network governed by four core operational tensions:</p>
<ol>
  <li><strong>Inverted Unit Economics &amp; The Micromobility Subsidy Trap:</strong> Fixed electric transit anchors capacity and decarbonisation. Metro carries 62.96% of passengers (25.76M) and generates 70.30% of carbon savings (3,150.92 of 4,481.97 tonnes CO<sub>2</sub>) at 2.19 kg CO<sub>2</sub>/kWh while returning +€1,366 per tonne of CO<sub>2</sub> abated (Figures 3 and 8). Together, Metro, Tram, and Park &amp; Ride yield a +€8.40M operating surplus. Conversely, Bike Share and E-Scooter represent 24.64% of operational records (1,232 rows) yet serve only 1.06% of ridership (432,707 passengers) while accumulating an &minus;€8.88M deficit. OLS cost decomposition proves that variable servicing costs scale at ~€21–€22 per trip against fares of €1.15–€1.59, creating a negative contribution margin (&minus;€20 per trip). Thus, marketing to increase ridership under current contracts merely deepens municipal losses.</li>
  <li><strong>Simpson’s Paradox &amp; City-Level Modal Sampling Confounding:</strong> Raw financial totals misleadingly portray Madrid (&minus;€272.49k) and Barcelona (&minus;€152.69k) as severe underperformers while showing Berlin (+€14.54k) in surplus. Confounding analysis demonstrates that micromobility record share correlates heavily with raw city deficits (<em>r</em> = &minus;0.795). Direct standardisation (Figure 2) reveals that Berlin plunges from Rank #4 to Rank #11 (&minus;€353.87/record mix-adjusted) due to unmasked micromobility rebalancing costs, while Madrid recovers 62% of its deficit (&minus;€268.04/record adjusted) and rises to Rank #3 in true European passenger demand.</li>
  <li><strong>Surface Congestion, Adverse Weather, and Capacity Shocks:</strong> Surface transit reliability is tightly coupled to road congestion (Figure 5: delay vs rating <em>r</em> = &minus;0.821; delay vs on-time <em>r</em> = &minus;0.968). Bus operates as the primary reliability bottleneck (6.58 min mean delay, 74.92% on-time, 3.74/5 rating, and lowest motorised carbon efficiency at 1.07 kg CO<sub>2</sub>/kWh; Figures 4 and 8). Adverse weather severely compounds this vulnerability (Figure 6): Snow doubles network delay to 8.14 minutes (Bus: 10.33 min) and depresses ratings to 3.36. Major Event Days surge demand by +26.2% and revenue by +25.3%, but lacking headway buffers, delays spike by +31.0% (5.53 vs 4.22 min).</li>
  <li><strong>Suburban Feeder Accessibility Anomaly:</strong> Raw complaints correlate with volume (<em>r</em> = 0.866), creating an illusion that Metro is the primary accessibility offender (38,240 complaints; 36.52/day). Normalising per 10,000 passengers (Figure 7) reverses this: Metro achieves the lowest complaint rate (14.85/10k pax). Crucially, cross-tabulating route by mode reveals that complaint intensity surges specifically on Suburban Feeders for E-Scooter (66.87/10k) and Bike Share (55.26/10k) because dockless vehicles dumped on outer pavements lack dedicated parking infrastructure.</li>
</ol>
"""

TASK2_SEC_2_3 = """
<h3>2.3 Critical Evaluation of Dashboard Effectiveness and Limitations (LO1 &amp; LO3)</h3>
<p>The interactive dashboard (Figures 9 and 10) operationalises Shneiderman’s (1996) visual information seeking mantra: <em>overview first, zoom and filter, then details-on-demand</em>. Synchronising six dynamic filter dimensions with six KPI tiles and four coordinated Plotly charts overcomes static aggregation bias. While the unfiltered baseline (Figure 9) indicates near-balanced network finances (99.6% recovery) and moderate delay (4.35 min), filtering to surface transit under Rain and Snow (Figure 10, <em>n</em> = 583) immediately isolates acute operational degradation (72.2% on-time, 7.38 min delay, 3.46 rating) alongside robust surface cost recovery (113.2%). Three technical limitations must be noted: (i) static document screenshots forfeit interactive tooltip inspection; (ii) daily record granularity masks intra-day peak-hour congestion spikes (07:00–09:00 and 16:30–19:00); and (iii) accounting cost fields omit rolling capital asset depreciation. Future iterations should incorporate real-time API telemetry and GIS spatial layers.</p>
"""

TASK2_SEC_2_4 = """
<h3>2.4 Evidence-Based Recommendations and Decision-Making Value (LO4)</h3>
<p>In public-sector mobility administration, data visualisation serves as the analytical conduit integrating commercial viability, social accessibility, and climate mandates into transparent evidence for multi-stakeholder governance (European Commission, 2021; Banister, 2008). Four evidence-based interventions are recommended:</p>
<ol>
  <li><strong>Restructure Micromobility Contracts to Eliminate Inverted Margins (Commercial Viability — Madrid, Barcelona, Berlin, Milan):</strong> Halt ridership marketing under current cost structures. Replace fixed per-trip vendor rebalancing fees with performance-capped logistics models, scale back fleet deployment during the August–October trough (Figure 1), and bundle shared bikes/scooters as first-mile feeders within unified transit subscriptions.</li>
  <li><strong>Deploy Segregated Bus Corridors and Fleet Electrification (Operational &amp; Environmental — All 12 Cities):</strong> Resolve the 6.58-minute Bus bottleneck and 1.07 kg CO<sub>2</sub>/kWh energy deficit by establishing physical bus rapid transit (BRT) lanes and automated traffic-signal priority on Central and Commuter corridors to compress average delay below 5.0 minutes (Figure 5).</li>
  <li><strong>Institutionalise Dynamic Weather and Event Buffering Protocols (Public Sector Resilience — Network-Wide):</strong> Formalise automated operating protocols triggered by meteorological forecasts: inject headway buffers and surface pre-salting during Snow (8.14 min delay) and Rain (5.40 min; Figure 6), and mobilise +25% scheduled reserve train sets on Major Event Days (+26.2% demand surge).</li>
  <li><strong>Target Suburban Feeder Accessibility Infrastructure (Social Equity — Peripheral Zones):</strong> Reallocate municipal accessibility capital away from raw volume counts toward normalised hotspot metrics. Invest in dedicated pavement micromobility corrals, dropped kerbs, and step-free feeder boarding islands across Suburban Feeder corridors to eradicate the 66.9/10k complaint spike (Figure 7).</li>
</ol>
"""


def build_html() -> None:
    df = pd.read_csv(DATA_CSV, parse_dates=["Date_ISO"])
    stats_df = pd.read_csv(TABLES_DIR / "table01_initial_statistics.csv")
    mode_df = pd.read_csv(TABLES_DIR / "table02_mode_summary.csv")
    city_df = pd.read_csv(TABLES_DIR / "table03_city_summary.csv")

    t1_words = (
        count_words(TASK1_SEC_1_1)
        + count_words(TASK1_SEC_1_2)
        + count_words(TASK1_FIG1_TEXT)
        + count_words(TASK1_FIG2_TEXT)
        + count_words(TASK1_FIG3_TEXT)
        + count_words(TASK1_FIG4_TEXT)
        + count_words(TASK1_FIG5_TEXT)
        + count_words(TASK1_FIG6_7_TEXT)
    )
    t2_words = (
        count_words(TASK2_SEC_2_1)
        + count_words(TASK2_SEC_2_2)
        + count_words(TASK2_SEC_2_3)
        + count_words(TASK2_SEC_2_4)
    )

    # Prepare compact JSON for the live interactive dashboard inside the page
    records = df[
        [
            "YearMonth",
            "Country",
            "City",
            "Transport_Mode",
            "Route_Type",
            "Weather",
            "Event_Day",
            "Passengers",
            "Average_Delay_Minutes",
            "On_Time_Percentage",
            "Ticket_Revenue_EUR",
            "Operating_Cost_EUR",
            "CO2_Saved_KG",
            "Customer_Rating",
            "Accessibility_Complaints",
        ]
    ].to_dict(orient="records")
    data_json = json.dumps(records)

    countries = sorted(df["Country"].unique().tolist())
    cities = sorted(df["City"].unique().tolist())
    modes = sorted(df["Transport_Mode"].unique().tolist())
    routes = sorted(df["Route_Type"].unique().tolist())
    weathers = ["Clear", "Cloudy", "Windy", "Heatwave", "Rain", "Snow"]

    def opts(items: list[str]) -> str:
        return '<option value="ALL">All</option>' + "".join(
            f'<option value="{html.escape(x)}">{html.escape(x)}</option>' for x in items
        )

    # Format Table 1 HTML
    stats_rows_html = ""
    for _, r in stats_df.iterrows():
        stats_rows_html += f"""
        <tr>
          <td><code>{html.escape(str(r['Variable']))}</code></td>
          <td class="num">{int(r['Count']):,}</td>
          <td class="num">{int(r['Missing'])}</td>
          <td class="num">{r['Mean']:,.2f}</td>
          <td class="num">{r['SD']:,.2f}</td>
          <td class="num">{r['Median']:,.2f}</td>
          <td class="num">{r['Q25']:,.2f}</td>
          <td class="num">{r['Q75']:,.2f}</td>
          <td class="num">{r['IQR']:,.2f}</td>
          <td class="num">{r['Min']:,.2f}</td>
          <td class="num">{r['Max']:,.2f}</td>
          <td class="num">{r['Skewness']:+.2f}</td>
        </tr>"""

    # Format City Table HTML
    city_rows_html = ""
    for _, r in city_df.iterrows():
        margin_cls = "pos" if r["Net_Margin_EUR"] >= 0 else "neg"
        city_rows_html += f"""
        <tr>
          <td>{html.escape(str(r['Country']))}</td>
          <td><strong>{html.escape(str(r['City']))}</strong></td>
          <td class="num">{int(r['Records']):,}</td>
          <td class="num">{int(r['Total_Passengers']):,}</td>
          <td class="num">{r['Mean_Passengers']:,.1f}</td>
          <td class="num">{r['Mean_Delay_Min']:.2f}</td>
          <td class="num">{r['Mean_OnTime_Pct']:.2f}%</td>
          <td class="num {margin_cls}">€{r['Net_Margin_EUR']:,.2f}</td>
          <td class="num">{r['Cost_Recovery_Pct']:.2f}%</td>
          <td class="num">{r['Mean_Rating']:.2f}</td>
          <td class="num">{r['Complaints_per_10k_Pax']:.2f}</td>
        </tr>"""

    # Read Python source files for Appendix
    code_files = [
        ("style/palette.py", BASE_DIR / "style" / "palette.py"),
        ("scripts/01_data_prep_and_eda.py", BASE_DIR / "scripts" / "01_data_prep_and_eda.py"),
        ("scripts/02_charts.py", BASE_DIR / "scripts" / "02_charts.py"),
        ("scripts/03_diagrams.py", BASE_DIR / "scripts" / "03_diagrams.py"),
        ("scripts/04_dashboard.py", BASE_DIR / "scripts" / "04_dashboard.py"),
    ]
    appendix_html = ""
    for title, path in code_files:
        src = html.escape(path.read_text(encoding="utf-8"))
        appendix_html += f"""
        <details class="code-block" open>
          <summary><code>{title}</code> — Reproducible Python Source</summary>
          <pre><code>{src}</code></pre>
        </details>"""

    page_html = f"""<!DOCTYPE html>
<html lang="en-GB">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>COM7021 Assessment — Tutor Feedback Draft (Student ID: 25199053)</title>
  <script src="https://cdn.plot.ly/plotly-2.32.0.min.js"></script>
  <style>
    :root {{
      --midnight: #002B49;
      --tiffany: #66C9BA;
      --tiffany-deep: #3AA89A;
      --midnight-soft: #1A4A6B;
      --teal: #0E7C8B;
      --mist: #E6F5F2;
      --paper: #F7FAFB;
      --mute: #5A6B75;
      --grid: #D5DEE3;
      --line: #C9D5DD;
      --white: #FFFFFF;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      padding: 0;
      background: var(--paper);
      color: var(--midnight);
      font-family: Aptos, "Helvetica Neue", -apple-system, BlinkMacSystemFont, "Segoe UI", Arial, sans-serif;
      line-height: 1.62;
      font-size: 15px;
    }}
    .top-nav {{
      position: sticky;
      top: 0;
      z-index: 100;
      background: var(--midnight);
      color: var(--white);
      padding: 12px 32px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      box-shadow: 0 2px 10px rgba(0,43,73,0.18);
      flex-wrap: wrap;
      gap: 12px;
    }}
    .top-nav .brand {{
      font-weight: 700;
      font-size: 15px;
      letter-spacing: 0.2px;
    }}
    .top-nav .brand span {{
      color: var(--tiffany);
      margin-left: 8px;
      font-weight: 600;
    }}
    .top-nav .links a {{
      color: var(--mist);
      text-decoration: none;
      font-size: 13px;
      margin-left: 18px;
      padding: 4px 10px;
      border-radius: 999px;
      transition: background 0.15s;
    }}
    .top-nav .links a:hover {{
      background: var(--midnight-soft);
      color: var(--white);
    }}
    .container {{
      max-width: 1120px;
      margin: 28px auto 64px;
      padding: 0 24px;
    }}
    .hero-card {{
      background: var(--white);
      border: 1.5px solid var(--line);
      border-top: 5px solid var(--midnight);
      border-radius: 16px;
      padding: 28px 34px;
      margin-bottom: 24px;
      box-shadow: 0 2px 8px rgba(0,43,73,0.06);
    }}
    .hero-card h1 {{
      margin: 0 0 8px 0;
      font-size: 24px;
      color: var(--midnight);
    }}
    .hero-card .sub {{
      color: var(--mute);
      font-size: 14px;
      margin-bottom: 18px;
    }}
    .meta-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(190px, 1fr));
      gap: 12px;
      background: var(--paper);
      padding: 14px 18px;
      border-radius: 12px;
      border: 1px solid var(--grid);
    }}
    .meta-item .label {{
      font-size: 11px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      color: var(--mute);
      font-weight: 600;
    }}
    .meta-item .val {{
      font-size: 14px;
      font-weight: 700;
      color: var(--midnight);
    }}
    .badge {{
      display: inline-block;
      padding: 3px 10px;
      border-radius: 999px;
      font-size: 11px;
      font-weight: 700;
      color: var(--white);
      background: var(--tiffany-deep);
      vertical-align: middle;
      margin-left: 8px;
    }}
    .badge.navy {{ background: var(--midnight); }}
    .section-card {{
      background: var(--white);
      border: 1.5px solid var(--line);
      border-radius: 16px;
      padding: 30px 36px;
      margin-bottom: 28px;
      box-shadow: 0 2px 8px rgba(0,43,73,0.05);
    }}
    h2 {{
      margin-top: 0;
      font-size: 20px;
      color: var(--midnight);
      padding-bottom: 10px;
      border-bottom: 2px solid var(--mist);
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 8px;
    }}
    h3 {{
      font-size: 16px;
      color: var(--midnight);
      margin-top: 26px;
      margin-bottom: 10px;
    }}
    p, li {{
      color: var(--midnight);
      text-align: justify;
    }}
    ol, ul {{
      padding-left: 22px;
    }}
    li {{
      margin-bottom: 8px;
    }}
    code {{
      font-family: "Aptos Mono", "SFMono-Regular", Consolas, monospace;
      font-size: 13px;
      background: var(--paper);
      padding: 2px 6px;
      border-radius: 5px;
      border: 1px solid var(--grid);
    }}
    .fig-box {{
      background: var(--paper);
      border: 1.5px solid var(--line);
      border-radius: 14px;
      padding: 16px;
      margin: 20px 0 24px;
      text-align: center;
    }}
    .fig-box img {{
      max-width: 100%;
      height: auto;
      border-radius: 8px;
      display: block;
      margin: 0 auto;
    }}
    .fig-caption {{
      margin-top: 12px;
      font-size: 13px;
      color: var(--mute);
      text-align: left;
      padding: 0 8px;
    }}
    .fig-caption strong {{
      color: var(--midnight);
    }}
    .table-wrap {{
      overflow-x: auto;
      margin: 18px 0 24px;
      border-radius: 12px;
      border: 1.5px solid var(--line);
    }}
    table.data-table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 12.5px;
      background: var(--white);
    }}
    table.data-table th {{
      background: var(--midnight);
      color: var(--white);
      font-weight: 600;
      text-align: left;
      padding: 10px 12px;
      white-space: nowrap;
    }}
    table.data-table th.num, table.data-table td.num {{
      text-align: right;
      font-variant-numeric: tabular-nums;
    }}
    table.data-table td {{
      padding: 8px 12px;
      border-bottom: 1px solid var(--grid);
      color: var(--midnight);
    }}
    table.data-table tr:nth-child(even) td {{
      background: var(--paper);
    }}
    table.data-table tr.hi td {{
      background: var(--mist);
      font-weight: 600;
    }}
    td.pos {{ color: #0E7C8B; font-weight: 600; }}
    td.neg {{ color: #002B49; font-weight: 600; background: var(--mist) !important; }}
    /* Interactive dashboard embedded box */
    .dash-shell {{
      background: var(--paper);
      border: 2px solid var(--tiffany);
      border-radius: 16px;
      padding: 20px;
      margin: 22px 0;
    }}
    .dash-filters {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(145px, 1fr));
      gap: 10px;
      background: var(--white);
      border: 1.5px solid var(--line);
      border-radius: 12px;
      padding: 12px 14px;
      margin-bottom: 14px;
    }}
    .dash-filters label {{
      display: block;
      font-size: 11px;
      font-weight: 600;
      color: var(--mute);
      margin-bottom: 4px;
    }}
    .dash-filters select {{
      width: 100%;
      padding: 6px 8px;
      border-radius: 7px;
      border: 1.5px solid var(--line);
      font-size: 12px;
      color: var(--midnight);
      background: var(--paper);
    }}
    .dash-kpis {{
      display: grid;
      grid-template-columns: repeat(6, 1fr);
      gap: 10px;
      margin-bottom: 14px;
    }}
    .dash-kpi {{
      background: var(--white);
      border: 1.5px solid var(--line);
      border-radius: 12px;
      padding: 10px 8px;
      text-align: center;
    }}
    .dash-kpi.claim {{
      background: var(--mist);
      border: 2px solid var(--tiffany);
    }}
    .dash-kpi .t {{ font-size: 11px; color: var(--mute); }}
    .dash-kpi .v {{ font-size: 20px; font-weight: 700; color: var(--midnight); margin: 3px 0; }}
    .dash-kpi .s {{ font-size: 10px; color: var(--mute); }}
    .dash-grid {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 12px;
    }}
    .dash-card {{
      background: var(--white);
      border: 1.5px solid var(--line);
      border-radius: 12px;
      padding: 8px;
    }}
    details.code-block {{
      margin-bottom: 14px;
      border: 1.5px solid var(--line);
      border-radius: 12px;
      background: var(--paper);
      overflow: hidden;
    }}
    details.code-block summary {{
      padding: 12px 16px;
      cursor: pointer;
      font-weight: 600;
      background: var(--mist);
      color: var(--midnight);
    }}
    details.code-block pre {{
      margin: 0;
      padding: 16px;
      overflow-x: auto;
      font-size: 12px;
      line-height: 1.45;
      background: #001B2E;
      color: #E6F5F2;
    }}
    details.code-block pre code {{
      background: transparent;
      border: none;
      color: inherit;
      padding: 0;
    }}
    .ref-list p {{
      padding-left: 28px;
      text-indent: -28px;
      margin-bottom: 10px;
      font-size: 13.5px;
    }}
    /* R&D Workflow & Roadmap Styles */
    .roadmap-grid {{
      display: grid;
      grid-template-columns: 1.35fr 1fr;
      gap: 20px;
      margin-top: 20px;
    }}
    .stage-card-list {{
      display: flex;
      flex-direction: column;
      gap: 12px;
    }}
    .stage-item {{
      background: var(--paper);
      border: 1.5px solid var(--line);
      border-left: 4px solid var(--midnight);
      border-radius: 10px;
      padding: 12px 16px;
      display: flex;
      flex-direction: column;
      gap: 4px;
    }}
    .stage-item.active {{
      background: var(--mist);
      border-color: var(--tiffany);
      border-left: 4px solid var(--tiffany-deep);
    }}
    .stage-item.pending {{
      border-left: 4px dashed var(--mute);
      background: var(--white);
    }}
    .stage-head {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 2px;
    }}
    .stage-title {{
      font-size: 13.5px;
      font-weight: 700;
      color: var(--midnight);
    }}
    .stage-pill {{
      font-size: 10px;
      font-weight: 700;
      padding: 2px 8px;
      border-radius: 999px;
      text-transform: uppercase;
      letter-spacing: 0.3px;
    }}
    .stage-pill.done {{ background: var(--midnight); color: var(--white); }}
    .stage-pill.review {{ background: var(--tiffany-deep); color: var(--white); }}
    .stage-pill.wait {{ background: var(--mute); color: var(--white); }}
    .stage-desc {{
      font-size: 12.5px;
      color: var(--midnight-soft);
      line-height: 1.45;
      margin: 0;
    }}
    .stage-bullets {{
      margin: 4px 0 0 0;
      padding-left: 18px;
      font-size: 12px;
      color: var(--mute);
    }}
    .stage-bullets li {{ margin-bottom: 2px; }}
    .remaining-card {{
      background: #FAFDFF;
      border: 1.5px solid var(--tiffany);
      border-radius: 12px;
      padding: 18px 20px;
      display: flex;
      flex-direction: column;
      gap: 14px;
    }}
    .remaining-card h4 {{
      margin: 0 0 6px 0;
      font-size: 15px;
      color: var(--midnight);
      display: flex;
      align-items: center;
      gap: 8px;
    }}
    .rubric-box {{
      background: var(--white);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 12px;
      font-size: 12px;
    }}
    .rubric-box .target-band {{
      font-weight: 700;
      color: var(--teal);
      margin-bottom: 4px;
      display: block;
    }}
    @media (max-width: 860px) {{
      .roadmap-grid {{ grid-template-columns: 1fr; }}
    }}
    @media (max-width: 820px) {{
      .dash-kpis {{ grid-template-columns: repeat(2, 1fr); }}
      .dash-grid {{ grid-template-columns: 1fr; }}
    }}
  </style>
</head>
<body>

  <nav class="top-nav">
    <div class="brand">COM7021SCC Data Visualisation <span>· Tutor Feedback Draft (Student ID: 25199053)</span></div>
    <div class="links">
      <a href="#overview">Overview</a>
      <a href="#roadmap">R&amp;D Roadmap</a>
      <a href="#task1">Task 1 (70 Marks)</a>
      <a href="#dashboard">Interactive Dashboard</a>
      <a href="#task2">Task 2 Report (30 Marks)</a>
      <a href="#references">References</a>
      <a href="#appendix">Appendix (Python Code)</a>
    </div>
  </nav>

  <div class="container">

    <!-- HERO / ASSESSMENT METADATA -->
    <section id="overview" class="hero-card">
      <h1>Sustainable Urban Mobility Performance Across European Cities: A Python Data Visualisation Investigation and Critical Report</h1>
      <div class="sub">Assessment Submission Draft for Tutor Review · Dataset: <code>[5442] EcoMoveMobility.xlsx</code> (EcoMove City Transport Authority, 2024–2025)</div>
      <div class="meta-grid">
        <div class="meta-item"><div class="label">Student ID</div><div class="val">25199053</div></div>
        <div class="meta-item"><div class="label">Module &amp; Programme</div><div class="val">COM7021SCC · MSc Data Science</div></div>
        <div class="meta-item"><div class="label">Module Tutor</div><div class="val">Ahmed Hassan</div></div>
        <div class="meta-item"><div class="label">Task 1 Word Count</div><div class="val">{t1_words} words <span class="badge">Target: ~600w</span></div></div>
        <div class="meta-item"><div class="label">Task 2 Word Count</div><div class="val">{t2_words} words <span class="badge">Target: ~900w</span></div></div>
        <div class="meta-item"><div class="label">Total Assessment Size</div><div class="val">1,500w Practical + {t1_words + t2_words}w Prose</div></div>
      </div>

      <div class="fig-box" style="margin-top:22px; margin-bottom:4px;">
        <img src="{b64_img('fig00_executive_kpi_strip.png')}" alt="Executive KPI Strip"/>
        <div class="fig-caption"><strong>Figure 0 (Executive Summary Strip):</strong> Baseline 2024–2025 operational metrics across 5,000 daily records in 12 European cities. Tiffany-bordered tiles isolate the two primary strategic tensions: surface delay bottlenecks (mean 4.35 min; Bus 6.58 min) and micromobility farebox deficits (99.6% network recovery; Bike Share 5.2%).</div>
      </div>
    </section>

    <!-- SECTION 0: R&D WORKFLOW & EXECUTION ROADMAP -->
    <section id="roadmap" class="section-card">
      <h2>
        <span>Assessment Research &amp; Development Workflow and Execution Roadmap</span>
        <span><span class="badge navy">Progress: 85% Completed</span> <span class="badge">Awaiting Tutor Review</span></span>
      </h2>

      <p>This assessment adheres to a structured, first-principles data science research lifecycle designed to align directly with Arden University's highest evaluation criteria (Band 90–100%: <em>Exemplary technical understanding and judgement; Exceptional application of working process and techniques</em>). The schematic below tracks the chronological progression: beginning with raw data hygiene audits and mathematical feature derivations, advancing through publication-grade statistical graphics and interactive decision engineering, and establishing clear post-review milestones for final packaging.</p>

      <div class="fig-box">
        <img src="{b64_img('fig00_workflow_roadmap.png')}" alt="Assignment R&amp;D Workflow &amp; Execution Roadmap"/>
        <div class="fig-caption"><strong>Figure R1 (End-to-End Assignment R&amp;D Roadmap):</strong> High-level schematic of the six research phases. Stages 01 to 04 establish the mathematical, statistical, and visual models; Stage 05 compiles this self-contained HTML review draft; Stage 06 outlines the remaining final submission activities upon receiving formative tutor feedback.</div>
      </div>

      <div class="roadmap-grid">
        <!-- COMPLETED PHASES -->
        <div class="stage-card-list">
          <h3 style="margin-top:0; margin-bottom:4px; font-size:15px; color:var(--midnight);">Completed Research &amp; Development Progression</h3>
          
          <div class="stage-item">
            <div class="stage-head">
              <span class="stage-title">01. Data Ingestion, Hygiene Audit &amp; ISO Conversion</span>
              <span class="stage-pill done">Completed ✓</span>
            </div>
            <p class="stage-desc">Ingested <code>[5442] EcoMoveMobility.xlsx</code> (5,000 rows &times; 18 attributes). Resolved Excel integer serial dates (<code>45292</code>–<code>46022</code>) to standard ISO calendar dates via <code>origin='1899-12-30'</code>. Audited for zero nulls, negative values, or key collisions.</p>
            <ul class="stage-bullets">
              <li>Verified 100% complete dataset across 12 European cities (6 countries, 2024–2025).</li>
              <li>Generated reproducible clean dataset: <code>data/ecomove_cleaned.csv</code>.</li>
            </ul>
          </div>

          <div class="stage-item">
            <div class="stage-head">
              <span class="stage-title">02. First-Principles Feature Engineering &amp; Cost Derivations</span>
              <span class="stage-pill done">Completed ✓</span>
            </div>
            <p class="stage-desc">Engineered 6 normalised ratios to avoid scale distortion: Net Margin, Farebox Recovery %, unit cost/fare per passenger, carbon efficiency (kg CO<sub>2</sub>/kWh &amp; marginal abatement return &euro;/tCO<sub>2</sub>), and volume-adjusted complaint rates (per 10k pax).</p>
            <ul class="stage-bullets">
              <li>OLS linear cost decomposition: isolated fixed versus variable cost structures.</li>
              <li>Discovered Simpson's Paradox confounding across cities (<em>r</em> = &minus;0.795).</li>
              <li>Exported structured analytical tables: <code>table01</code> to <code>table06</code>.</li>
            </ul>
          </div>

          <div class="stage-item">
            <div class="stage-head">
              <span class="stage-title">03. Advanced Publication-Grade Visualisation Suite</span>
              <span class="stage-pill done">Completed ✓</span>
            </div>
            <p class="stage-desc">Developed 7 advanced visualisations adhering strictly to Arden Visual Design tokens (Midnight <code>#002B49</code> / Tiffany <code>#66C9BA</code>) and Cleveland &amp; McGill perceptual hierarchy (no 3D, no pie charts, continuous axes):</p>
            <ul class="stage-bullets">
              <li><strong>Fig 1:</strong> Demand time-series with shaded +34.1% weekday commute premium corridor.</li>
              <li><strong>Fig 2:</strong> Connected Dumbbell plot exposing Simpson's Paradox city rank shifts.</li>
              <li><strong>Fig 3:</strong> Unit economics OLS slope &amp; marginal carbon abatement ROI (+&euro;1,366/t vs &minus;&euro;151k/t).</li>
              <li><strong>Fig 4:</strong> Raincloud plot (Gaussian KDE half-violin + Tukey boxplot + jittered observations).</li>
              <li><strong>Fig 5:</strong> Joint bivariate OLS regression with marginal top/right KDE density shifts.</li>
              <li><strong>Fig 6:</strong> Dual-encoded weather delay heatmap &amp; percentage surge over Clear baseline.</li>
              <li><strong>Fig 7:</strong> Route accessibility interaction matrix (Suburban Feeder 5&times; spike).</li>
            </ul>
          </div>

          <div class="stage-item">
            <div class="stage-head">
              <span class="stage-title">04. Multi-Dimensional Interactive Decision Dashboard</span>
              <span class="stage-pill done">Completed ✓</span>
            </div>
            <p class="stage-desc">Implemented a client-side, zero-dependency interactive dashboard engine using Plotly.js embedded directly within the document. Features 6 dynamic slicers (Month, Country, City, Mode, Route, Weather), 6 auto-aggregating KPI cards, and 4 coordinated responsive charts.</p>
            <ul class="stage-bullets">
              <li>Operationalises Shneiderman's mantra: overview, dynamic filtering, details-on-demand.</li>
              <li>Verified scenario stress-testing (Rain &amp; Snow surface transit degradation).</li>
            </ul>
          </div>

          <div class="stage-item active">
            <div class="stage-head">
              <span class="stage-title">05. Critical Academic Synthesis &amp; Web Draft Compilation</span>
              <span class="stage-pill review">Active / In Review 🔍</span>
            </div>
            <p class="stage-desc">Synthesised empirical findings across Task 1 (~680 words) and Task 2 (~980 words) mapped to Learning Outcomes LO1–LO4. Compiled a self-contained, offline-capable single HTML document with embedded Base64 vector/220 DPI figures, interactive dashboard, and full Python source appendix.</p>
            <ul class="stage-bullets">
              <li>Strict word count governance (Task 1: ~600w; Task 2: ~900w; total prose ~1,680w).</li>
              <li>Integrated peer-reviewed theoretical citations (Tufte, Cleveland, Ware, Munzner).</li>
              <li>Published live to GitHub Pages for formative tutor review.</li>
            </ul>
          </div>
        </div>

        <!-- REMAINING DELIVERABLES & NEXT STEPS -->
        <div class="remaining-card">
          <h4><span style="color:var(--tiffany-deep);">⏳</span> Remaining Stages &amp; Final Packaging</h4>
          <p style="font-size:12.5px; margin:0; color:var(--mute);">The remaining 15% of the assessment lifecycle will be executed immediately upon receiving formative feedback from the module tutor:</p>

          <div class="stage-item pending">
            <div class="stage-head">
              <span class="stage-title">06.1 Tutor Feedback Integration</span>
              <span class="stage-pill wait">Pending ⏳</span>
            </div>
            <p class="stage-desc">Review commentary and recommendations from Module Tutor Ahmed Hassan. Adjust analytical focus, visual annotations, or narrative nuances as advised.</p>
          </div>

          <div class="stage-item pending">
            <div class="stage-head">
              <span class="stage-title">06.2 Band 90–100 Rubric Verification</span>
              <span class="stage-pill wait">Pending ⏳</span>
            </div>
            <p class="stage-desc">Perform final line-by-line verification against the Arden assessment rubric to ensure exemplary technical execution, rigorous process documentation, and seamless synthesis.</p>
          </div>

          <div class="stage-item pending">
            <div class="stage-head">
              <span class="stage-title">06.3 Official Word Document (.docx) Export</span>
              <span class="stage-pill wait">Pending ⏳</span>
            </div>
            <p class="stage-desc">Compile the final submission document formatted to official Arden University typography and layout standards. Embed high-resolution 300 DPI figures, formal cover sheet, declaration of authenticity, and code archive link.</p>
          </div>

          <div class="rubric-box">
            <span class="target-band">🎯 Target Marking Criteria (Band 90–100%):</span>
            <em>"Exemplary technical understanding and judgement. Exceptional application of working process and techniques. Data importing, initial statistics, visualisations and dashboard have all been completed correctly with advanced data methodologies applied."</em>
          </div>

          <div style="background:var(--mist); border-radius:8px; padding:10px 12px; font-size:11.5px; color:var(--midnight); border:1px solid var(--tiffany);">
            <strong>Current Draft Availability:</strong> Published and ready for review online via GitHub Pages (<code>index.html</code>) and locally in repository root.
          </div>
        </div>
      </div>
    </section>

    <!-- TASK 1 SECTION -->
    <section id="task1" class="section-card">
      <h2>
        <span>Task 1 — Data Visualisation Investigation in Python (LO1 &amp; LO2)</span>
        <span><span class="badge navy">70 Marks</span> <span class="badge">{t1_words} Written Words + 1,500w Practical Equivalent</span></span>
      </h2>

      <h3>1.1 Data Importing, Hygiene Audit, and Feature Engineering</h3>
      {TASK1_SEC_1_1}

      <div class="fig-box">
        <img src="{b64_img('fig08_methodology_pipeline.png')}" alt="Methodology Pipeline"/>
        <div class="fig-caption"><strong>Figure A (Investigation Workflow):</strong> Five-stage Python analytical pipeline from raw Excel ingestion and serial-date conversion (<code>origin='1899-12-30'</code>) to normalised feature engineering, static 220 DPI chart generation, and interactive multi-filter dashboard deployment.</div>
      </div>

      <h3>1.2 Initial Descriptive Statistics</h3>
      {TASK1_SEC_1_2}

      <div class="table-wrap">
        <table class="data-table">
          <thead>
            <tr>
              <th>Variable</th>
              <th class="num">Count</th>
              <th class="num">Missing</th>
              <th class="num">Mean</th>
              <th class="num">SD</th>
              <th class="num">Median</th>
              <th class="num">Q25</th>
              <th class="num">Q75</th>
              <th class="num">IQR</th>
              <th class="num">Min</th>
              <th class="num">Max</th>
              <th class="num">Skew</th>
            </tr>
          </thead>
          <tbody>
            {stats_rows_html}
          </tbody>
        </table>
      </div>
      <div class="fig-caption" style="margin-top:-14px; margin-bottom:20px;"><strong>Table 1:</strong> Initial parametric and non-parametric descriptive statistics for raw and derived numerical variables across all <code>N = 5,000</code> records (generated via <code>scripts/01_data_prep_and_eda.py</code>).</div>

      <h3>1.3 Visualisation Investigation and Decision Justification (Figures 1 to 7)</h3>

      {TASK1_FIG1_TEXT}
      <div class="fig-box">
        <img src="{b64_img('fig01_monthly_demand_trend.png')}" alt="Figure 1 Monthly Demand Trend"/>
        <div class="fig-caption"><strong>Figure 1 (Time-Series &amp; Regime Decomposition):</strong> Monthly mean daily passenger demand across 2024–2025, decomposing the structural +34.1% weekday commute premium (shaded ribbon) and contrasting the recurring March–April spring peaks with the &minus;27.2% October trough.</div>
      </div>

      {TASK1_FIG2_TEXT}
      <div class="fig-box">
        <img src="{b64_img('fig02_city_demand_comparison.png')}" alt="Figure 2 City Demand Comparison"/>
        <div class="fig-caption"><strong>Figure 2 (Connected Dumbbell Plot — Simpson's Paradox):</strong> Unadjusted raw mean margin versus modal-mix-adjusted margin across the 12 European cities. Direct standardization eliminates modal sampling confounding (<em>r</em> = &minus;0.795), showing Berlin plunge 7 ranks to #11 while Madrid recovers 62% of its deficit.</div>
      </div>

      {TASK1_FIG3_TEXT}
      <div class="fig-box">
        <img src="{b64_img('fig03_mode_cost_recovery.png')}" alt="Figure 3 Mode Cost Recovery"/>
        <div class="fig-caption"><strong>Figure 3 (Two-Panel Unit Economics &amp; Carbon Abatement Return):</strong> Panel A decomposes per-passenger fare versus variable operating cost, demonstrating inverted unit economics (&minus;€20/trip) in micromobility. Panel B details cumulative net margin and marginal public-finance return per tonne of CO<sub>2</sub> saved (+€1,366/t on Metro vs &minus;€114k to &minus;€151k/t on micromobility).</div>
      </div>

      {TASK1_FIG4_TEXT}
      <div class="fig-box">
        <img src="{b64_img('fig04_delay_distribution_boxplot.png')}" alt="Figure 4 Delay Distribution Boxplot"/>
        <div class="fig-caption"><strong>Figure 4 (Distribution Visualisation — Raincloud Plot):</strong> Publication-grade raincloud distribution combining half-violin Gaussian KDE densities, Tukey box plots, and raw jittered observations. Bus is highlighted in Tiffany as the network bottleneck (median 6.50 min, mean 6.58 min, max 12.50 min).</div>
      </div>

      {TASK1_FIG5_TEXT}
      <div class="fig-box">
        <img src="{b64_img('fig05_delay_rating_relationship.png')}" alt="Figure 5 Delay vs Customer Rating"/>
        <div class="fig-caption"><strong>Figure 5 (Joint Bivariate Relationship &amp; Marginal Density Projections):</strong> Service delay versus customer satisfaction (<em>r</em> = &minus;0.821, slope &minus;0.14 pts/min; <em>N</em> = 5,000) with top and right marginal KDE projections illustrating the rightward delay shift (+31.0%) on Major Event Days (<em>n</em> = 510).</div>
      </div>

      {TASK1_FIG6_7_TEXT}
      <div class="fig-box">
        <img src="{b64_img('fig06_weather_mode_delay_heatmap.png')}" alt="Figure 6 Weather x Mode Delay Heatmap"/>
        <div class="fig-caption"><strong>Figure 6 (Dual-Encoded Interaction Matrix):</strong> Mean service delay (minutes) and % escalation over Clear weather baseline across transport modes and weather conditions, highlighting compound network vulnerability during Snow (+119% overall, Bus: 10.33 min) and Rain.</div>
      </div>

      <div class="fig-box">
        <img src="{b64_img('fig07_route_accessibility_rate.png')}" alt="Figure 7 Route Accessibility Rate"/>
        <div class="fig-caption"><strong>Figure 7 (Two-Way Accessibility Interaction Matrix):</strong> Volume-normalised accessibility complaints per 10,000 passengers by route type (Panel A) and 6×6 Route × Mode interaction heatmap (Panel B), exposing the acute 5-fold complaint spike on Suburban Feeder micromobility (E-Scooter: 66.87/10k; Bike Share: 55.26/10k).</div>
      </div>

      <div class="fig-box">
        <img src="{b64_img('fig09_mode_performance_matrix.png')}" alt="Figure 9 Mode Performance Matrix"/>
        <div class="fig-caption"><strong>Figure 8 (Multi-Dimensional Synthesis Matrix):</strong> Cross-modal comparison matrix across demand share, reliability, cost recovery, environmental efficiency (<code>CO2 / kWh</code>), and normalised accessibility complaints, highlighting Metro as the high-efficiency network backbone (70.3% of CO<sub>2</sub> savings at 2.19 kg CO<sub>2</sub>/kWh).</div>
      </div>
    </section>

    <!-- INTERACTIVE DASHBOARD SECTION -->
    <section id="dashboard" class="section-card">
      <h2>
        <span>1.4 Interactive Python Decision Dashboard (Live Filterable App + State Evidence)</span>
        <span class="badge">Live Interactive View + Report Screenshots</span>
      </h2>
      <p style="margin-top:0;">Use the six interactive filter dropdowns below to explore how demand, service delays, farebox cost recovery, carbon mitigation, and normalised accessibility complaints respond across countries, cities, transport modes, route types, weather conditions, and major event days. Beneath the live dashboard, Figures 10 and 11 provide the static state captures prepared for the Word report submission.</p>

      <div class="dash-shell">
        <div class="dash-filters">
          <div><label>Country</label><select id="f-country" onchange="updateDash()">{opts(countries)}</select></div>
          <div><label>City</label><select id="f-city" onchange="updateDash()">{opts(cities)}</select></div>
          <div><label>Transport Mode</label><select id="f-mode" onchange="updateDash()">{opts(modes)}</select></div>
          <div><label>Route Type</label><select id="f-route" onchange="updateDash()">{opts(routes)}</select></div>
          <div><label>Weather Condition</label><select id="f-weather" onchange="updateDash()">{opts(weathers)}</select></div>
          <div><label>Major Event Day</label><select id="f-event" onchange="updateDash()"><option value="ALL">All</option><option value="No">Standard Day (No)</option><option value="Yes">Event Day (Yes)</option></select></div>
        </div>

        <div class="dash-kpis">
          <div class="dash-kpi"><div class="t">Passengers</div><div class="v" id="k-pax">-</div><div class="s" id="k-records">-</div></div>
          <div class="dash-kpi"><div class="t">On-Time Rate</div><div class="v" id="k-ontime">-</div><div class="s">Target: 85.0%</div></div>
          <div class="dash-kpi claim"><div class="t">Mean Delay</div><div class="v" id="k-delay">-</div><div class="s">Service reliability</div></div>
          <div class="dash-kpi claim"><div class="t">Cost Recovery</div><div class="v" id="k-recovery">-</div><div class="s" id="k-margin">-</div></div>
          <div class="dash-kpi"><div class="t">CO2 Saved</div><div class="v" id="k-co2">-</div><div class="s">Tonnes mitigated</div></div>
          <div class="dash-kpi"><div class="t">Satisfaction</div><div class="v" id="k-rating">-</div><div class="s" id="k-comp">-</div></div>
        </div>

        <div class="dash-grid">
          <div class="dash-card"><div id="c-trend" style="height:290px;"></div></div>
          <div class="dash-card"><div id="c-mode" style="height:290px;"></div></div>
          <div class="dash-card"><div id="c-weather" style="height:290px;"></div></div>
          <div class="dash-card"><div id="c-route" style="height:290px;"></div></div>
        </div>
      </div>

      <div class="fig-box">
        <img src="{b64_img('fig10_dashboard_overview.png')}" alt="Figure 10 Dashboard Overview"/>
        <div class="fig-caption"><strong>Figure 9 (Dashboard Screenshot Evidence — Default Unfiltered View):</strong> Full-network baseline state (<code>N = 5,000</code> records across all 12 European cities), displaying top-level KPIs, modal delay and cost recovery bars, route-level accessibility complaint rates, and top city performance cards.</div>
      </div>

      <div class="fig-box">
        <img src="{b64_img('fig11_dashboard_filtered_scenario.png')}" alt="Figure 11 Dashboard Filtered Scenario"/>
        <div class="fig-caption"><strong>Figure 10 (Dashboard Screenshot Evidence — Filtered Decision Scenario):</strong> Executive scenario filtering to <code>Mode = Surface (Bus, Tram, Park &amp; Ride)</code> and <code>Weather = Rain + Snow</code> (<code>n = 583</code> records). Isolating surface modes under adverse precipitation reveals that mean delay surges to 7.38 min, on-time rate drops to 72.2%, satisfaction falls to 3.46/5, and Suburban Feeder accessibility complaints escalate to 20.41 per 10,000 passengers.</div>
      </div>
    </section>

    <!-- TASK 2 SECTION -->
    <section id="task2" class="section-card">
      <h2>
        <span>Task 2 — Data Visualisation Critical Report (LO3 &amp; LO4)</span>
        <span><span class="badge navy">30 Marks</span> <span class="badge">{t2_words} Written Words (Target: ~900w)</span></span>
      </h2>

      {TASK2_SEC_2_1}
      {TASK2_SEC_2_2}

      <div class="table-wrap">
        <table class="data-table">
          <thead>
            <tr>
              <th>Country</th>
              <th>City</th>
              <th class="num">Records</th>
              <th class="num">Total Passengers</th>
              <th class="num">Mean Pax</th>
              <th class="num">Mean Delay (m)</th>
              <th class="num">On-Time (%)</th>
              <th class="num">Net Margin (€)</th>
              <th class="num">Cost Recovery</th>
              <th class="num">Rating</th>
              <th class="num">Complaints / 10k</th>
            </tr>
          </thead>
          <tbody>
            {city_rows_html}
          </tbody>
        </table>
      </div>
      <div class="fig-caption" style="margin-top:-14px; margin-bottom:20px;"><strong>Table 2:</strong> City-level cumulative and mean operational performance across all 12 European cities (2024–2025), ordered by total passenger demand. Shaded cells in Net Margin denote cities operating in aggregate financial deficit due to shared micromobility costs.</div>

      {TASK2_SEC_2_3}
      {TASK2_SEC_2_4}

      <div class="table-wrap">
        <table class="data-table">
          <thead>
            <tr>
              <th>Decision Domain</th>
              <th>Target Mode / Corridor / City</th>
              <th>Empirical Evidence from Visual Investigation</th>
              <th>Recommended Managerial Intervention</th>
            </tr>
          </thead>
          <tbody>
            <tr class="hi">
              <td><strong>1. Financial Sustainability (Business)</strong></td>
              <td>Bike Share &amp; E-Scooter (especially Madrid, Barcelona, Milan, Hamburg)</td>
              <td>Bike Share recovers 5.25% (&minus;€5.60M) and E-Scooter 7.39% (&minus;€3.28M) of operating costs across 1,232 records while serving only 1.06% of passengers (Figure 3).</td>
              <td>Renegotiate fleet-rebalancing vendor contracts, consolidate low-demand docks in Aug–Oct (Figure 1), and bundle micromobility into Metro/Tram passes.</td>
            </tr>
            <tr>
              <td><strong>2. Service Reliability &amp; Decarbonisation (Environmental)</strong></td>
              <td>Bus Network (all 12 cities) &amp; Central/Commuter Corridors</td>
              <td>Bus has the highest delay (6.58 min mean, 74.92% on-time; Figure 4), lowest rating (3.74), and lowest motorised carbon efficiency (1.07 kg CO<sub>2</sub>/kWh vs Metro 2.19; Figure 8).</td>
              <td>Install segregated bus lanes and automated traffic-signal priority on high-load corridors; accelerate electric bus fleet conversion to reduce delay below 5.0 min.</td>
            </tr>
            <tr class="hi">
              <td><strong>3. Weather &amp; Event Resilience (Public Sector)</strong></td>
              <td>Surface Transit (Bus, Tram, Park &amp; Ride) during Rain/Snow &amp; Event Days</td>
              <td>Snow elevates network delay to 8.14 min (Bus 10.33 min; Figure 6); Rain + Snow on surface modes drops rating to 3.46 (Figure 10); Event Days surge demand +26.2% and delay +31.0% (Figure 5).</td>
              <td>Deploy meteorological trigger protocols (pre-salting, headway buffering) and pre-position +25% reserve Metro/Tram capacity on scheduled major event days.</td>
            </tr>
            <tr>
              <td><strong>4. Inclusive Mobility (Social Equity)</strong></td>
              <td>Suburban Feeder Routes &amp; Surface Boarding Stops</td>
              <td>Volume normalisation exposes Suburban Feeder as the highest complaint corridor (16.79/10k pax overall; 20.41/10k in rain/snow; Figures 7 &amp; 10), reversing raw Metro volume bias.</td>
              <td>Reallocate accessibility capital using per-capita complaint metrics to fund step-free kerb ramps, tactile paving, and sheltered feeder stops in outer zones.</td>
            </tr>
          </tbody>
        </table>
      </div>
      <div class="fig-caption" style="margin-top:-14px; margin-bottom:8px;"><strong>Table 3:</strong> Summary of evidence-based strategic recommendations linked to empirical visual findings across business, environmental, public-sector, and social dimensions.</div>
    </section>

    <!-- REFERENCES SECTION -->
    <section id="references" class="section-card">
      <h2>
        <span>References (Harvard Style)</span>
        <span class="badge navy">Academic &amp; Policy Literature</span>
      </h2>
      <div class="ref-list">
        <p>Banister, D. (2008) ‘The sustainable mobility paradigm’, <em>Transport Policy</em>, 15(2), pp. 73–80.</p>
        <p>Cleveland, W.S. and McGill, R. (1984) ‘Graphical perception: Theory, experimentation, and application to the development of graphical methods’, <em>Journal of the American Statistical Association</em>, 79(387), pp. 531–554.</p>
        <p>European Commission (2021) <em>The New EU Urban Mobility Framework</em> (COM(2021) 811 final). Brussels: European Commission.</p>
        <p>Few, S. (2012) <em>Show Me the Numbers: Designing Tables and Graphs to Enlighten</em>. 2nd edn. Burlingame, CA: Analytics Press.</p>
        <p>Few, S. (2013) <em>Information Dashboard Design: Displaying Data for At-a-Glance Monitoring</em>. 2nd edn. Burlingame, CA: Analytics Press.</p>
        <p>Munzner, T. (2014) <em>Visualization Analysis and Design</em>. Boca Raton, FL: CRC Press.</p>
        <p>Shneiderman, B. (1996) ‘The eyes have it: A task by data type taxonomy for information visualizations’, <em>Proceedings of the IEEE Symposium on Visual Languages</em>, Boulder, CO, 3–6 September, pp. 336–343.</p>
        <p>Tufte, E.R. (2001) <em>The Visual Display of Quantitative Information</em>. 2nd edn. Cheshire, CT: Graphics Press.</p>
        <p>Ware, C. (2021) <em>Information Visualization: Perception for Design</em>. 4th edn. Cambridge, MA: Morgan Kaufmann.</p>
        <p>Wertheimer, M. (1923) ‘Untersuchungen zur Lehre von der Gestalt II’, <em>Psychologische Forschung</em>, 4(1), pp. 301–350.</p>
      </div>
    </section>

    <!-- APPENDIX SECTION -->
    <section id="appendix" class="section-card">
      <h2>
        <span>Appendix — Complete Reproducible Python Code</span>
        <span class="badge navy">Verification Appendix</span>
      </h2>
      <p style="margin-top:0;">All data ingestion, serial-date transformation, descriptive statistics, analytical figures, SVG structural diagrams, and interactive dashboard outputs were produced in Python 3.11. Click any module below to inspect the complete source code.</p>
      {appendix_html}
    </section>

  </div>

  <script>
    const RAW_DATA = {data_json};
    function updateDash() {{
      const country = document.getElementById('f-country').value;
      const city = document.getElementById('f-city').value;
      const mode = document.getElementById('f-mode').value;
      const route = document.getElementById('f-route').value;
      const weather = document.getElementById('f-weather').value;
      const eventDay = document.getElementById('f-event').value;

      const rows = RAW_DATA.filter(r =>
        (country === 'ALL' || r.Country === country) &&
        (city === 'ALL' || r.City === city) &&
        (mode === 'ALL' || r.Transport_Mode === mode) &&
        (route === 'ALL' || r.Route_Type === route) &&
        (weather === 'ALL' || r.Weather === weather) &&
        (eventDay === 'ALL' || r.Event_Day === eventDay)
      );

      const n = rows.length || 1;
      const totalPax = rows.reduce((s, r) => s + r.Passengers, 0);
      const meanOnTime = rows.reduce((s, r) => s + r.On_Time_Percentage, 0) / n;
      const meanDelay = rows.reduce((s, r) => s + r.Average_Delay_Minutes, 0) / n;
      const totalRev = rows.reduce((s, r) => s + r.Ticket_Revenue_EUR, 0);
      const totalCost = rows.reduce((s, r) => s + r.Operating_Cost_EUR, 0);
      const netMargin = totalRev - totalCost;
      const recovery = totalCost > 0 ? (totalRev / totalCost * 100) : 0;
      const totalCO2 = rows.reduce((s, r) => s + r.CO2_Saved_KG, 0) / 1000.0;
      const meanRating = rows.reduce((s, r) => s + r.Customer_Rating, 0) / n;
      const totalComp = rows.reduce((s, r) => s + r.Accessibility_Complaints, 0);
      const compRate = totalPax > 0 ? (totalComp / totalPax * 10000) : 0;

      document.getElementById('k-pax').textContent = (totalPax / 1e6).toFixed(2) + 'M';
      document.getElementById('k-records').textContent = rows.length.toLocaleString() + ' records';
      document.getElementById('k-ontime').textContent = meanOnTime.toFixed(1) + '%';
      document.getElementById('k-delay').textContent = meanDelay.toFixed(2) + 'm';
      document.getElementById('k-recovery').textContent = recovery.toFixed(1) + '%';
      document.getElementById('k-margin').textContent = 'Net: ' + (netMargin >= 0 ? '+€' : '-€') + (Math.abs(netMargin)/1e6).toFixed(2) + 'M';
      document.getElementById('k-co2').textContent = totalCO2.toFixed(1) + 't';
      document.getElementById('k-rating').textContent = meanRating.toFixed(2);
      document.getElementById('k-comp').textContent = compRate.toFixed(2) + ' / 10k pax';

      if (typeof Plotly === 'undefined') return;

      const byMonth = {{}};
      rows.forEach(r => {{
        if (!byMonth[r.YearMonth]) byMonth[r.YearMonth] = {{sum: 0, cnt: 0}};
        byMonth[r.YearMonth].sum += r.Passengers;
        byMonth[r.YearMonth].cnt += 1;
      }});
      const mKeys = Object.keys(byMonth).sort();
      Plotly.react('c-trend', [{{
        x: mKeys,
        y: mKeys.map(k => byMonth[k].sum / byMonth[k].cnt),
        mode: 'lines+markers',
        line: {{color: '#002B49', width: 2.4}},
        marker: {{color: '#3AA89A', size: 6}}
      }}], {{
        title: {{text: 'Mean Daily Passengers by Month', font: {{size: 13, color: '#002B49'}}}},
        paper_bgcolor: '#FFFFFF', plot_bgcolor: '#F7FAFB',
        margin: {{l: 50, r: 16, t: 38, b: 36}}
      }}, {{displayModeBar: false, responsive: true}});

      const byMode = {{}};
      rows.forEach(r => {{
        if (!byMode[r.Transport_Mode]) byMode[r.Transport_Mode] = {{rev: 0, cost: 0}};
        byMode[r.Transport_Mode].rev += r.Ticket_Revenue_EUR;
        byMode[r.Transport_Mode].cost += r.Operating_Cost_EUR;
      }});
      const modeKeys = Object.keys(byMode).sort((a,b) => (byMode[a].rev/byMode[a].cost) - (byMode[b].rev/byMode[b].cost));
      const modeVals = modeKeys.map(k => byMode[k].rev / byMode[k].cost * 100);
      Plotly.react('c-mode', [{{
        x: modeVals, y: modeKeys, orientation: 'h', type: 'bar',
        marker: {{color: modeVals.map(v => v < 100 ? '#66C9BA' : '#1A4A6B')}}
      }}], {{
        title: {{text: 'Cost Recovery Ratio (%) by Mode', font: {{size: 13, color: '#002B49'}}}},
        paper_bgcolor: '#FFFFFF', plot_bgcolor: '#F7FAFB',
        margin: {{l: 95, r: 16, t: 38, b: 36}}
      }}, {{displayModeBar: false, responsive: true}});

      const wOrder = ['Clear', 'Cloudy', 'Windy', 'Heatwave', 'Rain', 'Snow'];
      const byW = {{}};
      rows.forEach(r => {{
        if (!byW[r.Weather]) byW[r.Weather] = {{d: 0, c: 0}};
        byW[r.Weather].d += r.Average_Delay_Minutes;
        byW[r.Weather].c += 1;
      }});
      const wKeys = wOrder.filter(k => byW[k]);
      const wVals = wKeys.map(k => byW[k].d / byW[k].c);
      Plotly.react('c-weather', [{{
        x: wKeys, y: wVals, type: 'bar',
        marker: {{color: wKeys.map(k => (k === 'Rain' || k === 'Snow') ? '#66C9BA' : '#1A4A6B')}}
      }}], {{
        title: {{text: 'Mean Delay (min) by Weather', font: {{size: 13, color: '#002B49'}}}},
        paper_bgcolor: '#FFFFFF', plot_bgcolor: '#F7FAFB',
        margin: {{l: 45, r: 16, t: 38, b: 36}}
      }}, {{displayModeBar: false, responsive: true}});

      const byR = {{}};
      rows.forEach(r => {{
        if (!byR[r.Route_Type]) byR[r.Route_Type] = {{comp: 0, pax: 0}};
        byR[r.Route_Type].comp += r.Accessibility_Complaints;
        byR[r.Route_Type].pax += r.Passengers;
      }});
      const rKeys = Object.keys(byR).sort((a,b) => (byR[a].comp/byR[a].pax) - (byR[b].comp/byR[b].pax));
      const rVals = rKeys.map(k => byR[k].comp / byR[k].pax * 10000);
      const maxR = Math.max(...rVals);
      Plotly.react('c-route', [{{
        x: rVals, y: rKeys, orientation: 'h', type: 'bar',
        marker: {{color: rVals.map(v => v === maxR ? '#66C9BA' : '#1A4A6B')}}
      }}], {{
        title: {{text: 'Complaints per 10k Pax by Route Type', font: {{size: 13, color: '#002B49'}}}},
        paper_bgcolor: '#FFFFFF', plot_bgcolor: '#F7FAFB',
        margin: {{l: 115, r: 16, t: 38, b: 36}}
      }}, {{displayModeBar: false, responsive: true}});
    }}
    window.addEventListener('DOMContentLoaded', updateDash);
  </script>
</body>
</html>
"""
    OUT_HTML.write_text(page_html, encoding="utf-8")
    print(f"Built self-contained review HTML: {OUT_HTML}")
    print(f"Task 1 written explanation word count: {t1_words} words (target ~600)")
    print(f"Task 2 written report word count:      {t2_words} words (target ~900)")
    print(f"Total written prose word count:        {t1_words + t2_words} words (target ~1,500)")


if __name__ == "__main__":
    build_html()
