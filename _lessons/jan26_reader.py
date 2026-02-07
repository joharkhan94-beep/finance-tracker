filename = "my_dataset.txt"
total_extracted = 0

print("--- Data Extraction Engine ---")

try:
    # "r" stands for READ
    with open(filename, "r") as file:
        # We loop through every line in the file
        for line in file:
            # We need to split "Rent: 800" into just the "800"
            if ":" in line:
                # split(":") gives us ["Rent", " 800"]
                parts = line.split(":")
                value = float(parts[1].strip())
                total_extracted += value
                print(f"Extracted Value: {value}")

    print("-" * 25)
    print(f"TOTAL DATA SUM: £{total_extracted:.2f}")

except FileNotFoundError:
    print("Error: Dataset file not found.")