# HOI4 production rules

## No guessing
- When writing comments that involve something you do not recognize, e.g. `state_xxx` (suppose this is a state ID), do not assume it is "the Estonian region". Look up the corresponding localization and find what it is actually called instead of inventing a name.


## Mandatory backup before editing existing files

**Hard rule**: Before every edit to an **existing file**, create a backup first; after the edit, compare against the backup to check whether anything was broken; delete the backup only after confirming it is fine; if there is a problem, fix/restore first, then delete the backup.

### Process (do not skip)

1. **Backup before editing**
   - Target: existing files about to be rewritten (`.txt` / `.yml` / `.mod` / `.gfx` / `.gui`, etc.).
   - Put the backup in the same directory or a project temp directory; include a timestamp in the name, e.g. `RSC.txt.bak_YYYYMMDD_HHMMSS`
   - New files do not need a backup.
   - If the same pass edits multiple existing files, **each** must get its own backup.

2. **Then edit**
   - Start writing only after the backup succeeds.
   - Do not insert/truncate/fully rewrite an existing file without a backup.

3. **Compare after editing**
   At least check:
   - Whether the file became obviously shorter / was truncated
   - Whether braces `{}` are balanced (script-like files)
   - Whether original key blocks still exist (e.g. original idea lists, the main focus tree body)
   - That this pass only adds/changes what was intended and does not delete unrelated content
   - That file encoding is still the original encoding (must not be silently changed mid-edit)

4. **Cleanup**
   - **No issues**: delete the corresponding backup.
   - **Issues found**: restore from the backup or repair to the correct state, then delete the backup.
   - Do not leave long-lived piles of `.bak_*` (delete as soon as repair is done).

### Forbidden

- Editing an existing file without a backup
- Deleting the backup without comparing after the edit
- Discovering a problem but deleting the backup without restoring/fixing
- Using "we have git anyway" as a substitute for this rule (this project may have no usable git history)

## Localization writing rules

When writing any localization text (focus names/descriptions, event titles and bodies, news, ideas, decisions, leader names, etc.), **first look up and match vanilla localization tone**, then write.

- Prefer matching the style of similar content under HOI4 base `localisation/simp_chinese/` (or the language directory used by the project).
- For news events, match vanilla `news.*` (usually in `events_l_simp_chinese.yml`).
- For focuses/events/ideas, match similar vanilla entries: short titles, telegraphic/diplomatic observational tone, little literary lyricism, little mechanic-manual wording.
- Use common vanilla dynamic-key styles (e.g. `[TAG.GetNameDef]`, `[TAG.GetLeader]`); separate paragraphs with `\n\n`.
- Do not write as uniform essay prose, player inner monologue, or "design document" explanations (e.g. directly narrating BOP/path mechanics).
- If the project already has a localization style, constrain by both project style and vanilla tone; if they conflict, ask the user first.

## File encoding rules

Before editing HOI4 `.txt` or `.yml` files, check the file encoding format first.

- Prefer Python with `utf-8-sig` for read/write.
- When Chinese mojibake appears, try recovering via `gbk` or `latin1` recoding.
- **Strictly forbidden** to write Chinese content directly with PowerShell `Set-Content`.

## Numeric design principles

- **5% rule**: percentage-like bonuses use `0.05` (i.e. 5%) as the base unit.
- **0.01 rule**: daily-value bonuses (e.g. political power, command power, ideology drift) use `0.01` as the base unit.

## National focus effect rules

A focus `completion_reward` **must not grant country-level modifiers directly**. Maintain effects through `add_ideas` or `add_timed_idea` national spirits (ideas).
A focus may also grant: IDEA/research bonus cards/army XP/command power/tech/buildings/company funds, etc.

```pdx
completion_reward = {
    add_ideas = RYH_5123i # Add proportional taxation national spirit
}
```

```pdx
completion_reward = {
    add_timed_idea = {
        idea = RYH_51i # Add temporary national spirit: popular national reconstruction
        days = 365 # Lasts 365 days
    }
}
```

## National spirit icon rules

In idea definitions, the `picture` field only needs a placeholder `picture = `; then tell the user to fill in the icon name themselves.

```pdx
RYH_5121i = {
    picture =
    modifier = {
        # ...
    }
}
```

## National spirit comment rules

A single-line comment above an idea should stay clean: **only the idea's display name**, without colon-appended explanatory descriptions after the name.

```pdx
# Establish national poverty relief
RYH_5121i = {
    # ...
}
```

## Code comment rules

Write code comments line by line and name the concrete operation target; avoid vague umbrella wording.

- ✅ `add_ideas = RYH_5121i # Add national poverty relief national spirit`
- ❌ `add_ideas = RYH_5121i # Add national spirit`

### No vague descriptive comments

Comments must state the **concrete operation and target**. Pure intent/background fluff is not allowed.

- ✅ `add_political_power = 100 # Add 100 political power`
- ❌ `add_political_power = 100 # Support private enterprise and unleash the private economy`

Background explanation belongs in focus/event/idea localization descriptions, not in code comments.

### Comments involving states

When focus effects act on concrete states (`add_resource`, `add_building_construction`, `add_extra_state_shared_building_slots`, etc.), comments **must use the state's localized name**, and the name language must match the project's comment language. Do not only use `state_XXX` IDs, and do not use fuzzy regional labels (e.g. "central mining region", "western industrial region").

- ✅ `205 = { add_resource = { type = steel amount = 8 } } # Kaluga`
- ❌ `205 = { add_resource = { type = steel amount = 8 } } # state 205`
- ❌ `205 = { add_resource = { type = steel amount = 8 } } # STATE_205`
- ❌ `# Increase steel resources in the central mining region`

Order for looking up state names:
1. Prefer the current mod's `localisation/<project-language>/state_names_l_<project-language>.yml`.
2. If the mod has none, check HOI4 base `localisation/<project-language>/state_names_l_<project-language>.yml`.
3. Only if still missing may you use `STATE_XXX` IDs or the original file name as the comment, and notify the user that the state name was not found.

## Handling effects that loop over states

### Specified state vs looped states

- When effects act on a **clearly specified concrete state** (e.g. `219 = { add_building_construction = ... }`), the game shows a tooltip automatically; no `hidden_effect` and no `custom_effect_tooltip` are needed.
- When effects need to **loop over multiple states or countries** (e.g. `every_state`, `every_neighbor_country`), the loop logic must go inside `hidden_effect`, and you must hand-write `custom_effect_tooltip`.

### How to write loop effects

When a focus reward must loop over multiple states (e.g. `add_claim_by`, `add_core_of`, `add_resource`, `add_building_construction`, `add_extra_state_shared_building_slots`), put the loop logic inside `hidden_effect` and show a summary via top-level `custom_effect_tooltip`.

- ✅ Keep `custom_effect_tooltip` at the top level of `completion_reward`.
- ✅ Write concrete `every_state` / `every_controlled_state` / `every_neighbor_country` loops inside `hidden_effect`.
- ❌ Do not expose a long chain of state effects at the top level, which makes tooltips too long.

Example:

```hoi4
completion_reward = {
    custom_effect_tooltip = RYH_1_claim_tt # Gain claims on RSC-controlled areas
    hidden_effect = {
        every_state = {
            limit = {
                is_controlled_by = RSC
                NOT = { is_core_of = RYH }
            }
            add_claim_by = RYH
        }
    }
}
```

## Dynamic national spirit tooltip rules

When adding a dynamic national spirit with `add_dynamic_modifier`, if modifier values are variable-driven the game will not auto-show concrete effects; you must hand-write `custom_effect_tooltip`. Full flow, examples, and rules: `references/dynamic-modifier-template.md`.

- **First time gaining this dynamic national spirit**: use `Gained §Y<name>§!:` as the tooltip title.
- **Later continued strengthening of the same dynamic national spirit**: use `§Y<name>§! Additional effects:` as the tooltip title.
- Write each modifier as its own localization key so lines can be output one by one for line breaks.
- `add_dynamic_modifier` may sit inside `hidden_effect`, but `custom_effect_tooltip` must stay at the top level of `completion_reward`.
- Ordinary ideas do not need `custom_effect_tooltip`; only dynamic national spirits do.

Example:

```yaml
  RSC_WY_tt: "§YKardashev's Great Cause§! Additional effects:"
  RSC_WY_tt1: " $MODIFIER_RESEARCH_SPEED_FACTOR$:§G +10.00%§!\n $MODIFIER_CONSUMER_GOODS_FACTOR$:§Y +10.00%§!"
```

## common directory gap-check

When unsure whether a `common/` subdirectory has a template, check `references/common-directory-index.md` first.
This gap-fill pass added: continuous focuses, occupation/resistance, game rules, tech sharing, tag aliases, raids, commander abilities, aces/medals, idea_tags, state_category/terrain, doctrine overview, script_constants.

## Advanced content references

Lower-priority / advanced topics (Scripted GUI, super events, Defines, map, models, music, fonts, shaders, map modes, dynamic place names, diplomacy button locks, debug):

- `references/scripted-gui-template.md`
- `references/super-event-template.md`
- `references/defines-template.md`
- `references/map-modding-template.md`
- `references/unit-models-template.md`
- `references/music-radio-template.md`
- `references/fonts-template.md`
- `references/shaders-template.md`
- `references/map-modes-template.md`
- `references/dynamic-renaming-template.md`
- `references/diplomacy-enable-triggers-template.md`
- `references/debug-workflow-template.md`

## Extended content references

Medium-priority system templates (bookmarks, new countries, GFX, ideologies, traits, autonomy, wargoals, resources/supply, name pools, tech files, modifier index, version migration):

- `references/bookmarks-template.md`
- `references/new-country-template.md`
- `references/gfx-registration-template.md`
- `references/ideologies-template.md`
- `references/custom-traits-template.md`
- `references/autonomy-template.md`
- `references/wargoals-peace-template.md`
- `references/resources-supply-template.md`
- `references/names-template.md`
- `references/technology-file-template.md`
- `references/modifiers-index-template.md`
- `references/version-migration-template.md`

## Language foundation references

When writing effects/triggers/scopes/variables/on_actions/scripted_effects, or handling `.mod` and localization syntax, also consult (beyond this rules file):

- `references/mod-structure-template.md` — mod structure, load order, `replace_path`
- `references/scopes-template.md` — scopes
- `references/effects-template.md` — effects
- `references/triggers-template.md` — triggers
- `references/variables-arrays-template.md` — variables and arrays
- `references/scripted-effects-template.md` — scripted effects
- `references/on-actions-template.md` — on_actions
- `references/localisation-syntax-template.md` — localization syntax (tone still follows this file's "Localization writing rules")

## Lookup and research order

When you do not know something or are unsure about a writing style:

1. First check this skill's references files.
2. Then check other files under the same directories in the current mod project.
3. Then check the user's HOI4 base install (e.g. `D:\Steam\steamapps\common\Hearts of Iron IV`).
4. If none of the above works or context is still missing, ask the user.
