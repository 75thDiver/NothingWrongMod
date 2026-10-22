---
name: hoi4-project-router
description: Use when working on the Nothing Wrong Hearts of Iron IV mod and deciding which project rules or HOI4 reference skill applies.
---

# Nothing Wrong project router

Use this router for every change to Nothing Wrong. Project instructions and the owner's latest direct request have priority over all imported references.

## Required context

1. Read the repository-root `AGENTS.md` and the relevant current document under `docs/`.
2. Treat `NothingWrongMod/` as the only active game build. `HISTORY_WORKSPACE/` and archive documents are historical references, never replacement source files.
3. Do not edit `history/states/`, map IDs, provinces, owners, cores, controllers, state filenames, or capitals without an explicit map assignment. Preserve the approved state ID canon in `docs/STATE_ID_CANON.md`.
4. Preserve the protected Russian focus prerequisites and political flags listed in `AGENTS.md` unless the owner explicitly requests changes to them.
5. Keep new mechanics consistent with `docs/LORE_CURRENT.md`, `docs/MECHANICS_INDEX.md`, and the live source code. A proposal or old report is not proof that a mechanic exists.

## Selecting references

- For general HOI4 syntax and broad file-system coverage, start with `hoi4-modding/references/common-directory-index.md`, then open only the matching `*-template.md` and `modding-rules.md` sections.
- For focused work on national focuses, events, decisions, ideas, scripted effects/triggers, GUI, localisation, modifiers, variables, on_actions, GFX, or unit design, use the matching `hoi4-*-` specialist skill and its relevant references.
- Confirm commands, scopes, modifiers, equipment, technologies, and GUI fields against the active project or original game files for the target version. Imported references are leads, not authoritative engine validation.
- Preserve the project's Russian UTF-8 BOM localisation convention and existing vanilla-GFX policy.
- Follow the project's own backup, validation, and review rules. Do not blindly apply another skill's backup method if it conflicts with an explicit user instruction or the project's current workflow.

## Reporting

State whether a conclusion is based on source inspection, a static validator, a rendered interface, or an actual HOI4 run. Never describe static checks as an engine test.
