from __future__ import annotations

from ..interfaces import DecisionOption, DecisionRequest
from ..planner import StrategicPlan
from ..trace import DecisionTrace


def _metadata_number(metadata: dict[str, object], key: str, default: float = 0.0) -> float:
    return float(metadata.get(key, default) or default)


def _metadata_bool(metadata: dict[str, object], key: str) -> bool:
    return bool(metadata.get(key))


def _recommended_blackjack_action(
    total: int,
    soft_total: int,
    dealer_upcard: int,
    *,
    can_double: bool = False,
    can_split: bool = False,
    can_surrender: bool = False,
    pair_value: int | None = None,
) -> str:
    if can_split and pair_value is not None:
        if pair_value in {11, 8}:
            return "split"
        if pair_value in {10, 5}:
            pass
        elif pair_value == 9 and dealer_upcard not in {7, 10, 11}:
            return "split"
        elif pair_value in {2, 3, 7} and dealer_upcard <= 7:
            return "split"
        elif pair_value == 6 and dealer_upcard <= 6:
            return "split"

    if can_surrender and not soft_total:
        if total == 16 and dealer_upcard in {9, 10, 11}:
            return "surrender"
        if total == 15 and dealer_upcard == 10:
            return "surrender"

    if can_double:
        if not soft_total and total == 11:
            return "double"
        if not soft_total and total == 10 and dealer_upcard <= 9:
            return "double"
        if not soft_total and total == 9 and 3 <= dealer_upcard <= 6:
            return "double"
        if soft_total and soft_total in {17, 18} and 3 <= dealer_upcard <= 6:
            return "double"

    if soft_total:
        if soft_total <= 17:
            return "hit"
        if soft_total == 18 and dealer_upcard >= 9:
            return "hit"
        return "stand"

    if total <= 11:
        return "hit"
    if total == 12 and 4 <= dealer_upcard <= 6:
        return "stand"
    if 13 <= total <= 16 and dealer_upcard <= 6:
        return "stand"
    if total >= 17:
        return "stand"
    return "hit"


def _should_use_peek(action: str, total: int, soft_total: int, bet: int, balance: int) -> bool:
    if action == "stand":
        return False
    if action == "hit" and total <= 11 and not soft_total:
        return False
    if action == "double" and bet < max(100, balance // 12):
        return False
    if action == "surrender":
        return True
    if total >= 12:
        return True
    return bet >= max(150, balance // 10)


def choose_blackjack_action(request: DecisionRequest, plan: StrategicPlan) -> tuple[DecisionOption | None, DecisionTrace]:
    metadata = dict(request.metadata)
    total = int(_metadata_number(metadata, "total"))
    soft_total = int(_metadata_number(metadata, "soft_total"))
    dealer_upcard = int(_metadata_number(metadata, "dealer_upcard"))
    bet = int(_metadata_number(metadata, "bet"))
    balance = int(_metadata_number(metadata, "balance"))
    can_double = bool(metadata.get("can_double"))
    can_split = bool(metadata.get("can_split"))
    can_surrender = bool(metadata.get("can_surrender"))
    can_peek = bool(metadata.get("can_peek"))
    pair_value = metadata.get("pair_value")
    pair_value = None if pair_value in {None, "", 0} else int(pair_value)
    simulated_next_total = metadata.get("simulated_next_total")
    next_total = None if simulated_next_total in {None, ""} else int(simulated_next_total)
    has_no_bust = bool(metadata.get("has_no_bust"))
    has_imminent_blackjack = bool(metadata.get("has_imminent_blackjack"))

    action = _recommended_blackjack_action(
        total,
        soft_total,
        dealer_upcard,
        can_double=can_double,
        can_split=can_split,
        can_surrender=can_surrender,
        pair_value=pair_value,
    )

    if can_peek and _should_use_peek(action, total, soft_total, bet, balance) and next_total is not None:
        if action == "surrender":
            if has_imminent_blackjack or has_no_bust or next_total <= 21:
                action = "hit"
        elif action == "double":
            if not has_imminent_blackjack and not has_no_bust and next_total > 21:
                action = "stand" if total >= 12 else "hit"
            elif not has_imminent_blackjack and next_total < 17:
                action = "hit"
        elif action == "hit":
            if has_imminent_blackjack or has_no_bust:
                action = "hit"
            elif next_total > 21:
                if can_surrender and not soft_total and total in {15, 16} and dealer_upcard in {9, 10, 11}:
                    action = "surrender"
                else:
                    action = "stand"

    selected = None
    score_breakdown: dict[str, float] = {}
    for option in request.normalized_options:
        score = 1.0 if str(option.value or option.label) == action else 0.0
        score_breakdown[option.option_id] = score
        if score > 0.0:
            selected = option

    confidence = 0.92 if selected is not None else 0.0
    trace = DecisionTrace(
        cycle=request.metadata.get("cycle"),
        day=request.metadata.get("day"),
        context=request.stable_context_id or request.request_type,
        request_type=request.request_type,
        strategic_goal=plan.goal,
        chosen_action=str(selected.value if selected and selected.value is not None else action),
        reason=f"goal={plan.goal} blackjack_action={action} total={total} soft={soft_total} dealer={dealer_upcard}",
        confidence=confidence,
        options=tuple(option.label for option in request.normalized_options),
        game_state_summary=dict(request.game_state),
        score_breakdown=score_breakdown,
        metadata={"plan": plan.to_dict()},
    )
    return selected, trace


def choose_insurance_option(request: DecisionRequest, plan: StrategicPlan) -> tuple[DecisionOption | None, DecisionTrace]:
    metadata = dict(request.metadata)
    can_afford = bool(metadata.get("can_afford"))
    has_whispers = bool(metadata.get("has_dealers_whispers"))
    dealer_blackjack = bool(metadata.get("dealer_has_blackjack"))
    decision = "yes" if can_afford and has_whispers and dealer_blackjack else "no"

    selected = None
    score_breakdown: dict[str, float] = {}
    for option in request.normalized_options:
        value = str(option.value or option.label).lower()
        score = 1.0 if value == decision else 0.0
        score_breakdown[option.option_id] = score
        if score > 0.0:
            selected = option

    trace = DecisionTrace(
        cycle=request.metadata.get("cycle"),
        day=request.metadata.get("day"),
        context=request.stable_context_id or request.request_type,
        request_type=request.request_type,
        strategic_goal=plan.goal,
        chosen_action=decision,
        reason=f"goal={plan.goal} insurance={decision} whispers={has_whispers} dealer_blackjack={dealer_blackjack}",
        confidence=0.95,
        options=tuple(option.label for option in request.normalized_options),
        game_state_summary=dict(request.game_state),
        score_breakdown=score_breakdown,
        metadata={"plan": plan.to_dict()},
    )
    return selected, trace


def choose_second_chance_option(request: DecisionRequest, plan: StrategicPlan) -> tuple[DecisionOption | None, DecisionTrace]:
    metadata = dict(request.metadata)
    free_hand = bool(metadata.get("free_hand"))
    bet = int(_metadata_number(metadata, "bet"))
    balance = int(_metadata_number(metadata, "balance"))
    insurance_bet = int(_metadata_number(metadata, "insurance_bet"))
    status = str(metadata.get("status", ""))
    reserve = int(_metadata_number(metadata, "reserve"))
    edge_score = int(_metadata_number(metadata, "edge_score"))

    replay = False
    if not free_hand and bet > 0:
        if not (status == "Dealer Blackjack" and insurance_bet > 0):
            post_loss_balance = balance - bet
            loss_ratio = bet / max(balance, 1)
            if post_loss_balance < reserve:
                replay = True
            elif status == "Player Bust":
                replay = loss_ratio >= 0.22 or (edge_score >= 5 and bet >= max(100, balance // 8))
            elif status == "Dealer Blackjack":
                replay = loss_ratio >= 0.18 and edge_score >= 4
            else:
                replay = loss_ratio >= 0.20 or (edge_score >= 6 and bet >= max(150, balance // 7))

    decision = "yes" if replay else "no"
    selected = None
    score_breakdown: dict[str, float] = {}
    for option in request.normalized_options:
        value = str(option.value or option.label).lower()
        score = 1.0 if value == decision else 0.0
        score_breakdown[option.option_id] = score
        if score > 0.0:
            selected = option

    trace = DecisionTrace(
        cycle=request.metadata.get("cycle"),
        day=request.metadata.get("day"),
        context=request.stable_context_id or request.request_type,
        request_type=request.request_type,
        strategic_goal=plan.goal,
        chosen_action=decision,
        reason=f"goal={plan.goal} second_chance={decision} status={status} edge={edge_score}",
        confidence=0.9,
        options=tuple(option.label for option in request.normalized_options),
        game_state_summary=dict(request.game_state),
        score_breakdown=score_breakdown,
        metadata={"plan": plan.to_dict()},
    )
    return selected, trace


def choose_blackjack_bet(request: DecisionRequest, plan: StrategicPlan) -> tuple[int | None, DecisionTrace]:
    metadata = dict(request.metadata)
    state = dict(request.game_state)
    balance = int(_metadata_number(metadata, "balance", state.get("balance", 0)))
    fake_cash = int(_metadata_number(metadata, "fake_cash"))
    total_available = balance + fake_cash
    min_bet = int(_metadata_number(metadata, "min_bet", 1))
    target = int(_metadata_number(metadata, "target"))
    floor = int(_metadata_number(metadata, "floor"))
    distance = int(_metadata_number(metadata, "distance"))
    store_budget = int(_metadata_number(metadata, "store_budget"))
    edge_score = int(_metadata_number(metadata, "edge_score"))
    day = int(_metadata_number(metadata, "day", state.get("day", 0)))
    stall_days = int(_metadata_number(metadata, "stall_days"))
    pending_marvin_price = int(_metadata_number(metadata, "pending_marvin_price"))
    pending_marvin_shortfall = int(_metadata_number(metadata, "pending_marvin_shortfall"))
    tuner_bet_ratio = _metadata_number(metadata, "tuner_bet_ratio")
    tuner_bet_ratio_safe = _metadata_number(metadata, "tuner_bet_ratio_safe")
    tuner_max_ratio = _metadata_number(metadata, "tuner_max_ratio")
    tuner_pressure_factor = _metadata_number(metadata, "tuner_pressure_factor")
    tuner_surplus_push = _metadata_number(metadata, "tuner_surplus_push")
    rank = int(_metadata_number(metadata, "rank", state.get("rank", 0)))
    health = int(_metadata_number(metadata, "health", state.get("health", 0)))
    sanity = int(_metadata_number(metadata, "sanity", state.get("sanity", 0)))
    has_car = bool(state.get("has_car"))
    dealer_happiness = int(_metadata_number(metadata, "dealer_happiness", state.get("dealer_happiness", 0)))

    wants_store = _metadata_bool(metadata, "wants_store")
    wants_pawn = _metadata_bool(metadata, "wants_pawn")
    wants_doctor = _metadata_bool(metadata, "wants_doctor")
    progression_ready = _metadata_bool(metadata, "progression_ready")
    wants_millionaire_push = _metadata_bool(metadata, "wants_millionaire_push")
    pending_marvin_active = _metadata_bool(metadata, "pending_marvin_active")
    early_caution = _metadata_bool(metadata, "early_caution")
    stranded_no_car = _metadata_bool(metadata, "stranded_no_car")
    survival_mode = _metadata_bool(metadata, "survival_mode")
    needs_car = _metadata_bool(metadata, "needs_car")
    has_extra_round_item = _metadata_bool(metadata, "has_extra_round_item")
    urgent_doctor = _metadata_bool(metadata, "urgent_doctor")
    has_met_tom = _metadata_bool(metadata, "has_met_tom")
    has_met_frank = _metadata_bool(metadata, "has_met_frank")
    has_met_oswald = _metadata_bool(metadata, "has_met_oswald")
    has_faulty_insurance = _metadata_bool(metadata, "has_faulty_insurance")
    wants_map_unlock = _metadata_bool(metadata, "wants_map_unlock")
    phase = str(metadata.get("phase", ""))
    stalled_run = stall_days >= (10 if day <= 30 else 14)
    pre_tom_breakout_window = (
        needs_car
        and phase == "car_rush"
        and not has_car
        and not has_met_tom
        and not urgent_doctor
        and not wants_doctor
        and balance >= 170
        and balance < 200
        and health >= 70
        and sanity >= 40
    )
    mechanic_threshold_push_window = (
        needs_car
        and phase == "car_rush"
        and not has_car
        and not has_met_tom
        and not urgent_doctor
        and not wants_doctor
        and health >= 60
        and sanity >= 34
        and balance >= 160
        and 0 < (200 - balance) <= 40
    )
    mechanic_gap = max(0, 200 - balance) if needs_car and not has_met_tom else 0
    low_balance_stall_window = (
        needs_car
        and phase == "car_rush"
        and not has_car
        and not has_met_tom
        and not urgent_doctor
        and not wants_doctor
        and balance < 160
    )
    midgame_growth_window = (
        has_car
        and rank <= 1
        and progression_ready
        and phase == "car_ready"
        and not wants_store
        and not wants_pawn
        and not wants_doctor
        and not urgent_doctor
        and not survival_mode
        and not pending_marvin_active
        and health >= 62
        and sanity >= 34
        and edge_score >= 2
        and 1200 <= balance < 8000
    )

    if total_available <= 0:
        trace = DecisionTrace(
            cycle=request.metadata.get("cycle"),
            day=day,
            context=request.stable_context_id or request.request_type,
            request_type=request.request_type,
            strategic_goal=plan.goal,
            chosen_action="0",
            reason=f"goal={plan.goal} blackjack_bet_empty_bankroll",
            confidence=0.95,
            options=tuple(option.label for option in request.normalized_options),
            game_state_summary=state,
            metadata={"plan": plan.to_dict()},
        )
        return 0, trace

    if phase == "car_rush":
        if balance < 100:
            ratio = 0.36
        elif balance < 200:
            ratio = 0.30
        elif balance < 350:
            ratio = 0.22
        else:
            ratio = 0.14
    elif phase == "million_rush" and wants_millionaire_push:
        if balance >= 600000 and has_extra_round_item and dealer_happiness >= 85:
            ratio = max(tuner_bet_ratio, 0.50)
        else:
            ratio = max(tuner_bet_ratio, 0.34 if balance < 500000 else 0.28)
    else:
        ratio = tuner_bet_ratio if progression_ready else tuner_bet_ratio_safe
    if stranded_no_car:
        if balance < 120:
            ratio = max(ratio, 0.42)
        elif balance < 250:
            ratio = max(ratio, 0.38)
        elif balance < 600:
            ratio = max(ratio, 0.34)
        else:
            ratio = max(ratio, 0.28)
    if balance >= 25000 and edge_score >= 6:
        ratio = min(ratio, 0.30 if balance < 100000 else 0.18)
    if stalled_run and not survival_mode:
        if phase == "car_rush":
            ratio = max(ratio, 0.26 if balance < 350 else 0.18)
        elif rank <= 1:
            ratio = max(ratio, 0.22)
    if midgame_growth_window:
        if balance < 2500:
            ratio = max(ratio, 0.34 if edge_score >= 4 else 0.30)
        elif balance < 5000:
            ratio = max(ratio, 0.30 if edge_score >= 4 else 0.26)
        else:
            ratio = max(ratio, 0.24)
    if pending_marvin_active and not survival_mode:
        if pending_marvin_shortfall > 0:
            ratio = min(ratio, 0.12 if edge_score >= 5 else 0.10)
        else:
            ratio = min(ratio, 0.06)

    if survival_mode:
        if phase == "car_rush":
            ratio = min(ratio, 0.18 if balance >= 200 else 0.22)
        elif balance < 10000:
            ratio = min(ratio, 0.14)
        else:
            ratio = min(ratio, 0.12)
    elif plan.goal == "restock_supplies" and wants_store:
        ratio = min(ratio, 0.18 if balance < 1000 else 0.14)
    elif plan.goal in {"contain_debt_escalation", "reduce_debt_risk"}:
        ratio = min(ratio, 0.16 if balance < 10000 else 0.12)
    elif wants_pawn and balance < 500:
        ratio = min(ratio, 0.18)
    if stranded_no_car:
        ratio = max(ratio, 0.22 if balance >= 1000 else 0.28)
    if low_balance_stall_window:
        if balance < 80:
            ratio = min(ratio, 0.22)
        elif balance < 120:
            ratio = min(ratio, 0.18)
        else:
            ratio = min(ratio, 0.16)
    if pre_tom_breakout_window:
        if balance < 80:
            ratio = max(ratio, 0.52)
        elif balance < 120:
            ratio = max(ratio, 0.46)
        elif balance < 160:
            ratio = max(ratio, 0.40)
        else:
            ratio = max(ratio, 0.34)
    if mechanic_threshold_push_window and balance > 0:
        ratio = max(ratio, min(0.62, (mechanic_gap / max(balance, 1)) + 0.10))
    if needs_car and stranded_no_car and phase == "car_rush":
        if not has_met_tom:
            if balance < 80:
                ratio = max(ratio, 0.52)
            elif balance < 120:
                ratio = max(ratio, 0.46)
            elif balance < 160:
                ratio = max(ratio, 0.34)
            elif balance < 200:
                ratio = max(ratio, 0.26)
    if early_caution:
        if phase == "car_rush" and balance < 200:
            ratio = min(ratio, 0.18 if urgent_doctor or wants_doctor else 0.16)
        elif balance < 150:
            ratio = max(ratio, 0.22)
        elif balance < 350:
            ratio = max(ratio, 0.18)
        elif balance < 900:
            ratio = min(ratio, 0.12)
        else:
            ratio = min(ratio, 0.10)
    if balance >= 25000 and edge_score >= 6:
        ratio = min(ratio, 0.30 if balance < 100000 else 0.18)

    if phase != "car_rush" and balance < 120:
        ratio = min(ratio, 0.24)
    elif phase != "car_rush" and balance < 250 and rank == 0:
        ratio = min(ratio, 0.30)
    if needs_car and stranded_no_car and phase == "car_rush":
        if not has_met_tom:
            if balance >= 200:
                ratio = min(ratio, 0.12)
        elif not has_met_frank and balance >= 200:
            ratio = min(ratio, 0.12)

    if distance and distance <= max(100, int(balance * 0.8)):
        if phase == "car_rush":
            pressure_factor = 0.9
        elif phase == "million_rush" and wants_millionaire_push:
            pressure_factor = 0.9 if balance < 500000 else 0.82
        else:
            pressure_factor = tuner_pressure_factor if progression_ready else max(0.5, tuner_pressure_factor - 0.14)
        if stranded_no_car:
            pressure_factor = max(pressure_factor, 0.94 if balance < 1000 else 0.82)
        if stalled_run and not survival_mode:
            pressure_factor = max(pressure_factor, 0.88 if rank <= 1 else 0.80)
        pressure_bet = int(distance * pressure_factor)
    else:
        pressure_bet = 0
    if mechanic_threshold_push_window:
        pressure_bet = max(pressure_bet, mechanic_gap)

    if phase == "car_rush":
        if balance < 100:
            max_ratio = 0.42
        elif balance < 200:
            max_ratio = 0.34
        elif balance < 350:
            max_ratio = 0.26
        else:
            max_ratio = 0.18
    elif phase == "million_rush" and wants_millionaire_push:
        if balance >= 600000 and has_extra_round_item and dealer_happiness >= 85:
            max_ratio = 0.72
        else:
            max_ratio = 0.62 if balance < 500000 else 0.52
    else:
        max_ratio = tuner_max_ratio if progression_ready else min(tuner_max_ratio, 0.45)
    if stranded_no_car:
        if balance < 120:
            max_ratio = max(max_ratio, 0.55)
        elif balance < 250:
            max_ratio = max(max_ratio, 0.50)
        elif balance < 600:
            max_ratio = max(max_ratio, 0.46)
        else:
            max_ratio = max(max_ratio, 0.40)
    if balance >= 25000 and edge_score >= 6:
        max_ratio = min(max_ratio, 0.38 if balance < 100000 else 0.24)
    if stalled_run and not survival_mode:
        if phase == "car_rush":
            max_ratio = max(max_ratio, 0.36 if balance < 350 else 0.24)
        elif rank <= 1:
            max_ratio = max(max_ratio, 0.34)
    if midgame_growth_window:
        if balance < 2500:
            max_ratio = max(max_ratio, 0.78 if edge_score >= 4 else 0.70)
        elif balance < 5000:
            max_ratio = max(max_ratio, 0.70 if edge_score >= 4 else 0.62)
        else:
            max_ratio = max(max_ratio, 0.58)
    if pending_marvin_active and not survival_mode:
        if pending_marvin_shortfall > 0:
            max_ratio = min(max_ratio, 0.18 if edge_score >= 5 else 0.15)
        else:
            max_ratio = min(max_ratio, 0.10)

    if survival_mode:
        if phase == "car_rush":
            max_ratio = min(max_ratio, 0.24)
        elif balance < 10000:
            max_ratio = min(max_ratio, 0.20)
        else:
            max_ratio = min(max_ratio, 0.16)
    elif plan.goal == "restock_supplies" and wants_store:
        max_ratio = min(max_ratio, 0.22 if balance < 1000 else 0.18)
    elif plan.goal in {"contain_debt_escalation", "reduce_debt_risk"}:
        max_ratio = min(max_ratio, 0.20 if balance < 10000 else 0.16)
    elif wants_pawn and balance < 500:
        max_ratio = min(max_ratio, 0.22)
    if stranded_no_car:
        max_ratio = max(max_ratio, 0.34 if balance >= 1000 else 0.40)
    if low_balance_stall_window:
        if balance < 80:
            max_ratio = min(max_ratio, 0.24)
        elif balance < 120:
            max_ratio = min(max_ratio, 0.20)
        else:
            max_ratio = min(max_ratio, 0.18)
    if pre_tom_breakout_window:
        if balance < 80:
            max_ratio = max(max_ratio, 0.66)
        elif balance < 120:
            max_ratio = max(max_ratio, 0.60)
        elif balance < 160:
            max_ratio = max(max_ratio, 0.54)
        else:
            max_ratio = max(max_ratio, 0.46)
    if mechanic_threshold_push_window and balance > 0:
        max_ratio = max(max_ratio, min(0.78, (mechanic_gap / max(balance, 1)) + 0.18))
    if needs_car and stranded_no_car and phase == "car_rush":
        if not has_met_tom:
            if balance < 80:
                max_ratio = max(max_ratio, 0.66)
            elif balance < 120:
                max_ratio = max(max_ratio, 0.60)
            elif balance < 160:
                max_ratio = max(max_ratio, 0.50)
            elif balance < 200:
                max_ratio = max(max_ratio, 0.40)
    if early_caution:
        if phase == "car_rush" and balance < 200:
            max_ratio = min(max_ratio, 0.22 if urgent_doctor or wants_doctor else 0.18)
        elif balance < 150:
            max_ratio = min(max_ratio, 0.16)
        elif balance < 350:
            max_ratio = min(max_ratio, 0.14)
        elif balance < 900:
            max_ratio = min(max_ratio, 0.12)
        else:
            max_ratio = min(max_ratio, 0.10)
    if balance >= 25000 and edge_score >= 6:
        max_ratio = min(max_ratio, 0.38 if balance < 100000 else 0.24)

    if phase != "car_rush" and balance < 120:
        max_ratio = min(max_ratio, 0.28)
    elif phase != "car_rush" and balance < 250 and rank == 0:
        max_ratio = min(max_ratio, 0.36)
    if needs_car and stranded_no_car and phase == "car_rush":
        if not has_met_tom:
            if balance >= 200:
                max_ratio = min(max_ratio, 0.16)
        elif not has_met_frank and balance >= 200:
            max_ratio = min(max_ratio, 0.18)
    max_ratio_bet = max(min_bet, int(balance * max_ratio))
    base_bet = max(min_bet, int(balance * ratio))
    bet = max(base_bet, min(max_ratio_bet, pressure_bet))

    if floor and balance > floor:
        if wants_doctor:
            floor_buffer = max(0, int(floor * 0.08))
        elif progression_ready:
            floor_buffer = 0
        else:
            floor_buffer = max(40, int(floor * 0.04))

        protected_floor = max(0, floor - floor_buffer)
        surplus = balance - protected_floor
        if surplus > 0:
            surplus_push = max(min_bet, int(surplus * (tuner_surplus_push if progression_ready else max(0.45, tuner_surplus_push - 0.18))))
            bet = min(max_ratio_bet, max(bet, surplus_push))
        bet = min(bet, max(min_bet, balance - protected_floor))

    if needs_car:
        if stranded_no_car and not has_met_tom:
            if balance >= 200:
                bet = min(bet, max(min_bet, balance - 180))
        if balance >= 75:
            mechanic_hold = 0
            if not has_met_tom:
                if balance >= 200:
                    mechanic_hold = max(mechanic_hold, 200)
            elif not has_met_frank and balance >= 200:
                mechanic_hold = max(mechanic_hold, 200)
            if not has_met_oswald and balance >= 850:
                mechanic_hold = max(mechanic_hold, 850)
            if mechanic_hold:
                bet = min(bet, max(min_bet, balance - mechanic_hold))

        for reserve_key in ("car_progress_reserve", "mechanic_purchase_reserve", "known_car_repair_reserve"):
            reserve = int(_metadata_number(metadata, reserve_key))
            if reserve:
                bet = min(bet, max(min_bet, balance - reserve))

        if day >= 4 and balance >= 150:
            if pre_tom_breakout_window:
                reserve = 55 if balance < 220 else 75 if balance < 320 else 95
            elif stranded_no_car:
                reserve = 55 if balance < 220 else 75 if balance < 320 else 95
            elif balance < 220:
                reserve = 150
            elif balance < 320:
                reserve = 190
            else:
                reserve = 230
            bet = min(bet, max(min_bet, balance - reserve))
        if balance >= 200:
            if stranded_no_car:
                reserve = 70 if balance < 350 else 95 if balance < 900 else 120
            elif day < 5:
                if balance < 260:
                    reserve = 90
                elif balance < 350:
                    reserve = 120
                elif balance < 500:
                    reserve = 160
                else:
                    reserve = 220
            elif balance < 350:
                reserve = 125
            elif balance < 900:
                reserve = 175
            else:
                reserve = 250
            bet = min(bet, max(min_bet, balance - reserve))
        elif day < 5 and balance >= 120:
            reserve = 55 if balance < 160 else 85
            bet = min(bet, max(min_bet, balance - reserve))
        elif day < 5:
            bet = max(bet, min(balance, max(min_bet, int(balance * 0.4))))

        if (not stranded_no_car) and balance >= 100 and not (has_met_tom or has_met_frank or has_met_oswald):
            bet = min(bet, max(min_bet, balance - (200 if day >= 5 and balance >= 200 else 100)))
        if (not stranded_no_car) and balance >= 200 and not has_met_tom:
            bet = min(bet, max(min_bet, balance - 200))
        if (not stranded_no_car) and balance >= 200 and has_met_tom and not has_met_frank and not has_car:
            bet = min(bet, max(min_bet, balance - 200))
        if (not stranded_no_car) and day >= 8 and balance >= 350 and not has_met_tom:
            bet = min(bet, max(min_bet, balance - 350))
        if early_caution:
            if balance >= 700:
                reserve = 240
            elif balance >= 350:
                reserve = 180
            elif balance >= 180:
                reserve = 110
            else:
                reserve = 55
            bet = min(bet, max(min_bet, balance - reserve))

    elif has_car:
        if balance < 150:
            reserve = 35
            cap_ratio = 0.22 if progression_ready else 0.14
        elif balance < 400:
            reserve = 50
            cap_ratio = 0.32 if progression_ready else 0.22
        elif balance < 1000:
            reserve = 85
            cap_ratio = 0.42 if progression_ready else 0.28
        else:
            reserve = 150
            cap_ratio = 0.46 if progression_ready else 0.28

        if wants_doctor:
            reserve = max(reserve, 120 if has_faulty_insurance else 260)
            cap_ratio = min(cap_ratio, 0.16)
        elif wants_store and store_budget:
            reserve = max(reserve, store_budget + 30)
            cap_ratio = min(cap_ratio, 0.30)
        elif wants_pawn:
            reserve = max(reserve, 90)
            cap_ratio = min(cap_ratio, 0.26)
        elif sanity < 20 or health < 50:
            reserve = max(reserve, 150)
            cap_ratio = min(cap_ratio, 0.15)

        if plan.goal in {"contain_debt_escalation", "reduce_debt_risk"}:
            reserve = max(reserve, 140)
            cap_ratio = min(cap_ratio, 0.18)
        elif plan.goal == "restock_supplies" and wants_store and store_budget:
            reserve = max(reserve, store_budget + 45)
            cap_ratio = min(cap_ratio, 0.24)

        if floor:
            reserve = max(reserve, floor)

        if pending_marvin_active:
            if pending_marvin_shortfall <= 0:
                reserve = max(reserve, pending_marvin_price)
                cap_ratio = min(cap_ratio, 0.10)
            elif fake_cash > 0:
                reserve = max(reserve, max(180, int(balance * 0.75)))
                cap_ratio = min(cap_ratio, 0.18 if edge_score >= 5 else 0.14)

        if phase == "million_rush" and wants_millionaire_push:
            if balance < 250000:
                reserve = min(reserve, max(25000, int(balance * 0.36)))
                cap_ratio = max(cap_ratio, 0.56)
            elif balance < 500000:
                reserve = min(reserve, max(90000, int(balance * 0.42)))
                cap_ratio = max(cap_ratio, 0.48)
            else:
                reserve = min(reserve, max(220000, int(balance * 0.5)))
                cap_ratio = max(cap_ratio, 0.38)

        if rank == 1 and not wants_store and not wants_doctor:
            reserve = min(reserve, 80 if balance < 5000 else 120)
            cap_ratio = max(cap_ratio, 0.62 if balance < 5000 else 0.56)
        elif rank == 0 and not wants_store and not wants_doctor and balance >= 250:
            reserve = min(reserve, 55 if balance < 400 else 80 if balance < 1000 else 120)
            cap_ratio = max(cap_ratio, 0.42 if balance < 400 else 0.54 if balance < 1000 else 0.58)
        elif rank == 2 and progression_ready:
            reserve = min(reserve, max(180, int(floor * 0.78)))
            cap_ratio = max(cap_ratio, 0.68)
        elif rank >= 3 and progression_ready:
            reserve = min(reserve, max(220, int(floor * 0.92)))
            cap_ratio = max(cap_ratio, 0.34)

        if edge_score >= 6 and balance >= 25000:
            reserve = max(reserve, int(balance * (0.72 if balance < 100000 else 0.82)))
            cap_ratio = min(cap_ratio, 0.34 if balance < 100000 else 0.22)

        if wants_map_unlock:
            if balance >= 7000:
                reserve = max(reserve, 6000)
            elif balance >= 3000:
                reserve = max(reserve, 2500)
            elif balance >= 1200:
                reserve = max(reserve, 1200)
            cap_ratio = min(cap_ratio, 0.22)

        if midgame_growth_window:
            if balance < 2500:
                reserve = min(reserve, 90 if rank >= 1 else 110)
                cap_ratio = max(cap_ratio, 0.74 if rank >= 1 else 0.66)
            elif balance < 5000:
                reserve = min(reserve, 120)
                cap_ratio = max(cap_ratio, 0.66 if rank >= 1 else 0.60)
            else:
                reserve = min(reserve, 160)
                cap_ratio = max(cap_ratio, 0.58)

        stabilized_cap = max(min_bet, int(balance * cap_ratio))
        bet = min(bet, stabilized_cap)
        if balance > reserve:
            bet = min(bet, max(min_bet, balance - reserve))

    if mechanic_threshold_push_window:
        bet = max(bet, min(total_available, max(min_bet, mechanic_gap)))
    if low_balance_stall_window:
        if balance < 80:
            conservative_cap = max(min_bet, int(balance * 0.22))
        elif balance < 120:
            conservative_cap = max(min_bet, int(balance * 0.18))
        else:
            conservative_cap = max(min_bet, int(balance * 0.16))
        bet = min(bet, conservative_cap)

    if fake_cash > 0 and not wants_doctor and not urgent_doctor:
        if health >= 48 and sanity >= 24:
            if pending_marvin_active and pending_marvin_shortfall <= 0:
                blend_slice = 0
            elif pending_marvin_active:
                target_blend = max(200, pending_marvin_shortfall)
                if edge_score >= 6:
                    blend_slice = min(fake_cash, max(400, int(target_blend * 0.45)))
                elif edge_score >= 4:
                    blend_slice = min(fake_cash, max(250, int(target_blend * 0.30)))
                else:
                    blend_slice = min(fake_cash, max(150, int(target_blend * 0.18)))
            elif edge_score >= 6:
                blend_slice = min(fake_cash, max(1000, int(fake_cash * 0.75)))
            elif edge_score >= 4:
                blend_slice = min(fake_cash, max(500, int(fake_cash * 0.55)))
            else:
                blend_slice = min(fake_cash, max(200, int(fake_cash * 0.30)))
            if blend_slice > 0:
                bet = max(bet, min(total_available, max(min_bet, balance + blend_slice)))

    if bet > total_available:
        bet = int(total_available)
    if bet < min_bet:
        bet = min(total_available, min_bet)

    trace = DecisionTrace(
        cycle=request.metadata.get("cycle"),
        day=day,
        context=request.stable_context_id or request.request_type,
        request_type=request.request_type,
        strategic_goal=plan.goal,
        chosen_action=str(bet),
        reason=f"goal={plan.goal} blackjack_bet phase={phase} survival={survival_mode} edge={edge_score}",
        confidence=0.88,
        options=tuple(option.label for option in request.normalized_options),
        game_state_summary=state,
        metadata={
            "plan": plan.to_dict(),
            "ratio": ratio,
            "max_ratio": max_ratio,
            "pressure_bet": pressure_bet,
            "mechanic_gap": mechanic_gap,
            "mechanic_threshold_push_window": mechanic_threshold_push_window,
            "store_budget": store_budget,
            "pending_marvin_active": pending_marvin_active,
            "pending_marvin_shortfall": pending_marvin_shortfall,
        },
    )
    return bet, trace