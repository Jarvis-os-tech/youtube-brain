---
video_id: 3utOGJsj9ko
title: "I Trusted Omarchy’s AI With My Linux Desktop"
url: https://www.youtube.com/watch?v=3utOGJsj9ko
watched: 2026-10-04 07:23
source: chrome:Default
indexed: 2026-10-04T02:32:52+00:00
topic: linux-infra
---


## Core Concept

The video hands an OpenAI Codex agent full control of an Omarchy Linux desktop running inside a virtual machine and stress-tests it across three challenges — cosmetic customization, a security audit of a listening web service, and diagnosing a deliberately broken systemd service — all under one rule: never trust the agent's claims, verify every change, every security claim, and every fix. The conclusion is nuanced: the agent proved genuinely capable and appropriately conservative, but the author still wouldn't grant it unrestricted access to a real workstation without backups, validation, and a rollback path.

## Key Takeaways

- **Test environment:** Omarchy runs in a VM on a Windows main machine; the agent is OpenAI Codex, connected to Omarchy via **Setup → Default Agent → Codex**.
- **Agent setup is trivial:** Omarchy asks only for an API token or username/password for ChatGPT, Claude, or Gemini — whatever backend you use.
- **Agent configuration lives in a Markdown file:** an `omarchy-agent-prompt.md` (transcribed as "omachi agent prompt") in the **controlled-chaos-linux-lab** repo, holding every prompt used in the video plus **eight additional example prompts** for viewers who want to try more.
- **Evaluation criteria (three questions per challenge):** Did the AI understand the request? Did the result actually work? How much help did it need from the user?
- **Challenge 1a — appearance:** asked for slightly rounder window corners, a clear blue border around the focused window, a slightly larger gap between windows, and a redder wallpaper. The agent backed up the original config, validated the new settings, and **reloaded Hyprland without restarting the session** — the session survived.
- **Challenge 1b — CPU/memory widget:** nothing existed in the taskbar, so the agent **designed a widget that updates every 2 seconds**, now visible in the top-right corner. This task took noticeably longer than expected but still succeeded with backup + validation.
- **Challenge 2 — security inspection:** a deliberately trivial Python web server on **port 8000**, bound to loopback. Prompt: inspect temporary web services on port 8000, accessible inside the VM but not from other machines. The agent inspected running processes, checked network configuration, and correctly concluded the server was **already restricted to localhost on 127.0.0.1** — it did *not* blindly edit firewall rules.
- **Verification of the security claim:** the agent supplied a copy-pasteable test command, run from **PowerShell on the Windows host**, which returned a **connection timeout** — proving the service is unreachable from outside the VM.
- **Honest scoping:** the check only covered **IPv4**. IPv6 was explicitly not verified and deliberately left out of scope.
- **Challenge 3 — broken service:** a second Python web service on **port 8765**, deliberately broken by the author. The agent found a **nonexistent path reference** in the unit file — `user/bin/python3/intentionally-missing` instead of the correct `user/bin/python3` — and fixed it. The service went from "failed to connect" to "omachi-demo service security test is passed."
- **Prompt hygiene pays off:** the demo-3 prompt contains a placeholder for the service name. On the first (pre-recorded) run the agent **asked the user for the service name**; on the recording-day run it had inferred `omachi-demo-service` from earlier context and never asked.
- **Demos are organized in the prompt file** as Demo 1 (sections A1 and A2) and Demo 2 (single section), each followed by setup instructions and the verbatim prompt.
- **Author's verdict:** genuinely impressed; the value of an agent isn't just executing commands, it's understanding the system, changing only what's necessary, and knowing when to leave things alone — but no unrestricted access to the main workstation.

## Technical Details

- **Agent backend selection:** Omarchy's menu exposes a single "default agent" entry; selecting Codex requires credentials for the model provider (ChatGPT / Claude / Gemini), not Omarchy-specific setup.
- **Configuration safety pattern the agent follows unprompted-ish:** back up the original file → write the new value → validate it → reload only the affected component (Hyprland reload, not session restart).
- **Widget implementation:** a desktop-bar widget polling system stats on a **2-second** interval.
- **Network exposure surface under test:**
  - Demo 2: Python web server, **port 8000**, loopback-only, verified unreachable from the host.
  - Demo 3: Python web server, **port 8765**, started via a systemd unit whose `ExecStart` path was corrupted.
- **Verification commands surfaced by the agent:**
  - Reachability test from Windows PowerShell (agent-provided, expected to time out):
    ```powershell
    # agent-supplied connectivity test — expected result: connection timeout
    ```
  - The agent's own inspection path: enumerate running processes → inspect network configuration → determine the listening socket's bind address (`127.0.0.1`).
- **Deliberate breakage (author's own sabotage):** a systemd unit pointing at a nonexistent interpreter path:
  ```
  user/bin/python3/intentionally-missing     # broken (author's sabotage)
  user/bin/python3                            # correct path the agent restored
  ```
- **Referenced files and paths:**
  - `omarchy-agent-prompt.md` — lives in the **controlled-chaos-linux-lab** repo; contains all demo prompts plus 8 extra examples.
  - Agent UI path: **Setup → Default Agent → Codex**.
- **Trust requirements the author insists on for any agent with system access:**
  - Backups of every config file it touches
  - Validation that the change actually took effect
  - A plain-language explanation of root cause on every fix
  - Explicit, clear rollback/undo instructions
- **Trade-offs observed:**
  - Small cosmetic tasks are trivially verifiable; security claims and broken services are the real test — and the gap between "thinks it's fixed" and "verifiably fixed" is where an agent earns trust.
  - Verification is often *outside* the VM (PowerShell on the Windows host), so a complete audit spans more than the agent's own environment.
  - IPv4-only testing leaves a real gap; a service safe on IPv4 loopback can still be exposed via IPv6.
  - The prompt file doubles as documentation and as a lever that reduces agent round-trips (the service-name question disappeared once the name was in context).

## Questions

- Which exact Hyprland config keys did the agent modify for rounded corners, focus border color, and window gaps? The video never names them.
- What tool did the agent use for the CPU/memory widget (e.g. `eww`, `waybar` module, `catpuck`/`sysinfo` script), and where was it installed?
- Which commands did it run to validate the widget and the appearance changes — was that visual, or a config parse/lint check?
- Was the port 8000 service's binding verified from a second host, or only from the Windows box? Only the Windows-side timeout is shown.
- Was IPv6 exposure checked at all? The author explicitly skipped it, so `::1` vs `0.0.0.0`/`::` behavior remains unverified.
- Was the port 8765 service also loopback-only, and did the agent confirm that after fixing the path?
- How long did each challenge take? The video mentions "a few seconds or a minute" and "a few minutes" but gives no measured timings.
- What was the exact prompt text used for the PowerShell reachability test? It was copied from screen but never spoken or shown in full text.
- Does the Omarchy agent integration run Codex with full `sudo`/root access, and is there any sandboxing or approval prompt before commands execute?
- What does the agent do when it guesses wrong (as with the inferred service name) — is there a confirmation step before it edits a systemd unit?
- The author mentions cutting portions where things "need more time to process" — were any failures or corrections edited out of the final video?
- Were the eight extra example prompts validated, or offered untested as starting points?
