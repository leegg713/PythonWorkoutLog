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

#Import Statements
#Error popup just means it has not been used, its for getting the time of the input
#import pandas as pd for when we do graphs and stuff
import time
import csv
import os


print("Welcome to Lee's Workout Tracker!")


#This section is for adding a lift (Sets,Reps,Weight,etc) (Difficulty 1)
#def is how you use python to write things (Functions)
#For this function I need to get user input and have them type in the following information:
#Exercise, Sets, Reps, and Weight (Starting simple)

def get_exercise():
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

    print(f"Exercise: {exercise_input} \nSets: {sets_input}  \nReps Completed: {rep_input} \nWeight Used: {weight_input}lbs ")

#Runs the function, can comment this out when testing another section
#get_exercise()

#This section is for creating/getting the csv file (Headers just like in powershell) (Difficulty 2)
#Log entry, file spot, file creation

def add_entry_to_CSV():
    print ("Test function to make sure we in right spot")
    new_entry = ['Squat', '3', '5', '225'] #Add in data from above for this, hardcoded now for testing
    #new_entry = [exercise_input, sets_input, rep_input, weight_input]
    file_path = os.path.join('WorkoutLog.csv')
        
    with open(file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        
        # Write the new entry to the CSV file
        writer.writerow(new_entry)
        
    print("New entry added to WorkoutLog.csv")

# Call the function to test
add_entry_to_CSV()


#This section is for writing the data that was entered to the CSV file
#Needs to get the user input and add it to the file (Diffculty: 3)


#Function to read workout logs that are already in CSV file Function above needs completion first (Diffculty: 4)


#Display Menu (Difficulty 1)

# Function to display the menu

#Main program loop (difficulty 1) (Else if statement to pick what other function to do)

