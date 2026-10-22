# Scopes template

HOI4 scripts evaluate within a specific **scope**. Effects and conditions are relative to the current scope.

## Common scope types

| Type | Description | Example entry method |
|------|------|----------------|
| Country | Country | `GER = { }`, `ROOT` |
| State | Region | `219 = { }`, `every_owned_state` |
| Character | Character | `random_character`, character within the effect |
| Unit leader | General | General related effects/conditions |
| Operation | Intelligence operations | Intelligence related |
| Faction | Faction | Faction related |
| Combat | Combat | Combat related on_action / effect |

## Dynamic scopes (Dynamic scopes)

| Logo | Meaning |
|------|------|
| `ROOT` | The **starting** scope of the current effect/event/resolution (most common: the country that received the event) |
| `FROM` | The previous scope passed in the calling chain (event initiator, original controller who changed control, etc., **changes according to context**) |
| `FROM.FROM` | One level up (for example, `on_state_control_changed` is often state) |
| `PREV` | Enter the scope before the current block |
| `THIS` | The current scope itself |
| `OWNER` | for state: owner country |
| `CONTROLLER` | for state: controller state |
| `CAPITAL` | For country: capital state |
| `OVERLORD` | Overlord country |
| `event_target:name` | saved event target |
**Don't guess the meaning of FROM**: Write on_action / check the wiki before the diplomatic event or the original hook comment with the same name.

## How to enter the scope

```pdx
# Fixed tag
GER = {
	add_political_power = 50
}

# Fixed state id
219 = {
	add_building_construction = {
		type = industrial_complex
		level=1
		instant_build = yes
	}
}

# Dynamic
ROOT = {
	every_owned_state = {
		limit = {
			is_coastal = yes
		}
		add_extra_state_shared_building_slots = 1
	}
}
```

## every / random / any / all

| prefix | purpose | context |
|------|------|------|
| `every_*` | Perform effects on each matching target | **Effects** |
| `random_*` | Randomly match the target execution effect | **Effect** |
| `any_*` | Whether there is a matching target | **Condition** |
| `all_*` | Whether all matches | **Condition** |
| `count_*` | Count (partial version/context) | **Condition/Variable** |

Common examples:

```pdx
# Effect: each neighboring country
every_neighbor_country = {
	limit = {
		has_war_with = ROOT
	}
	add_opinion_modifier = {
		target=ROOT
		modifier = large_decrease
	}
}

# Condition: Whether there is a country that meets the condition
any_country = {
	original_tag = SOV
	has_government = communism
}
# Randomly select one of your own cores
random_owned_controlled_state = {
	limit = {
		is_core_of = ROOT
		free_building_slots = {
			building = industrial_complex
			size > 0
			include_locked=yes
		}
	}
	add_building_construction = {
		type = industrial_complex
		level=1
		instant_build = yes
	}
}
```

### Common every/random/any targets (excerpt)

- Country: `every_country`, `every_other_country`, `every_enemy_country`, `every_allied_country`, `every_neighbor_country`, `every_subject_country`
- Region: `every_state`, `every_owned_state`, `every_controlled_state`, `every_core_state`, `every_neighbor_state`
- Characters: `every_character`, `every_army_leader`, `every_navy_leader`, `every_scientist`, etc.

The complete list is subject to wiki **Scopes** and the current version of the original document.

## limit

Use `limit = { }` inside `every_*` / `random_*` to filter targets:

```pdx
every_state = {
	limit = {
		is_controlled_by = RSC
		NOT = { is_core_of = RYH }
	}
	add_claim_by = RYH
}
```
Project specifications: Traversal class effects should be wrapped in `hidden_effect` and matched with the top-level `custom_effect_tooltip` (see `modding-rules.md`).

## PREV chain

When entering a nested scope, `PREV` refers to the outer scope:

```pdx
every_country = {
	limit = { has_war_with = ROOT }
	every_owned_state = {
		limit = {
			is_controlled_by = PREV # PREV = The enemy country currently cycled to
		}
		# THIS = this state
	}
}
```

Too deep `PREV.PREV.PREV` is difficult to maintain; give priority to `save_event_target_as` / variables.

## Event targets

```pdx
# save
random_owned_state = {
	limit = { is_capital = yes }
	save_event_target_as = my_capital_state
}

# use
event_target:my_capital_state = {
	add_manpower=1000
}

# Global
save_global_event_target_as = some_global_target
clear_global_event_target = some_global_target
```

It is often used to pass country/state across scopes in event options, delayed events, and news.

## Scope in conditional block

```pdx
trigger = {
	tag=GER
	has_war = yes
	any_owned_state = {
		is_coastal = yes
		arms_factory > 2
	}
	NOT = {
		is_in_faction_with = SOV
	}
	OR = {
		has_government = fascism
		has_government = neutrality
	}
	AND = {
		surrender_progress < 0.1
		num_of_factories > 50
	}
}
```
`AND` / `OR` / `NOT` / `if` / `limit` are logical structures, not national scope.

## Tooltip and hidden

- Scope switching will enter tooltip generation
- Don’t want to refresh the screen: use `hidden_effect = { }` and handwrite `custom_effect_tooltip`
- Debugging available log effects (if version supports it) or temporary `add_political_power` to verify whether the scope is correct

## Specification

- Write clearly in the comments who ROOT/FROM is in the context of this document
- It is forbidden to make up state names; check localization (see `modding-rules.md`)
- Uncertain scope combination: check wiki **Scopes** → Original similar events → Ask the user

## Related documents

- `effects-template.md`
- `triggers-template.md`
- `variables-arrays-template.md`
- `on-actions-template.md`
