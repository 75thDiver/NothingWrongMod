# Dynamic place name entry template

Dynamic place name: To change the state/VP display name during operation, commonly used **scripted_loc + map UI + flag/variable**, it is not a single effect.
The library's special case "dynamic place names" and the KR-style renaming GUI can be compared as a whole package.

## Common modules

| Module | Function |
|------|------|
| `scripted_localisation` | Return different place name keys according to conditions |
| `on_actions` / National focus/event | Set flag to trigger name change |
| `scripted_gui` (optional) | Player manual name change window |
| Localization | Multiple sets of place names |
| Optional GFX | Buttons and Forms |

## Logical representation

```pdx
#Effect: tag uses historical name
set_country_flag = TAG_use_old_city_names

# scripted_loc (indicative)
defined_text = {
	name = GetStateNameDynamic
	text = {
		trigger = {
			state=219
			has_country_flag = TAG_use_old_city_names
		}
		localization_key = STATE_219_OLD
	}
	text = {
		trigger = { state = 219 }
		localization_key = STATE_219
	}
}
```

The actual project needs to receive the call point where the place name is displayed in the game (if the original/total conversion system already exists, priority will be given to expansion, do not run two sets in parallel).

## Suggested workflow

1. Read the library's "Dynamic Place Names/Purpose of Each Document"
2. Verify a single state when testing the mod
3. Then batch state table driver
4. Pay attention to online and Chinese encoding

## Specification

- Place name verification, it is prohibited to make up historical geography (`modding-rules.md`)
- Use data table + generator for large-scale name change, handwriting is easy to miss
- Differentiate from `cosmetic_tag` country name changes: cosmetic is partial to country name, dynamic place name is partial to state/city
## Related

- `scripted-triggers-template.md` / `scripted-gui-template.md` / `on-actions-template.md` / `localisation-syntax-template.md` / `state-template.md`
