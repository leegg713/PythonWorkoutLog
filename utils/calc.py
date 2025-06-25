import os
import csv
import time
import datetime

file_path = "WorkoutLog.csv"

###### LIFT AVERAGE FLASK VERSION #########

def average_lift(exercise_to_avg):
    exercise_to_avg = exercise_to_avg.strip().replace(" ", "").lower()  # normalize input to lower to check the CSV
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
            if exercise.lower() == exercise_to_avg:  #Check to see if user input matches an exercise in the CSV -- Sets to lower to match exercise_to_avg form submission
                total_weight += float(weight) * int(reps) * int(sets)  # Gets weight in lbs
                total_reps += int(reps) * int(sets)# Add the total number of reps (sets * reps) to total_reps
    # Calculate and display the average

    
    if total_reps > 0:
        avg_weight_per_rep = total_weight / total_reps
        return {
        "exercise": exercise_to_avg,
        "average": round(avg_weight_per_rep, 2),
        "total_reps": total_reps
        }
    else:
        return {"error": f"No entries found for {exercise_to_avg}"}



##### WILKS CALCULATOR FLASK VERSION ########

def wilks(bodyweight_lbs, total_lift_lbs):
    # Convert pounds to kilograms
    weight_kg = bodyweight_lbs * 0.453592
    total_kg = total_lift_lbs * 0.453592

    # Wilks formula coefficients (for men)
    a = -216.0475144
    b = 16.2606339
    c = -0.002388645
    d = -0.00113732
    e = 7.01863E-06
    f = -1.291E-08

    coefficient = 500 / (a + b*weight_kg + c*(weight_kg**2) +
                         d*(weight_kg**3) + e*(weight_kg**4) + f*(weight_kg**5))
    wilks_score = round(total_kg * coefficient, 2)
    return wilks_score


##### GET DOTS SCORE FLASK VERSION ##### 
def dots(bodyweight_lbs, total_lift_lbs): #Passes these 2 parameters 
    # Convert pounds to kilograms
    weight_kg = bodyweight_lbs * 0.453592
    total_kg = total_lift_lbs * 0.453592
    a = -307.75076
    b = 24.0900756
    c = -0.1918759221
    d = 0.0007391293
    e = -0.000001093
    coefficient = (a + b*(weight_kg) + c*(weight_kg**2) + d*(weight_kg**3) +  e*(weight_kg**4))
    dots_score = (500 / coefficient) * total_kg
    dots_score = round(dots_score,2)
    return dots_score #Returns this to use in app.py as results.rm

    ########### One Rep Max Estimate Function FLASK VERSION ###################
def one_rep_max(weight, reps):
    #print("1 rep max calculator")
    #weight = float(input("Enter the weight used: "))
    #reps = float(input("Enter the reps completed: "))
    max = round(weight * reps**0.1, 2) #Rounds to 2 decimal points
    #print(f"Your estimated 1 rep max is {max}")
    #time.sleep(5)
    #os.system("clear")
    return max


##### PLATE CALCULATOR FLASK VERSION LBS ONLY ########

def plate_calculator(weight):
    #print("Using a standard 20KG/45LB barbell... get the plates needed to get your desired weight")
    #weight_type = input("LBs or Kilos? ").strip().lower()
    #LBS SECTION
    #if weight_type in ['lbs', 'lb', 'pounds', 'pound']:
        #print("Do this for lbs")

        weight_for_plates = weight - 45      #Subtracts bar weight of 45

        if weight_for_plates < 0:
            #print("Weight is less than the barbell weight!")
            return Error

        # Weight per side (divide by 2 since plates go on both sides)
        weight_per_side = weight_for_plates / 2
        remaining_weight = weight_per_side
        # Calculate plates needed per side (only whole numbers)
        forty_five_plates = int(weight_per_side // 45)
        remaining_weight = weight_per_side % 45
        #print(f"Weight left per side: {remaining_weight}") #For testing
        twenty_five_plates = int(remaining_weight // 25)
        remaining_weight = remaining_weight % 25
        #print(f"Weight left per side after 25s: {remaining_weight}") #For testing
        ten_plates = int(remaining_weight // 10)
        remaining_weight = remaining_weight % 10
        five_plates = int(remaining_weight // 5)
        remaining_weight = remaining_weight % 5
        two_and_half_plates = int(remaining_weight // 2.5)
        
        #print(f"You will need {fourty_five_plates} 45(s),{twenty_five_plates} 25(s), {ten_plates} 10(s), {five_plates} 5(s) and {two_and_half_plates} 2.5(s) per side")
        return {
        "45s": forty_five_plates,
        "25s": twenty_five_plates,
        "10s": ten_plates,
        "5s": five_plates,
        "2.5s": two_and_half_plates
    }
    #Returns a dictionary
