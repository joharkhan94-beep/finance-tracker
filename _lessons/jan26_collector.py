# 1. The Setup
filename = "my_dataset.txt"

print("--- AI Data Collector ---")
print(f"Data will be saved to: {filename}")

# 2. the Input Loop
while True:
    data_input = input("Enter a data point (or 'done'): ").strip()

    if data_input.lower() == 'done':
        break # Breaks the loop immediately

# 3. The "Write" Operation (The Pipeline)
# "a" stands for APPEND (add to the end, dont delete old data)
    with open(filename, "a") as file:
        file.write(f"{data_input}\n")
# \n means "New Line" - crucial for seperating data points!
    
    print(f"--> Saved '{data_input}' to database.")

print("Session closed. Data preserved.")
