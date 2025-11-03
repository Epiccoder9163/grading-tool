# Script used to export data to different formats
# CSV is currently only supported format
# !!! This script is only used in gui.py, not main.py

import csv

types = ['CSV', 'TXT']

def to_csv(names, grades):
    # Open or create the file in the working directory.
    with open('grades.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        # Write the header
        writer.writerow(['Name', 'Grade'])
        # Write the data
        for name, grade in zip(names, grades):
            writer.writerow([name, grade])

    return

def to_txt(names, grades):
    # Open or create the file in the working directory.
    with open('grades.txt', 'a', newline='') as file:
        # Write the data
        for i in range(len(names)):
            file.write(f"\n{names[i]}: {grades[i]}")

    return