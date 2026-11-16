---
video_id: f4fKkRnjzhU
title: "I Gave ChatGPT, Claude and Codex One Shared Brain"
url: https://www.youtube.com/watch?v=f4fKkRnjzhU&t=237s
watched: 2026-10-20 19:55
source: chrome:Default
topic: llm-core
indexed: 2026-11-13T03:04:01+00:00
type: youtube-note
source_url: https://www.youtube.com/watch?v=f4fKkRnjzhU&t=237s
tags: [youtube, youtube/llm-core]
---


## Core Concept

Every AI assistant operates in its own isolated bubble with its own chat history and memory, so context learned in one never reaches the others; the fix is to give ChatGPT, Claude, and Codex a single shared memory they search before answering and update after acting, implemented as one MCP-backed knowledge-graph file on your computer.

## Key Takeaways

- The problem: each agent keeps its own chat history, memory, and version of you, so a decision made in ChatGPT on Monday never reaches Claude on Tuesday and a fix Codex shipped overnight stays unknown to the rest.
- The fix is not a longer prompt or a giant pasted document; it is one shared memory that agents search before answering and update after acting.
- Architecture: sources (voice notes, sales calls, GitHub documents) sit at the top and can be fed to any agent; all three agents connect to one memory server, which stores everything in a single file on your computer.
- The glue is MCP (Model Context Protocol), an open standard that lets AI apps plug into tools; ChatGPT, Claude, and Codex all support it.
- In the visualization, colors map to sources (Telegram voice notes purple, GitHub blue, sales calls pink) and each agent has its own cluster; each dot is a single memory (decision, note, commit, or call) and each line is a connection between two memories.
- Pulling one memory can surface the whole story: the example bug search returned five memories from four sources (voice note, GitHub issue, Claude's plan, Codex's review, and the fixing commit).
- Setup takes about 30 minutes and requires Node.js installed.
- Step 1: create the memory using the official memory server from the MCP project; it stores a small knowledge graph in one file. Make a folder called `brain` and run it once to test.
- Critical rule: every agent must point at the same file using a full path; different paths mean two brains instead of one.
- Step 2: connect Claude — in Claude Desktop, open developer settings and add the memory server to the config with the full file path; in Claude Code it is a single command.
- Step 3: connect Codex with one command using the same file path; start a new session and confirm the memory tools appear.
- Step 4: ChatGPT is the tricky one because it cannot start programs on your computer and needs a public HTTPS address; either bridge the local file with a small gateway plus a tunnel, or use a hosted memory service and point all three agents at it. A tunnel has no login, so treat its address like a password.
- Step 5 (commonly skipped): connecting memory is not enough; every agent needs the same habit of searching memory before answering and saving decisions after, enforced by pasting a short rule into each agent's instructions.
- Test: in ChatGPT say the phrase below, then ask Claude when the beta launches (it should answer Friday), then ask Codex to add the launch date from memory to the README.
- Privacy warning: everything an agent reads is sent to that company, so never store passwords, API keys, or private information about other people.
- Backup warning: the whole brain is one file, so a copy is a backup.
- A full written guide with every command is linked in the description; a follow-up video will connect the author's real agents and run this live for a week.

## Technical Details

- MCP (Model Context Protocol): open standard enabling AI apps to plug into tools; supported by ChatGPT, Claude, and Codex.
- Memory server: the official memory server from the MCP project, storing a small knowledge graph in a single file.
- Shared-file requirement: all agents must reference the same file via a full path.
- ChatGPT access path: requires a public HTTPS endpoint, achieved via a local gateway plus tunnel or a hosted memory service.
- Agent habit rule: search memory before answering; save decisions after acting.
- Test utterance:
```
Remember the beta launches on Friday.
```
- Folder name referenced:
```
brain
```
- Content categories visualized: Telegram voice notes (purple), GitHub (blue), sales calls (pink); memories include decisions, notes, commits, and calls.

## Questions

- What exact command creates/starts the memory server and the `brain` folder contents? The transcript only references the linked written guide.
- What is the exact Claude Desktop config JSON and the single Claude Code / Codex commands? Not provided in the transcript.
- Which hosted memory service or tunnel/gateway tool is recommended? Not named in the transcript.
- What is the exact text of the "short rule" pasted into each agent's instructions? Not shown in the transcript.
- Which Node.js version is required, and how should the single brain file be named/backed up? Not specified.
- Is the 3D map visualization available to viewers, or only the author's own tool? Not stated.
- When will the follow-up video running real agents for a week be published? Not given.
<!-- yt-brain:related -->

## Related

- [[youtube/YouTube Knowledge Base|◻️ YouTube Knowledge Base]]
- [[youtube/llm-core|📁 LLMs & Model Behaviour]]
- [[index|🏛️ JARVIS Memory Vault]]

### Related notes

- [[youtube/agents/2026-09-29-claude-code-multi-agent-orchestration-with-opus-4-6-tmux-and|Claude Code Multi-Agent Orchestration with Opus 4.6, Tmux and Agent Sandboxes]] · relevance 0.10
- [[youtube/agents/2026-11-13-forget-prompting-this-is-how-a-10b-company-uses-ai-agents-wi|Forget Prompting. This Is How a $10B Company Uses AI Agents with Second Brain]] · relevance 0.09
- [[youtube/agents/2026-11-13-an-ai-agent-with-its-own-cursor-on-omarchy-cua-edge-channel|An AI Agent with Its Own Cursor on Omarchy (Cua, Edge Channel)]] · relevance 0.09
- [[youtube/linux-infra/2026-10-04-i-trusted-omarchy-s-ai-with-my-linux-desktop|I Trusted Omarchy’s AI With My Linux Desktop]] · relevance 0.08

<!-- /yt-brain:related -->
