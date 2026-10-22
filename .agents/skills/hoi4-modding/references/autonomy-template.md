# Autonomy/Puppet System Template

Definition: `common/autonomous_states/<xxx>.txt`
Start/effect settings: `set_autonomy` (history or effect).

## Define structure

```pdx
autonomy_state = {
	id = autonomy_puppet

	default=yes
	is_puppet = yes
	min_freedom_level = 0.4
	manpower_influence = 0.9

	rule = {
		desc = "RULE_DESC_IS_A_SUBJECT"
		can_not_declare_war = yes
		can_decline_call_to_war = no
		can_be_spymaster = no
		contributes_operatives = no
		can_create_collaboration_government = no
		units_deployed_to_overlord = no
	}

	modifier = {
		autonomy_manpower_share = 0.9
		can_master_build_for_us = 1
		extra_trade_to_overlord_factor = 1.0
		overlord_trade_cost_factor = -0.9
		cic_to_overlord_factor = 0.25
		mic_to_overlord_factor = 0.75
		research_sharing_per_country_bonus_factor = -0.5
	}

	ai_subject_wants_higher = {
		factor = 1.0
	}
	ai_overlord_wants_lower = {
		factor = 1.0
	}
	ai_overlord_wants_garrison = {
		always=no
	}
allowed = {
		# What kind of lord/vassal can enter this level?
	}

	can_take_level = {
		# Conditions for rising to a more free level
	}
	can_lose_level = {
		# Downgrade conditions
	}
}
```

## Original common id (excerpt)

| id | meaning (approximately) |
|----|------------|
| `autonomy_dominion` | Dominion |
| `autonomy_colony` | Colonial Colony |
| `autonomy_puppet` | puppet |
| `autonomy_integrated_puppet` | Integrated puppet |
| `autonomy_supervised_state` | Supervisory state |
| `autonomy_reichskommissariat` | Commissionerate area |
| `autonomy_reichsprotectorate` | Protectorate |
| `autonomy_satellite` | satellite state |
| `autonomy_collaboration_government` | Collaboration Government |
| `autonomy_personal_union` | Co-ownership Confederacy |
| `autonomy_wtt_imperial_*` | Empire related |
| `autonomy_aat_defense_council_member` | Nordic Defense Council (DLC) |

The complete file name is subject to `common/autonomous_states/`. See also `country-history-template.md` for the history list.

## Set up autonomy

```pdx
set_autonomy = {
	target=LIT
	autonomous_state = autonomy_puppet
	freedom_level = 0.5
}
puppet=LIT
end_puppet = LIT
```
- `freedom_level`: 0–1, affects the progress of upgrading and downgrading
- Overlord/vassal scope: when the effect is written on the overlord, `target = vassal`

## allowed design

The custom level must be written clearly:

- Required DLC
- Overlord tag / ideology
- vassal region or flag

Prevent all countries from being able to enter the exclusive level inexplicably.

## and Diplomatic Rules

`rule` controls whether to declare war, refuse the opponent's recall, whether to deploy troops to the suzerain, whether to be a spy supervisor, etc.
Before modification, compare the vanilla `puppet.txt` / `integrated_puppet.txt`.

## Localization

```yaml
  autonomy_puppet: "Puppet State"
  # rule desc keys etc.
```

## Specification

- Added `id` globally unique
- Values (factory turn-over, manpower sharing) are based on the design document and are close to the same level as the vanilla by default
- For `on_subject_free` / `on_puppet` and other hooks, see `on-actions-template.md`

## Related

- `country-history-template.md` / `effects-template.md` / `on-actions-template.md`
