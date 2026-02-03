import pandas as pd
import numpy as np
import os
import random
from datetime import datetime, timedelta

os.makedirs("test_data", exist_ok=True)

# Helper to generate dates
def random_dates(start, end, n):
    start_u = start.value//10**9
    end_u = end.value//10**9
    return [datetime.fromtimestamp(random.randint(start_u, end_u)).strftime("%Y-%m-%d") for _ in range(n)]

# 1. Employees (Clean Baseline) - 50 Rows
data1 = {
    "EmployeeID": range(1001, 1051),
    "FullName": [f"Employee_{i}" for i in range(1, 51)],
    "Department": [random.choice(["HR", "Engineering", "Sales", "Marketing"]) for _ in range(50)],
    "Salary": [random.randint(40000, 120000) for _ in range(50)],
    "Status": ["Active"] * 50
}
pd.DataFrame(data1).to_csv("test_data/1_Employees.csv", index=False)

# 2. Sales Data (Excel, Missing Values) - 50 Rows
# Intentionally removing some values to test "Handle Missing"
products = ["Widget A", "Widget B", "Gadget X", "Gadget Y", "Tool Z"]
rows = []
for i in range(50):
    rows.append({
        "TransactionID": f"TXN_{i+1}",
        "Product": random.choice(products),
        "Quantity": random.choice([1, 2, 5, 10, np.nan]) if i % 10 != 0 else np.nan, # 10% missing
        "Price": random.uniform(10.0, 500.0) if i % 15 != 0 else np.nan, # ~7% missing
        "Date": (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
    })
pd.DataFrame(rows).to_excel("test_data/2_Sales_Missing_Values.xlsx", index=False)

# 3. Inventory (Duplicates & Messy Text) - 60 Rows (to allow for removal)
# Tests "Remove Duplicates" and "Standardize Data"
items = ["  Laptop ", "laptop", "LAPTOP  ", " Mouse", "MOUSE", "KeyBoard", "monitor "]
raw_data = []
for i in range(50):
    raw_data.append([random.choice(items), random.randint(1, 100), "Warehouse A"])
# Add 10 duplicates
for _ in range(10):
    raw_data.append(raw_data[random.randint(0, 49)])

pd.DataFrame(raw_data, columns=["Item_Name", "Stock_Count", "Location"]).to_csv("test_data/3_Inventory_Messy_Duplicates.csv", index=False)

# 4. Merge Data A (Main) - 50 Rows
df_a = pd.DataFrame({
    "UserID": range(1, 51),
    "Username": [f"User_{i}" for i in range(1, 51)],
    "Email": [f"user{i}@example.com" for i in range(1, 51)]
})
df_a.to_csv("test_data/4_Merge_Users_Base.csv", index=False)

# 5. Merge Data B (Extensions) - 50 Rows (Same IDs)
# Tests the "Join" logic we implemented
df_b = pd.DataFrame({
    "UserID": range(1, 51),
    "LoginCount": [random.randint(1, 500) for _ in range(50)],
    "LastLogin": random_dates(pd.to_datetime('2023-01-01'), pd.to_datetime('2023-12-31'), 50)
})
df_b.to_csv("test_data/5_Merge_Users_Activity.csv", index=False)

# 6. Merge Data C (Append with Overlap) - IDs 30 to 80
# Base has 1-50. This has 30-80. Overlap is 30-50.
# Merging 4 and 6 should result in 80 unique rows (1-80).
df_c = pd.DataFrame({
    "UserID": range(30, 81),
    "Username": [f"User_{i}" for i in range(30, 81)],
    "Email": [f"user{i}@example.com" for i in range(30, 81)]
})
df_c.to_csv("test_data/6_Merge_Users_Append.csv", index=False)

print("Generated 6 cleaned datasets (including new overlap test) in test_data/.")
