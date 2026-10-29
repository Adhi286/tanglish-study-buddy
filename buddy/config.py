import os
from dotenv import load_dotenv
from openai import Client

load_dotenv()

def get_secret(key: str, default: str = "") -> str:
    val = os.getenv(key)
    if val:
        return val
    try:
        import streamlit as st
        if key in st.secrets:
            return str(st.secrets[key])
    except Exception:
        pass
    return default

NEBIUS_API_KEY = get_secret("NEBIUS_API_KEY")
TAVILY_API_KEY = get_secret("TAVILY_API_KEY")
MEMORY_FILE = get_secret("MEMORY_FILE", "memory.json")

# Updated to a known valid Nebius model ID
MODEL = get_secret("MODEL", "meta-llama/Meta-Llama-3.1-8B-Instruct")

def get_client():
    api_key = get_secret("NEBIUS_API_KEY")
    if not api_key:
        raise ValueError("NEBIUS_API_KEY is not set. Please set it in .env or Streamlit Secrets.")
    
    return Client(
        base_url="https://api.studio.nebius.ai/v1/",
        api_key=api_key
    )
