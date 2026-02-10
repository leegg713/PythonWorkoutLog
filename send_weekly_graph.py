#!/usr/bin/env python3
"""
Weekly CSV-only email script
=================================

This script reads workout entries from the CSV file `WorkoutLog.csv`,
filters entries from the past 7 days, and emails a human-readable summary
using the lightweight Gmail sender `send_email()` supplied by the user.

Notes:
- Uses only the CSV (no DB access)
- The email sender expects the environment variables `GMAIL_USERNAME` and
  `GMAIL_PASSWORD` to be set (these should be added as repo secrets in
  GitHub Actions and mapped to the environment in the workflow).

1) Add repository secrets on GitHub
- GMAIL_USERNAME: your Gmail address used to send
- GMAIL_PASSWORD: app password (recommended) or Gmail account password

2) Workflow
- The workflow is at `.github/workflows/weekly_email.yml` and runs the script weekly.
- It injects `GMAIL_USERNAME` and `GMAIL_PASSWORD` into the job environment.

Notes
- The script reads only `WorkoutLog.csv` from the repo root and sends a plain-text email
  containing workouts from the past 7 days.
- The recipient is currently hard-coded to `leemerigold7@gmail.com` inside the script.
  Change `send_email()` if you want to use a different recipient or an env var.
"""

import os
import pandas as pd
import datetime
import smtplib
from email.message import EmailMessage
from typing import Tuple
import matplotlib.pyplot as plt
import pathlib


# ---------------------------
# User-provided email helper
# ---------------------------
def send_email(subject: str, body: str, attachment_path: str | None = None):
    """Send a plain-text email using Gmail SMTP credentials from the env.

    If `attachment_path` is provided and the file exists, attach it to the
    email as an image/png. Uses `GMAIL_USERNAME` and `GMAIL_PASSWORD` from
    environment variables.
    """
    gmail_user = os.getenv("GMAIL_USERNAME")
    gmail_password = os.getenv("GMAIL_PASSWORD")

    if not gmail_user or not gmail_password:
        print("GMAIL_USERNAME or GMAIL_PASSWORD is not set. Email not sent.")
        return

    msg = EmailMessage()
    msg["From"] = gmail_user
    msg["To"] = "leemerigold7@gmail.com"
    msg["Subject"] = subject
    msg.set_content(body)

    # Attach image if available
    if attachment_path:
        p = pathlib.Path(attachment_path)
        if p.exists() and p.is_file():
            try:
                with open(p, "rb") as f:
                    data = f.read()
                # treat as PNG image
                msg.add_attachment(data, maintype="image", subtype="png", filename=p.name)
            except Exception as e:
                print(f"Warning: failed to attach {attachment_path}: {e}")

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.starttls()  # Secure the connection
            smtp.login(gmail_user, gmail_password)
            smtp.send_message(msg)
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

# ---------------------------
# CSV reading and parsing
# ---------------------------
def load_csv(csv_path: str) -> pd.DataFrame:
    """Load the CSV into a DataFrame.

    The CSV is expected to contain at least the columns:
    `exercise`, `sets`, `reps`, `weight`, `date` (in any common format).
    """
    # Checks to make sure CSV exists
    if not os.path.exists(csv_path):
        return pd.DataFrame()

    # Try reading with headers first; fall back to common column order
    try:
        df = pd.read_csv(csv_path)
    except Exception:
        # If reading fails, return empty DataFrame to not have the script error out
        return pd.DataFrame()

    #
    # Normalize column names
    df.columns = df.columns.astype(str).str.strip().str.lower()

    required = {"exercise", "sets", "reps", "weight", "date"}

    # Reload with default headers if required columns missing
    if not required.issubset(df.columns):
        try:
            df = pd.read_csv(csv_path, header=None,
                         names=["exercise", "sets", "reps", "weight", "date", "id"])
        except:
            return pd.DataFrame()

    return df

def parse_dates(df: pd.DataFrame) -> pd.DataFrame:
    """Parse the `date` column to pandas datetimes and drop invalid rows.

    This implementation relies on `pandas.to_datetime` which is fast and
    robust for common formats. It returns the cleansed DataFrame (may be
    empty if no valid dates exist).
    """
    # Checks to see if date is a column
    if df.empty or "date" not in df.columns:
        return df

    df = df.copy()
    # Parse dates (coerce invalid values to NaT), pandas infers common formats
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    # Drop rows where parsing failed
    df = df.dropna(subset=["date"]).reset_index(drop=True)

    # Normalize exercise and weight types for downstream processing
    if "exercise" in df.columns:
        df["exercise"] = df["exercise"].astype(str).str.strip()
    if "weight" in df.columns:
        df["weight"] = pd.to_numeric(df["weight"], errors="coerce")

    return df


# ---------------------------
# Filter and formatting helpers
# ---------------------------
def filter_last_n_days(df: pd.DataFrame, days: int = 7) -> Tuple[pd.DataFrame, datetime.date, datetime.date]:
    """Return rows whose dates fall within the last `days` days (inclusive).

    Returns a tuple (filtered_df, start_date, end_date).
    """
    # Use UTC today as the reference. `start` is the inclusive lower bound.
    today = datetime.datetime.now(datetime.UTC).date()
    start = today - datetime.timedelta(days=days)

    # Work with the date portion only (drop time) to make comparisons simple
    # and predictable. This avoids issues when timestamps include times.
    date_only = df["date"].dt.date

    # Boolean mask selecting rows where date falls between start and today.
    mask = (date_only >= start) & (date_only <= today)

    # Return a copy of the filtered rows plus the start/end dates used.
    return df.loc[mask].copy(), start, today


def format_workouts_text(df: pd.DataFrame) -> str:
    """Create a human-readable plain-text summary of workouts.

    Each line is formatted as: `YYYY-MM-DD | Exercise | sets x reps @ weight`
    """
    if df.empty:
        return "No workouts recorded this period."

    lines = []
    # Sort by date ascending for readability
    df = df.sort_values(by="date")
    for _, row in df.iterrows():
        date_str = row["date"].strftime("%Y-%m-%d")
        exercise = str(row.get("exercise", "")).strip()
        sets = str(row.get("sets", ""))
        reps = str(row.get("reps", ""))
        weight = str(row.get("weight", ""))
        lines.append(f"{date_str} | {exercise} | {sets} x {reps} @ {weight}")

    return "\n".join(lines)


# ---------------------------
# Main entrypoint
# ---------------------------
def main():
    """Load CSV, filter last week, and send the summary using `send_email()`.

    The script is intentionally minimal: it sends a plain-text email with
    the week's workouts and attaches an image of a graph of it as well
    """
    repo_root = os.getcwd()
    csv_path = "WorkoutLog.csv"

    # Load and parse CSV data
    df = load_csv(csv_path)
    if df.empty:
        print("CSV missing or empty; nothing to send.")
        return

    df = parse_dates(df)
    if df.empty:
        print("No parsable dates found in CSV; nothing to send.")
        return

    # Filter to the past 7 days
    week_df, start, end = filter_last_n_days(df, days=7)

    # Compose the email
    subject = f"Lee Weekly Workout Summary: {start.isoformat()} - {end.isoformat()}"
    body = format_workouts_text(week_df)

    # Create a PNG graph (or placeholder) and attach it to the email.
    out_path = os.path.join(repo_root, "weekly_graph.png")

    try:
        if week_df.empty:
            # Create a small placeholder image when no workouts are present
            plt.figure(figsize=(6, 3))
            plt.text(0.5, 0.5, "No workouts this week", ha="center", va="center", fontsize=14)
            plt.axis("off")
            plt.tight_layout()
            plt.savefig(out_path)
            plt.close()
        else:
            # Plot max weight per date for each exercise for readability
            plt.figure(figsize=(10, 6))
            for ex in week_df["exercise"].unique():
                sub = week_df[week_df["exercise"] == ex]
                if sub.empty:
                    continue
                agg = sub.groupby(sub["date"].dt.date)["weight"].max()
                dates = [pd.to_datetime(d) for d in agg.index]
                plt.plot(dates, agg.values, marker="o", label=ex)
            plt.xlabel("Date")
            plt.ylabel("Weight")
            plt.title("Weekly Workout Progression")
            plt.legend()
            plt.grid(True)
            plt.tight_layout()
            plt.savefig(out_path)
            plt.close()
    except Exception as e:
        print(f"Warning: failed to generate graph: {e}")
        out_path = None

    # Send using the provided Gmail helper (uses GMAIL_USERNAME / GMAIL_PASSWORD)
    send_email(subject, body, attachment_path=out_path)

if __name__ == "__main__":
    main()
