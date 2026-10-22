#Bookmarks template

File location: `common/bookmarks/<xxx>.txt`
Vanillas: `the_gathering_storm.txt` (1936), `blitzkrieg.txt` (1939).

## Infrastructure

```pdx
bookmarks = {
	bookmark = {
		name = MY_BOOKMARK_NAME
		desc = MY_BOOKMARK_DESC
		date = 1936.1.1.12
		picture = "GFX_select_date_1936"
		default_country = "GER"
		default=yes

		filters = { new_content continent }

		GER = {
			history = GER_MY_BOOKMARK_DESC
			ideology=fascism
			version = base_game
			ideas = {
				GER_idea_1
				GER_idea_2
				GER_idea_3
			}
			focuses = {
				GER_focus_a
				GER_focus_b
				GER_focus_c
			}
		}

		"---" = {
			history = OTHER_MY_BOOKMARK_DESC
		}

		"HUN" = {
			minor=yes
			history = HUN_MY_BOOKMARK_DESC
			ideology = neutrality
			ideas = { }
			focuses = { }
		}

		effect = {
			randomize_weather = 22345
		}
	}
}
```
## Field description

| Field | Description |
|------|------|
| `name` / `desc` | Script title/description localization key |
| `date` | Start time `year.month.day.hour`, cannot be earlier than the engine lower limit |
| `picture` | Scenario selection interface picture (GFX registration required) |
| `default_country` | Interesting country tags selected by default |
| `default` | Whether to use the default script |
| `filters` | Filter/sort tags |
| `TAG = { }` | Major country (big flag); none `minor = yes` |
| `minor = yes` | Minor country (small flag below) |
| `"---"` | "Other countries" empty slot |
| `history` | Introduction key displayed when selecting country |
| `ideology` | Group for displaying the ideology of the ruling party |
| `ideas` / `focuses` | For display purposes, about 3 items each by default; **Does not change the actual opening** |
| `available` / `required_dlc` | Display conditions (mostly used for DLC) |
| `version` | Content tag, such as `base_game` |
| `override_leader_portrait` | Override the avatar in the selection interface GFX |
| `effect` | The effect when the script is selected; the vanilla contains `randomize_weather` |

## Interesting Country

- When defined in a bookmark and the national focus tree is not the default tree, it is usually regarded as an "interesting country"
- Major countries will be displayed in the big card above

## Localization

```yaml
  MY_BOOKMARK_NAME: "My Script"
  MY_BOOKMARK_DESC: "Summary of the script."
  GER_MY_BOOKMARK_DESC: "Introduction to Germany's opening."
```

## Specification

- Display `ideas`/`focuses` must be a real id
- The real starting status is written in `history/countries`, don’t just change the bookmark
- New script image `gfx-registration-template.md`
## Related

- `new-country-template.md` / `gfx-registration-template.md` / `localisation-syntax-template.md`
