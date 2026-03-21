from __future__ import annotations

from ..config import STORE_MUST_HAVE_ITEMS
from ..interfaces import DecisionOption, DecisionRequest
from ..planner import StrategicPlan
from ..trace import DecisionTrace


def _score_purchase_option(option: DecisionOption, plan: StrategicPlan, request: DecisionRequest) -> float:
    option_meta = dict(option.metadata)
    request_meta = dict(request.metadata)
    score = float(option_meta.get("base_score", option_meta.get("priority", 0.0)) or 0.0)

    if option_meta.get("is_exit"):
        score -= 8.0

    category = str(option_meta.get("category", "generic"))
    item_name = str(option_meta.get("item_name", option.label))
    price = float(option_meta.get("price", 0.0) or 0.0)
    balance = int(request_meta.get("balance", request.game_state.get("balance", 0)) or 0)
    rank = int(request.game_state.get("rank", 0) or 0)
    has_car = bool(request.game_state.get("has_car", False))
    health = int(request.game_state.get("health", 0) or 0)
    sanity = int(request.game_state.get("sanity", 0) or 0)

    if request.stable_context_id == "convenience_store_menu":
        if plan.goal in {"preserve_companion_roster", "reduce_fatigue_pressure"} and category == "food":
            score += 18.0
        if plan.goal == "restock_supplies":
            if category in {"food", "medical", "car"}:
                score += 22.0
            elif category == "blackjack":
                score += 8.0
            else:
                score -= 6.0
        if plan.goal in {"recover_from_car_trouble", "repair_or_upgrade_gear"} and category == "car":
            score += 22.0
        if plan.goal in {"survive_emergency", "stabilize_health"} and category in {"medical", "food"}:
            score += 16.0
        if plan.goal == "bootstrap_blackjack_edge" and category == "blackjack":
            score += 10.0
        if request_meta.get("needs_recovery_day") and category not in {"medical", "food"}:
            score -= 10.0
        if has_car and rank == 0 and balance < 500:
            if category == "progression":
                score -= 42.0
            if category == "blackjack":
                score -= 18.0
            if category == "car" and item_name not in STORE_MUST_HAVE_ITEMS:
                score -= 20.0
            if item_name not in STORE_MUST_HAVE_ITEMS and category not in {"medical", "food"}:
                score -= 16.0
            if health < 85 or sanity < 70:
                if category in {"medical", "food"} or item_name in {"Road Flares", "Bug Spray"}:
                    score += 14.0
        if has_car and rank == 0 and balance < 250:
            if item_name not in STORE_MUST_HAVE_ITEMS and category not in {"medical", "food"}:
                score -= 32.0
            if category == "progression":
                score -= 18.0

    if request.stable_context_id == "witch_flask_menu":
        if plan.goal in {"survive_emergency", "stabilize_health", "stabilize_sanity"} and category == "defensive_flask":
            score += 24.0
        if plan.goal in {"exploit_marvin", "push_next_rank", "bootstrap_blackjack_edge"} and category == "offensive_flask":
            score += 18.0
        if plan.goal == "reduce_fatigue_pressure" and category == "utility_flask":
            score += 8.0

    if option_meta.get("is_exit") and score < 0.0:
        score += 12.0
    if price > 0 and balance and price > float(balance):
        score -= 50.0
    if item_name in {"LifeAlert", "First Aid Kit", "Faulty Insurance", "No Bust", "Second Chance"}:
        score += 6.0
    return score


def choose_purchase_option(request: DecisionRequest, plan: StrategicPlan) -> tuple[DecisionOption | None, DecisionTrace]:
    best_option: DecisionOption | None = None
    best_score = float("-inf")
    score_breakdown: dict[str, float] = {}

    for option in request.normalized_options:
        total = _score_purchase_option(option, plan, request)
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
            reason="no purchase options available",
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