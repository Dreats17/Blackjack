# Blackjack Roguelike — Overview & Quick Start Guide

> **Last Updated:** March 5, 2026  
> **Version:** Current Build (Split Architecture)  
> **Total Codebase:** ~35,000+ lines across 18 source files

---

## Table of Contents

1. [What Is This Game?](#what-is-this-game)
2. [How to Play](#how-to-play)
3. [Your Goal](#your-goal)
4. [Game Loop Summary](#game-loop-summary)
5. [Controls & Text Speed](#controls--text-speed)
6. [Wealth Ranks](#wealth-ranks)
7. [Key Stats at a Glance](#key-stats-at-a-glance)
8. [Documentation Index](#documentation-index)
9. [Beginner Tips](#beginner-tips)

---

## What Is This Game?

**Blackjack Roguelike** is a terminal-based narrative RPG where you play as a down-on-your-luck drifter living out of your car, trying to gamble your way to **$1,000,000** at a shady casino run by a mysterious, one-eyed Dealer.

But this is far more than a card game. Between hands of Blackjack, you'll:

- **Survive** day-to-day life on the road — managing your health, sanity, and fatigue
- **Explore** locations — shops, mechanic garages, adventure areas, and mysterious encounters
- **Befriend** over 25 animal companions who ride along in your wagon
- **Collect** items, flasks (potions), and collectibles to sell or use
- **Navigate** 14 multi-part storylines with memorable NPCs
- **Manage** the Dealer's happiness — if he gets too angry, he *will* kill you
- **Discover** hundreds of random events ranging from absurdist comedy to genuine emotional depth
- **Choose** your path to one of 8+ major endings

The tone blends dark humor, emotional storytelling, and chaotic randomness. You might befriend a sentient duck army one day and have a heartbreaking phone call with your estranged wife the next.

---

## How to Play

### Starting the Game

Run `blackjackMain.py` to start. You'll go through an opening sequence, then the main game loop begins.

### Text Display

All text is displayed with a **typewriter effect** — characters appear one at a time for immersion. You can control the speed:

| Key | Effect |
|-----|--------|
| **Spacebar** | Skip to end of current text block instantly |
| **,** (comma) | Set typing speed to Default |
| **.** (period) | Set typing speed to Fast |
| **/** (slash) | Set typing speed to Fastest |
| **p** | Set typing speed to Print (instant) |

### Input

When the game asks you a question, type your answer and press **Enter**. Common inputs:

- **yes / no** (or **y / n**) for yes/no questions
- **Numbers** for betting amounts
- **hit / stand** (or **h / s**) during Blackjack hands
- **Option names** when given multiple choices (e.g., "peek", "double", "split", "surrender")

---

## Your Goal

**Reach $1,000,000.** That's the dream.

You start with **$50** and 3 rounds of Blackjack per day. Between sessions, you live your life — encountering events, visiting shops, and trying not to die.

But reaching a million isn't the only way the game ends. There are **8+ major endings** depending on your choices, relationships, and mental state.

---

## Game Loop Summary

Each in-game day follows this cycle:

```
┌─────────────────────────────────────┐
│          MORNING (Start Day)        │
│  • Wake up (sleep quality report)   │
│  • Daily system updates             │
│  • Companion status checks          │
│  • Loan shark escalation            │
│  • Random morning event OR          │
│    storyline event fires            │
├─────────────────────────────────────┤
│          AFTERNOON                  │
│  • Choose activity:                 │
│    - Visit a SHOP                   │
│    - Visit the DOCTOR               │
│    - Visit a MECHANIC               │
│    - Go on an ADVENTURE             │
│    - Rest at camp                   │
│    - Visit Vinnie (Loan Shark)      │
│    - Visit Gus (Pawn Shop)          │
├─────────────────────────────────────┤
│          EVENING (Blackjack)        │
│  • Drive to the casino              │
│  • Play 3 rounds of Blackjack       │
│    (4 with certain items)           │
│  • Dealer happiness shifts          │
│  • Gifts delivered if wrapped       │
├─────────────────────────────────────┤
│          NIGHT (End Day)            │
│  • Random night event fires         │
│  • Companion interactions           │
│  • Health/sanity updates            │
│  • Day counter increments           │
│  • Sleep                            │
└─────────────────────────────────────┘
```

---

## Wealth Ranks

Your wealth rank determines which events, shops, and content you can access. Almost everything in the game is tier-gated.

| Rank | Title | Balance Range | What Unlocks |
|------|-------|---------------|--------------|
| 0 | **Poor** | $0 – $999 | Basic survival events, Kyle's convenience store |
| 1 | **Cheap** | $1,000 – $9,999 | More events, mechanic access, companion events |
| 2 | **Modest** | $10,000 – $99,999 | Squirrelly companion chain, Phil interrogation, more shops |
| 3 | **Rich** | $100,000 – $499,999 | Victoria rivalry, Bruno bodyguard, Grimy Gus pawn shop |
| 4 | **Doughman** | $500,000 – $899,999 | GUNMAN event, Betsy the Cow, drastic events |
| 5 | **Nearly There** | $900,000 – $999,999 | Adventure areas, rabbit chase finale, Suzy finale |
| 6 | **Millionaire** | $1,000,000+ | WIN — Special morning visitor, airport ending |

> **Important:** Events are drawn from pools specific to your current rank. As you climb ranks, you unlock new content but also face more dangerous events.

---

## Key Stats at a Glance

| Stat | Range | What It Does |
|------|-------|--------------|
| **Balance ($)** | $0 – $1,000,000+ | Your money. Reach $0 = game over. Reach $1M = win. |
| **Health (HP)** | 0 – 100 | Physical well-being. At 0 = death. |
| **Sanity** | 0 – 100 | Mental stability. Low sanity = hallucinations, madness ending risk. |
| **Fatigue** | 0 – 100 | Exhaustion level. High fatigue = missed events, poor sleep. |
| **Dealer Happiness** | 0 – 100 | The Dealer's mood. Below 20 = danger. At 0 = he may kill you. |
| **Day Counter** | 1+ | Tracks how many days you've survived. |

---

## Documentation Index

This guide is split into multiple files for easy navigation:

| File | Contents |
|------|----------|
| **01 — Overview & Quick Start** *(this file)* | Game introduction, controls, basic mechanics |
| **[02 — Core Systems](02_CORE_SYSTEMS.md)** | Health, Sanity, Fatigue, Dealer Happiness, Wealth Ranks, Day/Night cycle |
| **[03 — Blackjack & Gambling](03_BLACKJACK_AND_GAMBLING.md)** | Rules, betting, special actions (peek/double/split/surrender), dealer mechanics |
| **[04 — Items, Flasks & Upgrades](04_ITEMS_FLASKS_AND_UPGRADES.md)** | All items, flask potions, upgrade paths, durability, food items |
| **[05 — Locations, Shops & NPCs](05_LOCATIONS_SHOPS_AND_NPCS.md)** | Every location, shop inventory, NPC descriptions, services |
| **[06 — Companions](06_COMPANIONS.md)** | All 25+ companions, befriending, feeding, happiness, bonding, betrayal path |
| **[07 — Events & Storylines](07_EVENTS_AND_STORYLINES.md)** | Random events, 14 multi-part storylines, event chains, secret triggers |
| **[08 — Endings & Achievements](08_ENDINGS_AND_ACHIEVEMENTS.md)** | All 8+ endings with unlock guides, 240+ achievements by category |
| **[09 — Secrets & Advanced Strategies](09_SECRETS_AND_ADVANCED_STRATEGIES.md)** | Hidden events, exact-balance triggers, optimal strategies, death avoidance |

---

## Beginner Tips

1. **Don't bet everything.** The minimum bet scales with your balance. Betting smart keeps you alive longer.
2. **Watch the Dealer's mood.** If you win too much, he gets angry. Below 20% happiness, you get a warning. At 0%, he may shoot you.
3. **Buy a Health Indicator early.** It tells you your exact HP — otherwise you're guessing.
4. **Feed your companions.** They lose 5 happiness per day if not fed. At 10 or below, they might run away.
5. **Save your money for Oswald.** You only get one chance at each mechanic. His item upgrades are expensive ($120k–$400k) but dramatically change gameplay.
6. **Visit Kyle's store often.** After 3–5 purchases, you unlock the gift-wrapping system to boost Dealer happiness.
7. **Don't ignore your sanity.** Below 25, you start seeing hallucinations. At 0, it's either madness (game over) or permanent "broken" state.
8. **Flasks are single-use but powerful.** "No Bust" prevents going over 21. "Second Chance" lets you replay a losing hand. Buy them from the Witch Doctor.
9. **Adventure areas are high risk, high reward.** Woodlands unlocked at rank 3. All are available at rank 5 ($900k+), they offer huge payouts but cost HP and fatigue.
10. **There is no "right" ending.** Explore different paths — the game has 8+ endings, each telling a different story about who you are.
