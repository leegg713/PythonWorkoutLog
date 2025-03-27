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


print("Welcome to Python programming!")
#This is comment that is used to test staging to my project      
#Second stage testing

#Need validation so that typos are not made, will need a list of exercises that can be entered (Not case sensitive)
#This will also need a list of exercises that I can enter, pulling list from ChatGPT
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
        user_input = input("\nEnter the name of the exercise: ")

        if user_input in exercises:
            print(f"You've selected: {user_input}")
            break  # Exit the loop if the input is valid
        else:
            attempts_lift += 1
            print(f"Invalid exercise. You have {max_attempts_lift - attempts_lift} attempt(s) left to type it correctly.")

    if attempts_lift == max_attempts_lift:
        print("You've exceeded the maximum number of attempts. Please try again later idiot.")
    max_attempts_sets = 3
    attempts_sets = 0
    
    while attempts_sets < max_attempts_sets:
        user_input = input("Enter the amount of sets done(Weight will be select once):")
        if user_input.isdigit():
            print("You entered a number. Good job!")
            break
        else:
            attempts_sets += 1
            print(f"You need to enter only digits. Try again. {max_attempts_sets - attempts_sets} tries left. ")
    if attempts_sets == max_attempts_sets:
        print("You've exceeded the maximum number of attempts. Please try again later idiot.")

    max_attempts_reps = 3
    attempts_reps = 0

    while attempts_reps < max_attempts_reps:
        user_input = input("Enter the number of reps done: ")
        if user_input.isdigit():
            print("You entered a valid number of reps. Good job!")
            break
        else:
            attempts_reps += 1
            print(f"You need to enter only digits. Try again. {max_attempts_reps - attempts_reps} tries left.")

    if attempts_reps == max_attempts_reps:
        print("You've exceeded the maximum number of attempts. Please try again later, idiot.")

    max_attempts_weight = 3
    attempts_weight = 0

    while attempts_weight < max_attempts_weight:
        user_input = input("Enter the amount of weight done: ")
        if user_input.isdigit():
            print("You entered a number. Good job weak lil boy!")
            break
        else:
            attempts_weight += 1
            print(f"You need to enter only digits. Try again. {max_attempts_weight - attempts_weight} tries left.")

    if attempts_weight == max_attempts_weight:
        print("You've exceeded the maximum number of attempts. Please try again later, idiot.")

#Runs the function
get_exercise()
#This section is for adding a lift (Sets,Reps,Weight,etc) (Difficulty 1)
#def is how you use python to write things (Functions)
#For this function I need to get user input and have them type in the following information:
#Exercise, Sets, Reps, and Weight (Starting simple)






#This section is for creating/getting the csv file (Headers just like in powershell) (Difficulty 2)
#Log entry, file spot, file creation





#This section is for writing the data that was entered to the CSV file
#Needs to get the user input and add it to the file (Diffculty: 3)


#Function to read workout logs that are already in CSV file Function above needs completion first (Diffculty: 4)


#Display Menu (Difficulty 1)

# Function to display the menu
#Block comment for now, best practice to just comment using ###
""""
def display_menu():
    print("\n--- Workout Log ---")
    print("1. Add Workout Entry")
    print("2. View Workout Logs")
    print("3. Exit")
"""

#Main program loop (difficulty 1) (Else if statement to pick what other function to do)

#def main():

# Run the program
# main()