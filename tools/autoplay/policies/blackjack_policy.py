from __future__ import annotations

from ..interfaces import DecisionOption, DecisionRequest
from ..planner import StrategicPlan
from ..tuning import tval
from ..trace import DecisionTrace


def _tfloat(key: str, default: float) -> float:
    return float(tval(key, default))

def _item_bet_multiplier(metadata: dict[str, object], *, in_drawdown: bool) -> tuple[float, list[str]]:
    """Return a per-hand EV multiplier based on active items/flasks and the tags that fired."""
    tags: list[str] = []
    boost = 0.0

    def add(flag_key: str, amount: float, tag: str) -> None:
        nonlocal boost
        if metadata.get(flag_key):
            boost += amount
            tags.append(tag)

    # Flask: high-impact opportunity effects
    add("bet_has_no_bust", 0.42, "no_bust")
    add("bet_has_dealers_whispers", 0.28, "dealers_whispers")
    add("bet_has_second_chance", 0.14, "second_chance")
    add("bet_has_dealers_hesitation", 0.11, "dealers_hesitation")

    # Stochastic luck/protection items
    if metadata.get("bet_has_lucky_medallion"):
        boost += 0.28
        tags.append("lucky_medallion")
    elif metadata.get("bet_has_lucky_coin"):
        boost += 0.14
        tags.append("lucky_coin")

    if metadata.get("bet_has_invisible_cloak"):
        boost += 0.28
        tags.append("invisible_cloak")
    elif metadata.get("bet_has_tattered_cloak"):
        boost += 0.16
        tags.append("tattered_cloak")

    if metadata.get("bet_has_velvet_gloves"):
        boost += 0.16
        tags.append("velvet_gloves")
    elif metadata.get("bet_has_worn_gloves"):
        boost += 0.09
        tags.append("worn_gloves")

    # Action-expanding items
    add("bet_has_chalice", 0.11, "chalice_double")
    add("bet_has_locket", 0.09, "locket_split")
    add("bet_has_phoenix_feather", 0.08, "phoenix_feather")

    if not tags:
        return 1.0, []

    drawdown_multiplier = _tfloat("blackjack.item_boost.drawdown_multiplier", 0.40)
    effective_boost = boost * (drawdown_multiplier if in_drawdown else 1.0)
    return 1.0 + effective_boost, tags



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


def _coerce_action(action: str, request: DecisionRequest, fallback: str = "hit") -> str:
    """Ensure the chosen action exists in current normalized options."""
    allowed = {str(option.value or option.label) for option in request.normalized_options}
    if action in allowed:
        return action
    if fallback in allowed:
        return fallback
    if allowed:
        return next(iter(allowed))
    return fallback


def _blackjack_combo_profile(metadata: dict[str, object], can_peek: bool, next_total: int | None) -> tuple[dict[str, float], list[str]]:
    """Build a capability profile from explicit item/flask signals.

    We separate:
    - information advantage (peek/whispers/imminent)
    - safety net (no-bust/second chance/cloak/luck)
    - leverage (double/split/surrender enabled)
    - latent utility (Marvin items that don't directly alter one hand but improve run quality)
    """
    tags: list[str] = []
    info_advantage = 0.0
    safety_net = 0.0
    leverage = 0.0
    latent_utility = 0.0

    if metadata.get("has_imminent_blackjack"):
        info_advantage += 3.0
        tags.append("imminent_blackjack")
    if can_peek:
        info_advantage += 1.4
        tags.append("peek")
    if metadata.get("has_witch_doctors_amulet") and can_peek:
        info_advantage += 0.8
        tags.append("amulet_plus_peek")
    if metadata.get("has_dealers_whispers"):
        info_advantage += 1.1
        tags.append("dealers_whispers")
    if next_total is not None:
        info_advantage += 0.6
        tags.append("peeked_next_total")

    if metadata.get("has_no_bust"):
        safety_net += 2.4
        tags.append("no_bust")
    if metadata.get("has_second_chance"):
        safety_net += 1.8
        tags.append("second_chance")
    if metadata.get("has_dealers_hesitation"):
        safety_net += 0.9
        tags.append("dealers_hesitation")
    if metadata.get("has_lucky_medallion"):
        safety_net += 1.7
        tags.append("lucky_medallion")
    elif metadata.get("has_lucky_coin"):
        safety_net += 0.9
        tags.append("lucky_coin")
    if metadata.get("has_invisible_cloak"):
        safety_net += 1.9
        tags.append("invisible_cloak")
    elif metadata.get("has_tattered_cloak"):
        safety_net += 1.0
        tags.append("tattered_cloak")
    if metadata.get("has_velvet_gloves"):
        safety_net += 1.2
        tags.append("velvet_gloves")
    elif metadata.get("has_worn_gloves"):
        safety_net += 0.7
        tags.append("worn_gloves")

    if metadata.get("can_double"):
        leverage += 1.2
    if metadata.get("can_split"):
        leverage += 1.0
    if metadata.get("can_surrender"):
        leverage += 0.6
    if metadata.get("has_gamblers_chalice") or metadata.get("has_overflowing_goblet") or metadata.get("has_bonus_fortune"):
        leverage += 0.8
        tags.append("double_suite")
    if metadata.get("has_twins_locket") or metadata.get("has_mirror_of_duality") or metadata.get("has_split_serum"):
        leverage += 0.7
        tags.append("split_suite")
    if metadata.get("has_phoenix_feather") or metadata.get("has_white_feather"):
        leverage += 0.4
        tags.append("surrender_suite")

    # Marvin utility items with indirect but real gambling impact.
    if metadata.get("has_pocket_watch") or metadata.get("has_golden_watch") or metadata.get("has_sapphire_watch") or metadata.get("has_grandfather_clock"):
        latent_utility += 0.6
        tags.append("extra_round_watch")
    if metadata.get("has_quiet_sneakers"):
        latent_utility += 0.2
        tags.append("quiet_sneakers")
    if metadata.get("has_rusty_compass"):
        latent_utility += 0.2
        tags.append("compass")
    if metadata.get("has_faulty_insurance"):
        latent_utility += 0.2
        tags.append("insurance_card")
    if metadata.get("has_grimoire"):
        latent_utility += 0.2
        tags.append("grimoire")
    if metadata.get("has_animal_whistle"):
        latent_utility += 0.15
        tags.append("animal_whistle")
    if metadata.get("has_enchanting_bar"):
        latent_utility += 0.15
        tags.append("enchanting_bar")

    return {
        "info_advantage": info_advantage,
        "safety_net": safety_net,
        "leverage": leverage,
        "latent_utility": latent_utility,
    }, tags


def _apply_item_specific_overrides(
    action: str,
    metadata: dict[str, object],
    *,
    total: int,
    soft_total: int,
    dealer_upcard: int,
    can_double: bool,
    can_split: bool,
    can_surrender: bool,
    pair_value: int | None,
    next_total: int | None,
    info_advantage: float,
    safety_net: float,
) -> str:
    leverage_support = info_advantage + safety_net
    has_double_suite = bool(
        metadata.get("has_gamblers_chalice")
        or metadata.get("has_overflowing_goblet")
        or metadata.get("has_bonus_fortune")
    )
    has_split_suite = bool(
        metadata.get("has_twins_locket")
        or metadata.get("has_mirror_of_duality")
        or metadata.get("has_split_serum")
    )
    has_surrender_suite = bool(
        metadata.get("has_white_feather")
        or metadata.get("has_phoenix_feather")
    )

    if can_surrender and has_surrender_suite and not soft_total:
        if total == 16 and dealer_upcard >= 8:
            return "surrender"
        if total == 15 and dealer_upcard >= 10:
            return "surrender"
        if total == 14 and dealer_upcard == 11 and leverage_support < 2.2:
            return "surrender"

    if can_double and has_double_suite:
        if not soft_total:
            if total == 11:
                return "double"
            if total == 10 and dealer_upcard <= 10:
                return "double"
            if total == 9 and dealer_upcard <= 6 and leverage_support >= 1.4:
                return "double"
            if total == 8 and dealer_upcard <= 6 and next_total is not None and next_total >= 18 and leverage_support >= 2.4:
                return "double"
        else:
            if soft_total == 18 and dealer_upcard in {3, 4, 5, 6}:
                return "double"
            if soft_total == 17 and dealer_upcard in {4, 5, 6} and leverage_support >= 1.8:
                return "double"

    if can_split and has_split_suite and pair_value is not None:
        if pair_value in {8, 11}:
            return "split"
        if pair_value == 9 and dealer_upcard not in {7, 10, 11}:
            return "split"
        if pair_value == 7 and dealer_upcard <= 7 and leverage_support >= 1.0:
            return "split"
        if pair_value in {2, 3} and dealer_upcard <= 7 and leverage_support >= 1.4:
            return "split"
        if pair_value == 6 and dealer_upcard <= 6 and safety_net >= 1.0:
            return "split"
        if pair_value == 4 and dealer_upcard in {5, 6} and info_advantage >= 1.8:
            return "split"

    return action


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

    combo, combo_tags = _blackjack_combo_profile(metadata, can_peek=can_peek, next_total=next_total)
    info_advantage = combo["info_advantage"]
    safety_net = combo["safety_net"]
    leverage = combo["leverage"]
    latent_utility = combo["latent_utility"]

    # Deterministic high-value cases first.
    if has_imminent_blackjack:
        if can_double and total in {9, 10, 11}:
            action = "double"
        else:
            action = "hit"

    # Peek-aware branching: use seen card to alter line, not just confidence.
    if can_peek and next_total is not None and _should_use_peek(action, total, soft_total, bet, balance):
        if next_total > 21:
            if can_surrender and not soft_total and total in {15, 16} and dealer_upcard in {9, 10, 11}:
                action = "surrender"
            elif total >= 12:
                action = "stand"
            else:
                action = "hit"
        else:
            if can_double and total in {9, 10, 11} and (next_total >= 17 or info_advantage >= 2.2):
                action = "double"
            elif can_split and pair_value is not None and pair_value in {2, 3, 6, 7, 8, 9, 11} and next_total >= 16:
                action = "split"
            else:
                action = "hit" if next_total <= 16 else "stand"

    # Safety-net aggressive lines: with No Bust / heavy protection, hit deeper.
    if action == "stand" and has_no_bust and total <= 17:
        action = "hit"
    if action == "hit" and can_double and total in {10, 11} and (safety_net + leverage) >= 3.2:
        action = "double"
    if action == "stand" and can_split and pair_value is not None and pair_value in {8, 11} and (safety_net + leverage) >= 3.0:
        action = "split"

    action = _apply_item_specific_overrides(
        action,
        metadata,
        total=total,
        soft_total=soft_total,
        dealer_upcard=dealer_upcard,
        can_double=can_double,
        can_split=can_split,
        can_surrender=can_surrender,
        pair_value=pair_value,
        next_total=next_total,
        info_advantage=info_advantage,
        safety_net=safety_net,
    )

    # Conservative override when vulnerable and no combo support.
    vulnerability = float(max(0.0, 26.0 - balance / max(1, bet)))
    vulnerability_threshold = _tfloat("blackjack.action.vulnerability_threshold", 14.0)
    vulnerability_support_floor = _tfloat("blackjack.action.vulnerability_support_floor", 1.0)
    if vulnerability >= vulnerability_threshold and (safety_net + info_advantage) < vulnerability_support_floor:
        if action in {"double", "split"}:
            action = "hit" if total <= 11 else "stand"

    # Leverage-intent mode: enough combo support means pushing higher-EV lines.
    combo_intensity = info_advantage + safety_net + leverage + latent_utility
    combo_intensity_threshold = _tfloat("blackjack.action.combo_intensity_threshold", 5.0)
    if combo_intensity >= combo_intensity_threshold:
        leverage_support = info_advantage + safety_net
        if can_double and total in {10, 11} and dealer_upcard <= 9:
            action = "double"
        elif can_double and total == 9 and dealer_upcard <= 6 and leverage_support >= 2.0:
            action = "double"
        elif can_split and pair_value is not None:
            if pair_value in {8, 11}:
                action = "split"
            elif pair_value == 9 and dealer_upcard not in {7, 10, 11} and leverage_support >= 2.2:
                action = "split"
            elif pair_value in {2, 3, 6, 7} and dealer_upcard <= 7 and leverage_support >= 2.6:
                action = "split"

    action = _coerce_action(action, request, fallback="hit")

    selected = None
    score_breakdown: dict[str, float] = {}
    for option in request.normalized_options:
        score = 1.0 if str(option.value or option.label) == action else 0.0
        score_breakdown[option.option_id] = score
        if score > 0.0:
            selected = option

    confidence = _tfloat("blackjack.action.confidence", 0.92) if selected is not None else 0.0
    ranked = sorted(score_breakdown.items(), key=lambda item: item[1], reverse=True)
    trace = DecisionTrace(
        cycle=request.metadata.get("cycle"),
        day=request.metadata.get("day"),
        context=request.stable_context_id or request.request_type,
        request_type=request.request_type,
        strategic_goal=plan.goal,
        chosen_action=str(selected.value if selected and selected.value is not None else action),
        reason=(
            f"goal={plan.goal} blackjack_action={action} total={total} soft={soft_total} dealer={dealer_upcard} "
            f"combo=info:{info_advantage:.1f}/safe:{safety_net:.1f}/lev:{leverage:.1f}/latent:{latent_utility:.1f} "
            f"tags={','.join(combo_tags[:8])}"
        ),
        confidence=confidence,
        options=tuple(option.label for option in request.normalized_options),
        game_state_summary=dict(request.game_state),
        score_breakdown=score_breakdown,
        metadata={
            "plan": plan.to_dict(),
            "reason_code": "blackjack_action:combo_policy",
            "expected_value_estimate": float(info_advantage + safety_net + leverage + latent_utility),
            "candidate_actions": [
                {"option_id": option_id, "score": round(score, 3)}
                for option_id, score in ranked
            ],
        },
    )
    return selected, trace


def choose_insurance_option(request: DecisionRequest, plan: StrategicPlan) -> tuple[DecisionOption | None, DecisionTrace]:
    metadata = dict(request.metadata)
    can_afford = bool(metadata.get("can_afford"))
    has_whispers = bool(metadata.get("has_dealers_whispers"))
    has_mercy = bool(metadata.get("has_dealers_mercy"))
    has_grudge = bool(metadata.get("has_dealers_grudge"))
    dealer_blackjack = bool(metadata.get("dealer_has_blackjack"))
    balance = int(_metadata_number(metadata, "balance"))
    insurance_cost = int(_metadata_number(metadata, "insurance_cost"))

    # If we can observe dealer blackjack exactly (autotest has perfect information here),
    # insurance is always +EV when dealer_blackjack is true.
    insurance_bankroll_multiplier = _tfloat("blackjack.insurance.bankroll_multiplier", 20.0)
    if can_afford and dealer_blackjack and (has_mercy or has_grudge or has_whispers):
        decision = "yes"
    # Otherwise, buy only when richly bankrolled and holding an insurance item.
    elif (
        can_afford
        and (has_mercy or has_grudge)
        and insurance_cost > 0
        and balance >= insurance_cost * insurance_bankroll_multiplier
    ):
        decision = "yes"
    else:
        decision = "no"

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
        reason=(
            f"goal={plan.goal} insurance={decision} whispers={has_whispers} mercy={has_mercy} "
            f"grudge={has_grudge} dealer_blackjack={dealer_blackjack}"
        ),
        confidence=0.95,
        options=tuple(option.label for option in request.normalized_options),
        game_state_summary=dict(request.game_state),
        score_breakdown=score_breakdown,
        metadata={
            "plan": plan.to_dict(),
            "reason_code": "insurance:item_context",
            "expected_value_estimate": 1.0 if decision == "yes" else 0.0,
            "candidate_actions": [
                {"option": "yes", "selected": decision == "yes"},
                {"option": "no", "selected": decision == "no"},
            ],
        },
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
    has_no_bust = bool(metadata.get("has_no_bust"))
    has_hesitation = bool(metadata.get("has_dealers_hesitation"))
    has_whispers = bool(metadata.get("has_dealers_whispers"))
    has_lucky_medallion = bool(metadata.get("has_lucky_medallion"))
    has_lucky_coin = bool(metadata.get("has_lucky_coin"))
    has_invisible_cloak = bool(metadata.get("has_invisible_cloak"))
    has_tattered_cloak = bool(metadata.get("has_tattered_cloak"))

    protection = 0.0
    no_bust_weight = _tfloat("blackjack.second_chance.protection.no_bust", 1.2)
    hesitation_weight = _tfloat("blackjack.second_chance.protection.hesitation", 0.7)
    whispers_weight = _tfloat("blackjack.second_chance.protection.whispers", 0.6)
    lucky_medallion_weight = _tfloat("blackjack.second_chance.protection.lucky_medallion", 1.0)
    lucky_coin_weight = _tfloat("blackjack.second_chance.protection.lucky_coin", 0.5)
    invisible_cloak_weight = _tfloat("blackjack.second_chance.protection.invisible_cloak", 1.0)
    tattered_cloak_weight = _tfloat("blackjack.second_chance.protection.tattered_cloak", 0.6)
    if has_no_bust:
        protection += no_bust_weight
    if has_hesitation:
        protection += hesitation_weight
    if has_whispers:
        protection += whispers_weight
    if has_lucky_medallion:
        protection += lucky_medallion_weight
    elif has_lucky_coin:
        protection += lucky_coin_weight
    if has_invisible_cloak:
        protection += invisible_cloak_weight
    elif has_tattered_cloak:
        protection += tattered_cloak_weight

    replay = False
    if not free_hand and bet > 0:
        if not (status == "Dealer Blackjack" and insurance_bet > 0):
            post_loss_balance = balance - bet
            loss_ratio = bet / max(balance, 1)
            bust_loss_ratio_floor = _tfloat("blackjack.second_chance.player_bust.loss_ratio_floor", 0.16)
            bust_loss_ratio_base = _tfloat("blackjack.second_chance.player_bust.loss_ratio_base", 0.24)
            bust_protection_weight = _tfloat("blackjack.second_chance.player_bust.protection_weight", 0.03)
            bust_edge_base = _tfloat("blackjack.second_chance.player_bust.edge_base", 5.0)
            bust_bet_floor = _tfloat("blackjack.second_chance.player_bust.bet_floor", 80.0)
            bust_balance_divisor = _tfloat("blackjack.second_chance.player_bust.balance_divisor", 10.0)

            dealer_loss_ratio_floor = _tfloat("blackjack.second_chance.dealer_blackjack.loss_ratio_floor", 0.12)
            dealer_loss_ratio_base = _tfloat("blackjack.second_chance.dealer_blackjack.loss_ratio_base", 0.19)
            dealer_protection_weight = _tfloat("blackjack.second_chance.dealer_blackjack.protection_weight", 0.02)
            dealer_edge_base = _tfloat("blackjack.second_chance.dealer_blackjack.edge_base", 4.0)

            default_loss_ratio_floor = _tfloat("blackjack.second_chance.default.loss_ratio_floor", 0.14)
            default_loss_ratio_base = _tfloat("blackjack.second_chance.default.loss_ratio_base", 0.21)
            default_protection_weight = _tfloat("blackjack.second_chance.default.protection_weight", 0.025)
            default_edge_base = _tfloat("blackjack.second_chance.default.edge_base", 6.0)
            default_bet_floor = _tfloat("blackjack.second_chance.default.bet_floor", 110.0)
            default_balance_divisor = _tfloat("blackjack.second_chance.default.balance_divisor", 8.0)

            if post_loss_balance < reserve:
                replay = True
            elif status == "Player Bust":
                replay = (
                    loss_ratio >= max(bust_loss_ratio_floor, bust_loss_ratio_base - protection * bust_protection_weight)
                    or (
                        edge_score >= max(3, int(bust_edge_base - protection))
                        and bet >= max(bust_bet_floor, balance // max(1, int(bust_balance_divisor)))
                    )
                )
            elif status == "Dealer Blackjack":
                replay = (
                    loss_ratio >= max(dealer_loss_ratio_floor, dealer_loss_ratio_base - protection * dealer_protection_weight)
                    and edge_score >= max(2, int(dealer_edge_base - protection))
                )
            else:
                replay = (
                    loss_ratio >= max(default_loss_ratio_floor, default_loss_ratio_base - protection * default_protection_weight)
                    or (
                        edge_score >= max(4, int(default_edge_base - protection))
                        and bet >= max(default_bet_floor, balance // max(1, int(default_balance_divisor)))
                    )
                )

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
        reason=(
            f"goal={plan.goal} second_chance={decision} status={status} edge={edge_score} protection={protection:.1f}"
        ),
        confidence=0.9,
        options=tuple(option.label for option in request.normalized_options),
        game_state_summary=dict(request.game_state),
        score_breakdown=score_breakdown,
        metadata={
            "plan": plan.to_dict(),
            "reason_code": "second_chance:protection_stack",
            "expected_value_estimate": float(protection),
            "candidate_actions": [
                {"option": "yes", "selected": decision == "yes"},
                {"option": "no", "selected": decision == "no"},
            ],
        },
    )
    return selected, trace


def choose_blackjack_bet(request: DecisionRequest, plan: StrategicPlan) -> tuple[int | None, DecisionTrace]:
    p = plan.personality  # set by PersonalityManager at goal selection time

    # Default logic
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
    dealer_happiness = int(_metadata_number(metadata, "dealer_happiness", 45))
    wants_store = _metadata_bool(metadata, "wants_store")
    store_budget = int(_metadata_number(metadata, "store_budget"))
    needs_car = _metadata_bool(metadata, "needs_car")
    ever_had_car = _metadata_bool(metadata, "ever_had_car")
    early_caution = _metadata_bool(metadata, "early_caution")
    stranded_no_car = _metadata_bool(metadata, "stranded_no_car")
    survival_mode = _metadata_bool(metadata, "survival_mode")
    health = int(_metadata_number(metadata, "health", state.get("health", 100)))
    sanity = int(_metadata_number(metadata, "sanity", state.get("sanity", 100)))
    rank = int(_metadata_number(metadata, "rank", state.get("rank", 0)))
    loan_warning_level = int(_metadata_number(metadata, "loan_warning_level"))
    loan_debt = int(_metadata_number(metadata, "loan_debt"))
    wants_millionaire_push = _metadata_bool(metadata, "wants_millionaire_push")
    has_extra_round_item = _metadata_bool(metadata, "has_extra_round_item")
    car_progress_reserve = int(_metadata_number(metadata, "car_progress_reserve"))
    mechanic_purchase_reserve = int(_metadata_number(metadata, "mechanic_purchase_reserve"))
    known_car_repair_reserve = int(_metadata_number(metadata, "known_car_repair_reserve"))
    has_unbought_marvin_items = _metadata_bool(metadata, "has_unbought_marvin_items")
    is_millionaire = _metadata_bool(metadata, "is_millionaire")
    marvin_remaining_spend = int(_metadata_number(metadata, "marvin_remaining_spend"))

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
            metadata={
                "plan": plan.to_dict(),
                "reason_code": "bet:empty_bankroll",
                "expected_value_estimate": 0.0,
                "candidate_actions": [],
            },
        )
        return 0, trace

    # ── Imminent Blackjack: guaranteed 3:2 payout — bet as much as allowed ──
    if _metadata_bool(metadata, "bet_has_imminent_blackjack"):
        bet = max(min_bet, min(int(balance * 0.50), total_available))
        reason = f"imminent_blackjack_max_bet({p.name})"
        trace = DecisionTrace(
            cycle=request.metadata.get("cycle"),
            day=day,
            context=request.stable_context_id or request.request_type,
            request_type=request.request_type,
            strategic_goal=plan.goal,
            chosen_action=str(bet),
            reason=f"goal={plan.goal} blackjack_bet {reason}",
            confidence=1.0,
            options=tuple(option.label for option in request.normalized_options),
            game_state_summary=state,
            metadata={
                "plan": plan.to_dict(),
                "edge_score": edge_score,
                "reason_code": "bet:imminent_blackjack",
                "expected_value_estimate": 1.5,
                "candidate_actions": [{"bet": bet, "rule": "imminent_blackjack_max"}],
            },
        )
        return bet, trace

    in_drawdown = (
        p.drawdown_protection
        and run_peak_balance > 0
        and balance < run_peak_balance * p.drawdown_threshold
        and not needs_car
        and balance >= 350
    )
    drawdown_min_peak = int(_tfloat("blackjack.drawdown.min_peak", 8000.0))

    reason_code = "bet:score_ramp_with_constraints"

    bootstrap_reserve_target = max(
        int(_tfloat("blackjack.bootstrap.reserve_floor", 200.0)),
        car_progress_reserve,
        mechanic_purchase_reserve,
        known_car_repair_reserve,
    )
    critical_balance_cap = int(_tfloat("blackjack.bootstrap.critical_balance_cap", 55.0))
    critical_cash_buffer = int(_tfloat("blackjack.bootstrap.critical_cash_buffer", 12.0))
    critical_bet_ratio = _tfloat("blackjack.bootstrap.critical_bet_ratio", 0.24)
    stability_health_floor = int(_tfloat("blackjack.bootstrap.stability_health_floor", 72.0))
    stability_sanity_floor = int(_tfloat("blackjack.bootstrap.stability_sanity_floor", 40.0))
    cautious_push_ratio = _tfloat("blackjack.bootstrap.cautious_push_ratio", 0.24)
    steady_push_ratio_base = _tfloat("blackjack.bootstrap.push_ratio_base", 0.26)
    steady_push_ratio_edge_weight = _tfloat("blackjack.bootstrap.push_ratio_edge_weight", 0.028)
    steady_push_ratio_cap = _tfloat("blackjack.bootstrap.push_ratio_cap", 0.42)

    post_car_growth_floor = int(_tfloat("blackjack.post_car.growth_floor", 350.0))
    post_car_growth_ceiling = int(_tfloat("blackjack.post_car.growth_ceiling", 25000.0))
    post_car_health_floor = int(_tfloat("blackjack.post_car.health_floor", 70.0))
    post_car_sanity_floor = int(_tfloat("blackjack.post_car.sanity_floor", 36.0))
    post_car_warning_cap = int(_tfloat("blackjack.post_car.warning_cap", 2.0))
    post_car_debt_cap = int(_tfloat("blackjack.post_car.debt_cap", 1200.0))
    post_car_base_ratio = _tfloat("blackjack.post_car.base_ratio", 0.27)
    post_car_edge_weight = _tfloat("blackjack.post_car.edge_weight", 0.03)
    post_car_rank_bonus = _tfloat("blackjack.post_car.rank_bonus", 0.02)
    post_car_extra_round_bonus = _tfloat("blackjack.post_car.extra_round_bonus", 0.04)
    post_car_millionaire_bonus = _tfloat("blackjack.post_car.millionaire_bonus", 0.03)
    post_car_ratio_cap = _tfloat("blackjack.post_car.ratio_cap", 0.50)
    post_car_ratio_floor = _tfloat("blackjack.post_car.ratio_floor", 0.20)

    wealth_lock_balance_floor = int(_tfloat("blackjack.wealth_lock.balance_floor", 20000.0))
    wealth_lock_health_floor = int(_tfloat("blackjack.wealth_lock.health_floor", 64.0))
    wealth_lock_sanity_floor = int(_tfloat("blackjack.wealth_lock.sanity_floor", 34.0))
    wealth_lock_warning_cap = int(_tfloat("blackjack.wealth_lock.warning_cap", 1.0))
    wealth_lock_debt_cap = int(_tfloat("blackjack.wealth_lock.debt_cap", 0.0))
    wealth_lock_base_ratio = _tfloat("blackjack.wealth_lock.base_ratio", 0.09)
    wealth_lock_edge_weight = _tfloat("blackjack.wealth_lock.edge_weight", 0.01)
    wealth_lock_ratio_cap = _tfloat("blackjack.wealth_lock.ratio_cap", 0.16)
    wealth_lock_ratio_floor = _tfloat("blackjack.wealth_lock.ratio_floor", 0.06)

    millionaire_push_balance_floor = int(_tfloat("blackjack.millionaire_push.balance_floor", 100000.0))
    millionaire_push_health_floor = int(_tfloat("blackjack.millionaire_push.health_floor", 74.0))
    millionaire_push_sanity_floor = int(_tfloat("blackjack.millionaire_push.sanity_floor", 42.0))
    millionaire_push_warning_cap = int(_tfloat("blackjack.millionaire_push.warning_cap", 0.0))
    millionaire_push_debt_cap = int(_tfloat("blackjack.millionaire_push.debt_cap", 0.0))
    millionaire_push_base_ratio = _tfloat("blackjack.millionaire_push.base_ratio", 0.18)
    millionaire_push_edge_weight = _tfloat("blackjack.millionaire_push.edge_weight", 0.022)
    millionaire_push_rank_bonus = _tfloat("blackjack.millionaire_push.rank_bonus", 0.02)
    millionaire_push_extra_round_bonus = _tfloat("blackjack.millionaire_push.extra_round_bonus", 0.05)
    millionaire_push_surge_balance_floor = int(_tfloat("blackjack.millionaire_push.surge_balance_floor", 400000.0))
    millionaire_push_surge_bonus = _tfloat("blackjack.millionaire_push.surge_bonus", 0.05)
    millionaire_push_ratio_cap = _tfloat("blackjack.millionaire_push.ratio_cap", 0.40)
    millionaire_push_ratio_floor = _tfloat("blackjack.millionaire_push.ratio_floor", 0.16)

    in_no_car_bootstrap = needs_car and (run_peak_balance < bootstrap_reserve_target or balance < bootstrap_reserve_target)
    in_millionaire_push = (
        ever_had_car
        and (not needs_car)
        and wants_millionaire_push
        and balance >= millionaire_push_balance_floor
        and health >= millionaire_push_health_floor
        and sanity >= millionaire_push_sanity_floor
        and loan_warning_level <= millionaire_push_warning_cap
        and loan_debt <= millionaire_push_debt_cap
        and not survival_mode
        and not (in_drawdown and balance < millionaire_push_balance_floor)
    )
    in_wealth_lock = (
        ever_had_car
        and (not needs_car)
        and not in_millionaire_push
        and balance >= wealth_lock_balance_floor
        and health >= wealth_lock_health_floor
        and sanity >= wealth_lock_sanity_floor
        and loan_warning_level <= wealth_lock_warning_cap
        and loan_debt <= wealth_lock_debt_cap
        and not survival_mode
    )
    # ── Marvin-first mode: at $40k+ with unbought Marvin items, bet minimum ──
    # Bot preserves capital for Marvin purchases rather than risking it gambling.
    marvin_first_balance_floor = int(_tfloat("blackjack.marvin_first.balance_floor", 40000.0))
    in_marvin_first = (
        ever_had_car
        and (not needs_car)
        and not in_millionaire_push
        and balance >= marvin_first_balance_floor
        and has_unbought_marvin_items
        and not survival_mode
    )
    if in_millionaire_push:
        push_ratio = (
            millionaire_push_base_ratio
            + edge_score * millionaire_push_edge_weight
            + max(0, rank - 3) * millionaire_push_rank_bonus
            + (millionaire_push_extra_round_bonus if has_extra_round_item else 0.0)
        )
        if balance >= millionaire_push_surge_balance_floor:
            push_ratio += millionaire_push_surge_bonus
        if run_peak_balance > 0 and balance >= int(run_peak_balance * 0.75):
            push_ratio += 0.03
        push_ratio = max(millionaire_push_ratio_floor, min(millionaire_push_ratio_cap, push_ratio))
        bet = max(min_bet, int(balance * push_ratio))
        reason = f"millionaire_push({p.name})"
        reason_code = "bet:millionaire_push"
    elif in_marvin_first:
        bet = min_bet
        reason = f"marvin_first_min_bet({p.name},remaining={marvin_remaining_spend})"
        reason_code = "bet:marvin_first_min_bet"
    elif in_wealth_lock:
        lock_ratio = wealth_lock_base_ratio + edge_score * wealth_lock_edge_weight
        lock_ratio = max(wealth_lock_ratio_floor, min(wealth_lock_ratio_cap, lock_ratio))
        bet = max(min_bet, int(balance * lock_ratio))
        reason = f"wealth_lock_preserve({p.name})"
        reason_code = "bet:wealth_lock_preserve"
    elif in_no_car_bootstrap:
        if balance <= critical_balance_cap or survival_mode:
            spendable = max(0, balance - critical_cash_buffer)
            if spendable <= 0:
                bet = min_bet
            else:
                bet = max(min_bet, int(spendable * critical_bet_ratio))
            reason = f"no_car_bootstrap_survival({p.name})"
            reason_code = "bet:no_car_bootstrap_survival"
        else:
            stable = health >= stability_health_floor and sanity >= stability_sanity_floor
            if stable and not early_caution and not stranded_no_car:
                push_ratio = min(steady_push_ratio_cap, steady_push_ratio_base + edge_score * steady_push_ratio_edge_weight)
            else:
                push_ratio = cautious_push_ratio
            bet = max(min_bet, int(balance * push_ratio))
            reason = f"no_car_bootstrap_push({p.name})"
            reason_code = "bet:no_car_bootstrap_push"
    elif (
        ever_had_car
        and (not needs_car)
        and balance >= post_car_growth_floor
        and balance < post_car_growth_ceiling
        and health >= post_car_health_floor
        and sanity >= post_car_sanity_floor
        and loan_warning_level <= post_car_warning_cap
        and loan_debt <= post_car_debt_cap
        and not survival_mode
    ):
        # Drawdown override: when the run has had a significant peak and
        # balance has crashed below the drawdown threshold, switch to the
        # wealth-lock bet sizing even though balance is below
        # wealth_lock_balance_floor.  This prevents the 27-50% growth-push
        # bets from bleeding a run from $33k to $0 over 80 days.
        if in_drawdown and run_peak_balance >= drawdown_min_peak:
            lock_ratio = wealth_lock_base_ratio + edge_score * wealth_lock_edge_weight
            lock_ratio = max(wealth_lock_ratio_floor, min(wealth_lock_ratio_cap, lock_ratio))
            bet = max(min_bet, int(balance * lock_ratio))
            reason = f"drawdown_protection({p.name})"
            reason_code = "bet:drawdown_protection"
        else:
            growth_ratio = (
                post_car_base_ratio
                + edge_score * post_car_edge_weight
                + max(0, rank - 1) * post_car_rank_bonus
                + (post_car_extra_round_bonus if has_extra_round_item else 0.0)
                + (post_car_millionaire_bonus if wants_millionaire_push else 0.0)
            )
            # Taper the ratio cap as balance climbs: full cap at floor, 20% at ceiling.
            # Prevents catastrophic 50% bets at $10k+ that can wipe a run in 3 hands.
            growth_range = max(1, post_car_growth_ceiling - post_car_growth_floor)
            balance_fraction = max(0.0, min(1.0, (balance - post_car_growth_floor) / growth_range))
            scaled_cap = post_car_ratio_cap - balance_fraction * (post_car_ratio_cap - post_car_ratio_floor)
            growth_ratio = max(post_car_ratio_floor, min(scaled_cap, growth_ratio))
            bet = max(min_bet, int(balance * growth_ratio))
            reason = f"post_car_growth_push({p.name})"
            reason_code = "bet:post_car_growth_push"
    elif in_drawdown:
        bet = max(min_bet, int(balance * p.drawdown_bet_fraction))
        reason = f"drawdown_protection({p.name})"
        reason_code = "bet:drawdown_protection"
    elif wants_store and store_budget > 0 and balance >= store_budget and edge_score >= 4:
        bet = max(min_bet, int(balance * 0.5))
        reason = "shop_push_high_edge"
        reason_code = "bet:shop_push_high_edge"
    else:
        edge_factor = min(max(edge_score, 0), 7) / 7.0
        base_ratio = 0.12 + (0.23 * edge_factor)
        # Personality scales bet size around the baseline formula.
        # At bet_aggression=0.50 the multiplier is exactly 1.0 (no change).
        aggression_scale = 0.60 + 0.80 * p.bet_aggression
        bet = max(min_bet, int(balance * base_ratio * aggression_scale))
        reason = f"smooth_ramp_edge_{edge_score}({p.name})"

    # ── Per-item EV multiplier ────────────────────────────────────────────
    item_multiplier, item_tags = _item_bet_multiplier(metadata, in_drawdown=in_drawdown)
    if item_multiplier > 1.0:
        bet = max(min_bet, int(bet * item_multiplier))
        reason = f"{reason}+items[{','.join(item_tags)}]x{item_multiplier:.2f}"

    # ── Dealer happiness floor: bet ≥30% of balance when dealer is angry ──
    # At bet_ratio < 0.3, wins give minimal calm (+2) while losses can
    # outpace gains. At ≥0.3, calm values double/triple, preventing death.
    if dealer_happiness < 25 and balance > 0:
        angry_floor = max(min_bet, int(balance * 0.30))
        if bet < angry_floor:
            bet = angry_floor
            reason = f"{reason}+dealer_anger_floor(dh={dealer_happiness})"
            reason_code = "bet:dealer_anger_floor"

    bet = min(bet, int(balance * 0.50))
    # ── Millionaire protection: preserve $1.05M floor once flagged ──────
    # Prevents gambling back below $1M before the morning ending triggers.
    if is_millionaire and balance >= 1050000:
        max_millionaire_bet = max(min_bet, balance - 1050000)
        if bet > max_millionaire_bet:
            bet = max_millionaire_bet
            reason = f"{reason}+millionaire_floor_cap"
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
            "reason_code": reason_code,
            "expected_value_estimate": float(edge_score),
            "candidate_actions": [{"bet": bet, "reason": reason}],
        },
    )
    return bet, trace