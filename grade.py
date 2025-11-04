# Script used to gather percentage average of questions

def run(homework_list, key_list):
    wrong_answers = []
    numright = 0
    for i in range(0, len(homework_list)):
        if homework_list[i] == key_list[i]:
            numright += 1
        if homework_list[i] != key_list[i]:
            wrong_answers.append(f"{i}: {homework_list[i]}")
    print(numright)
    return [avg(len(homework_list), numright), wrong_answers]

def avg(numquestions, numright):
    avg = numright / numquestions
    output = round(avg * 100)
    return output
