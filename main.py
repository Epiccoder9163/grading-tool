import ollama
import libinput
import os
import time
from langchain_community.chat_models import ChatOllama

model = "gemma3:latest"

homework_list = []
key_list = []

print(ollama.list())
if model in str(ollama.list()):
    print("The selected model is available!")
else:
    print("The selected model is not available!")
    print("Downloading now")
    ollama.pull(model)

vision_llm = ChatOllama(base_url="http://localhost:11434", model=model)

while True:
    homework = libinput.get_homework()
    will_continue = input("Would you like to enter more pages? (Y/N): ")
    if will_continue == "Y" or will_continue == "y" or will_continue == "Yes" or will_continue == "yes":
        homework_list.append(homework)
        continue
    if will_continue == "N" or will_continue == "n" or will_continue == "no" or will_continue == "No":
        homework_list.append(homework)
        break


while True:
    key = libinput.get_key()
    will_continue = input("Would you like to enter more pages? (Y/N): ")
    if will_continue == "Y" or will_continue == "y" or will_continue == "Yes" or will_continue == "yes":
        key_list.append(key)
        continue
    if will_continue == "N" or will_continue == "n" or will_continue == "no" or will_continue == "No":
        key_list.append(key)
        break

