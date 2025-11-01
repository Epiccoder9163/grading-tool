import libinput
import inference
import grade
import ollama
import os

# Initialize variables
homework_list = []
keys = []
repeat = 0

# Create dictionaries
paths = {}

data = {}

graded = {}

# Initialize dictionary sections
paths['keys'] = {}
paths['homework'] = {}
paths['assignment_name'] = {}

data['keys'] = {}
data['homework'] = {}


# Check if the selected model exists, if not download it
try:
  ollama.chat(inference.model)
except ollama.ResponseError as e:
  print('Error:', e.error)
  if e.status_code == 404:
    ollama.pull(inference.model)


while True:
    # Count the number of times this loop as run
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
    while True:
        key = libinput.get_key()
        os.system('clear')
        will_continue = input("Would you like to enter more pages? (Y/N): ")
        if will_continue == "Y" or will_continue == "y" or will_continue == "Yes" or will_continue == "yes":
            keys.append(key)
            continue
        if will_continue == "N" or will_continue == "n" or will_continue == "no" or will_continue == "No":
            keys.append(key)
            break

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
# The loop starts at one to make the dictionary item valid, because zero isn't a valid number
for i in range(1, len(paths['homework']) + 1):
    # Initialize lists
    data['homework'][str(i)] = []
    data['keys'][str(i)] = []

    # Loop for as many times as there are paths in the homework path list
    for x in range(0, len(paths['homework'][str(i)])):
        print(paths['homework'][str(i)][x])
        output = inference.run(paths['homework'][str(i)][x])

        # Parse the output to turn it into a list
        result = [item.split(":")[1].strip() for item in output.split(",")]
        print(result)
        
        # Append the homework path to the list
        data['homework'][str(i)].extend(result)

    # Loop for as many times as there are paths in the key list (in case the lists are not of equal sizes)
    for x in range(0, len(paths['keys'][str(i)])):
        print(paths['keys'][str(i)][x])
        output = inference.run(paths['keys'][str(i)][x])

        # Parse the output to turn it into a list
        result = [item.split(":")[1].strip() for item in output.split(",")]
        print(result)

        # Append the key path to the list
        data['keys'][str(i)].extend(result)

# Loop for as many times as there are homework question data in the data dictionary
# The loop starts at one to make the dictionary item valid, because zero isn't a valid number
for i in range(1, len(data['homework']) + 1):
    graded[str(i)] = grade.run(data['homework'][str(i)], data['keys'][str(i)])

print(graded)