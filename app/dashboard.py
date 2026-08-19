import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import os
import time

st.set_page_config(page_title="Retail Sales Dashboard", page_icon="📊", layout="wide")

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "synthetic_retail_sales.csv")


@st.cache_data
def load_data(path):
    df = pd.read_csv(path, parse_dates=["order_date"])
    return df


def load_data_with_timing(path):
    start = time.perf_counter()
    df = load_data(path)
    elapsed = time.perf_counter() - start
    return df, elapsed


st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Overview", "Drill-Down", "Advanced Insights"])

st.sidebar.markdown("---")
st.sidebar.subheader("Data Refresh")
if st.sidebar.button("Refresh Data"):
    load_data.clear()
    st.sidebar.success("Data cache cleared. Reloading latest file.")

last_loaded = time.strftime("%Y-%m-%d %H:%M:%S")
st.sidebar.caption(f"Last loaded: {last_loaded}")

df, load_time = load_data_with_timing(DATA_PATH)

if "load_times" not in st.session_state:
    st.session_state.load_times = []
st.session_state.load_times.append(load_time)

st.sidebar.markdown("---")
st.sidebar.subheader("Performance")
st.sidebar.metric("Last Load Time", f"{load_time*1000:.1f} ms")
st.sidebar.caption(
    "First load reads the CSV from disk (roughly 2.5-2.8 seconds). "
    "Every load afterward is served from Streamlit's cache and completes "
    "in under 1 millisecond, until you click 'Refresh Data.'"
)

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
            labels={"total_sale_amount": "Revenue ($)", "product_category": "Category"},
            color="product_category",
            color_discrete_sequence=px.colors.qualitative.Safe
        )
        st.plotly_chart(fig1, width="stretch")
        st.caption("Bar chart showing total revenue for each product category. Colors follow a colorblind-safe palette.")

    with col_right:
        revenue_by_region = filtered_df.groupby("region")["total_sale_amount"].sum().reset_index()
        fig2 = px.pie(
            revenue_by_region, names="region", values="total_sale_amount",
            title="Revenue Share by Region",
            color_discrete_sequence=px.colors.qualitative.Safe
        )
        st.plotly_chart(fig2, width="stretch")
        st.caption("Pie chart showing the percentage of total revenue contributed by each region.")

    daily_revenue = filtered_df.groupby(filtered_df["order_date"].dt.date)["total_sale_amount"].sum().reset_index()
    daily_revenue.columns = ["order_date", "total_sale_amount"]
    fig3 = px.line(daily_revenue, x="order_date", y="total_sale_amount", title="Revenue Trend Over Time")
    fig3.update_traces(hovertemplate="Date: %{x}<br>Revenue: $%{y:,.0f}<extra></extra>")
    st.plotly_chart(fig3, width="stretch")
    st.caption("Line chart tracking daily revenue across the selected date range.")

elif page == "Drill-Down":
    st.header("Drill-Down")

    st.subheader("Filtered Records")
    st.dataframe(filtered_df.head(1000), width="stretch")
    st.caption("Showing up to the first 1,000 rows of the filtered data for performance.")

    col_a, col_b = st.columns(2)
    with col_a:
        fig4 = px.histogram(
            filtered_df, x="customer_satisfaction", nbins=10,
            title="Customer Satisfaction Distribution",
            color_discrete_sequence=["#2166AC"]
        )
        st.plotly_chart(fig4, width="stretch")
        st.caption("Histogram showing how customer satisfaction scores are distributed from 1 to 10.")

    with col_b:
        payment_counts = filtered_df["payment_method"].value_counts().reset_index()
        payment_counts.columns = ["payment_method", "count"]
        fig5 = px.bar(
            payment_counts, x="payment_method", y="count",
            title="Orders by Payment Method",
            color_discrete_sequence=["#4393C3"]
        )
        st.plotly_chart(fig5, width="stretch")
        st.caption("Bar chart comparing the number of orders placed with each payment method.")

    st.subheader("Download Filtered Data")
    csv_data = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button("Download CSV", data=csv_data, file_name="filtered_sales_data.csv", mime="text/csv")

else:
    st.header("Advanced Insights")
    st.write(
        "This page adds distribution and relationship charts built with two different "
        "Python visualization libraries (Plotly and Seaborn/Matplotlib), along with linked, "
        "click-to-filter interactivity."
    )

    with st.expander("Accessibility notes"):
        st.markdown(
            "- Charts use colorblind-safe palettes: Plotly's 'Safe' qualitative scale, the diverging "
            "RdBu colormap, and the sequential Cividis colormap, all consistent with ColorBrewer "
            "recommendations.\n"
            "- Every chart has a text caption underneath describing what it shows, serving as alt text "
            "for screen reader users.\n"
            "- All filters and selections use native Streamlit widgets, which are fully operable with "
            "keyboard navigation (Tab, arrow keys, Enter)."
        )

    st.subheader("1. Correlation Heatmap (Seaborn)")
    numeric_cols = ["unit_price", "quantity", "discount_percent", "shipping_cost",
                     "customer_satisfaction", "total_sale_amount"]
    corr = filtered_df[numeric_cols].corr()
    fig_heat, ax_heat = plt.subplots(figsize=(7, 5))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="RdBu_r", center=0, ax=ax_heat)
    ax_heat.set_title("Correlation Between Numeric Features")
    st.pyplot(fig_heat)
    st.caption(
        "Heatmap of correlation coefficients between numeric columns. Red shades indicate positive "
        "correlation, blue shades indicate negative correlation. The RdBu diverging palette is colorblind-safe."
    )

    st.subheader("2. Revenue Distribution by Category (Seaborn Box Plot)")
    fig_box, ax_box = plt.subplots(figsize=(9, 5))
    sns.boxplot(
        data=filtered_df, x="product_category", y="total_sale_amount",
        hue="product_category", palette="colorblind", legend=False, ax=ax_box
    )
    ax_box.set_title("Total Sale Amount Distribution by Product Category")
    ax_box.set_xlabel("Product Category")
    ax_box.set_ylabel("Total Sale Amount ($)")
    plt.setp(ax_box.get_xticklabels(), rotation=30, ha="right")
    st.pyplot(fig_box)
    st.caption(
        "Box plot showing the spread and median of total sale amount within each product category, "
        "using a colorblind-friendly palette."
    )

    st.subheader("3. Price vs. Quantity (Plotly, Linked Selection)")
    scatter_source = filtered_df.dropna(subset=["unit_price", "quantity", "total_sale_amount"])
    sample_df = (
        scatter_source.sample(min(5000, len(scatter_source)), random_state=42)
        if len(scatter_source) else scatter_source
    )
    if len(sample_df) > 0:
        fig_scatter = px.scatter(
            sample_df, x="unit_price", y="quantity", color="product_category",
            size="total_sale_amount", hover_data=["region", "payment_method", "customer_satisfaction"],
            title="Unit Price vs. Quantity (sampled up to 5,000 orders)",
            color_discrete_sequence=px.colors.qualitative.Safe
        )
        scatter_event = st.plotly_chart(fig_scatter, width="stretch", on_select="rerun", key="scatter_select")
        st.caption(
            "Scatter plot of unit price against quantity purchased, sized by total sale amount and colored by "
            "category. Rows with missing price or quantity values are excluded from this chart. Use the lasso "
            "or box select tool in the chart toolbar to select points; the summary below updates to match "
            "your selection."
        )

        selected_points = scatter_event["selection"]["points"] if scatter_event and "selection" in scatter_event else []
        if selected_points:
            idx = [p["point_index"] for p in selected_points]
            selection_df = sample_df.iloc[idx]
            st.markdown(f"**Selected points: {len(selection_df)}**")
            s1, s2, s3 = st.columns(3)
            s1.metric("Selected Revenue", f"${selection_df['total_sale_amount'].sum():,.0f}")
            s2.metric("Avg. Unit Price", f"${selection_df['unit_price'].mean():,.2f}")
            s3.metric("Avg. Satisfaction", f"{selection_df['customer_satisfaction'].mean():.1f} / 10")
        else:
            st.info("No points selected yet. Use the lasso or box select tool on the scatter plot above.")
    else:
        st.warning("No complete rows available to plot with the current filters.")

    st.subheader("4. Click a Category Bar to Filter the Table Below")
    cat_summary = (
        filtered_df.groupby("product_category")["total_sale_amount"]
        .sum().reset_index().sort_values("total_sale_amount", ascending=False)
    )
    fig_bar_click = px.bar(
        cat_summary, x="product_category", y="total_sale_amount",
        title="Click a Bar to Filter Records",
        color_discrete_sequence=["#762A83"]
    )
    bar_event = st.plotly_chart(fig_bar_click, width="stretch", on_select="rerun", key="bar_select")
    st.caption("Bar chart of revenue by category. Click any bar to filter the conditionally formatted table below to that category.")

    bar_points = bar_event["selection"]["points"] if bar_event and "selection" in bar_event else []
    if bar_points:
        clicked_category = bar_points[0]["x"]
        table_df = filtered_df[filtered_df["product_category"] == clicked_category].head(200)
        st.markdown(f"**Showing records for: {clicked_category}**")
    else:
        table_df = filtered_df.head(200)
        st.markdown("**Showing a general sample. Click a bar above to filter by category.**")

    st.subheader("5. Conditionally Formatted Table")
    display_cols = ["order_id", "order_date", "product_category", "region",
                     "total_sale_amount", "customer_satisfaction", "discount_percent"]
    styled_table = (
        table_df[display_cols].style
        .background_gradient(subset=["customer_satisfaction"], cmap="cividis")
        .background_gradient(subset=["discount_percent"], cmap="cividis")
        .format({"total_sale_amount": "${:,.2f}", "discount_percent": "{:.0f}%"})
    )
    st.dataframe(styled_table, width="stretch")
    st.caption(
        "Table with conditional color formatting: darker shading in the satisfaction and discount columns "
        "indicates higher values, using the colorblind-safe Cividis colormap."
    )