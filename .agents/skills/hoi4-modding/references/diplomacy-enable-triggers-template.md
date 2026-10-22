# Diplomacy Enable Triggers

Override whether diplomatic actions are available via a scripted trigger with a specific name in `common/scripted_triggers/`.
The original comments can be found in the `00_diplo_action_valid_triggers.txt` file.

## Format

```pdx
# ROOT = originating country, FROM = target country
DIPLOMACY_WAR_ENABLE_TRIGGER = {
	if = {
		limit = {
			tag=GER
		}
		custom_trigger_tooltip = {
			tooltip = PREVENT_GER_WAR_ON_SOV
			FROM = {
				NOT = { tag = SOV }
			}
		}
	}
}
```

- The file must be in `common/scripted_triggers/`
- The trigger's **name is fixed** and cannot be changed to your favorite name.
- Recommend `if` + `custom_trigger_tooltip` to keep tooltip clear

## Common coverable actions (names are based on the ontology list)

Example (incomplete, copied from body notes/documents):

- `DIPLOMACY_WAR_ENABLE_TRIGGER` declares war
- `DIPLOMACY_OFFER_JOIN_FACTION_ENABLE_TRIGGER` invite to join the camp
- Several `DIPLOMACY_*_ENABLE_TRIGGER` related to guaranteed independence, military access, lease, puppet etc.

**Some buttons cannot be disabled** (community note: such as partial military pass give/take). Check the main body and library "Restricted Diplomacy Button" files before making changes.

## Design Notes

- This is a **global rule** that affects both AI and players
- Use flag as a switch to facilitate event switching of "Eternal Peace", etc.
- The tooltip must be localized and explain why it cannot be clicked.
- Do not write detection logic that is compatible with other mods (project specifications)
## with rules / ideology

Ideology `rules`, autonomy `rule`, and decrees will also be restricted to diplomacy; this mechanism is an additional hard switch. Prioritize using the narrative flag + this trigger to avoid fighting between the three places.

## Related

- `scripted-triggers-template.md` / `ideologies-template.md` / `autonomy-template.md` / `triggers-template.md`
