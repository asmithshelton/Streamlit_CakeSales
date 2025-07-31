import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
@st.cache
def load_data():
    try:
        df = pd.read_csv("sales.csv")
        df['OrderDate'] = pd.to_datetime(df['OrderDate'], errors='coerce')
        return df.dropna(subset=["OrderDate"])
    except Exception as e:
        st.error(f"⚠️ Failed to load data: {e}")
        return pd.DataFrame()

df = load_data()

# Sidebar filters
st.sidebar.header("📅 Filter Orders")
min_date = df['OrderDate'].min()
max_date = df['OrderDate'].max()
start_date, end_date = st.sidebar.date_input("Select date range", [min_date, max_date])

filtered_df = df[(df['OrderDate'] >= pd.to_datetime(start_date)) & (df['OrderDate'] <= pd.to_datetime(end_date))]

# Dashboard
st.title("🎂 Ukrop’s Custom Cake Sales Dashboard")

# KPI Metrics
total_sales = filtered_df['RetailPrice'].sum()
total_orders = filtered_df['FSOrderNumber'].nunique()
top_cake = filtered_df['CakeName'].value_counts().idxmax()

st.metric("Total Sales", f"${total_sales:,.2f}")
st.metric("Total Orders", total_orders)
st.metric("Top-Selling Cake", top_cake)

# Sales over time
st.subheader("📈 Sales Trend")
daily_sales = filtered_df.groupby('OrderDate')['RetailPrice'].sum().reset_index()
fig1 = px.line(daily_sales, x='OrderDate', y='RetailPrice', title="Daily Sales", markers=True)
st.plotly_chart(fig1, use_container_width=True)

# Top Cakes
st.subheader("🎂 Top 10 Cakes by Orders")
top_cakes = filtered_df['CakeName'].value_counts().nlargest(10).reset_index()
top_cakes.columns = ['CakeName', 'Orders']
fig2 = px.bar(top_cakes, x='Orders', y='CakeName', orientation='h', title="Top 10 Bestsellers", text='Orders')
st.plotly_chart(fig2, use_container_width=True)

# Detailed Table
st.subheader("🔍 Order Details")
st.dataframe(filtered_df.sort_values(by="OrderDate", ascending=False))
