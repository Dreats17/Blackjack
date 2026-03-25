"""Named personality configurations for the autoplayer.

Each Personality defines behaviour parameters that tune policy decisions
across all domains: betting, purchasing, event choices, and routing.
The active personality is chosen by PersonalityManager based on the
current strategic goal and attached to StrategicPlan so every policy
can read it without additional lookups.
"""
from __future__ import annotations

from dataclasses import dataclass


PERSONALITY_SET_VERSION = "2026-03-23.objective-v1"


@dataclass(frozen=True)
class Personality:
    """Behaviour configuration for one strategic mode."""

    name: str

    # ── Blackjack betting ─────────────────────────────────────────────────
    # Scales the computed bet ratio around the baseline formula.
    # 0.50 = no change from the existing calibrated formula.
    # Range roughly: 0.10 (very timid) → 0.90 (very aggressive).
    bet_aggression: float = 0.50

    # When True, apply drawdown protection: cut bets when balance has fallen
    # below drawdown_threshold * run_peak.
    drawdown_protection: bool = True
    # Fraction of peak balance at which drawdown protection kicks in.
    drawdown_threshold: float = 0.50
    # Fraction of current balance to bet while in drawdown mode.
    drawdown_bet_fraction: float = 0.07

    # ── Health / medical priority ─────────────────────────────────────────
    # Multiplier on health-related score boosts in purchase_policy.
    health_caution: float = 1.0

    # ── Shopping / Marvin ─────────────────────────────────────────────────
    # Multiplier applied to all Marvin item score boosts in purchase_policy.
    marvin_aggression: float = 1.0
    # When True, extra penalty on non-essential (progression/blackjack) purchases.
    frugal_mode: bool = False

    # ── Event choices ─────────────────────────────────────────────────────
    # When True, the safe-choice heuristic in event_policy fires even when
    # resources are not critically low (i.e. always lean conservative).
    prefer_safe_events: bool = False

    # ── Routing ───────────────────────────────────────────────────────────
    # Flat score modifier added to adventure-tagged route options.
    adventure_bias: float = 0.0

    # ── Objective-driven strategy model ───────────────────────────────────
    objective_function: str = "balanced_progress"
    hard_constraints: tuple[str, ...] = ()
    risk_tolerance: str = "medium"  # low | medium | high
    switch_triggers: tuple[str, ...] = ()
    exploration_probability: float = 0.08

    # Safety cutoffs used by planner/policies when enforcing constraints.
    safety_min_health: int = 40
    safety_min_sanity: int = 24
    safety_max_warning: int = 2
    safety_reserve_fraction: float = 0.18

    def __str__(self) -> str:
        return self.name


# ── Built-in personalities ────────────────────────────────────────────────
#
# Bet-aggression scale note:
#   The betting formula applies  (0.60 + 0.80 * bet_aggression)  as a
#   multiplier on the base ratio.  At 0.50 the multiplier is exactly 1.0
#   (current behaviour unchanged).  At 0.10 it is 0.68 (32 % smaller
#   bets); at 0.72 it is 1.18 (18 % larger bets).

SURVIVAL_CONSERVATIVE = Personality(
    name="survival_conservative",
    bet_aggression=0.07,
    drawdown_protection=True,
    drawdown_threshold=0.70,
    drawdown_bet_fraction=0.04,
    health_caution=2.35,
    marvin_aggression=0.5,
    frugal_mode=True,
    prefer_safe_events=True,
    adventure_bias=-25.0,
    objective_function="maximize_days_alive_minimize_medical_crises",
    hard_constraints=(
        "never_force_high_variance_gambling_under_low_resources",
        "force_medical_stabilization_on_status_stack",
        "protect_minimum_cash_reserve",
    ),
    risk_tolerance="low",
    switch_triggers=(
        "health<45",
        "sanity<30",
        "warning>=2",
        "status_count>=2",
    ),
    exploration_probability=0.05,
    safety_min_health=48,
    safety_min_sanity=30,
    safety_max_warning=2,
    safety_reserve_fraction=0.28,
)

WEALTH_AGGRO = Personality(
    name="wealth_aggro",
    bet_aggression=0.72,
    drawdown_protection=True,
    drawdown_threshold=0.42,
    drawdown_bet_fraction=0.09,
    health_caution=0.82,
    marvin_aggression=1.6,
    frugal_mode=False,
    prefer_safe_events=False,
    adventure_bias=16.0,
    objective_function="maximize_bankroll_growth_rate",
    hard_constraints=(
        "maintain_recovery_reserve_before_high_risk_entries",
        "defer_extreme_bets_when_warning_tier_high",
    ),
    risk_tolerance="high",
    switch_triggers=(
        "drawdown>35%",
        "warning>=2",
        "health<52",
        "sanity<32",
    ),
    exploration_probability=0.12,
    safety_min_health=38,
    safety_min_sanity=24,
    safety_max_warning=2,
    safety_reserve_fraction=0.15,
)

ENDING_HUNTER = Personality(
    name="ending_hunter",
    bet_aggression=0.46,
    drawdown_protection=True,
    drawdown_threshold=0.52,
    drawdown_bet_fraction=0.07,
    health_caution=1.35,
    marvin_aggression=1.25,
    frugal_mode=True,
    prefer_safe_events=True,
    adventure_bias=-4.0,
    objective_function="maximize_branch_prerequisites_and_lock_points",
    hard_constraints=(
        "do_not_cross_millionaire_without_branch_prereqs",
        "prefer_route_lock_actions_over_short_term_ev",
    ),
    risk_tolerance="medium",
    switch_triggers=(
        "mechanic_lock_missing",
        "ending_prereq_progress<target",
    ),
    exploration_probability=0.06,
    safety_min_health=44,
    safety_min_sanity=26,
    safety_max_warning=2,
    safety_reserve_fraction=0.20,
)

COMPANION_COLLECTOR = Personality(
    name="companion_collector",
    bet_aggression=0.38,
    drawdown_protection=True,
    drawdown_threshold=0.50,
    drawdown_bet_fraction=0.07,
    health_caution=1.25,
    marvin_aggression=0.9,
    frugal_mode=True,
    prefer_safe_events=True,
    adventure_bias=4.0,
    objective_function="maximize_companion_count_and_sanctuary_readiness",
    hard_constraints=(
        "preserve_food_buffer_for_companions",
        "avoid_companion_loss_events_when_possible",
    ),
    risk_tolerance="medium",
    switch_triggers=(
        "companion_count<5_with_whistle_window",
        "runaway_risk>0",
    ),
    exploration_probability=0.10,
    safety_min_health=42,
    safety_min_sanity=24,
    safety_max_warning=2,
    safety_reserve_fraction=0.18,
)

CRAFTING_ENGINEER = Personality(
    name="crafting_engineer",
    bet_aggression=0.34,
    drawdown_protection=True,
    drawdown_threshold=0.54,
    drawdown_bet_fraction=0.07,
    health_caution=1.18,
    marvin_aggression=0.88,
    frugal_mode=True,
    prefer_safe_events=True,
    adventure_bias=-6.0,
    objective_function="maximize_recipe_depth_and_tier_progression",
    hard_constraints=(
        "acquire_toolkit_early",
        "prefer_component_branching_items_over_filler",
    ),
    risk_tolerance="low",
    switch_triggers=(
        "toolkit_missing",
        "crafting_depth_stalled",
    ),
    exploration_probability=0.07,
    safety_min_health=46,
    safety_min_sanity=28,
    safety_max_warning=2,
    safety_reserve_fraction=0.22,
)

DEBT_GAMBLER = Personality(
    name="debt_gambler",
    bet_aggression=0.60,
    drawdown_protection=True,
    drawdown_threshold=0.45,
    drawdown_bet_fraction=0.08,
    health_caution=0.92,
    marvin_aggression=1.15,
    frugal_mode=False,
    prefer_safe_events=False,
    adventure_bias=9.0,
    objective_function="stress_test_loan_and_fraud_systems",
    hard_constraints=(
        "never_enter_tony_zone_without_escape_reserve",
        "cap_warning_when_health_or_sanity_is_critical",
    ),
    risk_tolerance="high",
    switch_triggers=(
        "warning>=3",
        "fraudulent_cash>0",
        "debt>0",
    ),
    exploration_probability=0.10,
    safety_min_health=36,
    safety_min_sanity=22,
    safety_max_warning=3,
    safety_reserve_fraction=0.14,
)

RECOVERY_SPECIALIST = Personality(
    name="recovery_specialist",
    bet_aggression=0.12,
    drawdown_protection=True,
    drawdown_threshold=0.75,
    drawdown_bet_fraction=0.03,
    health_caution=2.7,
    marvin_aggression=0.4,
    frugal_mode=True,
    prefer_safe_events=True,
    adventure_bias=-28.0,
    objective_function="maximize_recovery_from_damaged_state",
    hard_constraints=(
        "force_medical_until_stable",
        "avoid_new_debt_during_recovery",
        "suspend_high_variance_gambling",
    ),
    risk_tolerance="low",
    switch_triggers=(
        "health<50",
        "sanity<32",
        "status_count>=2",
        "injury_count>=1",
    ),
    exploration_probability=0.03,
    safety_min_health=50,
    safety_min_sanity=32,
    safety_max_warning=1,
    safety_reserve_fraction=0.34,
)

BASELINE_RANDOM = Personality(
    name="baseline_random",
    bet_aggression=0.50,
    drawdown_protection=True,
    drawdown_threshold=0.50,
    drawdown_bet_fraction=0.07,
    health_caution=1.0,
    marvin_aggression=1.0,
    frugal_mode=False,
    prefer_safe_events=False,
    adventure_bias=0.0,
    objective_function="baseline_randomized_policy_for_coverage",
    hard_constraints=(
        "respect_absolute_safety_cutoffs",
    ),
    risk_tolerance="medium",
    switch_triggers=(
        "exploration_mode",
    ),
    exploration_probability=1.0,
    safety_min_health=34,
    safety_min_sanity=18,
    safety_max_warning=3,
    safety_reserve_fraction=0.12,
)

# Backward-compatible aliases for existing imports and mappings.
SURVIVOR = SURVIVAL_CONSERVATIVE
CAUTIOUS = RECOVERY_SPECIALIST
CONSERVATIVE = SURVIVAL_CONSERVATIVE
DEBT_RESOLVER = DEBT_GAMBLER
CAR_HUNTER = WEALTH_AGGRO
EDGE_BUILDER = WEALTH_AGGRO
PUSHER = WEALTH_AGGRO
MARVIN_HUNTER = WEALTH_AGGRO
GEAR_FOCUSED = CRAFTING_ENGINEER
FRAUD_BLENDER = DEBT_GAMBLER

# Used when no goal-specific mapping exists.
DEFAULT_PERSONALITY = SURVIVAL_CONSERVATIVE

# Full registry keyed by name — useful for debugging and reporting.
ALL_PERSONALITIES: dict[str, Personality] = {
    p.name: p
    for p in (
        SURVIVAL_CONSERVATIVE,
        WEALTH_AGGRO,
        ENDING_HUNTER,
        COMPANION_COLLECTOR,
        CRAFTING_ENGINEER,
        DEBT_GAMBLER,
        RECOVERY_SPECIALIST,
        BASELINE_RANDOM,
    )
}
