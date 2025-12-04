Campus Energy-Use Dashboard
Programming for Problem Solving Using Python
Capstone Project – Energy Consumption Analysis & Visualization
📌 Project Overview

This project provides a complete end-to-end pipeline for analyzing campus electricity usage.
It reads raw meter data from multiple buildings, validates and merges them, performs daily & weekly aggregations, builds an object-oriented model for energy consumption, generates visual dashboards, and exports an executive summary for administrators.

The goal is to help the campus facilities team identify energy-saving opportunities through data-driven insights.

🎯 Objectives

By completing this project, the student demonstrates the ability to:

Ingest and clean multiple datasets

Use Pandas for time-series analysis

Build reusable, modular data-processing functions

Apply Object-Oriented Programming for real-world modeling

Create multi-chart visualizations using Matplotlib

Export results (CSV + summary report)

Build a structured, reproducible project suitable for GitHub submission

📂 Project Structure
campus-energy-dashboard-<yourname>/
│
├── data/                     # Raw CSV files (input)
├── output/                   # Auto-generated files
│   ├── cleaned_energy_data.csv
│   ├── building_summary.csv
│   ├── dashboard.png
│   └── summary.txt
│
├── main.py                   # Main pipeline (Tasks 1–5)
├── generate_sample_data.py   # Optional sample dataset generator
├── requirements.txt          # Dependencies
└── README.md                 # Project documentation

🧩 Features Implemented
✅ Task 1 – Data Ingestion & Validation

Auto-detects all .csv files in /data/

Handles missing/corrupted lines with exception handling

Extracts building name & month from filename

Merges all buildings into a single DataFrame

✅ Task 2 – Aggregation Logic

Implemented:

calculate_daily_totals(df)

calculate_weekly_totals(df)

building_summary(df)

Outputs:

Daily energy totals

Weekly totals

Per-building statistics (min, max, mean, total)

✅ Task 3 – Object-Oriented Modeling

Classes used:

MeterReading

Stores a single timestamp + kWh pair.

Building

Holds all readings of a single building

Calculates total building consumption

Generates building-level reports

BuildingManager

Holds all building objects

Adds records dynamically

Generates reports for the entire campus

✅ Task 4 – Visualization Dashboard

The script generates a multi-chart dashboard using Matplotlib:

Trend Line – Daily consumption

Bar Chart – Weekly totals

Scatter Plot – Usage distribution over time

Saved as:

output/dashboard.png

✅ Task 5 – Export & Summary

Automatically exported:

cleaned_energy_data.csv

building_summary.csv

dashboard.png

summary.txt

The summary file includes:

Total campus consumption

Highest consuming building

Peak load time

Trend insights

▶ How to Run This Project
Step 1 — Install dependencies
pip install -r requirements.txt

Step 2 — Add CSV files

Place all building CSV files inside /data/ folder.

OR
Run the sample generator:

python generate_sample_data.py

Step 3 — Run main script
python main.py

Step 4 — View Outputs

All results will appear in /output/:

Cleaned dataset

Summary statistics

Full dashboard image

Executive summary report

🧪 Sample Dataset Format

Each CSV file should contain:

timestamp,kwh
2024-11-01 00:00,22.5
2024-11-01 01:00,21.8
...


Filename format:

Building_A_2024-11.csv

📊 Visualization Example

The dashboard includes:

Daily trend line

Weekly bar chart

Scatter plot across timestamps

All merged in a single PNG.

🏫 Academic Integrity

This is an individual assignment.
All code is original and written for academic purposes.

👨‍💻 Author

HARSH
B.Tech CSE
K.R. Mangalam University
