> Building definitions are used to extend original buildings or add custom buildings.

#Buildings template

## File location

`common/buildings/<xxx>.txt`

## Infrastructure

```pdx
buildings = {

	my_building = {
		base_cost = 5000
		per_level_extra_cost = 1000
		value=1

		provincial=no
		shares_slots = yes
		infrastructure_construction_effect = yes

		damage_factor = 0.3
		repair_speed_factor = 1.0

		allied_build = yes
		only_costal=no
		disabled_in_dmz = yes

		icon_frame = 3
		show_on_map = 1
		show_on_map_meshes = 1
		has_destroyed_mesh = yes

		military_production = 0
		general_production=0
		naval_production = 0

		infrastructure=no
		air_base=no
		supply_node=no
		is_port = no
		refinery=no
		fuel_silo=no
		radar=no
		nuclear_reactor=no

		country_modifiers = {
			modifiers = {
				max_fuel_building = 1.5
			}
		}

		level_cap = {
			shares_slots = yes
			state_max = 10
			#province_max = 5
			group_by = my_building_group
			exclusive_with = rocket_site
		}
	}
}

spawn_points = {
	my_spawn = {
		type = state
		max=1
		only_costal=yes
		disable_auto_nudging = yes
	}
}
```

## Common field descriptions

| Field | Description |
|------|------|
| `base_cost` | Base construction cost |
| `per_level_extra_cost` | Extra cost per level |
| `value` | Bomb health and peace meeting scores |
| `infrastructure_construction_effect` | Whether the construction speed is affected by the infrastructure level |
| `provincial` | Whether to build only on province |
| `shares_slots` | Whether to use building slots |
| `damage_factor` | Air raid/land battle damage correction |
| `allied_build` | Whether to allow allies to build |
| `only_costal` | Whether coastal only |
| `disabled_in_dmz` | Whether construction is prohibited in the demilitarized zone |
| `icon_frame` | Icon frame index |
| `base_cost_conversion` | Conversion cost |
| `show_modifier` | Whether to display construction modifications |
| `per_controlled_building_extra_cost` | Extra cost for each additional building |
| `spawn_point` | Spawn point |
| `hide_if_missing_tech` | Hide when missing technology |
| `special_icon` | Special icon |
| `repair_speed_factor` | Repair rate |
| `air_defence` | Anti-air defense |
| `show_on_map` | Number of map models |
| `show_on_map_meshes` | Number of primitives per model |
| `always_shown` | Ignore the fog of war display |
| `has_destroyed_mesh` | A separate model when destroyed |
| `centered` | The model is centered |
| `military_production` | Number of military factories |
| `general_production` | Number of migrant workers |
| `naval_production` | Number of docks |
| `infrastructure` | tagged infrastructure |
| `air_base` | Marked as air base |
| `supply_node` | Mark as supply node |
| `is_port` | Mark as port |
| `land_fort` | Increase the level of land fort |
| `naval_fort` | Increase coastal fort level |
| `refinery` | tagged synthetic refinery |
| `fuel_silo` | Mark as fuel depot |
| `radar` | Mark as radar station |
| `rocket_production` | Rocket daily progress |
| `rocket_launch_capacity` | Daily rocket launch capacity |
| `nuclear_reactor` | tagged nuclear reactor |
| `gun_emplacement` | Tagged large caliber artillery |
| `only_display_if_exists` | Display only if exists |
| `is_buildable` | Can it be built |
| `need_detection` | Whether detection is required |
| `need_supply` | Whether supplies are needed |
| `disable_grow_animation` | Disable construction animation |
| `missing_tech_loc` | Missing technology prompt localization |
| `tags` | Building tags |
| `country_modifiers` | Modifiers for countries |
| `state_modifiers` | Modifiers for regions |
| `level_cap` | Level upper limit |
## level_cap field

| Field | Description |
|------|------|
| `shares_slots` | Whether to share slots |
| `state_max` | Maximum level per state |
| `province_max` | Maximum level per province |
| `group_by` | Building group name |
| `exclusive_with` | Mutually exclusive construction |

## Generate point

| Field | Description |
|------|------|
| `type` | `state` / `province` |
| `max` | Maximum number of spawn points |
| `only_costal` | Whether coastal |
| `disable_auto_nudging` | Disable automatic positioning |
