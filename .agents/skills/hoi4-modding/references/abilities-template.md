# General Abilities Template

File：`common/abilities/<xxx>.txt`
Active abilities that consume Command power on the battlefield (powerful attack, forced attack, etc.)）。

```pdx
ability = {
	TAG_force_attack = {
		name = ABILITY_TAG_FORCE_ATTACK
		desc = ABILITY_TAG_FORCE_ATTACK_DESC
		icon = GFX_ability_chi_force_attack
		sound_effect = command_power_ability_offensive

		type = army_leader   # General type

		allowed = {
			is_leading_army_group = no
			OWNER = {
				has_completed_focus = TAG_unlock_ability
			}
		}

		cost = 0.11
		duration = 168

		unit_modifiers = {
			offence = 0.25
			breakthrough_factor = 0.25
		}

		ai_will_do = {
			factor = 1
		}
	}
}
```

## Main points

| Field | illustrate |
|------|------|
| `type` | Ability Attribution (Army General, etc.） |
| `cost` / `duration` | Command power consumption and duration (hours, etc., please refer to the Vanilla)） |
| `unit_modifiers` | Effect troops modifier |
| `allowed` | General/OWNER country conditions |

localization `name`/`desc` Key; Icon Go GFX.

## Related

- `custom-traits-template.md` / `character-template.md` / `modifiers-index-template.md`
