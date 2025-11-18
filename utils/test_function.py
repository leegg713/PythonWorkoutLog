
#!/usr/bin/env python3
"""
Simple function tester - Just import and call any function from Main.py
"""

#from main import * #Imports all functions in main
from webApp import * #Imports all functions in webapp.py
# Example usage:
# test_function.py

# Uncomment the function you want to test:

# get_valid_number_input("Enter a number: ", "Test")
# clear_last_entry()
# add_exercise()
# average_lift()
# wilks()
# dots()
# one_rep_max()
# calculator()
# plot_exercise_data()
#plate_calculator()
#exercise_frequency()
#mark_pr()

#print("Edit this file and uncomment the function you want to test, then run: python test_function.py")
#convertCSVToDB()

### FUNCTION TO RE CREATE CSV WITH A COLUMN ID ###
'''
# Load CSV from parent directory
df = pd.read_csv("../WorkoutLog.csv")

# Add ID column starting from 1 at the end
df["id"] = range(1, len(df) + 1)

# Save back to CSV
df.to_csv("data_with_id.csv", index=False)
'''

'''
# Step 1: Load CSV (from parent directory)
df = pd.read_csv("../WorkoutLog.csv")

# Step 2: Add ID column at the end
df["id"] = range(1, len(df) + 1)

# Step 3: Connect to SQLite (creates db if not exists)
conn = sqlite3.connect("WorkoutLog.db")

# Step 4: Write DataFrame to SQLite
# 'my_table' will be created automatically with columns in the same order
df.to_sql("my_table", conn, if_exists="replace", index=False)

# Step 5: Close connection
conn.close()
'''