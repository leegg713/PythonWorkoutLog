####TO DO

#Add Deadlift Data - Completed on 3/31
#Update Exercise list entry to always be capitilized with no spaces for user input and in the list itself as well??? -- Just no spaces would be best actually
#Date validation for entering dates
#Clear function -- To clear a certain lift that you entered --- Can make it so it only clears the last one entered if you have a typo
#Edit function to edit a certain entry -- Would need to have date, lift, sets, reps to make it specific enough to edit
#Fix graph so that it outputs more useful information - May need to rework that whole function now that we have real data

#Update ReadMe
#Input validation everywhere
#Set up classes so it can be used in other scripts??

#Difficult/Future Tense
#Allow the script to be run from my phone to enter data there
#Use the script in Google Sheets etc, not just locally
#Authentication to be able to run the script - Can comment it out after it works to save me time daily, but will be a nice feature to have

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


def add_exercise(
):  #Add exercise to CSV - Input of Exercise, Sets, Reps, Weight, Date
    # Predefined list of exercises, can add to this list as needed
    exercises = [
        "Squat", "Pause Squat", "Goblet Squat", "Pause Bench",
        "Touch N Go Bench", "Incline DB Bench", "Deadlift", "Deficit Deadlift",
        "Romanian Deadlift", "Overhead Press", "Overhead DB Press"
    ]

    # Print the list of exercises
    print("List of Exercises to choose from:")
    #For loop to print each exercise to the console
    for exercise in exercises:
        print(exercise)

# Set the maximum number of attempts to enter the name of an exercise

#Asking for user input for which exercise  #Fix this loop so that it works smoother, make you have to type in a correct name before proceeding with a try/except for all of those -- Can make a function for it since it is reused
    max_attempts_lift = 3
    attempts_lift = 0
    while attempts_lift < max_attempts_lift:
        exercise_input = input("\nEnter the name of the exercise: ")

        if exercise_input in exercises:
            print(f"You've selected: {exercise_input}")
            time.sleep(0.5)
            os.system("clear")
            break  # Exit the loop if the input is valid
        else:
            attempts_lift += 1
            print(
                f"Invalid exercise. You have {max_attempts_lift - attempts_lift} attempt(s) left to type it correctly."
            )

    if attempts_lift == max_attempts_lift:
        print(
            "You've exceeded the maximum number of attempts. Please try again later idiot."
        )
    max_attempts_sets = 3
    attempts_sets = 0

    #Asking for user input for the amount of sets done

    while attempts_sets < max_attempts_sets:
        sets_input = input("Sets > ")
        if sets_input.isdigit():
            sets_input = int(sets_input)
            print(f"Sets Completed: {sets_input}")
            time.sleep(0.5)
            os.system("clear")
            break
        else:
            attempts_sets += 1
            print(
                f"You need to enter only digits. Try again. {max_attempts_sets - attempts_sets} tries left. "
            )
    if attempts_sets == max_attempts_sets:
        print(
            "You've exceeded the maximum number of attempts. Please try again later idiot."
        )

#Asking for user input for the amount of reps done
    max_attempts_reps = 3
    attempts_reps = 0

    while attempts_reps < max_attempts_reps:
        rep_input = input("Reps Completed >  ")
        if rep_input.isdigit():
            rep_input = int(rep_input)
            print(f"{rep_input} reps completed")
            time.sleep(0.5)
            os.system("clear")
            break
        else:
            attempts_reps += 1
            print(
                f"You need to enter only digits. Try again. {max_attempts_reps - attempts_reps} tries left."
            )

    if attempts_reps == max_attempts_reps:
        print(
            "You've exceeded the maximum number of attempts. Please try again later, idiot."
        )

    max_attempts_weight = 3
    attempts_weight = 0

    #Asking for user input for the amount of weight done

    while attempts_weight < max_attempts_weight:
        weight_input = input("Weight > ")
        if weight_input.isdigit():
            weight_input = int(weight_input)
            print(f"{weight_input} lbs for {exercise_input}")
            time.sleep(0.5)
            os.system("clear")
            break
        else:
            attempts_weight += 1
            print(
                f"You need to enter only digits. Try again. {max_attempts_weight - attempts_weight} tries left."
            )

    if attempts_weight == max_attempts_weight:
        print(
            "You've exceeded the maximum number of attempts. Please try again later, idiot."
        )

#Asks the user for a date - Must be in the specific date format

    date_input = input(
        "Enter the date of this lift (MM/DD/YY), or press Enter to use the previous date: "
    )  #Need to have it work so I can use enter to use the previous date -- For multiple same day entries which will happen frequently
    time.sleep(0.5)
    os.system("clear")
    #print(f"The date {date_input} is invalid.")

    #Can maybe delete the line below - Just a print to the console to check it -- Keep it for a check and balance
    print(
        f"Exercise: {exercise_input} \nSets: {sets_input}  \nReps Completed: {rep_input} \nWeight Used: {weight_input}lbs Date Entered: {date_input} "
    )
    

    #Returns the inputs to use in the add_entry_to_CSV function -- Only needed since these same numbers are used in the other function
    #Combine the 2 functions eventually to avoid that and make it cleaner
    return exercise_input, sets_input, rep_input, weight_input, date_input


#Function to add the entry to the CSV


def add_entry_to_CSV(exercise_input, sets_input, rep_input, weight_input,
                     date_input):

    #Takes the user input from add_exercise and creates a variable (List)
    new_entry = [
        exercise_input, sets_input, rep_input, weight_input, date_input
    ]

    #This function opens the file specified by file_path.​
    #mode='a': Opens the file in append mode, meaning new data will be added to the end of the file without altering existing content. ​
    #newline='': Ensures that newline characters are handled consistently across different operating systems, preventing extra blank lines in the CSV file. ​
    #with: Utilizes a context manager to handle the file, ensuring it is properly closed after the indented block is executed, even if errors occur.
    with open(file_path, mode='a',
              newline='') as file:  #Gets file_path ready to write a file to it
        writer = csv.writer(
            file
        )  # csv.writer() is a function from Python's csv module. It creates a writer object that knows how to write data into the file in CSV (comma-separated values) format. file is the file object we just opened.

        # Write the new entry to the CSV file
        writer.writerow(new_entry)

    #print(
    #   "New lift entry added to WorkoutLog.csv"
    #)  #Can delete this after further testing, just used to tell you it worked with no errors
    print(f"New Lift added to {file_path}")
    time.sleep(2)
    os.system("clear")

#Function to get the average weight lifted per rep
def average_lift():
    exercise_to_avg = input(
        "Enter the exercise you want to calculate the average weight for: ")
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

        for row in reader:
            exercise, sets, reps, weight, *extra_columns = row  #Extra_columns needed otherwise it won't work due to an error saying its missing a row (Date)
            if exercise == exercise_to_avg:  #Check to see if user input matches an exercise in the CSV
                total_weight += float(weight) * int(reps) * int(
                    sets)  # Assuming weight is in pounds
                # Add the total number of reps (sets * reps) to total_reps
                total_reps += int(reps) * int(sets)
    # Calculate and display the average
    if total_reps > 0:
        avg_weight_per_rep = total_weight / total_reps
        print(
            f"The average weight lifted per rep for {exercise_to_avg} is: {avg_weight_per_rep:.2f} lbs"
        )
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

    with open(file_path, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)

        # Step 2: Process each row
        for row in reader:
            '''
            # Check if the Date field is not empty
            date_str = row['Date']
            if date_str:  # Only process if the Date is not empty
                try:
                    # Parse the date from the MM/DD/YY format
                    date = datetime.strptime(date_str, '%m/%d/%y')
                except ValueError:
                    print(f"Warning: Invalid date format in row: {row}") #Outputs an error the console if a date is not valid... should not occur as date input is validate
                    continue  # Skip this row if the date is invalid
            else:
                print(f"Warning: Empty date in row: {row}") #Prints an error to the console if the date is empty... should not occur with new data
                continue  # Skip this row if the date is empty
            '''
            date = row['Date']
            exercise = row['Exercise']  #Variable for that row exercise
            weight = float(
                row['Weight'])  #Variable for the weight for that row
            reps = int(row['Reps'])  # Number of reps for the set
            set_number = int(row['Sets'])  # Track each set number individually

            # Initialize a list for the exercise if it doesn't exist
            if exercise not in exercises:
                exercises[exercise] = {
                    'dates': [],
                    'weights': [],
                    'reps': [],
                    'set_numbers': []
                }

            # Append the data for this set
            exercises[exercise]['dates'].append(date)
            exercises[exercise]['weights'].append(weight)
            exercises[exercise]['reps'].append(reps)
            exercises[exercise]['set_numbers'].append(set_number)

    # Step 3: Plot a line graph for each exercise
    plt.figure(
        figsize=(10, 6)
    )  # Optional: Set the figure size - Not sure exactly what this modifys - Look into it later

    for exercise, data in exercises.items():
        # Plot each set individually
        # plt.plot(data['dates'], data['weights'], marker='o', label=f"{exercise} (Set)")
        plt.plot(data['dates'], data['weights'], label=exercise, marker='o')

# Add annotations for the number of reps on each set = Says how many reps was done for each set
    for i, date in enumerate(data['dates']):
        plt.annotate(
            f"{data['reps'][i]} reps",
            (data['dates'][i], data['weights'][i]),
            textcoords="offset points",
            xytext=(0, 5),  # Offset the text slightly to avoid overlap
            ha='center')
    # Adding title and labels
    plt.title("Weight Lifted Per Set Over Time")
    plt.xlabel("Date")
    plt.ylabel("Weight (lbs)")
    plt.xticks(rotation=45)  # Rotate date labels for readability
    plt.legend(title="Exercise")

    # Display the plot
    plt.tight_layout(
    )  # Optional: Adjust the layout to prevent overlap - Is this needed or better or worse?/ - Look into later
    plt.show()


#Function to a display menu that a user will see first
def display_menu():
    while True:
        print("\n--- Workout Log Menu ---")
        print("1. Add Exercise Entry")
        print("2. Calculate Average Lift")
        print("3. Graph it!")
        print("4. Exit")

        choice = input("Select an option (1, 2, 3, or 4): ")

        if choice == '1':
            # Call function to add exercise
            exercise_input, sets_input, rep_input, weight_input, date_input = add_exercise(
            )
            add_entry_to_CSV(exercise_input, sets_input, rep_input,
                             weight_input, date_input)
        elif choice == 'Add':
            # Call function to add exercise
            exercise_input, sets_input, rep_input, weight_input, date_input = add_exercise(
            )
            add_entry_to_CSV(exercise_input, sets_input, rep_input,
                             weight_input, date_input)
        elif choice == 'add':
            # Call function to add exercise
            exercise_input, sets_input, rep_input, weight_input, date_input = add_exercise(
            )
            add_entry_to_CSV(exercise_input, sets_input, rep_input,
                             weight_input, date_input)
        elif choice == '2':
            # Call function to calculate average lift
            average_lift()
        elif choice == 'Avg':
            # Call function to calculate average lift
            average_lift()
        elif choice == 'Average':
            # Call function to calculate average lift
            average_lift()
        elif choice == 'average':
            # Call function to calculate average lift
            average_lift()
        elif choice == '3':
            plot_exercise_data(file_path)
        elif choice == 'Graph':
            plot_exercise_data(file_path)
        elif choice == 'graph':
            plot_exercise_data(file_path)
        elif choice == '4':
            print("Exiting the program.")
            break  # Exit the program
        elif choice == 'Exit':
            print("Exiting the program.")
            break  # Exit the program
        elif choice == 'exit':
            print("Exiting the program.")
            break  # Exit the program
        else:
            print("Invalid option. Please try again.")


# Main function to execute the program
def main():
    display_menu()


# Call the main function
if __name__ == "__main__":
    main()

#Add section here to be able to test one function without having to go through the whole program??
