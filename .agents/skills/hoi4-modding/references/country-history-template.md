> The essence of the national history file is a collection of effects that take effect at the start of the game, and any effect code can be filled in.

# National historical document template

## File location

`history/countries/<TAG> - <country name>.txt`

File name format: `TAG` (in `common/country_tags`) + ` - ` + `country name` (corresponding `.txt` file name in `common/countries`).

## Infrastructure

```pdx
capital=1234

oob = "TAG_army_1936"
set_naval_oob = "TAG_navy_1936"
set_air_oob = "TAG_air_1936"

set_research_slots = 3
set_stability = 0.5
set_war_support = 0.5

set_technology = {
	infantry_weapons = 1
}

set_convoys = 100
starting_train_buffer = 20
set_fuel_ratio = 0.5
set_fuel = 100000

set_politics = {
	ruling_party = neutrality
	last_election = "1932.11.8"
	election_frequency = 48
	elections_allowed = yes
}

set_popularities = {
	democratic = 25
	community = 25
	fascism = 25
	neutrality=25
}

add_ideas = {
	my_idea_1
	my_idea_2
}

add_dynamic_modifier = {
	modifier = my_dynamic_modifier
}
set_variable = {
	my_variable = 100
}

set_autonomy = {
	target = PUP
	autonomous_state = autonomy_puppet
}

# Create equipment variants, see equipment-variant-template.md for details
# create_equipment_variant = { ... }
```

## Common field descriptions

| Field | Description |
|------|------|
| `capital` | Capital province ID |
| `oob` | Army starting organization |
| `set_naval_oob` | Naval starting establishment |
| `set_air_oob` | Air Force starting establishment |
| `set_research_slots` | Number of research slots |
| `set_stability` | Stability |
| `set_war_support` | War support |
| `set_technology` | Starting technology |
| `set_convoys` | Number of convoys |
| `starting_train_buffer` | Number of trains |
| `set_fuel_ratio` | Starting fuel ratio |
| `set_fuel` | Starting fuel quantity |
| `set_politics` | Political settings |
| `set_popularities` | Party support |
| `add_ideas` | Starting national spirit |
| `add_dynamic_modifier` | Dynamic modification |
| `set_variable` | Set variables |
| `set_autonomy` | Set vassal relationship |
| `create_equipment_variant` | Starting equipment variant |

## Ruling Party

| Ideology | Code |
|------|------|
| Democracy | `democratic` |
| Communism | `communism` |
| fascism | `fascism` |
| Neutrality | `neutrality` |
## Type of puppet state

| Type | Description |
|------|------|
| `autonomy_dominion` | Dominion |
| `autonomy_supervised_state` | Supervisory state |
| `autonomy_colony` | Colonial Colony |
| `autonomy_puppet` | Puppet state |
| `autonomy_integrated_puppet` | Semi-annexed puppet state |
| `autonomy_reichskommissariat` | Commissionerate area |
| `autonomy_reichsprotectorate` | Protectorate |
| `autonomy_satellite` | satellite state |
| `autonomy_wtt_imperial_associate` | Imperial Association |
| `autonomy_wtt_imperial_protectorate` | Imperial Protectorate |
| `autonomy_wtt_imperial_subject` | Imperial subject country |
| `autonomy_collaboration_government` | Collaboration Government |
| `autonomy_personal_union` | Co-ownership Confederacy |
| `autonomy_communist_satellite` | Satellite state |
| `autonomy_occupation_zone` | Occupation zone |
| `autonomy_aat_defense_council_member` | Nordic Defense Council Member States |
| `autonomy_austro_hungarian_subject` | Austria-Hungary Empire vassal |
| `autonomy_volkskommissariat` | People's Commissioner's Area |
| `autonomy_eu_member` | European Union member state |

## Notes
It is best to leave a blank line at the end of the history file to prevent the stupid donkey from not reading the last line.
