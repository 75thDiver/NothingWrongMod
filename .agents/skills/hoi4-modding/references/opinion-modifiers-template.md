> Diplomatic favorability modifier is used to adjust the relationship between two countries.

# Diplomatic favorability (Opinion Modifiers) template

## Backend definition

File location: `common/opinion_modifiers/<xxx>.txt`

```pdx
opinion_modifiers = {

	SOV_SPR_opinion_modifier = {
		value = 50 #Basic value of favorability, positive means friendly, negative means disgust
		decay = -1 # Monthly change value
		trade = yes #Whether it affects trade relations
		max_trust = 100 # Maximum trust value
		min_trust = -100 # Minimum trust value
	}

}
```

## Common field descriptions

| Field | Description |
|------|------|
| `value` | Initial favorability correction value |
| `decay` | Monthly natural decay/growth |
| `trade` | Whether there is a related trade relationship |
| `max_trust` | Maximum trust value limit |
| `min_trust` | Minimum trust value lower limit |
| `months` / `years` / `days` | Duration (optional) |
| `target` | Whether to target the target (the role is not yet clear) |

## Front-end usage

### Logic of `add_opinion_modifier`

`add_opinion_modifier` is written in the scope of the **party holding the favorable opinion**, and `target` is the **party being evaluated**.

- Want to make POA less favorable to RYH: ```pdx
POA = {
    add_opinion_modifier = {
        target=RYH
        modifier = RYH_sabotage_POA
    }
}
```
- Want to make RYH less favorable to POA:```pdx
RYH = {
    add_opinion_modifier = {
        target=POA
        modifier = RYH_sabotage_POA
    }
}
```

### Example of increasing favorability in national focus

```pdx
completion_reward = {
	SPR = {
		add_opinion_modifier = {
			target=ROOT
			modifier = SOV_SPR_opinion_modifier
		}
	}
}
```

### Commonly used effects

```pdx
#Add diplomatic relations modification (change in current country's favorability towards target)
add_opinion_modifier = {
	target=TAG
	modifier = my_opinion_modifier
}

# Remove diplomatic relations modifier
remove_opinion_modifier = {
	target=TAG
	modifier = my_opinion_modifier
}

# Reverse addition (target’s change in favorability towards the current country)
reverse_add_opinion_modifier = {
	target=TAG
	modifier = my_opinion_modifier
}

# Set world tension
add_named_threat = {
	threat = 0.05
	name = my_threat_name
}
```

## Example

```pdx
opinion_modifiers = {
	TAG_friendly_gesture = {
		value=25
		decay = -0.5
		trade=yes
		max_trust = 50
		min_trust = 0
	}
	TAG_hostile_action = {
		value = -50
		decay = 1
		trade = no
		max_trust = 0
		min_trust = -100
	}
}
```
