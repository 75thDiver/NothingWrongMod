# Defines template

Lua tables under `common/defines/` override engine numerical constants (date, diplomacy, combat, AI, etc.). **Correction of one error may cause the whole system to collapse**, the total conversion will be greatly changed; the content mod should be touched as little as possible.

## File

| File | Function |
|------|------|
| `00_defines.lua` | Primary value (`NDefines.NGame`, etc.) |
| `00_graphics.lua` | Graphics related definitions |
| `01_career_profile.lua` | Career/File category (if any) |

Usually only the keys that need to be covered are placed in the mod, and the structure is consistent with the vanilla:

```lua
NDefines = {
	NGame = {
		START_DATE = "1936.1.1.12",
		END_DATE = "1949.1.1.1",
	},
	NDiplomacy = {
		-- Write only the keys to be changed
	},
}
```

The actual merge rules are subject to the current version; check the complete file of the ontology before writing.

## Common namespaces (excerpt)

- `NGame`: start/end date, event timeout, resource name mapping, etc.
- `NDiplomacy`: diplomatic trust, request expiration, etc.
- `NCountry`: country layer value
- `NMilitary` / `NAir` / `NNavy`: Combat and Service
- `NPolitics`: Politics
- `NFocus`: national focus
- `NAI`: AI
- `NGraphics` / `NMapMode`, etc.: graphics and maps (partly in the graphics file)

The complete key name is subject to the ontology `00_defines.lua` and the library classification translation.

## Content mod Examples of relatively safe changes

- Extend `END_DATE` (modern/alternative timeline)
- Adjust `EVENT_TIMEOUT_DEFAULT` (requires design consent)
- Camera/graphics small parameters (`00_graphics.lua`, still needs to be tested)
## High risk

- Global formulas for battle width, organization, and supply
- AI large coefficient
- `SAVE_VERSION` and other archive identifiers (do not change them randomly)
- `MAX_EFFECT_ITERATION` and other upper limits (can cover bugs or infinite loops)

## Specification

- Only change a few keys at a time and enter the game one by one to verify
- Comments indicate why the change was made and what the original value was.
- Do not copy the entire 00_defines into the mod unless the total conversion is necessary (difficult to merge, difficult to upgrade)
- diff official defines (`version-migration-template.md`) during version migration

## Related

- `mod-structure-template.md` / `version-migration-template.md` / `debug-workflow-template.md`
