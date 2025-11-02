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
        output = []
        final_response = ''

        # Run the generation any amount of times as a failsafe for malformed generations
        for i in range(1):
            response = ollama.chat(
                model=model,
                options={"temperature": 0},
                stream=True,
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                        "images": [path],
                    }
                ],
                think=False
            )
            for chunk in response:
                segment = chunk['message']['content']
                print(segment, end='', flush=True)
                final_response += segment

            # Save final response
            output.append(final_response)

        if all(x == output[0] for x in output):
            # If they are all the same, continue
            print("Text detection is successful! Returning . . .")
            return output[0]
        else:
            # If not, try again
            print("Model's output is likely inaccurate!")
            print("Trying again . . .")
    