---
video_id: xzuzf9TH1OA
title: "Clef: Open-source decision models, and new RL fine-tuning platform"
url: https://www.youtube.com/watch?v=xzuzf9TH1OA
watched: 2026-10-04 06:55
source: chrome:Default
indexed: 2026-10-04T02:35:25+00:00
topic: ml-training
---


## Core Concept

Cloudflare released two open-source decision models — **Cleft** and **Cleft Flash** — on Workers AI: unlike autoregressive LLMs they return a typed, probability-scored answer against a user-defined schema instead of free-form text, and by skipping the decode phase entirely they run at a median **38.8 ms** (Flash) to **209.3 ms** (Cleft), far faster than Typesafe AI's Jev at **524.1 ms**. The same post introduces **RLCD** (reinforcement learning for calibrated decisions) and a five-stage fine-tuning pipeline built on AI Gateway, Workers, Containers, a new `trainer` component, and Workers AI with BYO model redeploy (COD), with self-serve train-and-redeploy coming later.

## Key Takeaways

- Source: Cloudflare blog post by Michelle Chen, Alex Renault, and Kevin Flansberg, tagged AI birthday week / developers / machine learning / open-source / Workers AI, listed as a 10-minute read; released October 1, 2026.
- **Latency table (median ms):** Cleft 209.3, Cleft Flash 38.8, Jev 524.1, Diffusion Gemma Jev 84.4, KV 9B 51.4, LIA 5.8.
- **P95 (ms):** Cleft 238.6, Cleft Flash 122.4, Jev 536.0, Diffusion Gemma Jev 211.2, KV 9B 187.9, LIA 222.5.
- Cleft's P95 is only ~29 ms above its median — a tight, predictable band. Cleft Flash goes 38.8 → 122.4 (~3×) but worst case stays under an eighth of a second.
- LIA has the fastest median (5.8 ms) and the second-widest P95 (222.5 ms) — fast median, unstable tail.
- 38.8 ms vs 524.1 ms is roughly **13×**. Cloudflare ran all models itself on its own infrastructure; competing models' serving conditions are unspecified in the post.
- Budget math: an agent hot path affords ~1–2 half-second routing decisions before lag is noticeable; at 38.8 ms you can afford ~10 and stay under half a second.
- **Not trained from scratch.** Base model is **Qwen** (transcribed "QN"); post-trained for decision use with **Qwen3-32B frozen** for Cleft and **Qwen3-8B (transcribed "QN35-9B")** for Cleft Flash. Frozen = backbone weights do not move.
- Training jointly optimized a **routing head** alongside **rank-256 LoRA adapters** — small extra params on a static model.
- **Inference mechanism (the clever part):** prefill-only pass, then all valid schema choices scored **in parallel**. Cleft skips decode entirely; the decision step is non-autoregressive, so there is no token-by-token intermediate text. Autoregressive = one-lane queue; parallel scoring = grid, all options graded at once.
- Architecture described as "a two-stage attention routing process combining option-specific evidence routing, joint cross-field attention, and schema-bound scoring with a lexical prior" — **prose only**, no paper, no ablations, no reproducible detail.
- **Calibration:** label-smoothed cross-entropy for schema validity + **Brier loss** for probability calibration, on internal synthetic datasets that permute field orders, prompts, and schema structures. Cross-entropy picks the right answer; Brier teaches honesty about confidence (95% should be right ~95/100).
- **RLCD** (reinforcement learning for calibrated decisions), a secondary optimization target, with three behaviors: partial credit for adjacent ordinal choices, reward for fully precise outputs, and a reference penalty against distribution shift.
- Partial credit example: true severity "major" vs predicted "critical" is a near miss, not a coin flip — training it that way produces confidence curves that make sense.
- **43 eval benchmarks total.** BFCL case exact: Cleft 98.47, Cleft Flash 98.76, Jev 95.75. Tool NDCG@10: Cleft 69.19, Flash 66.43, Jev 65.28. API-Bank accuracy: Cleft 91.93, Flash 93.11, Jev 88.19.
- Widest gap is classification: Home Appliances case exact — Cleft 82.95, Cleft Flash 97.73, Jev 52.27, Diffusion Gemma Jev 42.05, KV 9B 25.00, LIA 0.0. 52.27 → 97.73 moves from "must double-check" to "can route on."
- Banking77 macro-F1: Cleft 94.20, Cleft Flash 90.93, Jev 79.74. CLINC50+OS macro-F1: Cleft 97.43, Cleft Flash 66.77, Jev 89.27 — the small model drops hard here while the large model takes top score.
- Cloudflare published the losses too: Jev leads "when to call" accuracy 80.97 vs Cleft 72.37, and Bright NDCG@10 47.52 vs 45.91. Diffusion Gemma leads "fish and chips" accuracy 85.35 vs Cleft 79.60 (Typesafe's own eval suite).
- On Typesafe's suite, Cloudflare claims Cleft won 3 of 4 areas: invoice processing 64.7 vs 61.8, customer service 76.3 vs 76.0, security incidents 62.9 vs 61.7; Jev led agent trace observability 71.6 vs 68.5.
- Cleft is claimed leader on the **Jev Decision Index** — but that index is competitor-defined and was run by Cloudflare on Cloudflare's own demo site, so treat as vendor claim.
- **Drop-in spec lines:** 64K context window vs Jev's 32K (double), plus a **vision encoder** (image classification) where the post says Jev is text-only today. Combined with full Jev API compatibility, swapping is a configuration change.
- API shape: one HTTP POST to `api.cloudflare.com/client/v4/accounts/{account_id}/run/@cf/cloudflare/cleft` with a bearer token; body has `state` plus `questions`.
- Question types shown: `null`, `choice` with named criteria, and `score` with an **ordered** criteria list (e.g. no impact, minor, major, critical). That ordered list is exactly what RLCD's partial credit is built around — schema and training objective are the same idea from two sides.
- **Internal test:** Cloudflare's threat intel team used Cleft for website domain classification in a "browser run" workflow. Cleft took 2.2 s to fetch, render, and classify a page and returned 4 classifications; GPT-oss-120B (transcribed "GPT- O120B", described as Cloudflare's fastest general LLM) took 4.7 s and returned only two. GPT-oss-120B is OpenAI's open-weight 2025 model, hence the in-house baseline.
- Caveat stated in transcript: one internal workflow test, not a reproducible benchmark; the 2.2 vs 4.7 s includes fetch+render, not just model time; Cloudflare's "roughly 2× in both latency and results" blends speed with classification count. Most of the 2.2 s is the browser, not the model — that's what a 209.3 ms decision step buys.
- Domain classification example from the post: one domain scored 95% fashion website, 85% e-commerce, under 1% phishing — three fields, three probabilities, one call.
- **Five-component RL/fine-tuning pipeline:** AI Gateway (capture dataset from real traffic) → Workers AI (generate rollouts against base Cleft) → Cloudflare Containers (RL sandbox, scoring and replaying agent actions) → new **`trainer`** component (weight updates) → Workers AI + BYO model redeploy.
- BYO-model work is labeled **COD**, said to have progressed since Cloudflare's acquisition of **Replicate** (COD = the model packaging tooling that came with it).
- Three named internal targets: evaluating trust-and-safety submissions, triaging Cloudflare support requests, and deciding in bot products whether a crawler is a good bot or a bad bot. Cites **15+ years of network data** across domains as fine-tuning material.
- Stated trade-off, quoted as honest: fine-tuning may give up some general-purpose performance for higher accuracy in one domain. The claim that a fine-tuned Cleft is more accurate/faster than the generic model has **no supporting numbers yet**.
- Prior art credit: Cloudflare's earlier experiment adapted Diffusion Gemma to output deterministic probabilities by exposing LLM logprobs, and builds on independent research by **Matt Mrachet** (transcribed "Matt Mrachi"), who contributed ideas and PRs to **vLLM** (transcribed "VLM"), the dominant open-source serving engine.
- License: both models open-sourced on HuggingFace under **Apache 2.0** — commercial use, modification, and redistribution all allowed, so every table number is independently testable.
- Hosting on Workers AI, a platform Cloudflare has run since 2023, putting GPU inference across its global edge rather than a handful of regions — that geography is the entire basis of the latency argument.
- Policy line: models are enterprise-ready with a guarantee Cloudflare doesn't read, store, or train on requests/responses unless you use the fine-tuning product — a stated policy, not an external audit.
- Audience: anyone whose agent currently pays a reasoning model to write a paragraph before picking one of four labels — routing, triage, moderation, domain classification, severity scoring.
- Cleft is called Cloudflare's first Cloudflare-trained ML model from the Workers AI team, with the quote "we believe that Cleft has the ability to disrupt the way we use agents," fitting Cloudflare's "agent cloud" positioning. The 98.47 BFCL number is not.
- Name origin: in music theory a **clef** assigns pitch names to a staff — it tells you what the notes mean; CF = Cloudflare. Fits a model turning raw context into labeled, scored meaning.
- Rollout: hands-on with Cloudflare's forward-deployed engineer (FTE) team first, self-serve train-and-redeploy later; existing customers invited as design partners for the fine-tuning/RL work, so some answers come from that cohort first.

## Technical Details

- **What a decision model is:** returns a typed, probability-scored answer against a schema you define, versus an LLM's free-form paragraph. Shape of the output *is* the product.
- **Training stack:** Qwen base (Qwen3-32B frozen for Cleft; Qwen3-8B-class for Cleft Flash) + trainable routing head + **rank-256 LoRA adapters**.
- **Frozen backbone** = weights do not move; only the head and adapters learn. Cheap, small set of trainable parameters.
- **Prefill vs decode:** prefill is the phase where the model reads the input; decode is where it writes words one token at a time, each token waiting on the last. Cleft does prefill-only then parallel schema-choice scoring, so it never pays sequential decode latency.
- **Two-stage attention routing:** option-specific evidence routing → joint cross-field attention → schema-bound scoring with a lexical prior (prose description only).
- **Objective stack:** label-smoothed cross-entropy (schema validity) + Brier loss (probability calibration) + **RLCD** as secondary target.
- **RLCD mechanics:** partial credit for adjacent ordinal choices; reward for fully precise outputs; reference penalty to prevent distribution shift.
- **Brier score intuition:** a model claiming 95% should be correct ~95 times in 100 — otherwise threshold logic is built on sand.
- **Serving geometry trade-off:** LIA wins median (5.8 ms) but has the second-widest tail (222.5 ms P95); Cleft trades a higher median for the tightest median-to-P95 gap in the table (+29 ms). Median-only optimization hides tail risk.
- **API surface:** Jev API compatible, so migration is config not rewrite. 64K context vs Jev's 32K; vision encoder for image classification.
- **Inference cost model:** ~38.8 ms × N decisions fits inside a half-second agent hot path; ~524 ms × 1 barely fits, ×2 does not.

```bash
# HTTP request shape (endpoint + auth; account ID is a path segment)
POST api.cloudflare.com/client/v4/accounts/{account_id}/run/@cf/cloudflare/cleft
Authorization: Bearer <token>

# Request body: a `state` field plus `questions`
# Question types shown in the post:
#   null
#   choice  -> named criteria
#   score   -> ordered criteria list, e.g.
#             ["no impact", "minor", "major", "critical"]
```

```text
Median latency (ms)          P95 (ms)
Cleft                209.3    238.6
Cleft Flash           38.8    122.4
Jev                  524.1    536.0
Diffusion Gemma Jev    84.4    211.2
KV 9B                 51.4    187.9
LIA                    5.8    222.5
```

```text
Benchmark                     Cleft    Cleft Flash    Jev
BFCL case exact               98.47    98.76          95.75
Tool NDCG@10                  69.19    66.43          65.28
API-Bank accuracy             91.93    93.11          88.19
Home Appliances case exact    82.95    97.73          52.27
Banking77 macro-F1            94.20    90.93          79.74
CLINC50+OS macro-F1           97.43    66.77          89.27
```

```text
Fine-tuning / RL pipeline
1. AI Gateway              -> capture dataset from real traffic
2. Workers AI              -> generate rollouts against base Cleft
3. Cloudflare Containers   -> RL sandbox: score + replay agent actions
4. trainer (new component) -> weight updates
5. Workers AI + BYO model  -> redeploy  (COD, from the Replicate acquisition)
```

- **Broader trend:** small specialized classifiers replacing expensive general calls — a major network putting a calibrated, typed, API-compatible model in that slot with open weights.
- **Reproducibility asymmetry:** BFCL, API-Bank, Banking77, and CLINC50+OS are public benchmarks, so anyone with the HuggingFace weights can rerun them; the Jev Decision Index and Typesafe's suite results are not independently rerunnable from the post.

## Questions

- **Pricing** — no cost figure anywhere: not per request, per token, or per decision.
- Are both models generally available today, or is either behind a beta?
- **HuggingFace repo names, parameter counts, and local hardware requirements** are not published.
- Ship date or price for the self-serve platform and the new `trainer` component.
- Is vision actually live in the hosted API right now, and what are the image size/count/format limits?
- Rate limits, and the maximum number of questions per call.
- What is **browser run**, and can customers use it?
- Who owns the weights when Cloudflare's FTE team trains them for you?
- Why does Jev still lead on "when to call" (80.97 vs 72.37) and Bright NDCG@10 (47.52 vs 45.91) — is that a known class of task where Cleft is structurally weaker?
- Is there any paper, ablation, or reproducible architectural detail for the two-stage attention routing description beyond the prose?
- What supporting numbers exist for "a fine-tuned Cleft is more accurate and faster than the generic model"? None given yet.
- Which model to pick for a given task: Cleft Flash wins Home Appliances and API-Bank but collapses on CLINC50+OS (66.77) while Cleft takes top score (97.43) — is there published guidance?
- Under what serving conditions were the competing models (Jev, Diffusion Gemma Jev, KV 9B, LIA) run? Unspecified in the post.
