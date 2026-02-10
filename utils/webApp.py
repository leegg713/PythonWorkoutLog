### NEXT STEPS FOR PROJECT ### 

''' 
NEXT TO DO LIST

Step 1 — Clean up DB column types
Time: 30–60 min
Reason: Check column types, update table if needed, test reading data. -- COMPLETED the DB works as expected

Step 2 — Add date filters to graphs
Time: 1–2 hours
Reason: Add date inputs, update query to filter by dates, test plots. -- COMPLETED

Step 4 — Additional visualizations
Time: 2–4 hours
Reason: Volume, intensity, PR charts, testing plots, small tweaks for readability.- COMPLETED
##############################################################################################
Step 5 — Edit / Delete entries WORK ON THIS NEXT
-- Have the delete and edit buttons working
Now just need a table to view the workouts
view_table function will need to be created and then loaded into the add.html
Time: 2–3 hours
Reason: Create table view of workouts, add buttons, implement UPDATE and DELETE.
##############################################################################################

Step 8 — Export / Share
Time: 1–2 hours
Reason: Export CSV/PDF and optionally email graphs.

Step 6 — Multi-user support
Time: 1–2 days
Reason: Add users table, Flask-Login setup, link workouts to users, test authentication.

Step 10 — Deployment
Time: 1–2 hours for Render/Heroku simple deploy
Reason: Small Flask app with SQLite; longer if multi-user and HTTPS setup.
'''
####################### IMPORT STATEMENTS #######################

import os
import csv
import time
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
from io import BytesIO
import sqlite3

### GLOBAL VARIABLES ###
CSV_FILE = 'WorkoutLog.csv' #Global Variable
db_file = "WorkoutLog.db"
table_name = "Workout"

# Utility function to get the last entered date from CSV or DB
def get_last_date():
    # Try to get last date from CSV first
    if os.path.exists(CSV_FILE):
        try:
            with open(CSV_FILE, "r") as file:
                lines = list(csv.reader(file))
                if lines and len(lines[-1]) > 0:
                    last_date = lines[-1][-1].strip()
                    if last_date:
                        # Normalize to ISO (YYYY-MM-DD) for HTML <input type="date">
                        try:
                            # Try common formats: MM/DD/YY, MM/DD/YYYY, YYYY-MM-DD
                            for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%m/%d/%y"):
                                try:
                                    dt = datetime.datetime.strptime(last_date, fmt)
                                    return dt.strftime("%Y-%m-%d")
                                except Exception:
                                    continue
                        except Exception:
                            return ""
        except Exception:
            pass
    # If not found in CSV, try DB
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(f"SELECT date FROM {table_name} ORDER BY ROWID DESC LIMIT 1")
        row = cur.fetchone()
        conn.close()
        if row and row[0]:
            last_date = row[0]
            try:
                for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%m/%d/%y"):
                    try:
                        dt = datetime.datetime.strptime(last_date, fmt)
                        return dt.strftime("%Y-%m-%d")
                    except Exception:
                        continue
            except Exception:
                return ""
    except Exception:
        pass
    return ""
#### CONVERT CSV TO SQLITE DB #####
### ONE TIME RUN ONLY IF HAVE FRESH CSV ####
# NEED TO ADD THIS TO APP??? OR JUST LEAVE IT SINCE MULTI USERS WONT NEED IT ###

def convertCSVToDB():
    # ---- Settings ----
    CSV_FILE = "/workspaces/PythonWorkoutLog/WorkoutLog.csv"       # your CSV file
    db_file = "WorkoutLog.db"    # SQLite database file
    table_name = "Workout"       # name of the table to create

# ---- Load CSV into pandas ----
    df = pd.read_csv(CSV_FILE)

# ---- Connect to SQLite ----
    conn = sqlite3.connect(db_file)

# ---- Write dataframe to SQL ----
    df.to_sql(table_name, conn, if_exists="replace", index=False)

# ---- Close connection ----
    conn.close()

    print(f"CSV {CSV_FILE} successfully imported into {db_file} as table '{table_name}'")

####### CONNECT TO DB FUNCTION TO USE IN OTHER FUNCTIONS #######

def get_db_connection():
    conn = sqlite3.connect(db_file)
    conn.row_factory = sqlite3.Row  # optional
    return conn

 ##### CALCULATOR PAGE SECTION FOR DIFFERENT CALCULATIONS #####   


###### LIFT AVERAGE FLASK VERSION #########

def average_lift(exercise_to_avg):
    exercise_to_avg = exercise_to_avg.strip().replace(" ", "").lower()  # normalize input to lower to check the CSV
    #Initialize variables to be 0 
    total_weight = 0
    total_reps = 0

    #### CSV AVERAGE SECTION ####
    '''
    # Read the CSV file and calculate the total weight for the selected exercise
    with open(CSV_FILE, mode='r') as file:
        reader = csv.reader(file)

        # Skip the header row if there is one
        next(reader, None)  # Skip the header row 
        #Reads the file to get the total weight done and reps done
        for row in reader:
            #Below line Unpacks the row
            exercise, sets, reps, weight, *extra_columns = row  #Extra_columns needed otherwise it won't work due to an error saying its missing a row (Date)
            if exercise.lower() == exercise_to_avg:  #Check to see if user input matches an exercise in the CSV -- Sets to lower to match exercise_to_avg form submission
                total_weight += float(weight) * int(reps) * int(sets)  # Gets weight in lbs
                total_reps += int(reps) * int(sets)# Add the total number of reps (sets * reps) to total_reps
    
    # Calculate and display/returns the average
    if total_reps > 0:
        avg_weight_per_rep = total_weight / total_reps
        return {
        "exercise": exercise_to_avg,
        "average": round(avg_weight_per_rep, 2),
        "total_reps": total_reps
        }
    else:
        return {"error": f"No entries found for {exercise_to_avg}"}
        '''
    ##### DB READ AVERAGE SECTION ######
    conn = get_db_connection() #Uses function from above to connect to DB
    cur = conn.cursor()   # Creates a "cursor" object used to execute SQL commands
    # --- SQL Query to Get Relevant Rows ---
    cur.execute(f"""
    SELECT sets, reps, weight
    FROM {table_name}
    WHERE LOWER(REPLACE(exercise, ' ', '')) = ?
""", (exercise_to_avg,))
# Explanation:
# 1. SELECT sets, reps, weight: We only need these columns to calculate total weight lifted and total reps.
# 2. FROM {table_name}: This is the SQLite table where all your workout logs are stored.
# 3. WHERE LOWER(REPLACE(exercise, ' ', '')) = ?:
#    - This filters rows to only include the exercise the user specified.
#    - REPLACE(exercise, ' ', '') removes spaces in case the DB has different spacing.
#    - LOWER(...) makes it case-insensitive so "squat", "Squat", "SQUAT" all match.
# 4. The ? is a placeholder for parameterized queries, which protects against SQL injection.
# 5. (exercise_to_avg,) provides the actual value for the placeholder.

# --- Fetch All Matching Rows ---
    rows = cur.fetchall()
# Explanation:
# - fetchall() retrieves all rows returned by the query as a list of sqlite3.Row objects.
# - Each row contains 'sets', 'reps', and 'weight' for a single logged workout.

# --- Close the Database Connection ---
    conn.close()
# Explanation:
# - Always close the DB connection after fetching data to free resources which is useful when having more users and higher data usage.

# --- Sum Total Weight and Reps ---
    for row in rows:
        sets = int(row["sets"])        # Convert 'sets' from string to integer
        reps = int(row["reps"])        # Convert 'reps' from string to integer
        weight = float(row["weight"])  # Convert 'weight' from string to float

    # Total weight lifted in this entry = weight * reps * sets
        total_weight += weight * reps * sets

    # Total reps performed in this entry = reps * sets
        total_reps += reps * sets

# Explanation:
# - This loop accumulates total_weight and total_reps across all rows for the selected exercise.
# - These totals will later be used to compute the average weight lifted per rep.

# --- Calculate Average Weight per Rep ---
    if total_reps > 0: #Checks to make sure the exercise exists in the DB
        avg_weight_per_rep = total_weight / total_reps
        return {
            "exercise": exercise_to_avg,                 # The exercise name
            "average": round(avg_weight_per_rep, 2),     # Average weight per rep, rounded to 2 decimals
            "total_reps": total_reps                     # Total reps performed
        }
    else:
        return {"error": f"No entries found for {exercise_to_avg}"}
# Explanation:
# - If total_reps is zero, it means there are no entries for this exercise in the DB.
# - Otherwise, we compute average weight per rep: total_weight / total_reps.
# - Return a dictionary containing the exercise, average weight per rep, and total reps.
# - This dictionary can then be used in your Flask app or API response.
    
##### WILKS CALCULATOR FLASK VERSION ########

def wilks(bodyweight_lbs, total_lift_lbs):
    # Convert pounds to kilograms
    weight_kg = bodyweight_lbs * 0.453592
    total_kg = total_lift_lbs * 0.453592

    # Wilks formula coefficients (for men)
    a = -216.0475144
    b = 16.2606339
    c = -0.002388645
    d = -0.00113732
    e = 7.01863E-06
    f = -1.291E-08

    coefficient = 500 / (a + b*weight_kg + c*(weight_kg**2) +
                         d*(weight_kg**3) + e*(weight_kg**4) + f*(weight_kg**5))
    wilks_score = round(total_kg * coefficient, 2)
    return wilks_score


##### GET DOTS SCORE FLASK VERSION ##### 
def dots(bodyweight_lbs, total_lift_lbs): #Passes these 2 parameters 
    # Convert pounds to kilograms
    weight_kg = bodyweight_lbs * 0.453592
    total_kg = total_lift_lbs * 0.453592
    a = -307.75076
    b = 24.0900756
    c = -0.1918759221
    d = 0.0007391293
    e = -0.000001093
    coefficient = (a + b*(weight_kg) + c*(weight_kg**2) + d*(weight_kg**3) +  e*(weight_kg**4))
    dots_score = (500 / coefficient) * total_kg
    dots_score = round(dots_score,2)
    return dots_score #Returns this to use in app.py as results.rm

    ########### One Rep Max Estimate Function FLASK VERSION ###################
def one_rep_max(weight, reps):
    max = round(weight * reps**0.1, 2) #Rounds to 2 decimal points after multiplying weight by reps to the power of 0.1

    return max


##### PLATE CALCULATOR FLASK VERSION LBS ONLY ########

def plate_calculator(weight):
        weight_for_plates = weight - 45      #Subtracts bar weight of 45

        if weight_for_plates < 0:
            return Error

        # Weight per side (divide by 2 since plates go on both sides)
        weight_per_side = weight_for_plates / 2
        remaining_weight = weight_per_side
        # Calculate plates needed per side (only whole numbers)
        forty_five_plates = int(weight_per_side // 45)
        remaining_weight = weight_per_side % 45
        #print(f"Weight left per side: {remaining_weight}") #For testing
        twenty_five_plates = int(remaining_weight // 25)
        remaining_weight = remaining_weight % 25
        #print(f"Weight left per side after 25s: {remaining_weight}") #For testing
        ten_plates = int(remaining_weight // 10)
        remaining_weight = remaining_weight % 10
        five_plates = int(remaining_weight // 5)
        remaining_weight = remaining_weight % 5
        two_and_half_plates = int(remaining_weight // 2.5)
        
        #print(f"You will need {fourty_five_plates} 45(s),{twenty_five_plates} 25(s), {ten_plates} 10(s), {five_plates} 5(s) and {two_and_half_plates} 2.5(s) per side")
        return {
        "45s": forty_five_plates,
        "25s": twenty_five_plates,
        "10s": ten_plates,
        "5s": five_plates,
        "2.5s": two_and_half_plates
    }
    #Returns a dictionary

####################### ALL FUNCTIONS FROM HELPERS.PY #######################

##### BASICALLY JUST HELPER FUNCTIONS FOR OTHER FILES AND FUNCTIONS ON THIS PAGE #####

###### Function to get valid inputs #########
def get_valid_number_input(prompt, field_name, max_attempts=3, clear_screen=False):
    """
    Prompts the user to enter a numeric value with limited attempts.

    Parameters:
        prompt (str): The input prompt to display.
        field_name (str): What the number represents (e.g., Sets, Reps).
        max_attempts (int): How many times the user can try.
        clear_screen (bool): Whether to clear the screen after valid input.

    Returns:
        int or None: The validated integer, or None if attempts are exceeded.
    """
    attempts = 0

    while attempts < max_attempts:
        user_input = input(prompt).strip()

        if user_input.isdigit():
            num = int(user_input)
            print(f"{field_name} entered: {num}")
            time.sleep(1)
            if clear_screen:
                os.system("clear")  # Use "cls" on Windows to clear console
            return num
        else:
            attempts += 1
            print(f"Invalid input. Only digits allowed. {max_attempts - attempts} attempt(s) left.")

    print("You've exceeded the maximum number of attempts. Please try again later.")
    return None

    ###### CONVERT TIME FUNCTION ######## 
#### CONVERTS 2025-06-12 to 06/12/25 like how we want for CSV and for the DB ########
def convert_iso_to_mmddyy(iso_date_str):
    try:
        # Parse ISO format: '2025-06-19'
        date_obj = datetime.datetime.strptime(iso_date_str, "%Y-%m-%d")
        # Convert to MM/DD/YY
        return date_obj.strftime("%m/%d/%y")
    except ValueError:
        raise ValueError("Invalid date format. Expected YYYY-MM-DD.")


############### Clears the last workout entry entered in case of a typo/etc ###################
#### DO NOT HAVE THIS ADDED TO FLASK ROUTE PAGE YET ####
#### NEED IT TO WORK FOR DB AS WELL AS CSV ####
def clear_last_entry():
    #Read all lines from the file
    with open(CSV_FILE, "r") as file:
        lines = file.readlines()

    #Remove the last line
    if lines:
        lines = lines[:-1]  # All lines except the last

        # Step 3: Write the remaining lines back to the file -- This will overwrite the whole file with the old data minus the last line
        with open(CSV_FILE, "w") as file:
            file.writelines(lines)

        print("Last entry removed.")
    else:
        print("CSV is empty — nothing to remove.")

##### EXERCISE MANAGEMENT SECTION #######


#### ADD EXERCISE WITH ADDING TO SQLITE AND CSV #####

def add_exercise(form_data):
    # Predefined exercise list
    valid_exercises = [
        "Squat", "PauseSquat", "GobletSquat",
        "TouchNGoBench", "InclineBench", "Deadlift", "DeficitDeadlift",
        "RomanianDeadlift", "OverheadPress", "OverheadDBPress", "Bench", "PowerClean", "HangClean"
    ]

    # Extract form data -- NEEDED FOR BOTH CSV AND DB
    exercise_input = form_data.get('exercise', '').strip().replace(" ", "")
    sets_input = form_data.get('sets', '')
    rep_input = form_data.get('reps', '')
    weight_input = form_data.get('weight', '')
    date_input = form_data.get('date', '').strip()

    #### CSV SECTION ####
    # Validate and resolve exercise input
    if exercise_input == "":
        try:
            with open(CSV_FILE, "r") as file:
                last_line = list(csv.reader(file))[-1]
                exercise_input = last_line[0]
        except Exception:
            raise ValueError("No previous exercise found.")
    else:
        match_found = False
        for exercise in valid_exercises:
            if exercise.lower().replace(" ", "") == exercise_input.lower():
                exercise_input = exercise
                match_found = True
                break
        if not match_found:
            raise ValueError("Invalid exercise name.")

    # Use last date if none entered
    last_date = None
    try:
        with open(CSV_FILE, "r") as file:
            last_line = list(csv.reader(file))[-1]
            last_date = last_line[-2]  # second-to-last column (before id)
    except Exception:
        pass

    if not last_date:
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute(f"SELECT date FROM {table_name} ORDER BY id DESC LIMIT 1")
            row = cur.fetchone()
            if row:
                last_date = row[0]
            conn.close()
        except Exception:
            pass

    if date_input == "":
        if last_date:
            date_input = last_date
        else:
            raise ValueError("No previous date found.")
    else:
        try:
            date_input = convert_iso_to_mmddyy(date_input)
        except ValueError:
            raise ValueError("Invalid date format. Please use MM/DD/YY.")

    # Determine next ID for CSV
    next_id = 1
    try:
        with open(CSV_FILE, "r") as file:
            last_line = list(csv.reader(file))[-1]
            next_id = int(last_line[-1]) + 1
    except Exception:
        pass  # file missing or empty, start at 1

    # Write to CSV (ID last)
    # Write to CSV
    with open(CSV_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([exercise_input, sets_input, rep_input, weight_input, date_input, next_id])


    #### DB SECTION ####
    conn = get_db_connection()
    cur = conn.cursor()

    # Check if table exists
    cur.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
    table_exists = cur.fetchone() is not None

    if not table_exists:
        # Create new table with proper AUTOINCREMENT schema
        cur.execute(f"""
            CREATE TABLE {table_name} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                exercise TEXT,
                sets TEXT,
                reps TEXT,
                weight TEXT,
                date TEXT
            )
        """)
    else:
        # Table exists, but may not have proper AUTOINCREMENT
        # Check if id is properly defined as PRIMARY KEY
        cur.execute(f"PRAGMA table_info({table_name})")
        columns = {col[1]: col for col in cur.fetchall()}
        
        if 'id' not in columns or not columns['id'][5]:  # col[5] is pk flag
            # Table exists but doesn't have proper ID schema
            # Migrate data to new table with proper schema
            try:
                cur.execute(f"SELECT * FROM {table_name}")
                existing_data = cur.fetchall()
                
                # Rename old table
                cur.execute(f"ALTER TABLE {table_name} RENAME TO {table_name}_old")
                
                # Create new table with proper schema
                cur.execute(f"""
                    CREATE TABLE {table_name} (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        exercise TEXT,
                        sets TEXT,
                        reps TEXT,
                        weight TEXT,
                        date TEXT
                    )
                """)
                
                # Copy data back (new IDs will be generated)
                for row in existing_data:
                    cur.execute(f"""
                        INSERT INTO {table_name} (exercise, sets, reps, weight, date)
                        VALUES (?, ?, ?, ?, ?)
                    """, row[:-1])  # Skip old ID column
                
                # Drop old table
                cur.execute(f"DROP TABLE {table_name}_old")
                print(f"Migrated {table_name} to proper schema with auto-incrementing IDs")
            except Exception as e:
                print(f"Warning: Could not migrate table schema: {e}")

    # Insert the new entry (ID should be auto-generated by SQLite)
    cur.execute(f"""
        INSERT INTO {table_name} (exercise, sets, reps, weight, date)
        VALUES (?, ?, ?, ?, ?)
    """, (exercise_input, sets_input, rep_input, weight_input, date_input))

    conn.commit()
    conn.close()



##### EDIT EXERCISE SECTION ########

def edit_exercise(form_data):
    """
    Updates an exercise entry (by ID) in both CSV and DB.
    Matches validation and logic style of add_exercise().
    """
    valid_exercises = [
        "Squat", "PauseSquat", "GobletSquat", "PauseBench",
        "TouchNGoBench", "InclineBench", "Deadlift", "DeficitDeadlift",
        "RomanianDeadlift", "OverheadPress", "OverheadDBPress", "Bench",
        "PowerClean", "HangClean"
    ]

    # === Extract form data ===
    id_input = form_data.get('id', '').strip()
    exercise_input = form_data.get('exercise', '').strip().replace(" ", "")
    sets_input = form_data.get('sets', '')
    rep_input = form_data.get('reps', '')
    weight_input = form_data.get('weight', '')
    date_input = form_data.get('date', '').strip()

    if not id_input.isdigit():
        raise ValueError("ID must be provided and numeric.")

    #### VALIDATE EXERCISE ####
    if exercise_input:
        match_found = False
        for exercise in valid_exercises:
            if exercise.lower().replace(" ", "") == exercise_input.lower():
                exercise_input = exercise
                match_found = True
                break
        if not match_found:
            raise ValueError("Invalid exercise name.")

    #### === UPDATE IN DATABASE === ####
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(f"""
        UPDATE {table_name}
        SET exercise=?, sets=?, reps=?, weight=?, date=?
        WHERE id=?
    """, (exercise_input, sets_input, rep_input, weight_input, date_input, id_input))
    conn.commit()
    conn.close()

    #### === UPDATE IN CSV === ####
    if not os.path.exists(CSV_FILE):
        return  # no CSV to update, skip

    updated_rows = []
    with open(CSV_FILE, "r", newline="") as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) >= 6 and row[-1] == id_input:  # match by ID
                updated_rows.append([exercise_input, sets_input, rep_input, weight_input, date_input, id_input])
            else:
                updated_rows.append(row)

    with open(CSV_FILE, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(updated_rows)



###### DELETE EXERCISE SECTION ########

def delete_exercise(form_data):
    """
    Deletes an exercise entry (by ID) from both CSV and DB.
    Matches validation and structure of add_exercise() and edit_exercise().
    """
    id_input = form_data.get('id', '').strip()

    if not id_input.isdigit():
        raise ValueError("ID must be provided and numeric.")

    # Convert ID to integer for database query (DB stores ID as INTEGER)
    id_int = int(id_input)

    #### === DELETE FROM DATABASE === ####
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(f"""
            DELETE FROM {table_name}
            WHERE id=?
        """, (id_int,))
        rows_deleted = cur.rowcount  # Check how many rows were deleted
        conn.commit()
        conn.close()
        print(f"Database: Deleted {rows_deleted} row(s) with ID {id_int}")
    except Exception as e:
        print(f"Database deletion error: {e}")

    #### === DELETE FROM CSV === ####
    if not os.path.exists(CSV_FILE):
        print(f"CSV file not found: {CSV_FILE}")
        return  # skip if CSV missing

    updated_rows = []
    deleted = False
    with open(CSV_FILE, "r", newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) >= 6 and row[-1] == id_input:
                deleted = True
                print(f"CSV: Found and deleting row with ID {id_input}")
                continue  # skip the row we're deleting
            updated_rows.append(row)

    with open(CSV_FILE, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(updated_rows)

    if not deleted:
        print(f"CSV: No matching record found with ID {id_input}.")


####################### ALL FUNCTIONS FROM VISUALIZATIONS.PY #######################
####################### GRAPH SECTION #######################


def create_progression_graph(exercise=None, start_date=None, end_date=None):
    conn = get_db_connection()
    df = pd.read_sql_query("SELECT * FROM Workout", conn)
    conn.close()

    # Normalize columns and values
    df.columns = df.columns.str.strip().str.lower()
    df['exercise'] = df['exercise'].astype(str).str.strip().str.lower()
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df['weight'] = pd.to_numeric(df['weight'], errors='coerce')

    # Apply filters
    if exercise:
        df = df[df['exercise'] == exercise.strip().lower()]
    if start_date:
        df = df[df['date'] >= pd.to_datetime(start_date)]
    if end_date:
        df = df[df['date'] <= pd.to_datetime(end_date)]

    if df.empty:
        return None

    df = df.sort_values(by='date')

    plt.figure(figsize=(10, 6))
    for ex in df['exercise'].unique():
        subset = df[df['exercise'] == ex]
        plt.plot(subset['date'], subset['weight'], marker='o', label=ex.title())

    plt.xlabel("Date")
    plt.ylabel("Weight Lifted")
    plt.title("Progression Over Time")
    plt.legend()
    plt.grid(True)

    buffer = BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    buffer.seek(0)
    graph_data = base64.b64encode(buffer.getvalue()).decode()
    plt.close()

    return f'data:image/png;base64,{graph_data}'


def create_exercise_distribution_pie_chart(exercise=None, start_date=None, end_date=None):
    conn = get_db_connection()
    df = pd.read_sql_query("SELECT * FROM Workout", conn)
    conn.close()

    df.columns = df.columns.str.strip().str.lower()
    df['exercise'] = df['exercise'].astype(str).str.strip().str.lower()
    df['date'] = pd.to_datetime(df['date'], errors='coerce')

    if exercise:
        df = df[df['exercise'] == exercise.strip().lower()]
    if start_date:
        df = df[df['date'] >= pd.to_datetime(start_date)]
    if end_date:
        df = df[df['date'] <= pd.to_datetime(end_date)]

    if df.empty:
        return None

    distribution = df['exercise'].value_counts()

    plt.figure(figsize=(8, 8))
    plt.pie(distribution, autopct='%1.1f%%', startangle=90)
    plt.legend(
        labels=[ex.title() for ex in distribution.index],
        loc="center left",
        bbox_to_anchor=(0.1, 0.5)
    )
    plt.title("Exercise Distribution")
    plt.axis('equal')

    buffer = BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    buffer.seek(0)
    graph_data = base64.b64encode(buffer.getvalue()).decode()
    plt.close()

    return f'data:image/png;base64,{graph_data}'

