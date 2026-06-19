import pandas as pd
import numpy as np

# 1. Create the Raw "Chaotic" Data
raw_data = {
    "Employee ID": [101, 102, 103, 101, 104, 105],
    "Full Name": ["   john smith", "jane DOE", "ROBERT JOHNSON   ", "   john smith", "Emily brown", "MICHAEL GREEN"],
    "Department": ["Sales", "Marketing", np.nan, "Sales", "HR", "IT"],
    "Salary": [50000, 62000, 45000, 50000, 55000, 70000],
    "Bonus %": [0.10, 0.12, 0.05, 0.10, 0.00, 0.15],
    "Bonus Amount": ["5000", "7440", "2250", "5000", "#DIV/0!", "10500"]
}

df = pd.DataFrame(raw_data)
print("❌ Original Messy Data:")
print(df)
print("-" * 50)

# --- PIPELINE START ---

# Step 1: Remove Duplicate Entries (Video Chapter: Removing Duplicates)
df = df.drop_duplicates()

# Step 2: Trim Extra Spaces & Fix Text Casing (Video Chapters: Trim, Proper, Lower)
df["Full Name"] = df["Full Name"].str.strip().str.title()

# Step 3: Split Names into First and Last (Video Chapter: Text to Columns)
df[['First Name', 'Last Name']] = df['Full Name'].str.split(' ', n=1, expand=True)

# Step 4: Fill Empty Cells / Missing Values (Video Chapter: Filling Empty Cells)
df["Department"] = df["Department"].fillna("General")

# Step 5: Clean Division/Formula Errors (Video Chapter: IFERROR)
# Replace error strings with 0
df["Bonus Amount"] = df["Bonus Amount"].replace("#DIV/0!", 0).astype(float)

# Rearrange columns cleanly
df = df[["Employee ID", "First Name", "Last Name", "Department", "Salary", "Bonus %", "Bonus Amount"]]

# --- PIPELINE END ---

print("\n✅ Cleaned & Structured Data:")
print(df)

# Save to CSV
df.to_csv("cleaned_employee_data.csv", index=False)
