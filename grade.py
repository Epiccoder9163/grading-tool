# Script used to gather percentage average of questions

def run(homework_list, key_list):
    numright = 0

    for i in range(0, len(homework_list)):
        if homework_list[i] == key_list[i]:
            numright += 1
    print(numright)
    return avg(len(homework_list), numright)

def avg(numquestions, numright):
    avg = numright / numquestions
    output = round(avg * 100)
    return output

