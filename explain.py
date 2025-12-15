# Answer Explaination Script
# !!! This script is only used in gui.py, not main.py

import ollama
import gui
from configparser import ConfigParser

# Prompt for LLM
prompt = """
You’re an expert tutor helping a student learn from their mistakes. You’ll get:

The original assignment
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
Some answers should be correct. If there are some, you don't have to note it, just pass by them. Only comment on incorrect answers.
"""

def run(self, hw_paths, key_paths, progress_total, progress_index):
    # Initialize ollama client from configuration
    config = ConfigParser()
    config.read("config.ini")
    server_address = config.get("General", "Ollama Server")
    model = config.get("General", "Model")
    client = ollama.Client(host=server_address)
    output = []

    # Debugging messages
    print(hw_paths)
    print(key_paths)

    for i in range(0, len(hw_paths)):
        final_response = ""
        self.result.emit("\n")
        
        # Debugging messages
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
                    "content": prompt,
                    "images": [hw_paths[i]]
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
                
        output.append(final_response)
        progress_index += 1
        self.progress.emit(int((progress_index / progress_total) * 100))
    
    return output, progress_index
