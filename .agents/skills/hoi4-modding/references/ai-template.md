> Before writing AI, please be familiar with the two files `ai_equipment` and `ai_template`.

#AI template

## AI area (ai_area)

File location: `common/ai_areas/<xxx>.txt`

Used to package multiple strategic regions (strategic_regions) into one region name, simplifying the `area` reference in `ai_strategy`.

```pdx
areas = {
	Axis_core_regions = {
		strategic_regions = {
			7# Southern Germany
			6 # Northwestern Germany
			9 # Eastern Germany
			38 # German Prussia and Western Poland
			21 # Alps
			23 # Southern Italy
		}
	}
}
```

### Method to find strategic_regions

1. Enter the game in `-debug` mode, and the state id and strategic region id will be displayed when the mouse is hovering over the plot.
2. Install the plug-in **HOI4 Mod Utilities** (author Yang Chaofan) in VSCode, press `Ctrl+Shift+P` to open the command bar, select **Wire Mod Utilities: Preview World Map** to preview the original plot.

### Used in ai_strategy

```pdx
ENG_USA_invade_axis_core_regions = {
	allowed = {
		OR = {
			original_tag = ENG
			original_tag = USA
		}
	}
	enable = {
		OR = {
			has_war_with = GER
			has_war_with = ITA
		}
	}
	abort_when_not_enabled = yes

	ai_strategy = {
		type = invasion_unit_request
		area = Axis_core_regions
		value=25
	}
ai_strategy = {
		type = front_control
		area = Axis_core_regions
		ratio=0.5
		ordertype=front
		execution_type = balanced
		execute_order = yes
	}

	ai_strategy = {
		type = front_unit_request
		area = Axis_core_regions
		value=50
	}

	ai_strategy = {
		type = force_concentration_front_factor
		ratio=0.5
		area = Axis_core_regions
		value=50
	}
}
```

## AI strategy (ai_strategy)

File location: `common/ai_strategy/<xxx>.txt`

### Infrastructure

```pdx
my_ai_strategy = {
	enable = {
		# Open conditions
	}
	abort = {
		# Termination condition
	}
	abort_when_not_enabled = yes

	ai_strategy = {
		type = <strategy type>
		id = <object>
		value = <numeric value>
		target = <diplomatic action target>
	}
}
```

```pdx
# Add dynamically to national focuses/events/resolutions
TAG = {
	add_ai_strategy = {
		type = <strategy type>
		id = <object>
		value = <numeric value>
	}
}
```

### Diplomacy

| Type | Description |
|------|------|
| `alliance` | Tendency to ally with the target country |
| `antagonize` | Make the target more hostile |
| `asking_foreign_garrison` | Requesting foreign garrison |
| `befriend` | Be friendlier to the target |
| `conquer` | Conquer target |
| `consider_weak` | Consider the target weak |
| `contain` | Containment target |
| `declare_war` | Declare war when there is a war target |
| `diplo_action_acceptance` | To accept a diplomatic action, requires `target` |
| `diplo_action_desire` | If you want the target to perform diplomatic action, you need `target` |
| `dont_join_wars_with` | Do not join wars with the target, define the target with `target_country` |
| `ignore` | Ignore the target diplomatic action |
| `ignore_claim` | Ignore the claim on the target |
| `protect` | Protection target |
| `support` | Support target (Lease, Volunteer Army, etc.) |
| `send_lend_lease_desire` | Send lease preference |
| `send_volunteers_desire` | Send volunteer tendencies |
### Army Management

| Type | Description |
|------|------|
| `invade` | Launch a naval invasion of a target |
| `naval_invasion_focus` | Prefers maritime invasion, not targeting specific countries |
| `prepare_for_war` | Plan attack targets in advance |
| `area_priority` | Deploy more units in the specified AI area |
| `dont_defend_ally_borders` | Do not deploy on the target's border with the enemy |
| `force_defend_ally_borders` | Deploy at the target's border with the enemy |
| `front_armor_score` | Put more tanks on target |
| `front_control` | Modify the specified front line command |
| `front_unit_request` | Deploy more units on the specified front line |
| `invasion_unit_request` | Dedicate more units to the specified sea invasion |
| `garrison` | Controls the number of troops defending victory points and ports |
| `garrison_reinforcement_priority` | Prioritize reinforcement of garrison |
| `ignore_army_incompetence` | Ignore inexperience penalty |
| `put_unit_buffers` | Reserve a certain proportion of garrison divisions in designated areas |
| `spare_unit_factor` | Spread more units to defend allies |
| `theatre_distribution_demand_increase` | Distribute more troops to the target country's theater |

### front_control detailed parameters

```pdx
ai_strategy = {
	type = front_control
	state = 123
	tag=GER
	strategic_region=7
	area = Axis_core_regions
	country_trigger = { }
	state_trigger = { industrial_complex > 1 is_owned_by = ENG }
	ratio=0.1
	priority=1
	ordertype = front # front / invasion
	execution_type = rush # careful / balanced / rush / rush_weak
	execute_order = yes # yes forces an attack, no does not attack
	manual_attack = no # false Prevent small-scale engagements that are not planned by the front line
}
```
### Naval Management Class

| Type | Description |
|------|------|
| `naval_avoid_region` | Avoid designated strategic areas |
| `naval_convoy_raid_region` | Raid convoys in a designated area |
| `naval_mission_threshold` | Raise the threshold for naval mission execution |
| `strike_force_home_base` | Perform strike fleet missions in the designated area |

### Intelligence

| Type | Description |
|------|------|
| `agency_ai_base_num_factories_factor` | Intelligence agency upgrade baseline |
| `agency_ai_per_upgrade_factories_factor` | Factories required for each upgrade |
| `intelligence_agency_branch_desire_factor` | Branch upgrade desire |
| `intelligence_agency_usable_factories` | Intelligence agency usable factories |
| `operation_equipment_priority` | Prioritize the use of equipment for intelligence tasks |
| `operative_mission` | Perform the specified mission over the target |
| `operative_operation` | Perform the specified action on the target |

### Production and construction category

| Type | Description |
|------|------|
| `added_military_to_civilian_factory_ratio` | Military industry/civilian labor ratio |
| `air_factory_balance` | Air force factory ratio |
| `dockyard_to_military_factory_ratio` | Dockyard/military industry ratio |
| `railway_gun_divisions_ratio` | Train gun/division ratio |
| `build_building` | Build the specified building in the specified province |
| `building_target` | Increase the target value of the specified building |
| `factory_build_score_factor` | Increase the tendency to build factories in the specified state |
| `equipment_production_factor` | Produce specified equipment |
| `equipment_production_min_factories` | Specify the minimum number of equipment factories |
| `equipment_variant_production_factor` | Produce the specified equipment prototype |
| `equipment_stockpile_surplus_ratio` | Reserve ratio |
| `build_army` | Build the specified role army |
| `force_build_armies` | Force build armies |
| `production_upgrade_desire_offset` | Upgrade the production line to the specified equipment |
| `role_ratio` | Specify the number of role templates |
| `unit_ratio` | Specify the number of unit templates |
| `min_wanted_supply_trains` | Minimum number of supply trains |
| `min_wanted_supply_trucks` | Minimum number of supply trucks |
### Others

| Type | Description |
|------|------|
| `scorched_earth_prio` | Specify state scorched earth tactics |
| `land_xp_spend_priority` | Army experience spending priority |
| `pp_spend_amount` | Reserve political power for specified purposes |
| `pp_spend_priority` | Political point usage priority |
| `equipment_design_priority` | Equipment design priority |
| `occupation_policy` | Occupation policy for the specified country (0-3) |
| `research_tech` | Research designated technology |
| `save_equipment` | Save the specified equipment |
| `template_prio` | Template training tendency |
| `template_xp_reserve` | Template modification retention experience |

## Common examples

```pdx
ai_strategy = {
	type=alliance
	id = "USA"
	value=100
}

ai_strategy = {
	type = send_volunteers_desire
	id = "SOV"
	value=80
}

ai_strategy = {
	type = prepare_for_war
	id = "GER"
	value=100
}

ai_strategy = {
	type = force_build_armies
	value=100
}

ai_strategy = {
	type = equipment_stockpile_surplus_ratio
	value=50
}
```


## AI strategic plan (ai_strategy_plans)

File: `common/ai_strategy_plans/<TAG>_*.txt`
Prioritize national focuses according to historical/non-historical routes, often used in conjunction with `game_rules`.
```pdx
TAG_historical_plan = {
	name = "TAG Historical Plan"
	desc = ""

	allowed = {
		original_tag = TAG
	}
	enable = {
		OR = {
			has_country_flag = TAG_AI_RANDOM_HISTORICAL
			has_game_rule = {
				rule = TAG_AI_BEHAVIOR
				option=HISTORICAL
			}
		}
	}
	abort = {
		is_subject = yes
	}

	ai_national_focuses = {
		TAG_focus_early
		TAG_focus_mid
		TAG_focus_late
	}

	# Optional: research, ideas, trait weights, etc., refer to the original complete plan file
}
```

- `ai_national_focuses`: National focus id of priority point from top to bottom
- Separate plan files for each route (historical / alternate / fascism…)
- See `game-rules-template.md`

## AI preparation templates (ai_templates)

File: `common/ai_templates/<xxx>.txt`
Tell the AI what division you want to make (armor/infantry role).

```pdx
armor_generic = {
	blocked_for = { GER JAP } # Countries that do not use this general template
	role = armor
	upgrade_prio = {
		base=2
	}
	light_armor_early = {
		upgrade_prio = { base = 1 }
		target_template = {
			# Target compilation structure, compare with the vanilla
		}
	}
}
```
## AI equipment design (ai_equipment)

File: `common/ai_equipment/`
How tank/aircraft/ship designer AI stacks modules and upgrades priorities; separate files by country (such as `ENG_tank.txt`).
Before writing, copy the file structure of the vanilla of the same country, and do not create an empty role name.

## AI research trends (ai_focuses)

File: `common/ai_focuses/`
`ai_focus_defense` and other blocks give weight to technology categories; the sustainable national focus `supports_ai_strategy` can be linked.

```pdx
ai_focus_defense = {
	research = {
		defensive=5.0
		radar_tech = 1.0
		construction_tech = 2.0
	}
}
```

## Related documents

- `game-rules-template.md` / `continuous-focus-template.md` / `focus-template.md` / `unit-template.md`
