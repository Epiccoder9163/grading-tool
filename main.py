import ollama
import os
import libinput
from langchain_community.chat_models import ChatOllama
from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import StrOutputParser

# models = [vision model, small text model]
models = ['gemma3:latest', 'qwen3:0.6b']

# Prompt for the large language model
prompt = """
You are a precise and helpful assistant designed to grade math homework. You will be given two images: the student's completed homework and the teacher's answer key, in that order.
Your task is to compare the student's answers to the correct ones and return a Python list of boolean values. Each element in the list should represent whether the student's answer to that question is correct (`True`) or incorrect (`False`).
Only return the Python list. Do not include any explanation, formatting, or extra commentary. Be as accurate as possible, and assume the teacher would grade strictly based on correctness.
Example output format:
[True, False, True, True, False]
"""

# Check if the models listed above are available
print(ollama.list())
for i in range(0, len(models)):
    if models[i] in str(ollama.list()):
        print("The selected model is available!")
    else:
        print("The selected model is not available!")
        print("Downloading now")
        ollama.pull(models[i])
vision_llm = ChatOllama(base_url="http://localhost:11434", model=models[0])
text_llm = ChatOllama(base_url="http://localhost:11434", model=models[1])

def analyse(paths):
    message = HumanMessage(content=[
    {
        "type": "text",
        "text": prompt
    },
    {
        "type": "image_url",
        "image_url": f"data:image/jpeg;base64,{paths[0]}"
    },
    {
        "type": "image_url",
        "image_url": f"data:image/jpeg;base64,{paths[1]}"
    }
    ])
    response = vision_llm.invoke([message])
    out = response.content.strip()
    out = out.split("\n")
    return out
    


# Gather file paths
answer_key = libinput.get_key()
homework = libinput.get_homework()
base64_data = [homework, answer_key]
os.system('clear')
result = analyse(base64_data)
for line in result:
    print(line)