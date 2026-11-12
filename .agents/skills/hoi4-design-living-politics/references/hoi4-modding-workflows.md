# HOI4 implementation and review workflow

Use the public skill set at <https://github.com/eightman999/hoi4-modding-skills/tree/master/skills> as a procedural source. Keep this file as a concise crosswalk; consult the source skill when its exact workflow or an unfamiliar command matters. Do not copy another mod's story or code without checking its license and compatibility.

## Focus trees and layout

Apply `hoi4-nf-creator`, `hoi4-focus-searcher`, and `hoi4-gfx-searcher`:

- Search existing IDs, localization, prerequisites, icons, and patterns before adding or changing a focus.
- Keep focus IDs stable unless the owner approves a migration. Give each focus an intentional cost, prerequisite, availability condition, icon, AI behavior, localized title/description, and gameplay reward.
- In HOI4 focus syntax, multiple focus references in one `prerequisite = {}` block are alternatives; separate prerequisite blocks are cumulative requirements. Preserve that distinction. Multiple prerequisite blocks are not an error.
- Resolve every `relative_position_id` recursively before making layout judgments. Check cycles, unresolved anchors, duplicate cells, small card gaps, parent/child direction, long diagonals, and line paths that may cross other cards.
- Treat geometry lint as a screening pass. Inspect a full-tree render from HOI4 Mod Utilities or the game, including edges, labels, palette clearance, zoom and the farthest branches. Clearly label any hand-built diagram as schematic.
- Prefer the owner's requested vanilla focus sprites. Verify sprite IDs against actual vanilla/mod GFX definitions; do not infer validity only from a guessed DDS filename.

## Scripted gameplay

Apply `hoi4-event-helper`, `hoi4-decisions-helper`, `hoi4-scripted-effect-maker`, `hoi4-scripted-triggers-helper`, `hoi4-variable-helper`, `hoi4-on-actions-helper`, `hoi4-opinion-modifiers-helper`, and `hoi4-modifier-maker`:

- Establish and document scope (`ROOT`, `FROM`, country/state/character) at every scripted boundary. Verify the receiving scope before calling nested effects or triggers.
- For each event chain, check event IDs, trigger/target country, options, localized title/description/options, AI choice, flags set and cleared, retries, and every branch's terminal state. Make meaningful event options and avoid hidden, unrecoverable dead ends.
- For each decision, check category, visibility, availability, cost, cooldown, one-shot behavior, AI weight, and effect. Test whether the AI can repeatedly spend resources or enter a dead end.
- Initialize every custom variable before it is read; define its bounds, sources, sinks, and clamping. For seat counts/other collections, check integer values, conservation, non-negativity, and all edge cases.
- Use `on_actions` only for recurring or event-driven behavior. Record callback frequency and scope; guard per-country callbacks by tag/flag/condition, avoid duplicate work, and do not use weekly/monthly callbacks as startup initialization.
- Confirm modifier/effect names against a working vanilla or project example or authoritative documentation. Static parsing does not prove that the game recognizes a command.

## Content, UI and assets

Apply `hoi4-idea-creator`, `hoi4-scripted-localisation-helper`, `hoi4-gui`, `hoi4-image-asset-creator`, and `techtree-creator` where applicable:

- For ideas and dynamic modifiers, check unique IDs, icon/picture names, scope, duration/removal behavior, localization, and effect relevance.
- For scripted localization, test each branch in its actual calling scope and with unset, boundary, and normal variable values.
- For GUI, match window names, scripted-GUI names, property names, frame bindings, and click effects exactly; check all bound icons and localization keys. Inspect actual in-game layout at more than one UI scale when possible.
- For graphics, inspect existing consumers and neighboring assets first. Preserve user artwork, dimensions, alpha, encoding and compression requirements; do not fabricate historical flags or overwrite supplied assets.
- Apply tech-tree/unit-design workflows only when the mod actually defines or changes technologies, equipment variants, or unit designs. Validate template equipment and required tech against the target HOI4 version.

## Localization and release QA

- Use the requested language and filename convention; preserve UTF-8 BOM where required by the project. Check key coverage, duplicate keys, duplicate displayed focus titles, descriptions that disagree with effects, and missing event/decision/idea/UI strings.
- Run the narrow validator after each edit, then the whole-project validator. Preserve unrelated files and user-authored changes; inspect the diff.
- Regenerate manifests, previews, and validation reports whenever inputs change. Include source version/hash and tested scope so stale reports cannot present an old focus count as current.
- Report separately: parser/static checks, external renderer checks, and tests that require launching the target HOI4 build. Never claim an engine test from a text parser or a schematic preview.
