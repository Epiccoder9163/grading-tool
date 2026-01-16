# Script used to export data to different formats
# CSV is currently only supported format

import csv
import os
from configparser import ConfigParser

types = ['CSV', 'TXT']
filename = "grades"

config = ConfigParser()
config.read('config.ini')

def to_csv(names, grades, wrong_answers, explanations):
    # Open or create the file in the working directory.
    # If the file doesn't exist create the file and write the header
    if int(config.get("General", "Explain Incorrect Answers")) == 2:
        if os.path.exists(f"{filename}.csv") == False or os.path.getsize(f"{filename}.csv") == 0:
            with open(f"{filename}.csv", 'w', newline='') as file:
                writer = csv.writer(file)
                # Write the data
                writer.writerow(['Name', 'Grade', 'Questions Wrong', 'Explanations'])
        with open(f"{filename}.csv", 'a', newline='') as file:
            writer = csv.writer(file)
            # Write the data
            for name, grade, wrong_answers, explanations in zip(names, grades, wrong_answers, explanations):
                writer.writerow([name, grade, wrong_answers, explanations])
    else:
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

def to_txt(names, grades, wrong_answers, explanations):
    # Open or create the file in the working directory.
    if config.get("General", "Explain Incorrect Answers") == 2:
        with open(f"{filename}.txt", 'a', newline='') as file:
            # Write the data
            for i in range(len(names)):
                file.write(f"\n{names[i]}")
                file.write(f"\n    Grade: {grades[i]}")
                file.write(f"\n    Wrong Answer: {wrong_answers[i]}")
                file.write(f"\n    Explanations: {explanations[i]}")
    if config.get("General", "Explain Incorrect Answers") == 0:
        with open(f"{filename}.txt", 'a', newline='') as file:
            # Write the data
            for i in range(len(names)):
                file.write(f"\n{names[i]}")
                file.write(f"\n    Grade: {grades[i]}")
                file.write(f"\n    Wrong Answer: {wrong_answers[i]}")

    return