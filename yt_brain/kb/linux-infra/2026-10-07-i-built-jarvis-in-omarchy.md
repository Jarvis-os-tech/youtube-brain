---
video_id: mrdFgLXiy-o
title: "I BUILT JARVIS IN OMARCHY"
url: https://www.youtube.com/watch?v=mrdFgLXiy-o
watched: 2026-10-07 19:26
source: chrome:Default
topic: linux-infra
indexed: 2026-10-07T14:54:28+00:00
---

## Core Concept

The video is about building "Oma Voice," a Jarvis-like AI voice agent inside Omarchy — the Linux distribution released by DHH roughly two weeks before the talk — by binding an OpenAI GPT Realtime voice model directly to Omarchy's OS-level keybindings and Hyprland's keyboard-driven tiling workspaces, rather than building a voice agent as a web app hosted on Vercel. The central argument is that unlocking the OS (open-source, keyboard-first, source-modifiable) is what makes a genuinely Jarvis-like system possible: "the computer is the application" and the actual OS is the app, so the agent can do anything the keyboard can do.

## Key Takeaways

- Omarchy was released by DHH about two weeks before this talk; it's a Linux distro built on top of Linux, positioned as an "ultimate customizable OS experience" with a polished UI as a starting point.
- The speaker's implementation is called **Oma Voice**; anyone running Omarchy should be able to use the same framework and get a similar result.
- Most prior Jarvis implementations the speaker has seen (on TikTok etc.) are web apps with a voice agent plus tool calling, hosted on **Vercel**. He considers those cool but limited.
- Key rationale: "I'm not hosting some service on top of a computer and an isolated web app. The computer is the application."
- Voice model choice: ChatGPT realtime voice, specifically the **GPT realtime 2.1** model. He says GPT is "still the leader in this category by a lot." Alternatives mentioned and not chosen: OpenCode voice, Eleven Labs.
- He acknowledges a tradeoff: the request goes out to an API server and comes back, and "some people don't like that, which is perfectly fine." He says if he weren't running a potato for a computer, he'd consider something like the Thinking Machines Inkle to run locally.
- The manifest passed to the model lists "all of the key bindings," "all the different actions," and how to interact and execute them — so the agent can do anything the keyboard can do, which is basically the entire OS.
- Hyperland (described as a keyboard-driven tiling manager, "came out I think a couple years ago") is what makes this practical: the agent doesn't need to reason about how things are configured on screen, because Hyprland handles layout in the background. The agent just says "go to workspace two and do this."
- Comparison to **Diction**: he argues Diction is not the right medium because it requires you to speak, review, read, write — a mic-to-textbox-to-Claude-to-read loop. Oma Voice is meant to be "a person-like conversation" and lets him do things "when I'm not looking at my computer."
- Another Omarchy capability he uses: creating any sort of application from a website, done with Chromium by simply opening it. Combined with Hyprland, this lets you pre-package "experiences and views" so the agent can say "pull up this experience" without navigating a Chrome browser to a site. You can also build custom views if you host your own.
- Demo flow, triggered by pressing **super shift V**:
  1. "Hi Oma, how are you doing today?"
  2. Opens **Polymarket** and **x.com** on workspace one.
  3. Switches to **workspace two** and opens the curated newsfeed — stories mentioned: Russia at the G20 and a South African airline flyby.
  4. Opens workspace three, starts **tmux**, types **claude** to launch a Claude Code session, in the documents/dev work directory.
  5. Sends it a prompt to make a neural network for the "make moons" dataset and starts the job.
  6. Switches back to workspace one to scroll the X feed.
  7. Asks it to notify him when the Claude job finishes; it confirms the job is being watched.
- He built new keybindings (specifically to trigger Oma Voice) and "help fill some of the gaps or create new commands essentially that the AI can leverage."
- GitHub repo and the demo are both linked in the video description and chapters.

## Technical Details

- **Architecture**: OpenAI GPT realtime 2.1 voice model → function/tool manifest exposing Omarchy keybindings → OS-level actions resolved by Hyprland tiling → Chromium used as the app surface for web experiences.
- **Why OS-level over web app**
  - Web app on Vercel = isolated service hosted on top of a computer; limited to what the app exposes.
  - Omarchy = open source, so the source can be modified and applications built on top of it.
  - Keyboard-first by design (DHH pre-built bindings), so nearly any part of the OS is reachable by keybindings — which maps cleanly onto a voice agent.
- **Two components combined**: pre-configured Chromium-based web applications + Hyprland tiling. Together they let the agent construct "dynamic experiences" per workspace on demand.
- **Trade-offs / caveats stated by the speaker**
  - Cloud round-trip to the GPT API (not local inference).
  - Dialect: he builds on "make moons," a mis-recognition/verbatim rendering of the scikit-learn **make_moons** dataset.
  - Punctuation artifacts in the demo (e.g. "Huh,", "uh") come from the recorded transcript.
  - Resource constraints: he's "running a potato for a computer," which is why local-model options were rejected.
  - He positions this as "just a version one iteration."
- **Terms referenced**: Omarchy (Linux distro), Hyprland ("Hyperland" in speech, keyboard-driven tiling WM), Diction (dictation-based Claude workflow), Vercel, Chromium, tmux, Claude Code, Polymarket, x.com, Eleven Labs, OpenCode voice, Thinking Machines Inkle.
- Commands/actions demonstrated or named:
  - `super shift V` — launch Oma Voice
  - `tmux` — opened on workspace three
  - `claude` — typed into tmux to start a Claude Code session

## Questions

- What is the exact name of the DHH-developed tiling manager as spelled in the docs — "Hyprland" or "Hyperland"? The transcript consistently says "Hyperland."
- Which Omarchy version and what are the required dependencies/permissions (e.g. audio capture, keybinding interception) for the framework to work on another machine?
- What exactly is "the Thinking Machines Inkle" that could be run locally? The name is ambiguous in the transcript and may be a mis-transcription.
- What are the specific keybindings that ship with Omarchy, and which ones did he add or modify to trigger Oma Voice and fill "gaps"?
- What is the manifest structure — function names, parameter schemas, and how errors/confirmations are handled?
- How does he configure the system prompt, and what guardrails prevent the agent from destructive commands given it can invoke arbitrary keybindings?
- What are the latency characteristics, and how much does a 30-second Claude Code job delay other voice commands?
- Which stories/newsfeed source is the "curated newsfeed" pulling from, and is the curated view a Chromium-wrapped RSS/site or a self-hosted custom view?
- Does the agent require a wake word, or is it strictly the `super shift V` hotkey?
- No latency, cost, accuracy, or reliability measurements are given for the voice model or the tiling automation.
