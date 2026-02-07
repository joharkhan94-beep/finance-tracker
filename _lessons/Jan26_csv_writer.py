filename = "household_finances.csv"

print("--- Permanent Expense Logger (CSV) ---")
print(f"Saving data to: {filename}")

# 1. Check if file exists, if not, create headers (The 'Schema')
try:
    with open(filename, "x") as file: # "x" creates a file only if it doesn't exist
        file.write("Item,Cost\n") # The Column Headers
except FileExistsError:
    pass # File already exists, so we don't need to do anything

# 2. The Data Entry Loop
while True:
    name = input("Expense Name (or 'done'): ").strip().title()
    if name.lower() == 'done':
        break
    
    try:
        cost = float(input(f"Cost of {name}: £"))
        
        # 3. Append to CSV
        with open(filename, "a") as file:
            file.write(f"{name},{cost}\n")
            
        print(f"--> Logged: {name} | £{cost}")
        
    except ValueError:
        print("Error: Please enter a numeric cost.")

print("Session saved. You can now open 'household_finances.csv' in Excel.")