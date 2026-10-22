---
name: hoi4-modding
description: Guide for Hearts of Iron IV modding tasks. Use when the user is working on HOI4 mods, including editing national focuses, events, ideas, characters, localization, OOB, state files, or any other HOI4 script files.
---

# HOI4 Modding

Follow the rules in [references/modding-rules.md](references/modding-rules.md) for all HOI4 modding work.

## Reference Files

### Core rules and language foundation

- `references/modding-rules.md` — Core rules for HOI4 modding (encoding, comments, tooltips, loc flavor, design units).
- `references/mod-structure-template.md` — `.mod` / `descriptor.mod`, load order, `dependencies`, `replace_path`.
- `references/scopes-template.md` — Scopes (`ROOT`/`FROM`/`PREV`), `every_*`/`any_*`, event targets.
- `references/effects-template.md` — Common effects and where to use them.
- `references/triggers-template.md` — Common triggers, logic blocks, `allowed`/`available`/`visible`.
- `references/variables-arrays-template.md` — Variables, arrays, collections, event targets, loc display.
- `references/scripted-effects-template.md` — Reusable `common/scripted_effects` blocks.
- `references/on-actions-template.md` — `common/on_actions` hooks and ROOT/FROM discipline.
- `references/localisation-syntax-template.md` — YML encoding, color codes, dynamic keys, variables in loc.

### Content system templates

- `references/focus-template.md` — National focus tree templates and field reference.
- `references/decision-template.md` — Decision category and decision templates.
- `references/event-template.md` — Country event and news event templates.
- `references/mio-template.md` — Military industrial organization (MIO) templates and equipment bonuses.
- `references/idea-template.md` — Laws, national spirits, and manufacturer advisors.
- `references/subdoctrine-template.md` — Sub-doctrine templates and mastery rewards.
- `references/special-projects-template.md` — Special projects, specializations, scientists, and facilities.
- `references/bop-template.md` — Balance of power (BOP) templates.
- `references/ai-template.md` — AI areas and AI strategies.
- `references/equipment-template.md` — Equipment archetypes and variants.
- `references/equipment-module-template.md` — Tank, plane, and ship equipment modules.
- `references/equipment-variant-template.md` — Create equipment variant examples and parts lists.
- `references/unit-template.md` — Sub unit definitions and icon registration.
- `references/country-history-template.md` — Country history file structure and starting effects.
- `references/oob-template.md` — Order of battle and production line setup.
- `references/state-template.md` — State/province definitions and buildings.
- `references/advisor-traits-template.md` — Vanilla advisor slots and trait effects.
- `references/character-template.md` — Character definitions for leaders, advisors, commanders, scientists.
- `references/opinion-modifiers-template.md` — Diplomatic opinion modifiers.
- `references/scripted-triggers-template.md` — Scripted triggers and scripted localisation.
- `references/buildings-template.md` — Custom building definitions and spawn points.
- `references/intelligence-diplo-template.md` — Operatives, intelligence operations, and scripted diplomatic actions.
- `references/faction-system-template.md` — Faction templates, goals, manifests, rules, member upgrades, and AI FI spending.
- `references/dynamic-modifier-template.md` — Dynamic national spirits with variable-driven modifiers and tooltip conventions.

### Extended content (medium priority)

- `references/bookmarks-template.md` — Bookmarks / scenario select screen.
- `references/new-country-template.md` — Full new-country checklist (tag → history → flag → loc).
- `references/gfx-registration-template.md` — `.gfx` sprite registration (goals, ideas, events, shine, flags).
- `references/ideologies-template.md` — Ideologies and sub-ideologies.
- `references/custom-traits-template.md` — Custom country_leader and unit_leader traits.
- `references/autonomy-template.md` — Autonomous states / puppet levels.
- `references/wargoals-peace-template.md` — Wargoals, declare war, peace conference AI hooks.
- `references/resources-supply-template.md` — Resources, railways, supply nodes, strategic regions.
- `references/names-template.md` — Name pools and division name groups.
- `references/technology-file-template.md` — Technology file structure (not just ID lists).
- `references/modifiers-index-template.md` — Where modifiers live and how to look up keys.
- `references/version-migration-template.md` — Version adaption / migration checklist.

### Gap-fill (common coverage)

- `references/common-directory-index.md` — Full `common/` folder → skill page map; check here before inventing systems.
- `references/continuous-focus-template.md` — Continuous focus palettes.
- `references/occupation-resistance-template.md` — Occupation laws, resistance/compliance.
- `references/game-rules-template.md` — Pre-game rules and `has_game_rule`.
- `references/technology-sharing-template.md` — Technology sharing groups.
- `references/country-tag-aliases-template.md` — Dynamic country tag aliases.
- `references/raids-template.md` — Raid types.
- `references/abilities-template.md` — Commander abilities (command power).
- `references/aces-medals-template.md` — Aces and unit medals.
- `references/idea-tags-template.md` — Idea category / advisor slot layout.
- `references/state-category-terrain-template.md` — State categories and terrain.
- `references/doctrine-system-template.md` — Grand doctrine / tracks / mastery overview.
- `references/script-constants-template.md` — `script_constants` and `constant:` values.

### Advanced / low priority

- `references/scripted-gui-template.md` — Scripted GUI + `.gui` wiring.
- `references/super-event-template.md` — Super event (big event UI) community pattern.
- `references/defines-template.md` — `common/defines` Lua overrides (use sparingly).
- `references/map-modding-template.md` — Map folder responsibilities and safe vs unsafe edits.
- `references/unit-models-template.md` — 3D unit models / entities entry.
- `references/music-radio-template.md` — Music assets, songs lists, radio.
- `references/fonts-template.md` — Bitmap fonts registration.
- `references/shaders-template.md` — `gfx/FX` shaders entry (advanced).
- `references/map-modes-template.md` — Scripted map modes.
- `references/dynamic-renaming-template.md` — Dynamic place-name renaming entry.
- `references/diplomacy-enable-triggers-template.md` — Lock diplomacy buttons via fixed scripted_trigger names.
- `references/debug-workflow-template.md` — error.log workflow and debugging order.

### Data quick-reference

- `references/data/tech-list.md` — Vanilla technology code reference.
- `references/data/doctrine-list.md` — Vanilla doctrine and sub-doctrine codes.
- `references/data/equipment-list.md` — Vanilla equipment codes for bonuses and OOB.
- `references/data/state-modifiers.md` — State categories and national spirit modifier keys.

## Workflow

1. Read `references/modding-rules.md` before making changes.
1b. **Hard rule — backup before editing existing files:** Before modifying any existing file, create a timestamped backup; after the edit, compare against the backup for truncation, missing blocks, or brace imbalance; if clean, delete the backup; if broken, restore/fix then delete the backup. See `references/modding-rules.md` section "Mandatory backup before editing existing files". Never skip this.
2. When editing `.mod` / `descriptor.mod`, load order, `dependencies`, or `replace_path`, check `references/mod-structure-template.md`.
3. When writing scopes, `ROOT`/`FROM`/`PREV`, or `every_*`/`any_*` blocks, check `references/scopes-template.md`.
4. When writing or looking up effects, check `references/effects-template.md`.
5. When writing or looking up triggers / `limit` / `available` / `visible`, check `references/triggers-template.md`.
6. When writing variables, arrays, collections, or event targets, check `references/variables-arrays-template.md`.
7. When writing reusable scripted effects, check `references/scripted-effects-template.md`.
8. When writing `on_actions` hooks, check `references/on-actions-template.md`.
9. When writing localization files (syntax, color codes, dynamic keys), check `references/localisation-syntax-template.md` and match vanilla flavor per `modding-rules.md`.
10. When writing a national focus, check `references/focus-template.md`.
11. When writing a decision, check `references/decision-template.md`.
12. When writing an event, check `references/event-template.md`.
13. When writing an MIO, check `references/mio-template.md`.
14. When writing an idea, check `references/idea-template.md`.
15. When writing a sub-doctrine, check `references/subdoctrine-template.md`.
16. When writing a special project, check `references/special-projects-template.md`.
17. When writing a balance of power, check `references/bop-template.md`.
18. When writing AI behavior, check `references/ai-template.md`.
19. When writing equipment, check `references/equipment-template.md`.
20. When writing equipment modules, check `references/equipment-module-template.md`.
21. When creating equipment variants, check `references/equipment-variant-template.md`.
22. When writing units, check `references/unit-template.md`.
23. When writing country history, check `references/country-history-template.md`.
24. When writing OOB or production lines, check `references/oob-template.md`.
25. When writing states, check `references/state-template.md`.
26. When assigning vanilla advisor traits, check `references/advisor-traits-template.md`.
27. When writing characters, check `references/character-template.md`.
28. When adding diplomatic opinion modifiers, check `references/opinion-modifiers-template.md`.
29. When writing scripted triggers or scripted localisation, check `references/scripted-triggers-template.md`.
30. When writing buildings, check `references/buildings-template.md`.
31. When writing intelligence operations or diplomatic actions, check `references/intelligence-diplo-template.md`.
32. When writing a faction system, check `references/faction-system-template.md`.
33. When writing a dynamic national spirit, check `references/dynamic-modifier-template.md`.
34. When writing bookmarks / scenario select, check `references/bookmarks-template.md`.
35. When creating a new country (tag, color, history, flag, loc), check `references/new-country-template.md`.
36. When registering GFX (focus icons, idea icons, event pics, shine, flags), check `references/gfx-registration-template.md`.
37. When editing ideologies or sub-ideologies, check `references/ideologies-template.md`.
38. When writing custom leader or unit leader traits, check `references/custom-traits-template.md`.
39. When defining or setting autonomy/puppet levels, check `references/autonomy-template.md`.
40. When writing wargoals, war declaration, or peace conference AI, check `references/wargoals-peace-template.md`.
41. When placing resources, railways, supply nodes, or strategic regions, check `references/resources-supply-template.md`.
42. When writing name pools or division name groups, check `references/names-template.md`.
43. When writing technology files (tree structure, not only IDs), check `references/technology-file-template.md`.
44. When looking up or placing modifier keys, check `references/modifiers-index-template.md` then `references/data/state-modifiers.md`.
45. When adapting a mod to a new game version, check `references/version-migration-template.md`.
46. When writing scripted GUI or custom `.gui` windows, check `references/scripted-gui-template.md`.
47. When implementing super events (big event UI), check `references/super-event-template.md`.
48. When editing defines, check `references/defines-template.md` (prefer minimal overrides).
49. When editing map files or province layout, check `references/map-modding-template.md`.
50. When replacing unit 3D models/entities, check `references/unit-models-template.md`.
51. When adding music or radio stations, check `references/music-radio-template.md`.
52. When adding or changing fonts, check `references/fonts-template.md`.
53. When editing shaders under `gfx/FX`, check `references/shaders-template.md`.
54. When writing scripted map modes, check `references/map-modes-template.md`.
55. When implementing dynamic place renaming, check `references/dynamic-renaming-template.md`.
56. When locking diplomacy actions, check `references/diplomacy-enable-triggers-template.md`.
57. When debugging load errors or unexpected behavior, check `references/debug-workflow-template.md`.
58. When auditing which `common/` systems exist vs this skill, check `references/common-directory-index.md`.
59. When writing continuous focuses, check `references/continuous-focus-template.md`.
60. When writing occupation laws or resistance/compliance, check `references/occupation-resistance-template.md`.
61. When writing game rules or AI path rules, check `references/game-rules-template.md`.
62. When writing technology sharing groups, check `references/technology-sharing-template.md`.
63. When writing country tag aliases, check `references/country-tag-aliases-template.md`.
64. When writing raids, check `references/raids-template.md`.
65. When writing commander abilities, check `references/abilities-template.md`.
66. When writing aces or unit medals, check `references/aces-medals-template.md`.
67. When editing idea slot layout (`idea_tags`), check `references/idea-tags-template.md`.
68. When editing state categories or terrain, check `references/state-category-terrain-template.md`.
69. When working on the grand doctrine system (not only subdoctrines), check `references/doctrine-system-template.md`.
70. When defining script constants, check `references/script-constants-template.md`.
71. When looking up vanilla technology codes, check `references/data/tech-list.md`.
72. When looking up vanilla doctrine codes, check `references/data/doctrine-list.md`.
73. When looking up vanilla equipment codes, check `references/data/equipment-list.md`.
74. When looking up state categories or modifier keys, check `references/data/state-modifiers.md`.
75. When writing localization text (names/descriptions for focus/event/news/idea/decision), look up vanilla localization first and match its flavor/register.
76. When unsure about syntax or structure:
   - Check `references/common-directory-index.md` if the folder is unfamiliar.
   - Check this skill's references first (language base → content → gap-fill → advanced).
   - Check other files in the same directory within the project.
   - Check the user's HOI4 base game installation and official wiki / local library.
   - Ask the user if none of the above resolve the question.
