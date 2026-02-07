import pandas as pd
import matplotlib.pyplot as plt # The standard plotting tool

print("--- AI Visualizer ---")

# 1. Load the Data (Using your Pandas skill!)
df = pd.read_csv("household_finances.csv")

# 2. Setup the Graph
# We tell it: x-axis = "Item", y-axis = "Cost"
plt.figure(figsize=(10, 6)) # Make the window 10x6 inches
plt.bar(df["Item"], df["Cost"], color='salmon')

# 3. Add Labels (Always label your axes!)
plt.title("My Financial Empire")
plt.xlabel("Expense Item")
plt.ylabel("Cost (£)")

# 4. Reveal the Graph
print("Generating graph...")
plt.show()