---
video_id: NnT9vzaB9Rw
title: "The Secret to Advanced AI: Multi-Step Reasoning Explained (Lesson: 2) #Gemma4 #ollama #ai #ajagent"
url: https://www.youtube.com/watch?v=NnT9vzaB9Rw
watched: 2026-10-30 21:56
source: chrome:Default
topic: agents
indexed: 2026-11-13T02:49:41+00:00
---

## Core Concept
The video explains multi-step reasoning in an AI agent: instead of executing one pass of tool calls, the agent runs an execution loop (a while loop with a max-iterations safety cap) that lets it inspect each tool result and decide whether to make follow-up tool calls before synthesizing a final answer.

## Key Takeaways
- With the prompt about three boxes of cereal and two gallons of whole milk, the agent cycled through four tool calls across multiple iterations to gather stock data and compute prices.
- The previous single-step agent executed only a single pass of tool calls and could not inspect initial results or run follow-ups to answer multi-part queries.
- The Python agent swapped an `if` statement for a `while` loop, enabling sequential tool calls.
- A max-iterations safety cap prevents the loop from running indefinitely; it exits when reasoning finishes or the limit is hit.
- If an item is out of stock, the agent skips the price calculation step for that product.
- For the Thanksgiving prompt, the agent calls `check_store_policy` to verify holiday hours and `check_product_info` to check sourdough bread inventory, then combines results.
- Inventory is currently stored as a local Python dictionary with item name, price, stock count, unit of measurement, and aisle location.
- Store hours, holiday schedules, and return policies currently live in a simple Python dictionary.
- Upcoming lessons will connect to a real database with SQL/ORM queries and use a vector database with RAG for policy documents.
- The agent relies on three core tools: `check_product_info`, `check_store_policy`, and `calculate_item_total`.
- Each tool is a standard Python function, so capabilities can be scaled by adding custom functions to the tool registry.
- `Ollama.chat` calls Ollama's chat API endpoint, which accepts structured conversation histories and tool definitions.
- Gemma 4 is the local LLM running on Ollama and supports function calling/tool execution natively, parsing Python schemas and outputting structured JSON instructions.
- `messages` passes the full context history: system rules, previous user prompts, past assistant responses, and prior tool results.
- Both Gemma 4 and Ollama are open source and free to run locally; the model parameter can be updated to use a different LLM.
- The prompt "What are your return policy rules and what aisle can I find organic apples in?" uses different tools to produce its response.

## Technical Details
- Architecture contrast: single-step agent = one pass of tool calls; multi-step agent = looped execution with result inspection and conditional follow-ups.
- Control flow change: `if` statement replaced by `while` loop.
- Safety mechanism: max iterations cap on the loop.
- Conditional optimization: skip price calculation when an item is out of stock.
- Data storage: local Python dictionaries for inventory and policies; fields include item name, price, stock count, unit of measurement, and aisle location.
- Tool registry: standard Python functions (`check_product_info`, `check_store_policy`, `calculate_item_total`).
- Model/runtime: Gemma 4 via Ollama; Ollama exposes a chat API endpoint accepting structured conversation history and tool definitions.
- Context passing: `messages` carries full conversation history including system rules and prior tool results.
- Extensibility: model parameter is swappable for another LLM.

```text
check_product_info
check_store_policy
calculate_item_total
```

## Questions
- What exact value is used for the max iterations safety cap?
- What are the specific setup and installation steps (including any commands) for Ollama and Gemma 4?
- How is the loop's exit condition determined beyond finishing reasoning or hitting the cap?
- What schema/format do the Python dictionary entries use for inventory and policies?
- How will the transition from dictionaries to a database and RAG be implemented in future lessons?
