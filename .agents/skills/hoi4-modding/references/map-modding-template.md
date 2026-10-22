# Map project entrance template

The complete map drawing is an independent project (MapGen/Nudge/bmp). This page only lists **directory responsibilities and security changes** to avoid accidentally touching binary files.

## `map/` key file

| File/Directory | Function |
|-----------|------|
| `provinces.bmp` | Province color block definition |
| `definition.csv` | Province id ↔ RGB ↔ Sea, land, etc. |
| `terrain.bmp` / `terrain/` | Terrain texture |
| `heightmap.bmp` | height |
| `rivers.bmp` | rivers |
| `trees.bmp` / `cities.bmp` etc. | Decoration and cities |
| `adjacencies.csv` | adjacent/strait/impassable |
| `adjacency_rules.txt` | Special adjacency rules such as canals |
| `strategicregions/` | strategic regions |
| `supplyareas/` or supply-related | supply area (version-related) |
| `railways.txt` / `supply_nodes.txt` | Railway and hub data |
| `buildings.txt` / `positions.txt` | Building positions and unit positions |
| `unitstacks.txt` | Unit stacking bits |
| `default.map` | Map index declaration |
| `continent.txt` / `colors.txt` | Continents and Colors |

## Can be modified on the script side (relatively safe)

- `history/states/*.txt`: owner, building, resource, VP (`state-template.md`)
- In the effect, `add_building_construction` railway/port/hub (`resources-supply-template.md`)
- `map/strategicregions` text (needs to be synchronized when splitting provinces into strategic regions)
- `adjacency_rules` text rules
## High risk (special tools required)

- Redraw `provinces.bmp` / change `definition.csv` color value
- heightmap/river/terrain bmp
- Large-scale adjacency recalculation
- inconsistent with province list in `history/states`

Recommended tool chain: Library MapGen, Province Editor, Nudge; complete backup of `map/` before modification.

## default.map

Declare the file names of each map resource; `default.map` must be synchronized after renaming bmp.

## Verification

1. Is the startup stuck in loading the map?
2. Province/state does not match in the error log
3. Is there any unallocated province in the strategic area?
4. Whether the Strait/Canal Rules are still in effect

## with replace_path

Total conversion constant:

```pdx
replace_path="history/states"
replace_path="map/strategicregions"
```

`map` root bmp replacement should be done with extreme caution. See `mod-structure-template.md`.

## Related

- `state-template.md` / `resources-supply-template.md` / `ai-template.md` / `mod-structure-template.md`
