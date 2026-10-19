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
1. **Data Importing & Preparation:** Document exact schema (`5,000 × 18`), convert Excel serial integer `Date` (`45292`–`46022`, `origin='1899-12-30'`) to ISO `datetime64`, verify zero missing/duplicate records, and engineer normalised metrics (`Net_Margin_EUR`, `Cost_Recovery_Pct`, `Complaints_per_10k_Pax`, `Passengers_per_Trip`, `CO2_per_kWh`).
2. **Initial Statistics:** Present a structured summary statistics table (Mean, SD, Median, IQR, Min, Max, Skewness) before plotting, explaining why right-skewed variables (`Passengers`, `Ticket_Revenue_EUR`, `CO2_Saved_KG`) require both parametric and non-parametric (median/IQR) inspection.
3. **Six Distinct Visualisations (No Unnecessary Repetition):**
   - **Fig 1 (Time-Series):** Monthly mobility demand & seasonal trajectory (2024–2025) highlighting spring peaks and autumn troughs (`line` + `band` / `point`).
   - **Fig 2 (Comparison — Cities & Demand/Financials):** City-level ridership and net operating margin comparison across the 12 European cities (`col` / horizontal bar with highlighted claim).
   - **Fig 3 (Comparison / Structural Divide — Transport Modes):** Cost recovery ratio (`%`) and net financial performance across the 6 transport modes, exposing the shared micromobility (`Bike Share` / `E-Scooter`) structural deficit versus rail (`Metro` / `Tram` / `Park and Ride`) surplus.
   - **Fig 4 (Distribution — Reliability & Delays):** Distribution of `Average_Delay_Minutes` across transport modes and weather conditions (`boxplot` / violin or faceted distribution), isolating `Bus` and `Snow`/`Rain` tail risks.
   - **Fig 5 (Relationship — Delay, Satisfaction & Event Shocks):** Multivariate relationship between `Average_Delay_Minutes`, `Customer_Rating` ($r = -0.821$), and `Event_Day` / `Transport_Mode` (`scatter` / joint relationship view).
   - **Fig 6 (Performance Indicator & Sustainability / Accessibility Matrix):** Multi-metric performance table/chart (`Great Tables` `GT_aesth` or faceted dot/bar matrix) comparing `CO2_Saved_KG`, `Energy_Consumption_KWh`, and normalised `Complaints_per_10k_Pax` across modes and route types (`Suburban Feeder` complaint intensity vs `Metro` volume).
4. **Interactive Dashboard (`Shiny for Python` + `aesth`):**
   - Filters: Country/City, Transport Mode, Route Type, Weather Condition, Event Day, Date Range.
   - Views: Executive KPI strip + interactive trend, mode/route reliability & financial comparison, and formatted Great Tables summary.
5. **Process Evidence & Appendix:**
   - Screenshots of data import, initial statistics output, individual figures, and interactive dashboard states (default + filtered decision scenario).
   - Complete, clean, reproducible Python code in the Appendix.

---

## 4. Technical & Design Standard

- **Visual Package:** `aesth` (`plotnine` + `Great Tables` + `Shiny for Python`) using the locked `arden` palette (`#002B49` midnight, `#66C9BA` tiffany, `#3AA89A` tiffany_deep, `#0E7C8B` teal, `#1A4A6B` midnight_soft, `#E6F5F2` mist, `#F7FAFB` paper).
- **Typography:** Microsoft Aptos (`Regular`, `SemiBold`, `Bold`).
- **Strict Refusals:** No pie/donut/radar charts, no 3D, no dual y-axes, no rainbow hues, no uncaptioned screenshots.
- **Language:** British English throughout (`visualisation`, `colour`, `organise`, `centre`, `programme`, `analyse`).
