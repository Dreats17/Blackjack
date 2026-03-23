# BLACKJACK — Complete Game Index

> **51,971 lines of Python** across 32 game files.  
> **814 unique events** · **245 achievements** · **160+ items** · **11 endings**

---

# TABLE OF CONTENTS

1. [The Numbers](#the-numbers)
2. [Marvin's Mystical Merchandise (20 Items)](#marvins-mystical-merchandise)
3. [Witch Doctor Flasks (12 Types)](#witch-doctor-flasks)
4. [Crafting Recipes (26)](#crafting-recipes)
5. [Convenience Store (90 Items)](#convenience-store)
6. [Companions (8 + 3 Adventure)](#companions)
7. [Locations & Services (19)](#locations--services)
8. [Storylines & Chain Quests](#storylines--chain-quests)
9. [Event System](#event-system)
10. [Illness & Injury System (129 Types)](#illness--injury-system)
11. [Achievements (245)](#achievements)
12. [Endings (11)](#endings)
13. [Economy](#economy)
14. [Architecture](#architecture)
15. [Active Item Docs](#active-item-docs)

---

# THE NUMBERS

| Category | Count | Details |
|----------|------:|---------|
| Lines of Code | 51,971 | 7,608 engine + 44,363 story |
| Python Files | 32 | 5 engine + 27 story |
| Event Handler Functions | 821 | Across 14 event files |
| Unique Named Events | 638 | In weighted pools |
| Illnesses + Car Troubles | 176 | 129 medical + 47 car |
| **Total Possible Events** | **814** | Named + illness + car |
| Achievements | 245 | 74 direct unlocks + stat-based |
| Crafting Recipes | 26 | 7 categories |
| Store Items | 90 | Rank-gated rotation |
| Marvin Items | 20 | 17 upgradeable to final forms |
| Flasks | 12 | One-use potions |
| Companions | 11 | 8 recruitable + 3 adventure |
| Companion Dialogue Lines | 250+ | 4 mood states each |
| Storyline Functions | 103 | Multi-part NPC arcs |
| Named NPCs | 40+ | Recurring characters |
| Locations | 19 | 13 main + 6 adventure zones |
| Endings | 11 | 5 routes with branches |

---

# ACTIVE ITEM DOCS

Use these files together when working on item content:

| File | Purpose |
|------|---------|
| `ITEM_LIVE_REFERENCE.md` | Live operational master list for what tracked items do, where they matter, and what changed most recently |
| `04_ITEMS_FLASKS_AND_UPGRADES.md` | Primary reference for what major items, flasks, upgrades, and crafting recipes do |
| `ITEM_COMPLETION_LEDGER.md` | Per-item completion tracker for coverage, interconnectivity, and remaining gaps |
++ c:\Users\Dreat\MeFolder\blackjack\docs\DEV_INDEX.md
| `ITEM_COMPLETION_LEDGER.md` note | Ledger now covers the full planned scope: Marvin items, upgrades, flasks, existing crafts, High-Impact store items, Premium Endgame Shop, 6 new Tier 1 craft categories (Gadgets, Disguises, Tonics, Dark Arts, Luxury Items, Vehicle Upgrades), Tier 2 and 3 crafted items, Tier 4 legendary crafted items, 19 secret multi-item combinations, mechanic loyalty items, item evolution chains, and 7 systemic mechanics |
| `ITEM_PLANNING_REMAINING.md` | Category-level execution plan for what still needs implementation |
| `ITEM_PLANNING.md` | Historical master roadmap and design archive |

---

# MARVIN'S MYSTICAL MERCHANDISE

*Marvin shows 1–2 random items per visit. Items break after 15–25 uses and must be repaired at a mechanic. All 17 upgradeable items must be fully upgraded to unlock the secret Eternity ending.*

### Blackjack Modifiers

| Base Item | Price | Effect | Upgrade | Upgraded Effect |
|-----------|------:|--------|---------|-----------------|
| Sneaky Peeky Shades | $14K–$34K | Peek at next card (once/hand) | Sneaky Peeky Goggles | Same, 25 durability (vs 15) |
| Pocket Watch | $9K–$15K | 66% chance of 4 extra rounds/session | Grandfather Clock | Guaranteed 4 extra rounds |
| Lucky Coin | $4K | 25% to convert a loss into a push | Lucky Medallion | 50% to convert loss → push |
| Worn Gloves | $7K | 25% to redraw instead of busting | Velvet Gloves | 50% redraw on bust |
| Tattered Cloak | $8K | Free round — dealer forgets your bet | Invisible Cloak | Same + improved durability |
| Gambler's Chalice | $11K–$29K | Enhanced double down (raise bet + draw) | Overflowing Goblet | Improved double down |
| Twin's Locket | $14K | Enables pair splitting | Mirror of Duality | Enhanced split mechanics |
| White Feather | $5K | Unlocks the surrender option | Phoenix Feather | Improved surrender terms |
| Dealer's Grudge | $16K–$24K | Side bet vs Dealer's blackjack | Dealer's Mercy | Better side-bet payout |

### Stat & Utility Items

| Base Item | Price | Effect | Upgrade | Upgraded Effect |
|-----------|------:|--------|---------|-----------------|
| Delight Indicator | varies | See dealer's mood | Delight Manipulator | See + influence dealer mood |
| Health Indicator | varies | See your health status | Health Manipulator | See + influence health |
| Dirty Old Hat | $9K | Lowers minimum bet | Unwashed Hair | Further lowers min bet |
| Golden Watch | varies | Dealer impressed → extra rounds | Sapphire Watch | Always 4 guaranteed rounds |
| Faulty Insurance | $4K | Chance to reduce doctor bill | Real Insurance | Guaranteed reduced doctor bill |
| Quiet Sneakers | $11K–$17K | Skip an unfavorable day event | Quiet Bunny Slippers | More reliable event skip |
| Rusty Compass | varies | Navigation bonus in adventures | Golden Compass | Enhanced navigation |
| Gambler's Grimoire | $6K–$9K | Tracks your stats sarcastically | Oracle's Tome | Enhanced stat tracking |

### Non-Upgradeable

| Item | Price | Effect |
|------|------:|--------|
| Enchanting Silver Bar | $7.5K–$15K | Sells at profit — pure investment |
| Marvin's Monocle | $10K–$16K | See exactly how much of your bankroll is "hot" (fraudulent) |
| Animal Whistle | $40K | **SECRET** (10% spawn chance) — recruit animal companions + unlock Sanctuary ending |

---

# WITCH DOCTOR FLASKS

*One-use potions. Prices vary per visit. Stacking 3+ flasks simultaneously = 50% chance of full purge OR 10–40 HP damage.*

### Blackjack Flasks

| Flask | Price Range | What It Does |
|-------|:----------:|--------------|
| No Bust | $10K–$14K | Prevents bust on next hand |
| Imminent Blackjack | $16K–$22K | Guarantees two aces in draw |
| Pocket Aces | $17K–$22K | First card dealt is guaranteed Ace |
| Dealer's Whispers | $10K–$14K | **Only way to unlock insurance** |
| Dealer's Hesitation | $8K–$11K | Dealer forced to hesitate — player advantage |
| Bonus Fortune | $13K–$19K | Winnings multiplied by bonus % |
| Second Chance | $11K–$15K | Redraw on loss (once per session) |
| Split Serum | $11K–$16K | Enhanced pair-splitting functionality |

### Survival Flasks

| Flask | Price Range | What It Does |
|-------|:----------:|--------------|
| Anti-Venom | $9K–$12K | Prevents poison/venom effects |
| Anti-Virus | $10K–$12K | Prevents virus/illness effects |
| Fortunate Day | $4K–$6K | Biases day events toward positive outcomes |
| Fortunate Night | $4K–$7K | Biases night events toward positive outcomes |

---

# CRAFTING RECIPES

*Unlock crafting by buying the Tool Kit ($75) from the convenience store at Rank 2+. Build from components found in shops and events.*

### Weapons (4) — Combat & Self-Defense

| Recipe | Ingredients | Pawn | Effect |
|--------|------------|-----:|--------|
| Shiv | Duct Tape + Pocket Knife | $35 | +30% combat win rate, scares muggers |
| Slingshot | Rubber Bands + Bungee Cords | $20 | +15% ranged encounter hits |
| Road Flare Torch | Road Flares + Duct Tape | $40 | Lights dark areas + weapon, burns out after 3 uses |
| Pepper Spray | Bug Spray + Lighter | $30 | Guarantees escape from non-boss combat |

### Traps (3) — Night Protection & Theft Prevention

| Recipe | Ingredients | Pawn | Effect |
|--------|------------|-----:|--------|
| Improvised Trap | Fishing Line + Pocket Knife | $25 | +40% prevent theft, early warning on night attacks |
| Car Alarm Rigging | Bungee Cords + Spare Fuses | $30 | Prevents car break-in entirely, first-strike advantage |
| Snare Trap | Rope + Fishing Line | $20 | +20% find food in adventures, trips pursuers |

### Remedies (4) — Healing & Recovery

| Recipe | Ingredients | Pawn | Effect |
|--------|------------|-----:|--------|
| Home Remedy | First Aid Kit + Cough Drops | $20 | Cures Cold/Sore Throat |
| Wound Salve | First Aid Kit + Super Glue | $25 | Closes wounds — injury healing |
| Splint | Duct Tape + Rope | $15 | Stabilizes sprains and fractures |
| Smelling Salts | Hand Warmers + Breath Mints | $18 | Restores sanity (+8) |

### Tools (4) — Exploration & Utility

| Recipe | Ingredients | Pawn | Effect |
|--------|------------|-----:|--------|
| Lockpick Set | Pocket Knife + Fishing Line | $30 | Opens locked containers & doors |
| Fishing Rod | Fishing Line + Rope | $25 | Catches fish at water locations |
| Binocular Scope | Binoculars + Duct Tape | $45 | See danger before it sees you — early warning |
| Signal Mirror | Broken Compass + Super Glue | $15 | Flash for rescue / signal for help |

### Charms (3) — Luck & Sanity

| Recipe | Ingredients | Pawn | Effect |
|--------|------------|-----:|--------|
| Lucky Charm Bracelet | Lucky Penny + Fishing Line | $10 | Passive luck boost |
| Dream Catcher | Fishing Line + Rubber Bands | $15 | Reduces nightmare frequency |
| Worry Stone | Lucky Penny + Hand Warmers | $8 | Passive sanity restoration |

### Survival (5) — Sustenance & Signaling

| Recipe | Ingredients | Pawn | Effect |
|--------|------------|-----:|--------|
| Rain Collector | Plastic Wrap + Garbage Bag | $10 | Auto-collects water — hydration on autopilot |
| Emergency Blanket | Garbage Bag + Duct Tape | $12 | Cold protection / warmth |
| Smoke Signal Kit | Road Flares + Garbage Bag | $20 | Signal for help or scare wildlife |
| Fire Starter Kit | Lighter + Hand Warmers | $15 | Start campfire anywhere, any weather |
| Water Purifier | Plastic Wrap + Lighter | $18 | Solar still — purify dirty water |

### Companion (3) — Pet Care

| Recipe | Ingredients | Pawn | Effect |
|--------|------------|-----:|--------|
| Companion Bed | Blanket + Duct Tape | $15 | Boosts companion mood/comfort |
| Pet Toy | Rope + Rubber Bands | $8 | Boosts companion happiness |
| Feeding Station | Plastic Wrap + Duct Tape | $10 | No-spill food bowl — companion care |

---

# CONVENIENCE STORE

*Run by Kyle. Buy 1–2 items per visit. Inventory refreshes every 7 days. Higher wealth rank = fancier stock.*

### Always Available (All Ranks)
3 random food items (from: Candy Bar, Chips, Turkey Sandwich, Energy Drink, Beef Jerky, Cup Noodles, Granola Bar, Hot Dog, Microwave Burrito, Cheese, Bread, Sandwich) + Pest Control + Deck of Cards

### By Rank

| Rank | Balance | Notable Items | Key Unlocks |
|------|---------|--------------|-------------|
| 0 — Poor | $1–$1K | Lottery Ticket, Lucky Penny, Matches, Worn Map ($8), Breath Mints, Rubber Bands, Birdseed, Baking Soda | **Worn Map** → unlocks Marvin & Witch Doctor |
| 1 — Cheap | $1K–$10K | Necronomicon ($666 ⚠️ trap), Dog Whistle, Running Shoes, Road Flares, Bug Spray, Disposable Camera | Dog Whistle for chain quest |
| 2 — Modest | $10K–$100K | **Tool Kit ($75)**, Binoculars, Padlock, Fishing Line, Super Glue, Hand Warmers, Signal Booster, Welding Goggles | **Tool Kit** → unlocks crafting |
| 3 — Rich | $100K–$400K | Expensive Cologne ($150), Fancy Cigars ($200), Gold Chain ($500), Leather Gloves, Silver Flask, Fancy Pen | Luxury/gift items |
| 4+ — Doughman | $400K+ | Vintage Wine ($800), Lucky Rabbit Foot ($1K), Cursed Coin ($13 ⚠️ trap), Silk Handkerchief, Antique Pocket Watch ($1.2K) | Collector items |

### Car Maintenance (random availability, all ranks)
Jumper Cables, Battery Charger, Spare Fuses, Headlight Bulbs, Motor Oil, Coolant, Brake Fluid, Power Steering Fluid, Fix-a-Flat, Tire Patch Kit, Car Jack, Gas Can, Tool Kit, WD-40, Bungee Cords, Rope, Exhaust Tape, Radiator Stop Leak, OBD Scanner, Spare Spark Plugs, Serpentine Belt, Fuel Filter, Brake Pads

---

# COMPANIONS

*Recruit with the Animal Whistle ($40K, 10% spawn at Marvin's). Each companion has 4 mood states (Happy/Neutral/Sad/Bonded) with unique dialogue. 250+ total dialogue lines.*

| Companion | Type | Sanity | Special Ability | Favorite Food | How It Helps |
|-----------|------|:------:|----------------|---------------|-------------|
| **Squirrelly** | Squirrel | +2 | +1 Luck | Bag of Acorns | Passive luck boost to events & gambling |
| **Whiskers** | Alley Cat | +3 | Danger Warning | Cat Food | Warns you before bad events fire |
| **Lucky** | Three-Legged Dog | +5 | Physical Protection | Dog Food | Blocks/absorbs damage from attacks |
| **Mr. Pecks** | Crow | +1 | 5% Money Find | Birdseed | Random chance to find $1–$20 per day |
| **Patches** | Opossum | +2 | Night Bonus | Garbage | Better odds during night events |
| **Rusty** | Raccoon | +2 | 3% Steal | Anything | Chance to steal items from NPCs |
| **Slick** | Rat | +1 | Escape Routes | Cheese | Extra escape options from dangerous events |
| **Hopper** | Rabbit | +2 | +3 Luck | Carrot | Highest luck bonus of any companion |

### Adventure Companions (zone-specific, temporary)
| Companion | Zone | Role |
|-----------|------|------|
| Asphalt | The Road | Road dog — travel protection |
| Ursus | The Woodlands | Bear — heavy combat |
| Thunder | The Beach | Horse — exploration speed |

### Key Companion Mechanics
- **5+ companions + Animal Whistle** → unlocks the Sanctuary ending at the airport
- **Selling companions to Gus** → dark path (achievements: First Blood → The Product → Meat Cubes → The Factory)
- **Companion Bed/Pet Toy/Feeding Station** crafts boost mood → bonded state → unique dialogue

---

# LOCATIONS & SERVICES

## 13 Main Locations

| # | Location | Services | Cost | Key Detail |
|---|----------|----------|------|-----------|
| 1 | **Casino** | Blackjack gambling | Bet-based | The core loop — earn money toward $1M |
| 2 | **Your Car** | Rest, craft, eat, check inventory | Free | Home base — where you sleep and craft |
| 3 | **Doctor's Office** | Cure all illness, heal injury | 30–50% of balance | Real Insurance = free; Faulty Insurance = 50% discount (risky) |
| 4 | **Convenience Store** (Kyle) | Buy items (1–2/visit), gift wrap ($10) | $1–$1,200 | Rank-gated stock; refreshes weekly |
| 5 | **Marvin's Mystical Merchandise** | Buy magical items (1–2 random) | $4K–$40K | 20 items; 10% chance for secret Animal Whistle |
| 6 | **Witch Doctor's Tower** | Buy flasks, heal status effects | $4K–$22K / 5–25% balance | 12 flask types; 3+ flasks = overdose risk |
| 7 | **Tom's Trusty Trucks & Tires** | Repair broken items | $4K–$17.5K | Reliable, offers 20–35% discounts if you're broke |
| 8 | **Frank's Flawless Fixtures** | Repair broken items | $3K–$25K | 60% success rate — cheaper but unreliable |
| 9 | **Oswald's Optimal Outparts** | Repair items + **UPGRADE** (3+ visits) | $4.5K–$30K repair / $120K–$400K upgrade | Only place to upgrade Marvin items |
| 10 | **Gus's Pawn Shop** | Sell items for cash | $1–$500 base | Reputation affects prices; dark companion-selling option |
| 11 | **Vinnie's Loans** | Borrow money | Interest compounds | Debt escalates: warnings → threats → Tony the enforcer |
| 12 | **Tanya's Office** | Phone calls / story progression | — | Late-game; links to Salvation ending |
| 13 | **Airport** | Buy one-way ticket out | $10K | Bliss ending; 5+ companions + Whistle = Sanctuary |

## 6 Adventure Zones (Rank 2+)

| Zone | Themes | Risks | Rewards |
|------|--------|-------|---------|
| **The Road** | Street dice (Cee-lo), hitchhikers, roadside shrines | Bandits, losing money, stranded | NPC meetings, items, companion Asphalt |
| **The Woodlands** | Forest encounters, wildlife, mysterious locations | Getting lost, wildlife attacks | Hidden treasures, rare components |
| **The Swamp** | Murky water, creatures, atmospheric dread | Sickness from water, supernatural danger | Aquatic items, rare components |
| **The Beach** | Coastal encounters, shipwrecks, beach life | Drowning, harsh sun | Marine salvage, treasure, companion Thunder |
| **The City** | Urban encounters, crowds, street hustles | Mugging, theft, manipulation | Money opportunities, connections |
| **Underwater** | Diving, sea creatures, buried items | Drowning, decompression | Rarest items; **Kraken can be befriended** |

---

# STORYLINES & CHAIN QUESTS

## 4 Chain Quests (5 stages each)

| Quest | Key NPC | Stages | Reward |
|-------|---------|:------:|--------|
| **Hermit Trail** | Edgar | Find → Track → Follow → Discover → Hollow Tree Stash | Hollow Tree Stash item + achievement |
| **Midnight Radio** | Vera | Static → Signal → Source → Broadcast → Your Voice in the Dark | Pirate Radio Flyer item + achievement |
| **Junkyard Artisan** | Gideon | Observe → Learn → Weld → Create → Crown | Junkyard Crown ($100 pawn) + achievement |
| **Lost Dog Flyers** | Block Party NPCs | Flyers → Search → Find → Rescue → Reunion | Night Vision Scope + Reunion Photo + achievement |

## 24+ Multi-Part Story Arcs

| Arc | Stages | Summary |
|-----|:------:|---------|
| **Kyle** | 6 | Convenience store boy → his problem → after hours → his secret → finale |
| **Grandma** | 6 | First call → recipe → bad news → gift → last call (emotional) |
| **Dr. Feelgood** | 6 | First pill → feeling better → price hikes → rock bottom → recovery → resolution |
| **Mime** | 6 | Performance → encore → message → behind the paint → final act (surreal) |
| **Lucky Dog** | 6 | Befriended → who hurt you → previous owner → good boy → saves your life |
| **Dealer Past** | 6 | Photo → journal → questions → answer → choice (reveals Dealer backstory) |
| **Sleep Paralysis** | 5 | Can't move → it speaks → the offer → resolution (cosmic horror) |
| **Radio Signal** | 5 | Static → broadcast → source → who's watching (paranoia) |
| **Graveyard** | 5 | Wandering → digger → your plot → Edgar's request (morbid) |
| **Carnival** | 5 | Lights → fortune teller → the game → pack up (time-limited) |
| **Gas Station Hero** | 5 | Robbery → recognized → interviewed → media consequences |
| **Phil** | 5 | Interrogation → cryptic escalation → finale |
| **Martinez** | 5 | License → wellness → favor → resolution |
| **Stuart** | 5 | Side hustle → good deal → bad deal → Oswald finds out |
| **Jameson** | 5 | Carrot incident → horse trouble → rustlers → one last ride (western) |
| **Painkiller** | 4 | Chronic pain → addiction → withdrawal/dealer/overdose (dark path) |
| **The Collector** | 5 | Intro → small favor → payment → real offer (dark comedy) |
| **Suzy** | 4 | Meeting → color/animal questions → full story |
| **Victoria** | 3 | Rival appears → rivalry intensifies → new twist |
| **Betsy** | 4 | Hungry cow → starving cow → army of cows |
| **Stray Cat** | 4 | Meet → befriend → cat gets sick → dies or kittens |
| **Bridge Angel** | 4 | Contemplation → angel returns → the call → choice |
| **Lockbox** | 4 | The box → key hunt → who left it |
| **Tanya** | 3 | Met → got number → completed (ending path) |

## Mechanic Dreams (10 total)
- **Tom** (3 dreams): Photo on wall, family mentions, shared past
- **Frank** (4 dreams): Dark lore, the Dealer, Nazi bikers
- **Oswald** (3 dreams): Circuits, the Grand Casino vision, transcendence

---

# EVENT SYSTEM

*Events fire every day phase and night phase. The pool is selected by your current wealth rank. Each event has a weight (0–4 copies per rank) controlling probability.*

## Day Events by Rank

| Rank | Balance | Pool Size | Tone |
|------|---------|:---------:|------|
| 0 — Poor | $1–$1K | 232 | Desperate, scrappy, survival-focused |
| 1 — Cheap | $1K–$10K | 271 | Slightly better, more opportunities |
| 2 — Modest | $10K–$100K | 276 | Widest variety — most content unlocked |
| 3 — Rich | $100K–$400K | 217 | Luxury problems, wealth attracts trouble |
| 4 — Doughman | $400K–$750K | 216 | High stakes, paranoia, extravagance |
| 5 — Nearly | $750K+ | 192 | End-game tension, countdown to $1M |

## Night Events by Rank

| Rank | Pool Size | Content |
|------|:---------:|---------|
| 0–4 | 15–22 each | Dreams, nightmares, companion interactions |
| 5 — Nearly | 391 | Massive pool — dreams intensify, mechanic visions, finale buildup |

## 14 Event Files

| File | Functions | What's Inside |
|------|:---------:|---------------|
| **events_day_people** | 86 | NPC encounters — Suzy, Cowboy, Mime, Street Prophet, Doppelganger, strangers asking for help |
| **events_day_survival** | 77 | Weather events, hunger, pests, shelter crises, resource management |
| **events_day_items** | 76 | Finding items, cursed items, item-gated consequences, discovery events |
| **events_day_wealth** | 73 | Money milestones, financial windfalls/disasters, luxury temptations |
| **events_car** | 67 | Flat tires, dead batteries, engine failures, road breakdowns — 47 named car troubles |
| **events_day_dark** | 66 | Mugging, robbery, assault, serial killers, shadow creatures, witnessing crimes |
| **events_illness** | 142 | 129 illness/injury types across all severity tiers |
| **events_night** | 49 | Dreams, nightmares, sleep events, rabbit chase, mechanic dream chains |
| **events_day_animals** | 39 | Animal encounters — friendly, dangerous, bizarre |
| **events_day_storylines** | 38 | Story arc progression triggers — advances multi-part chains |
| **events_day_companions** | 36 | Companion interactions, bonding moments, companion-specific events |
| **events_day_numbers** | 32 | Balance/day-count triggers, numerology, probability quirks |
| **events_day_surreal** | 23 | Reality-bending — time loops, déjà vu, existential crises, cosmic weirdness |
| **events_day_casino** | 17 | Casino floor encounters, dealer interactions, other gamblers |

---

# ILLNESS & INJURY SYSTEM

*129 types across multiple categories. Caught through random events, adventure zones, and specific NPC encounters. Severity scales with wealth rank. Cured by Doctor (guaranteed) or Witch Doctor (50% chance, risky).*

| Category | Count | Examples | Effects |
|----------|:-----:|---------|---------|
| **Respiratory** | ~8 | Cold, Flu, Pneumonia, Bronchitis, Severe Asthma | Health drain, reduced stamina |
| **Infections** | ~15 | Staph, UTI, Strep Throat, Tetanus, Lyme Disease, Rat Bite Fever | Health drain, worsens over time |
| **Gastrointestinal** | ~8 | Food Poisoning, Appendicitis, Gallbladder Attack, Waterborne Illness | Severe health drain |
| **Toxicity** | ~8 | Lead Poisoning, Mercury Poisoning, Mold Toxicity, Chemical Burns | Chronic damage |
| **Mental Health** | ~6 | Severe Anxiety, PTSD, Chronic Insomnia, Trauma Flashback | Sanity drain |
| **Bone/Injury** | ~20 | Broken bones, Concussion, Deep Laceration, Burns, Whiplash, Dislocations | Mobility restriction, pain |
| **Combat Injuries** | ~10 | Stab wounds, blunt trauma, gunshot | Heavy HP + sanity loss |
| **Environmental** | ~8 | Heat exhaustion, Frostbite, Dehydration, Sunstroke | Ongoing drain |
| **Misc Medical** | ~46 | Everything else — ailments, chronic conditions, rare diseases | Varies |

### Curing Methods
- **Doctor** → removes all illness + heals 1 injury per visit (costs 30–50% of balance)
- **Witch Doctor** → 50% cure chance, risky side effects
- **Home Remedy (crafted)** → cures Cold/Sore Throat specifically
- **Anti-Venom / Anti-Virus flasks** → prevent specific categories

---

# ACHIEVEMENTS

*245 defined in total. Some unlock automatically from stats, others require specific actions or discoveries.*

| Category | Count | Examples |
|----------|:-----:|---------|
| **Money Milestones** | ~10 | Baby Steps ($1K), Getting Somewhere ($10K), Big Spender ($100K), Millionaire ($1M), Multi-Millionaire |
| **Survival Milestones** | ~10 | The Third Day, Still Kicking (7d), Fortnight Fighter, Stubborn (30d), Year Survivor (365d) |
| **Gambling** | ~20 | Twenty-One!, Beginner's Luck, Card Counter (50 hands), Hot Streak (5 wins), Blackjack Legend, Ten Thousand Hands |
| **Companions** | ~12 | First Friend, Bonding Time, Best Friends, Loyal Companion (30d), Noah's Ark (5 companions), Disney Princess |
| **Collection** | ~10 | Packrat Begins, Collector (10), Master Collector (20), Full House (every collectible), Item Master |
| **Social/Events** | ~15 | Social Butterfly (20 NPCs), Regular (50 casino visits), Night Owl, Story Seeker (50 events) |
| **Chain Quests** | ~12 | The Hermit's Legacy, Edgar's Daughter, Radio Nowhere, Junkyard Apprentice, Dog Hero, Connected |
| **Dark/Secret** | ~8 | First Blood (sell companion), The Product (3 sales), Meat Cubes (5), The Factory (15) |
| **Gameplay Mastery** | ~20 | Never Bust, Insurance Expert, Split Master, Double Down King, Surrender Survivor |
| **Location Mastery** | ~8 | Casino Rat, Shop Hopper, Hermit, Nomad |
| **NPC Relationships** | ~15 | Dealer Friend, Gus Partner, Oswald Masterwork, Marvin Believer, Kyle Regular |
| **Gift/Dealer** | ~6 | Gift Giver, Perfect Gift, Death Wish, Dealer Pleased, Dealer Furious |
| **Fraud** | ~5 | Money Launderer, Master Launderer, Caught Red-Handed |
| **Extreme Grinds** | ~8 | The Long Con (365d), Speedrunner ($1M in <30d), Fate Collector (all endings), Perfection (max everything) |
| **Unique Deaths** | ~5 | Dealer Executed, Tony Visited, Madness Consumed |
| **Rare Events** | ~10 | Lucky Sevens, Unlucky Thirteen, Kraken Encounter, Moon Touched, Mermaid Met |

---

# ENDINGS

*Reach $1,000,000 to trigger the endgame. The mechanic who visits you that morning depends on your dream score (who you dreamed about most).*

| # | Ending | Route | Trigger | What Happens |
|---|--------|-------|---------|-------------|
| 1 | **Salvation (Healed)** | Tom | Tanya visited 5+ times → auto-answer phone | Tom calls, you're pulled back to reality and heal |
| 2 | **Salvation** | Tom | Answer Tom's phone call → agree | Tom helps you process the journey, bittersweet freedom |
| 3 | **Resurrection** | Tom | Answer phone → refuse Tom's offer | Reject salvation, return to the table — can't stop gambling |
| 4 | **To Kill a Dealer** | Frank | Accept Frank's hit → shoot the Dealer | Join Frank's gang, Dealer dies, you inherit the underworld |
| 5 | **Retribution** | Frank | Accept hit → shoot Frank instead | Turn on Frank, earn the Dealer's respect, walk away clean |
| 6 | **Transcendence** | Oswald | Accept Oswald's casino offer | You become the new casino owner — "Your Very Own Casino" |
| 7 | **Eternity** | Oswald | **All 17 items upgraded** | Become a cyborg god, crush Oswald's skull — "Becoming a Monstrosity" |
| 8 | **Bliss** | Airport | Board the plane ($10K ticket) | Leave everything behind, clean break, start over |
| 9 | **Sanctuary** | Airport | 5+ companions + Animal Whistle | Take your animals, found an animal sanctuary — happiest ending |
| 10 | **Exhaust** | Special | Sanity critically low + despair | You simply stop. Too tired to continue. |
| 11 | **Madness** | Special | Sanity < 30 + shadow entity | Reality fractures, consumed by the darkness you couldn't escape |

### Ending Routing
```
Reach $1,000,000
    └─ Morning: Mechanic visits (based on dream score)
         ├─ Tom  → Phone rings → Answer? → Yes = Salvation / No = Resurrection
         │                                  (Tanya 5+ → auto Salvation Healed)
         ├─ Frank → Nazi bikers → Gun → Shoot Dealer = Destruction
         │                              Shoot Frank = Retribution
         ├─ Oswald → Casino offer → Accept = Transcendence
         │                          All 17 upgraded = Eternity
         └─ Airport → Board? → Yes = Bliss
                               5+ companions + Whistle = Sanctuary
```

---

# ECONOMY

## Wealth Ranks

| Rank | Balance Range | What Changes |
|------|-------------|-------------|
| 0 — Poor | $1–$999 | Basic store stock, desperate events, survival mode |
| 1 — Cheap | $1K–$9,999 | More shop variety, Necronomicon available |
| 2 — Modest | $10K–$99,999 | **Crafting unlocks**, adventures unlock, widest event variety |
| 3 — Rich | $100K–$399,999 | Luxury items, wealth-targeted events, higher repair costs |
| 4 — Doughman | $400K–$749,999 | Exclusive collector items, high-stakes everything |
| 5 — Nearly | $750K–$999,999 | Massive night pool (391 events), endgame tension |
| Millionaire | $1,000,000+ | **Endgame triggers** — morning mechanic visit |

## Money Flow

| Source | Income | Notes |
|--------|--------|-------|
| Casino (Blackjack) | Bet-based winnings | The core loop |
| Mr. Pecks (companion) | $1–$20/day | 5% chance per day |
| Rusty (companion) | Stolen items | 3% chance per encounter |
| Pawn Shop | $1–$500/item | Reputation multiplier |
| Events | Variable | Found cash, rewards, NPC gifts |

| Expense | Cost | Notes |
|---------|------|-------|
| Doctor | 30–50% of balance | Real Insurance = free |
| Mechanic Repairs | $3K–$30K | Tom cheapest, Oswald most expensive |
| Item Upgrades | $120K–$400K each | Oswald only — 17 items to upgrade |
| Marvin Items | $4K–$40K | Random stock each visit |
| Flasks | $4K–$22K | One-use consumables |
| Convenience Store | $1–$1,200 | Rank-gated pricing |
| Airport Ticket | $10K | One-way, endgame only |

## Loan Shark (Vinnie)

| Debt Level | Vinnie's Response |
|-----------|------------------|
| First visit | Friendly greeting, easy loan |
| $5K+ debt | Warning tier 1 |
| $10K+ debt | Warning tier 2 |
| $20K+ debt | Threats |
| $30K+ debt | Tony the enforcer visits — violence |

---

# ARCHITECTURE

```
blackjackMain.py (16 lines)        ← Entry point
├── blackjack.py (1,650 lines)     ← Card game engine
│   └── deckOfCards.py (114 lines) ← Deck & Card classes
├── lists.py (5,432 lines)         ← ALL game data
├── typer.py (396 lines)           ← Typewriter text + input
└── story/ (44,363 lines)          ← 27 files
    │
    ├── CORE
    │   ├── player_core.py    (995 lines,  103 fn) — Player state, inventory, stats
    │   ├── systems.py        (1,942 lines, 102 fn) — Achievements, upgrades, item checks
    │   ├── game_flow.py      (1,201 lines,  22 fn) — Day/night loop, millionaire check
    │   ├── event_dispatch.py (148 lines,   14 fn) — Event selection & firing
    │   ├── day_cycle.py      (420 lines,   27 fn) — Morning/afternoon/night phases
    │   └── economy.py        (153 lines,   25 fn) — Money, loans, pawn, balance
    │
    ├── WORLD
    │   ├── locations.py      (4,940 lines,  51 fn) — All shops & NPC visits
    │   ├── adventures.py     (4,142 lines,  23 fn) — 6 adventure zones
    │   ├── mechanics_intro.py (745 lines,   30 fn) — Tom/Frank/Oswald intros
    │   └── durability.py     (485 lines,   29 fn) — Item wear & repair
    │
    ├── NARRATIVE
    │   ├── storylines.py     (5,025 lines, 103 fn) — Multi-part story arcs
    │   └── endings.py        (3,217 lines,  31 fn) — 11 ending sequences
    │
    └── EVENTS (14 files, 20,945 lines, 821 functions)
        ├── events_day_people.py       (1,966 lines, 86 fn)
        ├── events_day_items.py        (2,248 lines, 76 fn)
        ├── events_day_dark.py         (2,430 lines, 66 fn)
        ├── events_day_survival.py     (1,779 lines, 77 fn)
        ├── events_day_wealth.py       (1,854 lines, 73 fn)
        ├── events_illness.py          (1,902 lines, 142 fn)
        ├── events_night.py            (2,405 lines, 49 fn)
        ├── events_car.py              (1,222 lines, 67 fn)
        ├── events_day_companions.py   (1,668 lines, 36 fn)
        ├── events_day_animals.py      (1,176 lines, 39 fn)
        ├── events_day_storylines.py   (1,156 lines, 38 fn)
        ├── events_day_numbers.py      (449 lines,  32 fn)
        ├── events_day_surreal.py      (474 lines,  23 fn)
        └── events_day_casino.py       (216 lines,  17 fn)
```

### How Events Fire
```
Day Phase:
  get_day_event(rank) → make_weighted_day_pool(rank) → weighted random pick → getattr(self, event_name)()
  
  Pool built from: _DAY_EVENT_TONE dict (195 entries × 6-element weight arrays)
  Weight 0 = excluded from rank, Weight 4 = 4 copies in pool (highest probability)
  
  + 129 illness events injected
  + 47 car trouble events injected

Night Phase:
  Similar pool system, separate night weights
  Rank 5 = 391 events (dream chains, mechanic visions, endgame buildup)
```
