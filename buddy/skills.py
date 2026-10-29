"""Reusable skills built on top of persistent memory."""
import re
from datetime import date, datetime

from . import memory

_FORMATS = ["%Y-%m-%d", "%b %d", "%B %d", "%d %b", "%d %B"]


def _parse(text: str):
    today = date.today()
    t = re.sub(r"(\d)(st|nd|rd|th)\b", r"\1", text.strip().replace(",", ""))
    for fmt in _FORMATS:
        try:
            d = datetime.strptime(t, fmt).date()
        except ValueError:
            continue
        if "%Y" not in fmt:
            d = d.replace(year=today.year)
            if d < today:
                d = d.replace(year=today.year + 1)
        return d
    return None


def _exams():
    today = date.today()
    out = []
    for key, val in memory.load().items():
        if key.startswith("exam_date_"):
            d = _parse(str(val))
            if d:
                out.append((key[len("exam_date_"):].replace("_", " "), d, (d - today).days))
    return sorted(out, key=lambda x: x[2])


def exam_countdown() -> str:
    exams = _exams()
    if not exams:
        return "No exam dates saved yet. Ask the student for their exam dates."
    return "\n".join(f"- {n}: {d.strftime('%b %d')} ({days} days left)" for n, d, days in exams)


def study_plan(hours_per_day=3) -> str:
    exams = _exams()
    if not exams:
        return "No exam dates saved yet. Ask the student for their exam dates first."
    hours = float(hours_per_day)
    weights = [1 / max(days, 1) for _, _, days in exams]
    total = sum(weights)
    lines = [f"Daily study budget: {hours:g} hours (closer exams get more time)"]
    for (name, d, days), w in zip(exams, weights):
        lines.append(f"- {name}: {hours * w / total:.1f} h/day, exam {d.strftime('%b %d')} ({days} days left)")
    weak = [(k[len('weak_'):].replace("_", " "), v) for k, v in memory.load().items() if k.startswith("weak_")]
    if weak:
        lines.append("Weak topics to focus on:")
        lines += [f"- {s}: {t}" for s, t in weak]
    return "\n".join(lines)


SKILL_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "exam_countdown",
            "description": "Show how many days are left for each saved exam.",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "study_plan",
            "description": "Build a daily study-time split across saved exams (closer exams get more hours) and list saved weak topics.",
            "parameters": {
                "type": "object",
                "properties": {"hours_per_day": {"type": "number", "description": "Hours the student can study per day"}},
            },
        },
    },
]
