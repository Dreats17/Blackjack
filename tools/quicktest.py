"""Fast automated playtest with structured per-day reporting."""

import atexit
import inspect
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

STORY_ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "story")

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
    CRAFTING_MIN_PRIORITY,
    CRAFTING_RECIPE_PRIORITIES,
    GIFT_WRAP_HAPPINESS_THRESHOLD,
    GIFT_WRAP_MIN_BALANCE,
    GIFT_WORTHY_ITEMS,
    MARVIN_ITEM_ORDER,
    STORE_CAR_SURVIVAL_PRIORITIES,
    STORE_MUST_HAVE_ITEMS,
    WITCH_FLASK_PRIORITIES,
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
_BLANK_PROMPT_STREAK = 0
_YN_FALLBACK_STREAK = 0
_YN_FALLBACK_LABEL = None
ANSI_RE = re.compile(r"\x1b\[[0-9;]*[A-Za-z]")
MECHANIC_DECISIONS = []
EARLY_MECHANIC_DAY_LIMIT = 10
EARLY_MECHANIC_THRESHOLD = 200
FALLBACK_DECISIONS = Counter()
FLASK_PURCHASES = Counter()  # tracks which witch flasks are bought during the run
ITEMS_EVER_BROKEN = Counter()  # accumulates all items that break across cycles
EVER_HAD_CAR = False
GIFT_DELIVERIES = []
DEALER_FREE_HANDS = []
DECISION_REQUESTS = []
DECISION_TRACES = []
FUNNEL_METRIC_DEFAULTS = {
    "store_buyout_ready_count": 0,
    "store_buyout_trigger_count": 0,
    "store_same_day_return_count": 0,
    "gift_unlock_push_count": 0,
    "gift_unlock_day": 0,
    "workbench_ready_count": 0,
    "workbench_trigger_count": 0,
    "craft_attempt_count": 0,
    "marvin_ready_count": 0,
    "marvin_route_present_count": 0,
    "marvin_direct_gate_count": 0,
    "marvin_conversion_window_count": 0,
    "debt_growth_override_count": 0,
    "loan_growth_override_count": 0,
    "pawn_growth_override_count": 0,
}
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


def _ensure_funnel_metrics(player):
    if player is None:
        return dict(FUNNEL_METRIC_DEFAULTS)
    metrics = getattr(player, "_autoplay_funnel_metrics", None)
    if not isinstance(metrics, dict):
        metrics = dict(FUNNEL_METRIC_DEFAULTS)
        player._autoplay_funnel_metrics = metrics
    else:
        for name, default in FUNNEL_METRIC_DEFAULTS.items():
            metrics.setdefault(name, default)
    return metrics


def _bump_funnel_metric(player, name, amount=1):
    metrics = _ensure_funnel_metrics(player)
    metrics[name] = int(metrics.get(name, 0) or 0) + int(amount)


def _set_funnel_day_once(player, name):
    if player is None:
        return
    metrics = _ensure_funnel_metrics(player)
    if int(metrics.get(name, 0) or 0) > 0:
        return
    metrics[name] = max(0, int(getattr(player, "_day", 0) or 0))


def _snapshot_funnel_metrics(player):
    metrics = dict(_ensure_funnel_metrics(player))
    return {name: int(metrics.get(name, 0) or 0) for name in FUNNEL_METRIC_DEFAULTS}


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


def _snapshot_companion_details(player):
    companions = getattr(player, "_companions", {}) or {}
    details = {}
    for name, data in companions.items():
        if not isinstance(data, dict):
            continue
        details[str(name)] = {
            "status": str(data.get("status", "unknown")),
            "type": str(data.get("type", "unknown")),
            "happiness": int(data.get("happiness", 0) or 0),
            "days_owned": int(data.get("days_owned", 0) or 0),
            "fed_today": bool(data.get("fed_today", False)),
            "bonded": bool(data.get("bonded", False)),
        }
    return details


def _companion_details(player):
    return _snapshot_companion_details(player)


def _companion_count(player):
    return len(_companion_details(player))


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
    text = " ".join(str(part) for part in args if part is not None)
    text = ANSI_RE.sub("", text)
    if text:
        _story_file.write(text)
        _story_file.flush()


def _is_menu_separator_line(line):
    stripped = str(line or "").strip().lower()
    if not stripped:
        return True
    if stripped.startswith("---") and stripped.endswith("---"):
        return True
    return "adventure destinations" in stripped


def _get_recent_menu_options(limit=40):
    recent_lines = RECENT_TEXT[-limit:]
    trailing_block = []
    started = False
    for line in reversed(recent_lines):
        match = re.match(r"^(\d+)\.\s+(.*)$", line)
        if match:
            trailing_block.append((int(match.group(1)), match.group(2).strip()))
            started = True
            continue
        if started:
            if _is_menu_separator_line(line):
                continue
            break
    trailing_block.reverse()
    if trailing_block:
        return trailing_block

    options = []
    for line in recent_lines:
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


def _resolve_numeric_menu_options(option_values, limit=40):
    menu_options = _get_recent_menu_options(limit=limit)
    allowed_numbers = {int(str(value).strip()) for value in option_values if str(value).strip().isdigit()}
    if not allowed_numbers:
        return menu_options

    non_numeric_values = [str(value).strip() for value in option_values if not str(value).strip().isdigit()]

    filtered = [(number, label) for number, label in menu_options if number in allowed_numbers]
    if non_numeric_values and menu_options:
        exit_candidates = [entry for entry in menu_options if entry[0] not in allowed_numbers]
        if len(exit_candidates) == 1:
            filtered.append(exit_candidates[0])
    if len(filtered) == len(allowed_numbers):
        filtered.sort(key=lambda entry: entry[0])
        return filtered

    if non_numeric_values and len(filtered) == len(allowed_numbers) + 1:
        filtered.sort(key=lambda entry: entry[0])
        return filtered

    return [(number, str(number)) for number in sorted(allowed_numbers)]


def _looks_like_numeric_menu_prompt(options):
    if not options:
        return False
    normalized = [str(option).strip().lower() for option in options]
    allowed_tokens = {"leave", "nothing", "none", "cancel"}
    return all(token.isdigit() or token in allowed_tokens for token in normalized)


def _looks_like_afternoon_destination_menu(menu_options, prompt_lower="", recent="", recent_short=""):
    if not menu_options:
        return False

    labels = [str(label).strip().lower() for _number, label in menu_options]
    has_stay_home = "stay home" in labels
    route_labels = {
        "doctor's office",
        "witch doctor's tower",
        "trusty tom's trucks and tires",
        "filthy frank's flawless fixtures",
        "oswald's optimal outoparts",
        "convenience store",
        "marvin's mystical merchandise",
        "grimy gus's pawn emporium",
        "vinnie's back alley loans",
        "airport",
        "make a phone call",
        "tanya's office",
        "car workbench",
        "wander off",
    }
    has_route_label = any(label in route_labels or label.startswith("drive to ") for label in labels)

    if has_stay_home and has_route_label:
        return True

    afternoon_markers = (
        "how do you want to spend the rest of your afternoon",
        "your wagon isn't road-ready",
        "places you can reach before sundown",
        "would you like to spend your day driving somewhere",
    )
    combined_text = "\n".join((prompt_lower, recent, recent_short))
    return any(marker in combined_text for marker in afternoon_markers) and has_route_label


def _map_numeric_choice_to_option_token(chosen_number, option_values):
    chosen_text = str(chosen_number)
    raw_values = [str(value).strip() for value in option_values]
    if chosen_text in raw_values:
        return chosen_text

    numeric_values = [int(value) for value in raw_values if value.isdigit()]
    non_numeric_values = [value for value in raw_values if not value.isdigit()]
    if non_numeric_values and numeric_values and int(chosen_number) == max(numeric_values) + 1:
        return non_numeric_values[0]
    if non_numeric_values and chosen_text not in raw_values:
        return non_numeric_values[0]
    return chosen_text


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


def _current_story_prompt_source():
    stack = inspect.stack()
    try:
        for frame_info in stack[1:]:
            filename = os.path.abspath(frame_info.filename)
            if not filename.startswith(STORY_ROOT):
                continue
            self_obj = frame_info.frame.f_locals.get("self")
            class_name = self_obj.__class__.__name__ if self_obj is not None else ""
            return {
                "story_source_function": frame_info.function,
                "story_source_file": os.path.basename(filename),
                "story_source_class": class_name,
            }
    finally:
        del stack
    return {}


def _request_metadata(*parts):
    merged = dict(_current_story_prompt_source())
    for part in parts:
        if part:
            merged.update(part)
    return merged


def _record_decision_trace(trace):
    if trace is not None:
        # Enrich trace with game text context for the decision tree.
        # metadata dict is mutable even on a frozen dataclass.
        meta = trace.metadata
        if meta is None:
            meta = {}
        if "raw_recent_text" not in meta:
            meta["raw_recent_text"] = tuple(RECENT_TEXT[-20:])
        if "raw_prompt_text" not in meta and DECISION_REQUESTS:
            last_req = DECISION_REQUESTS[-1]
            req_cycle = last_req.metadata.get("cycle") if last_req.metadata else None
            if req_cycle == CURRENT_CYCLE:
                meta["raw_prompt_text"] = last_req.raw_prompt_text or ""
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
        metadata=_request_metadata({
            "cycle": CURRENT_CYCLE,
        }, metadata),
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
        metadata=_request_metadata({
            "cycle": CURRENT_CYCLE,
            "day": game_state.day,
        }, metadata),
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
        metadata=_request_metadata({
            "cycle": CURRENT_CYCLE,
            "day": game_state.day,
        }, metadata),
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
        metadata=_request_metadata({
            "cycle": CURRENT_CYCLE,
            "day": game_state.day,
            "balance": game_state.balance,
            "rank": game_state.rank,
        }, metadata),
    )
    _record_decision_request(request)
    plan = choose_strategic_goal(game_state)
    if player is not None and hasattr(player, "request_progress_goal"):
        player.request_progress_goal(
            plan.goal,
            reason=plan.reason,
            source=f"planner:{request_type}",
            sticky=plan.goal in {"acquire_car", "unlock_marvin", "reach_adventure_threshold"},
        )

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
    if player is not None and hasattr(player, "request_progress_goal"):
        player.request_progress_goal(
            strategic_goal,
            reason=reason,
            source=f"interrupt:{interrupt_kind}",
            sticky=strategic_goal in {"acquire_car", "unlock_marvin", "reach_adventure_threshold"},
        )
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


def _is_protected_pawn_item(item_name):
    # Keep long-run progression intact: do not pawn Marvin/workbench unlock items.
    return item_name in {"Map", "Worn Map", "Tool Kit"}


def _sellable_collectibles(player):
    if player is None or not hasattr(player, "get_collectible_prices"):
        return []
    sellable = []
    for item in player.get_collectible_prices().keys():
        if player.has_item(item) and not _is_protected_pawn_item(item):
            sellable.append(item)
    return sellable


def _planned_pawn_sales(player):
    if player is None or not hasattr(player, "get_collectible_prices"):
        return []

    owned = []
    for item_name, price in player.get_collectible_prices().items():
        if player.has_item(item_name) and not _is_protected_pawn_item(item_name):
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

    store_summary = _store_chore_summary(player)
    store_candidates = _store_purchase_candidates(player)
    planned_sales = _planned_pawn_sales(player)
    collectible_prices = player.get_collectible_prices() if hasattr(player, "get_collectible_prices") else {}
    pawn_planned_sale_value = sum(int(collectible_prices.get(item_name, 0) or 0) for item_name in planned_sales)
    marvin_affordable_priority = _best_marvin_affordable_priority(player) if _has_marvin_access(player) else 0
    marvin_candidate = _best_marvin_candidate(player, player.get_balance()) if _has_marvin_access(player) else None
    marvin_future_candidate = _best_future_marvin_candidate(player, player.get_balance()) if _has_marvin_access(player) else None
    marvin_candidate_price = 0 if marvin_candidate is None else int(marvin_candidate[1])
    marvin_future_priority = 0 if marvin_future_candidate is None else int(marvin_future_candidate["priority"])
    marvin_future_shortfall = 0 if marvin_future_candidate is None else int(marvin_future_candidate["shortfall"])
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
                rank >= 2
                and marvin_candidate[0] >= 72
                and player.get_balance() >= max(12000, marvin_candidate_price + max(1500, int(tuner["marvin_floor_buffer"] * 0.2)))
            )
            or (
                rank >= 2
                and player.get_balance() >= 25000
                and marvin_candidate[0] >= 68
                and player.get_balance() >= marvin_candidate_price + max(1200, _doctor_cash_reserve(player))
            )
            or (
                rank <= 1
                and marvin_candidate[0] >= 60
                and player.get_balance() >= max(1400, marvin_candidate_price + max(200, int(tuner["marvin_floor_buffer"] * 0.2)))
            )
            or (
                rank <= 1
                and marvin_candidate[0] >= 44
                and player.get_balance() >= max(1050, marvin_candidate_price + 50)
            )
            or (
                rank <= 1
                and has_only_worn_map_access
                and marvin_candidate[0] >= 50
                and player.get_balance() >= max(1200, marvin_candidate_price + 100)
            )
        )
    )
    craft_candidate = _workbench_best_craft_candidate(player)
    return {
        "store_candidate_count": int(store_summary["count"]),
        "store_best_priority": int(store_summary["top"][0]) if store_summary["top"] else 0,
        "store_target_spend": int(store_summary["top"][1]) if store_summary["top"] else 0,
        "store_actionable_count": int(store_summary["actionable_count"]),
        "crafting_best_priority": int(craft_candidate[1]) if craft_candidate else 0,
        "pawn_sellable_value": _sellable_collectible_value(player),
        "pawn_planned_sale_count": len(planned_sales),
        "pawn_planned_sale_value": pawn_planned_sale_value,
        "marvin_affordable_priority": int(marvin_affordable_priority),
        "marvin_candidate_price": marvin_candidate_price,
        "marvin_future_priority": marvin_future_priority,
        "marvin_future_shortfall": marvin_future_shortfall,
        "marvin_strong_window": int(marvin_strong_window),
        "fake_cash": int(player.get_fraudulent_cash()) if hasattr(player, "get_fraudulent_cash") else 0,
        "edge_score": _blackjack_edge_score(player),
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


def _car_mechanic_name(player):
    if player is None:
        return None
    if hasattr(player, "get_car_mechanic"):
        mechanic = player.get_car_mechanic()
        if mechanic not in {None, "", "None"}:
            return str(mechanic)
    if not player.has_item("Car"):
        return None
    met_mechanics = [name for name in ["Tom", "Frank", "Oswald"] if player.has_met(name)]
    if len(met_mechanics) == 1:
        return met_mechanics[0]
    return None


def _mechanic_dream_counts(player):
    if player is None:
        return {"Tom": 0, "Frank": 0, "Oswald": 0}

    return {
        "Tom": int(player.get_tom_dreams()) if hasattr(player, "get_tom_dreams") else 0,
        "Frank": int(player.get_frank_dreams()) if hasattr(player, "get_frank_dreams") else 0,
        "Oswald": int(player.get_oswald_dreams()) if hasattr(player, "get_oswald_dreams") else 0,
    }


def _mechanic_story_focus_name(player, available_names=None):
    available = set(available_names or ())
    if not available:
        available = {name for name, _shop_label, _visit_label in _available_mechanic_routes(player)}
    if not available:
        return None

    car_mechanic = _car_mechanic_name(player)
    if car_mechanic in available:
        return car_mechanic

    chosen = _chosen_mechanic_name(player)
    if chosen in available:
        return chosen

    dream_counts = _mechanic_dream_counts(player)
    tie_order = {"Tom": 3, "Frank": 2, "Oswald": 1}
    dream_candidates = [name for name in available if dream_counts.get(name, 0) > 0]
    if dream_candidates:
        return max(dream_candidates, key=lambda name: (dream_counts.get(name, 0), tie_order.get(name, 0)))

    return None


def _mechanic_dream_reserve(player):
    if player is None or not player.has_item("Car"):
        return 0

    balance = player.get_balance()
    if balance <= 0:
        return 0

    dream_counts = _mechanic_dream_counts(player)
    if (
        dream_counts["Tom"] >= 2
        and dream_counts["Frank"] >= 2
        and dream_counts["Oswald"] >= 2
        and balance >= 750000
        and not player.has_met("Final Dream")
    ):
        return 750000

    focus = _mechanic_story_focus_name(player)
    if focus is None:
        return 0

    focus_dreams = dream_counts.get(focus, 0)
    threshold = 0
    if focus_dreams <= 0 and balance >= 1000:
        threshold = 1000
    elif focus_dreams == 1 and balance >= 10000:
        threshold = 10000
    elif focus_dreams == 2 and balance >= 400000:
        threshold = 400000
    elif focus == "Frank" and focus_dreams >= 3 and balance >= 100000 and not player.has_met("Dealer Dream Complete"):
        threshold = 100000

    return min(balance, threshold)


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
    car_mechanic = _car_mechanic_name(player)
    if car_mechanic in available_by_name:
        return available_by_name[car_mechanic]

    chosen = _chosen_mechanic_name(player)
    if chosen in available_by_name:
        return available_by_name[chosen]

    if _needs_oswald_attention(player) and "Oswald" in available_by_name:
        return available_by_name["Oswald"]

    focus_name = _mechanic_story_focus_name(player, available_by_name)
    if focus_name in available_by_name:
        return available_by_name[focus_name]

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

    return any(
        player.has_met(name)
        for name in ("Tom Event", "Frank Event", "Oswald Event", "Tom", "Frank", "Oswald")
    )


def _companion_metrics(player):
    companions = _companion_details(player)
    if not companions:
        return {
            "count": 0,
            "low": 0,
            "runaway": 0,
            "unfed": 0,
            "bond_window": 0,
        }

    metrics = {
        "count": len(companions),
        "low": 0,
        "runaway": 0,
        "unfed": 0,
        "bond_window": 0,
    }
    for data in companions.values():
        happiness = int(data.get("happiness", 50))
        days_owned = int(data.get("days_owned", 0))
        fed_today = bool(data.get("fed_today", False))
        bonded = bool(data.get("bonded", False))
        if happiness <= 45:
            metrics["low"] += 1
        if happiness <= 15:
            metrics["runaway"] += 1
        if not fed_today:
            metrics["unfed"] += 1
        if happiness >= 70 and days_owned >= 6 and not bonded:
            metrics["bond_window"] += 1
    return metrics


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
        companion_metrics = _companion_metrics(player)
        priority += min(10, companion_count * 2)
        if companion_metrics["runaway"] > 0:
            priority += 46
        elif companion_metrics["low"] > 0:
            priority += 30
        elif companion_metrics["bond_window"] > 0:
            priority += 18
        elif companion_metrics["unfed"] > 0:
            priority += 12

    return priority


def _gift_run_ready(player):
    if player is None:
        return False
    if not hasattr(player, "is_gift_system_unlocked") or not hasattr(player, "has_gift_wrapped"):
        return False
    if player.is_gift_system_unlocked():
        _set_funnel_day_once(player, "gift_unlock_day")
    return (
        player.is_gift_system_unlocked()
        and not player.has_gift_wrapped()
        and _dealer_happiness(player) < (GIFT_WRAP_HAPPINESS_THRESHOLD + 8)
        and player.get_balance() >= 100
        and player.get_health() >= 56
        and player.get_sanity() >= 32
    )


def _dealer_gift_recovery_mode(player):
    if player is None or not _gift_run_ready(player):
        return False
    happiness = _dealer_happiness(player)
    return (
        happiness <= 84
        or (
            happiness <= 88
            and player.get_balance() >= 400
            and player.get_health() >= 66
            and player.get_sanity() >= 36
        )
    )


def _gift_unlock_push_mode(player):
    if player is None:
        return False
    if not hasattr(player, "is_gift_system_unlocked"):
        return False
    if player.is_gift_system_unlocked():
        _set_funnel_day_once(player, "gift_unlock_day")
        return False
    if _dealer_happiness(player) >= GIFT_WRAP_HAPPINESS_THRESHOLD + 4:
        return False
    if _needs_car(player) or _doctor_visit_is_urgent(player):
        return False

    purchases = int(getattr(player, "_convenience_store_purchases", 0) or 0)
    ready = (
        purchases < 3
        and player.get_balance() >= 120
        and player.get_health() >= 56
        and player.get_sanity() >= 30
    )
    if ready:
        _bump_funnel_metric(player, "gift_unlock_push_count")
    return ready


def _wealth_lock_mode(player):
    if player is None or _needs_car(player):
        return False
    if _doctor_visit_is_urgent(player):
        return False
    return (
        player.get_balance() >= 20000
        and player.get_health() >= 62
        and player.get_sanity() >= 32
    )


def _is_companion_food_item(item_name, player):
    if player is None or not hasattr(player, "get_food_data"):
        return False
    food_data = player.get_food_data(item_name)
    return bool(food_data and food_data.get("companion_food"))


def _wants_companion_time(player):
    if player is None:
        return False
    companion_metrics = _companion_metrics(player)
    if companion_metrics["count"] <= 0:
        return False
    if companion_metrics["runaway"] > 0 or companion_metrics["low"] > 0 or companion_metrics["bond_window"] > 0:
        return True
    if player.get_health() < 72 or player.get_sanity() < 55:
        return True
    return companion_metrics["count"] >= 3


def _should_group_with_companions(player):
    if player is None:
        return False
    companion_metrics = _companion_metrics(player)
    companion_count = companion_metrics["count"]
    if companion_count <= 0:
        return False
    if companion_metrics["runaway"] > 0 or companion_metrics["unfed"] >= 2:
        return True
    if companion_metrics["low"] >= 2 or companion_metrics["bond_window"] >= 2:
        return True
    if player.get_health() < 85 or player.get_sanity() < 65:
        return True
    if companion_count >= 3:
        return True
    return False


def _best_companion_name(player):
    companions = _companion_details(player)
    if not companions:
        return None

    best_name = None
    best_score = float("-inf")
    for name, data in companions.items():
        happiness = int(data.get("happiness", 50))
        days_owned = int(data.get("days_owned", 0))
        fed_today = bool(data.get("fed_today", False))
        bonded = bool(data.get("bonded", False))
        score = float(days_owned)
        if happiness <= 15:
            score += 120.0
        elif happiness <= 30:
            score += 70.0
        elif happiness < 50:
            score += 28.0
        if not fed_today:
            score += 26.0
        if happiness >= 70 and days_owned >= 6 and not bonded:
            score += 60.0
        elif happiness >= 80 and not bonded:
            score += 48.0
        if bonded:
            score -= 12.0
        if best_name is None or score > best_score:
            best_name = name
            best_score = score
    return best_name


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


def _route_location_key(label):
    lowered = (label or "").strip().lower()
    if not lowered:
        return None
    if lowered == "doctor's office":
        return "doctor"
    if lowered == "witch doctor's tower":
        return "doctor:witch"
    if "marvin" in lowered:
        return "shop:marvin"
    if "convenience store" in lowered:
        return "shop:convenience_store"
    if "pawn" in lowered or "gus" in lowered:
        return "shop:pawn_shop"
    if "vinnie" in lowered or "loan" in lowered:
        return "shop:loan_shark"
    if "workbench" in lowered:
        return "shop:car_workbench"
    if "trusty tom" in lowered:
        return "mechanic:tom"
    if "frank" in lowered:
        return "mechanic:frank"
    if "oswald" in lowered or "outoparts" in lowered:
        return "mechanic:oswald"
    if lowered.startswith("drive to "):
        return f"route:{lowered}"
    if "stay home" in lowered:
        return "stay_home"
    return f"route:{lowered}"


def _route_circulation_metadata(player, menu_options):
    if player is None:
        return {}
    last_days, counts = _location_history(player)
    current_day = getattr(player, "_day", 1)
    circulation = {}
    for number, label in menu_options:
        option_id = f"route:{number}"
        location_key = _route_location_key(label)
        last_day = None if location_key is None else last_days.get(location_key)
        days_since = None if last_day is None else max(0, current_day - int(last_day))
        visits = 0 if location_key is None else int(counts.get(location_key, 0) or 0)
        circulation[option_id] = {
            "location_key": location_key,
            "days_since": days_since,
            "visits": visits,
        }
    return circulation


def _days_since_location(player, *labels):
    if player is None:
        return None

    last_days, _counts = _location_history(player)
    current_day = getattr(player, "_day", 1)
    candidates = [last_days[label] for label in labels if label in last_days]
    if not candidates:
        return None
    return max(0, current_day - max(candidates))


_STATUS_DAY_MARKS = {
    "spider bite": "Spider Bite",
    "snake bite": "Snake Bite",
    "squirrel bite": "Squirrel Bite",
    "rat bite": "Rat Bite",
    "rabies": "Rabies",
    "cold": "Cold",
    "sore throat": "Sore Throat",
    "hepatitis": "Hepatitis",
}


def _status_days_elapsed(player, status_name):
    if player is None:
        return None
    mark = _STATUS_DAY_MARKS.get(status_name)
    if mark is None or not hasattr(player, "get_days_elapsed"):
        return None
    try:
        return int(player.get_days_elapsed(mark))
    except Exception:
        return None


def _next_cycle_status_damage(status_name, days_elapsed, player):
    if days_elapsed is None:
        return 0
    if status_name == "spider bite":
        if days_elapsed <= 0:
            return 6
        if days_elapsed == 1:
            return 9
        return 15
    if status_name == "snake bite":
        if days_elapsed <= 0:
            return 12
        if days_elapsed == 1:
            return 18
        return 30
    if status_name == "rabies":
        if days_elapsed <= 1:
            return 0
        if days_elapsed == 2:
            return 70
        if days_elapsed == 3:
            return 90
        return 999
    if status_name == "cold":
        if days_elapsed <= 1:
            return 7
        if days_elapsed >= 3:
            return 9
        return 0
    if status_name == "sore throat":
        if player is not None and player.has_item("Cough Drops"):
            return 0
        if days_elapsed <= 1:
            return 5
        if days_elapsed >= 3:
            return 6
        return 0
    if status_name == "hepatitis":
        if days_elapsed <= 0:
            return 7
        if days_elapsed == 1:
            return 12
        if days_elapsed == 2:
            return 20
        if days_elapsed == 3:
            return 25
        return 30
    return 0


def _doctor_risk_profile(player):
    if player is None:
        return {
            "statuses": set(),
            "injuries": set(),
            "health": 0,
            "sanity": 0,
            "effective_health": 0,
            "next_tick_damage": 0,
            "event_buffer": 0,
            "margin": 0,
            "modeled_statuses": 0,
            "severe_injuries": 0,
            "acute_statuses": 0,
            "serious_statuses": 0,
        }

    statuses = _status_names(player)
    injuries = _injury_names(player)
    health = player.get_health()
    sanity = player.get_sanity()
    severe_injury_keywords = {
        "ruptured spleen", "concussion", "broken ribs", "broken leg", "broken ankle",
        "broken wrist", "fractured spine", "torn acl", "whiplash", "punctured lung",
        "dislocated shoulder",
    }
    acute_statuses = {
        "appendicitis", "anaphylaxis", "blood pressure crisis", "dvt", "gangrene", "heat stroke",
        "hypothermia", "kidney stones", "needle exposure", "pancreatitis", "pneumonia",
        "possible rabies", "seizure disorder", "sepsis", "severe asthma", "severe dehydration",
        "staph infection", "tetanus", "uncontrolled diabetes", "waterborne illness",
    }
    serious_statuses = {
        "bronchitis", "gallbladder attack", "malnutrition", "mold toxicity", "lead poisoning",
        "mercury poisoning", "asbestos damage", "tooth abscess", "mushroom poisoning",
        "shellfish poisoning", "lyme disease", "rat bite fever", "second degree burns",
    }
    mental_health_statuses = {
        "anxiety disorder", "severe depression", "chronic insomnia", "ptsd",
    }
    mental_health_count = sum(1 for status in statuses if status in mental_health_statuses)
    sanity_tick_drain = 0
    for status in statuses:
        if status in ("severe depression", "ptsd"):
            sanity_tick_drain += 5
        elif status in ("anxiety disorder", "chronic insomnia"):
            sanity_tick_drain += 4

    next_tick_damage = len(injuries)
    modeled_statuses = 0
    for status in statuses:
        days_elapsed = _status_days_elapsed(player, status)
        if days_elapsed is None:
            continue
        modeled_statuses += 1
        next_tick_damage += _next_cycle_status_damage(status, days_elapsed, player)

    severe_injury_count = sum(1 for injury in injuries if injury in severe_injury_keywords)
    next_tick_damage += severe_injury_count * 5

    acute_status_count = sum(1 for status in statuses if status in acute_statuses)
    serious_status_count = sum(1 for status in statuses if status in serious_statuses)
    next_tick_damage += acute_status_count * 18
    next_tick_damage += serious_status_count * 8
    next_tick_damage += max(0, len(statuses) - modeled_statuses - acute_status_count - serious_status_count - mental_health_count) * 4

    event_buffer = 4
    if len(injuries) >= 1:
        event_buffer += 3
    if len(injuries) >= 2:
        event_buffer += 3
    if len(statuses) >= 2:
        event_buffer += 2
    if health < 55:
        event_buffer += 4
    if health < 40:
        event_buffer += 6
    if sanity < 22:
        event_buffer += 2
    if mental_health_count >= 1 and sanity < 40:
        event_buffer += 4

    effective_health = health
    if player.has_item("LifeAlert"):
        effective_health += 25
    if player.has_item("First Aid Kit"):
        effective_health += 8

    margin = effective_health - next_tick_damage - event_buffer
    return {
        "statuses": statuses,
        "injuries": injuries,
        "health": health,
        "sanity": sanity,
        "effective_health": effective_health,
        "next_tick_damage": next_tick_damage,
        "event_buffer": event_buffer,
        "margin": margin,
        "modeled_statuses": modeled_statuses,
        "severe_injuries": severe_injury_count,
        "acute_statuses": acute_status_count,
        "serious_statuses": serious_status_count,
        "mental_health_statuses": mental_health_count,
        "sanity_tick_drain": sanity_tick_drain,
    }


def _needs_doctor(player):
    if player is None:
        return False
    risk = _doctor_risk_profile(player)
    statuses = risk["statuses"]
    injuries = risk["injuries"]
    rabies_days = _status_days_elapsed(player, "rabies")
    sanity_drain = risk.get("sanity_tick_drain", 0)
    if len(statuses) == 0:
        return (
            _doctor_visit_is_urgent(player)
            or risk["health"] < 26
            or risk["sanity"] < 16
            or (risk["severe_injuries"] >= 1 and risk["health"] < 84)
            or (len(injuries) >= 2 and risk["health"] < 70)
        )
    if sanity_drain > 0 and risk["sanity"] < (sanity_drain * 8):
        return True
    return (
        _doctor_visit_is_urgent(player)
        or risk["health"] < 32
        or risk["sanity"] < 18
        or risk["margin"] <= 14
        or (rabies_days is not None and rabies_days >= 2)
        or (risk["acute_statuses"] >= 1 and risk["health"] < 80)
        or (risk["serious_statuses"] >= 1 and risk["health"] < 62)
        or (len(statuses) >= 3 and risk["margin"] <= 24)
    )


def _doctor_visit_is_urgent(player):
    if player is None:
        return False
    risk = _doctor_risk_profile(player)
    statuses = risk["statuses"]
    urgent_injuries = {"ruptured spleen", "concussion", "broken ribs", "punctured lung"}
    injuries = risk["injuries"]
    rabies_days = _status_days_elapsed(player, "rabies")
    if len(statuses) == 0:
        return risk["health"] < 18 or (risk["health"] <= 24 and any(injury in urgent_injuries for injury in injuries))
    return (
        risk["health"] < 20
        or risk["sanity"] < 10
        or (risk.get("sanity_tick_drain", 0) > 0 and risk["sanity"] < risk.get("sanity_tick_drain", 0) * 4)
        or risk["margin"] <= -10
        or (risk["margin"] <= -2 and risk["health"] < 30)
        or (risk["acute_statuses"] >= 1 and (risk["health"] < 42 or risk["margin"] <= -2))
        or (any(injury in urgent_injuries for injury in injuries) and risk["health"] < 46)
        or (rabies_days is not None and rabies_days >= 3)
        or (len(injuries) >= 3 and risk["health"] < 42)
        or (len(injuries) >= 2 and len(statuses) >= 2 and risk["health"] < 40)
    )


def _doctor_need_score(player):
    if player is None:
        return 0

    risk = _doctor_risk_profile(player)
    score = max(0, 48 - risk["margin"])
    score += max(0, 50 - risk["health"])
    score += max(0, 28 - risk["sanity"]) // 2
    score += len(risk["statuses"]) * 4
    score += len(risk["injuries"]) * 8
    score += risk["acute_statuses"] * 28
    score += risk["serious_statuses"] * 10
    score += risk["severe_injuries"] * 14
    score += risk.get("mental_health_statuses", 0) * 12
    sanity_drain = risk.get("sanity_tick_drain", 0)
    if sanity_drain > 0:
        days_left = max(1, risk["sanity"] // max(1, sanity_drain))
        if days_left <= 8:
            score += max(0, 40 - days_left * 5)
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
        return max(0, int(balance * 0.20))
    return max(0, int(balance * 0.40))


def _doctor_cash_reserve(player):
    """Cash to hold back for a doctor/witch visit that is currently needed.

    Returns 0 when the player is healthy — there is no reason to reserve funds for
    a hypothetical future visit.  Only reserves when a visit is actually warranted.
    """
    if player is None:
        return 0
    if _should_defer_doctor_for_marvin_window(player):
        estimate = _witch_heal_cost_estimate(player) if player.has_met("Witch") else _doctor_heal_cost_estimate(player)
        return min(
            max(40, int(estimate * 0.12)),
            max(0, int(player.get_balance() * 0.08)),
        )
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


def _should_defer_doctor_for_marvin_window(player):
    if player is None or not player.has_item("Car") or not _has_marvin_access(player):
        return False
    if _doctor_visit_is_urgent(player) or not _needs_doctor(player):
        return False

    rank = int(player.get_rank()) if hasattr(player, "get_rank") else 0
    if rank > 2:
        return False

    risk = _doctor_risk_profile(player)
    balance = max(0, int(player.get_balance()))
    marvin_gap = _days_since_location(player, "shop:marvin")

    if marvin_gap == 0:
        return False
    min_health = 66 if rank <= 1 else 72
    min_sanity = 28 if rank <= 1 else 32
    min_margin = 14 if rank <= 1 else 20
    if risk["health"] < min_health or risk["sanity"] < min_sanity:
        return False
    if risk["margin"] <= min_margin:
        return False
    if len(risk["injuries"]) >= 1:
        return False
    if risk["acute_statuses"] >= 1 and risk["health"] < (66 if rank <= 1 else 74):
        return False
    if risk["severe_injuries"] >= 1 and risk["health"] < (62 if rank <= 1 else 70):
        return False
    if risk["serious_statuses"] >= 2 and risk["health"] < (58 if rank <= 1 else 66):
        return False
    if len(risk["statuses"]) >= 2 and risk["health"] < (74 if rank <= 1 else 80):
        return False
    if len(risk["statuses"]) >= 5 or len(risk["injuries"]) >= 3:
        return False

    essential_items = _marvin_essential_items()
    affordable = _best_marvin_candidate(player, balance)
    if affordable is not None:
        priority, price, item_name = affordable
        if (
            item_name in essential_items
            and priority >= (56 if rank <= 1 else 72)
            and balance >= max(1050 if rank <= 1 else 7000, price + 80)
            and balance - price >= _marvin_post_purchase_floor(player, item_name)
        ):
            return True

    future = _best_future_marvin_candidate(player, balance)
    if future is None:
        return False

    item_name = future["item"]
    if item_name not in essential_items:
        return False

    shortfall = int(future["shortfall"])
    priority = int(future["priority"])
    if priority < (64 if rank <= 1 else 78):
        return False
    if shortfall > (min(5200, max(2600, int(balance * 0.95))) if rank <= 1 else min(18000, max(7000, int(balance * 0.85)))):
        return False
    if marvin_gap is not None and marvin_gap <= 1 and shortfall > (2200 if rank <= 1 else 9000):
        return False
    return risk["health"] >= (56 if rank <= 1 else 62) and risk["sanity"] >= (26 if rank <= 1 else 30)


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


def _injury_tick_pressure(player):
    if player is None:
        return 0
    injuries = _injury_names(player)
    severe_injuries = {
        "ruptured spleen", "concussion", "broken ribs", "broken leg", "broken ankle",
        "broken wrist", "fractured spine", "torn acl", "whiplash", "punctured lung",
        "dislocated shoulder",
    }
    return len(injuries) + sum(1 for injury in injuries if injury in severe_injuries)


def _witch_full_cleanse_upside(player):
    if player is None or not player.has_met("Witch"):
        return 0.0
    risk = _doctor_risk_profile(player)
    injury_pressure = _injury_tick_pressure(player)
    if injury_pressure <= 0:
        return 0.0
    upside = injury_pressure * 8.0
    upside += len(risk["statuses"]) * 2.0
    if risk["health"] < 55:
        upside += 8.0
    if risk["margin"] <= 10:
        upside += 10.0
    if player.has_item("Real Insurance"):
        upside *= 0.45
    elif player.has_item("Faulty Insurance"):
        upside *= 0.7
    return upside


def _witch_status_clear_probability(player):
    if player is None:
        return 0.0
    statuses = _status_names(player)
    injuries = _injury_names(player)
    if not statuses and not injuries:
        return 0.0
    # Witch outcomes from locations.py:
    # 50% _clear_status, 10% _clear_all_status, otherwise no cleanse.
    if statuses and injuries:
        return 0.60
    if statuses:
        return 0.60
    if injuries:
        return 0.10
    return 0.0


def _witch_full_heal_probability(player):
    if player is None or not player.has_met("Witch"):
        return 0.0
    return 0.50


def _witch_retry_value(player):
    if player is None or not player.has_met("Witch"):
        return 0.0
    risk = _doctor_risk_profile(player)
    doctor_cost = _doctor_heal_cost_estimate(player)
    witch_cost = _witch_heal_cost_estimate(player)
    if doctor_cost <= witch_cost:
        return 0.0
    retry_value = min(30.0, (doctor_cost - witch_cost) / 8.0)
    if risk["margin"] >= 8:
        retry_value += 8.0
    elif risk["margin"] >= 4:
        retry_value += 4.0
    if risk["health"] >= 42:
        retry_value += 4.0
    retry_value += _witch_full_heal_probability(player) * 12.0
    return retry_value


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
    injury_pressure = _injury_tick_pressure(player)
    cleanse_upside = _witch_full_cleanse_upside(player)
    clear_probability = _witch_status_clear_probability(player)
    heal_probability = _witch_full_heal_probability(player)
    retry_value = _witch_retry_value(player)
    risk = _doctor_risk_profile(player)
    statuses = _status_names(player)
    injuries = _injury_names(player)
    if _doctor_visit_is_urgent(player):
        return balance >= estimated_cost and ((not doctor_available) or doctor_estimated_cost > balance + 40)

    if doctor_available and injuries and not statuses:
        return False
    if doctor_available and injuries and clear_probability < 0.60:
        if doctor_estimated_cost <= max(balance, estimated_cost + 200):
            return False

    if player.has_item("Real Insurance") and doctor_available:
        return False
    if player.has_item("Faulty Insurance") and doctor_available:
        if len(injuries) > 0 or player.get_health() < 64 or player.get_sanity() < 30:
            return False
        if potion_priority < 92:
            return False

    if flask_count >= 3:
        return False
    if balance < estimated_cost:
        return False
    if (
        not _doctor_visit_is_urgent(player)
        and injury_pressure >= 2
        and doctor_available
        and doctor_estimated_cost >= estimated_cost
        and risk["health"] >= 36
        and risk["margin"] >= 4
        and clear_probability >= 0.10
    ):
        return True
    if (
        not _doctor_visit_is_urgent(player)
        and heal_probability >= 0.50
        and doctor_available
        and doctor_estimated_cost >= estimated_cost + 80
        and risk["health"] >= 34
        and risk["margin"] >= 2
        and (injury_pressure >= 1 or len(_status_names(player)) >= 1)
    ):
        return True
    if (
        not _doctor_visit_is_urgent(player)
        and injury_pressure >= 1
        and cleanse_upside >= 18.0
        and doctor_available
        and doctor_estimated_cost >= estimated_cost + 60
        and risk["health"] >= 42
        and risk["sanity"] >= 20
        and (clear_probability >= 0.10 or retry_value >= 10.0)
    ):
        return True
    if (
        not _doctor_visit_is_urgent(player)
        and doctor_available
        and len(injuries) == 0
        and len(statuses) >= 1
        and doctor_estimated_cost >= estimated_cost + 80
        and player.get_health() >= 46
        and player.get_sanity() >= 22
        and clear_probability >= 0.60
    ):
        return True
    if doctor_available and doctor_estimated_cost > balance and balance >= estimated_cost:
        return True
    if doctor_available and doctor_estimated_cost >= max(estimated_cost + 120, int(balance * 0.35)):
        if player.get_health() >= 48 and (len(injuries) == 0 or cleanse_upside >= 20.0 or retry_value >= 12.0):
            return True
    if (
        doctor_available
        and len(statuses) >= 2
        and doctor_estimated_cost >= estimated_cost + 60
        and player.get_health() >= 50
        and player.get_sanity() >= 24
        and (len(injuries) == 0 or cleanse_upside >= 16.0)
        and clear_probability >= 0.60
    ):
        return True
    if potion_priority >= 88 and player.get_health() >= 52 and player.get_sanity() >= 24:
        return True
    if cleanse_upside >= 24.0 and player.get_health() >= 40 and clear_probability >= 0.10:
        return True
    if heal_probability >= 0.50 and retry_value >= 14.0 and risk["margin"] >= 2:
        return True
    if (player.get_health() < 68 or player.get_sanity() < 32) and clear_probability >= 0.60:
        return True
    if score >= 64 and balance >= estimated_cost and (len(injuries) == 0 or cleanse_upside >= 22.0 or retry_value >= 14.0):
        return True
    if balance >= 30000 and score < 140 and potion_priority < 80:
        return False
    return (
        score >= 60 and clear_probability >= 0.60
        or potion_priority >= 72
        or cleanse_upside >= 26.0
        or retry_value >= 16.0
    )


def _wants_witch_flask_only_run(player):
    """Return True when visiting the Witch Doctor purely to buy a flask (no healing needed).

    Verified from locations.py visit_witch_doctor:
      - Heal costs 5-25% of balance (optional — player can say NO).
      - Cheapest flasks are Fortunate Day ($12k-$18k) and Fortunate Night ($12k-$20k).
      - Flask prices are freshly randomised each visit, so we use min estimates to decide
        whether a visit is worth attempting; the bot will skip if the actual price is too high.
    Only fires when:
      - Not already needing healing (use _wants_witch_heal for that path).
      - Has met the Witch and has fewer than 2 active flasks.
      - Balance covers the heal cost buffer PLUS the cheapest affordable flask.
      - Health/sanity are high enough that the visit isn't health-motivated.
    - Has not visited the Witch recently (gap > 5 days).
    - Marvin does NOT have a clearly stronger immediate conversion window waiting.
    """
    if player is None or not player.has_met("Witch"):
        return False
    if _needs_doctor(player):
        return False  # Use _wants_witch_heal for that combined path
    if _flask_count(player) >= 2:
        return False
    if player.get_health() < 68 or player.get_sanity() < 34:
        return False

    witch_gap = _days_since_location(player, "doctor:witch")
    if witch_gap == 0:
        return False
    if witch_gap is not None and witch_gap <= 3:
        return False

    balance = player.get_balance()
    heal_buffer = _witch_heal_cost_estimate(player)
    affordable_priority = _best_affordable_witch_flask_priority(player)
    if affordable_priority < 54:
        return False
    marvin_priority = _best_marvin_affordable_priority(player) if _has_marvin_access(player) else 0
    if _wants_marvin_run(player) and marvin_priority >= 90 and balance < 26000:
        return False
    if _wants_marvin_run(player) and marvin_priority >= 84 and affordable_priority < 88 and balance < 22000:
        return False
    if (
        player.get_rank() >= 2
        and _has_marvin_access(player)
        and balance >= 10000
        and marvin_priority >= 72
        and affordable_priority < 88
        and balance < 18000
    ):
        return False
    visit_buffer = max(120, int(heal_buffer * 0.6))
    # Need balance to comfortably cover the flask purchase plus a heal buffer.
    # The heal is optional (bot will say NO to heal on a flask-only visit) but we
    # keep a buffer to avoid arriving just barely short of the flask price.
    # Find cheapest flask estimate that's affordable AND meets the priority threshold
    for flask_name in ["Fortunate Day", "Fortunate Night", "Dealer's Hesitation",
                       "Anti-Virus", "Anti-Venom", "Dealer's Whispers", "No Bust",
                       "Second Chance", "Bonus Fortune", "Split Serum",
                       "Imminent Blackjack", "Pocket Aces"]:
        priority = _witch_flask_priority(flask_name, player)
        if priority < 58:
            continue
        est = get_witch_flask_price_estimate(flask_name)
        if balance >= est + visit_buffer:
            return True
    return False


def _should_visit_doctor(player):
    if player is None or not _needs_doctor(player):
        return False
    if hasattr(player, "has_danger") and player.has_danger("Doctor Ban"):
        return False

    balance = player.get_balance()
    rank = int(player.get_rank()) if hasattr(player, "get_rank") else 0
    urgent = _doctor_visit_is_urgent(player)
    score = _doctor_need_score(player)
    risk = _doctor_risk_profile(player)
    estimated_cost = _doctor_heal_cost_estimate(player)
    last_doctor_gap = _days_since_location(player, "doctor")
    injuries = risk["injuries"]
    statuses = risk["statuses"]
    rabies_days = _status_days_elapsed(player, "rabies")

    if len(statuses) == 0:
        if len(injuries) == 0:
            return balance >= estimated_cost and (urgent or risk["health"] < 30)
        if balance < estimated_cost:
            return False
        if urgent:
            return True
        return (
            (risk["severe_injuries"] >= 1 and risk["health"] < 84)
            or (len(injuries) >= 2 and risk["health"] < 70)
            or (risk["health"] < 22 and not player.has_item("LifeAlert"))
        )

    if not urgent:
        if last_doctor_gap == 0:
            return False
        if last_doctor_gap is not None and last_doctor_gap <= 1:
            return False
        if last_doctor_gap is not None and last_doctor_gap <= 2 and score < 108:
            return False

    if balance < estimated_cost:
        return False

    if player.has_item("Real Insurance"):
        if urgent:
            return True
        return (
            risk["margin"] <= 8
            or (risk["acute_statuses"] >= 1 and risk["health"] < 82)
            or (risk["severe_injuries"] >= 1 and risk["health"] < 58)
            or (len(statuses) >= 3 and risk["health"] < 50)
        )

    if player.has_item("Faulty Insurance"):
        if urgent:
            return True
        return (
            risk["margin"] <= 6
            or (risk["acute_statuses"] >= 1 and risk["health"] < 78)
            or (risk["severe_injuries"] >= 1 and risk["health"] < 54)
            or (len(statuses) >= 3 and risk["health"] < 46)
        )

    if _wants_witch_heal(player) and not urgent:
        if len(statuses) <= 2 or _witch_full_cleanse_upside(player) >= 18.0:
            return False

    if _wants_witch_heal(player) and not urgent and _witch_full_cleanse_upside(player) >= 14.0:
        return False

    if urgent:
        return True

    if (
        player.has_item("Car")
        and balance >= max(estimated_cost, 5000 if rank <= 1 else 12000)
        and (
            (len(injuries) >= 1 and risk["health"] < (82 if rank <= 1 else 88))
            or (len(statuses) >= 1 and risk["health"] < (78 if rank <= 1 else 84))
            or (risk["margin"] <= (22 if rank <= 1 else 28) and (len(injuries) >= 1 or len(statuses) >= 1))
        )
    ):
        return True

    if (
        balance >= max(1200, estimated_cost)
        and player.has_item("Car")
        and (
            (len(injuries) >= 1 and risk["health"] < 64)
            or (len(statuses) >= 2 and risk["health"] < 70)
            or (risk["margin"] <= 18 and (len(injuries) >= 1 or len(statuses) >= 1))
        )
    ):
        return True

    return (
        risk["margin"] <= 4
        or risk["health"] < 34
        or (risk["sanity"] < 18 and risk["health"] < 52)
        or (rabies_days is not None and rabies_days >= 2)
        or (risk["acute_statuses"] >= 1 and risk["health"] < 74)
        or (risk["serious_statuses"] >= 1 and risk["health"] < 42)
        or (risk["severe_injuries"] >= 1 and risk["health"] < 48)
        or (len(injuries) >= 2 and risk["health"] < 46)
        or (len(statuses) >= 3 and risk["health"] < 42)
    )


def _progression_phase(player):
    if player is None:
        return "unknown"
    if _bankroll_emergency_mode(player):
        return "bankroll_emergency"
    if _fragile_post_car_recovery_mode(player):
        return "car_recovery"
    if _wealth_lock_mode(player):
        return "wealth_lock"
    if _needs_car(player):
        return "car_rush"
    if _marvin_push_window(player):
        return "marvin_push"
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


def _bankroll_emergency_mode(player):
    if player is None:
        return False
    return int(player.get_balance()) <= 0


def _fragile_post_car_recovery_mode(player):
    if player is None or _needs_car(player):
        return False

    balance = int(player.get_balance())
    if balance <= 0:
        return False

    rank = int(player.get_rank()) if hasattr(player, "get_rank") else 0
    health = int(player.get_health()) if hasattr(player, "get_health") else 0
    sanity = int(player.get_sanity()) if hasattr(player, "get_sanity") else 0
    debt = int(player.get_loan_shark_debt()) if hasattr(player, "get_loan_shark_debt") else 0
    warning = int(player.get_loan_shark_warning_level()) if hasattr(player, "get_loan_shark_warning_level") else 0
    if rank >= 2 and balance >= 2500 and health >= 62 and sanity >= 32 and debt <= 0 and warning <= 0:
        return False
    if balance < 120:
        return True
    if balance < 250 and (health < 70 or sanity < 34 or debt > 0 or warning > 0):
        return True
    if balance < 400 and (health < 58 or sanity < 28 or warning >= 2):
        return True
    if RUN_PEAK_BALANCE >= max(1200, balance * 3) and balance < max(250, int(RUN_PEAK_BALANCE * 0.15)):
        return True
    return False


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


def _rank_protection_floor(player):
    """Minimum balance to keep so a single purchase can't drop the player out of their rank.

    At ranks > 1 there should be strict rules about catastrophic spending.  The floor
    is the balance threshold of the CURRENT rank — a rank-2 player ($10k–$99k) should
    not spend down below $10,000 (the rank-2 entry threshold) in one shot.

    This prevents the bot from wiping out its rank cushion with a single low-priority
    purchase.  High-priority items (≥88) already have their own push-window override.

    Returns 0 at rank 0/1 because those ranks have minimal consequence.
    """
    if player is None:
        return 0
    rank = int(player.get_rank())
    # Balance thresholds per rank (index = rank): 0→$0, 1→$1k, 2→$10k, 3→$100k, 4→$400k, 5→$750k.
    # Rank 6+ shares the $750k protection floor until the millionaire ending resolves.
    # Must stay in sync with _rank_from_balance() and usage in Marvin buy decision.
    thresholds = [0, 1000, 10000, 100000, 400000, 750000]
    if rank <= 1:
        return 0
    return thresholds[min(rank, len(thresholds) - 1)]


def _in_rank_push_window(player):
    """True when the bot is actively pushing toward the next rank or a win milestone.

    Used to unlock more aggressive spend/loan decisions — e.g. borrowing right before
    a Marvin purchase so the post-purchase balance stays healthy, or allowing a deeper
    balance dip when buying a high-priority edge item.  The gate prevents these more
    aggressive strategies from firing during ordinary grinding when any downside is
    hard to recover from.
    """
    if player is None or not player.has_item("Car"):
        return False
    if _wants_doctor_visit(player) or _doctor_visit_is_urgent(player):
        return False
    if player.get_health() < 50 or player.get_sanity() < 24:
        return False

    balance = player.get_balance()
    rank = int(player.get_rank())
    target = _rank_target(balance)   # next rank threshold
    floor = _rank_floor(balance)     # current rank floor

    stall_days = _progress_stall_days(player)

    # "Pushing for a rank up": within the top half of the current rank bracket,
    # OR in the lower half but with a clear Marvin target identified.
    # e.g. rank 1 ($1k–$10k): pushing when balance >= $4.6k (= 1k + 40%*9k).
    # e.g. rank 2 ($10k–$100k): pushing when balance >= $28k (= 10k + 20%*90k).
    # We use a low 20% threshold for rank 2+ because rank brackets are wide and
    # the loan-before-Marvin strategy is most valuable early in the bracket.
    push_pct = 0.12 if rank >= 2 else 0.40
    rank_span = max(1, target - floor)
    push_threshold = floor + int(rank_span * push_pct)

    # "Pushing for a win": at rank 2+ with strong edge, healthy state — not
    # necessarily near the rank ceiling but positioned to sustain aggressive play.
    pushing_for_win = (
        rank >= 2
        and _blackjack_edge_score(player) >= 4
        and player.get_health() >= 65
        and player.get_sanity() >= 32
        and balance >= floor + int(rank_span * 0.06)
    )

    future_candidate = _best_future_marvin_candidate(player, balance)
    essential_marvin_push = (
        future_candidate is not None
        and future_candidate["item"] in _marvin_essential_items()
        and future_candidate["shortfall"] <= max(5500 if rank <= 1 else 16000, int(balance * (1.05 if rank <= 1 else 0.85)))
    )

    if stall_days > 12 and not essential_marvin_push:
        return False

    return balance >= push_threshold or pushing_for_win or essential_marvin_push


def _needs_recovery_day(player):
    # AGGRESSIVE: Never force recovery - let route policy handle it
    # Only return True in absolute life-threatening emergencies
    if player is None:
        return False
    if _doctor_visit_is_urgent(player):
        return False
    
    health = player.get_health()
    sanity = player.get_sanity()
    
    # Only if literally about to die
    if health <= 10 or sanity <= 5:
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
    doctor_reserve = _doctor_cash_reserve(player)
    stranded_no_car = _stranded_no_car_mode(player)

    if stranded_no_car:
        reserve = 15

    if player.has_item("Car"):
        reserve = max(reserve, 40)
    if balance < 1000 and player.has_item("Car"):
        reserve = max(reserve, 60)

    reserve = max(reserve, doctor_reserve)

    if stranded_no_car:
        reserve = min(reserve, max(15, min(balance, 45 if balance < 150 else 70 if balance < 400 else 90)))

    if floor:
        if priority >= 90:
            reserve = max(reserve, int(floor * tuner["floor_keep_high"]))
        elif priority >= 75:
            reserve = max(reserve, int(floor * tuner["floor_keep_mid"]))
        else:
            reserve = max(reserve, int(floor * tuner["floor_keep_base"]))

    rank = int(player.get_rank()) if hasattr(player, "get_rank") else 0
    if player.has_item("Car") and rank == 1:
        if balance >= 8500:
            reserve = max(reserve, 2600)
        elif balance >= 7000:
            reserve = max(reserve, 1800)
    elif player.has_item("Car") and rank == 2:
        if balance < 15000:
            reserve = max(reserve, 6500)
        elif balance < 25000:
            reserve = max(reserve, max(7000, int(balance * 0.40)))

    # Rank protection: at ranks > 1, do not let optional spending drop the player
    # more than one full rank.  This is a hard lower bound — the tuner coefficients
    # above already keep the balance near the CURRENT rank floor, but if the current
    # balance is far above that floor (e.g. $50k at rank 2) the protection floor
    # matters for ensuring a single large purchase cannot drop two ranks at once.
    protection_floor = _rank_protection_floor(player)
    if protection_floor > 0:
        if priority >= 88 and _in_rank_push_window(player):
            protection_floor = max(doctor_reserve, int(protection_floor * 0.70))
        elif rank == 2 and priority >= 80 and balance < 26000:
            protection_floor = max(doctor_reserve, int(protection_floor * 0.80))
        reserve = max(reserve, protection_floor)

    return min(balance, reserve)


def _can_afford_optional_purchase(player, price, priority=0):
    if player is None or price is None:
        return False
    balance = player.get_balance()
    if balance < price:
        return False
    return balance - price >= _cash_safety_reserve(player, priority)


def _can_afford_store_purchase(player, price, priority, item_name):
    if player is None or price is None or item_name is None:
        return False
    balance = player.get_balance()
    if balance < price:
        return False
    if _can_afford_optional_purchase(player, price, priority):
        return True

    post_purchase_balance = balance - price
    reserve = _cash_safety_reserve(player, priority)
    shortfall = reserve - post_purchase_balance
    if shortfall <= 0:
        return True

    rank = int(player.get_rank()) if hasattr(player, "get_rank") else 0
    health = player.get_health()
    sanity = player.get_sanity()
    if item_name == "Tool Kit" and player.has_item("Car") and not player.has_item("Tool Kit"):
        return rank <= 2 and health >= 58 and sanity >= 30 and shortfall <= 220
    if item_name in STORE_MUST_HAVE_ITEMS and priority >= 88:
        return health >= 60 and sanity >= 30 and shortfall <= 140
    if player.has_item("Tool Kit") and priority >= 78:
        return health >= 62 and sanity >= 32 and shortfall <= 90
    return False


def _item_happiness_value(item_name):
    """Return the dealer happiness delta for gifting this item. Used to prioritize happiness-boosting items."""
    ITEM_HAPPINESS_MAP = {
        "Dealer's Joker": 30,
        "Ace of Spades": 25,
        "Vintage Wine": 22,
        "Golden Compass": 20,
        "Antique Pocket Watch": 18,
        "Leather Gloves": 17,
        "Fancy Pen": 16,
        "Silver Flask": 15,
        "Moon Shard": 15,
        "Mirror of Duality": 15,
        "Lucky Rabbit Foot": 14,
        "Mysterious Envelope": 13,
        "Deck of Cards": 12,
        "Old Photograph": 12,
        "Gambler's Grimoire": 10,
        "Mysterious Lockbox": 8,
        "Pocket Watch": 5,
        "Sandwich": 3,
        "Energy Drink": 2,
        "Lucky Coin": 0,
        "Cursed Coin": -15,
        "Necronomicon": -20,
        "Voodoo Doll": -25,
        "Stolen Watch": -50,
        "Dealer's Grudge": -40,
    }
    return ITEM_HAPPINESS_MAP.get(item_name, 5)  # Default +5 for unlisted items


def _available_store_inventory(player):
    if player is None:
        return []
    return list(getattr(player, "_convenience_store_inventory", []))


def _store_item_priority(item_name, player):
    if player is None:
        return 0

    rank = int(player.get_rank()) if hasattr(player, "get_rank") else 0
    balance = player.get_balance()

    if player.has_item(item_name):
        return 0

    food_priority = _store_food_priority(item_name, player)
    priority = max(food_priority, get_store_base_priority(item_name))

    # When dealer happiness is low, boost high-value gift items proportionally
    # This encourages strategic gift purchases to recover happiness while still buying
    # aggressively for other utility items.
    dealer_happiness = _dealer_happiness(player)
    if dealer_happiness < 78 and _gift_run_ready(player):
        item_happiness = _item_happiness_value(item_name)
        if item_happiness >= 10:
            # Scale boost based on how low happiness is: at dh=0, boost is +24 for +22 items
            happiness_deficit = max(0, 78 - dealer_happiness)
            base_boost = min(24, int(item_happiness * 1.0))
            deficit_modifier = (happiness_deficit / 78.0)
            happiness_boost = int(base_boost * (0.5 + deficit_modifier * 0.5))
            priority = max(priority, 76 + happiness_boost)

    if item_name == "LifeAlert" and player.get_health() < 95:
        priority += 10
    if item_name == "Worn Map" and player.has_item("Car") and not player.has_item("Map"):
        priority += 34 if rank <= 1 else 16
        if not _has_marvin_access(player) and rank <= 1:
            priority = max(priority, 96)
    if item_name == "Tool Kit" and player.has_item("Car") and not player.has_item("Tool Kit"):
        priority += 22 if rank <= 1 else 12
    if item_name == "First Aid Kit" and (player.get_health() < 90 or _needs_doctor(player)):
        priority += 14
        if not player.has_item("Real Insurance") and not player.has_item("Faulty Insurance"):
            priority += 10
        if _doctor_need_score(player) >= 42:
            priority += 12
        if rank <= 1 and player.has_item("Car"):
            priority += 8
    if item_name in {"Water Bottles", "Duct Tape", "Bug Spray"} and _doctor_need_score(player) >= 36:
        priority += 6
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
    # Crafting synergy: if this item is an ingredient in a high-priority recipe and
    # the player has a Tool Kit, boost the priority so that crafting ingredients
    # trigger store visits even before the other ingredients are in inventory.
    # This breaks the chicken-and-egg deadlock where neither ingredient of a two-
    # ingredient recipe would ever be bought because the other wasn't present first.
    # Two tiers:
    #   - "completing" boost: all other ingredients present → recipe_priority + 16
    #     Applies at ALL ranks — a permanent crafted item is always worth a store trip.
    #   - "starting" boost:   no other ingredients yet       → recipe_priority + 6
    #     Applies up to rank 2 (or rank 3+ when balance < 50k) to seed ingredient chains.
    if player.has_item("Tool Kit"):
        try:
            for recipe_name, recipe in player._lists.get_crafting_recipes().items():
                if player.has_item(recipe_name):
                    continue  # already crafted this recipe
                ingredients = recipe.get("ingredients", [])
                if item_name not in ingredients:
                    continue
                recipe_priority = get_crafting_recipe_priority(recipe_name)
                if recipe_priority < CRAFTING_MIN_PRIORITY:
                    continue
                others = [ing for ing in ingredients if ing != item_name]
                if all(player.has_item(ing) for ing in others):
                    # Completing boost: buying this finishes the recipe — always worth it
                    priority = max(priority, recipe_priority + 16)
                elif rank <= 2 or balance < 50000:
                    # Starting boost: buying this makes progress toward the recipe
                    priority = max(priority, recipe_priority + 6)
                break
        except Exception:
            pass
    return priority


def _store_chore_candidates(player):
    if player is None:
        return []

    balance = player.get_balance()
    chores = []
    for item_name, price in _available_store_inventory(player):
        priority = _store_item_priority(item_name, player)
        if priority <= 0:
            continue
        affordable = price <= balance
        actionable = affordable and _can_afford_store_purchase(player, price, priority, item_name)
        chores.append((priority, price, item_name, actionable, affordable))

    chores.sort(key=lambda entry: (-entry[0], not entry[3], not entry[4], entry[1], entry[2]))
    return chores


def _store_chore_summary(player):
    chores = _store_chore_candidates(player)
    affordable = [entry for entry in chores if entry[4]]
    actionable = [entry for entry in chores if entry[3]]
    top = affordable[0] if affordable else (chores[0] if chores else None)
    return {
        "chores": chores,
        "affordable": affordable,
        "actionable": actionable,
        "top": top,
        "count": len(affordable),
        "actionable_count": len(actionable),
    }


def _store_purchase_candidates(player):
    if player is None:
        return []

    candidates = []
    for priority, price, item_name, actionable, _affordable in _store_chore_candidates(player):
        if not actionable:
            continue
        candidates.append((priority, price, item_name))

    candidates.sort(key=lambda entry: (-entry[0], entry[1], entry[2]))
    return candidates


def _store_buyout_candidate(player, balance=None):
    if player is None or _needs_car(player) or _doctor_visit_is_urgent(player):
        return None
    if player.get_health() < 68 or player.get_sanity() < 38:
        return None

    budget = max(0, int(player.get_balance() if balance is None else balance))
    if budget <= 0:
        return None

    affordable = []
    for priority, price, item_name in _store_purchase_candidates(player):
        if price > budget or priority < 50:
            continue
        affordable.append((priority, price, item_name))

    if len(affordable) < 2:
        return None

    bundle = []
    target_spend = 0
    for priority, price, item_name in affordable:
        if len(bundle) >= 3:
            break
        if bundle and priority < 58:
            break
        bundle.append((priority, price, item_name))
        target_spend += price

    if len(bundle) < 2:
        return None

    rank = int(player.get_rank()) if hasattr(player, "get_rank") else 0
    # Lower the early-game balance gate so the store gets "bought out" sooner.
    # Rank 0 players can trigger a buyout at 700+ (previously 2200) to ensure
    # multiple items are grabbed in one visit before Marvin becomes the focus.
    balance_gate = 700 if rank <= 0 else (1800 if rank <= 1 else 8000)
    best_priority = int(bundle[0][0])
    if budget < balance_gate and best_priority < 84:
        return None
    if budget < balance_gate and target_spend < max(120, int(budget * 0.12)):
        return None

    _bump_funnel_metric(player, "store_buyout_ready_count")

    return {
        "count": len(bundle),
        "priority": best_priority,
        "target_spend": int(target_spend),
        "items": tuple(item_name for _priority, _price, item_name in bundle),
    }


def _wants_store_run(player):
    if player is None or _needs_car(player):
        return False
    if _doctor_visit_is_urgent(player):
        return False
    if _bankroll_emergency_mode(player):
        return False

    dealer_happiness = _dealer_happiness(player)
    store_gap = _days_since_location(player, "shop:convenience_store")
    buyout_candidate = _store_buyout_candidate(player)
    gift_unlock_push = _gift_unlock_push_mode(player)
    if buyout_candidate is not None and store_gap != 0 and (store_gap is None or store_gap > 1):
        _bump_funnel_metric(player, "store_buyout_trigger_count")
        return True
    if dealer_happiness >= 96:
        return False

    store_summary = _store_chore_summary(player)
    chores = store_summary["chores"]
    affordable = store_summary["affordable"]
    if not affordable:
        return False

    tuner = _rank_tuner(player)
    best_priority, best_price, _best_item, _best_actionable, _best_affordable = store_summary["top"]
    companion_metrics = _companion_metrics(player)
    companion_emergency_item = any(
        affordable_now
        and _is_companion_food_item(item_name, player)
        and (companion_metrics["runaway"] > 0 or companion_metrics["low"] > 0 or companion_metrics["bond_window"] > 0)
        for _priority, _price, item_name, _actionable_now, affordable_now in chores[:5]
    )
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
    if _fragile_post_car_recovery_mode(player) and best_priority < 90 and not companion_emergency_item:
        return False

    if (
        player.get_rank() >= 2
        and 10000 <= balance < 100000
        and buyout_candidate is None
        and not gift_unlock_push
        and not companion_emergency_item
        and best_priority < 90
        and _best_item not in {"LifeAlert", "First Aid Kit", "Road Flares", "Spare Tire", "Tool Kit"}
    ):
        return False

    if store_gap == 0:
        if buyout_candidate is not None or gift_unlock_push or _best_item == "Tool Kit":
            _bump_funnel_metric(player, "store_same_day_return_count")
            if buyout_candidate is not None:
                _bump_funnel_metric(player, "store_buyout_trigger_count")
            return True
        return False
    if store_gap is not None and store_gap <= 1 and _best_item not in STORE_MUST_HAVE_ITEMS and not companion_emergency_item and not gift_unlock_push:
        return False
    if store_gap is not None and store_gap <= 2 and best_priority < 84 and not companion_emergency_item and not gift_unlock_push:
        return False
    if _best_item == "Tool Kit" and store_gap != 0 and (store_gap is None or store_gap >= 2):
        if player.get_health() >= 58 and player.get_sanity() >= 30:
            return True
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
        companion_emergency_item
        and player.get_balance() >= max(60, best_price)
        and player.get_health() >= 55
        and player.get_sanity() >= 28
    ):
        return True

    if gift_unlock_push and player.get_balance() >= max(120, min(best_price, 180)):
        return True

    if (
        store_summary["actionable_count"] >= 2
        and player.get_health() >= 58
        and player.get_sanity() >= 30
        and (store_gap is None or store_gap > 1)
    ):
        return True

    if (
        store_summary["count"] >= 3
        and best_priority >= 70
        and player.get_health() >= 62
        and player.get_sanity() >= 32
        and (store_gap is None or store_gap > 2)
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
        best_priority >= max(52, tuner["store_priority_min"] - 20)
        and player.get_balance() >= tuner["store_balance_gate"]
        and player.get_health() >= tuner["store_health_gate"]
        and player.get_sanity() >= tuner["store_sanity_gate"]
    ):
        return True
    return False


def _planned_store_spend(player):
    buyout_candidate = _store_buyout_candidate(player)
    if buyout_candidate is not None:
        return int(buyout_candidate["target_spend"])
    candidates = _store_purchase_candidates(player)
    if not candidates:
        store_summary = _store_chore_summary(player)
        top = store_summary["top"]
        return 0 if top is None else int(top[1])
    _priority, price, _name = candidates[0]
    return price


def _marvin_conversion_synergy_bonus(item_name, player):
    if player is None:
        return 0

    balance = player.get_balance()
    rank = int(player.get_rank()) if hasattr(player, "get_rank") else 0
    has_peek = player.has_item("Sneaky Peeky Shades") or player.has_item("Sneaky Peeky Goggles")
    has_watch = player.has_item("Pocket Watch") or player.has_item("Grandfather Clock")
    has_coin = player.has_item("Lucky Coin") or player.has_item("Lucky Medallion")
    has_double_item = player.has_item("Gambler's Chalice") or player.has_item("Overflowing Goblet")
    has_split_item = player.has_item("Twin's Locket") or player.has_item("Mirror of Duality")
    has_whispers = hasattr(player, "has_flask_effect") and player.has_flask_effect("Dealer's Whispers")
    has_bonus = hasattr(player, "has_flask_effect") and player.has_flask_effect("Bonus Fortune")
    has_second = hasattr(player, "has_flask_effect") and player.has_flask_effect("Second Chance")

    bonus = 0
    if item_name == "Gambler's Grimoire":
        bonus += 6 if rank <= 1 else 16
        if balance >= 8000:
            bonus += 8
        if not (has_peek or has_watch or has_coin):
            bonus += 4
        return bonus
    if item_name == "Sneaky Peeky Shades":
        bonus += 18 if rank <= 1 else 32
        if balance >= 18000:
            bonus += 10
        if has_watch:
            bonus += 10
        if has_coin:
            bonus += 8
        if has_second or has_whispers:
            bonus += 6
    elif item_name == "Pocket Watch":
        bonus += 14 if rank <= 1 else 26
        if balance >= 15000:
            bonus += 8
        if has_peek:
            bonus += 10
        if has_coin:
            bonus += 6
    elif item_name == "Lucky Coin":
        bonus += 10 if rank <= 1 else 16
        if balance >= 10000:
            bonus += 6
        if has_peek or has_watch:
            bonus += 6
    elif item_name == "Worn Gloves":
        bonus += 8 if rank <= 1 else 14
        if has_peek:
            bonus += 6
    elif item_name == "Tattered Cloak":
        bonus += 8 if rank <= 1 else 14
        if has_coin or has_second:
            bonus += 6
    elif item_name == "Twin's Locket":
        bonus += 6 if rank <= 1 else 24
        if balance >= 20000:
            bonus += 6
        if has_split_item or (hasattr(player, "has_flask_effect") and player.has_flask_effect("Split Serum")):
            bonus -= 14
        if has_watch or has_bonus:
            bonus += 6
    elif item_name == "White Feather":
        bonus += 8 if rank <= 1 else 20
        if balance >= 14000:
            bonus += 6
        if has_peek or has_watch:
            bonus += 4
    elif item_name == "Gambler's Chalice":
        bonus += 2 if rank <= 1 else 14
        if has_bonus:
            bonus -= 10
        elif balance >= 22000:
            bonus += 6
        if has_second or has_peek:
            bonus += 4
        if has_double_item:
            bonus -= 6
    elif item_name == "Dealer's Grudge":
        bonus += 2 if rank <= 1 else 12
        if has_whispers:
            bonus += 8
    elif item_name == "Health Indicator":
        bonus += 4 if rank <= 1 else 10
    elif item_name == "Delight Indicator":
        bonus += 2 if rank <= 1 else 8
    return bonus


def _marvin_conversion_items():
    return {
        "Faulty Insurance",
        "Rusty Compass",
        "Lucky Coin",
        "Gambler's Grimoire",
        "Quiet Sneakers",
        "Sneaky Peeky Shades",
        "Pocket Watch",
        "Worn Gloves",
        "Tattered Cloak",
        "Gambler's Chalice",
        "Twin's Locket",
        "White Feather",
        "Dealer's Grudge",
    }


def _marvin_capstone_items():
    return {"Pocket Watch", "Sneaky Peeky Shades", "Golden Watch", "Animal Whistle"}


def _marvin_late_game_leverage_items():
    return {
        "Worn Gloves",
        "Tattered Cloak",
        "Dealer's Grudge",
        "Golden Watch",
        "Animal Whistle",
        "Dirty Old Hat",
        "Gambler's Grimoire",
    }


def _marvin_early_essential_items():
    return {
        "Faulty Insurance",
        "Rusty Compass",
        "Lucky Coin",
        "White Feather",
        "Quiet Sneakers",
    }


def _marvin_essential_items():
    return _marvin_early_essential_items() | {
        "Pocket Watch",
        "Sneaky Peeky Shades",
        "Gambler's Chalice",
        "Twin's Locket",
        "Tattered Cloak",
        "Worn Gloves",
        "Dealer's Grudge",
    }


def _missing_marvin_items_count(player):
    """Count how many essential Marvin items the player still needs."""
    if player is None:
        return 0
    return sum(1 for item in _marvin_essential_items() if not player.has_item(item))


def _rotation_staleness_bonus(player, *location_keys, stale_after=2, bonus_per_day=5, max_bonus=20):
    """Return a score bonus that encourages visiting locations not recently seen.

    Drives natural rotation: a location untouched for ``stale_after + 1`` days
    starts accumulating bonus points, capped at ``max_bonus``.  Locations that
    have never been visited receive the full cap immediately.
    """
    if player is None:
        return 0
    gap = _days_since_location(player, *location_keys)
    if gap is None:
        return max_bonus
    if gap <= stale_after:
        return 0
    return min(max_bonus, (gap - stale_after) * bonus_per_day)


def _witch_marvin_pairing_flasks():
    return {
        "No Bust",
        "Second Chance",
        "Dealer's Whispers",
        "Bonus Fortune",
        "Split Serum",
        "Pocket Aces",
        "Imminent Blackjack",
        "Fortunate Day",
        "Fortunate Night",
    }


def _active_witch_marvin_flasks(player):
    if player is None or not hasattr(player, "has_flask_effect"):
        return set()
    return {
        flask_name
        for flask_name in _witch_marvin_pairing_flasks()
        if player.has_flask_effect(flask_name)
    }


def _witch_marvin_pairing_strength(player):
    if player is None:
        return 0
    active_flasks = _active_witch_marvin_flasks(player)
    if not active_flasks:
        return 0

    score = 0
    strong_flasks = {"No Bust", "Second Chance", "Dealer's Whispers", "Bonus Fortune"}
    capstone_flasks = {"Split Serum", "Pocket Aces", "Imminent Blackjack"}
    if active_flasks & strong_flasks:
        score += 14
    if len(active_flasks & strong_flasks) >= 2:
        score += 12
    if active_flasks & capstone_flasks:
        score += 10
    if {"Fortunate Day", "Fortunate Night"} & active_flasks:
        score += 4
    if player.get_rank() >= 2:
        score += 6
    if player.get_balance() >= 10000:
        score += 6
    return score


def _witch_drives_marvin_followup(player):
    if player is None or not _has_marvin_access(player) or not player.has_item("Car"):
        return False
    if player.get_rank() < 1:
        return False
    if player.get_health() < 58 or player.get_sanity() < 28:
        return False
    return _witch_marvin_pairing_strength(player) >= 20


def _marvin_post_purchase_floor(player, item_name):
    doctor_reserve = max(60, _doctor_cash_reserve(player))
    rank = int(player.get_rank()) if hasattr(player, "get_rank") else 0
    balance = max(0, int(player.get_balance())) if player is not None and hasattr(player, "get_balance") else 0
    item_floor = {
        "Faulty Insurance": 900,
        "Rusty Compass": 1000,
        "Lucky Coin": 1200,
        "Gambler's Grimoire": 1200,
        "Health Indicator": 1500,
        "Delight Indicator": 1500,
        "Quiet Sneakers": 1500,
        "Sneaky Peeky Shades": 3200,
        "Pocket Watch": 2200,
        "Worn Gloves": 2600,
        "Tattered Cloak": 2400,
        "Gambler's Chalice": 3800,
        "Twin's Locket": 4500,
        "White Feather": 1500,
        "Dealer's Grudge": 2600,
        "Golden Watch": 4200,
        "Animal Whistle": 7000,
        "Dirty Old Hat": 2200,
    }.get(item_name)
    if item_floor is None:
        return max(doctor_reserve, _rank_protection_floor(player))
    if rank <= 1:
        return max(doctor_reserve, min(item_floor, 2500))
    if balance >= 25000 and item_name in _marvin_late_game_leverage_items():
        relaxed_floor = 6000 if item_name == "Animal Whistle" else 4000
        if item_name in {"Gambler's Grimoire", "Dirty Old Hat"}:
            relaxed_floor = 2500
        return max(doctor_reserve, min(item_floor, relaxed_floor))
    if item_name in _marvin_essential_items():
        return max(doctor_reserve, min(item_floor, 5000 if item_name in _marvin_capstone_items() else 4000))
    return max(doctor_reserve, item_floor)


def _marvin_item_priority(item_name, player):
    if player is None or player.has_item(item_name):
        return 0
    if item_name in {"Health Indicator", "Delight Indicator"}:
        return 0

    priority = get_marvin_base_priority(item_name)
    balance = player.get_balance()
    rank = int(player.get_rank()) if hasattr(player, "get_rank") else 0
    price = _marvin_price_estimate(item_name)
    leverage_items = _marvin_late_game_leverage_items()
    if item_name == "Faulty Insurance" and player.has_item("Real Insurance"):
        return 0
    if player.has_item("Car") and rank < 2:
        if item_name == "Faulty Insurance":
            priority += 30
        if item_name in {"Rusty Compass", "Lucky Coin"}:
            priority += 24
        if item_name == "White Feather":
            priority += 24
        if item_name in {"Health Indicator", "Delight Indicator"}:
            priority += 4
        if item_name == "Quiet Sneakers":
            priority += 18
        if item_name == "Sneaky Peeky Shades":
            priority += 14
        if item_name == "Pocket Watch":
            priority += 24
        if item_name == "Gambler's Chalice":
            priority += 14
        if item_name == "Twin's Locket":
            priority += 10
        if item_name == "Animal Whistle":
            priority -= 10
        if item_name in {"Twin's Locket", "Dealer's Grudge"}:
            priority -= 4
        if item_name == "Marvin's Monocle":
            priority -= 18
        if balance < 12000 and price >= 15000:
            priority -= 14
        if 2500 <= balance < 12000 and item_name in _marvin_early_essential_items():
            priority += 12
        if 7000 <= balance < 18000 and item_name in {"Pocket Watch", "Sneaky Peeky Shades", "Gambler's Chalice"}:
            priority += 12
    if item_name == "Dirty Old Hat" and rank == 0 and balance < 1000:
        priority += 12
    if item_name == "Dirty Old Hat" and rank < 2 and balance < 12000:
        priority -= 10
    if item_name == "Golden Watch" and balance >= 5000:
        priority += 8
    if item_name == "Pocket Watch" and balance >= 3000:
        priority += 6
    if item_name in {"Rusty Compass", "Quiet Sneakers", "Sneaky Peeky Shades"} and rank < 2:
        priority += 10
    if item_name == "Animal Whistle":
        if _companion_count(player) < 5:
            priority += 14
        if player.has_item("Car"):
            priority += 8
    if player.has_item("Car") and rank >= 2:
        if item_name in _marvin_conversion_items():
            priority += 12
        if item_name == "Pocket Watch":
            priority += 22
        if item_name == "Sneaky Peeky Shades":
            priority += 20
        if item_name == "Twin's Locket":
            priority += 24
        if item_name == "White Feather":
            priority += 10
        if item_name == "Gambler's Chalice":
            priority += 18
        if 10000 <= balance < 22000 and item_name in {"Pocket Watch", "Sneaky Peeky Shades", "Gambler's Chalice", "Twin's Locket"}:
            priority += 12
    pairing_strength = _witch_marvin_pairing_strength(player)
    if pairing_strength > 0 and player.has_item("Car") and rank >= 2:
        if item_name == "Pocket Watch":
            priority += 16 + min(14, pairing_strength)
        if item_name == "Sneaky Peeky Shades":
            priority += 14 + min(12, pairing_strength)
        if item_name in {"Twin's Locket", "Gambler's Chalice", "Dealer's Grudge", "Worn Gloves", "Tattered Cloak"}:
            priority += 6 + min(8, pairing_strength // 2)
    if item_name == "Enchanting Silver Bar":
        if balance < 10000:
            priority -= 20
        else:
            priority += 12
    if item_name in {"Worn Gloves", "Tattered Cloak", "Pocket Watch", "Golden Watch"} and balance >= 25000:
        priority += 8
    if item_name == "Animal Whistle" and rank < 2 and balance < 16000:
        priority -= 12
    if item_name == "Marvin's Monocle" and player.has_met("Vinnie") and rank < 2:
        priority -= 12
    if balance >= 12000 and item_name == "Gambler's Grimoire":
        priority += 24
    if balance >= 18000 and item_name in {"Worn Gloves", "Tattered Cloak", "Dealer's Grudge", "Dirty Old Hat"}:
        priority += 14
    if balance >= 22000 and item_name == "Golden Watch":
        priority += 24
    if balance >= 25000 and item_name in leverage_items:
        priority += 10
    if balance >= 30000 and item_name == "Animal Whistle":
        priority += 26
    if rank >= 2 and player.get_health() >= 66 and player.get_sanity() >= 34 and item_name in leverage_items:
        priority += 8
    priority += _marvin_conversion_synergy_bonus(item_name, player)
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


def _has_unbought_marvin_items(player):
    if player is None or not _has_marvin_access(player):
        return False
    for item_name in MARVIN_ITEM_ORDER:
        if _marvin_item_priority(item_name, player) > 0:
            return True
    return False


def _marvin_remaining_spend(player):
    if player is None:
        return 0
    total = 0
    for item_name in MARVIN_ITEM_ORDER:
        if _marvin_item_priority(item_name, player) > 0:
            total += _marvin_price_estimate(item_name)
    return total


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


def _marvin_catalog_candidate(player, balance=None):
    if player is None or not player.has_item("Car") or not _has_marvin_access(player):
        return None
    if _needs_car(player) or _wants_doctor_visit(player) or _doctor_visit_is_urgent(player):
        return None
    if player.get_health() < 60 or player.get_sanity() < 32:
        return None

    real_balance = max(0, int(player.get_balance() if balance is None else balance))
    if real_balance <= 0:
        return None

    affordable = []
    for item_name in MARVIN_ITEM_ORDER:
        if player.has_item(item_name):
            continue
        price = _marvin_price_estimate(item_name)
        if price > real_balance:
            continue
        priority = _marvin_item_priority(item_name, player)
        if priority <= 0:
            continue
        affordable.append((priority, price, item_name))

    if not affordable:
        return None

    affordable.sort(key=lambda entry: (-entry[0], entry[1], entry[2]))
    rank = int(player.get_rank()) if hasattr(player, "get_rank") else 0
    conversion_items = _marvin_conversion_items()
    essential_items = _marvin_essential_items()
    best_priority, best_price, best_item = affordable[0]
    immediate_floor = _marvin_post_purchase_floor(player, best_item)
    if (
        best_item in conversion_items
        and best_priority >= (64 if rank >= 2 else 80)
        and real_balance - best_price >= immediate_floor
    ):
        return {
            "count": 1,
            "priority": int(best_priority),
            "target_spend": int(best_price),
            "items": (best_item,),
        }
    if real_balance >= 25000 and best_item in _marvin_late_game_leverage_items() and real_balance - best_price >= immediate_floor:
        return {
            "count": 1,
            "priority": int(best_priority),
            "target_spend": int(best_price),
            "items": (best_item,),
        }

    leverage_items = {
        "Faulty Insurance",
        "Rusty Compass",
        "Lucky Coin",
        "Gambler's Grimoire",
        "Health Indicator",
        "Delight Indicator",
        "Quiet Sneakers",
        "Sneaky Peeky Shades",
        "Pocket Watch",
        "Worn Gloves",
        "Tattered Cloak",
        "Gambler's Chalice",
        "Twin's Locket",
        "White Feather",
        "Dealer's Grudge",
        "Golden Watch",
        "Animal Whistle",
        "Dirty Old Hat",
    }
    bundle_size = 2 if rank <= 1 and real_balance < 16000 else 3 if rank <= 1 else 3 if real_balance >= 22000 else 2
    bundle = affordable[:bundle_size]
    target_spend = sum(price for _priority, price, _item_name in bundle)
    best_priority = int(bundle[0][0])
    balance_gate = 5500 if rank <= 1 and best_item in essential_items else 8000 if rank <= 1 else 9000
    if len(affordable) < 2 and real_balance < balance_gate:
        only_priority, only_price, only_item = bundle[0]
        if only_item not in leverage_items or only_priority < (74 if only_item in essential_items else 86):
            return None
        if real_balance - only_price < max(180 if rank <= 1 else 3500, _doctor_cash_reserve(player)):
            return None
    if real_balance < balance_gate and best_priority < (74 if best_item in essential_items else 80):
        return None
    if len(bundle) < 2 and target_spend < max(800, int(real_balance * 0.16)):
        only_priority, _only_price, only_item = bundle[0]
        if only_item not in leverage_items or only_priority < (74 if only_item in essential_items else 86):
            return None

    return {
        "count": len(bundle),
        "priority": best_priority,
        "target_spend": int(target_spend),
        "items": tuple(item_name for _priority, _price, item_name in bundle),
    }


def _best_future_marvin_candidate(player, balance):
    if player is None or balance <= 0:
        return None

    rank = int(player.get_rank())
    essential_items = _marvin_essential_items()
    if rank <= 1:
        max_shortfall = max(5000, min(9000, int(balance * 1.70)))
        min_priority = 66
        preferred_items = {
            "Faulty Insurance",
            "Rusty Compass",
            "Lucky Coin",
            "White Feather",
            "Quiet Sneakers",
            "Pocket Watch",
            "Sneaky Peeky Shades",
        }
    else:
        max_shortfall = max(24000, min(55000, int(balance * 3.0)))
        min_priority = 68
        preferred_items = {
            "Pocket Watch",
            "Gambler's Chalice",
            "Sneaky Peeky Shades",
            "White Feather",
            "Twin's Locket",
            "Worn Gloves",
            "Tattered Cloak",
            "Dealer's Grudge",
            "Golden Watch",
            "Animal Whistle",
            "Dirty Old Hat",
            "Gambler's Grimoire",
        }

    best = None
    for item_name in MARVIN_ITEM_ORDER:
        if player.has_item(item_name):
            continue
        price = _marvin_price_estimate(item_name)
        shortfall = price - balance
        if shortfall <= 0 or shortfall > max_shortfall:
            continue

        priority = _marvin_item_priority(item_name, player)
        if item_name in preferred_items:
            priority += 14
        if item_name in essential_items:
            priority += 10
        if rank <= 1 and 6000 <= balance < 12000 and item_name in {"White Feather", "Pocket Watch"}:
            priority += 18
        if rank <= 1 and 8000 <= balance < 16000 and item_name == "Gambler's Chalice":
            priority += 10
        if 10000 <= balance < 18000 and item_name == "Pocket Watch":
            priority += 24
        if 10000 <= balance < 22000 and item_name == "Sneaky Peeky Shades":
            priority += 8
        if 10000 <= balance < 22000 and item_name == "Gambler's Chalice":
            priority += 18
        if 10000 <= balance < 24000 and item_name == "Twin's Locket":
            priority += 14
        if balance >= 10000 and item_name in _marvin_capstone_items():
            priority += 12
        if rank >= 2 and balance >= 15000 and item_name in _marvin_late_game_leverage_items():
            priority += 12
        if balance >= 18000 and item_name in {"Dirty Old Hat", "Gambler's Grimoire"}:
            priority += 12
        if balance >= 22000 and item_name == "Golden Watch":
            priority += 22
        if balance >= 30000 and item_name == "Animal Whistle":
            priority += 26
        if balance >= 9000 and item_name in {"White Feather", "Pocket Watch", "Gambler's Chalice", "Twin's Locket", "Sneaky Peeky Shades"}:
            priority += 10
        if _witch_drives_marvin_followup(player) and item_name in _marvin_capstone_items():
            priority += 10
        if priority < (64 if item_name in essential_items and rank <= 1 else min_priority):
            continue

        candidate = (priority, -shortfall, -price, item_name)
        if best is None or candidate > best:
            best = candidate

    if best is None:
        return None

    priority, negative_shortfall, negative_price, item_name = best
    return {
        "priority": int(priority),
        "price": int(-negative_price),
        "item": item_name,
        "shortfall": int(-negative_shortfall),
    }


def _marvin_loan_plan(player):
    """Return a loan plan to fund a Marvin purchase, or None if not applicable.

    Two modes:
    1. Buy-enable  – the target item is unaffordable outright; borrow the shortfall.
    2. Buffer-preserve – the item IS affordable but buying it leaves the player nearly
       broke (dropping 2 ranks or below the post-purchase safety floor); borrow enough
       so the post-purchase balance stays comfortable.

    Mode 2 only activates during a rank-push or win-push window — i.e. when the player
    is actively pushing toward the next rank / a win milestone and has the health/edge
    to sustain aggressive play.  This mirrors the user intent of "loans right before a
    purchase, when pushing for a rank up or a win."
    """
    if player is None or not player.has_item("Car") or not _has_marvin_access(player):
        return None
    if not player.has_met("Vinnie") or int(player.get_loan_shark_debt()) > 0:
        return None
    if _fraudulent_cash_amount(player) > 0:
        return None
    if player.get_health() < 52 or player.get_sanity() < 28:
        return None

    balance = player.get_balance()
    rank = int(player.get_rank())
    doctor_reserve = max(80, _doctor_cash_reserve(player))
    if balance <= doctor_reserve:
        return None

    # Upper balance cap: no need to borrow when already flush.
    # Expanded from old $26k cap to allow buffer-preserve loans at higher ranks.
    max_balance_for_plan = {0: 14000, 1: 45000, 2: 140000, 3: 250000}.get(rank, 140000)
    if balance >= max_balance_for_plan:
        return None

    future_candidate = _best_future_marvin_candidate(player, balance)
    essential_future_push = (
        future_candidate is not None
        and future_candidate["item"] in _marvin_essential_items()
        and future_candidate["shortfall"] <= max(5000 if rank <= 1 else 16000, int(balance * (1.00 if rank <= 1 else 0.85)))
    )
    marvin_push = _marvin_push_window(player)
    in_push = marvin_push or _in_rank_push_window(player) or essential_future_push

    # Post-purchase safety floor: minimum balance to retain after buying.
    # During a push window we allow a deeper dip (protection_floor // 2 at minimum),
    # because the improved edge score will repay the short-term pain faster.
    protection_floor = _rank_protection_floor(player)
    if in_push:
        post_purchase_min = max(doctor_reserve, protection_floor // (3 if rank >= 2 else 2))
    else:
        post_purchase_min = max(doctor_reserve, protection_floor)

    # Check whether the current best affordable item already qualifies — if so, skip
    # borrowing; we'll just buy it.
    current = _best_marvin_candidate(player, balance)
    current_ok = current is not None and current[0] >= (84 if current[2] in _marvin_essential_items() else 90)
    aggressive_unlock_items = _marvin_essential_items()

    loan_amounts = (5000, 2500, 1000, 500, 100) if marvin_push else (100, 500, 1000, 2500, 5000)
    for loan_amount in loan_amounts:
        candidate = _best_marvin_candidate(player, balance + loan_amount)
        if candidate is None:
            continue
        priority, price, item_name = candidate

        shortfall = max(0, price - balance)

        # Mode 1: buy-enable — need the loan just to afford the item.
        if shortfall > 0:
            if shortfall > loan_amount:
                continue
            if marvin_push and rank <= 1 and item_name in aggressive_unlock_items and priority >= 56:
                return {"borrow": loan_amount, "price": price, "priority": priority, "item": item_name, "mode": "marvin_push"}
            required_post_purchase = doctor_reserve
            if item_name in aggressive_unlock_items:
                required_post_purchase = max(doctor_reserve, min(_marvin_post_purchase_floor(player, item_name), max(doctor_reserve, 800 if rank <= 1 else 3000)))
            if balance + loan_amount - price < required_post_purchase:
                continue
            if item_name == "Faulty Insurance" and priority >= 84:
                return {"borrow": loan_amount, "price": price, "priority": priority, "item": item_name, "mode": "buy_enable"}
            if item_name in aggressive_unlock_items and priority >= 72 and shortfall <= loan_amount:
                return {"borrow": loan_amount, "price": price, "priority": priority, "item": item_name, "mode": "buy_enable"}
            if priority >= 88 and shortfall <= loan_amount:
                return {"borrow": loan_amount, "price": price, "priority": priority, "item": item_name, "mode": "buy_enable"}
            if priority >= 82 and shortfall <= 5000:
                return {"borrow": loan_amount, "price": price, "priority": priority, "item": item_name, "mode": "buy_enable"}
            continue

        # Mode 2: buffer-preserve — can afford the item but post-purchase balance is
        # dangerously low.  Only during a push window, and only for high-priority items.
        if not in_push and item_name not in aggressive_unlock_items:
            continue
        if current_ok:
            continue  # can already afford a great item without a loan
        post_purchase = balance - price
        if post_purchase >= post_purchase_min + loan_amount:
            continue  # buffer is already fine even without borrowing
        needed_buffer = post_purchase_min - post_purchase
        if needed_buffer <= 0 or needed_buffer > loan_amount:
            continue
        if priority < (72 if item_name in aggressive_unlock_items else 76):
            continue
        if marvin_push and rank <= 1 and item_name in aggressive_unlock_items and priority >= 56:
            return {"borrow": loan_amount, "price": price, "priority": priority, "item": item_name, "mode": "marvin_push"}
        return {"borrow": loan_amount, "price": price, "priority": priority, "item": item_name, "mode": "buffer_preserve"}

    return None


def _pending_marvin_candidate(player, balance=None, fake_cash=None):
    if player is None or not player.has_item("Car") or not _has_marvin_access(player):
        return None
    marvin_gap = _days_since_location(player, "shop:marvin")
    if marvin_gap == 0:
        return None
    if _wants_doctor_visit(player) or _doctor_visit_is_urgent(player):
        return None
    if player.get_health() < 56 or player.get_sanity() < 30:
        return None

    real_balance = max(0, int(player.get_balance() if balance is None else balance))
    affordable_candidate = _best_marvin_candidate(player, real_balance)
    future_candidate = _best_future_marvin_candidate(player, real_balance)
    essential_items = _marvin_essential_items()

    if affordable_candidate is not None:
        priority, price, item_name = affordable_candidate
        affordable_payload = {
            "priority": int(priority),
            "price": int(price),
            "item": item_name,
            "shortfall": max(0, int(price) - real_balance),
        }
        if (
            item_name in _marvin_conversion_items()
            and real_balance >= price
            and real_balance - price >= _marvin_post_purchase_floor(player, item_name)
            and priority >= (72 if player.get_rank() >= 2 else 84)
        ):
            return affordable_payload
        if (
            player.get_rank() >= 2
            and item_name in _marvin_late_game_leverage_items()
            and real_balance >= price
            and real_balance - price >= _marvin_post_purchase_floor(player, item_name)
            and priority >= 72
        ):
            return affordable_payload
        if future_candidate is None:
            return affordable_payload

        if (
            future_candidate["item"] in essential_items
            and future_candidate["shortfall"] <= max(5000 if player.get_rank() <= 1 else 9000, int(real_balance * (1.10 if player.get_rank() <= 1 else 0.60)))
            and future_candidate["priority"] >= affordable_payload["priority"] - 2
            and item_name not in essential_items
        ):
            return future_candidate

        if (
            player.get_rank() <= 1
            and real_balance >= 5000
            and future_candidate["item"] in {"White Feather", "Pocket Watch", "Gambler's Chalice"}
            and future_candidate["shortfall"] <= max(5000, int(real_balance * 0.8))
            and future_candidate["priority"] >= affordable_payload["priority"] + 2
            and item_name not in {"Faulty Insurance", "Lucky Coin", "Rusty Compass"}
        ):
            return future_candidate

        if (
            player.get_rank() >= 2
            and real_balance >= 10000
            and future_candidate["item"] in _marvin_capstone_items()
            and future_candidate["shortfall"] <= (18000 if _witch_drives_marvin_followup(player) else 12000)
            and future_candidate["priority"] >= affordable_payload["priority"] - 4
            and item_name not in _marvin_capstone_items()
        ):
            return future_candidate
        if (
            player.get_rank() >= 2
            and real_balance >= 14000
            and future_candidate["item"] in _marvin_late_game_leverage_items()
            and future_candidate["shortfall"] <= max(18000, int(real_balance * 0.60))
            and future_candidate["priority"] >= affordable_payload["priority"] - 2
            and item_name not in _marvin_late_game_leverage_items()
        ):
            return future_candidate

        if (
            player.get_rank() >= 2
            and future_candidate["price"] > real_balance
            and future_candidate["priority"] >= affordable_payload["priority"] + 4
            and item_name not in _marvin_conversion_items()
        ):
            return future_candidate
        return affordable_payload

    if future_candidate is None:
        return None
    return future_candidate


def _marvin_push_window(player):
    if player is None or not player.has_item("Car") or not _has_marvin_access(player):
        return False
    if not player.has_met("Vinnie") or int(player.get_loan_shark_debt()) > 0:
        return False
    if _fraudulent_cash_amount(player) > 0:
        return False
    if _doctor_visit_is_urgent(player) or _bankroll_emergency_mode(player) or _fragile_post_car_recovery_mode(player):
        return False

    balance = int(player.get_balance())
    rank = int(player.get_rank()) if hasattr(player, "get_rank") else 0
    if rank > 1 or balance < 1000 or balance >= 10000:
        return False
    if player.get_health() < 58 or player.get_sanity() < 30:
        return False

    essential_items = _marvin_essential_items()
    affordable = _best_marvin_candidate(player, balance)
    if affordable is not None and affordable[2] in essential_items and affordable[0] >= 56:
        return True

    post_loan = _best_marvin_candidate(player, balance + 5000)
    if post_loan is not None and post_loan[2] in essential_items and post_loan[0] >= 56:
        return True

    future = _best_future_marvin_candidate(player, balance)
    return bool(
        future is not None
        and future["item"] in essential_items
        and future["priority"] >= 64
        and future["shortfall"] <= 5000
    )


def _marvin_purchase_push_candidate(player, balance=None):
    if player is None or not player.has_item("Car") or not _has_marvin_access(player):
        return None
    marvin_gap = _days_since_location(player, "shop:marvin")
    if marvin_gap == 0:
        return None
    if _needs_car(player) or _wants_doctor_visit(player) or _doctor_visit_is_urgent(player):
        return None
    if player.get_health() < 60 or player.get_sanity() < 34:
        return None

    real_balance = max(0, int(player.get_balance() if balance is None else balance))
    if real_balance <= 0:
        return None

    rank = int(player.get_rank()) if hasattr(player, "get_rank") else 0
    essential_items = _marvin_essential_items()
    priority_floor = 80 if rank <= 1 else 82
    preferred_items = (
        {
            "Faulty Insurance",
            "Rusty Compass",
            "Lucky Coin",
            "Quiet Sneakers",
            "White Feather",
            "Pocket Watch",
            "Gambler's Chalice",
        }
        if rank <= 1
        else {
            "Pocket Watch",
            "Sneaky Peeky Shades",
            "Twin's Locket",
            "White Feather",
            "Gambler's Chalice",
            "Tattered Cloak",
            "Worn Gloves",
            "Dealer's Grudge",
            "Golden Watch",
            "Animal Whistle",
            "Dirty Old Hat",
            "Gambler's Grimoire",
        }
    )

    candidate = _best_marvin_candidate(player, real_balance)
    if candidate is None:
        return None

    priority, price, item_name = candidate
    if item_name in essential_items:
        priority_floor = min(priority_floor, 74 if rank <= 1 else 76)
    if rank <= 1 and real_balance >= 7000 and item_name in {"White Feather", "Pocket Watch", "Gambler's Chalice"}:
        priority_floor = 80
    if rank >= 2 and real_balance >= 10000 and item_name in _marvin_capstone_items():
        priority_floor = 82 if _witch_drives_marvin_followup(player) else 84
    if rank >= 2 and real_balance >= 18000 and item_name in _marvin_late_game_leverage_items():
        priority_floor = min(priority_floor, 74)
    if price > real_balance or priority < priority_floor or item_name not in preferred_items:
        return None

    reserve = _cash_safety_reserve(player, priority)
    post_purchase = real_balance - price
    extra_buffer = max(120, min(1800 if rank <= 1 else 3500, max(price // 5, int(real_balance * 0.06))))
    desired_post_purchase = reserve + extra_buffer
    buffer_shortfall = desired_post_purchase - post_purchase
    max_shortfall = max(500 if item_name in essential_items else 350, min(3000 if rank <= 1 else 9000, price // 2 + (1500 if rank >= 2 else 0)))
    if rank >= 2 and real_balance >= 25000 and item_name in _marvin_late_game_leverage_items():
        max_shortfall = max(max_shortfall, min(12000, price // 2 + 2500))
    if buffer_shortfall <= 0 or buffer_shortfall > max_shortfall:
        return None
    if real_balance > price + max_shortfall:
        return None

    return {
        "priority": int(priority),
        "price": int(price),
        "item": item_name,
        "shortfall": int(buffer_shortfall),
    }


def _should_suspend_marvin_pressure(player, planner_goal=None):
    if player is None:
        return False

    recovery_goals = {
        "survive_emergency",
        "stabilize_health",
        "stabilize_sanity",
        "reduce_fatigue_pressure",
        "reduce_debt_risk",
        "contain_debt_escalation",
    }
    if planner_goal in recovery_goals:
        return True
    if _doctor_visit_is_urgent(player) or _wants_doctor_visit(player):
        return True

    health = int(player.get_health()) if hasattr(player, "get_health") else 0
    sanity = int(player.get_sanity()) if hasattr(player, "get_sanity") else 0
    debt = int(player.get_loan_shark_debt()) if hasattr(player, "get_loan_shark_debt") else 0
    warning = int(player.get_loan_shark_warning_level()) if hasattr(player, "get_loan_shark_warning_level") else 0
    if health < 64 or sanity < 38:
        return True
    if debt > 0 and warning >= 1:
        return True
    if warning >= 2:
        return True
    return False


def _strong_marvin_route_interrupt(player, labels):
    if player is None:
        return None
    marvin_choice = labels.get("Marvin's Mystical Merchandise")
    if marvin_choice is None or not _has_marvin_access(player) or not player.has_item("Car"):
        return None
    if _should_suspend_marvin_pressure(player):
        return None
    if _wants_doctor_visit(player) or _doctor_visit_is_urgent(player) or _needs_recovery_day(player):
        return None
    pairing_strength = _witch_marvin_pairing_strength(player)
    if player.get_health() < (62 if pairing_strength >= 20 else 66) or player.get_sanity() < (34 if pairing_strength >= 20 else 38):
        return None

    rank = int(player.get_rank()) if hasattr(player, "get_rank") else 0
    balance = int(player.get_balance())
    affordable = _best_marvin_candidate(player, balance)
    future = _best_future_marvin_candidate(player, balance)
    essential_items = _marvin_essential_items()
    marvin_gap = _days_since_location(player, "shop:marvin")
    if marvin_gap == 0:
        return None

    if affordable is not None:
        priority, price, item_name = affordable
        if (
            rank >= 2
            and balance >= 9000
            and item_name in _marvin_capstone_items()
            and priority >= 82
            and balance - price >= _marvin_post_purchase_floor(player, item_name)
        ):
            return marvin_choice
        if (
            rank >= 2
            and balance >= 14000
            and item_name in _marvin_late_game_leverage_items()
            and priority >= 74
            and balance - price >= _marvin_post_purchase_floor(player, item_name)
        ):
            return marvin_choice
        if (
            rank <= 1
            and item_name in _marvin_conversion_items()
            and future["priority"] >= 80
            and future["shortfall"] <= (22000 if _witch_drives_marvin_followup(player) else 16000)
            and balance >= max(1200, price + 150)
            and player.get_health() >= 62
            and player.get_sanity() >= 32
            and (marvin_gap is None or marvin_gap >= 1)
        ):
            return marvin_choice
        if (
            rank <= 1
            and item_name in {"White Feather", "Pocket Watch", "Gambler's Chalice"}
            and priority >= 80
            and balance - price >= _marvin_post_purchase_floor(player, item_name)
            and balance >= max(5000, price + 300)
            and player.get_health() >= 64
            and player.get_sanity() >= 34
            and (marvin_gap is None or marvin_gap >= 2)
        ):
            return marvin_choice
        if (
            rank >= 2
            and item_name in _marvin_conversion_items()
            and priority >= 72
            and balance - price >= _marvin_post_purchase_floor(player, item_name)
            and balance >= max(7000, _rank_floor(balance) - 1500)
        ):
            return marvin_choice

    if future is not None:
        if (
            rank <= 1
            and future["item"] in essential_items
            and future["priority"] >= 68
            and future["shortfall"] <= max(5000, int(balance * 1.10))
            and balance >= 1200
            and player.get_health() >= 60
            and player.get_sanity() >= 30
            and (marvin_gap is None or marvin_gap >= 1)
        ):
            return marvin_choice
        if (
            rank >= 2
            and balance >= 10000
            and future["item"] in _marvin_capstone_items()
            and future["priority"] >= 82
            and future["shortfall"] <= (18000 if _witch_drives_marvin_followup(player) else 12000)
            and (marvin_gap is None or marvin_gap >= 2)
        ):
            return marvin_choice
        if (
            rank <= 1
            and future["item"] in _marvin_conversion_items()
            and future["priority"] >= 72
            and future["shortfall"] <= max(4200, int(balance * 0.85))
            and balance >= 1500
            and player.get_health() >= 64
            and player.get_sanity() >= 34
            and (marvin_gap is None or marvin_gap >= 3)
        ):
            return marvin_choice
        if (
            rank <= 1
            and future["item"] in {"White Feather", "Pocket Watch", "Gambler's Chalice"}
            and future["priority"] >= 80
            and future["shortfall"] <= max(5000, int(balance * 0.95))
            and balance >= 3500
            and player.get_health() >= 64
            and player.get_sanity() >= 34
            and (marvin_gap is None or marvin_gap >= 2)
        ):
            return marvin_choice
        if (
            rank >= 2
            and future["item"] in _marvin_conversion_items()
            and future["priority"] >= 84
            and future["shortfall"] <= max(7000, int(balance * 0.45))
            and balance >= 7000
            and (marvin_gap is None or marvin_gap >= 2)
        ):
            return marvin_choice
        if (
            rank >= 2
            and future["item"] in _marvin_late_game_leverage_items()
            and future["priority"] >= 76
            and future["shortfall"] <= max(18000, int(balance * 0.55))
            and balance >= 12000
            and (marvin_gap is None or marvin_gap >= 1)
        ):
            return marvin_choice

    return None


def _force_marvin_buy_interrupt(player, labels):
    if player is None:
        return None
    marvin_choice = labels.get("Marvin's Mystical Merchandise")
    if marvin_choice is None or not _has_marvin_access(player) or not player.has_item("Car"):
        return None
    balance = int(player.get_balance())
    if balance < 10000:
        return None
    if _days_since_location(player, "shop:marvin") == 0:
        return None
    if _should_suspend_marvin_pressure(player):
        return None
    reserve = max(500, _cash_safety_reserve(player, 88))
    budget = max(0, balance - reserve)
    if _best_marvin_candidate(player, budget) is None:
        return None
    return marvin_choice


def _catalog_push_candidate(player, balance=None):
    marvin_candidate = _marvin_catalog_candidate(player, balance=balance)
    store_candidate = _store_buyout_candidate(player, balance=balance)
    best = None

    if marvin_candidate is not None:
        best = {
            "kind": "marvin",
            "count": int(marvin_candidate["count"]),
            "priority": int(marvin_candidate["priority"]),
            "target_spend": int(marvin_candidate["target_spend"]),
        }

    if store_candidate is not None:
        store_payload = {
            "kind": "store",
            "count": int(store_candidate["count"]),
            "priority": int(store_candidate["priority"]),
            "target_spend": int(store_candidate["target_spend"]),
        }
        if best is None:
            best = store_payload
        else:
            best_score = best["priority"] * 12 + best["target_spend"] + best["count"] * 250
            store_score = store_payload["priority"] * 12 + store_payload["target_spend"] + store_payload["count"] * 250
            if store_score > best_score:
                best = store_payload

    return best


def _current_offer_name(recent, names):
    recent_lower = recent.lower()
    best_name = None
    best_index = -1
    best_length = -1
    for name in names:
        index = recent_lower.rfind(name.lower())
        if index < 0:
            continue
        if index > best_index or (index == best_index and len(name) > best_length):
            best_name = name
            best_index = index
            best_length = len(name)
    return best_name


def _has_marvin_access(player):
    return player is not None and (player.has_item("Map") or player.has_item("Worn Map"))


def _wants_marvin_run(player):
    if not _has_marvin_access(player):
        return False
    if not player.has_item("Car"):
        return False
    if _bankroll_emergency_mode(player):
        return False
    if _wants_doctor_visit(player):
        return False
    if player.get_health() < 50 or player.get_sanity() < 26:
        return False
    marvin_gap = _days_since_location(player, "shop:marvin")
    if marvin_gap == 0:
        return False
    # Allow a visit whenever the player can actually afford an item and has a
    # basic post-purchase safety cushion.  Once the bankroll reaches 10k the
    # full list opens up, but even in early-game the player should scout when
    # a cheap essential is within reach.
    balance = player.get_balance()
    affordable = _best_marvin_candidate(player, balance)
    if affordable is not None:
        _price = affordable[1]
        # Must have at least a $800 cushion after the purchase.
        if balance - _price >= 800:
            _bump_funnel_metric(player, "marvin_ready_count")
            return True
    # Future-item scouting: player is building toward a purchase.
    future = _best_future_marvin_candidate(player, balance)
    if _fragile_post_car_recovery_mode(player):
        if future is None:
            return False
        if player.get_health() < 62 or player.get_sanity() < 34:
            return False
        if balance < 400 or future["shortfall"] > 5000:
            return False
        _bump_funnel_metric(player, "marvin_ready_count")
        return True

    if balance < 10000:
        if future is not None and future["shortfall"] <= 5000 and balance >= 400:
            _bump_funnel_metric(player, "marvin_ready_count")
            return True
        return False
    _bump_funnel_metric(player, "marvin_ready_count")
    return True


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
    if _car_mechanic_name(player) != "Oswald":
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
    if _bankroll_emergency_mode(player) or _fragile_post_car_recovery_mode(player):
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
    if _car_mechanic_name(player) != "Oswald":
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
    if best_name is None:
        return None
    if best_priority < CRAFTING_MIN_PRIORITY:
        if int(player.get_rank()) <= 1 and player.has_item("Tool Kit") and best_priority >= CRAFTING_MIN_PRIORITY - 18:
            return (best_name, best_priority)
        return None
    return (best_name, best_priority)


def _wants_workbench_craft_run(player):
    """Return True when visiting the Car Workbench to craft an item is worthwhile.

    Requires Tool Kit in inventory (which unlocks the Car Workbench in make_shop_list)
    and at least one craftable recipe above the minimum priority threshold.
    Verified from lists.py: Car Workbench is unlocked by has_item("Tool Kit").
    """
    if player is None or not player.has_item("Car") or not player.has_item("Tool Kit"):
        return False
    if _doctor_visit_is_urgent(player):
        return False
    if _wants_doctor_visit(player):
        risk = _doctor_risk_profile(player)
        if risk["margin"] <= 8 or risk["health"] < 58 or risk["sanity"] < 24:
            return False
    candidate = _workbench_best_craft_candidate(player)
    if candidate is None:
        return False
    _bump_funnel_metric(player, "workbench_ready_count")
    if not player.has_met("Car Workbench"):
        return player.get_health() >= 54 and player.get_sanity() >= 28
    workbench_gap = _days_since_location(player, "shop:car_workbench")
    _recipe_name, recipe_priority = candidate
    if workbench_gap == 0:
        if recipe_priority >= 96 and player.get_health() >= 60 and player.get_sanity() >= 30:
            _bump_funnel_metric(player, "workbench_trigger_count")
            return True
        return False
    # Don't return for crafting more than every 2 days (low opportunity cost when nothing new is ready)
    if workbench_gap is not None and workbench_gap <= 1 and recipe_priority < 88:
        return False
    _bump_funnel_metric(player, "workbench_trigger_count")
    return True


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
        _bump_funnel_metric(player, "craft_attempt_count")
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
    companion_recipes = frozenset(
        name for name, recipe in CRAFTING_RECIPE_PRIORITIES.items()
        if name in ("Companion Bed", "Pet Toy", "Feeding Station")
    )
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
            # Try matching any known recipe name inside the label
            for known_name in CRAFTING_RECIPE_PRIORITIES:
                if known_name.lower() in lowered:
                    priority = get_crafting_recipe_priority(known_name)
                    label_stripped = known_name
                    break
        if priority <= 0:
            continue
        if label_stripped in companion_recipes and companion_count > 0:
            priority += 18
        if priority > best_priority:
            best_priority = priority
            best_number = number

    if best_number is not None:
        _bump_funnel_metric(player, "craft_attempt_count")
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
    return player is not None and _should_visit_doctor(player) and not _should_defer_doctor_for_marvin_window(player)


def _defer_doctor_for_no_car_progression(player, route_labels, planned_goal=None):
    # Since there is no on-foot travel, the Doctor is never in the route menu when
    # the player has no car.  This function is kept as a no-op to avoid breaking
    # call-sites while the dead-code is cleaned up gradually.
    return False


def _medical_destination_label(player):
    if player is None:
        return None
    wants_witch = player.has_met("Witch") and _wants_witch_heal(player)
    wants_doctor = _wants_doctor_visit(player)
    if not wants_doctor and not wants_witch:
        # Flask-only witch visit is handled in _choose_progression_destination,
        # not here, so it doesn't override medical priority routing.
        return None
    if (
        wants_witch
        and not _doctor_visit_is_urgent(player)
        and (len(_injury_names(player)) == 0 or _witch_full_cleanse_upside(player) >= 14.0)
    ):
        return "Witch Doctor's Tower"

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
        metadata=_request_metadata({
            "doctor_need_score": _doctor_need_score(player),
            "urgent_medical": _doctor_visit_is_urgent(player),
            "wants_doctor": wants_doctor,
            "wants_witch": wants_witch,
            "injury_tick_pressure": _injury_tick_pressure(player),
            "witch_cleanse_upside": _witch_full_cleanse_upside(player),
            "witch_clear_probability": _witch_status_clear_probability(player),
            "witch_heal_probability": _witch_full_heal_probability(player),
            "witch_retry_value": _witch_retry_value(player),
            "risk_margin": _doctor_risk_profile(player)["margin"],
            "affordable_flask_priority": _best_affordable_witch_flask_priority(player),
            "doctor_cost": _doctor_heal_cost_estimate(player),
            "witch_cost": _witch_heal_cost_estimate(player),
            "flask_count": _flask_count(player),
            "has_real_insurance": player.has_item("Real Insurance"),
            "has_faulty_insurance": player.has_item("Faulty Insurance"),
        }),
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
    balance = player.get_balance()
    has_peek = player.has_item("Sneaky Peeky Shades") or player.has_item("Sneaky Peeky Goggles")
    has_watch = player.has_item("Pocket Watch") or player.has_item("Grandfather Clock")
    has_double_item = player.has_item("Gambler's Chalice") or player.has_item("Overflowing Goblet")
    has_split_item = player.has_item("Twin's Locket") or player.has_item("Mirror of Duality")
    if flask_name == "Anti-Virus" and _status_names(player):
        priority += 18
    if flask_name == "Anti-Venom" and any(
        keyword in _status_names(player)
        for keyword in {"spider bite", "possible rabies", "needle exposure"}
    ):
        priority += 18
    if flask_name == "No Bust":
        if balance >= 12000:
            priority += 10
        if has_peek or has_watch:
            priority += 6
    if flask_name == "Second Chance":
        if balance >= 14000:
            priority += 8
        if has_peek or has_watch:
            priority += 6
    if flask_name == "Dealer's Whispers":
        if balance >= 15000:
            priority += 8
        if has_peek or has_watch:
            priority += 10
    if flask_name == "Bonus Fortune":
        if balance >= 22000:
            priority += 12
        if player.has_flask_effect("No Bust") or player.has_flask_effect("Second Chance"):
            priority += 8
        if has_double_item:
            priority -= 6
    if flask_name == "Dealer's Hesitation":
        if balance >= 15000:
            priority += 6
        if has_peek or player.has_flask_effect("Dealer's Whispers"):
            priority += 12
    if flask_name == "Pocket Aces":
        if balance >= 30000:
            priority += 18
        if has_double_item or player.has_flask_effect("Bonus Fortune"):
            priority += 10
    if flask_name == "Imminent Blackjack":
        if balance >= 28000:
            priority += 14
        if player.has_flask_effect("No Bust") or player.has_flask_effect("Second Chance"):
            priority += 8
    if flask_name == "Split Serum":
        if has_split_item:
            priority -= 14
        elif balance >= 20000:
            priority += 10
    if flask_name in {"No Bust", "Second Chance", "Dealer's Whispers", "Bonus Fortune"} and player.get_rank() >= 1:
        priority += 8
    if player.get_rank() >= 2 and _has_marvin_access(player):
        if flask_name in {"No Bust", "Second Chance", "Dealer's Whispers", "Bonus Fortune"}:
            priority += 8
        if balance >= 10000 and flask_name in {"No Bust", "Second Chance", "Dealer's Whispers"}:
            priority += 6
        if balance >= 14000 and flask_name == "Bonus Fortune":
            priority += 6
    if flask_name in {"No Bust", "Second Chance"} and player.get_balance() >= 10000:
        priority += 10
    if flask_name in {"Fortunate Day", "Fortunate Night"} and player.get_balance() < 10000:
        priority -= 12
    if _flask_count(player) >= 2:
        priority -= 10 if balance >= 35000 and priority >= 88 else 18
    return priority


def _witch_flask_price_estimate(flask_name):
    return get_witch_flask_price_estimate(flask_name)


def _choose_witch_flask(options, player):
    defensive_flasks = {"No Bust", "Second Chance", "Anti-Virus", "Anti-Venom", "Dealer's Whispers"}
    offensive_flasks = {"Imminent Blackjack", "Pocket Aces", "Split Serum", "Bonus Fortune", "Dealer's Hesitation"}
    active_flasks = {
        flask_name
        for flask_name in WITCH_FLASK_PRIORITIES
        if player is not None and hasattr(player, "has_flask_effect") and player.has_flask_effect(flask_name)
    }
    has_peek = player is not None and (player.has_item("Sneaky Peeky Shades") or player.has_item("Sneaky Peeky Goggles"))
    has_double_item = player is not None and (player.has_item("Gambler's Chalice") or player.has_item("Overflowing Goblet"))
    has_split_item = player is not None and (player.has_item("Twin's Locket") or player.has_item("Mirror of Duality"))
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
        combo_bonus = 0.0
        if flask_name == "Dealer's Whispers" and ("No Bust" in active_flasks or "Second Chance" in active_flasks):
            combo_bonus += 18.0
        if flask_name == "No Bust" and ("Dealer's Whispers" in active_flasks or "Bonus Fortune" in active_flasks):
            combo_bonus += 18.0
        if flask_name == "Second Chance" and "Bonus Fortune" in active_flasks:
            combo_bonus += 16.0
        if flask_name == "Bonus Fortune" and ({"No Bust", "Second Chance"} & active_flasks):
            combo_bonus += 18.0
        if flask_name == "Pocket Aces" and ("Bonus Fortune" in active_flasks or has_double_item):
            combo_bonus += 18.0
        if flask_name == "Dealer's Hesitation" and ("Dealer's Whispers" in active_flasks or has_peek):
            combo_bonus += 16.0
        if flask_name == "Imminent Blackjack" and ({"No Bust", "Second Chance"} & active_flasks):
            combo_bonus += 12.0
        if flask_name == "Split Serum" and has_split_item:
            combo_bonus -= 20.0
        score = float(priority) + combo_bonus
        category = "defensive_flask" if flask_name in defensive_flasks else "offensive_flask" if flask_name in offensive_flasks else "utility_flask"
        option_metadata_by_number[number] = {
            "item_name": flask_name,
            "priority": float(priority),
            "combo_bonus": combo_bonus,
            "base_score": score,
            "price": float(_witch_flask_price_estimate(flask_name)),
            "category": category,
        }
        if priority <= 0:
            continue
        if player is None or player.get_balance() < _witch_flask_price_estimate(flask_name):
            continue
        if best_choice is None or score > best_choice[0]:
            best_choice = (score, number, flask_name)
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
        FLASK_PURCHASES[best_choice[2]] += 1
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
    return balance >= 50000 and balance < 1000000 and player.get_health() >= 55 and player.get_sanity() >= 32


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
    if player is not None:
        loan_menu_token = (CURRENT_CYCLE, int(getattr(player, "_day", 0) or 0))
        if getattr(player, "_autoplay_loan_menu_token", None) != loan_menu_token:
            player._autoplay_loan_menu_token = loan_menu_token
            player._autoplay_loan_menu_count = 0
        player._autoplay_loan_menu_count = int(getattr(player, "_autoplay_loan_menu_count", 0) or 0) + 1
        if player._autoplay_loan_menu_count >= 2:
            fallback = options[-1][0] if options else 1
            for number, label in options:
                lowered = label.lower()
                if "leave" in lowered or "never mind" in lowered:
                    fallback = number
                    break
            return _record_numeric_menu_trace(
                player,
                request_type="loan_decision",
                stable_context_id="loan_menu",
                menu_options=options,
                chosen_number=fallback,
                reason="loan_menu_reentry_exit",
                confidence=0.9,
            )

    debt = 0 if player is None else int(player.get_loan_shark_debt())
    warning = 0 if player is None or not hasattr(player, "get_loan_shark_warning_level") else int(player.get_loan_shark_warning_level())
    edge_score = _blackjack_edge_score(player)
    reserve = _cash_safety_reserve(player, 88) if player is not None else 0
    balance = 0 if player is None else player.get_balance()
    marvin_plan = _marvin_loan_plan(player) if player is not None and debt <= 0 else None
    repayment_capacity = max(0, balance - reserve)
    bootstrap_window = _loan_bootstrap_window(player)
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
            if marvin_plan is not None:
                marvin_score = 102.0 + min(18.0, float(marvin_plan["priority"]) / 8.0)
                if marvin_plan["mode"] in {"buy_enable", "marvin_push"}:
                    marvin_score += 8.0
                option_metadata_by_number[number].update(
                    {
                        "base_score": max(option_metadata_by_number[number]["base_score"], marvin_score),
                        "actionable": True,
                        "desired_amount": float(marvin_plan["borrow"]),
                        "target_item": marvin_plan["item"],
                    }
                )
            if bootstrap_window:
                option_metadata_by_number[number]["base_score"] = max(option_metadata_by_number[number]["base_score"], 96.0)
                option_metadata_by_number[number]["actionable"] = True
            if _poverty_escape_loan_mode(player):
                option_metadata_by_number[number]["base_score"] = max(option_metadata_by_number[number]["base_score"], 98.0)
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
            if _in_rank_push_window(player) and balance < 9000 and edge_score >= 2:
                option_metadata_by_number[number]["base_score"] = max(option_metadata_by_number[number]["base_score"], 84.0)
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
    bootstrap_window = _loan_bootstrap_window(player)
    marvin_plan = _marvin_loan_plan(player) if player is not None else None
    if marvin_plan is not None:
        desired = int(marvin_plan["borrow"])
    elif bootstrap_window:
        if player is not None and not player.has_item("Tool Kit"):
            desired = 2500
        else:
            desired = 1000
    elif _poverty_escape_loan_mode(player):
        desired = 5000 if edge_score >= 4 else 2500 if edge_score >= 2 else 1000
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
    if repayment_capacity <= 0:
        fallback = None
        for number, label in options:
            if "never mind" in label.lower():
                fallback = number
                break
        if fallback is None:
            fallback = options[-1][0] if options else 1
        return _record_numeric_menu_trace(
            player,
            request_type="loan_decision",
            stable_context_id="loan_repay_amount",
            menu_options=options,
            chosen_number=fallback,
            reason="repay_amount_no_capacity_exit",
            confidence=0.86,
        )
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
        and player.get_health() >= 58
        and player.get_sanity() >= 26
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
            "Drive to The Woodlands",
            "Drive to The Beach",
            "Drive to The Road",
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
    if prompt_lower == "suggest trusty tom might be able to help?":
        if player is None:
            return "no"
        return "yes"
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
        # Saving the cat: +15 sanity now, prevents -25 sanity from stray_cat_dies later.
        # Net +40 sanity vs not paying — always save if balance allows any flexibility.
        return "yes" if (player.get_balance() >= cost + 40) else "no"
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


def _decide_numbered_menu_choice(menu_options, player, prompt_lower="", recent="", recent_short=""):
    # ── Madness confrontation quiz: pick best answers for guaranteed survival ──
    # Options are ["1","2","3","4"] so they look like a numeric menu.
    # Check in reverse order (Q3→Q2→Q1) because earlier question text persists in recent.
    # Q3: "would you walk away?" → 1 "Yes. I would walk away" = +2
    if ("walk away" in recent or "first walked" in recent) and "fifty dollars" in recent and len(menu_options) == 4:
        return "1"
    # Q2: "What do you see when you look at the Dealer?" → 3 "Nothing. He's just a man" = +3
    if "what do you see" in recent and "dealer" in recent and len(menu_options) == 4:
        return "3"
    # Q1: "Why do you gamble?" → 4 "I don't know anymore" = +3
    if "why do you gamble" in recent and len(menu_options) == 4:
        return "4"

    millionaire_afternoon = (
        "choose a number" in prompt_lower
        or "choose a number" in recent_short
    ) and "drive to the airport" in recent
    if millionaire_afternoon:
        return str(_choose_millionaire_afternoon(menu_options, player))
    if _looks_like_pawn_menu(menu_options):
        return str(_choose_pawn_menu(menu_options, player))
    if "who do you want to interact with" in prompt_lower or "after noon with your companions" in recent or "afternoon with your companions" in recent:
        return str(_choose_companion_interaction(menu_options, player))
    if _looks_like_store_menu(menu_options):
        return str(_choose_store_item(menu_options, player))
    if _looks_like_loan_borrow_menu(menu_options):
        return str(_choose_loan_borrow_amount(menu_options, player))
    if _looks_like_loan_repay_menu(menu_options):
        return str(_choose_loan_repay_amount(menu_options, player))
    if _looks_like_loan_menu(menu_options):
        return str(_choose_loan_menu(menu_options, player))
    if _looks_like_afternoon_destination_menu(menu_options, prompt_lower, recent, recent_short):
        return str(_choose_destination(menu_options, player))
    if "what do you want?" in recent or "what else you want?" in recent:
        return str(_choose_store_item(menu_options, player))
    if "flask of" in recent:
        return str(_choose_witch_flask(menu_options, player))
    if "mind if i take a look at em" in recent or "is there anything you would like stuart to fix" in recent:
        return str(_choose_repair_item(menu_options, player))
    if "which item would you like stuart to upgrade" in recent:
        return str(_choose_upgrade_item(menu_options, player))
    if "car workbench" in recent:
        if "what do you want to craft" in recent.lower():
            return str(_choose_workbench_craft(menu_options, player))
        return str(_choose_workbench_menu(menu_options, player))
    return str(menu_options[-1][0] if menu_options else 1)


def _choose_inline_choice(inline_choices, player, prompt=""):
    if not inline_choices:
        return "1"

    prompt_lower = (prompt or "").lower()
    recent = _recent_lower(80)
    event_label = _latest_cycle_event_label() or "inline_choice_prompt"
    event_request = DecisionRequest(
        request_type="event_inline",
        stable_context_id=event_label,
        game_state=_current_game_state(player, context_tag=event_label).to_dict(),
        normalized_options=_structured_options(tuple(inline_choices), prefix="event_inline"),
        raw_prompt_text=prompt or "",
        raw_recent_text=tuple(RECENT_TEXT[-20:]),
        metadata=_request_metadata({
            "cycle": CURRENT_CYCLE,
            "prompt_lower": prompt_lower,
            "recent_lower": recent,
            "event_name": event_label,
        }),
    )
    event_plan = choose_strategic_goal(_current_game_state(player, context_tag=event_label))
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

    # Tom: always say yes. If can't afford, 50% chance he drops $50 — say yes to that too.
    # Oswald: always say yes. If can't afford, free $50-100 gift.
    # Frank: only accept if we can't afford Tom ($150 cheapest) or Tom already showed up.
    #   Frank is 40% success, Tom is 100% — so prefer waiting for Tom when we can afford him.

    if "frank" in recent or "i can fix this up for like" in recent:
        # If Tom already came and went, Frank is our best shot
        if player.has_met("Tom Event"):
            return True
        # If we can't afford Tom's cheapest ($150), take Frank
        if balance < 150:
            return True
        # We can afford Tom — skip Frank and wait
        return False

    # Tom and Oswald: always accept
    return True


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

    if not player.has_met("Tom Event") and balance >= 200:
        reserve = max(reserve, 200)
    elif not player.has_met("Frank Event") and balance >= 100:
        reserve = max(reserve, 100)
    if not player.has_met("Oswald Event") and balance >= 850:
        reserve = max(reserve, 850)

    return min(balance, reserve)


def _mechanic_dream_focus_reserve(player):
    return _mechanic_dream_reserve(player)


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

    if _bankroll_emergency_mode(player):
        return True

    pawn_gap = _days_since_location(player, "shop:pawn_shop")
    if pawn_gap == 0:
        return False

    balance = player.get_balance()
    sell_value = _sellable_collectible_value(player)

    if player.has_item("Car") and player.get_health() >= 60 and player.get_sanity() >= 30:
        if _wants_marvin_run(player) and sell_value < 220 and balance >= 1200:
            return False
        if _wants_adventure_run(player) and sell_value < 180 and balance >= 1000:
            return False

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
    bootstrap_window = _loan_bootstrap_window(player)

    # Refuse loans when the bot already peaked high and crashed — borrowing
    # at this point is throwing good money after bad.
    if RUN_PEAK_BALANCE >= 5000 and balance < max(500, int(RUN_PEAK_BALANCE * 0.10)):
        return False

    if player.get_health() < 48 or player.get_sanity() < 26:
        return False
    # Require at least one edge item even at very low balance.
    # Borrowing with edge_score=0 (no useful items) means gambling with borrowed money
    # at a raw house edge — the 20%/week interest will compound faster than the expected
    # win rate.  At rank 0 edge_score>=1 is a reasonable floor; edge_score>=2 for rank 1+.
    if rank == 0 and edge_score < 1 and not bootstrap_window:
        return False
    if rank >= 1 and edge_score < 2 and not bootstrap_window:
        return False
    if rank == 0:
        return balance < 1400
    if rank == 1 and not player.has_item("Map"):
        return balance < 4500
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
    marvin_plan = _marvin_loan_plan(player) if debt <= 0 else None
    if _wealth_lock_mode(player) and debt <= 0 and marvin_plan is None:
        return False
    fake_cash = _fraudulent_cash_amount(player)
    wants_doctor = _wants_doctor_visit(player)
    reserve = _cash_safety_reserve(player, 88)
    repayment_capacity = max(0, balance - reserve)
    aggressive_debt_cleanup = debt > 0 and warning >= 1 and repayment_capacity >= max(100, debt // 2)
    loan_gap = _days_since_location(player, "shop:loan_shark")
    if loan_gap == 0:
        return False
    if loan_gap is not None and loan_gap <= (1 if aggressive_debt_cleanup else (1 if debt > 0 else 2)):
        return False

    if _bankroll_emergency_mode(player):
        if debt > 0:
            return max(0, balance - _cash_safety_reserve(player, 88)) > 0
        return warning > 0 or balance <= 0

    if _poverty_escape_loan_mode(player):
        return True

    if marvin_plan is not None:
        return True

    if debt > 0:
        if repayment_capacity >= debt:
            return True
        if warning >= 1 and repayment_capacity >= min(100, debt):
            return True
        return False

    if fake_cash > 0:
        return False

    edge_score = _blackjack_edge_score(player)
    bootstrap_window = _loan_bootstrap_window(player)
    # Require at least 1 edge item before proactive borrowing: without any edge advantage
    # the bot is gambling at the raw house edge, and 20%/wk interest compounds faster
    # than the expected win rate.  (Exception: repaying existing debt is always allowed.
    # Exception 2: Marvin access at low balance — the first purchase provides edge.)
    if edge_score < 1 and not bootstrap_window and balance >= 1600:
        return False

    if bootstrap_window and balance < 2600:
        return True
    if _in_rank_push_window(player) and _has_marvin_access(player) and edge_score >= 2 and balance < 9000:
        return True

    if balance < 500:
        return True
    if player.get_rank() <= 0 and balance < 900 and player.get_health() >= 48 and player.get_sanity() >= 24:
        return True

    if player.get_health() < 42 or player.get_sanity() < 22:
        return False
    if wants_doctor:
        if player.has_item("Real Insurance"):
            if balance >= 900 and edge_score >= 1:
                return True
            return False
        if player.has_item("Faulty Insurance"):
            if balance >= 850 and edge_score >= 2:
                return True
            return False
        if balance >= max(120, _doctor_heal_cost_estimate(player)):
            if balance < 1800 and edge_score >= 2 and player.get_health() >= 50 and player.get_sanity() >= 28:
                return True
            return False
        if edge_score < 4:
            return False
    if _has_marvin_access(player) and _best_marvin_affordable_priority(player) < 90 and balance < 10000 and edge_score >= 3:
        return True
    if player.get_rank() == 0:
        if balance < 325:
            return True
        if balance < 900:
            return True
        if balance < 1800 and edge_score >= 2:
            return True
        return balance < 2500 and edge_score >= 2
    if player.get_rank() == 1 and not player.has_item("Map"):
        if bootstrap_window and player.get_sanity() >= 30:
            return balance < 8000
        return balance < 8000 and edge_score >= 2 and player.get_sanity() >= 30
    return balance < max(9000, _rank_floor(balance) + 1500) and edge_score >= 2


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


def _loan_bootstrap_window(player):
    if player is None or not player.has_item("Car"):
        return False
    if not player.has_met("Vinnie"):
        return False
    if _doctor_visit_is_urgent(player) or _fraudulent_cash_amount(player) > 0:
        return False
    if int(player.get_loan_shark_debt()) > 0:
        return False
    if player.get_health() < 55 or player.get_sanity() < 30:
        return False

    balance = player.get_balance()
    rank = int(player.get_rank()) if hasattr(player, "get_rank") else 0
    if rank == 0:
        return balance < 2500
    if rank == 1 and not player.has_item("Map"):
        return balance < 6500
    if rank <= 1 and not player.has_item("Tool Kit"):
        return balance < 4000
    return False


def _wants_adventure_run(player):
    if not _adventure_ready(player):
        return False
    if _bankroll_emergency_mode(player):
        return False
    if _wants_doctor_visit(player):
        return False
    if _needs_recovery_day(player):
        return False

    rank_val = int(player.get_rank())
    if rank_val < 0:
        return False

    balance = int(player.get_balance())
    has_utility = _has_adventure_utility(player)

    if rank_val <= 1:
        if not has_utility and balance < 9000:
            return False
        if not has_utility and not player.has_item("Map") and balance < 12000:
            return False
        if not has_utility and (player.get_health() < 66 or player.get_sanity() < 34):
            return False
        if not has_utility and (
            _in_rank_push_window(player)
            or _wants_loan_shark_run(player)
            or _wants_marvin_run(player)
            or _wants_workbench_craft_run(player)
        ):
            return False
    elif rank_val == 2 and not has_utility and balance < 14000 and _wants_upgrade_run(player):
        return False

    # Can't revisit same day
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

    return True


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


def _progression_chore_choices(labels, options, player):
    if player is None or not player.has_item("Car"):
        return []

    day = getattr(player, "_day", 1)
    chores = []
    store_summary = _store_chore_summary(player)
    workbench_candidate = _workbench_best_craft_candidate(player)
    marvin_loan_plan = _marvin_loan_plan(player)

    mechanic_choice = _choose_mechanic_progression_destination(labels, player)
    if mechanic_choice is not None:
        visits = getattr(player, "get_mechanic_visits", lambda: 0)() or 0
        score = 90 - min(36, int(visits) * 12)
        if _needs_oswald_attention(player):
            score += 24
        chores.append((score, mechanic_choice))

    marvin_choice = labels.get("Marvin's Mystical Merchandise")
    if marvin_choice is not None and _wants_marvin_run(player):
        score = 82 + min(32, _best_marvin_affordable_priority(player) // 2)
        if _marvin_bootstrap_window(player):
            score += 18
        if _in_rank_push_window(player):
            score += 12
        # Prioritise Marvin when the player is still collecting essential items.
        missing_marvin = _missing_marvin_items_count(player)
        score += min(24, missing_marvin * 3)
        # Rotation: bump score when Marvin hasn't been visited recently.
        score += _rotation_staleness_bonus(player, "shop:marvin", stale_after=2, bonus_per_day=4, max_bonus=16)
        chores.append((score, marvin_choice))

    loan_choice = labels.get("Vinnie's Back Alley Loans")
    if loan_choice is not None and _wants_loan_shark_run(player):
        score = 82
        if _poverty_escape_loan_mode(player):
            score += 40
        elif _loan_bootstrap_window(player):
            score += 28
        if marvin_loan_plan is not None:
            score += 42 + min(18, int(marvin_loan_plan["priority"]) // 6)
            if marvin_loan_plan["mode"] in {"buy_enable", "marvin_push"}:
                score += 10
        if _in_rank_push_window(player):
            score += 14
        warning = int(player.get_loan_shark_warning_level()) if hasattr(player, "get_loan_shark_warning_level") else 0
        debt = int(player.get_loan_shark_debt()) if hasattr(player, "get_loan_shark_debt") else 0
        score += min(24, warning * 10 + debt // 250)
        chores.append((score, loan_choice))

    workbench_choice = labels.get("Car Workbench")
    if workbench_choice is not None and _wants_workbench_craft_run(player):
        craft_priority = 0 if workbench_candidate is None else int(workbench_candidate[1])
        score = 74 + min(30, craft_priority // 2)
        if int(player.get_rank()) <= 1:
            score += 12
        if _in_rank_push_window(player):
            score += 10
        if not player.has_met("Car Workbench"):
            score += 18
        # Rotation: encourage crafting when the workbench hasn't been used recently.
        score += _rotation_staleness_bonus(player, "shop:car_workbench", stale_after=3, bonus_per_day=5, max_bonus=20)
        chores.append((score, workbench_choice))

    store_choice = labels.get("Convenience Store")
    if store_choice is not None and _wants_store_run(player):
        top = store_summary["top"]
        top_priority = 0 if top is None else int(top[0])
        top_item = "" if top is None else str(top[2])
        score = 60 + min(24, top_priority // 3)
        score += min(18, store_summary["count"] * 5)
        score += min(16, store_summary["actionable_count"] * 6)
        if top_item == "Tool Kit":
            score += 18
        elif _in_rank_push_window(player) and top_priority < 92 and (top is None or int(top[1]) <= max(260, int(player.get_balance() * 0.10))):
            score -= 12
        # Rotation: reward the store when it hasn't been visited in a while.
        score += _rotation_staleness_bonus(player, "shop:convenience_store", stale_after=2, bonus_per_day=5, max_bonus=20)
        chores.append((score, store_choice))

    adventure_choice = _choose_adventure_destination(options, player) if _wants_adventure_run(player) else None
    if adventure_choice is not None:
        score = 56 + int(player.get_rank()) * 8
        if _has_adventure_utility(player):
            score += 12
        score += (day % 3) * 2
        # Rotation: adventures are the fallback rotation filler — give them a
        # meaningful staleness bonus so they aren't crowded out indefinitely.
        score += _rotation_staleness_bonus(
            player,
            "adventure:road",
            "adventure:woodlands",
            "adventure:swamp",
            "adventure:beach",
            "adventure:ocean_depths",
            "adventure:city",
            stale_after=2,
            bonus_per_day=6,
            max_bonus=24,
        )
        chores.append((score, adventure_choice))

    upgrade_choice = labels.get("Oswald's Optimal Outoparts")
    if upgrade_choice is not None and _wants_upgrade_run(player):
        upgrade_candidate = _best_upgrade_candidate(player)
        urgency = 52 if upgrade_candidate is None else int(upgrade_candidate[0])
        chores.append((58 + min(28, urgency // 2), upgrade_choice))

    chores.sort(key=lambda entry: (-entry[0], entry[1]))
    return [choice for _score, choice in chores]


def _choose_progression_destination(labels, options, player):
    if player is None or not player.has_item("Car"):
        return None
    ordered = _progression_chore_choices(labels, options, player)
    doctor_choice = labels.get("Doctor's Office") if _wants_doctor_visit(player) else None
    for choice in ordered + ([doctor_choice] if doctor_choice is not None else []):
        if choice is not None:
            return choice
    return None


def _legacy_choose_destination(options, player):
    _mark_afternoon_menu_presented(player, options)

    def finalize(choice):
        return _record_route_choice_flow(player, choice, options)

    labels = {label: number for number, label in options}

    medical_choice = _medical_destination_label(player)
    if medical_choice in labels and _doctor_visit_is_urgent(player):
        return finalize(labels[medical_choice])

    if _needs_recovery_day(player) and "Stay Home" in labels:
        return finalize(labels["Stay Home"])

    progression_choice = _choose_progression_destination(labels, options, player)
    if progression_choice is not None:
        progression_label = next((label for label, number in labels.items() if number == progression_choice), "")
        if (
            "Marvin's Mystical Merchandise" == progression_label
            or progression_label.startswith("Drive to ")
            # Loan shark bootstrapping is just as time-sensitive as Marvin — give it the
            # same priority bypass so it isn't blocked by the pawn/store guards below.
            or ("Vinnie's Back Alley Loans" == progression_label and _poverty_escape_loan_mode(player))
        ):
            return finalize(progression_choice)

    if "Grimy Gus's Pawn Emporium" in labels and _wants_pawn_cashout(player):
        return finalize(labels["Grimy Gus's Pawn Emporium"])

    # Flask-only witch visit: healthy player with affordable flask at rank 2+.
    # Placed after pawn shop and progression so it doesn't override Marvin/adventure.
    if "Witch Doctor's Tower" in labels and _wants_witch_flask_only_run(player):
        return finalize(labels["Witch Doctor's Tower"])

    if medical_choice in labels and (_wants_doctor_visit(player) or _wants_witch_heal(player)):
        return finalize(labels[medical_choice])

    if medical_choice in labels:
        return finalize(labels[medical_choice])

    if progression_choice is not None:
        return finalize(progression_choice)

    if "Convenience Store" in labels and _wants_store_run(player):
        return finalize(labels["Convenience Store"])

    if "Stay Home" in labels:
        return finalize(labels["Stay Home"])

    return finalize(options[-1][0] if options else 1)


def _quicktest_route_tags(label):
    lowered = str(label or "").lower()
    tags = set()
    if "doctor" in lowered:
        tags.add("medical")
    if "witch" in lowered:
        tags.add("witch")
        tags.add("medical")
    if "marvin" in lowered:
        tags.add("marvin")
    if "vinnie" in lowered or "loan" in lowered:
        tags.add("loan")
    if "pawn" in lowered or "gus" in lowered:
        tags.add("pawn")
    if "convenience" in lowered:
        tags.add("store")
    if "workbench" in lowered or "outoparts" in lowered:
        tags.add("upgrade")
    if "tom" in lowered or "frank" in lowered or "oswald" in lowered:
        tags.add("mechanic")
    if label.startswith("Drive to "):
        tags.add("adventure")
    if "stay home" in lowered:
        tags.add("stay_home")
    return tags


def _planner_choose_destination(options, player):
    if player is None or not options:
        return None

    menu_options = list(options)
    store_summary = _store_chore_summary(player)
    game_state = _current_game_state(player, menu_options=menu_options, context_tag="route_select")
    plan = choose_strategic_goal(game_state)
    if player is not None and hasattr(player, "request_progress_goal"):
        player.request_progress_goal(
            plan.goal,
            reason=plan.reason,
            source="planner:route_select",
            sticky=plan.goal in {"acquire_car", "unlock_marvin", "reach_adventure_threshold"},
        )
    plan_top_score = max(plan.scores.values(), default=0.0)
    store_goal_score = float(plan.scores.get("restock_supplies", 0.0) or 0.0)
    pawn_goal_score = float(plan.scores.get("cashout_pawn_inventory", 0.0) or 0.0)
    store_spend = game_state.store_target_spend
    pawn_value = game_state.pawn_sellable_value
    catalog_push = _catalog_push_candidate(player)
    loan_pressure = max(
        int(player.get_loan_shark_debt()) if hasattr(player, "get_loan_shark_debt") else 0,
        (int(player.get_loan_shark_warning_level()) if hasattr(player, "get_loan_shark_warning_level") else 0) * 200,
    )
    # Poverty escape: flag when the bot has a car, no debt, and not enough cash to
    # pay even the cheapest mechanic quote ($150 at Tom). Visiting Vinnie first for a
    # loan breaks the "visit Tom but can't pay" loop.
    poverty_loan_mode = bool(
        _poverty_escape_loan_mode(player)
        and game_state.balance < 150
        and _wants_loan_shark_run(player)
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
    marvin_future_priority = 0
    marvin_future_shortfall = 0
    wants_marvin_raw = _wants_marvin_run(player)
    wants_marvin = wants_marvin_raw and not _should_suspend_marvin_pressure(player, plan.goal)
    if wants_marvin:
        # AGGRESSIVE: If bot wants Marvin, give it high priority in routing
        marvin_priority = 100
        future_candidate = _best_future_marvin_candidate(player, game_state.balance) if _has_marvin_access(player) else None
        if future_candidate is not None:
            marvin_future_priority = int(future_candidate["priority"])
            marvin_future_shortfall = int(future_candidate["shortfall"])
    adventure_readiness = 0
    if _wants_adventure_run(player):
        adventure_readiness = min(100, max(30, int(player.get_rank()) * 20 + max(0, player.get_health() - 60) // 2 + max(0, player.get_sanity() - 35) // 2))
    wants_store = game_state.store_candidate_count > 0
    wants_pawn = game_state.pawn_planned_sale_value > 0
    workbench_craft_candidate = _workbench_best_craft_candidate(player) if _wants_workbench_craft_run(player) else None
    workbench_craft_priority = workbench_craft_candidate[1] if workbench_craft_candidate else 0
    route_labels = {label for _number, label in menu_options}
    if "Marvin's Mystical Merchandise" in route_labels:
        _bump_funnel_metric(player, "marvin_route_present_count")
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
        metadata=_request_metadata({
            "cycle": CURRENT_CYCLE,
            "day": game_state.day,
            "urgent_medical": _doctor_visit_is_urgent(player),
            "needs_recovery_day": _needs_recovery_day(player),
            "medical_choice": _medical_destination_label(player),
            "wants_doctor": _wants_doctor_visit(player) and not defer_doctor,
            "wants_witch": _wants_witch_heal(player),
            "wants_witch_flask_only": _wants_witch_flask_only_run(player),
            "wants_workbench_craft": _wants_workbench_craft_run(player),
            "workbench_craft_priority": workbench_craft_priority,
            "wants_marvin": wants_marvin,
            "wants_loan": _wants_loan_shark_run(player),
            "poverty_loan_mode": poverty_loan_mode,
            "wants_store": wants_store,
            "wants_adventure": _wants_adventure_run(player),
            "has_adventure_utility": _has_adventure_utility(player),
            "wants_upgrade": _wants_upgrade_run(player),
            "wants_mechanic": _wants_mechanic_progression_run(player),
            "wants_pawn": wants_pawn,
            "store_spend": store_spend,
            "store_actionable_count": int(store_summary["actionable_count"]),
            "catalog_push_active": catalog_push is not None,
            "catalog_push_kind": "" if catalog_push is None else str(catalog_push["kind"]),
            "catalog_push_spend": 0 if catalog_push is None else int(catalog_push["target_spend"]),
            "catalog_push_count": 0 if catalog_push is None else int(catalog_push["count"]),
            "catalog_push_priority": 0 if catalog_push is None else int(catalog_push["priority"]),
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
            "marvin_future_priority": marvin_future_priority,
            "marvin_future_shortfall": marvin_future_shortfall,
            "adventure_readiness": adventure_readiness,
            "has_car": game_state.has_car,
            "has_marvin_access": game_state.has_marvin_access,
            "mechanic_visits": game_state.mechanic_visits,
            "rank": game_state.rank,
            "bankroll_emergency": game_state.bankroll_emergency,
            "fragile_post_car": game_state.fragile_post_car,
            "location_circulation": _route_circulation_metadata(player, menu_options),
        }),
    )
    _record_decision_request(request)
    choice, trace = choose_route_option(request, plan)
    if choice is None:
        trace.metadata["route_outcome"] = "no_choice"
    else:
        planner_applied = trace.confidence >= 0.40
        trace.metadata["planner_applied"] = planner_applied
        trace.metadata["route_outcome"] = "applied" if planner_applied else "suppressed"
    _record_decision_trace(trace)
    if choice is None:
        return None
    chosen_tags = _quicktest_route_tags(choice.label)
    if plan.goal in {"push_next_rank", "exploit_marvin", "restock_supplies", "reach_adventure_threshold"}:
        if "loan" in chosen_tags:
            _bump_funnel_metric(player, "debt_growth_override_count")
            _bump_funnel_metric(player, "loan_growth_override_count")
        if "pawn" in chosen_tags:
            _bump_funnel_metric(player, "debt_growth_override_count")
            _bump_funnel_metric(player, "pawn_growth_override_count")
    if trace.confidence < 0.40:
        return None
    return int(choice.value)


def _choose_destination(options, player):
    _mark_afternoon_menu_presented(player, options)

    def finalize(choice):
        return _record_route_choice_flow(player, choice, options)

    labels = {label: number for number, label in options}
    medical_choice = _medical_destination_label(player)
    balance = 0 if player is None else int(player.get_balance())
    warning = 0 if player is None or not hasattr(player, "get_loan_shark_warning_level") else int(player.get_loan_shark_warning_level())
    debt = 0 if player is None or not hasattr(player, "get_loan_shark_debt") else int(player.get_loan_shark_debt())
    debt_cleanup_payment = max(0, balance - (_cash_safety_reserve(player, 88) if player is not None else 0))
    debt_cleanup_ready = (
        player is not None
        and "Vinnie's Back Alley Loans" in labels
        and debt > 0
        and _wants_loan_shark_run(player)
        and player.get_health() >= 42
        and player.get_sanity() >= 24
        and debt_cleanup_payment >= (min(100, debt) if warning >= 1 else max(100, debt // 2))
    )

    # ── PRIORITY 1: Urgent medical (life-threatening) ──
    if medical_choice in labels and _doctor_visit_is_urgent(player):
        _record_route_interrupt_trace(player, labels[medical_choice], f"urgent medical override -> {medical_choice}", "survive_emergency", "urgent_medical")
        return finalize(labels[medical_choice])

    # ── PRIORITY 2: Marvin force-buy ($10k+ with access and unbought items) ──
    # Marvin is the single highest-leverage location once affordable.  Route here
    # every day it's available until completely bought out.
    forced_marvin = _force_marvin_buy_interrupt(player, labels)
    if forced_marvin is not None:
        _bump_funnel_metric(player, "marvin_direct_gate_count")
        _record_route_interrupt_trace(player, forced_marvin, "hard marvin 10k force-buy", "exploit_marvin", "marvin_force_buy_10k")
        return finalize(forced_marvin)

    # ── PRIORITY 3: Debt cleanup (loan warning level high) ──
    if debt_cleanup_ready:
        _record_route_interrupt_trace(
            player,
            labels["Vinnie's Back Alley Loans"],
            "debt cleanup override -> Vinnie's Back Alley Loans",
            "reduce_debt_risk",
            "debt_cleanup_window",
        )
        return finalize(labels["Vinnie's Back Alley Loans"])

    # ── PRIORITY 4: Pawn cashout (broke / needs cash for a specific goal) ──
    # At low balances (≤ $1000), no gap enforcement — survival-critical.
    # Above $1000, require 2-day gap to prevent hogging the rotation.
    pawn_gap = _days_since_location(player, "shop:pawn_shop") if player is not None else None
    pawn_gap_ok = True if balance <= 1000 else (pawn_gap is None or pawn_gap >= 2)
    if (
        "Grimy Gus's Pawn Emporium" in labels
        and _wants_pawn_cashout(player)
        and pawn_gap_ok
    ):
        _record_route_interrupt_trace(player, labels["Grimy Gus's Pawn Emporium"], "pawn cashout interrupt", "cashout_pawn_inventory", "pawn_cashout_interrupt")
        return finalize(labels["Grimy Gus's Pawn Emporium"])

    # ── PRIORITY 5: Planner (goal-based scoring across all locations) ──
    planner_choice = _planner_choose_destination(options, player)
    if planner_choice is not None:
        return finalize(planner_choice)

    # ── PRIORITY 6: Loan shark bootstrap (broke, no debt, need cash injection) ──
    if "Vinnie's Back Alley Loans" in labels and _poverty_escape_loan_mode(player):
        _record_route_interrupt_trace(player, labels["Vinnie's Back Alley Loans"], "poverty-escape loan bootstrap", "push_next_rank", "poverty_loan_bootstrap")
        return finalize(labels["Vinnie's Back Alley Loans"])

    # ── PRIORITY 7: Witch flask purchase (healthy player, affordable flask) ──
    if "Witch Doctor's Tower" in labels and _wants_witch_flask_only_run(player):
        _record_route_interrupt_trace(player, labels["Witch Doctor's Tower"], "witch flask-only visit", "exploit_witch_flask", "witch_flask_only")
        return finalize(labels["Witch Doctor's Tower"])

    # ── PRIORITY 8: Legacy fallback (progression, store, stay home) ──
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
            "gift_target": item_name in GIFT_WORTHY_ITEMS and _gift_run_ready(player),
            "companion_food": _is_companion_food_item(item_name, player),
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

    target_companion = _best_companion_name(player)
    if target_companion is not None:
        for number, label in options:
            lowered = label.lower()
            if target_companion.lower() in lowered:
                return _record_numeric_menu_trace(
                    player,
                    request_type="menu_select",
                    stable_context_id="companion_menu",
                    menu_options=options,
                    chosen_number=number,
                    reason=f"target_companion:{target_companion}",
                    confidence=0.66,
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
            if _is_protected_pawn_item(item_name):
                continue
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


def _looks_like_store_menu(options):
    """Return True when options look like the Kyle convenience-store item menu.

    The store always appends "I'm not buying anything" as the last option.
    We rely on this structural feature rather than scanning recent text because
    the item list can easily exceed the 120-char recent window, causing the old
    ``"what do you want?" in recent`` check to miss the store entirely and fall
    through to the generic last-option fallback ("I'm not buying anything").
    Item price labels use ANSI color codes (e.g. green/bright "$3"), so checking
    for a literal " - $" pattern is unreliable; the exit-option text is plain.
    """
    labels = [label.lower() for _number, label in options]
    return any("i'm not buying anything" in label for label in labels)


def _decide_yes_no(prompt=""):
    player = CURRENT_PLAYER
    prompt_lower = (prompt or "").lower().strip()
    recent = _recent_lower(80)
    recent_mechanic = _recent_lower(20)
    cost = _extract_cash_amount(prompt, recent)
    event_label = _latest_cycle_event_label() or "yes_no_prompt"

    def finalize(answer, reason, confidence=0.62):
        _record_structured_trace(
            player,
            request_type="yes_no",
            stable_context_id=event_label,
            chosen_action=answer,
            reason=reason,
            confidence=confidence,
            prompt=prompt,
            options=("yes", "no"),
            metadata={
                "cost": cost,
                "prompt_lower": prompt_lower,
                "event_name": event_label,
            },
        )
        return answer

    if player is not None and hasattr(player, "was_millionaire_visited") and player.was_millionaire_visited():
        millionaire_endgame_prompts = {
            "take the phone call?": "millionaire_tom_take_call",
            '"will you come back home?"': "millionaire_tom_go_home",
            "put on the jacket?": "millionaire_frank_accept",
            "accept oswald's offer?": "millionaire_oswald_accept",
        }
        millionaire_reason = millionaire_endgame_prompts.get(prompt_lower)
        if millionaire_reason is not None:
            return finalize("yes", millionaire_reason, 0.96)

    mechanic_answer = _decide_mechanic_intro_response(player, recent_mechanic, prompt, source="yesno")
    if mechanic_answer is not None:
        return finalize(mechanic_answer, "mechanic_intro_offer")

    if (
        "whaddya say" in recent
        or "what do you think" in recent
        or "you buying" in recent
        or "you interested" in recent
        or "you buying" in prompt_lower
        or "you interested" in prompt_lower
    ):
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
            balance = player.get_balance()
            if balance >= 10000 and balance >= cost and not _doctor_visit_is_urgent(player):
                return finalize("yes", f"marvin_offer_forced_10k:{current_offer}", 0.95)
            conversion_window_items = _marvin_conversion_items()
            post_purchase_floor = _marvin_post_purchase_floor(player, current_offer)
            rank = int(player.get_rank()) if hasattr(player, "get_rank") else 0
            if rank >= 2 and current_offer not in conversion_window_items and priority < 70:
                return finalize("no", f"marvin_offer_rank2_low_priority:{current_offer}")
            doctor_res = max(60, _doctor_cash_reserve(player))
            if (
                rank >= 2
                and current_offer in conversion_window_items
                and priority >= 60
                and balance >= cost
                and not _doctor_visit_is_urgent(player)
                and not _needs_doctor(player)
                and player.get_health() >= 68
                and player.get_sanity() >= 40
            ):
                conversion_floor = max(doctor_res, post_purchase_floor)
                if balance - cost >= conversion_floor:
                    return finalize("yes", f"marvin_offer_conversion_window:{current_offer}", 0.76)
            if rank >= 2:
                rank2_post_purchase_floor = 15000
                if current_offer not in conversion_window_items and balance - cost < rank2_post_purchase_floor and priority < 88:
                    return finalize("no", f"marvin_offer_rank2_post_purchase_floor:{current_offer}")
            if rank <= 1 and priority >= 84 and balance >= cost and balance - cost >= doctor_res:
                return finalize("yes", f"marvin_offer_rank01_high_priority:{current_offer}", 0.82)
            if rank <= 1 and priority >= 76 and balance >= cost and balance - cost >= doctor_res + 120:
                return finalize("yes", f"marvin_offer_rank01_edge_window:{current_offer}", 0.76)
            if _can_afford_optional_purchase(player, cost, priority):
                return finalize("yes", f"marvin_offer_affordable:{current_offer}", 0.8)
            if priority >= 88 and balance >= cost:
                in_push = _in_rank_push_window(player)
                doctor_res = max(120, _doctor_cash_reserve(player))
                _rank_thresholds = [0, 1000, 10000, 100000, 400000, 750000]
                rank_below_floor = _rank_thresholds[max(0, min(rank - 1, 5))]
                if in_push:
                    if balance - cost >= max(doctor_res, rank_below_floor):
                        return finalize("yes", f"marvin_offer_push_window:{current_offer}", 0.72)
                else:
                    prot = _rank_protection_floor(player)
                    if balance - cost >= max(doctor_res, prot):
                        return finalize("yes", f"marvin_offer_high_priority:{current_offer}", 0.68)
            return finalize("no", f"marvin_offer_budget_block:{current_offer}")
        must_have = any(name in recent for name in [
            "faulty insurance", "health indicator", "delight indicator", "rusty compass",
            "spare tire", "tire patch kit", "fix-a-flat", "tool kit", "first aid kit",
        ])
        affordable = player.get_balance() >= cost
        conservative = cost <= max(200, int(player.get_balance() * 0.25))
        answer = "yes" if affordable and (must_have or conservative) else "no"
        return finalize(answer, "generic_offer_budget_gate")

    event_request, event_plan = _build_event_policy_request(
        player,
        request_type="yes_no",
        stable_context_id=event_label,
        options=("yes", "no"),
        prompt=prompt,
        metadata={
            "prompt_lower": prompt_lower,
            "recent_lower": recent,
            "cost": cost,
            "event_name": event_label,
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
        # Never skip a needed doctor visit to socialise — medical need takes priority.
        if player is not None and (_doctor_visit_is_urgent(player) or _wants_doctor_visit(player)):
            answer = "no"
        elif player is not None and _wants_marvin_run(player) and not _bankroll_emergency_mode(player):
            # Yield companion time when Marvin visit is actively queued so the
            # player reaches the destination menu and can go to the shop.
            answer = "no"
        else:
            answer = "yes" if player is not None and _wants_companion_time(player) else "no"
        return finalize(answer, "companion_recovery_gate")
    # Phil / final interrogation: "yes" = 25% death, "no" = 33% death.
    # Answer yes for better survival odds.
    if "will you leave" in recent and "answer me" in prompt_lower:
        return finalize("yes", "interrogation_better_odds", 0.95)
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
        protected_sale_tokens = ("sell map", "sell the map", "sell worn map", "sell the worn map", "sell tool kit", "sell the tool kit")
        if any(token in prompt_lower for token in protected_sale_tokens):
            return finalize("no", "protect_progression_sale_block")
        planned_sales = {item_name.lower() for item_name in _planned_pawn_sales(player)}
        for item_name in planned_sales:
            if item_name in prompt_lower:
                return finalize("yes", "planned_pawn_sale")
        return finalize("no", "unplanned_sale_block")
    if "continue?" in prompt_lower:
        return finalize("no", "continue_prompt_stop")
    if "purchase any of my powerful potions" in recent or "mood to spend some money on my magic potions" in recent:
        if player is None:
            return finalize("no", "witch_potion_without_player")
        if _flask_count(player) >= 2:
            return finalize("no", "witch_potion_capacity_block")
        # Allow earlier inspection so mid-game bankroll spikes can actually convert
        # into flasks before the next damage spiral wipes the run.
        answer = "yes" if player.get_balance() >= 6000 else "no"
        return finalize(answer, "witch_potion_budget_gate")
    if "heal you" in recent and "witch doctor" in recent:
        # Say YES to healing if we genuinely need it; say NO on a flask-only visit
        # (heal costs 5-25% of balance — save that cash for the flask purchase).
        if _wants_witch_heal(player):
            answer = "yes"
            reason = "witch_heal_gate"
        elif _wants_witch_flask_only_run(player):
            answer = "no"
            reason = "witch_flask_only_skip_heal"
        else:
            answer = "no"
            reason = "witch_heal_gate"
        return finalize(answer, reason)
    if _should_buy_car_repair(player, cost, recent):
        return finalize("yes", "car_repair_required", 0.82)
    if _needs_car(player) and any(name in recent for name in ["tom", "frank", "oswald", "stuart"]):
        return finalize("no", "decline_non_viable_car_offer")
    if "do you accept this offer" in recent and "stuart" in recent:
        if cost is None or player is None:
            return finalize("no", "stuart_offer_missing_cost")
        answer = "yes" if player.get_balance() >= cost and cost <= max(90000, int(player.get_balance() * 0.55)) else "no"
        return finalize(answer, "stuart_offer_budget_gate")
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
    # Track consecutive fallback hits for the same event label — crash if stuck.
    global _YN_FALLBACK_STREAK, _YN_FALLBACK_LABEL
    if event_label == _YN_FALLBACK_LABEL:
        _YN_FALLBACK_STREAK += 1
        if _YN_FALLBACK_STREAK > 20:
            raise RuntimeError(
                f"yes/no fallback loop: {_YN_FALLBACK_STREAK}x for "
                f"{event_label!r}, cycle={CURRENT_CYCLE}"
            )
    else:
        _YN_FALLBACK_LABEL = event_label
        _YN_FALLBACK_STREAK = 1

    if player is not None and (player.get_balance() >= 1000 or int(player.get_rank()) >= 1):
        _record_fallback_decision("yesno", prompt, recent, source="high-resource-default")
        return finalize("no", "fallback_high_resource_default", 0.35)
    _record_fallback_decision("yesno", prompt, recent, source="low-resource-default")
    return finalize("yes", "fallback_low_resource_default", 0.3)


def _decide_option(prompt, options):
    player = CURRENT_PLAYER
    prompt_lower = (prompt or "").lower()
    recent = _recent_lower(80)
    recent_short = "\n".join(RECENT_TEXT[-5:]).lower()
    event_label = _latest_cycle_event_label() or "option_prompt"
    numeric_option_prompt = _looks_like_numeric_menu_prompt(options)

    if numeric_option_prompt:
        menu_options = _resolve_numeric_menu_options(options)
        if menu_options:
            chosen_number = _decide_numbered_menu_choice(menu_options, player, prompt_lower, recent, recent_short)
            return _map_numeric_choice_to_option_token(chosen_number, options)
        if options:
            return str(options[-1])

    def finalize(chosen, reason, confidence=0.55):
        _record_structured_trace(
            player,
            request_type="event_branch",
            stable_context_id=event_label,
            chosen_action=chosen,
            reason=reason,
            confidence=confidence,
            prompt=prompt,
            options=tuple(options),
            metadata={
                "prompt_lower": prompt_lower,
                "event_name": event_label,
            },
        )
        return chosen

    event_request, event_plan = _build_event_policy_request(
        player,
        request_type="event_branch",
        stable_context_id=event_label,
        options=tuple(options),
        prompt=prompt,
        metadata={
            "prompt_lower": prompt_lower,
            "recent_lower": recent,
            "event_name": event_label,
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
    global LAST_INPUT_FINGERPRINT, REPEATED_INPUT_COUNT, _BLANK_PROMPT_STREAK

    # Crash safety: detect infinite blank-prompt loops.  ask.yes_or_no() calls
    # input("") in a while-True loop; if our routing returns something it doesn't
    # recognise, each "What? " reiteration changes the fingerprint so the
    # REPEATED_INPUT_COUNT safety never fires.  This hard counter does.
    if not (prompt or "").strip():
        _BLANK_PROMPT_STREAK += 1
        if _BLANK_PROMPT_STREAK > 50:
            hint = "\n".join(RECENT_TEXT[-5:])[:200] if RECENT_TEXT else "(empty)"
            raise RuntimeError(
                f"Input loop: {_BLANK_PROMPT_STREAK} consecutive blank prompts | "
                f"cycle={CURRENT_CYCLE} | recent={hint!r}"
            )
    else:
        _BLANK_PROMPT_STREAK = 0

    player = CURRENT_PLAYER
    prompt_lower = (prompt or "").lower()
    options = _get_recent_menu_options()
    recent = _recent_lower(120)
    recent_mechanic = _recent_lower(20)
    recent_short = "\n".join(RECENT_TEXT[-5:]).lower()
    inline_choices = _extract_inline_choices(prompt, *RECENT_TEXT[-12:])
    fingerprint = (prompt_lower.strip(), "\n".join(RECENT_TEXT[-10:]).lower())
    raw_override = None
    event_label = _latest_cycle_event_label() or "raw_input_prompt"
    witch_numeric_menu_visible = (
        "choose a number" in recent_short
        and "flask of" in recent
        and "i'm not buying anything" in recent
    )

    if inline_choices:
        event_request, event_plan = _build_event_policy_request(
            player,
            request_type="event_inline",
            stable_context_id=event_label,
            options=tuple(inline_choices),
            prompt=prompt,
            metadata={
                "prompt_lower": prompt_lower,
                "recent_lower": recent,
                "event_name": event_label,
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
        if "choose a number" in prompt_lower or "choose a number" in recent_short:
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
    # Detect yes/no reiteration: ask.yes_or_no() prints "What? " when it gets
    # unrecognised input.  Catch this BEFORE numbered-menu heuristics below
    # intercept the blank prompt via stale "choose a number" text in recent.
    if not prompt_lower and any(
        rt.strip().lower().startswith("what?") for rt in RECENT_TEXT[-3:]
    ):
        return _decide_yes_no(prompt)
    if not prompt_lower and any(
        phrase in recent for phrase in [
            "would you like me to heal you", "you buying", "what do you think", "whaddya say",
            "do you accept", "are you in the mood to spend some money on my magic potions",
            "care to purchase any of my powerful potions", "you interested", "you game",
            "could ya do", "speak up", "come again", "mumbling",
        ]
    ) and not witch_numeric_menu_visible:
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
        or "choose a number" in recent_short
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
    if "choose a number" in prompt_lower or "choose a number" in recent_short:
        return _decide_numbered_menu_choice(options, player, prompt_lower, recent, recent_short)
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
    if balance < 400000:
        return 400000
    if balance < 750000:
        return 750000
    return 1000000


def _rank_floor(balance):
    if balance >= 750000:
        return 750000
    if balance >= 400000:
        return 400000
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
        metadata=_request_metadata({
            "cycle": CURRENT_CYCLE,
            "day": game_state.day,
        }, metadata),
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
    marvin_purchase_push = _marvin_purchase_push_candidate(player, balance=balance)
    catalog_push = _catalog_push_candidate(player, balance=balance)
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
            "has_unbought_marvin_items": _has_unbought_marvin_items(player),
            "marvin_remaining_spend": _marvin_remaining_spend(player),
            "purchase_push_active": marvin_purchase_push is not None,
            "purchase_push_kind": "marvin" if marvin_purchase_push is not None else "",
            "purchase_push_price": 0 if marvin_purchase_push is None else int(marvin_purchase_push["price"]),
            "purchase_push_shortfall": 0 if marvin_purchase_push is None else int(marvin_purchase_push["shortfall"]),
            "purchase_push_priority": 0 if marvin_purchase_push is None else int(marvin_purchase_push["priority"]),
            "catalog_push_active": catalog_push is not None,
            "catalog_push_kind": "" if catalog_push is None else str(catalog_push["kind"]),
            "catalog_push_spend": 0 if catalog_push is None else int(catalog_push["target_spend"]),
            "catalog_push_count": 0 if catalog_push is None else int(catalog_push["count"]),
            "catalog_push_priority": 0 if catalog_push is None else int(catalog_push["priority"]),
            "stall_days": _progress_stall_days(player),
            "early_caution": _needs_car(player) and getattr(player, "_day", 1) <= 10,
            "stranded_no_car": _stranded_no_car_mode(player),
            "survival_mode": _wants_doctor_visit(player) or _doctor_visit_is_urgent(player) or _needs_recovery_day(player),
            "needs_car": _needs_car(player),
            "ever_had_car": EVER_HAD_CAR or player.has_item("Car"),
            "wants_millionaire_push": _wants_millionaire_push(player),
            "is_millionaire": bool(player.is_millionaire()) if hasattr(player, "is_millionaire") else False,
            "has_extra_round_item": _has_extra_round_item(player),
            "urgent_doctor": _doctor_visit_is_urgent(player),
            "bankroll_emergency": strategic_state.bankroll_emergency,
            "fragile_post_car": strategic_state.fragile_post_car,
            "has_met_tom": player.has_met("Tom Event"),
            "has_met_frank": player.has_met("Frank Event"),
            "has_met_oswald": player.has_met("Oswald Event"),
            "car_progress_reserve": _car_progress_reserve(player),
            "mechanic_purchase_reserve": _mechanic_purchase_reserve(player),
            "mechanic_dream_reserve": _mechanic_dream_focus_reserve(player),
            "known_car_repair_reserve": _known_car_repair_reserve(player),
            "has_faulty_insurance": player.has_item("Faulty Insurance"),
            "wants_map_unlock": _wants_map_unlock_window(player),
            "loan_debt": int(player.get_loan_shark_debt()) if hasattr(player, "get_loan_shark_debt") else 0,
            "loan_warning_level": int(player.get_loan_shark_warning_level()) if hasattr(player, "get_loan_shark_warning_level") else 0,
            "run_peak_balance": RUN_PEAK_BALANCE,
            # ── Item/flask-specific bet multiplier flags ─────────────────────────
            # These let the policy respond to each item's direct EV impact
            # rather than only seeing the blunt aggregate edge_score.
            # Catastrophic-opportunity flasks
            "bet_has_imminent_blackjack": (
                hasattr(player, "has_flask_effect") and player.has_flask_effect("Imminent Blackjack")
            ),
            "bet_has_no_bust": (
                hasattr(player, "has_flask_effect") and player.has_flask_effect("No Bust")
            ),
            "bet_has_dealers_whispers": (
                hasattr(player, "has_flask_effect") and player.has_flask_effect("Dealer's Whispers")
            ),
            "bet_has_second_chance": (
                hasattr(player, "has_flask_effect") and player.has_flask_effect("Second Chance")
                and not getattr(self, "_Blackjack__used_second_chance", True)
            ),
            "bet_has_dealers_hesitation": (
                hasattr(player, "has_flask_effect") and player.has_flask_effect("Dealer's Hesitation")
            ),
            # Luck / protection items (stochastic EV per hand)
            "bet_has_lucky_medallion": _has_active_item(player, "Lucky Medallion"),
            "bet_has_lucky_coin": _has_active_item(player, "Lucky Coin"),
            "bet_has_invisible_cloak": _has_active_item(player, "Invisible Cloak"),
            "bet_has_tattered_cloak": _has_active_item(player, "Tattered Cloak"),
            "bet_has_velvet_gloves": _has_active_item(player, "Velvet Gloves"),
            "bet_has_worn_gloves": _has_active_item(player, "Worn Gloves"),
            # Action-expanding items (double / split / surrender changes bet leverage)
            "bet_has_chalice": (
                _has_active_item(player, "Gambler's Chalice")
                or _has_active_item(player, "Overflowing Goblet")
                or (hasattr(player, "has_flask_effect") and player.has_flask_effect("Bonus Fortune"))
            ),
            "bet_has_locket": (
                _has_active_item(player, "Twin's Locket")
                or _has_active_item(player, "Mirror of Duality")
                or (hasattr(player, "has_flask_effect") and player.has_flask_effect("Split Serum"))
            ),
            "bet_has_phoenix_feather": _has_active_item(player, "Phoenix Feather"),
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
            "has_dealers_mercy": player.has_item("Dealer's Mercy"),
            "has_dealers_grudge": player.has_item("Dealer's Grudge"),
            "balance": int(self._Blackjack__balance),
            "insurance_cost": int(insurance_cost),
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
            "has_no_bust": player.has_flask_effect("No Bust"),
            "has_dealers_hesitation": player.has_flask_effect("Dealer's Hesitation"),
            "has_dealers_whispers": player.has_flask_effect("Dealer's Whispers"),
            "has_lucky_medallion": _has_active_item(player, "Lucky Medallion"),
            "has_lucky_coin": _has_active_item(player, "Lucky Coin"),
            "has_invisible_cloak": _has_active_item(player, "Invisible Cloak"),
            "has_tattered_cloak": _has_active_item(player, "Tattered Cloak"),
        },
    )
    return decision == "yes"


def _auto_bet(self):
    """Route bet sizing through the structured blackjack policy."""
    bet = _choose_blackjack_bet_amount(self)
    self._Blackjack__bet = bet
    # Apply fake-cash-first mechanic: loan money is always spent before real cash.
    # Mirrors the logic in bet() so end_round() can compute the correct real_loss.
    player = self._Blackjack__player
    fake_available = player.get_fraudulent_cash()
    self._Blackjack__fraudulent_portion = 0
    if fake_available > 0:
        self._Blackjack__fraudulent_portion = min(bet, fake_available)
        player.blend_fraudulent_cash(self._Blackjack__fraudulent_portion)
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
            "has_pocket_aces": self._Blackjack__player.has_flask_effect("Pocket Aces"),
            "has_dealers_whispers": self._Blackjack__player.has_flask_effect("Dealer's Whispers"),
            "has_dealers_hesitation": self._Blackjack__player.has_flask_effect("Dealer's Hesitation"),
            "has_bonus_fortune": self._Blackjack__player.has_flask_effect("Bonus Fortune"),
            "has_split_serum": self._Blackjack__player.has_flask_effect("Split Serum"),
            "has_second_chance": self._Blackjack__player.has_flask_effect("Second Chance") and not self._Blackjack__used_second_chance,
            "has_sneaky_peeky_shades": self._Blackjack__player.has_item("Sneaky Peeky Shades"),
            "has_sneaky_peeky_goggles": self._Blackjack__player.has_item("Sneaky Peeky Goggles"),
            "has_witch_doctors_amulet": self._Blackjack__player.has_item("Witch Doctor's Amulet"),
            "has_gamblers_chalice": self._Blackjack__player.has_item("Gambler's Chalice"),
            "has_overflowing_goblet": self._Blackjack__player.has_item("Overflowing Goblet"),
            "has_twins_locket": self._Blackjack__player.has_item("Twin's Locket"),
            "has_mirror_of_duality": self._Blackjack__player.has_item("Mirror of Duality"),
            "has_white_feather": self._Blackjack__player.has_item("White Feather"),
            "has_phoenix_feather": self._Blackjack__player.has_item("Phoenix Feather"),
            "has_lucky_coin": _has_active_item(self._Blackjack__player, "Lucky Coin"),
            "has_lucky_medallion": _has_active_item(self._Blackjack__player, "Lucky Medallion"),
            "has_worn_gloves": _has_active_item(self._Blackjack__player, "Worn Gloves"),
            "has_velvet_gloves": _has_active_item(self._Blackjack__player, "Velvet Gloves"),
            "has_tattered_cloak": _has_active_item(self._Blackjack__player, "Tattered Cloak"),
            "has_invisible_cloak": _has_active_item(self._Blackjack__player, "Invisible Cloak"),
            "has_pocket_watch": _has_active_item(self._Blackjack__player, "Pocket Watch"),
            "has_golden_watch": _has_active_item(self._Blackjack__player, "Golden Watch"),
            "has_sapphire_watch": _has_active_item(self._Blackjack__player, "Sapphire Watch"),
            "has_grandfather_clock": _has_active_item(self._Blackjack__player, "Grandfather Clock"),
            "has_dealers_grudge": _has_active_item(self._Blackjack__player, "Dealer's Grudge"),
            "has_dealers_mercy": _has_active_item(self._Blackjack__player, "Dealer's Mercy"),
            "has_quiet_sneakers": _has_active_item(self._Blackjack__player, "Quiet Sneakers") or _has_active_item(self._Blackjack__player, "Quiet Bunny Slippers"),
            "has_rusty_compass": _has_active_item(self._Blackjack__player, "Rusty Compass") or _has_active_item(self._Blackjack__player, "Golden Compass"),
            "has_faulty_insurance": _has_active_item(self._Blackjack__player, "Faulty Insurance") or _has_active_item(self._Blackjack__player, "Real Insurance"),
            "has_grimoire": _has_active_item(self._Blackjack__player, "Gambler's Grimoire") or _has_active_item(self._Blackjack__player, "Oracle's Tome"),
            "has_animal_whistle": _has_active_item(self._Blackjack__player, "Animal Whistle"),
            "has_enchanting_bar": _has_active_item(self._Blackjack__player, "Enchanting Silver Bar") or _has_active_item(self._Blackjack__player, "Enchanting Gold Bar"),
            "has_dirty_hat": _has_active_item(self._Blackjack__player, "Dirty Old Hat") or _has_active_item(self._Blackjack__player, "Unwashed Hair"),
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


def _extract_hand_cards(hand):
    """Extract card strings from a Hand object."""
    cards = []
    for i in range(len(hand)):
        try:
            cards.append(str(hand.get_card(i)))
        except (IndexError, AttributeError):
            break
    return cards


def _auto_end_round(self, status):
    # Capture hand snapshot BEFORE end_round modifies anything
    _hand_snapshot = {
        "cycle": CURRENT_CYCLE,
        "bet": int(self._Blackjack__bet),
        "player_cards": _extract_hand_cards(self._Blackjack__hand),
        "dealer_cards": _extract_hand_cards(self._Blackjack__dealer_hand),
        "player_total": self._Blackjack__hand.ace_value() if self._Blackjack__hand.possible_hands() == 2 and self._Blackjack__hand.ace_value() <= 21 else self._Blackjack__hand.value(),
        "dealer_total": self._Blackjack__dealer_hand.ace_value() if self._Blackjack__dealer_hand.possible_hands() == 2 and self._Blackjack__dealer_hand.ace_value() <= 21 else self._Blackjack__dealer_hand.value(),
        "outcome": status,
        "balance_before": int(self._Blackjack__balance),
        "free_hand": bool(self._Blackjack__free_hand),
    }

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
            _hand_snapshot["second_chance"] = True
            HAND_LOG.append(_hand_snapshot)
            return False

        self._Blackjack__used_second_chance = True
        try:
            result = _ORIGINAL_END_ROUND(self, status)
        finally:
            self._Blackjack__used_second_chance = False
        _hand_snapshot["balance_after"] = int(self._Blackjack__balance)
        HAND_LOG.append(_hand_snapshot)
        return result

    result = _ORIGINAL_END_ROUND(self, status)
    _hand_snapshot["balance_after"] = int(self._Blackjack__balance)
    HAND_LOG.append(_hand_snapshot)
    return result


bj.Blackjack.bet = _auto_bet
bj.Blackjack.offer_insurance = _auto_offer_insurance
bj.Blackjack.hit_or_stand = _auto_hit_or_stand
bj.Blackjack.end_round = _auto_end_round

def _resolve_cli_args() -> tuple[int, int]:
    """Resolve quicktest CLI args.

    Supported forms:
    - quicktest.py <seed>
    - quicktest.py <cycles> <seed>  (legacy)

    When only seed is provided, cycles default to QUICKTEST_CYCLES env var
    (if set) or 300.
    """
    env_cycles = os.getenv("QUICKTEST_CYCLES")
    default_cycles = int(env_cycles) if env_cycles else 300

    if len(sys.argv) > 2:
        return int(sys.argv[1]), int(sys.argv[2])
    if len(sys.argv) > 1:
        return default_cycles, int(sys.argv[1])
    return default_cycles, 42


CYCLES, SEED = _resolve_cli_args()
LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_out.txt")
JSON_LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_out.json")
STORY_LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "story_out.txt")
DTREE_LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_decision_tree.txt")
ARTIFACT_KIND = "quicktest_report"
ARTIFACT_SCHEMA_VERSION = 2
ARTIFACT_RUN_ID = f"seed{SEED}-cycles{CYCLES}-pid{os.getpid()}-{int(time.time() * 1000)}"
LOG_TMP = f"{LOG}.tmp.{ARTIFACT_RUN_ID}"
JSON_LOG_TMP = f"{JSON_LOG}.tmp.{ARTIFACT_RUN_ID}"
STORY_LOG_TMP = f"{STORY_LOG}.tmp.{ARTIFACT_RUN_ID}"
DTREE_LOG_TMP = f"{DTREE_LOG}.tmp.{ARTIFACT_RUN_ID}"

CURRENT_CYCLE = None
CURRENT_EVENTS = []
ALL_EVENTS = []
CURRENT_CYCLE_FLOW = None
CYCLE_FLOW_REPORTS = []
RUN_PEAK_BALANCE = 50
CYCLE_SNAPSHOTS = []
HAND_LOG = []          # Each entry: {cycle, bet, player_cards, dealer_cards, player_total, dealer_total, outcome, balance_before, balance_after, items_active}
CYCLE_TEXT = {}         # cycle_number → list of text lines from that cycle
CYCLE_EVENTS = {}       # cycle_number → list of event labels from that cycle
errs = []
_ARTIFACTS_PUBLISHED = False

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
    "total_borrowed",
    "total_repaid",
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
    response = _decide_raw_input(_prompt)
    # Mirror the prompt + player response into the story log
    prompt_clean = ANSI_RE.sub("", str(_prompt)).strip()
    if prompt_clean:
        _story_file.write(prompt_clean + " ")
    _story_file.write(f"[{response}]\n")
    _story_file.flush()
    return response


_log_file = open(LOG_TMP, "w", encoding="utf-8", newline="\n")
_story_file = open(STORY_LOG_TMP, "w", encoding="utf-8", newline="\n")


def _cleanup_unpublished_artifacts():
    if not _log_file.closed:
        _log_file.close()
    if not _story_file.closed:
        _story_file.close()

    if _ARTIFACTS_PUBLISHED:
        return

    for temp_path in (LOG_TMP, STORY_LOG_TMP, JSON_LOG_TMP, DTREE_LOG_TMP):
        try:
            os.remove(temp_path)
        except FileNotFoundError:
            continue
        except OSError:
            continue


def _extract_decision_context(trace):
    """Extract meaningful game text context lines from a trace's raw_recent_text.

    Returns (prompt_text, context_lines) where:
    - prompt_text: the direct question / prompt shown to the player (if available)
    - context_lines: condensed event narrative leading up to the decision
    """
    meta = trace.metadata or {}
    raw_lines = meta.get("raw_recent_text", ())
    prompt = meta.get("raw_prompt_text", "")

    # BJ-related noise patterns to skip
    _bj_noise = {
        "your hand has a value", "the dealer's hand has a value",
        "dealer's second card", "press enter", "your balance is",
        "minimum bet is", "the dealer deals", "the dealer draws",
        "the dealer hits", "the dealer stands", "the dealer's next card",
        "the dealer's first card", "the dealer's known value", "known value of",
        "dealer's hand has a known", "your first card", "your second card",
        "your next card", "you draw", "you hit", "you stand",
        "player busts", "dealer busts", "you have a blackjack",
        "the dealer has a blackjack", "card is face down", "bet amount:",
        "your bet is", "you have $", "you had $", "your new balance",
        "new balance is", "with a bet of", "you've doubled it",
        "since they have an ace", "since you have an ace",
        "you win back your bet", "the house always wins",
        "close, but close only", "you topple the dealer", "your bet of $",
        "you lost your bet", "dealer hand goes bust", "you simply got outplayed",
        "is a draw", "one lucky lucy", "witnessing a heist", "beginner's luck!",
        "the cards shift", "the dealer points to the door",
        "without questioning his word", "making it back to your car",
        "eager to get some sleep", "you scurry to the door",
        "sit. let's see what fate", "you keep coming back",
        "walk to the casino", "eager to play more blackjack",
        "as the sun begins to set", "day summary", "you've survived",
        "you started your journey", "since then, you've managed",
        "that brings you to a grand total", "let's not get too far ahead",
        "you've got a unique path", "here's a little bit of inspiration",
        "~ ~ ~ morning", "~ ~ ~ day", "you slept",
    }
    _decorative = {"══════════", "──────────", "==========", "----------",
                   "yippee!", "yessir!", "nice!", "impressive!"}

    context_lines = []
    for raw in raw_lines:
        line = str(raw).strip()
        if not line or len(line) <= 3:
            continue
        lower = line.lower()
        if any(pat in lower for pat in _bj_noise):
            continue
        if line in _decorative:
            continue
        if lower in _decorative:
            continue
        # Skip quoted inspirational lines
        if line.startswith('"') and line.endswith('"') and len(line) > 40:
            continue
        context_lines.append(line)

    return prompt.strip(), context_lines


def _write_decision_tree():
    """Write a comprehensive decision tree showing every hand, event, and decision."""

    # ── Index all data by cycle ──────────────────────────────────────────────
    traces_by_cycle = defaultdict(list)
    for trace in DECISION_TRACES:
        traces_by_cycle[trace.cycle or 0].append(trace)

    snapshots_by_cycle = {}
    for cycle_num, before, after in CYCLE_SNAPSHOTS:
        snapshots_by_cycle[cycle_num] = (before, after)

    flows_by_cycle = {}
    for flow in CYCLE_FLOW_REPORTS:
        flows_by_cycle[int(flow.get("cycle", 0))] = flow

    hands_by_cycle = defaultdict(list)
    for hand in HAND_LOG:
        hands_by_cycle[hand.get("cycle") or 0].append(hand)

    all_cycles = sorted(
        set(traces_by_cycle.keys())
        | set(snapshots_by_cycle.keys())
    )

    lines = []
    w = lines.append

    w("╔" + "═" * 98 + "╗")
    w("║" + f" DECISION TREE — seed={SEED}  cycles={CYCLES}".ljust(98) + "║")
    w("║" + f" Generated {time.strftime('%Y-%m-%d %H:%M:%S')}".ljust(98) + "║")
    w("╚" + "═" * 98 + "╝")
    w("")

    # ── Accumulators ─────────────────────────────────────────────────────────
    missed_marvin_cycles = []
    total_damage_events = 0
    total_hands = 0
    total_wins = 0
    total_losses = 0
    total_ties = 0
    total_bet_amount = 0
    total_won_amount = 0
    total_lost_amount = 0
    low_confidence_decisions = []
    turning_points = []
    unhandled_events = []  # events with no traced decisions
    all_event_labels = []

    for cycle_num in all_cycles:
        if cycle_num == 0:
            pre_traces = traces_by_cycle.get(0, [])
            if pre_traces:
                w("┌" + "─" * 98 + "┐")
                w("│ PRE-GAME SETUP" + " " * 83 + "│")
                w("└" + "─" * 98 + "┘")
                for trace in pre_traces:
                    ctx = trace.context or trace.request_type or "?"
                    action = trace.chosen_action or "?"
                    reason = trace.reason or ""
                    w(f"  {ctx}: {action} | {reason[:80]}")
                w("")
            continue

        before, after = snapshots_by_cycle.get(cycle_num, ({}, {}))
        b_bal = int(before.get("balance", 0))
        a_bal = int(after.get("balance", 0))
        b_hp = int(before.get("health", 0))
        a_hp = int(after.get("health", 0))
        b_san = int(before.get("sanity", 0))
        a_san = int(after.get("sanity", 0))
        rank = int(after.get("rank", before.get("rank", 0)))
        has_car = "Y" if after.get("has_car") else "N"
        day = int(after.get("day", before.get("day", cycle_num)))
        alive = after.get("alive", True)
        d_bal = a_bal - b_bal
        d_hp = a_hp - b_hp
        d_san = a_san - b_san

        # Status flags
        flags = []
        if d_hp < -10 or d_san < -10:
            flags.append("DAMAGE")
        if not alive:
            flags.append("DEATH")
        if d_bal < -500:
            flags.append("BIG LOSS")
        if d_bal > 2000:
            flags.append("BIG WIN")
        flag_str = "  ◄ " + ", ".join(flags) if flags else ""

        # ── Day header ───────────────────────────────────────────────────────
        w("╔" + "═" * 98 + "╗")
        header = f" Day {day:3d} | ${b_bal:>8,} → ${a_bal:>8,} ({d_bal:+,}) | HP:{b_hp}→{a_hp}({d_hp:+d}) SAN:{b_san}→{a_san}({d_san:+d}) | R:{rank} Car:{has_car}{flag_str}"
        w("║" + header.ljust(98) + "║")
        w("╚" + "═" * 98 + "╝")

        # ── Events that fired this cycle (enriched with narrative + decisions) ─
        events = CYCLE_EVENTS.get(cycle_num, [])
        if events:
            all_event_labels.extend(events)

        # Group event-type AND location-type traces by their event label
        _event_decision_types = frozenset(("event_branch", "event_inline", "yes_no"))
        _location_trace_types = frozenset((
            "purchase_select", "loan_decision", "repair_select",
            "upgrade_select", "medical_select", "menu_select",
        ))
        # Map location trace context IDs → location event labels
        _ctx_to_location = {
            "convenience_store_menu": "location:shop:convenience_store",
            "loan_menu": "location:shop:loan_shark",
            "loan_borrow_amount": "location:shop:loan_shark",
            "loan_repay_amount": "location:shop:loan_shark",
            "repair_menu": "location:shop:tom",
            "upgrade_menu": "location:shop:tom",
            "workbench_menu": "location:workbench",
            "workbench_craft_menu": "location:workbench",
            "pawn_menu": "location:shop:pawn",
            "pawn_sale_menu": "location:shop:pawn",
            "witch_flask_menu": "location:doctor:witch",
            "medical_destination": "location:doctor",
            "companion_menu": "location:companion",
        }
        cycle_traces_all = traces_by_cycle.get(cycle_num, [])
        non_bj_traces_pre = [t for t in cycle_traces_all if t.request_type not in ("blackjack_bet", "blackjack_action")]
        event_trace_map: dict[str, list] = {}  # event_label → list of traces
        other_traces: list = []  # non-event traces (routes, insurance, etc.)
        for t in non_bj_traces_pre:
            if t.request_type in _event_decision_types:
                key = t.context or "unknown_event"
                event_trace_map.setdefault(key, []).append(t)
            elif t.request_type in _location_trace_types:
                ctx = t.context or ""
                # Try exact match first, then prefix match against event labels
                loc_label = _ctx_to_location.get(ctx)
                if loc_label is None:
                    # Fuzzy: check if any location event in this cycle matches
                    for ev in events:
                        if ev.startswith("location:") and any(
                            part in ctx for part in ev.split(":")[1:]
                        ):
                            loc_label = ev
                            break
                if loc_label:
                    event_trace_map.setdefault(loc_label, []).append(t)
                else:
                    other_traces.append(t)
            else:
                other_traces.append(t)

        if events or event_trace_map:
            w("  ┌─ EVENTS ─────────────────────────────────────")
            # Merge: show all events from CYCLE_EVENTS + any that only appear in traces
            seen_labels = set()
            all_labels = list(events)
            for k in event_trace_map:
                if k not in all_labels:
                    all_labels.append(k)

            for ev in all_labels:
                seen_labels.add(ev)
                ev_traces = event_trace_map.get(ev, [])
                w(f"  │ ▸ {ev}")

                # Extract narrative context from the first trace for this event
                if ev_traces:
                    prompt_text, ctx_lines = _extract_decision_context(ev_traces[0])
                    # Show up to 5 key narrative lines
                    for cl in ctx_lines[-5:]:
                        w(f"  │   {cl[:110]}")
                    if prompt_text and prompt_text not in [cl[:110] for cl in ctx_lines[-5:]]:
                        w(f"  │   ? {prompt_text[:110]}")

                # Show decisions made during this event
                for tr in ev_traces:
                    action = tr.chosen_action or "?"
                    reason = tr.reason or ""
                    opts = tr.options or ()
                    meta = tr.metadata or {}
                    reason_code = meta.get("reason_code", "")
                    conf = tr.confidence if tr.confidence is not None else -1.0
                    if conf < 0 or conf >= 0.90:
                        conf_tag = ""
                    elif conf >= 0.70:
                        conf_tag = f" [conf={conf:.2f}]"
                    elif conf >= 0.50:
                        conf_tag = f" ◄ UNCERTAIN conf={conf:.2f}"
                    else:
                        conf_tag = f" ◄◄ GUESSING conf={conf:.2f}"

                    if tr.request_type == "yes_no":
                        reason_short = reason[:80] if reason else ""
                        w(f"  │   → Y/N: {action} | {reason_short}{conf_tag}")
                    elif tr.request_type == "event_branch":
                        alt_opts = [str(o) for o in opts[:6] if str(o) != str(action)]
                        w(f"  │   → chose '{action}' [{reason_code}]{conf_tag}")
                        if alt_opts:
                            w(f"  │     (other: {', '.join(alt_opts)})")
                    elif tr.request_type == "event_inline":
                        alt_opts = [str(o) for o in opts[:6] if str(o) != str(action)]
                        w(f"  │   → '{action}' [{reason_code}]{conf_tag}")
                        if alt_opts:
                            w(f"  │     (other: {', '.join(alt_opts)})")
                    elif tr.request_type == "purchase_select":
                        alt_opts = [str(o) for o in opts[:8] if str(o) != str(action)]
                        w(f"  │   → PURCHASE: {action} [{reason_code}]{conf_tag}")
                        if alt_opts:
                            w(f"  │     (other: {', '.join(alt_opts)})")
                    elif tr.request_type == "loan_decision":
                        w(f"  │   → LOAN: {action} [{reason_code}]{conf_tag}")
                    elif tr.request_type == "repair_select":
                        w(f"  │   → REPAIR: {action} [{reason_code}]{conf_tag}")
                    elif tr.request_type == "upgrade_select":
                        w(f"  │   → UPGRADE: {action} [{reason_code}]{conf_tag}")
                    elif tr.request_type == "medical_select":
                        w(f"  │   → MEDICAL: {action} [{reason_code}]{conf_tag}")
                    elif tr.request_type == "menu_select":
                        w(f"  │   → MENU: {action} [{reason_code}]{conf_tag}")
                    else:
                        w(f"  │   → {action} [{reason_code}]{conf_tag}")

                    # Track low-confidence
                    if 0 <= conf < 0.50:
                        low_confidence_decisions.append((
                            cycle_num, day, tr.request_type or ev, action, conf,
                            reason_code or reason[:40], list(opts[:6])
                        ))
                if ev != all_labels[-1]:
                    w("  │")
            w("  └──────────────────────────────────────────────")

        # ── Afternoon route (from flow report) ───────────────────────────────
        flow = flows_by_cycle.get(cycle_num, {})
        if flow.get("afternoon_menu_presented"):
            menu_opts = flow.get("menu_options", [])
            route_choice = flow.get("route_choice")
            menu_labels = list(menu_opts) if menu_opts else []
            if menu_labels:
                chosen_str = route_choice or "none"
                other_opts = [lbl for lbl in menu_labels if lbl != chosen_str]
                w(f"  ROUTE    chose: {chosen_str}")
                if other_opts:
                    w(f"           avail: {', '.join(other_opts)}")
                if "Marvin's Mystical Merchandise" in menu_labels and route_choice != "Marvin's Mystical Merchandise":
                    missed_marvin_cycles.append(cycle_num)
                    w(f"           ⚠ MARVIN AVAILABLE BUT NOT VISITED")

        # ── Blackjack hands ──────────────────────────────────────────────────
        cycle_hands = hands_by_cycle.get(cycle_num, [])
        # Get bet/action traces for this cycle
        cycle_traces = traces_by_cycle.get(cycle_num, [])
        bet_traces = [t for t in cycle_traces if t.request_type == "blackjack_bet"]
        action_traces = [t for t in cycle_traces if t.request_type == "blackjack_action"]
        non_bj_traces = [t for t in cycle_traces if t.request_type not in ("blackjack_bet", "blackjack_action")]

        if cycle_hands:
            w("")
            w(f"  ┌─ BLACKJACK SESSION ({len(cycle_hands)} hand{'s' if len(cycle_hands) != 1 else ''}) ─────────────")

            # Match each hand with its corresponding bet trace
            action_idx = 0
            for h_idx, hand in enumerate(cycle_hands):
                total_hands += 1
                outcome = hand["outcome"]
                bet = hand["bet"]
                p_cards = hand["player_cards"]
                d_cards = hand["dealer_cards"]
                p_total = hand["player_total"]
                d_total = hand["dealer_total"]
                bal_before = hand["balance_before"]
                bal_after = hand.get("balance_after", bal_before)
                free = hand.get("free_hand", False)
                second_chance = hand.get("second_chance", False)
                delta = bal_after - bal_before

                # Classify outcome
                is_win = outcome in ("Player Blackjack", "Player Wins", "Dealer Bust")
                is_loss = outcome in ("Dealer Blackjack", "Dealer Wins", "Player Bust")
                is_tie = outcome in ("Tie", "Tie Blackjack")

                if is_win:
                    total_wins += 1
                    total_won_amount += abs(delta)
                    result_marker = "  ✓ WIN"
                elif is_loss:
                    total_losses += 1
                    total_lost_amount += abs(delta)
                    result_marker = "  ✗ LOSS"
                else:
                    total_ties += 1
                    result_marker = "  = TIE"
                total_bet_amount += bet

                if second_chance:
                    result_marker += " (2nd Chance → replayed)"

                # Show the bet decision
                bet_reason = ""
                if h_idx < len(bet_traces):
                    bt = bet_traces[h_idx]
                    bt_meta = bt.metadata or {}
                    bet_reason = bt_meta.get("reason_code", "")
                    edge = int(bt_meta.get("edge_score", 0))
                    bet_reason = f"[{bet_reason}] edge={edge}"

                w(f"  │")
                w(f"  │ Hand {h_idx + 1}: Bet ${bet:,} / ${bal_before:,} {bet_reason}")
                w(f"  │   Player: {', '.join(p_cards):40s} = {p_total}")
                w(f"  │   Dealer: {', '.join(d_cards):40s} = {d_total}")
                w(f"  │   Result: {outcome:20s} {delta:+,}{' (free hand)' if free else ''}{result_marker}")

                # Show hit/stand/double/split decisions for this hand
                # Count action traces that belong to this hand
                hand_actions = []
                while action_idx < len(action_traces):
                    at = action_traces[action_idx]
                    hand_actions.append(at)
                    action_idx += 1
                    # If the action was "stand", "double", or "surrender", the hand is over
                    if at.chosen_action in ("stand", "double", "surrender"):
                        break
                    # If we've consumed more actions than cards drawn, stop
                    if len(hand_actions) >= len(p_cards):
                        break

                if hand_actions:
                    action_strs = []
                    for at in hand_actions:
                        at_meta = at.metadata or {}
                        candidates = at_meta.get("candidate_actions", [])
                        alt_list = [f"{c.get('option_id','?')}:{c.get('score',0):.0f}" for c in candidates if str(c.get('option_id','')) != str(at.chosen_action)] if candidates else []
                        alts = f"(vs {','.join(alt_list)})" if alt_list else ""
                        action_strs.append(f"{at.chosen_action} {alts}".strip())
                    w(f"  │   Actions: {' → '.join(action_strs)}")

            session_delta = sum(
                (h.get("balance_after", h["balance_before"]) - h["balance_before"])
                for h in cycle_hands if not h.get("second_chance")
            )
            w(f"  │")
            w(f"  └─ Session: {len(cycle_hands)} hands, net {session_delta:+,}")
            w("")

        # ── Non-event decisions (routes, purchases, loans, insurance, etc.) ──
        if other_traces:
            for trace in other_traces:
                ctx = trace.context or trace.request_type or "?"
                action = trace.chosen_action or "?"
                reason = trace.reason or ""
                opts = trace.options or ()
                meta = trace.metadata or {}
                reason_code = meta.get("reason_code", "")
                conf = trace.confidence if trace.confidence is not None else -1.0

                # Confidence grade
                if conf < 0 or conf >= 0.90:
                    conf_tag = ""
                elif conf >= 0.70:
                    conf_tag = f" [conf={conf:.2f}]"
                elif conf >= 0.50:
                    conf_tag = f" ◄ UNCERTAIN conf={conf:.2f}"
                else:
                    conf_tag = f" ◄◄ GUESSING conf={conf:.2f}"

                if ctx == "afternoon_destination" or trace.request_type == "route_select":
                    goal = trace.strategic_goal or "?"
                    alt_opts = [str(o) for o in opts if str(o) != str(action)]
                    w(f"  ROUTE    → {action}")
                    w(f"             goal={goal}  conf={conf:.2f}  [{reason_code}]")
                    if alt_opts:
                        w(f"             rejected: {', '.join(alt_opts)}")

                elif "purchase" in ctx or trace.request_type == "purchase_select":
                    alt_opts = [str(o) for o in opts[:8] if str(o) != str(action)]
                    w(f"  PURCHASE → {action} [{reason_code}]{conf_tag}")
                    if alt_opts:
                        w(f"             other items: {', '.join(alt_opts)}")

                elif trace.request_type == "upgrade_select":
                    w(f"  UPGRADE  → {action} [{reason_code}]{conf_tag}")

                elif trace.request_type == "repair_select":
                    w(f"  REPAIR   → {action} [{reason_code}]{conf_tag}")

                elif "loan" in ctx or trace.request_type == "loan_decision":
                    w(f"  LOAN     → {action} [{reason_code}]{conf_tag}")

                elif trace.request_type == "menu_select" or trace.request_type == "medical_select":
                    label = "MEDICAL" if trace.request_type == "medical_select" else "MENU"
                    w(f"  {label:8s} → {action} [{reason_code}] opts={','.join(str(o) for o in opts[:6])}{conf_tag}")

                elif trace.request_type in ("insurance_decision",):
                    w(f"  INSURE   → {action} [{reason_code}]{conf_tag}")

                elif trace.request_type in ("second_chance_decision",):
                    w(f"  2ndCHANC → {action} [{reason_code}]{conf_tag}")

                else:
                    reason_short = reason[:60] if reason else ""
                    w(f"  DECIDE   {ctx}: {action} | {reason_short}{conf_tag}")

                # Track low-confidence
                if 0 <= conf < 0.50:
                    low_confidence_decisions.append((
                        cycle_num, day, trace.request_type or ctx, action, conf,
                        reason_code or reason[:40], list(opts[:6])
                    ))

        # ── State changes ────────────────────────────────────────────────────
        inv_before = set(before.get("inventory", set()))
        inv_after = set(after.get("inventory", set()))
        added = inv_after - inv_before
        removed = inv_before - inv_after
        if added:
            w(f"  +ITEM  {', '.join(sorted(added))}")
        if removed:
            w(f"  -ITEM  {', '.join(sorted(removed))}")

        comp_before = set(before.get("companions", set()))
        comp_after = set(after.get("companions", set()))
        comp_added = comp_after - comp_before
        comp_removed = comp_before - comp_after
        if comp_added:
            w(f"  +COMP  {', '.join(sorted(comp_added))}")
        if comp_removed:
            w(f"  -COMP  {', '.join(sorted(comp_removed))}")

        inj_before = set(before.get("injuries", set()))
        inj_after = set(after.get("injuries", set()))
        inj_added = inj_after - inj_before
        inj_removed = inj_before - inj_after
        if inj_added:
            w(f"  +INJ   {', '.join(sorted(inj_added))}")
            total_damage_events += 1
        if inj_removed:
            w(f"  -INJ   {', '.join(sorted(inj_removed))}")

        stat_before = set(before.get("statuses", set()))
        stat_after = set(after.get("statuses", set()))
        stat_added = stat_after - stat_before
        stat_removed = stat_before - stat_after
        if stat_added:
            w(f"  +STAT  {', '.join(sorted(stat_added))}")
        if stat_removed:
            w(f"  -STAT  {', '.join(sorted(stat_removed))}")

        story_before = set(before.get("active_storylines", set()))
        story_after = set(after.get("active_storylines", set()))
        story_added = story_after - story_before
        if story_added:
            w(f"  +STORY {', '.join(sorted(story_added))}")

        broken_before = set(before.get("broken_items", set()))
        broken_after = set(after.get("broken_items", set()))
        broken_added = broken_after - broken_before
        if broken_added:
            w(f"  BROKE  {', '.join(sorted(broken_added))}")

        # Check for events that had NO traced decisions (pure RNG events)
        if events and not non_bj_traces:
            for ev in events:
                if not ev.startswith("location:") and not ev.startswith("met:"):
                    unhandled_events.append((day, ev, d_bal, d_hp, d_san))

        # Death
        if not alive:
            death = after.get("death_cause") or before.get("death_cause") or "Unknown"
            w(f"  ╔══════════════════════════════════════════════")
            w(f"  ║ ☠ DIED: {death}")
            w(f"  ╚══════════════════════════════════════════════")
            turning_points.append((day, d_bal, b_bal, a_bal, death))
        elif abs(d_bal) >= 2000 or d_hp <= -20 or d_san <= -20:
            turning_points.append((day, d_bal, b_bal, a_bal, None))

        w("")

    # ══════════════════════════════════════════════════════════════════════════
    # SUMMARY
    # ══════════════════════════════════════════════════════════════════════════
    w("╔" + "═" * 98 + "╗")
    w("║" + " DECISION TREE SUMMARY".ljust(98) + "║")
    w("╚" + "═" * 98 + "╝")
    w("")

    final = snapshots_by_cycle.get(all_cycles[-1], ({}, {})) if all_cycles else ({}, {})
    final_after = final[1] if final else {}
    w(f"  Final State:")
    w(f"    Balance: ${int(final_after.get('balance', 0)):,}  |  HP: {int(final_after.get('health', 0))}  |  SAN: {int(final_after.get('sanity', 0))}  |  Rank: {int(final_after.get('rank', 0))}")
    w(f"    Peak balance: ${RUN_PEAK_BALANCE:,}")
    w(f"    Days survived: {int(final_after.get('day', 0))}")
    w(f"    Total decisions traced: {len(DECISION_TRACES)}")
    w("")

    # ── Blackjack Statistics ─────────────────────────────────────────────────
    w("  Blackjack Statistics:")
    w(f"    Hands played: {total_hands}  |  Won: {total_wins}  |  Lost: {total_losses}  |  Tied: {total_ties}")
    win_rate = f"{total_wins / total_hands * 100:.1f}%" if total_hands else "N/A"
    w(f"    Win rate: {win_rate}")
    w(f"    Total wagered: ${total_bet_amount:,}")
    w(f"    Total won: ${total_won_amount:,}  |  Total lost: ${total_lost_amount:,}  |  Net: ${total_won_amount - total_lost_amount:+,}")
    avg_bet = total_bet_amount // total_hands if total_hands else 0
    w(f"    Average bet: ${avg_bet:,}")
    w("")

    # ── Event Statistics ─────────────────────────────────────────────────────
    event_counts = Counter(all_event_labels)
    day_events = [(ev, c) for ev, c in event_counts.most_common() if ev.startswith("day:")]
    night_events = [(ev, c) for ev, c in event_counts.most_common() if ev.startswith("night:")]
    location_events = [(ev, c) for ev, c in event_counts.most_common() if ev.startswith("location:")]
    meet_events = [(ev, c) for ev, c in event_counts.most_common() if ev.startswith("met:")]
    storyline_events = [(ev, c) for ev, c in event_counts.most_common() if ev.startswith("storyline:")]

    w(f"  Events ({len(all_event_labels)} total, {len(event_counts)} unique):")
    if day_events:
        w(f"    Day events ({len(day_events)}):")
        for ev, c in day_events[:30]:
            w(f"      {ev:55s} ×{c}")
    if night_events:
        w(f"    Night events ({len(night_events)}):")
        for ev, c in night_events[:20]:
            w(f"      {ev:55s} ×{c}")
    if location_events:
        w(f"    Location visits ({len(location_events)}):")
        for ev, c in location_events:
            w(f"      {ev:55s} ×{c}")
    if meet_events:
        w(f"    People met ({len(meet_events)}):")
        for ev, c in meet_events:
            w(f"      {ev:55s} ×{c}")
    if storyline_events:
        w(f"    Storylines ({len(storyline_events)}):")
        for ev, c in storyline_events:
            w(f"      {ev:55s} ×{c}")
    w("")

    # ── Damage events: random events with no decisions ───────────────────────
    if unhandled_events:
        w(f"  Pure RNG Events (no player decision, {len(unhandled_events)} total):")
        for _day, _ev, _dbal, _dhp, _dsan in sorted(unhandled_events, key=lambda x: x[2]):
            impact = []
            if _dbal:
                impact.append(f"${_dbal:+,}")
            if _dhp:
                impact.append(f"HP:{_dhp:+d}")
            if _dsan:
                impact.append(f"SAN:{_dsan:+d}")
            impact_str = " | ".join(impact) if impact else "no impact"
            w(f"    Day {_day:3d} | {_ev:40s} | {impact_str}")
        w("")

    # ── Reason Code Distribution ─────────────────────────────────────────────
    reason_codes = Counter()
    for trace in DECISION_TRACES:
        rc = (trace.metadata or {}).get("reason_code", "")
        if rc:
            reason_codes[rc] += 1
    w("  Bet/Action Reason Codes:")
    for rc, count in reason_codes.most_common(30):
        w(f"    {rc:50s} {count:5d}")
    w("")

    # ── Missed Marvin ────────────────────────────────────────────────────────
    w(f"  Marvin Opportunities: {len(missed_marvin_cycles)} missed")
    if missed_marvin_cycles:
        for mc in missed_marvin_cycles:
            snap = snapshots_by_cycle.get(mc, ({}, {}))
            b = snap[0]
            flow = flows_by_cycle.get(mc, {})
            route = flow.get("route_choice", "?")
            w(f"    Day {int(b.get('day', mc)):3d} | ${int(b.get('balance', 0)):>8,} | Chose: {route}")
    w("")

    # ── Low-confidence decisions ─────────────────────────────────────────────
    w(f"  Low Confidence Decisions ({len(low_confidence_decisions)}, conf < 0.50 = bot was guessing):")
    if low_confidence_decisions:
        for _cyc, _day, _type, _act, _conf, _reason, _opts in sorted(low_confidence_decisions, key=lambda x: x[4]):
            alt_str = f" alts=[{','.join(str(o) for o in _opts if str(o) != str(_act))}]" if _opts else ""
            w(f"    Day {_day:3d} | {_type:20s} → {str(_act):15s} conf={_conf:.2f} | {_reason}{alt_str}")
    w("")

    # ── Critical turning points ──────────────────────────────────────────────
    w(f"  Critical Turning Points ({len(turning_points)}, balance swing ≥$2k or severe injury):")
    if turning_points:
        for _day, _dbal, _bbal, _abal, _death in sorted(turning_points, key=lambda x: x[1]):
            if _death:
                w(f"    Day {_day:3d} | ${_bbal:>8,} → ${_abal:>8,} ({_dbal:+,}) ☠ {_death[:80]}")
            else:
                w(f"    Day {_day:3d} | ${_bbal:>8,} → ${_abal:>8,} ({_dbal:+,})")
    w("")

    # Write to file
    with open(DTREE_LOG_TMP, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines))
        f.write("\n")
        f.flush()
        try:
            os.fsync(f.fileno())
        except OSError:
            pass


def _write_json_artifact(payload):
    with open(JSON_LOG_TMP, "w", encoding="utf-8", newline="\n") as json_handle:
        json.dump(payload, json_handle, indent=2, sort_keys=True)
        json_handle.write("\n")
        json_handle.flush()
        try:
            os.fsync(json_handle.fileno())
        except OSError:
            pass


def _publish_artifacts():
    global _ARTIFACTS_PUBLISHED
    if _ARTIFACTS_PUBLISHED:
        return

    if not _log_file.closed:
        _log_file.close()
    if not _story_file.closed:
        _story_file.close()

    os.replace(LOG_TMP, LOG)
    os.replace(STORY_LOG_TMP, STORY_LOG)
    os.replace(JSON_LOG_TMP, JSON_LOG)
    if os.path.exists(DTREE_LOG_TMP):
        os.replace(DTREE_LOG_TMP, DTREE_LOG)
    _ARTIFACTS_PUBLISHED = True


atexit.register(_cleanup_unpublished_artifacts)


def log(message=""):
    _log_file.write(str(message) + "\n")
    _log_file.flush()


def record_event(kind, name):
    if CURRENT_CYCLE is None:
        return
    label = f"{kind}:{name}"
    CURRENT_EVENTS.append(label)
    ALL_EVENTS.append((CURRENT_CYCLE, kind, name))


def _new_cycle_flow(player=None):
    day = None
    if player is not None:
        day = int(getattr(player, "_day", 0) or 0)
    return {
        "cycle": CURRENT_CYCLE,
        "day": day,
        "afternoon_menu_presented": False,
        "menu_kind": None,
        "menu_options": [],
        "route_choice": None,
        "route_choice_number": None,
        "route_choice_reason": None,
        "route_choice_confidence": None,
        "route_outcome": None,
        "night_handoff": None,
        "night_caller": None,
        "night_mode": None,
    }


def _ensure_cycle_flow(player=None):
    global CURRENT_CYCLE_FLOW
    if CURRENT_CYCLE is None:
        return None
    if CURRENT_CYCLE_FLOW is None or CURRENT_CYCLE_FLOW.get("cycle") != CURRENT_CYCLE:
        CURRENT_CYCLE_FLOW = _new_cycle_flow(player)
    elif player is not None and CURRENT_CYCLE_FLOW.get("day") is None:
        CURRENT_CYCLE_FLOW["day"] = int(getattr(player, "_day", 0) or 0)
    return CURRENT_CYCLE_FLOW


def _latest_cycle_route_trace():
    for trace in reversed(DECISION_TRACES):
        if trace.request_type == "route_select" and trace.cycle == CURRENT_CYCLE:
            return trace
    return None


def _mark_afternoon_menu_presented(player, menu_options, menu_kind="afternoon_destination"):
    flow = _ensure_cycle_flow(player)
    if flow is None:
        return
    flow["afternoon_menu_presented"] = True
    flow["menu_kind"] = str(menu_kind)
    flow["menu_options"] = [str(label) for _number, label in menu_options]


def _record_route_choice_flow(player, chosen_number, menu_options, menu_kind="afternoon_destination"):
    flow = _ensure_cycle_flow(player)
    if flow is None:
        return chosen_number
    _mark_afternoon_menu_presented(player, menu_options, menu_kind=menu_kind)
    choice_label = next((label for number, label in menu_options if number == chosen_number), str(chosen_number))
    flow["route_choice_number"] = int(chosen_number)
    flow["route_choice"] = str(choice_label)
    trace = _latest_cycle_route_trace()
    if trace is not None:
        trace_number = str(trace.chosen_action or "")
        trace_label = str(trace.metadata.get("chosen_label", "") or "")
        if trace_number == str(chosen_number) or trace_label == str(choice_label):
            flow["route_choice_reason"] = str(trace.reason or "") or None
            flow["route_choice_confidence"] = float(trace.confidence)
            flow["route_outcome"] = str(trace.metadata.get("route_outcome", "") or "") or None
    return chosen_number


def _recent_text_contains(*phrases):
    recent_text = "\n".join(RECENT_TEXT[-20:]).lower()
    return any(str(phrase).lower() in recent_text for phrase in phrases)


def _latest_cycle_event_label(prefix=None):
    for label in reversed(CURRENT_EVENTS):
        if prefix is None or label.startswith(prefix):
            return label
    return None


def _latest_non_night_event_label():
    for prefix in ("location:", "storyline:", "day:", "met:"):
        label = _latest_cycle_event_label(prefix)
        if label is not None:
            return label
    return None


def _classify_night_handoff(player, caller_name):
    flow = _ensure_cycle_flow(player)
    if flow is None:
        return None
    route_choice = flow.get("route_choice")
    if route_choice:
        if caller_name == "night_event":
            night_label = _latest_cycle_event_label("night:")
            if night_label:
                return f"after route {route_choice} -> {night_label}"
        return f"after route {route_choice}"

    if caller_name == "night_event":
        night_label = _latest_cycle_event_label("night:")
        if night_label:
            return f"night event handoff via {night_label}"
        return "night event handoff"

    if _recent_text_contains(
        "you lose the afternoon to car trouble and head straight to the casino at dusk",
        "your car trouble eats up the whole afternoon",
        "hoping for better luck at the tables than you had with your car",
    ):
        return "afternoon skipped by car trouble"

    if caller_name == "afternoon":
        event_label = _latest_non_night_event_label()
        if event_label:
            return f"afternoon auto-handoff after {event_label}"
        return "afternoon auto-handoff"

    if caller_name.startswith("visit_"):
        return f"after {caller_name[6:].replace('_', ' ')}"

    if "adventure" in caller_name:
        return f"after {caller_name.replace('_', ' ')}"

    return f"via {caller_name}"


def _format_cycle_flow(flow):
    if not flow:
        return "untracked"
    parts = [f"menu={'shown' if flow.get('afternoon_menu_presented') else 'skipped'}"]
    route_choice = flow.get("route_choice")
    if route_choice:
        route_text = str(route_choice)
        route_outcome = flow.get("route_outcome")
        if route_outcome:
            route_text += f" ({route_outcome})"
        parts.append(f"route={route_text}")
    else:
        parts.append("route=none")
    parts.append(f"handoff={flow.get('night_handoff') or 'unknown'}")
    if flow.get("night_mode"):
        parts.append(f"night={flow['night_mode']}")
    return " | ".join(parts)


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


def _wrap_dealer_systems():
    original_deliver_gift = getattr(story.Player, "deliver_gift_to_dealer", None)
    if original_deliver_gift is not None:
        def wrapped_deliver_gift(self, *args, **kwargs):
            gift_name = None
            if hasattr(self, "get_wrapped_gift"):
                gift_name = self.get_wrapped_gift()
            before_happiness = int(self.get_dealer_happiness()) if hasattr(self, "get_dealer_happiness") else None
            day = getattr(self, "_day", None)
            cycle = CURRENT_CYCLE
            result = original_deliver_gift(self, *args, **kwargs)
            after_happiness = int(self.get_dealer_happiness()) if hasattr(self, "get_dealer_happiness") else before_happiness
            GIFT_DELIVERIES.append({
                "day": None if day is None else int(day),
                "cycle": cycle,
                "item": None if gift_name is None else str(gift_name),
                "happiness_before": before_happiness,
                "happiness_after": after_happiness,
                "happiness_change": None if before_happiness is None or after_happiness is None else after_happiness - before_happiness,
                "alive_after": bool(getattr(self, "_alive", True)),
            })
            return result
        setattr(story.Player, "deliver_gift_to_dealer", wrapped_deliver_gift)

    original_dealer_status = getattr(bj.Blackjack, "dealer_status", None)
    if original_dealer_status is not None:
        def wrapped_dealer_status(self, *args, **kwargs):
            result = original_dealer_status(self, *args, **kwargs)
            free_hand = bool(getattr(self, "_Blackjack__free_hand", False))
            if free_hand:
                player = getattr(self, "_Blackjack__player", None)
                happiness = int(getattr(self, "_Blackjack__dealer_happiness", 0) or 0)
                if happiness == 100:
                    tier = "100"
                elif happiness > 95:
                    tier = ">95"
                else:
                    tier = ">90"
                DEALER_FREE_HANDS.append({
                    "day": None if player is None else int(getattr(player, "_day", 0) or 0),
                    "cycle": CURRENT_CYCLE,
                    "dealer_happiness": happiness,
                    "bet": int(getattr(self, "_Blackjack__bet", 0) or 0),
                    "balance": int(getattr(self, "_Blackjack__balance", 0) or 0),
                    "tier": tier,
                })
            return result
        setattr(bj.Blackjack, "dealer_status", wrapped_dealer_status)


def _wrap_afternoon_night_flow():
    original_afternoon = getattr(story.Player, "afternoon", None)
    if original_afternoon is not None:
        def wrapped_afternoon(self, *args, **kwargs):
            if CURRENT_CYCLE is not None:
                _ensure_cycle_flow(self)
            result = original_afternoon(self, *args, **kwargs)
            if CURRENT_CYCLE is not None:
                flow = _ensure_cycle_flow(self)
                if flow is not None:
                    if flow.get("night_handoff") is None:
                        flow["night_caller"] = "afternoon"
                        flow["night_handoff"] = _classify_night_handoff(self, "afternoon")
                    if flow.get("night_mode") is None:
                        flow["night_mode"] = "drive" if self.has_item("Car") else "walk"
            return result

        setattr(story.Player, "afternoon", wrapped_afternoon)

    original_start_night = getattr(story.Player, "start_night", None)
    if original_start_night is not None:
        def wrapped_start_night(self, *args, **kwargs):
            if CURRENT_CYCLE is not None:
                flow = _ensure_cycle_flow(self)
                caller = inspect.currentframe().f_back.f_code.co_name
                if flow is not None:
                    flow["night_caller"] = caller
                    if flow.get("night_handoff") is None:
                        flow["night_handoff"] = _classify_night_handoff(self, caller)
            return original_start_night(self, *args, **kwargs)

        setattr(story.Player, "start_night", wrapped_start_night)

    for method_name, mode in [
        ("start_night_1", "intro"),
        ("start_night_car", "walk"),
        ("start_night_car_fixed", "drive"),
        ("start_night_tanya_skip", "skip"),
        ("start_night_motel_strip", "motel_strip"),
    ]:
        original = getattr(story.Player, method_name, None)
        if original is None:
            continue

        def make_wrapper(fn, night_mode):
            def wrapped(self, *args, **kwargs):
                if CURRENT_CYCLE is not None:
                    flow = _ensure_cycle_flow(self)
                    if flow is not None:
                        flow["night_mode"] = night_mode
                return fn(self, *args, **kwargs)

            return wrapped

        setattr(story.Player, method_name, make_wrapper(original, mode))


def install_tracking_hooks():
    _wrap_storyline_get_stage_event()
    _wrap_day_and_night_selection()
    _wrap_meet()
    _wrap_kill()
    _wrap_location_visits()
    _wrap_item_mutations()
    _wrap_dealer_systems()
    _wrap_afternoon_night_flow()


def run(fn, label):
    global RUN_TERMINATION
    try:
        fn()
        return True
    except _GameTerminated as exc:
        if RUN_TERMINATION is None:
            RUN_TERMINATION = {"label": label, "reason": str(exc), **getattr(exc, "details", {})}
        return False
    except Exception as exc:
        errs.append(f"{label}: {type(exc).__name__}: {exc}")
        log(traceback.format_exc())
        return False


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
    if hasattr(player, "is_gift_system_unlocked") and player.is_gift_system_unlocked():
        _set_funnel_day_once(player, "gift_unlock_day")
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
        "dealer_happiness": int(player.get_dealer_happiness()) if hasattr(player, "get_dealer_happiness") else 50,
        "gift_system_unlocked": bool(player.is_gift_system_unlocked()) if hasattr(player, "is_gift_system_unlocked") else False,
        "has_wrapped_gift": bool(player.has_gift_wrapped()) if hasattr(player, "has_gift_wrapped") else False,
        "store_purchases": int(getattr(player, "_convenience_store_purchases", 0) or 0),
        "loan_shark_debt": int(player.get_loan_shark_debt()) if hasattr(player, "get_loan_shark_debt") else 0,
        "loan_shark_warning_level": int(player.get_loan_shark_warning_level()) if hasattr(player, "get_loan_shark_warning_level") else 0,
        "fraudulent_cash": int(player.get_fraudulent_cash()) if hasattr(player, "get_fraudulent_cash") else 0,
        "gus_items_sold_count": int(player.get_gus_items_sold()) if hasattr(player, "get_gus_items_sold") else len(getattr(player, "_gus_items_sold", set())),
        "gus_total_collectibles": int(player.get_gus_total_collectibles()) if hasattr(player, "get_gus_total_collectibles") else len(getattr(player, "_gus_items_sold", set())),
        "mechanic_dreams": {
            "tom": int(player.get_tom_dreams()) if hasattr(player, "get_tom_dreams") else 0,
            "frank": int(player.get_frank_dreams()) if hasattr(player, "get_frank_dreams") else 0,
            "oswald": int(player.get_oswald_dreams()) if hasattr(player, "get_oswald_dreams") else 0,
            "car_mechanic": str(player.get_car_mechanic()) if hasattr(player, "get_car_mechanic") and player.get_car_mechanic() not in {None, "", "None"} else "",
            "chosen": str(player.get_chosen_mechanic()) if hasattr(player, "get_chosen_mechanic") and player.get_chosen_mechanic() else "",
        },
        "active_progress_goals": tuple(player.get_active_progress_goals()) if hasattr(player, "get_active_progress_goals") else (),
        "completed_progress_goals": tuple(player.get_completed_progress_goals()) if hasattr(player, "get_completed_progress_goals") else (),
        "recent_progress_requests": list(player.get_recent_progress_requests()) if hasattr(player, "get_recent_progress_requests") else [],
        "funnel_metrics": _snapshot_funnel_metrics(player),
        "inventory": set(player._inventory),
        "injuries": set(player._injuries),
        "statuses": set(player._status_effects),
        "companions": set(player._companions.keys()),
        "companion_details": _snapshot_companion_details(player),
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


def _story_print(*args, **kwargs):
    """Capture game print() calls as paragraph breaks in the story log."""
    text = kwargs.get("sep", " ").join(str(a) for a in args)
    text = ANSI_RE.sub("", text)
    # Treat any print() call as a paragraph separator — output its actual content
    # (which is often "\n" or empty) to keep the story readable.
    end = kwargs.get("end", "\n")
    _story_file.write(text + end)
    _story_file.flush()


class _GameTerminated(RuntimeError):
    """Raised when the game attempts to terminate via quit()/exit()."""

    def __init__(self, reason, *, details=None):
        super().__init__(reason)
        self.details = details or {}


RUN_TERMINATION = None
RUN_RESULT_NOTE = None
STALL_REPEAT_THRESHOLD = 3


def _normalize_terminal_name(raw_name):
    name = str(raw_name or "").strip()
    if not name:
        return ""
    name = re.sub(r"(?i)^secret ending:\s*", "", name)
    return re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_")


def _caller_terminal_name(function_name):
    normalized = _normalize_terminal_name(function_name)
    if not normalized:
        return ""
    if normalized.startswith("betrayal_ending_"):
        return normalized[len("betrayal_ending_"):]
    if normalized.endswith("_ending"):
        return normalized[:-len("_ending")]
    return normalized


def _extract_terminal_ending_name(recent_lines, termination=None):
    for line in reversed(recent_lines or []):
        stripped = re.sub(r"\s+", " ", str(line)).strip()
        if not stripped:
            continue
        match = re.search(r"~ ~ ~\s*(.*?)\s*~ ~ ~", stripped, re.IGNORECASE)
        if not match:
            continue
        heading = match.group(1).strip()
        if heading.lower() == "the end":
            continue
        normalized = _normalize_terminal_name(heading)
        if normalized:
            return normalized

    if termination:
        normalized = _caller_terminal_name(termination.get("caller_function"))
        if normalized:
            return normalized
    return ""


def _request_game_termination(*args, **kwargs):
    details = {}
    story_root = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "story")
    for frame_info in inspect.stack()[1:]:
        filename = os.path.abspath(frame_info.filename)
        if not filename.startswith(story_root):
            continue
        if frame_info.function == "_request_game_termination":
            continue
        details = {
            "caller_function": frame_info.function,
            "caller_file": os.path.basename(filename),
        }
        break
    raise _GameTerminated("quit() called", details=details)


def _set_run_result(note):
    global RUN_RESULT_NOTE
    if RUN_RESULT_NOTE is None:
        RUN_RESULT_NOTE = str(note)
        log(f"Result  {RUN_RESULT_NOTE}")


_builtins.print = _story_print
_builtins.quit = _request_game_termination
_builtins.exit = _request_game_termination

with patch("builtins.input", fake_input):
    random.seed(SEED)
    p = story.Player()
    CURRENT_PLAYER = p
    g = bj.Blackjack(p)
    RUN_TERMINATION = None
    RUN_RESULT_NOTE = None
    event_polarity_counts = Counter()
    item_impacts = {}
    max_rank_seen = int(p.get_rank())
    max_balance_seen = int(p.get_balance())
    max_balance_days = [int(p.get_day())] if hasattr(p, "get_day") else [1]
    RUN_PEAK_BALANCE = max_balance_seen
    early_peak_balance = int(p.get_balance())
    early_peak_days = [int(p.get_day())] if hasattr(p, "get_day") else [1]
    early_balance_end = int(p.get_balance())
    EVER_HAD_CAR = bool(p.has_item("Car"))
    CURRENT_CYCLE_FLOW = None
    CYCLE_FLOW_REPORTS = []
    HAND_LOG.clear()
    CYCLE_TEXT.clear()
    CYCLE_EVENTS.clear()
    run(p.opening_lines, "opening")
    if RUN_TERMINATION is not None:
        ending_name = _extract_terminal_ending_name(RECENT_TEXT, RUN_TERMINATION)
        ending_detail = f" | ending: {ending_name}" if ending_name else ""
        source = RUN_TERMINATION.get("caller_function") or RUN_TERMINATION["label"]
        _set_run_result(f"terminal ending before cycle 1{ending_detail} | source: {source}")

    stalled_cycles = 0
    previous_cycle_signature = None
    for cycle_number in range(1, CYCLES + 1):
        if RUN_RESULT_NOTE is not None:
            break
        CURRENT_CYCLE = cycle_number
        CURRENT_EVENTS = []
        CURRENT_CYCLE_FLOW = _new_cycle_flow(p)
        before = snapshot_player(p)
        recent_start = len(RECENT_TEXT)

        if run(g.play_round, f"c{cycle_number}.play") and RUN_TERMINATION is None:
            if run(p.end_day, f"c{cycle_number}.end") and RUN_TERMINATION is None:
                if run(p.start_day, f"c{cycle_number}.start") and RUN_TERMINATION is None:
                    run(p.afternoon, f"c{cycle_number}.aftern")

        after = snapshot_player(p)
        CYCLE_SNAPSHOTS.append((cycle_number, before, after))
        if CURRENT_CYCLE_FLOW is not None:
            CURRENT_CYCLE_FLOW["day"] = int(after["day"])
        cycle_recent_lines = RECENT_TEXT[recent_start:]
        CYCLE_TEXT[cycle_number] = list(cycle_recent_lines)
        CYCLE_EVENTS[cycle_number] = list(CURRENT_EVENTS)
        EVER_HAD_CAR = EVER_HAD_CAR or after["has_car"]
        max_rank_seen = max(max_rank_seen, after["rank"])
        if after["balance"] > max_balance_seen:
            max_balance_seen = after["balance"]
            max_balance_days = [after["day"]]
            RUN_PEAK_BALANCE = max_balance_seen
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
        for item_name in broken_added:
            ITEMS_EVER_BROKEN[item_name] += 1

        stat_changes = stat_deltas(before["statistics"], after["statistics"], TRACKED_STATS)
        gambling_changes = stat_deltas(before["gambling"], after["gambling"], TRACKED_GAMBLING_STATS)

        log("=" * 88)
        log(f"Cycle {cycle_number:02d} | Day {after['day']}")
        log(f"State   {format_state(before, after)}")
        log(f"Events  {', '.join(events) if events else 'none captured'}")
        log(f"Polarity {polarity}")
        log(f"Flow    {_format_cycle_flow(CURRENT_CYCLE_FLOW)}")

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
        if CURRENT_CYCLE_FLOW is not None:
            CYCLE_FLOW_REPORTS.append({
                "cycle": int(CURRENT_CYCLE_FLOW.get("cycle") or cycle_number),
                "day": int(CURRENT_CYCLE_FLOW.get("day") or after["day"]),
                "afternoon_menu_presented": bool(CURRENT_CYCLE_FLOW.get("afternoon_menu_presented")),
                "menu_kind": CURRENT_CYCLE_FLOW.get("menu_kind"),
                "menu_options": list(CURRENT_CYCLE_FLOW.get("menu_options") or []),
                "route_choice": CURRENT_CYCLE_FLOW.get("route_choice"),
                "route_choice_number": CURRENT_CYCLE_FLOW.get("route_choice_number"),
                "route_choice_reason": CURRENT_CYCLE_FLOW.get("route_choice_reason"),
                "route_choice_confidence": CURRENT_CYCLE_FLOW.get("route_choice_confidence"),
                "route_outcome": CURRENT_CYCLE_FLOW.get("route_outcome"),
                "night_handoff": CURRENT_CYCLE_FLOW.get("night_handoff"),
                "night_caller": CURRENT_CYCLE_FLOW.get("night_caller"),
                "night_mode": CURRENT_CYCLE_FLOW.get("night_mode"),
            })

        if RUN_TERMINATION is not None:
            if not after["alive"]:
                cause = after["death_cause"] or before["death_cause"] or "Unknown"
                _set_run_result(f"player died during cycle {cycle_number} | cause: {cause}")
            elif after["balance"] == 0:
                _set_run_result(f"player hit $0 during cycle {cycle_number}")
            else:
                ending_name = _extract_terminal_ending_name(cycle_recent_lines, RUN_TERMINATION)
                ending_detail = f" | ending: {ending_name}" if ending_name else ""
                source = RUN_TERMINATION.get("caller_function") or RUN_TERMINATION["label"]
                _set_run_result(f"terminal ending during cycle {cycle_number}{ending_detail} | source: {source}")
            break

        if not after["alive"]:
            cause = after["death_cause"] or before["death_cause"] or "Unknown"
            _set_run_result(f"player died during cycle {cycle_number} | cause: {cause}")
            break

        if after["balance"] == 0:
            _set_run_result(f"player hit $0 during cycle {cycle_number}")
            break

        cycle_signature = (
            after["day"],
            after["balance"],
            after["health"],
            after["sanity"],
            after["rank"],
            after["alive"],
            tuple(after["inventory"]),
            tuple(after["injuries"]),
            tuple(after["statuses"]),
            tuple(after["travel_restrictions"]),
        )
        if after["day"] <= before["day"] or cycle_signature == previous_cycle_signature:
            stalled_cycles += 1
        else:
            stalled_cycles = 0
        previous_cycle_signature = cycle_signature
        if stalled_cycles >= STALL_REPEAT_THRESHOLD:
            _set_run_result(
                f"stalled during cycle {cycle_number} | day={after['day']} repeated {stalled_cycles} cycles"
            )
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

if RUN_RESULT_NOTE is None:
    _set_run_result(f"reached cycle cap {CYCLES}")

log("")
log("#" * 88)
log(f"Run Summary | cycles_requested={CYCLES} | seed={SEED}")
log(f"Artifact | kind={ARTIFACT_KIND} | schema={ARTIFACT_SCHEMA_VERSION} | run_id={ARTIFACT_RUN_ID} | complete=True")
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
companion_summary = []
for name, data in sorted(final_state["companion_details"].items()):
    companion_summary.append(
        f"{name}:{data['status']}:{data['happiness']}%:{data['days_owned']}d{'*' if data['bonded'] else ''}"
    )
log(f"Companion detail   {companion_summary if companion_summary else 'none'}")
log(
    "Mechanic dreams   "
    f"tom={final_state['mechanic_dreams']['tom']} "
    f"frank={final_state['mechanic_dreams']['frank']} "
    f"oswald={final_state['mechanic_dreams']['oswald']} "
    f"car={final_state['mechanic_dreams'].get('car_mechanic') or 'none'} "
    f"chosen={final_state['mechanic_dreams']['chosen'] or 'none'}"
)
if GIFT_DELIVERIES:
    log("Dealer gifts")
    for delivery in GIFT_DELIVERIES:
        delta = delivery["happiness_change"]
        delta_str = "?" if delta is None else f"{delta:+d}"
        log(
            f"  day={delivery['day'] if delivery['day'] is not None else '?'} item={delivery['item'] or 'unknown'} "
            f"happy={delivery['happiness_before']}->{delivery['happiness_after']} ({delta_str}) "
            f"alive-after={delivery['alive_after']}"
        )
else:
    log("Dealer gifts")
    log("  none")
if DEALER_FREE_HANDS:
    log("Dealer free hands")
    for hand in DEALER_FREE_HANDS:
        log(
            f"  day={hand['day'] if hand['day'] is not None else '?'} tier={hand['tier']} "
            f"happy={hand['dealer_happiness']} bet=${hand['bet']:,} balance=${hand['balance']:,}"
        )
else:
    log("Dealer free hands")
    log("  none")
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
    personality_counts = Counter(
        str((trace.metadata or {}).get("plan", {}).get("personality", "unknown"))
        for trace in DECISION_TRACES
    )
    reason_code_counts = Counter(
        str((trace.metadata or {}).get("reason_code", "unknown"))
        for trace in DECISION_TRACES
    )
    ev_values = [
        float((trace.metadata or {}).get("expected_value_estimate", 0.0) or 0.0)
        for trace in DECISION_TRACES
    ]
    log("  goals " + " | ".join(f"{goal}={count}" for goal, count in goal_counts.most_common(8)))
    log("  personalities " + " | ".join(f"{name}={count}" for name, count in personality_counts.most_common(8)))
    log("  reason_codes " + " | ".join(f"{name}={count}" for name, count in reason_code_counts.most_common(10)))
    if ev_values:
        log(f"  expected_value avg={sum(ev_values)/len(ev_values):.2f} max={max(ev_values):.2f} min={min(ev_values):.2f}")
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
decision_personality_counts = Counter(
    str((trace.metadata or {}).get("plan", {}).get("personality", "unknown"))
    for trace in DECISION_TRACES
)
decision_reason_code_counts = Counter(
    str((trace.metadata or {}).get("reason_code", "unknown"))
    for trace in DECISION_TRACES
)
decision_expected_values = [
    float((trace.metadata or {}).get("expected_value_estimate", 0.0) or 0.0)
    for trace in DECISION_TRACES
]

json_payload = {
    "artifact": {
        "kind": ARTIFACT_KIND,
        "schema_version": ARTIFACT_SCHEMA_VERSION,
        "run_id": ARTIFACT_RUN_ID,
        "seed": SEED,
        "cycles_requested": CYCLES,
        "complete": True,
        "generated_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "pythonhashseed": os.getenv("PYTHONHASHSEED", ""),
    },
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
        "result_note": RUN_RESULT_NOTE,
    },
    "final_state": {
        "inventory": sorted(final_state["inventory"]),
        "has_car": final_state["has_car"],
        "dealer_happiness": final_state["dealer_happiness"],
        "gift_system_unlocked": final_state["gift_system_unlocked"],
        "has_wrapped_gift": final_state["has_wrapped_gift"],
        "store_purchases": final_state["store_purchases"],
        "loan_shark_debt": final_state["loan_shark_debt"],
        "loan_shark_warning_level": final_state["loan_shark_warning_level"],
        "fraudulent_cash": final_state["fraudulent_cash"],
        "gus_items_sold_count": final_state["gus_items_sold_count"],
        "gus_total_collectibles": final_state["gus_total_collectibles"],
        "mechanic_dreams": dict(final_state["mechanic_dreams"]),
        "active_progress_goals": sorted(final_state["active_progress_goals"]),
        "completed_progress_goals": sorted(final_state["completed_progress_goals"]),
        "recent_progress_requests": list(final_state["recent_progress_requests"]),
        "funnel_metrics": dict(final_state["funnel_metrics"]),
        "injuries": sorted(final_state["injuries"]),
        "statuses": sorted(final_state["statuses"]),
        "pawned_items": sorted(final_state["pawned_items"]),
        "companions": sorted(final_state["companions"]),
        "companion_details": dict(final_state["companion_details"]),
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
    "flask_purchases": dict(FLASK_PURCHASES),
    "items_ever_broken": dict(ITEMS_EVER_BROKEN),
    "gift_deliveries": list(GIFT_DELIVERIES),
    "dealer_free_hands": list(DEALER_FREE_HANDS),
    "event_polarity": dict(event_polarity_counts),
    "item_impacts": dict(item_impacts),
    "item_provenance": {
        item_name: {
            key: list(history[key])
            for key in ["acquired", "used", "removed", "broken", "fixed", "repairing"]
        }
        for item_name, history in ITEM_PROVENANCE.items()
    },
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
        "personality_counts": dict(decision_personality_counts),
        "reason_code_counts": dict(decision_reason_code_counts),
        "expected_value_summary": {
            "avg": (sum(decision_expected_values) / len(decision_expected_values)) if decision_expected_values else 0.0,
            "max": max(decision_expected_values) if decision_expected_values else 0.0,
            "min": min(decision_expected_values) if decision_expected_values else 0.0,
        },
        "route_outcome_counts": dict(route_outcome_counts),
        "route_interrupt_kind_counts": dict(route_interrupt_kind_counts),
        "route_interrupted_goal_counts": dict(route_interrupted_goal_counts),
        "route_interrupted_top_goal_counts": dict(route_interrupted_top_goal_counts),
        "route_applied_goal_counts": dict(route_applied_goal_counts),
        "route_suppressed_goal_counts": dict(route_suppressed_goal_counts),
    },
    "cycle_flows": list(CYCLE_FLOW_REPORTS),
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

_write_json_artifact(json_payload)
_write_decision_tree()

# Restore real print before closing so final messages are visible
_builtins.print = _real_print
_publish_artifacts()
print(f"Results -> {LOG}")
print(f"Story   -> {STORY_LOG}")
print(f"Tree    -> {DTREE_LOG}")
print(f"Errors: {len(errs)}")
