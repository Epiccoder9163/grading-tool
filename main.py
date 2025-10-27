import ollama
import libinput
import inference
import os

# The LLM used in the program
# Make sure it is an Ollama-compatible model
model = "gemma3:latest"

# Prompt for the LLM
prompt = """
You are an AI assistant designed to grade homework assignments against a key. You will recieve the key first, then the homework
assignment you will grade. You will score the assignment as a percentage out of 100, with just the number. DO NOT INCLUDE ANY OTHER FEEDBACK OR TEXT, JUST REPORT A
NUMBER ANSWER.
"""

# Initialize variables
homework_list = []
keys = []
repeat = 0

# Create dictionaries
data = {
    'Title': 'data'
}

grading_data = {
    'Title': 'Grading_data'
}

# Initialize dictionary sections
data['keys'] = {}
data['homework'] = {}
data['assignment_name'] = {}

# Check if the model exists and ollama is working
print(ollama.list())
if model in str(ollama.list()):
    print("The selected model is available!")
else:
    print("The selected model is not available!")
    print("Downloading now")
    ollama.pull(model)

while True:
    repeat += 1

    os.system('clear')
    assignment_name = input("What is the name of the assignment you would like to enter?: ")
    while True:
        homework = libinput.get_homework()
        os.system('clear')
        will_continue = input("Would you like to enter more pages? (Y/N): ")
        if will_continue == "Y" or will_continue == "y" or will_continue == "Yes" or will_continue == "yes":
            homework_list.append(homework)
            continue
        if will_continue == "N" or will_continue == "n" or will_continue == "no" or will_continue == "No":
            homework_list.append(homework)
            break
        
    os.system('clear')
    keys.append(libinput.get_key())

    # Append the key value to the dictionary
    data['keys'][str(repeat)] = keys
    # Append the homework path list to the dictionary
    data['homework'][str(repeat)] = homework_list
    # Append the assignment name to the dictionary
    data['assignment_name'][str(repeat)] = assignment_name
    print(data)
    #os.system('clear')
    will_continue = input("Would you like to enter more assignments? (Y/N): ")
    if will_continue == "Y" or will_continue == "y" or will_continue == "Yes" or will_continue == "yes":
        continue
    if will_continue == "N" or will_continue == "n" or will_continue == "no" or will_continue == "No":
        break

for i in range(1, len(data['homework']) + 1):
    for x in range(0, len(data['homework'][str(i)])):
        print(data['keys'][str(i)][x])
        print(data['homework'][str(i)][x])
        print(inference.run(data['homework'][str(i)][x]))
