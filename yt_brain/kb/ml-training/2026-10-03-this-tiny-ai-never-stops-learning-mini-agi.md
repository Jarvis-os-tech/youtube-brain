---
video_id: L-6O7R71CCg
title: "This Tiny AI Never Stops Learning (mini-AGI)"
url: https://www.youtube.com/watch?v=L-6O7R71CCg
watched: 2026-10-03 16:00
source: chrome:Default
indexed: 2026-10-03T12:06:34+00:00
topic: ml-training
---


## Core Concept

Mini AGI is a toy-scale language model that is trained from absolute zero (random weights, no pretraining) on a single consumer laptop and trained **continually** — it reads text in order, one chunk at a time, takes a small learning step per chunk, and never has a finish line. Its distinguishing claims are that it can be trained on hardware far too small for conventional training, that its knowledge is stored as a self-governing pool of expert files on disk, and that a slowly-updating shared core plus fast-changing specialists let it absorb new domains without the catastrophic forgetting that ruins ordinary fine-tuning. The video's demonstration trains one on children's stories, then feeds it Quentin Tarantino screenplays, holding out *Reservoir Dogs* as a test script.

## Key Takeaways

- Trained entirely on an **M2 Max MacBook Pro with 32 GB of RAM**; the repo had "only ever tested on an Nvidia card," so running it on a Mac was already off-script.
- Step 1 starts from a **completely blank model** — "just a bunch of random numbers" — that reads text **byte by byte, letter by letter**.
- Step 1 dataset: **tiny stories** (short children's stories) "to give it a voice."
- Step 2 dataset: **Pulp Fiction, Jackie Brown, Inglourious Basterds, Django Unchained, and his segment of Four Rooms**. *Reservoir Dogs* was deliberately withheld the entire time as a held-out test.
- Progression of English ability: at **7 minutes** output was nonsense ("thousand worded their lone Sheraton"); at **2 hours** it produced `Once upon a time, there was very down.`; by **4 hours** it "finally had a model that writes simple English."
- Every **5 minutes** the English-only model was given a read-only probe: the invented scene `Two men sit in a booth, one of them leans in, "Vincent."` and had to write Vincent's next line. It learned nothing from this — it was only a peek at the current training stage. Early answers: `They said you are mine.` / `They said you are their mom.` / `They say you are cone.`
- Catastrophic forgetting test run by the project's author: a model that had learned **8 different subjects** (stories, code, math) was fed **half a million characters of nothing but chess**. A normal setup lost **roughly half** of everything else; mini AGI kept **99.84%**.
- Screenplay format learned in **5 minutes** of phase 2 (indentation, character names in caps); the cast (Ordell, Louis, Schultz) appeared within **half an hour**; characters then apologized "like kindergarteners."
- English degraded simultaneously with the Tarantino phase until even `once upon a time` emerged as screenplay fragments.
- At roughly **15 minutes** the held-out *Reservoir Dogs* score stopped improving while the training scripts kept improving — the model shifted from style learning to memorization ("learning to be funny from your uncle versus memorizing his five favorite jokes").
- After a pause overnight and switching back to children's stories, English returned in **5 minutes**; learning it the first time had taken hours. Knowledge "was never erased. It was already on the disk."
- Adding **three more scripts** and resuming, the model snapped back into Tarantino mode "almost instantly," produced **Bill from Kill Bill**, and scored its best result yet on the hidden *Reservoir Dogs* script. Crossover improved too: `The bastards who should be more companion show up to the food court.`
- Roughly **1.5 hours** of further training produced "a somewhat coherent Frankenstein model."
- Total training was **7 hours, "maybe even more, maybe like 9 hours."**
- The demo app let the user set: their own character, the scene partner, a scene heading + action to open, the **reply length**, and how **crazy to tone the temperature**. Played as John robbing a bank with Freddy, the model looped on the phrase **"a silence"** and eventually switched scenes by itself ("it switched to a new place by itself").
- The author's verdict: to actually talk like Tarantino it would need **hundreds of millions of characters of English**, i.e. **several days of non-stop training**.
- The author calls it a **toy-scale model** and the **weights are not out yet**.

## Technical Details

- **Never-frozen training loop** — text is consumed in order, one chunk at a time, with a small learning step after each chunk; "there is no finish line."
- **Mixture of Experts (MoE) with on-disk residency** — a team of small specialist networks, only some active at any moment; here "every expert is its own file on disk, holding everything needed to train it." Before each chunk the model loads only the experts the incoming text needs onto the GPU, so "the model can be way bigger than your graphics card."
- **Self-governing expert population** — new experts appear as new files in the folder; unused experts are deleted automatically.
- **Two-speed architecture to defeat forgetting** — a *shared core* that every letter passes through, plus the *expert* specialists:
  - experts: "allowed to change quickly"
  - shared core: "only allowed to change **10 times slower**"
  - effect: "the new stuff mostly lands in the specialists, while the foundation everything else relies on stays pretty much intact" — likened to renovating rooms without touching the house foundation.
- **Why local training was previously impractical** — training needs "roughly **three or four times more memory** than just running a model," which is why a 30-billion-parameter model can be chatted with on a MacBook but training even a small model was "a job for a giant hyperscaler data center."
- **Catastrophic forgetting, defined by example** — a model trained on basic English and then taught chess "would suddenly forget how to write English."
- **Held-out generalization is the diagnostic** — with only one withheld script, validation noise is high enough that the author could not distinguish style learning from memorization until more scripts were added.
- Verbatim prompt/scene fragments referenced in the demo (no commands, CLI flags, file paths, or config were given in the transcript):
  ```
  Two men sit in a booth, one of them leans in, "Vincent."

  Once upon a time, there was very down.
  Timmy was sad because he was so happy.
  They said you are mine.
  Stephen, I'm soaring.
  The bastards who should be more companion show up to the food court.
  ```
- **Trade-offs stated by the speaker** — cannot hold a coherent conversation; cannot write meaningful adult sentences after<9 hours; "should you use it in production? Absolutely not"; "is it AGI? Hell no. Can it write a coherent sentence? Well, barely."

## Questions

- What repo is this? No repository URL, clone command, dataset download command, or training command was mentioned.
- No hyperparameters were stated: chunk size, learning rate, embedding/model dimensions, number of experts, routing strategy, optimizer, or the actual 10x slowdown factor's implementation.
- How was the 99.84% retention figure measured — over what evaluation set, and against which "normal setup" baseline?
- What score/metric was used on the hidden *Reservoir Dogs* script? The video shows it improving but never defines the measurement.
- No numbers are given for the total characters consumed in each phase, the number of scripts added in the second run, or GPU/CPU utilization and wall-clock breakdown.
- The shared-core "10 times slower" rule is asserted but not explained: is it a separate learning rate, a delayed update, or a replay buffer?
- How does expert deletion get decided (usage threshold, score, age), and what prevents catastrophic expert churn?
- The weights "aren't even out yet" — no release date, license, or paper link is mentioned.
- Would behavior change on an Nvidia GPU (the only tested path), or on a base M2 /16 GB machine?
- What prevented overfitting on the training scripts beyond the observed ~15-minute memorization plateau — is early stopping, regularization, or deduplication used?
- How much does phase ordering matter (stories → Tarantino → stories → Tarantino), and would other domain pairs behave the same?
