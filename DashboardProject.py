import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
st.set_page_config(layout="wide")

st.sidebar.date_input("Select a date")

st.title("📊 E-Commerce Performance Dashboard")
st.markdown("Welcome! Track sales performance, regional breakdowns, and category profitability below.")
st.write("---")

df = pd.read_csv("clean_data_e-commerce.csv")

with st.expander("📂 View Raw Cleaned Data"):
    st.dataframe(df, use_container_width=True)


df['Order Date'] = pd.to_datetime(df['Order Date'])


monthly_sales = df.resample('M', on='Order Date')['Sales'].sum().reset_index()
st.subheader("Monthly Sales Trend")
fig = px.area(monthly_sales, x='Order Date', y='Sales', 
              title="Sales Performance Over Time",
              labels={'Sales': 'Total Revenue', 'Order Date': 'Year'})
st.plotly_chart(fig, use_container_width=True)

st.subheader("Sales Breakdown by Region and Category")

fig = px.sunburst(
    df, 
    path=['Region', 'Category'], 
    values='Sales', 
    title="Click on a Region slice to drill down into its Categories"
)


fig.update_traces(textinfo="label+percent parent")

st.plotly_chart(fig, use_container_width=True)

st.subheader("Detailed Category Profit Trends")

category_list = df['Category'].dropna().unique()
selected_category = st.selectbox("Select a Category to view its profit timeline:", category_list)

category_df = df[df['Category'] == selected_category]

monthly_cat_profit = category_df.resample('M', on='Order Date')['Profit'].sum().reset_index()

fig_line_profit = px.line(
    monthly_cat_profit, 
    x='Order Date', 
    y='Profit', 
    title=f"Monthly Profit Performance for: {selected_category}",
    labels={'Profit': 'Total Profit ($)', 'Order Date': 'Timeline'},
    markers=True 
)

fig_line_profit.update_traces(line_color='#2ECC71') 

st.plotly_chart(fig_line_profit, use_container_width=True)
