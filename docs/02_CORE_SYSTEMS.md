# Core Systems Guide

> **Last Updated:** March 5, 2026

This document covers every core system that governs your survival and progression.

---

## Table of Contents

1. [Health System](#health-system)
2. [Sanity System](#sanity-system)
3. [Fatigue & Sleep](#fatigue--sleep)
4. [Dealer Happiness](#dealer-happiness)
5. [Wealth Ranks & Economy](#wealth-ranks--economy)
6. [Day/Night Cycle](#daynight-cycle)
7. [Gambling Stats & Grimoire](#gambling-stats--grimoire)
8. [Statistics Tracking](#statistics-tracking)
9. [Status Effects, Injuries & Illnesses](#status-effects-injuries--illnesses)
10. [Dangers & Event Chains](#dangers--event-chains)

---

## Health System

### Overview

- **Range:** 0 – 100 HP
- **Starting Value:** 100
- **At 0 HP:** You die.

### Taking Damage

Damage comes from events, combat, illnesses, injuries, the loan shark, the Dealer, weather, poisoning, explosions, and animal attacks.

**Damage Reduction:**
- **First Aid Kit:** If you take 15+ damage and own a First Aid Kit, it's consumed to cut the damage in half.
- **LifeAlert:** If damage would kill you, LifeAlert activates — you survive at 25 HP (consumed on use).

### Healing Sources

| Source | Amount | Notes |
|--------|--------|-------|
| Doctor's Office | Full heal to 100 | Costs 65–90% of balance |
| Real Insurance (item) | Full heal, free | Upgraded from Faulty Insurance |
| Faulty Insurance (item) | Full heal, 10–35% cost | 10% chance of being banned |
| Food items | 3–15 HP | Varies by food type |
| End-of-day passive | +1/3/5 HP | Small automatic recovery |
| Events | Variable | Peaceful events, kind strangers |
| Witch Doctor | 50% chance to clear one status | Also sells flasks |

### Health Indicator Items

- **Health Indicator** (base): Shows your exact HP with color coding when you take damage or heal. Updates on durability use.
- **Health Manipulator** (upgraded): Same functionality with enhanced messaging and extended durability.

---

## Sanity System

### Overview

- **Range:** 0 – 100
- **Starting Value:** 100
- **Visible Stat:** Shown at start of day when below 75.

### Sanity Thresholds

| Threshold | Effect |
|-----------|--------|
| **100–76** | Clear-headed. No effects. |
| **75** | Warning: "Your mind feels... foggy." |
| **50** | Warning: "The edges of your vision blur. Reality feels thin." |
| **25** | Warning: "Your thoughts are fracturing. The shadows are getting closer." |
| **Below 25** | Hallucination effects start appearing during gameplay. |
| **0** | **Critical:** 40% chance = Madness Ending (game over). 60% chance = "Broken" state. |

### The Broken State

If you survive sanity hitting 0 (60% chance), you enter a **permanent Broken state**:

- Sanity is locked at 0 and cannot recover.
- **15 unique hallucination effects** randomly fire during gameplay:
  - "The furniture is talking again. It's saying reasonable things. That's what worries you."
  - "The Dealer has too many hands. Count them. One. Two. One. Just one."
  - "You can hear your heartbeat in the cards. Thump. Thump. Hit. Stand. Thump."
  - "Gravity reversed for a moment. Nobody else noticed."
  - "The shadows have names now. You know them all."
  - And 10 more...
- Broken state effects appear at start of each gambling session.
- Sleep quality is permanently worse (−8 to −15 recovery).

### Sanity Loss Sources

| Source | Amount | Notes |
|--------|--------|-------|
| Gambling losses | −1 to −3 | Scales with bet size |
| Witnessing violence | −5 to −15 | Combat events, deaths |
| Loan shark visits | −5 to −15 | Escalates with warning level |
| Existential events | −3 to −10 | Dark philosophical encounters |
| Devil's Bargain | −10+ | Supernatural deal |
| Necronomicon (item) | −1 to −3/day | 20% daily chance while owned |
| Loneliness | −1 to −5 | Events when isolated |
| Companion death/loss | −5 to −10 | Losing a bonded companion is worse |

### Sanity Restoration

| Source | Amount | Notes |
|--------|--------|-------|
| Companions (daily) | +2 to +5 | Alive companions passively restore |
| Suzy's Gift (item) | +1/day | 33% daily chance |
| Peaceful events | +3 to +15 | "Rain on the Roof" = +15 |
| Doctor's Office | +1 to +3 | Small bonus with full heal |
| Kind stranger events | +5 to +10 | Variable |
| Storyline completions | +5 to +15 | Major story beats |
| Sleep (good quality) | Indirect | Better sleep = less sanity drain |
| Crossing above 50 | Message | "A sense of clarity washes over you." |

### Gambling & Sanity

Low sanity imposes a **gambling modifier**:

| Sanity Range | Modifier | Effect |
|--------------|----------|--------|
| 76–100 | 0 | No penalty |
| 51–75 | 1 | Slight disadvantage |
| 26–50 | 2 | Noticeable disadvantage |
| 0–25 | 3 | Severe disadvantage |

### Madness Confrontation

At sanity ≤40, there's a scaling chance each day for a **madness confrontation** event. This is a one-time event where you face your deteriorating mental state. Surviving it sets the `faced_madness` flag and prevents it from triggering again.

---

## Fatigue & Sleep

### Overview

- **Range:** 0 (well-rested) – 100 (exhausted)
- **Starting Value:** 0
- **Source of Gain:** Adventures add 5–22 fatigue each.

### Fatigue Effects

When fatigue is very high, positive day events can be **blocked** — you're too tired to participate.

| Fatigue Level | Block Chance |
|---------------|-------------|
| 0–74 | 0% (never blocked) |
| 75–84 | 10% |
| 85–94 | 20% |
| 95–100 | 35% |

**Mitigation:**
- **Running Shoes** (item): Passively prevents fatigue blocking entirely.
- **Energy Drink** (consumable): If fatigue would block an event and you have one, it's auto-consumed (−25 fatigue) and the event proceeds.

### Sleep Quality

At the start of each day, sleep is "processed." Recovery depends on conditions:

| Factor | Effect |
|--------|--------|
| Base recovery | 35–50 fatigue reduction |
| Per alive companion | +3 each (max +12) |
| Currently sick | −3 to −8 |
| Currently injured | −2 to −6 |
| Sanity ≤ 25 | −5 to −12 |
| Sanity ≤ 50 | −3 to −7 |
| Broken state | −8 to −15 |
| Minimum recovery | Always at least 10 |

**Sleep Quality Tiers** (7 tiers × 20 unique texts = 140 descriptions):

| Tier | Fatigue After Sleep | Example Text |
|------|-------------------|--------------|
| Refreshed | 0–10 | "You slept like a baby. A baby who doesn't gamble." |
| Well Rested | 11–25 | "Decent night. You feel human." |
| Decent | 26–40 | "Could've been worse. Could've been better." |
| Restless | 41–55 | "Tossed and turned. Dreams of losing." |
| Poor | 56–70 | "Barely slept. The seat doesn't recline far enough." |
| Terrible | 71–85 | "Your back is ruined. Your neck is a war crime." |
| Wrecked | 86–100 | "You didn't sleep. You suffered horizontally." |

---

## Dealer Happiness

### Overview

- **Range:** 0 – 100
- **Starting Value:** 45
- **Daily Reset:** +5/7/10 (random) at start of each gambling session, unless you've given him too much fake cash.

The Dealer is the gatekeeper of your income. His mood determines whether he gives you free hands, ignores you, warns you, or **kills you**.

### Happiness Tiers

| Range | Behavior |
|-------|----------|
| **100** | 33% chance of a free hand (bet size: balance/18 to balance/8) |
| **96–99** | 10% chance of a free hand |
| **91–95** | 10% chance of a smaller free hand |
| **31–90** | Normal behavior |
| **21–30** | Warning: "The Dealer is visibly pissed." |
| **10–19** | Increasing violence threats |
| **5–9** | 20% chance of death or ejection per hand |
| **1–4** | 40% chance of death or ejection |
| **0** | 50% chance of **instant death** (shot), 50% ejection |

### What Affects Dealer Happiness

**Decreases (you angering him):**
- Winning hands (especially with large bets)
- Player Blackjack = highest anger
- Betting below minimum (−5 per offense)
- Having too much fraudulent cash in the system
- Giving bad gifts

**Increases (him calming down):**
- Losing hands
- Ties (slight calm)
- Daily session reset (+5/7/10)
- Good gifts (wrapped items delivered at casino)
- Delight Manipulator item (passive calming)

### Anger Scaling by Bet Ratio

The Dealer gets angrier when you bet a large portion of your balance and win:

| Bet Ratio (bet/balance) | Player Blackjack Anger | Player Win Anger |
|--------------------------|----------------------|-----------------|
| ≥ 90% | −20 | −10 |
| ≥ 60% | −10 | −7 |
| ≥ 30% | −7 | −4 |
| < 30% | −5 | −2 |

A **rank modifier** (+0 to +5 based on wealth rank) is added to anger values. Richer players anger the Dealer more.

### Monitoring Happiness

- **Delight Indicator** (item): Shows exact happiness % with color coding (green/yellow/red). Messages appear when happiness changes.
- **Delight Manipulator** (upgraded): Same with enhanced messaging and extended durability.

### Gift System

After 3–5 purchases at Kyle's Convenience Store (rank ≥ 1):
1. **Gift wrapping unlocks** ($10 per wrap)
2. Wrap any inventory item
3. Item is automatically delivered to the Dealer at the start of your next casino session
4. Each item has a **unique reaction** with dialogue and happiness modifier (−50 to +30)
5. **WARNING:** Some gifts are **lethal** — Dealer's Grudge (−40, kills you), Stolen Watch (−50, kills you)

---

## Wealth Ranks & Economy

### Rank Breakdown

| Rank | Title | Range | Key Unlocks |
|------|-------|-------|-------------|
| 0 | Poor | $0 – $999 | Basic events, Kyle's store |
| 1 | Cheap | $1,000 – $9,999 | Mechanic access, companion events, more shops |
| 2 | Modest | $10,000 – $99,999 | Squirrelly chain, Phil interrogation, expanded shops |
| 3 | Rich | $100,000 – $499,999 | Victoria, Bruno, Grimy Gus, Marvin's |
| 4 | Doughman | $500,000 – $899,999 | GUNMAN, Betsy's Cow Army, drastic events |
| 5 | Nearly There | $900,000 – $999,999 | Adventures, rabbit finale, Suzy finale |
| 6 | Millionaire | $1,000,000+ | WIN — morning visitor, airport |

### Minimum Bets

The minimum bet scales with your balance. It's calculated from the first two digits of your balance:

| Balance | Minimum Bet |
|---------|------------|
| $1–$9 | $1 |
| $50 | $5 |
| $500 | $50 |
| $5,000 | $500 |
| $50,000 | $5,000 |
| $500,000 | $50,000 |

**Reduction items:**
- **Dirty Old Hat** / **Unwashed Hair**: Minimum bet set to balance/4 instead.

### Fraudulent Cash

From Vinnie the Loan Shark, you can receive **fraudulent cash** — fake money that must be "blended" through gambling:
- When you bet more than your real balance, the shortfall is pulled from fraudulent cash.
- Successfully blended cash becomes real.
- **Warning:** If the Dealer accumulates too much fake cash, he stops gaining daily happiness and becomes suspicious.

---

## Day/Night Cycle

### Morning (start_day)

1. Day banner displayed
2. Daily companion updates (happiness decay, runaway checks)
3. Loan shark interest and warning level escalation
4. Achievement checks
5. Passive item effects (Suzy's Gift, Necronomicon, Cursed Coin)
6. Broken state effects (if applicable)
7. Sleep quality processed and displayed
8. **Millionaire check:** If you hit $1M, a special morning visitor arrives
9. **Storyline check:** Sequential storyline events take priority (max 1 per day)
10. If no storyline fires, a random day event occurs

### Afternoon

Player chooses from available activities (shops, doctor, mechanic, adventures, rest, loan shark, pawn shop).

### Evening (Blackjack)

3 rounds of Blackjack (4 with watch items). Dealer happiness effects, gift delivery, balance updates.

### Night (end_day)

Random night event fires, companion feeding/interaction, health/sanity updates, day counter increments.

---

## Gambling Stats & Grimoire

### Tracked Statistics

The game tracks detailed gambling stats:

| Stat | Description |
|------|-------------|
| total_hands | Total hands played |
| wins | Total wins |
| losses | Total losses |
| blackjacks | Natural 21s hit |
| busts | Times you busted (>21) |
| ties | Push outcomes |
| biggest_win | Largest single hand payout |
| biggest_loss | Largest single hand loss |
| current_streak | Current win/loss streak |
| best_win_streak | Longest winning streak ever |
| worst_loss_streak | Longest losing streak ever |
| total_won | Total money won gambling |
| total_lost | Total money lost gambling |
| double_downs_won | Successful double downs |
| splits_won | Successful split wins |
| surrenders_used | Times surrendered |
| insurance_collected | Insurance payouts received |

### Gambler's Grimoire / Oracle's Tome

- **Gambler's Grimoire** (item): Displays all gambling stats when checked.
- **Oracle's Tome** (upgraded): Enhanced stat display with predictions and advice.

---

## Statistics Tracking

Beyond gambling, the game tracks broad lifetime statistics:

| Category | What's Tracked |
|----------|---------------|
| days_survived | Total days alive |
| total_money_earned | All income |
| total_money_spent | All expenditures |
| highest_balance | Peak wealth |
| lowest_balance | Deepest poverty |
| items_collected | Unique items acquired |
| items_sold | Items sold at pawn shop |
| events_experienced | Total events triggered |
| people_met | Unique NPCs encountered |
| injuries_sustained | Total injuries |
| illnesses_contracted | Total illnesses |
| near_death_experiences | Times barely surviving |
| companions_befriended | Total companions gained |
| loans_taken | Loan shark loans |
| loans_repaid | Debts fully paid |
| times_robbed | Times you were robbed |
| times_hospitalized | Hospital visits |
| mechanic_visits | Garage visits |
| doctor_visits | Doctor trips |
| casino_visits | Casino sessions |
| pawn_shop_visits | Gus visits |

---

## Status Effects, Injuries & Illnesses

### Illnesses (18 Types)

Your character can contract various illnesses from events:

| Illness | Common Sources |
|---------|---------------|
| Cold | Weather, homeless shelter |
| Flu | Close contact, public areas |
| Fever | Infection complications |
| Pneumonia | Untreated cold, weakened immune |
| Bronchitis | Air exposure, smoking |
| Stomach Flu | Bad food, contaminated water |
| Food Poisoning | Hot dogs, bad oysters, food trucks |
| Infection | Wounds, dirty needle, rat bite |
| Measles | Rare outbreak events |
| Chickenpox | Contact events |
| Mono | Social events |
| Strep Throat | Poor tier medical events |
| Sinus Infection | Poor tier medical events |
| Ear Infection | Swimming, poor hygiene |
| Pink Eye | Public pool, contact |
| Lyme Disease | Tick bite events |
| Tetanus | Rusty metal injury |
| Malaria | Rare swamp events |

### Injuries (30+ Types)

| Category | Examples |
|----------|---------|
| Fractures | Broken Arm, Leg, Ribs, Nose, Wrist, Ankle, Hand |
| Sprains | Sprained Ankle, Sprained Wrist |
| Dislocations | Dislocated Shoulder, Separated Shoulder |
| Trauma | Concussion, Whiplash, Torn ACL, Fractured Spine |
| Surface | Deep Cut, Burns (2nd degree), Frostbite, Black Eye |
| Chronic | Pulled Muscle, Bruised Tailbone, Jammed Finger |

### Mental Health Conditions (5 Types)

| Condition | Effects |
|-----------|---------|
| Anxiety | Increased sanity drain from events |
| Depression | Reduced sanity recovery |
| PTSD | Trauma flashbacks trigger additional sanity loss |
| Insomnia | Worse sleep quality, 3 AM epiphany events |
| Paranoia | More danger events, suspicion dialogue |

---

## Dangers & Event Chains

"Dangers" are flags set by events that trigger follow-up events later. They create branching narrative chains:

| Initial Event | Danger Flag | Follow-Up Events |
|--------------|------------|-----------------|
| Spider Bite | Spider | Bite complications, infestation |
| Cockroach | Cockroach | Infestation escalation |
| Rat Encounter | Rat | Rat colony growth |
| Knife Wound | Knife Wound | Infection (20% death) |
| Gut Wound | Gut Wound | Complications (40% death) |
| Dog Bite | Dog Bite | Rabies scare (20% positive) |
| Fuel Leak | Fuel Leak | Car fire OR mechanic fix ($150) |
| Heart Condition | Heart Condition | Flare-ups (10% death per event) |
| Damaged Exhaust | Damaged Exhaust | Carbon monoxide (10% death) |
| Shoulder Injury | Shoulder Destroyed | Pain → Painkiller → Dependency → Withdrawal → Overdose (30% death) |
| Drug Dealer | Cocaine | Temptation → Crash → Heart Attack (40% death) |
| Burn Injury | Burn Scars | Stares, infection (20% death) |
| Weakened Immune | Weakened Immune | Cold → Pneumonia (30% death) |
| ATM Theft | ATM Theft | Police ($200 fine / jail / prison) |
| Unpaid Tickets | Unpaid Tickets | Boot on car → Impound |
| Stray Cat | Stray Cat chain | Sick → Dies or Saved → Has Kittens |
| Bridge Encounter | Bridge Angel | Returns → Phone number → Call for support (+30 sanity) |
| Devil's Bargain | Soulless | Emptiness → Mirror → Recognition (no shadow) |
| Angry Dealer | Angry Dealer | Kicked out of casino for the session |

> **Key Insight:** Many "dangers" create escalating consequence chains. A small event today can become a life-threatening situation days later. Pay attention to warnings.
