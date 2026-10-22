> This article summarizes the original cabinet advisor slots and common features of HOI4.

# Advisor and Cabinet feature templates

## General structure

```pdx
advisor = {
	cost = 100
	slot = political_advisor
	idea_token = my_advisor
	allowed = {
		original_tag = TAG
	}
	traits = {
		silent_workhorse
	}
	ai_will_do = {
		factor = 1
	}
}
```

## slot

| Slot | Description |
|------|------|
| `theorist` | theorist |
| `high_command` | Commander-in-Chief (Army) |
| `navy_command` | Commander-in-Chief of the Navy |
| `air_command` | Commander-in-Chief of the Air Force |
| `army_chief` | Secretary of the Army |
| `navy_chief` | Secretary of the Navy |
| `air_chief` | Secretary of the Air Force |
| `political_advisor` | Political Advisor |

## theorist

| Features | Effects |
|------|------|
| `military_theorist` | Army doctrine cost -10% |
| `air_warfare_theorist` | Air doctrine cost -10% |
| `naval_theorist` | Naval doctrine cost -10% |
| `mobile_warfare_expert` | Mobile warfare doctrine cost -15% |
| `blitzkrieg_theorist` | Maneuver combat doctrine -15%, armor technology maximum speed +10% |
| `superior_firepower_expert` | Superior firepower theory -15% |
| `grand_battle_plan_expert` | Grand Battle Plan Doctrine -10% |
| `mass_assault_expert` | Mass Assault Doctrine -15% |
| `submarine_specialist` | Trade blockade doctrine -15% |
| `close_air_support_proponent` | Battlefield Support Doctrine -15% |
| `victory_through_airpower` | Strategic Destruction Doctrine -15% |
| `dive_bomber` | Close support aircraft ground attack +10% |
| `naval_aviation_pioneer` | Base strike doctrine -10% |
| `grand_fleet_proponent` | Fleet Doctrine of Existence -15% |
| `assault_avaition` | Continuous Combat Doctrine -10% |
| `nuclear_scientist` | Atomic energy research speed +15% |
| `rocket_scientist` | Rocket research speed +15% |
## Commander-in-Chief (high_command / navy_command / air_command)

### Commander-in-Chief of the Army

| Features | Effects |
|------|------|
| `army_regrouping_1/2/3` | Army organization recovery +4/8/10% |
| `army_cavalry_1/2/3` | Cavalry attack/defense +5/10/15% |
| `army_infantry_1/2/3` | Army experience gain +0.06/0.09/0.12, infantry attack +5/10/15%, defense +10/15/20% |
| `army_logistics_1/2/3` | Army experience gain +0.06/0.09/0.12, army attrition -4/8/12% |
| `army_entrenchment_1/2/3` | Army experience gain +0.06/0.09/0.12, trench speed +8/16/24% |
| `army_armored_1/2/3` | Army experience gain +0.06/0.09/0.12, armor attack/defense +5/10/15% |
| `army_commando_1/2/3` | Army experience gain +0.06/0.09/0.12, special attack/defense +10/15/20% |
| `navy_amphibious_assault_1/2/3` | Amphibious landing speed +5/10/15% |
| `army_CombinedArms_1/2/3` | Motorcycle/Motorcycle Attack/Defense +5/10/15% |
| `army_artillery_1/2/3` | Army experience gain +0.06/0.09/0.12, artillery attack +10/15/20%, defense +5/10/15% |
| `army_concealment_1/2/3` | Enemy air support -5/10/15% |

### Commander-in-Chief of the Navy

| Features | Effects |
|------|------|
| `navy_fleet_logistics_1/2/3` | Naval experience gain +0.06/0.09/0.12, maximum naval range +5/10/15% |
| `air_naval_strike_1/2/3` | Sea attack/aiming/mobility +2/3/5% |
| `navy_carrier_1/2/3` | Attack efficiency +10/15/20% |
| `navy_capital_ship_1/2/3` | Naval experience gain +0.06/0.09/0.12, capital ship attack/armor +5/10/15% |
| `navy_submarine_1/2/3` | Submarine attack +10/15/20%, defense +5/10/15% |
| `navy_naval_air_defense_1/2/3` | Naval experience gain +0.06/0.09/0.12, naval air attack +8/15/20% |
| `navy_screen_1/2/3` | Naval experience gain +0.06/0.09/0.12, screen guard attack +5/10/15%, defense +10/15/20% |
| `navy_anti_submarine_1/2/3` | Submarine detection +10/15/20% |
### Commander-in-Chief of the Air Force

| Features | Effects |
|------|------|
| `air_bomber_interception_1/2/3` | Air force experience gain +0.06/0.09/0.12, interception mission attack/defense/maneuver +2/3/5% |
| `air_air_combat_training_1/2/3` | Air force experience growth +0.06/0.09/0.12, ace generation probability +5/10/15% |
| `air_close_air_support_1/2/3` | Air force experience gain +0.06/0.09/0.12, CAS attack/defense/maneuver +2/3/5% |
| `air_tactical_bombing_1/2/3` | Ground support +15% |
| `air_strategic_bombing_1/2/3` | Air force experience gain +0.06/0.09/0.12, strategic bombing +3/5/7%, bombing attack/defense/maneuver +1/2/3% |
| `air_air_superiority_1/2/3` | Air force experience growth +0.06/0.09/0.12, seizing air superiority attack/defense/maneuver +2/3/5% |
| `air_airborne_1/2/3` | Airdrop mission attack +1/2/3, defense +3/5/7, maneuver +3/5/7 |
| `air_pilot_training_1/2/3` | Air Force Training Experience Increase +15% |

## Minister (army_chief / navy_chief / air_chief)

### Secretary of the Army

| Features | Effects |
|------|------|
| `army_chief_offensive_1/2/3` | Army experience gain +0.06/0.09/0.12, unit attack +5/10/15% |
| `army_chief_entrenchment_1/2/3` | Army experience growth +0.06/0.09/0.12, mobilization speed -2/4/6%, trench limit +3/5/7 |
| `army_chief_reform_1/2/3` | Army experience gain +0.12/0.16/0.20 |
| `army_chief_planning_1/2/3` | Army experience gain +0.06/0.09/0.12, planning speed +5/10/15% |
| `army_chief_defensive_1/2/3` | Army experience gain +0.06/0.09/0.12, unit defense +5/10/15% |
| `army_chief_maneuver_1/2/3` | Army experience gain +0.06/0.09/0.12, army speed +5/10/15% |
| `army_chief_organizational_1/2/3` | Army experience growth +0.06/0.09/0.12, Army organization +4/8/12% |
| `army_chief_morale_1/2/3` | Army experience gain +0.06/0.09/0.12, non-combat supply depletion penalty -3/6/9% |
| `army_chief_drill_1/2/3` | Army experience gain +0.06/0.09/0.12, Army division training time -5/10/15% |
### Secretary of the Navy

| Features | Effects |
|------|------|
| `navy_chief_naval_aviation_1/2/3` | Naval experience growth +0.06/0.09/0.12, aircraft carrier aircraft attack/defense/maneuver +3/6/10 / +3/7/12 / +4/8/15 |
| `navy_chief_decisive_battle_1/2/3` | Naval experience growth +0.06/0.09/0.12, battleship/screen guard attack/defense +5/10/15% |
| `navy_chief_reform_1/2/3` | Naval experience growth +0.1/0.3/0.5, naval experience growth +5/10/15% |
| `navy_chief_commerce_raiding_1/2/3` | Naval experience gain +0.06/0.09/0.12, attack transport ship mission efficiency +10/15/20% |
| `navy_chief_maneuver_1/2/3` | Naval experience gain +0.06/0.09/0.12, naval speed +5/10/15% |

### Secretary of the Air Force

| Features | Effects |
|------|------|
| `air_chief_safety_1/2/3` | Air Force experience gain +0.06/0.09/0.12, Air Force accident probability -5/10/15% |
| `air_chief_ground_support_1/2/3` | Air force experience gain +0.06/0.09/0.12, air superiority +5/10/15% |
| `air_chief_night_operations_1/2/3` | Night operation penalty -10/20/30% |
| `air_chief_reform_1/2/3` | Air force experience gain +0.12/0.16/0.20 |
| `air_chief_all_weather_1/2/3` | Air Force experience gain +0.12/0.16/0.20, Air Force bad weather penalty -10/20/30% |
| `air_chief_old_guard` | Air force experience gain +0.3, maximum command power +10 |
## Political Advisor (political_advisor)

| Features | Effects |
|------|------|
| `ideological_crusader` | Party support modifies stability by +10%, monthly relationship with the same ideology +100% |
| `head_of_intelligence` | Agent position +1, intelligence agency upgrade time -15% |
| `fortification_engineer` | Land fortification/coast fort/air defense position construction speed +20% |
| `armaments_organizer` | Civilian-to-army consumption -20%, supply center construction speed +10% |
| `silent_workhorse` | Political power +15% |
| `popular_figurehead` | Stability +15% |
| `education_reformer` | Research speed +5% |
| `financial_expert` | Consumer goods factory -5% |
| `war_industrialist` | Military factory/naval dock/oil tank construction speed +10% |
| `captain_of_industry` | Infrastructure/Civil Factory/Railway/Synthetic Refinery Construction Speed +10% |
| `compassionate_gentleman` | Improve relations +15%, damage to garrison -15% |
| `fascist_demagogue` | Fascism daily approval rating +0.10 |
| `democratic_reformer` | Democratic daily approval rating +0.10 |
| `smooth_talking_charmer` | Improved relationship cost -50%, trade agreement relationship modifier +10% |
| `anti_communist_crusader` | Stability +5%, fascism daily support -0.10 |
| `editor` | Political power +5%, stability +5% |
| `economist` | Maximum productivity +5% |
| `prince_of_terror` | Non-core manpower +2%, foreign subversion efficiency -30%, damage to garrison -25% |
| `backroom_backstabber` | Resistance to ideological change +25%, subversive activity cost -25% |
| `first_lady` | Stability +5%, war support +5% |
| `economic_organizer` | Stability +5%, consumer goods factory -5% |
| `quartermaster_general` | Air force base/naval base/radar station/nuclear reactor/rocket base construction speed +15% |
| `mastermind_code_cracker` | Cracking ability +15% |
| `socialist_novelist` | War support +10%, socialist daily support +0.10 |
| `red_suffragette` | Serviceable population +2%, stability -10% |
| `hawk` | War support +10%, stability -5% |
| `appeaser` | Stability +10%, war support -5% |
| `national_integralist` | Political power +15%, weekly stability +0.10% |
| `technocrat` | Scientific research speed +5%, civilian factory construction speed +5% |
| `anti_fascist_agent` | Stability +10%, fascism daily support -0.02 |
| `connected_citizen` | Political power +5%, stability +5% |
| `liberal_journalist` | Political power +5%, Democratic daily support +0.05 |
| `political_commissar` | Maximum command power +30, daily communist support +0.10, political power +5 |
| `iron_lazar` | Train reliability +15%, train construction cost +5%, oil conversion efficiency +5%, supply center/rail construction speed +5% |
| `head_of_the_nkvd_yezhov_initial` | Stability -5%, intelligence network strength growth rate +10%, enemy agent discovery probability offset +0.10, enemy agent arrest probability +15%, leakage of civil affairs intelligence -10% |
