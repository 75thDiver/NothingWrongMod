#Country Tag Aliases

File: `common/country_tag_aliases/tag_aliases.txt`
Use a **dynamic 3-letter alias** to refer to "a country that meets the conditions" in the script instead of hard-coding GER.

## Mapping method

```pdx
# Directly map variables/event target
X01 = {
	event_target = my_saved_enemy
}

# Search among candidates
FOE = {
	original_tag = GER
	# targets = { GER ITA }
	# target_array = my_enemies
	country_score = {
		base=1
		modifier = {
			add=10
			is_in_faction_with = PREV
		}
	}
	fallback = GER
	# Additional trigger: or/and, etc., only accepted if the goal is met
}
```

Notes from the vanilla:

- Aliases must be 3 letters long and do not conflict with existing tags
- `PREV` = script scope using this alias
- Available `variable` / `event_target` / `global_event_target` **direct** binding
- Otherwise, search in `original_tag` / `targets` / `target_array`, and use `country_score` to select the highest score
- `fallback`: fallback when there is no match
- **DO NOT** Unlimited scanning of countries all over the world (Performance)

## Use

Write an alias token anywhere a country is accepted (effect target, trigger comparison, etc.) and the engine resolves it to the real country.

## Specification

- Aliases should be in all uppercase letters and prefixed within the project to avoid conflicts (note only 3 characters)
- Documented "parsing rules", otherwise national focuses will be difficult to read
- Division of work with `event_target`: target is used for short-term delivery, and alias is used for stable strategy reference
## Related

- `scopes-template.md` / `variables-arrays-template.md` / `scripted-effects-template.md`
