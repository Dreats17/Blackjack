# 02 — Core Game Systems

This document provides comprehensive coverage of all core systems that govern gameplay in the Blackjack text adventure.

---

## Table of Contents

1. [Day/Night Cycle](#daynight-cycle)
2. [Health System](#health-system)
3. [Sanity System](#sanity-system)
4. [Fatigue System](#fatigue-system)
5. [Rank/Progression System](#rankprogression-system)
6. [Injury/Status System](#injurystatus-system)
7. [Economy System](#economy-system)
8. [Durability System](#durability-system)
9. [Achievement System](#achievement-system)
10. [Bankroll Emergency & Recovery Modes](#bankroll-emergency--recovery-modes)

---

## Day/Night Cycle

The game operates on a structured day/night loop. Each "day" progresses through distinct phases that determine what activities, events, and mechanics are available.

### Night Phase — Casino

- The core gameplay loop: Blackjack at the Casino with the Dealer
- All blackjack hands, side bets, and dealer interactions occur during night

### `end_day()` — End of Day

- Displays a day summary (hands played, money won/lost)
- Applies balance changes from the day's activity
- Shows a rank comment reflecting current financial standing
- Heals the player **1–5 HP** passively (natural overnight recovery)

### `start_day()` — Morning Setup

- Initializes the new day's state
- Dispatches morning events (random encounters, story triggers)
- Applies **companion bonuses** (passive healing, sanity restoration, item effects)
- Runs **fatigue checks** — if fatigue is too high, the player may be forced to rest or miss activities

### `afternoon()` — Daytime Activities

Daytime is the open exploration phase. Available activities include:

- **Shopping** — Visit stores, buy items and supplies
- **Crafting** — Combine or use items at workbenches
- **Exploring** — Discover new locations, trigger adventure events
- **Visiting NPCs** — Interact with story characters, advance questlines

### Dream System

- **30% chance** each night a dream fires, replacing the normal day summary
- Dreams are **tied to wealth tiers** — different financial brackets unlock different dream content
- Dreams also reflect **mechanic progression** (storyline advancement, companion status, sanity level)
- Dreams can foreshadow events, provide lore, or affect sanity

---

## Health System

Health represents the player's physical condition and is a core survival metric.

### Scale

- **0–100 HP** range
- Health **0 = death** (game over)

### Damage Sources

- **Injuries** add damage over time (ongoing HP drain each day)
- **Status effects** (Cold, Flu, Spider Bite, etc.) drain health at varying rates
- Certain events and encounters deal direct damage

### Healing & Recovery

| Method | Details |
|---|---|
| **Overnight rest** | Heals 1–5 HP passively via `end_day()` |
| **Doctor's Office** | Professional healing for **$75–$200** |
| **Witch Doctor** | Alternative healer; **requires the Map item** to access |
| **First Aid Kit** | Reduces ongoing injury damage (doesn't cure, mitigates) |
| **Companion bonuses** | Certain companions provide passive healing each day |

### Critical Thresholds

- **Health < 50** — Triggers critical events (urgent warnings, special encounters, NPC reactions)
- **Health = 0** — Death; the game ends

---

## Sanity System

Sanity tracks the player's mental stability, affecting perception, dialogue, and story branching.

### Scale

- **0–100** range

### Sanity Drains

- **Casino play** — Extended gambling sessions reduce sanity
- **Strange events** — Supernatural or disturbing encounters drain sanity
- Certain items, choices, and storylines cost sanity

### Sanity Thresholds

| Threshold | Effect |
|---|---|
| **< 50** | Low sanity — **warps casino perception** (distorted descriptions, unreliable narration) |
| **< 30** | Very low sanity — Triggers the **Bridge Angel storyline** |
| **Critical** | "Broken state" — Descriptions are fundamentally altered, dialogue options change |

### Sanity Recovery

- **Companions** restore sanity (passive daily bonus)
- **Sleep/rest** restores small amounts
- **Certain items** provide sanity bonuses

---

## Fatigue System

Fatigue represents exhaustion from activity. It gates player actions and can cause missed days.

### Fatigue Sources

- Playing too many hands at the casino
- Going on adventures
- Certain events and encounters

### Fatigue Effects

- **High fatigue blocks events** — the player may miss entire days of activity
- **Fatigue ≥ 88** — Triggers **emergency warnings** (collapse risk, forced rest)

### Fatigue Recovery

- **Rest at home** reduces fatigue
- **Certain items** reduce fatigue gain rate

---

## Rank/Progression System

The player's rank is determined by their current balance and gates access to content throughout the game.

### Rank Tiers

| Rank | Title | Balance Range |
|---|---|---|
| 0 | **Poor** | $0 – $999 |
| 1 | **Cheap** | $1,000 – $9,999 |
| 2 | **Modest** | $10,000 – $99,999 |
| 3 | **Rich** | $100,000 – $399,999 |
| 4 | **Doughman** | $400,000 – $749,999 |
| 5 | **Nearly** | $750,000+ |

### Rank Mechanics

- Each rank **unlocks**: new events, shop items, storylines, and dialogue options
- **Rank regression is possible** — if the player's balance drops below a tier threshold, they lose access to that rank's content
- Rank is recalculated dynamically based on current balance

---

## Injury/Status System

A deep illness and injury model with tiered severity and infection chains.

### Illness Pool

- **80+ illnesses** across three severity tiers: **Minor**, **Moderate**, **Severe**

### Infection Chains

Untreated conditions can escalate through infection chains:

- Dirty needle → Blood disease
- Food poisoning → Dehydration
- Rat bite → Fever
- Cold → Flu → Pneumonia

### Status Effects

- **Physical:** Cold, Flu, Pneumonia, Spider Bite
- **Beneficial:** Lucky, Blood Moon Luck
- **Dark:** Devil's Bargain
- **Mental (Severe):** PTSD, Insomnia, Depression

### Persistence

- Injuries and statuses **persist until treated** (they do not expire on their own)
- Treatment options: Doctor's Office, Witch Doctor, specific items

---

## Economy System

The economy governs all money flow — earning, spending, debt, and special financial mechanics.

### Starting Conditions

- **Starting balance: $50** (Grandma's gift)

### Income Sources

| Source | Type |
|---|---|
| **Blackjack winnings** | Primary income |
| Found money | Secondary |
| Adventure rewards | Secondary |
| Gifts from NPCs | Secondary |
| Selling at pawn shop | Secondary |

### Expenses

- **Car repairs** (maintenance and breakdown costs)
- **Shop purchases** (items, supplies, equipment)
- **Doctor bills** ($75–$200 per visit)
- **Loan repayment** (Vinnie's principal + interest)

### Loan Shark — Vinnie

- Vinnie offers loans when the player is desperate
- **20% weekly interest** on outstanding debt
- **Escalating collection** — missed payments trigger increasingly threatening encounters

### Pawn Shop — Grimy Gus

- Sell items at set prices
- **70+ items** with defined pawn values

### Fraudulent Cash Mechanic

- **Marked money** can enter the player's possession through certain events
- Dealers **can detect** fraudulent cash — getting caught has consequences

---

## Durability System

Special items degrade with use, adding a maintenance layer to inventory management.

### Core Mechanics

- **Special items have durability** — a hidden or visible wear counter
- Items **can break** from use or as a result of events
- **Broken items stop providing bonuses** until repaired

### Repair Options

| Method | Requirements |
|---|---|
| **Car Workbench** | Requires the **Tool Kit** item |
| **Super Glue** | Fixes select items |
| **Duct Tape** | Fixes select items |
| **Oswald's Optimal Outoparts** | Shop that sells upgrade parts and repair materials |

---

## Achievement System

A massive achievement tracker rewarding exploration, survival, and both light and dark playstyles.

### Scale

- **500+ achievements** across multiple rarity tiers

### Achievement Tiers

| Tier | Description |
|---|---|
| **Common** | Basic milestones most players will hit |
| **Uncommon** | Requires moderate exploration or skill |
| **Rare** | Harder to reach goals |
| **Epic** | Significant accomplishments |
| **Legendary** | Extreme feats |
| **Secret / Dark** | Hidden achievements tied to dark or obscure paths |

### Special Achievement Chains

- **Companion selling** → dark factory ending chain
- **Dealer happiness path** — keeping the dealer's mood/relationship high
- **Suicide metrics** — tracking despair-related outcomes (Bridge Angel, sanity collapse)

---

## Bankroll Emergency & Recovery Modes

Two special financial states that alter gameplay when the player is in economic crisis.

### Bankroll Emergency Mode

- **Triggered when:** Balance is critically low **and** the player owns a car
- Alters **betting strategy**, restricts event availability, may trigger emergency-only events

### Fragile Post-Car Recovery Mode

- **Triggered when:** The player has just acquired or recovered their car
- Conservative **betting adjustments**, modified event pool
- Gradually eases restrictions as balance stabilizes
