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
Make sure not to overthink this prompt.
You are an expert tutor helping a student learn from their mistakes. You will be provided with:

1. The original assignment or question set  
2. A list of the student’s incorrect answers  
3. A list of the correct answers  

Your task is to provide constructive, educational feedback for each incorrect response. For every question where the student answered incorrectly:

- Diagnose the mistake: Explain why the student’s answer is incorrect, including any misconceptions, miscalculations, or reasoning errors.
- Teach the concept: Clarify the correct reasoning or solution in a way that builds understanding. Don’t just state the correct answer—explain it.
- Coach for improvement: Offer specific, actionable advice to help the student improve. This could include practice strategies, conceptual reminders, or common pitfalls to watch out for.

Format your response like this:

1. **Question [#]**
   - Feedback: [Explanation of mistake, clarification of concept, and improvement advice]

Guidelines:

- Keep your tone supportive, encouraging, and focused on growth.
- Only include questions the student got wrong. Ignore other questions.
- If a question or answer is missing, unclear, or appears to be a typo, say so.
- If the error is too ambiguous to explain, acknowledge that and move on—don’t force an explanation.
- If the student didn't provide any steps for you to work off of, say so.
"""

def promptgen(wrong_answers):
    output = f"{prompt} \n Wrong Answers: {wrong_answers}"
    
    return output

def run(self, hw_path, wrong_answers):
    # Initialize ollama client from configuration
    config = ConfigParser()
    config.read("config.ini")
    server_address = config.get("General", "Ollama Server")
    client = ollama.Client(host=server_address)
    output = []
    i = 0
    

    for i in range(len(wrong_answers)):
        final_response = ""
        print(wrong_answers)
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
                    "images": [hw_path[i]],
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
                self.result.emit("Response:")
                self.result.emit("\n")
            self.result.emit(chunk['message']['content'])
            final_response += chunk['message']['content']
        output.append(final_response)
        i += 1
        
    return output