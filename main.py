import ollama
import os
import libinput
from langchain_community.chat_models import ChatOllama
from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import StrOutputParser

# models = [vision model, small text model]
models = ['llava:latest', 'qwen3:0.6b']

# Prompt for the large language model
prompt = """
You will receive two images:  
1. Student’s math homework (each page lists questions with the student’s 
answers).  
2. Teacher’s answer key (same questions with the correct answersh).

**Task**  
1. Use OCR to extract all text from both images.  
2. For each question, compare the student’s answer with the correct 
answer.  
   - Treat answers as equal if the text or numeric value matches exactly, 
ignoring leading/trailing whitespace and case.  
3. Output **only** a Python list of booleans (`True` for a correct answer, 
`False` otherwise), in the same order as the questions.  
4. Do not provide any explanation, formatting, or extra text.  

**Example**  
```
[True, False, True, True, False]
```

Ensure the list length equals the number of questions.


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

os.system('clear')

# Gather file paths
os.system('clear')
answer_key = libinput.get_key()
os.system('clear')
homework = libinput.get_homework()
base64_data = [homework, answer_key]
os.system('clear')
print("Generating a response...")
print("This may take a while")
result = analyse(base64_data)
for line in result:
    print(line)
