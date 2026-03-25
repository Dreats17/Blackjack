# PERSONALITIES PLANNING

Purpose: make the personality system immediately actionable using the existing autoplay architecture in tools.

This plan assumes implementation will use these files directly:
- tools/autoplay/personalities.py
- tools/autoplay/personality_manager.py
- tools/autoplay/planner.py
- tools/autoplay/route_policy.py
- tools/autoplay/scenario_cases.py

---

## 1) Current System Snapshot (Do Not Rebuild)

The meta-controller already exists in practice across planner + personality_manager.

Current flow:
1. planner.choose_strategic_goal computes goal scores.
2. personality_manager.get_for_state(goal, game_state) picks a personality with state overrides and optional exploration.
3. StrategicPlan carries personality to policy modules.
4. route_policy.choose_route_option uses goal alignment plus metadata and applies personality.adventure_bias.

Action rule:
- improve this existing pipeline instead of adding a brand-new controller class.

---

## 2) Live Personality Inventory

From tools/autoplay/personalities.py:
- survival_conservative
- wealth_aggro
- ending_hunter
- companion_collector
- crafting_engineer
- debt_gambler
- recovery_specialist
- baseline_random

Key fields already available for tuning:
- bet_aggression
- drawdown_protection
- health_caution
- marvin_aggression
- frugal_mode
- prefer_safe_events
- adventure_bias
- objective_function
- hard_constraints
- risk_tolerance
- switch_triggers
- exploration_probability
- safety_min_health
- safety_min_sanity
- safety_max_warning
- safety_reserve_fraction

Implementation note:
- stage behavior should be expressed by remapping goals to these personalities and tuning these fields, not by creating duplicate profiles with new names.

---

## 3) Live Goal-to-Personality Wiring

From tools/autoplay/personality_manager.py _GOAL_TO_PERSONALITY:
- survive_emergency -> recovery_specialist
- stabilize_health, stabilize_sanity -> recovery_specialist
- reduce_debt_risk, contain_debt_escalation, cashout_pawn_inventory -> debt_gambler
- acquire_car, bootstrap_blackjack_edge, push_next_rank, exploit_adventure, reach_adventure_threshold, exploit_marvin, unlock_marvin -> wealth_aggro
- advance_mechanic_arc, convert_millionaire_to_ending -> ending_hunter
- repair_or_upgrade_gear, restore_blackjack_edge_after_breakage, recover_from_car_trouble, restock_supplies -> crafting_engineer
- preserve_companion_roster -> companion_collector

State override rules already in place:
- low health/sanity or stacked injuries/statuses -> recovery_specialist
- high warning/debt -> debt_gambler
- millionaire conversion state -> ending_hunter

Actionable change target:
- tune mapping and thresholds first to fix startup failures before adding any new personalities.

---

## 4) Startup Failure Fix Plan (Priority)

Observed issue: many runs fail to launch early.

### A) Bootstrap lock for no-car phase

Where:
- tools/autoplay/personality_manager.py
- tools/autoplay/planner.py

What to change:
- force no-car goals (acquire_car, bootstrap_blackjack_edge) to prefer survival_conservative until a minimum cash floor is reached.
- switch to wealth_aggro only after floor condition passes.

Suggested floor:
- balance >= 220 and health >= 60 and sanity >= 35.

### B) Debt personality over-aggression

Where:
- tools/autoplay/personality_manager.py
- tools/autoplay/personalities.py

What to change:
- for warning >= 2 in rank 0-1, override to recovery_specialist instead of debt_gambler unless debt is already critical.
- keep debt_gambler for warning >= 3 or debt >= 20000.

Why:
- early debt resolution behavior should not trigger high-risk recovery loops.

### C) Route scoring for fragile starts

Where:
- tools/autoplay/route_policy.py

What to change:
- increase penalties on mechanic/marvin/adventure routes during bankroll_emergency and fragile_post_car windows.
- increase weight for stay_home, doctor, pawn, and loan when cash floor not met.

Why:
- this directly addresses runs that repeatedly choose non-launch actions.

---

## 5) Route Metadata Contract (Use Existing Keys)

When building DecisionRequest metadata for route decisions, keep these keys populated because route_policy already uses them:
- urgent_medical
- wants_doctor
- needs_recovery_day
- wants_store
- store_spend
- store_actionable_count
- wants_pawn
- pawn_value
- wants_loan
- loan_pressure
- wants_marvin
- marvin_priority
- marvin_future_priority
- marvin_future_shortfall
- wants_mechanic
- mechanic_urgency
- wants_upgrade
- wants_workbench_craft
- upgrade_urgency
- wants_adventure
- adventure_readiness
- planner_goal
- catalog_push_active
- catalog_push_kind
- catalog_push_spend
- catalog_push_count
- catalog_push_priority
- poverty_loan_mode

Actionable requirement:
- if a key is unknown at call site, set it to zero/false explicitly; do not omit.

---

## 6) Scenario Cases: Make It Enforceable

Use tools/autoplay/scenario_cases.py as the acceptance suite for personality routing.

Existing high-value startup scenarios already present:
- saveable_doctor_death
- no_car_store_hints_do_not_create_store_goal
- low_cash_marvin_access_does_not_force_marvin_goal
- healthy_midgame_store_pressure_defers_to_rank_push
- debt_pressure_case
- high_fatigue_missed_event_case

Add new startup stability scenarios now:
1. no_car_low_health_prefers_recovery_specialist
2. warning_two_rank_one_avoids_debt_gambler
3. bankroll_emergency_prefers_liquidity_routes
4. early_unlock_delay_prioritizes_store_or_loan
5. fragile_post_car_avoids_adventure_branch

Pass criteria per scenario:
- expected strategic goal,
- expected route choice,
- expected max/min bet band where relevant.

---

## 7) Stage Model Using Existing Personalities

Use this mapping for stage behavior (no new profile names needed):

- Bootstrap stage (rank 0-1, no car or fragile cash): survival_conservative or recovery_specialist
- Launch stage (car online, rank <= 1): wealth_aggro only when vitals and reserve floors are safe
- Control stage (rank 2 stable): crafting_engineer or wealth_aggro depending on objective
- Debt containment stage: debt_gambler only when debt pressure is truly high
- Ending conversion stage: ending_hunter
- Companion route stage: companion_collector
- Exploration/coverage stage: baseline_random by exploration_probability only

---

## 8) Metrics and Logging (Use Current Outputs)

Use existing summary outputs in tools for validation:
- tools/test_out.txt
- tools/cumulative_test_out.txt

Track at minimum:
- bootstrap success rate by day threshold,
- day-to-car and day-to-rank-2 median,
- warning-tier >= 2 incidence before day 20,
- bankruptcy/death before day 20,
- scenario suite pass rate by suite type.

For each decision trace, include:
- goal
- personality
- reason_code
- objective_function
- safety thresholds hit
- switch reason (goal_max_score, exploration_switch, constraint reason)

---

## 9) Immediate Implementation Order

1. Tune personality_manager override thresholds for early-game safety.
2. Tune no-car and fragile-post-car scoring in route_policy.
3. Adjust survival_conservative and recovery_specialist parameter values in personalities.
4. Add the five new startup scenarios in scenario_cases.
5. Run scenario suite and batch validation; compare startup metrics.
6. Only after startup improves, retune wealth_aggro and debt_gambler for speed.

---

## 10) Ready-to-Hand Off Tasks For The Other Bot

Task 1:
- edit tools/autoplay/personality_manager.py
- implement safer rank 0-1 override logic and debt-gating rules.

Task 2:
- edit tools/autoplay/route_policy.py
- increase liquidity-route bias in bankroll_emergency and fragile_post_car windows.

Task 3:
- edit tools/autoplay/personalities.py
- tighten startup safety defaults for survival_conservative and recovery_specialist.

Task 4:
- edit tools/autoplay/scenario_cases.py
- add startup scenarios and explicit assertions for goal + route + bet limits.

Task 5:
- run validation suite and update tools/test_out.txt and tools/cumulative_test_out.txt with latest run results.

This ordering is optimized for your stated problem: getting more runs to launch successfully under scenario-driven alternative routing.
