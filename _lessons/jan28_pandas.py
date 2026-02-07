# 1. Import the tool
import pandas as pd  # "pd" is the nickname pros use

print("--- AI Data Analysis ---")

# 2. Load the data (The Magic Line)
# This replaces ALL the 'with open...' code you wrote before
df = pd.read_csv("household_finances.csv")

# 3. View the data
print("\nHere is your dataset:")
print(df)

# 4. Instant Math
print("\n--- Quick Stats ---")
print(f"Total Cost: £{df['Cost'].sum()}")
print(f"Average Cost: £{df['Cost'].mean():.2f}")