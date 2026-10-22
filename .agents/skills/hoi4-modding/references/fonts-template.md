# Font template

## Location

| path | function |
|------|------|
| `gfx/fonts/` | Font texture/glyph resources (such as `.fnt` + dds) |
| `interface/*fonts*.gfx` / `core_chinese.gfx` etc. | `bitmapfonts` registration |

## Registration concept

```pdx
bitmapfonts = {
	bitmapfont = {
		name = "hoi_18mbs"
		path = "gfx/fonts/..."
		# color / fontfiles etc. are subject to the vanilla.
	}
}
```

The `.gui` text control refers to the **registered name** via `font = "hoi_18mbs"`.

## Chinese

- The original Chinese version relies on `core_chinese.gfx` and other configurations
- Self-made fonts must cover the complete range of Chinese characters, otherwise there will be missing characters
- Back up the font before changing it; incorrect registration may cause the UI to be completely empty or crash.

## Production process (entry)

1. Follow the library's "How to Make a HOI4 Font" to generate the glyph map and fnt
2. Put into `gfx/fonts/`
3. Register bitmapfont in the `interface` of the mod
4. Change `font =` in the target `.gui`
5. Test main menu, events, map fonts

## Specification

- Content mods should use original font names as much as possible
- Add custom fonts only when the UI project requires unified vision
- Follow the tutorials for coding and tool chains, and do not modify binary fonts by hand without backing them up.

## Related

- `scripted-gui-template.md` / `gfx-registration-template.md` / `localisation-syntax-template.md`
