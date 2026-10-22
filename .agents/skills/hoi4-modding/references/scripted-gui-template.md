# Scripted GUI template

Use scripts to drive custom interfaces: resolution category inline UI, player full screen window, super event container, etc. The complete control syntax is subject to wiki **Scripted GUI** / **Interface** and ontology `interface/*.gui`.

## Involved files

| path | function |
|------|------|
| `common/scripted_guis/<xxx>.txt` | Visibility, button effects, dynamic graphics/text |
| `interface/<xxx>.gui` | Window and control layout |
| `interface/<xxx>.gfx` | Control texture registration |
| `localisation/` | text |
| `common/scripted_localisation/` | Dynamic title/image key (optional) |

## scripted_gui structure

```pdx
scripted_gui = {
	TAG_my_ui = {
		context_type = decision_category # or player_context etc.
		window_name = "TAG_my_ui_window"

		visible = {
			tag=TAG
			has_country_flag = TAG_show_ui
		}

		triggers = {
			TAG_my_button_click_enabled = {
				has_political_power > 50
			}
			TAG_my_icon_visible = {
				has_country_flag = TAG_icon_on
			}
		}

		effects = {
			TAG_my_button_click = {
				add_political_power = -50
				set_country_flag = TAG_clicked
			}
		}
properties = {
			TAG_my_dynamic_icon = {
				image = "[GET_TAG_ICON]"
			}
		}
	}
}
```

### context_type (common)

| Value | Meaning |
|----|------|
| `player_context` | Player country context; can be used as a permanent/full-screen layer |
| `decision_category` | Hang on a certain decision category (`scripted_gui = TAG_my_ui` in the category) |
| Others | Subject to wiki/vanilla (national diplomatic window, etc.) |

### Naming Convention

- `window_name` must correspond to `containerWindowType` / window name in `.gui`
- `triggers` / `effects` key name = **control name + suffix**
  - Click: `<buttonName>_click`
  - Whether it can be clicked: `<buttonName>_click_enabled`
  - Whether it is visible: `<widgetName>_visible`
- `properties` can change dynamic properties such as `image` and `frame`

## .gui concept (minimalist)

```gui
guiTypes = {
	containerWindowType = {
		name = "TAG_my_ui_window"
		position = { x = 0 y = 0 }
		size = { width = 600 height = 400 }
		Orientation = center

		instantTextBoxType = {
			name = "TAG_my_title"
			position = { x = 20 y = 20 }
			font = "hoi_18mbs"
			text = "TAG_MY_UI_TITLE"
		}
buttonType = {
			name = "TAG_my_button"
			position = { x = 20 y = 350 }
			spriteType = "GFX_TAG_btn"
			buttonText = "TAG_MY_UI_OK"
		}
	}
}
```

- The control `name` is consistent with the triggers/effects prefix of scripted_gui
- `Orientation`: `UPPER_LEFT` / `CENTER` / `LOWER_RIGHT` etc.
- The font name must be registered with fonts gfx

## Debugging sequence

1. Whether the window is `visible`
2. Is `window_name` spelled correctly?
3. Is the button name consistent with `_click`?
4. `.gfx` pink picture
5. Error reported by scripted gui in `error.log`

## Specification

- First copy the original small UI (such as a certain DLC decision_category GUI) and then expand it
- For interfaces that AI does not need to see, add `is_ai = no`
- Add logic to `scripted_effects`, and the button only adjusts `TAG_do_thing = yes`
- For super events, see `super-event-template.md`

## Related

- `gfx-registration-template.md` / `scripted-triggers-template.md` / `scripted-effects-template.md` / `decision-template.md` / `localisation-syntax-template.md`
