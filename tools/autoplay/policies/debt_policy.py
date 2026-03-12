from __future__ import annotations

from ..interfaces import DecisionOption, DecisionRequest
from ..planner import StrategicPlan
from ..trace import DecisionTrace


def _score_loan_option(option: DecisionOption, plan: StrategicPlan, request: DecisionRequest) -> float:
    option_meta = dict(option.metadata)
    request_meta = dict(request.metadata)
    score = float(option_meta.get("base_score", 0.0) or 0.0)
    action_kind = str(option_meta.get("action_kind", "unknown"))
    amount = float(option_meta.get("amount", 0.0) or 0.0)
    warning = float(request_meta.get("warning_level", 0.0) or 0.0)
    debt = float(request_meta.get("debt", 0.0) or 0.0)
    actionable = bool(option_meta.get("actionable", False)) if action_kind != "leave" else True

    if action_kind == "leave":
        score -= 5.0
    elif not actionable:
        score -= 60.0

    if actionable and plan.goal in {"contain_debt_escalation", "reduce_debt_risk"}:
        if action_kind == "repay":
            score += 28.0 + min(18.0, debt / 150.0)
        if action_kind == "borrow":
            score -= 20.0 + warning * 5.0

    if actionable and plan.goal in {"acquire_car", "bootstrap_blackjack_edge", "exploit_marvin"}:
        if action_kind == "borrow":
            score += 14.0
        if action_kind == "repay" and debt <= 0:
            score -= 10.0

    if actionable and warning >= 2 and action_kind == "repay":
        score += 16.0
    if actionable and warning >= 2 and action_kind == "borrow":
        score -= 12.0
    if actionable and amount > 0 and option_meta.get("desired_amount"):
        score += max(0.0, 8.0 - abs(amount - float(option_meta.get("desired_amount", 0.0))) / 250.0)
    return score


def choose_loan_option(request: DecisionRequest, plan: StrategicPlan) -> tuple[DecisionOption | None, DecisionTrace]:
    best_option: DecisionOption | None = None
    best_score = float("-inf")
    score_breakdown: dict[str, float] = {}

    for option in request.normalized_options:
        total = _score_loan_option(option, plan, request)
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
            reason="no loan options available",
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