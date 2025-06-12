# This page will be how the actual work is done by using the functions in Main.py

# app.py
from flask import Flask, render_template, request
from main import display_menu, calculator

app = Flask(__name__)

@app.route("/")
def home():
  #First page stuff
  menu = display_menu()
  calculator = calculator()
  return render_template("index.html", menu = menu, calculator = calculator)


if __name__ == "__main__":
    app.run(debug=True)