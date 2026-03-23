# Item Planning — Interconnection & Expansion Roadmap

> Master planning document for item interactions, gap analysis, secret combinations,
> and proposed changes. Every section includes the exact function/file where work happens.

---

## Table of Contents

1. [Current State Audit](#1-current-state-audit)
2. [Gap Analysis — What's Inert](#2-gap-analysis--whats-inert)
3. [Cross-File Interaction Map](#3-cross-file-interaction-map)
4. [Multi-Item Combination Map](#4-multi-item-combination-map)
5. [Tier 1 — Marvin Items React to the World](#5-tier-1--marvin-items-react-to-the-world)
6. [Tier 2 — Crafted Items Cross File Boundaries](#6-tier-2--crafted-items-cross-file-boundaries)
7. [Tier 3 — Convenience Store Items Come Alive](#7-tier-3--convenience-store-items-come-alive)
8. [Tier 4 — Secret Multi-Item Combinations](#8-tier-4--secret-multi-item-combinations)
9. [Tier 5 — Missing Systemic Mechanics](#9-tier-5--missing-systemic-mechanics)
10. [Tier 6 — New Features](#10-tier-6--new-features)
11. [Flask Narrative Integration](#11-flask-narrative-integration)
12. [Companion-Item Synergy Plan](#12-companion-item-synergy-plan)
13. [Adventure Zone Item Gaps](#13-adventure-zone-item-gaps)
14. [Event Weight Tuning Notes](#14-event-weight-tuning-notes)
15. [Implementation Priority Matrix](#15-implementation-priority-matrix)
16. [**CRAFTING EXPANSION — Complete Overhaul**](#16-crafting-expansion--complete-overhaul)
17. [**New Recipe Category: Gadgets**](#17-new-recipe-category-gadgets)
18. [**New Recipe Category: Disguises**](#18-new-recipe-category-disguises)
19. [**New Recipe Category: Tonics & Consumables**](#19-new-recipe-category-tonics--consumables)
20. [**New Recipe Category: Dark Arts**](#20-new-recipe-category-dark-arts)
21. [**New Recipe Category: Luxury Crafts**](#21-new-recipe-category-luxury-crafts)
22. [**New Recipe Category: Vehicle Upgrades**](#22-new-recipe-category-vehicle-upgrades)
23. [**Tier 2 Crafting — Crafted + Crafted Recipes**](#23-tier-2-crafting--crafted--crafted-recipes)
24. [**Tier 3 Crafting — Triple-Ingredient Masterworks**](#24-tier-3-crafting--triple-ingredient-masterworks)
25. [**Tier 4 Crafting — Legendary Items**](#25-tier-4-crafting--legendary-items)
26. [**Crafting Tree Visualization**](#26-crafting-tree-visualization)
27. [**New Ingredient Usage Map**](#27-new-ingredient-usage-map)
28. [**Crafting Event Interactions — What Each New Item Does**](#28-crafting-event-interactions--what-each-new-item-does)
29. [**Milestone & Achievement Updates**](#29-milestone--achievement-updates)
30. [**Full Recipe Count Summary**](#30-full-recipe-count-summary)
31. [**Item Trigger Display Standard**](#31-item-trigger-display-standard)
32. [**Recipe Hint System Design**](#32-recipe-hint-system-design)
33. [**All Recipe Hint Texts (by Tier)**](#33-all-recipe-hint-texts-by-tier)
34. [**Shop & Pawn Descriptions — All New Items**](#34-shop--pawn-descriptions--all-new-items)
35. [**Craft Text & Use Descriptions — All New Items**](#35-craft-text--use-descriptions--all-new-items)
36. [**Full Event Narrative Drafts — Gadgets**](#36-full-event-narrative-drafts--gadgets)
37. [**Full Event Narrative Drafts — Disguises**](#37-full-event-narrative-drafts--disguises)
38. [**Full Event Narrative Drafts — Tonics & Consumables**](#38-full-event-narrative-drafts--tonics--consumables)
39. [**Full Event Narrative Drafts — Dark Arts**](#39-full-event-narrative-drafts--dark-arts)
40. [**Full Event Narrative Drafts — Luxury Crafts**](#40-full-event-narrative-drafts--luxury-crafts)
41. [**Full Event Narrative Drafts — Vehicle Upgrades**](#41-full-event-narrative-drafts--vehicle-upgrades)
42. [**Full Event Narrative Drafts — Tier 2 Items**](#42-full-event-narrative-drafts--tier-2-items)
43. [**Full Event Narrative Drafts — Tier 3 & 4 Items**](#43-full-event-narrative-drafts--tier-3--4-items)
44. [**Wild Item Interactions — The Weird Stuff**](#44-wild-item-interactions--the-weird-stuff)
45. [**Quality Pass — Rewritten Weak Event Narratives**](#45-quality-pass--rewritten-weak-event-narratives)
46. [**Craft Text Overhaul — The Amateur Crafter**](#46-craft-text-overhaul--the-amateur-crafter)

---

## 1. Current State Audit

### Status Of This Document

This file is now a historical master roadmap, not the authoritative status tracker.

Authoritative current-state tracking lives in `docs/ITEM_PLANNING_REMAINING.md`.

The original opening audit in this file substantially under-reported implemented work. In particular, it treated large parts of the current codebase as greenfield even though the following are already in place:

- Marvin blackjack item behavior in `blackjack.py`
- Multiple non-table Marvin and upgrade hooks across `story/*.py`
- Flask durability and some narrative integration
- Dealer gift wrapping and gift delivery systems
- Mechanic loyalty reward items
- Inventory-aware event weighting
- Expanded crafting recipes, hints, and workbench flow
- Wrong-item and wild-item event infrastructure

### Current High-Level Reality

The remaining implementation problem is narrower than this document originally claimed.

- The biggest real gap is not recipe existence; it is uneven world integration.
- The most valuable unfinished work is still Marvin saturation, flask saturation, crafted-item cross-file presence, and selected combo/system follow-through.
- Sections 16-35 in this file are mostly useful as design reference, not as an accurate missing-feature list.

---

## 2. Gap Analysis — What's Actually Still Open

The original "narrative-inert" tables below are obsolete and should not be used for implementation counting.

Use this simplified view instead:

### Confirmed Remaining Work

- Under-covered Marvin items and upgrades still need broader event presence.
- Flasks still need stronger non-casino narrative payoff.
- Many crafted items still need to escape `events_day_items.py` isolation.
- Higher-tier crafted items still need more memorable non-crafting triggers.
- Some convenience-store items remain flavor-light compared with better-integrated utility items.
- Multi-item combinations are still underbuilt relative to inventory size.
- Optional systemic proposals remain undecided, not implemented.

### Not Open In The Way This File Originally Claimed

- Crafting recipes and crafting categories are already implemented.
- Workbench browsing, hints, inspect flows, and multi-tier crafting are already implemented.
- Dealer gifting is already implemented.
- Mechanic loyalty items are already implemented.
- Inventory-aware event-weight tuning already exists.
- Wrong-item interactions already exist in partial form.

### Reading Rule

If a later section in this file says an item family has "zero narrative" or is wholly inert, treat that as historical planning language unless it has been re-verified against current code.

---

## 3. Cross-File Interaction Map

The original counts in this section were useful for spotting isolation patterns, but they are no longer authoritative item-by-item metrics.

What still holds true:

- Highly connected utility items feel systemic because they appear in multiple event families.
- Several crafted, luxury, flask, and Marvin-derived items still lag behind that standard.
- Cross-file presence remains the right measure for whether an item feels "real" in the game.

What changed:

- Some items previously listed as isolated now have additional hooks.
- Some systems previously described as disconnected are already integrated.
- The exact per-item file counts should be refreshed only after the remaining implementation waves are complete.

Practical rule for continuing work:

- Prefer moving under-covered items into people, dark, night, survival, companion, surreal, and adventure events over adding more recipe-layer complexity.
- Use `docs/ITEM_PLANNING_REMAINING.md` as the live checklist for which families still need that treatment.

---

## 4. Multi-Item Combination Map

### Current AND Combinations (5 total in entire game)

| Items | Function | File | Effect |
|-------|----------|------|--------|
| Spare Tire + Car Jack | tire repair event | events_car.py L399 | Full tire fix (without Jack = partial) |
| Bag of Acorns + Squirrely companion | companion feeding | game_flow.py L617 | Feed companion |
| Pest Control + has_pests() | pest elimination | game_flow.py L608 | Get rid of pests |
| LifeAlert (auto) | critical health check | player_core.py L282 | Emergency rescue |
| Marvin's Monocle + loan calculation | loan shark eval | economy.py L55 | Better loan terms |

### Current OR Combinations (20+ patterns)

| Category | Items in OR Group | Where |
|----------|------------------|-------|
| Food | Turkey Sandwich / Beef Jerky / Granola Bar | adventures.py L284 |
| Fish | Fish / Live Fish / Stolen Marlin | adventures.py L2911 |
| Bird Food | Birdseed / Bread | events_day_animals.py L705 |
| Small Animal Food | Cheese / Sandwich / Turkey Sandwich | events_day_animals.py L829 |
| Rain Gear | Umbrella / Poncho / Plastic Poncho | events_day_survival.py L1758 |
| Sun Protection | Cheap Sunscreen / Premium Sunscreen | events_day_survival.py L1199 |
| Security | Padlock / Car Alarm Rigging | events_day_survival.py L1440 |
| Repair | Duct Tape / Tool Kit | adventures.py L487 |
| Tools | Pocket Knife / Tool Kit | events_day_storylines.py L887 |
| Battery Fix | Battery Terminal Cleaner / Baking Soda | events_car.py L150 |
| Cover | Plastic Wrap / Garbage Bag | events_car.py L1014 |
| Rope | Bungee Cords / Rope | events_car.py L1035 |
| Maps | Map / Worn Map | multiple files |
| Treasure Maps | Treasure Map / Joe's Treasure Map / Fairy's Secret Map / Treasure Coordinates | events_day_items.py L2015 |
| Elegance | Leather Gloves / Silk Handkerchief / Gold Chain / Antique Pocket Watch | events_day_people.py L540 |
| Drink | Vintage Wine / Silver Flask | events_day_people.py L572 |
| Fire | Lighter / Matches / Monogrammed Lighter / Road Flares | player_core.py L598 |
| Cutting | Pocket Knife / Golden Trident / Golden Shovel | player_core.py L603 |
| Fishing Lure | Lucky Lure / Earl's Lucky Lure | events_day_items.py L2112 |
| Grimoire | Gambler's Grimoire / Oracle's Tome | systems.py L281 |

### The Gap

Only **5 AND combos** exist. A game with 235+ items should have dozens of secret combinations that reward players for holding specific item pairs. The OR groups are good but they're safety nets, not discoveries.

---

## 5. Tier 1 — Marvin Items React to the World

**Goal:** Make the 15 narrative-inert Marvin items show up in events. Each item gets 3–4 new `has_item()` checks inserted into existing events across multiple files.

### Sneaky Peeky Shades / Goggles → See Through Deception

| Target Event | File | Line Area | New Behavior |
|--------------|------|-----------|-------------|
| con_artist_encounter | events_day_dark.py | con artist scam events | "Through your enchanted lenses, you notice the cards are marked." Skip the con, +$200 |
| suspicious_stranger | events_day_people.py | stranger approach | "Your shades reveal a bulge in his jacket — a weapon." Avoid mugging entirely |
| three_card_monte | events_day_people.py | street hustle | "The goggles track the queen. You pick correctly every time." +$500 |
| poker_night / street_dice | adventures.py | gambling encounters | "You can see the loaded dice glow faintly." Refuse to play, keep money |

### Tattered Cloak / Invisible Cloak → Avoid Detection

| Target Event | File | Line Area | New Behavior |
|--------------|------|-----------|-------------|
| mugging events | events_day_dark.py | robbery scenarios | "You pull the cloak tight. The mugger's eyes slide right past you." Skip mugging |
| casino_knows | events_day_wealth.py | being recognized | "The cloak shimmers. The pit boss looks right through you." Avoid surveillance |
| reporters_found_you | events_day_wealth.py | media exposure | "You vanish into the crowd mid-sentence. The reporter blinks." Escape interview |
| night_ambush | events_night.py | nighttime attacks | "The cloak wraps around you like shadow. The footsteps pass." Avoid night danger |

### Oracle's Tome / Gambler's Grimoire → Predict Events

| Target Event | File | Line Area | New Behavior |
|--------------|------|-----------|-------------|
| car_trouble events | events_car.py | car breakdown | "The Grimoire's margin notes warned: 'Check the belts today.'" Prevent breakdown |
| illness onset | events_illness.py | getting sick | "The Tome's pages flutter open: 'Avoid the water today.'" Dodge illness |
| blood_moon_bargain | events_day_dark.py | devil's deal | "The Tome screams in your bag, pages turning frantically." Warning text, +sanity |
| investment_opportunity | events_day_wealth.py | money events | "A cramped footnote reads: 'This one's real.'" Guarantee good investment |

### Golden Compass / Rusty Compass → Find Hidden Things

| Target Event | File | Line Area | New Behavior |
|--------------|------|-----------|-------------|
| adventure zone entry | adventures.py | zone selection | "The compass needle spins wildly, then points east." Bias toward better sub-zones |
| lost in woods | events_day_survival.py | getting lost | "The compass hums warmly. You were never truly lost." Skip damage, find shortcut |
| treasure events | events_day_items.py | treasure hunts | "The compass pulls toward something buried nearby." +bonus treasure find |
| night_wandering | events_night.py | nighttime lost | "A faint golden glow leads you back to your car." Return safely |

### Phoenix Feather / White Feather → Survive Death

| Target Event | File | Line Area | New Behavior |
|--------------|------|-----------|-------------|
| lethal damage events | events_day_dark.py | murder/accident | "The feather ignites. Warmth floods your broken body." Survive with 1 HP, feather consumed |
| casino_hitman | events_day_wealth.py | assassination | "The bullet hits the feather. It dissolves into ash and light." Survive, item consumed |
| bridge_call / despair | events_day_dark.py | suicide events | "The feather lifts from your pocket and hovers before your eyes." +sanity, avoid death |
| companion death | events_day_companions.py | companion dying | "The feather drifts from your hand to your companion's body." Save companion, feather consumed |

### Lucky Medallion / Lucky Coin → Turn Bad Luck Good

| Target Event | File | Line Area | New Behavior |
|--------------|------|-----------|-------------|
| robbery events | events_day_dark.py | being robbed | "You flip the coin. Heads. The robber's gun jams." Escape |
| gambling_loss | events_day_casino.py | losing streak | "The medallion grows warm against your chest." Recover partial loss |
| flat tire / breakdown | events_car.py | car trouble | "The coin rolls under your seat and clinks against a spare part." Find free fix |
| night_chase | events_night.py | being chased | "You stumble — but the coin catches under your heel and you vault a fence." Escape |

### Dealer's Mercy / Dealer's Grudge → Dealer Relationship Moments

| Target Event | File | Line Area | New Behavior |
|--------------|------|-----------|-------------|
| dealer_dream events | mechanics_intro.py | Frank dreams | "The Grudge pulses in your pocket. The Dealer's shadow turns toward you." Extra dream text |
| casino_events | events_day_casino.py | dealer interactions | "He glances at the Mercy on your wrist. 'You're one of the old ones.'" Unique dialogue |
| blood_moon_bargain | events_day_dark.py | devil deal | "The Grudge burns your leg. The Dealer whispers: 'Not this one.'" Refuse deal automatically |
| final_dream | events_day_wealth.py | dream finale | "The Mercy glows white. For one perfect moment, the Dealer smiles." +bonus sanity |

### Twin's Locket / Mirror of Duality → Identity Events

| Target Event | File | Line Area | New Behavior |
|--------------|------|-----------|-------------|
| mirror_stranger | events_day_surreal.py | surreal mirror | "The locket opens. Inside, both reflections look back at once." Unique surreal branch |
| identity crisis events | events_day_surreal.py | existential | "The Mirror shows you two futures. In one, you're rich. In the other, you're free." Choice text |
| time_loop | events_day_surreal.py | temporal anomaly | "The locket's twin faces tick in opposite directions." Extra temporal text |
| the_glitch | events_day_surreal.py | reality break | "The Mirror cracks. You step through." Bonus surreal outcome |

### Gambler's Chalice / Overflowing Goblet → Social Drinking Events

| Target Event | File | Line Area | New Behavior |
|--------------|------|-----------|-------------|
| bar events | events_day_people.py | social drinking | "You raise the Chalice. The bartender's eyes widen." Free drinks, NPC bonding |
| fancy_dinner events | events_day_wealth.py | high society | "The Goblet appears to refill itself. Your host is impressed." Social advantage |
| night_celebration | events_night.py | nighttime social | "You toast the stars with the Chalice. Silver light dances on the rim." +sanity |
| lonely_night | events_night.py | isolation | "You pour one drink. Then another. The Chalice never empties." Sanity restoration |

### Worn Gloves / Velvet Gloves → Elegance & Manipulation

| Target Event | File | Line Area | New Behavior |
|--------------|------|-----------|-------------|
| elegance checks | events_day_people.py L540 | luxury social | Add to existing OR group: Leather Gloves / Silk Handkerchief / Gold Chain / **Velvet Gloves** |
| handshake events | events_day_people.py | business deals | "Your handshake, firm through velvet, seals the deal." Better negotiation |
| cold_weather | events_day_survival.py | freezing | "The enchanted gloves keep your fingers nimble." Avoid cold damage |
| pickpocket | events_day_dark.py | theft | "Gloved fingers leave no prints." Escape accusation |

### Dirty Old Hat / Unwashed Hair → Disguise Events

| Target Event | File | Line Area | New Behavior |
|--------------|------|-----------|-------------|
| casino_knows | events_day_wealth.py | recognition | "No one expects a millionaire to wear that hat." Avoid recognition |
| reporters_found_you | events_day_wealth.py | media | "The reporter walks right past the man in the ratty hat." Escape |
| beggar_kindness | events_day_people.py | charity events | "A stranger hands you $20. You look like you need it more." Free money |
| police events | events_day_dark.py | law encounters | "Officers don't bother with the homeless-looking man." Avoid questioning |

### Golden Watch / Sapphire Watch → Time & Status Events

| Target Event | File | Line Area | New Behavior |
|--------------|------|-----------|-------------|
| time_loop | events_day_surreal.py | temporal | "The watch's hands spin backwards. You've been here before." Extra loop text |
| business events | events_day_people.py | negotiations | "You check the time ostentatiously. They start talking faster." Better deal |
| night_events | events_night.py | timing | "The watch chimes midnight. Something stirs." Unique midnight event |
| elegance checks | events_day_people.py | luxury social | Add to existing elegance OR group alongside Antique Pocket Watch |

### Pocket Watch / Grandfather Clock → Time Manipulation

| Target Event | File | Line Area | New Behavior |
|--------------|------|-----------|-------------|
| time_loop | events_day_surreal.py | temporal events | "The pocket watch ticks louder. This time, you remember." Break the loop |
| daily deadline events | events_day_survival.py | time pressure | "The clock's chime gives you an extra moment to decide." Better choice outcome |
| night_transition | events_night.py | dusk events | "The Grandfather Clock strikes thirteen." Bonus liminal event |
| mechanic dreams | mechanics_intro.py | dream sequences | "You hear a clock ticking in the dream. Louder each time." Extra dream flavor |

### Delight Indicator / Manipulator → Self-Awareness Events

| Target Event | File | Line Area | New Behavior |
|--------------|------|-----------|-------------|
| sanity_loss events | various | all sanity drain | "The Indicator flashes red. You're losing yourself." Warning text before big loss |
| lonely events | events_night.py | isolation | "The needle points to zero. It's been a long time since you smiled." Flavor text |
| celebration events | events_day_wealth.py | winning | "The Manipulator's dial swings to euphoric. You adjust it down." Self-control moment |
| companion moments | events_day_companions.py | companion joy | "The Indicator reads 'Content' for the first time in weeks." Heartfelt moment |

### Health Indicator / Manipulator → Body Awareness Events

| Target Event | File | Line Area | New Behavior |
|--------------|------|-----------|-------------|
| illness events | events_illness.py | getting sick | "The Indicator warned you yesterday. You should have listened." Earlier detection |
| combat events | events_day_dark.py | taking damage | "The Manipulator floods you with adrenaline." Reduce damage taken |
| healing events | events_day_survival.py | recovery | "The Health Indicator confirms: you're going to be okay." Flavor during heal |
| doctor visits | locations.py | medical | "The doctor reads your Indicator. 'This thing is more accurate than my equipment.'" Discount |

---

## 6. Tier 2 — Crafted Items Cross File Boundaries

**Goal:** Make the 19 single-file crafted items appear in 2–3 more event files each.

### Pepper Spray → Dark + Night + Survival

| Target | File | Proposed Check |
|--------|------|---------------|
| Mugging events | events_day_dark.py | Alternative to running: spray attacker, keep belongings |
| Night stalker | events_night.py | Spray pursuer, avoid damage |
| Bear/animal encounter | events_day_survival.py | Spray bear, escape unharmed |
| Adventure threats | adventures.py | Spray Swamp Ogre for free escape |

### Dream Catcher → Night + Surreal + Dark

| Target | File | Proposed Check |
|--------|------|---------------|
| Nightmares | events_night.py | "The Dream Catcher glows. The nightmare dissolves." Avoid sanity loss |
| Mechanic dreams | mechanics_intro.py | Bonus dream text: "The catcher's web shimmers with the mechanic's face." |
| Surreal events | events_day_surreal.py | "The Dream Catcher hums. This is a dream, isn't it?" Extra awareness |
| Blood moon | events_day_dark.py | "The catcher catches the bargain before it reaches you." Skip devil deal |

### Emergency Blanket → Survival + Night + Companions

| Target | File | Proposed Check |
|--------|------|---------------|
| Cold weather | events_day_survival.py | (already here) Warm in cold snap |
| Night exposure | events_night.py | "You wrap the blanket tight. The cold doesn't reach you." Avoid night damage |
| Companion comfort | events_day_companions.py | Share blanket with companion → +happiness |
| Homeless events | events_day_people.py | Give to homeless person → karma/sanity |

### Fire Starter Kit → Dark + Night + Adventures + Survival

| Target | File | Proposed Check |
|--------|------|---------------|
| Dark confrontations | events_day_dark.py | "You ignite the fire starter. The shadows scatter." Escape dark event |
| Night camp | events_night.py | "The fire keeps creature eyes at bay." Avoid night attacks |
| Adventure camping | adventures.py | "You build a fire. The zone feels less hostile." Better sub-zone rolls |
| Cold/rain events | events_day_survival.py | "Warmth returns to your bones." Avoid weather damage |

### Binocular Scope → People + Adventures + Dark + Night

| Target | File | Proposed Check |
|--------|------|---------------|
| Scouting strangers | events_day_people.py | "Through the scope, you see they're armed." Avoid ambush |
| Adventure recon | adventures.py | "You scope the zone entrance. Something glints in the distance." Scout bonus |
| Dark surveillance | events_day_dark.py | "The scope catches movement. You slip away before they see you." Escape |
| Night navigation | events_night.py | "Moonlight through the scope. You map a safe path." Navigate safely |

### Water Purifier → Adventures + Survival + Illness

| Target | File | Proposed Check |
|--------|------|---------------|
| Swamp adventure | adventures.py | "You purify the swamp water. Safe to drink." Avoid poison |
| Contaminated water | events_day_survival.py | "The purifier catches the parasites." Avoid illness |
| Illness prevention | events_illness.py | "You've been purifying your water. The stomach bug skips you." Block illness |
| Fountain events | adventures.py | "You purify the mysterious fountain water first." Better fountain outcome |

### Fishing Rod → Adventures + Night + Survival

| Target | File | Proposed Check |
|--------|------|---------------|
| Swamp fishing | adventures.py | "You cast into the murky water." Catch something in swamp zone |
| Night fishing | events_night.py | "Moonlight fishing. Something tugs the line." Night catch event |
| River crossing | events_day_survival.py | "You use the rod to test the current depth." Avoid drowning |
| Beach adventure | adventures.py | "You surf-cast from the shore." Beach zone fishing bonus |

### Lockpick Set → Dark + Night + Adventures

| Target | File | Proposed Check |
|--------|------|---------------|
| Locked car | events_day_dark.py | "You pick the lock on the glove box." Find hidden stash |
| Night storage | events_night.py | "The storage locker clicks open." Night loot bonus |
| Shipwreck chest | adventures.py | "The lockpick finds the ancient mechanism." Better underwater loot |
| Abandoned building | events_day_survival.py | "You pick the padlock. Inside: supplies." Find items |

### Scrap Armor → Night + Adventures + Survival

| Target | File | Proposed Check |
|--------|------|---------------|
| Night combat | events_night.py | "The armor catches the blow. You barely feel it." Reduce night damage |
| Adventure boss fights | adventures.py | "The scrap metal deflects the ogre's fist." Reduce adventure damage |
| Falling/accident | events_day_survival.py | "The armor plates take the impact." Reduce accident damage |
| Animal attack | events_day_animals.py | "The armor turns the claw." Survive predator encounter |

### Lucky Charm Bracelet → Night + Casino + Wealth

| Target | File | Proposed Check |
|--------|------|---------------|
| Night fortune | events_night.py | "The bracelet jingles. You find $100 in the gutter." Night money find |
| Casino events | events_day_casino.py | "The charm glows warm. The next hand feels right." Flavor text before good hand |
| Wealth events | events_day_wealth.py | "The bracelet hums. An opportunity approaches." Better wealth event outcome |
| Number events | events_day_numbers.py | "Lucky bracelet, lucky numbers." Better lottery/number outcomes |

### Road Flare Torch → Night + Dark + Adventures

| Target | File | Proposed Check |
|--------|------|---------------|
| Night threats | events_night.py | "The torch blazes. Whatever was following you stops." Scare off threat |
| Dark alleys | events_day_dark.py | "You light the torch. The alley isn't so dark anymore." Reveal hidden danger |
| Cave exploration | adventures.py | "Torchlight bounces off crystal walls." See hidden loot in adventure zones |
| Wildlife deterrent | events_day_animals.py | "The flame keeps the predator at bay." Avoid animal attack |

### Signal Mirror → Survival + Adventures + People

| Target | File | Proposed Check |
|--------|------|---------------|
| Lost events | events_day_survival.py | "You flash the mirror. A passing car spots you." Get rescued |
| Adventure rescue | adventures.py | "The mirror's flash catches a boat's attention." Emergency escape from zone |
| Stranger signal | events_day_people.py | "You signal the distant figure. They wave back." Friendly encounter |
| Night moonlight | events_night.py | "Moonlight in the mirror. For a moment, you see something." Surreal bonus |

### Improvised Trap → Night + Animals + Adventures

| Target | File | Proposed Check |
|--------|------|---------------|
| Night intruder | events_night.py | "The trap snaps. You hear a yelp outside." Catch nighttime thief |
| Predator defense | events_day_animals.py | "The trap slows the creature. You escape." Avoid animal attack |
| Adventure hunting | adventures.py | "You set a trap in the undergrowth." Catch food in adventure zone |
| Camp security | events_day_survival.py | "Your perimeter trap gives you early warning." Avoid surprise attack |

### Snare Trap → Night + Animals + Survival

| Target | File | Proposed Check |
|--------|------|---------------|
| Night hunting | events_night.py | "The snare catches a rabbit in the moonlight." Night food |
| Animal encounters | events_day_animals.py | "You set a snare and wait." Catch small animal |
| Survival food | events_day_survival.py | "The snare provides dinner." Avoid hunger damage |
| Adventure trapping | adventures.py | "You set snares between the trees." Woodland zone food bonus |

### Slingshot → Animals + Dark + Adventures

| Target | File | Proposed Check |
|--------|------|---------------|
| Bird encounters | events_day_animals.py | "A well-aimed stone." Alternate animal interaction |
| Dark intimidation | events_day_dark.py | "You hurl a stone at the streetlight. It shatters. The mugger flinches." Escape |
| Adventure combat | adventures.py | "You launch a stone at the creature." Ranged attack option |
| Night noise | events_night.py | "You pelt the shadow with stones. It retreats." Scare off threat |

### Rain Collector → Survival + Night + Illness

| Target | File | Proposed Check |
|--------|------|---------------|
| Drought events | events_day_survival.py | "The rain collector has a full jug. You drink." Avoid dehydration |
| Night hydration | events_night.py | "Morning dew collects. Clean water." Sleep bonus |
| Illness prevention | events_illness.py | "You've been drinking purified rain. Your immune system holds." Avoid illness |
| Adventure camping | adventures.py | "The rain collector fills overnight." Adventure hydration bonus |

### Splint → Survival + Night + Adventures

| Target | File | Proposed Check |
|--------|------|---------------|
| Fall damage | events_day_survival.py | "You splint the fracture. It's not broken after all." Reduce damage |
| Night injury | events_night.py | "You splint your ankle by moonlight." Avoid -health compounding |
| Adventure injury | adventures.py | "The splint holds. You press on." Continue adventure without penalty |
| Companion injury | events_day_companions.py | "You splint your companion's leg." Save companion from leaving |

### Worry Stone → Night + Surreal + Dark + Companions

| Target | File | Proposed Check |
|--------|------|---------------|
| Night anxiety | events_night.py | "You rub the stone. The worry melts." Night sanity restoration |
| Surreal events | events_day_surreal.py | "The stone's smooth surface anchors you to reality." Avoid sanity loss |
| Dark dread | events_day_dark.py | "You grip the stone. Whatever's out there can't touch your mind." Reduce sanity damage |
| Companion bonding | events_day_companions.py | "You let your companion sniff the stone. They calm down." +companion happiness |

### Home Remedy → Illness + Survival + Companions

| Target | File | Proposed Check |
|--------|------|---------------|
| Illness treatment | events_illness.py | "You mix the remedy. The fever breaks." Cure illness faster |
| Injury healing | events_day_survival.py | "The home remedy's poultice draws out the infection." Bonus healing |
| Companion illness | events_day_companions.py | "You apply the remedy to your companion's wound." Heal companion |
| Food poisoning | events_day_dark.py | "The remedy settles your stomach." Skip food poisoning damage |

### Wound Salve → Survival + Night + Dark + Adventures

| Target | File | Proposed Check |
|--------|------|---------------|
| Injury events | events_day_survival.py | "The salve stings, then soothes." Bonus healing |
| Night wounds | events_night.py | "You dress the wound by moonlight." Reduce HP loss |
| Dark violence | events_day_dark.py | "You smear salve on the cut. It's not deep." Reduce damage taken |
| Adventure injuries | adventures.py | "The salve patches you up enough to continue." Adventure heal mid-zone |

### Smelling Salts → Dark + Surreal + Night

| Target | File | Proposed Check |
|--------|------|---------------|
| Knockout events | events_day_dark.py | "The salts jolt you awake. You're still alive." Wake from knockout |
| Surreal dissociation | events_day_surreal.py | "One whiff and reality snaps back." Break surreal loop |
| Night fatigue | events_night.py | "The salts keep you alert through the longest night." Avoid night penalty |
| Fainting events | events_day_survival.py | "You crack the salts under your nose. The world steadies." Avoid collapse |

### Car Alarm Rigging → Night + Dark + Survival

| Target | File | Proposed Check |
|--------|------|---------------|
| Night theft | events_night.py | "Your car alarm screams. The thief bolts." Prevent item loss |
| Break-in attempt | events_day_dark.py | "The rigged alarm goes off. Neighbors come running." Scare off burglar |
| Camp security | events_day_survival.py | "The alarm serves as a perimeter warning." Early warning |
| Companion safety | events_day_companions.py | "The alarm wakes you. Your companion was being lured away." Save companion |

---

## 7. Tier 3 — Convenience Store Items Come Alive

**Goal:** Give store items interesting event reactions beyond their primary use.

### Necronomicon ($666) → Full Event Chain

Currently: Purchased as a "trap" — cursed book. Needs reactive events:

| Proposed Event | File | Description |
|----------------|------|-------------|
| necronomicon_reading | events_day_dark.py | "You open the book. The text writhes. You can't look away." Sanity -10 but learn a dark secret |
| necronomicon_whispers | events_night.py | "The book whispers your name at 3 AM." Sanity -5, gain forbidden knowledge |
| necronomicon_scholar | events_day_people.py | "A professor spots the book. 'Where did you GET that?'" Sell for $2,000 or keep for power |
| necronomicon_portal | events_day_surreal.py | "The final page opens. Something looks back." Unique surreal branch |
| necronomicon_protection | events_day_dark.py | "Dark entities recoil from the book's presence." Protection from dark events |
| necronomicon_madness | events_day_dark.py | Cumulative: each reading erodes sanity but grants increasingly powerful protections |

### Running Shoes ($45) → Escape Enhancement

| Target Event | File | New Behavior |
|--------------|------|-------------|
| Chase events | events_day_dark.py | "Your running shoes eat pavement. The pursuer falls behind." Auto-escape |
| Night pursuit | events_night.py | "You sprint. The shoes grip perfectly." Avoid night chase damage |
| Adventure escape | adventures.py | "You outrun the danger." Emergency zone exit without penalty |
| Competition | events_day_people.py | "You win the impromptu footrace." +$100 and respect |
| Morning events | events_day_survival.py | "Your morning jog shakes off the cobwebs." +health passive |

### Deck of Cards ($9) → Street Games

| Target Event | File | New Behavior |
|--------------|------|-------------|
| Stranger bonding | events_day_people.py | "You pull out the deck. 'Want to play?' They sit down." Social event, +sanity |
| Bar games | events_day_people.py | "You deal a hand. The bar crowd gathers." Mini-gambling side event |
| Lonely night | events_night.py | "You play solitaire. The cards feel familiar. You're not alone." +sanity |
| Companion trick | events_day_companions.py | "You teach your companion a card trick. They're fascinated." +companion happiness |
| Prison/captivity | events_day_dark.py | "You pass the time with cards. The hours blur." Reduce dark event duration |

### Dog Whistle ($22) → Animal Communication

| Target Event | File | New Behavior |
|--------------|------|-------------|
| Wild dog pack | events_day_animals.py | "The whistle confuses the pack. They scatter." Avoid attack |
| Night howling | events_night.py | "You blow the whistle into the darkness. The howling stops." Silence threat |
| Companion call | events_day_companions.py | "Your companion hears the whistle from a mile away." Recall lost companion |
| Adventure animal | adventures.py | "The whistle draws a curious wolf. It tilts its head." Unique animal encounter |

### Disposable Camera ($20) → Evidence & Memory

| Target Event | File | New Behavior |
|--------------|------|-------------|
| Crime witness | events_day_dark.py | "You snap a photo. Evidence." Can report crime for reward later |
| Beautiful moment | events_day_surreal.py | "You photograph the impossible. The photo comes out blank." Surreal reaction |
| Companion photo | events_day_companions.py | "You photograph your companion. They look perfect." +sanity, +companion happiness |
| Tourist event | events_day_people.py | "A tourist asks you to take their photo. You keep one for yourself." Social moment |
| Adventure proof | adventures.py | "You photograph the treasure before touching it." Insurance against curse |

### Binoculars ($65) → Enhanced Scouting

| Target Event | File | New Behavior |
|--------------|------|-------------|
| Stranger approach | events_day_people.py | "Through the binoculars, you see they're smiling." Confirm safe encounter |
| Adventure scouting | adventures.py | "You scope the zone from the hilltop." Reveal sub-zone options before entering |
| Night watch | events_night.py | "Night-vision through binoculars: shadows, but nothing dangerous." Reduce night anxiety |
| Weather prediction | events_day_survival.py | "Storm clouds through the binoculars. You prepare." Advance weather warning |

### Luxury Items (Gold Chain, Fancy Cigars, Vintage Wine) → NPC Impression

| Target Event | File | New Behavior |
|--------------|------|-------------|
| High-society events | events_day_people.py | "Your gold chain catches the light. They treat you differently." Better NPC reactions |
| Business meetings | events_day_wealth.py | "You offer a cigar. The deal goes smoother." Better investment returns |
| Bartender events | events_day_people.py | "You pour from the vintage bottle. The table goes quiet." Social dominance |
| Gambling den | adventures.py | "Your luxury sends a message: you belong here." Better gambling den odds |

---

## 8. Tier 4 — Secret Multi-Item Combinations

**Goal:** Add 15+ hidden combinations that reward holding specific item pairs. These should feel like discoveries, not requirements.

### Defensive Combinations

| Items | Name | Effect | Where to Check |
|-------|------|--------|---------------|
| Necronomicon + Dream Catcher | Lucid Dreaming | All dreams become controllable — choose which dream to have. +sanity, skip nightmares | events_night.py, mechanics_intro.py |
| Phoenix Feather + Fire Starter Kit | Sacred Flame | Full heal (100 HP + 100 sanity), both items consumed. One-time miracle | events_day_survival.py |
| Scrap Armor + Road Flare Torch | Blazing Knight | All combat damage reduced to 0 for one encounter. Torch consumed | events_day_dark.py |
| Emergency Blanket + Fire Starter Kit | Fortress Mode | Immune to cold, rain, and night exposure for 3 days | events_day_survival.py, events_night.py |
| Quiet Sneakers + Tattered Cloak | Ghost Mode | Invisible to all hostile NPCs for the night. Both items lose 5 durability | events_night.py |

### Information Combinations

| Items | Name | Effect | Where to Check |
|-------|------|--------|---------------|
| Mirror of Duality + Marvin's Monocle | True Sight | See the Dealer's true form in the next dream. Unique dream scene | mechanics_intro.py |
| Oracle's Tome + Deck of Cards | Fortune Reading | Predict the next 3 events. Player receives warning text | day_cycle.py |
| Binocular Scope + Night Vision Scope | All-Seeing Eye | See hidden items in every area. +$500 bonus find per location visit | locations.py |
| Gambler's Grimoire + Hermit's Journal | Scholar's Insight | Combine both knowledge sources: reveal all crafting recipes + secret shop hint | systems.py |

### Social Combinations

| Items | Name | Effect | Where to Check |
|-------|------|--------|---------------|
| Vintage Wine + Gambler's Chalice | Royal Toast | Any NPC you meet gives you a gift. One-time use, wine consumed | events_day_people.py |
| Gold Chain + Velvet Gloves + Sapphire Watch | High Roller | Casino events always favor you. VIP access everywhere | events_day_casino.py, events_day_wealth.py |
| Deck of Cards + Dealer's Mercy | Dealer's Game | Challenge any NPC to blackjack. Win = they give you their best item | events_day_people.py |
| Fancy Cigars + Dog Whistle | Old Man's Trick | Summon a stray dog AND befriend it, no Animal Whistle needed. One-time | events_day_animals.py |

### Luck Combinations

| Items | Name | Effect | Where to Check |
|-------|------|--------|---------------|
| Lucky Penny + Lucky Coin + Lucky Charm Bracelet | Triple Luck | Blackjack odds +15% for 5 hands. All three consumed | systems.py |
| Worry Stone + Dream Catcher + Lucky Charm Bracelet | Peace of Mind | Full sanity restoration + permanent +5 max sanity. All consumed | events_day_items.py |
| Moon Shard + Lucky Medallion | Lunar Fortune | Night events always roll positive. Permanent passive | events_night.py |

### Companion Combinations

| Items | Name | Effect | Where to Check |
|-------|------|--------|---------------|
| Animal Whistle + Dog Whistle | Pack Call | All nearby animals gather. If you have a companion, their happiness maxes out | events_day_animals.py, events_day_companions.py |
| Pet Toy + Companion Bed + Feeding Station | Perfect Home | Companion happiness never decays. Permanent passive | game_flow.py |
| Shiv + Scrap Armor | Armed and Armored | Both you and your companion gain combat protection | events_day_dark.py, events_day_companions.py |

---

## 9. Tier 5 — Missing Systemic Mechanics

### NPC Gifting System

**Problem:** You can't give items to NPCs. Every item is either used on yourself or sold.

**Proposal:** Add `gift_item_to_npc(npc_name, item_name)` method to player_core.py.

| NPC | Likes | Effect |
|-----|-------|--------|
| Grimy Gus | Valuable items ($50+ pawn) | Better pawn prices permanently |
| Marvin | Flasks (return empty) | Discount on next purchase |
| Kyle (store) | Food items | Free item next visit |
| Tom / Frank / Oswald | Their specialty parts | Cheaper repair/service |
| Companions | Their food | Double happiness bonus |
| Random NPCs in events | Contextual gifts | Karma counter → affects ending |

### Companion Quest Items

**Problem:** Companions are bonded through feeding/time only. No companion-specific quests.

**Proposal:** Each companion unlocks a 3-step quest chain that yields a unique companion item.

| Companion | Quest Target | Reward Item |
|-----------|-------------|-------------|
| Thunder | Race training (3 wins) | Thunder's Horseshoe (+luck) |
| Bubbles | Fish 3 times | Bubbles' Scale (+swim protection) |
| Buddy | Fetch 3 items | Buddy's Collar (+loyalty, can't run away) |
| Grace | Visit 3 nature areas | Grace's Antler (+healing) |
| Slick | Explore 3 sewers | Slick's Ratstone (+danger sense) |

### Mechanic Loyalty Items

**Problem:** Choosing Tom/Frank/Oswald has no item reward.

**Proposal:** Each mechanic gives a unique item at dream stage 2.

| Mechanic | Item | Effect |
|----------|------|--------|
| Tom | Tom's Wrench | Car repairs cost 50% less at Tom's shop |
| Frank | Frank's Flask | +1 Flask durability on all flasks |
| Oswald | Oswald's Dice | +5% blackjack luck (passive) |

### Item Lore Discovery

**Problem:** Items have no backstory. They appear, they do a thing, they break.

**Proposal:** Some items gain lore text after 10+ uses. Add `_item_use_count` tracker.

| Item | Lore Threshold | Discovery Text |
|------|---------------|---------------|
| Gambler's Grimoire | 10 uses | "You find an inscription on the spine: 'To the one who keeps counting.'" |
| Phoenix Feather | 3 near-death | "The feather remembers every time it saved you. It's growing warmer." |
| Dream Catcher | 5 dreams | "You notice tiny symbols woven into the web. They match your dreams." |
| Dirty Old Hat | 15 days worn | "There's a name stitched inside the brim. Someone wore this before you." |

### Weather-Item Synergy

**Problem:** Weather happens, items exist, they never interact.

**Proposal:** Weather conditions buff/debuff certain items.

| Weather | Buffed Items | Debuffed Items |
|---------|-------------|---------------|
| Rain | Rain Collector (+double water), Umbrella (+sanity) | Fire Starter Kit (blocked), Road Flares (fizzle) |
| Heat | Cheap Sunscreen (essential), Water Purifier (critical) | Emergency Blanket (overheat -5 HP) |
| Cold | Fire Starter Kit (+warmth), Emergency Blanket (+essential) | Running Shoes (ice, -mobility) |
| Night | Flashlight (essential), Night Vision Scope (bonus) | Binoculars (useless) |
| Storm | Car Alarm Rigging (false alarm -sanity), Signal Mirror (useless) | Rain Collector (overflows +double water) |

### Flask Narrative Events

**Problem:** 11/12 flasks have zero narrative presence. They're bought, they affect cards, they break. No story.

**Proposal:** Add 1 narrative event per flask type.

| Flask | Event | File | Description |
|-------|-------|------|-------------|
| Flask of No Bust | no_bust_miracle | events_day_casino.py | "The flask glows. Your hand should have busted — but it didn't. The table goes silent." |
| Flask of Imminent Blackjack | blackjack_vision | events_day_casino.py | "You see the blackjack before the cards are dealt. The flask hums." |
| Flask of Dealer's Whispers | dealer_whisper_event | events_day_casino.py | "You hear the Dealer's voice through the flask: 'Hit.' You obey." |
| Flask of Bonus Fortune | fortune_overflow | events_day_wealth.py | "The flask overflows with golden light. Your winnings double, then triple." |
| Flask of Anti-Venom | venom_cure_moment | events_illness.py | "The venom recedes. The flask saved your life." |
| Flask of Anti-Virus | virus_cure_moment | events_illness.py | "Your fever breaks. The flask did what medicine couldn't." |
| Flask of Fortunate Day | lucky_day_event | events_day_items.py | "Everything goes right today. The flask radiates warmth." |
| Flask of Fortunate Night | lucky_night_event | events_night.py | "The stars align. The flask glows silver." |
| Flask of Second Chance | second_chance_moment | events_day_casino.py | "Time hiccups. You're back at the hand you just lost. Play again." |
| Flask of Split Serum | split_transformation | events_day_casino.py | "Your hand splits like a living thing. Two hands, twice the power." |
| Flask of Pocket Aces | pocket_aces_glory | events_day_casino.py | "You feel them before you see them. Two aces, burning in your pocket." |

---

## 10. Tier 6 — New Features

### Secret Shop (Marvin's Back Room)

**Unlock:** Own all 19 base Marvin items OR have balance > $500,000

**Inventory:**

| Item | Price | Effect |
|------|-------|--------|
| Dealer's Mirror | $50,000 | Shows what the Dealer sees. Permanent peek at hole card |
| The Last Card | $100,000 | Guarantee the next card drawn is exactly what you need. One use |
| Marvin's Eye | $75,000 | See all hidden event outcomes before choosing |
| Bottle of Tomorrow | $40,000 | Skip to the next day with full health/sanity |
| Blank Check | $200,000 | One free purchase from any shop, any item |

### Item Evolution Chains

Items that physically transform after enough use:

| Chain | Stage 1 | Stage 2 | Stage 3 |
|-------|---------|---------|---------|
| Blade | Pocket Knife (10 uses) → Utility Blade (15 uses) → Master Knife | Cuts faster, unlocks more locks, never breaks |
| Light | Flashlight (10 uses) → Lantern (15 uses) → Eternal Light | Brighter, reveals hidden items, permanent |
| Armor | Scrap Armor (5 combats) → Plated Vest (10 combats) → Road Warrior | More protection, lighter, adds intimidation |
| Charm | Lucky Penny (20 flips) → Lucky Coin (10 pushes) → Fortune's Token | Luck stacks, permanent passive |
| Compass | Worn Map (5 locations) → Rusty Compass (10 zones) → Golden Compass | Navigate perfectly, bonus loot, can't get lost |

### Hoarding Consequences

**Problem:** No downside to carrying 50+ items.

**Proposal:** At 20+ items, events start noticing:

| Item Count | Effect |
|-----------|--------|
| 20+ | "Your car is packed. Finding anything takes time." Slower event resolution |
| 30+ | "The weight of your possessions slows you down." -1 escape chance in chases |
| 40+ | "People stare. You look like a hoarder." Social penalties |
| 50+ | "Your companion can barely fit in the car." Companion happiness -5/day |

### Legendary 3-Ingredient Crafting

**Proposal:** The Car Workbench accepts special 3-ingredient recipes after reaching certain milestones.

| Recipe | Ingredients | Milestone | Result | Effect |
|--------|------------|-----------|--------|--------|
| Witch Doctor's Amulet | Phoenix Feather + Ritual Token + Alien Crystal | Beat 3 adventure bosses | Amulet of Marvin | Auto-revive once per life |
| Road King's Crown | Junkyard Crown + Scrap Metal Rose + Artisan's Toolkit | Complete artisan storyline | Crown of the Road | All NPCs treat you as royalty |
| Dream Walker's Lens | Dream Catcher + Sneaky Peeky Goggles + Mirror of Duality | See all 3 mechanic dreams | Lens of Truth | See true outcomes of every choice |
| Beast Master's Call | Animal Whistle + Dog Whistle + Moon Shard | Bond 5 companions | Master's Horn | All companions permanent, can't die or leave |
| Gambler's Soul | Gambler's Grimoire + Dealer's Mercy + Lucky Medallion | Win 100 blackjack hands | The Loaded Deck | +25% blackjack advantage permanent |

### "Wrong Item" Moments

**Problem:** Using an item always helps or does nothing. No comedy of errors.

**Proposal:** Some items have contextually wrong uses that create memorable moments:

| Situation | Wrong Item | What Happens |
|-----------|-----------|-------------|
| Campfire | Bug Spray | "The can explodes near the fire. -20 HP. Your eyebrows are gone." |
| Bear encounter | Dog Whistle | "The whistle summons a dog. The bear eats the dog. You feel terrible." |
| Formal dinner | Dirty Old Hat | "The maître d' physically recoils. You're escorted out." Banned from event |
| Night stealth | Road Flares | "You light a road flare for visibility. Every creature in a mile turns toward you." Ambush |
| Loan shark meeting | Necronomicon | "You open the book as collateral. The loan shark's eyes go white. He forgives all debts." Debt cleared, sanity -15 |
| Doctor visit | Flask of Anti-Venom | "The doctor examines the flask. 'This is snake oil. Literally.'" Lose flask, no treatment |
| Romance event | Pest Control | "You pull out a can of Pest Control. The mood evaporates instantly." Event fails |

---

## 11. Flask Narrative Integration

### Current Flask State

All 12 flasks live exclusively in `systems.py` (blackjack effects) and `durability.py` (degradation) and `locations.py` (Marvin's shop). No flask name appears in any event narrative file.

### Proposed Flask Reactions in Events

Beyond the standalone flask events in Tier 5, flasks should react to the world:

### Flask of Anti-Venom in Illness Events

| Target | File | Reaction |
|--------|------|----------|
| Snake bite | events_day_animals.py | "You uncork the Anti-Venom. The burning stops." Instant cure |
| Poison food | events_day_dark.py | "The flask neutralizes the poison before it reaches your stomach." Block food poisoning |
| Scorpion sting | events_day_survival.py | "A quick sip. The venom loses its grip." Block venom damage |
| Spider encounter | adventures.py | "The flask's contents glow near the spider. It hisses and retreats." Deterrent |

### Flask of Anti-Virus in Illness Events

| Target | File | Reaction |
|--------|------|----------|
| Illness onset | events_illness.py | "The flask fights the infection before symptoms start." Prevent illness |
| Contaminated water | events_day_survival.py | "You pour a drop into the water. Clean." Purify water |
| Hospital visit | locations.py | "The doctor tests the flask. 'This is more advanced than our medicine.'" Discount treatment |
| Companion illness | events_day_companions.py | "You give your companion a drop. They perk up immediately." Cure companion sickness |

### Flask of Fortunate Day/Night in Events

| Target | File | Reaction |
|--------|------|----------|
| *Any* day/night event | events_day_*.py / events_night.py | 5% chance: "The flask hums warm. Fate smiles." Bonus $50–200 on any event |
| Bad luck events | various | "The flask absorbs the bad luck. You feel lighter." Skip minor negative event |
| Gambling side-events | events_day_casino.py | "The flask grows warm near the table." Flavor text confirming luck is active |

### Flask of No Bust Side Effects in Events

| Target | File | Reaction |
|--------|------|----------|
| Near-death | events_day_dark.py | "Your body refuses to fail. The flask's magic holds." Survive lethal with 1 HP |
| Car crash | events_car.py | "The impact should have killed you. The flask disagrees." Reduce crash damage |
| Fall damage | events_day_survival.py | "You fall. But somehow you don't break." Reduce fall damage |

### Flask of Pocket Aces in Casino Events

| Target | File | Reaction |
|--------|------|----------|
| Casino entry | events_day_casino.py | "The flask pulses with twin heartbeats. Two aces, waiting." Flavor anticipation |
| Poker side-event | events_day_casino.py | "You feel the aces move. Even outside blackjack, they answer." +$200 on poker |
| Street dice | adventures.py | "The flask hums. Double sixes." Win street dice automatically |

### Flask Interaction Matrix

| Flask | # Proposed New Interactions | Primary Files Affected |
|-------|---------------------------|----------------------|
| Anti-Venom | 4 events + illness cure | events_day_animals, events_day_dark, events_day_survival, adventures |
| Anti-Virus | 4 events + illness block | events_illness, events_day_survival, locations, events_day_companions |
| Fortunate Day | 3 passive triggers | events_day_*.py (all day files) |
| Fortunate Night | 3 passive triggers | events_night.py |
| No Bust | 3 survival saves | events_day_dark, events_car, events_day_survival |
| Pocket Aces | 3 gambling reactions | events_day_casino, adventures |
| Second Chance | 2 redo moments | events_day_dark, events_day_survival |
| Imminent Blackjack | 2 vision moments | events_day_casino, events_day_surreal |
| Dealer's Whispers | 2 voice moments | events_day_casino, mechanics_intro |
| Bonus Fortune | 2 overflow moments | events_day_wealth, events_day_casino |
| Split Serum | 1 transformation | events_day_casino |
| Dealer's Hesitation | Already has narrative | (skip) |

---

## 12. Companion-Item Synergy Plan

### Current Companion-Item State

Companions only interact with items through:
1. Feeding (specific food item → +happiness)
2. Animal Whistle (recruitment gate)
3. Companion Bed / Pet Toy / Feeding Station (happiness boosters)

### Proposed: Companions React to Player Items

| Companion | Item Reaction | Effect |
|-----------|--------------|--------|
| Thunder (Horse) | Running Shoes | "Thunder races alongside you. He's faster." Double escape bonus |
| Bubbles (Fish) | Fishing Rod | "Bubbles leads you to the best fishing spot." Guaranteed rare catch |
| Buddy (Dog) | Dog Whistle | "Buddy goes crazy at the sound. He digs up something buried." Find hidden item |
| Grace (Deer) | Dream Catcher | "Grace sleeps peacefully near the catcher. No nightmares tonight." Companion happiness bonus at night |
| Bruno (Bear) | Scrap Armor | "Bruno wears the armor plate like a badge." +companion protection |
| Slick (Rat) | Lockpick Set | "Slick watches you pick the lock. Next time, he does it himself." Auto-open locks |
| Echo (Cat) | Disposable Camera | "Echo strikes a pose. Even cats know they're photogenic." +sanity |
| Chomper (Gator) | Fish bait items | "Chomper is very interested in your bait." Feed companion auto |
| Moonwhisker (Rabbit) | Lucky Charm Bracelet | "Moonwhisker's foot twitches near the bracelet. Double lucky." +luck stack |
| Shellbert (Turtle) | Worry Stone | "Shellbert nuzzles the stone. Both of you relax." +sanity, +happiness |
| Asphalt (Road Dog) | Road Flares | "Asphalt tilts his head at the flare, then leads you through the dark." Night navigation bonus |
| Ursus (Bear) | Beef Jerky | "Ursus snatches the jerky. You've never seen him so happy." +20 happiness, jerky consumed |
| Deathclaw (Crab) | Slingshot | "Deathclaw catches the pellet in his claw. He thinks it's a game." +happiness |
| Kraken (Octopus) | Water Purifier | "Kraken's tentacles curl around the purifier. 'Clean water is life,' he seems to say." Deep bond moment |

### Proposed: Companions Find Items

Bonded companions (happiness ≥ 80) should occasionally find items.

| Companion | Found Item | Condition |
|-----------|-----------|-----------|
| Buddy (Dog) | Random pawn-value item | 10% chance per day when bonded |
| Slick (Rat) | Lucky Penny / Pocket Knife | 5% chance per night when bonded |
| Mr. Pecks (Crow) | Shiny item (Gold Chain, Lucky Coin) | 3% chance per day when bonded |
| Rusty (Raccoon) | Stolen item from NPC | 5% chance per day when bonded |
| Moonwhisker (Rabbit) | Magic Acorn / Moon Shard | 2% chance per night when bonded |

---

## 13. Adventure Zone Item Gaps

### Items That Should Matter in Adventures but Don't

| Item | Zone | Proposed Interaction |
|------|------|---------------------|
| Flashlight | All underground/cave | "The flashlight reveals a hidden passage." Bonus loot |
| First Aid Kit | All combat zones | "You patch yourself up between encounters." Mid-zone heal |
| Binoculars | Road, Woodlands, Beach | "You scout ahead." Reveal sub-zone type before entering |
| Rope | Woodlands, Underwater | "You rappel down the cliff." Access hidden area |
| Pocket Knife | All zones | "You cut through the brush." Shortcut, skip obstacle |
| Scrap Armor | All combat zones | Reduce boss damage taken |
| Pepper Spray | City, Road | Emergency escape in dangerous sub-zones |
| Lockpick Set | City, Underwater | Open locked containers for bonus loot |
| Fishing Rod | Swamp, Beach, Underwater | Catch food/items in water zones |
| Fire Starter Kit | Woodlands, Beach | Build camp, rest mid-zone |
| Tool Kit | City, Road | Fix broken things for rewards |
| Emergency Blanket | All zones (night variant) | Recovery if adventure runs long |

### Items That Should Be Adventure Rewards but Aren't

| Zone | Missing Reward | Proposed |
|------|---------------|----------|
| Road | No persistent item | Road Warrior Badge: +escape chance in all road events |
| City | No persistent item | Underground Pass: access to secret city sub-zones |
| Woodlands | Limited items | Druid's Staff: nature events always positive |
| Swamp | Limited items | Swamp Rune: poison immunity |
| Beach | Limited items | Sea Glass: sell to Marvin for flask discount |
| Underwater | Good items but rare | Depth Charm: underwater adventures always give bonus loot |

---

## 14. Event Weight Tuning Notes

### Items That Should Affect Event Pools

Currently, the event pool is built purely on wealth rank. Items should influence pool composition:

| Item | Pool Effect |
|------|------------|
| Dream Catcher | Reduce nightmare event weight by 50% at night |
| Necronomicon | Increase dark event weight by 25% (you invited this) |
| Lucky Charm Bracelet | Increase positive event weight by 10% during day |
| Flask of Fortunate Day | Increase positive event weight by 15% during day (while active) |
| Flask of Fortunate Night | Increase positive event weight by 15% at night (while active) |
| Scrap Armor | Reduce combat event weight by 20% (thugs avoid the armored one) |
| Animal Whistle | Increase animal event weight by 30% |
| Road Flare Torch | Reduce dark event weight by 15% at night |
| Fire Starter Kit | Increase camp/rest event weight by 20% |

### Proposed: Inventory-Aware Pool Modifier

Add to `make_weighted_day_pool()`:

```
After building base pool from rank:
- For each pool-affecting item the player owns:
  - Multiply relevant event weights by modifier
  - Rebuild pool with adjusted weights
```

This makes items feel like they reshape your world, not just react to it.

---

## 15. Implementation Priority Matrix

### Priority 1 — Highest Impact, Lowest Effort

| Change | Files Touched | Est. Checks Added | Impact |
|--------|--------------|-------------------|--------|
| Marvin items react to events (Tier 1) | 8 event files | ~60 has_item checks | Huge — expensive items finally feel alive |
| Secret multi-item combos (Tier 4) | 6 event files | ~15 combo checks | Huge — players discover hidden synergies |
| Flask narrative events (Tier 5 subset) | 5 event files | ~12 flask checks | High — $10K+ items get story moments |

### Priority 2 — Medium Impact, Medium Effort

| Change | Files Touched | Est. Checks Added | Impact |
|--------|--------------|-------------------|--------|
| Crafted items cross boundaries (Tier 2) | 6+ event files | ~57 has_item checks | High — crafting feels more rewarding |
| Store items come alive (Tier 3) | 5 event files | ~25 has_item checks | Medium — cheap items feel worthwhile |
| Companion-item synergy (Section 12) | 3 event files + game_flow | ~14 checks | Medium — companions feel connected to items |

### Priority 3 — High Impact, High Effort (New Systems)

| Change | Files Touched | New Code | Impact |
|--------|--------------|----------|--------|
| NPC gifting system | player_core + locations + events | New method + ~20 gift checks | Medium — adds social depth |
| Item evolution chains | systems + player_core | New tracking + 5 evolution chains | High — long-term item investment |
| Weather-item synergy | day_cycle + all event files | New weather system hooks | Medium — world feels dynamic |
| Inventory-aware pools | event_dispatch + lists | Pool modifier function | High — items reshape the world |

### Priority 4 — Nice to Have (Future)

| Change | Notes |
|--------|-------|
| Secret Marvin back room | Endgame content, needs balance testing |
| Legendary 3-ingredient crafting | Needs milestone tracking infrastructure |
| Hoarding consequences | Could frustrate collectors, needs playtesting |
| "Wrong item" comedy | Fun but low urgency |
| Companion quest chains | Significant new content, full storylines |
| Item lore discovery | Needs use-count tracking, medium infrastructure |

---

## Appendix A: Complete Item-to-File Cross-Reference

For quick lookup: which files check which items.

| Item | events_day_items | events_day_dark | events_day_survival | events_day_people | events_day_wealth | events_day_animals | events_day_surreal | events_day_numbers | events_day_companions | events_day_casino | events_day_storylines | events_night | adventures | events_car | events_illness | mechanics_intro | locations |
|------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| Animal Whistle | | | | ✓ | | ✓ | | | ✓ | | ✓ | ✓ | ✓ | | | | ✓ |
| Pocket Knife | ✓ | | ✓ | | | | | | | | ✓ | ✓ | | ✓ | | | |
| Duct Tape | | | ✓ | | | | | | | | | | ✓ | ✓ | | | |
| Tool Kit | | | ✓ | | | | | | | | ✓ | | | ✓ | | | |
| Flashlight | ✓ | | ✓ | | | | | | | | | ✓ | | | | | |
| Pest Control | | | ✓ | | | ✓ | | | | | | ✓ | | | | | |
| Spare Tire | | | ✓ | | | | | | | | | | | ✓ | | | ✓ |
| First Aid Kit | ✓ | | ✓ | | | | | | | | | | | | ✓ | | |
| Binoculars | ✓ | | ✓ | | | | | | | | | ✓ | | | | | |
| Quiet Sneakers | | | | | | | | | | | | ✓ | | | | | |
| Marvin's Monocle | | | | | | | | | | | | | | | | | ✓ |
| Scrap Armor | | ✓ | | | | | | | | | | | | | | | |
| All other Marvin items | | | | | | | | | | | | | | | | | |
| All 11 flasks | | | | | | | | | | | | | | | | | |

**Key insight from this table:** The bottom-right is almost entirely empty. Marvin items, flasks, and most crafted items don't appear anywhere in the event grid. That's the gap this plan fills.

---

## Appendix B: Pawn Value Quick Reference

For balancing new item rewards and checking if consumption is fair.

| Tier | Items | Pawn Range |
|------|-------|-----------|
| Junk | Garbage Bag, Matches, Rubber Bands, Lighter | $1–$5 |
| Cheap | Flashlight, Poncho, Cough Drops, Blanket | $4–$15 |
| Moderate | Pocket Knife, Jumper Cables, Slingshot, Lockpick Set | $10–$35 |
| Valuable | Scrap Armor, Artisan's Toolkit, Tool Kit, Night Vision Scope | $40–$60 |
| Luxury | Vintage Wine, Camera, Laptop, Gold Chain | $75–$200 |
| Premium | Diamond Ring, Designer Watch, Silver Bar | $200–$500 |
| Priceless | Animal Whistle, Marvin items, Flasks | Can pawn but shouldn't — irreplaceable |

---

## Appendix C: Crafting Recipe Quick Reference

All 26 recipes for cross-referencing in new event implementations.

| Result | Ingredient 1 | Ingredient 2 | Category |
|--------|-------------|-------------|----------|
| Shiv | Duct Tape | Pocket Knife | Weapon |
| Slingshot | Rubber Bands | Bungee Cords | Weapon |
| Road Flare Torch | Road Flares | Duct Tape | Weapon |
| Pepper Spray | Bug Spray | Lighter | Weapon |
| Improvised Trap | Fishing Line | Pocket Knife | Trap |
| Car Alarm Rigging | Bungee Cords | Spare Fuses | Trap |
| Snare Trap | Rope | Fishing Line | Trap |
| Home Remedy | First Aid Kit | Cough Drops | Remedy |
| Wound Salve | First Aid Kit | Super Glue | Remedy |
| Splint | Duct Tape | Rope | Remedy |
| Smelling Salts | Hand Warmers | Breath Mints | Remedy |
| Lockpick Set | Pocket Knife | Fishing Line | Tool |
| Fishing Rod | Fishing Line | Rope | Tool |
| Binocular Scope | Binoculars | Duct Tape | Tool |
| Signal Mirror | Broken Compass | Super Glue | Tool |
| Lucky Charm Bracelet | Lucky Penny | Fishing Line | Charm |
| Dream Catcher | Fishing Line | Rubber Bands | Charm |
| Worry Stone | Lucky Penny | Hand Warmers | Charm |
| Rain Collector | Plastic Wrap | Garbage Bag | Survival |
| Emergency Blanket | Garbage Bag | Duct Tape | Survival |
| Smoke Signal Kit | Road Flares | Garbage Bag | Survival |
| Fire Starter Kit | Lighter | Hand Warmers | Survival |
| Water Purifier | Plastic Wrap | Lighter | Survival |
| Companion Bed | Blanket | Duct Tape | Companion |
| Pet Toy | Rope | Rubber Bands | Companion |
| Feeding Station | Plastic Wrap | Duct Tape | Companion |
| Scrap Armor | Shiv + Slingshot + Road Flare Torch | (3 ingredients) | Legendary |

---

## Appendix D: Exact Insertion Points — Function Names & Lines

Every proposed item check needs to land inside an existing event function. This appendix maps exact targets.

### events_day_dark.py — Insertion Targets

| Function | Line | Category | Items That Should React |
|----------|------|----------|------------------------|
| `the_desperate_gambler` | 136 | Con/Deception | Sneaky Peeky Shades/Goggles ("You notice his sob story doesn't match his shoes. Scam.") |
| `casino_hitman` | 515 | Combat | Phoenix Feather (survive), Scrap Armor (reduce damage), Tattered Cloak (never found) |
| `the_confession` | 632 | Deception | Oracle's Tome ("The Tome's margin: 'He's lying about the storage unit.'") |
| `back_alley_shortcut` | 813 | Mugging | Tattered Cloak (invisible, skip), Pepper Spray (spray, escape), Road Flare Torch (scare off) |
| `gas_station_robbery` | 970 | Robbery | Tattered Cloak (hide), Scrap Armor (reduce), Lucky Medallion (gun jams) |
| `drug_dealer_encounter` | 1306 | Law | Dirty Old Hat (mistaken for harmless, let go), Running Shoes (sprint away) |
| `food_poisoning` | 1484 | Illness | Home Remedy (cure), Flask of Anti-Virus (prevent), Water Purifier (would have prevented) |
| `attacked_by_dog` | 1535 | Combat | Dog Whistle (calm dog), Animal Whistle (befriend), Scrap Armor (reduce bite) |
| `electrocution_hazard` | 1626 | Hazard | Worn Gloves/Velvet Gloves (insulation, avoid shock) |
| `car_explosion` | 1677 | Hazard | Health Manipulator (adrenaline boost, reduce damage), Scrap Armor (shrapnel protection) |
| `devils_bargain_consequence` | 1822 | Devil | Dream Catcher ("The catcher intercepts the Devil's whisper"), Oracle's Tome (warned you) |
| `soulless_emptiness` | 1860 | Devil | Worry Stone (anchor to reality, +sanity), Delight Indicator (reads zero, flavor) |
| `soulless_mirror` | 1876 | Devil | Twin's Locket / Mirror of Duality (the mirror shows both faces, unique text) |

### events_day_people.py — Insertion Targets

| Function | Line | Category | Items That Should React |
|----------|------|----------|------------------------|
| `lone_cowboy` | 115 | Stranger | Golden Watch ("He notices your watch. 'You're not from around here.'") |
| `social_encounter` | 377 | Social | Deck of Cards (break the ice, +sanity), Vintage Wine (share, better outcome) |
| `robbery_attempt` | 460 | Theft | Car Alarm Rigging (triggers, thief runs), Scrap Armor (intimidation) |
| `photo_opportunity` | 505 | Business | Disposable Camera (take photo, +reward), Binoculars (spot opportunity) |
| `classy_encounter` | 530 | Elegance | Velvet Gloves + Sapphire Watch + Gold Chain (instant VIP treatment) |
| `wine_and_dine` | 567 | Dining | Gambler's Chalice ("You drink from the Chalice. The table falls silent.") |
| `cigar_circle` | 597 | Social | Fancy Cigars (instant welcome), Dirty Old Hat (rejected) |
| `lost_tourist` | 672 | Stranger | Rusty Compass/Golden Compass ("You point them in the right direction.") |
| `fancy_coffee` | 1030 | Elegance | Gold Chain (free upgrade), Dirty Old Hat (barista gives you side-eye) |
| `the_hitchhiker` | 1086 | Stranger | Binoculars (scope them first), Pepper Spray (safety net visible) |
| `the_prophet` | 1123 | Stranger | Oracle's Tome ("The prophet reads the Tome. His eyes widen."), Necronomicon (recoils in fear) |
| `the_doppelganger` | 1206 | Identity | Twin's Locket (opens, shows both of you), Mirror of Duality (cracks) |
| `yard_sale_find` | 1345 | Business | Marvin's Monocle (identify hidden treasure in junk pile), Binoculars (spot rare item) |
| `friendly_drunk` | 1389 | Bar | Gambler's Chalice (drink together), Deck of Cards (play together, +sanity) |
| `parking_lot_poker` | 1463 | Hustle | Sneaky Peeky Shades (see marked cards), Deck of Cards (use your own clean deck) |
| `fancy_restaurant_mistake` | 1831 | Elegance | Gold Chain + Velvet Gloves (they let you stay), Dirty Old Hat (thrown out immediately) |

### events_day_surreal.py — Insertion Targets

| Function | Line | Category | Items That Should React |
|----------|------|----------|------------------------|
| `sock_puppet_therapist` | 54 | Existential | Delight Indicator (reads "confused"), Worry Stone (anchors you) |
| `time_loop` | 90 | Temporal | Pocket Watch/Grandfather Clock ("The clock counts the loops"), Golden Watch (hands spin backwards) |
| `mirror_stranger` | 132 | Mirror | Mirror of Duality (both reflections speak), Twin's Locket (opens in the mirror) |
| `the_glitch` | 156 | Reality break | Oracle's Tome (predicts the glitch), Dream Catcher (catches the broken reality fragment) |
| `wrong_universe` | 201 | Identity | Twin's Locket (your other self has one too), Mirror of Duality (shows infinite reflections) |
| `fourth_wall_break` | 235 | Reality | Gambler's Grimoire ("The Grimoire writes: 'They're reading about you right now.'") |
| `the_collector` | 267 | Existential | Twin's Locket (he already has one from another you), Phoenix Feather (you can't be collected — you keep living) |
| `the_empty_room` | 310 | Existential | Worry Stone (something to hold), Dream Catcher (catches the emptiness) |
| `blood_moon_bargain` | 341 | Devil deal | Oracle's Tome (screams warning), Dealer's Grudge (burns), Necronomicon (dark entities recoil from the moon) |
| `alien_abduction` | 382 | Alien | Disposable Camera (photograph aliens, proof), Binocular Scope (see mothership) |

### events_day_casino.py — Insertion Targets

| Function | Line | Category | Items That Should React |
|----------|------|----------|------------------------|
| `perfect_hand` | 56 | Special | Lucky Charm Bracelet (glow), Flask of Pocket Aces (pulse) |
| `high_stakes_feeling` | 80 | Atmosphere | Gambler's Grimoire (records the milestone), Dealer's Grudge/Mercy (dealer reacts) |
| `casino_security` | 107 | Paranoia | Tattered Cloak (invisible to cameras), Dirty Old Hat (look like nobody) |
| `even_further_interrogation` | 126 | Interrogation | Sneaky Peeky Shades (read interrogator), Oracle's Tome (know what they'll ask) |
| `the_dying_dealer` | 169 | Story | Dealer's Mercy (the dealer forgives), Phoenix Feather (save him? — consumed) |

### events_night.py — Insertion Targets

| Function | Line | Category | Items That Should React |
|----------|------|----------|------------------------|
| `woodlands_path` | 95 | Creature | Flashlight (see ahead), Dream Catcher (prophetic shimmer), Fire Starter Kit (campfire wards) |
| `woodlands_river` | 204 | Creature | Fishing Rod (fish instead of danger), Rope (safe crossing) |
| `woodlands_field` | 303 | Encounter | Binoculars (scope field first), Slingshot (scare wasps) |
| `swamp_stroll` | 392 | Creature | Pepper Spray (snake deterrent), Flask of Anti-Venom (immune to bites) |
| `swamp_wade` | 552 | Danger | Scrap Armor (gator protection), Emergency Blanket (warmth after swim) |
| `swamp_swim` | 692 | Danger | Gator Tooth Necklace (respect), Flask of No Bust ("Your body refuses to fail") |
| `beach_stroll` | 879 | Mixed | Lucky Charm Bracelet (find something), Worry Stone (peaceful night +sanity) |
| `beach_swim` | 1053 | Danger | Emergency Blanket (hypothermia prevention), Splint (injury after swim) |
| `city_streets` | 1321 | Urban | Tattered Cloak (invisible), Running Shoes (fast escape), Pepper Spray (mugger defense) |
| `city_stroll` | 1567 | Urban | Dirty Old Hat (look harmless), Flashlight (see danger), Deck of Cards (street card game) |
| `city_park` | 1742 | Mixed | Worry Stone (peace +sanity), Dog Whistle (attract stray), Companion Bed (rest with companion) |
| `midnight_snack_run` | 2021 | Timing | Golden Watch (know exact time), Lucky Coin (find dropped money) |
| `mysterious_lights` | 2042 | Surreal | Binocular Scope (see lights clearly), Disposable Camera (photograph UFO) |
| `late_night_radio` | 2054 | Timing | Strange Frequency Dial (tune in to hidden broadcast), Static Recorder (record message) |
| `insomnia_night` | 2148 | Sleep | Dream Catcher (helps fall asleep), Worry Stone (calms mind), Smelling Salts (stay alert instead) |
| `nightmare` | 2342 | Dream | Dream Catcher (catch nightmare), Worry Stone (anchor), Necronomicon (nightmare bows to darker power) |
| `police_checkpoint` | 2289 | Law | Dirty Old Hat (look harmless), Running Shoes (flee checkpoint) |

### adventures.py — Insertion Targets

| Zone | Sub-function Area | Items That Should React |
|------|-------------------|------------------------|
| Road — Street Dice | L59–L200 | Deck of Cards (use clean deck), Sneaky Peeky Shades (see loaded dice) |
| Road — Broken Bus | L350–L500 | Tool Kit (fix bus, bigger reward), Duct Tape (partial fix) |
| Road — Road Dog | L560–L700 | Dog Whistle (befriend without Animal Whistle), Running Shoes (keep up with dog) |
| Woodlands — Hunting | L894–L1050 | Slingshot (hunting weapon), Binocular Scope (spot prey), Snare Trap (passive hunting) |
| Woodlands — Bear | L1050–L1200 | Scrap Armor (survive attack), Pepper Spray (bear deterrent), Fire Starter Kit (scare bear) |
| Woodlands — Fountain | L1200–L1300 | Water Purifier (purify fountain water first, better outcome), Binoculars (see if safe) |
| Swamp — Ogre | L1400–L1600 | Scrap Armor (take hit), Pepper Spray (spray ogre), Slingshot (ranged attack) |
| Swamp — Fairy | L1600–L1700 | Dream Catcher (protect wishes), Lucky Charm Bracelet (better wish outcomes) |
| Beach — Bonfire | L1950–L2100 | Fire Starter Kit (enhance ritual), Dream Catcher (catch visions), Worry Stone (steady mind during ritual) |
| Beach — Crab Racing | L2200–L2400 | Binoculars (scout crabs), Lucky Coin (flip for lane choice) |
| Underwater — Shipwreck | L2550–L2750 | Lockpick Set (open locked chests), Flashlight (see in dark water), Tool Kit (pry open hatches) |
| Underwater — Kraken | L2800–L3000 | Scrap Armor (tentacle whip protection), Flask of No Bust (survive crushing pressure) |
| City — Gambling Den | L3066–L3200 | Deck of Cards (play your way in), Sneaky Peeky Shades (spot cheaters) |
| City — Bank Heist | L3600–L3800 | Lockpick Set (faster escape), Running Shoes (flee scene), Tattered Cloak (cameras miss you) |

---

## Appendix E: Draft Narrative Text Samples

Example `has_item()` text for the most impactful additions. These show the tone and length for implementation.

### Sneaky Peeky Goggles in `the_desperate_gambler` (events_day_dark.py L136)

```python
if self.has_item("Sneaky Peeky Goggles") or self.has_item("Sneaky Peeky Shades"):
    self.typer("Through the enchanted lenses, you notice something off. His tears are dry. His 'eviction notice' is a grocery list folded backwards. His watch costs more than your car.", 0.02)
    self.typer("You walk away. The scammer stares after you, bewildered.", 0.02)
    self.typer("'How did you—' he starts. But you're already gone.", 0.02)
    self.change_balance(0)  # no loss
    return
```

### Tattered Cloak in `back_alley_shortcut` (events_day_dark.py L813)

```python
if self.has_item("Invisible Cloak"):
    self.typer("You pull the cloak tight around your shoulders. The fabric shimmers and you feel the world's attention slide off you like water.", 0.02)
    self.typer("Three men step out of the shadows. Knives glint. But their eyes pass right over the space where you're standing.", 0.02)
    self.typer("'Thought I heard someone,' one mutters. They disappear back into the dark.", 0.02)
    self.typer("You exhale and keep walking.", 0.02)
    return
elif self.has_item("Tattered Cloak"):
    self.typer("You wrap the cloak around yourself. It doesn't make you invisible — not quite — but the men hesitate.", 0.02)
    self.typer("'Just a homeless guy,' one whispers. They let you pass.", 0.02)
    self.change_balance(-50)  # they take a little something
    return
```

### Oracle's Tome in `blood_moon_bargain` (events_day_surreal.py L341)

```python
if self.has_item("Oracle's Tome") or self.has_item("Gambler's Grimoire"):
    book_name = "Oracle's Tome" if self.has_item("Oracle's Tome") else "Gambler's Grimoire"
    self.typer(f"The {book_name} erupts from your bag. Its pages turn in a wind that isn't there.", 0.02)
    self.typer("You catch a glimpse of the text: 'THE MOON LIES. EVERY DEAL IS A DEBT. EVERY GIFT IS A HOOK.'", 0.02)
    self.typer("The blood moon's light dims. The shadow offering the deal takes a step back.", 0.02)
    self.typer("'You... carry a warning,' it hisses. 'Very well. Not tonight.'", 0.02)
    self.restore_sanity(5)
    return
```

### Phoenix Feather in `casino_hitman` (events_day_dark.py L515)

```python
if self.has_item("Phoenix Feather"):
    self.typer("The hitman fires. The bullet strikes the feather in your breast pocket.", 0.02)
    self.typer("For one heartbeat, nothing happens. Then the feather ignites.", 0.02)
    self.typer("Golden fire erupts from the wound, cauterizing it shut. The hitman staggers back, gun shaking.", 0.02)
    self.typer("'What ARE you?' he whispers. Then he runs.", 0.02)
    self.typer("You look down. The feather is ash. But you're alive.", 0.02)
    self.use_item("Phoenix Feather")
    self.hurt(10)  # injured but alive
    return
elif self.has_item("White Feather"):
    self.typer("The feather in your pocket grows warm. Not enough to save you — but enough to warn you.", 0.02)
    self.typer("You duck behind the slot machines half a second before the shot.", 0.02)
    self.hurt(25)  # still shot, but not killed
    return
```

### Dream Catcher in `nightmare` (events_night.py L2342)

```python
if self.has_item("Dream Catcher"):
    self.typer("The nightmare begins to form — dark water, drowning, cards scattering into nothing —", 0.02)
    self.typer("But the Dream Catcher above your rearview mirror glows. Threads of bad dream snag in the web like flies.", 0.02)
    self.typer("The nightmare dissolves. What replaces it is silence. Good silence.", 0.02)
    self.typer("You sleep through till morning.", 0.02)
    self.restore_sanity(5)
    return
```

### Necronomicon + Dream Catcher Combo in `nightmare` (events_night.py L2342)

```python
if self.has_item("Necronomicon") and self.has_item("Dream Catcher"):
    self.typer("The nightmare begins — but the Necronomicon opens in the dream.", 0.02)
    self.typer("You see the text, clear as daylight: instructions for lucid dreaming, written in a language you suddenly understand.", 0.02)
    self.typer("The Dream Catcher's threads glow. The nightmare reshapes itself around your will.", 0.02)
    self.typer("You choose to dream of winning. You choose to dream of sunlight.", 0.02)
    self.typer("When you wake, you feel like a god.", 0.02)
    self.restore_sanity(15)
    self.heal(10)
    return
```

### Twin's Locket in `mirror_stranger` (events_day_surreal.py L132)

```python
if self.has_item("Mirror of Duality"):
    self.typer("The reflection holds up a sign: 'SOON.'", 0.02)
    self.typer("You hold up the Mirror of Duality. The reflection freezes.", 0.02)
    self.typer("Slowly, the mirror-you lowers the sign. Both reflections — yours and the one in the Mirror — stare at each other.", 0.02)
    self.typer("'There are three of us now,' the reflection whispers. 'When did that happen?'", 0.02)
    self.typer("The Mirror cracks. One thin line, top to bottom. But the reflections smile.", 0.02)
    self.restore_sanity(3)
    return
elif self.has_item("Twin's Locket"):
    self.typer("The reflection holds up a sign: 'SOON.'", 0.02)
    self.typer("The Twin's Locket grows warm against your chest. You open it.", 0.02)
    self.typer("Inside, both faces stare back — yours and the reflection's. They're the same face.", 0.02)
    self.typer("The reflection touches its own chest, where a locket hangs. It opens it too.", 0.02)
    self.typer("You both close your lockets at the same time.", 0.02)
    return
```

### Phoenix Feather + Fire Starter Kit Combo in survival events

```python
if self.has_item("Phoenix Feather") and self.has_item("Fire Starter Kit"):
    self.typer("You strike the Fire Starter. But the spark catches the Phoenix Feather instead.", 0.02)
    self.typer("Sacred flame erupts — warm, golden, impossibly gentle. It doesn't burn. It heals.", 0.02)
    self.typer("Every wound closes. Every ache fades. For one perfect moment, you are whole.", 0.02)
    self.typer("The feather and the fire starter are both ash now. But you have never felt more alive.", 0.02)
    self.use_item("Phoenix Feather")
    self.use_item("Fire Starter Kit")
    self.heal(100)
    self.restore_sanity(100)
    return
```

### Gambler's Chalice in `wine_and_dine` (events_day_people.py L567)

```python
if self.has_item("Overflowing Goblet") or self.has_item("Gambler's Chalice"):
    cup_name = "Overflowing Goblet" if self.has_item("Overflowing Goblet") else "Gambler's Chalice"
    self.typer(f"You set the {cup_name} on the table. The wine pours itself.", 0.02)
    self.typer("The dining room goes quiet. Every eye finds the cup that never empties.", 0.02)
    self.typer("'Where did you get that?' your host asks, voice barely a whisper.", 0.02)
    self.typer("'From a witch doctor,' you say. And for some reason, they believe you.", 0.02)
    self.typer("Dinner is on them. Everything is on them tonight.", 0.02)
    self.change_balance(500)
    self.restore_sanity(10)
    return
```

### Dirty Old Hat in `fancy_restaurant_mistake` (events_day_people.py L1831)

```python
if self.has_item("Dirty Old Hat") or self.has_item("Unwashed Hair"):
    hat_name = "Unwashed Hair implant" if self.has_item("Unwashed Hair") else "Dirty Old Hat"
    self.typer("The maître d' takes one look at you and physically recoils.", 0.02)
    self.typer(f"'Sir, your... {hat_name.lower()}... does not meet our dress code.'", 0.02)
    self.typer("You're escorted out before the bread arrives.", 0.02)
    self.typer("Outside, a homeless man high-fives you. 'Nice hat.'", 0.02)
    self.lose_sanity(3)
    return
```

### Running Shoes in chase events (events_day_dark.py various)

```python
if self.has_item("Running Shoes"):
    self.typer("Your Running Shoes grip the pavement. You were born for this — the sprint, the escape, the clean getaway.", 0.02)
    self.typer("Behind you, heavy boots stumble on gravel. The gap widens with every stride.", 0.02)
    self.typer("By the time they round the corner, you're three blocks away and climbing.", 0.02)
    return  # clean escape, no damage
```

### Deck of Cards in `insomnia_night` (events_night.py L2148)

```python
if self.has_item("Deck of Cards"):
    self.typer("You can't sleep. The ceiling stares back at you.", 0.02)
    self.typer("You pull out the deck. Shuffle. Cut. Deal. Solitaire.", 0.02)
    self.typer("The familiar rhythm of cards on cardboard fills the silence.", 0.02)
    self.typer("Shuffle. Cut. Deal. Your breathing slows.", 0.02)
    self.typer("You fall asleep with a king of hearts on your chest.", 0.02)
    self.restore_sanity(8)
    return
```

---

## Appendix F: Event Pool Modifier Pseudocode

How inventory-aware event weighting would work in `make_weighted_day_pool()`:

```python
def make_weighted_day_pool(self, rank):
    pool = self._build_base_pool(rank)  # existing logic
    
    # Item-based pool modifiers
    modifiers = {}
    
    if self.has_item("Dream Catcher"):
        modifiers["nightmare"] = 0.5      # 50% fewer nightmares
        modifiers["insomnia_night"] = 0.5
        
    if self.has_item("Necronomicon"):
        # Dark events increase — you invited this
        for event in self._dark_events:
            modifiers[event] = modifiers.get(event, 1.0) * 1.25
            
    if self.has_item("Lucky Charm Bracelet"):
        for event in self._positive_events:
            modifiers[event] = modifiers.get(event, 1.0) * 1.10
            
    if self.has_item("Animal Whistle"):
        for event in self._animal_events:
            modifiers[event] = modifiers.get(event, 1.0) * 1.30
            
    if self.has_item("Scrap Armor"):
        for event in self._combat_events:
            modifiers[event] = modifiers.get(event, 1.0) * 0.80
    
    if self.has_item("Road Flare Torch") or self.has_item("Fire Starter Kit"):
        for event in self._dark_night_events:
            modifiers[event] = modifiers.get(event, 1.0) * 0.85
    
    # Apply modifiers to pool
    modified_pool = []
    for event in pool:
        count = max(1, round(pool.count(event) * modifiers.get(event, 1.0)))
        modified_pool.extend([event] * count)
    
    random.shuffle(modified_pool)
    return modified_pool
```

---

## Appendix G: Complete Proposed Item Interaction Count

Summary of all proposed new interactions across the entire plan.

| Section | New has_item Checks | New Combo Checks | New Events | Files Modified |
|---------|-------------------|-----------------|------------|---------------|
| Tier 1 (Marvin items) | ~60 | 0 | 0 | 8 event files |
| Tier 2 (Crafted items) | ~57 | 0 | 0 | 6+ event files |
| Tier 3 (Store items) | ~25 | 0 | 6 new events | 5 event files |
| Tier 4 (Secret combos) | 0 | ~20 | 0 | 6 event files |
| Tier 5 (Systemic) | ~30 | 0 | 11 new events | 5 event files |
| Section 11 (Flask narrative) | ~35 | 0 | 11 new events | 7 event files |
| Section 12 (Companion-item) | ~14 | 0 | 0 | 3 event files |
| Section 13 (Adventure gaps) | ~25 | 0 | 0 | adventures.py |
| Section 14 (Pool modifiers) | 0 | 0 | 0 | lists.py / event_dispatch.py |
| **TOTAL** | **~246** | **~20** | **~28** | **~12 files** |

### What This Changes

- **Before:** 42 narrative-inert items (Marvin + flasks). 5 multi-item AND combos. 19 single-file crafted items.
- **After:** 0 narrative-inert items. 25+ multi-item combos. All crafted items in 3+ files. Flasks appear in event narratives. Companions react to player items. Event pools respond to inventory.

---

## 16. Crafting Expansion — Complete Overhaul

### The Problem

The game has **~95 purchasable store items** but only **27 crafting recipes**. Over half the store inventory is never used as a crafting ingredient. Players buy Flashlights, Matches, Sunglasses, Running Shoes, Umbrellas, Dog Whistles — and none of them can be combined into anything. Crafting should feel like a living system where almost anything in your inventory might combine with something else.

### Design Goals

1. **Match crafted items to base items**: Get from 27 recipes to **80+ recipes** so the crafting system feels as deep as the store
2. **Tiered crafting**: Crafted items become ingredients for Tier 2 items. Tier 2 items become ingredients for Tier 3 masterworks. Tier 3 + rare drops = Tier 4 legendaries
3. **Use every store item**: No item should exist only to be pawned. Every purchasable item should be an ingredient in at least one recipe
4. **3-ingredient recipes**: The workbench currently only supports 2-ingredient recipes. Tier 3+ recipes use 3 ingredients (requires workbench code update)
5. **Every crafted item does something in events**: No pawn-fodder crafts. Each new recipe must have at least 2 `has_item()` checks in event files

### Current Ingredient Coverage

**21 out of ~95 store items** are used as crafting ingredients (22%). The remaining 78% are dead-end items.

| Store Item | Used in Crafting? | Recipes |
|-----------|:-:|:-:|
| Duct Tape | **YES** | 5 recipes |
| Fishing Line | **YES** | 5 recipes |
| Garbage Bag | **YES** | 4 recipes |
| Rope | **YES** | 4 recipes |
| Hand Warmers | **YES** | 3 recipes |
| Rubber Bands | **YES** | 3 recipes |
| Plastic Wrap | **YES** | 3 recipes |
| Bungee Cords | **YES** | 2 recipes |
| First Aid Kit | **YES** | 2 recipes |
| Lighter | **YES** | 2 recipes |
| Pocket Knife | **YES** | 2 recipes |
| Road Flares | **YES** | 2 recipes |
| Super Glue | **YES** | 2 recipes |
| Lucky Penny | **YES** | 2 recipes |
| Binoculars | **YES** | 1 recipe |
| Blanket | **YES** | 1 recipe |
| Breath Mints | **YES** | 1 recipe |
| Broken Compass | **YES** | 1 recipe |
| Bug Spray | **YES** | 1 recipe |
| Cough Drops | **YES** | 1 recipe |
| Spare Fuses | **YES** | 1 recipe |
| Flashlight | NO | — |
| Umbrella | NO | — |
| Sunglasses | NO | — |
| Matches | NO | — |
| Baking Soda | NO | — |
| Dog Whistle | NO | — |
| Dog Treat | NO | — |
| Running Shoes | NO | — |
| Disposable Camera | NO | — |
| Air Freshener | NO | — |
| Padlock | NO | — |
| Welding Goggles | NO | — |
| Signal Booster | NO | — |
| LifeAlert | NO | — |
| Deck of Cards | NO | — |
| Pest Control | NO | — |
| Necronomicon | NO | — |
| Birdseed | NO | — |
| Can of Tuna | NO | — |
| Poncho | NO | — |
| Cheap/Premium Sunscreen | NO | — |
| Battery Terminal Cleaner | NO | — |
| Water Bottles | NO | — |
| Fancy Cigars | NO | — |
| Gold Chain | NO | — |
| Leather Gloves | NO | — |
| Silver Flask | NO | — |
| Expensive Cologne | NO | — |
| Vintage Wine | NO | — |
| Silk Handkerchief | NO | — |
| Monogrammed Lighter | NO | — |
| Antique Pocket Watch | NO | — |
| Fancy Pen | NO | — |
| Mysterious Envelope | NO | — |
| Old Photograph | NO | — |
| Spare Tire | NO | — |
| Car Jack | NO | — |
| Jumper Cables | NO | — |
| Motor Oil | NO | — |
| WD-40 | NO | — |
| Tool Kit | NO (unlocks workbench, not consumed) | — |

**Target:** Get every "NO" item into at least one recipe.

---

## 17. New Recipe Category: Gadgets

Tech-flavored items. Built from electronics, optics, and scavenged parts.

### Tier 1 Gadgets (2 ingredients)

| # | Ingredients | Result | Pawn | Description |
|---|-----------|--------|------|-------------|
| 28 | Flashlight + Duct Tape | **Headlamp** | $28 | Hands-free light source. Night events: see threats earlier |
| 29 | Flashlight + Binoculars | **Spotlight** | $55 | Long-range illumination. Adventures: reveal hidden paths |
| 30 | Disposable Camera + Signal Booster | **Evidence Kit** | $45 | Document crimes/events. Dark events: leverage over NPCs |
| 31 | Signal Booster + Spare Fuses | **Radio Jammer** | $40 | Block signals. Wealth events: avoid casino surveillance |
| 32 | Battery Terminal Cleaner + Spare Fuses | **EMP Device** | $50 | Short-circuit electronics. Dark events: disable car alarm to escape, casino security scramble |
| 33 | LifeAlert + Signal Booster | **Distress Beacon** | $90 | Enhanced emergency signal. Survival: guaranteed rescue in any danger |
| 34 | Padlock + Pocket Knife | **Security Bypass** | $35 | Open or lock anything. Adventures: access restricted areas |

### Event Interactions for New Gadgets

| Item | Target Events | File | Effect |
|------|--------------|------|--------|
| **Headlamp** | night walks, cave exploration, car repair at night | events_night.py, adventures.py, events_car.py | See hazards, avoid damage, fix car in dark |
| **Spotlight** | adventure scouting, night creature encounters, lost events | adventures.py, events_night.py, events_day_survival.py | Reveal sub-zone content, blind creatures, signal for rescue |
| **Evidence Kit** | crime witness, robbery, corruption events | events_day_dark.py, events_day_people.py | Photograph crime → sell evidence or report for reward ($200-1000) |
| **Radio Jammer** | casino_knows, reporters_found_you, surveillance | events_day_wealth.py, events_day_casino.py | Block tracking, avoid recognition events |
| **EMP Device** | car alarm false triggers, casino electronics, ATM events | events_day_dark.py, events_day_casino.py, events_car.py | Disable security systems, scramble slot machines, emergency car disable |
| **Distress Beacon** | any lethal event, lost in wilderness, drowning | all survival/death events | Last-resort rescue (consumed), survive any event with 1 HP |
| **Security Bypass** | locked containers, restricted areas, safes | events_day_items.py, adventures.py, events_day_dark.py | Open any locked thing without lockpick skill |

---

## 18. New Recipe Category: Disguises

Social manipulation items. Built from clothing, accessories, and appearance items.

### Tier 1 Disguises (2 ingredients)

| # | Ingredients | Result | Pawn | Description |
|---|-----------|--------|------|-------------|
| 35 | Sunglasses + Poncho | **Low-Profile Outfit** | $20 | Blend with crowds. People events: avoid recognition |
| 36 | Sunglasses + Cheap Sunscreen | **Beach Bum Disguise** | $18 | Look like a tourist. Dark events: muggers ignore tourists |
| 37 | Welding Goggles + Air Freshener | **Gas Mask** | $35 | Breathe through anything. Survival: chemical spills, smoke, gas leaks |
| 38 | Umbrella + Plastic Poncho | **Storm Suit** | $18 | Full weather protection. Survival: immune to all rain/cold penalties |
| 39 | Leather Gloves + Padlock | **Brass Knuckles** | $70 | Hidden weapon. Dark events: win any fistfight |
| 40 | Expensive Cologne + Silk Handkerchief | **Gentleman's Charm** | $200 | Irresistible sophistication. People events: any NPC trusts you |
| 41 | Fancy Pen + Old Photograph | **Forged Documents** | $60 | Fake identity papers. Law events: avoid arrest. Wealth: fake VIP access |

### Event Interactions for Disguises

| Item | Target Events | File | Effect |
|------|--------------|------|--------|
| **Low-Profile Outfit** | casino_knows, reporters, police events | events_day_wealth.py, events_day_dark.py | Nobody recognizes you. Avoid fame-related negative events |
| **Beach Bum Disguise** | mugging, social status checks | events_day_dark.py, events_day_people.py | "Just a tourist." Muggers look for richer targets |
| **Gas Mask** | carbon monoxide, chemical spill, smoke inhalation, swamp gas | events_day_dark.py, events_day_survival.py, adventures.py | Immune to all airborne hazards |
| **Storm Suit** | all rain/cold/storm events | events_day_survival.py, events_night.py | Complete weather immunity. No cold damage, no rain sickness |
| **Brass Knuckles** | fistfight, bar brawl, mugging (fight back) | events_day_dark.py, events_day_people.py, events_night.py | Auto-win physical confrontations. Intimidation bonus |
| **Gentleman's Charm** | elegance checks, business deals, fancy dinner | events_day_people.py, events_day_wealth.py | +$500 on any social event. NPCs give gifts, share secrets |
| **Forged Documents** | police encounters, casino entry, hospital, loan shark | events_day_dark.py, events_day_wealth.py, events_day_casino.py | Fake identity avoids legal trouble. VIP access without earning it |

---

## 19. New Recipe Category: Tonics & Consumables

Single-use or limited-use items. Built from food, medicine, and natural ingredients.

### Tier 1 Tonics (2 ingredients)

| # | Ingredients | Result | Pawn | Description |
|---|-----------|--------|------|-------------|
| 42 | Baking Soda + Water Bottles | **Antacid Brew** | $8 | Cure food poisoning / nausea. Illness: prevent stomach-related events |
| 43 | Matches + Birdseed | **Trail Mix Bomb** | $10 | Distraction device. Dark events: throw to create diversion, escape |
| 44 | Dog Treat + Birdseed | **Animal Bait** | $12 | Attract any animal. Animal events: trigger companion recruitment without Animal Whistle (one-time) |
| 45 | Can of Tuna + Baking Soda | **Stink Bomb** | $8 | Area denial. Dark events: clear a room, force NPCs to flee |
| 46 | Cough Drops + Breath Mints | **Voice Soother** | $10 | Clear throat for persuasion. People events: better negotiation outcomes |
| 47 | Cheap Sunscreen + Bug Spray | **Outdoor Shield** | $15 | Combined protection outdoors. Survival: block sunburn AND mosquitoes |
| 48 | Premium Sunscreen + Water Bottles | **Cool Down Kit** | $18 | Heat protection. Survival: prevent heat stroke, cool off after exertion |
| 49 | Matches + Garbage Bag | **Smoke Flare** | $8 | Visible smoke signal. Survival: attract rescue without road flares |
| 50 | Pest Control + Baking Soda | **Vermin Bomb** | $20 | Nuclear option against pests. Car events: eliminate all car pest problems permanently |

### Event Interactions for Tonics

| Item | Target Events | File | Effect |
|------|--------------|------|--------|
| **Antacid Brew** | food poisoning, illness onset, bad food | events_day_dark.py, events_illness.py, events_day_survival.py | Instant cure for stomach illness. Consumed on use |
| **Trail Mix Bomb** | mugging, chase, trapped scenarios | events_day_dark.py, events_night.py | Throw → distraction → escape. Consumed |
| **Animal Bait** | any animal encounter without Animal Whistle | events_day_animals.py, events_night.py | One-time companion attempt. Consumed |
| **Stink Bomb** | enclosed spaces with hostile NPCs | events_day_dark.py, adventures.py | Force everyone to leave. Area cleared. Consumed |
| **Voice Soother** | negotiation, persuasion, business deals | events_day_people.py, events_day_wealth.py | +25% better negotiation outcome. Consumed |
| **Outdoor Shield** | any outdoor survival event | events_day_survival.py | Block both sunburn AND insect damage. Consumed per day |
| **Cool Down Kit** | heat events, desert zones, overheating | events_day_survival.py, adventures.py | Prevent heat-related illness. Consumed |
| **Smoke Flare** | lost events, stranded, emergency | events_day_survival.py, adventures.py | Attract help. Works like Road Flares but craftable from scraps. Consumed |
| **Vermin Bomb** | all pest events, car infestations | events_car.py, events_day_animals.py | Permanent pest immunity for 5 days. Consumed |

---

## 20. New Recipe Category: Dark Arts

Sinister or morally gray items. Built from dark drops, cursed objects, and forbidden materials.

### Tier 1 Dark Arts (2 ingredients)

| # | Ingredients | Result | Pawn | Description |
|---|-----------|--------|------|-------------|
| 51 | Necronomicon + Matches | **Eldritch Candle** | $100 | Cursed light source. Dark events: dark entities obey you. Sanity cost per use |
| 52 | Necronomicon + Old Photograph | **Binding Portrait** | $80 | Trap a person's likeness. People events: blackmail leverage, NPC obedience |
| 53 | Mysterious Envelope + Fancy Pen | **Blackmail Letter** | $75 | Anonymous threat. Wealth events: extort money from rich NPCs |
| 54 | Deck of Cards + Matches | **Devil's Deck** | $30 | Marked cards. Casino events: cheat at any card game. Risk: caught = punishment |
| 55 | Deck of Cards + Lucky Penny | **Fortune Cards** | $20 | Divination deck. Surreal events: predict next event outcome, choose to avoid it |

### Event Interactions for Dark Arts

| Item | Target Events | File | Effect |
|------|--------------|------|--------|
| **Eldritch Candle** | blood_moon, devil deal, dark creature encounters | events_day_dark.py, events_day_surreal.py, events_night.py | Dark entities recognize you as one of them. Skip dark combat. -5 sanity per use |
| **Binding Portrait** | any NPC encounter | events_day_people.py, events_day_dark.py | Force NPC to do your bidding once. Morally dark. NPC remembers and may seek revenge |
| **Blackmail Letter** | wealthy NPC events, business deals | events_day_wealth.py, events_day_people.py | Extort $500-2000 from an NPC. Risk: 20% chance they call police. Consumed |
| **Devil's Deck** | poker, street dice, card games | events_day_casino.py, adventures.py, events_day_people.py | Auto-win any gambling side event. 15% chance caught → bounced + beaten |
| **Fortune Cards** | any event with branching choices | events_day_surreal.py, events_day_items.py | Peek at outcome before committing. Incredible power. Consumed after 3 readings |

---

## 21. New Recipe Category: Luxury Crafts

High-end items built from expensive Rank 3+ ingredients. Status symbols that unlock wealth-tier reactions.

### Tier 1 Luxury Crafts (2 ingredients)

| # | Ingredients | Result | Pawn | Description |
|---|-----------|--------|------|-------------|
| 56 | Gold Chain + Fancy Cigars | **Kingpin Look** | $350 | Full crime boss aesthetic. Dark events: criminals respect you, leave you alone |
| 57 | Silver Flask + Vintage Wine | **Enchanted Vintage** | $400 | Wine that never runs out. Social events: infinite toasting, NPCs become loyal |
| 58 | Antique Pocket Watch + Fancy Pen | **Heirloom Set** | $500 | Looks inherited. Elegance events: treated as old money, not new money |
| 59 | Leather Gloves + Silk Handkerchief | **Aristocrat's Touch** | $250 | Noble hands. People events: handshake seals any deal, elegance always passes |
| 60 | Monogrammed Lighter + Fancy Cigars | **Power Move Kit** | $300 | The look of authority. Business events: instant intimidation, better deals |
| 61 | Expensive Cologne + Leather Gloves | **Animal Magnetism** | $200 | Irresistible presence. People events: strangers approach you with gifts and offers |
| 62 | Lucky Rabbit Foot + Lucky Penny | **Luck Totem** | $150 | Concentrated luck. Passive: +5% on all random chance rolls (permanent while held) |

### Event Interactions for Luxury Crafts

| Item | Target Events | File | Effect |
|------|--------------|------|--------|
| **Kingpin Look** | mugging, drug events, dark alley, underground | events_day_dark.py, adventures.py | Criminals won't touch you. Underground NPCs respect you. Access to hidden events |
| **Enchanted Vintage** | all social/dining events | events_day_people.py, events_day_wealth.py | Never run out of wine. Every social event becomes positive. +sanity at social gatherings |
| **Heirloom Set** | elegance checks, VIP events, business | events_day_people.py, events_day_wealth.py | Always pass elegance checks. "Old money" reactions — better than Gold Chain alone |
| **Aristocrat's Touch** | handshake events, deals, formal | events_day_people.py | Auto-win any negotiation. Social dominance |
| **Power Move Kit** | business meetings, intimidation | events_day_people.py, events_day_wealth.py | Intimidation + elegance. Dual-purpose social weapon |
| **Animal Magnetism** | stranger encounters, social events | events_day_people.py, events_night.py | Random NPCs give you things. Friendship bonus. Strangers share secrets |
| **Luck Totem** | ALL random events | all event files | Passive luck bonus. Not consumed. Tweaks RNG in player's favor |

---

## 22. New Recipe Category: Vehicle Upgrades

Car improvement items. Built from car parts and tools. Reduce car trouble frequency.

### Tier 1 Vehicle Upgrades (2 ingredients)

| # | Ingredients | Result | Pawn | Description |
|---|-----------|--------|------|-------------|
| 63 | Spare Tire + Car Jack | **Tire Ready Kit** | $60 | Pre-assembled tire change. Car events: instant tire fix, no damage |
| 64 | Jumper Cables + Spare Fuses | **Power Grid** | $40 | Electrical system backup. Car events: prevent all electrical failures |
| 65 | Motor Oil + WD-40 | **Miracle Lube** | $35 | Universal lubricant. Car events: prevent engine seizure, squeaks, rust |
| 66 | Tool Kit + Duct Tape | **Mobile Workshop** | $60 | Portable repair station. Car events: fix any car problem on the spot |
| 67 | Dog Whistle + Running Shoes | **Pursuit Package** | $40 | Chase deterrent. Dark events: outrun anyone + call dog distraction |

### Event Interactions for Vehicle Upgrades

| Item | Target Events | File | Effect |
|------|--------------|------|--------|
| **Tire Ready Kit** | all tire blowout events | events_car.py, events_day_survival.py | Instant fix, no pulling over, no damage. Not consumed (reusable) |
| **Power Grid** | dead battery, electrical failure, fuse events | events_car.py | Skip all electrical car trouble. Permanent prevention while held |
| **Miracle Lube** | engine events, rust, squeaks, oil leaks | events_car.py | Universal car fluid fix. Consumed per use but covers any fluid problem |
| **Mobile Workshop** | any car breakdown | events_car.py | Fix ANY car problem regardless of what's wrong. Reusable but loses 1 durability per fix |
| **Pursuit Package** | car chase events, being followed, escape | events_day_dark.py, events_night.py | Combined speed (shoes) + distraction (whistle). Auto-escape vehicle pursuits |

---

## 23. Tier 2 Crafting — Crafted + Crafted Recipes

**The big innovation.** Crafted items can combine with other crafted items OR with base items to create Tier 2 items. These are meaningfully more powerful.

### Tier 2 Weapons (Crafted + Crafted/Base)

| # | Ingredients | Result | Pawn | Description |
|---|-----------|--------|------|-------------|
| 68 | Shiv + Pepper Spray | **Assassin's Kit** | $80 | Close + ranged combat. Dark events: auto-win any violence. Never take damage in fights |
| 69 | Slingshot + Road Flare Torch | **Fire Launcher** | $75 | Ranged incendiary. Night events: clear an entire area of threats. Adventures: boss damage bonus |
| 70 | Pepper Spray + Stink Bomb | **Tear Gas** | $50 | Room-clearing chemical weapon. Dark events: incapacitate all hostiles in enclosed space |
| 71 | Shiv + Brass Knuckles | **Street Fighter Set** | $100 | Full melee arsenal. Dark events: reputation as dangerous → most violence events skip entirely |

### Tier 2 Survival (Crafted + Crafted/Base)

| # | Ingredients | Result | Pawn | Description |
|---|-----------|--------|------|-------------|
| 72 | Emergency Blanket + Fire Starter Kit | **Survival Bivouac** | $40 | Complete shelter. Night: immune to cold/exposure. Survival: skip all weather events |
| 73 | Water Purifier + Rain Collector | **Hydration Station** | $35 | Clean water forever. Illness: can't get waterborne disease. Survival: ignore thirst mechanics |
| 74 | Snare Trap + Fishing Rod | **Provider's Kit** | $50 | Food independence. Survival: any food-shortage event gives food instead |
| 75 | Improvised Trap + Car Alarm Rigging | **Fortified Perimeter** | $55 | Multi-layer defense. Night: no theft, no intrusion, no surprise attacks while sleeping |
| 76 | Storm Suit + Outdoor Shield | **All-Weather Armor** | $45 | Immune to ALL environmental damage — heat, cold, rain, sun, insects, chemicals |

### Tier 2 Tools (Crafted + Crafted/Base)

| # | Ingredients | Result | Pawn | Description |
|---|-----------|--------|------|-------------|
| 77 | Lockpick Set + Security Bypass | **Master Key** | $80 | Open literally anything. Adventures: access hidden room in every zone |
| 78 | Binocular Scope + Headlamp | **Night Scope** | $65 | See everything in darkness. Night events: no surprise, full awareness |
| 79 | Signal Mirror + Smoke Flare | **SOS Kit** | $30 | Ultimate rescue signal. Any peril: guaranteed rescue even in remote areas |
| 80 | Evidence Kit + Forged Documents | **Intelligence Dossier** | $100 | Leverage on everyone. People events: know NPC secrets. casino events: know house edge |
| 81 | Spotlight + Radio Jammer | **Surveillance Suite** | $90 | Counter-intelligence. Wealth events: block ALL surveillance, tracking, recognition |

### Tier 2 Charms (Crafted + Crafted/Base)

| # | Ingredients | Result | Pawn | Description |
|---|-----------|--------|------|-------------|
| 82 | Dream Catcher + Worry Stone | **Mind Shield** | $30 | Complete mental defense. All sanity loss reduced by 50%. Nightmares impossible |
| 83 | Lucky Charm Bracelet + Luck Totem | **Fortune's Favor** | $200 | Stacked luck. Passive: +10% all random chances. Casino side events always win |
| 84 | Lucky Charm Bracelet + Fortune Cards | **Fate Reader** | $50 | Foresight + luck. Surreal events: always choose the right path. Consumed after 5 readings |
| 85 | Dream Catcher + Eldritch Candle | **Lucid Dreaming Kit** | $80 | Control dreams. Mechanic dreams: choose dream content. Night: always positive sleep |

### Tier 2 Social (Crafted + Crafted/Base)

| # | Ingredients | Result | Pawn | Description |
|---|-----------|--------|------|-------------|
| 86 | Gentleman's Charm + Heirloom Set | **Old Money Identity** | $500 | Perfect disguise as wealthy aristocrat. All wealth-tier events treat you as billionaire |
| 87 | Low-Profile Outfit + Forged Documents | **New Identity** | $100 | Complete alias. Police: can't be found. Casino: fresh start. Reporters: wrong name |
| 88 | Animal Bait + Pet Toy | **Beast Tamer Kit** | $30 | Advanced animal handling. Animal events: always befriend, never attacked by creatures |
| 89 | Devil's Deck + Evidence Kit | **Cheater's Insurance** | $60 | Cheat AND have evidence others cheat too. Casino: cheat without risk of getting caught |

### Tier 2 Vehicle (Crafted + Crafted/Base)

| # | Ingredients | Result | Pawn | Description |
|---|-----------|--------|------|-------------|
| 90 | Tire Ready Kit + Power Grid | **Roadside Shield** | $100 | Combined tire + electrical fix. Car: prevent 60% of all car troubles |
| 91 | Mobile Workshop + Miracle Lube | **Auto Mechanic** | $120 | Fix + prevent. Car troubles reduced by 80%. Any car problem fixed instantly |
| 92 | Pursuit Package + Fortified Perimeter | **Rolling Fortress** | $110 | Mobile defense. Car: immune to car theft. Chase: auto-escape. Night: car is impregnable |

---

## 24. Tier 3 Crafting — Triple-Ingredient Masterworks

These require updating the workbench to accept 3 ingredients. Each is a major game-changer.

**Workbench code change:** In `make_crafting_recipes()`, add support for `"ingredients": ["A", "B", "C"]` with 3 entries. The `get_available_recipes()` filter and `workbench_craft()` ingredient removal loop must iterate `len(recipe["ingredients"])` instead of hardcoded 2.

### Tier 3 Masterworks

| # | Ingredients (3) | Result | Pawn | Description |
|---|----------------|--------|------|-------------|
| 93 | Assassin's Kit + Scrap Armor + Street Fighter Set | **Road Warrior Armor** | $300 | Full combat loadout. All physical damage reduced to 0. Dark events auto-resolve in your favor |
| 94 | Mind Shield + Lucid Dreaming Kit + Fortune Cards | **Third Eye** | $200 | Total awareness. See all event outcomes before choosing. Dreams are fully controlled. Sanity can't drop below 50 |
| 95 | Survival Bivouac + Provider's Kit + Hydration Station | **Nomad's Camp** | $150 | Self-sufficient living. No survival event can harm you. Food/water/shelter always covered |
| 96 | Master Key + Night Scope + Intelligence Dossier | **All-Access Pass** | $350 | Know everything, go everywhere. Every locked path opens. Every NPC secret revealed. Adventures: always find hidden rooms |
| 97 | Old Money Identity + Cheater's Insurance + Enchanted Vintage | **Master of Games** | $800 | Social + gambling perfection. All casino events favor you. All social events succeed. Elegance always passes |
| 98 | Auto Mechanic + Rolling Fortress + Roadside Shield | **Immortal Vehicle** | $500 | Car never breaks down. Car never stolen. Car repairs itself overnight. Car trouble events stop appearing |
| 99 | Fortune's Favor + Luck Totem + Smelling Salts | **Gambler's Aura** | $400 | Luck is your constant companion. +15% all random chances. Blackjack and side games always lean your way |
| 100 | Beast Tamer Kit + Animal Bait + Feeding Station | **Ark Master's Horn** | $250 | Command all animals. Companions never leave, never die, max happiness always. All animal events are positive |
| 101 | SOS Kit + Distress Beacon + Fortified Perimeter | **Guardian Angel** | $300 | Cannot die from events. Any lethal damage becomes non-lethal. Rescue always arrives. One-time self-revive if HP hits 0 |
| 102 | Gas Mask + All-Weather Armor + Storm Suit | **Hazmat Suit** | $150 | Immune to ALL environmental, chemical, weather, and gas damage |
| 103 | Surveillance Suite + New Identity + Radio Jammer | **Ghost Protocol** | $400 | Invisible to all tracking. Casino doesn't know you. Police can't find you. Reporters don't exist. You are nobody |
| 104 | Eldritch Candle + Binding Portrait + Devil's Deck | **Dark Pact Reliquary** | $200 | Master of dark powers. Devil deals always favor you. Dark entities serve you. Massive sanity cost (-3/day) |

---

## 25. Tier 4 Crafting — Legendary Items

Require one Tier 3 masterwork + one rare event-drop item. These are endgame rewards for players who've explored deeply.

### Legendary Items

| # | Ingredients | Result | Effect |
|---|-----------|--------|--------|
| 105 | Road Warrior Armor + Gator Tooth Necklace | **Beastslayer Mantle** | Immune to all violence + all animal attacks. Physical invincibility |
| 106 | Third Eye + Hermit's Journal | **Seer's Chronicle** | Know every future event for 10 days. Perfect foresight |
| 107 | Nomad's Camp + Carved Walking Stick | **Wanderer's Rest** | Fully self-sufficient + nature heals you. +10 HP/day passive |
| 108 | All-Access Pass + Night Vision Scope | **Skeleton Key** | Unlock any door, any lock, any secret in the game. Access all hidden content |
| 109 | Master of Games + Junkyard Crown | **King of the Road** | Every NPC defers to you. Every game favors you. +$1000/day passive income |
| 110 | Immortal Vehicle + Artisan's Toolkit | **War Wagon** | Car is a mobile fortress with self-repair, storage, and combat capability |
| 111 | Gambler's Aura + Moon Shard | **Moonlit Fortune** | Luck itself bends to your will. Permanent +20% blackjack advantage |
| 112 | Ark Master's Horn + Kraken Pearl | **Leviathan's Call** | Command sea and land creatures. Companion army. All creature events are recruitment |
| 113 | Guardian Angel + Phoenix Feather (Marvin) | **Last Breath Locket** | True immortality. Cannot die. Period. HP cannot reach 0 |
| 114 | Ghost Protocol + Scrap Metal Rose | **Phantom Rose** | You are a legend no one can find. +$500/day from mysterious admirers. Zero negative recognition |
| 115 | Dark Pact Reliquary + Ritual Token | **Soul Forge** | Rewrite any past event outcome. One use — choose any event from your history to change its result |

---

## 26. Crafting Tree Visualization

Shows how items flow from store purchases through crafting tiers.

### Tier 0 → Tier 1 (Base → Crafted)

```
STORE ITEMS (95+)
├── Weapons: Duct Tape, Pocket Knife, Rubber Bands, Bungee Cords, Bug Spray, Lighter, Road Flares
├── Traps: Fishing Line, Pocket Knife, Bungee Cords, Spare Fuses, Rope
├── Remedies: First Aid Kit, Cough Drops, Super Glue, Duct Tape, Hand Warmers, Breath Mints, Rope
├── Tools: Pocket Knife, Fishing Line, Rope, Binoculars, Broken Compass, Super Glue, Duct Tape
├── Charms: Lucky Penny, Fishing Line, Rubber Bands, Hand Warmers
├── Survival: Plastic Wrap, Garbage Bag, Duct Tape, Road Flares, Lighter, Hand Warmers
├── Companion: Blanket, Duct Tape, Rope, Rubber Bands, Plastic Wrap
├── [NEW] Gadgets: Flashlight, Signal Booster, Spare Fuses, Battery Terminal Cleaner, Padlock, LifeAlert, Disposable Camera, Binoculars
├── [NEW] Disguises: Sunglasses, Poncho, Cheap Sunscreen, Welding Goggles, Air Freshener, Umbrella, Leather Gloves, Padlock, Expensive Cologne, Silk Handkerchief, Fancy Pen, Old Photograph, Plastic Poncho
├── [NEW] Tonics: Baking Soda, Water Bottles, Matches, Birdseed, Dog Treat, Can of Tuna, Cough Drops, Bug Spray, Pest Control, Cheap Sunscreen, Premium Sunscreen, Breath Mints
├── [NEW] Dark Arts: Necronomicon, Mysterious Envelope, Deck of Cards, Lucky Penny, Old Photograph, Fancy Pen, Matches
├── [NEW] Luxury: Gold Chain, Fancy Cigars, Silver Flask, Vintage Wine, Antique Pocket Watch, Fancy Pen, Leather Gloves, Silk Handkerchief, Monogrammed Lighter, Expensive Cologne, Lucky Rabbit Foot
└── [NEW] Vehicle: Spare Tire, Car Jack, Jumper Cables, Motor Oil, WD-40, Tool Kit, Duct Tape, Dog Whistle, Running Shoes
```

### Tier 1 → Tier 2 (Crafted + Crafted)

```
TIER 1 CRAFTED (67 items)
├── Assassin's Kit ← Shiv + Pepper Spray
├── Fire Launcher ← Slingshot + Road Flare Torch
├── Tear Gas ← Pepper Spray + Stink Bomb
├── Street Fighter Set ← Shiv + Brass Knuckles
├── Survival Bivouac ← Emergency Blanket + Fire Starter Kit
├── Hydration Station ← Water Purifier + Rain Collector
├── Provider's Kit ← Snare Trap + Fishing Rod
├── Fortified Perimeter ← Improvised Trap + Car Alarm Rigging
├── All-Weather Armor ← Storm Suit + Outdoor Shield
├── Master Key ← Lockpick Set + Security Bypass
├── Night Scope ← Binocular Scope + Headlamp
├── SOS Kit ← Signal Mirror + Smoke Flare
├── Intelligence Dossier ← Evidence Kit + Forged Documents
├── Surveillance Suite ← Spotlight + Radio Jammer
├── Mind Shield ← Dream Catcher + Worry Stone
├── Fortune's Favor ← Lucky Charm Bracelet + Luck Totem
├── Fate Reader ← Lucky Charm Bracelet + Fortune Cards
├── Lucid Dreaming Kit ← Dream Catcher + Eldritch Candle
├── Old Money Identity ← Gentleman's Charm + Heirloom Set
├── New Identity ← Low-Profile Outfit + Forged Documents
├── Beast Tamer Kit ← Animal Bait + Pet Toy
├── Cheater's Insurance ← Devil's Deck + Evidence Kit
├── Roadside Shield ← Tire Ready Kit + Power Grid
├── Auto Mechanic ← Mobile Workshop + Miracle Lube
└── Rolling Fortress ← Pursuit Package + Fortified Perimeter
```

### Tier 2 → Tier 3 (3 Ingredients)

```
TIER 2 CRAFTED (25 items)
├── Road Warrior Armor ← Assassin's Kit + Scrap Armor + Street Fighter Set
├── Third Eye ← Mind Shield + Lucid Dreaming Kit + Fortune Cards
├── Nomad's Camp ← Survival Bivouac + Provider's Kit + Hydration Station
├── All-Access Pass ← Master Key + Night Scope + Intelligence Dossier
├── Master of Games ← Old Money Identity + Cheater's Insurance + Enchanted Vintage
├── Immortal Vehicle ← Auto Mechanic + Rolling Fortress + Roadside Shield
├── Gambler's Aura ← Fortune's Favor + Luck Totem + Smelling Salts
├── Ark Master's Horn ← Beast Tamer Kit + Animal Bait + Feeding Station
├── Guardian Angel ← SOS Kit + Distress Beacon + Fortified Perimeter
├── Hazmat Suit ← Gas Mask + All-Weather Armor + Storm Suit
├── Ghost Protocol ← Surveillance Suite + New Identity + Radio Jammer
└── Dark Pact Reliquary ← Eldritch Candle + Binding Portrait + Devil's Deck
```

### Tier 3 → Tier 4 (Masterwork + Rare Event Drop)

```
TIER 3 MASTERWORKS (12 items)
├── Beastslayer Mantle ← Road Warrior Armor + Gator Tooth Necklace
├── Seer's Chronicle ← Third Eye + Hermit's Journal
├── Wanderer's Rest ← Nomad's Camp + Carved Walking Stick
├── Skeleton Key ← All-Access Pass + Night Vision Scope
├── King of the Road ← Master of Games + Junkyard Crown
├── War Wagon ← Immortal Vehicle + Artisan's Toolkit
├── Moonlit Fortune ← Gambler's Aura + Moon Shard
├── Leviathan's Call ← Ark Master's Horn + Kraken Pearl
├── Last Breath Locket ← Guardian Angel + Phoenix Feather
├── Phantom Rose ← Ghost Protocol + Scrap Metal Rose
└── Soul Forge ← Dark Pact Reliquary + Ritual Token
```

---

## 27. New Ingredient Usage Map

Every store item and where it's now used as a crafting ingredient.

### Previously Unused Items — Now Active

| Item | Old Use | New Recipe(s) | Category |
|------|---------|--------------|----------|
| Flashlight | 0 recipes | Headlamp, Spotlight | Gadget |
| Disposable Camera | 0 recipes | Evidence Kit | Gadget |
| Signal Booster | 0 recipes | Radio Jammer, Distress Beacon | Gadget |
| Battery Terminal Cleaner | 0 recipes | EMP Device | Gadget |
| LifeAlert | 0 recipes | Distress Beacon | Gadget |
| Padlock | 0 recipes | Security Bypass, Brass Knuckles | Gadget/Disguise |
| Sunglasses | 0 recipes | Low-Profile Outfit, Beach Bum Disguise | Disguise |
| Poncho | 0 recipes | Low-Profile Outfit | Disguise |
| Cheap Sunscreen | 0 recipes | Beach Bum Disguise, Outdoor Shield | Disguise/Tonic |
| Premium Sunscreen | 0 recipes | Cool Down Kit | Tonic |
| Welding Goggles | 0 recipes | Gas Mask | Disguise |
| Air Freshener | 0 recipes | Gas Mask | Disguise |
| Umbrella | 0 recipes | Storm Suit | Disguise |
| Plastic Poncho | 0 recipes | Storm Suit | Disguise |
| Leather Gloves | 0 recipes | Brass Knuckles, Aristocrat's Touch, Animal Magnetism | Disguise/Luxury |
| Expensive Cologne | 0 recipes | Gentleman's Charm, Animal Magnetism | Luxury |
| Silk Handkerchief | 0 recipes | Gentleman's Charm, Aristocrat's Touch | Luxury |
| Fancy Pen | 0 recipes | Forged Documents, Blackmail Letter, Heirloom Set | Dark/Luxury |
| Old Photograph | 0 recipes | Forged Documents, Binding Portrait | Disguise/Dark |
| Baking Soda | 0 recipes | Antacid Brew, Stink Bomb, Vermin Bomb | Tonic |
| Water Bottles | 0 recipes | Antacid Brew, Cool Down Kit | Tonic |
| Matches | 0 recipes | Trail Mix Bomb, Smoke Flare, Eldritch Candle, Devil's Deck | Tonic/Dark |
| Birdseed | 0 recipes | Trail Mix Bomb, Animal Bait | Tonic |
| Dog Treat | 0 recipes | Animal Bait | Tonic |
| Can of Tuna | 0 recipes | Stink Bomb | Tonic |
| Pest Control | 0 recipes | Vermin Bomb | Tonic |
| Necronomicon | 0 recipes | Eldritch Candle, Binding Portrait | Dark |
| Mysterious Envelope | 0 recipes | Blackmail Letter | Dark |
| Deck of Cards | 0 recipes | Devil's Deck, Fortune Cards | Dark |
| Gold Chain | 0 recipes | Kingpin Look | Luxury |
| Fancy Cigars | 0 recipes | Kingpin Look, Power Move Kit | Luxury |
| Silver Flask | 0 recipes | Enchanted Vintage | Luxury |
| Vintage Wine | 0 recipes | Enchanted Vintage | Luxury |
| Antique Pocket Watch | 0 recipes | Heirloom Set | Luxury |
| Monogrammed Lighter | 0 recipes | Power Move Kit | Luxury |
| Lucky Rabbit Foot | 0 recipes | Luck Totem | Luxury |
| Running Shoes | 0 recipes | Pursuit Package | Vehicle |
| Dog Whistle | 0 recipes | Pursuit Package | Vehicle |
| Spare Tire | 0 recipes | Tire Ready Kit | Vehicle |
| Car Jack | 0 recipes | Tire Ready Kit | Vehicle |
| Jumper Cables | 0 recipes | Power Grid | Vehicle |
| Motor Oil | 0 recipes | Miracle Lube | Vehicle |
| WD-40 | 0 recipes | Miracle Lube | Vehicle |

**Result: 43 previously unused items now participate in crafting.**

### Updated Ingredient Coverage

| Metric | Before | After |
|--------|--------|-------|
| Store items used as ingredients | 21 / 95 (22%) | **64 / 95 (67%)** |
| Total Tier 1 recipes | 27 | **67** |
| Total Tier 2 recipes | 0 | **25** |
| Total Tier 3 recipes | 0 | **12** |
| Total Tier 4 recipes | 0 | **11** |
| **Total recipes** | **27** | **115** |
| Crafted items usable as ingredients | 0 | **~50** |

---

## 28. Crafting Event Interactions — What Each New Item Does

Every new crafted item needs at least 2 event file interactions. Here's the complete interaction matrix.

### Tier 1 New Items — Event Presence

| Crafted Item | events_day_dark | events_day_people | events_day_survival | events_night | adventures | events_car | events_day_wealth | events_day_casino | events_illness | events_day_surreal | events_day_animals |
|-------------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| Headlamp | | | ✓ | ✓ | ✓ | ✓ | | | | | |
| Spotlight | | | ✓ | ✓ | ✓ | | | | | | |
| Evidence Kit | ✓ | ✓ | | | | | ✓ | | | | |
| Radio Jammer | | | | | | | ✓ | ✓ | | | |
| EMP Device | ✓ | | | | | ✓ | | ✓ | | | |
| Distress Beacon | ✓ | | ✓ | ✓ | ✓ | | | | | | |
| Security Bypass | ✓ | | | | ✓ | | | | | | |
| Low-Profile Outfit | ✓ | | | | | | ✓ | | | | |
| Beach Bum Disguise | ✓ | ✓ | | | | | | | | | |
| Gas Mask | ✓ | | ✓ | | ✓ | | | | | | |
| Storm Suit | | | ✓ | ✓ | | | | | | | |
| Brass Knuckles | ✓ | ✓ | | ✓ | | | | | | | |
| Gentleman's Charm | | ✓ | | | | | ✓ | | | | |
| Forged Documents | ✓ | | | | | | ✓ | ✓ | | | |
| Antacid Brew | ✓ | | ✓ | | | | | | ✓ | | |
| Trail Mix Bomb | ✓ | | | ✓ | | | | | | | |
| Animal Bait | | | | ✓ | | | | | | | ✓ |
| Stink Bomb | ✓ | | | | ✓ | | | | | | |
| Voice Soother | | ✓ | | | | | ✓ | | | | |
| Outdoor Shield | | | ✓ | | ✓ | | | | | | |
| Cool Down Kit | | | ✓ | | ✓ | | | | | | |
| Smoke Flare | | | ✓ | | ✓ | | | | | | |
| Vermin Bomb | | | | | | ✓ | | | | | ✓ |
| Eldritch Candle | ✓ | | | ✓ | | | | | | ✓ | |
| Binding Portrait | ✓ | ✓ | | | | | | | | | |
| Blackmail Letter | | | | | | | ✓ | | | | |
| Devil's Deck | | ✓ | | | ✓ | | | ✓ | | | |
| Fortune Cards | | | | | | | | | | ✓ | |
| Kingpin Look | ✓ | | | | ✓ | | | | | | |
| Enchanted Vintage | | ✓ | | | | | ✓ | | | | |
| Heirloom Set | | ✓ | | | | | ✓ | | | | |
| Aristocrat's Touch | | ✓ | | | | | | | | | |
| Power Move Kit | | ✓ | | | | | ✓ | | | | |
| Animal Magnetism | | ✓ | | ✓ | | | | | | | |
| Luck Totem | all files (passive) | | | | | | | | | | |
| Tire Ready Kit | | | | | | ✓ | | | | | |
| Power Grid | | | | | | ✓ | | | | | |
| Miracle Lube | | | | | | ✓ | | | | | |
| Mobile Workshop | | | | | | ✓ | | | | | |
| Pursuit Package | ✓ | | | ✓ | | | | | | | |

### Tier 2 Items — Event Presence (inherited + enhanced)

Tier 2 items inherit the event presence of both parents PLUS gain unique interactions:

| Crafted Item | Unique New Interaction | Files |
|-------------|----------------------|-------|
| Assassin's Kit | Auto-win ALL combat. Intimidation aura scares NPCs | all violence events |
| Fire Launcher | Clear creature dens. Boss bonus damage | adventures.py, events_night.py |
| Tear Gas | Mass incapacitation. Area denial | events_day_dark.py |
| Street Fighter Set | Reputation as dangerous. Violence events auto-skip | events_day_dark.py |
| Survival Bivouac | Weather immunity + warmth | events_day_survival.py, events_night.py |
| Hydration Station | Waterborne disease immunity | events_illness.py |
| Provider's Kit | Food shortage → food surplus | events_day_survival.py |
| Fortified Perimeter | Zero theft/intrusion at night | events_night.py |
| All-Weather Armor | ALL environmental immunity | events_day_survival.py |
| Master Key | Hidden room access in all zones | adventures.py |
| Night Scope | Full night awareness. No surprises | events_night.py |
| SOS Kit | Global rescue availability | all survival events |
| Intelligence Dossier | NPC secrets revealed | events_day_people.py |
| Surveillance Suite | ALL tracking blocked | events_day_wealth.py |
| Mind Shield | 50% sanity loss reduction | all events |
| Fortune's Favor | +10% luck passive | all random events |
| Fate Reader | Foresight on choices | events_day_surreal.py |
| Lucid Dreaming Kit | Dream control | mechanics_intro.py, events_night.py |
| Old Money Identity | Billionaire treatment | events_day_wealth.py |
| New Identity | Police/casino/reporter immunity | events_day_dark.py, events_day_wealth.py |
| Beast Tamer Kit | Always befriend animals | events_day_animals.py |
| Cheater's Insurance | Cheat at gambling risk-free | events_day_casino.py |
| Roadside Shield | 60% car trouble prevention | events_car.py |
| Auto Mechanic | 80% car trouble prevention + instant fix | events_car.py |
| Rolling Fortress | Car theft immunity + chase escape | events_day_dark.py, events_night.py |

---

## 29. Milestone & Achievement Updates

The workbench currently has milestones at 1, 5, 10, 15, and 27 (all). With 115 recipes, new milestones are needed.

### Proposed Milestones

| Count | Message | Reward |
|-------|---------|--------|
| 1 | "First craft! You're handy with a tool kit. Who knew?" | (existing) |
| 5 | "Five crafted items. You're basically a blacksmith now..." | (existing) |
| 10 | "Ten crafted items! Your car looks like a mad scientist's laboratory." | (existing) |
| 15 | "Fifteen items. You could teach a survival course." | (existing) |
| 20 | "Twenty items. The workbench groans under the weight of your ambition." | Unlock Tier 2 recipe hints |
| 25 | "Twenty-five. You've crafted more than most people own." | +sanity |
| 30 | "Thirty! Your car is a mobile workshop, pharmacy, and armory combined." | Achievement: Craftsman |
| 40 | "Forty items... When did you become an engineer?" | Achievement: Master Craftsman |
| 50 | "Fifty. Half the things in your car didn't exist yesterday." | Achievement: Inventor |
| 67 | "Every Tier 1 recipe mastered. The workbench hums with potential." | Unlock T2 recipe book. Achievement: Journeyman |
| 80 | "Eighty items. Your car is worth more than the casino." | +$5000 bonus |
| 92 | "Every Tier 2 recipe complete. You see combinations in everything." | Unlock T3 recipe book. Achievement: Expert |
| 100 | "One hundred crafted items. You started with nothing. Look at you now." | Achievement: Centurion. +sanity, +health |
| 104 | "Every Tier 3 masterwork forged. You've bent the world to your will." | Unlock T4 recipe book. Achievement: Artificer |
| 115 | "Every recipe. Every combination. Every possibility exhausted." | Achievement: **Grand Artificer**. Unique ending hint |

### Tier Gating

Recipes should unlock progressively:

| Tier | Unlock Condition | Recipes Available |
|------|-----------------|-------------------|
| Tier 1 | Own Tool Kit | 67 base recipes |
| Tier 2 | Craft 20+ Tier 1 items | 25 combination recipes |
| Tier 3 | Craft ALL Tier 1 items (67) + Craft 15+ Tier 2 items | 12 masterwork recipes |
| Tier 4 | Craft ALL Tier 1-3 items (104) + own the rare event drop ingredient | 11 legendary recipes |

This creates a satisfying progression: early game you're making shivs and traps. Mid-game you're combining crafted items. Late-game you're forging masterworks. Endgame you're creating legendary items from adventure drops.

---

## 30. Full Recipe Count Summary

### By Category

| Category | Tier 1 | Tier 2 | Tier 3 | Tier 4 | Total |
|----------|:---:|:---:|:---:|:---:|:---:|
| Weapons | 4 | 4 | — | — | **8** |
| Traps | 3 | — | — | — | **3** |
| Remedies | 4 | — | — | — | **4** |
| Tools | 4 | 5 | — | — | **9** |
| Charms | 3 | 4 | — | — | **7** |
| Survival | 5 | 5 | — | — | **10** |
| Companion | 3 | 1 | — | — | **4** |
| Gadgets (NEW) | 7 | — | — | — | **7** |
| Disguises (NEW) | 7 | — | — | — | **7** |
| Tonics (NEW) | 9 | — | — | — | **9** |
| Dark Arts (NEW) | 5 | — | — | — | **5** |
| Luxury (NEW) | 7 | — | — | — | **7** |
| Vehicle (NEW) | 5 | 3 | — | — | **8** |
| Social (NEW) | — | 4 | — | — | **4** |
| Combat (Tier 2) | — | — | 1 | 1 | **2** |
| Awareness (Tier 3) | — | — | 1 | 1 | **2** |
| Independence (Tier 3) | — | — | 1 | 1 | **2** |
| Access (Tier 3) | — | — | 1 | 1 | **2** |
| Mastery (Tier 3) | — | — | 1 | 1 | **2** |
| Vehicle (Tier 3) | — | — | 1 | 1 | **2** |
| Luck (Tier 3) | — | — | 1 | 1 | **2** |
| Animals (Tier 3) | — | — | 1 | 1 | **2** |
| Protection (Tier 3) | — | — | 1 | 1 | **2** |
| Environment (Tier 3) | — | — | 1 | — | **1** |
| Stealth (Tier 3) | — | — | 1 | 1 | **2** |
| Dark (Tier 3) | — | — | 1 | 1 | **2** |
| **TOTALS** | **67** | **25** | **12** | **11** | **115** |

### By Tier

| Tier | Recipes | Ingredients Per | Total Ingredients Consumed |
|------|---------|:---:|:---:|
| Tier 1 | 67 | 2 each | 134 base items |
| Tier 2 | 25 | 2 each (1-2 crafted) | 50 items (mix of base + crafted) |
| Tier 3 | 12 | 3 each (all crafted) | 36 crafted items |
| Tier 4 | 11 | 2 each (1 masterwork + 1 event drop) | 22 items |
| **TOTAL** | **115** | — | **242 ingredient slots** |

### The Complete Item Economy After Expansion

| Category | Count |
|----------|:---:|
| Purchasable store items | ~95 |
| Marvin items + upgrades | ~37 |
| Flasks | 12 |
| Tier 1 crafted items | 67 |
| Tier 2 crafted items | 25 |
| Tier 3 masterworks | 12 |
| Tier 4 legendaries | 11 |
| Event-drop / quest items | ~50 |
| **Total unique items** | **~309** |

### What This Changes for the Player

- **Before:** 27 recipes using 21 ingredients. Crafting is a side activity you do once and forget. Most store items are pawn fodder.
- **After:** 115 recipes using 64+ ingredients across 4 tiers. Crafting is a core progression system. Every store purchase opens new possibilities. Late-game legendaries reward exploration. The workbench is the most important location in the game after the blackjack table.

### Required Code Changes

| File | Change | Effort |
|------|--------|--------|
| lists.py `make_crafting_recipes()` | Add 88 new recipe entries to dict | Large — but mechanical (copy pattern) |
| locations.py `visit_workbench()` | Support 3-ingredient recipes (loop over `len(ingredients)`) | Small — change hardcoded 2 to dynamic |
| locations.py `get_available_recipes()` | Filter by tier unlock conditions | Medium — add tier gating logic |
| locations.py milestone code | Add new milestones at 20, 25, 30, 40, 50, 67, 80, 92, 100, 104, 115 | Small — add elif branches |
| locations.py `workbench_browse()` | Add Tier 2/3/4 category tabs | Medium — new category display |
| All event files | Add ~200+ new has_item checks for new crafted items | Large — but each is a simple if-block |
| systems.py | Tier gating logic: track player's craft tier | Small — new counter method |

### Implementation Order

1. **Add all 88 new Tier 1 recipes to lists.py** — mechanical, low risk
2. **Update workbench for 3-ingredient support** — small code change
3. **Add Tier 2 recipes to lists.py** — depends on Tier 1
4. **Add milestone updates** — small
5. **Add Tier 3 + Tier 4 recipes** — depends on Tier 2
6. **Add tier gating logic** — medium
7. **Add event interactions** — largest piece, can be done incrementally

---

## 31. Item Trigger Display Standard

### The Rule

Every time an item **triggers** in an event (i.e. changes the outcome because the player has it), the item name is displayed in `cyan(bright("ItemName"))`. This is **never hidden** — the player always knows what item saved/helped them.

### Display Format Reference

| Context | Format | Example |
|---------|--------|---------|
| **Event trigger** (item changes outcome) | `cyan(bright("ItemName"))` | `"Your " + cyan(bright("Pepper Spray")) + " sends him reeling!"` |
| **Shop acquisition** | `bright(magenta("You got a X!"))` | `bright(magenta("You got a Headlamp!"))` |
| **Pawn shop listing** | `cyan(bright(item))` + `green(price)` | `cyan(bright("Headlamp")) + " — " + green("$28")` |
| **Workbench craft success** | `bright(cyan("ItemName"))` | `bright(cyan("You crafted a Headlamp!"))` |
| **Workbench browse — crafted** | `green("[CRAFTED]")` | `green("[CRAFTED]") + " Headlamp"` |
| **Workbench browse — ready** | `cyan("[READY]")` | `cyan("[READY]") + " Headlamp"` |
| **Workbench browse — missing** | `red("[MISSING MATERIALS]")` | `red("[MISSING MATERIALS]") + " Headlamp"` |
| **Inventory check** | plain text | `"Headlamp"` (already in inventory display) |

### Multiple Item Priority

When multiple items could trigger on the same event, use this priority:
1. **Highest tier first** — Tier 4 > Tier 3 > Tier 2 > Tier 1 > base items
2. **Within same tier** — most specific item wins (Assassin's Kit > Shiv for combat)
3. **Display ALL that trigger** — if both a Shiv and Pepper Spray help, show both

### Code Pattern

```python
# Standard item trigger pattern
if has_item(player, "Headlamp"):
    typer.typewriter(f"Your {cyan(bright('Headlamp'))} cuts through the darkness.")
    # ... modified outcome ...
elif has_item(player, "Flashlight"):
    typer.typewriter(f"Your {cyan(bright('Flashlight'))} helps, but it's not ideal.")
    # ... lesser modified outcome ...
else:
    # ... default outcome ...
```

### Implementation Note

Crafted items should ALWAYS check before their base ingredients — e.g., check for "Headlamp" before "Flashlight" since the Headlamp is the upgraded version. This prevents the lesser item from triggering when the player has the better version.

---

## 32. Recipe Hint System Design

### Overview

When the player visits the workbench, they receive a **random recipe hint** before the menu appears. The hint quality scales with how many items they've crafted — rewarding experimentation. A player who has crafted 0 items gets cryptic, vague hints. A player who has crafted 40+ items gets crystal-clear recipes.

### Hint Tiers

| Tier | Name | Crafted Count | Hint Style | Example |
|------|------|--------------|------------|---------|
| 0 | **Vague** | 0–2 crafted | Poetic/cryptic, no item names | *"Light and adhesion... there's something there."* |
| 1 | **Suggestive** | 3–9 crafted | Category + partial ingredient | *"Something from the gadget family... involves a light source."* |
| 2 | **Clear** | 10–19 crafted | Full ingredient list, no result name | *"Flashlight + Duct Tape = ???"* |
| 3 | **Expert** | 20–39 crafted | Full recipe revealed | *"Flashlight + Duct Tape = Headlamp"* |
| 4 | **Master** | 40+ crafted | Tier 2/3/4 recipe revealed + flavor | *"Combine Binocular Scope + Headlamp to forge a Night Scope — eyes that never sleep."* |

### Hint Selection Logic

1. Determine player's hint tier based on `len(player.crafted_items)`
2. Filter to recipes the player **has NOT yet crafted**
3. Pick one at random
4. Display the hint at the appropriate tier's verbosity level
5. If ALL recipes at current tier are crafted, pull from the next tier up

### Hint Exclusions

- Never hint at a recipe the player has already crafted
- Never hint at Tier 3/4 recipes unless player is at Master tier (40+ crafts)
- If player has crafted everything available at their tier, say: *"You've mastered everything you know. Perhaps greater combinations await..."*

### Implementation Location

**File:** `locations.py` → `visit_workbench()` (around L2494)

Insert hint display AFTER the workbench description text but BEFORE the choice menu.

```python
def get_recipe_hint(player):
    """Return a random recipe hint scaled to player's crafting experience."""
    recipes = get_crafting_recipes()
    crafted_count = len(getattr(player, 'crafted_items', []))
    uncrafted = [name for name in recipes if name not in getattr(player, 'crafted_items', [])]
    
    if not uncrafted:
        return italic("You've mastered every recipe known. Legend status.")
    
    recipe_name = random.choice(uncrafted)
    recipe = recipes[recipe_name]
    ingredients = recipe["ingredients"]
    
    if crafted_count <= 2:
        # Tier 0: Vague
        return recipe.get("hint_vague", "Something useful can be made here...")
    elif crafted_count <= 9:
        # Tier 1: Suggestive
        return recipe.get("hint_suggestive", f"Something in the {recipe['category']} family...")
    elif crafted_count <= 19:
        # Tier 2: Clear
        ing_text = " + ".join(ingredients)
        return f"{ing_text} = ???"
    elif crafted_count <= 39:
        # Tier 3: Expert
        ing_text = " + ".join(ingredients)
        return f"{ing_text} = {recipe_name}"
    else:
        # Tier 4: Master — reveal Tier 2+ recipes
        tier2_uncrafted = [n for n in uncrafted if recipes[n].get("tier", 1) >= 2]
        if tier2_uncrafted:
            t2_name = random.choice(tier2_uncrafted)
            t2 = recipes[t2_name]
            ing_text = " + ".join(t2["ingredients"])
            return f"{ing_text} = {t2_name} — {t2.get('hint_master', 'a masterwork')}"
        return f"{' + '.join(ingredients)} = {recipe_name}"
```

### Display Example (in `visit_workbench`)

```python
# After workbench description, before menu
hint = get_recipe_hint(player)
typer.typewriter("")
typer.typewriter(yellow("💡 Crafting Insight: ") + italic(hint))
typer.typewriter("")
```

### Recipe Dict Additions

Each recipe entry in `lists.py` gains these optional fields:

```python
"Headlamp": {
    "ingredients": ["Flashlight", "Duct Tape"],
    "description": "A hands-free light source strapped to your head.",
    "pawn_value": 28,
    "category": "Gadgets",
    "craft_text": "You strap the flashlight to a band of duct tape. Ugly, but it works.",
    "hint_vague": "Light and adhesion... there's something there.",
    "hint_suggestive": "A gadget involving a light source and something sticky.",
    "tier": 1
}
```

---

## 33. All Recipe Hint Texts (by Tier)

Every recipe needs a **Vague** (Tier 0) and **Suggestive** (Tier 1) hint. Tiers 2–3 are auto-generated from ingredients/name. Tier 4 (Master) hints are written for Tier 2+ recipes only.

### Gadgets (7 recipes)

| Recipe | Vague Hint | Suggestive Hint |
|--------|-----------|----------------|
| **Headlamp** | *"Light and adhesion... there's something there."* | *"A gadget involving a light source and something sticky."* |
| **Spotlight** | *"Focused vision, magnified brilliance."* | *"A gadget combining illumination with magnification."* |
| **Evidence Kit** | *"A snapshot and a signal — truth finds a way."* | *"A gadget for documentation. Camera meets communication."* |
| **Radio Jammer** | *"Silence the airwaves, muffle the noise."* | *"A gadget that disrupts signals. Boost meets spark."* |
| **EMP Device** | *"Dead circuits, fried connections."* | *"A gadget that kills electronics. Battery cleaner meets fuses."* |
| **Distress Beacon** | *"When you scream into the void and it answers."* | *"A gadget for emergencies. Life-saving tech meets signal range."* |
| **Security Bypass** | *"The locked and the sharp make an unlikely pair."* | *"A gadget for getting through doors. Lock meets blade."* |

### Disguises (7 recipes)

| Recipe | Vague Hint | Suggestive Hint |
|--------|-----------|----------------|
| **Low-Profile Outfit** | *"Blend in. Become nobody."* | *"A disguise using eyewear and weather protection."* |
| **Beach Bum Disguise** | *"Sun-kissed anonymity."* | *"A disguise for hot days. Shades and sunscreen."* |
| **Gas Mask** | *"Breathe clean in a filthy world."* | *"A disguise for toxic air. Eye protection meets freshness."* |
| **Storm Suit** | *"Nature's fury, deflected."* | *"A disguise against weather. Rain gear meets rain gear."* |
| **Brass Knuckles** | *"Fist and steel, a brutal marriage."* | *"A weapon disguised as accessory. Gloves meet metal."* |
| **Gentleman's Charm** | *"Smell and silk — the tools of persuasion."* | *"A social disguise. Fragrance meets fine fabric."* |
| **Forged Documents** | *"Ink makes identity."* | *"A disguise on paper. Writing instrument meets memory."* |

### Tonics & Consumables (9 recipes)

| Recipe | Vague Hint | Suggestive Hint |
|--------|-----------|----------------|
| **Antacid Brew** | *"Settle the storm inside."* | *"A tonic for stomach trouble. Powder meets hydration."* |
| **Trail Mix Bomb** | *"Seeds of chaos, ignited."* | *"A consumable surprise. Fire meets feed."* |
| **Animal Bait** | *"The way to a beast's heart..."* | *"A tonic for luring creatures. Treats meet seeds."* |
| **Stink Bomb** | *"Rotten chemistry at its finest."* | *"A consumable weapon. Fish meets chemistry."* |
| **Voice Soother** | *"Words flow like honey."* | *"A tonic for the throat. Soothing drops meet fresh breath."* |
| **Outdoor Shield** | *"Sun and bugs bow before you."* | *"A tonic for outdoor protection. Sunblock meets repellent."* |
| **Cool Down Kit** | *"Beat the heat, drink the solution."* | *"A tonic for hot weather. Premium protection meets hydration."* |
| **Smoke Flare** | *"A dark cloud with a purpose."* | *"A consumable signal. Fire meets plastic."* |
| **Vermin Bomb** | *"Nuclear option for tiny invaders."* | *"A consumable for pests. Extermination meets chemistry."* |

### Dark Arts (5 recipes)

| Recipe | Vague Hint | Suggestive Hint |
|--------|-----------|----------------|
| **Eldritch Candle** | *"Forbidden light, pages that shouldn't be read."* | *"A dark creation. Cursed text meets flame."* |
| **Binding Portrait** | *"A face captured is a soul leashed."* | *"A dark creation. Cursed text meets a frozen moment."* |
| **Blackmail Letter** | *"Secrets are currency."* | *"A dark creation. Sealed mystery meets fine writing."* |
| **Devil's Deck** | *"Cards that play themselves."* | *"A dark creation. A game meets fire."* |
| **Fortune Cards** | *"Luck stacked in your favor, literally."* | *"A dark creation. A game meets a lucky charm."* |

### Luxury Crafts (7 recipes)

| Recipe | Vague Hint | Suggestive Hint |
|--------|-----------|----------------|
| **Kingpin Look** | *"Gold and smoke — power dresses itself."* | *"A luxury item. Precious metal meets fine tobacco."* |
| **Enchanted Vintage** | *"Silver vessel, crimson spirit."* | *"A luxury item. Fine drinkware meets aged wine."* |
| **Heirloom Set** | *"Time and ink, passed down forever."* | *"A luxury item. Antique timepiece meets writing instrument."* |
| **Aristocrat's Touch** | *"Soft hands that command hard rooms."* | *"A luxury item. Fine leather meets fine fabric."* |
| **Power Move Kit** | *"The lighter clicks. The room listens."* | *"A luxury item. Personalized flame meets fine tobacco."* |
| **Animal Magnetism** | *"They can't explain it. They just lean closer."* | *"A luxury item. Fragrance meets leather."* |
| **Luck Totem** | *"Double the luck, double the superstition."* | *"A luxury item. Two lucky charms become one."* |

### Vehicle Upgrades (5 recipes)

| Recipe | Vague Hint | Suggestive Hint |
|--------|-----------|----------------|
| **Tire Ready Kit** | *"Flat tires fear preparation."* | *"A vehicle upgrade. Spare rubber meets lifting power."* |
| **Power Grid** | *"Jump-start everything at once."* | *"A vehicle upgrade. Cable power meets fuse protection."* |
| **Miracle Lube** | *"Squeaks, groans, and resistance — silenced."* | *"A vehicle upgrade. Two lubricants become one."* |
| **Mobile Workshop** | *"Fix anything, anywhere."* | *"A vehicle upgrade. Full toolkit meets quick fixes."* |
| **Pursuit Package** | *"Catch anything on four legs."* | *"A vehicle upgrade. Calling meets chasing."* |

### Tier 2 Master Hints (shown at 40+ crafts)

These are full reveal + flavor. Only shown once the player is deep into crafting.

| Recipe | Master Hint |
|--------|------------|
| **Assassin's Kit** | *"Shiv + Pepper Spray = Assassin's Kit — strike silent, strike blind."* |
| **Fire Launcher** | *"Slingshot + Road Flare Torch = Fire Launcher — rain fire from a distance."* |
| **Tear Gas** | *"Pepper Spray + Stink Bomb = Tear Gas — a crowd-clearing cocktail."* |
| **Street Fighter Set** | *"Shiv + Brass Knuckles = Street Fighter Set — blade and bruise, together at last."* |
| **Survival Bivouac** | *"Emergency Blanket + Fire Starter Kit = Survival Bivouac — a home in the wild."* |
| **Hydration Station** | *"Water Purifier + Rain Collector = Hydration Station — nature's tap, purified."* |
| **Provider's Kit** | *"Snare Trap + Fishing Rod = Provider's Kit — land and sea, covered."* |
| **Fortified Perimeter** | *"Improvised Trap + Car Alarm Rigging = Fortified Perimeter — nothing gets close."* |
| **All-Weather Armor** | *"Storm Suit + Outdoor Shield = All-Weather Armor — laugh at the forecast."* |
| **Master Key** | *"Lockpick Set + Security Bypass = Master Key — every door opens for you."* |
| **Night Scope** | *"Binocular Scope + Headlamp = Night Scope — eyes that never sleep."* |
| **SOS Kit** | *"Signal Mirror + Smoke Flare = SOS Kit — visible from miles."* |
| **Intelligence Dossier** | *"Evidence Kit + Forged Documents = Intelligence Dossier — know everything about everyone."* |
| **Surveillance Suite** | *"Spotlight + Radio Jammer = Surveillance Suite — see all, hear nothing."* |
| **Mind Shield** | *"Dream Catcher + Worry Stone = Mind Shield — your thoughts are your fortress."* |
| **Fortune's Favor** | *"Lucky Charm Bracelet + Luck Totem = Fortune's Favor — luck made physical."* |
| **Fate Reader** | *"Lucky Charm Bracelet + Fortune Cards = Fate Reader — peek behind destiny's curtain."* |
| **Lucid Dreaming Kit** | *"Dream Catcher + Eldritch Candle = Lucid Dreaming Kit — command the dream."* |
| **Old Money Identity** | *"Gentleman's Charm + Heirloom Set = Old Money Identity — you were always rich."* |
| **New Identity** | *"Low-Profile Outfit + Forged Documents = New Identity — who you were is dead."* |
| **Beast Tamer Kit** | *"Animal Bait + Pet Toy = Beast Tamer Kit — friend to every creature."* |
| **Cheater's Insurance** | *"Devil's Deck + Evidence Kit = Cheater's Insurance — cheat and never get caught."* |
| **Roadside Shield** | *"Tire Ready Kit + Power Grid = Roadside Shield — breakdowns are extinct."* |
| **Auto Mechanic** | *"Mobile Workshop + Miracle Lube = Auto Mechanic — your car purrs like a kitten."* |
| **Rolling Fortress** | *"Pursuit Package + Fortified Perimeter = Rolling Fortress — a mobile bunker."* |

### Tier 3 & 4 Vision Hints (shown at 40+ crafts, rare)

These appear after the player has crafted most Tier 2 items. They reference Tier 3/4 recipes but stay mysterious.

| Tier | Recipe | Vision Hint |
|------|--------|------------|
| T3 | **Road Warrior Armor** | *"Three weapons forged into one... you'd be untouchable."* |
| T3 | **Third Eye** | *"The mind, the dream, and the fortune — combine them."* |
| T3 | **Nomad's Camp** | *"Shelter, food, water. All three. Total freedom."* |
| T3 | **All-Access Pass** | *"Locks, darkness, secrets — master them all."* |
| T3 | **Master of Games** | *"Identity, insurance, and a full glass. The perfect con."* |
| T3 | **Immortal Vehicle** | *"A mechanic's dream — the car that fixes itself."* |
| T3 | **Gambler's Aura** | *"Luck upon luck upon luck. The universe bends."* |
| T3 | **Ark Master's Horn** | *"Call them. Feed them. Command them."* |
| T3 | **Guardian Angel** | *"Signal, beacon, perimeter. Nothing can touch you."* |
| T3 | **Hazmat Suit** | *"Mask, armor, storm gear. Walk through anything."* |
| T3 | **Ghost Protocol** | *"Surveillance, identity, silence. Vanish completely."* |
| T3 | **Dark Pact Reliquary** | *"Candle, portrait, deck. The devil's own toolkit."* |
| T4 | **Beastslayer Mantle** | *"Armor and a tooth... the predator becomes prey."* |
| T4 | **Seer's Chronicle** | *"The third eye meets the hermit's wisdom..."* |
| T4 | **Wanderer's Rest** | *"A camp and a walking stick. True nomad freedom."* |
| T4 | **Skeleton Key** | *"All-access meets night vision. Nothing is locked."* |
| T4 | **King of the Road** | *"The master of games claims the crown..."* |
| T4 | **War Wagon** | *"Immortal vehicle meets artisan skill. The ultimate ride."* |
| T4 | **Moonlit Fortune** | *"The gambler's aura catches a shard of moonlight..."* |
| T4 | **Leviathan's Call** | *"The ark master finds the pearl of the deep..."* |
| T4 | **Last Breath Locket** | *"An angel and a phoenix feather. Death loses meaning."* |
| T4 | **Phantom Rose** | *"A ghost leaves behind only a metal flower..."* |
| T4 | **Soul Forge** | *"The reliquary accepts a ritual token. You rewrite fate."* |

---

## 34. Shop & Pawn Descriptions — All New Items

### Grimy Gus Pawn Dialogue (Tier 1 — 40 items)

When selling crafted items to Grimy Gus, he has a custom reaction. These go in the `gus_descriptions` dict in `locations.py`.

#### Gadgets

| Item | Pawn Value | Gus Quote |
|------|-----------|-----------|
| **Headlamp** | $28 | *"A flashlight taped to a headband? I've seen worse. Actually no, I haven't. Twenty-eight bucks."* |
| **Spotlight** | $55 | *"Flashlight-binocular love child. Could blind a man at fifty yards. Fifty-five."* |
| **Evidence Kit** | $45 | *"Camera and a signal booster strapped together. Playing detective? Forty-five."* |
| **Radio Jammer** | $40 | *"This blocks radio? ...Why do you need to block radio? Forty, don't tell me."* |
| **EMP Device** | $50 | *"This thing'll fry every phone in a city block. Fifty and I'm keeping it behind the counter."* |
| **Distress Beacon** | $90 | *"LifeAlert on steroids. Coast Guard would love this. Ninety."* |
| **Security Bypass** | $35 | *"Padlock shiv combo. Very illegal. Very useful. Thirty-five."* |

#### Disguises

| Item | Pawn Value | Gus Quote |
|------|-----------|-----------|
| **Low-Profile Outfit** | $20 | *"Sunglasses and a poncho. You look like a tourist who gave up. Twenty."* |
| **Beach Bum Disguise** | $18 | *"The 'I peaked in high school' starter pack. Eighteen."* |
| **Gas Mask** | $35 | *"Welding goggles and air freshener? You'll smell like pine while looking like a bug. Thirty-five."* |
| **Storm Suit** | $18 | *"Double rain gear. You expecting a hurricane or just paranoid? Eighteen."* |
| **Brass Knuckles** | $70 | *"Gloves with a padlock weight. Old school. Respect. Seventy."* |
| **Gentleman's Charm** | $200 | *"Cologne and silk... you trying to schmooze or seduce? Either way — two hundred."* |
| **Forged Documents** | $60 | *"I don't even want to read these. Sixty and I never saw you."* |

#### Tonics & Consumables

| Item | Pawn Value | Gus Quote |
|------|-----------|-----------|
| **Antacid Brew** | $8 | *"Baking soda water. My grandma made this. Eight bucks for nostalgia."* |
| **Trail Mix Bomb** | $10 | *"Matches and birdseed? Is this... a firebomb for birds? Ten."* |
| **Animal Bait** | $12 | *"Dog treats and seeds. Either you're hunting or hosting a party. Twelve."* |
| **Stink Bomb** | $8 | *"Tuna and baking soda. You monster. Eight, and open it outside."* |
| **Voice Soother** | $10 | *"Cough drops and mints. Gonna serenade someone? Ten."* |
| **Outdoor Shield** | $15 | *"Sunscreen-bug spray combo. Taking on Mother Nature. Fifteen."* |
| **Cool Down Kit** | $18 | *"Premium sunscreen and water. The 'I refuse to sweat' package. Eighteen."* |
| **Smoke Flare** | $8 | *"Matches in a bag. Primitive but effective. Eight."* |
| **Vermin Bomb** | $20 | *"Industrial pest killer. I could use one of these. Twenty."* |

#### Dark Arts

| Item | Pawn Value | Gus Quote |
|------|-----------|-----------|
| **Eldritch Candle** | $100 | *"Is that... are those pages from the Necronomicon? Wrapped around a CANDLE? A hundred. Don't light it in here."* |
| **Binding Portrait** | $80 | *"A photo bound with cursed text. The person in this picture is having a bad week. Eighty."* |
| **Blackmail Letter** | $75 | *"Sealed envelope, fancy pen, look of guilt on your face. Seventy-five and I'm not reading it."* |
| **Devil's Deck** | $30 | *"Charred playing cards. These feel... warm. Thirty and take them back."* |
| **Fortune Cards** | $20 | *"Lucky penny glued to a deck of cards. Homemade tarot? Twenty."* |

#### Luxury Crafts

| Item | Pawn Value | Gus Quote |
|------|-----------|-----------|
| **Kingpin Look** | $350 | *"Gold chain, cigars... you look like a movie villain. I love it. Three-fifty."* |
| **Enchanted Vintage** | $400 | *"Silver flask filled with wine aged beyond reason. My mouth is watering. Four hundred."* |
| **Heirloom Set** | $500 | *"Antique watch and pen set. This screams old money. Five hundred, easy."* |
| **Aristocrat's Touch** | $250 | *"Leather and silk combo. You could convince a king you're his cousin. Two-fifty."* |
| **Power Move Kit** | $300 | *"Monogrammed lighter and cigars. Power lunch energy. Three hundred."* |
| **Animal Magnetism** | $200 | *"Cologne and gloves. The 'mysterious stranger' starter kit. Two hundred."* |
| **Luck Totem** | $150 | *"Rabbit foot and lucky penny fused together. That's either genius or an abomination. One-fifty."* |

#### Vehicle Upgrades

| Item | Pawn Value | Gus Quote |
|------|-----------|-----------|
| **Tire Ready Kit** | $60 | *"Spare and a jack, pre-bundled. Smart. Sixty."* |
| **Power Grid** | $40 | *"Jumper cables and fuses together. Emergency kit deluxe. Forty."* |
| **Miracle Lube** | $35 | *"Motor oil and WD-40 merged into... super lube? Thirty-five."* |
| **Mobile Workshop** | $60 | *"Tool kit and duct tape. You could rebuild a car with this. Sixty."* |
| **Pursuit Package** | $40 | *"Dog whistle and running shoes. Chasing something or running from it? Forty."* |

### Grimy Gus Pawn Dialogue (Tier 2 — 25 items)

| Item | Pawn Value | Gus Quote |
|------|-----------|-----------|
| **Assassin's Kit** | $80 | *"Blade and spray. You don't mess around. Eighty."* |
| **Fire Launcher** | $75 | *"A slingshot that launches FIRE? Seventy-five and please leave."* |
| **Tear Gas** | $50 | *"Homemade tear gas. We live in a society. Fifty."* |
| **Street Fighter Set** | $100 | *"Shiv and brass knuckles. You were born in the wrong century. A hundred."* |
| **Survival Bivouac** | $40 | *"Portable shelter with a heat source. Doomsday prepper stuff. Forty."* |
| **Hydration Station** | $35 | *"Purifier and rain catcher combo. You could live in the desert. Thirty-five."* |
| **Provider's Kit** | $50 | *"Trap and rod. You eating like a king out there? Fifty."* |
| **Fortified Perimeter** | $55 | *"Traps and alarms. Nothing's getting within a hundred feet of you. Fifty-five."* |
| **All-Weather Armor** | $45 | *"Weather can't touch you in this. Forty-five."* |
| **Master Key** | $80 | *"Opens anything, anywhere. I should charge more. Eighty."* |
| **Night Scope** | $65 | *"See in the dark? For real? Sixty-five and let me try it."* |
| **SOS Kit** | $30 | *"Mirror and smoke. Rescue will find you. Thirty."* |
| **Intelligence Dossier** | $100 | *"Evidence and forged papers. You running a spy ring? A hundred."* |
| **Surveillance Suite** | $90 | *"Light and jammer. Full counter-intel. Ninety."* |
| **Mind Shield** | $30 | *"Dream catcher and a stone. For the anxious apocalypse survivor. Thirty."* |
| **Fortune's Favor** | $200 | *"Double luck charms. You're either blessed or cursed. Two hundred."* |
| **Fate Reader** | $50 | *"DIY fortune telling. Does it work? ...Don't answer that. Fifty."* |
| **Lucid Dreaming Kit** | $80 | *"Dream catcher with a cursed candle. Sweet dreams... or nightmares. Eighty."* |
| **Old Money Identity** | $500 | *"Complete aristocrat package. You fooled ME and I know it's fake. Five hundred."* |
| **New Identity** | $100 | *"New name, new face, new you. FBI wishes they'd thought of this. A hundred."* |
| **Beast Tamer Kit** | $30 | *"Bait and toys. You Dr. Dolittle now? Thirty."* |
| **Cheater's Insurance** | $60 | *"Cheat at cards AND have evidence on the house. Diabolical. Sixty."* |
| **Roadside Shield** | $100 | *"Complete roadside rescue package. AAA in a box. A hundred."* |
| **Auto Mechanic** | $120 | *"Workshop in a bag. My actual mechanic knows less than this kit. One-twenty."* |
| **Rolling Fortress** | $110 | *"Mobile bunker on wheels. Mad Max would be jealous. One-ten."* |

### Grimy Gus Pawn Dialogue (Tier 3 — 12 items)

| Item | Pawn Value | Gus Quote |
|------|-----------|-----------|
| **Road Warrior Armor** | $300 | *"Three weapons fused into... I don't even know what this is. Three hundred, don't point it at me."* |
| **Third Eye** | $200 | *"You can see the FUTURE with this? ...What's my future? Two hundred."* |
| **Nomad's Camp** | $150 | *"Complete off-grid survival system. You don't need society. One-fifty."* |
| **All-Access Pass** | $350 | *"Keys, scopes, dossiers. You could rob the Pentagon. Three-fifty."* |
| **Master of Games** | $800 | *"The complete con artist's toolkit. I'm... honestly impressed. Eight hundred."* |
| **Immortal Vehicle** | $500 | *"Self-repairing car kit. My mechanic is out of a job. Five hundred."* |
| **Gambler's Aura** | $400 | *"Triple luck. The universe owes you favors. Four hundred."* |
| **Ark Master's Horn** | $250 | *"You command animals now? Like a pirate? Two-fifty."* |
| **Guardian Angel** | $300 | *"Beacon, signal, and fortress. You're untouchable. Three hundred."* |
| **Hazmat Suit** | $150 | *"Walk through poison gas, acid rain, and a hurricane. One-fifty."* |
| **Ghost Protocol** | $400 | *"Full invisibility package. You're a ghost. Four hundred."* |
| **Dark Pact Reliquary** | $200 | *"Candle, portrait, cards — all cursed. I need gloves to hold this. Two hundred."* |

### Grimy Gus Pawn Dialogue (Tier 4 — 11 items)

| Item | Pawn Value | Gus Quote |
|------|-----------|-----------|
| **Beastslayer Mantle** | $1000 | *"This radiates... danger. A thousand and get it out of my shop."* |
| **Seer's Chronicle** | $1000 | *"The pages write THEMSELVES? A thousand. No, two — no, a thousand."* |
| **Wanderer's Rest** | $800 | *"True self-sufficiency. You don't need money anymore. Eight hundred."* |
| **Skeleton Key** | $1500 | *"Opens. Anything. Fifteen hundred. I'm locking my safe."* |
| **King of the Road** | $2000 | *"Everyone listens to you. Every game favors you. Two thousand. Your Majesty."* |
| **War Wagon** | $1800 | *"A car that fights AND fixes itself? Eighteen hundred. Can I ride in it?"* |
| **Moonlit Fortune** | $2000 | *"Permanent luck boost. The casinos will ban you from EXISTING. Two thousand."* |
| **Leviathan's Call** | $1500 | *"Command sea creatures. I once had a pet goldfish. Fifteen hundred."* |
| **Last Breath Locket** | $5000 | *"You... can't die? Five thousand. I don't know what else to say."* |
| **Phantom Rose** | $2500 | *"A legend no one can find. You'll be a myth. Twenty-five hundred."* |
| **Soul Forge** | $3000 | *"Rewrite the past. Change a mistake. Three thousand... I have a lot of mistakes."* |

### Workbench Inspection Descriptions (Tier 1 — all 40 new items)

When using "Inspect" at the workbench, each recipe shows a description. These go in the recipe dict's `"description"` field.

#### Gadgets

| Item | Inspection Description |
|------|----------------------|
| **Headlamp** | *A flashlight rigged to a duct tape headband. Hands-free illumination for the resourceful survivor.* |
| **Spotlight** | *Binocular lenses focused through a flashlight beam. Sees further and brighter than either alone.* |
| **Evidence Kit** | *A disposable camera wired to a signal booster. Document anything and transmit proof instantly.* |
| **Radio Jammer** | *Signal booster reversed into a noise emitter. Blankets nearby frequencies with static.* |
| **EMP Device** | *Battery cleaner acid and spare fuses jury-rigged into a pulse generator. One burst kills all electronics nearby.* |
| **Distress Beacon** | *LifeAlert hardware boosted with signal range. Calls for help across county lines.* |
| **Security Bypass** | *A padlock's innards used with a knife to probe tumblers. Opens most standard locks.* |

#### Disguises

| Item | Inspection Description |
|------|----------------------|
| **Low-Profile Outfit** | *Sunglasses tucked into a poncho hood. You look like nobody worth remembering.* |
| **Beach Bum Disguise** | *Shades and sunscreen. The universal "don't talk to me, I'm on vacation" look.* |
| **Gas Mask** | *Welding goggles sealed with air freshener filters. Ugly but breathable.* |
| **Storm Suit** | *Umbrella frame reinforced with plastic poncho material. Full-body weather shield.* |
| **Brass Knuckles** | *A padlock nested in the fingers of leather gloves. Hits like a truck.* |
| **Gentleman's Charm** | *Expensive cologne dabbed on a silk handkerchief. Charisma in a pocket square.* |
| **Forged Documents** | *An old photograph attached to hand-lettered papers. Convincing enough. Mostly.* |

#### Tonics & Consumables

| Item | Inspection Description |
|------|----------------------|
| **Antacid Brew** | *Baking soda dissolved in clean water. Grandma's stomach cure.* |
| **Trail Mix Bomb** | *Birdseed packed around matches. Light the fuse, scatter the blast. Mostly seeds.* |
| **Animal Bait** | *Dog treats and birdseed mixed together. If it walks, crawls, or flies — it's coming.* |
| **Stink Bomb** | *Tuna juice and baking soda in a sealed container. Open at everyone else's risk.* |
| **Voice Soother** | *Cough drops dissolved in minty water. Your voice becomes silk.* |
| **Outdoor Shield** | *Sunscreen and bug spray combined. One application, total outdoor armor.* |
| **Cool Down Kit** | *Premium sunscreen mixed with cold water bottles. Ice bath for your skin.* |
| **Smoke Flare** | *Matches stuffed in a garbage bag with an air pocket. Light and toss for thick smoke cover.* |
| **Vermin Bomb** | *Pest control chemicals mixed with baking soda accelerant. Chemical warfare against rats.* |

#### Dark Arts

| Item | Inspection Description |
|------|----------------------|
| **Eldritch Candle** | *Pages from the Necronomicon wrapped around a wax core. The flame burns cold and green.* |
| **Binding Portrait** | *An old photograph inscribed with forbidden text. The subject's eyes seem to follow you.* |
| **Blackmail Letter** | *Contents of a mysterious envelope rewritten in elegant calligraphy. Leverage, distilled.* |
| **Devil's Deck** | *Playing cards passed through open flame. The suits have changed to things you don't recognize.* |
| **Fortune Cards** | *A lucky penny fixed to the deck's ace of spades. The cards fall in patterns that shouldn't be random.* |

#### Luxury Crafts

| Item | Inspection Description |
|------|----------------------|
| **Kingpin Look** | *Gold chain over a fine cigar jacket. You look like you own the building.* |
| **Enchanted Vintage** | *Vintage wine decanted into a silver flask. The taste improves with each sip.* |
| **Heirloom Set** | *Antique watch paired with a monogrammed pen. Inherited wealth you never had.* |
| **Aristocrat's Touch** | *Leather gloves and silk handkerchief, perfectly matched. Old money manners.* |
| **Power Move Kit** | *Monogrammed lighter and premium cigars. The "I just closed a deal" accessory.* |
| **Animal Magnetism** | *Cologne-scented leather gloves. People lean toward you without knowing why.* |
| **Luck Totem** | *Lucky rabbit foot braided with a penny on a cord. Double superstition.* |

#### Vehicle Upgrades

| Item | Inspection Description |
|------|----------------------|
| **Tire Ready Kit** | *Spare tire pre-mounted with a car jack bracket. One-stop flat tire fix.* |
| **Power Grid** | *Jumper cables and fuses in a quick-access panel. Your car's electrical lifeline.* |
| **Miracle Lube** | *Motor oil and WD-40 in a squeeze bottle. Fixes any squeak, grind, or groan.* |
| **Mobile Workshop** | *Tool kit strapped to duct tape rolls. Fix anything from a fender to a fuel line.* |
| **Pursuit Package** | *Dog whistle and running shoes bundled together. Chase or be chased — you're ready either way.* |

---

## 35. Craft Text & Use Descriptions — All New Items

### Craft Text (Tier 1 — 40 items)

Displayed when the player successfully crafts the item at the workbench. Goes in `"craft_text"` field.

#### Gadgets

| Item | Craft Text |
|------|-----------|
| **Headlamp** | *You strap the flashlight to a band of duct tape. Ugly, but it works. Hands are free.* |
| **Spotlight** | *You jam the flashlight into the binocular housing. The beam narrows to a piercing lance of light.* |
| **Evidence Kit** | *Camera snaps, signal boosts. Click and transmit. Digital justice.* |
| **Radio Jammer** | *You reverse the signal booster's polarity. Static fills every frequency. Silence for everyone else.* |
| **EMP Device** | *Acid meets wire meets fury. One pulse and everything electronic in shouting distance dies.* |
| **Distress Beacon** | *You boost the LifeAlert's range tenfold. If you scream now, three counties hear it.* |
| **Security Bypass** | *You feel how the padlock's pins move. The knife becomes a key.* |

#### Disguises

| Item | Craft Text |
|------|-----------|
| **Low-Profile Outfit** | *Shades under the poncho hood. You catch your reflection — even you don't recognize yourself.* |
| **Beach Bum Disguise** | *Sunscreen and shades. You look like someone who lost their beach towel and their ambition.* |
| **Gas Mask** | *Goggles sealed with air freshener filters. You breathe pine-scented safety.* |
| **Storm Suit** | *Umbrella frame over poncho shell. You're weatherproof from head to ankle.* |
| **Brass Knuckles** | *Padlock nested in leather. Your fist weighs double now.* |
| **Gentleman's Charm** | *A dab of cologne on silk. You could talk a banker into giving you his wallet.* |
| **Forged Documents** | *Careful penmanship over an old photo. New name, new history. Same face, though.* |

#### Tonics & Consumables

| Item | Craft Text |
|------|-----------|
| **Antacid Brew** | *Baking soda fizzes in the water. Your stomach unclenches just looking at it.* |
| **Trail Mix Bomb** | *Seeds packed around matches. Light, throw, scatter. Chaos in a handful.* |
| **Animal Bait** | *Treats and seeds mixed together. Everything with a nose is coming to you.* |
| **Stink Bomb** | *Tuna juice and baking soda sealed tight. The moment this opens, people evacuate.* |
| **Voice Soother** | *Cough drops melt into minty water. Your throat hums with clarity.* |
| **Outdoor Shield** | *Sunscreen and bug spray swirled together. One coat and the outdoors can't touch you.* |
| **Cool Down Kit** | *Premium sunscreen mixed with ice-cold water. Your skin sighs with relief.* |
| **Smoke Flare** | *Matches in a garbage bag with trapped air. Light the fuse and toss. Smoke for days.* |
| **Vermin Bomb** | *Pest powder in a fizzing baking soda shell. The rats won't know what hit them.* |

#### Dark Arts

| Item | Craft Text |
|------|-----------|
| **Eldritch Candle** | *You wrap the forbidden pages around the wax. The candle seems to light itself for a moment.* |
| **Binding Portrait** | *Cursed ink crosses the photograph. The person in the picture blinks. You're sure of it.* |
| **Blackmail Letter** | *The envelope's secrets, rewritten in your hand. Power on paper.* |
| **Devil's Deck** | *The cards pass through the flame. The jokers grin wider than before.* |
| **Fortune Cards** | *The penny adheres to the ace. The deck shuffles itself once — then stops.* |

#### Luxury Crafts

| Item | Craft Text |
|------|-----------|
| **Kingpin Look** | *Gold draped over fine cigars. You don't just look rich. You look dangerous.* |
| **Enchanted Vintage** | *Wine poured into silver. It tastes like money and moonlight.* |
| **Heirloom Set** | *Watch ticks, pen waits. Together they tell a story of wealth you're borrowing.* |
| **Aristocrat's Touch** | *Leather pulls, silk folds. Your hands look like they belong to someone important.* |
| **Power Move Kit** | *Lighter snaps, cigar catches. The room turns to watch you.* |
| **Animal Magnetism** | *Cologne on leather. You smell like confidence and old libraries.* |
| **Luck Totem** | *Rabbit foot tied to a lucky penny. The superstition doubles — or cancels out. Either way, something's happening.* |

#### Vehicle Upgrades

| Item | Craft Text |
|------|-----------|
| **Tire Ready Kit** | *Jack pre-set, tire mounted. Next flat takes two minutes instead of twenty.* |
| **Power Grid** | *Cables and fuses organized into a quick-access panel. Your car's nervous system, sorted.* |
| **Miracle Lube** | *Oil and WD-40 combined. Everything moves smoother than it has a right to.* |
| **Mobile Workshop** | *Tools and tape in arm's reach. You could rebuild a transmission on the side of the road.* |
| **Pursuit Package** | *Whistle and shoes. If it runs, you follow. Fast.* |

### Craft Text (Tier 2 — 25 items)

| Item | Craft Text |
|------|-----------|
| **Assassin's Kit** | *Blade and spray unified. One blinds, the other finishes. You feel a little sick about how natural this felt.* |
| **Fire Launcher** | *Flaming projectile, loaded. Point and release. Everything in the target zone burns.* |
| **Tear Gas** | *Pepper spray atomized through stink bomb chemistry. The air weeps.* |
| **Street Fighter Set** | *Knuckles and blade. Every punch cuts, every cut breaks. Street rules.* |
| **Survival Bivouac** | *Blanket over fire. A warm shelter materializes from nothing. You could live here.* |
| **Hydration Station** | *Rain flows into the purifier. Clean water, forever, for free.* |
| **Provider's Kit** | *Trap on land, rod in water. You eat like a king in the apocalypse.* |
| **Fortified Perimeter** | *Traps and alarms in a ring. Nothing approaches without you knowing — and regretting.* |
| **All-Weather Armor** | *Storm suit fused with outdoor shield. Let the hurricane come. You'll wait it out.* |
| **Master Key** | *Picks and bypass tools merged. Every lock you look at is already open.* |
| **Night Scope** | *Headlamp focused through scope lenses. Darkness isn't dark anymore.* |
| **SOS Kit** | *Mirror and smoke in a launch package. Your distress call reaches the horizon.* |
| **Intelligence Dossier** | *Evidence compiles, documents forge. You know everything about everyone who matters.* |
| **Surveillance Suite** | *Spotlight scans, jammer blocks. You see them. They don't see you.* |
| **Mind Shield** | *Dream catcher weaves around the worry stone. Bad thoughts bounce off like rain.* |
| **Fortune's Favor** | *Two lucky charms, bound. The dice of the universe are loaded in your favor.* |
| **Fate Reader** | *Cards deal themselves. The bracelet hums. You know what happens next.* |
| **Lucid Dreaming Kit** | *The candle's cold flame passes through the catcher. Tonight, you drive the dream.* |
| **Old Money Identity** | *Charm meets heirloom. Your entire history rewrites itself. You were always rich.* |
| **New Identity** | *Low profile meets forged papers. The old you is gone. This is someone else now.* |
| **Beast Tamer Kit** | *Bait and toys combined. Every animal within a mile considers you family.* |
| **Cheater's Insurance** | *The Devil's Deck paired with evidence. Cheat and never get caught. The house always loses.* |
| **Roadside Shield** | *Full emergency roadside kit integrated. Breakdowns are someone else's problem now.* |
| **Auto Mechanic** | *Workshop and lube fused. Your car purrs. It hasn't purred since the lot.* |
| **Rolling Fortress** | *Pursuit gear meets perimeter defense. Your car is a castle that moves.* |

### Craft Text (Tier 3 — 12 items)

| Item | Craft Text |
|------|-----------|
| **Road Warrior Armor** | *Three weapons merge into something terrible and beautiful. You aren't a survivor anymore. You're a force.* |
| **Third Eye** | *Mind, dream, fortune — unified. Your perception tears through the veil of now. You see tomorrow.* |
| **Nomad's Camp** | *Shelter, food, water. Complete self-sufficiency. The world could end and you'd barely notice.* |
| **All-Access Pass** | *Keys, scope, intel. Nothing is locked, hidden, or secret from you.* |
| **Master of Games** | *Identity, insurance, wine. The perfect con. You could buy a casino with borrowed money and a smile.* |
| **Immortal Vehicle** | *Mechanic, fortress, shield. Your car doesn't break. Your car can't break.* |
| **Gambler's Aura** | *Luck upon luck upon luck. The dealer flinches when you sit down.* |
| **Ark Master's Horn** | *Bait, horn, station. The animals don't just come to you — they obey.* |
| **Guardian Angel** | *Signal, beacon, perimeter. You're wrapped in an invisible shield of rescue and defense.* |
| **Hazmat Suit** | *Gas mask, armor, storm gear. Walk through chemical spills, acid rain, and the end of the world.* |
| **Ghost Protocol** | *Surveillance, identity, silence. You are invisible. You are nobody. You are everywhere.* |
| **Dark Pact Reliquary** | *Candle, portrait, deck. The dark items merge into something that whispers. It knows your name.* |

### Craft Text (Tier 4 — 11 items)

| Item | Craft Text |
|------|-----------|
| **Beastslayer Mantle** | *The gator tooth bonds to the armor. Predators recognize you as one of their own — and look away.* |
| **Seer's Chronicle** | *The journal's pages merge with the third eye's vision. The future writes itself in your handwriting.* |
| **Wanderer's Rest** | *The walking stick plants into the camp. Roots grow. This isn't a camp anymore — it's a garden.* |
| **Skeleton Key** | *The night scope merges with the pass. Every door in the world clicks open as you approach.* |
| **King of the Road** | *The crown settles. The games master becomes the road king. Everyone recognizes your authority.* |
| **War Wagon** | *The artisan toolkit welds itself to the vehicle system. Your car rebuilds itself while driving.* |
| **Moonlit Fortune** | *Moon shard meets the aura. Permanent luck. The blackjack table is your kingdom.* |
| **Leviathan's Call** | *The pearl resonates with the horn. Sea creatures surface. Land creatures bow. You are the Ark.* |
| **Last Breath Locket** | *The phoenix feather ignites inside the angel's locket. Death looks at you and looks away. Permanently.* |
| **Phantom Rose** | *The metal rose blooms inside the ghost protocol. You are a legend. A story. A whisper that no one can catch.* |
| **Soul Forge** | *The ritual token feeds the reliquary. Time bends. History rewrites. One moment of the past changes forever.* |

---

## 36. Full Event Narrative Drafts — Gadgets

**Target:** 7 items × 3–4 events each = ~24 new event blocks across multiple files.

### Headlamp (4 events)

**Event 1: Night Cave Exploration** — `events_night.py`
```
Trigger: night exploration event, has_item("Headlamp")
Narrative: "Your HEADLAMP cuts through the cave darkness. Both hands free, 
           you climb deeper. Something glints in the rock — a hidden cache."
Effect: Find bonus loot ($50–200) in night events. Skip darkness penalty.
```

**Event 2: Car Breakdown at Night** — `events_car.py`
```
Trigger: nighttime car trouble, has_item("Headlamp")
Narrative: "You strap on the HEADLAMP and duck under the hood. With both
           hands free, the repair goes twice as fast."
Effect: Car repair takes no time penalty. Better fix quality.
```

**Event 3: Search & Rescue** — `events_day_survival.py`
```
Trigger: lost person event, has_item("Headlamp")
Narrative: "Your HEADLAMP sweeps the treeline. There — a flash of color. 
           You find them huddled in a ditch."
Effect: Guaranteed rescue success. +sanity, +karma reward.
```

**Event 4: Dark Confrontation** — `events_day_dark.py`
```
Trigger: ambush/attack in darkness, has_item("Headlamp")
Narrative: "You flick the HEADLAMP on full beam. The attacker recoils, 
           blinded. You have three seconds to run."
Effect: Escape dark confrontation without damage.
```

### Spotlight (3 events)

**Event 1: Night Watch** — `events_night.py`
```
Trigger: night patrol/guard event, has_item("Spotlight")
Narrative: "The SPOTLIGHT pierces 200 yards of darkness. Nothing moves 
           without you seeing it first."
Effect: Prevent all night theft/ambush events for the night.
```

**Event 2: Adventure Scouting** — `adventures.py`
```
Trigger: adventure zone entry, has_item("Spotlight")
Narrative: "You sweep the SPOTLIGHT across the zone entrance. The terrain 
           reveals itself — paths, dangers, and shortcuts."
Effect: +15% better adventure zone outcomes.
```

**Event 3: Signal for Help** — `events_day_survival.py`
```
Trigger: stranded/lost event, has_item("Spotlight")
Narrative: "You aim the SPOTLIGHT at the sky. A passing truck sees the beam 
           and pulls over."
Effect: Guaranteed rescue from stranded events.
```

### Evidence Kit (3 events)

**Event 1: Crime Scene** — `events_day_dark.py`
```
Trigger: witness crime event, has_item("Evidence Kit")
Narrative: "You snap photos and boost the signal. The EVIDENCE KIT transmits 
           proof to local authorities before the perps notice you."
Effect: Crime solved, +$200 reward, +karma.
```

**Event 2: Con Artist Encounter** — `events_day_people.py`
```
Trigger: scam/fraud event, has_item("Evidence Kit")
Narrative: "Your EVIDENCE KIT captures the con mid-pitch. You show them the 
           photo. They drop the act and walk away fast."
Effect: Avoid scam, keep money, con artist flagged.
```

**Event 3: Insurance Claim** — `events_car.py`
```
Trigger: car damage event, has_item("Evidence Kit")
Narrative: "You document the damage with your EVIDENCE KIT. The insurance 
           company can't argue with timestamped photos."
Effect: Get full repair reimbursement instead of partial.
```

### Radio Jammer (3 events)

**Event 1: Police Scanner** — `events_day_dark.py`
```
Trigger: police pursuit/checkpoint event, has_item("Radio Jammer")
Narrative: "The RADIO JAMMER blankets police frequencies. Their radios 
           squawk static. You slip away in the confusion."
Effect: Escape police encounters without consequences.
```

**Event 2: Casino Surveillance** — `events_day_casino.py`
```
Trigger: casino security event, has_item("Radio Jammer")
Narrative: "You thumb the RADIO JAMMER. Security earpieces go dead. For 
           thirty blessed seconds, nobody is watching."
Effect: Escape casino surveillance/ban events.
```

**Event 3: Ambush Prevention** — `events_night.py`
```
Trigger: coordinated attack event, has_item("Radio Jammer")
Narrative: "The RADIO JAMMER kills their walkies. The ambush falls apart — 
           they can't coordinate without comms."
Effect: Neutralize planned night ambush.
```

### EMP Device (3 events)

**Event 1: Security System** — `events_day_dark.py`
```
Trigger: building/facility encounter, has_item("EMP Device")
Narrative: "The EMP DEVICE pulses. Every camera, lock, and alarm in the 
           building goes dark. You walk in like you own the place."
Effect: Bypass security in any building event. One-time use (consumed).
```

**Event 2: Vehicle Pursuit** — `events_car.py`
```
Trigger: chase event, has_item("EMP Device")
Narrative: "You toss the EMP DEVICE out the window. The pursuing car's 
           electronics die. It coasts to a stop."
Effect: End any vehicle pursuit instantly. Item consumed.
```

**Event 3: Electronics Market** — `events_day_people.py`
```
Trigger: tech/electronics event, has_item("EMP Device")
Narrative: "The vendor eyes your EMP DEVICE. 'That's military grade. Where 
           did you...' He offers three times its pawn value."
Effect: Sell for 3x pawn value if you choose.
```

### Distress Beacon (3 events)

**Event 1: Medical Emergency** — `events_illness.py`
```
Trigger: critical health event, has_item("Distress Beacon")
Narrative: "You activate the DISTRESS BEACON. Within minutes, a helicopter 
           appears on the horizon. Medical team incoming."
Effect: Emergency hospital trip with no travel penalty. Full heal.
```

**Event 2: Stranded in Wild** — `adventures.py`
```
Trigger: stranded in adventure zone, has_item("Distress Beacon")
Narrative: "The DISTRESS BEACON wails. Rangers triangulate your position. 
           You're pulled out within the hour."
Effect: Emergency exit from any adventure with no penalty.
```

**Event 3: Companion in Danger** — `events_day_companions.py`
```
Trigger: companion injury/danger, has_item("Distress Beacon")
Narrative: "You fire the DISTRESS BEACON for your companion. Help arrives 
           before you can count to a hundred."
Effect: Save companion from any danger event.
```

### Security Bypass (4 events)

**Event 1: Locked Building** — `events_day_items.py`
```
Trigger: locked door/container event, has_item("Security Bypass")
Narrative: "The SECURITY BYPASS makes quick work of the lock. Tumblers click, 
           the door swings open."
Effect: Access locked locations/containers (better than Lockpick Set).
```

**Event 2: Car Lockout** — `events_car.py`
```
Trigger: locked out of car event, has_item("Security Bypass")
Narrative: "The SECURITY BYPASS pops the car lock in seconds. No broken 
           windows, no locksmith fees."
Effect: Solve car lockout instantly and free.
```

**Event 3: Escape Detention** — `events_day_dark.py`
```
Trigger: captured/detained event, has_item("Security Bypass")
Narrative: "They didn't search well enough. The SECURITY BYPASS picks the 
           cuffs. You're gone before they notice."
Effect: Escape any capture/detention event.
```

**Event 4: Hidden Stash** — `events_day_survival.py`
```
Trigger: abandoned building exploration, has_item("Security Bypass")
Narrative: "Locked cabinet? Not anymore. The SECURITY BYPASS reveals a stash 
           someone left behind in a hurry."
Effect: Find hidden loot ($100–400) in exploration events.
```

---

## 37. Full Event Narrative Drafts — Disguises

**Target:** 7 items × 3–4 events each = ~24 new event blocks.

### Low-Profile Outfit (4 events)

**Event 1: Casino Recognition** — `events_day_wealth.py`
```
Trigger: recognized by casino/media, has_item("Low-Profile Outfit")
Narrative: "The LOW-PROFILE OUTFIT turns you invisible. The pit boss scans the 
           room and his eyes slide right over you."
Effect: Avoid casino recognition/ban events entirely.
```

**Event 2: Police Encounter** — `events_day_dark.py`
```
Trigger: police questioning, has_item("Low-Profile Outfit")
Narrative: "In the LOW-PROFILE OUTFIT, you look like a nobody. The officer 
           waves you through without a second glance."
Effect: Avoid police questioning/search.
```

**Event 3: Street Mugging** — `events_night.py`
```
Trigger: targeted mugging, has_item("Low-Profile Outfit")
Narrative: "The mugger passes you in the LOW-PROFILE OUTFIT. Who robs 
           someone who looks like they have nothing?"
Effect: Avoid night mugging — not worth the mugger's time.
```

**Event 4: Reporter Event** — `events_day_wealth.py`
```
Trigger: reporter/interview event, has_item("Low-Profile Outfit")
Narrative: "The reporter's photographer scans the crowd. Your LOW-PROFILE 
           OUTFIT makes you part of the background."
Effect: Escape media attention.
```

### Beach Bum Disguise (3 events)

**Event 1: Social Event Infiltration** — `events_day_people.py`
```
Trigger: exclusive party/event, has_item("Beach Bum Disguise")
Narrative: "In the BEACH BUM DISGUISE, you look harmless. The doorman lets 
           you in out of pity."
Effect: Access exclusive social events through the "harmless" angle.
```

**Event 2: Heat Wave** — `events_day_survival.py`
```
Trigger: extreme heat event, has_item("Beach Bum Disguise")
Narrative: "The BEACH BUM DISGUISE wasn't just for looks — the sunscreen 
           keeps you cool when everyone else is melting."
Effect: Immune to heat wave damage.
```

**Event 3: Charity Event** — `events_day_people.py`
```
Trigger: charity/donation event, has_item("Beach Bum Disguise")
Narrative: "Someone hands you $50. 'You look like you need this more.' The 
           BEACH BUM DISGUISE is too convincing."
Effect: Receive free money from charity-minded NPCs.
```

### Gas Mask (3 events)

**Event 1: Toxic Spill** — `events_day_survival.py`
```
Trigger: chemical/toxic event, has_item("Gas Mask")
Narrative: "The GAS MASK filters the toxic fumes. You breathe pine-scented 
           air while everyone else evacuates."
Effect: Immune to all poison/toxic/gas events.
```

**Event 2: Fire/Smoke Event** — `events_day_dark.py`
```
Trigger: building fire/smoke, has_item("Gas Mask")
Narrative: "Smoke fills the room. You pull on the GAS MASK and walk through 
           like it's a light fog."
Effect: Navigate smoke/fire events without health damage.
```

**Event 3: Swamp Adventure** — `adventures.py`
```
Trigger: swamp zone gas hazard, has_item("Gas Mask")
Narrative: "Swamp gas that would knock you out rolls harmlessly past the 
           GAS MASK's filters."
Effect: Immune to swamp gas penalties in adventure zones.
```

### Storm Suit (3 events)

**Event 1: Hurricane/Storm Event** — `events_day_survival.py`
```
Trigger: severe weather, has_item("Storm Suit")
Narrative: "The STORM SUIT holds against the hurricane-force winds. Rain 
           bounces off. You stand while others crawl."
Effect: Immune to all rain/storm/weather damage events.
```

**Event 2: Flash Flood** — `events_car.py`
```
Trigger: flood/water crossing, has_item("Storm Suit")
Narrative: "You wade through the flood in the STORM SUIT. Dry from neck to 
           ankle. The car is another story."
Effect: No health damage from flood events (car may still take damage).
```

**Event 3: Cold Night** — `events_night.py`
```
Trigger: cold/freezing night, has_item("Storm Suit")
Narrative: "The STORM SUIT traps your body heat. The temperature drops but 
           you barely notice."
Effect: Immune to nighttime cold damage.
```

### Brass Knuckles (4 events)

**Event 1: Bar Fight** — `events_day_people.py`
```
Trigger: confrontation/fight, has_item("Brass Knuckles")
Narrative: "Your fist connects through the BRASS KNUCKLES. One punch. 
           The other guy sits down and reconsiders his life."
Effect: Win any physical confrontation in one hit.
```

**Event 2: Mugging Defense** — `events_day_dark.py`
```
Trigger: mugging/robbery, has_item("Brass Knuckles")
Narrative: "The mugger sees the BRASS KNUCKLES and decides today isn't his 
           day. He backs off without a word."
Effect: Mugger leaves immediately — deterrence effect.
```

**Event 3: Animal Attack** — `events_day_animals.py`
```
Trigger: aggressive animal, has_item("Brass Knuckles")
Narrative: "You swing the BRASS KNUCKLES. The animal yelps and scatters. 
           Not your proudest moment, but you're alive."
Effect: Defend against animal attacks.
```

**Event 4: Adventure Combat** — `adventures.py`
```
Trigger: combat encounter in adventure zone, has_item("Brass Knuckles")
Narrative: "The BRASS KNUCKLES crack against your opponent. They go down 
           hard and stay down."
Effect: +50% combat advantage in adventure encounters.
```

### Gentleman's Charm (3 events)

**Event 1: VIP Access** — `events_day_wealth.py`
```
Trigger: exclusive venue/VIP event, has_item("Gentleman's Charm")
Narrative: "The GENTLEMAN'S CHARM precedes you — cologne and silk. The rope 
           parts. The door opens. You belong here."
Effect: Automatic VIP access to all exclusive events.
```

**Event 2: Negotiation** — `events_day_people.py`
```
Trigger: business deal/negotiation, has_item("Gentleman's Charm")
Narrative: "You produce the silk handkerchief from the GENTLEMAN'S CHARM. 
           Something about the gesture makes them offer better terms."
Effect: +30% better deal in any negotiation/purchase event.
```

**Event 3: Romance/Social** — `events_day_people.py`
```
Trigger: romantic interest/social bonding, has_item("Gentleman's Charm")
Narrative: "The GENTLEMAN'S CHARM does the talking before you open your 
           mouth. Cologne, silk, and eye contact. Irresistible."
Effect: Auto-succeed social charm checks.
```

### Forged Documents (4 events)

**Event 1: Identity Check** — `events_day_dark.py`
```
Trigger: ID check/verification, has_item("Forged Documents")
Narrative: "You hand over the FORGED DOCUMENTS. The officer studies them, 
           nods, and waves you through. Flawless."
Effect: Pass any identity check/verification event.
```

**Event 2: Hospital/Medical** — `events_illness.py`
```
Trigger: medical treatment needed, has_item("Forged Documents")
Narrative: "The FORGED DOCUMENTS list you as a veteran. The hospital treats 
           you at no charge."
Effect: Free medical treatment.
```

**Event 3: Bank/Financial** — `events_day_wealth.py`
```
Trigger: banking/financial event, has_item("Forged Documents")
Narrative: "With the FORGED DOCUMENTS, the bank sees a clean credit history. 
           Loan approved. No questions."
Effect: Better financial terms, loan approval events.
```

**Event 4: Border/Checkpoint** — `events_day_survival.py`
```
Trigger: checkpoint/restricted area, has_item("Forged Documents")
Narrative: "The FORGED DOCUMENTS clear you through the checkpoint. The guard 
           even salutes."
Effect: Bypass any restricted area/checkpoint event.
```

---

## 38. Full Event Narrative Drafts — Tonics & Consumables

**Target:** 9 items × 3 events each = ~27 new event blocks. Many consumables are **single-use** (consumed on trigger).

### Antacid Brew (3 events)

**Event 1: Food Poisoning** — `events_illness.py`
```
Trigger: food poisoning/nausea event, has_item("Antacid Brew")
Narrative: "You chug the ANTACID BREW. The fizzing settles your stomach 
           instantly. Crisis averted."
Effect: Cure food poisoning. Item consumed.
```

**Event 2: Bad Food at Social Event** — `events_day_people.py`
```
Trigger: social dinner/food event, has_item("Antacid Brew")
Narrative: "The shrimp was off. You feel it coming. One swig of ANTACID BREW 
           and you're back at the table like nothing happened."
Effect: Avoid illness from bad food. Item consumed.
```

**Event 3: Stress Stomach** — `events_day_dark.py`
```
Trigger: high-stress event aftermath, has_item("Antacid Brew")
Narrative: "The adrenaline fades and your stomach revolts. The ANTACID BREW 
           calms everything down."
Effect: Prevent stress-related health loss. Item consumed.
```

### Trail Mix Bomb (3 events)

**Event 1: Animal Distraction** — `events_day_animals.py`
```
Trigger: aggressive animal encounter, has_item("Trail Mix Bomb")
Narrative: "You light the TRAIL MIX BOMB and toss it. Seeds scatter in a 
           fiery burst. The animal bolts in the other direction."
Effect: Scare away any aggressive animal. Item consumed.
```

**Event 2: Crowd Distraction** — `events_day_people.py`
```
Trigger: need to create a distraction, has_item("Trail Mix Bomb")
Narrative: "The TRAIL MIX BOMB pops and scatters burning seeds. Everyone 
           turns to look. You slip away in the chaos."
Effect: Create distraction to escape social situations. Item consumed.
```

**Event 3: Night Defense** — `events_night.py`
```
Trigger: night intruder/threat, has_item("Trail Mix Bomb")
Narrative: "A TRAIL MIX BOMB tossed toward the sound. Sparks and seeds 
           explode. Whatever was out there isn't anymore."
Effect: Repel night threats. Item consumed.
```

### Animal Bait (3 events)

**Event 1: Companion Recruitment** — `events_day_companions.py`
```
Trigger: wild animal appears as potential companion, has_item("Animal Bait")
Narrative: "You set out the ANIMAL BAIT. The creature approaches cautiously, 
           sniffs... and stays. You've made a friend."
Effect: Guarantee companion recruitment from wild animal events.
```

**Event 2: Hunting** — `events_day_survival.py`
```
Trigger: foraging/hunting event, has_item("Animal Bait")
Narrative: "The ANIMAL BAIT draws prey to you. No tracking needed — dinner 
           walks right up."
Effect: Guaranteed food from hunting events. Item consumed.
```

**Event 3: Animal Threat Redirect** — `events_day_animals.py`
```
Trigger: predator approaching, has_item("Animal Bait")
Narrative: "You toss the ANIMAL BAIT the opposite direction. The predator 
           follows the scent away from you."
Effect: Redirect predator attention. Item consumed.
```

### Stink Bomb (3 events)

**Event 1: Mugging Defense** — `events_day_dark.py`
```
Trigger: mugging/assault, has_item("Stink Bomb")
Narrative: "You crack the STINK BOMB at your feet. The mugger gags, eyes 
           streaming. You walk away untouched."
Effect: Escape any mugging without losing items/money. Item consumed.
```

**Event 2: Building Clearance** — `events_day_survival.py`
```
Trigger: need to clear a building/room, has_item("Stink Bomb")
Narrative: "The STINK BOMB clears the room in seconds. Everyone evacuates. 
           You have the place to yourself."
Effect: Clear any occupied building for looting/escape. Item consumed.
```

**Event 3: Pest Removal** — `events_day_animals.py`
```
Trigger: pest infestation, has_item("Stink Bomb")
Narrative: "The STINK BOMB's chemical assault drives out every rodent, bug, 
           and critter in a fifty-foot radius."
Effect: Clear pest infestation (alternative to Pest Control). Item consumed.
```

### Voice Soother (3 events)

**Event 1: Negotiation Boost** — `events_day_people.py`
```
Trigger: negotiation/persuasion event, has_item("Voice Soother")
Narrative: "One sip of VOICE SOOTHER and your words come out smooth as honey. 
           The other party melts into agreement."
Effect: +50% better negotiation outcomes. Item consumed.
```

**Event 2: Performance Event** — `events_day_people.py`
```
Trigger: performance/speech/karaoke event, has_item("Voice Soother")
Narrative: "The VOICE SOOTHER does its magic. You sing/speak like an angel. 
           The crowd erupts."
Effect: Guaranteed success in any performance event. Item consumed.
```

**Event 3: Companion Calming** — `events_day_companions.py`
```
Trigger: scared/upset companion, has_item("Voice Soother")
Narrative: "Your soothed voice calms your companion. The VOICE SOOTHER 
           turns your words into a lullaby."
Effect: Calm companion, restore companion happiness. Item consumed.
```

### Outdoor Shield (3 events)

**Event 1: Extreme UV** — `events_day_survival.py`
```
Trigger: sunburn/UV event, has_item("Outdoor Shield")
Narrative: "The OUTDOOR SHIELD absorbs the sun and repels the bugs. You hike 
           through the worst of it without a scratch."
Effect: Immune to sunburn AND bug-bite events.
```

**Event 2: Swamp Bugs** — `adventures.py`
```
Trigger: bug swarm in adventure zone, has_item("Outdoor Shield")
Narrative: "Mosquitoes the size of grapes bounce off the OUTDOOR SHIELD's 
           chemical barrier. Not a single bite."
Effect: Immune to bug swarm penalties in adventures.
```

**Event 3: Long Hike** — `events_day_survival.py`
```
Trigger: extended travel/hike event, has_item("Outdoor Shield")
Narrative: "Sun beats down, bugs swarm, but the OUTDOOR SHIELD has you 
           covered on all fronts."
Effect: No health damage from extended outdoor travel.
```

### Cool Down Kit (3 events)

**Event 1: Heatstroke Prevention** — `events_day_survival.py`
```
Trigger: extreme heat/heatstroke event, has_item("Cool Down Kit")
Narrative: "The COOL DOWN KIT's cold compress and sunscreen stop the Heat 
           before it starts. You feel almost refreshed."
Effect: Immune to heatstroke/heat damage. Item consumed.
```

**Event 2: Desert/Arid Adventure** — `adventures.py`
```
Trigger: desert/arid zone, has_item("Cool Down Kit")
Narrative: "You apply the COOL DOWN KIT. The desert heat registers as a 
           mild annoyance rather than a death sentence."
Effect: Reduced damage from desert/arid adventure zones.
```

**Event 3: Hot Car** — `events_car.py`
```
Trigger: car overheating / hot car interior, has_item("Cool Down Kit")
Narrative: "You pour the COOL DOWN KIT's water over your head and the 
           engine. Both temperatures drop."
Effect: Reduce car overheat damage AND avoid health penalty.
```

### Smoke Flare (3 events)

**Event 1: Rescue Signal** — `events_day_survival.py`
```
Trigger: stranded/lost event, has_item("Smoke Flare")
Narrative: "The SMOKE FLARE sends a column of black smoke skyward. Within 
           an hour, someone finds you."
Effect: Guaranteed rescue from stranded events. Item consumed.
```

**Event 2: Pursuit Escape** — `events_day_dark.py`
```
Trigger: being chased/pursued, has_item("Smoke Flare")
Narrative: "You drop the SMOKE FLARE behind you. Thick smoke fills the 
           alley. Your pursuers cough and stumble. You're gone."
Effect: Escape any pursuit event. Item consumed.
```

**Event 3: Night Signal** — `events_night.py`
```
Trigger: night rescue/signal event, has_item("Smoke Flare")
Narrative: "The SMOKE FLARE lights the night with an orange glow. In the 
           darkness, it's visible for miles."
Effect: Signal for help during night events. Item consumed.
```

### Vermin Bomb (3 events)

**Event 1: Rat Infestation** — `events_day_survival.py`
```
Trigger: rodent/vermin infestation, has_item("Vermin Bomb")
Narrative: "The VERMIN BOMB detonates in a cloud of chemical fury. Every rat 
           within earshot abandons ship."
Effect: Instantly clear any pest/vermin event. Item consumed.
```

**Event 2: Car Pests** — `events_car.py`
```
Trigger: pests in car (mice eating wires, etc.), has_item("Vermin Bomb")
Narrative: "You set off the VERMIN BOMB under the hood. Mice, spiders, and 
           something you don't want to identify flee the engine bay."
Effect: Clear car pest damage. Item consumed.
```

**Event 3: Storage Clearing** — `events_day_items.py`
```
Trigger: infested storage/cache found, has_item("Vermin Bomb")
Narrative: "The storage unit is crawling. One VERMIN BOMB later, it's clear 
           enough to loot. The smell lingers, though."
Effect: Access infested containers/storage for loot. Item consumed.
```

---

## 39. Full Event Narrative Drafts — Dark Arts

**Target:** 5 items × 3–4 events each = ~17 event blocks. Dark Arts items have surreal, morally gray effects.

### Eldritch Candle (4 events)

**Event 1: Séance at Midnight** — `events_night.py`
```
Trigger: supernatural night event, has_item("Eldritch Candle")
Narrative: "You light the ELDRITCH CANDLE. The flame burns green. Shadows 
           lean toward it, whispering truths you shouldn't know."
Effect: +large sanity OR -large sanity (50/50). Reveals secret info about upcoming event.
```

**Event 2: Devil's Bargain** — `events_day_dark.py`
```
Trigger: demonic/devil deal event, has_item("Eldritch Candle")
Narrative: "The ELDRITCH CANDLE flares. The devil pauses. 'You've read the 
           book,' he says. 'The terms change.'"
Effect: Better devil deal terms — reduced cost by half.
```

**Event 3: Haunted Location** — `adventures.py`
```
Trigger: haunted zone encounter, has_item("Eldritch Candle")
Narrative: "The ELDRITCH CANDLE's glow makes the ghosts visible. They're not 
           hostile — they're trapped. You could free them."
Effect: Peaceful resolution to haunted encounters. +karma.
```

**Event 4: Blood Moon** — `events_day_dark.py`
```
Trigger: blood moon event, has_item("Eldritch Candle")
Narrative: "Under the blood moon, the ELDRITCH CANDLE burns crimson. Power 
           flows into you from somewhere ancient."
Effect: Temporary stat boost during blood moon events.
```

### Binding Portrait (3 events)

**Event 1: NPC Betrayal Prevention** — `events_day_people.py`
```
Trigger: NPC betrayal/scam event, has_item("Binding Portrait")
Narrative: "You show the BINDING PORTRAIT. The NPC's face drains of color. 
           'I'll behave,' they whisper. The portrait's eyes glow."
Effect: Prevent any NPC betrayal. Target NPC becomes cooperative.
```

**Event 2: Companion Loyalty** — `events_day_companions.py`
```
Trigger: companion leaving/disloyalty, has_item("Binding Portrait")
Narrative: "The BINDING PORTRAIT pulses. Your companion's eyes go distant 
           for a moment, then clear. 'I'm staying,' they say."
Effect: Prevent companion departure (morally questionable).
```

**Event 3: Surreal Identity** — `events_day_surreal.py`
```
Trigger: identity crisis / mirror event, has_item("Binding Portrait")
Narrative: "The BINDING PORTRAIT shows your face — but younger. Happier. 
           Is that who you were, or who you'll become?"
Effect: +sanity if low, -sanity if already high. Reality warps.
```

### Blackmail Letter (4 events)

**Event 1: Corrupt Official** — `events_day_people.py`
```
Trigger: authority figure event, has_item("Blackmail Letter")
Narrative: "You slide the BLACKMAIL LETTER across the table. The official 
           reads it, turns pale, and asks what you want."
Effect: Get any favor from authority figures — free pass, money, information.
```

**Event 2: Casino Leverage** — `events_day_casino.py`
```
Trigger: casino management event, has_item("Blackmail Letter")
Narrative: "You mention the BLACKMAIL LETTER. The casino manager suddenly 
           remembers that ban was a mistake."
Effect: Reverse casino bans, get VIP treatment.
```

**Event 3: Debt Forgiveness** — `events_day_wealth.py`
```
Trigger: debt collection event, has_item("Blackmail Letter")
Narrative: "The debt collector opens the BLACKMAIL LETTER. Long pause. 'Your 
           debt is cleared,' they say quietly."
Effect: Clear any debt event. Item consumed (evidence used up).
```

**Event 4: Gang/Criminal Encounter** — `events_day_dark.py`
```
Trigger: gang/criminal threat, has_item("Blackmail Letter")
Narrative: "You wave the BLACKMAIL LETTER. The gang leader's bravado 
           evaporates. 'What do you want?' Leverage is everything."
Effect: De-escalate any criminal confrontation.
```

### Devil's Deck (3 events)

**Event 1: Supernatural Poker** — `events_night.py`
```
Trigger: gambling event at night, has_item("Devil's Deck")
Narrative: "You deal from the DEVIL'S DECK. The cards burn faintly. Your 
           opponents' hands are always worse than yours."
Effect: Guaranteed gambling win. But +1 dark karma.
```

**Event 2: Fortune Telling** — `events_day_surreal.py`
```
Trigger: fortune teller/mystic event, has_item("Devil's Deck")
Narrative: "The fortune teller reaches for her cards but stops when she sees 
           the DEVIL'S DECK. 'Those shouldn't exist,' she whispers."
Effect: Get an extremely detailed (and accurate) future reading.
```

**Event 3: Cursed Gamble** — `events_day_casino.py`
```
Trigger: risky bet/all-in situation, has_item("Devil's Deck")
Narrative: "The DEVIL'S DECK warms in your pocket. You feel impossibly 
           confident. You go all in. The cards fall your way."
Effect: Win any high-stakes gamble. But future bad luck event queued.
```

### Fortune Cards (3 events)

**Event 1: Daily Prediction** — `events_day_items.py`
```
Trigger: morning/start of day, has_item("Fortune Cards")
Narrative: "You draw a FORTUNE CARD. It shows [random positive/negative 
           omen]. Today's luck tilts accordingly."
Effect: Small random buff OR debuff for the day. Fun flavor.
```

**Event 2: Decision Helper** — `events_day_people.py`
```
Trigger: difficult choice event, has_item("Fortune Cards")
Narrative: "You flip a FORTUNE CARD for guidance. The card shows [relevant 
           symbol]. The choice becomes clearer."
Effect: Reveal which choice has better outcome in choice events.
```

**Event 3: Merchant Mystique** — `events_day_people.py`
```
Trigger: shop/merchant event, has_item("Fortune Cards")
Narrative: "You offer to read the merchant's fortune with the FORTUNE CARDS. 
           They're so impressed they give you a discount."
Effect: 20% discount at shops for the day.
```

---

## 40. Full Event Narrative Drafts — Luxury Crafts

**Target:** 7 items × 3 events each = ~21 event blocks. Luxury items excel in social, wealth, and reputation scenarios.

### Kingpin Look (3 events)

**Event 1: VIP Casino Treatment** — `events_day_casino.py`
```
Trigger: casino entrance/visit, has_item("Kingpin Look")
Narrative: "Gold chain, cigar — the KINGPIN LOOK commands the room. The 
           dealer nods. The pit boss offers you the high-roller table."
Effect: Automatic high-roller access. Better table limits.
```

**Event 2: Street Cred** — `events_day_dark.py`
```
Trigger: gang/criminal encounter, has_item("Kingpin Look")
Narrative: "The KINGPIN LOOK makes them rethink. You don't look like a 
           victim — you look like the boss. They nod and step aside."
Effect: Intimidate criminals. Avoid mugging/robbery through respect.
```

**Event 3: Business Meeting** — `events_day_people.py`
```
Trigger: business/investment event, has_item("Kingpin Look")
Narrative: "You walk in with the KINGPIN LOOK. Before you say a word, they 
           assume you're the money. Better seat, better terms."
Effect: +40% better deals in business/investment events.
```

### Enchanted Vintage (3 events)

**Event 1: Social Bonding** — `events_day_people.py`
```
Trigger: social gathering/party, has_item("Enchanted Vintage")
Narrative: "You uncork the ENCHANTED VINTAGE. The first sip makes time slow. 
           Everyone at the table becomes your best friend."
Effect: Maximum social bonding at any gathering. +NPC loyalty.
```

**Event 2: Celebration** — `events_day_wealth.py`
```
Trigger: big win/celebration event, has_item("Enchanted Vintage")
Narrative: "You toast with the ENCHANTED VINTAGE. The silver flask catches 
           the light. This is what winning tastes like."
Effect: +sanity, +happiness. Bonus celebration reward.
```

**Event 3: Companion Bonding** — `events_day_companions.py`
```
Trigger: companion rest/bonding, has_item("Enchanted Vintage")
Narrative: "You share the ENCHANTED VINTAGE with your companion. The wine 
           never seems to run out. Neither does the conversation."
Effect: Max companion happiness boost. 
```

### Heirloom Set (3 events)

**Event 1: Pawn Premium** — `locations.py` (Grimy Gus)
```
Trigger: pawning any item while holding Heirloom Set
Narrative: "Gus spots the HEIRLOOM SET in your pocket. 'You've got taste,' 
           he says. 'I'll add ten percent for a fellow collector.'"
Effect: +10% pawn value on ALL items while holding Heirloom Set.
```

**Event 2: Estate Sale** — `events_day_wealth.py`
```
Trigger: auction/estate sale event, has_item("Heirloom Set")
Narrative: "The HEIRLOOM SET catches the auctioneer's eye. 'Ah, a fellow 
           connoisseur.' You're invited to the private viewing."
Effect: Access to exclusive sale items, better prices.
```

**Event 3: Bank Trust** — `events_day_people.py`
```
Trigger: financial/banking event, has_item("Heirloom Set")
Narrative: "You produce the HEIRLOOM SET's pen to sign papers. The bank 
           manager's demeanor shifts — you're old money now."
Effect: Better loan terms, higher credit limits.
```

### Aristocrat's Touch (3 events)

**Event 1: Elegance Check** — `events_day_people.py`
```
Trigger: elegance/luxury social event, has_item("Aristocrat's Touch")
Narrative: "The ARISTOCRAT'S TOUCH — silk and leather at your fingertips. 
           You don't just fit in at the gala. You own it."
Effect: Joins existing elegance OR group. Top-tier social access.
```

**Event 2: Cold Weather Survival** — `events_day_survival.py`
```
Trigger: freezing/cold event, has_item("Aristocrat's Touch")
Narrative: "The gloves from the ARISTOCRAT'S TOUCH keep your fingers warm 
           and nimble. The silk handkerchief wraps around your neck."
Effect: Immune to cold weather damage (elegance + function).
```

**Event 3: High Society Infiltration** — `events_day_wealth.py`
```
Trigger: exclusive party/gala, has_item("Aristocrat's Touch")
Narrative: "With the ARISTOCRAT'S TOUCH, every handshake is precise, every 
           gesture deliberate. You belong among the elite."
Effect: Access VIP events, bonus social outcomes.
```

### Power Move Kit (3 events)

**Event 1: Intimidation** — `events_day_dark.py`
```
Trigger: confrontation/threat, has_item("Power Move Kit")
Narrative: "You snap the POWER MOVE KIT's lighter. Light the cigar. The 
           flame reflects in their eyes. Nobody makes the first move."
Effect: De-escalate confrontations through pure power presence.
```

**Event 2: Deal Closing** — `events_day_people.py`
```
Trigger: negotiation climax, has_item("Power Move Kit")
Narrative: "You offer a cigar from the POWER MOVE KIT. The lighter clicks. 
           Smoke rises. 'We have a deal,' they say."
Effect: Guarantee successful deal closure.
```

**Event 3: Night Campfire** — `events_night.py`
```
Trigger: night rest/camp, has_item("Power Move Kit")
Narrative: "The POWER MOVE KIT's lighter starts the fire. Cigar in hand, 
           stars above. For one night, everything is under control."
Effect: +sanity restoration at night. Peaceful night guarantee.
```

### Animal Magnetism (3 events)

**Event 1: Companion Attraction** — `events_day_companions.py`
```
Trigger: new companion opportunity, has_item("Animal Magnetism")
Narrative: "The ANIMAL MAGNETISM draws the creature closer. The cologne's 
           leather scent is... comforting? It nuzzles your hand."
Effect: +50% companion recruitment chance.
```

**Event 2: NPC Charm** — `events_day_people.py`
```
Trigger: NPC interaction, has_item("Animal Magnetism")
Narrative: "Something about the ANIMAL MAGNETISM — the cologne, the gloves — 
           makes people trust you instantly."
Effect: Better NPC interaction outcomes across the board.
```

**Event 3: Predator Pacification** — `events_day_animals.py`
```
Trigger: predator encounter, has_item("Animal Magnetism")
Narrative: "The predator stops. Sniffs. The ANIMAL MAGNETISM confuses its 
           instincts. You smell like... one of them."
Effect: Pacify predator encounters without combat.
```

### Luck Totem (3 events)

**Event 1: Gambling Boost** — `events_day_casino.py`
```
Trigger: gambling event, has_item("Luck Totem")
Narrative: "The LUCK TOTEM hums against your chest. The dice bounce your way. 
           The dealer busts. Again and again."
Effect: +15% gambling luck for the session.
```

**Event 2: Loot Discovery** — `events_day_items.py`
```
Trigger: search/loot event, has_item("Luck Totem")
Narrative: "The LUCK TOTEM pulses warm. You reach into the junk pile and pull 
           out something valuable. Every time."
Effect: Better loot quality from search events.
```

**Event 3: Lottery Effect** — `events_day_numbers.py`
```
Trigger: numbers/lottery/chance event, has_item("Luck Totem")
Narrative: "The LUCK TOTEM vibrates. The numbers align. Not jackpot, but 
           close enough. Much closer than random."
Effect: Better lottery/numbers event outcomes.
```

---

## 41. Full Event Narrative Drafts — Vehicle Upgrades

**Target:** 5 items × 3 events each = ~15 event blocks. All trigger in car-related scenarios.

### Tire Ready Kit (3 events)

**Event 1: Flat Tire** — `events_car.py`
```
Trigger: flat tire event, has_item("Tire Ready Kit")
Narrative: "The TIRE READY KIT makes this a two-minute job. Jack clicks, tire 
           rolls, done. You're back on the road before your coffee cools."
Effect: Instant flat tire fix. No time/money penalty.
```

**Event 2: Adventure Zone Road** — `adventures.py`
```
Trigger: rough road in adventure zone, has_item("Tire Ready Kit")
Narrative: "The rough road shreds a tire. But the TIRE READY KIT is right 
           there. Quick swap and you barely slow down."
Effect: Avoid tire damage penalty in adventures.
```

**Event 3: Roadside Assistance** — `events_day_people.py`
```
Trigger: stranded motorist event, has_item("Tire Ready Kit")
Narrative: "A stranded motorist waves you down. Your TIRE READY KIT fixes 
           their flat in minutes. They pay you $75."
Effect: Help NPC for cash reward + karma.
```

### Power Grid (3 events)

**Event 1: Dead Battery** — `events_car.py`
```
Trigger: dead battery event, has_item("Power Grid")
Narrative: "The POWER GRID self-diagnoses and jumps the battery. Fuses intact, 
           power stable. Your car purrs to life."
Effect: Instant battery fix. No time/money penalty.
```

**Event 2: Electrical Failure** — `events_car.py`
```
Trigger: electrical system failure, has_item("Power Grid")
Narrative: "The POWER GRID re-routes around the blown circuit. Headlights 
           flicker back on. Dash lights glow green."
Effect: Fix any electrical car issue automatically.
```

**Event 3: Emergency Power** — `events_night.py`
```
Trigger: night without light/power, has_item("Power Grid")
Narrative: "You hook the POWER GRID to a camp light. Warm glow fills the 
           night. Your car battery doesn't even notice."
Effect: Provide light and power at night camps.
```

### Miracle Lube (3 events)

**Event 1: Engine Trouble** — `events_car.py`
```
Trigger: engine grinding/squeaking, has_item("Miracle Lube")
Narrative: "A squirt of MIRACLE LUBE and the grinding stops. The engine 
           purrs. Whatever was wrong decided not to be."
Effect: Fix engine noise/trouble events. Prevent breakdown.
```

**Event 2: Door/Lock Maintenance** — `events_day_survival.py`
```
Trigger: stuck/jammed event, has_item("Miracle Lube")
Narrative: "The MIRACLE LUBE frees the mechanism instantly. Squeak — click — 
           smooth. Works on anything with moving parts."
Effect: Fix any mechanical jam/stuck event.
```

**Event 3: Car Maintenance Day** — `events_car.py`
```
Trigger: general car maintenance, has_item("Miracle Lube")
Narrative: "You give the whole car the MIRACLE LUBE treatment. Doors, hinges, 
           wheels, engine. Everything moves like new."
Effect: Full car condition boost during maintenance events.
```

### Mobile Workshop (3 events)

**Event 1: Major Breakdown** — `events_car.py`
```
Trigger: major car repair needed, has_item("Mobile Workshop")
Narrative: "The MOBILE WORKSHOP has everything you need. Wrench, tape, pliers, 
           and a can-do attitude. Full repair, roadside."
Effect: Fix any car breakdown without tow/mechanic. No cost.
```

**Event 2: Build/Craft on the Road** — `events_day_survival.py`
```
Trigger: need to build/repair in the field, has_item("Mobile Workshop")
Narrative: "The MOBILE WORKSHOP unfolds like a surgeon's kit. Whatever's 
           broken, you have the tools to fix it."
Effect: Perform field repairs on any item/structure.
```

**Event 3: Help Another Driver** — `events_day_people.py`
```
Trigger: broken-down motorist, has_item("Mobile Workshop")
Narrative: "You pull out the MOBILE WORKSHOP. Thirty minutes later, their car 
           runs better than it did new. They insist on paying."
Effect: Help NPC motorist. Earn $100–200 + karma.
```

### Pursuit Package (3 events)

**Event 1: Chase Sequence** — `events_day_dark.py`
```
Trigger: chase/pursuit event, has_item("Pursuit Package")
Narrative: "Running shoes hit pavement, whistle coordinates the pursuit. 
           The PURSUIT PACKAGE turns you into a tracking machine."
Effect: Guarantee catching fleeing targets in chase events.
```

**Event 2: Lost Pet/Animal** — `events_day_animals.py`
```
Trigger: lost animal event, has_item("Pursuit Package")
Narrative: "The PURSUIT PACKAGE's whistle calls, your shoes close the gap. 
           The lost animal turns, sees you, and comes running."
Effect: Guarantee animal recovery in lost pet events.
```

**Event 3: Morning Run Event** — `events_day_survival.py`
```
Trigger: exercise/health event, has_item("Pursuit Package")
Narrative: "Morning run in the PURSUIT PACKAGE shoes. The whistle keeps tempo. 
           Five miles feels like one. Health restored."
Effect: Bonus health restoration from exercise events.
```

---

## 42. Full Event Narrative Drafts — Tier 2 Items

**Target:** 25 items × 3 events each = ~75 event blocks. Tier 2 items are powerful combinations that outperform their components.

### Tier 2 Weapons (4 items)

**Assassin's Kit** (Shiv + Pepper Spray) — 3 events
```
Event 1 — events_day_dark.py: Ambush defense. "The ASSASSIN'S KIT — spray 
  to blind, blade to finish. The attacker never stood a chance." Win any combat.
Event 2 — events_night.py: Night stalker. "Spray in the dark, blade follows 
  the sound. The ASSASSIN'S KIT is silent and brutal." Eliminate night threats.
Event 3 — adventures.py: Adventure combat. "The ASSASSIN'S KIT gives you a 
  decisive edge. Blind, strike, move. Professional." +75% combat advantage.
```

**Fire Launcher** (Slingshot + Road Flare Torch) — 3 events
```
Event 1 — events_day_dark.py: Siege defense. "The FIRE LAUNCHER hurls 
  burning projectiles. The fence line becomes a wall of fire." Area denial.
Event 2 — events_night.py: Night signal. "Launch a flaming rock skyward with 
  the FIRE LAUNCHER. The sky lights up. Help is coming." Super-signal.
Event 3 — events_day_animals.py: Animal deterrent. "A flaming stone from the 
  FIRE LAUNCHER sends the pack running. Nothing charges into fire." Repel packs.
```

**Tear Gas** (Pepper Spray + Stink Bomb) — 3 events
```
Event 1 — events_day_dark.py: Crowd/gang dispersal. "One TEAR GAS canister 
  clears the street. Eyes streaming, lungs burning. They scatter." Disperse groups.
Event 2 — events_day_people.py: Escape panic. "You pop the TEAR GAS. 
  Everyone evacuates. In the chaos, you walk out the back." Emergency escape.
Event 3 — events_day_survival.py: Building clearance. "TEAR GAS through the 
  window. Wait two minutes. Walk in. The building is yours." Commandeer spaces.
```

**Street Fighter Set** (Shiv + Brass Knuckles) — 3 events
```
Event 1 — events_day_dark.py: One-on-one combat. "STREET FIGHTER SET — blade 
  and bruise. The fight ends before the other guy processes what happened." Instant win.
Event 2 — events_day_people.py: Reputation. "Word spreads about the STREET 
  FIGHTER SET. Nobody picks a fight with you anymore." Permanent intimidation.
Event 3 — adventures.py: Boss fight. "Triple-ingredient advantage: blade 
  cuts, fist breaks. The STREET FIGHTER SET is a one-person army." Adventure boss win.
```

### Tier 2 Survival (5 items)

**Survival Bivouac** (Emergency Blanket + Fire Starter Kit) — 3 events
```
Event 1 — events_night.py: Night shelter. "The SURVIVAL BIVOUAC deploys in 
  minutes. Warm, dry, safe. The night passes peacefully." Perfect night rest.
Event 2 — events_day_survival.py: Storm shelter. "Rain hammers down. The 
  SURVIVAL BIVOUAC sheds it all. You sit by the fire, bone dry." Storm immunity.
Event 3 — adventures.py: Adventure camp. "SURVIVAL BIVOUAC at the zone edge. 
  Full rest, hot meal. You enter the zone at peak condition." +health before adventure.
```

**Hydration Station** (Water Purifier + Rain Collector) — 3 events
```
Event 1 — events_day_survival.py: Drought event. "The HYDRATION STATION pulls 
  moisture from the air. Clean water, even in drought." Immune to dehydration.
Event 2 — adventures.py: Desert zone. "The HYDRATION STATION collects dew at 
  dawn. You have water when everyone else is parched." Desert zone advantage.
Event 3 — events_illness.py: Waterborne illness. "The HYDRATION STATION 
  catches the pathogen. Your water stays pure." Block waterborne disease.
```

**Provider's Kit** (Snare Trap + Fishing Rod) — 3 events
```
Event 1 — events_day_survival.py: Starvation event. "The PROVIDER'S KIT feeds 
  you from land and sea. Rabbit in the trap, fish on the line." Immune to starvation.
Event 2 — events_day_companions.py: Feed companion. "The PROVIDER'S KIT 
  provides for two. Companion eats well." Keep companion fed.
Event 3 — adventures.py: Long expedition. "The PROVIDER'S KIT sustains you 
  through the longest expeditions. Food is never a concern." No food penalty in adventures.
```

**Fortified Perimeter** (Improvised Trap + Car Alarm Rigging) — 3 events
```
Event 1 — events_night.py: Night defense. "The FORTIFIED PERIMETER activates 
  at dusk. Alarms, traps, tripwires. Nothing gets close." Immune to night intrusions.
Event 2 — events_day_dark.py: Ambush prevention. "The FORTIFIED PERIMETER 
  catches the scout. The ambush is revealed before it starts." Prevent ambushes.
Event 3 — events_day_survival.py: Camp security. "Animals, thieves, weather — 
  the FORTIFIED PERIMETER handles them all." Immune to camp raiding events.
```

**All-Weather Armor** (Storm Suit + Outdoor Shield) — 3 events
```
Event 1 — events_day_survival.py: Any weather event. "ALL-WEATHER ARMOR. Sun, 
  rain, wind, snow. You walk through it unfazed." Immune to ALL weather damage.
Event 2 — adventures.py: Environmental zone. "The ALL-WEATHER ARMOR laughs at 
  the conditions. Swamp, desert, tundra — you adapt to everything." Zone immunity.
Event 3 — events_car.py: Stranded in weather. "Car broke down in a blizzard. 
  The ALL-WEATHER ARMOR keeps you warm until help arrives." Survive stranded-in-weather.
```

### Tier 2 Tools (5 items)

**Master Key** (Lockpick Set + Security Bypass) — 3 events
```
Event 1 — events_day_dark.py: Any locked obstacle. "The MASTER KEY opens 
  anything. Doors, safes, cuffs, vaults. Click." Open any lock in the game.
Event 2 — adventures.py: Secret rooms. "The MASTER KEY reveals a hidden door. 
  Behind it: treasure that was never meant to be found." Secret adventure loot.
Event 3 — events_day_items.py: Locked container. "The MASTER KEY turns. The 
  safe opens. Inside: everything the previous owner couldn't take with them." High-value loot.
```

**Night Scope** (Binocular Scope + Headlamp) — 3 events
```
Event 1 — events_night.py: Night navigation. "The NIGHT SCOPE turns midnight 
  into noon. Every path is clear, every threat visible." Perfect night vision.
Event 2 — events_day_dark.py: Dark location. "The NIGHT SCOPE pierces the 
  abandoned building's darkness. You see them before they see you." Stealth advantage.
Event 3 — adventures.py: Night adventure. "NIGHT SCOPE active. The night zone 
  reveals its secrets. You move like you own the darkness." +50% night adventure bonus.
```

**SOS Kit** (Signal Mirror + Smoke Flare) — 3 events
```
Event 1 — events_day_survival.py: Stranded. "SOS KIT deployed. Mirror flashes 
  catch the sun, smoke marks your position. Rescue in under an hour." Guaranteed rescue.
Event 2 — events_car.py: Roadside emergency. "The SOS KIT's smoke and mirrors 
  flag down three passing cars in ten minutes." Fastest roadside help.
Event 3 — adventures.py: Lost in zone. "SOS KIT fires. Rangers spot you from 
  their tower. You're pulled out within the hour." Emergency adventure exit.
```

**Intelligence Dossier** (Evidence Kit + Forged Documents) — 3 events
```
Event 1 — events_day_dark.py: NPC investigation. "The INTELLIGENCE DOSSIER 
  has everything. Photos, records, secrets. You own this person." Leverage on any NPC.
Event 2 — events_day_wealth.py: Financial event. "The INTELLIGENCE DOSSIER 
  reveals the real numbers behind the deal. You negotiate from total knowledge." Perfect intel.
Event 3 — events_day_people.py: Social manipulation. "The DOSSIER whispers 
  everyone's secret. At the party, you know more than the host." Social dominance.
```

**Surveillance Suite** (Spotlight + Radio Jammer) — 3 events
```
Event 1 — events_night.py: Night patrol. "SURVEILLANCE SUITE active. The 
  spotlight scans, the jammer blocks their comms. You see all, they hear nothing." Night control.
Event 2 — events_day_dark.py: Counter-surveillance. "The SURVEILLANCE SUITE 
  detects their bugs and kills their signal. You're clean." Block surveillance.
Event 3 — events_day_casino.py: Casino ops. "SUITE jams their earpieces while 
  the light tracks their movement. Security is blind and deaf." Ultimate casino stealth.
```

### Tier 2 Charms (4 items)

**Mind Shield** (Dream Catcher + Worry Stone) — 3 events
```
Event 1 — events_night.py: Nightmare defense. "The MIND SHIELD absorbs the 
  nightmare. You sleep like the dead. Peacefully." Immune to all sanity loss at night.
Event 2 — events_day_surreal.py: Reality break. "The MIND SHIELD holds your 
  sanity together. Reality warps but you don't." Immune to surreal event sanity damage.
Event 3 — events_day_dark.py: Psychological attack. "The MIND SHIELD deflects 
  the horror. Your mind is a fortress." Block all psychological damage.
```

**Fortune's Favor** (Lucky Charm Bracelet + Luck Totem) — 3 events
```
Event 1 — events_day_casino.py: Any gambling. "FORTUNE'S FAVOR radiates luck. 
  The dealer busts three times in a row. Coincidence? Not anymore." +25% gambling luck.
Event 2 — events_day_numbers.py: Lottery/chance. "FORTUNE'S FAVOR hums. The 
  numbers fall close. Not perfect, but close enough." Significant lottery boost.
Event 3 — events_day_items.py: Loot quality. "FORTUNE'S FAVOR guides your hand 
  to the best loot in the pile. Every time." Premium loot rolls.
```

**Fate Reader** (Lucky Charm Bracelet + Fortune Cards) — 3 events
```
Event 1 — events_day_surreal.py: Future vision. "The FATE READER deals three 
  cards. Past, present, future. The future card shows..." Reveal next day's main event.
Event 2 — events_day_people.py: NPC reading. "You read their fortune with the 
  FATE READER. Their face goes pale. 'How did you know that?'" NPC manipulation.
Event 3 — events_day_dark.py: Danger prediction. "The FATE READER warns of 
  danger ahead. You change course. The danger passes." Avoid next negative event.
```

**Lucid Dreaming Kit** (Dream Catcher + Eldritch Candle) — 3 events
```
Event 1 — events_night.py: Dream control. "The LUCID DREAMING KIT activates. 
  You're in the dream, but this time YOU decide what happens." Choose dream outcome.
Event 2 — mechanics_intro.py: Mechanic dreams. "The LUCID DREAMING KIT enhances 
  the mechanic's dream. Details sharpen. Secrets surface." Bonus dream content.
Event 3 — events_day_dark.py: Blood moon dream. "Under the blood moon, the 
  LUCID DREAMING KIT lets you negotiate with the dream. Better terms." Better blood moon outcomes.
```

### Tier 2 Social (4 items)

**Old Money Identity** (Gentleman's Charm + Heirloom Set) — 3 events
```
Event 1 — events_day_wealth.py: VIP everything. "The OLD MONEY IDENTITY opens 
  every door. Platinum card? No, old money. Better." Maximum VIP access everywhere.
Event 2 — events_day_people.py: Social dominance. "OLD MONEY IDENTITY. People 
  defer before you speak. Waiters appear. Doors open." Auto-win social encounters.
Event 3 — events_day_casino.py: Casino royalty. "The casino rolls out the red 
  carpet for the OLD MONEY IDENTITY. Private table, personal dealer." Ultimate casino treatment.
```

**New Identity** (Low-Profile Outfit + Forged Documents) — 3 events
```
Event 1 — events_day_dark.py: Erase history. "The NEW IDENTITY is complete. 
  Whatever you were, whoever was looking — it's over. Clean slate." Reset heat/wanted level.
Event 2 — events_day_wealth.py: Financial fresh start. "The NEW IDENTITY opens 
  a bank account. No history, no debt, no past." Reset financial negatives.
Event 3 — events_illness.py: Medical under radar. "The NEW IDENTITY gets you 
  treated under a different name. No questions, no records." Anonymous medical care.
```

**Beast Tamer Kit** (Animal Bait + Pet Toy) — 3 events
```
Event 1 — events_day_animals.py: Any animal. "The BEAST TAMER KIT calms, 
  feeds, and befriends. Even the wolf lies down." Pacify any animal.
Event 2 — events_day_companions.py: Companion training. "The BEAST TAMER KIT 
  teaches your companion new tricks. Loyalty maxes out." Max companion bonding.
Event 3 — adventures.py: Animal zone. "BEAST TAMER KIT active. The creatures 
  in this zone treat you as pack leader." Animal zones become trivial.
```

**Cheater's Insurance** (Devil's Deck + Evidence Kit) — 3 events
```
Event 1 — events_day_casino.py: Casino cheating. "CHEATER'S INSURANCE: the 
  Devil's Deck wins, the Evidence Kit ensures they can't prove it." Guaranteed casino win.
Event 2 — events_day_dark.py: Blackmail combo. "You cheated them. They caught 
  you. Then you show the EVIDENCE. Mutual destruction assured. They let you go." Escape caught-cheating.
Event 3 — events_day_wealth.py: Financial crime. "CHEATER'S INSURANCE protects 
  the con. Even if they suspect, the evidence points elsewhere." Cover tracks.
```

### Tier 2 Vehicle (3 items)

**Roadside Shield** (Tire Ready Kit + Power Grid) — 3 events
```
Event 1 — events_car.py: Any breakdown. "ROADSIDE SHIELD activates. Tire? 
  Fixed. Battery? Jumped. Fuse? Replaced. Back on the road in five minutes." Fix any car issue.
Event 2 — events_day_survival.py: Stranded. "The ROADSIDE SHIELD prevents 
  being stranded. Redundant systems keep the car alive." Prevent stranding.
Event 3 — events_night.py: Night breakdown. "ROADSIDE SHIELD deploys in the 
  dark. Pre-mounted jack, pre-wired grid. Fixed before fear sets in." Night car immunity.
```

**Auto Mechanic** (Mobile Workshop + Miracle Lube) — 3 events
```
Event 1 — events_car.py: Major repair. "AUTO MECHANIC: full workshop + super 
  lube. The engine rebuilds itself while you watch." Fix any car problem, any severity.
Event 2 — events_day_people.py: Help motorist. "AUTO MECHANIC turns you into 
  roadside AAA. Fix their car, earn $200 and a friend." Premium NPC help rewards.
Event 3 — adventures.py: Vehicle adventure. "AUTO MECHANIC keeps the car in 
  peak condition through the roughest terrain." Immune to car damage in adventures.
```

**Rolling Fortress** (Pursuit Package + Fortified Perimeter) — 3 events
```
Event 1 — events_car.py: Car chase. "ROLLING FORTRESS. They chase you? Traps 
  deploy. You chase them? Nothing escapes." Win any vehicle pursuit.
Event 2 — events_night.py: Night car defense. "Sleeping in the ROLLING 
  FORTRESS. Alarms, traps, and reinforced doors. Safer than a bank vault." Perfect car camping.
Event 3 — events_day_dark.py: Vehicular threat. "They approach the ROLLING 
  FORTRESS. The alarm screams. The traps spring. They reconsider." Immune to car-targeting crimes.
```

---

## 43. Full Event Narrative Drafts — Tier 3 & 4 Items

**Target:** 12 Tier 3 items × 2–3 events + 11 Tier 4 items × 1–2 events = ~41 event blocks.
Tier 3/4 items are endgame powerhouses. Their events should feel legendary.

### Tier 3 Items (12 items)

**Road Warrior Armor** (Assassin's Kit + Scrap Armor + Street Fighter Set) — 3 events
```
Event 1 — events_day_dark.py: ANY violence. "The ROAD WARRIOR ARMOR absorbs 
  the blow. Blade, bullet, fist — nothing penetrates. You hit back. Once. It's enough."
  Effect: Immune to ALL physical damage. Win all combat.
Event 2 — adventures.py: Adventure boss. "The ROAD WARRIOR ARMOR gleams under 
  dungeon light. The boss sees it and hesitates. Smart." Auto-win adventure bosses.
Event 3 — events_night.py: Night assault. "They came with knives. They left 
  with regrets. The ROAD WARRIOR ARMOR doesn't even have a scratch." Night immunity.
```

**Third Eye** (Mind Shield + Lucid Dreaming Kit + Fortune Cards) — 3 events
```
Event 1 — events_day_surreal.py: ANY surreal event. "The THIRD EYE opens. You 
  see what's really happening behind the illusion. The surreal becomes navigable."
  Effect: Perfect surreal event outcomes. See through all illusions.
Event 2 — events_day_dark.py: Danger sense. "The THIRD EYE pulses a warning. 
  Danger. There. Five seconds from now. You step left. The bullet misses."
  Effect: Precognition — dodge any single incoming threat.
Event 3 — mechanics_intro.py: Dream mastery. "The THIRD EYE makes dreams 
  crystalline. The mechanic speaks clearly. Every detail is memorized."
  Effect: Perfect dream recall. Maximum dream content.
```

**Nomad's Camp** (Survival Bivouac + Provider's Kit + Hydration Station) — 2 events
```
Event 1 — events_day_survival.py: ANY survival event. "The NOMAD'S CAMP 
  provides everything — shelter, food, water. You could live here forever."
  Effect: Immune to ALL survival threats (starvation, dehydration, exposure).
Event 2 — events_night.py: Night survival. "The NOMAD'S CAMP at night: fire 
  crackles, traps set, feast prepared. The wilderness is your home."
  Effect: Perfect night rest + full health restoration.
```

**All-Access Pass** (Master Key + Night Scope + Intelligence Dossier) — 3 events
```
Event 1 — events_day_dark.py: ANY locked/hidden content. "ALL-ACCESS PASS. 
  See in the dark, open any lock, know every secret. Nothing is hidden from you."
  Effect: Access any locked/hidden content in any event.
Event 2 — adventures.py: Secret zones. "The ALL-ACCESS PASS reveals doors that 
  don't exist on any map. Behind them: legendary loot."
  Effect: Access hidden adventure sub-zones.
Event 3 — events_day_wealth.py: Financial secrets. "ALL-ACCESS PASS decodes 
  their books, opens their safe, reads their encrypted emails."
  Effect: Maximum financial advantage in wealth events.
```

**Master of Games** (Old Money Identity + Cheater's Insurance + Enchanted Vintage) — 2 events
```
Event 1 — events_day_casino.py: ANY casino event. "MASTER OF GAMES. The 
  identity is real, the insurance is loaded, the wine never runs dry. You own the table."
  Effect: Win any casino event automatically.
Event 2 — events_day_people.py: ANY social event. "MASTER OF GAMES: charming, 
  wealthy, insured. Every person in the room wants to be you or know you."
  Effect: Perfect social event outcomes.
```

**Immortal Vehicle** (Auto Mechanic + Rolling Fortress + Roadside Shield) — 2 events
```
Event 1 — events_car.py: ANY car event. "IMMORTAL VEHICLE. Self-repairing, 
  self-defending, self-diagnosing. Your car is more reliable than gravity."
  Effect: Immune to ALL car problems. Car never breaks down.
Event 2 — adventures.py: Vehicle adventure. "The IMMORTAL VEHICLE plows 
  through terrain that should destroy it. Not a scratch. Not a squeak."
  Effect: Perfect vehicle performance in all adventure zones.
```

**Gambler's Aura** (Fortune's Favor + Luck Totem + Smelling Salts) — 2 events
```
Event 1 — events_day_casino.py: ANY gambling. "GAMBLER'S AURA. Triple luck 
  radiates from you. Every card falls right. The dealer looks sick."
  Effect: +30% permanent gambling advantage.
Event 2 — events_day_numbers.py: Lottery. "The GAMBLER'S AURA bends 
  probability. The numbers lean toward yours."
  Effect: Major lottery/numbers boost.
```

**Ark Master's Horn** (Beast Tamer Kit + Animal Bait + Feeding Station) — 2 events
```
Event 1 — events_day_animals.py: ANY animal event. "The ARK MASTER'S HORN 
  sounds. Every creature in earshot responds. They come to you. They obey."
  Effect: Command any animal in any event.
Event 2 — events_day_companions.py: Companion mastery. "The ARK MASTER'S 
  HORN bonds you to your companion at the deepest level. Unbreakable loyalty."
  Effect: Companion can never leave, maximum happiness.
```

**Guardian Angel** (SOS Kit + Distress Beacon + Fortified Perimeter) — 2 events
```
Event 1 — events_day_dark.py: ANY danger. "GUARDIAN ANGEL activates. SOS 
  fires, beacon screams, perimeter deploys. You are untouchable."
  Effect: Immune to damage from any single event. Once-per-day shield.
Event 2 — events_illness.py: Medical emergency. "GUARDIAN ANGEL calls for 
  medical help before you even realize you're sick. EMTs arrive in minutes."
  Effect: Automatic medical response. Prevent any illness from worsening.
```

**Hazmat Suit** (Gas Mask + All-Weather Armor + Storm Suit) — 2 events
```
Event 1 — events_day_survival.py: ANY environmental hazard. "HAZMAT SUIT. 
  Poison gas, acid rain, radiation, hurricanes. You walk through it all."
  Effect: Immune to ALL environmental damage.
Event 2 — adventures.py: Toxic zones. "The HAZMAT SUIT lets you walk through 
  zones that would kill anyone else. The treasure is unguarded — no one else can get here."
  Effect: Access toxic adventure zones with no penalty.
```

**Ghost Protocol** (Surveillance Suite + New Identity + Radio Jammer) — 3 events
```
Event 1 — events_day_dark.py: ANY pursuit/wanted event. "GHOST PROTOCOL 
  active. Cameras see nothing, radios hear nothing, records say nothing. You don't exist."
  Effect: Invisible to all surveillance, law enforcement, and enemies.
Event 2 — events_day_wealth.py: Financial stealth. "GHOST PROTOCOL erases your 
  financial footprint. The IRS, the casino, the bank — none of them can find you."
  Effect: Immune to financial tracking/consequences.
Event 3 — events_day_casino.py: Casino stealth. "GHOST PROTOCOL. No camera 
  catches your face. No pit boss remembers your name. You play and vanish."
  Effect: Cannot be banned/tracked by casinos.
```

**Dark Pact Reliquary** (Eldritch Candle + Binding Portrait + Devil's Deck) — 2 events
```
Event 1 — events_day_dark.py: Devil interaction. "The DARK PACT RELIQUARY 
  glows. The devil recognizes the toolkit. 'You've done your homework,' he says. Terms heavily favored."
  Effect: Maximum advantage in any demonic/dark deal.
Event 2 — events_day_surreal.py: Supernatural event. "The RELIQUARY opens 
  a door between worlds. The boundary between real and unreal thins. You step through."
  Effect: Access unique supernatural event chain.
```

### Tier 4 Items — Legendary Events (11 items)

Tier 4 items are **game-changing**. Each gets 1–2 signature events that feel legendary.

**Beastslayer Mantle** — 1 event
```
events_day_animals.py: "The BEASTSLAYER MANTLE radiates primal dominion. 
Every creature — predator and prey — recognizes the alpha. You walk through 
the wild untouched. The biggest bear bows its head."
Effect: Permanent immunity to all animal attacks. All animals become docile.
```

**Seer's Chronicle** — 1 event
```
events_day_surreal.py: "The SEER'S CHRONICLE's pages turn by themselves. 
Tomorrow's date appears. Then the next day. And the next. Ten days of future 
written in your own handwriting."
Effect: Reveal the next 10 days of events. Player can prepare for everything.
```

**Wanderer's Rest** — 1 event
```
events_day_survival.py: "The WANDERER'S REST has grown roots. Literally. 
You planted the walking stick and a tree sprouted overnight. Fruit hangs 
from branches. A spring bubbles up. You will never want for anything again."
Effect: Permanent self-sufficiency. No survival stat ever drops.
```

**Skeleton Key** — 2 events
```
Event 1 — events_day_dark.py: "The SKELETON KEY doesn't just open locks. 
It opens possibilities. Walls develop doors. Dead ends become passages. 
The game itself rearranges to let you through."
Effect: Access ANY hidden content. Unlock secret endings.

Event 2 — adventures.py: "The SKELETON KEY opens a door that shouldn't 
exist in this adventure zone. Behind it: the developer's stash."
Effect: Access ultimate secret adventure loot.
```

**King of the Road** — 1 event
```
events_day_people.py: "The KING OF THE ROAD enters the room. Conversations 
stop. The casino manager comps your everything. The cop tears up the ticket. 
The con artist gives YOUR money back. The road belongs to you."
Effect: All NPCs defer to you. All interactions favor you. Permanent.
```

**War Wagon** — 1 event
```
events_car.py: "The WAR WAGON rumbles. The engine is alive — really alive. 
It predicts potholes and avoids them. It self-diagnoses and self-repairs. 
When someone tries to follow you, it... deals with them."
Effect: Car is AI-enhanced. Never breaks, self-defends, self-navigates.
```

**Moonlit Fortune** — 1 event
```
events_day_casino.py: "The MOONLIT FORTUNE glows beneath your shirt. At the 
blackjack table, you FEEL what the next card is. Not see — feel. The dealer 
can't explain it. The house edge is gone. It's your edge now."
Effect: Permanent +20% blackjack advantage. Stacks with other gambling buffs.
```

**Leviathan's Call** — 1 event
```
events_day_animals.py: "You sound the LEVIATHAN'S CALL. The ground trembles. 
Birds take flight. From the nearest body of water, something LARGE surfaces. 
It waits for your command."
Effect: Summon a creature guardian. Immune to all threats for 3 days.
```

**Last Breath Locket** — 1 event
```
events_day_dark.py: "You died. The bullet, the blade, the fall — it was 
lethal. But the LAST BREATH LOCKET ignites. White fire. Your body knits 
back together. You stand up. Death looks at you, confused, and walks away."
Effect: TRUE IMMORTALITY. Cannot die from any event. Permanent.
```

**Phantom Rose** — 1 event
```
events_day_wealth.py: "The PHANTOM ROSE makes you a legend — the gambler 
nobody can find, the one who wins and vanishes. Stories spread, but no one 
can prove you exist. You are a whisper, a myth, a rose left on a table."
Effect: Immune to all negative reputation events. Legendary status.
```

**Soul Forge** — 1 event
```
events_day_surreal.py: "The SOUL FORGE activates. Time fractures. You see 
every decision you've ever made. One of them glows red. Do you want to 
change it? The forge burns. History rewrites itself."
Effect: Rewrite ONE past event outcome. The consequences cascade forward.
One-time use. The most powerful item in the game.
```

---

### Summary — Total New Event Blocks

| Section | Category | Items | Events | Files Touched |
|---------|----------|-------|--------|---------------|
| 36 | Gadgets | 7 | 23 | 8 files |
| 37 | Disguises | 7 | 24 | 9 files |
| 38 | Tonics & Consumables | 9 | 27 | 9 files |
| 39 | Dark Arts | 5 | 17 | 7 files |
| 40 | Luxury Crafts | 7 | 21 | 9 files |
| 41 | Vehicle Upgrades | 5 | 15 | 6 files |
| 42 | Tier 2 Items | 25 | 75 | 11 files |
| 43 | Tier 3 & 4 Items | 23 | 41 | 10 files |
| **Total** | **All New Items** | **88** | **~243** | **11 unique event files** |

### Event File Coverage

| Event File | New Event Blocks Added |
|------------|----------------------|
| events_day_dark.py | ~35 |
| events_night.py | ~25 |
| events_day_survival.py | ~22 |
| adventures.py | ~20 |
| events_day_people.py | ~20 |
| events_car.py | ~18 |
| events_day_animals.py | ~12 |
| events_day_casino.py | ~12 |
| events_day_companions.py | ~10 |
| events_day_surreal.py | ~10 |
| events_day_wealth.py | ~12 |
| events_illness.py | ~8 |
| events_day_items.py | ~6 |
| mechanics_intro.py | ~3 |
| locations.py | ~2 |
| events_day_numbers.py | ~2 |

### Minimum Events Per Item

Every new crafted item has **at least 3 event appearances** across **at least 2 different files**, exceeding the current average of ~1.15 events per crafted item. Tier 4 legendary items have fewer events but each one is a game-changing moment.

---

## 44. Wild Item Interactions — The Weird Stuff

> Items shouldn't just do what their name says. The best items in any game make you go "wait, I can do THAT?" This section catalogs **unexpected, bizarre, morally questionable, and emergent behaviors** — things players discover by accident and tell their friends about. **Things get weird.**

### Design Philosophy

1. **No item does only one thing.** If an item has an obvious use, it ALSO has a non-obvious one.
2. **Consequences are unpredictable.** Using an item "correctly" can create unexpected problems. Using it "wrong" can create unexpected solutions.
3. **Moral weight.** Some of the best uses are... questionable. The game doesn't judge. But the world reacts.
4. **Emergent combos.** Two items used in the same event can create outcomes neither would alone.
5. **The world remembers.** Wild interactions create reputation, heat, karma shifts, NPC memory. Nothing happens in a vacuum.

---

### 44A. Single-Item Wild Triggers

> These fire when a player has ONE specific item during an event where it has NO obvious relevance. The game rewards curiosity and experimentation.

#### Gadgets — Off-Label Uses

**Headlamp at a Poker Game** — `events_day_casino.py`
```
Trigger: poker/card event at night, has_item("Headlamp")
Narrative: "You forgot to take off the HEADLAMP. The light catches the 
           dealer's cards at an angle. For a split second, you see through 
           the coating. You see EVERYTHING."
Effect: Peek at the dealer's hole card for ONE hand. Not cheating. Not really.
Consequence: 20% chance the pit boss notices the glare. If caught: banned for one day.
```

**EMP Device at the Blackjack Table** — `events_day_casino.py`
```
Trigger: casino gambling, has_item("EMP Device")
Narrative: "The EMP DEVICE pulses in your pocket. The electronic card shuffler 
           DIES. Sparks. Silence. The dealer blinks, then reaches for a manual 
           shuffler. The old kind. The imperfect kind. Your odds just changed."
Effect: Manual shuffling = +10% blackjack advantage for rest of session. 
Consequence: Casino notices fried electronics. Security sweeps. You have 3 
  hands before they trace it. Item consumed. Casino heat +50.
```

**Radio Jammer During a Police Chase** — `events_day_dark.py`
```
Trigger: police pursuit/warrant event, has_item("Radio Jammer")
Narrative: "You flip the RADIO JAMMER. The cop's radio dies mid-sentence. 
           Dispatch hears static. Backup never comes. The officer alone 
           realizes he's outgunned by silence and drives away."
Effect: Cancel police backup. Single officer encounter instead of full squad.
Consequence: Next time you see police, they have SIGNAL-PROOF radios. 
  One-time trick per playthrough. FCC violation flagged (flavor text).
```

**Evidence Kit at a Wedding** — `events_day_people.py`
```
Trigger: social celebration (wedding/party), has_item("Evidence Kit")
Narrative: "You photograph the wedding out of boredom. But the EVIDENCE KIT 
           catches something the eye missed — the best man pocketing the 
           ring box. The bride pays you $200. The best man pays you $300 
           to delete the photos."
Effect: Choose — give photos to bride (+$200, +karma) or sell to best man 
  (+$300, -karma, best man owes you a favor later).
```

**Distress Beacon in a Casino** — `events_day_casino.py`
```
Trigger: in casino, losing badly, has_item("Distress Beacon")
Narrative: "You trigger the DISTRESS BEACON under the table. Ambulance, fire 
           truck, two cop cars. The casino evacuates. In the chaos, no one 
           notices you pocket $500 in chips off the floor."
Effect: +$500. But: casino recognizes you as the beacon source (80% chance).
  If caught: permanent reputation as "that guy." -access to one casino.
  Item consumed. Karma -2.
```

**Security Bypass on Your Own Car** — `events_car.py`
```
Trigger: any car event, has_item("Security Bypass"), car condition > 50%
Narrative: "Bored, you pick the lock on your own glove compartment — the one 
           that's been stuck since you bought the car. Inside: a $50 bill, 
           a photo of someone else's family, and a loaded revolver."
Choice: Keep the gun (new item: 'Previous Owner's Gun'), keep the money ($50), 
  or put it all back (nothing happens, but +1 karma for restraint).
Effect: One-time discovery. Adds backstory to your vehicle. The photo becomes 
  relevant 20 days later.
```

**Spotlight During Night Sleep** — `events_night.py`
```
Trigger: sleeping in car at night, has_item("Spotlight")
Narrative: "You leave the SPOTLIGHT on to deter visitors. At 3am, the beam 
           catches a deer frozen in the light. Behind it: two men who were 
           creeping toward your car. They scatter. The deer stays, staring."
Effect: Prevent night robbery event. But: battery drain. -5% car condition.
  The deer becomes a recurring character (appears randomly for 5 days).
```

#### Disguises — Identity Gets Complicated

**Low-Profile Outfit at a Homeless Shelter** — `events_day_people.py`
```
Trigger: shelter/charity event, has_item("Low-Profile Outfit")
Narrative: "The LOW-PROFILE OUTFIT works too well. The shelter worker hands 
           you a blanket and a meal. 'We see you, brother. You're safe here.' 
           You didn't come for charity. But the soup is... really good."
Effect: Free food (+health). Free blanket item (comfort +10 at night). 
  But: NPC who saw you starts recognizing you as "shelter regular." 
  Future events may reference this false identity.
```

**Beach Bum Disguise at a Job Interview** — `events_day_people.py`
```
Trigger: business/professional event, has_item("Beach Bum Disguise")
Narrative: "You forgot you're wearing the BEACH BUM DISGUISE. The investor 
           stares at your flip-flops. Long pause. 'I like your energy,' 
           he says. 'You're either a genius or insane. I'm in.'"
Effect: 50/50 — either get the deal (they think you're eccentric-rich) 
  or get thrown out (they think you're a beach bum). If it works: +$300 
  and the investor becomes a recurring contact. If not: reputation -10.
```

**Gas Mask at a Funeral** — `events_day_dark.py`
```
Trigger: death/mourning event, has_item("Gas Mask")
Narrative: "You show up to the funeral in a GAS MASK because you forgot to 
           take it off. Everyone stares. Someone whispers 'He must know 
           something we don't.' Panic spreads. People start running. 
           You stand there, confused, in a cloud of pine-scented air."
Effect: Funeral attendees evacuate. You loot the reception table — free 
  food, $40 in the donation box, and an antique brooch someone left behind.
  Karma -3. But: one NPC who stayed thinks you're a government agent.
  They bring you "tips" for the next 10 days (mix of useful and nonsense).
```

**Forged Documents at a Hospital** — `events_illness.py`
```
Trigger: illness/injury, has_item("Forged Documents")
Narrative: "The FORGED DOCUMENTS identify you as Dr. Robert Chen, MD. The 
           nurse doesn't question it. They hand you a lab coat. Suddenly 
           you're not the patient — you're the doctor. Everyone looks at 
           you for instructions."
Effect: Free medical treatment. But: 30% chance you're asked to perform a 
  procedure. Choice — attempt it (-karma but +$500 from the con) or 
  admit you're not a doctor (+karma, the real doctor treats you free 
  out of amusement, and the nurse becomes a friend contact).
```

**Brass Knuckles at a Negotiation** — `events_day_people.py`
```
Trigger: negotiation/deal, has_item("Brass Knuckles")
Narrative: "You reach out for a handshake. You forgot you're wearing BRASS 
           KNUCKLES. The businessman's eyes drop to your hand. He signs 
           the deal without reading it. 'Your terms are fine,' he says."
Effect: Auto-win negotiation. But: next time you meet this NPC, they 
  bring hired security. Negotiations become harder with them specifically.
  NPCs talk. 15% chance the next 2 NPCs you negotiate with also know.
```

**Storm Suit at a Club** — `events_day_wealth.py`
```
Trigger: nightlife/party event, has_item("Storm Suit")
Narrative: "You walk into the club wearing a full STORM SUIT. The bouncer 
           opens his mouth, closes it, and steps aside. Inside, someone 
           assumes you're the DJ. They hand you the mic."
Choice: Go with it (become DJ for the night: +sanity, +$100 tips, 
  -reputation as "that storm suit DJ") or clarify (they laugh, you 
  get free drinks all night for being a good sport).
```

#### Tonics — Unintended Side Effects

**Stink Bomb at a Casino** — `events_day_casino.py`
```
Trigger: in casino, has_item("Stink Bomb")
Narrative: "The STINK BOMB cracks. Methane-level stench fills the casino 
           floor. Fire alarms trigger. Sprinklers deploy. The vault door 
           unlocks automatically per safety protocol. You have exactly 
           90 seconds before security realizes what happened."
Choice: Rob the vault (+$2000, -karma 5, MASSIVE heat increase, item 
  consumed) or flee with the crowd (grab $300 in abandoned chips off 
  tables, no karma hit, item consumed).
Effect: Either way, this casino PERMANENTLY knows your face. If you 
  robbed the vault: bounty hunters show up in 5 days.
```

**Voice Soother at an Interrogation** — `events_day_dark.py`
```
Trigger: police/authority questioning, has_item("Voice Soother")
Narrative: "One sip of VOICE SOOTHER. Your voice drops to melted butter. 
           The detective leans back. 'You know what? You're convincing.' 
           Then: 'Too convincing. Nobody is this calm.' He calls for backup."
Effect: 60% chance — talk your way out completely. 40% chance — your 
  unnatural calm makes them MORE suspicious. Double search. If you're 
  carrying anything illegal, they WILL find it.
```

**Animal Bait on Yourself** — `events_night.py`
```
Trigger: night event, has_item("Animal Bait"), no companion
Narrative: "You smear ANIMAL BAIT on your hands out of curiosity. At 2am, 
           a raccoon army arrives. They don't attack — they ORGANIZE. 
           They raid the nearby dumpster and bring you: a half-eaten 
           sandwich, a working lighter, and someone's car keys."
Effect: Free loot — random food item + random useful item. The raccoons 
  come back for 3 nights (diminishing returns: night 2 brings junk, 
  night 3 they bring you a dead bird and seem proud about it).
  If you have a companion: the companion and the raccoons DO NOT get along.
```

**Cool Down Kit on Your Car** — `events_car.py`
```
Trigger: car overheating, has_item("Cool Down Kit")
Narrative: "You dump the COOL DOWN KIT on the engine. Steam erupts. The 
           temperature gauge drops from red to blue. But something else 
           happens — the cold water hits the hot block and cracks a 
           gasket. Silence. Then a very expensive hissing noise."
Effect: Fix overheating immediately. But: 25% chance of gasket damage 
  (-15% car condition). The remaining 75%: the rapid cooling actually 
  IMPROVES pressure seals. +5% car condition bonus. Gamble.
```

**Outdoor Shield at Night** — `events_night.py`
```
Trigger: night rest, has_item("Outdoor Shield")
Narrative: "You applied OUTDOOR SHIELD before bed. The bug spray component 
           repels mosquitoes. But the UV reflectant catches moonlight. 
           You glow faintly silver. A passing NPC thinks you're a ghost. 
           The rumor spreads. 'The glowing man' becomes a local legend."
Effect: +5 reputation as "supernatural figure." Future NPC encounters 
  have a 10% chance of referencing the glow. Some NPCs are afraid 
  of you. One NPC seeks you out to ask if you can cure their disease.
```

**Vermin Bomb in a Restaurant** — `events_day_people.py`
```
Trigger: dining/restaurant event, has_item("Vermin Bomb")
Narrative: "You drop the VERMIN BOMB under the table. Not to clear vermin — 
           just to see what happens. Thirty seconds later, a river of rats 
           pours out of the kitchen. The health inspector, who happened to 
           be eating two tables over, shuts the place down on the spot."
Effect: Free meal (the chaos means nobody charges you). The restaurant 
  closes for a week. If you come back: the owner hates you specifically.
  But: the health inspector remembers you as a "concerned citizen." 
  Future health/authority events go better. Item consumed.
```

#### Dark Arts — Things You Probably Shouldn't Do

**Eldritch Candle During a Blackjack Hand** — `events_day_casino.py`
```
Trigger: gambling, has_item("Eldritch Candle")
Narrative: "You set the ELDRITCH CANDLE on the table. The green flame makes 
           the cards translucent. You can see the face values through the 
           backs. The dealer stares at the flame, hypnotized. Other players 
           leave the table. It's just you and the Math now."
Effect: Perfect information for 5 hands. Then the candle goes out and 
  won't relight for 3 days. During those 3 days: -5 luck at ALL gambling.
  The darkness needs to be repaid.
```

**Binding Portrait on a Shopkeeper** — `locations.py`
```
Trigger: visiting any shop, has_item("Binding Portrait"), karma < -2
Narrative: "You show the BINDING PORTRAIT to the shopkeeper. Their pupils 
           dilate. 'I'll give you whatever you want,' they say in a voice 
           that isn't entirely theirs. From now on, this shop sells to you 
           at half price. The shopkeeper seems fine. Mostly."
Effect: 50% discount at ONE shop, permanently. But: the shopkeeper 
  starts appearing in your dreams. Not threatening. Just... watching. 
  Sanity -1 per night for 5 nights. After that, they stop. Or maybe 
  you stop noticing.
```

**Blackmail Letter to Your Companion** — `events_day_companions.py`
```
Trigger: companion present, has_item("Blackmail Letter"), companion loyalty < 50
Narrative: "You show the BLACKMAIL LETTER to your companion. It's blank — 
           the actual blackmail isn't on paper, it's in the implication. 
           Your companion freezes. 'You wouldn't.' You would. They know. 
           'Fine. I'll stay. I'll do whatever you want.'"
Effect: Companion loyalty instantly maxes to 100. But: companion happiness 
  drops to 0. They obey you mechanically. They stop having personality 
  in dialogue. After 10 days: choice event — they try to leave for real.
  If you let them: +5 karma, they're gone. If you use the letter again: 
  they stay forever, but your karma drops to minimum and you get a 
  unique ending flag: "The Handler."
```

**Devil's Deck at a Children's Event** — `events_day_people.py`
```
Trigger: family/children event, has_item("Devil's Deck")
Narrative: "You do card tricks for a group of kids using the DEVIL'S DECK. 
           The cards move on their own — floating, reshuffling, changing 
           suits. The kids are AMAZED. Their parents are TERRIFIED. One 
           mother drags her child away. Another asks for your number."
Effect: +$50 tips from impressed parents. One kid is now convinced magic 
  is real and follows you around town for 3 days asking to learn tricks.
  (The kid has a 5% chance of finding a random item each day and giving 
  it to you. "I found this! Is it magic?" It's usually junk. USUALLY.)
```

**Fortune Cards Read for Your Car** — `events_car.py`
```
Trigger: car maintenance/check, has_item("Fortune Cards")
Narrative: "You lay FORTUNE CARDS on the dashboard. The car vibrates. The 
           cards arrange themselves: 'THE TOWER' on the brake pedal, 
           'DEATH' on the exhaust pipe. Then one card you've never seen 
           slides under the seat: 'THE JOURNEY.' Your car hums. Approval?"
Effect: Fortune Cards accurately predict the next car problem (gives a 
  warning 1-3 days before a car event occurs). If you fix the problem 
  before it triggers: no event. If you ignore it: the event is WORSE 
  than normal. The car remembers being read and runs 2% smoother.
```

#### Luxury — Conspicuous Consequences

**Kingpin Look at a Pawn Shop** — `locations.py`
```
Trigger: visiting Grimy Gus, has_item("Kingpin Look")
Narrative: "Gus looks up. Looks at the chain. The cigar. The stance. 
           'Oh. OH. Sir, I — I didn't realize. Please. Premium prices 
           for you. Whatever you need.' Gus's hands are shaking."
Effect: +25% pawn value on ALL items for this visit. But: Gus tells 
  other NPCs a "big player" came by. Criminal element hears about it. 
  +10% chance of being targeted by a scam or robbery in the next 5 days.
```

**Enchanted Vintage at an Enemy Encounter** — `events_day_dark.py`
```
Trigger: hostile NPC confrontation, has_item("Enchanted Vintage")
Narrative: "You offer the hostile NPC a sip of ENCHANTED VINTAGE. Against 
           all reason, they accept. The wine is... transcendent. Warm. 
           Healing. Their anger dissolves. 'I... don't know why I was 
           upset,' they say. 'Sit with me.'"
Effect: Hostile NPC becomes neutral or friendly for this encounter. 
  25% chance they become a recurring contact. But: the Enchanted Vintage 
  loses 1 "charge" (it has 3). When charges run out, the flask stays but 
  it pours nothing. Sadness. Refill requires Vintage Wine + Silver Flask 
  again.
```

**Heirloom Set at a Crime Scene** — `events_day_dark.py`
```
Trigger: crime scene/investigation, has_item("Heirloom Set")
Narrative: "The detective examines the pen from the HEIRLOOM SET. 'Wait. 
           These initials — VRM — that's Victor Reginald Montague. The 
           missing millionaire. Where did you get this?' Turns out the 
           'antique pen' belonged to a man who vanished in 1987."
Effect: The detective either: (a) thinks you found the pen (+$100 finder's 
  fee, new quest chain — find what happened to Victor), or (b) thinks 
  you KILLED Victor (flee! +heat, -karma, but you keep the pen which 
  is now worth $500 as evidence).
```

**Animal Magnetism at Night** — `events_night.py`
```
Trigger: sleeping at night, has_item("Animal Magnetism")
Narrative: "You wake up surrounded by stray cats. Seven of them. They're 
           purring. The ANIMAL MAGNETISM's cologne drew them from across 
           town. One of them brought you a dead bird. Another brought a 
           watch. A third brought a note that reads 'HELP ME.'"
Effect: Random loot from cats (1-3 items: junk 60%, useful 30%, unsettling 
  10%). The note triggers a mini-quest if you investigate — leads to a 
  person trapped in a basement 2 blocks away. Rescue them: +karma +$200.
  Ignore the note: the cats stop coming. They know.
```

#### Vehicle — Cars Have Feelings

**Tire Ready Kit During a Chase** — `events_day_dark.py`
```
Trigger: car chase, has_item("Tire Ready Kit")
Narrative: "Mid-chase, you throw the spare tire from the TIRE READY KIT out 
           the window. It bounces, hits the pursuing car's windshield. 
           They swerve into a ditch. You didn't plan that. But it worked."
Effect: Escape pursuit. Tire Ready Kit loses its spare (can still fix 
  flats but takes longer). The pursuing driver becomes a recurring 
  nemesis. They want their windshield money.
```

**Miracle Lube at a Stealth Event** — `events_day_dark.py`
```
Trigger: stealth/infiltration, has_item("Miracle Lube")
Narrative: "The door hinges are ancient and rusty. One squeak and everyone 
           hears you. A drop of MIRACLE LUBE on each hinge. You open the 
           door in absolute silence. Then the next. Then the vault."
Effect: Perfect stealth on any "door" event. But: the lube leaves a 
  scent trail. Anyone with a dog can follow your path afterward.
```

**Mobile Workshop Builds Something Weird** — `events_day_surreal.py`
```
Trigger: surreal event, has_item("Mobile Workshop"), random 10% chance
Narrative: "You black out for an hour. When you come to, the MOBILE WORKSHOP 
           is fully deployed and you've built... something. It looks like a 
           satellite dish made of spoons. You have no memory of building it. 
           It's receiving a signal. The signal is a weather forecast for 
           a city that doesn't exist."
Effect: The device becomes an item: 'Spoon Satellite.' It predicts weather 
  events 2 days early. It also occasionally picks up what sounds like 
  a conversation in a language you almost understand. Sanity -1 or +1 
  (the player finds it either deeply unsettling or weirdly comforting).
```

**Pursuit Package at a Marathon** — `events_day_people.py`
```
Trigger: crowd/competition event, has_item("Pursuit Package")
Narrative: "You're wearing the PURSUIT PACKAGE shoes and carrying the whistle. 
           A charity marathon passes. Someone shoves a number bib on you. 
           You run. You WIN. The crowd cheers. You win $500 and a trophy. 
           You're on the local news. Everyone knows your face now."
Effect: +$500, +reputation. But: your face is on TV. Heat +15. Any NPC 
  looking for you now has a much easier time. Trade-off: fame vs safety.
```

---

### 44B. Cross-Item Wild Combos

> When a player has TWO specific items during the same event, something NEITHER item would do alone happens. These are the "holy crap" moments. Players should discover these through experimentation, NOT through hint text.

#### Weaponized Combinations

**Stink Bomb + Evidence Kit = "The Insurance Scam"** — `events_day_wealth.py`
```
Trigger: business/restaurant/building event, has both items
Narrative: "You photograph the building with the EVIDENCE KIT. Clean record. 
           Then you crack the STINK BOMB inside. Health code violation. 
           You send the 'before' photos to the owner. They pay you $800 
           to make this go away."
Effect: +$800. -karma 3. The owner is ruined OR grateful depending on 
  how you phrase it. Choice: extort ($800, -karma) or offer to help 
  clean up (+$200 honestly, +karma 2). Either way: both items consumed.
```

**EMP Device + Security Bypass = "Ghost in the Machine"** — `events_day_dark.py`
```
Trigger: locked/secured building, has both items
Narrative: "EMP kills the alarms. Security Bypass handles the physical 
           locks. You walk through a building that thinks it's perfectly 
           secure. Camera feeds are static. Door logs show nothing. 
           You were never here. Except you took everything."
Effect: Loot an entire building — $500-$2000 + 2-3 random items. But: 
  EMP is consumed. Security Bypass has a 30% chance of being damaged 
  (picks bent). When the building discovers the robbery: if you used 
  the EMP first, NO evidence traces to you. Clean crime.
```

**Brass Knuckles + Gentleman's Charm = "Civilized Violence"** — `events_day_people.py`
```
Trigger: confrontation at a social event, has both items
Narrative: "The man insults you. You dab the GENTLEMAN'S CHARM cologne on 
           your BRASS KNUCKLES. 'I'm terribly sorry about this,' you say 
           with genuine politeness. You punch him once. He goes down 
           elegantly. The crowd applauds. It was the classiest beatdown 
           anyone has ever witnessed."
Effect: Win the confrontation AND gain social points. The unconscious man's 
  friends buy you a drink. +$50. +reputation 5. No karma penalty because 
  everyone agrees he deserved it. Unlocks title: "The Gentleman."
```

**Fire Launcher + Animal Bait = "The BBQ Trap"** — `events_day_survival.py`
```
Trigger: starvation/food crisis, has both items
Narrative: "Set the ANIMAL BAIT. Wait. Light the FIRE LAUNCHER. What follows 
           is technically hunting, technically cooking, and technically a 
           war crime against the local squirrel population. But you eat 
           like a king tonight."
Effect: Massive food (+50 health). Animal Bait consumed. Fire Launcher 
  loses one "charge." But: the local animal population REMEMBERS. Future 
  animal events in this area are more hostile for 10 days. PETA (or 
  whatever the in-game equivalent is) adds you to a list.
```

#### Mind-Bending Combinations

**Eldritch Candle + Fortune Cards = "True Sight"** — `events_day_surreal.py`
```
Trigger: any event, has both items, night time
Narrative: "The ELDRITCH CANDLE lights. The FORTUNE CARDS spread themselves. 
           The green flame illuminates cards that aren't in any normal deck — 
           THE PLAYER. THE ENGINE. THE SAVE FILE. One card shows tomorrow. 
           Not in metaphor. Literally. It shows you what event will trigger 
           and what choice wins."
Effect: Reveal the EXACT next day event and its optimal choice. Meta-breaking. 
  But: sanity -5. The candle shows you a card labeled 'THE THING WATCHING.' 
  You don't know what it means. You will. (Seeds a rare event 7-14 days 
  later where something acknowledges you saw it through the cards.)
```

**Devil's Deck + Binding Portrait = "The Soul Game"** — `events_night.py`
```
Trigger: night gambling or supernatural event, has both items
Narrative: "You deal from the DEVIL'S DECK. You wager the BINDING PORTRAIT. 
           Your opponent wagers a memory. When you win — and you do — their 
           memory enters the portrait. They forget meeting you. They forget 
           everything about today. You keep the memory. It's not yours but 
           you can watch it whenever you want."
Effect: Acquire 'Stolen Memory' item. It gives +1 to a random stat 
  permanently. But: the person you stole from becomes a hollow NPC — 
  present but empty. If you hold 3 Stolen Memories: you unlock the 
  secret "Memory Thief" event chain. But your own memories start to 
  blur — 10% chance per day that a flashback plays wrong.
```

**Gas Mask + Voice Soother = "The Voice of God"** — `events_day_people.py`
```
Trigger: crowd/group event, has both items
Narrative: "The GAS MASK distorts your VOICE SOOTHER-enhanced voice into 
           something deep, resonant, and inhuman. You sound like an 
           authority from another dimension. People freeze. One person 
           kneels. You said 'excuse me' but they heard a commandment."
Effect: Any crowd event auto-succeeds. NPCs in the crowd become 
  "followers" for 3 days — they'll do small favors if encountered.  
  But: one NPC starts a CULT based on your muffled words. This becomes 
  a storyline. They show up periodically asking for guidance. If you 
  lean into it: you get a "congregation" that pays you tribute ($50/day 
  for 10 days). If you deny it: they're crushed, -sanity for you.
```

**Lucid Dreaming Kit + Fortune Cards = "Dream Gambling"** — `events_night.py`
```
Trigger: night rest, has both items
Narrative: "In the dream, the FORTUNE CARDS become a full casino. You can 
           gamble in your sleep. The stakes? Not money — time. Win and 
           tomorrow has extra events. Lose and tomorrow has fewer. The 
           dream dealer looks like you but older."
Effect: Play a mini-blackjack hand in the dream. Win: next day gets a 
  bonus positive event. Lose: next day starts with a penalty event.
  Push: the older version of you says something cryptic that's actually 
  useful advice about an upcoming event. No health cost either way — 
  it's just a dream. ...Right?
```

#### Social Engineering Combos

**Forged Documents + Kingpin Look = "The Federal Agent"** — `events_day_dark.py`
```
Trigger: criminal/authority encounter, has both items
Narrative: "FORGED DOCUMENTS that say FBI. KINGPIN LOOK that says 'believe 
           me.' You flash the badge. 'Federal investigation. Everyone out.' 
           The criminals run. The police defer. For ten minutes, you ARE  
           the law."
Effect: Clear any criminal encounter instantly. Access restricted areas. 
  But: 20% chance a real federal agent sees you. If that happens: RUN. 
  Impersonating a fed is a felony. Heat +100. But if you get away with 
  it: +$300 in confiscated "evidence" you pocketed.
```

**Blackmail Letter + Old Money Identity = "The Hostile Takeover"** — `events_day_wealth.py`
```
Trigger: business/financial event, has both items
Narrative: "You arrive as old money. You present the BLACKMAIL LETTER at 
           the board meeting. 'Resign,' you say. They do. You sit in the 
           chair. For one day, you own this business."
Effect: Gain $500-$1500 from the business. But: the business was money 
  laundering for someone dangerous. They come looking for you in 5-7 
  days. If you're still wearing Old Money Identity: they find you. If 
  you've switched to New Identity: they walk right past.
```

**New Identity + Blackmail Letter = "The Disappearing Act"** — `events_day_dark.py`
```
Trigger: heat > 50, has both items
Narrative: "Step one: NEW IDENTITY erases who you were. Step two: BLACKMAIL 
           LETTER ensures anyone who remembers stays quiet. You don't just 
           disappear — you disappear RETROACTIVELY. NPCs who met you 
           don't remember. Your wanted poster gets taken down."
Effect: Reset ALL heat to 0. All NPC memory of negative interactions 
  wiped. But: all POSITIVE NPC relationships also reset. Friends forget 
  you. Contacts forget you. You're a stranger everywhere. Complete 
  fresh start. The loneliest clean slate.
```

**Cheater's Insurance + Casino Event = "The Perfect Heist"** — `events_day_casino.py`
```
Trigger: high-stakes casino event, has_item("Cheater's Insurance")
Narrative: "The DEVIL'S DECK portion of CHEATER'S INSURANCE ensures you win. 
           The EVIDENCE KIT portion ensures they can't prove it. But the 
           real genius is what happens when the pit boss confronts you: 
           your evidence shows THEM cheating. They pay YOU hush money."
Effect: Win the table (+$500-$800). Get hush money (+$300-$500). Casino 
  reputation destroyed — they can't call you a cheater because your evidence 
  is better than theirs. But: the pit boss has a cousin. The cousin has 
  friends. This isn't over.
```

#### Existential Combos

**Binding Portrait + Forged Documents + Eldritch Candle = "Become Someone Else"** — `events_day_surreal.py`
```
Trigger: has all three items, full moon or blood moon
Narrative: "The ELDRITCH CANDLE illuminates the FORGED DOCUMENTS. You write 
           a name — any name — and press the BINDING PORTRAIT against the 
           page. The portrait changes. Your face CHANGES. When you look in 
           the mirror, someone else looks back. You are, in every measurable 
           way, a different person."
Effect: Complete identity transformation. New name, new appearance in all 
  text. All NPC relationships reset. All heat reset. But: once per game.
  Your old identity becomes an NPC who walks around town, confused, 
  wearing your old clothes. If you meet yourself: sanity check. If you 
  talk to yourself: 50/50 chance you merge back (undo the change) or 
  your old self walks away forever.
```

**Soul Forge + Any Companion = "The Deal"** — `events_day_companions.py`
```
Trigger: has Soul Forge + companion at night + companion loyalty 100
Narrative: "The SOUL FORGE opens. Your companion looks at it. Looks at you. 
           'I know what that does,' they say. 'I'll do it. For you.' They 
           step into the forge. The light is blinding. When it fades, they 
           are permanent. Not a companion — a PART OF YOU. Their stats 
           merge with yours. They speak in your thoughts."
Effect: Companion permanently merges with you. Their stat bonuses become 
  permanent player bonuses. But: you can never have another companion. 
  You hear their voice in event text, reacting to situations. They're 
  not gone — they're closer than ever. Some players find this beautiful. 
  Some find it horrifying. Both reactions are correct.
```

**Phantom Rose + Eldritch Candle = "Legend Unwritten"** — `events_day_surreal.py`
```
Trigger: has both Tier 4 items, 10+ days survived
Narrative: "The PHANTOM ROSE blooms when the ELDRITCH CANDLE is lit. Together 
           they undo something fundamental — your name disappears from the 
           game's text. Event descriptions refer to you as 'someone' or 
           'a figure.' NPCs call you 'you' because they can't remember your 
           name. You are erased from the narrative while still inside it."
Effect: You become invisible to ALL negative events for 5 days. Nothing 
  bad can happen to a person who doesn't exist. But: nothing GOOD can 
  either. No NPC interactions, no shops, no gambling wins. You exist 
  outside the story. After 5 days: everything snaps back. The world 
  SAW you come back. They're not sure who or what you are anymore.
```

---

### 44C. Chain Reactions & Butterfly Effects

> Some item uses don't just resolve an event — they **create new events** days later. Nothing happens in isolation. The world is a web of consequences.

#### The Ripple System

Every "wild" interaction has a **Ripple Score** from 1-5. Ripple 1 means it's contained. Ripple 5 means the entire game changes.

| Ripple | Meaning | Example |
|--------|---------|---------|
| 1 | NPC remembers | Someone mentions what you did in passing |
| 2 | Reputation shift | A group of NPCs changes how they treat you |
| 3 | New event chain | A multi-day storyline triggers from the action |
| 4 | World state change | Shops close, areas become accessible/inaccessible |
| 5 | Endgame flag | Action contributes to a unique ending |

#### Documented Chain Reactions

**"The Stink Bomb Casino" Chain (Ripple 4)**
```
Day 0: Stink Bomb at casino → evacuation → grab chips / rob vault.
Day 2: Casino announces renovation. Closed for 5 days.
Day 4: Rival casino opens temp location. Worse tables, shadier staff.
Day 6: Original casino reopens with enhanced security. Your face on a 
  wall behind the security desk. If you robbed the vault: bounty hunter 
  NPC appears. If you just grabbed chips: $200 fine if recognized.
Day 10: The bounty hunter, if active, becomes a recurring nemesis. They 
  learn your patterns. Every 5 days: an encounter. They get closer each 
  time. Shake them by using New Identity, or fight them with weapons,  
  or PAY them more than the bounty ($3000) and they become your bodyguard.
```

**"The Cult of the Mask" Chain (Ripple 5)**
```
Day 0: Gas Mask + Voice Soother → crowd thinks you're divine.
Day 3: Three NPCs form "The Circle." They leave notes at your car.
Day 5: The Circle has 8 members. They built a shrine. It has your 
  gas mask filter in a jar. They want a sermon.
Day 7: Choice — give a sermon (full cult leader path) or denounce it.
  SERMON PATH: The cult grows. Day 10 they have 15 members. Day 15 
  they have 30. They pay you $100/day. They fight for you in combat. 
  But: they also do things in your name that you didn't authorize. A 
  cult member robs a store "for the Prophet." Your karma drops.
  DENOUNCE PATH: The Circle breaks up. But 1 member doesn't accept it. 
  They become a stalker. They follow you, leave gifts, write letters. 
  Eventually: confrontation event where you have to deal with them.
Day 20 (Sermon Path): The cult draws media attention. Reporter event. 
  You're on the news as "The Mask Prophet." +50 heat. Choose to embrace 
  fame or go underground. Both lead to unique ending flags.
```

**"The Victor Montague Mystery" Chain (Ripple 3)**
```
Day 0: Heirloom Set at crime scene → detective finds initials V.R.M.
Day 2: An old woman approaches you. "You have Victor's pen. How?"
Day 4: She gives you a key. The key opens a locker at the bus station.
Day 6: Inside the locker: Victor's journal. He didn't die. He ran.
Day 8: The journal contains a map to a cabin in the adventure zone.
Day 10: At the cabin: Victor is alive. 83 years old. Still hiding.
  Choice — turn him in ($500 reward, story ends), protect him (+karma, 
  he gives you one of his heirlooms worth $2000), or blackmail him 
  ($1000/week for 3 weeks, then he disappears for real this time).
```

**"The Memory Thief" Chain (Ripple 5)**
```
Day 0+: Collect 3 Stolen Memories via Devil's Deck + Binding Portrait.
Chain trigger: The third memory unlocks a dream event.
Dream: All three stolen memories play simultaneously. You see through 
  three pairs of eyes at once. One memory shows a location you haven't 
  visited. One shows a conversation you shouldn't know about. One shows 
  your own face, seen through someone else's perspective, and you're 
  doing something you don't remember doing.
Day after dream: An NPC approaches. They recognize you. "You took my 
  Tuesday," they say. "Give it back." They don't want money. They don't 
  want violence. They want the memory. 
  RETURN IT: You lose 1 stat point. They walk away. +4 karma.
  KEEP IT: They curse you. -1 luck permanently. But the stat point stays.
If you collected 5+ memories: Unique ending available — "The Collector."
  Your final score screen shows all stolen memories like a photo album.
```

**"The Raccoon Network" Chain (Ripple 2)**
```
Day 0: Animal Bait on yourself at night → raccoons bring gifts.
Day 3: Raccoons bring increasingly specific items. How do they know 
  what you need? They brought you a screwdriver the day before your car 
  broke. Coincidence. Probably.
Day 5: A raccoon with a collar appears. Tag reads "AGENT FLUFFINGTON." 
  There's a phone number. If you call it: voicemail says "Your delivery 
  subscription has been upgraded. Expect premium packages."
Day 7: Raccoons bring a sealed envelope. Inside: a crude map drawn in 
  what might be crayon or might be blood. X marks a spot in the park.
Day 9: At the spot: a buried box. Inside: $300 and a note. "Services
  rendered. — F." The raccoons never come back. But sometimes, at 
  night, you hear chittering. Watching.
```

---

### 44D. Item Backfire Table

> Not every interaction goes right. When items are used in the WRONG context, they can spectacularly fail. These aren't punishments — they're comedy.

| Item | Wrong Context | What Happens |
|------|--------------|--------------|
| **Headlamp** | Stealth mission | Your forehead lights up like a beacon. Every enemy sees you. Stealth fails. |
| **Spotlight** | Indoor social event | Blinding an NPC at dinner is not "making an entrance." -reputation 10. |
| **Radio Jammer** | Listening to radio for news | You jam your OWN radio. Miss a weather warning. Storm hits unprepared. |
| **EMP Device** | Near your own car | Your car electronics die. -20% car condition. The irony is not lost on you. |
| **Stink Bomb** | On a first date | There are no words. The date leaves. A nearby dog also leaves. -15 sanity. |
| **Voice Soother** | During a fight | Your smooth, calming voice enrages your opponent more. "Stop being REASONABLE!" Damage +50%. |
| **Eldritch Candle** | Children's event | The green flame terrifies everyone under 12. Mass crying. You're asked to leave. -karma 2. |
| **Binding Portrait** | On yourself | You feel a tug. A pull. The portrait BLINKS — with your eyes. Sanity -10. You've bound yourself. Unclear consequences. |
| **Fire Launcher** | Inside a building | You set the building on fire. Everyone evacuates. Including you. You lose your shelter. |
| **Tear Gas** | Windy day | The gas blows back into your face. -health 15. You stumble into traffic. A passing car honks. It's the NPC you were trying to gas. |
| **Kingpin Look** | Pawn shop while broke | Gus sees the look but your wallet is empty. "All flash, no cash. I charge you double now." |
| **Gentleman's Charm** | Talking to animals | The cologne confuses the dog. It follows you for 3 days demanding belly rubs. You can't refuse. It's a companion now. |
| **Devil's Deck** | Playing Solitaire | You win, as always. But you wagered against yourself. Something intangible leaves you. -1 random stat. |
| **Forged Documents** | At your own bank | The bank compares your real ID to the forged one. Both have your photo. Security holds you for 2 hours. Miss next event. |
| **Mobile Workshop** | During a date | You absentmindedly disassemble the restaurant table. The waiter is speechless. Your date is... impressed? 50/50. |
| **Pursuit Package** | Running FROM something | The whistle you blow to coordinate your escape also signals the thing chasing you. It runs faster. |
| **Luck Totem** | At a funeral | The LUCK TOTEM rattles. A bird flies through the window. It lands on the casket. The deceased's family stares at you. "Did you... summon that?" |
| **Cool Down Kit** | In winter | Hypothermia speedrun. -20 health. You deserve this. |
| **Storm Suit** | At a pool party | You show up in full weather gear to a poolside event. Nobody speaks to you. But you don't get sunburned. Silver lining. |

---

## 45. Quality Pass — Rewritten Weak Event Narratives

> The original Section 37 (Disguises), 38 (Tonics), 40 (Luxury), 41 (Vehicle), and parts of 42 (Tier 2) followed a pattern of "item does what item does." A Low-Profile Outfit makes you low-profile. Boring.
>
> Below are **complete replacement drafts** for every weak entry. These replace the originals in Sections 37–42. Each event now has: unexpected consequences, meaningful choices, trade-offs, or emergent weirdness.

---

### 45A. Disguises — Rewritten (Replaces Section 37)

> Old pattern: "Wear disguise → avoid detection." Every event was "item makes you invisible."  
> New pattern: Disguises create unexpected IDENTITIES. NPCs react to who they THINK you are, not just whether they see you. Every disguise has a failure mode and a bonus nobody expected.

#### Low-Profile Outfit (4 events — rewritten)

**Event 1: Casino Recognition** — `events_day_wealth.py`
```
Trigger: casino area, recognized, has_item("Low-Profile Outfit")
Narrative: "The LOW-PROFILE OUTFIT turns you invisible — too invisible. The 
           cocktail waitress assumes you're staff and hands you a tray of 
           drinks. You could deliver them (access to VIP rooms) or set the 
           tray down and walk to the high-roller table unnoticed."
Choice: Deliver drinks → access VIP back rooms, overhear a tip worth $200.
  Or: slip to high-roller table → play one hand at increased stakes before 
  anyone realizes you don't belong. 
Consequence: If you delivered drinks, the real waiter gets fired. You see 
  them outside later, crying. -1 karma if you don't help them.
```

**Event 2: Police Encounter** — `events_day_dark.py`
```
Trigger: police checkpoint, has_item("Low-Profile Outfit")
Narrative: "The cop glances at your LOW-PROFILE OUTFIT and waves you through— 
           then stops. 'Hold on. You match a description.' Not YOUR 
           description. Someone else's. Someone who owes the mob money."
Choice: Play along ("That's not me, officer") → free pass, but the mob
  hears you were spotted → mob event in 3-5 days, looking for the REAL guy  
  but finding you instead. Or: admit you're nobody → cop searches you. If 
  you're clean: free. If carrying contraband: problem.
```

**Event 3: Street Mugging** — `events_night.py`
```
Trigger: attempted mugging, has_item("Low-Profile Outfit")
Narrative: "The mugger looks at your LOW-PROFILE OUTFIT. Pauses. 'Marcus? 
           Holy crap, Marcus? It's me, Danny from juvie!' He thinks you're 
           someone he knows. He puts the knife away and starts CRYING. 'I 
           thought you were dead, man.'"
Choice: Play along as "Marcus" → Danny becomes a contact who knows the 
  criminal underworld (3 future discounts on shady deals). Or: admit 
  you're not Marcus → Danny's grief turns to rage → fight. Or: hug him 
  silently → he gives you $30 and a phone number, walks away happy.
  If you played along: Danny will eventually figure it out. In 7 days: 
  a very angry event.
```

**Event 4: Homeless Shelter** — `events_day_people.py`
```
Trigger: charity/social event, has_item("Low-Profile Outfit")
Narrative: "The LOW-PROFILE OUTFIT works. A church volunteer hands you a 
           warm meal, a sleeping bag, and a card for a job interview. 'We 
           believe in second chances,' she says. The food is incredible. 
           The sleeping bag is better than anything you own."  
Effect: Free food (+10 health), new item: 'Donated Sleeping Bag' (+comfort 
  at night). But: the job interview card is REAL. In 3 days: an event where 
  you show up. If you go: honest money ($100/week for 3 weeks). If you 
  skip: nothing. The volunteer remembers your face either way.
```

#### Beach Bum Disguise (3 events — rewritten)

**Event 1: Rich People Think You're Entertainment** — `events_day_wealth.py`
```
Trigger: luxury/party event, has_item("Beach Bum Disguise")
Narrative: "In the BEACH BUM DISGUISE, the yacht party assumes you're the 
           hired entertainment. The host shoves a ukulele in your hands. 
           'Play something tropical!' You don't play ukulele. Or do you?"
Choice: Wing it → 50% chance you're terrible (they laugh, give you $50 
  for being a good sport, free food all night) or 50% you're inexplicably 
  amazing (tips: $200, the host's wife gives you her number, husband notices).
  Or: refuse → they assume you're a gatecrasher → bounced out, lose access.
Consequence (if amazing): The host hires you for next party. Recurring $200 gig.
```

**Event 2: Heat Wave** — `events_day_survival.py`
```
Trigger: extreme heat, has_item("Beach Bum Disguise")
Narrative: "Everyone wilts in the heat. You, in the BEACH BUM DISGUISE, 
           are perfectly comfortable — the sunscreen is doing god's work. 
           Too comfortable. You fall asleep on a park bench. When you wake 
           up, someone has left a donation cup in front of you. It has $23 
           in it. A passing dog has also fallen asleep on your lap."
Effect: +$23. Dog companion offered (temporary, 2-day duration). Immune 
  to heat. But: a photograph of you sleeping on the bench goes viral on 
  the local community Facebook group. Some NPCs recognize "the bench guy."
```

**Event 3: Beach Bum Actually Finds Beach Bums** — `events_day_people.py`
```
Trigger: wandering/social event, has_item("Beach Bum Disguise")
Narrative: "A group of actual beach bums wave you over. 'One of us!' They 
           share their food (questionable), their wisdom (surprisingly deep), 
           and their scheme to sneak into the water park after hours."
Choice: Join the water park scheme → fun adventure mini-event, +sanity, 
  +$0, but you find $80 in the wave pool filter. 15% chance security catches 
  you → hilarious chase scene, -$40 fine. Or: just hang out → +sanity, 
  they teach you a survival trick (+5 to next outdoor survival event).
```

#### Gas Mask (3 events — rewritten)

**Event 1: Toxic Spill** — `events_day_survival.py`
```
Trigger: chemical/toxic event, has_item("Gas Mask")
Narrative: "Toxic fumes. Everyone runs. You put on the GAS MASK and walk 
           straight in. You breathe pine-scented air while stepping over 
           unconscious bodies. And then you see it — the source of the spill 
           is a truck full of expensive chemicals. Unguarded. Leaking money."
Choice: Loot the chemicals ($200-$500 depending on what you grab) and leave 
  → karma -2, but you're rich. Or: find the truck driver unconscious, drag 
  him to safety → he's a chemical company exec, gives you a $300 reward and 
  a job offer (future recurring income event). Or: seal the spill yourself 
  → +karma 3, local news covers you as "The Gas Mask Hero," +20 reputation, 
  but the chemical company sues you for touching their property. $100 legal fee.
```

**Event 2: Fire in a Building** — `events_day_dark.py`
```
Trigger: fire/smoke event, has_item("Gas Mask")
Narrative: "Smoke fills the building. You pull on the GAS MASK. Everyone runs 
           OUT. You walk IN. Through the smoke: a safe, door open. Someone 
           left in a hurry. Also: a cat on a shelf, meowing. The fire is 
           getting worse."
Choice: Grab the safe's contents ($400) → karma -1, nobody knows. Or: 
  save the cat → the cat's owner is the building manager, eternal gratitude, 
  free access to the building's roof (useful in future events). Or: grab 
  BOTH → you trip on the cat, drop half the money, the cat scratches your 
  face. $200 + cat companion (angry cat, 1 loyalty). The fire dept arrives 
  and you're standing there holding a scratched face, a cat, and a fistful 
  of cash. They have questions.
```

**Event 3: Swamp Adventure** — `adventures.py`
```
Trigger: swamp zone, has_item("Gas Mask")
Narrative: "Swamp gas that drops grown men rolls past the GAS MASK's filters. 
           But the mask fogs up. You can breathe but can't see. You navigate 
           by sound. And the sounds in this swamp are... wrong. Something 
           large is breathing nearby. It's not hostile. It's curious."
Effect: Immune to swamp gas. But: the creature following you turns out to 
  be a 200-lb snapping turtle. If you have Animal Bait: it becomes a 
  terrifying but loyal companion. If not: it follows you to the swamp edge 
  and stares as you leave. For the rest of the game, 5% chance events in 
  swampy areas mention "something large watching from the water."
```

#### Storm Suit (3 events — rewritten)

**Event 1: Hurricane** — `events_day_survival.py`
```
Trigger: severe weather, has_item("Storm Suit")
Narrative: "Hurricane-force winds. Trees uprooting. You stand in the STORM 
           SUIT like a lighthouse. Then a lawn chair hits you. Then a mailbox. 
           Then a PERSON. They grab onto you because you're the only thing 
           not moving. You are a human anchor."
Effect: Immune to storm damage. +1 companion (temporary — the person who 
  grabbed you). They're terrified and grateful. After the storm: they offer 
  you $150. Choice: take the money or refuse → they remember you forever 
  and send help during future survival events (NPC ally, 30% trigger rate).
```

**Event 2: Flash Flood** — `events_car.py`
```
Trigger: flood, has_item("Storm Suit")
Narrative: "The flood rises. Your car floats. YOU don't float — the STORM 
           SUIT is waterproof but heavy. You wade through chest-deep water 
           to higher ground. On the way: a submerged car with the trunk 
           popped open. Something glints inside."
Choice: Investigate trunk → random valuable item ($50-$300) but the current 
  is strong, -10 health from the effort. Or: keep moving → safe, no loot. 
  Or: wait for flood to recede → your car takes damage but you find the 
  trunk item AND two other things washed up. Patience rewarded.
```

**Event 3: Storm Suit at Night** — `events_night.py`
```
Trigger: cold/rain at night, has_item("Storm Suit")
Narrative: "The STORM SUIT traps your body heat. You're warm while the world 
           freezes. But the rustling waterproof fabric sounds like something 
           moving through leaves. At 2am, a security guard flashlights your 
           location. He thought you were a bear. He's armed."
Effect: Immune to cold. But: 25% chance of security encounter. Talk your 
  way out → no issue. Fail → he calls police → minor hassle. If you have 
  Forged Documents: flash them, he apologizes and leaves you a coffee.
```

#### Brass Knuckles (4 events — rewritten)

**Event 1: Bar Fight** — `events_day_people.py`
```
Trigger: confrontation, has_item("Brass Knuckles")
Narrative: "The other guy swings first. Your BRASS KNUCKLES connect with his 
           jaw. One punch. He goes down. The bar goes quiet. Then the 
           bartender says: 'That guy runs a tab here. You just inherited it.'
           It's $47. Also: the guy you hit? His GIRLFRIEND is now looking 
           at you. With interest."
Effect: Win fight. But: inherit $47 bar tab (pay or owe the bar). The 
  girlfriend becomes a contact — she's the one who remembers you. In 3 
  days: she tips you off about a job ($200). Her ex finds out. That's 
  a future event.
```

**Event 2: Mugging Defense — But They Work for Someone** — `events_day_dark.py`
```
Trigger: mugging, has_item("Brass Knuckles")
Narrative: "The mugger sees the BRASS KNUCKLES and backs off. Smart. But 
           as he leaves, he pulls out a phone. 'Boss? Yeah, that one's 
           armed.' He wasn't freelancing. He was scouting for someone bigger."
Effect: Avoid mugging. But: in 3-5 days, a more organized crew shows up. 
  They don't attack — they offer you a JOB. "Someone who fights like that 
  is wasted getting mugged." Choice: take the job (criminal work, $300, 
  -karma) or refuse (they respect it, leave, but remember you).
```

**Event 3: Animal Attack** — `events_day_animals.py`
```
Trigger: aggressive animal, has_item("Brass Knuckles")
Narrative: "You punch the coyote. With BRASS KNUCKLES. It yelps and runs. 
           Then it comes back. With friends. You've punched the alpha. 
           Now you're the alpha. Eight coyotes sit in a semicircle, waiting 
           for instructions."
Effect: 60% chance — coyotes scatter permanently. 40% chance — you've 
  accidentally formed a coyote pack. They follow you for 2 days, scaring 
  away every threat AND every friendly NPC. Having a coyote escort is 
  cool but socially ruinous.
```

**Event 4: Knocking on a Locked Door** — `events_day_dark.py`
```
Trigger: locked building event, has_item("Brass Knuckles")
Narrative: "You COULD use finesse. Instead, you knock on the locked door 
           with BRASS KNUCKLES. The lock breaks on the third hit. So does 
           the door frame. And part of the wall. You've less 'picked' the 
           lock and more 'removed the concept of a door.'"
Effect: Bypass locked door. But: the noise draws attention. 50% chance 
  someone investigates (choose: hide, flee, or intimidate). The building 
  owner later sues for $100 in damages. If you have Forged Documents: 
  the lawsuit goes to your fake identity. Problem solved.
```

#### Gentleman's Charm (3 events — rewritten)

**Event 1: VIP Access — But They Think You're Someone** — `events_day_wealth.py`
```
Trigger: VIP event, has_item("Gentleman's Charm")
Narrative: "The GENTLEMAN'S CHARM gets you past the rope. Then: 'Alejandro! 
           You came!' A woman in diamonds kisses both cheeks. She thinks 
           you're someone named Alejandro. Alejandro apparently owes her 
           $5,000. But Alejandro also has a reservation at the best table."
Choice: Be Alejandro → best table, free champagne, VIP treatment. But 
  eventually she asks about the $5,000. Stall (+charm) or confess. 
  Or: correct her → she's embarrassed, you lose VIP access but she gives 
  you $50 as an apology for the confusion. The real Alejandro never shows.
  Who IS Alejandro? (5% chance this seeds a "Find Alejandro" mini-quest.)
```

**Event 2: Negotiation Turns Personal** — `events_day_people.py`
```
Trigger: deal/negotiation, has_item("Gentleman's Charm")
Narrative: "The silk handkerchief from the GENTLEMAN'S CHARM catches their 
           eye. 'My grandfather had one just like that,' they say. Their 
           voice breaks. The negotiation stops. This is no longer about 
           money. This is about their dead grandfather."
Effect: +50% better deal IF you let them talk about grandpa. Takes time — 
  you miss the next event window. Or: push through the business → normal 
  deal, no bonus, but the NPC thinks you're cold. Future deals with them 
  are 10% worse. Or: give them the handkerchief → they give you 200% the 
  deal value out of gratitude. But you lose the handkerchief component. 
  The Gentleman's Charm now works without it (degraded: +20% instead of +30%).
```

**Event 3: Charm at a Dive Bar** — `events_day_people.py`
```
Trigger: low-class social event, has_item("Gentleman's Charm")
Narrative: "You walk into the dive bar smelling like the GENTLEMAN'S CHARM. 
           Cologne. Silk. The regulars stare. 'Who the hell invited James Bond?' 
           One guy slow-claps. Another buys you a beer 'because you clearly 
           need one.' A third offers to arm-wrestle you for $20."
Effect: +free beer (tiny health). Arm wrestle: win (+$20) or lose (-$20 but 
  you earn their respect). Either way: these guys become bar contacts. They 
  hear things. Future events: 15% chance a bar regular tips you off about 
  something useful.
```

#### Forged Documents (4 events — rewritten)

**Event 1: Identity Check** — `events_day_dark.py`
```
Trigger: ID check/verification, has_item("Forged Documents")
Narrative: "You hand over the FORGED DOCUMENTS. The officer squints. 
           'Dr. Robert Chen?' 'Yes.' A long pause. 'Doctor, there's a 
           medical emergency two blocks away. We need you.' The ID was 
           TOO good. You're now a doctor."
Choice: Help at the medical emergency → use common sense, 70% chance you 
  stabilize the patient (+$200, +karma 3, newspaper press, +reputation). 
  30% you panic and make it worse (+heat, someone records it, video goes 
  local). Or: refuse → "What kind of doctor are you?" → suspicion, search.
  Or: run → they chase you. Doctors don't run.
```

**Event 2: Hospital Visit** — `events_illness.py`
```
Trigger: medical treatment needed, has_item("Forged Documents")  
Narrative: "FORGED DOCUMENTS: Veteran status. Free treatment. But the nurse 
           recognizes the format. 'Which unit?' she asks. She's a veteran 
           too. Real one. And she has follow-up questions."
Effect: 50% chance — your bluff holds, free treatment + veteran contact who 
  invites you to a weekly poker game (+recurring gambling option). 50% — 
  she catches the fake. She doesn't call security. She just looks at you 
  with such disappointment that you lose 5 sanity. She treats you anyway. 
  "Because that's what we do." You can't come back here.
```

**Event 3: Bank Visit** — `events_day_wealth.py`
```
Trigger: financial event, has_item("Forged Documents")
Narrative: "FORGED DOCUMENTS say clean credit history. Loan approved: $1000. 
           Easy money. Except the documents also show a permanent address. 
           The bank will mail statements there. Someone LIVES there. In 5 
           days: that someone shows up, confused. They've been getting YOUR 
           mail."
Effect: +$1000 loan. But: in 5 days, the address owner creates a problem. 
  Choice: pay them off ($200 to stay quiet), charm them (Gentleman's Charm 
  helps), or let it escalate → police report → +30 heat.
```

**Event 4: Checkpoint** — `events_day_survival.py`
```
Trigger: checkpoint/restricted area, has_item("Forged Documents")
Narrative: "The FORGED DOCUMENTS clear the checkpoint. The guard salutes. 
           Behind the checkpoint: a restricted zone. Military supply caches. 
           Medical supplies. And a second checkpoint. This one has DOGS. 
           Dogs can't read forged documents."
Effect: Past first checkpoint → loot opportunity ($100-$400 in supplies). 
  Second checkpoint: if you have Animal Bait or Animal Magnetism → dogs 
  are pacified, proceed further (bonus loot). If not: dogs alert, you 
  flee with whatever you grabbed. Either way: you know this place exists 
  now. It's marked on your map for future visits (with better preparation).
```

---

### 45B. Tonics & Consumables — Rewritten (Replaces Section 38)

> Old pattern: "Have problem → use tonic → problem solved." Every event was a one-button fix.  
> New pattern: Tonics have side effects, over-performance, moral tangles, and cascading consequences. Consumability matters — using the item UP should feel like a DECISION, not a reflex.

#### Antacid Brew (3 events — rewritten)

**Event 1: Food Poisoning at a Business Dinner** — `events_illness.py`
```
Trigger: food poisoning / nausea, has_item("Antacid Brew")
Narrative: "The shrimp was bad. You feel it. Under the table, you chug the 
           ANTACID BREW. The fizzing is... loud. Everyone stares. 'What was 
           that noise?' You burp with the force of a foghorn. Silence. Then 
           the host laughs. Then everyone laughs. You've become the legend 
           of this dinner party. 'The Burp Guy.' Forever."
Effect: Cured. Item consumed. +social reputation as 'that guy.'
  Future social events: 10% chance someone calls you Burp Guy. It's 
  endearing. +5 social bonus when recognized. Weirdly, this is better 
  for your reputation than being normal.
```

**Event 2: Poisoned By An NPC** — `events_day_dark.py`
```
Trigger: NPC offers food/drink, poison flag, has_item("Antacid Brew")
Narrative: "You sip the drink. Immediately wrong. Your tongue goes numb. 
           Poison. You slam the ANTACID BREW before the toxin hits your 
           stomach. Fizz vs. poison. Fizz wins. Barely. The NPC watches, 
           expressionless. They know you know. You know they know you know."
Effect: Survive poisoning. Item consumed. But: the NPC is now aware 
  you're prepared. Choice — confront them (risky: they might have a weapon) 
  or leave calmly and mark them as hostile (future events: this NPC becomes 
  a rival). If you have Blackmail Letter: additional option to leverage 
  the attempted murder for $500 and permanent NPC compliance.
```

**Event 3: Drinking Contest** — `events_day_people.py`
```
Trigger: competition/contest event, has_item("Antacid Brew")
Narrative: "Someone challenges you to a hot wings eating contest. Six rounds 
           in, your opponent surrenders. You feel fine. The ANTACID BREW 
           neutralized every capsaicin molecule. The crowd carries you on 
           their shoulders. You're the Wing King. The restaurant offers you 
           free food for a month."
Effect: Win contest. +$100 prize. Free food (heals 5 health/day for 7 
  days). Item consumed. Title: "Wing King" — 15% of food-related events 
  go better because staff recognize you. The losing opponent wants a 
  rematch. In 5 days: they show up with Carolina Reapers.
```

#### Trail Mix Bomb (3 events — rewritten)

**Event 1: Animal Encounter Goes Wrong** — `events_day_animals.py`
```
Trigger: aggressive animal, has_item("Trail Mix Bomb")
Narrative: "You light the TRAIL MIX BOMB and throw it at the charging bear. 
           Seeds explode. Fire scatters. The bear... sits down. It's eating 
           the trail mix. The fire part? It lit a bush. The bush is between 
           you and your car. The bear is eating. The bush is burning. You 
           need to choose: past the bear or through the fire."
Choice: Past the bear → 70% chance it ignores you (it's busy eating), 30% 
  it's still agitated and swipes → -15 health. Through the fire → -10 
  health guaranteed, but you're at your car. Wait → the fire department 
  comes. They also see the bear. It becomes a regional news story. Your 
  car is in the background. Anyone looking for your car now knows the area.
```

**Event 2: Distraction That Works Too Well** — `events_day_people.py`
```
Trigger: social event, need to escape/distract, has_item("Trail Mix Bomb")
Narrative: "The TRAIL MIX BOMB pops and scatters burning seeds across the 
           restaurant floor. Perfect distraction. Except: the fire sprinklers 
           trigger. Everyone's drenched. The pianist keeps playing. A dog runs 
           in from outside to eat the seeds. Two children start screaming with 
           joy. Total chaos. You escape through the kitchen. The chef gives 
           you a bread roll on the way out, unbothered."
Effect: Escape. Item consumed. +bread roll (tiny health). The restaurant 
  bans you if they figure it out (30% chance). The two children tell their 
  mom about 'the seed firework man.' In 3 days: the mom finds you and 
  demands you do it again at their birthday party. ($0 pay, but +karma, +sanity.)
```

**Event 3: Night Camp Defense** — `events_night.py`
```
Trigger: night intruder, has_item("Trail Mix Bomb")
Narrative: "Something's circling your camp. You throw the TRAIL MIX BOMB 
           blind into the dark. POP. Seeds and fire scatter. A raccoon 
           screams. A second raccoon screams. A THIRD raccoon — how many 
           are there? — runs directly at you in blind panic and climbs 
           your leg like a tree. You now have a raccoon on your head."
Effect: Threat repelled. Item consumed. But: raccoon. It stays until morning. 
  It steals one small item from your inventory overnight. When it leaves, 
  it drops a different item it stole from somewhere else. Net neutral or 
  net positive depending on what it takes vs. what it gives.
```

#### Animal Bait (3 events — rewritten)

**Event 1: Companion Recruitment — Too Many Applicants** — `events_day_companions.py`
```
Trigger: animal companion opportunity, has_item("Animal Bait")
Narrative: "You set out the ANIMAL BAIT for the stray dog. The dog comes. 
           So does a cat. And a possum. And a raccoon. And a HAWK. They 
           all sit in a semicircle, looking at you expectantly. You can 
           only take one. The others will be... disappointed."
Choice: Pick one → the chosen companion. The others leave sad. But: the 
  HAWK follows from the sky for 2 days and occasionally drops things on 
  NPCs you're talking to. Helpful? Unclear. The possum plays dead 
  dramatically whenever anything happens — witnessed by NPCs who are 
  deeply confused.
```

**Event 2: Hunting — Ethical Dilemma** — `events_day_survival.py`
```
Trigger: food crisis/hunting, has_item("Animal Bait")
Narrative: "The ANIMAL BAIT works. A deer approaches. This is the part where 
           you hunt it. Except: the deer is a doe. And she has a fawn behind 
           her. They both stare at you with enormous brown eyes. The fawn 
           does a little hop."
Choice: Hunt anyway → full food (+30 health), but -3 karma, and the fawn 
  runs away into the woods (seeds a future event where you see a fully 
  grown deer that flinches when it sees humans). Or: don't hunt → the doe 
  leads you to a berry bush she knows about. +15 health, +2 karma. The 
  fawn nuzzles your hand. You didn't eat but you feel full somehow.
  Item consumed either way.
```

**Event 3: Animal Bait in the City** — `events_day_animals.py`
```
Trigger: urban area, has_item("Animal Bait")
Narrative: "You drop ANIMAL BAIT in the city. In the forest, this summons 
           deer. In the city, this summons: 14 pigeons, a very confident 
           rat, someone's escaped parrot, and a man named Gary who claims 
           he can also 'smell opportunity.' Gary is not an animal. Probably."
Effect: Item consumed. Gain nothing useful from the animals (they're city 
  animals, they have nothing). But Gary: Gary is a fence who deals in 
  stolen goods. He offers to buy anything you're selling at 80% of value, 
  no questions asked, forever. He gives you a business card. It says 
  "Gary. I Know A Guy." Gary is a contact now.
```

#### Stink Bomb (3 events — rewritten)

**Event 1: Mugging Defense — Nuclear Option** — `events_day_dark.py`
```
Trigger: mugging, has_item("Stink Bomb")
Narrative: "You crack the STINK BOMB. The mugger gags. You gag. EVERYONE 
           gags. A woman across the street vomits into her purse. A dog 
           faints. The mugger drops his knife and crawls away. The smell 
           spreads. Police respond to a 'gas leak.' You're four blocks 
           away before the air clears. The knife is still on the ground."
Effect: Escape mugging. Item consumed. Bonus: pick up the knife (free weapon). 
  But: the area is quarantined for 6 hours. If you had any allies in the 
  area, they were also caught in the stink. NPC relationships in the area 
  -5. The mugger? He'll never forget your smell. Literally — he can 
  track you by it for 2 days.
```

**Event 2: Stink Bomb at a Negotiation** — `events_day_people.py`
```
Trigger: negotiation/meeting, has_item("Stink Bomb")
Narrative: "Negotiations stall. You 'accidentally' crack the STINK BOMB 
           under the table. The room empties in 20 seconds. You calmly 
           pick up the contract, sign it yourself, and leave. By the time 
           they come back, the deal is done and legally binding."
Effect: Win negotiation by default. Maximum terms. Item consumed. But: 
  they KNOW. This NPC will never negotiate with you in an enclosed space 
  again. Future deals must be outdoors. Also: -10 reputation with anyone 
  who was in the room. One of them blogs about it. "Worst Meeting Ever."
```

**Event 3: Stink Bomb in a Car** — `events_car.py`
```
Trigger: passenger/hitchhiker event, has_item("Stink Bomb")
Narrative: "The hitchhiker won't leave your car. He's been talking for an 
           hour. You crack the STINK BOMB in the back seat. His face goes 
           green. He opens the door at 40mph and rolls into a ditch. 
           Clean exit. The smell stays. For days. Every NPC who gets in 
           your car comments on it."
Effect: Remove unwanted passenger immediately. Item consumed. But: car 
  "smell" debuff for 5 days. Any NPC interactions in the car are at -20%. 
  Companions refuse to ride. The lingering smell attracts one specific 
  type of person: a retired chemistry professor who finds the chemical 
  composition "fascinating." He becomes an optional contact.
```

#### Voice Soother (3 events — rewritten)

**Event 1: Talking Down a Jumper** — `events_day_dark.py`
```
Trigger: crisis/desperate NPC event, has_item("Voice Soother")
Narrative: "They're on the edge. Literally. You uncap the VOICE SOOTHER, 
           take a sip. Your voice becomes velvet. 'Come here. We'll figure 
           this out.' They listen. They step back. They collapse into your 
           arms sobbing. You saved a life with cough drops dissolving in 
           minty water. How is this real?"
Effect: +karma 5. +sanity 10. The person you saved gives you their watch  
  ($80 value) and says you're the only good person they've met. In 5 days: 
  they find you and repay you threefold with a favor (cash, item, or info — 
  player choice). Item consumed. This is the best use of a Voice Soother.
```

**Event 2: Voice Soother at Karaoke** — `events_day_people.py`
```
Trigger: performance/karaoke event, has_item("Voice Soother")
Narrative: "One sip. Your voice drops an octave and gains three octaves of 
           range. You sing 'Bohemian Rhapsody' and the bar goes SILENT. 
           Not polite silence. REVERENT silence. The bartender pours you a 
           drink he keeps behind the top shelf. A record producer in the 
           back hands you his card. This is insane."
Effect: +$150 in tips. Record producer contact (future income event: 
  $300 one-time "demo recording" if pursued). Item consumed. But: you're 
  now known as "that singer." 10% of future social events, someone asks 
  you to sing. You don't have the Voice Soother anymore. You're about to 
  be VERY disappointing. (This seeds a comedy event.)
```

**Event 3: Interrogation Counter** — `events_day_dark.py`
```
Trigger: police/authority questioning, has_item("Voice Soother")
Narrative: "Sip. Your voice smooths to silk. You answer every question 
           perfectly. Too perfectly. The detective's partner whispers: 'He's 
           either innocent or the best liar I've ever seen.' They let you go. 
           But they assign a tail. For 3 days, an unmarked car follows you."
Effect: Pass interrogation. Item consumed. But: 3-day surveillance. Any 
  illegal activity during surveillance = instant bust. If you're clean 
  for 3 days: they lose interest. If you notice the tail (requires 
  Binocular Scope or Spotlight): option to confront or shake them.
```

#### Outdoor Shield (3 events — rewritten)

**Event 1: UV Event — The Farmer** — `events_day_survival.py`
```
Trigger: sunburn/UV event, has_item("Outdoor Shield")
Narrative: "OUTDOOR SHIELD applied. The sun can't touch you. You walk past 
           a group of farm workers melting in the heat. One of them, sun-
           blistered and desperate, asks what you're using. You show them."
Choice: Share the Outdoor Shield → item consumed, but: the farmer remembers 
  you. He's connected. Future events: 20% chance a farm worker gives you 
  free produce when you encounter them. Or: keep it → immune to UV, no 
  loss, but the farmer mutters something about city people.
```

**Event 2: Bug Swarm — The Nest** — `adventures.py`
```
Trigger: bug swarm in adventure, has_item("Outdoor Shield")
Narrative: "OUTDOOR SHIELD repels the mosquitoes. But it doesn't repel YOUR 
           curiosity. You follow the swarm to its source — a nest the size 
           of a basketball. Inside: amber. Actual fossilized amber with 
           something trapped inside. Could be worth money. Could be nothing."
Effect: Unique find — 'Mystery Amber.' Pawn value: $50 guaranteed. BUT: 
  10% chance Gus identifies it as containing a prehistoric insect worth 
  $500 to the right buyer. He offers to broker the deal (he keeps $150).
```

**Event 3: Night Glow Incident** — `events_night.py`
```
Trigger: night rest, has_item("Outdoor Shield")
Narrative: "You applied OUTDOOR SHIELD before bed. The UV-reflective layer 
           catches the full moon. You glow faintly blue. A night jogger 
           spots you and SCREAMS. She runs. She tells the neighborhood 
           Facebook group. 'THE GLOWING MAN IS REAL.' The post gets 400 
           comments."
Effect: +reputation 10 as 'supernatural figure.' Future events: 15% chance 
  NPCs are either scared of you or in awe. One NPC brings you offerings 
  (food, small items). Another NPC brings a priest. The priest is confused 
  but gives you a blessing (+1 luck for 3 days). This is all from sunscreen.
```

#### Cool Down Kit (3 events — rewritten)

**Event 1: Heatstroke Save — The Ice Cream Truck** — `events_day_survival.py`
```
Trigger: extreme heat, has_item("Cool Down Kit")
Narrative: "You're applying the COOL DOWN KIT when an ice cream truck 
           passes. The driver sees you pouring water on your head and stops. 
           'Rough day?' He gives you a free ice cream. You sit on the curb, 
           dripping wet, eating a Rocket Pop. Cars pass. Life is briefly, 
           impossibly perfect."
Effect: Heat immunity. +5 sanity (moment of peace). The ice cream driver 
  becomes a contact — he drives a ROUTE. Knows the area. Tips you off 
  about events happening in different zones. Item consumed.
```

**Event 2: Overheating Car — The Gamble** — `events_car.py`
```
Trigger: car overheating, has_item("Cool Down Kit")
Narrative: "You dump the COOL DOWN KIT on the engine. Steam geysers. The 
           cold water hits the hot block. Metal groans. Something POPS. 
           Then silence. Then... the engine starts. Smoother than before."
Effect: 75% chance — fix overheat + bonus 5% car condition (the rapid 
  thermal cycle fixed a warped seal). 25% chance — cracked gasket, -15% 
  car condition. You won't know which happened until the next car event.
  The uncertainty is the point. Item consumed.
```

**Event 3: Cool Down Kit on a Companion** — `events_day_companions.py`
```
Trigger: companion overheating/stressed, has_item("Cool Down Kit") 
Narrative: "Your companion is panting/sweating. You dump the COOL DOWN KIT 
           on them. They gasp. Then they shake (if animal) or glare (if 
           human). Then: 'Actually, that felt amazing.' Loyalty +20. They 
           look at you differently now. Like you care."
Effect: Companion health fully restored. Loyalty +20. Item consumed. If  
  animal companion: they fetish-ly follow you near any water source from 
  now on, expecting a repeat. +comedy dialogue.
```

#### Smoke Flare (3 events — rewritten)

**Event 1: Stranded — Wrong Rescue** — `events_day_survival.py`
```
Trigger: stranded/lost, has_item("Smoke Flare")
Narrative: "You fire the SMOKE FLARE. Black smoke billows. Within an hour, 
           three responses: a helicopter (news crew), a fire truck (thought 
           it was a wildfire), and a man in a pickup who 'just likes driving 
           toward smoke.' The news crew interviews you. The fire truck 
           charges you $200 for a false alarm. The pickup guy offers you 
           jerky and a ride."
Choice: Ride with pickup guy → free ride, he talks the whole time about 
  conspiracy theories, 50% of which turn out to be TRUE events you 
  encounter later. Or: argue fire truck fee → it escalates, you end up 
  paying $100 (negotiated). Or: do the news interview → +reputation, +heat.
  Item consumed.
```

**Event 2: Pursuit Escape — The Decoy** — `events_day_dark.py`
```
Trigger: being chased, has_item("Smoke Flare")
Narrative: "SMOKE FLARE drops behind you. Thick smoke. But your pursuer 
           knows about smoke screens — they run straight through it. What 
           they DON'T expect: the smoke flare also caught a dumpster on 
           fire. They run through smoke into a wall of heat and stagger. 
           You're three blocks away, on a bus, eating a granola bar."
Effect: Escape pursuit. Item consumed. Dumpster fire triggers fire dept 
  response. The area is cordoned off for a day — any events in that area 
  are replaced with "construction zone" events (potentially useful if 
  you needed to avoid that area anyway).
```

**Event 3: Smoke Flare at a Party** — `events_day_people.py`
```
Trigger: party/social gathering, has_item("Smoke Flare")
Narrative: "Someone dares you to do something crazy. You launch the SMOKE 
           FLARE off the balcony. It arcs across the night sky, trailing 
           orange fire. Everyone on the balcony CHEERS. Someone films it. 
           It goes moderately viral. '#BalconyFlare' trends locally."
Effect: +$0. But: +sanity 5, +reputation 15, everyone at the party becomes 
  a contact. Item consumed. Downside: fire marshal investigates, $50 fine. 
  But: the video catches something in the background nobody noticed at 
  the time. An NPC approaches you in 3 days: "I saw your video. Can we 
  talk about what was behind the smoke?" Storyline hook.
```

#### Vermin Bomb (3 events — rewritten)

**Event 1: Rat Infestation — The Kingdom** — `events_day_survival.py`
```
Trigger: vermin infestation, has_item("Vermin Bomb")
Narrative: "You set off the VERMIN BOMB. Chemical death rolls through the 
           building. Rats pour out. Hundreds. The stream of fleeing rats 
           CROSSES A ROAD. Traffic stops. A news crew arrives. The mayor's 
           office issues a statement. You are now responsible for what the 
           press calls 'Ratpocalypse Tuesday.'"
Effect: Infestation cleared. Item consumed. +15 reputation as 'the person 
  who exposed the rat problem.' The city hires an exterminator — but the 
  exterminator is terrible and wants YOUR help. Mini-quest: exterminate 
  rats for $200. Requires: another Vermin Bomb or any fire-based item.
```

**Event 2: Car Pests — Discovery** — `events_car.py`
```
Trigger: pests in car, has_item("Vermin Bomb")
Narrative: "VERMIN BOMB under the hood. Chemical blast. Mice flee. Spiders 
           flee. Something you can't identify flees. But as the smoke 
           clears: the mice were nesting on something. A bundle of $20 
           bills, chewed at the edges. Previous owner's emergency fund. 
           $140, minus what the mice ate."
Effect: Clear pests. +$140. Item consumed. The car smells like chemicals 
  for 3 days but runs better now (-5% decay rate for a week). If you 
  had a companion: they refuse to ride for 1 day due to the chemical smell.
```

**Event 3: Vermin Bomb as a Weapon** — `events_day_dark.py`
```
Trigger: building standoff/confrontation, has_item("Vermin Bomb")
Narrative: "They're barricaded inside. The VERMIN BOMB goes through the mail 
           slot. What follows is: chemical cloud, screaming, the sound of a 
           grown man slipping on something, a door flying open, and three 
           people running out coughing and covered in a substance you hope 
           is pest control residue."
Effect: Clear any occupied building. Item consumed. The people inside 
  drop items in their panic (1-2 random items). But: is this a war crime? 
  Not technically. But the look on the responding officer's face suggests 
  you're in a gray area. +5 heat unless you have Forged Documents to 
  explain yourself as "city pest control."
```

---

### 45C. Luxury Crafts — Rewritten (Replaces Section 40)

> Old pattern: "Have luxury item → auto-win social event." Zero consequences for wealth display.  
> New pattern: Luxury items project an image that ATTRACTS as much as it OPENS. Wealth makes you a target. Power has a cost. Every social auto-win also paints a bullseye.

#### Kingpin Look (3 events — rewritten)

**Event 1: Casino — You're The Mark Now** — `events_day_casino.py`
```
Trigger: casino, has_item("Kingpin Look")
Narrative: "The KINGPIN LOOK gets you the high-roller table. Gold chain, 
           cigar, the works. The pit boss smiles. The dealer nods. But 
           across the room, three men in cheap suits are watching. They 
           don't work here. They're here for whoever sits at that table."
Effect: High-roller access (+better blackjack limits). But: post-session, 
  the three men approach. They either: (a) try to rob you in the parking 
  lot — fight/flee/talk options, (b) offer you a "business opportunity" 
  that's actually money laundering, or (c) one of them IS an undercover 
  cop running a sting. You don't know which until it happens.
```

**Event 2: Street Cred — Someone Believes It** — `events_day_dark.py`
```
Trigger: criminal area, has_item("Kingpin Look")
Narrative: "The gang respects the KINGPIN LOOK. They think you're connected. 
           The leader nods. 'We got a problem. Rival crew. You handle it, 
           we cut you in.' He thinks you're here to help. You're not. But 
           saying 'no' to someone with face tattoos feels unwise."
Choice: Handle it → criminal side quest, $500, -karma 3, but you're now 
  allies with a gang (useful for future dangerous events). Or: stall for 
  time → leave before things get real, but they remember you made promises.
  In 5 days: they come asking. Or: admit you're nobody → 50% they laugh 
  and let you go, 50% they take the gold chain "as compensation for 
  wasting our time." Lose Kingpin Look component.
```

**Event 3: Business Meeting — The Offer** — `events_day_people.py`
```
Trigger: business event, has_item("Kingpin Look")
Narrative: "The KINGPIN LOOK walks into the meeting room. They assume 
           you're the investor. You're not. But the pitch is... actually 
           good? It's a food truck business. The numbers work. The name? 
           'Kingpin's Kitchen.' They want to use YOUR image."
Choice: Invest → costs $300 upfront. In 10 days: the food truck opens. 
  It either succeeds ($100/week passive income for the rest of the game) 
  or fails (-$300, nothing). 70/30 odds. Or: just take the branding deal 
  → $50/week for using your look in their ads. Your face is on a food 
  truck now. NPCs recognize you. Some think it's cool. Some think it's sad.
```

#### Enchanted Vintage (3 events — rewritten)

**Event 1: Social Gathering — The Truth Serum** — `events_day_people.py`
```
Trigger: party/gathering, has_item("Enchanted Vintage")
Narrative: "You share the ENCHANTED VINTAGE. The first sip makes everyone 
           honest. Brutally, uncomfortably honest. The host admits she hates 
           her own party. A guest confesses to stealing office supplies. 
           Another admits he's been wearing a toupee since 2003. The wine 
           doesn't just bond people — it EXPOSES them."
Effect: +social max. Everyone at the party is now deeply bonded through 
  mutual vulnerability. But: one confession is SERIOUS — someone admits 
  to a crime. Choice: report it (+karma, -social), keep quiet (+social 
  bond with everyone, -karma), or blackmail them (Blackmail Letter not 
  required — you witnessed it, $400, -karma 3). Enchanted Vintage loses 
  one charge.
```

**Event 2: Companion Bonding — Too Deep** — `events_day_companions.py`
```
Trigger: companion rest, has_item("Enchanted Vintage")
Narrative: "You share the ENCHANTED VINTAGE. The conversation goes deeper 
           than expected. Your companion tells you something they've never 
           told anyone. It's heavy. It's real. You wish you could unlearn 
           it. But now you understand them. Completely."
Effect: Companion loyalty MAX. Companion happiness +30. But: companion 
  gained the "Vulnerability" flag. Future events where the companion is 
  humiliated/in danger hit HARDER — you care more. Mechanical: companion 
  loss events cause double sanity damage. The bond is real. That's the 
  cost. Enchanted Vintage loses one charge.
```

**Event 3: Drinking Alone** — `events_night.py`
```
Trigger: alone at night, no companion, has_item("Enchanted Vintage")
Narrative: "Nobody to share it with. You drink the ENCHANTED VINTAGE alone. 
           The wine is perfect. The silence is perfect. And for the first 
           time in weeks, you cry. Not from sadness — from relief. The 
           weight lifts. Just for tonight. Tomorrow it comes back. But 
           tonight? Tonight you're okay."
Effect: +15 sanity, +10 health. Enchanted Vintage loses one charge. But: 
  a subtle flag gets set — "Alone At Night" counter. If this happens 3 
  times: a unique event triggers where a stray animal or a wandering NPC 
  finds you and just... sits with you. No dialogue. Just presence.
```

#### Heirloom Set (3 events — rewritten)

**Event 1: Pawn Shop — Gus Has Questions** — `locations.py`
```
Trigger: pawning, has_item("Heirloom Set")
Narrative: "Gus spots the HEIRLOOM SET's pen. Squints. Pulls out a loupe.
           'This monogram. VRM. Where'd you get this?' His hands are 
           shaking. 'I've been looking for this pen for thirty years. It 
           belonged to my father. He disappeared in 1987.'"
Choice: Tell the truth (you made it at a workbench) → Gus is crushed 
  but grateful for the honest answer. +10% pawn value permanently out of 
  respect. Or: make up a story → Gus believes you, pays $200 for the 
  pen. But guilt: -2 karma. In 5 days: Gus realizes the monogram was 
  hand-scratched, not professional. He's angry. All future pawn values 
  drop 10% until you apologize.
```

**Event 2: Antique Fair** — `events_day_wealth.py`
```
Trigger: market/fair event, has_item("Heirloom Set")
Narrative: "The HEIRLOOM SET catches the eye of an antique dealer. 'This 
           watch — is it a 1931 Hamilton?' It's not. You made it from a 
           pocket watch and cologne. But she's convinced. She offers $400."
Choice: Sell for $400 (she'll discover it's fake in a week — NPC becomes 
  a nemesis). Or: admit it's a craft → she's impressed by the quality, 
  offers $100 (honest price). She becomes a recurring buyer for crafted 
  items (+15% value for anything crafted you sell to her). Or: offer to 
  appraise HER items → she has a box of junk, but one piece is worth $200. 
  You split the profit.
```

**Event 3: Formal Event** — `events_day_people.py`
```
Trigger: formal/social event, has_item("Heirloom Set")
Narrative: "The HEIRLOOM SET's pen signs the guest book. The host examines 
           your signature. 'Good penmanship. Strong hand.' They seat you 
           at the head table. Between a retired senator and a woman who 
           'does imports.' The senator is boring. The importer is... not."
Effect: Access to the head table → information. The importer offers you 
  a job: transport a package from A to B. $500. She won't say what's in 
  it. Choice: take the job (it's fine — 80% legal import, 20% it's drugs 
  and you have to decide what to do mid-transport). Or: decline politely 
  → she respects it, gives you her card for future opportunities.
```

#### Aristocrat's Touch (3 events — rewritten)

**Event 1: Gala — The Imposter** — `events_day_wealth.py`
```
Trigger: gala/fancy event, has_item("Aristocrat's Touch")
Narrative: "The ARISTOCRAT'S TOUCH — gloves and silk — sells the illusion. 
           You're seated with billionaires. The conversation turns to yachts. 
           You don't own a yacht. You don't own a BOAT. But the gloves are 
           so convincing that when you say 'mine's a forty-footer,' everyone 
           nods. Then someone asks for photos."
Choice: Bluff deeper → you need to find a yacht photo fast. If you have 
  Evidence Kit: snap a stock photo from google — believed. +$200 investment 
  offer. If not: caught. Humiliating. Ejected. -10 reputation. Or: 
  admit you're not wealthy → they're charmed by your honesty. The oldest 
  billionaire invites you to his private poker game. "I like someone who 
  can't afford to lose."
```

**Event 2: Cold Snap** — `events_day_survival.py`
```
Trigger: cold weather, has_item("Aristocrat's Touch")
Narrative: "The ARISTOCRAT'S TOUCH gloves keep your hands warm. The silk 
           handkerchief wraps your neck. But you're walking past a 
           shivering kid at a bus stop. Their gloves have holes. Yours 
           are leather. Italian. The kid looks at your hands."
Choice: Give them the gloves → lose Aristocrat's Touch glove component. 
  -30% effectiveness. +karma 3. The kid's parent sees, comes running, 
  gives you a homemade scarf (equivalent item). In 10 days: the parent 
  returns your gloves, cleaned, with a thank-you note and $30. Or: 
  walk by → you're warm. They're cold. -0 karma because no one saw. 
  But YOU know. -2 sanity.
```

**Event 3: Aristocrat's Touch at a Fight** — `events_day_dark.py`
```
Trigger: physical confrontation, has_item("Aristocrat's Touch")
Narrative: "Someone throws a punch. You catch their fist in the ARISTOCRAT'S 
           TOUCH leather gloves. 'I'd prefer we discuss this like 
           gentlemen,' you say. The leather creaks. Their knuckles crack. 
           You're squeezing harder than you realize."
Effect: De-escalate OR escalate — your choice. De-escalate: they back 
  down, impressed. +reputation. Escalate: the leather gloves function 
  like soft brass knuckles. You win the fight but the gloves are damaged. 
  Need repair (Mobile Workshop) or -20% effectiveness.
```

#### Power Move Kit (3 events — rewritten)

**Event 1: Intimidation — The Lighter Trick** — `events_day_dark.py`
```
Trigger: confrontation/threat, has_item("Power Move Kit")
Narrative: "You snap the POWER MOVE KIT's lighter. Click. The flame dances. 
           You light the cigar. Slow. The aggressor watches the flame, not 
           your face. You speak through smoke: 'Walk away.' They walk away. 
           Then you realize the lighter is also near a gas tank. That was 
           closer than you thought."
Effect: Intimidation success. But: 10% chance the gas tank spark triggers 
  a small fire. If fire: -$50 in damage, local fire response. You look 
  dumb. The aggressor comes back because you're clearly not a threat—just 
  an arsonist. Different kind of intimidation needed.
```

**Event 2: Closing a Deal — The After-Cigar** — `events_day_people.py`
```
Trigger: negotiation, has_item("Power Move Kit")
Narrative: "You offer a cigar from the POWER MOVE KIT. They accept. You 
           smoke together in silence. The negotiation that seemed impossible 
           resolves itself. Not through words — through the shared ritual 
           of tobacco and fire. When it's done, you shake hands. The deal 
           is better than you expected. The cigar cost $2."
Effect: Best possible deal terms. +NPC relationship. But: the cigar supply 
  is finite. Power Move Kit has 5 "charges" (cigars). Each use consumes 
  one. When they run out, the kit still has the lighter (half as effective). 
  Restock cigars at the convenience store ($15).
```

**Event 3: Night Campfire — The Memory** — `events_night.py`
```
Trigger: night rest, has_item("Power Move Kit")
Narrative: "You start the fire with the POWER MOVE KIT lighter. Cigar in 
           hand, stars above. For the first time in a long time, you 
           remember who you were BEFORE all this. The memory stings. But 
           the cigar smoke carries it away. Tomorrow you'll survive. 
           Tonight you'll just... be."
Effect: +10 sanity. Night fully restful. But: the memory flag sets. In 
  2-3 days: a dream event about your past. It might be good. It might 
  be painful. The campfire opened a door you can't close.
```

#### Animal Magnetism (3 events — rewritten)

**Event 1: Too Magnetic** — `events_day_companions.py`
```
Trigger: companion recruitment, has_item("Animal Magnetism")
Narrative: "The ANIMAL MAGNETISM's cologne draws the companion to you. 
           Perfect. But it also draws: a second animal, a third, and a 
           very confused mail carrier who can't explain why he walked 
           toward you. Animals line up. The mail carrier apologizes and 
           slowly backs away."
Effect: Guaranteed companion recruitment. +50% bonus. But: the extra 
  animals follow you for a day, causing minor chaos at every location. 
  Shops take 10% longer. NPCs are distracted by your animal entourage. 
  One animal steals a small item from a shop — you get blamed. $20 fine 
  OR give back the item (which is weirdly useful).
```

**Event 2: Predator Confusion** — `events_day_animals.py`
```
Trigger: predator encounter, has_item("Animal Magnetism")
Narrative: "The predator charges. Then stops. Sniffs. The ANIMAL MAGNETISM 
           confuses its prey instinct. You smell like... alpha. Like 
           territory. Like 'this one fights back.' The predator circles 
           twice, then lies down and rolls over. It's... submitting."
Effect: Predator pacified. But: 15% chance the predator FOLLOWS you. 
  Having a bear following you through town creates PROBLEMS. NPCs 
  panic. Police are called. But: if you lead it to the forest exit, 
  a wildlife officer rewards you $100 for "safe animal handling." If 
  the bear enters a shop: chaos, property damage, hilarity.
```

**Event 3: Animal Magnetism at a Date** — `events_day_people.py`
```
Trigger: social/romantic event, has_item("Animal Magnetism")
Narrative: "The date is going well. The ANIMAL MAGNETISM's cologne is 
           working on humans too. Your date leans in. Then a pigeon 
           lands on your head. Your date laughs. A second pigeon lands. 
           They laugh harder. A third. Fourth. By pigeon seven, your 
           date can't breathe from laughing. Best date they've ever had."
Effect: +NPC relationship MAX (through comedy). Future dates with this 
  NPC always attract pigeons. It becomes "your thing." This is the only 
  item that makes romance events funnier instead of more dramatic.
```

#### Luck Totem (3 events — rewritten)

**Event 1: Gambling — The Streak** — `events_day_casino.py`
```
Trigger: gambling event, has_item("Luck Totem")
Narrative: "The LUCK TOTEM hums. You win. And win. And WIN. The streak is 
           unnatural. The pit boss watches. Other players notice. One 
           elderly woman at the slot machine asks to touch the totem 'for 
           luck.' If you let her: she hits jackpot. Her family surrounds 
           you in gratitude. If you don't: she mutters a curse."
Choice: Let her touch it → she wins $500 (not your money). Her family 
  gives you $50 and free dinner. +karma 2. The totem glows warmer. 
  Or: refuse → she curses. -1 luck for 2 days. But: your own streak 
  continues. +15% gambling for this session. Selfish vs. generous — 
  the totem is testing you.
```

**Event 2: Loot Discovery — The Pattern** — `events_day_items.py`
```
Trigger: search/loot event, has_item("Luck Totem")
Narrative: "The LUCK TOTEM pulses. You reach into the junk pile and pull 
           out something valuable. Naturally. But this time the totem does 
           something new: it pulls your hand TWICE. You pull out a second 
           item. A photograph. Old. Faded. It shows this exact junk pile, 
           twenty years ago. And someone already found the valuable item 
           once before. They put it back. Why?"
Effect: Double loot from this event. But: the photograph seeds a mystery. 
  Why did someone return something valuable? In 5 days: an NPC approaches 
  you. "You found it. The thing that was supposed to stay hidden." This 
  leads to a mini-quest about a buried secret (literally or figuratively).
```

**Event 3: Lottery — Almost** — `events_day_numbers.py`
```
Trigger: lottery/numbers event, has_item("Luck Totem")
Narrative: "LUCK TOTEM vibrates. You pick numbers. The draw happens. You 
           got 5 out of 6. Agonizingly close. The totem is warm, almost 
           apologetic. You won $300 instead of $30,000. On the way home, 
           you find a $20 bill on the sidewalk. The totem pulses. Like it's 
           trying to make it up to you."
Effect: +$320 total ($300 lottery + $20 found). The totem establishes a 
  pattern: it gives you just enough. Never the jackpot. But never nothing. 
  The universe is in on this joke and it's barely trying to hide it.
```

---

### 45D. Vehicle Upgrades — Rewritten (Replaces Section 41)

> Old pattern: "Tire kit fixes tires. Lube fixes engines." Zero ambition.  
> New pattern: Car items interact with the world OUTSIDE the car. The car is your home, your weapon, your hiding spot, and your identity. Vehicle items should feel like having a base of operations.

#### Tire Ready Kit (3 events — rewritten)

**Event 1: Flat Tire — The Body** — `events_car.py`
```
Trigger: flat tire, has_item("Tire Ready Kit")
Narrative: "The TIRE READY KIT makes this a two-minute fix. Jack clicks, 
           tire rolls. But when you pull the flat off: something is INSIDE 
           the tire. A waterproof bag. Contains: $200 in 20s, a SIM card, 
           and a note that says 'DON'T LOOK FOR ME.' This was here when 
           you bought the car."
Choice: Keep everything (+$200, SIM card becomes an item that occasionally 
  receives cryptic texts — side storyline). Or: throw it all away (+karma 1, 
  nothing happens, probably). Or: take it to police (+karma 2, officer gives 
  you $50 finder's fee, but you're on their radar now).
  The SIM card storyline: every 3-5 days a text arrives. Each one references 
  a location in the game. Visit the locations in order → find a cache ($500).
```

**Event 2: Helping A Stranded Driver** — `events_day_people.py`
```
Trigger: stranded motorist, has_item("Tire Ready Kit")
Narrative: "Stranded woman with a flat. Your TIRE READY KIT fixes it in 
           three minutes. She stares. 'You carry a pre-mounted spare?' She's 
           impressed. She's also a mechanic. 'You know you've got a cracked 
           caliper, right? I can feel it in the jack vibration.' She offers 
           to fix it, for free, right now. But she needs you to hold the 
           flashlight for an hour."
Choice: Let her fix it → +15% car condition, lose 1 event window (the 
  hour passes). She becomes a recurring contact — best mechanic in the 
  game, better rates than the dealership. Or: decline → she shrugs, gives 
  you her card. You can call her later, but the caliper stays cracked 
  (seeds a future brake failure event — preventable if you visit her first).
```

**Event 3: Tire as a Weapon** — `events_day_dark.py`
```
Trigger: pursuit/chase, has_item("Tire Ready Kit")
Narrative: "They're gaining. You reach back, grab the spare from the TIRE 
           READY KIT, and roll it out the driver's side window Hail Mary 
           style. It bounces twice, catches their front wheel, and they 
           spin into a guardrail. You would be impressed with yourself, 
           but your hands are shaking too hard."
Effect: Escape pursuit. Tire Ready Kit loses spare (fixable at mechanic 
  shop for $25). The chase gets reported — witnesses describe your car 
  launching a tire. +10 heat, but the police report calls it "bizarre" 
  and nobody takes it seriously. The pursuing driver has a grudge now.
```

#### Power Grid (3 events — rewritten)

**Event 1: Dead Battery — The Broadcast** — `events_car.py`
```
Trigger: dead battery, has_item("Power Grid")
Narrative: "POWER GRID jumps the battery. Everything comes alive. But the 
           surge also wakes up the old radio. It's picking up a signal 
           that shouldn't exist — a pirate radio station broadcasting 
           from somewhere nearby. The DJ is giving stock tips. They're... 
           weirdly accurate?"
Effect: Battery fixed. +1 new radio station. The pirate station broadcasts 
  for 7 days. Each day: a tip. 3 are financial (+$50-$100 if acted on), 
  2 are about local events (heads-up on upcoming random events), 1 is 
  nonsense, and 1 is a direct message to YOU. "We know you're listening. 
  Meet us at [location]." Side quest hook.
```

**Event 2: Power Grid Weaponized** — `events_day_dark.py`
```
Trigger: someone tries to steal your car, has_item("Power Grid")
Narrative: "The thief pops the door. Touches the ignition. The POWER GRID, 
           wired to the frame, sends a jolt through the chassis. The thief 
           yelps, drops the screwdriver, and runs. Your car alarm didn't go 
           off because you don't HAVE an alarm. The Power Grid IS the alarm."
Effect: Prevent car theft. The thief drops their screwdriver (free tool). 
  But: 15% chance the jolt also shorts your headlights. -5% car condition. 
  The thief tells their friends about "the electric car." No car thief 
  targets you for 10 days. The screwdriver is marked — it's from a 
  specific shop. Tracking it leads to the thief's fence: discount black 
  market items if you approach non-aggressively.
```

**Event 3: Power Grid as a Gift** — `events_day_people.py`
```
Trigger: NPC with electrical problem, has_item("Power Grid")
Narrative: "The old man's RV won't start. Dead electrical. You hook up the 
           POWER GRID. His RV roars to life. He tears up. 'My wife and I 
           lived in this for thirty years,' he says. 'She passed last month. 
           I was just going to drive it one more time.' He gives you a ring. 
           His wife's wedding ring. Worth $500. You try to refuse. He insists."
Effect: +$500 item (wife's ring). +karma 3. But: the ring is emotionally 
  weighted. If you pawn it: -karma 5, Gus comments on it darkly. If you 
  keep it: +1 luck permanently (sentimental items have passive bonuses in 
  this game). In 5 days: the old man dies peacefully. His RV is found 
  parked at a scenic overlook. You hear about it on the radio.
```

#### Miracle Lube (3 events — rewritten)

**Event 1: Engine Trouble — The Lemon** — `events_car.py`
```
Trigger: engine grinding, has_item("Miracle Lube")
Narrative: "MIRACLE LUBE fixes the grinding. But it also reveals something 
           worse — the oil runs clean in a spot where it should be dirty. 
           Your engine block has a MICRO-FRACTURE. The lube sealed it 
           temporarily. You have maybe 20 days before it opens again."
Effect: Immediate fix. +5% car condition. But: a 20-day timer starts. On 
  day 20: catastrophic engine failure unless you've visited a mechanic 
  ($200) or crafted Mobile Workshop + Miracle Lube (Auto Mechanic) to fix 
  it permanently. The game warns you at day 15: "Your engine makes a sound 
  it hasn't made since that day with the Miracle Lube." Tension.
```

**Event 2: Miracle Lube Opens a Safe** — `events_day_dark.py`
```
Trigger: locked safe/container, has_item("Miracle Lube")
Narrative: "The safe's hinges are rusted shut. No key will help — the 
           mechanism is frozen solid. A squirt of MIRACLE LUBE. Ten seconds. 
           The tumblers move. The handle turns. Inside: someone's hidden 
           stash. Cash, documents, and a photo of a family that doesn't 
           exist anymore."
Effect: +$150-$300 cash. The documents are property deeds — worthless 
  unless you find the property. The photo: if kept, becomes an emotional 
  item. Show it to certain NPCs and they react. One of them knows the 
  family. A 5-day breadcrumb quest to return the photo to a surviving 
  relative. Reward: $200 + an item from the family's old house.
```

**Event 3: Miracle Lube Smooths Everything** — `events_day_survival.py`
```
Trigger: stuck/jammed anything, has_item("Miracle Lube")
Narrative: "The water pump is seized. MIRACLE LUBE on the bearing. It spins. 
           The door hinge is frozen. MIRACLE LUBE. It swings. The old man's 
           wheelchair is stuck. MIRACLE LUBE on the axle. He rolls free. 
           'What IS that stuff?' he asks. You look at the bottle. 'Motor oil 
           and WD-40.' 'You should sell it,' he says. Maybe you should."
Effect: Fix any mechanical jam. But: the old man's suggestion seeds a 
  potential income stream. If you have 3+ Miracle Lubes (or crafting 
  materials to make them): option to set up a roadside lube stand. $30-50 
  per day for 5 days. NPCs pay for the magic lube. One of them is a 
  reporter. "Local Mechanic Sells Miracle Product." +reputation.
```

#### Mobile Workshop (3 events — rewritten)

**Event 1: Major Breakdown — The Rebuild** — `events_car.py`
```
Trigger: catastrophic repair needed, has_item("Mobile Workshop")
Narrative: "The engine drops. Literally. Half of it is on the road. The 
           MOBILE WORKSHOP unfolds. You spend four hours in a trance of 
           wrench-and-tape surgery. When you surface: the engine is back in. 
           It sounds... different. Better? You added something during the 
           rebuild — you're not sure what — but the car gained 5 MPH."
Effect: Full car repair. +5% car condition BEYOND previous max. The car 
  now has a quirk (random from: starts faster, runs quieter, horn sounds 
  different, dashboard light blinks morse code sometimes). The quirk is 
  cosmetic but makes the car feel alive and unique.
```

**Event 2: Mobile Workshop Builds an Invention** — `events_day_surreal.py`
```
Trigger: rest period + boredom flag, has_item("Mobile Workshop")
Narrative: "You open the MOBILE WORKSHOP with no intention. Your hands move 
           on their own. Forty minutes later: you've built a device. It's 
           a box with a crank and an antenna. When you turn the crank, it 
           plays music. But: you didn't install a speaker. Where is the 
           sound coming from? The box has no speaker. The music plays from 
           the air itself. You can't explain it. Nobody can."
Effect: New item: 'The Crank Box.' When used: +5 sanity, +5 companion 
  happiness. NPCs react with curiosity. Some are fascinated, some are 
  unnerved. One NPC offers $300 for it (sell or keep — it's one-of-a-kind). 
  If kept: 5% chance per night rest that the box plays by itself. The 
  song is always the player's actual "theme" — the events of that day, 
  translated into melody somehow. This can't be explained. Don't try.
```

**Event 3: Mobile Workshop Helps The Helpless** — `events_day_people.py`
```
Trigger: NPC needs repair, has_item("Mobile Workshop")
Narrative: "The family's car is wrecked. Three kids in the back. Dad is on 
           the phone with a tow truck that costs $300 he doesn't have. You 
           open the MOBILE WORKSHOP. Two hours later, their car runs. The 
           kids draw you a thank-you card. It says 'THANKYOU MR FIX IT' 
           in crayon. You keep it."
Effect: +karma 4. 'Kid's Thank-You Card' item — no mechanical value, but 
  it sits in your inventory as a reminder. If you're ever at critically 
  low sanity (<10), the card triggers a recovery event: you look at it 
  and remember there's good in the world. +10 sanity. One-time trigger, 
  but it's there when you need it most.
```

#### Pursuit Package (3 events — rewritten)

**Event 1: Chase — You're Faster** — `events_day_dark.py`
```
Trigger: chase/pursuit, has_item("Pursuit Package")
Narrative: "Running shoes hit pavement. Whistle coordinates your breathing. 
           The PURSUIT PACKAGE turns you into a missile. You catch them in 
           two blocks. Or — wait. They're running FROM something else. 
           Something bigger is behind BOTH of you."
Choice: Keep running (together — forced temporary alliance with whoever 
  you were chasing). Whatever's behind you: deal with it together or split 
  up. Together: +combat advantage if it's a fight, +companion for 1 day. 
  Split: solo event, standard difficulty. Or: stop and face it → reveal 
  what was chasing them. Could be anything: dog, cop, ex-girlfriend.
```

**Event 2: Pursuit Package at a Job** — `events_day_people.py`
```
Trigger: employment/work event, has_item("Pursuit Package")
Narrative: "A delivery service needs a runner. The PURSUIT PACKAGE makes you 
           the fastest courier in town. First delivery: $30. Second: $50. 
           Third: a package that's heavier than it should be. The address 
           it's going to doesn't exist. The phone number rings a voicemail 
           in a language you don't speak."
Effect: $80 from first two deliveries. Third delivery: choice. Deliver 
  it (to a location that turns out to be a dead drop — someone takes it 
  without showing their face, gives you $200 cash). Or: open it → 
  contents vary (medical supplies, 60%. Electronics, 30%. Something you 
  shouldn't have seen, 10% — seeds a thriller event chain). Or: return 
  to sender → the delivery service fires you. +karma.
```

**Event 3: Morning Run — The Witness** — `events_day_survival.py`
```
Trigger: morning/exercise event, has_item("Pursuit Package")
Narrative: "Morning run. PURSUIT PACKAGE shoes eat the miles. Five miles. 
           Seven. You're in a part of town you've never seen. Abandoned 
           buildings. A fence. Behind the fence: a man burying something. 
           He sees you. You see him. He's wearing a suit. This isn't 
           landscaping."
Choice: Run away → 90% clean escape. 10% he follows. If followed: 
  confrontation (the PURSUIT PACKAGE shoes outrun him, but he saw your 
  face). Or: hide and watch → see where he buries it. Return later with 
  digging tools → $300-$1000 cache. But: camera footage shows you in the 
  area. Or: confront him → he panics, offers $500 to forget what you 
  saw. Take the money or refuse. Either way: you now know about The Fence.
```

---

## 46. Craft Text Overhaul — The Amateur Crafter

> The player is NOT a professional. They're cobbling together items on a workbench in a gas station parking lot using duct tape, optimism, and YouTube tutorials they vaguely remember. Every craft text should capture the PROCESS — the failures, the confusion, the accidental genius, and the very real question of "why does this work?"
>
> **These replace the entries in Section 35.** Same `"craft_text"` field in the recipe dict.

---

### Tier 1 — 40 Items (Rewritten)

#### Gadgets

| Item | Craft Text (Replacement) |
|------|-----------|
| **Headlamp** | *You duct tape the flashlight to your forehead. It falls off. You add more tape. It falls off again. You tape it to a headband THEN tape the headband to your skull. It holds. You look like an idiot. You can see in the dark. Trade-offs.* |
| **Spotlight** | *You shove the flashlight into the binoculars backwards. Then forwards. Then sideways. Fifteen minutes of confused optics later, you accidentally create a beam that could guide aircraft. You have no idea which angle made it work. Don't touch it.* |
| **Evidence Kit** | *You wire the camera to the signal booster with a paperclip and hope. The first test photo transmits four miles and also to a random fax machine in Guatemala. Good enough.* |
| **Radio Jammer** | *"Reverse the polarity" sounded smart when you said it. What you actually did was unscrew things until the signal booster started screaming static. Nothing within earshot gets a signal. Including your own phone. Didn't think that through.* |
| **EMP Device** | *You pour battery acid on wires while holding your breath. Something sparks. Something else sparks. Everything in a twenty-foot radius goes dark, including the streetlamp you were working under. You finish assembly by feel. Your hands are shaking.* |
| **Distress Beacon** | *You crack open the LifeAlert and solder the signal booster's antenna onto it with a lighter and prayers. The range jumps from "your living room" to "three counties." The first test alert brings two ambulances and a news helicopter. Overkill, but functional.* |
| **Security Bypass** | *You disassemble the padlock to understand how pins work. Then you file the pocket knife into a tension wrench. It takes four hours, three cut fingers, and a moment of enlightenment that would concern a locksmith.* |

#### Disguises

| Item | Craft Text (Replacement) |
|------|-----------|
| **Low-Profile Outfit** | *Sunglasses tucked under the poncho hood. You check your reflection. You look like a background character in your own life. You say "hello" to yourself. Even you don't care. Perfect disguise.* |
| **Beach Bum Disguise** | *Sunscreen applied in thick, visible streaks. Shades at an angle that says "I have nowhere to be and I've accepted it." You test the look on a mirror. The mirror looks away. You've achieved weaponized apathy.* |
| **Gas Mask** | *You seal welding goggles with duct tape and shove air freshener filters where the real filters go. Your first breath tastes like a car dealership. Your second breath tastes like surviving. You'll take it.* |
| **Storm Suit** | *You break the umbrella trying to use it as a frame. You break a second umbrella. The third umbrella cooperates. Poncho over the frame, sealed with tape. You look like a walking tent. Rain hits you and slides right off. Worth every destroyed umbrella.* |
| **Brass Knuckles** | *Getting the padlock to nestle between the glove fingers takes twenty minutes and one accidentally punched workbench. The workbench now has a dent. Your hand now has a bruise. But the NEXT thing you punch will have a bigger dent and a bigger bruise. Science.* |
| **Gentleman's Charm** | *One drop of cologne on the silk handkerchief. Two drops. Three. The entire gas station smells like a department store. A passing woman actually stops and looks around. You've created a scent radius. Weaponized elegance.* |
| **Forged Documents** | *Your handwriting is terrible. You practice for thirty minutes. It's still terrible but now it's consistently terrible — and consistency reads as "official." The photo doesn't quite match but you draw the outline of a government seal with a ballpoint pen and frankly it's close enough for anyone who isn't looking hard.* |

#### Tonics & Consumables

| Item | Craft Text (Replacement) |
|------|-----------|
| **Antacid Brew** | *Baking soda into water. Stir. It fizzes like a tiny volcano. You take a test sip and your stomach immediately forgives you for everything you've eaten this week. Grandma was right. She was always right.* |
| **Trail Mix Bomb** | *Birdseed packed around matches, wrapped in a napkin. You test it by throwing it at a trash can. SEEDS EVERYWHERE. A flock of pigeons appears from nowhere. The matches didn't even light. That's fine. Version two: more matches. Version two works too well.* |
| **Animal Bait** | *Dog treats and birdseed in a ziplock bag. Simple enough. But when you open the bag to test the scent, a pigeon lands on your hand, a squirrel appears on the workbench, and something in the bushes makes a noise. You close the bag quickly. That was a LOT of interest.* |
| **Stink Bomb** | *You seal the tuna juice and baking soda container and immediately regret every life choice that led to this moment. Your eyes water through the SEALED jar. How? You don't know. Chemistry? A warning from God? The gas station attendant asks you to leave.* |
| **Voice Soother** | *Cough drops dissolve into the minty water. You take a sip and hum experimentally. Your voice drops half an octave and smooths out like jazz. You say "Good evening" to no one. It sounds like a movie trailer. You practice saying "Good evening" six more times.* |
| **Outdoor Shield** | *Sunscreen goes in first. Bug spray goes in second. You mix with a stick you found. The resulting paste smells like a tropical hardware store. You apply it to one arm as a test. A mosquito approaches, pivots six inches away, and flies directly into a wall. Effective.* |
| **Cool Down Kit** | *You mix the premium sunscreen with cold water bottles. The resulting mixture is chemically soothing and also just... cold. A cold thing that protects you from hot things. Look, not every invention needs to be complicated.* |
| **Smoke Flare** | *Matches in a garbage bag with trapped air. You seal it, poke a fuse hole, and light a test. Thick, angry smoke billows. You can't see. You can't breathe. You're two feet away and you've lost the workbench. By the time the smoke clears, you've drifted into the parking lot. It works GREAT.* |
| **Vermin Bomb** | *Pest control powder + baking soda accelerant in a sealed cup. The test detonation clears the workbench of ants you didn't know were there. Also the test cup. Also your confidence in the structural integrity of sealed cups. But the rats? They'll be GONE.* |

#### Dark Arts

| Item | Craft Text (Replacement) |
|------|-----------|
| **Eldritch Candle** | *You wrap the Necronomicon pages around the wax. On the third wrap, the candle lights. You didn't light it. Nobody lit it. The flame is green. You blow it out. It relights. You blow harder. It goes out. For now. Your hands are cold. The workbench is cold. Nothing is wrong. Probably.* |
| **Binding Portrait** | *Cursed ink from the envelope, applied carefully to the photograph. The pen moves easier than it should — like the ink WANTS to be here. You finish the last symbol and the photograph's subject blinks. Once. Clearly. You put it face-down and don't look at it for an hour.* |
| **Blackmail Letter** | *You transcribe the envelope's contents in your neatest handwriting. Halfway through, you realize you're writing threats to a person you've never met. The words are elegant. The implications are not. Your hand didn't shake once. That concerns you more than the letter.* |
| **Devil's Deck** | *Pass the cards through the candle flame. Ace of spades first. By the seventh card, the flame bends TOWARD the deck. By the twenty-second, you notice the face cards are looking at you. The jokers? The jokers are grinning. Wider than they were printed.* |
| **Fortune Cards** | *Super glue the penny to the ace of spades. Simple. But when you set the deck down, the cards shuffle. By themselves. Once. Neatly. You pick up the ace. The penny is warm. The deck reshuffles. You put it down, slowly, and step back.* |

#### Luxury Crafts

| Item | Craft Text (Replacement) |
|------|-----------|
| **Kingpin Look** | *Gold chain over the shoulders. Cigars in the pocket. You check the mirror and immediately hate that it works. You look like a man who owns things. You own a Gas Station Parking Lot Workbench Crafting Station. But they don't know that. THEY don't know that.* |
| **Enchanted Vintage** | *Pour the wine into the silver flask. It should taste like regular wine in a nicer container. It doesn't. It tastes BETTER. Like, transcendentally better. You take one more sip to confirm. Then one more. Stop. You're drinking your inventory. Cap it.* |
| **Heirloom Set** | *Pair the watch with the pen. Scratch fake initials into the pen cap with a nail. You hold them together and squint. It looks... inherited? Like someone's rich grandfather left them to you? You never had a rich grandfather. You barely had a regular grandfather. But holding these, you FEEL like you did.* |
| **Aristocrat's Touch** | *Gloves on, silk folded into the pocket. You adjust the silk three times. It has to look effortless, which takes incredible effort. You wave your gloved hand at an imaginary butler. Nobody's watching. You check. Then you do it again.* |
| **Power Move Kit** | *Lighter snaps. Cigar catches. You practice the motion — snap, light, lean back — fifteen times. By the eighth, it looks natural. By the fifteenth, you're genuinely concerned that you ENJOY this. You've become the person at the party. You don't even GO to parties.* |
| **Animal Magnetism** | *Apply cologne to the leather gloves. The smell is immediately overwhelming in the best way. You put on the gloves and shake your own hand. Confident. Trustworthy. You convince yourself you're a good person, just from a handshake. This is dangerously effective.* |
| **Luck Totem** | *Tie the rabbit foot to the lucky penny. The knot takes four tries. When it finally holds, the totem SWINGS — toward the northwest, specifically, like a compass. You rotate. It follows northwest. Toward what? You don't know. But something out there is lucky and it's calling you.* |

#### Vehicle Upgrades

| Item | Craft Text (Replacement) |
|------|-----------|
| **Tire Ready Kit** | *You pre-mount the spare and rig the jack to a bracket on the frame. The first test: you lift the car in 45 seconds. The second test: you drop the car because the bracket slipped. The third test: you add more bolts. It holds. Your mechanic would cry if she saw this. Tears of pride or horror, unclear.* |
| **Power Grid** | *Jumper cables wired to the fuse panel through a distribution block you made from a lunchbox. It looks like a bomb. It is not a bomb. You label it "NOT A BOMB" in Sharpie. This does not help. But it will jumpstart your car, stabilize the voltage, and run a camp light, so aesthetic concerns are secondary.* |
| **Miracle Lube** | *Motor oil and WD-40 in a squeeze bottle. You shake it. The mixture turns a color that doesn't exist in nature. You squeeze a drop onto the workbench hinge. The hinge, which has never been silent in its life, makes zero sound. You squeeze a drop on your shoe. Your shoe becomes frictionless. You need to be careful with this stuff.* |
| **Mobile Workshop** | *Tools strapped to duct tape rolls in a canvas bag. Wrench here, pliers there, socket set held together with ATTITUDE. You organize everything by "frequency of panic use." The most-grabbed tool is on top. It's the duct tape. It's always the duct tape.* |
| **Pursuit Package** | *Dog whistle taped to a lanyard. Running shoes laced tight. You test the whistle — no audible sound but three dogs within earshot go BERSERK. You test the shoes — fast. Too fast? No. Just fast ENOUGH for a person who may need to chase or be chased at any moment. That's your life now. Running shoes and a dog whistle. Don't think about it too hard.* |

### Tier 2 — 25 Items (Rewritten)

| Item | Craft Text (Replacement) |
|------|-----------|
| **Assassin's Kit** | *You strap the pepper spray to the shiv handle. The blade catches the light. The spray nozzle points forward. One weapon, two damage types. You test the grip. It feels natural. TOO natural. You set it down and stare at your hands like they belong to someone else. Where did you LEARN this?* |
| **Fire Launcher** | *Load the road flare into the slingshot. Pull back. It launches. It hits a dumpster. The dumpster is on fire. You didn't mean to hit the dumpster. You were aiming at the GROUND. The range on this thing is... concerning. You make three more projectiles and suddenly you're an artillery battery.* |
| **Tear Gas** | *Pepper spray meets stink bomb chemistry and the result is EVIL. Your eyes water through the sealed container. A passing bird changes direction mid-flight. You've created a Geneva Convention violation in a sandwich bag. You're not proud. But you're prepared.* |
| **Street Fighter Set** | *Shiv in the left hand. Brass knuckles on the right. You shadowbox the air. Left jab cuts, right hook breaks. You look ridiculous. You feel dangerous. These two feelings are not mutually exclusive. A pedestrian watches you punch air for thirty seconds and decides to cross the street.* |
| **Survival Bivouac** | *Emergency blanket draped over the fire starter kit setup. You crawl in. It's warm. It's dry. It smells like aluminum and hope. You were going to test it for five minutes but you fell asleep for forty. When you woke up, it was raining and you were dry. This thing works better than your apartment.* |
| **Hydration Station** | *Water purifier hose runs into the rain collector basin. The first test collects morning dew and filters it into the purest water you've ever tasted. You drink it. You fill a bottle. You drink that too. You've been dehydrated for three days and didn't know it. This machine just saved your life and it's made of a tarp.* |
| **Provider's Kit** | *Snare trap rigged next to the fishing rod in a carrying case. Land food. Sea food. All food. You bait both and wait. Two hours later: a rabbit in the trap and a bass on the line. You're eating like a man with a plan for the first time in weeks. The rod broke during retrieval. You fixed it with the trap's spare wire. This is who you are now.* |
| **Fortified Perimeter** | *Car alarm rigging wired to improvised trip-wire traps in a 50-foot radius. The first test triggers when a CAT walks through. The alarm screams. The trap pops. The cat is fine but deeply offended. Calibration complete. No cat, dog, human, or cryptid is getting within 50 feet without you knowing.* |
| **All-Weather Armor** | *Storm suit over outdoor shield application. You look like a HAZMAT worker who's also prepared for a beach vacation. You step outside during a thunderstorm to test it. Rain bounces off. Wind pushes and you don't budge. Lightning flashes and you realize you're standing in a field during a thunderstorm to prove a point. Priorities.* |
| **Master Key** | *Lockpick set integrated with security bypass tools into a single roll-up case. You test it on the workbench padlock. Open in four seconds. You test it on your car door. Three seconds. You test it on the gas station bathroom. Two seconds. You test it on the manager's office. He's inside. You apologize and close the door.* |
| **Night Scope** | *Headlamp focused through the binocular scope. The result turns 2am into noon with terrifying clarity. You can see the license plate on a car 200 yards away, in the dark. You can see a raccoon's FACIAL EXPRESSION at 100 yards. It looks guilty. You're going to see things you don't want to see. That's the cost of clarity.* |
| **SOS Kit** | *Signal mirror angled into the smoke flare launcher. Day or night, you can be found. The test launch sends smoke 200 feet up and the mirror catches it from a mile away. A helicopter pilot three counties over radios that he sees "some kind of distress signal." You wave them off. It was a test. They're not happy. But they found you — in eleven minutes.* |
| **Intelligence Dossier** | *Evidence kit records. Forged documents create cover. Together they form a dossier that could fool the CIA. You write a practice entry about yourself. Full background check, credit history, criminal record. All fake. All flawless. You read it and feel sad. This fictional version of you has better credit.* |
| **Surveillance Suite** | *Spotlight angled for scanning. Radio jammer set to block. You test it in the gas station parking lot. The spotlight catches every movement within 200 yards. The jammer kills every phone signal in the area. The gas station attendant comes out: "My phone's dead." Yours too. Friendly fire. Adjust the range.* |
| **Mind Shield** | *Dream catcher woven around worry stone, tied with a leather cord. You hold it. The anxiety in your chest—the one you forgot was always there—goes quiet. Not gone. Just quiet. Like it's behind a wall. You can still hear it, but distantly. You put the Mind Shield under your pillow. You sleep better than you have in weeks. What was the anxiety about? You can't remember. Good.* |
| **Fortune's Favor** | *Two lucky charms, bound with copper wire. The moment the wire closes the circuit, every coin in your pocket lands heads-up. You checked. The lotto ticket in your wallet — you scratch it. $5 winner. Coincidence? The second scratch: $10. The third: nothing. Even luck has limits. But the limits just moved.* |
| **Fate Reader** | *Lucky bracelet threaded through the fortune card deck. The cards deal themselves. Three. They land face up: Past, Present, Future. The Past card shows a room you recognize. The Present card shows this workbench. The Future card is blank. Then it's not. But what it shows — no. That can't be right. ...Can it?* |
| **Lucid Dreaming Kit** | *Eldritch candle placed in the center of the dream catcher. The green flame passes through the web strings without burning them. The strings GLOW. The whole thing hums at a frequency you feel in your teeth. You set it on your nightstand. That night, for the first time, the dream asks for YOUR permission.* |
| **Old Money Identity** | *Gentleman's charm combined with the heirloom set. You button the cuffs. Adjust the watch. Dab the cologne. Check the mirror. Staring back at you is a man who went to prep school and summers in Martha's Vineyard. He has opinions about wine. He played lacrosse. He's YOU. But also: not you. You're terrified of how easy this was.* |
| **New Identity** | *Low-profile outfit. Forged documents. You put it on. Open the passport. Look at the mirror. The name says Michael Torres. The face says nobody. You test it — walk into a diner where they KNOW you. The waitress says "What can I get you?" No recognition. None. The old you just... stopped. You order coffee as Michael. It tastes different.* |
| **Beast Tamer Kit** | *Animal bait and pet toy bundled together. You test it by setting it in the grass. Within five minutes: a squirrel, two birds, a stray cat, and something that might be a ferret? They line up. Orderly. Like students. The cat swats the squirrel. You say "No." The cat stops. WHY did the cat stop? You say "Sit." They sit. All of them. You're a Disney princess now.* |
| **Cheater's Insurance** | *Devil's deck paired with evidence kit. One cheats. The other covers. You test it at a solo card game. You win. Obviously. Then you photograph the winning hand, the card order, the shuffle pattern. The evidence looks like proof of FAIR play. You just documented your own cheat as honest. This is the most ethically bankrupt thing you've ever built. It's also the most useful.* |
| **Roadside Shield** | *Tire ready kit mounted next to power grid, all in the trunk. Pre-wired, pre-jacked, pre-everything. You simulate a breakdown. Flat tire AND dead battery simultaneously. Fixed in under five minutes. The car starts. The tire holds. You feel invincible. A car drives past and the driver waves, assuming you're a roadside mechanic. You almost believe it yourself.* |
| **Auto Mechanic** | *Mobile workshop opened, miracle lube loaded. Full diagnostic: pop the hood, feel the belts, check the fluid, listen to the engine. Your car makes a sound at 2000 RPM you've never heard. You apply lube. The sound stops. You apply more lube. The engine PURRS. It hasn't purred since the dealership. You scratch the dashboard. "Good car." You just talked to your car. The car said nothing back. Obviously. ...Obviously.* |
| **Rolling Fortress** | *Pursuit package strapped to the roof. Fortified perimeter wired to the chassis. Alarms on every door. Traps under the bumper. You test the alarm — a passing jogger triggers it from 30 feet. The traps deploy — a trash bag trips the line. The jogger screams. The trash bag is neutralized. You apologize to the jogger and spend ten minutes adjusting the sensitivity. Your car is now a bunker that goes 60 MPH. Mad Max would cry.* |

### Tier 3 — 12 Items (Rewritten)

| Item | Craft Text (Replacement) |
|------|-----------|
| **Road Warrior Armor** | *Three weapons fused into a harness of steel, spray, and flame. You strap it on. It's heavy. It's terrifying. You look at yourself in the car window and the person staring back is someone you don't entirely recognize. They look like they've been through something. You HAVE been through something. This armor is proof.* |
| **Third Eye** | *Mind shield, dream kit, and fate reader merge into a headband that HUMS. You put it on. The world looks the same. Then it doesn't. You see a shimmer around things — people, cars, doors — like heat haze. The shimmer around the next event is brighter than the rest. You know what happens tomorrow. You don't know how you know. The headband is warm.* |
| **Nomad's Camp** | *Bivouac. Provider's kit. Hydration station. All assembled, tested, deployed. You could live here. Not "survive" — LIVE. Shelter, food, water, warmth. You sit in the camp and for the first time, nothing is wrong. The silence is comfortable. The world could end tomorrow. You'd barely notice. You'd eat breakfast and watch the sunrise.* |
| **All-Access Pass** | *Master key, night scope, intelligence dossier. You hold all three and something shifts. Every locked door, dark hallway, and hidden password becomes trivial. The world has guardrails and you just found the staff entrance. The night scope shows you secrets. The key lets you in. The dossier tells you why it matters. You are the most informed lock-picker in human history.* |
| **Master of Games** | *Old money identity. Cheater's insurance. Enchanted vintage. You put together the ultimate con artist starter pack and feel your soul leave your body for just a second. You could buy a casino with borrowed money and a smile. You could out-bluff the devil. You could sell sand to a desert. You don't want to know what kind of person you are for building this. But it's built.* |
| **Immortal Vehicle** | *Auto mechanic. Rolling fortress. Roadside shield. The merge takes two hours and when it's done, your car is more machine than machine. Self-diagnosing. Self-defending. Self-repairing, almost. You turn the key and the car starts before you finish the motion. It KNEW. "Ready," you say to no one. The dashboard lights blink twice.* |
| **Gambler's Aura** | *Three layers of luck, braided and bound. The totem, the favor, the bracelet. You hold the finished aura against your chest. Your heart skips a beat. Then the coin on the ground catches your eye. Then the scratch ticket in the gutter. Then the $20 in the drain. It's already working. The universe has noticed you and it's embarrassed about everything it owes.* |
| **Ark Master's Horn** | *Beast tamer kit. Hydration station. Animal bait. The horn is just a rolled-up cone of tin, but when you blow it, every bird within earshot changes direction. Toward you. Dogs sit. Cats appear from nowhere. A fish jumps. Out of water. INTO YOUR HANDS. You are the Ark. The animals chose you.* |
| **Guardian Angel** | *SOS kit. Distress beacon. Fortified perimeter. All synchronized. Triple redundancy: if one system fails, two others catch you. You test all three simultaneously and three different emergency services respond. Again: you have to wave them off. But the response time? Under eight minutes. From three directions. Nothing can reach you that help can't reach faster.* |
| **Hazmat Suit** | *Gas mask over all-weather armor over storm suit components. Full coverage. You seal the last seam and realize you've built something that could walk through a chemical plant explosion. You put it on and your own breathing sounds like Darth Vader. Every step is a heavy thud. You are invulnerable to weather, gas, acid, and social interaction. Nobody talks to the hazmat guy.* |
| **Ghost Protocol** | *Surveillance suite. New identity. Mind shield. The ghost protocol doesn't make you invisible — it makes you IRRELEVANT. Cameras don't focus on you. Dogs don't bark. NPCs' eyes slide past you like you're furniture. You test it by standing in the middle of a crowded parking lot. Nobody looks. Nobody acknowledges. For five minutes, you don't exist. It's peaceful. Then it's terrifying. You take it off.* |
| **Dark Pact Reliquary** | *Eldritch candle. Binding portrait. Devil's deck. They merge and the temperature drops five degrees. The reliquary whispers. Not words — ALMOST words. Like someone speaking through a wall. The candle lights itself. The portrait's eyes move. The cards shuffle continuously, even sealed. You set it in your bag and the bag hums. The reliquary knows your name. You never told it.* |

### Tier 4 — 11 Items (Rewritten)

| Item | Craft Text (Replacement) |
|------|-----------|
| **Beastslayer Mantle** | *Gator tooth bonds to the road warrior armor. It shouldn't fit. It does. The tooth finds its place like it was always missing from the armor. When you put it on, you don't feel human. You feel like something that hunts humans. Every predator instinct you didn't know you had wakes up at once. A bird of prey circles overhead. Respect? Recognition? You nod at it. It nods back. No it doesn't. ...Does it?* |
| **Seer's Chronicle** | *The old journal's pages merge with the Third Eye's vision. Your handwriting appears on blank pages — but you're not writing. The chronicle IS writing. It describes tomorrow. Then the day after. Then next week. You try to read ahead. The pages go blank. "You're not ready for that yet," the chronicle seems to say. Not in words. In empty pages.* |
| **Wanderer's Rest** | *Walking stick planted. Nomad's camp deployed around it. Roots grow. Actually grow. From the stick. Into the dirt. In an hour, the camp has a living fence of vines that weren't there before. This isn't a camp anymore. It's a garden that showed up uninvited. You water the roots. The garden grows a tomato. ONE tomato. It's perfect.* |
| **Skeleton Key** | *All-Access Pass merges with the night scope. The key doesn't look like a key — it looks like UNDERSTANDING. You hold it near a door. The door's lock EXPLAINS itself to you. Tumblers, mechanism, intent. Why it was locked. What it's protecting. You could open it. Should you? The key doesn't judge. The key just knows.* |
| **King of the Road** | *The crown settles. You didn't make a crown — you made the Master of Games, and when you put it on, something in the world shifts. People notice you. Not your clothes, not your face — your GRAVITY. You walk into a room and conversations pause. You sit at a table and the dealer straightens up. Authority isn't earned or stolen. It's WORN. And it fits you terrifyingly well.* |
| **War Wagon** | *Artisan toolkit welds to the Immortal Vehicle. The car twitches. TWITCHES. Like a reflex. The dashboard lights cycle through a sequence you didn't program. The steering wheel adjusts itself to your hand size. The engine runs without the key. Your car isn't just fixed — it's AWAKE. You're not sure it sleeps anymore. When you park at night, you hear the engine humming. Softly. Like breathing.* |
| **Moonlit Fortune** | *Moon shard meets gambler's aura. The fusion happens at exactly midnight. Not approximately — exactly. The moon shard glows, the aura absorbs it, and luck becomes physics. Coins land how you want. Dice roll how you need. Cards fall where they should. It's not cheating. It's the universe paying a debt it didn't know it owed. Permanent luck. PERMANENT. The blackjack table is your kingdom. The math changed.* |
| **Leviathan's Call** | *Pearl meets the Ark Master's Horn. The pearl vibrates when you hold it near water. Any water. A puddle. A glass. A tear. The horn amplifies it into a call that travels through water, soil, and something else. You blow the horn by the river. The water stills. Then ripples. Something just acknowledged you from very, very deep down. The fish surface — not summoned. ATTENDING.* |
| **Last Breath Locket** | *Phoenix feather ignites inside the Guardian Angel's locket. The flame doesn't consume it — it LIVES inside, circling the chamber like a caged sun. You clasp it shut. Warm against your chest. Your heartbeat syncs with the flame. For one second, your heart stops. Then it starts again. Stronger. The locket didn't save your life. It CLAIMED it. Death has to go through the locket first now. And the locket doesn't open for anyone.* |
| **Phantom Rose** | *Metal rose inserted into the Ghost Protocol casing. The rose blooms. A metal flower, blooming. The petals open and inside: a mirror so small it fits in your palm. In the mirror: a hallway. You can't identify it but you've been there. That's the place between being seen and not being seen. You're a legend now. A story. A whisper that walks through walls. People who look for you will find only the rose's scent.* |
| **Soul Forge** | *Ritual token feeds the Dark Pact Reliquary. The whispers become a VOICE. Not threatening — negotiating. "What would you change?" it asks. "One moment. One choice. And I'll rewrite it." You think of every mistake. Every wrong turn. Every moment you wish you'd chosen differently. The Soul Forge waits. It's patient. It has all the time in the world. It has YOUR time. "Choose carefully," it says. "This is the only one you get."* |
