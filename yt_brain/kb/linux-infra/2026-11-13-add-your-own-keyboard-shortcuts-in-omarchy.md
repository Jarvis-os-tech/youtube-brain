---
video_id: OUxwcLOdf1s
title: "Add Your Own Keyboard Shortcuts in Omarchy"
url: https://www.youtube.com/watch?v=OUxwcLOdf1s&pp=wgIGCgQQARgD0gcJCVAApj3NqvgS&feature=push-fr&attr_tag=gTKfcAbwJ6K8KZdd%3A6&parentCsn=6NNl23-3Ti-6rnW7&parentTrackingParams=CAYQhsUBIhMI8b_ytoHTlwMVyLeuBR0f6hoakgEYVUM5Q0Z4T0JGWUVCeEZ1QkRkZk82RHRBsgEpChZIbWJQdTd6TzhSS1cwamNOVmVPXzhBEJQBGgwI06jz1gYQuPrl9AI%3D
watched: 2026-10-24 21:24
source: chrome:Default
topic: linux-infra
indexed: 2026-11-13T03:02:37+00:00
---

## Core Concept
The video demonstrates adding personal keyboard shortcuts in Omarchy by first checking that a key combination is unused, then editing the user-owned key bindings file in Neovim, saving to apply changes immediately, and later removing or overriding bindings as needed.

## Key Takeaways
- Press `Super+K` to open the full shortcut list; navigate with arrow keys, type to filter, and note that the list calls Enter "return"; press `Escape` twice to close it.
- To reserve `Super+Shift+I`, type `super shift + I` (with the plus, as the list writes it) in the filter and confirm there are no matches.
- Press `Super+Space` to open the main menu, type `key bindings`, then arrow down once and press Enter to choose "key bindings" under "setup"; this opens the user key bindings file in Neovim.
- The user key bindings file contains explanatory comments and persists through updates; built-in shortcuts live in system files that updates replace.
- Jump to the end with `Shift+G`, open a new line with `o`, clear an accidental comment marker with `Ctrl+U`, and enter one shortcut per line using `o.bind` followed by keys, display name, and command, each in quotes; press `Escape`, then save with `:w`, which reloads desktop settings immediately.
- The first shortcut binds `Super+Shift+I` to Pinta; pressing `Super+Shift+I` opens Pinta, and `Super+W` closes it.
- The second shortcut binds `Super+Shift+T` to "copy date", piping today's date into `wl-copy` for the clipboard; nothing pops up, and it can be verified by opening a terminal with `Super+Enter`, pasting with `Super+V`, then closing the terminal with `Super+W`.
- Removing a shortcut means deleting its line with `dd` (press `D` twice), then saving with `:w`, which frees the key combination again.
- To change a built-in shortcut, add an `unbind` line for its keys first, then bind the same keys again on the next line.
- Close the editor with `:q`.
- A written guide containing every typed line is available on starryhope.com.

## Technical Details
- Terms: Omarchy, Neovim, user key bindings file, built-in system shortcuts, `o.bind`, `unbind`, `wl-copy`, clipboard.
- Architecture: user-owned shortcut definitions are separate from built-in system shortcuts; system files may be replaced by updates, while the user file persists.
- Configuration behavior: each shortcut is one line; saving with `:w` causes the desktop to reload its settings immediately, so changes take effect without a separate reload step.
- Editing flow and commands:
```
Super+K
Escape Escape
Super+Space
Shift+G
o
Ctrl+U
Escape
:w
Super+Shift+I
Super+W
Super+Shift+T
Super+Enter
Super+V
Super+W
dd
:w
:q
```
- The transcript describes the binding form as `o.bind` followed by keys, a display name, and a command, each in quotes, but does not show the exact completed line or exact command string for Pinta.
- The transcript describes changing a built-in shortcut as adding an `unbind` line for its keys, then binding those same keys again on the next line, but does not specify exact `unbind` syntax.

## Questions
- What is the exact file path of the user key bindings file on disk?
- What is the exact syntax and quoting for `o.bind` and `unbind` lines in this Omarchy version?
- What exact command opens Pinta, and what exact command produces and pipes the date?
- Does `wl-copy` need to be installed or configured separately?
- What date format does the "copy date" command produce?
- Does `Super+V` paste in all terminals and applications, or only the one shown?
- Are shortcut names and key combinations case-sensitive when typed into the filter or binding lines?
