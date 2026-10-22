# Faction System Template (Faction System)



New mechanics based on HOI4 1.15+ faction system. All files are placed in the corresponding directories under `common/`.



## File layout



```

common/

  factions/ # Faction system root directory

    templates/ # Camp templates

      <template>.txt

    goals/ # Faction goals / Faction charter

      <goals>.txt

    rules/ # Faction rules

      <rules>.txt

    rule_groups/ # Rule group

      <rule_groups>.txt

    member_upgrades/ # Member upgrade (single level)

      <upgrades>.txt

    member_upgrade_groups/ # Member upgrade group

      <upgrade_groups>.txt

    icons/ # Faction icon pool

      <pool>.txt

  collections/ # scripted collections (for ratio_progress)

    <collections>.txt

  ai_strategy/ # AI cost FI / intelligence advisory strategy

    <strategy>.txt

```



---



## 1. Faction Template



`common/factions/templates/<your_template>.txt`
```yaml

faction_template_<id> = { # Template ID

    name = <loc_key> # Faction name localization key

    icon = GFX_faction_icon_<id> # Faction icon

    manifest = <manifest_id> # Faction charter target ID



    visible = { # Whether to display in the list when created

        # ROOT = the country where the faction was created

    }



    available = { # Is it optional?

        # ROOT = the country where the faction was created

    }



    can_leader_join_other_factions = yes # Can the leader join other factions (it will disband the old faction and recruit members)



    goals = { # Initial goal list

        <goal_id_1>

        <goal_id_2>

    }



    default_rules = { # Rules enabled by default (will override the default rules in the rule group)

        <rule_id_1>

        <rule_id_2>

    }

}

```



**Recommended effects for creating a faction**:

```yaml

create_faction_from_template = {

    template = <template_id>

    # name = <loc_key> # Optional: override template name

    # icon = GFX_<icon_id> # Optional: override template icon
}

```



---



## 2. Faction Goal



`common/factions/goals/<your_goals>.txt`



General goals (short term/medium term/long term):



```yaml

<goal_id> = {

    name = <loc_key> # target name

    description = <loc_key> # Target description

    category = short_term # short_term / medium_term / long_term

    group = FOCUS_FILTER_INTERNAL_AFFAIRS # UI filter grouping



    visible = { # Whether to display in the selection list

        # ROOT = faction leader, FROM = view member countries of this target

    }



    available = { # Is it optional?

        # ROOT = faction leader, FROM = member country

    }



    completed = { # Completion condition; if left blank, it will never be completed.

        # ROOT = Faction Leader

    }



    auto_complete = yes # Automatically complete when the progress reaches 100%



    ai_will_do = { # Leader AI selects the weight of the target

        factor = 200

        # scope = member country

    }
complete_effect = { # Execute once when complete

        # ROOT = Faction Leader

    }



    cancel = { # Whether the target should be removed from the faction

        # ROOT = Faction Leader

    }



    cancel_effect = { # Execute once when canceling

        # ROOT = Faction Leader

    }



    select_effect = { # Execute once when selected (only after the game starts)

        # ROOT = Faction Leader

    }



    remove_effect = { # Execute once when removing (only after the game starts)

        # ROOT = Faction Leader

    }

}

```



### 2.1 Progress system (optional, for continuous goals)



```yaml

<goal_id> = {

    # ...basic fields ...



    progress = {

        progress_sections = {

            <section_loc> = {

                min = 0.1 # phase start (0.1 = 10%)

                max = 0.5 #End of stage

                modifier = { # Modifier given when the stage takes effect

                    drift_defence_factor = 0.1

                }
rule = <rule_id> # Rules applied when the stage takes effect

            }

        }

    }

}

```



### 2.2 Ratio progress (ratio_progress)



```yaml

<goal_id> = {

    # ...basic fields ...



    ratio_progress = {

        # Choose one: collection or fixed value/variable

        total_amount_collection = game:all_countries

        completed_amount_collection = democratic_countries



        # total_amount = 8

        # completed_amount = <variable>



        range = { min = 0.1 max = 0.8 } # Ratio mapped to the range of progress



        scale = { # Correction given according to the satisfaction ratio

            trade_opinion_factor = 0.25

            stability_factor = 0.15

        }



        reversed = { # Reverse correction according to the unsatisfied proportion

            stability_factor = -0.15

        }



        progress_sections = {

            manifest_fulfilled = {

                min=0.75
modifier = {

                    drift_defence_factor = 0.15

                }

            }

        }

    }

}

```



**Note**: `scripted collections` are defined in `common/collections/<your_collections>.txt`.



---



## 3. Faction Manifest



Essentially a faction target with `is_manifest = yes`.



```yaml

<manifest_id> = {

    name = <loc_key>

    description = <loc_key>

    is_manifest = yes # mark as charter



    ratio_progress = {

        total_amount = 8

        completed_amount_collection = collection:<collection_id>



        scale = {

            trade_opinion_factor = 0.25

            faction_trade_opinion_factor = 0.50

            stability_factor = 0.15

        }



        reversed = {

            stability_factor = -0.15

        }



        progress_sections = {
manifest_fulfilled = {

                min=0.75

                modifier = {

                    drift_defence_factor = 0.15

                }

            }

        }

    }

}

```



---



## 4. Faction Rules



`common/factions/rules/<your_rules>.txt`



```yaml

<rule_id> = {

    type = <type_token> # Rule type, see the table below



    visible = { # Whether to display in the rule list

        # ROOT = Faction Leader

    }



    available = { # Is it available to factions?

        # ROOT = Faction Leader

    }



    can_remove = { # Whether it can be removed after taking effect

        # ROOT = Faction Leader

    }



    trigger = { #actual judgment condition of the rule

        # Scope depends on type

    }



    modifier = { # Global modifier obtained after enabling the rule

        political_power_factor = -0.1

    }



    peace_action_modifiers = { # Only type = peace_conference_rules takes effect
<cost_modifier_id>

    }



    ai_will_do = { # AI selects the weight of this rule

        base=0

        modifier = { add = 2 }

        # ROOT = Faction Leader

    }

}

```



### 4.1 Special types and scopes



| type | scope (ROOT) | source scope (FROM) | description |

|------|--------------|----------------|------|

| `joining_rule` | Countries applying to join | Faction leaders | Who can join a faction |

| `war_declaration_rule` | Declaring country | Declared target | Who can declare war |

| `call_to_war_rule` | The country calling for war | The target of the call | Who can draw people to war |

| `member_rules` | Faction leader | None | Can member become a government-in-exile |

| `change_leader_rules` | The country to be the leader | None | Who can be the new leader |

| `peace_conference_rules` | Faction leaders | None | List of peace conference modifiers |



---



## 5. Faction Rule Groups



`common/factions/rule_groups/<your_groups>.txt`



```yaml

<group_id> = { # Group ID, also a localization key

    default_rule = <rule_id> # Default enabled rules

    rules = {
<rule_id_1>

        <rule_id_2>

        # You can define rules directly inline or reference rules in DB

    }

}

```



---



## 6. Faction Member Upgrades



### 6.1 Single upgrade level



`common/factions/member_upgrades/<your_upgrades>.txt`



```yaml

<upgrade_id> = {

    name = <loc_key> # Override the upgrade group name

    desc = <loc_key> # Override upgrade group description

    icon = GFX_<icon_id> # Override the upgrade group icon

    upgrade_cost = 50 # Replace the FI required for this upgrade

    bonus = 0.05 # Bonus value, meaning depends on upgrade_type

}

```



### 6.2 Upgrade Group



`common/factions/member_upgrade_groups/<your_groups>.txt`



```yaml

<upgrade_group_id> = {

    name = <loc_key>

    desc = <loc_key>

    icon = GFX_<icon_id>



    upgrade_type = faction_member_upgrade_manpower # See supported types below



    default_upgrade = <upgrade_id> #Default level
upgrades = { # Level list, sorted by bonus

        <upgrade_id_1>

        <upgrade_id_2>

        <upgrade_id_3>

    }

}

```



### 6.3 Currently known supported upgrade_types



- `faction_member_upgrade_manpower`: Inject national manpower into the faction manpower pool in proportion to `bonus`.



---



## 7. Faction icon pool



`common/factions/icons/<your_pool>.txt`



```yaml

faction_icon_pool = { # Fixed ID faction_icon_pool

    icons = {

        GFX_faction_logo_generic_democratic

        GFX_faction_logo_generic_fascist

        GFX_faction_logo_generic

        # More icons...

    }

}

```



**Note**: If a camp template does not define `icon`, it will be randomly selected from the pool.



---



## 8. Quick check on related effects, triggers and modifiers



### 8.1 Effects



- `create_faction` — Templateless creation of factions (deprecated)

- `create_faction_from_template` — Recommended way

- `dismantle_faction` — disband a faction

- `set_faction_leader` — change the leader

- `set_faction_spymaster` — change the spy master
- `set_faction_name` — change name

- `add_to_faction` — add countries

- `remove_from_faction` — remove country

- `leave_faction` — current country leaves

- `set_faction_rule` — set rules

- `set_faction_manifest` — change the charter

- `add_faction_goal` — add a goal

- `remove_faction_goal` — remove goal

- `add_faction_initiative` — add FI

- `add_faction_power_projection` — increase influence

- `add_faction_influence_score` — Increase the influence score of a country

- `add_faction_influence_ratio` — Increase the influence of a country proportionally



### 8.2 Triggers



- `faction_manifest_fulfillment` — Compare charter completion

- `has_faction_template` — Whether in the template faction

- `faction_power_projection` — Compare faction influence

- `faction_influence_score` — Compare a country’s influence score

- `faction_influence_ratio` — Compare the influence ratio of a certain country

- `faction_influence_rank` — Compare the influence ranking of a country

- `has_faction_goal` — whether there is an active/completed goal

- `has_completed_faction_goal` — Whether a goal has been completed

- `faction_goal_fulfillment` — the degree of completion of a certain goal

- `has_manpower_to_become_leader` — Whether deployed manpower exceeds the leader and his vassals
- `has_industry_to_become_leader` — Whether the number of factories exceeds the leader



### 8.3 Modifiers



- `faction_influence_war_score_factor`

- `faction_influence_industrial_capacity_factor`

- `faction_influence_garrison_support_provider_factor`

- `faction_influence_garrison_support_reciver_factor`

- `faction_influence_expeditionary_force_provider_factor`

- `faction_influence_expeditionary_force_reciver_factor`



---



## 9. Defines and console



### 9.1 Defines



Override in `common/defines/<your_defines>.txt`:



```yaml

NFactions = {

    FACTION_INITIATIVE_CHANGE_RULE_COST = 25 # Modify the FI consumed by the rule

}

```



### 9.2 Console



```

faction_initiative

f

```



---



## 10. AI spending FI strategy



`common/ai_strategy/<your_strategy>.txt`



```yaml

<strategy_id> = {

    enable = { always = yes }

    abort_when_not_enabled = yes
ai_strategy = {

        type = spent_faction_initiative_priority

        id = program # program / unlock_doctrine_sharing / unlock_faction_commander

        value=5

    }

}

```



Intelligence Advisor Strategy (requires La Resistance):



```yaml

<strategy_id> = {

    allowed = { has_dlc = "La Resistance" }

    enable = { is_major = no }

    abort_when_not_enabled = yes

    ai_strategy = {

        type = become_spymaster # become_spymaster / become_head_of_crypto / become_head_of_counter_intel / become_head_of_operations

        value=2

    }

}

```



---



## 11. Common pitfalls



1. **Goal completion condition cannot be left blank**: `completed = {}` will cause the goal to never be completed.

2. In **ratio_progress`, `total_amount` and `total_amount_collection` are mutually exclusive**, and `completed_amount` and `completed_amount_collection` are mutually exclusive.

3. **Rules `available` / `can_remove` do not prevent rules from being set or removed via effects**, just control the UI.
4. **The `trigger` scope of the rule depends on the `type`**, don’t get confused.

5. **Scope of camp target**:

   - `visible` / `available`: `ROOT = leader`, `FROM = member`

   - `completed` / `complete_effect` / `cancel` / `cancel_effect`: `ROOT = leader`

6. **Scripted collections** are used for `ratio_progress` and need to be defined separately in `common/collections/`.

7. **`default_rules` in the camp template will override the default rules defined in the rule group**.

8. **The `upgrades` in the member upgrade group will be automatically sorted by `bonus`, so the order is not important.

9. **The icon pool ID is fixed to `faction_icon_pool`** and is not named arbitrarily.

10. **`create_faction` has been deprecated**, please use `create_faction_from_template` for new content.



---



## 12. Minimal runnable example



```yaml

# common/factions/templates/my_faction.txt

faction_template_my_pact = {

    name = MY_PACT_NAME

    icon = GFX_faction_icon_my_pact

    manifest = manifest_my_pact

    goals = {

        goal_defend_frontier

    }

    default_rules = {

        joining_rule_non_fascist
    }

}



# common/factions/goals/my_faction.txt

manifest_my_pact = {

    name = MANIFEST_MY_PACT

    description = MANIFEST_MY_PACT_DESC

    is_manifest = yes

    ratio_progress = {

        total_amount = 5

        completed_amount_collection = collection:my_pact_members

        scale = {

            stability_factor = 0.10

        }

        reversed = {

            stability_factor = -0.10

        }

    }

}



goal_defend_frontier = {

    name = GOAL_DEFEND_FRONTIER

    description = GOAL_DEFEND_FRONTIER_DESC

    category = short_term

    group = FOCUS_FILTER_WAR

    completed = {

        ROOT = { has_war = yes }

    }

    complete_effect = {

        add_faction_initiative = { value = 50 }

    }

}



# common/collections/my_faction.txt

collection:my_pact_members = {

    countries = {

        is_in_faction_with = ROOT

        OR = {

            tag = TAG_A

            tag = TAG_B

        }

    }

}

```

