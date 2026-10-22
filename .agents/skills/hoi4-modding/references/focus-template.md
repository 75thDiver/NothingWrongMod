> Corresponds to HOI4 1.19.x version.

# National Focus template

## File location

`common/national_focus/<filename>.txt`

## Filter tag

```pdx
search_filters = { FOCUS_FILTER_POLITICAL } # Politics
search_filters = { FOCUS_FILTER_RESEARCH } # Scientific research
search_filters = { FOCUS_FILTER_INDUSTRY } # Industrial
search_filters = { FOCUS_FILTER_STABILITY } # Stability
search_filters = { FOCUS_FILTER_WAR_SUPPORT } # War support
search_filters = { FOCUS_FILTER_MANPOWER } # Manpower
search_filters = { FOCUS_FILTER_ANNEXATION } # annex
search_filters = { FOCUS_FILTER_HISTORICAL } # Historical facts
```

## National focus tree framework

```pdx
focus_tree = {
	id = mod_focus_tree
	country = {
		factor=0
		modifier = {
			add=10
			tag=GER
		}
	}
	default=no
	Reset_on_civilwarno = no

	#Initial camera position
	initial_show_position = {
		x = 17
		y = 0
		offset = {
			x = 0
			y = 0
			trigger={}
		}
	}
# Navigation buttons
	shortcut = {
		name = my_shortcut_loc
		target = GER_guoce1
		scroll_wheel_factor = 0.5
		trigger={}
	}

	# Quote shared national focus
	shared_focus = GER_shared_focus_1

	# National focus GUI window position
	inlay_window = {
		id = my_inlay_window
		position = { x = 1 y = 20 }
	}

	continuous_focus_position = { x = 1200 y = 100 }

	focus = {
		id = GER_guoce1
		icon = GFX_<icon name>
		x=5
		y = 0
		cost = 10
		search_filters = { FOCUS_FILTER_POLITICAL }
		completion_reward = {
			# Effect
		}
	}

	focus = {
		id = GER_guoce2
		icon = GFX_<icon name>
		relative_position_id = GER_guoce1
		prerequisite = {
			focus = GER_guoce1
			focus = GER_guoce1b
		}
		mutually_exclusive = { focus = GER_guoce2_alt }
		x = -2
		y=1
		cost = 5
		search_filters = { FOCUS_FILTER_INDUSTRY }
		completion_reward = {
			# Effect
		}
	}
}
```

## Ordinary national focus

```pdx
focus = {
	id = GER_my_focus
	icon = GFX_my_focus_icon
# Dynamic icon
	dynamic=yes
	icon = {
		GFX_icon_example_1 = {
			# Display conditions
		}
		GFX_icon_example_2 = yes
	}

	# Title bar style
	text_icon = my_titlebar_style
	style = {
		name = my_titlebar_style
		unavailable = GFX_title_unavailable
		available = GFX_title_available
		completed = GFX_title_completed
		current = GFX_title_current
	}

	x=5
	y = 0
	offset = {
		x = -5
		trigger={}
	}

	relative_position_id = GER_other_focus

	prerequisite = { focus = GER_parent_1 focus = GER_parent_2 }
	prerequisite = { focus = GER_parent_3 }
	mutually_exclusive = { focus = GER_exclusive }

	cost = 10
	ai_will_do = {
		base=1
		modifier = {
			add=5
			factor = 2
			# Condition
		}
	}

	available = { }
	allow_branch = { }
	select_effect = { }
	bypass = { }
	cancel = { }

	available_if_capitulated = yes
	cancelable=yes
	bypass_if_unavailable = no
	cancel_if_invalid = yes
	continue_if_invalid = no
will_lead_to_war_with = SOV
	historical_ai = { }

	search_filters = { FOCUS_FILTER_MANPOWER }

	completion_reward = {
		mark_focus_tree_layout_dirty = yes
		# Effect
	}
}
```

## Shared national focus (shared_focus)

File location: `common/national_focus/<filename>.txt`

```pdx
shared_focus = {
	id = GER_shared_focus_1
	icon = GFX_shared_icon
	relative_position_id = GER_base_focus

	x = 0
	y=1

	prerequisite = { focus = GER_base_focus }
	cost = 10

	completion_reward = {
		# Effect
	}
}
```

Quoted in `focus_tree`:

```pdx
focus_tree = {
	id = GER_tree
	shared_focus = GER_shared_focus_1
	#...
}
```

## United Nations Policy (joint_focus)

```pdx
joint_focus = {
	id = GER_joint_focus_1
	icon = GFX_joint_icon
	relative_position_id = GER_base_focus

	x = 0
	y=1
	cost = 10

	joint_trigger = {
		# Determine the initiator
	}

	completion_reward = {
		# Shared by initiators and members
	}
	completion_reward_joint_originator = {
		# The initiator only enjoys
	}
	completion_reward_joint_member = {
		# Other members enjoy
	}
}
```
## Sustainability National Policy

File location: `common/continuous_focus/<filename>.txt`

```pdx
continuous_focus_palette = {
	id = BHR_focus_palette
	country = {
		factor=0
		modifier = {
			tag=BHR
			add=10
		}
	}
	position = { x = 50 y = 1000 }

	focus = {
		id = BHR_continuous_1
		icon = GFX_continuous_icon
		daily_cost = 0.1

		available = { }
		enable = { }
		select_effect = { }
		cancel_effect = { }

		available_if_capitulated = yes
		search_filters = { FOCUS_FILTER_MANPOWER }

		modifier = {
			# Continuous corrections
		}
	}
}
```

## National focus GUI (inlay_window)

Definition file: `common/focus_inlay_windows/<file name>.txt`

```pdx
my_inlay_window = {
	window_name = gui_component_name
	internal=yes
	visible = { }

	scripted_buttons = {
		my_button = {
			available = { }
		}
		click_effect = { }
	}

	scripted_images = {
		my_icon = {
			GFX_icon_1 = { }
			GFX_icon_2 = yes
		}
	}
scripted_progressbars = {
		my_bar = {
			progress = my_variable
		}
	}
}
```

In `focus_tree`:

```pdx
focus_tree = {
	id = GER_tree
	inlay_window = {
		id = my_inlay_window
		position = { x = 1 y = 20 }
	}
}
```

## Common field descriptions

### focus_tree field

| Field | Description |
|------|------|
| `id` | National focus tree ID |
| `country` | Applicable countries and weights |
| `default` | Whether it is a general national focus |
| `Reset_on_civilwarno` | Whether to reset during civil war |
| `shared_focus` | Quote shared national focus |
| `initial_show_position` | Camera position after entering the national focus tree |
| `shortcut` | Lower left corner navigation button |
| `inlay_window` | National focus GUI window position |
| `continuous_focus_position` | Continuous national focus position |

### focus field

| Field | Description |
|------|------|
| `id` | Unique identifier of national focus |
| `icon` | icon name |
| `dynamic` | Whether the icon is dynamic |
| `text_icon` / `style` | Title bar style |
| `x` / `y` | Coordinates |
| `offset` | Dynamic offset |
| `relative_position_id` | Relative positioning national focus |
| `prerequisite` | Prerequisite national focus |
| `mutually_exclusive` | Mutually exclusive focus |
| `cost` | National focus cost, 1 = 7 days |
| `ai_will_do` | AI priority |
| `available` | Clickable conditions |
| `allow_branch` | Branch display conditions |
| `select_effect` | Effect when clicked |
| `bypass` | Skip condition |
| `cancel` | Cancellation conditions |
| `historical_ai` | Historical AI error prevention |
| `available_if_capitulated` | Whether it can be clicked after surrendering |
| `cancelable` | Can it be canceled |
| `bypass_if_unavailable` | Whether to skip when unavailable |
| `cancel_if_invalid` | Whether to cancel when illegal |
| `continue_if_invalid` | Whether to continue if it is illegal |
| `will_lead_to_war_with` | War target prompt |
| `search_filters` | Filter tag |
| `completion_reward` | Completion reward |
| `mark_focus_tree_layout_dirty` | Refresh the national focus tree |
### Shared/United Policy Fields

| Field | Description |
|------|------|
| `joint_trigger` | United Nations trigger conditions |
| `completion_reward_joint_originator` | Initiator exclusive reward |
| `completion_reward_joint_member` | Member exclusive rewards |

### Continuous national focus field

| Field | Description |
|------|------|
| `daily_cost` | Daily political point cost |
| `enable` | Enable conditions |
| `cancel_effect` | Cancel effect |
| `modifier` | Continuous modifier |
