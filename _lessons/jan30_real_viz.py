import pandas as pd
import matplotlib.pyplot as plt

print("--- Real Finance Analyzer ---")

# 1. Load the file
df = pd.read_csv("real_finance.csv")

# 2. FILTER: We only want to see where money is LEAVING
# We create a new table called 'expenses' containing only Outgoing rows
expenses = df[df["Type"] == "Outgoing"]

# 3. SORT: Let's put the most expensive items first
# ascending=False means "Big numbers at the top"
expenses = expenses.sort_values(by="Amount (£)", ascending=False)

# 4. PLOT
plt.figure(figsize=(12, 8)) # A big window for big data
plt.bar(expenses["Description"], expenses["Amount (£)"], color="salmon")

# 5. Make it readable
plt.title("My Household Expenses (Real Data)")
plt.xlabel("Expense Item")
plt.ylabel("Cost (£)")
plt.xticks(rotation=45, ha='right') # Rotate labels so they don't overlap!
plt.tight_layout() # Auto-adjust margins so labels aren't cut off

print("Generating report...")
plt.show()