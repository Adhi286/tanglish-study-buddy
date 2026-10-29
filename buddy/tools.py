import os
from tavily import TavilyClient
from buddy import memory
from buddy import skills
from buddy.config import TAVILY_API_KEY

tavily_client = TavilyClient(api_key=TAVILY_API_KEY) if TAVILY_API_KEY else None

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "save_memory",
            "description": "Save important user context, exam dates, or weak topics to local memory.",
            "parameters": {
                "type": "object",
                "properties": {
                    "key": {"type": "string", "description": "Key like 'exam_date_Computer_Networks' or 'weak_topics'"},
                    "value": {"description": "Value to store"}
                },
                "required": ["key", "value"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "forget_memory",
            "description": "Remove a key from local memory.",
            "parameters": {
                "type": "object",
                "properties": {
                    "key": {"type": "string"}
                },
                "required": ["key"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "exam_countdown",
            "description": "Calculate remaining days for saved exam dates.",
            "parameters": {"type": "object", "properties": {}}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "study_plan",
            "description": "Generate a daily study hours distribution weighted by exam urgency and weak topics.",
            "parameters": {
                "type": "object",
                "properties": {
                    "daily_hours": {"type": "number", "description": "Total available study hours per day"}
                },
                "required": ["daily_hours"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": "Search the web using Tavily API for current engineering topics or real-time info.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query"}
                },
                "required": ["query"]
            }
        }
    }
]

def execute_tool(name, args):
    if name == "save_memory":
        return memory.remember(args["key"], str(args["value"]))
    elif name == "forget_memory":
        return memory.forget(args["key"])
    elif name == "exam_countdown":
        return skills.exam_countdown()
    elif name == "study_plan":
        return skills.study_plan(args.get("daily_hours", 4))
    elif name == "web_search":
        if not tavily_client:
            return {"error": "TAVILY_API_KEY is not set in .env"}
        try:
            res = tavily_client.search(query=args["query"], max_results=3)
            snippets = [{"title": r.get("title"), "content": r.get("content")[:300]} for r in res.get("results", [])]
            return {"results": snippets}
        except Exception as e:
            return {"error": str(e)}
    return {"error": f"Unknown tool: {name}"}
