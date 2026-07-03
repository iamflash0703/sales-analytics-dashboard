"""
============================================================
PROJECT 1: SALES DASHBOARD - DATA CLEANING SCRIPT
============================================================
Author: Shovit Nayak
Purpose: Clean messy sales data for analysis
Skills Demonstrated: Data Cleaning, Pandas, Data Validation
"""

import pandas as pd
import numpy as np
from datetime import datetime

# ============================================================
# STEP 1: LOAD THE DATA
# ============================================================
print("=" * 60)
print("STEP 1: LOADING RAW DATA")
print("=" * 60)

# Read the CSV file
df = pd.read_csv('sales_data_raw.csv')
print(f"Loaded {len(df)} rows and {len(df.columns)} columns")
print(f"Columns: {list(df.columns)}")

# ============================================================
# STEP 2: REMOVE DUPLICATES
# ============================================================
print("\n" + "=" * 60)
print("STEP 2: REMOVING DUPLICATES")
print("=" * 60)

print(f"Before: {len(df)} rows")
df = df.drop_duplicates()
print(f"After: {len(df)} rows")
print(f"Removed {5050 - len(df)} duplicate rows")

# ============================================================
# STEP 3: HANDLE MISSING VALUES
# ============================================================
print("\n" + "=" * 60)
print("STEP 3: HANDLING MISSING VALUES")
print("=" * 60)

print("Missing values before:")
print(df.isnull().sum()[df.isnull().sum() > 0])

# Fill missing values with appropriate defaults
df['Customer_Name'] = df['Customer_Name'].fillna('Unknown Customer')
df['Payment_Method'] = df['Payment_Method'].fillna('Not Specified')
df['City'] = df['City'].fillna('Unknown')

print("\nMissing values after: 0")

# ============================================================
# STEP 4: CLEAN TEXT DATA
# ============================================================
print("\n" + "=" * 60)
print("STEP 4: CLEANING TEXT DATA")
print("=" * 60)

# List of text columns to clean
text_columns = ['Product', 'Category', 'Region', 'City', 'Payment_Method', 'Order_Status']

for col in text_columns:
    # Convert to string (handles mixed types)
    df[col] = df[col].astype(str)
    # Remove leading/trailing spaces
    df[col] = df[col].str.strip()
    # Standardize to Title Case
    df[col] = df[col].str.title()

# Fix specific typos
df['Product'] = df['Product'].str.replace('Desk Lamp', 'Desk Lamp')
df['Product'] = df['Product'].str.replace('Laptop', 'Laptop')
df['Product'] = df['Product'].str.replace('Notebook', 'Notebook')
df['Product'] = df['Product'].str.replace('Novel', 'Novel')
df['Product'] = df['Product'].str.replace('Tablet', 'Tablet')
df['Product'] = df['Product'].str.replace('Vacuum Cleaner', 'Vacuum Cleaner')

print("Text data standardized!")
print(f"Unique products: {df['Product'].nunique()}")
print(f"Unique categories: {df['Category'].nunique()}")

# ============================================================
# STEP 5: FIX DATA TYPES
# ============================================================
print("\n" + "=" * 60)
print("STEP 5: FIXING DATA TYPES")
print("=" * 60)

# Fix Discount_Percent: remove '%' and convert to number
df['Discount_Percent'] = df['Discount_Percent'].astype(str).str.replace('%', '', regex=False)
df['Discount_Percent'] = pd.to_numeric(df['Discount_Percent'], errors='coerce')
df['Discount_Percent'] = df['Discount_Percent'].fillna(0)

print(f"Discount_Percent: converted to {df['Discount_Percent'].dtype}")

# ============================================================
# STEP 6: FIX DATES
# ============================================================
print("\n" + "=" * 60)
print("STEP 6: FIXING DATES")
print("=" * 60)

# Convert to datetime (handles multiple formats automatically)
df['Order_Date'] = pd.to_datetime(df['Order_Date'], errors='coerce', dayfirst=True)

# Remove rows with invalid dates
invalid_dates = df['Order_Date'].isnull().sum()
print(f"Invalid dates found: {invalid_dates}")
df = df.dropna(subset=['Order_Date'])

# Remove future dates (data validation)
today = pd.Timestamp('2026-07-03')
future_count = len(df[df['Order_Date'] > today])
print(f"Future dates found: {future_count}")
df = df[df['Order_Date'] <= today]

print(f"Date range: {df['Order_Date'].min()} to {df['Order_Date'].max()}")

# ============================================================
# STEP 7: FIX NUMERIC OUTLIERS
# ============================================================
print("\n" + "=" * 60)
print("STEP 7: FIXING NUMERIC OUTLIERS")
print("=" * 60)

# Remove negative quantities
neg_qty = len(df[df['Quantity'] < 0])
print(f"Negative quantities: {neg_qty}")
df = df[df['Quantity'] > 0]

# Remove impossible prices
bad_prices = len(df[(df['Unit_Price'] <= 0) | (df['Unit_Price'] > 50000)])
print(f"Impossible prices: {bad_prices}")
df = df[(df['Unit_Price'] > 0) & (df['Unit_Price'] < 50000)]

# ============================================================
# STEP 8: RECALCULATE TOTAL AMOUNT
# ============================================================
print("\n" + "=" * 60)
print("STEP 8: RECALCULATING TOTAL AMOUNT")
print("=" * 60)

# Formula: Quantity × Unit_Price × (1 - Discount/100)
df['Total_Amount'] = df['Quantity'] * df['Unit_Price'] * (1 - df['Discount_Percent']/100)
df['Total_Amount'] = df['Total_Amount'].round(2)

print("Total_Amount recalculated correctly!")

# ============================================================
# STEP 9: CREATE USEFUL DERIVED COLUMNS
# ============================================================
print("\n" + "=" * 60)
print("STEP 9: CREATING DERIVED COLUMNS")
print("=" * 60)

df['Year'] = df['Order_Date'].dt.year
df['Month'] = df['Order_Date'].dt.month
df['Month_Name'] = df['Order_Date'].dt.strftime('%B')
df['Quarter'] = df['Order_Date'].dt.quarter
df['Day_of_Week'] = df['Order_Date'].dt.day_name()

print("Added: Year, Month, Month_Name, Quarter, Day_of_Week")

# ============================================================
# STEP 10: SAVE CLEANED DATA
# ============================================================
print("\n" + "=" * 60)
print("STEP 10: SAVING CLEANED DATA")
print("=" * 60)

df.to_csv('sales_data_cleaned.csv', index=False)
print(f"✅ Saved {len(df)} cleaned rows to 'sales_data_cleaned.csv'")

print("\n" + "=" * 60)
print("CLEANING COMPLETE!")
print("=" * 60)
print(f"Final dataset: {len(df)} rows × {len(df.columns)} columns")
print(f"Date range: {df['Order_Date'].min()} to {df['Order_Date'].max()}")
print(f"Total revenue: ${df['Total_Amount'].sum():,.2f}")
