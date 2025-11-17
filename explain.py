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
You’re an expert tutor helping a student learn from their mistakes. You’ll get:

The original assignment
The student’s incorrect answers
The correct answers
For each question the student got wrong, give clear, helpful feedback in this format:

Question [#]

Feedback: [Explain why the answer is wrong → clarify the correct concept → give one actionable tip to improve]
Guidelines:
If you are given a numerical answer, do not get hung up over the multiple choice answers, use the numerical one.
Read all word answers as lowercase words, do not think letter case mismatches are actual errors, disregard case mismatches.
Be supportive and encouraging — focus on growth, not blame.
Only respond to questions the student got wrong. Skip others.
If something’s missing, unclear, or seems like a typo — say so.
If the error is too vague to explain — say so, and move on.
If the student didn’t show work or reasoning — say so.
"""

def promptgen(wrong_answers, answers):
    wrong_answers_lower = []
    for i in range(len(wrong_answers)):
        wrong_answers_lower.append(wrong_answers[i].lower())
    output = f"{prompt} \n Wrong Answers: {wrong_answers_lower} \n Correct Answers: {answers}"
    
    return output

def run(self, hw_paths, wrong_answers, student_answers, key_answers, progress_total, progress_index):
    # Initialize ollama client from configuration
    config = ConfigParser()
    config.read("config.ini")
    server_address = config.get("General", "Ollama Server")
    client = ollama.Client(host=server_address)
    output = []

    for i in range(len(hw_paths)):
        final_response = ""
        wrong_answers_active = []
        for x in range(len(student_answers[i])):
            try:
                if wrong_answers[x] == student_answers[i][x]:
                    wrong_answers_active.append(wrong_answers[x])
            except IndexError:
                break
        currentprompt = promptgen(wrong_answers_active, key_answers[i])
        self.result.emit("\n")
        print(hw_paths[i])
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
                    "images": hw_paths[i]
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
        progress_index += 1
        self.progress.emit(int((progress_index / progress_total) * 100))
    
    return output, progress_index