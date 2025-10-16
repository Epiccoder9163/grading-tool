import ollama
from promptgenold import analyse
from promptgenold import compare
import libinput

# models = [vision model, small text model]
models = ['llava:latest', 'qwen3:0.6b']

# Check if the models listed above are available
print(ollama.list())
for i in range(0, len(models)):
    if models[i] in str(ollama.list()):
        print("The selected model is available!")
    else:
        print("The selected model is not available!")
        print("Downloading now")
        ollama.pull(models[i])

# Gather file paths
answer_key = libinput.get_key()
homework = libinput.get_homework()

#analyse(answer_key)
#formatted_homework = analyse(homework)

#print(compare(homework, answer_key))
print(analyse(homework, answer_key))



