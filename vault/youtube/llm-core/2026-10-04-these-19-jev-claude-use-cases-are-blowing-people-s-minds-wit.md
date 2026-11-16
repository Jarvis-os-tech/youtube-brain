---
video_id: 3iDiWTt8lok
title: "These 19 Jev-Claude use cases are blowing people's minds (with prompts)"
url: https://www.youtube.com/watch?v=3iDiWTt8lok
watched: 2026-10-04 07:23
source: chrome:Default
indexed: 2026-10-04T02:34:20+00:00
topic: llm-core
type: youtube-note
source_url: https://www.youtube.com/watch?v=3iDiWTt8lok
tags: [youtube, youtube/llm-core]
---



## Core Concept

Jev is a **decision model** — it cannot write prose, but it picks one answer from a menu you supply (true/false, a category, a score) in a fraction of a second at a fraction of the cost, which the speaker frames as up to 200× faster and 400× cheaper than other models. The video's actual argument is architectural: point Jev at a pile of data or text you already have and let it *classify* rather than *generate*, so a large language model is only invoked for the small residue of cases that genuinely require writing. The 19 use cases are all instances of that one pattern, escalating from spreadsheet tagging to model routing, in-app search, and self-assembling web pages.

## Key Takeaways

- **Speed is most visible in a spreadsheet.** Because Jev can only choose from your list, "it never invents a category that you didn't ask for" — the closed answer set is the safety property, not a limitation.
- **Use case 1 — Google Sheets:** Claude builds a plugin; you type a new column name (e.g. `category`) and Jev fills every row while you watch.
- **Use case 2 — customer inquiry triage:** Jev as the decision layer instead of an LLM reading every message. Tags each inquiry (billing / bug / question) *and returns a confidence score*. Rule example given: **if Jev is less than 60% sure, route straight to a person**; adjust the threshold as you learn.
- **Benchmark cited:** 217 customer call transcripts sorted into categories in **13 seconds for 7 cents**.
- **Use case 3 — competitor ads:** The Meta Ad Library is the source; a Claude-built plugin or Chrome extension saves each ad, Jev tags format / call to action / funnel stage, results land in a database as a "swipe file."
- **Benchmark:** 54 ads across 3 brands tagged in **~1.5 seconds for less than a cent**.
- **Use case 4 — clipping:** Scored **411 possible clips from a 70-minute interview in 6.5 seconds**, then picked the top 10 worth posting. Record once, get a short list.
- **Use case 5 — customer scoring/profiling:** Read tenure, plan type, cancellation signals; bucket customers as healthy / needs attention / at risk of churn so you know who to contact *this week* rather than after they cancel.
- **Use case 6 — internal linking:** Same trick serves two purposes — cross-linking pages on a large site (navigation + a bit of SEO) and linking notes inside a "second brain" folder so agents can navigate it.
- **Benchmark:** 60 test blog posts linked in **2.5 seconds**.
- **Use case 7 — buyers in comments:** Scrape comments (Apify cited) → Jev tags ready-to-buy / question / complaint → produces a priority list.
- **Use case 8 — verification via validation set:** A few dozen to ~100 examples with known-correct or hand-sorted answers. Run Jev on that set *without showing it the answers*, count the matches, then inspect the errors to calibrate.
- **The stated pattern for use cases 1–8:** point Jev at a pile of stuff you already have and categorize it at lightning speed.
- **Use case 9 — skill selection:** With ~145 skills in the speaker's workspace, Jev found the right skills across 14 tests in **~5 seconds total**, versus **~30 seconds for Opus 5**. TypeSafe's own test with **182 skills** cut wrong picks by **more than half**.
- **Use case 10 — model routing:** A `/jv` command makes Jev read every message and pick the model in **~a third of a second** — e.g. a file-path request went to Haiku (cheapest) instead of Opus; hard jobs still escalate. Said to work in Codex and other agentic platforms too, not just Claude.
- **Use case 11 — Jev as a pre-filter for agents:** An email-handling agent otherwise pays a big model to read everything including spam.
- **Benchmark:** Jev sorted **1,700 emails for 18 cents**, tagging what needs a reply, what is a brand deal, what is spam/scam. Only the remainder reaches Claude, so both reads and token spend drop.
- **Use case 12 — Chrome extensions:** Cited example checks each post as it loads in the X feed and asks one question (AI slop or not); slop gets folded. Same trick applies to LinkedIn feeds. A second example: an extension named **Unclutter** that hides ads and cookie banners.
- **Use case 13 — search by meaning:** Replaces Ctrl+F exact-match. Splits the page into paragraphs, asks Jev which matches best, highlights and scrolls there. Described as fast enough to feel real-time; positioned as the cheapest possible upgrade to any existing search box.
- **Use case 14 — search images by content:** Typing `Claude` finds images *about* Claude, not just filenames containing it. Requires per-image metadata (the speaker logs the generation prompt); if you lack it, a small cheap model writes a caption — **Gemini Flash Lite** suggested, described as costing "about only 50" for 1,000 images.
- **Use case 15 — live checking:** Because latency is sub-second, Jev can classify text *as it is spoken*. Cited build: a live BS meter that scores every sentence of a debate. Meeting-plugin variant sorts each sentence as spoken into decisions / action items / risks / questions — useful for live sales-call recaps, interviews, podcasts.
- **Use case 16 — chatbot with zero LLM calls:** Narrow Q&A over a fixed dataset (pre-transcribed video list, or company documents). Jev answers in real time from a list of what each item is about. Framed as "sounds implausible" but works because the answer space is bounded.
- **Use case 17 — smarter app design:** Jev picks the icon as you type — a habit tracker turns "drink more water" into the water icon; a mood app picks a mood icon from your written day. Trade-off named: the prior options were a costly LLM, or a **regex-based** matching system that is "sometimes not as effective."
- **Use case 18 — self-assembling web pages:** Jev cannot write code but can select parts from a library of ready-made pieces (forms, buttons, sign-in boxes, fonts) and assemble the page per visitor on the fly, at roughly normal page-load speed.
- **Use case 19 — finding your own use cases:** **shipwithjv.com** lists use cases by category; paste it into Claude along with a file describing yourself and your business and ask which apply most. Second method: have Claude review past sessions and flag the steps where "a quick Jev call would have done the job."
- **Closing competitive note:** OpenAI launched a **decisions API** at its dev day — question plus list of allowed answers, picks one in **~150 ms** — read as their answer to Jev. The speaker's prediction: other labs (Anthropic named) will copy this shape.

## Technical Details

- **Model class:** decision model, not generative. Output is constrained to a supplied answer set → categorical, boolean, or score outputs.
- **Economics cited:** up to 200× faster, 400× cheaper than other models; per-task costs of 7¢ / 18¢ / <1¢; label inference at roughly a third of a second; OpenAI's competing endpoint at ~150 ms.
- **Architecture pattern:** Jev occupies the cheap deterministic-routing tier; an expensive LLM occupies the generative tier. The system only escalates on genuine generation work.
- **Confidence scores** are a first-class output and are the intended threshold-routing mechanism (60% example).
- **Closed-vocabulary guarantee** is the correctness argument for bulk tagging: no hallucinated categories.
- **Latency class enables new interaction models:** live sentence classification during speech is impossible with slower models, which is what makes the BS meter and meeting notes possible.
- **Validation / calibration loop:** hold out a labeled set → score without answers → count matches → inspect misclassifications → adjust. This is the transcript's answer to "how do I trust the categorization."
- **Metadata prerequisite** for image search: you need *some* text per image. Preferred source is the generation prompt log; fallback is a cheap captioning model.
- **Trade-offs named:**
  - Regex matching vs LLM vs Jev — regex is cheaper but less effective; an LLM is effective but costlier; Jev aims to be both.
  - LLM-generating-UI vs Jev-selecting-parts — Jev cannot author components, only compose from a library, so page assembly inherits the library's load speed.
  - Narrow-dataset chatbots only work when answers are bounded by a known corpus; this is the precondition for zero LLM calls.

Named entities as they appear in the transcript (note several are speech-to-text artifacts — "Clawed," "Jeff," "Entropic," "Codeex," "reject based matching," "animal plan," "Robberonuggets" — the intended referents are Claude, Jev, Anthropic, Codex, regex-based, annual plan, and the Robb AI Nuggets community):

```
/jv                     # the Claude command that enables Jev model routing
                       # Ctrl+F is the exact-match baseline being replaced
shipwithjv.com         # use cases listed by category
Meta Ad Library        # source of competitor ads
Apify                  # comment scraping tool
Gemini Flash Lite      # cheap captioner for image metadata
Unclutter              # Chrome extension hiding ads and cookie banners
Claude Code / Codex    # agentic platforms where skill + model routing applies
Robb AI Nuggets        # community; Claude Living Master Class; Agents as a Service course
```

## Questions

- The transcript announces "Here's a prompt to get you started" at use case 1 but never reads the prompt text. None of the 19 prompt bodies appear in the transcript — they are said to be in a free PDF guide linked in the description.
- Not stated anywhere: Jev's actual API surface, SDK, or how the speaker wires it into Claude Code, Chrome extensions, or Sheets. Every use case is described behaviorally.
- No pricing is given per token or per 1K classifications — only end-to-end task costs (7¢, 18¢, <1¢) with no item counts normalized, so unit economics can't be derived.
- The image-captioning cost is transcribed as "captioning a,000 images costs about only 50" with no currency symbol. Whether that is $0.50 or $50 is unresolved.
- Model names are unverified: "Opus 5," "haiku helper," "Gemini Flash Light" are as spoken. Version numbers and availability are not confirmed.
- The comparison is Jev vs Opus 5 at ~5s vs ~30s over 14 tests on 145 skills. No accuracy metric is given — speed is compared without stating how often each picked correctly, and Opus's wrong-pick rate is unknown.
- The TypeSafe test (182 skills, wrong picks cut by more than half) gives no baseline wrong-pick rate, so the absolute improvement is unclear.
- shipwithjv.com is named but never demonstrated; whether it is comprehensive or curated is unknown.
- No guidance on answer-menu size limits, how many classes Jev can choose between, or behavior when the correct answer is absent from the list — relevant to use cases 2, 5, and 16.
- No mention of latency under concurrency, rate limits, or the cost/latency of a Jev call in absolute terms — only ratios and task totals.
- The validation-set guidance (use case 8) gives no accuracy threshold that counts as good enough, nor a sample-size rationale beyond "a few dozen or hundred."
- The transcript does not address PII: use cases 5, 7, and 11 run customer data, emails, and comments through a model with no mention of redaction, retention, or consent.
- "Entropic 2" appears to mean Anthropic; no source is cited for the prediction that other labs will copy this.
- The demo chatbot (use case 16) is described with a pre-transcribed video list, but it's unstated whether Jev returns the video itself or only a yes/no match per candidate.
<!-- yt-brain:related -->

## Related

- [[youtube/YouTube Knowledge Base|◻️ YouTube Knowledge Base]]
- [[youtube/llm-core|📁 LLMs & Model Behaviour]]
- [[index|🏛️ JARVIS Memory Vault]]

### Related notes

- [[youtube/ml-training/2026-10-04-clef-open-source-decision-models-and-new-rl-fine-tuning-plat|Clef: Open-source decision models, and new RL fine-tuning platform]] · relevance 0.09
- [[youtube/llm-core/2026-10-04-nyu-proffesor-yann-lecun-explains-what-comes-after-llms|NYU Proffesor Yann LeCun Explains What Comes After LLMs]] · relevance 0.08
- [[youtube/linux-infra/2026-10-07-i-built-jarvis-in-omarchy|I BUILT JARVIS IN OMARCHY]] · relevance 0.08
- [[youtube/agents/2026-11-13-forget-prompting-this-is-how-a-10b-company-uses-ai-agents-wi|Forget Prompting. This Is How a $10B Company Uses AI Agents with Second Brain]] · relevance 0.07

<!-- /yt-brain:related -->
