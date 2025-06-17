import pandas as pd
import matplotlib.pyplot as plt
import time
import os

file_path = 'WorkoutLog.csv'



########## GRAPH Function make it work for FLASK #########
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