---
video_id: Pic4NLTjx6w
title: "Gemini 4 RSI Leak Destroys Astra and Fable in Benchmarks"
url: https://www.youtube.com/watch?v=Pic4NLTjx6w
watched: 2026-10-03 15:23
source: chrome:Default
indexed: 2026-10-03T12:17:25+00:00
topic: llm-core
type: youtube-note
source_url: https://www.youtube.com/watch?v=Pic4NLTjx6w
tags: [youtube, youtube/llm-core]
---



## Core Concept

A model aliasing itself as "Gemini 3.8 Flash" in the blind Arena leaderboard is believed by the community to actually be an unreleased flagship — nicknamed Gemini 4 — whose far higher benchmark scores, ~10x lower rumored price, 10M/256K context ceilings, and robot motor-control support suggest a deliberate camouflage rather than a real Flash-tier checkpoint, with the transcript arguing Google's need to replace the scrapped Gemini 3.5 Pro makes an RSI-driven capability jump and an imminent fall-event reveal the coherent explanation.

## Key Takeaways

- **The anomaly:** A model listed as "Gemini 3.8 Flash" on Arena went quiet ~10 minutes on a raw-SVG vector render of a PlayStation 5, then emitted thousands of lines of code capturing curves, shadows, and the optical-drive accent. The real Flash answers the same prompt in 10–15 seconds with approximate geometry.
- **Naming rationale:** "Gemini 3.8 Flash" is a real, public, documented, priced model shipped September 2nd, so reusing its name is camouflage, not stealth. Anonymity itself is normal on Arena — anonymous "Ox Alpha" hit the top three within 48 hours in mid-August and was never claimed.
- **Anatomy of the platform:** Arena came out of a UC Berkeley team in 2023; you chat with two unidentified models, vote, and labs get brand-blind data. Everyone, Google included, does anonymous release-candidate testing.
- **Spatial reasoning jumps:** Voxel pagodas and BMW M4 renders beat older Gemini checkpoints on lighting, depth, shading, and geometric alignment — "categorically better, not incrementally better." The classic pelican-riding-a-bicycle prompt under a starry twilight sky came back with no clipping and no misaligned paths.
- **Instruction-following:** One developer, Pankaj Kumar, reported the model parses multi-part instructions off a single prompt (color grading, day-to-night switch, working headlights, anatomical annotations, pedaling cadence) instead of needing four rounds of correction, and called it "fast where it counts."
- **Why the latency is a feature:** The 8–10 minute generations are heavy test-time compute — planning, writing, executing, debugging, and polishing internally before any token ships. Old Flash checkpoints were instant basic shapes and approximate coordinate math; this is precision placement and advanced voxel/lighting math.
- **Creative/front-end evidence:** Developer "B" shipped a sketch/pencil/graphite-themed showcase site in 14 minutes where scrolling progressively darkens the lines — an interaction the model conceptualized on its own. Another test blended cyberpunk + retrofuturism with a 3D grid, live dashboard, and interactive 3D model on one hero section.
- **Other outputs:** A full 3D Airbus H145 helicopter in ~10 minutes; a pixel-art 3D pagoda that "feels like you're standing inside it"; a 3D flight simulation that beats real Flash output; a Minecraft-style build compared favorably to published Astra results; a 3D cart racer that looks more modern than Cart Rider in its prime, with complete interactive logic in one shot.
- **Leaked benchmark chart (unconfirmed):** Deep SWEV 1.1 agentic coding ~88% (~2 points over Astra); GDP Eval-A-V2 — the only model on the board at2064 Elo; Terminal Bench 2.1 at 95.3% (first place); OSWorld 2.0 computer use at 86.8% (ahead of both Astra and Fable 5.1).
- **Spatial fidelity punchline:** Developer "Vidi" ran an SVG cat comparison and was floored mostly because GPT-6 Astra returned something "substantially more tiger than cat."
- **Pricing rumor as the bigger story:** $2.25/M input, $11.25/M output. Astra launched September 3, Fable 5.1 landed September 1, both at $10 in / $50 out — so ~22.5% of the Frontier tier. Against Google's own Flash promo pricing ($0.75 / $3.75 through end of December 2026), it's roughly triple, exactly what a pro tier costs.
- **Back-end specs (traced via ghost-routed calls, including one by researcher Qwena):** 10M token input ceiling and 256K token output ceiling, vs. official Flash's 1,048,576 in / 65,536 out — roughly 9.5x the input and nearly 4x the output. Most frontier models cap generation at 4K–16K tokens.
- **256K output implications:** entire repositories, full codebase refactors, long-form novels in a single continuous pass.
- **Buried capabilities:** permanent native cross-session memory (no bolted-on vector DB); direct internet access not routed through an API; "sandbox trap" environments that route malicious/untrusted code into an isolated synthetic environment; and native robotic motor control protocols — actual motor control translation, not a text-API bridge — pointing at DeepMind unified multimodal models running on physical hardware.
- **Official record is empty:** As of mid-September, no model card, parameter count, benchmark results, or API endpoint for Gemini 4 or Gemini 4 Pro.
- **The pressure behind it:** Last real pro series update was Gemini 3.1 Pro on February 19th (7 months prior). Pichai previewed Gemini 3.5 Pro at I/O for a June launch; it slipped, then reports in August said it was killed. Semi Analysis reported three blown deadlines and that the underlying architecture was scrapped entirely; The Wall Street Journal reported the same read. Reason given: the pro model wasn't improving faster than the flash model.
- **What Google says publicly:** On July 21, with the Gemini 3.6 Flash announcement, Google said it had begun its most ambitious pre-training effort to date. Two days later Pichai said plainly on Alphabet's Q2 earnings call that the company needs Gemini 4 to stay competitive at the frontier. Position: 3.5 is dead, everything rides on 4, pre-training evals strong, post-training progressing.
- **The RSI thread:** Google DeepMind Chief Strategy Officer Jasjit Singh said at the Agentech AI Summit in Berkeley that RSI has become a core part of the industry's capex, while admitting current AI revenue doesn't remotely support spending at that scale. The Information reports researchers at both DeepMind and OpenAI place realistic RSI around 2027–2028. The specific rumor: Gemini 4 finished pre-training early because DeepMind closed an RSI loop during training.
- **Dream RSI:** On the 14th, Google published research on how agents continuously improve their own search strategies during exploration and carry that experience into the next round — not proof, but confirmation RSI is central to the roadmap.
- **Downstream stakes:** Alphabet's market cap is ~$4.23 trillion (it crossed $4 trillion in January, after Apple announced Gemini powers the new Siri). TPUs are fabbed by TSMC; TPU servers come from Foxconn, Quanta, Inventec, Wistron, and Wiwynn. Gemini sparks Japanese version launched in July; enterprise customers are rolling onto Gemini Enterprise.
- **Timing:** Consensus guess is a reveal alongside new developer tooling at a fall event, most likely October, with Google historically stress-testing release candidates publicly weeks ahead of announcements.

## Technical Details

- **Comparison table (as stated in the transcript):**

  | Item | Official Gemini 3.8 Flash | Leaked anonymous model |
  |---|---|---|
  | Max input tokens | 1,048,576 | 10,000,000 |
  | Max output tokens | 65,536 | 256,000 |
  | Input pricing | $0.75 / M (promo, through end of Dec 2026) | $2.25 / M (rumored) |
  | Output pricing | $3.75 / M (promo) | $11.25 / M (rumored) |
  | PS5 SVG render time | 10–15 s | ~10 min |

- **Competitor pricing referenced:** Astra and Fable 5.1 both at $10 in / $50 out per million tokens.
- **Benchmark scores (unconfirmed):** `Deep SWEV 1.1 ~88%`, `GDP Eval-A-V2 2064 Elo`, `Terminal Bench 2.1 95.3%`, `OSWorld 2.0 86.8%`.
- **Test-time compute pipeline** described: `plan → write → execute → debug → polish`, then emit tokens.
- **Architectural trade-off:** basic geometric shapes + approximate coordinate math delivered instantly (speed tier) vs. precision coordinate placement + advanced voxel and lighting math delivered on completion (pro tier).
- **Supply chain:** `TSMC` (TPU wafers) → `Foxconn`, `Quanta`, `Inventec`, `Wistron`, `Wiwynn` (TPU servers).
- **Dates cited:** Gemini 3.8 Flash shipped Sept 2; Fable 5.1 Sept 1; Astra Sept 3; Gemini 3.6 Flash post July 21; Pichai on Q2 earnings call July 23; Gemini 3.1 Pro Feb 19; Dream RSI published "on the 14th"; Flash promo pricing ends December 2026.
- **Platform name:** Arena (blind LLM leaderboard, UC Berkeley team, 2023).

## Questions

- Is the Arena alias genuinely Gemini 4, and why would Google reuse a live model's exact name rather than publish an anonymous or staged entry?
- Every number in this video — benchmarks, pricing, context ceilings, back-end specs, cross-session memory, internet access, sandbox traps, motor control — is rumor or traced speculation. None is confirmed by Google.
- Why do early stop-training claims ("finished pre-training early") differ so sharply from DeepMind/OpenAI researcher estimates of 2027–2028 for realistic RSI?
- Would256K output and full-repo refactors in one pass actually change agentic coding economics, or is that a theoretical ceiling no real task fills?
- Native motor control "translation" is described but not specified: what protocols, at what rate, on what hardware, with what safety envelope?
- How do the claimed wins compare on cost-per-solved-task, not just raw score? The score chart and the pricing chart come from different unverified sources.
- Gemini 3.5 Pro was reportedly cancelled because pro wasn't improving faster than flash — what does that imply for the Flash/Pro tier split going forward, and does it hold if the leaked model is really a flagship wearing a Flash label?
- The video notes the scored benchmarks don't include robotics at all, so the most consequential claimed capability is also the least measured. What's the actual evaluation methodology?
- Nothing has been published under the Gemini 4 or Gemini 4 Pro names as of mid-September — does that absence itself signal something (delayed launch, safety hold, or just normal pre-announcement silence)?
- If the reveal slips past October, does that mean RSI wasn't actually in the loop, or just that shipping is late?
- Transcript notes Alphabet's $4T cap and TSMC/Foxconn supply chain exposure as read-throughs — but there's no order-book evidence cited here. How much of the training run is actually locked in, and on what terms?
<!-- yt-brain:related -->

## Related

- [[youtube/YouTube Knowledge Base|◻️ YouTube Knowledge Base]]
- [[youtube/llm-core|📁 LLMs & Model Behaviour]]
- [[index|🏛️ JARVIS Memory Vault]]

### Related notes

- [[youtube/llm-core/2026-10-03-the-first-real-rsi-is-here-and-it-s-evolving-fast|The First Real RSI is Here and It’s Evolving Fast]] · relevance 0.08
- [[youtube/llm-core/2026-10-05-use-opus-5-5-in-antigravity-official-method|Use Opus 5.5 In Antigravity (Official Method)]] · relevance 0.06
- [[youtube/linux-infra/2026-10-03-ai-harness-engineering-forward-deployed-engineering-tutorial|AI Harness Engineering - Forward Deployed Engineering Tutorial]] · relevance 0.06
- [[youtube/agents/2026-11-13-how-to-guarantee-structured-ai-outputs-with-pydantic-lesson|How to Guarantee Structured AI Outputs with Pydantic (Lesson: 3) #ollama #aiagents #gemini #ai]] · relevance 0.06

<!-- /yt-brain:related -->
