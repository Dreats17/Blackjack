# Blackjack & Gambling Guide

> **Last Updated:** March 5, 2026

Everything about the card game at the heart of the experience.

---

## Table of Contents

1. [Basic Rules](#basic-rules)
2. [Card Values](#card-values)
3. [Betting](#betting)
4. [Standard Actions (Hit & Stand)](#standard-actions-hit--stand)
5. [Special Actions](#special-actions)
6. [Dealer Behavior](#dealer-behavior)
7. [Round Outcomes](#round-outcomes)
8. [Item Effects During Gambling](#item-effects-during-gambling)
9. [Flask Effects During Gambling](#flask-effects-during-gambling)
10. [Dealer Happiness & Gambling](#dealer-happiness--gambling)

---

## Basic Rules

You play standard Blackjack against the Dealer:

1. You and the Dealer are each dealt 2 cards.
2. Your goal: get as close to **21** as possible without going over.
3. The Dealer's second card is **face down** (unless they have 21).
4. You choose to **hit** (take another card) or **stand** (keep your hand).
5. After you stand, the Dealer reveals their hidden card and hits until reaching **17 or higher**.
6. Whoever is closest to 21 without going over wins.

### Per-Session Structure

Each gambling session (evening), you play a set number of rounds:
- **Default:** 3 rounds
- **With Pocket Watch:** 66% chance of 4 rounds (watch durability consumed)
- **With Golden Watch / Sapphire Watch:** Always 4 rounds
- **With Grandfather Clock:** Always 4 rounds (guaranteed)

---

## Card Values

| Card | Value |
|------|-------|
| 2–10 | Face value |
| Jack, Queen, King | 10 |
| Ace | 1 **or** 11 (whichever is better for the hand) |

**Ace Logic:** If counting the Ace as 11 would put you over 21, it counts as 1 instead. The game automatically tracks both possible hand values when you have an Ace.

---

## Betting

### Minimum Bets

The minimum bet is calculated from the first two digits of your balance:

| Balance Example | Min Bet |
|-----------------|---------|
| $50 | $5 |
| $250 | $25 |
| $2,500 | $250 |
| $25,000 | $2,500 |
| $250,000 | $25,000 |

**Reduction:** The **Dirty Old Hat** and **Unwashed Hair** items change the minimum to balance/4.

### Maximum Bet

Your maximum bet equals your total available funds (real balance + fraudulent cash).

### Betting Below Minimum

Betting below minimum **angers the Dealer**:
- Happiness ≥ 30: "The Dealer doesn't like that bet."
- Happiness ≥ 25: Aggressive eye contact
- Happiness ≥ 20: Infuriated response
- Happiness ≥ 15: Charges his revolver (warning)
- Happiness < 15: **Instant death** — three shots to the chest

Each rejected bet costs **−5 Dealer Happiness**.

### Fraudulent Cash Blending

If you have fraudulent cash (from Vinnie the Loan Shark):
- You can bet above your real balance
- The overflow is drawn from fraudulent cash
- Successfully completing the hand "launders" the fake money
- Display shows: "Blending $X fraudulent cash with $Y real money"

---

## Standard Actions (Hit & Stand)

### Hit (h)
- Draw one more card.
- If your hand exceeds 21, you **bust** and lose.
- You can keep hitting as long as you're under 21.

### Stand (s)
- Keep your current hand.
- The Dealer then plays their turn.
- If you have an Ace with two possible values, the game chooses the higher value (if ≤ 21).

---

## Special Actions

Special actions require specific items and are only available under certain conditions.

### Peek (p)
**Requires:** Sneaky Peeky Shades OR Sneaky Peeky Goggles

- See the **next card** on top of the deck before deciding to hit or stand.
- **One use per hand.**
- Consumes item durability.
- Sneaky Peeky Goggles (upgraded) has more durability.

### Double Down (d)
**Requires:** Gambler's Chalice OR Overflowing Goblet OR "Bonus Fortune" flask effect

- **Only available as your first action** (must have exactly 2 cards).
- Doubles your bet, then draws **exactly one more card** and forces you to stand.
- You must have enough balance to cover the doubled bet.
- High risk, high reward — perfect when you have a strong starting hand (9, 10, or 11).
- Consumes Gambler's Chalice durability (Overflowing Goblet has more).

### Split
**Requires:** Twin's Locket OR Mirror of Duality OR "Split Serum" flask effect

- **Only available as your first action** with a **pair** (two cards of equal value).
- Splits your pair into two separate hands.
- Each hand receives one additional card.
- You play the first hand normally, then the second.
- Consumes Twin's Locket durability (Mirror of Duality has more).

### Surrender (sur)
**Requires:** White Feather OR Phoenix Feather

- **Only available as your first action** (must have exactly 2 cards).
- Forfeit the hand and lose **half your bet** instead of the full amount.
- Useful when your starting hand is terrible against a strong dealer upcard.
- **Phoenix Feather bonus:** 25% chance to get your FULL bet back instead of losing half.
- Consumes White Feather durability (Phoenix Feather has more).

### Insurance
**Requires:** Dealer's Grudge OR Dealer's Mercy

- **Automatically offered** when the Dealer's first card is an **Ace**.
- Side bet costing **half your original bet**.
- If the Dealer has Blackjack, insurance pays **2:1** (you get back your insurance bet + double).
- If the Dealer doesn't have Blackjack, you lose the insurance bet.
- Consumes Dealer's Grudge durability.

---

## Dealer Behavior

### Dealer's Turn

After you stand, the Dealer plays:

1. Reveals their face-down second card.
2. **Must hit** on 16 or below.
3. **Must stand** on 17 or above (including soft 17 with Ace).
4. Continues hitting until reaching 17+ or busting.

### Dealer's Hesitation Flask

If you have an active **"Dealer's Hesitation"** flask effect:
- 66% chance to **force the Dealer to draw one extra card** when they would normally stand at 17–20.
- This can cause the Dealer to bust when they otherwise wouldn't.

---

## Round Outcomes

| Outcome | Result | Payout |
|---------|--------|--------|
| **Player Blackjack** | Natural 21 on first two cards | **3× bet** (bet returned + 2× winnings) |
| **Player Wins** | Higher hand than Dealer | **2× bet** (bet returned + 1× winnings) |
| **Dealer Bust** | Dealer exceeds 21 | **2× bet** (bet returned + 1× winnings) |
| **Dealer Blackjack** | Dealer's natural 21 | **Lose bet** |
| **Dealer Wins** | Dealer's hand is higher | **Lose bet** |
| **Player Bust** | You exceed 21 | **Lose bet** |
| **Tie (Push)** | Equal hand values | **Bet returned** (no gain, no loss) |
| **Tie Blackjack** | Both natural 21 | **Bet returned** |

### Free Hands

When the Dealer gives you a **free hand** (from high happiness), you bet nothing:
- Win: You gain the free bet amount.
- Lose: "Your balance is still $X." No loss.

---

## Item Effects During Gambling

These items passively affect gameplay during hands:

### Worn Gloves / Velvet Gloves
- **Trigger:** When a drawn card would cause you to bust.
- **Effect:** The bust card is discarded and a new card is drawn.
- **Chance:** Worn Gloves = 25% (1 in 4). Velvet Gloves = 50% (2 in 4).
- Consumes durability on activation.

### Lucky Coin / Lucky Medallion
- **Trigger:** When you would lose a hand (Dealer Wins, Dealer Blackjack, or Player Bust).
- **Effect:** The loss is converted to a **Push/Tie** — you keep your bet.
- **Chance:** Lucky Coin = 20% (1 in 5). Lucky Medallion = always triggers.
- Consumes durability on activation.

### Tattered Cloak / Invisible Cloak
- **Trigger:** When you lose a hand.
- **Effect:** The Dealer "forgets to collect your bet" — your bet is refunded.
- **Chance:** Tattered Cloak = 25%. Invisible Cloak = 50%.
- Consumes durability on activation.
- Stacks with Lucky Coin: Coin triggers first (turns loss to tie), then Cloak might refund anyway.

### Second Chance Flask
- **Trigger:** When you would lose a hand.
- **Effect:** You're asked if you want to **replay the hand entirely**.
- **Once per session** (resets each gambling day).
- Consumes flask durability on use.

### Pocket Aces Flask
- **Trigger:** At the start of a hand (first deal).
- **Effect:** Guarantees your **first card is an Ace** (an Ace is found in the deck and moved to the top).
- **One-time use** — the flask effect is removed after activation.

---

## Flask Effects During Gambling

| Flask | Effect | Duration |
|-------|--------|----------|
| **No Bust** | Prevents going over 21 (details vary) | 4 uses |
| **Pocket Aces** | First card guaranteed Ace | Single use |
| **Dealer's Hesitation** | 66% force dealer extra hit when at 17–20 | 4 uses |
| **Second Chance** | Replay one losing hand per session | 4 uses |
| **Bonus Fortune** | Grants Double Down ability (like Gambler's Chalice) | 4 uses |
| **Split Serum** | Grants Split ability (like Twin's Locket) | 4 uses |

> Flask effects are purchased from the **Witch Doctor** and have limited durability (typically 4 uses).

---

## Dealer Happiness & Gambling

Every hand outcome adjusts Dealer happiness. The magnitude depends on the **bet ratio** (your bet ÷ your balance):

### Player Wins (Dealer Gets Angrier)

| Bet Ratio | Blackjack | Normal Win | Dealer Bust |
|-----------|-----------|------------|-------------|
| ≥ 90% | −20 | −10 | −12 |
| ≥ 60% | −10 | −7 | −8 |
| ≥ 30% | −7 | −4 | −4 |
| < 30% | −5 | −2 | −2 |

### Player Loses (Dealer Calms Down)

| Bet Ratio | Dealer Blackjack | Dealer Wins | Player Bust |
|-----------|-----------------|-------------|-------------|
| ≥ 90% | +25 | +10 | +12 |
| ≥ 60% | +15 | +6 | +7 |
| ≥ 30% | +7 | +3 | +3 |
| < 30% | +5 | +2 | +2 |

### Ties

| Bet Ratio | Tie | Tie Blackjack |
|-----------|-----|---------------|
| ≥ 90% | −3 | −4 |
| ≥ 60% | −2 | −3 |
| ≥ 30% | −1 | −1 |
| < 30% | −1 | −1 |

> **Note:** A **rank modifier** (+0 at Poor to +5 at Nearly There) is added to anger values. Higher wealth = more Dealer resentment when you win.

### Strategy Tip

To manage Dealer happiness:
- Bet small percentages of your balance to minimize anger per win.
- Use the gift system to periodically boost happiness.
- Items like the Delight Indicator let you monitor his mood precisely.
- If he's getting angry, intentionally losing a hand or two can save your life.
