import os
import csv
import time
import datetime


file_path = 'WorkoutLog.csv'

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