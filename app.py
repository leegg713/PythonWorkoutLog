
# This is the Flask page that runs all the functions in webApp.py
# Contains a few functions and logic in this page as well

#Imports flask, render_template function and requests function from flask
from flask import Flask, render_template, request, redirect, url_for
from utils.webApp import wilks, dots, one_rep_max, plate_calculator, average_lift, get_db_connection, create_exercise_distribution_pie_chart, get_valid_number_input, convert_iso_to_mmddyy, clear_last_entry, add_exercise, edit_exercise, delete_exercise, create_progression_graph, get_last_date
#from utils.helpers import get_valid_number_input, convert_iso_to_mmddyy, clear_last_entry, add_exercise
#from utils.visualizations import create_progression_graph, volume_per_workout, average_intensity
#import matplotlib.pyplot as plt
#import io
#import base64
import pandas as pd

app = Flask(__name__)

file_path = "WorkoutLog.csv"

@app.route("/")
def home():
    #First page stuff
    #menu = display_menu()
    #calculator = calculator()
    return render_template("home.html")

@app.route('/add', methods=['GET', 'POST'])  # Handles Add/Edit/Delete Exercise
def add():
    if request.method == 'POST':
        action = request.form.get('action')  # get which button was pressed
        form_data = request.form

        if action == 'add':
            add_exercise(form_data)  # Save entry to CSV + DB
            # Keep the submitted values to prefill the form for the next entry
            params = {
                'exercise': form_data.get('exercise', ''),
                'sets': form_data.get('sets', ''),
                'reps': form_data.get('reps', ''),
                'weight': form_data.get('weight', ''),
                'date': form_data.get('date', '')
            }
            return redirect(url_for('add', **params))

        elif action == 'edit':
            edit_exercise(form_data)  # Update existing entry

        elif action == 'delete':
            delete_exercise(form_data)  # Remove entry from CSV + DB

        # Redirect to the same page after processing (default)
        return redirect(url_for('add'))

    # === DROPDOWN OPTIONS ===
    valid_exercises = [
        "Squat", "PauseSquat", "GobletSquat", "PauseBench",
        "TouchNGoBench", "InclineBench", "Deadlift", "DeficitDeadlift",
        "RomanianDeadlift", "OverheadPress", "OverheadDBPress", "Bench",
        "PowerClean", "HangClean"
    ]
    weight_options = list(range(45, 605, 5))
    rep_options = list(range(1, 21))
    set_options = list(range(1, 21))

    # Get last entered date from utility function
    last_date = get_last_date()

    # Prefill values (if provided via query params after a redirect)
    prefill_exercise = request.args.get('exercise', '')
    prefill_sets = request.args.get('sets', '')
    prefill_reps = request.args.get('reps', '')
    prefill_weight = request.args.get('weight', '')
    # If no date specified, fall back to last_date
    prefill_date = request.args.get('date') or last_date

    return render_template(
        'add.html',
        exercises=valid_exercises,
        weights=weight_options,
        reps=rep_options,
        sets=set_options,
        last_date=last_date,
        prefill_exercise=prefill_exercise,
        prefill_sets=prefill_sets,
        prefill_reps=prefill_reps,
        prefill_weight=prefill_weight,
        prefill_date=prefill_date
    )

@app.route('/graph')
def graph():
    # Read query params
    selected_exercise = request.args.get('exercise', '').strip()
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    # ---------------------------
    # Fetch exercises for dropdown
    # ---------------------------
    conn = get_db_connection()
    exercises_df = pd.read_sql_query(
        """
        SELECT DISTINCT Exercise AS exercise
        FROM Workout
        WHERE Exercise IS NOT NULL
        """,
        conn
    )
    conn.close()

    # Normalize column names and values
    exercises_df.columns = exercises_df.columns.str.strip().str.lower()

    if 'exercise' in exercises_df.columns:
        exercises = (
            exercises_df['exercise']
            .astype(str)
            .str.strip()
            .sort_values()
            .tolist()
        )
    else:
        exercises = []

    # ---------------------------
    # Generate graphs safely
    # ---------------------------
    graphs = []

    try:
        graphs.append(
            create_progression_graph(
                exercise=selected_exercise if selected_exercise else None,
                start_date=start_date,
                end_date=end_date
            )
        )
    except Exception as e:
        print(f"Progression graph error: {e}")

    try:
        graphs.append(
            create_exercise_distribution_pie_chart(
                exercise=selected_exercise if selected_exercise else None,
                start_date=start_date,
                end_date=end_date
            )
        )
    except Exception as e:
        print(f"Distribution graph error: {e}")

    # ---------------------------
    # Render template
    # ---------------------------
    return render_template(
        'graph.html',
        graphs=graphs,
        exercises=exercises,
        selected_exercise=selected_exercise,
        start_date=start_date,
        end_date=end_date
    )


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