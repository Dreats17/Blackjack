# 01 — Overview & Quick Start

> A blackjack-based text adventure where you gamble your way from $50 to $1,000,000 — or die trying.

---

## What Is This Game?

You play as **Johnathan**, a man living in his car with nothing but $50 from Grandma and a desperate need to survive. The Casino — run by a mysterious jade-eyed Dealer — is your only path to a million dollars. But between the cards and the cash, you'll face illness, injury, loan sharks, surreal nightmares, animal companions, therapy sessions, and nine possible endings ranging from triumphant salvation to utter madness.

This is a **text-based survival RPG** built around a blackjack core loop, with deep systems for health, sanity, economy, companions, crafting, storylines, and multiple endings.

---

## How to Play

### Starting the Game

Run `blackjackMain.py` to start. The game begins with a short intro sequence, then enters the day/night loop.

### The Core Loop

```
NIGHT → Play blackjack at the Casino
  ↓
END OF DAY → Summary, healing, rank check
  ↓
MORNING → Events fire, companion bonuses apply
  ↓
AFTERNOON → Shop, craft, explore, visit NPCs
  ↓
(repeat)
```

### Your Goal

Reach **$1,000,000**. How you get there — and what you do when you arrive — determines your ending.

---

## Key Stats

| Stat | Range | Death At | Purpose |
|------|-------|----------|---------|
| **Health** | 0–100 | 0 | Physical condition. Damaged by illness, injury, events. |
| **Sanity** | 0–100 | — | Mental stability. Affects perception, dialogue, events. Below 30 triggers dark storylines. |
| **Fatigue** | 0–100 | — | Exhaustion. Too high = missed days. |
| **Balance** | $0+ | — | Your money. Determines rank and available content. |

---

## Rank System

Your balance determines your rank, which unlocks content:

| Rank | Title | Balance |
|------|-------|---------|
| 0 | Poor | $0–$999 |
| 1 | Cheap | $1,000–$9,999 |
| 2 | Modest | $10,000–$99,999 |
| 3 | Rich | $100,000–$399,999 |
| 4 | Doughman | $400,000–$749,999 |
| 5 | Nearly | $750,000+ |

---

## Quick Start Strategy

### Days 1–5: Survive
- Bet **$5–10** per hand. Don't risk big.
- Save **$50–100** to buy a car from Frank (cheapest mechanic).
- Take every free healing/sanity option offered.

### Days 5–10: Get Mobile
- **Buy a car** — this is the #1 priority. It unlocks all shops and locations.
- Buy the **Worn Map** ($8) — unlocks Marvin's shop and the Witch Doctor.

### Days 10–20: Invest
- Buy **Tool Kit** ($75) — unlocks crafting at the Car Workbench.
- Start visiting **Marvin** — his mystical items give you a real edge at blackjack.
- Watch for **Tanya's Number** (5% spawn after day 12) — needed for the best ending.

### Days 20+: Push for the Million
- Buy Marvin items: **Lucky Coin** ($4k) → **White Feather** ($5k) → **Sneaky Peeky Shades** ($14k)
- Use **loans strategically** when you have 2+ Marvin items (edge score ≥ 2).
- Keep health and sanity above safe levels — runs collapse from stat crises, not bad cards.
- Visit **Tanya 5+ times** for the best ending (Salvation: Healed).

---

## Key Locations

| Location | Unlock | Purpose |
|----------|--------|---------|
| The Casino | Always | Play blackjack |
| Convenience Store | Car | Buy supplies (rank-based inventory) |
| Doctor's Office | Car | Heal injuries ($75–$200) |
| Filthy Frank's | Meet Frank | Cheap car repairs (40% fail) |
| Trusty Tom's | Meet Tom | Reliable repairs ($150–$350) |
| Oswald's | Meet Oswald | Perfect repairs ($800–$900) |
| Marvin's | Worn Map | Buy blackjack-enhancing items |
| Witch Doctor | Map | Alternative healing + flasks |
| Vinnie's | Meet Vinnie | Emergency loans (20% weekly interest) |
| Grimy Gus's | Meet Gus | Pawn shop — sell items for cash |
| Tanya's Office | Tanya's Number | Therapy sessions → best ending |
| Car Workbench | Tool Kit | 50+ crafting recipes |
| Airport | $1,000,000 | Bliss ending — fly away |

---

## The 9 Endings

| # | Ending | Requirements | Tone |
|---|--------|-------------|------|
| 1 | **Salvation (Healed)** ⭐ | $1M + Tanya 5+ visits + Met Tom | Best ending — true healing |
| 2 | **Salvation** | $1M + Met Tom + Answer phone + Agree | Good — bittersweet reunion |
| 3 | **Resurrection** | $1M + Met Tom + Answer phone + Refuse | Hollow — you said no |
| 4 | **Destruction** | $1M + Befriend Frank | Dark — violence and crime |
| 5 | **Transcendence** | $1M + Befriend Oswald | Eerie — become the new Dealer |
| 6 | **Bliss** | $1M + Own car | Escapist — fly away forever |
| 7 | **Sanctuary** 🐾 | $1M + 5 companions + Animal Whistle | Secret — animal sanctuary |
| 8 | **Exhaust** | Low sanity + despair choices | Darkest ending |
| 9 | **Madness** | Sanity < 30 + shadow entity | Horrifying — mind breaks |

---

## Companions

8 animal companions provide passive bonuses:

| Companion | Type | Key Bonus |
|-----------|------|-----------|
| Squirrelly | Squirrel | +2 sanity, +1 luck |
| Whiskers | Alley Cat | +3 sanity, danger warning |
| Lucky | Three-Legged Dog | +5 sanity, physical protection |
| Mr. Pecks | Crow | +1 sanity, 5% money finding |
| Patches | Opossum | +2 sanity, night bonuses |
| Rusty | Raccoon | +2 sanity, 3% steal chance |
| Slick | Rat | +1 sanity, escape routes |
| Hopper | Rabbit | +2 sanity, +3 luck |

Feed them their favorite foods to keep happiness high. 5+ companions + Animal Whistle = secret Sanctuary ending.

---

## Important Items

| Item | Price | Why It Matters |
|------|-------|----------------|
| **Worn Map** | $8 | Unlocks Marvin and Witch Doctor |
| **Tool Kit** | $75 | Unlocks crafting |
| **Lucky Coin** | $4,000 | Converts losses to pushes (Marvin) |
| **Sneaky Peeky Shades** | $14,000 | See the next card (Marvin) |
| **Spare Tire** | $50 | Prevents flat tire events |
| **Bug Spray** | $15 | Prevents mosquito swarms |
| **Tanya's Number** | Event | 5% spawn after day 12 → best ending |

---

## Things to Avoid

| Trap | Why |
|------|-----|
| **Necronomicon** ($666) | Cursed — drains sanity, causes bad luck |
| **Cursed Coin** ($13) | Deceptively cheap, causes bad luck |
| **Devil's Bargain** | +$10–50k but −25 sanity |
| **Ignoring health/sanity** | Stat crises kill more runs than bad cards |
| **Ignoring Tanya** | Miss the best ending in the game |

---

## Documentation Index

| Doc | Contents |
|-----|---------|
| [02 — Core Systems](02_CORE_SYSTEMS.md) | Day/night cycle, health, sanity, fatigue, ranks, economy, durability |
| [03 — Blackjack & Gambling](03_BLACKJACK_AND_GAMBLING.md) | Dealer, blackjack rules, Marvin items, betting, special actions |
| [04 — Items, Flasks & Upgrades](04_ITEMS_FLASKS_AND_UPGRADES.md) | All items, crafting, pawn prices, flasks |
| [05 — Locations, Shops & NPCs](05_LOCATIONS_SHOPS_AND_NPCS.md) | Every location, shop, and character |
| [06 — Companions](06_COMPANIONS.md) | All 8 companions, feeding, happiness, bonuses |
| [07 — Events & Storylines](07_EVENTS_AND_STORYLINES.md) | Event system, storylines, quest chains |
| [08 — Endings & Achievements](08_ENDINGS_AND_ACHIEVEMENTS.md) | All 9 endings, 500+ achievements |
| [09 — Secrets & Advanced Strategies](09_SECRETS_AND_ADVANCED_STRATEGIES.md) | Hidden mechanics, optimal paths, traps |
| [10 — All Events Reference](10_ALL_EVENTS_REFERENCE.md) | Complete event catalog |
| [10 — Gameplay Fairness Changelog](10_GAMEPLAY_FAIRNESS_CHANGELOG.md) | Balance changes and fairness notes |
