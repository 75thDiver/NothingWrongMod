# Create a new national full process template

The smallest closed loop from tag to playable country. Missing any step will result in a gray name, no flags, no history, or crash.

## List

1. `common/country_tags/<xxx>.txt` Register TAG
2. `common/countries/<Country Name>.txt` color and graphical_culture
3. `history/countries/TAG - <Country Name>.txt` opening script
4. `history/states/` owns/core land (or land given by event/national focus)
5. Localization: country name, adjectives, country introduction, etc.
6. Flag `gfx/flags/` (and small and medium size if needed)
7. (Optional) National focus tree, characters, OOB, idea, cosmetic tag
8. (Optional) `bookmarks` make interesting countries

## 1. country_tags

`common/country_tags/00_countries.txt` or standalone file:

```pdx
RYH = "countries/russiaYH.txt"
```

- Left: 3 letters TAG (conventionally capitalized)
- Right: File name under `common/countries/`

## 2. common/countries

`common/countries/russiaYH.txt`：

```pdx
graphical_culture = eastern_european_gfx
graphical_culture_2d = eastern_european_2d

color={80 100 120}
```

`color` is the map color RGB. The culture key must exist in the original graphical culture definition.

## 3. history/countries

File name: `TAG - <name corresponding to countries file name>.txt`
See `country-history-template.md` for details.
Minimum:

```pdx
capital=219
set_research_slots = 3
set_technology = {
	infantry_weapons = 1
}
set_politics = {
	ruling_party = neutrality
	last_election = "1936.1.1"
	election_frequency = 48
	elections_allowed = no
}
set_popularities = {
	neutrality=100
}
recruit_character = RYH_leader
```

## 4. Lot

- Exists at the beginning: change `owner` / `add_core_of` of `history/states/<id>-xxx.txt`
- Appeared later: events/national focuses `transfer_state`, `set_state_owner`, `add_state_core`
- Total conversion often `replace_path="history/states"`

For how to write state, see `state-template.md`. Comments use localized state names (`modding-rules.md`).

## 5. Localization

```yaml
  RYH: "Russian Parliament"
  RYH_DEF: "Russian Parliament"
  RYH_ADJ: "Parliamentary Russia"
  RYH_neutrality: "Russian Parliament"
  RYH_neutrality_DEF: "Russian Parliament"
  #Complete the country names of each ideology according to the existing key style of the project
```

Also check if `state_names` and victory roll require new keys.

## 6. Flag

Path convention (subject to the vanilla):

```
gfx/flags/RYH.tga
gfx/flags/medium/RYH.tga
gfx/flags/small/RYH.tga
```
- The format/size is the same as the original flag (common TGA)
- Ideological variants: `RYH_fascism.tga` etc. (if used)
- See `gfx-registration-template.md` for details

## 7. Characters and national focuses

- Character: `common/characters/RYH.txt` + history `recruit_character` (`character-template.md`)
- National focus: `common/national_focus/RYH.txt` and `default = no` tree binding tag (`focus-template.md`)
- OOB: `history/units` + `oob =` in history (`oob-template.md`)

## 8. Cosmetic tag (optional)

Used for "same TAG reskin country name/flag":

```pdx
set_cosmetic_tag = RYH_provisional
drop_cosmetic_tag = yes
```

Requires corresponding localization and optional flag resources.

## 9. Bookmarks (optional)

See `bookmarks-template.md` to write RYH as primary or secondary country.

## Dependencies and replacements

- If you depend on total conversion: `.mod` write `dependencies` (`mod-structure-template.md`)
- Large-scale history change: use `replace_path` with caution
- Specifications for this project: **Do not write compatible code**

## Verify

1. Does the country selection interface have a name, flag, and color?
2. Whether there is a capital, technology, and politics at the start
3. Is there missing country / missing flag / invalid state in `error.log`

## Related

- `country-history-template.md` / `state-template.md` / `character-template.md` / `focus-template.md` / `gfx-registration-template.md` / `mod-structure-template.md`
