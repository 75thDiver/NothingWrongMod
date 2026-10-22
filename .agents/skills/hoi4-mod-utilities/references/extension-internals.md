# HOI4 Mod Utilities: inspected behavior

These notes describe the local VS Code installation inspected on 22 October 2026. Verify the installed extension version before relying on them.

## Installation inspected

- VS Code CLI: `E:\Microsoft VS Code\bin\code.cmd`
- Extension ID: `chaofan.hoi4modutilities`
- Installed version: `0.18.1`
- Extension directory: `%USERPROFILE%\.vscode\extensions\chaofan.hoi4modutilities-0.18.1`
- Main manifest: `package.json`
- Bundled implementation: `dist/extension.js` and `dist/web-extension.js`

## Relevant commands

The manifest registers these command IDs:

- `hoi4modutilities.preview` — preview the active supported HOI4 file
- `hoi4modutilities.previewworld` — world map preview
- `hoi4modutilities.scanreferences` — scan references
- `hoi4modutilities.selectmodfile` — select the active `.mod` descriptor
- `hoi4modutilities.selecthoifolder` — select the HOI4 install directory

The commands are registered through the VS Code extension API. `code --list-extensions --show-versions` can confirm installation, but the CLI does not expose a general `code --command <extension-command>` invocation. Use the VS Code command palette or an available VS Code UI automation surface to launch previews.

## Focus-tree parser and preview path

In version 0.18.1, the bundled extension contains `FocusTreeLoader`. It parses Paradox/Clausewitz script from `.txt` files using the extension's parser schema. The relevant schema includes `focus_tree`, `shared_focus`, `joint_focus`, focus IDs, icons, coordinates, `relative_position_id`, prerequisites, mutual exclusions, allow-branch conditions, and continuous-focus placement.

The loader resolves shared focuses from indexed focus files, reads title-bar styles and interface/GFX dependencies, builds a focus-tree data model, and passes it to the extension's webview preview. The local implementation is bundled/minified in `dist/extension.js`; class names such as `FocusTreeLoader` can be used as search anchors. The preview is not based on an XML export: the input is Clausewitz script, with supporting localisation/GFX resources.

## Setup for an actual preview

1. Open the mod development folder as the VS Code workspace.
2. Configure `hoi4ModUtilities.installPath` or run “Select HOI4 install path”.
3. Optionally select the `.mod` descriptor with “Select mod file”.
4. Open a supported file such as `common/national_focus/14_nw_SOV.txt` and run “Preview HOI4 file” from the command palette or editor toolbar.
5. Inspect the complete rendered tree, including far edges, connections, labels, and palette clearance. Treat the preview as an extension rendering, not proof that the game accepts every script command.

If the current agent session cannot control VS Code, ask the user to run the command and provide a screenshot or relevant output. Continue with source-level analysis in parallel where useful.

## Limits

- The extension's preview is a visual aid; it does not replace validation in the target HOI4 build.
- Bundled parser code is implementation evidence, not a stable public API. Do not import or patch minified bundle code as a normal project dependency.
- Confirm names, scopes, effects, GFX, localisation, and map facts from the active mod and target game files.
- Never modify `history/states/` or map data for Nothing Wrong without an explicit map assignment.
