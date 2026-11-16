---
type: youtube-note
topic: ml-training
video_id: 
source_url: 
tags: [youtube, youtube/ml-training]
---
## Core Concept

The video demonstrates how to generate a customized training dataset from seed vocabulary data using AI, then fine-tune a local LLM model with QLoRA to create a personalized Indonesian tutor that respects the learner's known vocabulary constraints.

## Key Takeaways

- Can bring in GitHub repo, CSV or JSON file, Hugging Face dataset, or PDF document as source data
- Selected "vocabulary seed" CSV with 276 rows of Indonesian/English words (columns: Indonesian, English, category, example, example English)
- Data must be transformed into "instruction and output" or "instruction, input, output" format for fine-tuning
- Used "category" node to generate different task types with weighted distribution: 27% one category, 23% chat, 5% correction
- Created instruction: "You are Carto, Tim's personal Indonesian tutor. Speak simple Indonesian using only vocabulary Tim already knows."
- Used AI generation step with model provider (local model or OpenAI/Anthropic via endpoint and API key)
- Used "AI structured data generator" node to generate training examples
- Configured model preset with Hugging Face model, adjustable temperature for randomness
- Generated input/output format with JSON schema: input (string), output (string), required input/output
- Generated 50-row dataset; estimated ~332 seconds (~5 minutes) on local model, with progress updates every 5 entries
- Can generate 1k or 10k rows; can enable batching, throughput, retries
- In train tab: selected 3.1B instruct Unsloth BNB 4-bit model
- Method: QLoRA; recommends staying with 4-bit as higher methods take long
- Dataset: select local (created recipes) or upload CSV; data format should be instruction, input, output
- Project name: "Indo Training 2"
- Recommended: start with 1 epoch for simple data; standard best practice is 3 epochs
- Other parameters (rank, alpha, dropout, LoRA adapters, hyperparameters): beginners should leave unchanged
- Only epoch directly determines training time
- Training shows VRAM usage, temperature, power, training loss, gradient norm, learning rate
- Learning rate gradually decreases over time
- Training loss is the main graph; expected to decrease over time
- Loss dropping below 1 typically means good performance
- Can compare base model vs fine-tuned model via "compare chat" feature
- Can export model to GGUF (for Ollama), 16-bit inference, or LoRA version

## Technical Details

- QLoRA (Quantized Low-Rank Adaptation) 4-bit training via Unsloth library
- Hugging Face model: 3.1B instruct Unsloth BNB 4-bit model
- Model preset configuration: provider "local model" or OpenAI/Anthropic via endpoint and API key
- Temperature parameter adjustable for randomness in AI generation
- AI structured data generator node with custom prompt specifying:
  - "You are generating one training example for fine-tuning a Indonesian tutor for Tim, a beginner"
  - Hard rule: every Indonesian word in example may only come from known words list
  - English text unrestricted, never use any other Indonesian word except if row type is "new word", use exactly one word from new words pool
  - Style rule: short and friendly
  - Variables embedded: task type, vocabulary card Indonesian, English, example, example English
- Output JSON schema with input (string) and output (string, required) fields
- Training parameters: rank, alpha, dropout, LoRA adapters, hyperparameters (beginners leave unchanged)
- Epoch settings: 1 epoch for simple data, 3 epochs standard best practice; more data may require more epochs
- Training monitoring: VRAM usage, temperature, power draw, training loss, gradient norm, learning rate
- Learning rate gradually decreases over training steps
- Loss value decrease indicates model accuracy improvement; loss below 1 typically signifies good performance
- Compare chat feature to side-by-side base model vs fine-tuned model responses
- Export options: GGUF model (for Ollama), 16-bit inference model, LoRA version
- System prompt can be set during comparison (e.g., "hello, apa kabar" for Indonesian greeting)
- CSV seed data format: columns Indonesian, English, category, example, example English with 276 rows
- Recipe category weights: 27% primary category, 23% chat, 5% correction (and other task types: translate, quiz, new word, correction, daily practice)
- Full run can generate 50, 1k, 10k+ records with batching and retry settings
- Progress updates polled every 5 entries during generation
- Dataset view: instruction, input, output columns after AI assistant column assignment (system=instruction, user=input, assistant=output)
- Make row output should be split into separate input/output rows for proper user/assistant marking

## Questions

- What specific CSV/JSON column mappings work best for the fine-tuning data format?
- How should the "make row" output be properly split into separate input/output rows for proper system/user/assistant marking?
- What exactly determines the optimal epoch count beyond "simple vs complex data" classification?
- How does the vocabulary filtering rule ("every Indonesian word may only come from known words list") enforce constraints during AI generation?
- What are the specific trade-offs between 4-bit QLoRA and higher quantization methods in terms of quality vs speed?
- How does the "new words pool" exception work for "new word" row types during generation?
- What minimum dataset size is needed for effective fine-tuning results?
- What system prompts work best for beginner-level language tutoring scenarios?
- How to properly validate that fine-tuning actually improved the model versus the base model capabilities?
- What are the exact steps to export a fine-tuned model to GGUF and use it with Ollama?
- How does the category weight distribution affect the variety and balance of generated training examples?
<!-- yt-brain:related -->

## Related

- [[youtube/YouTube Knowledge Base|◻️ YouTube Knowledge Base]]
- [[youtube/ml-training|📁 ML Training & Fine-Tuning]]
- [[index|🏛️ JARVIS Memory Vault]]

### Related notes

- [[youtube/ml-training/2026-10-09-how-to-fine-tune-any-ai-model-locally-full-tutorial|How to Fine-Tune any AI Model Locally (FULL Tutorial)]] · relevance 0.91
- [[youtube/dev-craft/2026-11-13-build-your-first-local-ai-agent-python-tutorial-lesson-01-ai|Build Your First Local AI Agent (Python Tutorial) (Lesson: 01) #AIAgent #Gemma4 #Ollama #ai]] · relevance 0.06
- [[youtube/ml-training/2026-10-03-this-tiny-ai-never-stops-learning-mini-agi|This Tiny AI Never Stops Learning (mini-AGI)]] · relevance 0.05
- [[youtube/agents/2026-11-13-fastmcp-python-building-local-agent-tools-step-by-step-lesso|FastMCP & Python: Building Local Agent Tools Step-by-Step (Lesson:9) #ai #mcp #ollama #gemini]] · relevance 0.05

<!-- /yt-brain:related -->
