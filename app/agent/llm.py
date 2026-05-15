import os

from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()


client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)


MODEL_NAME = "llama-3.3-70b-versatile"


def generate_response(system_prompt, user_prompt):

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ],
        temperature=0.2,
    )

    return (
        response
        .choices[0]
        .message
        .content
    )