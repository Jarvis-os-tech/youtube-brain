---
video_id: wEEbyindf5U
title: "How to Build AI Agents That Never Crash (Lesson: 5) #Ollama #Gemma4 #ai #artificialintelligence"
url: https://www.youtube.com/watch?v=wEEbyindf5U
watched: 2026-10-30 22:04
source: chrome:Default
topic: llm-core
indexed: 2026-11-13T02:48:31+00:00
---

## Core Concept
The video is about building a self-healing AI agent loop where, instead of crashing or exposing raw exceptions when a tool fails, the agent records a structured error response into session history and lets the LLM correct its parameters, retry, or produce a polite fallback answer.

## Key Takeaways
- The opening example asks the supermarket helpdesk agent to check dragon fruit stock; when an issue occurs, the agent catches it and sends a clear, polite response instead of a generic runtime error.
- The core function is `run persistent agent step`, accepting an active session object, a user input prompt, a model name defaulting to Gemma 4, and a max duration cap to prevent infinite loops.
- On each iteration, chat receives the updated session memory plus available tools; `session get full context` provides a system prompt plus managed message history without exceeding token limits.
- After the LLM returns a payload, the model's message is immediately recorded into session state.
- If tool calls are empty, the response is treated as a non-tool terminal response: the final answer is printed, the updated conversation session is saved to disk, and the loop exits.
- When tool calls are present, the agent loops through them, extracts function parameters, logs the action, and dispatches execution through the registry.
- If a tool output has an error status, the agent logs the execution error and routes a structured message back into the session, explicitly instructing the LLM to correct parameters and retry or formulate a polite response.
- If tool execution succeeds, the result is printed to the console and stored in session history under the tool role, then passed back to the model on the next turn.
- The saved JSON session file in `/sessions/` shows the full turn lifecycle: pinned system prompt, user query, assistant tool invocation attempt, structured tool error response, and Gemma 4's polite response after processing the error.
- A second example asks for the price of 5,000 units of organic apples at $2.99 each; the agent gives a polite message instead of a system error.
- The next lesson will force the agent's final synthesized response into a strict structured schema.

## Technical Details
- Terms and flow include: active session object, user input prompt, model name defaulting to Gemma 4, max duration cap, updated session memory, available tools, managed message history, token limits, tool calls, terminal response, registry execution, error status, structured message, tool role, loop re-entry.
- Iteration guard check: the system verifies whether the current loop iteration is strictly less than max iterations; if not, a warning is logged, the current session state is saved to disk, and the function exits.
- Ollama chat execution sends the entire formatted message context plus dynamic tool schemas to local Ollama.
- Exception branch: if an API or network error occurs, the error is logged, a fallback error message is appended for the assistant, session state is persisted, and execution stops.
- Success branch: the raw assistant message payload is extracted and appended directly into session history.
- Tool call evaluation has two paths: Path A is a final text response with no tool calls; Path B is tool invocation needed.
- Tool execution statuses are `success` and `error`; success output is formatted as JSON, wrapped in a `role = tool` message, and appended to session context.
- Self-healing error context includes explicit parameters and corrective instructions.
- After appending tool responses or self-healing error context, control returns to the iteration guard check.
- File path shown in the transcript:
```text
/sessions/
```

## Questions
- What is the exact numeric value of the max iteration cap?
- How does the tool registry determine whether an output has an error status?
- What are the exact dynamic tool schemas passed to Ollama?
- How many retries are allowed before the agent stops attempting correction?
- What is the exact filename or subfolder naming convention under `/sessions/`?
- What strict structured schema will be used for the final response in the next lesson?
