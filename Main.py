#Difficulty Level so I know what order to go 1,2,3,4,5  (5 being hardest)

#Steps for Project
#1st - Get the project to work so I can manually type in the data and it saves to the CSV
#2nd - script works so that I can select different things to view from the command line and not just the CSV
#2b - Save the file in two spots in case of any issues with modifying the file(Do that in the script)
#3rd - Make the sheet be able to be sorted or filtered so it can be a graph (Multiple sheets)?
#4th - Make the graph look pretty so it can be easily read
#5th - Think of some sort of authentication step to build into it(Just for me to authenticate)
#6th - Think of how to have other users use it (Marty)
#7th - Any other ideas for it?


####TO DO

#First have the file upload to Google Drive
#Second add some actual real data to work with
#Third clean up all comments and make this mess easier to Read
#Along with updating the readme
#Have the file in Google Drive so I always have it
#Input validation everywhere



#How to Update FILE PATH
'''
import gdown

# Step 1: Define the Google Drive file ID
file_id = 'YOUR_GOOGLE_DRIVE_FILE_ID'  # Replace with your file ID

# Step 2: Generate the download URL using the file ID
url = f'https://drive.google.com/uc?export=download&id={file_id}'

# Step 3: Download the file to the local environment
output = 'WorkoutLog.csv'  # You can name the downloaded file here
gdown.download(url, output, quiet=False)

# Step 4: Now you can use this file just like a local file
file_path = 'WorkoutLog.csv'

# Your code can now continue working with the file

'''

#Difficult/Future Tense
#Allow the script to be run from my phone to enter data there

#Import Statements
#Error popup just means it has not been used, its for getting the time of the input
#import pandas as pd for when we do graphs and stuff
import time
import csv
import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime


print("Welcome to Lee's Workout Tracker!")

file_path = 'WorkoutLog.csv'


#This section is for adding a lift (Sets,Reps,Weight,etc) (Difficulty 1)
#def is how you use python to write things (Functions)
#For this function I need to get user input and have them type in the following information:
#Exercise, Sets, Reps, and Weight (Starting simple)

def add_exercise():
    # Predefined list of exercises
    exercises = [
        "Squat",
        "Pause Squat",
        "Goblet Squat",
        "Pause Bench",
        "Touch N Go Bench",
        "Incline DB Bench",
        "Deadlift",
        "Deficit Deadlift",
        "Romanian Deadlift",
        "Overhead Press",
        "Overhead DB Press"


    ]

    # Print the list of exercises
    print("List of Exercises to choose from:")
    #For loop to print each exercise to the console
    for exercise in exercises:
        print(exercise)

   # user_input =  input("Enter an exercise from the list above: ")

# Validate user input against the list of exercises

# Set the maximum number of attempts
    max_attempts_lift = 3
    attempts_lift = 0
    while attempts_lift < max_attempts_lift:
        exercise_input = input("\nEnter the name of the exercise: ")

        if exercise_input in exercises:
            print(f"You've selected: {exercise_input}")
            break  # Exit the loop if the input is valid
        else:
            attempts_lift += 1
            print(f"Invalid exercise. You have {max_attempts_lift - attempts_lift} attempt(s) left to type it correctly.")

    if attempts_lift == max_attempts_lift:
        print("You've exceeded the maximum number of attempts. Please try again later idiot.")
    max_attempts_sets = 3
    attempts_sets = 0
    
    while attempts_sets < max_attempts_sets:
        sets_input = input("Enter the amount of sets done(Weight will be select once):")
        if sets_input.isdigit():
            print(f"You said you did this many sets: {sets_input}")
            break
        else:
            attempts_sets += 1
            print(f"You need to enter only digits. Try again. {max_attempts_sets - attempts_sets} tries left. ")
    if attempts_sets == max_attempts_sets:
        print("You've exceeded the maximum number of attempts. Please try again later idiot.")

    max_attempts_reps = 3
    attempts_reps = 0

    while attempts_reps < max_attempts_reps:
        rep_input = input("Enter the number of reps done: ")
        if rep_input.isdigit():
            print(f"You said you did this many reps: {rep_input}")
            break
        else:
            attempts_reps += 1
            print(f"You need to enter only digits. Try again. {max_attempts_reps - attempts_reps} tries left.")

    if attempts_reps == max_attempts_reps:
        print("You've exceeded the maximum number of attempts. Please try again later, idiot.")

    max_attempts_weight = 3
    attempts_weight = 0

    while attempts_weight < max_attempts_weight:
        weight_input = input("Enter the amount of weight done(in pounds): ")
        if weight_input.isdigit():
            print(f"You said you did this much weight: {weight_input}")
            break
        else:
            attempts_weight += 1
            print(f"You need to enter only digits. Try again. {max_attempts_weight - attempts_weight} tries left.")

    if attempts_weight == max_attempts_weight:
        print("You've exceeded the maximum number of attempts. Please try again later, idiot.")
#Prints the user output to see what they entered


    date_input = input("Enter the date of this lift(MM/DD/YY): ")
    
    
    print(f"The date {date_input} is invalid.")
    
    print(f"Exercise: {exercise_input} \nSets: {sets_input}  \nReps Completed: {rep_input} \nWeight Used: {weight_input}lbs Date Entered: {date_input} ")

    return exercise_input, sets_input, rep_input, weight_input, date_input



#Runs the function, can comment this out when testing another section
#add_exercise()

#This section is for writing the data that was entered to the CSV file
#Needs to get the user input and add it to the file (Diffculty: 3)

def add_entry_to_CSV(exercise_input, sets_input, rep_input, weight_input, date_input):
    print ("Test function to make sure we in right spot")
    #new_entry = ['Squat', '3', '5', '225'] #Add in data from above for this, hardcoded now for testing
    new_entry = [exercise_input, sets_input, rep_input, weight_input, date_input]
    file_path = os.path.join('WorkoutLog.csv')
        
    with open(file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        
        # Write the new entry to the CSV file
        writer.writerow(new_entry)
        
    print("New entry added to WorkoutLog.csv")

# Call the function to test
#add_entry_to_CSV()

#Average a lift - May eventually delete but it can prove useful for now for practice

# Function to calculate the average weight lifted for a specific exercise
#Gets average weight per rep
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
        
        for row in reader:
            exercise, sets, reps, weight = row
            if exercise == exercise_to_avg:
               # total_entries += 1
                total_weight += float(weight) * int(reps) * int(sets)  # Assuming weight is in pounds
    # Add the total number of reps (sets * reps) to total_reps
                total_reps += int(reps) * int(sets)
    # Calculate and display the average
    if total_reps > 0:
        avg_weight_per_rep = total_weight / total_reps
        print(f"The average weight lifted per rep for {exercise_to_avg} is: {avg_weight_per_rep:.2f} lbs")
    else:
        print(f"No entries found for {exercise_to_avg}.")

#Uncomment to test function if we need to add stuff
#average_lift()
#Function to read workout logs that are already in CSV file Function above needs completion first (Diffculty: 4)

def plot_exercise_data(file_path):
    """
    Reads exercise data from a CSV file and plots a line graph showing the weight lifted per set
    for each exercise, over time.

    Args:
    - csv_file (str): The path to the CSV file containing the exercise data.
    """
    # Step 1: Read the data from the CSV file
    exercises = {}  # To store data for each exercise

    with open(file_path, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        # Step 2: Process each row
        for row in reader:
            
            # Check if the Date field is not empty
            date_str = row['Date']
            if date_str:  # Only process if the Date is not empty
                try:
                    # Parse the date from the MM/DD/YY format
                    date = datetime.strptime(date_str, '%m/%d/%y')
                except ValueError:
                    print(f"Warning: Invalid date format in row: {row}")
                    continue  # Skip this row if the date is invalid
            else:
                print(f"Warning: Empty date in row: {row}")
                continue  # Skip this row if the date is empty
            
            
            exercise = row['Exercise']
            weight = float(row['Weight'])
            reps = int(row['Reps'])  # Number of reps for the set
            set_number = int(row['Sets'])  # Track each set number individually
            
            # Initialize a list for the exercise if it doesn't exist
            if exercise not in exercises:
                exercises[exercise] = {'dates': [], 'weights': [], 'reps': [], 'set_numbers': []}
            
            # Append the data for this set
            exercises[exercise]['dates'].append(date)
            exercises[exercise]['weights'].append(weight)
            exercises[exercise]['reps'].append(reps)
            exercises[exercise]['set_numbers'].append(set_number)

    # Step 3: Plot a line graph for each exercise
    plt.figure(figsize=(10, 6))  # Optional: Set the figure size

    for exercise, data in exercises.items():
        # Plot each set individually
        plt.plot(data['dates'], data['weights'], marker='o', label=f"{exercise} (Set)")


# Add annotations for the number of reps on each set
    for i, date in enumerate(data['dates']):
            plt.annotate(f"{data['reps'][i]} reps", 
                        (data['dates'][i], data['weights'][i]),
                        textcoords="offset points",
                        xytext=(0, 5),  # Offset the text slightly to avoid overlap
                        ha='center')
    # Adding title and labels
    plt.title("Weight Lifted Per Set Over Time")
    plt.xlabel("Date")
    plt.ylabel("Weight (kg)")
    plt.xticks(rotation=45)  # Rotate date labels for readability
    plt.legend(title="Exercise")

    # Display the plot
    plt.tight_layout()  # Optional: Adjust the layout to prevent overlap
    plt.show()

# Example usage:
# plot_exercise_data('exercise_log.csv')  # Call this function with your CSV file


#Display Menu (Difficulty 1)

# Function to display the menu and handle user selection
#Will want to update this later to not have a million if else, works for now though
def display_menu():
    while True:
        print("\n--- Workout Log Menu ---")
        print("1. Add Exercise Entry")
        print("2. Calculate Average Lift")
        print("3. Graph it!")
        print("4. Exit")
        
        choice = input("Select an option (1, 2, or 3): ")
        
        if choice == '1':
            # Call function to add exercise
            exercise_input, sets_input, rep_input, weight_input, date_input = add_exercise()
            add_entry_to_CSV(exercise_input, sets_input, rep_input, weight_input,date_input)
        elif choice == 'Add':
            # Call function to add exercise
            exercise_input, sets_input, rep_input, weight_input, date_input = add_exercise()
            add_entry_to_CSV(exercise_input, sets_input, rep_input, weight_input, date_input)
        elif choice == 'add':
            # Call function to add exercise
            exercise_input, sets_input, rep_input, weight_input, date_input = add_exercise()
            add_entry_to_CSV(exercise_input, sets_input, rep_input, weight_input, date_input)
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

# Function to display the menu

#Main program loop (difficulty 1) (Else if statement to pick what other function to do)

# Main function to execute the sequence

# Main function to execute the program
def main():
    display_menu()

# Call the main function
if __name__ == "__main__":
    main()