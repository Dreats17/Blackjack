from __future__ import annotations

from dataclasses import dataclass, field
import random

from .personalities import DEFAULT_PERSONALITY, PERSONALITY_SET_VERSION, Personality
from .state import GameState
from .tuning import tval


@dataclass(frozen=True)
class StrategicPlan:
    goal: str
    scores: dict[str, float] = field(default_factory=dict)
    reason: str = ""
    personality: Personality = field(default_factory=lambda: DEFAULT_PERSONALITY)
    reason_code: str = "goal_max_score"
    objective_value: float = 0.0
    personality_version: str = PERSONALITY_SET_VERSION

    def to_dict(self) -> dict[str, object]:
        return {
            "goal": self.goal,
            "scores": dict(self.scores),
            "reason": self.reason,
            "personality": self.personality.name,
            "reason_code": self.reason_code,
            "objective_value": self.objective_value,
            "personality_version": self.personality_version,
            "risk_tolerance": self.personality.risk_tolerance,
            "objective_function": self.personality.objective_function,
            "hard_constraints": list(self.personality.hard_constraints),
            "switch_triggers": list(self.personality.switch_triggers),
        }


def _goal_objective_bonus(goal: str, game_state: GameState, personality: Personality) -> float:
    health = game_state.health
    sanity = game_state.sanity
    debt = game_state.loan_debt
    warning = game_state.loan_warning_level
    companion_count = game_state.companion_count
    has_marvin_access = game_state.has_marvin_access
    has_car = game_state.has_car
    rank = game_state.rank
    balance = game_state.balance

    # Objective-driven nudges that preserve existing heuristics but make each
    # personality explicit about what "good" looks like.
    if personality.objective_function == "maximize_days_alive_minimize_medical_crises":
        if goal in {"survive_emergency", "stabilize_health", "stabilize_sanity", "reduce_fatigue_pressure"}:
            return 26.0
        if goal in {"exploit_adventure", "push_next_rank"} and (health < 60 or sanity < 35):
            return -24.0
    elif personality.objective_function == "maximize_bankroll_growth_rate":
        if goal in {"push_next_rank", "bootstrap_blackjack_edge", "exploit_adventure", "exploit_marvin"}:
            return 18.0
        if goal in {"stabilize_health", "stabilize_sanity"} and (health > 70 and sanity > 45):
            return -8.0
    elif personality.objective_function == "maximize_branch_prerequisites_and_lock_points":
        if goal in {"advance_mechanic_arc", "convert_millionaire_to_ending", "repair_or_upgrade_gear"}:
            return 20.0
    elif personality.objective_function == "maximize_companion_count_and_sanctuary_readiness":
        if goal in {"preserve_companion_roster", "restock_supplies", "reach_adventure_threshold"}:
            return 18.0
        if companion_count >= 5 and goal == "convert_millionaire_to_ending":
            return 12.0
    elif personality.objective_function == "maximize_recipe_depth_and_tier_progression":
        if goal in {"restock_supplies", "repair_or_upgrade_gear", "restore_blackjack_edge_after_breakage"}:
            return 16.0
    elif personality.objective_function == "stress_test_loan_and_fraud_systems":
        if goal in {"reduce_debt_risk", "contain_debt_escalation", "blend_fraudulent_cash_safely", "push_next_rank"}:
            return 14.0
        if warning >= personality.safety_max_warning and goal in {"exploit_adventure", "exploit_marvin"}:
            return -18.0
    elif personality.objective_function == "maximize_recovery_from_damaged_state":
        if goal in {"survive_emergency", "stabilize_health", "stabilize_sanity", "reduce_debt_risk"}:
            return 28.0
        if goal in {"exploit_adventure", "exploit_marvin", "push_next_rank"} and (health < 62 or sanity < 38):
            return -26.0

    # Lightweight global nudges to keep the objective model grounded in state.
    bonus = 0.0
    if debt > 0 and goal in {"reduce_debt_risk", "contain_debt_escalation"}:
        bonus += min(14.0, debt / 2500.0)
    if warning >= 2 and goal in {"exploit_adventure", "push_next_rank"}:
        bonus -= 10.0
    if has_car and has_marvin_access and rank <= 1 and goal == "exploit_marvin":
        bonus += 6.0
    if balance < 140 and goal == "acquire_car":
        bonus += 8.0
    return bonus


def _apply_hard_constraints(goal: str, game_state: GameState, personality: Personality) -> tuple[str, str]:
    health = game_state.health
    sanity = game_state.sanity
    warning = game_state.loan_warning_level
    debt = game_state.loan_debt
    balance = max(1, game_state.balance)
    reserve_floor = int(balance * personality.safety_reserve_fraction)

    aggressive_goals = {
        "exploit_adventure",
        "push_next_rank",
        "exploit_marvin",
        "bootstrap_blackjack_edge",
    }

    if health <= personality.safety_min_health or sanity <= personality.safety_min_sanity:
        if goal != "survive_emergency":
            return "survive_emergency", "constraint:low_vitals"

    if warning > personality.safety_max_warning and goal in aggressive_goals:
        return "reduce_debt_risk", "constraint:warning_cap"

    if debt > 0 and goal == "exploit_adventure" and personality.risk_tolerance == "low":
        return "reduce_debt_risk", "constraint:debt_vs_adventure"

    if game_state.bankroll_emergency and goal in aggressive_goals:
        return "contain_debt_escalation", "constraint:bankroll_emergency"

    if reserve_floor > balance and goal in {"exploit_adventure", "exploit_marvin"}:
        return "stabilize_health", "constraint:reserve_floor"

    return goal, "goal_max_score"


def _maybe_explore_goal(candidates: tuple[str, ...], best_goal: str, personality: Personality) -> tuple[str, str]:
    if len(candidates) <= 1:
        return best_goal, "goal_max_score"
    if personality.exploration_probability <= 0:
        return best_goal, "goal_max_score"
    if random.random() >= personality.exploration_probability:
        return best_goal, "goal_max_score"

    alternatives = [goal for goal in candidates if goal != best_goal]
    if not alternatives:
        return best_goal, "goal_max_score"
    return random.choice(alternatives), "exploration_switch"


def choose_strategic_goal(game_state: GameState) -> StrategicPlan:
    from .personality_manager import personality_manager

    scores: dict[str, float] = {}

    def score(goal: str, value: float) -> None:
        scores[goal] = scores.get(goal, 0.0) + value

    if not game_state.alive:
        p = personality_manager.get_for_state("run_ended", game_state)
        return StrategicPlan(
            goal="run_ended",
            scores={"run_ended": 1.0},
            reason="player is no longer alive",
            personality=p,
            reason_code="terminal:run_ended",
            objective_value=1.0,
        )

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
        score("acquire_car", float(tval("planner.no_car.acquire_car_base", 80.0)))
        score("bootstrap_blackjack_edge", float(tval("planner.no_car.bootstrap_edge_base", 30.0)))
        if game_state.balance >= 120:
            score("acquire_car", float(tval("planner.no_car.acquire_bonus_120", 28.0)))
        if game_state.balance >= 200:
            score("acquire_car", float(tval("planner.no_car.acquire_bonus_200", 24.0)))
    else:
        score("push_next_rank", 38.0)

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
        # Aggressive Marvin: make it a top priority at ALL ranks with healthy balance
        if game_state.rank >= 2 and game_state.balance > 10000:
            score("exploit_marvin", 180.0 + min(80.0, game_state.marvin_affordable_priority * 1.2))
            if game_state.marvin_affordable_priority >= 72:
                score("exploit_marvin", 60.0)
            if game_state.marvin_affordable_priority >= 84:
                score("exploit_marvin", 50.0)
            if game_state.marvin_candidate_price > game_state.balance and game_state.marvin_candidate_price <= game_state.balance + 20000:
                score("exploit_marvin", 44.0)
        else:
            # RANK 0-1: Massive boost to Marvin 
            score("exploit_marvin", 88.0 + min(60.0, game_state.marvin_affordable_priority * 1.4))
            if game_state.rank <= 1:
                score("exploit_marvin", 48.0)
                if game_state.has_met_vinnie and game_state.loan_debt == 0 and 1000 <= game_state.balance < 8000:
                    score("exploit_marvin", 56.0)
                if game_state.has_worn_map and not game_state.has_map and game_state.balance >= 1200:
                    score("exploit_marvin", 52.0)
                if game_state.marvin_affordable_priority >= 56 and game_state.balance >= 1800:
                    score("exploit_marvin", 48.0)
                if 1200 <= game_state.balance < 10000 and game_state.health >= 62 and game_state.sanity >= 34:
                    score("exploit_marvin", 42.0)
                if game_state.marvin_candidate_price > game_state.balance and game_state.marvin_candidate_price <= game_state.balance + 5000:
                    score("exploit_marvin", 44.0)
                if game_state.marvin_future_priority >= 56 and 0 < game_state.marvin_future_shortfall <= 5000 and game_state.balance >= 950:
                    score("exploit_marvin", 52.0)
                    if game_state.has_met_vinnie and game_state.loan_debt == 0:
                        score("exploit_marvin", 38.0)
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
            score("exploit_adventure", 58.0)
            # At rank 2+ with adventure safe, also boost push_next_rank so the planner
            # considers adventure as a valid push-forward action.
            score("push_next_rank", 48.0)
        else:
            score("reach_adventure_threshold", 76.0)

    # Proactive borrowing: when Vinnie is available and balance is low, score
    # push_next_rank higher so the loan route beats the convenience store.
    if game_state.opportunity_flags.get("can_borrow_to_bootstrap"):
        score("push_next_rank", float(tval("planner.borrow_to_bootstrap.push_next_rank_bonus", 26.0)))
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
        score("push_next_rank", float(tval("planner.rank_push.rank0", 72.0)))
    elif game_state.rank == 1:
        score("push_next_rank", float(tval("planner.rank_push.rank1", 68.0)))
    elif game_state.rank == 2:
        score("push_next_rank", float(tval("planner.rank_push.rank2", 52.0)))
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
        score("push_next_rank", float(tval("planner.bankroll_emergency.push_next_rank_penalty", -34.0)))
        score("exploit_adventure", float(tval("planner.bankroll_emergency.exploit_adventure_penalty", -80.0)))
        score("unlock_marvin", float(tval("planner.bankroll_emergency.unlock_marvin_penalty", -40.0)))
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
    preliminary_scores = {goal: scores.get(goal, 0.0) for goal in candidate_goals}
    rough_best_goal = max(preliminary_scores, key=lambda goal: (preliminary_scores[goal], goal))
    personality = personality_manager.get_for_state(rough_best_goal, game_state)

    filtered_scores: dict[str, float] = {}
    objective_total = 0.0
    for goal in candidate_goals:
        bonus = _goal_objective_bonus(goal, game_state, personality)
        objective_total += bonus
        filtered_scores[goal] = preliminary_scores[goal] + bonus

    best_goal = max(filtered_scores, key=lambda goal: (filtered_scores[goal], goal))
    best_goal, reason_code = _maybe_explore_goal(candidate_goals, best_goal, personality)
    constrained_goal, constraint_code = _apply_hard_constraints(best_goal, game_state, personality)
    if constraint_code != "goal_max_score":
        reason_code = constraint_code
    final_personality = personality_manager.get_for_state(constrained_goal, game_state)
    if final_personality != personality:
        objective_total = 0.0
        filtered_scores = {}
        for goal in candidate_goals:
            bonus = _goal_objective_bonus(goal, game_state, final_personality)
            objective_total += bonus
            filtered_scores[goal] = preliminary_scores[goal] + bonus
    if constrained_goal not in filtered_scores:
        filtered_scores[constrained_goal] = scores.get(constrained_goal, 0.0)

    reason = (
        f"goal={constrained_goal} score={filtered_scores[constrained_goal]:.1f} "
        f"personality={final_personality.name} objective={final_personality.objective_function} "
        f"reason_code={reason_code}"
    )
    return StrategicPlan(
        goal=constrained_goal,
        scores=filtered_scores,
        reason=reason,
        personality=final_personality,
        reason_code=reason_code,
        objective_value=objective_total,
    )