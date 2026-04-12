from __future__ import annotations

from ..config import (
    GIFT_WRAP_HAPPINESS_THRESHOLD,
    GIFT_WRAP_MIN_BALANCE,
    MILLIONAIRE_ENDING_PREFERENCE,
)
from ..interfaces import DecisionOption, DecisionRequest
from ..planner import StrategicPlan
from ..trace import DecisionTrace


# ==============================================================================
# TRACE HELPERS
# ==============================================================================


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
        metadata={
            "plan": plan.to_dict(),
            "reason_code": reason,
            "event_handler": reason,
            "expected_value_estimate": 1.0 if chosen == "yes" else 0.0,
            "candidate_actions": [
                {"option": "yes", "selected": chosen == "yes"},
                {"option": "no", "selected": chosen == "no"},
            ],
        },
    )


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
        metadata={
            "plan": plan.to_dict(),
            "reason_code": reason,
            "event_handler": reason,
            "expected_value_estimate": 1.0,
            "candidate_actions": [
                {
                    "option_id": option.option_id,
                    "selected": idx == chosen_index,
                }
                for idx, option in enumerate(options)
            ],
        },
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
        metadata={
            "plan": plan.to_dict(),
            "reason_code": reason,
            "event_handler": reason,
            "expected_value_estimate": 1.0,
            "candidate_actions": [
                {"option": option.label, "selected": str(option.label).lower() == str(chosen).lower()}
                for option in request.normalized_options
            ],
        },
    )


# ==============================================================================
# UTILITY HELPERS
# ==============================================================================


def _choice_matches(choice: str, keyword: str) -> bool:
    choice_text = str(choice).strip().lower().replace("_", " ").replace("-", " ")
    keyword_text = str(keyword).strip().lower().replace("_", " ").replace("-", " ")
    return keyword_text in choice_text


def _pick_safe_option(options, normalized, reason_prefix="avoid_violence"):
    """When a dangerous option is present, pick the safest alternative."""
    safe_keywords = [
        "comply", "leave", "walk", "hide", "surrender", "run", "back away",
        "apologize", "calm", "talk", "pay", "beg", "observe", "watch", "wait",
    ]
    for safe_kw in safe_keywords:
        for i, opt in enumerate(normalized):
            if safe_kw in opt:
                return i, f"{reason_prefix}_pick_{safe_kw}"
    return 0, f"{reason_prefix}_first_option"


# ==============================================================================
# GENERIC BEHAVIORAL STRATEGIES (for unmapped events only)
# ==============================================================================


def _choose_generic_option(
    options: list[DecisionOption],
    request: DecisionRequest,
    *,
    prefer_safe: bool = False,
) -> tuple[int | None, str | None, float]:
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

    if low_resources or prefer_safe:
        for keyword in [
            "leave", "walk", "observe", "watch", "decline", "refuse", "ignore", "save",
            "wait", "talk", "comply", "call", "call_911", "ask", "ask_questions", "ask_advice",
            "photograph", "report", "return", "apologize", "prove", "calm", "help", "follow", "peek",
        ]:
            for index, choice in enumerate(normalized):
                if _choice_matches(choice, keyword):
                    reason_tag = "prefer_safe" if (prefer_safe and not low_resources) else "generic_low_resource"
                    return index, f"{reason_tag}_choice:{keyword}", 0.5

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


def _choose_generic_inline(request: DecisionRequest, *, prefer_safe: bool = False) -> tuple[str | None, str | None, float]:
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

    if low_resources or prefer_safe:
        for keyword in [
            "leave", "walk", "observe", "watch", "decline", "refuse", "ignore", "save",
            "wait", "talk", "comply", "call", "call_911", "ask", "ask_questions", "ask_advice",
            "photograph", "report", "return", "apologize", "prove", "calm", "help", "follow", "peek",
        ]:
            for choice in choices:
                if _choice_matches(choice, keyword):
                    reason_tag = "prefer_safe" if (prefer_safe and not low_resources) else "generic_inline_low_resource"
                    return choice, f"{reason_tag}_choice:{keyword}", 0.42

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


# ==============================================================================
# EVENT YES/NO: SIMPLE YES EVENTS
# Events where ALL yes/no prompts should be answered "yes".
# ==============================================================================

_SIMPLE_YES_EVENTS = {
    # -- Storyline: Kyle --
    "storyline:kyle:stage0",            # "Do you ask if he's okay?"
    "storyline:kyle:stage1",            # "Do you listen?"
    "storyline:kyle:stage2",            # "Promise to keep his secret?"
    # -- Storyline: Martinez --
    "storyline:martinez:stage0",        # "Do you try to explain your situation?"
    "storyline:martinez:stage1",        # "Accept the coffee?"
    "storyline:martinez:stage2",        # "Take the card?"
    # -- Storyline: Suzy --
    "storyline:suzy:stage2",            # "Do you like it?"
    # -- Storyline: Grandma (stage 1 only) --
    "storyline:grandma:stage1",         # "Write down the recipe?"
    # -- Storyline: Lucky Dog --
    "storyline:lucky_dog:stage0",       # "Keep petting him?"
    "storyline:lucky_dog:stage2",       # "Throw the rock?"
    # -- Storyline: Dealer Past --
    "storyline:dealer_past:stage0",     # "Ask about the photo?"
    "storyline:dealer_past:stage1",     # "Pick it up?"
    "storyline:dealer_past:stage2",     # "Ask the Dealer about his past?"
    "storyline:dealer_past:stage4",     # "Accept his lesson?"
    # -- Storyline: Radio Signal --
    "storyline:radio_signal:stage0",    # "Write down the numbers?"
    "storyline:radio_signal:stage1",    # "Try to tune to the frequency?"
    "storyline:radio_signal:stage2",    # "Go inside?" + "Take the logbook?"
    # -- Storyline: Graveyard --
    "storyline:graveyard:stage0",       # "Walk through the cemetery?"
    "storyline:graveyard:stage1",       # "Talk to Edgar?"
    "storyline:graveyard:stage3",       # "Take the letter?"
    # -- Storyline: Carnival --
    "storyline:carnival:stage0",        # "Enter the carnival?"
    "storyline:carnival:stage1",        # "Ask if it gets better?"
    # -- Storyline: Lockbox --
    "storyline:lockbox:stage2",         # "Check out the apartment?"
    # -- Storyline: Tanya --
    "storyline:tanya:stage0",           # "Go inside?"
    # -- Storyline: Rosa --
    "storyline:rosa:stage0",            # "Spot her $6?"
    "storyline:rosa:stage1",            # "Offer to help?"
    # -- Storyline: Eli --
    "storyline:eli:stage0",             # "Step into the tent?"
    "storyline:eli:stage1",             # "Help him set up chairs?"
    "storyline:eli:stage2",             # "Stay and help before the storm?"
    # -- Storyline: Stuart (stage 0 only) --
    "storyline:stuart:stage0",          # "Are you interested?"
    # -- Day: Phil interrogation stages --
    "day:interrogation",                # "Do you? Know this?"
    "storyline:phil:stage0",
    "day:further_interrogation",        # "Did you? Read it?"
    "storyline:phil:stage1",
    "day:even_further_interrogation",   # "Are you? Gonna leave?"
    "storyline:phil:stage2",
    "day:final_interrogation",          # "Answer me."
    "storyline:phil:stage3",
    # -- Day: Animals --
    "day:stray_cat",                    # "Feed it some of your food?"
    "storyline:stray_cat:stage0",
    "day:three_legged_dog",             # "Take him in?"
    "day:opossum_in_trash",             # "Try to befriend the trash gremlin?"
    "day:sewer_rat",                    # "Offer it some food?"
    "day:garden_rabbit",                # "Take the rabbit with you?"
    "day:duck_army",                    # "Follow the duck parade?"
    "day:pigeon_mafia",                 # "Throw them some bread/money as tribute?"
    "day:crow_encounter",               # "Offer it some {item}?"
    "day:raccoon_raid",                 # "Try to catch it?"
    # -- Day: People --
    "day:whats_my_name",                # "What was that?"
    "day:the_mime",                     # "Do you applaud?"
    "storyline:mime:stage0",
    "day:the_photographer",             # "Allow the photoshoot?"
    "day:wrong_number",                 # "Reply anyway?"
    "day:found_phone",                  # "Try to return it to the owner?"
    "day:the_hitchhiker",               # "Pick her up?"
    "day:the_journalist",               # "Grant the interview?"
    "day:the_offer_refused",            # "Accept the VIP treatment?"
    "day:the_confession",               # "Listen to him?"
    "day:the_dying_dealer",             # "Visit him?"
    "day:autograph_request",            # "Play along?"
    "day:mysterious_package",           # "Open it?"
    "day:broken_atm",                   # "Take the money?"
    "day:friendly_drunk",               # "Keep it?"
    # -- Day: Wealth --
    "day:victoria_returns",             # "Shake her hand?"
    "storyline:victoria:stage1",
    "day:media_known_documentary",      # "Agree to the documentary?"
    "day:gas_station_hero_interview",   # "Do the interview?"
    "storyline:gas_station_hero:stage2",
    # -- Day: Surreal --
    "day:sock_puppet_therapist",        # "Talk to... Dr. Socksworth?"
    # -- Day: Items --
    "day:ritual_token_ceremony",        # "Use the Ritual Token?"
    "day:found_phone_call",             # "Call them?"
    "day:fake_flower_gift",             # "Give them the flower?"
    "day:suspicious_package_open",      # "Open it?"
    "day:stolen_watch_recognition",     # "Give it back?"
    "day:underwater_camera_photos",     # "Post found photos flyers?"
    "day:magic_acorn_planting",         # "Plant it?"
    "day:treasure_map_follow",          # "Follow it now?"
    "day:capture_fairy_release",        # "Let it go?"
    "day:mysterious_code_decode",       # "Work it out now?"
    "day:swamp_gold_attention",         # "Give it back?"
    # -- Day: Survival --
    "day:turn_to_god",                  # "Do you?"
    # -- Day: Companions --
    "day:patches_night_watch",          # "Take it?" / "Keep the kitten?"
    "day:companion_brings_friend",      # "Try to befriend the {friend}?"
    # -- Night events --
    "night:whats_my_favorite_animal",   # "Do you promise?"
    "night:giant_oyster_opening",       # "Open it?"
    "night:ocean_jetty",                # "Stay and fish with him?"
    "night:chase_the_third_rabbit",     # "Use the carrot to lure the rabbit?"
    "night:swamp_swim",                 # "Accept Earl's moonshine?"
    # -- Night: wander exploration (blank prompts -> explore) --
    "night:woodlands_path",
    "night:woodlands_field",
    "night:beach_stroll",
    "night:beach_bonfire",
    "night:beach_swim",
    "night:beach_dive",
    "night:swamp_stroll",
    "night:swamp_wade",
    "night:city_stroll",
    "night:city_park",
}


# ==============================================================================
# EVENT YES/NO: SIMPLE NO EVENTS
# Events where ALL yes/no prompts should be answered "no".
# ==============================================================================

_SIMPLE_NO_EVENTS = {
    # -- Storyline: Dr. Feelgood --
    "storyline:dr_feelgood:stage0",     # "Take the pill?"
    # -- Storyline: Sleep Paralysis --
    "storyline:sleep_paralysis:stage2", # "Do you accept the shadow's offer?"
    # -- Storyline: Mime --
    "storyline:mime:stage2",            # "Ask who 'they' are?"
    # -- Storyline: Stuart (stage 2) --
    "storyline:stuart:stage2",          # "Hold the box for Stuart?"
    # -- Storyline: Carnival (stage 2) --
    "storyline:carnival:stage2",        # "Pay $100 to spin?"
    # -- Day: Dark --
    "day:blood_moon_bargain",           # "Accept the blood moon bargain?"
    "day:midnight_visitor",             # "Accept the devil's offer?"
    "day:organ_harvester",              # "Sell your kidney?"
    "day:drug_dealer_encounter",        # "Buy the drugs? ($500)"
    "day:shoulder_painkiller_addiction", # "Buy the painkillers? ($100)"
    "storyline:painkiller:stage1",
    "day:painkiller_dealer_returns",    # "Buy more pills? ($150)"
    "day:cocaine_temptation",           # All prompts -> no
    "day:the_relapse",                  # "Go back to the tables?"
    "day:phone_scam_call",              # "Hang up?" -> no (stay on the line)
    "day:tax_man",                      # "Lie and say yes?" -> no
    # -- Day: People --
    "day:homeless_network",             # "Pay him $50 for the info?"
    "day:the_prophet",                  # "Pay $20 for a prophecy?"
    "day:old_friend_recognition",       # "Tell them the truth?"
    "day:the_final_temptation",         # "Accept his offer?"
    # -- Day: Survival --
    "day:threw_out_old_photo",          # "Throw it away?" -> no (keep it)
}


# ==============================================================================
# EVENT YES/NO: CONDITIONAL HANDLERS
# These need game state to decide.
# Signature: (request, plan, prompt_lower, recent, cost, balance, health, sanity)
# ==============================================================================


def _yn_betsy_moo(r, p, prompt, recent, cost, bal, hp, san):
    """Betsy arc: hungry_cow, starving_cow, cow_army. Pay if we have money."""
    if any(m in recent for m in ("army", "hundred thousand", "100,000",
                                  "rest of the cows", "flooded with cows")):
        # Cow army takes ALL your money — only accept at low stakes where
        # losing everything isn't run-ending.
        answer = "yes" if 0 < bal <= 500 else "no"
        return answer, _yes_no_trace(r, p, answer, "betsy_army_survival", 0.98)
    answer = "yes" if bal > 0 else "no"
    if "tractor" in recent:
        return answer, _yes_no_trace(r, p, answer, "betsy_tractor_survival", 0.96)
    return answer, _yes_no_trace(r, p, answer, "betsy_hungry_survival", 0.94)


def _yn_kyle_stage3(r, p, prompt, recent, cost, bal, hp, san):
    """Kyle stage 3: No if loyalty bonus, yes otherwise."""
    if "loyalty bonus" in recent:
        return "no", _yes_no_trace(r, p, "no", "kyle_loyalty_bonus_refusal", 0.8)
    return "yes", _yes_no_trace(r, p, "yes", "kyle_take_money", 0.82)


def _yn_kyle_stage4(r, p, prompt, recent, cost, bal, hp, san):
    """Kyle stage 4: 'Stand up for Kyle?' -> yes, 'Do you run?' -> no."""
    if "stand up" in prompt or "kyle" in prompt:
        return "yes", _yes_no_trace(r, p, "yes", "kyle_stand_up", 0.82)
    return "no", _yes_no_trace(r, p, "no", "kyle_dont_run", 0.8)


def _yn_grandma_stage0(r, p, prompt, recent, cost, bal, hp, san):
    """Grandma stage 0: 'Call the number?' -> yes, 'Correct her?' -> no."""
    if "correct" in prompt:
        return "no", _yes_no_trace(r, p, "no", "grandma_dont_correct", 0.82)
    return "yes", _yes_no_trace(r, p, "yes", "grandma_call_number", 0.82)


def _yn_grandma_stage2(r, p, prompt, recent, cost, bal, hp, san):
    """Grandma stage 2: Drive to hospital if affordable."""
    c = cost if cost is not None else 100
    answer = "yes" if bal >= c + 40 else "no"
    return answer, _yes_no_trace(r, p, answer, "grandma_hospital_budget_gate", 0.76)


def _yn_dr_feelgood_stage1(r, p, prompt, recent, cost, bal, hp, san):
    """Dr. Feelgood stage 1/2: All prompts -> no."""
    return "no", _yes_no_trace(r, p, "no", "feelgood_refuse_pills", 0.82)


def _yn_dr_feelgood_stage3(r, p, prompt, recent, cost, bal, hp, san):
    """Dr. Feelgood stage 3: Refuse delivery."""
    return "no", _yes_no_trace(r, p, "no", "feelgood_refuse_delivery", 0.8)


def _yn_casino_hitman(r, p, prompt, recent, cost, bal, hp, san):
    """Casino hitman: Pay $200k if we can afford."""
    answer = "yes" if bal >= 200000 else "no"
    return answer, _yes_no_trace(r, p, answer, "casino_hitman_buyout", 0.9)


def _yn_desperate_gambler(r, p, prompt, recent, cost, bal, hp, san):
    """Desperate gambler: Give money if affordable."""
    answer = "yes" if bal >= 100 else "no"
    return answer, _yes_no_trace(r, p, answer, "desperate_gambler_charity", 0.74)


def _yn_city_streets(r, p, prompt, recent, cost, bal, hp, san):
    """Night city streets: Buy the gyro if cheap food helps."""
    answer = "yes" if bal >= 5 and (hp < 92 or san < 72) else "no"
    return answer, _yes_no_trace(r, p, answer, "gyro_health_gate", 0.72)


def _yn_beach_boardwalk(r, p, prompt, recent, cost, bal, hp, san):
    """Night beach boardwalk: Buy fried dough if stats need it."""
    answer = "yes" if bal >= 5 and (hp < 92 or san < 72) else "no"
    return answer, _yes_no_trace(r, p, answer, "fried_dough_health_gate", 0.72)


def _yn_street_musician(r, p, prompt, recent, cost, bal, hp, san):
    """Street musician: give money if affordable and sanity low."""
    answer = "yes" if bal >= 20 and san < 85 else "no"
    return answer, _yes_no_trace(r, p, answer, "street_musician_relief_gate", 0.74)


def _yn_forgotten_birthday(r, p, prompt, recent, cost, bal, hp, san):
    """Forgotten birthday: buy cupcake if sanity low."""
    answer = "yes" if bal >= 20 and san < 55 else "no"
    return answer, _yes_no_trace(r, p, answer, "cupcake_sanity_gate", 0.7)


def _yn_book_club(r, p, prompt, recent, cost, bal, hp, san):
    """Book club: attend if sanity low."""
    answer = "yes" if san < 55 else "no"
    return answer, _yes_no_trace(r, p, answer, "book_club_sanity_gate", 0.68)


def _yn_the_offer(r, p, prompt, recent, cost, bal, hp, san):
    """The offer: double money -> yes, ominous or vague -> no."""
    if "double whatever you have" in recent:
        return "yes", _yes_no_trace(r, p, "yes", "double_money_offer_accept", 0.74)
    return "no", _yes_no_trace(r, p, "no", "unknown_offer_cautious_refusal", 0.6)


def _yn_gift_wrap(r, p, prompt, recent, cost, bal, hp, san):
    """Convenience store gift wrap for dealer happiness."""
    if "gift" not in prompt and "wrap" not in prompt:
        return "yes", _yes_no_trace(r, p, "yes", "shop_generic_yes", 0.6)
    dealer_happiness = int(r.game_state.get("dealer_happiness", 50) or 50)
    plan_goal = (p.goal if p else "")
    in_emergency = (
        plan_goal in {"survive_emergency", "acquire_car", "contain_debt_escalation"}
        or hp < 45 or san < 20 or not r.game_state.get("has_car", True)
    )
    answer = (
        "yes"
        if (
            bal >= GIFT_WRAP_MIN_BALANCE
            and dealer_happiness < GIFT_WRAP_HAPPINESS_THRESHOLD
            and not in_emergency
        )
        else "no"
    )
    return answer, _yes_no_trace(r, p, answer, "gift_wrap_happiness_gate", 0.8)


def _yn_witch_doctor(r, p, prompt, recent, cost, bal, hp, san):
    """Witch doctor: accept healing and soup."""
    return "yes", _yes_no_trace(r, p, "yes", "witch_heal_accept", 0.96)


def _yn_workbench(r, p, prompt, recent, cost, bal, hp, san):
    """Car workbench: confirm crafting."""
    return "yes", _yes_no_trace(r, p, "yes", "workbench_craft_confirm", 0.9)


def _yn_investment_pitch(r, p, prompt, recent, cost, bal, hp, san):
    """Investment pitch: don't give him $100."""
    return "no", _yes_no_trace(r, p, "no", "investment_pitch_refusal", 0.84)


def _yn_stray_cat_sick(r, p, prompt, recent, cost, bal, hp, san):
    """Stray cat sick: take to vet if affordable."""
    c = cost if cost is not None else 200
    answer = "yes" if bal >= c + 40 else "no"
    return answer, _yes_no_trace(r, p, answer, "vet_cost_gate", 0.78)


def _yn_stuart_stage1(r, p, prompt, recent, cost, bal, hp, san):
    """Stuart stage 1: buy for $50 if affordable."""
    c = cost if cost is not None else 50
    answer = "yes" if bal >= c + 50 else "no"
    return answer, _yes_no_trace(r, p, answer, "stuart_buy_budget_gate", 0.72)


def _yn_stuart_stage3(r, p, prompt, recent, cost, bal, hp, san):
    """Stuart stage 3: tell truth yes, defend if healthy."""
    if "defend" in prompt:
        answer = "yes" if hp >= 50 else "no"
        return answer, _yes_no_trace(r, p, answer, "stuart_defend_health_gate", 0.72)
    return "yes", _yes_no_trace(r, p, "yes", "stuart_tell_truth", 0.82)


def _yn_food_truck_festival(r, p, prompt, recent, cost, bal, hp, san):
    """Food truck: feast if affordable and need stats."""
    c = cost if cost is not None else 25
    answer = "yes" if bal >= c + 50 and (hp < 90 or san < 70) else "no"
    return answer, _yes_no_trace(r, p, answer, "food_truck_health_gate", 0.72)


def _yn_fancy_restaurant(r, p, prompt, recent, cost, bal, hp, san):
    """Fancy restaurant: only if really need stats and can afford."""
    c = cost if cost is not None else 200
    answer = "yes" if bal >= c + 200 and (hp < 60 or san < 45) else "no"
    return answer, _yes_no_trace(r, p, answer, "fancy_restaurant_budget_gate", 0.68)


def _yn_parking_ticket(r, p, prompt, recent, cost, bal, hp, san):
    """Pay parking ticket if affordable."""
    c = cost if cost is not None else 75
    answer = "yes" if bal >= c + 100 else "no"
    return answer, _yes_no_trace(r, p, answer, "parking_ticket_budget_gate", 0.7)


def _yn_parking_lot_poker(r, p, prompt, recent, cost, bal, hp, san):
    """Parking lot poker: skip when preserving run."""
    answer = "no" if bal >= 1000 else "yes"
    return answer, _yes_no_trace(r, p, answer, "poker_risk_gate", 0.6)


def _yn_deck_of_cards_game(r, p, prompt, recent, cost, bal, hp, san):
    """Street card game: skip when preserving run."""
    answer = "no" if bal >= 1000 else "yes"
    return answer, _yes_no_trace(r, p, answer, "street_card_risk_gate", 0.6)


def _yn_social_encounter(r, p, prompt, recent, cost, bal, hp, san):
    """Social encounter: sell Necronomicon if offered $2000+."""
    if "necronomicon" in prompt or "necronomicon" in recent:
        return "yes", _yes_no_trace(r, p, "yes", "sell_necronomicon", 0.78)
    return "yes", _yes_no_trace(r, p, "yes", "social_encounter_yes", 0.6)


def _yn_bottle_of_tomorrow(r, p, prompt, recent, cost, bal, hp, san):
    """Bottle of tomorrow: drink if hurt, skip if healthy."""
    answer = "yes" if hp < 50 or san < 30 else "no"
    return answer, _yes_no_trace(r, p, answer, "bottle_of_tomorrow_gate", 0.6)


def _yn_rex_stage1(r, p, prompt, recent, cost, bal, hp, san):
    """Rex stage 1: Lend $50 if affordable."""
    answer = "yes" if bal >= 100 else "no"
    return answer, _yes_no_trace(r, p, answer, "rex_lend_budget_gate", 0.7)


def _yn_rosa_stage2(r, p, prompt, recent, cost, bal, hp, san):
    """Rosa stage 2: Cover $24 locker fee if affordable."""
    answer = "yes" if bal >= 50 else "no"
    return answer, _yes_no_trace(r, p, answer, "rosa_locker_fee_gate", 0.7)


def _yn_jameson_stage1(r, p, prompt, recent, cost, bal, hp, san):
    """Jameson stage 1: 'Suggest Tom' -> yes, 'Give $100' -> no."""
    if "$100" in prompt or "vet" in prompt:
        return "no", _yes_no_trace(r, p, "no", "jameson_vet_bill_refusal", 0.82)
    return "yes", _yes_no_trace(r, p, "yes", "jameson_suggest_tom", 0.88)


def _yn_surplus_gate(threshold, min_remain, reason):
    """Factory for surplus-gated handlers."""
    def handler(r, p, prompt, recent, cost, bal, hp, san):
        c = cost if cost is not None else threshold
        answer = "yes" if bal - int(c) >= min_remain else "no"
        return answer, _yes_no_trace(r, p, answer, reason, 0.72)
    return handler


# -- Conditional dispatch table --

_EVENT_YES_NO = {
    # Betsy arc (all cow events + storyline labels)
    "day:hungry_cow":                  _yn_betsy_moo,
    "day:starving_cow":                _yn_betsy_moo,
    "day:cow_army":                    _yn_betsy_moo,
    "storyline:betsy:stage0":          _yn_betsy_moo,
    "storyline:betsy:stage1":          _yn_betsy_moo,
    "storyline:betsy:stage2":          _yn_betsy_moo,
    # Kyle arc
    "storyline:kyle:stage3":           _yn_kyle_stage3,
    "storyline:kyle:stage4":           _yn_kyle_stage4,
    # Grandma
    "storyline:grandma:stage0":        _yn_grandma_stage0,
    "storyline:grandma:stage2":        _yn_grandma_stage2,
    # Dr. Feelgood
    "storyline:dr_feelgood:stage1":    _yn_dr_feelgood_stage1,
    "storyline:dr_feelgood:stage2":    _yn_dr_feelgood_stage1,
    "storyline:dr_feelgood:stage3":    _yn_dr_feelgood_stage3,
    # Casino
    "day:casino_hitman":               _yn_casino_hitman,
    # Money/charity
    "day:the_desperate_gambler":       _yn_desperate_gambler,
    "day:investment_pitch":            _yn_investment_pitch,
    "day:street_musician":             _yn_street_musician,
    "day:forgotten_birthday":          _yn_forgotten_birthday,
    "day:book_club_invite":            _yn_book_club,
    "day:charity_opportunity":         _yn_surplus_gate(100, 2500, "charity_surplus_gate"),
    "day:food_truck_festival":         _yn_food_truck_festival,
    "day:fancy_restaurant_mistake":    _yn_fancy_restaurant,
    "day:parking_ticket":              _yn_parking_ticket,
    "day:parking_lot_poker":           _yn_parking_lot_poker,
    "day:deck_of_cards_street_game":   _yn_deck_of_cards_game,
    # Vehicles
    "day:damaged_exhaust_fixed":       lambda r, p, pr, rc, c, b, h, s: (
        ("yes" if b >= 100 else "no"),
        _yes_no_trace(r, p, "yes" if b >= 100 else "no", "exhaust_repair_budget", 0.92)),
    "day:fuel_leak_fixed":             lambda r, p, pr, rc, c, b, h, s: (
        ("yes" if b >= 150 else "no"),
        _yes_no_trace(r, p, "yes" if b >= 150 else "no", "fuel_leak_repair_budget", 0.92)),
    "day:booted_car_impound":          _yn_surplus_gate(800, 700, "car_recovery_gate"),
    "day:unpaid_ticket_consequence":   _yn_surplus_gate(500, 500, "fine_reserve_gate"),
    "day:unpaid_tickets_boot":         _yn_surplus_gate(300, 500, "boot_reserve_gate"),
    # The offer
    "day:the_offer":                   _yn_the_offer,
    # Companion/animal health
    "day:stray_cat_sick":              _yn_stray_cat_sick,
    "storyline:stray_cat:stage1":      _yn_stray_cat_sick,
    # Social
    "day:social_encounter":            _yn_social_encounter,
    # Night
    "night:city_streets":              _yn_city_streets,
    "night:beach_boardwalk":           _yn_beach_boardwalk,
    # Locations
    "location:shop:convenience_store": _yn_gift_wrap,
    "location:doctor:witch":           _yn_witch_doctor,
    "location:shop:car_workbench":     _yn_workbench,
    "met:Car Workbench":               _yn_workbench,
    # Stuart
    "storyline:stuart:stage1":         _yn_stuart_stage1,
    "storyline:stuart:stage3":         _yn_stuart_stage3,
    # Rex, Rosa
    "storyline:rex:stage1":            _yn_rex_stage1,
    "storyline:rosa:stage2":           _yn_rosa_stage2,
    # Jameson (override simple-yes for conditional multi-prompt)
    "storyline:jameson:stage1":        _yn_jameson_stage1,
    # Items
    "day:swamp_gold_attention":        lambda r, p, pr, rc, c, b, h, s: (
        "yes", _yes_no_trace(r, p, "yes", "swamp_gold_cooperate", 0.74)),
    "day:bottle_of_tomorrow_use":      _yn_bottle_of_tomorrow,
    # Bodyguard
    "day:the_bodyguard_offer":         lambda r, p, pr, rc, c, b, h, s: (
        ("yes" if b >= 20000 else "no"),
        _yes_no_trace(r, p, "yes" if b >= 20000 else "no", "bodyguard_budget_gate", 0.75)),
}


# ==============================================================================
# EVENT OPTION HANDLERS
# ==============================================================================


def _opt_madness_quiz(r, p, options, normalized, bal, hp):
    """Madness confrontation quiz: 3 questions during the ending."""
    recent = str(r.metadata.get("recent_lower", "") or "")
    # Q3: "would you walk away?" / "first walked" + "fifty dollars"
    if ("walk away" in recent or "first walked" in recent) and "fifty dollars" in recent and len(options) == 4:
        for idx, opt in enumerate(normalized):
            if "yes" in opt or "walk away" in opt:
                return options[idx], _option_trace(r, p, options, idx, "madness_q3_best_answer", 0.99)
        return options[0], _option_trace(r, p, options, 0, "madness_q3_pick_1", 0.99)
    # Q2: "What do you see when you look at the Dealer?"
    if "what do you see" in recent and "dealer" in recent and len(options) == 4:
        for idx, opt in enumerate(normalized):
            if "just a man" in opt or "nothing" in opt or "doing a job" in opt:
                return options[idx], _option_trace(r, p, options, idx, "madness_q2_best_answer", 0.99)
        return options[2], _option_trace(r, p, options, 2, "madness_q2_pick_3", 0.99)
    # Q1: "Why do you gamble?"
    if "why do you gamble" in recent and len(options) == 4:
        for idx, opt in enumerate(normalized):
            if "don't know" in opt or "anymore" in opt:
                return options[idx], _option_trace(r, p, options, idx, "madness_q1_best_answer", 0.99)
        return options[3], _option_trace(r, p, options, 3, "madness_q1_pick_4", 0.99)
    return None, None


def _opt_millionaire_menu(r, p, options, normalized, bal, hp):
    """Millionaire ending: mechanic goodbye or airport."""
    millionaire_labels = {opt.label.lower(): idx for idx, opt in enumerate(options)}
    is_millionaire = (
        any("drive to the airport" in lbl for lbl in millionaire_labels)
        and any(
            keyword in lbl
            for keyword in ("tom", "frank", "oswald", "mechanic")
            for lbl in millionaire_labels
        )
    )
    if not is_millionaire:
        return None, None
    chosen_mechanic = str(r.game_state.get("chosen_mechanic") or "")
    for pref in MILLIONAIRE_ENDING_PREFERENCE:
        if pref == "mechanic" and chosen_mechanic:
            for lbl, idx in millionaire_labels.items():
                if chosen_mechanic.lower() in lbl:
                    return options[idx], _option_trace(r, p, options, idx, f"millionaire_mechanic_ending:{chosen_mechanic}", 0.8)
        elif pref == "mechanic":
            for lbl, idx in millionaire_labels.items():
                if any(name in lbl for name in ("tom", "frank", "oswald")):
                    return options[idx], _option_trace(r, p, options, idx, "millionaire_mechanic_ending_any", 0.8)
        elif pref == "airport":
            for lbl, idx in millionaire_labels.items():
                if "airport" in lbl:
                    return options[idx], _option_trace(r, p, options, idx, "millionaire_airport_ending", 0.8)
    return None, None


def _opt_by_keyword(keyword, reason, confidence=0.8):
    """Factory: picks first option containing keyword."""
    def handler(r, p, options, normalized, bal, hp):
        for i, opt in enumerate(normalized):
            if keyword in opt:
                return options[i], _option_trace(r, p, options, i, reason, confidence)
        return options[0], _option_trace(r, p, options, 0, f"{reason}_kw_miss", 0.5)
    return handler


def _opt_safe_default(reason, confidence=0.8):
    """Factory: picks the safest option."""
    def handler(r, p, options, normalized, bal, hp):
        idx, r_reason = _pick_safe_option(options, normalized, reason)
        return options[idx], _option_trace(r, p, options, idx, r_reason, confidence)
    return handler


def _opt_loan_shark_visit(r, p, options, normalized, bal, hp):
    """Loan shark: pay if rich, beg otherwise."""
    for i, opt in enumerate(normalized):
        if "pay" in opt and bal >= 50000:
            return options[i], _option_trace(r, p, options, i, "loan_shark_pay_now", 0.8)
    for i, opt in enumerate(normalized):
        if "beg" in opt or "time" in opt:
            return options[i], _option_trace(r, p, options, i, "loan_shark_beg_time", 0.8)
    return options[0], _option_trace(r, p, options, 0, "loan_shark_first_option", 0.6)


def _opt_cancer_diagnosis(r, p, options, normalized, bal, hp):
    """Cancer: pay for treatment if possible."""
    for i, opt in enumerate(normalized):
        if "pay" in opt and bal >= 5000:
            return options[i], _option_trace(r, p, options, i, "cancer_pay_treatment", 0.8)
    for i, opt in enumerate(normalized):
        if "refuse" in opt:
            return options[i], _option_trace(r, p, options, i, "cancer_refuse_treatment", 0.8)
    return options[0], _option_trace(r, p, options, 0, "cancer_first_option", 0.6)


def _opt_jameson_stage2(r, p, options, normalized, bal, hp):
    """Jameson stage 2: help if healthy, honk horn otherwise."""
    for i, opt in enumerate(normalized):
        if ("help" in opt or "charge" in opt) and hp >= 65:
            return options[i], _option_trace(r, p, options, i, "jameson_help", 0.8)
    for i, opt in enumerate(normalized):
        if "honk" in opt or "horn" in opt:
            return options[i], _option_trace(r, p, options, i, "jameson_horn", 0.8)
    return options[0], _option_trace(r, p, options, 0, "jameson_first_option", 0.6)


# -- Option dispatch table --

_EVENT_OPTION = {
    # -- Endings --
    "day:madness_confrontation":           _opt_madness_quiz,
    "location:shop:airport":               _opt_millionaire_menu,
    # -- Day: Casino --
    "day:casino_security":                 _opt_by_keyword("flee", "casino_security_flee", 0.8),
    # -- Day: Dark --
    "day:loan_shark_visit":                _opt_loan_shark_visit,
    "day:withdrawal_nightmare":            _opt_by_keyword("ride", "ride_it_out", 0.8),
    "day:casino_overdose":                 _opt_by_keyword("call", "call_for_help", 0.8),
    "day:cancer_diagnosis":                _opt_cancer_diagnosis,
    "day:the_bridge_call":                 _opt_by_keyword("call", "bridge_call_someone", 0.8),
    "day:back_alley_shortcut":             _opt_safe_default("alley_safe", 0.8),
    "day:gas_station_robbery":             _opt_by_keyword("hide", "gas_station_hide", 0.85),
    "storyline:gas_station_hero:stage0":   _opt_by_keyword("hide", "gas_station_hide", 0.85),
    "day:drug_dealer_encounter":           _opt_by_keyword("wrong", "wrong_person", 0.8),
    "day:bridge_contemplation":            _opt_by_keyword("stay", "stay_meets_bridge_angel", 0.8),
    "storyline:bridge_angel:stage0":       _opt_by_keyword("stay", "stay_meets_bridge_angel", 0.8),
    "day:car_explosion":                   _opt_by_keyword("bail", "bail_out", 0.8),
    "day:fuel_leak_fire":                  _opt_safe_default("fuel_leak_safe", 0.8),
    "day:cocaine_temptation":              _opt_by_keyword("sell", "sell_cocaine", 0.8),
    "day:voodoo_doll_temptation":          _opt_by_keyword("burn", "burn_voodoo_doll", 0.8),
    # -- Day: Animals --
    "day:squirrel_invasion":               _opt_by_keyword("keep", "squirrel_keep", 0.7),
    "day:stray_cat":                       _opt_by_keyword("cat", "stray_cat_pick_cat", 0.7),
    "storyline:stray_cat:stage0":          _opt_by_keyword("cat", "stray_cat_pick_cat", 0.7),
    "day:wild_rat_attack":                 _opt_by_keyword("kick", "kick_rat_away", 0.8),
    "day:slingshot_bird_hunt":             _opt_by_keyword("scare", "scare_bird", 0.7),
    "day:snare_trap_catch":                _opt_by_keyword("free", "free_animal", 0.7),
    "day:binocular_scope_discovery":       _opt_by_keyword("help", "help_scope", 0.7),
    "day:sentient_sandwich":               _opt_by_keyword("apologize", "sandwich_apologize", 0.8),
    # -- Day: Companions --
    "day:mr_pecks_treasure":               _opt_by_keyword("return", "return_treasure", 0.8),
    "day:rusty_midnight_heist":            _opt_by_keyword("return", "return_cash", 0.8),
    "day:companion_sick_day":              _opt_by_keyword("help", "help_sick_companion", 0.8),
    "day:companion_rivalry":               _opt_by_keyword("break", "break_up_fight", 0.7),
    "day:companion_food_crisis":           _opt_by_keyword("share", "share_food", 0.7),
    "day:companion_lost_adventure":        _opt_by_keyword("search", "search_for_companion", 0.8),
    # -- Day: People --
    "day:coin_flip_stranger":              _opt_by_keyword("head", "coin_flip_heads", 0.5),
    "day:street_performer_duel":           _opt_by_keyword("neither", "choose_neither", 0.7),
    # -- Day: Wealth --
    "day:investment_opportunity":           _opt_by_keyword("help", "help_investment", 0.7),
    "day:reporters_found_you":             _opt_by_keyword("humble", "choose_humble", 0.7),
    "day:old_rival_encounter":             _opt_by_keyword("ask", "ask_for_help", 0.7),
    # -- Day: Surreal --
    "day:time_loop":                       _opt_by_keyword("ignore", "ignore_phone_time_loop", 0.8),
    "day:the_collector":                   _opt_by_keyword("not interested", "not_interested", 0.8),
    "storyline:collector:stage0":          _opt_by_keyword("not interested", "not_interested", 0.8),
    "day:dance_battle":                    _opt_by_keyword("moonwalk", "moonwalk", 0.7),
    # -- Day: Items --
    "day:blank_check_opportunity":         _opt_by_keyword("leave", "blank_check_leave", 0.7),
    # -- Day: Storylines --
    "day:hermit_trail_discovery":          _opt_by_keyword("follow", "hermit_follow", 0.7),
    "day:midnight_radio_broadcast":        _opt_by_keyword("record", "radio_record", 0.7),
    "day:junkyard_artisan_meet":           _opt_by_keyword("learn", "junkyard_learn", 0.7),
    # -- Storyline stages --
    "storyline:lucky_dog:stage1":          _opt_by_keyword("prove", "lucky_dog_prove_it", 0.8),
    "storyline:lockbox:stage0":            _opt_by_keyword("try", "lockbox_try_combination", 0.8),
    "storyline:lockbox:stage1":            _opt_by_keyword("try", "lockbox_try_again", 0.8),
    "storyline:rex:stage2":                _opt_by_keyword("need", "rex_need_money", 0.7),
    "storyline:dr_feelgood:stage3":        _opt_by_keyword("walk", "pill_menu_cold_turkey", 0.8),
    "storyline:jameson:stage2":            _opt_jameson_stage2,
    # -- Car events --
    "day:nail_in_tire":                    _opt_safe_default("nail_in_tire_safe", 0.7),
    # -- Night events --
    "night:city_streets":                  _opt_safe_default("city_streets_safe", 0.7),
    "night:city_stroll":                   _opt_safe_default("city_stroll_safe", 0.7),
    "night:city_park":                     _opt_safe_default("city_park_safe", 0.7),
    "night:beach_bonfire":                 _opt_by_keyword("join", "beach_bonfire_join", 0.7),
    "night:beach_swim":                    _opt_safe_default("beach_swim_safe", 0.7),
    "night:beach_dive":                    _opt_safe_default("beach_dive_safe", 0.7),
    "night:swamp_swim":                    _opt_safe_default("swamp_swim_safe", 0.7),
    "night:swamp_wade":                    _opt_safe_default("swamp_wade_safe", 0.7),
    "night:swamp_stroll":                  _opt_by_keyword("wait", "swamp_wait", 0.7),
}


# ==============================================================================
# EVENT INLINE CHOICE HANDLERS
# ==============================================================================


def _inline_companion_sick(r, p, prompt, recent, bal, hp, rank, choices, choice_set, inventory):
    """Companion sick day: pay for vet if affordable, use item, or rest."""
    if bal >= 50:
        return "2", _inline_trace(r, p, "2", "companion_sick_pay", 0.84)
    if "cough drops" in inventory:
        return "1", _inline_trace(r, p, "1", "companion_sick_item", 0.82)
    return "4", _inline_trace(r, p, "4", "companion_sick_rest", 0.8)


def _inline_companion_hungry(r, p, prompt, recent, bal, hp, rank, choices, choice_set, inventory):
    """Morning companion hunger: feed if we have money or companions unhappy."""
    companion_runaway_risk = int(r.game_state.get("companion_runaway_risk_count", 0) or 0)
    low_happiness = int(r.game_state.get("companion_low_happiness_count", 0) or 0)
    urgent = companion_runaway_risk > 0 or low_happiness > 0
    chosen = "3" if (bal >= 20 or urgent) else "4"
    return chosen, _inline_trace(r, p, chosen, "hungry_companions_gate", 0.82)


def _inline_swamp_nectar(r, p, prompt, recent, bal, hp, rank, choices, choice_set, inventory):
    """Swamp nectar: save if high rank, drink otherwise."""
    chosen = "save" if rank >= 2 else "drink"
    return chosen, _inline_trace(r, p, chosen, "swamp_nectar_choice", 0.8)


def _inline_pull_burn(r, p, prompt, recent, bal, hp, rank, choices, choice_set, inventory):
    """Pull/burn choice: burn if we have fire source."""
    chosen = "burn" if any(item in inventory for item in {"lighter", "matches", "road flares"}) else "pull"
    return chosen, _inline_trace(r, p, chosen, "fire_source_gate", 0.8)


def _inline_pet_feed_ignore(r, p, prompt, recent, bal, hp, rank, choices, choice_set, inventory):
    """Pet/feed/ignore: feed if we have food."""
    chosen = "feed" if "can of tuna" in inventory else "pet"
    return chosen, _inline_trace(r, p, chosen, "pet_or_feed_gate", 0.8)


def _inline_woodland_spring(r, p, prompt, recent, bal, hp, rank, choices, choice_set, inventory):
    """Woodland spring: drink if hurt, bottle if need water."""
    chosen = "drink" if hp < 55 else ("bottle" if "water bottles" not in inventory else "wash")
    return chosen, _inline_trace(r, p, chosen, "woodland_spring_choice", 0.8)


def _inline_favorite_color(r, p, prompt, recent, bal, hp, rank, choices, choice_set, inventory):
    return "blue", _inline_trace(r, p, "blue", "favorite_color_default", 0.85)


def _inline_favorite_animal(r, p, prompt, recent, bal, hp, rank, choices, choice_set, inventory):
    return "dog", _inline_trace(r, p, "dog", "favorite_animal_default", 0.85)


# -- Choice-set handlers: match on the exact set of choices presented --
# Stable because changing a choice label naturally invalidates the old match.

_INLINE_SET_HANDLERS = {
    # Road adventure
    frozenset({"stop", "honk", "drive_past"}): ("stop", "road_stop_hitchhiker"),
    frozenset({"drop_her_off", "give_money", "offer_food", "talk_more"}): ("give_money", "road_give_money_reward"),
    frozenset({"touch_stone", "pray", "leave_offering", "read_symbols", "walk_away"}): ("pray", "shrine_pray_free_heal"),
    frozenset({"help", "sell_water", "entertain", "rob", "ignore"}): ("help", "road_help_caravan"),
    frozenset({"stop", "toss_food", "follow", "drive_past"}): ("stop", "road_stop_animal"),
    frozenset({"double", "walk"}): ("walk", "road_gamble_walk_preserve"),
    frozenset({"again", "leave"}): ("leave", "road_gamble_leave_with_winnings"),
    # Woodlands adventure
    frozenset({"enter", "bet", "observe"}): ("enter", "woodlands_enter_competition"),
    frozenset({"track", "trap", "climb"}): ("track", "woodlands_track_best"),
    frozenset({"rush", "wait", "sabotage"}): ("wait", "woodlands_wait_patience"),
    frozenset({"fight", "flee", "offer", "submit"}): ("offer", "woodlands_boss_offer_safe"),
    frozenset({"eyes", "dodge", "dead"}): ("eyes", "woodlands_eyes_staredown"),
    frozenset({"river", "cliff", "brambles"}): ("river", "woodlands_river_escape"),
    frozenset({"knock", "peek", "leave"}): ("knock", "woodlands_knock_witch"),
    frozenset({"memory", "year", "favor"}): ("favor", "woodlands_witch_favor_best"),
    # Swamp adventure
    frozenset({"around", "wait"}): ("wait", "swamp_wait_out_event"),
    frozenset({"race", "bet", "watch"}): ("bet", "swamp_bet_on_race"),
    frozenset({"lettuce", "yelling", "poking"}): ("lettuce", "swamp_lettuce_train"),
    frozenset({"cheer", "pray", "throw"}): ("cheer", "swamp_cheer_turtle"),
    frozenset({"fight", "bribe", "riddle", "run"}): ("riddle", "swamp_troll_riddle_safest"),
    frozenset({"kneecaps", "climb", "distract"}): ("distract", "swamp_troll_distract"),
    frozenset({"free", "keep", "negotiate", "ignore"}): ("free", "fairy_free_for_wish"),
    frozenset({"money", "luck", "health", "item", "info"}): ("health", "fairy_wish_health"),
    frozenset({"money", "luck", "health"}): ("health", "fairy_wish_health_simple"),
    frozenset({"kiss", "talk", "run", "insult"}): ("talk", "mermaid_talk_safe"),
    frozenset({"luck", "love", "revenge"}): ("luck", "luck_preference"),
    # Beach adventure
    frozenset({"tough", "beach"}): ("beach", "beach_pick"),
    frozenset({"wrestle", "bet", "watch", "nope"}): ("bet", "beach_gator_bet"),
    frozenset({"circle", "charge", "taunt"}): ("circle", "beach_gator_circle_safe"),
    frozenset({"jaw_clamp", "roll", "escape"}): ("escape", "beach_gator_escape"),
    frozenset({"join", "bet", "watch", "nope"}): ("join", "beach_volleyball_join"),
    frozenset({"bump", "spike", "dive"}): ("spike", "beach_volleyball_spike"),
    frozenset({"block", "set", "cheer"}): ("block", "beach_volleyball_block"),
    frozenset({"trust_grandma", "go_hero", "teamwork"}): ("teamwork", "beach_volleyball_teamwork"),
    frozenset({"classic_castle", "modern", "weird", "huge"}): ("huge", "sandcastle_huge_best"),
    frozenset({"enter", "judge", "sabotage", "watch"}): ("judge", "sandcastle_judge_cashout"),
    frozenset({"compete", "bet", "sabotage", "watch"}): ("compete", "beach_fishing_compete"),
    frozenset({"grouper", "tuna", "marlin"}): ("marlin", "fishing_marlin_biggest"),
    frozenset({"freeze", "splash", "swim"}): ("splash", "alligator_splash_scares"),
    # Underwater adventure
    frozenset({"open", "shake", "throw_back", "sell"}): ("open", "underwater_open_clam"),
    frozenset({"race", "bet", "catch_own", "watch"}): ("catch_own", "underwater_catch_own_crab"),
    frozenset({"yelling", "food", "poking", "singing"}): ("singing", "underwater_sing_to_crab"),
    # City adventure
    frozenset({"join", "observe", "sabotage", "leave"}): ("join", "city_join_ritual"),
    frozenset({"wealth", "love", "power", "peace"}): ("peace", "city_ritual_peace_safest"),
    # Generic scene choices
    frozenset({"force", "take"}): ("force", "force_opening"),
    frozenset({"help", "buy", "swim"}): ("help", "help_default"),
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
    frozenset({"pet", "feed", "ignore"}): None,  # handled by conditional helper
    frozenset({"drink", "save", "toss"}): None,  # handled by conditional helper
    frozenset({"pull", "burn"}): None,            # handled by conditional helper
    frozenset({"drink", "wash", "bottle", "leave"}): None,  # handled by conditional helper
}


# -- Event-name inline dispatch table --

_EVENT_INLINE = {
    # Night: Favorites
    "night:whats_my_favorite_color":   _inline_favorite_color,
    "night:whats_my_favorite_animal":  _inline_favorite_animal,
    # Storyline: Suzy
    "storyline:suzy:stage0":           _inline_favorite_color,
    "storyline:suzy:stage1":           _inline_favorite_animal,
    # Companions
    "day:companion_sick_day":          _inline_companion_sick,
    "day:companion_rivalry":           lambda r, p, pr, rc, b, h, rk, c, cs, inv: (
        "1", _inline_trace(r, p, "1", "break_it_up_carefully", 0.82)),
    "day:companion_lost_adventure":    lambda r, p, pr, rc, b, h, rk, c, cs, inv: (
        "1", _inline_trace(r, p, "1", "search_immediate_area", 0.8)),
}


# ==============================================================================
# PUBLIC ENTRY POINTS
# ==============================================================================


def choose_event_yes_no(request: DecisionRequest, plan: StrategicPlan) -> tuple[str | None, DecisionTrace | None]:
    """Dispatch a yes/no decision by event name."""
    event_name = str(request.metadata.get("event_name", "") or request.stable_context_id or "")
    prompt_lower = str(request.metadata.get("prompt_lower", "") or "").strip()
    recent = str(request.metadata.get("recent_lower", "") or "")
    cost = request.metadata.get("cost")
    balance = int(request.game_state.get("balance", 0) or 0)
    health = int(request.game_state.get("health", 0) or 0)
    sanity = int(request.game_state.get("sanity", 0) or 0)

    # 1. Conditional event-name handlers (checked first: may override simple sets)
    handler = _EVENT_YES_NO.get(event_name)
    if handler is not None:
        return handler(request, plan, prompt_lower, recent, cost, balance, health, sanity)

    # 2. Simple yes/no event sets
    if event_name in _SIMPLE_YES_EVENTS:
        return "yes", _yes_no_trace(request, plan, "yes", f"event_yes:{event_name}", 0.82)

    if event_name in _SIMPLE_NO_EVENTS:
        return "no", _yes_no_trace(request, plan, "no", f"event_no:{event_name}", 0.82)

    # 3. Unmapped event: return None (caller handles)
    return None, None


def choose_event_option(request: DecisionRequest, plan: StrategicPlan) -> tuple[DecisionOption | None, DecisionTrace | None]:
    """Dispatch an option decision by event name."""
    event_name = str(request.metadata.get("event_name", "") or request.stable_context_id or "")
    options = list(request.normalized_options)
    normalized = [str(option.label).strip().lower() for option in options]
    balance = int(request.game_state.get("balance", 0) or 0)
    health = int(request.game_state.get("health", 0) or 0)

    # 1. Event-name handler
    handler = _EVENT_OPTION.get(event_name)
    if handler is not None:
        result = handler(request, plan, options, normalized, balance, health)
        if result[0] is not None:
            return result

    # 2. Violence avoidance (cross-cutting safety)
    for idx, opt in enumerate(normalized):
        if any(danger in opt for danger in ("fight", "attack", "shoot", "stab", "kill")):
            safe_idx, reason = _pick_safe_option(options, normalized, "avoid_violence")
            return options[safe_idx], _option_trace(request, plan, options, safe_idx, reason, 0.85)

    # 3. Generic behavioral strategy
    chosen_index, reason, confidence = _choose_generic_option(
        options, request, prefer_safe=plan.personality.prefer_safe_events
    )
    if chosen_index is None:
        return None, None
    return options[chosen_index], _option_trace(request, plan, options, chosen_index, reason or "event_option_generic", confidence)


def choose_event_inline_choice(request: DecisionRequest, plan: StrategicPlan) -> tuple[str | None, DecisionTrace | None]:
    """Dispatch an inline choice decision by event name."""
    event_name = str(request.metadata.get("event_name", "") or request.stable_context_id or "")
    prompt_lower = str(request.metadata.get("prompt_lower", "") or "")
    recent = str(request.metadata.get("recent_lower", "") or "")
    balance = int(request.game_state.get("balance", 0) or 0)
    health = int(request.game_state.get("health", 0) or 0)
    rank = int(request.game_state.get("rank", 0) or 0)
    choices = [str(option.label).strip().lower() for option in request.normalized_options]
    choice_set = set(choices)
    inventory = {str(item).lower() for item in request.game_state.get("inventory", ())}

    # 1. Event-name handler
    handler = _EVENT_INLINE.get(event_name)
    if handler is not None:
        result = handler(request, plan, prompt_lower, recent, balance, health, rank, choices, choice_set, inventory)
        if result[0] is not None:
            return result

    # 2. Choice-set handler
    mapped = _INLINE_SET_HANDLERS.get(frozenset(choice_set))
    if mapped is not None:
        chosen, reason = mapped
        return chosen, _inline_trace(request, plan, chosen, reason, 0.82)
    # Check for conditional choice-set handlers (None values in the table)
    if frozenset(choice_set) in _INLINE_SET_HANDLERS:
        # None means a conditional handler exists outside the table
        if choice_set == {"pull", "burn"}:
            return _inline_pull_burn(request, plan, prompt_lower, recent, balance, health, rank, choices, choice_set, inventory)
        if choice_set == {"pet", "feed", "ignore"}:
            return _inline_pet_feed_ignore(request, plan, prompt_lower, recent, balance, health, rank, choices, choice_set, inventory)
        if choice_set == {"drink", "save", "toss"}:
            return _inline_swamp_nectar(request, plan, prompt_lower, recent, balance, health, rank, choices, choice_set, inventory)
        if choice_set == {"drink", "wash", "bottle", "leave"}:
            return _inline_woodland_spring(request, plan, prompt_lower, recent, balance, health, rank, choices, choice_set, inventory)

    # 3. "choose:" prompt handlers (companion systems)
    if prompt_lower == "choose:":
        if "your companion is sick" in recent:
            return _inline_companion_sick(request, plan, prompt_lower, recent, balance, health, rank, choices, choice_set, inventory)
        if "break it up carefully" in recent:
            return "1", _inline_trace(request, plan, "1", "break_it_up_carefully", 0.82)
        if "morning" in recent and "companions are hungry" in recent:
            return _inline_companion_hungry(request, plan, prompt_lower, recent, balance, health, rank, choices, choice_set, inventory)
        if "is gone." in recent and "search the immediate area" in recent:
            return "1", _inline_trace(request, plan, "1", "search_immediate_area", 0.8)
        if "someone in trouble" in recent and "drive over and help" in recent:
            return "1", _inline_trace(request, plan, "1", "drive_over_and_help", 0.8)

    # 4. Generic behavioral strategy
    chosen, reason, confidence = _choose_generic_inline(request, prefer_safe=plan.personality.prefer_safe_events)
    if chosen is None:
        return None, None
    return chosen, _inline_trace(request, plan, chosen, reason or "event_inline_generic", confidence)
