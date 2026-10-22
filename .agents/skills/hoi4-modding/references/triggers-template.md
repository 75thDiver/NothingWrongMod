# Condition (Triggers) template

The condition evaluates to yes/no in the current scope. Trigger blocks for `trigger`, `available`, `visible`, `allowed`, `limit`, `modifier = { factor = ... }`, etc.

The complete list is subject to the current version of wiki **Triggers**; this page is written for high frequency.

## Logical combination

```pdx
trigger = {
	always=yes
	always=no

	AND = {
		has_war = yes
		tag=GER
	}
	OR = {
		has_government = fascism
		has_government = neutrality
	}
	NOT = {
		is_in_faction = yes
	}
	if = {
		limit = {
			has_dlc = "No Step Back"
		}
		has_tech = improved_infantry_weapons
	}
}
```

- Multiple conditions within the same block default to **AND**
- `count_triggers` and other rare structures are subject to wiki

## National Identity and Politics

```pdx
tag=GER
original_tag = GER
is_ai = yes
is_major = yes
has_government = democratic
has_country_leader = {
	character = TAG_leader
	ruling_only = yes
}
has_country_flag = TAG_flag
has_global_flag = some_global
has_idea = TAG_spirit
has_dynamic_modifier = {
	modifier = TAG_dyn
}
```
## War and Diplomacy

```pdx
has_war = yes
has_war_with = SOV
has_war_together_with = ITA
is_in_faction = yes
is_in_faction_with = GER
is_faction_leader = yes
is_subject = yes
is_subject_of = ENG
is_puppet = yes
has_guaranteed = CZE
has_non_aggression_pact_with = SOV
has_opinion = {
	target=GER
	value > 50
}
has_wargoal_against = POL
surrender_progress > 0.3
```

## Country value

```pdx
has_political_power > 100
has_stability > 0.5
has_war_support > 0.6
num_of_factories > 50
num_of_military_factories > 20
num_of_civilian_factories > 20
num_of_naval_factories > 5
num_of_available_civilian_factories > 10
amount_research_slots > 3
threat > 0.25
date > 1939.9.1
```

Comparator: `>` `<` `=`, etc., refer to the wiki description of the trigger.

## Technology and Doctrine

```pdx
has_tech = infantry_weapons
is_researching_technology = improved_infantry_weapons
has_doctrine = mobile_warfare # Check the vanilla for specific key names
```
## Region (country or state context)

```pdx
# Country scope
owns_state = 219
controls_state = 219
has_full_control_of_state = 219
any_owned_state = {
	is_coastal = yes
	arms_factory > 0
}
any_controlled_state = {
	is_core_of = ROOT
}

# state scope
state=219
is_owned_by = GER
is_controlled_by = GER
is_core_of = GER
is_claimed_by = GER
is_capital = yes
is_coastal = yes
industrial_complex > 2
arms_factory > 1
infrastructure > 3
free_building_slots = {
	building = industrial_complex
	size > 0
	include_locked=yes
}
```

## Variable conditions

```pdx
check_variable = {
	var = TAG_strength
	value=3
	compare = greater_than_or_equals
}
# compare common: less_than / less_than_or_equals / equals / not_equals / greater_than / greater_than_or_equals

has_variable = TAG_strength
```

See `variables-arrays-template.md` for details.

## Script conditions

```pdx
my_scripted_trigger = yes
my_scripted_trigger = no
```
See `scripted-triggers-template.md` for definition.

## National Policy / Decision / Event Progress

```pdx
has_completed_focus = TAG_focus_id
has_active_mission = TAG_mission_id
has_decision = TAG_decision_id
has_country_custom_difficulty_setting = yes # Use less often
```

## Existence traversal (condition)

```pdx
any_country = {
	original_tag = SOV
	has_government = communism
}
all_enemy_country = {
	surrender_progress > 0.5
}
any_neighbor_country = {
	has_war_with = ROOT
}
any_character = {
	is_country_leader = yes
	has_trait = TAG_trait
}
```

`any_*` = there is one satisfaction; `all_*` = all are satisfied. Don't use `every_*` as a condition.

## Differences in Focus Tree/Decision Fields

| Fields | Common Opportunities |
|------|----------|
| `allowed` | Often started or occasionally tested (such as whether the decision category appears) |
| `available` | Persistence: whether clickable |
| `visible` | Persistence: whether to display |
| `trigger` (event) | Automatic trigger condition |
| `limit` | Traverse/if filter |

Writing wrong fields will result in "never visible" or "AI clutter". Please check the original files of the same type before making changes.

## Common trigger quick check

| Condition | Meaning |
|------|------|
| `tag` / `original_tag` | current / original tag |
| `has_war` / `has_war_with` | war |
| `has_government` | Ruling Party Ideology Group |
| `has_idea` | own idea |
| `has_country_flag` | country flag |
| `has_tech` | Researched technology |
| `has_completed_focus` | Completed focus |
| `owns_state` / `controls_state` | Own/control regions |
| `is_in_faction_with` | Same camp |
| `is_subject` / `is_subject_of` | vassals |
| `has_stability` / `has_war_support` | stability / war support |
| `num_of_factories` | Number of factories |
| `date` | Date comparison |
| `check_variable` | Variable comparison |
| `any_owned_state` | There is an owned land that meets the conditions |
| `always` | Always true/always false |
## Specification

- It is forbidden to make up trigger names
- Complex condition extraction `scripted_triggers` reuse
- For traversing tooltip and effect side specifications, see `modding-rules.md`
- When not found: wiki **Triggers** → Original → Ask the user

## Related documents

- `scopes-template.md` / `effects-template.md` / `scripted-triggers-template.md` / `variables-arrays-template.md`
