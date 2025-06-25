
# This page will be how the actual work is done by using the functions in Main.py

# app.py
from flask import Flask, render_template, request, redirect, url_for #Imports flask, render_template function and requests function
#from main import  add_exercise, average_lift, wilks, one_rep_max,  dots, plate_calculator #create_line_graph
from utils.calc import wilks, dots, one_rep_max, plate_calculator, average_lift
from utils.helpers import get_valid_number_input, convert_iso_to_mmddyy, clear_last_entry, add_exercise
from utils.visualizations import create_progression_graph, volume_per_workout, average_intensity
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

file_path = "WorkoutLog.csv"

@app.route("/")
def home():
    #First page stuff
    #menu = display_menu()
    #calculator = calculator()
    return render_template("home.html")

@app.route('/add', methods=['GET', 'POST']) #Sets a new route when add button selected etc
def add():
    if request.method == 'POST':
        form_data = request.form
        add_exercise(form_data)  # pass form data to the function
        return redirect(url_for('home'))
    return render_template('add.html')

@app.route('/graph')
def graph():
    graphs = [] #List to store different graphs

  # Append one simple graph to the list # Add more below here
    graphs.append(create_progression_graph(file_path))
    graphs.append(volume_per_workout(file_path))
    graphs.append(average_intensity(file_path))
    # If you want to add more graphs, just call your graph functions and append them here

    return render_template('graph.html', graphs=graphs)

@app.route('/timer', methods=['GET', 'POST']) #Timer Page
def timer():
    return render_template('timer.html')  # This will render timer.html page

@app.route('/calc', methods=['GET', 'POST'])
def calc():
    #result = None  # Default, no result shown on GET
    results = {} # Stores differnet results variables per calculator function
    if request.method == 'POST':
        choice = request.form.get('choice', '')
        
        if choice == '1':
            exercise_to_avg = request.form.get('exercise_to_avg', '').strip() #Sets exercise_to_avg equal to what the user inputs on the page
            if exercise_to_avg:
                results['average'] = average_lift(exercise_to_avg) # If exercise_to_avg matches the checks it will run the python function from main.py to get output, exercise, average, and total reps
            else:
                results['average'] = {"error": "Please enter a valid exercise name."} #Shows no matter what --- Will need to fix that to display properly only when bad input
        elif choice == '2':
            try:
                bodyweight = float(request.form.get('bodyweight', '').strip())
                total_lift = float(request.form.get('total_lift', '').strip())
                results['wilks'] = f"WILKS Score: {wilks(bodyweight, total_lift)}"
            except (TypeError, ValueError):
                results['wilks'] = "Please enter valid numbers for bodyweight and total lifted." #Shows the error prior to entering input -- Need to fix

            #result = wilks()
        elif choice == '3':
            try:
                bodyweight = float(request.form.get('bodyweight', '').strip())
                total_lift = float(request.form.get('total_lift', '').strip())
                results['dots'] = f"DOTS Score: {dots(bodyweight, total_lift)}"
            except (TypeError, ValueError):
                results['dots'] = "Please enter valid numbers for bodyweight and total lifted."
            #result = dots()
        elif choice == '4':
            try:
                weight = float(request.form.get('weight', '').strip())
                reps = float(request.form.get('reps', '').strip())
                results['rm'] = f"Estimated One Rep Max: {one_rep_max(weight, reps)}"
            except (TypeError, ValueError):
                results['rm'] = "Please enter valid numbers for bodyweight and total lifted."
            #result = one_rep_max()
        elif choice == '5':
            try:
                weight = float(request.form.get('weight', '').strip())
                plate_counts = plate_calculator(weight)
                if isinstance(plate_counts, str):
                    results['plate'] = plate_counts
                else:
                    results['plate'] = (
                    f"Plates per side: 45s: {plate_counts['45s']}, "
                    f"25s: {plate_counts['25s']}, 10s: {plate_counts['10s']}, "
                    f"5s: {plate_counts['5s']}, 2.5s: {plate_counts['2.5s']}")
            except (TypeError, ValueError):
                results['plate'] = "Please enter a valid number for the weight."
            #LB Plate Calculator
           
        else:
            results['error'] = "Invalid selection."

    return render_template('calc.html', results=results)
    



if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")