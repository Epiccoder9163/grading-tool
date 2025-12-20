# Script used to gather percentage average of questions

import ollama
from configparser import ConfigParser

prompt = """
You will be given one or more images. Each image will contain either a student’s completed homework or an answer key. 
Your task is to identify which image is the answer key and which is the student’s work. Extract all question numbers and answers from both.

Compare the student’s answers to the correct answers. Mark each question as correct or incorrect. When comparing answers, 
allow for small variations that still mean the same thing. For example, treat answers as correct if they are equivalent, formatted differently, or phrased differently but clearly express the same meaning. Examples include capitalization differences, minor spelling errors, equivalent wording, or mathematically equivalent expressions. Only mark an answer wrong if it is clearly different in meaning or value from the correct answer.

If a student leaves a question blank, record it as blank. If the answer is unreadable, record it as unreadable. 
Only grade questions that appear in both the student’s work and the answer key.

After grading, calculate the percentage score using the number of correct answers divided by the total number of questions, 
multiplied by 100. Round to the nearest whole number.

Your final output must follow this exact format: (percentage score), 
list of wrong answers

List wrong answers in ascending numerical order. 
Each wrong answer must be written as: question_number: student_answer

Example output: 75, 2: b, 6: c, 10: 32
"""
def avg(numquestions, numright):
    avg = numright / numquestions
    output = round(avg * 100)
    return output

def run_basic(homework_list, key_list):
    wrong_answers = []
    numright = 0
    for i in range(0, len(homework_list)):
        if homework_list[i].lower() == key_list[i].lower():
            numright += 1
        if homework_list[i].lower() != key_list[i].lower():
            # i + 1 because the for loop starts at 0, but 0 is (usually) not a question number
            wrong_answers.append(f"{i + 1}: {homework_list[i]}")
    return [avg(len(homework_list), numright), wrong_answers]

def run_full(hw_path, key_path):
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
                        "images": [hw_path, key_path],
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