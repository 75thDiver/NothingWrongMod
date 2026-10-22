#Technology file structure template

Technology **ID list** see `data/tech-list.md`. This page describes how to write the `common/technologies/` file.

## File location

```
common/technologies/
  infantry.txt
  armor.txt
  artillery.txt
  air_techs.txt
  ...
```

## Infrastructure

```pdx
technologies = {
	@1936 = 2
	@1938 = 4
	@1939 = 6
	@1940 = 8
	@1941 = 10
	@1942 = 12

	TAG_improved_widget = {
		enable_equipments = {
			tag_widget_equipment_1
		}

		enable_equipment_modules = {
			# module token
		}

		enable_subunits = {
			# arms
		}

		path = {
			leads_to_tech = TAG_advanced_widget
			research_cost_coeff = 1
		}

		research_cost = 1.5
		start_year = 1938

		folder = {
			name = infantry_folder
			position = { x = 0 y = @1938 }
		}

		categories = {
			infantry_weapons
		}

		ai_will_do = {
			factor = 1
		}

		xor = { TAG_other_branch }
		allow = {
			# Research conditions
		}
		on_research_complete = {
			# Optional effects
		}
	}
}
```
## Key fields

| Field | Description |
|------|------|
| `enable_equipments` | Unlock equipment |
| `enable_equipment_modules` | Unlock modules |
| `enable_subunits` | Unlock establishment units |
| `path` | Follow-up technology |
| `research_cost` | Research cost coefficient |
| `start_year` | Year (related to early research penalty) |
| `folder` | Technology tree tabs and coordinates |
| `position` | x/y in the tree; `y` commonly used `@1936` macro |
| `categories` | Bonus cards/filter categories |
| `xor` | Mutually exclusive technology |
| `allow` | Allow research triggers |
| `ai_will_do` | AI weight |
| `on_research_complete` | Effect on completion |
| `show_equipment_icon` etc. | The vanilla shall prevail |

The top `@1936 = 2` category is the **position macro**, used by `position = { y = @1936 }`.

## folders and categories

- `folder.name` must be a defined technology page (original `infantry_folder`, `armour_folder`, etc.)
- Customizing folders requires a complete set of interface/GFX/folder definitions, which is difficult; content mods give priority to the original folders
- `categories` corresponds to `add_tech_bonus = { category = ... }` (see effects / library prompts)

## Grant technology at the start

`history/countries`:

```pdx
set_technology = {
	infantry_weapons = 1
	infantry_weapons1 = 1
}
```
A value of `1` means researched.

## Research bonus

```pdx
add_tech_bonus = {
	name = infantry_weapons_bonus
	bonus = 0.5
	uses=1
	category = infantry_weapons
	# or technology = infantry_weapons1
	# ahead_reduction = 1
}
```

## With equipment and units

Technology is only responsible for unlocking; equipment is defined in `common/units/equipment/`, units are in `common/units/`, and modules are in `equipment/modules/`.
New technology chain sequence: equipment/unit definition → technology enable → localization → GFX icon.

## Localization

```yaml
  TAG_improved_widget: "Improved widget"
  TAG_improved_widget_desc: "Description."
```

## Specification

- New technology IDs are prefixed with TAG to avoid conflicts
- The coordinates should not overlap with the original icon so that it cannot be clicked.
- Use `xor` for mutual exclusion, and write clear AI
- The complete folding/doctrine tab mechanism is subject to the ontology and wiki **Technology**

## Related

- `data/tech-list.md` / `equipment-template.md` / `unit-template.md` / `effects-template.md`



## Technology Sharing



For camp/organization research sharing groups, see `technology-sharing-template.md`.
