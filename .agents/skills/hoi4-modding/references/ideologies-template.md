# Ideology template

File location: `common/ideologies/00_ideologies.txt` (can be split into multiple files and eventually merged).

## Structure

```pdx
ideologies = {
	democratic = {
		types = {
			conservatism = { }
			liberalism = { }
			socialism = { }
			populism = { }
		}

		dynamic_faction_names = {
			"FACTION_NAME_DEMOCRATIC_1"
			"FACTION_NAME_DEMOCRATIC_2"
		}

		color = { 0 0 255 }

		rules = {
			can_declare_war_on_same_ideology = no
			can_force_government = yes
			can_send_volunteers = no
			can_puppet = no
			can_lower_tension = yes
			can_only_justify_war_on_threat_country = yes
			can_guarantee_other_ideologies = yes
			can_create_collaboration_government = no
		}

		can_host_government_in_exile = yes

		war_impact_on_world_tension = 0.25
		faction_impact_on_world_tension = 0.1

		modifiers = {
			generate_wargoal_tension = 1.00
			join_faction_tension = 0.80
			lend_lease_tension = 0.50
			#Intelligence, embargo, etc. modifiers see the vanilla
		}
faction_modifiers = {
			faction_trade_opinion_factor = 0.50
		}

		ai_democratic = yes
	}
}
```

## Main ideology vs sub-ideology

| Hierarchy | Example | Usage |
|------|------|------|
| Main group | `democratic` / `communism` / `fascism` / `neutrality` | `has_government`, voter support bar, legal availability |
| Subtypes | `marxism` / `stalinism` / `nazism` | `country_leader = {ideology = ... }` |

What is written in the character is the **sub-ideology** token:

```pdx
country_leader = {
	ideology=stalinism
	traits = { }
	expire = "1965.1.1"
}
```

`set_politics = { ruling_party = communism }` uses the **main group**.

## Original main group and common subtypes

- **democratic**: `conservatism` `liberalism` `socialism` `populism`
- **communism**: `marxism` `leninism` `stalinism` `anti_revisionism` `anarchist_communism` …
- **fascism**: `nazism` `gen_nazism` `fascism_ideology` `falangism` `rexism` …
- **neutrality**: `despotism` `oligarchism` `anarchism` `moderatism` `centrism` …
Based on the current ontology `00_ideologies.txt`; DLC may add subtypes (such as `can_be_randomly_selected = no`).

## Add main ideology (cautious)

1. Add main group + `types` in `ideologies = { }`
2. Added `color`, `rules`, `modifiers`, AI flags (`ai_fascist`, etc., check the vanilla)
3. Localization: ideology name, drill-down description
4. Interface/GFX: support icons and legends (interface and diagrams are often required)
5. Bill `allowed`, national focus `available`, event conditions fully adapted
6. Character sub-ideology, `set_popularities` key name

Total conversions are done only when doing new main groups; content mods take precedence over adding subtypes to existing main groups.

## Add new sub-ideology

```pdx
communism = {
	types = {
		marxism = { }
		TAG_councilism = {
			can_be_randomly_selected = no
		}
	}
}
```

- Localized subtype name
- leader `ideology = TAG_councilism`
- Random leader pool available `can_be_randomly_selected`

## history settings

```pdx
set_politics = {
	ruling_party = neutrality
	elections_allowed = no
}
set_popularities = {
	democratic=10
	community = 10
	fascism = 10
	neutrality=70
}
```

Key is **Main Group**; sum should be 100.

## Specification

- Don't make up subtype names that the vanilla doesn't have but don't define them
- Changing `rules` will affect declaration of war/guaranteed independence/tension, and requires design confirmation
- Disabled compatibility patch "detect other mod ideologies"
## Related

- `character-template.md` / `country-history-template.md` / `idea-template.md` / `localisation-syntax-template.md`
