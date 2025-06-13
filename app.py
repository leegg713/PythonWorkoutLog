
# This page will be how the actual work is done by using the functions in Main.py

# app.py
from flask import Flask, render_template, request, redirect, url_for #Imports flask, render_template function and requests function
from main import  add_exercise, average_lift, wilks, one_rep_max, exercise_frequency, dots, plate_calculator

app = Flask(__name__)

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

@app.route('/calc', methods=['GET', 'POST'])
def calc():
    result = None
    if request.method == 'POST':
        choice = request.form['choice']
        if choice == "1":
            result = average_lift()
        elif choice == "2":
            result = wilks()
        elif choice == "3":
            result = dots()
        elif choice == "4":
            result = one_rep_max()
        elif choice == "5":
            result = plate_calculator()
        elif choice == "6":
            result = exercise_frequency()
        else:
            result = "Invalid selection."
    return render_template("calc.html", result=result)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")