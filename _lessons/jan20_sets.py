
# using summation operator - 

# starting_balance = 500
# paycheck = 200
# expenses = [45.50, 80.00, 15.75, 200.00, 500.00]
# final_balance = starting_balance + paycheck - sum(expenses)
# if final_balance < 0:
#     debt = abs(final_balance)
#     print(f"WARNING: you hava a deficit of £{debt}")
# else:
#     print(f"SUCCESS: you have a cushion of £{final_balance}")

# Lesson 3 - 20/01/2026

# 1. The Set of Expenses (Vector)
expenses = [45.50, 80.00, 15.75, 200.00, 500.00]
starting_balance = 500

# 2. Interactive input (Talking to the User)
# We convert the input from Text to Float (Decimal)
paycheck = float(input("Enter your paycheck amount: "))

# 3. The Calculation (Summation)
total_expenses = sum(expenses)
final_balance = starting_balance + paycheck - total_expenses

# 4. The Decision Gate
if final_balance < 0:
    debt = abs(final_balance)
    print(f"WARNING: Logic indicates a deficit of £{debt}")
else:
    print(f"SUCCESS: Logic indicates a surplus of £{final_balance}")