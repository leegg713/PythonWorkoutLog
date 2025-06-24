import pandas as pd
import matplotlib.pyplot as plt
import time
import os
import io
import base64
from io import BytesIO

file_path = 'WorkoutLog.csv'

###NEED TO CREATE 4 DIFFERENT GRAPHS #####
'''
1. Progression Over Time (Line Graph)
Purpose: Track how much weight you're lifting for a specific exercise across time.
X-axis: Date
Y-axis: Weight lifted
Group: One line per exercise
Insight: Shows whether you're gaining strength or plateauing in a lift like bench press or squat.

2. Total Volume per Workout (Bar Graph)
Purpose: Measure workout intensity using total volume: sets × reps × weight.
X-axis: Date
Y-axis: Total volume
Group: Optionally grouped by exercise or entire workout
Insight: Highlights overall workload and helps identify deload weeks or progressions.

3. Rep Range Patterns (Box Plot or Histogram)
Purpose: Visualize rep patterns to see consistency or variation.
X-axis: Exercise name (or dates)
Y-axis: Number of reps
Insight: Reveals whether you're training mostly for strength (low reps) or hypertrophy/endurance (higher reps), and how consistent you are.

4. Average Intensity by Exercise (Bar Graph)
Purpose: Compare how heavy you lift on average for each exercise.
X-axis: Exercise
Y-axis: Average weight lifted (or average volume)
Insight: Helps assess which exercises are prioritized or neglected in terms of intensity.
'''
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
    # You can also group by date: volume_per_day = df.groupby('Date')['Volume'].sum()
    # ------------------------
    
    # TEMPLATE PLACEHOLDER: Replace this with your actual volume logic
   # df['Volume'] = df['Weight']  # Placeholder, change this!
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
