---
video_id: b4ZTfs0KwR0
title: "OpenAI Dots Alternative: Free, Open Source & Any Model"
url: https://www.youtube.com/watch?v=b4ZTfs0KwR0
watched: 2026-09-30 19:08
source: chrome:Default
indexed: 2026-09-30T16:34:43+00:00
topic: dev-craft
type: youtube-note
source_url: https://www.youtube.com/watch?v=b4ZTfs0KwR0
tags: [youtube, youtube/dev-craft]
---



## Core Concept
OpenDots is presented as a free, open-source, self-hosted alternative to OpenAI's newly launched "dots" service: an always-on AI assistant app that runs on your own computer, works with any model from any provider (including models you run yourself), keeps your data and encrypted keys local, and gates every action behind a single human-approval checkpoint with logged, readable rules.

## Key Takeaways
- OpenAI "dots" is described as AI assistants that run around the clock on OpenAI's servers while you do something else — but it requires a paid plan and is locked to OpenAI's models.
- OpenDots runs on your own computer; you chat with it, give it tools, and it can use a browser for you.
- It is independently built and explicitly **not affiliated with OpenAI**. Over 4,000 developers have starred it on GitHub.
- Model flexibility is the headline difference: dots = one company's models; OpenDots = "any model" — type a model name from any provider or one you run yourself, including uncensored open models (the video says to "use those responsibly").
- Each assistant can use a *different* model — a cheap one for chores, a powerful one for hard problems.
- No extra subscription required: paste in an API key and pay only for what you use. If you already pay for ChatGPT or Claude, you can log in with that plan and use it here instead.
- Data locality: chats are saved on your computer and your keys are encrypted. Run a model on your own machine and nothing leaves it; with a hosted model only your messages go to that provider.
- Safety model: everything an assistant wants to do goes through one checkpoint. Nothing is allowed by default, and anything risky stops and asks you first — e.g., "delete a folder" pops up an approval card. Every decision is logged, and the rules are open code you can read and change.
- App integration: sign in once, then issue instructions from chat, such as "checking or creating issues on GitHub."
- Each assistant can get its own sealed-off browser (optional feature) — the video warns not to send it to sketchy websites.
- Setup is described as "a few commands": download the code, start the server, start the app, add your model. All settings are documented in the readme.
- Honest limitation stated by the video: still a prototype, built for one person for now, and dots can do more out of the box today.
- Free for everyone; pull requests are welcome. Repo is called "open dots" / OpenDots.

## Technical Details

**Architecture as described**
- Self-hosted, local-first app: the assistant process, chat history, and encrypted credentials live on the user's machine.
- Provider-agnostic model layer — model selection is per assistant, not global.
- Optional sandboxed browser instance per assistant ("sealed off browser"), so browsing state is isolated from the host environment and from other assistants.
- Permission gate between the model and any side-effecting action: deny-by-default, single approval checkpoint, approval card UI for risky operations.
- Audit log of every decision; permission rules are user-readable, user-editable source code.

**Credential / cost model**
- Two paths: bring-your-own API key (pay-per-token, no subscription) *or* log in with an existing ChatGPT/Claude plan.
- Keys stored encrypted at rest locally.

**Setup flow (as narrated, no literal commands given)**
```
1. Download the code
2. Start the server
3. Start the app
4. Add your model
```
All configuration is documented in the readme.

**Trade-offs stated or implied**
- Privacy vs. capability: a locally-run model gives total data locality; a hosted model leaks only messages to that one provider.
- Isolation vs. convenience: the per-assistant sandboxed browser is opt-in, trading safety for web capability.
- Ownership vs. maturity: free, private, any-model — but prototype, single-user, fewer built-in capabilities than dots today.

**Named entities / terms**
- OpenAI `dots` (paid, hosted, OpenAI-models-only)
- `OpenDots` / "open dots" (open source, 4,000+ GitHub stars, unaffiliated with OpenAI)
- Approval card, deny-by-default checkpoint, decision log
- GitHub issues (as the worked example of app integration)

## Questions
- What is the actual repository URL? The transcript only says "start open dots on GitHub" and "the link's below" — no org/repo is named.
- What are the literal setup commands, the server/app entrypoints, and the config file format? The steps are described narratively only.
- Which model providers and self-hosted runtimes (e.g., local LLM servers) are supported, and what is the exact model-name string format to type in?
- Does "log in with that plan" work via OAuth with a ChatGPT/Claude subscription, or must it be a separate API key from that account?
- What encryption is used for stored keys, and what is the threat model (at-rest only, or also keychain-backed / passphrase-derived)?
- Where are chats and the decision log stored on disk, and is there an export/retention policy?
- What is the "one checkpoint" enforced at — OS-level sandboxing, containerization, or in-process tool gating? Can the rules themselves be bypassed by a malicious model or plugin?
- Which tools are built in beyond the browser and GitHub integration? Are custom tools/MCP-style servers supported?
- Is the sandboxed browser containerized (gVisor/Firecracker/container), and is network egress restricted per assistant?
- What are the concurrency and multi-user limits, and is there a roadmap for multi-user or team hosting?
- Rough resource requirements (RAM/VRAM/GPU) for running the app plus a local model?
- Which license is it released under, given pull requests are invited?
<!-- yt-brain:related -->

## Related

- [[youtube/YouTube Knowledge Base|◻️ YouTube Knowledge Base]]
- [[youtube/dev-craft|📁 Software Engineering Craft]]
- [[index|🏛️ JARVIS Memory Vault]]

### Related notes

- [[youtube/dev-craft/2026-11-13-i-built-a-python-sdk-for-ai|I built a Python SDK for AI]] · relevance 0.11
- [[youtube/linux-infra/2026-10-07-i-built-jarvis-in-omarchy|I BUILT JARVIS IN OMARCHY]] · relevance 0.10
- [[youtube/dev-craft/2026-09-29-openmanus-vs-manus-who-wins|OpenManus VS Manus: Who Wins?]] · relevance 0.09
- [[youtube/linux-infra/2026-11-13-i-build-offline-voice-assistant-for-hyprland-arch-linux|I Build Offline Voice Assistant For Hyprland + Arch Linux]] · relevance 0.09

<!-- /yt-brain:related -->
