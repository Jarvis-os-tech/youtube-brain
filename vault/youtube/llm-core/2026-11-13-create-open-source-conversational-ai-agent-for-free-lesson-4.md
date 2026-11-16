---
video_id: Bum_TOaER04
title: "Create Open-Source Conversational AI Agent for Free! (Lesson:4) #LocalAI #Ollama #AIAgents #gemini"
url: https://www.youtube.com/watch?v=Bum_TOaER04
watched: 2026-10-30 22:01
source: chrome:Default
topic: llm-core
indexed: 2026-11-13T02:48:58+00:00
type: youtube-note
source_url: https://www.youtube.com/watch?v=Bum_TOaER04
tags: [youtube, youtube/llm-core]
---


## Core Concept
The video demonstrates enhancing a local open-source conversational AI agent (built in a previous lesson, running via Ollama/Gemma) by adding memory and conversation state management: a dedicated conversation session object that ingests each interaction as standard chat payloads, trims history to a configurable maximum number of turns while keeping the system prompt pinned and avoiding orphan tool responses, and persists the full session to disk for cross-session reuse.

## Key Takeaways
- Example conversation flow: the user asks how many organic apples are in stock; the agent makes a tool call to get product information for organic apple and replies with the available quantity; the user asks the cost of five apples; the agent makes a tool call to calculate the total price passing quantity and price as parameters; the user asks for return policy rules; the agent makes a tool call to get the store return policy and returns it.
- Three upgrades are required to make the agent production ready: create a dedicated conversation session object, drop older messages when history gets too long, and store conversation history.
- The agent receives the user's message and generates an answer using either the LLM directly or registered tools; the model and tools always communicate through the agent's central execution loop; once tool execution completes, the agent returns the final response.
- The system prompt is always available and never lost during trimming.
- Session state initialization fields: `session_id` tracks specific user sessions for multi-user or isolated workflows; `system_prompt` retains core instructions separately so they are never lost during pruning; `messages` holds active multi-turn interactions (user inputs, model replies, tool call execution requests, tool returns); `max_history_turns` sets the strict maximum length for retained turns to manage token budgets.
- Ingesting messages: every interaction is dynamically appended to the session context, converted into standard chat payload dictionaries with keys like `role`, `content`, `name`, or `tool_calls`, and triggers an immediate trim-history check to evaluate context bounds in real time.
- Context window trimming: no action is taken if total history is within `max_history_turns`; otherwise the list is sliced to retain only the latest messages; a while loop removes any leading tool responses created after trimming to prevent breaking model inference with orphan tool calls.
- Constructing context: right before the API call to local Ollama/Gemma models, the pinned `system_prompt` is prepended to the trimmed messages array so system rules are always evaluated first without occupying space in the trim list.
- Session persistence: the entire conversation session object is saved to a formatted session file on disk; on load, the code checks for an existing session file, reads the payload, and instantiates a fully hydrated conversation session object; `max_history_turns` is passed as a parameter when a session is opened and is also stored in the session file, defaulting to a value in the code if not provided.
- The conversation session class was covered in detail; other modules are covered in previous lessons; full code and installation instructions are available via the GitHub link in the video description.

## Technical Details
- Invoked tools: product information lookup for organic apple; total price calculation (quantity and price parameters); store return policy retrieval.
- Session fields: `session_id`, `system_prompt`, `messages`, `max_history_turns`.
- Chat payload keys: `role`, `content`, `name`, `tool_calls`.
- Trimming behavior: compare total history against `max_history_turns`; slice to retain latest messages; remove leading orphan tool responses via a while loop.
- Context assembly: prepend pinned `system_prompt` to the trimmed `messages` array before the Ollama/Gemma API call.
- Persistence target path pattern:
```
/sessions/.json
```
- `max_history_turns` is passed at session open, stored in the session file, and falls back to a default value in the code if omitted.
- Backend: local Ollama / Gemma models.
- Series context: "Learning AI" lessons using 100% open-source tools runnable locally.

## Questions
- What is the exact default value of `max_history_turns` used when none is provided at session open?
- What is the precise session file naming scheme (the path is shown only as `/sessions/.json`)?
- Which specific Gemma model variant and Ollama version are used?
- How are `session_id` values generated or assigned for multi-user/isolated workflows?
- What are the request/response schemas of the three tools (product info, price calculation, return policy)?
- Where exactly is the GitHub repository link and its installation instructions (referenced only as being in the video description)?
- Does "turn" in `max_history_turns` mean a full user/assistant exchange or an individual message, and how are tool call/result pairs kept consistent during trimming?
<!-- yt-brain:related -->

## Related

- [[youtube/YouTube Knowledge Base|◻️ YouTube Knowledge Base]]
- [[youtube/llm-core|📁 LLMs & Model Behaviour]]
- [[index|🏛️ JARVIS Memory Vault]]

### Related notes

- [[youtube/agents/2026-11-13-building-a-reflective-agentic-rag-system-lesson-17-ai-agenti|Building a Reflective Agentic RAG System (Lesson: 17) #AI #AgenticRAG #Ollama #Gemma #FastMCP]] · relevance 0.15
- [[youtube/llm-core/2026-11-13-how-to-build-ai-agents-that-never-crash-lesson-5-ollama-gemm|How to Build AI Agents That Never Crash (Lesson: 5) #Ollama #Gemma4 #ai #artificialintelligence]] · relevance 0.12
- [[youtube/dev-craft/2026-11-13-build-your-first-local-ai-agent-python-tutorial-lesson-01-ai|Build Your First Local AI Agent (Python Tutorial) (Lesson: 01) #AIAgent #Gemma4 #Ollama #ai]] · relevance 0.11
- [[youtube/agents/2026-11-13-fastmcp-python-building-local-agent-tools-step-by-step-lesso|FastMCP & Python: Building Local Agent Tools Step-by-Step (Lesson:9) #ai #mcp #ollama #gemini]] · relevance 0.11

<!-- /yt-brain:related -->
