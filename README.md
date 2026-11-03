# Retail Sales Interactive Dashboard

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://interactive-dashboard-part1-dtgx8zsez5chcibnc9ymjk.streamlit.app)

**Live application:** https://interactive-dashboard-part1-dtgx8zsez5chcibnc9ymjk.streamlit.app

```math
\begin{aligned}
&\textbf{Interactive analytics on 750{,}000 synthetic retail sales records} \\[4pt]
&\text{Revenue} = \sum_{i} \text{sale}_i, \qquad \text{Average order value} = \frac{\sum_i \text{sale}_i}{\text{number of orders}} \\[4pt]
&\text{Three linked pages: Overview} \;\rightarrow\; \text{Drill-Down} \;\rightarrow\; \text{Advanced Insights}
\end{aligned}
```

## Overview
An interactive Streamlit dashboard that explores a synthetic retail sales dataset of 750,000 records. It has an Overview page with summary metrics and charts, a Drill-Down page for filtered record-level exploration, and an Advanced Insights page with additional chart types and linked, click-to-filter interactivity.

## Features
**Overview page:** total revenue, order count, average order value, average satisfaction score, revenue by category, revenue by region, and a revenue trend over time.

**Drill-Down page:** a filtered data table, a customer satisfaction distribution, orders by payment method, and a button to download the filtered data as a CSV.

**Advanced Insights page**
- Correlation heatmap (Seaborn) across all numeric fields.
- Box plot (Seaborn) of total sale amount by product category.
- Plotly scatter plot of unit price against quantity with lasso and box selection; the selection updates summary metrics below the chart.
- Plotly bar chart that filters the record table when a bar is clicked.
- Conditionally formatted table with colour gradients on satisfaction and discount.

**Filters:** region, product category and payment method, an order date range, and an option to exclude rows with missing values. Filters apply across all three pages.

**Performance:** data are cached; the first load reads the CSV from disk and later loads are served from cache. A sidebar button clears the cache and reloads the file, and the sidebar shows the last load time.

**Accessibility:** colour-blind-safe palettes (Plotly Safe, RdBu, Cividis), a text caption under every chart, and native Streamlit widgets with keyboard navigation.

## Run locally
```bash
pip install -r requirements.txt
cd app
streamlit run dashboard.py
```
The app opens at `http://localhost:8501`.

## Repository structure
| Path | Contents |
|---|---|
| `app/dashboard.py` | Streamlit application |
| `data/synthetic_retail_sales.csv` | Synthetic dataset generated with NumPy and pandas |
| `requirements.txt` | Python libraries |

## Tools
Python, Streamlit, pandas, Plotly, Matplotlib, Seaborn, Streamlit Community Cloud

## Author
Ngaji Calvince Otieno
