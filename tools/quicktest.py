"""Fast automated playtest with structured per-day reporting."""

import atexit
import itertools
import json
import os
import random
import re
import sys
import traceback
import types
import warnings
from collections import Counter, defaultdict
from unittest.mock import patch

# Patch msvcrt before anything else imports it.
# msvcrt is Windows-only; install a stub for other platforms.
if "msvcrt" not in sys.modules:
    _stub = types.ModuleType("msvcrt")
    _stub.kbhit = lambda: False  # type: ignore[attr-defined]
    _stub.getch = lambda: b""  # type: ignore[attr-defined]
    sys.modules["msvcrt"] = _stub

import msvcrt  # noqa: E402  (now always available)

msvcrt.kbhit = lambda: False
msvcrt.getch = lambda: b""

import time

time.sleep = lambda _seconds: None

# Neuter colorama so it does not hijack stdout.
import colorama

colorama.init = lambda **_kw: None
colorama.deinit = lambda: None

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

warning_messages = []


def _capture_warning(message, category, filename, lineno, file=None, line=None):
    formatted = warnings.formatwarning(message, category, filename, lineno, line).strip()
    if formatted not in warning_messages:
        warning_messages.append(formatted)


warnings.simplefilter("always")
warnings.showwarning = _capture_warning

import blackjack as bj
import lists as _lists_mod
import story
import typer as _typer
from tools.autoplay import DecisionOption, DecisionRequest, DecisionTrace, build_game_state_snapshot, choose_route_option, choose_strategic_goal
from tools.autoplay.config import (
    GIFT_WRAP_HAPPINESS_THRESHOLD,
    GIFT_WRAP_MIN_BALANCE,
    MARVIN_ITEM_ORDER,
    STORE_CAR_SURVIVAL_PRIORITIES,
    STORE_MUST_HAVE_ITEMS,
    get_crafting_recipe_priority,
    get_rank_tuner,
    get_marvin_base_priority,
    get_marvin_price_estimate,
    get_store_base_priority,
    get_upgrade_base_priority,
    get_upgrade_price_estimate,
    get_witch_flask_base_priority,
    get_witch_flask_price_estimate,
)
from tools.autoplay.policies import (
    choose_blackjack_action,
    choose_blackjack_bet,
    choose_event_inline_choice,
    choose_event_option,
    choose_event_yes_no,
    choose_insurance_option,
    choose_loan_option,
    choose_medical_option,
    choose_purchase_option,
    choose_repair_option,
    choose_second_chance_option,
)

CURRENT_PLAYER = None
RECENT_TEXT = []
LAST_INPUT_FINGERPRINT = None
REPEATED_INPUT_COUNT = 0
ANSI_RE = re.compile(r"\x1b\[[0-9;]*[A-Za-z]")
MECHANIC_DECISIONS = []
EARLY_MECHANIC_DAY_LIMIT = 10
EARLY_MECHANIC_THRESHOLD = 200
FALLBACK_DECISIONS = Counter()
EVER_HAD_CAR = False
DECISION_REQUESTS = []
DECISION_TRACES = []
ITEM_PROVENANCE = defaultdict(lambda: {
    "acquired": [],
    "used": [],
    "removed": [],
    "broken": [],
    "fixed": [],
    "repairing": [],
})


def _infer_death_cause_from_recent_text():
    patterns = [
        "gunshot", "shot", "poisoning", "overdose", "drowned", "heart attack", "mauled",
        "electrocution", "explosion", "loan sharks", "wrath", "succumbed to your wounds",
        "hostage", "rabies", "pneumonia", "fentanyl", "bleeding", "wounds",
    ]
    for line in reversed(RECENT_TEXT[-40:]):
        lowered = line.lower()
        if any(pattern in lowered for pattern in patterns):
            return line.strip().rstrip(".")
    return "Unknown"


def _remember_text(*parts):
    text = " ".join(str(part) for part in parts if part is not None).strip()
    text = ANSI_RE.sub("", text)
    if not text:
        return
    for line in text.splitlines():
        cleaned = line.strip()
        if cleaned:
            RECENT_TEXT.append(cleaned)
    del RECENT_TEXT[:-200]


def _current_context_source():
    preferred_prefixes = ["location:", "storyline:", "day:", "night:", "met:"]
    for prefix in preferred_prefixes:
        for label in reversed(CURRENT_EVENTS):
            if label.startswith(prefix):
                return label
    for line in reversed(RECENT_TEXT[-20:]):
        lowered = line.lower()
        if "marvin" in lowered:
            return "text:marvin"
        if "doctor" in lowered:
            return "text:doctor"
        if "witch" in lowered:
            return "text:witch"
        if "loan" in lowered or "vinnie" in lowered:
            return "text:loan_shark"
    return "unknown"


def _record_item_provenance(player, item_name, action):
    if player is None or not item_name:
        return
    day = getattr(player, "_day", None)
    ITEM_PROVENANCE[str(item_name)][action].append({
        "day": None if day is None else int(day),
        "source": _current_context_source(),
        "cycle": CURRENT_CYCLE,
    })


def _render_item_history(entries):
    if not entries:
        return "-"
    rendered = []
    for entry in entries[:8]:
        day = "?" if entry.get("day") is None else str(entry.get("day"))
        rendered.append(f"{day}@{entry.get('source', 'unknown')}")
    return ",".join(rendered)


def _capture_type(self, *args, **kwargs):
    _remember_text(*args)


def _get_recent_menu_options(limit=40):
    options = []
    for line in RECENT_TEXT[-limit:]:
        match = re.match(r"^(\d+)\.\s+(.*)$", line)
        if match:
            options.append((int(match.group(1)), match.group(2).strip()))
    unique = []
    seen = set()
    for number, label in reversed(options):
        if number in seen:
            continue
        seen.add(number)
        unique.append((number, label))
    unique.reverse()
    return unique


def _current_game_state(player, *, menu_options=None, context_tag=None):
    normalized_menu = [label for _number, label in (menu_options or _get_recent_menu_options())]
    economy_hints = _structured_economy_hints(player)
    return build_game_state_snapshot(
        player,
        current_context_tag=context_tag or _current_context_source(),
        available_routes=normalized_menu,
        available_menu_options=normalized_menu,
        economy_hints=economy_hints,
    )


def _record_decision_trace(trace):
    if trace is not None:
        DECISION_TRACES.append(trace)


def _record_decision_request(request):
    if request is not None:
        DECISION_REQUESTS.append(request)


def _structured_options(options, *, prefix):
    normalized = []
    for index, option in enumerate(options):
        normalized.append(
            DecisionOption(
                option_id=f"{prefix}:{index}",
                label=str(option),
                value=str(option),
                metadata={"index": index},
            )
        )
    return tuple(normalized)


def _build_event_policy_request(
    player,
    *,
    request_type,
    stable_context_id,
    options,
    prompt="",
    metadata=None,
):
    snapshot = _current_game_state(player, context_tag=stable_context_id)
    request = DecisionRequest(
        request_type=request_type,
        stable_context_id=stable_context_id,
        game_state=snapshot.to_dict(),
        normalized_options=_structured_options(tuple(options), prefix=request_type),
        raw_prompt_text=prompt or "",
        raw_recent_text=tuple(RECENT_TEXT[-20:]),
        metadata={
            "cycle": CURRENT_CYCLE,
            **(metadata or {}),
        },
    )
    plan = choose_strategic_goal(snapshot)
    return request, plan


def _record_structured_trace(
    player,
    *,
    request_type,
    stable_context_id,
    chosen_action,
    reason,
    confidence,
    prompt="",
    options=(),
    metadata=None,
):
    game_state = _current_game_state(player, context_tag=stable_context_id)
    request = DecisionRequest(
        request_type=request_type,
        stable_context_id=stable_context_id,
        game_state=game_state.to_dict(),
        normalized_options=_structured_options(options, prefix=request_type),
        raw_prompt_text=prompt or "",
        raw_recent_text=tuple(RECENT_TEXT[-20:]),
        metadata={
            "cycle": CURRENT_CYCLE,
            "day": game_state.day,
            **(metadata or {}),
        },
    )
    _record_decision_request(request)
    plan = choose_strategic_goal(game_state)
    _record_decision_trace(
        DecisionTrace(
            cycle=CURRENT_CYCLE,
            day=game_state.day,
            context=stable_context_id,
            request_type=request_type,
            strategic_goal=plan.goal,
            chosen_action=str(chosen_action),
            reason=reason,
            confidence=confidence,
            options=tuple(str(option) for option in options),
            game_state_summary=request.game_state,
            metadata={
                "plan": plan.to_dict(),
                **request.metadata,
            },
        )
    )


def _record_numeric_menu_trace(
    player,
    *,
    request_type,
    stable_context_id,
    menu_options,
    chosen_number,
    reason,
    confidence=0.58,
    prompt="",
    metadata=None,
):
    game_state = _current_game_state(player, menu_options=menu_options, context_tag=stable_context_id)
    normalized_options = tuple(
        DecisionOption(
            option_id=f"{request_type}:{number}",
            label=label,
            value=number,
            metadata={"number": number},
        )
        for number, label in menu_options
    )
    request = DecisionRequest(
        request_type=request_type,
        stable_context_id=stable_context_id,
        game_state=game_state.to_dict(),
        normalized_options=normalized_options,
        raw_prompt_text=prompt or "",
        raw_recent_text=tuple(RECENT_TEXT[-20:]),
        metadata={
            "cycle": CURRENT_CYCLE,
            "day": game_state.day,
            **(metadata or {}),
        },
    )
    _record_decision_request(request)
    plan = choose_strategic_goal(game_state)
    chosen_label = next((label for number, label in menu_options if number == chosen_number), str(chosen_number))
    _record_decision_trace(
        DecisionTrace(
            cycle=CURRENT_CYCLE,
            day=game_state.day,
            context=stable_context_id,
            request_type=request_type,
            strategic_goal=plan.goal,
            chosen_action=str(chosen_number),
            reason=reason,
            confidence=confidence,
            options=tuple(label for _number, label in menu_options),
            game_state_summary=request.game_state,
            metadata={
                "plan": plan.to_dict(),
                "chosen_label": chosen_label,
                **request.metadata,
            },
        )
    )
    return chosen_number


def _choose_policy_numeric_option(
    player,
    *,
    request_type,
    stable_context_id,
    menu_options,
    option_metadata_by_number,
    prompt="",
    metadata=None,
):
    game_state = _current_game_state(player, menu_options=menu_options, context_tag=stable_context_id)
    normalized_options = tuple(
        DecisionOption(
            option_id=f"{request_type}:{number}",
            label=label,
            value=number,
            metadata={"number": number, **dict(option_metadata_by_number.get(number, {}))},
        )
        for number, label in menu_options
    )
    request = DecisionRequest(
        request_type=request_type,
        stable_context_id=stable_context_id,
        game_state=game_state.to_dict(),
        normalized_options=normalized_options,
        raw_prompt_text=prompt or "",
        raw_recent_text=tuple(RECENT_TEXT[-20:]),
        metadata={
            "cycle": CURRENT_CYCLE,
            "day": game_state.day,
            "balance": game_state.balance,
            "rank": game_state.rank,
            **(metadata or {}),
        },
    )
    _record_decision_request(request)
    plan = choose_strategic_goal(game_state)

    if request_type == "purchase_select":
        choice, trace = choose_purchase_option(request, plan)
    elif request_type == "loan_decision":
        choice, trace = choose_loan_option(request, plan)
    elif request_type in {"repair_select", "upgrade_select"}:
        choice, trace = choose_repair_option(request, plan)
    else:
        return None

    _record_decision_trace(trace)
    if choice is None or choice.value is None:
        return None
    return int(choice.value)


def _record_route_interrupt_trace(player, chosen_action, reason, strategic_goal, interrupt_kind):
    snapshot = _current_game_state(player, context_tag="route_interrupt")
    interrupt_plan = choose_strategic_goal(snapshot)
    _record_decision_trace(
        DecisionTrace(
            cycle=CURRENT_CYCLE,
            day=snapshot.day,
            context="afternoon_destination_interrupt",
            request_type="route_select",
            strategic_goal=strategic_goal,
            chosen_action=str(chosen_action),
            reason=reason,
            confidence=1.0,
            game_state_summary=snapshot.to_dict(),
            metadata={
                "interrupt": True,
                "interrupt_kind": interrupt_kind,
                "route_outcome": "interrupt",
                "candidate_goals": list(snapshot.current_progress_goal_candidates),
                "top_goal_before_interrupt": interrupt_plan.goal,
            },
        )
    )


def _extract_cash_amount(*texts):
    candidate = None
    for text in texts:
        for match in re.finditer(r"\$([0-9,]+)", text or ""):
            candidate = int(match.group(1).replace(",", ""))
        for match in re.finditer(r"\b([0-9][0-9,]*)\s*(?:bucks|dollars|cash)\b", text or "", re.IGNORECASE):
            candidate = int(match.group(1).replace(",", ""))
    return candidate


def _extract_mechanic_offer_cost(prompt, recent):
    amounts = []
    for text in (prompt or "", recent or ""):
        for match in re.finditer(r"\$([0-9,]+)", text):
            amounts.append(int(match.group(1).replace(",", "")))
        for match in re.finditer(r"\b([0-9][0-9,]*)\s*(?:bucks|dollars|cash)\b", text, re.IGNORECASE):
            amounts.append(int(match.group(1).replace(",", "")))

    if not amounts:
        return None

    recent_lower = (recent or "").lower()
    realistic_amounts = [amount for amount in amounts if amount <= 5000]
    if any(fragment in recent_lower for fragment in ["oswald", "stuart", "limousine", "optimal outoparts"]):
        if realistic_amounts:
            return realistic_amounts[-1]
    if realistic_amounts:
        return realistic_amounts[-1]
    return amounts[-1]


def _extract_inline_choices(*texts):
    for text in texts:
        if not text:
            continue
        for match in re.finditer(r"\(([^()]+/[^()]+)\)", text):
            options = [part.strip().lower() for part in match.group(1).split("/") if part.strip()]
            if options:
                return options
    return []


def _detect_mechanic_name(recent):
    recent_lower = (recent or "").lower()
    if any(fragment in recent_lower for fragment in ["oswald", "stuart", "limousine", "optimal outoparts"]):
        return "Oswald"
    if any(fragment in recent_lower for fragment in ["frank", "filthy frank", "you game", "fix this up for like"]):
        return "Frank"
    if any(fragment in recent_lower for fragment in ["tom", "trusty trucks", "busted alright", "whaddya say"]):
        return "Tom"
    return "Unknown"


def _looks_like_mechanic_intro_offer(recent, prompt=""):
    recent_lower = (recent or "").lower()
    prompt_lower = (prompt or "").lower()
    offer_phrases = [
        "whaddya say",
        "you game",
        "could ya do",
        "do you accept",
        "this thing's busted alright",
        "i can fix this up for like",
        "get you back on the road",
        "fix your limousine",
    ]
    mechanic_phrases = [
        "tom",
        "frank",
        "oswald",
        "stuart",
        "mechanic",
        "wagon",
        "engine",
        "limousine",
        "trusty trucks",
        "flawless fixtures",
        "optimal outoparts",
    ]
    combined = recent_lower + "\n" + prompt_lower
    return any(phrase in combined for phrase in offer_phrases) and any(phrase in combined for phrase in mechanic_phrases)


def _record_mechanic_decision(player, recent, cost, answer, source):
    day = getattr(player, "_day", None) if player is not None else None
    balance = player.get_balance() if player is not None else None
    MECHANIC_DECISIONS.append({
        "day": day,
        "mechanic": _detect_mechanic_name(recent),
        "cost": cost,
        "answer": answer,
        "source": source,
        "balance": balance,
    })


def _build_early_mechanic_funnel(final_state, peak_balance, peak_days):
    route_traces = [
        trace
        for trace in DECISION_TRACES
        if trace.request_type == "route_select"
        and trace.day is not None
        and int(trace.day) <= EARLY_MECHANIC_DAY_LIMIT
    ]
    early_mechanic_decisions = [
        decision
        for decision in MECHANIC_DECISIONS
        if isinstance(decision.get("day"), int) and int(decision["day"]) <= EARLY_MECHANIC_DAY_LIMIT
    ]

    affordable_offer_count = 0
    accept_count = 0
    first_offer_day = None
    first_accept_day = None
    for decision in early_mechanic_decisions:
        day = int(decision["day"])
        balance = decision.get("balance")
        cost = decision.get("cost")
        if first_offer_day is None or day < first_offer_day:
            first_offer_day = day
        if isinstance(balance, int) and isinstance(cost, int) and balance >= cost:
            affordable_offer_count += 1
        if decision.get("answer") == "yes":
            accept_count += 1
            if first_accept_day is None or day < first_accept_day:
                first_accept_day = day

    medical_interrupt_count = sum(
        1
        for trace in route_traces
        if str(trace.metadata.get("interrupt_kind", "")) in {"urgent_doctor", "recovery_day"}
    )
    route_outcome_counts = Counter(str(trace.metadata.get("route_outcome", "unknown")) for trace in route_traces)

    return {
        "day_limit": EARLY_MECHANIC_DAY_LIMIT,
        "threshold": EARLY_MECHANIC_THRESHOLD,
        "ending_day": min(int(final_state["day"]), EARLY_MECHANIC_DAY_LIMIT),
        "peak_balance": int(peak_balance),
        "peak_days": list(peak_days),
        "balance_end": int(final_state["balance"]),
        "reached_threshold": int(peak_balance) >= EARLY_MECHANIC_THRESHOLD,
        "first_day_reached_threshold": None if int(peak_balance) < EARLY_MECHANIC_THRESHOLD else min(int(day) for day in peak_days),
        "mechanic_offer_count": len(early_mechanic_decisions),
        "mechanic_affordable_offer_count": affordable_offer_count,
        "mechanic_accept_count": accept_count,
        "first_offer_day": first_offer_day,
        "first_accept_day": first_accept_day,
        "route_interrupt_count": int(route_outcome_counts.get("interrupt", 0)),
        "medical_interrupt_count": medical_interrupt_count,
        "route_applied_count": int(route_outcome_counts.get("applied", 0)),
        "route_suppressed_count": int(route_outcome_counts.get("suppressed", 0)),
    }


def _fallback_prompt_label(kind, prompt="", recent="", options=None, source=""):
    base = (prompt or "").strip()
    if not base:
        recent_lines = [line.strip() for line in (recent or "").splitlines() if line.strip()]
        question_lines = [line for line in recent_lines if "?" in line or line.endswith(":")]
        if question_lines:
            base = question_lines[-1]
        elif recent_lines:
            base = recent_lines[-1]
        else:
            base = "(blank prompt)"
    base = ANSI_RE.sub("", base)
    base = re.sub(r"\s+", " ", base).strip()
    if len(base) > 90:
        base = base[:87] + "..."
    option_text = ""
    if options:
        rendered = "/".join(str(option).strip().lower() for option in list(options)[:4])
        if rendered:
            option_text = f" | {rendered}"
    source_text = f" [{source}]" if source else ""
    return f"{kind}: {base}{option_text}{source_text}"


def _record_fallback_decision(kind, prompt="", recent="", options=None, source=""):
    FALLBACK_DECISIONS[_fallback_prompt_label(kind, prompt, recent, options, source)] += 1


def _decide_mechanic_intro_response(player, recent, prompt="", source=""):
    if not _looks_like_mechanic_intro_offer(recent, prompt):
        return None
    cost = _extract_mechanic_offer_cost(prompt, recent)
    answer = "yes" if _should_buy_car_repair(player, cost, recent) else "no"
    _record_mechanic_decision(player, recent, cost, answer, source)
    return answer


def _recent_contains(*needles):
    haystack = "\n".join(RECENT_TEXT[-30:]).lower()
    return all(needle.lower() in haystack for needle in needles)


def _status_names(player):
    if player is None:
        return set()
    return {status.lower() for status in getattr(player, "_status_effects", [])}


def _injury_names(player):
    if player is None:
        return set()
    return {injury.lower() for injury in getattr(player, "_injuries", [])}


def _sellable_collectibles(player):
    if player is None or not hasattr(player, "get_collectible_prices"):
        return []
    sellable = []
    for item in player.get_collectible_prices().keys():
        if player.has_item(item):
            sellable.append(item)
    return sellable


def _planned_pawn_sales(player):
    if player is None or not hasattr(player, "get_collectible_prices"):
        return []

    owned = []
    for item_name, price in player.get_collectible_prices().items():
        if player.has_item(item_name):
            owned.append((item_name, price))
    if not owned:
        return []

    owned = [(item_name, price) for item_name, price in owned if price >= 100]
    if not owned:
        return []

    owned.sort(key=lambda entry: (-entry[1], entry[0]))
    balance = player.get_balance()
    target = _rank_target(balance)
    required_cash = 0

    if _wants_doctor_visit(player):
        required_cash = max(required_cash, max(0, _doctor_cash_reserve(player) - balance))
    elif _doctor_visit_is_urgent(player):
        required_cash = max(required_cash, max(0, _doctor_heal_cost_estimate(player) - balance))

    if player.has_item("Car") and (player.get_health() < 70 or player.get_sanity() < 35):
        required_cash = max(required_cash, max(0, _doctor_cash_reserve(player) - balance))

    if _stranded_no_car_mode(player):
        if balance < max(220, target):
            required_cash = max(required_cash, min(max(320, target), 600) - balance)
    elif _needs_car(player):
        if balance < 275:
            required_cash = max(required_cash, 275 - balance)
        elif balance + sum(price for _item, price in owned) >= 250:
            required_cash = max(required_cash, max(0, 250 - balance))
    elif player.get_rank() == 0:
        if balance < 900:
            required_cash = max(required_cash, min(1000, target) - balance)
    elif player.get_rank() == 1 and not player.has_item("Map"):
        if balance < 1800:
            required_cash = max(required_cash, 1800 - balance)
        elif balance + sum(price for _item, price in owned) >= 5000:
            required_cash = max(required_cash, 5000 - balance)
    else:
        if balance < 300:
            required_cash = max(required_cash, 300 - balance)
        elif balance + sum(price for _item, price in owned) >= target:
            required_cash = max(required_cash, target - balance)

    if required_cash <= 0:
        return []

    planned = []
    planned_total = 0
    for item_name, price in owned:
        planned.append(item_name)
        planned_total += price
        if planned_total >= required_cash:
            break

    return planned if planned_total > 0 else []


def _sellable_collectible_value(player):
    if player is None or not hasattr(player, "get_collectible_prices"):
        return 0
    prices = player.get_collectible_prices()
    return sum(prices.get(item, 0) for item in _sellable_collectibles(player))


def _structured_economy_hints(player):
    if player is None:
        return {}

    store_candidates = _store_purchase_candidates(player)
    planned_sales = _planned_pawn_sales(player)
    collectible_prices = player.get_collectible_prices() if hasattr(player, "get_collectible_prices") else {}
    pawn_planned_sale_value = sum(int(collectible_prices.get(item_name, 0) or 0) for item_name in planned_sales)
    marvin_affordable_priority = _best_marvin_affordable_priority(player) if _has_marvin_access(player) else 0
    marvin_candidate = _best_marvin_candidate(player, player.get_balance()) if _has_marvin_access(player) else None
    marvin_candidate_price = 0 if marvin_candidate is None else int(marvin_candidate[1])
    tuner = _rank_tuner(player)
    rank = int(player.get_rank()) if hasattr(player, "get_rank") else 0
    has_only_worn_map_access = player.has_item("Worn Map") and not player.has_item("Map") if hasattr(player, "has_item") else False
    marvin_strong_window = bool(
        marvin_candidate is not None
        and (
            (
                marvin_candidate[0] >= 84
                and player.get_balance() >= max(int(tuner["marvin_min_balance"]), marvin_candidate_price + max(1000, int(tuner["marvin_floor_buffer"] // 2)))
            )
            or (
                rank <= 1
                and marvin_candidate[0] >= 60
                and player.get_balance() >= max(1800, marvin_candidate_price + max(300, int(tuner["marvin_floor_buffer"] * 0.3)))
            )
            or (
                rank <= 1
                and marvin_candidate[0] >= 44
                and player.get_balance() >= max(1400, marvin_candidate_price + 100)
            )
            or (
                rank <= 1
                and has_only_worn_map_access
                and marvin_candidate[0] >= 50
                and player.get_balance() >= max(1600, marvin_candidate_price + 200)
            )
        )
    )
    return {
        "store_candidate_count": len(store_candidates),
        "store_best_priority": int(store_candidates[0][0]) if store_candidates else 0,
        "store_target_spend": int(store_candidates[0][1]) if store_candidates else 0,
        "pawn_sellable_value": _sellable_collectible_value(player),
        "pawn_planned_sale_count": len(planned_sales),
        "pawn_planned_sale_value": pawn_planned_sale_value,
        "marvin_affordable_priority": int(marvin_affordable_priority),
        "marvin_candidate_price": marvin_candidate_price,
        "marvin_strong_window": int(marvin_strong_window),
    }


def _has_active_item(player, item_name):
    if player is None or not player.has_item(item_name):
        return False
    if hasattr(player, "has_broken_item") and player.has_broken_item(item_name):
        return False
    if hasattr(player, "is_repairing_item") and player.is_repairing_item(item_name):
        return False
    return True


def _blackjack_edge_score(player):
    if player is None:
        return 0

    weights = {
        "Dirty Old Hat": 2,
        "Unwashed Hair": 3,
        "Pocket Watch": 5,
        "Golden Watch": 6,
        "Sapphire Watch": 7,
        "Grandfather Clock": 7,
        "Sneaky Peeky Shades": 5,
        "Sneaky Peeky Goggles": 7,
        "Quiet Sneakers": 3,
        "Quiet Bunny Slippers": 5,
        "Lucky Coin": 4,
        "Lucky Medallion": 5,
        "Worn Gloves": 4,
        "Velvet Gloves": 5,
        "Tattered Cloak": 4,
        "Invisible Cloak": 5,
        "Rusty Compass": 4,
        "Golden Compass": 6,
        "Gambler's Chalice": 3,
        "Overflowing Goblet": 4,
        "Twin's Locket": 3,
        "Mirror of Duality": 4,
        "White Feather": 3,
        "Phoenix Feather": 4,
        "Dealer's Grudge": 4,
        "Dealer's Mercy": 6,
        "Gambler's Grimoire": 3,
        "Oracle's Tome": 5,
        "Health Indicator": 0,
        "Health Manipulator": 0,
        "Delight Indicator": 0,
        "Delight Manipulator": 0,
        "Faulty Insurance": 3,
        "Real Insurance": 4,
        "Enchanting Silver Bar": 2,
        "Enchanting Gold Bar": 3,
        "Animal Whistle": 4,
    }
    return sum(weight for item_name, weight in weights.items() if _has_active_item(player, item_name))


def _broken_item_names(player):
    if player is None:
        return set()
    return set(getattr(player, "_broken_inventory", set()))


def _repairing_item_names(player):
    if player is None:
        return set()
    return set(getattr(player, "_repairing_inventory", set()))


def _repair_item_priority(item_name):
    priorities = {
        "Sapphire Watch": 104,
        "Grandfather Clock": 102,
        "Lucky Medallion": 100,
        "Pocket Watch": 100,
        "Golden Watch": 96,
        "Velvet Gloves": 95,
        "Lucky Coin": 94,
        "Worn Gloves": 92,
        "Invisible Cloak": 91,
        "Tattered Cloak": 90,
        "Overflowing Goblet": 89,
        "Gambler's Chalice": 88,
        "Mirror of Duality": 86,
        "Twin's Locket": 84,
        "Phoenix Feather": 83,
        "White Feather": 82,
        "Oracle's Tome": 81,
        "Gambler's Grimoire": 78,
        "Real Insurance": 77,
        "Faulty Insurance": 76,
        "Golden Compass": 74,
        "Dealer's Mercy": 72,
        "Health Indicator": 0,
        "Delight Indicator": 0,
        "Rusty Compass": 70,
        "Dealer's Grudge": 68,
        "Sneaky Peeky Goggles": 66,
        "Sneaky Peeky Shades": 64,
        "Quiet Bunny Slippers": 62,
        "Quiet Sneakers": 60,
        "Dirty Old Hat": 52,
        "Unwashed Hair": 54,
    }
    return priorities.get(item_name, 0)


def _needs_oswald_attention(player):
    return bool(_broken_item_names(player) or _repairing_item_names(player))


def _chosen_mechanic_name(player):
    if player is None or not hasattr(player, "get_chosen_mechanic"):
        return None
    chosen = player.get_chosen_mechanic()
    if chosen in {None, "", "None"}:
        return None
    return str(chosen)


def _available_mechanic_routes(player):
    if player is None:
        return []

    routes = []
    if player.has_met("Tom"):
        routes.append(("Tom", "Trusty Tom's Trucks and Tires", "mechanic:tom"))
    if player.has_met("Frank"):
        routes.append(("Frank", "Filthy Frank's Flawless Fixtures", "mechanic:frank"))
    if player.has_met("Oswald"):
        routes.append(("Oswald", "Oswald's Optimal Outoparts", "mechanic:oswald"))
    return routes


def _preferred_mechanic_route(player):
    available = _available_mechanic_routes(player)
    if not available:
        return None

    available_by_name = {name: (shop_label, visit_label) for name, shop_label, visit_label in available}
    chosen = _chosen_mechanic_name(player)
    if chosen in available_by_name:
        return available_by_name[chosen]

    if _needs_oswald_attention(player) and "Oswald" in available_by_name:
        return available_by_name["Oswald"]

    if _needs_car(player):
        for name in ["Tom", "Frank", "Oswald"]:
            if name in available_by_name:
                return available_by_name[name]

    for name in ["Tom", "Oswald", "Frank"]:
        if name in available_by_name:
            return available_by_name[name]

    return next(iter(available_by_name.values()), None)


def _chosen_mechanic_route(player):
    return _preferred_mechanic_route(player)


def _missed_all_mechanics(player):
    if player is None:
        return False
    return (
        player.has_met("Tom Event")
        and player.has_met("Frank Event")
        and player.has_met("Oswald Event")
        and not player.has_item("Car")
    )


def _stranded_no_car_mode(player):
    if player is None or player.has_item("Car"):
        return False

    if _missed_all_mechanics(player):
        return True

    if getattr(player, "_day", 1) < 18:
        return False

    if _available_mechanic_routes(player):
        return False

    return any(
        player.has_met(name)
        for name in ["Tom Event", "Frank Event", "Oswald Event"]
    )


def _companion_count(player):
    if player is None or not hasattr(player, "get_all_companions"):
        return 0
    return len(player.get_all_companions())


def _inventory_food_count(player):
    if player is None or not hasattr(player, "get_inventory_food"):
        return 0
    return len(player.get_inventory_food())


def _store_food_priority(item_name, player):
    if player is None or not hasattr(player, "get_food_data"):
        return 0

    food_data = player.get_food_data(item_name)
    if not food_data:
        return 0

    priority = 12
    health = player.get_health()
    sanity = player.get_sanity()
    food_count = _inventory_food_count(player)
    companion_count = _companion_count(player)

    priority += int(food_data.get("heal", 0)) * (2 if health < 70 else 1)
    priority += int(food_data.get("sanity", 0)) * (3 if sanity < 35 else 1)
    priority += int(food_data.get("fatigue_reduce", 0)) // 2

    if food_count == 0:
        priority += 10
    elif food_count == 1:
        priority += 4

    if health < 55:
        priority += int(food_data.get("heal", 0))
    if sanity < 25:
        priority += int(food_data.get("sanity", 0)) * 2
    if food_data.get("energy") and (health < 65 or sanity < 30):
        priority += 8
    if food_data.get("companion_food") and companion_count > 0:
        priority += min(10, companion_count * 2)

    return priority


def _should_group_with_companions(player):
    if player is None:
        return False
    companion_count = _companion_count(player)
    if companion_count <= 0:
        return False
    if player.get_health() < 85 or player.get_sanity() < 65:
        return True
    if companion_count >= 3:
        return True
    return False


def _location_history(player):
    if player is None:
        return {}, {}
    if not hasattr(player, "_autoplay_location_last_day"):
        player._autoplay_location_last_day = {}
    if not hasattr(player, "_autoplay_location_count"):
        player._autoplay_location_count = {}
    return player._autoplay_location_last_day, player._autoplay_location_count


def _mark_location_visit(player, label):
    if player is None:
        return
    last_days, counts = _location_history(player)
    last_days[label] = getattr(player, "_day", 1)
    counts[label] = counts.get(label, 0) + 1


def _days_since_location(player, *labels):
    if player is None:
        return None

    last_days, _counts = _location_history(player)
    current_day = getattr(player, "_day", 1)
    candidates = [last_days[label] for label in labels if label in last_days]
    if not candidates:
        return None
    return max(0, current_day - max(candidates))


def _needs_doctor(player):
    if player is None:
        return False
    severe_status_keywords = {
        "pneumonia", "waterborne illness", "severe dehydration", "staph infection", "needle exposure",
        "appendicitis", "blood pressure crisis", "heat stroke", "hypothermia", "kidney stones",
        "anaphylaxis", "uncontrolled diabetes", "pancreatitis", "gallbladder attack", "tetanus",
        "sepsis", "gangrene", "possible rabies", "severe asthma", "seizure disorder",
        "dvt", "severe burns", "malnutrition",
    }
    statuses = _status_names(player)
    injuries = _injury_names(player)
    severe_injury_keywords = {
        "ruptured spleen", "concussion", "broken ribs", "broken ankle", "broken wrist",
        "torn acl", "whiplash", "punctured lung", "dislocated shoulder",
    }
    return (
        any(keyword in statuses for keyword in severe_status_keywords)
        or any(keyword in injuries for keyword in severe_injury_keywords)
        or player._health < 35
        or player._sanity < 18
        or (player.has_item("Car") and len(injuries) >= 1 and 60 <= player._health < 85)
        or (player._health < 55 and len(injuries) >= 1)
        or (player._health < 60 and len(statuses) >= 1)
        or len(injuries) >= 2
        or (player._health < 50 and len(statuses) >= 2)
        or (player._sanity < 24 and len(statuses) >= 2)
        or len(statuses) >= 4
    )


def _doctor_visit_is_urgent(player):
    if player is None:
        return False
    urgent_statuses = {
        "appendicitis", "anaphylaxis", "blood pressure crisis", "dvt", "gangrene", "heat stroke",
        "hypothermia", "kidney stones", "needle exposure", "pancreatitis", "pneumonia",
        "possible rabies", "seizure disorder", "sepsis", "severe asthma", "severe dehydration",
        "staph infection", "tetanus", "uncontrolled diabetes", "waterborne illness",
    }
    statuses = _status_names(player)
    urgent_injuries = {"ruptured spleen", "concussion", "broken ribs", "punctured lung"}
    injuries = _injury_names(player)
    return (
        player._health < 30
        or player._sanity < 12
        or any(status in urgent_statuses for status in statuses)
        or any(injury in urgent_injuries for injury in injuries)
        or (player._health < 42 and len(statuses) >= 2)
    )


def _doctor_need_score(player):
    if player is None:
        return 0

    statuses = _status_names(player)
    injuries = _injury_names(player)
    severe_status_keywords = {
        "pneumonia", "waterborne illness", "severe dehydration", "staph infection", "needle exposure",
        "appendicitis", "blood pressure crisis", "heat stroke", "hypothermia", "kidney stones",
        "anaphylaxis", "uncontrolled diabetes", "pancreatitis", "gallbladder attack", "tetanus",
        "sepsis", "gangrene", "possible rabies", "severe asthma", "seizure disorder",
        "dvt", "severe burns", "malnutrition",
    }
    severe_injury_keywords = {
        "ruptured spleen", "concussion", "broken ribs", "broken ankle", "broken wrist",
        "torn acl", "whiplash", "punctured lung", "dislocated shoulder",
    }

    score = max(0, 55 - player.get_health())
    score += max(0, 30 - player.get_sanity()) // 2
    score += len(statuses) * 6
    score += len(injuries) * 12
    score += sum(18 for status in statuses if status in severe_status_keywords)
    score += sum(20 for injury in injuries if injury in severe_injury_keywords)
    if _doctor_visit_is_urgent(player):
        score += 100
    return score


def _doctor_heal_cost_estimate(player):
    if player is None:
        return 0
    balance = max(0, int(player.get_balance()))
    if player.has_item("Real Insurance"):
        return 0
    if player.has_item("Faulty Insurance"):
        return max(0, int(balance * 0.18))
    return max(0, int(balance * 0.48))


def _flask_count(player):
    if player is None or not hasattr(player, "len_flasks"):
        return 0
    return int(player.len_flasks())


def _witch_heal_cost_estimate(player):
    if player is None:
        return 0
    balance = max(0, int(player.get_balance()))
    if balance <= 200:
        return max(5, int(balance * 0.12))
    if balance <= 2000:
        return max(25, int(balance * 0.14))
    if balance <= 20000:
        return max(180, int(balance * 0.16))
    return max(1200, int(balance * 0.18))


def _best_affordable_witch_flask_priority(player):
    if player is None:
        return 0
    budget = player.get_balance() - _witch_heal_cost_estimate(player)
    if budget <= 0:
        return 0

    best_priority = 0
    for flask_name in [
        "No Bust",
        "Imminent Blackjack",
        "Dealer's Whispers",
        "Bonus Fortune",
        "Anti-Venom",
        "Anti-Virus",
        "Fortunate Day",
        "Fortunate Night",
        "Second Chance",
        "Split Serum",
        "Dealer's Hesitation",
        "Pocket Aces",
    ]:
        if _witch_flask_price_estimate(flask_name) > budget:
            continue
        best_priority = max(best_priority, _witch_flask_priority(flask_name, player))
    return best_priority


def _wants_witch_heal(player):
    if player is None or not player.has_met("Witch"):
        return False
    if not _needs_doctor(player):
        return False

    balance = player.get_balance()
    score = _doctor_need_score(player)
    flask_count = _flask_count(player)
    witch_gap = _days_since_location(player, "doctor:witch")
    doctor_available = not (hasattr(player, "has_danger") and player.has_danger("Doctor Ban"))
    if witch_gap == 0:
        return False

    estimated_cost = _witch_heal_cost_estimate(player)
    doctor_estimated_cost = _doctor_heal_cost_estimate(player)
    potion_priority = _best_affordable_witch_flask_priority(player)
    if _doctor_visit_is_urgent(player):
        return balance >= estimated_cost and ((not doctor_available) or doctor_estimated_cost > balance + 40)

    if player.has_item("Real Insurance") and doctor_available:
        return False
    if player.has_item("Faulty Insurance") and doctor_available:
        if len(_injury_names(player)) > 0 or player.get_health() < 64 or player.get_sanity() < 30:
            return False
        if potion_priority < 92:
            return False

    if flask_count >= 3:
        return False
    if balance < estimated_cost:
        return False
    if doctor_available and doctor_estimated_cost > balance and balance >= estimated_cost:
        return True
    if doctor_available and doctor_estimated_cost >= max(estimated_cost + 120, int(balance * 0.35)):
        if player.get_health() >= 48 and len(_injury_names(player)) == 0:
            return True
    if potion_priority >= 88 and player.get_health() >= 52 and player.get_sanity() >= 24:
        return True
    if player.get_health() < 68 or player.get_sanity() < 32:
        return True
    if score >= 64 and balance >= estimated_cost and len(_injury_names(player)) == 0:
        return True
    if balance >= 30000 and score < 140 and potion_priority < 80:
        return False
    return score >= 60 or potion_priority >= 72


def _should_visit_doctor(player):
    if player is None or not _needs_doctor(player):
        return False
    if hasattr(player, "has_danger") and player.has_danger("Doctor Ban"):
        return False

    balance = player.get_balance()
    urgent = _doctor_visit_is_urgent(player)
    score = _doctor_need_score(player)
    estimated_cost = _doctor_heal_cost_estimate(player)
    remaining_balance = balance - estimated_cost
    last_doctor_gap = _days_since_location(player, "doctor")
    injuries = _injury_names(player)
    statuses = _status_names(player)
    severe_injuries = {
        "ruptured spleen", "concussion", "broken ribs", "broken ankle", "broken wrist",
        "torn acl", "whiplash", "punctured lung", "dislocated shoulder",
    }

    if not urgent:
        if last_doctor_gap == 0:
            return False
        if last_doctor_gap is not None and last_doctor_gap <= 1 and score < 78:
            return False
        if last_doctor_gap is not None and last_doctor_gap <= 3 and score < 96:
            return False

    if player.has_item("Real Insurance"):
        if urgent:
            return True
        if player.get_health() < 72 or player.get_sanity() < 34:
            return True
        return score >= 34
    if player.has_item("Faulty Insurance"):
        if urgent:
            return True
        if player.get_health() < 74 or player.get_sanity() < 38:
            return True
        if len(statuses) >= 1:
            return True
        return score >= 26

    if urgent:
        return balance >= estimated_cost
    if player.has_item("Car"):
        if len(injuries) >= 2 and remaining_balance >= 70:
            return True
        if len(injuries) >= 1 and remaining_balance >= 80:
            if player.get_health() < 85 or any(injury in severe_injuries for injury in injuries):
                return True
        if len(statuses) >= 2 and remaining_balance >= 90 and player.get_health() < 80:
            return True
    if remaining_balance < 120:
        return False
    if player.get_health() < 62 and remaining_balance >= 120:
        return True
    if player.get_sanity() < 28 and remaining_balance >= 140:
        return True
    if len(statuses) >= 2 and remaining_balance >= 140:
        return True
    if len(injuries) >= 1 and player.get_health() < 68 and remaining_balance >= 130:
        return True
    if score >= 78 and remaining_balance >= 120:
        return True
    if score >= 64 and remaining_balance >= 220:
        return True
    if score >= 52 and remaining_balance >= 400:
        return True
    if score >= 42 and remaining_balance >= 800:
        return True
    return False


def _progression_phase(player):
    if player is None:
        return "unknown"
    if _needs_car(player):
        return "car_rush"
    balance = player.get_balance()
    if balance < 1000:
        return "rank_one_rush"
    if balance < 10000:
        return "rank_two_rush"
    if balance < 100000:
        return "rank_three_rush"
    if balance < 1000000:
        return "million_rush"
    return "late_game"


def _progress_stall_days(player):
    if player is None:
        return 0

    current_day = max(1, int(getattr(player, "_day", 1)))
    has_marvin_access = player.has_item("Map") or player.has_item("Worn Map")
    has_marvin_visit = getattr(player, "_autoplay_location_count", {}).get("shop:marvin", 0) > 0
    current_rank = int(player.get_rank())
    current_balance = int(player.get_balance())
    current_peak_gate = max(50, int(max(1, current_balance) * 0.25))

    tracker = getattr(player, "_autoplay_progress_tracker", None)
    if tracker is None:
        tracker = {
            "last_progress_day": current_day,
            "best_rank": current_rank,
            "best_balance": current_balance,
            "has_car": bool(player.has_item("Car")),
            "marvin_access": has_marvin_access,
            "marvin_visit": has_marvin_visit,
        }
        player._autoplay_progress_tracker = tracker
        return 0

    progressed = False
    if current_rank > tracker["best_rank"]:
        tracker["best_rank"] = current_rank
        progressed = True
    if current_balance >= tracker["best_balance"] + max(200, current_peak_gate):
        tracker["best_balance"] = current_balance
        progressed = True
    if player.has_item("Car") and not tracker["has_car"]:
        tracker["has_car"] = True
        progressed = True
    if has_marvin_access and not tracker["marvin_access"]:
        tracker["marvin_access"] = True
        progressed = True
    if has_marvin_visit and not tracker["marvin_visit"]:
        tracker["marvin_visit"] = True
        progressed = True

    if progressed:
        tracker["last_progress_day"] = current_day
    return max(0, current_day - tracker["last_progress_day"])


def _rank_tuner(player):
    rank = 0 if player is None else int(player.get_rank())
    return get_rank_tuner(rank)


def _doctor_cash_reserve(player):
    if player is None:
        return 0
    if _doctor_visit_is_urgent(player):
        if _wants_witch_heal(player):
            return _witch_heal_cost_estimate(player)
        return _doctor_heal_cost_estimate(player)
    if _needs_doctor(player):
        estimate = _witch_heal_cost_estimate(player) if player.has_met("Witch") else _doctor_heal_cost_estimate(player)
        return min(max(60, int(estimate * 0.75)), max(0, int(player.get_balance())))
    if _wants_witch_heal(player):
        return _witch_heal_cost_estimate(player)
    if _wants_doctor_visit(player):
        return _doctor_heal_cost_estimate(player)
    return 0


def _needs_recovery_day(player):
    if player is None:
        return False
    if _doctor_visit_is_urgent(player):
        return False
    health = player.get_health()
    sanity = player.get_sanity()
    day = getattr(player, "_day", 1)
    statuses = _status_names(player)
    injuries = _injury_names(player)
    if _needs_doctor(player) and not _wants_doctor_visit(player):
        return True
    if health < 62 or sanity < 24:
        return True
    if player.has_item("Car") and day >= 35 and sanity < 38:
        return True
    if player.has_item("Car") and day >= 45 and (statuses or injuries) and sanity < 44:
        return True
    if health < 72 and (statuses or injuries):
        return True
    if sanity < 32 and len(statuses) >= 2:
        return True
    return False


def _dealer_happiness(player):
    if player is None or not hasattr(player, "get_dealer_happiness"):
        return 50
    return int(player.get_dealer_happiness())


def _fraudulent_cash_amount(player):
    if player is None or not hasattr(player, "get_fraudulent_cash"):
        return 0
    return int(player.get_fraudulent_cash())


def _has_extra_round_item(player):
    if player is None:
        return False
    return any(
        player.has_item(item_name)
        for item_name in ["Pocket Watch", "Golden Watch", "Sapphire Watch", "Grandfather Clock"]
    )


def _cash_safety_reserve(player, priority=0):
    if player is None:
        return 0

    balance = player.get_balance()
    floor = _rank_floor(balance)
    tuner = _rank_tuner(player)
    reserve = 25
    stranded_no_car = _stranded_no_car_mode(player)

    if stranded_no_car:
        reserve = 15

    if player.has_item("Car"):
        reserve = max(reserve, 40)
    if balance < 1000 and player.has_item("Car"):
        reserve = max(reserve, 60)

    reserve = max(reserve, _doctor_cash_reserve(player))

    if stranded_no_car:
        reserve = min(reserve, max(15, min(balance, 45 if balance < 150 else 70 if balance < 400 else 90)))

    if floor:
        if priority >= 90:
            reserve = max(reserve, int(floor * tuner["floor_keep_high"]))
        elif priority >= 75:
            reserve = max(reserve, int(floor * tuner["floor_keep_mid"]))
        else:
            reserve = max(reserve, int(floor * tuner["floor_keep_base"]))

    return min(balance, reserve)


def _can_afford_optional_purchase(player, price, priority=0):
    if player is None or price is None:
        return False
    balance = player.get_balance()
    if balance < price:
        return False
    return balance - price >= _cash_safety_reserve(player, priority)


def _available_store_inventory(player):
    if player is None:
        return []
    return list(getattr(player, "_convenience_store_inventory", []))


def _store_item_priority(item_name, player):
    if player is None:
        return 0

    if player.has_item(item_name):
        return 0

    food_priority = _store_food_priority(item_name, player)
    priority = max(food_priority, get_store_base_priority(item_name))
    if item_name == "LifeAlert" and player.get_health() < 95:
        priority += 10
    if item_name == "Worn Map" and player.has_item("Car") and not player.has_item("Map"):
        priority += 34 if int(player.get_rank()) <= 1 else 16
    if item_name == "First Aid Kit" and (player.get_health() < 90 or _needs_doctor(player)):
        priority += 14
    if item_name in {"Road Flares", "Flashlight", "Bug Spray", "Duct Tape", "Water Bottles"} and player.get_health() < 85:
        priority += 8
    if item_name in {"Road Flares", "Flashlight", "Bug Spray", "Duct Tape", "Pocket Knife"} and player.get_sanity() < 45:
        priority += 6
    if item_name in STORE_CAR_SURVIVAL_PRIORITIES and player.has_item("Car"):
        priority += 10
    if item_name in {"Spare Tire", "Tire Patch Kit", "Fix-a-Flat", "Tool Kit", "Road Flares", "LifeAlert"} and player.get_balance() >= 200:
        priority += 8
    if item_name in {"Flashlight", "Pocket Knife", "Duct Tape", "Water Bottles", "Binoculars"} and player.get_balance() >= 1200:
        priority += 6
    if item_name == "Lottery Ticket" and player.get_balance() < 150:
        priority += 4
    if item_name == "Lucky Penny" and player.get_rank() == 0:
        priority += 4
    return priority


def _store_purchase_candidates(player):
    if player is None:
        return []

    balance = player.get_balance()
    candidates = []
    for item_name, price in _available_store_inventory(player):
        priority = _store_item_priority(item_name, player)
        if priority <= 0 or price > balance or not _can_afford_optional_purchase(player, price, priority):
            continue
        candidates.append((priority, price, item_name))

    candidates.sort(key=lambda entry: (-entry[0], entry[1], entry[2]))
    return candidates


def _wants_store_run(player):
    if player is None or _needs_car(player):
        return False
    if _doctor_visit_is_urgent(player):
        return False

    dealer_happiness = _dealer_happiness(player)
    store_gap = _days_since_location(player, "shop:convenience_store")
    if (
        hasattr(player, "is_gift_system_unlocked")
        and hasattr(player, "has_gift_wrapped")
        and player.is_gift_system_unlocked()
        and not player.has_gift_wrapped()
        and dealer_happiness <= 85
        and player.get_balance() >= 120
        and player.get_health() >= 60
        and player.get_sanity() >= 35
        and store_gap != 0
        and (store_gap is None or store_gap > 2)
    ):
        return True
    if dealer_happiness >= 96:
        return False

    candidates = _store_purchase_candidates(player)
    if not candidates:
        return False

    tuner = _rank_tuner(player)
    best_priority, best_price, _best_item = candidates[0]
    missing_survival = any(not player.has_item(item_name) for item_name in STORE_MUST_HAVE_ITEMS)
    balance = player.get_balance()
    midgame_growth_window = (
        player.has_item("Car")
        and player.get_rank() <= 1
        and 1200 <= balance < 10000
        and player.get_health() >= 65
        and player.get_sanity() >= 34
    )
    low_impact_store_item = _best_item not in {
        "Worn Map",
        "LifeAlert",
        "First Aid Kit",
        "Road Flares",
        "Spare Tire",
        "Tool Kit",
    }

    if (
        player.get_rank() >= 2
        and 10000 <= balance < 100000
        and _best_item not in {"LifeAlert", "First Aid Kit", "Road Flares", "Spare Tire", "Tool Kit"}
    ):
        return False

    if store_gap == 0:
        return False
    if store_gap is not None and store_gap <= 2 and _best_item not in STORE_MUST_HAVE_ITEMS:
        return False
    if store_gap is not None and store_gap <= 4 and best_priority < 90:
        return False
    if (
        missing_survival
        and store_gap != 0
        and (store_gap is None or store_gap >= 2)
        and player.get_balance() >= max(120, best_price)
        and player.get_health() >= 55
        and player.get_sanity() >= 28
        and best_priority >= 82
    ):
        return True

    if (
        midgame_growth_window
        and low_impact_store_item
        and best_priority < 90
        and best_price <= max(180, int(balance * 0.08))
    ):
        return False

    if best_priority >= 90:
        return True
    if best_priority >= tuner["store_priority_min"] and player.get_balance() - best_price >= 80:
        return True
    if (
        best_priority >= max(56, tuner["store_priority_min"] - 16)
        and player.get_balance() >= tuner["store_balance_gate"]
        and player.get_health() >= tuner["store_health_gate"]
        and player.get_sanity() >= tuner["store_sanity_gate"]
    ):
        return True
    return False


def _planned_store_spend(player):
    candidates = _store_purchase_candidates(player)
    if not candidates:
        return 0
    _priority, price, _name = candidates[0]
    return price


def _marvin_item_priority(item_name, player):
    if player is None or player.has_item(item_name):
        return 0

    priority = get_marvin_base_priority(item_name)
    if item_name == "Faulty Insurance" and player.has_item("Real Insurance"):
        return 0
    if player.has_item("Car") and player.get_rank() < 2:
        if item_name == "Faulty Insurance":
            priority += 18
        if item_name == "Pocket Watch":
            priority += 14
        if item_name == "Lucky Coin":
            priority += 12
        if item_name == "Gambler's Grimoire":
            priority += 12
        if item_name in {"Rusty Compass", "Quiet Sneakers", "Sneaky Peeky Shades"}:
            priority += 8
        if item_name in {"Animal Whistle", "White Feather", "Twin's Locket", "Dealer's Grudge"}:
            priority -= 10
    if item_name == "Dirty Old Hat" and player.get_rank() == 0 and player.get_balance() < 1000:
        priority += 12
    if item_name == "Dirty Old Hat" and player.get_rank() < 2 and player.get_balance() < 25000:
        priority -= 12
    if item_name == "Golden Watch" and player.get_balance() >= 5000:
        priority += 8
    if item_name == "Pocket Watch" and player.get_balance() >= 3000:
        priority += 6
    if item_name in {"Rusty Compass", "Quiet Sneakers", "Sneaky Peeky Shades"} and player.get_rank() < 2:
        priority += 10
    if item_name == "Animal Whistle":
        if _companion_count(player) < 5:
            priority += 14
        if player.has_item("Car"):
            priority += 8
    if item_name == "Enchanting Silver Bar":
        if player.get_balance() < 10000:
            priority -= 20
        else:
            priority += 12
    if item_name in {"Worn Gloves", "Tattered Cloak", "Pocket Watch", "Golden Watch"} and player.get_balance() >= 25000:
        priority += 8
    if item_name == "Gambler's Grimoire" and player.get_balance() >= 10000:
        priority += 6
    if item_name == "Animal Whistle" and player.get_rank() < 2 and player.get_balance() < 50000:
        priority -= 18
    return priority


def _marvin_price_estimate(item_name):
    return get_marvin_price_estimate(item_name)


def _best_marvin_affordable_priority(player):
    if player is None:
        return 0

    balance = player.get_balance()
    best_priority = 0
    for item_name in MARVIN_ITEM_ORDER:
        if _marvin_price_estimate(item_name) > balance:
            continue
        best_priority = max(best_priority, _marvin_item_priority(item_name, player))
    return best_priority


def _best_marvin_candidate(player, budget):
    if player is None or budget <= 0:
        return None

    best = None
    for item_name in MARVIN_ITEM_ORDER:
        price = _marvin_price_estimate(item_name)
        if price > budget:
            continue
        priority = _marvin_item_priority(item_name, player)
        if priority <= 0:
            continue
        candidate = (priority, price, item_name)
        if best is None or candidate[0] > best[0] or (candidate[0] == best[0] and candidate[1] < best[1]):
            best = candidate
    return best


def _marvin_loan_plan(player):
    if player is None or not player.has_item("Car") or not _has_marvin_access(player):
        return None
    if not player.has_met("Vinnie") or int(player.get_loan_shark_debt()) > 0:
        return None
    if _fraudulent_cash_amount(player) > 0:
        return None
    if player.get_health() < 56 or player.get_sanity() < 32:
        return None

    balance = player.get_balance()
    if balance < 2000 or balance >= 26000:
        return None

    current = _best_marvin_candidate(player, balance)
    if current is not None and current[0] >= 84:
        return None

    doctor_reserve = max(80, _doctor_cash_reserve(player))
    if balance <= doctor_reserve:
        return None

    for loan_amount in (500, 1000, 2500, 5000):
        candidate = _best_marvin_candidate(player, balance + loan_amount)
        if candidate is None:
            continue
        priority, price, item_name = candidate
        shortfall = max(0, price - balance)
        if shortfall == 0 or shortfall > loan_amount:
            continue
        if balance + loan_amount - price < doctor_reserve:
            continue
        if item_name == "Faulty Insurance" and priority >= 88 and shortfall <= loan_amount:
            return {"borrow": loan_amount, "price": price, "priority": priority, "item": item_name}
        if priority >= 92 and shortfall <= 2500:
            return {"borrow": loan_amount, "price": price, "priority": priority, "item": item_name}
        if priority >= 84 and shortfall <= 1500:
            return {"borrow": loan_amount, "price": price, "priority": priority, "item": item_name}
    return None


def _pending_marvin_candidate(player, balance=None, fake_cash=None):
    if player is None or not player.has_item("Car") or not _has_marvin_access(player):
        return None
    if getattr(player, "_autoplay_location_count", {}).get("shop:marvin", 0) > 0:
        return None
    if _wants_doctor_visit(player) or _doctor_visit_is_urgent(player):
        return None
    if player.get_health() < 56 or player.get_sanity() < 30:
        return None

    real_balance = max(0, int(player.get_balance() if balance is None else balance))
    blended_budget = real_balance + max(0, int(_fraudulent_cash_amount(player) if fake_cash is None else fake_cash))
    candidate = _best_marvin_candidate(player, blended_budget)
    if candidate is None:
        return None

    priority, price, item_name = candidate
    if priority < 78 and real_balance < price:
        return None

    return {
        "priority": priority,
        "price": price,
        "item": item_name,
        "shortfall": max(0, price - real_balance),
    }


def _current_offer_name(recent, names):
    recent_lower = recent.lower()
    for name in sorted(names, key=len, reverse=True):
        if name.lower() in recent_lower:
            return name
    return None


def _has_marvin_access(player):
    return player is not None and (player.has_item("Map") or player.has_item("Worn Map"))


def _wants_marvin_run(player):
    if not _has_marvin_access(player):
        return False
    if _wants_doctor_visit(player):
        return False
    if player.get_health() < 54 or player.get_sanity() < 28:
        return False
    balance = player.get_balance()
    floor = _rank_floor(balance)
    tuner = _rank_tuner(player)
    marvin_gap = _days_since_location(player, "shop:marvin")
    has_only_worn_map_access = player.has_item("Worn Map") and not player.has_item("Map")
    affordable_priority = _best_marvin_affordable_priority(player)
    stall_days = _progress_stall_days(player)
    if marvin_gap == 0:
        return False
    if marvin_gap is not None and marvin_gap <= 2 and player.get_rank() < 2:
        return False
    if (
        player.get_rank() <= 1
        and affordable_priority >= 60
        and balance >= 1500
        and player.get_health() >= 56
        and player.get_sanity() >= 30
        and (marvin_gap is None or marvin_gap >= 4)
    ):
        return True
    if (
        player.get_rank() >= 1
        and balance >= 2200
        and player.get_health() >= 60
        and player.get_sanity() >= 34
        and stall_days >= 8
        and (marvin_gap is None or marvin_gap >= 6)
    ):
        return True
    if stall_days >= 12 and affordable_priority >= 60 and balance >= 1200:
        return True
    if stall_days >= 8 and affordable_priority >= 50 and balance >= 1500:
        return True
    if stall_days >= 18 and affordable_priority >= 44 and balance >= 1400:
        return True
    if player.get_rank() < 2 and has_only_worn_map_access and affordable_priority >= 50:
        return balance >= max(1800, floor - 400 if floor else 1800)
    if player.get_rank() < 2 and has_only_worn_map_access and balance >= 7000 and affordable_priority >= 50:
        return True
    if player.get_rank() < 2 and balance < (1400 if affordable_priority >= 44 else 1800):
        return False
    if player.get_rank() < 2 and affordable_priority >= 44:
        return True
    if player.get_rank() < 2 and balance >= 3500 and player.get_health() >= 56 and player.get_sanity() >= 30:
        return True
    if affordable_priority >= 84:
        return balance >= max(8000, floor - 1000 if floor else 8000)
    if player.get_rank() >= 2 and _blackjack_edge_score(player) < 5:
        return balance >= max(6000, floor)
    return balance >= max(tuner["marvin_min_balance"], floor + tuner["marvin_floor_buffer"])


def _marvin_bootstrap_window(player):
    if player is None or not _wants_marvin_run(player):
        return False

    rank = int(player.get_rank())
    if rank > 1:
        return False

    balance = player.get_balance()
    affordable_priority = _best_marvin_affordable_priority(player)
    has_only_worn_map_access = player.has_item("Worn Map") and not player.has_item("Map")

    if affordable_priority >= 60 and balance >= 1400:
        return True
    if has_only_worn_map_access and affordable_priority >= 50 and balance >= 1500:
        return True
    return affordable_priority >= 50 and balance >= 1650


def _wants_oswald_progression_run(player):
    if player is None or not player.has_item("Car"):
        return False
    if _chosen_mechanic_name(player) != "Oswald":
        return False
    if _wants_doctor_visit(player) or _doctor_visit_is_urgent(player):
        return False
    if not hasattr(player, "get_mechanic_visits"):
        return False

    gap = _days_since_location(player, "mechanic:oswald")
    if gap == 0:
        return False
    if _needs_oswald_attention(player):
        if _repairing_item_names(player):
            return gap is None or gap >= 1
        if gap is not None and gap <= 1:
            return False
        best_broken = max((_repair_item_priority(item_name) for item_name in _broken_item_names(player)), default=0)
        if best_broken >= 88:
            return player.get_balance() >= 4500
        if best_broken >= 72:
            return player.get_balance() >= 2500
        return player.get_balance() >= 1200

    visits = player.get_mechanic_visits()
    if visits >= 3:
        return False
    if gap is not None and gap <= 2:
        return False

    balance = player.get_balance()
    if player.get_health() < 55 or player.get_sanity() < 22:
        return False
    if not _needs_oswald_attention(player) and _marvin_bootstrap_window(player):
        return False

    if visits <= 0:
        return balance >= 120
    if visits == 1:
        return balance >= 250 or player.get_rank() >= 1
    if player.get_rank() >= 2:
        return balance >= max(300, _rank_floor(balance))
    return balance >= 450


def _wants_mechanic_progression_run(player):
    if player is None or not player.has_item("Car"):
        return False
    if _wants_doctor_visit(player) or _doctor_visit_is_urgent(player):
        return False
    if not hasattr(player, "get_mechanic_visits"):
        return False

    chosen_route = _chosen_mechanic_route(player)
    if chosen_route is None:
        return False

    gap = _days_since_location(player, chosen_route[1])
    if gap == 0:
        return False
    if _needs_oswald_attention(player):
        if _repairing_item_names(player):
            return gap is None or gap >= 1
        if gap is not None and gap <= 1:
            return False
        best_broken = max((_repair_item_priority(item_name) for item_name in _broken_item_names(player)), default=0)
        if best_broken >= 88:
            return player.get_balance() >= 4500
        if best_broken >= 72:
            return player.get_balance() >= 2500
        return player.get_balance() >= 1200

    visits = player.get_mechanic_visits()
    if visits >= 3:
        return False
    if gap is not None and gap <= 2:
        return False

    balance = player.get_balance()
    if player.get_health() < 55 or player.get_sanity() < 22:
        return False

    if visits <= 0:
        return balance >= 120
    if visits == 1:
        return balance >= 250 or player.get_rank() >= 1
    if player.get_rank() >= 2:
        return balance >= max(300, _rank_floor(balance))
    return balance >= 450


def _choose_mechanic_progression_destination(labels, player):
    if not _wants_mechanic_progression_run(player):
        return None

    chosen_route = _chosen_mechanic_route(player)
    if chosen_route is None:
        return None

    shop_label, _visit_label = chosen_route
    if shop_label not in labels:
        return None

    return labels[shop_label]


def _upgrade_item_priority(item_name):
    return get_upgrade_base_priority(item_name)


def _best_upgrade_candidate(player):
    if player is None or not hasattr(player, "can_upgrade"):
        return None

    candidates = []
    for item_name, price in sorted(
        ((item_name, get_upgrade_price_estimate(item_name)) for item_name in (
            "Delight Indicator",
            "Health Indicator",
            "Dirty Old Hat",
            "Golden Watch",
            "Sneaky Peeky Shades",
            "Quiet Sneakers",
            "Faulty Insurance",
            "Lucky Coin",
            "Worn Gloves",
            "Tattered Cloak",
            "Rusty Compass",
            "Pocket Watch",
            "Gambler's Chalice",
            "Twin's Locket",
            "White Feather",
            "Dealer's Grudge",
            "Gambler's Grimoire",
        )),
        key=lambda entry: entry[0],
    ):
        if not player.can_upgrade(item_name):
            continue
        priority = _upgrade_item_priority(item_name)
        if priority <= 0 or not _can_afford_optional_purchase(player, price, priority):
            continue
        candidates.append((priority, price, item_name))

    if not candidates:
        return None
    candidates.sort(key=lambda entry: (-entry[0], entry[1], entry[2]))
    return candidates[0]


def _wants_upgrade_run(player):
    if player is None or not hasattr(player, "can_access_upgrades"):
        return False
    if _chosen_mechanic_name(player) != "Oswald":
        return False
    if not player.can_access_upgrades() or _wants_doctor_visit(player):
        return False
    if player.get_rank() < 2:
        return False
    if _needs_oswald_attention(player):
        return False
    upgrade_gap = _days_since_location(player, "shop:car_workbench")
    if upgrade_gap == 0:
        return False
    if upgrade_gap is not None and upgrade_gap <= 3 and player.get_rank() < 4:
        return False
    return _best_upgrade_candidate(player) is not None


def _workbench_best_craft_candidate(player):
    """Returns (recipe_name, priority) for the best craftable item, or None.

    Uses player._lists.get_available_recipes to find what can be crafted,
    then ranks them by get_crafting_recipe_priority.  Companion items get a
    bonus when companions are present so the bot prefers them.
    """
    if player is None or not hasattr(player, "_lists"):
        return None
    try:
        available = player._lists.get_available_recipes(player)
    except Exception:
        return None
    if not available:
        return None
    companion_count = _companion_count(player)
    best_name = None
    best_priority = -1
    for name in available:
        priority = get_crafting_recipe_priority(name)
        recipe = available[name]
        if recipe.get("category") == "companion" and companion_count > 0:
            priority += 18
        if priority > best_priority:
            best_name = name
            best_priority = priority
    if best_name is None or best_priority < 60:
        return None
    return (best_name, best_priority)


def _choose_workbench_menu(options, player):
    """Choose from workbench main menu: craft if viable, otherwise pack up."""
    leave_choice = None
    craft_choice = None
    for number, label in options:
        lowered = label.lower()
        if "pack up" in lowered or "leave" in lowered:
            leave_choice = number
        elif "craft something" in lowered or lowered.startswith("1.") or number == 1:
            craft_choice = number

    candidate = _workbench_best_craft_candidate(player)
    if candidate is not None and craft_choice is not None:
        name, priority = candidate
        return _record_numeric_menu_trace(
            player,
            request_type="menu_select",
            stable_context_id="workbench_menu",
            menu_options=options,
            chosen_number=craft_choice,
            reason=f"workbench_craft_viable:{name}",
            confidence=0.78,
        )
    # No viable recipe: pack up
    target = leave_choice if leave_choice is not None else (options[-1][0] if options else 1)
    return _record_numeric_menu_trace(
        player,
        request_type="menu_select",
        stable_context_id="workbench_menu",
        menu_options=options,
        chosen_number=target,
        reason="workbench_pack_up_no_recipes",
        confidence=0.88,
    )


def _choose_workbench_craft(options, player):
    """Pick the best recipe from the workbench craft sub-menu."""
    if not options:
        return options[-1][0] if options else 1
    cancel_choice = None
    companion_count = _companion_count(player)
    best_number = None
    best_priority = -1
    for number, label in options:
        lowered = label.lower()
        if "never mind" in lowered or "cancel" in lowered:
            cancel_choice = number
            continue
        # Match recipe name from the label (number. Name <- ingredients)
        label_stripped = label.split("←")[0].strip()
        label_stripped = label_stripped.lstrip("0123456789. ").strip()
        priority = get_crafting_recipe_priority(label_stripped)
        if priority <= 0:
            # Try matching known recipe names inside the label
            for known_name in ("Companion Bed", "Pet Toy", "Feeding Station",
                               "Home Remedy", "Wound Salve", "Splint",
                               "Binocular Scope", "Road Flare Torch",
                               "Pepper Spray", "Dream Catcher", "Emergency Blanket"):
                if known_name.lower() in lowered:
                    priority = get_crafting_recipe_priority(known_name)
                    break
        if priority <= 0:
            continue
        recipe_cat = ""
        for r_name in ("Companion Bed", "Pet Toy", "Feeding Station"):
            if r_name.lower() in lowered:
                recipe_cat = "companion"
                break
        if recipe_cat == "companion" and companion_count > 0:
            priority += 18
        if priority > best_priority:
            best_priority = priority
            best_number = number

    if best_number is not None:
        return _record_numeric_menu_trace(
            player,
            request_type="menu_select",
            stable_context_id="workbench_craft_menu",
            menu_options=options,
            chosen_number=best_number,
            reason="workbench_recipe_selected",
            confidence=0.82,
        )
    # No good recipe found: cancel
    target = cancel_choice if cancel_choice is not None else (options[-1][0] if options else 1)
    return _record_numeric_menu_trace(
        player,
        request_type="menu_select",
        stable_context_id="workbench_craft_menu",
        menu_options=options,
        chosen_number=target,
        reason="workbench_no_viable_recipe_cancel",
        confidence=0.8,
    )


def _wants_doctor_visit(player):
    return player is not None and _should_visit_doctor(player)


def _defer_doctor_for_no_car_progression(player, route_labels, planned_goal=None):
    if player is None or player.has_item("Car") or _doctor_visit_is_urgent(player):
        return False

    if planned_goal is None:
        planned_goal = choose_strategic_goal(
            _current_game_state(player, context_tag="no_car_doctor_deferral")
        ).goal

    if planned_goal != "acquire_car":
        return False

    injuries = _injury_names(player)
    statuses = _status_names(player)
    severe_injuries = {"ruptured spleen", "concussion", "broken ribs", "punctured lung"}
    severe_statuses = {
        "appendicitis", "anaphylaxis", "blood pressure crisis", "dvt", "gangrene", "heat stroke",
        "hypothermia", "kidney stones", "needle exposure", "pancreatitis", "pneumonia",
        "possible rabies", "seizure disorder", "sepsis", "severe asthma", "severe dehydration",
        "staph infection", "tetanus", "uncontrolled diabetes", "waterborne illness",
    }
    progression_routes = {
        "Trusty Tom's Trucks and Tires",
        "Filthy Frank's Flawless Fixtures",
        "Oswald's Optimal Outoparts",
        "Grimy Gus's Pawn Emporium",
        "Vinnie's Back Alley Loans",
    }

    if not any(label in route_labels for label in progression_routes):
        return False

    return (
        player.get_health() >= 50
        and player.get_sanity() >= 28
        and len(injuries) <= 1
        and len(statuses) <= 2
        and not any(injury in severe_injuries for injury in injuries)
        and not any(status in severe_statuses for status in statuses)
        and _doctor_need_score(player) < 92
    )


def _medical_destination_label(player):
    if player is None or not _needs_doctor(player):
        return None
    game_state = _current_game_state(player, context_tag="medical_destination")
    options = [
        DecisionOption(option_id="medical:doctor", label="Doctor's Office", value="Doctor's Office"),
    ]
    if player.has_met("Witch"):
        options.append(DecisionOption(option_id="medical:witch", label="Witch Doctor's Tower", value="Witch Doctor's Tower"))
    request = DecisionRequest(
        request_type="medical_select",
        stable_context_id="medical_destination",
        game_state=game_state.to_dict(),
        normalized_options=tuple(options),
        metadata={
            "doctor_need_score": _doctor_need_score(player),
            "urgent_medical": _doctor_visit_is_urgent(player),
            "wants_doctor": _wants_doctor_visit(player),
            "wants_witch": _wants_witch_heal(player),
            "affordable_flask_priority": _best_affordable_witch_flask_priority(player),
            "doctor_cost": _doctor_heal_cost_estimate(player),
            "witch_cost": _witch_heal_cost_estimate(player),
            "flask_count": _flask_count(player),
            "has_real_insurance": player.has_item("Real Insurance"),
            "has_faulty_insurance": player.has_item("Faulty Insurance"),
        },
    )
    plan = choose_strategic_goal(game_state)
    choice, _trace = choose_medical_option(request, plan)
    if choice is None:
        return None
    return str(choice.value or choice.label)


def _witch_flask_priority(flask_name, player):
    if player is None or flask_name is None:
        return 0
    if hasattr(player, "has_flask_effect") and player.has_flask_effect(flask_name):
        return 0

    priority = get_witch_flask_base_priority(flask_name)
    if flask_name == "Anti-Virus" and _status_names(player):
        priority += 18
    if flask_name == "Anti-Venom" and any(
        keyword in _status_names(player)
        for keyword in {"spider bite", "possible rabies", "needle exposure"}
    ):
        priority += 18
    if flask_name in {"No Bust", "Second Chance", "Dealer's Whispers", "Bonus Fortune"} and player.get_rank() >= 1:
        priority += 8
    if flask_name in {"No Bust", "Second Chance"} and player.get_balance() >= 10000:
        priority += 10
    if flask_name in {"Fortunate Day", "Fortunate Night"} and player.get_balance() < 10000:
        priority -= 12
    if _flask_count(player) >= 2:
        priority -= 18
    return priority


def _witch_flask_price_estimate(flask_name):
    return get_witch_flask_price_estimate(flask_name)


def _choose_witch_flask(options, player):
    defensive_flasks = {"No Bust", "Second Chance", "Anti-Virus", "Anti-Venom", "Dealer's Whispers"}
    offensive_flasks = {"Imminent Blackjack", "Pocket Aces", "Split Serum", "Bonus Fortune", "Dealer's Hesitation"}
    leave_choice = None
    best_choice = None
    option_metadata_by_number = {}
    for number, label in options:
        if "not buying anything" in label.lower():
            leave_choice = number
            option_metadata_by_number[number] = {"is_exit": True, "base_score": 0.0, "category": "exit"}
            continue
        flask_name = label.replace("Flask of ", "", 1).strip()
        priority = _witch_flask_priority(flask_name, player)
        category = "defensive_flask" if flask_name in defensive_flasks else "offensive_flask" if flask_name in offensive_flasks else "utility_flask"
        option_metadata_by_number[number] = {
            "item_name": flask_name,
            "priority": float(priority),
            "base_score": float(priority),
            "price": float(_witch_flask_price_estimate(flask_name)),
            "category": category,
        }
        if priority <= 0:
            continue
        if player is None or player.get_balance() < _witch_flask_price_estimate(flask_name):
            continue
        if best_choice is None or priority > best_choice[0]:
            best_choice = (priority, number, flask_name)
    policy_choice = _choose_policy_numeric_option(
        player,
        request_type="purchase_select",
        stable_context_id="witch_flask_menu",
        menu_options=options,
        option_metadata_by_number=option_metadata_by_number,
    )
    if policy_choice is not None:
        return policy_choice
    if best_choice is not None:
        return _record_numeric_menu_trace(
            player,
            request_type="purchase_select",
            stable_context_id="witch_flask_menu",
            menu_options=options,
            chosen_number=best_choice[1],
            reason=f"witch_flask_priority:{best_choice[2]}",
            confidence=0.66,
        )
    fallback = leave_choice if leave_choice is not None else (options[-1][0] if options else 1)
    return _record_numeric_menu_trace(
        player,
        request_type="purchase_select",
        stable_context_id="witch_flask_menu",
        menu_options=options,
        chosen_number=fallback,
        reason="witch_flask_decline",
        confidence=0.5,
    )


def _is_progression_ready(player):
    if player is None:
        return False
    if player.get_rank() >= 2 and player.has_item("Car"):
        return (
            not _doctor_visit_is_urgent(player)
            and player.get_health() >= 50
            and player.get_sanity() >= 24
        )
    return (
        player.has_item("Car")
        and not _wants_doctor_visit(player)
        and not _wants_store_run(player)
        and player.get_health() >= 50
        and player.get_sanity() >= 26
    )


def _wants_millionaire_push(player):
    if player is None or not player.has_item("Car"):
        return False
    if _wants_doctor_visit(player) or _doctor_visit_is_urgent(player):
        return False
    balance = player.get_balance()
    return balance >= 100000 and balance < 1000000 and player.get_health() >= 65 and player.get_sanity() >= 40


def _choose_millionaire_afternoon(options, player):
    """Choose from millionaire afternoon menu.

    Preference order: chosen mechanic ending > any mechanic ending > airport ending.
    The "continue gambling" option is also available but we prefer ending.
    Traces the decision for post-run review.
    """
    if not options:
        return 1
    mechanic_choice = None
    airport_choice = None
    chosen_mechanic = _chosen_mechanic_name(player)
    for number, label in options:
        lowered = label.lower()
        if "airport" in lowered:
            airport_choice = number
            continue
        # Check for mechanic visit option
        if any(name in lowered for name in ("tom", "frank", "oswald")):
            if chosen_mechanic and chosen_mechanic.lower() in lowered:
                mechanic_choice = number  # prefer the chosen mechanic
            elif mechanic_choice is None:
                mechanic_choice = number  # fallback to any mechanic

    # Prefer mechanic ending; fall back to airport; fall back to last option
    target = mechanic_choice if mechanic_choice is not None else (airport_choice or options[-1][0])
    reason = (
        f"millionaire_mechanic_ending:{chosen_mechanic}"
        if target == mechanic_choice and mechanic_choice is not None
        else "millionaire_airport_ending"
        if target == airport_choice
        else "millionaire_afternoon_fallback"
    )
    return _record_numeric_menu_trace(
        player,
        request_type="menu_select",
        stable_context_id="millionaire_afternoon",
        menu_options=options,
        chosen_number=target,
        reason=reason,
        confidence=0.85,
    )


def _repair_item_priorities(player):
    if player is None:
        return []
    return sorted(
        getattr(player, "_broken_inventory", set()),
        key=lambda item_name: (-_repair_item_priority(item_name), item_name),
    )


def _choose_repair_item(options, player):
    priorities = _repair_item_priorities(player)
    leave_choice = None
    option_metadata_by_number = {}
    for number, label in options:
        if "I'm all set" in label or "I'm finished" in label or "Never mind" in label or "Pack Up" in label:
            leave_choice = number
            option_metadata_by_number[number] = {"is_exit": True, "base_score": 0.0, "category": "exit"}
            continue
        base_score = 0.0
        for wanted in priorities:
            if label.strip() == wanted:
                base_score = float(_repair_item_priority(wanted))
                option_metadata_by_number[number] = {
                    "item_name": wanted,
                    "priority": base_score,
                    "base_score": base_score,
                }
                break
        else:
            option_metadata_by_number[number] = {"base_score": 0.0}
    policy_choice = _choose_policy_numeric_option(
        player,
        request_type="repair_select",
        stable_context_id="repair_menu",
        menu_options=options,
        option_metadata_by_number=option_metadata_by_number,
    )
    if policy_choice is not None:
        return policy_choice
    fallback = leave_choice if leave_choice is not None else (options[-1][0] if options else 1)
    return _record_numeric_menu_trace(
        player,
        request_type="repair_select",
        stable_context_id="repair_menu",
        menu_options=options,
        chosen_number=fallback,
        reason="repair_menu_exit",
        confidence=0.52,
    )


def _choose_upgrade_item(options, player):
    best = _best_upgrade_candidate(player)
    leave_choice = None
    option_metadata_by_number = {}
    for number, label in options:
        if "I'm finished" in label:
            leave_choice = number
            option_metadata_by_number[number] = {"is_exit": True, "base_score": 0.0, "category": "exit"}
            continue
        item_name = label.split("→", 1)[0].strip()
        option_metadata_by_number[number] = {
            "item_name": item_name,
            "priority": float(_upgrade_item_priority(item_name)),
            "base_score": float(best[0]) if best is not None and item_name == best[2] else 0.0,
        }
    policy_choice = _choose_policy_numeric_option(
        player,
        request_type="upgrade_select",
        stable_context_id="upgrade_menu",
        menu_options=options,
        option_metadata_by_number=option_metadata_by_number,
    )
    if policy_choice is not None:
        return policy_choice
    fallback = leave_choice if leave_choice is not None else (options[-1][0] if options else 1)
    return _record_numeric_menu_trace(
        player,
        request_type="upgrade_select",
        stable_context_id="upgrade_menu",
        menu_options=options,
        chosen_number=fallback,
        reason="upgrade_menu_exit",
        confidence=0.52,
    )


def _choose_loan_menu(options, player):
    debt = 0 if player is None else int(player.get_loan_shark_debt())
    warning = 0 if player is None or not hasattr(player, "get_loan_shark_warning_level") else int(player.get_loan_shark_warning_level())
    edge_score = _blackjack_edge_score(player)
    reserve = _cash_safety_reserve(player, 88) if player is not None else 0
    balance = 0 if player is None else player.get_balance()
    repayment_capacity = max(0, balance - reserve)
    marvin_loan_plan = _marvin_loan_plan(player)
    leave_choice = None
    option_metadata_by_number = {}
    for number, label in options:
        lowered = label.lower()
        option_metadata_by_number[number] = {"action_kind": "leave", "base_score": 0.0, "actionable": False}
        if "repay debt" in lowered and debt > 0:
            option_metadata_by_number[number] = {"action_kind": "repay", "amount": float(debt), "base_score": 0.0, "actionable": False}
            if repayment_capacity >= debt:
                option_metadata_by_number[number]["base_score"] = 100.0
                option_metadata_by_number[number]["actionable"] = True
            if warning >= 2 and repayment_capacity >= min(100, debt):
                option_metadata_by_number[number]["base_score"] = max(option_metadata_by_number[number]["base_score"], 86.0)
                option_metadata_by_number[number]["actionable"] = True
            if warning >= 1 and repayment_capacity >= max(100, debt // 2):
                option_metadata_by_number[number]["base_score"] = max(option_metadata_by_number[number]["base_score"], 72.0)
                option_metadata_by_number[number]["actionable"] = True
        if "borrow money" in lowered and debt == 0 and player is not None:
            option_metadata_by_number[number] = {"action_kind": "borrow", "base_score": 0.0, "actionable": False}
            if marvin_loan_plan is not None:
                option_metadata_by_number[number]["base_score"] = 98.0
                option_metadata_by_number[number]["actionable"] = True
            if _poverty_escape_loan_mode(player):
                option_metadata_by_number[number]["base_score"] = max(option_metadata_by_number[number]["base_score"], 90.0)
                option_metadata_by_number[number]["actionable"] = True
            if _stranded_no_car_mode(player) and balance < 900:
                option_metadata_by_number[number]["base_score"] = max(option_metadata_by_number[number]["base_score"], 84.0)
                option_metadata_by_number[number]["actionable"] = True
            if player.has_met("Vinnie") and _fraudulent_cash_amount(player) == 0:
                if balance < 3000 and edge_score >= 2:
                    option_metadata_by_number[number]["base_score"] = max(option_metadata_by_number[number]["base_score"], 70.0)
                    option_metadata_by_number[number]["actionable"] = True
                if balance < 5000 and edge_score >= 4:
                    option_metadata_by_number[number]["base_score"] = max(option_metadata_by_number[number]["base_score"], 76.0)
                    option_metadata_by_number[number]["actionable"] = True
            if _has_marvin_access(player) and balance < 6000 and edge_score >= 3:
                option_metadata_by_number[number]["base_score"] = max(option_metadata_by_number[number]["base_score"], 72.0)
                option_metadata_by_number[number]["actionable"] = True
            if balance < 400:
                option_metadata_by_number[number]["base_score"] = max(option_metadata_by_number[number]["base_score"], 62.0)
                option_metadata_by_number[number]["actionable"] = True
            if balance < 1400 and edge_score >= 3:
                option_metadata_by_number[number]["base_score"] = max(option_metadata_by_number[number]["base_score"], 66.0)
                option_metadata_by_number[number]["actionable"] = True
            if edge_score >= 6 and balance < 1800:
                option_metadata_by_number[number]["base_score"] = max(option_metadata_by_number[number]["base_score"], 74.0)
                option_metadata_by_number[number]["actionable"] = True
            if edge_score >= 4 and balance < 700:
                option_metadata_by_number[number]["base_score"] = max(option_metadata_by_number[number]["base_score"], 64.0)
                option_metadata_by_number[number]["actionable"] = True
            if _fraudulent_cash_amount(player) == 0 and balance < 250:
                option_metadata_by_number[number]["base_score"] = max(option_metadata_by_number[number]["base_score"], 68.0)
                option_metadata_by_number[number]["actionable"] = True
        if "leave" in lowered or "never mind" in lowered:
            leave_choice = number
            option_metadata_by_number[number] = {"action_kind": "leave", "base_score": 12.0, "is_exit": True}
    policy_choice = _choose_policy_numeric_option(
        player,
        request_type="loan_decision",
        stable_context_id="loan_menu",
        menu_options=options,
        option_metadata_by_number=option_metadata_by_number,
        metadata={"debt": debt, "warning_level": warning},
    )
    if policy_choice is not None:
        return policy_choice
    fallback = leave_choice if leave_choice is not None else (options[-1][0] if options else 1)
    return _record_numeric_menu_trace(
        player,
        request_type="loan_decision",
        stable_context_id="loan_menu",
        menu_options=options,
        chosen_number=fallback,
        reason="loan_menu_exit",
        confidence=0.48,
    )


def _looks_like_loan_menu(options):
    labels = [label.lower() for _, label in options]
    if not labels:
        return False
    has_leave = any("leave" in label or "never mind" in label for label in labels)
    return has_leave and any("borrow money" in label or "repay debt" in label for label in labels)


def _looks_like_loan_borrow_menu(options):
    labels = [label.lower() for _, label in options]
    if not labels:
        return False
    has_leave = any("never mind" in label for label in labels)
    has_amount = any("borrow $" in label for label in labels)
    return has_leave and has_amount


def _looks_like_loan_repay_menu(options):
    labels = [label.lower() for _, label in options]
    if not labels:
        return False
    has_leave = any("never mind" in label for label in labels)
    repayment_markers = ("pay in full", "pay half", "pay what you have", "pay everything")
    return has_leave and any(any(marker in label for marker in repayment_markers) for label in labels)


def _choose_loan_borrow_amount(options, player):
    leave_choice = None
    target = _rank_target(0 if player is None else player.get_balance())
    balance = 0 if player is None else player.get_balance()
    edge_score = _blackjack_edge_score(player)
    marvin_loan_plan = _marvin_loan_plan(player)
    if marvin_loan_plan is not None:
        desired = marvin_loan_plan["borrow"]
    elif _poverty_escape_loan_mode(player):
        desired = 5000 if edge_score >= 6 else 2500 if edge_score >= 4 else 1000
    elif _stranded_no_car_mode(player):
        desired = 2500 if edge_score >= 5 else 1000
    elif balance < 250:
        desired = 1000 if edge_score >= 4 else 500
    elif balance < 800:
        desired = 1000 if edge_score >= 5 else 500
    elif balance < 1800 and edge_score >= 4:
        desired = 2500
    elif edge_score >= 6:
        desired = min(5000, max(500, target - balance))
    else:
        desired = 500
    best = None
    option_metadata_by_number = {}
    for number, label in options:
        lowered = label.lower()
        if "never mind" in lowered:
            leave_choice = number
            option_metadata_by_number[number] = {"action_kind": "leave", "is_exit": True, "base_score": 12.0, "desired_amount": float(desired)}
            continue
        amount = _extract_cash_amount(label)
        if amount is None:
            option_metadata_by_number[number] = {"action_kind": "borrow", "base_score": 0.0, "desired_amount": float(desired), "actionable": False}
            continue
        score = (0 if amount >= desired else 1, abs(amount - desired), -amount)
        option_metadata_by_number[number] = {
            "action_kind": "borrow",
            "amount": float(amount),
            "desired_amount": float(desired),
            "base_score": max(0.0, 60.0 - score[1] / 50.0 + (6.0 if amount >= desired else 0.0)),
            "actionable": True,
        }
        if best is None or score < best[0]:
            best = (score, number)
    policy_choice = _choose_policy_numeric_option(
        player,
        request_type="loan_decision",
        stable_context_id="loan_borrow_amount",
        menu_options=options,
        option_metadata_by_number=option_metadata_by_number,
        metadata={"debt": 0, "warning_level": 0, "desired_amount": desired},
    )
    if policy_choice is not None:
        return policy_choice
    if best is not None:
        return _record_numeric_menu_trace(
            player,
            request_type="loan_decision",
            stable_context_id="loan_borrow_amount",
            menu_options=options,
            chosen_number=best[1],
            reason=f"borrow_amount_target:{desired}",
            confidence=0.72,
            metadata={"desired_amount": desired},
        )
    fallback = leave_choice if leave_choice is not None else (options[-1][0] if options else 1)
    return _record_numeric_menu_trace(
        player,
        request_type="loan_decision",
        stable_context_id="loan_borrow_amount",
        menu_options=options,
        chosen_number=fallback,
        reason="borrow_amount_exit",
        confidence=0.48,
        metadata={"desired_amount": desired},
    )


def _choose_loan_repay_amount(options, player):
    leave_choice = None
    debt = 0 if player is None else int(player.get_loan_shark_debt())
    balance = 0 if player is None else player.get_balance()
    warning = 0 if player is None or not hasattr(player, "get_loan_shark_warning_level") else int(player.get_loan_shark_warning_level())
    reserve = _cash_safety_reserve(player, 88) if player is not None else 0
    repayment_capacity = max(0, balance - reserve)
    best_partial = None
    option_metadata_by_number = {}
    for number, label in options:
        lowered = label.lower()
        if "never mind" in lowered:
            leave_choice = number
            option_metadata_by_number[number] = {"action_kind": "leave", "is_exit": True, "base_score": 12.0}
            continue
        amount = _extract_cash_amount(label)
        if amount is None:
            option_metadata_by_number[number] = {"action_kind": "repay", "base_score": 0.0, "actionable": False}
            continue
        if "pay in full" in lowered and repayment_capacity >= debt and debt > 0:
            option_metadata_by_number[number] = {"action_kind": "repay", "amount": float(debt), "base_score": 100.0, "actionable": True}
            continue
        if "pay half" in lowered and repayment_capacity >= max(100, debt // 2):
            if warning >= 1 or debt <= max(500, balance // 3):
                option_metadata_by_number[number] = {"action_kind": "repay", "amount": float(max(100, debt // 2)), "base_score": 80.0, "actionable": True}
                continue
        if amount <= repayment_capacity:
            score = (0 if warning >= 2 else 1, -amount)
            option_metadata_by_number[number] = {
                "action_kind": "repay",
                "amount": float(amount),
                "base_score": 64.0 + (10.0 if warning >= 2 else 0.0) + min(12.0, amount / 250.0),
                "actionable": True,
            }
            if best_partial is None or score < best_partial[0]:
                best_partial = (score, number)
        else:
            option_metadata_by_number[number] = {"action_kind": "repay", "amount": float(amount), "base_score": 0.0, "actionable": False}
    policy_choice = _choose_policy_numeric_option(
        player,
        request_type="loan_decision",
        stable_context_id="loan_repay_amount",
        menu_options=options,
        option_metadata_by_number=option_metadata_by_number,
        metadata={"debt": debt, "warning_level": warning},
    )
    if policy_choice is not None:
        return policy_choice
    if best_partial is not None:
        return _record_numeric_menu_trace(
            player,
            request_type="loan_decision",
            stable_context_id="loan_repay_amount",
            menu_options=options,
            chosen_number=best_partial[1],
            reason="repay_amount_best_partial",
            confidence=0.62,
        )
    fallback = leave_choice if leave_choice is not None else (options[-1][0] if options else 1)
    return _record_numeric_menu_trace(
        player,
        request_type="loan_decision",
        stable_context_id="loan_repay_amount",
        menu_options=options,
        chosen_number=fallback,
        reason="repay_amount_exit",
        confidence=0.48,
    )


def _recent_lower(limit=30):
    return "\n".join(RECENT_TEXT[-limit:]).lower()


def _needs_car(player):
    return player is not None and not player.has_item("Car")


def _adventure_ready(player):
    if player is None:
        return False
    if _needs_doctor(player) or _doctor_visit_is_urgent(player):
        return False
    return (
        player.has_item("Car")
        and player.get_health() >= 65
        and player.get_sanity() >= 35
        and player.get_balance() >= 40
    )


def _choose_adventure_destination(options, player):
    if not _adventure_ready(player):
        return None

    adventure_labels = {label: number for number, label in options if label.startswith("Drive to ")}
    if not adventure_labels:
        return None

    if player.has_item("Animal Whistle") and _companion_count(player) < 5:
        priorities = [
            "Drive to The Road",
            "Drive to The Woodlands",
            "Drive to The Beach",
            "Drive to The City",
            "Drive to The Swamp",
            "Drive to The Ocean Depths",
        ]
    elif player.has_item("Rusty Compass") or player.has_item("Golden Compass"):
        priorities = [
            "Drive to The Woodlands",
            "Drive to The City",
            "Drive to The Beach",
            "Drive to The Swamp",
            "Drive to The Road",
            "Drive to The Ocean Depths",
        ]
    elif player.has_item("Quiet Sneakers") or player.has_item("Quiet Bunny Slippers"):
        priorities = [
            "Drive to The Woodlands",
            "Drive to The Road",
            "Drive to The Beach",
            "Drive to The Swamp",
            "Drive to The City",
            "Drive to The Ocean Depths",
        ]
    elif player.get_rank() <= 2 or player.get_health() < 80 or player.get_sanity() < 50:
        priorities = [
            "Drive to The Road",
            "Drive to The Woodlands",
            "Drive to The Beach",
            "Drive to The Swamp",
            "Drive to The City",
            "Drive to The Ocean Depths",
        ]
    else:
        priorities = [
            "Drive to The Woodlands",
            "Drive to The Beach",
            "Drive to The Swamp",
            "Drive to The City",
            "Drive to The Ocean Depths",
            "Drive to The Road",
        ]

    for label in priorities:
        if label in adventure_labels:
            return adventure_labels[label]

    return next(iter(adventure_labels.values()), None)


def _adapter_yes_no_fallback(prompt_lower, player, cost=None):
    if prompt_lower == "treat yourself to a feast? ($25)":
        if player is None:
            return "no"
        target_cost = 25 if cost is None else cost
        return "yes" if _can_afford_optional_purchase(player, target_cost, 38) and (player.get_health() < 90 or player.get_sanity() < 70) else "no"
    if prompt_lower == "stay and eat? ($200)":
        if player is None:
            return "no"
        target_cost = 200 if cost is None else cost
        return "yes" if _can_afford_optional_purchase(player, target_cost, 66) and (player.get_health() < 60 or player.get_sanity() < 45) else "no"
    if prompt_lower == "pay for the repair? ($100)":
        if player is None:
            return "no"
        target_cost = 100 if cost is None else cost
        return "yes" if _can_afford_optional_purchase(player, target_cost, 78) else "no"
    if prompt_lower == "pay the mechanic? ($150)":
        if player is None:
            return "no"
        target_cost = 150 if cost is None else cost
        return "yes" if _can_afford_optional_purchase(player, target_cost, 82) else "no"
    if prompt_lower == "pay the $500 fine?":
        if player is None:
            return "no"
        target_cost = 500 if cost is None else cost
        return "yes" if player.get_balance() - target_cost >= 500 else "no"
    if prompt_lower == "pay to remove the boot? ($300)":
        if player is None:
            return "no"
        target_cost = 300 if cost is None else cost
        return "yes" if player.get_balance() - target_cost >= 500 else "no"
    if prompt_lower == "pay to get your car back? ($800)":
        if player is None:
            return "no"
        target_cost = 800 if cost is None else cost
        return "yes" if player.get_balance() - target_cost >= 700 else "no"

    if prompt_lower == "drive to the hospital to visit her? ($100 gas money)":
        if player is None or cost is None:
            return "no"
        return "yes" if _can_afford_optional_purchase(player, cost, 74) else "no"

    if prompt_lower == "take the cat to a vet? ($200)":
        if player is None or cost is None:
            return "no"
        return "yes" if _can_afford_optional_purchase(player, cost, 88) else "no"

    if prompt_lower == "buy it for $50?":
        if player is None or cost is None:
            return "no"
        return "yes" if _can_afford_optional_purchase(player, cost, 72) else "no"

    if prompt_lower == "pay the ticket?":
        if player is None:
            return "no"
        if cost is None:
            cost = 75
        return "yes" if _can_afford_optional_purchase(player, cost, 64) else "no"

    return None


def _choose_inline_choice(inline_choices, player, prompt=""):
    if not inline_choices:
        return "1"

    prompt_lower = (prompt or "").lower()
    recent = _recent_lower(80)
    event_request = DecisionRequest(
        request_type="event_inline",
        stable_context_id="inline_choice_prompt",
        game_state=_current_game_state(player, context_tag="inline_choice_prompt").to_dict(),
        normalized_options=_structured_options(tuple(inline_choices), prefix="event_inline"),
        raw_prompt_text=prompt or "",
        raw_recent_text=tuple(RECENT_TEXT[-20:]),
        metadata={
            "cycle": CURRENT_CYCLE,
            "prompt_lower": prompt_lower,
            "recent_lower": recent,
        },
    )
    event_plan = choose_strategic_goal(_current_game_state(player, context_tag="inline_choice_prompt"))
    event_choice, event_trace = choose_event_inline_choice(event_request, event_plan)
    if event_choice is not None and event_trace is not None:
        _record_decision_request(event_request)
        _record_decision_trace(event_trace)
        return event_choice

    return str(inline_choices[0]).strip().lower()


def _should_buy_car_repair(player, cost, recent):
    if player is None or not _needs_car(player):
        return False

    balance = player.get_balance()

    def can_pay(target_cost, priority):
        if target_cost is None:
            return False
        return _can_afford_optional_purchase(player, target_cost, priority)

    if "frank" in recent:
        if not player.has_met("Tom Event"):
            return False
        target_cost = cost if cost is not None else 100
        if target_cost <= 100 and balance >= target_cost:
            return True
        return can_pay(target_cost, 92)
    if "tom" in recent:
        target_cost = cost if cost is not None else 250
        if target_cost <= balance and balance >= 200:
            return True
        if cost is not None and balance < cost:
            return True
        if can_pay(cost, 85):
            return True
        return balance >= 200
    if "stuart" in recent or "oswald" in recent:
        target_cost = cost if cost is not None else 900
        if target_cost <= balance and balance >= 850:
            return True
        if balance < target_cost:
            return True
        return can_pay(target_cost, 75)
    if "i can fix this up for like" in recent:
        target_cost = cost if cost is not None else 100
        if target_cost <= 100 and balance >= target_cost:
            return True
        return can_pay(target_cost, 92)
    if "this thing's busted alright" in recent or "could ya do" in recent:
        target_cost = cost if cost is not None else 250
        if target_cost <= balance and balance >= 200:
            return True
        if "could ya do" not in recent and cost is not None and balance < cost:
            return True
        if can_pay(target_cost, 85):
            return True
        return balance >= 200
    if "get you back on the road" in recent or "fix your limousine" in recent:
        target_cost = cost if cost is not None else 900
        if target_cost <= balance and balance >= 850:
            return True
        if balance < target_cost:
            return True
        return can_pay(target_cost, 75)

    if cost is None or balance < cost:
        return False

    return can_pay(cost, 80)


def _car_progress_reserve(player):
    if player is None or not _needs_car(player):
        return 0

    balance = player.get_balance()
    day = getattr(player, "_day", 1)

    if day <= 2 and balance < 150:
        return 0
    if day <= 3 and balance < 100:
        return 0

    if balance >= 260:
        reserve = 200
    elif balance >= 180:
        reserve = 150
    elif balance >= 120:
        reserve = 0 if day < 4 else 50
    elif balance >= 75:
        reserve = 0 if day < 4 else 25
    else:
        reserve = 0

    return min(balance, reserve)


def _mechanic_purchase_reserve(player):
    if player is None or not _needs_car(player):
        return 0

    balance = player.get_balance()
    day = getattr(player, "_day", 1)
    reserve = 0

    if not player.has_met("Tom Event"):
        if balance >= 200:
            reserve = max(reserve, 200)
    elif not player.has_met("Frank Event") and balance >= 200:
        reserve = max(reserve, 200)
    if not player.has_met("Oswald Event") and balance >= 800:
        reserve = max(reserve, 850)

    return min(balance, reserve)


def _known_car_repair_reserve(player):
    if player is None or not _needs_car(player):
        return 0

    balance = player.get_balance()
    reserve = 0

    if player.has_met("Frank"):
        reserve = max(reserve, 100)
    if player.has_met("Tom"):
        reserve = max(reserve, 180)
    if player.has_met("Oswald"):
        reserve = max(reserve, 900)

    return min(balance, reserve)


def _wants_pawn_cashout(player):
    planned_sales = _planned_pawn_sales(player)
    if player is None or not planned_sales:
        return False

    pawn_gap = _days_since_location(player, "shop:pawn_shop")
    if pawn_gap == 0:
        return False

    if player.has_item("Car") and player.get_health() >= 60 and player.get_sanity() >= 30:
        if _wants_marvin_run(player):
            return False
        if _wants_adventure_run(player):
            return False

    balance = player.get_balance()
    sell_value = _sellable_collectible_value(player)
    target = _rank_target(balance)
    marvin_priority = _best_marvin_affordable_priority(player) if _has_marvin_access(player) else 0
    if _wants_doctor_visit(player) and balance + sell_value >= _doctor_cash_reserve(player):
        return True
    if (
        player.has_item("Car")
        and _has_marvin_access(player)
        and player.get_rank() <= 1
        and player.get_health() >= 54
        and player.get_sanity() >= 28
        and marvin_priority >= 60
        and balance >= 1400
    ):
        return False
    if (
        player.has_item("Car")
        and _has_marvin_access(player)
        and player.get_rank() <= 1
        and player.get_health() >= 54
        and player.get_sanity() >= 28
        and balance + sell_value >= 1800
    ):
        return balance < 1400 and sell_value >= 250
    if player.has_item("Car") and pawn_gap is not None and pawn_gap <= 2 and balance >= 1200:
        return False
    if player.has_item("Car") and (player.get_health() < 70 or player.get_sanity() < 35) and sell_value >= 100:
        return True
    if _needs_car(player):
        return balance < 275 or balance + sell_value >= 250
    if player.get_rank() == 0:
        return balance < 900 or balance + sell_value >= min(1000, target)
    if player.get_rank() == 1 and not player.has_item("Map"):
        return balance < 1800 or balance + sell_value >= 5000
    return balance < 300 or balance + sell_value >= target


def _poverty_escape_loan_mode(player):
    if player is None or not player.has_item("Car"):
        return False
    if _wants_doctor_visit(player) or _doctor_visit_is_urgent(player):
        return False
    if not player.has_met("Vinnie"):
        return False
    if int(player.get_loan_shark_debt()) > 0:
        return False
    if _fraudulent_cash_amount(player) > 0:
        return False

    balance = player.get_balance()
    edge_score = _blackjack_edge_score(player)
    rank = int(player.get_rank())

    if player.get_health() < 48 or player.get_sanity() < 26:
        return False
    if edge_score < 2:
        return False

    if rank == 0:
        return balance < 900
    if rank == 1 and not player.has_item("Map"):
        return balance < 3000
    return False


def _wants_loan_shark_run(player):
    if player is None or not player.has_item("Car"):
        return False
    if _doctor_visit_is_urgent(player):
        return False
    if not player.has_met("Vinnie"):
        return False

    balance = player.get_balance()
    debt = int(player.get_loan_shark_debt())
    warning = int(player.get_loan_shark_warning_level()) if hasattr(player, "get_loan_shark_warning_level") else 0
    fake_cash = _fraudulent_cash_amount(player)
    wants_doctor = _wants_doctor_visit(player)
    loan_gap = _days_since_location(player, "shop:loan_shark")
    if loan_gap == 0:
        return False
    if loan_gap is not None and loan_gap <= (2 if debt > 0 else 4):
        return False

    if _poverty_escape_loan_mode(player):
        return True

    reserve = _cash_safety_reserve(player, 88)
    repayment_capacity = max(0, balance - reserve)

    if debt > 0:
        if repayment_capacity >= debt:
            return True
        if warning >= 2 and repayment_capacity >= min(100, debt):
            return True
        if warning >= 1 and repayment_capacity >= max(100, debt // 2):
            return True
        return False

    if fake_cash > 0:
        return False

    if balance < 500:
        return True
    if player.get_rank() <= 0 and balance < 900 and player.get_health() >= 48 and player.get_sanity() >= 24:
        return True

    edge_score = _blackjack_edge_score(player)
    if player.get_health() < 42 or player.get_sanity() < 22:
        return False
    if wants_doctor:
        if player.has_item("Real Insurance"):
            if balance >= 800 and edge_score >= 2:
                return True
            return False
        if player.has_item("Faulty Insurance"):
            if balance >= 700 and edge_score >= 3:
                return True
            return False
        if balance >= max(120, _doctor_heal_cost_estimate(player)):
            return False
        if edge_score < 4:
            return False
    if _marvin_loan_plan(player) is not None:
        return True
    if _has_marvin_access(player) and _best_marvin_affordable_priority(player) < 84 and balance < 6000 and edge_score >= 3:
        return True
    if player.get_rank() == 0:
        if edge_score < 2:
            return False
        if balance < 150:
            return True
        if balance < 325:
            return True
        if balance < 900:
            return True
        if balance < 1800 and edge_score >= 3:
            return True
        return balance < 1400 and edge_score >= 4
    if player.get_rank() == 1 and not player.has_item("Map"):
        return balance < 3600 and edge_score >= 3 and player.get_sanity() >= 30
    return balance < max(3600, _rank_floor(balance)) and edge_score >= 3


def _has_adventure_utility(player):
    if player is None:
        return False
    return any(
        player.has_item(item_name)
        for item_name in [
            "Animal Whistle",
            "Quiet Sneakers",
            "Quiet Bunny Slippers",
            "Rusty Compass",
            "Golden Compass",
        ]
    )


def _wants_adventure_run(player):
    if not _adventure_ready(player):
        return False
    if _wants_doctor_visit(player) or _wants_store_run(player):
        return False

    balance = player.get_balance()
    floor = _rank_floor(balance)
    rank = int(player.get_rank())

    if rank <= 0:
        return False
    adventure_gap = _days_since_location(
        player,
        "adventure:road",
        "adventure:woodlands",
        "adventure:swamp",
        "adventure:beach",
        "adventure:ocean_depths",
        "adventure:city",
    )
    if adventure_gap == 0:
        return False
    utility_push = _has_adventure_utility(player)
    if adventure_gap is not None and adventure_gap <= 1:
        return False
    if adventure_gap is not None and adventure_gap <= 2 and rank < 4 and not utility_push:
        return False
    whistle_push = player.has_item("Animal Whistle") and _companion_count(player) < 5
    if rank == 1 and not whistle_push:
        if not utility_push:
            return False
        return balance >= max(850, floor - 250) and player.get_health() >= 60 and player.get_sanity() >= 30
    if rank == 1 and whistle_push:
        return balance >= max(750, floor - 300) and player.get_health() >= 60 and player.get_sanity() >= 30
    if rank == 2:
        if utility_push:
            return balance >= max(600, floor - 650) and player.get_health() >= 58 and player.get_sanity() >= 26
        return balance >= floor and player.get_health() >= 65 and player.get_sanity() >= 32
    return balance >= floor + 1000 and player.get_health() >= 68 and player.get_sanity() >= 36


def _wants_map_unlock_window(player):
    if player is None:
        return False
    return (
        player.has_item("Car")
        and not _has_marvin_access(player)
        and int(player.get_rank()) <= 1
        and player.get_health() >= 55
        and player.get_sanity() >= 35
    )


def _choose_progression_destination(labels, options, player):
    if player is None or not player.has_item("Car"):
        return None

    day = getattr(player, "_day", 1)
    adventure_choice = _choose_adventure_destination(options, player) if _wants_adventure_run(player) else None
    adventure_push = adventure_choice is not None and _has_adventure_utility(player)

    mechanic_progression_choice = _choose_mechanic_progression_destination(labels, player)
    mechanic_bootstrap = (
        mechanic_progression_choice is not None
        and hasattr(player, "get_mechanic_visits")
        and player.get_mechanic_visits() < 3
    )
    marvin_choice = labels.get("Marvin's Mystical Merchandise") if _wants_marvin_run(player) else None
    marvin_bootstrap = marvin_choice is not None and _marvin_bootstrap_window(player)
    marvin_priority_push = (
        marvin_choice is not None
        and (
            player.get_rank() >= 1
            or _marvin_loan_plan(player) is not None
            or _best_marvin_affordable_priority(player) >= 80
            or marvin_bootstrap
        )
    )
    upgrade_choice = labels.get("Oswald's Optimal Outoparts") if _wants_upgrade_run(player) else None
    loan_choice = labels.get("Vinnie's Back Alley Loans") if _wants_loan_shark_run(player) else None
    marvin_loan_plan = _marvin_loan_plan(player)
    poverty_loan_push = loan_choice is not None and _poverty_escape_loan_mode(player)
    store_choice = labels.get("Convenience Store") if _wants_store_run(player) else None
    doctor_choice = labels.get("Doctor's Office") if _wants_doctor_visit(player) else None

    if loan_choice is not None and marvin_loan_plan is not None:
        ordered = [loan_choice, marvin_choice, mechanic_progression_choice, adventure_choice, upgrade_choice, store_choice, doctor_choice]
    elif poverty_loan_push:
        ordered = [loan_choice, mechanic_progression_choice, marvin_choice, store_choice, adventure_choice, upgrade_choice, doctor_choice]
    elif marvin_choice is not None and (_best_marvin_affordable_priority(player) >= 84 or marvin_bootstrap):
        ordered = [marvin_choice, mechanic_progression_choice, adventure_choice, upgrade_choice, loan_choice, store_choice, doctor_choice]
    elif player.get_rank() >= 2:
        if mechanic_bootstrap:
            ordered = [mechanic_progression_choice, marvin_choice, upgrade_choice, loan_choice, adventure_choice, store_choice, doctor_choice]
        else:
            rotation = day % 3
            if rotation == 1:
                ordered = [mechanic_progression_choice, marvin_choice, upgrade_choice, loan_choice, adventure_choice, store_choice, doctor_choice]
            elif rotation == 2:
                ordered = [marvin_choice, mechanic_progression_choice, upgrade_choice, loan_choice, adventure_choice, store_choice, doctor_choice]
            else:
                ordered = [upgrade_choice, mechanic_progression_choice, marvin_choice, loan_choice, adventure_choice, store_choice, doctor_choice]
            if adventure_push:
                ordered = [marvin_choice, adventure_choice, mechanic_progression_choice, upgrade_choice, loan_choice, store_choice, doctor_choice]
    else:
        if mechanic_bootstrap:
            if marvin_priority_push:
                ordered = [marvin_choice, mechanic_progression_choice, loan_choice, store_choice, adventure_choice, upgrade_choice, doctor_choice]
            else:
                ordered = [mechanic_progression_choice, marvin_choice, loan_choice, store_choice, adventure_choice, upgrade_choice, doctor_choice]
        elif marvin_choice is not None:
            ordered = [marvin_choice, mechanic_progression_choice, adventure_choice, loan_choice, store_choice, upgrade_choice, doctor_choice]
        elif adventure_push:
            ordered = [mechanic_progression_choice, adventure_choice, loan_choice, store_choice, upgrade_choice, doctor_choice]
        else:
            ordered = [mechanic_progression_choice, loan_choice, marvin_choice, store_choice, adventure_choice, upgrade_choice, doctor_choice]

    for choice in ordered:
        if choice is not None:
            return choice
    return None


def _legacy_choose_destination(options, player):
    labels = {label: number for number, label in options}

    medical_choice = _medical_destination_label(player)
    if medical_choice in labels and _doctor_visit_is_urgent(player):
        return labels[medical_choice]

    if medical_choice in labels and (_wants_doctor_visit(player) or _wants_witch_heal(player)):
        return labels[medical_choice]

    if _needs_recovery_day(player) and "Stay Home" in labels:
        return labels["Stay Home"]

    progression_choice = _choose_progression_destination(labels, options, player)
    if progression_choice is not None:
        progression_label = next((label for label, number in labels.items() if number == progression_choice), "")
        if (
            "Marvin's Mystical Merchandise" == progression_label
            or progression_label.startswith("Drive to ")
        ):
            return progression_choice

    if "Grimy Gus's Pawn Emporium" in labels and _wants_pawn_cashout(player):
        return labels["Grimy Gus's Pawn Emporium"]

    if medical_choice in labels:
        return labels[medical_choice]

    if progression_choice is not None:
        return progression_choice

    if "Convenience Store" in labels and _wants_store_run(player):
        return labels["Convenience Store"]

    if "Stay Home" in labels:
        return labels["Stay Home"]

    return options[-1][0] if options else 1


def _planner_choose_destination(options, player):
    if player is None or not options:
        return None

    menu_options = list(options)
    game_state = _current_game_state(player, menu_options=menu_options, context_tag="route_select")
    plan = choose_strategic_goal(game_state)
    plan_top_score = max(plan.scores.values(), default=0.0)
    store_goal_score = float(plan.scores.get("restock_supplies", 0.0) or 0.0)
    pawn_goal_score = float(plan.scores.get("cashout_pawn_inventory", 0.0) or 0.0)
    store_spend = game_state.store_target_spend
    pawn_value = game_state.pawn_sellable_value
    loan_pressure = max(
        int(player.get_loan_shark_debt()) if hasattr(player, "get_loan_shark_debt") else 0,
        (int(player.get_loan_shark_warning_level()) if hasattr(player, "get_loan_shark_warning_level") else 0) * 200,
    )
    mechanic_urgency = 0
    if _wants_mechanic_progression_run(player):
        mechanic_urgency = 80 - min(45, int(getattr(player, "get_mechanic_visits", lambda: 0)() or 0) * 15)
        if _needs_oswald_attention(player):
            mechanic_urgency += 28
    upgrade_urgency = 0
    if _wants_upgrade_run(player):
        upgrade_candidate = _best_upgrade_candidate(player)
        upgrade_urgency = int(upgrade_candidate[0]) if upgrade_candidate is not None else 52
    marvin_priority = 0
    if _wants_marvin_run(player):
        marvin_priority = _best_marvin_affordable_priority(player)
    adventure_readiness = 0
    if _wants_adventure_run(player):
        adventure_readiness = min(100, max(30, int(player.get_rank()) * 20 + max(0, player.get_health() - 60) // 2 + max(0, player.get_sanity() - 35) // 2))
    wants_store = (
        plan.goal in {
        "restock_supplies",
        "preserve_companion_roster",
        "reduce_fatigue_pressure",
        "stabilize_health",
        "bootstrap_blackjack_edge",
        }
        or store_goal_score >= max(58.0, plan_top_score - 12.0)
    ) and game_state.store_candidate_count > 0
    wants_pawn = (
        plan.goal in {
        "cashout_pawn_inventory",
        "reduce_debt_risk",
        "contain_debt_escalation",
        "acquire_car",
        "stabilize_health",
        }
        or pawn_goal_score >= max(60.0, plan_top_score - 12.0)
    ) and game_state.pawn_planned_sale_value > 0
    route_labels = {label for _number, label in menu_options}
    defer_doctor = _defer_doctor_for_no_car_progression(player, route_labels, planned_goal=plan.goal)
    normalized_options = tuple(
        DecisionOption(
            option_id=f"route:{number}",
            label=label,
            value=number,
            metadata={"number": number},
        )
        for number, label in menu_options
    )
    request = DecisionRequest(
        request_type="route_select",
        stable_context_id="afternoon_destination",
        game_state=game_state.to_dict(),
        normalized_options=normalized_options,
        raw_recent_text=tuple(RECENT_TEXT[-20:]),
        metadata={
            "cycle": CURRENT_CYCLE,
            "day": game_state.day,
            "urgent_medical": _doctor_visit_is_urgent(player),
            "needs_recovery_day": _needs_recovery_day(player),
            "medical_choice": _medical_destination_label(player),
            "wants_doctor": _wants_doctor_visit(player) and not defer_doctor,
            "wants_witch": _wants_witch_heal(player),
            "wants_marvin": _wants_marvin_run(player),
            "wants_loan": _wants_loan_shark_run(player),
            "wants_store": wants_store,
            "wants_adventure": _wants_adventure_run(player),
            "wants_upgrade": _wants_upgrade_run(player),
            "wants_mechanic": _wants_mechanic_progression_run(player),
            "wants_pawn": wants_pawn,
            "store_spend": store_spend,
            "pawn_value": pawn_value,
            "pawn_planned_sale_value": game_state.pawn_planned_sale_value,
            "store_candidate_count": game_state.store_candidate_count,
            "planner_goal": plan.goal,
            "store_goal_score": store_goal_score,
            "pawn_goal_score": pawn_goal_score,
            "loan_pressure": loan_pressure,
            "mechanic_urgency": mechanic_urgency,
            "upgrade_urgency": upgrade_urgency,
            "marvin_priority": marvin_priority,
            "adventure_readiness": adventure_readiness,
            "has_car": game_state.has_car,
            "has_marvin_access": game_state.has_marvin_access,
            "mechanic_visits": game_state.mechanic_visits,
            "rank": game_state.rank,
        },
    )
    _record_decision_request(request)
    choice, trace = choose_route_option(request, plan)
    if choice is None:
        trace.metadata["route_outcome"] = "no_choice"
    else:
        planner_applied = trace.confidence >= 0.55
        trace.metadata["planner_applied"] = planner_applied
        trace.metadata["route_outcome"] = "applied" if planner_applied else "suppressed"
    _record_decision_trace(trace)
    if choice is None:
        return None
    if trace.confidence < 0.55:
        return None
    return int(choice.value)


def _choose_destination(options, player):
    labels = {label: number for number, label in options}
    medical_choice = _medical_destination_label(player)
    defer_doctor = _defer_doctor_for_no_car_progression(player, labels.keys())

    if medical_choice in labels and _doctor_visit_is_urgent(player):
        _record_route_interrupt_trace(player, labels[medical_choice], f"urgent medical override -> {medical_choice}", "survive_emergency", "urgent_medical")
        return labels[medical_choice]

    if medical_choice in labels and not defer_doctor and (_wants_doctor_visit(player) or _wants_witch_heal(player)):
        forced_goal = "stabilize_health" if medical_choice == "Doctor's Office" else "stabilize_sanity"
        _record_route_interrupt_trace(player, labels[medical_choice], f"medical stabilization override -> {medical_choice}", forced_goal, "medical_stabilization")
        return labels[medical_choice]

    allow_recovery_override = True
    if _needs_recovery_day(player) and player is not None:
        recovery_state = _current_game_state(player, menu_options=options, context_tag="recovery_override_check")
        recovery_plan = choose_strategic_goal(recovery_state)
        recovery_injuries = _injury_names(player)
        recovery_statuses = _status_names(player)
        severe_recovery_injuries = {"ruptured spleen", "concussion", "broken ribs", "punctured lung"}
        severe_recovery_statuses = {
            "appendicitis", "anaphylaxis", "blood pressure crisis", "dvt", "gangrene", "heat stroke",
            "hypothermia", "kidney stones", "needle exposure", "pancreatitis", "pneumonia",
            "possible rabies", "seizure disorder", "sepsis", "severe asthma", "severe dehydration",
            "staph infection", "tetanus", "uncontrolled diabetes", "waterborne illness",
        }
        mild_recovery_pressure = (
            player.get_health() >= 60
            and player.get_sanity() >= 28
            and len(recovery_injuries) <= 2
            and len(recovery_statuses) <= 2
            and not any(injury in severe_recovery_injuries for injury in recovery_injuries)
            and not any(status in severe_recovery_statuses for status in recovery_statuses)
            and _doctor_need_score(player) < 84
        )
        store_window_open = (
            recovery_plan.goal == "restock_supplies"
            and "Convenience Store" in labels
            and recovery_state.store_target_spend > 0
        )
        pawn_window_open = (
            recovery_plan.goal == "cashout_pawn_inventory"
            and "Grimy Gus's Pawn Emporium" in labels
            and recovery_state.pawn_planned_sale_value > 0
        )
        marvin_window_open = (
            recovery_plan.goal == "exploit_marvin"
            and "Marvin's Mystical Merchandise" in labels
            and recovery_state.has_marvin_access
            and _best_marvin_affordable_priority(player) > 0
        )
        loan_window_open = (
            recovery_plan.goal in {"acquire_car", "reduce_debt_risk", "contain_debt_escalation"}
            and "Vinnie's Back Alley Loans" in labels
            and player.get_health() >= 50
            and player.get_sanity() >= 30
        )
        mechanic_window_open = (
            recovery_plan.goal == "acquire_car"
            and any(
                label in labels
                for label in (
                    "Trusty Tom's Trucks and Tires",
                    "Filthy Frank's Flawless Fixtures",
                    "Oswald's Optimal Outoparts",
                )
            )
        )
        mild_no_car_medical_clutter = (
            player.get_health() >= 56
            and player.get_sanity() >= 34
            and len(recovery_injuries) <= 1
            and len(recovery_statuses) <= 3
            and not any(injury in severe_recovery_injuries for injury in recovery_injuries)
            and not any(status in severe_recovery_statuses for status in recovery_statuses)
            and _doctor_need_score(player) < 72
        )
        no_car_recovery_push = (
            recovery_plan.goal == "acquire_car"
            and _needs_car(player)
            and not _stranded_no_car_mode(player)
            and (
                (
                    player.get_health() >= 50
                    and player.get_sanity() >= 28
                    and len(recovery_injuries) <= 1
                    and len(recovery_statuses) <= 2
                    and not any(injury in severe_recovery_injuries for injury in recovery_injuries)
                    and not any(status in severe_recovery_statuses for status in recovery_statuses)
                    and _doctor_need_score(player) < 96
                )
                or mild_no_car_medical_clutter
            )
            and (mechanic_window_open or store_window_open or pawn_window_open or loan_window_open)
        )
        if mild_recovery_pressure and (store_window_open or pawn_window_open or marvin_window_open):
            allow_recovery_override = False
        if no_car_recovery_push:
            allow_recovery_override = False

    if allow_recovery_override and _needs_recovery_day(player) and "Stay Home" in labels:
        _record_route_interrupt_trace(player, labels["Stay Home"], "recovery-day override -> Stay Home", "stabilize_health", "recovery_day")
        return labels["Stay Home"]

    planner_choice = _planner_choose_destination(options, player)
    if planner_choice is not None:
        return planner_choice
    return _legacy_choose_destination(options, player)


def _choose_store_item(options, player):
    leave_choice = None
    ranked_choices = {item_name: priority for priority, _price, item_name in _store_purchase_candidates(player)}
    best_choice = None
    car_items = {"Spare Tire", "Tire Patch Kit", "Fix-a-Flat", "Tool Kit", "OBD Scanner", "Portable Battery Charger", "Jumper Cables", "Motor Oil", "Brake Fluid", "Spare Fuses"}
    medical_items = {"LifeAlert", "First Aid Kit", "Road Flares", "Bug Spray", "Flashlight", "Duct Tape", "Water Bottles", "Pocket Knife"}
    blackjack_items = {"Worn Map", "Lucky Rabbit Foot", "Lucky Penny", "Silver Flask", "Antique Pocket Watch"}
    option_metadata_by_number = {}
    for number, label in options:
        if "I'm not buying anything" in label:
            leave_choice = number
            option_metadata_by_number[number] = {"is_exit": True, "base_score": 0.0, "category": "exit"}
            continue
        item_name = label.split(" - ", 1)[0].strip()
        priority = ranked_choices.get(item_name, 0)
        price = _extract_cash_amount(label) or 0
        if item_name in car_items:
            category = "car"
        elif item_name in medical_items:
            category = "medical"
        elif _store_food_priority(item_name, player) > 0:
            category = "food"
        elif item_name in blackjack_items:
            category = "blackjack"
        else:
            category = "generic"
        option_metadata_by_number[number] = {
            "item_name": item_name,
            "priority": float(priority),
            "base_score": float(priority),
            "price": float(price),
            "category": category,
        }
        if priority <= 0:
            continue
        if best_choice is None or priority > best_choice[0]:
            best_choice = (priority, number, item_name)
    policy_choice = _choose_policy_numeric_option(
        player,
        request_type="purchase_select",
        stable_context_id="convenience_store_menu",
        menu_options=options,
        option_metadata_by_number=option_metadata_by_number,
        metadata={"needs_recovery_day": _needs_recovery_day(player)},
    )
    if policy_choice is not None:
        return policy_choice
    if best_choice is not None:
        return _record_numeric_menu_trace(
            player,
            request_type="purchase_select",
            stable_context_id="convenience_store_menu",
            menu_options=options,
            chosen_number=best_choice[1],
            reason=f"store_priority:{best_choice[2]}",
            confidence=0.68,
        )
    fallback = leave_choice if leave_choice is not None else (options[-1][0] if options else 1)
    return _record_numeric_menu_trace(
        player,
        request_type="purchase_select",
        stable_context_id="convenience_store_menu",
        menu_options=options,
        chosen_number=fallback,
        reason="store_menu_exit",
        confidence=0.5,
    )


def _choose_companion_interaction(options, player):
    if not options:
        return 1

    if _should_group_with_companions(player):
        for number, label in options:
            lowered = label.lower()
            if "spend time with all" in lowered:
                return _record_numeric_menu_trace(
                    player,
                    request_type="menu_select",
                    stable_context_id="companion_menu",
                    menu_options=options,
                    chosen_number=number,
                    reason="group_companion_time",
                    confidence=0.7,
                )

    for number, label in options:
        lowered = label.lower()
        if "skip and head out" in lowered:
            continue
        if "spend time with all" in lowered:
            continue
        return _record_numeric_menu_trace(
            player,
            request_type="menu_select",
            stable_context_id="companion_menu",
            menu_options=options,
            chosen_number=number,
            reason="first_individual_companion",
            confidence=0.54,
        )

    return _record_numeric_menu_trace(
        player,
        request_type="menu_select",
        stable_context_id="companion_menu",
        menu_options=options,
        chosen_number=options[-1][0],
        reason="companion_menu_fallback_exit",
        confidence=0.42,
    )


def _choose_pawn_menu(options, player):
    if _sellable_collectibles(player):
        for number, label in options:
            if "Start selling" in label:
                return _record_numeric_menu_trace(
                    player,
                    request_type="menu_select",
                    stable_context_id="pawn_menu",
                    menu_options=options,
                    chosen_number=number,
                    reason="pawn_start_selling",
                    confidence=0.66,
                )
        for number, label in options:
            if "See what I can sell" in label:
                return _record_numeric_menu_trace(
                    player,
                    request_type="menu_select",
                    stable_context_id="pawn_menu",
                    menu_options=options,
                    chosen_number=number,
                    reason="pawn_view_inventory",
                    confidence=0.6,
                )
    for number, label in options:
        if "Leave" in label:
            return _record_numeric_menu_trace(
                player,
                request_type="menu_select",
                stable_context_id="pawn_menu",
                menu_options=options,
                chosen_number=number,
                reason="pawn_menu_exit",
                confidence=0.5,
            )
    fallback = options[-1][0] if options else 1
    return _record_numeric_menu_trace(
        player,
        request_type="menu_select",
        stable_context_id="pawn_menu",
        menu_options=options,
        chosen_number=fallback,
        reason="pawn_menu_fallback",
        confidence=0.4,
    )


def _choose_pawn_sale_item(options, player):
    prices = {} if player is None else dict(player.get_collectible_prices())
    leave_choice = None
    best_choice = None
    for number, label in options:
        lowered = label.lower()
        if "never mind" in lowered or "leave" in lowered:
            leave_choice = number
            continue
        matched_name = None
        matched_price = 0
        for item_name, price in prices.items():
            if item_name.lower() in lowered and price >= matched_price:
                matched_name = item_name
                matched_price = price
        if matched_name is None:
            if best_choice is None:
                best_choice = (0, number)
            continue
        if best_choice is None or matched_price > best_choice[0]:
            best_choice = (matched_price, number, matched_name)
    if best_choice is not None:
        return _record_numeric_menu_trace(
            player,
            request_type="menu_select",
            stable_context_id="pawn_sale_menu",
            menu_options=options,
            chosen_number=best_choice[1],
            reason=f"pawn_sale_value:{best_choice[2]}",
            confidence=0.7,
        )
    fallback = leave_choice if leave_choice is not None else (options[-1][0] if options else 1)
    return _record_numeric_menu_trace(
        player,
        request_type="menu_select",
        stable_context_id="pawn_sale_menu",
        menu_options=options,
        chosen_number=fallback,
        reason="pawn_sale_exit",
        confidence=0.5,
    )


def _looks_like_pawn_menu(options):
    labels = {label.lower() for _number, label in options}
    return (
        any("start selling" in label for label in labels)
        and any("see what i can sell" in label for label in labels)
    )


def _decide_yes_no(prompt=""):
    player = CURRENT_PLAYER
    prompt_lower = (prompt or "").lower()
    recent = _recent_lower(80)
    recent_mechanic = _recent_lower(20)
    cost = _extract_cash_amount(prompt, recent)

    def finalize(answer, reason, confidence=0.62):
        _record_structured_trace(
            player,
            request_type="yes_no",
            stable_context_id="yes_no_prompt",
            chosen_action=answer,
            reason=reason,
            confidence=confidence,
            prompt=prompt,
            options=("yes", "no"),
            metadata={
                "cost": cost,
                "prompt_lower": prompt_lower,
            },
        )
        return answer

    mechanic_answer = _decide_mechanic_intro_response(player, recent_mechanic, prompt, source="yesno")
    if mechanic_answer is not None:
        return finalize(mechanic_answer, "mechanic_intro_offer")

    event_request, event_plan = _build_event_policy_request(
        player,
        request_type="yes_no",
        stable_context_id="yes_no_prompt",
        options=("yes", "no"),
        prompt=prompt,
        metadata={
            "prompt_lower": prompt_lower,
            "recent_lower": recent,
            "cost": cost,
        },
    )
    event_answer, event_trace = choose_event_yes_no(event_request, event_plan)
    if event_answer is not None and event_trace is not None:
        _record_decision_request(event_request)
        _record_decision_trace(event_trace)
        return event_answer

    event_override = _adapter_yes_no_fallback(prompt_lower, player, cost)
    if event_override is not None:
        return finalize(event_override, "adapter_budget_gate")

    if "spend time with your companions" in prompt_lower:
        answer = "yes" if player is not None and (_companion_count(player) >= 3 or player.get_sanity() < 55 or player.get_health() < 70) else "no"
        return finalize(answer, "companion_recovery_gate")
    if any(
        re.search(rf"\b{re.escape(phrase)}\b", recent)
        for phrase in [
            "pistol", "gun", "badge", "questioning", "handcuffs", "police cruiser",
            "loan sharks", "freight truck", "blood covers", "move right now", "i'll be back",
        ]
    ):
        return finalize("no", "threat_context_refusal", 0.88)
    if "companions" in prompt_lower:
        return finalize("no", "companion_prompt_default")
    if "gift wrap" in prompt_lower:
        if player is None:
            return finalize("no", "gift_wrap_without_player")
        dealer_happiness = _dealer_happiness(player)
        in_emergency = player.get_health() < 45 or player.get_sanity() < 20 or not player.has_item("Car")
        if (
            player.get_balance() >= GIFT_WRAP_MIN_BALANCE
            and dealer_happiness < GIFT_WRAP_HAPPINESS_THRESHOLD
            and not in_emergency
        ):
            return finalize("yes", "gift_wrap_for_dealer_happiness")
        return finalize("no", "gift_wrap_not_worth_it")
    if prompt_lower.startswith("sell ") or prompt_lower.startswith("sell the "):
        if "sell whiskers" in prompt_lower or "sell lucky" in prompt_lower:
            return finalize("no", "protect_companion_sale_block")
        planned_sales = {item_name.lower() for item_name in _planned_pawn_sales(player)}
        for item_name in planned_sales:
            if item_name in prompt_lower:
                return finalize("yes", "planned_pawn_sale")
        return finalize("no", "unplanned_sale_block")
    if "continue?" in prompt_lower:
        return finalize("no", "continue_prompt_stop")
    if "heal you" in recent and "witch doctor" in recent:
        answer = "yes" if _wants_witch_heal(player) else "no"
        return finalize(answer, "witch_heal_gate")
    if "purchase any of my powerful potions" in recent or "mood to spend some money on my magic potions" in recent:
        if player is None:
            return finalize("no", "witch_potion_without_player")
        if _flask_count(player) >= 2:
            return finalize("no", "witch_potion_capacity_block")
        answer = "yes" if player.get_balance() >= 12000 else "no"
        return finalize(answer, "witch_potion_budget_gate")
    if _should_buy_car_repair(player, cost, recent):
        return finalize("yes", "car_repair_required", 0.82)
    if _needs_car(player) and any(name in recent for name in ["tom", "frank", "oswald", "stuart"]):
        return finalize("no", "decline_non_viable_car_offer")
    if "do you accept this offer" in recent and "stuart" in recent:
        if cost is None or player is None:
            return finalize("no", "stuart_offer_missing_cost")
        answer = "yes" if player.get_balance() >= cost and cost <= max(90000, int(player.get_balance() * 0.55)) else "no"
        return finalize(answer, "stuart_offer_budget_gate")
    if "whaddya say" in recent or "what do you think" in recent or "you buying" in recent or "you interested" in recent:
        if cost is None or player is None:
            return finalize("no", "offer_missing_budget_context")
        marvin_items = {
            "Pocket Watch", "Lucky Coin", "Gambler's Grimoire", "Faulty Insurance", "Dirty Old Hat", "Golden Watch",
            "Health Indicator", "Delight Indicator", "Worn Gloves", "Tattered Cloak", "Gambler's Chalice",
            "White Feather", "Twin's Locket", "Dealer's Grudge", "Rusty Compass", "Quiet Sneakers",
            "Sneaky Peeky Shades", "Enchanting Silver Bar", "Animal Whistle",
        }
        current_offer = _current_offer_name(recent, marvin_items)
        if current_offer is not None:
            priority = _marvin_item_priority(current_offer, player)
            if priority <= 0:
                return finalize("no", f"marvin_offer_priority_zero:{current_offer}")
            if _can_afford_optional_purchase(player, cost, priority):
                return finalize("yes", f"marvin_offer_affordable:{current_offer}", 0.8)
            if priority >= 90 and player.get_balance() >= cost and player.get_balance() - cost >= max(120, _doctor_cash_reserve(player)):
                return finalize("yes", f"marvin_offer_high_priority:{current_offer}", 0.72)
            return finalize("no", f"marvin_offer_budget_block:{current_offer}")
        must_have = any(name in recent for name in [
            "faulty insurance", "health indicator", "delight indicator", "rusty compass",
            "spare tire", "tire patch kit", "fix-a-flat", "tool kit", "first aid kit",
        ])
        affordable = player.get_balance() >= cost
        conservative = cost <= max(200, int(player.get_balance() * 0.25))
        answer = "yes" if affordable and (must_have or conservative) else "no"
        return finalize(answer, "generic_offer_budget_gate")
    if "pay" in prompt_lower and cost is not None and player is not None:
        if player.get_balance() < cost:
            return finalize("no", "cannot_afford_payment")
        urgent = any(
            phrase in recent
            for phrase in [
                "fix-now-or-die", "before you blow yourself up", "you can't drive like this",
                "carbon monoxide", "severe dehydration", "you need a mechanic", "life or death",
            ]
        )
        if urgent:
            return finalize("yes", "urgent_payment_required", 0.86)
        reserve = max(20, int(player.get_balance() * 0.2))
        answer = "yes" if player.get_balance() - cost >= reserve else "no"
        return finalize(answer, "payment_reserve_gate")
    if player is not None and (player.get_balance() >= 1000 or int(player.get_rank()) >= 1):
        _record_fallback_decision("yesno", prompt, recent, source="high-resource-default")
        return finalize("no", "fallback_high_resource_default", 0.35)
    _record_fallback_decision("yesno", prompt, recent, source="low-resource-default")
    return finalize("yes", "fallback_low_resource_default", 0.3)


def _decide_option(prompt, options):
    player = CURRENT_PLAYER
    prompt_lower = (prompt or "").lower()
    recent = _recent_lower(80)

    def finalize(chosen, reason, confidence=0.55):
        _record_structured_trace(
            player,
            request_type="event_branch",
            stable_context_id="option_prompt",
            chosen_action=chosen,
            reason=reason,
            confidence=confidence,
            prompt=prompt,
            options=tuple(options),
            metadata={
                "prompt_lower": prompt_lower,
            },
        )
        return chosen

    event_request, event_plan = _build_event_policy_request(
        player,
        request_type="event_branch",
        stable_context_id="option_prompt",
        options=tuple(options),
        prompt=prompt,
        metadata={
            "prompt_lower": prompt_lower,
            "recent_lower": recent,
        },
    )
    event_choice, event_trace = choose_event_option(event_request, event_plan)
    if event_choice is not None and event_trace is not None:
        _record_decision_request(event_request)
        _record_decision_trace(event_trace)
        return str(event_choice.value if event_choice.value is not None else event_choice.label)

    if options:
        return finalize(options[0], "event_option_empty_policy_fallback", 0.1)
    return finalize("", "event_option_empty_option_set", 0.0)


def _decide_cash(total, prompt=""):
    player = CURRENT_PLAYER
    if player is None:
        return 0
    if "how much money do you give" in (prompt or "").lower():
        return min(total, max(0, player.get_balance() // 10))
    return 0


def _decide_raw_input(prompt=""):
    global LAST_INPUT_FINGERPRINT, REPEATED_INPUT_COUNT

    player = CURRENT_PLAYER
    prompt_lower = (prompt or "").lower()
    options = _get_recent_menu_options()
    recent = _recent_lower(120)
    recent_mechanic = _recent_lower(20)
    inline_choices = _extract_inline_choices(prompt, *RECENT_TEXT[-12:])
    fingerprint = (prompt_lower.strip(), "\n".join(RECENT_TEXT[-10:]).lower())
    raw_override = None

    if inline_choices:
        event_request, event_plan = _build_event_policy_request(
            player,
            request_type="event_inline",
            stable_context_id="raw_input_prompt",
            options=tuple(inline_choices),
            prompt=prompt,
            metadata={
                "prompt_lower": prompt_lower,
                "recent_lower": recent,
            },
        )
        event_choice, event_trace = choose_event_inline_choice(event_request, event_plan)
        if event_choice is not None and event_trace is not None:
            _record_decision_request(event_request)
            _record_decision_trace(event_trace)
            raw_override = event_choice

    if fingerprint == LAST_INPUT_FINGERPRINT:
        REPEATED_INPUT_COUNT += 1
    else:
        LAST_INPUT_FINGERPRINT = fingerprint
        REPEATED_INPUT_COUNT = 0

    if raw_override is not None:
        return raw_override

    mechanic_offer_prompt = not prompt_lower and _looks_like_mechanic_intro_offer(recent_mechanic, prompt)

    if REPEATED_INPUT_COUNT >= 6:
        if "choose a number" in prompt_lower or "choose a number" in "\n".join(RECENT_TEXT[-5:]).lower():
            return str(options[-1][0] if options else 1)
        if mechanic_offer_prompt:
            return _decide_mechanic_intro_response(player, recent_mechanic, prompt, source="repeated") or "no"
        if "yes/no" in prompt_lower or any(
            phrase in recent
            for phrase in [
                "whaddya say", "you game", "could ya do", "speak up", "come again", "mumbling",
                "do you accept", "what do you think", "you buying", "you interested", "try again",
            ]
        ):
            return "no"
    if mechanic_offer_prompt:
        return _decide_mechanic_intro_response(player, recent_mechanic, prompt, source="blank") or "no"

    if "yes/no" in prompt_lower:
        return _decide_yes_no(prompt)
    if not prompt_lower and any(
        phrase in recent for phrase in [
            "would you like me to heal you", "you buying", "what do you think", "whaddya say",
            "do you accept", "are you in the mood to spend some money on my magic potions",
            "care to purchase any of my powerful potions", "you interested", "you game",
            "could ya do", "speak up", "come again", "mumbling",
        ]
    ):
        return _decide_yes_no(prompt)
    if "eat/save" in prompt_lower:
        if player is not None and (player.get_health() < 78 or player.get_sanity() < 42):
            return "eat"
        return "save"
    if "drink/save/toss" in prompt_lower:
        if player is not None and (player.get_health() < 60 or player.get_sanity() < 30):
            return "drink"
        if player is not None and player.get_rank() >= 1:
            return "save"
        return "toss"
    if "drink/wash/bottle/leave" in prompt_lower:
        if player is not None and player.get_health() < 55:
            return "drink"
        if player is not None and player.has_item("Water Bottles"):
            return "wash"
        return "bottle"
    if "drink/save" in prompt_lower:
        if player is not None and (player.get_health() < 65 or player.get_sanity() < 35):
            return "drink"
        return "save"
    if inline_choices:
        return _choose_inline_choice(inline_choices, player, prompt)
    if "who do you want to sell" in prompt_lower:
        return str(_choose_pawn_sale_item(options, player))
    # Millionaire afternoon menu: mechanic ending vs airport vs continue
    millionaire_afternoon = (
        "choose a number" in prompt_lower
        or "choose a number" in "\n".join(RECENT_TEXT[-5:]).lower()
    ) and "drive to the airport" in recent
    if millionaire_afternoon:
        return str(_choose_millionaire_afternoon(options, player))
    if "choose:" in prompt_lower and _looks_like_pawn_menu(options):
        return str(_choose_pawn_menu(options, player))
    if "choose:" in prompt_lower and _looks_like_loan_borrow_menu(options):
        return str(_choose_loan_borrow_amount(options, player))
    if "choose:" in prompt_lower and _looks_like_loan_repay_menu(options):
        return str(_choose_loan_repay_amount(options, player))
    if "choose:" in prompt_lower and _looks_like_loan_menu(options):
        return str(_choose_loan_menu(options, player))
    if "choose:" in prompt_lower and "car workbench" in recent:
        # Workbench main menu (Pack Up is option 5, Craft Something is option 1)
        if "pack up" in recent.lower():
            return str(_choose_workbench_menu(options, player))
        # Workbench craft sub-menu (recipe list with numbered items)
        if "what do you want to craft" in recent.lower():
            return str(_choose_workbench_craft(options, player))
        # Fallback: pack up
        return str(options[-1][0] if options else 1)
    if (
        "choose:" in prompt_lower
        and "what would you like to do?" in recent
        and "grimy gus" not in recent
        and not _looks_like_loan_menu(options)
    ):
        return str(options[-1][0] if options else 1)
    if "choose a number" in prompt_lower or "choose a number" in "\n".join(RECENT_TEXT[-5:]).lower():
        if _looks_like_pawn_menu(options):
            return str(_choose_pawn_menu(options, player))
        if "who do you want to interact with" in prompt_lower or "after noon with your companions" in recent or "afternoon with your companions" in recent:
            return str(_choose_companion_interaction(options, player))
        if "would you like to spend your day driving somewhere" in recent:
            return str(_choose_destination(options, player))
        if _looks_like_loan_borrow_menu(options):
            return str(_choose_loan_borrow_amount(options, player))
        if _looks_like_loan_repay_menu(options):
            return str(_choose_loan_repay_amount(options, player))
        if _looks_like_loan_menu(options):
            return str(_choose_loan_menu(options, player))
        if "what do you want?" in recent or "what else you want?" in recent:
            return str(_choose_store_item(options, player))
        if "flask of" in recent:
            return str(_choose_witch_flask(options, player))
        if "mind if i take a look at em" in recent or "is there anything you would like stuart to fix" in recent:
            return str(_choose_repair_item(options, player))
        if "which item would you like stuart to upgrade" in recent:
            return str(_choose_upgrade_item(options, player))
        if "car workbench" in recent:
            # Craft sub-menu reached via "choose a number" path
            if "what do you want to craft" in recent.lower():
                return str(_choose_workbench_craft(options, player))
            return str(_choose_workbench_menu(options, player))
        return str(options[-1][0] if options else 1)
    if "choose: " in prompt_lower and "who do you want to sell" not in prompt_lower:
        return str(options[-1][0] if options else 1)
    if "you buying" in recent:
        return _decide_yes_no(prompt)
    return "1"


_typer.Type.fast = _capture_type
_typer.Type.slow = _capture_type
_typer.Type.type = _capture_type
_typer.Type.type_clean = _capture_type
_typer.Type.fast_clean = _capture_type
_typer.Type.slow_clean = _capture_type
_typer.Type.suspense = _capture_type
_typer.Type.typeover = _capture_type
_typer.Ask.press_continue = lambda self, *args, **kwargs: None
_typer.Ask.yes_or_no = lambda self, prompt="", *args, **kwargs: _decide_yes_no(prompt)
_typer.Ask.choose_an_option = lambda self, options, *args, **kwargs: _decide_option("", options)
_typer.Ask.option = lambda self, prompt, options, *args, **kwargs: _decide_option(prompt, options)
_typer.Ask.give_cash = lambda self, total, prompt="", *args, **kwargs: _decide_cash(total, prompt)


def _rank_target(balance):
    if balance < 1000:
        return 1000
    if balance < 10000:
        return 10000
    if balance < 100000:
        return 100000
    if balance < 500000:
        return 500000
    if balance < 900000:
        return 900000
    return 1000000


def _rank_floor(balance):
    if balance >= 900000:
        return 900000
    if balance >= 500000:
        return 500000
    if balance >= 100000:
        return 100000
    if balance >= 10000:
        return 10000
    if balance >= 1000:
        return 1000
    return 0


def _visible_total(hand):
    if hand.possible_hands() == 2 and hand.ace_value() <= 21:
        return hand.ace_value()
    return hand.value()


def _dealer_upcard_value(dealer_hand):
    value = dealer_hand.get_card(0).value()
    return 11 if value == 1 else value


def _simulate_hit_total(hand, card_value):
    possible_totals = [hand.value()]
    if hand.possible_hands() == 2 and hand.ace_value() <= 21:
        possible_totals.append(hand.ace_value())

    new_totals = set()
    for running_total in possible_totals:
        if card_value == 1:
            new_totals.add(running_total + 1)
            if running_total + 11 <= 21:
                new_totals.add(running_total + 11)
        else:
            new_totals.add(running_total + card_value)

    valid_totals = [total for total in new_totals if total <= 21]
    if valid_totals:
        return max(valid_totals)
    return min(new_totals)


def _choose_blackjack_policy_option(player, *, stable_context_id, options, metadata):
    game_state = _current_game_state(player, context_tag=stable_context_id)
    request = DecisionRequest(
        request_type="blackjack_action" if stable_context_id == "blackjack_action" else stable_context_id,
        stable_context_id=stable_context_id,
        game_state=game_state.to_dict(),
        normalized_options=_structured_options(options, prefix=stable_context_id),
        raw_recent_text=tuple(RECENT_TEXT[-20:]),
        metadata={
            "cycle": CURRENT_CYCLE,
            "day": game_state.day,
            **metadata,
        },
    )
    _record_decision_request(request)
    plan = choose_strategic_goal(game_state)
    if stable_context_id == "blackjack_action":
        choice, trace = choose_blackjack_action(request, plan)
    elif stable_context_id == "insurance_decision":
        choice, trace = choose_insurance_option(request, plan)
    elif stable_context_id == "second_chance_decision":
        choice, trace = choose_second_chance_option(request, plan)
    else:
        return None
    _record_decision_trace(trace)
    return None if choice is None else str(choice.value if choice.value is not None else choice.label)


def _choose_blackjack_bet_amount(self):
    player = self._Blackjack__player
    balance = int(self._Blackjack__balance)
    fake_cash = _fraudulent_cash_amount(player)
    strategic_state = _current_game_state(player, context_tag="blackjack_bet")
    strategic_plan = choose_strategic_goal(strategic_state)
    pending_marvin = _pending_marvin_candidate(player, balance=balance, fake_cash=fake_cash)
    tuner = _rank_tuner(player)

    request = DecisionRequest(
        request_type="blackjack_bet",
        stable_context_id="blackjack_bet",
        game_state=strategic_state.to_dict(),
        raw_recent_text=tuple(RECENT_TEXT[-20:]),
        metadata={
            "cycle": CURRENT_CYCLE,
            "day": strategic_state.day,
            "rank": strategic_state.rank,
            "health": strategic_state.health,
            "sanity": strategic_state.sanity,
            "dealer_happiness": strategic_state.dealer_happiness,
            "balance": balance,
            "fake_cash": fake_cash,
            "min_bet": max(1, int(self._Blackjack__min_bet)),
            "target": _rank_target(balance),
            "floor": _rank_floor(balance),
            "distance": max(0, _rank_target(balance) - balance),
            "store_budget": max(_planned_store_spend(player), strategic_state.store_target_spend),
            "wants_store": _wants_store_run(player) or (strategic_plan.goal == "restock_supplies" and strategic_state.store_target_spend > 0),
            "wants_pawn": strategic_plan.goal == "cashout_pawn_inventory" and strategic_state.pawn_planned_sale_value > 0,
            "wants_doctor": _wants_doctor_visit(player),
            "progression_ready": _is_progression_ready(player),
            "phase": _progression_phase(player),
            "tuner_bet_ratio": tuner["bet_ratio"],
            "tuner_bet_ratio_safe": tuner["bet_ratio_safe"],
            "tuner_max_ratio": tuner["max_ratio"],
            "tuner_pressure_factor": tuner["pressure_factor"],
            "tuner_surplus_push": tuner["surplus_push"],
            "edge_score": _blackjack_edge_score(player),
            "pending_marvin_active": pending_marvin is not None,
            "pending_marvin_price": 0 if pending_marvin is None else int(pending_marvin["price"]),
            "pending_marvin_shortfall": 0 if pending_marvin is None else int(pending_marvin["shortfall"]),
            "stall_days": _progress_stall_days(player),
            "early_caution": _needs_car(player) and getattr(player, "_day", 1) <= 10,
            "stranded_no_car": _stranded_no_car_mode(player),
            "survival_mode": _wants_doctor_visit(player) or _doctor_visit_is_urgent(player) or _needs_recovery_day(player),
            "needs_car": _needs_car(player),
            "wants_millionaire_push": _wants_millionaire_push(player),
            "has_extra_round_item": _has_extra_round_item(player),
            "urgent_doctor": _doctor_visit_is_urgent(player),
            "has_met_tom": player.has_met("Tom Event"),
            "has_met_frank": player.has_met("Frank Event"),
            "has_met_oswald": player.has_met("Oswald Event"),
            "car_progress_reserve": _car_progress_reserve(player),
            "mechanic_purchase_reserve": _mechanic_purchase_reserve(player),
            "known_car_repair_reserve": _known_car_repair_reserve(player),
            "has_faulty_insurance": player.has_item("Faulty Insurance"),
            "wants_map_unlock": _wants_map_unlock_window(player),
        },
    )
    _record_decision_request(request)
    bet, trace = choose_blackjack_bet(request, strategic_plan)
    _record_decision_trace(trace)
    return 0 if bet is None else int(bet)


def _auto_peek_card(self):
    self._Blackjack__used_peek = True
    next_card = self._Blackjack__deck.peek()
    self._Blackjack__player.update_sneaky_peeky_glasses_durability()
    return next_card


def _should_take_insurance(self):
    player = self._Blackjack__player
    if not (player.has_item("Dealer's Grudge") or player.has_item("Dealer's Mercy")):
        return False
    insurance_cost = self._Blackjack__bet // 2
    if self._Blackjack__balance < insurance_cost:
        return False
    decision = _choose_blackjack_policy_option(
        player,
        stable_context_id="insurance_decision",
        options=("yes", "no"),
        metadata={
            "can_afford": True,
            "has_dealers_whispers": player.has_flask_effect("Dealer's Whispers"),
            "dealer_has_blackjack": self._Blackjack__dealer_hand.value() == 21,
        },
    )
    return decision == "yes"


def _should_replay_hand(self, status):
    player = self._Blackjack__player
    bet = int(self._Blackjack__bet)
    balance = int(self._Blackjack__balance)
    decision = _choose_blackjack_policy_option(
        player,
        stable_context_id="second_chance_decision",
        options=("yes", "no"),
        metadata={
            "status": status,
            "free_hand": self._Blackjack__free_hand,
            "bet": bet,
            "balance": balance,
            "insurance_bet": int(self._Blackjack__insurance_bet),
            "edge_score": _blackjack_edge_score(player),
            "reserve": _cash_safety_reserve(player, 88),
        },
    )
    return decision == "yes"


def _auto_bet(self):
    """Route bet sizing through the structured blackjack policy."""
    self._Blackjack__bet = _choose_blackjack_bet_amount(self)
    return True


def _auto_hit_or_stand(self):
    """Use an aggressive, simplified blackjack policy to grow bankroll quickly."""
    hand = self._Blackjack__hand
    dealer_hand = self._Blackjack__dealer_hand
    balance = self._Blackjack__balance
    bet = self._Blackjack__bet
    dealer_upcard = _dealer_upcard_value(dealer_hand)

    card_count = len(hand)
    soft_total = hand.ace_value() if hand.possible_hands() == 2 and hand.ace_value() <= 21 else 0
    total = soft_total or hand.value()

    can_double = (
        (self._Blackjack__player.has_item("Gambler's Chalice") or self._Blackjack__player.has_item("Overflowing Goblet")
         or self._Blackjack__player.has_flask_effect("Bonus Fortune"))
        and card_count == 2
        and not self._Blackjack__used_double_down
        and balance >= bet
    )
    can_split = (
        (self._Blackjack__player.has_item("Twin's Locket") or self._Blackjack__player.has_item("Mirror of Duality")
         or self._Blackjack__player.has_flask_effect("Split Serum"))
        and card_count == 2
        and not self._Blackjack__used_split
    )
    can_surrender = (
        (self._Blackjack__player.has_item("White Feather") or self._Blackjack__player.has_item("Phoenix Feather"))
        and card_count == 2
        and not self._Blackjack__used_surrender
    )
    can_peek = (
        (self._Blackjack__player.has_item("Sneaky Peeky Shades") or self._Blackjack__player.has_item("Sneaky Peeky Goggles"))
        and not self._Blackjack__used_peek
    )

    pair_value = None
    if can_split:
        first = hand.get_card(0).value()
        second = hand.get_card(1).value()
        if first == second:
            pair_value = 11 if first == 1 else first

    next_total = None
    if can_peek:
        next_card = _auto_peek_card(self)
        next_total = _simulate_hit_total(hand, next_card.value())

    action = _choose_blackjack_policy_option(
        self._Blackjack__player,
        stable_context_id="blackjack_action",
        options=tuple(option for option, allowed in (
            ("hit", True),
            ("stand", True),
            ("double", can_double),
            ("split", can_split),
            ("surrender", can_surrender),
        ) if allowed),
        metadata={
            "total": total,
            "soft_total": soft_total,
            "dealer_upcard": dealer_upcard,
            "bet": bet,
            "balance": balance,
            "can_double": can_double,
            "can_split": can_split,
            "can_surrender": can_surrender,
            "can_peek": can_peek,
            "pair_value": pair_value,
            "simulated_next_total": next_total,
            "has_no_bust": self._Blackjack__player.has_flask_effect("No Bust"),
            "has_imminent_blackjack": self._Blackjack__player.has_flask_effect("Imminent Blackjack"),
        },
    ) or "hit"

    if action == "split":
        return self.split_hand()
    if action == "surrender":
        return self.surrender()
    if action == "double":
        return self.double_down()
    if action == "stand":
        hand.get_final_value()
        return True

    self.hit()
    return False


def _auto_offer_insurance(self):
    can_insure = (self._Blackjack__player.has_item("Dealer's Grudge") or self._Blackjack__player.has_item("Dealer's Mercy"))
    if not can_insure:
        return

    insurance_cost = self._Blackjack__bet // 2
    if self._Blackjack__balance < insurance_cost:
        print()
        bj.type.fast(bj.cyan("Your insurance item glows, but you lack funds for the side-bet..."))
        print()
        return

    print()
    if self._Blackjack__player.has_item("Dealer's Mercy"):
        bj.type.fast("Your " + bj.magenta(bj.bright("Dealer's Mercy")) + " pulses with protective energy...")
    else:
        bj.type.fast("Your " + bj.magenta(bj.bright("Dealer's Grudge")) + " grows cold in your pocket...")
    print()

    if _should_take_insurance(self):
        self._Blackjack__insurance_bet = insurance_cost
        self._Blackjack__balance -= insurance_cost
        self._Blackjack__player.set_balance(self._Blackjack__balance)
        bj.type.fast(bj.cyan("The Dealer shows an Ace. You buy insurance for " + bj.green("${:,}".format(insurance_cost)) + "."))
        print()
        if not self._Blackjack__player.has_item("Dealer's Mercy"):
            self._Blackjack__player.update_dealers_grudge_durability()
    else:
        bj.type.fast(bj.cyan("The Dealer shows an Ace. You decline the insurance."))
        print()


_ORIGINAL_END_ROUND = bj.Blackjack.end_round


def _auto_end_round(self, status):
    if (
        self._Blackjack__player.has_flask_effect("Second Chance")
        and not self._Blackjack__used_second_chance
        and status in ["Dealer Wins", "Dealer Blackjack", "Player Bust"]
    ):
        if _should_replay_hand(self, status):
            self._Blackjack__used_second_chance = True
            bj.type.fast(bj.yellow(bj.bright("Your Flask of Second Chance glimmers. You replay the hand.")))
            print("\n")
            self._Blackjack__player.update_second_chance_durability()
            return False

        self._Blackjack__used_second_chance = True
        try:
            return _ORIGINAL_END_ROUND(self, status)
        finally:
            self._Blackjack__used_second_chance = False

    return _ORIGINAL_END_ROUND(self, status)


bj.Blackjack.bet = _auto_bet
bj.Blackjack.offer_insurance = _auto_offer_insurance
bj.Blackjack.hit_or_stand = _auto_hit_or_stand
bj.Blackjack.end_round = _auto_end_round

CYCLES = int(sys.argv[1]) if len(sys.argv) > 1 else 300
SEED = int(sys.argv[2]) if len(sys.argv) > 2 else 42
LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_out.txt")
JSON_LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_out.json")

CURRENT_CYCLE = None
CURRENT_EVENTS = []
ALL_EVENTS = []
errs = []

TRACKED_STATS = [
    "days_survived",
    "total_money_earned",
    "total_money_spent",
    "items_collected",
    "items_sold",
    "events_experienced",
    "people_met",
    "injuries_sustained",
    "illnesses_contracted",
    "near_death_experiences",
    "companions_befriended",
    "loans_taken",
    "loans_repaid",
    "times_robbed",
    "times_hospitalized",
    "mechanic_visits",
    "doctor_visits",
    "witch_doctor_visits",
    "casino_visits",
    "pawn_shop_visits",
    "marvin_visits",
    "loan_shark_visits",
]

TRACKED_GAMBLING_STATS = [
    "total_hands",
    "wins",
    "losses",
    "ties",
    "blackjacks",
    "busts",
    "total_won",
    "total_lost",
    "double_downs_won",
    "splits_won",
    "surrenders_used",
    "insurance_collected",
]


def fake_input(_prompt=""):
    _remember_text(_prompt)
    return _decide_raw_input(_prompt)


_log_file = open(LOG, "w", encoding="utf-8")


def _close_log_file():
    if not _log_file.closed:
        _log_file.close()


atexit.register(_close_log_file)


def log(message=""):
    _log_file.write(str(message) + "\n")
    _log_file.flush()


def record_event(kind, name):
    if CURRENT_CYCLE is None:
        return
    label = f"{kind}:{name}"
    CURRENT_EVENTS.append(label)
    ALL_EVENTS.append((CURRENT_CYCLE, kind, name))


def _wrap_storyline_get_stage_event():
    original = story.storylines.StorylineSystem._get_stage_event

    def wrapped(self, name):
        event = original(self, name)
        if event is None:
            return None

        stage = self.storylines[name].get("stage", 0)
        label = f"{name}:stage{stage}"

        def invoke():
            record_event("storyline", label)
            return event()

        invoke.__name__ = getattr(event, "__name__", "storyline_event")
        return invoke

    story.storylines.StorylineSystem._get_stage_event = wrapped


def _wrap_day_and_night_selection():
    original_day = _lists_mod.Lists.get_day_event
    original_night = _lists_mod.Lists.get_night_event

    def wrapped_day(self):
        name = original_day(self)
        record_event("day", name)
        return name

    def wrapped_night(self):
        name = original_night(self)
        record_event("night", name)
        return name

    _lists_mod.Lists.get_day_event = wrapped_day
    _lists_mod.Lists.get_night_event = wrapped_night


def _wrap_meet():
    original = story.Player.meet

    def wrapped(self, person):
        record_event("met", person)
        return original(self, person)

    story.Player.meet = wrapped


def _wrap_kill():
    original = story.Player.kill

    def wrapped(self, cause_of_death=None):
        cause = (cause_of_death or "").strip() or _infer_death_cause_from_recent_text()
        self._autoplay_death_cause = cause
        return original(self, cause_of_death)

    story.Player.kill = wrapped


def _wrap_location_visits():
    location_methods = {
        "visit_doctor": "doctor",
        "visit_witch_doctor": "doctor:witch",
        "visit_tom": "mechanic:tom",
        "visit_frank": "mechanic:frank",
        "visit_oswald": "mechanic:oswald",
        "visit_convenience_store": "shop:convenience_store",
        "visit_marvin": "shop:marvin",
        "visit_pawn_shop": "shop:pawn_shop",
        "visit_loan_shark": "shop:loan_shark",
        "visit_airport": "shop:airport",
        "visit_phone_call": "shop:phone_call",
        "visit_workbench": "shop:car_workbench",
        "road_adventure": "adventure:road",
        "woodlands_adventure": "adventure:woodlands",
        "swamp_adventure": "adventure:swamp",
        "beach_adventure": "adventure:beach",
        "underwater_adventure": "adventure:ocean_depths",
        "city_adventure": "adventure:city",
    }

    for method_name, label in location_methods.items():
        original = getattr(story.Player, method_name, None)
        if original is None:
            continue

        def make_wrapper(fn, event_label):
            def wrapped(self, *args, **kwargs):
                _mark_location_visit(self, event_label)
                record_event("location", event_label)
                return fn(self, *args, **kwargs)

            return wrapped

        setattr(story.Player, method_name, make_wrapper(original, label))


def _wrap_item_mutations():
    original_add_item = getattr(story.Player, "add_item", None)
    if original_add_item is not None:
        def wrapped_add_item(self, item, *args, **kwargs):
            had_item = self.has_item(item)
            result = original_add_item(self, item, *args, **kwargs)
            if not had_item and self.has_item(item):
                _record_item_provenance(self, item, "acquired")
            return result
        setattr(story.Player, "add_item", wrapped_add_item)

    original_use_item = getattr(story.Player, "use_item", None)
    if original_use_item is not None:
        def wrapped_use_item(self, item, *args, **kwargs):
            had_item = self.has_item(item)
            result = original_use_item(self, item, *args, **kwargs)
            if had_item and not self.has_item(item):
                _record_item_provenance(self, item, "used")
            return result
        setattr(story.Player, "use_item", wrapped_use_item)

    original_remove_item = getattr(story.Player, "remove_item", None)
    if original_remove_item is not None:
        def wrapped_remove_item(self, item, *args, **kwargs):
            had_item = self.has_item(item)
            result = original_remove_item(self, item, *args, **kwargs)
            if had_item and not self.has_item(item):
                _record_item_provenance(self, item, "removed")
            return result
        setattr(story.Player, "remove_item", wrapped_remove_item)

    original_break_item = getattr(story.Player, "break_item", None)
    if original_break_item is not None:
        def wrapped_break_item(self, item, *args, **kwargs):
            had_item = self.has_item(item)
            result = original_break_item(self, item, *args, **kwargs)
            if had_item and self.has_broken_item(item):
                _record_item_provenance(self, item, "broken")
            return result
        setattr(story.Player, "break_item", wrapped_break_item)

    original_fix_item = getattr(story.Player, "fix_item", None)
    if original_fix_item is not None:
        def wrapped_fix_item(self, item, *args, **kwargs):
            was_broken = self.has_broken_item(item) or self.is_repairing_item(item)
            result = original_fix_item(self, item, *args, **kwargs)
            if was_broken and self.has_item(item):
                _record_item_provenance(self, item, "fixed")
            return result
        setattr(story.Player, "fix_item", wrapped_fix_item)

    original_repair_item = getattr(story.Player, "repair_item", None)
    if original_repair_item is not None:
        def wrapped_repair_item(self, item, *args, **kwargs):
            was_broken = self.has_broken_item(item)
            result = original_repair_item(self, item, *args, **kwargs)
            if was_broken and self.is_repairing_item(item):
                _record_item_provenance(self, item, "repairing")
            return result
        setattr(story.Player, "repair_item", wrapped_repair_item)


def install_tracking_hooks():
    _wrap_storyline_get_stage_event()
    _wrap_day_and_night_selection()
    _wrap_meet()
    _wrap_kill()
    _wrap_location_visits()
    _wrap_item_mutations()


def run(fn, label):
    try:
        fn()
    except Exception as exc:
        errs.append(f"{label}: {type(exc).__name__}: {exc}")
        log(traceback.format_exc())


def snapshot_player(player):
    active_storylines = sorted(
        name
        for name, data in player._storyline_system.storylines.items()
        if data.get("stage", 0) > 0 and not data.get("completed") and not data.get("failed")
    )
    completed_storylines = sorted(
        name for name, data in player._storyline_system.storylines.items() if data.get("completed")
    )
    failed_storylines = sorted(
        name for name, data in player._storyline_system.storylines.items() if data.get("failed")
    )
    return {
        "day": int(player._day),
        "balance": int(player._balance),
        "health": int(player._health),
        "sanity": int(player._sanity),
        "rank": int(player._rank),
        "alive": bool(player._alive),
        "death_cause": getattr(player, "_autoplay_death_cause", ""),
        "has_car": bool(player.has_item("Car")),
        "is_millionaire": bool(player.is_millionaire()) if hasattr(player, "is_millionaire") else False,
        "millionaire_visited": bool(player.was_millionaire_visited()) if hasattr(player, "was_millionaire_visited") else False,
        "inventory": set(player._inventory),
        "injuries": set(player._injuries),
        "statuses": set(player._status_effects),
        "companions": set(player._companions.keys()),
        "travel_restrictions": set(player._travel_restrictions),
        "broken_items": set(player._broken_inventory),
        "repairing_items": set(player._repairing_inventory),
        "pawned_items": set(getattr(player, "_gus_items_sold", set())),
        "active_storylines": set(active_storylines),
        "completed_storylines": set(completed_storylines),
        "failed_storylines": set(failed_storylines),
        "statistics": dict(player._statistics),
        "gambling": dict(player._gambling_stats),
    }


def unique_preserve_order(values):
    seen = set()
    ordered = []
    for value in values:
        if value in seen:
            continue
        seen.add(value)
        ordered.append(value)
    return ordered


def format_signed(value, money=False):
    prefix = "+" if value >= 0 else "-"
    number = abs(int(value))
    if money:
        return f"{prefix}${number:,}"
    return f"{prefix}{number}"


def format_state(before, after):
    return (
        f"$ {before['balance']:,} -> {after['balance']:,} ({format_signed(after['balance'] - before['balance'], money=True)}) | "
        f"HP {before['health']} -> {after['health']} ({format_signed(after['health'] - before['health'])}) | "
        f"SAN {before['sanity']} -> {after['sanity']} ({format_signed(after['sanity'] - before['sanity'])}) | "
        f"Rank {before['rank']} -> {after['rank']} | Car {'Y' if after['has_car'] else 'N'}"
    )


def _cycle_effect_score(before, after):
    cash_delta = after["balance"] - before["balance"]
    health_delta = after["health"] - before["health"]
    sanity_delta = after["sanity"] - before["sanity"]
    return (cash_delta / 25.0) + (health_delta * 8.0) + (sanity_delta * 6.0)


def _cycle_polarity(before, after):
    score = _cycle_effect_score(before, after)
    if score >= 3:
        return "positive"
    if score <= -3:
        return "negative"
    return "neutral"


def _cycle_relevant_items(before, after, recent_lines):
    candidates = set(before["inventory"]) | set(after["inventory"])
    candidates |= set(before["broken_items"]) | set(after["broken_items"])
    candidates |= set(before["repairing_items"]) | set(after["repairing_items"])

    recent_blob = "\n".join(recent_lines).lower()
    relevant = set()
    for item_name in candidates:
        item_lower = str(item_name).lower()
        if len(item_lower) < 4:
            continue
        if item_name in (after["inventory"] - before["inventory"]) or item_name in (before["inventory"] - after["inventory"]):
            relevant.add(item_name)
            continue
        if item_lower in recent_blob:
            relevant.add(item_name)
    return sorted(relevant)


def _record_item_impact(item_impacts, item_name, polarity, before, after):
    entry = item_impacts.setdefault(
        item_name,
        {"hits": 0, "positive": 0, "negative": 0, "neutral": 0, "cash": 0, "health": 0, "sanity": 0},
    )
    entry["hits"] += 1
    entry[polarity] += 1
    entry["cash"] += after["balance"] - before["balance"]
    entry["health"] += after["health"] - before["health"]
    entry["sanity"] += after["sanity"] - before["sanity"]


def set_diff(before_set, after_set):
    return sorted(after_set - before_set), sorted(before_set - after_set)


def format_change_line(label, added, removed):
    pieces = []
    if added:
        pieces.append(f"+{label}={added}")
    if removed:
        pieces.append(f"-{label}={removed}")
    return " | ".join(pieces)


def stat_deltas(before, after, keys):
    changes = []
    for key in keys:
        delta = int(after.get(key, 0) - before.get(key, 0))
        if not delta:
            continue
        is_money = ("money" in key) or (key in {"total_won", "total_lost"})
        changes.append(f"{key} {format_signed(delta, money=is_money)}")
    return changes


def render_distribution(title, pairs):
    log(title)
    if not pairs:
        log("  none")
        log("")
        return
    for name, count in pairs:
        log(f"  {count:>3}  {name}")
    log("")


install_tracking_hooks()

import builtins as _builtins

_real_print = _builtins.print
_builtins.print = lambda *args, **kwargs: None
_builtins.quit = lambda *args, **kwargs: None
_builtins.exit = lambda *args, **kwargs: None

with patch("builtins.input", fake_input):
    random.seed(SEED)
    p = story.Player()
    CURRENT_PLAYER = p
    g = bj.Blackjack(p)
    event_polarity_counts = Counter()
    item_impacts = {}
    max_rank_seen = int(p.get_rank())
    max_balance_seen = int(p.get_balance())
    max_balance_days = [int(p.get_day())] if hasattr(p, "get_day") else [1]
    early_peak_balance = int(p.get_balance())
    early_peak_days = [int(p.get_day())] if hasattr(p, "get_day") else [1]
    early_balance_end = int(p.get_balance())
    EVER_HAD_CAR = bool(p.has_item("Car"))
    run(p.opening_lines, "opening")

    for cycle_number in range(1, CYCLES + 1):
        CURRENT_CYCLE = cycle_number
        CURRENT_EVENTS = []
        before = snapshot_player(p)
        recent_start = len(RECENT_TEXT)

        run(g.play_round, f"c{cycle_number}.play")
        run(p.end_day, f"c{cycle_number}.end")
        run(p.start_day, f"c{cycle_number}.start")
        run(p.afternoon, f"c{cycle_number}.aftern")

        after = snapshot_player(p)
        cycle_recent_lines = RECENT_TEXT[recent_start:]
        EVER_HAD_CAR = EVER_HAD_CAR or after["has_car"]
        max_rank_seen = max(max_rank_seen, after["rank"])
        if after["balance"] > max_balance_seen:
            max_balance_seen = after["balance"]
            max_balance_days = [after["day"]]
        elif after["balance"] == max_balance_seen and after["day"] not in max_balance_days:
            max_balance_days.append(after["day"])
        if after["day"] <= EARLY_MECHANIC_DAY_LIMIT:
            early_balance_end = after["balance"]
            if after["balance"] > early_peak_balance:
                early_peak_balance = after["balance"]
                early_peak_days = [after["day"]]
            elif after["balance"] == early_peak_balance and after["day"] not in early_peak_days:
                early_peak_days.append(after["day"])
        events = unique_preserve_order(CURRENT_EVENTS)
        polarity = _cycle_polarity(before, after)
        if events:
            event_polarity_counts[polarity] += len(events)
        else:
            event_polarity_counts[polarity] += 1
        for item_name in _cycle_relevant_items(before, after, cycle_recent_lines):
            _record_item_impact(item_impacts, item_name, polarity, before, after)

        inventory_added, inventory_removed = set_diff(before["inventory"], after["inventory"])
        injuries_added, injuries_removed = set_diff(before["injuries"], after["injuries"])
        statuses_added, statuses_removed = set_diff(before["statuses"], after["statuses"])
        companions_added, companions_removed = set_diff(before["companions"], after["companions"])
        story_added, story_removed = set_diff(before["active_storylines"], after["active_storylines"])
        story_completed_added, _story_completed_removed = set_diff(
            before["completed_storylines"], after["completed_storylines"]
        )
        story_failed_added, _story_failed_removed = set_diff(
            before["failed_storylines"], after["failed_storylines"]
        )
        travel_added, travel_removed = set_diff(before["travel_restrictions"], after["travel_restrictions"])
        broken_added, broken_removed = set_diff(before["broken_items"], after["broken_items"])
        repairing_added, repairing_removed = set_diff(before["repairing_items"], after["repairing_items"])

        stat_changes = stat_deltas(before["statistics"], after["statistics"], TRACKED_STATS)
        gambling_changes = stat_deltas(before["gambling"], after["gambling"], TRACKED_GAMBLING_STATS)

        log("=" * 88)
        log(f"Cycle {cycle_number:02d} | Day {after['day']}")
        log(f"State   {format_state(before, after)}")
        log(f"Events  {', '.join(events) if events else 'none captured'}")
        log(f"Polarity {polarity}")

        change_lines = [
            format_change_line("items", inventory_added, inventory_removed),
            format_change_line("injuries", injuries_added, injuries_removed),
            format_change_line("status", statuses_added, statuses_removed),
            format_change_line("companions", companions_added, companions_removed),
            format_change_line("travel", travel_added, travel_removed),
            format_change_line("broken", broken_added, broken_removed),
            format_change_line("repairing", repairing_added, repairing_removed),
            format_change_line("story", story_added, story_removed),
            format_change_line("story_completed", story_completed_added, []),
            format_change_line("story_failed", story_failed_added, []),
        ]
        change_lines = [line for line in change_lines if line]

        log(f"Changes {' | '.join(change_lines) if change_lines else 'none'}")
        log(f"Stats   {', '.join(stat_changes) if stat_changes else 'no tracked stat changes'}")
        log(f"Gamble  {', '.join(gambling_changes) if gambling_changes else 'no gambling stat changes'}")

        if not after["alive"]:
            cause = after["death_cause"] or before["death_cause"] or "Unknown"
            log(f"Result  player died during cycle {cycle_number} | cause: {cause}")
            break

        if after["balance"] == 0:
            log(f"Result  player hit $0 during cycle {cycle_number}")
            break

_builtins.print = _real_print

final_state = snapshot_player(p)
EVER_HAD_CAR = EVER_HAD_CAR or final_state["has_car"]
max_rank_seen = max(max_rank_seen, final_state["rank"])
max_balance_seen = max(max_balance_seen, final_state["balance"])
if final_state["day"] <= EARLY_MECHANIC_DAY_LIMIT:
    early_balance_end = final_state["balance"]
    if final_state["balance"] > early_peak_balance:
        early_peak_balance = final_state["balance"]
        early_peak_days = [final_state["day"]]
    elif final_state["balance"] == early_peak_balance and final_state["day"] not in early_peak_days:
        early_peak_days.append(final_state["day"])
early_mechanic_funnel = _build_early_mechanic_funnel(
    final_state,
    peak_balance=early_peak_balance,
    peak_days=early_peak_days,
)
early_mechanic_funnel["balance_end"] = int(early_balance_end)
event_counter = Counter(f"{kind}:{name}" for _, kind, name in ALL_EVENTS)
day_counter = Counter(name for _, kind, name in ALL_EVENTS if kind == "day")
night_counter = Counter(name for _, kind, name in ALL_EVENTS if kind == "night")
storyline_counter = Counter(name for _, kind, name in ALL_EVENTS if kind == "storyline")
meet_counter = Counter(name for _, kind, name in ALL_EVENTS if kind == "met")
location_counter = Counter(name for _, kind, name in ALL_EVENTS if kind == "location")

log("")
log("#" * 88)
log(f"Run Summary | cycles_requested={CYCLES} | seed={SEED}")
log(
    f"Final    Day {final_state['day']} | $ {final_state['balance']:,} | HP {final_state['health']} | "
    f"SAN {final_state['sanity']} | Rank {final_state['rank']} | Alive={final_state['alive']}"
)
log(f"Peak     $ {max_balance_seen:,} | Rank {max_rank_seen}")
log(f"Peak days    {', '.join(str(day) for day in max_balance_days)}")
log(f"Inventory   {sorted(final_state['inventory'])}")
log(f"Has car            {final_state['has_car']}")
log(f"Ever had car       {EVER_HAD_CAR}")
log(f"Has map            {'Map' in final_state['inventory']}")
log(f"Has worn map       {'Worn Map' in final_state['inventory']}")
log(f"Has marvin access  {('Map' in final_state['inventory']) or ('Worn Map' in final_state['inventory'])}")
log(f"Millionaire reached {final_state['is_millionaire']}")
log(f"Millionaire visited {final_state['millionaire_visited']}")
log(f"Death cause        {final_state['death_cause'] or 'None'}")
log(f"Injuries    {sorted(final_state['injuries'])}")
log(f"Status      {sorted(final_state['statuses'])}")
log(f"Pawned items {sorted(final_state['pawned_items'])}")
log(f"Pawned count {len(final_state['pawned_items'])}")
log(f"Companions  {sorted(final_state['companions'])}")
log(f"Travel restrictions  {sorted(final_state['travel_restrictions'])}")
log(f"Broken items        {sorted(final_state['broken_items'])}")
log(f"Repairing items     {sorted(final_state['repairing_items'])}")
log(f"Storylines active     {sorted(final_state['active_storylines'])}")
log(f"Storylines completed  {sorted(final_state['completed_storylines'])}")
log(f"Storylines failed     {sorted(final_state['failed_storylines'])}")
if MECHANIC_DECISIONS:
    log("Mechanic intro decisions")
    for decision in MECHANIC_DECISIONS:
        cost = "?" if decision["cost"] is None else f"${decision['cost']:,}"
        balance = "?" if decision["balance"] is None else f"${decision['balance']:,}"
        day = "?" if decision["day"] is None else str(decision["day"])
        log(
            f"  day={day} mechanic={decision['mechanic']} cost={cost} balance={balance} answer={decision['answer']} source={decision['source']}"
        )
else:
    log("Mechanic intro decisions")
    log("  none")
log("")

if FALLBACK_DECISIONS:
    log("Fallback decisions")
    for label, count in FALLBACK_DECISIONS.most_common(20):
        log(f"  {count} {label}")
else:
    log("Fallback decisions")
    log("  none")
log("")

log("Event polarity")
for label in ["positive", "negative", "neutral"]:
    log(f"  {label} {event_polarity_counts.get(label, 0)}")
log("")

if item_impacts:
    log("Item impact")
    ranked_item_impacts = sorted(
        item_impacts.items(),
        key=lambda item: (
            item[1]["positive"] - item[1]["negative"],
            item[1]["hits"],
            item[1]["cash"],
            item[0],
        ),
        reverse=True,
    )
    for item_name, stats in ranked_item_impacts[:20]:
        log(
            f"  {item_name} hits={stats['hits']} pos={stats['positive']} neg={stats['negative']} neu={stats['neutral']} cash={stats['cash']:+} hp={stats['health']:+} san={stats['sanity']:+}"
        )
else:
    log("Item impact")
    log("  none")
log("")

marvin_items = []
for item_name, history in sorted(ITEM_PROVENANCE.items()):
    acquired_from_marvin = [
        entry for entry in history["acquired"]
        if "shop:marvin" in entry.get("source", "") or entry.get("source") == "text:marvin"
    ]
    if not acquired_from_marvin:
        continue
    marvin_items.append((item_name, acquired_from_marvin, history))

log("Marvin provenance")
if marvin_items:
    for item_name, acquired_from_marvin, history in marvin_items:
        log(
            f"  item={item_name}; bought={_render_item_history(acquired_from_marvin)}; "
            f"used={_render_item_history(history['used'])}; removed={_render_item_history(history['removed'])}; "
            f"broken={_render_item_history(history['broken'])}; fixed={_render_item_history(history['fixed'])}"
        )
else:
    log("  none")
log("")

log("Planner traces")
if DECISION_TRACES:
    goal_counts = Counter(trace.strategic_goal or "unknown" for trace in DECISION_TRACES)
    log("  goals " + " | ".join(f"{goal}={count}" for goal, count in goal_counts.most_common(8)))
    for trace in DECISION_TRACES[-8:]:
        log(
            f"  cycle={trace.cycle if trace.cycle is not None else '?'} day={trace.day if trace.day is not None else '?'} "
            f"goal={trace.strategic_goal or 'unknown'} action={trace.chosen_action} "
            f"confidence={trace.confidence:.2f} reason={trace.reason}"
        )
else:
    log("  none")
log("")

route_traces = [trace for trace in DECISION_TRACES if trace.request_type == "route_select"]
route_outcome_counts = Counter(str(trace.metadata.get("route_outcome", "unknown")) for trace in route_traces)
route_interrupt_kind_counts = Counter(
    str(trace.metadata.get("interrupt_kind", "unknown"))
    for trace in route_traces
    if trace.metadata.get("route_outcome") == "interrupt"
)
route_interrupted_goal_counts = Counter()
route_interrupted_top_goal_counts = Counter()
for trace in route_traces:
    if trace.metadata.get("route_outcome") != "interrupt":
        continue
    for goal in trace.metadata.get("candidate_goals", ()):
        route_interrupted_goal_counts[str(goal)] += 1
    route_interrupted_top_goal_counts[str(trace.metadata.get("top_goal_before_interrupt", "unknown"))] += 1
route_applied_goal_counts = Counter(
    trace.strategic_goal or "unknown"
    for trace in route_traces
    if trace.metadata.get("route_outcome") == "applied"
)
route_suppressed_goal_counts = Counter(
    trace.strategic_goal or "unknown"
    for trace in route_traces
    if trace.metadata.get("route_outcome") == "suppressed"
)

log("Route visibility")
if route_traces:
    log("  outcomes " + " | ".join(f"{name}={count}" for name, count in route_outcome_counts.most_common(6)))
    if route_interrupt_kind_counts:
        log("  interrupts " + " | ".join(f"{name}={count}" for name, count in route_interrupt_kind_counts.most_common(6)))
    if route_interrupted_goal_counts:
        log("  blocked_goals " + " | ".join(f"{name}={count}" for name, count in route_interrupted_goal_counts.most_common(8)))
    if route_interrupted_top_goal_counts:
        log("  interrupted_top_goals " + " | ".join(f"{name}={count}" for name, count in route_interrupted_top_goal_counts.most_common(8)))
    if route_applied_goal_counts:
        log("  applied_goals " + " | ".join(f"{name}={count}" for name, count in route_applied_goal_counts.most_common(8)))
    if route_suppressed_goal_counts:
        log("  suppressed_goals " + " | ".join(f"{name}={count}" for name, count in route_suppressed_goal_counts.most_common(8)))
else:
    log("  none")
log("")

render_distribution("Event Distribution | day", sorted(day_counter.items(), key=lambda item: (-item[1], item[0])))
render_distribution("Event Distribution | night", sorted(night_counter.items(), key=lambda item: (-item[1], item[0])))
render_distribution(
    "Event Distribution | storyline",
    sorted(storyline_counter.items(), key=lambda item: (-item[1], item[0])),
)
render_distribution("Event Distribution | met", sorted(meet_counter.items(), key=lambda item: (-item[1], item[0]))[:25])
render_distribution("Event Distribution | location", sorted(location_counter.items(), key=lambda item: (-item[1], item[0])))
render_distribution("Event Distribution | all", sorted(event_counter.items(), key=lambda item: (-item[1], item[0]))[:40])

log("Final Statistics")
for key in TRACKED_STATS:
    log(f"  {key:22} {final_state['statistics'].get(key, 0)}")
log("")

log("Final Gambling Statistics")
for key, value in final_state["gambling"].items():
    log(f"  {key:22} {value}")
log("")

if errs:
    log(f"ERRORS ({len(errs)}):")
    for error in errs:
        log(f"  {error}")
else:
    log("NO ERRORS")

log("")
if warning_messages:
    log(f"WARNINGS ({len(warning_messages)}):")
    for warning_message in warning_messages:
        log(f"  {warning_message}")
else:
    log("NO WARNINGS")

decision_request_counts = Counter(request.request_type for request in DECISION_REQUESTS)
decision_request_context_counts = Counter(request.stable_context_id or request.request_type for request in DECISION_REQUESTS)
decision_trace_request_counts = Counter(trace.request_type for trace in DECISION_TRACES)
decision_trace_context_counts = Counter(trace.context or trace.request_type for trace in DECISION_TRACES)
decision_goal_counts = Counter(trace.strategic_goal or "unknown" for trace in DECISION_TRACES)

json_payload = {
    "seed": SEED,
    "cycles_requested": CYCLES,
    "run_summary": {
        "day": final_state["day"],
        "balance": final_state["balance"],
        "health": final_state["health"],
        "sanity": final_state["sanity"],
        "rank": final_state["rank"],
        "alive": final_state["alive"],
        "peak_balance": max_balance_seen,
        "peak_rank": max_rank_seen,
        "peak_days": list(max_balance_days),
        "ever_had_car": EVER_HAD_CAR,
        "has_map": "Map" in final_state["inventory"],
        "has_worn_map": "Worn Map" in final_state["inventory"],
        "has_marvin_access": ("Map" in final_state["inventory"]) or ("Worn Map" in final_state["inventory"]),
        "millionaire_reached": final_state["is_millionaire"],
        "millionaire_visited": final_state["millionaire_visited"],
        "death_cause": final_state["death_cause"],
    },
    "final_state": {
        "inventory": sorted(final_state["inventory"]),
        "has_car": final_state["has_car"],
        "injuries": sorted(final_state["injuries"]),
        "statuses": sorted(final_state["statuses"]),
        "pawned_items": sorted(final_state["pawned_items"]),
        "companions": sorted(final_state["companions"]),
        "travel_restrictions": sorted(final_state["travel_restrictions"]),
        "broken_items": sorted(final_state["broken_items"]),
        "repairing_items": sorted(final_state["repairing_items"]),
        "active_storylines": sorted(final_state["active_storylines"]),
        "completed_storylines": sorted(final_state["completed_storylines"]),
        "failed_storylines": sorted(final_state["failed_storylines"]),
        "statistics": dict(final_state["statistics"]),
        "gambling": dict(final_state["gambling"]),
    },
    "early_mechanic_funnel": dict(early_mechanic_funnel),
    "mechanic_decisions": list(MECHANIC_DECISIONS),
    "fallback_decisions": dict(FALLBACK_DECISIONS),
    "event_polarity": dict(event_polarity_counts),
    "item_impacts": dict(item_impacts),
    "marvin_provenance": {
        item_name: {
            "acquired": list(acquired_from_marvin),
            "used": list(history["used"]),
            "removed": list(history["removed"]),
            "broken": list(history["broken"]),
            "fixed": list(history["fixed"]),
            "repairing": list(history["repairing"]),
        }
        for item_name, acquired_from_marvin, history in marvin_items
    },
    "decision_summary": {
        "request_counts": dict(decision_request_counts),
        "request_context_counts": dict(decision_request_context_counts),
        "trace_request_counts": dict(decision_trace_request_counts),
        "trace_context_counts": dict(decision_trace_context_counts),
        "goal_counts": dict(decision_goal_counts),
        "route_outcome_counts": dict(route_outcome_counts),
        "route_interrupt_kind_counts": dict(route_interrupt_kind_counts),
        "route_interrupted_goal_counts": dict(route_interrupted_goal_counts),
        "route_interrupted_top_goal_counts": dict(route_interrupted_top_goal_counts),
        "route_applied_goal_counts": dict(route_applied_goal_counts),
        "route_suppressed_goal_counts": dict(route_suppressed_goal_counts),
    },
    "decision_requests": [request.to_dict() for request in DECISION_REQUESTS],
    "decision_traces": [trace.to_dict() for trace in DECISION_TRACES],
    "event_distribution": {
        "day": dict(day_counter),
        "night": dict(night_counter),
        "storyline": dict(storyline_counter),
        "met": dict(meet_counter),
        "location": dict(location_counter),
        "all": dict(event_counter),
    },
    "errors": list(errs),
    "warnings": list(warning_messages),
}

with open(JSON_LOG, "w", encoding="utf-8") as json_handle:
    json.dump(json_payload, json_handle, indent=2, sort_keys=True)

_close_log_file()
print(f"Results -> {LOG}")
print(f"Errors: {len(errs)}")
