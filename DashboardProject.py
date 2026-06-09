import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

st.sidebar.date_input("Select a date")
st.title("📊 E-Commerce Performance Dashboard")
st.markdown("Welcome! Track sales performance, regional breakdowns, and category profitability below.")
st.write("---")

# 1. Cache the data loading so interactions are lightning-fast
@st.cache_data
def load_data():
    df = pd.read_csv("clean_data_e-commerce.csv")
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    return df

df = load_data()

# --- Top Row: Raw Data Expander ---
with st.expander("📂 View Raw Cleaned Data"):
    st.dataframe(df, use_container_width=True)

st.write("---")

# --- Interactive Tabs: Completely eliminates vertical scrolling ---
tab1, tab2, tab3 = st.tabs([
    "📈 Monthly Sales Trend", 
    "🌍 Regional Breakdown", 
    "💰 Category Profit"
])

# Tab 1: Monthly Sales Trend
with tab1:
    monthly_sales = df.resample('ME', on='Order Date')['Sales'].sum().reset_index()
    fig1 = px.area(monthly_sales, x='Order Date', y='Sales', 
                   title="Sales Performance Over Time", 
                   labels={'Sales': 'Total Revenue', 'Order Date': 'Year'})
    st.plotly_chart(fig1, use_container_width=True)

# Tab 2: Regional Breakdown (Sized larger and centered)
with tab2:
    fig2 = px.sunburst(df, path=['Region', 'Category'], values='Sales', 
                      title="Click on a Region slice to drill down",
                      height=700) 
    fig2.update_traces(textinfo="label+percent parent")
    
    # Centering grid so it looks clean on wide displays
    left_spacer, center_content, right_spacer = st.columns([1, 5, 1])
    with center_content:
        st.plotly_chart(fig2, use_container_width=True)

# Tab 3: Detailed Category Profit Trends (Using a form container to lock scroll)
with tab3:
    category_list = df['Category'].dropna().unique()
    
    # Using a Streamlit form stops automatic scroll-jumping on selection changes
    with st.form("profit_filter_form", clear_on_submit=False):
        selected_category = st.selectbox("Select a Category for the Profit Timeline:", category_list)
        submit_button = st.form_submit_button(label="Update Chart", type="primary")
    
    # Filter and construct the timeline dynamically
    category_df = df[df['Category'] == selected_category]
    monthly_cat_profit = category_df.resample('ME', on='Order Date')['Profit'].sum().reset_index()
    
    fig3 = px.line(monthly_cat_profit, x='Order Date', y='Profit', 
                              title=f"Monthly Profit for: {selected_category}", 
                              labels={'Profit': 'Total Profit ($)', 'Order Date': 'Timeline'}, 
                              markers=True)
    fig3.update_traces(line_color='#2ECC71')
    st.plotly_chart(fig3, use_container_width=True)
