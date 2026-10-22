#Event template

## File location

`events/<xxx>.txt`

## Event file ownership rules

The event file is subject to the **initiator**. Even if the target or recipient of the event is another country, the initiator should write its own event file and use a separate event namespace.

- ✅ RYH initiates a destruction event on POA, which is written in `events/RYH_events.txt` and the namespace is `POA_sabotage`.
- ❌ Do not write events initiated by RYH to `events/POA_events.txt`.

## Namespace rules

- Namespaces should be prefixed with event IDs, not country tags.
- ✅ `add_namespace = POA_sabotage`, event ID is `POA_sabotage.1`.
- ❌ `add_namespace = POA` (POA is the country tag, not the event prefix).

## Ordinary national events

```pdx
add_namespace = my_event_prefix

country_event = {
	id = my_event_prefix.1
	picture = GFX_<event picture name>
	title = my_event_prefix.1.t
	desc = my_event_prefix.1.d

	# Choose one between trigger and is_triggered_only
	is_triggered_only = yes
	# or
	trigger = {
		# Automatically trigger when conditions are met
	}

	# Usually trigger is paired with fire_only_once = yes
	fire_only_once = yes

	hidden=no

	immediate = {
		# Effect that takes effect immediately when the event is triggered
	}

	option = {
		name = my_event_prefix.1.a
		trigger = {
			# Conditions for this option to appear
		}
		# Option effects
	}
option = {
		name = my_event_prefix.1.b
		# Option effects
	}
}
```

## News events

```pdx
news_event = {
	id = my_event_prefix.100
	picture = GFX_<event picture name>
	title = my_event_prefix.100.t
	desc = my_event_prefix.100.d

	is_triggered_only = yes

	major = yes # yes is displayed for the whole world, no is only for this country

	option = {
		name = my_event_prefix.100.a
	}
}
```

## Common field descriptions

| Field | Description |
|------|------|
| `add_namespace` | Event namespace |
| `id` | Unique identifier of the event, format `prefix.number` |
| `picture` | Event pictures |
| `title` | Title localization key |
| `desc` | Describes the localization key |
| `is_triggered_only` | Can only be called out by scripts/national focuses/decisions, and will not be triggered automatically |
| `trigger` | Automatic trigger condition; choose one from `is_triggered_only` |
| `fire_only_once` | Whether to trigger only once |
| `hidden` | Whether it is a hidden event |
| `immediate` | The effect of executing immediately when the event pops up |
| `option` | Event options, `name` is the option localization key |
| `major` | Whether news events are visible to the world |

## Localization

`title` and `desc` require the actual text to be written in the localization file:

```yaml
  my_event_prefix.1.t: "Event title"
  my_event_prefix.1.d: "Event description."
  my_event_prefix.1.a: "Option A"
  my_event_prefix.1.b: "Option B"
```
