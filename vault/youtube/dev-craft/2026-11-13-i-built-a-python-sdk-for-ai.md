---
video_id: D-4nHVL6Xw8
title: "I built a Python SDK for AI"
url: https://www.youtube.com/watch?v=D-4nHVL6Xw8
watched: 2026-11-02 20:45
source: chrome:Default
topic: dev-craft
indexed: 2026-11-13T02:45:26+00:00
type: youtube-note
source_url: https://www.youtube.com/watch?v=D-4nHVL6Xw8
tags: [youtube, youtube/dev-craft]
---


## Core Concept
Fury is a small, single-file, open-source Python package for building LLM agents against any OpenAI-compatible API, consolidating recurring agent plumbing—chat loops, history, tool calling, parallel tool execution, multimodal inputs, voice transcription, and streaming—into one transparent codebase.

## Key Takeaways
- The package is positioned as a minimal alternative to bloated LLM/agent tooling; it is open source, one file, and about 500 lines long.
- Fury works with any OpenAI-compatible LLM API, with named examples: VLLM, SGLang, Ollama, Llama.cpp server, and OpenRouter.
- Installation is via UV or pip; there is no PyPI account yet, and the package is currently added directly from GitHub.
- Out-of-the-box capabilities include an easy API, tool registration, parallel tool execution, multimodal inputs, voice input handling, and streaming responses.
- Multimodal support includes adding base64 images to LLM history and transcribing voice bytes with Whisper before passing them to the LLM.
- An agent is created in roughly four lines: model name, system prompt, base URL, and API key.
- Agent startup checks that the configured server is actually serving the claimed model, then prints the model, available tools, and system prompt.
- A parallel tool-calling tool is injected by default; it can be disabled with `parallel_tool_calls` set to false.
- Tools are created with `create_tool`, using an ID, description, function, announcement phrase, and input/output schemas.
- Tool descriptions should be treated as mini-prompts with detailed usage guidance.
- The example tool `check_time` uses `datetime` and returns the current local time as an ISO string.
- Tool calls expose reasoning tokens and a tool call object; announcement phrases can be printed before a tool runs.
- The package currently lacks IntelliSense and more developer docs; PRs are welcomed, and there is a Discord community linked in the README.

## Technical Details
- Architecture: a single Python file, `source/fury/agent.py`, is described as the whole package implementation; future complexity may be split into multiple files.
- Compatibility: targets OpenAI-compatible endpoints, including local servers such as Llama.cpp server and hosted providers such as OpenRouter.
- Configuration flow: instantiate an agent with model name, system prompt, base URL, and API key; create a history object; then run a basic chat loop.
- Startup behavior: Fury verifies the configured model is online and reports the pointed-at model, available tools, and system prompt.
- Tooling:
  - `create_tool` accepts an ID, description, callable function, announcement phrase, and input/output schemas.
  - Input/output schemas follow the standard OpenAI schema; an input-less tool can leave input blank.
  - Announcement phrases are printed before the tool function runs, useful for UI transparency.
  - Tool descriptions should include when and how to use the tool, not just a one-line label.
- Parallel execution: LLMs can call multiple tools at once; Fury supports asynchronous parallel tool execution and injects a parallel tool-use tool by default.
- Multimodal and voice:
  - Base64 images can be added to LLM history.
  - Voice bytes can be transcribed with Whisper before being handed to the LLM.
- Streaming: streaming responses are standard and described as the expected interaction mode.
- Example workflow commands mentioned:
  - `uv init`
  - `uv add` from GitHub directly
  - `uv run main.py`
- Example local run: Quen 30B via Llama server, with no API key because it runs locally.
- Example tool: `check_time`, backed by a `datetime` function returning the current local time in ISO format.
- Transparency/debugging: tool call objects and reasoning tokens can be inspected; announcement phrases can be printed during tool calls.
- Project status: no PyPI release yet; seeking stability before official ship; documentation and IntelliSense still needed.

## Questions
- What is the exact GitHub URL and install command for adding Fury from GitHub?
- What Python versions are supported, and are there dependency/version constraints?
- What are the exact class/function signatures for `Fury`, `create_tool`, history objects, and streaming APIs?
- How does Fury handle errors, retries, timeouts, or malformed tool outputs?
- Does Whisper transcription run locally or through a service, and how is it configured?
- What does the injected parallel tool-calling tool look like, and what are its limits?
- Are there tests, benchmarks, or examples beyond the `check_time` tool?
- What license applies to Fury?
- How are multimodal image inputs structured in history beyond base64?
- What exact behavior occurs when the startup model check fails?
<!-- yt-brain:related -->

## Related

- [[youtube/YouTube Knowledge Base|◻️ YouTube Knowledge Base]]
- [[youtube/dev-craft|📁 Software Engineering Craft]]
- [[index|🏛️ JARVIS Memory Vault]]

### Related notes

- [[youtube/linux-infra/2026-11-13-i-build-offline-voice-assistant-for-hyprland-arch-linux|I Build Offline Voice Assistant For Hyprland + Arch Linux]] · relevance 0.13
- [[youtube/dev-craft/2026-09-30-openai-dots-alternative-free-open-source-any-model|OpenAI Dots Alternative: Free, Open Source & Any Model]] · relevance 0.11
- [[youtube/agents/2026-11-13-fastmcp-python-building-local-agent-tools-step-by-step-lesso|FastMCP & Python: Building Local Agent Tools Step-by-Step (Lesson:9) #ai #mcp #ollama #gemini]] · relevance 0.11
- [[youtube/dev-craft/2026-11-13-build-your-first-local-ai-agent-python-tutorial-lesson-01-ai|Build Your First Local AI Agent (Python Tutorial) (Lesson: 01) #AIAgent #Gemma4 #Ollama #ai]] · relevance 0.10

<!-- /yt-brain:related -->
