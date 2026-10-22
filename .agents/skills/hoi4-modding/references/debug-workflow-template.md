# Debugging and error.log workflow

## Log location

```
Documents/Paradox Interactive/Hearts of Iron IV/logs/error.log
Documents/Paradox Interactive/Hearts of Iron IV/logs/game.log
Documents/Paradox Interactive/Hearts of Iron IV/logs/system.log
```

After modifying the script: **Restart or reload to the steps that can be reproduced → Read the error.log first**.

## Startup parameters / console (commonly used)

- Debug related parameters can be added to the startup item (subject to the current version of wiki)
- Common in-game consoles (` key): `tag`, `event`, `research_on_icon`, `tdebug`, `annex`, `observe`
- The specific command list will change with the version, check wiki **Console commands**, no inferences are allowed.

## Checking order

1. **Grammar fans**: Recently changed txt brackets/quotes
2. **error.log first error**: constant chaining, repair the earliest line first
3. **Location file**: unknown token / missing file path
4. **scope**: whether the effect is applied to the country or state (`scopes-template.md`)
5. **Localization**: Display key name if key is missing; encoding BOM (`localisation-syntax-template.md`)
6. **GFX**: Pink picture check `.gfx` and path
7. **GUI**: visible / window_name / button suffix
8. **Version**: expired modifier/field (`version-migration-template.md`)
## Common error types

| Symptoms | Directions |
|------|------|
| Unexpected token | Brackets, key names, misplaced blocks |
| Unknown effect/trigger/modifier | Key name error or version change |
| Invalid node / missing file | Path, replace_path cleared too much |
| National focus is not displayed | `allow`/`available`, shared tree, tag binding |
| The event is not triggered | `is_triggered_only`, namespace, target country |
| Select country pink flag | flags file name/size |
| Crash at start | history syntax, replace empty directory, map mismatch |

## Dichotomy

- Disable half of new file positioning
- Create a minimal test mod that only leaves suspect systems
- Do not change the economy + map + GUI at once before testing

## Tools

- Library: Error log analysis tool, folder comparator
- Version management: For diff, avoid "mysteriously changing one more line"

## Specification

- Refactoring is not easy when fixing bugs
- Write down the reasons after the repair is completed; do not leave the temporary debug effect (plus PP) in the release version
- If the design is unclear, ask the user first, and do not change the gameplay without authorization to "fix it"

## Related

- `mod-structure-template.md` / `modding-rules.md` / Templates for each system
