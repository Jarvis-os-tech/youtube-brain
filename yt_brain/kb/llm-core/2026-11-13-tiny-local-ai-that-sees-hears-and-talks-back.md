---
video_id: 1kLbc_1ibnE
title: "Tiny Local AI That Sees, Hears And Talks Back"
url: https://www.youtube.com/watch?v=1kLbc_1ibnE
watched: 2026-11-09 18:50
source: chrome:Default
topic: llm-core
indexed: 2026-11-13T02:43:45+00:00
---

## Core Concept
LFM3 Omni 2B is a roughly 2.2-billion-parameter open-weights model released October 27 that unifies speech recognition, vision, language modeling, and text-to-speech in one model. Its central design is to place audio and video frames for the same moment adjacent in the input stream, allowing it to answer questions that depend on both what is visible and what is audible, while remaining small enough for local use but with documented weaknesses in tool calling, spoken accuracy, and app-level feature support.

## Key Takeaways
- Liquid says one model replaces four: speech recognition, a vision model, a language model, and text-to-speech; it can look at a photo or video, listen, and answer aloud.
- Released October 27 as open weights at about 2.2 billion parameters.
- On Liquid's own public test of questions about videos with soundtracks, LFM3 Omni scored about 70 versus Qwen's omni model at about 61; Qwen's model is 10.7 billion parameters total. All scores on the model card come from Liquid's own runs, with no independent test available at launch.
- Still images are processed at native resolution, with each 2x2 block of patches becoming one language token.
- Video arrives at 2 frames per second: each pair gets a timestamp, then the two frames, then the sound from that moment, so sight and sound arrive together.
- Because sight and sound arrive together, it can answer questions requiring both, such as what happens and what can be heard in a clip.
- Liquid's examples are a tutor that looks at handwritten math and answers a spoken question, and an in-car assistant combining camera input with driver speech.
- The causal audio encoder starts processing while you are still speaking, reducing wait time after you finish.
- Text and speech output are woven together, so the voice can start before the full answer is written.
- LiquidCodec turns each 80 milliseconds of speech into 12 tokens and decodes about 87 times faster than real time on one CPU thread of an M4 Max.
- In Liquid's Python example, a video comes in without sound unless two flags are enabled; otherwise the model receives frames only.
- The 32,000-token context window must hold the question, media, and answer; each visual frame adds tokens, so long clips require lowering frame rate or capping frames, while the soundtrack is always fully heard.
- On Liquid's table, LFM3 Omni at 2.2 billion parameters leads all three video-with-sound tests against Qwen 3B, listed at 6 billion total parameters, and Gemma 4 E2B at 5 billion parameters, including a test asking who is speaking.
- Those wins are specific to video with sound: on OmniBench, with a still image plus audio clip, it scores slightly below both Qwen omni models.
- English speech recognition is about as good as Qwen's smaller omni model, with about 6 words in 100 wrong.
- Its voice is rated higher than Qwen's, the only rival with a voice score in the table.
- On MMStar, image questions scored about 56 when typed and about 52 when spoken, a roughly 4-point accuracy loss for speaking.
- On Liquid's internal tool-calling evaluation with spoken requests, LFM3 Omni scored about 52 versus Gemma 4 E4B at about 72, a 20-point gap; it also trails Gemma on spoken chat.
- It is a non-reasoning model with no thinking mode; every answer still opens with an empty thinking section.
- App support differs sharply for the same weights: Llama.app's model card says image, audio, and video; Llama.app's own page lists text, images, and audio with no video; Ollama on macOS gives image and audio only; LM Studio gives image only; llama.cpp server supports real-time voice conversations, including tool calls; SGLang gives text only.
- llama.cpp locks video sampling to 2 frames per second, and passing the video frames-per-second flag has no effect.
- The "about one gigabyte" figure refers to the text model, not Omni; Ollama's Omni download is 2.4 gigabytes before context.
- Digital Applied notes that one gigabyte is not a full application budget because encoders, context state, and runtime overhead consume memory; Liquid has not published a running memory figure for Omni.
- Llama.app lists its 8-bit build as needing a machine with 8 gigabytes of memory or more; Liquid's Python Transformers documentation recommends a GPU; the laptop and phone route is the compressed llama.cpp build.
- Licensing is Apache-based but free commercial use is capped at 10 million dollars of annual revenue, counting parent companies and affiliates under common control.
- Internal research, testing, and evaluation are permitted without a commercial license, but using the models in everyday business operations can still count as commercial use even if not directly revenue-generating.
- Liquid's launch post does not mention the license; crossing the 10-million-dollar threshold requires a separate commercial license.

## Technical Details
- Input ordering: still images at native resolution, each 2x2 patch block becomes one language token; video at 2 fps as timestamp, two frames, then that moment's sound.
- Context budget: 32,000 tokens total for question, media, and answer; visual frames add tokens, so long videos use fewer frames but never less audio.
- Output: text and speech are woven together; LiquidCodec encodes 80 ms of speech into 12 tokens.
- Reported decode speed: about 87 times faster than real time on one CPU thread of an M4 Max.
- Audio input behavior: causal audio encoder begins processing during speech; Python example requires two unnamed flags to include video sound.
- Benchmark and evaluation figures:
  - Liquid's video-with-soundtrack QA test: about 70 versus Qwen omni at about 61.
  - OmniBench: slightly below both Qwen omni models.
  - English ASR: about 6 words per 100 wrong.
  - MMStar: about 56 typed versus about 52 spoken.
  - Internal tool-calling with spoken requests: about 52 versus Gemma 4 E4B at about 72.
- Compared model sizes on Liquid's table: LFM3 Omni 2.2B, Qwen 3B listed at 6B total, Gemma 4 E2B at 5B, Gemma 4 E4B at about 72 on tool calling.
- Deployment behavior by app:
  - Llama.app model card: image, audio, video.
  - Llama.app own page: text, images, audio, no video.
  - Ollama on macOS: image and audio only.
  - LM Studio: image only.
  - llama.cpp server: real-time voice conversations, including tool calls; video sampling fixed at 2 fps.
  - SGLang: text only.
- Memory and hardware:
  - About 1 GB figure is for the text model, not Omni.
  - Ollama Omni download: 2.4 GB before context.
  - Llama.app 8-bit build: machine with 8 GB memory or more.
  - Python Transformers documentation: GPU recommended.
  - Laptop and phone route: compressed llama.cpp build.
- License terms:
  - Apache-based terms.
  - Free commercial use capped at 10 million dollars annual revenue.
  - Entity definition includes parent companies and affiliates under common control.
  - Internal research, testing, and evaluation permitted without commercial license.
  - Everyday business operations may count as commercial use even without direct revenue generation.
  - Separate commercial license required at or above the 10-million-dollar threshold.

## Questions
- What are the two flags in Liquid's Python example that enable audio for video input?
- What exact llama.cpp server command and flags are shown on screen for the real-time voice setup?
- What is Omni's actual runtime memory requirement, since Liquid has not published a running memory figure?
- How does the model perform on independent benchmarks rather than Liquid's own runs?
- Does Llama.app actually support video input despite the discrepancy between its model card and its own page?
- What is its tool-calling performance with typed rather than spoken requests?
- Does it support languages other than English for speech recognition or speech output?
- What latency or resource requirements apply to the real-time voice conversation mode?
