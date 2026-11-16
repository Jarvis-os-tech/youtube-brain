---
video_id: nAkfg5TUBKk
title: "Forget Prompting. This Is How a $10B Company Uses AI Agents with Second Brain"
url: https://www.youtube.com/watch?v=nAkfg5TUBKk&t=18s
watched: 2026-11-09 18:58
source: chrome:Default
topic: agents
indexed: 2026-11-13T02:42:16+00:00
type: youtube-note
source_url: https://www.youtube.com/watch?v=nAkfg5TUBKk&t=18s
tags: [youtube, youtube/agents]
---


## Core Concept

Notion is presented as a central context layer — a "second brain"/"backpack" of memory and skills — where humans and AI agents collaborate: internal company data lives in Notion databases, external tools (Salesforce, Gong, Zendesk, Jira, Slack, Snowflake, HubSpot) are synced in via Notion Workers, and custom agents with scoped permissions automate triage, support, feedback routing, and data analysis. The same shared context powers multiplayer agent improvement (many people improving one agent via Slack), non-engineer-built micro-apps/MVPs that engineering later adopts, and portable skills that travel between agents and people, while Notion itself orchestrates existing models rather than building its own.

## Key Takeaways

- Notion employees are called "notinos"; Notion 1.0 was documents/pages, Notion 2.0 added general-purpose databases.
- Database scale: currently ~100,000 rows, targeting ~100 million rows; ~1 million rows already causes slowness; AI agents generate data ~3 orders of magnitude faster than humans.
- Go-to-market stack uses Salesforce (CRM), Gong, and Zendesk alongside Notion.
- Notion Workers (released ~4 months ago) sync a Notion database with any other data layer via cron-like jobs running every 15 minutes; e.g., joining Jira engineering data with Salesforce feature requests.
- Per-account dashboards ("customer hub") surface Zendesk tickets, Gong conversations, and open Salesforce opportunities in one place.
- Enterprise search answers company-wide questions across tools and can leverage shared "skills" (e.g., a coworker's meeting-prep skill); results respect per-user permissions.
- Custom agents have three parts: triggers (events in Discord/Notion/email), instructions (a prompt/doc), and tools (Notion pages, Slack, MCPs, Snowflake, a model, a computer/VM); default access is none.
- "Data scout" is a custom agent built by a Notion data scientist, available to everyone; each query costs a few dollars but replaces data-science bottlenecks.
- Multiple people can collaboratively build an agent, then the whole company can use it.
- Mail triage agent filters/archives email, drafts replies, and creates tasks.
- "Smilers" is a people-team Slack agent answering repetitive questions (health insurance, office supplies) with voice/tone rules; it is a self-building knowledge base that creates tasks when it lacks an answer.
- Feedback router centrally collects feedback in Slack and routes it to the right people/teams.
- Second-brain maintenance can be offloaded to agents ("keep filling this thing by yourself"), so users benefit without manual upkeep.
- Notion homepage positioning: "a platform where humans and AIs can collaborate together."
- The **router** is a routing-rules database with thousands of instructions, none written by humans; people give feedback in Slack and it builds the rules (e.g., Ivan's rule to add an emoji and thank the person on AI questions).
- The router is the agent's primary memory, updated day-to-day; built by the product ops team so no employee has to manage it directly.
- A single agent is used by multiple people simultaneously, and they collaboratively improve it for everyone ("true multiplayer collaborative AI").
- A **Kanban-style flow** runs the engineering factory: one agent ingests field bugs into tasks, another picks them up and moves to review, Claude writes the plan, Codex writes code, another agent ships; humans read/comment/approve.
- The factory metaphor extends beyond engineering (performance marketing, performance reviews); one engineer built the setup and everyone uses it, and non-engineers can build it too.
- You don't have to change your stack: it can sync with Linear/Jira or run standalone; AI handles documentation/understanding/shipping while humans approve/reject and orchestrate.
- Growth School account prep: fragmented workspaces, usage, and spend surfaced; a phone query preps a meeting in ~5 minutes, replacing separate asks to data scientist, revops, rep, and enablement.
- Don't move your data: connect Salesforce/HubSpot/etc. into a central context layer; cloud agent, Codex, and Cursor agents all pull from the same context.
- Notion pricing anecdote: ~$30,000 total spend over a year; fragmentation as teams grew; recency meant not all 7 years of data was pulled.
- Knowledge as advantage: references Andre Karpathy's LLM wiki and Gstack (Gary Tan); the core edge is giving the right context to the right agent.
- Unlaunched **custom blocks**: Austin (people team, SF environment lead, ~7,800 people) built a seat-map micro-app replacing ~$50k office software, with rearrange seats, bank, shift-click multi-move, seat sharing, conflict flagging (Jack/Kevin same seat), planned moves, complete-save writing to the DB, person search, and IP toggle.
- A custom block is a v-coded view with a Notion database as the data layer (bidirectional sync); built by someone who never coded before.
- Storytelling channel + "Ish" helps employees post; affiliates (employees) get 5–10x impressions vs. the brand account.
- Personal agents discussed: Muse, Instinct, Grockbot, with trade-offs (multi-agent vs. single agent with background threads; side chats vs. one chat).
- Nathan's instructions doc: copy to all agents; creates an `agents` doc in private Notion with shared memory/context; Muse shows "memory writes two-way sync with Notion memory."
- The setup lets you start a new agent product without re-teaching it; the "cost of moving from one agent to another" is made free/portable.
- Notion has invested in MCP/connectors so agents can read from and write to Notion memory; a newly released agent can get "instant on" access and write back into shared memory.
- Skills can be stored centrally in Notion: personal and company-wide skills appear in a library and can be enabled for agents such as Muse and Grock (as spoken).
- A skill built in Notion can be used across agents; the conversation notes similar deployment could happen from GitHub, Claude, or Codex, but Notion is presented as easier for non-technical users.
- Notion is described as not building its own model; it orchestrates existing models and acts as context infrastructure.
- The speaker places AI-native companies around the 50th–60th percentile of AI usage, with higher percentile claims for San Francisco and the world, while describing Notion itself as middle-of-the-curve overall.
- Ramp is cited as a company that uses Notion even better than Notion uses itself, leveraging a context graph, agents, a router, spend management, and product spin-ups.
- A three-person team is said to run about 300,000 agent queries per month.
- Most people outside San Francisco are described as using AI like Google search; the gap between AI capability and adoption/diffusion is described as unusually large.
- The capability-vs-adoption gap is illustrated by a "humanoid robots cutting corn one by one" vs. "combine harvesting" meme: current work mirrors human workflows, while an agent-native way of working is still emerging.
- Historical analogies: the printing press initially produced handwritten-style output until typography; film was initially shot like stage plays until camera movement.
- Notion's history: founded in 2013, first product launched in 2017; originally aimed to democratize software-making as a no-code platform, in the same vintage as Airtable, Figma, and "Kod" (as spoken).
- The market wedge was docs/knowledge; many users moved from Evernote to Notion.
- "Malleable software" means AI-generated Notion artifacts can be tweaked by the user rather than only conversed with.
- AI is framed as augmenting human intelligence ("bicycle/electric car for the mind"), not AGI replacement; average users can improve while top 1% can do even more.
- Roles blur: product designers ship and engineers design, making "builder" a more fitting label.
- Sponsored segment: the speaker describes opening Notion after podcasts, holding `Fn` for hands-free dictation via Whisper, which learns their speech; about 180,000 words spoken ("basically a whole book"). It also mentions Fulcrum for building AI agents/assessment reports and Art for consistent character images and one-click image-to-video.
- Non-engineering functions (customer success, sales, marketing, product, design) ship their own MVPs; engineering does not touch the MVP. A basic skill ensures integration with "the O," pulls the right data, and stays secure/non-breaking; the MVP is pushed to learners/users, tested, and adopted based on metrics.
- If adoption signals are good, the function presents to the product lead (with PostHog data) and engineering then takes the codebase into the main product. Team is 400 people total, only 20 in engineering/product/design.
- The speaker frames the future as two roles: builder or seller; best people are builders who can sell or sellers. Sales metric pushed: percentage of time spent speaking with customers.
- Anthropic economic-impact report: a job is a bundle of tasks across four types — human-only, AI-augmented, AI end-to-end, and newly created by AI. The human-only category is largely conversation. ~80% of the speaker's sales calls are now done by AI, enabling conversations that humans couldn't have had before; team has ~10x better conversations than two years ago.
- Bridgewater-style total legibility: recording/transcribing nearly everything (95%+ of meetings except 1:1s/personal) makes the business legible and gives AI infinite context humans can't hold; AI can answer questions like why a release date moved.
- Notion acted as company note-taker for ~5 years; AI now does note-taking. Central context repository concept: GitHub for engineers, Notion for knowledge work (e.g., performance marketing and demand gen sharing context).
- Notion hesitantly shipped MCP; became one of the first five connectors any harness ships. Customer owns their data.
- Notion AI product timeline: alpha released ~a week before ChatGPT; writer product (GPT-4 wrapper, doc completion); enterprise search (like Glean, connects Notion + other tools); meeting notes ~a year ago; agent (can do anything a human can, build databases, connect things); custom agents (define an employee with permissions/tasks). Context/connective-tissue shift in last 3–6 months; ~10 years spent building the context layer (editor, database, connections).
- Rapid fire: strange AI use = voice mode while driving alone (Tesla hard-press activates Grok). If only one AI tool kept (not Notion): Riverside (weekly podcast with daughter; Apple voice message to published in ~30 min). Favorite outside Notion: Matic vacuum (used ~2x/day, kids love it) plus Pebble ring/watch for on-the-go recording that MCPs into Notion; Meta shipping Charm; Tamagotchi-like devices returning.
- Future of jobs: bright, net positive; displacement but more jobs created; "AI won't take your job but someone using AI will."
- Mind-blown: conversational quality improving daily. Never let AI replace: time with kids. If not building: culinary school / making food (plumber joked). Underrated AI product: Tesla Full Self-Driving — felt dangerous 18 months ago, tryable 12 months ago, subscriber 6 months ago, hasn't driven in 2 months; handles ~150 mi through city/highways/forest and parks; camera-tricking viral video mentioned; wants steering wheel removed; made with just cameras.

## Technical Details

- Scaling target: 100,000 → 100,000,000 rows per database.
- Sync cadence: every 15 minutes via Notion Workers.
- Agent anatomy: triggers, instructions (stored as a Notion doc), tools/access (default no access).
- Agent capabilities mentioned: Slack connector, Snowflake direct access, model selection, computer/VM.
- Example agent query (verbatim intent):
```
I am meeting with web hub. What's your email? Can you look at their personal usage and also their company usage? Give me trends and spend details. Also look at our enablement docs and suggest ideas for how they can use notion better.
```
- Self-building knowledge base pattern: answer from knowledge; when unknown, create a task; when answered, write back into knowledge.
- Router: routing-rules database, thousands of rules, Slack-driven feedback, day-to-day updates; product ops built it.
- Engineering flow: bug ingestion → task creation → review → plan (Claude) → code (Codex) → ship; human comments move it forward.
- Context layer: central store queried by phone; integrations with Salesforce/HubSpot and agents (cloud agent, Codex, Cursor).
- Custom blocks: Notion DB as data layer; vcoded view; bidirectional data↔visualization sync; "rearrange seats" toggle, "people bank", "complete save" writes DB.
- Personal agent sync: shared `agents` doc + two-way memory sync with Notion memory.
- Terms and concepts: MCP, connector, memory, skills, library, context graph, router, vector database, malleable software, AGI, augmentation, "builder."
- Architecture described: Notion as central context; skills stored in a Notion library and enabled per user/agent; agents read/write through connectors; multiplayer company context shares skills across people and agents.
- Deployment options mentioned: build/point to skills in Notion, with options to deploy into other agents; GitHub, Claude, and Codex are mentioned as possible skill locations/deployment paths.
- Trade-off/comparison: GitHub can do similar skill sharing, but Notion is presented as easier for non-technical users; many technical users also find GitHub complex.
- Model strategy: Notion orchestrates existing models rather than building its own.
- Historical/product context: Notion started as a platform for building end-to-end apps without code; narrowed to docs/knowledge as a wedge; AI later made the broader "build your own software" vision more accessible.
- Sponsored technical claims: hands-free dictation via `Fn` key and Whisper; Fulcrum analyzes a requested AI agent and produces an AI assessment report; Art maintains the same character across scenes and converts an image to a short video.
- Numbers mentioned: 2013, 2017, four or five years before first launch, 2012/2013 vintage, 3 weeks away, 50th/60th percentile, 95th percentile, 99th percentile, 3 people, 300,000 agent queries/month, 50th percentile, 98th percentile designer, top 1 percentile, 180,000 words, "basically a whole book."
- Roles/stack mentioned: PostHog (adoption metrics), Notion (docs/databases/meetings/agents/MCP), MCP (connectors), GitHub (engineering context), Slack (channels), Riverside (podcast production), Matic (hardware vacuum), Pebble (wearable recorder), Tesla FSD/Grok (in-car).
- Architecture pattern: central context repository feeding agents; "everything recorded/transcribed/summarized into a meetings database available to everyone"; 95%+ meetings captured.
- Trade-off noted: shipping MCP may affect product/business flows, but customer owns data; connective tissue across tools is now the priority.
- No code, commands, or file paths appear in several transcript segments (explicitly noted).

## Questions

- What are the exact per-query costs and limits for agents like data scout ("a few dollars" is unspecified)?
- How are triggers, instructions, and tool permissions configured at the UI/API level, and what governance controls exist?
- What are the precise current row limits and performance characteristics at 1M+ rows?
- Are Workers push- or pull-based, and what retry/error handling exists?
- How is the "computer" (VM) for agents provisioned and secured?
- What data-residency and permission models apply to cross-tool synced data?
- Does the enterprise-search skill system support versioning/sharing beyond a single workspace?
- When do custom blocks launch, and will they be generally available?
- How does the router prevent bad/collusive rules from Slack feedback (only "it's within the team" was said)?
- What is the recency window for Notion's data pull (7 years wasn't fully pulled)?
- How is access control handled when non-engineers build and launch micro-apps company-wide?
- What's the cost/seat model for custom blocks vs. the $50k office software it replaced?
- Multi-agent vs. single-agent-with-threads: which does the speaker actually prefer long-term (still figuring out)?
- How does the shared `agents` doc handle conflicts when multiple agents write simultaneously?
- What exactly are "Muse" and "Grock" (as spoken), and how do they integrate with Notion memory/skills?
- How are skills technically synchronized or deployed across agents such as Notion, Claude, Codex, GitHub, and newly released agents?
- What does "context graph" mean in the Ramp example, and how is the router implemented?
- Are the percentile and productivity claims (50th–60th, 95th, 99th, 300,000 queries/month) measured or anecdotal?
- What is the "self-re writer" skill, and why is it tied to performance season?
- How does Notion's early no-code platform relate to its current "malleable software" model?
- The transcript cuts off at "as of today the way it's working for me I I would love to know how i," so the final thought is incomplete and should be verified.
- Which statements come from the sponsored segment, and should those tool claims be verified independently?
- What does "the O" refer to in "integrates with the O" — OAuth or another system? The transcript does not clarify.
- What are "learners" vs. "users" in the MVP push — internal learners, external beta users, or something else? Unspecified.
- The Anthropic report is referenced but not named or dated beyond "a couple of weeks back"; the four task categories are described loosely.
- The claim that "80% of sales calls are done by AI" and "10x better conversations" is anecdotal; no supporting data in transcript.
- Whether the 95%+ meeting recording rate and 10-year context build are exact or approximate is not verified.
- The "two roles left" framing (builder/seller) is an opinion; transcript does not substantiate it empirically.
<!-- yt-brain:related -->

## Related

- [[youtube/YouTube Knowledge Base|◻️ YouTube Knowledge Base]]
- [[youtube/agents|📁 AI Agents & Orchestration]]
- [[index|🏛️ JARVIS Memory Vault]]

### Related notes

- [[youtube/linux-infra/2026-10-03-ai-harness-engineering-forward-deployed-engineering-tutorial|AI Harness Engineering - Forward Deployed Engineering Tutorial]] · relevance 0.12
- [[youtube/llm-core/2026-11-13-i-gave-chatgpt-claude-and-codex-one-shared-brain|I Gave ChatGPT, Claude and Codex One Shared Brain]] · relevance 0.09
- [[youtube/agents/2026-09-29-introducing-multi-agent-orchestration|Introducing multi-agent orchestration]] · relevance 0.09
- [[youtube/dev-craft/2026-10-03-building-a-software-factory-that-actually-works-full-course|Building a Software Factory that actually works (Full Course)]] · relevance 0.09

<!-- /yt-brain:related -->
