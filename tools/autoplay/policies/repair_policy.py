from __future__ import annotations

from ..interfaces import DecisionOption, DecisionRequest
from ..planner import StrategicPlan
from ..trace import DecisionTrace


def _score_repair_option(option: DecisionOption, plan: StrategicPlan, request: DecisionRequest) -> float:
    option_meta = dict(option.metadata)
    score = float(option_meta.get("base_score", option_meta.get("priority", 0.0)) or 0.0)
    is_exit = bool(option_meta.get("is_exit"))
    if is_exit:
        score -= 8.0

    if plan.goal in {"recover_from_car_trouble", "repair_or_upgrade_gear", "restore_blackjack_edge_after_breakage"}:
        score += 24.0
    if plan.goal == "advance_mechanic_arc":
        score += 10.0
    if is_exit and score < 0:
        score += 12.0
    return score


def choose_repair_option(request: DecisionRequest, plan: StrategicPlan) -> tuple[DecisionOption | None, DecisionTrace]:
    best_option: DecisionOption | None = None
    best_score = float("-inf")
    score_breakdown: dict[str, float] = {}

    for option in request.normalized_options:
        total = _score_repair_option(option, plan, request)
        score_breakdown[option.option_id] = total
        if total > best_score:
            best_option = option
            best_score = total

    if best_option is None:
        trace = DecisionTrace(
            cycle=request.metadata.get("cycle"),
            day=request.metadata.get("day"),
            context=request.stable_context_id or request.request_type,
            request_type=request.request_type,
            strategic_goal=plan.goal,
            chosen_action="fallback:none",
            reason="no repair options available",
            confidence=0.0,
            options=tuple(option.label for option in request.normalized_options),
            game_state_summary=dict(request.game_state),
            score_breakdown=score_breakdown,
            metadata={"plan": plan.to_dict()},
        )
        return None, trace

    sorted_scores = sorted(score_breakdown.values(), reverse=True)
    margin = sorted_scores[0] - sorted_scores[1] if len(sorted_scores) > 1 else sorted_scores[0]
    confidence = min(1.0, max(0.1, 0.5 + margin / 120.0))
    trace = DecisionTrace(
        cycle=request.metadata.get("cycle"),
        day=request.metadata.get("day"),
        context=request.stable_context_id or request.request_type,
        request_type=request.request_type,
        strategic_goal=plan.goal,
        chosen_action=str(best_option.value if best_option.value is not None else best_option.option_id),
        reason=f"goal={plan.goal} selected {best_option.label} score={best_score:.1f} margin={margin:.1f}",
        confidence=confidence,
        options=tuple(option.label for option in request.normalized_options),
        game_state_summary=dict(request.game_state),
        score_breakdown=score_breakdown,
        metadata={"plan": plan.to_dict()},
    )
    return best_option, trace