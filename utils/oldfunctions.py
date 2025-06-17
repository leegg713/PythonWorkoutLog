#These functions are not needed for flask app but I want to keep the code in case I need it for something

'''

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
'''

'''
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


    '''

    '''
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
        return {
        "exercise": exercise_to_avg,
        "average": round(avg_weight_per_rep, 2),
        "total_reps": total_reps
        }
    else:
        print(f"No entries found for {exercise_to_avg}.")
        #print(f"No avg weight per rep found: {avg_weight_per_rep}")
        time.sleep(5)
        os.system("clear")
        return {"error": f"No entries found for {exercise_to_avg}"}

        '''

    '''
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

    '''   

    '''
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
'''

'''
def one_rep_max():
    print("1 rep max calculator")
    weight = float(input("Enter the weight used: "))
    reps = float(input("Enter the reps completed: "))
    max = round(weight * reps**0.1, 2) #Rounds to 2 decimal points
    print(f"Your estimated 1 rep max is {max}")
    time.sleep(5)
    os.system("clear")
'''

'''
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
'''

'''
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

        '''
'''
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

'''
