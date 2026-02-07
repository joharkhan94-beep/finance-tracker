# 1. The Tools (definitions)
def add_tax(amount):
    return amount * 1.20 # Adds 20% VAT

# 2. The Axioms (variables)
ledger = {}
active = True

print("--- Business expense Tracker (VAT Auto-Add) ---")

# 3. The Input Engine
while active:
    name = input("Item name (or 'done'): ").strip().capitalize()
    
    if name.lower() == 'done':
        active = False
    else:
        try:
            raw_price = float(input(f"Price of {name} (excl. VAT): £"))
            ledger[name] = raw_price
        except ValueError:
            print("Please enter a valid number")

# 4. The Final Report
print("\n--- FINAL INVOICE ---")
grand_total = 0

for item, price in ledger.items():
# HERE is where we use our tool!
    price_with_tax = add_tax(price)
    grand_total += price_with_tax

    print(f"{item}: £{price: .2f} -> (w/VAT): £{price_with_tax: .2f}")

print("-" * 30)
print(f"TOTAL TO PAY: £{grand_total: .2f}")
