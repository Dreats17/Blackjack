from __future__ import annotations

from ..interfaces import DecisionOption, DecisionRequest
from ..planner import StrategicPlan
from ..trace import DecisionTrace


def _score_medical_option(option: DecisionOption, plan: StrategicPlan, request: DecisionRequest) -> float:
    metadata = dict(request.metadata)
    game_state = dict(request.game_state)
    label = option.label

    health = int(game_state.get("health", 0) or 0)
    sanity = int(game_state.get("sanity", 0) or 0)
    injuries = len(tuple(game_state.get("injuries", ()) or ()))
    statuses = len(tuple(game_state.get("statuses", ()) or ()))

    doctor_need_score = float(metadata.get("doctor_need_score", 0.0) or 0.0)
    potion_priority = float(metadata.get("affordable_flask_priority", 0.0) or 0.0)
    doctor_cost = float(metadata.get("doctor_cost", 0.0) or 0.0)
    witch_cost = float(metadata.get("witch_cost", 0.0) or 0.0)
    flask_count = int(metadata.get("flask_count", 0) or 0)
    urgent = bool(metadata.get("urgent_medical"))
    wants_doctor = bool(metadata.get("wants_doctor"))
    wants_witch = bool(metadata.get("wants_witch"))
    has_real_insurance = bool(metadata.get("has_real_insurance"))
    has_faulty_insurance = bool(metadata.get("has_faulty_insurance"))

    if label == "Doctor's Office":
        score = doctor_need_score
        if urgent:
            score += 100.0
        if wants_doctor:
            score += 40.0
        if has_real_insurance:
            score += 85.0
        elif has_faulty_insurance:
            score += 70.0
        score += max(0, injuries - 1) * 20.0
        score += max(0, statuses - 1) * 10.0
        score += max(0, 55 - health)
        if plan.goal in {"survive_emergency", "stabilize_health"}:
            score += 24.0
        if plan.goal == "stabilize_sanity":
            score -= 6.0
        if witch_cost < doctor_cost:
            score -= min(24.0, (doctor_cost - witch_cost) / 6.0)
        return score

    if label == "Witch Doctor's Tower":
        score = potion_priority
        if wants_witch:
            score += 34.0
        if witch_cost < doctor_cost:
            score += min(24.0, (doctor_cost - witch_cost) / 6.0)
        if health >= 60 and sanity >= 28:
            score += 12.0
        if flask_count == 0:
            score += 8.0
        if has_real_insurance:
            score -= 35.0
        elif has_faulty_insurance:
            score -= 28.0
        if injuries >= 1:
            score -= 10.0
        if statuses >= 2:
            score -= 10.0
        if urgent or health < 45 or injuries >= 2 or statuses >= 3:
            score -= 50.0
        if plan.goal == "stabilize_sanity":
            score += 18.0
        elif plan.goal == "stabilize_health":
            score += 6.0
        return score

    return float("-inf")


def choose_medical_option(request: DecisionRequest, plan: StrategicPlan) -> tuple[DecisionOption | None, DecisionTrace]:
    best_option: DecisionOption | None = None
    best_score = float("-inf")
    score_breakdown: dict[str, float] = {}

    for option in request.normalized_options:
        total = _score_medical_option(option, plan, request)
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
            reason="no medical options available",
            confidence=0.0,
            options=tuple(option.label for option in request.normalized_options),
            game_state_summary=dict(request.game_state),
            score_breakdown=score_breakdown,
            metadata={"plan": plan.to_dict()},
        )
        return None, trace

    sorted_scores = sorted(score_breakdown.values(), reverse=True)
    margin = sorted_scores[0] - sorted_scores[1] if len(sorted_scores) > 1 else sorted_scores[0]
    confidence = min(1.0, max(0.2, 0.55 + margin / 120.0))
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