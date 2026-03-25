from __future__ import annotations

from typing import Iterable

from .interfaces import DecisionOption, DecisionRequest
from .planner import StrategicPlan
from .tuning import tval
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
        # bootstrap_blackjack_edge: borrowing from Vinnie buys edge items we couldn't afford yet.
        "bootstrap_blackjack_edge": {"store": 14.0, "loan": 22.0, "stay_home": 18.0, "adventure": -18.0},
        "reduce_debt_risk": {"loan": 95.0, "pawn": 18.0, "marvin": -15.0, "adventure": -20.0},
        "contain_debt_escalation": {"loan": 105.0, "pawn": 22.0, "marvin": -18.0, "adventure": -28.0},
        "cashout_pawn_inventory": {"pawn": 108.0, "loan": 18.0, "store": -8.0, "marvin": -12.0, "adventure": -24.0},
        "blend_fraudulent_cash_safely": {"marvin": 24.0, "store": 8.0, "adventure": -15.0},
        "unlock_marvin": {"mechanic": 20.0, "store": 8.0, "adventure": 6.0},
        "exploit_marvin": {"marvin": 102.0, "loan": 48.0, "upgrade": 12.0, "mechanic": -12.0, "adventure": -10.0},
        "recover_from_car_trouble": {"mechanic": 92.0, "upgrade": 55.0, "stay_home": 18.0, "adventure": -40.0},
        "advance_mechanic_arc": {"mechanic": 92.0, "upgrade": 35.0, "marvin": -10.0},
        "repair_or_upgrade_gear": {"upgrade": 90.0, "mechanic": 72.0, "marvin": -10.0},
        "restore_blackjack_edge_after_breakage": {"upgrade": 95.0, "mechanic": 78.0, "store": 12.0, "adventure": -28.0},
        "reach_adventure_threshold": {"marvin": 26.0, "mechanic": 16.0, "adventure": 88.0},
        "exploit_adventure": {"adventure": 120.0, "marvin": 24.0, "loan": -5.0},
        "convert_millionaire_to_ending": {"upgrade": 14.0, "adventure": -30.0, "loan": -40.0},
        # push_next_rank: loan shark is a direct bankroll multiplier at rank 0-1 — far more
        # efficient than the store for a cash-poor player.  Adventure is also valid at rank 2+.
        "push_next_rank": {"marvin": 34.0, "store": 2.0, "upgrade": 18.0, "mechanic": 10.0, "adventure": 16.0, "loan": 44.0, "stay_home": -8.0},
    }
    goal_weights = mapping.get(goal, {})
    return sum(goal_weights.get(tag, 0.0) for tag in tags)


def _score_route_opportunity(tags: set[str], metadata: dict[str, object]) -> float:
    total = 0.0
    catalog_push_kind = str(metadata.get("catalog_push_kind", "") or "")
    catalog_push_spend = float(metadata.get("catalog_push_spend", 0) or 0)
    catalog_push_count = float(metadata.get("catalog_push_count", 0) or 0)
    catalog_push_priority = float(metadata.get("catalog_push_priority", 0) or 0)

    store_spend = float(metadata.get("store_spend", 0) or 0)
    store_actionable_count = float(metadata.get("store_actionable_count", 0) or 0)
    if "store" in tags and metadata.get("wants_store"):
        total += 92.0 + min(52.0, store_spend / 6.0)
        total += min(38.0, store_actionable_count * 14.0)
    if "store" in tags and metadata.get("catalog_push_active") and catalog_push_kind == "store":
        total += 64.0 + min(48.0, catalog_push_spend / 10.0) + min(32.0, catalog_push_count * 8.0)
        total += min(24.0, catalog_push_priority / 4.0)

    pawn_value = float(metadata.get("pawn_value", 0) or 0)
    if "pawn" in tags and metadata.get("wants_pawn"):
        total += 50.0 + min(36.0, pawn_value / 18.0)

    loan_pressure = float(metadata.get("loan_pressure", 0) or 0)
    if "loan" in tags and metadata.get("wants_loan"):
        total += 64.0 + min(36.0, loan_pressure / 4.0)
    # In poverty-escape mode the bot can't afford any mechanic quote; boosting the
    # loan shark ensures it visits Vinnie first to raise capital, breaking the
    # "try Tom → can't pay → try again" loop.
    if "loan" in tags and metadata.get("poverty_loan_mode"):
        total += 120.0
    if "mechanic" in tags and metadata.get("poverty_loan_mode"):
        total -= 80.0

    marvin_priority = float(metadata.get("marvin_priority", 0) or 0)
    marvin_future_priority = float(metadata.get("marvin_future_priority", 0) or 0)
    marvin_future_shortfall = float(metadata.get("marvin_future_shortfall", 0) or 0)
    if "marvin" in tags and metadata.get("wants_marvin"):
        total += 88.0 + min(54.0, marvin_priority / 2.0)
        if marvin_priority >= 72:
            total += 42.0
        elif marvin_priority >= 56:
            total += 28.0
        if marvin_future_priority >= 56 and 0 < marvin_future_shortfall <= 5000:
            total += 38.0
        elif marvin_future_priority >= 76 and 0 < marvin_future_shortfall <= 12000:
            total += 36.0
    if "marvin" in tags and metadata.get("catalog_push_active") and catalog_push_kind == "marvin":
        total += 72.0 + min(54.0, catalog_push_spend / 150.0) + min(36.0, catalog_push_count * 12.0)
        total += min(32.0, catalog_push_priority / 2.0)
    if (
        "loan" in tags
        and metadata.get("wants_loan")
        and metadata.get("wants_marvin")
        and marvin_priority <= 0
        and marvin_future_priority >= 56
        and 0 < marvin_future_shortfall <= 5000
    ):
        total += 28.0

    mechanic_urgency = float(metadata.get("mechanic_urgency", 0) or 0)
    if "mechanic" in tags and metadata.get("wants_mechanic"):
        total += 58.0 + min(30.0, mechanic_urgency / 3.0)

    upgrade_urgency = float(metadata.get("upgrade_urgency", 0) or 0)
    if "upgrade" in tags and metadata.get("wants_upgrade"):
        total += 46.0 + min(28.0, upgrade_urgency / 4.0)
    if "upgrade" in tags and metadata.get("wants_workbench_craft"):
        total += 54.0

    planner_goal = str(metadata.get("planner_goal", "") or "")
    if planner_goal == "push_next_rank":
        if "loan" in tags:
            total += 22.0
        if "marvin" in tags:
            total += 18.0
        if "upgrade" in tags:
            total += 12.0
        if "store" in tags and store_spend <= 260.0:
            total -= 12.0
    elif planner_goal == "exploit_marvin":
        if "loan" in tags:
            total += 18.0
            if marvin_priority <= 0 and marvin_future_priority >= 56 and 0 < marvin_future_shortfall <= 5000:
                total += 16.0
        if "upgrade" in tags and metadata.get("wants_workbench_craft"):
            total += 10.0

    adventure_readiness = float(metadata.get("adventure_readiness", 0) or 0)
    if "adventure" in tags and metadata.get("wants_adventure"):
        total += 48.0 + min(26.0, adventure_readiness / 3.0)

    if "stay_home" in tags and metadata.get("needs_recovery_day"):
        total += 8.0

    return total


def choose_route_option(request: DecisionRequest, plan: StrategicPlan) -> tuple[DecisionOption | None, DecisionTrace]:
    metadata = dict(request.metadata)
    game_state = dict(request.game_state)
    best_option: DecisionOption | None = None
    best_total = float("-inf")
    score_by_option: dict[str, float] = {}
    store_spend = float(metadata.get("store_spend", 0) or 0)
    pawn_value = float(metadata.get("pawn_value", 0) or 0)
    balance = float(game_state.get("balance", 0) or 0)
    rank = int(game_state.get("rank", 0) or 0)
    has_car = bool(game_state.get("has_car"))
    health = float(game_state.get("health", 100) or 100)
    sanity_val = float(game_state.get("sanity", 100) or 100)
    bankroll_emergency = bool(game_state.get("bankroll_emergency")) or balance <= 0
    fragile_post_car = bool(game_state.get("fragile_post_car"))
    startup_cash_floor_unmet = (
        not has_car
        and rank <= int(tval("route.startup.rank_max", 1))
        and balance < float(tval("route.startup.cash_floor", 220.0))
    )
    marvin_priority = float(metadata.get("marvin_priority", 0) or 0)
    marvin_future_priority = float(metadata.get("marvin_future_priority", 0) or 0)
    marvin_future_shortfall = float(metadata.get("marvin_future_shortfall", 0) or 0)
    marvin_window = bool(
        metadata.get("wants_marvin")
        and not metadata.get("urgent_medical")
        and health >= 62
        and sanity_val >= 34
        and (
            marvin_priority >= 56
            or (marvin_future_priority >= 56 and 0 < marvin_future_shortfall <= 5000)
            or (marvin_future_priority >= 76 and 0 < marvin_future_shortfall <= 12000)
        )
    )
    economy_growth_window = bool(
        has_car
        and not metadata.get("urgent_medical")
        and not metadata.get("wants_doctor")
        and health >= 60
        and sanity_val >= 30
        and rank <= 2
        and 350 <= balance <= 16000
    )

    for option in request.normalized_options:
        tags = _route_tags(option.label)
        total = _score_goal_alignment(plan.goal, tags)
        total += _score_route_opportunity(tags, metadata)
        # Personality bias: adventure_bias adjusts how willing the bot is to take road trips
        if "adventure" in tags:
            total += plan.personality.adventure_bias

        if startup_cash_floor_unmet:
            if "loan" in tags:
                total += float(tval("route.startup.loan_wants_bonus", 92.0)) if metadata.get("wants_loan") else float(tval("route.startup.loan_soft_bonus", 34.0))
            if "pawn" in tags:
                total += float(tval("route.startup.pawn_wants_bonus", 68.0)) if (metadata.get("wants_pawn") or pawn_value > 0) else float(tval("route.startup.pawn_soft_bonus", 22.0))
            if "medical" in tags:
                if metadata.get("wants_doctor") or health < 65 or sanity_val < 38:
                    total += float(tval("route.startup.medical_wants_bonus", 54.0))
                else:
                    total += float(tval("route.startup.medical_soft_bonus", 14.0))
            if "stay_home" in tags:
                total += float(tval("route.startup.stay_home_bonus", 36.0))
            if "mechanic" in tags:
                total -= float(tval("route.startup.mechanic_penalty", 30.0))
            if "marvin" in tags:
                total -= float(tval("route.startup.marvin_penalty", 78.0))
            if "adventure" in tags:
                total -= float(tval("route.startup.adventure_penalty", 86.0))
            if "store" in tags and store_spend <= 0:
                total -= float(tval("route.startup.store_no_spend_penalty", 42.0))

        if bankroll_emergency:
            if "loan" in tags and metadata.get("wants_loan"):
                total += float(tval("route.bankroll.loan_wants_bonus", 180.0))
            elif "loan" in tags:
                total -= float(tval("route.bankroll.loan_soft_penalty", 40.0))
            if "pawn" in tags and (metadata.get("wants_pawn") or pawn_value > 0):
                total += float(tval("route.bankroll.pawn_wants_bonus", 110.0))
            elif "pawn" in tags:
                total -= float(tval("route.bankroll.pawn_soft_penalty", 18.0))
            if "medical" in tags:
                total += float(tval("route.bankroll.medical_urgent_bonus", 80.0)) if metadata.get("urgent_medical") else float(tval("route.bankroll.medical_soft_bonus", 24.0))
            if "stay_home" in tags:
                total += float(tval("route.bankroll.stay_home_bonus", 46.0))
            if "mechanic" in tags or "marvin" in tags or "upgrade" in tags or "adventure" in tags:
                total -= float(tval("route.bankroll.high_risk_penalty", 165.0))
            if "store" in tags and store_spend <= 0:
                total -= float(tval("route.bankroll.store_no_spend_penalty", 90.0))

        if fragile_post_car:
            if "loan" in tags:
                total += float(tval("route.fragile.loan_bonus", 28.0))
            if "pawn" in tags:
                total += float(tval("route.fragile.pawn_bonus", 24.0))
            if "medical" in tags and metadata.get("wants_doctor"):
                total += float(tval("route.fragile.medical_bonus", 22.0))
            if "stay_home" in tags and metadata.get("needs_recovery_day"):
                total += float(tval("route.fragile.stay_home_recovery_bonus", 18.0))
            if "mechanic" in tags and not metadata.get("wants_mechanic"):
                total -= float(tval("route.fragile.mechanic_penalty", 72.0))
            if "marvin" in tags:
                total -= float(tval("route.fragile.marvin_penalty", 58.0))
            if "adventure" in tags:
                total -= float(tval("route.fragile.adventure_penalty", 64.0))
            if "store" in tags and store_spend <= 0:
                total -= float(tval("route.fragile.store_no_spend_penalty", 28.0))

        if metadata.get("urgent_medical"):
            total += 140.0 if "medical" in tags else -80.0
        # Proactive medical: even if not "urgent", boost doctor when injuries or low health/sanity
        injury_count = len(tuple(game_state.get("injuries", ()) or ()))
        status_count = len(tuple(game_state.get("statuses", ()) or ()))
        if not metadata.get("urgent_medical"):
            if "medical" in tags and (health < 65 or injury_count >= 1 or status_count >= 2):
                total += 60.0
            if "medical" in tags and sanity_val < 40:
                total += 40.0
        if marvin_window and "marvin" in tags:
            total += 46.0
            if plan.goal in {"exploit_marvin", "push_next_rank"}:
                total += 18.0
        if marvin_window and "loan" in tags and marvin_priority <= 0 and marvin_future_priority >= 56:
            total += 22.0
        if (
            metadata.get("wants_marvin")
            and metadata.get("wants_loan")
            and marvin_priority <= 0
            and marvin_future_priority >= 56
            and 0 < marvin_future_shortfall <= 5000
        ):
            if "loan" in tags:
                total += 36.0
            if "marvin" in tags:
                total -= 26.0
        if marvin_window and "medical" in tags and not metadata.get("wants_doctor"):
            total -= 38.0
        if marvin_window and "store" in tags and float(metadata.get("store_spend", 0) or 0) <= 260.0:
            total -= 16.0
        if metadata.get("needs_recovery_day") and "stay_home" in tags:
            total += 28.0
        if metadata.get("wants_doctor") and option.label == "Doctor's Office":
            total += 42.0
        if metadata.get("wants_witch") and option.label == "Witch Doctor's Tower":
            total += 34.0
        if metadata.get("wants_marvin") and "marvin" in tags:
            total += 22.0
        if metadata.get("wants_loan") and "loan" in tags:
            total += 24.0
        if metadata.get("wants_store") and "store" in tags:
            total += 12.0
        if metadata.get("wants_adventure") and "adventure" in tags:
            total += 14.0
        if metadata.get("wants_upgrade") and "upgrade" in tags:
            total += 18.0
        if metadata.get("wants_workbench_craft") and "upgrade" in tags:
            total += 18.0
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

        if economy_growth_window:
            if "loan" in tags:
                total += 36.0
            if "pawn" in tags and (pawn_value > 0 or metadata.get("wants_pawn")):
                total += 24.0
            if "upgrade" in tags and metadata.get("wants_workbench_craft"):
                total += 30.0
            if "store" in tags and store_spend > 0:
                total += 14.0
            if "stay_home" in tags:
                total -= 18.0
            if "medical" in tags and not metadata.get("wants_doctor"):
                total -= 20.0

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
            metadata={
                "plan": plan.to_dict(),
                "reason_code": "route:no_options",
                "expected_value_estimate": 0.0,
                "candidate_actions": [],
            },
        )
        return None, trace

    sorted_scores = sorted(score_by_option.values(), reverse=True)
    margin = sorted_scores[0] - sorted_scores[1] if len(sorted_scores) > 1 else sorted_scores[0]
    confidence = min(1.0, max(0.05, 0.45 + margin / 100.0))
    reason_code = "route:best_score"
    reason = (
        f"goal={plan.goal} selected {best_option.label} score={best_total:.1f} margin={margin:.1f} "
        f"risk={plan.personality.risk_tolerance}"
    )
    ranked = sorted(score_by_option.items(), key=lambda item: item[1], reverse=True)
    candidate_actions = [
        {
            "option_id": option_id,
            "score": round(score, 3),
        }
        for option_id, score in ranked[:6]
    ]
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
        metadata={
            "plan": plan.to_dict(),
            "reason_code": reason_code,
            "expected_value_estimate": float(best_total),
            "candidate_actions": candidate_actions,
            "constraint_profile": list(plan.personality.hard_constraints),
        },
    )
    return best_option, trace