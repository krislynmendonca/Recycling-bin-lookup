import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

# Read API configuration from environment variables
API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL")
MODEL_NAME = "qwen2.5:3b-instruct-q4_K_M"

client = OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL
)

def call_llm(prompt: str) -> str:
    """
    General LLM api caller, return raw model response string.
    Args:
        prompt: User prompt sent to large language model
    Returns:
        Stripped raw text response from LLM
    """
    response = client.chat.completions.create(
        model=MODEL_NAME,
        temperature=0,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()
