import os
import base64
from io import BytesIO
from PIL import Image

def get_key():
    global homework_list
    global key_list

    while True:
        while True:
            key_path = input("Enter the full extended file path of the answer key: ")
            if os.path.exists(key_path) and ".png" in key_path or ".jpeg" in key_path or ".jpg" in key_path:
                return (convert_to_base64(key_path))
            else:
                print("This path is invalid! Check that the file exists and is either a PNG or JPG.")

def get_homework():
    while True:
        key_path = input("Enter the full extended file path of the homework: ")
        if os.path.exists(key_path) and ".png" in key_path or ".jpeg" in key_path or ".jpg" in key_path:
            return convert_to_base64(key_path)
        else:
            print("This path is invalid! Check that the file exists and is either a PNG or JPG.")

def convert_to_base64(key_path):
    image = Image.open(key_path)
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")