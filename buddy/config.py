import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

MEMORY_FILE = "memory.json"
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
MODEL = os.getenv("MODEL", "nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B")

def get_client():
    load_dotenv(override=True)
    api_key = os.getenv("NEBIUS_API_KEY")
    return OpenAI(
        base_url="https://api.tokenfactory.nebius.com/v1/",
        api_key=api_key,
        timeout=90.0,
        max_retries=3
    )

client = get_client()
