# ALL EVENTS REFERENCE

Complete listing of every event in every pool, the tone-gate table, night pools, special categories, inventory weight modifiers, and wander tracks.

---

## HOW THE DAY EVENT SYSTEM WORKS

1. **Pool Build**: `make_unified_day_pool()` merges all 6 rank-tier builders into one list, deduplicates, then applies the tone table as a multiplier (each event gets N copies where N = its tone weight at the player's current rank; weight 0 = excluded).
2. **Illness/Car-Trouble Dispatch**: Individual illness and car-trouble event names are stripped from the raw pool and replaced by `random_illness` and `random_car_trouble` dispatchers (injected at fixed copy counts per rank).
3. **Car Gating**: Events in `_CAR_DEPENDENT_DAY_NAMES` are removed if the player has no car.
4. **Inventory Weights**: `_apply_inventory_pool_weights` adds/removes copies based on held items.
5. **Draw**: `get_day_event()` pops from the shuffled pool. If a popped event's tone weight at the current rank is 0, it's discarded (up to 600 tries).

Night pools are **rank-specific** (not unified) — each rank has its own dedicated pool.

---

## DAY EVENT POOLS

### POOR DAY EVENTS (`make_poor_day_events_list`, line 2510)

**Everytime:**
`seat_cash`, `left_window_down`, `estranged_dog`, `freight_truck`, `morning_stretch`, `ant_invasion`, `bird_droppings`, `flat_tire`, `mysterious_note`, `radio_static`, `vending_machine_luck`, `talking_to_yourself`, `wrong_number`, `cloud_watching`, `car_alarm_symphony`, `trash_treasure`, `coin_flip_stranger`, `seagull_attack`, `lucky_penny`, `vinnie_referral_card`, `stray_cat`, `three_legged_dog`, `opossum_in_trash`, `raccoon_gang_raid`, `sewer_rat`, `conspiracy_theorist`, `dropped_ice_cream`, `motivational_graffiti`

**Deadly:**
`back_alley_shortcut`, `food_poisoning`, `attacked_by_dog`, `carbon_monoxide`

**Medical:**
`contract_cold`, `contract_flu`, `contract_strep_throat`, `contract_ear_infection`, `contract_sinus_infection`, `contract_pink_eye`, `contract_ringworm`, `contract_scabies`, `rat_bite`, `dirty_needle_stick`, `unclean_water`, `mold_exposure`, `lead_poisoning`, `bad_oysters`, `homeless_shelter_outbreak`, `bad_tattoo_infection`, `public_pool_infection`, `food_truck_nightmare`

**Injury:**
`slip_in_shower`, `fall_down_stairs`, `kitchen_accident`, `bar_fight_aftermath`, `broken_nose`, `broken_wrist`, `deep_laceration`, `whiplash_injury`, `dog_attack_severe`, `assault_aftermath`

**Mental Health:**
`severe_anxiety_attack`, `severe_depression_episode`, `insomnia_chronic`, `stress_breakdown`, `trauma_flashback`, `sleep_deprivation_crisis`

**Conditional:**
`sore_throat`, `spider_bite`, `hungry_cockroach`, `ant_bite`, `knife_wound_infection`, `gut_wound_complications`, `dog_bite_rabies_scare`, `fuel_leak_fire`, `fuel_leak_fixed`, `damaged_exhaust_fixed`, `damaged_exhaust_again`, `atm_theft_police`, `soulless_emptiness`, `soulless_mirror`, `painkiller_withdrawal`, `empty_event`, `unpaid_tickets_boot`, `booted_car_impound`, `mystery_car_problem_worsens`

**Random Small:**
`found_twenty`, `lost_wallet`, `sunburn`, `mosquito_bite_infection`, `good_hair_day`, `bad_hair_day`, `found_gift_card`, `car_battery_dead`, `flat_tire_again`, `nice_weather`, `terrible_weather`, `weird_noise`, `back_pain`, `stretching_helps`, `random_kindness`, `random_cruelty`, `someone_stole_your_stuff`, `prayer_answered`, `prayer_ignored`, `found_old_photo`, `got_a_tan`

**One-Time:**
`lone_cowboy`, `whats_my_name`, `interrogation`, `old_man_jenkins`, `the_mime`

**Secret:**
`midnight_visitor`, `perfect_hand`

**Silly Creative:**
`duck_army`, `sentient_sandwich`, `motivational_raccoon`, `pigeon_mafia`, `sock_puppet_therapist`, `dance_battle`

**Weird Creative:**
`time_loop`, `mirror_stranger`, `the_glitch`, `fourth_wall_break`, `wrong_universe`

**Dark Creative:**
`the_empty_room`, `blood_moon_bargain`

**Goofy Creative:**
`alien_abduction`

**Number Secrets:**
`exactly_100`, `exactly_420`, `exactly_13`, `day_palindrome`, `prime_day`, `same_as_health`

**Non-Number Secrets:**
`first_sunrise`, `perfect_health_moment`, `rock_bottom`, `completely_broke_wisdom`, `the_cat_knows`, `rain_on_the_roof`, `the_sleeping_stranger`

**Companion Day:**
`lucky_guards_car`, `mr_pecks_treasure`, `whiskers_sixth_sense`, `slick_escape_route`, `hopper_lucky_day`, `buddy_passive_find`, `slick_passive_find`, `hopper_passive_find`, `patches_night_watch`, `squirrelly_stash`, `companion_sick_day`, `companion_hero_moment`, `companion_nightmare`, `companion_lost_adventure`, `companion_food_crisis`

**Crafted Item:**
`shiv_confrontation`, `lockpick_opportunity`, `fishing_day`, `trap_night_thief`, `dream_catcher_night`, `slingshot_bird_hunt`, `signal_mirror_rescue`, `rain_collector_bonus`, `fire_starter_campfire`, `companion_bed_bonus`, `worry_stone_moment`, `snare_trap_catch`, `binocular_scope_discovery`, `emergency_blanket_cold_night`, `lucky_charm_streak`, `water_purifier_use`, `pet_toy_playtime`, `home_remedy_illness`, `road_flare_torch_encounter`, `feeding_station_morning`, `splint_injury_event`

**Item Use (no-use activation):**
`road_talisman_protection`, `silver_horseshoe_luck`, `mystery_potion_effect`, `feelgood_bottle_moment`, `persistent_bottle_refill`, `ritual_token_ceremony`, `council_feather_blessing`, `cowboy_jacket_encounter`, `found_phone_call`, `alien_crystal_event`, `dimensional_coin_flip`, `radio_numbers_broadcast`, `mysterious_envelope_reveal`, `lockbox_contents`, `hollow_tree_stash_find`, `vision_map_navigate`, `secret_route_shortcut`, `street_cat_ally_benefit`, `old_photograph_memory`, `beach_romance_call`, `apartment_key_visit`, `fake_flower_gift`, `empty_locket_memory`, `stack_of_flyers_opportunity`, `mysterious_key_lockbox_open`, `suspicious_package_open`, `stolen_watch_recognition`, `underwater_camera_photos`, `witch_ward_dark_protection`, `deck_of_cards_street_game`, `ace_of_spades_blackjack_omen`, `dealer_joker_revelation`, `magic_acorn_planting`, `treasure_map_follow`, `capture_fairy_release`, `lucky_lure_fishing`, `mysterious_code_decode`, `swamp_gold_attention`

**Chain Starters:**
`hermit_trail_discovery`, `lost_dog_flyers_found`, `lost_dog_investigation`

**Recurring Chain Item:**
`herbal_pouch_remedy`, `walking_stick_hike`, `tinfoil_hat_event`, `reunion_photo_comfort`

**New Crafted (Tier 1):**
`headlamp_night_walk`, `spotlight_hidden_path`, `brass_knuckles_brawl`, `stink_bomb_escape`, `animal_bait_companion`, `trail_mix_bomb_distraction`, `forged_documents_police`, `fortune_cards_warning`, `luck_totem_windfall`, `tire_ready_flat`, `miracle_lube_breakdown`

**Car Trouble:**
`corroded_battery_terminals`, `fuse_blown`, `abs_light_on`, `slow_tire_leak`, `headlights_burned_out`, `starter_motor_grinding`, `windshield_cracked`, `hail_damage`, `key_wont_turn`, `window_wont_roll_up`, `trunk_wont_close`, `bald_tires_noticed`, `exhaust_leak_loud`, `thermostat_stuck`, `nail_in_tire`

**Car Trouble Follow-Ups:**
`nail_in_tire_blows`, `failing_starter_dies`

**Section 45 Rewritten Item:**
`low_profile_shelter_meal`, `beach_bum_heatwave`, `beach_bum_tribe`, `outdoor_shield_farmer`, `cool_down_car_overheat`, `vermin_bomb_car`

**Section 44A Wild Item Interactions:**
`wild_headlamp_poker`, `wild_fortune_cards_car`, `lottery_ticket_check`

**Wrong Item Comedy:**
`wrong_item_bug_spray_campfire`, `wrong_item_road_flares_stealth`, `wrong_item_dog_whistle_bear`

---

### CHEAP DAY EVENTS (`make_cheap_day_events_list`, line 2827)

**Everytime:**
`sun_visor_bills`, `strong_winds`, `morning_fog`, `car_wont_start`, `raccoon_raid`, `beautiful_sunrise`, `fortune_cookie`, `deja_vu_again`, `street_musician`, `roadkill_philosophy`, `yard_sale_find`, `broken_atm`, `friendly_drunk`, `car_wash_encounter`, `lottery_scratch`, `free_sample_spree`, `parking_lot_poker`, `phone_scam_call`

**Companion Encounters:**
`crow_encounter`, `garden_rabbit`, `three_legged_dog`

**Deadly:**
`gas_station_robbery`, `drug_dealer_encounter`, `electrocution_hazard`, `car_explosion`

**Medical:**
`contract_bronchitis`, `contract_stomach_flu`, `contract_uti`, `contract_mono`, `contract_staph_infection`, `bee_sting_allergy`, `asthma_attack`, `migraine_severe`, `vertigo_episode`, `tooth_abscess`, `severe_dehydration`, `malnutrition`, `camping_tick_bite`, `daycare_plague`, `botched_piercing`, `bad_sushi`

**Injury:**
`car_accident_minor`, `construction_site_accident`, `grease_fire`, `sports_injury`, `gym_accident`, `electric_shock`, `broken_ankle`, `broken_hand`, `dislocated_shoulder`, `concussion_injury`, `broken_ribs_injury`, `second_degree_burns`, `hiking_disaster`, `trampoline_disaster`, `weight_dropping`

**Conditional Deadly:**
`knife_wound_infection`, `gut_wound_complications`, `dog_bite_rabies_scare`, `fuel_leak_fire`, `fuel_leak_fixed`, `damaged_exhaust_fixed`, `damaged_exhaust_again`, `atm_theft_police`, `heart_condition_flare`, `painkiller_withdrawal`, `painkiller_dealer_returns`, `painkiller_overdose`, `cocaine_temptation`, `cocaine_crash`, `cocaine_heart_attack`, `voodoo_doll_temptation`, `soulless_emptiness`, `soulless_mirror`, `soulless_recognition`, `weakened_immune_cold`, `weakened_immune_pneumonia`, `unpaid_tickets_boot`, `booted_car_impound`, `mystery_car_problem_worsens`, `stray_cat_has_kittens`

**Random Small:**
`found_twenty`, `lost_wallet`, `sunburn`, `mosquito_bite_infection`, `good_hair_day`, `bad_hair_day`, `found_gift_card`, `car_battery_dead`, `flat_tire_again`, `nice_weather`, `terrible_weather`, `weird_noise`, `back_pain`, `stretching_helps`, `random_kindness`, `random_cruelty`, `someone_stole_your_stuff`, `prayer_answered`, `prayer_ignored`, `found_old_photo`, `threw_out_old_photo`, `got_a_tan`

**Item-Using:**
`mosquito_swarm`, `scorching_sun`, `sudden_downpour`, `freezing_night`, `car_smell`, `roadside_breakdown`, `broken_belonging`, `social_encounter`, `rubber_band_save`, `penny_luck`, `grimy_gus_discovery`, `vinnie_referral_card`, `windblown_worn_map`, `flea_market_route_map`, `laundromat_bulletin_map`, `witch_doctor_matchbook`, `roadside_bone_chimes`, `trusty_tom_coupon_mailer`, `filthy_frank_radio_giveaway`, `oswald_concierge_card`

**Conditional:**
`got_a_cold`, `cold_gets_worse`, `empty_event`

**One-Time:**
`turn_to_god`, `hungry_cow`, `ice_cream_truck`, `kid_on_bike`, `lost_tourist`, `the_hitchhiker`

**Conditional:**
`mayas_luck`

**Secret:**
`deja_vu`, `exactly_1111`

**Creative:**
`duck_army`, `sentient_sandwich`, `motivational_raccoon`, `pigeon_mafia`, `sock_puppet_therapist`, `dance_battle`, `time_loop`, `mirror_stranger`, `the_glitch`, `fourth_wall_break`, `wrong_universe`, `alien_abduction`, `blood_moon_bargain`

**Number Secrets:**
`exactly_1234`, `day_palindrome`, `prime_day`, `same_as_health`

**Non-Number Secrets:**
`the_veteran_gambler`, `perfect_health_moment`, `rock_bottom`, `companion_reunion`, `the_cat_knows`, `the_crow_council`, `insomniac_revelation`, `rain_on_the_roof`, `the_sleeping_stranger`

**Companion Day:**
`lucky_guards_car`, `mr_pecks_treasure`, `rusty_midnight_heist`, `whiskers_sixth_sense`, `slick_escape_route`, `hopper_lucky_day`, `buddy_passive_find`, `slick_passive_find`, `hopper_passive_find`, `patches_night_watch`, `squirrelly_stash`, `companion_sick_day`, `companion_rivalry`, `companion_hero_moment`, `companion_nightmare`, `companion_lost_adventure`, `companion_brings_friend`, `companion_food_crisis`, `companion_milestone`, `buddy_dog_whistle_synergy`, `thunder_running_shoes_synergy`, `grace_dream_catcher_synergy`, `echo_camera_synergy`, `shellbert_worry_stone_synergy`, `bear_scrap_armor_synergy`

**Crafted Item:**
`shiv_confrontation`, `lockpick_opportunity`, `fishing_day`, `trap_night_thief`, `dream_catcher_night`, `slingshot_bird_hunt`, `signal_mirror_rescue`, `rain_collector_bonus`, `fire_starter_campfire`, `companion_bed_bonus`, `worry_stone_moment`, `snare_trap_catch`, `binocular_scope_discovery`, `emergency_blanket_cold_night`, `lucky_charm_streak`, `water_purifier_use`, `pet_toy_playtime`, `home_remedy_illness`, `road_flare_torch_encounter`, `feeding_station_morning`, `splint_injury_event`

**Item Use (no-use activation):**
`road_talisman_protection`, `silver_horseshoe_luck`, `mystery_potion_effect`, `feelgood_bottle_moment`, `persistent_bottle_refill`, `ritual_token_ceremony`, `council_feather_blessing`, `cowboy_jacket_encounter`, `found_phone_call`, `alien_crystal_event`, `dimensional_coin_flip`, `radio_numbers_broadcast`, `mysterious_envelope_reveal`, `lockbox_contents`, `hollow_tree_stash_find`, `vision_map_navigate`, `secret_route_shortcut`, `street_cat_ally_benefit`, `old_photograph_memory`, `beach_romance_call`, `apartment_key_visit`, `fake_flower_gift`, `empty_locket_memory`, `stack_of_flyers_opportunity`, `mysterious_key_lockbox_open`, `suspicious_package_open`, `stolen_watch_recognition`, `underwater_camera_photos`, `witch_ward_dark_protection`, `deck_of_cards_street_game`, `ace_of_spades_blackjack_omen`, `dealer_joker_revelation`, `magic_acorn_planting`, `treasure_map_follow`, `capture_fairy_release`, `lucky_lure_fishing`, `mysterious_code_decode`, `swamp_gold_attention`

**Chain Starters:**
`hermit_trail_discovery`, `lost_dog_flyers_found`, `lost_dog_investigation`

**Chain Progression:**
`hermit_camp_return`, `hermit_journal_study`, `midnight_radio_signal`, `midnight_radio_frequency`, `lost_dog_whistle_search`, `lost_dog_culprit`, `lost_dog_reunion`

**Recurring Chain Item:**
`herbal_pouch_remedy`, `walking_stick_hike`, `tinfoil_hat_event`, `reunion_photo_comfort`, `junkyard_crown_moment`

**New Crafted (Tier 1):**
`headlamp_night_walk`, `spotlight_hidden_path`, `brass_knuckles_brawl`, `stink_bomb_escape`, `animal_bait_companion`, `trail_mix_bomb_distraction`, `forged_documents_police`, `fortune_cards_warning`, `luck_totem_windfall`, `tire_ready_flat`, `miracle_lube_breakdown`, `evidence_kit_crime`, `radio_jammer_checkpoint`, `security_bypass_locked_room`, `gentleman_charm_dinner`, `gas_mask_chemical`, `voice_soother_persuasion`, `devils_deck_gambling`, `blackmail_letter_extortion`, `kingpin_look_respect`, `heirloom_set_recognition`

**Car Trouble:**
`dead_battery_afternoon`, `engine_oil_empty`, `oil_leak_spotted`, `brakes_squealing`, `ran_out_of_gas`, `car_alarm_malfunction`, `frozen_door_locks`, `parking_brake_stuck`, `clogged_fuel_filter`, `strange_engine_noise`, `check_engine_light_on`, `engine_overheating`, `car_wont_go_in_reverse`, `gas_pedal_sticking`, `wheel_alignment_off`, `suspension_creaking`, `nail_in_tire`

**Car Trouble Follow-Ups:**
`leaking_battery_worsens`, `engine_knock_worsens`, `bald_tires_hydroplane`, `nail_in_tire_blows`, `failing_starter_dies`

**Section 45 Rewritten Item:**
`low_profile_casino_blend`, `low_profile_police_encounter`, `low_profile_mugging_marcus`, `low_profile_shelter_meal`, `beach_bum_heatwave`, `beach_bum_tribe`, `gas_mask_fire_rescue`, `storm_suit_hurricane`, `storm_suit_flood`, `storm_suit_night_bear`, `antacid_business_dinner`, `outdoor_shield_farmer`, `cool_down_car_overheat`, `smoke_flare_pursuit`, `vermin_bomb_car`

**Section 44A Wild Item Interactions:**
`wild_headlamp_poker`, `wild_evidence_kit_wedding`, `wild_gas_mask_funeral`, `wild_devil_deck_children`, `wild_fortune_cards_car`, `lottery_ticket_check`

**Wrong Item Comedy:**
`wrong_item_bug_spray_campfire`, `wrong_item_road_flares_stealth`, `wrong_item_pest_control_romance`, `wrong_item_vermin_bomb_romance`, `wrong_item_dog_whistle_bear`

---

### MODEST DAY EVENTS (`make_modest_day_events_list`, line 3222)

**Everytime:**
`left_door_open`, `fancy_coffee`, `parking_ticket`, `found_phone`, `street_performer_duel`, `compliment_stranger`, `vinnie_referral_card`, `grimy_gus_discovery`, `windblown_worn_map`, `flea_market_route_map`, `laundromat_bulletin_map`, `witch_doctor_matchbook`, `roadside_bone_chimes`, `trusty_tom_coupon_mailer`, `filthy_frank_radio_giveaway`, `oswald_concierge_card`, `forgotten_birthday`, `book_club_invite`, `car_compliment`, `dog_walker_collision`, `coffee_shop_philosopher`, `food_truck_festival`

**Deadly:**
`back_alley_shortcut`, `heart_attack_scare`, `drug_dealer_encounter`

**Medical:**
`contract_pneumonia`, `contract_shingles`, `contract_lyme_disease`, `contract_tetanus`, `contract_rabies_scare`, `develop_diabetes_symptoms`, `high_blood_pressure_crisis`, `severe_allergic_reaction`, `kidney_stones`, `gallbladder_attack`, `appendicitis_attack`, `blood_clot_in_leg`, `seizure_episode`, `pancreatitis_attack`, `blood_poisoning`, `asbestos_exposure`, `mercury_poisoning`, `dental_disaster`, `allergic_reaction_restaurant`, `wasp_nest_encounter`, `gym_collapse`, `ptsd_flashback`

**Injury:**
`severe_burn_injury`, `broken_collarbone`, `torn_acl`, `herniated_disc`, `puncture_wound`, `frostbite`, `heat_stroke`, `hypothermia`, `chemical_burn`, `electrical_burn`, `jaw_fracture`, `orbital_fracture`, `nerve_damage`, `tendon_rupture`, `muscle_tear`, `motorcycle_crash`, `pool_diving_accident`, `chemical_spill`, `workplace_injury`, `caught_in_fire`, `frozen_outdoors`, `heat_exhaustion_collapse`, `mma_fight_aftermath`

**Conditional Deadly:**
`knife_wound_infection`, `gut_wound_complications`, `bridge_contemplation`, `dog_bite_rabies_scare`, `fuel_leak_fire`, `fuel_leak_fixed`, `heart_condition_flare`, `painkiller_withdrawal`, `painkiller_dealer_returns`, `painkiller_overdose`, `cocaine_temptation`, `cocaine_crash`, `voodoo_doll_temptation`, `soulless_emptiness`, `soulless_mirror`, `soulless_recognition`, `burn_scars_stares`, `burn_scars_infection`, `weakened_immune_cold`, `weakened_immune_pneumonia`, `unpaid_tickets_boot`, `booted_car_impound`, `mystery_car_problem_worsens`, `stray_cat_has_kittens`, `old_rival_encounter`, `media_known_harassed`, `media_known_documentary`

**Random Small:**
`found_twenty`, `lost_wallet`, `sunburn`, `good_hair_day`, `bad_hair_day`, `nice_weather`, `terrible_weather`, `back_pain`, `stretching_helps`, `random_kindness`, `random_cruelty`, `prayer_answered`, `prayer_ignored`

**One-Time:**
`the_prophet`

**Conditional:**
`unpaid_ticket_consequence`, `mayas_luck`, `street_performer`, `power_outage_area`, `construction_noise`, `empty_event`, `starving_cow`

**Item-Using:**
`important_document`, `caught_fishing`, `robbery_attempt`, `photo_opportunity`, `need_fire`

**Conditional:**
`another_spider_bite`, `squirrel_invasion`, `homeless_network`

**One-Time:**
`the_photographer`, `the_food_truck`

**Secret:**
`exactly_50000`

**Creative:**
`duck_army`, `sentient_sandwich`, `motivational_raccoon`, `pigeon_mafia`, `dance_battle`, `time_loop`, `mirror_stranger`, `the_glitch`, `fourth_wall_break`, `wrong_universe`, `the_collector`, `the_empty_room`, `alien_abduction`, `blood_moon_bargain`

**Number Secrets:**
`exactly_69420`, `day_palindrome`, `prime_day`

**Non-Number Secrets:**
`the_veteran_gambler`, `perfect_health_moment`, `companion_reunion`, `haunted_by_losses`, `the_cat_knows`, `the_crow_council`, `insomniac_revelation`, `item_hoarder`, `rain_on_the_roof`

**Companion Day:**
`lucky_guards_car`, `mr_pecks_treasure`, `rusty_midnight_heist`, `whiskers_sixth_sense`, `slick_escape_route`, `hopper_lucky_day`, `buddy_passive_find`, `slick_passive_find`, `hopper_passive_find`, `patches_night_watch`, `squirrelly_stash`, `companion_sick_day`, `companion_rivalry`, `companion_hero_moment`, `companion_death_sacrifice`, `companion_nightmare`, `companion_lost_adventure`, `companion_bonded_moment`, `companion_learns_trick`, `companion_brings_friend`, `companion_food_crisis`, `companion_milestone`, `buddy_dog_whistle_synergy`, `thunder_running_shoes_synergy`, `grace_dream_catcher_synergy`, `echo_camera_synergy`, `shellbert_worry_stone_synergy`, `bear_scrap_armor_synergy`

**Crafted Item:**
*(Same 21 as Poor/Cheap)*

**Item Use (no-use activation):**
*(Same 38 as Poor/Cheap)*

**Hermit Chain:**
`hermit_trail_discovery`, `hermit_camp_return`, `hermit_journal_study`, `hermit_trail_stranger`, `hermit_hollow_oak`

**Midnight Radio Chain:**
`midnight_radio_signal`, `midnight_radio_frequency`, `midnight_radio_pole`, `midnight_radio_visit`, `midnight_radio_broadcast`

**Junkyard Artisan Chain:**
`junkyard_artisan_meet`, `junkyard_lesson_one`, `junkyard_lesson_two`

**Lost Dog Chain:**
`lost_dog_flyers_found`, `lost_dog_investigation`, `lost_dog_whistle_search`, `lost_dog_culprit`, `lost_dog_reunion`

**Recurring Chain Item:**
`herbal_pouch_remedy`, `walking_stick_hike`, `tinfoil_hat_event`, `reunion_photo_comfort`, `junkyard_crown_moment`, `scrap_armor_event`

**Crossover:**
`crossover_night_vision_bonus`

**New Crafted (Tier 1+):**
*(Same 21 as Cheap)* PLUS: `emp_device_pursuit`, `eldritch_candle_entity`, `road_warrior_ambush`, `third_eye_foresight`, `gamblers_aura_blackjack`

**Car Trouble:**
`engine_wont_turn_over`, `tire_blowout`, `battery_acid_leak`, `alternator_failing`, `brake_fluid_leak`, `fuel_pump_whining`, `stuck_in_gear`, `radiator_leak`, `power_steering_failure`, `frozen_fuel_line`, `water_pump_failing`, `dead_battery_afternoon`, `engine_overheating`, `car_alarm_malfunction`

**Car Trouble Follow-Ups:**
`leaking_battery_worsens`, `engine_knock_worsens`, `bald_tires_hydroplane`, `failing_fuel_pump_dies`, `broken_ball_joint_breaks`, `failing_starter_dies`

**Section 45 Rewritten Item:**
`low_profile_casino_blend`, `low_profile_police_encounter`, `low_profile_mugging_marcus`, `low_profile_shelter_meal`, `beach_bum_yacht_party`, `beach_bum_heatwave`, `beach_bum_tribe`, `gas_mask_toxic_spill`, `gas_mask_fire_rescue`, `storm_suit_hurricane`, `storm_suit_flood`, `storm_suit_night_bear`, `antacid_business_dinner`, `outdoor_shield_farmer`, `cool_down_car_overheat`, `smoke_flare_pursuit`, `vermin_bomb_car`, `enchanted_vintage_party`, `power_move_intimidation`, `animal_magnetism_recruit`, `animal_magnetism_predator`, `power_grid_dead_battery`, `mobile_workshop_stranger`, `pursuit_package_chase`, `pursuit_package_witness`

**Section 44A Wild Item Interactions:**
`wild_headlamp_poker`, `wild_emp_casino`, `wild_radio_jammer_police`, `wild_evidence_kit_wedding`, `wild_distress_beacon_casino`, `wild_stink_bomb_casino_vault`, `wild_gas_mask_funeral`, `wild_eldritch_candle_gambling`, `wild_devil_deck_children`, `wild_binding_portrait_shopkeeper`, `wild_fortune_cards_car`, `wild_blackmail_letter_companion`, `lottery_ticket_check`, `bottle_of_tomorrow_use`, `blank_check_opportunity`

**Wrong Item Comedy:**
`wrong_item_bug_spray_campfire`, `wrong_item_road_flares_stealth`, `wrong_item_pest_control_romance`, `wrong_item_vermin_bomb_romance`, `wrong_item_dirty_hat_dinner`, `wrong_item_dog_whistle_bear`, `wrong_item_necronomicon_loan_shark`, `necronomicon_reading`

---

### RICH DAY EVENTS (`make_rich_day_events_list`, line 3650)

**Everytime:**
`left_trunk_open`, `luxury_car_passes`, `paparazzi_mistake`, `luxury_problems`, `imposter_syndrome`, `charity_opportunity`, `investment_opportunity`, `expensive_taste`, `news_van`, `fancy_restaurant_mistake`, `autograph_request`, `casino_regular`, `mysterious_package`, `rich_persons_problems`, `investment_pitch`

**Deadly:**
`back_alley_shortcut`, `heart_attack_scare`, `drug_dealer_encounter`, `car_explosion`

**Medical:**
`contract_measles`, `skull_fracture`, `collapsed_lung`, `ruptured_spleen`, `liver_laceration`, `detached_retina`, `crush_injury`, `gangrene_infection`, `drug_overdose_survival`, `botched_surgery`, `covid_complications`, `earthquake_injury`, `carnival_ride_accident`, `window_crash`, `explosion_nearby`, `coma_awakening`, `prison_shiv_wound`, `bad_mushrooms`

**Conditional Deadly:**
`knife_wound_infection`, `gut_wound_complications`, `bridge_contemplation`, `heart_condition_flare`, `painkiller_withdrawal`, `painkiller_dealer_returns`, `painkiller_overdose`, `cocaine_temptation`, `cocaine_crash`, `cocaine_heart_attack`, `voodoo_doll_temptation`, `soulless_emptiness`, `soulless_mirror`, `soulless_recognition`, `burn_scars_stares`, `weakened_immune_cold`, `weakened_immune_pneumonia`, `mystery_car_problem_worsens`, `old_rival_encounter`, `media_known_harassed`, `media_known_documentary`, `high_roller_room_visit`, `high_roller_whale`

**Random Small:**
`found_twenty`, `lost_wallet`, `good_hair_day`, `bad_hair_day`, `nice_weather`, `terrible_weather`, `back_pain`, `stretching_helps`, `prayer_answered`, `prayer_ignored`

**Item-Using (Premium):**
`classy_encounter`, `wine_and_dine`, `cigar_circle`, `lucky_rabbit_encounter`

**Conditional:**
`wild_rat_attack`, `hungry_termites`, `wealth_anxiety`, `tax_man`, `empty_event`, `even_further_interrogation`

**One-Time:**
`the_rival`, `the_bodyguard_offer`, `high_roller_invitation`, `old_friend_recognition`, `grimy_gus_discovery`, `vinnie_referral_card`, `windblown_worn_map`, `flea_market_route_map`, `laundromat_bulletin_map`, `witch_doctor_matchbook`, `roadside_bone_chimes`, `trusty_tom_coupon_mailer`, `filthy_frank_radio_giveaway`, `oswald_concierge_card`, `the_gambler_ghost`

**Secret:**
`exactly_250000`

**Companion Day:**
*(Same 26 as Modest — includes `companion_death_sacrifice`, `companion_bonded_moment`, `companion_learns_trick`)*

**Crafted Item:** *(Same 21)*
**Item Use:** *(Same 38)*

**Hermit Chain:**
*(Same 5 as Modest)* plus `hermit_trail_stranger`, `hermit_hollow_oak`

**Midnight Radio Chain:** *(Same 5 as Modest)*

**Junkyard Artisan Chain:**
*(Same 3 as Modest)* PLUS: `junkyard_gideon_story`, `junkyard_masterpiece`

**Lost Dog Chain:** *(Same 5 as Modest)*
**Recurring Chain Item:** *(Same 6 as Modest)*

**Crossover:**
`crossover_radio_hermit`, `crossover_artisan_rose_gift`, `crossover_night_vision_bonus`, `crossover_all_chains_complete`

**New Crafted (Tier 1+2):**
*(Same 25 as Modest)* PLUS: `ghost_protocol_invisible`, `immortal_vehicle_breakdown`

**Car Trouble:**
`transmission_slipping`, `broken_ball_joint`, `catalytic_converter_stolen`, `flooded_engine`, `mystery_breakdown`, `tire_blowout`, `alternator_failing`, `brake_fluid_leak`, `water_pump_failing`

**Car Trouble Follow-Ups:**
`leaking_battery_worsens`, `engine_knock_worsens`, `bald_tires_hydroplane`, `failing_fuel_pump_dies`, `broken_ball_joint_breaks`

**Section 45 Rewritten Item:**
*(Same 25 as Modest)* PLUS: `aristocrat_cold_elegance`

**Section 44A Wild Item Interactions:** *(Same 15 as Modest)*

**Wrong Item Comedy:**
`wrong_item_pest_control_romance`, `wrong_item_vermin_bomb_romance`, `wrong_item_dirty_hat_dinner`, `wrong_item_necronomicon_loan_shark`

---

### DOUGHMAN DAY EVENTS (`make_doughman_day_events_list`, line 4010)

**Everytime:**
`thunderstorm`, `high_stakes_feeling`, `casino_security`, `wealthy_doubts`, `people_watching`, `money_counting_ritual`, `nervous_habits`, `millionaire_fantasy`, `wealth_paranoia`, `high_roller_room`, `old_rival_returns`, `casino_comps`, `millionaire_milestone`

**Deadly:**
`heart_attack_scare`, `drug_dealer_encounter`

**Medical:**
`skull_fracture`, `collapsed_lung`, `ruptured_spleen`, `liver_laceration`, `detached_retina`, `ruptured_eardrum`, `gangrene_infection`, `drug_overdose_survival`, `botched_surgery`, `earthquake_injury`, `explosion_nearby`, `assault_aftermath`, `pool_diving_accident`, `coma_awakening`, `stress_breakdown`, `sleep_deprivation_crisis`

**Conditional Deadly:**
`knife_wound_infection`, `gut_wound_complications`, `bridge_contemplation`, `devils_bargain_consequence`, `heart_condition_flare`, `painkiller_withdrawal`, `painkiller_dealer_returns`, `painkiller_overdose`, `cocaine_crash`, `cocaine_heart_attack`, `voodoo_doll_temptation`, `soulless_emptiness`, `soulless_mirror`, `soulless_recognition`, `weakened_immune_pneumonia`, `old_rival_encounter`, `media_known_harassed`, `media_known_documentary`, `high_roller_room_visit`, `high_roller_whale`

**Random Small:**
`good_hair_day`, `bad_hair_day`, `nice_weather`, `terrible_weather`, `prayer_answered`, `prayer_ignored`

**Conditional:**
`the_temptation`, `even_further_interrogation`, `cow_army`

**One-Time:**
`likely_death`, `the_veteran`, `the_journalist`, `the_offer_refused`, `the_doppelganger`

**Secret:**
`exactly_777777`

**Creative:**
`time_loop`, `mirror_stranger`, `the_glitch`, `fourth_wall_break`, `the_collector`, `the_empty_room`, `blood_moon_bargain`

**Number Secrets:**
`exactly_7777`, `day_palindrome`, `prime_day`, `full_moon_madness`

**Non-Number Secrets:**
`the_veteran_gambler`, `companion_reunion`, `haunted_by_losses`, `the_crow_council`, `insomniac_revelation`, `item_hoarder`, `birthday_forgotten`, `rain_on_the_roof`

**Drastic:**
`loan_shark_visit`, `the_desperate_gambler`, `withdrawal_nightmare`, `organ_harvester`, `casino_overdose`, `cancer_diagnosis`, `the_bridge_call`, `the_relapse`, `the_confession`, `the_high_roller_suicide`, `the_dying_dealer`

**More Secrets:**
`the_anniversary_loss`, `survivor_guilt`, `the_scar_story`, `the_winning_streak_paranoia`, `old_gambling_buddy`

**Companion Day:** *(Same 26 as Rich)*
**Crafted Item:** *(Same 21)*
**Item Use:** *(Same 38)*
**Hermit Chain:** *(Same 5 as Rich)*
**Midnight Radio Chain:** *(Same 5 as Rich)*
**Junkyard Artisan Chain:** *(Same 5 as Rich)*
**Lost Dog Chain:** *(Same 5 as Rich)*
**Recurring Chain Item:** *(Same 6 as Rich)*
**Crossover:** *(Same 4 as Rich)*

**New Crafted (Tier 1+2+3):**
*(Same 27 as Rich)* PLUS: `guardian_angel_lethal`

**Car Trouble:**
`catalytic_converter_stolen`, `transmission_slipping`, `mystery_breakdown`, `flooded_engine`, `broken_ball_joint`

**Car Trouble Follow-Ups:**
`engine_knock_worsens`, `failing_fuel_pump_dies`, `broken_ball_joint_breaks`, `bald_tires_hydroplane`

**Section 45 Rewritten Item:** *(Same 26 as Rich)*
**Section 44A Wild Item Interactions:** *(Same 15 as Rich)*

**Wrong Item Comedy:**
`wrong_item_dirty_hat_dinner`, `wrong_item_necronomicon_loan_shark`

---

### NEARLY DAY EVENTS (`make_nearly_day_events_list`, line 4366)

**Everytime:**
`almost_there`, `the_weight_of_wealth`, `casino_knows`, `last_stretch`, `strange_visitors`, `the_final_temptation`, `reporters_found_you`, `casino_owner_meeting`

**Deadly:**
`heart_attack_scare`

**Medical:**
`skull_fracture`, `liver_laceration`, `ruptured_spleen`, `collapsed_lung`, `crush_injury`, `gangrene_infection`, `blood_poisoning`, `drug_overdose_survival`, `botched_surgery`, `explosion_nearby`, `assault_aftermath`, `coma_awakening`, `stress_breakdown`, `sleep_deprivation_crisis`, `trauma_flashback`

**Conditional Deadly:**
`knife_wound_infection`, `gut_wound_complications`, `bridge_contemplation`, `devils_bargain_consequence`, `heart_condition_flare`, `painkiller_overdose`, `cocaine_heart_attack`, `soulless_emptiness`, `soulless_mirror`, `soulless_recognition`, `media_known_documentary`, `high_roller_room_visit`, `high_roller_whale`

**Random Small:**
`prayer_answered`, `prayer_ignored`

**Conditional:**
`too_close_to_quit`, `cow_army`

**One-Time:**
`the_warning`, `the_celebration`, `the_offer`

**One-Time Conditional (Suzy):**
`gift_from_suzy`

**Secret:**
`exactly_999999`, `all_dreams_complete`

**Creative:**
`the_glitch`, `fourth_wall_break`, `the_collector`, `the_empty_room`, `blood_moon_bargain`

**Number Secrets:**
`day_palindrome`, `prime_day`, `full_moon_madness`

**Non-Number Secrets:**
`the_veteran_gambler`, `companion_reunion`, `haunted_by_losses`, `insomniac_revelation`, `item_hoarder`, `birthday_forgotten`, `rain_on_the_roof`

**Drastic:**
`loan_shark_visit`, `the_desperate_gambler`, `withdrawal_nightmare`, `casino_overdose`, `cancer_diagnosis`, `the_bridge_call`, `the_relapse`, `casino_hitman`, `the_confession`, `the_high_roller_suicide`, `the_dying_dealer`

**More Secrets:**
`the_anniversary_loss`, `survivor_guilt`, `the_scar_story`, `the_winning_streak_paranoia`, `old_gambling_buddy`

**Companion Day:** *(Same 26 as Doughman)*
**Crafted Item:** *(Same 21)*
**Item Use:** *(Same 38)*
**Hermit Chain:** *(Same 5)*
**Midnight Radio Chain:** *(Same 5)*
**Junkyard Artisan Chain:** *(Same 5)*
**Lost Dog Chain:** *(Same 5)*
**Recurring Chain Item:** *(Same 6)*
**Crossover:** *(Same 4)*
**New Crafted:** *(Same 28 as Doughman — through `guardian_angel_lethal`)*

**Car Trouble:**
`mystery_breakdown`, `flooded_engine`, `catalytic_converter_stolen`

**Car Trouble Follow-Ups:**
`engine_knock_worsens`, `broken_ball_joint_breaks`, `failing_fuel_pump_dies`, `bald_tires_hydroplane`

**Section 45 Rewritten Item:** *(Same 26 as Doughman)*
**Section 44A Wild Item Interactions:** *(Same 15 as Doughman)*
*(No wrong_item_* events at Nearly tier)*

---

## NIGHT EVENT POOLS

Night pools are rank-specific (not unified). Each rank has its own dedicated list.

### POOR NIGHT EVENTS (line 2802)
`ditched_wallet`, `went_jogging`, `woodlands_path`, `stargazing`, `stray_cat_returns`, `midnight_walk`, `raccoon_invasion`, `insomnia_night`, `peaceful_night`, `nightmare_of_losing`, `dream_of_winning`, `drowning_dream`, `nice_dream`, `nightmare`, `stray_cat_dies` (conditional), `giant_oyster_opening` (conditional), `chase_the_rabbit` (one-time)

### CHEAP NIGHT EVENTS (line 3188)
`woodlands_path`, `woodlands_river` (x2), `woodlands_field` (x2), `swamp_stroll` (x2), `midnight_snack_run`, `stargazing`, `stray_cat_returns`, `midnight_walk`, `raccoon_invasion`, `police_checkpoint`, `satellite_falling`, `peaceful_night`, `insomnia_night`, `drowning_dream`, `carbon_monoxide`, `nice_dream`, `nightmare`, `stray_cat_dies` (conditional), `stray_cat_has_kittens` (conditional), `giant_oyster_opening` (conditional), `whats_my_favorite_color` (one-time Suzy), `chase_the_second_rabbit` (one-time)

### MODEST NIGHT EVENTS (line 3618)
`woodlands_path`, `swamp_wade` (x2), `swamp_swim` (x2), `woodlands_field`, `woodlands_river`, `swamp_stroll`, `beach_stroll` (x2), `mysterious_lights`, `midnight_snack_run`, `midnight_walk`, `peaceful_night`, `insomnia_night`, `nightmare_of_losing`, `dream_of_winning`, `drowning_dream`, `nice_dream`, `nightmare`, `stray_cat_has_kittens` (conditional), `giant_oyster_opening` (conditional), `chase_the_third_rabbit` (one-time)

### RICH NIGHT EVENTS (line 3979)
`swamp_stroll`, `swamp_wade`, `swamp_swim`, `beach_stroll`, `beach_swim` (x2), `beach_dive` (x2), `city_streets` (x2), `late_night_radio`, `mysterious_lights`, `midnight_walk`, `peaceful_night`, `insomnia_night`, `nightmare_of_losing`, `dream_of_winning`, `drowning_dream`, `nice_dream`, `nightmare`, `whats_my_favorite_animal` (one-time Suzy), `chase_the_fourth_rabbit` (one-time)

### DOUGHMAN NIGHT EVENTS (line 4342)
`beach_stroll`, `beach_swim`, `beach_dive`, `city_streets`, `city_stroll` (x2), `city_park` (x2), `midnight_walk`, `peaceful_night`, `insomnia_night`, `nightmare_of_losing`, `dream_of_winning`, `drowning_dream`, `nice_dream`, `nightmare`, `chase_the_fifth_rabbit` (one-time)

### NEARLY NIGHT EVENTS (line 4671)
`woodlands_adventure`, `swamp_adventure`, `beach_adventure`, `underwater_adventure`, `city_adventure`, `midnight_walk`, `peaceful_night`, `insomnia_night`, `nightmare_of_losing`, `dream_of_winning`, `drowning_dream`, `nice_dream`, `nightmare`, `chase_the_last_rabbit` (one-time)

---

## RANKED WANDER TRACKS (event_dispatch.py, line 54)

Requires `Car` item. Player gets tracks where `rank >= track["rank"]`.

| Rank | Label | Events | Adventure |
|---|---|---|---|
| 1 | The Woodlands | `woodlands_path`, `woodlands_river`, `woodlands_field` | `woodlands_adventure` |
| 2 | The Swamp | `swamp_stroll`, `swamp_wade`, `swamp_swim` | `swamp_adventure` |
| 3 | The Beach | `beach_stroll`, `beach_boardwalk`, `beach_bonfire` | `beach_adventure` |
| 4 | The Ocean Depths | `beach_swim`, `beach_dive`, `ocean_jetty` | `underwater_adventure` |
| 5 | The City | `city_streets`, `city_stroll`, `city_park` | `city_adventure` |

---

## SPECIAL CATEGORY SETS

### `_ILLNESS_NAMES` (line 4698) — 120 entries
Stripped from raw pool and replaced by `random_illness` dispatcher.

`contract_cold`, `contract_flu`, `contract_pneumonia`, `contract_bronchitis`, `contract_strep_throat`, `contract_stomach_flu`, `contract_ear_infection`, `contract_sinus_infection`, `contract_uti`, `contract_pink_eye`, `contract_mono`, `contract_shingles`, `contract_lyme_disease`, `contract_ringworm`, `contract_scabies`, `contract_staph_infection`, `contract_tetanus`, `contract_rabies_scare`, `contract_measles`, `develop_diabetes_symptoms`, `high_blood_pressure_crisis`, `severe_allergic_reaction`, `asthma_attack`, `kidney_stones`, `gallbladder_attack`, `appendicitis_attack`, `blood_clot_in_leg`, `migraine_severe`, `vertigo_episode`, `seizure_episode`, `pancreatitis_attack`, `severe_burn_injury`, `concussion_injury`, `broken_ribs_injury`, `dislocated_shoulder`, `broken_hand`, `broken_wrist`, `broken_ankle`, `torn_acl`, `herniated_disc`, `deep_laceration`, `puncture_wound`, `second_degree_burns`, `frostbite`, `heat_stroke`, `hypothermia`, `crush_injury`, `chemical_burn`, `electrical_burn`, `whiplash_injury`, `jaw_fracture`, `skull_fracture`, `collapsed_lung`, `ruptured_spleen`, `liver_laceration`, `ruptured_eardrum`, `detached_retina`, `orbital_fracture`, `broken_nose`, `broken_collarbone`, `tooth_abscess`, `blood_poisoning`, `severe_dehydration`, `malnutrition`, `nerve_damage`, `tendon_rupture`, `muscle_tear`, `gangrene_infection`, `severe_anxiety_attack`, `severe_depression_episode`, `insomnia_chronic`, `ptsd_flashback`, `dirty_needle_stick`, `bad_oysters`, `rat_bite`, `bad_mushrooms`, `unclean_water`, `mold_exposure`, `bee_sting_allergy`, `lead_poisoning`, `asbestos_exposure`, `mercury_poisoning`, `gym_accident`, `slip_in_shower`, `fall_down_stairs`, `car_accident_minor`, `construction_site_accident`, `bar_fight_aftermath`, `kitchen_accident`, `grease_fire`, `sports_injury`, `motorcycle_crash`, `dog_attack_severe`, `pool_diving_accident`, `chemical_spill`, `electric_shock`, `workplace_injury`, `assault_aftermath`, `caught_in_fire`, `frozen_outdoors`, `heat_exhaustion_collapse`, `drug_overdose_survival`, `allergic_reaction_restaurant`, `botched_surgery`, `dental_disaster`, `gym_collapse`, `food_truck_nightmare`, `public_pool_infection`, `hiking_disaster`, `wasp_nest_encounter`, `camping_tick_bite`, `homeless_shelter_outbreak`, `prison_shiv_wound`, `daycare_plague`, `bad_tattoo_infection`, `mma_fight_aftermath`, `covid_complications`, `earthquake_injury`, `carnival_ride_accident`, `window_crash`, `trampoline_disaster`, `explosion_nearby`, `botched_piercing`, `weight_dropping`, `bad_sushi`, `coma_awakening`, `stress_breakdown`, `trauma_flashback`, `sleep_deprivation_crisis`

### `_CAR_TROUBLE_NAMES` (line 4737) — 47 entries
Stripped from raw pool and replaced by `random_car_trouble` dispatcher.

`dead_battery_afternoon`, `corroded_battery_terminals`, `battery_acid_leak`, `engine_overheating`, `check_engine_light_on`, `engine_wont_turn_over`, `strange_engine_noise`, `engine_oil_empty`, `oil_leak_spotted`, `slow_tire_leak`, `tire_blowout`, `bald_tires_noticed`, `nail_in_tire`, `headlights_burned_out`, `alternator_failing`, `fuse_blown`, `car_alarm_malfunction`, `starter_motor_grinding`, `brakes_squealing`, `brake_fluid_leak`, `abs_light_on`, `ran_out_of_gas`, `fuel_pump_whining`, `clogged_fuel_filter`, `transmission_slipping`, `stuck_in_gear`, `radiator_leak`, `thermostat_stuck`, `water_pump_failing`, `power_steering_failure`, `wheel_alignment_off`, `suspension_creaking`, `broken_ball_joint`, `exhaust_leak_loud`, `catalytic_converter_stolen`, `hail_damage`, `flooded_engine`, `windshield_cracked`, `frozen_door_locks`, `frozen_fuel_line`, `mystery_breakdown`, `key_wont_turn`, `car_wont_go_in_reverse`, `window_wont_roll_up`, `trunk_wont_close`, `gas_pedal_sticking`, `parking_brake_stuck`

### `_CAR_DEPENDENT_DAY_NAMES` (line 4753) — 56 entries
All 47 `_CAR_TROUBLE_NAMES` PLUS:
`car_battery_dead`, `flat_tire_again`, `mystery_car_problem_worsens`, `fuel_leak_fire`, `fuel_leak_fixed`, `damaged_exhaust_fixed`, `damaged_exhaust_again`, `unpaid_tickets_boot`, `booted_car_impound`

### Random Illness Injection Copies (by rank):
`[2, 2, 3, 3, 5, 6, 8]`

### Random Car Trouble Injection Copies (by rank, if has car):
`[3, 3, 3, 1, 2, 2, 3]`

---

## TONE GATE TABLE (`_DAY_EVENT_TONE`, line 4763)

Format: `[poor, cheap, modest, rich, doughman, nearly]` — weight 0 = blocked at that rank. Unlisted events default to weight 1.

### Silly / Goofy
| Event | poor | cheap | modest | rich | dough | near |
|---|---|---|---|---|---|---|
| `duck_army` | 4 | 3 | 2 | 1 | 0 | 0 |
| `sentient_sandwich` | 4 | 3 | 2 | 1 | 0 | 0 |
| `motivational_raccoon` | 4 | 3 | 2 | 1 | 0 | 0 |
| `pigeon_mafia` | 4 | 3 | 2 | 1 | 0 | 0 |
| `sock_puppet_therapist` | 4 | 3 | 2 | 1 | 0 | 0 |
| `dance_battle` | 4 | 3 | 2 | 1 | 0 | 0 |
| `alien_abduction` | 3 | 2 | 1 | 0 | 0 | 0 |
| `hungry_cow` | 3 | 3 | 2 | 1 | 0 | 0 |
| `ice_cream_truck` | 3 | 3 | 2 | 1 | 0 | 0 |
| `kid_on_bike` | 3 | 3 | 2 | 1 | 0 | 0 |
| `the_mime` | 3 | 2 | 1 | 0 | 0 | 0 |
| `opossum_in_trash` | 4 | 3 | 2 | 1 | 0 | 0 |
| `raccoon_gang_raid` | 4 | 3 | 2 | 1 | 0 | 0 |
| `sewer_rat` | 3 | 3 | 2 | 1 | 0 | 0 |
| `raccoon_raid` | 3 | 3 | 2 | 1 | 0 | 0 |
| `raccoon_invasion` | 3 | 3 | 2 | 1 | 0 | 0 |

### Mundane / Peaceful
| Event | poor | cheap | modest | rich | dough | near |
|---|---|---|---|---|---|---|
| `morning_stretch` | 3 | 3 | 2 | 1 | 0 | 0 |
| `cloud_watching` | 3 | 3 | 2 | 1 | 0 | 0 |
| `bird_droppings` | 3 | 3 | 2 | 1 | 0 | 0 |
| `car_alarm_symphony` | 3 | 3 | 2 | 1 | 0 | 0 |
| `lucky_penny` | 3 | 3 | 2 | 1 | 0 | 0 |
| `seagull_attack` | 3 | 3 | 2 | 1 | 0 | 0 |
| `motivational_graffiti` | 3 | 3 | 2 | 1 | 0 | 0 |
| `dropped_ice_cream` | 3 | 3 | 2 | 1 | 0 | 0 |
| `talking_to_yourself` | 3 | 3 | 2 | 1 | 0 | 0 |
| `wrong_number` | 3 | 3 | 2 | 1 | 0 | 0 |
| `trash_treasure` | 3 | 3 | 2 | 1 | 0 | 0 |
| `coin_flip_stranger` | 3 | 3 | 2 | 1 | 0 | 0 |
| `stray_cat` | 3 | 3 | 2 | 1 | 0 | 0 |
| `three_legged_dog` | 3 | 3 | 2 | 1 | 0 | 0 |
| `estranged_dog` | 3 | 3 | 2 | 1 | 0 | 0 |
| `radio_static` | 3 | 3 | 2 | 1 | 0 | 0 |
| `mysterious_note` | 3 | 3 | 2 | 1 | 0 | 0 |
| `ant_invasion` | 3 | 3 | 2 | 1 | 0 | 0 |
| `left_window_down` | 3 | 3 | 2 | 1 | 0 | 0 |
| `vending_machine_luck` | 3 | 3 | 2 | 1 | 0 | 0 |
| `conspiracy_theorist` | 3 | 3 | 2 | 0 | 0 | 0 |
| `freight_truck` | 3 | 3 | 2 | 1 | 0 | 0 |
| `roadkill_philosophy` | 3 | 2 | 1 | 0 | 0 | 0 |
| `street_musician` | 2 | 2 | 1 | 0 | 0 | 0 |
| `deja_vu_again` | 2 | 2 | 1 | 0 | 0 | 0 |
| `car_wash_encounter` | 2 | 2 | 1 | 0 | 0 | 0 |
| `mosquito_bite_infection` | 3 | 2 | 1 | 0 | 0 | 0 |
| `got_a_tan` | 3 | 3 | 2 | 1 | 0 | 0 |

### Small Everyday Struggles
| Event | poor | cheap | modest | rich | dough | near |
|---|---|---|---|---|---|---|
| `good_hair_day` | 2 | 2 | 2 | 1 | 1 | 0 |
| `bad_hair_day` | 2 | 2 | 2 | 1 | 1 | 0 |
| `nice_weather` | 2 | 2 | 2 | 1 | 1 | 0 |
| `terrible_weather` | 2 | 2 | 2 | 1 | 1 | 0 |
| `back_pain` | 2 | 2 | 2 | 1 | 1 | 0 |
| `stretching_helps` | 2 | 2 | 2 | 1 | 1 | 0 |
| `weird_noise` | 2 | 2 | 2 | 1 | 0 | 0 |
| `found_twenty` | 2 | 2 | 2 | 1 | 0 | 0 |
| `lost_wallet` | 2 | 2 | 2 | 1 | 0 | 0 |
| `sunburn` | 2 | 2 | 2 | 1 | 0 | 0 |
| `flat_tire` | 2 | 2 | 1 | 0 | 0 | 0 |
| `flat_tire_again` | 2 | 2 | 1 | 0 | 0 | 0 |
| `car_battery_dead` | 2 | 2 | 1 | 0 | 0 | 0 |
| `found_gift_card` | 2 | 2 | 2 | 1 | 0 | 0 |
| `random_kindness` | 2 | 2 | 2 | 1 | 1 | 0 |
| `random_cruelty` | 2 | 2 | 2 | 2 | 1 | 1 |
| `someone_stole_your_stuff` | 2 | 2 | 2 | 1 | 0 | 0 |
| `prayer_answered` | 2 | 2 | 2 | 2 | 2 | 2 |
| `prayer_ignored` | 2 | 2 | 2 | 2 | 2 | 2 |
| `found_old_photo` | 2 | 2 | 2 | 1 | 1 | 1 |
| `threw_out_old_photo` | 1 | 1 | 2 | 2 | 2 | 1 |
| `morning_fog` | 2 | 2 | 2 | 1 | 0 | 0 |
| `car_wont_start` | 2 | 2 | 1 | 0 | 0 | 0 |
| `strong_winds` | 2 | 2 | 2 | 1 | 0 | 0 |
| `beautiful_sunrise` | 2 | 2 | 2 | 1 | 1 | 0 |

### Poor/Cheap Specific
| Event | poor | cheap | modest | rich | dough | near |
|---|---|---|---|---|---|---|
| `seat_cash` | 3 | 0 | 0 | 0 | 0 | 0 |
| `sun_visor_bills` | 2 | 3 | 1 | 0 | 0 | 0 |
| `fortune_cookie` | 2 | 2 | 1 | 0 | 0 | 0 |
| `broken_atm` | 2 | 2 | 1 | 0 | 0 | 0 |
| `lottery_scratch` | 2 | 2 | 1 | 0 | 0 | 0 |
| `parking_lot_poker` | 2 | 2 | 1 | 0 | 0 | 0 |
| `free_sample_spree` | 2 | 2 | 1 | 0 | 0 | 0 |
| `phone_scam_call` | 2 | 2 | 1 | 0 | 0 | 0 |
| `yard_sale_find` | 2 | 2 | 1 | 0 | 0 | 0 |
| `friendly_drunk` | 2 | 2 | 1 | 0 | 0 | 0 |
| `completely_broke_wisdom` | 3 | 1 | 0 | 0 | 0 | 0 |
| `rock_bottom` | 2 | 2 | 1 | 0 | 0 | 0 |
| `grimy_gus_discovery` | 1 | 3 | 3 | 2 | 0 | 0 |
| `vinnie_referral_card` | 3 | 4 | 3 | 2 | 1 | 0 |
| `windblown_worn_map` | 2 | 5 | 4 | 2 | 0 | 0 |
| `flea_market_route_map` | 1 | 4 | 4 | 2 | 0 | 0 |
| `laundromat_bulletin_map` | 0 | 3 | 4 | 2 | 0 | 0 |
| `witch_doctor_matchbook` | 0 | 1 | 2 | 1 | 0 | 0 |
| `roadside_bone_chimes` | 0 | 1 | 2 | 1 | 0 | 0 |
| `trusty_tom_coupon_mailer` | 0 | 2 | 2 | 1 | 0 | 0 |
| `filthy_frank_radio_giveaway` | 0 | 1 | 2 | 1 | 0 | 0 |
| `oswald_concierge_card` | 0 | 1 | 1 | 1 | 0 | 0 |

### Gritty Danger
| Event | poor | cheap | modest | rich | dough | near |
|---|---|---|---|---|---|---|
| `back_alley_shortcut` | 1 | 1 | 2 | 3 | 0 | 0 |
| `food_poisoning` | 1 | 1 | 2 | 2 | 1 | 0 |
| `attacked_by_dog` | 1 | 1 | 1 | 0 | 0 | 0 |
| `carbon_monoxide` | 1 | 1 | 2 | 2 | 2 | 1 |
| `gas_station_robbery` | 0 | 1 | 1 | 1 | 0 | 0 |
| `drug_dealer_encounter` | 0 | 1 | 2 | 3 | 3 | 2 |
| `electrocution_hazard` | 0 | 1 | 1 | 1 | 0 | 0 |
| `car_explosion` | 0 | 1 | 1 | 2 | 2 | 1 |
| `heart_attack_scare` | 0 | 0 | 1 | 2 | 3 | 4 |

### Dark / Horror
| Event | poor | cheap | modest | rich | dough | near |
|---|---|---|---|---|---|---|
| `blood_moon_bargain` | 0 | 0 | 1 | 2 | 3 | 4 |
| `the_empty_room` | 0 | 0 | 1 | 2 | 3 | 4 |
| `the_dying_dealer` | 0 | 0 | 0 | 1 | 3 | 3 |
| `the_high_roller_suicide` | 0 | 0 | 0 | 0 | 2 | 4 |
| `casino_hitman` | 0 | 0 | 0 | 0 | 0 | 4 |
| `organ_harvester` | 0 | 0 | 0 | 1 | 3 | 3 |
| `the_bridge_call` | 0 | 0 | 0 | 1 | 3 | 4 |
| `the_relapse` | 0 | 0 | 0 | 1 | 3 | 4 |
| `cancer_diagnosis` | 0 | 0 | 0 | 1 | 3 | 3 |
| `casino_overdose` | 0 | 0 | 0 | 1 | 3 | 3 |
| `withdrawal_nightmare` | 0 | 0 | 0 | 1 | 3 | 3 |
| `the_desperate_gambler` | 0 | 0 | 0 | 1 | 3 | 3 |
| `loan_shark_visit` | 0 | 0 | 0 | 1 | 3 | 3 |
| `likely_death` | 0 | 0 | 0 | 0 | 3 | 0 |
| `the_confession` | 0 | 0 | 0 | 1 | 2 | 3 |
| `the_anniversary_loss` | 0 | 0 | 0 | 1 | 2 | 3 |
| `survivor_guilt` | 0 | 0 | 0 | 1 | 2 | 3 |
| `the_scar_story` | 0 | 0 | 0 | 1 | 2 | 2 |
| `the_winning_streak_paranoia` | 0 | 0 | 0 | 1 | 2 | 3 |
| `old_gambling_buddy` | 0 | 0 | 0 | 1 | 2 | 2 |

### Surreal / Existential
| Event | poor | cheap | modest | rich | dough | near |
|---|---|---|---|---|---|---|
| `time_loop` | 1 | 1 | 2 | 2 | 3 | 3 |
| `mirror_stranger` | 1 | 1 | 2 | 2 | 3 | 3 |
| `the_glitch` | 1 | 1 | 2 | 2 | 3 | 3 |
| `fourth_wall_break` | 1 | 1 | 2 | 2 | 3 | 3 |
| `wrong_universe` | 1 | 1 | 2 | 2 | 0 | 0 |
| `the_collector` | 0 | 0 | 1 | 2 | 3 | 3 |
| `soulless_emptiness` | 0 | 0 | 1 | 1 | 3 | 3 |
| `soulless_mirror` | 0 | 0 | 1 | 1 | 3 | 3 |
| `soulless_recognition` | 0 | 0 | 1 | 1 | 3 | 3 |
| `haunted_by_losses` | 0 | 0 | 1 | 1 | 3 | 3 |
| `wealth_anxiety` | 0 | 0 | 1 | 1 | 3 | 3 |
| `bridge_contemplation` | 0 | 0 | 1 | 1 | 3 | 4 |
| `devils_bargain_consequence` | 0 | 0 | 0 | 1 | 3 | 4 |
| `insomniac_revelation` | 1 | 1 | 1 | 2 | 2 | 2 |
| `the_sleeping_stranger` | 2 | 2 | 1 | 1 | 0 | 0 |
| `the_cat_knows` | 1 | 1 | 1 | 1 | 1 | 1 |
| `rain_on_the_roof` | 1 | 1 | 1 | 1 | 1 | 1 |
| `found_old_photo` | 2 | 2 | 2 | 1 | 1 | 1 |
| `perfect_health_moment` | 1 | 1 | 1 | 1 | 1 | 1 |
| `first_sunrise` | 2 | 1 | 1 | 1 | 1 | 0 |
| `the_veteran_gambler` | 0 | 1 | 1 | 1 | 2 | 2 |
| `the_crow_council` | 0 | 1 | 1 | 1 | 2 | 2 |
| `birthday_forgotten` | 0 | 0 | 0 | 1 | 2 | 2 |
| `item_hoarder` | 0 | 0 | 1 | 1 | 2 | 2 |
| `companion_reunion` | 0 | 1 | 1 | 1 | 1 | 1 |
| `empty_event` | 2 | 2 | 2 | 1 | 1 | 0 |

### Chain / Conditional
| Event | poor | cheap | modest | rich | dough | near |
|---|---|---|---|---|---|---|
| `starving_cow` | 0 | 1 | 2 | 0 | 0 | 0 |
| `cow_army` | 0 | 0 | 0 | 0 | 2 | 1 |
| `even_further_interrogation` | 0 | 0 | 0 | 1 | 1 | 0 |

### Wealth-Tier Mid (modest/rich)
| Event | poor | cheap | modest | rich | dough | near |
|---|---|---|---|---|---|---|
| `luxury_car_passes` | 0 | 0 | 2 | 4 | 2 | 1 |
| `paparazzi_mistake` | 0 | 0 | 2 | 4 | 2 | 1 |
| `imposter_syndrome` | 0 | 0 | 2 | 4 | 2 | 1 |
| `charity_opportunity` | 0 | 0 | 2 | 4 | 2 | 1 |
| `investment_opportunity` | 0 | 0 | 2 | 4 | 2 | 1 |
| `expensive_taste` | 0 | 0 | 2 | 4 | 2 | 1 |
| `autograph_request` | 0 | 0 | 1 | 4 | 2 | 1 |
| `casino_regular` | 0 | 0 | 1 | 4 | 2 | 1 |
| `mysterious_package` | 0 | 0 | 1 | 3 | 2 | 1 |
| `rich_persons_problems` | 0 | 0 | 1 | 4 | 2 | 1 |
| `investment_pitch` | 0 | 0 | 1 | 4 | 2 | 1 |
| `news_van` | 0 | 0 | 1 | 3 | 2 | 1 |
| `fancy_restaurant_mistake` | 0 | 0 | 2 | 4 | 2 | 1 |
| `luxury_problems` | 0 | 0 | 2 | 4 | 2 | 1 |
| `left_trunk_open` | 0 | 0 | 1 | 3 | 2 | 1 |
| `classy_encounter` | 0 | 0 | 0 | 4 | 2 | 1 |
| `wine_and_dine` | 0 | 0 | 0 | 4 | 2 | 1 |
| `cigar_circle` | 0 | 0 | 0 | 4 | 2 | 1 |
| `lucky_rabbit_encounter` | 0 | 0 | 0 | 4 | 2 | 1 |
| `old_rival_encounter` | 0 | 0 | 1 | 2 | 2 | 1 |
| `media_known_harassed` | 0 | 0 | 1 | 1 | 2 | 1 |
| `media_known_documentary` | 0 | 0 | 1 | 1 | 2 | 1 |
| `high_roller_room_visit` | 0 | 0 | 0 | 3 | 3 | 2 |
| `high_roller_whale` | 0 | 0 | 0 | 3 | 3 | 2 |

### Wealth-Tier High (doughman/nearly)
| Event | poor | cheap | modest | rich | dough | near |
|---|---|---|---|---|---|---|
| `reporters_found_you` | 0 | 0 | 0 | 1 | 3 | 4 |
| `casino_knows` | 0 | 0 | 0 | 0 | 3 | 4 |
| `casino_owner_meeting` | 0 | 0 | 0 | 0 | 3 | 4 |
| `almost_there` | 0 | 0 | 0 | 0 | 2 | 4 |
| `the_weight_of_wealth` | 0 | 0 | 0 | 0 | 3 | 4 |
| `wealth_paranoia` | 0 | 0 | 0 | 1 | 3 | 4 |
| `millionaire_fantasy` | 0 | 0 | 0 | 0 | 3 | 3 |
| `high_roller_room` | 0 | 0 | 0 | 0 | 3 | 3 |
| `last_stretch` | 0 | 0 | 0 | 0 | 0 | 4 |
| `strange_visitors` | 0 | 0 | 0 | 0 | 2 | 4 |
| `the_final_temptation` | 0 | 0 | 0 | 0 | 2 | 4 |
| `high_stakes_feeling` | 0 | 0 | 0 | 0 | 3 | 4 |
| `casino_security` | 0 | 0 | 0 | 1 | 3 | 3 |
| `wealthy_doubts` | 0 | 0 | 0 | 1 | 3 | 3 |
| `people_watching` | 0 | 0 | 0 | 1 | 2 | 2 |
| `money_counting_ritual` | 0 | 0 | 0 | 0 | 3 | 3 |
| `nervous_habits` | 0 | 0 | 0 | 1 | 3 | 3 |
| `millionaire_milestone` | 0 | 0 | 0 | 0 | 3 | 3 |
| `old_rival_returns` | 0 | 0 | 0 | 1 | 3 | 2 |
| `casino_comps` | 0 | 0 | 0 | 0 | 3 | 3 |
| `thunderstorm` | 0 | 0 | 0 | 1 | 3 | 4 |
| `too_close_to_quit` | 0 | 0 | 0 | 0 | 0 | 3 |

### Crafted Item Events
| Event | poor | cheap | modest | rich | dough | near |
|---|---|---|---|---|---|---|
| `headlamp_night_walk` | 1 | 2 | 2 | 2 | 1 | 1 |
| `spotlight_hidden_path` | 1 | 2 | 2 | 2 | 1 | 1 |
| `evidence_kit_crime` | 0 | 1 | 2 | 2 | 2 | 1 |
| `radio_jammer_checkpoint` | 0 | 1 | 2 | 2 | 2 | 1 |
| `emp_device_pursuit` | 0 | 0 | 1 | 2 | 2 | 2 |
| `security_bypass_locked_room` | 0 | 1 | 2 | 2 | 2 | 1 |
| `gentleman_charm_dinner` | 0 | 1 | 2 | 2 | 2 | 1 |
| `forged_documents_police` | 1 | 1 | 2 | 2 | 2 | 1 |
| `brass_knuckles_brawl` | 1 | 2 | 2 | 2 | 1 | 1 |
| `gas_mask_chemical` | 0 | 1 | 2 | 2 | 1 | 1 |
| `stink_bomb_escape` | 1 | 2 | 2 | 2 | 1 | 1 |
| `animal_bait_companion` | 1 | 2 | 2 | 1 | 1 | 0 |
| `trail_mix_bomb_distraction` | 1 | 2 | 2 | 1 | 1 | 0 |
| `voice_soother_persuasion` | 0 | 1 | 2 | 2 | 1 | 1 |
| `eldritch_candle_entity` | 0 | 0 | 1 | 2 | 3 | 3 |
| `devils_deck_gambling` | 0 | 1 | 2 | 2 | 2 | 1 |
| `fortune_cards_warning` | 0 | 1 | 2 | 2 | 2 | 1 |
| `blackmail_letter_extortion` | 0 | 0 | 1 | 2 | 2 | 2 |
| `kingpin_look_respect` | 0 | 0 | 1 | 2 | 2 | 2 |
| `heirloom_set_recognition` | 0 | 0 | 1 | 2 | 2 | 2 |
| `luck_totem_windfall` | 0 | 1 | 2 | 2 | 2 | 1 |
| `tire_ready_flat` | 1 | 2 | 2 | 2 | 1 | 1 |
| `miracle_lube_breakdown` | 1 | 2 | 2 | 2 | 1 | 1 |
| `road_warrior_ambush` | 0 | 0 | 1 | 2 | 2 | 2 |
| `third_eye_foresight` | 0 | 0 | 1 | 2 | 2 | 2 |
| `ghost_protocol_invisible` | 0 | 0 | 0 | 1 | 2 | 3 |
| `immortal_vehicle_breakdown` | 0 | 0 | 0 | 1 | 2 | 3 |
| `gamblers_aura_blackjack` | 0 | 0 | 1 | 2 | 2 | 2 |
| `guardian_angel_lethal` | 0 | 0 | 0 | 0 | 2 | 3 |

### Section 45 Rewritten Item Events
| Event | poor | cheap | modest | rich | dough | near |
|---|---|---|---|---|---|---|
| `low_profile_casino_blend` | 0 | 1 | 2 | 2 | 1 | 1 |
| `low_profile_police_encounter` | 0 | 1 | 2 | 2 | 1 | 1 |
| `low_profile_mugging_marcus` | 0 | 1 | 2 | 2 | 1 | 1 |
| `low_profile_shelter_meal` | 1 | 1 | 2 | 1 | 0 | 0 |
| `beach_bum_yacht_party` | 0 | 0 | 1 | 2 | 2 | 1 |
| `beach_bum_heatwave` | 1 | 1 | 2 | 1 | 1 | 1 |
| `beach_bum_tribe` | 1 | 1 | 2 | 1 | 1 | 1 |
| `gas_mask_toxic_spill` | 0 | 0 | 1 | 2 | 2 | 1 |
| `gas_mask_fire_rescue` | 0 | 0 | 1 | 2 | 2 | 1 |
| `storm_suit_hurricane` | 0 | 1 | 2 | 2 | 1 | 1 |
| `storm_suit_flood` | 0 | 1 | 2 | 2 | 1 | 1 |
| `storm_suit_night_bear` | 0 | 1 | 2 | 2 | 1 | 1 |
| `antacid_business_dinner` | 0 | 1 | 2 | 2 | 1 | 1 |
| `outdoor_shield_farmer` | 1 | 1 | 2 | 2 | 1 | 1 |
| `cool_down_car_overheat` | 1 | 1 | 2 | 2 | 1 | 1 |
| `smoke_flare_pursuit` | 0 | 1 | 2 | 2 | 1 | 1 |
| `vermin_bomb_car` | 1 | 1 | 2 | 1 | 1 | 1 |
| `enchanted_vintage_party` | 0 | 0 | 1 | 2 | 2 | 2 |
| `aristocrat_cold_elegance` | 0 | 0 | 0 | 2 | 2 | 2 |
| `power_move_intimidation` | 0 | 0 | 1 | 2 | 2 | 1 |
| `animal_magnetism_recruit` | 0 | 0 | 1 | 2 | 2 | 1 |
| `animal_magnetism_predator` | 0 | 0 | 1 | 2 | 2 | 1 |
| `power_grid_dead_battery` | 0 | 0 | 1 | 2 | 2 | 1 |
| `mobile_workshop_stranger` | 0 | 0 | 1 | 2 | 2 | 1 |
| `pursuit_package_chase` | 0 | 0 | 1 | 2 | 2 | 1 |
| `pursuit_package_witness` | 0 | 0 | 1 | 2 | 2 | 1 |

### Wild Item Interactions
| Event | poor | cheap | modest | rich | dough | near |
|---|---|---|---|---|---|---|
| `wild_headlamp_poker` | 1 | 2 | 2 | 1 | 1 | 1 |
| `wild_emp_casino` | 0 | 0 | 1 | 2 | 2 | 1 |
| `wild_radio_jammer_police` | 0 | 0 | 1 | 2 | 2 | 1 |
| `wild_evidence_kit_wedding` | 0 | 1 | 2 | 2 | 1 | 1 |
| `wild_distress_beacon_casino` | 0 | 0 | 1 | 2 | 2 | 1 |
| `wild_stink_bomb_casino_vault` | 0 | 0 | 1 | 2 | 2 | 1 |
| `wild_gas_mask_funeral` | 0 | 1 | 2 | 2 | 1 | 1 |
| `wild_eldritch_candle_gambling` | 0 | 0 | 1 | 2 | 2 | 1 |
| `wild_devil_deck_children` | 0 | 1 | 2 | 2 | 1 | 1 |
| `wild_binding_portrait_shopkeeper` | 0 | 0 | 1 | 2 | 2 | 1 |
| `wild_fortune_cards_car` | 1 | 1 | 2 | 2 | 1 | 1 |
| `wild_blackmail_letter_companion` | 0 | 0 | 1 | 2 | 2 | 1 |
| `lottery_ticket_check` | 2 | 2 | 1 | 1 | 1 | 1 |

### Wrong Item Comedy
| Event | poor | cheap | modest | rich | dough | near |
|---|---|---|---|---|---|---|
| `wrong_item_bug_spray_campfire` | 1 | 1 | 1 | 0 | 0 | 0 |
| `wrong_item_road_flares_stealth` | 1 | 1 | 1 | 0 | 0 | 0 |
| `wrong_item_pest_control_romance` | 0 | 1 | 1 | 1 | 0 | 0 |
| `wrong_item_vermin_bomb_romance` | 0 | 1 | 1 | 1 | 0 | 0 |
| `wrong_item_dirty_hat_dinner` | 0 | 0 | 1 | 1 | 1 | 0 |
| `wrong_item_dog_whistle_bear` | 1 | 1 | 1 | 0 | 0 | 0 |
| `wrong_item_necronomicon_loan_shark` | 0 | 0 | 1 | 1 | 1 | 0 |
| `necronomicon_reading` | 0 | 0 | 1 | 1 | 1 | 0 |

---

## INVENTORY POOL WEIGHT MODIFIERS (`_apply_inventory_pool_weights`, line 5129)

### Night-time Adjustments
| Item | Effect | Target Events |
|---|---|---|
| Dream Catcher | Remove 1 copy each | `_NIGHTMARE_EVENTS` + `_DARK_NIGHT_EVENTS` |
| Road Flare Torch | Remove 1 copy each | `_DARK_NIGHT_EVENTS` |
| Flask "Fortunate Night" | +1 copy each | `_POSITIVE_NIGHT_EVENTS` |
| Necronomicon | +2 copies each | `_DARK_NIGHT_EVENTS` |
| Animal Whistle | +2 copies each | `_ANIMAL_EVENTS` |
| Nomad's Camp | +3 copies each | `_CAMP_EVENTS` |
| Gambler's Aura | +1 copy each | `_POSITIVE_NIGHT_EVENTS` |
| Ghost Protocol | Remove all | `_COMBAT_EVENTS` |

### Day-time Adjustments
| Item | Effect | Target Events |
|---|---|---|
| Necronomicon | +2 copies each | `_DARK_DAY_EVENTS` |
| Animal Whistle | +2 copies each | `_ANIMAL_EVENTS` |
| Lucky Charm Bracelet | +1 copy each | `_POSITIVE_DAY_EVENTS` |
| Luck Totem | +1 copy each (stacks) | `_POSITIVE_DAY_EVENTS` |
| Flask "Fortunate Day" | +1 copy each | `_POSITIVE_DAY_EVENTS` |
| Fire Starter Kit | +2 copies each | `_CAMP_EVENTS` |
| Scrap Armor | Remove all | `_COMBAT_EVENTS` |
| Gambler's Aura | +2 copies each | `_POSITIVE_DAY_EVENTS` |
| Fortune's Favor | +1 copy each (stacks) | `_POSITIVE_DAY_EVENTS` |
| Beast Tamer Kit | +2 copies each | `_ANIMAL_EVENTS` |
| Nomad's Camp | +3 copies each | `_CAMP_EVENTS` |
| Ghost Protocol | Remove all | `_COMBAT_EVENTS` |
| Road Warrior Armor | Remove all | `_COMBAT_EVENTS` |

### Event Category Sets
**`_ANIMAL_EVENTS`:** `duck_army`, `motivational_raccoon`, `pigeon_mafia`, `raccoon_gang_raid`, `raccoon_raid`, `raccoon_invasion`, `opossum_in_trash`, `stray_cat`, `three_legged_dog`, `estranged_dog`, `bird_droppings`, `seagull_attack`, `sewer_rat`, `hungry_cow`, `attacked_by_dog`, `stray_cat_returns`

**`_POSITIVE_DAY_EVENTS`:** `lucky_penny`, `found_twenty`, `found_gift_card`, `vending_machine_luck`, `prayer_answered`, `random_kindness`, `good_hair_day`, `nice_weather`, `beautiful_sunrise`, `found_old_photo`, `morning_stretch`

**`_DARK_DAY_EVENTS`:** `blood_moon_bargain`, `the_empty_room`, `the_dying_dealer`, `organ_harvester`, `the_bridge_call`, `the_relapse`, `casino_overdose`, `withdrawal_nightmare`, `loan_shark_visit`, `the_confession`, `the_anniversary_loss`, `survivor_guilt`, `the_scar_story`

**`_COMBAT_EVENTS`:** `gas_station_robbery`, `back_alley_shortcut`, `drug_dealer_encounter`, `car_explosion`

**`_CAMP_EVENTS`:** `fire_starter_campfire`

**`_NIGHTMARE_EVENTS`:** `nightmare`, `nightmare_of_losing`, `drowning_dream`, `companion_nightmare`

**`_DARK_NIGHT_EVENTS`:** `blood_moon_bargain`, `the_empty_room`, `organ_harvester`, `withdrawal_nightmare`

**`_POSITIVE_NIGHT_EVENTS`:** `peaceful_night`, `nice_dream`, `dream_of_winning`, `stargazing`, `woodlands_path`, `woodlands_river`, `woodlands_field`, `midnight_walk`
