---
video_id: 4JofSJIrjwU
title: "How to Fine-Tune any AI Model Locally (FULL Tutorial)"
url: https://www.youtube.com/watch?v=4JofSJIrjwU
watched: 2026-10-09 18:18
source: chrome:Default
topic: ml-training
indexed: 2026-10-09T15:42:31+00:00
---

## Core Concept
The video demonstrates how to generate a customized training dataset from seed vocabulary data using AI, then fine-tune a local LLM model with QLoRA to create a personalized Indonesian tutor that respects the learner's known vocabulary constraints.

## Key Takeaways
- Unsloth Studio is a free, open-source graphical UI for fine-tuning that runs locally without internet
- LoRA adapter layers are trained on top of the base model and comprise less than 1% of the base model's size
- QLoRA uses a quantized (4-bit) version of the base model, shrinking a 16 GB model to 5–7 GB
- Windows requires an Nvidia GPU with ideally 12 GB VRAM or more; Mac needs a modern M-series with 24–64 GB unified RAM
- Low-end hardware can use a free Google Colab notebook from Unsloth
- Model format must be MLK or safe tensors; GGUF format is not supported for fine-tuning
- Llama 3.1 8B instruct Unsloth BNB 4-bit is a 6 GB model suitable for mid-level hardware
- Always select the "instruct" model variant, not the base model
- Datasets require three columns: instruction, input, and output
- 300–1,000 rows shifts tone and format; 5,000–15,000 examples teach a real skill; speaker used 1,100 rows
- Datasets can be generated via Claude by describing your vocabulary; Unsloth Studio includes a recipe system
- Recipe system supports starting empty, using learning recipes, or importing from Hugging Face

## Technical Details
- **LoRA/QLoRA architecture**: Train adapter layers on top of frozen base model; QLoRA adds 4-bit quantization for significant size reduction
- **Quantization**: 16-bit weights → 4-bit format reduces model from ~16 GB to 5–7 GB, enabling training with adapter layers in limited VRAM
- **Hardware requirements**: 
  - Windows: Nvidia GPU with ≥12 GB VRAM
  - Mac: M-series with 24–64 GB unified RAM (M3, M4, M5 Pro/Max)
  - Low-end: Google Colab notebook from Unsloth documentation
- **Installation**: 
  - Mac/Linux: command shown on documentation page (exact command not transcribed)
  - Windows: separate command shown on documentation page (exact command not transcribed)
- **Launch**: Type "yes" or run launch command; UI accessible at localhost:8888
- **Model selection**: Must use "fine-tune ready" filter; avoid GGUF format; select BNB 4-bit variant with safe tensors
- **Dataset structure**: JSONL with instruction, input (optional), output columns; 300–1,000 rows for tone/formatting; 5K–15K for skill training
- **Recipe system**: New recipe (empty or learning); seed data can be PDF/doc; can import from Hugging Face; custom recipes可创建 via AI generation (e.g., Claude)
- **JSON schema**: `{"input": {"type": "string"}, "output": {"type": "string", "required": true}}`
- **System prompt example**: `"hello, apa kabar"`
- **Training parameters**: rank, alpha, dropout, LoRA adapters, hyperparameters (beginners leave unchanged)
- **Epoch settings**: 1 epoch for simple data, 3 epochs standard best practice; more data may require more epochs
- **Training monitoring**: VRAM usage, temperature, power draw, training loss, gradient norm, learning rate
- **Learning rate**: gradually decreases over training steps
- **Loss value**: decrease indicates model accuracy improvement; loss below 1 typically signifies good performance
- **Compare chat**: side-by-side base model vs fine-tuned model responses
- **Export options**: GGUF model (for Ollama), 16-bit inference model, LoRA version
- **CSV seed data format**: columns Indonesian, English, category, example, example English with 276 rows
- **Recipe category weights**: 27% primary category, 23% chat, 5% correction (and other task types: translate, quiz, new word, correction, daily practice)
- **Full run**: can generate 50, 1k, 10k+ records with batching and retry settings
- **Progress updates**: polled every 5 entries during generation
- **Dataset view**: instruction, input, output columns after AI assistant column assignment (system=instruction, user=input, assistant=output)
- **Make row output**: should be split into separate input/output rows for proper system/user/assistant marking

## Questions
- What are the exact install commands for Mac/Linux and Windows shown on the documentation page?
- What specific Google Colab notebook from Unsloth enables cloud training on free GPUs?
- How does the Unsloth Studio recipe system work in practice for custom domains?
- What are the precise differences in output quality between LoRA and QLoRA beyond the size trade-off?
- How should users with mixed hardware (e.g., Apple Silicon + external GPU) configure the setup?
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
