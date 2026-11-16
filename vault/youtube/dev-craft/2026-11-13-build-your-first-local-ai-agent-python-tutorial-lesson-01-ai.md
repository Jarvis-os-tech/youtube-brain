---
video_id: pvbsVZlDjlU
title: "Build Your First Local AI Agent (Python Tutorial) (Lesson: 01) #AIAgent #Gemma4 #Ollama #ai"
url: https://www.youtube.com/watch?v=pvbsVZlDjlU
watched: 2026-10-30 21:52
source: chrome:Default
topic: dev-craft
indexed: 2026-11-13T02:51:03+00:00
type: youtube-note
source_url: https://www.youtube.com/watch?v=pvbsVZlDjlU
tags: [youtube, youtube/dev-craft]
---


## Core Concept
This lesson demonstrates building and running a first local AI agent in Python: an LLM-centered system that plans, reasons, and executes multi-step tasks, with behavior shaped by system and user prompts and optionally extended through external tools such as a budget calculation tool.

## Key Takeaways
- The agent was run to calculate total expense using the "calculate budget tool" and returned `$550.75`.
- The system prompt defines the agent's identity, rules, allowed tools, and output formatting before user input is read.
- The system and user prompts were changed to use the agent as an analytical agent requesting YouTube video title ideas plus a cost calculation.
- The agent used the LLM for YouTube title suggestions and the Python function tool for the calculation.
- The user prompt is the runtime instruction, payload, or question that triggers the agent.
- An AI agent plans, reasons, and executes multi-step tasks independently using an LLM as its central reasoning engine.
- Agents interact with external tools and use both short-term context and long-term vector memory.
- Agents operate continuously, unlike passive standard LLMs.
- The prompts were changed to use the agent as a content strategy agent using only the LLM and no tools, requesting three YouTube video opening hook scripts under 30 words each.
- The agent generated three suggestions under 30 words each.
- The prompts were changed again to request Python coding suggestions, specifically reviewing a Python function signature and explaining how to handle missing arguments.
- The agent delivered three structured suggestions with sample code, pros and cons, and core concepts.
- The agent loop is: user provides an objective; the core LLM analyzes it; the agent creates a sequence of actions; actions execute and retrieve information from external environments, tools, or databases; results, data, or errors are returned; feedback and action history are stored in short-term memory; the loop repeats until the goal is met; then the final response is delivered.
- Agents differ from chatbots in four ways: they run loops until the goal is met; they act by running scripts, querying APIs, scraping data, and updating local files; they manage multi-step projects; and they catch execution errors, rewrite syntax, and rerun code.
- Required components mentioned: Ollama engine for pulling and running open-source models locally; model Gemma 4, hosted via Ollama; Python 3.13 for script compatibility.
- The project was developed and tested on macOS on a Mac mini but is described as compatible with Windows and Linux.
- Terminal logs can be exported into a markdown file on GitHub for cleaner formatting and rendering.
- If not using the Gemma 4 model, the model name must be changed in the script.
- The system prompt and user prompt can be changed in the script and the script rerun multiple times.
- Starter scripts and setup guides are available in the video description.
- The video asks viewers to like, comment, and subscribe.

## Technical Details
- Terms: system prompt, user prompt, AI agent, large language model (LLM), external tools, short-term context/memory, long-term vector memory, analytical agent, content strategy agent, agent loop, recursive process.
- Architecture described: the user initiates the process with a specific objective; the core LLM analyzes the goal; the agent creates a sequence of actions; it executes those actions and retrieves information from external environments, tools, and databases; it receives results, data, or errors; that feedback plus action history is stored in short-term memory to inform the next loop iteration; once the goal is met, the final completed task or response is delivered.
- Prompt behavior: the system prompt is set before user input and defines identity, thinking style, allowed tools, and output format; the user prompt supplies the runtime task and inputs.
- Tool usage mentioned: "calculate budget tool" for the expense calculation and a Python function tool; LLM-only operation for YouTube hook scripts and Python coding suggestions.
- LLM-only mode was used for the content strategy agent to generate three opening hook scripts under 30 words each.
- Agent feedback handling includes receiving results, data, or errors from executed actions.
- Configuration and environment: Ollama engine is required for pulling and running open-source language models locally; the model is Gemma 4, described as Google's open-source Gemma 4 model hosted via Ollama; Python 3.13 is specified for compatibility with the repository scripts; the project is cross-platform, developed and tested on macOS Mac mini, with stated compatibility for Windows and Linux.
- Script usage notes: change the model name in the script if not using Gemma 4; change the system prompt and user prompt in the script and rerun as needed.
- Output handling note: terminal logs can be exported into a markdown file on GitHub for clean formatting and rendering.

## Questions
- What inputs or parameters did the "calculate budget tool" use to produce `$550.75`?
- What was the exact Python function signature reviewed, and which arguments were missing?
- What were the three YouTube opening hook scripts and the three structured Python suggestions?
- What exact model name string should be used when changing the model in the script?
- Which files, paths, or commands are included in the starter scripts and setup guides?
- How is long-term vector memory implemented or configured in this agent?
- Is exporting terminal logs to a markdown file on GitHub a built-in script feature or a manual step?
- Are specific Ollama, Gemma 4, or Python dependency versions required beyond Python 3.13?
<!-- yt-brain:related -->

## Related

- [[youtube/YouTube Knowledge Base|◻️ YouTube Knowledge Base]]
- [[youtube/dev-craft|📁 Software Engineering Craft]]
- [[index|🏛️ JARVIS Memory Vault]]

### Related notes

- [[youtube/agents/2026-11-13-how-to-guarantee-structured-ai-outputs-with-pydantic-lesson|How to Guarantee Structured AI Outputs with Pydantic (Lesson: 3) #ollama #aiagents #gemini #ai]] · relevance 0.19
- [[youtube/agents/2026-11-13-fastmcp-python-building-local-agent-tools-step-by-step-lesso|FastMCP & Python: Building Local Agent Tools Step-by-Step (Lesson:9) #ai #mcp #ollama #gemini]] · relevance 0.18
- [[youtube/agents/2026-11-13-the-secret-to-advanced-ai-multi-step-reasoning-explained-les|The Secret to Advanced AI: Multi-Step Reasoning Explained (Lesson: 2) #Gemma4 #ollama #ai #ajagent]] · relevance 0.15
- [[youtube/agents/2026-11-13-building-a-reflective-agentic-rag-system-lesson-17-ai-agenti|Building a Reflective Agentic RAG System (Lesson: 17) #AI #AgenticRAG #Ollama #Gemma #FastMCP]] · relevance 0.12

<!-- /yt-brain:related -->
