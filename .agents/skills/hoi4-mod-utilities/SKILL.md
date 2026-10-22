---
name: hoi4-mod-utilities
description: Use when inspecting, previewing, or validating Hearts of Iron IV mod files with the HOI4 Mod Utilities VS Code extension.
---

# HOI4 Mod Utilities integration

Use the installed HOI4 Mod Utilities extension as a source of parser behavior and visual previews when it is available. Follow Nothing Wrong's root `AGENTS.md` and `hoi4-project-router` skill for project constraints.

## Workflow

1. Confirm the installed extension and version with `code --list-extensions --show-versions`; inspect its local `package.json`, README, and bundled code when needed. Never modify the extension installation.
2. Identify whether the task needs the actual VS Code webview preview or only a static source audit. The extension's registered commands run inside the VS Code extension host; the `code` CLI can list extensions but does not itself invoke those commands.
3. For an actual extension preview, use UI automation only if the current session exposes VS Code control. Otherwise give the user the relevant command-palette steps and ask them to share the preview or its screenshot. Do not describe a hand-built rendering as the extension's preview.
4. For independent analysis, inspect the mod's Clausewitz files and relevant extension parser/output code. Label any generated SVG/HTML or coordinate report as an independent/static preview, not an engine or extension run.
5. Use preview findings to identify concrete source locations, then verify conclusions against the mod files. Keep project restrictions on state/map edits and protected routes in force.

## Extension capabilities

Depending on the installed version, the extension can preview focus trees, event trees, technology trees, MIOs, scripted GUI, world map, `.gfx`, `.dds`, and `.tga`. Check the local manifest instead of assuming all commands exist.

For observed parser and rendering behavior in version 0.18.1, read [extension-internals.md](references/extension-internals.md). Recheck the installed version before relying on version-specific details.
