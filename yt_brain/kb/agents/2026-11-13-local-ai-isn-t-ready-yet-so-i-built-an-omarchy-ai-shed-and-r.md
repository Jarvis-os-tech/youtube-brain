---
video_id: MdST_zkfO8I
title: "Local AI Isn't Ready Yet - So I Built An Omarchy AI Shed And Run Claude From My Phone"
url: https://www.youtube.com/watch?v=MdST_zkfO8I
watched: 2026-10-30 21:47
source: chrome:Default
topic: agents
indexed: 2026-11-13T02:52:05+00:00
---

## Core Concept
The video argues that local AI is not yet ready for serious development work—open-weight models lag far behind cloud models in intelligence while requiring expensive hardware—so the speaker instead built a cheap "AI shed" (a Ryzen 9 5950X box assembled from scavenged parts) that runs cloud-based agents (Claude and Codex) and is managed remotely from a phone, letting long-running tasks churn unattended while the speaker works elsewhere. A later segment shows an experiment where an AI agent was given the script to *Das Boot* and built a game, reiterating that local AI needs strong justification, is fun to experiment with, but is not suitable for the speaker's everyday needs and still requires manual human testing, with remote work done through open chats and Tailscale.

## Key Takeaways
- The speaker's normal workflow: cloud Claude edits the repository, generates code, compiles and runs it, reviews tests, and iterates on test failures and specs; cloud side plus local PC.
- The speaker's older box has 16 cores/32 threads but only 32 GB RAM, which becomes a bottleneck under multiple tasks.
- An intelligence comparison shows Claude Opus 5.5 at AA index 55 (coding 60) and "Astra" at 53, while the nearest open-weight models (Memo, TML, Deep Seek, Step 5 preview) sit at 46.
- Local hardware options quoted: a 64 GB PC with an RTX 5016 runs "quaint" (index 34); Strix Halo (120 GB) runs a 90 GB model (index 40); a 512 GB unified Mac runs the aggressively compressed Mimo (index 46); RTX Pro pricing is described as insane.
- A GPU card alone is quoted around 15,000; a local system plus Claude in the cloud is around 2,000; reaching top intelligence with local compute is quoted at 17,000–18,000.
- The speaker's 5-year math: a 2,000-pound computer plus 190 pounds/month Claude Max takes 81 payments (6–7 years) to equal 17,000 pounds.
- Local AI is described as "pants"—roughly ChatGPT 3/4 era—fine for basic tasks but not for C++/graphics-heavy development.
- Valid reasons to run AI locally: businesses that cannot go online, simple bots, image work (e.g., Flux), and basic parity tasks.
- The speaker runs Claude Max and Astra accounts at about 190 pounds/month each and rarely hits limits.
- The "AI shed" is a Dell 8950 replacement: Lian case, Ryzen 9 5950X (~300 quid, AM4/DDR4), 64 GB scavenged DDR4 RAM, old SSDs, an old 750 W Rampage PSU, fans, and a motherboard chosen by AI; uses an Intel Arc B580 for Vulkan work. 16 cores/32 threads.
- Hardware depreciates sharply (quoted examples: 40,000-pound Mac Pro, 7,000-pound Mac "trash can" now ~300 quid; RTX 3090 24 GB cards flying off shelves).
- Omarchy 4.5 release candidate is available with many features; Glyphs (remote machine control via remote desktop) is highlighted as a game changer.
- Machines are connected over Tailscale; the speaker built a Glyphs manager switching between "Colossus" and "Guardian".
- Guardian runs Herder; a WWII U-boat game is being built there with Codex using goals (pause/resume), code checks, and open chat windows.
- Remote control: Codex sessions are exposed via a Codex server (paired with "Hamachi") and appear on paired devices including the ChatGPT phone app; Claude uses `/rc` to continue a session remotely, visible in the Claude mobile app.
- Unattended operation: tasks can be left running, with image/video proof sent to the phone and notifications keeping the speaker updated.
- Shortcuts: `CX` runs Codex unrestricted; `CDX` runs Codex in "yellow mode"; Claude requires typing `RC` before leaving.
- The speaker is replacing OBS with "Omegacaster", built with FFmpeg 9.1 and written via Omarchy/Archie, expected within weeks.
- Token discipline: Fable is used only for planning; Codex high and Opus 5.5 are not used for everything.
- The AI was given the script to *Das Boot* and created a game, with only the last bits remaining; the speaker hopes to publish the game shortly.
- Steam pushed out version 3.9.5, and the speaker needs to work with Nvidia drivers on Steam.
- The speaker must wait for the over-the-air ISO update before redoing the Nvidia Steam installer.
- Once the ISO is available, the speaker can assemble the ISO and fold the Nvidia loaders back in, then distribute it.
- The main takeaway is that you really need good reasons to do local AI; it is fun to experiment with, but not suitable for the speaker's needs.
- Setting up a rig like this is described as easy, with "no magic."
- "Glyph manager" is mentioned, with a requirement of 4.5 or "Mach 4.5."
- "Mach" is described as a perfect environment that is geared up for this kind of work.
- Tailscale is strongly recommended; it is described as free with one seat and as many machines as you want to attach, allowing the entire network to talk to each other.
- The speaker leaves a couple of chats open so projects can be started on the go, such as while on the tube or Overground to Hampstead Heath.
- By the time the speaker returns, about half the project may be built, but manual human testing is still required.

## Technical Details
- Workflow architecture: cloud AI (Claude/Codex) performs planning/coding; the local "AI shed" handles compilation and execution; remote access via Tailscale + Glyphs remote desktop; Codex server exposes sessions to paired devices; Claude remote control via `/rc`.
- Tools/commands/platforms mentioned:
  - Amasha (presentation tool), Marqo 4.5 (release candidate), Omarchy 4.5, Glyphs, Tailscale, Herder, Codex, Codex server, "Hamachi", ChatGPT mobile app, Claude mobile app, `/rc`, `CX`, `CDX`, OBS, Omegacaster, FFmpeg 9.1.
  - Glyph manager, Mach 4.5, Steam, Nvidia drivers, over-the-air ISO update.
- Hardware specifics:
  - Older box: 16 cores / 32 threads, 32 GB RAM.
  - AI shed: Ryzen 9 5950X, AM4, DDR4, 64 GB RAM, old SSDs, 750 W Rampage PSU, Lian case, Intel Arc B580 (Vulkan), fans.
  - Local AI targets: RTX 5016, Strix Halo (120 GB, 90 GB model), RTX Pro, 512 GB unified Mac.
- Intelligence indices: Claude Opus 5.5 = 55 (coding 60); Astra = 53; open-weight nearest = 46; "quaint" = 34; Strix Halo path = 40; Mimo (Mac) = 46.
- Costs/numbers:
  - GPU card alone ~15,000; local+cloud system ~2,000; full local compute+intelligence ~17,000–18,000.
  - Claude Max ~190 pounds/month; 2,000 + 190/month = 81 payments ≈ 6–7 years to reach 17,000.
  - 5950X ~300 quid (down from 700–800); Mac "trash can" 7,000 quid now ~300; Mac Pro up to 1.5 TB ~40,000; 50,000-pound render jobs.
  - 3D analogy: 720×576 frames, 5 minutes–1 hour each, 750 frames = 31 days on one box; render farm returns in ~6 hours.
- Machine names: Colossus (this machine), Guardian (the shed).
- Steam version mentioned: 3.9.5.
- Tailscale is described as free with one seat and unlimited machine attachments, enabling network-wide communication.
- Workflow described: leave chats open, start a project or research remotely, then manually test the result.
- No code, commands, or file paths appear in the second transcript excerpt.

```text
codex server
/rc
CX
CDX
```

## Questions
- The speaker never names the processor in the first (older) box ("I can't remember the name").
- Whether Omarchy 4.5's Glyphs will ship with a built-in machine manager is unknown; the speaker built their own.
- The exact pairing mechanism referred to as "Hamachi" for exposing Codex sessions is unclear and worth verifying.
- The meaning of Codex "yellow mode" (triggered by `CDX`) is not explained.
- The precise Intel Arc model name is stated inconsistently ("B58B"/"B580").
- Whether "Astra" refers to a specific product (and its exact pricing/tier) is not clarified.
- The release timeline for Omegacaster ("a few weeks") is vague, and part 2 presumably continues the walkthrough.
- What exactly is meant by "Glyph manager" and "Mach 4.5," and is "Mach" a transcription of "Omarchy"?
- What specific ISO, Nvidia loader, and installer process is being redone for Steam?
- What is the game based on *Das Boot*, and where will it be published?
- What hardware or machine specs are used for the local AI rig?
- How is phone access to the AI workflow implemented beyond leaving chats open?
- What parts of the workflow still require manual human testing?
