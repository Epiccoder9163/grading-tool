# Answer Explaination Script
# !!! This script is only used in gui.py, not main.py

import ollama
import gui
from configparser import ConfigParser

# LLM to be used
# This has to be a vision-enabled model
model = "qwen3-vl:8b"

config = ConfigParser()
config.read(gui.path)
server_address = config.get("General", "Ollama Server")

client = ollama.Client(host=server_address)

def explain(path, question_list, wrong_answers):
    # TO DO
    # Make LLM give answer explainations for incorrect questions
    print("Nothing here yet!")