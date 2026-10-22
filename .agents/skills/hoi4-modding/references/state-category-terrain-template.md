# Area categories and terrain templates

## Region category state_category

Directory：`common/state_category/`

```pdx
state_categories = {
	city = {
		local_building_slots = 6
		color = { 0 200 0 }
	}
	rural = {
		local_building_slots = 2
		color = { 200 200 0 }
	}
}
```

`history/states` inside：

```pdx
state_category = city
```

- `local_building_slots`：shared building base
- Custom categories require localized names
- The list is also scattered `data/state-modifiers.md`  

## terrain terrain

File：`common/terrain/00_terrain.txt`

```pdx
categories = {
	forest = {
		color = { 89 199 85 }
		movement_cost = 1.5
		combat_width = 60
		combat_support_width = 30
		units = {
			attack = -0.15
		}
		enemy_army_bonus_air_superiority_factor = -0.1
		supply_flow_penalty_factor = 0.08
		buildings_max_level = {
			bunker = 4
		}
	}
	ocean = {
		naval_terrain = yes
		is_water = yes
		# ...
	}
}
```

- Changing the terrain is a matter of **global combat/movement/supply** balance, so be extremely careful.
- Map `terrain.bmp` Only determines what class is where; the values ​​are in this file
- The terrain characteristics of generals are linked with this（`custom-traits-template.md`）  

## Related

- `state-template.md` / `map-modding-template.md` / `resources-supply-template.md`
