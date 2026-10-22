> Full doctrine code reference table.

# Doctrine list

## Mastery effect

```pdx
add_mastery = {
	amount=100
	folder=land
	grand_doctrine = mobile_warfare
	sub_doctrine = mobile_infantry
	track = infantry
	index = 1
}

add_mastery_bonus = {
	bonus = 0.1
	days = 90
	name = my_mastery_bonus_loc
	folder=land
	track = infantry
}

add_daily_mastery = {
	amount = 0.1
	days = 90
	name = my_daily_mastery_loc
	folder=land
	track = infantry
}
```

| Field | Description |
|------|------|
| `amount` | Amount of mastery |
| `bonus` | Mastery gain percentage |
| `days` | Number of days to last |
| `name` | localization key |
| `folder` | Doctrine folder |
| `grand_doctrine` | Grand Doctrine |
| `sub_doctrine` | Sub-doctrine |
| `track` | Track type |
| `index` | Track index (starting from 0) |

## Army sub-doctrine

### Infantry

| code | name |
|------|------|
| `mobile_infantry` | Motorized infantry |
| `defensive_postures` | Defensive posture |
| `large_unit_tactics` | Large unit tactics |
| `assault_infantry` | Assault infantry |
| `mounted_infantry` | Mounted infantry |
| `commandos` | Excellent individual soldier |
| `irregulars` | Irregulars |
| `peoples_war` | People's Militia |
| `great_war_infantry` | Great War Infantry |
### Artillery and Combat Support

| code | name |
|------|------|
| `fire_concentration` | Concentration of firepower |
| `anti_tank_frontline` | Anti-tank frontline |
| `flying_batteries` | Mobile artillery battery |
| `air_cavalry` | Air Cavalry |
| `mobile_recon_and_assault` | Mobile reconnaissance and assault |
| `self_propelled_support` | Self-propelled support |
| `siege_artillery` | Attacking firepower |
| `field_engineering` | Field engineering |

### Armor

| code | name |
|------|------|
| `armored_spearhead` | Armored Spearhead |
| `armored_infantry_support` | Armored infantry support |
| `streamlined_deployment` | Streamlined deployment |
| `mobile_defense` | Mobile defense |
| `armored_cavalry` | Armored Cavalry |
| `tank_destroyer_force` | Self-propelled anti-tank gun force |

### Combat

| code | name |
|------|------|
| `mission_type_tactics` | Mission-type tactics |
| `last_stand` | Desperate defense |
| `infiltration_tactics` | Infiltration tactics |
| `grand_assault` | Large-scale assault |
| `deep_battle` | Deep battle |
| `guerilla_war` | guerrilla warfare |
| `rapid_domination` | Rapid dominance |
| `expeditionary_warfare` | Expeditionary Warfare |
## Hainanzi Doctrine

### Submarine

| code | name |
|------|------|
| `wolfpacks` | wolf pack tactics |
| `submarine_fleet_operations` | Fleet operations |
| `capital_hunters` | Capital ship hunters |
| `submarine_coastal_defense` | Coastal defense submarine |
| `coastal_minelaying` | Coastal minelaying |
| `long_range_submarines` | Long range submarines |

### Screen Guard Ship

| code | name |
|------|------|
| `convoy_escort` | Convoy escort |
| `support_integrated_operations` | Joint operations |
| `hunter_killers` | Hunting wolves |
| `torpedo_primacy` | Torpedo supremacy |
| `anti_aircraft_cruisers` | Anti-aircraft cruisers |
| `screen_support_focus` | Focus on screen support |
| `jeune_ecole` | New tactical school |
| `patrol_boats` | patrol boats |

### Aircraft carrier

| code | name |
|------|------|
| `carrier_battlegroups` | Carrier battle group |
| `floating_airfields` | Maritime airports |
| `escort_carrier_support` | Escort carrier support |
| `broad_naval_support` | Comprehensive combat support |
| `massed_carrier_fleet` | Aircraft carrier fleet cluster |
| `light_task_forces` | Light task force |

### Battleship

| code | name |
|------|------|
| `line_of_battle` | Line of battle |
| `battlecruiser_spremacy` | Fast battleship |
| `armored_raiders` | Armored raiders |
| `coastal_defence_fleet` | Coastal defense ship |
| `naval_gunfire_support` | Naval gunfire support |
| `battleship_antiair_screen` | Anti-aircraft battleship |
## Air Force Doctrine

### Fighter

| code | name |
|------|------|
| `air_subdoctrine_fighter_homeland_defense` | Homeland Air Defense |
| `air_subdoctrine_escort_fighter` | Medium range escort |
| `air_subdoctrine_fighter_bombers` | Fighter-bombers |
| `air_subdoctrine_tactical_flexibility` | Airspace dominance |
| `air_subdoctrine_dogfighting_mastery` | Volley Knight |
| `air_subdoctrine_fighter_central_field` | Air Combat Patrol |

### Attack aircraft

| code | name |
|------|------|
| `air_subdoctrine_flying_artillery` | Aerial artillery |
| `air_subdoctrine_dive_bombers` | Precision Strike |
| `air_subdoctrine_flexible_fire_support` | Earthsea coordination |
| `air_subdoctrine_carrier_strikes` | Sea-to-land air support |
| `air_subdoctrine_naval_strike_tactics` | Precision sea bombing |
| `air_subdoctrine_naval_torpedo_tactics` | Group mine tactics |

### Medium aircraft

| code | name |
|------|------|
| `air_subdoctrine_bomber_interception` | Heavy Interceptor |
| `air_subdoctrine_long_range_escort` | Long range escort |
| `air_subdoctrine_operational_air_support` | Combat air support |
| `air_subdoctrine_tactical_battlefield_support` | Tactical-level battlefield support |
| `air_subdoctrine_theater_interdiction` | Warzone lockdown |
| `air_subdoctrine_aerial_reconnaissance` | Aerial reconnaissance |
### Heavy aircraft

| code | name |
|------|------|
| `air_subdoctrine_night_bombing` | Night strategic bombing |
| `air_subdoctrine_carpet_bombing` | Carpet bombing |
| `air_subdoctrine_deep_air_raids` | Air raids behind enemy lines |
| `air_subdoctrine_flying_fortresses` | Flying Fortresses |
| `air_subdoctrine_coastal_air_patrol` | Coastal air patrol |
| `air_subdoctrine_open_ocean_air_patrol` | Ocean air patrol |
| `air_subdoctrine_heavy_aircraft_focus` | Multi-purpose heavy aircraft center of gravity |

## Original Lord Doctrine

### Army

| code | name |
|------|------|
| `new_mobile_warfare` | Mobile warfare |
| `superior_firepower` | Superior firepower |
| `grand_battleplan` | Grand battle plan |
| `mass_assault` | Mass Assault |

### Navy

| code | name |
|------|------|
| `new_fleet_in_being` | fleet in being |
| `new_convoy_raiding` | Trade blocking |
| `new_base_strike` | Base strike |

### Air Force

| code | name |
|------|------|
| `new_operational_integrity` | Continuous operations |
| `new_battlefield_support` | Battlefield support |
| `new_strategic_destruction` | Strategic destruction |
## Original track type

### Army

| code | name |
|------|------|
| `infantry` | Infantry sub-doctrine |
| `combat_support` | Battlefield support sub-doctrine |
| `armor` | Armor sub-doctrine |
| `operations` | Operations sub-doctrine |

### Navy

| code | name |
|------|------|
| `submarines` | Submarines doctrine |
| `screens` | Screen Guard Ship Doctrine |
| `carriers` | Aircraft carrier theory |
| `capital_ships` | Capital ship doctrine |

### Air Force

| code | name |
|------|------|
| `fighter_aircraft` | Fighter Aircraft Doctrine |
| `strike_aircraft` | Attack aircraft doctrine |
| `medium_aircraft` | Medium aircraft sub-doctrine |
| `heavy_aircraft` | Heavy aircraft sub-doctrine |
