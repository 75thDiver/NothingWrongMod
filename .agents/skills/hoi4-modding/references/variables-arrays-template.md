# Variables, arrays and Event Target templates

Used for dynamic numerical values, list logic, and cross-scope parameter passing. See wiki **Variables** / **Arrays** for a complete list; see `dynamic-modifier-template.md` for integration with dynamic ethos.

## Variable type (concept)

| Category | Description |
|------|------|
| Country variable | Exists in a certain country scope |
| Global variables | `global.` prefix, shared by the whole game |
| Temporary variable | `set_temp_variable`, valid within the current effect chain |
| State, etc. | Some variables can be hung in state and other scopes |

Prefix examples: `var:my_var`, `global.my_var` (the reading and writing syntax is subject to the specific effect).

## Basic reading and writing

```pdx
set_variable = { TAG_strength = 1 }
set_variable = {
	var = TAG_strength
	value=1
}

add_to_variable = { TAG_strength = 1 }
subtract_from_variable = { TAG_strength = 1 }
multiply_variable = { TAG_strength = 2 }
divide_variable = { TAG_strength = 2 }
modulo_variable = { TAG_strength = 3 }

set_temp_variable = {
	var = temp_calc
	value=10
}
add_to_temp_variable = { temp_calc = 5 }

clear_variable = TAG_strength
```

## Clamp, round, random

```pdx
clamp_variable = {
	var = TAG_strength
	min = 0
	max=10
}
round_variable = TAG_strength
randomize_variable = {
	var = TAG_roll
	distribution = uniform
	min=1
	max = 6
}
```

`distribution`: `uniform` / `binomial` / `poisson` (poisson requires `lambda`), etc., subject to wiki.

## Comparison (condition)

```pdx
check_variable = {
	var = TAG_strength
	value=5
	compare = greater_than_or_equals
}
has_variable = TAG_strength
```

## Dynamic correction linkage

```pdx
set_variable = { RYH_42_factory_output = 0.05 }
add_dynamic_modifier = { modifier = RYH_42_revival_plan }
#In the definition industrial_capacity_factory = RYH_42_factory_output
add_to_variable = { RYH_42_factory_output = 0.05 }
```

Numerical design: Percent **0.05** steps; Daily classes **0.01** steps (`modding-rules.md`).

## Arrays

```pdx
# write
add_to_array = {
	array = TAG_partner_countries
	value = SOV
}
add_to_array = { global.colonial_powers = THIS }

remove_from_array = {
	array = TAG_partner_countries
	value = SOV
}
clear_array = TAG_partner_countries
# Whether it contains (condition, name shall be subject to version)
is_in_array = {
	array = TAG_partner_countries
	value = SOV
}

# Traversal effect
for_each_scope_loop = {
	array = TAG_partner_countries
	#The current scope becomes the corresponding scope of the array element (country, etc.)
	add_political_power = 1
}

for_each_loop = {
	array = TAG_numbers
	set_temp_variable = { v = v }
	# Use v as the element value (the syntax is subject to wiki)
}
```

Original opening example (concept): `add_to_array = { global.colonial_powers = THIS }`.

Array elements can be numeric values ​​or scope tokens; **If you write the wrong type, it will fail silently**. Check `error.log` after changing it.

## Script Collections Collections

Systems such as 1.15+ factions use `common/collections/`. Faction `ratio_progress` etc. See `faction-system-template.md`.
When you need to customize a collection, check the ontology `common/collections/` and wiki, do not invent it from scratch.

## Event targets

```pdx
save_event_target_as = my_target
save_global_event_target_as = my_global_target

event_target:my_target = {
	add_stability = 0.05
}

clear_event_target = my_target
clear_global_event_target = my_global_target
```
Purpose:

- The event option passes the "random country/region" to subsequent effects
- `on_actions` is saved across ROOT/FROM
- Referenced in localization (if supported by key)

## Display variables in localization

```yaml
  TAG_strength_tt: "Current strength: §Y[?TAG_strength]§!"
  TAG_strength_tt_alt: "$TAG_STRENGTH_LOC$: [?ROOT.TAG_strength|%+]"
```

Common format (subject to wiki **Localisation**):

- `[?var_name]`
- `[?ROOT.var_name]`
- `[?var_name|%]` percentage display
- `[?var_name|+=]` with symbols, etc.

For tooltip specifications of dynamic ethos, see `dynamic-modifier-template.md` and `modding-rules.md`.

## MTTH / variables in weights

Events `mean_time_to_happen` and AI `factor` can be operated with modifiers and variables; copy the original blocks of the same type before writing to avoid creating non-existent modifier triggers.

## Standards and Pitfalls

- Globally unique variable name style: `TAG_system_meaning` is recommended (such as `RYH_42_factory_output`)
- `set_variable` is initialized and then `add_to_variable`
- Temporary variables do not assume that they persist across events
- Array traversal + Pay attention to concurrency logic when modifying the same array, and copy to a temporary array first if necessary
- It is forbidden to make up geographical/historical facts corresponding to the meaning of variables in comments.

## Query order

1. This page + `dynamic-modifier-template.md`
2. Variable usage in ontology `common/scripted_effects`
3. wiki: **Variables** / **Arrays**
4. You can refer to the library prompt (variable chapter), but the ontology and wiki still prevail.
5. Ask the user
## Related documents

- `effects-template.md` / `triggers-template.md` / `scopes-template.md` / `scripted-effects-template.md`
