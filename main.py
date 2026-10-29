import sys
from buddy.agent import chat

history = []

print("Tanglish Study Buddy ready. Type 'exit' to quit.\n")

while True:
    try:
        q = input("You: ").strip()
        if not q:
            continue
        if q.lower() in ["exit", "quit"]:
            break
            
        history.append({"role": "user", "content": q})
        ans = chat(history)
        history.append({"role": "assistant", "content": ans})
        
        print(f"\nBuddy: {ans}\n")
    except KeyboardInterrupt:
        break
    except Exception as e:
        print(f"\nError: {e}\n")
