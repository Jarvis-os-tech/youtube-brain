---
video_id: P4uzfNuSL5E
title: "How to Setup and Customize Quickshell on Hyprland"
url: https://www.youtube.com/watch?v=P4uzfNuSL5E
watched: 2026-10-25 22:13
source: chrome:Default
topic: linux-infra
indexed: 2026-11-13T03:02:11+00:00
---

## Core Concept
The video is a walkthrough of the author's Quickshell configuration on Hyprland: it demonstrates the widgets (app launcher, volume/brightness control, power menu, system monitor, static and live wallpaper switchers, and a voice assistant widget), then shows how to clone, install, and customize the config from scratch, including wallpaper-driven theming through Wallust.

## Key Takeaways
- App launcher shows recently used apps on top; navigate with arrow keys or mouse, launch with Enter; shrinks smoothly when searching.
- Volume/brightness control works (brightness not visible in recording); changing volume spawns a small widget from the bottom.
- Power menu works with arrow keys and mouse.
- System monitor widget shows CPU, RAM, and disk usage plus CPU and GPU temperatures and battery percentage.
- Static and live wallpaper switchers support arrow keys and mouse; changing wallpaper recolors the entire configuration to match.
- A widget exists for the author's voice assistant (built in a separate video).
- Setup from scratch: clone the repo (link in description), move the quick shell directory into the config directory, run `QS`, copy IPC handler commands from the README, bind keys in Hyprland.
- Customization points: update `live wallpaper switcher.qml` for the live wallpaper directory, username, thumbnail save path, and thumbnail-generation script path; update `wallpaper switcher.qml` for the static wallpaper directory; add `restore wallpaper.sh` to Hyprland config to run on startup; set the Hyprlock lock screen wallpaper path.
- `bar.qml`: launches the app launcher by clicking the arch icon, tweakable opacity, changeable logo.
- `applauncher.qml`: contains an IPC handler; adjustable width and height.
- Power menu values can be tweaked to preference.
- System monitor widget width and height are tweakable.
- `cell.qml`: add or remove entries as desired.
- Theming uses Wallust: a quick shell theme template generates `colors.qml`, which updates on wallpaper change and is used throughout the config.

## Technical Details
- Tools: Quickshell (`QS`), Hyprland, Hyprlock, Wallust.
- Files referenced: `live wallpaper switcher.qml`, `wallpaper switcher.qml`, `restore wallpaper.sh`, `bar.qml`, `applauncher.qml`, `cell.qml`, `colors.qml`, and the quick shell theme template.
- Everything in the configuration exposes IPC handlers for toggling; the commands are copied from the README.
- Run command:
  ```
  QS
  ```
- Wallpaper flow: `restore wallpaper.sh` runs automatically on PC startup; the Hyprlock path is set to match the current wallpaper; the switcher saves a thumbnail of each wallpaper for display.

## Questions
- What are the exact IPC handler command names and toggle syntax?
- What is the repository URL and the exact config directory path?
- What is the name/path of the thumbnail-generation script?
- What Hyprland keybinds are used for the widgets?
- What are the specific Wallust configuration and template locations?
- Does the live wallpaper switcher require additional dependencies?
- What are the voice assistant widget's implementation details (covered in a separate video)?
