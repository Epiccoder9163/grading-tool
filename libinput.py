import promptgen
import os

def get_key():
    while True:
        key_path = input("Enter the full extended file path of the answer key: ")
        if os.path.exists(key_path) and ".png" in key_path or ".jpeg" in key_path or ".jpg" in key_path:
            return key_path
        else:
            print("This path is invalid! Check that the file exists and is either a PNG or JPG.")

def get_homework():
    while True:
        key_path = input("Enter the full extended file path of the homework: ")
        if os.path.exists(key_path) and ".png" in key_path or ".jpeg" in key_path or ".jpg" in key_path:
            return key_path
        else:
            print("This path is invalid! Check that the file exists and is either a PNG or JPG.")