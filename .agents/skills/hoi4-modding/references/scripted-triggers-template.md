> Used to organize reuse conditions and dynamic text.

# Script conditions and script localization templates

## scripted_triggers

File location: `common/scripted_triggers/<xxx>.txt`

Used to organize reused conditional presets.

### Definition

```pdx
my_condition = {
	has_country_flag = my_flag
	has_war=no
}
```

### Use

```pdx
GER = {
	if = {
		limit = {
			my_condition = yes # satisfies the condition
		}
		set_country_flag = boluo
	}
}
```

```pdx
if = {
	limit = {
		my_condition = no # The condition is not met
	}
	#...
}
```

## scripted_localisation

File location: `common/scripted_localisation/<xxx>.txt`

Used to dynamically display different text based on conditions.

### Definition

```pdx
defined_text = {
	name = GER_GUI

	text = {
		trigger = {
			has_country_flag = AOR_GER_gui
		}
		localization_key = AOR_GER_SP_LOC_1
	}

	text = {
		trigger = {
			has_country_flag = AOR_GER_not_gui
		}
		localization_key = AOR_GER_SP_LOC_2
	}
}
```

### Localized call

```yaml
GER:0 "[GER_GUI]"
AOR_GER_SP_LOC_1:0 "entry 1"
AOR_GER_SP_LOC_2:0 "entry 2"
```
### Example

```pdx
defined_text = {
	name = dynamic_news_title

	text = {
		trigger = { tag = GER }
		localization_key = news_title_ger
	}

	text = {
		trigger = { tag = SOV }
		localization_key = news_title_sov
	}
}
```

```yaml
  news_title_ger:0 "German Perspective Title"
  news_title_sov:0 "Soviet Perspective Title"
```

## Common field descriptions

| Field | Description |
|------|------|
| `scripted_trigger` | Conditional preset, when used `name = yes/no` |
| `defined_text` | Dynamic localization definition |
| `name` | script ID |
| `trigger` | The condition to display this text |
| `localization_key` | Corresponding localization key |
