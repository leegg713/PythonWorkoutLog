import pandas as pd
import matplotlib.pyplot as plt
import time
import os
import io
import base64

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
def create_simple_default_graph():
    # Create a simple dataframe with sample data
    data = {
        'X': [1, 2, 3, 4, 5],
        'Y': [10, 20, 15, 25, 30]
    }
    df = pd.DataFrame(data)

    # Plot
    plt.figure(figsize=(6, 4))
    plt.plot(df['X'], df['Y'], marker='o', linestyle='-', color='green')
    plt.title('Simple Default Graph')
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.grid(True)
    plt.tight_layout()

    # Convert plot to base64 string to embed in HTML
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode()
    plt.close()

    return f"data:image/png;base64,{graph_url}"

