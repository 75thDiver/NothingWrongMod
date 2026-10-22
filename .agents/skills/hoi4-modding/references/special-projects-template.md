#Special Projects template

## File location

```
common/special_projects/
├── project_xx_example.txt # Project definition
├── project_tags/ # Project specialization
│ └── my_specialization.txt
└── prototype_rewards/ # General prototype rewards
    └── generic_prototype_rewards.txt

common/scientist_traits/
└── my_scientist_traits.txt # Scientist Traits

common/buildings/
└── my_project_facility.txt # Facility building
```

## Project definition

```pdx
my_custom_project = {
	specialization = "my_specialization_token"

	allowed = {
		has_dlc = "my_dlc_name"
	}
	available = {
		has_tech = "my_tech_name"
	}
	visible = {
		has_building = my_building_name
	}

	breakthrough_cost = {
		specialization_air = 2
		specialization_nuclear = 1
		specialization_land = {
			base=1
			modifier = {
				add=-1
				has_tech = improved_medium_tank_chassis
			}
		}
	}
	narrative = {
		name = "my_project_name_loc_key"
		desc = "my_project_desc_loc_key"
	}

	icon = "GFX_my_project_icon"
	blueprint_image = "GFX_my_project_blueprint"

	prototype_time = 5
	complexity = 15

	resource_cost = {
		resources = {
			steel = 10
			rubber = 5
		}
	}

	empty_reward_weight = {
		base = 1.0
		modifier = {
			factor = 2.0
			has_tech = "my_tech_name"
		}
	}

	ai_will_do = {
		base = 1
		modifier = {
			factor = 1.5
			has_dlc = "my_dlc_name"
		}
	}

	special_project_parent = {
		"my_other_project_token"
		"another_project_token"
	}

	project_output = {
		country_effects = {
			add_stability = 0.05
		}
		facility_state_effects = {
			add_province_modifier = {
				static_modifiers = { flooded }
				province = { id = 6241 }
			}
		}
		scientist_effects = {
			retire = yes
		}
		enable_equipments = {
			limit = { }
			equipment_variant_token
		}
		enable_equipment_modules = {
			limit = { }
			module_token
		}
		enable_subunits = {
			limit = { }
			subunit_token
		}
		sub_unit_bonus = {
			cavalry = {
				soft_attack = 0.05
				hard_attack = 0.05
			}
		}
		equipment_bonus = {
			armor = {
				armor_value = 3
				soft_attack = 3
			}
		}
	}

unique_prototype_rewards = {
		dynamic_token1 = {
			country_effects = {
				add_stability = 0.05
			}
		}
	}

	generic_prototype_rewards = {
		"generic_prototype_reward_token"
	}
}
```

## Project Specialization

File location: `common/special_projects/project_tags/<xxx>.txt`

```pdx
my_specialization_token = {
	blueprint_image = "GFX_my_specialization_blueprint"
	facility_model = "my_specialization_entity"

	sub_specializations = {
		my_specialization_sub1 = {
			blueprint_image = "GFX_my_specialization_sub1_blueprint"
		}
		my_specialization_sub2 = {
			facility_model = "GFX_my_specialization_sub2_entity"
		}
	}
}
```

## Definition of scientist

### Scientist Traits

File location: `common/scientist_traits/<xxx>.txt`

```pdx
my_scientist_trait_token = {
	name = "my_scientist_trait_name_loc_key"
	icon = "GFX_my_scientist_trait_icon"

	specialization = { specialization_land }
available = {
		has_dlc = "No Step Back"
		ROOT = {
			has_tech = tech_engineers
		}
	}

	modifier = {
		special_project_prototype_speed_factor = 0.5
	}
}
```

### Scientist role

```pdx
USA_Einstein = {
	portraits = {
		army = {
			large = GFX_portrait_USA_Einstein
		}
	}
	scientist = {
		traits = { my_scientist_trait_token }
		skills = {
			specialization_nuclear = 3
		}
	}
}
```

## Facility customization

File location: `common/buildings/<xxx>.txt`

```pdx
my_project_facility = {
	icon_frame = 1
	provincial=yes
	disabled_in_dmz = yes
	base_cost = 20000
	value=30
	damage_factor = -1
	allied_build = yes
	show_on_map = 1
	has_destroyed_mesh = yes
	infrastructure_construction_effect = yes

	building_level_cap = {
		state_max = 1
		province_max = 1
	}

	requirements = {
		is_coastal = yes
		has_resources_in_country = {
			resource=steel
			amount > 0
		}
	}
construction_speed_modifier = {
		bonus = 0.2
		has_resources_amount = {
			resource=steel
			amount > 0
			delivered=yes
		}
	}
}
```

## Common field descriptions

| Field | Description |
|------|------|
| `specialization` | The professional field to which the project belongs |
| `allowed` | Check whether the opening is unlocked |
| `available` | Is the item optional |
| `visible` | Whether the item is visible |
| `breakthrough_cost` | Breakthrough point cost |
| `narrative` | Name and description localization |
| `icon` / `blueprint_image` | Icon and blueprint background |
| `prototype_time` | Number of days for each prototype iteration |
| `complexity` | Progress percentage of each prototype iteration |
| `resource_cost` | Resource consumption |
| `empty_reward_weight` | Empty reward weight |
| `ai_will_do` | AI selection tendency |
| `special_project_parent` | Parent project |
| `project_output` | Project completion reward |
| `iteration_output` | Reward for each iteration |
| `unique_prototype_rewards` | Exclusive prototype rewards |
| `generic_prototype_rewards` | Generic prototype rewards |
| `sub_specializations` | Subspecializations |
| `scientist` | The scientist field in the role |
| `skills` | Scientist professional level |
| `building_level_cap` | Facility level upper limit |
