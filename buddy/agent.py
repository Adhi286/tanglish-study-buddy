import json
from datetime import datetime
from buddy.config import get_client, MODEL
from buddy.tools import TOOLS, execute_tool

TODAY_DATE = datetime.now().strftime("%Y-%m-%d")

SYSTEM_PROMPT = f"""You are Tanglish Study Buddy, an AI assistant for Tamil-medium engineering students.
Always respond in Roman-letter Tanglish (Tamil written using the English alphabet). Do NOT use Tamil script (தமிழ்) or any other script.

CRITICAL RULES:
1. Today's date is {TODAY_DATE}.
2. NEVER guess or invent current dates, exam dates, or countdowns.
3. When the user asks about remaining time, exam dates, or countdowns (e.g., "Innum evlo naal irukku?"), ALWAYS call the `exam_countdown` tool.
4. Use saved memory and tools for all factual context.
"""

def chat(messages, model=MODEL):
    client = get_client()
    full_messages = [{"role": "system", "content": SYSTEM_PROMPT}] + messages
    
    response = client.chat.completions.create(
        model=model,
        messages=full_messages,
        tools=TOOLS,
        tool_choice="auto",
        max_tokens=2500
    )
    
    msg = response.choices[0].message
    
    if msg.tool_calls:
        full_messages.append(msg)
        
        for tool_call in msg.tool_calls:
            result = execute_tool(tool_call.function.name, json.loads(tool_call.function.arguments))
            full_messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(result)
            })
        
        second_response = client.chat.completions.create(
            model=model,
            messages=full_messages,
            tools=TOOLS,
            max_tokens=2500
        )
        return second_response.choices[0].message.content
        
    return msg.content
