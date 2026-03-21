# 03 — Blackjack & Gambling Systems

> *"The house always wins — but the house hasn't met you yet."*

---

## Table of Contents

1. [The Dealer](#the-dealer)
2. [Basic Blackjack Rules](#basic-blackjack-rules)
3. [Marvin's Mystical Items](#marvins-mystical-items)
4. [Betting Strategy](#betting-strategy)
5. [Special Actions (Item-Dependent)](#special-actions-item-dependent)
6. [Gambling Psychology](#gambling-psychology)
7. [The Casino](#the-casino)
8. [Fraudulent Cash](#fraudulent-cash)

---

## The Dealer

A mysterious jade-eyed figure in a cowboy hat. Calm, composed, and unsettlingly knowing — the Dealer seems to understand more about you than he should.

### Backstory (Frank's Dream Chain)

- **Former life:** He was a teacher.
- **Tragedy:** His wife **Maria** and daughter **Sofia** were killed in a car accident.
- **Current existence:** He occupies a liminal space between life and death, dealing cards for eternity.

### Dealer Happiness System

| Action | Effect |
|---|---|
| Giving gifts | Increases happiness |
| Cash blending (clean play) | Neutral to slight positive |
| Fraudulent cash detection | Decreases happiness |
| Respectful player behavior | Increases happiness |
| Aggressive/reckless play | Decreases happiness |

Dealer happiness influences table atmosphere, dialogue tone, and can subtly affect game flow.

---

## Basic Blackjack Rules

### Card Values

| Card | Value |
|---|---|
| 2–10 | Face value |
| Jack, Queen, King | 10 |
| Ace | 1 or 11 (whichever benefits the hand) |

### Core Actions

- **Hit** — Draw another card.
- **Stand** — Keep your current hand; end your turn.

### Key Rules

- **Natural Blackjack** — 21 on first two cards. Pays **1.5× your bet**.
- **Dealer hits on soft 17** — Dealer must hit if hand totals 17 with Ace as 11.
- **Bust** — Exceed 21, you lose immediately.
- **Push** — Same total as Dealer, bet is returned.

---

## Marvin's Mystical Items

18 items that modify blackjack gameplay. **$3,000–$30,000** each, **40% stock chance** per visit.

### Item Catalog

| Item | Price | Effect |
|---|---|---|
| **Sneaky Peeky Shades** | $14,000 | Peek at the next card in the deck |
| **Pocket Watch** | $9,000 | Grants 4 extra rounds per session |
| **Gambler's Chalice** | $11,000 | Enhances the double down action |
| **Twin's Locket** | $14,000 | Enables splitting pairs |
| **White Feather** | $5,000 | Unlocks the surrender option |
| **Lucky Coin** | $4,000 | Losses can become pushes (ties) |
| **Worn Gloves** | $7,000 | Chance to redraw when you bust |
| **Tattered Cloak** | $8,000 | Dealer "forgets" your bet — free round |
| **Dirty Old Hat** | $9,000 | Reduces minimum bet requirement |
| **Faulty Insurance** | $4,000 | Cheaper doctor visits |
| *+ 8 additional items* | $3k–$30k | Unique effects (discovered in-game) |

### Edge Score System

Each item carries an **`edge_score`** weight (2–7 points). Combined edge score affects:

- **Bet sizing** — Higher edge allows more favorable calculations
- **Night earnings** — Items stack for increasingly profitable sessions
- **Guaranteed returns** — Enough items shift gambling from risky to reliably profitable

---

## Betting Strategy

### Bet Limits

| Factor | Rule |
|---|---|
| **Minimum bet** | Scales with player rank |
| **Maximum bet** | Limited by balance and game phase |
| **Floor protection** | At rank 2+, cannot bet below rank minimums |

### Phase-Based Strategy

| Phase | Approach | Notes |
|---|---|---|
| **Car Rush** | Conservative | Save money to purchase a car |
| **Growth Phases** | Aggressive | Push rank progression with item edge |
| **Millionaire Push** | High-risk | Large bets to break through to $1M |

---

## Special Actions (Item-Dependent)

### Peek — *Sneaky Peeky Shades*
See the next card before deciding to hit or stand. Extremely powerful.

### Double Down — *Gambler's Chalice*
Double your bet, receive exactly one more card. Best on 9, 10, 11 vs weak dealer upcard.

### Split — *Twin's Locket*
Split matching pairs into two separate hands. Always split Aces and 8s.

### Surrender — *White Feather*
Forfeit hand, recover half your bet. Optimal on hard 15–16 vs dealer 9/10/Ace.

### Insurance — *Dealer's Whispers Flask*
Side bet against dealer blackjack when dealer shows Ace. Situational.

---

## Gambling Psychology

### Streak Tracking

| Condition | Effect |
|---|---|
| **Winning streak** | Boosts confidence and sanity |
| **Losing streak** | Triggers desperation events; erodes sanity |

### Key Characters

- **Victoria** — Rival gambler at **$50,000+**
- **Veteran Gambler** — Warning at **$800,000+**: *"I've seen people lose it all."*

### Sanity & Gambling

- Low sanity causes **reality distortions** inside the casino
- Winning streaks restore sanity; losing streaks drain it
- The casino becomes increasingly surreal as sanity drops

---

## The Casino

- Open **every night**. The Dealer is always present.
- **Rain prevents casino visits.**

### Events & Easter Eggs

| Trigger | Event |
|---|---|
| Carrying a grandfather clock | Easter egg interaction with the Dealer |
| High rank progression | Casino owner meeting |
| Milestone achievement | **High Roller Keycard** earned |
| Continued high play | **VIP lounge invitations** |

### Low Sanity Effects

- Visual distortions (flickering lights, shifting shadows)
- Audio anomalies (distant laughter, muffled voices)
- Strange Dealer dialogue (breaking the fourth wall)

---

## Fraudulent Cash

Some events introduce **marked** or **fraudulent** currency into your wallet.

### How It Works

1. **Acquisition:** Certain events reward fraudulent cash mixed into your balance.
2. **Detection risk:** The Dealer can detect it during play.
3. **Blending:** Mix real cash with fraudulent cash to reduce detection.
4. **Consequences:** Caught = decreased Dealer happiness, trust damage, penalties.

### Blending Strategy

| Approach | Detection Risk |
|---|---|
| All fraudulent | Very high |
| High blend ratio (mostly real) | Low |
| Moderate blend | Medium |
| No blending (spend clean only) | None |

---

## Quick Reference: Item Priority by Phase

| Phase | Priority Items | Reason |
|---|---|---|
| **Early Game** | Lucky Coin, White Feather, Dirty Old Hat | Loss protection, surrender, lower minimums |
| **Car Rush** | Worn Gloves, Tattered Cloak | Bust protection, free rounds |
| **Growth** | Sneaky Peeky Shades, Gambler's Chalice, Twin's Locket | Peek, double down, split |
| **Millionaire Push** | Pocket Watch + full suite | Extra rounds + max edge score |
