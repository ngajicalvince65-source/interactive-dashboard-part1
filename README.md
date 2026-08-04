\# Retail Sales Interactive Dashboard



\## Overview

This project is an interactive dashboard built with Streamlit that explores a synthetic retail sales dataset of 750,000 records. It includes an Overview page with summary metrics and charts, and a Drill-Down page for filtered record-level exploration.



\## Requirements

\- Python 3.10 or higher

\- streamlit

\- pandas

\- plotly



Install dependencies with:

\## How to Run

1\. Open a terminal and navigate to the `app` folder.

2\. Run:

3\. The app will open automatically in your default browser at `http://localhost:8501`.



\## Live Version

This app is also deployed on Streamlit Community Cloud:

https://interactive-dashboard-part1-dtgx8zsez5chcibnc9ymjk.streamlit.app



\## Features

\- \*\*Overview page:\*\* total revenue, order count, average order value, average satisfaction score, revenue by category, revenue by region, and a revenue trend line over time.

\- \*\*Drill-Down page:\*\* a filtered data table, a customer satisfaction distribution chart, an orders-by-payment-method chart, and a button to download the currently filtered data as a CSV.

\- \*\*Filters:\*\* region, product category, and payment method (multi-select dropdowns), an order date range slider, and a checkbox to exclude rows with missing values.

\- \*\*Refresh mechanism:\*\* a sidebar button that clears the cached data and reloads the CSV file, along with a timestamp of the last load.



\## Data

The dataset is a synthetic retail sales file generated with NumPy and pandas, described in full in the technical report located in the `docs` folder.



