> State is a "region" and contains multiple provinces.

# State (region) template

## File location

`history/states/<xxx>.txt`

## Infrastructure

```pdx
state = {
	id=242
	name = "STATE_242"

	manpower = 131000
	state_category = city

	local_supplies = 0.0

	provinces = {
		528 2246 2333 3322
	}

	buildings_max_level_factor = 0.1
	impassable=no

	resources = {
		oil = 0
		aluminum = 0
		rubber = 0
		tungsten = 0
		steel = 0
		chromium = 0
		coal=0
	}

	history = {
		owner=LYU
		add_core_of = LYU
		# controller = TAG # Used when the controller is different from the owner

		victory_points = {
			2246 1
		}

		buildings = {
			infrastructure=5
			industrial_complex = 3
			arms_factory = 1

			2246 = {
				bunker = 3
				dockyard=5
			}
		}

		219.1.1 = {
			owner=WUU
			add_core_of = WUU
		}
	}
}
```

## Common field descriptions

| Field | Description |
|------|------|
| `id` | Region ID |
| `name` | Region name localization key |
| `manpower` | population |
| `state_category` | Region type |
| `local_supplies` | Regional supplies |
| `provinces` | List of included province IDs |
| `buildings_max_level_factor` | Maximum building level modifier |
| `impassable` | Whether it is impassable, `yes/no` |
| `resources` | Resource reserves |
| `owner` | owner |
| `add_core_of` | core |
| `controller` | Controller (when different from owner) |
| `victory_points` | Victory points `{ province score }` |
| `buildings` | buildings |
## Region type

| Type | Description |
|------|------|
| `wasteland` | desert |
| `large_city` | Dense urban areas |
| `metropolis` | large urban area |
| `megalopolis` | metropolitan areas |
| `town` | Developed rural areas |
| `large_town` | Sparse town area |
| `rural` | rural areas |
| `enclave` | enclave |
| `small_island` | small island |
| `tiny_island` | Tiny island |
| `large_island` | Large Island |
| `pastoral` | pastoral area |
| `city` | urban area |

## Resource type

| Code | Description |
|------|------|
| `oil` | petroleum |
| `aluminium` | aluminum |
| `rubber` | rubber |
| `tungsten` | tungsten |
| `steel` | steel |
| `chromium` | Chromium |
| `coal` | coal |

## Common buildings

| Architecture | Description |
|------|------|
| `infrastructure` | infrastructure |
| `industrial_complex` | Civilian factory |
| `arms_factory` | Military factory |
| `dockyard` | Dockyard |
| `air_base` | air force base |
| `naval_base` | naval base |
| `bunker` | land fortress |
| `coastal_bunker` | Coastal bunker |
| `anti_air_building` | Anti-aircraft guns |
| `radar_station` | Radar station |
| `fuel_silo` | Fuel Silo |
| `rocket_site` | rocket launch site |
| `nuclear_reactor` | Nuclear reactor |
| `synthetic_refinery` | Synthetic Refinery |
## Multiple script ownership

```pdx
history = {
	owner = TAG
	add_core_of = TAG

	1936.1.1 = {
		owner = TAG
		add_core_of = TAG
	}

	1939.1.1 = {
		owner=OTHER
	}
}
```
