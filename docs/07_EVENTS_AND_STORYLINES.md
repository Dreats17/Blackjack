# 📖 EVENTS & STORYLINES GUIDE

*Every random event, multi-part storyline, and narrative arc in the game.*

---

## TABLE OF CONTENTS

1. [How Events Work](#how-events-work)
2. [Day Events by Wealth Rank](#day-events-by-wealth-rank)
3. [Night Events](#night-events)
4. [The Storyline System](#the-storyline-system)
5. [All Storylines](#all-storylines)
6. [Unlock Events](#unlock-events)
7. [Car Events](#car-events)
8. [Medical Events](#medical-events)
9. [Event Chains & Dangers](#event-chains--dangers)

---

## HOW EVENTS WORK

### Day Events
Each morning, the game checks for events in this priority order:

1. **Storyline Check** — The StorylineSystem checks if any active or new storyline should fire (escalating probability). Only **one storyline event per day**.
2. **Random Event Pool** — If no storyline fires, a random event is pulled from your current **wealth rank's event pool**.

Events are drawn from shuffled lists. Once every event in a list has been seen, the list is reshuffled. This ensures variety while guaranteeing you'll eventually see everything.

### Night Events
After gambling at the casino, a random night event occurs. Night events are separate from day events and include encounters, dreams, and the rabbit chase.

### Event Conditions
Many events have conditions that must be met before they trigger:
- **Rank-gated**: Only appear at certain wealth levels
- **Day-gated**: Only appear after a minimum number of days
- **State-gated**: Require specific player states (injuries, items, companions, etc.)
- **One-time**: Some events only fire once per playthrough

---

## DAY EVENTS BY WEALTH RANK

### Poor ($0–$999) — Survival Tier
The largest event pool. You're scraping by, and the world doesn't care.

**Life Events:**
- `seat_cash` — Find coins in your seat
- `left_window_down` — Left your window open (consequences)
- `morning_stretch` — Simple morning stretch
- `cloud_watching` — Peaceful moment watching clouds
- `talking_to_yourself` — You start conversations with no one
- `found_twenty` — Find a $20 bill
- `lost_wallet` — Lose your wallet
- `nice_weather` / `terrible_weather` — Weather affects your day
- `random_kindness` / `random_cruelty` — Strangers can be angels or demons
- `found_old_photo` — Memories of better times

**Creature Encounters:**
- `estranged_dog` — A stray approaches
- `stray_cat` — Meet a stray cat (can start Whiskers storyline)
- `three_legged_dog` — Meet Lucky
- `opossum_in_trash` — Meet Patches
- `sewer_rat` — Meet Slick
- `bird_droppings` — A bird... contributes to your day
- `seagull_attack` — Aggressive seagull encounter

**Danger Events:**
- `back_alley_shortcut` — Take the sketchy shortcut (health risk)
- `food_poisoning` — Bad food, bad day
- `attacked_by_dog` — Violent encounter
- `carbon_monoxide` — Silent killer in your car

**Social Events:**
- `conspiracy_theorist` — Meet a tinfoil hat enthusiast
- `coin_flip_stranger` — Gamble with a passerby
- `lone_cowboy` — Meet the mysterious cowboy
- `whats_my_name` — Suzy asks you a question (starts Suzy storyline)
- `interrogation` — Phil the interrogator

**Secret Events:**
- `midnight_visitor` — A mysterious visitor at your car
- `perfect_hand` — Something special happens with the cards

### Modest ($1,000–$9,999) — Getting By
Events expand. You're no longer invisible.

**New events include:**
- Officer Martinez encounters
- More complex social situations
- Better item-finding opportunities
- Expanded medical events
- Kyle's store interactions

### Well-Off ($10,000–$49,999) — Comfortable
The world starts noticing you have money.

**New events include:**
- Victoria the rival gambler appears ($50k+)
- More NPC interactions
- Bigger stakes in random encounters
- Car upgrade opportunities
- The Collector begins to circle ($100k+)

### Rich ($50,000–$249,999) — High Roller
Money brings new problems.

**New events include:**
- High-stakes encounters
- More complex storyline triggers
- Jealousy and rivalry events

### Very Rich ($250,000–$499,999) — Almost There
The endgame approaches.

**New events include:**
- Final storyline stages
- Pre-millionaire tension events

### Nearly There ($500,000–$999,999) — The Final Push
Everything builds toward the million.

---

## NIGHT EVENTS

Night events fire after your gambling session at the casino. They include:

**Common Night Events:**
- Strange dreams (vary based on sanity level)
- Nightmares (more frequent at low sanity)
- Car break-in attempts
- Mysterious sounds in the parking lot
- Wildlife encounters
- Stargazing moments
- Insomnia episodes

**The Rabbit Chase:**
A recurring night event where you can chase a rabbit. Successfully catching it over multiple encounters eventually leads to the **Rabbit's Blessing** item.

**Companion Night Bonuses:**
If you have companions with night bonuses (like Patches the opossum), they keep watch while you sleep, providing sanity restoration and fatigue reduction.

**Mechanic Dreams:**
Special dream sequences tied to whichever mechanic you've visited. Each mechanic's dreams reveal different lore:
- **Tom's Dreams**: Reveal secrets about Tom's family
- **Frank's Dreams**: Show the Dealer's dark history
- **Oswald's Dreams**: Expose the casino's true nature

Dream progress is tracked separately for each mechanic (0–3+ stages).

---

## THE STORYLINE SYSTEM

The `StorylineSystem` manages **multi-part narrative arcs** that fire as day events with escalating probability.

### How It Works
1. Each storyline has a **stage** counter (0 = not started)
2. **Start conditions** must be met for stage 0 → 1 (e.g., day count, balance, items, injuries)
3. Between stages, a **minimum gap** (in days) must pass
4. After the gap, there's a **base chance** per day for the next stage to fire
5. Each additional day past the gap adds **escalation** to the probability
6. Chance is capped at **95%** — you WILL eventually see the next stage

### System Rules
- Only **one storyline event fires per day**
- If multiple storylines are eligible, one is **chosen randomly**
- Storylines can be **completed** (all stages done) or **failed** (abandoned/wrong choices)
- Multiple storylines can be active simultaneously

---

## ALL STORYLINES

### 🎭 Suzy — "What's My Name?"
| Property | Value |
|---|---|
| **Stages** | 4 (meet → color question → animal question → finale) |
| **Min Gap** | 3 days |
| **Start Condition** | Player has a name (from whats_my_name event) |
| **Base Chance** | 15%, +10%/day escalation |

Suzy is a quirky, hopeful woman who asks you strange questions. Her storyline explores themes of identity and connection. Your answers to her questions affect the outcome.

### 🔍 Phil — The Interrogator
| Property | Value |
|---|---|
| **Stages** | 4 (interrogation → further → even further → final) |
| **Min Gap** | 4 days |
| **Start Condition** | Day 3+ |
| **Base Chance** | 12%, +8%/day escalation |

Phil is relentless. He asks increasingly probing questions about your life, your choices, and your gambling. Feels like a therapy session from hell.

### 👑 Victoria — The Rival
| Property | Value |
|---|---|
| **Stages** | 2 (the rival → Victoria returns) |
| **Min Gap** | 5 days |
| **Start Condition** | Balance ≥$50,000, Day 10+ |
| **Base Chance** | 15%, +10%/day escalation |

A rival gambler who challenges your dominance at the table. High-stakes confrontation.

### 🐄 Betsy — The Cow Chain
| Property | Value |
|---|---|
| **Stages** | 3 (hungry cow → starving cow → cow army) |
| **Min Gap** | 5 days |
| **Start Condition** | Day 5+ |
| **Base Chance** | 10%, +8%/day escalation |

What starts as a hungry cow by the road escalates into something... unexpected.

### 🐱 Stray Cat — Whiskers' Story
| Property | Value |
|---|---|
| **Stages** | 3 (befriended → sick → resolved) |
| **Min Gap** | 3 days |
| **Start Condition** | Day 2+ |
| **Base Chance** | 15%, +10%/day escalation |

A stray cat's journey from the streets to your heart. Depending on choices, Whiskers may live, have kittens, or die.

### 🌉 Bridge Angel
| Property | Value |
|---|---|
| **Stages** | 3 (contemplation → angel returns → the call) |
| **Min Gap** | 4 days |
| **Start Condition** | Health <30 OR Sanity <40, Day 7+ |
| **Base Chance** | 12%, +8%/day escalation |

A deeply emotional arc that triggers when you're at your lowest. Someone appears on a bridge. You decide whether to intervene.

### ⛽ Gas Station Hero
| Property | Value |
|---|---|
| **Stages** | 4 (robbery → recognized → interview → media consequences) |
| **Min Gap** | 3 days |
| **Start Condition** | Day 5+, Rank ≥1 (Modest) |
| **Base Chance** | 15%, +10%/day escalation |

You witness a gas station robbery. Your response leads to fame, interviews, and consequences.

### 💊 Painkiller — Addiction Arc
| Property | Value |
|---|---|
| **Stages** | 3 (chronic pain → addiction → withdrawal/dealer/overdose) |
| **Min Gap** | 2 days |
| **Start Condition** | Has "Shoulder Destroyed" injury |
| **Base Chance** | 20%, +12%/day escalation |

Painkillers for your injury spiral into addiction. Fast-paced and dangerous.

### 🎩 The Collector
| Property | Value |
|---|---|
| **Stages** | 4 (intro → small favor → payment → real offer) |
| **Min Gap** | 5 days |
| **Start Condition** | Balance ≥$100,000, Day 15+ |
| **Base Chance** | 10%, +8%/day escalation |

A mysterious figure who appears when you have real money. What does he really want?

### 🔧 Mechanic Dreams
| Property | Value |
|---|---|
| **Stages** | Progressive dream stages |
| **Min Gap** | 3 days |
| **Start Condition** | Met at least one mechanic, Day 5+ |
| **Base Chance** | 15%, +10%/day escalation |

Dreams shared with whichever mechanic you've visited most. Each reveals different lore.

### 🏪 Kyle — The Shopkeeper's Secret
| Property | Value |
|---|---|
| **Stages** | 5 (just another customer → Kyle's problem → after hours → Kyle's secret → finale) |
| **Min Gap** | 3 days |
| **Start Condition** | Day 5+ |
| **Base Chance** | 15%, +10%/day escalation |

Kyle seems like a normal convenience store clerk. He's not. Five-part arc with deepening revelations.

### 👮 Officer Martinez — The Law
| Property | Value |
|---|---|
| **Stages** | 4 (license check → wellness → favor → resolution) |
| **Min Gap** | 4 days |
| **Start Condition** | Day 4+ |
| **Base Chance** | 12%, +8%/day escalation |

An officer who starts by checking your license and ends up entangled in your life.

### 💉 Dr. Feelgood — The Prescription
| Property | Value |
|---|---|
| **Stages** | 5 (first pill → feeling better → price up → rock bottom → resolution) |
| **Min Gap** | 2 days |
| **Start Condition** | Has a severe injury (Broken Leg, Fractured Spine, etc.), Day 5+ |
| **Base Chance** | 20%, +12%/day escalation |

A back-alley doctor offering cheap fixes. The price goes up. And up. And up.

### 🤡 The Mime — Gerald's Story
| Property | Value |
|---|---|
| **Stages** | 5 (performance → encore → message → behind the paint → final act) |
| **Min Gap** | 5 days |
| **Start Condition** | Day 3+ |
| **Base Chance** | 10%, +8%/day escalation |

A street mime who communicates without words. Until he doesn't. What's behind the paint?

### 🤠 Jameson — The Rancher
| Property | Value |
|---|---|
| **Stages** | 4 (carrot → horse trouble → rustlers → one last ride) |
| **Min Gap** | 5 days |
| **Start Condition** | Day 5+ |
| **Base Chance** | 12%, +8%/day escalation |

An old rancher and his horses. Rustlers threaten everything. Can lead to befriending Thunder.

### 🔧 Stuart — The Side Hustle
| Property | Value |
|---|---|
| **Stages** | 4 (side hustle → good deal → bad deal → Oswald finds out) |
| **Min Gap** | 4 days |
| **Start Condition** | Day 5+ |
| **Base Chance** | 12%, +8%/day escalation |

Oswald's mechanic Stuart has a side business. What happens when the boss finds out?

### 👵 Grandma Eleanor — The Calls
| Property | Value |
|---|---|
| **Stages** | 5 (first call → recipe → bad news → gift → last call) |
| **Min Gap** | 4 days |
| **Start Condition** | Day 5+ |
| **Base Chance** | 12%, +8%/day escalation |

Your grandmother calls. She shares recipes, stories, and eventually... bad news. One of the most emotionally devastating arcs.

### 🐕 Lucky Dog — Origins
| Property | Value |
|---|---|
| **Stages** | 5 (befriended → who hurt you → previous owner → good boy → saves your life) |
| **Min Gap** | 3 days |
| **Start Condition** | Day 3+ |
| **Base Chance** | 15%, +10%/day escalation |

Lucky's backstory unfolds. Who hurt him? Who cut off his leg? The truth is darker than you imagined.

### 🃏 The Dealer's Past
| Property | Value |
|---|---|
| **Stages** | 5 (photo → journal → question → answer → choice) |
| **Min Gap** | 5 days |
| **Start Condition** | Day 5+ |
| **Base Chance** | 10%, +6%/day escalation |

The slowest-burning storyline. Fragments of the Dealer's ancient past emerge. Who is he really? Lowest escalation rate — this story takes its time.

### 😱 Sleep Paralysis
| Property | Value |
|---|---|
| **Stages** | 4 (can't move → it speaks → the offer → resolution) |
| **Min Gap** | 4 days |
| **Start Condition** | Day 4+ |
| **Base Chance** | 12%, +8%/day escalation |

Something visits you while you sleep. It can't be real. Can it?

### 📻 Radio Signal
| Property | Value |
|---|---|
| **Stages** | 4 (static → broadcast → source → who's watching) |
| **Min Gap** | 4 days |
| **Start Condition** | Day 4+ |
| **Base Chance** | 12%, +8%/day escalation |

Your car radio picks up a strange signal. Someone is broadcasting. Someone is watching.

### ⚰️ The Graveyard — Edgar's Request
| Property | Value |
|---|---|
| **Stages** | 4 (wandering → digger → your plot → Edgar's request) |
| **Min Gap** | 5 days |
| **Start Condition** | Day 5+ |
| **Base Chance** | 10%, +8%/day escalation |

You find a graveyard. There's a gravedigger named Edgar. And there's a plot with your name on it.

### 🎪 The Carnival
| Property | Value |
|---|---|
| **Stages** | 4 (lights → fortune teller → the game → pack up) |
| **Min Gap** | 1 day |
| **Start Condition** | Day 3+ |
| **Base Chance** | 40%, +25%/day escalation |

The fastest storyline — a traveling carnival that arrives and departs quickly. The fortune teller knows things she shouldn't. The carnival game is rigged. Or is it? Extremely high base chance and escalation — this arc moves fast.

### 🔒 The Lockbox
| Property | Value |
|---|---|
| **Stages** | 3 (the box → key hunt → who left it) |
| **Min Gap** | 3 days |
| **Start Condition** | Day 3+ |
| **Base Chance** | 15%, +10%/day escalation |

You find a mysterious lockbox. The key hunt spans multiple days. What's inside?

---

## UNLOCK EVENTS

### Grimy Gus — Pawn Shop Discovery
| Property | Value |
|---|---|
| **Stages** | 1 (one-shot discovery) |
| **Start Condition** | Day 7+, Rank ≥1 (Modest), haven't met Gus |
| **Base Chance** | 15%, +10%/day escalation |

A one-time event that unlocks **Grimy Gus's Pawn Shop** as an afternoon destination. After this event, you can sell items, collectibles, and (darkly) companions.

---

## CAR EVENTS

Your wagon is your home, and it breaks down. A lot. There are **47 car events** covering:

**Breakdowns & Failures:**
- Engine won't start
- Flat tires (multiple variants)
- Battery dead
- Overheating
- Transmission failure
- Brake failure
- Exhaust damage
- Fuel leaks

**Mechanic Visits:**
Car problems send you to one of three mechanics:
- **Tom's Trusty Trucks and Tires** — Friendly, fair, golden truck
- **Filthy Frank's Flawless Fixtures** — Rough around the edges, hidden darkness
- **Oswald's Optimal Outoparts** — Eccentric entrepreneur, Stuart does the real work

Each mechanic has unique dialogue, pricing, and personality. Visiting mechanics enough times unlocks the **upgrade system** and triggers **mechanic dreams**.

**Car Upgrades:**
Through events and mechanic visits, your wagon can receive improvements that reduce future breakdown frequency.

---

## MEDICAL EVENTS

### Illnesses (18 Types)
Contracted through Poor-tier events and specific encounters:

| Illness | Source Events |
|---|---|
| Common Cold | `contract_cold` |
| Flu | `contract_flu` |
| Strep Throat | `contract_strep_throat` |
| Ear Infection | `contract_ear_infection` |
| Sinus Infection | `contract_sinus_infection` |
| Pink Eye | `contract_pink_eye` |
| Ringworm | `contract_ringworm` |
| Scabies | `contract_scabies` |
| Rat Bite Fever | `rat_bite` |
| Needle-Stick Infection | `dirty_needle_stick` |
| Waterborne Illness | `unclean_water` |
| Mold Exposure | `mold_exposure` |
| Lead Poisoning | `lead_poisoning` |
| Food Poisoning (Severe) | `bad_oysters` |
| Shelter Outbreak | `homeless_shelter_outbreak` |
| Tattoo Infection | `bad_tattoo_infection` |
| Pool Infection | `public_pool_infection` |
| Food Truck Nightmare | `food_truck_nightmare` |

### Injuries (30+ Types)
From accidents, fights, and misfortune:

| Category | Examples |
|---|---|
| **Falls** | Slip in shower, Fall down stairs |
| **Fights** | Bar fight aftermath, Assault aftermath, Broken nose |
| **Fractures** | Broken leg, Broken wrist, Fractured spine |
| **Cuts** | Deep laceration, Severed skin, Knife wound infection |
| **Animal** | Dog attack severe, Dog bite rabies scare |
| **Car** | Whiplash injury |
| **Other** | Kitchen accident, Gut wound complications |

### Mental Health (5 Conditions)
| Condition | Event |
|---|---|
| Severe Anxiety Attack | `severe_anxiety_attack` |
| Severe Depression Episode | `severe_depression_episode` |
| Chronic Insomnia | `insomnia_chronic` |
| Stress Breakdown | `stress_breakdown` |
| Trauma Flashback | `trauma_flashback` |

### Treatment
- **The Doctor** (afternoon location): Treats illnesses and injuries for a fee
- **The Witch Doctor** (afternoon location): Alternative treatments with potions/flasks
- **Untreated conditions** worsen over time and can cause death

---

## EVENT CHAINS & DANGERS

Some events create **persistent dangers** — ongoing conditions that trigger follow-up events:

| Danger | Initial Event | Follow-Up Events |
|---|---|---|
| Shoulder Destroyed | Severe injury | Painkiller storyline trigger, chronic pain events |
| Fuel Leak | Car event | `fuel_leak_fire` or `fuel_leak_fixed` |
| Damaged Exhaust | Car event | `damaged_exhaust_fixed` or `damaged_exhaust_again` |
| Unpaid Tickets | Police event | `unpaid_tickets_boot` → `booted_car_impound` |
| Mystery Car Problem | Car event | `mystery_car_problem_worsens` |
| Soulless | Dark event | `soulless_emptiness`, `soulless_mirror` |
| Painkiller Dependency | Painkiller storyline | `painkiller_withdrawal` |

Dangers persist until resolved through events, mechanic visits, or doctor treatment.

---

*← Back to [06 — Companions](06_COMPANIONS.md) | Next: [08 — Endings & Achievements](08_ENDINGS_AND_ACHIEVEMENTS.md) →*
