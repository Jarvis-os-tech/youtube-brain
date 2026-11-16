---
video_id: JA_KKpHk8Ww
title: "Why You Shouldn't Use One LLM for Everything | Lesson:11 #ai #Ollama #OpenWebUI #Gemma #FastMCP"
url: https://www.youtube.com/watch?v=JA_KKpHk8Ww
watched: 2026-10-30 22:12
source: chrome:Default
topic: agents
indexed: 2026-11-13T02:46:45+00:00
type: youtube-note
source_url: https://www.youtube.com/watch?v=JA_KKpHk8Ww
tags: [youtube, youtube/agents]
---


## Core Concept
This lesson is about local model routing and dynamic load balancing in an offline supermarket help-desk multi-agent system: instead of sending every request to one heavy LLM, an intent router evaluates query complexity on the fly and dispatches low-overhead classification work to an ultra-fast small model (Gemma 2B) while reserving multimodal analysis, complex document context, and final response generation for a heavier reasoning model (Gemma 4), with automatic failover and a VRAM-aware circuit breaker to keep the system stable.

## Key Takeaways
- Lesson 11 in an AI learning series; the previous lesson covered multimodal vision agents.
- The system is an offline supermarket help-desk AI handling text and visual inputs such as product photos and receipts.
- Stack mentioned: local Ollama execution, Gemma 4 (reasoning tier), Gemma 2B (fast SLM tier), local FastMCP tool servers, a local SQLI database for product inventory and pricing, PDF documents for return policies and holiday store hours, and an Open Web UI front end.
- Example prompts: attach a fruit photo and ask "Do you sell this fruit?"; attach a receipt and ask "Can I return the product in the receipt?"; also "What is the capital of USA?"
- The intent router evaluates input complexity and routes low-overhead tasks (rapid intent classification, keyword extraction, JSON metadata parsing) to the fast SLM tier (Gemma 2B), which runs in fractions of a second without locking GPU cycles.
- Based on the identified intent (product, return policy, store policy/working hours, or vision task), control transfers to the respective domain agent, which queries local tools, the SQLI database, policy documents, or store schedules.
- Multimodal analysis, complex document context, and final user response generation are offloaded to the reasoning LLM tier (Gemma 4), which compiles and formats the synthesized response before returning it to the UI.
- `server_wrapper.py` instantiates the help desk with a dynamic router configuration and routes network traffic into process query; the intent router dispatches the user prompt to the fast model tier instead of invoking heavy parameters to categorize incoming text.
- The `call_llm` method is the core dispatcher: it inspects incoming requests, routes them to the correct model tier, logs latency metrics, and handles automatic failover. It checks the tier parameter (`fast` or `reasoning`) or the presence of an image/score path, measures execution duration in seconds, and prints router logs. If the reasoning model hits an out-of-memory or timeout error, it automatically falls back to the fast model to preserve system stability.
- `mcp_servers.py` is the data/tool layer housing standalone execution functions that read from SQLI databases and PDF policies to supply verified facts back to the agent.
- For the intent task the agent used Gemma 2, while for reasoning MCP tool execution it used Gemma 4. A token comparison was shown, but no figures were given in the transcript.
- Pros of local model routing and dynamic load balancing: significantly reduced latency, resource and compute efficiency, built-in system fault tolerance, task-tailored model specialization.
- Cons: increased architectural complexity, model context overhead and VRAM churn, risk of routing misclassifications, inconsistent response output formats.
- A circuit breaker monitors VRAM/memory usage in real time: on the safe path, local Gemma 4 processes the full-resolution image and returns a high-quality response; on the high-memory path, the circuit breaker trips to prevent a crash and routes the request through one of two fallbacks — degrade (shrink the image or reduce context size for lower-resource local inference) or offload (hand off to a cloud API or a smaller fallback model). The user receives either the full-quality answer or a fallback response with a notice that quality was adjusted.

## Technical Details
- File paths involved:
```
server_wrapper.py
mcp_servers.py
```
- Model tiers: fast SLM tier `Gemma 2B` (intent classification, keyword extraction, JSON metadata parsing); reasoning LLM tier `Gemma 4` (multimodal analysis, complex document context, final response generation).
- `call_llm` dispatcher parameters/logic: tier (`fast` or `reasoning`), presence of image/score path, execution duration measured in seconds, router logs printed; automatic fallback from reasoning tier to fast tier on out-of-memory or timeout.
- Data sources: local SQLI database (product inventory and pricing); PDF documents (return policies, holiday store hours).
- Tooling/front end: local FastMCP tool servers; Open Web UI front end; local Ollama execution.
- Circuit breaker: real-time VRAM/memory monitoring with safe path (full-resolution image, high-quality response) and high-memory path (trip + degrade or offload fallbacks).

## Questions
- The transcript garbles the exact function names in `mcp_servers.py` (rendered roughly as "query and score inventory, search and score turn or score policy, get and score and score hours"); the precise identifiers should be verified against the source.
- No latency or token figures are provided despite a "token comparison" being shown; the actual numbers should be checked in the code or video visuals.
- The transcript refers to the reasoning tier as the "hyperparameter reasoning LLM tier"; whether this means "high-parameter" or something else should be verified.
- The fast tier is called both "Gemma 2B" and "Gemma 2" in different places; it is unclear whether these refer to the same model.
- The handling of off-topic queries such as "What is the capital of USA?" is not explained.
- The circuit breaker's VRAM/memory thresholds and the exact meaning of "image or score path" in `call_llm` are not specified.
- Whether the degrade/offload fallbacks preserve the original response format consistently is not detailed.
<!-- yt-brain:related -->

## Related

- [[youtube/YouTube Knowledge Base|◻️ YouTube Knowledge Base]]
- [[youtube/agents|📁 AI Agents & Orchestration]]
- [[index|🏛️ JARVIS Memory Vault]]

### Related notes

- [[youtube/agents/2026-11-13-building-a-reflective-agentic-rag-system-lesson-17-ai-agenti|Building a Reflective Agentic RAG System (Lesson: 17) #AI #AgenticRAG #Ollama #Gemma #FastMCP]] · relevance 0.19
- [[youtube/agents/2026-11-13-the-secret-to-advanced-ai-multi-step-reasoning-explained-les|The Secret to Advanced AI: Multi-Step Reasoning Explained (Lesson: 2) #Gemma4 #ollama #ai #ajagent]] · relevance 0.11
- [[youtube/dev-craft/2026-11-13-build-your-first-local-ai-agent-python-tutorial-lesson-01-ai|Build Your First Local AI Agent (Python Tutorial) (Lesson: 01) #AIAgent #Gemma4 #Ollama #ai]] · relevance 0.10
- [[youtube/agents/2026-11-13-fastmcp-python-building-local-agent-tools-step-by-step-lesso|FastMCP & Python: Building Local Agent Tools Step-by-Step (Lesson:9) #ai #mcp #ollama #gemini]] · relevance 0.09

<!-- /yt-brain:related -->
