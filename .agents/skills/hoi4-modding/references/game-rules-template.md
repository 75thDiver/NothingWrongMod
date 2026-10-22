# Game Rules template

File: `common/game_rules/00_game_rules.txt`
"Game Rules" menu before starting; commonly used for AI routes, historical/non-historical facts, allowing declaration of war, etc.

## Structure

```pdx
TAG_ai_behavior = {
	name = "TAG_AI_BEHAVIOR"
	group = "RULE_GROUP_OTHER_OPTIONS"
	icon = "GFX_decision_generic"
	required_dlc = "Some DLC" # optional

	option = {
		name = DEFAULT
		text = "TAG_AI_DEFAULT"
		desc = "TAG_AI_DEFAULT_DESC"
		# allow_achievements = yes/no
	}
	default = {
		name = HISTORICAL
		text = "TAG_AI_HISTORICAL"
		desc = "TAG_AI_HISTORICAL_DESC"
	}
	option = {
		name = ALTERNATE
		text = "TAG_AI_ALTERNATE"
		desc = "TAG_AI_ALTERNATE_DESC"
		allow_achievements = no
	}
}
```

| Field | Description |
|------|------|
| `name` / `desc` | Rule title localization |
| `group` | Group filtering |
| `option` / `default` | Options; `default` can override "the first item is the default" |
| `allow_achievements` | Whether this option allows achievements |
| `required_dlc` | DLC latch |

## Read in script

```pdx
has_game_rule = {
	rule = TAG_ai_behavior
	option = HISTORICAL
}
```

Often used in conjunction with `enable` of `ai_strategy_plans` (`ai-template.md`).

## Specification

- option token uses stable uppercase name
-Non-default options will always enable achievements by default, please confirm before release
- Don’t insert key gameplay logic without writing desc

## Related

- `ai-template.md` / `bookmarks-template.md` / `localisation-syntax-template.md`
