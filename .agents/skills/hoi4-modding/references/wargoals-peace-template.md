# War Goals and Peace Conference Template

## War target definition

File: `common/wargoals/00_invasion.txt` (new files can be added)

```pdx
wargoal_types = {
	take_state = {
		# PREV = target country, ROOT = owner of target (see original comments)
		allowed = { }
		available = { }

		take_states = { }

		generate_base_cost = 200
		generate_per_state_cost = 50
		take_states_limit = 5
		take_states_cost = -20
		expire=60
		threat=2
	}

	puppet_wargoal_focus = {
		allowed = { always = no }
		puppet = { always = yes }
		generate_base_cost = 200
		generate_per_state_cost = 50
		puppet_cost = -50
		expire=730
		threat=2
	}
}
```

### Field concept

| Field | Description |
|------|------|
| `allowed` / `available` | Can it be generated/used |
| `take_states` / `puppet` / `force_government`, etc. | Action type after victory (subject to the original block) |
| `generate_*_cost` | Justify cost |
| `expire` | Expiration days |
| `threat` | The impact of world tension |

National focus-specific goals are often `allowed = { always = no }` and are created solely by effect.
## Create and declare war (effect)

```pdx
create_wargoal = {
	type = annex_everything
	target=LIT
}
declare_war_on = {
	target=LIT
	type = annex_everything
}
```

`type` must be a defined wargoal token. Common original names: `take_state`, `annex_everything`, `puppet_wargoal_focus`, `topple_government`, etc. - **Subject to the ontology file, no inferences are allowed**.

## Tension and Ideology

`generate_wargoal_tension` in the main ideology `modifiers` and other influence justifications (`ideologies-template.md`).  
Democracy etc. may `can_only_justify_war_on_threat_country`.

## Peace Conference (Concept)

Directory: `common/peace_conference/`

| subdirectory/file | purpose |
|-------------|------|
| `categories/` | Peace operations categories |
| `cost_modifiers/` | Cost modifiers (if any) |
| `ai_peace/` | AI peaceful desires `peace_ai_desires` |

```pdx
peace_ai_desires = {
	take_our_cores = {
		peace_action_type = { take_states }
		enable = {
			ROOT = { tag = ROOT.FROM }
			ROOT.FROM.FROM.FROM = { is_core_of = ROOT.FROM }
		}
		ai_desire = 100
	}
}
```
The scope chain is special in peace conferences (`ROOT`/`FROM` multi-level). **You must compare the original comments and `documentation` (if any)**, and do not use the FROM intuition of ordinary events.

## Script side related effects

```pdx
white_peace = LIT
annex_country = {
	target=LIT
	transfer_troops = yes
}
puppet=LIT
transfer_state = 96
```

Direct annexation/white peace that skips the meeting will bypass some peace AI, narrative events are commonly used, pay attention to tension and alliance relationships.

## on_actions

- `on_declare_war`
- `on_capitulation`
- `on_peaceconference_started` / `on_peaceconference_ended`
- `on_annex`

See `on-actions-template.md`.

## Specification

- New wargoal needs localized name and description
- National focus uses `create_wargoal` for the target, and considers `expire`
- Changing the peace AI will affect the overall situation, and the total conversion will be greatly changed; content mod should be used with caution `00_misc.txt`
- The complete fields are subject to wiki **War goal** / **Peace conference** and the ontology.

## Related

- `effects-template.md` / `triggers-template.md` / `ideologies-template.md` / `on-actions-template.md`
