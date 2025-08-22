### ALL FUNCTIONS FROM CALC.PY ###

import os
import csv
import time
import datetime

import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
from io import BytesIO
#from utils.calc import average_lift

file_path = 'WorkoutLog.csv' #Global Variable

###### LIFT AVERAGE FLASK VERSION #########

def average_lift(exercise_to_avg):
    exercise_to_avg = exercise_to_avg.strip().replace(" ", "").lower()  # normalize input to lower to check the CSV
    #Initialize variables to be 0 
    total_weight = 0
    total_reps = 0

    # Read the CSV file and calculate the total weight for the selected exercise
    with open(file_path, mode='r') as file:
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

### ALL FUNCTIONS FROM HELPERS.PY ###

'''
import os
import csv
import time
import datetime


file_path = 'WorkoutLog.csv'
'''
###### Function to get valid inputs #########
### Add this line to test a push### 
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
                os.system("clear")  # Use "cls" on Windows
            return num
        else:
            attempts += 1
            print(f"Invalid input. Only digits allowed. {max_attempts - attempts} attempt(s) left.")

    print("You've exceeded the maximum number of attempts. Please try again later.")
    return None

    ###### CONVERT TIME FUNCTION ######## 
#### CONVERTS 2025-06-12 to 06/12/25 like how we want for CSV ########
def convert_iso_to_mmddyy(iso_date_str):
    try:
        # Parse ISO format: '2025-06-19'
        date_obj = datetime.datetime.strptime(iso_date_str, "%Y-%m-%d")
        # Convert to MM/DD/YY
        return date_obj.strftime("%m/%d/%y")
    except ValueError:
        raise ValueError("Invalid date format. Expected YYYY-MM-DD.")


############### Clears the last workout entry entered in case of a typo/etc ###################
def clear_last_entry():
    #Read all lines from the file
    with open(file_path, "r") as file:
        lines = file.readlines()

    #Remove the last line
    if lines:
        lines = lines[:-1]  # All lines except the last

        # Step 3: Write the remaining lines back to the file -- This will overwrite the whole file with the old data minus the last line
        with open(file_path, "w") as file:
            file.writelines(lines)

        print("Last entry removed.")
    else:
        print("CSV is empty — nothing to remove.")


#### MARK A PR FUNCTION #####

#### NEED TO FIX THIS STILL ####

'''
def mark_pr(exercise, new_weight):
    max_weight = 0 
    # Needs to check what exercise and then see the max weight done for that exercise
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['Exercise'].lower() == exercise.lower():
                try:
                    weight = float(row['Weight'])
                    if weight > max_weight:
                        max_weight = weight
                except ValueError:
                    continue
    return new_weight > max_weight

'''

#### ADD EXERCISE FLASK VERSION ######

def add_exercise(form_data):
    # Predefined exercise list
    valid_exercises = [
        "Squat", "PauseSquat", "GobletSquat", "PauseBench",
        "TouchNGoBench", "InclineDBBench", "Deadlift", "DeficitDeadlift",
        "RomanianDeadlift", "OverheadPress", "OverheadDBPress", "Bench"
    ]

    # Extract form data
    exercise_input = form_data.get('exercise', '').strip().replace(" ", "")
    sets_input = form_data.get('sets', '')
    rep_input = form_data.get('reps', '')
    weight_input = form_data.get('weight', '')
    date_input = form_data.get('date', '')

    # Validate and resolve exercise input
    if exercise_input == "":
        try:
            with open(file_path, "r") as file:
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
    if date_input.strip() == "":
        try:
            with open(file_path, "r") as file:
                last_line = list(csv.reader(file))[-1]
                date_input = last_line[-1]
        except Exception:
            raise ValueError("No previous date found.")
    else:
    # Validate date format
        try:
            date_input = convert_iso_to_mmddyy(date_input)
        except ValueError:
            raise ValueError("Invalid date format. Please use MM/DD/YY.")
# Write the validated data to CSV
    new_entry = [exercise_input, sets_input, rep_input, weight_input, date_input]
    with open(file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(new_entry)




### ALL FUNCTIONS FROM VISUALIZATIONS.PY ###

'''
import pandas as pd
import matplotlib.pyplot as plt
import time
import os
import io
import base64
from io import BytesIO
from utils.calc import average_lift

file_path = 'WorkoutLog.csv'
'''

def create_progression_graph(file_path):
    # Load CSV
    df = pd.read_csv(file_path)

    # Convert Date column to datetime
    df['Date'] = pd.to_datetime(df['Date'])

    # Sort by date to keep lines in order
    df = df.sort_values(by='Date')

    # Plot setup
    plt.figure(figsize=(10, 6))

    # Plot one line per exercise
    for exercise in df['Exercise'].unique():
        subset = df[df['Exercise'] == exercise]
        plt.plot(subset['Date'], subset['Weight'], marker='o', label=exercise)

    # Labels & legend
    plt.xlabel("Date")
    plt.ylabel("Weight Lifted")
    plt.title("Progression Over Time")
    plt.legend(title="Exercise")
    plt.grid(True)

    # Save to buffer for Flask embedding
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    graph_data = base64.b64encode(buffer.getvalue()).decode()
    plt.close()
    return f'data:image/png;base64,{graph_data}'

def volume_per_workout(file_path):
    # Load CSV
    df = pd.read_csv(file_path)

    # Convert Date column to datetime
    df['Date'] = pd.to_datetime(df['Date'])

    # OPTIONAL: Sort by date
    df = df.sort_values(by='Date')

    df['Volume'] = df['Weight'] * df['Reps'] * df['Sets']
    volume_per_day = df.groupby('Date')['Volume'].sum().reset_index()

    # === Bar Chart ===
    plt.figure(figsize=(10, 6))
    # Create an empty list to hold bar colors
    colors = []

# Loop through each volume value
    for volume in volume_per_day['Volume']:
        if volume > 7000:
            colors.append('red')
        else:
            colors.append('green')
    plt.bar(volume_per_day['Date'].dt.strftime('%Y-%m-%d'), volume_per_day['Volume'], color=colors)
    
    # Labels and layout
    plt.xlabel("Date")
    plt.ylabel("Total Volume")
    plt.title("Workout Volume Per Day")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.grid(True, axis='y')

    # Save to buffer for Flask
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    graph_data = base64.b64encode(buffer.getvalue()).decode()
    plt.close()
    return f'data:image/png;base64,{graph_data}'

import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64

def average_intensity(file_path):
    # Load CSV
    df = pd.read_csv(file_path)

    # Calculate total weight and total reps per row
    df['TotalWeight'] = df['Weight'] * df['Reps'] * df['Sets']
    df['TotalReps'] = df['Reps'] * df['Sets']

    # Group by exercise
    grouped = df.groupby('Exercise').agg({
        'TotalWeight': 'sum',
        'TotalReps': 'sum'
    }).reset_index()

    # Calculate average weight per rep for each exercise
    grouped['AvgWeightPerRep'] = grouped['TotalWeight'] / grouped['TotalReps']

    # === Bar Chart ===
    plt.figure(figsize=(10, 6))
    plt.bar(grouped['Exercise'], grouped['AvgWeightPerRep'], color='purple')


    # Labels and layout
    plt.xlabel("Exercise")
    plt.ylabel("Average Weight per Rep")
    plt.title("Average Intensity by Exercise")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.grid(True, axis='y')

    # Save to buffer for Flask
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    graph_data = base64.b64encode(buffer.getvalue()).decode()
    plt.close()

    return f'data:image/png;base64,{graph_data}'

