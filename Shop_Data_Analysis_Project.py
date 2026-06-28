import numpy as np
import pandas as pd
import mysql.connector
import matplotlib.pyplot as plt

# =========================
# 1. DATABASE CONNECTION
# =========================
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="yuvr@j123",
    database="shop"
)

# =========================
# 2. LOAD DATA (SQL JOIN)
# =========================
query = """
SELECT 
    o.order_id,
    c.name,
    c.city,
    c.gender,
    o.product,
    o.category,
    o.quantity,
    o.price,
    o.order_date
FROM orders o
JOIN customer c
ON o.customer_id = c.customer_id
"""

df = pd.read_sql(query, conn)
print("\n--- DATA PREVIEW ---")
print(df.head())

# =========================
# 3. DATA CLEANING
# =========================
print("\n--- MISSING VALUES ---")
print(df.isnull().sum())

print("\n--- DUPLICATE VALUES ---")
print(df.duplicated().sum())

df = df.drop_duplicates()

# =========================
# 4. FEATURE ENGINEERING
# =========================
df["total_amount"] = df["quantity"] * df["price"]

# =========================
# 5. NUMPY ANALYSIS
# =========================
print("\n--- TOTAL REVENUE ---")
print(np.sum(df["total_amount"]))

print("\n--- AVERAGE ORDER VALUE ---")
print(np.mean(df["total_amount"]))

print("\n--- MAX ORDER VALUE ---")
print(np.max(df["total_amount"]))

# =========================
# 6. BUSINESS ANALYSIS
# =========================
print("\n--- CITY WISE REVENUE ---")
city_wise = df.groupby("city")["total_amount"].sum()
print(city_wise)

print("\n--- PRODUCT WISE SALES ---")
product_wise = df.groupby("product")["total_amount"].sum()
print(product_wise)

print("\n--- CATEGORY WISE SALES ---")
category_wise = df.groupby("category")["total_amount"].sum()
print(category_wise)

print("\n--- TOP 3 CUSTOMERS ---")
top_customers = df.groupby("name")["total_amount"].sum().sort_values(ascending=False).head(3)
print(top_customers)

print("\n--- GENDER WISE SPENDING ---")
gender_wise = df.groupby("gender")["total_amount"].sum()
print(gender_wise)

# =========================
# 7. VISUALIZATION
# =========================

# CITY WISE BAR CHART
plt.figure()
plt.bar(city_wise.index, city_wise.values)
plt.title("City Wise Revenue")
plt.xlabel("City")
plt.ylabel("Revenue")
plt.xticks(rotation=45)
plt.show()

# CATEGORY PIE CHART
plt.figure()
plt.pie(category_wise.values, labels=category_wise.index, autopct="%1.1f%%")
plt.title("Category Wise Sales Distribution")
plt.show()

# TOP CUSTOMERS BAR CHART
plt.figure()
plt.bar(top_customers.index, top_customers.values)
plt.title("Top 3 Customers")
plt.xlabel("Customer Name")
plt.ylabel("Total Spending")
plt.xticks(rotation=45)
plt.show()