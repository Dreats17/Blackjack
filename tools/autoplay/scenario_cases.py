from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from .interfaces import DecisionOption, DecisionRequest
from .planner import StrategicPlan, choose_strategic_goal
from .policies import choose_blackjack_bet, choose_event_inline_choice, choose_event_option, choose_event_yes_no
from .route_policy import choose_route_option
from .state import GameState, build_game_state_snapshot


@dataclass(frozen=True)
class ScenarioResult:
    scenario_id: str
    suite: str
    passed: bool
    summary: str
    details: dict[str, object]


RouteCheck = Callable[[StrategicPlan, str], tuple[bool, str]]
BetCheck = Callable[[int], tuple[bool, str]]


class _FakeListsShim:
    """Minimal shim for FakeScenarioPlayer._lists so workbench recipe checks work."""

    def __init__(self, player: "FakeScenarioPlayer") -> None:
        self._player = player

    def get_available_recipes(self, _player=None) -> dict[str, dict]:
        """Return recipes for which all ingredients are in player inventory."""
        # Inline subset of the full recipe table from lists.py make_crafting_recipes.
        # Covers the most commonly-reached recipes in test scenarios.
        all_recipes: dict[str, dict] = {
            "Emergency Blanket": {"ingredients": ["Garbage Bag", "Duct Tape"], "category": "survival"},
            "Wound Salve": {"ingredients": ["First Aid Kit", "Super Glue"], "category": "remedy"},
            "Home Remedy": {"ingredients": ["First Aid Kit", "Cough Drops"], "category": "remedy"},
            "Feeding Station": {"ingredients": ["Plastic Wrap", "Duct Tape"], "category": "companion"},
            "Binocular Scope": {"ingredients": ["Binoculars", "Duct Tape"], "category": "tool"},
            "Lockpick Set": {"ingredients": ["Pocket Knife", "Fishing Line"], "category": "tool"},
            "Splint": {"ingredients": ["Duct Tape", "Rope"], "category": "remedy"},
            "Companion Bed": {"ingredients": ["Blanket", "Duct Tape"], "category": "companion"},
            "Pet Toy": {"ingredients": ["Rope", "Rubber Bands"], "category": "companion"},
            "Rain Collector": {"ingredients": ["Plastic Wrap", "Garbage Bag"], "category": "survival"},
            "Snare Trap": {"ingredients": ["Rope", "Fishing Line"], "category": "trap"},
            "Improvised Trap": {"ingredients": ["Fishing Line", "Pocket Knife"], "category": "trap"},
            "Pepper Spray": {"ingredients": ["Bug Spray", "Lighter"], "category": "weapon"},
            "Shiv": {"ingredients": ["Duct Tape", "Pocket Knife"], "category": "weapon"},
        }
        return {
            name: recipe
            for name, recipe in all_recipes.items()
            if all(self._player.has_item(ing) for ing in recipe["ingredients"])
        }


class FakeScenarioPlayer:
    def __init__(
        self,
        *,
        day: int,
        balance: int,
        rank: int,
        health: int,
        sanity: int,
        fatigue: int = 0,
        inventory: tuple[str, ...] = (),
        statuses: tuple[str, ...] = (),
        injuries: tuple[str, ...] = (),
        met: tuple[str, ...] = (),
        store_inventory: tuple[tuple[str, int], ...] = (),
        collectible_prices: dict[str, int] | None = None,
        companions: dict[str, dict] | None = None,
        food_data: dict[str, dict] | None = None,
        mechanic_visits: int = 0,
        chosen_mechanic: str | None = None,
        dealer_happiness: int = 50,
        gift_system_unlocked: bool = False,
        has_wrapped_gift: bool = False,
        tom_dreams: int = 0,
        frank_dreams: int = 0,
        oswald_dreams: int = 0,
        loan_debt: int = 0,
        loan_warning_level: int = 0,
        fraudulent_cash: int = 0,
        flasks: tuple[str, ...] = (),
    ) -> None:
        self._day = day
        self._balance = balance
        self._rank = rank
        self._health = health
        self._sanity = sanity
        self._fatigue = fatigue
        self._alive = True
        self._inventory = list(inventory)
        self._status_effects = list(statuses)
        self._injuries = list(injuries)
        self._travel_restrictions = []
        self._broken_inventory = []
        self._repairing_inventory = []
        self._flask_effects = list(flasks)
        self._convenience_store_inventory = list(store_inventory)
        self._collectible_prices = dict(collectible_prices or {})
        self._companions = dict(companions or {})
        self._food_data = dict(food_data or {})
        self._mechanic_visits = mechanic_visits
        self._chosen_mechanic = chosen_mechanic
        self._dealer_happiness = dealer_happiness
        self._gift_system_unlocked = gift_system_unlocked
        self._has_wrapped_gift = has_wrapped_gift
        self._tom_dreams = tom_dreams
        self._frank_dreams = frank_dreams
        self._oswald_dreams = oswald_dreams
        self._loan_debt = loan_debt
        self._loan_warning_level = loan_warning_level
        self._fraudulent_cash = fraudulent_cash
        self._met = set(met)
        self._autoplay_location_last_day = {}
        self._autoplay_location_count = {}
        # Minimal _lists shim: returns the full game recipe set so workbench routing
        # can evaluate _workbench_best_craft_candidate correctly.
        self._lists = _FakeListsShim(self)

    def get_balance(self):
        return self._balance

    def get_health(self):
        return self._health

    def get_sanity(self):
        return self._sanity

    def get_fatigue(self):
        return self._fatigue

    def get_rank(self):
        return self._rank

    def is_alive(self):
        return self._alive

    def has_item(self, item_name):
        return item_name in self._inventory

    def has_met(self, name):
        return name in self._met

    def has_flask_effect(self, effect_name):
        return effect_name in self._flask_effects

    def get_all_companions(self):
        return dict(self._companions)

    def get_inventory_food(self):
        return [item_name for item_name in self._inventory if item_name in self._food_data]

    def get_food_data(self, item_name):
        food = self._food_data.get(item_name)
        return None if food is None else dict(food)

    def get_collectible_prices(self):
        return dict(self._collectible_prices)

    def can_access_upgrades(self):
        return False

    def can_upgrade(self, _item_name):
        return False

    def get_mechanic_visits(self):
        return self._mechanic_visits

    def get_chosen_mechanic(self):
        return self._chosen_mechanic

    def get_loan_shark_debt(self):
        return self._loan_debt

    def get_loan_shark_warning_level(self):
        return self._loan_warning_level

    def get_fraudulent_cash(self):
        return self._fraudulent_cash

    def get_dealer_happiness(self):
        return self._dealer_happiness

    def is_gift_system_unlocked(self):
        return self._gift_system_unlocked

    def has_gift_wrapped(self):
        return self._has_wrapped_gift

    def get_tom_dreams(self):
        return self._tom_dreams

    def get_frank_dreams(self):
        return self._frank_dreams

    def get_oswald_dreams(self):
        return self._oswald_dreams

    def len_flasks(self):
        return 0

    def has_danger(self, _danger_name):
        return False

    def has_broken_item(self, _item_name):
        return False

    def is_repairing_item(self, _item_name):
        return False

    def has_fire_source(self):
        return False


def _route_options(*labels: str) -> tuple[DecisionOption, ...]:
    return tuple(
        DecisionOption(option_id=f"route_{index + 1}", label=label, value=label)
        for index, label in enumerate(labels)
    )


def _event_options(*labels: str) -> tuple[DecisionOption, ...]:
    return tuple(
        DecisionOption(option_id=f"event_{index + 1}", label=label, value=label)
        for index, label in enumerate(labels)
    )


def _assert_goal_and_route(expected_goal: str, expected_route: str) -> RouteCheck:
    def checker(plan: StrategicPlan, chosen_route: str) -> tuple[bool, str]:
        ok = plan.goal == expected_goal and chosen_route == expected_route
        return ok, f"goal={plan.goal} route={chosen_route} expected_goal={expected_goal} expected_route={expected_route}"

    return checker


def _assert_max_bet(max_bet: int) -> BetCheck:
    def checker(bet: int) -> tuple[bool, str]:
        ok = bet <= max_bet
        return ok, f"bet={bet} max_bet={max_bet}"

    return checker


def _assert_min_bet(min_bet: int) -> BetCheck:
    def checker(bet: int) -> tuple[bool, str]:
        ok = bet >= min_bet
        return ok, f"bet={bet} min_bet={min_bet}"

    return checker


def _assert_balance_blend(balance: int) -> BetCheck:
    def checker(bet: int) -> tuple[bool, str]:
        ok = bet > balance
        return ok, f"bet={bet} balance={balance}"

    return checker


def _run_route_scenario(
    scenario_id: str,
    suite: str,
    state: GameState,
    route_labels: tuple[str, ...],
    metadata: dict[str, object],
    check: RouteCheck,
) -> ScenarioResult:
    plan = choose_strategic_goal(state)
    request = DecisionRequest(
        request_type="route_select",
        stable_context_id="scenario_route",
        game_state=state.to_dict(),
        normalized_options=_route_options(*route_labels),
        metadata={"day": state.day, **metadata},
    )
    option, trace = choose_route_option(request, plan)
    chosen_route = "" if option is None else str(option.value if option.value is not None else option.label)
    passed, detail = check(plan, chosen_route)
    return ScenarioResult(
        scenario_id=scenario_id,
        suite=suite,
        passed=passed,
        summary=detail,
        details={
            "goal": plan.goal,
            "goal_reason": plan.reason,
            "route": chosen_route,
            "trace_reason": trace.reason,
        },
    )


def _run_event_yes_no_scenario(
    scenario_id: str,
    suite: str,
    state: GameState,
    prompt: str,
    recent_lines: tuple[str, ...],
    metadata: dict[str, object],
    expected_answer: str,
) -> ScenarioResult:
    plan = choose_strategic_goal(state)
    request = DecisionRequest(
        request_type="yes_no",
        stable_context_id="scenario_yes_no",
        game_state=state.to_dict(),
        normalized_options=_event_options("yes", "no"),
        raw_prompt_text=prompt,
        raw_recent_text=recent_lines,
        metadata={"day": state.day, **metadata},
    )
    answer, trace = choose_event_yes_no(request, plan)
    passed = answer == expected_answer
    return ScenarioResult(
        scenario_id=scenario_id,
        suite=suite,
        passed=passed,
        summary=f"answer={answer} expected={expected_answer}",
        details={
            "goal": plan.goal,
            "answer": answer,
            "expected": expected_answer,
            "trace_reason": None if trace is None else trace.reason,
        },
    )


def _run_event_option_scenario(
    scenario_id: str,
    suite: str,
    state: GameState,
    options: tuple[str, ...],
    metadata: dict[str, object],
    expected_label: str,
) -> ScenarioResult:
    plan = choose_strategic_goal(state)
    request = DecisionRequest(
        request_type="event_branch",
        stable_context_id="scenario_event_branch",
        game_state=state.to_dict(),
        normalized_options=_event_options(*options),
        metadata={"day": state.day, **metadata},
    )
    option, trace = choose_event_option(request, plan)
    chosen_label = "" if option is None else str(option.value if option.value is not None else option.label)
    passed = chosen_label == expected_label
    return ScenarioResult(
        scenario_id=scenario_id,
        suite=suite,
        passed=passed,
        summary=f"choice={chosen_label} expected={expected_label}",
        details={
            "goal": plan.goal,
            "choice": chosen_label,
            "expected": expected_label,
            "trace_reason": None if trace is None else trace.reason,
        },
    )


def _run_event_inline_scenario(
    scenario_id: str,
    suite: str,
    state: GameState,
    prompt: str,
    recent_lines: tuple[str, ...],
    choices: tuple[str, ...],
    metadata: dict[str, object],
    expected_choice: str,
) -> ScenarioResult:
    plan = choose_strategic_goal(state)
    request = DecisionRequest(
        request_type="event_inline",
        stable_context_id="scenario_event_inline",
        game_state=state.to_dict(),
        normalized_options=_event_options(*choices),
        raw_prompt_text=prompt,
        raw_recent_text=recent_lines,
        metadata={"day": state.day, **metadata},
    )
    chosen, trace = choose_event_inline_choice(request, plan)
    passed = chosen == expected_choice
    return ScenarioResult(
        scenario_id=scenario_id,
        suite=suite,
        passed=passed,
        summary=f"choice={chosen} expected={expected_choice}",
        details={
            "goal": plan.goal,
            "choice": chosen,
            "expected": expected_choice,
            "trace_reason": None if trace is None else trace.reason,
        },
    )


def _run_bet_scenario(
    scenario_id: str,
    suite: str,
    state: GameState,
    metadata: dict[str, object],
    check: BetCheck,
) -> ScenarioResult:
    plan = choose_strategic_goal(state)
    request = DecisionRequest(
        request_type="blackjack_bet",
        stable_context_id="scenario_blackjack_bet",
        game_state=state.to_dict(),
        metadata={"day": state.day, **metadata},
    )
    bet, trace = choose_blackjack_bet(request, plan)
    chosen_bet = 0 if bet is None else int(bet)
    passed, detail = check(chosen_bet)
    return ScenarioResult(
        scenario_id=scenario_id,
        suite=suite,
        passed=passed,
        summary=detail,
        details={
            "goal": plan.goal,
            "bet": chosen_bet,
            "trace_reason": trace.reason,
            "trace_metadata": trace.metadata,
        },
    )


def _run_snapshot_goal_scenario(
    scenario_id: str,
    suite: str,
    player: FakeScenarioPlayer,
    *,
    economy_hints: dict[str, object],
    available_routes: tuple[str, ...] = (),
    expected_goal: str,
) -> ScenarioResult:
    state = build_game_state_snapshot(
        player,
        current_context_tag="scenario_snapshot_goal",
        available_routes=available_routes,
        economy_hints=economy_hints,
    )
    plan = choose_strategic_goal(state)
    passed = plan.goal == expected_goal
    return ScenarioResult(
        scenario_id=scenario_id,
        suite=suite,
        passed=passed,
        summary=f"goal={plan.goal} expected={expected_goal}",
        details={
            "goal": plan.goal,
            "expected": expected_goal,
            "available_routes": list(state.available_routes),
            "opportunity_flags": dict(state.opportunity_flags),
        },
    )


def _run_quicktest_destination_scenario(
    scenario_id: str,
    suite: str,
    player: FakeScenarioPlayer,
    route_labels: tuple[str, ...],
    expected_label: str,
) -> ScenarioResult:
    from tools import quicktest as quicktest_harness

    menu_options = tuple((index + 1, label) for index, label in enumerate(route_labels))
    chosen_number = quicktest_harness._choose_destination(menu_options, player)
    by_number = {number: label for number, label in menu_options}
    chosen_label = by_number.get(chosen_number, "")
    passed = chosen_label == expected_label
    return ScenarioResult(
        scenario_id=scenario_id,
        suite=suite,
        passed=passed,
        summary=f"route={chosen_label} expected={expected_label}",
        details={
            "route": chosen_label,
            "expected": expected_label,
            "day": player._day,
            "balance": player._balance,
            "health": player._health,
            "sanity": player._sanity,
            "statuses": list(player._status_effects),
            "injuries": list(player._injuries),
        },
    )


def _run_quicktest_loan_borrow_scenario(
    scenario_id: str,
    suite: str,
    player: FakeScenarioPlayer,
    menu_options: tuple[tuple[int, str], ...],
    expected_label: str,
) -> ScenarioResult:
    from tools import quicktest as quicktest_harness

    chosen_number = quicktest_harness._choose_loan_borrow_amount(menu_options, player)
    by_number = {number: label for number, label in menu_options}
    chosen_label = by_number.get(chosen_number, "")
    passed = chosen_label == expected_label
    return ScenarioResult(
        scenario_id=scenario_id,
        suite=suite,
        passed=passed,
        summary=f"choice={chosen_label} expected={expected_label}",
        details={
            "choice": chosen_label,
            "expected": expected_label,
            "day": player._day,
            "balance": player._balance,
            "health": player._health,
            "sanity": player._sanity,
            "inventory": list(player._inventory),
            "met": sorted(player._met),
        },
    )


def _run_quicktest_mechanic_offer_scenario(
    scenario_id: str,
    suite: str,
    player: FakeScenarioPlayer,
    *,
    cost: int,
    recent: str,
    expected_answer: str,
) -> ScenarioResult:
    from tools import quicktest as quicktest_harness

    answer = "yes" if quicktest_harness._should_buy_car_repair(player, cost, recent.lower()) else "no"
    passed = answer == expected_answer
    return ScenarioResult(
        scenario_id=scenario_id,
        suite=suite,
        passed=passed,
        summary=f"answer={answer} expected={expected_answer}",
        details={
            "answer": answer,
            "expected": expected_answer,
            "day": player._day,
            "balance": player._balance,
            "recent": recent,
            "met": sorted(player._met),
        },
    )


def _run_quicktest_store_menu_scenario(
    scenario_id: str,
    suite: str,
    player: FakeScenarioPlayer,
    menu_options: tuple[tuple[int, str], ...],
    expected_label: str,
) -> ScenarioResult:
    from tools import quicktest as quicktest_harness

    chosen_number = quicktest_harness._choose_store_item(menu_options, player)
    by_number = {number: label for number, label in menu_options}
    chosen_label = by_number.get(chosen_number, "")
    passed = chosen_label == expected_label
    return ScenarioResult(
        scenario_id=scenario_id,
        suite=suite,
        passed=passed,
        summary=f"choice={chosen_label} expected={expected_label}",
        details={
            "choice": chosen_label,
            "expected": expected_label,
            "balance": player._balance,
            "dealer_happiness": player._dealer_happiness,
            "store_inventory": list(player._convenience_store_inventory),
        },
    )


def _run_quicktest_companion_menu_scenario(
    scenario_id: str,
    suite: str,
    player: FakeScenarioPlayer,
    menu_options: tuple[tuple[int, str], ...],
    expected_label: str,
) -> ScenarioResult:
    from tools import quicktest as quicktest_harness

    chosen_number = quicktest_harness._choose_companion_interaction(menu_options, player)
    by_number = {number: label for number, label in menu_options}
    chosen_label = by_number.get(chosen_number, "")
    passed = chosen_label == expected_label
    return ScenarioResult(
        scenario_id=scenario_id,
        suite=suite,
        passed=passed,
        summary=f"choice={chosen_label} expected={expected_label}",
        details={
            "choice": chosen_label,
            "expected": expected_label,
            "companions": dict(player._companions),
        },
    )


def run_all_scenarios() -> list[ScenarioResult]:
    results: list[ScenarioResult] = []

    results.append(
        _run_route_scenario(
            "saveable_doctor_death",
            "route",
            GameState(
                day=12,
                balance=240,
                rank=0,
                health=28,
                sanity=44,
                fatigue=34,
                alive=True,
                current_context_tag="afternoon_destination",
                has_car=True,
                mechanic_visits=1,
                opportunity_flags={
                    "can_visit_marvin": False,
                    "can_restock_supplies": True,
                },
                current_progress_goal_candidates=("survive_emergency", "stabilize_health", "restock_supplies"),
            ),
            ("Doctor's Office", "Convenience Store", "Stay Home"),
            {
                "urgent_medical": True,
                "wants_doctor": True,
                "needs_recovery_day": False,
                "has_car": True,
                "medical_choice": "Doctor's Office",
                "wants_store": True,
                "store_spend": 60,
            },
            _assert_goal_and_route("survive_emergency", "Doctor's Office"),
        )
    )

    results.append(
        _run_snapshot_goal_scenario(
            "no_car_store_hints_do_not_create_store_goal",
            "state_goal",
            FakeScenarioPlayer(
                day=5,
                balance=141,
                rank=0,
                health=64,
                sanity=75,
                fatigue=0,
            ),
            economy_hints={
                "store_candidate_count": 4,
                "store_best_priority": 78,
                "store_target_spend": 8,
            },
            expected_goal="acquire_car",
        )
    )

    results.append(
        _run_snapshot_goal_scenario(
            "low_cash_marvin_access_does_not_force_marvin_goal",
            "state_goal",
            FakeScenarioPlayer(
                day=12,
                balance=73,
                rank=0,
                health=96,
                sanity=41,
                inventory=("Car", "Worn Map"),
            ),
            economy_hints={
                "marvin_affordable_priority": 0,
            },
            expected_goal="push_next_rank",
        )
    )

    results.append(
        _run_snapshot_goal_scenario(
            "strong_marvin_window_prefers_marvin_goal",
            "state_goal",
            FakeScenarioPlayer(
                day=24,
                balance=18000,
                rank=1,
                health=84,
                sanity=71,
                inventory=("Car", "Worn Map"),
            ),
            economy_hints={
                "marvin_affordable_priority": 92,
                "marvin_candidate_price": 12000,
                "marvin_strong_window": 1,
            },
            available_routes=("Marvin's Mystical Merchandise", "Convenience Store"),
            expected_goal="exploit_marvin",
        )
    )

    results.append(
        _run_snapshot_goal_scenario(
            "healthy_midgame_store_pressure_defers_to_rank_push",
            "state_goal",
            FakeScenarioPlayer(
                day=26,
                balance=2500,
                rank=1,
                health=82,
                sanity=64,
                fatigue=14,
                inventory=("Car",),
                store_inventory=(("Pocket Knife", 90), ("Water Bottles", 60), ("Binoculars", 140)),
            ),
            economy_hints={
                "store_candidate_count": 3,
                "store_best_priority": 70,
                "store_target_spend": 90,
            },
            expected_goal="push_next_rank",
        )
    )

    results.append(
        _run_route_scenario(
            "catalog_push_store_buyout_prefers_store_route",
            "route",
            GameState(
                day=41,
                balance=9600,
                rank=1,
                health=86,
                sanity=72,
                fatigue=10,
                alive=True,
                current_context_tag="afternoon_destination",
                has_car=True,
                has_worn_map=True,
                store_candidate_count=3,
                store_best_purchase_priority=90,
                store_target_spend=420,
                opportunity_flags={
                    "can_restock_supplies": True,
                },
                current_progress_goal_candidates=("push_next_rank", "restock_supplies"),
            ),
            ("Convenience Store", "Pawn Shop", "Stay Home"),
            {
                "has_car": True,
                "wants_store": True,
                "store_spend": 420,
                "catalog_push_active": True,
                "catalog_push_kind": "store",
                "catalog_push_spend": 420,
                "catalog_push_count": 3,
                "catalog_push_priority": 90,
            },
            _assert_goal_and_route("restock_supplies", "Convenience Store"),
        )
    )

    results.append(
        _run_route_scenario(
            "marvin_access_but_no_visit",
            "route",
            GameState(
                day=24,
                balance=18000,
                rank=1,
                health=84,
                sanity=71,
                fatigue=20,
                alive=True,
                current_context_tag="afternoon_destination",
                has_car=True,
                has_worn_map=True,
                has_marvin_access=True,
                opportunity_flags={"can_visit_marvin": True},
                current_progress_goal_candidates=("exploit_marvin", "push_next_rank"),
            ),
            ("Marvin", "Convenience Store", "Stay Home"),
            {
                "has_car": True,
                "has_marvin_access": True,
                "wants_marvin": True,
                "marvin_priority": 92,
                "store_spend": 0,
            },
            _assert_goal_and_route("exploit_marvin", "Marvin"),
        )
    )

    results.append(
        _run_route_scenario(
            "companion_food_crisis",
            "route",
            GameState(
                day=18,
                balance=900,
                rank=1,
                health=77,
                sanity=51,
                fatigue=22,
                alive=True,
                current_context_tag="afternoon_destination",
                has_car=True,
                companion_count=3,
                companion_low_happiness_count=2,
                inventory_food_count=0,
                store_candidate_count=4,
                store_best_purchase_priority=95,
                store_target_spend=140,
                opportunity_flags={
                    "can_preserve_companions": True,
                    "can_restock_supplies": True,
                },
                current_progress_goal_candidates=("preserve_companion_roster", "restock_supplies", "push_next_rank"),
            ),
            ("Convenience Store", "Pawn Shop", "Stay Home"),
            {
                "has_car": True,
                "wants_store": True,
                "store_spend": 140,
                "wants_pawn": False,
            },
            _assert_goal_and_route("restock_supplies", "Convenience Store"),
        )
    )

    results.append(
        _run_route_scenario(
            "debt_pressure_case",
            "route",
            GameState(
                day=21,
                balance=340,
                rank=0,
                health=74,
                sanity=58,
                fatigue=18,
                alive=True,
                current_context_tag="afternoon_destination",
                has_car=True,
                loan_debt=4200,
                loan_warning_level=3,
                pawn_planned_sale_count=2,
                pawn_planned_sale_value=260,
                opportunity_flags={
                    "can_reduce_debt_risk": True,
                    "can_contain_debt_escalation": True,
                    "can_cashout_pawn_inventory": True,
                },
                current_progress_goal_candidates=("contain_debt_escalation", "cashout_pawn_inventory", "reduce_debt_risk"),
            ),
            ("Loan Shark", "Pawn Shop", "Marvin"),
            {
                "has_car": True,
                "wants_loan": True,
                "loan_pressure": 64,
                "wants_pawn": True,
                "pawn_value": 260,
                "wants_marvin": False,
            },
            _assert_goal_and_route("contain_debt_escalation", "Loan Shark"),
        )
    )

    results.append(
        _run_route_scenario(
            "high_fatigue_missed_event_case",
            "route",
            GameState(
                day=16,
                balance=700,
                rank=1,
                health=69,
                sanity=48,
                fatigue=92,
                alive=True,
                current_context_tag="afternoon_destination",
                has_car=True,
                opportunity_flags={"can_reduce_fatigue_pressure": True},
                current_progress_goal_candidates=("reduce_fatigue_pressure", "push_next_rank"),
            ),
            ("Stay Home", "Convenience Store", "Marvin"),
            {
                "has_car": True,
                "needs_recovery_day": True,
                "wants_store": False,
                "wants_marvin": False,
            },
            _assert_goal_and_route("reduce_fatigue_pressure", "Stay Home"),
        )
    )

    results.append(
        _run_route_scenario(
            "car_trouble_interruption_case",
            "route",
            GameState(
                day=22,
                balance=620,
                rank=1,
                health=78,
                sanity=61,
                fatigue=26,
                alive=True,
                current_context_tag="afternoon_destination",
                has_car=True,
                travel_restrictions=("Engine Trouble",),
                mechanic_visits=1,
                opportunity_flags={
                    "can_recover_from_car_trouble": True,
                    "can_advance_mechanic_arc": True,
                },
                current_progress_goal_candidates=("recover_from_car_trouble", "advance_mechanic_arc"),
            ),
            ("Tom's Auto Shop", "Stay Home", "Convenience Store"),
            {
                "has_car": True,
                "wants_mechanic": True,
                "mechanic_urgency": 80,
                "needs_recovery_day": False,
            },
            _assert_goal_and_route("recover_from_car_trouble", "Tom's Auto Shop"),
        )
    )

    results.append(
        _run_quicktest_destination_scenario(
            "urgent_medical_interrupt_route",
            "route_interrupt",
            FakeScenarioPlayer(
                day=14,
                balance=350,
                rank=0,
                health=24,
                sanity=45,
                fatigue=18,
                inventory=("Car",),
                injuries=("Broken Ribs",),
            ),
            ("Doctor's Office", "Convenience Store", "Stay Home"),
            "Doctor's Office",
        )
    )

    results.append(
        _run_quicktest_destination_scenario(
            "recovery_day_interrupt_route",
            "route_interrupt",
            FakeScenarioPlayer(
                day=18,
                balance=500,
                rank=1,
                health=58,
                sanity=40,
                fatigue=20,
                inventory=("Car",),
                injuries=("Scraped Knee",),
                store_inventory=(("LifeAlert", 100),),
            ),
            ("Doctor's Office", "Convenience Store", "Stay Home"),
            "Stay Home",
        )
    )

    results.append(
        _run_quicktest_destination_scenario(
            "recovery_day_store_bypass_route",
            "route_interrupt",
            FakeScenarioPlayer(
                day=18,
                balance=500,
                rank=1,
                health=68,
                sanity=34,
                fatigue=20,
                inventory=("Car",),
                injuries=("Scraped Knee",),
                store_inventory=(("LifeAlert", 100),),
            ),
            ("Convenience Store", "Stay Home", "Marvin's Mystical Merchandise"),
            "Convenience Store",
        )
    )

    results.append(
        _run_quicktest_destination_scenario(
            "recovery_day_pawn_bypass_route",
            "route_interrupt",
            FakeScenarioPlayer(
                day=18,
                balance=300,
                rank=1,
                health=66,
                sanity=34,
                fatigue=20,
                inventory=("Car", "Silver Ring"),
                injuries=("Scraped Knee",),
                collectible_prices={"Silver Ring": 300},
            ),
            ("Grimy Gus's Pawn Emporium", "Stay Home", "Convenience Store"),
            "Grimy Gus's Pawn Emporium",
        )
    )

    results.append(
        _run_quicktest_destination_scenario(
            "recovery_day_no_car_mechanic_bypass_route",
            "route_interrupt",
            FakeScenarioPlayer(
                day=10,
                balance=160,
                rank=0,
                health=54,
                sanity=45,
                fatigue=18,
                injuries=("Scraped Knee",),
                met=("Tom", "Tom Event"),
            ),
            ("Trusty Tom's Trucks and Tires", "Doctor's Office", "Stay Home"),
            # Without a car the bot can't travel on foot; Stay Home is the correct choice.
            "Stay Home",
        )
    )

    results.append(
        _run_quicktest_destination_scenario(
            "recovery_day_no_car_mild_status_stack_bypass_route",
            "route_interrupt",
            FakeScenarioPlayer(
                day=10,
                balance=190,
                rank=0,
                health=58,
                sanity=42,
                fatigue=18,
                injuries=("Broken Leg",),
                statuses=("Flu", "Ringworm", "Sinus Infection"),
                met=("Tom", "Tom Event"),
            ),
            ("Trusty Tom's Trucks and Tires", "Doctor's Office", "Stay Home"),
            # No car means no on-foot travel; compound conditions but can't afford doctor ($190).
            "Stay Home",
        )
    )

    results.append(
        _run_quicktest_destination_scenario(
            "no_car_progression_defers_nonurgent_doctor_route",
            "route_interrupt",
            FakeScenarioPlayer(
                day=10,
                balance=300,
                rank=0,
                health=50,
                sanity=45,
                fatigue=18,
                injuries=("Broken Leg",),
                met=("Tom", "Tom Event"),
            ),
            ("Trusty Tom's Trucks and Tires", "Doctor's Office", "Stay Home"),
            # Broken Leg + health=50 + balance=$300: urgent medical care is the right call.
            "Doctor's Office",
        )
    )

    results.append(
        _run_quicktest_destination_scenario(
            "car_injury_doctor_preempts_progression",
            "route_interrupt",
            FakeScenarioPlayer(
                day=19,
                balance=176,
                rank=0,
                health=79,
                sanity=96,
                inventory=("Car", "Worn Map"),
                injuries=("Broken Leg",),
            ),
            ("Doctor's Office", "Marvin's Mystical Merchandise", "Convenience Store", "Stay Home"),
            "Doctor's Office",
        )
    )

    results.append(
        _run_quicktest_destination_scenario(
            "workbench_craft_route_fires_when_ingredients_ready",
            "route_interrupt",
            FakeScenarioPlayer(
                day=22,
                balance=1800,
                rank=1,
                health=80,
                sanity=55,
                inventory=("Car", "Tool Kit", "Duct Tape", "Garbage Bag"),
            ),
            # Car Workbench is unlocked because player has Tool Kit.
            # Emergency Blanket recipe: Garbage Bag + Duct Tape — both in inventory.
            # No higher-priority destinations present; workbench craft should win.
            ("Convenience Store", "Car Workbench", "Stay Home"),
            "Car Workbench",
        )
    )

    # Crafting synergy: completing boost — player has Duct Tape + Tool Kit;
    # Garbage Bag in store completes Emergency Blanket → priority >= 86, store fires.
    results.append(
        _run_quicktest_destination_scenario(
            "crafting_ingredient_completing_boost_triggers_store",
            "route_interrupt",
            FakeScenarioPlayer(
                day=15,
                balance=700,
                rank=1,
                health=82,
                sanity=60,
                inventory=("Car", "Tool Kit", "Duct Tape"),
                store_inventory=(("Garbage Bag", 3),),
            ),
            ("Convenience Store", "Stay Home"),
            "Convenience Store",
        )
    )

    # Crafting synergy: starting boost — player has Tool Kit but no other ingredient;
    # Garbage Bag alone gets a starting boost to 78, which crosses the rank-1 secondary
    # store gate (>= 68) with balance >= 600.
    results.append(
        _run_quicktest_destination_scenario(
            "crafting_ingredient_starting_boost_triggers_store",
            "route_interrupt",
            FakeScenarioPlayer(
                day=15,
                balance=700,
                rank=1,
                health=82,
                sanity=60,
                inventory=("Car", "Tool Kit"),
                store_inventory=(("Garbage Bag", 3),),
            ),
            ("Convenience Store", "Stay Home"),
            "Convenience Store",
        )
    )

    results.append(
        _run_quicktest_destination_scenario(
            "witch_flask_only_run_fires_when_healthy_and_affordable",
            "route_interrupt",
            FakeScenarioPlayer(
                day=25,
                balance=15000,
                rank=2,
                health=80,
                sanity=55,
                # No Map → Marvin not accessible, so flask-only witch path can fire.
                # Player is healthy (health >= 72, sanity >= 38) with $15k.
                # Fortunate Day estimate $12k fits comfortably within budget.
                inventory=("Car",),
                met=("Witch",),
                store_inventory=(("LifeAlert", 120),),
            ),
            # Witch Doctor should be chosen over store (flask-only path fires).
            ("Witch Doctor's Tower", "Convenience Store", "Stay Home"),
            "Witch Doctor's Tower",
        )
    )

    shared_event_state = GameState(
        day=19,
        balance=600,
        rank=1,
        health=80,
        sanity=60,
        fatigue=20,
        alive=True,
        current_context_tag="event",
        has_car=True,
        current_progress_goal_candidates=("push_next_rank",),
    )

    results.append(
        _run_event_yes_no_scenario(
            "suspicious_bargain_refusal",
            "event_yes_no",
            shared_event_state,
            "accept the devil's offer?",
            (),
            {
                "prompt_lower": "accept the devil's offer?",
                "recent_lower": "a smiling stranger promises an easy out if you just agree now",
            },
            "no",
        )
    )

    results.append(
        _run_event_yes_no_scenario(
            "loyalty_bonus_money_refusal",
            "event_yes_no",
            shared_event_state,
            "take the money?",
            ("A loyalty bonus offer appears before you.",),
            {
                "prompt_lower": "take the money?",
                "recent_lower": "loyalty bonus - take the money?",
            },
            "no",
        )
    )

    results.append(
        _run_event_yes_no_scenario(
            "kyle_secret_kept",
            "event_yes_no",
            shared_event_state,
            "Promise to keep his secret?",
            ("Kyle looks at you with desperate eyes.",),
            {
                "prompt_lower": "promise to keep his secret?",
                "recent_lower": "kyle looks at you with desperate eyes.",
            },
            "yes",
        )
    )

    results.append(
        _run_event_yes_no_scenario(
            "street_musician_relief_gate",
            "event_yes_no",
            GameState(
                day=11,
                balance=60,
                rank=0,
                health=80,
                sanity=70,
                fatigue=10,
                alive=True,
                current_context_tag="event",
                current_progress_goal_candidates=("push_next_rank",),
            ),
            "Give him some money to make him go away?",
            (),
            {
                "prompt_lower": "give him some money to make him go away?",
                "recent_lower": "a street musician is butchering careless whisper outside your car",
            },
            "yes",
        )
    )

    results.append(
        _run_event_yes_no_scenario(
            "investment_pitch_refusal",
            "event_yes_no",
            shared_event_state,
            "Give him $100 to make him go away?",
            (),
            {
                "prompt_lower": "give him $100 to make him go away?",
                "recent_lower": "a guy in a cheap suit corners you with a business opportunity",
            },
            "no",
        )
    )

    results.append(
        _run_event_yes_no_scenario(
            "casino_enforcement_buyout",
            "event_yes_no",
            GameState(
                day=140,
                balance=850000,
                rank=4,
                health=82,
                sanity=71,
                fatigue=18,
                alive=True,
                current_context_tag="event",
                has_car=True,
                current_progress_goal_candidates=("push_next_rank",),
            ),
            "Pay $200,000?",
            (),
            {
                "prompt_lower": "pay $200,000?",
                "recent_lower": "the house doesn't like to lose. under the bar, you feel something cold press against your ribs. a gun.",
            },
            "yes",
        )
    )

    results.append(
        _run_event_yes_no_scenario(
            "cupcake_sanity_gate",
            "event_yes_no",
            GameState(
                day=8,
                balance=40,
                rank=0,
                health=78,
                sanity=41,
                fatigue=12,
                alive=True,
                current_context_tag="event",
                current_progress_goal_candidates=("stabilize_health",),
            ),
            "buy yourself a cupcake?",
            (),
            {
                "prompt_lower": "buy yourself a cupcake?",
                "recent_lower": "",
            },
            "yes",
        )
    )

    results.append(
        _run_event_option_scenario(
            "protect_companion_branch",
            "event_option",
            shared_event_state,
            ("refuse - lucky stays with you", "tell him to prove it", "give lucky back"),
            {},
            "tell him to prove it",
        )
    )

    results.append(
        _run_event_option_scenario(
            "generic_low_resource_walkaway_branch",
            "event_option",
            GameState(
                day=9,
                balance=20,
                rank=0,
                health=44,
                sanity=21,
                fatigue=18,
                alive=True,
                current_context_tag="event",
                current_progress_goal_candidates=("survive_emergency",),
            ),
            ("Kick the door", "Walk away", "Fight them"),
            {"prompt_lower": "what do you do?"},
            "Walk away",
        )
    )

    results.append(
        _run_event_yes_no_scenario(
            "sandcastle_bribe_yes",
            "event_yes_no",
            shared_event_state,
            "",
            ("Do you take the bribe?",),
            {
                "prompt_lower": "",
                "recent_lower": "you walk around judging castles. one builder slips you $500 to vote for them. do you take the bribe?",
            },
            "yes",
        )
    )

    results.append(
        _run_event_inline_scenario(
            "sandcastle_judge_cashout",
            "event_inline",
            shared_event_state,
            "(enter/judge/sabotage/watch):",
            (
                "A sandcastle competition is underway!",
                "A judge approaches. $200 entry. Grand prize is $8,000 and the Golden Shovel trophy!",
            ),
            ("enter", "judge", "sabotage", "watch"),
            {
                "prompt_lower": "(enter/judge/sabotage/watch):",
                "recent_lower": "a sandcastle competition is underway! a judge approaches. $200 entry. grand prize is $8,000 and the golden shovel trophy!",
            },
            "judge",
        )
    )

    results.append(
        _run_event_option_scenario(
            "car_trouble_option_branch",
            "event_option",
            GameState(
                day=11,
                balance=10,
                rank=0,
                health=72,
                sanity=58,
                fatigue=16,
                alive=True,
                current_context_tag="event",
                inventory=("Spare Tire",),
                current_progress_goal_candidates=("recover_from_car_trouble",),
            ),
            ("pull it out", "leave it", "drive to shop"),
            {"prompt_lower": "what do you do?"},
            "pull it out",
        )
    )

    results.append(
        _run_event_option_scenario(
            "gas_station_robbery_prefers_hide",
            "event_option",
            GameState(
                day=6,
                balance=66,
                rank=0,
                health=95,
                sanity=82,
                fatigue=9,
                alive=True,
                current_context_tag="event",
                current_progress_goal_candidates=("acquire_car",),
            ),
            ("comply", "hide", "hero"),
            {"prompt_lower": "what do you do?"},
            "hide",
        )
    )

    results.append(
        _run_event_inline_scenario(
            "inline_decline_suspicious_offer",
            "event_inline",
            shared_event_state,
            "",
            (),
            ("accept", "decline", "scram"),
            {"prompt_lower": "", "recent_lower": ""},
            "decline",
        )
    )

    results.append(
        _run_event_inline_scenario(
            "inline_companion_sick_choice",
            "event_inline",
            GameState(
                day=10,
                balance=80,
                rank=0,
                health=75,
                sanity=52,
                fatigue=14,
                alive=True,
                current_context_tag="raw_input",
                inventory=("Cough Drops",),
                current_progress_goal_candidates=("push_next_rank",),
            ),
            "Choose:",
            ("Your companion is sick. What do you do?",),
            ("1", "2", "3", "4"),
            {
                "prompt_lower": "choose:",
                "recent_lower": "your companion is sick. what do you do?",
            },
            "2",
        )
    )

    results.append(
        _run_event_inline_scenario(
            "inline_cheap_choice_prefers_free_when_broke",
            "event_inline",
            GameState(
                day=7,
                balance=8,
                rank=0,
                health=70,
                sanity=45,
                fatigue=10,
                alive=True,
                current_context_tag="raw_input",
                current_progress_goal_candidates=("stabilize_health",),
            ),
            "",
            (),
            ("$1", "$5", "free"),
            {"prompt_lower": "", "recent_lower": ""},
            "free",
        )
    )

    results.append(
        _run_event_inline_scenario(
            "inline_wish_prefers_health",
            "event_inline",
            GameState(
                day=13,
                balance=120,
                rank=0,
                health=52,
                sanity=50,
                fatigue=12,
                alive=True,
                current_context_tag="raw_input",
                current_progress_goal_candidates=("push_next_rank",),
            ),
            "Wish for something:",
            (),
            ("money", "health", "luck"),
            {"prompt_lower": "wish for something:", "recent_lower": ""},
            "health",
        )
    )

    results.append(
        _run_event_inline_scenario(
            "inline_pet_feed_uses_tuna",
            "event_inline",
            GameState(
                day=9,
                balance=60,
                rank=0,
                health=68,
                sanity=54,
                fatigue=10,
                alive=True,
                current_context_tag="raw_input",
                inventory=("Can of Tuna",),
                current_progress_goal_candidates=("push_next_rank",),
            ),
            "",
            (),
            ("pet", "feed", "ignore"),
            {"prompt_lower": "", "recent_lower": ""},
            "feed",
        )
    )

    bet_state = GameState(
        day=15,
        balance=600,
        rank=0,
        health=39,
        sanity=42,
        fatigue=18,
        alive=True,
        current_context_tag="blackjack_bet",
        has_car=True,
        dealer_happiness=50,
        current_progress_goal_candidates=("survive_emergency", "stabilize_health"),
    )
    results.append(
        _run_bet_scenario(
            "saveable_doctor_death_bet_reserve",
            "blackjack_bet",
            bet_state,
            {
                "cycle": 0,
                "rank": 0,
                "health": 39,
                "sanity": 42,
                "dealer_happiness": 50,
                "balance": 600,
                "fake_cash": 0,
                "min_bet": 10,
                "target": 1000,
                "floor": 0,
                "distance": 400,
                "store_budget": 0,
                "wants_store": False,
                "wants_pawn": False,
                "wants_doctor": True,
                "progression_ready": False,
                "phase": "car_ready",
                "tuner_bet_ratio": 0.17,
                "tuner_bet_ratio_safe": 0.12,
                "tuner_max_ratio": 0.26,
                "tuner_pressure_factor": 0.62,
                "tuner_surplus_push": 0.42,
                "edge_score": 1,
                "pending_marvin_active": False,
                "pending_marvin_price": 0,
                "pending_marvin_shortfall": 0,
                "stall_days": 0,
                "early_caution": False,
                "stranded_no_car": False,
                "survival_mode": True,
                "needs_car": False,
                "wants_millionaire_push": False,
                "has_extra_round_item": False,
                "urgent_doctor": True,
                "has_met_tom": True,
                "has_met_frank": False,
                "has_met_oswald": False,
                "car_progress_reserve": 0,
                "mechanic_purchase_reserve": 0,
                "known_car_repair_reserve": 0,
                "has_faulty_insurance": False,
                "wants_map_unlock": False,
            },
            _assert_max_bet(96),
        )
    )

    no_car_threshold_state = GameState(
        day=5,
        balance=220,
        rank=0,
        health=78,
        sanity=55,
        fatigue=14,
        alive=True,
        current_context_tag="blackjack_bet",
        has_car=False,
        dealer_happiness=50,
        current_progress_goal_candidates=("acquire_car", "push_next_rank"),
    )
    results.append(
        _run_bet_scenario(
            "no_car_preserves_tom_threshold",
            "blackjack_bet",
            no_car_threshold_state,
            {
                "cycle": 0,
                "rank": 0,
                "health": 78,
                "sanity": 55,
                "dealer_happiness": 50,
                "balance": 220,
                "fake_cash": 0,
                "min_bet": 10,
                "target": 1000,
                "floor": 0,
                "distance": 780,
                "store_budget": 0,
                "wants_store": False,
                "wants_pawn": False,
                "wants_doctor": False,
                "progression_ready": False,
                "phase": "car_rush",
                "tuner_bet_ratio": 0.17,
                "tuner_bet_ratio_safe": 0.12,
                "tuner_max_ratio": 0.26,
                "tuner_pressure_factor": 0.62,
                "tuner_surplus_push": 0.42,
                "edge_score": 3,
                "pending_marvin_active": False,
                "pending_marvin_price": 0,
                "pending_marvin_shortfall": 0,
                "stall_days": 0,
                "early_caution": False,
                "stranded_no_car": True,
                "survival_mode": False,
                "needs_car": True,
                "wants_millionaire_push": False,
                "has_extra_round_item": False,
                "urgent_doctor": False,
                "has_met_tom": False,
                "has_met_frank": False,
                "has_met_oswald": False,
                "car_progress_reserve": 200,
                "mechanic_purchase_reserve": 200,
                "known_car_repair_reserve": 0,
                "has_faulty_insurance": False,
                "wants_map_unlock": False,
            },
            _assert_max_bet(20),
        )
    )

    no_car_bridge_state = GameState(
        day=5,
        balance=141,
        rank=0,
        health=64,
        sanity=75,
        fatigue=0,
        alive=True,
        current_context_tag="blackjack_bet",
        has_car=False,
        dealer_happiness=50,
        current_progress_goal_candidates=("acquire_car",),
    )
    results.append(
        _run_bet_scenario(
            "no_car_bridges_tom_threshold_band",
            "blackjack_bet",
            no_car_bridge_state,
            {
                "cycle": 0,
                "rank": 0,
                "health": 64,
                "sanity": 75,
                "dealer_happiness": 50,
                "balance": 141,
                "fake_cash": 0,
                "min_bet": 5,
                "target": 1000,
                "floor": 0,
                "distance": 859,
                "store_budget": 8,
                "wants_store": False,
                "wants_pawn": False,
                "wants_doctor": False,
                "progression_ready": False,
                "phase": "car_rush",
                "tuner_bet_ratio": 0.17,
                "tuner_bet_ratio_safe": 0.12,
                "tuner_max_ratio": 0.26,
                "tuner_pressure_factor": 0.62,
                "tuner_surplus_push": 0.42,
                "edge_score": 0,
                "pending_marvin_active": False,
                "pending_marvin_price": 0,
                "pending_marvin_shortfall": 0,
                "stall_days": 0,
                "early_caution": False,
                "stranded_no_car": True,
                "survival_mode": True,
                "needs_car": True,
                "wants_millionaire_push": False,
                "has_extra_round_item": False,
                "urgent_doctor": False,
                "has_met_tom": False,
                "has_met_frank": False,
                "has_met_oswald": False,
                "car_progress_reserve": 50,
                "mechanic_purchase_reserve": 0,
                "known_car_repair_reserve": 0,
                "has_faulty_insurance": False,
                "wants_map_unlock": False,
            },
            _assert_max_bet(22),
        )
    )

    no_car_push_state = GameState(
        day=2,
        balance=50,
        rank=0,
        health=90,
        sanity=70,
        fatigue=5,
        alive=True,
        current_context_tag="blackjack_bet",
        has_car=False,
        dealer_happiness=50,
        current_progress_goal_candidates=("acquire_car",),
    )
    results.append(
        _run_bet_scenario(
            "no_car_low_bankroll_pushes_for_car",
            "blackjack_bet",
            no_car_push_state,
            {
                "cycle": 0,
                "rank": 0,
                "health": 90,
                "sanity": 70,
                "dealer_happiness": 50,
                "balance": 50,
                "fake_cash": 0,
                "min_bet": 10,
                "target": 1000,
                "floor": 0,
                "distance": 950,
                "store_budget": 0,
                "wants_store": False,
                "wants_pawn": False,
                "wants_doctor": False,
                "progression_ready": False,
                "phase": "car_rush",
                "tuner_bet_ratio": 0.17,
                "tuner_bet_ratio_safe": 0.12,
                "tuner_max_ratio": 0.26,
                "tuner_pressure_factor": 0.62,
                "tuner_surplus_push": 0.42,
                "edge_score": 3,
                "pending_marvin_active": False,
                "pending_marvin_price": 0,
                "pending_marvin_shortfall": 0,
                "stall_days": 0,
                "early_caution": False,
                "stranded_no_car": True,
                "survival_mode": False,
                "needs_car": True,
                "wants_millionaire_push": False,
                "has_extra_round_item": False,
                "urgent_doctor": False,
                "has_met_tom": False,
                "has_met_frank": False,
                "has_met_oswald": False,
                "car_progress_reserve": 0,
                "mechanic_purchase_reserve": 0,
                "known_car_repair_reserve": 0,
                "has_faulty_insurance": False,
                "wants_map_unlock": False,
            },
            _assert_min_bet(14),
        )
    )

    pre_tom_breakout_state = GameState(
        day=5,
        balance=174,
        rank=0,
        health=88,
        sanity=95,
        fatigue=0,
        alive=True,
        current_context_tag="blackjack_bet",
        has_car=False,
        dealer_happiness=50,
        current_progress_goal_candidates=("acquire_car",),
    )
    results.append(
        _run_bet_scenario(
            "pre_tom_doctor_window_preserves_cash",
            "blackjack_bet",
            pre_tom_breakout_state,
            {
                "cycle": 0,
                "rank": 0,
                "health": 88,
                "sanity": 95,
                "dealer_happiness": 50,
                "balance": 174,
                "fake_cash": 0,
                "min_bet": 5,
                "target": 1000,
                "floor": 0,
                "distance": 826,
                "store_budget": 0,
                "wants_store": False,
                "wants_pawn": False,
                "wants_doctor": True,
                "progression_ready": False,
                "phase": "car_rush",
                "tuner_bet_ratio": 0.17,
                "tuner_bet_ratio_safe": 0.12,
                "tuner_max_ratio": 0.26,
                "tuner_pressure_factor": 0.62,
                "tuner_surplus_push": 0.42,
                "edge_score": 0,
                "pending_marvin_active": False,
                "pending_marvin_price": 0,
                "pending_marvin_shortfall": 0,
                "stall_days": 0,
                "early_caution": True,
                "stranded_no_car": False,
                "survival_mode": True,
                "needs_car": True,
                "wants_millionaire_push": False,
                "has_extra_round_item": False,
                "urgent_doctor": True,
                "has_met_tom": False,
                "has_met_frank": False,
                "has_met_oswald": False,
                "car_progress_reserve": 50,
                "mechanic_purchase_reserve": 0,
                "known_car_repair_reserve": 0,
                "has_faulty_insurance": False,
                "wants_map_unlock": False,
            },
            _assert_max_bet(31),
        )
    )

    mechanic_threshold_state = GameState(
        day=9,
        balance=160,
        rank=0,
        health=72,
        sanity=52,
        fatigue=10,
        alive=True,
        current_context_tag="blackjack_bet",
        has_car=False,
        dealer_happiness=50,
        current_progress_goal_candidates=("acquire_car",),
    )
    results.append(
        _run_bet_scenario(
            "first_mechanic_threshold_pushes_for_one_hand_cross",
            "blackjack_bet",
            mechanic_threshold_state,
            {
                "cycle": 0,
                "rank": 0,
                "health": 72,
                "sanity": 52,
                "dealer_happiness": 50,
                "balance": 160,
                "fake_cash": 0,
                "min_bet": 5,
                "target": 1000,
                "floor": 0,
                "distance": 840,
                "store_budget": 0,
                "wants_store": False,
                "wants_pawn": False,
                "wants_doctor": False,
                "progression_ready": False,
                "phase": "car_rush",
                "tuner_bet_ratio": 0.17,
                "tuner_bet_ratio_safe": 0.12,
                "tuner_max_ratio": 0.26,
                "tuner_pressure_factor": 0.62,
                "tuner_surplus_push": 0.42,
                "edge_score": 0,
                "pending_marvin_active": False,
                "pending_marvin_price": 0,
                "pending_marvin_shortfall": 0,
                "stall_days": 0,
                "early_caution": False,
                "stranded_no_car": False,
                "survival_mode": False,
                "needs_car": True,
                "wants_millionaire_push": False,
                "has_extra_round_item": False,
                "urgent_doctor": False,
                "has_met_tom": False,
                "has_met_frank": False,
                "has_met_oswald": False,
                "car_progress_reserve": 50,
                "mechanic_purchase_reserve": 0,
                "known_car_repair_reserve": 0,
                "has_faulty_insurance": False,
                "wants_map_unlock": False,
            },
            _assert_min_bet(40),
        )
    )

    results.append(
        _run_quicktest_mechanic_offer_scenario(
            "tom_offer_accepted_at_threshold",
            "mechanic_offer",
            FakeScenarioPlayer(
                day=5,
                balance=200,
                rank=0,
                health=78,
                sanity=55,
                fatigue=14,
            ),
            cost=150,
            recent="Tom pulls a big red wrench out of his pocket. Yep, this thing's busted alright!",
            expected_answer="yes",
        )
    )

    blend_state = GameState(
        day=28,
        balance=4000,
        rank=1,
        health=85,
        sanity=72,
        fatigue=16,
        alive=True,
        current_context_tag="blackjack_bet",
        has_car=True,
        fraudulent_cash=2000,
        dealer_happiness=88,
        current_progress_goal_candidates=("blend_fraudulent_cash_safely", "push_next_rank"),
    )
    results.append(
        _run_bet_scenario(
            "fraudulent_cash_blend_case",
            "blackjack_bet",
            blend_state,
            {
                "cycle": 0,
                "rank": 1,
                "health": 85,
                "sanity": 72,
                "dealer_happiness": 88,
                "balance": 4000,
                "fake_cash": 2000,
                "min_bet": 25,
                "target": 10000,
                "floor": 1000,
                "distance": 6000,
                "store_budget": 0,
                "wants_store": False,
                "wants_pawn": False,
                "wants_doctor": False,
                "progression_ready": True,
                "phase": "car_ready",
                "tuner_bet_ratio": 0.24,
                "tuner_bet_ratio_safe": 0.16,
                "tuner_max_ratio": 0.36,
                "tuner_pressure_factor": 0.72,
                "tuner_surplus_push": 0.54,
                "edge_score": 6,
                "pending_marvin_active": False,
                "pending_marvin_price": 0,
                "pending_marvin_shortfall": 0,
                "stall_days": 0,
                "early_caution": False,
                "stranded_no_car": False,
                "survival_mode": False,
                "needs_car": False,
                "wants_millionaire_push": False,
                "has_extra_round_item": True,
                "urgent_doctor": False,
                "has_met_tom": True,
                "has_met_frank": True,
                "has_met_oswald": False,
                "car_progress_reserve": 0,
                "mechanic_purchase_reserve": 0,
                "known_car_repair_reserve": 0,
                "has_faulty_insurance": False,
                "wants_map_unlock": False,
            },
            _assert_balance_blend(4000),
        )
    )

    marvin_hold_state = GameState(
        day=30,
        balance=12000,
        rank=1,
        health=90,
        sanity=74,
        fatigue=14,
        alive=True,
        current_context_tag="blackjack_bet",
        has_car=True,
        has_worn_map=True,
        has_marvin_access=True,
        dealer_happiness=82,
        current_progress_goal_candidates=("exploit_marvin", "push_next_rank"),
    )
    results.append(
        _run_bet_scenario(
            "marvin_preserve_cash_window",
            "blackjack_bet",
            marvin_hold_state,
            {
                "cycle": 0,
                "rank": 1,
                "health": 90,
                "sanity": 74,
                "dealer_happiness": 82,
                "balance": 12000,
                "fake_cash": 0,
                "min_bet": 50,
                "target": 10000,
                "floor": 10000,
                "distance": 0,
                "store_budget": 0,
                "wants_store": False,
                "wants_pawn": False,
                "wants_doctor": False,
                "progression_ready": True,
                "phase": "car_ready",
                "tuner_bet_ratio": 0.24,
                "tuner_bet_ratio_safe": 0.16,
                "tuner_max_ratio": 0.36,
                "tuner_pressure_factor": 0.72,
                "tuner_surplus_push": 0.54,
                "edge_score": 5,
                "pending_marvin_active": True,
                "pending_marvin_price": 9000,
                "pending_marvin_shortfall": 0,
                "stall_days": 0,
                "early_caution": False,
                "stranded_no_car": False,
                "survival_mode": False,
                "needs_car": False,
                "wants_millionaire_push": False,
                "has_extra_round_item": False,
                "urgent_doctor": False,
                "has_met_tom": True,
                "has_met_frank": True,
                "has_met_oswald": False,
                "car_progress_reserve": 0,
                "mechanic_purchase_reserve": 0,
                "known_car_repair_reserve": 0,
                "has_faulty_insurance": False,
                "wants_map_unlock": False,
            },
            _assert_max_bet(1200),
        )
    )

    marvin_purchase_push_state = GameState(
        day=31,
        balance=9200,
        rank=1,
        health=92,
        sanity=76,
        fatigue=10,
        alive=True,
        current_context_tag="blackjack_bet",
        has_car=True,
        has_worn_map=True,
        has_marvin_access=True,
        dealer_happiness=84,
        current_progress_goal_candidates=("push_next_rank", "exploit_marvin"),
    )
    results.append(
        _run_bet_scenario(
            "marvin_purchase_push_window_bets_for_margin",
            "blackjack_bet",
            marvin_purchase_push_state,
            {
                "cycle": 0,
                "rank": 1,
                "health": 92,
                "sanity": 76,
                "dealer_happiness": 84,
                "balance": 9200,
                "fake_cash": 0,
                "min_bet": 50,
                "target": 10000,
                "floor": 1000,
                "distance": 800,
                "store_budget": 0,
                "wants_store": False,
                "wants_pawn": False,
                "wants_doctor": False,
                "progression_ready": True,
                "phase": "rank_two_rush",
                "tuner_bet_ratio": 0.24,
                "tuner_bet_ratio_safe": 0.16,
                "tuner_max_ratio": 0.36,
                "tuner_pressure_factor": 0.72,
                "tuner_surplus_push": 0.54,
                "edge_score": 5,
                "pending_marvin_active": True,
                "pending_marvin_price": 8000,
                "pending_marvin_shortfall": 0,
                "purchase_push_active": True,
                "purchase_push_kind": "marvin",
                "purchase_push_price": 8000,
                "purchase_push_shortfall": 900,
                "purchase_push_priority": 88,
                "stall_days": 4,
                "early_caution": False,
                "stranded_no_car": False,
                "survival_mode": False,
                "needs_car": False,
                "wants_millionaire_push": False,
                "has_extra_round_item": False,
                "urgent_doctor": False,
                "has_met_tom": True,
                "has_met_frank": True,
                "has_met_oswald": False,
                "car_progress_reserve": 0,
                "mechanic_purchase_reserve": 0,
                "known_car_repair_reserve": 0,
                "has_faulty_insurance": False,
                "wants_map_unlock": False,
            },
            _assert_min_bet(1600),
        )
    )

    midgame_growth_state = GameState(
        day=27,
        balance=2000,
        rank=1,
        health=86,
        sanity=69,
        fatigue=12,
        alive=True,
        current_context_tag="blackjack_bet",
        has_car=True,
        has_worn_map=True,
        has_marvin_access=True,
        dealer_happiness=78,
        current_progress_goal_candidates=("push_next_rank", "exploit_marvin"),
    )
    results.append(
        _run_bet_scenario(
            "post_car_midgame_growth_window_pushes_harder",
            "blackjack_bet",
            midgame_growth_state,
            {
                "cycle": 0,
                "rank": 1,
                "health": 86,
                "sanity": 69,
                "dealer_happiness": 78,
                "balance": 2000,
                "fake_cash": 0,
                "min_bet": 25,
                "target": 10000,
                "floor": 1000,
                "distance": 8000,
                "store_budget": 0,
                "wants_store": False,
                "wants_pawn": False,
                "wants_doctor": False,
                "progression_ready": True,
                "phase": "car_ready",
                "tuner_bet_ratio": 0.24,
                "tuner_bet_ratio_safe": 0.16,
                "tuner_max_ratio": 0.36,
                "tuner_pressure_factor": 0.72,
                "tuner_surplus_push": 0.54,
                "edge_score": 4,
                "pending_marvin_active": False,
                "pending_marvin_price": 0,
                "pending_marvin_shortfall": 0,
                "stall_days": 3,
                "early_caution": False,
                "stranded_no_car": False,
                "survival_mode": False,
                "needs_car": False,
                "wants_millionaire_push": False,
                "has_extra_round_item": False,
                "urgent_doctor": False,
                "has_met_tom": True,
                "has_met_frank": True,
                "has_met_oswald": False,
                "car_progress_reserve": 0,
                "mechanic_purchase_reserve": 0,
                "known_car_repair_reserve": 0,
                "has_faulty_insurance": False,
                "wants_map_unlock": False,
            },
            _assert_min_bet(540),
        )
    )

    near_marvin_growth_state = GameState(
        day=34,
        balance=6200,
        rank=1,
        health=88,
        sanity=72,
        fatigue=10,
        alive=True,
        current_context_tag="blackjack_bet",
        has_car=True,
        has_worn_map=True,
        has_marvin_access=True,
        dealer_happiness=80,
        current_progress_goal_candidates=("push_next_rank", "exploit_marvin"),
    )
    results.append(
        _run_bet_scenario(
            "near_marvin_shortfall_growth_window_stays_aggressive",
            "blackjack_bet",
            near_marvin_growth_state,
            {
                "cycle": 0,
                "rank": 1,
                "health": 88,
                "sanity": 72,
                "dealer_happiness": 80,
                "balance": 6200,
                "fake_cash": 0,
                "min_bet": 25,
                "target": 10000,
                "floor": 1000,
                "distance": 3800,
                "store_budget": 0,
                "wants_store": False,
                "wants_pawn": False,
                "wants_doctor": False,
                "progression_ready": True,
                "phase": "rank_two_rush",
                "tuner_bet_ratio": 0.24,
                "tuner_bet_ratio_safe": 0.16,
                "tuner_max_ratio": 0.36,
                "tuner_pressure_factor": 0.72,
                "tuner_surplus_push": 0.54,
                "edge_score": 4,
                "pending_marvin_active": True,
                "pending_marvin_price": 8000,
                "pending_marvin_shortfall": 1800,
                "stall_days": 5,
                "early_caution": False,
                "stranded_no_car": False,
                "survival_mode": False,
                "needs_car": False,
                "wants_millionaire_push": False,
                "has_extra_round_item": False,
                "urgent_doctor": False,
                "has_met_tom": True,
                "has_met_frank": True,
                "has_met_oswald": False,
                "car_progress_reserve": 0,
                "mechanic_purchase_reserve": 0,
                "known_car_repair_reserve": 0,
                "has_faulty_insurance": False,
                "wants_map_unlock": False,
            },
            _assert_min_bet(1100),
        )
    )

    rank_one_core_unlock_state = GameState(
        day=29,
        balance=5200,
        rank=1,
        health=86,
        sanity=70,
        fatigue=8,
        alive=True,
        current_context_tag="blackjack_bet",
        has_car=True,
        has_worn_map=True,
        has_marvin_access=True,
        dealer_happiness=78,
        current_progress_goal_candidates=("push_next_rank", "exploit_marvin"),
    )
    results.append(
        _run_bet_scenario(
            "rank_one_core_marvin_unlock_bets_harder",
            "blackjack_bet",
            rank_one_core_unlock_state,
            {
                "cycle": 0,
                "rank": 1,
                "health": 86,
                "sanity": 70,
                "dealer_happiness": 78,
                "balance": 5200,
                "fake_cash": 0,
                "min_bet": 25,
                "target": 10000,
                "floor": 1000,
                "distance": 4800,
                "store_budget": 0,
                "wants_store": False,
                "wants_pawn": False,
                "wants_doctor": False,
                "progression_ready": True,
                "phase": "rank_two_rush",
                "tuner_bet_ratio": 0.24,
                "tuner_bet_ratio_safe": 0.16,
                "tuner_max_ratio": 0.36,
                "tuner_pressure_factor": 0.72,
                "tuner_surplus_push": 0.54,
                "edge_score": 4,
                "pending_marvin_active": True,
                "pending_marvin_price": 11000,
                "pending_marvin_shortfall": 5800,
                "stall_days": 4,
                "early_caution": False,
                "stranded_no_car": False,
                "survival_mode": False,
                "needs_car": False,
                "wants_millionaire_push": False,
                "has_extra_round_item": False,
                "urgent_doctor": False,
                "has_met_tom": True,
                "has_met_frank": True,
                "has_met_oswald": False,
                "car_progress_reserve": 0,
                "mechanic_purchase_reserve": 0,
                "known_car_repair_reserve": 0,
                "has_faulty_insurance": True,
                "wants_map_unlock": False,
            },
            _assert_min_bet(1450),
        )
    )

    rank_two_marvin_upgrade_state = GameState(
        day=68,
        balance=11500,
        rank=2,
        health=84,
        sanity=68,
        fatigue=12,
        alive=True,
        current_context_tag="blackjack_bet",
        has_car=True,
        has_worn_map=True,
        has_marvin_access=True,
        dealer_happiness=82,
        current_progress_goal_candidates=("push_next_rank", "exploit_marvin"),
    )
    results.append(
        _run_bet_scenario(
            "rank_two_marvin_upgrade_window_uses_surplus",
            "blackjack_bet",
            rank_two_marvin_upgrade_state,
            {
                "cycle": 0,
                "rank": 2,
                "health": 84,
                "sanity": 68,
                "dealer_happiness": 82,
                "balance": 11500,
                "fake_cash": 0,
                "min_bet": 50,
                "target": 100000,
                "floor": 10000,
                "distance": 88500,
                "store_budget": 0,
                "wants_store": False,
                "wants_pawn": False,
                "wants_doctor": False,
                "progression_ready": True,
                "phase": "million_rush",
                "tuner_bet_ratio": 0.28,
                "tuner_bet_ratio_safe": 0.18,
                "tuner_max_ratio": 0.40,
                "tuner_pressure_factor": 0.78,
                "tuner_surplus_push": 0.56,
                "edge_score": 5,
                "pending_marvin_active": True,
                "pending_marvin_price": 19000,
                "pending_marvin_shortfall": 7500,
                "stall_days": 6,
                "early_caution": False,
                "stranded_no_car": False,
                "survival_mode": False,
                "needs_car": False,
                "wants_millionaire_push": True,
                "has_extra_round_item": False,
                "urgent_doctor": False,
                "has_met_tom": True,
                "has_met_frank": True,
                "has_met_oswald": False,
                "car_progress_reserve": 0,
                "mechanic_purchase_reserve": 0,
                "known_car_repair_reserve": 0,
                "has_faulty_insurance": False,
                "wants_map_unlock": False,
            },
            _assert_min_bet(1400),
        )
    )

    results.append(
        _run_quicktest_loan_borrow_scenario(
            "marvin_unlock_loan_prefers_large_borrow",
            "quicktest_loan_borrow",
            FakeScenarioPlayer(
                day=30,
                balance=6200,
                rank=1,
                health=84,
                sanity=66,
                fatigue=8,
                inventory=("Car", "Map", "Faulty Insurance"),
                met=("Vinnie",),
            ),
            ((1, "Borrow $500"), (2, "Borrow $1,000"), (3, "Borrow $2,500"), (4, "Borrow $5,000"), (5, "Never mind")),
            "Borrow $5,000",
        )
    )

    catalog_push_bet_state = GameState(
        day=44,
        balance=7200,
        rank=1,
        health=87,
        sanity=74,
        fatigue=8,
        alive=True,
        current_context_tag="blackjack_bet",
        has_car=True,
        has_worn_map=True,
        has_marvin_access=True,
        dealer_happiness=81,
        current_progress_goal_candidates=("push_next_rank", "exploit_marvin"),
    )
    results.append(
        _run_bet_scenario(
            "catalog_push_window_bets_for_marvin_buyout",
            "blackjack_bet",
            catalog_push_bet_state,
            {
                "cycle": 0,
                "rank": 1,
                "health": 87,
                "sanity": 74,
                "dealer_happiness": 81,
                "balance": 7200,
                "fake_cash": 0,
                "min_bet": 25,
                "target": 10000,
                "floor": 1000,
                "distance": 2800,
                "store_budget": 0,
                "wants_store": False,
                "wants_pawn": False,
                "wants_doctor": False,
                "progression_ready": True,
                "phase": "rank_two_rush",
                "tuner_bet_ratio": 0.24,
                "tuner_bet_ratio_safe": 0.16,
                "tuner_max_ratio": 0.36,
                "tuner_pressure_factor": 0.72,
                "tuner_surplus_push": 0.54,
                "edge_score": 4,
                "pending_marvin_active": False,
                "pending_marvin_price": 0,
                "pending_marvin_shortfall": 0,
                "catalog_push_active": True,
                "catalog_push_kind": "marvin",
                "catalog_push_spend": 15000,
                "catalog_push_count": 2,
                "catalog_push_priority": 94,
                "stall_days": 5,
                "early_caution": False,
                "stranded_no_car": False,
                "survival_mode": False,
                "needs_car": False,
                "wants_millionaire_push": False,
                "has_extra_round_item": False,
                "urgent_doctor": False,
                "has_met_tom": True,
                "has_met_frank": True,
                "has_met_oswald": False,
                "car_progress_reserve": 0,
                "mechanic_purchase_reserve": 0,
                "known_car_repair_reserve": 0,
                "has_faulty_insurance": False,
                "wants_map_unlock": False,
            },
            _assert_min_bet(2200),
        )
    )

    # ===== GIFT WRAP SCENARIOS =====

    # Gift wrap: should accept when dealer happiness is low and not in emergency
    results.append(
        _run_event_yes_no_scenario(
            "gift_wrap_accepted_when_dealer_sad",
            "event_yes_no",
            GameState(
                day=10,
                balance=350,
                rank=1,
                health=72,
                sanity=55,
                fatigue=20,
                alive=True,
                current_context_tag="yes_no_prompt",
                has_car=True,
                dealer_happiness=55,
                current_progress_goal_candidates=("push_next_rank",),
            ),
            "Gift wrap?",
            (),
            {
                "prompt_lower": "gift wrap?",
                "recent_lower": "would you like to gift wrap an item for the dealer?",
            },
            "yes",
        )
    )

    # Gift wrap: should decline when dealer happiness is already high
    results.append(
        _run_event_yes_no_scenario(
            "gift_wrap_declined_when_dealer_happy",
            "event_yes_no",
            GameState(
                day=10,
                balance=350,
                rank=1,
                health=72,
                sanity=55,
                fatigue=20,
                alive=True,
                current_context_tag="yes_no_prompt",
                has_car=True,
                dealer_happiness=92,
                current_progress_goal_candidates=("push_next_rank",),
            ),
            "Gift wrap?",
            (),
            {
                "prompt_lower": "gift wrap?",
                "recent_lower": "would you like to gift wrap an item for the dealer?",
            },
            "no",
        )
    )

    # Gift wrap: should decline when in emergency (survive_emergency goal)
    results.append(
        _run_event_yes_no_scenario(
            "gift_wrap_declined_in_emergency",
            "event_yes_no",
            GameState(
                day=10,
                balance=350,
                rank=0,
                health=32,
                sanity=18,
                fatigue=20,
                alive=True,
                current_context_tag="yes_no_prompt",
                has_car=True,
                dealer_happiness=55,
                current_progress_goal_candidates=("survive_emergency",),
            ),
            "Gift wrap?",
            (),
            {
                "prompt_lower": "gift wrap?",
                "recent_lower": "would you like to gift wrap an item for the dealer?",
            },
            "no",
        )
    )

    results.append(
        _run_quicktest_destination_scenario(
            "gift_loop_store_run_pushes_convenience_store",
            "route_interrupt",
            FakeScenarioPlayer(
                day=17,
                balance=260,
                rank=1,
                health=74,
                sanity=58,
                inventory=("Car",),
                met=("Tom",),
                store_inventory=(("Fancy Pen", 25),),
                dealer_happiness=89,
                gift_system_unlocked=True,
                has_wrapped_gift=False,
            ),
            ("Convenience Store", "Stay Home"),
            "Convenience Store",
        )
    )

    results.append(
        _run_quicktest_store_menu_scenario(
            "gift_loop_prefers_giftworthy_item",
            "purchase_select",
            FakeScenarioPlayer(
                day=17,
                balance=260,
                rank=1,
                health=74,
                sanity=58,
                inventory=("Car",),
                store_inventory=(("Fancy Pen", 25), ("Duct Tape", 12)),
                dealer_happiness=87,
                gift_system_unlocked=True,
                has_wrapped_gift=False,
            ),
            (
                (1, "Fancy Pen - $25"),
                (2, "Duct Tape - $12"),
                (3, "I'm not buying anything"),
            ),
            "Fancy Pen - $25",
        )
    )

    # ===== MILLIONAIRE AFTERNOON SCENARIOS =====

    # Millionaire afternoon: should choose chosen mechanic ending
    results.append(
        _run_event_option_scenario(
            "millionaire_afternoon_prefers_mechanic_ending",
            "event_option",
            GameState(
                day=45,
                balance=1_200_000,
                rank=3,
                health=85,
                sanity=72,
                fatigue=10,
                alive=True,
                current_context_tag="option_prompt",
                has_car=True,
                chosen_mechanic="Tom",
                current_progress_goal_candidates=("convert_millionaire_to_ending",),
                opportunity_flags={"can_convert_millionaire_to_ending": True},
            ),
            (
                "Visit Tom's Trusty Trucks and Tires",
                "Drive to the Airport",
                "Continue gambling",
            ),
            {
                "prompt_lower": "choose a number",
                "recent_lower": "you wake up as a millionaire. what do you do?",
            },
            "Visit Tom's Trusty Trucks and Tires",
        )
    )

    # Millionaire afternoon: airport when no mechanic chosen
    results.append(
        _run_event_option_scenario(
            "millionaire_afternoon_airport_when_no_mechanic",
            "event_option",
            GameState(
                day=45,
                balance=1_200_000,
                rank=3,
                health=85,
                sanity=72,
                fatigue=10,
                alive=True,
                current_context_tag="option_prompt",
                has_car=True,
                chosen_mechanic=None,
                current_progress_goal_candidates=("convert_millionaire_to_ending",),
                opportunity_flags={"can_convert_millionaire_to_ending": True},
            ),
            (
                "Drive to the Airport",
                "Continue gambling",
            ),
            {
                "prompt_lower": "choose a number",
                "recent_lower": "you wake up as a millionaire. what do you do? drive to the airport",
            },
            "Drive to the Airport",
        )
    )

    # ===== WORKBENCH CONFIRM SCENARIOS =====

    # Workbench craft confirm: should say yes when combining items
    results.append(
        _run_event_yes_no_scenario(
            "workbench_craft_confirm_says_yes",
            "event_yes_no",
            GameState(
                day=12,
                balance=600,
                rank=1,
                health=75,
                sanity=60,
                fatigue=15,
                alive=True,
                current_context_tag="yes_no_prompt",
                has_car=True,
                current_progress_goal_candidates=("push_next_rank",),
            ),
            "(yes/no): ",
            (
                "Car Workbench",
                "Combine First Aid Kit and Cough Drops into a Home Remedy?",
            ),
            {
                "prompt_lower": "(yes/no):",
                "recent_lower": "car workbench combine first aid kit and cough drops into a home remedy?",
            },
            "yes",
        )
    )

    # ===== COMPANION RUNAWAY PREVENTION SCENARIOS =====

    # Companion hungry with runaway risk: should buy food (option 3) even with limited balance
    results.append(
        _run_event_inline_scenario(
            "companion_hungry_runaway_risk_buys_food",
            "event_inline",
            GameState(
                day=14,
                balance=35,
                rank=0,
                health=68,
                sanity=45,
                fatigue=22,
                alive=True,
                current_context_tag="inline_choice_prompt",
                has_car=True,
                companion_count=2,
                companion_runaway_risk_count=1,
                companion_low_happiness_count=2,
                current_progress_goal_candidates=("preserve_companion_roster",),
            ),
            "Choose:",
            ("morning. your companions are hungry.",),
            ("1", "2", "3", "4"),
            {
                "prompt_lower": "choose:",
                "recent_lower": "morning. your companions are hungry.",
            },
            "3",
        )
    )

    results.append(
        _run_quicktest_companion_menu_scenario(
            "companion_menu_groups_for_bond_and_runaway_pressure",
            "companion_menu",
            FakeScenarioPlayer(
                day=19,
                balance=180,
                rank=1,
                health=80,
                sanity=70,
                inventory=("Car",),
                companions={
                    "Lucky": {"type": "Three-Legged Dog", "happiness": 74, "days_owned": 6, "fed_today": False, "bonded": False},
                    "Mr. Pecks": {"type": "Crow", "happiness": 14, "days_owned": 8, "fed_today": False, "bonded": False},
                },
            ),
            (
                (1, "Lucky (Three-Legged Dog) ~"),
                (2, "Mr. Pecks (Crow) ..."),
                (3, "Spend time with all of them"),
                (4, "Skip and head out"),
            ),
            "Spend time with all of them",
        )
    )

    results.append(
        _run_quicktest_destination_scenario(
            "mechanic_route_prefers_dream_leader",
            "route_interrupt",
            FakeScenarioPlayer(
                day=24,
                balance=2200,
                rank=1,
                health=82,
                sanity=68,
                inventory=("Car",),
                met=("Tom", "Frank", "Oswald"),
                mechanic_visits=1,
                tom_dreams=1,
                frank_dreams=2,
                oswald_dreams=0,
            ),
            (
                "Trusty Tom's Trucks and Tires",
                "Filthy Frank's Flawless Fixtures",
                "Oswald's Optimal Outoparts",
                "Stay Home",
            ),
            "Filthy Frank's Flawless Fixtures",
        )
    )

    results.append(
        _run_quicktest_destination_scenario(
            "rich_marvin_conversion_interrupt_beats_store_and_pawn",
            "route_interrupt",
            FakeScenarioPlayer(
                day=64,
                balance=14200,
                rank=2,
                health=86,
                sanity=72,
                inventory=("Car", "Worn Map"),
                met=("Tom", "Frank", "Vinnie"),
            ),
            (
                "Marvin's Mystical Merchandise",
                "Convenience Store",
                "Grimy Gus's Pawn Emporium",
                "Stay Home",
            ),
            "Marvin's Mystical Merchandise",
        )
    )

    results.append(
        _run_quicktest_destination_scenario(
            "rank_one_marvin_conversion_interrupt_beats_store",
            "route_interrupt",
            FakeScenarioPlayer(
                day=26,
                balance=2400,
                rank=1,
                health=84,
                sanity=66,
                inventory=("Car", "Worn Map"),
                met=("Tom",),
            ),
            (
                "Marvin's Mystical Merchandise",
                "Convenience Store",
                "Stay Home",
            ),
            "Marvin's Mystical Merchandise",
        )
    )

    results.append(
        _run_quicktest_destination_scenario(
            "witch_powered_marvin_followup_beats_store",
            "route_interrupt",
            FakeScenarioPlayer(
                day=58,
                balance=11800,
                rank=2,
                health=80,
                sanity=64,
                inventory=("Car", "Worn Map"),
                met=("Tom", "Witch"),
                flasks=("No Bust", "Dealer's Whispers"),
            ),
            (
                "Marvin's Mystical Merchandise",
                "Witch Doctor's Tower",
                "Convenience Store",
                "Stay Home",
            ),
            "Marvin's Mystical Merchandise",
        )
    )

    dream_reserve_state = GameState(
        day=28,
        balance=10200,
        rank=1,
        health=84,
        sanity=66,
        fatigue=8,
        alive=True,
        current_context_tag="blackjack_bet",
        has_car=True,
        dealer_happiness=70,
        chosen_mechanic="Frank",
        current_progress_goal_candidates=("advance_mechanic_arc", "push_next_rank"),
    )
    results.append(
        _run_bet_scenario(
            "mechanic_dream_reserve_preserves_threshold",
            "blackjack_bet",
            dream_reserve_state,
            {
                "cycle": 0,
                "rank": 1,
                "health": 84,
                "sanity": 66,
                "dealer_happiness": 70,
                "balance": 10200,
                "fake_cash": 0,
                "min_bet": 25,
                "target": 10000,
                "floor": 1000,
                "distance": 0,
                "store_budget": 0,
                "wants_store": False,
                "wants_pawn": False,
                "wants_doctor": False,
                "progression_ready": True,
                "phase": "car_ready",
                "tuner_bet_ratio": 0.22,
                "tuner_bet_ratio_safe": 0.15,
                "tuner_max_ratio": 0.34,
                "tuner_pressure_factor": 0.72,
                "tuner_surplus_push": 0.48,
                "edge_score": 4,
                "pending_marvin_active": False,
                "pending_marvin_price": 0,
                "pending_marvin_shortfall": 0,
                "stall_days": 0,
                "early_caution": False,
                "stranded_no_car": False,
                "survival_mode": False,
                "needs_car": False,
                "wants_millionaire_push": False,
                "has_extra_round_item": False,
                "urgent_doctor": False,
                "has_met_tom": True,
                "has_met_frank": True,
                "has_met_oswald": False,
                "car_progress_reserve": 0,
                "mechanic_purchase_reserve": 0,
                "mechanic_dream_reserve": 10000,
                "known_car_repair_reserve": 0,
                "has_faulty_insurance": False,
                "wants_map_unlock": False,
            },
            _assert_max_bet(200),
        )
    )

    return results