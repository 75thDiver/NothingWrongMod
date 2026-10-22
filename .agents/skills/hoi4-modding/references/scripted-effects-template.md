# Scripted Effects template

Reusable effect blocks, defined in `common/scripted_effects/`, can be called with `name = yes` in any effect context.

## File location

`common/scripted_effects/<xxx>.txt`

## Definition

```pdx
# Example: Converting civilian to military factories (illustration)
TAG_convert_one_civ_to_arms = {
	random_owned_controlled_state = {
		limit = {
			is_fully_controlled_by = ROOT
			industrial_complex > 0
		}
		remove_building = {
			type = industrial_complex
			level=1
		}
		add_building_construction = {
			type = arms_factory
			level=1
			instant_build = yes
		}
	}
}

TAG_story_setup = {
	set_country_flag = TAG_story_started
	set_variable = { TAG_story_stage = 1 }
	add_ideas = TAG_story_spirit
}
```

Original description style (`00_scripted_effects.txt`):

```pdx
# example_effect = {
# add_political_power = 66
# }
# Call:
# effect = {
# example_effect = yes
# }
```

## Call

```pdx
completion_reward = {
	TAG_story_setup = yes # Execute script effect TAG_story_setup
}
option = {
	name = some.event.a
	TAG_convert_one_civ_to_arms = yes
}

# Same in on_actions / history
effect = {
	TAG_story_setup = yes
}
```

Do not write scripted effect** in **trigger context; use `scripted_triggers` for conditions.

## Scope

- Execute the script effect body in the **current scope** when called
- Scope can be switched within the body (`every_owned_state`, `GER = {}`, etc.)
- Switch first when you need to target other countries:

```pdx
SOV = {
	TAG_story_setup = yes
}
```

## with hidden_effect/tooltip

```pdx
completion_reward = {
	custom_effect_tooltip = TAG_convert_tt
	hidden_effect = {
		TAG_convert_one_civ_to_arms = yes
		TAG_convert_one_civ_to_arms = yes
	}
}
```

If the script effect contains `every_*`, it also follows the project traversal tooltip specification (`modding-rules.md`).

## Parameterization (common patterns)

Native scripted effects **do not** have a real parameter list; common patterns:

1. **Convention variables**: `set_temp_variable` / `set_variable` before calling, the effect is read in the body
2. **Convention event_target**: `save_event_target_as` before calling
3. **Split into multiple effects**: `TAG_setup_low` / `TAG_setup_high`
```pdx
# Before calling
set_temp_variable = { temp_pp_gain = 50 }
TAG_add_temp_pp = yes

# Definition
TAG_add_temp_pp = {
	add_political_power = temp_pp_gain
}
```

Whether a specific variable can be directly used as the rvalue of `add_political_power` depends on the version and wiki; if not, use `add_to_variable` and then handle it indirectly or check the vanilla for the same type.

## Naming convention

- Prefix + verb + object: `RYH_setup_parliament`, `RSC_clear_bop_flags`
- Avoid reading confusion caused by having the same name as trigger, idea, and national focus ID
- Globally written in `00_*.txt` style files; country-specific `TAG_scripted_effects.txt`

## When to extract scripted effect

| Suitable | Not suitable |
|------|--------|
| The same effect repeated in multiple places | Three lines of effect used only once |
| on_action shares logic with national focus | A display block that strongly relies on a single tooltip copy and cannot be hidden |
| Advancement of story stages that require unified modification | Apply conditional logic of `scripted_trigger` |

## Debugging

- It does not take effect after being called: check whether the trigger file, name spelling, and current scope are written.
- tooltip is ugly: the vanilla often has this problem, use `custom_effect_tooltip` + `hidden_effect` package to call it
- Infinite loop: Do not call itself again unconditionally within a scripted effect (unless there is an explicit termination flag)

## Query order

1. This page
2. Ontology `common/scripted_effects/`
3. wiki: **Scripted effects** (or the scripted chapter in the Effect page)
4. Ask the user
## Related documents

- `effects-template.md` / `on-actions-template.md` / `scripted-triggers-template.md` / `variables-arrays-template.md`
