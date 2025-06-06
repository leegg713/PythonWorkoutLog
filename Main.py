####TO DO

#Add Deadlift Data - Completed on 3/31
#Update Exercise list entry to always be capitilized with no spaces for user input and in the list itself as well??? -- Just no spaces would be best actually -- Completed
#Date validation for entering dates - Completed
#Graph section next - Completed for now
#Clear function -- To clear a certain lift that you entered --- Completed -- Just clears last one
#Edit function to edit a certain entry -- Would need to have date, lift, sets, reps to make it specific enough to edit

#Update ReadMe
#Create requirements.txt file to use

#Difficult/Future Tense
#Allow the script to be run from my phone to enter data there -- Works in Replit currently
#Use the script in Google Sheets etc, not just locally -- Works if someone uses the GitHub repo

#Import Statements
import time  #Used for adding delays to the script if needed
import csv  #Used to import the CSV
import os  #Used to import the file path for the CSV and other useful functions
import pandas as pd #Used to get a dataframe for the graph
import matplotlib.pyplot as plt  #Used to plot the graph

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


def add_exercise():
    exercises = [
        "Squat", "PauseSquat", "GobletSquat", "PauseBench",
        "TouchNGoBench", "InclineDBBench", "Deadlift", "DeficitDeadlift",
        "RomanianDeadlift", "OverheadPress", "OverheadDBPress"
    ]

    print("List of Exercises to choose from:")
    for exercise in exercises:
        print(exercise)

    max_attempts_lift = 3
    attempts_lift = 0
    exercise_input = None

    while attempts_lift < max_attempts_lift:
        user_input = input("\nEnter the name of the exercise: ").strip().replace(" ", "")
        for exercise in exercises:
            if exercise.lower().replace(" ", "") == user_input.lower():
                print(f"You've selected: {exercise}")
                time.sleep(0.5)
                os.system("clear")
                exercise_input = exercise  # Store the correctly formatted name
                break
        else:
            attempts_lift += 1
            print(f"Invalid exercise. {max_attempts_lift - attempts_lift} attempt(s) left.")

        if exercise_input:
            break  # Exit loop after successful selection

    if exercise_input is None:
        print("You've exceeded the maximum number of attempts. Please try again later.")
        return

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
    time.sleep(0.5)
    os.system("clear")
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
        time.sleep(5)
        os.system("clear")
    else:
        print(f"No entries found for {exercise_to_avg}.")
        time.sleep(5)
        os.system("clear")

#Function to create a graph to see trends for lifts
def plot_exercise_data():
    df = pd.read_csv(file_path) #Dataframe using pandas to read the csv
    #print(df.head()) #Prints First 5 rows to test it out to make sure it imported correct

    lift_name = input("\nEnter the name of the exercise to get a graph for: ").strip().replace(" ", "")
    lift_data = df[df["Exercise"] == lift_name]

    plt.plot(lift_data["Date"], lift_data["Weight"], marker="o")
    plt.title(f"{lift_name} Weight Over Time")
    plt.xlabel("Date")
    plt.ylabel("Weight")
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    '''
    plt.figure(figsize=(10, 6))
    for weight in lift_data["Weight"].unique():
        weight_data = lift_data[lift_data["Weight"] == weight]
        plt.plot(weight_data["Date"], weight_data["Reps"], marker="o", label=f"{weight} lbs")

    plt.title(f"{lift_name} — Reps Over Time (Grouped by Weight)")
    plt.xlabel("Date")
    plt.ylabel("Reps")
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.legend(title="Weight")
    plt.tight_layout()
    plt.show()

    '''




#Function to a display menu that a user will see first
def display_menu():
    while True:
        print("\n--- Workout Log Menu ---")
        print("1. Add Exercise Entry")
        print("2. Calculate Average Lift")
        print("3. Graph it!")
        print("4. Clear last entry")
        print("5. Exit")

        choice = input("Select an option (1, 2, 3, 4, or 5): ")

        if choice == '1' or choice == 'add' or choice == 'Add':
            # Call function to add exercise
            add_exercise()
            #exercise_input, sets_input, rep_input, weight_input, date_input = add_exercise()
            #add_entry_to_CSV(exercise_input, sets_input, rep_input,weight_input, date_input)
        
        elif choice == '2' or choice == 'Avg' or choice == 'Average' or choice == 'average' or choice == 'avg':
            # Call function to calculate average lift
            average_lift()
        elif choice == '3' or choice == 'Graph' or choice == 'graph':
            plot_exercise_data()

        elif choice == '4' or choice == 'clear' or choice == 'remove' or choice == "Clear" or choice == "Remove":
            clear_last_entry()
        elif choice == '5' or choice == 'Exit' or choice == 'exit':
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
