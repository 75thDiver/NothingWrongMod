# Ace Pilot and Troop Medal Template

## Air Force Ace Correction

File: `common/aces/00_aces.txt`

```pdx
modifiers = {
	fighter_good = {
		type = { fighter heavy_fighter interceptor }
		chance = 0.9
		effect = {
			air_attack_factor = 0.03
			air_maximum_speed_factor = 0.03
			air_agility_factor = 0.05
		}
	}
}
```

- `type`: the types of aircraft equipment that can appear
- `chance`: weight
- `effect`: Ace’s additional air force modifier
- Tag names are globally unique; please use new tags when adding mods to avoid silent overwriting.

See `names-template.md` for the name pool.

## Unit Medals unit_medals

File: `common/unit_medals/`

```pdx
unit_medals = {
	TAG_cross = {
		available = {
			original_tag = TAG
		}
		frame=1
		icon = "GFX_medal_icon_tag"
		cost = 30
		unit_modifiers = {
			army_org_factor = 0.05
		}
		# ship_modifiers = { } ship medals
		# one_time_effect = { } when awarding a medal (the opponent ship may not run away, see the original comments)
	}
}
```

`common/medals/` also has definitions related to the medal system, please open the comparison before changing.

## Related

- `names-template.md` / `modifiers-index-template.md` / `unit-template.md`
