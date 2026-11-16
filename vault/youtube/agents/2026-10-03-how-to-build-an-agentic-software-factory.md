---
video_id: lOedDFKrC7Y
title: "How to build an Agentic Software Factory"
url: https://www.youtube.com/watch?v=lOedDFKrC7Y
watched: 2026-10-02 20:15
source: chrome:Default
indexed: 2026-10-03T02:51:05+00:00
topic: agents
type: youtube-note
source_url: https://www.youtube.com/watch?v=lOedDFKrC7Y
tags: [youtube, youtube/agents]
---



## Core Concept

Most teams are stuck at "level 3" of agent usage, where agents generate large PRs but humans become the review bottleneck because the model repeatedly violates repo conventions. The path to a "software factory" (level 5 — hand off a requirement, get merged user value without reading the code) requires two things: **documentation** (CLAUDE.md, architecture docs) and **guardrails** (linters, tests, a review loop). Each human review correction should be converted into a permanent rule so the same mistake never recurs.

## Key Takeaways

- **Five levels of agent adoption:** (1) advisor — copy/paste snippets to/from ChatGPT or Claude, used for the last ~2–3 years; (2) pair programming — agent solves part of the task, you refactor by hand; (3) big PRs — you become the bottleneck, e.g. a 40-file PR getting 20 comments, then 20 more, then 15; (4) autonomous — 40-file PR where you have only one or two changes to request, or none; (5) software factory — you hand off the requirement and it ships pure user value.
- **Level 3 →4 needs only two things:** documentation and guardrails.
- **The core loop:** don't tell the model "fix those 20 issues" in the PR — instead extend CLAUDE.md so those issues never happen. Every correction becomes a rule.
- **Five pillars:** CLAUDE.md, architecture docs, deterministic guards (linters), tests, and the review loop.
- **CLAUDE.md cannot hold 10,000 lines** — in a monorepo, use separate docs (front-end, back-end, database) and route to them: "if you're making a change in the front end, go to front-end.md."
- **Architecture docs should describe services *and* user journeys** (e.g. `user-journeys.md`: the file-upload journey goes to a page → a service → S3 → Postgres). Reason: it's easier for a model to read 3 files than 40 to figure out how the system works.
- **Prose isn't enforceable** — "AI doesn't have to follow this prose." Linters restrict it. Custom rules cited: "do not create a barrel in this folder", "use this state hook and not the other one", "do not use these two components together, use another component instead."
- **Ask AI to write the lint rule for you** rather than writing it by hand.
- **Tests are the most important pillar** — "your architecture can be nice, code can be nicely written, but if your app doesn't work, it just doesn't work."
- **The parallel-PR problem:** with 6 PRs from 6 agents, manually clicking through each work tree doesn't scale. Automation via tests: back-end integration tests (hundreds to thousands, fast, high coverage), Storybook-style interaction tests (render page with mocked data, click, fill a form, assert the API is called on submit), visual tests, and a small number of E2E tests.
- **Keep E2E count low** — they run long, require a deployed web app, and are prone to flakiness.
- **Storybook/Vitest abandonment is no longer an excuse:** enforce tests with a linter rule — any `*.page.tsx` must have a nearby `*.test.tsx`, otherwise PR gates fail.
- **Visual testing problem:** 10 agent PRs all touching the UI can pass interaction tests while breaking design tokens or shared components. The speaker built **uiverify.ai** for this.
- **uiverify.ai workflow:** on every PR it screenshots all Storybook stories, Playwright end-to-end tests, and Vitest components, compares them against baselines in `main`, reports the diffs, and AI classifies them as regressions vs. intended. The same agent that authored the PR pulls the diffs into context and fixes them. Free for early adopters.
- **Second-model review:** a *different* model runs on every PR in GitHub, goes deeper than the authoring model, checks whether CLAUDE.md and rule documents were violated, then approves.
- **Daily skills:** *review loop* (runs Claude and Codex in parallel, collects findings, fixes, repeats until convergence or only nitpicks the two models disagree on); *E2E verify* (runs your app on unique ports so 10 agents can each have their own web app version, then Playwright + MCP drive it); *babysit PR* (opens the PR, pings it every 10 minutes for failed jobs or reviewer comments, fixes and pushes again, waits for green checks or no review comments); *add rule* (a CLAUDE.md meta-instruction to convert any human pushback into a CLAUDE.md or lint rule); *evaluate* (reads the whole Claude Code session to check whether it violated your rules — e.g. skipped the E2E verify step — then updates the skill or adds rules); *factory* (umbrella: docs fed in via CLAUDE.md → implement → review with two models in parallel → browser verify if needed → babysit the PR; input is a Linear ticket, output is a merge-ready change).
- **Organizational advice:** invest in agentic infrastructure from wherever you are (level 1–3 all have room to improve). Have one or two people spend a few days to a week adding skills and CLAUDE.md rules. A reviewer bot was added and now handles many PR approvals/comments.

## Technical Details

- **Terminology:** "CLAUDE.md" (transcribed variously as "Code MD" / "Cloudinary" / "Claude code" / "Cloud MD") is the per-repo agent instruction file created on first install of Claude Code; the talk's advice is to treat it as a constantly extended rulebook.
- **Model routing for review:** Claude and Codex run in parallel as independent reviewers, which gives diversity so that convergence criteria can be "only nitpicks the two models disagree about."
- **Test taxonomy and trade-offs:**

  | Layer | Purpose | Notes from talk |
  |---|---|---|
  | Back-end integration tests | Service → DB write → retrieve | hundreds/thousands, quick, broad coverage |
  | Storybook interaction tests | Render page isolated with mocked data, click button, fill form, assert API call on submit | "very easy to write with AI" |
  | Visual tests | Detect CSS/design-token/shared-component regressions | needs a baseline on `main` |
  | E2E tests | Whole-stack verification | keep few; slow, needs deployment, flaky |

- **Work tree / unique port isolation:** each agent gets its own checkout and its own listening port so N agents can run N full stacks concurrently. Automation is driven by Playwright + MCP.
- **Gating:** CI gates + a second-model PR reviewer + visual diff review; a PR is only merged after green checks and zero open review comments.
- **Rule-targeting routing pattern in CLAUDE.md:** front-end change → `front-end.md`; DB access change → `database.md`; user flows → `user-journeys.md`.
- **Monorepo implication:** split rules per top-level area (web, backend, etc.) instead of one global file.
- **No code, commands, or file paths were shown verbatim in the transcript.** The only literal artifacts named are: `*.page.tsx` (must be paired with `*.test.tsx`), `front-end.md`, `database.md`, `user-journeys.md`, CLAUDE.md, and the products uiverify.ai / Claude / Codex / ChatGPT / Playwright / Storybook / Vitest / S3 / Postgres / Linear. Visual-testing inputs are described as "Storybook stories, Playwright and e2e tests, and Vitest components"; Storybook is explicitly said to be optional ("not necessarily Storybook").

## Questions

- What are the exact contents of the "very small snippet" and lint rule behind the QR code? Not spoken aloud.
- What URL/hosting model does uiverify.ai use, and how are baselines stored and reviewed in practice?
- Which specific linters are used to implement custom rules (ESLint plugins, custom CI checks, Biome, etc.)? Only the rule *content* was described, never the tooling.
- What are the exact E2E verify and babysit PR implementation details — the unique-port allocation strategy and the CLI invocation (`I run this command` is never named)?
- How is the parallel Claude/Codex review loop bounded — max iterations, cost, and timeout?
- What is the token/context size of the uiverify.ai diff payload, and how does the agent "get all of those diffs into the context" in practice (image-based diffs vs. structured data)?
- How is `factory` wired to Linear tickets (issue → requirement format, human-in-the-loop approval points)?
- How is regression vs. intended-change classification decided in uiverify.ai, and what is the false-positive/false-negative rate?
- Are visual baselines updated manually on merge, and who approves baseline changes?
- No quantitative results were given: no productivity/loc/PR-defect-reduction numbers beyond the claim that productivity "will skyrocket."
<!-- yt-brain:related -->

## Related

- [[youtube/YouTube Knowledge Base|◻️ YouTube Knowledge Base]]
- [[youtube/agents|📁 AI Agents & Orchestration]]
- [[index|🏛️ JARVIS Memory Vault]]

### Related notes

- [[youtube/agents/2026-10-03-ai-software-factories-are-the-next-big-thing-and-i-m-buildin|AI Software Factories Are the Next Big Thing (And I'm Building You One)]] · relevance 0.17
- [[youtube/dev-craft/2026-10-03-building-a-software-factory-that-actually-works-full-course|Building a Software Factory that actually works (Full Course)]] · relevance 0.13
- [[youtube/agents/2026-09-29-claude-code-multi-agent-orchestration-with-opus-4-6-tmux-and|Claude Code Multi-Agent Orchestration with Opus 4.6, Tmux and Agent Sandboxes]] · relevance 0.10
- [[youtube/agents/2026-10-08-andrej-karpathy-from-vibe-coding-to-agentic-engineering-w-st|Andrej Karpathy: From Vibe Coding to Agentic Engineering w/ Stephanie Zhan]] · relevance 0.09

<!-- /yt-brain:related -->
