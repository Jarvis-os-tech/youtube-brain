---
video_id: Wzpz7rQawNo
title: "Pi vs PiG: Is This New Go Agent Faster?"
url: https://www.youtube.com/watch?v=Wzpz7rQawNo
watched: 2026-10-03 15:21
source: chrome:Default
indexed: 2026-10-03T12:18:31+00:00
topic: agents
type: youtube-note
source_url: https://www.youtube.com/watch?v=Wzpz7rQawNo
tags: [youtube, youtube/agents]
---



# Video Study Notes: Pi vs PiG — Is This New Go Agent Faster?

## Core Concept

PiG is a community-owned Go port of the minimal terminal coding agent Pi, designed to stay byte-for-byte behavior-compatible with upstream Pi (down to Pi's own extensions) while gaining three things Pi doesn't have: a ~19x faster startup, a single static binary with no Node dependency for its core, and the ability to hand a team a fully configured agent as one signed, compiled file via "piglets." The tradeoff is that PiG is a 0.x release pinned to a specific Pi version (0.87.1) while upstream Pi has already moved to 0.99, so the speed advantage largely evaporates if your setup depends on TypeScript extensions or on features landing upstream that week.

## Key Takeaways

- **PiG** = Pi rebuilt in Go, shipped as a **155 MB** binary; install took about **3 seconds**.
- First public release was **5 days** before the video; version **0.3** shipped **4 days** after that, announced in the "Dynamus community" / "Dynamus Project Showcase."
- Creator: **Michael Kinsey**, built at **Hewlett Packard Enterprise (HPE)**; HPE's open-source office sponsors the project.
- Timeline: **end of April** — committed a **5,900-line** scaffold of Pi rewritten in Go (and by his own account, Pi helped write it). **End of May** — it was his daily coding agent.
- Repo at **339 stars**; upstream Pi has **more than 110,000**.
- Six things deliberately kept out of PiG's core (mirroring Pi): **no built-in MCP, no sub-agents, no permission system, no plan mode, no to-do list, no background shell** — add them as extensions or don't.
- Every PiG release is pinned to one Pi version; currently **0.87.1**. The repo publishes a scorecard: **424 of 564 files ported (~75%)**, with **47** checked against real Pi behavior using **617 paired test scenarios**. Behavioral differences are labeled a bug or a documented divergence.
- **Benchmark (PiG's own numbers):**
  - `--version`: median **21.5 ms** vs **300 ms** for Pi, using about **a quarter of the memory**.
  - One prompt against a local mock model: **29 ms** vs **440 ms**.
  - Caveat: runs used a **single-core Linux box** and a build **from before version 0.2**.
- **Where the gap closes:** load TypeScript extensions and PiG goes from **8% faster to 19% slower** than Pi, because it must start Node for them. The core binary never needs Node; your TypeScript extensions still do.
- **Install (Ubuntu under WSL):** one `curl` line downloads the release, verifies it against published checksums, and refuses to install on mismatch. Windows gets a one-liner PowerShell install but is still labeled **preview**.
- Observed `pig version` output: **PiG 0.3 tracking Pi 0.87.1**; file is **55 MB** (per-file/per-binary size noted after the 155 MB initial figure); version check came back in **14 ms**.
- **41 built-in providers** ship with PiG; **Ollama is not one of them** — a fully local setup requires writing one JSON config file pointing PiG at your server.
- **Two config settings that mattered most** (both found by getting them wrong):
  1. **Context length.** First attempt gave Qwen a **131,000-token** context; **11% of the model spilled onto the CPU** and every agent turn took **30–50 seconds**. A copy of the model capped at **32,000 tokens** fits entirely on the **7900 XTX**, and turns dropped to a few seconds.
  2. **Thinking.** Qwen reasons by default; in one run it burned **14,000 tokens** "tracing strings in its head." Mapping PiG's minimal thinking level to a llama's **`none`** turned it off.
- **Real test** (empty folder, one prompt: build `pigsay` — cowsay but with a pig — plus a test file, run the tests):
  - Session starts by listing a home folder that doesn't exist, runs `pwd` to find the actual location.
  - Writes **three files**, then hits **seven failed test/vet runs**: a `break` statement outside a loop → an off-by-one in the bubble width → and the author's favorite bug, an ASCII pig whose drawing **contained back ticks**, which in Go end a raw string literal, so the drawing broke the compiler.
  - It found them with a **one-line Python script**, redrew the pig without back ticks, and the **eighth run passed**. Total: **just under 5 minutes**, entirely local.
  - Verdict: the drawing "looks more like an owl on stilts, but the loop works." The seven failures were blamed on **Qwen, not PiG**.
- **Extensions:** PiG extensions can be written in **Go**. One command scaffolds an extension from a **name and a language**, producing **two files**; the `.go` file registers **three things**: a **tool** the model can call, a **slash command** for the user, and a **status line** for the footer. Load with `e` and the footer shows `oink loaded`; `/oink` prints `hello from oink`; asking Qwen to call the tool returns `pong from oink`.
- Since **0.3**, PiG also loads **Pi's own JavaScript packages** — the MCP adapter package for Pi runs there too, though release notes warn **not every package is qualified yet**.
- **Piglets:** a short **YAML** file defining one agent (model, extensions, tools, prompt). The author's is **nine lines** (local Qwen + the Oink extension). `pig build` compiles it into its own executable: **first build 26 seconds**, **rebuild 6 seconds**, producing a **55 MB** `pig oink` binary that already knows its model and tools.
  - **Catch:** a binary build requires the **PiG source checked out and `go` on your PATH**; without the source the build stops and asks for the **source root variable**.
  - Once working: you can hand your team one agent as one file and sign it — but they still bring their own model access.
- **Known limitations / risk:**
  - Still a **0.x** release; **a quarter of Pi's files aren't ported**.
  - **Windows is preview**; **macOS binaries are not notarized**.
  - Runs with your permissions and ships **no sandbox**, same as Pi — the README says use a **container or VM** for isolation.
  - Opt-out install `ping` sends **only the version number**.
  - Upstream moved the day PiG 0.3 shipped: **Pi 0.99 added built-in MCP**, while PiG is still pinned to **0.87**, and per the author, porting upstream changes still needs manual work.
- **Alternatives/positioning:** if you only want a Go-written coding agent, **Charm's Crush** already exists; PiG's differentiator is **Pi compatibility down to Pi's own extensions**.
- Recommendation: install PiG if you write Go or want to ship an agent as one file. **Don't switch for the startup numbers if your setup runs TypeScript extensions** (that gap mostly disappears). **Stick with Pi** if you need upstream features like the new MCP support the week they land.

## Technical Details

- **Architecture / design philosophy**
  - PiG copies Pi's minimal-core design rather than reinventing it — the divergence is implementation language, not feature set.
  - Deliberate non-core features (the "six things that stay out of the core"): MCP, sub-agents, permissions, plan mode, to-do list, background shell.
  - **Version-pinning model:** each PiG release tracks exactly one Pi version; compatibility is verified by a published scorecard (files ported + paired behavioral tests) rather than by CI parity.
  - **Parity methodology:** paired test scenarios run against real Pi behavior; mismatches are triaged as bug vs. documented divergence.
  - Extension runtime is hybrid: **Go-native extensions** for tools/slash-commands/status lines, plus **Pi JavaScript packages** (loaded since 0.3) which reintroduce a Node dependency.
  - **Piglet** is a declarative YAML agent spec (model, extensions, tools, prompt) compiled by `pig build` into a self-contained executable.

- **Binary / performance characteristics**
  - Single static binary; core path requires **no Node and no cloud account**.
  - `--version` latency: ~21.5 ms vs Pi's ~300 ms; ~1/4 the memory; 14 ms observed locally on a 55 MB binary.
  - Startup advantage is a function of extension language: Node-backed TypeScript extensions erase it (8% faster → 19% slower).
  - Benchmark caveats: single-core Linux host, pre-0.2 build.

- **Local model integration**
  - **41 built-in providers; Ollama unsupported** → hand-written JSON config pointing at a local server.
  - Local LLM (Qwen) on an **AMD 7900 XTX** GPU; context length must be trimmed to fit VRAM (131k → 32k) or ~11% of the model offloads to CPU and turns take 30–50 s.
  - Thinking must be disabled (minimal thinking level → llama `none`) to avoid ~14k tokens of hidden reasoning per run.

- **Installation / supply chain**
  - `curl` one-liner for Ubuntu/WSL that downloads the release, checks it against **published checksums**, and aborts on mismatch.
  - One-liner PowerShell install for Windows (preview).
  - macOS binaries present but **not notarized**.
  - Telemetry: opt-out install ping sends **only the version number**.

- **Extension SDK contract** — a PiG Go extension scaffolds to two files, and the `.go` file registers exactly three things:
  1. a **tool** callable by the model
  2. a **slash command** for the human
  3. a **status line** for the footer

- **Agent distribution model**
  - `pig build` compiles a piglet YAML into a single signed executable (26 s cold, 6 s incremental).
  - Build-time prerequisites: **PiG source tree checked out** + **`go` on PATH**; missing source triggers a prompt for the **source root variable**.
  - Binary bundles config (model, tools, extensions) but **not** model credentials/access.

- **Isolation model:** none. Executes with user permissions; upstream guidance is container or VM.

- **Version strings reported on screen:**
  ```
  PiG 0.3 tracking Pi 0.87.1
  ```

- **PiG-native commands referenced:**
  ```
  pig version
  pig build
  ```
  **Pi-ecosystem commands referenced:**
  ```
  pwd
  ```
  **Footer / in-agent commands referenced:**
  ```
  e
  /oink
  ```

- **Sponsorship/community:** creator posts every release in the Dynamus community project showcase; community-owned and sponsored by HPE's open-source office. (Promo segment referenced Dynamus AI Mastery courses, a Dino Chat feature, and a 10% discount link.)

## Questions

- What are the exact `curl` and PowerShell install commands (and checksum/signature mechanism — SHA-256? GPG?) shown on screen? Not stated.
- What is the exact JSON config file path and schema for pointing PiG at an Ollama-compatible server? The transcript only says "one JSON file" and "two settings."
- Which 47 of the 424 ported files are the behaviorally verified ones, and where is the scorecard hosted (a docs page, a CSV, CI output)?
- What is PiG's actual current completeness trend — is the 25% unported set mostly peripheral, or does it include features users rely on?
- How much manual work is a typical upstream port when Pi releases a breaking change? "Still needs manual work" is unquantified — is there a documented rebase procedure?
- What are the 41 built-in providers, and why is Ollama excluded (maintenance, licensing, protocol mismatch)? Are other local runtimes (llama.cpp server, LM Studio, vLLM) supported?
- Does the "one-line Python script" used to hunt the bugs have a name or is it ad-hoc? Worth verifying the actual command if reproducing the demo.
- What were the seven failing test/vet runs in exact order, and which were PiG/tooling defects versus Qwen output errors? The transcript attributes them to Qwen but doesn't separate PiG's own bug rate.
- What is PiG's memory footprint precisely ("about a quarter of the memory" — quarter of RSS? peak? against which Pi build and which version comparison)?
- Is macOS notarization planned, and does Windows "preview" cover ARM64? Are there known WSL-specific issues?
- Does the JavaScript-package loading path in 0.3 have a documented list of "qualified" Pi packages, or is qualification ad hoc?
- What exactly is Pi 0.87.1 vs 0.99 in terms of the other changes PiG is now missing besides built-in MCP?
- How is the piglet binary signed (what tool, what key distribution), and would a verifying party need the PiG source to check it?
- What is the source root variable actually called, and can a release binary build a piglet without a source checkout (e.g., embedded source or prebuilt SDK)?
<!-- yt-brain:related -->

## Related

- [[youtube/YouTube Knowledge Base|◻️ YouTube Knowledge Base]]
- [[youtube/agents|📁 AI Agents & Orchestration]]
- [[index|🏛️ JARVIS Memory Vault]]

### Related notes

- [[youtube/agents/2026-09-29-claude-code-multi-agent-orchestration-with-opus-4-6-tmux-and|Claude Code Multi-Agent Orchestration with Opus 4.6, Tmux and Agent Sandboxes]] · relevance 0.07
- [[youtube/agents/2026-11-13-an-ai-agent-with-its-own-cursor-on-omarchy-cua-edge-channel|An AI Agent with Its Own Cursor on Omarchy (Cua, Edge Channel)]] · relevance 0.06
- [[youtube/agents/2026-10-03-he-finally-10x-claude-code-with-this-method|He Finally 10x Claude Code With This Method]] · relevance 0.06
- [[youtube/agents/2026-10-03-this-ai-can-edit-its-own-code-and-evolve-its-free|This AI Can Edit Its Own Code and Evolve (its free)]] · relevance 0.06

<!-- /yt-brain:related -->
