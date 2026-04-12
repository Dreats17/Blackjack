# Top Run Audit: Seed 1449769179

Top run under the current code after the dealer-happiness sync fix and the route-circulation fix.

## Snapshot

- Seed: `1449769179`
- Outcome: `broke`
- Peak balance: `$51,285`
- Peak day: `162`
- Final day: `164`
- Final balance: `$0`
- Final state: `Alive=True`, `HP 100`, `SAN 100`, `Rank 3`

Primary source artifacts:

- `tools/test_out.json` for the full structured ledger of all `1122` decisions
- `tools/test_out.txt` for cycle-by-cycle balances and end-state
- `tools/story_out.txt` for the exact text shown during the run

## Decision Inventory

- Total decisions: `1122`
- Blackjack actions: `661`
- Blackjack bets: `385`
- Yes/no prompts: `68`
- Event branches: `8`

Interpretation:

- The run was not lost because of one obviously bad hit/stand sequence.
- The run was lost at the strategy layer: bankroll management, route conversion failure, and a terminal Betsy storyline event.

## What Actually Killed The Run

The bankroll peaked at `$51,285` on day `162`, then the run reached day `164` still alive and still at rank `3`.

The final loss was not a blackjack bust spiral. It was the Betsy army finale:

- Story text: `Do you feed Betsy and her friends?`
- Cost of answering yes: `$100,000`
- Cost of answering no: death by cow attack

In this run, the autoplay answered `yes`, the balance dropped to `$0`, and the game ended immediately because the player had no cash left.

Important nuance: by the time this prompt appeared, the run was already strategically cornered. At `$55,285`, both available answers were losing answers:

- `yes` means immediate bankruptcy
- `no` means immediate death

So the final click was not the root-cause mistake. The root cause was arriving at the Betsy army finale with no counter-item, no millionaire conversion, and only `$55k` liquid.

## Afternoon Travel Decisions

This replay did not surface any explicit afternoon destination menu to the autoplay layer.

Verified counts from the replay artifacts:

- `route_select` traces: `0`
- `menu_select` traces: `0`
- story occurrences of `How do you want to spend the rest of your afternoon`: `0`
- story occurrences of `You get in your car and drive to`: `0`

The regenerated harness now also records the afternoon-to-night handoff explicitly in both `tools/test_out.txt` and `tools/test_out.json`.

Representative late-run flow lines:

```text
Cycle 143 | Day 144
Flow    menu=skipped | route=none | handoff=afternoon auto-handoff after day:attacked_by_dog | night=drive

Cycle 145 | Day 146
Flow    menu=skipped | route=none | handoff=afternoon auto-handoff after storyline:radio_signal:stage2 | night=drive

Cycle 149 | Day 150
Flow    menu=skipped | route=none | handoff=afternoon auto-handoff after storyline:betsy:stage1 | night=drive
```

That resolves the earlier ambiguity about owning the car. In this seed, the player did have a car, but the afternoon still handed off straight into the night phase after the daytime event resolved. The car only changed the night mode from walking to driving; it did not force an explicit destination menu.

So there were no discretionary afternoon travel choices of the form:

- `Doctor's Office`
- `Convenience Store`
- `Marvin's Mystical Merchandise`
- `Stay Home`
- other route/menu destinations

What the run did have was a small number of scripted daytime travel intents embedded in event text. Those are the only afternoon-travel entries that can be added for this seed:

```text
Day 109: headed out from the car to grab a cheap coffee
Day 144: headed toward a convenience store, but the approach was interrupted by a hostile dog and the player returned to the car
Day 147: headed out from the car to the dumpster behind a convenience store
```

Interpretation:

- The replay did have daytime movement.
- It did not have any explicit afternoon destination selection screen.
- The replay now proves that those days were `menu=skipped` / `night=drive` handoffs, not missing parser output.
- The afternoon travel layer for this seed was effectively scripted, not chosen.

## Chronological Daytime Prompt Choices

These are all `76` non-blackjack decisions from the structured trace, in order.

```text
0    cycle None day 1   yes_no      choice yes        reason car_repair_required
9    cycle 1    day 2   yes_no      choice no         reason adapter_budget_gate
30   cycle 4    day 5   event_branch choice hide      reason hide_robbery_cover
46   cycle 7    day 8   yes_no      choice no         reason threat_context_refusal
52   cycle 8    day 9   event_branch choice heads     reason coin_flip_heads
68   cycle 10   day 11  yes_no      choice no         reason threat_context_refusal
75   cycle 11   day 12  yes_no      choice no         reason event_no:hang up?
103  cycle 14   day 15  yes_no      choice yes        reason event_yes:ask about the photo?
133  cycle 18   day 19  yes_no      choice no         reason threat_context_refusal
147  cycle 20   day 21  yes_no      choice no         reason threat_context_refusal
160  cycle 22   day 23  yes_no      choice no         reason threat_context_refusal
173  cycle 24   day 25  yes_no      choice no         reason threat_context_refusal
185  cycle 26   day 27  yes_no      choice yes        reason event_yes:walk through the cemetery while you wait?
191  cycle 27   day 28  yes_no      choice yes        reason event_yes:talk to... dr. socksworth?
197  cycle 28   day 29  yes_no      choice yes        reason event_yes:feed it some of your food?
207  cycle 30   day 31  yes_no      choice yes        reason event_yes:pick it up?
220  cycle 32   day 33  yes_no      choice yes        reason mechanic_intro_offer
221  cycle 32   day 33  yes_no      choice yes        reason mechanic_intro_offer
230  cycle 33   day 34  yes_no      choice yes        reason mechanic_intro_offer
237  cycle 34   day 35  yes_no      choice no         reason threat_context_refusal
257  cycle 37   day 38  event_branch choice need      reason generic_non_risky_choice
272  cycle 39   day 40  yes_no      choice yes        reason event_yes:applaud the performance?
283  cycle 41   day 42  yes_no      choice no         reason event_no:give jameson $100 for vet bills?
297  cycle 43   day 44  yes_no      choice yes        reason event_yes:talk to edgar?
315  cycle 46   day 47  yes_no      choice yes        reason book_club_sanity_gate
332  cycle 49   day 50  yes_no      choice no         reason threat_context_refusal
347  cycle 51   day 52  yes_no      choice no         reason threat_context_refusal
356  cycle 52   day 53  yes_no      choice yes        reason event_yes:pick her up?
375  cycle 54   day 55  yes_no      choice yes        reason event_yes:try to befriend the trash gremlin?
381  cycle 55   day 56  yes_no      choice yes        reason event_yes:ask the dealer about his past?
390  cycle 56   day 57  yes_no      choice no         reason event_no:pay him $50 for the info?
391  cycle 56   day 57  yes_no      choice no         reason cupcake_sanity_gate
399  cycle 57   day 58  yes_no      choice no         reason event_no:ask who 'they' are?
413  cycle 59   day 60  yes_no      choice no         reason threat_context_refusal
420  cycle 60   day 61  yes_no      choice yes        reason event_yes:feed it some of your food?
434  cycle 61   day 62  yes_no      choice no         reason threat_context_refusal
448  cycle 63   day 64  yes_no      choice yes        reason event_yes:enter the carnival?
463  cycle 66   day 67  yes_no      choice no         reason threat_context_refusal
470  cycle 67   day 68  yes_no      choice yes        reason event_yes:ask if it gets better?
491  cycle 70   day 71  event_branch choice apologize reason apologize_default
492  cycle 70   day 71  yes_no      choice yes        reason event_yes:accept the vip treatment?
498  cycle 71   day 72  yes_no      choice no         reason threat_context_refusal
510  cycle 73   day 74  yes_no      choice no         reason threat_context_refusal
522  cycle 75   day 76  yes_no      choice yes        reason event_yes:accept his lesson?
561  cycle 81   day 82  yes_no      choice yes        reason event_yes:take the letter?
588  cycle 85   day 86  yes_no      choice yes        reason event_yes:"answer me. "
601  cycle 87   day 88  yes_no      choice yes        reason mechanic_intro_offer
621  cycle 90   day 91  yes_no      choice yes        reason event_yes:"what was that?"
622  cycle 90   day 91  yes_no      choice yes        reason event_yes:"what was that?"
623  cycle 90   day 91  event_branch choice kick it away reason kick_rat_away
629  cycle 91   day 92  yes_no      choice yes        reason blank_prompt_investigate_yes
695  cycle 101  day 102 yes_no      choice no         reason threat_context_refusal
711  cycle 103  day 104 yes_no      choice no         reason threat_context_refusal
718  cycle 104  day 105 event_branch choice leave     reason prefer_safe_choice:leave
740  cycle 107  day 108 yes_no      choice yes        reason event_yes:do you like it?
754  cycle 109  day 110 yes_no      choice yes        reason event_yes:check out the apartment?
762  cycle 110  day 111 yes_no      choice yes        reason mechanic_intro_offer
841  cycle 122  day 123 yes_no      choice no         reason adapter_budget_gate
862  cycle 125  day 126 event_branch choice follow    reason prefer_safe_choice:follow
880  cycle 128  day 129 yes_no      choice yes        reason fine_reserve_gate
886  cycle 129  day 130 yes_no      choice yes        reason event_yes:write down the numbers?
906  cycle 132  day 133 yes_no      choice yes        reason betsy_hungry_budget_gate
907  cycle 132  day 133 yes_no      choice yes        reason betsy_hungry_budget_gate
941  cycle 137  day 138 yes_no      choice yes        reason event_yes:try to tune to the frequency and listen for more?
961  cycle 140  day 141 yes_no      choice yes        reason event_yes:try to return it to the owner?
967  cycle 141  day 142 yes_no      choice yes        reason bodyguard_budget_gate
993  cycle 145  day 146 yes_no      choice yes        reason event_yes:go inside?
994  cycle 145  day 146 yes_no      choice yes        reason event_yes:take the logbook?
1025 cycle 149  day 150 yes_no      choice yes        reason betsy_tractor_budget_gate
1030 cycle 150  day 151 event_branch choice moonwalk  reason moonwalk
1045 cycle 152  day 153 yes_no      choice yes        reason event_yes:do you try to explain your situation?
1076 cycle 157  day 158 yes_no      choice no         reason charity_surplus_gate
1083 cycle 158  day 159 yes_no      choice yes        reason event_yes:take him in?
1092 cycle 159  day 160 yes_no      choice yes        reason event_yes:keep petting him?
1109 cycle 161  day 162 yes_no      choice yes        reason event_yes:accept the coffee?
1121 cycle 163  day 164 yes_no      choice yes        reason betsy_hungry_budget_gate
```

Interpretation:

- The replay did have daytime choices.
- Those choices were prompt-driven event choices, not destination-menu travel choices.
- The entire controllable daytime layer for this seed is the prompt list above.

## Betting Choices

The replay recorded `385` blackjack bet selections.

High-level pattern:

- Days `1-31`: tiny bootstrap bets while trying to get off the ground
- Days `32-89`: gradual ramping, then a brief lucky-coin edge window with more assertive bets
- Days `90-102`: recovery and drawdown-protection bets during low-stability play
- Days `103-126`: smooth-ramp and post-car growth bets while rebuilding after edge deterioration
- Days `127-163`: mostly `wealth_lock_preserve(...)` bets, even though `edge=0`

That last phase is the strategic problem. The bot was still risking large chunks of bankroll after it had already lost meaningful leverage.

### Day-By-Day Bet Ledger

```text
DAY 1: bets=6, 5, 4 || reasons=acquire_car | no_car_bootstrap_survival(survival_conservative) edge=0
DAY 2: bets=3, 3, 3 || reasons=acquire_car | no_car_bootstrap_survival(survival_conservative) edge=0 ; acquire_car | no_car_bootstrap_survival(baseline_random) edge=0
DAY 3: bets=4, 5, 6 || reasons=acquire_car | no_car_bootstrap_survival(survival_conservative) edge=0
DAY 4: bets=4, 5, 4 || reasons=acquire_car | no_car_bootstrap_survival(survival_conservative) edge=0
DAY 5: bets=3, 3 || reasons=acquire_car | no_car_bootstrap_survival(survival_conservative) edge=0
DAY 6: bets=3, 4 || reasons=acquire_car | no_car_bootstrap_survival(survival_conservative) edge=0
DAY 7: bets=27, 27 || reasons=acquire_car | no_car_bootstrap_push(survival_conservative) edge=0
DAY 8: bets=24, 30 || reasons=acquire_car | no_car_bootstrap_push(baseline_random) edge=0 ; acquire_car | no_car_bootstrap_push(survival_conservative) edge=0
DAY 9: bets=37, 28 || reasons=acquire_car | no_car_bootstrap_push(survival_conservative) edge=0
DAY 10: bets=21, 9, 18 || reasons=acquire_car | no_car_bootstrap_push(survival_conservative) edge=0 ; acquire_car | no_car_bootstrap_survival(survival_conservative) edge=0
DAY 11: bets=8, 6 || reasons=acquire_car | no_car_bootstrap_survival(survival_conservative) edge=0
DAY 12: bets=5, 5 || reasons=acquire_car | no_car_bootstrap_survival(survival_conservative) edge=0
DAY 13: bets=4, 4, 3 || reasons=acquire_car | no_car_bootstrap_survival(survival_conservative) edge=0
DAY 14: bets=3, 3, 3 || reasons=acquire_car | no_car_bootstrap_survival(survival_conservative) edge=0 ; acquire_car | no_car_bootstrap_survival(baseline_random) edge=0
DAY 15: bets=4, 5 || reasons=acquire_car | no_car_bootstrap_survival(survival_conservative) edge=0 ; acquire_car | no_car_bootstrap_survival(baseline_random) edge=0
DAY 16: bets=5, 5, 5 || reasons=acquire_car | no_car_bootstrap_survival(survival_conservative) edge=0
DAY 17: bets=7, 6 || reasons=stabilize_sanity | no_car_bootstrap_survival(recovery_specialist) edge=0
DAY 18: bets=7, 6 || reasons=stabilize_sanity | no_car_bootstrap_survival(recovery_specialist) edge=0
DAY 19: bets=5, 6 || reasons=stabilize_sanity | no_car_bootstrap_survival(recovery_specialist) edge=0
DAY 20: bets=8, 8 || reasons=stabilize_sanity | no_car_bootstrap_survival(recovery_specialist) edge=0
DAY 21: bets=7, 8 || reasons=acquire_car | no_car_bootstrap_survival(survival_conservative) edge=0
DAY 22: bets=19, 7 || reasons=stabilize_sanity | no_car_bootstrap_push(recovery_specialist) edge=0 ; stabilize_sanity | no_car_bootstrap_survival(recovery_specialist) edge=0
DAY 23: bets=9, 19 || reasons=acquire_car | no_car_bootstrap_survival(survival_conservative) edge=0 ; acquire_car | no_car_bootstrap_push(survival_conservative) edge=0
DAY 24: bets=7, 6, 5 || reasons=acquire_car | no_car_bootstrap_survival(survival_conservative) edge=0 ; acquire_car | no_car_bootstrap_survival(baseline_random) edge=0
DAY 25: bets=6, 5 || reasons=stabilize_sanity | no_car_bootstrap_survival(baseline_random) edge=0 ; stabilize_sanity | no_car_bootstrap_survival(recovery_specialist) edge=0
DAY 26: bets=8, 6, 8 || reasons=stabilize_sanity | no_car_bootstrap_survival(recovery_specialist) edge=0 ; stabilize_sanity | no_car_bootstrap_survival(baseline_random) edge=0
DAY 27: bets=8, 7 || reasons=stabilize_sanity | no_car_bootstrap_survival(recovery_specialist) edge=0 ; stabilize_health | no_car_bootstrap_survival(recovery_specialist) edge=0
DAY 28: bets=5, 6 || reasons=acquire_car | no_car_bootstrap_survival(survival_conservative) edge=0
DAY 29: bets=6 || reasons=preserve_companion_roster | no_car_bootstrap_survival(companion_collector) edge=0
DAY 30: bets=7, 8 || reasons=preserve_companion_roster | no_car_bootstrap_survival(companion_collector) edge=0
DAY 31: bets=8, 8, 7 || reasons=preserve_companion_roster | no_car_bootstrap_survival(companion_collector) edge=0
DAY 32: bets=21, 27, 34 || reasons=preserve_companion_roster | no_car_bootstrap_push(baseline_random) edge=0 ; preserve_companion_roster | no_car_bootstrap_push(companion_collector) edge=0
DAY 33: bets=21, 21, 21 || reasons=preserve_companion_roster | smooth_ramp_edge_0(companion_collector) edge=0 ; preserve_companion_roster | smooth_ramp_edge_0(baseline_random) edge=0
DAY 34: bets=13, 11, 12 || reasons=preserve_companion_roster | smooth_ramp_edge_0(companion_collector) edge=0
DAY 35: bets=12, 13 || reasons=preserve_companion_roster | smooth_ramp_edge_0(companion_collector) edge=0
DAY 36: bets=18, 16, 15 || reasons=acquire_car | smooth_ramp_edge_0(survival_conservative) edge=0
DAY 37: bets=16, 19, 21 || reasons=acquire_car | smooth_ramp_edge_0(survival_conservative) edge=0
DAY 38: bets=19, 21, 15 || reasons=acquire_car | smooth_ramp_edge_0(survival_conservative) edge=0 ; acquire_car | smooth_ramp_edge_0(baseline_random) edge=0
DAY 39: bets=15, 15 || reasons=acquire_car | smooth_ramp_edge_0(survival_conservative) edge=0
DAY 40: bets=15, 15 || reasons=acquire_car | smooth_ramp_edge_0(survival_conservative) edge=0
DAY 41: bets=15, 13 || reasons=acquire_car | smooth_ramp_edge_0(survival_conservative) edge=0 ; acquire_car | drawdown_protection(survival_conservative) edge=0
DAY 42: bets=12, 11, 9 || reasons=acquire_car | drawdown_protection(survival_conservative) edge=0
DAY 43: bets=11, 13 || reasons=acquire_car | drawdown_protection(survival_conservative) edge=0
DAY 44: bets=12, 12 || reasons=acquire_car | drawdown_protection(survival_conservative) edge=0
DAY 45: bets=15, 15, 13 || reasons=acquire_car | smooth_ramp_edge_0(survival_conservative) edge=0 ; acquire_car | drawdown_protection(survival_conservative) edge=0
DAY 46: bets=15, 16 || reasons=acquire_car | smooth_ramp_edge_0(survival_conservative) edge=0
DAY 47: bets=14, 14 || reasons=acquire_car | smooth_ramp_edge_0(survival_conservative) edge=0
DAY 48: bets=16, 17 || reasons=acquire_car | smooth_ramp_edge_0(survival_conservative) edge=0 ; acquire_car | smooth_ramp_edge_0(baseline_random) edge=0
DAY 49: bets=13, 14, 15 || reasons=acquire_car | drawdown_protection(survival_conservative) edge=0 ; acquire_car | smooth_ramp_edge_0(survival_conservative) edge=0
DAY 50: bets=15 || reasons=acquire_car | smooth_ramp_edge_0(survival_conservative) edge=0
DAY 51: bets=15, 13 || reasons=acquire_car | smooth_ramp_edge_0(survival_conservative) edge=0 ; acquire_car | drawdown_protection(survival_conservative) edge=0
DAY 52: bets=14, 16, 17 || reasons=acquire_car | smooth_ramp_edge_0(survival_conservative) edge=0
DAY 53: bets=16, 17, 12 || reasons=acquire_car | smooth_ramp_edge_0(survival_conservative) edge=0 ; acquire_car | smooth_ramp_edge_0(baseline_random) edge=0 ; acquire_car | drawdown_protection(survival_conservative) edge=0
DAY 54: bets=38, 82 || reasons=acquire_car | smooth_ramp_edge_4(survival_conservative)+items[lucky_coin]x1.14 edge=4 ; acquire_car | smooth_ramp_edge_4(wealth_aggro)+items[lucky_coin]x1.14 edge=4
DAY 55: bets=42, 30 || reasons=preserve_companion_roster | smooth_ramp_edge_4(companion_collector)+items[lucky_coin]x1.14 edge=4
DAY 56: bets=46, 34 || reasons=preserve_companion_roster | smooth_ramp_edge_4(companion_collector)+items[lucky_coin]x1.14 edge=4
DAY 57: bets=43, 31 || reasons=preserve_companion_roster | smooth_ramp_edge_4(companion_collector)+items[lucky_coin]x1.14 edge=4
DAY 58: bets=9, 8, 7 || reasons=preserve_companion_roster | drawdown_protection(companion_collector)+items[lucky_coin]x1.06 edge=4 ; preserve_companion_roster | drawdown_protection(baseline_random)+items[lucky_coin]x1.06 edge=4
DAY 59: bets=7, 6 || reasons=preserve_companion_roster | drawdown_protection(companion_collector)+items[lucky_coin]x1.06 edge=4
DAY 60: bets=7 || reasons=preserve_companion_roster | drawdown_protection(companion_collector)+items[lucky_coin]x1.06 edge=4
DAY 61: bets=6, 7, 6 || reasons=preserve_companion_roster | drawdown_protection(companion_collector)+items[lucky_coin]x1.06 edge=4
DAY 62: bets=27, 11 || reasons=acquire_car | smooth_ramp_edge_4(survival_conservative)+items[lucky_coin]x1.14 edge=4 ; acquire_car | drawdown_protection(survival_conservative)+items[lucky_coin]x1.06 edge=4
DAY 63: bets=11, 12 || reasons=acquire_car | drawdown_protection(survival_conservative)+items[lucky_coin]x1.06 edge=4
DAY 64: bets=12, 11 || reasons=acquire_car | drawdown_protection(survival_conservative)+items[lucky_coin]x1.06 edge=4
DAY 65: bets=12, 12 || reasons=acquire_car | drawdown_protection(survival_conservative)+items[lucky_coin]x1.06 edge=4
DAY 66: bets=136, 101 || reasons=acquire_car | smooth_ramp_edge_4(wealth_aggro)+items[lucky_coin]x1.14 edge=4
DAY 67: bets=74 || reasons=acquire_car | smooth_ramp_edge_4(wealth_aggro)+items[lucky_coin]x1.14 edge=4
DAY 68: bets=14, 14, 14 || reasons=acquire_car | drawdown_protection(survival_conservative)+items[lucky_coin]x1.06 edge=4
DAY 69: bets=16, 14 || reasons=acquire_car | drawdown_protection(survival_conservative)+items[lucky_coin]x1.06 edge=4
DAY 70: bets=14, 16, 14 || reasons=acquire_car | drawdown_protection(survival_conservative)+items[lucky_coin]x1.06 edge=4 ; acquire_car | drawdown_protection(baseline_random)+items[lucky_coin]x1.06 edge=4
DAY 71: bets=13, 14 || reasons=acquire_car | drawdown_protection(survival_conservative)+items[lucky_coin]x1.06 edge=4
DAY 72: bets=13, 11 || reasons=acquire_car | drawdown_protection(survival_conservative)+items[lucky_coin]x1.06 edge=4
DAY 73: bets=11, 10, 9 || reasons=acquire_car | drawdown_protection(survival_conservative)+items[lucky_coin]x1.06 edge=4
DAY 74: bets=8, 7, 7 || reasons=acquire_car | drawdown_protection(survival_conservative)+items[lucky_coin]x1.06 edge=4
DAY 75: bets=9 || reasons=acquire_car | drawdown_protection(survival_conservative)+items[lucky_coin]x1.06 edge=4
DAY 76: bets=10, 9, 8 || reasons=acquire_car | drawdown_protection(survival_conservative)+items[lucky_coin]x1.06 edge=4
DAY 77: bets=8, 7 || reasons=acquire_car | drawdown_protection(survival_conservative)+items[lucky_coin]x1.06 edge=4
DAY 78: bets=11, 10, 11 || reasons=acquire_car | drawdown_protection(survival_conservative)+items[lucky_coin]x1.06 edge=4
DAY 79: bets=11, 12 || reasons=acquire_car | drawdown_protection(survival_conservative)+items[lucky_coin]x1.06 edge=4
DAY 80: bets=11, 11 || reasons=acquire_car | drawdown_protection(survival_conservative)+items[lucky_coin]x1.06 edge=4
DAY 81: bets=13, 14, 14 || reasons=acquire_car | drawdown_protection(survival_conservative)+items[lucky_coin]x1.06 edge=4
DAY 82: bets=13, 15 || reasons=acquire_car | drawdown_protection(survival_conservative)+items[lucky_coin]x1.06 edge=4
DAY 83: bets=8, 9, 8 || reasons=acquire_car | drawdown_protection(survival_conservative)+items[lucky_coin]x1.06 edge=4
DAY 84: bets=7, 7 || reasons=acquire_car | drawdown_protection(survival_conservative)+items[lucky_coin]x1.06 edge=4
DAY 85: bets=7, 6, 6 || reasons=acquire_car | drawdown_protection(survival_conservative)+items[lucky_coin]x1.06 edge=4
DAY 86: bets=7, 6 || reasons=acquire_car | drawdown_protection(survival_conservative)+items[lucky_coin]x1.06 edge=4
DAY 87: bets=6, 6, 6 || reasons=acquire_car | drawdown_protection(survival_conservative)+items[lucky_coin]x1.06 edge=4
DAY 88: bets=10 || reasons=acquire_car | drawdown_protection(survival_conservative)+items[lucky_coin]x1.06 edge=4
DAY 89: bets=11, 10 || reasons=acquire_car | drawdown_protection(baseline_random)+items[lucky_coin]x1.06 edge=4 ; acquire_car | drawdown_protection(survival_conservative)+items[lucky_coin]x1.06 edge=4
DAY 90: bets=11 || reasons=stabilize_health | drawdown_protection(recovery_specialist)+items[lucky_coin]x1.06 edge=4
DAY 91: bets=12, 11 || reasons=survive_emergency | drawdown_protection(recovery_specialist)+items[lucky_coin]x1.06 edge=4
DAY 92: bets=11, 12 || reasons=stabilize_health | drawdown_protection(recovery_specialist) edge=0 ; survive_emergency | drawdown_protection(recovery_specialist) edge=0
DAY 93: bets=14, 15, 17 || reasons=stabilize_health | drawdown_protection(recovery_specialist) edge=0
DAY 94: bets=6, 6 || reasons=survive_emergency | drawdown_protection(recovery_specialist) edge=0
DAY 95: bets=7, 8, 7 || reasons=survive_emergency | drawdown_protection(recovery_specialist) edge=0
DAY 96: bets=8, 7 || reasons=stabilize_health | drawdown_protection(recovery_specialist) edge=0
DAY 97: bets=8, 7, 8 || reasons=stabilize_health | drawdown_protection(recovery_specialist) edge=0
DAY 98: bets=9, 9, 10 || reasons=stabilize_health | drawdown_protection(recovery_specialist) edge=0
DAY 99: bets=11, 12, 15 || reasons=stabilize_health | drawdown_protection(recovery_specialist) edge=0
DAY 101: bets=20, 20 || reasons=stabilize_health | drawdown_protection(recovery_specialist) edge=0
DAY 102: bets=24, 27, 32 || reasons=stabilize_health | drawdown_protection(recovery_specialist) edge=0 ; stabilize_health | smooth_ramp_edge_0(recovery_specialist) edge=0
DAY 103: bets=30, 27, 27 || reasons=restore_blackjack_edge_after_breakage | smooth_ramp_edge_0(crafting_engineer) edge=0
DAY 104: bets=27, 30, 33 || reasons=restore_blackjack_edge_after_breakage | smooth_ramp_edge_0(crafting_engineer) edge=0
DAY 105: bets=34, 33 || reasons=restore_blackjack_edge_after_breakage | smooth_ramp_edge_0(baseline_random) edge=0 ; restore_blackjack_edge_after_breakage | smooth_ramp_edge_0(crafting_engineer) edge=0
DAY 106: bets=39, 35, 45 || reasons=restore_blackjack_edge_after_breakage | smooth_ramp_edge_0(crafting_engineer) edge=0 ; restore_blackjack_edge_after_breakage | smooth_ramp_edge_0(baseline_random) edge=0
DAY 107: bets=44, 49, 54 || reasons=restore_blackjack_edge_after_breakage | smooth_ramp_edge_0(crafting_engineer) edge=0
DAY 108: bets=48, 43 || reasons=restore_blackjack_edge_after_breakage | smooth_ramp_edge_0(crafting_engineer) edge=0
DAY 109: bets=58 || reasons=restore_blackjack_edge_after_breakage | smooth_ramp_edge_0(crafting_engineer) edge=0
DAY 110: bets=277, 248 || reasons=restore_blackjack_edge_after_breakage | smooth_ramp_edge_0(crafting_engineer) edge=0
DAY 111: bets=371, 371, 471 || reasons=restore_blackjack_edge_after_breakage | post_car_growth_push(baseline_random) edge=0 ; restore_blackjack_edge_after_breakage | post_car_growth_push(crafting_engineer) edge=0
DAY 112: bets=591, 910, 1156 || reasons=restore_blackjack_edge_after_breakage | post_car_growth_push(baseline_random) edge=0 ; restore_blackjack_edge_after_breakage | post_car_growth_push(crafting_engineer) edge=0
DAY 113: bets=844, 844, 616 || reasons=restore_blackjack_edge_after_breakage | post_car_growth_push(baseline_random) edge=0 ; restore_blackjack_edge_after_breakage | post_car_growth_push(crafting_engineer) edge=0
DAY 114: bets=783, 639 || reasons=restore_blackjack_edge_after_breakage | post_car_growth_push(crafting_engineer) edge=0
DAY 115: bets=811, 1249, 1586 || reasons=restore_blackjack_edge_after_breakage | post_car_growth_push(crafting_engineer) edge=0
DAY 116: bets=1158, 1783, 2265 || reasons=restore_blackjack_edge_after_breakage | post_car_growth_push(crafting_engineer) edge=0
DAY 117: bets=1351, 1493, 1337 || reasons=restore_blackjack_edge_after_breakage | smooth_ramp_edge_0(crafting_engineer) edge=0
DAY 118: bets=1693, 1654, 1481 || reasons=restore_blackjack_edge_after_breakage | smooth_ramp_edge_0(baseline_random) edge=0 ; restore_blackjack_edge_after_breakage | smooth_ramp_edge_0(crafting_engineer) edge=0
DAY 119: bets=1326, 1326, 3290 || reasons=restore_blackjack_edge_after_breakage | smooth_ramp_edge_0(crafting_engineer) edge=0 ; restore_blackjack_edge_after_breakage | post_car_growth_push(crafting_engineer) edge=0
DAY 120: bets=1701 || reasons=restore_blackjack_edge_after_breakage | smooth_ramp_edge_0(crafting_engineer) edge=0
DAY 121: bets=1694 || reasons=restore_blackjack_edge_after_breakage | smooth_ramp_edge_0(crafting_engineer) edge=0
DAY 122: bets=1760 || reasons=restore_blackjack_edge_after_breakage | smooth_ramp_edge_0(crafting_engineer) edge=0
DAY 123: bets=1701, 1879 || reasons=restore_blackjack_edge_after_breakage | smooth_ramp_edge_0(crafting_engineer) edge=0
DAY 124: bets=1682, 1506, 1348 || reasons=restore_blackjack_edge_after_breakage | smooth_ramp_edge_0(crafting_engineer) edge=0
DAY 125: bets=1870, 1826 || reasons=restore_blackjack_edge_after_breakage | smooth_ramp_edge_0(baseline_random) edge=0 ; restore_blackjack_edge_after_breakage | smooth_ramp_edge_0(crafting_engineer) edge=0
DAY 126: bets=1958 || reasons=restore_blackjack_edge_after_breakage | smooth_ramp_edge_0(crafting_engineer) edge=0
DAY 127: bets=2000, 1953, 1749 || reasons=restore_blackjack_edge_after_breakage | wealth_lock_preserve(crafting_engineer) edge=0 ; restore_blackjack_edge_after_breakage | smooth_ramp_edge_0(crafting_engineer) edge=0
DAY 128: bets=2000 || reasons=restore_blackjack_edge_after_breakage | wealth_lock_preserve(crafting_engineer) edge=0
DAY 129: bets=2100, 2600 || reasons=restore_blackjack_edge_after_breakage | wealth_lock_preserve(crafting_engineer) edge=0
DAY 130: bets=2600, 2300 || reasons=restore_blackjack_edge_after_breakage | wealth_lock_preserve(crafting_engineer) edge=0
DAY 131: bets=2500, 2200 || reasons=restore_blackjack_edge_after_breakage | wealth_lock_preserve(crafting_engineer) edge=0
DAY 132: bets=2400, 2100 || reasons=restore_blackjack_edge_after_breakage | wealth_lock_preserve(crafting_engineer) edge=0
DAY 133: bets=2200, 2400 || reasons=restore_blackjack_edge_after_breakage | wealth_lock_preserve(crafting_engineer) edge=0
DAY 134: bets=2100, 2071 || reasons=restore_blackjack_edge_after_breakage | wealth_lock_preserve(crafting_engineer) edge=0 ; restore_blackjack_edge_after_breakage | smooth_ramp_edge_0(crafting_engineer) edge=0
DAY 135: bets=1855, 1761 || reasons=restore_blackjack_edge_after_breakage | smooth_ramp_edge_0(crafting_engineer) edge=0
DAY 136: bets=1946, 2200, 2600 || reasons=restore_blackjack_edge_after_breakage | smooth_ramp_edge_0(crafting_engineer) edge=0 ; restore_blackjack_edge_after_breakage | wealth_lock_preserve(crafting_engineer) edge=0
DAY 137: bets=2900, 2900, 2900 || reasons=stabilize_health | wealth_lock_preserve(recovery_specialist) edge=0
DAY 138: bets=3500, 3100, 2800 || reasons=stabilize_health | wealth_lock_preserve(recovery_specialist) edge=0 ; stabilize_health | wealth_lock_preserve(baseline_random) edge=0
DAY 139: bets=2800, 2500, 2300 || reasons=stabilize_health | wealth_lock_preserve(recovery_specialist) edge=0
DAY 140: bets=2100, 1800, 2000 || reasons=stabilize_health | wealth_lock_preserve(recovery_specialist) edge=0 ; stabilize_health | drawdown_protection(recovery_specialist) edge=0
DAY 141: bets=2400, 2900 || reasons=restore_blackjack_edge_after_breakage | wealth_lock_preserve(crafting_engineer) edge=0
DAY 142: bets=2600, 2400, 2600 || reasons=restore_blackjack_edge_after_breakage | wealth_lock_preserve(crafting_engineer) edge=0
DAY 143: bets=3200, 2900 || reasons=restore_blackjack_edge_after_breakage | wealth_lock_preserve(baseline_random) edge=0 ; restore_blackjack_edge_after_breakage | wealth_lock_preserve(crafting_engineer) edge=0
DAY 144: bets=2900, 2900 || reasons=restore_blackjack_edge_after_breakage | wealth_lock_preserve(crafting_engineer) edge=0
DAY 145: bets=3200, 2900 || reasons=restore_blackjack_edge_after_breakage | wealth_lock_preserve(baseline_random) edge=0 ; restore_blackjack_edge_after_breakage | wealth_lock_preserve(crafting_engineer) edge=0
DAY 146: bets=2700, 2700, 2500 || reasons=restore_blackjack_edge_after_breakage | wealth_lock_preserve(crafting_engineer) edge=0
DAY 147: bets=2700, 2700, 3000 || reasons=restore_blackjack_edge_after_breakage | wealth_lock_preserve(crafting_engineer) edge=0
DAY 148: bets=3300, 3000, 2700 || reasons=restore_blackjack_edge_after_breakage | wealth_lock_preserve(baseline_random) edge=0 ; restore_blackjack_edge_after_breakage | wealth_lock_preserve(crafting_engineer) edge=0
DAY 149: bets=3200, 2900 || reasons=restore_blackjack_edge_after_breakage | wealth_lock_preserve(crafting_engineer) edge=0
DAY 150: bets=1600 || reasons=restore_blackjack_edge_after_breakage | drawdown_protection(baseline_random) edge=0
DAY 151: bets=1800, 2081, 2081 || reasons=restore_blackjack_edge_after_breakage | drawdown_protection(crafting_engineer) edge=0 ; restore_blackjack_edge_after_breakage | smooth_ramp_edge_0(crafting_engineer) edge=0
DAY 152: bets=2400, 2600, 2300 || reasons=restore_blackjack_edge_after_breakage | wealth_lock_preserve(crafting_engineer) edge=0 ; restore_blackjack_edge_after_breakage | wealth_lock_preserve(baseline_random) edge=0
DAY 153: bets=2100, 2035, 2100 || reasons=restore_blackjack_edge_after_breakage | wealth_lock_preserve(crafting_engineer) edge=0 ; restore_blackjack_edge_after_breakage | smooth_ramp_edge_0(crafting_engineer) edge=0
DAY 154: bets=2300, 2100, 2300 || reasons=restore_blackjack_edge_after_breakage | wealth_lock_preserve(crafting_engineer) edge=0 ; restore_blackjack_edge_after_breakage | wealth_lock_preserve(baseline_random) edge=0
DAY 155: bets=2500, 2800, 3000 || reasons=restore_blackjack_edge_after_breakage | wealth_lock_preserve(crafting_engineer) edge=0
DAY 156: bets=2700, 2500, 2700 || reasons=restore_blackjack_edge_after_breakage | wealth_lock_preserve(crafting_engineer) edge=0
DAY 157: bets=3000, 2700 || reasons=restore_blackjack_edge_after_breakage | wealth_lock_preserve(crafting_engineer) edge=0
DAY 158: bets=3000, 3000, 2700 || reasons=restore_blackjack_edge_after_breakage | wealth_lock_preserve(crafting_engineer) edge=0
DAY 159: bets=3200, 3500, 3200 || reasons=preserve_companion_roster | wealth_lock_preserve(baseline_random) edge=0 ; restore_blackjack_edge_after_breakage | wealth_lock_preserve(crafting_engineer) edge=0
DAY 160: bets=3500, 3800, 3500 || reasons=restore_blackjack_edge_after_breakage | wealth_lock_preserve(crafting_engineer) edge=0
DAY 161: bets=3800, 4200, 4600 || reasons=restore_blackjack_edge_after_breakage | wealth_lock_preserve(crafting_engineer) edge=0
DAY 162: bets=5100, 5600, 5000 || reasons=preserve_companion_roster | wealth_lock_preserve(companion_collector) edge=0 ; restore_blackjack_edge_after_breakage | wealth_lock_preserve(crafting_engineer) edge=0
DAY 163: bets=4500, 4500, 5000 || reasons=restore_blackjack_edge_after_breakage | wealth_lock_preserve(crafting_engineer) edge=0
```

## Late Window: Day 159 To Day 164

Cycle summary from the replay:

- Day `159`: `$30,185 -> $32,585`
- Day `160`: `$32,585 -> $35,485`
- Day `161`: `$35,485 -> $38,685`
- Day `162`: `$38,685 -> $51,285`
- Day `163`: `$51,285 -> $45,785`
- Day `164`: `$45,785 -> $0`

Late betting behavior from the trace was dominated by `wealth_lock_preserve(...)` bets with `edge=0`, including stake sizes around `$3,500`, `$3,800`, `$4,200`, `$4,500`, `$5,000`, `$5,100`, and `$5,600`.

That means the bot was still risking roughly ten percent chunks of bankroll even though it had no item-driven edge and no millionaire-conversion path active.

## Which Decisions Should Have Been Different

### 1. Strategy, not hand-play, should have changed before day 164

No individual blackjack action stands out as the decisive blunder. The damaging pattern was letting the run sit in a high-cash, no-conversion state instead of buying protection or pushing into a real millionaire route.

The run ended day `164` with:

- no `Animal Whistle`
- no `Delight Indicator` or `Delight Manipulator`
- no millionaire visit/conversion state
- no route activity late in the run

That is the real failure. By the time Betsy Army fires, the run has no safe answer left.

### 2. The final Betsy decision was logged under the wrong policy branch

The autoplay trace recorded the last choice as `betsy_hungry_budget_gate`, but the actual event was the cow-army finale.

Why that matters:

- All three Betsy prompts share the raw prompt `Moo?`
- The yes/no policy in `event_policy.py` disambiguates using recent-text markers
- The stage-2 finale text says `Do you feed Betsy and her friends?`, not `army` or `100,000` before the choice is made
- So the trace fell through to the cheap `$100` hungry-cow handler even though the event was the `$100,000` finale

This mismatch did not create a winning alternative for this seed, but it did prove the policy was reasoning about the wrong event class at the final prompt.

### 3. The bot preserved bankroll too loosely at `$30k-$55k`

From day `159` onward the run kept placing large bets under `wealth_lock_preserve(...)` even with `edge=0`.

That should have been different.

At that stage, better play would have been one of these:

- switch from wealth-lock betting to stronger capital preservation when no edge item exists
- route into conversion or protection instead of continuing table-only growth
- prioritize items that neutralize future animal/dealer/event spikes instead of treating `$50k` as stable wealth

### 4. The first two Betsy prompts were not the real pivot

The run also answered:

- day `133`: `yes`, `betsy_hungry_budget_gate`
- day `150`: `yes`, `betsy_tractor_budget_gate`

Those are expensive, but they are not obviously the wrong local choices:

- refusing the day-150 tractor event causes an `80` damage hit and `Fractured Spine`
- the Betsy storyline also advances before the prompt branch resolves

So the local prompt answers were defensible. The problem was never developing a Betsy-safe state before the finale arrived.

## Blackjack Verdict

This replay does not read like a hand-strategy failure.

It reads like this:

- the blackjack actions were mostly routine and coherent
- the bets were too large for an `edge=0` lock-preservation regime
- the run never converted its midgame money into safety or a true win condition
- the Betsy finale then converted that strategic weakness into an unavoidable terminal prompt

## Bottom Line

The run did not really die because of one bad click on day `164`.

It died because it reached a forced-loss storyline checkpoint with too much money to still be playing passively, and not enough money or protection to survive the checkpoint.

If you want the next patch target after this audit, it is not basic blackjack action logic. It is late-game bankroll conversion and event-risk protection when the bot is sitting in the `$30k-$100k` band without a real edge item.