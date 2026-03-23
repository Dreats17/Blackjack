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

    # Marvin item leverage: always use Marvin items when available and advantageous
    marvin_items = [
        metadata.get("has_sneaky_peeky_shades", False),
        metadata.get("has_sneaky_peeky_goggles", False),
        metadata.get("has_gamblers_chalice", False),
        metadata.get("has_overflowing_goblet", False),
        metadata.get("has_twins_locket", False),
        metadata.get("has_mirror_of_duality", False),
        metadata.get("has_pocket_watch", False),
        metadata.get("has_grandfather_clock", False),
        metadata.get("has_marvins_eye", False)
    ]
    has_marvin = any(marvin_items)

    action = _recommended_blackjack_action(
        total,
        soft_total,
        dealer_upcard,
        can_double=can_double,
        can_split=can_split,
        can_surrender=can_surrender,
        pair_value=pair_value,
    )

    # If Marvin item is available, always use peek/split/double when possible and advantageous
    run_peak_balance = int(metadata.get("run_peak_balance", balance))
    # Over 15k: play much safer, avoid risky actions unless odds are overwhelming
    if has_marvin:
        if run_peak_balance > 15000:
            # Only use Marvin items if action is not risky or if it prevents a loss
            if can_peek and action != "stand" and total >= 15:
                action = "peek"
            elif can_split and total >= 16:
                action = "split"
            elif can_double and total >= 10 and dealer_upcard <= 6:
                action = "double"
            # Otherwise, play standard safe
        else:
            # Under 15k, be aggressive
            if can_peek and action != "stand":
                action = "peek"
            elif can_split:
                action = "split"
            elif can_double and total >= 9:
                action = "double"

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
    # Dynamically select personality based on current goal
    try:
        from tools.autoplay.personality_manager import personality_manager
        personality = personality_manager.get_personality(plan.goal)
        # Try to use the personality's choose_blackjack_bet if it exists
        if hasattr(personality, "choose_blackjack_bet"):
            # Extract relevant arguments from request and state
            state = dict(request.game_state)
            metadata = dict(request.metadata)
            min_bet = int(metadata.get("min_bet", 1))
            max_bet = int(metadata.get("max_bet", state.get("balance", 0)))
            bet = personality.choose_blackjack_bet(state, min_bet, max_bet)
            trace = DecisionTrace(
                cycle=request.metadata.get("cycle"),
                day=metadata.get("day", state.get("day", 0)),
                context=request.stable_context_id or request.request_type,
                request_type=request.request_type,
                strategic_goal=plan.goal,
                chosen_action=str(bet),
                reason=f"goal={plan.goal} blackjack_bet (personality: {getattr(personality, 'PERSONALITY_NAME', 'unknown')})",
                confidence=0.97,
                options=tuple(option.label for option in request.normalized_options),
                game_state_summary=state,
                metadata={"plan": plan.to_dict()},
            )
            return bet, trace
    except Exception as e:
        # Fallback to default logic if anything fails
        pass

    # Default logic (original implementation)
    metadata = dict(request.metadata)
    state = dict(request.game_state)
    balance = int(_metadata_number(metadata, "balance", state.get("balance", 0)))
    fake_cash = int(_metadata_number(metadata, "fake_cash"))
    total_available = balance + fake_cash
    min_bet = int(_metadata_number(metadata, "min_bet", 1))
    edge_score = int(_metadata_number(metadata, "edge_score"))
    day = int(_metadata_number(metadata, "day", state.get("day", 0)))
    run_peak_balance = int(_metadata_number(metadata, "run_peak_balance", balance))
    starting_balance = int(_metadata_number(metadata, "starting_balance", 50))
    wants_store = _metadata_bool(metadata, "wants_store")
    store_budget = int(_metadata_number(metadata, "store_budget"))

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

    if run_peak_balance > 0 and balance < run_peak_balance * 0.5:
        bet = max(min_bet, int(balance * 0.07))
        reason = "drawdown_protection"
    elif wants_store and store_budget > 0 and balance >= store_budget and edge_score >= 4:
        bet = max(min_bet, int(balance * 0.5))
        reason = "shop_push_high_edge"
    else:
        edge_factor = min(max(edge_score, 0), 7) / 7.0
        base_ratio = 0.12 + (0.23 * edge_factor)
        bet = max(min_bet, int(balance * base_ratio))
        reason = f"smooth_ramp_edge_{edge_score}"

    bet = min(bet, int(balance * 0.5))
    if bet > min_bet:
        bet = max(bet, int(balance * 0.07))
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
        reason=f"goal={plan.goal} blackjack_bet {reason} edge={edge_score}",
        confidence=0.97,
        options=tuple(option.label for option in request.normalized_options),
        game_state_summary=state,
        metadata={
            "plan": plan.to_dict(),
            "edge_score": edge_score,
            "run_peak_balance": run_peak_balance,
            "starting_balance": starting_balance,
            "store_budget": store_budget,
            "wants_store": wants_store,
        },
    )
    return bet, trace