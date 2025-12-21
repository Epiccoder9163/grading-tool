# Answer Explaination Script
# !!! This script is only used in gui.py, not main.py

import ollama
import gui
from configparser import ConfigParser

# Prompt for LLM
prompt = """
You are an expert tutor. Your job is to give feedback only on the questions the student answered incorrectly. You will receive the assignment and the student’s answers.

For each incorrect question, output exactly:

Question [#]
Feedback: why the answer is wrong → the correct concept or method → one specific improvement tip

Rules:

Use the student’s numerical answer as the basis for evaluation; ignore multiple‑choice letters.

Treat all word answers as lowercase; ignore capitalization differences.

Skip correct answers entirely.

Be supportive and focused on learning, not blame.

If an answer is missing, unclear, or looks like a typo, state that.

If the mistake is too vague to explain, say so briefly.

If no reasoning or work is shown where it is needed, note that.

Keep explanations concise, accurate, and concept‑focused.

Do not add extra commentary, formatting, or sections beyond the required structure.
"""

def run(self, hw_paths, key_paths, progress_total, progress_index):
    # Initialize ollama client from configuration
    config = ConfigParser()
    config.read("config.ini")
    server_address = config.get("General", "Ollama Server")
    model = config.get("General", "Model")
    client = ollama.Client(host=server_address)
    output = []

    for i in range(0, len(hw_paths)):
        final_response = ""
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
                    "content": prompt,
                    "images": [hw_paths[i]],
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
                
        output.append(final_response)
        progress_index += 1
        self.progress.emit(int((progress_index / progress_total) * 100))
    
    return output, progress_index
