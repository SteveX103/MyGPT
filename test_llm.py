from services.llm_service import generate_response


prompt = """
Explain cloud computing in 3 simple points.
"""


answer = generate_response(prompt)


print("\n========== ANSWER ==========\n")

print(answer)