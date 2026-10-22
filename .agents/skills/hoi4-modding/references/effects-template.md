# Effects template

The effect is executed in the current scope immediately or on call. The complete list is subject to the official wiki **Effects** and the current game version; this page is a high-frequency writing and query portal.

## Use location

- National focus `completion_reward` / `select_effect`
- event `immediate` / `option`
- Resolution `complete_effect` / `remove_effect` etc.
- `history/countries` opening script
- `effect` of `scripted_effects`, `on_actions`
- Concept `on_add` / `on_remove`

## Structural habits

```pdx
completion_reward = {
	add_political_power = 100 # Add 100 political power
	add_ideas = TAG_my_spirit # Add a certain national spirit
	hidden_effect = {
		set_country_flag = TAG_did_thing
	}
	custom_effect_tooltip = TAG_did_thing_tt
}
```

- Percentage gain is based on the **5% principle** (`0.05`)
- Daily categories based on **0.01 rule**
- Prioritize `add_ideas` / `add_timed_idea` for long-term national-level modifiers of national focuses, and do not pile permanent national-level modifiers in `completion_reward` (see `modding-rules.md`)

## Politics and Stability

```pdx
add_political_power = 150
add_stability = 0.05
add_war_support = 0.05
add_popularity = {
	ideology = democratic
	popularity = 0.1
}
set_politics = {
	ruling_party = communism
	elections_allowed = no
}
set_political_party = {
	ideology=fascism
	popularity = 40
}
```
## Idea / Law / Dynamic Modification

```pdx
add_ideas = TAG_spirit
add_timed_idea = {
	idea = TAG_temp_spirit
	days = 365
}
remove_ideas = TAG_spirit
swap_ideas = {
	remove_idea = TAG_old
	add_idea = TAG_new
}
add_dynamic_modifier = { modifier = TAG_dyn }
remove_dynamic_modifier = { modifier = TAG_dyn }
```

## Scientific Research and Doctrine

```pdx
add_research_slot = 1
set_technology = {
	infantry_weapons = 1
}
add_tech_bonus = {
	name = infantry_bonus
	bonus = 0.5
	uses=1
	category = infantry
}
add_doctrine_cost_reduction = {
	name = land_doc_bonus
	cost_reduction = 0.5
	uses=1
	category = land_doctrine
}
army_experience = 25
navy_experience = 25
air_experience=25
```

## Buildings and resources (state scope)

```pdx
219 = {
	add_extra_state_shared_building_slots = 2
	add_building_construction = {
		type = industrial_complex
		level=2
		instant_build = yes
	}
	add_building_construction = {
		type = arms_factory
		level=1
		instant_build = yes
	}
	add_resource = {
		type=steel
		amount = 8
	}
}
```
Comments must write the state locale (see `modding-rules.md`).

## Region and Diplomacy

```pdx
transfer_state = 219
set_state_owner = 219
set_state_controller = 219
add_state_core = 219
add_state_claim = 219
remove_state_claim = 219
add_core_of = RYH # in state scope
add_claim_by = RYH # in state scope

create_wargoal = {
	type = annex_everything
	target=LIT
}
declare_war_on = {
	target=LIT
	type = annex_everything
}
white_peace = LIT
annex_country = {
	target=LIT
	transfer_troops = yes
}
puppet=LIT
set_autonomy = {
	target=LIT
	autonomous_state = autonomy_puppet
	freedom_level = 0.5
}
release = LIT
release_puppet = LIT
```

## Camp

```pdx
create_faction = "my_faction_name"
add_to_faction = HUN
remove_from_faction = HUN
dismantle_faction=yes
```

## Favorability and relationship

```pdx
add_opinion_modifier = {
	target=GER
	modifier = large_increase
}
remove_opinion_modifier = {
	target=GER
	modifier = large_increase
}
give_guarantee = CZE
diplomatic_relation = {
	country=ITA
	relation = non_aggression_pact
	active=yes
}
```
## Manpower, troops, equipment

```pdx
add_manpower=50000
load_oob = "TAG_1936"
division_template = {
	name = "Infantry Division"
	regiments = {
		infantry = { x = 0 y = 0 }
		infantry = { x = 0 y = 1 }
	}
}
create_equipment_variant = {
	name = "a certain tank"
	type = light_tank_chassis_1
	# modules = { ... }
}
add_equipment_to_stockpile = {
	type = infantry_equipment_1
	amount=1000
	producer=ROOT
}
```

## Characters

```pdx
recruit_character = TAG_some_leader
add_country_leader_role = {
	character = TAG_some_leader
	promote_leader = yes
	country_leader = {
		ideology=stalinism
		expire = "1965.1.1"
		traits = { }
	}
}
retire_character = TAG_old_leader
promote_character = TAG_some_leader
```

## Events and Delays

```pdx
country_event = { id = TAG_story.1 }
country_event = { id = TAG_story.2 days = 10 }
country_event = { id = TAG_story.3 hours = 6 random_hours = 12 }
news_event = { id = TAG_news.1 days = 2 }
```
## Flag / variable (usually matched)

```pdx
set_country_flag = TAG_flag
clr_country_flag = TAG_flag
set_global_flag = global_thing_happened
set_variable = { TAG_strength = 1 }
add_to_variable = { TAG_strength = 1 }
```

See `variables-arrays-template.md` for more complete variables/arrays.

## Process control (effect context)

```pdx
if = {
	limit = {
		has_war = yes
	}
	add_war_support = 0.05
	else_if = {
		limit = {
			threat > 0.5
		}
		add_stability = -0.05
	}
	else = {
		add_political_power = 50
	}
}

for_loop_effect = {
	start=0
	end=5
	add_political_power = 10
}

hidden_effect = {
	# Do not display the default tooltip
}
effect_tooltip = {
	# Only display the tooltip without executing it (use with caution and check the version)
}
custom_effect_tooltip = MY_TOOLTIP_KEY
```

## Quick check of common effects (country scope unless otherwise noted)

| Effect | Meaning |
|------|------|
| `add_political_power` | Political power |
| `add_stability` / `add_war_support` | Stability / War support |
| `add_ideas` / `remove_ideas` | National Spirit |
| `add_timed_idea` | Limited time spirit |
| `set_technology` | Directly to technology |
| `add_tech_bonus` | Research bonus cards |
| `army_experience` etc. | Army experience |
| `transfer_state` | Ceded region (country) |
| `create_wargoal` | War goal |
| `declare_war_on` | declare war |
| `puppet` / `set_autonomy` | puppet / autonomy |
| `annex_country` | annexation |
| `country_event` / `news_event` | Call event |
| `set_country_flag` | Country flag |
| `add_opinion_modifier` | Diplomacy modifier |
| `create_faction` / `add_to_faction` | Faction |
| `add_manpower` | Manpower |
| `add_equipment_to_stockpile` | Stock equipment |
| `add_building_construction` | Building (mostly in state) |
| `add_resource` | Resource (state) |
| `add_extra_state_shared_building_slots` | Building slots (state) |
| `every_owned_state` etc. | Traverse the scope |
## Prohibitions and Attention

- Don't make up effect names that don't exist; if you're not sure, check the wiki/vanilla
- Large paragraphs `every_*` must consider tooltip (`hidden_effect` + `custom_effect_tooltip`)
- The meaning of `FROM`/`ROOT` in effects depends on the call stack (see `scopes-template.md`)
- War, annexation, and transfer will trigger `on_actions` in chain, please pay attention to the infinite loop

## Query order

1. This page and related templates
2. There is already a similar `completion_reward`/event in the project
3. Ontology `common/`, `events/`
4. wiki: **Effects**
5. Ask the user

## Related documents

- `scopes-template.md` / `triggers-template.md` / `scripted-effects-template.md` / `on-actions-template.md`
