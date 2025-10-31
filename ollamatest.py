import ollama

MODEL = "qwen3-vl:8b"

prompt = """
You have been given a student's homework assignment. Your job is to find the student's answer (this could be numerical or alphabetical) 
and output it as follows, with (answer) being the answer that you found previously, and (question number) 
being the number of the question that corresponds to the answer you found previously; (question number): (answer), (question number): (answer), (question number): (answer)
provide only either the alphabetical or numerical answer, not both. If there is an alphabetical answer, eg. A, B, or C, use that, but if not look for numerical answers
or phrases like x = 10, or just 10, and convert decimals to fractions, so like 0.25 to 1/4.
"""
# Path to your image
IMAGE_PATH = "/home/elliott/Documents/GitHub/grading-tool/homework.png"

# Send a message with both text and image
response = ollama.chat(
    model=MODEL,
    messages=[
        {
            "role": "user",
            "content": prompt,
            "images": [IMAGE_PATH],  # list of image paths or raw bytes
        }
    ],
)
print(response["message"]["content"])
