# 07 — Events & Storylines

---

## Event System Overview

Events fire during **day** and **night** phases, providing narrative, challenge, rewards, and long-form story arcs.

| Concept | Description |
|---|---|
| **Phase-based** | Day and night events fire separately |
| **Rank-based pools** | Each wealth rank has different eligible events |
| **Weighted tiers** | Events weighted by copies: `[poor, cheap, modest, rich, doughman, nearly]` |
| **One-time vs repeatable** | Some fire once then are removed from the pool |
| **Weather/status gating** | Conditions filter eligible events |

---

## Day Events

### Survival Events (60+)

**Money Finding:** Seat cash, sun visor bills (5% rare: $800–$2,000), found $20, strong winds (3% rare: $300–$800).

**Pests:** Spiders (bite status), cockroaches (money loss), ants, rats, termites. Bug Spray prevents mosquitoes.

**Weather:** Flat tire (Spare Tire prevents), rain (blocks casino), morning fog, dead battery.

**Illness Chain:** Sore throat → Cold → Flu → Pneumonia (escalating if untreated). Cough Drops cure sore throat.

**Item-Gated:**

| Item | Effect |
|---|---|
| Sunscreen | Prevents sunburn |
| Umbrella/Poncho | Prevents cold from rain |
| Hand Warmers | Survives freezing |
| Road Flares/Flashlight | Flags tow truck |
| Bug Spray | Prevents mosquitoes |
| Fancy Pen | Document signing +$100–$300 |

**Emotional:** Beautiful sunrise (+5–15 HP), random kindness (gifts), random cruelty (−12 sanity), prayer events.

### Animal Events
Companion encounters, wildlife interactions. Animal Whistle enhances these.

### Casino-Adjacent Events
Dealer interactions outside the table, casino atmosphere, other gamblers' stories.

### Companion Events
Per-companion story beats, happiness interactions, feeding/care events.

### Dark Events
Muggings, violent confrontations, theft, escalating danger at higher ranks.

### Item Events
Item discovery, usage triggers, item-centered narratives.

### Number Events

| Trigger | Event |
|---|---|
| $1,111 | Make a wish (heal 50, +$100–300, Lucky) |
| $777,777 | Lucky sevens (Lucky + 30 HP) |
| Palindrome day | Special event |
| Prime number day | Unique encounter |

### People Events
Random NPC encounters, stranger interactions, social events.

### Surreal Events (15+)

**Weird:** Time loop, mirror reflection, glitch reality, wrong universe, fourth-wall stranger.

**Dark:** The Collector (soul bargain), Empty Room (−20 sanity), Blood Moon Bargain (luck for 1 year of life).

**Goofy:** Alien abduction, dance battle, sock puppet therapist.

### Wealth Events (40+)

**Milestones:** $50k celebration, $250k golden butterfly (+$1,000), $999,999 wind blows $1.

**Luxury Problems:** Paparazzi (5% earn $1–3k), loan requests, wealth anxiety, imposter syndrome.

**Critical:** Victoria (rival, $50k+), Tax Man ($150k+), The Offer (double balance if you quit), Final Temptation (+$10–50k, −25 sanity).

---

## Night Events

- Dream sequences tied to mechanic NPCs (Tom/Frank/Oswald)
- Per-rank pools with depletion system
- Low sanity unlocks darker events
- Standalone encounters during sleep

---

## Illness System (80+ conditions)

### Severity Tiers

| Tier | Count | Damage | Examples |
|---|---|---|---|
| Minor | 30+ | 3–10 HP, −1–2 sanity | Cold, sore throat, sprains, pink eye |
| Moderate | 40+ | 12–25 HP, −2–4 sanity | Pneumonia, kidney stones, seizure |
| Severe | 20+ | 28–45 HP, −3–6 sanity | Collapsed lung, gangrene, skull fracture |
| Mental | 6+ | −7–12 sanity | PTSD, depression, psychosis |

### Infection Chains
Dirty needle → blood disease, food poisoning → dehydration, staph → sepsis, rabies → encephalitis, cold → flu → pneumonia.

### Injury Events (20+)
Gym accident, car crash, bar fight, grease fire, dog attack, electrical shock, botched surgery, and more.

---

## Car Events

Flat tire, dead battery, engine overheating, oil leak, broken window, damaged mirror. Roadside mechanics have **45% trigger chance**.

---

## Multi-Part Storylines (20+)

### Character Arcs

| NPC | Stages | Theme |
|-----|--------|-------|
| Suzy | 3 | Questions → gift or arrest |
| Kyle | 5 | Casino regular with a secret |
| Martinez | 4 | Lost brother |
| Dr. Feelgood | 5 | Addiction spiral |
| Jameson | 4 | Cowboy out of time |
| Grandma | 5 | Phone call connection |
| Lucky Dog | 4 | Scarred stray → loyalty |
| Gerald | 5 | Mime's hidden identity |
| Stuart | 4 | Oswald's apprentice side hustle |
| Rosa | 4 | Laundromat drifter and her sister's suitcase |
| Eli | 4 | Revival-tent mercy and practical faith |
| Rex | 4 | Pawned luck and a gambler's last lesson |

### Danger Arcs

| NPC | Stages | Theme |
|-----|--------|-------|
| Phil | 4 | Interrogator escalation |
| Victoria | 2 | Rival at $50k+ |
| Betsy | 3 | Cow invasion |
| Gas Station Hero | 3 | Robbery witness |
| Painkiller | 3 | Injury addiction |

### Emotional Arcs

| NPC | Stages | Theme |
|-----|--------|-------|
| Bridge Angel | 3 | Suicide prevention (sanity ≤ 30) |
| Dealer's Past | 5 | Dealer's former life revealed |
| Sleep Paralysis | 4 | Shadow entity temptation |
| Graveyard | 4 | Edgar's existential philosophy |

### Discovery Arcs

| NPC | Stages | Theme |
|-----|--------|-------|
| Radio Signal | 4 | Alan's observer station |
| Carnival | 4 | Professor Midnight's reality-bending |
| The Collector | 1 | $100k+ proposition |

---

## Chain Quest Events (4 chains × 5 stages)

### Hermit Trail
Map → Journal → Walking Stick → Stranger → Hollow Oak treasure

### Midnight Radio
Signal Booster → Broadcast → Frequency Dial → Station → Record

### Junkyard Artisan
Goggles → Metal Rose → Toolkit → Gideon's Backstory → Junkyard Crown

### Lost Dog Flyers
Flyers → Investigate → Whistle → Culprit → Neighborhood Party

**4 crossover events** when completing 2+ chains.

---

## Mechanic Dream Chains

### Tom's Dreams
**Rebecca → Nathan → Johnathan** — Player's true identity revealed.

### Frank's Dreams
**Dealer's anger → Scarred face → Revolver → Joker card** — Dealer's trauma.

### Oswald's Dreams
**Casino bar → Mirror-self table → Rain of wealth** — Wealth temptation.

---

## Tanya Therapist

| Detail | Value |
|---|---|
| **Spawn** | 5% per day after day 12 |
| **Mechanic** | Phone number → repeatable therapy |
| **Ending** | 5+ visits → **Salvation (Healed)** |

---

## Storyline Mechanics

- **Stage system** — numbered stages, one per day max
- **Timing controls** — `force_start_day`, minimum day gaps, escalating probability
- **Pool depletion** — one-time events removed after firing
- **State persistence** — storyline progress saved across sessions
