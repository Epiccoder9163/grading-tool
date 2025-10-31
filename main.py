import libinput
import inference
import ollama
import os

# Initialize variables
homework_list = []
keys = []
repeat = 0

# Create dictionaries
paths = {
    'Title': 'paths'
}

grading_data = {
    'Title': 'Grading_data'
}

# Initialize dictionary sections
paths['keys'] = {}
paths['homework'] = {}
paths['assignment_name'] = {}

# List installed models
models = ollama.list()
print(models)
ollama.pull(inference.model)


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
    paths['keys'][str(repeat)] = keys
    # Append the homework path list to the dictionary
    paths['homework'][str(repeat)] = homework_list
    # Append the assignment name to the dictionary
    paths['assignment_name'][str(repeat)] = assignment_name
    print(paths)
    os.system('clear')
    will_continue = input("Would you like to enter more assignments? (Y/N): ")
    if will_continue == "Y" or will_continue == "y" or will_continue == "Yes" or will_continue == "yes":
        continue
    if will_continue == "N" or will_continue == "n" or will_continue == "no" or will_continue == "No":
        break

# Loop for as many times as there are homework path lists in the paths dictionary
for i in range(1, len(paths['homework']) + 1):
    # Loop for as many times as there are 
    for x in range(0, len(paths['homework'][str(i)])):
        print(paths['keys'][str(i)][x])
        print(paths['homework'][str(i)][x])
        print(inference.run(paths['homework'][str(i)][x]))
        print(inference.run(paths['keys'][str(i)][x]))
