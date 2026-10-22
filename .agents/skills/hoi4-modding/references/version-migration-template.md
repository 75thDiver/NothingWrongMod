# Version adaptation and migration note template

Module `supported_version` must match the target game major version. This page records **what to check when migrating** and is not the full text of the official changelog.

## Statement

```pdx
supported_version="1.19.*"
```

- Both user directory `.mod` and `descriptor.mod` must be written
- `1.19.*` can cover minor versions; regression testing is required across major versions (1.15→1.19)

## Migration workflow

1. Backup mods
2. Read the official patch notes and DLC changes (NSB/BBA/AAT/Götterdämmerung/NCNS, etc.)
3. Use the game to load the mod and check `logs/error.log` and `game.log`
4. Return according to the system: country selection at the start → national focus → event → battle → peace
5. Check the library's "Adaptation Guide" for documents related to your span (consumer products, 1.15 migration, NCNS, etc.)
6. Update `supported_version` and self-test instructions

## High risk directory

| Region | Reason |
|------|------|
| `common/national_focus` | New fields, filters, shared trees |
| `common/ideas` / Bill | Semantic changes to consumer goods and other economic fields |
| `common/technologies` / doctrines | Tree rework, sub-doctrine |
| `common/units` / equipment | Tank and aircraft designers, modules |
| `common/characters` | consultant/scientist structure |
| `history/*` | state number change, building name |
| `common/peace_conference` | AI/actions after peace system rework |
| `common/factions` | New faction system |
| `interface` / `gfx` | UI revision leads to pink pictures |
| `common/defines` | Numeric constant renaming |
## Known points of concern (need to respond to the corresponding patch of the year, do not memorize the values)

- **Consumer Goods**: Old fields and new `consumer_goods_factor` and other semantics are subject to the current ontology idea and adaptation documents.
- **Character system**: old `create_country_leader` moved to `characters`
- **Equipment Designer**: OOB and `create_equipment_variant` after tank/aircraft/ship modularization
- **doctrine**: Subdoctrine/Mastery (`subdoctrine-template.md`)
- **Faction**: 1.15+ faction template system (`faction-system-template.md`)
- **map/state**: Large version of history and strategic areas after Zengzhou
- **MIO**: Manufacturer replacement for old designer idea slot

For a specific version of the "new correction list", please refer to the library's `information/adaptation guide' and official instructions; record the conclusions in your own mod notes instead of copying out-of-date values.

## error.log reading (simplified)

- `Unknown modifier`: Modification key expired → check `modifiers-index-template.md`
- `Invalid technology` / `Unknown focus`: id rename or delete
- `Error: unexpected token`: syntax or new keyword
- Pink picture: GFX path or interface revision

## Depends on mod

- After upgrading the front-end total conversion, check the `dependencies` name and content API
- Specifications for this project: **Do not write compatible code**; keep up with the previous version or clearly break the release

## Checklist template (can be copied to PR/memo)

```
Target version:
span:
error.log clear: yes/no
Start:
National focus:
Event:
Battle:
Peace:
Known breaking changes:
```

## Related
- `mod-structure-template.md` / `modifiers-index-template.md` / `character-template.md` / `equipment-variant-template.md` / `faction-system-template.md`
