# 1. Axioms (Variables)
running_total = 0
all_expenses = [] # This is our memory bank
active = True

print("--- Automated Expense Tracker ---")
print("Type 'done' when you are finished.")

# 2. The Loop (The Sigma Engine)
while active:
# .strip() removes accidental spaces, .lower() ignores capital letters
    user_input = input("Enter expense amount or 'done': ").strip().lower()

# --- EVERYTHING BELOW MUST BE INDENTIFIED ONE TAB ---
    if user_input == 'done':
        active = False # This breaks the loop.
    else:
    # Convert the text input to a number and add to the total
    # We wrap this in a "try" block, just in case you type a typo
        try:
            amount = float(user_input)
            all_expenses.append(amount) # Saves the number to the list
            running_total = sum(all_expenses) # Recalculate total from the list
            print(f"Items recorded: {len(all_expenses)}")
        except ValueError:
            print("Logic Error: Please enter a number or the word 'done'.")

# 3. Final Output
print(f"--- Final Summary ---")
print(f"Individual items: {all_expenses}")
print(f"total spent today: £{running_total}")

# The Equation: Total / Count
average = sum(all_expenses) / len(all_expenses)
# The second number (2) tells python how many decimal places to keep
print(f"Average expense: £{round(average, 2)}")
