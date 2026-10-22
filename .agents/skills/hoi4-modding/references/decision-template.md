> This template corresponds to HOI4 1.16.x version.

#Decision template

## Resolution classification

File location: `common/decisions/categories/<xxx>_decision_category.txt`

```pdx
XXX_decision_category = {
	icon = <icon name>
	picture = <picture name>
	scripted_gui = <scripted_gui_name>

	allowed = {
		# Only detect once at the start of the game
	}
	available = {
		#Continuous detection
	}
	visible = {
		# Continuously detect and display only when satisfied
	}

	priority = {
		base=10
		modifier = {
			add=5
			tag=GER
		}
	}

	visible_when_empty = no

	#Plot highlight
	highlight_states = {
		highlight_state_targets = {
			state = 123
		}
		highlight_provinces = {
			1234 5678
		}
		highlight_states_trigger = {
			is_owned_by = GER
		}
		highlight_color_before_active = 0
		highlight_color_while_active = 1
	}

	# Map pseudo-resolution
	on_map_area = {
		name = my_map_decision_loc
		zoom=300
		state = 123
		target_root_trigger = { }
		target_trigger = { }
		target_array = my_array
	}
}
```
## Ordinary resolutions

File location: `common/decisions/<xxx>.txt`

```pdx
XXX_decision_category = {

	XX_decision = {
		icon = <icon name>

		cost = 50
		days_remove = 30

		custom_cost_trigger = {
			# Display custom_cost_text only when conditions are met
		}
		custom_cost_text = my_custom_cost_loc

		fire_only_once = yes
		days_re_enable = 60

		allowed = { }
		available = { }
		visible = { }

		remove_trigger = {
			# Remove immediately if satisfied
		}
		cancel_trigger = {
			# Cancel task conditions, taking precedence over remove_trigger
		}

		modifier = {
			# Modification of decision duration
		}
		targeted_modifier = {
			tag = SOV
			# Fixes for target countries
		}

		complete_effect = {
			# Click/Start Effect
		}
		remove_effect = {
			# Complete/remove effects
		}
		cancel_effect = {
			# Cancel effect
		}

		war_with_on_remove = SOV
		war_with_on_complete = SOV

		fixed_random_seed = no

		highlight_states = {
			highlight_state_targets = { state = 123 }
			highlight_provinces = { 1234 }
			highlight_states_trigger = { is_owned_by = ROOT }
			highlight_color_before_active = 0
			highlight_color_while_active = 1
		}
ai_will_do = {
			factor = 1
			modifier = {
				add=5
				factor = 2
			}
		}
	}

}
```

## Targeted Resolution

```pdx
XXX_decision_category = {

	targeted_decision = {
		#Method 1: Specify targets directly
		targets = {
			SOV
			FRA
			state = 123
		}
		targets_dynamic=yes

		#Method 2: Use target_array
		target_array = my_array
		targets_dynamic=yes

		#Method 3: Full range scan
		target_trigger = {
			#Limit the target range
		}
		target_root_trigger = {
			# Scan in ROOT home country
		}

		# Regional Targeted Resolutions
		state_target = yes # yes/no/any/any_owned_state/any_controlled_state/continent_key
		on_map_mode = map_and_decisions_view # map_only / decision_view_only / map_and_decisions_view
		target_non_existing = no

		cost = 50
		days_remove = 30
		fire_only_once = yes
		days_re_enable = 60

		allowed = { }
		available = { }
		visible = { }

		modifier = { }
		targeted_modifier = {
			tag = FROM
		}
complete_effect = { }
		remove_effect = { }
		cancel_effect = { }

		war_with_on_complete = FROM
		war_with_on_remove = FROM
		war_with_on_timeout = FROM

		ai_will_do = {
			factor = 1
		}
	}

}
```

### Manually activate targeted resolutions

```pdx
activate_targeted_decision = {
	target = SOV
	decision = my_targeted_decision
}
```

## Task template

```pdx
XXX_decision_category = {

	xx_mission = {
		activation = {
			# Conditions for task occurrence
		}
		available = {
			# Task completion conditions
		}
		allowed = {
			# Only deployment detection
		}

		is_good = yes
		selectable_mission = no

		days_mission_timeout = 60

		war_with_on_timeout = SOV

		timeout_effect = {
			# Unfinished effect after timeout
		}
		complete_effect = {
			# Task completion effect
		}
		cancel_trigger = {
			# Cancel condition
		}
		cancel_effect = {
			# Cancel effect
		}
	}

}
```

## Common field descriptions

### Classification field

| Field | Description |
|------|------|
| `icon` / `picture` | Icons and pictures |
| `scripted_gui` | Scripted GUI |
| `allowed` | Start detection only |
| `available` | Continuous detection |
| `visible` | Continuously detect and display only when satisfied |
| `priority` | Priority |
| `visible_when_empty` | Whether to display categories when there is no visible resolution |
| `highlight_states` | Lot highlighting |
| `on_map_area` | Map pseudo-resolution |
### Resolution field

| Field | Description |
|------|------|
| `cost` | Consume political power |
| `custom_cost_trigger` / `custom_cost_text` | Customized cost display |
| `days_remove` | Number of days the resolution lasts |
| `fire_only_once` | Whether it can only be clicked once |
| `days_re_enable` | Enable intervals again |
| `allowed` | Start detection only |
| `available` | Clickable conditions |
| `visible` | Visibility conditions |
| `remove_trigger` | Automatically remove conditions |
| `cancel_trigger` | Cancellation condition (priority) |
| `modifier` | Continuous modification |
| `targeted_modifier` | Modifier for target country |
| `complete_effect` | Click effect |
| `remove_effect` | Complete/remove effect |
| `cancel_effect` | Cancel effect |
| `war_with_on_complete/remove/timeout` | War warning |
| `fixed_random_seed` | Whether to fix the random seed |
| `highlight_states` | Lot highlighting |
| `state_target` | Regional targeted resolutions |
| `targets` / `target_array` | Target range |
| `target_trigger` / `target_root_trigger` | Target filtering |
| `targets_dynamic` | Expand to derived TAG |
| `target_non_existing` | Whether to allow non-existing countries |
| `on_map_mode` | Map display mode |
### Task field

| Field | Description |
|------|------|
| `activation` | Task triggering conditions |
| `available` | Completion conditions |
| `allowed` | Start detection |
| `is_good` | Progress bar color |
| `selectable_mission` | Whether players need to manually select |
| `days_mission_timeout` | Mission time limit |
| `war_with_on_timeout` | Timeout war warning |
| `timeout_effect` | Timeout effect |
| `complete_effect` | Complete effect |
| `cancel_trigger` / `cancel_effect` | Cancel conditions and effects |

## Scope

- `ROOT`: The country that obtained the resolution
- `FROM`: the country or region targeted by the targeted resolution
