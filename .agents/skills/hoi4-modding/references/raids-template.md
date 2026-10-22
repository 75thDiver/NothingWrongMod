# Raid / Raids Template

File: `common/raids/` (like `air_raids.txt`) + `categories/`
DLC contains a lot of content (such as Götterdämmerung), so check the same entries in the main body before writing.

## Structure diagram

```pdx
types = {
	TAG_facility_strike = {
		days_to_prepare = 90
		category = air_raids
		command_power = 25

allowed = {
			has_dlc = "Gotterdammerung"
		}
		visible = { }
		show_target = {
			# Target is visible
		}
		available = {
			# Executable
		}

		ai_will_do = {
			base = 1
		}

# Fields such as target type, consumption, success/failure effects, etc. are subject to the original complete entries.
	}
}
```

## Key Points

- `category` corresponds to `raids/categories`
- Consume Command power and preparation days
- Targets may be facilities, states, fleets, etc. (by type)
- AI must limit potential enemies to avoid global explosions

## Related

- `effects-template.md` / `triggers-template.md` / `special-projects-template.md`
