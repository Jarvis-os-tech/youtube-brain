---
video_id: eSuMmMMMrm0
title: "CLIP… But For Decisions (Contrastive Language Models Explained)"
url: https://www.youtube.com/watch?v=eSuMmMMMrm0
watched: 2026-10-03 18:09
source: chrome:Default
indexed: 2026-10-04T00:00:47+00:00
topic: llm-core
type: youtube-note
source_url: https://www.youtube.com/watch?v=eSuMmMMMrm0
tags: [youtube, youtube/llm-core]
---



## Core Concept

Contrastive Language Models (CLM) apply CLIP's contrastive-embedding trick to decision-making instead of image/text matching: a **state encoder** embeds the current situation and an **action encoder** embeds each candidate action into the same space, so choosing an option becomes a nearest-neighbor lookup plus a softmax rather than a token-by-token generation. Because action embeddings are computed once and cached, latency stays nearly flat as the candidate list grows — but because the state never sees the options, accuracy collapses on large candidate sets.

## Key Takeaways

- **Context:** System One (fast, non-reasoning) models are hot again after Jev's release; most in-software decisions (next tool, ticket urgency, which link to click) need millisecond answers, not 30-second reasoning.
- **Most "Jev clones" are still LLMs** — they read the text, read every option, and write an answer (even a single word with probability).
- **CLM comes from Stanford + NVIDIA Research**, an8B-parameter model, claimed **up to 9x faster than Jev at on-par accuracy**.
- Speed does **not** come from a smaller model — it comes from architecture: **state encoder + action encoder** (the "CLIP but for decisions" mental model), softmax over similarity scores → probability per action.
- It exposes the **same Jev API** with three primitives — yes/no, multi-choice, score — all of which reduce to *state + closed candidate list* (yes/no = two candidates, `true`/`false`).
- **Contrastive training trick:** no one writes wrong answers. Grab 1,000 examples at once; for one situation, the other 999 actions are automatically negatives ("negatives for free").
- **Latency math:** Jev-style calls re-read state + all options every call and decode token by token — constrained decoding with a 238B model climbs **over 4 seconds**. CLM embeds actions once, caches them, and each new step costs one state embedding + a dot product ("essentially free"). Mario demo: **5 forward passes → 1**.
- **Chart numbers:** as candidates go 1 → 1,024, CLM's line barely moves. At ~1,024 options: **44 ms vs 570 ms for Jev ≈ 13x faster**.
- **The catch:** the state is encoded alone, so it never sees options side by side; every option is judged in isolation. Accuracy does not scale like latency does.
- **Plain embeddings ≠ right answers:** asking raw Qwen embeddings "who wrote Romeo and Juliet" puts **William Shakespeare third**; after CLM training he comes **first**. Same encoder, same candidates — only the ~20M-parameter head differs. In the demo, raw Qwen puts **Christopher Marlowe first, Shakespeare second**; with CLM, **Shakespeare jumps to 98%**.
- **Three-stage training:** (1) **60M QA pairs** from NVIDIA NeMoTron data (question = state, answer = action) for world knowledge; (2) **30M Gemini-generated hard negatives** ("close but wrong" — e.g. Venus instead of Mercury for the planet closest to the sun); (3) **~1M steps of real agent trajectories** ("here's my context, here's what I did") with **40% of the original QA data mixed back in**.
- **Order matters:** on a hard-negative test, pre-training alone = **52%**; adding the hard-negative stage = **69%**; training on hard negatives from day one peaks at **62%** then overfits. Without the 40% replay in stage 3, hard-negative scores fall **69 → 56**.
- **Frozen backbone:** the 8B model is frozen and used only as a reader/encoder; **the only trainable parts are small heads (~20M parameters) on each side**. So you embed the dataset once, then a full pre-training run takes **~1 hour on a single RTX 4090**.
- **Scaling law:** loss follows a power law in compute, data, head size, and encoder size — and **encoder size gives the biggest gains of the four**, implying a bigger backbone is the obvious next step.
- **Demo hardware:** everything ran on a **DGX Spark** with the **Qwen 3 8B encoder served through vLLM** plus the team's released **CLM server** (~**75 MB** server, **~25 GB** total memory).
- **Support-ticket demo:** state = customer charged twice, can't reach anyone; three typed questions in one call — *Is this urgent?* **84%**, *Which team?* **Billing 99%**, *How frustrated?* **very angry**. Re-asking the same ticket returns in **under 2 ms** because everything is cached.
- **1,080-tool demo:** tool list (Stripe, Twilio, QuickBooks, …). Jev caps a choice at **255 options**, so this wouldn't fit a single Jev call. First request takes a few seconds (embedding every tool), then **~80 ms** per request, and picking from 1 tool vs 1,000 costs about the same once cached.
- **Wiki Racing rebuild** (not released by the team, rebuilt by the presenter): Plate Tectonics → Bioluminescence; **934 links on the first page scored in one go**; it picked Biosphere → Biome → Plant con…, where bioluminescence ranked first at **58%**; finished in **~4 clicks vs ~6** reported in the team's own demo.
- **Accuracy reality check:** **8 tools → 86% correct; all 1,080 tools → 17%**, mostly confusing similar-sounding tools (several different "refund" tools). The same pattern showed in Wiki Racing — some races nailed, others wandered off.
- **Recommended usage pattern today:** CLM as a **first stage** — cut 1,000 tools/candidates down to **top 10 in milliseconds**, then let a model that reads the options *together* make the final call. Fast thinking produces the shortlist; System Two makes the careful decision. Works well when the action set is already small and stable (game loop, a handful of routes). The presenter also suggests **sub-agents with separate tool sets** rather than 1,000 tools for one agent.
- **Roadmap:** current version is text-only; a **35B-parameter multimodal** model is coming, and a multimodal CLM is expected **early next month**.
- **Closing thesis:** older algorithms are making a comeback — contrastive learning was hot in **2017-2018**, and System One models are bringing it back, because existing algorithms aren't fully pushed.

## Technical Details

- **Dual-encoder architecture (CLIP analogy):** CLIP embeds images and text into one space so "a photo of a dog" lands next to that phrase; CLM embeds **situations** and **actions** into one space. Scoring = dot product / closeness between state embedding and each action embedding; a **softmax** turns scores into per-action probabilities (example: jump 80%, right 15%, left 5%).
- **Three primitives, one mechanism:** yes/no, multi-choice, and score are all *state + closed candidate list*. Constraint: it can never invent an answer off the list, but it can pick the wrong one from the list — and do so confidently.
- **Caching asymmetry:** in most agent loops actions don't change step to step, only state does → embed actions once, cache, then per step: 1 state embedding + N dot products.
- **Scaling-law knobs:** compute, data, head size, encoder size — encoder size dominates. Frozen backbone means the dataset is embedded once and only ~20M-param heads are trained.
- **Failure mechanism (architectural, not a bug):** independent per-option encoding removes any side-by-side comparison, so it lacks contrast *within* the candidate list — the exact thing it learned during contrastive training.
- **Reported benchmark numbers:**
  - constrained decoding, 238B model: **>4 s**
  - 1,024 options: **44 ms (CLM) vs 570 ms (Jev)** ≈ **13x**
  - Mario demo: **5 forward passes → 1**
  - hard-negative test: pretrain **52%** → +hard negatives **69%**; from-day-one hard negatives **62%** peak then overfit; no replay in stage 3: **69% → 56%**
  - accuracy vs candidate count: **8 tools 86%**, **1,080 tools 17%**
  - memory: CLM server **~75 MB**, total stack **~25 GB**
  - training cost: **~1 hour on one RTX 4090**
  - Jev option cap: **255**
- **Stack named:** DGX Spark, Qwen 3 8B encoder, vLLM serving, NVIDIA NeMoTron data, Gemini for hard-negative generation, RTX 4090, embedding cache, softmax over similarity scores, contrastive loss with in-batch negatives.

## Questions

- The model claims "up to 9x faster than Jev" but the chart shows ~13x at 1,024 options (44 ms vs 570 ms) — which configurations were used for each number?
- "On par accuracy" with Jev — at what candidate count, and on which benchmark? The video deliberately avoids a head-to-head.
- What exactly is the reported accuracy benchmark, and does the 17% @1,080-tools result hold outside the presenter's own tool list?
- Are the two heads ~20M params *each* or 20M total, and what is the total trainable footprint?
- The transcript says the frozen backbone "gets a single gradient" — unclear phrasing; what is the actual training procedure for the heads?
- How are cached action embeddings invalidated when the tool/action list changes, and what is the cost of a cold cache in a live agent loop?
- Since the state never sees the options, how does CLM behave when the state text is ambiguous or when two options are near-duplicates (the "several refund tools" failure)?
- Is the softmax temperature / score scaling specified, and are the probabilities calibrated?
- Does the text-only8B model's contrastive training transfer to non-QA agentic states, or does it degrade outside the training distribution?
- Timeline and availability for the 35B multimodal model and the "early next month" multimodal CLM; will the35B version also use a frozen backbone?
- What serving overhead does the ~25 GB footprint become at 35B, and can it still run on a DGX Spark?
- No published Wiki Racing code — the presenter rebuilt it; unclear how close that reimplementation is to the team's evaluation harness.
<!-- yt-brain:related -->

## Related

- [[youtube/YouTube Knowledge Base|◻️ YouTube Knowledge Base]]
- [[youtube/llm-core|📁 LLMs & Model Behaviour]]
- [[index|🏛️ JARVIS Memory Vault]]

### Related notes

- [[youtube/llm-core/2026-10-04-nyu-proffesor-yann-lecun-explains-what-comes-after-llms|NYU Proffesor Yann LeCun Explains What Comes After LLMs]] · relevance 0.14
- [[youtube/ml-training/2026-10-04-clef-open-source-decision-models-and-new-rl-fine-tuning-plat|Clef: Open-source decision models, and new RL fine-tuning platform]] · relevance 0.06
- [[youtube/llm-core/2026-11-13-tiny-local-ai-that-sees-hears-and-talks-back|Tiny Local AI That Sees, Hears And Talks Back]] · relevance 0.06
- [[youtube/llm-core/2026-10-04-these-19-jev-claude-use-cases-are-blowing-people-s-minds-wit|These 19 Jev-Claude use cases are blowing people's minds (with prompts)]] · relevance 0.06

<!-- /yt-brain:related -->
