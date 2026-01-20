# Answer Explaination Script

import ollama
import gui
from configparser import ConfigParser

# Prompt to be used for the LLM (beta)
# The prompt is in a list, as it will be generated on program run, inserting run-specific text to help the AI analyse the prompt more efficiently with less errors
# See function promptgen
prompt_beta = ["You are given ", " images, some of which are a student's homework or an answer key, as shown: \n", "The student got a ", "\n on the assignment", 
"""\n 
Your task is to evaluate all pages as a single assignment by identifying key figures or answers present in the images. 
Using the provided answer key, rubric, or example (if no clear questions and answers are available), determine the correctness of each response. 
When encountering an incorrect answer, identify the specific mistake made by the student and explain why this error would result in a 
deduction of points based on the grading criteria. If there are slight discrepancies between student work and the answer key/example or 
variations from the rubric that do not significantly alter the meaning or correctness of the answer, disregard them. Provide a clear 
explanation for each mistake identified and include any relevant examples to support your reasoning. Your output should be a detailed 
analysis focusing on incorrect answers, including specific mistakes made by the student and reasons for point deductions.

Example output:
1. In question #3, the student mistakenly divided by 4 instead of multiplying by 4 to find the area of a rectangle. 
This results in an incorrect calculation of the total square feet, which leads to an answer that is off by a factor of 4 
(2560 sq ft instead of 640 sq ft). Therefore, there will be a deduction of points for this mistake based on the grading criteria.

2. In question #7(b), the student's solution to the quadratic equation is incorrect due to an error in applying the quadratic formula. 
The student swapped the values of b and c, which results in roots that do not satisfy the original equation. This shows a misunderstanding of 
the quadratic formula and leads to an incorrect answer. As such, there will be a deduction of points for this mistake based on the grading criteria.
"""]

# Prompt for LLM (in legacy mode)
prompt_legacy = """
You’re an expert tutor helping a student learn from their mistakes. You’ll get:

 - The original assignment
 - For each question the student got wrong, give clear, helpful feedback in this format:

Question [#]

Feedback: [Explain why the answer is wrong → clarify the correct concept → give one actionable tip to improve]

Guidelines:
 - If you are given a numerical answer, do not get hung up over the multiple choice answers, use the numerical one.
 - Read all word answers as lowercase words, do not think letter case mismatches are actual errors, disregard case mismatches.
 - Be supportive and encouraging — focus on growth, not blame.
 - Only respond to questions the student got wrong. Skip others.
 - If something’s missing, unclear, or seems like a typo — say so.
 - If the error is too vague to explain — say so, and move on.
 - If the student didn’t show work or reasoning — say so.
 - Some answers should be correct. If there are some, you don't have to note it, just pass by them. Only comment on incorrect answers.
"""
def promptgen(hw, keys, grade):
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
    prompt_out = prompt_beta[0] + str(len(hw) + len(keys)) + prompt_beta[1] + image_des + prompt_beta[2] + str(grade) + prompt_beta[3] + prompt_beta[4]

    print(prompt_out)
    return prompt_out

# Run function (full LLM beta)
def run(hw, keys, grade, self):

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
                "content": promptgen(hw, keys, grade),
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

def legacyrun(self, hw_paths, key_paths, progress_total, progress_index):
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
                    "content": prompt_legacy,
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
