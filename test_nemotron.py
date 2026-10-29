"""Day-1 smoke test: one call to Nemotron on Nebius Token Factory."""
from buddy.config import client, MODEL

r = client().chat.completions.create(
    model=MODEL,
    messages=[{"role": "user", "content": "Say hello in Tanglish in one line."}],
    max_tokens=1500,
)
print(r.choices[0].message.content)
