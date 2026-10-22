# Custom map mode template

File: `common/map_modes/` (see the main body `documentation.md` and examples).

## Structural concept

```pdx
scripted_map_modes = {
	TAG_test_map_mode = {
		top = {
			type = country # none / country / state / state_controller / or hardcoded game_map_mode_*
			color = {
				set_temp_variable = { red = 0.0 }
				set_temp_variable = { green = 0.5 }
				set_temp_variable = { blue = 1.0 }
				set_temp_variable = { alpha = 0.7 }
				# Calculate color according to FROM country/state
			}
		}
		bottom = {
			type=none
		}
	}
}
```

## Localization and icon conventions

Based on the map mode name, the engine looks for example:

- `MAPMODE_TAG_TEST_MAP_MODE` / `_NAME` / `_DESCRIPTION`
- `tag_test_map_mode_tooltip` etc.
- `GFX_mapmode_buttons_*_tag_test_map_mode`

The specific key names are subject to the ontology documentation and wiki.

## Layer

- `top` / `bottom` two layers, the rendering order is fixed
- `type` determines border granularity and scope (player vs FROM country/state)
- Hardcoded layers can be used to directly embed original patterns

## Performance

- `color` trigger is called for each country/state to avoid recalculation and long every
- Use the temp variable to set the color, do not change the permanent variable in color
## Specification

- Do read-only dyeing mode first, then click interaction (if the version supports it)
- Can be combined with `ai_areas` / strategic area data, but do not rely on circular dependencies

## Related

- `variables-arrays-template.md` / `scopes-template.md` / `gfx-registration-template.md` / `localisation-syntax-template.md`
