# Balance of Power template

## File location

`common/bop/<xxx>.txt`

## Infrastructure

```pdx
test_bop = {
	initial_value = 0 #Initial position
	left_side = left_name # left name
	right_side = right_name #right side name

	decision_category = test_decision # Associated decision category

	# middle range
	range = {
		id = mid_range
		min=-0.1
		max=0.1
		modifier = {
			# Continuous effect
		}
	}

	# left
	side = {
		id = left_side
		icon = GFX_left_icon

		range = {
			id = left_range
			min=-1
			max = -0.1

			on_activate = {
				# Triggered instantly when entering this range
			}
			on_deactivate = {
				# Triggers instantly when leaving this range
			}

			modifier = {
				# Continuous effect
			}

			rule = {
				# Game rules settings
			}
		}
	}

	# right side
	side = {
		id = right_side
		icon = GFX_right_icon

		range = {
			id = right_side_range
			min=0.1
			max = 1

			modifier = {
				# Continuous effect
			}
		}
	}
}
```

## Common field descriptions

| Field | Description |
|------|------|
| `initial_value` | Initial value, range `-1.0` to `1.0` |
| `left_side` / `right_side` | Side name keys |
| `decision_category` | The associated decision category |
| `range` | Determination interval, you can write multiple |
| `id` | interval identifier |
| `min` / `max` | Upper and lower bounds of the interval |
| `modifier` | Continuous modifier |
| `on_activate` | Triggered when entering the range |
| `on_deactivate` | Triggered when leaving the interval |
| `rule` | Game rule settings |
| `icon` | side icon |
## Modify BOP value

In a decision, focus, or event:

```pdx
add_power_balance_value = {
	id = test_bop
	value=0.05
}
```

```pdx
set_power_balance = {
	id = test_bop
	left_side = left_side # Directly to the left
}
```
