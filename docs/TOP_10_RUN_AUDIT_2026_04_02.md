# Top 10 Run Audit (2026-04-02 Random 200)

This audit is based on replaying the current top 10 runs from `tools/cumulative_test_out.txt` with:

```text
tools/quicktest.py 1000 <seed>
```

For each seed, the review used the structured decision traces in `tools/test_out.json`, the cycle summaries in `tools/test_out.txt`, and the exact narrative tail in `tools/story_out.txt`.

## Top 10 Seeds Reviewed

By peak balance from the latest `random/200` batch:

1. `1736117051` peak `$90,723`
2. `594063413` peak `$24,073`
3. `447854184` peak `$15,231`
4. `515466475` peak `$15,004`
5. `460815224` peak `$14,360`
6. `205118913` peak `$11,262`
7. `820687521` peak `$10,438`
8. `1114482741` peak `$9,730`
9. `247187017` peak `$8,289`
10. `287586888` peak `$8,181`

## Cross-Run Findings

1. The dominant late-game failure is not one blackjack action; it is route/prompt policy drift after the bankroll spike. Eight of the top ten runs still top-route through Marvin, and several of them keep routing to Marvin, the convenience store, or doctor loops after the run is already in a fragile state.

2. The autoplayer still wastes too many late afternoons on low-conversion actions. The exact traces show repeated convenience-store food buys, Marvin window shopping with no purchase, and mechanic/doctor loops that preserve life temporarily but do not rebuild the bankroll.

3. Debt cleanup is still mishandled. Two of the top five bankrupts end at Vinnie enforcement prompts, and the exact final input is `pay what you have`, which zeroes the run after the bot spent the preceding day at the convenience store instead of solving the debt state.

4. Sanity-collapse endings are driven by misaligned route choices. In the madness seeds, the bot keeps choosing Marvin or convenience-store routes under `stabilize_sanity` / `survive_emergency` goals, often with no meaningful purchase, and only goes doctor when the run is already unrecoverable.

5. Betsy no longer kills the bot directly, but she still zeroes out several otherwise strong runs because the bot arrives at the tractor/army stages with no millionaire conversion, no counterplay, and too little cash to survive the survival-first payment policy.

## Per-Run Findings

### 1. Seed `1736117051` (`broke`, peak `$90,723`, final day `213`)

- Exact late decisions:
  - `d210 route_select 5 <- goal=restore_blackjack_edge_after_breakage selected Convenience Store`
  - `d210 purchase_select 13 <- Turkey Sandwich - $15`
  - `d210 purchase_select 12 <- Duct Tape - $12`
  - `d211 route_select 5 <- Convenience Store`
  - `d211 purchase_select 2 <- Pocket Knife - $35`
  - `d212 route_select 5 <- Convenience Store`
  - `d212 purchase_select 1 <- Rope - $20`
  - terminal `Moo? -> yes <- betsy_tractor_survival_override`
- What went wrong:
  - After reaching `$90k`, the bot was no longer converting toward millionaire or protecting the bankroll.
  - The exact late inputs are low-value store purchases on three consecutive days, followed by a Betsy tractor payment that clamped the remaining bankroll to `$0`.

### 2. Seed `594063413` (`broke`, peak `$24,073`, final day `108`)

- Exact late decisions:
  - `d107 route_select 4 <- goal=restock_supplies selected Convenience Store`
  - `d107 purchase_select 12 <- Turkey Sandwich - $15`
  - multiple `yes <- gift_wrap_happiness_gate`
  - terminal enforcement branch `pay what you have <- pay_partial_when_possible`
- Final prompt context:
  - `"Vinnie's done waiting. You owe him $13,529. Today."`
- What went wrong:
  - The bot carried a large debt state into the terminal enforcement window.
  - Instead of routing to debt resolution earlier, it spent the preceding afternoon at the convenience store and kept spending on side actions, then surrendered the remaining bankroll at enforcement.

### 3. Seed `447854184` (`died`, peak `$15,231`, final day `66`)

- Exact late decisions:
  - `d64 route_select 1 <- goal=survive_emergency selected Witch Doctor's Tower`
  - `d64 yes_no no <- threat_context_refusal`
  - `d64 purchase_select 10 <- I'm not buying anything`
  - `d65 route_select 1 <- goal=survive_emergency selected Witch Doctor's Tower`
  - `d65 yes_no no <- threat_context_refusal`
  - `d65 purchase_select 8 <- I'm not buying anything`
- Final prompt context:
  - `Would you like me to HEAL you, HUMAN?`
- What went wrong:
  - This is the clearest exact-policy failure in the top 10.
  - The route policy correctly sent the player to healing twice under `survive_emergency`, but the yes/no policy answered `no` to the heal prompt both times, and the purchase policy then selected `I'm not buying anything`.
  - The run died of untreated wounds immediately afterward.

### 4. Seed `515466475` (`madness`, peak `$15,004`, final day `90`)

- Exact late decisions:
  - `d87 yes <- marvin_offer_rank01_high_priority:Pocket Watch`
  - `d87 yes <- marvin_offer_rank01_high_priority:White Feather`
  - `d87 yes <- marvin_offer_rank01_high_priority:Faulty Insurance`
  - `d88 route_select 4 <- goal=survive_emergency selected Convenience Store`
  - `d88 purchase_select 9 <- Cup Noodles - $7`
  - `d89 route_select 1 <- urgent medical override -> Doctor's Office`
- What went wrong:
  - The run was already sanity-fragile, but the exact late inputs still spent cash at Marvin and then shifted to a snack/store day.
  - The doctor interrupt arrived one day before the terminal madness ending, which is too late to recover from the prior sanity spiral.

### 5. Seed `460815224` (`broke`, peak `$14,360`, final day `129`)

- Exact late decisions:
  - `d126 route_select 2 <- Witch Doctor's Tower`
  - `d126 yes_no no <- threat_context_refusal`
  - `d126 purchase_select 8 <- I'm not buying anything`
  - `d127 route_select 1 <- Doctor's Office`
  - `d128 route_select 4 <- Convenience Store`
  - terminal enforcement branch `pay what you have <- pay_partial_when_possible`
- Final prompt context:
  - `"Vinnie's done waiting. You owe him $2,160. Today."`
- What went wrong:
  - This run mixed emergency-routing with debt neglect.
  - It refused witch healing, took a doctor day, then spent the final interactive afternoon at the convenience store before the loan-shark enforcement wiped out the bankroll.

### 6. Seed `205118913` (`broke`, peak `$11,262`, final day `137`)

- Exact late decisions:
  - no route choices in the last three days; all afternoons auto-handoff through day/story events
  - terminal `Moo? -> yes <- betsy_tractor_survival_override`
  - decision summary includes `betsy_hungry_survival_override=10`
- What went wrong:
  - The run spent a large part of its event budget repeatedly feeding Betsy and never converted the rank-2 bankroll into a durable winning state.
  - By the time the tractor stage arrived, the only surviving input was another Betsy payment, which zeroed the run.

### 7. Seed `820687521` (`broke`, peak `$10,438`, final day `217`)

- Exact late decisions:
  - `d208` through `d217`: `route_select 1 <- urgent medical override -> Doctor's Office` ten days in a row
- What went wrong:
  - This run devolved into a pure doctor loop.
  - The exact route decisions show ten consecutive doctor overrides with no productive recovery path afterward, so the bot kept spending afternoons on medical stabilization until the bankroll was gone.

### 8. Seed `1114482741` (`madness`, peak `$9,730`, final day `109`)

- Exact late decisions:
  - `d107` repeated Marvin offer declines (`Pocket Watch`, `Health Indicator`, `Sneaky Peeky Shades`)
  - `d108 route_select 4 <- goal=survive_emergency selected Convenience Store`
  - `d108 purchase_select 9 <- Beef Jerky - $10`
  - `d108 purchase_select 1 <- Candy Bar - $5`
  - `d108 event_branch save <- generic_low_resource_choice:save`
- What went wrong:
  - The bot was already in a sanity emergency but still spent the final day on low-impact food handling and Marvin browsing rather than decisive sanity recovery.
  - The exact final interactive inputs are snack purchases and `save` branches, followed by madness on the next cycle.

### 9. Seed `247187017` (`broke`, peak `$8,289`, final day `127`)

- Exact late decisions:
  - `d123 route_select 3 <- goal=recover_from_car_trouble selected Oswald's Optimal Outoparts`
  - `d124 route_select 3 <- Oswald's Optimal Outoparts`
  - `d125 route_select 3 <- Oswald's Optimal Outoparts`
  - `d126 route_select 3 <- Oswald's Optimal Outoparts`
  - terminal `Moo? -> yes <- betsy_tractor_survival_override`
- What went wrong:
  - The bot spent four consecutive afternoons in an Oswald loop under `recover_from_car_trouble` and got no bankroll conversion from it.
  - Immediately after that loop, Betsy tractor zeroed the remaining cash.

### 10. Seed `287586888` (`madness`, peak `$8,181`, final day `88`)

- Exact late decisions:
  - `d87 route_select 6 <- goal=stabilize_sanity selected Marvin's Mystical Merchandise`
  - then eight straight Marvin offer refusals:
    - `Lucky Coin`
    - `Twin's Locket`
    - `Twin's Locket`
    - `Rusty Compass`
    - `Delight Indicator`
    - `Dealer's Grudge`
    - `Gambler's Chalice`
    - `Dirty Old Hat`
- What went wrong:
  - This is the clearest route-goal mismatch among the madness runs.
  - Under `stabilize_sanity`, the exact route choice was Marvin, and the exact follow-up inputs were a full afternoon of refusing items. The bot spent the final actionable day on a zero-payoff Marvin loop and then hit madness the next cycle.

## Bottom Line

The top 10 runs are not mainly failing because of single blackjack misplays. They are failing because the autoplay keeps making low-conversion daytime decisions after reaching a viable bankroll:

- repeated Marvin visits with no purchase or with sanity-irrelevant purchases,
- repeated convenience-store afternoons spent on food and misc items,
- repeated doctor/mechanic loops that preserve life but do not recover trajectory,
- debt states left unresolved until Vinnie enforcement,
- Betsy still acting as a bankroll wipe because the run arrives there undercapitalized.

The single sharpest prompt bug exposed by the top 10 is still the Witch Doctor heal refusal in seed `447854184`.