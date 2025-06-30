import pandas as pd
import matplotlib.pyplot as plt
import time
import os
import io
import base64
from io import BytesIO
from utils.calc import average_lift

file_path = 'WorkoutLog.csv'

def create_progression_graph(file_path):
    # Load CSV
    df = pd.read_csv(file_path)

    # Convert Date column to datetime
    df['Date'] = pd.to_datetime(df['Date'])

    # Sort by date to keep lines in order
    df = df.sort_values(by='Date')

    # Plot setup
    plt.figure(figsize=(10, 6))

    # Plot one line per exercise
    for exercise in df['Exercise'].unique():
        subset = df[df['Exercise'] == exercise]
        plt.plot(subset['Date'], subset['Weight'], marker='o', label=exercise)

    # Labels & legend
    plt.xlabel("Date")
    plt.ylabel("Weight Lifted")
    plt.title("Progression Over Time")
    plt.legend(title="Exercise")
    plt.grid(True)

    # Save to buffer for Flask embedding
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    graph_data = base64.b64encode(buffer.getvalue()).decode()
    plt.close()
    return f'data:image/png;base64,{graph_data}'

def volume_per_workout(file_path):
    # Load CSV
    df = pd.read_csv(file_path)

    # Convert Date column to datetime
    df['Date'] = pd.to_datetime(df['Date'])

    # OPTIONAL: Sort by date
    df = df.sort_values(by='Date')

    df['Volume'] = df['Weight'] * df['Reps'] * df['Sets']
    volume_per_day = df.groupby('Date')['Volume'].sum().reset_index()

    # === Bar Chart ===
    plt.figure(figsize=(10, 6))
    # Create an empty list to hold bar colors
    colors = []

# Loop through each volume value
    for volume in volume_per_day['Volume']:
        if volume > 7000:
            colors.append('red')
        else:
            colors.append('green')
    plt.bar(volume_per_day['Date'].dt.strftime('%Y-%m-%d'), volume_per_day['Volume'], color=colors)
    
    # Labels and layout
    plt.xlabel("Date")
    plt.ylabel("Total Volume")
    plt.title("Workout Volume Per Day")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.grid(True, axis='y')

    # Save to buffer for Flask
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    graph_data = base64.b64encode(buffer.getvalue()).decode()
    plt.close()
    return f'data:image/png;base64,{graph_data}'

import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64

def average_intensity(file_path):
    # Load CSV
    df = pd.read_csv(file_path)

    # Calculate total weight and total reps per row
    df['TotalWeight'] = df['Weight'] * df['Reps'] * df['Sets']
    df['TotalReps'] = df['Reps'] * df['Sets']

    # Group by exercise
    grouped = df.groupby('Exercise').agg({
        'TotalWeight': 'sum',
        'TotalReps': 'sum'
    }).reset_index()

    # Calculate average weight per rep for each exercise
    grouped['AvgWeightPerRep'] = grouped['TotalWeight'] / grouped['TotalReps']

    # === Bar Chart ===
    plt.figure(figsize=(10, 6))
    plt.bar(grouped['Exercise'], grouped['AvgWeightPerRep'], color='purple')


    # Labels and layout
    plt.xlabel("Exercise")
    plt.ylabel("Average Weight per Rep")
    plt.title("Average Intensity by Exercise")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.grid(True, axis='y')

    # Save to buffer for Flask
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    graph_data = base64.b64encode(buffer.getvalue()).decode()
    plt.close()

    return f'data:image/png;base64,{graph_data}'

