# Gameplay Fairness Changelog

> Tracks recent balance changes, new features, and fairness philosophy.

---

## Recent Changes

### New: Salvation (Healed) Ending ⭐
- **The best ending in the game** — requires 5+ Tanya therapy visits
- 20-year epilogue: reunion, kindergarten, little league, "Thanks for coming home, Dad"
- Automatic phone answer (no hesitation) because therapy healed you
- Tom's farewell, companion goodbye, drive home sequence

### New: Tanya Therapy System
- **5% daily spawn** after day 12 for Tanya's Number
- Repeatable therapy visits with meaningful dialogue
- 5+ visits unlock the Healed ending path
- Therapy is rewarded, not penalized

### Endings Expansion (5 → 9)
- **Added:** Salvation (Healed), Sanctuary, Exhaust, Madness
- **Refined:** Salvation, Resurrection, Destruction, Transcendence, Bliss
- Each ending has unique narrative, consequences, and tone
- Multiple paths encourage replayability

### Locations Expansion
- **Convenience store** inventory now scales by player rank
- **Marvin's** expanded to 18 items with edge score system
- **Tanya's Office** added as repeatable therapy location
- **Airport** added for Bliss ending ($1M+)
- **Adventures** expanded with new areas and encounters

### Economy Rebalance
- Wealth rank thresholds refined for smoother progression
- Marvin item prices balanced ($3k–$30k range)
- Edge score system creates meaningful blackjack progression
- Pawn prices categorized into low/mid/high tiers
- Loan shark interest compounds weekly (not daily)

### Storyline Chains
- 20+ multi-part storylines with numbered stages
- `force_start_day` mechanic prevents storylines from starting too early
- `min_gap` between stages prevents overwhelming the player
- Chain quests (Hermit, Radio, Junkyard, Dog) with crossover events

### Event Pool Architecture
- 6-tier weighted system by wealth rank
- One-time events deplete from pool after firing
- Night pools are per-rank with depletion
- Illness chains create meaningful medical gameplay
- 420+ total events across all categories

### Companion System
- 8 companions with unique abilities and personalities
- 4-tier happiness system (Bonded → Happy → Neutral → Sad)
- 24 unique dialogue lines per companion (6 per mood)
- Sanctuary ending rewards companion care
- Dark selling path as deliberate moral choice

### Night Event Overhaul
- Per-rank pools prevent repetition
- Depletion system ensures variety
- Sanity-gated events for low-sanity players
- Mechanic dream chains reveal story
- Dream progression ties to ending selection

---

## Balance Philosophy

| Principle | Implementation |
|-----------|---------------|
| **No gotcha moments** | Dangerous events have clear warnings |
| **Transparent danger** | Debt stages, illness chains are visible |
| **Rewards not traps** | Good choices lead to good outcomes |
| **Skill expression** | Edge score, bet sizing, item management |
| **Multiple valid paths** | 9 endings, no single "correct" route |
| **Comeback mechanics** | Loan system, item finding, companion buffs |
| **Escalating challenge** | Higher ranks = better rewards + harder events |

---

## Fairness Notes

### No Unfair Deaths
- Every lethal event has a prevention method or warning
- Illness chains give time to treat before escalation
- Debt has 6 escalation stages before violence
- Car breakdown has roadside mechanic (45% chance)

### Transparent Mechanics
- Marvin items show exact edge score bonus
- Shop prices are fixed (no hidden inflation)
- Storyline stages are sequential (no skipping)
- Companion happiness is visible

### Player Agency
- Most events offer meaningful choices
- Endings require deliberate setup
- Dark paths are clearly marked as dark
- Therapy is always beneficial (never a trap)

### Bot/Autoplay Fairness
- Edge score system rewards strategic item purchasing
- Bet sizing scales with bankroll and edge
- Loan strategy has defined optimal windows
- Achievement tracking provides clear milestones
