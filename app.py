# This page will be how the actual work is done by using the functions in Main.py

# app.py
from flask import Flask, render_template, request
from main import * # import your logic

app = Flask(__name__)

@app.route("/")
def home():
    #name = request.args.get("name", "World")  # default to "World" if no query param
    menu = display_menu()
    return render_template("index.html", menu = menu)

if __name__ == "__main__":
    app.run(debug=True)