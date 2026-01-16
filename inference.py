# Script used to inference with LLM

import ollama
from configparser import ConfigParser
from PyQt6.QtGui import QTextCursor
import gui

# Prompt to be used for the LLM
prompt_legacy = """
You are given an image of either a student's homework or an answer key. Your task is to extract the answers provided for each question.

For each question, output the answer in the format:
(question number): (answer)

Rules:
- Only extract what is written—do not verify correctness.
- Prefernumerical answers; if none, use a alphabetical answer or a full word (or words) if available.
- If you get an alphabetical or word answer, then put it in all lowercase. Also, only give the letter or word, no parenthesis or other formatting.
- Output only one answer per question, although that answer could be made up of multiple words.
- Do not include explanations or extra formatting.
- Avoid redundant checks.
- Don't make new lines for each answer in your final response, put it all on one line.

Example output:
1: 42, 2: b, 3: 17
"""

def promptgen(hw, keys):
    # Generate the prompt dynamically to distinguish images to the model

    print("hello")

def run(path, self):
    # Initialize ollama client from configuration
    config = ConfigParser()
    config.read("config.ini")
    model = config.get("General", "Model")
    server_address = config.get("General", "Ollama Server")

    client = ollama.Client(host=server_address)




def legacyrun(path, self):
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
                        "content": "Don't overthink your prompt, just answer it."
                    },
                    {
                        "role": "user",
                        "content": prompt_legacy,
                        "images": [path],
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
    