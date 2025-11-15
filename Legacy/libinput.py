# Old input library script
# !!! As main.py will not be updated anymore, libinput.py will not be updated either, all changes are being merged into gui.py
# !!! This script is only used in main.py, not used in gui.py
# !!! Script not being used anymore, will be removed in a future commit

import os
import base64
from io import BytesIO
from PIL import Image

def get_folder():
    folder = input("Enter the full extended file path of the folder: ")
    if os.path.isdir(folder):
        return folder
    else:
        print("This path is invalid! Check that the folder exists and is a directory.")
        
def get_key():
    while True:
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

def convert_to_base64(key_path):
    image = Image.open(key_path)
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")