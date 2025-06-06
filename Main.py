####TO DO

#Add Deadlift Data - Completed on 3/31
#Update Exercise list entry to always be capitilized with no spaces for user input and in the list itself as well??? -- Just no spaces would be best actually -- Completed
#Date validation for entering dates - Completed
#Graph section next
#Clear function -- To clear a certain lift that you entered --- Can make it so it only clears the last one entered if you have a typo
#Edit function to edit a certain entry -- Would need to have date, lift, sets, reps to make it specific enough to edit
#Fix graph so that it outputs more useful information - May need to rework that whole function now that we have real data

#Update ReadMe
#Input validation everywhere
#Set up classes so it can be used in other scripts??

#Difficult/Future Tense
#Allow the script to be run from my phone to enter data there -- Works in Replit currently
#Use the script in Google Sheets etc, not just locally -- Works if someone uses the GitHub repo

#Import Statements
import time  #Used for adding delays to the script if needed
import csv  #Used to import the CSV
import os  #Used to import the file path for the CSV and other useful functions
#import pandas as pd #Not currently used
import matplotlib.pyplot as plt  #Used to plot the graph
from datetime import datetime  #Used to

print("Welcome to Lee's Workout Tracker!")

#Global variables - Not going to change
file_path = 'WorkoutLog.csv'

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

def add_exercise():
    exercises = [
        "Squat", "PauseSquat", "GobletSquat", "PauseBench",
        "TouchNGoBench", "InclineDBBench", "Deadlift", "DeficitDeadlift",
        "RomanianDeadlift", "OverheadPress", "OverheadDBPress"
    ]

    print("List of Exercises to choose from:")
    for exercise in exercises:
        print(exercise)

    # Input exercise with attempts
    max_attempts_lift = 3
    attempts_lift = 0
    exercise_input = None
    while attempts_lift < max_attempts_lift:
        user_input = input("\nEnter the name of the exercise: ").strip().replace(" ", "")
        match = next((ex for ex in exercises if ex.lower() == user_input.lower()), None)
        if match:
            exercise_input = match
            print(f"You've selected: {match}")
            time.sleep(0.5)
            os.system("clear")
            break
        else:
            attempts_lift += 1
            print(f"Invalid exercise. {max_attempts_lift - attempts_lift} attempt(s) left.")
    if exercise_input is None:
        print("You've exceeded the maximum number of attempts. Please try again later.")
        return  # Exit the function early

    # Get sets, reps, weight
    sets_input = get_valid_number_input("Sets > ", field_name="Sets", max_attempts=3, clear_screen=True)
    rep_input = get_valid_number_input("Reps > ", field_name="Reps", max_attempts=3, clear_screen=True)
    weight_input = get_valid_number_input("Weight > ", field_name="Lbs", max_attempts=3, clear_screen=True)

    # Date input (keep last used date if user just presses Enter)
    date_input = input("Enter the date of this lift (MM/DD/YY), or press Enter to use the previous date: ").strip()
    if not date_input:
        try:
            #Trys to read the last line of the file
            with open(file_path, "r") as file:
                last_line = list(csv.reader(file))[-1] #Gets the last line of the CSV in the date column
                date_input = last_line[-1] #Uses the last item in the row to get the date
                print(f"Using previous date: {date_input}")
        except Exception:
            print("No previous date found. Please enter the date manually next time.")
            return

    time.sleep(1)
    os.system("clear")

    print(f"Exercise: {exercise_input}\nSets: {sets_input}\nReps: {rep_input}\nWeight: {weight_input} lbs\nDate: {date_input}")

    # Append to CSV
    new_entry = [exercise_input, sets_input, rep_input, weight_input, date_input]
    with open(file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(new_entry)

    print(f"New Lift added to {file_path}")
    time.sleep(2)
    os.system("clear")

#Function to get the average weight lifted per rep
def average_lift():
    exercise_to_avg = input("Enter the exercise you want to calculate the average weight for: ")
    file_path = 'WorkoutLog.csv'
    if not os.path.exists(file_path):
        print(f"The file {file_path} does not exist.")
        return

    total_weight = 0
    total_reps = 0

    # Read the CSV file and calculate the total weight for the selected exercise
    with open(file_path, mode='r') as file:
        reader = csv.reader(file)

        # Skip the header row if there is one
        next(reader, None)  # Skip the header row (if there is one)
        #Reads the file to get the total weight done and reps done
        for row in reader:
            exercise, sets, reps, weight, *extra_columns = row  #Extra_columns needed otherwise it won't work due to an error saying its missing a row (Date)
            if exercise == exercise_to_avg:  #Check to see if user input matches an exercise in the CSV
                total_weight += float(weight) * int(reps) * int(sets)  # Gets weight in lbs
                total_reps += int(reps) * int(sets)# Add the total number of reps (sets * reps) to total_reps
    # Calculate and display the average
    if total_reps > 0:
        avg_weight_per_rep = total_weight / total_reps
        print(f"The average weight lifted per rep for {exercise_to_avg} is: {avg_weight_per_rep:.2f} lbs")
    else:
        print(f"No entries found for {exercise_to_avg}.")

#Function to create a graph to see trends for lifts
def plot_exercise_data(file_path):
    """
    Reads exercise data from a CSV file and plots a line graph showing the weight lifted per set
    for each exercise, over time.

    Args:
    - csv_file (str): The path to the CSV file containing the exercise data.
    """
    # Step 1: Read the data from the CSV file
    exercises = {}  # To store data for each exercise

    #This opens the file and reads it file_path is define above in the script as WorkoutLog.csv
'''
    with open(file_path, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)

        # Step 2: Process each row
        for row in reader:
'''
#Function to a display menu that a user will see first
def display_menu():
    while True:
        print("\n--- Workout Log Menu ---")
        print("1. Add Exercise Entry")
        print("2. Calculate Average Lift")
        print("3. Graph it!")
        print("4. Exit")

        choice = input("Select an option (1, 2, 3, or 4): ")

        if choice == '1' or choice == 'add' or choice == 'Add':
            # Call function to add exercise
            add_exercise()
            #exercise_input, sets_input, rep_input, weight_input, date_input = add_exercise()
            #add_entry_to_CSV(exercise_input, sets_input, rep_input,weight_input, date_input)
        
        elif choice == '2' or choice == 'Avg' or choice == 'Average' or choice == 'average' or choice == 'avg':
            # Call function to calculate average lift
            average_lift()
        elif choice == '3' or choice == 'Graph' or choice == 'graph':
            plot_exercise_data(file_path)
        elif choice == '4' or choice == 'Exit' or choice == 'exit':
            print("Exiting the program.")
            break  # Exit the program
        else:
            print("Invalid option selected. Please try again.")


# Main function to execute the program
def main():
    display_menu()


# Call the main function
if __name__ == "__main__":
    main()

#Add section here to be able to test one function without having to go through the whole program??
