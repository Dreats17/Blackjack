# BLACKJACK — Complete Game Index

> **51,971 lines of Python** across 32 game files.  
> **814 unique events** · **252 achievements** · **221 collectible/core items** · **115 crafting recipes** · **11 endings**

---

# TABLE OF CONTENTS

1. [The Numbers](#the-numbers)
2. [Marvin's Mystical Merchandise](#marvins-mystical-merchandise)
3. [Witch Doctor Flasks (12 Types)](#witch-doctor-flasks)
4. [Crafting Recipes (115)](#crafting-recipes)
5. [Item System Strategy](#item-system-strategy)
6. [Advanced Route Guides](#advanced-route-guides)
7. [Convenience Store (90 Items)](#convenience-store)
8. [Companions (8 + 3 Adventure)](#companions)
9. [Locations & Services (19)](#locations--services)
10. [Storylines & Chain Quests](#storylines--chain-quests)
11. [Event System](#event-system)
12. [Illness & Injury System (129 Types)](#illness--injury-system)
13. [Achievements (252)](#achievements)
14. [Endings (11)](#endings)
15. [Economy](#economy)
16. [Architecture](#architecture)
17. [Active Item Docs](#active-item-docs)

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
| Achievements | 252 | Live source count from `lists.py` |
| Crafting Recipes | 115 | 26 base + 40 Tier 1 + 25 Tier 2 + 12 Tier 3 + 12 Tier 4 |
| Collectible/Core Items | 221 | Live `get_all_collectibles_list()` count; `all_items_tmp.txt` has 225 lines because it also includes Bodyguard Bruno, Car, Squirrely, and Street Cat Ally |
| Marvin-Sold Items | 25 | 22 rotating stock items + Animal Whistle + 5 Back Room items with 3 overlaps |
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
| `04_ITEMS_FLASKS_AND_UPGRADES.md` | Player-facing reference for major items, flasks, upgrades, and crafting; currently behind the full 115-recipe live workbench scope |
| `ITEM_COMPLETION_LEDGER.md` | Per-item completion tracker for coverage, interconnectivity, and remaining gaps |
| `ITEM_COMPLETION_LEDGER.md` note | Ledger now covers the full planned scope: Marvin items, upgrades, flasks, existing crafts, High-Impact store items, Premium Endgame Shop, 6 new Tier 1 craft categories (Gadgets, Disguises, Tonics, Dark Arts, Luxury Items, Vehicle Upgrades), Tier 2 and 3 crafted items, Tier 4 legendary crafted items, 19 secret multi-item combinations, mechanic loyalty items, item evolution chains, and 7 systemic mechanics |
| `ITEM_PLANNING_REMAINING.md` | Category-level execution plan for what still needs implementation |
| `ITEM_PLANNING.md` | Historical master roadmap and design archive |

---

# MARVIN'S MYSTICAL MERCHANDISE

*Live source scope: 22 rotating stock items, Animal Whistle as a 10% secret pull, and a 5-item Back Room with 25 unique Marvin-sold items total. All 17 upgradeable Marvin base items still feed the Eternity route.*

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

### Back Room Premium Stock

*Unlock when you own the full Marvin base set or exceed the back-room balance threshold. The live Back Room stock is smaller but more explicit than the older doc version.*

| Item | Price | Effect |
|------|------:|--------|
| Dealer's Mirror | $50K | Permanent dealer hole-card read |
| The Last Card | $100K | One perfect forced draw |
| Marvin's Eye | $75K | Hidden-outcome and best-play reader |
| Bottle of Tomorrow | $40K | Skip to tomorrow with full health and sanity |
| Blank Check | $200K | One free purchase from any shop |

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

*Unlock crafting by buying the Tool Kit ($85) from the Convenience Store. The live workbench now contains 115 recipes across 5 tiers. The old 26-recipe, 7-category summary is no longer complete.*

## Live Recipe Breakdown

| Tier | Count | Scope |
|------|------:|-------|
| Tier 0 | 26 | Original workbench recipes |
| Tier 1 | 40 | Expanded single-step crafting families |
| Tier 2 | 25 | Crafted + crafted or crafted + base composites |
| Tier 3 | 12 | Triple-ingredient masterworks |
| Tier 4 | 12 | Legendary endgame crafts |

## Live Category Breakdown

| Category | Count |
|----------|------:|
| Weapon | 8 |
| Trap | 3 |
| Remedy | 4 |
| Tool | 9 |
| Charm | 7 |
| Survival | 10 |
| Companion | 4 |
| Gadget | 7 |
| Disguise | 9 |
| Tonic | 9 |
| Dark Arts | 6 |
| Luxury | 7 |
| Vehicle | 8 |
| Legendary | 24 |

## Full Recipe Roster By Tier

### Tier 0 (26)

Shiv, Slingshot, Road Flare Torch, Pepper Spray, Improvised Trap, Car Alarm Rigging, Snare Trap, Home Remedy, Wound Salve, Splint, Smelling Salts, Lockpick Set, Fishing Rod, Binocular Scope, Signal Mirror, Lucky Charm Bracelet, Dream Catcher, Worry Stone, Rain Collector, Emergency Blanket, Smoke Signal Kit, Fire Starter Kit, Water Purifier, Companion Bed, Pet Toy, Feeding Station.

### Tier 1 (40)

Headlamp, Spotlight, Evidence Kit, Radio Jammer, EMP Device, Distress Beacon, Security Bypass, Low-Profile Outfit, Beach Bum Disguise, Gas Mask, Storm Suit, Brass Knuckles, Gentleman's Charm, Forged Documents, Antacid Brew, Trail Mix Bomb, Animal Bait, Stink Bomb, Voice Soother, Outdoor Shield, Cool Down Kit, Smoke Flare, Vermin Bomb, Eldritch Candle, Binding Portrait, Blackmail Letter, Devil's Deck, Fortune Cards, Kingpin Look, Enchanted Vintage, Heirloom Set, Aristocrat's Touch, Power Move Kit, Animal Magnetism, Luck Totem, Tire Ready Kit, Power Grid, Miracle Lube, Mobile Workshop, Pursuit Package.

### Tier 2 (25)

Assassin's Kit, Fire Launcher, Tear Gas, Street Fighter Set, Survival Bivouac, Hydration Station, Provider's Kit, Fortified Perimeter, All-Weather Armor, Master Key, Night Scope, SOS Kit, Intelligence Dossier, Surveillance Suite, Mind Shield, Fortune's Favor, Fate Reader, Lucid Dreaming Kit, Old Money Identity, New Identity, Beast Tamer Kit, Cheater's Insurance, Roadside Shield, Auto Mechanic, Rolling Fortress.

### Tier 3 (12)

Road Warrior Armor, Third Eye, Nomad's Camp, All-Access Pass, Master of Games, Immortal Vehicle, Gambler's Aura, Ark Master's Horn, Guardian Angel, Hazmat Suit, Ghost Protocol, Dark Pact Reliquary.

### Tier 4 (12)

Beastslayer Mantle, Seer's Chronicle, Wanderer's Rest, Skeleton Key, King of the Road, War Wagon, Moonlit Fortune, Leviathan's Call, Last Breath Locket, Phantom Rose, Soul Forge, Witch Doctor's Amulet.

## Where To Check Details

- `04_ITEMS_FLASKS_AND_UPGRADES.md` should hold the player-facing full crafting and item reference.
- `ITEM_COMPLETION_LEDGER.md` currently has the most complete live coverage of the expanded Tier 1 through Tier 4 recipe families.
- `ITEM_LIVE_REFERENCE.md` tracks practical in-game usage and coverage state for the most important craft families.

---

# ITEM SYSTEM STRATEGY

This is a code-aware optimization route for the entire game loop. It is not "play safe" advice; it is a threshold-and-system exploitation plan.

## 1) Core Economy Exploits

- Use rank thresholds as hard control points, not fuzzy ranges:
  - Rank 0: $1 to $999
  - Rank 1: $1,000 to $9,999
  - Rank 2: $10,000 to $99,999
  - Rank 3: $100,000 to $399,999
  - Rank 4: $400,000 to $749,999
  - Rank 5: $750,000 to $999,999
- Stay intentionally in Rank 2 while building your core, because this is the widest practical content unlock band (adventures + workbench + strong store utility) without peak late-game volatility.
- Use pre-service spending to reduce percentage-based costs:
  - Doctor bill is `30% to 50%` of current balance.
  - Witch heal is `5% to 25%` of current balance.
  - If a forced medical stop is likely, convert excess cash into durable value first (items/crafts/upgrades), then pay the reduced percentage.

## 2) Day/Night Pool Manipulation

- The day pool is weighted by rank, then modified again by your inventory.
- In live code, carrying specific crafted items changes event composition directly:
  - `Ghost Protocol`: strips combat events from pool.
  - `Road Warrior Armor`: reduces combat density.
  - `Gambler's Aura`, `Fortune's Favor`: increase positive day events.
  - `Nomad's Camp`: heavily increases camp/survival events.
  - `Beast Tamer Kit`: increases animal-event frequency.
- Strategic implication: build for pool-shaping, not just one-off event solving. If your inventory does not alter pool odds, it is usually inferior to an item that does.

## 3) Shop Routing Exploits

- `Worn Map` at Rank 1 is your route accelerator because it unlocks Marvin access from the shop list logic.
- `Tool Kit` always appears if you do not own one; buy it early because this is guaranteed progression leverage, not RNG.
- Use the convenience-store second-item chance (`~40%` after first purchase) to buy in high-value pairs when possible.
- Gift wrap unlocks after repeated store purchases and automatically routes wrapped gifts into dealer interactions; this is a hidden consistency boost path, not flavor only.

## 4) Doctor, Insurance, and Ban Management

- `Real Insurance` is elite-tier consistency: zero bill at doctor, with sanity upside.
- `Faulty Insurance` is high-EV but volatile:
  - Discounted bill path exists.
  - Roughly 20% failure path can trigger `Doctor Ban` and consume the item.
- Exploit rule:
  - Use `Faulty Insurance` aggressively only while your run can tolerate doctor denial.
  - Pivot to `Real Insurance` before prolonged high-risk route pushes.

## 5) Loan Shark and Hot-Cash Conversion

- Loan principal is useful only if immediately converted into real edge.
- Debt escalates on a strict timer:
  - Interest compounds weekly.
  - Warning tiers rise by overdue days.
  - Random encounters scale up with warning level.
- `Marvin's Monocle` has a hidden anti-synergy with Vinnie:
  - Raises interest floor to 35%.
  - Applies/maintains a 10% knowing fee on new loans.
  - Can add instant surcharge when debt already exists.
- Blackjack hot-cash detection is per-hand and scales with fake ratio in the bet plus cumulative dealer exposure.
- Exploit rule:
  - If you borrow, launder quickly through controlled, moderate-risk betting windows.
  - Do not carry unresolved loan pressure into long survival stretches.
  - Avoid Monocle-before-debt if your plan includes borrowing.

## 6) Blackjack Engine Advantage Stack

- Build toward compounding control, in order:
  1. Information: `Sneaky Peeky` line, `Dealer's Whispers`, `Dealer's Mirror`, `Marvin's Eye`.
  2. Optionality: `Twin's Locket`/`Mirror of Duality`, `White Feather`/`Phoenix Feather`, `Gambler's Chalice`/`Overflowing Goblet`.
  3. Volatility smoothing: `Lucky Coin`/`Lucky Medallion`, insurance tools.
- If dealer happiness is collapsing, preserve bankroll by reducing exposure and forcing recovery windows; min-bet aggression and all-in pressure can escalate when the dealer state is bad.

## 7) Mechanic and Upgrade Route Control

- Your millionaire ending mechanic path is locked by your chosen car mechanic history.
- Choose route early based on ending target:
  - Tom track for salvation variants.
  - Frank track for destructive/retribution track.
  - Oswald track for transcendence/eternity path.
- Oswald upgrades are a major endgame conversion tool and are required for full Eternity route completion (`all 17 upgradeable lines`).
- Use mechanic-specific bonuses when found (`Tom's Wrench`, `Frank's Flask`, `Oswald's Dice`) to reduce friction and push your intended branch.

## 8) Marvin Optimization (Including Back Room)

- Marvin inventory rolls many items at `3/5` appearance check if not owned; revisit often when bankroll supports buy-on-sight policy for core pieces.
- `Animal Whistle` remains rare and route-defining.
- Back Room unlock is deterministic once conditions are met:
  - Own all base Marvin lines (upgrades count), or
  - Exceed high-balance threshold.
- Back Room priority generally follows:
  1. `Dealer's Mirror` (persistent card information)
  2. `Bottle of Tomorrow` (recovery/time compression)
  3. `Marvin's Eye` (decision quality)
  4. `The Last Card` (surgical bailout)
  5. `Blank Check` (single huge tempo spike)

## 9) Crafting Progression for Maximum Edge

### Early Conversion (Tier 0 to Tier 1)

- Acquire broad-branch ingredients early (`Duct Tape`, line/rope, first-aid pieces, ignition sources).
- Build one item each for:
  - defense,
  - sustain,
  - mobility/access,
  - information/signal.

### Mid Conversion (Tier 1 to Tier 2)

- Prefer role-compression crafts that replace two inventory slots with one multi-use effect.
- Keep at least one direct combat solve and one non-combat escape solve active.

### Late Conversion (Tier 3 to Tier 4)

- Shift to event-family suppression and route-defining legendaries, not marginal stat bumps.
- Legendary priority should follow your ending and economy target, not collection impulse.

## 10) Companion and Airport Branch Exploit

- Sanctuary route requirement is exact and binary: `Animal Whistle` + `5+ companions` at airport branch.
- If you are on Sanctuary line, lock it early and protect companion retention; do not treat companions as optional flavor.
- Airport ticket can be reversed in the branch decision flow, so you can probe timing without fully committing until route condition is ready.

## 11) Endgame Timing and Trigger Discipline

- Millionaire morning visitor triggers when you hit and hold `$1,000,000` and have not consumed that special visit yet.
- Final optimization rule:
  - Enter millionaire threshold only when your intended ending branch is already prepared (mechanic lock, companion count, whistle state, and key upgrades).
  - Do not rush the million if your route prerequisites are incomplete; reaching it early can force suboptimal branch pressure.

## 12) Full-Run Milestone Ladder

- Milestone A: Rank 1 map unlock online (`Worn Map`) + baseline survival kit.
- Milestone B: Tool Kit online + stable Tier 1 loadout.
- Milestone C: Rank 2 control phase with pool-shaping crafts and first Marvin control item.
- Milestone D: Debt-neutral or debt-contained economy with doctor/insurance stability.
- Milestone E: Branch lock complete (Tom/Frank/Oswald or Sanctuary setup).
- Milestone F: Tier 3/4 control stack complete + Back Room leverage.
- Milestone G: Controlled millionaire crossing with pre-selected ending execution.

If a run destabilizes, step down exactly one milestone and rebuild consistency before pushing bankroll growth again.

---

# ADVANCED ROUTE GUIDES

These are practical, system-level routes built from code behavior, not flavor text.

## 1) Companion and Pet Guarantees

### What can be guaranteed

- On many animal events, `Animal Whistle` converts the encounter into an automatic companion recruit if you do not already own that companion.
- This includes high-value recruits like `Asphalt` (Road), `Ursus` (Woodlands), `Deathclaw` (Beach crab event), and `Kraken` (Underwater boss event).
- `Animal Whistle` also guarantees multiple day-event recruits (`Lucky`, `Mr. Pecks`, `Patches`, `Hopper`, `Slick`, `Clover`, `Squirrelly`, `Don Coo`, `General Quackers`, and others) when those events fire.

### Non-whistle deterministic conversions

- `Fancy Cigars` + `Dog Whistle` in the road-dog style animal chain yields guaranteed `Scout`.
- `Bag of Acorns` in the squirrel invasion chain yields deterministic `Squirrelly` if not blocked by prior dead-state logic.
- `Animal Bait` in `stray_cat` lets you choose one recruit from cat/dog/possum/hawk immediately.
- `Birdseed` or `Bread` in crow encounter yields `Mr. Pecks` when you accept feeding.
- Food offer in sewer-rat encounter (`Cheese`, `Sandwich`, `Turkey Sandwich`, or `Animal Bait`) can convert into `Slick`.

### Important limitation

- These guarantees apply once the event appears. They do not hard-force event spawn by themselves.
- To increase animal-event frequency, prioritize animal-weighted tools (`Beast Tamer Kit`) and keep running zones/events where those companions live.

## 2) Mechanic Intro Mastery (Tom vs Frank vs Oswald)

### Intro economics and reliability

- `Tom` intro repair: $150-$350, high reliability (if you can pay, you get car and Tom route lock).
- `Frank` intro repair: $50-$100, but only 40% success on repair outcome after payment.
- `Oswald` intro repair: $800-$900, effectively guaranteed when paid, plus $50-$100 tip (net usually ~$700-$850).

### Optimal handling by goal

- Survival consistency goal: prefer `Tom` first successful repair.
- Cheapest possible early gamble: `Frank` only if you accept failure variance.
- Wealth route with upgrade plan: lock `Oswald` early so your ending path is aligned with Transcendence/Eternity planning.

### Why this matters

- First successful mechanic lock influences millionaire-route narrative branching and ending access.
- Delaying this decision until late creates route friction and can force suboptimal ending pivots.

## 3) Best Event Routes for Wealth

### Core wealth loop

- Stabilize in Rank 2 while building control inventory and workbench economy.
- Use adventure betting/competition spikes only when your health/sanity buffers are healthy.
- Convert unstable cash into durable edge (control items, upgrades, route enablers) before percentage-cost services.

### Highest-value adventure money spikes

- Underwater Deep Sea Hunting Championship: top placement can pay $50,000 + `Golden Trident`.
- Beach volleyball championship: strong top-end tournament payouts.
- Swamp tortoise racing: high upside via race success and longshot betting.
- Beach crab racing: high-odds outcomes and optional catch-your-own branch.
- City fighting ring bets can spike hard but are volatility-heavy.

### Supplemental wealth optimizers

- `Mr. Pecks` companion adds passive daily money finds.
- Pawn reputation increases sale multiplier (`0.5 + rep/200`, up to 1.2x).
- Marvin back-room power pieces convert survival into accelerated profit windows.

## 4) Best Event Routes to Avoid Death

### Medical stabilization first

- Doctor is deterministic stabilization:
  - Full heal,
  - Clears active status effects,
  - Treats one injury per visit,
  - Cost scales with current balance.
- Real insurance is the strongest anti-death economic shield for long runs.

### Volatility control rules

- Avoid carrying severe loan-shark warnings into consecutive days (encounter risk rises by warning tier).
- Do not stack 3+ active flasks casually:
  - Can hard-purge all flask effects,
  - Or inflict heavy direct HP damage (10-40), including lethal outcomes when low.
- Keep dealer hostility and fake-cash suspicion low when bankroll is fragile.

### Event-pool suppression path

- Prioritize combat-suppression and positive-event weighting inventory lines.
- Build one guaranteed exit tool, one heal line, one weather line, and one anti-car-failure line before greed scaling.

## 5) Adventure Gambling Games and How To Unlock Them

### Zone unlock model

- `The Road`: walk access at Rank 2+.
- `The Woodlands`: walk access at Rank 3+, after all 3 woodlands precursor events or prior woodlands adventure flag.
- `The Swamp` and `The Beach`: walk access at Rank 4+, with their respective precursor/event flags.
- Rank 5 relaxes most gating and broadens zone access.
- `The City`: Rank 5 + city progression flag logic.
- `Underwater`: tied to beach/underwater progression flags and Rank 5 access flow.

### Special gambling game map

- Road: `Cee-lo` street dice.
- Woodlands: Hunting competition enter/bet branches.
- Swamp: Tortoise race enter/bet branches.
- Beach: Volleyball tournament betting and crab racing betting/racing.
- Underwater: Deep Sea Hunting championship enter/bet branches.
- City: Underground den gambling and fight-ring betting.

### How to farm a specific mini-game

- Choose the exact zone repeatedly each afternoon once unlocked.
- Keep a bankroll buffer above each event's entry floor so opportunities are never skipped.
- Remove unrelated high-risk obligations (loan pressure, severe status) before minigame farming days.

## 6) Doctor vs Witch Doctor: Exact Practical Differences

### Doctor's Office

- Deterministic core recovery.
- Full health recovery each visit.
- Clears status effects and removes one injury per visit.
- Cost: 30-50% of current balance (modified by insurance interactions).

### Witch Doctor's Tower

- Volatile healing path with lower baseline cost (5-25% balance) but probabilistic outcomes.
- Grants flask economy access and high-impact one-shot effects.
- Overstacked flask risk can backfire hard.
- Has unique irreversible branch (tower closure) via violence path.

### Which one to choose

- Pick Doctor for guaranteed stabilization before critical route pushes.
- Pick Witch when deliberately planning a flask spike and you can absorb variance.

## 7) Guide to Unlocking All Endings

### Shared setup

- Reach and hold $1,000,000 to trigger millionaire morning flow.
- Ensure desired mechanic path is already locked before crossing the threshold.

### Tom branch

- Lock `Tom` as your mechanic.
- At millionaire branch, visit Tom for salvation/resurrection pathing.
- `Salvation (Healed)` requires Tanya progression (`5+` office visits) before the final morning flow.

### Frank branch

- Lock `Frank` as your mechanic.
- In final branch, follow Frank confrontation choices:
  - Shoot Dealer -> `To Kill a Dealer` route.
  - Shoot Frank -> `Retribution` route.

### Oswald branch

- Lock `Oswald` as your mechanic.
- Accept Oswald's final route for `Transcendence`.
- For `Eternity`, complete all 17 Oswald-upgrade lines before final resolution.

### Airport branch

- `Bliss`: take airport route and board.
- `Sanctuary`: airport route with `Animal Whistle` + 5+ companions, then take private-plane companion option.

### Collapse branches

- `Exhaust`: despair/low-stability collapse path.
- `Madness`: deep sanity collapse and dark-entity progression path.

### Completionist order recommendation

- Run 1: Tom Salvation (Healed if possible) for baseline stability.
- Run 2: Frank split routes.
- Run 3: Oswald Transcendence.
- Run 4: Oswald Eternity full-upgrade route.
- Run 5: Airport Bliss.
- Run 6: Sanctuary with companion-focused route.
- Final runs: force collapse endings intentionally after all stable branches are secured.

## 8) Companion Matrix (Fast Unlock + Guarantee Reference)

| Companion | Primary Event/Source | Guaranteed Method | Fallback Method | Common Failure/Blockers |
|---|---|---|---|---|
| Squirrelly | Squirrel invasion chain | Animal Whistle auto-bond | Bag of Acorns route, Companion Bed route | Dead-Squirrely state logic, event not rolled |
| Lucky | Three-legged dog encounter | Animal Whistle auto-bond | Accept recruit prompt | Event not rolled |
| Mr. Pecks | Crow encounter | Animal Whistle auto-bond | Feed Birdseed/Bread | Decline feed, event not rolled |
| Patches | Opossum encounter | Animal Whistle auto-bond | Accept recruit prompt | Event not rolled |
| Rusty | Raccoon encounter | High chance via catch path | Repeat encounter and retry catch | Bite/escape outcome branch |
| Slick | Rat/sewer encounter | Animal Whistle auto-bond | Food offer (Cheese/Sandwich/Turkey Sandwich/Animal Bait) | No food, decline offer |
| Hopper | Garden rabbit encounter | Accept recruit prompt | Animal Bait improves consistency | Decline recruit |
| Whiskers | Stray cat encounter | Animal Bait pick-list (cat) | Feed route in cat event chain | Choosing other Animal Bait target |
| Asphalt | Road adventure dog event | Animal Whistle auto-bond | Stop/follow route may bond | Event RNG |
| Ursus | Woodlands giant-bear event | Animal Whistle auto-bond | Non-whistle combat/survival path only | Event RNG |
| Deathclaw | Beach crab-racing event | Animal Whistle auto-bond | Race/bet branches (not guaranteed companion) | Event RNG |
| Kraken | Underwater giant-octopus event | Animal Whistle auto-bond | Non-whistle branch is boss encounter only | Event RNG |
| Scout | Animal event combo | Fancy Cigars + Dog Whistle combo | None | Missing combo components |

### Companion routing priority

- If your target is Sanctuary, treat `Animal Whistle` as a route-critical key item, not a luxury buy.
- Farm Road/Beach/Underwater once unlocked to accelerate high-value companion opportunities.
- Carry low-cost animal converters (Birdseed, Bread, Acorns, Animal Bait) when pushing companion count.

## 9) Ending Checklist Table (Lock Points + Failure Traps)

| Ending | Required Setup | Final Choice | Hard Lock Points | Common Mistake |
|---|---|---|---|---|
| Salvation (Healed) | Tom mechanic route + Tanya progress | Tom phone branch | Tanya progression must be done before final morning | Hitting millionaire trigger before Tanya setup |
| Salvation | Tom route | Accept Tom offer | Tom must be your meaningful mechanic branch | Wrong mechanic locked early |
| Resurrection | Tom route | Refuse Tom offer | Tom branch must be active | Taking airport/other branch first |
| To Kill a Dealer | Frank route | Shoot Dealer | Frank branch required | Not locking Frank early |
| Retribution | Frank route | Shoot Frank | Frank branch required | Taking wrong gun choice |
| Transcendence | Oswald route | Accept Oswald offer | Oswald branch required | Million hit before Oswald route prep |
| Eternity | Oswald route + all 17 upgrades | Oswald final route | Full upgrade completion required | Underestimating upgrade cash/time requirements |
| Bliss | Millionaire + airport access | Board plane | None beyond airport availability | Delaying too long and drifting into other lock-ins |
| Sanctuary | Bliss setup + 5+ companions + Animal Whistle | Private-plane companion option | Companion count + whistle must both be live at airport | Entering airport before 5 companions |
| Exhaust | Low-sanity collapse setup | Collapse path | Run-state dependent | Accidental recovery from sanity floor |
| Madness | Deeper sanity fracture path | Collapse path | Dark-entity/sanity progression | Recovering too early with hard stabilization |

## 10) Adventure Gambling EV Sheet (Practical Risk Bands)

| Mini-Game/Event | Typical Entry | Top Payout Band | Volatility | Best Use Case |
|---|---:|---:|---|---|
| Road Cee-lo | $50+ | 2x style hand outcomes | Medium | Early bankroll growth with strict stop-loss |
| Woodlands hunting competition | $5,000 | Mid/high five figures in top outcomes | High | Mid-game spike when HP/sanity healthy |
| Swamp tortoise race | $2,000 race / variable bet | Mid five figures in high-roll outcomes | High | Rank 3-4 push with surplus bankroll |
| Beach volleyball tournament | $3,000 join / variable bet | High four to low five figures | Medium-High | Controlled growth when injuries are low |
| Beach crab racing | $500 race / variable bet | High multiplier outcomes | High | Cheap high-variance shot taking |
| Underwater deep-sea hunt | $5,000 | ~$50,000 + key item at top result | Very High | Pre-endgame leap when fully stabilized |
| City fight-ring betting | Variable | High multiplier outcomes | Very High | Aggressive money route only |

### EV discipline rules

- Never enter high-volatility events while already under loan-shark pressure.
- Keep a minimum medical reserve before each high-risk entry window.
- Stop after one major win if your route goal is consistency, not leaderboard variance.

## 11) Doctor vs Witch Doctor Decision Grid (Day-to-Day Calls)

| Current State | Recommended Visit | Why |
|---|---|---|
| Low HP + multiple status effects + injury | Doctor | Deterministic reset, strongest survival stability |
| Moderate HP, no urgent status pressure, planned casino spike | Witch Doctor | Flask timing value can exceed doctor certainty |
| Heavy debt + fragile run | Doctor (or skip spending if stable) | Avoid compounding risk from volatile flask stack behavior |
| Near milestone push with known variance ahead | Witch Doctor (targeted flask only) | Planned spike is valid when controlled |
| Repeated high-risk days upcoming | Doctor then low-variance routing | Guarantees baseline survival before greed |

### Anti-overstack rule

- Do not casually maintain 3+ simultaneous flask effects unless deliberately accepting purge/damage risk.

## 12) Route Playbooks (Ready-To-Run)

### A) Low-Risk Consistency Run

1. Lock car reliably (`Tom` preferred).
2. Buy `Worn Map`, then `Tool Kit`, then build Tier 1 stability loadout.
3. Prioritize doctor stabilization over high-variance event entries.
4. Push Rank 2 control economy before attempting major spike events.
5. Hit millionaire threshold only after ending branch prerequisites are complete.

### B) Aggressive Wealth Run

1. Stabilize just enough to survive, then target high-EV adventure entries.
2. Use selective Marvin control stack for blackjack conversion.
3. Take higher multiplier betting branches in Beach/Swamp/Underwater windows.
4. Convert wins into route locks/upgrades immediately to prevent backslide.

### C) Sanctuary Completion Run

1. Hard-prioritize `Animal Whistle` acquisition.
2. Farm companion-rich events and zones while carrying animal-conversion items.
3. Track live companion count aggressively; aim to exceed 5 early.
4. Delay airport commit until whistle + count are both satisfied.

## 13) Trap List (And Anti-Trap Counterplay)

| Trap | Why It Kills Runs | Anti-Trap Counterplay |
|---|---|---|
| Early Monocle before debt planning | Increases Vinnie punishment rates | Delay Monocle if loan use is planned |
| Flask overstack for no reason | Can purge effects or inflict heavy HP damage | Keep flask usage intentional and sparse |
| Premature millionaire crossing | Forces endgame pressure before setup | Delay million push until route prerequisites are complete |
| Frank-only intro gamble when fragile | Cheap but unreliable repair success | Use Tom/Oswald when consistency matters |
| Adventure spike while medically unstable | One bad branch can end run | Heal first, spike second |
| Carrying high warning debt into event days | Random escalation encounters compound loss | Pay down early or avoid debt spiral |

## 14) Unlock Dependencies Graph (Quick Logic Map)

```text
Rank 1 -> Worn Map -> Marvin access
No Tool Kit -> Tool Kit guaranteed in convenience store -> Workbench crafting loop
Mechanic intro success -> Mechanic lock (Tom/Frank/Oswald) -> Endgame branch identity
Animal Whistle + Companion count >= 5 -> Sanctuary option at airport
Oswald route + all 17 upgrades -> Eternity route unlock
Rank progression + precursor adventure flags -> Full zone walk access
Millionaire threshold + prepared branch state -> Clean ending conversion
```

## 15) One-Page Cheat Sheet (In-Run)

### If you need money now

- Run one high-upside mini-game only when HP/sanity and debt state are stable.
- Convert gains into durable advantages, not random spending.

### If you need survival now

- Doctor first if status/injury stack is live.
- Drop one risk tier (event choice, bet size, route aggression) immediately.

### If you need Sanctuary

- Buy/roll for Animal Whistle.
- Farm companion events/zones with animal conversion items in inventory.
- Do not board at airport until whistle + 5+ companions are confirmed.

### If you need Eternity

- Lock Oswald early.
- Funnel capital into the 17-upgrade requirement efficiently.
- Avoid side-route cash bleed once upgrade grind starts.

### If run is spiraling

- Pause greed route.
- Stabilize health/sanity.
- Resolve debt pressure.
- Resume at previous milestone, not maximum aggression.

---

# CONVENIENCE STORE

*Run by Kyle. Buy 1–2 items per visit. Inventory refreshes every 7 days. Food rotates, wealth rank gates extra stock, many repair items can appear at any rank, and Tool Kit ($85) can appear whenever you do not already own it.*

### Always Available (All Ranks)
3 random food items (from: Candy Bar, Chips, Turkey Sandwich, Energy Drink, Beef Jerky, Cup Noodles, Granola Bar, Hot Dog, Microwave Burrito, Cheese, Bread, Sandwich) + Pest Control + Deck of Cards

### By Rank

| Rank | Balance | Notable Items | Key Unlocks |
|------|---------|--------------|-------------|
| 0 — Poor | $1–$1K | Lottery Ticket, Lucky Penny, Matches, Breath Mints, Rubber Bands, Birdseed, Baking Soda | Early survival and low-cost utility pool |
| 1 — Cheap | $1K–$10K | Worn Map ($8), Necronomicon ($666 ⚠️ trap), Dog Whistle, Running Shoes, Road Flares, Bug Spray, Disposable Camera | **Worn Map** → early Marvin access and map/event progression |
| 2 — Modest | $10K–$100K | Binoculars, Padlock, Fishing Line, Super Glue, Hand Warmers, Signal Booster, Welding Goggles | Strongest non-luxury utility stock |
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

*252 defined in the live source. Some unlock automatically from stats, others require specific actions or discoveries. Older docs that still say 245 or 500+ are out of date.*

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
