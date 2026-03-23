from __future__ import annotations

from dataclasses import dataclass, field

from .state import GameState


@dataclass(frozen=True)
class StrategicPlan:
    goal: str
    scores: dict[str, float] = field(default_factory=dict)
    reason: str = ""

    def to_dict(self) -> dict[str, object]:
        return {
            "goal": self.goal,
            "scores": dict(self.scores),
            "reason": self.reason,
        }


def choose_strategic_goal(game_state: GameState) -> StrategicPlan:
    scores: dict[str, float] = {}

    def score(goal: str, value: float) -> None:
        scores[goal] = scores.get(goal, 0.0) + value

    if not game_state.alive:
        return StrategicPlan(goal="run_ended", scores={"run_ended": 1.0}, reason="player is no longer alive")

    health = game_state.health
    sanity = game_state.sanity
    fatigue = game_state.fatigue
    injuries = len(game_state.injuries)
    statuses = len(game_state.statuses)
    companion_pressure = game_state.companion_low_happiness_count * 12.0 + game_state.companion_runaway_risk_count * 22.0
    debt_pressure = min(70.0, game_state.loan_warning_level * 18.0 + game_state.loan_debt / 600.0)
    bankroll_pressure = 180.0 if game_state.bankroll_emergency else (54.0 if game_state.fragile_post_car else 0.0)
    store_pressure = min(
        78.0,
        game_state.store_best_purchase_priority * 0.55
        + game_state.store_candidate_count * 4.0
        + max(0, game_state.companion_count - game_state.inventory_food_count) * 8.0,
    )
    pawn_pressure = min(
        84.0,
        game_state.pawn_planned_sale_value / 8.0
        + game_state.pawn_planned_sale_count * 6.0
        + max(0.0, 380.0 - game_state.balance) / 18.0,
    )
    midgame_growth_window = (
        game_state.has_car
        and game_state.rank <= 1
        and 1200 <= game_state.balance < 10000
        and game_state.health >= 65
        and game_state.sanity >= 34
        and game_state.store_best_purchase_priority < 90
        and game_state.store_target_spend <= max(180.0, game_state.balance * 0.08)
    )
    growth_push_window = (
        game_state.has_car
        and health >= 62
        and sanity >= 32
        and fatigue < 76
        and injuries <= 2
        and statuses <= 2
        and (
            (game_state.rank <= 1 and 1000 <= game_state.balance < 20000)
            or (
                game_state.rank == 2
                and 15000 <= game_state.balance < 120000
                and health >= 78
                and sanity >= 52
                and fatigue < 62
                and injuries == 0
                and statuses <= 1
                and game_state.loan_debt <= 0
                and game_state.loan_warning_level <= 0
            )
        )
    )

    late_breakout_threat = (
        game_state.rank >= 2
        and game_state.balance >= 10000
        and (
            health < 80
            or sanity < 58
            or injuries > 0
            or statuses > 1
            or game_state.loan_debt > 0
            or game_state.loan_warning_level > 0
        )
    )

    score("survive_emergency", max(0.0, 55.0 - health) * 3.0)
    score("survive_emergency", max(0.0, 30.0 - sanity) * 2.4)
    score("survive_emergency", injuries * 9.0 + statuses * 6.0)
    score("survive_emergency", bankroll_pressure)
    if fatigue >= 88:
        score("survive_emergency", 16.0)
    if game_state.bankroll_emergency:
        score("stabilize_health", 46.0)
        score("contain_debt_escalation", 64.0)
        score("cashout_pawn_inventory", 42.0)
        score("reduce_debt_risk", 38.0)
    elif game_state.fragile_post_car:
        score("stabilize_health", 18.0)
        score("contain_debt_escalation", 20.0)
        score("cashout_pawn_inventory", 18.0)

    score("stabilize_health", max(0.0, 72.0 - health) * 1.6)
    score("stabilize_health", injuries * 7.0 + statuses * 5.0)
    if game_state.has_car and health < 68:
        score("stabilize_health", 22.0)
    if game_state.has_car and (injuries >= 1 or statuses >= 2):
        score("stabilize_health", 16.0)
    score("stabilize_sanity", max(0.0, 48.0 - sanity) * 1.8)
    if game_state.has_car and sanity < 40:
        score("stabilize_sanity", 24.0)
    if game_state.has_car and sanity < 50:
        score("stabilize_sanity", 14.0)

    if game_state.opportunity_flags.get("can_reduce_fatigue_pressure"):
        score("reduce_fatigue_pressure", max(0.0, fatigue - 58.0) * 1.8)
        if fatigue >= 82:
            score("reduce_fatigue_pressure", 28.0)

    if game_state.opportunity_flags.get("can_preserve_companions"):
        score("preserve_companion_roster", companion_pressure)
        if game_state.inventory_food_count < game_state.companion_count:
            score("preserve_companion_roster", (game_state.companion_count - game_state.inventory_food_count) * 7.0)

    if game_state.opportunity_flags.get("can_restock_supplies"):
        score("restock_supplies", store_pressure)
        if game_state.health < 72 or game_state.sanity < 36:
            score("restock_supplies", 12.0)
        if game_state.inventory_food_count < game_state.companion_count:
            score("restock_supplies", 16.0)
        if not game_state.has_car and game_state.balance < 140:
            score("restock_supplies", -18.0)
        if midgame_growth_window:
            score("restock_supplies", -20.0)
        if growth_push_window and game_state.store_best_purchase_priority < 92:
            score("restock_supplies", -24.0)
        if growth_push_window and game_state.store_target_spend <= max(260.0, game_state.balance * 0.10):
            score("restock_supplies", -18.0)

    if game_state.opportunity_flags.get("can_contain_debt_escalation"):
        score("contain_debt_escalation", debt_pressure + 28.0)

    if game_state.opportunity_flags.get("can_cashout_pawn_inventory"):
        score("cashout_pawn_inventory", pawn_pressure)
        if not game_state.has_car:
            score("cashout_pawn_inventory", 12.0)
        if game_state.loan_debt > 0:
            score("cashout_pawn_inventory", 10.0)
        if game_state.health < 72 or game_state.sanity < 36:
            score("cashout_pawn_inventory", 8.0)

    if not game_state.has_car:
        score("acquire_car", 70.0)
        score("bootstrap_blackjack_edge", 20.0)
        if game_state.balance >= 120:
            score("acquire_car", 14.0)
        if game_state.balance >= 200:
            score("acquire_car", 12.0)
    else:
        score("push_next_rank", 10.0)

    if game_state.opportunity_flags.get("can_reduce_debt_risk"):
        score("reduce_debt_risk", 40.0 + min(30.0, game_state.loan_warning_level * 10.0))
        if game_state.loan_debt > 0:
            score("reduce_debt_risk", min(20.0, game_state.loan_debt / 1000.0))

    if late_breakout_threat:
        score("stabilize_health", 26.0)
        score("stabilize_sanity", 30.0)
        score("push_next_rank", -42.0)
        score("exploit_marvin", -24.0)
        score("exploit_adventure", -28.0)
        if game_state.loan_debt > 0 or game_state.loan_warning_level > 0:
            score("reduce_debt_risk", 26.0)
            score("contain_debt_escalation", 18.0)

    if game_state.fraudulent_cash > 0:
        score("blend_fraudulent_cash_safely", 45.0 + min(20.0, game_state.fraudulent_cash / 1000.0))

    if game_state.opportunity_flags.get("can_visit_marvin"):
        # Deep run Marvin boost: if balance > $10k and rank >= 2, make Marvin top priority
        if game_state.rank >= 2 and game_state.balance > 10000:
            score("exploit_marvin", 120.0 + min(60.0, game_state.marvin_affordable_priority * 0.7))
            if game_state.marvin_affordable_priority >= 72:
                score("exploit_marvin", 40.0)
            if game_state.marvin_affordable_priority >= 84:
                score("exploit_marvin", 30.0)
            if game_state.marvin_candidate_price > game_state.balance and game_state.marvin_candidate_price <= game_state.balance + 20000:
                score("exploit_marvin", 24.0)
        else:
            score("exploit_marvin", 16.0 + min(40.0, game_state.marvin_affordable_priority * 0.5))
            if game_state.rank <= 1:
                score("exploit_marvin", 14.0)
                if game_state.has_met_vinnie and game_state.loan_debt == 0 and 1000 <= game_state.balance < 8000:
                    score("exploit_marvin", 24.0)
                if game_state.has_worn_map and not game_state.has_map and game_state.balance >= 1200:
                    score("exploit_marvin", 22.0)
                if game_state.marvin_affordable_priority >= 56 and game_state.balance >= 1800:
                    score("exploit_marvin", 18.0)
                if 1200 <= game_state.balance < 10000 and game_state.health >= 62 and game_state.sanity >= 34:
                    score("exploit_marvin", 14.0)
                if game_state.marvin_candidate_price > game_state.balance and game_state.marvin_candidate_price <= game_state.balance + 5000:
                    score("exploit_marvin", 16.0)
                if game_state.marvin_future_priority >= 56 and 0 < game_state.marvin_future_shortfall <= 5000 and game_state.balance >= 950:
                    score("exploit_marvin", 24.0)
                    if game_state.has_met_vinnie and game_state.loan_debt == 0:
                        score("exploit_marvin", 18.0)
            if fatigue < 72 and sanity >= 32:
                score("exploit_marvin", 6.0)
            if game_state.marvin_strong_window and game_state.marvin_candidate_price >= 10_000:
                score("exploit_marvin", 18.0)
            if game_state.rank >= 2 and game_state.balance >= 7000 and game_state.marvin_affordable_priority >= 72:
                score("exploit_marvin", 18.0)
            if game_state.rank >= 2 and game_state.marvin_future_priority >= 76 and 0 < game_state.marvin_future_shortfall <= 12000 and game_state.balance >= 7000:
                score("exploit_marvin", 16.0)
            # Extra boost when the best affordable item is genuinely high-priority (≥84).
            # Ensures Marvin beats routine store restocking even if marvin_strong_window is
            # False (e.g. exact $10k balance where condition 3 just barely fails by $100).
            if game_state.marvin_affordable_priority >= 84:
                score("exploit_marvin", 14.0)
            if game_state.rank <= 1 and game_state.marvin_affordable_priority >= 72:
                score("exploit_marvin", 12.0)
            # Items reduce blackjack variance and guarantee earnings — prioritize buying
            # first items when the bot has a car but low edge_score.
            if game_state.edge_score < 4 and game_state.rank >= 1 and game_state.marvin_affordable_priority >= 56:
                score("exploit_marvin", 20.0)
            if game_state.edge_score < 8 and game_state.rank >= 2 and game_state.marvin_affordable_priority >= 60:
                score("exploit_marvin", 16.0)
            if growth_push_window:
                score("exploit_marvin", 18.0)
                if game_state.marvin_candidate_price > game_state.balance and game_state.marvin_candidate_price <= game_state.balance + 10_000:
                    score("exploit_marvin", 16.0)
                if game_state.marvin_affordable_priority >= 72:
                    score("exploit_marvin", 10.0)
            if game_state.fragile_post_car:
                score("exploit_marvin", -36.0)
            if game_state.bankroll_emergency:
                score("exploit_marvin", -70.0)
    elif game_state.has_car and not game_state.has_marvin_access:
        score("unlock_marvin", 22.0)

    if game_state.opportunity_flags.get("can_recover_from_car_trouble"):
        score("recover_from_car_trouble", 56.0 + len(game_state.travel_restrictions) * 8.0)

    if game_state.opportunity_flags.get("can_advance_mechanic_arc"):
        score("advance_mechanic_arc", 40.0)
        if game_state.fragile_post_car:
            score("advance_mechanic_arc", -26.0)
        if game_state.bankroll_emergency:
            score("advance_mechanic_arc", -60.0)

    if game_state.opportunity_flags.get("can_repair_or_upgrade"):
        score("repair_or_upgrade_gear", 24.0 + len(game_state.broken_items) * 8.0)
        if growth_push_window:
            score("repair_or_upgrade_gear", 14.0)
        if game_state.fragile_post_car:
            score("repair_or_upgrade_gear", -18.0)
        if game_state.bankroll_emergency:
            score("repair_or_upgrade_gear", -42.0)

    if game_state.opportunity_flags.get("can_restore_blackjack_edge"):
        score("restore_blackjack_edge_after_breakage", 30.0 + len(game_state.broken_items) * 12.0 + len(game_state.repairing_items) * 6.0)
        if growth_push_window:
            score("restore_blackjack_edge_after_breakage", 12.0)

    if game_state.opportunity_flags.get("can_adventure_safely"):
        if game_state.rank >= 2:
            score("exploit_adventure", 18.0)
            # At rank 2+ with adventure safe, also boost push_next_rank so the planner
            # considers adventure as a valid push-forward action.
            score("push_next_rank", 8.0)
        else:
            score("reach_adventure_threshold", 16.0)

    # Proactive borrowing: when Vinnie is available and balance is low, score
    # push_next_rank higher so the loan route beats the convenience store.
    if game_state.opportunity_flags.get("can_borrow_to_bootstrap"):
        score("push_next_rank", 26.0)
        if game_state.rank <= 1 and 1200 <= game_state.balance < 10000 and game_state.has_marvin_access:
            score("push_next_rank", 18.0)
            score("exploit_marvin", 18.0)
            if game_state.has_met_vinnie and game_state.loan_debt == 0 and game_state.marvin_affordable_priority >= 44:
                score("push_next_rank", 24.0)
                score("exploit_marvin", 22.0)
            if game_state.has_met_vinnie and game_state.loan_debt == 0 and game_state.marvin_future_priority >= 56 and 0 < game_state.marvin_future_shortfall <= 5000:
                score("push_next_rank", 22.0)
                score("exploit_marvin", 24.0)
        if growth_push_window:
            score("push_next_rank", 18.0)

    if game_state.opportunity_flags.get("can_convert_millionaire_to_ending"):
        score("convert_millionaire_to_ending", 200.0)

    if game_state.rank == 0:
        score("push_next_rank", 24.0)
    elif game_state.rank == 1:
        score("push_next_rank", 20.0)
    elif game_state.rank == 2:
        score("push_next_rank", 12.0)
    if midgame_growth_window:
        score("push_next_rank", 12.0)
    if growth_push_window:
        score("push_next_rank", 24.0)
        if game_state.has_marvin_access:
            score("push_next_rank", 10.0)
        if game_state.rank <= 1 and game_state.balance < 12000:
            score("push_next_rank", 12.0)

    if fatigue >= 70:
        score("push_next_rank", -12.0)
        score("exploit_adventure", -20.0)
    if game_state.bankroll_emergency:
        score("push_next_rank", -34.0)
        score("exploit_adventure", -80.0)
        score("unlock_marvin", -40.0)
    elif game_state.fragile_post_car:
        score("push_next_rank", -10.0)
        score("exploit_adventure", -26.0)
    if companion_pressure > 0:
        score("exploit_adventure", -10.0)
    if debt_pressure >= 40.0:
        score("exploit_marvin", -8.0)
    if game_state.store_target_spend > 0:
        if growth_push_window and game_state.store_best_purchase_priority < 92 and game_state.store_target_spend <= max(260.0, game_state.balance * 0.10):
            score("push_next_rank", -min(4.0, game_state.store_target_spend / 60.0))
        else:
            score("push_next_rank", -min(12.0, game_state.store_target_spend / 20.0))
    if game_state.pawn_planned_sale_value > 0 and game_state.balance < 450:
        score("push_next_rank", -10.0)

    candidate_goals = game_state.current_progress_goal_candidates or ("bootstrap_blackjack_edge",)
    filtered_scores = {goal: scores.get(goal, 0.0) for goal in candidate_goals}
    best_goal = max(filtered_scores, key=lambda goal: (filtered_scores[goal], goal))
    reason = f"highest scored goal {best_goal}={filtered_scores[best_goal]:.1f}"
    return StrategicPlan(goal=best_goal, scores=filtered_scores, reason=reason)