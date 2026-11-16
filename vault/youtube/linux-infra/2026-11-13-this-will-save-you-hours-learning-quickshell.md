---
video_id: fOFB1tYKP0c
title: "This will save you hours learning Quickshell."
url: https://www.youtube.com/watch?v=fOFB1tYKP0c
watched: 2026-10-25 22:26
source: chrome:Default
topic: linux-infra
indexed: 2026-11-13T02:58:49+00:00
type: youtube-note
source_url: https://www.youtube.com/watch?v=fOFB1tYKP0c
tags: [youtube, youtube/linux-infra]
---


## Core Concept
This video teaches the practical workflow for reading live system data in QuickShell: start from a `PanelWindow`, then navigate the QuickShell documentation from an "uncreatable" type up to its singleton service, following property chains (and `ObjectModel` lists) until you reach the value you want to display — demonstrated end-to-end with Wi-Fi network name and signal strength.

## Key Takeaways
- Imports needed: `Quickshell` (for `PanelWindow` and anchors), `QtQuick` (text, etc.), and `QtQuick.Layouts` (layout).
- A top bar is a `PanelWindow` with `anchors.top/left/right: true` and `implicitHeight: 40`; no `width` because anchoring stretches it across the screen. `implicitHeight` is preferred over `height` so overflowing modules aren't cut off.
- Bar color set to a near-black "Material black"; sample text "hello world" in a light color ("E8 E A"), centered with `anchors.centerIn: parent`.
- Run the shell with `qs -p .` (spoken as "QS-P dot"); check version with `qs --version` (0.3.1 in the video).
- Use `quickshell.org` docs: the search box is the primary tool, and you must switch to the latest version because type names differ by version.
- Searching "signal strength" leads to the `WifiNetwork` type (a subtype of `Network`), whose `signalStrength` is a real number from 0.0 to 1.0 (multiply by 100 for a percentage).
- `WifiNetwork` and `Network` are marked "uncreatable": you cannot instantiate or dot into them directly; you must climb to the `Networking` singleton in `Quickshell.Net.Networking`.
- From `Networking`, use `.devices` (an `ObjectModel<NetworkDevice>`); convert to a usable list with `.values`, then take index 0 (e.g. interface `wlp3s0`, found via `ip -c a`).
- Each `NetworkDevice` has `.networks` (an `ObjectModel<Network>`); use `.values.find(n => n.connected)` to get the connected network, then read `.name` and `.signalStrength`.
- Properties are exposed as `readonly property var` (e.g. `wifiName`, `wifiStrength`) and bound into a `Text`.
- The same "climb the type ladder" approach applies to other services like PipeWire (volume) and power (battery), though those aren't demonstrated.
- Promotional: "Hyper Accelerator" and "Hyper Accelerator Max" courses, plus a "Dynamite" dynamic-island shell and a "pill bar" starter.

## Technical Details
- Imports:
  ```qml
  import Quickshell
  import QtQuick
  import QtQuick.Layouts
  ```
- Panel window:
  ```qml
  PanelWindow {
      anchors.top: true
      anchors.left: true
      anchors.right: true
      implicitHeight: 40
      color: "Material black"   // near-black dark gray

      Text {
          text: "hello world"
          color: "#E8EA..."     // spoken as "E8 E A"
          anchors.centerIn: parent
      }
  }
  ```
- Networking import and property chain (as described):
  ```qml
  import Quickshell.Net.Networking

  readonly property var wifiName: Networking.devices.values[0].networks.values.find(n => n.connected).name
  readonly property var wifiStrength: Networking.devices.values[0].networks.values.find(n => n.connected).signalStrength * 100
  ```
- Display binding (spoken result: "Atlantis 82%"):
  ```qml
  Text {
      text: wifiName + " " + wifiStrength + "%"
  }
  ```
- Commands mentioned: `qs -p .` (run), `qs --version` (version check, 0.3.1), `ip -c a` (list network interfaces).
- Documentation concepts: "uncreatable" badge means a type cannot be instantiated directly; "singleton" badge means the type is the entry point (start queries there); `ObjectModel<T>` is a typed list/view requiring `.values` before indexing or `.find`.
- Trade-off note: index `[0]` of devices assumes a single (wireless) interface; with both wired and wireless connected, device ordering may differ.

## Questions
- What is the exact QML import path for the networking service (`Quickshell.Net.Networking` vs. a `Services` namespace)? Verify against installed QuickShell 0.3.1.
- Does `.values[0]` reliably select the wireless interface when multiple devices are present, or should the device be filtered by type/name?
- What are the exact color strings used ("Material black", "E8 E A") — are these theme/material names or hex values?
- The transcript only demonstrates networking; how do PipeWire (volume) and power (battery) services expose their equivalent singletons and property chains?
- Does `signalStrength` update reactively in bindings as shown, and what is the update cadence? (Video asserts it updates but doesn't specify.)
<!-- yt-brain:related -->

## Related

- [[youtube/YouTube Knowledge Base|◻️ YouTube Knowledge Base]]
- [[youtube/linux-infra|📁 Linux & Infrastructure]]
- [[index|🏛️ JARVIS Memory Vault]]

### Related notes

- [[youtube/linux-infra/2026-11-13-how-to-setup-and-customize-quickshell-on-hyprland|How to Setup and Customize Quickshell on Hyprland]] · relevance 0.11
- [[youtube/linux-infra/2026-11-13-omarchy-explained-a-deep-dive|Omarchy Explained: A Deep Dive]] · relevance 0.07
- [[youtube/linux-infra/2026-09-29-paperclip-ai-is-insane-build-a-company-run-entirely-by-ai|Paperclip AI Is Insane \| Build a Company Run Entirely by AI]] · relevance 0.06
- [[youtube/agents/2026-10-03-how-to-build-an-agentic-software-factory|How to build an Agentic Software Factory]] · relevance 0.05

<!-- /yt-brain:related -->
