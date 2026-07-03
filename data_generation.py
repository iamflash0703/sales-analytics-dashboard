"""
============================================================
PROJECT 1: SALES DASHBOARD - DATA GENERATION SCRIPT
============================================================
Author: Shovit Nayak
Purpose: Generate a realistic but messy sales dataset for practice
Skills Demonstrated: Data Simulation, Python, Pandas

This script creates a 5,000+ record sales dataset with intentional
messiness (duplicates, missing values, typos, wrong formats) so that
learners can practice real-world data cleaning.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# ============================================================
# CONFIGURATION
# ============================================================
np.random.seed(42)      # For reproducibility (same data every time)
random.seed(42)

N_RECORDS = 5000        # Number of sales records to generate

# ============================================================
# PRODUCT CATALOG
# ============================================================
products = {
    'Laptop':        {'category': 'Electronics', 'base_price': 850},
    'Smartphone':    {'category': 'Electronics', 'base_price': 650},
    'Headphones':    {'category': 'Electronics', 'base_price': 120},
    'Tablet':        {'category': 'Electronics', 'base_price': 400},
    'T-Shirt':       {'category': 'Clothing',    'base_price': 25},
    'Jeans':         {'category': 'Clothing',    'base_price': 60},
    'Jacket':        {'category': 'Clothing',    'base_price': 120},
    'Sneakers':      {'category': 'Clothing',    'base_price': 90},
    'Coffee Maker':  {'category': 'Home',        'base_price': 80},
    'Blender':       {'category': 'Home',        'base_price': 55},
    'Vacuum Cleaner':{'category': 'Home',        'base_price': 200},
    'Desk Lamp':     {'category': 'Home',        'base_price': 35},
    'Novel':         {'category': 'Books',       'base_price': 15},
    'Textbook':      {'category': 'Books',       'base_price': 80},
    'Notebook':      {'category': 'Books',       'base_price': 10},
}

# ============================================================
# REGIONS AND CITIES
# ============================================================
regions = {
    'North': ['Delhi', 'Chandigarh', 'Jaipur'],
    'South': ['Bangalore', 'Chennai', 'Hyderabad'],
    'East':  ['Kolkata', 'Bhubaneswar', 'Guwahati'],
    'West':  ['Mumbai', 'Pune', 'Ahmedabad']
}

# ============================================================
# CUSTOMER NAMES (Indian names for realism)
# ============================================================
first_names = [
    'Aarav', 'Vivaan', 'Aditya', 'Vihaan', 'Arjun', 'Sai', 'Arnav', 'Ayaan',
    'Krishna', 'Ishaan', 'Aadhya', 'Ananya', 'Diya', 'Saanvi', 'Aaradhya',
    'Navya', 'Anvi', 'Pari', 'Kavya', 'Sara', 'Rahul', 'Priya', 'Amit',
    'Sneha', 'Rajesh', 'Pooja', 'Vikram', 'Neha', 'Suresh', 'Kavita',
    'Shovit', 'Ramesh', 'Geeta', 'Manoj', 'Sunita', 'Deepak', 'Anita',
    'Sanjay', 'Rekha', 'Vinod'
]

last_names = [
    'Sharma', 'Kumar', 'Singh', 'Patel', 'Gupta', 'Reddy', 'Nair', 'Das',
    'Bose', 'Mehta', 'Nayak', 'Iyer', 'Joshi', 'Malhotra', 'Agarwal',
    'Verma', 'Yadav', 'Rao', 'Mishra', 'Pandey'
]

payment_methods = ['Credit Card', 'Debit Card', 'UPI', 'Cash on Delivery', 'Net Banking']

# ============================================================
# STEP 1: GENERATE CLEAN DATA
# ============================================================
print("=" * 60)
print("STEP 1: GENERATING CLEAN DATA")
print("=" * 60)

start_date = datetime(2024, 1, 1)
end_date = datetime(2026, 6, 30)
date_range = (end_date - start_date).days

data = []

for i in range(N_RECORDS):
    # Generate random date
    random_days = random.randint(0, date_range)
    order_date = start_date + timedelta(days=random_days)

    # Pick product
    product_name = random.choice(list(products.keys()))
    product_info = products[product_name]

    # Add price variation (+-20%)
    price_variation = random.uniform(0.8, 1.2)
    unit_price = round(product_info['base_price'] * price_variation, 2)

    # Quantity based on price (cheaper items = more quantity)
    if unit_price < 50:
        quantity = random.randint(1, 5)
    elif unit_price < 200:
        quantity = random.randint(1, 3)
    else:
        quantity = random.randint(1, 2)

    # Calculate total
    total_amount = round(unit_price * quantity, 2)

    # Region and city
    region = random.choice(list(regions.keys()))
    city = random.choice(regions[region])

    # Customer
    customer_name = f"{random.choice(first_names)} {random.choice(last_names)}"

    # Payment method
    payment = random.choice(payment_methods)

    # Order status (mostly completed)
    status = random.choices(
        ['Completed', 'Cancelled', 'Returned', 'Pending'],
        weights=[0.85, 0.08, 0.05, 0.02]
    )[0]

    # Discount (0-30%)
    discount = random.choice([0, 0, 0, 5, 10, 15, 20, 25, 30])

    data.append({
        'Order_ID': f"ORD-{2024 + random_days // 365}-{random.randint(10000, 99999)}",
        'Order_Date': order_date.strftime('%Y-%m-%d'),
        'Customer_Name': customer_name,
        'Product': product_name,
        'Category': product_info['category'],
        'Quantity': quantity,
        'Unit_Price': unit_price,
        'Discount_Percent': discount,
        'Total_Amount': total_amount,
        'Payment_Method': payment,
        'Region': region,
        'City': city,
        'Order_Status': status
    })

df = pd.DataFrame(data)
print(f"Generated {len(df)} clean records")

# ============================================================
# STEP 2: INTRODUCE MESSINESS (Real-World Problems)
# ============================================================
print("\n" + "=" * 60)
print("STEP 2: INTRODUCING REAL-WORLD MESSINESS")
print("=" * 60)

# 1. Missing values (5% of data)
print("1. Adding missing values...")
missing_count = int(len(df) * 0.05)
missing_indices = random.sample(range(len(df)), missing_count)
for idx in missing_indices:
    col = random.choice(['Customer_Name', 'Payment_Method', 'City'])
    df.loc[idx, col] = np.nan
print(f"   Added {missing_count} missing values")

# 2. Duplicate rows
print("2. Adding duplicate rows...")
duplicate_rows = df.sample(n=50, random_state=42)
df = pd.concat([df, duplicate_rows], ignore_index=True)
print(f"   Added 50 duplicates (total: {len(df)})")

# 3. Wrong date formats
print("3. Adding wrong date formats...")
wrong_date_indices = random.sample(range(len(df)), 30)
for idx in wrong_date_indices:
    df.loc[idx, 'Order_Date'] = random.choice([
        '16-10-2025', 'Oct 16, 2025', '2025/10/16', '16th Oct 2025'
    ])
print(f"   Corrupted {len(wrong_date_indices)} date formats")

# 4. Negative quantities
print("4. Adding negative quantities...")
neg_indices = random.sample(range(len(df)), 15)
for idx in neg_indices:
    df.loc[idx, 'Quantity'] = -random.randint(1, 3)
print(f"   Added {len(neg_indices)} negative quantities")

# 5. Price outliers
print("5. Adding price outliers...")
outlier_indices = random.sample(range(len(df)), 10)
for idx in outlier_indices:
    df.loc[idx, 'Unit_Price'] = random.choice([99999.99, 0.01, -500])
print(f"   Added {len(outlier_indices)} price outliers")

# 6. Text inconsistencies
print("6. Adding text inconsistencies...")
text_indices = random.sample(range(len(df)), 40)
for idx in text_indices:
    col = random.choice(['Product', 'Category', 'Region'])
    val = str(df.loc[idx, col])
    df.loc[idx, col] = random.choice([
        val.upper(), val.lower(), val + ' ', ' ' + val,
        val.replace('e', '3'), val.replace('a', '@')
    ])
print(f"   Added {len(text_indices)} text inconsistencies")

# 7. Wrong data types (numbers as text)
print("7. Adding wrong data types...")
type_indices = random.sample(range(len(df)), 20)
for idx in type_indices:
    df.loc[idx, 'Discount_Percent'] = str(df.loc[idx, 'Discount_Percent']) + '%'
print(f"   Stored {len(type_indices)} discounts as text with '%'")

# 8. Future dates
print("8. Adding impossible future dates...")
future_indices = random.sample(range(len(df)), 5)
for idx in future_indices:
    df.loc[idx, 'Order_Date'] = '2027-12-25'
print(f"   Added {len(future_indices)} future dates")

# ============================================================
# STEP 3: SAVE THE MESSY DATA
# ============================================================
print("\n" + "=" * 60)
print("STEP 3: SAVING MESSY DATASET")
print("=" * 60)

df.to_csv('sales_data_raw.csv', index=False)
print(f"Saved {len(df)} messy records to 'sales_data_raw.csv'")
print(f"Missing values: {df.isnull().sum().sum()}")
print(f"Duplicate rows: {df.duplicated().sum()}")

print("\n" + "=" * 60)
print("DATA GENERATION COMPLETE!")
print("=" * 60)
print("Now run: python data_cleaning.py")
