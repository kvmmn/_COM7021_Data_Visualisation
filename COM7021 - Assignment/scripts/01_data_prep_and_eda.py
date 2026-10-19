#!/usr/bin/env python3
"""Step 1: Data Importing, Cleaning, Feature Engineering, and Initial Statistics.
Dataset: [5442] EcoMoveMobility.xlsx
Module: COM7021 Data Visualisation — Arden University (Student ID: 25199053)
"""

from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_XLSX = BASE_DIR / "[5442] EcoMoveMobility.xlsx"
DATA_DIR = BASE_DIR / "data"
TABLES_DIR = BASE_DIR / "output" / "tables"


def load_and_clean_data(xlsx_path: Path = RAW_XLSX) -> pd.DataFrame:
    """Import raw Excel sheet, validate schema, parse Excel serial dates, and engineer metrics."""
    df = pd.read_excel(xlsx_path, sheet_name="Dataset")
    # Drop any completely empty trailing columns if present
    df = df.dropna(axis=1, how="all").copy()

    # 1. Convert Excel serial integer Date (origin 1899-12-30) to ISO datetime
    df["Date_ISO"] = pd.to_datetime(df["Date"], unit="D", origin="1899-12-30")
    df["Year"] = df["Date_ISO"].dt.year
    df["Month"] = df["Date_ISO"].dt.month
    df["Month_Name"] = df["Date_ISO"].dt.strftime("%b")
    df["YearMonth"] = df["Date_ISO"].dt.to_period("M").astype(str)
    df["Day_Name"] = df["Date_ISO"].dt.day_name()
    df["Is_Weekend"] = np.where(df["Date_ISO"].dt.dayofweek >= 5, "Weekend", "Weekday")

    # 2. Engineer operational, financial, social, and environmental ratios
    df["Net_Margin_EUR"] = (df["Ticket_Revenue_EUR"] - df["Operating_Cost_EUR"]).round(2)
    df["Cost_Recovery_Pct"] = (
        (df["Ticket_Revenue_EUR"] / df["Operating_Cost_EUR"]) * 100.0
    ).round(2)
    df["Complaints_per_10k_Pax"] = (
        (df["Accessibility_Complaints"] / df["Passengers"]) * 10000.0
    ).round(2)
    df["Passengers_per_Trip"] = (df["Passengers"] / df["Trips"]).round(2)
    df["CO2_per_Pax_KG"] = (df["CO2_Saved_KG"] / df["Passengers"]).round(4)
    df["CO2_per_kWh"] = np.where(
        df["Energy_Consumption_KWh"] > 0,
        (df["CO2_Saved_KG"] / df["Energy_Consumption_KWh"]).round(3),
        np.nan,
    )
    df["Fare_per_Pax_EUR"] = (df["Ticket_Revenue_EUR"] / df["Passengers"]).round(4)
    df["Cost_per_Pax_EUR"] = (df["Operating_Cost_EUR"] / df["Passengers"]).round(4)
    df["Margin_per_Pax_EUR"] = (df["Net_Margin_EUR"] / df["Passengers"]).round(4)
    return df


def compute_initial_statistics(df: pd.DataFrame) -> pd.DataFrame:
    """Compute comprehensive parametric and non-parametric descriptive statistics."""
    numeric_cols = [
        "Passengers",
        "Trips",
        "Average_Delay_Minutes",
        "On_Time_Percentage",
        "Ticket_Revenue_EUR",
        "Operating_Cost_EUR",
        "Net_Margin_EUR",
        "Cost_Recovery_Pct",
        "CO2_Saved_KG",
        "Energy_Consumption_KWh",
        "Customer_Rating",
        "Accessibility_Complaints",
        "Complaints_per_10k_Pax",
        "Passengers_per_Trip",
        "Fare_per_Pax_EUR",
        "Cost_per_Pax_EUR",
        "Margin_per_Pax_EUR",
    ]
    stats = pd.DataFrame(
        {
            "Count": df[numeric_cols].count(),
            "Missing": df[numeric_cols].isnull().sum(),
            "Mean": df[numeric_cols].mean(),
            "SD": df[numeric_cols].std(),
            "Median": df[numeric_cols].median(),
            "Q25": df[numeric_cols].quantile(0.25),
            "Q75": df[numeric_cols].quantile(0.75),
            "IQR": df[numeric_cols].quantile(0.75) - df[numeric_cols].quantile(0.25),
            "Min": df[numeric_cols].min(),
            "Max": df[numeric_cols].max(),
            "Skewness": df[numeric_cols].skew(),
        }
    ).round(2)
    stats.index.name = "Variable"
    return stats


def compute_mix_adjusted_cities(df: pd.DataFrame) -> pd.DataFrame:
    """First-Principles Direct Standardisation: adjust city means for modal sampling mix."""
    mode_weights = df["Transport_Mode"].value_counts(normalize=True)
    city_mode = (
        df.groupby(["City", "Transport_Mode"], as_index=False)
        .agg(
            Mean_Pax=("Passengers", "mean"),
            Mean_Margin=("Net_Margin_EUR", "mean"),
            Mean_Delay=("Average_Delay_Minutes", "mean"),
            Records=("Record_ID", "count"),
        )
    )
    city_mode["Network_Mode_Weight"] = city_mode["Transport_Mode"].map(mode_weights)
    city_mode["Adj_Pax_Contrib"] = city_mode["Mean_Pax"] * city_mode["Network_Mode_Weight"]
    city_mode["Adj_Margin_Contrib"] = city_mode["Mean_Margin"] * city_mode["Network_Mode_Weight"]
    city_mode["Adj_Delay_Contrib"] = city_mode["Mean_Delay"] * city_mode["Network_Mode_Weight"]

    adj = (
        city_mode.groupby("City", as_index=False)
        .agg(
            Mix_Adj_Mean_Pax=("Adj_Pax_Contrib", "sum"),
            Mix_Adj_Mean_Margin_EUR=("Adj_Margin_Contrib", "sum"),
            Mix_Adj_Mean_Delay_Min=("Adj_Delay_Contrib", "sum"),
        )
    )
    raw = (
        df.groupby(["Country", "City"], as_index=False)
        .agg(
            Records=("Record_ID", "count"),
            Total_Passengers=("Passengers", "sum"),
            Raw_Mean_Pax=("Passengers", "mean"),
            Total_Net_Margin_EUR=("Net_Margin_EUR", "sum"),
            Raw_Mean_Margin_EUR=("Net_Margin_EUR", "mean"),
            Raw_Mean_Delay_Min=("Average_Delay_Minutes", "mean"),
            Micromobility_Share_Pct=(
                "Transport_Mode",
                lambda s: s.isin(["Bike Share", "E-Scooter"]).mean() * 100.0,
            ),
            Rail_Share_Pct=(
                "Transport_Mode",
                lambda s: s.isin(["Metro", "Tram"]).mean() * 100.0,
            ),
        )
    )
    merged = raw.merge(adj, on="City")
    merged["Raw_Margin_Rank"] = merged["Raw_Mean_Margin_EUR"].rank(ascending=False).astype(int)
    merged["Mix_Adj_Margin_Rank"] = merged["Mix_Adj_Mean_Margin_EUR"].rank(ascending=False).astype(int)
    merged["Rank_Shift"] = merged["Raw_Margin_Rank"] - merged["Mix_Adj_Margin_Rank"]
    merged["Raw_Pax_Rank"] = merged["Raw_Mean_Pax"].rank(ascending=False).astype(int)
    merged["Mix_Adj_Pax_Rank"] = merged["Mix_Adj_Mean_Pax"].rank(ascending=False).astype(int)
    return merged.sort_values("Raw_Mean_Margin_EUR", ascending=False).round(2)


def compute_unit_economics_and_carbon(df: pd.DataFrame) -> pd.DataFrame:
    """First-Principles Unit Economics (OLS Cost Slope) & Marginal Carbon Abatement Return."""
    rows = []
    for mode, grp in df.groupby("Transport_Mode"):
        slope_cost, intercept_cost = np.polyfit(grp["Passengers"], grp["Operating_Cost_EUR"], 1)
        slope_rev, intercept_rev = np.polyfit(grp["Passengers"], grp["Ticket_Revenue_EUR"], 1)
        r_cost = np.corrcoef(grp["Passengers"], grp["Operating_Cost_EUR"])[0, 1]
        tot_rev = grp["Ticket_Revenue_EUR"].sum()
        tot_cost = grp["Operating_Cost_EUR"].sum()
        tot_margin = grp["Net_Margin_EUR"].sum()
        tot_pax = grp["Passengers"].sum()
        tot_co2_t = grp["CO2_Saved_KG"].sum() / 1000.0
        tot_kwh = grp["Energy_Consumption_KWh"].sum()
        rows.append(
            {
                "Transport_Mode": mode,
                "Records": len(grp),
                "Mean_Pax_per_Day": grp["Passengers"].mean(),
                "Mean_Fare_per_Pax_EUR": tot_rev / tot_pax,
                "Mean_Cost_per_Pax_EUR": tot_cost / tot_pax,
                "Net_Margin_per_Pax_EUR": tot_margin / tot_pax,
                "OLS_Fixed_Cost_EUR": intercept_cost,
                "OLS_Variable_Cost_per_Pax_EUR": slope_cost,
                "OLS_Marginal_Contribution_per_Pax_EUR": slope_rev - slope_cost,
                "Cost_Pax_R2": r_cost**2,
                "Total_CO2_Saved_Tonnes": tot_co2_t,
                "Net_Return_per_Tonne_CO2_EUR": tot_margin / tot_co2_t,
                "kWh_per_100_Pax": (tot_kwh / tot_pax) * 100.0,
            }
        )
    return pd.DataFrame(rows).sort_values("Net_Margin_per_Pax_EUR", ascending=False).round(2)


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    TABLES_DIR.mkdir(parents=True, exist_ok=True)

    df = load_and_clean_data()
    cleaned_csv = DATA_DIR / "ecomove_cleaned.csv"
    df.to_csv(cleaned_csv, index=False)

    stats = compute_initial_statistics(df)
    stats_csv = TABLES_DIR / "table01_initial_statistics.csv"
    stats.to_csv(stats_csv)

    # Mode summary table
    mode_tbl = (
        df.groupby("Transport_Mode")
        .agg(
            Records=("Record_ID", "count"),
            Total_Passengers=("Passengers", "sum"),
            Mean_Passengers=("Passengers", "mean"),
            Median_Delay_Min=("Average_Delay_Minutes", "median"),
            Mean_Delay_Min=("Average_Delay_Minutes", "mean"),
            Mean_OnTime_Pct=("On_Time_Percentage", "mean"),
            Total_Revenue_EUR=("Ticket_Revenue_EUR", "sum"),
            Total_Cost_EUR=("Operating_Cost_EUR", "sum"),
            Net_Margin_EUR=("Net_Margin_EUR", "sum"),
            Total_CO2_KG=("CO2_Saved_KG", "sum"),
            Total_Energy_KWh=("Energy_Consumption_KWh", "sum"),
            Mean_Rating=("Customer_Rating", "mean"),
            Total_Complaints=("Accessibility_Complaints", "sum"),
        )
        .round(2)
    )
    mode_tbl["Cost_Recovery_Pct"] = (
        mode_tbl["Total_Revenue_EUR"] / mode_tbl["Total_Cost_EUR"] * 100.0
    ).round(2)
    mode_tbl["Complaints_per_10k_Pax"] = (
        mode_tbl["Total_Complaints"] / mode_tbl["Total_Passengers"] * 10000.0
    ).round(2)
    mode_tbl["CO2_per_kWh"] = np.where(
        mode_tbl["Total_Energy_KWh"] > 0,
        (mode_tbl["Total_CO2_KG"] / mode_tbl["Total_Energy_KWh"]).round(2),
        np.nan,
    )
    mode_tbl.to_csv(TABLES_DIR / "table02_mode_summary.csv")

    # City summary table
    city_tbl = (
        df.groupby(["Country", "City"])
        .agg(
            Records=("Record_ID", "count"),
            Total_Passengers=("Passengers", "sum"),
            Mean_Passengers=("Passengers", "mean"),
            Mean_Delay_Min=("Average_Delay_Minutes", "mean"),
            Mean_OnTime_Pct=("On_Time_Percentage", "mean"),
            Total_Revenue_EUR=("Ticket_Revenue_EUR", "sum"),
            Total_Cost_EUR=("Operating_Cost_EUR", "sum"),
            Net_Margin_EUR=("Net_Margin_EUR", "sum"),
            Total_CO2_KG=("CO2_Saved_KG", "sum"),
            Mean_Rating=("Customer_Rating", "mean"),
            Total_Complaints=("Accessibility_Complaints", "sum"),
        )
        .round(2)
    )
    city_tbl["Cost_Recovery_Pct"] = (
        city_tbl["Total_Revenue_EUR"] / city_tbl["Total_Cost_EUR"] * 100.0
    ).round(2)
    city_tbl["Complaints_per_10k_Pax"] = (
        city_tbl["Total_Complaints"] / city_tbl["Total_Passengers"] * 10000.0
    ).round(2)
    city_tbl = city_tbl.sort_values("Total_Passengers", ascending=False)
    city_tbl.to_csv(TABLES_DIR / "table03_city_summary.csv")

    # Table 4: Mix-Adjusted Cities (Simpson's Paradox Decomposition)
    mix_adj_tbl = compute_mix_adjusted_cities(df)
    mix_adj_tbl.to_csv(TABLES_DIR / "table04_mix_adjusted_cities.csv", index=False)

    # Table 5: Unit Economics & Marginal Carbon Abatement Cost
    unit_econ_tbl = compute_unit_economics_and_carbon(df)
    unit_econ_tbl.to_csv(TABLES_DIR / "table05_unit_economics_and_carbon_cost.csv", index=False)

    # Table 6: Route x Mode Accessibility Complaint Intensity Matrix (per 10k Pax)
    acc_piv = (
        df.pivot_table(
            index="Route_Type",
            columns="Transport_Mode",
            values="Complaints_per_10k_Pax",
            aggfunc="mean",
        )
        .round(2)
    )
    acc_piv.to_csv(TABLES_DIR / "table06_route_mode_accessibility_matrix.csv")

    print("=" * 72)
    print("ECOMOVE MOBILITY DATASET — FIRST-PRINCIPLES & EDA SUMMARY")
    print("=" * 72)
    print(f"Raw file:        {RAW_XLSX.name}")
    print(f"Cleaned shape:   {df.shape[0]:,} rows x {df.shape[1]} columns")
    print("\n--- TABLE 4: SIMPSON'S PARADOX / MIX-ADJUSTED CITY PERFORMANCE ---")
    print(mix_adj_tbl.to_string(index=False))
    print("\n--- TABLE 5: UNIT ECONOMICS & CARBON ABATEMENT RETURN BY MODE ---")
    print(unit_econ_tbl.to_string(index=False))
    print("\n--- TABLE 6: ROUTE x MODE ACCESSIBILITY COMPLAINTS PER 10K PAX ---")
    print(acc_piv.to_string())


if __name__ == "__main__":
    main()

