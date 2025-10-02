# Lee's Workout Tracker

This workout app will help you track workouts over time to notice trends about your workouts that are easily readable by looking at graphs.
There are also some calculation features to help you see where you stack up against your prior self and others as well. 

## Features
- Workout Logging
Add exercises and log workout data via a simple form which uploads the information to a CSV and also a SQLite DB.

- Data Visualization
View multiple interactive graphs tracking workout progress, volume, and intensity.

- Fitness Calculators
Calculate average lifts, WILKS score, DOTS score, estimated one-rep max, and plate loading based on user inputs.

- Timer Page
Built-in timer tool for workout sessions.

## CSV FILE FORMAT
Exercise, Sets, Reps, Weight, Date

## Requirements
- Python 3.x
- pandas
- matplotlib

## Installation

1. Clone this repository to your own GitHub or download the script files.
2. Install dependencies:
   ```bash (While in terminal)
   pip install -r requirements.txt
## RUN
To run the script via console only(Does not contain all features): python main.py
To run the script with all features and have a flask app load: python app.py

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repo  
2. Create a new branch for your feature or fix  
3. Commit your changes with clear messages  
4. Push your branch and open a Pull Request  
5. I will review and see if I want to add the feature

If you have suggestions or questions, feel free to open an issue.

Thank you for helping me improve this project!


## IMPROVEMENTS TO COME ##
Log In Functionality for End Users
Multi User support -- Will need to update how the DB takes data to have a key per user

