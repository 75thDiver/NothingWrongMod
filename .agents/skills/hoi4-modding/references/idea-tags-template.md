# Idea classification slot (idea_tags) template

File: `common/idea_tags/00_idea.txt`
Define the **slot layout** on the political interface: ethos area, bill slots, advisor slots, manufacturer slots, etc.

```pdx
idea_categories = {
	hidden_ideas = {
		hidden = yes
		cost = 0
		removal_cost = -1
		ledger = hidden
	}

	country = {
		type = national_spirit
		cost = 0
		removal_cost = -1
		ledger = hidden
	}

	government = {
		slot = mobilization_laws
		slot = trade_laws
		slot = economy
		character_slot = political_advisor
		character_slot = political_advisor
		character_slot = political_advisor
		ledger = civilian
		cost = 150
		removal_cost = 0
	}

	research_production = {
		slot = tank_manufacturer
		# ...
		character_slot = theorist
		ledger = civilian
	}
}
```

## Key Points

| Concept | Description |
|------|------|
| `slot` | bill/manufacturer etc idea subtype slot |
| `character_slot` | Character advisor slot (corresponding to characters advisor `slot`) |
| `ledger` | Interface ledger: `army`/`navy`/`air`/`civilian`/`hidden`/`all`… |
| `type = national_spirit` | National spirit list area |
| `cost` / `removal_cost` | Default hiring/removal cost |

- Content mods generally **do not change** idea_tags, only insert ideas/characters into the original slots
- The total conversion needs to add "Fourth Act Slot/More Advisors" before changing this file
- Linked with `idea-template.md`, `character-template.md`, `mio-template.md`

## Related

- `idea-template.md` / `character-template.md` / `advisor-traits-template.md`
