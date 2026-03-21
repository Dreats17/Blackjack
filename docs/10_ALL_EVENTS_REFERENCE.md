# All Events Reference

> Complete catalog of every event pool and individual event in the game.

---

## Event Pool Architecture

Events are organized into **phase → category → pool** with weighted tier distribution.

### Weight System

Each event has a **copies array** defining how many copies exist per wealth rank:

```
[poor, cheap, modest, rich, doughman, nearly_there]
```

More copies = higher probability at that rank. Events with `[0,0,0,1,1,1]` only appear at rich+.

### Depletion

One-time events are removed from the pool after firing. Repeatable events stay.

### Gating

Events can require:
- Specific items (Map, Tool Kit, etc.)
- Minimum/maximum balance
- Specific status effects
- Weather conditions
- Companion ownership
- Storyline progress
- Minimum day number

---

## Day Events by Category

### Survival Events (~60)

**Money Finding:**
- Crumpled bills in seat ($5–$50)
- Sun visor cash ($10–$80; 5% rare: $800–$2,000)
- Found $20 on ground
- Strong winds ($5–$50; 3% rare: $300–$800)
- Loose change in vending machine

**Pest Events:**
- Spider in car (bite → swell, treat or escalate)
- Cockroach infestation (lose food items)
- Ant colony (minor annoyance)
- Rat in car (damage items)
- Termites (car damage)
- Mosquitoes (Bug Spray prevents)

**Weather Events:**
- Flat tire (Spare Tire auto-fix)
- Heavy rain (blocks casino trip)
- Morning fog (reduced event pool)
- Dead battery (jumper cables or wait)
- Heatwave (+fatigue)
- Freezing night (Hand Warmers save)

**Illness Triggers:**
- Sore throat → Cold → Flu → Pneumonia
- Food poisoning → Dehydration
- Dirty needle → Blood disease
- Minor cut → Infection → Sepsis
- Animal bite → Rabies
- Sunburn (Sunscreen prevents)

**Emotional Events:**
- Beautiful sunrise (+5–15 HP)
- Random act of kindness (gift)
- Random cruelty (−12 sanity)
- Prayer at roadside shrine
- Nostalgic memory (+sanity)
- Nightmare aftermath (−sanity)

**Item-Gated Events:**

| Required Item | Event |
|---|---|
| Sunscreen | Prevents sunburn |
| Umbrella/Poncho | Prevents cold from rain |
| Hand Warmers | Survives freezing |
| Road Flares | Flags passing help |
| Flashlight | Night visibility events |
| Bug Spray | Blocks mosquitoes |
| Fancy Pen | Sign documents (+$100–300) |
| Cough Drops | Cure sore throat |
| Spare Tire | Auto-fix flat tire |

### Animal Events (~25)

- Companion discovery events (1 per companion type)
- Wildlife encounters (deer, hawk, snake)
- Animal Whistle enhanced encounters
- Feeding/care companion events
- Companion happiness milestones
- Companion mood dialogues (24 per companion)

### Casino-Adjacent Events (~15)

- Dealer small talk
- Other gamblers' stories
- Casino atmosphere (rank-dependent)
- VIP lounge access (High Roller Keycard)
- Grandfather clock trigger
- Casino distortions (low sanity)

### Companion Events (~20)

- Per-companion unique story beats
- Companion interaction events
- Companion protection triggers
- Companion special ability activations
- Companion selling events (dark path)

### Dark Events (~20)

- Mugging (Bruno prevents)
- Theft (lose random item)
- Violent confrontation
- Tony's visit (debt escalation)
- Stalker encounter
- Night attack
- Car break-in

### Item Events (~30)

- Item discovery (random finds)
- Item usage triggers
- Crafting discoveries
- Tool Kit unlocks
- Map-gated location reveals
- Pawn shop opportunities
- Item degradation (durability)

### Number Events (~10)

| Balance/Day | Event |
|---|---|
| $1,111 | Wish event (heal, money, Lucky) |
| $777,777 | Lucky sevens (Lucky, +30 HP) |
| $999,999 | Wind blows $1 |
| Palindrome day | Special encounter |
| Prime number day | Unique event |
| Day 7 multiples | Weekly events |
| Day 100 | Century milestone |

### People Events (~25)

- Stranger encounters
- Hitchhiker events
- Street performer
- Lost tourist
- Angry local
- Friendly neighbor
- Phone call events
- Grandma storyline beats
- NPC introduction events

### Surreal Events (~15)

**Weird:**
- Time loop (repeat previous day)
- Mirror reflection (wrong face)
- Glitch in reality (matrix moment)
- Wrong universe (everything slightly off)
- Fourth-wall stranger (knows they're in a game)

**Dark:**
- The Collector ($100k+ soul bargain)
- Empty Room (−20 sanity)
- Blood Moon Bargain (luck ↔ 1 year of life)
- Shadow entity (sanity < 30)
- Void whispers

**Goofy:**
- Alien abduction (lose time)
- Dance battle (win prizes)
- Sock puppet therapist (+sanity)
- Singing telegram
- Conspiracy theorist

### Wealth Events (~40)

**Milestone Celebrations:**
- $10k first big milestone
- $50k celebration night
- $100k golden butterfly
- $250k golden butterfly (+$1,000)
- $500k halfway party
- $999,999 wind event

**Luxury Problems:**
- Paparazzi (5%: earn $1–3k from photos)
- Loan requests from strangers
- Wealth anxiety (−sanity)
- Imposter syndrome
- Gold-digger encounter

**High-Stakes Events:**
- Victoria rival ($50k+): 2-stage rivalry
- Tax Man ($150k+): pay or evade
- The Offer: double balance if you quit forever
- Final Temptation: +$10–50k, −25 sanity

---

## Night Events

### Dream Sequences

**Tom's Dreams (3 stages):**
1. Rebecca at a window
2. Nathan learning to walk
3. "John, please come home"

**Frank's Dreams (4 stages):**
1. Dealer's blazing eyes
2. Scarred face close-up
3. Revolver on green felt
4. Joker card burns

**Oswald's Dreams (3 stages):**
1. Crystal casino bar
2. Mirror-self dealing cards
3. Rain of golden coins

### Per-Rank Night Pools

Each rank has unique night events that deplete after firing:

| Rank | Pool Size | Theme |
|------|-----------|-------|
| Poor | ~15 | Survival anxiety, cold nights |
| Cheap | ~15 | Money worries, small hopes |
| Modest | ~12 | Growing confidence, new fears |
| Rich | ~10 | Wealth paranoia, luxury dreams |
| Doughman | ~8 | Isolation, power fantasies |
| Nearly There | ~5 | Endgame visions, final choices |

### Sanity-Gated Night Events

| Sanity Range | Events |
|---|---|
| < 50 | Disturbing dreams |
| < 30 | Shadow entity, sleep paralysis |
| < 15 | Madness visions, ending triggers |

---

## Illness Events (~80)

### Minor (30+)

| Illness | HP Loss | Sanity Loss | Cure |
|---------|---------|-------------|------|
| Sore throat | 3 | −1 | Cough Drops |
| Common cold | 5 | −1 | Doctor / time |
| Headache | 3 | −2 | Painkillers |
| Minor cut | 4 | 0 | First Aid Kit |
| Sprain | 5 | −1 | Rest |
| Pink eye | 3 | −1 | Doctor |
| Sunburn | 5 | −1 | Sunscreen (prevent) |
| Bug bites | 3 | −1 | Bug Spray (prevent) |

### Moderate (40+)

| Illness | HP Loss | Sanity Loss | Notes |
|---------|---------|-------------|-------|
| Flu | 12 | −2 | Chains from cold |
| Pneumonia | 20 | −3 | Chains from flu |
| Food poisoning | 15 | −2 | Random |
| Kidney stones | 18 | −3 | Random |
| Seizure | 15 | −4 | Low health trigger |
| Infection | 12 | −2 | Chains from cuts |
| Dehydration | 10 | −2 | Chains from food poisoning |

### Severe (20+)

| Illness | HP Loss | Sanity Loss | Notes |
|---------|---------|-------------|-------|
| Collapsed lung | 35 | −5 | Rare |
| Gangrene | 40 | −5 | Untreated infection |
| Skull fracture | 45 | −6 | Injury event |
| Sepsis | 38 | −5 | Chains from staph |
| Encephalitis | 42 | −6 | Chains from rabies |

### Mental (6+)

| Condition | Sanity Loss | Trigger |
|-----------|-------------|---------|
| PTSD | −7 | Trauma events |
| Depression | −8 | Sustained low sanity |
| Psychosis | −12 | Extreme sanity loss |
| Anxiety | −7 | Wealth + stress |
| Paranoia | −9 | Dark events |
| Insomnia | −8 | Night events |

---

## Car Events (~15)

| Event | Effect | Prevention |
|-------|--------|-----------|
| Flat tire | Can't drive | Spare Tire |
| Dead battery | Can't drive | Jumper Cables |
| Engine overheating | Damage | Coolant |
| Oil leak | Gradual damage | Mechanic visit |
| Broken window | Security risk | Mechanic visit |
| Damaged mirror | Minor | Mechanic visit |
| Radiator crack | Can't drive | Mechanic visit |
| Brake failure | Dangerous | Mechanic visit |

**Roadside mechanic:** 45% trigger chance when car breaks down.

---

## Summary Statistics

| Category | Estimated Count |
|----------|----------------|
| Survival events | ~60 |
| Animal events | ~25 |
| Casino events | ~15 |
| Companion events | ~20 |
| Dark events | ~20 |
| Item events | ~30 |
| Number events | ~10 |
| People events | ~25 |
| Surreal events | ~15 |
| Wealth events | ~40 |
| Night events | ~65 |
| Illness events | ~80 |
| Car events | ~15 |
| **Total** | **~420+** |
