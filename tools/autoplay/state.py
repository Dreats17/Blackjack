from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


def _sorted_strings(values: Any) -> tuple[str, ...]:
    if not values:
        return ()
    return tuple(sorted(str(value) for value in values))


def _safe_call(obj: Any, method_name: str, default: Any = None) -> Any:
    if obj is None or not hasattr(obj, method_name):
        return default
    method = getattr(obj, method_name)
    if not callable(method):
        return default
    try:
        return method()
    except Exception:
        return default


def _available_routes(player: Any) -> tuple[str, ...]:
    route_labels: list[str] = []
    lists_obj = getattr(player, "_lists", None)
    if lists_obj is not None and hasattr(lists_obj, "make_shop_list"):
        try:
            on_foot = not bool(player and player.has_item("Car"))
            route_labels.extend(str(label) for label in lists_obj.make_shop_list(on_foot=on_foot))
        except Exception:
            pass
    return tuple(dict.fromkeys(route_labels))


def _companion_metrics(player: Any) -> dict[str, int]:
    companions = _safe_call(player, "get_all_companions", {}) or {}
    if not isinstance(companions, dict):
        return {
            "count": 0,
            "bonded": 0,
            "low_happiness": 0,
            "runaway_risk": 0,
            "unfed": 0,
        }

    count = len(companions)
    bonded = 0
    low_happiness = 0
    runaway_risk = 0
    unfed = 0
    for data in companions.values():
        happiness = int(data.get("happiness", 50) or 0)
        if data.get("bonded"):
            bonded += 1
        if happiness < 35:
            low_happiness += 1
        if happiness <= 15:
            runaway_risk += 1
        if not data.get("fed_today", False):
            unfed += 1

    return {
        "count": count,
        "bonded": bonded,
        "low_happiness": low_happiness,
        "runaway_risk": runaway_risk,
        "unfed": unfed,
    }


def _inventory_food_count(player: Any) -> int:
    foods = _safe_call(player, "get_inventory_food", ()) or ()
    try:
        return len(foods)
    except Exception:
        return 0


def _economy_hint_value(economy_hints: dict[str, Any], key: str) -> int:
    return int(economy_hints.get(key, 0) or 0)


def _route_tokens(available_routes: tuple[str, ...]) -> set[str]:
    tokens: set[str] = set()
    for route in available_routes:
        lowered = route.lower()
        if "convenience store" in lowered:
            tokens.add("store")
        if "pawn" in lowered:
            tokens.add("pawn")
        if "loan shark" in lowered:
            tokens.add("loan")
        if "marvin" in lowered:
            tokens.add("marvin")
        if "witch" in lowered:
            tokens.add("witch")
        if any(name in lowered for name in ("tom", "frank", "oswald")):
            tokens.add("mechanic")
        if lowered.startswith("drive to "):
            tokens.add("adventure")
        if "car workbench" in lowered:
            tokens.add("workbench")
    return tokens


def _opportunity_flags(
    player: Any,
    available_routes: tuple[str, ...],
    balance: int,
    health: int,
    sanity: int,
    fatigue: int,
    travel_restrictions: tuple[str, ...],
    broken_items: tuple[str, ...],
    repairing_items: tuple[str, ...],
    companion_metrics: dict[str, int],
    inventory_food_count: int,
    economy_hints: dict[str, Any],
) -> dict[str, bool]:
    has_car = bool(player and player.has_item("Car"))
    has_map = bool(player and player.has_item("Map"))
    has_worn_map = bool(player and player.has_item("Worn Map"))
    route_tokens = _route_tokens(available_routes)
    mechanic_visits = int(_safe_call(player, "get_mechanic_visits", 0) or 0)
    debt = int(_safe_call(player, "get_loan_shark_debt", 0) or 0)
    warning_level = int(_safe_call(player, "get_loan_shark_warning_level", 0) or 0)
    can_access_upgrades = bool(_safe_call(player, "can_access_upgrades", False))
    has_met_witch = bool(player and player.has_met("Witch"))
    marvin_affordable_priority = _economy_hint_value(economy_hints, "marvin_affordable_priority")
    marvin_strong_window = bool(_economy_hint_value(economy_hints, "marvin_strong_window"))
    marvin_ready_window = bool(
        has_car
        and (has_map or has_worn_map)
        and health >= 54
        and sanity >= 28
        and marvin_affordable_priority > 0
        and (
            marvin_strong_window
            or (
                int(_safe_call(player, "get_rank", 0) or 0) <= 1
                and marvin_affordable_priority >= 44
                and balance >= 1400
            )
        )
    )

    return {
        "can_unlock_car": not has_car and balance >= 120,
        "can_advance_mechanic_arc": has_car and mechanic_visits < 3 and "mechanic" in route_tokens,
        "can_visit_marvin": "marvin" in route_tokens and marvin_ready_window,
        "can_visit_witch": "witch" in route_tokens and has_met_witch and health >= 45 and sanity >= 20,
        "can_adventure_safely": has_car and "adventure" in route_tokens and balance >= 40 and health >= 65 and sanity >= 35,
        "can_convert_millionaire_to_ending": balance >= 1_000_000,
        "can_reduce_debt_risk": "loan" in route_tokens and (debt > 0 or warning_level > 0),
        "can_repair_or_upgrade": has_car and can_access_upgrades and "workbench" in route_tokens,
        "can_reduce_fatigue_pressure": fatigue >= 68,
        "can_preserve_companions": companion_metrics.get("count", 0) > 0 and (
            companion_metrics.get("runaway_risk", 0) > 0
            or companion_metrics.get("low_happiness", 0) > 0
            or inventory_food_count < companion_metrics.get("count", 0)
        ),
        "can_contain_debt_escalation": "loan" in route_tokens and debt > 0 and warning_level >= 2,
        "can_recover_from_car_trouble": has_car and "mechanic" in route_tokens and bool(travel_restrictions),
        "can_restore_blackjack_edge": bool(broken_items or repairing_items),
        "can_restock_supplies": has_car
        and "store" in route_tokens
        and _economy_hint_value(economy_hints, "store_candidate_count") > 0
        and _economy_hint_value(economy_hints, "store_best_priority") >= 56,
        "can_cashout_pawn_inventory": has_car
        and "pawn" in route_tokens
        and _economy_hint_value(economy_hints, "pawn_planned_sale_value") > 0
        and not marvin_ready_window,
        # Proactive borrowing: Vinnie met, no current debt, balance low enough that a loan is
        # worth the 20%/week interest cost (rank-based thresholds verified from systems.py).
        "can_borrow_to_bootstrap": (
            has_car
            and "loan" in route_tokens
            and debt == 0
            and _economy_hint_value(economy_hints, "fake_cash") == 0
            and bool(player and player.has_met("Vinnie"))
            and health >= 48
            and sanity >= 26
            and (
                (int(_safe_call(player, "get_rank", 0) or 0) == 0 and balance < 900)
                or (int(_safe_call(player, "get_rank", 0) or 0) == 1 and not has_map and balance < 3000)
            )
        ),
    }


def _goal_candidates(
    player: Any,
    flags: dict[str, bool],
    health: int,
    sanity: int,
    statuses: tuple[str, ...],
    injuries: tuple[str, ...],
    balance: int,
    fatigue: int,
    companion_metrics: dict[str, int],
) -> tuple[str, ...]:
    candidates: list[str] = []
    debt = int(_safe_call(player, "get_loan_shark_debt", 0) or 0)
    fake_cash = int(_safe_call(player, "get_fraudulent_cash", 0) or 0)

    if health < 45 or sanity < 20:
        candidates.append("survive_emergency")
    if health < 68 or len(statuses) >= 2 or len(injuries) >= 2:
        candidates.append("stabilize_health")
    if sanity < 34:
        candidates.append("stabilize_sanity")
    if flags["can_reduce_fatigue_pressure"]:
        candidates.append("reduce_fatigue_pressure")
    if flags["can_preserve_companions"]:
        candidates.append("preserve_companion_roster")
    if flags["can_restock_supplies"]:
        candidates.append("restock_supplies")
    if not flags["can_unlock_car"] and not bool(player and player.has_item("Car")):
        candidates.append("bootstrap_blackjack_edge")
    if not bool(player and player.has_item("Car")):
        candidates.append("acquire_car")
    if flags["can_reduce_debt_risk"]:
        candidates.append("reduce_debt_risk")
    if flags["can_contain_debt_escalation"]:
        candidates.append("contain_debt_escalation")
    if flags["can_cashout_pawn_inventory"]:
        candidates.append("cashout_pawn_inventory")
    if fake_cash > 0:
        candidates.append("blend_fraudulent_cash_safely")
    # Proactive borrowing: when Vinnie is accessible and balance is low, borrowing is one
    # of the best moves in the game.  Include push_next_rank/bootstrap as goals so the
    # route policy's loan alignment (+30 / +22) can beat the convenience store score.
    if flags.get("can_borrow_to_bootstrap"):
        if not any(g in candidates for g in ("bootstrap_blackjack_edge", "push_next_rank")):
            candidates.append("push_next_rank")
    if flags["can_visit_marvin"]:
        candidates.append("exploit_marvin")
    elif bool(player and player.has_item("Car")) and not (bool(player and player.has_item("Map")) or bool(player and player.has_item("Worn Map"))):
        candidates.append("unlock_marvin")
    if flags["can_recover_from_car_trouble"]:
        candidates.append("recover_from_car_trouble")
    if flags["can_advance_mechanic_arc"]:
        candidates.append("advance_mechanic_arc")
    if flags["can_repair_or_upgrade"]:
        candidates.append("repair_or_upgrade_gear")
    if flags["can_restore_blackjack_edge"]:
        candidates.append("restore_blackjack_edge_after_breakage")
    if flags["can_adventure_safely"] and int(_safe_call(player, "get_rank", 0) or 0) >= 2:
        candidates.append("exploit_adventure")
    elif bool(player and player.has_item("Car")):
        candidates.append("reach_adventure_threshold")
    if flags["can_convert_millionaire_to_ending"]:
        candidates.append("convert_millionaire_to_ending")
    if debt == 0 and balance < 1_000_000:
        candidates.append("push_next_rank")

    if not candidates:
        candidates.append("bootstrap_blackjack_edge")
    return tuple(dict.fromkeys(candidates))


@dataclass(frozen=True)
class GameState:
    day: int
    balance: int
    rank: int
    health: int
    sanity: int
    fatigue: int
    alive: bool
    current_context_tag: str
    available_routes: tuple[str, ...] = ()
    available_menu_options: tuple[str, ...] = ()
    statuses: tuple[str, ...] = ()
    injuries: tuple[str, ...] = ()
    travel_restrictions: tuple[str, ...] = ()
    inventory: tuple[str, ...] = ()
    broken_items: tuple[str, ...] = ()
    repairing_items: tuple[str, ...] = ()
    flask_effects: tuple[str, ...] = ()
    companions: tuple[str, ...] = ()
    companion_count: int = 0
    companion_low_happiness_count: int = 0
    companion_runaway_risk_count: int = 0
    companion_bonded_count: int = 0
    companion_unfed_count: int = 0
    inventory_food_count: int = 0
    has_car: bool = False
    has_map: bool = False
    has_worn_map: bool = False
    has_marvin_access: bool = False
    has_met_witch: bool = False
    has_met_vinnie: bool = False
    has_met_gus: bool = False
    chosen_mechanic: str | None = None
    mechanic_visits: int = 0
    loan_debt: int = 0
    loan_warning_level: int = 0
    fraudulent_cash: int = 0
    dealer_happiness: int = 50
    store_candidate_count: int = 0
    store_best_purchase_priority: int = 0
    store_target_spend: int = 0
    pawn_sellable_value: int = 0
    pawn_planned_sale_count: int = 0
    pawn_planned_sale_value: int = 0
    marvin_affordable_priority: int = 0
    marvin_candidate_price: int = 0
    marvin_strong_window: bool = False
    opportunity_flags: dict[str, bool] = field(default_factory=dict)
    current_progress_goal_candidates: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def build_game_state_snapshot(
    player: Any,
    *,
    current_context_tag: str = "unknown",
    available_menu_options: list[str] | tuple[str, ...] | None = None,
    available_routes: list[str] | tuple[str, ...] | None = None,
    economy_hints: dict[str, Any] | None = None,
) -> GameState:
    if player is None:
        return GameState(
            day=0,
            balance=0,
            rank=0,
            health=0,
            sanity=0,
            fatigue=0,
            alive=False,
            current_context_tag=current_context_tag,
        )

    balance = int(_safe_call(player, "get_balance", getattr(player, "_balance", 0)) or 0)
    health = int(_safe_call(player, "get_health", getattr(player, "_health", 0)) or 0)
    sanity = int(_safe_call(player, "get_sanity", getattr(player, "_sanity", 0)) or 0)
    fatigue = int(_safe_call(player, "get_fatigue", getattr(player, "_fatigue", 0)) or 0)
    resolved_available_routes = tuple(available_routes) if available_routes is not None else _available_routes(player)
    statuses = _sorted_strings(getattr(player, "_status_effects", ()))
    injuries = _sorted_strings(getattr(player, "_injuries", ()))
    travel_restrictions = _sorted_strings(getattr(player, "_travel_restrictions", ()))
    broken_items = _sorted_strings(getattr(player, "_broken_inventory", ()))
    repairing_items = _sorted_strings(getattr(player, "_repairing_inventory", ()))
    companion_metrics = _companion_metrics(player)
    inventory_food_count = _inventory_food_count(player)
    normalized_economy_hints = dict(economy_hints or {})
    flags = _opportunity_flags(
        player,
        resolved_available_routes,
        balance,
        health,
        sanity,
        fatigue,
        travel_restrictions,
        broken_items,
        repairing_items,
        companion_metrics,
        inventory_food_count,
        normalized_economy_hints,
    )

    return GameState(
        day=int(getattr(player, "_day", 0) or 0),
        balance=balance,
        rank=int(_safe_call(player, "get_rank", getattr(player, "_rank", 0)) or 0),
        health=health,
        sanity=sanity,
        fatigue=fatigue,
        alive=bool(_safe_call(player, "is_alive", getattr(player, "_alive", True)) if hasattr(player, "is_alive") else getattr(player, "_alive", True)),
        current_context_tag=current_context_tag,
        available_routes=resolved_available_routes,
        available_menu_options=tuple(str(option) for option in (available_menu_options or ())),
        statuses=statuses,
        injuries=injuries,
        travel_restrictions=travel_restrictions,
        inventory=_sorted_strings(getattr(player, "_inventory", ())),
        broken_items=broken_items,
        repairing_items=repairing_items,
        flask_effects=_sorted_strings(getattr(player, "_flask_effects", ())),
        companions=_sorted_strings(_safe_call(player, "get_all_companions", ()) or ()),
        companion_count=companion_metrics["count"],
        companion_low_happiness_count=companion_metrics["low_happiness"],
        companion_runaway_risk_count=companion_metrics["runaway_risk"],
        companion_bonded_count=companion_metrics["bonded"],
        companion_unfed_count=companion_metrics["unfed"],
        inventory_food_count=inventory_food_count,
        has_car=bool(player.has_item("Car")),
        has_map=bool(player.has_item("Map")),
        has_worn_map=bool(player.has_item("Worn Map")),
        has_marvin_access=bool(player.has_item("Map") or player.has_item("Worn Map")),
        has_met_witch=bool(player.has_met("Witch")),
        has_met_vinnie=bool(player.has_met("Vinnie") or int(_safe_call(player, "get_loan_shark_debt", 0) or 0) > 0),
        has_met_gus=bool(player.has_met("Grimy Gus")),
        chosen_mechanic=str(_safe_call(player, "get_chosen_mechanic", None)) if _safe_call(player, "get_chosen_mechanic", None) not in {None, "", "None"} else None,
        mechanic_visits=int(_safe_call(player, "get_mechanic_visits", 0) or 0),
        loan_debt=int(_safe_call(player, "get_loan_shark_debt", 0) or 0),
        loan_warning_level=int(_safe_call(player, "get_loan_shark_warning_level", 0) or 0),
        fraudulent_cash=int(_safe_call(player, "get_fraudulent_cash", 0) or 0),
        dealer_happiness=int(_safe_call(player, "get_dealer_happiness", 50) or 50),
        store_candidate_count=_economy_hint_value(normalized_economy_hints, "store_candidate_count"),
        store_best_purchase_priority=_economy_hint_value(normalized_economy_hints, "store_best_priority"),
        store_target_spend=_economy_hint_value(normalized_economy_hints, "store_target_spend"),
        pawn_sellable_value=_economy_hint_value(normalized_economy_hints, "pawn_sellable_value"),
        pawn_planned_sale_count=_economy_hint_value(normalized_economy_hints, "pawn_planned_sale_count"),
        pawn_planned_sale_value=_economy_hint_value(normalized_economy_hints, "pawn_planned_sale_value"),
        marvin_affordable_priority=_economy_hint_value(normalized_economy_hints, "marvin_affordable_priority"),
        marvin_candidate_price=_economy_hint_value(normalized_economy_hints, "marvin_candidate_price"),
        marvin_strong_window=bool(_economy_hint_value(normalized_economy_hints, "marvin_strong_window")),
        opportunity_flags=flags,
        current_progress_goal_candidates=_goal_candidates(
            player,
            flags,
            health,
            sanity,
            statuses,
            injuries,
            balance,
            fatigue,
            companion_metrics,
        ),
    )