---
video_id: xvquJW5zgmQ
title: "Complete Guide to building Jarvis with Claude"
url: https://www.youtube.com/watch?v=xvquJW5zgmQ
watched: 2026-11-13 18:29
history_class: ai
transcript: "/home/g0pi/jarvis-yt-brain/yt_brain/transcripts/xvquJW5zgmQ.txt"
indexed: 2026-11-14T13:31:22+00:00
---

## Key Points

- Most "Jarvis" setups online are fake ChatGPT wrappers; a real system monitors data, triages mail, suggests actions, and schedules automated background routines.
- The design uses three specialized agents behind one visual command center instead of one overloaded chatbot.
- Scout (read-only intelligence officer): gathers business, finance, productivity data overnight and assembles it in one place.
- Operator (worker): handles routine tasks like drafting email replies, managing CRM, preparing content, bound by a safety rulebook.
- Advisor (chief of staff): reads scout and operator reports and produces exactly three ranked daily actions plus an accountability loop.
- Recommended build sequence: command center on mock data → scout → operator (review drafts first) → advisor → wire real data replacing mock data.
- Command center needs a visual screen (built via Claude Design) so the assistant isn't forgotten; includes a voice layer via browser speech recognition/synthesis.

## Required / Actionable Items

- Build the command center at claude.ai/design using a futuristic dashboard prompt; structure all metrics into one central mock data object at the top of the file.
- Add voice: browser built-in speech recognition/synthesis; optional 11 Labs API key with the George voice (or Fish Audio).
- Connect tools in Claude's connectors tab (Stripe/RevenueCat, Meta/Google Ads, GA/PostHog/Clarity, Shopify, GitHub); use Claude in Chrome for apps without official MCP connectors.
- Create the scout as an automated morning routine in Claude Code using the scout system prompt; enforce the "unavailable" rule (no guessing when data can't be verified).
- Operator: connect Gmail/Outlook, Slack/Discord, Notion/Trello, HubSpot/GoHighLevel; create a `faq.md` with repeated client questions and answers in your personal voice; add the operator prompt.
- Advisor: schedule a routine in Claude Code right after the scout; copy the advisor prompt; it filters through three tiers (production/revenue blockers, outperforming campaigns needing resources, slow operational leaks) and runs an accountability loop over the last 7 days of ignored recommendations.
- Personally review every operator draft for the first few days before granting write permissions.
- Like, subscribe, and comment with your #1 automation task for a chance to win a $100 Claude/ChatGPT Max subscription.
- Optional community access for prompts/templates/content OS: school.com/raisyfoo.

## Important Details

- Creator: Ray, ex-Meta software engineer.
- Demo numbers mentioned: Stripe $3,150 collected yesterday, $42,100 month-to-date (+16% vs. last month); Meta ad spend $480 at 3.1x ROAS; ad set two outperforming benchmark by 35%; scale daily budget by 20%; recurring 2:00 p.m. check on client emails.
- Command center runs locally in one self-contained HTML file.
- 11 Labs has a free generous plan; other voice APIs (e.g., Fish Audio) also work.
- Scout is strictly read-only and cannot break business data; operator never sends rogue emails because it is bound by `faq.md` and reviewed drafts.
- Advisor produces exactly three concrete ranked actions and surfaces ignored tasks until completed or killed.
- Content operating system (5-minute setup interview, competitor analysis, script drafting) is available via the school community, not public.
