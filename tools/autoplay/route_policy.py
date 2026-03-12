from __future__ import annotations

from typing import Iterable

from .interfaces import DecisionOption, DecisionRequest
from .planner import StrategicPlan
from .trace import DecisionTrace


def _route_tags(label: str) -> set[str]:
    lowered = label.lower()
    tags: set[str] = set()
    if "doctor" in lowered:
        tags.add("medical")
    if "witch" in lowered:
        tags.add("witch")
        tags.add("medical")
    if "marvin" in lowered:
        tags.add("marvin")
    if "vinnie" in lowered or "loan" in lowered:
        tags.add("loan")
    if "tom" in lowered or "frank" in lowered or "oswald" in lowered:
        tags.add("mechanic")
    if "workbench" in lowered or "outoparts" in lowered:
        tags.add("upgrade")
    if "convenience" in lowered:
        tags.add("store")
    if "pawn" in lowered or "gus" in lowered:
        tags.add("pawn")
    if label.startswith("Drive to "):
        tags.add("adventure")
    if "stay home" in lowered:
        tags.add("stay_home")
    return tags


def _score_goal_alignment(goal: str, tags: set[str]) -> float:
    mapping = {
        "survive_emergency": {"medical": 100.0, "stay_home": 60.0, "loan": -40.0, "adventure": -60.0},
        "stabilize_health": {"medical": 90.0, "stay_home": 35.0, "loan": -18.0, "adventure": -35.0},
        "stabilize_sanity": {"medical": 55.0, "stay_home": 40.0, "adventure": -20.0},
        "reduce_fatigue_pressure": {"stay_home": 88.0, "store": 22.0, "adventure": -45.0, "loan": -18.0},
        "preserve_companion_roster": {"store": 70.0, "stay_home": 24.0, "pawn": -28.0, "adventure": -20.0},
        "restock_supplies": {"store": 102.0, "stay_home": 18.0, "pawn": -16.0, "loan": -12.0, "adventure": -24.0},
        "acquire_car": {"mechanic": 85.0, "loan": 28.0, "store": 10.0, "marvin": -18.0, "adventure": -25.0},
        "bootstrap_blackjack_edge": {"store": 14.0, "stay_home": 18.0, "adventure": -18.0},
        "reduce_debt_risk": {"loan": 95.0, "pawn": 18.0, "marvin": -15.0, "adventure": -20.0},
        "contain_debt_escalation": {"loan": 105.0, "pawn": 22.0, "marvin": -18.0, "adventure": -28.0},
        "cashout_pawn_inventory": {"pawn": 108.0, "loan": 18.0, "store": -8.0, "marvin": -12.0, "adventure": -24.0},
        "blend_fraudulent_cash_safely": {"marvin": 24.0, "store": 8.0, "adventure": -15.0},
        "unlock_marvin": {"mechanic": 20.0, "store": 8.0, "adventure": 6.0},
        "exploit_marvin": {"marvin": 95.0, "loan": 35.0, "mechanic": -12.0, "adventure": -10.0},
        "recover_from_car_trouble": {"mechanic": 92.0, "upgrade": 55.0, "stay_home": 18.0, "adventure": -40.0},
        "advance_mechanic_arc": {"mechanic": 92.0, "upgrade": 35.0, "marvin": -10.0},
        "repair_or_upgrade_gear": {"upgrade": 90.0, "mechanic": 72.0, "marvin": -10.0},
        "restore_blackjack_edge_after_breakage": {"upgrade": 95.0, "mechanic": 78.0, "store": 12.0, "adventure": -28.0},
        "reach_adventure_threshold": {"marvin": 26.0, "mechanic": 16.0, "adventure": 10.0},
        "exploit_adventure": {"adventure": 90.0, "marvin": 12.0, "loan": -10.0},
        "convert_millionaire_to_ending": {"upgrade": 14.0, "adventure": -30.0, "loan": -40.0},
        "push_next_rank": {"marvin": 20.0, "store": 8.0, "adventure": 10.0, "stay_home": -5.0},
    }
    goal_weights = mapping.get(goal, {})
    return sum(goal_weights.get(tag, 0.0) for tag in tags)


def _score_route_opportunity(tags: set[str], metadata: dict[str, object]) -> float:
    total = 0.0

    store_spend = float(metadata.get("store_spend", 0) or 0)
    if "store" in tags and metadata.get("wants_store"):
        total += 54.0 + min(34.0, store_spend / 8.0)

    pawn_value = float(metadata.get("pawn_value", 0) or 0)
    if "pawn" in tags and metadata.get("wants_pawn"):
        total += 50.0 + min(36.0, pawn_value / 18.0)

    loan_pressure = float(metadata.get("loan_pressure", 0) or 0)
    if "loan" in tags and metadata.get("wants_loan"):
        total += 52.0 + min(32.0, loan_pressure / 4.0)

    marvin_priority = float(metadata.get("marvin_priority", 0) or 0)
    if "marvin" in tags and metadata.get("wants_marvin"):
        total += 48.0 + min(28.0, marvin_priority / 4.0)

    mechanic_urgency = float(metadata.get("mechanic_urgency", 0) or 0)
    if "mechanic" in tags and metadata.get("wants_mechanic"):
        total += 58.0 + min(30.0, mechanic_urgency / 3.0)

    upgrade_urgency = float(metadata.get("upgrade_urgency", 0) or 0)
    if "upgrade" in tags and metadata.get("wants_upgrade"):
        total += 46.0 + min(28.0, upgrade_urgency / 4.0)

    adventure_readiness = float(metadata.get("adventure_readiness", 0) or 0)
    if "adventure" in tags and metadata.get("wants_adventure"):
        total += 48.0 + min(26.0, adventure_readiness / 3.0)

    if "stay_home" in tags and metadata.get("needs_recovery_day"):
        total += 22.0

    return total


def choose_route_option(request: DecisionRequest, plan: StrategicPlan) -> tuple[DecisionOption | None, DecisionTrace]:
    metadata = dict(request.metadata)
    best_option: DecisionOption | None = None
    best_total = float("-inf")
    score_by_option: dict[str, float] = {}
    store_spend = float(metadata.get("store_spend", 0) or 0)
    pawn_value = float(metadata.get("pawn_value", 0) or 0)

    for option in request.normalized_options:
        tags = _route_tags(option.label)
        total = _score_goal_alignment(plan.goal, tags)
        total += _score_route_opportunity(tags, metadata)

        if metadata.get("urgent_medical"):
            total += 140.0 if "medical" in tags else -80.0
        if metadata.get("needs_recovery_day") and "stay_home" in tags:
            total += 28.0
        if metadata.get("wants_doctor") and option.label == "Doctor's Office":
            total += 42.0
        if metadata.get("wants_witch") and option.label == "Witch Doctor's Tower":
            total += 34.0
        if metadata.get("wants_marvin") and "marvin" in tags:
            total += 22.0
        if metadata.get("wants_loan") and "loan" in tags:
            total += 16.0
        if metadata.get("wants_store") and "store" in tags:
            total += 12.0
        if metadata.get("wants_adventure") and "adventure" in tags:
            total += 14.0
        if metadata.get("wants_upgrade") and "upgrade" in tags:
            total += 14.0
        if metadata.get("wants_mechanic") and "mechanic" in tags:
            total += 18.0
        if metadata.get("wants_pawn") and "pawn" in tags:
            total += 14.0
        if option.label == metadata.get("medical_choice") and "medical" in tags:
            total += 12.0

        if metadata.get("has_car") is False and "mechanic" in tags:
            total += 24.0
        if metadata.get("has_car") and "mechanic" in tags and metadata.get("mechanic_visits", 0) >= 3:
            total -= 30.0
        if metadata.get("has_car") and "store" in tags and store_spend <= 0:
            total -= 22.0
        if metadata.get("has_car") and "pawn" in tags and pawn_value <= 0:
            total -= 18.0
        if metadata.get("has_marvin_access") is False and "marvin" in tags:
            total -= 60.0
        if metadata.get("rank", 0) <= 1 and "adventure" in tags and not metadata.get("wants_adventure"):
            total -= 16.0

        score_by_option[option.option_id] = total
        if total > best_total:
            best_option = option
            best_total = total

    if best_option is None:
        trace = DecisionTrace(
            cycle=metadata.get("cycle"),
            day=metadata.get("day"),
            context=request.stable_context_id or request.request_type,
            request_type=request.request_type,
            strategic_goal=plan.goal,
            chosen_action="fallback:none",
            reason="no route options available",
            confidence=0.0,
            options=tuple(option.label for option in request.normalized_options),
            game_state_summary=dict(request.game_state),
            score_breakdown={},
            metadata={"plan": plan.to_dict()},
        )
        return None, trace

    sorted_scores = sorted(score_by_option.values(), reverse=True)
    margin = sorted_scores[0] - sorted_scores[1] if len(sorted_scores) > 1 else sorted_scores[0]
    confidence = min(1.0, max(0.05, 0.45 + margin / 100.0))
    reason = f"goal={plan.goal} selected {best_option.label} score={best_total:.1f} margin={margin:.1f}"
    trace = DecisionTrace(
        cycle=metadata.get("cycle"),
        day=metadata.get("day"),
        context=request.stable_context_id or request.request_type,
        request_type=request.request_type,
        strategic_goal=plan.goal,
        chosen_action=str(best_option.value if best_option.value is not None else best_option.option_id),
        reason=reason,
        confidence=confidence,
        options=tuple(option.label for option in request.normalized_options),
        game_state_summary=dict(request.game_state),
        score_breakdown=score_by_option,
        metadata={"plan": plan.to_dict()},
    )
    return best_option, trace