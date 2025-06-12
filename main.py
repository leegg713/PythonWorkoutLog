####TO DO### 

#Plate Calculator -- You want 135 on the bar... what weights are needed in either kg or lbs -- Completed
#Eventually make it so that when its a visual app you can use either plate
#Test function first
#After it works, add to display menu section
#Exercise Frequency - How often a week you train each exercise
#Date format validation - Ensure consistent date entry
#Create new branch
'''
Now you can access the exercise frequency analysis by:

Going to the Calculator menu (option 2)
Typing "frequency" when prompted
The analysis will show you:

Total sets performed for each exercise
Days trained for each exercise
Frequency per week for each exercise
Training insights including most/least trained exercises
Recent activity showing what you've trained in the last 2 weeks

'''
#Date format validation - Ensure consistent date entry
#One Rep Max to work in KILOS or LBS
#Date format validation - Ensure consistent date entry

#Rest timer - Built-in countdown timer between sets -- Can be used on the app directly eventually

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



#Global variables - Not going to change
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

################# Function to get weight and total in kgs and lbs ###################
#Used for calculator functions

def get_weight_total():
    type = input("Enter lbs or kgs: ").strip().lower()
    if type == "lbs":
        weight_lbs = float(input("Enter your body weight in pounds: "))
        total_lbs = float(input("Enter your total for the big 3 lifts in pounds(squat,bench,deadlift) "))
        total_kg = total_lbs * 0.45359237
        weight_kg = weight_lbs * 0.45359237
    else:
        weight_kg = float(input("Enter your body weight in kilograms: "))
        total_kg = float(input("Enter your total for the big 3 lifts in kilograms (squat, bench, deadlift): "))
        weight_lbs = weight_kg / 0.45359237
        total_lbs = total_kg / 0.45359237

    return weight_kg, total_kg, weight_lbs, total_lbs

############# Function to add lift to the CSV ###################
def add_exercise():
    time.sleep(0.5)
    os.system("clear")
    exercises = [
        "Squat", "PauseSquat", "GobletSquat", "PauseBench",
        "TouchNGoBench", "InclineDBBench", "Deadlift", "DeficitDeadlift",
        "RomanianDeadlift", "OverheadPress", "OverheadDBPress", "Bench"
    ]

    print("List of Exercises to choose from:")
    for exercise in exercises:
        print(exercise)
        
    #exercise_input = None

    exercise_input = input("\nEnter the name of the exercise (or press Enter to use previous): ").strip().replace(" ", "")

    if exercise_input == "":
        # User wants to reuse last exercise
        try:
            with open(file_path, "r") as file:
                last_line = list(csv.reader(file))[-1]
                exercise_input = last_line[0]  # Assumes the first column is the exercise name
                print(f"Using previous exercise: {exercise_input}")
        except Exception:
            print("No previous exercise found. Please enter the exercise manually next time.")
            return
    else:
        # User typed something — validate it
        for exercise in exercises:
            if exercise.lower().replace(" ", "") == exercise_input.lower():
                print(f"You've selected: {exercise}")
                time.sleep(0.5)
                os.system("clear")
                exercise_input = exercise
                break
        else:
            print("Invalid exercise entered and no fallback option used.")
            return

    # Get sets, reps, weight by using the get_valid_number_input function
    sets_input = get_valid_number_input("Sets > ", field_name="Sets", max_attempts=3, clear_screen=True)
    rep_input = get_valid_number_input("Reps > ", field_name="Reps", max_attempts=3, clear_screen=True)
    weight_input = get_valid_number_input("Weight > ", field_name="Lbs", max_attempts=3, clear_screen=True)

    while True:
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
        try:
            # Try to parse input date to validate format --Makes the date have to be MM/DD/YY
            datetime.datetime.strptime(date_input, "%m/%d/%y")
            break  # valid format, exit loop
        except ValueError:
            print("Invalid date format. Please enter date as MM/DD/YY.")
    time.sleep(1)
    os.system("clear")

    print(f"Exercise: {exercise_input}\nSets: {sets_input}\nReps: {rep_input}\nWeight: {weight_input} lbs\nDate: {date_input}")

    # Adds the entry to the CSV (Appends == 'a')
    new_entry = [exercise_input, sets_input, rep_input, weight_input, date_input]
    with open(file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(new_entry)

    print(f"New Lift added to {file_path}")
    time.sleep(2)
    os.system("clear")

############# Lift Average ###########
def average_lift():
    time.sleep(0.5)
    os.system("clear")
    exercise_to_avg = input("Enter the exercise you want to calculate the average weight for: ")
    #file_path = 'WorkoutLog.csv'
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

########### Get WILKS Score Function ###############
def wilks():
    
    os.system("clear")
    print("Wilks Calculator for Men")
    #get_weight_total()
    result = get_weight_total()
    if not result:
        return  # If invalid input, exit function

    weight_kg, total_kg, weight_lbs, total_lbs = result # The order the values are returned in from the function and this unpacks the variables vs setting it equal to result
    a = -216.0475144
    b = 16.2606339
    c = -0.002388645
    d = -0.00113732
    e = 7.01863E-06 # equivalent to 7.01863 x 10^-6
    f = -1.291E-08 # equivalent to -1.291 × 10^-8
    coefficient =  500 / (a + b*(weight_kg) + c*(weight_kg**2) + d*(weight_kg**3) +  e*(weight_kg**4) + f*(weight_kg**5))
    wilks = round(total_kg * coefficient, 2) #Rounds the score to 2 decimal points
    print(f"\nYour Wilks score is {round(wilks,2)}")
    print(f"Body weight: {round(weight_kg, 2)} kg ({round(weight_lbs, 2)} lbs)")
    print(f"Total lift: {round(total_kg, 2)} kg ({round(total_lbs, 2)} lbs)")
    time.sleep(10)
    os.system("clear")

####### Get DOTS Score Function ######
def dots():
    print("Dots Calculator")
    #get_weight_total()
    result = get_weight_total()
    if not result:
        return  # If invalid input, exit function

    weight_kg, total_kg, weight_lbs, total_lbs = result # The order the values are returned in from the function and this unpacks the variables vs setting it equal to result
    a = -307.75076
    b = 24.0900756
    c = -0.1918759221
    d = 0.0007391293
    e = -0.000001093
    coefficient = (a + b*(weight_kg) + c*(weight_kg**2) + d*(weight_kg**3) +  e*(weight_kg**4))
    dots_score = (500 / coefficient) * total_kg
    print(f"\nYour DOTS score is {round(dots_score, 2)}") #Rounds to 2 decimal points
    print(f"Body weight: {round(weight_kg, 2)} kg ({round(weight_lbs, 2)} lbs)")
    print(f"Total lift: {round(total_kg, 2)} kg ({round(total_lbs, 2)} lbs)")
    time.sleep(10)
    os.system("clear")

########### One Rep Max Estimate Function ###################
def one_rep_max():
    print("1 rep max calculator")
    weight = float(input("Enter the weight used: "))
    reps = float(input("Enter the reps completed: "))
    max = round(weight * reps**0.1, 2) #Rounds to 2 decimal points
    print(f"Your estimated 1 rep max is {max}")
    time.sleep(5)
    os.system("clear")

########### Plate Calculator Function #######################
def plate_calculator():
    print("Using a standard 20KG/45LB barbell... get the plates needed to get your desired weight")
    weight_type = input("LBs or Kilos? ").strip().lower()
    while True:
        desired_weight = float(input("Enter the weight you want to lift: ")) #Float for 2.5 plate calculations to work
        if desired_weight % 5 != 0:
            print("Weight entered must end in a 5 or 0 for calculator to work... try again!")
            continue
        else:
            break
    #LBS SECTION
    if weight_type in ['lbs', 'lb', 'pounds', 'pound']:
        print("Do this for lbs")

        weight_for_plates = desired_weight - 45 #Subtracts bar weight of 45

        if weight_for_plates < 0:
            print("Weight is less than the barbell weight!")
            return

        # Weight per side (divide by 2 since plates go on both sides)
        weight_per_side = weight_for_plates / 2
        remaining_weight = weight_per_side
        # Calculate plates needed per side (only whole numbers)
        fourty_five_plates = int(weight_per_side // 45)
        remaining_weight = weight_per_side % 45
        print(f"Weight left per side: {remaining_weight}") #For testing
        twenty_five_plates = int(remaining_weight // 25)
        remaining_weight = remaining_weight % 25
        print(f"Weight left per side after 25s: {remaining_weight}") #For testing
        ten_plates = int(remaining_weight // 10)
        remaining_weight = remaining_weight % 10
        five_plates = int(remaining_weight // 5)
        remaining_weight = remaining_weight % 5
        two_and_half_plates = int(remaining_weight // 2.5)
        
        print(f"You will need {fourty_five_plates} 45(s),{twenty_five_plates} 25(s), {ten_plates} 10(s), {five_plates} 5(s) and {two_and_half_plates} 2.5(s) per side")

    #KILO SECTION
    elif weight_type in ['kgs', 'kg', 'kilos', 'kilo', 'kilogram', 'kilograms']:
        print("Do this for kgs")

        weight_for_plates = desired_weight - 20 #Subtracts bar weight of 20KG

        if weight_for_plates < 0:
            print("Weight is less than the barbell weight!")
            return

        # Weight per side (divide by 2 since plates go on both sides)
        weight_per_side = weight_for_plates / 2
        remaining_weight = weight_per_side
        # Calculate plates needed per side (only whole numbers)
        #print(f"Weight left per side: {remaining_weight}") #For testing
        twenty_five_plates = int(remaining_weight // 25)
        remaining_weight = remaining_weight % 25
        #print(f"Weight left per side after 25s: {remaining_weight}") #For testing
        twenty_plates = int(remaining_weight // 20)
        remaining_weight = remaining_weight % 20
        fifteen_plates = int(remaining_weight // 15)
        remaining_weight = remaining_weight % 15
        ten_plates = int(remaining_weight // 10)
        remaining_weight = remaining_weight % 10
        five_plates = int(remaining_weight // 5)
        remaining_weight = remaining_weight % 5
        two_and_half_plates = int(remaining_weight // 2.5)
        remaining_weight = remaining_weight % 2.5
        one_and_point_two_five_plates = int(remaining_weight // 1.25)
        print(f"You need {twenty_five_plates} 25(s), {twenty_plates} 20(s), {fifteen_plates} 15(s), {ten_plates} 10(s), {five_plates} 5(s), {two_and_half_plates} 2,5(s), and {one_and_point_two_five_plates} 1.25(s) on each side")
        
    else:
        print("Invalid input selected... returning to main menu")
        return

############## Exercise Frequency Function ##################
def exercise_frequency():

    '''
    Total sets performed for each exercise - Completed
    Total reps performed for each exercise - Completed
    Days trained for each exercise - Completed
    Frequency per week for each exercise -- WIP
    Training insights including most/least trained exercises -- WIP
    Recent activity showing what you've trained in the last 2 weeks -- WIP

    '''
    # Read the CSV into a DataFrame
    df = pd.read_csv(file_path)

    # Normalize the 'Exercise' column to lowercase for consistent comparison
    df['Exercise'] = df['Exercise'].str.strip().str.lower()

    # Ask the user for a lift
    lift = input("Enter the lift to get frequency for: ").strip().lower()

    # Filter rows matching the lift
    lift_df = df[df['Exercise'] == lift].copy() #Need the copy for no error

    # Check if anything matched
    if lift_df.empty:
        print(f"'{lift}' not found in {file_path}")
    else:
        # Total sets Instead of index you can use the name of the column
        total_sets = lift_df['Sets'].astype(int).sum()

        # Total reps (sets × reps per row, then sum)
        lift_df['Reps'] = lift_df['Reps'].astype(int)
        lift_df['Sets'] = lift_df['Sets'].astype(int)
        lift_df['TotalReps'] = lift_df['Sets'] * lift_df['Reps']
        total_reps = lift_df['TotalReps'].sum()

        # Print dates where lift was done
        date_count = 0
        print("Dates this lift was performed:")
        for date in lift_df['Date']:
            unique_dates = set(lift_df['Date'])
            date_count = len(unique_dates)
            #print(f"Total Unique Days for {lift.capitalize()}: {date_count}")

        # Final output
        print(f"\nTotal Sets for {lift.capitalize()}: {total_sets}")
        print(f"Total Reps for {lift.capitalize()}: {total_reps}")
        print(f"Total Different Days for {lift.capitalize()}: {date_count}")


    
    '''
    CSV READER VERSION OUTDATED GOING TO USE PANDAS TO LEARN IT
    #User select a lift
    #Get the info based on the lift
    #Output the info
    lift = input("Enter the lift you want to get frequency for: ").strip().lower() # Will have to see if this actually pulls the right data
    # Read the CSV file and calculate the total weight for the selected exercise
    found = False  # Track if we find a match
    total_sets = 0
    total_reps = 0
    df =pd.read_csv('MYDATA.csv') #Reads CSV for 
    with open(file_path, mode='r') as file:
        reader = csv.reader(file)
        # convert strings to datetimes
        reader['recvd_dttm'] = pd.to_datetime(df['recvd_dttm'])

        # get first and last datetime for final week of data
        range_max = df['recvd_dttm'].max()
        range_min = range_max - dt.timedelta(days=7)

        # take slice with final week of data
        sliced_df = df[(df['recvd_dttm'] >= range_min) & 
                       (df['recvd_dttm'] <= range_max)]
        
        # Skip the header row if there is one
        next(reader, None)  # Skip the header row (if there is one)
        #Reads the file to get the data needed
        for row in reader:
            exercise = row[0].strip().lower()
            if lift == exercise:
                #print(row) #Test output for whole row #Prints whole row
                #print(f"Lift: {row[0]}") #For just first index in row #Prints just Squat
                #print(f"Sets: {row[1]}") #Sets 
                set = int(row[1])
                total_sets += set
                #print(f"Reps: {row[2]}") #Reps
                rep = int(row[2])
                total_reps += rep*set
                #print(f"Weight: {row[3]}") #Weight used
                date = row[4]
                print(date)
                found = True
            # After loop ends, check if nothing was found
    if not found:
        print(f"'{lift}' not found in {file_path}")
    elif found:
        print(f"Total Sets for {lift.capitalize()}: {total_sets}")
        print(f"Total Reps for {lift.capitalize()}: {total_reps}")

'''

########### Menu to use different calculators ##############
def calculator():
    os.system("clear")
    print("Calculator Page")
    print("Options are Average, WILKS, DOTS, 1RM, Plate Calculator ")
    print("\n--- Calculator Menu ---")
    print("1. Average")
    print("2. WILKS")
    print("3. DOTS")
    print("4. 1RM")
    print("5. Plate Calculator")
    print("6. Exercise Frueqency")

    choice = input("Select an option (1, 2, 3, 4, 5, or 6): ").strip().lower()
    time.sleep(1)
    os.system("clear")
    if choice == "average" or choice == "1":
        average_lift()
    elif choice == "wilks" or choice == "2":
        wilks()
    elif choice == "dots" or choice == "3":
        dots()
    elif choice == "1rm" or choice == "4":
        #print("1RM calculator")
        one_rep_max()
    elif choice == "platecalculator" or choice == "5":
    #print("1RM calculator")
        plate_calculator()
    elif choice == "frequency" or choice == "6":
    #print("1RM calculator")
        exercise_frequency()
    else:
        print("Nothing valid selected... clearing page and returning to main menu")
        time.sleep(3)
        os.system("clear")

########## GRAPH Function #########
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
    #plt.show()
    #Needed for script to continue after plotting
    plt.show(block=False)
    plt.pause(0.001)
    
    time.sleep(3)
    os.system("clear")

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

