
# This page will be how the actual work is done by using the functions in Main.py

# app.py
from flask import Flask, render_template, request, redirect, url_for #Imports flask, render_template function and requests function
from main import calculator, add_exercise

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


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")