# Custom manufacturer (MIO) template

MIO files are located under `common/military_industrial_organization/`.

## File structure

```
common/military_industrial_organization/
├── policies/ #Manufacturer policy
│ └── xxx_policy.txt
├── organizations/ # country specific manufacturer
│ └── xxx_organization.txt
└── equipment_groups/ # Equipment types (available in Vanilla, can also be customized)
    └── mio_equipment_groups.txt
```

##Manufacturer Policy

File location: `common/military_industrial_organization/policies/<xxx>.txt`

```pdx
mio_policy_air_perfect_finish = {
	icon = GFX_mio_policy_perfect_finish

	allowed = {
		# MIO scope, only deployment detection
	}
	visible = {
		# Visible conditions
	}
	available = {
		# Conditions of use
	}

	equipment_bonus = {
		same_as_mio = {
			maximum_speed = 0.05
			build_cost_ic = 0.05
		}
	}

	production_bonus = {
		# Bonus to the production line
	}

	organization_modifier = {
		# Fixes to MIO itself
	}

	on_add = {
		# Effect when the policy is implemented
	}
	on_remove = {
		# Effect when the policy ends
	}
ai_will_do = {
		#AITendencies
	}

	cost = 25 # Policy cost (political power), default 25
	cooldown = 180 # Cooldown time (days), default 180
}
```

## Manufacturer Organization

File location: `common/military_industrial_organization/organizations/<xxx>.txt`

```pdx
AST_cockatoo_doe_organization = {
	name = AST_cockatoo_doe_organization
	include = generic_raider_ship_organization
	icon = GFX_idea_Cockatoo_doe

	allowed = {
		# Conditions that are allowed to appear
	}
	visible = {
		# Visible conditions
	}
	available = {
		# Available conditions
	}

	on_design_team_assigned_to_tech = {
		# Effect when added to scientific research
	}
	on_design_team_assigned_to_variant = {
		# Effect when attached to designer
	}
	on_industrial_manufacturer_assigned = {
		# Effect when associated with production line
	}
	on_industrial_manufacturer_unassigned = {
		# Effect when canceling the association of the production line
	}
	on_tech_research_completed = {
		# Effect when correlation research is completed
	}
	on_tech_research_cancelled = {
		# Effect when associated research is canceled
	}

	equipment_type = {
		# Equipment bonus types, see mio_equipment_groups
	}
	research_categories = {
		# Research bonus types
	}
tree_header_text = {
		text = xxxx # localization key
		x = 3
	}

	initial_trait = {
		name = generic_mio_initial_trait_standardized_production
		equipment_bonus = {
			armor_value = -0.05
			defense = -0.05
			build_cost_ic = -0.03
		}
	}

	trait = {
		token = generic_mio_trait_crew_ergonomics
		name = generic_mio_trait_crew_ergonomics
		icon = GFX_generic_mio_trait_icon_maximum_speed

		available = {
			has_mio_size > 3
		}

		position = { x = 4 y = 0 }
		relative_position_id = generic_mio_trait_simplified_suspension

		any_parent = {
			# Prerequisite traits (partially satisfied, dotted line)
		}
		all_parents = {
			# Prerequisite characteristics (all satisfied, solid line)
		}
		mutually_exclusive = {
			# Mutually exclusive traits
		}
		parent = {
			traits = {
				#Associate prerequisite traits
			}
			num_parents_needed = 1
		}

		special_trait_background = no

		equipment_bonus = {
			maximum_speed = 0.02
			defense = 0.02
		}
		production_bonus = {
			# Production line bonus
		}
		organization_modifier = {
			# MIO self-correction
		}
		limit_to_equipment_type = {
			# Limit equipment types
		}
		on_complete = {
			# Trigger effect after selection
		}
	}
}
```
## Trait position rules

When writing the `position` of `trait` / `add_trait`, you must first distinguish between **absolute coordinates** and **relative coordinates**.

### Absolute coordinates

Without `relative_position_id`, `position = { x = N y = M }` is the absolute position in the trait tree.

### Relative coordinates

As long as the trait uses `relative_position_id = XXX`, the `position` here is the offset relative to XXX:

```text
Final x = XXX of x + position.x
Ultimately y = XXX of y + position.y
```

In common writing methods, the preceding traits pointed to by `any_parent` / `all_parents` are often written as `relative_position_id` at the same time. At this time, `position` must be written in terms of relative offsets and can no longer be understood in terms of absolute coordinates.

### Error example

The parent trait is at `x = 9 y = 0`, and the child trait wants to be placed directly below it at `x = 9 y = 1`:

```pdx
# Error: this would place the child trait at x = 18, y = 1
add_trait = {
	token = child_trait
	relative_position_id = parent_trait
	any_parent = { parent_trait }
	position = { x = 9 y = 1 }
}
```

Because `9 + 9 = 18`.

### Correct example

```pdx
# Correct: 0 to the right and 1 below the parent trait, and ultimately x = 9, y = 1
add_trait = {
	token = child_trait
	relative_position_id = parent_trait
	any_parent = { parent_trait }
	position = { x = 0 y = 1 }
}
```
### Writing List

1. Root trait: Writable absolute `position`.
2. There is a sub-trait of `relative_position_id`: `position` only writes relative offsets.
3. When you want to paste it directly below the parent trait, you usually write `position = { x = 0 y = 1 }`.
4. When you want to paste it to the right of the parent trait, you usually write `position = { x = 1 y = 0 }`.
5. Do not copy the absolute x/y of the parent trait into the `position` of the child trait.

## Equipment type

File location: `common/equipment_groups/mio_equipment_groups.txt`

```pdx
mio_cat_eq_only_light_fighter = {
	equipment_type = {
		small_plane_airframe_0
		small_plane_airframe_1
		small_plane_airframe_2
		small_plane_airframe_3
		small_plane_airframe_4
		cv_small_plane_airframe_0
		cv_small_plane_airframe_1
		cv_small_plane_airframe_2
		cv_small_plane_airframe_3
		cv_small_plane_airframe_4
		fighter_equipment_0
		fighter_equipment_1
		fighter_equipment_2
		fighter_equipment_3
		cv_fighter_equipment_0
		cv_fighter_equipment_1
		cv_fighter_equipment_2
		cv_fighter_equipment_3
		jet_fighter_equipment
		rocket_interceptor_equipment
	}
}
```
If a custom equipment type does not have a localized name, it will be displayed as a list of included equipment in the game. Icon format: `GFX_<custom equipment type code>`.

## Commonly used equipment bonus attributes

### Army General

| Properties | Description |
|------|------|
| `maximum_speed` | Maximum speed |
| `reliability` | reliability |
| `defense` | defense |
| `breakthrough` | breakthrough |
| `soft_attack` | Soft attack |
| `hard_attack` | Hard attack |
| `ap_attack` | Armor-piercing |
| `air_attack` | Anti-air attack |
| `build_cost_ic` | Production cost |
| `fuel_consumption` | Fuel consumption |
| `hardness` | Armor rate |
| `armor_value` | Armor thickness |

### Navy

| Properties | Description |
|------|------|
| `lg_attack` / `lg_armor_piercing` | Light artillery attack / Armor piercing |
| `hg_attack` / `hg_armor_piercing` | Heavy artillery attack / armor piercing |
| `torpedo_attack` | Torpedo attack |
| `sub_attack` | Anti-submarine / secondary battery attack |
| `anti_air_attack` | Anti-air attack |
| `naval_speed` | Naval speed |
| `naval_range` | voyage |
| `max_strength` | Maximum strength |
| `surface_detection` / `sub_detection` | Surface / Underwater detection |
| `surface_visibility` / `sub_visibility` | Surface / Underwater visibility |
| `mines_sweeping` / `mines_planting` | Minesweeping / Minelaying |
| `carrier_size` | Aircraft carrier size (officially not recommended) |
### Air Force

| Properties | Description |
|------|------|
| `air_superiority` | Air superiority |
| `air_attack` / `air_defence` | Air attack / defense |
| `air_agility` | Maneuvering |
| `maximum_speed` | Maximum speed |
| `air_range` | range |
| `naval_strike_attack` / `naval_strike_targetting` | Naval attack / targeting |
| `air_ground_attack` | Ground attack |
| `air_bombing` | strategic bombing |
| `night_penalty` | Night punishment |

### Production line bonus

| Properties | Description |
|------|------|
| `production_cost_factor` | Production cost |
| `production_capacity_factor` | Production volume |
| `production_efficiency_cap_factor` | Production efficiency upper limit |
| `production_efficiency_gain_factor` | Production efficiency growth |
| `production_resource_need_factor` | Production resource requirements |
| `production_resource_penalty_factor` | Resource missing penalty modifier |
| `production_conversion_speed_factor` | Conversion production line speed correction |

### MIO organization fixes

| Properties | Description |
|------|------|
| `military_industrial_organization_research_bonus` | Military-industrial organization research speed |
| `military_industrial_organization_design_team_assign_cost` | Design team assignment cost |
| `military_industrial_organization_design_team_change_cost` | Design team change cost |
| `military_industrial_organization_industrial_manufacturer_assign_cost` | Industrial manufacturer assignment cost |
| `military_industrial_organization_task_capacity` | Military-industrial organization task capability |
| `military_industrial_organization_size_up_requirement` | Upgrade funding requirements |
| `military_industrial_organization_funds_gain` | Military-industrial organization fund gains |
## Special project equipment code

Naval special items can be augmented by vanilla MIO:

| Special Projects | Code |
|----------|------|
| Cruiser submarine | `ship_hull_cruiser_submarine` / `cruiser_submarine` |
| Fleet submarine | `ship_hull_fleet_submarine` / `fleet_submarine` |
| Nuclear submarine | `ship_hull_nuclear_submarine` / `nuclear_submarine` |
| Mini submarine | `ship_hull_midget_submarine` / `midget_submarine` |
| Heavy torpedo cruiser | `ship_hull_torpedo_cruiser` / `torpedo_cruiser` |
| Super heavy battleship | `ship_hull_super_heavy_1` / `SH_battleship_1` |
| Modern battleship | `ship_hull_heavy_modern` / `modern_battleship` |
| Ice carrier | `ship_hull_mega_carrier` / `mega_carrier` |
| Modern aircraft carrier | `ship_hull_carrier_modern` / `modern_carrier` |

Army Special Projects:

| Special Projects | Code |
|----------|------|
| Land Cruise | `land_cruiser_chassis` / `land_cruiser_equipment` |
| Armored Support Vehicle | `armored_support_vehicle` |
| Super heavy train gun | `super_heavy_railway_gun_equipment` |
| Super heavy howitzer | `super_heavy_artillery_equipment` |
| Super heavy self-propelled howitzer | `self_propelled_super_heavy_artillery_equipment` |
Air Force Special Projects:

| Special Projects | Code |
|----------|------|
| Space mothership | `mothership_equipment_0` |
| Intercontinental bomber | `strat_bomber_intercontinental_equipment_1` |
| Supersonic jet | `small_plane_airframe_5` / `supersonic_fighter_equipment_1` |
| Helicopter | `helicopter_equipment` |
| Guided Missile | `guided_missile_equipment` |
| Ballistic Missile | `ballistic_missile_equipment` |
| Nuclear missile | `nuclear_missile_equipment` |
| Surface-to-air missile | `sam_missile_equipment` |
