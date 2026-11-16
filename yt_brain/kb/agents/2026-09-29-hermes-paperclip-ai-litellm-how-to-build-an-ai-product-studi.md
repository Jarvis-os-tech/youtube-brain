---
video_id: Et5cxBu_D8Y
title: "Hermes + Paperclip AI + LiteLLM: How to Build an AI Product Studio"
url: https://www.youtube.com/watch?v=Et5cxBu_D8Y
watched: 2026-09-29 10:25
source: chrome:Default
indexed: 2026-09-29T16:31:59+00:00
topic: agents
---


## Core Concept

Building an "AI product studio" by combining three open-source layers: Paperclip as the management/governance layer that defines an organization of AI agents with roles, budgets, task queues, and approval gates; Hermes as the hands-on execution agent that actually reads files, calls tools, runs commands, and writes code; and LiteLLM as the model gateway that routes each role to the right model while centralizing API keys, rate limits, and cost tracking. The claim is that the win is not perfect unattended software delivery but a governed, observable workflow where AI does more execution while humans retain control of consequential decisions.

## Key Takeaways

- A single coding agent is not enough for a real product: a food delivery platform needs requirements, UX, architecture, code, tests, documentation, and review. One agent owning all of it produces messy context and no accountability.
- The mental model to adopt is a small company: roles, a task board, budgets, and human checkpoints where a person says yes, continue, or rethink.
- Paperclip = "an operating system for an AI company." You create an organization, set a goal, and give agents defined jobs and reporting lines.
- The example org for the food delivery app: a CEO agent called "boss," plus business analyst, product manager, UX designer, architect, developer, QA engineer, and technical writer.
- Paperclip supplies tasks, budgets, approval workflows, project workspaces, and a visible activity trail. It is explicitly *not* the model that writes code.
- Hermes is the hands-on worker: works in the terminal, interacts with files and repos, calls MCP servers, and completes multi-step tasks rather than returning a chat response.
- Example delegation: Paperclip assigns "create the architecture for restaurant onboarding"; Hermes reads requirements, inspects the repository, creates files, runs commands, and reports back.
- Hermes can convert useful experience into reusable skills so repeated workflows become more consistent.
- LiteLLM gives applications/agents one OpenAI-compatible interface and routes to many providers, replacing per-agent integrations with OpenAI, Anthropic, or local models.
- LiteLLM capabilities called out: routing work to different models, centralized API keys, spend tracking, authentication and rate limits, and swapping models behind a stable name.
- Alias-based routing example: a "cloud fast" name for planning, "cloud coder" for implementation, "cloud design" for UX — the agent asks for a capability, LiteLLM picks the route.
- The demo flow: goal to Paperclip → CEO agent turns it into strategy → PM (requirements), UX (user journeys), architect (approach), developers (build), QA (testing), writers (documentation). Hermes is the execution engine; LiteLLM underneath routes planner→fast model, developer→coding model, and tracks cost.
- Adoption advice: start small with a bounded job — a landing page, a product brief, scaffolding an API with tests, or investigating a bug and proposing a fix. Not "build the next Uber overnight."
- Set budgets, give each agent a narrow role, and keep human approval gates for product direction, security, production, deployment, and anything affecting real users or money.
- All three tools are described as open source.

## Technical Details

- **Three-layer separation of concerns**
  - Paperclip = manager (org structure, tasks, budgets, approvals, activity trail)
  - Hermes = worker (execution engine: files, commands, tests, tools, MCP)
  - LiteLLM = model + cost control layer (routing, keys, spend, auth, rate limits)
- **Paperclip responsibilities**
  - Organization creation, goal definition, agent job definitions, reporting lines
  - Work queue / task assignment, budgets per agent, approval workflows
  - Project workspaces and a visible activity trail
  - Knows: the goal, team structure, work queue, and which decision needs human approval
- **Paperclip's boundary:** the actual worker still needs to inspect files, use tools, write code, and run commands — that role belongs to Hermes.
- **Hermes capabilities**
  - Terminal-based work
  - File and repository interaction
  - MCP server calls
  - Multi-step task execution (not just chat responses)
  - Skill creation from experience for workflow consistency
- **LiteLLM capabilities**
  - One OpenAI-compatible interface for apps and agents
  - Routing to multiple model providers, including local models
  - Centralized API keys, spend tracking, authentication, rate limits
  - Model swapping behind a stable alias name
  - Capability-based alias pattern: planner → fast model, developer → coding model
- **Trade-offs / implications stated or implied**
  - Agent-per-everything: messy context, unclear accountability vs. specialization
  - Direct agent→provider wiring: "painful fast" vs. a single gateway
  - Full autonomy vs. "governed observable workflow" with human control of important decisions
  - Big-bang ambition vs. bounded first jobs with budgets and approval gates
- **No code, commands, CLI invocations, config files, or file paths appear in the transcript** — the tool is discussed conceptually only; no setup steps were shown.

## Questions

- How are Paperclip, Hermes, and LiteLLM actually installed and wired together? The transcript gives no commands, config, or API surface.
- What is Paperclip's canonical name/spelling? The transcript renders it variously as "paper clip AI," "paper," "Paperclip," and "paperclipip" — likely all the same product.
- "Hermes agent is an open-source tool using AI agent from nose research" — the vendor name is transcribed as "nose research"; this likely refers to Nous Research, but the transcript does not confirm it. Worth verifying.
- LiteLLM alias examples are transcribed as "cloud fast / cloud coder / cloud design" — the actual model names behind these aliases (and whether they are Anthropic models) are never stated.
- How budgets are expressed and enforced (per agent, per run, per month) and what happens when a budget is exceeded is never specified.
- How approval gates are configured, who approves, and whether approvals block or merely notify.
- How Paperclip decides which specialist agent receives a task — no routing or delegation algorithm is described.
- No pricing, self-hosting requirements, or deployment topology (local vs. hosted) is given.
- The transcript is auto-generated and contains no Q&A, benchmarks, demos, or verification steps, so all performance and outcome claims are unvalidated.
