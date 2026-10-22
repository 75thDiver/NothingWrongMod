# Sub-Doctrine template

## File location

`common/doctrines/subdoctrines/land/<xxx>.txt`

## Infrastructure

```pdx
SUM_army_doctrine = {
	track = infantry
	name = SUM_army_doctrine
	description = SUM_army_doctrine_desc
	icon = GFX_SUM_army_doctrine_medium

	xp_cost = 75
	xp_type = army

	available = {
		has_dlc = "No Compromise, No Surrender"
		is_SUM = yes
	}
	visible = {
		is_SUM = yes
	}

	ai_will_do = {
		base = 1
		modifier = {
			factor = 95
			is_SUM = yes
		}
	}

# The effect given immediately after unlocking the sub-doctrine
	SUM_Forest_Watcher = {
		soft_attack = 0.30
		hard_attack = 0.30
		defense = 0.30
		breakthrough = 0.10
	}

	category_SUM_Eremites = {
		soft_attack = 0.25
		hard_attack = 0.25
		defense = 0.15
		breakthrough = 0.10
		default_morale = 0.20
	}

# Mastery rewards
	rewards = {
		strength_Forest_Desert_ranger = {
			Mastery = 50
			SUM_Forest_Watcher = {
				defense = 0.10
				soft_attack = 0.10
				supply_consumption = -0.05
				ap_attack = 0.10
			}
			category_SUM_Eremites = {
				max_organisation = 5
				soft_attack = 0.10
				hard_attack = 0.10
			}
			experience_gain_army_unit_factor = 0.05
		}

		Training_Special_Forest_Desert_Watcher = {
			mastery = 50
			category_SUM_Eremites = {
				default_morale = 0.20
				equipment_capture_factor = 0.10
				supply_consumption = -0.05
			}
			SUM_Forest_Watcher = {
				equipment_capture_factor = 0.05
				hard_attack = 0.10
				soft_attack = 0.10
			}
			attrition = -0.10
		}
	}
}
```

## Common field descriptions

| Field | Description |
|------|------|
| `track` | Doctrine type, such as `infantry` |
| `name` | Doctrine name localization key |
| `description` | Describes the localization key |
| `icon` | Icon name, needs to be registered in `gfx` and `interface` |
| `xp_cost` | The experience cost to unlock |
| `xp_type` | Experience type, `army` / `navy` / `air` |
| `available` | Unlock conditions |
| `visible` | Visibility conditions |
| `ai_will_do` | AI selection tendency |
| `rewards` | Mastery Rewards Group |
| `mastery` | Mastery required for this level of mastery |

## Icon registration

Register the subdoctrine icon in `interface/<xxx>.gfx`:

```pdx
spriteType = {
	name = "GFX_SUM_army_doctrine_medium"
	texturefile = "gfx/interface/doctrines/SUM_army_doctrine.dds"
}
```



## Overview of Doctrine



Grand Doctrine / Track / Mastery See `doctrine-system-template.md` and the main body `common/doctrines/_documentation.md`.

