# Item Live Reference

> Working master list for the item overhaul.
> This file exists primarily to keep implementation coverage honest while the overhaul is in progress.
> Over time, it should also become the easiest place to see what each important item physically does in the game.

---

## How To Use This File

- `Core Effect` is the item's real gameplay function, not just flavor text.
- `Live Uses Right Now` is the short summary of where the item currently matters in code.
- `Coverage` is the live implementation state:
  - `done`
  - `partial`
  - `under-covered`
  - `optional`
  - `cut`
- `Last Update` is the last overhaul batch that materially changed the row.

This file is the operational bridge between:

- `04_ITEMS_FLASKS_AND_UPGRADES.md` for item descriptions
- `ITEM_COMPLETION_LEDGER.md` for acceptance and missing work
- `ITEM_PLANNING_REMAINING.md` for category-level execution order

---

## Marvin Items

| Item | Core Effect | Live Uses Right Now | Coverage | Last Update |
|------|-------------|---------------------|----------|-------------|
| Sneaky Peeky Shades | Peek at the next blackjack card | Blackjack plus dark robbery reads, wealth surveillance mapping, night scouting, and conspiracy-event hidden-mic detection | done | Wave 1 batch 3 |
| Pocket Watch | Grants extra blackjack rounds | Blackjack plus surreal loop tension, an exact-$100 timing omen, and an Old Man Jenkins nostalgia beat that turns it into a real world-time item | done | Wave 1 batch 4 |
| Gambler's Chalice | Enhances double down play | Blackjack plus the social wine ritual and the night-drinking insomnia scene | done | Wave 1 doc audit |
| Twin's Locket | Enables pair splitting | Blackjack plus surreal identity scenes, the night true-sight combo, a social dual-self read, and a doppelganger scene that reframes the impostor | done | Wave 1 batch 5 |
| White Feather | Unlocks surrender and survival-style reprieves | Blackjack plus death-avoidance hooks and a mercy-forward desperate-gambler intervention | done | Wave 1 batch 4 |
| Lucky Coin | Sometimes turns losses into pushes | Blackjack plus car-luck saves, number-event luck reads, a trench-coat coin duel, and a softened devil bargain | done | Wave 1 batch 3 |
| Worn Gloves | Improves bust recovery odds | Blackjack plus handshake/deal confidence, classy social read, freezing-night dexterity control, and dark-scene no-prints utility | done | Wave 1 batch 7 |
| Tattered Cloak | Lets the dealer forget your bet on losses | Blackjack plus dark ambush avoidance, wealth surveillance evasion, reporter escape, and night stealth coverage | done | Wave 1 doc audit |
| Dirty Old Hat | Lowers the minimum bet by making you look poor | Blackjack, casino invisibility, reporter misdirection, social disguise value, wrong-item dinner fallout, and parking-ticket mercy | done | Wave 1 batch 5 |
| Faulty Insurance | May reduce doctor costs | Doctor-facing utility plus hospital and emergency-admission spillover, including carbon-monoxide ambulance billing | done | Wave 1 batch 5 |
| Delight Indicator | Reads emotional state, especially the Dealer's mood | Blackjack mood read plus wealth anxiety, surreal readings, companion mood moments, social telemetry, panic calibration, and new animal-mood reads | done | Wave 1 batch 9 |
| Health Indicator | Reads your physical condition | UI health warning plus diabetes, blood-pressure, migraine, and heat-warning early-detection support across illness and survival | done | Wave 1 batch 9 |
| Golden Watch | Signals status and helps extend table time | Blackjack, casino status, surveillance intimidation, social-status leverage, and high-roller presentation | done | Wave 1 doc audit |
| Quiet Sneakers | Lets you skip an unfavorable day event | Day-event avoidance now includes back-alley and electrocution escapes, plus ghost-mode and existing night danger avoidance identity | done | Wave 1 batch 7 |
| Rusty Compass | Helps find better outcomes and navigation paths | Adventure navigation, survival wayfinding, checkpoint rerouting, midnight return-home guidance, treasure steering, and lost-tourist route fixing | done | Wave 1 batch 6 |
| Dealer's Grudge | Enables side-bet style relationship pressure with the Dealer | Blackjack plus casino attention, media intimidation, dark hitman fear, surreal ownership reactions, people-event combo pressure, and rich-tier stranger recognition | done | Wave 1 batch 3 |
| Gambler's Grimoire | Tracks stats and acts like an omen-heavy book | Blackjack tracking plus numbers omens, car warnings, wealth validation, surreal prophecy beats, and a prophet scene where the book critiques the prophet | done | Wave 1 batch 3 |
| Marvin's Monocle | Reveals how much money is "hot" or dangerous | Economy and loan-shark visibility plus surreal truth-sight, interrogation tell-reading, and Mr. Pecks loot triage | done | Wave 1 batch 4 |
| Enchanting Silver Bar | Investment item that grows in sale value | Economy item with day-cycle value growth, a freight-trucker appraisal warning, and an investment-side appraisal lead that treats it like a serious asset | done | Wave 1 batch 6 |
| Animal Whistle | Recruits animals and unlocks companion paths | Deep integration across animals, companions, endings, and special encounters | done | pre-live-reference |

## Marvin Upgrades

| Item | Core Effect | Live Uses Right Now | Coverage | Last Update |
|------|-------------|---------------------|----------|-------------|
| Sneaky Peeky Goggles | Stronger, longer-lasting peek item | All Shades coverage plus a stronger conspiracy-event read that spots an earpiece and the surveillance sedan behind the warning | done | Wave 1 batch 3 |
| Grandfather Clock | Guarantees extra table rounds | Blackjack, absurd dealer banter, surreal time-loop control, and stronger timing-omen variants in number and nostalgia scenes | done | Wave 1 batch 4 |
| Overflowing Goblet | Stronger Chalice | Luxury, wealth, and strange drinking-event presence across social ritual and night drinking scenes | done | Wave 1 doc audit |
| Mirror of Duality | Stronger splitting item | Surreal identity scenes, true-sight combo value, a signature mirror fear-swap moment, and stronger social/doppelganger split-self reads | done | Wave 1 batch 5 |
| Phoenix Feather | Stronger surrender and stronger death-defiance | Signature survival item with resurrection saves, Sacred Flame combo value, and a stronger mercy-and-hope intervention for the desperate gambler | done | Wave 1 batch 4 |
| Lucky Medallion | Stronger luck reversal | All Lucky Coin coverage plus overt fate-manipulation in the devil bargain and guaranteed success in the trench-coat coin duel | done | Wave 1 batch 3 |
| Velvet Gloves | Stronger glove item | Stronger social leverage in handshake and classy scenes, plus improved freezing-night precision and existing dark utility inheritance | done | Wave 1 batch 7 |
| Invisible Cloak | Stronger stealth item | Casino invisibility, escape, surveillance, dark avoidance, and true night-time ghosting | done | Wave 1 doc audit |
| Unwashed Hair | Stronger poor/disguise item | Casino and social disguise, a stray-animal trust reaction, wrong-item dinner fallout, and stronger parking-mercy treatment from authority | done | Wave 1 batch 5 |
| Real Insurance | Guarantees doctor bill relief | Doctor-facing premium medical utility plus accident, ER, player-core admission, and carbon-monoxide emergency reassurance | done | Wave 1 batch 5 |
| Delight Manipulator | Reads and actively manipulates emotional state | Wealth, surreal, companion, social, panic, and new animal-extortion hostility control scenes with direct mood intervention | done | Wave 1 batch 9 |
| Health Manipulator | Reads and actively stabilizes health | Active stabilization in diabetes, blood-pressure crisis, migraine, and heat exposure, plus prior illness and panic support | done | Wave 1 batch 9 |
| Sapphire Watch | Stronger prestige watch | Casino prestige, surveillance intimidation, explicit high-status social recognition, and high-roller table presence | done | Wave 1 doc audit |
| Golden Compass | Stronger navigation and opportunity-finding item | Navigation, route correction, checkpoint rerouting, opportunity bias, and near-perfect route guidance for lost travelers | done | Wave 1 batch 6 |

## Legendary Crafts

| Item | Core Effect | Live Uses Right Now | Coverage | Last Update |
|------|-------------|---------------------|----------|-------------|
| Witch Doctor's Amulet / Amulet of Marvin | Planned legendary ritual charm | Tracked from ITEM_PLANNING only; live implementation status still unresolved | optional | planning audit |
| Road King's Crown | Planned legendary road-dominance craft | Tracked from ITEM_PLANNING only; live implementation status still unresolved | optional | planning audit |
| Dream Walker's Lens | Planned legendary dream/perception craft | Tracked from ITEM_PLANNING only; live implementation status still unresolved | optional | planning audit |
| Beast Master's Call / Master's Horn | Planned legendary animal-command craft | Tracked from ITEM_PLANNING only; live implementation status still unresolved | optional | planning audit |
| Gambler's Soul / The Loaded Deck | Planned legendary endgame gambling craft | Tracked from ITEM_PLANNING only; live implementation status still unresolved | optional | planning audit |
| Dealer's Mercy | Upgraded Dealer relationship item | Casino recognition, media intimidation, dark hitman deterrence, surreal protection, people-event combo authority, and a rich-tier visitor who confirms you are under protection | done | Wave 1 batch 3 |
| Oracle's Tome | Upgraded grimoire | Prediction, prophecy, omen, and warning value across surreal, dark, wealth, car, number, and prophet scenes, with the new encounter treating it like a literal answer key | done | Wave 1 batch 3 |
| Quiet Bunny Slippers | Stronger event-skip item | Stronger day-event avoidance in ambush and electrocution scenes, plus night ghost-mode stealth and animal-calming behavior | done | Wave 1 batch 7 |

## Flasks

| Item | Core Effect | Live Uses Right Now | Coverage | Last Update |
|------|-------------|---------------------|----------|-------------|
| Flask of No Bust | Prevents busting on key hands | Blackjack plus dark, numbers, survival, and illness "refuse to collapse" branches during extreme danger | partial | Wave 1 batch 9 |
| Flask of Imminent Blackjack | Strongly improves blackjack draws | Blackjack core plus non-table omen and probability-sense beats in numbers and survival luck events | partial | Wave 1 batch 9 |
| Flask of Dealer's Whispers | Reveals hole-card style information and unlocks insurance | Blackjack core identity plus some eerie flavor potential | partial | pre-live-reference |
| Flask of Bonus Fortune | Improves winnings | Wealth-facing overflow text plus survival and numbers windfall amplification outside casino contexts | done | Wave 1 batch 10 |
| Flask of Anti-Venom | Prevents venom or poison effects | Repeated venom and toxin neutralization across survival, illness, and companion recovery branches | done | Wave 1 batch 9 |
| Flask of Anti-Virus | Prevents illness or viral effects | Illness-chain interruption, contamination defense, companion treatment, and sepsis mitigation across multiple files | done | Wave 1 batch 9 |
| Flask of Fortunate Day | Biases day events toward positive outcomes | Explicit payoff branches in wealth exact-number and rare paparazzi-luck events with clear felt positive outcomes | done | Wave 1 batch 10 |
| Flask of Fortunate Night | Biases night events toward positive outcomes | New jogging and midnight-walk fortune detection branches now make night-luck presence strongly visible | done | Wave 1 batch 10 |
| Flask of Second Chance | Gives a retry-style safety net | Dark back-alley ambush time-reversal escape plus existing table identity now providing fate-defiance across contexts | partial | Wave 1 batch 10 |
| Flask of Split Serum | Improves splitting behavior | Social encounter dual-path conversation branching now provides non-table narrative use alongside table identity | partial | Wave 1 batch 10 |
| Flask of Pocket Aces | Guarantees an ace start | Deja-vu event hidden-ace omen discovery now provides non-casino narrative moment outside gambling context | partial | Wave 1 batch 10 |
| Flask of Dealer's Hesitation | Delays or disrupts dealer momentum | Already has both table and narrative presence | done | pre-live-reference |

## Crafted Items

| Item | Core Effect | Live Uses Right Now | Coverage | Last Update |
|------|-------------|---------------------|----------|-------------|
| Shiv | Improvised combat weapon | Combat and defense item with some expanded event presence | partial | pre-live-reference |
| Slingshot | Ranged improvised weapon | Crow deterrent (scares away seagull-sized threats), pigeon-mafia intimidation (saves tribute money), animal evasion | partial | Wave 1 batch 11 |
| Road Flare Torch | Temporary light and threat deterrent | Back-alley combo with Scrap Armor (blazing knight defender), swamp-wade navigation (safe path through darkness), night visibility | partial | Wave 1 batch 11 |
| Pepper Spray | Guaranteed escape from many threats | Good emergency tool, still too isolated from broader event families | partial | pre-live-reference |
| Improvised Trap | Early warning and defense trap | Good fit for night, dark, and camp defense, but still thin | under-covered | pre-live-reference |
| Car Alarm Rigging | Vehicle security tool | Security and anti-theft identity, but not yet saturated | partial | pre-live-reference |
| Snare Trap | Animal-catching and pursuer-tripping tool | Strong survival identity, still underused outside narrow scenes | under-covered | pre-live-reference |
| Home Remedy | Basic illness cure item | Illness support item that still needs more real narrative reach | under-covered | pre-live-reference |
| Wound Salve | Wound-healing craft | Good medical identity, still needs more field-event presence | under-covered | pre-live-reference |
| Splint | Stabilizes broken limbs or sprains | Strong injury identity, still underused across night and companion scenes | under-covered | pre-live-reference |
| Smelling Salts | Revives and restores sanity or consciousness | Good crisis item, still not spread widely enough | under-covered | pre-live-reference |
| Lockpick Set | Opens locked things | Adventure and infiltration tool with obvious room to grow | partial | pre-live-reference |
| Fishing Rod | Enables fishing | Adventure and food utility, narrow but valid | partial | pre-live-reference |
| Binocular Scope | Enhanced scouting tool | Strong scouting identity, still underused across files | under-covered | pre-live-reference |
| Signal Mirror | Signaling and rescue tool | Strong survival identity, still underused across files | under-covered | pre-live-reference |
| Lucky Charm Bracelet | Passive luck charm | Light luck utility with room for more people and wealth scenes | partial | pre-live-reference |
| Dream Catcher | Reduces nightmares and anchors surreal combos | Night and surreal identity with combo value | partial | pre-live-reference |
| Worry Stone | Restores calm and reduces stress | Good sanity item, still too isolated | under-covered | pre-live-reference |
| Rain Collector | Passively gathers water | Strong survival concept, still needs broader event hooks | under-covered | pre-live-reference |
| Emergency Blanket | Cold and exposure protection | Good survival item, still underused in companion and night scenes | under-covered | pre-live-reference |
| Smoke Signal Kit | Signaling and calling attention | Survival and rescue utility with some expansion room | partial | pre-live-reference |
| Fire Starter Kit | Starts fires reliably | Core survival tool that should matter in more than one file | under-covered | pre-live-reference |
| Water Purifier | Makes water safe to drink | Good illness and survival identity, still needs more spread | partial | pre-live-reference |
| Companion Bed | Improves companion rest and comfort | Companion support item with room for more unique interactions | partial | pre-live-reference |
| Pet Toy | Improves companion happiness | Companion support and combo anchor | partial | pre-live-reference |
| Feeding Station | Improves companion feeding logistics | Companion support and combo anchor | partial | pre-live-reference |

## High-Impact Store Items

| Item | Core Effect | Live Uses Right Now | Coverage | Last Update |
|------|-------------|---------------------|----------|-------------|
| Lottery Ticket | Tiny gambling novelty item | Exists, but still needs either a memorable payoff or a deliberate filler ruling | under-covered | pre-live-reference |
| Necronomicon | High-risk occult store book | Documented elsewhere and implied alive in current planning, but it was missing from the live reference table | partial | planning audit |
| Dog Whistle | Animal or companion command tool | Companion and animal support, but still has room to expand | partial | pre-live-reference |
| Running Shoes | Escape and chase tool | Rat encounter speed burst (outrun attackers), drug-dealer chase (early escape velocity + high survival rate), dark escape specialist | partial | Wave 1 batch 11 |
| Disposable Camera | Evidence, keepsake, or proof item | Some surreal or companion use exists, still needs broader event utility | under-covered | pre-live-reference |
| Binoculars | Basic scouting tool | Already appears in several places, but still has room to deepen | partial | pre-live-reference |
| Deck of Cards | Social gambling prop and combo item | Social, companion, and combo identity, but still lighter than it should be | under-covered | pre-live-reference |
| Fancy Cigars | Luxury social item | Social and wealth flavor with more room for strong hooks | partial | pre-live-reference |
| Gold Chain | Status symbol | Social and wealth credibility signal with some existing live use | partial | pre-live-reference |
| Vintage Wine | Social, gifting, and dominance item | Good social identity, combo value, and event leverage | partial | pre-live-reference |
| Expensive Cologne | Social impression item | Existing social utility, still has room to spread | under-covered | pre-live-reference |

## Adventure Reward Items

| Item | Core Effect | Live Uses Right Now | Coverage | Last Update |
|------|-------------|---------------------|----------|-------------|
| Road Warrior Badge | Planned road-zone completion reward | Tracked from ITEM_PLANNING only; live implementation status still unresolved | optional | planning audit |
| Underground Pass | Planned city-zone access reward | Tracked from ITEM_PLANNING only; live implementation status still unresolved | optional | planning audit |
| Druid's Staff | Planned woodland-zone nature reward | Tracked from ITEM_PLANNING only; live implementation status still unresolved | optional | planning audit |
| Swamp Rune | Planned swamp-zone poison protection reward | Tracked from ITEM_PLANNING only; live implementation status still unresolved | optional | planning audit |
| Sea Glass | Planned beach-zone sale-discount reward | Tracked from ITEM_PLANNING only; live implementation status still unresolved | optional | planning audit |
| Depth Charm | Planned underwater-zone loot reward | Tracked from ITEM_PLANNING only; live implementation status still unresolved | optional | planning audit |

## Premium Endgame Shop

| Item | Core Effect | Live Uses Right Now | Coverage | Last Update |
|------|-------------|---------------------|----------|-------------|
| Dealer's Mirror | Planned premium shop mirror for dealer insight | Tracked from ITEM_PLANNING only; live implementation status still unresolved | optional | planning audit |
| The Last Card | Planned premium shop one-shot perfect-card item | Tracked from ITEM_PLANNING only; live implementation status still unresolved | optional | planning audit |
| Marvin's Eye | Planned premium shop hidden-outcome reader | Tracked from ITEM_PLANNING only; live implementation status still unresolved | optional | planning audit |
| Bottle of Tomorrow | Planned premium shop day-skip recovery item | Tracked from ITEM_PLANNING only; live implementation status still unresolved | optional | planning audit |
| Blank Check | Planned premium shop universal free-purchase item | Tracked from ITEM_PLANNING only; live implementation status still unresolved | optional | planning audit |

## Optional System-Dependent Families

| Family | Core Effect | Live Uses Right Now | Coverage | Last Update |
|--------|-------------|---------------------|----------|-------------|
| Secret Marvin back room items | Planned premium endgame shop inventory | Item-by-item rows now exist above; keep this as the system-level reminder only | optional | planning audit |
| Adventure reward items | Planned zone-specific persistent reward items | ITEM_PLANNING names six zone rewards, now tracked here as a dedicated optional section | optional | planning audit |
| NPC gift-target items | Expanded gifting targets beyond the Dealer | Depends on whether gifting expansion remains in scope | optional | pre-live-reference |
| Companion quest reward items | Unique quest-chain item rewards | Planning names examples like Thunder's Horseshoe, Bubbles' Scale, Buddy's Collar, Grace's Antler, and Slick's Ratstone, but the system is still unresolved | optional | planning audit |
| Lore-discovery items | Items that unlock backstory through use | Depends on whether lore-discovery remains in scope | optional | pre-live-reference |

---

## Maintenance Rule

When an overhaul batch lands:

1. Update the affected rows here.
2. Update the same rows in `ITEM_COMPLETION_LEDGER.md`.
3. Update wave or category progress in `ITEM_PLANNING_REMAINING.md`.
4. Update `04_ITEMS_FLASKS_AND_UPGRADES.md` when the item's practical behavior changed in a player-visible way.
