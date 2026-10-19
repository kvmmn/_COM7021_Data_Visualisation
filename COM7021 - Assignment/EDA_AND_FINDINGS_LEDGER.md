# EDA and Findings Ledger — `[5442] EcoMoveMobility.xlsx`

This ledger records every empirical check, data preparation rule, descriptive statistic, and analytical finding from the `[5442] EcoMoveMobility.xlsx` dataset. All figures, dashboard views, and written claims in Task 1 and Task 2 draw directly from these verified numbers.

---

## 1. Dataset Schema & Data Hygiene Audit

- **Source File:** `COM7021 - Assignment/[5442] EcoMoveMobility.xlsx` (Sheet: `Dataset`)
- **Dimensions:** `5,000` rows × `18` valid columns (note: `openpyxl` raw sheet scan shows 8 trailing empty `None` columns beyond column 18 which `pandas` drops automatically; documented as part of import hygiene).
- **Primary Key:** `Record_ID` (`EM-00001` to `EM-05000`), `5,000` unique values (`0` duplicates).
- **Missing Values:** `0` missing/null values across all 18 columns.
- **Negative Value Check:** `0` negative values across all raw numeric measures (`Passengers`, `Trips`, `Average_Delay_Minutes`, `On_Time_Percentage`, `Ticket_Revenue_EUR`, `Operating_Cost_EUR`, `CO2_Saved_KG`, `Energy_Consumption_KWh`, `Customer_Rating`, `Accessibility_Complaints`).
- **Date Encoding Issue (Critical Data Prep Finding):**
  - Raw `Date` column is stored as Excel serial integers (`int64`, min `45292`, max `46022`) rather than ISO dates.
  - Converted via `pd.to_datetime(df["Date"], unit="D", origin="1899-12-30")`.
  - Verified date range: **`2024-01-01` to `2025-12-31`** (exactly 2 full calendar years; `2,567` records in 2024 and `2,433` records in 2025).
- **Granularity (Unit of Observation):**
  - Each row (`Record_ID`) represents a single daily operational record for a specific `City`, `Transport_Mode`, and `Route_Type` under observed `Weather` and `Event_Day` conditions.
- **Engineered / Derived Variables Created for Analysis:**
  1. `Date_dt` (`datetime64[ns]`), `Year`, `YearMonth`, `Month_Num`, `DayOfWeek`, `Is_Weekend` (`bool`).
  2. `Net_Margin_EUR` = `Ticket_Revenue_EUR - Operating_Cost_EUR` (daily operating surplus/deficit in EUR).
  3. `Cost_Recovery_Pct` = `(Ticket_Revenue_EUR / Operating_Cost_EUR) * 100` (farebox recovery ratio in %).
  4. `Complaints_per_10k_Pax` = `(Accessibility_Complaints / Passengers) * 10,000` (volume-normalised accessibility complaint intensity).
  5. `Passengers_per_Trip` = `Passengers / Trips` (vehicle/service occupancy load).
  6. `CO2_per_kWh` = `CO2_Saved_KG / Energy_Consumption_KWh` (environmental efficiency for motorised modes).

---

## 2. Categorical Variable Frequencies

| Variable | Unique Levels | Distribution (Counts & Share of 5,000 Records) |
|---|---:|---|
| `Country` | 6 | Germany (`1,260`, 25.2%), Netherlands (`880`, 17.6%), Italy (`820`, 16.4%), France (`810`, 16.2%), Spain (`796`, 15.9%), Austria (`434`, 8.7%) |
| `City` | 12 | Amsterdam (`478`), Vienna (`434`), Munich (`428`), Hamburg (`424`), Paris (`422`), Rome (`420`), Barcelona (`408`), Berlin (`408`), Rotterdam (`402`), Milan (`400`), Lyon (`388`), Madrid (`388`) |
| `Transport_Mode` | 6 | Bus (`1,375`, 27.5%), Metro (`1,047`, 20.9%), Tram (`761`, 15.2%), Bike Share (`759`, 15.2%), Park and Ride (`585`, 11.7%), E-Scooter (`473`, 9.5%) |
| `Route_Type` | 6 | Tourist Zone (`904`, 18.1%), Commuter Corridor (`831`, 16.6%), Central Route (`820`, 16.4%), Airport Connector (`818`, 16.4%), Suburban Feeder (`817`, 16.3%), University Area (`810`, 16.2%) |
| `Weather` | 6 | Clear (`2,071`, 41.4%), Cloudy (`1,293`, 25.9%), Rain (`905`, 18.1%), Windy (`306`, 6.1%), Heatwave (`243`, 4.9%), Snow (`182`, 3.6%) |
| `Event_Day` | 2 | No (`4,490`, 89.8%), Yes (`510`, 10.2%) |

---

## 3. Initial Descriptive Statistics (All 5,000 Records)

| Variable | Mean | SD | Median | Q25 | Q75 | IQR | Min | Max | Skewness |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `Passengers` | 8,181.94 | 10,018.72 | 4,398.00 | 1,411.75 | 10,077.50 | 8,665.75 | 64.00 | 66,416.00 | +1.90 |
| `Trips` | 121.77 | 155.79 | 52.00 | 36.00 | 106.00 | 70.00 | 11.00 | 1,048.00 | +2.13 |
| `Average_Delay_Minutes` | 4.35 | 2.39 | 4.40 | 2.60 | 6.00 | 3.40 | 0.00 | 12.50 | +0.16 |
| `On_Time_Percentage` | 82.06 | 7.93 | 82.00 | 76.50 | 87.90 | 11.40 | 55.00 | 99.00 | -0.15 |
| `Ticket_Revenue_EUR` | 22,328.12 | 28,822.41 | 11,190.02 | 3,280.33 | 26,329.65 | 23,049.32 | 90.93 | 204,386.05 | +1.95 |
| `Operating_Cost_EUR` | 22,422.00 | 26,114.32 | 11,638.28 | 7,189.86 | 22,732.98 | 15,543.11 | 978.37 | 178,936.39 | +2.15 |
| `Net_Margin_EUR` (derived) | -93.88 | 6,022.60 | +306.74 | -2,721.77 | +2,674.23 | 5,396.00 | -30,923.78 | +31,285.36 | -0.06 |
| `Cost_Recovery_Pct` (derived) | 84.12% | 45.82% | 102.26% | 80.44% | 115.00% | 34.57% | 2.96% | 158.80% | -0.93 |
| `CO2_Saved_KG` | 896.39 | 1,261.16 | 338.30 | 126.85 | 1,009.48 | 882.62 | 8.30 | 8,884.10 | +2.09 |
| `Energy_Consumption_KWh` | 466.81 | 564.22 | 269.70 | 85.20 | 599.62 | 514.42 | 0.00 | 3,856.30 | +1.85 |
| `Customer_Rating` | 4.01 | 0.40 | 4.00 | 3.70 | 4.30 | 0.60 | 2.70 | 4.90 | -0.24 |
| `Accessibility_Complaints` | 12.53 | 16.97 | 7.00 | 2.00 | 15.00 | 13.00 | 0.00 | 147.00 | +2.59 |
| `Complaints_per_10k_Pax` (derived) | 16.96 | 14.15 | 16.29 | 8.79 | 22.59 | 13.80 | 0.00 | 389.61 | +5.64 |

**Methodological Note on Distributions:**
Volume-linked variables (`Passengers`, `Trips`, `Ticket_Revenue_EUR`, `Operating_Cost_EUR`, `CO2_Saved_KG`, `Energy_Consumption_KWh`, `Accessibility_Complaints`) exhibit strong positive skewness ($\text{Skew} \in [1.85, 2.59]$) because the dataset pools high-capacity rail (`Metro`, mean `24,601` pax) with individual micromobility (`Bike Share`, mean `354` pax; `E-Scooter`, mean `347` pax). Consequently, reporting global means alone is misleading; stratified analysis by `Transport_Mode` and non-parametric summaries (median/IQR) are essential.

---

## 4. Eight Core Empirical Findings (The Data Narrative)

### Finding 1: Structural Hierarchy of Transport Modes (Volume vs Micromobility)
- **Mass Transit Dominance:** Across all 5,000 records (`40,909,721` total passengers), **Metro** accounts for **62.96% of total ridership** (`25,757,522` passengers; mean `24,601.26` pax/record, `528.72` pax/trip), followed by **Tram** (`15.60%`, `6,380,878` pax; mean `8,384.86`), **Bus** (`12.40%`, `5,073,394` pax; mean `3,689.74`), and **Park and Ride** (`7.98%`, `3,265,220` pax; mean `5,581.57`).
- **Micromobility Niche:** **Bike Share** (`0.66%` of passengers, `268,765` total; mean `354.10` pax/record) and **E-Scooter** (`0.40%` of passengers, `163,942` total; mean `346.60` pax/record) together represent **24.64% of operational records** (`1,232` rows) but only **1.06% of total passengers** (`1.00` passenger per trip).

| Transport Mode | Records | Total Passengers | Share of Pax (%) | Mean Pax | Mean Delay (min) | On-Time (%) | Total Rev (€M) | Total Cost (€M) | Net Margin (€M) | Cost Recovery (%) | Total $\text{CO}_2$ (t) | Mean Rating | Raw Complaints (mean) | Complaints / 10k Pax |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **Metro** | 1,047 | 25,757,522 | 62.96% | 24,601.3 | 3.73 | 84.09% | 73.33 | 69.03 | **+4.30** | **106.24%** | 3,150.92 | 4.09 | 36.52 | **14.87** |
| **Tram** | 761 | 6,380,878 | 15.60% | 8,384.9 | 4.79 | 80.63% | 15.67 | 13.36 | **+2.31** | **117.30%** | 646.92 | 3.94 | 12.64 | 15.19 |
| **Bus** | 1,375 | 5,073,394 | 12.40% | 3,689.7 | **6.58** | **74.92%** | 12.00 | 11.99 | **+0.01** | **100.08%** | 414.16 | **3.74** | 6.44 | 18.16 |
| **Park and Ride** | 585 | 3,265,220 | 7.98% | 5,581.6 | 5.17 | 79.46% | 10.07 | 8.28 | **+1.78** | **121.53%** | 199.19 | 3.90 | 8.86 | 16.18 |
| **Bike Share** | 759 | 268,765 | 0.66% | 354.1 | **1.62** | **90.85%** | 0.31 | 5.91 | **-5.60** | **5.25%** | 49.13 | **4.35** | 0.60 | 17.58 |
| **E-Scooter** | 473 | 163,942 | 0.40% | 346.6 | 1.94 | 89.71% | 0.26 | 3.54 | **-3.28** | **7.39%** | 21.65 | 4.29 | 0.64 | **20.88** |

---

### Finding 2: Financial Performance — The Micromobility Subsidy Trap
- Across the entire authority, total revenue is **`€111.64M`** against total operating cost of **`€112.11M`**, yielding a slight aggregate deficit of **`-€0.47M`** (`-€93.88` mean per record).
- However, disaggregating by `Transport_Mode` reveals a stark structural split:
  - **Profitable Fixed/Mass Modes (+€8.40M combined surplus):** `Metro` generates **`+€4.30M`** net surplus (`106.24%` aggregate cost recovery), `Tram` generates **`+€2.31M`** (`117.30%` recovery), `Park and Ride` generates **`+€1.78M`** (`121.53%` recovery), and `Bus` breaks even at **`+€0.01M`** (`100.08%` recovery).
  - **Loss-Making Shared Micromobility (-€8.88M combined deficit):** `Bike Share` earns only `€408.90` mean daily revenue against `€7,789.57` operating cost (**`5.25%` aggregate cost recovery**, losing **`-€5.60M`** overall). `E-Scooter` earns `€552.39` mean daily revenue against `€7,477.72` operating cost (**`7.39%` cost recovery**, losing **`-€3.28M`** overall).
- **Decision Insight:** Fixed-route transit cross-subsidises shared micromobility. City-level deficits (e.g., Madrid `-€272.5k`, Barcelona `-€152.7k`, Milan `-€145.9k`, Hamburg `-€137.6k`) are driven by high micromobility operating costs relative to low per-trip fare revenue (`~€1.15` per Bike Share trip and `~€1.59` per E-Scooter trip).

---

### Finding 3: City-Level Demand Hierarchy & Financial Dispersion
- **Top-Tier Demand Cities:** **Paris** (`4,492,481` total pax; mean `10,645.69`/record) and **Berlin** (`4,487,351` total pax; mean `10,998.41`/record) lead total network demand, carrying **21.95%** of all passengers across the 12 cities. Their high averages hold across every mode (e.g., Paris Metro averages `31,620.8` pax/day and Berlin Metro `30,747.2` pax/day vs Rotterdam Metro `20,288.4` and Lyon Metro `19,547.0`).
- **Mid-Tier Cities:** **Munich** (`3.60M` pax), **Barcelona** (`3.53M`), **Rome** (`3.42M`), **Vienna** (`3.39M`), **Amsterdam** (`3.36M`), **Madrid** (`3.29M`), **Milan** (`3.10M`), and **Hamburg** (`3.00M`).
- **Lower-Volume Cities:** **Rotterdam** (`2.70M` pax; mean `6,710.73`) and **Lyon** (`2.54M` pax; mean `6,537.44`).
- **City Financial Leaders vs Laggards:**
  - **Surplus Cities:** **Munich** (`+€171.24k`, `101.76%` cost recovery), **Vienna** (`+€90.10k`, `100.98%`), **Lyon** (`+€85.20k`, `101.25%`), **Berlin** (`+€14.54k`, `100.12%`), **Rotterdam** (`+€8.34k`, `100.11%`).
  - **Deficit Cities:** **Madrid** (`-€272.49k`, `97.03%` recovery), **Barcelona** (`-€152.69k`, `98.44%`), **Milan** (`-€145.86k`, `98.30%`), **Hamburg** (`-€137.63k`, `98.33%`), **Rome** (`-€94.46k`, `98.99%`), **Amsterdam** (`-€29.66k`, `99.68%`), **Paris** (`-€6.03k`, `99.95%`).

---

### Finding 4: Service Reliability & Customer Satisfaction Bottleneck (`Bus` & Delay Link)
- **Strong Linear Coupling:** Across all 5,000 observations, `Average_Delay_Minutes` is strongly negatively correlated with `On_Time_Percentage` (**$r = -0.968$**) and `Customer_Rating` (**$r = -0.821$**).
- **Bus as the Primary Reliability Bottleneck:**
  - **Bus** is the weakest-performing mode operationally: highest mean delay (**`6.58` min**, median `6.50` min, IQR `2.0` min), lowest on-time percentage (**`74.92%`**), and lowest customer satisfaction (**`3.74` / 5.0**).
  - **Park and Ride** (`5.17` min delay, `79.46%` on-time, `3.90` rating) and **Tram** (`4.79` min delay, `80.63%` on-time, `3.94` rating) form a middle tier due to mixed surface-traffic exposure.
  - Grade-separated **Metro** achieves `3.73` min mean delay, `84.09%` on-time, and `4.09` customer rating despite carrying 6.7× the passenger load of Bus.
  - **Bike Share** (`1.62` min delay, `90.85%` on-time, `4.35` rating) and **E-Scooter** (`1.94` min delay, `89.71%` on-time, `4.29` rating) have the lowest delays and highest ratings because dock/vehicle availability is uncoupled from road congestion.

---

### Finding 5: Weather Shocks & Major Event Day Pressures
- **Adverse Weather Escalation:**
  - **Clear** (`3.71` min delay, `84.17%` on-time, `4.15` rating) and **Cloudy** (`3.89` min delay, `83.46%` on-time, `4.12` rating) represent baseline operations (`67.3%` of days).
  - **Windy** (`4.86` min delay, `80.42%` on-time, `4.02` rating) and **Heatwave** (`4.91` min delay, `80.19%` on-time, `3.76` rating; demand drops `-25.3%` vs Clear to `6,583.6` pax) cause moderate degradation.
  - **Rain** (`5.40` min delay, `78.70%` on-time, `3.70` rating) increases delays by **`+45.6%`** over Clear weather.
  - **Snow** (`182` records) triggers severe network disruption: mean delay more than doubles to **`8.14` min** (`+119.4%` vs Clear), on-time performance drops to **`69.97%`**, and customer rating falls to **`3.36`**. During **Snow**, **Bus** delays average **`10.33` min**, **Park and Ride** **`9.40` min**, **Tram** **`8.99` min**, and even **Metro** rises to **`7.45` min**.
- **Major Event Days (`Event_Day = Yes`, `510` records / 10.2%):**
  - Mean passenger demand surges by **`+26.2%`** (`10,057.93` vs `7,968.86` on non-event days) and ticket revenue rises `+25.3%` (`€27,268.11` vs `€21,767.01`).
  - However, mean delay increases by **`+31.0%`** (`5.53` min vs `4.22` min), on-time percentage drops **`-4.28` percentage points** (`78.21%` vs `82.49%`), and customer satisfaction drops from `4.02` to `3.87`.

---

### Finding 6: Temporal & Seasonal Dynamics (2024–2025)
- **Spring Peak vs Late-Summer/Autumn Trough:**
  - Across both 2024 and 2025, passenger demand peaks in **Q1–Spring (January–April)**, averaging **`8,805` to `9,354` passengers/record** (highest single month: **April 2025** at `10,285.47` mean pax and **March 2024** at `9,412.22` mean pax / `2.08M` total pax).
  - Demand declines through late summer and early autumn (**August–October**), reaching its lowest level in **October** (`6,805.48` mean pax; `6,647.95` in Oct 2024 and `6,979.39` in Oct 2025 — a **`-27.2%` seasonal drop** from April), before recovering in **November–December** (`7,558.91` and `7,922.45` mean pax).
- **Weekday vs Weekend Regime:**
  - Weekdays (`3,614` records) average **`8,802.88` passengers/record** versus **`6,562.86` passengers/record** on weekends (`1,386` records) — a **`+34.1%` weekday demand premium**, while delay (`4.33` vs `4.41` min) and rating (`4.01` vs `3.99`) remain stable.

---

### Finding 7: Accessibility Complaints — Raw Volume Illusion vs Normalised Intensity
- **Raw Volume Illusion:** `Accessibility_Complaints` correlates strongly with `Passengers` (**$r = 0.866$**). Consequently, **Metro** (`36.52` complaints/record; `38,240` total) and high-volume routes (`Central Route` `14.14`/record; `Commuter Corridor` `14.06`/record) appear worst when looking at unadjusted counts.
- **Volume-Normalised Reality (`Complaints_per_10k_Pax`):**
  - By mode, **Metro** actually has the **lowest** complaint rate per 10,000 passengers (**`14.87`**), followed by **Tram** (`15.19`) and **Park and Ride** (`16.18`), whereas **Bus** (`18.16` mean / `17.46` aggregate per 10k pax) and **E-Scooter** (`20.88` mean per 10k pax) experience substantially higher per-passenger accessibility friction.
  - By route type, **`Suburban Feeder`** has the lowest raw complaints (`10.36`/record) due to smaller passenger loads (`6,167.34` mean pax), but exhibits the **highest normalised complaint rate across the entire network at `16.79` complaints per 10,000 passengers** (compared with `14.70` on `Central Route` and `14.90` on `Commuter Corridor`). This points to first/last-mile infrastructure gaps (kerb ramps, step-free feeder stops) outside city centres.

---

### Finding 8: Environmental Impact & Energy Efficiency
- **Total $\text{CO}_2$ Mitigation:** EcoMove operations saved **`4,481.97` tonnes** (`4,481,974.3 kg`) of $\text{CO}_2$ over 2024–2025 while consuming **`2,334.03` MWh** (`2,334,033.3 kWh`) of energy.
- **Modal Contributions & Efficiency:**
  - **Metro** delivers **70.30%** of total $\text{CO}_2$ savings (`3,150.92` tonnes; `3,009.47 kg`/record) at high energy efficiency (**`2.19 kg` $\text{CO}_2$ saved per kWh** consumed, or `0.056 kWh` per passenger).
  - **Tram** contributes **14.43%** of $\text{CO}_2$ savings (`646.92` tonnes) at **`1.66 kg` $\text{CO}_2$/kWh**.
  - **Bus** contributes **9.24%** of $\text{CO}_2$ savings (`414.16` tonnes) but has the **lowest motorised environmental efficiency at `1.07 kg` $\text{CO}_2$ saved per kWh** (`0.076 kWh` per passenger — **36.5% more energy per passenger than Metro**).
  - **Park and Ride** delivers **`1.72 kg` $\text{CO}_2$/kWh** (`199.19` tonnes total).
  - **Bike Share** consumes **`0.00 kWh`** (`49.13` tonnes $\text{CO}_2$ saved) and **E-Scooter** averages just `6.35 kWh`/record (`7.21 kg` $\text{CO}_2$/kWh, `21.65` tonnes total), confirming zero/near-zero tailpipe energy use but modest total $\text{CO}_2$ volume due to low ridership share (`1.06%`).

---

## 5. First-Principles Structural Decomposition (Advanced Data Science Layer)

Moving beyond surface aggregations, a first-principles decomposition of the data-generating process ($\text{Cost} = \alpha + \beta \cdot \text{Passengers}$, direct modal standardization across cities, marginal carbon abatement economics, and two-way $\text{Route} \times \text{Mode}$ interaction matrices) uncovers four critical structural insights:

### Discovery A: Inverted Unit Economics & Negative Contribution Margin in Micromobility
- Standard financial summaries show that `Bike Share` (`5.25%` cost recovery) and `E-Scooter` (`7.39%` cost recovery) lose `-€8.88M` combined. A naive manager might prescribe "marketing to increase ridership so fixed costs are spread over more trips."
- **First-Principles OLS Cost Decomposition ($\text{Cost} = \alpha + \beta \cdot \text{Passengers}$) refutes this:**
  - **`Bike Share`:** Mean fare = **`€1.15/pax`**, OLS Variable Cost = **`€22.15/pax`** (Fixed intercept = `-€52.95`, $R^2 = 0.61$). **Marginal contribution = `-€21.00` per additional trip** (ratio of aggregates: `-€20.84/pax`).
  - **`E-Scooter`:** Mean fare = **`€1.59/pax`**, OLS Variable Cost = **`€21.37/pax`** (Fixed intercept = `+€71.96`, $R^2 = 0.58$). **Marginal contribution = `-€19.79` per additional trip** (ratio of aggregates: `-€19.98/pax`).
  - Because variable logistics costs (manual van collection, battery swapping, dock rebalancing, and vandalism repair) scale linearly at `~€21–€22` per trip against a `€1.15–€1.59` fare, **every additional micromobility trip deepens the deficit by ~€20**. Consequently, high-demand cities (`Paris` `479` trips/day, `Berlin` `449` trips/day) lose *more* money per micromobility day (`-€9,357` and `-€9,297` on Bike Share) than smaller cities (`Rotterdam` `-€5,263`/day).
  - By contrast, fixed-route mass transit exhibits positive marginal contribution: **`Park and Ride` (`+€0.55/pax`)**, **`Tram` (`+€0.36/pax`)**, **`Metro` (`+€0.17/pax`, $R^2 = 0.96$)**, while **`Bus` (`€0.00/pax`, $R^2 = 0.95$)** operates at exact break-even (`€2.37` fare vs `€2.36` cost).

### Discovery B: Simpson’s Paradox & Modal Composition Confounding Across Cities
- In raw city totals, **Madrid** (`-€272.49k`, `-€702.29`/record) and **Barcelona** (`-€152.69k`, `-€374.25`/record) look like severe financial underperformers, whereas **Berlin** (`+€14.54k`, `+€35.65`/record) appears profitable.
- **Root Cause (Confounding by Unbalanced Modal Sampling):** Across the 12 cities, the share of micromobility records (`Bike Share + E-Scooter`) ranges from `22.18%` (`Amsterdam`) and `22.30%` (`Berlin`) to **`28.61%` (`Madrid`)** and **`27.45%` (`Barcelona`)**, while rail records (`Metro + Tram`) range from **`41.18%` in `Berlin`** down to **`32.47%` in `Madrid`**. Across all 12 cities, $\text{Corr}(\text{Micromobility Share \%}, \text{City Net Margin}) = \mathbf{-0.795}$!
- **Direct Standardisation (Mix-Adjusted City Performance):** When every city’s mode-specific performance is weighted by the exact network-average modal proportions (`Bus 27.5%`, `Metro 20.94%`, `Tram 15.22%`, `Bike Share 15.18%`, `P&R 11.70%`, `E-Scooter 9.46%`):
  - **Berlin plunges 7 places from `#4` (`+€35.65`/record raw) to `#11` (`-€353.87`/record mix-adjusted)** because its huge per-day micromobility losses were masked by an over-representation of profitable Metro rows (`93` rows, `22.79%`)!
  - **Madrid’s** apparent deficit shrinks by **62%** (`-€702.29` raw $\rightarrow$ `-€268.04` mix-adjusted), and **Madrid’s mix-adjusted passenger demand jumps from `#4` (`8,479` raw) to `#3` in Europe (`9,275` pax/record)** behind only `Paris` (`10,786`) and `Berlin` (`10,258`)!
  - **Milan** rises from `#10` (`-€364.64`) to **`#6` (`-€76.39`)**, **Barcelona** rises from `#11` (`-€374.25`) to **`#7` (`-€120.46`)**, and **Rotterdam** climbs from `#5` (`+€20.74`) to **`#3` (`+€90.43`)** behind **Munich** (`#1`, `+€215.27`) and **Lyon** (`#2`, `+€120.99`).

### Discovery C: Public-Finance Efficiency of Decarbonisation (Net Return per Tonne of $\text{CO}_2$ Saved)
- Evaluating climate strategy through **Marginal Carbon Abatement Cost/Return** ($\text{Net Margin EUR} / \text{Tonnes CO}_2 \text{ Saved}$):
  - **`Park and Ride`:** Saves `199.19 t` $\text{CO}_2$ while generating **`+€8,953` net surplus per tonne of $\text{CO}_2$ abated**.
  - **`Tram`:** Saves `646.92 t` $\text{CO}_2$ (`14.43%`) while generating **`+€3,571` net surplus per tonne of $\text{CO}_2$**.
  - **`Metro`:** Saves `3,150.92 t` $\text{CO}_2$ (`70.30%` of network total) while generating **`+€1,366` net surplus per tonne of $\text{CO}_2$**.
  - **`Bus`:** Saves `414.16 t` $\text{CO}_2$ (`9.24%`) at **`+€23` net surplus per tonne of $\text{CO}_2$**.
  - **`Bike Share` & `E-Scooter`:** Save just `49.13 t` and `21.65 t` $\text{CO}_2$ (`1.58%` combined) at a staggering net public subsidy cost of **`€114,016` per tonne of $\text{CO}_2$** (`Bike Share`) and **`€151,293` per tonne of $\text{CO}_2$** (`E-Scooter`)! Relative to the EU ETS carbon price (`~€65–€90/t`), un-reformed micromobility contracts are **>1,500× costlier per tonne of $\text{CO}_2$ abated** than electrified rail.

### Discovery D: The `Suburban Feeder × Micromobility` Accessibility Anomaly
- Disaggregating `Complaints_per_10k_Pax` across the full $6 \times 6$ `Route_Type × Transport_Mode` matrix reveals that high accessibility complaint intensity is **not** uniform across routes or modes, but concentrated in one acute structural interaction cell:
  - Across 5 of the 6 route types (`Airport Connector`, `Central Route`, `Commuter Corridor`, `Tourist Zone`, `University Area`), `Bike Share` and `E-Scooter` average just **`9.06` to `12.94` complaints per 10,000 passengers** (lower than Metro's `14.27–15.50`).
  - **Strictly on `Suburban Feeder` routes**, however, mean complaint intensity surges **5×** to **`66.87 per 10,000 passengers` for `E-Scooter`** (`54.02` ratio of sums) and **`55.26 per 10,000 passengers` for `Bike Share`** (`49.26` ratio of sums), while **`Bus` rises to `22.34` (`21.20` ratio of sums)** and **`Park and Ride` to `19.59` (`18.61` ratio of sums)**!
  - **Physical Mechanism:** Suburban feeder zones lack dedicated micromobility parking corrals and drop-kerb bus boarding islands; dockless scooters and bikes left on narrow suburban footways create severe pavement obstruction complaints (`~0.6` complaints/day against smaller suburban ridership denominators of `~110–130` trips/day).

