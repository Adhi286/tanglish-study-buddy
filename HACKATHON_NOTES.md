# Tanglish Study Buddy - Hackathon Notes & Progress Log

**Track:** Personal AI  
**Hackathon:** Nebius x NVIDIA Global AI Hackathon  
**Developer:** Adhibalan P. (3rd Year CSBS, SVCT)  
**Target Completion:** October 30, 2026  

---

## 1. Project Architecture Overview
- **Primary Model (Dev):** `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B` via Nebius Token Factory
- **Demo Model:** `nvidia/nemotron-3-super-120b-a12b`
- **Tooling Integrations:** Local JSON persistent memory (`memory.json`), custom skill calculators (`exam_countdown`, `study_plan`), Tavily Web Search API
- **Target Deliverables:** Public GitHub repo (MIT License), CLI & Web UI demo, <3m YouTube walkthrough video

---

## 2. Key Architecture Fixes & Lessons Learned

### A. Nebius Token Factory Integration
1. **Tool Loop & Payload Serialization:**
   - **Issue:** OpenAI Python SDK defaults pass raw `ChatCompletionMessage` objects on tool response loops, causing schema validation errors with Token Factory routing.
   - **Fix:** Explicitly serialized assistant tool call messages into dict structures (`role`, `content`, `tool_calls` array with `id`, `type`, `function`).

2. **Tool System Prompt Guard:**
   - **Issue:** Nemotron models occasionally answered time/date questions directly without invoking registered tools.
   - **Fix:** Injected explicit system constraints (`CRITICAL RULES`: force `exam_countdown` for timing questions) and dynamically passed today's date (`YYYY-MM-DD`).

3. **Authentication & API Key Management:**
   - **Issue:** Stale client instances and environment variable overrides led to recurring `401 Unauthorized` responses.
   - **Fix:** Updated `buddy/config.py` with a dynamic `get_client()` factory pattern that reloads `.env` parameters explicitly before API dispatch.

4. **Tavily Web Search Token Management:**
   - **Issue:** Raw Tavily web search payloads occasionally blew past output limits, causing downstream model context errors.
   - **Fix:** Trimmed web search responses to top 3 concise result snippets (300 characters max per content snippet) in `buddy/tools.py`.

---

## 3. Model Benchmark & Quality Comparison

| Feature / Metric | Nemotron 3 Nano (30B A3B) | Nemotron 3 Super (120B A12B) |
| :--- | :--- | :--- |
| **Primary Use Case** | Rapid CLI iterations, localized agent responses | Final demo presentation, complex multi-turn reasoning |
| **Tanglish Prompt Adherence** | Strong script enforcement; occasional English phrasing bleed | Excellent native Roman-script Tanglish tone consistency |
| **Tool Calling Reliability** | High (with strict system prompt guards) | Exceptional (native multi-tool planning without extra prompting) |
| **Response Latency** | Low latency (~60 tok/s) | Moderate latency (~127 tok/s on Token Factory) |
| **Cost Profile** | $0.06 / $0.24 per 1M tokens | $0.30 / $0.90 per 1M tokens |

---

## 4. Pending Roadmap to Submission
- [x] Fix tool loop serialization and 401 Auth handling
- [x] Integrate `exam_countdown`, `study_plan`, and `save_memory` skills
- [ ] Add fresh Tavily API key and verify end-to-end `web_search` output
- [ ] Build Web Interface frontend (Streamlit / FastHTML / HTML-JS)
- [ ] Record <3m YouTube demonstration video
- [ ] Complete Devpost project submission prior to deadline
