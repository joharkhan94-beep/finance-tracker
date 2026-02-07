# 1. Axioms (Variables)
ledger = {} # An empty dictionary to store our "Receipt"
active = True

print(" --- Professional Receipt Builder ---")

# 2. The Interaction Loop
while active:
    name = input("what did you buy? (or type 'done'): ").strip().capitalize()
    if name.lower() == 'done':
        active = False
    else:
        try:
            amount = float(input(f"How much was {name}? £"))
# This line 'maps' the amount to the name in pur ledger            
            ledger[name] = amount
        except ValueError:
            print("Invalid price. Please enter a number.")

# 3. The Output (The Formatted Receipt)
print('\n--- Final Statement ---')
for item, price in ledger.items():
    print(f"- {item}: £{price:.2f}")

total = sum(ledger.values())
print(f"TOTAL SPENT: £{total:.2f}")
