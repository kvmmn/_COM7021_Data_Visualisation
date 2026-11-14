from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW_XLSX = ROOT / "[5442] EcoMoveMobility.xlsx"
DATA_DIR = ROOT / "data"
TABLES_DIR = ROOT / "output" / "tables"
EXCEL_EPOCH = pd.Timestamp("1899-12-30")


def load_and_clean_data(xlsx_path=RAW_XLSX):
    df = pd.read_excel(xlsx_path, sheet_name="Dataset").dropna(axis=1, how="all").copy()

    iso_dates = EXCEL_EPOCH + pd.to_timedelta(df["Date"], unit="D")
    df["Date_ISO"] = iso_dates
    df["Year"] = iso_dates.dt.year
    df["Month"] = iso_dates.dt.month
    df["Month_Name"] = iso_dates.dt.strftime("%b")
    df["YearMonth"] = iso_dates.dt.to_period("M").astype(str)
    df["Day_Name"] = iso_dates.dt.day_name()
    df["Is_Weekend"] = np.where(iso_dates.dt.dayofweek >= 5, "Weekend", "Weekday")

    rev = df["Ticket_Revenue_EUR"]
    cost = df["Operating_Cost_EUR"]
    pax = df["Passengers"]
    kwh = df["Energy_Consumption_KWh"]

    df["Net_Margin_EUR"] = (rev - cost).round(2)
    df["Cost_Recovery_Pct"] = ((rev / cost) * 100.0).round(2)
    df["Complaints_per_10k_Pax"] = ((df["Accessibility_Complaints"] / pax) * 10000.0).round(2)
    df["Passengers_per_Trip"] = (pax / df["Trips"]).round(2)
    df["CO2_per_Pax_KG"] = (df["CO2_Saved_KG"] / pax).round(4)
    df["CO2_per_kWh"] = np.where(kwh > 0, (df["CO2_Saved_KG"] / kwh).round(3), np.nan)
    df["Fare_per_Pax_EUR"] = (rev / pax).round(4)
    df["Cost_per_Pax_EUR"] = (cost / pax).round(4)
    df["Margin_per_Pax_EUR"] = (df["Net_Margin_EUR"] / pax).round(4)
    return df


def compute_initial_statistics(df):
    skip = {"Date", "Year", "Month", "CO2_per_Pax_KG", "CO2_per_kWh"}
    sub = df[[c for c in df.select_dtypes(include="number").columns if c not in skip]]
    stats = sub.describe().T.rename(
        columns={"count": "Count", "mean": "Mean", "std": "SD", "25%": "Q25", "50%": "Median", "75%": "Q75", "min": "Min", "max": "Max"}
    )
    stats.insert(1, "Missing", sub.isna().sum())
    stats["Count"] = stats["Count"].astype(int)
    stats.insert(7, "IQR", stats["Q75"] - stats["Q25"])
    stats["Skewness"] = sub.skew()
    stats.index.name = "Variable"
    return stats[["Count", "Missing", "Mean", "SD", "Median", "Q25", "Q75", "IQR", "Min", "Max", "Skewness"]].round(2)


def compute_mix_adjusted_cities(df: pd.DataFrame) -> pd.DataFrame:
    weights = df["Transport_Mode"].value_counts(normalize=True)
    cell = (
        df.groupby(["City", "Transport_Mode"], as_index=False)
        .agg(
            Mean_Pax=("Passengers", "mean"),
            Mean_Margin=("Net_Margin_EUR", "mean"),
            Mean_Delay=("Average_Delay_Minutes", "mean"),
            Records=("Record_ID", "count"),
        )
    )
    w = cell["Transport_Mode"].map(weights)
    cell["Adj_Pax_Contrib"] = cell["Mean_Pax"] * w
    cell["Adj_Margin_Contrib"] = cell["Mean_Margin"] * w
    cell["Adj_Delay_Contrib"] = cell["Mean_Delay"] * w

    adj = cell.groupby("City", as_index=False).agg(
        Mix_Adj_Mean_Pax=("Adj_Pax_Contrib", "sum"),
        Mix_Adj_Mean_Margin_EUR=("Adj_Margin_Contrib", "sum"),
        Mix_Adj_Mean_Delay_Min=("Adj_Delay_Contrib", "sum"),
    )
    raw = df.groupby(["Country", "City"], as_index=False).agg(
        Records=("Record_ID", "count"),
        Total_Passengers=("Passengers", "sum"),
        Raw_Mean_Pax=("Passengers", "mean"),
        Total_Net_Margin_EUR=("Net_Margin_EUR", "sum"),
        Raw_Mean_Margin_EUR=("Net_Margin_EUR", "mean"),
        Raw_Mean_Delay_Min=("Average_Delay_Minutes", "mean"),
        Micromobility_Share_Pct=("Transport_Mode", lambda s: s.isin(["Bike Share", "E-Scooter"]).mean() * 100.0),
        Rail_Share_Pct=("Transport_Mode", lambda s: s.isin(["Metro", "Tram"]).mean() * 100.0),
    )
    out = raw.merge(adj, on="City")
    out["Raw_Margin_Rank"] = out["Raw_Mean_Margin_EUR"].rank(ascending=False).astype(int)
    out["Mix_Adj_Margin_Rank"] = out["Mix_Adj_Mean_Margin_EUR"].rank(ascending=False).astype(int)
    out["Rank_Shift"] = out["Raw_Margin_Rank"] - out["Mix_Adj_Margin_Rank"]
    out["Raw_Pax_Rank"] = out["Raw_Mean_Pax"].rank(ascending=False).astype(int)
    out["Mix_Adj_Pax_Rank"] = out["Mix_Adj_Mean_Pax"].rank(ascending=False).astype(int)
    return out.sort_values("Raw_Mean_Margin_EUR", ascending=False).round(2)


def compute_unit_economics_and_carbon(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for mode, grp in df.groupby("Transport_Mode"):
        x = grp["Passengers"]
        slope_cost, intercept_cost = np.polyfit(x, grp["Operating_Cost_EUR"], 1)
        slope_rev, _ = np.polyfit(x, grp["Ticket_Revenue_EUR"], 1)
        r_cost = np.corrcoef(x, grp["Operating_Cost_EUR"])[0, 1]
        tot_rev = grp["Ticket_Revenue_EUR"].sum()
        tot_cost = grp["Operating_Cost_EUR"].sum()
        tot_margin = grp["Net_Margin_EUR"].sum()
        tot_pax = x.sum()
        tot_co2_t = grp["CO2_Saved_KG"].sum() / 1000.0
        rows.append(
            {
                "Transport_Mode": mode,
                "Records": len(grp),
                "Mean_Pax_per_Day": x.mean(),
                "Mean_Fare_per_Pax_EUR": tot_rev / tot_pax,
                "Mean_Cost_per_Pax_EUR": tot_cost / tot_pax,
                "Net_Margin_per_Pax_EUR": tot_margin / tot_pax,
                "OLS_Fixed_Cost_EUR": intercept_cost,
                "OLS_Variable_Cost_per_Pax_EUR": slope_cost,
                "OLS_Marginal_Contribution_per_Pax_EUR": slope_rev - slope_cost,
                "Cost_Pax_R2": r_cost**2,
                "Total_CO2_Saved_Tonnes": tot_co2_t,
                "Net_Return_per_Tonne_CO2_EUR": tot_margin / tot_co2_t,
                "kWh_per_100_Pax": (grp["Energy_Consumption_KWh"].sum() / tot_pax) * 100.0,
            }
        )
    return pd.DataFrame(rows).sort_values("Net_Margin_per_Pax_EUR", ascending=False).round(2)


def _enrich_grouped_ratios(tbl: pd.DataFrame, grouped) -> pd.DataFrame:
    tbl["Cost_Recovery_Pct"] = (tbl["Total_Revenue_EUR"] / tbl["Total_Cost_EUR"] * 100.0).round(2)
    tbl["Mean_Record_Cost_Recovery_Pct"] = grouped["Cost_Recovery_Pct"].mean().round(2)
    tbl["Complaints_per_10k_Pax"] = (tbl["Total_Complaints"] / tbl["Total_Passengers"] * 10000.0).round(2)
    return tbl


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    TABLES_DIR.mkdir(parents=True, exist_ok=True)

    df = load_and_clean_data()
    df.to_csv(DATA_DIR / "ecomove_cleaned.csv", index=False)
    compute_initial_statistics(df).to_csv(TABLES_DIR / "table01_initial_statistics.csv")

    base_metrics = {
        "Records": ("Record_ID", "count"),
        "Total_Passengers": ("Passengers", "sum"),
        "Mean_Passengers": ("Passengers", "mean"),
        "Mean_Delay_Min": ("Average_Delay_Minutes", "mean"),
        "Mean_OnTime_Pct": ("On_Time_Percentage", "mean"),
        "Total_Revenue_EUR": ("Ticket_Revenue_EUR", "sum"),
        "Total_Cost_EUR": ("Operating_Cost_EUR", "sum"),
        "Net_Margin_EUR": ("Net_Margin_EUR", "sum"),
        "Total_CO2_KG": ("CO2_Saved_KG", "sum"),
        "Mean_Rating": ("Customer_Rating", "mean"),
        "Total_Complaints": ("Accessibility_Complaints", "sum"),
    }

    mode_grp = df.groupby("Transport_Mode")
    mode_tbl = mode_grp.agg(
        **base_metrics,
        Median_Delay_Min=("Average_Delay_Minutes", "median"),
        Total_Energy_KWh=("Energy_Consumption_KWh", "sum"),
    ).round(2)
    _enrich_grouped_ratios(mode_tbl, mode_grp)
    mode_tbl["Mean_Record_Complaints_per_10k"] = mode_grp["Complaints_per_10k_Pax"].mean().round(2)
    mode_tbl["CO2_per_kWh"] = np.where(
        mode_tbl["Total_Energy_KWh"] > 0, (mode_tbl["Total_CO2_KG"] / mode_tbl["Total_Energy_KWh"]).round(2), np.nan
    )
    mode_tbl.to_csv(TABLES_DIR / "table02_mode_summary.csv")

    city_grp = df.groupby(["Country", "City"])
    city_tbl = city_grp.agg(**base_metrics, Mean_Margin_EUR=("Net_Margin_EUR", "mean")).round(2)
    _enrich_grouped_ratios(city_tbl, city_grp)
    city_tbl.sort_values("Total_Passengers", ascending=False).to_csv(TABLES_DIR / "table03_city_summary.csv")

    compute_mix_adjusted_cities(df).to_csv(TABLES_DIR / "table04_mix_adjusted_cities.csv", index=False)
    compute_unit_economics_and_carbon(df).to_csv(TABLES_DIR / "table05_unit_economics_and_carbon_cost.csv", index=False)

    acc = df.groupby(["Route_Type", "Transport_Mode"], as_index=False).agg(
        Total_Complaints=("Accessibility_Complaints", "sum"),
        Total_Passengers=("Passengers", "sum"),
    )
    acc["Rate"] = (acc["Total_Complaints"] / acc["Total_Passengers"] * 10000.0).round(2)
    acc.pivot(index="Route_Type", columns="Transport_Mode", values="Rate").round(2).to_csv(
        TABLES_DIR / "table06_route_mode_accessibility_matrix.csv"
    )
    print(f"Cleaned rows: {len(df):,} | Tables saved to {TABLES_DIR}")


if __name__ == "__main__":
    main()
