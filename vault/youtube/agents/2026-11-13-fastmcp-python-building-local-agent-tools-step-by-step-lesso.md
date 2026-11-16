---
video_id: cMU-_RdXvnQ
title: "FastMCP & Python: Building Local Agent Tools Step-by-Step (Lesson:9) #ai #mcp #ollama #gemini"
url: https://www.youtube.com/watch?v=cMU-_RdXvnQ
watched: 2026-10-30 22:10
source: chrome:Default
topic: agents
indexed: 2026-11-13T02:47:42+00:00
type: youtube-note
source_url: https://www.youtube.com/watch?v=cMU-_RdXvnQ
tags: [youtube, youtube/agents]
---


## Core Concept
This lesson converts the agent tools built in the previous lesson into standalone MCP servers, separating the central LLM core from actual tool execution so that, instead of reading files directly, the LLM sends JSON-RPC requests via MCP to distinct specialized servers for inventory, policy, and schedule data that handle data access locally.

## Key Takeaways
- The lesson opens with an example exchange: "Do you have organic Gala apples in stock? And how much are they?" answered with "Yes, we have organic Gala apples in stock. The price is $2.49."
- A supermarket database is created for the database MCP tool server to store all product inventory.
- `query_inventory` is registered as an executable MCP tool over the SQLite database; its docstring and parameter type hints are exposed as JSON-RPC metadata, and it returns a newline-separated string to the LLM.
- Holidays and working hours are also defined as an MCP tool.
- The MCP client registry class acts as the host client, registering available MCP tools into a lookup dictionary.
- A tool execution dispatcher handles JSON-RPC style tool execution: it logs the dispatch attempt, executes the registered tool function with keyword arguments, catches execution errors, and returns string-formatted tool outputs.
- MCP is an open standard that simplifies how LLMs connect to external data sources, tools, and local/remote software systems, creating a universal protocol for tool execution and contact retrieval.
- MCP architecture has three components: the MCP host/LLM application (main environment executing the AI agent), the MCP client (inside the host, discovering servers, formatting tool definitions for the LLM, dispatching JSON-RPC tool requests), and MCP servers (lightweight specialized scripts or applications exposing capabilities via three primitives: tools, resources, prompts).
- Initialization sets up the target local LLM model, Gemma 4, and instantiates the MCP client registry to route calls to decoupled MCP servers.
- The local model interface sends formatted system and user prompts to the local Ollama instance running Gemma 4 and handles communication errors.
- Intent classification assigns incoming queries to one of four intent tags: `product`, `return_policy`, `working_hours`, or `general`.
- The product agent extracts key search terms using the LLM, executes `query_inventory` against the SQLite database, and synthesizes an answer using real-time stock data.
- The policy agent calls `search_return_policy` to retrieve return rules and generates a customer service response based on the document extract.
- The schedule agent calls `get_start_hours` to retrieve operating hours and holiday schedules to answer timing questions.
- The main orchestrator runs the intent router agent first, then directs execution to the appropriate specialized domain agent.
- MCP rationale: tools run as isolated independent processes; domain servers can be updated or replaced independently; MCP servers can be reused across different LLMs; the core LLM only interacts with pre-approved schema endpoints; but setting up MCP has higher upfront architectural overhead.
- The lesson recaps prior building blocks: local AI agent setup with Ollama running fully autonomous open-source models locally; multi-step reasoning with plan/reflect/execute dynamic tool calls in a continuous loop; Pydantic data validation for strict type safety and schema validation across tool inputs and arguments; prompt memory maintaining conversational history across turns while trimming context dynamically; robust error handling intercepting execution failures, malformed parameters, and model retries gracefully; structured output guaranteeing validated, deterministic JSON and HTML output schemas from LLM responses.

## Technical Details
- LLM runtime: Gemma 4 served locally via Ollama.
- Storage: SQLite database for product inventory.
- Protocol: JSON-RPC requests dispatched by the MCP client to specialized MCP servers.
- MCP server primitives: tools, resources, prompts.
- MCP tool functions exposed (names as given):
  - `query_inventory`
  - `search_return_policy`
  - `get_start_hours`
- Intent tags: `product`, `return_policy`, `working_hours`, `general`.
- Architecture components in this lesson:
  - MCP host / LLM application
  - MCP client (registry + dispatcher)
  - MCP servers (inventory, policy, schedule)
- Tool result format returned to the LLM: newline-separated string.
- Metadata exposed from tool functions: docstring and parameter type hints.
- Prior-lesson building blocks referenced: Ollama local models, multi-step reasoning loop, Pydantic validation, prompt memory with dynamic context trimming, robust error handling, structured JSON/HTML output.

```text
MCP tools: query_inventory, search_return_policy, get_start_hours
Intent tags: product, return_policy, working_hours, general
LLM: Gemma 4 via Ollama
Database: SQLite (product inventory)
```

## Questions
- The transcript says MCP creates a universal protocol for tool execution and "contact retrieval" — is that "context retrieval," and what exactly does it entail?
- No file paths, module names, or full code listings are given for the MCP servers, registry, or dispatcher; a viewer would need to verify the actual implementation.
- It is unspecified how the MCP servers are launched or wired (stdio vs. HTTP/SSE) and how the JSON-RPC transport is configured.
- The exact SQLite schema and the `query_inventory` parameter signature are not shown.
- It is not stated whether the policy and schedule data live in files, databases, or hardcoded structures.
- The transcript does not clarify how errors from one MCP server propagate to the orchestrator or how retries are handled at the MCP layer.
- Whether Gemma 4 is the only supported model, and how model selection is configured, is not detailed.
<!-- yt-brain:related -->

## Related

- [[youtube/YouTube Knowledge Base|◻️ YouTube Knowledge Base]]
- [[youtube/agents|📁 AI Agents & Orchestration]]
- [[index|🏛️ JARVIS Memory Vault]]

### Related notes

- [[youtube/dev-craft/2026-11-13-build-your-first-local-ai-agent-python-tutorial-lesson-01-ai|Build Your First Local AI Agent (Python Tutorial) (Lesson: 01) #AIAgent #Gemma4 #Ollama #ai]] · relevance 0.18
- [[youtube/agents/2026-11-13-how-to-guarantee-structured-ai-outputs-with-pydantic-lesson|How to Guarantee Structured AI Outputs with Pydantic (Lesson: 3) #ollama #aiagents #gemini #ai]] · relevance 0.15
- [[youtube/linux-infra/2026-11-13-i-build-offline-voice-assistant-for-hyprland-arch-linux|I Build Offline Voice Assistant For Hyprland + Arch Linux]] · relevance 0.13
- [[youtube/agents/2026-11-13-the-secret-to-advanced-ai-multi-step-reasoning-explained-les|The Secret to Advanced AI: Multi-Step Reasoning Explained (Lesson: 2) #Gemma4 #ollama #ai #ajagent]] · relevance 0.13

<!-- /yt-brain:related -->
