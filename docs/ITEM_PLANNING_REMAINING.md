# Item Planning Remaining Work

> This document replaces the stale assumption that most of ITEM_PLANNING is still greenfield.
> It tracks only what is still required to reach practical 100% coverage of the original item planning goals.

---

## Purpose

Use this document as the execution source of truth for remaining item work.

- Do not re-implement recipe, hint, description, or craft-text systems that already exist in `lists.py` and `story/locations.py`.
- Do not treat early audit sections in `ITEM_PLANNING.md` as factual without checking code.
- Prefer additive event hooks first.
- Delay new stateful systems until additive coverage is stable.
- When implementing event hooks, dialogue may be copied directly from `ITEM_PLANNING.md` draft narrative blocks and only lightly adapted for branch context, pacing, or durability/consumption outcomes.

---

## Definition Of Done

We consider ITEM_PLANNING effectively complete when all of the following are true:

1. Every still-missing item family has meaningful event presence across appropriate files.
2. Existing crafted tiers have enough world hooks that they feel systemic, not recipe-only.
3. High-value systemic proposals that remain in scope are either implemented or explicitly cut.
4. `docs/ITEM_PLANNING.md` can be re-labeled as historical planning and no longer drives execution.
5. This remaining-work document is empty or reduced to deliberate stretch goals.

---

## Acceptance Criteria

The execution waves in this file are category-level planning. Final completion should be judged against per-item acceptance rules.

### Coverage Minimums

- Base Marvin item: at least 3 meaningful non-table triggers, unless the item is intentionally table-focused.
- Marvin upgrade: at least 1 distinct upgrade-only trigger or variant beyond the base version.
- Flask: at least 2 non-casino narrative triggers for flasks that logically apply outside blackjack.
- Tier 1 crafted item: at least 2 event families outside `events_day_items.py`.
- Tier 2 crafted item: at least 2 meaningful non-crafting world hooks.
- Tier 3 or Tier 4 crafted item: at least 2 memorable high-value hooks outside recipe text, inspect text, and pawn value.
- Convenience-store item with gameplay identity: at least 1 clear world-facing use, and 2+ if it is a premium, social, or utility item.

### Interconnectivity Minimums

- Premium items should usually touch at least 2 gameplay domains where appropriate: people, dark, survival, night, companions, surreal, adventure, wealth, or car.
- "Appears once" is not enough to count as interconnected unless the item is deliberately niche.
- If an item is intentionally lightweight filler, mark it as intentionally low-impact instead of leaving it silently underdeveloped.

### Documentation Minimums

- Every tracked item must have a short "what it does" description in the item docs.
- Every tracked item must appear in the completion ledger with current status.
- Every tracked item should appear in `ITEM_LIVE_REFERENCE.md` with a short live-use summary.
- `DEV_INDEX.md` must point to both the item reference doc and the completion ledger.

### Optional-System Closure Rule

The following do not need to be implemented for item coverage to be considered complete, but they must be explicitly resolved as either `implemented` or `cut`:

- Expanded NPC gifting
- Companion quest chains and reward items
- Secret Marvin back room / hidden shop layer
- Hoarding consequences
- Item evolution
- Item lore discovery
- Weather-item synergy pilot

### Final Audit Rule

Item work is only truly complete when the per-item ledger shows no unresolved high-priority rows in the tracked categories.

---

## Current Truth

These parts are already substantially implemented and should not be treated as open work:

- Marvin item core blackjack behavior in `blackjack.py`
- Marvin durability systems in `story/durability.py` and `story/systems.py`
- Gift wrapping and Dealer gift system in `story/systems.py` and `story/locations.py`
- Mechanic loyalty reward items: `Tom's Wrench`, `Frank's Flask`, `Oswald's Dice`
- Inventory-aware event weighting in `lists.py`
- Major crafting expansion in `lists.py`
- Workbench browse, hints, inspect, and multi-tier crafting flow in `story/locations.py`
- Wrong-item event infrastructure and several wild-item events
- Large portions of gadget, disguise, tonic, dark arts, luxury, and vehicle recipe text/data

---

## Remaining Work By Original Section

### Sections 1-2: Audit And Gap Analysis

Status: stale documentation, not missing code.

Remaining work:

- Re-audit Marvin, flask, crafted, and store item coverage from live code.
- Replace false "inert" counts with verified current counts.
- Mark which items are truly under-covered instead of treating whole categories as unfinished.

Implementation target:

- `docs/ITEM_PLANNING.md`

### Section 3: Cross-File Interaction Map

Status: mostly historical reference.

Remaining work:

- Refresh counts only after the remaining event-hook passes are complete.

Implementation target:

- `docs/ITEM_PLANNING.md`

### Section 4: Multi-Item Combination Map

Status: partially surpassed by implementation, but still incomplete as a designed system.

Remaining work:

- Add the still-missing high-value pair and trio combinations from the original plan.
- Normalize trigger precedence where multiple combos can fire.
- Keep combos additive and local to event files unless a shared helper becomes necessary.

Primary files:

- `story/events_day_dark.py`
- `story/events_day_people.py`
- `story/events_night.py`
- `story/events_day_animals.py`
- `story/events_day_companions.py`
- `story/adventures.py`

### Section 5: Tier 1 Marvin Items React To The World

Status: partially implemented, but not fully saturated.

Remaining work:

- Add more upgrade-specific variants where base items already have coverage but upgrades do not feel distinct.
- Keep monitoring gloves and quiet-sneaker families for regressions, but their core weak spots are now addressed by dedicated day-event and social hooks.
- Reuse existing durability hooks when these items trigger outside blackjack.

Primary files:

- `story/events_day_dark.py`
- `story/events_day_people.py`
- `story/events_day_wealth.py`
- `story/events_night.py`
- `story/events_day_surreal.py`
- `story/events_illness.py`
- `story/adventures.py`
- `story/mechanics_intro.py`

### Section 6: Tier 2 Crafted Items Cross File Boundaries

Status: partial.

Remaining work:

- For every crafted item that still mainly exists in `events_day_items.py`, add 1-3 hooks in the best-fit non-item files.
- Prioritize items that are already partially integrated so they cross the threshold into "systemic" fastest.
- Use existing item-first precedence where a crafted item should beat its base ingredient.

Highest-priority item clusters:

- Emergency Blanket
- Fire Starter Kit
- Binocular Scope
- Signal Mirror
- Improvised Trap
- Snare Trap
- Slingshot
- Rain Collector
- Splint
- Worry Stone
- Home Remedy
- Wound Salve
- Smelling Salts
- Car Alarm Rigging

Primary files:

- `story/events_day_dark.py`
- `story/events_day_people.py`
- `story/events_day_survival.py`
- `story/events_day_animals.py`
- `story/events_day_companions.py`
- `story/events_night.py`
- `story/events_illness.py`
- `story/adventures.py`

### Section 7: Convenience Store Items Come Alive

Status: mixed. Necronomicon is alive; many ordinary store items are still underdeveloped.

Remaining work:

- Expand non-crafted store items that still feel shallow in world interaction.
- Focus on items with high flavor payoff: Running Shoes, Deck of Cards, Dog Whistle, Disposable Camera, Binoculars, and luxury consumables.
- Use common events instead of one-off novelty wherever possible.

Primary files:

- `story/events_day_people.py`
- `story/events_day_dark.py`
- `story/events_day_survival.py`
- `story/events_day_companions.py`
- `story/events_night.py`
- `story/adventures.py`

### Section 8: Secret Multi-Item Combinations

Status: partial.

Remaining work:

- Add the most valuable missing defensive combinations.
- Add the most valuable missing information combinations.
- Add the most valuable missing social and companion combinations.
- Avoid bloating this into a universal combo framework unless repetition becomes unmanageable.

Top combinations still worth implementing:

- Necronomicon + Dream Catcher
- Phoenix Feather + Fire Starter Kit
- Scrap Armor + Road Flare Torch
- Quiet Sneakers + Tattered Cloak
- Oracle's Tome + Deck of Cards
- Mirror of Duality + Marvin's Monocle
- Binocular Scope + Night Vision Scope
- Animal Whistle + Dog Whistle
- Vintage Wine + Gambler's Chalice
- Pet Toy + Companion Bed + Feeding Station

### Section 9: Missing Systemic Mechanics

Status: partially implemented.

Already present:

- Dealer gift system
- Mechanic loyalty items

Remaining work:

- Decide whether non-Dealer NPC gifting is still in scope.
- Decide whether companion quest chains and companion quest reward items are still in scope.
- Pilot an item lore discovery system if the original backstory-unlock idea still matters.
- Pilot weather-item synergy only if additive hooks are not enough.
- Add any missing payoff loops for mechanic loyalty items if they still feel too isolated.

This section should be treated as optional-until-proven-necessary after additive event work is done.

Primary files:

- `story/systems.py`
- `story/player_core.py`
- `story/locations.py`
- `story/events_day_companions.py`
- `story/day_cycle.py`

### Section 10: New Features

Status: mostly still open.

Remaining work candidates:

- Secret Marvin back room or equivalent hidden shop content
- Item evolution chains
- Hoarding consequences
- Wrong-item expansion beyond the already-implemented set

Implementation rule:

- Do not start this section until additive coverage work is stable.
- Prefer isolated flags and one-way unlocks over broad new systems.

### Section 11: Flask Narrative Integration

Status: partial.

Already present:

- Strong casino-facing flask hooks
- Some illness, survival, and companion reactions
- Event-pool weighting for Fortunate Day and Fortunate Night

Remaining work:

- Add more non-casino context for Anti-Venom and Anti-Virus.
- Add stronger flavor and payoff hooks for Fortunate Day and Fortunate Night.
- Add a few more broad-use narrative triggers for No Bust, Second Chance, Split Serum, and Pocket Aces if they still feel too table-only.

Primary files:

- `story/events_illness.py`
- `story/events_day_survival.py`
- `story/events_day_companions.py`
- `story/events_night.py`
- `story/events_day_dark.py`

### Section 12: Companion-Item Synergy Plan

Status: partial, but further along than the original audit suggested.

Remaining work:

- Inventory all existing synergy events in `events_day_companions.py`.
- Add only the missing companion-item pairings that still matter for coverage.
- Avoid duplicating already-implemented synergy events.

Primary files:

- `story/events_day_companions.py`
- `story/events_day_animals.py`
- `story/game_flow.py`

### Section 13: Adventure Zone Item Gaps

Status: partial.

Remaining work:

- Fill remaining zone-specific hooks for underused items in `adventures.py`.
- Give more crafted and high-tier items adventure-specific payoff.
- Make sure each major adventure region has at least a few item-specific advantages beyond generic survival gear.

Primary file:

- `story/adventures.py`

### Section 14: Event Weight Tuning Notes

Status: implemented enough for now.

Remaining work:

- Only extend if new item families still need pool influence after direct event-hook work.
- Otherwise this section is done and only needs documentation cleanup.

### Section 15: Implementation Priority Matrix

Status: superseded by this document.

Remaining work:

- None. Use the execution waves below instead.

### Sections 16-25: Crafting Expansion And Tiers

Status: mostly implemented in data and workbench flow.

Remaining work:

- Stop treating recipe implementation as open.
- Focus only on world integration for crafted items that already exist.
- Verify any missing Tier 4 event payoffs once lower-tier coverage is complete.

### Sections 26-35: Visualization, Hints, Text, Shop And Pawn Descriptions

Status: mostly implemented.

Remaining work:

- Documentation cleanup only.
- Optional consistency pass after gameplay work is done.

### Sections 36-43: Full Event Narrative Drafts For Crafted Families

Status: strongest source of real remaining content work.

Remaining work:

- Gadgets and Disguises: top off any obvious weak spots, but these are not the biggest gap.
- Tonics and Dark Arts: add missing medium-coverage event hooks where the recipe layer outpaces the live event layer.
- Luxury Crafts: still needs broader social, wealth, dark, and night integration.
- Vehicle Upgrades: still needs broader people, survival, and story presence outside car failure handling.
- Tier 2 items: still need more non-item-event hooks.
- Tier 3 and Tier 4 items: still the largest coverage gap among crafted systems.

Primary files:

- `story/events_day_people.py`
- `story/events_day_wealth.py`
- `story/events_day_dark.py`
- `story/events_day_survival.py`
- `story/events_night.py`
- `story/events_day_animals.py`
- `story/events_day_companions.py`
- `story/events_car.py`
- `story/events_day_surreal.py`
- `story/adventures.py`

### Section 44: Wild Item Interactions

Status: partial.

Remaining work:

- Expand the existing wild-item event family using the current pattern in `lists.py` and the live event files.
- Expand wrong-item moments only where they create good comedy or risk-reward.
- Focus on 8-12 high-value weird interactions instead of trying to implement every draft.
- Keep these optional and non-blocking for core progression.

### Sections 45-46: Quality Pass And Craft Text Overhaul

Status: largely integrated already.

Remaining work:

- Only revisit if new event writing creates visible tone mismatch.

---

## Execution Waves

### Wave 1: Remaining Marvin Coverage

Goal: finish the still-under-covered Marvin and Marvin-upgrade world hooks.

Deliverables:

- Dealer's Grudge and Dealer's Mercy saturation pass
- Upgrade-specific variants where upgrades still feel too similar to base items
- Durability-consistent non-blackjack triggers

### Wave 2: Flask Completion Pass

Goal: make flasks feel like world items, not just casino modifiers.

Deliverables:

- More Anti-Venom and Anti-Virus world saves
- More Fortunate Day and Fortunate Night visible payoffs
- A few high-impact narrative uses for remaining table-flask items

### Wave 3: Crafted Cross-File Pass

Goal: move lingering crafted items out of `events_day_items.py` isolation.

Deliverables:

- 1-3 new hooks per under-covered crafted item
- Better coverage in dark, people, night, survival, companions, and adventure files

### Wave 4: Luxury And Vehicle Integration

Goal: make these crafted families feel truly systemic.

Deliverables:

- More common people-event and wealth-event hooks for luxury items
- More social and world-facing uses for vehicle upgrade items outside raw repair events

### Wave 5: Tier 2 Through Tier 4 World Hooks

Goal: make high-tier crafted items matter outside crafting and inspection.

Deliverables:

- Selective but meaningful Tier 2 item integration
- 2-4 memorable triggers per Tier 3 or Tier 4 item where appropriate

### Wave 6: Systemic Stretch Features

Goal: implement only the remaining big systems that still feel worth the complexity.

Candidates:

- Secret shop layer
- Expanded gifting beyond Dealer
- Companion quest chains and quest reward items
- Hoarding consequences
- Item evolution if still desired
- Item lore discovery unlocks
- Weather-item synergy pilot
- Additional wrong-item moments

---

## Implementation Rules

1. Prefer editing existing events over adding new systems.
2. Reuse current helpers, statuses, dangers, and durability methods.
3. When a crafted item upgrades a base item, check the crafted item first.
4. Keep new effects local and comprehensible.
5. Do not broaden scope during implementation without updating this document first.

---

## Tracking Checklist

### Documentation

- [ ] Re-audit `ITEM_PLANNING.md` opening sections
- [ ] Mark stale sections as historical
- [ ] Keep this document updated as waves land
- [ ] Keep `ITEM_COMPLETION_LEDGER.md` synchronized with implementation
- [ ] Keep `DEV_INDEX.md` pointing at the current item references

### Wave Progress Notes

- [ ] Wave 1 Marvin coverage complete
- [x] Wave 1 batch 1: utility Marvin items gained new people and illness hooks
- [x] Wave 1 batch 2: surreal upgrades and medical or stealth upgrades gained distinct world hooks
- [x] Wave 1 batch 3: luck, prophecy, surveillance, and dealer-mark families now have richer people and wealth hooks
- [x] Wave 1 batch 4: timekeeping, mercy, hot-money reads, and silver-value items gained new people, numbers, dark, and companion hooks
- [x] Wave 1 batch 5: identity, shabby-disguise, and insurance families gained new people and emergency-scene hooks
- [x] Wave 1 batch 6: compass and silver-bar families gained new people and wealth hooks, and stale Marvin rows were reconciled against live code
- [x] Wave 1 batch 7: gloves and quiet-sneaker families gained stronger day-event avoidance, social leverage, and upgrade-specific variants
- [x] Wave 1 batch 8: High Roller combo gained additional casino-security recognition and VIP-treatment coverage
- [x] Wave 1 batch 9: indicator and manipulator families plus key flask families gained major new illness, survival, animal, and numbers hooks
- [x] Wave 1 batch 10: Fortunate Day and Fortunate Night gained explicit visible payoff branches in wealth and night events; Flask of Split Serum, Pocket Aces, and Second Chance got first non-casino narrative hooks in social, survival, and dark contexts
- [x] Wave 1 batch 11: Slingshot and Running Shoes moved to partial status with animal/dark escape hooks; Road Flare Torch strengthened with swamp-navigation night-event coverage beyond combo-only use

### Content Coverage

- [ ] Finish remaining Marvin world hooks
- [ ] Finish remaining flask world hooks
- [ ] Finish remaining crafted cross-file hooks
- [ ] Finish luxury and vehicle world coverage
- [ ] Finish Tier 2 item coverage
- [ ] Finish Tier 3 item coverage
- [ ] Finish Tier 4 item coverage
- [ ] Expand wild-item interactions to target set
- [ ] Expand wrong-item moments where still worthwhile

### Optional Systems

- [ ] Decide whether NPC gifting beyond Dealer is still in scope
- [ ] Decide whether companion quest chains are still in scope
- [ ] Decide whether secret shop is still in scope
- [ ] Decide whether hoarding consequences are still in scope
- [ ] Decide whether item evolution is still in scope
- [ ] Decide whether item lore discovery is still in scope
- [ ] Decide whether a weather-item synergy pilot is still in scope

---

## Next Concrete Steps

1. Finish the Marvin pass.
2. Finish the flask pass.
3. Build a per-item crafted coverage ledger for under-covered crafted items.
4. Execute the crafted cross-file pass in file clusters.
5. Revisit this document after each wave and remove completed work.
6. Update `ITEM_COMPLETION_LEDGER.md` and `DEV_INDEX.md` whenever item coverage meaningfully changes.
