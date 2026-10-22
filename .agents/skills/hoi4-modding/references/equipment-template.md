# Equipment template

## File location

`common/units/equipment/<xxx>.txt`

## Infrastructure

```pdx
equipments = {

	# Equipment prototype (archetype)
	my_equipment_archetype = {
		year=1936
		picture = GFX_my_equipment_medium

		is_archetype = yes
		is_buildable = no

		type = motorized
		group_by = archetype

		interface_category = interface_category_land

		upgrades = {
			tank_reliability_upgrade
		}
	}

	#Specific equipment model
	my_equipment_1 = {
		year=1936
		active = yes # no requires technology activation, yes will be available at the start
		priority=20

		archetype = my_equipment_archetype
		parent = my_equipment_0
		picture = GFX_my_equipment_1_medium

		can_convert_from = {
			my_equipment_0
		}

		#Basic attributes
		reliability=0.8
		maximum_speed = 12

		# Defense attributes
		defense = 4
		breakthrough=12
		hardness = 0.1
		armor_value = 0.5

		# Offensive attributes
		soft_attack = 30
		hard_attack = 25
		ap_attack = 30
		air_attack = 5
# Others
		lend_lease_cost = 1
		build_cost_ic = 22

		resources = {
			steel=1
			oil=1
			tungsten = 1
			chromium=1
			aluminum = 1
			rubber=1
		}
	}

}
```

## Production interface classification

| `interface_category` | Description |
|------|------|
| `interface_category_land` | Army equipment |
| `interface_category_armor` | Tank/Armor |
| `interface_category_capital_ships` | Capital ships |
| `interface_category_screen_ships` | Screen Guard Ships |
| `interface_category_other_ships` | Other ships |
| `interface_category_air` | Aircraft |

## Common field descriptions

| Field | Description |
|------|------|
| `year` | Equipment year |
| `is_archetype` | Whether it is a prototype |
| `is_buildable` | Whether it is buildable |
| `type` | Applicable unit type |
| `group_by` | Grouping method |
| `active` | Whether the start is activated |
| `priority` | Production priority |
| `archetype` | Belonging to the prototype |
| `parent` | Parent equipment |
| `can_convert_from` | Can convert source |
| `reliability` | reliability |
| `maximum_speed` | Maximum speed |
| `defense` | defense |
| `breakthrough` | breakthrough |
| `hardness` | Armor rate |
| `armor_value` | Armor thickness |
| `soft_attack` | Soft attack |
| `hard_attack` | Hard attack |
| `ap_attack` | Armor-piercing |
| `air_attack` | Against the air |
| `lend_lease_cost` | Lease transport ship consumption |
| `build_cost_ic` | Cost |
| `resources` | Resource consumption |
| `upgrades` | Available upgrade slots |
