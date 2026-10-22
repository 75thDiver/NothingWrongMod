# Technology sharing group template

File：`common/technology_sharing/<xxx>.txt`

```pdx
technology_sharing_group = {
	id = TAG_research_circle
	name = TAG_research_circle_name
	desc = TAG_research_circle_desc
	picture = GFX_technology_sharing_default

	research_sharing_per_country_bonus = 0.1

	available = {
		is_in_faction_with = TAG
		# or autonomy / flag condition
	}
}
```

## Effect side join/leave

```pdx
add_to_tech_sharing_group = TAG_research_circle
remove_from_tech_sharing_group = TAG_research_circle
```

（The effect name is based on wiki **Effects** / the Vanilla, if the version is used `join_technology_sharing` etc. shall prevail. )

## Key Points

- `research_sharing_per_country_bonus`：Shared bonus provided by each additional country  
- `available`：Can a country be in this group?
- Original modes such as camp research circle and Commonwealth can be directly compared

## Related

- `technology-file-template.md` / `effects-template.md` / `faction-system-template.md`
