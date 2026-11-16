---
video_id: IO5lICe3tqg
title: "How to Guarantee Structured AI Outputs with Pydantic (Lesson: 3) #ollama #aiagents #gemini #ai"
url: https://www.youtube.com/watch?v=IO5lICe3tqg
watched: 2026-10-30 22:00
source: chrome:Default
topic: agents
indexed: 2026-11-13T02:49:14+00:00
---

## Core Concept
This lesson demonstrates building a local AI agent whose tools are defined as Python classes with Pydantic validation and collected by a dynamic tool registry, rather than as simple Python functions; it shows that Pydantic provides schema-based validation of tool arguments, but business constraints such as quantity limits must be added explicitly, and the agent can be forced to call tools instead of computing answers itself.

## Key Takeaways
- Example query: “I want to buy three boxes of cereal and two gallons of whole milk. Are both in stock and what will the total price be?”
- Previous lesson used simple Python functions as tools; this lesson uses Python classes with Pydantic validation.
- A dynamic tool registry automatically collects all defined tools instead of manually adding every tool to a Python list.
- Python decorators wrap a function to add behavior without changing the original source code; `@` syntax is shorthand for reassignment.
- The registry automates three operations: schema extraction, tool lookup, and runtime argument validation.
- The registry stores registered tools in a private dictionary keyed by function name.
- The register decorator takes a Pydantic base model class (transcript: “ars schema”) and wraps a Python function; it uses `inspect` to read the function’s docstring and the model schema to generate an LLM-compatible JSON schema definition, storing both the function and metadata.
- `get_definitions` extracts all stored JSON schema definitions into a single list formatted for the LLM’s `tools` parameter during model calls.
- `execute` receives a tool name and raw argument dictionary from the LLM, validates the payload against the tool’s Pydantic schema, runs the function if valid, or returns formatted validation error messages back to the agent if validation fails.
- When a tool is defined as a Python class, a Pydantic decorator is used to register it.
- Extreme overflow test: “Calculate the price for 1 trillion boxes of cereal.” The function-based agent still calculates and returns the answer; the class-based agent initially also gives the same answer without validation.
- Pydantic does not automatically perform all validation; additional constraints and validation must be added in the tool.
- After adding constraints (quantity zero and less than 1,000) and forcing tool use, invalid quantity input produces a clear warning instead of a trillions-of-dollars total.
- Zero-quantity test: “I want to buy zero boxes of cereal and zero gallons of whole milk. Are both in stock? And what will the total price be?” The function tool returns a total price of zero; the constrained class tool returns a clear warning instead of $0.
- Validation is possible in functions, but the transcript states it is much easier in classes.

## Technical Details
- Terms and concepts: Pydantic, base model, dynamic tool registry, decorator, wrapper, `inspect`, JSON schema, LLM `tools` parameter, runtime argument validation, validation errors.
- Architecture comparison: direct function approach versus dynamic Pydantic approach.
- Registry responsibilities: schema extraction, tool lookup, runtime argument validation.
- Added constraint wording from transcript: quantity zero and less than 1,000.
- Additional behavior: forced the agent to use the tool to avoid the LLM doing the calculation without calling the tool.
- No code snippets, commands, or file paths were provided in the transcript.

## Questions
- What are the exact Pydantic model fields and constraint definitions, including whether bounds are inclusive?
- Which LLM/model and surrounding framework are used for the agent?
- How is the agent forced to use the tool (for example, a tool-choice setting)?
- What are the exact validation error message formats and registry method signatures?
- How does the registry handle duplicate tool names, missing tools, or lookup failures?
- Which files or paths contain the implementation?
- Does the quantity constraint apply equally to boxes of cereal and gallons of milk?
