import ollama
import langchain
import langchain
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage
from langchain_core.documents import Document
from PIL import Image
import base64

# models = [vision model, small text model]
models = ['gemma3:latest', 'qwen3:0.6b']
repeat_number = 1

# Specific prompts for the tasks completed. Be very consise, or the LLM may either give the wrong answer entirely, or not format it correctly.
analyse_prompt = """
You are a helpful tool designed to examine a student's homework assignment. You will be given an image to analyse. You will list the answer given by the student, as well as the question number.
If there isn't a question number, then number the questions yourself. You will find out whether the assignment is a free response or multiple choice, and format
your response correspondingly. If the assignment is free response, then give the number the student has circled, or otherwise emphasized (1.2555, 3/4, etc.).
For multiple choice, give the circled or otherwise emphasized letter answer (A, B, C, etc.).You will format your answer as follows, with the words in 
parentheses being placeholders for you to fill; (question number): (student answer). Give no other feedback or response other than what was shown previously.
"""
check_prompt = """
You are a helpful tool designed to compare responses from another large language model. You will be given the responses in a list format after
I say "These are your responses", separated by semicolons. If the responses are very similar, then report True and nothing else. If you are given a fraction and a
decimal number (1/2 vs 0.5, etc), then still report True if they even out to be the same thing. If they are too different to mean the same thing, 
then report False and nothing more.
These are your responses: 
"""
compare_prompt = """
You are a helpful tool designed to examine a student's homework assignment. You will take the list of question numbers and answers, separated by commas, from the student, and
compare those answers to the given answer key, which is formatted the same way. You will format your response as follows, giving no other feedback, with the words in parentheses (dont include 
the parentheses, just execute the action) being placeholders for you to fill in: "(question_number). (True or False, depending on if the student answer is correct or not)"
You can figure out whether you should put true or false if the questions are multiple choice (A, B, C, etc.), by simply comparing the two answers. If the answer 
key says A, but the student says B, then report an incorrect answer. If the questions are free 
response (1.555, 3/4, 6) then you should compare the two answers. If the answer key says 6, but the student says 5, then report an
incorrect answer. There is one exception, and that is if the answer key says 1.57656 but the student says 1.58, then they are still correct due to a simple
error, and you are supposed to still report correct even if there is a rounding error. Only give the question number, a period, and either True or False, no parentheses, 
and in that order. DO NOT INCLUDE THE PARENTHESE, and format the list in a human-readable way. 
You will be given both answers, separated by semicolons, after this sentence.
Here are your answers: 
"""

# Initialize models

vision_llm = ChatOllama(model=models[0])

text_llm = ChatOllama(model=models[1])

def analyse(image_path):
    # Encode image
    with open("/home/ewise/Documents/answer key.png", "rb") as f:
        image_data = base64.b64encode(f.read()).decode("utf-8")
    while True:
        responses = []
        for i in range(0, repeat_number):
            response = ollama.chat(
                model="llava",
                messages=[{
                    "role": "user",
                    "content": analyse_prompt,
                    "images": [image_data]
                }]
            )
            print(response["message"]["content"])
            responses.append(response["message"]["content"])
        if check(responses):
            result = responses[0]
            break
    return result
        

def check(responses):
    combined_responses = ""
    for i in range(0, len(responses)):
        combined_responses += str(responses[i]) + ";"
    print(combined_responses)
    # Send responses with prompt
    response = text_llm.invoke([
        HumanMessage(
            content=check_prompt + combined_responses,
        )
    ]       )
    print(response)

def compare(homework, answer_key):
    responses = []
    while True:
        for i in range(0, repeat_number):
            response = text_llm.invoke([
                HumanMessage(
                    content=compare_prompt + homework + ";" + answer_key
                )
            ]       )
            responses.append(response)
        if check(responses):
                result = responses[0]
                break
    return result