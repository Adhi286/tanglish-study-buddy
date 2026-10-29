"""Lists NVIDIA / Nemotron models available on your Nebius Token Factory account."""
from buddy.config import client

models = [m.id for m in client().models.list()]
hits = [m for m in models if "nemotron" in m.lower() or m.lower().startswith("nvidia/")]
print("NVIDIA / Nemotron models:" if hits else "No Nemotron match. All models:")
for m in (hits or models):
    print(" -", m)
