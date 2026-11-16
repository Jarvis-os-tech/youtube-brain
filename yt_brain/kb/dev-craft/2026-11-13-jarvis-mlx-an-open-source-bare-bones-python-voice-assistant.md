---
video_id: _SB1Nl4LAV4
title: "JARVIS MLX - An open source bare-bones python voice assistant optimized for Mac."
url: https://www.youtube.com/watch?v=_SB1Nl4LAV4
watched: 2026-11-02 20:59
source: chrome:Default
topic: dev-craft
indexed: 2026-11-13T02:44:39+00:00
---

## Core Concept
JARVIS MLX is a bare-bones, fully offline Python voice assistant optimized to run on Apple Silicon (M1/M2/M3), including low-resource machines like an 8GB MacBook Air, combining a quantized mlx Whisper for speech-to-text, a quantized Phi-3 (3.8B) language model, and Melo TTS for speech output, all orchestrated from a single `main.py`.

## Key Takeaways
- The repo is optimized for Mac/Apple Silicon and is intended to run offline on M1/M2/M3 chips, including MacBook Air.
- Speech-to-text uses Whisper V3 via the mlx-optimized, quantized version, plus a voice activity detection component that records detected speech into a queue.
- The default LLM is Phi-3 (3.8B parameters, ~2.1GB at 4-bit mlx quantization), chosen so it runs on machines with as little as 8GB RAM; it can be swapped for other mlx-community models on Hugging Face (e.g., Gemma, Mistral instruct v2 ~14GB) with more research.
- Text-to-speech uses Melo TTS (by MyShell), stripped down to English-only inference; it supports custom voices via a speaker ID and can be fine-tuned on your own dataset.
- Melo TTS is the only part not optimized for mlx — it uses PyTorch/MPS — and rewriting ~10 files would be needed; PRs are welcome.
- The assistant loop: a listening task records audio into a queue; a transcribe loop, when not speaking, processes queued voice data, transcribes it, appends a user message to history, generates an LLM reply with configurable temperature and max tokens, appends the assistant reply, speaks it, sleeps 1 second, then toggles listening back on.
- Setup: `pip install -r requirements.txt` (requirements split into ML libraries, testing/misc, Melo TTS niche libs, and audio libs); mlx must run natively in a Python environment (e.g., conda).
- There is a known bug requiring code at the bottom of `main.py` to avoid an error; fixing it is the project's "first bounty."
- The master prompt is ~253 characters instructing the model to act like JARVIS; keep it short because the small model struggles with huge/complex tasks.
- TTS output is processed with librosa to strip silences, played as a numpy array without saving to disk; speaking speed defaults to 0.95 and sdp ratio adjusts pitch.
- Future plans: train a custom voice model, fine-tune Phi-3, add a basic browser-based (HTML) UI, and possibly move training code to a separate repo.

## Technical Details
- Core files: `main.py` (all basic logic), `test/` (tests), `stt/` (Whisper mlx + VAD), `mellow/` (Melo TTS, inference-only).
- LLM generation parameters include `temperature` and `max_tokens` (default 100, roughly ~25 words); increase for longer completions.
- History is a list of messages with `role` ("assistant"/"user") and `content`; history is flattened to one string and passed to the model followed by an assistant tag.
- Melo TTS generates at 44.1 kHz; the speaker mentions 16,000 Hz might suffice but current quality is 44.1k.
- Blocking audio playback means the code waits for speech to finish; a 1-second sleep is added as a cleanup buffer due to OS/Python audio lag.
- Melo TTS niche libs and audio libs are separated in `requirements.txt` from core ML and testing dependencies.
- Model swap path: Hugging Face → mlx community → choose model (e.g., Gemma, Mistral instruct v2); larger models need more powerful hardware (e.g., M1 Max for ~14GB Mistral).

```python
# Conceptual flow from main.py
# listening task records audio into a queue
# transcribe loop:
if listening_mode and voice_data_available:
    stop_listening()
    transcript = transcribe(queued_audio)
    history.append({"role": "user", "content": transcript})
    prompt_text = flatten(history) + master_prompt
    response = llm.generate(prompt_text, temperature=..., max_tokens=100)
    assistant_reply = extract_assistant(response)
    history.append({"role": "assistant", "content": assistant_reply})
    speak(assistant_reply, speaker_id=..., speed=0.95, sdp_ratio=..., quiet=True)
    # librosa strips silences; played as numpy array
    sleep(1)
    toggle_listening()
```

```text
# requirements.txt categories (per transcript)
# machine learning libraries
# miscellaneous / testing libraries
# Melo TTS niche libraries
# audio libraries
```

## Questions
- What is the exact "weird bug" requiring code at the bottom of `main.py`, and what is the bounty/fix?
- What are the precise VAD sensitivity settings and where exactly to adjust them?
- What is the exact librosa decibel threshold used to strip silences?
- Which specific mlx Whisper variant/model ID is used, and is it V3 large or a smaller variant?
- How does the custom voice training and Phi-3 fine-tuning actually work (training code not yet in repo)?
- Is there a concrete plan/timeline for the browser-based UI beyond "maybe"?
- What Python version and conda setup steps are required (not detailed in transcript)?
