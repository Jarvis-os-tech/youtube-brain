---
video_id: _LCeJZFIsd4
title: "Building a Software Factory that actually works (Full Course)"
url: https://www.youtube.com/watch?v=_LCeJZFIsd4
watched: 2026-10-03 11:16
source: chrome:Default
indexed: 2026-10-03T12:33:01+00:00
topic: dev-craft
type: youtube-note
source_url: https://www.youtube.com/watch?v=_LCeJZFIsd4
tags: [youtube, youtube/dev-craft]
---



## Core Concept

A "software factory" is a model- and harness-agnostic development workflow — not a product — encoded as a small set of markdown files (an `agents.md` plus roughly five or six skills) that let agents ship software at assembly-line speed without sloppy output. The workflow has four opinionated stages: **isolate** (every feature starts in a fresh Git worktree branched from `origin main`), **build** (a `code structure` skill enforcing service-layer architecture), **prove** (`evidence-driven testing` and `before and after` skills forcing before/after visual or measured evidence), and **ship** (a `Grep Loop` skill that runs an external code-review agent like Greptile until its confidence score maxes out). The goal is to replace ad-hoc prompting and back-and-forth with a repeatable, self-looping pipeline that many agents can run in parallel, with the results attributable to workflows, skills, and domain knowledge rather than to model choice.

## Key Takeaways

- **"Software factory" is going viral** — the assembly-line metaphor applied to software, letting one person use AI agents to ship software that "isn't sloppy at all" and create multiple revenue-generating apps.
- **Model and harness agnostic.** "It doesn't matter what model you use, it doesn't matter what harness you use." A factory is someone's workflow, skills, and domain knowledge "packed up in specific skills."
- **The baseline it replaces:** the loop of opening Codex / Claude Code / Cursor, saying "build this," disliking the output, iterating, then deploying to Vercel or production.
- **The failure mode it solves:** the old way is linear — one feature at a time. Multiple features on the same branch cause conflicts and agents overwriting or deleting files; most "my agent deleted a bunch of stuff" tweets are attributed to this.
- **The factory is ~5–6 files.** One is `agents.md` — a single markdown doc injected into the agent **chat on every message**, not the system prompt. He criticizes most `agents.md` files for restating what's already derivable from the codebase; his contains a workflow not native to the agent.
- **His skills are free** — but he asks viewers to understand the process rather than blindly copy it.
- **Step 1 — Isolate:** a skill named `new feature` with the verbatim instruction (below). A worktree is a copy-paste of the app at a moment in time; you work in the copy and merge back. Concurrent work by "me and Greg and another person, or you yourself with 50 different agents" no longer steps on itself. Demo: four terminal tabs on one app — an email client, a computer/Linux environment, a landing-page update. He jokes about renaming the step to "team" and that "isolate sounds like some sort of whey protein." Worktree cleanup after merge exists but isn't covered.
- **Step 2 — Build:** a `code structure` skill written in **service layer architecture**, so a human developer — or an agent returning cold — can read it. Models are "great at doing the work" but "if it could get it done in a sloppy way, it'll get it done in a sloppy way." Evidence: GPT-5.6 produced code that *worked*, then Fable reviewed it: "This is disgusting. Like there's duplications, there's functions all over the place, there's dead code." Real use case: a skills-like repository where agents connect to the app and store skills; the agent kept citing the `code structure` skill while writing.
- **Step 3 — Prove:** "agents can't pinky promise." Most models can be pushed into lying or admitting "I actually realized I didn't do this work for you" — GPT-6 Astra is called out as an improvement (least hallucinating, his favorite/most powerful workhorse). `evidence-driven testing` captures the *before* state (pre-feature, or the bug in action) and the *after* state, proving the fix; `before and after` is the fallback when the machine can't record, embedding both states in the PR. Media can be video or screenshots.
- **Prove examples shown:** (1) a PR for an admin email page plus connecting an email service, with a before state showing the page didn't exist and an after state; (2) a "give my agent a computer" feature where the first run failed on a different machine without the factory — after being told "use the skills, use the factory," the after screenshot showed the app working. Non-visual proof too: on a performance fix, page load went from **850 ms** ("a sin in web development") to roughly **60 ms**, with tests and results returned instead of screenshots.
- **The factory loops itself.** Skills are written so the agent recognizes unmet before/after criteria and returns to building on its own — "I didn't have to tell it."
- **Why prove matters to the human reviewer:** he's down to skimming, even barely. Before/after screenshots and video make review feasible for a non-technical "agent manager"; the host compares the flow to clicking through Instagram/TikTok stories, or a senior engineer reviewing a PR with a description and tests.
- **Step 4 — Ship:** a `Grep Loop` skill built around the third-party code-review agent **Greptile** (also mentioned: Macroscope, CodeRabbit, "tons of good ones"). He strongly recommends *some* code review agent for software real users will touch. Example: initial Greptile feedback flagged pagination issues and unpreserved menu space; confidence score was **3/5**, and after his agent addressed the feedback it became **5/5**. The loop runs automatically — "Someone doesn't have to write Grep Loop." At 5/5 Greptile reports "five out of five, unresolved comments" and presents the PR URL; the only remaining step is a human clicking **merge**, returning the work to the main version of the app.
- **Scale and automation claims:** "Automatically the agents will wait for a new score" — described as "a good loop." One merge was done while working on **15 simultaneous features** using different agents and sub-agents. Grep loop auto-activates by diff size: "If your file change is like 10,000 lines plus, um that skill activates"; smaller diffs the agent handles directly, so the user "doesn't have to worry. The agent does it itself."
- **Merge/deploy/release notes stay human.** After QC passes you still "have to merge it… deploy the PR… do release notes," and if feedback fails QC you "have to do that loop again."
- **Factory metaphors mapped onto software:** custom order → own station; build → assembly line; prove → quality control; ship → out the door. The speaker agrees: "my names are terrible… that's exactly how this works."
- **A software factory is literally markdown files.** "A software factory is not a product. It's not a special harness… a software factory is literally just a bunch of markdown files." Some startups are now "an agent with a couple markdown files."
- **Explicitly not about models or compute.** "We didn't talk about model. We didn't talk about hardness. It's all workflows, skills, and a little bit of domain knowledge."
- **Acknowledges this is one person's workflow.** "Not everybody works the same. This is how I work… but I found great results with this."
- **Sponsor segment (Brex, `brex.com/solutions/startups`):** high-limit cards, banking, and AI that handles back-office busywork like expense reports; described as built for the "agentic world"; the guest says his company has been on it a year and a half.

## Technical Details

- **Concept vocabulary**
  - Software factory: workflow + skills + domain knowledge encoded in markdown files, independent of model or harness.
  - Harness: the agent tool/UI — Codex, Claude Code, Cursor (Cursor Cloud agents shown in the PR demo).
  - Skill: a discrete instruction document the agent loads and cites during work.
- **`agents.md`** — one markdown file, appended to the agent chat on every message (explicitly *not* the system prompt). Its job: dictate how the agent should behave, especially for processes not native to the agent.
- **Isolate mechanics**
  - Fresh Git worktree per feature, branched from `origin main`.
  - Never build on `main`; merge back when done; worktree deleted after merge.
  - Described as "a work tree in isolated environment" — each agent gets its own station.
  - Merge conflicts avoided because each agent works on its own copy of the app.
- **Build mechanics** — service layer architecture, chosen for human readability and for agent re-readability across sessions/agents without codebase context.
- **Proof mechanics**
  - `evidence-driven testing`: capture before (pre-change state or the bug occurring), capture after (working state); media can be video or screenshots.
  - `before and after`: same before/after contract when the local machine can't record; states attached to the PR.
  - Non-visual proof: agent writes tests and returns results as measured numbers.
  - Quality-control framing: "does it turn on? Does it fit? Does it break under pressure?"
- **Ship mechanics** — third-party code review agent returns findings plus a confidence score out of five plus unresolved comments; loop continues until 5/5, each iteration attributed in the PR. Large diffs (10,000+ lines) auto-activate the Grep Loop skill; smaller diffs are handled by the agent directly.
- **Model references in the episode**
  - **GPT-6 Astra** — a big capability leap; least hallucinating model; most powerful "workhorse" and favorite.
  - **Fable** — among the first to write code better than the best engineers he's seen; also the harshest reviewer.
  - **GPT-5.6** — produces working, "all right" code; blamed for the 850 ms page load.
- **Named artifacts / identifiers**
  - `agents.md`, `origin main`, Git worktrees, PRs
  - Skills: `new feature`, `code structure`, `evidence-driven testing`, `before and after`, `Grep Loop`
  - Tools/services: Greptile, Macroscope, CodeRabbit, Cursor Cloud agents, Codex, Claude Code, Cursor, Vercel
  - Sponsor URL: `brex.com/solutions/startups`
- **Trade-offs stated**
  - Speed + structure vs. conversational back-and-forth: ad-hoc prompting traded for standardized, repeatable steps.
  - More moving parts (5–6 files to maintain) vs. slop and clobbered agents.
  - Code review automation costs third-party service usage, deemed worth it for user-facing software.
  - Proof artifacts cost time/screenshots/video per PR in exchange for trust without reading code.
  - Merge, deploy, release notes, and feedback remain human even after a 5/5 gate.
- **Verbatim skill text**

```
Every new feature starts in a fresh Git work tree branched from origin main,
so agents can work in parallel without conflicts. Never build on main.
```

- **No code, commands, flags, or config files were shown** — the workflow is described in prose and referenced as markdown files plus a slide deck the host offers to rename for the user.

## Questions

- The transcript cuts off mid-sentence at the crucial part of step four: "when it doesn't [have a visible surface], it'll give you nu—" — the fallback evidence for non-visual, non-measurable changes is unknown.
- Only one skill's text is quoted verbatim. The contents of `code structure`, `evidence-driven testing`, `before and after`, and `Grep Loop` are described but never shown.
- The guest says the factory is "five or six files" but only `agents.md` and five skills are identified — unclear whether that accounts for all of them.
- Naming is garbled by transcription: "I brought on Ross Mike," "Michael is on Greg's channel," "a name of it very soon." The guest's actual name, and whether "Bezel" is a real app name, are unconfirmed.
- Model names are taken as-is with no context: GPT-6 Astra, GPT-5.6, and Fable are never explained or linked.
- The performance improvement reads as "850 milliseconds" → "60. 817 61" — the exact final number and the measurement method (which tool, which page) are unclear.
- How does the agent actually capture video/screenshots — a specific tool (Cursor Cloud agents, a browser recorder)? Not stated.
- How is the "wait for a new score" mechanism implemented — polling PR status, a webhook, a CI check, or the agent blocking on the review service?
- How is the agent prevented from gaming or self-marking the prove step, given that build and self-proof run in the same loop?
- What happens on merge when two worktrees genuinely touch the same file, across 15 simultaneous feature worktrees? Conflicts are asserted to be avoided; the resolution/merge-queue strategy isn't covered.
- What does a Greptile confidence score of 3/5 or 4/5 mean numerically, what threshold stops the loop, and is there an iteration cap before escalating to a human?
- How does the external reviewer distinguish an agent's PR from a human PR, and what are the failure modes when the reviewer is wrong or 5/5 is reached with real problems still present?
- What "Grep loop ops" (mentioned alongside "Grep loop") actually does differently — a second skill for the large-diff case?
- Were all 15 parallel features green at 5/5 at merge time, or were some shipped below it?
- What does `before and after` do when the machine genuinely can't produce either state (e.g. backend-only changes)? Described but mechanics skipped.
- Cleanup of worktrees is mentioned as existing but explicitly not covered.
- Cost: no figures for Greptile or for agent/token usage at factory scale.
- Part 2 of the transcript is not included, so anything after the `Grep Loop` description — final steps, more examples, the skill download — is unknown. The episode ends with the speaker asking viewers what he needs to "further explain or add on."
<!-- yt-brain:related -->

## Related

- [[youtube/YouTube Knowledge Base|◻️ YouTube Knowledge Base]]
- [[youtube/dev-craft|📁 Software Engineering Craft]]
- [[index|🏛️ JARVIS Memory Vault]]

### Related notes

- [[youtube/agents/2026-10-03-how-to-build-an-agentic-software-factory|How to build an Agentic Software Factory]] · relevance 0.13
- [[youtube/agents/2026-10-03-ai-software-factories-are-the-next-big-thing-and-i-m-buildin|AI Software Factories Are the Next Big Thing (And I'm Building You One)]] · relevance 0.13
- [[youtube/agents/2026-09-29-hermes-paperclip-ai-litellm-how-to-build-an-ai-product-studi|Hermes + Paperclip AI + LiteLLM: How to Build an AI Product Studio]] · relevance 0.10
- [[youtube/agents/2026-10-03-agentic-engineering-graphs-workflows-verifiable-coding-agent|Agentic engineering: Graphs, workflows, verifiable coding agent runtimes, and staying in control]] · relevance 0.10

<!-- /yt-brain:related -->
