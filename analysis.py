"""
============================================================
PROJECT 1: SALES DASHBOARD - ANALYSIS SCRIPT
============================================================
Author: Shovit Nayak
Purpose: Analyze cleaned sales data and extract business insights
Skills Demonstrated: Data Analysis, GroupBy, Aggregation, Business Intelligence
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set style for beautiful charts
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")

# ============================================================
# LOAD CLEANED DATA
# ============================================================
print("=" * 60)
print("SALES DATA ANALYSIS")
print("=" * 60)

df = pd.read_csv('sales_data_cleaned.csv')
df['Order_Date'] = pd.to_datetime(df['Order_Date'])

print(f"Analyzing {len(df)} sales records...")

# ============================================================
# KPI OVERVIEW
# ============================================================
print("=" * 60)
print("KEY PERFORMANCE INDICATORS (KPIs)")
print("=" * 60)

total_revenue = df['Total_Amount'].sum()
total_orders = len(df)
total_customers = df['Customer_Name'].nunique()
avg_order_value = df['Total_Amount'].mean()
total_units = df['Quantity'].sum()

print(f"💰 Total Revenue:        ${total_revenue:>12,.2f}")
print(f"📦 Total Orders:         {total_orders:>12,}")
print(f"👥 Unique Customers:       {total_customers:>12,}")
print(f"📊 Average Order Value:  ${avg_order_value:>12,.2f}")
print(f"📦 Total Units Sold:     {total_units:>12,}")

# ============================================================
# ANALYSIS 1: REVENUE BY CATEGORY
# ============================================================
print("" + "=" * 60)
print("ANALYSIS 1: REVENUE BY CATEGORY")
print("=" * 60)

category_analysis = df.groupby('Category').agg({
    'Total_Amount': ['sum', 'mean'],
    'Quantity': 'sum',
    'Order_ID': 'count'
}).round(2)

category_analysis.columns = ['Total_Revenue', 'Avg_Order_Value', 'Units_Sold', 'Order_Count']
category_analysis['Revenue_Share_%'] = (category_analysis['Total_Revenue'] / total_revenue * 100).round(1)
category_analysis = category_analysis.sort_values('Total_Revenue', ascending=False)

print(category_analysis)

# Insight
best_category = category_analysis.index[0]
print(f"💡 INSIGHT: {best_category} generates the most revenue!")

# ============================================================
# ANALYSIS 2: REGIONAL PERFORMANCE
# ============================================================
print("" + "=" * 60)
print("ANALYSIS 2: REGIONAL PERFORMANCE")
print("=" * 60)

region_analysis = df.groupby('Region').agg({
    'Total_Amount': 'sum',
    'Order_ID': 'count',
    'Customer_Name': 'nunique'
}).round(2)

region_analysis.columns = ['Revenue', 'Orders', 'Unique_Customers']
region_analysis['Revenue_Share_%'] = (region_analysis['Revenue'] / total_revenue * 100).round(1)
region_analysis['Avg_Revenue_per_Customer'] = (region_analysis['Revenue'] / region_analysis['Unique_Customers']).round(2)
region_analysis = region_analysis.sort_values('Revenue', ascending=False)

print(region_analysis)

best_region = region_analysis.index[0]
print(f"💡 INSIGHT: {best_region} region is our top performer!")

# ============================================================
# ANALYSIS 3: MONTHLY TRENDS
# ============================================================
print("" + "=" * 60)
print("ANALYSIS 3: MONTHLY SALES TRENDS")
print("=" * 60)

monthly = df.groupby(df['Order_Date'].dt.to_period('M')).agg({
    'Total_Amount': 'sum',
    'Order_ID': 'count'
}).round(2)

monthly.columns = ['Revenue', 'Orders']
monthly['MoM_Growth_%'] = monthly['Revenue'].pct_change() * 100
monthly = monthly.round(1)

print(monthly.tail(12))

# Find best month
best_month = monthly['Revenue'].idxmax()
print(f"💡 INSIGHT: Best month was {best_month} with ${monthly.loc[best_month, 'Revenue']:,.2f} revenue!")

# ============================================================
# ANALYSIS 4: TOP PRODUCTS
# ============================================================
print("" + "=" * 60)
print("ANALYSIS 4: TOP 10 PRODUCTS BY REVENUE")
print("=" * 60)

product_analysis = df.groupby('Product').agg({
    'Total_Amount': 'sum',
    'Quantity': 'sum',
    'Order_ID': 'count'
}).round(2)

product_analysis.columns = ['Revenue', 'Units_Sold', 'Orders']
product_analysis = product_analysis.sort_values('Revenue', ascending=False)

print(product_analysis.head(10))

best_product = product_analysis.index[0]
print(f"💡 INSIGHT: {best_product} is our best-selling product!")

# ============================================================
# ANALYSIS 5: PAYMENT METHOD PREFERENCES
# ============================================================
print("" + "=" * 60)
print("ANALYSIS 5: PAYMENT METHOD PREFERENCES")
print("=" * 60)

payment_analysis = df.groupby('Payment_Method').agg({
    'Total_Amount': 'sum',
    'Order_ID': 'count'
}).round(2)

payment_analysis.columns = ['Revenue', 'Orders']
payment_analysis['Revenue_Share_%'] = (payment_analysis['Revenue'] / total_revenue * 100).round(1)
payment_analysis = payment_analysis.sort_values('Revenue', ascending=False)

print(payment_analysis)

popular_payment = payment_analysis.index[0]
print(f"💡 INSIGHT: {popular_payment} is the most popular payment method!")

# ============================================================
# ANALYSIS 6: CUSTOMER SEGMENTATION
# ============================================================
print("" + "=" * 60)
print("ANALYSIS 6: CUSTOMER SEGMENTATION (RFM-style)")
print("=" * 60)

customer_stats = df.groupby('Customer_Name').agg({
    'Total_Amount': 'sum',
    'Order_ID': 'count',
    'Order_Date': 'max'
}).round(2)

customer_stats.columns = ['Total_Spent', 'Order_Count', 'Last_Order']
customer_stats = customer_stats.sort_values('Total_Spent', ascending=False)

# Segment customers
def segment_customer(row):
    if row['Total_Spent'] >= 5000:
        return 'VIP'
    elif row['Total_Spent'] >= 2000:
        return 'Premium'
    elif row['Total_Spent'] >= 500:
        return 'Regular'
    else:
        return 'New'

customer_stats['Segment'] = customer_stats.apply(segment_customer, axis=1)
segment_summary = customer_stats['Segment'].value_counts()

print("Customer Segments:")
print(segment_summary)
print(f"💡 INSIGHT: We have {segment_summary.get('VIP', 0)} VIP customers who drive major revenue!")

# ============================================================
# SAVE ANALYSIS RESULTS
# ============================================================
print("" + "=" * 60)
print("SAVING ANALYSIS RESULTS")
print("=" * 60)

category_analysis.to_csv('analysis_category.csv')
region_analysis.to_csv('analysis_region.csv')
monthly.to_csv('analysis_monthly.csv')
product_analysis.to_csv('analysis_products.csv')
payment_analysis.to_csv('analysis_payment.csv')
customer_stats.to_csv('analysis_customers.csv')

print("✅ All analysis results saved to CSV files!")
print("" + "=" * 60)
print("ANALYSIS COMPLETE!")
print("=" * 60)
