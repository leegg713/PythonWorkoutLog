#!/usr/bin/env python3
"""Simple utility to view the database in a readable table format."""

import sqlite3
import pandas as pd

db_file = "WorkoutLog.db"
table_name = "Workout"

try:
    # Connect to database
    conn = sqlite3.connect(db_file)
    
    # Read table into pandas DataFrame
    df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
    conn.close()
    
    # Display the DataFrame nicely
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', None)
    
    print(f"\n{'='*100}")
    print(f"Database: {db_file}")
    print(f"Table: {table_name}")
    print(f"Total rows: {len(df)}")
    print(f"{'='*100}\n")
    
    print(df.to_string(index=False))
    
    print(f"\n{'='*100}\n")
    
except Exception as e:
    print(f"Error: {e}")
