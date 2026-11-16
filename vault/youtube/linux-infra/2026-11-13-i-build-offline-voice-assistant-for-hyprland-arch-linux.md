---
video_id: c1gC5tU3_YM
title: "I Build Offline Voice Assistant For Hyprland + Arch Linux"
url: https://www.youtube.com/watch?v=c1gC5tU3_YM
watched: 2026-10-25 22:17
source: chrome:Default
topic: linux-infra
indexed: 2026-11-13T03:01:56+00:00
type: youtube-note
source_url: https://www.youtube.com/watch?v=c1gC5tU3_YM
tags: [youtube, youtube/linux-infra]
---


## Core Concept
An entirely offline, open-source, free voice assistant for Hyprland on Arch Linux that records audio on a keybind, transcribes it with Whisper, converts the transcription into a JSON command using a local LLM via Ollama, executes the action through a Python script using hyprctl, and replies with synthesized speech via Piper.

## Key Takeaways
- Demoed capabilities include navigating to workspaces, opening Discord, launching VS Code, opening YouTube, and moving windows.
- The assistant is still a work in progress; planned additions include a quick shell widget for visual feedback and the ability to run terminal commands.
- Trigger: hold `super A` to start recording; releasing the key sends the audio to Whisper for transcription.
- Whisper was installed from the AUR and a key bind was added to the Hyprland configuration.
- The first LLM tried was "Gwen 3" with 4 billion parameters via Ollama; it overthought, pushed CPU temperatures to 83°C, and took about 2 minutes to produce correct JSON, so the speaker switched to Gemma 3 with 1 billion parameters for speed.
- `take_action.py` was created to execute commands; its first failure was a syntax error.
- Piper was installed from the AUR with a voice model; the first package was wrong and had to be reinstalled by specifying it.
- The first Piper voice sounded male despite the speaker wanting a female voice; switching models fixed this.
- Gemma 3 with 4 billion parameters was used to generate natural responses, with error logging that saves failures and clears logs when the assistant starts.
- Installation of the 4B model was slow, so it was temporarily tested with Gemma 3 1B plus a detailed system prompt.
- The 1B model hallucinated significantly, so the speaker switched back to Gemma 3 4B, which produced noticeably better responses.
- Occasional misheard input was attributed to the microphone not being properly tuned.
- The repository link is promised in the video description.

## Technical Details
- Architecture pipeline: audio recording → Whisper transcription → LLM (Qwen/Gemma via Ollama) → JSON command → Python + hyprctl execution → Piper voice response.
- Trigger and config: key bind in the Hyprland configuration using `super A` (hold to record, release to transcribe).
- LLM trade-offs: Qwen 3 4B produced correct JSON but was slow and hot (CPU ~83°C); Gemma 3 1B was fast but hallucinated; Gemma 3 4B gave the best response quality.
- Execution component: `take_action.py`.
- Voice synthesis: Piper installed from AUR; voice model selection affected perceived gender of output.
- Logging: errors are saved automatically and logs clear when the assistant starts.
- Dependencies mentioned: Whisper (AUR), Ollama, Piper (AUR), Python, hyprctl.

## Questions
- Which exact Whisper model and size were used, and what transcription accuracy/latency was achieved?
- What are the exact Hyprland keybind and recording commands in the configuration?
- What is the JSON command schema the LLM is expected to output?
- What caused the initial runtime error revealed by manual execution, beyond the syntax error in `take_action.py`?
- Which specific Piper voice model packages were tried and finally selected?
- How is the microphone tuning supposed to be fixed, and what tool/settings are involved?
- What are the hardware specs (CPU/GPU/RAM) and whether GPU acceleration is used for Whisper/Ollama/Piper?
- Where is the repository link, and does it include setup instructions and the prompts used?
<!-- yt-brain:related -->

## Related

- [[youtube/YouTube Knowledge Base|◻️ YouTube Knowledge Base]]
- [[youtube/linux-infra|📁 Linux & Infrastructure]]
- [[index|🏛️ JARVIS Memory Vault]]

### Related notes

- [[youtube/dev-craft/2026-11-13-jarvis-mlx-an-open-source-bare-bones-python-voice-assistant|JARVIS MLX - An open source bare-bones python voice assistant optimized for Mac.]] · relevance 0.20
- [[youtube/dev-craft/2026-11-13-i-built-a-python-sdk-for-ai|I built a Python SDK for AI]] · relevance 0.13
- [[youtube/agents/2026-11-13-fastmcp-python-building-local-agent-tools-step-by-step-lesso|FastMCP & Python: Building Local Agent Tools Step-by-Step (Lesson:9) #ai #mcp #ollama #gemini]] · relevance 0.13
- [[youtube/linux-infra/2026-10-07-i-built-jarvis-in-omarchy|I BUILT JARVIS IN OMARCHY]] · relevance 0.12

<!-- /yt-brain:related -->
