# Occupation Law and Resistance/Compliance Templates

## Occupation Law

File: `common/occupation_laws/occupation_laws.txt`

The original document has full comments at the top. Streamline fields:

```pdx
TAG_harsh_occupation = {
	tooltip = TAG_harsh_occupation_tt
	icon = "GFX_occupation_policy_icon_strip:3"
	sound_effect = "Martial_Law_Interface_Harsh_Occupation"

	visible = {
		# occupying power scope
	}
	available = {
		# FROM = related to the occupied party (see original comments)
	}

	fallback_law = foreign_civilian_oversight
	# main_fallback_law = yes # Global main fallback, usually only one for the whole file

	state_modifier = {
		resistance_target = 0.1
		local_factories = -0.1
		required_garrison_factor = 0.1
	}
	suppressed_state_modifier = {
		# When the resistance is pressed to 0
	}

	gui_order = 5

	ai_will_do = {
		base=10
		modifier = {
			add=50
			# state scope; FROM occupying power
		}
	}
}
```

Special: `missing_garrison_law`, scaling of insufficient garrison penalties, etc. See the vanilla.

## Resistance/Compliance Fixes

Directory:

- `common/resistance_compliance_modifiers/`
- `common/resistance_activity/` (resistance activity)
```pdx
compliance_25 = {
	type = core_compliance_modifier
	icon = "GFX_occupation_compliance_modifier_strip:2"
	small_icon = "GFX_occupation_compliance_modifier_small_strip:2"
	threshold = 25
	margin=2
	state_modifier = {
		required_garrison_factor = -0.25
		recruitable_population = 0.005
	}
}
```

Changes such as resistance targets and activity frequency affect the global occupation experience, and the content mod carefully changes the original curve.

## Effect side

```pdx
set_occupation_law = {
	# Check wiki / original effect name
}
# See the Effects page for state modification, compliance/resistance variable effects
```

## Specification

- New law must be localized `tooltip`/name
- AI `ai_will_do` is in state scope, pay attention to performance
- Read the vanilla first when linking with autonomous and cooperative government systems

## Related

- `autonomy-template.md` / `modifiers-index-template.md` / `state-template.md`
