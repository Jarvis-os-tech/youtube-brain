## Overview

- **164 videos** total; **49** are AI/non-AI classified (**23 AI, 26 non-AI**), leaving **115 unclassified (70.1%)**.
- **140/164 (85.4%)** have transcripts; **24 (14.6%)** do not.
- Only **12/140 transcribed videos (8.6%)** were summarized, and **11** became classified notes.
- Artifact drift is severe: state references **12 note files** and **11 classified JSON files**, but only **2 of each** still exist on disk.
- A separate legacy `kb/` tree retains **60 markdown notes** (59 indexed), including at least one truncated note and uneven metadata.

## AI vs Non-AI Breakdown

- **AI: 23 videos (14.0%)** — agents, RAG, MCP/FastMCP, Ollama/Gemma, Claude/Jarvis, structured outputs, reasoning, vision, and AI productivity/OS workflows. **21 have transcripts**; only **2** are summarized/classified.
- **Non-AI: 26 videos (15.9%)** — mostly Telugu DSA/algorithms coursework (B-trees, AVL, knapsack, greedy, backtracking, Floyd-Warshall, branch-and-bound), plus memory/architecture, digital electronics, Hyprland/Linux, design, and Ghostfolio. **16 have transcripts**; **10** are summarized and **9** classified.
- Among classified videos, the split is roughly balanced (**2 AI / 9 non-AI**).
- Classification noise exists: a portfolio-website tutorial is tagged AI, and titles include `untitled` / `YouTube`; many clearly AI-relevant videos remain unclassified.

## Coverage & Gaps

- **115/164 videos (70.1%)** have no AI/non-AI classification.
- **24 videos (14.6%)** lack transcripts: 18 language mismatches, 3 disabled, 1 unplayable/removed, 1 unavailable, 1 connection error.
- Summary coverage is only **12/140 (8.6%)**, with AI coverage much worse (**2/23**).
- **21 of 23 AI videos** with transcripts still have no summary.
- State references are stale: **10/12 note files** and **9/11 classified JSON files** are missing.
- **11/12 summaries** were classified; one knapsack note failed classification.
- Legacy `kb/` contains about 60 notes covering many of the same videos, but they are not reconciled with current state.

## Quality Issues

- LLM backend exhaustion caused all **115 stage-1**, **128 summary**, and **1 classification** failures.
- State schema is inconsistent: `processed` has 115 entries vs `videos` has 164; `history_class` is `None` for 115; `note_class_status` is missing for 152.
- Artifact drift makes state references unreliable and prevents indexed notes from matching stored files.
- Only **2 stored notes** are directly reviewable on disk, both AI; their quality is high (complete sections, concrete steps, tools, details), but non-AI note quality cannot currently be verified.
- `kb/` metadata is uneven: two notes lack `video_id`, one note is truncated, and titles include `untitled` and `YouTube`.
- No integrity check currently guards counts or missing artifact paths before review.

## Recommended Follow-ups

1. Restore LLM access or reduce batch size, then rerun classification, summarization, and note classification for the 115 unclassified and 128 failed videos.
2. Reconcile state with disk and `kb/`: clear stale `note_path`/`classified_path` values or regenerate missing artifacts; validate/import the orphaned `kb` notes.
3. Add a pre-review integrity check for counts and missing artifact paths.
4. Retry transcripts for the 24 missing videos, prioritizing high-value AI content.
5. Enforce coursework exclusions before transcription, or add a dedicated study-material topic.
6. Fix poor metadata titles (`untitled`, `YouTube`) before further processing.
7. Prioritize summarizing the 21 AI videos that already have transcripts, then run `index.py rebuild` and republish.
