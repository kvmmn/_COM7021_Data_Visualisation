# COM7021 Data Visualisation — Final Assessment Submission (Student ID: 25199053)

**Title:** Sustainable Urban Mobility Performance Across European Cities: A Python Data Visualisation Investigation and Critical Report  
**Programme:** MSc Data Science (Arden University)  
**Tutor:** Ahmed Hassan  

## Contents
- `COM7021_Assessment_25199053.docx` — Complete assessment report (Cover Sheet, Task 1, Task 2, References, and Appendix source code).
- `[5442] EcoMoveMobility.xlsx` — Raw dataset (5,000 daily logs, 12 European cities, 2024–2025).
- `style/palette.py` — Shared Arden Midnight & Tiffany colour palette and Matplotlib styling helpers.
- `scripts/01_data_prep_and_eda.py` — Data ingestion, serial-date conversion, feature engineering, and summary CSV tables (`output/tables/`).
- `scripts/02_charts.py` — Generates Figures 1 to 7 (`output/figures/`).
- `scripts/03_diagrams.py` — Generates Figure 0, Figure A, and Figure 8 (`output/figures/`).
- `scripts/04_streamlit_dashboard.py` — Interactive Streamlit & Plotly decision dashboard (Figures 9 & 10).
- `data/ecomove_cleaned.csv` — Cleaned dataset produced by `01_data_prep_and_eda.py`.
- `output/tables/` — Six analytical CSV summary tables (`table01`–`table06`).
- `output/figures/` — All 12 final high-resolution figures (`fig00`–`fig10`).

## Reproducibility & Live Links
- **Live Dashboard:** https://com7021-data-visualisation.streamlit.app/
- **GitHub Repository:** https://github.com/kvmmn/_COM7021_Data_Visualisation
- **Run Locally:**
  ```bash
  pip install -r requirements.txt
  python scripts/01_data_prep_and_eda.py
  python scripts/02_charts.py
  python scripts/03_diagrams.py
  streamlit run scripts/04_streamlit_dashboard.py
  ```
