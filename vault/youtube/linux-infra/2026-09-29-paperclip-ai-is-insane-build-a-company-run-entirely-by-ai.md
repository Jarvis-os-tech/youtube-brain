---
video_id: Bj4mNOYjOek
title: "Paperclip AI Is Insane | Build a Company Run Entirely by AI"
url: https://www.youtube.com/watch?v=Bj4mNOYjOek
watched: 2026-09-29 10:35
source: chrome:Default
indexed: 2026-09-29T16:17:20+00:00
topic: linux-infra
type: youtube-note
source_url: https://www.youtube.com/watch?v=Bj4mNOYjOek
tags: [youtube, youtube/linux-infra]
---



## Core Concept

Paperclip is a free, open-source framework for running a company staffed entirely by AI agents: a human acts as the board of advisors, gives one instruction to a CEO agent, and that CEO hires whatever agents it needs and delegates issues to them (CTO, content writers, SEO engineer) which then execute autonomously. The video provisions a real instance end to end — Hostinger VPS, Anthropic API key, spend limits, a company called WP Optimizer — and then stress-tests it against real WordPress sites to see whether an agent-only company can actually deliver a business deliverable (SEO optimization, content generation, images, weekly performance reporting), what it costs, and where it breaks.

## Key Takeaways

**Deployment**

- Paperclip is free and open source but needs a host; the recommended target is a VPS (a 24/7 cloud computer). Hostinger auto-deploys Paperclip with the VPS.
- Hostinger flow: **Virtual Private Server** → **KVM 1** plan ("I think it's sufficient to run paperclip") → **Deploy**. Coupon code `30` = 10% extra discount. Term options are 1 / 12 / 24 months, but the minimum to get the discount is **12 months**.
- Optional extras declined by the speaker: daily backups ("never had any problem with my VPS") and non-nearest server locations. Hostinger offers a 30-day, no-questions-asked refund.
- Signup: Google, GitHub, or email + password. Billing address needs first name, last name, country, address. Payment shown: credit card, PayPal, Google Pay, Apple Pay — he avoids the ones that "take a business day" and uses a credit card.
- Deploy form asks for a model provider: **Anthropic, OpenAI, Gemini, or CursorAI**. Paperclip itself is free; the *agent work* costs provider credits.
- Credits are the real cost driver. Pitch is "build for only just $5"; tiering is **$5 of credits = up to 30,000 tokens per minute**, **at least $40 = up to 250,000 tokens per minute**. He funds **$50** because high-quality tasks blow past the 30k tier.
- **Never enable auto reload.** The dashboard offers to "turn on auto reload" (charging the card when credits run out) — "I've been burned multiple times with thousands of dollars." He uses **Organization settings → Spend limits** instead, currently capped at **$500/month**, and checks **Billing → auto reload is disabled**.
- API key wiring: **Manage API keys → Create key**, name it `paper clip`, copy it once ("make sure that this code is never visible to anyone except for you"), paste into the Anthropic field, **Deploy**.
- Two containers appear after deploy: the Paperclip container plus one called **traffic**, described as "an extra security layer from Hostinger that will make your whole project secure."
- Access path: Hostinger → **Docker Manager → Projects → Access → Open** → sign in with the same credentials.

**Company setup**

- Company name **WP Optimizer** (Z spelling chosen over S); mission drafted externally with ChatGPT; agent name **CEO** (joke alternatives: Josh, Cindy); runner **Claude Code** ("we use Anthropic and Anthropic is linked with Claude Code"; ChatGPT pairs with **Codex**, unused); model = **default**; **Test** connection → "working with a few warnings. That's totally fine."
- Launch issue: title **"Hire the right agents for the right tasks"**, body asking it to find people to scan WordPress sites, optimize them for SEO and LMS, research blog-post content, and hire content writers plus whatever else is needed. Final button: **"Create an open issue"**.
- Multi-company support via the left rail (**plus** button). Contrasted with "OpenClaw," where all agents live in one Telegram chat box — "with Paperclip, you have multiple companies. It gives a bit more structure."
- Dashboard signals: active agents, in-progress tasks, monthly spend, and **pending approvals** ("waiting board review"). Role split is explicit: he is the **board of advisors**, not the CEO; the CEO decides how to execute.
- First approval: "hire an agent, chief technology officer" → **approve**. **Company org** then shows CEO + CTO, both actively working.
- Issues board: list view, **green = done, red = blocked**; filters new / in progress / blocked / done.

**Run 1 — first two failures**

- After ~10 minutes and **$7.50 spent**, the CTO had started optimizing **ferdy.com** (inferred because the hosting account is his) and was **scraping the public front end because there was no REST API**. It asked for a login URL, username, and WordPress application password, and promised "nothing will be scraped or modified without your explicit submission." Called "part of the learning process" — "$7.30" burned.
- Fix was a new issue, not a correction: *"Only work on websites"* — the business is a service where the customer supplies URL + username + application password.
- Test target `wearewebdivine.com` (a web design agency site, blog posts previously removed). In WordPress **Users** he created `wp-optimizer`, generated an application password, and handed URL + user + app password to the CEO via a new issue.
- ~20 minutes later the issue was picked up by **agent number eight**, which replied with a structured scope: *analysis* (titles, tags, categories, meta descriptions), *phase two: content optimization*, *phase three: content generation*, plus the constraint "it will stop if it's not working after three times" and the goal of "transform[ing] the website into a fully optimized, continuously growing content platform that increases organic traffic authority and AI visibility with minimum manual effort."
- Second failure: issue turned **red** because the username `WP optimizer` was not a real user on the site. His fix in a reply: give the **administrator's real username/email**, state that the **application password *name* is "WP optimizer"**, then the password — this woke the CTO and work resumed.
- Business model sketched mid-run: **$500 one-off**, or a **$100/month** subscription where the company keeps optimizing a site each month at a cost of "a few dollars."
- Results on the real site: **three new blog posts** added, keyword-rich page titles, meta descriptions adjusted, taxonomy cleanup, and it correctly flagged manual cleanup — a **fake phone number** and **an unused Elementor page that should be trashed**.
- Generated posts were locally targeted: "How to choose a web design agency in Amsterdam" and "SEO for small businesses in Amsterdam"; the site now has an "About WebDefine — Amsterdam web agency" page title, though the visible menu label still says "About."
- Third iteration: the SEO checker reported "no images or videos found on this page" and "title exceeds" 60 characters. He asked for a **featured image per post plus inline images**; **five minutes later** an update listed which post, which images, and where the edits were. After a refresh **all issues went green**. Caveat: the images came "from a free website."

**Run 2 — operating an existing site**

- **Link a paid iStock subscription** (100 images/month) to the agent's workflow. Unlinked/agent-sourced images "do the job" but "come across as not super professional."
- Acceptable alternative: pre-upload a curated high-quality set of iStock (or AI-generated) images, optimize them at **png.com** to shrink file size, upload them to the WordPress media library, and let Paperclip select from that library. Demonstrated: the agent pulled an image out of the media library, and those were high-quality iStock files.
- **Filename rule learned the hard way:** a team he hired years ago put years in image filenames, so every image still reads 2024 even though the agent correctly changed post text from 2024 to 2026. Rule: **never use a number (like a year) in image filenames.**
- Instruction he wants given: do the whole thing (featured images + in-post images) in **one pass**, without being asked repeatedly — the images "are part of the process."
- Credentials handed to an agent are **four items**: the website URL, the WordPress admin/user-interface URL, the application password *name*, and the application password *value*. Path: *User → Edit Profile → scroll down → WP-Optimizer → add an application password*. Spoken route for the test sites (`optimizedv5.com`, `hpsdv5.com`): `wp-admin/user/application/user/application/password`.
- **Issue → CEO → CTO routing behaves like an org chart:** he created a new issue assigned to the CEO, the dashboard showed "sent to the CTO," the CEO woke up, the issue flipped to in-progress, and the CTO began with the login details already in hand. The inbox showed it talking through a plan ("go to #11") before running.
- **Unattended 10-minute run:** by default it created new blog posts *and* updated all existing blog posts — every "2024" changed to "2026", and each post's publish date set to today.
- New posts inherited the old media library, so stale 2024 imagery leaked into brand-new posts.
- **Heading hierarchy was a mess:** H2s, then H3s ("it's even H3, that's the problem"), then H4, and some things that "are not even an H." He wants them promoted to real titles or styled like the existing purple titles.
- **Verify before selling it:** Google Analytics, Surfer SEO, Rank Math, or Yoast — "You've optimized the website, keep track of how the website is performing." If it isn't improving, don't use the tool on your own site.
- **Recurring agent task:** a weekly digest of site performance — increased views? sales? visibility, visitors, engagement — by asking Paperclip to "check those websites" and give an overview every week. Caveat: it cannot track sales for a local business, so visibility/visitors/engagement are the proxy metrics.
- **Use-case discovery trick:** ask ChatGPT `what are some great paperclip use cases that can help me with my <business or YouTube channel>`, then paste the ideas into Paperclip's **+** → create a new company, write a mission, etc.
- **Cost checkpoint:** total spend for the whole run was **less than $17** to optimize two websites. "I would be less happy if it would be $80." He frames it as trial and error on a brand-new tool, with the policy: "if it's not working, you should not sell this to others."
- **Closing thesis:** ChatGPT = chat and get answers → OpenAI/"open call" = perform tasks → Paperclip = multiple agents doing multiple things. He invites topic requests leaning "less WordPress, more AI kind of tools."

## Technical Details

- **Architecture / roles**
  - Board (human) → instructs → **CEO agent** → hires and delegates → **CTO** and other agents (content writers, SEO engineer).
  - The CEO "can hire other agents… it can do things by itself. It can delegate things."
  - Multiple isolated **companies** per Paperclip instance, each with its own org chart and agents.
  - Delegation is observable: issue assigned to CEO → CEO reassigns → dashboard shows "sent to the CTO" → target agent wakes with credentials already in the thread.
- **Work item model:** everything is an **issue** with a status (`new` / `in progress` / `blocked` / `done`) and an assignee agent; the human review surface is a queue of **pending approvals** in an **inbox** (approve / reply `done`).
- **Failure model:** agents are expected to retry and give up — "it will stop if it's not working after three times." Blocked issues render **red**, finished **green**, in-progress **yellow**.
- **Hosting stack:** VPS (Hostinger, KVM 1) → Docker Manager → Paperclip container + a `traffic` container for edge security → browser access via Docker Manager Projects → Access → Open.
- **Model providers selectable at deploy time:** Anthropic, OpenAI, Gemini, CursorAI. Paired coding runners: **Claude Code** (Anthropic) and **Codex** (ChatGPT/OpenAI). Model choice: default; a **Test** button validates the connection before launch.
- **Credential handling:** provider API key is created in the provider console (`Manage API keys → Create key`), pasted into the deploy form once, never displayed again. Target-site credentials are passed as **URL + WordPress admin URL + application password name + application password value**; the agent refuses to touch a site without an explicit submission.

```
ferdy.com forward slash paperclip . com      # sponsor link (transcribed)
KVM 1                                        # VPS plan
30                                           # coupon code for 10% extra discount
Anthropic | OpenAI | Gemini | CursorAI       # provider choice
Claude Code | Codex                          # runner choice
paper clip                                   # name given to the created API key
```

- **WordPress integration:** prefers a **REST API**; falls back to **front-end scraping** when none is available. Writes performed via the application password: post creation, bulk body-copy year sweeps, publish dates, page titles, meta descriptions, taxonomy, heading levels, featured and inline images, media-library selection.

```
WordPress Users -> create user: wp-optimizer
WordPress Users -> Edit Profile -> scroll down -> WP-Optimizer
                  -> add an application password
spoken route:   wp-admin/user/application/user/application/password
agent #8 -> took the wearewebdivine.com issue
```

- **Editorial/technical taxonomy the agent mishandles (usable as an agent spec)**
  - Year strings embedded in body copy → sweep to the current year (2024 → 2026).
  - Post `publish date` → set to today to avoid looking stale.
  - Heading levels H2/H3/H4 and unlabeled non-heading blocks → normalize to one title level matching site styling (purple titles).
  - Featured image per post plus in-body images → treat as one standard process, done in a single pass.
  - Image filenames must not contain years or numbers.
- **Media pipeline (the "professional images" workaround)**

```
iStock subscription  --+
or AI-generated set   --+--> optimize at png.com --> upload to WP media library
existing high-quality --+                                     |
                                                              +--> agent selects from library
```

  Direct subscription linking is preferred over the library dump; the library dump introduces stale-file risk (the 2024 problem).

- **Rate-limit economics (why $50, not $5):**

  | Credits added | Throughput |
  |---|---|
  | $5 | up to 30,000 tokens/min |
  | ≥ $40 | up to 250,000 tokens/min |

```
$5   -> 30,000 tokens per minute
$40+ -> 250,000 tokens per minute
$50  -> what he actually funded
$500 -> monthly spend limit (Organization settings)
auto reload -> tops up $40-$50 when balance hits $5 (left disabled)
$100/month, or $500 one-off -> pricing he considers selling at
```

- **Safety rails in the provider console:** Organization settings → **spend limits** ($500/month), Billing → **auto reload** (disabled).
- **Verification / measurement stack**
  - Google Analytics (traffic); Rank Math, Yoast, Surfer SEO (rank/health)
  - Rollup metrics: views, sales (where trackable), visibility, visitors, engagement
  - Test sites: `wearewebdivine.com` / `wearewebdefine.com`, `optimizedv5.com`, `hpsdv5.com`, `divi5.com`
  - Cost gate: **< $17** actual vs. **$80** considered unacceptable
- **Trade-offs stated or implied**
  - Agent-picked free/AI images: functional but unprofessional-looking → costs quality.
  - Pre-curated media library: better images, but upkeep and stale-file risk.
  - Unattended 10-minute runs: fast, but produce hierarchy/date/filename defects a human must audit.
  - Low cost vs. unproven efficacy: he refuses to commit until analytics confirm lift.
  - Multi-company structure vs. a single shared chat box (his "OpenClaw" comparison).
- **Spend and latency, as narrated:** **$7.50** at the ~10-minute mark of run 1 while still setting up; "$7.30" for the ferdy.com detour; **under $17** total for the whole run. Latency: ~20 minutes from issue submission to the CTO's detailed scope-of-work reply; ~5 minutes from the featured-image request to a completed all-green update; ~10 minutes for the unattended bulk update run.

## Questions

- **No total cost breakdown.** $7.50 at 10 minutes, $7.30 for the detour, and "less than $17" total are given, but never the final bill per website, nor whether the "$100/month subscription for a few dollars of cost" math survives provider fees, retries, and blocked attempts.
- **Whether the $500/month spend cap is compatible with a retry-three-times agent** is never reconciled; a single runaway loop could consume the cap quickly.
- **Second half of run 1 is unwatched.** The transcript ends mid-inspection of the inserted images ("or mobile. So there's…"), so the final state of that company and any remaining manual work are unknown.
- **Image quality/licensing unresolved.** The agent filled posts with images "from a free website" / free stock; the answer given is only "if I take a look at the quality… okay." No licensing, attribution, or QC policy — and no explanation of how iStock reuse across many posts avoids duplicate-asset problems.
- **Still-open SEO complaints.** "Title exceeds" 60 characters was flagged, but the follow-up request covered images only; no confirmation the over-length titles were ever rewritten. Likewise, the "About" menu label vs. the new "About WebDefine — Amsterdam web agency" page title is left unreconciled.
- **Accuracy of generated content is unverified.** Three Amsterdam-focused posts were published; nothing is said about factual correctness, brand fit, or ranking. Nor is there a stated wait time or threshold for judging whether the work actually worked ("I will take some time").
- **The `traffic` container is asserted, not explained.** "An extra security layer from Hostinger" with no detail on what it does or whether it costs extra.
- **Model configuration is almost entirely default.** "I will go with the default model" — no info on which model per role, context limits, or whether Claude Code over Codex mattered for quality or cost. Nor is the per-agent model/provider mapping given, so the $17 figure can't be itemized.
- **How the agent actually authenticates** is unclear: WP REST API with the application password, WPGraphQL, or browser automation. The WordPress/Divi version and plugin set are never stated.
- **The application-password route is spoken garbled** as `wp-admin/user/application/user/application/password`; the exact route needs verifying, as does whether the WP-Optimizer plugin is required at all versus the native WordPress Application Passwords screen.
- **Recurring tasks are underspecified.** How the weekly digest is scheduled — a Paperclip-native recurrence, a cron, or an external n8n/job hitting the agent — is not said. Nor is it said whether the agent can read Google Analytics / Search Console directly or whether the human must pull the data and feed it in.
- **No dry-run / preview mode is shown.** Inbox approval is described as post-hoc ("if I'm happy, I can say done"), implying a real risk of live publishing.
- **No rollback path for live writes.** The agent modified a production site (titles, meta, taxonomy, dates, posts, images) with no mention of staging or backups — especially notable since daily VPS backups were declined earlier. Nor is there a stated recovery path if a run half-completes.
- **Scaling limits are unstated.** He hints a bigger company needs "more instructions from us," but there's no ceiling on agent count, concurrency, or companies per instance.
- **Portability is unaddressed:** does the CTO skillset transfer to Shopify/Webflow/custom stacks, or is it WordPress-specific?
- **Mission quality is outsourced to ChatGPT** in the video, with no discussion of how good or bad that mission statement actually is as a driver of agent performance — nor of the "Only work on websites" issue that was needed to correct the initial scope creep.
- **Site-name spelling is inconsistent in the transcript** — `wearewebdivine.com`, `wearewebdevine.com`, and `wearewebdefine.com` all appear, and the on-page title is quoted as "About WebDefine". Worth verifying which domain and brand was actually targeted.
<!-- yt-brain:related -->

## Related

- [[youtube/YouTube Knowledge Base|◻️ YouTube Knowledge Base]]
- [[youtube/linux-infra|📁 Linux & Infrastructure]]
- [[index|🏛️ JARVIS Memory Vault]]

### Related notes

- [[youtube/agents/2026-09-29-autonomous-ai-and-agent-orchestration-buzz-paperclip|Autonomous AI and Agent Orchestration - Buzz + Paperclip]] · relevance 0.10
- [[youtube/agents/2026-09-29-paperclip-vs-multica-which-ai-agent-orchestrator-is-actually|Paperclip vs Multica: Which AI Agent Orchestrator is Actually Good? (2026 Latest Review)]] · relevance 0.09
- [[youtube/agents/2026-09-29-run-hermes-agent-on-a-free-vps-unlimited-use|Run Hermes Agent on a FREE VPS (UNLIMITED USE)]] · relevance 0.09
- [[youtube/agents/2026-09-29-hermes-paperclip-ai-litellm-how-to-build-an-ai-product-studi|Hermes + Paperclip AI + LiteLLM: How to Build an AI Product Studio]] · relevance 0.08

<!-- /yt-brain:related -->
