import pandas as pd
import matplotlib.pyplot as plt
import time
import os

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


