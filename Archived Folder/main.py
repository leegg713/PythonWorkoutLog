### TO DO #####
#MARK A PR FUNCTION
# -- Checks the highest weight for that lift and then outputs a message to the screen -- Can make it in only python first before flask version
'''
Data Storage
You’re currently using CSV — that can work initially but consider migrating to a database like SQLite or PostgreSQL for:

Multi-user support

Concurrent access

Easier queries and edits
'''

'''
5. User Accounts & Authentication
Add user login/signup so different people can keep their own logs.

Flask-Login or Django’s built-in auth make this easier.'''

'''
 Hosting
Deploy on cloud platforms like:

Heroku (easy Flask/Django deploy)

Render, AWS, DigitalOcean, or Google Cloud

Make sure file paths and persistent storage are handled properly.

'''

#Import Statements
import time  #Used for adding delays to the script if needed
import csv  #Used to import the CSV
import os  #Used to import the file path for the CSV and other useful functions
import pandas as pd #Used to get a dataframe for the graph
import matplotlib.pyplot as plt  #Used to plot the graph
import datetime as datetime
from utils.calc import wilks, dots, one_rep_max, plate_calculator, average_lift
from utils.helpers import get_valid_number_input, convert_iso_to_mmddyy, clear_last_entry, add_exercise
#from utils.visualizations import create_line_graph

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
            #ADD GRAPH FUNCTIONS FROM VISUALIZATIONS HERE#
            print()
            

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

