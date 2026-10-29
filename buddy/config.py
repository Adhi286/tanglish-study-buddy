import os
from dotenv import load_dotenv

load_dotenv()

def get_secret(key: str, default: str = "") -> str:
    # 1. Try environment variables (.env / OS)
    val = os.getenv(key)
    if val:
        return val
    
    # 2. Try Streamlit Secrets (for Streamlit Community Cloud)
    try:
        import streamlit as st
        if key in st.secrets:
            return str(st.secrets[key])
    except Exception:
        pass
        
    return default

GEMINI_API_KEY = get_secret("GEMINI_API_KEY")
TAVILY_API_KEY = get_secret("TAVILY_API_KEY")
MEMORY_FILE = get_secret("MEMORY_FILE", "memory.json")
