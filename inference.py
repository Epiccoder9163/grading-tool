# Script used to inference with LLM

import ollama
from configparser import ConfigParser
from PyQt6.QtGui import QTextCursor
import gui

# Prompt to be used for the LLM
prompt = """
You are given an image of a student’s homework or an answer key. Your job is to extract the written answer for every question. After extracting all answers, you must decide if the assignment needs further review.

Output all answers on one line. Use this format exactly:
(question number): (answer)

Separate each item with a comma and a space. After the final answer, add either true or false in all lowercase.

Rules:

Extract only what is written. Do not check correctness.

Prefer numerical answers. If no number is written, use the letter or the word that is written.

All letters and words must be lowercase.

Do not add parentheses, punctuation, or formatting around answers.

Give exactly one answer per question.

Do not add explanations.

Do not add extra text.

Do not add extra lines.

If you cannot find an answer for any question, output whatever answers you can and end with true.

If all answers are simple (multiple choice or simple numbers), end with false.

If any answer is open ended, long, or complex, end with true.

If the assignment mixes simple and complex questions, end with true.

Example output:
1: 42, 2: b, 3: 17, false
"""




def guirun(path, self):
    # Initialize ollama client from configuration
    config = ConfigParser()
    config.read("config.ini")
    model = config.get("General", "Model")
    server_address = config.get("General", "Ollama Server")

    client = ollama.Client(host=server_address)

    while True:
        output = []
        final_response = ''

        # Run the generation any amount of times as a failsafe for malformed generations
        for i in range(1):
            self.result.emit("\n")
            response = client.chat(
                model=model,
                options={"temperature": 0},
                stream=True,
                messages=[
                    {
                        "role": "system",
                        "content": "Don't overthink your prompt, just answer it simply and consisely. You are an AI OCR tool designed to take homework assignments and produce a list of answers and their corresponding question numbers."
                    },
                    {
                        "role": "user",
                        "content": prompt,
                        "images": [path],
                        "keep_alive": "0s"
                    }
                ],
                think=False
            )
            in_thinking = False

            for chunk in response:
                if chunk.message.thinking and not in_thinking:
                    in_thinking = True
                    self.result.emit("\n")
                    self.result.emit("Thinking:")
                    self.result.emit("\n")

                if chunk.message.thinking:
                    self.result.emit(chunk.message.thinking)
                elif chunk.message.content:
                    if in_thinking:
                        self.result.emit("\n")
                        self.result.emit("Response:")
                        self.result.emit("\n")
                        in_thinking = False
                    self.result.emit(chunk.message.content)
                    final_response += chunk.message.content

            # Save final response
            output.append(final_response)
            self.result.emit("\n")

        if all(x == output[0] for x in output):
            # If they are all the same, continue
            return output[0]
        else:
            # If not, try again
            continue


# Old run function, used in main.py
# !!! Function not being used anymore, will be removed in a future commit
def run(path):
    while True:
        output = []
        final_response = ''

        # Run the generation any amount of times as a failsafe for malformed generations
        for i in range(1):
            response = ollama.chat(
                model=model,
                options={"temperature": 0},
                stream=True,
                messages=[
                    {
                        "role": "system",
                        "content": "Skip reasoning, just give the result"
                    },
                    {
                        "role": "user",
                        "content": prompt,
                        "images": [path],
                    }
                ],
                think=False
            )
            for chunk in response:
                thinking = chunk.get("message", {}).get("thinking")
                if thinking:
                    print(thinking, end='', flush=True)
                print(chunk['message']['content'], end='', flush=True)
                final_response += chunk['message']['content']


            # Save final response
            output.append(final_response)

        if all(x == output[0] for x in output):
            # If they are all the same, continue
            print("Text detection is successful! Returning . . .")
            return output[0]
        else:
            # If not, try again
            print("Model's output is likely inaccurate!")
            print("Trying again . . .")
    
