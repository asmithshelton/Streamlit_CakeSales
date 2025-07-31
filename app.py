import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# App Config
st.set_page_config(page_title="🎂 Custom Cake Sales Dashboard", layout="wide")

# Load data
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("sales.csv")
        df['OrderDate'] = pd.to_datetime(df['OrderDate'], errors='coerce')
        return df.dropna(subset=["OrderDate"])
    except Exception as e:
        st.error(f"⚠️ Failed to load data: {e}")
        return pd.DataFrame()

df = load_data()

# Sidebar Filters
with st.sidebar:
    st.header("📅 Filter Orders")
    min_date = df['OrderDate'].min()
    max_date = df['OrderDate'].max()
    start_date, end_date = st.date_input("Select date range", [min_date, max_date])
    st.markdown("---")
    st.caption("💡 Select a date range to update the dashboard.")

filtered_df = df[
    (df['OrderDate'] >= pd.to_datetime(start_date)) &
    (df['OrderDate'] <= pd.to_datetime(end_date))
]

# Title & Header
st.markdown("<h1 style='text-align: center;'>🎂 Custom Cake Sales Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

# KPIs with Columns
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="💵 Total Sales", value=f"${filtered_df['RetailPrice'].sum():,.2f}")
with col2:
    st.metric(label="🧾 Total Orders", value=filtered_df['FSOrderNumber'].nunique())
with col3:
    if not filtered_df.empty:
        top_cake = filtered_df['CakeName'].value_counts().idxmax()
        st.metric(label="🏆 Top-Selling Cake", value=top_cake)
    else:
        st.metric(label="🏆 Top-Selling Cake", value="N/A")

# Sales Trend
st.subheader("📈 Daily Sales Trend")
if not filtered_df.empty:
    daily_sales = (
        filtered_df.groupby('OrderDate')['RetailPrice']
        .sum()
        .reset_index()
        .sort_values('OrderDate')
    )
    fig1 = px.line(
        daily_sales,
        x='OrderDate',
        y='RetailPrice',
        markers=True,
        template="plotly_white",
        color_discrete_sequence=["#D62728"]
    )
    fig1.update_layout(title="", xaxis_title="Date", yaxis_title="Total Sales ($)")
    st.plotly_chart(fig1, use_container_width=True)
else:
    st.warning("No data for the selected date range.")

# Top Cakes
st.subheader("🍰 Top 10 Best-Selling Cakes")
if not filtered_df.empty:
    top_cakes = filtered_df['CakeName'].value_counts().nlargest(10).reset_index()
    top_cakes.columns = ['CakeName', 'Orders']
    fig2 = px.bar(
        top_cakes,
        x='Orders',
        y='CakeName',
        orientation='h',
        text='Orders',
        template="plotly_white",
        color_discrete_sequence=["#1F77B4"]
    )
    fig2.update_layout(xaxis_title="Orders", yaxis_title="Cake Name", showlegend=False)
    st.plotly_chart(fig2, use_container_width=True)
else:
    st.info("No cakes to show for the selected range.")

# Detailed Table
st.subheader("📋 Detailed Order Table")
st.dataframe(filtered_df.sort_values(by="OrderDate", ascending=False), use_container_width=True)
