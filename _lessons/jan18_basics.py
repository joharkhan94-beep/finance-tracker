
# Lesson 1 - 18/01/2026

# Connect Your Terminal to VS Code
# This is a "pro move" that lets you open projects instantly.
# Open VS Code from your Applications folder.
# Press Cmd + Shift + P to open the "Command Palette."
# Type "shell command" and select: Shell Command: Install 'code' command in PATH.
# Restart your Terminal.
# Now, go back to terminal and type: cd my-finance-app code.
# This will launch VS code directly into your priject folder.

# 1. The Variables.
starting_balance = 500 
paycheck = 200
item_name = "Groceries"
cost = 45.50
quantity = 5

# 2. The equation
# Total = Balance + Income - Expense
final_balance = starting_balance + paycheck - (cost*quantity)

# 3. is the balance less than zero (True or False)
is_overdrawn = final_balance < 0

# 4. The Output 19/01/2026
print(f"I started with {starting_balance}, but now i have {final_balance}")
print(f"balance: {final_balance}")
print(f"Am I overdrawn? {is_overdrawn}")