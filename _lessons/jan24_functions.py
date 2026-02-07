# 1. The Function Factory (the Axioms) ---
def add_tax(price):
    """
    
    Takes a raw price and returns the price with 20% VAT added
    """
    tax_amount = price * 0.20
    final_price = price + tax_amount
    return final_price

# 2. The Main Program ---
print("--- VAT Calculator ---")

# Let's test our new tool manually first
raw_cost = float(input("Enter the orice of the item: £"))

# We "call" the function here.
# We pass 'raw_cost' into the machine, and catch the result in 'price_with_tax'
price_with_tax = add_tax(raw_cost)

print(f"Original: £{raw_cost: .2f}")
print(f"With 20% VAT: £{price_with_tax: .2f}")
