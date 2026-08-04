import streamlit as st
import pandas as pd
import plotly.express as px
import os
import time

st.set_page_config(page_title="Retail Sales Dashboard", page_icon="📊", layout="wide")

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "synthetic_retail_sales.csv")


@st.cache_data
def load_data(path):
    df = pd.read_csv(path, parse_dates=["order_date"])
    return df


st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Overview", "Drill-Down"])

st.sidebar.markdown("---")
st.sidebar.subheader("Data Refresh")
if st.sidebar.button("Refresh Data"):
    load_data.clear()
    st.sidebar.success("Data cache cleared. Reloading latest file.")

last_loaded = time.strftime("%Y-%m-%d %H:%M:%S")
st.sidebar.caption(f"Last loaded: {last_loaded}")

df = load_data(DATA_PATH)

st.sidebar.markdown("---")
st.sidebar.subheader("Filters")

regions = sorted(df["region"].unique())
categories = sorted(df["product_category"].unique())
payment_methods = sorted(df["payment_method"].unique())

selected_regions = st.sidebar.multiselect("Region", regions, default=regions)
selected_categories = st.sidebar.multiselect("Product Category", categories, default=categories)
selected_payment = st.sidebar.multiselect("Payment Method", payment_methods, default=payment_methods)

min_date = df["order_date"].min().date()
max_date = df["order_date"].max().date()
date_range = st.sidebar.slider(
    "Order Date Range",
    min_value=min_date,
    max_value=max_date,
    value=(min_date, max_date)
)

exclude_missing = st.sidebar.checkbox("Exclude rows with missing values", value=False)

filtered_df = df[
    df["region"].isin(selected_regions)
    & df["product_category"].isin(selected_categories)
    & df["payment_method"].isin(selected_payment)
    & (df["order_date"].dt.date >= date_range[0])
    & (df["order_date"].dt.date <= date_range[1])
]

if exclude_missing:
    filtered_df = filtered_df.dropna()

st.title("Retail Sales Interactive Dashboard")
st.caption(f"Showing {len(filtered_df):,} of {len(df):,} total rows based on current filters.")

if page == "Overview":
    st.header("Overview")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Revenue", f"${filtered_df['total_sale_amount'].sum():,.0f}")
    col2.metric("Total Orders", f"{len(filtered_df):,}")
    avg_order = filtered_df["total_sale_amount"].mean() if len(filtered_df) else 0
    col3.metric("Average Order Value", f"${avg_order:,.2f}")
    avg_satisfaction = filtered_df["customer_satisfaction"].mean() if len(filtered_df) else 0
    col4.metric("Avg. Satisfaction", f"{avg_satisfaction:.1f} / 10")

    col_left, col_right = st.columns(2)

    with col_left:
        revenue_by_category = (
            filtered_df.groupby("product_category")["total_sale_amount"]
            .sum()
            .reset_index()
            .sort_values("total_sale_amount", ascending=False)
        )
        fig1 = px.bar(
            revenue_by_category,
            x="product_category",
            y="total_sale_amount",
            title="Revenue by Product Category",
            labels={"total_sale_amount": "Revenue ($)", "product_category": "Category"}
        )
        st.plotly_chart(fig1, use_container_width=True)

    with col_right:
        revenue_by_region = filtered_df.groupby("region")["total_sale_amount"].sum().reset_index()
        fig2 = px.pie(revenue_by_region, names="region", values="total_sale_amount", title="Revenue Share by Region")
        st.plotly_chart(fig2, use_container_width=True)

    daily_revenue = filtered_df.groupby(filtered_df["order_date"].dt.date)["total_sale_amount"].sum().reset_index()
    daily_revenue.columns = ["order_date", "total_sale_amount"]
    fig3 = px.line(daily_revenue, x="order_date", y="total_sale_amount", title="Revenue Trend Over Time")
    st.plotly_chart(fig3, use_container_width=True)

else:
    st.header("Drill-Down")

    st.subheader("Filtered Records")
    st.dataframe(filtered_df.head(1000), use_container_width=True)
    st.caption("Showing up to the first 1,000 rows of the filtered data for performance.")

    col_a, col_b = st.columns(2)
    with col_a:
        fig4 = px.histogram(filtered_df, x="customer_satisfaction", nbins=10, title="Customer Satisfaction Distribution")
        st.plotly_chart(fig4, use_container_width=True)

    with col_b:
        payment_counts = filtered_df["payment_method"].value_counts().reset_index()
        payment_counts.columns = ["payment_method", "count"]
        fig5 = px.bar(payment_counts, x="payment_method", y="count", title="Orders by Payment Method")
        st.plotly_chart(fig5, use_container_width=True)

    st.subheader("Download Filtered Data")
    csv_data = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button("Download CSV", data=csv_data, file_name="filtered_sales_data.csv", mime="text/csv")