# Script used to export data to different formats
# CSV is currently only supported format
# !!! This script is only used in gui.py, not main.py

import csv
import os

types = ['CSV', 'TXT']
filename = "grades"

def to_csv(names, grades, wrong_answers):
    # Open or create the file in the working directory.
    # If the file doesn't exist create the file and write the header
    if os.path.exists(f"{filename}.csv") == False or os.path.getsize(f"{filename}.csv") == 0:
        with open(f"{filename}.csv", 'w', newline='') as file:
            writer = csv.writer(file)
            # Write the data
            writer.writerow(['Name', 'Grade', 'Questions Wrong'])
    with open(f"{filename}.csv", 'a', newline='') as file:
        writer = csv.writer(file)
        # Write the data
        for name, grade, wrong_answers in zip(names, grades, wrong_answers):
            writer.writerow([name, grade, wrong_answers])

    return

def to_txt(names, grades, wrong_answers):
    # Open or create the file in the working directory.
    with open(f"{filename}.txt", 'a', newline='') as file:
        # Write the data
        for i in range(len(names)):
            file.write(f"\n{names[i]}")
            file.write(f"\n    Grade: {grades[i]}")
            file.write(f"\n    Wrong Answer: {wrong_answers[i]}")

    return