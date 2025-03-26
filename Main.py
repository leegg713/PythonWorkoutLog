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
        "Overhead DB Press",
    ]


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