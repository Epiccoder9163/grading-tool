# Script used to inference with LLM

import ollama
from configparser import ConfigParser
from PyQt6.QtGui import QTextCursor
import gui

# Prompt to be used for the LLM (beta)
# The prompt is in a list, as it will be generated on program run, inserting run-specific text to help the AI analyse the prompt more efficiently with less errors
# See function promptgen
prompt_beta = ["You are given ", " images, some of which are a student's homework or an answer key, as shown: \n", """\n 
Your task is to evaluate all pages as a single assignment. Identify any key figures or answers present in the images. Based on this analysis, 
determine the correctness of each response using the provided answer key, rubric, or example (if no clear questions and answers are available). 
Calculate an overall grade according to these criteria. If there are slight discrepancies between student work and the answer key/example or 
variations from the rubric that do not significantly alter the meaning or correctness of the answer, disregard them. However, do not overlook 
any significant errors, even if they are minor changes in interpretation. Provide your final grade as a whole number, rounding to the nearest 
integer (e.g., 2/3 questions correct should be graded as 67). 
Your output should only include this final average score in the following format:
average

Example output:
93
"""]


# Prompt to be used for the LLM (in legacy mode)
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
    # Generate the prompt dynamically to distinguish the image types to the model
    # The image types may vary based on the context (ex. 3 homework images and 2 key images), so this will distinguish them to the LLM
    
    # Generates the image discriptions based on the images in question
    image_des = ""
    image_count = 0
    for i in range(len(hw)):
        image_count += 1
        image_des += f"\nimage {str(image_count)}: homework page {str(i + 1)}"
    for i in range(len(keys)):
        image_count += 1
        image_des += f"\nimage {str(image_count)}: answer key page {str(i + 1)}"

    # Add together the prompt list and add the generated items
    prompt_out = prompt_beta[0] + str(len(hw) + len(keys)) + prompt_beta[1] + image_des + prompt_beta[2]

    print(prompt_out)
    return prompt_out

# Run function (full LLM beta)
def run(hw, keys, self):

    # Initialize ollama client from configuration
    config = ConfigParser()
    config.read("config.ini")
    # Grab model config
    model = config.get("General", "Model")
    # Grab server config
    server_address = config.get("General", "Ollama Server")

    # Set ollama server from config
    client = ollama.Client(host=server_address)
    
    # Build combined paths list from hw and key lists
    paths = []
    paths.extend(hw)
    paths.extend(keys)

    self.result.emit("\n")
    response = client.chat(
        # Set model from configuration
        model=model,

        # Temperature (0) tells the model to not change its answer each time it is run, in an attempt to produce the same result
        # each time the program is run with the same prompt
        options={"temperature": 0},

        # Stream tells the function to continually add new output tokens to a list, this is used to show the model thinking and responding
        # in real time, rather than having to wait for the model to finish responding to see its entire output at once
        stream=True,
        messages=[
            {
                # System prompt changes how the model acts towards your main prompt
                "role": "system",
                "content": "You are a professional grader that should grade assignments exactly like a human grader would."
            },
            {
                "role": "user",
                # Dynamically generate the prompt based on certain information given
                "content": promptgen(hw, keys),
                # Use combined paths list
                "images": paths,
            }
        ]
    )

    # Set temporary variables
    in_thinking = False
    final_response = []

    # If model is in thinking stage (when applicable) show thinking messages
    # When model is finished thinking, show real response
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

    # Return final response
    return "".join(final_response)




# Run function (legacy mode)
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
        # This is set to 1 (generate one time) for speed
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
    