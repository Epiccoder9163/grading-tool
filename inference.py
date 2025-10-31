import ollama

# Prompt to be used for the LLM
prompt = """
You have been given a student's homework assignment. Your job is to find the student's answer (this could be numerical or alphabetical) 
and output it as follows, with (answer) being the answer that you found previously, and (question number) 
being the number of the question that corresponds to the answer you found previously; (question number): (answer), (question number): (answer), (question number): (answer)
provide only either the alphabetical or numerical answer, not both. If there is an alphabetical answer, eg. A, B, or C, use that, but if not look for numerical answers
or phrases like x = 10, or just 10, and convert decimals to fractions, so like 0.25 to 1/4.
"""

# Model to be used for the LLM
model = "qwen3-vl:8b"

def run(path):
    while True:
        response = ollama.chat(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                    "images": [path],
                }
            ],
        )
        output = response["message"]["content"]
        print(output)
        output2 = response["message"]["content"]
        print(output2)
        if output == output2:
            print("Text detection is successful! Returning . . .")
            return output
            break
        else:
            print("Model's output is likely inaccurate!")
            print("Trying again . . .")
    