# Bill and National Spirit (Idea) Template

## File location

`common/ideas/<xxx>.txt`

## Bill Template

Bill type: `economy` (economic bill), `trade_laws` (trade bill), `mobilization_laws` (mobilization/military service bill).

```pdx
ideas = {
	economy = {
		law=yes
		use_list_view = yes

		my_economy_law = {
			cost = 150 # Switching cost
			removal_cost = -1 # Replacement cost, usually -1
			available = {
				# Enable conditions
			}
			on_add = {
				# Add instant effect
			}
			on_remove = {
				# Instant effect when removed
			}
			modifier = {
				# Correction effect
			}
			ai_will_do = {
				#AITendencies
			}
			default = yes # Whether it is the default bill
			cancel_if_invalid = no # Whether to cancel when the conditions are not met
		}
	}
}
```

## Create new bill type

If you need to create a new bill type, add the following to `common/ideas/00_idea.txt`:

```pdx
slot = economy # or government / research_production
```

Optional slots: `government` (government page, most commonly used), `research_production` (research and production).

## Hidden national spirit

```pdx
ideas = {
	hidden_ideas = {
		my_hidden_idea = {
			allowed_civil_war = {
				has_government = democratic
			}
			on_add = {
				# Get the effect
			}
			on_remove = {
				# Remove effect
			}
			do_effect = {
				#Real effective conditions
			}
			cancel = {
				# Automatically remove conditions
			}
			modifier = {
				# Country scope correction
			}
			equipment_bonus = {
				armor = {
					build_cost_ic = -0.5
					instant=yes
				}
			}
			research_bonus = {
				construction_tech = 0.1
			}
			rule = {
				can_create_factions = yes
			}
		}
	}
}
```
## National spirit

```pdx
ideas = {
	country = {
		my_country_idea = {
			picture = generic_coastal_defense_ships2

			allowed_civil_war = {
				has_government = democratic
			}
			on_add = {
				add_stability = 0.2
			}
			on_remove = {
				add_stability = -0.2
			}
			do_effect = {
				has_war=no
			}
			cancel = {
				has_war_with = FRA
			}
			modifier = {
				consumer_goods_factor = 0.1
				army_infantry_attack_factor = 0.1
				army_infantry_defence_factor = 0.1
			}
			equipment_bonus = {
				armor = {
					build_cost_ic = -0.5
					instant=yes
				}
			}
			research_bonus = {
				construction_tech = 0.1
			}
			rule = {
				can_create_factions = yes
			}
		}
	}
}
```

##Manufacturer Consultant

```pdx
ideas = {
	naval_manufacturer = {
		my_naval_manufacturer = {
			picture = generic_naval_manufacturer

			allowed = {
				# Check once at the start
			}
			visible = {
				# Visible conditions
			}
			available = {
				# Clickable conditions
			}
modifier = {
				# Country scope correction
			}
			equipment_bonus = {
				# Equipment bonus
			}
			research_bonus = {
				# Scientific research bonus
			}
			traits = {
				# country_leader trait
			}

			ai_will_do = {
				factor = 1
			}
		}
	}

	materiel_manufacturer = {
		# Army Equipment Manufacturer
	}

	tank_manufacturer = {
		#tankmaker
	}

	aircraft_manufacturer = {
		# aircraft manufacturer
	}

	industrial_concern = {
		# industrial enterprise
	}
}
```

## Common field descriptions

| Field | Description |
|------|------|
| `cost` | Switching/recruitment cost |
| `removal_cost` | Removal cost, usually `-1` |
| `available` | Enable/clickable condition |
| `visible` | Visibility conditions |
| `allowed` | Start detection conditions |
| `on_add` | Effect when adding |
| `on_remove` | Effect when removed |
| `do_effect` | Real effective conditions |
| `cancel` | Automatically remove conditions |
| `modifier` | Country scope modifier |
| `equipment_bonus` | Equipment bonus |
| `research_bonus` | Scientific research bonus |
| `rule` | National rules (such as whether a camp can be created) |
| `traits` | Advisor Traits |
| `picture` | Icon name, corresponding to the `name` in the `.gfx` file, remove the `GFX_idea_` prefix; or use `picture = ` placeholder |
## Slot layout



The politics interface slot is defined by `common/idea_tags`, see `idea-tags-template.md`. Content mods generally only add ideas to the original slot and do not change tags.
