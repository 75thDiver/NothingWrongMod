# Continuous Focus template

File: `common/continuous_focus/<xxx>.txt`
Use `continuous_focus_position = { x = y = }` to position the palette in the focus tree; see `focus-template.md`.

## Structure

```pdx
continuous_focus_palette = {
	id = generic_focus
	default=yes
	reset_on_civilwar = no
	position = { x = 50 y = 1000 }

	country = {
		factor = 1
		# modifier = { factor = 0 tag = XXX } etc.
	}

	focus = {
		id = TAG_continuous_industry
		icon = GFX_goal_continuous_non_factory_construct

		available = {
			# Display/optional conditions
		}
		enable = {
			# Requires continuous satisfaction during activation (can be divided with available)
		}

		modifier = {
			production_speed_buildings_factor = 0.05
		}

		daily_effect = {
			# Optional: daily effects
		}

		select_effect = {
			# When clicked
		}
		complete_effect = {
			# When canceled/completed (subject to the original field)
		}

		ai_will_do = {
			base=1
		}

		supports_ai_strategy = ai_focus_war_production
	}
}
```
## Key Points

| Field | Description |
|------|------|
| `continuous_focus_palette` | A whole continuous national focus panel |
| `country` | Which countries use this panel (weights) |
| `focus` | A single continuous national focus |
| `modifier` | Country modifier during activation |
| `supports_ai_strategy` | Hooks `ai_focuses` Research Focus |
| `position` | The coordinates of the panel in the national focus interface; there is also `continuous_focus_position` in the tree |

- Only limited bars can usually be active at the same time (engine rules, subject to version)
- Icon multi-purpose `GFX_goal_continuous_*` (`gfx-registration-template.md`)
- Does not replace ordinary national focuses; ordinary trees still use `national_focus`

## Localization

```yaml
  TAG_continuous_industry: "Continuous Industrial Mobilization"
  TAG_continuous_industry_desc: "Description."
```

## Related

- `focus-template.md` / `ai-template.md` / `modifiers-index-template.md`
