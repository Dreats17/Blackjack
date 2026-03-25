"""Dynamic personality manager for the autoplayer.

Maps every strategic goal produced by the planner to a Personality that
modulates policy decisions across betting, purchasing, routing, and event
choices.  The personality travels with the StrategicPlan so each policy
function can read it without any extra state lookups.
"""
from __future__ import annotations

from dataclasses import replace
import random

from .personalities import (
    BASELINE_RANDOM,
    COMPANION_COLLECTOR,
    CRAFTING_ENGINEER,
    DEBT_GAMBLER,
    DEFAULT_PERSONALITY,
    ENDING_HUNTER,
    PERSONALITY_SET_VERSION,
    RECOVERY_SPECIALIST,
    SURVIVAL_CONSERVATIVE,
    WEALTH_AGGRO,
    Personality,
)
from .tuning import tscale, tval

# Complete mapping — every goal the planner can produce has an entry.
_GOAL_TO_PERSONALITY: dict[str, Personality] = {
    # Run over
    "run_ended":                              SURVIVAL_CONSERVATIVE,
    # Emergencies
    "survive_emergency":                      RECOVERY_SPECIALIST,
    # Recovery
    "stabilize_health":                       RECOVERY_SPECIALIST,
    "stabilize_sanity":                       RECOVERY_SPECIALIST,
    "reduce_fatigue_pressure":                RECOVERY_SPECIALIST,
    # Crew & supplies
    "preserve_companion_roster":              COMPANION_COLLECTOR,
    "restock_supplies":                       CRAFTING_ENGINEER,
    # Debt management
    "reduce_debt_risk":                       DEBT_GAMBLER,
    "contain_debt_escalation":                DEBT_GAMBLER,
    "cashout_pawn_inventory":                 DEBT_GAMBLER,
    # Pre-car bootstrap
    "acquire_car":                            WEALTH_AGGRO,
    "bootstrap_blackjack_edge":               WEALTH_AGGRO,
    # Growth / ranking up
    "push_next_rank":                         WEALTH_AGGRO,
    "exploit_adventure":                      WEALTH_AGGRO,
    "reach_adventure_threshold":              WEALTH_AGGRO,
    # Marvin
    "exploit_marvin":                         WEALTH_AGGRO,
    "unlock_marvin":                          WEALTH_AGGRO,
    # Gear & maintenance
    "recover_from_car_trouble":               CRAFTING_ENGINEER,
    "advance_mechanic_arc":                   ENDING_HUNTER,
    "repair_or_upgrade_gear":                 CRAFTING_ENGINEER,
    "restore_blackjack_edge_after_breakage":  CRAFTING_ENGINEER,
    # Special cases
    "blend_fraudulent_cash_safely":           DEBT_GAMBLER,
    "convert_millionaire_to_ending":          ENDING_HUNTER,
}


class PersonalityManager:
    """Selects the appropriate Personality for a given strategic goal."""

    version: str = PERSONALITY_SET_VERSION

    _BOOTSTRAP_GOALS: frozenset[str] = frozenset({
        "acquire_car",
        "bootstrap_blackjack_edge",
        "push_next_rank",
    })

    _BOOTSTRAP_BALANCE_FLOOR: int = 220
    _BOOTSTRAP_HEALTH_FLOOR: int = 60
    _BOOTSTRAP_SANITY_FLOOR: int = 35

    def _tune_personality(self, personality: Personality) -> Personality:
        name = personality.name
        tuned = replace(
            personality,
            bet_aggression=tscale(f"personality.{name}.bet_aggression_scale", personality.bet_aggression, minimum=0.01, maximum=1.5),
            drawdown_threshold=tscale(f"personality.{name}.drawdown_threshold_scale", personality.drawdown_threshold, minimum=0.05, maximum=0.99),
            drawdown_bet_fraction=tscale(f"personality.{name}.drawdown_bet_fraction_scale", personality.drawdown_bet_fraction, minimum=0.01, maximum=0.5),
            health_caution=tscale(f"personality.{name}.health_caution_scale", personality.health_caution, minimum=0.25, maximum=5.0),
            marvin_aggression=tscale(f"personality.{name}.marvin_aggression_scale", personality.marvin_aggression, minimum=0.1, maximum=5.0),
            adventure_bias=float(tval(f"personality.{name}.adventure_bias", personality.adventure_bias)),
            exploration_probability=tscale(
                "manager.exploration_global_scale",
                tscale(f"personality.{name}.exploration_probability_scale", personality.exploration_probability, minimum=0.0, maximum=1.0),
                minimum=0.0,
                maximum=1.0,
            ),
            safety_min_health=int(tval(f"personality.{name}.safety_min_health", personality.safety_min_health)),
            safety_min_sanity=int(tval(f"personality.{name}.safety_min_sanity", personality.safety_min_sanity)),
            safety_max_warning=int(tval(f"personality.{name}.safety_max_warning", personality.safety_max_warning)),
            safety_reserve_fraction=tscale(f"personality.{name}.safety_reserve_fraction_scale", personality.safety_reserve_fraction, minimum=0.01, maximum=0.9),
        )
        return tuned

    def _state_trigger_override(self, goal: str, game_state: object | None) -> Personality | None:
        if game_state is None:
            return None

        health = int(getattr(game_state, "health", 100) or 100)
        sanity = int(getattr(game_state, "sanity", 100) or 100)
        injuries = len(tuple(getattr(game_state, "injuries", ()) or ()))
        statuses = len(tuple(getattr(game_state, "statuses", ()) or ()))
        warning = int(getattr(game_state, "loan_warning_level", 0) or 0)
        debt = int(getattr(game_state, "loan_debt", 0) or 0)
        companion_count = int(getattr(game_state, "companion_count", 0) or 0)
        has_car = bool(getattr(game_state, "has_car", False))
        rank = int(getattr(game_state, "rank", 0) or 0)
        balance = int(getattr(game_state, "balance", 0) or 0)
        bankroll_emergency = bool(getattr(game_state, "bankroll_emergency", False))
        fragile_post_car = bool(getattr(game_state, "fragile_post_car", False))

        bootstrap_balance_floor = int(tval("manager.bootstrap.balance_floor", self._BOOTSTRAP_BALANCE_FLOOR))
        bootstrap_health_floor = int(tval("manager.bootstrap.health_floor", self._BOOTSTRAP_HEALTH_FLOOR))
        bootstrap_sanity_floor = int(tval("manager.bootstrap.sanity_floor", self._BOOTSTRAP_SANITY_FLOOR))

        if not has_car and goal in self._BOOTSTRAP_GOALS:
            bootstrap_ready = (
                balance >= bootstrap_balance_floor
                and health >= bootstrap_health_floor
                and sanity >= bootstrap_sanity_floor
            )
            if not bootstrap_ready:
                return SURVIVAL_CONSERVATIVE

        warning_tier_recovery = int(tval("manager.debt.warning_tier_recovery", 3))
        warning_tier_hard = int(tval("manager.debt.warning_tier_hard", 4))
        warning_rank_max = int(tval("manager.debt.recovery_rank_max", 0))
        critical_debt = int(tval("manager.debt.critical_amount", 50_000))

        if rank <= warning_rank_max and warning >= warning_tier_recovery and warning < warning_tier_hard and debt < critical_debt:
            return RECOVERY_SPECIALIST

        if health < 35 or sanity < 18 or injuries >= 2 or statuses >= 3:
            return RECOVERY_SPECIALIST
        if (bankroll_emergency or fragile_post_car) and rank <= 1:
            return RECOVERY_SPECIALIST
        if warning >= warning_tier_hard or debt >= critical_debt:
            return DEBT_GAMBLER
        if goal == "convert_millionaire_to_ending" or balance >= 1_000_000:
            return ENDING_HUNTER
        if companion_count >= 3 and rank <= 2:
            return COMPANION_COLLECTOR
        if has_car and rank >= 1 and goal in {"repair_or_upgrade_gear", "recover_from_car_trouble"}:
            return CRAFTING_ENGINEER
        return None

    def _maybe_explore(self, personality: Personality) -> Personality:
        if personality.exploration_probability <= 0:
            return personality
        if random.random() < personality.exploration_probability:
            return BASELINE_RANDOM
        return personality

    def get_for_goal(self, goal: str) -> Personality:
        """Return the Personality configured for *goal*."""
        return self._tune_personality(_GOAL_TO_PERSONALITY.get(goal, DEFAULT_PERSONALITY))

    def get_for_state(self, goal: str, game_state: object | None = None) -> Personality:
        base = self.get_for_goal(goal)
        override = self._state_trigger_override(goal, game_state)
        return self._maybe_explore(override or base)

    # Backwards-compatibility alias
    def get_personality(self, goal: str) -> Personality:
        return self.get_for_goal(goal)


# Module-level singleton used by the planner and all policy modules.
personality_manager = PersonalityManager()
