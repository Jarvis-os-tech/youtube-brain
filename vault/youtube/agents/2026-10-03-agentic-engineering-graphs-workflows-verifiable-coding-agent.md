---
video_id: epg292lGCZ4
title: "Agentic engineering: Graphs, workflows, verifiable coding agent runtimes, and staying in control"
url: https://www.youtube.com/watch?v=epg292lGCZ4&t=214s
watched: 2026-10-03 15:03
source: chrome:Default
indexed: 2026-10-03T12:21:42+00:00
topic: agents
type: youtube-note
source_url: https://www.youtube.com/watch?v=epg292lGCZ4&t=214s
tags: [youtube, youtube/agents]
---



## Core Concept

Agentic engineering is a control-systems problem, not a prompting problem. A control loop compares the codebase against acceptance criteria and repairs it; a DAG (graph) coordinates which stages depend on what and what can run in parallel; and a **verifiable coding agent runtime** — Atomic, an open-source TypeScript project the speaker works on at Microsoft Research — supplies the deterministic gates, artifacts, and checkpoints that make multi-hour and multi-day runs inspectable by a human. The thesis: correctness must be a property of the system you build, not a claim the model makes, so agents can own long tasks (a 130-commit-plus feature spanning database, API, and security work) while real engineering still needs evidence-backed gates and human judgment. Reliability, the speaker argues, comes from the graph topology and from artifacts that a human can inspect — not from the model's own narration.

## Key Takeaways

- **Runtime definition:** Atomic defines a runtime as "an environment that your agents can execute in" — the agent-world analogue of "node or bun for JavaScript." It owns sessions, tools, models, and state.
- Atomic contains a **workflow runtime**: graph-based, handling durability, resuming, rate limit handling, and fallback models — "to be as fault tolerant as possible for multi-hour, multi-day or even multi-week sessions."
- **Verifiable** means every claim is inspectable by the engineer: outputs, test results, artifacts, checkpoints. "It's actually some proof of completion and otherwise it didn't happen" — explicitly contrasted with "the model saying that it's done."
- Atomic is framed as "applying CI-level trust to agent execution," motivated by open source: regressions shipping, and wanting "a control plane that engineers can own."
- **Control theory mapping** (slide 2, left to right): acceptance criteria = set point / desired state ("we want all test cases to pass"); **workflow policy = controller**; **agent + its tools = actuator** ("what everyone is talking about with the harness"); **codebase = plant**; **tests, linters, independent review = sensors** returning feedback/error to the controller.
- Engineering is "a multi-stage machine that is implementation, checking, fixing, and repeating until CI is green" — unit, integration, end-to-end. Loops make that cycle executable "through bounded, tracked iterations with explicit stop conditions."
- Loop statuses are explicit: **pass → repair → fail / stop when the budget ends**. "The output varies, but the control stays explicit." Status indicators are sent back to the engineer so a multi-hour run can be audited instead of probed by hours of model interrogation.
- The control-loop framing is credited as inspired by **Dexory** and **The Human Layer**; the speaker's own contribution is framing a *verifiable agent runtime*.
- "A transcript records the work but a graph coordinates the work." A graph is "the shape of a run": stages/sessions are **nodes**, handoffs are **edges**, and the structure is a **DAG** for agent work (cycles are possible but are "more complex behavior").
- Graph engineering is to multi-agent systems what prompt engineering is to a single model: which stages run in parallel, where verification gates sit, what evidence flows between them, when a loop stops. "Reliability comes from this topology."
- The questions a graph answers: **dependency understanding**, **readiness** (blocked vs. done vs. defer to human), **parallelism**, **evidence** (stays attached to the work that produced it, so "one failed branch is repaired without redoing the test"), and **control** (pause/resume a node; steer the graph while it works).
- Concrete steering example: on a CI regression, jump to a sub-workflow that tries to reproduce the error, then file it to a **GitHub issue** or a **Linear ticket**.
- The real graph example was **not hand-generated** — he posted it on X and the agent discovered the repo's conventions and fanned out the work itself: a **security audit that ran for 30 minutes**, a deployment plan, a migration audit, a user-impact/user-testing pass, and key lifecycle checks — against the 130-commit-plus feature.
- Atomic's graph syntax is **TypeScript**, executed by "a combination of Node and the agent runtime"; real JS primitives like `await` create an event-loop barrier, so the runtime is "almost like an interpreter of sorts that's dynamically executing this graph."
- **Verifiable primitives**, each producing evidence: stages, durable checkpoints, tool calls, artifacts, verification gates, structured outputs, human approval points.
- **Verification pipeline stages:** **propose** (model writes a change; not trusted) → **measure** (deterministic, agent-free: tests, type checks, builds, browser flows, any runnable command; screenshots or short recordings for UI work, attachable to PRs) → **review** (a **fresh verifier**, possibly a model, reporting from a clean session given files + evidence from measure) → **decide** (a model proposes an outcome from those reports under a **bounded repair-and-review cap**). That repair/review cycle is itself a sub-loop scaled to the assurance you want; for critical work it may run "for hours or days."
- Atomic uses the **typebox** library for structure validation at build time — "if you're familiar with Python, it's like pydantic" — catching missing fields, wrong types, and undeclared outputs. Workflows are type-annotated. Caveat: shape checks "only prove that the data looks right, not that the code works."
- Review policy: manual code review can only be skipped when the checks are "comparatively cheap, objective, and hard to spoof." Even then, produce evidence the behavior works and concentrate human review on **critical code paths**. He pushes back on skipping review — verification also matters for **participation**: humans gain understanding, which generates new ideas.
- Framing discipline: "I like to separate Atomic from graph engineering... I don't treat it as really graph engineering. I treat it as like building reliable software." What matters is producing **artifacts an engineer can review**. Anti-hype: "I don't want to drive a hype train that oh this is AGI, because it's not."
- Borrowed from **Adi Osmani**: the **judgment filter** — "we decide what goes into production and we're responsible for what goes to production." Acceleration is not a license to ship slop or regressions.
- Context management = "deciding what each stage is allowed to see," framed as an optimization: you can't hand every stage the whole repo because "it could add noise, it could cost more, and it could bias the next decision."
- **Fresh context window** (left lane): clean model session seeing only prompt, system prompt, files, and evidence you hand it. Preferred for reviewer sub-agents.
- Theoretical reason: models are **autoregressive** — the next token depends on the cumulative probability of previous tokens — so a reviewer agent "is inherently a biased estimator that you're trying to have review your code." A new context window, or small artifacts passed between worker and reviewer, gives better results with cited evidence.
- **Forked context window** (right lane): continue from an earlier conversation while keeping decisions already made. Good for worker/implementer agents, to avoid re-discovering things and wasting tokens, and to self-correct from a previous trace.
- Concrete pattern: the implementer writes a **patch summary and test results to a file**; the workflow passes those files to the reviewer, which reads them.
- **Pass artifacts, not context, between stages.** Stages hand off "declared values, outputs, files, and reads" — that handoff is the interface. Artifacts are files the model searches selectively; tokens are what get loaded into the context window. Atomic's generated workflows **save artifacts as files** automatically — "one of the principles in Atomic that's emphasized" — against the common mistake that "context is finite."
- **Verbatim compaction, not summary compaction.** Near a context limit, Atomic drops selected older messages and protects recent ones; it does not generate a lossy summary before overflow. Cited research shows verbatim compaction "significantly outperforms summary compaction," and this trick alone helps scale to multi-hour/multi-day runs.
- "Summaries lose resolution; verbatim compaction retains resolution." A summary may forget a failing test case or paraphrase an error unintuitively; with verbatim compaction the model has a **delete context tool** and can prune passing test cases while keeping failing ones.
- **Durability = keeping finished work when the process stops.** The scheduler checkpoints every completed step so you can roll back, or resume after an error/mid-run interruption instead of restarting.
- **Dual checkpointing.** One checkpoint tracks *which node in the graph* you're on plus that node's dependencies; the second, inside a language-model node, resumes at the *exact point in the trace* where the failure or pause happened. Necessary because models mutate the filesystem mid-workflow — "without a good revert mechanism you confuse the next iteration."
- Lifecycle vocabulary: **resumption → redispatching → replaying work → continuing incomplete work.**
- **Pause / steer / control.** Pausing a workflow pauses all dependent nodes in the DAG so execution doesn't race. Interrupting does the same DAG pause. Quit ends the execution, resumable after.
- **Steering a workflow ≠ steering a chat.** In chat your question continues the model's train of thought; in autonomous multi-hour/multi-day runs it doesn't — observed behavior was a model "simply answer a steering question and stop working." Atomic injects a deterministic hook message — "continue working, the user was just steering you" — after a steered session finishes. The hooks are auditable: "a further level of reliability."
- **Self-correcting workflows.** The model gets a **workflow tool primitive** and can modify the workflow it created, so workflows effectively do automated QA. Highlighted especially for *dynamic workflows* as "interesting emergent behavior."
- **Skills → workflows:** ask Atomic to convert a skill to a workflow.
- Progression (also in Ray's post): **prompts → skills → workflows → graphs.** Most people writing skills are implicitly writing a state machine ("first do this, then do this, if it fails do that") — encode those as states so you can **audit** instead of relying on the model's thinking trace.
- **Brownfield onboarding:** install Atomic and start with the built-in workflows rather than hand-rolling. Named built-ins: the **goal workflow** ("more reliable than the slash goal in Codex") and the **Ralph workflow** (research + verifier stages, an orchestrator stage that spawns parallel agents, adversarial reviewers); also a **research codebase workflow** and **research codebase skill**.
- **Recommended first real workflow:** create a GitHub ticket for the feature, ask Atomic to tackle the issue in a **separate git worktree**, let it spawn and run the workflow in the background, then probe what it's doing — possible because Atomic is plugged into the workflow tool itself with full understanding of the running workflow.
- **Then customize:** build workflows tailored to the codebase, your style, your team. Engineers reported a custom workflow saved "at least one and a half hours per ticket" (he stresses this is conservative). The power comes from *uber*-customizing so workflows encode that codebase's practices.
- The speaker's favorite skill is **`create spec`** — inspired by high-quality PRDs/specs from Microsoft, Amazon, Google, Apple; a combination of problem-framing approaches that asks you specific implementation questions, versus the "grill me" style. With a workflow on top he's seen complex implementations land one-shot/zero-shot.
- Why precise specs: current models "have the tendency to over scope too much" — rewriting your entire backend because it deems it suboptimal, or a 50,000-line PR where multiple ~100-line PRs (e.g. GitHub stacks) were possible.
- **Verifiability as the category:** Atomic is positioned as the first runtime of its kind — not just extending the runtime idea, but adding verifiability for high-assurance systems and reproducible agent results, "rather than relying on the model's own narration." Brownfield codebases are named as where it shines best.

## Technical Details

- **Atomic** — open-source verifiable coding agent runtime; "the runtime for agent work." Owns sessions, tools, models, state, plus a workflow runtime for durability/resume/rate limits/fallback models. Implemented in TypeScript with typebox.
- **Runtime (definition)** — "an environment that your agents can execute in," compared to "node or bun for JavaScript."
- **Workflow policy** — the controller: "a way to define a graph of what happens in the execution of the model."
- **Graph primitives in Atomic's TypeScript SDK:**
  - pass a prompt
  - control context with a fresh context window, and **fork** context windows
  - structured output via a **schema**
  - spawn **parallel branches**, with controllable **concurrency** ("you want to prevent from getting rate limited")
  - **fail fast** — "sometimes an error is okay, but sometimes it should halt the execution and should go back to the agent to delegate what happened"
  - `await` dependencies, create dependencies, bound concurrency, join tasks
- **Mapbox-style fan-out/fan-in** (as done by "rays waves") cited as the partition-work pattern: split into worker agents, then synthesize.
- **Execution model** — runtime = Node + agent runtime; JavaScript `await` creates an event-loop barrier so execution blocks until dependencies are constructed; the runtime dynamically interprets the graph.
- **Control-loop statuses** — `pass`, `repair`, `fail`, `stop when budget ends`; status indicators reported back to the engineer for auditability.
- **Evidence surfaces** — outputs, test results, artifacts, checkpoints, screenshots or short recordings of browser flows, artifacts attached to PRs.
- **Validation** — `typebox` for build-time structure validation (pydantic equivalent); typed workflow contracts catch missing fields, wrong types, undeclared outputs; does not prove code correctness.
- **Human-in-the-loop points** — readiness can defer to a human; approval points are first-class primitives; critical code paths get emphasized human review.
- **Subgraph steering targets** — reproduction sub-workflow → GitHub issue / Linear ticket on a CI regression.
- **Agent fan-out context rule** — findings from a sub-agent return *into the implementer's fork* (not inherited into it), so the reviewer/verifier can't bias the implementer, then the loop continues. The parent does **not** inherit the sub-agent's context window.
- **OS analogy for context engineering** — CPU threads ≈ sub-agents; memory ≈ context you manage directly; context engineering = "manual memory management."
- **Review loop** — decider proposes an outcome under a bounded repair-and-review cap; the cycle is a tunable sub-loop scaled by required assurance (hours or days for critical paths).
- **Review-skip precondition** — checks must be "comparatively cheap, objective, and hard to spoof."
- **Stage interfaces / handoff artifacts** — *declared values, outputs, files, reads*; artifacts persisted as files, not injected into the context window.
- **Compaction** — `verbatim compaction` (selective deletion of context elements instead of summary-at-overflow) vs. summary compaction in "other coding agents / other runtimes"; model-side `delete context tool` for pruning.
- **Durability / checkpointing (two levels)** — graph-level: current node identity + node dependency tracking; trace-level: exact checkpoint inside the node's context window. Enables roll back, resume mid-run, resume after quit, preserve the thinking trace, and avoid filesystem confusion on resume. Lifecycle verbs: `resume` → `redispatch` → `replay` → `continue incomplete work`.
- **Control surface:** `pause`, `interrupt`, `quit`, `resume`
  - `pause` / `interrupt` → pauses all dependent DAG nodes (no races; dependencies respected)
  - `quit` → ends the workflow execution; resumable afterward
  - deterministic continuation hooks auto-inject a "keep working" message post-steer
  - workflow tool primitive exposed to the model → self-modifying/self-correcting workflows, including dynamic workflows
  - diagram framing: **observe, steer, control**
- **Built-in workflows / skills** — goal workflow; Ralph workflow (research, verifier, orchestrator with parallel agent spawn, adversarial reviewers); research codebase workflow; research codebase skill; `create spec`; skill→workflow conversion.
- **External products referenced by name** — GitHub issues, GitHub stacks, git worktrees, Codex `/goal` (slash goal), PRDs from Microsoft/Amazon/Google/Apple, Ray's post (prompts → skills → workflows → graphs), Mapbox fan-out/fan-in.
- **Attributions** — control-loop framing inspired by Dexory and The Human Layer; judgment filter framing from Adi Osmani.
- **Trade-offs stated:**
  - Artifacts-as-files: more context-efficient, prevents overflow and model divergence — at the cost of requiring the model to search rather than having context preloaded.
  - Verbatim compaction: retains resolution, beats summary compaction in research — requires a working context-pruning mechanism (the delete context tool) to be useful.
  - Trace-level resume: preserves reasoning, reduces confusion from partial filesystem mutations — at the cost of implementation complexity (dual checkpointing).
  - Unfiltered autonomy: gains throughput (1.5+ hrs/ticket reported) — requires deterministic continuation hooks, since steering a multi-day run is more nuanced than steering a chat.
  - Scope control: precise specs + graphs instead of trusting the thinking trace, to prevent 50k-line PRs.
  - Customization over out-of-the-box: built-in workflows for onboarding, then codebase-specific workflows as the real source of value.
- **Diagram framing** — **observe, steer, control** as the human-in-the-loop surfaces for durable workflows.

## Questions

- No code was shown verbatim — the Atomic SDK slide was described (prompt, context control, schema, parallel branches, concurrency, fail-fast, worker/synthesizer pattern) but the TypeScript snippet was not reproduced. Exact API names and signatures are unverified.
- The live example/demos, the build walkthrough, and any specific commands, CLIs, flags, or file paths are missing from these notes.
- The evidence for fresh-context reviewers is asserted ("there's evidence that it explains this directly") with no study, paper, or metric cited.
- Which publication shows verbatim compaction "significantly outperforms summary compaction"? No citation, author, or numbers.
- No quantitative numbers anywhere: no context-window sizes, no compaction percentages, no resume-time savings, no cost/token/reliability numbers, no false-positive/negative rates for gates — only "30 minutes" for the security audit, "130 commit plus" scope, and the anecdotal "at least one and a half hours per ticket."
- No comparison of Atomic's goal workflow vs. Codex `/goal` beyond "more reliable."
- Unspecified: default concurrency limits, rate-limit thresholds, repair/review cap defaults, checkpoint format and storage, multi-day session durability implementation, and how fallback models are selected.
- Unspecified: how the agent "discovers" repo conventions and generates the graph itself — the mechanism, prompting, or config behind a 130-commit review fan-out.
- Unspecified: what "Atomic" stands for, the repository/URL, whether the graph syntax is stable/versioned, and the license.
- Unclear how trace-level checkpoint persistence/restore works per model provider, and the recovery guarantee if failure was mid-tool-call or mid-file-write.
- Unclear what the filesystem rollback mechanism actually is (snapshotting? `git worktree reset? something else) — "a good revert mechanism" is stated but not specified.
- Unclear what the deterministic hooks look like: trigger conditions, ordering, exact injected message, and how they're "auditable" (where the hook log lives).
- No guardrails, sandboxing, or blast-radius constraints described for the self-modifying workflow primitive.
- Unclear how screenshot/recording capture for browser flows works (driver, storage location, attachment to PRs), and how the decider's bounded repair-and-review cap is expressed in the SDK or whether the decider is a model or a rule.
- Where the `create spec` methodology is published and whether it's usable outside Atomic; exact names/APIs of built-in workflows and skills as commands or file paths.
- No pricing, licensing, install command, platform support, or model-provider support for Atomic.
- The Q&A on brownfield codebases was cut short ("it's actually quite simple, right?"); integration mechanics beyond "install it and start with built-in workflows" weren't detailed.
- Where human judgment "belongs" is argued but not formalized — humans as "participants" rather than always verifiers is asserted with no proposed model for the shift.
- Whether "GPT 5.6 six" refers to a real released model or is an auto-caption transcription artifact is unclear.
<!-- yt-brain:related -->

## Related

- [[youtube/YouTube Knowledge Base|◻️ YouTube Knowledge Base]]
- [[youtube/agents|📁 AI Agents & Orchestration]]
- [[index|🏛️ JARVIS Memory Vault]]

### Related notes

- [[youtube/agents/2026-10-08-andrej-karpathy-from-vibe-coding-to-agentic-engineering-w-st|Andrej Karpathy: From Vibe Coding to Agentic Engineering w/ Stephanie Zhan]] · relevance 0.12
- [[youtube/agents/2026-11-13-local-ai-isn-t-ready-yet-so-i-built-an-omarchy-ai-shed-and-r|Local AI Isn't Ready Yet - So I Built An Omarchy AI Shed And Run Claude From My Phone]] · relevance 0.11
- [[youtube/agents/2026-09-29-claude-code-multi-agent-orchestration-with-opus-4-6-tmux-and|Claude Code Multi-Agent Orchestration with Opus 4.6, Tmux and Agent Sandboxes]] · relevance 0.11
- [[youtube/agents/2026-10-03-ai-software-factories-are-the-next-big-thing-and-i-m-buildin|AI Software Factories Are the Next Big Thing (And I'm Building You One)]] · relevance 0.10

<!-- /yt-brain:related -->
