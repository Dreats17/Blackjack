# Item Tier List

> **Blackjack** — you live in your car, survive the days, and play Blackjack at night.
> This document covers every item's mechanical interactions: what you avoid with it, what you gain, and what it costs you when you don't have it.

---

## Tier Definitions

| Tier | Meaning |
|------|---------|
| **S** | Prevents major negative events OR enables major positive chains. Interactions across multiple files. |
| **A** | Meaningfully changes the outcome of 2–5 events. Usually consumable or dual-purpose. |
| **B** | Changes the outcome of one specific event. Single-use or niche but real. |
| **C** | Collectible with a dedicated one-time event OR appears in the daily passive flavor pool. Sell to Gus for real money. |
| **D** | Pure collectible. Sell to Gus. No mechanical effect. |

---

## S Tier

---

### Pest Control
**How to get:** General store / roadside shop  
**Consumed:** No (sprays last the whole game)

| Event | File | Without | With |
|-------|------|---------|------|
| `raccoon_invasion` | events_night.py | Food stolen, sanity loss | Raccoons scatter — clean |
| `spider_bite` | events_day_survival.py | Spider remains, sanity−1–2 | `kill_pests()`, spider gone |
| `another_spider_bite` | events_day_survival.py | Repeat bite | `kill_pests()`, cleared |
| `hungry_cockroach` | events_day_survival.py | Cockroach infestation added | `kill_pests()`, cleared |
| `ant_invasion` | events_day_survival.py | Ants danger added | `kill_pests()`, ants gone |
| `ant_bite` | events_day_survival.py | `hurt(20)` | `hurt(10)` (halved) |
| `left_door_open` | events_day_survival.py | Pests possibly enter | Precautionary spray |
| `left_trunk_open` | events_day_survival.py | Pests infest trunk | Trunk sprayed clean |
| `rat_bite` | events_day_animals.py | Rat infestation | `kill_pests()`, cleared |
| `hungry_termites` | events_day_animals.py | Termite damage | `kill_pests()`, cleared |
| `update_status` | game_flow.py | Camping blocked if pests present | Camping allowed |

**Summary:** Pest Control is arguably the single most impactful item in the game. It blocks an entire class of events and keeps the camping buff active.

---

### Spare Tire
**How to get:** Auto parts store, pawn shop  
**Consumed:** Yes (on use)  
**Best with:** Car Jack (see below)

| Event | File | Without | With |
|-------|------|---------|------|
| `tire_blowout` (with Car Jack) | events_car.py | — | Free fix, `sanity+10` |
| `tire_blowout` (no Car Jack) | events_car.py | `change_balance(−$150)`, travel restricted | Travel restricted (but no cost) |
| `tire_blowout` (neither) | events_car.py | `change_balance(−$150)`, `lose_sanity(15)`, stranded | — |
| `nail_in_tire` | events_car.py | `add_travel_restriction`, `lose_sanity(10)` | Changed out, travel restriction avoided |
| `nail_in_tire_blows` | events_car.py | `lose_sanity(10)`, stranded | Used, gets you moving |
| `flat_tire` | events_day_survival.py | `change_balance(−$50–150)`, travel restricted | Quick swap, no cost |
| `flat_tire_again` | events_day_survival.py | Left with no options | 20-minute fix |

**Summary:** Tires go flat constantly. Without a spare you're paying $50–200 every time and losing the day. Having both a Spare Tire AND Car Jack is worth stacking.

---

### Car Jack
**How to get:** Auto parts store  
**Consumed:** No

| Event | File | Without | With (paired w/ Spare Tire) |
|-------|------|---------|------|
| `tire_blowout` | events_car.py | Can't change tire alone | `sanity+10`, free fix in ~1 hour |

**Note:** On its own the Car Jack does nothing. Paired with a Spare Tire it converts a `$150 + sanity−15` tow call into a free fix with a sanity bonus.

---

### Tool Kit
**How to get:** Hardware store, auto parts store  
**Consumed:** No

| Event | File | Without | With |
|-------|------|---------|------|
| `engine_wont_turn_over` | events_car.py | `add_travel_restriction`, `add_danger("Engine Damage")`, `lose_sanity(12)` | DIY fix, `sanity+5` |
| `car_alarm_malfunction` | events_car.py | `add_travel_restriction`, `lose_sanity(20)` | Disconnect battery, `sanity+8` |
| `parking_brake_stuck` | events_car.py | `add_travel_restriction`, `add_danger("Stuck Parking Brake")`, `lose_sanity(10)` | Manual release, downgraded danger only |
| `car_battery_dead` | events_day_survival.py | Stranded | Jump cables from kit, `sanity+5` |
| `road_adventure` | adventures.py | Duct Tape fallback | Tool Kit preferred, better outcome |
| `lost_dog_whistle_search` | events_day_storylines.py | Harder pry | Pry latch open, `sanity+8` |

**Summary:** Every car crisis that could leave you stranded or bleeding sanity has a Tool Kit exit. High-priority buy.

---

### Pocket Knife
**How to get:** General store, pawn shop  
**Consumed:** Only in `city_stroll` (used as weapon)

| Event | File | Without | With |
|-------|------|---------|------|
| `robbery_attempt` | events_day_people.py | Lose `$50–200` | Brandish knife, thief runs — no loss |
| `lockpick_opportunity` | events_day_items.py | Can't open the box | Pry lock, loot inside |
| `lockbox_contents` | events_day_items.py | `change_balance(−$20)` to open | Wedge open free |
| `lost_dog_whistle_search` | events_day_storylines.py | Harder option | Pry latch, `sanity+8` |
| `city_stroll` | events_night.py | Mugger succeeds | Fight off mugger (item consumed) |
| `has_cutting_tool()` | player_core.py | `False` | `True` — unlocks cutting checks |

---

### Cough Drops
**How to get:** Pharmacy, general store  
**Consumed:** Yes (on use)

| Event | File | Without | With |
|-------|------|---------|------|
| `sore_throat` | events_day_survival.py | `add_status("Sore Throat")`, marked for the day | Cured instantly, item consumed |
| `got_a_cold` | events_day_survival.py | Cold worsens | Symptom blunted |
| `companion_sick_day` | events_day_companions.py | Companion suffers longer | Shared with companion, recovery |
| `update_status` | game_flow.py | Cold blocks camping bonus | With drops, camping still works |

**Summary:** The Sore Throat status snowballs quickly. A box of Cough Drops is cheap insurance.

---

### First Aid Kit
**How to get:** Pharmacy, general store  
**Consumed:** Yes — auto-consumed when damage ≥ 15

| Event / System | File | Without | With |
|----------------|------|---------|------|
| `hurt()` passive | player_core.py | Full damage taken | Any hit ≥ 15: **auto-triggered**, damage halved |
| `mosquito_bite_infection` | events_day_survival.py | `hurt(10)` | `hurt(3)`, `sanity+3` |
| `back_pain` | events_day_survival.py | `hurt(15)`, immobile | Treated, `hurt` reduced |

**Summary:** The passive auto-trigger is what makes this S tier. Any large hit is automatically halved if you're carrying a First Aid Kit. You don't have to do anything — it just fires.

---

## A Tier

---

### Hand Warmers
**How to get:** General store, camping supply  
**Consumed:** Yes

| Event | File | Without | With |
|-------|------|---------|------|
| `freezing_night` | events_day_survival.py | `hurt(15–25)`, 25% chance `add_status("Cold")` | Zero damage, comfortable night |

**Best cold-night item.** Fire source (Lighter etc.) gives `hurt(5)`. Blanket gives `hurt(8)`. Hand Warmers are the only way out clean.

---

### Blanket
**How to get:** Storyline gift, general store  
**Consumed:** No

| Event | File | Without | With |
|-------|------|---------|------|
| `freezing_night` | events_day_survival.py | `hurt(15–25)` | `hurt(8)` — survivable |

**Fallback tier** for cold nights when you have no fire source or Hand Warmers.

---

### Umbrella
**How to get:** General store  
**Consumed:** No

| Event | File | Without | With |
|-------|------|---------|------|
| `scorching_sun` | events_day_survival.py | `hurt(15–25)` | `hurt(5)` only |
| `sunburn` | events_day_survival.py | Sunburn status added | Protected |
| `sudden_downpour` | events_day_survival.py | `hurt(10)` | Dry, no damage |
| `thunderstorm` | events_day_survival.py | Soaked, sanity loss | Sheltered |

---

### Plastic Poncho / Poncho
**How to get:** General store (Plastic Poncho cheap; Poncho mid-tier)  
**Consumed:** No

| Event | File | Without | With |
|-------|------|---------|------|
| `sudden_downpour` | events_day_survival.py | `hurt(10)` | Dry, no damage |
| `thunderstorm` | events_day_survival.py | Soaked | Gear up, protected |
| `freezing_night` (fire tier) | events_day_survival.py | — | Acts as fire-source tier: `hurt(5)` |

---

### Road Flares
**How to get:** General store, auto parts  
**Consumed:** Yes (on use in roadside events)

| Event | File | Without | With |
|-------|------|---------|------|
| `roadside_breakdown` | events_day_survival.py | `change_balance(−$100–200)`, travel restricted | Trucker helps, flares consumed — no cost |
| `need_fire` | events_day_survival.py | `hurt(10)`, `lose_sanity(3)` | Fire lit, item consumed |
| `has_fire_source()` | player_core.py | `False` | `True` — counts as fire |

---

### Lighter / Monogrammed Lighter / Matches
**How to get:** General store / story event (Monogrammed Lighter)  
**Consumed:** Lighter: 20% chance per use consumed; Monogrammed Lighter: never consumed; Matches: consumed

| Event | File | Without | With |
|-------|------|---------|------|
| `frozen_door_locks` | events_car.py | `add_travel_restriction`, `hurt(5)` | Heat key, fix it, `sanity+3` |
| `need_fire` | events_day_survival.py | `hurt(10)`, `lose_sanity(3)` | Fire lit |
| `has_fire_source()` | player_core.py | `False` | `True` |

**Monogrammed Lighter** is strictly better — identical function, never runs out.

---

### Flashlight
**How to get:** General store  
**Consumed:** No

| Event | File | Without | With |
|-------|------|---------|------|
| `trap_night_thief` | events_day_items.py | `sanity+2` (lucky) | Catch thief in the beam, full resolution |
| `road_flare_torch_encounter` | events_day_items.py | `lose_sanity(3–5)` | Sweep beam, no loss |
| `roadside_breakdown` | events_day_survival.py | `change_balance(−$100–200)`, stranded | Flag cars down, travel restricted (partial) |

---

### WD-40
**How to get:** Hardware store, auto parts  
**Consumed:** Yes (on use)

| Event | File | Without | With |
|-------|------|---------|------|
| `key_wont_turn` | events_car.py | `add_danger("Worn Ignition")`, `add_travel_restriction` | Spray ignition, fixed |
| `gas_pedal_sticking` | events_car.py | `add_danger("Sticky Gas Pedal")`, `lose_sanity(15)` | Lubricate linkage, danger downgraded |

---

### Tire Patch Kit
**How to get:** Auto parts store  
**Consumed:** Yes

| Event | File | Without | With |
|-------|------|---------|------|
| `slow_tire_leak` | events_car.py | Visit air pumps all afternoon (travel lost) | Patch nail, fixed |
| `nail_in_tire` | events_car.py | Consume Spare Tire + travel restricted | Patch instead — spare preserved |

**Saves your Spare Tire.** If you have both, use the patch kit first.

---

### Duct Tape
**How to get:** Hardware store  
**Consumed:** Yes (usually)

| Event | File | Without | With |
|-------|------|---------|------|
| `broken_belonging` | events_day_survival.py | `lose_sanity(2)` | Fixed, no loss |
| `flat_tire_again` | events_day_survival.py | Worse damage tier | `hurt(3)` emergency patch, buys time |
| `road_adventure` | adventures.py | Less resourceful outcome | Tool Kit or Duct Tape — better result |

---

### Jumper Cables
**How to get:** Auto parts store  
**Consumed:** No

| Event | File | Without | With |
|-------|------|---------|------|
| `dead_battery_afternoon` | events_car.py | Stranded, tow required | Flag down driver, jump start, `sanity+3` |

---

### Portable Battery Charger
**How to get:** Auto parts store (more expensive)  
**Consumed:** No

| Event | File | Without | With |
|-------|------|---------|------|
| `dead_battery_afternoon` | events_car.py | Stranded | Self-sufficient start, `sanity+5` |

Strictly better than Jumper Cables — no flagging down strangers needed.

---

### Scrap Armor
**How to get:** Crafted at junkyard  
**Consumed:** No

| Event | File | Without | With |
|-------|------|---------|------|
| `attacked_by_dog` | events_day_dark.py | `hurt(40)`, `lose_sanity(15)`, `add_danger("Dog Bite Wound")`, possible `$600` vet bill | `hurt(20)` — halved |
| `electrocution_hazard` (minor) | events_day_dark.py | `hurt(10)`, `lose_sanity(8)` | `hurt(4)` |
| `electrocution_hazard` (major) | events_day_dark.py | `hurt(35)`, `lose_sanity(15)`, possible `$500` ER bill | `hurt(18)` |

---

### Coolant / Antifreeze
**How to get:** Auto parts store  
**Consumed:** Yes

| Event | File | Without | With |
|-------|------|---------|------|
| `engine_overheating` | events_car.py | Wait hours, `change_balance(−$200)`, `lose_sanity(10)` | Add fluid, back on road, `sanity+5` |

Water Bottles work as an emergency fallback but add `add_danger("Cooling System Damage")`.

---

### OBD Scanner
**How to get:** Auto parts store  
**Consumed:** No

| Event | File | Without | With |
|-------|------|---------|------|
| `check_engine_light_on` | events_car.py | 20% chance: car dies, `add_travel_restriction`, `add_danger("Major Engine Failure")`, `lose_sanity(15)` | Code read, specific issue identified, `sanity+4–6` |

---

### Binoculars
**How to get:** General store  
**Consumed:** No

| Event | File | Without | With |
|-------|------|---------|------|
| `someone_stole_your_stuff` | events_day_survival.py | Theft attempt proceeds | Spot thief early, scare them off, `sanity+4–5`, return early |
| `stargazing` | events_night.py | Base sanity (3–5) | Enhanced view, extra sanity |

---

### Plastic Wrap / Garbage Bag
**How to get:** General store / found  
**Consumed:** Yes

| Event | File | Without | With |
|-------|------|---------|------|
| `window_wont_roll_up` | events_car.py | `add_danger("Open Window")`, `lose_sanity(8)` | Seal window, `sanity+3`, downgraded to `add_danger("Broken Window")` |

---

### Bungee Cords / Rope
**How to get:** Hardware store / found  
**Consumed:** No

| Event | File | Without | With |
|-------|------|---------|------|
| `trunk_wont_close` | events_car.py | `add_travel_restriction`, `add_danger("Open Trunk")` | Secured, `sanity+3`, downgraded to `add_danger("Broken Trunk Latch")` |

---

### Bag of Acorns
**How to get:** Woodland area / Squirrely companion event  
**Consumed:** Yes (one acorn per feeding)

| Event | File | Without | With |
|-------|------|---------|------|
| `squirrely_feeding` | events_day_animals.py | Squirrely hungry, mood drop | Acorn given, Squirrely happy |
| `bag_of_acorns_daily` | game_flow.py | — | `restore_sanity(3)` when feeding Squirrely |

---

## B Tier

---

### Car Alarm Rigging
**How to get:** Crafted (bungee cords + spare fuses) or event  
**Consumed:** No

| Event | File | Without | With |
|-------|------|---------|------|
| `trap_night_thief` | events_day_items.py | Thief may succeed | Alarm triggers, thief flees, `sanity+2` |
| `robbery_attempt` | events_day_people.py | Money lost | Alarm deters thief |
| `someone_stole_your_stuff` | events_day_survival.py | Theft proceeds | Attempted break-in fails |

---

### Padlock
**How to get:** Hardware store  
**Consumed:** No

| Event | File | Without | With |
|-------|------|---------|------|
| `robbery_attempt` | events_day_people.py | `change_balance(−$50–200)` | Thief fails, `sanity+6` |
| `someone_stole_your_stuff` | events_day_survival.py | Theft succeeds | Lock holds, thief gives up |

---

### Carrot
**How to get:** Grocery store, found events  
**Consumed:** Yes

| Event | File | Without | With |
|-------|------|---------|------|
| `chase_the_rabbit` | events_night.py | Rabbit not lured | Carrot used, rabbit befriended |
| `rabbit_encounter` | events_day_animals.py | Rabbit flees | Fed, relationship built |

---

### Fish / Live Fish / Stolen Marlin
**How to get:** Fishing events / adventures  
**Consumed:** Yes

| Event | File | Without | With |
|-------|------|---------|------|
| `kraken_encounter` (offer) | adventures.py | Kraken unimpressed | Offering accepted, receive Deep Stone |
| `wildlife_feeding` | events_day_items.py | — | Feed wildlife, `sanity+15`, `heal(5)` |

---

### Silver Flask
**How to get:** General store, gift  
**Consumed:** No

| Event | File | Without | With |
|-------|------|---------|------|
| `upper_class_encounter` | events_day_people.py | Standard outcome | Share swig, `sanity+5`, rapport built |

---

### Vintage Wine
**How to get:** Liquor store, pawn shop  
**Consumed:** Sometimes

| Event | File | Without | With |
|-------|------|---------|------|
| `upper_class_encounter` | events_day_people.py | Standard outcome | Share wine, social bonus |
| `dinner_invitation` | events_day_people.py | Polite but plain | Wine gift, better outcome |

---

### Fancy Pen
**How to get:** General store, pawn shop  
**Consumed:** No

| Event | File | Without | With |
|-------|------|---------|------|
| `bureaucracy_event` | events_day_survival.py | Borrow a pen, no impression | Sign with flourish, bonus cash reward |

---

### Deck of Cards
**How to get:** General store  
**Consumed:** No

| Event | File | Without | With |
|-------|------|---------|------|
| `children_magic_event` | adventures.py | No trick to perform | Card trick delights kids |
| `deck_of_cards_street_game` | events_day_items.py | Can't join | Street gambling: **67% win rate**, `sanity+3–8` |

---

### Ace of Spades
**How to get:** Casino event when balance is exactly $21  
**Consumed:** No (one-time event trigger, `has_met` gate)

| Event | File | Without | With |
|-------|------|---------|------|
| `ace_of_spades_blackjack_omen` | events_day_items.py | Standard gambling | `add_status("Lucky")`, `add_status("Sharp")`, `change_balance(+$200–1000)`, `sanity+10` |

---

### Dealer's Joker
**How to get:** Mechanics intro dream sequence (story event, early game)  
**Consumed:** No (one-time event trigger, `has_met` gate)

| Event | File | Without | With |
|-------|------|---------|------|
| `dealer_joker_revelation` | events_day_items.py | Nothing | Casino comps you `$500–2000`, `sanity+10` |

---

### Mysterious Key + Mysterious Lockbox
**How to get:** Key — underwater adventure / `mysterious_code_decode` fallback. Lockbox — swamp night event.  
**Consumed:** Both consumed together

| Event | File | Without | With (both items) |
|-------|------|---------|------|
| `mysterious_key_lockbox_open` | events_day_items.py | Nothing (items just sit) | Cash `$500–2000`, OR old photograph + `sanity+15`, OR gems `$300–1200`, OR Treasure Coordinates map |

---

### Suspicious Package
**How to get:** City adventure  
**Consumed:** Yes

| Event | File | Outcome |
|-------|------|---------|
| `suspicious_package_open` | events_day_items.py | Cash `$1000–5000` + `sanity−8`, OR casino surveillance photos + `sanity+5`, OR drugs found `sanity−15` `hurt(5)`, OR birthday cake `sanity+10` `heal(5)` |

---

### Stolen Watch
**How to get:** City adventure (mugger drops it)  
**Consumed:** Yes if returned

| Event | File | Choice | Outcome |
|-------|------|---------|---------|
| `stolen_watch_recognition` | events_day_items.py | Return | `change_balance(+$50–200)`, `sanity+12`, item gone |
| | | Keep | `lose_sanity(8)` |

---

### Underwater Camera
**How to get:** Beach night dive event  
**Consumed:** Yes

| Event | File | Outcome |
|-------|------|---------|
| `underwater_camera_photos` | events_day_items.py | Sell prints `$200–600` + `sanity+8`, OR reunite family `sanity+15`, OR mysterious deep-water photo `sanity−5` then `+8` |

---

### Witch's Ward
**How to get:** Swamp night witch encounter  
**Consumed:** Yes (one-time)

| Event | File | Without | With |
|-------|------|---------|------|
| `witch_ward_dark_protection` | events_day_items.py | No deflection | Dark event diverted, `change_balance(+$100–500)`, `heal(5)`, `sanity+10` |

---

### Magic Acorn
**How to get:** Woodland fairy adventure  
**Consumed:** Yes (if planted)

| Event | File | Choice | Outcome |
|-------|------|---------|---------|
| `magic_acorn_planting` | events_day_items.py | Plant | `sanity+12`, `add_status("Nature Blessed")` |
| | | Keep | `sanity+3` |

---

### Treasure Map / Joe's Treasure Map / Fairy's Secret Map / Treasure Coordinates
**How to get:** Shipwreck adventure / Earl's fishing shack / Fairy woodland adventure / lockbox or events  
**Consumed:** Yes (whichever map used)

| Event | File | Outcome |
|-------|------|---------|
| `treasure_map_follow` | events_day_items.py | Cash `$300–1500` + `sanity+12`, OR coins `$150–600`, OR fresh air `sanity+5 heal+5`, OR Vision Map |

---

### Captured Fairy
**How to get:** Woodland adventure  
**Consumed:** Yes if released

| Event | File | Choice | Outcome |
|-------|------|---------|---------|
| `capture_fairy_release` | events_day_items.py | Release | `sanity+20`, `heal(15)`, `add_status("Fairy Blessed")`, receive Magic Acorn |
| | | Keep | `lose_sanity(8)` |

---

### Lucky Lure / Earl's Lucky Lure
**How to get:** Night swamp fishing (Lucky Lure) / Earl's fishing shack (Earl's Lucky Lure)  
**Consumed:** No (`has_met` gate fires once per playthrough)

| Event | File | Outcome |
|-------|------|---------|
| `lucky_lure_fishing` | events_day_items.py | Big catch `$100–500` + `sanity+20`, OR catch-and-release `sanity+15 heal+5 fatigue−10`, OR boot with $20, OR three fish to share `sanity+18 heal+8` |

---

### Mysterious Code
**How to get:** City adventure  
**Consumed:** Yes

| Event | File | Outcome |
|-------|------|---------|
| `mysterious_code_decode` | events_day_items.py | Storage locker cash `$200–1000` + `sanity+12`, OR Mysterious Key + `sanity+10`, OR radio broadcast `sanity+20` |

---

### Swamp Gold
**How to get:** Swamp night event  
**Consumed:** Sometimes

| Event | File | Choice | Outcome |
|-------|------|---------|---------|
| `swamp_gold_attention` | events_day_items.py | Return to owner | `change_balance(+$200–600)`, `sanity+20`, consumed |
| | | Sell to collector | `change_balance(+$300–900)`, `sanity+5`, consumed |
| | | Refuse both | `lose_sanity(5)` then `sanity+3` (net −2) |

---

### Giant Oyster
**How to get:** Beach night dive event  
**Consumed:** Yes

| Event | File | Outcome |
|-------|------|---------|
| `giant_oyster_opening` | events_night.py | Pink Pearl + `$200–500`, OR Matched Pearls, OR oyster meal `heal(15–25) sanity+8` |

---

### Voodoo Doll
**How to get:** Dark events / Witch Doctor's Tower shop  
**Consumed:** No

| Event | File | Without | With |
|-------|------|---------|------|
| `voodoo_temptation` | events_day_dark.py | No temptation event | Offered dark deal — harm someone for cash benefit |

---

### Scrap Metal Rose
**How to get:** Crafted at junkyard (Gideon storyline)  
**Consumed:** No

| Event | File | Without | With |
|-------|------|---------|------|
| `junkyard_masterpiece` | events_day_storylines.py | Story beat unavailable | Gideon impressed, storyline advances |
| `crossover_artisan_rose_gift` | events_day_storylines.py | Event gated | Connects Gideon to Radio Nowhere storyline |
| Achievement | systems.py | No achievement | Unlocks `junkyard_apprentice` |

---

### Fancy Cigars
**How to get:** Cigar shop, gift  
**Consumed:** Yes (on sharing)

| Event | File | Without | With |
|-------|------|---------|------|
| `wealthy_npc_encounter` | events_day_people.py | Standard chat | Share cigars, social rapport boost |

---

### Casino VIP Card
**How to get:** Casino progression events  
**Consumed:** No

| Event | File | Without | With |
|-------|------|---------|------|
| `vip_lounge_access` | events_day_wealth.py | Standard entry | VIP access, 3 separate perk events |

---

### Road Talisman
**How to get:** Roadside shop, gift  
**Consumed:** No

| Event | File | Without | With |
|-------|------|---------|------|
| `road_talisman_blessing` | events_day_items.py | Event skipped | Driving comfort, small sanity/money find |

---

### Silver Horseshoe
**How to get:** Pawn shop, gift  
**Consumed:** No

| Event | File | Without | With |
|-------|------|---------|------|
| `silver_horseshoe_luck` | events_day_items.py | Event skipped | Lucky outcome, sanity boost |

---

### Herbal Pouch
**How to get:** Witch Doctor's Tower, woodland events  
**Consumed:** Yes

| Event | File | Without | With |
|-------|------|---------|------|
| `herbal_pouch_remedy` | events_day_items.py | Event skipped | Brew tea, heal + sanity |

---

### Persistent Bottle
**How to get:** Story / found  
**Consumed:** No

| Event | File | Without | With |
|-------|------|---------|------|
| `persistent_bottle_refill` | events_day_items.py | Event skipped | Refill water, hydration + sanity |

---

### Lucky Charm Bracelet
**How to get:** Flea market / gift  
**Consumed:** No

| Event | File | Without | With |
|-------|------|---------|------|
| `lucky_charm_event` | events_day_items.py | Event skipped | Small lucky find |

---

### Lucky Rabbit Foot
**How to get:** Pawn shop  
**Consumed:** No

| Event | File | Without | With |
|-------|------|---------|------|
| `rabbit_foot_event` | events_day_animals.py | Event skipped | Luck-adjacent bonus |

---

## C Tier — Passive Flavor Pool

These items appear in `apply_daily_item_flavor()` in `player_core.py`. Once per ~3 days, **one** item is chosen at random from whatever you're carrying. A single quiet moment fires — no more.

| Item | Pawn Value | Daily Flavor Effect | Also Has Event |
|------|-----------|--------------------|-|
| Filled Locket | $500 | `sanity+2` | `empty_locket_memory` |
| Moon Shard | $15,000 | `sanity+3`, `heal(2)` | Stargazing bonus |
| Midnight Rose | $2,500 | `sanity+2` | — |
| Rabbit's Blessing | $10,000 | `sanity+2`, `+$5–25` | — |
| Championship Medal | $5,000 | `sanity+2` | — |
| Key to the City | $25,000 | `+$25–100` | — |
| Bear King's Respect | $50,000 | `sanity+3` | — |
| Kraken's Memory | $50,000 | `sanity+4`, `heal(3)` | — |
| Fight Champion Belt | $10,000 | `sanity+3` | — |
| Deep Stone | $40,000 | `sanity+3` | — |
| Antique Ring | $4,000 | `sanity+2` | — |
| Kraken Pearl | $100,000 | `sanity+4` | — |
| Mermaid Crown | $75,000 | `sanity+4` | — |
| Hero Medal | $15,000 | `sanity+3` | — |
| Giant Bear Tooth | $15,000 | `sanity+2` | — |
| Crab Racing Trophy | $3,000 | `sanity+3` | — |
| Tortoise Trophy | $4,000 | `sanity+3` | — |
| Matched Pearls | $5,000 | `sanity+3` | `giant_oyster_opening` |
| Pink Pearl | $3,000 | `sanity+3` | `giant_oyster_opening` |
| Mermaid Pearl | $6,000 | `sanity+3` | — |
| Ancient Sea Map | $25,000 | `sanity+3` | — |
| Cannon Gem | $20,000 | `sanity+2` | — |
| Pirate Treasure | $60,000 | `sanity+3` | — |
| Treasure Chest | $10,000 | `sanity+3` | — |

**How it works:** Each morning `random.randrange(3)` is checked — only fires 1-in-3 days. Of all flavor-pool items you currently have, one is picked at random. The stat effect is applied silently then a single cyan line of text prints. You'll never see more than one of these per day.

---

## D Tier — Pure Collectibles

These items have no mechanical effect in any event. Sell to Gus at the Pawn Shop.

| Item | Pawn Value | How to Get |
|------|-----------|------------|
| Golden Trident | $80,000 | Ocean adventure (has_cutting_tool — technically B) |
| Golden Shovel | $15,000 | Woodland/dig adventure (has_cutting_tool — technically B) |
| Mermaid's Pearl | $8,000 | Beach/mermaid encounter |
| Captain's Compass | $12,000 | Ocean adventure |
| Witch's Riddle | $3,000 | Witch storyline |
| Gator Tooth Necklace | $5,000 | Swamp/alligator event |
| Ogre's Gemstone | $30,000 | Mountain/ogre adventure |
| Ogre's Gift | $20,000 | Mountain/ogre adventure |
| Bear's Gold Coin | $5,000 | Bear King encounter |
| Swamp Crystal | $8,000 | Swamp dive |
| Fairy Dust | $5,000 | Woodland fairy encounter |
| Giant Pearl | $20,000 | Ocean depth |
| Mermaid Scale | $3,000 | Mermaid encounter |
| Sunken Locket | $500 | Shipwreck dive |
| Old Photograph | $100 | Found / lockbox event |
| Crab Racing Trophy | (see C) | Crab racing event |
| Tortoise Trophy | (see C) | Tortoise race |
| Witch's Favor | $12,000 | Witch encounter |
| Granny's Swamp Nectar | $1,500 | Swamp granny / roadside |
| Stolen Watch | (see B) | City adventure |
| Fountain Water | $500 | Fountain of Youth event |
| Radio Numbers | — | Numbers station event |
| Static Recorder | — | Numbers station event |
| Strange Frequency Dial | — | Numbers station event |
| Pirate Radio Flyer | — | Pirate radio chain |
| Tinfoil Hat | — | Conspiracy event (has own event `tinfoil_hat_event`) |
| Professor Bear | — | Bear Kingdom storyline |
| Bodyguard Bruno | — | City protection storyline |
| Night Vision Scope | — | Military surplus / dark events |

> **Note on Golden Trident / Golden Shovel:** These appear in `has_cutting_tool()` checks alongside Pocket Knife, so they technically unlock cutting-tool events. In practice the Pocket Knife is cheaper and available far earlier. Trident/Shovel are still worth holding for the pawn value.

---

## Quick Reference — What to Buy First

| Priority | Item | Why |
|----------|------|-----|
| 1 | **Pest Control** | Blocks the most events, keeps camping active |
| 2 | **Spare Tire + Car Jack** | Tires pop constantly; pair is free fix |
| 3 | **First Aid Kit** | Passive damage reduction — always-on |
| 4 | **Pocket Knife** | Robbery protection + cutting tool + lockpick |
| 5 | **Tool Kit** | 4+ car crises solved cheaply |
| 6 | **Cough Drops** | Sore Throat snowballs fast |
| 7 | **Hand Warmers** | Coldest nights: zero damage |
| 8 | **WD-40** | Key and pedal failures are sudden |
| 9 | **Flashlight** | Night safety net |
| 10 | **Tire Patch Kit** | Preserves your spare tire |
