#!/usr/bin/env python3
"""Step 5: Build a single, self-contained HTML assessment report and synchronized root index.html.
Incorporates all formative feedback from Tutor Ahmed Hassan:
1. Unified sequential Figure numbering (Figures 1 to 10) across filenames, captions, and in-text references.
2. Rigorous non-causal statistical language (observational associations, covariance, and unmeasured confounders).
3. Explicit financial reconciliation across per-record, per-passenger, and cumulative totals, plus unweighted average (84.12%) vs volume-weighted aggregate (99.58%) cost recovery.
4. Evidence-proportionate recommendations framed as targeted options for pilot evaluation and feasibility appraisal.
5. Removal of repeated personal reflection boxes and project progress banners; insights integrated into academic prose.
6. Strict word count compliance (~600 words Task 1 prose; ~900 words Task 2 report) and reduced repetition across tasks.
"""

from __future__ import annotations

import base64
import html
import json
import re
import shutil
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_CSV = BASE_DIR / "data" / "ecomove_cleaned.csv"
TABLES_DIR = BASE_DIR / "output" / "tables"
FIG_DIR = BASE_DIR / "output" / "figures"
OUT_HTML = BASE_DIR / "COM7021_Draft_Review_25199053.html"
ROOT_INDEX = BASE_DIR.parent / "index.html"


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
<p>The investigation examines <code>[5442] EcoMoveMobility.xlsx</code> (5,000 daily records, 18 columns) across 12 European cities (6 countries) for 2024–2025 (Figure A). All <code>Record_ID</code> keys are unique with zero missing or negative values. Excel serial dates (<code>45292</code>–<code>46022</code>) were converted to ISO dates (<code>origin='1899-12-30'</code>), and six normalised features were derived: <code>Net_Margin_EUR</code>, <code>Cost_Recovery_Pct</code>, <code>Fare_per_Pax_EUR</code>, <code>Cost_per_Pax_EUR</code>, <code>Complaints_per_10k_Pax</code>, and <code>CO2_per_kWh</code>.</p>
"""

TASK1_SEC_1_2 = """
<p>Initial statistics (Table 1) show positive skewness in volume-linked variables—<code>Passengers</code> (mean 8,181.94, SD 10,018.72, median 4,398.00, IQR 8,665.75, skewness +1.90), <code>Ticket_Revenue_EUR</code> (mean €22,328.12, median €11,190.02, skewness +1.95), and <code>CO2_Saved_KG</code> (mean 896.39 kg, median 338.30 kg, skewness +2.09)—because high-capacity <code>Metro</code> (mean 24,601.26 pax; 62.96% of ridership) is pooled with single-rider <code>Bike Share</code> (354.10) and <code>E-Scooter</code> (346.60). Medians and IQRs are thus reported alongside means. Cumulative revenue (€111.64M; €2.73/pax) and cost (€112.11M; €2.74/pax) yield 99.58% overall recovery (net &minus;€0.47M; &minus;€93.88/record), whereas daily record recovery averages 84.12% (median 102.26%) because low-recovery micromobility comprises 24.64% of records but 1.06% of passengers.</p>
"""

TASK1_FIG1_TEXT = """
<p><strong>1. Seasonal &amp; Weekday Regime (Figure 1):</strong> A dual-series line chart tracks monthly mean demand across 2024–2025, separating weekday and weekend regimes (+34.1% weekday premium: 8,802.88 vs 6,562.86 pax/record). Spring peaks (March 2024: 9,412.22; April 2025: 10,285.47) contrast with a &minus;27.2% October trough (6,805.48), identifying October for low-disruption maintenance.</p>
"""

TASK1_FIG2_TEXT = """
<p><strong>2. Simpson’s Paradox in City Margins (Figure 2):</strong> A connected dumbbell plot compares raw per-record city margins against modal-mix-adjusted margins via direct standardisation. Because micromobility record shares vary across cities (22.18% Amsterdam to 28.61% Madrid) and correlate negatively with raw margins (<em>r</em> = &minus;0.795), unadjusted rankings are confounded: standardising modal weights shifts Berlin from Rank #4 (+€35.65/record raw; +€14.54k total) to Rank #11 (&minus;€353.87/record adjusted) and cuts Madrid’s deficit by 62% (&minus;€702.29 to &minus;€268.04/record).</p>
"""

TASK1_FIG3_TEXT = """
<p><strong>3. Unit Economics &amp; Carbon Abatement (Figure 3):</strong> A two-panel bar chart pairs per-passenger unit economics (Panel A) with cumulative net margins and carbon returns (Panel B). Park &amp; Ride (€3.08 fare vs €2.54 cost; +€0.55/pax), Tram (€2.46 vs €2.09; +€0.36/pax), and Metro (€2.85 vs €2.68; +€0.17/pax) earn positive margins, while Bus breaks even (€2.37 vs €2.36). Bike Share (€1.15 vs €22.00; &minus;€20.84/pax, 5.25% recovery) and E-Scooter (€1.59 vs €21.57; &minus;€19.98/pax, 7.39% recovery) incur steep losses. Metro abates 3,150.92 tCO<sub>2</sub> (+€4.30M surplus; +€1,366/tCO<sub>2</sub>), whereas micromobility requires €114k–€151k/tCO<sub>2</sub> in subsidy.</p>
"""

TASK1_FIG4_TEXT = """
<p><strong>4. Service Delay Distribution (Figure 4):</strong> A raincloud plot combining half-violin KDEs, Tukey boxplots, and jittered points exposes tail risks hidden by means. Bus shows the widest delay spread (median 6.50 min, IQR 2.00 min, mean 6.58 min, max 12.50 min; 74.92% on-time), above Park &amp; Ride (median 5.00 min) and Tram (4.70 min), whereas Metro remains compact (median 3.60 min, mean 3.73 min; 84.09% on-time).</p>
"""

TASK1_FIG5_TEXT = """
<p><strong>5. Delay, Satisfaction &amp; Event-Day Associations (Figure 5):</strong> A joint scatter plot with OLS regression and marginal KDEs examines the association between delay and rating (<em>r</em> = &minus;0.821, slope &minus;0.14 pts/min; <em>N</em> = 5,000). Because correlation cannot establish causation, lower ratings may also reflect co-occurring crowding or transfer friction. Major Event Days (<em>n</em> = 510) coincide with +26.2% higher ridership, +31.0% higher delay (5.53 vs 4.22 min), and lower ratings (3.87 vs 4.02).</p>
"""

TASK1_FIG6_8_TEXT = """
<p><strong>6. Weather Shocks, Accessibility &amp; Synthesis (Figures 6–8):</strong> Figure 6 shows Snow coincides with +119.4% higher delay vs Clear weather (8.14 vs 3.71 min; Bus 10.33 min). Figure 7 corrects exposure bias in accessibility complaints: raw counts track ridership (<em>r</em> = 0.866), making Metro appear highest (36.52/record), but rates per 10,000 passengers (Panel A) show Metro is lowest (14.85/10k) and Suburban Feeders highest (16.79/10k), led by Suburban Feeder E-Scooter (54.02/10k aggregate; 66.87/10k record mean) and Bike Share (49.26/10k aggregate; 55.26/10k record mean; Panel B). Figure 8 synthesises modal KPIs; Figures 9–10 present the Streamlit dashboard.</p>
"""


# ==============================================================================
# TASK 2 PROSE (~900 WORDS TARGET)
# ==============================================================================
TASK2_SEC_2_1 = """
<h3>2.1 Critical Justification of Visualisation Design for Technical and Non-Technical Audiences (LO1 &amp; LO3)</h3>
<p>Communicating transport performance across EcoMove requires serving two cognitive profiles: technical analysts—who inspect distributional skew, covariance, and denominator-adjusted rates—and non-technical executives, who require rapid anomaly detection and policy trade-offs (Munzner, 2014; Few, 2013). Rejecting low-precision encodings such as pie charts, 3D graphics, radar plots, or dual y-axes, the visual suite operationalises Cleveland and McGill’s (1984) perceptual hierarchy. Spatial position along a common scale governs all primary comparisons: the city dumbbell plot (Figure 2), unit-economics bars (Figure 3), and route accessibility chart (Figure 7) align metrics on shared Cartesian axes to minimise decoding error.</p>
<p>To limit cognitive load across multidimensional data, the graphics apply Tufte’s (2001) data-ink maximisation and Ware’s (2021) pre-attentive processing principles. A restrained semantic palette—Arden Midnight (<code>#002B49</code>) for structural context paired with Tiffany accents (<code>#66C9BA</code> / <code>#3AA89A</code>) reserved for focal anomalies—creates pre-attentive pop-out while preserving WCAG 4.5:1 contrast. For non-technical audiences, selective hue contrast and direct callouts in Figures 2, 3, and 8 highlight municipal rank reversals and modal deficits without legend scanning. Simultaneously, technical analysts are served by multi-layered encodings: the raincloud plot (Figure 4; Allen <em>et al.</em>, 2019) integrates kernel density estimation, Tukey quartiles, and observation jitter, while the joint plot (Figure 5) pairs bivariate regression with marginal density strips. Gestalt principles of proximity, similarity, and common region (Wertheimer, 1923; Few, 2012) group shaded regimes and dashboard panels into coherent zones.</p>
"""

TASK2_SEC_2_2 = """
<h3>2.2 Critical Synthesis of Findings and Methodological Reflections (LO2 &amp; LO3)</h3>
<p>Synthesising the evidence without repeating raw descriptions highlights four methodological conclusions:</p>
<ol>
  <li><strong>Reconciling Per-Record, Per-Passenger, and Overall Financial Metrics:</strong> Aggregation basis alters financial interpretation. Whereas the unweighted mean of daily record cost-recovery ratios is 84.12% because low-recovery micromobility represents 24.64% of records (1,232 rows), volume-weighted overall recovery (<code>Sum Revenue / Sum Cost</code>) reaches 99.58% (€111.64M vs €112.11M; &minus;€0.47M total or &minus;€93.88/record). Fixed-route modes—Metro (+€4.30M, +€0.17/pax, 106.24% overall vs 107.00% record mean), Tram (+€2.31M, +€0.36/pax, 117.30% vs 117.99%), and Park &amp; Ride (+€1.78M, +€0.55/pax, 121.53% vs 122.21%)—cross-subsidise Bike Share (&minus;€5.60M, &minus;€20.84/pax, 5.25% overall vs 5.99% record mean) and E-Scooter (&minus;€3.28M, &minus;€19.98/pax, 7.39% vs 8.63%), where servicing costs (~€21.57–€22.00/pax) exceed fares (€1.15–€1.59/pax; Figure 3).</li>
  <li><strong>Controlling for Compositional Confounding Across Cities:</strong> Unadjusted city totals (Table 2) exhibit Simpson’s Paradox (Simpson, 1951) because modal record shares vary across cities and correlate negatively with raw margins (<em>r</em> = &minus;0.795). Direct standardisation (Figure 2) shows Berlin’s raw surplus (+€14.54k total; +€35.65/record) masks per-day micromobility losses (&minus;€353.87/record adjusted, Rank #11), whereas Madrid’s deficit (&minus;€272.49k total; &minus;€702.29/record) narrows by 62% (&minus;€268.04/record adjusted) under equal modal weights.</li>
  <li><strong>Distinguishing Correlation from Causation in Operational Quality:</strong> Although surface delays (Figure 4), adverse weather (Figure 6), and event surges (Figure 5) co-vary with lower on-time rates (<em>r</em> = &minus;0.968) and lower ratings (<em>r</em> = &minus;0.821), observational data cannot prove single-variable causation. Unmeasured confounders—such as vehicle crowding during event surges, platform discomfort during snow, or fleet age—likely co-occur with delays to reduce satisfaction.</li>
  <li><strong>Correcting Exposure Bias in Accessibility Evaluation:</strong> Raw accessibility complaints scale with ridership (<em>r</em> = 0.866), making high-capacity Metro appear worst in raw terms. Volume-weighted normalisation per 10,000 passengers (Figure 7) removes this exposure bias, showing Metro achieves the lowest complaint rate (14.85/10k) while Suburban Feeders exhibit the highest intensity (16.79/10k), concentrated in peripheral E-Scooter (54.02/10k) and Bike Share (49.26/10k) operations.</li>
</ol>
"""

TASK2_SEC_2_3 = """
<h3>2.3 Critical Evaluation of Dashboard Effectiveness and Analytical Limitations (LO1 &amp; LO3)</h3>
<p>The interactive Streamlit decision dashboard (Section 1.4; Figures 9 and 10) implements Shneiderman’s (1996) visual information-seeking mantra (<em>overview first, zoom and filter, then details-on-demand</em>) by linking six sidebar filters to six KPI cards and coordinated Plotly tabs. Its core strength is scenario isolation: whereas the unfiltered view (Figure 9, <em>N</em> = 5,000) shows near-balanced recovery (99.6%) and 4.35-minute mean delay, filtering to surface transit under Rain and Snow (Figure 10, <em>n</em> = 583) isolates elevated delays (7.38 min), lower on-time rates (72.2%), and lower ratings (3.46/5) alongside positive surface recovery (113.2%). Three limitations apply: (i) static Word screenshots forfeit live tooltips; (ii) daily aggregation masks intra-day peak congestion (07:00–09:00, 16:30–19:00); and (iii) operating costs exclude capital depreciation.</p>
"""

TASK2_SEC_2_4 = """
<h3>2.4 Evidence-Supported Recommendations and Decision-Making Value (LO4)</h3>
<p>Within European sustainable mobility governance (European Commission, 2021; Banister, 2008), visual evidence supports policy appraisal across commercial, environmental, and social domains. Because findings derive from observational records rather than controlled trials, four targeted interventions are proposed for pilot evaluation and feasibility appraisal rather than presented as established solutions (Table 3):</p>
<ol>
  <li><strong>Audit Micromobility Contracts and Seasonal Scaling (Commercial):</strong> Given negative unit margins (&minus;€19.98 to &minus;€20.84/trip; Figure 3) and compositional city deficits (Figure 2), authorities in Madrid, Barcelona, Milan, and Berlin should audit vendor rebalancing fees, evaluate seasonal scaling during the August–October trough (Figure 1), and pilot fare bundling before expanding fleets.</li>
  <li><strong>Appraise Bus Priority on High-Delay Corridors (Operational &amp; Environmental):</strong> Because Bus shows the widest delay spread (6.58 min mean; Figure 4) and lowest motorised carbon efficiency (1.07 vs Metro’s 2.19 kg CO<sub>2</sub>/kWh; Figure 8), planners should appraise signal priority or bus lanes where delays exceed 6.0 minutes (Figure 5), alongside phased electric bus renewal.</li>
  <li><strong>Pilot Weather and Event-Day Timetable Buffers (Resilience):</strong> Based on elevated delays during Snow (8.14 min) and Rain (5.40 min; Figures 6, 10) and on Major Event Days (+31.0% delay, +26.2% ridership; Figure 5), operators should trial weather-triggered headway buffers and evaluate reserve rail/tram deployment during scheduled events.</li>
  <li><strong>Conduct Site Audits on Suburban Feeder Corridors (Social Equity):</strong> Guided by normalised complaint rates (Figure 7) rather than raw counts, municipalities should conduct site audits along Suburban Feeder corridors to test whether docking corrals and step-free kerb upgrades reduce micromobility complaint rates (49.3–54.0/10k pax).</li>
</ol>
"""

# Arden University Harvard (AU Harvard) Reference List
HARVARD_REFERENCES = [
    "Allen, M., Poggiali, D., Whitaker, K., Marshall, T.R. and Kievit, R.A. (2019) ‘Raincloud plots: a multi-platform tool for robust data visualization’, <em>Wellcome Open Research</em>, 4, p. 63. Available at: https://doi.org/10.12688/wellcomeopenres.15191.1 (Accessed: 15 October 2026).",
    "Banister, D. (2008) ‘The sustainable mobility paradigm’, <em>Transport Policy</em>, 15(2), pp. 73–80. Available at: https://doi.org/10.1016/j.tranpol.2007.10.005 (Accessed: 15 October 2026).",
    "Cleveland, W.S. and McGill, R. (1984) ‘Graphical perception: theory, experimentation, and application to the development of graphical methods’, <em>Journal of the American Statistical Association</em>, 79(387), pp. 531–554. Available at: https://doi.org/10.1080/01621459.1984.10478080 (Accessed: 15 October 2026).",
    "European Commission (2021) <em>The New EU Urban Mobility Framework</em> (COM(2021) 811 final). Brussels: European Commission. Available at: https://transport.ec.europa.eu/transport-themes/urban-transport/new-eu-urban-mobility-framework_en (Accessed: 15 October 2026).",
    "Few, S. (2012) <em>Show Me the Numbers: Designing Tables and Graphs to Enlighten</em>. 2nd edn. Burlingame, CA: Analytics Press.",
    "Few, S. (2013) <em>Information Dashboard Design: Displaying Data for At-a-Glance Monitoring</em>. 2nd edn. Burlingame, CA: Analytics Press.",
    "Munzner, T. (2014) <em>Visualization Analysis and Design</em>. Boca Raton, FL: CRC Press.",
    "Shneiderman, B. (1996) ‘The eyes have it: a task by data type taxonomy for information visualizations’, <em>Proceedings of the IEEE Symposium on Visual Languages</em>. Boulder, CO, 3–6 September. Piscataway, NJ: IEEE, pp. 336–343. Available at: https://doi.org/10.1109/VL.1996.545307 (Accessed: 15 October 2026).",
    "Simpson, E.H. (1951) ‘The interpretation of interaction in contingency tables’, <em>Journal of the Royal Statistical Society: Series B (Methodological)</em>, 13(2), pp. 238–241. Available at: https://doi.org/10.1111/j.2517-6161.1951.tb00088.x (Accessed: 15 October 2026).",
    "Tufte, E.R. (2001) <em>The Visual Display of Quantitative Information</em>. 2nd edn. Cheshire, CT: Graphics Press.",
    "Ware, C. (2021) <em>Information Visualization: Perception for Design</em>. 4th edn. Cambridge, MA: Morgan Kaufmann.",
    "Wertheimer, M. (1923) ‘Untersuchungen zur Lehre von der Gestalt II’, <em>Psychologische Forschung</em>, 4(1), pp. 301–350. Available at: https://doi.org/10.1007/BF00410640 (Accessed: 15 October 2026).",
]


def build_html() -> None:
    df = pd.read_csv(DATA_CSV, parse_dates=["Date_ISO"])
    stats_df = pd.read_csv(TABLES_DIR / "table01_initial_statistics.csv")
    city_df = pd.read_csv(TABLES_DIR / "table03_city_summary.csv")

    t1_words = (
        count_words(TASK1_SEC_1_1)
        + count_words(TASK1_SEC_1_2)
        + count_words(TASK1_FIG1_TEXT)
        + count_words(TASK1_FIG2_TEXT)
        + count_words(TASK1_FIG3_TEXT)
        + count_words(TASK1_FIG4_TEXT)
        + count_words(TASK1_FIG5_TEXT)
        + count_words(TASK1_FIG6_8_TEXT)
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

    # Format City Table HTML (including both Total and Per-Record Mean Margin & Overall vs Mean Recovery)
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
          <td class="num {margin_cls}">€{r['Mean_Margin_EUR']:,.2f}</td>
          <td class="num">{r['Cost_Recovery_Pct']:.2f}% <span style="color:var(--mute);font-size:11px;">({r['Mean_Record_Cost_Recovery_Pct']:.1f}%)</span></td>
          <td class="num">{r['Mean_Rating']:.2f}</td>
          <td class="num">{r['Complaints_per_10k_Pax']:.2f}</td>
        </tr>"""

    # Read Python source files for Appendix
    code_files = [
        ("style/palette.py", BASE_DIR / "style" / "palette.py"),
        ("scripts/01_data_prep_and_eda.py", BASE_DIR / "scripts" / "01_data_prep_and_eda.py"),
        ("scripts/02_charts.py", BASE_DIR / "scripts" / "02_charts.py"),
        ("scripts/03_diagrams.py", BASE_DIR / "scripts" / "03_diagrams.py"),
        ("scripts/04_streamlit_dashboard.py", BASE_DIR / "scripts" / "04_streamlit_dashboard.py"),
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
  <title>COM7021 Assessment — Final Submission Report (Student ID: 25199053)</title>
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
      margin-left: 14px;
      padding: 4px 10px;
      border-radius: 999px;
      transition: background 0.15s;
    }}
    .top-nav .links a:hover {{
      background: var(--midnight-soft);
      color: var(--white);
    }}
    .site-footer {{
      margin-top: 48px;
      padding-top: 20px;
      border-top: 1px solid var(--line);
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 11px;
      color: var(--mute);
    }}
    .site-footer a {{
      color: var(--mute);
      text-decoration: underline;
    }}
    .site-footer a:hover {{
      color: var(--midnight);
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
    @media (max-width: 820px) {{
      .dash-kpis {{ grid-template-columns: repeat(2, 1fr); }}
      .dash-grid {{ grid-template-columns: 1fr; }}
    }}
  </style>
</head>
<body>

  <nav class="top-nav">
    <div class="brand">COM7021SCC Data Visualisation <span>· Assessment Submission Report (Student ID: 25199053)</span></div>
    <div class="links">
      <a href="#overview">Overview</a>
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
      <div class="sub">COM7021 Assessment Submission · Dataset: <code>[5442] EcoMoveMobility.xlsx</code> (EcoMove City Transport Authority, 2024–2025)</div>
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
        <div class="fig-caption"><strong>Figure 0 (Executive Summary Strip):</strong> Baseline 2024–2025 operational metrics across 5,000 daily records in 12 European cities. Tiffany-bordered tiles highlight surface delay bottlenecks (mean 4.35 min; Bus 6.58 min) and aggregate vs modal cost-recovery divergence (99.6% overall network recovery; Bike Share 5.2%).</div>
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
        <img src="{b64_img('fig00_methodology_pipeline.png')}" alt="Methodology Pipeline"/>
        <div class="fig-caption"><strong>Figure A (Investigation Workflow):</strong> Five-stage Python analytical pipeline from raw Excel ingestion and serial-date conversion (<code>origin='1899-12-30'</code>) to normalised feature engineering, static 220 DPI chart generation, and interactive multi-filter dashboard deployment.</div>
      </div>

      <h3>1.2 Initial Descriptive Statistics and Financial Aggregation Basis</h3>
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
      <div class="fig-caption" style="margin-top:-14px; margin-bottom:12px;"><strong>Table 1:</strong> Initial parametric and non-parametric descriptive statistics for raw and derived numerical variables across all <code>N = 5,000</code> daily records (generated via <code>scripts/01_data_prep_and_eda.py</code>). Note that <code>Cost_Recovery_Pct</code> mean (84.12%) reflects the unweighted average of daily record ratios, whereas volume-weighted overall cost recovery (<code>Sum Revenue / Sum Cost</code>) is 99.58%.</div>

      <h3>1.3 Visualisation Investigation and Decision Justification (Figures 1 to 8)</h3>

      {TASK1_FIG1_TEXT}
      <div class="fig-box">
        <img src="{b64_img('fig01_monthly_demand_trend.png')}" alt="Figure 1 Monthly Demand Trend"/>
        <div class="fig-caption"><strong>Figure 1 (Time-Series &amp; Regime Decomposition):</strong> Monthly mean daily passenger demand across 2024–2025, decomposing the +34.1% weekday commute premium (shaded ribbon) and contrasting recurring March–April spring peaks with the &minus;27.2% October trough.</div>
      </div>

      {TASK1_FIG2_TEXT}
      <div class="fig-box">
        <img src="{b64_img('fig02_city_demand_comparison.png')}" alt="Figure 2 City Demand Comparison"/>
        <div class="fig-caption"><strong>Figure 2 (Connected Dumbbell Plot — Simpson's Paradox):</strong> Unadjusted raw mean net margin per record versus modal-mix-adjusted net margin per record across the 12 European cities. Direct standardisation controls for modal sampling share (<em>r</em> = &minus;0.795), shifting Berlin from Rank #4 (+€35.65/record) to Rank #11 (&minus;€353.87/record) while Madrid improves from &minus;€702.29 to &minus;€268.04/record.</div>
      </div>

      {TASK1_FIG3_TEXT}
      <div class="fig-box">
        <img src="{b64_img('fig03_mode_cost_recovery.png')}" alt="Figure 3 Mode Cost Recovery"/>
        <div class="fig-caption"><strong>Figure 3 (Two-Panel Unit Economics &amp; Carbon Abatement Return):</strong> Panel A compares aggregate per-passenger ticket fare against operating cost across modes, illustrating negative per-trip unit margins in Bike Share (&minus;€20.84/trip; 5.25% overall recovery) and E-Scooter (&minus;€19.98/trip; 7.39% recovery). Panel B reports cumulative 2-year net margins (€M) and net public-finance return per tonne of CO<sub>2</sub> saved.</div>
      </div>

      {TASK1_FIG4_TEXT}
      <div class="fig-box">
        <img src="{b64_img('fig04_delay_distribution_boxplot.png')}" alt="Figure 4 Delay Distribution Boxplot"/>
        <div class="fig-caption"><strong>Figure 4 (Distribution Visualisation — Raincloud Plot):</strong> Raincloud distribution combining half-violin Gaussian KDE densities, Tukey boxplots (median and IQR), and jittered daily observations across modes. Bus exhibits the highest delay distribution (median 6.50 min, mean 6.58 min, max 12.50 min).</div>
      </div>

      {TASK1_FIG5_TEXT}
      <div class="fig-box">
        <img src="{b64_img('fig05_delay_rating_relationship.png')}" alt="Figure 5 Delay vs Customer Rating"/>
        <div class="fig-caption"><strong>Figure 5 (Joint Bivariate Relationship &amp; Marginal Density Projections):</strong> Observational association between average service delay and customer satisfaction rating (<em>r</em> = &minus;0.821, OLS slope &minus;0.14 pts/min; <em>N</em> = 5,000), with top and right marginal KDE strips comparing Standard Days (<em>n</em> = 4,490) against Major Event Days (<em>n</em> = 510).</div>
      </div>

      {TASK1_FIG6_8_TEXT}
      <div class="fig-box">
        <img src="{b64_img('fig06_weather_mode_delay_heatmap.png')}" alt="Figure 6 Weather x Mode Delay Heatmap"/>
        <div class="fig-caption"><strong>Figure 6 (Dual-Encoded Weather × Mode Interaction Heatmap):</strong> Mean service delay (minutes) and percentage escalation relative to Clear weather across transport modes and weather conditions.</div>
      </div>

      <div class="fig-box">
        <img src="{b64_img('fig07_route_accessibility_rate.png')}" alt="Figure 7 Route Accessibility Rate"/>
        <div class="fig-caption"><strong>Figure 7 (Two-Way Accessibility Complaint Rate Matrix):</strong> Volume-weighted aggregate accessibility complaints per 10,000 passengers by route type (Panel A) and across the 6×6 Route × Mode interaction matrix (Panel B), isolating elevated complaint intensity on Suburban Feeder micromobility services (E-Scooter: 54.02/10k aggregate; Bike Share: 49.26/10k aggregate).</div>
      </div>

      <div class="fig-box">
        <img src="{b64_img('fig08_mode_performance_matrix.png')}" alt="Figure 8 Mode Performance Matrix"/>
        <div class="fig-caption"><strong>Figure 8 (Multi-Dimensional Modal Performance Matrix):</strong> Cross-modal summary comparing passenger demand share, mean service delay, overall cost-recovery ratio, environmental efficiency (<code>CO2 / kWh</code>), and aggregate accessibility complaints per 10,000 passengers.</div>
      </div>
    </section>

    <!-- INTERACTIVE DASHBOARD SECTION -->
    <section id="dashboard" class="section-card">
      <h2>
        <span>1.4 Interactive Streamlit &amp; Plotly Decision Dashboard (Live App + Figures 9 &amp; 10)</span>
        <span class="badge">Streamlit App + Live Web View + Report Screenshots</span>
      </h2>
      <p style="margin-top:0;">The interactive decision dashboard is implemented in <strong>Streamlit + Plotly</strong> (<code>scripts/04_streamlit_dashboard.py</code>, launched via <code>streamlit run "COM7021 - Assignment/scripts/04_streamlit_dashboard.py"</code>) and mirrored below as a live browser widget. It links executive scenario presets and six sidebar filters (Country, City, Transport Mode, Route Type, Weather Condition, and Major Event Day) to six KPI cards (reporting both volume-weighted overall and unweighted record-mean cost recovery) and five analytical tabs. Beneath the live widget, <strong>Figure 9</strong> (unfiltered network baseline) and <strong>Figure 10</strong> (filtered adverse-weather surface transit scenario) provide the static Streamlit screenshot evidence embedded in the Word submission.</p>

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
          <div class="dash-kpi claim"><div class="t">Overall Recovery</div><div class="v" id="k-recovery">-</div><div class="s" id="k-margin">-</div></div>
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
        <img src="{b64_img('fig09_dashboard_overview.png')}" alt="Figure 9 Dashboard Overview"/>
        <div class="fig-caption"><strong>Figure 9 (Dashboard Screenshot Evidence — Default Unfiltered View):</strong> Full-network baseline state (<code>N = 5,000</code> records across all 12 European cities), displaying top-level KPIs (40.91M passengers, 82.1% on-time, 4.35 min delay, 99.6% overall cost recovery), modal delay and recovery bars, route-level accessibility complaint rates, and top city summary cards.</div>
      </div>

      <div class="fig-box">
        <img src="{b64_img('fig10_dashboard_filtered_scenario.png')}" alt="Figure 10 Dashboard Filtered Scenario"/>
        <div class="fig-caption"><strong>Figure 10 (Dashboard Screenshot Evidence — Filtered Decision Scenario):</strong> Executive scenario filtering to <code>Mode = Surface (Bus, Tram, Park &amp; Ride)</code> and <code>Weather = Rain + Snow</code> (<code>n = 583</code> records). Isolating surface modes under precipitation shows mean delay rising to 7.38 min, on-time rate dropping to 72.2%, customer rating falling to 3.46/5, overall surface cost recovery at 113.2% (+€0.84M net), and Suburban Feeder accessibility complaints reaching 20.41 per 10,000 passengers.</div>
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
              <th class="num">Total Net Margin (€)</th>
              <th class="num">Mean Margin / Rec (€)</th>
              <th class="num">Overall (Mean) Recovery</th>
              <th class="num">Rating</th>
              <th class="num">Complaints / 10k</th>
            </tr>
          </thead>
          <tbody>
            {city_rows_html}
          </tbody>
        </table>
      </div>
      <div class="fig-caption" style="margin-top:-14px; margin-bottom:12px;"><strong>Table 2:</strong> Reconciled city-level cumulative and per-record operational performance across all 12 European cities (2024–2025), ordered by total passenger demand. Both cumulative <code>Total Net Margin (€)</code> and <code>Mean Margin / Rec (€)</code> (used in Figure 2) are reported alongside volume-weighted <code>Overall Recovery</code> (<code>Sum Rev / Sum Cost</code>) and unweighted per-record mean recovery in parentheses.</div>

      {TASK2_SEC_2_3}

      {TASK2_SEC_2_4}

      <div class="table-wrap">
        <table class="data-table">
          <thead>
            <tr>
              <th>Decision Domain</th>
              <th>Target Scope</th>
              <th>Supporting Empirical Evidence</th>
              <th>Proposed Option for Pilot Evaluation &amp; Appraisal</th>
            </tr>
          </thead>
          <tbody>
            <tr class="hi">
              <td><strong>1. Commercial Viability (Business)</strong></td>
              <td>Shared Bike Share &amp; E-Scooter (focused on Madrid, Barcelona, Milan, Berlin)</td>
              <td>Bike Share recovers 5.25% overall (5.99% record mean; &minus;€5.60M total, &minus;€20.84/trip) and E-Scooter 7.39% overall (8.63% record mean; &minus;€3.28M total, &minus;€19.98/trip) across 1,232 records (1.06% of pax; Figures 2 &amp; 3).</td>
              <td>Audit vendor rebalancing fee structures, evaluate seasonal fleet scaling during the Aug–Oct demand trough (Figure 1), and pilot integrated multimodal pass bundling prior to any fleet expansion.</td>
            </tr>
            <tr>
              <td><strong>2. Service Reliability &amp; Efficiency (Environmental)</strong></td>
              <td>Bus Network &amp; High-Delay Surface Corridors (12 cities)</td>
              <td>Bus exhibits the highest delay distribution (6.58 min mean, 6.50 min median, 74.92% on-time; Figure 4), lowest rating (3.74/5), and lowest motorised carbon efficiency (1.07 kg CO<sub>2</sub>/kWh vs Metro 2.19; Figure 8).</td>
              <td>Conduct corridor feasibility studies for traffic-signal priority or segregated bus lanes on routes exceeding 6.0 min delay (Figure 5), alongside capital appraisal for phased electric bus renewal.</td>
            </tr>
            <tr class="hi">
              <td><strong>3. Weather &amp; Event Resilience (Public Sector)</strong></td>
              <td>Surface Modes (Bus, Tram, Park &amp; Ride) during Rain/Snow &amp; Major Event Days</td>
              <td>Snow is associated with an 8.14 min mean delay (Bus 10.33 min; Figure 6); Rain + Snow on surface modes coincides with 7.38 min delay and 3.46 rating (Figure 10); Event Days show +26.2% ridership and +31.0% delay (Figure 5).</td>
              <td>Pilot weather-triggered timetable headway buffers during precipitation warnings and evaluate deploying reserve rail/tram sets on scheduled major event days to test delay mitigation.</td>
            </tr>
            <tr>
              <td><strong>4. Inclusive Mobility (Social Equity)</strong></td>
              <td>Suburban Feeder Routes &amp; Peripheral Micromobility Zones</td>
              <td>Volume-normalised complaint rates identify Suburban Feeders as the highest-friction route (16.79/10k pax overall; 54.02/10k on E-Scooter and 49.26/10k on Bike Share aggregate; Figures 7 &amp; 10), reversing raw Metro volume bias.</td>
              <td>Use per-10k-passenger complaint metrics to prioritise physical site audits on Suburban Feeders, testing designated micromobility parking corrals and step-free kerb upgrades in high-complaint zones.</td>
            </tr>
          </tbody>
        </table>
      </div>
      <div class="fig-caption" style="margin-top:-14px; margin-bottom:12px;"><strong>Table 3:</strong> Summary of evidence-informed managerial options linked to empirical visual findings across business, environmental, public-sector, and social dimensions.</div>
    </section>

    <!-- REFERENCES SECTION -->
    <section id="references" class="section-card">
      <h2>
        <span>References (Arden University Harvard Format)</span>
        <span class="badge navy">Academic &amp; Policy Literature</span>
      </h2>
      <div class="ref-list">
        {"".join(f"<p>{r}</p>" for r in HARVARD_REFERENCES)}
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

    <footer class="site-footer">
      <span>COM7021SCC · Student ID: 25199053 · MSc Data Science · Arden University Berlin</span>
      <span>Language: <strong>English</strong> · <a href="index_fa.html">فارسی</a></span>
    </footer>

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
        title: {{text: 'Overall Cost Recovery (%) by Mode', font: {{size: 13, color: '#002B49'}}}},
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
    window.addEventListener('DOMContentLoaded', () => {{
      updateDash();
      const params = new URLSearchParams(window.location.search);
      if (params.get('lang') === 'fa') {{
        window.location.href = 'index_fa.html';
      }}
    }});
  </script>
</body>
</html>
"""
    OUT_HTML.write_text(page_html, encoding="utf-8")
    shutil.copyfile(OUT_HTML, ROOT_INDEX)
    print(f"Built self-contained review HTML: {OUT_HTML} and {ROOT_INDEX}")
    print(f"Task 1 written explanation word count: {t1_words} words (target ~600)")
    print(f"Task 2 written report word count:      {t2_words} words (target ~900)")
    print(f"Total written prose word count:        {t1_words + t2_words} words (target ~1,500)")


if __name__ == "__main__":
    build_html()
