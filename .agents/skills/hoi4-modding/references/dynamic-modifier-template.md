# Dynamic National Spirit (Dynamic Modifier) complete template

Used to create an ethos whose values change with variables. Defined in `common/dynamic_modifiers/<filename>.txt`, added to country or state via `add_dynamic_modifier`.

## Complete process

```
1. Define modifier in common/dynamic_modifiers/<file>.txt
2. Initialize variables in national focus completion_reward or history/countries
3. Use add_dynamic_modifier to add modifier to the country
4. Subsequent national focuses change the variable value through add_to_variable
5. Use remove_dynamic_modifier to remove when necessary
```

## File location

```
common/dynamic_modifiers/<filename>.txt
```

## Define structure

```hoi4
# <modifier_id> is both a script ID and a localization key name
<modifier_id> = {
    enable = {
        # Trigger condition; common tag = XXX
        tag=RYH
    }

    icon = <icon_name> # Icon name; write whatever the user gives you, do not add the GFX_idea_ prefix without authorization

    # The value of the correction item must be a variable name, and the actual value is determined by the corresponding variable
    production_speed_buildings_factor = <var_building_speed>
    industrial_capacity_factory = <var_factory_output>
    consumer_goods_factor = <var_consumer_goods>
    stability_factor = <var_stability>
}
```
## Numerical design principles

- Percentage gain uses `0.05` (5%) as the basic unit.
- When initializing variables, use `set_variable` first, and then use `add_to_variable` for subsequent enhancement.
- Debuff also follows the 5% rule and is written as `-0.05`.

## Add and update examples

```hoi4
# 1. Initialize variables and add dynamic national spirit (usually written in national focus completion_reward)
set_variable = { RYH_42_building_speed = 0.05 }
set_variable = { RYH_42_factory_output = 0.05 }
set_variable = { RYH_42_consumer_goods = -0.05 }
set_variable = { RYH_42_stability = 0.05 }

add_dynamic_modifier = {
    modifier = RYH_42_revival_plan
}

# 2. Subsequently use variables to dynamically change the effect
add_to_variable = { RYH_42_factory_output = 0.05 }
add_to_variable = { RYH_42_consumer_goods = -0.05 }

# 3. When it needs to be removed
remove_dynamic_modifier = {
    modifier = RYH_42_revival_plan
}
```

## Optional parameters for scope and number of days

```hoi4
add_dynamic_modifier = {
    modifier = <modifier_id>
    scope = GER # Optional: specify scope
    days = 30 # Optional: Automatically removed after a limited time of X days
}
```

## Add in hidden_effect
The actual effect of adding dynamic national spirit can be hidden and only the `custom_effect_tooltip` is exposed to the player.

```hoi4
completion_reward = {
    # Write prompt first
    custom_effect_tooltip = RYH_42_tt
    custom_effect_tooltip = RYH_42_tt1
    custom_effect_tooltip = RYH_42_tt2
    custom_effect_tooltip = RYH_42_tt3
    custom_effect_tooltip = RYH_42_tt4

    # Then wrap the actual effect into hidden_effect
    hidden_effect = {
        set_variable = { RYH_42_building_speed = 0.05 }
        set_variable = { RYH_42_factory_output = 0.05 }
        set_variable = { RYH_42_consumer_goods = -0.05 }
        set_variable = { RYH_42_stability = 0.05 }

        add_dynamic_modifier = {
            modifier = RYH_42_revival_plan
        }
    }
}
```

## Complete example

### `common/dynamic_modifiers/RYH_00.txt`

```hoi4
RYH_42_revival_plan = {
    enable = {
        tag=RYH
    }
    icon = generic_improved_industries
    production_speed_buildings_factor = RYH_42_building_speed
    industrial_capacity_factory = RYH_42_factory_output
    consumer_goods_factor = RYH_42_consumer_goods
    stability_factor = RYH_42_stability
}
```
### `common/national_focus/RYH.txt`

```hoi4
focus = {
    id = RYH_42
    # ...
    completion_reward = {
        custom_effect_tooltip = RYH_42_tt
        custom_effect_tooltip = RYH_42_tt1
        custom_effect_tooltip = RYH_42_tt2
        custom_effect_tooltip = RYH_42_tt3
        custom_effect_tooltip = RYH_42_tt4

        hidden_effect = {
            set_variable = { RYH_42_building_speed = 0.05 }
            set_variable = { RYH_42_factory_output = 0.05 }
            set_variable = { RYH_42_consumer_goods = -0.05 }
            set_variable = { RYH_42_stability = 0.05 }

            add_dynamic_modifier = {
                modifier = RYH_42_revival_plan
            }
        }
    }
}

focus = {
    id = RYH_421
    # ...
    completion_reward = {
        custom_effect_tooltip = RYH_42_add_tt
        custom_effect_tooltip = RYH_421_tt

add_to_variable = { RYH_42_factory_output = 0.05 }
    }
}
```

## Localization

### Name and description of national spirit

```yaml
  <modifier_id>: "National Spiritual Name"
  <modifier_id>_desc: "Description of national spirit"
```

Example:

```yaml
  RYH_42_revival_plan: "Moscow Revitalization and Economic Reconstruction Plan"
  RYH_42_revival_plan_desc: "With New Moscow as the core, gradually restore Russia's economy and order."
```

### Tooltip writing method

When dynamic national spirit uses variables, the game will not automatically display the specific effect, and `custom_effect_tooltip` must be handwritten in the national focus.

#### Obtained for the first time

```yaml
  <modifier_id>_tt: "Get §Y<name>§!:"
  <modifier_id>_tt1: " $MODIFIER_XXX$:§G +5.00%§!"
  <modifier_id>_tt2: " $MODIFIER_YYY$:§Y -5.00%§!"
```

Example:

```yaml
  RYH_42_tt: "Acquired §YMoscow Reconstruction and Economic Reconstruction Plan§!:"
  RYH_42_tt1: "$MODIFIER_PRODUCTION_SPEED_BUILDINGS_FACTOR$:§G +5.00%§!"
  RYH_42_tt2: "$MODIFIER_INDUSTRIAL_CAPACITY_FACTOR$:§G +5.00%§!"
  RYH_42_tt3: "$MODIFIER_CONSUMER_GOODS_FACTOR$:§Y -5.00%§!"
  RYH_42_tt4: "$MODIFIER_STABILITY_FACTOR$:§G +5.00%§!"
```
#### Subsequent additional effects

When the same dynamic national spirit is strengthened by subsequent national focuses, use the `Additional Effect:` title.

```yaml
  <modifier_id>_add_tt: "§Y<name>§! Additional effect:"
  <focus_id>_tt: " $MODIFIER_XXX$:§G +5.00%§!"
```

Example:

```yaml
  RYH_42_add_tt: "§YMoscow Reconstruction and Economic Reconstruction Plan§! Additional effect:"
  RYH_421_tt: "$MODIFIER_INDUSTRIAL_CAPACITY_FACTOR$:§G +5.00%§!"
```

### Fix localization key reference

Commonly used correction tokens in `custom_effect_tooltip`:

- `$MODIFIER_RESEARCH_SPEED_FACTOR$` — research speed
- `$MODIFIER_PRODUCTION_SPEED_BUILDINGS_FACTOR$` — building speed
- `$MODIFIER_INDUSTRIAL_CAPACITY_FACTOR$` — factory output
- `$MODIFIER_CONSUMER_GOODS_FACTOR$` — consumer goods
- `$MODIFIER_STABILITY_FACTOR$` — Stability
- `$MODIFIER_WAR_SUPPORT_FACTOR$` — war support
- `$MODIFIER_POLITICAL_POWER_GAIN$` — Daily political power

## Notes

1. **Use the icon directly according to the writing method given by the user**, do not add the `GFX_idea_` prefix without authorization.
2. **Variable names must be consistent**: The variable names used in `set_variable` / `add_to_variable` / `dynamic_modifiers` must be consistent.
3. **The first time you obtain it, use the `obtain' title, and subsequent enhancements, use the `Additional Effects' title**.
4. **Multiple correction suggestions are split into multiple localization keys**, one `custom_effect_tooltip` per line to facilitate line breaks.
5. Dynamic national spirit will not automatically display the effect and must be combined with `custom_effect_tooltip`.
6. `add_dynamic_modifier` can be written in `hidden_effect`, but the tooltip must remain at the top level of `completion_reward`.
7. Don’t write `custom_effect_tooltip` in ordinary ideas, it is only needed for dynamic national spirit.
8. Since the effect depends on variables, it is recommended that the user manually verify it in the game and do not actively start the game or run the program for the user.
## Common mistakes

- Write `custom_effect_tooltip` in idea definition.
- Prefix `icon` with `GFX_idea_`.
- Annotate effects involving state with `state_XXX` or obscure region names.
- Write the specific effects of dynamic folk spirit directly in comments instead of using `custom_effect_tooltip`.
- Use the same tooltip title for both initial acquisition and subsequent additions.
