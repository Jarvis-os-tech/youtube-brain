---
video_id: 3oGDb2wzpGA
title: "AI Built an OS… and It Actually Works"
url: https://www.youtube.com/watch?v=3oGDb2wzpGA
watched: 2026-09-29 11:10
source: chrome:Default
indexed: 2026-09-30T16:35:50+00:00
topic: llm-core
---


## Core Concept

The video tests whether any operating systems genuinely written by AI actually work: the author asks Abacus AI's root-LLM router to recommend fully AI-made OSes, then tries to build bootable USB media for the top recommendation (Vib OS) with an AI agent, boots it on real hardware, and audits each shell, file manager, and bundled app to separate "boots and looks like an OS" from "actually functional."

## Key Takeaways

- The only recommendation the router gave was a warning: "If you're looking for an operating system for daily use or production, there are no reliable complete operating systems coded entirely by AI. But we do have some low-level systems."
- Abacus AI's **root LLM mode** auto-routed the query to **Gemini 3.8 Flash**; the video is sponsored by Abacus AI (ChatGPT6 Astra + Claude Fable 5.1 advertised at $10/month in the description).
- **Vib OS** (also called Viv OS in the terminal, "Vevo OS" in the boot menu) is an "open-source experiment in Vibe coding an operating system from scratch using large language models," on **version 2.2.1** on GitHub, described as a multi-architecture OS with full GUI.
- Vib OS is a from-scratch Unix-like OS built with **25,000 lines of C and assembly**, UI inspired by macOS, running natively on **QEMU**, real hardware including **Raspberry Pi** and **Apple Silicon**; the x86 bootable version was described as "soon."
- The author used an **Abacus agent session in max mode** (Fable 5.1 + GPT-6 Astra) fed the GitHub link to produce bootable media, yielding a **Vib OS x86-64 USB image** and an **ISO**.
- Flashing the ISO with **Rufus** first failed on "cluster size"; retrying with **512 bytes** wrote successfully, but real-PC boot failed while the ISO booted fine in a VM.
- AI's advice was to use the **`.gz`/`.zip` USB image instead of the ISO**; extracted, Rufus defaulted to **MBR** (AI recommended GPT but it was locked), and it still didn't boot.
- A second agent run produced a purpose-built **128 MB MBR image with a single active FAT32 partition and a correct FAT header**. It also failed — boot menu showed "Vevo OS," then a green line and four small color blocks.
- A third agent run diagnosed the issue and produced a fixed image; booting the USB then offered **two boot entries, the second labeled "safe mode PS2 input only"** — that one booted into the OS with working mouse and keyboard.
- `neofetch` reported the host as a **virtual machine** and the CPU as **"QEMU virtual CPU"** despite running on real hardware, using **12 MB of 512 MB** — prompting the theory that a VM is being emulated on the USB.
- Files and apps are largely non-functional: report.txt, wallpaper JPEG, notes.txt, readme.txt, project1.text all fail to open; the calculator only accepts **keyboard** input (5 + 6 on the numpad worked) with no on-screen input; the notes app types but cannot save or open; the settings tab just reopens the file manager; the analog clock hands are frozen; snake starts but moves extremely slowly and ignores arrow keys — **all reproduced in a VM**, so it is not just a real-hardware artifact.
- **Doom** is listed on the GitHub page as a "fully working version of Doom built in," but the author never got it to run and went looking for someone else's video of it working.
- The second recommendation, **Mate OS**, required typing "operating system" to get past a wrong result (a Spanish professional poker player named Mate); its GitHub page lists exactly **two contributors: Daniel Mateos and Claude**, and its screenshots show Doom running. It was deferred to a follow-up video.

## Technical Details

- Boot media pipeline: AI agent → x86-64 image/ISO → Rufus → USB stick → F9 boot menu on real hardware, with a VM (QEMU) used as a working baseline.
- Claimed target platforms: QEMU, Raspberry Pi, Apple Silicon; boot path described as UEFI + BIOS, with a bootable x86 build pending.
- The working image's distinguishing trait: MBR layout, one **active FAT32** partition, valid FAT header, ~128 MB.
- Rufus settings that mattered during debugging: partition scheme **GPT vs MBR**, **cluster size 512 bytes**, and choosing the `.zip`-derived raw image over the ISO.
- Why the OS may boot at all: the binary reports itself as a QEMU guest, so the USB may be booting an emulated guest rather than driving hardware directly — which would also explain the mouse/input failures.
- A "safe mode PS2 input only" boot option was the only path that produced a working desktop, implying the default PS/2 vs USB input handling was the actual boot blocker.
- GUI behaviors observed: macOS-style dock **magnification/zoom** on hover, single-click folder navigation, window dragging drives a fake clock.
- Trade-off framing: the project is explicitly labeled a vibe-coding *experiment*; the router's own verdict was that nothing AI-made is production-ready, and every app that "works" only accepts real keyboard input or refuses to persist data.
- Useful commands inside the OS:

```
help
neofetch
free
ls
cd
pwd
```

- Referenced artifacts / paths (as named in the video):

```
vib-os-x86-64-USB-image.gz
vib-os-x86-64-USB-image.zip
vib OS x86-64 USB image
ISO  (first AI-built image)
rebuilt 128 MB MBR / single active FAT32 image
final fixed image
```

- Verified-working CLI surface: list directory contents, change directory, print working directory, and a `free`-style memory report showing 12 MB in use.

## Questions

- What exactly did the agent change in the final "fixed" image, and was the blocker PS/2 vs USB input handling, the FAT/partition layout, or both?
- Is Vib OS really booting a QEMU guest off the USB, or is `neofetch` simply misreporting host/CPU on the native build?
- Are the file-open failures, missing save, frozen clock, and sluggish snake inherent to Vib OS, or a side effect of a build that never completed? The author only verified one self-built image in one VM configuration.
- Does the advertised Doom build actually run anywhere? No demonstration was obtained.
- The prompt behind the rabbit hole was a straight recommendation query, so which "operating systems made entirely by AI" the router was weighing — and why it returned only Vib OS and Mate OS.
- Does the promised bootable x86 version exist now, and does anything run on Raspberry Pi or Apple Silicon as the README claims?
- Mate OS was entirely unevaluated: no boot test, no app audit, and its authorship is one human plus "Claude" as a GitHub contributor, which raises the question of what "made entirely by AI" means for licensing and attribution.
