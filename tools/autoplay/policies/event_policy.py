from __future__ import annotations

from ..config import (
    GIFT_WRAP_HAPPINESS_THRESHOLD,
    GIFT_WRAP_MIN_BALANCE,
    MILLIONAIRE_ENDING_PREFERENCE,
)
from ..interfaces import DecisionOption, DecisionRequest
from ..planner import StrategicPlan
from ..trace import DecisionTrace


def _choice_matches(choice: str, keyword: str) -> bool:
    choice_text = str(choice).strip().lower().replace("_", " ").replace("-", " ")
    keyword_text = str(keyword).strip().lower().replace("_", " ").replace("-", " ")
    return keyword_text in choice_text


def _option_trace(
    request: DecisionRequest,
    plan: StrategicPlan,
    options: list[DecisionOption],
    chosen_index: int,
    reason: str,
    confidence: float,
) -> DecisionTrace:
    chosen = options[chosen_index]
    score_breakdown = {option.option_id: (1.0 if idx == chosen_index else 0.0) for idx, option in enumerate(options)}
    return DecisionTrace(
        cycle=request.metadata.get("cycle"),
        day=request.metadata.get("day"),
        context=request.stable_context_id or request.request_type,
        request_type=request.request_type,
        strategic_goal=plan.goal,
        chosen_action=str(chosen.value if chosen.value is not None else chosen.label),
        reason=reason,
        confidence=confidence,
        options=tuple(option.label for option in options),
        game_state_summary=dict(request.game_state),
        score_breakdown=score_breakdown,
        metadata={"plan": plan.to_dict()},
    )


def _choose_generic_option(options: list[DecisionOption], request: DecisionRequest) -> tuple[int | None, str | None, float]:
    normalized = [str(option.label).strip().lower() for option in options]
    prompt_lower = str(request.metadata.get("prompt_lower", "") or "")
    balance = int(request.game_state.get("balance", 0) or 0)
    health = int(request.game_state.get("health", 0) or 0)
    sanity = int(request.game_state.get("sanity", 0) or 0)
    rank = int(request.game_state.get("rank", 0) or 0)

    if not normalized:
        return None, None, 0.0

    if "what do you do" in prompt_lower and normalized == ["pull it out", "leave it", "drive to shop"]:
        inventory = {str(item).lower() for item in request.game_state.get("inventory", ())}
        if balance >= 25:
            return normalized.index("drive to shop"), "car_triage_drive_to_shop", 0.7
        if "tire patch kit" in inventory or "spare tire" in inventory:
            return normalized.index("pull it out"), "car_triage_self_repair", 0.7
        return normalized.index("leave it"), "car_triage_leave_it", 0.7

    if ("pay everything" in normalized or "pay what you have" in normalized) and balance > 0:
        if "pay everything" in normalized:
            return normalized.index("pay everything"), "pay_everything_when_possible", 0.62
        if "pay what you have" in normalized:
            return normalized.index("pay what you have"), "pay_partial_when_possible", 0.62

    low_resources = health < 50 or sanity < 25 or balance < 50
    preserving_run = balance >= 1000 or rank >= 1

    if low_resources:
        for keyword in [
            "leave", "walk", "observe", "watch", "decline", "refuse", "ignore", "save",
            "wait", "talk", "comply", "call", "call_911", "ask", "ask_questions", "ask_advice",
            "photograph", "report", "return", "apologize", "prove", "calm", "help", "follow", "peek",
        ]:
            for index, choice in enumerate(normalized):
                if _choice_matches(choice, keyword):
                    return index, f"generic_low_resource_choice:{keyword}", 0.5

    if preserving_run:
        for keyword in [
            "leave", "walk", "observe", "watch", "decline", "refuse", "ignore", "save",
            "wait", "comply", "call", "call_911", "report", "ask", "ask_questions", "ask_advice",
            "photograph", "return", "apologize", "prove", "talk", "calm", "peek",
        ]:
            for index, choice in enumerate(normalized):
                if _choice_matches(choice, keyword):
                    return index, f"generic_preserve_run_choice:{keyword}", 0.48

    prioritized_keywords = [
        "help", "join", "enter", "play", "follow", "accept", "investigate", "comply",
        "talk", "communicate", "negotiate", "teamwork", "calm", "report", "organize",
        "return", "apologize", "prove", "call", "ask", "ask_questions", "ask_advice",
        "peek", "photograph", "observe", "watch", "leave",
    ]
    for keyword in prioritized_keywords:
        for index, choice in enumerate(normalized):
            if _choice_matches(choice, keyword):
                return index, f"generic_keyword_choice:{keyword}", 0.42

    risky_keywords = {"rob", "steal", "betray", "sabotage", "insult", "all_in", "fight"}
    for index, choice in enumerate(normalized):
        if not any(_choice_matches(choice, keyword) for keyword in risky_keywords):
            return index, "generic_non_risky_choice", 0.35

    return 0, "first_option_fallback", 0.25


def _choose_generic_inline(request: DecisionRequest) -> tuple[str | None, str | None, float]:
    prompt_lower = str(request.metadata.get("prompt_lower", "") or "")
    balance = int(request.game_state.get("balance", 0) or 0)
    health = int(request.game_state.get("health", 0) or 0)
    sanity = int(request.game_state.get("sanity", 0) or 0)
    rank = int(request.game_state.get("rank", 0) or 0)
    choices = [str(option.label).strip().lower() for option in request.normalized_options]

    if not choices:
        return None, None, 0.0

    if "$1" in choices or "$5" in choices or "free" in choices:
        if balance < 20:
            chosen = "free" if "free" in choices else choices[0]
            return chosen, "cheap_inline_low_balance", 0.52
        chosen = "$1" if "$1" in choices else ("free" if "free" in choices else choices[0])
        return chosen, "cheap_inline_budget_pick", 0.52

    if "money" in prompt_lower or "wish" in prompt_lower:
        for choice in ["health", "luck", "info", "peace", "money"]:
            if choice in choices:
                return choice, f"wish_inline_choice:{choice}", 0.5

    low_resources = health < 50 or sanity < 25 or balance < 50
    preserving_run = balance >= 1000 or rank >= 1

    if low_resources:
        for keyword in [
            "leave", "walk", "observe", "watch", "decline", "refuse", "ignore", "save",
            "wait", "talk", "comply", "call", "call_911", "ask", "ask_questions", "ask_advice",
            "photograph", "report", "return", "apologize", "prove", "calm", "help", "follow", "peek",
        ]:
            for choice in choices:
                if _choice_matches(choice, keyword):
                    return choice, f"generic_inline_low_resource_choice:{keyword}", 0.42

    if preserving_run:
        for keyword in [
            "leave", "walk", "observe", "watch", "decline", "refuse", "ignore", "save",
            "wait", "comply", "call", "call_911", "report", "ask", "ask_questions", "ask_advice",
            "photograph", "return", "apologize", "prove", "talk", "calm", "peek",
        ]:
            for choice in choices:
                if _choice_matches(choice, keyword):
                    return choice, f"generic_inline_preserve_run_choice:{keyword}", 0.4

    prioritized_keywords = [
        "help", "join", "enter", "play", "follow", "accept", "investigate", "comply",
        "talk", "communicate", "negotiate", "teamwork", "calm", "report", "organize",
        "return", "apologize", "prove", "call", "ask", "ask_questions", "ask_advice",
        "peek", "photograph", "observe", "watch", "leave",
    ]
    for keyword in prioritized_keywords:
        for choice in choices:
            if _choice_matches(choice, keyword):
                return choice, f"generic_inline_keyword_choice:{keyword}", 0.35

    risky_keywords = {"rob", "steal", "betray", "sabotage", "insult", "all_in", "fight"}
    for choice in choices:
        if not any(_choice_matches(choice, keyword) for keyword in risky_keywords):
            return choice, "generic_inline_non_risky_choice", 0.3

    return choices[0], "generic_inline_first_choice", 0.25


def _yes_no_trace(request: DecisionRequest, plan: StrategicPlan, chosen: str, reason: str, confidence: float) -> DecisionTrace:
    return DecisionTrace(
        cycle=request.metadata.get("cycle"),
        day=request.metadata.get("day"),
        context=request.stable_context_id or request.request_type,
        request_type=request.request_type,
        strategic_goal=plan.goal,
        chosen_action=chosen,
        reason=reason,
        confidence=confidence,
        options=tuple(option.label for option in request.normalized_options),
        game_state_summary=dict(request.game_state),
        metadata={"plan": plan.to_dict()},
    )


def _inline_trace(request: DecisionRequest, plan: StrategicPlan, chosen: str, reason: str, confidence: float) -> DecisionTrace:
    return DecisionTrace(
        cycle=request.metadata.get("cycle"),
        day=request.metadata.get("day"),
        context=request.stable_context_id or request.request_type,
        request_type=request.request_type,
        strategic_goal=plan.goal,
        chosen_action=chosen,
        reason=reason,
        confidence=confidence,
        options=tuple(option.label for option in request.normalized_options),
        game_state_summary=dict(request.game_state),
        metadata={"plan": plan.to_dict()},
    )


def choose_event_yes_no(request: DecisionRequest, plan: StrategicPlan) -> tuple[str | None, DecisionTrace | None]:
    prompt_lower = str(request.metadata.get("prompt_lower", "") or "").strip()
    recent = str(request.metadata.get("recent_lower", "") or "")
    cost = request.metadata.get("cost")
    balance = int(request.game_state.get("balance", 0) or 0)
    health = int(request.game_state.get("health", 0) or 0)
    sanity = int(request.game_state.get("sanity", 0) or 0)
    rank = int(request.game_state.get("rank", 0) or 0)

    always_yes = {
        "do you ask if he's okay?",
        "do you listen?",
        "stand up for kyle?",
        "do you try to explain your situation?",
        "accept the coffee?",
        "take the card?",
        "applaud the performance?",
        "do you like it?",
        '"what was that?"',
        "what was that?",
        '"what was that?',
        "do you? know this?",
        "did you? read it?",
        "are you? gonna leave?",
        "suggest trusty tom might be able to help?",
        "call the number?",
        "write down the recipe?",
        "keep petting him?",
        "throw the rock?",
        "ask about the photo?",
        "pick it up?",
        "ask the dealer about his past?",
        "accept his lesson?",
        "write down the numbers?",
        "try to tune to the frequency and listen for more?",
        "go inside?",
        "take the logbook?",
        "walk through the cemetery while you wait?",
        "talk to edgar?",
        "take the letter?",
        "enter the carnival?",
        "ask if it gets better?",
        "check out the apartment?",
        "feed it some of your food?",
        "take him in?",
        "try to befriend the trash gremlin?",
        "offer it some food?",
        "take the rabbit with you?",
        "follow the duck parade?",
        "throw them some bread/money as tribute?",
        "keep the kitten?",
        "visit him?",
        "give him money?",
        "allow the photoshoot?",
        "reply anyway?",
        "try to return it to the owner?",
        "pick her up?",
        "grant the interview?",
        "accept the vip treatment?",
        "shake her hand?",
        "agree to the documentary?",
        "talk to... dr. socksworth?",
        "listen to him?",
        "do the interview?",
        "do you promise?",
        # Phil's final interrogation: "Will you leave?" → answer "yes" = 25% death,
        # "no" = 33% death. Always say yes for the better odds (bot normally hits
        # threat_context_refusal and says no, which is the worse choice).
        '"answer me. "',
        '"answer me."',
        "answer me.",
    }
    always_no = {
        "take the pill?",
        "pay $50 for the pills?",
        "accept the credit?",
        "hold the box for stuart?",
        "do you correct her?",
        "do you accept the shadow's offer?",
        "accept the blood moon bargain?",
        "accept the devil's offer?",
        "sell your kidney?",
        "buy the drugs? ($500)",
        "buy the painkillers? ($100)",
        "buy more pills? ($150 - prices went up)",
        "pay $100 to spin?",
        "hang up?",
        "lie and say yes?",
        "go back to the tables?",
        "ask who 'they' are?",
        "give jameson $100 for vet bills?",
        "pay him $50 for the info?",
        "pay $20 for a prophecy?",
        "tell them the truth?",
        "accept his offer?",
    }

    if prompt_lower in always_yes:
        return "yes", _yes_no_trace(request, plan, "yes", f"event_yes:{prompt_lower}", 0.82)
    if prompt_lower in always_no:
        return "no", _yes_no_trace(request, plan, "no", f"event_no:{prompt_lower}", 0.82)

    # Betsy the cow: "Moo? " prompt. Two different events with very different costs.
    # hungry_cow  (stage 0): $100 per feeding — affordable, pay unless it would block car acquisition.
    # starving_cow (stage 1): $10,000 per feeding — only pay if we genuinely have it.
    # cow_army    (stage 2): $100,000 per feeding — refuse unless Doughman/nearly rich.
    # Differentiator: "tractor" in recent → stage 1 ($10k); "army" in recent → stage 2 ($100k).
    if prompt_lower == "moo?":
        rank = int(request.game_state.get("rank", 0) or 0)
        needs_car = not bool(request.game_state.get("has_car", False))
        if "army" in recent or "hundred thousand" in recent or "100,000" in recent:
            # cow_army: $100k per round — only pay if Doughman (rank 4+)
            answer = "yes" if rank >= 4 and balance >= 100000 else "no"
            return answer, _yes_no_trace(request, plan, answer, "betsy_army_budget_gate", 0.85)
        if "tractor" in recent:
            # starving_cow: $10,000 per round — only pay if we can afford it
            answer = "yes" if balance >= 10000 else "no"
            return answer, _yes_no_trace(request, plan, answer, "betsy_tractor_budget_gate", 0.85)
        # hungry_cow: $100 per round. Pay unless it would block car acquisition.
        car_reserve = 250 if needs_car else 0
        answer = "yes" if balance >= 100 + car_reserve else "no"
        return answer, _yes_no_trace(request, plan, answer, "betsy_hungry_budget_gate", 0.82)

    if prompt_lower == "take the money?" and "loyalty bonus" in recent:
        return "no", _yes_no_trace(request, plan, "no", "loyalty_bonus_money_refusal", 0.8)
    if prompt_lower == "do you run?" and "hendricks" in recent:
        return "no", _yes_no_trace(request, plan, "no", "hendricks_refusal", 0.8)
    if prompt_lower == "do the delivery?" and "feelgood" in recent:
        return "no", _yes_no_trace(request, plan, "no", "feelgood_delivery_refusal", 0.8)

    if prompt_lower == "buy the gyro?":
        answer = "yes" if balance >= 5 and (health < 92 or sanity < 72) else "no"
        return answer, _yes_no_trace(request, plan, answer, "gyro_health_or_sanity_gate", 0.72)
    if prompt_lower == "give him some money to make him go away?":
        answer = "yes" if balance >= 150 and sanity < 55 else "no"
        return answer, _yes_no_trace(request, plan, answer, "sanity_relief_payment_gate", 0.7)
    if prompt_lower == "buy yourself a cupcake?":
        answer = "yes" if balance >= 20 and sanity < 55 else "no"
        return answer, _yes_no_trace(request, plan, answer, "cupcake_sanity_gate", 0.7)
    if prompt_lower == "attend the book club?":
        answer = "yes" if sanity < 55 else "no"
        return answer, _yes_no_trace(request, plan, answer, "book_club_sanity_gate", 0.68)
    if prompt_lower == "donate $100 to charity?":
        answer = "yes" if balance - int(cost or 100) >= 2500 else "no"
        return answer, _yes_no_trace(request, plan, answer, "charity_surplus_gate", 0.72)
    if prompt_lower == "hire the bodyguard?":
        answer = "yes" if balance >= 20000 else "no"
        return answer, _yes_no_trace(request, plan, answer, "bodyguard_budget_gate", 0.75)

    if prompt_lower == "accept the offer?":
        if "walk away right now" in recent and "double whatever you have" in recent:
            return "yes", _yes_no_trace(request, plan, "yes", "double_money_offer_accept", 0.74)
        if "guarantee your victory" in recent or "something you won't even miss" in recent:
            return "no", _yes_no_trace(request, plan, "no", "ominous_offer_refusal", 0.74)
        if "vague" in recent or "wrong" in recent:
            return "no", _yes_no_trace(request, plan, "no", "vague_offer_refusal", 0.72)

    if prompt_lower == "pay the $500 fine?":
        answer = "yes" if balance - int(cost or 500) >= 500 else "no"
        return answer, _yes_no_trace(request, plan, answer, "fine_reserve_gate", 0.72)
    if prompt_lower == "pay to remove the boot? ($300)":
        answer = "yes" if balance - int(cost or 300) >= 500 else "no"
        return answer, _yes_no_trace(request, plan, answer, "boot_reserve_gate", 0.72)
    if prompt_lower == "pay to get your car back? ($800)":
        answer = "yes" if balance - int(cost or 800) >= 700 else "no"
        return answer, _yes_no_trace(request, plan, answer, "car_recovery_gate", 0.74)

    # Gift wrap decision: wrap an item when dealer happiness is below the useful threshold
    # and we have enough balance and aren't in an emergency.
    if "gift wrap" in prompt_lower:
        dealer_happiness = int(request.game_state.get("dealer_happiness", 50) or 50)
        # Emergency check: goal-based and stats-based for belt-and-suspenders safety
        in_emergency_goal = plan.goal in {"survive_emergency", "acquire_car", "contain_debt_escalation"}
        in_emergency_stats = health < 45 or sanity < 20 or not request.game_state.get("has_car", True)
        in_emergency = in_emergency_goal or in_emergency_stats
        answer = (
            "yes"
            if (
                balance >= GIFT_WRAP_MIN_BALANCE
                and dealer_happiness < GIFT_WRAP_HAPPINESS_THRESHOLD
                and not in_emergency
            )
            else "no"
        )
        return answer, _yes_no_trace(request, plan, answer, "gift_wrap_happiness_gate", 0.8)

    # Confirm crafting at workbench: always accept when the autoplay chose to craft.
    # Require "car workbench" in recent to avoid false positives from other yes/no contexts.
    if "(yes/no):" in prompt_lower and "car workbench" in recent and "crafted" not in recent and (
        "combine" in recent or "what do you want to craft" in recent
    ):
        return "yes", _yes_no_trace(request, plan, "yes", "workbench_craft_confirm", 0.9)

    if not prompt_lower:
        if any(
            phrase in recent
            for phrase in [
                "do you search the body?",
                "do you approach the figure?",
                "do you open it?",
                "do you search it?",
                "do you check on them?",
                "do you help him collect shells?",
                "do you join them?",
                "do you approach the witch's shack?",
                "do you try to pull it up and search it?",
                "do you swim over to investigate?",
            ]
        ):
            return "yes", _yes_no_trace(request, plan, "yes", "blank_prompt_investigate_yes", 0.68)
        if "do you sit and listen?" in recent:
            return "no", _yes_no_trace(request, plan, "no", "blank_prompt_listen_no", 0.68)

    return None, None


def choose_event_option(request: DecisionRequest, plan: StrategicPlan) -> tuple[DecisionOption | None, DecisionTrace | None]:
    options = list(request.normalized_options)
    normalized = [str(option.label).strip().lower() for option in options]
    balance = int(request.game_state.get("balance", 0) or 0)
    health = int(request.game_state.get("health", 0) or 0)

    chosen_index = None
    reason = None

    if normalized == ["pay $300 for the pills", "walk away cold turkey", "threaten him"]:
        chosen_index, reason = 1, "pill_menu_cold_turkey"
    elif normalized == ["help jameson - charge in", "honk your horn to scare them off", "stay hidden and watch"]:
        chosen_index, reason = (0, "jameson_help") if health >= 65 else (1, "jameson_horn")
    elif normalized == ["refuse - lucky stays with you", "tell him to prove it", "give lucky back"]:
        chosen_index, reason = 1, "protect_lucky_prove_it"
    elif normalized == ["try the combination", "ask around about who left the notes", "leave it alone"]:
        chosen_index, reason = 0, "try_combination"
    elif normalized == ["eat it anyway", "apologize", "throw it"]:
        chosen_index, reason = (0, "eat_anyway_low_health") if health < 40 else (1, "apologize_default")
    elif normalized == ["use it", "throw it away", "return it"]:
        chosen_index, reason = 2, "return_found_item"
    elif normalized == ["pay now", "beg for time", "refuse"]:
        chosen_index, reason = (0, "pay_now_high_balance") if balance >= 75000 else (1, "beg_for_time")
    elif normalized == ["ride it out", "drive to casino anyway", "hurt yourself more"]:
        chosen_index, reason = 0, "ride_it_out"
    elif normalized == ["call for help", "try to help yourself", "walk away"]:
        chosen_index, reason = 0, "call_for_help"
    elif normalized == ["pay for treatment", "refuse treatment", "break down"]:
        chosen_index, reason = (0, "pay_treatment") if balance >= 50000 else (1, "refuse_treatment")
    elif normalized == ["climb the railing", "call someone", "walk away"]:
        chosen_index, reason = 1, "call_someone"
    elif normalized == ["agree to leave", "offer money", "fight back"]:
        chosen_index, reason = 0, "agree_to_leave"
    elif normalized == ["comply", "run", "fight"]:
        chosen_index, reason = 0, "comply_default"
    elif normalized == ["comply", "hide", "hero"]:
        chosen_index, reason = 1, "hide_robbery_cover"
    elif normalized == ["wrong person", "play along", "run"]:
        chosen_index, reason = 0, "wrong_person"
    elif normalized == ["step back", "stay", "call for help"]:
        chosen_index, reason = 2, "call_for_help"
    elif normalized == ["bail out", "investigate", "ignore it"]:
        chosen_index, reason = 0, "bail_out"
    elif normalized == ["try it", "sell it", "throw it away"]:
        chosen_index, reason = 1, "sell_it"
    elif normalized == ["save the bird", "ignore your phone", "scream"]:
        chosen_index, reason = 1, "ignore_phone"
    elif normalized == ["not interested", "what are you offering", "souls?"]:
        chosen_index, reason = 0, "not_interested"
    elif normalized == ["take it", "leave it"]:
        chosen_index, reason = 0, "take_it"
    elif normalized == ["keep the cash", "return it all"]:
        chosen_index, reason = 1, "return_it_all"
    elif normalized == ["sell it", "turn it in"]:
        chosen_index, reason = 1, "turn_it_in"
    elif normalized == ["heads", "tails"]:
        chosen_index, reason = 0, "coin_flip_heads"
    elif normalized == ["violinist", "drummer", "neither"]:
        chosen_index, reason = 2, "choose_neither"
    elif normalized == ["confident", "humble", "no comment"]:
        chosen_index, reason = 1, "choose_humble"
    elif normalized == ["apologize", "confront", "ask for help"]:
        chosen_index, reason = 2, "ask_for_help"
    elif normalized == ["worm", "robot", "spin move", "moonwalk", "interpretive dance"]:
        chosen_index, reason = 3, "moonwalk"

    # Millionaire afternoon menu: choose between mechanic ending and airport.
    # Options like "Visit Tom's...", "Drive to the Airport", "Continue gambling".
    if chosen_index is None:
        millionaire_labels = {
            opt.label.lower(): idx
            for idx, opt in enumerate(options)
        }
        is_millionaire_menu = (
            any("drive to the airport" in lbl for lbl in millionaire_labels)
            and any(
                keyword in lbl
                for keyword in ("tom", "frank", "oswald", "mechanic")
                for lbl in millionaire_labels
            )
        )
        if is_millionaire_menu:
            chosen_mechanic = str(request.game_state.get("chosen_mechanic") or "")
            for pref in MILLIONAIRE_ENDING_PREFERENCE:
                if pref == "mechanic" and chosen_mechanic:
                    for lbl, idx in millionaire_labels.items():
                        if chosen_mechanic.lower() in lbl:
                            chosen_index = idx
                            reason = f"millionaire_mechanic_ending:{chosen_mechanic}"
                            break
                elif pref == "mechanic":
                    for lbl, idx in millionaire_labels.items():
                        if any(name in lbl for name in ("tom", "frank", "oswald")):
                            chosen_index = idx
                            reason = "millionaire_mechanic_ending_any"
                            break
                elif pref == "airport":
                    for lbl, idx in millionaire_labels.items():
                        if "airport" in lbl:
                            chosen_index = idx
                            reason = "millionaire_airport_ending"
                            break
                if chosen_index is not None:
                    break

    if chosen_index is None:
        chosen_index, reason, confidence = _choose_generic_option(options, request)
        if chosen_index is None:
            return None, None
        return options[chosen_index], _option_trace(request, plan, options, chosen_index, reason or "event_option_policy", confidence)

    return options[chosen_index], _option_trace(request, plan, options, chosen_index, reason or "event_option_policy", 0.8)


def choose_event_inline_choice(request: DecisionRequest, plan: StrategicPlan) -> tuple[str | None, DecisionTrace | None]:
    prompt_lower = str(request.metadata.get("prompt_lower", "") or "")
    recent = str(request.metadata.get("recent_lower", "") or "")
    balance = int(request.game_state.get("balance", 0) or 0)
    choices = [str(option.label).strip().lower() for option in request.normalized_options]
    choice_set = set(choices)
    inventory = {str(item).lower() for item in request.game_state.get("inventory", ())}

    if prompt_lower == "your favorite color:":
        return "blue", _inline_trace(request, plan, "blue", "favorite_color_default", 0.85)
    if prompt_lower == "your favorite animal:":
        return "dog", _inline_trace(request, plan, "dog", "favorite_animal_default", 0.85)

    set_map = {
        frozenset({"around", "wait"}): ("wait", "wait_out_event"),
        frozenset({"force", "take"}): ("force", "force_opening"),
        frozenset({"help", "buy", "swim"}): ("help", "help_default"),
        frozenset({"luck", "love", "revenge"}): ("luck", "luck_preference"),
        frozenset({"tough", "beach"}): ("beach", "beach_pick"),
        frozenset({"fight", "parallel", "float"}): ("parallel", "parallel_pick"),
        frozenset({"open", "save"}): ("open", "open_default"),
        frozenset({"keep", "return"}): ("return", "return_default"),
        frozenset({"swim", "still", "scare"}): ("still", "still_default"),
        frozenset({"accept", "decline", "scram"}): ("decline", "decline_suspicious_offer"),
        frozenset({"nice", "cheap", "skip"}): ("skip", "skip_cheap_option"),
        frozenset({"listen", "tip", "walk"}): ("listen", "listen_default"),
        frozenset({"help", "run", "sneak", "film"}): ("film", "film_over_risk"),
        frozenset({"help", "love", "dodge"}): ("love", "love_over_risk"),
        frozenset({"fight", "talk", "comply", "run"}): ("comply", "comply_default"),
        frozenset({"tip", "flinch", "watch"}): ("watch", "watch_default"),
        frozenset({"help", "ignore", "trick"}): ("help", "help_default"),
        frozenset({"feed", "flee", "dominance"}): ("dominance", "dominance_pick"),
        frozenset({"sit", "money", "walk"}): ("sit", "sit_default"),
        frozenset({"line", "cut", "resist"}): ("line", "line_default"),
        frozenset({"feed", "skip", "sit"}): ("sit", "sit_default"),
        frozenset({"play", "watch", "decline"}): ("watch", "watch_default"),
        frozenset({"approach", "watch", "leave"}): ("watch", "watch_default"),
    }
    mapped = set_map.get(frozenset(choice_set))
    if mapped is not None:
        chosen, reason = mapped
        return chosen, _inline_trace(request, plan, chosen, reason, 0.82)

    if choice_set == {"pull", "burn"}:
        chosen = "burn" if any(item in inventory for item in {"lighter", "matches", "road flares"}) else "pull"
        return chosen, _inline_trace(request, plan, chosen, "fire_source_gate", 0.8)
    if choice_set == {"pet", "feed", "ignore"}:
        chosen = "feed" if "can of tuna" in inventory else "pet"
        return chosen, _inline_trace(request, plan, chosen, "pet_or_feed_gate", 0.8)

    if prompt_lower == "choose:":
        if "your companion is sick. what do you do?" in recent:
            if balance >= 50:
                return "2", _inline_trace(request, plan, "2", "companion_sick_pay_choice", 0.84)
            if "cough drops" in inventory:
                return "1", _inline_trace(request, plan, "1", "companion_sick_item_choice", 0.82)
            return "4", _inline_trace(request, plan, "4", "companion_sick_rest_choice", 0.8)
        if "what do you do?\n1. break it up carefully" in recent or "break it up carefully" in recent:
            return "1", _inline_trace(request, plan, "1", "break_it_up_carefully", 0.82)
        if "morning. your companions are hungry." in recent:
            # If companion runaway risk is high, prefer buying food (option 3) over skipping (option 4)
            companion_runaway_risk = int(request.game_state.get("companion_runaway_risk_count", 0) or 0)
            low_happiness = int(request.game_state.get("companion_low_happiness_count", 0) or 0)
            urgent_companion_need = companion_runaway_risk > 0 or low_happiness > 0
            chosen = "3" if (balance >= 20 or urgent_companion_need) else "4"
            return chosen, _inline_trace(request, plan, chosen, "hungry_companions_gate", 0.82)
        if "something's wrong." in recent and "is gone." in recent and "search the immediate area" in recent:
            return "1", _inline_trace(request, plan, "1", "search_immediate_area", 0.8)
        if "someone in trouble" in recent and "1. drive over and help" in recent:
            return "1", _inline_trace(request, plan, "1", "drive_over_and_help", 0.8)

    chosen, reason, confidence = _choose_generic_inline(request)
    if chosen is None:
        return None, None
    return chosen, _inline_trace(request, plan, chosen, reason or "event_inline_policy", confidence)