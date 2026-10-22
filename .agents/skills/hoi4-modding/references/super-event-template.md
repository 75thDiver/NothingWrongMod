# Super Event template

"Super event" is not an engine keyword, but a community mode: **Big picture UI + script localization + optional music + on/off with variables**.
It is recommended to directly modify it based on the "Super Event Template" of Shuangze Library instead of inventing it from scratch.

## Component list

| Module | Typical path |
|------|----------|
| Display container | `common/scripted_guis/` |
| Open/Clean | `common/scripted_effects/` |
| Picture/title/text/button dynamic key | `common/scripted_localisation/` |
| Layout and textures | `interface/*.gui` + `interface/*.gfx` |
| Large image resources | `gfx/...` |
| Test events | `events/` |
| Music | `music/` + `.asset` + track list |
| Localization | `localisation/` |

## Core mechanism (common implementation)

1. Set a global variable as the serial number: `set_variable = { global.se_display = 1 }`
2. `visible` of `scripted_gui` checks `has_variable = global.se_display` and `is_ai = no`
3. `scripted_localisation` press `check_variable = { global.se_display = 1 }` to return different images and text keys
4. Close the button: `clear_variable = global.se_display`, and clear the centered flag
5. Optional: `play_song = my_se_song_1`

```pdx
# Open (national focus/event/decision effect)
set_variable = { global.se_display = 1 }
play_song = TAG_se_song_1
# Close (GUI button effects)
clear_variable = global.se_display
clr_global_flag = TAG_se_center
```

## scripted_gui indication

```pdx
scripted_gui = {
	TAG_SE_main = {
		window_name = TAG_SE_main
		context_type = player_context
		visible = {
			has_variable = global.se_display
			is_ai = no
		}
		effects = {
			TAG_SE_exit_btn_click = {
				clear_variable = global.se_display
			}
		}
		properties = {
			TAG_SE_picture = {
				image = "[TAG_SE_getpicture]"
			}
		}
	}
}
```

## scripted_localisation indication

```pdx
defined_text = {
	name = TAG_SE_getpicture
	text = {
		trigger = { check_variable = { global.se_display = 1 } }
		localization_key = "GFX_TAG_SE_1"
	}
	text = {
		trigger = { check_variable = { global.se_display = 2 } }
		localization_key = "GFX_TAG_SE_2"
	}
}
```

Title/description/introduction/button are divided into files or `defined_text` in the same way.
## Resources and Music

- One large picture for each super event, registered as `GFX_TAG_SE_1` etc. in `.gfx`
- Music: see `music-radio-template.md`; tracks should be limited to super-event scenes to avoid contaminating the normal playlist (the template commonly used independent songs list)

## Negative lessons (summary from community templates)

- Localized file header/`l_xxx:` and encoding errors will cause large-scale exceptions
- Without `clear_variable` after opening, the UI will freeze.
- AI visibility is meaningless and may slow down performance → `is_ai = no`
- If the serial number is inconsistent with loc/GFX, the image will be pink/blank

## Workflow suggestions

1. Copy the entire package of library hyperevent templates to the standalone test mod
2. Only change the pictures, text, and songs of Event No. 1, and verify the switch.
3. Receive formal national focuses/events again
4. Do not lay numbers on a large area of the main project before the design is finalized.

## Related

- `scripted-gui-template.md` / `scripted-effects-template.md` / `scripted-triggers-template.md` / `music-radio-template.md` / `gfx-registration-template.md`
