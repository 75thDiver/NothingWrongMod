> This article is formatted, please consider the project needs when writing it.

# Unit (Sub Unit) template

## File location

`common/units/<xxx>.txt`

## Infrastructure

```pdx
sub_units = {

	my_unit = {
		sprite = infantry
		map_icon_category = infantry

		active = yes # no requires technology activation
		cavalry=no
		special_forces=no
		marines=no
		mountaineers = no
		can_be_parachuted = no
		affects_speed = no # mostly used for support companies

		transport = motorized_equipment # Commonly used only by motorized/mechanized infantry

		priority=3000
		ai_priority = 3000

		type = {
			infantry
		}

		group = infantry # infantry / mobile / armor / support

		categories = {
			category_army
			category_front_line
			category_all_infantry
		}

		combat_width = 2

		max_strength = 25
		max_organisation = 70
		default_morale = 0.3
		manpower = 300

		training_time = 120
		suppression = 5.0
		weight=0.5
		supply_consumption = 0.20

		need = {
			infantry_equipment = 100
			artillery_equipment = 12
		}
# Support common attribute bonuses
		defense = -0.4
		breakthrough = -0.4
		soft_attack = -0.4
		hard_attack = -0.4
		air_attack = -0.2

		# Terrain bonus
		mountain = {
			attack = 0.05
			defense = 0.05
			movement = 0.05
		}
		hills = {
			defense = 0.1
		}
		river = {
			attack = 0.2
			movement = 0.5
		}
		amphibious = {
			attack = 0.4
			movement = 0.5
		}
		forest = {
			movement = -0.2
		}
		urban = {
			attack = 0.25
		}
		fort = {
			attack = 0.2
		}
		marsh = {
			movement = 0.2
		}
		jungle = {
			movement = -0.2
		}
	}

}
```

## Common field descriptions

| Field | Description |
|------|------|
| `sprite` | Unit sprite |
| `map_icon_category` | Map icon category |
| `active` | Whether the start is activated |
| `cavalry` | Whether to be cavalry |
| `special_forces` | Whether special forces |
| `marines` | Whether to be a Marine Corps |
| `mountaineers` | Is it a mountain division |
| `can_be_parachuted` | Can it be airdropped |
| `affects_speed` | Whether to affect division speed |
| `transport` | Transport equipment |
| `priority` / `ai_priority` | Soldier card/AI weight |
| `type` | Unit type, multiple selections possible |
| `group` | UI groups: `infantry` / `mobile` / `armor` / `support` |
| `categories` | Label classification, decide which bonuses to eat |
| `combat_width` | Battlefield width |
| `max_strength` | HP |
| `max_organisation` | Degree of organization |
| `default_morale` | Organizational recovery |
| `manpower` | Manpower |
| `training_time` | Training time |
| `suppression` | Suppression value |
| `weight` | Weight, `1` requires a transport ship |
| `supply_consumption` | Supply consumption |
| `need` | Required equipment and quantity |
## Common types

| type | description |
|------|------|
| `infantry` | infantry |
| `motorized` | Motorized |
| `mechanized` | Mechanized |
| `armor` | armor |
| `support` | support company |
| `flame` | Breathing fire |
| `anti_air` | Anti-aircraft |

## Common categories

| category | description |
|------|------|
| `category_army` | Army |
| `category_front_line` | Frontline troops |
| `category_all_infantry` | All infantry and motorized/mechanized infantry |
| `category_light_infantry` | Dismounted infantry |
| `category_support_battalions` | Support Battalions |
| `category_recon` | Reconnaissance |
| `category_line_artillery` | Towed artillery |
| `category_artillery` | Towed artillery and light artillery |
| `category_all_armor` | Tanks and armored vehicles |
| `category_tanks` | tanks |
| `category_special_forces` | Special Forces |
| `category_fighter` | fighter |
| `category_heavy_fighter` | Heavy fighter |
| `category_cas` | Close support machine |
| `category_nav_bomber` | Naval bomber |
| `category_tac_bomber` | Tactical bomber |
| `category_strat_bomber` | Strategic bomber |
## Icon registration

```pdx
spriteType = {
	name = "GFX_unit_my_unit_icon_medium"
	texturefile = "gfx/interface/counters/divisions_large/xxx.png"
	noOfFrames = 2
}

spriteType = {
	name = "GFX_unit_my_unit_icon_medium_white"
	texturefile = "gfx/interface/counters/divisions_large/xxx_white.png"
	noOfFrames = 2
}

spriteType = {
	name = "GFX_unit_my_unit_icon_small"
	texturefile = "gfx/interface/counters/divisions_small/xxx.png"
	legacy_lazy_load = no
	noOfFrames = 2
}
```

Custom categories can be created in `common/unit_tags/<xxx>.txt`.
