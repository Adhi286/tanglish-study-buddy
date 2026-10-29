# Tanglish Study Buddy

A private, always-on study assistant for Tamil-medium engineering students.
Talks in Tanglish, remembers your subjects and exams locally, and searches the web when needed.

**Hackathon:** Nebius x NVIDIA Global AI Hackathon, Personal AI track

## How it uses Nebius + NVIDIA
- **NVIDIA Nemotron** model for all reasoning and replies
- **Nebius Token Factory** (OpenAI-compatible API) for inference
- **Tavily** for web search (optional)

## Setup
```bash
git clone <this-repo>
cd tanglish-study-buddy
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env      # add NEBIUS_API_KEY (and TAVILY_API_KEY)
python list_models.py     # pick a Nemotron model ID, put it in .env as NEBIUS_MODEL_ID
python test_nemotron.py   # smoke test
python main.py            # chat
```

## Features
- Persistent memory (local `memory.json`, you own your data)
- Tool calling: save/forget memory, web search
- Tanglish explanations, step by step

## License
MIT
