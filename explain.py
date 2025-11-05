# Answer Explaination Script
# !!! This script is only used in gui.py, not main.py

import ollama
import gui
from configparser import ConfigParser

# LLM to be used
# This has to be a vision-enabled model
model = "qwen3-vl:8b"

# Prompt for LLM
prompt = """
You are an expert tutor. You will be given:
1. The original assignment.
2. The list of incorrect answers from the student.
3. The list of correct answers.

Your task:
- Explain why the student’s answer is incorrect.
- Clarify the correct reasoning or solution in a way that teaches the concept, not just states the answer.
- Suggest specific, actionable steps the student can take to improve their understanding (e.g., practice strategies, common pitfalls to avoid, or conceptual reminders).

Format your response as follows:
1. **Question [#]**
   - Feedback: [explanation of mistake, clarification of concept, and improvement advice]

Keep your tone encouraging, supportive, and educational. Focus on growth and learning, not just correction.
"""

def promptgen(wrong_answers):
    output = f"{prompt} \n Wrong Answers: {wrong_answers}"
    
    return output

def run(self, hw_path, wrong_answers):
    # TO DO
    # Make LLM give answer explainations for incorrect questions

    # Initialize ollama client from configuration
    config = ConfigParser()
    config.read("config.ini")
    server_address = config.get("General", "Ollama Server")
    client = ollama.Client(host=server_address)
    output = []
    i = 0
    

    for hw_path in hw_path:
        final_response = ""
        currentprompt = promptgen(wrong_answers[i])
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
                    "content": currentprompt,
                    "images": [hw_path],
                }
            ],
            think=False
        )
        for chunk in response:
            thinking = chunk.get("message", {}).get("thinking")
            if thinking:
                self.result.emit(thinking)
            if chunk['message']['content'] == "":
                nocontent = True
            if chunk['message']['content'] != "" and nocontent == True:
                nocontent = False
                self.result.emit("\n")
            self.result.emit(chunk['message']['content'])
            final_response += chunk['message']['content']
        output.append(final_response)
        i += 1
        
    return output