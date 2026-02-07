import os
import pandas as pd
import matplotlib.pyplot as plt

filename = "my_tracker.csv"

# --- CONFIGURATION ---
# Key = Category Name, Value = Max Limit (£)
BUDGETS = {
    "Food": 50,
    "Travel": 30,
    "Bills": 200
    }

# --- SYSTEM CHECK ---
# If the file doesn't exist, create it with our new "Schema"
if not os.path.exists(filename):
    with open(filename, "w") as file:
        file.write("Date,Category,Item,Cost\n") # The Headers
    print("System: New database created.")
else:
    print("System: Database found.")

# --- THE MAIN LOOP ---
while True:
    print("\n--- FINANCE TRACKER 2.0 ---")
    print("1. Add a new expense")
    print("2. View all expenses")
    print("3. Visualize Spending (NEW!)")  # <--- New Option
    print("4. Exit")
    
    choice = input("Select an option (1-4): ")
    
    if choice == "1":
        print("\n--- NEW EXPENSE ---")
        date = input("Date (DD/MM/YYYY): ")
        
        # Show user the valid categories
        print(f"Categories: {list(BUDGETS.keys())}") 
        category = input("Category: ")
        item = input("Item Name: ")
        
        try:
            cost = float(input("Cost: £"))
            
            # --- BUDGET CHECKER START ---
            # 1. Calculate how much we have ALREADY spent in this category
            current_total = 0
            if os.path.exists(filename):
                df = pd.read_csv(filename)
                if not df.empty:
                    # Filter for just this category
                    category_data = df[df["Category"] == category]
                    current_total = category_data["Cost"].sum()
            
            # 2. Check if this new cost pushes us over the edge
            limit = BUDGETS.get(category, 999999) # Default to huge limit if category not listed
            
            if current_total + cost > limit:
                print(f"\n⚠️  WARNING: OVER BUDGET! ⚠️")
                print(f"Limit: £{limit}")
                print(f"Current: £{current_total}")
                print(f"New Total would be: £{current_total + cost}")
                confirm = input("Do you still want to save this? (y/n): ")
                if confirm.lower() != "y":
                    print("Cancelled.")
                    continue # Skip the saving part
            # --- BUDGET CHECKER END ---

            # Save to CSV if we passed the check
            with open(filename, "a") as file:
                file.write(f"{date},{category},{item},{cost}\n")
            print(f"SUCCESS: Saved {item} for £{cost}!")
            
        except ValueError:
            print("ERROR: Cost must be a number.")

    elif choice == "2":
        print("\n--- YOUR SPENDING ---")
        try:
            df = pd.read_csv(filename)
            if df.empty:
                 print("Result: File is empty.")
            else:
                 print(df)
                 print(f"\nTotal Spent: £{df['Cost'].sum()}")
            input("\nPress Enter to return to menu...")
        except Exception:
            print("No data found.")

    elif choice == "3":
        print("\n--- GENERATING GRAPH ---")
        try:
            # 1. Load Data
            df = pd.read_csv(filename)
            
            # 2. GROUP BY CATEGORY (The Smart Part)
            # This combines all "Food" rows into one total, all "Bills" into another
            data = df.groupby("Category")["Cost"].sum()
            
            # 3. Plot it
            plt.figure(figsize=(10, 6))
            plt.bar(data.index, data.values, color="mediumpurple")
            
            plt.title("Expenses by Category")
            plt.ylabel("Total Cost (£)")
            plt.tight_layout()
            
            print("Graph opened in new window...")
            plt.show() # This pauses the app until you close the graph
            
        except Exception as e:
            print(f"Could not graph data: {e}")

    elif choice == "4":
        print("Saving and Exiting...")
        break
        
    else:
        print("Invalid choice. Try again.")
