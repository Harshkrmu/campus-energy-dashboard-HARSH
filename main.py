import os
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO, format='[LOG] %(message)s')

DATA_DIR = Path("data")
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

# ---------------------------------------------------------
# TASK 1: DATA INGESTION + VALIDATION
# ---------------------------------------------------------

def load_and_merge():
    csv_files = list(DATA_DIR.glob("*.csv"))
    if not csv_files:
        logging.warning("No CSV files found in /data/")
        return pd.DataFrame()

    frames = []
    for file in csv_files:
        try:
            df = pd.read_csv(
                file,
                parse_dates=["timestamp"],
                on_bad_lines="skip"
            )
        except Exception as e:
            logging.error(f"Error reading {file}: {e}")
            continue

        # clean kwh column
        if "kwh" not in df.columns:
            for alt in ["energy", "usage", "units"]:
                if alt in df.columns:
                    df.rename(columns={alt: "kwh"}, inplace=True)

        # add metadata from file name
        name = file.stem
        parts = name.split("_")
        building = parts[0]
        month = parts[-1]

        df["building"] = building
        df["month"] = month

        frames.append(df)

    df_combined = pd.concat(frames, ignore_index=True)
    logging.info("Merged all building data successfully.")
    return df_combined


# ---------------------------------------------------------
# TASK 2: AGGREGATIONS
# ---------------------------------------------------------

def calculate_daily_totals(df):
    df_daily = df.set_index("timestamp").resample("D")["kwh"].sum().reset_index()
    return df_daily

def calculate_weekly_totals(df):
    df_weekly = df.set_index("timestamp").resample("W")["kwh"].sum().reset_index()
    return df_weekly

def building_summary(df):
    return df.groupby("building")["kwh"].agg(["min", "max", "mean", "sum"]).reset_index()


# ---------------------------------------------------------
# TASK 3: OOP MODELING
# ---------------------------------------------------------

class MeterReading:
    def __init__(self, timestamp, kwh):
        self.timestamp = timestamp
        self.kwh = kwh

class Building:
    def __init__(self, name):
        self.name = name
        self.readings = []

    def add_reading(self, reading: MeterReading):
        self.readings.append(reading)

    def calculate_total_consumption(self):
        return sum(r.kwh for r in self.readings)

    def generate_report(self):
        total = self.calculate_total_consumption()
        return f"{self.name}: Total Consumption = {total:.2f} kWh"

class BuildingManager:
    def __init__(self):
        self.buildings = {}

    def add_record(self, building, timestamp, kwh):
        if building not in self.buildings:
            self.buildings[building] = Building(building)
        self.buildings[building].add_reading(MeterReading(timestamp, kwh))

    def generate_all_reports(self):
        return [b.generate_report() for b in self.buildings.values()]


# ---------------------------------------------------------
# TASK 4: DASHBOARD (MATPLOTLIB)
# ---------------------------------------------------------

def generate_dashboard(df):
    fig, axs = plt.subplots(3, 1, figsize=(10, 14))

    # Trend line – daily
    df_daily = calculate_daily_totals(df)
    axs[0].plot(df_daily["timestamp"], df_daily["kwh"])
    axs[0].set_title("Daily Energy Consumption (All Buildings)")
    axs[0].set_ylabel("kWh")

    # Weekly bar chart
    df_weekly = calculate_weekly_totals(df)
    axs[1].bar(df_weekly["timestamp"], df_weekly["kwh"])
    axs[1].set_title("Weekly Total Consumption")
    axs[1].set_ylabel("kWh")

    # Scatter – peak hours
    axs[2].scatter(df["timestamp"], df["kwh"], s=10)
    axs[2].set_title("Scatter Plot – Consumption Over Time")
    axs[2].set_ylabel("kWh")

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "dashboard.png")
    plt.close()
    logging.info("Saved dashboard.png")


# ---------------------------------------------------------
# TASK 5: EXPORT + SUMMARY
# ---------------------------------------------------------

def export_outputs(df):
    df.to_csv(OUTPUT_DIR / "cleaned_energy_data.csv", index=False)

    summary = building_summary(df)
    summary.to_csv(OUTPUT_DIR / "building_summary.csv", index=False)

    total_consumption = df["kwh"].sum()
    highest = summary.loc[summary["sum"].idxmax()]["building"]
    peak_time = df.loc[df["kwh"].idxmax()]["timestamp"]

    text = f"""
CAMPUS ENERGY SUMMARY REPORT
----------------------------

Total Campus Consumption: {total_consumption:.2f} kWh
Highest Consuming Building: {highest}
Peak Load Time: {peak_time}

Daily and weekly trends have been processed.
Visual dashboard saved as dashboard.png
"""

    with open(OUTPUT_DIR / "summary.txt", "w") as f:
        f.write(text)

    logging.info("Exported summary + CSVs.")


# ---------------------------------------------------------
# MAIN EXECUTION
# ---------------------------------------------------------

def main():
    df = load_and_merge()
    if df.empty:
        return

    # OOP population
    manager = BuildingManager()
    for _, r in df.iterrows():
        manager.add_record(r["building"], r["timestamp"], r["kwh"])

    generate_dashboard(df)
    export_outputs(df)

    print("\n".join(manager.generate_all_reports()))


if __name__ == "__main__":
    main()
