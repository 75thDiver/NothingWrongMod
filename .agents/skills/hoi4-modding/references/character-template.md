> Character files integrate leaders, advisors, generals, scientists and other roles.

#Characters template

## File location

`common/characters/<XXX>.txt`

## Infrastructure

```pdx
characters = {

	TAG_my_character = {
		name = TAG_my_character

		portraits = {
			army = {
				large = "gfx/leaders/TAG/TAG_my_character.png"
				small = "gfx/interface/ideas/TAG_my_character.png"
			}
			civilian = {
				large = "gfx/leaders/TAG/TAG_my_character.png"
				small = "gfx/interface/ideas/TAG_my_character.png"
			}
		}

		gender=male
		can_be_captured = yes

		country_leader = {
			ideology=nazism
			traits = { }
			expire = "1965.1.1.1"
			desc = TAG_my_character_desc
		}

		advisor = {
			slot = political_advisor
			idea_token = TAG_my_character_advisor
			ledger = army
			cost = 150
			traits = { }
			can_be_fired = yes
			removal_cost = -1
			on_add = { }
			on_remove = { }
			ai_will_do = {
				factor = 1
			}
		}
corps_commander = {
			legacy_id = -1
			traits = { }
			skill=3
			attack_skill=3
			defense_skill=2
			planning_skill = 2
			logistics_skill=2
			visible = {
				# Condition
			}
		}

		scientist = {
			traits = { }
			skills = {
				specialization_land = 1
				specialization_air = 1
				specialization_naval = 1
				specialization_nuclear = 1
			}
			desc = TAG_my_character_scientist_desc
			visible = {
				# Condition
			}
		}
	}

}
```

## Common field descriptions

| Field | Description |
|------|------|
| `name` | Character name localization key |
| `portraits` | Avatar configuration |
| `gender` | Gender: `undefined` / `male` / `female` |
| `can_be_captured` | Whether can be captured |
| `country_leader` | Country leader role |
| `advisor` | Cabinet advisor role |
| `field_marshal` | Marshal role |
| `corps_commander` | General role |
| `navy_leader` | Navy general role |
| `scientist` | scientist role |

## Leader

```pdx
country_leader = {
	ideology=nazism
	traits = {my_trait}
	expire = "1965.1.1.1"
	desc = TAG_leader_desc
}
```
## Consultant

```pdx
advisor = {
	slot = political_advisor
	idea_token = TAG_my_advisor
	ledger = army
	cost = 150
	traits = { silent_workhorse }
	can_be_fired = yes
	removal_cost = -1
	on_add = { }
	on_remove = { }
	ai_will_do = {
		factor = 1
	}
}
```

### Consultant slot

| Slot | Description |
|------|------|
| `political_advisor` | Political Advisor |
| `army_chief` | Secretary of the Army |
| `navy_chief` | Secretary of the Navy |
| `air_chief` | Secretary of the Air Force |
| `high_command` | Commander-in-Chief |
| `theorist` | theorist |

### ledger

| value | description |
|------|------|
| `army` | Army |
| `air` | Air Force |
| `navy` | navy |
| `military` | military |
| `civilian` | civilian |
| `all` | all |
| `hidden` | hide |
| `invalid` | Invalid |

## General

```pdx
field_marshal = {
	legacy_id = -1
	traits = {my_trait}
	skill=5
	attack_skill=4
	defense_skill = 3
	planning_skill = 4
	logistics_skill=5
}

corps_commander = {
	legacy_id = -1
	traits = {my_trait}
	skill=3
	attack_skill=3
	defense_skill=2
	planning_skill = 2
	logistics_skill=2
}
navy_leader = {
	legacy_id = -1
	traits = {my_trait}
	skill=3
	attack_skill=3
	defense_skill=2
	maneuvering_skill = 2
	coordination_skill = 2
}
```

## Scientist

```pdx
scientist = {
	traits = { my_scientist_trait }
	skills = {
		specialization_land = 1
		specialization_air = 1
		specialization_naval = 1
		specialization_nuclear = 1
	}
	desc = TAG_scientist_desc
}
```

## Dynamic variants

You can use `instance` to switch different versions of the same character based on conditions:

```pdx
TAG_my_character = {
	#Default version
	name = TAG_my_character_default
	country_leader = { ... }

	instance = {
		allowed = {
			has_government = communism
		}
		name = TAG_my_character_communist
		country_leader = {
			ideology = marxism
			traits = { ... }
		}
	}
}
```

## Recruit in history

```pdx
recruit_character = TAG_my_character
```
