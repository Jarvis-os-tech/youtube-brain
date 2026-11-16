---
video_id: qLfSDQ5NGh0
title: "He Finally 10x Claude Code With This Method"
url: https://www.youtube.com/watch?v=qLfSDQ5NGh0&t=449s
watched: 2026-10-03 11:41
source: chrome:Default
indexed: 2026-10-03T12:29:32+00:00
topic: agents
type: youtube-note
source_url: https://www.youtube.com/watch?v=qLfSDQ5NGh0&t=449s
tags: [youtube, youtube/agents]
---



## Core Concept

The video adapts Andre Karpathy's Auto Researcher loop — a structure where an agent runs many scored experiments, keeping changes that improve a score and reverting ones that don't — into a Claude Code setup for building app features. The team's contribution is a second, nested loop (`auto loop`) that reads the first loop's results, detects recurring agent mistakes, and rewrites the "how to work" section of `program.md` so habits learned in one run carry into the next, while checks stay locked and unmodifiable by both loops.

## Key Takeaways

- **Origin:** Karpathy's `Auto Researcher` let an agent train a model in a loop; he wrote the instructions file in plain English and let it run for **2 days**, producing **700 experiments** and **20 changes** that made the model train faster.
- **Three-file discipline in Auto Researcher:** the agent could edit only the training file, a second file scored the model (kept if better, undone if same/worse), and the agent was forbidden from touching the scoring file — otherwise it could make the score easier to beat instead of improving the model. A third file, `program.md`, told the agent how to run each round.
- **Proof point:** the CEO of Shopify ran the same kind of loop on one of his own models while asleep — **37 experiments** overnight, model performing **19% better** the next morning.
- **Four conditions before building a loop:** you repeat the task often; your usage limit can absorb it (a long loop on a **$20 plan** hits limits mid-task, and failed rounds still consume tokens); the work can be checked by something producing a clear score; and the agent can actually run what it built and see what breaks.
- **Scope rule:** loops are used for **one feature at a time** or a simple version of the app that loop checks can verify — never "a full app built in one loop and call it done."
- **Three skills built:** `project context` (memory bank of app behavior, pages, conventions, things to avoid — used as a skill because only the skill's short description stays in context, so the agent always knows it's available but loads full details on demand), `build` (drives the loop), and `write checks` (project-specific, related to their earlier "test author" agent).
- **Anti-gaming lock-in chain:** you review the plain-language check list → the `approve checks` program moves checks into a **locked folder** → a rule in Claude Code settings blocks the agent from editing that folder → the build skill **commits** the approved checks as an extra layer.
- **Isolation:** the build skill never builds features in its own context window; each feature goes to a **feature builder agent** that starts fresh, with every round's result stored in a file.
- **First live run:** a half-built app, feature = guests ordering food for pickup from the restaurant's website. Claude added it to the tracking file `features.md` and wrote online-ordering rules there. Checks started at **10**; the team asked for a guest email check → **11 checks**, including that the email is a real address. Feature builder took **~6 minutes**; all **11 checks passed in the first round**, so no second round was needed.
- **Blind spot the score didn't show:** the checks only tested ordering rules, so the loop had written the rules but not the order form guests actually use. The loop built the form and wired it to the rules before marking the feature done.
- **The core problem:** an agent improves within a loop but doesn't remember the lesson next run — every feature starts with a fresh feature builder and the same instruction files, so mistakes carry over.
- **The fix:** a second loop reads the first loop's `results file` (which records each round's kept/undone status, what the agent tried, and which checks failed), writes down each recurring habit along with the rounds that show it, and rewrites the "how to work" part of `program.md` — where Karpathy's version had a human write that file.
- **Hard constraint:** the auto loop cannot edit the checks, or it could make them easier to pass and rounds would stop failing without the habits actually being fixed.
- **Test run (project management app, no way to combine/share workflows):** first feature, a shared database, passed all **10 checks** — but the app never saved anything to it. Auto loop added habit #1: **connect each feature to the app in the same round that makes its checks pass**.
- **Second habit:** mentions (`@name` task assignment) passed its checks, but an older part of the app still parsed `@` the old way. Habit #2: **find every place the app already does a job and make each one follow the new rules**. Both habits worked — subsequent features arrived with screens already connected.
- **Undo demonstrated:** the builder got two rounds of shared projects wrong. Round 1 broke mentions → mentions failed → round undone. Round 2 estimated each person's share the naive way, so **3 people got 33 each = 99** → check failed. Round 3 fixed it and passed all **10 checks**. The final report states where the agent went wrong, how it was fixed, and what the workflow looked like.
- **Auto loop vs build skill:** build runs a single pass with identical instructions every feature; auto loop runs the same loop (same feature builder agent, same `write checks` skill) nested inside another loop, one feature at a time, reviewing and updating instructions after each.
- Skills are available through their community product, AI Labs Pro; Upstash Box is the sponsor (per-agent cloud sandboxes, used for 10 agents, scales to zero).

## Technical Details

- **Loop criteria checklist (from the video):** repeated task + enough usage limit + externally checkable clear score + agent can run its own output and observe failures.
- **Token cost model:** every round re-reads the project and attempts a new fix, so failed rounds are still billed.

  ```
  round N:
    read project context
    propose one change
    run app / execute code
    score via locked checks
    keep if score improved, else revert
  ```

- **Skill/agent separation rationale:** using a *skill* rather than plain files for project context means only the short description is permanently resident in context; full content loads on demand.
- **Three files in the original Auto Researcher pattern:** editable training file, immutable scoring file, and `program.md` as the plain-English per-round instruction file.
- **In the team's setup, `program.md` carries two distinct parts:** the fixed rules and the "how to work" section. The "how to work" part is the auto loop's mutable target; the rules are not.
- **Files and paths named in the transcript:**

  ```
  program.md      — loop instructions: fixed rules + "how to work" section
  features.md     — feature tracking; loop-written rules for each feature
  results file    — every round: kept/undone, what was tried, failing checks
  locked folder   — approved checks live here; settings rule blocks edits
  ```

- **Check-locking pipeline, in order:**

  ```
  write checks → human reviews plain-language list → approve checks
  → move into locked folder → build skill commits them → loop runs
  ```

- **Skills and agents in the system:** `project context`, `write checks`, `build` (one pass, single-feature isolation), `approve checks` (small program), `feature builder agent` (fresh context each feature), `auto loop` (nested loop that rewrites `how to work`).
- **Trade-off:** instruction files drift from the agent's actual behavior across runs without the auto loop; the auto loop adds instruction churn that may over- or under-fit to recent history — the transcript does not evaluate this.
- **Trade-off:** the loops guard against the agent gaming its own score, but the checks can still be incomplete (the order-form gap) — the loop only patches what it happens to notice.
- **Claude Code settings rule** is the enforcement mechanism for the locked checks folder; the commit of approved checks acts as a second, recoverable barrier.

## Questions

- What exact Claude Code settings rule blocks edits to the locked checks folder, and is it a permissions deny entry, a hook, or something else?
- What file extension and schema does the `results file` use, and does the auto loop read it across separate Claude Code sessions or within one?
- How does the auto loop avoid instruction drift or overfitting — e.g., is there a cap on habits, or a way to retire a habit that stops being relevant?
- What is the mechanism that made the loop notice the missing order form, given the checks all passed? Is it a rule in `program.md`, a static review step, or something else?
- How long did the auto loop test run take in total, and what were the token costs of the nested loop versus a single build pass?
- How does the 6-minute build time and11-check pass rate compare across more features, and what happens when a feature fails repeatedly — is there a retry or escalation limit?
- The Shopify CEO's loop (37 experiments, 19% better) is cited second-hand; no primary source or exact setup is given.
<!-- yt-brain:related -->

## Related

- [[youtube/YouTube Knowledge Base|◻️ YouTube Knowledge Base]]
- [[youtube/agents|📁 AI Agents & Orchestration]]
- [[index|🏛️ JARVIS Memory Vault]]

### Related notes

- [[youtube/dev-craft/2026-10-03-building-a-software-factory-that-actually-works-full-course|Building a Software Factory that actually works (Full Course)]] · relevance 0.09
- [[youtube/agents/2026-09-29-claude-code-multi-agent-orchestration-with-opus-4-6-tmux-and|Claude Code Multi-Agent Orchestration with Opus 4.6, Tmux and Agent Sandboxes]] · relevance 0.08
- [[youtube/agents/2026-10-08-andrej-karpathy-from-vibe-coding-to-agentic-engineering-w-st|Andrej Karpathy: From Vibe Coding to Agentic Engineering w/ Stephanie Zhan]] · relevance 0.08
- [[youtube/llm-core/2026-10-03-deepseek-has-rsi-now|DeepSeek Has RSI Now]] · relevance 0.08

<!-- /yt-brain:related -->
