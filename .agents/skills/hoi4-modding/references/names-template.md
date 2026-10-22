# Name pool and division number template

## Pilot/Agent name pool

File: `common/names/00_names.txt` (can be appended by mod)

```pdx
default = {
	male = {
		names = { "John" "Bob" }
		surnames = { }
		callsigns = { }
	}
	surnames = { "Smith" "Jones" }
	callsigns = { "Easy Kill" "The Lightning" }
	prefix = o_operation
	operation = {
		0 = { o_default_operation }
	}
	use_geographical_default_operation_names = yes
}

GER = {
	male = {
		names = { "Hans" "Fritz" }
	}
	surnames = { "Müller" "Schmidt" }
	# callsigns / operation sub-pool optional
}
```

- Override `default` by **tag**
- Names can be written separately for men and women; surnames can be shared
- Operation plan name `operation` is a molecular pool based on strategic area id; `0` is a general pool
- Localization: `o_operation`, specific operation key

## Division names (division names)

Directory: `common/units/names_divisions/`

```pdx
TAG_INF_01 = {
	name = "Infantry Division"

	for_countries = {TAG}

	can_use = { always = yes }

	division_types = { "infantry" }
fallback_name = "%d Infantry Division"

	ordered = {
		1 = { "%d Infantry Division" }
		2 = { "%d Infantry Division" }
		3 = { "Special Name Division" }
	}
}
```

| Field | Description |
|------|------|
| `for_countries` | applicable tag |
| `can_use` | Additional conditions |
| `division_types` | Corresponds to `sub_units` type key |
| `fallback_name` | The pattern after the sequence number is exhausted, `%d` is a number |
| `ordered` | Historical number list |

Different arms of land, sea and air have different name groups; ships also have a `names_ships` directory (based on the ontology `common/units/`).

## Equipment display name

Equipment localization is in `localisation`, the key is related to the equipment definition; country-specific weapon names can be localized in the country or overridden in the equipment related yml.  
Don't just write the device name in the names file.

## Military History Entries

Some mods use scripted loc/history archives to show "X Division was involved in..."; there is no unified mandatory path. If necessary, compare the library's "Military History Entry Template" with the existing implementation of the project.

## Specification

- Chinese project: The localization style of the serial number is consistent with the original Chinese ("%s Infantry Division", etc., check the original yml)
- `division_types` must be real sub unit names
- UTF-8 BOM is written as yml; the txt encoding of names is consistent with the project

## Related

- `unit-template.md` / `oob-template.md` / `localisation-syntax-template.md` / `character-template.md`
