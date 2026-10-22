# Modifiers index template

This page explains where **modifier is written, how to check it**, and lists the most frequent keys. A longer country/state related table is available in `data/state-modifiers.md`.

## Possible positions

| Location | Description |
|------|------|
| `idea` / `timed_idea` | National spirit, bill |
| `dynamic_modifiers` | Variable driven modifications |
| `country_leader` / `unit_leader` Traits | Leaders and Generals |
| Technology / Doctrine / Sub-doctrine | Research completion or tracking results |
| Equipment / Modules / Manufacturers / MIO | Production and Combat Bonuses |
| Architecture | Province/Country level effects |
| Ideology `modifiers` | Overview of the ruling party |
| Autonomy level `modifier` | Vassal |
| Terrain/Weather (Map and Strategic Areas) | Combat Environment |
| `modifier = { factor = }` in AI/MTTH | **weight modifier**, not country attribute |

National attribute class modifier keys and AI factors **Do not mix**.

## Query order (it is forbidden to make up key names)

1. `references/data/state-modifiers.md`
2. Ontology: `common/ideas`, `common/country_leader`, `common/unit_leader`, `common/dynamic_modifiers`
3. Ontology: `common/modifier_definitions/` (if there are definitions/classification comments)
4. wiki: **Modifiers**
5. Shuangze Library Teleprompter "Correction Complete Collection" (need to go back to the main body to check)
6. If still nothing, ask the user

## High frequency country correction (excerpt)

```
political_power_factor
political_power_gain
stability_factor
war_support_factor
consumer_goods_factor
production_speed_buildings_factor
production_speed_arms_factory_factor
production_speed_industrial_complex_factor
industrial_capacity_factory
industrial_capacity_dockyard
line_change_production_efficiency_factor
production_factory_max_efficiency_factor
production_factory_efficiency_gain_factor
research_speed_factor
army_org_factor
army_attack_factor
army_defence_factor
army_speed_factor
max_planning
planning_speed
supply_consumption_factor
attrition
winter_attrition_factor
out_of_supply_factor
experience_gain_army
experience_gain_army_factor
description
subscription_factor
mobilization_speed
training_time_factor
justify_war_goal_time
generate_wargoal_tension
join_faction_tension
lend_lease_tension
send_volunteer_factor
opinion_gain_monthly
opinion_gain_monthly_same_ideology
drift_defence_factor
democracy_drift / communism_drift / fascism_drift / neutrality_drift
autonomy_gain
subject_autonomy_gain
cic_to_overlord_factor
mic_to_overlord_factor
```
The specific numerical semantics and positive and negative directions are subject to wiki/original idea.

## How to write equipment bonuses (idea/traits, etc.)

```pdx
equipment_bonus = {
	infantry_equipment = {
		build_cost_ic = -0.1
		soft_attack = 0.05
	}
}
```

See `data/equipment-list.md` for equipment keys.

## Terrain correction (general/troops)

```pdx
modifier = {
	urban = {
		attack = 0.1
		defense = 0.1
	}
	forest = {
		movement = 0.05
	}
}
```

## Dynamic correction

Write the variable name as the value, not the hard number: see `dynamic-modifier-template.md`.

## Localized display

- Ordinary idea: the engine automatically generates tooltip according to modifier
- Dynamic modification: required `custom_effect_tooltip` (`modding-rules.md`)
- Custom modifier definitions (`modifier_definitions`) are advanced, please read the ontology comments before making changes

## Design value

- Percent: **0.05** step
- Daily direction: political power/command power/drift, etc. **0.01** step

## Related

- `data/state-modifiers.md` / `idea-template.md` / `dynamic-modifier-template.md` / `custom-traits-template.md`
