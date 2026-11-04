# Assignment Control — COM7021 Assessment

## 1. Identity

- **Module:** COM7021SCC (Data Visualisation)
- **Assignment:** COM7021 Assessment (Task 1 Investigation + Task 2 Report)
- **Student ID:** 25199053
- **Institution:** Arden University Berlin (MSc Data Science)
- **Tutor:** Ahmed Hassan
- **Weighting:** 100% of final module grade (Task 1: 70 marks | Task 2: 30 marks)
- **Word Limit:** 3,000 words equivalent total:
  - Task 1 Practical Python Work: 1,500 words equivalent (charts, dashboard, data prep, tables, screenshots)
  - Task 1 Written Explanation: ~600 words
  - Task 2 Written Report: ~900 words
- **Submission Format:** Single `.docx` report with Python code in the Appendix and Student ID (`25199053`) clearly stated.

---

## 2. Authoritative Materials

| Source | File Path | Read Fully | Key Authority |
|---|---|---|---|
| Assessment Brief | `COM7021 - Assignment/COM7021-DataVisualization-Assessment-Statement.pdf` | Yes | Official tasks, marks (70/30), LOs 1–4, 6 chart categories + 1 dashboard, word allocation |
| Assignment Guide | `COM7021 - Assignment/COM7021 Assignment Guide.docx` | Yes | Tutor's explicit workflow, Do's/Don'ts, Level 7 critical evaluation expectations |
| Marking Rubric | Provided by student (90–100 down to 0–19 bands) | Yes | Requires data importing, initial statistics, visualisations, dashboard, methodologies, and critical understanding |
| Dataset | `COM7021 - Assignment/[5442] EcoMoveMobility.xlsx` | Yes | 5,000 records × 18 columns across 12 European cities (2024–2025) |
| Visual Design Guide | `COM7021 - Assignment/VISUAL_DESIGN_GUIDE.md` | Yes | Arden palette (`#002B49` midnight, `#66C9BA` tiffany), Aptos typography, matplotlib + SVG recipes |
| Reference Studies | `_studies/design_guide/render_studies.py` | Yes | Proven SVG + `rsvg-convert` builder patterns matching COM7020 |

---

## 3. Learning Outcomes & Rubric Alignment

| Learning Outcome | Assessed In | Requirement & Evidence Strategy |
|---|---|---|
| **LO1:** Critically appraise a variety of data visualisation techniques in terms of psychology, cultural context, effectiveness, and target audience | Task 1 & Task 2 | Justify every chart using perceptual psychology (Cleveland & McGill hierarchy, Gestalt principles, pre-attentive attributes, cognitive load, data-ink ratio) and non-colour-dependent encoding (WCAG contrast / greyscale distinction). |
| **LO2:** Apply appropriate data visualisation techniques to analyse and present data | Task 1 (70 marks) | Complete Python pipeline: data import, serial date parsing, derived metrics, initial descriptive statistics table, ≥6 distinct non-repeating visualisations, and 1 interactive Shiny dashboard. |
| **LO3:** Demonstrate a critical understanding of how data visualisation can support technical and non-technical audiences in making business decisions | Task 2 (30 marks) | Differentiate how operational analysts (technical) vs senior transport executives (non-technical) use the static figures and interactive dashboard filters for route planning, reliability, pricing, and accessibility. |
| **LO4:** Critically evaluate and contextualise understanding of subject area linking to local, national, and global issues using academic/professional resources | Task 2 (30 marks) | Connect findings to European urban mobility policy, decarbonisation ($\text{CO}_2$ vs energy), social equity (accessibility complaints per 10k passengers), and public-sector subsidy trade-offs (micromobility deficit vs mass transit surplus) with Harvard references. |

### Rubric Checklist for Band 80–100 (Outstanding / Exemplary)
1. **Data Importing & Preparation:** Document exact schema (`5,000 × 18`), convert Excel serial integer `Date` (`45292`–`46022`, `origin='1899-12-30'`) to ISO `datetime64`, verify zero missing/duplicate records, and engineer normalised metrics (`Net_Margin_EUR`, `Cost_Recovery_Pct`, `Fare_per_Pax_EUR`, `Cost_per_Pax_EUR`, `Complaints_per_10k_Pax`, `CO2_per_kWh`).
2. **Initial Statistics:** Present a structured summary statistics table (Mean, SD, Median, IQR, Min, Max, Skewness) before plotting, explaining why right-skewed variables (`Passengers`, `Ticket_Revenue_EUR`, `CO2_Saved_KG`) require both parametric and non-parametric (median/IQR) inspection, and reconciling unweighted record-mean cost recovery (`84.12%`) against volume-weighted overall cost recovery (`99.58%`).
3. **Unified Visualisation Suite (Figure 0, Figure A, and Figures 1 to 10):**
   - **Figure 0 (`fig00_executive_kpi_strip.png`):** Executive KPI summary strip across all 5,000 daily records.
   - **Figure A (`fig00_methodology_pipeline.png`):** Five-stage Python data investigation and visualisation pipeline.
   - **Figure 1 (`fig01_monthly_demand_trend.png`):** Monthly mobility demand & weekday/weekend regime decomposition (2024–2025).
   - **Figure 2 (`fig02_city_demand_comparison.png`):** Connected dumbbell plot of raw vs modal-mix-adjusted city margins (resolving Simpson's Paradox).
   - **Figure 3 (`fig03_mode_cost_recovery.png`):** Two-panel per-passenger unit economics and cumulative net margin / carbon abatement return.
   - **Figure 4 (`fig04_delay_distribution_boxplot.png`):** Raincloud distribution (half-violin KDE + Tukey boxplot + jittered observations) of daily service delays across modes.
   - **Figure 5 (`fig05_delay_rating_relationship.png`):** Joint scatter + OLS regression + marginal KDE strips of service delay vs customer satisfaction ($r = -0.821$) and Major Event Day shifts.
   - **Figure 6 (`fig06_weather_mode_delay_heatmap.png`):** Dual-encoded Weather × Mode delay interaction heatmap.
   - **Figure 7 (`fig07_route_accessibility_rate.png`):** Two-way volume-weighted accessibility complaint rate matrix per 10,000 passengers across routes and modes.
   - **Figure 8 (`fig08_mode_performance_matrix.png`):** Multi-dimensional modal performance matrix synthesising demand share, delay, overall cost recovery, carbon efficiency, and complaint rates.
   - **Figure 9 (`fig09_dashboard_overview.png`):** Streamlit interactive dashboard screenshot — default unfiltered network baseline ($N = 5,000$).
   - **Figure 10 (`fig10_dashboard_filtered_scenario.png`):** Streamlit interactive dashboard screenshot — filtered adverse-weather surface transit scenario ($n = 583$).
4. **Interactive Dashboard (`Streamlit + Plotly` Application — `scripts/04_streamlit_dashboard.py` + `scripts/04_dashboard.py`):**
   - Scenario Presets: 6 1-click executive scenario presets (including Figure 9 Baseline and Figure 10 Adverse Weather Surface Scenario) + Custom Exploration mode.
   - Sidebar Filters: Date Range & Day Regime, Country, City, Transport Mode, Route Topology, Weather Condition, Major Event Day, and Financial Basis Toggle.
   - Views: 6 KPI cards with live baseline deltas & dual-basis cost recovery (`99.58%` overall vs `84.12%` record mean) + 5 structured analytical decision tabs + static screenshot evidence (Figures 9 and 10).
5. **Process Evidence & Appendix:**
   - Final `.docx` submission (`COM7021_Assessment_25199053.docx`) and synchronised HTML reports (`COM7021_Draft_Review_25199053.html`, `index.html`).
   - Complete, clean, reproducible Python & Streamlit source code (6 modules) in the Appendix.

---

## 4. Technical & Design Standard

- **Visual Styling:** Locked `arden` palette (`#002B49` midnight, `#66C9BA` tiffany, `#3AA89A` tiffany_deep, `#0E7C8B` teal, `#1A4A6B` midnight_soft, `#E6F5F2` mist, `#F7FAFB` paper).
- **Typography:** Microsoft Aptos (`Regular`, `SemiBold`, `Bold`).
- **Strict Refusals:** No pie/donut/radar charts, no 3D, no dual y-axes, no rainbow hues, no uncaptioned screenshots, no personal reflection boxes or project progress banners.
- **Language:** British English throughout (`visualisation`, `colour`, `normalised`, `standardisation`, `programme`, `analyse`).

---

## 5. Tutor Formative Feedback Resolution Log (Ahmed Hassan)

| Feedback Area | Resolution Implemented |
|---|---|
| **1. Figure Numbering** | Unified sequential numbering (`Figure 0`, `Figure A`, and `Figures 1 to 10`) across all filenames, SVG headers, captions, and in-text references in Task 1 and Task 2. |
| **2. Statistical Interpretation** | Framed all correlations ($r = -0.821$ delay vs rating, $r = -0.968$ delay vs on-time, $r = 0.866$ complaints vs passengers) as observational associations/covariation, explicitly noting unmeasured confounders (vehicle crowding, transfer friction, platform discomfort, fleet age). |
| **3. Financial Analysis** | Reconciled cumulative totals (€111.64M rev, €112.11M cost, −€0.47M net), per-record means (€22,328.12 rev, €22,422.00 cost, −€93.88 net), and per-passenger figures (€2.73 vs €2.74/pax), and explained the difference between unweighted record-mean cost recovery (`84.12%`, median `102.26%`) and volume-weighted overall recovery (`99.58%`). |
| **4. Recommendations** | Framed all four policy interventions (contract rebalancing audits, corridor bus priority appraisal, weather/event timetable buffers, suburban feeder site audits) as evidence-supported options for pilot evaluation and feasibility appraisal rather than established solutions. |
| **5. Presentation** | Removed all 13 personal reflection callout boxes and the "Project Working Topology & Status Overview" banner; integrated key methodological reflections directly into the academic discussion. |
| **6. Word Count & Conciseness** | Eliminated cross-section repetition; Task 1 prose is `618 words` (target ~600w) and Task 2 report is `945 words` (target ~900w), totalling `1,563 words` of written prose. |
