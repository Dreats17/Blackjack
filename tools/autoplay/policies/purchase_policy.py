from __future__ import annotations

from ..config import STORE_MUST_HAVE_ITEMS
from ..interfaces import DecisionOption, DecisionRequest
from ..planner import StrategicPlan
from ..tuning import tval
from ..trace import DecisionTrace


def _score_purchase_option(option: DecisionOption, plan: StrategicPlan, request: DecisionRequest) -> float:
    p = plan.personality
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
    run_peak_balance = int(request_meta.get("run_peak_balance", balance) or balance)
    has_car = bool(request.game_state.get("has_car", False))
    health = int(request.game_state.get("health", 0) or 0)
    sanity = int(request.game_state.get("sanity", 0) or 0)

    # Personality: medical/food items get a health_caution boost
    if category in {"medical", "food"} and p.health_caution > 1.0:
        score += (p.health_caution - 1.0) * float(tval("purchase.medical_health_caution_multiplier", 14.0))
    # Personality: frugal mode penalises non-essential spending
    if p.frugal_mode and category in {"progression", "blackjack"} and item_name not in STORE_MUST_HAVE_ITEMS:
        score -= float(tval("purchase.frugal_nonessential_penalty", 12.0))

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
    # If affordable, and blackjack edge is high, nudge up score for high-impact items
    # Marvin item prioritization: always boost Marvin items, even more for deep runs
    if category == "marvin":
        rank = int(request.game_state.get("rank", 0) or 0)
        # If run is over 15k, play much safer: only buy Marvin items if they are a clear upgrade or needed for stability
        marvin_safe_peak = int(tval("purchase.marvin.safe_peak_threshold", 15000))
        marvin_deep_peak = int(tval("purchase.marvin.deep_peak_threshold", 10000))
        if run_peak_balance > marvin_safe_peak:
            # Only buy if item is not already owned or is a direct upgrade
            already_owned = option_meta.get("already_owned", False)
            is_upgrade = option_meta.get("is_upgrade", False)
            if not already_owned or is_upgrade:
                score += float(tval("purchase.marvin.safe_buy_bonus", 60.0)) * p.marvin_aggression
            else:
                score -= float(tval("purchase.marvin.safe_already_owned_penalty", 40.0))
            # If price is affordable, boost a bit, but avoid loans unless item is critical
            if price > 0 and balance and price <= float(balance):
                score += float(tval("purchase.marvin.safe_affordable_bonus", 10.0))
            elif price > 0 and balance and price > float(balance):
                score -= float(tval("purchase.marvin.safe_unaffordable_penalty", 30.0))
        else:
            # Under 15k — personality-scaled aggression
            score += float(tval("purchase.marvin.base_buy_bonus", 100.0)) * p.marvin_aggression
            if run_peak_balance > marvin_deep_peak and rank >= 2:
                score += float(tval("purchase.marvin.deep_run_bonus", 100.0)) * p.marvin_aggression
            if price > 0 and balance and price <= float(balance):
                score += float(tval("purchase.marvin.affordable_bonus", 25.0))
            elif price > 0 and balance and price > float(balance):
                score += float(tval("purchase.marvin.unaffordable_soft_bonus", 10.0))
    else:
        safe_peak = int(tval("purchase.general.safe_peak_threshold", 15000))
        if run_peak_balance > safe_peak:
            # Over 15k: play safe, avoid unnecessary purchases, penalize risky spending
            if price > 0 and balance and price > float(balance):
                score -= float(tval("purchase.general.safe_unaffordable_penalty", 80.0))
            elif price > 0 and balance and price <= float(balance):
                score -= float(tval("purchase.general.safe_affordable_penalty", 10.0))
        else:
            if price > 0 and balance and price > float(balance):
                score -= float(tval("purchase.general.unaffordable_penalty", 50.0))
            elif price > 0 and balance and price <= float(balance):
                # If blackjack edge is high, and item is blackjack/progression, boost score
                edge_score = int(request_meta.get("edge_score", 0))
                rank = int(request.game_state.get("rank", 0) or 0)
                if edge_score >= 5 and category in {"blackjack", "progression"}:
                    score += float(tval("purchase.general.edge_high_bonus", 10.0))
                elif edge_score >= 3 and category in {"blackjack", "progression"}:
                    score += float(tval("purchase.general.edge_mid_bonus", 5.0))
    if item_name in {"LifeAlert", "First Aid Kit", "Faulty Insurance", "No Bust", "Second Chance"}:
        score += float(tval("purchase.must_have_flat_bonus", 6.0))
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
            metadata={
                "plan": plan.to_dict(),
                "reason_code": "purchase:no_options",
                "expected_value_estimate": 0.0,
                "candidate_actions": [],
            },
        )
        return None, trace

    sorted_scores = sorted(score_breakdown.values(), reverse=True)
    margin = sorted_scores[0] - sorted_scores[1] if len(sorted_scores) > 1 else sorted_scores[0]
    confidence = min(1.0, max(0.1, 0.5 + margin / 120.0))
    ranked = sorted(score_breakdown.items(), key=lambda item: item[1], reverse=True)
    candidate_actions = [{"option_id": option_id, "score": round(score, 3)} for option_id, score in ranked[:6]]
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
        metadata={
            "plan": plan.to_dict(),
            "reason_code": "purchase:best_score",
            "expected_value_estimate": float(best_score),
            "candidate_actions": candidate_actions,
            "risk_band": plan.personality.risk_tolerance,
        },
    )
    return best_option, trace