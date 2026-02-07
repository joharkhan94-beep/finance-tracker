# 1. The Dictionary (labeled Set)
# Format is "Name" : Value
expenses = {"Rent": 800, "Groceries": 45.50, "Internet": 15.75, "Coffee": 5.50}

# 2. Accessing Specific Date
#Instead of sum(), we can grab one specific item by its name
internet_cost = expenses["Internet"]
coffee_cost = expenses["Coffee"]

# 3. Calculation
starting_balance = 1000
final_balance = starting_balance - internet_cost - coffee_cost
print(f"Your coffee cost is £{coffee_cost}")
print(f"Your internet cost is £{internet_cost}")
print(f"Balance after internet: £{final_balance}")
