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

---

## 1. Current State Audit

### Item Counts by Category

| Category | Total Items | Active in Events | Narrative-Inert | Pawn Fodder Only |
|----------|------------|-----------------|-----------------|-----------------|
| Marvin Items (base) | 19 | 4 | **15** | 0 |
| Marvin Upgrades | 18 | 2 | **16** | 0 |
| Flasks | 12 | 1 | **11** | 0 |
| Crafted Items | 26 | 26 | 0 | 0 |
| Convenience Store | ~55 | ~50 | 0 | **1** (Lottery Ticket) |
| Quest/Story Items | ~40 | 40 | 0 | 0 |
| Adventure Rewards | ~30 | 30 | 0 | 0 |
| Food Items | ~15 | 15 | 0 | 0 |
| Car Parts | ~20 | 20 | 0 | 0 |
| **Totals** | **~235** | **~188** | **~42** | **~1** |

### The Core Problem

~18% of all items (the most expensive, hardest-to-get Marvin items and flasks) have **zero narrative presence**. A player spends $5,000–$22,000 on a Marvin item and it only exists as a blackjack mechanical buff. They never see it mentioned in events, never get a reaction from NPCs, never use it to solve a problem outside of cards. This makes the Marvin shop feel disconnected from the rest of the game.

Meanwhile, cheap convenience store items like Duct Tape, Pocket Knife, and Road Flares appear in 5+ event files and feel deeply woven into the world.

---

## 2. Gap Analysis — What's Inert

### Narrative-Inert Marvin Items (15 items — mechanics only, zero event text)

| Item | Price Range | Blackjack Effect | Problem |
|------|-----------|-----------------|---------|
| Delight Indicator | $3K–5K | Reads happiness stat | No event ever mentions it |
| Health Indicator | $3K–5K | Reads health stat | Only checked in player_core.py display |
| Dirty Old Hat | $9K–13K | Min bet drops to $1 | No NPC reacts to your hat |
| Golden Watch | $11K–15K | Increases table time | No one notices your watch |
| Sneaky Peeky Shades | $14K–18K | Peek at next card | No event text about wearing sunglasses |
| Lucky Coin | $4K–6K | 1x push recovery | Never flipped in a story moment |
| Worn Gloves | $7K–10K | Subtle card-feel luck | No one comments on your gloves |
| Tattered Cloak | $8K–12K | Dealer "forgets" bets | Invisible outside blackjack table |
| Rusty Compass | $3K–5K | Finds opportunities | Never used to navigate in events |
| Pocket Watch | $9K–13K | Extra rounds | Never pulled out in a story scene |
| Gambler's Chalice | $11K–15K | Double-bet draw | Never toasted, never spilled |
| Twin's Locket | $14K–20K | Split any pair | Never opened, never shown |
| White Feather | $5K–9K | Dignified surrender | Never caught the wind in a scene |
| Dealer's Grudge | $8K–12K | Side bet vs dealer | Never invoked in dealer dialogue |
| Gambler's Grimoire | $3K–5K | Stat tracker | Never read aloud, never quoted |

### Narrative-Inert Marvin Upgrades (16 items — same problem as above)

| Upgrade | Base Item | Effect | Problem |
|---------|-----------|--------|---------|
| Delight Manipulator | Delight Indicator | Adjusts happiness | Zero narrative |
| Health Manipulator | Health Indicator | Adjusts health | Zero narrative |
| Unwashed Hair | Dirty Old Hat | Better disguise | Zero narrative |
| Sapphire Watch | Golden Watch | Better VIP | Zero narrative |
| Sneaky Peeky Goggles | Sneaky Peeky Shades | Better peek | Zero narrative |
| Lucky Medallion | Lucky Coin | Better push | Zero narrative |
| Velvet Gloves | Worn Gloves | Better feel | Zero narrative |
| Invisible Cloak | Tattered Cloak | Better stealth | Zero narrative |
| Golden Compass | Rusty Compass | Better finding | Zero narrative |
| Grandfather Clock | Pocket Watch | More rounds | Zero narrative |
| Overflowing Goblet | Gambler's Chalice | Better double | Zero narrative |
| Mirror of Duality | Twin's Locket | Better splits | Zero narrative |
| Phoenix Feather | White Feather | Better surrender | Zero narrative |
| Dealer's Mercy | Dealer's Grudge | Better side bet | Zero narrative |
| Oracle's Tome | Gambler's Grimoire | Better tracking | Zero narrative |
| Real Insurance | Faulty Insurance | Better hospital | Zero narrative |

### Narrative-Inert Flasks (11 out of 12)

| Flask | Price | Mechanical Effect | Narrative Presence |
|-------|-------|-------------------|-------------------|
| Flask of No Bust | $10K–14K | Prevents busting 4 hands | durability.py only |
| Flask of Imminent Blackjack | $16K–22K | Increases BJ odds | Shop/durability only |
| Flask of Dealer's Whispers | $10K–14K | Reveals hole card | Shop/durability only |
| Flask of Bonus Fortune | $13K–19K | +bonus on wins | Shop/durability only |
| Flask of Anti-Venom | $9K–12K | Cures poison | Shop/durability only |
| Flask of Anti-Virus | $10K–12K | Cures illness | Shop/durability only |
| Flask of Fortunate Day | $4K–6K | Boosts day luck | Shop/durability only |
| Flask of Fortunate Night | $4K–7K | Boosts night luck | Shop/durability only |
| Flask of Second Chance | $11K–15K | Replay missed hand | durability.py only |
| Flask of Split Serum | $11K–16K | Split enhancement | durability.py only |
| Flask of Pocket Aces | $17K–22K | Guarantee ace | Shop/durability only |
| ~~Flask of Dealer's Hesitation~~ | ~~$8K–11K~~ | ~~Dealer delays~~ | **HAS narrative** in endings.py |

### Single Inert Store Item

| Item | Price | Problem |
|------|-------|---------|
| Lottery Ticket | $5 | Never checked anywhere — completely dead code |

---

## 3. Cross-File Interaction Map

How many event files check each item. Items appearing in only 1 file feel isolated.
Items appearing in 3+ files feel woven into the world.

### Most Connected Items (3+ files)

| Item | Files | Where |
|------|-------|-------|
| Animal Whistle | 8 | events_day_people, events_day_animals, events_night, adventures, events_day_companions, endings, events_day_storylines, locations |
| Pocket Knife | 5 | events_day_items, events_day_storylines, events_night, events_car, events_day_survival |
| Duct Tape | 4 | events_day_survival, adventures, events_car, systems (crafting) |
| Tool Kit | 4 | events_day_survival, events_day_storylines, events_car, locations |
| Flashlight | 3 | events_day_items, events_day_survival, events_night |
| Pest Control | 3 | events_day_survival, events_day_animals, events_night |
| Spare Tire | 3 | events_day_survival, events_car, locations |
| First Aid Kit | 3 | events_day_survival, events_day_items, events_illness |
| Binoculars | 3 | events_day_survival, events_night, events_day_items |
| Road Flares | 3 | events_day_survival, events_car, events_night |

### Isolated Items (1 file only)

| Item | File | What It Does |
|------|------|-------------|
| Pepper Spray | events_day_items | Robbery defense only |
| Shiv | events_day_items | Robbery defense only |
| Dream Catcher | events_day_items | Sleep quality only |
| Worry Stone | events_day_items | Sanity relief only |
| Slingshot | events_day_items | Bird hunt only |
| Signal Mirror | events_day_items | Rescue signal only |
| Rain Collector | events_day_items | Hydration only |
| Fire Starter Kit | events_day_items | Campfire only |
| Snare Trap | events_day_items | Rabbit trap only |
| Emergency Blanket | events_day_items | Cold protection only |
| Water Purifier | events_day_items | Clean water only |
| Home Remedy | events_day_items | Illness cure only |
| Lucky Charm Bracelet | events_day_items | Luck boost only |
| Road Flare Torch | events_day_items | Scare threats only |
| Splint | events_day_items | Injury prevention only |
| Scrap Armor | events_day_dark | Violence protection only |
| Lockpick Set | events_day_items | Lock opening only |
| Binocular Scope | events_day_items | Observation only |
| Fishing Rod | events_day_items | Fishing only |

**Pattern:** All 26 crafted items are active, but 19 of them only work in a single file (events_day_items.py). They never appear in night events, adventures, dark events, survival events, or people events.

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
