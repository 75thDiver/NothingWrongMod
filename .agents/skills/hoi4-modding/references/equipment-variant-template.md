#Equipment variant (create_equipment_variant) template

## Use location

Typically located in `history/countries/<XXX>.txt`, an OOB file, or a script effect.

## Infrastructure

```pdx
create_equipment_variant = {
	name = "Light Tank Mk. IV"
	type = light_tank_chassis_1
	parent_version = 0

	modules = {
		main_armament_slot = tank_heavy_machine_gun
		turret_type_slot = tank_light_one_man_tank_turret
		suspension_type_slot = tank_christie_suspension
		armor_type_slot = tank_riveted_armor
		engine_type_slot = tank_gasoline_engine
	}

	upgrades = {
		tank_nsb_engine_upgrade = 2
		tank_nsb_armor_upgrade = 1
	}

	icon = "GFX_ENG_basic_light_tank_medium"
	model = <model>
	design_team = <MIO name>
	obsolete=yes
}
```

## Common fields

| Field | Description |
|------|------|
| `name` | Variant name |
| `type` | Chassis/fuselage/hull type |
| `parent_version` | Sort by the same chassis, `0` is the oldest |
| `name_group` | Name group |
| `modules` | Module assembly |
| `upgrades` | Upgrade levels |
| `icon` | icon |
| `model` | model |
| `design_team` | Specify MIO |
| `obsolete` | Whether to retire |
| `allow_without_tech` | Whether to bypass technology requirements |
| `role_icon_index` | Role icon index (ship) |
| `mark_older_equipment_obsolete` | Mark old variants obsolete |
| `show_position` | Whether to display version suffix |
## Tank Chassis

| Code | Description |
|------|------|
| `light_tank_chassis_0` | Interwar light tank chassis |
| `light_tank_chassis_1/2/3` | Basic/improved/advanced light tank chassis |
| `medium_tank_chassis_0/1/2/3` | Medium tank chassis |
| `heavy_tank_chassis_0/1/2/3` | Heavy tank chassis |
| `modern_tank_chassis_1` | Modern tank chassis |
| `amphibious_tank_chassis_1` | Amphibious tank chassis |
| `super_heavy_tank_chassis_1` | Super heavy tank chassis |

## Tank module slot

| Slot | Description |
|------|------|
| `main_armament_slot` | Main gun |
| `turret_type_slot` | Turret |
| `suspension_type_slot` | Suspension |
| `armor_type_slot` | Armor type |
| `engine_type_slot` | Engine |
| `special_type_slot_1~4` | Special functions |

## Commonly used tank accessories

### Engine

| Code | Description |
|------|------|
| `tank_gasoline_engine` | Gasoline engine |
| `tank_diesel_engine` | Diesel engine |
| `tank_petrol_electric_engine` | Fuel-electric engine |
| `tank_gas_turbine_engine` | Gas turbine engine |

### Armor

| Code | Description |
|------|------|
| `tank_riveted_armor` | Riveted armor |
| `tank_cast_armor` | Cast Armor |
| `tank_welded_armor` | Welded armor |
### Suspension

| Code | Description |
|------|------|
| `tank_torsion_bar_suspension` | Torsion bar |
| `tank_christie_suspension` | Christie Suspension |
| `tank_bogie_suspension` | Trolley suspension |
| `tank_interleaved_suspension` | Interleaved road wheels |

### Turret

| Code | Description |
|------|------|
| `tank_light_one_man_tank_turret` | Light single-crew turret |
| `tank_medium_one_man_tank_turret` | Medium one-man turret |
| `tank_light_two_man_tank_turret` | Light two-man turret |
| `tank_medium_two_man_tank_turret` | Medium two-man turret |
| `tank_heavy_two_man_tank_turret` | Heavy two-man turret |
| `tank_light_three_man_tank_turret` | Light three-man turret |
| `tank_medium_three_man_tank_turret` | Medium three-man turret |
| `tank_heavy_three_man_tank_turret` | Heavy three-man turret |
| `tank_super_heavy_three_man_tank_turret` | Super heavy three-man turret |
| `tank_light_fixed_superstructure_turret` | Light fixed turret |
| `tank_medium_fixed_superstructure_turret` | Medium fixed turret |
| `tank_heavy_fixed_superstructure_turret` | Heavy fixed turret |
| `tank_super_heavy_four_man_tank_turret` | Super heavy four-man turret |
| `tank_modern_tank_turret` | Modern turret |
### Main gun

| Code | Description |
|------|------|
| `tank_heavy_machine_gun` | Heavy machine gun |
| `flamethrower` | flamethrower |
| `tank_auto_cannon` / `tank_auto_cannon_2` | Machine cannon |
| `tank_anti_air_cannon/2/3` | Anti-aircraft cannon |
| `tank_medium_howitzer` / `tank_medium_howitzer_2` | Medium howitzer |
| `tank_heavy_howitzer` | Heavy howitzer |
| `tank_small_cannon` / `tank_small_cannon_2` | Small cannon |
| `tank_medium_cannon` / `tank_medium_cannon_2` | Medium cannon |
| `tank_high_velocity_cannon/2/3` | High velocity cannon |
| `tank_heavy_cannon/2/3` | Heavy cannon |
| `tank_super_heavy_cannon` | Super heavy cannon |
| `tank_close_support_gun` | Close support gun |

### Special features

| Code | Description |
|------|------|
| `tank_radio_1/2/3` | radio |
| `amphibious_drive` | Amphibious drive |
| `secondary_turret_hmg` | Heavy machine gun secondary turret |
| `secondary_turret_small_cannon` | Small cannon secondary turret |
| `secondary_turret_close_support_gun` | Close support gun secondary turret |
| `additional_machine_guns` | Additional machine guns |
| `sloped_armor` | Sloped armor |
| `stabilizer` | gun stabilizer |
| `smoke_launchers` | Smoke launchers |
| `extra_ammo_storage` | Extra ammo rack |
| `wet_ammo_storage` | Wet ammunition rack |
| `expanded_fuel_tank` | Fuel tank |
## Naval Hull

| Code | Description |
|------|------|
| `ship_hull_carrier_1/2/3` | 1936/1940/1944 aircraft carrier hull |
| `ship_hull_carrier_conversion_bb` | Conversion of battleship hull |
| `ship_hull_carrier_conversion_ca` | Conversion of cruiser hull |
| `ship_hull_cruiser_1/2/3/4` | Cruiser Hull |
| `ship_hull_pre_dreadnought` | Early heavy battleship hull |
| `ship_hull_heavy_1/2/3/4` | Battleship Hull |
| `ship_hull_super_heavy_1` | Super heavy battleship |
| `ship_hull_light_1/2/3/4` | Destroyer Hull |
| `ship_hull_submarine_1/2/3/4` | Submarine hull |
| `ship_hull_cruiser_submarine` | Cruiser submarine |
| `ship_hull_torpedo_cruiser` / `torpedo_cruiser` | Heavy mine cruiser |
| `ship_hull_cruiser_panzerschiff` | Armored ship |
| `ship_hull_cruiser_coastal_defense_ship` | Coastal defense ship |
| `SH_battleship_1/2` | Super heavy battleship |

## Ship module slot

| Slot | Description |
|------|------|
| `fixed_ship_battery_slot` | Main gun |
| `fixed_ship_secondaries_slot` | Secondary battery |
| `fixed_ship_anti_air_slot` | Anti-aircraft gun |
| `fixed_ship_torpedo_slot` | Torpedo |
| `fixed_ship_deck_slot_1/2` | Deck space |
| `fixed_ship_fire_control_system_slot` | Fire control |
| `fixed_ship_radar_slot` | Radar/Sonar |
| `fixed_ship_engine_slot` | Engine |
| `fixed_ship_armor_slot` | Armor |
| `front_1/2_custom_slot` | Free choice of ship front |
| `mid_1/2/3_custom_slot` | Customized mid section |
| `rear_1/2_custom_slot` | Rear selection |
## Commonly used ship accessories

### Main gun

| Code | Description |
|------|------|
| `ship_light_battery_1/2/3/4` | Light artillery |
| `dp_light_battery_1/2/3/4` | High and flat dual-purpose light gun |
| `ship_heavy_battery_1/2/3/4` | Heavy artillery |
| `ship_super_heavy_battery_1` | Super heavy gun |
| `ship_light_medium_battery_1/2/3/4` | Light cruiser gun |
| `ship_medium_battery_1/2/3/4` | Heavy cruiser gun |
| `dp_ship_medium_1` | 152mm high and flat dual-purpose rapid-fire gun |

### Secondary battery/anti-aircraft/torpedoes

| Code | Description |
|------|------|
| `ship_secondaries_1/2` | Secondary batteries |
| `dp_ship_secondaries_1/2/3/4` | High and flat dual-purpose secondary guns |
| `ship_torpedo_1/2/3/4` | Surface torpedo |
| `ship_torpedo_sub_1/2/3/4` | Submarine torpedo |
| `ship_anti_air_1/2/3/4` | Anti-aircraft guns |
| `ship_depth_charge_1/2/3/4` | depth charge |

### Engine

| Code | Description |
|------|------|
| `light_ship_engine_1/2/3/4` | Light engine |
| `sub_ship_engine_1/2/3/4` | Submarine engine |
| `cruiser_ship_engine_1/2/3/4` | Cruiser engine |
| `heavy_ship_engine_1/2/3/4` | Heavy engine |
| `carrier_ship_engine_1/2/3/4` | Carrier engine |
### Armor

| Code | Description |
|------|------|
| `ship_armor_bb_1/2/3` | Battleship armor |
| `ship_armor_bc_1/2/3` | Battlecruiser armor |
| `ship_armor_shbb` | Super heavy armor |
| `ship_armor_cruiser_1/2/3/4` | Cruiser armor |
| `ship_armor_carrier_deck` | Flight deck armor |

### Others

| Code | Description |
|------|------|
| `ship_fire_control_system_1/2/3` | Fire control |
| `ship_radar_1/2/3/4` | radar |
| `ship_sonar_1/2` | Sonar |
| `ship_sub_snorkel_1/2` | snorkel |
| `ship_mine_layer_1` / `ship_mine_sweeper_1` | Minelaying/Mine Sweeper |
| `ship_airplane_launcher_1/2` | Seaplane catapult |
| `ship_deck_space` | Hangar |
| `ship_extra_fuel_tank` | Extra fuel tank |

## Aircraft fuselage

| Code | Description |
|------|------|
| `fighter_equipment_0/1/2/3` | Fighter |
| `cv_fighter_equipment_0/1/2/3` | Carrier-based fighter |
| `jet_fighter_equipment_1/2` | Jet fighter |
| `CAS_equipment_1/2/3` | Close support aircraft |
| `cv_CAS_equipment_1/2/3` | Carrier-based close support aircraft |
| `nav_bomber_equipment_1/2/3` | Naval bomber |
| `cv_nav_bomber_equipment_1/2/3` | Carrier-based naval bomber |
| `tac_bomber_equipment_0/1/2/3` | Tactical bomber |
| `jet_tac_bomber_equipment_1/2` | Jet tactical bomber |
| `heavy_fighter_equipment_1/2/3` | Heavy fighter |
| `strat_bomber_equipment_1/2/3` | Strategic bomber |
| `jet_strat_bomber_equipment_1` | Jet strategic bomber |
| `scout_plane_equipment_1/2` | Scouting plane |
| `rocket_suicide_equipment_1` | Suicide attack aircraft |
## Aircraft module slot

| Slot | Description |
|------|------|
| `fixed_main_weapon_slot` | Main weapon |
| `fixed_auxiliary_weapon_slot_1~4` | Secondary weapons |
| `engine_type_slot` | Engine |
| `special_type_slot_1~6` | Special functions (use `empty` when not needed) |

## Commonly used aircraft accessories

### Weapons

| Code | Description |
|------|------|
| `light_mg_2x/4x` | Light machine gun |
| `heavy_mg_2x/4x` | Heavy machine gun |
| `aircraft_cannon_1_1x/2x` | Cannon I |
| `aircraft_cannon_2_1x/2x` | Cannon II |
| `small_bomb_bay` | Small bomb bay |
| `medium_bomb_bay` | Medium bomb bay |
| `large_bomb_bay` | Large bomb bay |
| `tank_buster_1/2` | Anti-tank cannon |
| `rocket_rails` | Rocket launch rails |
| `bomb_locks` | bomb holder |
| `guided_anti_ship_missile` | Guided anti-ship missile |
| `torpedo_mounting` | Torpedo mount |
| `fixed_explosive_charge` | Fixed explosive (suicide aircraft) |
| `airdropped_mines` | Airdropped mines |
| `recon_camera` | Reconnaissance camera |

### Engine

| Code | Description |
|------|------|
| `engine_1_1x/2x/3x/4x/6x` | Engine I |
| `engine_2_1x/2x/3x/4x/6x` | Engine II |
| `engine_3_1x/2x/3x/4x/6x` | Engine III |
| `engine_4_1x/2x/3x/4x/6x` | Engine IV |
| `jet_engine_1x/2x/3x/4x/6x` | Jet engine |
| `rocket_engine_1/2/3` | Rocket engine |
### Special features

| Code | Description |
|------|------|
| `bomb_sights_1/2` | Bomb sight |
| `radio_navigation_1/2` | Radio navigation |
| `air_ground_radar_1/2` | Air-ground radar |
| `air_air_radar_1/2` | Air-to-air radar |
| `fuel_tanks_small/medium/large` | Extra fuel tanks |
| `self_sealing_fuel_tanks_small/medium/large` | Self-sealing fuel tanks |
| `armor_plate_small/medium/large` | Armor plate |
| `dive_brakes_small/medium/large` | Dive speed brake |
| `flying_boat_medium/large` | Hull modification |
| `lmg_defense_turret` / `hmg_defense_turret` / `cannon_defense_turret` | Defense Turrets |
| `drop_tanks` | Disposable drop tanks |
| `floats` | floats |
| `demining_coil` | Demining coil |
| `non_strategic_materials_small` | Use non-strategic resource materials |

## Empty module

If a slot does not require accessories, use `empty`:

```pdx
modules = {
	fixed_auxiliary_weapon_slot_1 = empty
}
```
