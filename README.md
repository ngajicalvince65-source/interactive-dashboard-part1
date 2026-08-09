# Retail Sales Interactive Dashboard

## Overview
This project is an interactive dashboard built with Streamlit that explores a synthetic retail sales dataset of 750,000 records. It includes an Overview page with summary metrics and charts, a Drill-Down page for filtered record-level exploration, and an Advanced Insights page with additional chart types and linked, click-to-filter interactivity.

## Requirements
- Python 3.10 or higher
- streamlit
- pandas
- plotly
- matplotlib
- seaborn

Install dependencies with:
## How to Run
1. Open a terminal and navigate to the `app` folder.
2. Run:
3. The app will open automatically in your default browser at `http://localhost:8501`.

## Live Version
This app is also deployed on Streamlit Community Cloud:
https://interactive-dashboard-part1-dtgx8zsez5chcibnc9ymjk.streamlit.app

## Features

### Overview page
Total revenue, order count, average order value, average satisfaction score, revenue by category, revenue by region, and a revenue trend line over time.

### Drill-Down page
A filtered data table, a customer satisfaction distribution chart, an orders-by-payment-method chart, and a button to download the currently filtered data as a CSV.

### Advanced Insights page
- A correlation heatmap built with Seaborn, showing relationships between all numeric fields.
- A box plot built with Seaborn, showing the distribution of total sale amount within each product category.
- A Plotly scatter plot of unit price versus quantity, with lasso and box select tools. Selecting points updates a set of summary metrics below the chart, forming a linked visualization.
- A Plotly bar chart that filters the record table below it when a bar is clicked, another example of linked, click-to-filter interactivity.
- A conditionally formatted table using color gradients on the satisfaction and discount columns to highlight higher values.

### Filters
Region, product category, and payment method (multi-select dropdowns), an order date range slider, and a checkbox to exclude rows with missing values. These filters apply across all three pages.

### Refresh mechanism
A sidebar button that clears the cached data and reloads the CSV file, along with a timestamp of the last load.

### Accessibility considerations
- All charts use colorblind-safe palettes (Plotly's Safe qualitative scale, the RdBu diverging colormap, and the Cividis sequential colormap), consistent with ColorBrewer recommendations.
- Every chart includes a text caption describing what it shows, serving as alt text for screen reader users.
- All filters and interactive elements use native Streamlit widgets, which support full keyboard navigation.

## Data
The dataset is a synthetic retail sales file generated with NumPy and pandas, described in full in the technical report located in the `docs` folder.