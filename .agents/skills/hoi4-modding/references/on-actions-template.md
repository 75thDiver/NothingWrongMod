#On Actions Template

`on_actions` Executes effects (war, annexation, control change, daily, etc.) when the game's **specific hook** is triggered. The file is located in `common/on_actions/`.

## File location

`common/on_actions/<xxx>.txt`

## Basic structure

```pdx
on_actions = {
	on_startup = {
		effect = {
			# When the game loads/starts
		}
	}

	on_daily = {
		effect = {
			# Pay attention to performance: run on all related objects every day
		}
	}

	on_state_control_changed = {
		effect = {
			# ROOT / FROM / FROM.FROM The meaning is as follows and the original comments
		}
	}
}
```

The same `on_actions = { }` can write multiple hooks; multiple files will **merge** the effects under the same hook (don't assume that only your own file is running).

## Scope convention (be sure to check the vanilla)

`ROOT` / `FROM` are different for different hooks. Before writing, open the comments at the top of the ontology `common/on_actions/00_on_actions.txt` and other files.

Common (**may change with the version, the vanilla shall prevail**):

| hook | common ROOT | common FROM |
|------|-----------|-----------|
| `on_startup` | Special/global context | — |
| `on_daily` / `on_weekly` / `on_monthly` | Country (by country) | — |
| `on_declare_war` | Declaring country | Declared country |
| `on_war_relation_added` | one side | the other side |
| `on_capitulation` | Surrendering country | Accept surrender/related parties (check vanilla) |
| `on_annex` | annexer | annexed |
| `on_puppet` | puppet | suzerain or opposite (check vanilla) |
| `on_subject_free` | Former vassal | Former overlord |
| `on_government_change` | The country | — |
| `on_ruling_party_change` | The country | — |
| `on_coup_succeeded` | The country | — |
| `on_state_control_changed` | New controller | Old controller; `FROM.FROM` is always state |
| `on_peaceconference_started` | Relevant countries | Check vanilla |
| `on_peaceconference_ended` | Relevant countries | Check vanilla |
| `on_join_faction` | Joining country | Alliance leader, etc. |
| `on_leave_faction` | Leave country | — |
| `on_civil_war_end` | The winning side and others | Check the vanilla |
| `on_unit_leader_created` | Country/General context | Check vanilla |
| `on_operative_recruited` | Country | Check vanilla |
**It is forbidden to write the meaning of FROM from memory**; indicate in the comments who the ROOT/FROM of this hook is.

## Writing mode

```pdx
on_actions = {
	on_state_control_changed = {
		effect = {
			if = {
				limit = {
					FROM.FROM = { state = 219 } # Moscow, etc.: subject to actual state
					FROM = { original_tag = RSC }
					ROOT = { original_tag = RYH }
				}
				# Specific effects: flag / event / script effect
				RYH = {
					country_event = { id = RYH_story.10 hours = 6 }
				}
			}
		}
	}

	on_startup = {
		effect = {
			if = {
				limit = {
					has_dlc = "Gotterdammerung"
				}
				# DLC conditional buildings, etc.
			}
		}
	}

	on_daily_TAG = {
		# Some versions support daily optimized by tag; if not, on_daily + limit tag
		effect = {
			if = {
				limit = { tag = RYH }
				#Daily logic
			}
		}
	}
}
```

Whether there is such a key as `on_daily_TAG` shall be subject to the **current version of the original file**.

## Performance

- Avoid double `every_country` / `every_state` without `limit` within `on_daily` / `on_weekly`
- can flag the door latch: `has_country_flag` leave early
- Use `country_event` to distribute heavy logic to events instead of calculating everything every day
- Delete the refresh log after debugging
## Division of work with events and scripted_effect

| Means | Suitable |
|------|------|
| `on_actions` | System-level hooks, world rules that will be triggered across mods |
| `country_event` + `trigger` | optional mean_time / optional narrative |
| `is_triggered_only` event | Triggered by national focus/decision/on_action roll call |
| `scripted_effect` | An effect body that reuses hooks and national focuses |

```pdx
on_annex = {
	effect = {
		if = {
			limit = {
				tag=RYH
				FROM = { original_tag = RSC }
			}
			RYH_on_annex_rsc = yes # scripted_effect
		}
	}
}
```

## List of common hooks (extract, not exhaustive)

```
on_startup
on_daily
on_weekly
on_monthly
on_yearly
on_declare_war
on_war_relation_added
on_capitulation
on_uncapitulation
on_annex
on_puppet
on_subject_free
on_government_change
on_ruling_party_change
on_state_control_changed
on_peaceconference_started
on_peaceconference_ended
on_join_faction
on_leave_faction
on_civil_war_end
on_justifying_wargoal_pulse
on_wargoal_expire
on_liberated
on_release_as_puppet
on_release_as_free
on_unit_leader_level_up
on_operative_detected_during_operation
```
Full list: Ontology `common/on_actions/` All file names and contents + wiki **On actions**.

## Specification

- Write a clear limit for each `if` to avoid affecting all countries.
- Comments indicate ROOT/FROM
- Do not create an infinite loop in on_action (A annexation triggers annexation again)
- Prioritize `country_event`/`news_event` delay hours when connecting with news/narrative

## Query order

1. This page
2. Ontology `common/on_actions/00_on_actions.txt` and other hooks with the same name
3. wiki: **On actions**
4. Ask the user

## Related documents

- `scopes-template.md` / `effects-template.md` / `scripted-effects-template.md` / `event-template.md`
