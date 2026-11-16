---
video_id: xVLz32EWmz0
title: "NYU Proffesor Yann LeCun Explains What Comes After LLMs"
url: https://www.youtube.com/watch?v=xVLz32EWmz0
watched: 2026-10-03 18:21
source: chrome:Default
indexed: 2026-10-03T23:59:33+00:00
topic: llm-core
type: youtube-note
source_url: https://www.youtube.com/watch?v=xVLz32EWmz0
tags: [youtube, youtube/llm-core]
---



## Core Concept

LeCun's argument across all three parts is that LLMs cannot reach human-level intelligence because they are generative systems trained on a tiny, highly redundant slice of human experience (text, ~10^14 bytes ≈ 400,000 human-years of reading — the same data volume as a four-year-old's visual experience), and that the correct alternative is a non-generative, joint-embedding, energy-based **world model**: perceive, encode state (using memory), imagine candidate action sequences inside the world model, score them with an energy/objective function used *at inference time rather than for learning*, and search for the sequence minimizing that energy — with guardrail objectives that make the architecture intrinsically safe and un-jailbreakable. The second half of the talk covers why such a world model must be trained by **predicting in representation space (JEPA)** rather than by pixel/token generation, why the central obstacle is **representation collapse** and how **SIGReg** (isotropic Gaussian regularization) solves it, and a set of research directives (energy-based over predictive, regularized over contrastive, world models over generative/video, observation over RL) that explicitly tell academics not to work on LLMs.

## Key Takeaways

**Part 1 — the critique and the architecture**

- **"Machine learning sucks."** Current ML is powerful but doesn't handle the real world: continuous, high-dimensional, noisy data. "The real world is messy; language is simple."
- **Moravec's paradox** (transcribed "the moravic paradox"): things simple for humans are hard for computers — a 10-year-old can do what you'd want a domestic robot to do, zero-shot. Teenagers learn to drive in a few hours of practice; self-driving companies have millions of hours of training data and still only reach Level 2/3, with heavily engineered robotaxis — no Level 5.
- **Piaget** (transcribed "Jean P"/"Jeep") is a major influence, as is Vladimir ("Vladlin") and "Jandra." The line *"intelligence is not what you know, it's what you do when you don't know"* was **never actually said by Piaget — it is apocryphal**, but other psychologists distilled his thinking into it.
- **Historical anecdote:** a late-1970s debate in France between Chomsky and Minsky over whether language is innate or learned. Marvin Minsky (transcribed "Simar Papard"), MIT professor, participated — and 10 years earlier had published the perceptron book that "basically killed the entire field of neural net" by pointing out the perceptron's limitations. In the debate he argued those simple models were evidence that learning is *possible*.
- **Three negations defining intelligence:** it is *not* an accumulation of declarative knowledge (which is what LLMs mainly are); it is *not* a collection of skills (you can brute-force any task with enough resources, including self-driving); it is the **ability to accomplish new tasks with little or no prior training**.
- **Consequence:** there will be **no simple measure of intelligence**, because any particular task can eventually be cracked with enough effort. What matters is *adaptability*.
- **"The notion of AGI is complete nonsense."** Human intelligence is **specialized** — we know different things because we were exposed to different environments.
- **How infants learn (mostly by observation in the first months):**
  - ~2 months: can vocalize, develops a dynamical model of its own limbs, but cannot affect the world; already learns the world is **3D** — distance is the best explanation of how the view changes as you move your head.
  - **Object permanence, stability, rigidity:** learned very quickly.
  - **Inertia and gravity (intuitive physics): ~9 months** for human infants, shorter for most animals. An 8–9 month old in a high chair systematically throws toys on the floor — running the experiment that *gravity applies to everything*.
  - Babies learn gravity **by observation**: the "car on a platform pushed off so it appears to float" scenario. A **6-month-old barely pays attention**; a **10-month-old is visibly surprised**. This is psychology's **violation-of-expectation** method, which he says can test whether an ML system has acquired common sense. (Paper co-authored mostly by "Emanuel Dupu," with "Gitenra" contributing little.)
- **The data-volume calculation against scaling LLMs to AGI:** typical LLM ≈ **20 trillion words ≈ 30 trillion tokens × ~3 bytes/token ≈ 10^14 bytes ≈ 400,000 human-years of reading**. A **four-year-old**: ~**16 hours** awake (~**30 minutes of YouTube uploads**), **2 million optic nerve fibers** at ~**1 byte/sec** each → ~**10^14 bytes** through vision (and probably touch). "We're not going to get to anything like human-like intelligence by just training on text."
- **Rebuttal to "video is more redundant than text":** redundancy is **a feature, not a bug** — self-supervised learning *needs* redundancy. ("You don't want too much of it.")
- **Two modes of inference — the central architectural claim:** LLM-style = propagate input through a **fixed number of layers**; LeCun's alternative = compute the output by **searching at inference time for the output most compatible with the input**, minimizing an energy function. "Intrinsically more powerful computationally." The energy/objective function "is **not used for learning, it's used for inference**" — like a cost function, a negative likelihood in a probabilistic model, or (his preferred framing) **an energy function**.
- **The two architectures contrasted on stage:**
  - *Left (LLM-like):* input window → fixed number of layers with **a few hundred billion parameters** → one token → shift into input → next token. Autoregressive; **a fixed amount of computation per token**. "This is not a good model of reasoning." You coerce an LLM to reason by "trick[ing] it into generating more tokens" — humans "reason internally… we don't reason in token space in language even."
  - *Right (his architecture):* perceive environment → infer current world state → **imagine a sequence of actions** → **internal world model** → predicts the outcome → **objective** measures how far the task has been accomplished → **optimization/search** minimizes this energy at inference time.
- **The long paper** (architecture settled ~**5 years ago**, posted online in **2022**, QR codes on stage, "relatively easy to read but kind of long") is based on the idea that **reasoning and planning proceed by energy minimization rather than forward propagation, and require a world model**.
- **Memory + perception:** perception gives only a representation of *what is currently perceived*; it must be **combined with memory** for a state of the world (or at least what you know about it).
- **Objective function shape:** outputs **zero** if the task is accomplished, a **positive number** if not — possibly scaled by *distance* to completion.
- **Guardrails as a second set of objectives:** ensure state sequences won't hurt/kill anyone. Such a system is **intrinsically safe** because it must optimize guardrails on every output. Contrast: the only way to make an LLM safe is **fine-tuning**, and "there is always a way to break the conditioning" — **"here you can't jailbreak a system like this."**
- **Multi-step use:** apply the world model across multiple timesteps; decompose action sequences into steps and **apply guardrails to every step**. This is **akin to model predictive control (MPC)** — "very classical stuff in optimal control going back to the 1960s."
- **Hierarchical planning (NYU → Paris example):** you can't plan a whole trip in **10-millisecond muscle actions** — it's too long *and* you lack information (how long will a taxi take?). High-level 2-step plan ("get to the airport and catch a plane," budgeting ~1–1.5 hours) → subgoal *be at the airport* → hail a taxi → subgoal *get down on the street* → elevator, button, down, exit → subgoal *reach the elevator* → eventually an action needing no planning ("you can probably stand up from your chair without having to think about it") — that's a **policy**. Animals do this too.
- **Hierarchical planning is an unsolved problem** — "completely open," "nobody has proved that they know how to do this," and an explicitly recommended PhD topic.
- **Training, first 10–15 years:** he's been trying to train world-model-like things for ~**15 years, mostly failing for the first 10** because he was training **generative models**.
- **Why masked-prediction self-supervision works for text but not video:** for text, corrupt the input and recover the missing parts — **BERT** did this; **an LLM is the special case where the only word removed is the last one**. For video, predicting next frames at pixel level gives representations that are "not particularly good." Text works because the vocabulary is **finite**; video has an effectively **infinite number of plausible frames** — slowly pan the camera around this room and no system can predict what the audience looks like or which chairs are unoccupied. "You just don't have the information. So when you train a system to make this kind of prediction, **you kill it.**"
- **The saving distinction:** **video generation is done in representation space**, with a second stage turning predictions into high-res, high-frame-rate video. The system needs only **one cute-looking video** — "a much simpler problem." Diffusion models producing cute videos show **no evidence of understanding the world**.
- **Why the old work was blurry:** a 10-year-old paper predicted short clips — **2 frames from 4 frames of context** — and got blurry output "because the system predicts the **average** of everything that can happen." GANs weren't successful; latent-variable models like **diffusion models** might help (not known at the time).
- **JEPA — Joint Embedding Predictive Architecture:**
  - *Generative:* observe x, action a, result y → **reconstruct y in its most minute detail**.
  - *JEPA:* observe **X, Y, and A**, **encode both X and Y**, and **predict in representation space**.
  - Effect: the system **eliminates from the input all information about Y that is simply not predictable** — predictions become "more abstract with fewer details but more accurate."
  - Generative models are easy to train because the cost is just **reconstruction cost** — train as an **autoencoder**, then restrict information content in the code, i.e. a **denoising autoencoder** (MAE and similar: corrupt the input, recover the original). **Diffusion models are a bit of a special case of denoising.**
  - Talk cuts off mid-punchline: "the bad news is when you train systems of this type to learn representations of images you don't get good representations…"

**Part 2 — JEPA, collapse, SIGReg**

- **The core point:** LLMs are *generative* systems trained as *predictors of the world in text space*. "This is not what we want for the next generation of systems."
- **The framing:** "The way to think about AI, the way to think about deep learning, and machine learning in general, is that basically it's about prediction."
- **Two things we want:** representations that are **predictable** and representations that are **informative**. "We want to build models that are aware of the world and can predict what happens in the world."
- **Two architectures:** predictive (generative) vs. joint embedding. Best systems for image/video representations all use self-supervised learning with joint embedding; **none** uses reconstruction.
- **JEPA training recipe:** either (a) two views of the same scene, trained so both representations are identical; or (b) corrupt/transform the input and predict the representation of the *original* from the corrupted version's representation.
- **The collapse problem:** an autoencoder without a restriction on information content "is just going to learn the identity function"; a JEPA can ignore inputs, produce constant representations, and get zero prediction error.
- **Preferred fix — information maximization:** a differentiable objective measuring information content of the encoder output, maximized (cost = minus information).
- **Named methods of the last ~6–7 years:** **VICReg**, **NCR²**, **VICRegG**, **BYOL**, "BYOL twins," **MCR** (Berkeley), **MCR²** (Simon Shlomo, NYU neuroscience). VICReg came from people working with him. ~**1,700 papers** on Google Scholar mention "Joint Embedding Predictive Architecture" spelled out.
- **Why information maximization is hard:** (1) no objective measures of information content — all proper definitions need the true distribution, and you only have samples; (2) to maximize you need a *lower* bound, but every empirical measure is an *upper* bound. "We come up with a good upper bound and we cross our fingers and we show some theorems and whatever."
- **Energy-based models** — his framing for ~20 years: capture dependencies between X and Y where there's no function Y = f(X). Learn an energy function scoring whether a point in XY space is near the training data — a landscape with data points in the valleys ("in Switzerland it would be a lake"). Given X, compatible Y values **minimize** energy → **inference by optimization, not forward propagation**. Works in both directions. Probabilistic models are a special case with particular energy form and loss.
- **EBM collapse = flat energy everywhere**, the same failure as the identity autoencoder or constant-representation joint embedding.
- **Two families of collapse fixes:** *contrastive* — generate points outside the data region and push energy up; *regularization* — **minimize the volume of space that can have low energy** ("the preferred" of the two).
- **Back to SIGReg:** run a batch through encoders → a matrix whose rows are samples and columns are representation variables. Make **rows all different** (sample-contrastive) or **columns all different** (dimension-contrastive → maximally disentangled). CLIP-style image/text embedding is sample-contrastive; he prefers dimension-contrastive.
- **The abstraction argument:** hierarchy from quantum fields → particles → atoms → molecules → proteins → cells → organisms → individuals → societies → ecosystems. Each level enables longer-range predictions by ignoring lower-level detail; hence psychology beats particle physics for explaining this room right now. Each abstraction "contains new knowledge … not apparent at the level below."
- **Aerodynamics example:** CFD models air in cubes by velocity and density, solving Navier–Stokes PDEs — it *ignores* molecules bumping into each other, because simulating at that level "would diverge from reality really quickly because it has too many details." So world models **should not be simulators**, **not digital twins**, **not generative models**, and **not video generation**.
- **"If you want to use world models, do not work on video generation. This is a different problem."** Cute videos → video generation; robot control, industrial processes, understanding the world → not generation.
- **Robotics framing:** a free humanoid can be given dynamics equations and simulated doing somersaults and kung fu; real-world interaction is much harder to reduce to equations. For a turbo jet, chemical plant, or patient you instead learn a **phenomenological model** of the system plus its environment interaction to predict and plan action sequences. "The concept is very old. It goes back to the 1960s. It's the root of optimal control."
- **SIGReg details:** make the representation distribution **isotropic Gaussian** (same variance in all dimensions) — that's independent variables, maximally informative individually; also max-entropy for a given variance, "but we don't really care about that." Trick: project points onto one direction → marginal; points are discrete so compute the **empirical CDF (a staircase)**; measure distance from the Gaussian CDF, giving a **gradient per training sample** telling you which way to move the point in that projection. Theorem: optimizing along many directions ⇒ the joint distribution becomes isotropic Gaussian.
- **Practical SIGReg results:** "this really works in practice," applied to **action-conditioned** world models used for planning. "Works decently," source code available, "very simple," trains on **one GPU**. Needs scaling up; demo used a push-T-like simulation.
- **Recent theoretical paper (a few days old):** if the underlying data distribution *is* isotropic Gaussian and observations are a complicated nonlinear transform (his example: a spiral transform), training with SIGReg recovers the original Gaussian in representation space — **up to a rotation**. Not a general proof.
- **Distillation methods (conceptually favorite but not yet scaled):** still two encoders with identical architectures sharing weights, but no backprop through the right encoder. The right encoder updates via an **exponential moving average (EMA)** of the left encoder's weights; left gets gradients all the time, right updates slowly.
- **Origins:** intuitive ideas from people at Google DeepMind using this to stabilize variance in reinforcement learning, then applied to SSL from images — **"Bootstrap Your Own Latent" (BYOL)**. Meta developed a whole batch (VICReg etc.) using the EMA idea.
- **V-JEPA:** JEPA applied to video — take a video, mask a big chunk, train the JEPA to predict the representation of the *full* video from the partially-masked representation. State of the art on **action recognition, action prediction**.
- **Scaling results:** V-JEPA beats **MAE** (generative autoencoder) and is "much faster to train." **DINO** (former Meta colleagues in Paris, "completely self supervised," joint embedding + distillation "with various tricks which I'm not going to explain") "basically at this time produce[s] the best generic representations of images" — probably the best encoder for any vision task.
- **Video prediction demo:** masked JEPA window of **16 frames**, slid over a video, predicting the next ~15–16 frames; a planner using the world model drives a simulated environment toward the goal configuration "in less than 25 steps." Also applied to double pendulum and push-T.
- **Emergent common sense:** show V-JEPA a video where something impossible happens and the **internal prediction error shoots through the roof** — e.g. a ball is thrown and disappears. "It's the first time, at least from my point of view, that I've seen completely self-supervised system acquire some level of common sense — tell you what's possible, what's not possible."

**Part 3 — results, directives, Q&A**

- **3D understanding falls out of video prediction.** Experimental proof: the representation from a version of V-JEPA (transcribed "VJA 2.1") was taken, a **head was trained on top of it to predict depth from a single image**, and it produced "really good results — in fact better than the V3" (transcription ambiguous; likely a comparison against the prior V-JEPA generation).
- **Interpretation:** a system trained only to fill in blanks in video *at the representation level* "understands" (in scare quotes) the notion of an object, and that the world is three-dimensional.
- **Transfer evidence:** feeding that representation into a **segmentation system** "works decently well," as do "various other things."
- **Research directives, in his words:**
  - Work on better generative models — but **do not work on LLMs**. "If you're in academia, you should absolutely not work on LLM. There is nothing you can bring to the table."
  - Favor **joint embedding architectures**.
  - **Abandon predictive models** in favor of **energy-based models** ("I didn't have time to really explain why").
  - Argue for **regularized methods / information maximization through variables instead of samples**.
  - **Abandon contrastive methods** — "which again have a lot of practical applications."
  - **Minimize, don't abandon, RL**: it is "horribly inefficient in terms of sample efficiency," and "RL is like what you do when you're desperate and there is nothing else you can do." Do most learning **by observation / world models**, then RL on top of already-good representations. Sometimes you can't avoid it. ("I don't really mean abandon.")
- For "real progress in AI … grounded AI for the real world … physical AI": **don't work on LLMs, and don't work on generative models either.**
- **Industry fallout:** this "does not make me very popular in Silicon Valley."
- **Left Meta** at the end of last year and formed a new company (transcribed "AMABS"/"AMAs"), whose purpose is "AI for the real world," i.e. physical AI. **Robotics is a use case but not the whole thing** — also **control of industrial processes**: "anything that is high-dimensional, continuous and noisy, for which LLMs are completely helpless."
- **Q&A (the only audience question taken):** an engineer asks how constraints like "don't bump into the wall," which engineers normally specify in **state space** (e.g. 3D space) for **MPC**, get expressed in a system operating in **representation space**.
  - LeCun: learn a **very small head** on top of the representation mapping it to the constraint you care about. "That part has to be trained, but you can train it with very small number of samples because it's a tiny — basically just a projection."
  - You need a **different projector for each constraint**. For a task objective like opening a door you need a **cost function** telling you whether the door is open, which "might have to be trained when you train to accomplish the task" — quoted sample count is garbled ("basically that request two samples").
  - Session closed immediately after ("I think we'll have to leave it here").

## Technical Details

- **Two inference paradigms**
  - *Forward propagation:* input → fixed depth of NN layers → output. Fixed compute per output.
  - *Inference-time search:* propose outputs, score them, return the minimum-energy one. Variable compute, spent on search rather than depth.

- **Pipeline as described (left → right):**

```
LLM-like:
  input window -> [fixed layers, few hundred billion params] -> next token
                -> shift token into window -> repeat

LeCun-style:
  perceive -> encode current world state -> imagine candidate action sequence
  -> world model predicts outcome -> objective/energy scores predicted outcome
  -> search/optimize for minimum energy -> output action

With memory:
  perception (what is perceived now) + memory (what is known)
  -> full state of the world -> world model -> ...
```

- **Architecture comparison (LLMs vs. JEPA as world models):**

```
LLM today:
   tokens --(transformer)--> next-token representation
         --(joint embedding with vocabulary)--> output token
   - generative model
   - autoregressive model (ABM) = special case of JEPA
     with a single predictable representation
   - predicts text in the space of tokens

Desired:
   world / video / images --> joint embedding architecture --> compact representation
   - can predict in representation space
   - can reason, predict, and plan
```

- **Objective/energy function contract:**

```
  f(task_accomplished) = 0        when accomplished
  f(...) = positive value         when not,
                                   optionally scaled by distance to completion

  Optimized at inference time ONLY -- explicitly not a learning loss
  Interpretations: cost function | negative log-likelihood in a probabilistic model
                 | energy function (his preferred framing)
```

- **Safety property claimed:** guardrail objectives are optimized on *every* emitted action, so safety is architectural rather than a fine-tuning patch — "there is always a way to break the conditioning" for LLMs; "here you can't jailbreak a system like this."
- **Control-theoretic framing:** applying the world model over multiple timesteps with per-step guardrails is "akin to **model predictive control (MPC)** … very classical stuff in optimal control going back to the 1960s."
- **Hierarchy of planning levels used as the example**
  - Top level: *get to the airport and catch a plane* (duration estimate ~1–1.5 hours)
  - Subgoal: *be at the airport* → walking down the street, hailing a taxi
  - Subgoal: *get down on the street* → walk to elevator, press button, ride down, exit the door
  - Subgoal: *reach the elevator*
  - Base level: single familiar action requiring no planning — **a policy**
  - Leaf actions are the human elementary motor actions at **10 ms** granularity
- **SIGReg computation, as described:**

```
1. Run a batch of samples through encoder(s).
2. Collect points in representation space
   (e.g. ~2000 dims, a few hundred–few thousand points).
3. For many random directions u:
     a. project every point: t = u · z
     b. build the empirical CDF of {t}  -> a STAIRCASE
        (points are discrete, not a density)
     c. compare to the Gaussian CDF along that projection
     d. distance => per-sample gradient: move the point left or right
4. Backprop those gradients through the network
   (update weights, points move).
5. Theorem: optimizing over lots and lots of directions
   => the joint distribution becomes isotropic Gaussian.

Target: isotropic Gaussian = same variance in all dimensions
      = independent variables = maximally informative individually
      = max entropy for a given variance (stated as not the reason)
```

  - Contrastive vs. regularized axes in SIGReg's matrix view: rows all different → **sample contrastive** methods (CLIP-like); columns all different → **dimension contrastive** methods = a *regularized* method (his preference; per-variable disentanglement).
  - Desiderata of a good representation: predictable, informative, and **incrementally predictable** (predictable for a while) — stated as something "people keep forgetting."

- **Theory result (paper released days before the talk):**

```
Assumptions:
  - the underlying explanatory variables are isotropic Gaussian
  - observed data = some complicated nonlinear transform of those
    variables (his example: a spiral transformation)
Result:
  - training a neural net with SIGReg recovers the original
    isotropic Gaussian in representation space, UP TO A ROTATION
Not claimed:
  - a general proof that SIGReg works in every case
```

- **Energy-based model as a landscape:** train samples sit in the **valleys** of an energy landscape ("the black dots are in the valley… in Switzerland it would be a lake"); level curves rise away from data. Inference: given X, compatible Y values **minimize** energy → **inference by optimization, not by forward propagation**. Symmetric: given Y, infer multiple possible X. "Probabilistic models are special cases where your energy has a particular form and the way you train it [is a] particular loss function."
- **Self-supervised objectives contrasted**
  - Text: mask arbitrary words, predict them — **BERT**
  - Text, autoregressive special case: mask only the **last** token → **LLM**
  - Video pixel-level next-frame prediction: fails; information-theoretically unconstrained
  - Image/video reconstruction: autoencoder → **denoising autoencoder** (e.g. **MAE**) → reconstruction cost as the only training signal
  - **Diffusion models:** "a bit of a special case" of the general denoising idea; video quality ≠ world understanding
  - **JEPA:** predict in encoded representation space of X and Y (conditioned on action A), discarding unpredictable detail
- **The data-bandwidth argument (numbers as stated)**

```
LLM training corpus:
  ~20 trillion words -> ~30 trillion tokens -> ~3 bytes/token
  -> ~10^14 bytes -> ~400,000 human-years of reading

4-year-old visual experience:
  ~16 hours awake
  ≈ ~30 minutes of YouTube uploads
  × 2,000,000 optic nerve fibers × ~1 byte/sec
  -> ~10^14 bytes
```

  Implication: text-only training cannot reach human-like intelligence; **self-supervision requires redundancy**, so video's redundancy is an asset.
- **Terminology and acronym table**

| Term | Meaning |
| --- | --- |
| JEPA | Joint Embedding Predictive Architecture |
| SIGReg | Sketch Isotropic Gaussian Regularization (also "sigreg"/"sigg") |
| EMA | Exponential moving average of encoder weights (target encoder in distillation) |
| BYOL | "Bootstrap your own latent" — Google DeepMind ancestor of the EMA-target-encoder idea |
| V-JEPA | Video JEPA — masked video → representation of full video |
| DINO | Meta self-distillation joint embedding architecture, best generic image representations |
| MAE | Generative autoencoder baseline V-JEPA is compared against |
| VICReg / NCR² / VICRegG / MCR / MCR² | Named information-maximization SSL methods (last ~6–7 years) |
| CLIP | Sample-contrastive joint embedding between images and text, used in LLM perceptual pipelines |
| EBM | Energy-based model — his unifying framework for all learning systems |
| ABM | Autoregressive model — described as a special case of JEPA with a single predictable representation |

- **Demo / probe numbers**
  - World-model planner video: complex-dynamics simulated environment, goal at top, initial state at bottom; reaches a configuration "as close as possible to the original" in **< 25 steps** of planned actions. Environments: **push-T**, simple robotic arm in simulation, **double pendulum**.
  - V-JEPA prediction error probe: input window of **16 frames**; measure error for the next 15–16 frames while sliding. Infeasible/unphysical event → error "shoots to the roof" (thrown ball that disappears).
  - Depth probe: lightweight **head** on a V-JEPA representation mapping a **single image → depth**; downstream **segmentation system** also consumes the representation.
- **Proposed architectural direction (part 3):** **joint embedding architectures** instead of pixel/token generation; **energy-based models** instead of purely predictive (autoregressive/generative) models; **information maximization through variables rather than samples** as a regularized objective; **contrastive methods explicitly rejected** despite practical value.
- **Sample-efficiency argument:** the bottleneck in current AI is samples. Observation-based world models do the heavy lifting; RL is a last-resort top layer over good representations.
- **Two action spaces:** **state space** (where engineers write MPC constraints like 3D collision avoidance) vs. **representation space** (where the proposed system operates). Bridging uses **per-constraint projection heads**, trainable cheaply, but **non-transferable across constraints** — one projector per constraint, one cost function per task objective.
- **Stated problem class for the new company:** high-dimensional, continuous, noisy control problems — robotics plus **industrial process control** — where "LLMs are completely helpless."
- **World models are not simulators:** CFD/Navier–Stokes models air by velocity and density in cubes, ignoring molecular collisions, because the finer simulation "would diverge from reality really quickly because it has too many details." Hence: not simulators, not digital twins, not generative models, not video generation. Learn a **phenomenological model** instead — "the root of optimal control," 1960s vintage.
- **Trade-offs stated**
  - Joint embedding methods predict in representation space → fast, informative, abstract target rather than pixel-level; but require a way to *measure* information content without the true distribution, and every practical measure is an upper bound where a lower bound is needed.
  - Contrastive methods are popular and effective (CLIP, perceptual LLM pipelines) but require generating negatives/out-of-distribution points; regularization methods (minimizing low-energy volume) are his preference.
  - Video generation is a *different problem* from world models; equating them is a mistake, as is the "digital twin" buzz phrase.
- **Landscape claim:** self-driving is at Level 2–3 in consumer cars; robotaxis are "engineered very heavily" with various sensors — Level 5 does not exist.
- **Speaker/attribution notes (transcript spellings):** "Jean P"/"Jeep" = Piaget; "Nam Chsky"/"Chungsky" = Chomsky; "Simar Papard" = Marvin Minsky; "Gitenra" and "Emanuel Dupu" = co-authors of the infant-cognition / violation-of-expectation paper; "Vladlin" and "Jandra" referenced in the infant discussion; the new company renders as "AMABS"/"AMAs."
- **Terms used without expansion:** **MPC**, **guard rails** (referenced as on an earlier slide, never defined), **cost function**, **Navier–Stokes**, **CFD**.

## Questions

- **Hierarchical planning is the stated open problem** — no method, no proof. Everything above it in the talk is conditional on solving it.
- **How is the energy/objective function itself obtained?** Objectives are used at inference only, not for learning — but the talk never says how task objectives and guardrail objectives are specified, learned, or who defines them. This is the practical bottleneck for the safety claim.
- **Intrinsic safety is conditional on the world model being correct.** A system optimizing a guardrail objective through a *wrong* world model could satisfy the objective while violating the intent. Not addressed.
- **Inference-time search cost/latency** is asserted to be more powerful but never quantified — no comparison against autoregressive generation.
- **Whether JEPA can be applied hierarchically** is untouched; training discussion says "hierarchical or not, let's say non-hierarchical to start."
- **What exactly does the JEPA predictor head consume**, and how are loss, normalization, and batch size set?
- **What defines "world model"** in his framework — is it a JEPA plus a planning/search component (like Dreamer), and what loss is used?
- **How does V-JEPA compare against DINO/SigLIP on benchmark numbers?** He explicitly avoided a results table, so the claims are unquantified.
- **What "JEPA for action" work is this, and is it released?** Source code is "available" with no URL, repo, or name given.
- **How large are the SIGReg batch and projection counts in practice**, and what's the compute cost relative to a reconstruction objective?
- **Since the SIGReg guarantee requires the explanatory variables to already be Gaussian, what happens when they aren't?** He flags this as unproven.
- **Why do reconstruction autoencoders (MAE-style) remain useful** if pixel-level prediction is the wrong objective — is there a hybrid or a regime where they still win?
- **How does the information-maximization / distributional-regularization family (VICReg, MCR²) relate to SIGReg** — generalization, or orthogonal?
- **How are the distillation methods (BYOL / V-JEPA / DINO) formally framed as energy-based models?** Not addressed.
- **No compute-budget comparison:** V-JEPA vs. MAE training cost, or SIGReg vs. contrastive loss cost.
- **The common-sense demonstration is anecdotal** (prediction error spikes on impossible videos); no quantification of a "common sense benchmark."
- **Why precisely is pixel-level video prediction "killing" to representations** while JEPA's abstract prediction isn't — the mechanism (discarding unpredictable information) is asserted, not demonstrated.
- **No numbers on how a world-model system would actually be trained** — data sources, compute, or scale needed.
- **The 2022 long paper is never named** on the transcript — only described ("long," "relatively easy to read," general architecture, QR codes).
- **The 10^14-byte comparison** is an order-of-magnitude argument: "3 bytes/token," the 1-byte/sec-per-fiber figure, and the "30 minutes of YouTube uploads" analogy are approximations stated without sources. "20 trillion words / 30 trillion tokens" is dated to the moment of the talk and isn't tied to any specific model.
- **Company name:** the transcript renders it "AMABS"/"AMAs." Verify the actual name and founding details — the transcript itself does not disambiguate.
- **"Better than the V3":** which baseline/model generation is being beaten at depth prediction from a single image? No benchmark, dataset, or metric is given.
- **Guardrails:** referenced as being on an earlier slide but never defined. How the mechanism differs from the constraint-projection heads is unresolved.
- **MPC:** never explained; he never says whether engineers keep state-space constraints by hand-mapping or whether the system learns them. His answer covers only a learned **projector per constraint**.
- **Contrastive methods:** rejected without a stated replacement objective.
- **Sample-efficiency claims are unquantified:** "very small number of samples," "request[s] two samples," "so horribly inefficient" for RL.
- **Part 3 is conclusions + Q&A, not self-contained** — it assumes the earlier material rather than restating it, and several promised arguments ("I didn't have time to really explain why") are explicitly deferred.
<!-- yt-brain:related -->

## Related

- [[youtube/YouTube Knowledge Base|◻️ YouTube Knowledge Base]]
- [[youtube/llm-core|📁 LLMs & Model Behaviour]]
- [[index|🏛️ JARVIS Memory Vault]]

### Related notes

- [[youtube/llm-core/2026-10-04-clip-but-for-decisions-contrastive-language-models-explained|CLIP… But For Decisions (Contrastive Language Models Explained)]] · relevance 0.14
- [[youtube/llm-core/2026-10-04-these-19-jev-claude-use-cases-are-blowing-people-s-minds-wit|These 19 Jev-Claude use cases are blowing people's minds (with prompts)]] · relevance 0.08
- [[youtube/llm-core/2026-10-03-the-first-real-rsi-is-here-and-it-s-evolving-fast|The First Real RSI is Here and It’s Evolving Fast]] · relevance 0.07
- [[youtube/linux-infra/2026-10-03-ai-harness-engineering-forward-deployed-engineering-tutorial|AI Harness Engineering - Forward Deployed Engineering Tutorial]] · relevance 0.07

<!-- /yt-brain:related -->
