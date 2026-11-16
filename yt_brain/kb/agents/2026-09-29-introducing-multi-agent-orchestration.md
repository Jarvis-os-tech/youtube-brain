---
video_id: RWT3sh68PWE
title: "Introducing multi-agent orchestration"
url: https://www.youtube.com/watch?v=RWT3sh68PWE
watched: 2026-09-29 11:26
source: chrome:Default
indexed: 2026-09-29T11:05:18+00:00
topic: agents
---


## Core Concept
Oz gained a set of features for governing agentic development at scale: multi-harness support, automatic subagent orchestration, cross-harness agent memory, and improved agent handoff between local, cloud, Slack, and phone — all managed from a single control plane that sits above individual harnesses and can run on your own infrastructure with your own data.

## Key Takeaways
- The stated demand: engineering leaders want to deploy cloud agents at scale, but in a controlled and governed way.
- Three named requirements leaders ask for: choice between multiple agent harnesses, the ability to track/steer/audit regardless of harness, and the ability to run agents on your own infrastructure and own the resulting data.
- Multi-harness: Oz can now start and track cloud agents from Claude Code, Codex, and Warp Agent from one unified control plane.
- Oz "sits a level above all these harnesses," so you can see which harness is most effective for a given task and get a single interface for access control and governance — "a single pane of glass for all your cloud agents."
- Oz can orchestrate subagents automatically, deploying multiple agents for complex tasks.
- Cross-repo, long-horizon tasks are supported (examples given: complex feature buildouts and legacy code migrations), and this works across every harness.
- Warp's agent memory automatically extracts relevant info from sessions and resurfaces it into context at the right time; it targets repetitive/complex tasks and tasks spanning multiple context windows across sessions. It also works across harnesses. Status: research preview.
- Improved agent handoff, including local → cloud, with conversation sessions and artifacts staying in context.
- Usage example: start 10 sessions in your terminal, set them running overnight, pick them up on your laptop the next morning.
- Cross-surface handoff: start an agent in Slack, pick it up on a phone, move it back to your terminal.
- Also announced but not detailed: better self-hosting options, richer access controls, and improved remote coding.

## Technical Details
- **Oz** — the control plane; sits above the harnesses rather than replacing them.
- **Harnesses supported:** Claude Code, Codex, Warp Agent.
- **Multi-harness** — start and track cloud agents from multiple harnesses through one unified control plane.
- **Access control and governance** — provided once at the Oz layer, so it is harness-independent.
- **Harness selection** — visibility into "which one is most effective" for any given task.
- **Subagent orchestration** — automatic, for deploying multiple agents on complex tasks.
- **Cross-repo long-horizon tasks** — feature buildouts, legacy code migrations; supported across every harness.
- **Agent memory** — session-derived extraction, resurfaced into context at the right time; cross-session and cross-harness; research preview.
- **Handoff** — local ↔ cloud; conversation sessions and artifacts preserved in context; terminal → laptop, Slack → phone → terminal.
- **Self-hosting** — run agents on your own infrastructure and own the data agents produce.
- **No code, commands, flags, or file paths appear in the transcript**, so none are reproduced here.

## Questions
- Which harnesses beyond Claude Code, Codex, and Warp Agent are supported or planned?
- What is the mechanism for orchestration — how are subagents spawned, coordinated, and are results merged automatically?
- How does Oz measure "which harness is most effective"? Is there a published success-rate or evaluation metric?
- What are the limits on agent memory: retention, storage location, and how it is surfaced or dismissed in context?
- What are the self-hosting requirements and the data-residency story — where is state stored and how is it deleted?
- What are the specifics of the "richer access controls" — roles, per-harness policies, or audit-log formats?
- What does "research preview" mean in practice for agent memory: opt-in flag, plan gating, or roadmap commitment?
- Is there any pricing, availability region, or GA-vs-preview timeline for these features?
