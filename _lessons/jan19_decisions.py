# Lesson 2 - 19/01/2026

# The Decision Gate (19/01/2026)

# if final_balance < 0:
#     print("WARNING: Logic indicates a deficit.")
#    print(f"you are over by: {abs(final_balance)}")
#else:
#    print("SUCCESS: logic indicates a surplus.")
#    print(f"You have a cushion of: {final_balance}")

# refining the above and combing lesson 1 & 2
starting_balance = 500
paycheck = 200
cost = 45.50
quantity = 5
final_balance = starting_balance + paycheck - (cost*quantity)

# refined Decision Gate - 
if final_balance < 0:
    debt = abs(final_balance)
    print(f"WARNING: you have a deficit of £{debt}")
else:
    print(f"SUCCESS: you have a cushion of £{final_balance}")    
    