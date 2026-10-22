# Equipment Modules template

## File location

`common/units/equipment/modules/<xxx>.txt`

## General structure

```pdx
equipment_modules = {

	my_module = {
		abbreviation = "MM"
		category = tank_engine_type

		parent = previous_module

		add_stats = {
			reliability=0.05
			maximum_speed = 1
		}
		multiply_stats = {
			build_cost_ic = 0.05
		}

		xp_cost = 1
		dismantle_cost_ic = 2

		build_cost_resources = {
			steel=1
		}

		can_convert_from = {
			module = old_module
			module_category = tank_engine_type
			convert_cost_ic = 1
		}
	}

}
```

## tank module category

| category | description |
|------|------|
| `tank_engine_type` | Engine |
| `tank_armor_type` | Armor |
| `tank_suspension_type` | Suspension |
| `tank_non_tracked_suspension_type` | Non-tracked suspension |
| `tank_light_turret_type` | Light turret |
| `tank_medium_turret_type` | Medium turret |
| `tank_heavy_turret_type` | Heavy turret |
| `tank_super_heavy_turret_type` | Super heavy turret |
| `tank_modern_turret_type` | Modern turret |
| `tank_small_main_armament` | Small main gun |
| `tank_flamethrower` | Flamethrower |
| `tank_medium_main_armament` | Medium main gun |
| `tank_heavy_main_armament` | Heavy main gun |
| `tank_super_heavy_main_armament` | Super heavy main gun |
| `tank_radio_module` | Radio |
| `tank_special_module` | Special module |
| `tank_secondary_turret` | Secondary turret |
| `lc_main_armament` | Land patrol main weapon |
| `lc_secondary_armament` | Land patrol secondary weapon |
| `lc_additional_armament` | Land patrol additional weapons |
| `lc_radio_module` | Land Cruiser Radio |
| `lc_aerial_deployment` | Land patrol air deployment |
| `lc_external_features` | Land patrol external features |
| `lc_structural_features` | Land patrol structural features |
## Aircraft module category

| category | description |
|------|------|
| `plane_engine_type` | Single engine |
| `twin_plane_engine_type` | Twin engine |
| `medium_plane_engine_type` | three-engine |
| `quad_large_plane_engine_type` | Quad engine |
| `large_plane_engine_type` | Six-engine |
| `plane_jet_engine_type` | Single jet engine |
| `twin_plane_jet_engine_type` | Twin jet engine |
| `medium_plane_jet_engine_type` | Three-jet engine |
| `quad_large_plane_jet_engine_type` | Quad jet engine |
| `large_plane_jet_engine_type` | Six jet engine |
| `plane_rocket_engine_type` | rocket engine |
| `fighter_weapon` | Fighter weapon |
| `cas_weapon` | Close ground support aircraft weapon |
| `tac_weapon` | Tactical bomber weapon |
| `strat_weapon` | Strategic bomber weapons |
| `nav_bomber_weapon` | Naval bomber weapon |
| `recon_camera` | Reconnaissance camera |
| `mine_warfare_offense` | Mine laying equipment |
| `mine_warfare_defense` | Mine clearing equipment |
| `kamikaze_bomber_weapon` | Suicide aircraft weapon |
| `plane_special_module_small` | Small armor plate |
| `plane_special_module_medium` | Medium armor plate |
| `plane_special_module_large` | Large armor plate |
| `plane_special_module_bomb_sights` | Bomber sights |
| `plane_special_module_radio_navigation` | Radio navigation |
| `plane_special_module_air_ground_radar` | Air-to-ground radar |
| `plane_special_module_air_air_radar` | Air-to-air radar |
| `plane_special_module_defense_turret` | Defense turret |
| `plane_special_module_defense_turret_x2` | Twin defense turrets |
## Ship module category

| category | description |
|------|------|
| `ship_light_battery` | Light artillery |
| `dp_light_battery` | High and flat dual-purpose light cannon |
| `ship_heavy_battery` | Heavy artillery |
| `ship_super_heavy_battery` | Super heavy gun |
| `ship_medium_battery` | Hit |
| `ship_light_medium_battery` | Cruiser main battery |
| `ship_secondaries` | Secondary batteries |
| `ship_dp_secondaries` | High-level dual-purpose secondary guns |
| `ship_anti_air` | Anti-aircraft gun |
| `ship_fire_control_system` | Fire control |
| `ship_radar` | radar |
| `sub_ship_engine` | Submarine engine |
| `sub_ship_nuclear_engine` | Nuclear submarine engine |
| `cruiser_ship_engine` | Cruiser engine |
| `heavy_ship_engine` | Heavy battleship engine |
| `carrier_ship_engine` | Aircraft carrier engine |
| `ship_torpedo` | Surface torpedo |
| `ship_torpedo_sub` | Submarine torpedo |
| `ship_mine_layer` | Surface mines |
| `ship_mine_layer_sub` | Submarine mines |
| `ship_mine_warfare` | Minesweeper |
| `ship_depth_charge` | depth charge |
| `ship_sub_snorkel` | periscope |
| `ship_sub_coating` | coating |
| `ship_light_battery_sub` | Submarine light gun |
| `ship_airplane_launcher` | Seaplane launcher |
| `ship_deck_space` | aircraft deck |
| `big_ship_deck_space` | Large aircraft deck |
| `ship_rocket` | Ship-based missiles |
| `ship_nuclear_rocket` | Ship-based nuclear missile |
| `ship_extra_fuel_tank` | Extra fuel tank |
| `ship_sonar` | Sonar |
| `ship_heavy_armor` | Heavy battleship armor |
| `ship_cruiser_armor` | Cruiser armor |
| `ship_carrier_armor` | Aircraft carrier armor |
| `ship_ice_carrier_armor` | Ice carrier armor |
## Common field descriptions

| Field | Description |
|------|------|
| `abbreviation` | abbreviation |
| `category` | Module slot type |
| `parent` | Predecessor module |
| `allowed_module_categories` | Allowed main weapon categories (for turrets) |
| `forbid_equipment_type_exact_match_for_category` | Forbid exact matching equipment types (for turrets) |
| `allow_equipment_type` | What positioning is allowed |
| `forbid_equipment_type` | What positioning is prohibited |
| `forbid_equipment_type_exact_match` | Forbidden as exact match (like `armor`) |
| `add_stats` | Addition attributes |
| `multiply_stats` | Multiplication properties |
| `add_average_stats` | Add average value (for some ships/aircraft) |
| `mission_type_stats` | Mission-specific bonuses (for aircraft) |
| `xp_cost` | Design experience cost (tank/aircraft); fixed to 5 for ships |
| `dismantle_cost_ic` | Dismantling cost |
| `build_cost_resources` | Resource consumption |
| `can_convert_from` | Can convert source |
| `critical_parts` | Module damaged display type |
| `add_equipment_type` | Change equipment type |
| `allow_mission_type` | Allowed missions (for aircraft) |
| `gui_category` | UI grouping |
| `gfx` | Ship module icon name |
| `sfx` | sound effects |
## Icon definition

### Tank/Aircraft Module

```pdx
spriteType = {
	name = "GFX_EMI_my_module"
	textureFile = "gfx/interface/equipmentdesigner/<xxx>.dds"
	legacy_lazy_load = no
}
```

### Ship module

```pdx
spriteType = {
	name = "GFX_SMI_my_module"
	textureFile = "gfx/interface/equipmentdesigner/naval/<xxx>.dds"
	legacy_lazy_load = no
}
```

## Localization

```yaml
 my_module:0 "Module name"
 my_module_desc:0 "Module Detailed Description"
```
