# Resources, Railways and Supply Templates

## Resource definition

File: `common/resources/00_resources.txt`

```pdx
resources = {
	oil = {
		icon_frame = 1
		cic = 0.125
		convoys = 0.1
	}
	steel = {
		icon_frame = 5
		cic = 0.125
		convoys = 0.1
	}
	# aluminum rubber tungsten chromium coal ...
}
```

| Field | Description |
|------|------|
| `icon_frame` | Interface icon frame |
| `cic` | Related to civilian factory valuation |
| `convoys` | Shipping consumption related |

**New resources** also require interface frames, localization, and production/trade UI adaptation. Content mods generally only use original resource types.

## Place resources on state

`history/states` or effect:

```pdx
resources = {
	steel=16
	oil=8
}

# Effect context (state scope)
add_resource = {
	type=steel
	amount = 8
}
```

Comment out the state locale (`modding-rules.md`).

## Infrastructure buildings (state/province)

In state's `history` building block or `add_building_construction`:

| Type (common in vanilla) | Level |
|------------------|------|
| `infrastructure` | state |
| `air_base` | state |
| `anti_air_building` | state |
| `radar_station` | state |
| `industrial_complex` / `arms_factory` / `dockyard` | state shared bits |
| `synthetic_refinery` / `fuel_silo`, etc. | Subject to the ontology buildings |
| `naval_base` | **province** level |
| `bunker` / `coastal_bunker` | province |
| `rail_way` | provincial railway |
| `supply_node` | Supply hub (province) |
```pdx
219 = {
	add_building_construction = {
		type=infrastructure
		level=1
		instant_build = yes
	}
	add_building_construction = {
		type = rail_way
		level=1
		instant_build = yes
		province=1234
	}
	add_building_construction = {
		type = supply_node
		level=1
		instant_build = yes
		province=1234
	}
	add_building_construction = {
		type = naval_base
		level=3
		instant_build = yes
		province=1234
	}
}
```

The province id must belong to the state; filling it in randomly will be invalid or an error will be reported.

## Strategic Area

File: `map/strategicregions/<id>-Name.txt`

```pdx
strategic_region = {
	id=1
	name = "STRATEGICREGION_1"
	provinces = {
		221 271 296
	}
	weather = {
		period = {
			between = { 0.0 30.0 }
			temperature = { -6.0 12.0 }
			# rain/snow/mud…
		}
	}
}
```

- Each province should fall within a strategic area
- Strategicregions must be maintained when changing the map/removing provinces
- AI `ai_areas` references strategic area id (`ai-template.md`)
- Localization: `STRATEGICREGION_*`
For large map projects, see the library map tutorial; **This template does not cover the entire bmp/Nudge process** (it is a low-priority map project).

## Supply concept (script side)

- Railway grade, supply hub, and port affect supply reach
- Country modifications may include `supply_consumption_factor`, `out_of_supply_factor`, etc. (check the modifier table)
- Dynamically modify railway building effects, do not manually modify unknown binary map files

## Specification

- Prioritize the six major resources of the vanilla + the existing types of the ontology (such as `coal`)
- Use `hidden_effect` + `custom_effect_tooltip` (traversal specification) when adding resources/railways in batches
- It is forbidden to make up the province; check the state file `provinces = {}`

## Related

- `state-template.md` / `buildings-template.md` / `ai-template.md` / `effects-template.md`
