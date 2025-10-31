import ollama

# Prompt to be used for the LLM
prompt = """
You have been given a student's homework assignment. Your job is to find the student's answer (this could be numerical or alphabetical) 
and output it as follows, with (answer) being the answer that you found previously, and (question number) 
being the number of the question that corresponds to the answer you found previously; (question number): (answer), (question number): (answer), (question number): (answer)
provide only either the alphabetical or numerical answer, not both. Use the numerical answer first if there is one, if not use the alphabetical answer.
"""

# Model to be used for the LLM
model = "qwen3-vl:8b"

def run(path):
    while True:
        response = ollama.chat(
            model=model,
            # Temperature = 0 reduces randomness
            options={"temperature": 0},
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                    "images": [path],
                }
            ],
        )
        # Run the generation 3 times as a failsafe for malformed generations

        # Run 1
        output = response["message"]["content"]
        print(output)

        response = ollama.chat(
            model=model,
            # Temperature = 0 reduces randomness
            options={"temperature": 0},
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                    "images": [path],
                }
            ],
        )
        
        # Run 2
        output2 = response["message"]["content"]
        print(output2)

        response = ollama.chat(
            model=model,
            # Temperature = 0 reduces randomness
            options={"temperature": 0},
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                    "images": [path],
                }
            ],
        )

        # Run 3
        output3 = response["message"]["content"]
        print(output3)
        if output == output2 == output3:
            # If they are all the same, continue
            print("Text detection is successful! Returning . . .")
            return output
            break
        else:
            # If not, try again
            print("Model's output is likely inaccurate!")
            print("Trying again . . .")
    