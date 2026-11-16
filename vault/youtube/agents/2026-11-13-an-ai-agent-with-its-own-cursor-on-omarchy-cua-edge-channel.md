---
video_id: sNE7mJKa69M
title: "An AI Agent with Its Own Cursor on Omarchy (Cua, Edge Channel)"
url: https://www.youtube.com/watch?v=sNE7mJKa69M
watched: 2026-10-25 22:23
source: chrome:Default
topic: agents
indexed: 2026-11-13T02:59:22+00:00
type: youtube-note
source_url: https://www.youtube.com/watch?v=sNE7mJKa69M
tags: [youtube, youtube/agents]
---


## Core Concept

Cua is an open-source driver that lets an AI agent see the apps on your screen and operate them by sending clicks and keystrokes, while the AI model — here Codex, signed in with a ChatGPT plan — decides each step. With an extra Hyprland plugin, the agent gets a cursor of its own, so it can work in one window while you keep typing in another. The setup is experimental: the plugin is currently only on Omarchy's edge channel, and it pins Hyprland to one exact version, so it's meant for a spare machine rather than a daily driver.

## Key Takeaways

- Install on Omarchy (edge channel) entirely via `pacman` from a terminal: adds the Cua driver, its Hyprland plugin, and Inkscape.
- Before granting software this much control, have an AI coding agent read through Cua's source code first.
- The plugin needs a fresh session, so restart before continuing.
- First command loads the plugin into Hyprland; a small settings file switches the plugin's input on so the agent can click/type through it; reloading Hyprland settings applies the file.
- Cua sends usage data by default (described as content-free); disable with `KUA driver telemetry disable`.
- Cua has no intelligence of its own — it reads the screen and sends clicks/keys while the model decides. Any MCP-capable agent can drive it; here that's Codex on a ChatGPT plan, with no separate Cua account, and usage counts toward that plan.
- Add the driver to Codex as a tool; Codex also needs a few session settings. The written guide on starryhope.com has those plus the Hyprland settings file.
- Foreground mode: the agent uses your real pointer/keyboard. Prompt: take over the Chromium window and open the Wikipedia article on Inkscape.
- Before its first click, Codex shows an approval prompt for the driver's click tool; allow it for the session.
- First click is refused because the Enter key used to approve is still held; after a ~2-second wait (as the prompt requests), the second click is accepted.
- A pink arrow over the address bar marks where the agent is working; it typed the new URL after the old one (Chromium couldn't reach the site), then Codex saw the error and retyped the whole address, opening the article.
- A held key or mouse button makes the driver refuse any foreground step — keep your hands off.
- Background mode: the agent works with its own cursor and leaves yours alone.
- A single click in Chromium is refused with `background unavailable. Client not qualified.` — Chromium isn't on the driver's background-input allowlist; on this desktop only Inkscape is.
- `Super` is the Windows key; `Super+Shift+2` sends Codex to the second workspace, where Inkscape and Omarite (a writing app) are already open.
- Prompt requests a blue rectangle, a blue circle, and the words "starry hope"; background actions only; never focus Inkscape or move your pointer.
- While typing in Omarite, the agent draws the rectangle then the circle (pink-arrow cursor), selects both shapes and sets one blue fill for the pair, moves the rectangle fully onto the page, and adds "starry hope" in the same blue.
- Omarite keeps focus the whole time and no keystroke is lost; the drawing took 1 minute 46 seconds (sped up in the video).
- While the plugin is installed it pins Hyprland to one exact version, so system updates can fail — experiment on a spare machine.

## Technical Details

- Architecture: Cua reads the screen and sends clicks/keys; the AI model decides each step; integration is via MCP.
- Apps involved: Inkscape (drawing), Chromium (browser), Omarite (writing app), Codex (agent), Hyprland (compositor/window manager).
- Install path: `pacman` on Omarchy's edge channel.
- Telemetry toggle: `KUA driver telemetry disable`.
- Plugin activation: load into Hyprland, enable input via a settings file, reload Hyprland settings.
- Agent wiring: driver added to Codex as a tool; extra Codex session settings required (in the guide).
- Workspace navigation: `Super+Shift+2` (Super = Windows key).
- Error string: `background unavailable. Client not qualified.`
- Visual marker for agent activity: pink arrow cursor.
- Timing: ~2-second wait between refused/accepted foreground click; 1 minute 46 seconds for the Inkscape drawing.
- Safety notes: foreground steps refused while any key/button is held; background input only works on allowlisted apps (Inkscape here).

## Questions

- What is the exact `pacman` command and package names? (The video refers to "this command" without showing it in the transcript.)
- What are the full contents of the Hyprland settings file and the Codex session settings? (Referenced as being in the guide on starryhope.com.)
- Which apps besides Inkscape are on the driver's background-input allowlist?
- How do you handle Hyprland updates while the plugin pins it to one exact version?
- Does foreground mode work in apps other than Chromium?
- What exactly does Cua's telemetry send, and is it truly content-free?
- What happens if the agent's cursor and the user's interact during background mode?
<!-- yt-brain:related -->

## Related

- [[youtube/YouTube Knowledge Base|◻️ YouTube Knowledge Base]]
- [[youtube/agents|📁 AI Agents & Orchestration]]
- [[index|🏛️ JARVIS Memory Vault]]

### Related notes

- [[youtube/llm-core/2026-11-13-i-gave-chatgpt-claude-and-codex-one-shared-brain|I Gave ChatGPT, Claude and Codex One Shared Brain]] · relevance 0.09
- [[youtube/linux-infra/2026-10-07-i-built-jarvis-in-omarchy|I BUILT JARVIS IN OMARCHY]] · relevance 0.08
- [[youtube/linux-infra/2026-11-13-omarchy-explained-a-deep-dive|Omarchy Explained: A Deep Dive]] · relevance 0.08
- [[youtube/agents/2026-11-13-the-secret-to-advanced-ai-multi-step-reasoning-explained-les|The Secret to Advanced AI: Multi-Step Reasoning Explained (Lesson: 2) #Gemma4 #ollama #ai #ajagent]] · relevance 0.07

<!-- /yt-brain:related -->
