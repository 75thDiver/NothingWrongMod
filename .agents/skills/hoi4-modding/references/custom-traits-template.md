# Custom trait template

There are sub-catalogs for leader/advisor traits and general traits. The original advisor slot effect table can be found in `advisor-traits-template.md`.

## File location

| type | path |
|------|------|
| Country leaders/advisors to leader_traits | `common/country_leader/xx_traits.txt` |
| Traits of army and navy generals | `common/unit_leader/xx_traits.txt` |
| Scientist Traits | `common/scientist_traits/` (see also Special Items) |

## National leader traits (country_leader)

```pdx
leader_traits = {
	TAG_iron_administrator = {
		random=no
		political_power_factor = 0.1
		consumer_goods_factor = -0.05
		stability_factor = 0.05

		ai_will_do = {
			factor = 1
		}
	}
}
```

Character quotes:

```pdx
country_leader = {
	ideology = despotism
	traits = {TAG_iron_administrator}
}
advisor = {
	traits = {TAG_iron_administrator}
	#...
}
```

### Common fields

| Field | Description |
|------|------|
| `random` | Whether to enter the random pool |
| Various modifiers | Country modifiers similar to idea |
| `targeted_modifier` | Targeted at other countries (check vanilla) |
| `equipment_bonus` | Equipment bonus |
| `ai_will_do` | AI weight |
| `command_cap` etc. | Subject to the same characteristics of the vanilla |
Value: Percent **0.05** steps, daily steps towards **0.01** (`modding-rules.md`).

## General traits (unit_leader)

The original `00_traits.txt` has full field annotations at the top. Simplified example:

```pdx
leader_traits = {
	TAG_city_fighter = {
		type = corps_commander
		trait_type = assignable_trait
		gain_xp = {
			is_fighting_in_urban = yes
		}
		cost=1000
		modifier = {
			urban = {
				attack = 0.1
				defense = 0.1
			}
		}
		ai_will_do = {
			factor = 1
		}
		gui_row = -1
	}
}
```

### Important fields (general)

| Field | Description |
|------|------|
| `type` | `all` / `field_marshal` / `corps_commander` / `navy` etc. |
| `trait_type` | `basic_trait` `personality_trait` `assignable_trait` `status_trait` terrain class, etc. |
| `attack_skill` etc. | Integer skill modifier |
| `*_skill_factor` | Skill factor |
| `modifier` / `corps_commander_modifier` / `field_marshal_modifier` | Correction |
| `sub_unit_modifiers` | Unit modifications |
| `parent` / `any_parent` / `mutually_exclusive` | Trait tree relationships |
| `prerequisites` / `allowed` / `gain_xp` | Trigger, the scope is mostly generals |
| `on_add` / `on_remove` / `daily_effect` | Effect |
| `gui_row` / `gui_column` | Unlockable tree position; `-1` does not display in the tree |
| `cost` | Allocation cost |
It is safer to copy adjacent properties of the original and then change them than to invent fields from scratch.

## Localization

```yaml
  TAG_iron_administrator: "Iron-fisted Administrator"
  TAG_iron_administrator_desc: "Description."
  TAG_city_fighter: "Street Fighting Expert"
  TAG_city_fighter_desc: "Description."
```

## Same as original traits

- Give priority to using the original token (see `advisor-traits-template.md` for advisor list)
- Make sure there is no same name before customizing
- The general skill name (such as `engineer_officer`) is based on the body `unit_leader` and the unit history, **No fabrication is allowed**

## Specification

- Modifier keys must actually exist (check `state-modifiers.md` / original traits)
- Note clearly the Chinese trait name
- Do not write "compatible with other mod traits" logic

## Related

- `advisor-traits-template.md` / `character-template.md` / `effects-template.md`
