---
video_id: 96jN2OCOfLs
title: "Andrej Karpathy: From Vibe Coding to Agentic Engineering w/ Stephanie Zhan"
url: https://www.youtube.com/watch?v=96jN2OCOfLs
watched: 2026-10-08 11:25
source: chrome:Default
topic: agents
indexed: 2026-10-08T06:03:20+00:00
type: youtube-note
source_url: https://www.youtube.com/watch?v=96jN2OCOfLs
tags: [youtube, youtube/agents]
---


## Core Concept

Karpathy's argument across both parts is that AI code generation's December inflection point wasn't a speedup but an arrival at "Software 3.0" — a paradigm where the prompt, not the code, is the program and the LLM is the interpreter — and that because these systems are shaped by pre-training statistics plus RL environments with verification rewards, they are "jagged entities": extremely capable where output is verifiable (math, code), quietly wrong at the edges (advising a walk to a car wash 50m away), and best understood as "ghosts" rather than animals. The professional response is therefore neither blind vibe coding (which raises the floor) nor a 10x-engineer fantasy (which is "not the speed up you gain"), but "agentic engineering" — a discipline that preserves the pre-existing professional quality bar while exploiting a ceiling far above the old baseline, with humans owning aesthetics, judgment, taste, spec and oversight. He extends that framing outward: today's tooling (docs, DNS, dashboards, settings menus) is human-first and must be rewritten to be agent-native, and even if thinking can be outsourced, understanding cannot — leaving the human as the bottleneck for knowing what to build and how to direct agents.

## Key Takeaways

- **December was the inflection point.** Karpathy was on a break with more time; agent "chunks" started coming out fine, he kept asking for more, and "I can't remember the last time I corrected it." His side-projects folder is "extremely full." People who experienced AI as "ChatGPT adjacent thing" last year "had to look again" as of December, because "things have changed fundamentally." He describes feeling "never felt more behind as a programmer" a couple of months ago — "a mixture of both," exhilarating and unsettling.
- **Background framing:** co-founded OpenAI in that office, got Autopilot working at Tesla, coined "vibe coding" last year.
- **Software 1.0 / 2.0 / 3.0.** 1.0 = writing explicit code. 2.0 = "programming by creating data sets" and training neural nets (arranging datasets, objectives, architectures). 3.0 = programming turns to prompting; "what's in the context window is your lever over the interpreter that is the LLM."
- **Why training on the internet yields a programmable computer:** to train one GPT/LLM on a sufficiently large task set, you implicitly must multitask everything in the data distribution — "these actually become kind of like a programmable computer in a certain sense."
- **OpenClaw as the software 3.0 tell.** Normally installation is a bash/shell script that balloons in complexity to target many platforms. OpenClaw's install is instead "a copy-paste of a bunch of text that you're supposed to give to your agent" — the agent inspects your environment and debugs in the loop. "What is the piece of text to copy-paste to your agent? That's the programming paradigm now."
- **MenuGen as the paradigm kill shot.** An app on Vercel that uploads a restaurant menu photo, OCRs the item titles, runs an image generator for pictures of each dish, and re-renders the menu — motivated by the ~50% of menu items he has no idea what are. The 3.0 version: give the photo to Gemini and say "use Nano Banana to overlay the things onto the menu." The returned image reproduced his exact menu with the dishes rendered into the pixels. "All of my menu gen is spurious. It's working in the old paradigm. That app shouldn't exist."
- **The framing error to avoid:** don't treat this as a speedup of existing things — "New things are available now." Example: LLM knowledge bases — have LLMs build wikis for an organization or a person. "This is not even a program... there was no code that would create a knowledge base based on a bunch of facts." You recompile documents into a different order and framing.
- **The exotic extrapolation.** A device taking raw video or audio into a neural net, using diffusion to render a UI unique to that moment. In the '50s–'60s it wasn't obvious whether computers would look like calculators or neural nets; we went the calculator path, so neural nets are virtualized on existing computers. That flips: the neural net becomes the host process, CPUs the co-processor, neural nets "the dominant spend of flops," and tool use survives as "historical appendage for some kinds of like deterministic tasks." Timeline conceded as TBD — "we'll probably get there sort of piece by piece."
- **Verifiability as the unifying principle.** Traditional computers automate what you can *specify* in code; this round automates what you can *verify*. Frontier labs train on "giant reinforcement learning environments" given "verification rewards," producing "jagged entities" that peak in verifiable domains (math, code, adjacent) and are "rougher on the edges" elsewhere.
- **Jaggedness has two causes:** how labs train, and what they choose to put in the data distribution — some domains are more economically valuable, so labs build environments for them, code being the clear example. "There are probably lots of verifiable environments... that happen not to make it into the mix because they're just not that useful to have the capability around." We are "slightly at the mercy of whatever the labs are doing."
- **The strawberry → car wash failure progression.** The old canonical failure was "how many letters are in a strawberry?" — models now patch it. Current version: "I want to go to a car wash... it's 50 m away, should I drive or should I walk?" State-of-the-art will say walk. "How is it possible that state-of-the-art Opus 4.7 will simultaneously refactor a 100,000[-line] codebase or find zero-day vulnerabilities and yet tells me to walk to this car wash?" Either something is slightly off in the model, or you must stay in the loop and treat them as fallible tools.
- **Chess as data-distribution evidence.** GPT-3.5 → GPT-4 improved at chess far more than generic capability progression would predict, which he attributes publicly to "a huge amount of data of chess" landing in the pre-training set — someone at OpenAI added it. Lesson: explore what you get with no manual and find out which circuits you're in.
- **Founders: verifiable domains are a moat, not a threat.** If your problem is verifiable, you can build your own RL environments/examples and fine-tune — "technology that just works." With huge diverse RL environment datasets and "your favorite fine-tuning framework," "you can pull the lever and get something that actually works pretty well." Applications outside the model's circuits "won't necessarily come out of the LLM out of the box."
- **Almost everything is eventually automatable; it's a gradient, not a wall.** Even writing can be made verifiable — "you can imagine having a council of LLM judges." The question is what's easy vs. hard. He twice starts to name a highly valuable unclaimed RL environment, then stops, teasing it and getting called out for vagueposting.
- **Vibe coding vs. agentic engineering.** Vibe coding "is about raising the floor for everyone... everyone can vibe code anything." Agentic engineering "is about preserving the quality bar that existed before in professional software" — "you're not allowed to introduce vulnerabilities due to vibe coding," you're still responsible, but can you go faster? Agents are "spiky entities... a bit fallible, a little bit stochastic, but extremely powerful."
- **The 10x engineer is dead.** People peaking at this "magnified a lot more" than 10x; "10x is not the speed up you gain."
- **Mediocre vs. AI-native coder.** Analogous to engineers maximizing their tools (Vim or VS Code, now Claude Code or Codex) — get the most out of all available features and invest in your own setup.
- **Hiring must be refactored.** "If you're giving out puzzles to solve, then this is still the old paradigm." Instead: "Let's write, say, a Twitter clone for agents and then make it really good, make it really secure, and then have some agents simulate some activity on this Twitter. And then I'm going to use 10 codex 5.4 x high to try to break your website that you deployed... they should not be able to break it."
- **Humans own aesthetics, judgment, taste, oversight.** He no longer remembers tensor API minutiae — "keepdims versus keepdim," "dim or axis," "reshape or permute or transpose" — "I don't remember this stuff anymore, right? Because you don't have to."
- **The MenuGen agent bug, as an argument for spec ownership.** Google-account signups plus Stripe credit purchases, both keyed on email addresses, but no persistent user ID; the agent tried to cross-correlate the Stripe email to the Google email and would fail to attach credits if they differed. "It's like why would you use email addresses to try to cross-correlate the funds? They can be arbitrary... this is such a weird thing to do."
- **Plan/spec as the human's job.** You work *with* the agent to write a very detailed spec that is basically the docs, then get agents to implement it. He's "in charge of the spec, this plan" — though he adds he doesn't even particularly like plan mode while acknowledging it's "obviously very useful."
- **LLM "intern" analogy for APIs.** Assistants have very good recall, but you still need the fundamentals — e.g. that PyTorch tensors have an underlying view, that a view shares storage with the same tensor while separate storage "will be less efficient" — "so that you're not copying memory around unnecessarily." "The details of the APIs are now handed off."
- **Division of labor today.** "You're in charge of the taste, the engineering, the design... you're doing some of the design and development and the engineers are doing the fill in the blanks."
- **Why LLM code quality is mediocre.** Likely "not part of the RL" — "There's probably no aesthetics cost or reward, or it's not good enough." Generated code is "very bloated," full of "copy-paste," with "awkward abstractions that are brittle" that work but are "really gross." On taste/judgment rising: "nothing fundamental is preventing it. It's just the labs haven't done it yet almost."
- **microGPT as the counter-example.** He tried to make LLM training as simple as possible; "the models hate this. They can't do it." Prompting "simplify more, simplify more" fails — "you're obviously pulling teeth. It's not like light speed."
- **Jagged forms of intelligence: animals vs. ghosts.** "We're not building animals. We are summoning ghosts." These intelligences are "shaped by data and reward functions, but not by intrinsic motivation or fun or curiosity or empowerment" — traits that "came about via evolution." Practical consequence: yelling at the model has no effect on performance, since the substrate is pre-training statistics with RL "bolting on top," which "kind of like increases the disadvantages." He admits the framing is "a little bit of philosophizing" with uncertain "real power" — it functions as "being suspicious of it and figuring out over time."
- **Agent permissions in practice.** The audience notes agents "have real permissions. They have local contacts. They actually take action on your behalf."
- **Everything is still written for humans.** "Everything has to be rewritten. Everything is still fundamentally written for humans and has to be moved around." His "favorite pet peeve": docs that say "go to this URL" instead of "what to copy paste to my agent."
- **Agent-native infrastructure recipe.** Decompose work into "sensors over the world, actuators over the world," "describe it to agents first," and build "automation around data structures that are very legible to the LLMs."
- **The Vercel deployment anecdote.** Writing MenuGen's code wasn't the trouble; "deploying it on Vercel because I had to work with all these different services" was — stringing them together, entering each service's settings menus, configuring DNS. "It was just so annoying." Proposed benchmark: give a prompt to an LLM, have it build MenuGen and deploy it with no human intervention.
- **Where this lands: agent representation.** "My agent talk to your agent to figure out some of the details of our meetings" — agent-native representation for people and organizations.
- **Education thesis and the human bottleneck.** The line that stuck: "you can outsource your thinking, but you can't outsource your understanding." "Information still has to make it into my brain, and I feel like I'm becoming a bottleneck of just even knowing what we're trying to build, why is it worth doing, how do I direct my agents." "You can't be a good director if... the LLMs certainly don't excel at understanding. You still are uniquely in charge of that." He closes excited to return in a couple of years to see "if we've been fully automated out of the loop."
- **Knowledge bases as understanding tools.** He reads an article, his wiki gets built up from it, and he asks questions of it — "a lot of prompts for me to do synthetic data generation kind of over some fixed data." "Anytime I see a different projection onto information, I always feel like I gain insight."

## Technical Details

**Paradigm stack**

| Version | Programming means |
|---|---|
| Software 1.0 | Writing code — explicit rules |
| Software 2.0 | Creating datasets + objectives + architectures, training neural nets |
| Software 3.0 | Prompting; the context window is the lever over the LLM "interpreter" |

**Automation criterion**

- Classical: automate what you can *specify in code*.
- Current LLM generation: automate what you can *verify*.
- Training substrate: "giant reinforcement learning environments" supplied with "verification rewards."
- Capability shape: "jagged entities" — peaks in verifiable domains (math, code, adjacent), "stagnate and are a little bit rougher on the edges" elsewhere.
- Diagnostic heuristic: "if you're in the circuits that were part of the RL, you fly."
- Chess evidence: GPT-3.5 → GPT-4 chess jump attributed to "a huge amount of data of chess" in the pre-training set.

**Architecture extrapolation**

- Neural net as host process; CPU as co-processor.
- Neural nets become "the dominant spend of flops."
- Tool use retained as "historical appendage" for deterministic tasks.
- Device class imagined: raw video/audio → neural net → diffusion-rendered UI "unique for that moment."
- Status: "I don't think that progression is TBD" (i.e. timeline explicitly uncommitted) — "we'll probably get there sort of piece by piece."

**Karpathy's model of the LLM stack**

- Base substrate: **pre-training** → "just statistics."
- On top: **RL** → "bolting on top, so it kind of like increases the disadvantages."
- Missing from the RL objective: an **aesthetics cost or reward** — the hypothesized reason generated code stays bloated and brittle.
- Consequence: yelling at the model has no effect; the framing yields "being suspicious of it and figuring out over time."

**Software 3.0 replacements for real software**

- Shell/bash install script → copy-paste prompt blob handed to the agent, which inspects the local environment and self-debugs (OpenClaw).
- Menu-photo app on Vercel (OCR + image generation + re-render) → single Gemini call: give it the photo, say "use Nano Banana to overlay the things onto the menu."
- Docs that say "go to this URL" → "what to copy paste to my agent."

**Agent-native system decomposition**

- **Sensors** over the world (perception / input side).
- **Actuators** over the world (action side).
- "Describe it to agents first," then wrap in "automation around data structures that are very legible to the LLMs."
- Emerging architecture: "agent representation for people and for organizations," with agent-to-agent negotiation replacing human coordination (e.g. scheduling meetings).

**Domain stack touched on**

- `Google` account auth + `Stripe` credit purchase, correlated only by email address (the identified flaw — no persistent user ID).
- `PyTorch` / `NumPy` / `pandas` tensor and dataframe API surface: `keepdims` vs `keepdim`, `dim` vs `axis`, `reshape` vs `permute` vs `transpose`.
- Tensor memory model: an underlying tensor has a **view** that shares the same storage, or has **different storage**, which "will be less efficient" — "so that you're not copying memory around unnecessarily."
- Tooling continuum: `Vim`, `VS Code` → `Claude Code`, `Codex`, `OpenClaw`.
- **microGPT** — the canonical "simplify LLM training as simple as possible" project, used as the benchmark for what models cannot do.

**Deployment anti-pattern (MenuGen on Vercel)** — manual steps to eliminate:

- stringing together multiple services
- navigating each service's settings menus
- configuring DNS records by hand

**Knowledge-base workflow (personal)**

- article → wiki entry built up from articles → question the wiki → "different projection onto information" produces insight.
- Characterized as "synthetic data generation" over a fixed corpus.

**No conventional code or command lines were spoken.** The closest verbatim artifacts are the install paradigm and the hiring drill:

```
Let's write, say, a Twitter clone for agents and then make it really good,
make it really secure, and then have some agents simulate some activity on
this Twitter. And then I'm going to use 10 codex 5.4 x high to try to break
your break your this website that you deployed
```

**Trade-offs asserted**

- Floor-raising (broad access) vs. ceiling-preserving (professional quality bar) — vibe coding and agentic engineering are different goals, not stages.
- Speed vs. verification — you get the speedup only by owning verification, oversight and spec.
- Capability you didn't fine-tune vs. capability you own: out-of-distribution domains "won't necessarily come out of the LLM out of the box," so fine-tuning becomes the founder's lever.
- More automation of *task selection* now, but human concentration on aesthetics, judgment, taste, spec, and oversight.
- Humans as "bottleneck of just even knowing what we're trying to build" — accepted as the current scarcity, not resolved.

## Questions

- **The withheld domain.** He twice says there are "very valuable reinforcement learning environments" not in the mix, and starts to name "one domain that I think is very uh—" before stopping himself and calling it vagueposting. Never given.
- **Which circuits am I in?** The core diagnostic advice ("if you're in the circuits that were part of the RL, you fly") has no accompanying method — no benchmark, probe, or eval he'd recommend for determining whether your use case is in-distribution.
- **Is the car-wash failure diagnosed?** He offers two hypotheses (something slightly off in the model, or "you need to actually be in the loop a little bit") and doesn't resolve between them. No root cause for a model that reportedly refactors a 100,000-line codebase while failing this trivial judgment call.
- **Fine-tuning specifics.** "Your favorite fine-tuning framework" is never named; no framework, dataset scale, compute budget, or cost is given for the "just pull the lever" path.
- **Which verifiable professions move faster than expected?** The host asked directly; he answered only that "almost everything" is verifiable to some extent, including writing via "a council of LLM judges." No concrete list, no signal on whether LLM judges scale beyond writing or are themselves jagged.
- **Does an aesthetics reward actually work?** Would adding an aesthetic cost/reward to RL improve code quality, or shift the failure mode? He asserts the absence of it is why code stays bloated and brittle but offers no evidence; "the labs haven't done it yet almost."
- **Can any current model reproduce microGPT's simplification?** If not, what makes that task categorically "outside the RL circuits"? Prompting "simplify more" reportedly yields "pulling teeth."
- **What would infrastructure need to look like?** For the "prompt → build MenuGen → deploy with zero human touches" test to pass today: how do the sensors/actuators decomposition and agent-native infrastructure concretely map onto an existing deployment stack, and who builds it?
- **The generational coding parallel.** Asked for the ChatGPT-gateway / Google-search-replacement analogy for coding, he answered in terms of individual skill investment ("get the most out of the tools"), not generational differences in how people work. Unaddressed.
- **Agent accountability.** If agents get representation and talk to each other, who is accountable for what an agent agrees to on a person's or organization's behalf?
- **Agent security model.** Agents have "real permissions" and "local contacts" and "take action on your behalf" — what access control, auditing, and revocation model is proposed? None is discussed.
- **Timeline for the neural-host / CPU-copcessor flip.** Explicitly deferred.
- **MenuGen's fate.** Retired, kept as a demo of the old paradigm, or rewritten as a thin wrapper over a Gemini/Nano Banana call? Not stated.
- **How much understanding is required to direct agents well?** And how would someone train that without the fundamentals (like tensor storage semantics) the segment says you must retain?
- **Is the human bottleneck removable?** "Becoming a bottleneck" for knowing what to build — does it vanish, or harden into the new scarce skill?
- **Does the ghost framing have real power?** He openly says "I'm not sure if it actually has real power" and calls it "a little bit of philosophizing."
- **Zero metrics.** No benchmark numbers, latency, cost, pass rates, or headcount comparisons appear anywhere in either part — including for the "well above 10x" claim and the security red-team drill.
- **Unverified model/agent names.** "Opus 4.7," "codex 5.4 x high," and "Nano Banana" are spoken as-is; the transcript provides no confirmation of versions or whether these reflect actual state of the art at recording time. "Open Claw" / "cloud code" are speech-to-text renderings.
<!-- yt-brain:related -->

## Related

- [[youtube/YouTube Knowledge Base|◻️ YouTube Knowledge Base]]
- [[youtube/agents|📁 AI Agents & Orchestration]]
- [[index|🏛️ JARVIS Memory Vault]]

### Related notes

- [[youtube/agents/2026-10-03-agentic-engineering-graphs-workflows-verifiable-coding-agent|Agentic engineering: Graphs, workflows, verifiable coding agent runtimes, and staying in control]] · relevance 0.12
- [[youtube/agents/2026-10-03-how-to-build-an-agentic-software-factory|How to build an Agentic Software Factory]] · relevance 0.09
- [[youtube/agents/2026-10-03-he-finally-10x-claude-code-with-this-method|He Finally 10x Claude Code With This Method]] · relevance 0.08
- [[youtube/agents/2026-09-29-claude-code-multi-agent-orchestration-with-opus-4-6-tmux-and|Claude Code Multi-Agent Orchestration with Opus 4.6, Tmux and Agent Sandboxes]] · relevance 0.08

<!-- /yt-brain:related -->
