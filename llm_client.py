import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

# Backend switch: ollama / bailian, default to local Ollama
BACKEND = os.getenv("LLM_BACKEND", "ollama")

# ========== Local Ollama config (original logic fully preserved) ==========
OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY", "ollama")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:3b-instruct-q4_K_M")

ollama_client = OpenAI(
    api_key=OLLAMA_API_KEY,
    base_url=OLLAMA_BASE_URL
)

# ========== Added: Alibaba Cloud Bailian cloud API config ==========
BAILIAN_API_KEY = os.getenv("BAILIAN_API_KEY")
BAILIAN_BASE_URL = os.getenv("BAILIAN_BASE_URL")
BAILIAN_MODEL = os.getenv("BAILIAN_MODEL", "qwen3-flash")

bailian_client = OpenAI(
    api_key=BAILIAN_API_KEY,
    base_url=BAILIAN_BASE_URL
)

def call_llm(prompt: str) -> str:
    """
    General LLM api caller, return raw model response string.
    Args:
        prompt: User prompt sent to large language model
    Returns:
        Stripped raw text response from LLM
    """
    if BACKEND == "bailian":
        response = bailian_client.chat.completions.create(
            model=BAILIAN_MODEL,
            temperature=0,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
    else:
        # Default: local Ollama, original logic unchanged
        response = ollama_client.chat.completions.create(
            model=OLLAMA_MODEL,
            temperature=0,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
    return response.choices[0].message.content.strip()
