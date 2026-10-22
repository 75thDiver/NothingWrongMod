# Overview of doctrine system (Grand/Track/Subdoctrine)

New doctrinal structures (after NCNS etc.) see ontology `common/doctrines/_documentation.md`.
Use `subdoctrine-template.md` to write details of subdoctrine; check `data/doctrine-list.md` for ID.

## Concept

| Concept | Meaning |
|------|------|
| Folder | Land/Sea/Air Doctrine Page |
| Grand Doctrine | Page mutually exclusive root doctrine, cost XP to unlock |
| Track | Track into which subdoctrine can be inserted |
| Subdoctrine | Mount the branch of track |
| Mastery | Track Mastery Progression |
| Reward / Milestone | Mastery Reward |

## Directory

```
common/doctrines/
  folders/
  grand_doctrines/
  tracks/
  subdoctrines/
  _documentation.md
```

## Effects and conditions (document excerpt)

Effects: `set_grand_doctrine`, `set_sub_doctrine`, `add_mastery`, `add_daily_mastery`, `add_mastery_bonus`
Conditions: `has_doctrine`, `has_completed_subdoctrine`, `has_completed_track`, `has_subdoctrine_in_track`, `has_mastery`…

Correction example:

```pdx
land_doctrine_cost_factor = -0.15
land_track_mastery_gain_factor = 0.15
```

## When writing mod

1. Give priority to inserting compatible sub-doctrines into the original track (if the design allows)
2. New grand/track requires complete UI/GFX/localization
3. AI `ai_will_do` and XP economic test
4. The versions of the old single doctrine tree are quite different—subject to the current ontology document.
## Related

- `subdoctrine-template.md` / `data/doctrine-list.md` / `effects-template.md` / `modifiers-index-template.md`
