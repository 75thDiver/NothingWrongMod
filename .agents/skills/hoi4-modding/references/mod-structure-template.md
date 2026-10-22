# Mod structure and loading rules

`.mod` / `descriptor.mod` / load order / `dependencies` / `replace_path` specification.

## File location

| File | Function |
|------|------|
| `Documents/.../mod/<Name>.mod` | User-side description read by the launcher; includes `path=` |
| `<mod folder>/descriptor.mod` | Mod package description; this shall prevail when uploading to the Steam Workshop |
| `<mod folder>/` | Actual content root directory |

The fields on both sides should be as consistent as possible. `replace_path`, `dependencies`, `supported_version`, `tags` **must be written on both sides**, otherwise it may not take effect or be overwritten by the launcher.

## descriptor / .mod field

```pdx
name="MyWorkProject"
version="1"
supported_version="1.19.*"
path="D:/Documents/Paradox Interactive/Hearts of Iron IV/mod/MyWorkProject" # Only required for user-side .mod
picture="Thumbnail.png"
tags={
	"Alternative History"
	"Events"
}
dependencies={
	"Testmod" # The name of the dependent mod (name field), not the folder name
}
replace_path="history/countries"
replace_path="history/states"
```

| Field | Description |
|------|------|
| `name` | Launcher display name; `dependencies` also refers to this name |
| `version` | The module's own version string |
| `supported_version` | Game version, available `1.19.*` |
| `path` | User directory only `.mod`; points to the mod folder |
| `picture` | Thumbnail, relative to the mod root directory |
| `tags` | Creative workshop classification tags |
| `dependencies` | Mods that must be loaded **before** loading this mod |
| `replace_path` | When this mod is loaded, the previously loaded content in this path will be cleared |
| `remote_file_id` | Creative workshop ID (automatic/manual after uploading) |
## Loading order

1. Original + DLC
2. User directory coverage (if any)
3. Enabled mods, according to the launcher list **from top to bottom** (first loaded first)
4. `dependencies` ensures that the dependent mod is ranked before the dependent ones

**File with the same name**: loaded last overrides loaded first.
**Files with different names**: usually coexist (there can be multiple `.txt` in the same directory).

## replace_path

### Semantics

At the moment when this mod is loaded, unload all files that have been loaded under the relative path.

- Will clear: the vanilla, DLC, user directory, and the contents of the mod in this path that are ranked in front of this mod.
- **doesn't** change the overall loading order
- **will not** prevent **later** mods from loading files with the same path
- Different from "overwrite with the same name": replace clears the entire directory level, solving the problem of "the vanilla must also be removed with different file names"

### Loading order example

Activation order **A → B → C** (A is the earliest, C is the latest), both A and C have written `replace_path="common"`:

1. Vanilla loaded common
2. A loads → replace → only A remains
3. B loads (without replace) → A + B
4. C loads → replace → removes A and B → **only C** remains

If only A replaces, B/C does not replace: final = A + B + C (the latter shall prevail if the same name is used).

### Limitations

- Only works on files directly under the path**, **does not recurse into subdirectories**
- Most effective for directories indexed in the main menu stage; `history/units`, part of `gfx/flags` and other paths loaded by reference have weak or invalid effects
- Empty directory replace may cause missing files to crash (national focus, scripted trigger, etc.)
- Must be declared in both user `.mod` and `descriptor.mod`
### Common replace target (total conversion)

```pdx
replace_path="history/countries"
replace_path="history/states"
replace_path="history/units"
replace_path="history/general"
replace_path="common/national_focus"
replace_path="common/ideas"
replace_path="events"
replace_path="gfx/loadingscreens"
```

Content patch modules usually don't replace large directories easily, giving priority to overwriting or new files with the same name.

## dependencies compatible with

- The name in `dependencies={ "XX Mod" }` must be equal to the other party `name=`
- Dependency only guarantees the order, but does not guarantee the stability of the other party's API.
- Specifications for this project: **Do not write compatible code**; when dependencies are required, declare them in `.mod`, and write the logic according to the existing content of the dependent mod

## Directory habits

```
MyMod/
  descriptor.mod
  common/
  events/
  history/
  localisation/
    simp_chinese/
  gfx/
  interface/
  music/ # optional
```

The localized language directory name must be consistent with the game (such as `simp_chinese`, `english`).

## Checklist

1. Whether the launcher is enabled and the order is correct
2. Whether `path` points to a real folder (forward slashes are available)
3. Whether `supported_version` matches the current game
4. Did `replace_path` accidentally clear the original/pre-mod that is still needed?
5. Is there missing file / unknown token in `error.log` (`Documents/.../logs/error.log`)
## Query order (when not sure)

1. This SKILL references
2. Similar files to the current mod
3. HOI4 body and pre-mod enabled
4. Official wiki: `Mod structure` / `Modding`
5. If still unsure, ask the user
