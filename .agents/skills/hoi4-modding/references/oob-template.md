# OOB (starting troops and production lines) template

## File location

`history/units/<xxx>.txt`

## Loading method

In `history/countries/<TAG>.txt` write:

```pdx
set_oob = "TAG_army_1936" # Army
set_naval_oob = "TAG_navy_1936" # Navy
set_air_oob = "TAG_air_1936" # Air Force
```

The army, navy and air force must be written separately.

## Army establishment template

```pdx
division_template = {
	name = "Infantry Division"
	regiments = {
		infantry = { x = 0 y = 0 }
		infantry = { x = 0 y = 1 }
		infantry = { x = 0 y = 2 }
		infantry = { x = 1 y = 0 }
		infantry = { x = 1 y = 1 }
		infantry = { x = 1 y = 2 }
		artillery_brigade = { x = 2 y = 0 }
	}
	support = {
		engineer = { x = 0 y = 0 }
		recon = { x = 0 y = 1 }
	}
	priority=1
	division_names_group = USA_INF_01
}
```

### Common fields

| Field | Description |
|------|------|
| `name` | Create name |
| `regiments` | Combat camp, `x` row `y` column |
| `support` | support company |
| `priority` | Supply priority: `0` reserve, `1` default, `2` elite |
| `division_cap` | The upper limit of training for this division |
| `is_locked` | Whether to lock |
| `force_allow_recruiting` | Whether to allow training to lock the establishment |
| `division_names_group` | Name group |
## Army unit generation

```pdx
units = {
	division = {
		name = "1st Infantry Division"
		location=9392
		division_template = "Infantry Division"
		start_experience_factor = 0.2
		start_equipment_factor = 0.3
		start_manpower_factor = 0.3
		force_equipment_variants = {
			infantry_equipment_0 = {
				owner = TAG
				creator=TAG
				amount=1000
			}
		}
	}
}
```

### Common fields

| Field | Description |
|------|------|
| `location` | Generate location (province) |
| `division_template` | Using division |
| `start_experience_factor` | Initial experience `0~1` |
| `start_equipment_factor` | Initial equipment `0~1` |
| `start_manpower_factor` | Initial manpower `0~1` |
| `force_equipment_variants` | Force specified equipment |
| `officer` | Teacher information |

## Naval unit generation

```pdx
units = {
	fleet = {
		name = "High Seas Fleet"
		naval_base = 241

		task_force = {
			name = "First Task Force"
			location=241

			ship = {
				name = "Germany"
				definition = heavy_cruiser
				start_experience_factor = 0.3
				pride_of_the_fleet = yes
				equipment = {
					ship_hull_cruiser_panzerschiff = {
						amount=1
						owner=GER
						version_name = "Germany"
					}
				}
			}
		}
	}
}
```
## Air force unit generation

```pdx
air_wings = {
	500 = { # state id, airport required
		fighter_equipment_0 = {
			owner = "BRA"
			amount=10
			version_name = "Design model name"
		}
		name = "1st Fighter Wing"
	}
}
```

## Production line settings

```pdx
instant_effect = {
	add_equipment_production = {
		equipment = {
			type = infantry_equipment_0
			creator = "TAG"
			version_name = "name"
		}
		requested_factories = 1
		efficiency=100
		progress=0.19
		industrial_manufacturer = mio:xxx
	}
}
```

## Army Combat Battalion Code

| Code | Description |
|------|------|
| `infantry` | infantry |
| `cavalry` | Cavalry |
| `camelry` | Camel Cavalry |
| `motorized` | Motorized infantry |
| `bicycle_battalion` | bike camp |
| `mountaineers` | Mountain infantry |
| `mechanized` | Mechanized infantry |
| `marine` | Marine Corps |
| `marine_commando` | Marine Commando |
| `paratrooper` | airborne paratrooper |
| `militia` | militia |
| `irregular_infantry` | Irregular infantry |
| `penal_battalion` | Penal battalion |
| `fake_intel_unit` | Suspicious Soldier Camp |
| `light_armor` | Light tank |
| `medium_armor` | Medium tank |
| `heavy_armor` | Heavy tank |
| `super_heavy_armor` | Super heavy tank |
| `modern_armor` | Modern tanks |
| `amphibious_armor` | Amphibious tank |
| `amphibious_mechanized` | Amphibious mechanized vehicle |
| `anti_tank_brigade` | Anti-tank gun |
| `anti_air_brigade` | Anti-aircraft gun |
| `armored_car` | Armored car |
| `artillery_brigade` | Artillery |
| `mot_artillery_brigade` | Motorized artillery |
| `mot_anti_tank_brigade` | Motorized anti-tank |
| `mot_anti_air_brigade` | Motorized air defense |
| `rocket_artillery_brigade` | rocket launcher |
| `mot_rocket_artillery_brigade` | Motorized rocket launcher |
| `motorized_rocket_brigade` | Self-propelled rocket launcher |
| `light_sp_anti_air_brigade` | Light self-propelled air defense |
| `medium_sp_anti_air_brigade` | Medium self-propelled air defense |
| `heavy_sp_anti_air_brigade` | Heavy self-propelled air defense |
| `super_heavy_sp_anti_air_brigade` | Super heavy self-propelled air defense |
| `modern_sp_anti_air_brigade` | Modern self-propelled air defense |
| `light_sp_artillery_brigade` | Light self-propelled artillery |
| `medium_sp_artillery_brigade` | Medium self-propelled artillery |
| `heavy_sp_artillery_brigade` | Heavy self-propelled artillery |
| `super_heavy_sp_artillery_brigade` | Super heavy self-propelled artillery |
| `modern_sp_artillery_brigade` | Modern self-propelled artillery |
| `light_tank_destroyer_brigade` | Light self-propelled anti-tank |
| `medium_tank_destroyer_brigade` | Medium self-propelled anti-tank |
| `heavy_tank_destroyer_brigade` | Heavy self-propelled anti-tank |
| `super_heavy_tank_destroyer_brigade` | Super heavy self-propelled anti-tank |
| `modern_tank_destroyer_brigade` | Modern self-propelled anti-tank |
## Army Support Company Code

| Code | Description |
|------|------|
| `anti_air` | Anti-aircraft |
| `anti_tank` | anti-tank |
| `armored_car_recon` | Lightly armored reconnaissance |
| `artillery` | Artillery support |
| `engineer` | Engineer |
| `field_hospital` | Field hospital |
| `logistics_company` | Logistics |
| `maintenance_company` | Maintenance |
| `military_police` | Military Police |
| `mot_recon` | Motorized reconnaissance |
| `recon` | Reconnaissance |
| `rocket_artillery` | Rocket artillery support |
| `signal_company` | Communication |
| `light_flame_tank` | Light flame tank |
| `medium_flame_tank` | Medium flame tank |
| `heavy_flame_tank` | Heavy flame tank |
| `rangers_support` | Rangers |
| `airborne_light_armor` | Airborne light armor |
| `mountaineers_ski` | Ski Troops |
| `pioneer_support` | Pioneer Engineering Troops |
| `marines_shore_parties` | beachhead parties |
| `marines_commandoes` | Marine Commandoes |
| `winter_logistics_support` | Winter logistics |
| `long_range_patrol_support` | Long range patrol |

## Ship definition code

| Code | Description |
|------|------|
| `battleship` | battleship |
| `carrier` | aircraft carrier |
| `destroyer` | destroyer |
| `battle_cruiser` | Battlecruiser |
| `heavy_cruiser` | Heavy cruiser |
| `light_cruiser` | light cruiser |
| `submarine` | submarine |
## Air Force Equipment Code

Refer to the aircraft fuselage section in `equipment-variant-template.md`.

## Naval Hull Code

See the naval hull section in `equipment-variant-template.md`.
