> Contains agents, intelligence agencies, missions, agency upgrades, and custom diplomatic actions.

# Intelligence and custom diplomatic action templates

## Create agent

```pdx
create_operative_leader = {
	name = "Ramón Mercader"
	GFX = GFX_portrait_SOV_ramon_mercader
	traits = { }
	portrait_tag_override = GER
	bypass_recruitment=no
	available_to_spy_master = yes
	nationalities = {TAG}
}
```

## Intelligence agencies

File location: `common/intelligence_agencies/<xxx>.txt`

```pdx
intelligence_agency = {
	picture = GFX_intelligence_agency_logo_usa
	names = { "Office of Strategic Services" }
	default={}
	available = { }
}
```

## Agent Tasks (Operations)

File location: `common/operations/<xxx>_historical_operations.txt`

```pdx
my_operation = {
	icon = GFX_my_operation_icon
	map_icon = GFX_my_operation_map_icon
	name = my_operation_name
	desc = my_operation_desc

	days = 270
	priority=10

	allowed = { }
	available = { }
	visible = { }

	operations = 1
	network_strength = 25
on_start = { }

	outcome_modifiers = { operation_outcome operation_steal_tech_outcome }
	cost_modifiers = { target_sabotage_cost operation_cost }
	risk_modifiers = { operation_risk operation_steal_tech_risk }

	outcome_potential = { }
	risk_chance = 0.25
	experience=5

	outcome_execute = {
		# Success result
	}

	phases = {
		infiltration_border = { base = 60 }
		infiltration_submarine = { base = 20 }
		infiltration_diplomatic = { base = 20 }
	}
	phases = {
		steal_blueprints_bribe = { base = 60 }
	}
	phases = {
		exfiltration_air_pickup = { base = 60 }
	}
}
```

## Agent Traits

File location: `common/unit_leader/<xxx>_traits.txt`

```pdx
operative_my_trait = {
	type = operative
	trait_type = basic_trait
	new_commander_weight = {
		base=1
	}
	cost = 400
	gain_xp_leader = {
		operative_leader_mission = root_out_resistance
	}
}
```
### Agent long-term mission

| Task | Description |
|------|------|
| `build_intel_network` | Build an intelligence network |
| `counter_intelligence` | Counterintelligence |
| `quiet_network` | Quiet Intelligence Network |
| `boost_ideology` | Strengthen ideology |
| `propaganda` | political propaganda |
| `root_out_resistance` | Root out resistance |
| `control_trade` | Control trade |
| `diplomatic_pressure` | Diplomatic pressure |

### Agent small tasks/actions

| Action | Description |
|------|------|
| `operation_capture_cipher` | Steal password |
| `operation_rescue_operative` | Rescue agent |
| `operation_infiltrate_civilian` | Infiltrate civil affairs |
| `operation_infiltrate_armed_forces_army/navy/airforce` | Infiltrate Army, Navy and Air Force |
| `operation_make_resistance_contacts` | Contact resistance groups |
| `operation_boost_resistance` | Strengthen the resistance organization |
| `operation_targeted_sabotage_industry/infrastructure/resources` | Destroy industry/infrastructure/resources |
| `operation_steal_tech_airforce/army/civilian/navy` | Steal blueprints |

## Intelligence agency upgrade

File location: `common/intelligence_agency_upgrades/<xxx>.txt`
```pdx
my_branch = {
	my_upgrade = {
		picture = GFX_upgrade_icon
		frame = upgradeframe_1
		sound = click_default

		ai_will_do = {
			factor = 2
			modifier = {
				factor=20
				is_major = yes
			}
		}

		modifiers_during_progress = { }
		visible = { }
		available = { }

		level = {
			modifier = { }
			complete_effect = { }
		}
		level = {
			modifier = { }
			complete_effect = { }
		}
	}
}
```

## Task phase

File location: `common/operation_phases/<xxx>_operation_phases.txt`

```pdx
phase_test = {
	name = phase_test_name
	desc = phase_test_desc
	icon = GFX_phase_icon
	outcome = phase_test_outcome
	outcome_extra = phase_test_outcome_extra
	map_icon = GFX_phase_map_icon

	requirements = { }
	return_on_complete = no

	equipment = {
		# Equipment cost
	}
}
```

## Task Token

File location: `common/operation_tokens/<xxx>.txt`
```pdx
token_my_token = {
	name = ""
	desc = ""
	icon = ""
	text_icon = ""

	targeted_modifier = targeted_modifier_id

	intel_source = navy
	intel_gain = 1.0
}
```

## Custom diplomatic actions

File location: `common/scripted_diplomatic_actions/<xxx>.txt`

```pdx
scripted_diplomatic_actions = {

	DIP_ACTION_DISARM = {
		allowed = { always = yes }
		visible = { always = yes }
		selectable = { always = yes }

		requires_acceptance = yes
		cost = 10
		command_power=10

		show_acceptance_on_action_button = yes
		icon = 1

		on_sent_effect = { }

		complete_effect = {
			THIS = {
				delete_unit = all
				destroy_ships = all
			}
		}

		reject_effect = {
			ROOT = {
				create_wargoal = {
					type = anytype
					target = PREV.THIS
				}
			}
		}

		send_description = DIP_ACTION_DISARM_SEND_DESC
		receive_description = DIP_ACTION_DISARM_RECEIVE_DESC
		accept_title = DIP_ACTION_DISARM_ACCEPT_TITLE
		accept_description = DIP_ACTION_DISARM_ACCEPT_DESC
		reject_title = DIP_ACTION_DISARM_REJECT_TITLE
		reject_description = DIP_ACTION_DISARM_REJECT_DESC
can_be_sent = { always = yes }
		can_be_accepted = { always = yes }

		ai_acceptance = {
			condition = {
				base=100
			}
		}

		ai_desire = {
			base=-1
			modifier = {
				ROOT = { tag = ENG }
				tag=GER
				add=1000
			}
		}
	}

}
```

## Common field descriptions

### Agent

| Field | Description |
|------|------|
| `bypass_recruitment` | Whether to directly join the available list |
| `available_to_spy_master` | Whether the faction spy master can be recruited |
| `nationalities` | Nationality |

### Task

| Field | Description |
|------|------|
| `operatives` | Number of agents required |
| `network_strength` | Required spy network strength |
| `risk_chance` | Basic risk |
| `outcome_modifiers` | Outcome modifications |
| `cost_modifiers` | Cost modifiers |
| `risk_modifiers` | Risk Modifiers |
| `phases` | Penetration phases |

### Diplomatic Action

| Field | Description |
|------|------|
| `requires_acceptance` | Whether the other party needs to accept |
| `cost` | Political point cost |
| `command_power` | Command point cost |
| `on_sent_effect` | Effect when sending |
| `complete_effect` | Effect on acceptance |
| `reject_effect` | Effect when rejecting |
| `can_be_sent` | Available conditions for the send button |
| `can_be_accepted` | Accept button availability conditions |
| `ai_acceptance` | AI acceptance |
| `ai_desire` | AI initiated tendency |
