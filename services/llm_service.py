import ollama


DEFAULT_MODEL = "gemma3-local" # Replace with your desired model name


def generate_response(
    prompt: str,
    model: str = DEFAULT_MODEL
) -> str:

    if not prompt or not prompt.strip():
        raise ValueError("Prompt cannot be empty")

    response = ollama.chat(
        model=model,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]