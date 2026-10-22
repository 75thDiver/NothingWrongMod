> References for province types and `modifier` commonly used modifier entries.

#Province type and national spirit modification

## Province type

| code | name | initial building slot |
|------|------|-----------|
| `megalopolis` | Metropolitan area | 12 |
| `metropolis` | Metropolitan area | 10 |
| `large_city` | Dense urban areas | 8 |
| `city` | urban area | 6 |
| `large_town` | Sparse town area | 5 |
| `town` | Developed rural areas | 4 |
| `rural` | rural areas | 2 |
| `small_island` | small island | 1 |
| `pastoral` | pastoral | 1 |
| `wasteland` | desert | 0 |
| `enclave` | enclave | 0 |
| `tiny_island` | Tiny island | 0 |

## Politics and Bills

| Correction | Explanation |
|------|------|
| `civilian_factory_use` | Determine the number of migrant workers to be temporarily used |
| `send_volunteer_divisions_required` | Minimum number of volunteer divisions to send |
| `generate_wargoal_tension` | Create the tension limit of war goal |
| `justify_war_goal_time` | The time required to justify the war goal |
| `join_faction_tension` | Join the faction tension |
| `surrender_limit` | Surrender limit |
| `mobilization_laws_cost_factor` | Conscription bill cost |
| `trade_laws_cost_factor` | Trade bill cost |
| `economy_cost_factor` | Economy bill cost |
| `political_advisor_cost_factor` | Political advisor cost |
| `tank_manufacturer_cost_factor` | Armor manufacturer cost |
| `naval_manufacturer_cost_factor` | Naval manufacturer cost |
| `aircraft_manufacturer_cost_factor` | Aircraft manufacturer cost |
| `materiel_manufacturer_cost_factor` | Munitions design cost |
| `industrial_concern_cost_factor` | Industrial enterprise costs |
| `theorist_cost_factor` | Theorist cost |
| `army_chief_cost_factor` | Army chief cost |
| `navy_chief_cost_factor` | Navy chief cost |
| `air_chief_cost_factor` | Secretary of the Air Force cost |
| `high_command_cost_factor` | Commander-in-chief cost |
## Trade and Diplomacy

| Correction | Explanation |
|------|------|
| `opinion_gain_monthly_factor` | Improve relationship evaluation |
| `improve_relations_maintain_cost_factor` | Improve relationship maintenance cost |
| `opinion_gain_monthly_same_ideology` | Same ideology monthly evaluation |
| `consumer_goods_factor` | Consumer goods |
| `consumer_goods_expected_value` | Expected basic consumer goods |
| `min_export` | Exportable resources |
| `trade_opinion_factor` | Trade influence coefficient |

## Resources

| Correction | Explanation |
|------|------|
| `state_resource_<Resource>` | Increased regional resources |
| `state_resource_cost_<Resource>` | Regional resource consumption |
| `state_resources_<Resource>_factor` | Regional resource increase rate |
| `state_resources_factor` | Locally available resources |
| `temporary_state_resource_<Resource>` | Additional regional resources added |
| `production_lack_of_resource_penalty_factor` | Lack of strategic resource penalty |
| `local_resources_factor` | Regional strategic resource acquisition rate |
| `local_resources` | Acquisition of regional strategic resources |
| `country_resource_<Resource>` | Country resources increased |
| `country_resource_cost_<Resource>` | National resource consumption |
| `resource_trade_cost_bonus_per_factory` | Trade additional resources per factory |
## Construction

| Correction | Explanation |
|------|------|
| `production_speed_buildings_factor` | Construction speed |
| `production_speed_nuclear_reactor_factor` | Nuclear reactor construction speed |
| `production_speed_arms_factory_factor` | Military factory construction speed |
| `production_speed_industrial_complex_factor` | Civilian factory construction speed |
| `production_speed_infrastructure_factor` | Infrastructure construction speed |
| `production_speed_synthetic_refinery_factor` | Chemical synthesis plant construction speed |
| `production_speed_dockyard_factor` | Naval dock construction speed |
| `production_speed_bunker_factor` | Bunker building speed |
| `conversion_cost_civ_to_mil_factor` | Cost of converting civilian workers into military industry |
| `local_building_slots_factor` | Regional maximum industrial value (for dynamic_modifier) |
| `global_building_slots_factor` | Maximum number of factories in a region |
| `local_building_slots` | Number of local building slots (for dynamic_modifier) |
| `global_building_slots` | Number of regional building slots |

## Political power/stability/war support

| Correction | Explanation |
|------|------|
| `political_power_factor` | Political point percentage |
| `political_power_gain` | Daily political point increase |
| `political_power_cost` | Daily political point consumption |
| `stability_factor` | Stability |
| `stability_weekly` | Weekly stability |
| `stability_weekly_factor` | Weekly stability growth |
| `defensive_war_stability_factor` | Defensive war stability correction |
| `offensive_war_stability_factor` | Offensive war stability modifier |
| `war_support_factor` | War support |
| `war_support_weekly` | Weekly war support growth |
| `command_power_gain` | Daily command point growth |
| `max_command_power` | Maximum command power |
| `command_power_gain_mult` | Daily command point growth percentage |
| `max_command_power_mult` | Maximum command point growth percentage |
## Ideology

| Correction | Explanation |
|------|------|
| `autonomy_gain` | Autonomy increases daily |
| `<ideology>_drift` | Ideology increases daily |

### Drift numerical ratio

In this mod, the `drift` value and actual effect are **1:1**. `drift = 0.01` in-game represents a daily change in ideological support of **0.01%**, not 1%.

- To increase the ideology by 0.01% per day, write `drift = 0.01`.
- To increase the ideology by 1% per day, write `drift = 1.0`.

## Army

| Correction | Explanation |
|------|------|
| `army_org_factor` | Army organization degree |
| `army_morale_factor` | Organizational recovery |
| `supply_consumption_factor` | Supply consumption |
| `no_supply_grace` | Number of accompanying supply hours |
| `org_loss_when_moving` | Army moving organization loss |
| `breakthrough_factor` | breakthrough |
| `recon_factor` | Army Reconnaissance |
| `land_reinforce_rate` | Reinforcement rate |
| `military_leader_cost_factor` | Commander recruitment cost |
| `army_leader_start_level` | Initial level of new army commander |
| `acclimatization_hot_climate_gain_factor` | Hot adaptation growth rate |
| `acclimatization_cold_climate_gain_factor` | Cold adaptation growth rate |
| `conscription` | Eligible population |
| `conscription_factor` | Serviceable population modifier |
| `non_core_manpower` | Non-core manpower |
| `monthly_population` | Monthly manpower percentage |
| `weekly_manpower` | Weekly manpower increase |
| `mobilization_speed` | Mobilization speed |
| `line_change_production_efficiency_factor` | Production efficiency maintenance |
| `production_factory_efficiency_gain_factor` | Production efficiency growth |
| `production_factory_max_efficiency_factor` | Production efficiency upper limit |
| `production_factory_start_efficiency_factor` | Basic production efficiency |
| `industrial_capacity_factory` | Factory output |
| `industrial_capacity_dockyard` | Dockyard output |
| `training_time_army_factor` | Training time |
| `army_infantry_attack_factor` | Infantry attack |
| `army_infantry_defence_factor` | Infantry defense |
| `motorized_attack_factor` | Motorized infantry attack |
| `motorized_defence_factor` | Motorized infantry defense |
| `mechanized_attack_factor` | Mechanized attack |
| `mechanized_defence_factor` | Mechanized defense |
| `army_artillery_attack_factor` | Artillery attack |
| `army_artillery_defence_factor` | Artillery defense |
| `army_armor_attack_factor` | Tank attack |
| `army_armor_defence_factor` | Tank defense |
| `army_core_attack_factor` | Army core attack |
| `army_core_defence_factor` | Army core defense |
| `army_attack_factor` | Army attack |
| `army_defence_factor` | Army Defense |
| `army_speed_factor` | Army division speed |
| `army_bonus_air_superiority_factor` | Army air superiority |
| `planning_speed` | Planning speed |
| `max_planning` | Maximum planning bonus |
| `max_planning_factor` | Planning bonus upper limit factor |
| `max_dig_in_factor` | Trench upper limit factor |
| `max_dig_in` | Maximum trench limit |
| `experience_loss_factor` | Experienced soldier loss |
| `experience_gain_army_factor` | Army experience gain |
| `army_fuel_consumption_factor` | Army fuel consumption |
## Navy

| Correction | Explanation |
|------|------|
| `navy_org` | Naval organization degree |
| `navy_screen_attack_factor` | Screen guard ship attack |
| `navy_screen_defence_factor` | Screen defense ship defense |
| `navy_capital_ship_attack_factor` | Capital ship attack |
| `naval_speed_factor` | Naval speed |
| `navy_max_range_factor` | Navy maximum range parameter |
| `navy_carrier_air_attack_factor` | Aircraft carrier air attack |
| `navy_carrier_air_targetting_factor` | Aircraft carrier-based aircraft aerial targeting |
| `SORTIE_EFFICIENCY_FACTOR` | Attack efficiency |
| `screening_efficiency` | Screen guard efficiency |
| `naval_retreat_speed` | Fleet speed during retreat |
| `positioning` | Position |
| `spotting_chance` | Spotting enemy speed |
| `navy_fuel_consumption_factor` | Navy fuel consumption |
| `navy_anti_air_attack_factor` | Naval anti-air attack |
| `refit_ic_cost` | Ship modification cost |
| `refit_speed` | Ship refit speed |
| `repair_speed_factor` | Ship repair speed |

## Air Force

| Correction | Explanation |
|------|------|
| `air_accidents` | Air Force accident probability |
| `air_weather_penalty` | Air Force weather penalty |
| `air_attack_factor` | Anti-air attack |
| `air_ace_generation_chance_factor` | Air combat ace generation probability |
| `air_mission_efficiency` | Air Force mission efficiency |
| `air_superiority_efficiency` | Air superiority efficiency |
| `air_intercept_efficiency` | Air force interception efficiency |
| `air_cas_efficiency` | Air support mission efficiency |
| `air_night_penalty` | Night punishment |
| `air_range_factor` | Air force range |
| `air_agility_factor` | Air force mobility performance |
| `air_escort_efficiency` | Escort efficiency |
| `strategic_bomber_bombing_factor` | Strategic bombing factor |
| `air_fuel_consumption_factor` | Air Force fuel consumption |
## Occupation and Resistance

| Correction | Explanation |
|------|------|
| `resistance_target` | Resistance target |
| `resistance_target_on_our_occupied_states` | Resistance target on our occupied states |
| `resistance_decay` | Resistance to decline rate |
| `resistance_decay_on_our_occupied_states` | Resistance decline in our occupied states |
| `resistance_growth` | Resistance growth rate |
| `resistance_growth_on_our_occupied_states` | Resistance growth rate in our occupied states |
| `compliance_starting_value` | Initial compliance |
| `compliance_gain` | Daily compliance gain |
| `compliance_growth` | Compliance growth rate |
| `compliance_growth_on_our_occupied_states` | Compliance growth rate in our occupied states |
| `required_garrison_factor` | Garrison requirements |
| `attrition` | loss |

## Landing and Amphibious

| Correction | Explanation |
|------|------|
| `invasion_preparation` | Login preparation time |
| `NAVAL_INVASION_PENALTY` | Login penalty |
| `amphibious_invasion` | Amphibious landing speed |

## AI

| Correction | Explanation |
|------|------|
| `ai_focus_aggressive_factor` | AI focus on offense |
| `ai_focus_defense_factor` | AI focus defense |
| `ai_call_ally_desire_factor` | AI requests allies’ willingness to join the war |
| `ai_join_ally_desire_factor` | AI willingness to join the war |
| `ai_get_ally_desire_factor` | AI desire to join/expand camp |
| `ai_focus_naval_factor` | AI focus navy |
| `ai_focus_naval_air_factor` | AI focuses on naval aviation |
| `ai_focus_aviation_factor` | AI focus on air force |
## Scientific research

| Correction | Explanation |
|------|------|
| `research_speed_factor` | Research speed |

## Military code

```
infantry = infantry battalion
militia = militia camp
cavalry = cavalry battalion
camelry = camel camp
motorized = motorized
light_armor = light tank
medium_armor = medium tank
heavy_armor = heavy tank
super_heavy_armor = super heavy tank
modern_armor = modern tank
marine = Marine Corps
paratrooper = airborne paratrooper
amphibious_armor = amphibious tank
amphibious_mechanized = amphibious mechanized
anti_tank_brigade = anti-tank gun
anti_air_brigade = anti-aircraft gun
armored_car = armored car
artillery_brigade = artillery battalion
mot_artillery_brigade = Motorized artillery
rocket_artillery_brigade = Rocket Artillery
mot_rocket_artillery_brigade = Motorized rocket launcher
motorized_rocket_brigade = self-propelled rocket launcher
bicycle_batallion = bicycle batallion
mountaineers = mountain infantry
mechanized = mechanized
light_sp_anti_air_brigade = Light self-propelled air defense
medium_sp_anti_air_brigade = medium self-propelled air defense
heavy_sp_anti_air_brigade = heavy self-propelled air defense
super_heavy_sp_anti_air_brigade = Super heavy self-propelled air defense
modern_sp_anti_air_brigade = Modern self-propelled air defense
light_sp_artillery_brigade = Light self-propelled artillery
medium_sp_artillery_brigade = medium self-propelled artillery
heavy_sp_artillery_brigade = heavy self-propelled artillery
super_heavy_sp_artillery_brigade = Super heavy self-propelled artillery
modern_sp_artillery_brigade = Modern self-propelled artillery
light_tank_destroyer_brigade = light self-propelled anti-tank
medium_tank_destroyer_brigade = medium self-propelled anti-tank
heavy_tank_destroyer_brigade = heavy self-propelled anti-tank
super_heavy_tank_destroyer_brigade = super heavy self-propelled anti-tank
modern_tank_destroyer_brigade = modern self-propelled anti-tank
```
## Support linking codes

```
engineer = engineer
artillery = artillery support company
recon = reconnaissance company
military_police = military police
mot_recon = Motorized reconnaissance
armored_car_recon = armored car recon
light_tank_recon = light tank recon
anti_air = anti-aircraft
anti_tank = anti-tank
field_hospital = field hospital
logistics_company = logistics
maintenance_company = maintenance
rocket_artillery = rocket launcher
signal_company = communication
```
