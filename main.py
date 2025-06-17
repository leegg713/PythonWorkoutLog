####TO DO### 

#Plate Calculator -- You want 135 on the bar... what weights are needed in either kg or lbs -- Completed
#Eventually make it so that when its a visual app you can use either plate
#Test function first
#After it works, add to display menu section
#Exercise Frequency - How often a week you train each exercise
#Date format validation - Ensure consistent date entry
#Create new branch

#Date format validation - Ensure consistent date entry
#One Rep Max to work in KILOS or LBS
#Date format validation - Ensure consistent date entry

#Rest timer - Built-in countdown timer between sets -- Can be used on the app directly eventually -- Build this next

#Function page and main page seperated?? When we make this an app for real probably need to do that

#Edit function to change an old entry --- Would need date, lift, sets, reps, weight to do it --- Can be a point and click maybe????

#Better Visualizations --- More difficult - Do after 100 days Python completed
#May want to not use matplotlib and may want something else???
#Multiple exercise comparison - Graph multiple lifts on same chart
#Volume vs strength trends - Compare total volume against max weights
#Weekly/monthly summaries - Aggregate data views
#Exercise distribution pie charts - See training balance

#Import Statements
import time  #Used for adding delays to the script if needed
import csv  #Used to import the CSV
import os  #Used to import the file path for the CSV and other useful functions
import pandas as pd #Used to get a dataframe for the graph
import matplotlib.pyplot as plt  #Used to plot the graph
import datetime as datetime
from utils.calc import wilks, dots, one_rep_max, plate_calculator, average_lift
from utils.helpers import get_valid_number_input, convert_iso_to_mmddyy, clear_last_entry, add_exercise
from utils.visualizations import plot_exercise_data

#Global variables - Not going to change
file_path = 'WorkoutLog.csv'

    ########## MENU FUNCTION ########
def display_menu():
    print("Welcome to Lee's Workout Tracker!")
    while True:
        print("\n--- Workout Log Menu ---")
        print("1. Add Exercise Entry")
        print("2. Calculator")
        print("3. Graph it!")
        print("4. Clear last entry")
        print("5. Exit")

        choice = input("Select an option (1, 2, 3, 4, or 5): ")

        choice_lower = choice.lower() #Sets the selection to lower if the user enters a word instead of 1,2,3,4,5

        if choice == '1' or choice_lower == 'add':
            add_exercise()

        elif choice == '2' or choice_lower in ['avg', 'average', 'calculator', 'calc']:
            calculator()

        elif choice == '3' or choice_lower == 'graph':
            plot_exercise_data()

        elif choice == '4' or choice_lower in ['clear', 'remove']:
            clear_last_entry()

        elif choice == '5' or choice_lower == 'exit':
            print("Exiting the program.")
            break

# Main function to execute the program
def main():
    display_menu()


# Call the main function
if __name__ == "__main__":
    main()

