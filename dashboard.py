"""
============================================================
PROJECT 1: SALES DASHBOARD - STREAMLIT WEB APP
============================================================
Author: Shovit Nayak
Purpose: Interactive sales dashboard for data analyst portfolio
Skills Demonstrated: Streamlit, Data Visualization, Dashboard Design

HOW TO RUN:
    1. Make sure you have Streamlit installed: pip install streamlit
    2. Run: streamlit run dashboard.py
    3. Open the URL shown in your browser
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ============================================================
# PAGE CONFIGURATION
# ============================================================
st.set_page_config(
    page_title="Sales Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM CSS FOR BETTER LOOKS
# ============================================================
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .kpi-card {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .kpi-value {
        font-size: 2rem;
        font-weight: bold;
        color: #1f77b4;
    }
    .kpi-label {
        font-size: 1rem;
        color: #666;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# LOAD DATA
# ============================================================
@st.cache_data
def load_data():
    df = pd.read_csv('sales_data_cleaned.csv')
    df['Order_Date'] = pd.to_datetime(df['Order_Date'])
    return df

df = load_data()

# ============================================================
# SIDEBAR FILTERS
# ============================================================
st.sidebar.title("🔧 Filters")
st.sidebar.markdown("---")

# Date range filter
min_date = df['Order_Date'].min().date()
max_date = df['Order_Date'].max().date()
date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# Region filter
regions = ['All'] + sorted(df['Region'].unique().tolist())
selected_region = st.sidebar.selectbox("Select Region", regions)

# Category filter
categories = ['All'] + sorted(df['Category'].unique().tolist())
selected_category = st.sidebar.selectbox("Select Category", categories)

# Payment method filter
payments = ['All'] + sorted(df['Payment_Method'].unique().tolist())
selected_payment = st.sidebar.selectbox("Payment Method", payments)

# ============================================================
# APPLY FILTERS
# ============================================================
filtered_df = df.copy()

if len(date_range) == 2:
    filtered_df = filtered_df[
        (filtered_df['Order_Date'].dt.date >= date_range[0]) &
        (filtered_df['Order_Date'].dt.date <= date_range[1])
    ]

if selected_region != 'All':
    filtered_df = filtered_df[filtered_df['Region'] == selected_region]

if selected_category != 'All':
    filtered_df = filtered_df[filtered_df['Category'] == selected_category]

if selected_payment != 'All':
    filtered_df = filtered_df[filtered_df['Payment_Method'] == selected_payment]

# ============================================================
# HEADER
# ============================================================
st.markdown('<p class="main-header">📊 Sales Analytics Dashboard</p>', unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #666;'>Interactive dashboard for sales performance analysis</p>", unsafe_allow_html=True)

# ============================================================
# KPI CARDS
# ============================================================
st.markdown("---")
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-value">${filtered_df['Total_Amount'].sum():,.0f}</div>
        <div class="kpi-label">Total Revenue</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-value">{len(filtered_df):,}</div>
        <div class="kpi-label">Total Orders</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-value">{filtered_df['Customer_Name'].nunique():,}</div>
        <div class="kpi-label">Unique Customers</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-value">${filtered_df['Total_Amount'].mean():,.0f}</div>
        <div class="kpi-label">Avg Order Value</div>
    </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-value">{filtered_df['Quantity'].sum():,}</div>
        <div class="kpi-label">Units Sold</div>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# CHARTS ROW 1
# ============================================================
st.markdown("---")
col1, col2 = st.columns(2)

# Chart 1: Revenue by Category
with col1:
    st.subheader("📈 Revenue by Category")
    cat_revenue = filtered_df.groupby('Category')['Total_Amount'].sum().reset_index()
    cat_revenue = cat_revenue.sort_values('Total_Amount', ascending=True)

    fig1 = px.bar(
        cat_revenue,
        x='Total_Amount',
        y='Category',
        orientation='h',
        color='Category',
        text=cat_revenue['Total_Amount'].apply(lambda x: f'${x:,.0f}'),
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig1.update_layout(showlegend=False, height=400)
    fig1.update_traces(textposition='outside')
    st.plotly_chart(fig1, use_container_width=True)

# Chart 2: Monthly Trend
with col2:
    st.subheader("📅 Monthly Sales Trend")
    monthly = filtered_df.groupby(filtered_df['Order_Date'].dt.to_period('M'))['Total_Amount'].sum().reset_index()
    monthly['Order_Date'] = monthly['Order_Date'].astype(str)

    fig2 = px.line(
        monthly,
        x='Order_Date',
        y='Total_Amount',
        markers=True,
        line_shape='spline',
        color_discrete_sequence=['#1f77b4']
    )
    fig2.update_layout(height=400, xaxis_title="Month", yaxis_title="Revenue ($)")
    st.plotly_chart(fig2, use_container_width=True)

# ============================================================
# CHARTS ROW 2
# ============================================================
st.markdown("---")
col1, col2 = st.columns(2)

# Chart 3: Regional Performance
with col1:
    st.subheader("🌍 Regional Performance")
    region_data = filtered_df.groupby('Region').agg({
        'Total_Amount': 'sum',
        'Order_ID': 'count'
    }).reset_index()
    region_data.columns = ['Region', 'Revenue', 'Orders']

    fig3 = px.pie(
        region_data,
        values='Revenue',
        names='Region',
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig3.update_layout(height=400)
    st.plotly_chart(fig3, use_container_width=True)

# Chart 4: Top Products
with col2:
    st.subheader("🏆 Top 10 Products")
    top_products = filtered_df.groupby('Product')['Total_Amount'].sum().reset_index()
    top_products = top_products.sort_values('Total_Amount', ascending=True).tail(10)

    fig4 = px.bar(
        top_products,
        x='Total_Amount',
        y='Product',
        orientation='h',
        color='Total_Amount',
        color_continuous_scale='Blues',
        text=top_products['Total_Amount'].apply(lambda x: f'${x:,.0f}')
    )
    fig4.update_layout(showlegend=False, height=400, coloraxis_showscale=False)
    fig4.update_traces(textposition='outside')
    st.plotly_chart(fig4, use_container_width=True)

# ============================================================
# CHARTS ROW 3
# ============================================================
st.markdown("---")
col1, col2 = st.columns(2)

# Chart 5: Payment Method Distribution
with col1:
    st.subheader("💳 Payment Methods")
    payment_data = filtered_df.groupby('Payment_Method')['Total_Amount'].sum().reset_index()
    payment_data = payment_data.sort_values('Total_Amount', ascending=False)

    fig5 = px.bar(
        payment_data,
        x='Payment_Method',
        y='Total_Amount',
        color='Payment_Method',
        text=payment_data['Total_Amount'].apply(lambda x: f'${x:,.0f}'),
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig5.update_layout(showlegend=False, height=400)
    fig5.update_traces(textposition='outside')
    st.plotly_chart(fig5, use_container_width=True)

# Chart 6: Order Status
with col2:
    st.subheader("📋 Order Status Distribution")
    status_data = filtered_df['Order_Status'].value_counts().reset_index()
    status_data.columns = ['Status', 'Count']

    fig6 = px.bar(
        status_data,
        x='Status',
        y='Count',
        color='Status',
        text='Count',
        color_discrete_sequence=px.colors.qualitative.Set1
    )
    fig6.update_layout(showlegend=False, height=400)
    fig6.update_traces(textposition='outside')
    st.plotly_chart(fig6, use_container_width=True)

# ============================================================
# DATA TABLE
# ============================================================
st.markdown("---")
st.subheader("📋 Detailed Sales Data")

# Show data with pagination
page_size = st.selectbox("Rows per page", [10, 25, 50, 100], index=0)
display_df = filtered_df[['Order_ID', 'Order_Date', 'Customer_Name', 'Product', 
                           'Category', 'Quantity', 'Unit_Price', 'Discount_Percent', 
                           'Total_Amount', 'Region', 'City', 'Order_Status']].copy()
display_df['Order_Date'] = display_df['Order_Date'].dt.strftime('%Y-%m-%d')

st.dataframe(display_df.head(page_size), use_container_width=True)

# Download button
st.download_button(
    label="📥 Download Filtered Data as CSV",
    data=filtered_df.to_csv(index=False),
    file_name="filtered_sales_data.csv",
    mime="text/csv"
)

# ============================================================
# FOOTER
# ============================================================
st.markdown("---")
st.markdown("<p style='text-align: center; color: #999;'>Built with ❤️ by Shovit Nayak | Data Analyst Portfolio Project</p>", unsafe_allow_html=True)
