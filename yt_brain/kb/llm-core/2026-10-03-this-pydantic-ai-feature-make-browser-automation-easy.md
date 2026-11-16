---
video_id: KzCI6usl5kk
title: "This Pydantic AI feature make browser automation easy"
url: https://www.youtube.com/watch?v=KzCI6usl5kk
watched: 2026-10-03 14:05
source: chrome:Default
indexed: 2026-10-03T12:25:03+00:00
topic: llm-core
---


## Core Concept
Pydantic AI's **harness** abstraction lets you wrap an agent model with composable **capabilities** (tools/skills the agent can invoke), so an agent gains real-world action rather than just reasoning — demonstrated by building an agent that browses MSN.com through a geo-located proxy, delegates per-country research to sub-agents, and writes the collected headlines to a file on the local file system.

## Key Takeaways

- A harness is built around a model plus a list of **capabilities**; three are used in the demo: `browser use`, `file system`, and `sub agents`.
- Web mode is served with `uvicorn`: `uv run uvicorn`, the app object is `app`, host `127.0.0.1`, port `7932`, then open that address in a browser and chat like ChatGPT.
- Model used is **OpenAI GPT-6 Luna**, shared by the main agent and every sub-agent.
- `browser use` capability is configured with:
  - a **browser profile** (holds proxy settings),
  - the **LLM** it drives (same as the agent's model),
  - **`allow_domains`** — a hard allow-list; set to only `msn.com` so it cannot visit anything else,
  - **`headless: False`** — only for debugging so you can watch the Chrome window; the default is `true` and behavior is the same in the background,
  - **`extend_system_message`** — appended instructions: only use MSN.com, don't visit any other website, assume the user has a Japanese IP, prefer MSN because it's local to Japan.
- Geo-localization is done with a proxy, not a language setting: a Japanese IP makes MSN serve the Japanese homepage. Without a proxy the run returned Japanese-market news (typhoon, mayoral race, Japan-US diplomacy).
- Proxy provider used/sponsored: **ProxyCheep** — residential, data center, and mobile proxies worldwide. Order flow: dashboard → **order proxy** → pick type (**static residential** suffices) → **dedicated** → country (e.g. Finland, or drill down to a city) → ISP → number of proxies → time period → **next** → checkout. Credentials appear in the dashboard and are copied with **copy in format**.
- A `browser profile` contains proxy settings; proxy settings need three fields: **server**, **username**, **password**. The copied credential string is split: everything before the colon is the username; drop the trailing colon and `@`.
- **One limitation drives the architecture:** proxy settings live on a single `browser use` instance, so one agent is permanently pinned to one country. Multi-country coverage requires multiple browser-use agents, which requires **sub agents**.
- Sub-agent pattern: the country agent is renamed to a specific `name` plus `description` (e.g. `"japan news researcher"` / "A researcher focused on gathering news from Japan"), then passed into `sub_agents` as a `list` of `sub_agent(...)` instances — "as many agents as you like". In the run, the main agent called **`delegate task`** and expanded into the Austria news researcher.
- Verified country behavior: the Austria sub-agent's Chrome landed on the **German-language** MSN (Austrian version), returning Austrian stories (social assistance, taxes, a journalist's video) — different from the Japan run. A second country means a second proxy credential set.
- `file system` capability is added to the **main** agent's capability list (order relative to `sub agents` doesn't matter) and takes **one important argument: the root directory** — here a folder called `workspace`. Inside that root the agent can create, read, delete, and edit files.
- End-to-end verified run: ask about Japan again and "write the results to a file" → agent completed the browser task, then wrote a file, and reported the path **`Japan MSN headlines.md`**, whose summary matched the chat output.
- The web UI surfaces browser-use steps (and `delegate task` expansion), which doubles as a debug view when the agent does the wrong thing.
- Capability catalog is broader than the demo and includes service integrations added shortly before the video: **Slack, GitHub, Notion, Linear** (transcribed as "Lineer") and more; the point is composing any set of capabilities into a harness for your application's goal.

## Technical Details

- Concepts and entities:
  - **Harness** — the wrapper around a model plus capabilities; capability is the term for the composable pieces (browser use, file system, sub agents, service integrations).
  - **Capability list** — a single list on the agent holding all enabled capabilities.
  - **Browser profile** — browser settings container; the only place proxy configuration is attached.
  - **Proxy settings object** — `server`, `username`, `password`.
  - **Sub agents** — instantiated as a list, each entry a `sub_agent` wrapping an agent.
  - **`delegate task`** — the main agent's call that routes to the appropriate sub-agent.
  - **`extend_system_message`** — extra instructions scoped to the browser-use portion of the harness.
  - **`allow_domains`** — network allow-list constraint.

- Stated trade-offs / constraints:
  - Proxy is pinned per `browser use` instance → one agent = one country; scale to N countries with N agents + sub-agents.
  - `headless: False` is a debugging-only choice; production keeps headless on, since behavior is otherwise identical.
  - Domain allow-listing is a safety boundary the agent cannot exceed.

- Runtime configuration mentioned:
  - Server: `uvicorn`, app object `app`, host `127.0.0.1`, port `7932`.
  - Package manager / runner: `uv`; LLM provider: OpenAI.
  - Write scope root: `workspace` directory.

- Code shapes shown (reconstructed from the walkthrough):

```python
japan_proxy_config = proxy_settings(
    server=...,
    username=...,
    password=...,
)

japan_profile = browser_profile(
    proxy=japan_proxy_config,
)

browser_use(
    browser_profile=japan_profile,
    llm=..., # same model as the agent
    allow_domains=["msn.com"],
    headless=False,
    extend_system_message="...",
)
```

```python
japan_agent = agent(
    name="japan news researcher",
    description="A researcher focused on gathering news from Japan.",
    ...,
)

austria_agent = agent(
    name="austria news researcher",
    description="A researcher focused on gathering news from Austria.",
    ...,
)

main_agent = agent(
    ...,
    capabilities=[
        sub_agents=[
            sub_agent(japan_agent),
            sub_agent(austria_agent),
        ],
        file_system(root="workspace"),
    ],
)
```

- Filesystem output produced by the agent:

```
Japan MSN headlines.md
```

- Verified behavior on a restarted `uvicorn`: Japan prompt → `browse web` → Chrome opens → Japanese MSN homepage → news summary returned. Austria prompt → `delegate task` → Austria news researcher → Chrome opens → German MSN → Austrian stories returned.

## Questions

- What are the exact import paths for `browser use`, `browser profile`, `proxy_settings`, `file_system`, `sub_agents`/`sub_agent`, and `agent` in the Pydantic AI harness package?
- Full API signature of `proxy_settings` and `browser_profile` is never shown — only the three fields and the `proxy=` keyword; unknown what other profile settings exist (viewport, user agent, locale).
- Cost/permission model of the capabilities is unaddressed: whether `file_system` allows writes outside the root, symlink traversal, or path escapes, and whether `browser use` is rate-limited.
- No error handling, retries, timeouts, or failure behavior is shown — what happens if a proxy drops, a site loads slowly, or the sub-agent returns nothing.
- The exact Pydantic AI version is never stated, and the video mentions new capabilities were added "a couple of days ago" — the catalog may have changed since.
- Whether `headless=True` genuinely performs identically (timing, anti-bot detection against MSN) is claimed but not tested.
- Whether a `language`/`Accept-Language` or geolocation browser option exists as an alternative to a paid proxy is not mentioned — the proxy is presented as the only method for forcing the Japanese/Austrian MSN variant.
- No mention of proxy rotation, whether ProxyCheep's static residential is billed per IP or bandwidth, or the price.
- The chat UI's transcript/debug format, persistence, and whether the `Japan MSN headlines.md` write is idempotent on repeat runs are not covered.
- Model name is transcribed as "GPT6 Luna" and cannot be verified from the transcript.
