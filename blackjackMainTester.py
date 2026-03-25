import random
import story
import hashlib
import sys
import inspect
import re
from colorama import Fore, Style


def red(text):
    return (Fore.RED + text + Fore.WHITE)


def bright(text):
    return (Style.BRIGHT + text + Style.NORMAL)


REROUTE_LOG = []
ACTIVE_TEST_SEED = None
ACTIVE_TEST_SEED_COUNTER = 0
_EVENT_REQUIREMENT_CACHE = {}


def _derive_test_seed(base_seed, counter):
    payload = f"{int(base_seed)}:{int(counter)}".encode("utf-8")
    return int(hashlib.sha256(payload).hexdigest(), 16) % (2 ** 32)


def _apply_test_seed(player, seed):
    candidate_names = [
        "set_seed",
        "seed",
        "set_random_seed",
        "set_rng_seed",
    ]
    for name in candidate_names:
        method = getattr(player, name, None)
        if callable(method):
            method(int(seed))
            return

    random.seed(int(seed))


def _apply_event_ready_profile(player):
    """Set permissive baseline state so prerequisite-heavy events are more likely to fire."""
    if hasattr(player, "_alive"):
        player._alive = True
    if hasattr(player, "_health"):
        player._health = max(100, getattr(player, "_health", 100))
    if hasattr(player, "_sanity"):
        player._sanity = max(100, getattr(player, "_sanity", 100))
    if hasattr(player, "_is_broken"):
        player._is_broken = False

    # Mid-run day/rank improves access to many gated branches.
    if hasattr(player, "_day"):
        player._day = max(30, getattr(player, "_day", 1))
    if hasattr(player, "_rank"):
        player._rank = max(2, getattr(player, "_rank", 0))

    # Clear common blockers.
    if hasattr(player, "_status_effects"):
        player._status_effects = set()
    if hasattr(player, "_injuries"):
        player._injuries = set()
    if hasattr(player, "_travel_restrictions"):
        player._travel_restrictions = set()


def _install_reroute_guards(player):
    def _reroute(event_kind):
        REROUTE_LOG.append({
            "kind": event_kind,
            "day": getattr(player, "_day", "?"),
            "balance": getattr(player, "_balance", "?"),
        })
        print(bright(red("REROUTE BLOCKED: " + event_kind + " (event prerequisites not met)")))
        return None

    player.day_event = lambda: _reroute("day_event")
    player.night_event = lambda: _reroute("night_event")


def _infer_tester_name_from_stack():
    for frame_info in inspect.stack()[2:10]:
        fn_name = frame_info.function
        if fn_name in {"new_player", "run_all_events", "run_seeded_subset", "run_seeded_sweep", "main"}:
            continue
        if fn_name.startswith("<"):
            continue
        return fn_name
    return None


def _resolve_event_name(player, tester_name):
    if not tester_name:
        return None

    candidates = [tester_name]
    if "__" in tester_name:
        candidates.append(tester_name.split("__", 1)[1])

    for name in candidates:
        method = getattr(player, name, None)
        if callable(method):
            return name
    return None


def _parse_event_requirements(player, event_name):
    if not event_name:
        return {
            "dangers": set(),
            "met": set(),
            "statuses": set(),
            "injuries": set(),
            "companions": set(),
            "min_day": None,
            "min_rank": None,
            "min_companions": 0,
            "min_fake_cash_level": 0,
            "min_pawn_reputation": None,
            "min_loan_warning": None,
        }

    cached = _EVENT_REQUIREMENT_CACHE.get(event_name)
    if cached is not None:
        return cached

    requirements = {
        "dangers": set(),
        "met": set(),
        "statuses": set(),
        "injuries": set(),
        "companions": set(),
        "min_day": None,
        "min_rank": None,
        "min_companions": 0,
        "min_fake_cash_level": 0,
        "min_pawn_reputation": None,
        "min_loan_warning": None,
    }

    event_callable = getattr(player, event_name, None)
    if not callable(event_callable):
        _EVENT_REQUIREMENT_CACHE[event_name] = requirements
        return requirements

    try:
        source = inspect.getsource(event_callable)
    except (OSError, TypeError):
        _EVENT_REQUIREMENT_CACHE[event_name] = requirements
        return requirements

    def _extract_set(pattern):
        found = set()
        for quote, value in re.findall(pattern, source):
            if value:
                found.add(value)
        return found

    requirements["dangers"].update(
        _extract_set(r"not\s+self\.has_danger\(([\"'])(.+?)\1\)")
    )
    requirements["met"].update(
        _extract_set(r"not\s+self\.has_met\(([\"'])(.+?)\1\)")
    )
    requirements["statuses"].update(
        _extract_set(r"not\s+self\.has_status\(([\"'])(.+?)\1\)")
    )
    requirements["injuries"].update(
        _extract_set(r"not\s+self\.has_injury\(([\"'])(.+?)\1\)")
    )
    requirements["companions"].update(
        _extract_set(r"not\s+self\.has_companion\(([\"'])(.+?)\1\)")
    )
    requirements["companions"].update(
        _extract_set(r"self\.get_companion\(([\"'])(.+?)\1\)\s*\[\s*[\"']status[\"']\s*\]\s*!=\s*[\"']alive[\"']")
    )

    day_matches = re.findall(r"self\.get_day\(\)\s*<\s*(\d+)", source)
    if day_matches:
        requirements["min_day"] = max(int(m) for m in day_matches)

    rank_matches = re.findall(r"self\.get_rank\(\)\s*<\s*(\d+)", source)
    if rank_matches:
        requirements["min_rank"] = max(int(m) for m in rank_matches)

    companion_len_matches = re.findall(r"len\([^\n]*companions[^\n]*\)\s*<\s*(\d+)", source)
    if companion_len_matches:
        requirements["min_companions"] = max(int(m) for m in companion_len_matches)

    assignment_lines = re.findall(
        r"^\s*([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.+)$",
        source,
        flags=re.MULTILINE,
    )
    companion_vars = {
        var for var, expr in assignment_lines if "companions" in expr
    }
    changed = True
    while changed:
        changed = False
        for var, expr in assignment_lines:
            if var in companion_vars:
                continue
            if any(existing in expr for existing in companion_vars):
                companion_vars.add(var)
                changed = True
    for var in companion_vars:
        if re.search(rf"if\s+not\s+{re.escape(var)}\b", source):
            requirements["min_companions"] = max(requirements["min_companions"], 1)
        if re.search(rf"if\s+len\(\s*{re.escape(var)}\s*\)\s*==\s*0", source):
            requirements["min_companions"] = max(requirements["min_companions"], 1)
        var_len_matches = re.findall(rf"if\s+len\(\s*{re.escape(var)}\s*\)\s*<\s*(\d+)", source)
        if var_len_matches:
            requirements["min_companions"] = max(
                requirements["min_companions"],
                max(int(m) for m in var_len_matches),
            )

    fake_cash_matches = re.findall(r"self\.get_dealer_fake_cash_danger_level\(\)\s*<\s*(\d+)", source)
    if fake_cash_matches:
        requirements["min_fake_cash_level"] = max(int(m) for m in fake_cash_matches)

    pawn_matches = re.findall(r"self\.get_pawn_reputation\(\)\s*<\s*(\d+)", source)
    if pawn_matches:
        requirements["min_pawn_reputation"] = max(int(m) for m in pawn_matches)

    loan_matches = re.findall(r"self\.get_loan_shark_warning_level\(\)\s*<\s*(\d+)", source)
    if loan_matches:
        requirements["min_loan_warning"] = max(int(m) for m in loan_matches)

    _EVENT_REQUIREMENT_CACHE[event_name] = requirements
    return requirements


def _seed_companion(player, name):
    if not hasattr(player, "_companions"):
        return
    companions = getattr(player, "_companions", None)
    if not isinstance(companions, dict):
        return
    if name in companions:
        companions[name]["status"] = "alive"
        companions[name]["happiness"] = max(80, companions[name].get("happiness", 80))
        companions[name]["days_owned"] = max(120, companions[name].get("days_owned", 120))
        companions[name]["bonded"] = bool(companions[name].get("bonded", True))
        companions[name]["fed_today"] = True
        return
    companions[name] = {
        "status": "alive",
        "happiness": 90,
        "days_owned": 120,
        "fed_today": True,
        "bonded": True,
    }


def _apply_requirements(player, requirements):
    for danger in requirements.get("dangers", set()):
        if hasattr(player, "add_danger"):
            player.add_danger(danger)
    for name in requirements.get("met", set()):
        if hasattr(player, "meet"):
            player.meet(name)
    for status in requirements.get("statuses", set()):
        if hasattr(player, "add_status"):
            player.add_status(status)
    for injury in requirements.get("injuries", set()):
        if hasattr(player, "add_injury"):
            player.add_injury(injury)

    min_day = requirements.get("min_day")
    if min_day is not None and hasattr(player, "_day"):
        player._day = max(int(min_day), getattr(player, "_day", 1))

    min_rank = requirements.get("min_rank")
    if min_rank is not None and hasattr(player, "_rank"):
        player._rank = max(int(min_rank), getattr(player, "_rank", 0))

    for companion_name in requirements.get("companions", set()):
        _seed_companion(player, companion_name)

    min_companions = int(requirements.get("min_companions", 0) or 0)
    if min_companions > 0:
        companions = getattr(player, "_companions", {})
        alive_count = 0
        if isinstance(companions, dict):
            alive_count = sum(1 for data in companions.values() if data.get("status") == "alive")
        idx = 1
        while alive_count < min_companions:
            _seed_companion(player, f"Tester Companion {idx}")
            alive_count += 1
            idx += 1

    min_fake_cash_level = int(requirements.get("min_fake_cash_level", 0) or 0)
    if min_fake_cash_level > 0 and hasattr(player, "_dealer_fake_cash_total"):
        min_total = 10 ** (min_fake_cash_level + 2)
        player._dealer_fake_cash_total = max(int(getattr(player, "_dealer_fake_cash_total", 0)), int(min_total))

    min_pawn_rep = requirements.get("min_pawn_reputation")
    if min_pawn_rep is not None and hasattr(player, "_pawn_shop_reputation"):
        player._pawn_shop_reputation = max(int(getattr(player, "_pawn_shop_reputation", 50)), int(min_pawn_rep))

    min_loan_warning = requirements.get("min_loan_warning")
    if min_loan_warning is not None and hasattr(player, "_loan_shark_warning_level"):
        player._loan_shark_warning_level = max(int(getattr(player, "_loan_shark_warning_level", 0)), int(min_loan_warning))


def _apply_explicit_overrides(player, dangers=None, statuses=None, injuries=None, met=None, attrs=None):
    for danger in (dangers or []):
        if hasattr(player, "add_danger"):
            player.add_danger(danger)
    for status in (statuses or []):
        if hasattr(player, "add_status"):
            player.add_status(status)
    for injury in (injuries or []):
        if hasattr(player, "add_injury"):
            player.add_injury(injury)
    for person in (met or []):
        if hasattr(player, "meet"):
            player.meet(person)
    if isinstance(attrs, dict):
        for key, value in attrs.items():
            setattr(player, key, value)


def new_player(
    balance=50,
    items=None,
    *,
    event_ready=True,
    infer_requirements=True,
    dangers=None,
    statuses=None,
    injuries=None,
    met=None,
    attrs=None,
):
    global ACTIVE_TEST_SEED_COUNTER
    if items is None:
        items = []
    player = story.Player()
    if ACTIVE_TEST_SEED is not None:
        derived_seed = _derive_test_seed(ACTIVE_TEST_SEED, ACTIVE_TEST_SEED_COUNTER)
        ACTIVE_TEST_SEED_COUNTER += 1
        _apply_test_seed(player, derived_seed)
        setattr(player, "_tester_seed", derived_seed)
    player.set_balance(balance)
    if event_ready:
        _apply_event_ready_profile(player)
    if event_ready and infer_requirements:
        tester_name = _infer_tester_name_from_stack()
        event_name = _resolve_event_name(player, tester_name)
        requirements = _parse_event_requirements(player, event_name)
        _apply_requirements(player, requirements)
    _apply_explicit_overrides(
        player,
        dangers=dangers,
        statuses=statuses,
        injuries=injuries,
        met=met,
        attrs=attrs,
    )
    for item in items:
        player.add_item(item)
    _install_reroute_guards(player)
    return player


"""story.events_day_animals.py"""
def cow_army():
    print(bright(red("TESTING cow_army with no items")))
    player = new_player(balance=500000)
    player.meet("Betsy")
    player.add_danger("Betsy Army")
    player.cow_army()

def crow_encounter():
    print(bright(red("TESTING crow_encounter with no items")))
    player = new_player()
    player.crow_encounter()
    print(bright(red("Testing crow_encounter with Animal Whistle")))
    player = new_player(items=['Animal Whistle'])
    player.crow_encounter()
    print(bright(red("Testing crow_encounter with Birdseed")))
    player = new_player(items=['Birdseed'])
    player.crow_encounter()
    print(bright(red("Testing crow_encounter with Bread")))
    player = new_player(items=['Bread'])
    player.crow_encounter()
    print(bright(red("Testing crow_encounter with Disposable Camera")))
    player = new_player(items=['Disposable Camera'])
    player.crow_encounter()
    print(bright(red("Testing crow_encounter with Slingshot")))
    player = new_player(items=['Slingshot'])
    player.crow_encounter()

def duck_army():
    print(bright(red("TESTING duck_army with no items")))
    player = new_player()
    player.duck_army()
    print(bright(red("Testing duck_army with Animal Whistle")))
    player = new_player(items=['Animal Whistle'])
    player.duck_army()
    print(bright(red("Testing duck_army with Luck Totem")))
    player = new_player(items=['Luck Totem'])
    player.duck_army()

def estranged_dog():
    print(bright(red("TESTING estranged_dog with no items")))
    player = new_player()
    player.estranged_dog()
    print(bright(red("Testing estranged_dog with Animal Whistle")))
    player = new_player(items=['Animal Whistle'])
    player.estranged_dog()
    print(bright(red("Testing estranged_dog with Beastslayer Mantle")))
    player = new_player(items=['Beastslayer Mantle'])
    player.estranged_dog()
    print(bright(red("Testing estranged_dog with Dog Treat")))
    player = new_player(items=['Dog Treat'])
    player.estranged_dog()
    print(bright(red("Testing estranged_dog with Dog Whistle")))
    player = new_player(items=['Dog Whistle'])
    player.estranged_dog()
    print(bright(red("Testing estranged_dog with Fancy Cigars")))
    player = new_player(items=['Fancy Cigars'])
    player.estranged_dog()
    print(bright(red("Testing estranged_dog with Leviathan's Call")))
    player = new_player(items=["Leviathan's Call"])
    player.estranged_dog()
    print(bright(red("Testing estranged_dog with Quiet Bunny Slippers")))
    player = new_player(items=['Quiet Bunny Slippers'])
    player.estranged_dog()
    print(bright(red("Testing estranged_dog with Trail Mix Bomb")))
    player = new_player(items=['Trail Mix Bomb'])
    player.estranged_dog()
    print(bright(red("Testing estranged_dog with Unwashed Hair")))
    player = new_player(items=['Unwashed Hair'])
    player.estranged_dog()

def garden_rabbit():
    print(bright(red("TESTING garden_rabbit with no items")))
    player = new_player()
    player.garden_rabbit()
    print(bright(red("Testing garden_rabbit with Animal Bait")))
    player = new_player(items=['Animal Bait'])
    player.garden_rabbit()
    print(bright(red("Testing garden_rabbit with Luck Totem")))
    player = new_player(items=['Luck Totem'])
    player.garden_rabbit()

def grimy_gus_discovery():
    print(bright(red("TESTING grimy_gus_discovery with no items")))
    player = new_player()
    player.grimy_gus_discovery()
    print(bright(red("Testing grimy_gus_discovery with Car")))
    player = new_player(items=['Car'])
    player.grimy_gus_discovery()

def hungry_cow():
    print(bright(red("TESTING hungry_cow with no items")))
    player = new_player()
    player.hungry_cow()
    print(bright(red("Testing hungry_cow with Animal Whistle")))
    player = new_player(items=['Animal Whistle'])
    player.hungry_cow()
    print(bright(red("Testing hungry_cow with Delight Indicator")))
    player = new_player(items=['Delight Indicator'])
    player.hungry_cow()
    print(bright(red("Testing hungry_cow with Delight Manipulator")))
    player = new_player(items=['Delight Manipulator'])
    player.hungry_cow()

def hungry_termites():
    print(bright(red("TESTING hungry_termites with no items")))
    player = new_player()
    player.hungry_termites()
    print(bright(red("Testing hungry_termites with Pest Control")))
    player = new_player(items=['Pest Control'])
    player.hungry_termites()

def lucky_penny():
    print(bright(red("TESTING lucky_penny with no items")))
    player = new_player()
    player.lucky_penny()

def lucky_rabbit_encounter():
    print(bright(red("TESTING lucky_rabbit_encounter with no items")))
    player = new_player()
    player.lucky_rabbit_encounter()
    print(bright(red("Testing lucky_rabbit_encounter with Animal Whistle")))
    player = new_player(items=['Animal Whistle'])
    player.lucky_rabbit_encounter()
    print(bright(red("Testing lucky_rabbit_encounter with Carrot")))
    player = new_player(items=['Carrot'])
    player.lucky_rabbit_encounter()
    print(bright(red("Testing lucky_rabbit_encounter with Lucky Rabbit Foot")))
    player = new_player(items=['Lucky Rabbit Foot'])
    player.lucky_rabbit_encounter()

def motivational_raccoon():
    print(bright(red("TESTING motivational_raccoon with no items")))
    player = new_player()
    player.motivational_raccoon()

def opossum_in_trash():
    print(bright(red("TESTING opossum_in_trash with no items")))
    player = new_player()
    player.opossum_in_trash()
    print(bright(red("Testing opossum_in_trash with Animal Whistle")))
    player = new_player(items=['Animal Whistle'])
    player.opossum_in_trash()

def pigeon_mafia():
    print(bright(red("TESTING pigeon_mafia with no items")))
    player = new_player()
    player.pigeon_mafia()
    print(bright(red("Testing pigeon_mafia with Animal Whistle")))
    player = new_player(items=['Animal Whistle'])
    player.pigeon_mafia()
    print(bright(red("Testing pigeon_mafia with Slingshot")))
    player = new_player(items=['Slingshot'])
    player.pigeon_mafia()

def raccoon_gang_raid():
    print(bright(red("TESTING raccoon_gang_raid with no items")))
    player = new_player()
    player.raccoon_gang_raid()
    print(bright(red("Testing raccoon_gang_raid with Animal Whistle")))
    player = new_player(items=['Animal Whistle'])
    player.raccoon_gang_raid()
    print(bright(red("Testing raccoon_gang_raid with Ark Master's Horn")))
    player = new_player(items=["Ark Master's Horn"])
    player.raccoon_gang_raid()
    print(bright(red("Testing raccoon_gang_raid with Beast Tamer Kit")))
    player = new_player(items=['Beast Tamer Kit'])
    player.raccoon_gang_raid()
    print(bright(red("Testing raccoon_gang_raid with Beastslayer Mantle")))
    player = new_player(items=['Beastslayer Mantle'])
    player.raccoon_gang_raid()
    print(bright(red("Testing raccoon_gang_raid with Feeding Station")))
    player = new_player(items=['Feeding Station'])
    player.raccoon_gang_raid()
    print(bright(red("Testing raccoon_gang_raid with Fire Launcher")))
    player = new_player(items=['Fire Launcher'])
    player.raccoon_gang_raid()
    print(bright(red("Testing raccoon_gang_raid with Stink Bomb")))
    player = new_player(items=['Stink Bomb'])
    player.raccoon_gang_raid()
    print(bright(red("Testing raccoon_gang_raid with Vermin Bomb")))
    player = new_player(items=['Vermin Bomb'])
    player.raccoon_gang_raid()

def raccoon_raid():
    print(bright(red("TESTING raccoon_raid with no items")))
    player = new_player()
    player.raccoon_raid()

def events_day_animals__rat_bite():
    print(bright(red("TESTING story.events_day_animals:rat_bite with no items")))
    player = new_player()
    story.DayAnimalsMixin.rat_bite(player)
    print(bright(red("Testing story.events_day_animals:rat_bite with Animal Whistle")))
    player = new_player(items=['Animal Whistle'])
    story.DayAnimalsMixin.rat_bite(player)
    print(bright(red("Testing story.events_day_animals:rat_bite with Beastslayer Mantle")))
    player = new_player(items=['Beastslayer Mantle'])
    story.DayAnimalsMixin.rat_bite(player)
    print(bright(red("Testing story.events_day_animals:rat_bite with Pepper Spray")))
    player = new_player(items=['Pepper Spray'])
    story.DayAnimalsMixin.rat_bite(player)
    print(bright(red("Testing story.events_day_animals:rat_bite with Pest Control")))
    player = new_player(items=['Pest Control'])
    story.DayAnimalsMixin.rat_bite(player)
    print(bright(red("Testing story.events_day_animals:rat_bite with Pet Toy")))
    player = new_player(items=['Pet Toy'])
    story.DayAnimalsMixin.rat_bite(player)
    print(bright(red("Testing story.events_day_animals:rat_bite with Stink Bomb")))
    player = new_player(items=['Stink Bomb'])
    story.DayAnimalsMixin.rat_bite(player)
    print(bright(red("Testing story.events_day_animals:rat_bite with Vermin Bomb")))
    player = new_player(items=['Vermin Bomb'])
    story.DayAnimalsMixin.rat_bite(player)

def seagull_attack():
    print(bright(red("TESTING seagull_attack with no items")))
    player = new_player()
    player.seagull_attack()
    print(bright(red("Testing seagull_attack with Animal Magnetism")))
    player = new_player(items=['Animal Magnetism'])
    player.seagull_attack()
    print(bright(red("Testing seagull_attack with Animal Whistle")))
    player = new_player(items=['Animal Whistle'])
    player.seagull_attack()
    print(bright(red("Testing seagull_attack with Ark Master's Horn")))
    player = new_player(items=["Ark Master's Horn"])
    player.seagull_attack()
    print(bright(red("Testing seagull_attack with Beast Tamer Kit")))
    player = new_player(items=['Beast Tamer Kit'])
    player.seagull_attack()
    print(bright(red("Testing seagull_attack with Beastslayer Mantle")))
    player = new_player(items=['Beastslayer Mantle'])
    player.seagull_attack()
    print(bright(red("Testing seagull_attack with Delight Indicator")))
    player = new_player(items=['Delight Indicator'])
    player.seagull_attack()
    print(bright(red("Testing seagull_attack with Delight Manipulator")))
    player = new_player(items=['Delight Manipulator'])
    player.seagull_attack()
    print(bright(red("Testing seagull_attack with Dog Whistle")))
    player = new_player(items=['Dog Whistle'])
    player.seagull_attack()
    print(bright(red("Testing seagull_attack with Slingshot")))
    player = new_player(items=['Slingshot'])
    player.seagull_attack()

def sentient_sandwich():
    print(bright(red("TESTING sentient_sandwich with no items")))
    player = new_player()
    player.sentient_sandwich()

def sewer_rat():
    print(bright(red("TESTING sewer_rat with no items")))
    player = new_player()
    player.sewer_rat()
    print(bright(red("Testing sewer_rat with Animal Bait")))
    player = new_player(items=['Animal Bait'])
    player.sewer_rat()
    print(bright(red("Testing sewer_rat with Cheese")))
    player = new_player(items=['Cheese'])
    player.sewer_rat()
    print(bright(red("Testing sewer_rat with Sandwich")))
    player = new_player(items=['Sandwich'])
    player.sewer_rat()
    print(bright(red("Testing sewer_rat with Turkey Sandwich")))
    player = new_player(items=['Turkey Sandwich'])
    player.sewer_rat()

def squirrel_invasion():
    print(bright(red("TESTING squirrel_invasion with no items")))
    player = new_player()
    player.squirrel_invasion()
    print(bright(red("Testing squirrel_invasion with Animal Whistle")))
    player = new_player(items=['Animal Whistle'])
    player.squirrel_invasion()
    print(bright(red("Testing squirrel_invasion with Bag of Acorns")))
    player = new_player(items=['Bag of Acorns'])
    player.squirrel_invasion()
    print(bright(red("Testing squirrel_invasion with Companion Bed")))
    player = new_player(items=['Companion Bed'])
    player.squirrel_invasion()
    print(bright(red("Testing squirrel_invasion with Snare Trap")))
    player = new_player(items=['Snare Trap'])
    player.squirrel_invasion()
    print(bright(red("Testing squirrel_invasion with Squirrely")))
    player = new_player(items=['Squirrely'])
    player.squirrel_invasion()

def starving_cow():
    print(bright(red("TESTING starving_cow with no items")))
    player = new_player()
    player.starving_cow()

def stray_cat():
    print(bright(red("TESTING stray_cat with no items")))
    player = new_player()
    player.stray_cat()
    print(bright(red("Testing stray_cat with Animal Bait")))
    player = new_player(items=['Animal Bait'])
    player.stray_cat()

def stray_cat_dies():
    print(bright(red("TESTING stray_cat_dies with no items")))
    player = new_player()
    player.stray_cat_dies()

def stray_cat_has_kittens():
    print(bright(red("TESTING stray_cat_has_kittens with no items")))
    player = new_player()
    player.stray_cat_has_kittens()

def stray_cat_sick():
    print(bright(red("TESTING stray_cat_sick with no items")))
    player = new_player()
    player.stray_cat_sick()

def three_legged_dog():
    print(bright(red("TESTING three_legged_dog with no items")))
    player = new_player()
    player.three_legged_dog()
    print(bright(red("Testing three_legged_dog with Animal Whistle")))
    player = new_player(items=['Animal Whistle'])
    player.three_legged_dog()

def wild_rat_attack():
    print(bright(red("TESTING wild_rat_attack with no items")))
    player = new_player()
    player.wild_rat_attack()
    print(bright(red("Testing wild_rat_attack with Animal Magnetism")))
    player = new_player(items=['Animal Magnetism'])
    player.wild_rat_attack()
    print(bright(red("Testing wild_rat_attack with Beast Tamer Kit")))
    player = new_player(items=['Beast Tamer Kit'])
    player.wild_rat_attack()
    print(bright(red("Testing wild_rat_attack with Pursuit Package")))
    player = new_player(items=['Pursuit Package'])
    player.wild_rat_attack()
    print(bright(red("Testing wild_rat_attack with Road Flare Torch")))
    player = new_player(items=['Road Flare Torch'])
    player.wild_rat_attack()
    print(bright(red("Testing wild_rat_attack with Running Shoes")))
    player = new_player(items=['Running Shoes'])
    player.wild_rat_attack()
    print(bright(red("Testing wild_rat_attack with Trail Mix Bomb")))
    player = new_player(items=['Trail Mix Bomb'])
    player.wild_rat_attack()

def wrong_item_dog_whistle_bear():
    print(bright(red("TESTING wrong_item_dog_whistle_bear with no items")))
    player = new_player()
    player.wrong_item_dog_whistle_bear()
    print(bright(red("Testing wrong_item_dog_whistle_bear with Dog Whistle")))
    player = new_player(items=['Dog Whistle'])
    player.wrong_item_dog_whistle_bear()


"""story.events_day_casino.py"""
def casino_security():
    print(bright(red("TESTING casino_security with no items")))
    player = new_player()
    player.casino_security()
    print(bright(red("Testing casino_security with Cheater's Insurance")))
    player = new_player(items=["Cheater's Insurance"])
    player.casino_security()
    print(bright(red("Testing casino_security with Devil's Deck")))
    player = new_player(items=["Devil's Deck"])
    player.casino_security()
    print(bright(red("Testing casino_security with EMP Device")))
    player = new_player(items=['EMP Device'])
    player.casino_security()
    print(bright(red("Testing casino_security with Eldritch Candle")))
    player = new_player(items=['Eldritch Candle'])
    player.casino_security()
    print(bright(red("Testing casino_security with Flask of Dealer's Whispers")))
    player = new_player(items=["Flask of Dealer's Whispers"])
    player.casino_security()
    print(bright(red("Testing casino_security with Flask of Pocket Aces")))
    player = new_player(items=['Flask of Pocket Aces'])
    player.casino_security()
    print(bright(red("Testing casino_security with Flask of Split Serum")))
    player = new_player(items=['Flask of Split Serum'])
    player.casino_security()
    print(bright(red("Testing casino_security with Ghost Protocol")))
    player = new_player(items=['Ghost Protocol'])
    player.casino_security()
    print(bright(red("Testing casino_security with Gold Chain")))
    player = new_player(items=['Gold Chain'])
    player.casino_security()
    print(bright(red("Testing casino_security with Golden Watch")))
    player = new_player(items=['Golden Watch'])
    player.casino_security()
    print(bright(red("Testing casino_security with New Identity")))
    player = new_player(items=['New Identity'])
    player.casino_security()
    print(bright(red("Testing casino_security with Radio Jammer")))
    player = new_player(items=['Radio Jammer'])
    player.casino_security()
    print(bright(red("Testing casino_security with Sapphire Watch")))
    player = new_player(items=['Sapphire Watch'])
    player.casino_security()
    print(bright(red("Testing casino_security with Stink Bomb")))
    player = new_player(items=['Stink Bomb'])
    player.casino_security()
    print(bright(red("Testing casino_security with Surveillance Suite")))
    player = new_player(items=['Surveillance Suite'])
    player.casino_security()
    print(bright(red("Testing casino_security with Velvet Gloves")))
    player = new_player(items=['Velvet Gloves'])
    player.casino_security()
    print(bright(red("Testing casino_security with Worn Gloves")))
    player = new_player(items=['Worn Gloves'])
    player.casino_security()

def even_further_interrogation():
    print(bright(red("TESTING even_further_interrogation with no items")))
    player = new_player()
    player.even_further_interrogation()

def high_stakes_feeling():
    print(bright(red("TESTING high_stakes_feeling with no items")))
    player = new_player()
    player.high_stakes_feeling()
    print(bright(red("Testing high_stakes_feeling with Cheater's Insurance")))
    player = new_player(items=["Cheater's Insurance"])
    player.high_stakes_feeling()
    print(bright(red("Testing high_stakes_feeling with Flask of Dealer's Hesitation")))
    player = new_player(items=["Flask of Dealer's Hesitation"])
    player.high_stakes_feeling()
    print(bright(red("Testing high_stakes_feeling with Flask of Imminent Blackjack")))
    player = new_player(items=['Flask of Imminent Blackjack'])
    player.high_stakes_feeling()
    print(bright(red("Testing high_stakes_feeling with Flask of No Bust")))
    player = new_player(items=['Flask of No Bust'])
    player.high_stakes_feeling()
    print(bright(red("Testing high_stakes_feeling with Flask of Second Chance")))
    player = new_player(items=['Flask of Second Chance'])
    player.high_stakes_feeling()
    print(bright(red("Testing high_stakes_feeling with Gold Chain")))
    player = new_player(items=['Gold Chain'])
    player.high_stakes_feeling()
    print(bright(red("Testing high_stakes_feeling with Golden Watch")))
    player = new_player(items=['Golden Watch'])
    player.high_stakes_feeling()
    print(bright(red("Testing high_stakes_feeling with Old Money Identity")))
    player = new_player(items=['Old Money Identity'])
    player.high_stakes_feeling()
    print(bright(red("Testing high_stakes_feeling with Sapphire Watch")))
    player = new_player(items=['Sapphire Watch'])
    player.high_stakes_feeling()
    print(bright(red("Testing high_stakes_feeling with Velvet Gloves")))
    player = new_player(items=['Velvet Gloves'])
    player.high_stakes_feeling()
    print(bright(red("Testing high_stakes_feeling with Worn Gloves")))
    player = new_player(items=['Worn Gloves'])
    player.high_stakes_feeling()

def perfect_hand():
    print(bright(red("TESTING perfect_hand with no items")))
    player = new_player()
    player.perfect_hand()
    print(bright(red("Testing perfect_hand with Eldritch Candle")))
    player = new_player(items=['Eldritch Candle'])
    player.perfect_hand()
    print(bright(red("Testing perfect_hand with Flask of Imminent Blackjack")))
    player = new_player(items=['Flask of Imminent Blackjack'])
    player.perfect_hand()
    print(bright(red("Testing perfect_hand with Fortune's Favor")))
    player = new_player(items=["Fortune's Favor"])
    player.perfect_hand()
    print(bright(red("Testing perfect_hand with Gambler's Aura")))
    player = new_player(items=["Gambler's Aura"])
    player.perfect_hand()
    print(bright(red("Testing perfect_hand with Master of Games")))
    player = new_player(items=['Master of Games'])
    player.perfect_hand()
    print(bright(red("Testing perfect_hand with Moonlit Fortune")))
    player = new_player(items=['Moonlit Fortune'])
    player.perfect_hand()

def the_dying_dealer():
    print(bright(red("TESTING the_dying_dealer with no items")))
    player = new_player()
    player.the_dying_dealer()
    print(bright(red("Testing the_dying_dealer with Deck of Cards")))
    player = new_player(items=['Deck of Cards'])
    player.the_dying_dealer()
    print(bright(red("Testing the_dying_dealer with Flask of Dealer's Hesitation")))
    player = new_player(items=["Flask of Dealer's Hesitation"])
    player.the_dying_dealer()
    print(bright(red("Testing the_dying_dealer with Flask of Dealer's Whispers")))
    player = new_player(items=["Flask of Dealer's Whispers"])
    player.the_dying_dealer()


"""story.events_day_companions.py"""
def bear_scrap_armor_synergy():
    print(bright(red("TESTING bear_scrap_armor_synergy with no items")))
    player = new_player()
    player.bear_scrap_armor_synergy()
    print(bright(red("Testing bear_scrap_armor_synergy with Scrap Armor")))
    player = new_player(items=['Scrap Armor'])
    player.bear_scrap_armor_synergy()

def buddy_dog_whistle_synergy():
    print(bright(red("TESTING buddy_dog_whistle_synergy with no items")))
    player = new_player()
    player.buddy_dog_whistle_synergy()
    print(bright(red("Testing buddy_dog_whistle_synergy with Dog Whistle")))
    player = new_player(items=['Dog Whistle'])
    player.buddy_dog_whistle_synergy()

def buddy_passive_find():
    print(bright(red("TESTING buddy_passive_find with no items")))
    player = new_player()
    player.buddy_passive_find()
    print(bright(red("Testing buddy_passive_find with Bandage")))
    player = new_player(items=['Bandage'])
    player.buddy_passive_find()
    print(bright(red("Testing buddy_passive_find with Granola Bar")))
    player = new_player(items=['Granola Bar'])
    player.buddy_passive_find()

def companion_bed_bonus():
    print(bright(red("TESTING companion_bed_bonus with no items")))
    player = new_player()
    player.companion_bed_bonus()
    print(bright(red("Testing companion_bed_bonus with Companion Bed")))
    player = new_player(items=['Companion Bed'])
    player.companion_bed_bonus()

def companion_bonded_moment():
    print(bright(red("TESTING companion_bonded_moment with no items")))
    player = new_player()
    player.companion_bonded_moment()
    print(bright(red("Testing companion_bonded_moment with Beast Tamer Kit")))
    player = new_player(items=['Beast Tamer Kit'])
    player.companion_bonded_moment()
    print(bright(red("Testing companion_bonded_moment with Companion Bed")))
    player = new_player(items=['Companion Bed'])
    player.companion_bonded_moment()
    print(bright(red("Testing companion_bonded_moment with Deck of Cards")))
    player = new_player(items=['Deck of Cards'])
    player.companion_bonded_moment()
    print(bright(red("Testing companion_bonded_moment with Delight Indicator")))
    player = new_player(items=['Delight Indicator'])
    player.companion_bonded_moment()
    print(bright(red("Testing companion_bonded_moment with Delight Manipulator")))
    player = new_player(items=['Delight Manipulator'])
    player.companion_bonded_moment()
    print(bright(red("Testing companion_bonded_moment with Feeding Station")))
    player = new_player(items=['Feeding Station'])
    player.companion_bonded_moment()
    print(bright(red("Testing companion_bonded_moment with Pet Toy")))
    player = new_player(items=['Pet Toy'])
    player.companion_bonded_moment()

def companion_brings_friend():
    print(bright(red("TESTING companion_brings_friend with no items")))
    player = new_player()
    player.companion_brings_friend()

def companion_death_sacrifice():
    print(bright(red("TESTING companion_death_sacrifice with no items")))
    player = new_player()
    player.companion_death_sacrifice()

def companion_food_crisis():
    print(bright(red("TESTING companion_food_crisis with no items")))
    player = new_player()
    player.companion_food_crisis()
    print(bright(red("Testing companion_food_crisis with Provider's Kit")))
    player = new_player(items=["Provider's Kit"])
    player.companion_food_crisis()

def companion_hero_moment():
    print(bright(red("TESTING companion_hero_moment with no items")))
    player = new_player()
    player.companion_hero_moment()

def companion_learns_trick():
    print(bright(red("TESTING companion_learns_trick with no items")))
    player = new_player()
    player.companion_learns_trick()
    print(bright(red("Testing companion_learns_trick with Ark Master's Horn")))
    player = new_player(items=["Ark Master's Horn"])
    player.companion_learns_trick()
    print(bright(red("Testing companion_learns_trick with Devil's Deck")))
    player = new_player(items=["Devil's Deck"])
    player.companion_learns_trick()
    print(bright(red("Testing companion_learns_trick with Dog Whistle")))
    player = new_player(items=['Dog Whistle'])
    player.companion_learns_trick()
    print(bright(red("Testing companion_learns_trick with Flashlight")))
    player = new_player(items=['Flashlight'])
    player.companion_learns_trick()
    print(bright(red("Testing companion_learns_trick with Fortune Cards")))
    player = new_player(items=['Fortune Cards'])
    player.companion_learns_trick()
    print(bright(red("Testing companion_learns_trick with Headlamp")))
    player = new_player(items=['Headlamp'])
    player.companion_learns_trick()
    print(bright(red("Testing companion_learns_trick with Night Scope")))
    player = new_player(items=['Night Scope'])
    player.companion_learns_trick()

def companion_lost_adventure():
    print(bright(red("TESTING companion_lost_adventure with no items")))
    player = new_player()
    player.companion_lost_adventure()

def companion_milestone():
    print(bright(red("TESTING companion_milestone with no items")))
    player = new_player()
    player.companion_milestone()

def companion_reunion():
    print(bright(red("TESTING companion_reunion with no items")))
    player = new_player()
    player.companion_reunion()

def companion_rivalry():
    print(bright(red("TESTING companion_rivalry with no items")))
    player = new_player()
    player.companion_rivalry()

def companion_sick_day():
    print(bright(red("TESTING companion_sick_day with no items")))
    player = new_player()
    player.companion_sick_day()
    print(bright(red("Testing companion_sick_day with Cough Drops")))
    player = new_player(items=['Cough Drops'])
    player.companion_sick_day()
    print(bright(red("Testing companion_sick_day with Flask of Anti-Venom")))
    player = new_player(items=['Flask of Anti-Venom'])
    player.companion_sick_day()
    print(bright(red("Testing companion_sick_day with Flask of Anti-Virus")))
    player = new_player(items=['Flask of Anti-Virus'])
    player.companion_sick_day()
    print(bright(red("Testing companion_sick_day with Splint")))
    player = new_player(items=['Splint'])
    player.companion_sick_day()

def echo_camera_synergy():
    print(bright(red("TESTING echo_camera_synergy with no items")))
    player = new_player()
    player.echo_camera_synergy()
    print(bright(red("Testing echo_camera_synergy with Disposable Camera")))
    player = new_player(items=['Disposable Camera'])
    player.echo_camera_synergy()

def feeding_station_morning():
    print(bright(red("TESTING feeding_station_morning with no items")))
    player = new_player()
    player.feeding_station_morning()
    print(bright(red("Testing feeding_station_morning with Feeding Station")))
    player = new_player(items=['Feeding Station'])
    player.feeding_station_morning()

def grace_dream_catcher_synergy():
    print(bright(red("TESTING grace_dream_catcher_synergy with no items")))
    player = new_player()
    player.grace_dream_catcher_synergy()
    print(bright(red("Testing grace_dream_catcher_synergy with Dream Catcher")))
    player = new_player(items=['Dream Catcher'])
    player.grace_dream_catcher_synergy()

def hopper_lucky_day():
    print(bright(red("TESTING hopper_lucky_day with no items")))
    player = new_player()
    player.hopper_lucky_day()

def hopper_passive_find():
    print(bright(red("TESTING hopper_passive_find with no items")))
    player = new_player()
    player.hopper_passive_find()
    print(bright(red("Testing hopper_passive_find with Worry Stone")))
    player = new_player(items=['Worry Stone'])
    player.hopper_passive_find()

def lucky_guards_car():
    print(bright(red("TESTING lucky_guards_car with no items")))
    player = new_player()
    player.lucky_guards_car()

def mr_pecks_treasure():
    print(bright(red("TESTING mr_pecks_treasure with no items")))
    player = new_player()
    player.mr_pecks_treasure()
    print(bright(red("Testing mr_pecks_treasure with Disposable Camera")))
    player = new_player(items=['Disposable Camera'])
    player.mr_pecks_treasure()
    print(bright(red("Testing mr_pecks_treasure with Golden Ring")))
    player = new_player(items=['Golden Ring'])
    player.mr_pecks_treasure()
    print(bright(red("Testing mr_pecks_treasure with Marvin's Monocle")))
    player = new_player(items=["Marvin's Monocle"])
    player.mr_pecks_treasure()

def patches_night_watch():
    print(bright(red("TESTING patches_night_watch with no items")))
    player = new_player()
    player.patches_night_watch()

def pet_toy_playtime():
    print(bright(red("TESTING pet_toy_playtime with no items")))
    player = new_player()
    player.pet_toy_playtime()
    print(bright(red("Testing pet_toy_playtime with Pet Toy")))
    player = new_player(items=['Pet Toy'])
    player.pet_toy_playtime()

def rusty_midnight_heist():
    print(bright(red("TESTING rusty_midnight_heist with no items")))
    player = new_player()
    player.rusty_midnight_heist()

def shellbert_worry_stone_synergy():
    print(bright(red("TESTING shellbert_worry_stone_synergy with no items")))
    player = new_player()
    player.shellbert_worry_stone_synergy()
    print(bright(red("Testing shellbert_worry_stone_synergy with Worry Stone")))
    player = new_player(items=['Worry Stone'])
    player.shellbert_worry_stone_synergy()

def slick_escape_route():
    print(bright(red("TESTING slick_escape_route with no items")))
    player = new_player()
    player.slick_escape_route()

def slick_passive_find():
    print(bright(red("TESTING slick_passive_find with no items")))
    player = new_player()
    player.slick_passive_find()
    print(bright(red("Testing slick_passive_find with Lucky Penny")))
    player = new_player(items=['Lucky Penny'])
    player.slick_passive_find()
    print(bright(red("Testing slick_passive_find with Pocket Knife")))
    player = new_player(items=['Pocket Knife'])
    player.slick_passive_find()

def squirrelly_stash():
    print(bright(red("TESTING squirrelly_stash with no items")))
    player = new_player()
    player.squirrelly_stash()

def the_cat_knows():
    print(bright(red("TESTING the_cat_knows with no items")))
    player = new_player()
    player.the_cat_knows()

def thunder_running_shoes_synergy():
    print(bright(red("TESTING thunder_running_shoes_synergy with no items")))
    player = new_player()
    player.thunder_running_shoes_synergy()
    print(bright(red("Testing thunder_running_shoes_synergy with Running Shoes")))
    player = new_player(items=['Running Shoes'])
    player.thunder_running_shoes_synergy()

def whiskers_sixth_sense():
    print(bright(red("TESTING whiskers_sixth_sense with no items")))
    player = new_player()
    player.whiskers_sixth_sense()


"""story.events_day_dark.py"""
def attacked_by_dog():
    print(bright(red("TESTING attacked_by_dog with no items")))
    player = new_player()
    player.attacked_by_dog()
    print(bright(red("Testing attacked_by_dog with Dog Whistle")))
    player = new_player(items=['Dog Whistle'])
    player.attacked_by_dog()
    print(bright(red("Testing attacked_by_dog with Plated Vest")))
    player = new_player(items=['Plated Vest'])
    player.attacked_by_dog()
    print(bright(red("Testing attacked_by_dog with Road Warrior Plate")))
    player = new_player(items=['Road Warrior Plate'])
    player.attacked_by_dog()
    print(bright(red("Testing attacked_by_dog with Scrap Armor")))
    player = new_player(items=['Scrap Armor'])
    player.attacked_by_dog()

def back_alley_shortcut():
    print(bright(red("TESTING back_alley_shortcut with no items")))
    player = new_player()
    player.back_alley_shortcut()
    print(bright(red("Testing back_alley_shortcut with Assassin's Kit")))
    player = new_player(items=["Assassin's Kit"])
    player.back_alley_shortcut()
    print(bright(red("Testing back_alley_shortcut with Beach Bum Disguise")))
    player = new_player(items=['Beach Bum Disguise'])
    player.back_alley_shortcut()
    print(bright(red("Testing back_alley_shortcut with Brass Knuckles")))
    player = new_player(items=['Brass Knuckles'])
    player.back_alley_shortcut()
    print(bright(red("Testing back_alley_shortcut with Cheater's Insurance")))
    player = new_player(items=["Cheater's Insurance"])
    player.back_alley_shortcut()
    print(bright(red("Testing back_alley_shortcut with Fate Reader")))
    player = new_player(items=['Fate Reader'])
    player.back_alley_shortcut()
    print(bright(red("Testing back_alley_shortcut with Fire Launcher")))
    player = new_player(items=['Fire Launcher'])
    player.back_alley_shortcut()
    print(bright(red("Testing back_alley_shortcut with Flask of No Bust")))
    player = new_player(items=['Flask of No Bust'])
    player.back_alley_shortcut()
    print(bright(red("Testing back_alley_shortcut with Flask of Second Chance")))
    player = new_player(items=['Flask of Second Chance'])
    player.back_alley_shortcut()
    print(bright(red("Testing back_alley_shortcut with Forged Documents")))
    player = new_player(items=['Forged Documents'])
    player.back_alley_shortcut()
    print(bright(red("Testing back_alley_shortcut with Gentleman's Charm")))
    player = new_player(items=["Gentleman's Charm"])
    player.back_alley_shortcut()
    print(bright(red("Testing back_alley_shortcut with Guardian Angel")))
    player = new_player(items=['Guardian Angel'])
    player.back_alley_shortcut()
    print(bright(red("Testing back_alley_shortcut with Health Indicator")))
    player = new_player(items=['Health Indicator'])
    player.back_alley_shortcut()
    print(bright(red("Testing back_alley_shortcut with Health Manipulator")))
    player = new_player(items=['Health Manipulator'])
    player.back_alley_shortcut()
    print(bright(red("Testing back_alley_shortcut with Improvised Trap")))
    player = new_player(items=['Improvised Trap'])
    player.back_alley_shortcut()
    print(bright(red("Testing back_alley_shortcut with Intelligence Dossier")))
    player = new_player(items=['Intelligence Dossier'])
    player.back_alley_shortcut()
    print(bright(red("Testing back_alley_shortcut with Invisible Cloak")))
    player = new_player(items=['Invisible Cloak'])
    player.back_alley_shortcut()
    print(bright(red("Testing back_alley_shortcut with Kingpin Look")))
    player = new_player(items=['Kingpin Look'])
    player.back_alley_shortcut()
    print(bright(red("Testing back_alley_shortcut with Low-Profile Outfit")))
    player = new_player(items=['Low-Profile Outfit'])
    player.back_alley_shortcut()
    print(bright(red("Testing back_alley_shortcut with Lucid Dreaming Kit")))
    player = new_player(items=['Lucid Dreaming Kit'])
    player.back_alley_shortcut()
    print(bright(red("Testing back_alley_shortcut with Master Key")))
    player = new_player(items=['Master Key'])
    player.back_alley_shortcut()
    print(bright(red("Testing back_alley_shortcut with Mind Shield")))
    player = new_player(items=['Mind Shield'])
    player.back_alley_shortcut()
    print(bright(red("Testing back_alley_shortcut with Miracle Lube")))
    player = new_player(items=['Miracle Lube'])
    player.back_alley_shortcut()
    print(bright(red("Testing back_alley_shortcut with Necronomicon")))
    player = new_player(items=['Necronomicon'])
    player.back_alley_shortcut()
    print(bright(red("Testing back_alley_shortcut with Night Scope")))
    player = new_player(items=['Night Scope'])
    player.back_alley_shortcut()
    print(bright(red("Testing back_alley_shortcut with Pepper Spray")))
    player = new_player(items=['Pepper Spray'])
    player.back_alley_shortcut()
    print(bright(red("Testing back_alley_shortcut with Phoenix Feather")))
    player = new_player(items=['Phoenix Feather'])
    player.back_alley_shortcut()
    print(bright(red("Testing back_alley_shortcut with Quiet Bunny Slippers")))
    player = new_player(items=['Quiet Bunny Slippers'])
    player.back_alley_shortcut()
    print(bright(red("Testing back_alley_shortcut with Quiet Sneakers")))
    player = new_player(items=['Quiet Sneakers'])
    player.back_alley_shortcut()
    print(bright(red("Testing back_alley_shortcut with Road Flare Torch")))
    player = new_player(items=['Road Flare Torch'])
    player.back_alley_shortcut()
    print(bright(red("Testing back_alley_shortcut with Rolling Fortress")))
    player = new_player(items=['Rolling Fortress'])
    player.back_alley_shortcut()
    print(bright(red("Testing back_alley_shortcut with Running Shoes")))
    player = new_player(items=['Running Shoes'])
    player.back_alley_shortcut()
    print(bright(red("Testing back_alley_shortcut with Scrap Armor")))
    player = new_player(items=['Scrap Armor'])
    player.back_alley_shortcut()
    print(bright(red("Testing back_alley_shortcut with Shiv")))
    player = new_player(items=['Shiv'])
    player.back_alley_shortcut()
    print(bright(red("Testing back_alley_shortcut with Skeleton Key")))
    player = new_player(items=['Skeleton Key'])
    player.back_alley_shortcut()
    print(bright(red("Testing back_alley_shortcut with Smelling Salts")))
    player = new_player(items=['Smelling Salts'])
    player.back_alley_shortcut()
    print(bright(red("Testing back_alley_shortcut with Splint")))
    player = new_player(items=['Splint'])
    player.back_alley_shortcut()
    print(bright(red("Testing back_alley_shortcut with Stink Bomb")))
    player = new_player(items=['Stink Bomb'])
    player.back_alley_shortcut()
    print(bright(red("Testing back_alley_shortcut with Street Fighter Set")))
    player = new_player(items=['Street Fighter Set'])
    player.back_alley_shortcut()
    print(bright(red("Testing back_alley_shortcut with Surveillance Suite")))
    player = new_player(items=['Surveillance Suite'])
    player.back_alley_shortcut()
    print(bright(red("Testing back_alley_shortcut with Tattered Cloak")))
    player = new_player(items=['Tattered Cloak'])
    player.back_alley_shortcut()
    print(bright(red("Testing back_alley_shortcut with Tear Gas")))
    player = new_player(items=['Tear Gas'])
    player.back_alley_shortcut()
    print(bright(red("Testing back_alley_shortcut with Velvet Gloves")))
    player = new_player(items=['Velvet Gloves'])
    player.back_alley_shortcut()
    print(bright(red("Testing back_alley_shortcut with White Feather")))
    player = new_player(items=['White Feather'])
    player.back_alley_shortcut()
    print(bright(red("Testing back_alley_shortcut with Worn Gloves")))
    player = new_player(items=['Worn Gloves'])
    player.back_alley_shortcut()
    print(bright(red("Testing back_alley_shortcut with Wound Salve")))
    player = new_player(items=['Wound Salve'])
    player.back_alley_shortcut()

def bridge_angel_returns():
    print(bright(red("TESTING bridge_angel_returns with no items")))
    player = new_player()
    player.bridge_angel_returns()

def bridge_contemplation():
    print(bright(red("TESTING bridge_contemplation with no items")))
    player = new_player()
    player.bridge_contemplation()

def burn_scars_infection():
    print(bright(red("TESTING burn_scars_infection with no items")))
    player = new_player()
    player.burn_scars_infection()

def burn_scars_stares():
    print(bright(red("TESTING burn_scars_stares with no items")))
    player = new_player()
    player.burn_scars_stares()

def call_bridge_angel():
    print(bright(red("TESTING call_bridge_angel with no items")))
    player = new_player()
    player.call_bridge_angel()
    print(bright(red("Testing call_bridge_angel with Angel's Number")))
    player = new_player(items=["Angel's Number"])
    player.call_bridge_angel()

def cancer_diagnosis():
    print(bright(red("TESTING cancer_diagnosis with no items")))
    player = new_player()
    player.cancer_diagnosis()

def car_explosion():
    print(bright(red("TESTING car_explosion with no items")))
    player = new_player()
    player.car_explosion()

def carbon_monoxide():
    print(bright(red("TESTING carbon_monoxide with no items")))
    player = new_player()
    player.carbon_monoxide()
    print(bright(red("Testing carbon_monoxide with Faulty Insurance")))
    player = new_player(items=['Faulty Insurance'])
    player.carbon_monoxide()
    print(bright(red("Testing carbon_monoxide with Real Insurance")))
    player = new_player(items=['Real Insurance'])
    player.carbon_monoxide()

def casino_hitman():
    print(bright(red("TESTING casino_hitman with no items")))
    player = new_player()
    player.casino_hitman()
    print(bright(red("Testing casino_hitman with Dealer's Grudge")))
    player = new_player(items=["Dealer's Grudge"])
    player.casino_hitman()
    print(bright(red("Testing casino_hitman with Dealer's Mercy")))
    player = new_player(items=["Dealer's Mercy"])
    player.casino_hitman()
    print(bright(red("Testing casino_hitman with Ghost Protocol")))
    player = new_player(items=['Ghost Protocol'])
    player.casino_hitman()
    print(bright(red("Testing casino_hitman with Last Breath Locket")))
    player = new_player(items=['Last Breath Locket'])
    player.casino_hitman()
    print(bright(red("Testing casino_hitman with Phoenix Feather")))
    player = new_player(items=['Phoenix Feather'])
    player.casino_hitman()
    print(bright(red("Testing casino_hitman with Road Warrior Armor")))
    player = new_player(items=['Road Warrior Armor'])
    player.casino_hitman()
    print(bright(red("Testing casino_hitman with Shiv")))
    player = new_player(items=['Shiv'])
    player.casino_hitman()
    print(bright(red("Testing casino_hitman with White Feather")))
    player = new_player(items=['White Feather'])
    player.casino_hitman()

def casino_overdose():
    print(bright(red("TESTING casino_overdose with no items")))
    player = new_player()
    player.casino_overdose()
    print(bright(red("Testing casino_overdose with Evidence Kit")))
    player = new_player(items=['Evidence Kit'])
    player.casino_overdose()
    print(bright(red("Testing casino_overdose with Flask of Second Chance")))
    player = new_player(items=['Flask of Second Chance'])
    player.casino_overdose()

def cocaine_crash():
    print(bright(red("TESTING cocaine_crash with no items")))
    player = new_player()
    player.cocaine_crash()

def cocaine_heart_attack():
    print(bright(red("TESTING cocaine_heart_attack with no items")))
    player = new_player()
    player.cocaine_heart_attack()

def cocaine_temptation():
    print(bright(red("TESTING cocaine_temptation with no items")))
    player = new_player()
    player.cocaine_temptation()
    print(bright(red("Testing cocaine_temptation with Bag of Cocaine")))
    player = new_player(items=['Bag of Cocaine'])
    player.cocaine_temptation()

def devils_bargain_consequence():
    print(bright(red("TESTING devils_bargain_consequence with no items")))
    player = new_player()
    player.devils_bargain_consequence()
    print(bright(red("Testing devils_bargain_consequence with Dark Pact Reliquary")))
    player = new_player(items=['Dark Pact Reliquary'])
    player.devils_bargain_consequence()

def dog_bite_rabies_scare():
    print(bright(red("TESTING dog_bite_rabies_scare with no items")))
    player = new_player()
    player.dog_bite_rabies_scare()

def drowning_dream():
    print(bright(red("TESTING drowning_dream with no items")))
    player = new_player()
    player.drowning_dream()
    print(bright(red("Testing drowning_dream with Distress Beacon")))
    player = new_player(items=['Distress Beacon'])
    player.drowning_dream()

def drug_dealer_encounter():
    print(bright(red("TESTING drug_dealer_encounter with no items")))
    player = new_player()
    player.drug_dealer_encounter()
    print(bright(red("Testing drug_dealer_encounter with Blackmail Letter")))
    player = new_player(items=['Blackmail Letter'])
    player.drug_dealer_encounter()
    print(bright(red("Testing drug_dealer_encounter with Enchanted Vintage")))
    player = new_player(items=['Enchanted Vintage'])
    player.drug_dealer_encounter()
    print(bright(red("Testing drug_dealer_encounter with New Identity")))
    player = new_player(items=['New Identity'])
    player.drug_dealer_encounter()
    print(bright(red("Testing drug_dealer_encounter with Running Shoes")))
    player = new_player(items=['Running Shoes'])
    player.drug_dealer_encounter()
    print(bright(red("Testing drug_dealer_encounter with Tire Ready Kit")))
    player = new_player(items=['Tire Ready Kit'])
    player.drug_dealer_encounter()

def electrocution_hazard():
    print(bright(red("TESTING electrocution_hazard with no items")))
    player = new_player()
    player.electrocution_hazard()
    print(bright(red("Testing electrocution_hazard with Plated Vest")))
    player = new_player(items=['Plated Vest'])
    player.electrocution_hazard()
    print(bright(red("Testing electrocution_hazard with Quiet Bunny Slippers")))
    player = new_player(items=['Quiet Bunny Slippers'])
    player.electrocution_hazard()
    print(bright(red("Testing electrocution_hazard with Quiet Sneakers")))
    player = new_player(items=['Quiet Sneakers'])
    player.electrocution_hazard()
    print(bright(red("Testing electrocution_hazard with Road Warrior Plate")))
    player = new_player(items=['Road Warrior Plate'])
    player.electrocution_hazard()
    print(bright(red("Testing electrocution_hazard with Scrap Armor")))
    player = new_player(items=['Scrap Armor'])
    player.electrocution_hazard()

def food_poisoning():
    print(bright(red("TESTING food_poisoning with no items")))
    player = new_player()
    player.food_poisoning()

def fuel_leak_fire():
    print(bright(red("TESTING fuel_leak_fire with no items")))
    player = new_player()
    player.fuel_leak_fire()
    print(bright(red("Testing fuel_leak_fire with Gas Mask")))
    player = new_player(items=['Gas Mask'])
    player.fuel_leak_fire()

def fuel_leak_fixed():
    print(bright(red("TESTING fuel_leak_fixed with no items")))
    player = new_player()
    player.fuel_leak_fixed()

def gas_station_hero_interview():
    print(bright(red("TESTING gas_station_hero_interview with no items")))
    player = new_player()
    player.gas_station_hero_interview()

def gas_station_hero_recognized():
    print(bright(red("TESTING gas_station_hero_recognized with no items")))
    player = new_player()
    player.gas_station_hero_recognized()

def gas_station_robbery():
    print(bright(red("TESTING gas_station_robbery with no items")))
    player = new_player()
    player.gas_station_robbery()
    print(bright(red("Testing gas_station_robbery with All-Access Pass")))
    player = new_player(items=['All-Access Pass'])
    player.gas_station_robbery()
    print(bright(red("Testing gas_station_robbery with Forged Documents")))
    player = new_player(items=['Forged Documents'])
    player.gas_station_robbery()
    print(bright(red("Testing gas_station_robbery with Ghost Protocol")))
    player = new_player(items=['Ghost Protocol'])
    player.gas_station_robbery()
    print(bright(red("Testing gas_station_robbery with Kingpin Look")))
    player = new_player(items=['Kingpin Look'])
    player.gas_station_robbery()
    print(bright(red("Testing gas_station_robbery with Marvin's Eye")))
    player = new_player(items=["Marvin's Eye"])
    player.gas_station_robbery()
    print(bright(red("Testing gas_station_robbery with Road Warrior Armor")))
    player = new_player(items=['Road Warrior Armor'])
    player.gas_station_robbery()
    print(bright(red("Testing gas_station_robbery with Sneaky Peeky Goggles")))
    player = new_player(items=['Sneaky Peeky Goggles'])
    player.gas_station_robbery()
    print(bright(red("Testing gas_station_robbery with Sneaky Peeky Shades")))
    player = new_player(items=['Sneaky Peeky Shades'])
    player.gas_station_robbery()

def gut_wound_complications():
    print(bright(red("TESTING gut_wound_complications with no items")))
    player = new_player()
    player.gut_wound_complications()

def heart_attack_scare():
    print(bright(red("TESTING heart_attack_scare with no items")))
    player = new_player()
    player.heart_attack_scare()

def heart_condition_flare():
    print(bright(red("TESTING heart_condition_flare with no items")))
    player = new_player()
    player.heart_condition_flare()

def knife_wound_infection():
    print(bright(red("TESTING knife_wound_infection with no items")))
    player = new_player()
    player.knife_wound_infection()
    print(bright(red("Testing knife_wound_infection with Wound Salve")))
    player = new_player(items=['Wound Salve'])
    player.knife_wound_infection()

def loan_shark_visit():
    print(bright(red("TESTING loan_shark_visit with no items")))
    player = new_player()
    player.loan_shark_visit()
    print(bright(red("Testing loan_shark_visit with Gold Chain")))
    player = new_player(items=['Gold Chain'])
    player.loan_shark_visit()
    print(bright(red("Testing loan_shark_visit with King of the Road")))
    player = new_player(items=['King of the Road'])
    player.loan_shark_visit()
    print(bright(red("Testing loan_shark_visit with Master of Games")))
    player = new_player(items=['Master of Games'])
    player.loan_shark_visit()

def necronomicon_reading():
    print(bright(red("TESTING necronomicon_reading with no items")))
    player = new_player()
    player.necronomicon_reading()
    print(bright(red("Testing necronomicon_reading with Necronomicon")))
    player = new_player(items=['Necronomicon'])
    player.necronomicon_reading()

def old_gambling_buddy():
    print(bright(red("TESTING old_gambling_buddy with no items")))
    player = new_player()
    player.old_gambling_buddy()

def organ_harvester():
    print(bright(red("TESTING organ_harvester with no items")))
    player = new_player()
    player.organ_harvester()
    print(bright(red("Testing organ_harvester with Ghost Protocol")))
    player = new_player(items=['Ghost Protocol'])
    player.organ_harvester()
    print(bright(red("Testing organ_harvester with Third Eye")))
    player = new_player(items=['Third Eye'])
    player.organ_harvester()

def painkiller_dealer_returns():
    print(bright(red("TESTING painkiller_dealer_returns with no items")))
    player = new_player()
    player.painkiller_dealer_returns()

def painkiller_overdose():
    print(bright(red("TESTING painkiller_overdose with no items")))
    player = new_player()
    player.painkiller_overdose()

def painkiller_withdrawal():
    print(bright(red("TESTING painkiller_withdrawal with no items")))
    player = new_player()
    player.painkiller_withdrawal()

def shoulder_chronic_pain():
    print(bright(red("TESTING shoulder_chronic_pain with no items")))
    player = new_player()
    player.shoulder_chronic_pain()

def shoulder_painkiller_addiction():
    print(bright(red("TESTING shoulder_painkiller_addiction with no items")))
    player = new_player()
    player.shoulder_painkiller_addiction()

def soulless_emptiness():
    print(bright(red("TESTING soulless_emptiness with no items")))
    player = new_player()
    player.soulless_emptiness()

def soulless_mirror():
    print(bright(red("TESTING soulless_mirror with no items")))
    player = new_player()
    player.soulless_mirror()

def soulless_recognition():
    print(bright(red("TESTING soulless_recognition with no items")))
    player = new_player()
    player.soulless_recognition()

def survivor_guilt():
    print(bright(red("TESTING survivor_guilt with no items")))
    player = new_player()
    player.survivor_guilt()

def the_anniversary_loss():
    print(bright(red("TESTING the_anniversary_loss with no items")))
    player = new_player()
    player.the_anniversary_loss()

def the_bridge_call():
    print(bright(red("TESTING the_bridge_call with no items")))
    player = new_player()
    player.the_bridge_call()
    print(bright(red("Testing the_bridge_call with Flask of Second Chance")))
    player = new_player(items=['Flask of Second Chance'])
    player.the_bridge_call()

def the_confession():
    print(bright(red("TESTING the_confession with no items")))
    player = new_player()
    player.the_confession()

def the_desperate_gambler():
    print(bright(red("TESTING the_desperate_gambler with no items")))
    player = new_player()
    player.the_desperate_gambler()
    print(bright(red("Testing the_desperate_gambler with Flask of Split Serum")))
    player = new_player(items=['Flask of Split Serum'])
    player.the_desperate_gambler()
    print(bright(red("Testing the_desperate_gambler with Phoenix Feather")))
    player = new_player(items=['Phoenix Feather'])
    player.the_desperate_gambler()
    print(bright(red("Testing the_desperate_gambler with Voice Soother")))
    player = new_player(items=['Voice Soother'])
    player.the_desperate_gambler()
    print(bright(red("Testing the_desperate_gambler with White Feather")))
    player = new_player(items=['White Feather'])
    player.the_desperate_gambler()

def the_high_roller_suicide():
    print(bright(red("TESTING the_high_roller_suicide with no items")))
    player = new_player()
    player.the_high_roller_suicide()

def the_relapse():
    print(bright(red("TESTING the_relapse with no items")))
    player = new_player()
    player.the_relapse()
    print(bright(red("Testing the_relapse with Flask of Dealer's Whispers")))
    player = new_player(items=["Flask of Dealer's Whispers"])
    player.the_relapse()
    print(bright(red("Testing the_relapse with Flask of Imminent Blackjack")))
    player = new_player(items=['Flask of Imminent Blackjack'])
    player.the_relapse()
    print(bright(red("Testing the_relapse with Flask of Pocket Aces")))
    player = new_player(items=['Flask of Pocket Aces'])
    player.the_relapse()

def the_scar_story():
    print(bright(red("TESTING the_scar_story with no items")))
    player = new_player()
    player.the_scar_story()

def the_winning_streak_paranoia():
    print(bright(red("TESTING the_winning_streak_paranoia with no items")))
    player = new_player()
    player.the_winning_streak_paranoia()
    print(bright(red("Testing the_winning_streak_paranoia with Worry Stone")))
    player = new_player(items=['Worry Stone'])
    player.the_winning_streak_paranoia()

def voodoo_doll_temptation():
    print(bright(red("TESTING voodoo_doll_temptation with no items")))
    player = new_player()
    player.voodoo_doll_temptation()
    print(bright(red("Testing voodoo_doll_temptation with Voodoo Doll")))
    player = new_player(items=['Voodoo Doll'])
    player.voodoo_doll_temptation()

def weakened_immune_cold():
    print(bright(red("TESTING weakened_immune_cold with no items")))
    player = new_player()
    player.weakened_immune_cold()

def weakened_immune_pneumonia():
    print(bright(red("TESTING weakened_immune_pneumonia with no items")))
    player = new_player()
    player.weakened_immune_pneumonia()

def withdrawal_nightmare():
    print(bright(red("TESTING withdrawal_nightmare with no items")))
    player = new_player()
    player.withdrawal_nightmare()

def wrong_item_necronomicon_loan_shark():
    print(bright(red("TESTING wrong_item_necronomicon_loan_shark with no items")))
    player = new_player()
    player.wrong_item_necronomicon_loan_shark()
    print(bright(red("Testing wrong_item_necronomicon_loan_shark with Necronomicon")))
    player = new_player(items=['Necronomicon'])
    player.wrong_item_necronomicon_loan_shark()

def wrong_item_road_flares_stealth():
    print(bright(red("TESTING wrong_item_road_flares_stealth with no items")))
    player = new_player()
    player.wrong_item_road_flares_stealth()
    print(bright(red("Testing wrong_item_road_flares_stealth with Road Flares")))
    player = new_player(items=['Road Flares'])
    player.wrong_item_road_flares_stealth()


"""story.events_day_items.py"""
def ace_of_spades_blackjack_omen():
    print(bright(red("TESTING ace_of_spades_blackjack_omen with no items")))
    player = new_player()
    player.ace_of_spades_blackjack_omen()
    print(bright(red("Testing ace_of_spades_blackjack_omen with Ace of Spades")))
    player = new_player(items=['Ace of Spades'])
    player.ace_of_spades_blackjack_omen()

def alien_crystal_event():
    print(bright(red("TESTING alien_crystal_event with no items")))
    player = new_player()
    player.alien_crystal_event()
    print(bright(red("Testing alien_crystal_event with Alien Crystal")))
    player = new_player(items=['Alien Crystal'])
    player.alien_crystal_event()

def animal_bait_companion():
    print(bright(red("TESTING animal_bait_companion with no items")))
    player = new_player()
    player.animal_bait_companion()
    print(bright(red("Testing animal_bait_companion with Animal Bait")))
    player = new_player(items=['Animal Bait'])
    player.animal_bait_companion()
    print(bright(red("Testing animal_bait_companion with Beast Tamer Kit")))
    player = new_player(items=['Beast Tamer Kit'])
    player.animal_bait_companion()

def animal_magnetism_predator():
    print(bright(red("TESTING animal_magnetism_predator with no items")))
    player = new_player()
    player.animal_magnetism_predator()
    print(bright(red("Testing animal_magnetism_predator with Animal Magnetism")))
    player = new_player(items=['Animal Magnetism'])
    player.animal_magnetism_predator()
    print(bright(red("Testing animal_magnetism_predator with Beast Tamer Kit")))
    player = new_player(items=['Beast Tamer Kit'])
    player.animal_magnetism_predator()

def animal_magnetism_recruit():
    print(bright(red("TESTING animal_magnetism_recruit with no items")))
    player = new_player()
    player.animal_magnetism_recruit()
    print(bright(red("Testing animal_magnetism_recruit with Animal Magnetism")))
    player = new_player(items=['Animal Magnetism'])
    player.animal_magnetism_recruit()
    print(bright(red("Testing animal_magnetism_recruit with Beast Tamer Kit")))
    player = new_player(items=['Beast Tamer Kit'])
    player.animal_magnetism_recruit()

def antacid_business_dinner():
    print(bright(red("TESTING antacid_business_dinner with no items")))
    player = new_player()
    player.antacid_business_dinner()
    print(bright(red("Testing antacid_business_dinner with Antacid Brew")))
    player = new_player(items=['Antacid Brew'])
    player.antacid_business_dinner()

def apartment_key_visit():
    print(bright(red("TESTING apartment_key_visit with no items")))
    player = new_player()
    player.apartment_key_visit()
    print(bright(red("Testing apartment_key_visit with Apartment Key")))
    player = new_player(items=['Apartment Key'])
    player.apartment_key_visit()

def aristocrat_cold_elegance():
    print(bright(red("TESTING aristocrat_cold_elegance with no items")))
    player = new_player()
    player.aristocrat_cold_elegance()
    print(bright(red("Testing aristocrat_cold_elegance with Aristocrat's Touch")))
    player = new_player(items=["Aristocrat's Touch"])
    player.aristocrat_cold_elegance()
    print(bright(red("Testing aristocrat_cold_elegance with Old Money Identity")))
    player = new_player(items=['Old Money Identity'])
    player.aristocrat_cold_elegance()

def beach_bum_heatwave():
    print(bright(red("TESTING beach_bum_heatwave with no items")))
    player = new_player()
    player.beach_bum_heatwave()
    print(bright(red("Testing beach_bum_heatwave with All-Weather Armor")))
    player = new_player(items=['All-Weather Armor'])
    player.beach_bum_heatwave()
    print(bright(red("Testing beach_bum_heatwave with Beach Bum Disguise")))
    player = new_player(items=['Beach Bum Disguise'])
    player.beach_bum_heatwave()

def beach_bum_tribe():
    print(bright(red("TESTING beach_bum_tribe with no items")))
    player = new_player()
    player.beach_bum_tribe()
    print(bright(red("Testing beach_bum_tribe with All-Weather Armor")))
    player = new_player(items=['All-Weather Armor'])
    player.beach_bum_tribe()
    print(bright(red("Testing beach_bum_tribe with Beach Bum Disguise")))
    player = new_player(items=['Beach Bum Disguise'])
    player.beach_bum_tribe()

def beach_bum_yacht_party():
    print(bright(red("TESTING beach_bum_yacht_party with no items")))
    player = new_player()
    player.beach_bum_yacht_party()
    print(bright(red("Testing beach_bum_yacht_party with All-Weather Armor")))
    player = new_player(items=['All-Weather Armor'])
    player.beach_bum_yacht_party()
    print(bright(red("Testing beach_bum_yacht_party with Beach Bum Disguise")))
    player = new_player(items=['Beach Bum Disguise'])
    player.beach_bum_yacht_party()

def beach_romance_call():
    print(bright(red("TESTING beach_romance_call with no items")))
    player = new_player()
    player.beach_romance_call()
    print(bright(red("Testing beach_romance_call with Beach Romance Number")))
    player = new_player(items=['Beach Romance Number'])
    player.beach_romance_call()

def binocular_scope_discovery():
    print(bright(red("TESTING binocular_scope_discovery with no items")))
    player = new_player()
    player.binocular_scope_discovery()
    print(bright(red("Testing binocular_scope_discovery with Binocular Scope")))
    player = new_player(items=['Binocular Scope'])
    player.binocular_scope_discovery()

def blackmail_letter_extortion():
    print(bright(red("TESTING blackmail_letter_extortion with no items")))
    player = new_player()
    player.blackmail_letter_extortion()
    print(bright(red("Testing blackmail_letter_extortion with Blackmail Letter")))
    player = new_player(items=['Blackmail Letter'])
    player.blackmail_letter_extortion()

def blank_check_opportunity():
    print(bright(red("TESTING blank_check_opportunity with no items")))
    player = new_player()
    player.blank_check_opportunity()
    print(bright(red("Testing blank_check_opportunity with Blank Check")))
    player = new_player(items=['Blank Check'])
    player.blank_check_opportunity()

def bottle_of_tomorrow_use():
    print(bright(red("TESTING bottle_of_tomorrow_use with no items")))
    player = new_player()
    player.bottle_of_tomorrow_use()
    print(bright(red("Testing bottle_of_tomorrow_use with Bottle of Tomorrow")))
    player = new_player(items=['Bottle of Tomorrow'])
    player.bottle_of_tomorrow_use()

def brass_knuckles_brawl():
    print(bright(red("TESTING brass_knuckles_brawl with no items")))
    player = new_player()
    player.brass_knuckles_brawl()
    print(bright(red("Testing brass_knuckles_brawl with Brass Knuckles")))
    player = new_player(items=['Brass Knuckles'])
    player.brass_knuckles_brawl()
    print(bright(red("Testing brass_knuckles_brawl with Street Fighter Set")))
    player = new_player(items=['Street Fighter Set'])
    player.brass_knuckles_brawl()

def capture_fairy_release():
    print(bright(red("TESTING capture_fairy_release with no items")))
    player = new_player()
    player.capture_fairy_release()
    print(bright(red("Testing capture_fairy_release with Captured Fairy")))
    player = new_player(items=['Captured Fairy'])
    player.capture_fairy_release()
    print(bright(red("Testing capture_fairy_release with Magic Acorn")))
    player = new_player(items=['Magic Acorn'])
    player.capture_fairy_release()

def cool_down_car_overheat():
    print(bright(red("TESTING cool_down_car_overheat with no items")))
    player = new_player()
    player.cool_down_car_overheat()
    print(bright(red("Testing cool_down_car_overheat with Cool Down Kit")))
    player = new_player(items=['Cool Down Kit'])
    player.cool_down_car_overheat()

def council_feather_blessing():
    print(bright(red("TESTING council_feather_blessing with no items")))
    player = new_player()
    player.council_feather_blessing()
    print(bright(red("Testing council_feather_blessing with Council Feather")))
    player = new_player(items=['Council Feather'])
    player.council_feather_blessing()

def cowboy_jacket_encounter():
    print(bright(red("TESTING cowboy_jacket_encounter with no items")))
    player = new_player()
    player.cowboy_jacket_encounter()
    print(bright(red("Testing cowboy_jacket_encounter with Cowboy Jacket")))
    player = new_player(items=['Cowboy Jacket'])
    player.cowboy_jacket_encounter()

def dealer_joker_revelation():
    print(bright(red("TESTING dealer_joker_revelation with no items")))
    player = new_player()
    player.dealer_joker_revelation()
    print(bright(red("Testing dealer_joker_revelation with Dealer's Joker")))
    player = new_player(items=["Dealer's Joker"])
    player.dealer_joker_revelation()

def deck_of_cards_street_game():
    print(bright(red("TESTING deck_of_cards_street_game with no items")))
    player = new_player()
    player.deck_of_cards_street_game()
    print(bright(red("Testing deck_of_cards_street_game with Deck of Cards")))
    player = new_player(items=['Deck of Cards'])
    player.deck_of_cards_street_game()

def devils_deck_gambling():
    print(bright(red("TESTING devils_deck_gambling with no items")))
    player = new_player()
    player.devils_deck_gambling()
    print(bright(red("Testing devils_deck_gambling with Cheater's Insurance")))
    player = new_player(items=["Cheater's Insurance"])
    player.devils_deck_gambling()
    print(bright(red("Testing devils_deck_gambling with Devil's Deck")))
    player = new_player(items=["Devil's Deck"])
    player.devils_deck_gambling()

def dimensional_coin_flip():
    print(bright(red("TESTING dimensional_coin_flip with no items")))
    player = new_player()
    player.dimensional_coin_flip()
    print(bright(red("Testing dimensional_coin_flip with Dimensional Coin")))
    player = new_player(items=['Dimensional Coin'])
    player.dimensional_coin_flip()

def dream_catcher_night():
    print(bright(red("TESTING dream_catcher_night with no items")))
    player = new_player()
    player.dream_catcher_night()
    print(bright(red("Testing dream_catcher_night with Dream Catcher")))
    player = new_player(items=['Dream Catcher'])
    player.dream_catcher_night()

def eldritch_candle_entity():
    print(bright(red("TESTING eldritch_candle_entity with no items")))
    player = new_player()
    player.eldritch_candle_entity()
    print(bright(red("Testing eldritch_candle_entity with Dark Pact Reliquary")))
    player = new_player(items=['Dark Pact Reliquary'])
    player.eldritch_candle_entity()
    print(bright(red("Testing eldritch_candle_entity with Eldritch Candle")))
    player = new_player(items=['Eldritch Candle'])
    player.eldritch_candle_entity()

def emergency_blanket_cold_night():
    print(bright(red("TESTING emergency_blanket_cold_night with no items")))
    player = new_player()
    player.emergency_blanket_cold_night()
    print(bright(red("Testing emergency_blanket_cold_night with Emergency Blanket")))
    player = new_player(items=['Emergency Blanket'])
    player.emergency_blanket_cold_night()

def emp_device_pursuit():
    print(bright(red("TESTING emp_device_pursuit with no items")))
    player = new_player()
    player.emp_device_pursuit()
    print(bright(red("Testing emp_device_pursuit with EMP Device")))
    player = new_player(items=['EMP Device'])
    player.emp_device_pursuit()
    print(bright(red("Testing emp_device_pursuit with Pursuit Package")))
    player = new_player(items=['Pursuit Package'])
    player.emp_device_pursuit()

def empty_locket_memory():
    print(bright(red("TESTING empty_locket_memory with no items")))
    player = new_player()
    player.empty_locket_memory()
    print(bright(red("Testing empty_locket_memory with Empty Locket")))
    player = new_player(items=['Empty Locket'])
    player.empty_locket_memory()
    print(bright(red("Testing empty_locket_memory with Old Photograph")))
    player = new_player(items=['Old Photograph'])
    player.empty_locket_memory()

def enchanted_vintage_party():
    print(bright(red("TESTING enchanted_vintage_party with no items")))
    player = new_player()
    player.enchanted_vintage_party()
    print(bright(red("Testing enchanted_vintage_party with Enchanted Vintage")))
    player = new_player(items=['Enchanted Vintage'])
    player.enchanted_vintage_party()
    print(bright(red("Testing enchanted_vintage_party with Master of Games")))
    player = new_player(items=['Master of Games'])
    player.enchanted_vintage_party()

def evidence_kit_crime():
    print(bright(red("TESTING evidence_kit_crime with no items")))
    player = new_player()
    player.evidence_kit_crime()
    print(bright(red("Testing evidence_kit_crime with Evidence Kit")))
    player = new_player(items=['Evidence Kit'])
    player.evidence_kit_crime()

def fake_flower_gift():
    print(bright(red("TESTING fake_flower_gift with no items")))
    player = new_player()
    player.fake_flower_gift()
    print(bright(red("Testing fake_flower_gift with Fake Flower")))
    player = new_player(items=['Fake Flower'])
    player.fake_flower_gift()

def feelgood_bottle_moment():
    print(bright(red("TESTING feelgood_bottle_moment with no items")))
    player = new_player()
    player.feelgood_bottle_moment()
    print(bright(red("Testing feelgood_bottle_moment with Feelgood Bottle")))
    player = new_player(items=['Feelgood Bottle'])
    player.feelgood_bottle_moment()

def fire_starter_campfire():
    print(bright(red("TESTING fire_starter_campfire with no items")))
    player = new_player()
    player.fire_starter_campfire()
    print(bright(red("Testing fire_starter_campfire with Fire Starter Kit")))
    player = new_player(items=['Fire Starter Kit'])
    player.fire_starter_campfire()

def fishing_day():
    print(bright(red("TESTING fishing_day with no items")))
    player = new_player()
    player.fishing_day()
    print(bright(red("Testing fishing_day with Fishing Rod")))
    player = new_player(items=['Fishing Rod'])
    player.fishing_day()

def forged_documents_police():
    print(bright(red("TESTING forged_documents_police with no items")))
    player = new_player()
    player.forged_documents_police()
    print(bright(red("Testing forged_documents_police with Forged Documents")))
    player = new_player(items=['Forged Documents'])
    player.forged_documents_police()
    print(bright(red("Testing forged_documents_police with New Identity")))
    player = new_player(items=['New Identity'])
    player.forged_documents_police()

def fortune_cards_warning():
    print(bright(red("TESTING fortune_cards_warning with no items")))
    player = new_player()
    player.fortune_cards_warning()
    print(bright(red("Testing fortune_cards_warning with Fate Reader")))
    player = new_player(items=['Fate Reader'])
    player.fortune_cards_warning()
    print(bright(red("Testing fortune_cards_warning with Fortune Cards")))
    player = new_player(items=['Fortune Cards'])
    player.fortune_cards_warning()

def found_phone_call():
    print(bright(red("TESTING found_phone_call with no items")))
    player = new_player()
    player.found_phone_call()
    print(bright(red("Testing found_phone_call with Found Phone")))
    player = new_player(items=['Found Phone'])
    player.found_phone_call()

def gamblers_aura_blackjack():
    print(bright(red("TESTING gamblers_aura_blackjack with no items")))
    player = new_player()
    player.gamblers_aura_blackjack()
    print(bright(red("Testing gamblers_aura_blackjack with Devil's Deck")))
    player = new_player(items=["Devil's Deck"])
    player.gamblers_aura_blackjack()
    print(bright(red("Testing gamblers_aura_blackjack with Gambler's Aura")))
    player = new_player(items=["Gambler's Aura"])
    player.gamblers_aura_blackjack()
    print(bright(red("Testing gamblers_aura_blackjack with Moonlit Fortune")))
    player = new_player(items=['Moonlit Fortune'])
    player.gamblers_aura_blackjack()

def gas_mask_chemical():
    print(bright(red("TESTING gas_mask_chemical with no items")))
    player = new_player()
    player.gas_mask_chemical()
    print(bright(red("Testing gas_mask_chemical with Gas Mask")))
    player = new_player(items=['Gas Mask'])
    player.gas_mask_chemical()
    print(bright(red("Testing gas_mask_chemical with Hazmat Suit")))
    player = new_player(items=['Hazmat Suit'])
    player.gas_mask_chemical()

def gas_mask_fire_rescue():
    print(bright(red("TESTING gas_mask_fire_rescue with no items")))
    player = new_player()
    player.gas_mask_fire_rescue()
    print(bright(red("Testing gas_mask_fire_rescue with Gas Mask")))
    player = new_player(items=['Gas Mask'])
    player.gas_mask_fire_rescue()
    print(bright(red("Testing gas_mask_fire_rescue with Hazmat Suit")))
    player = new_player(items=['Hazmat Suit'])
    player.gas_mask_fire_rescue()

def gas_mask_toxic_spill():
    print(bright(red("TESTING gas_mask_toxic_spill with no items")))
    player = new_player()
    player.gas_mask_toxic_spill()
    print(bright(red("Testing gas_mask_toxic_spill with Gas Mask")))
    player = new_player(items=['Gas Mask'])
    player.gas_mask_toxic_spill()
    print(bright(red("Testing gas_mask_toxic_spill with Hazmat Suit")))
    player = new_player(items=['Hazmat Suit'])
    player.gas_mask_toxic_spill()

def gentleman_charm_dinner():
    print(bright(red("TESTING gentleman_charm_dinner with no items")))
    player = new_player()
    player.gentleman_charm_dinner()
    print(bright(red("Testing gentleman_charm_dinner with Flask of Pocket Aces")))
    player = new_player(items=['Flask of Pocket Aces'])
    player.gentleman_charm_dinner()
    print(bright(red("Testing gentleman_charm_dinner with Gentleman's Charm")))
    player = new_player(items=["Gentleman's Charm"])
    player.gentleman_charm_dinner()
    print(bright(red("Testing gentleman_charm_dinner with Old Money Identity")))
    player = new_player(items=['Old Money Identity'])
    player.gentleman_charm_dinner()

def ghost_protocol_invisible():
    print(bright(red("TESTING ghost_protocol_invisible with no items")))
    player = new_player()
    player.ghost_protocol_invisible()
    print(bright(red("Testing ghost_protocol_invisible with Ghost Protocol")))
    player = new_player(items=['Ghost Protocol'])
    player.ghost_protocol_invisible()
    print(bright(red("Testing ghost_protocol_invisible with New Identity")))
    player = new_player(items=['New Identity'])
    player.ghost_protocol_invisible()
    print(bright(red("Testing ghost_protocol_invisible with Phantom Rose")))
    player = new_player(items=['Phantom Rose'])
    player.ghost_protocol_invisible()

def guardian_angel_lethal():
    print(bright(red("TESTING guardian_angel_lethal with no items")))
    player = new_player()
    player.guardian_angel_lethal()
    print(bright(red("Testing guardian_angel_lethal with Guardian Angel")))
    player = new_player(items=['Guardian Angel'])
    player.guardian_angel_lethal()
    print(bright(red("Testing guardian_angel_lethal with Last Breath Locket")))
    player = new_player(items=['Last Breath Locket'])
    player.guardian_angel_lethal()

def headlamp_night_walk():
    print(bright(red("TESTING headlamp_night_walk with no items")))
    player = new_player()
    player.headlamp_night_walk()
    print(bright(red("Testing headlamp_night_walk with Flashlight")))
    player = new_player(items=['Flashlight'])
    player.headlamp_night_walk()
    print(bright(red("Testing headlamp_night_walk with Headlamp")))
    player = new_player(items=['Headlamp'])
    player.headlamp_night_walk()

def heirloom_set_recognition():
    print(bright(red("TESTING heirloom_set_recognition with no items")))
    player = new_player()
    player.heirloom_set_recognition()
    print(bright(red("Testing heirloom_set_recognition with Heirloom Set")))
    player = new_player(items=['Heirloom Set'])
    player.heirloom_set_recognition()

def herbal_pouch_remedy():
    print(bright(red("TESTING herbal_pouch_remedy with no items")))
    player = new_player()
    player.herbal_pouch_remedy()
    print(bright(red("Testing herbal_pouch_remedy with Herbal Pouch")))
    player = new_player(items=['Herbal Pouch'])
    player.herbal_pouch_remedy()

def hollow_tree_stash_find():
    print(bright(red("TESTING hollow_tree_stash_find with no items")))
    player = new_player()
    player.hollow_tree_stash_find()
    print(bright(red("Testing hollow_tree_stash_find with Hollow Tree Stash")))
    player = new_player(items=['Hollow Tree Stash'])
    player.hollow_tree_stash_find()

def home_remedy_illness():
    print(bright(red("TESTING home_remedy_illness with no items")))
    player = new_player()
    player.home_remedy_illness()
    print(bright(red("Testing home_remedy_illness with Home Remedy")))
    player = new_player(items=['Home Remedy'])
    player.home_remedy_illness()
    print(bright(red("Testing home_remedy_illness with Smelling Salts")))
    player = new_player(items=['Smelling Salts'])
    player.home_remedy_illness()
    print(bright(red("Testing home_remedy_illness with Wound Salve")))
    player = new_player(items=['Wound Salve'])
    player.home_remedy_illness()

def immortal_vehicle_breakdown():
    print(bright(red("TESTING immortal_vehicle_breakdown with no items")))
    player = new_player()
    player.immortal_vehicle_breakdown()
    print(bright(red("Testing immortal_vehicle_breakdown with Auto Mechanic")))
    player = new_player(items=['Auto Mechanic'])
    player.immortal_vehicle_breakdown()
    print(bright(red("Testing immortal_vehicle_breakdown with Immortal Vehicle")))
    player = new_player(items=['Immortal Vehicle'])
    player.immortal_vehicle_breakdown()
    print(bright(red("Testing immortal_vehicle_breakdown with War Wagon")))
    player = new_player(items=['War Wagon'])
    player.immortal_vehicle_breakdown()

def item_hoarder():
    print(bright(red("TESTING item_hoarder with no items")))
    player = new_player()
    player.item_hoarder()

def junkyard_crown_moment():
    print(bright(red("TESTING junkyard_crown_moment with no items")))
    player = new_player()
    player.junkyard_crown_moment()
    print(bright(red("Testing junkyard_crown_moment with Junkyard Crown")))
    player = new_player(items=['Junkyard Crown'])
    player.junkyard_crown_moment()

def kingpin_look_respect():
    print(bright(red("TESTING kingpin_look_respect with no items")))
    player = new_player()
    player.kingpin_look_respect()
    print(bright(red("Testing kingpin_look_respect with Brass Knuckles")))
    player = new_player(items=['Brass Knuckles'])
    player.kingpin_look_respect()
    print(bright(red("Testing kingpin_look_respect with Kingpin Look")))
    player = new_player(items=['Kingpin Look'])
    player.kingpin_look_respect()

def lockbox_contents():
    print(bright(red("TESTING lockbox_contents with no items")))
    player = new_player()
    player.lockbox_contents()
    print(bright(red("Testing lockbox_contents with Lockbox")))
    player = new_player(items=['Lockbox'])
    player.lockbox_contents()
    print(bright(red("Testing lockbox_contents with Lockpick Set")))
    player = new_player(items=['Lockpick Set'])
    player.lockbox_contents()
    print(bright(red("Testing lockbox_contents with Master Knife")))
    player = new_player(items=['Master Knife'])
    player.lockbox_contents()
    print(bright(red("Testing lockbox_contents with Pocket Knife")))
    player = new_player(items=['Pocket Knife'])
    player.lockbox_contents()
    print(bright(red("Testing lockbox_contents with Utility Blade")))
    player = new_player(items=['Utility Blade'])
    player.lockbox_contents()

def lockpick_opportunity():
    print(bright(red("TESTING lockpick_opportunity with no items")))
    player = new_player()
    player.lockpick_opportunity()
    print(bright(red("Testing lockpick_opportunity with Lockpick Set")))
    player = new_player(items=['Lockpick Set'])
    player.lockpick_opportunity()
    print(bright(red("Testing lockpick_opportunity with Master Knife")))
    player = new_player(items=['Master Knife'])
    player.lockpick_opportunity()
    print(bright(red("Testing lockpick_opportunity with Pocket Knife")))
    player = new_player(items=['Pocket Knife'])
    player.lockpick_opportunity()
    print(bright(red("Testing lockpick_opportunity with Utility Blade")))
    player = new_player(items=['Utility Blade'])
    player.lockpick_opportunity()

def lottery_ticket_check():
    print(bright(red("TESTING lottery_ticket_check with no items")))
    player = new_player()
    player.lottery_ticket_check()
    print(bright(red("Testing lottery_ticket_check with Lottery Ticket")))
    player = new_player(items=['Lottery Ticket'])
    player.lottery_ticket_check()

def love_potion_use():
    print(bright(red("TESTING love_potion_use with no items")))
    player = new_player()
    player.love_potion_use()
    print(bright(red("Testing love_potion_use with Love Potion")))
    player = new_player(items=['Love Potion'])
    player.love_potion_use()

def low_profile_casino_blend():
    print(bright(red("TESTING low_profile_casino_blend with no items")))
    player = new_player()
    player.low_profile_casino_blend()
    print(bright(red("Testing low_profile_casino_blend with Low-Profile Outfit")))
    player = new_player(items=['Low-Profile Outfit'])
    player.low_profile_casino_blend()
    print(bright(red("Testing low_profile_casino_blend with New Identity")))
    player = new_player(items=['New Identity'])
    player.low_profile_casino_blend()

def low_profile_mugging_marcus():
    print(bright(red("TESTING low_profile_mugging_marcus with no items")))
    player = new_player()
    player.low_profile_mugging_marcus()
    print(bright(red("Testing low_profile_mugging_marcus with Low-Profile Outfit")))
    player = new_player(items=['Low-Profile Outfit'])
    player.low_profile_mugging_marcus()
    print(bright(red("Testing low_profile_mugging_marcus with New Identity")))
    player = new_player(items=['New Identity'])
    player.low_profile_mugging_marcus()

def low_profile_police_encounter():
    print(bright(red("TESTING low_profile_police_encounter with no items")))
    player = new_player()
    player.low_profile_police_encounter()
    print(bright(red("Testing low_profile_police_encounter with Low-Profile Outfit")))
    player = new_player(items=['Low-Profile Outfit'])
    player.low_profile_police_encounter()
    print(bright(red("Testing low_profile_police_encounter with New Identity")))
    player = new_player(items=['New Identity'])
    player.low_profile_police_encounter()

def low_profile_shelter_meal():
    print(bright(red("TESTING low_profile_shelter_meal with no items")))
    player = new_player()
    player.low_profile_shelter_meal()
    print(bright(red("Testing low_profile_shelter_meal with Low-Profile Outfit")))
    player = new_player(items=['Low-Profile Outfit'])
    player.low_profile_shelter_meal()
    print(bright(red("Testing low_profile_shelter_meal with New Identity")))
    player = new_player(items=['New Identity'])
    player.low_profile_shelter_meal()

def luck_totem_windfall():
    print(bright(red("TESTING luck_totem_windfall with no items")))
    player = new_player()
    player.luck_totem_windfall()
    print(bright(red("Testing luck_totem_windfall with Fortune's Favor")))
    player = new_player(items=["Fortune's Favor"])
    player.luck_totem_windfall()
    print(bright(red("Testing luck_totem_windfall with Gambler's Aura")))
    player = new_player(items=["Gambler's Aura"])
    player.luck_totem_windfall()
    print(bright(red("Testing luck_totem_windfall with Luck Totem")))
    player = new_player(items=['Luck Totem'])
    player.luck_totem_windfall()

def lucky_charm_streak():
    print(bright(red("TESTING lucky_charm_streak with no items")))
    player = new_player()
    player.lucky_charm_streak()
    print(bright(red("Testing lucky_charm_streak with Lucky Charm Bracelet")))
    player = new_player(items=['Lucky Charm Bracelet'])
    player.lucky_charm_streak()

def lucky_lure_fishing():
    print(bright(red("TESTING lucky_lure_fishing with no items")))
    player = new_player()
    player.lucky_lure_fishing()
    print(bright(red("Testing lucky_lure_fishing with Earl's Lucky Lure")))
    player = new_player(items=["Earl's Lucky Lure"])
    player.lucky_lure_fishing()
    print(bright(red("Testing lucky_lure_fishing with Fish")))
    player = new_player(items=['Fish'])
    player.lucky_lure_fishing()
    print(bright(red("Testing lucky_lure_fishing with Live Fish")))
    player = new_player(items=['Live Fish'])
    player.lucky_lure_fishing()
    print(bright(red("Testing lucky_lure_fishing with Lucky Lure")))
    player = new_player(items=['Lucky Lure'])
    player.lucky_lure_fishing()

def magic_acorn_planting():
    print(bright(red("TESTING magic_acorn_planting with no items")))
    player = new_player()
    player.magic_acorn_planting()
    print(bright(red("Testing magic_acorn_planting with Magic Acorn")))
    player = new_player(items=['Magic Acorn'])
    player.magic_acorn_planting()

def miracle_lube_breakdown():
    print(bright(red("TESTING miracle_lube_breakdown with no items")))
    player = new_player()
    player.miracle_lube_breakdown()
    print(bright(red("Testing miracle_lube_breakdown with Auto Mechanic")))
    player = new_player(items=['Auto Mechanic'])
    player.miracle_lube_breakdown()
    print(bright(red("Testing miracle_lube_breakdown with Miracle Lube")))
    player = new_player(items=['Miracle Lube'])
    player.miracle_lube_breakdown()
    print(bright(red("Testing miracle_lube_breakdown with Mobile Workshop")))
    player = new_player(items=['Mobile Workshop'])
    player.miracle_lube_breakdown()

def mobile_workshop_stranger():
    print(bright(red("TESTING mobile_workshop_stranger with no items")))
    player = new_player()
    player.mobile_workshop_stranger()
    print(bright(red("Testing mobile_workshop_stranger with Auto Mechanic")))
    player = new_player(items=['Auto Mechanic'])
    player.mobile_workshop_stranger()
    print(bright(red("Testing mobile_workshop_stranger with Mobile Workshop")))
    player = new_player(items=['Mobile Workshop'])
    player.mobile_workshop_stranger()

def mysterious_code_decode():
    print(bright(red("TESTING mysterious_code_decode with no items")))
    player = new_player()
    player.mysterious_code_decode()
    print(bright(red("Testing mysterious_code_decode with Mysterious Code")))
    player = new_player(items=['Mysterious Code'])
    player.mysterious_code_decode()
    print(bright(red("Testing mysterious_code_decode with Mysterious Key")))
    player = new_player(items=['Mysterious Key'])
    player.mysterious_code_decode()

def mysterious_envelope_reveal():
    print(bright(red("TESTING mysterious_envelope_reveal with no items")))
    player = new_player()
    player.mysterious_envelope_reveal()
    print(bright(red("Testing mysterious_envelope_reveal with Mysterious Envelope")))
    player = new_player(items=['Mysterious Envelope'])
    player.mysterious_envelope_reveal()

def mysterious_key_lockbox_open():
    print(bright(red("TESTING mysterious_key_lockbox_open with no items")))
    player = new_player()
    player.mysterious_key_lockbox_open()
    print(bright(red("Testing mysterious_key_lockbox_open with Mysterious Key")))
    player = new_player(items=['Mysterious Key'])
    player.mysterious_key_lockbox_open()
    print(bright(red("Testing mysterious_key_lockbox_open with Mysterious Lockbox")))
    player = new_player(items=['Mysterious Lockbox'])
    player.mysterious_key_lockbox_open()

def mystery_potion_effect():
    print(bright(red("TESTING mystery_potion_effect with no items")))
    player = new_player()
    player.mystery_potion_effect()
    print(bright(red("Testing mystery_potion_effect with Mystery Potion")))
    player = new_player(items=['Mystery Potion'])
    player.mystery_potion_effect()

def old_photograph_memory():
    print(bright(red("TESTING old_photograph_memory with no items")))
    player = new_player()
    player.old_photograph_memory()
    print(bright(red("Testing old_photograph_memory with Old Photograph")))
    player = new_player(items=['Old Photograph'])
    player.old_photograph_memory()

def outdoor_shield_farmer():
    print(bright(red("TESTING outdoor_shield_farmer with no items")))
    player = new_player()
    player.outdoor_shield_farmer()
    print(bright(red("Testing outdoor_shield_farmer with All-Weather Armor")))
    player = new_player(items=['All-Weather Armor'])
    player.outdoor_shield_farmer()
    print(bright(red("Testing outdoor_shield_farmer with Outdoor Shield")))
    player = new_player(items=['Outdoor Shield'])
    player.outdoor_shield_farmer()

def persistent_bottle_refill():
    print(bright(red("TESTING persistent_bottle_refill with no items")))
    player = new_player()
    player.persistent_bottle_refill()
    print(bright(red("Testing persistent_bottle_refill with Persistent Bottle")))
    player = new_player(items=['Persistent Bottle'])
    player.persistent_bottle_refill()

def power_grid_dead_battery():
    print(bright(red("TESTING power_grid_dead_battery with no items")))
    player = new_player()
    player.power_grid_dead_battery()
    print(bright(red("Testing power_grid_dead_battery with Power Grid")))
    player = new_player(items=['Power Grid'])
    player.power_grid_dead_battery()
    print(bright(red("Testing power_grid_dead_battery with Roadside Shield")))
    player = new_player(items=['Roadside Shield'])
    player.power_grid_dead_battery()

def power_move_intimidation():
    print(bright(red("TESTING power_move_intimidation with no items")))
    player = new_player()
    player.power_move_intimidation()
    print(bright(red("Testing power_move_intimidation with King of the Road")))
    player = new_player(items=['King of the Road'])
    player.power_move_intimidation()
    print(bright(red("Testing power_move_intimidation with Power Move Kit")))
    player = new_player(items=['Power Move Kit'])
    player.power_move_intimidation()

def pursuit_package_chase():
    print(bright(red("TESTING pursuit_package_chase with no items")))
    player = new_player()
    player.pursuit_package_chase()
    print(bright(red("Testing pursuit_package_chase with Pursuit Package")))
    player = new_player(items=['Pursuit Package'])
    player.pursuit_package_chase()
    print(bright(red("Testing pursuit_package_chase with Rolling Fortress")))
    player = new_player(items=['Rolling Fortress'])
    player.pursuit_package_chase()

def pursuit_package_witness():
    print(bright(red("TESTING pursuit_package_witness with no items")))
    player = new_player()
    player.pursuit_package_witness()
    print(bright(red("Testing pursuit_package_witness with Pursuit Package")))
    player = new_player(items=['Pursuit Package'])
    player.pursuit_package_witness()
    print(bright(red("Testing pursuit_package_witness with Rolling Fortress")))
    player = new_player(items=['Rolling Fortress'])
    player.pursuit_package_witness()

def radio_jammer_checkpoint():
    print(bright(red("TESTING radio_jammer_checkpoint with no items")))
    player = new_player()
    player.radio_jammer_checkpoint()
    print(bright(red("Testing radio_jammer_checkpoint with Forged Documents")))
    player = new_player(items=['Forged Documents'])
    player.radio_jammer_checkpoint()
    print(bright(red("Testing radio_jammer_checkpoint with Radio Jammer")))
    player = new_player(items=['Radio Jammer'])
    player.radio_jammer_checkpoint()

def radio_numbers_broadcast():
    print(bright(red("TESTING radio_numbers_broadcast with no items")))
    player = new_player()
    player.radio_numbers_broadcast()
    print(bright(red("Testing radio_numbers_broadcast with Radio Logbook")))
    player = new_player(items=['Radio Logbook'])
    player.radio_numbers_broadcast()
    print(bright(red("Testing radio_numbers_broadcast with Radio Numbers")))
    player = new_player(items=['Radio Numbers'])
    player.radio_numbers_broadcast()

def rain_collector_bonus():
    print(bright(red("TESTING rain_collector_bonus with no items")))
    player = new_player()
    player.rain_collector_bonus()
    print(bright(red("Testing rain_collector_bonus with Rain Collector")))
    player = new_player(items=['Rain Collector'])
    player.rain_collector_bonus()

def reunion_photo_comfort():
    print(bright(red("TESTING reunion_photo_comfort with no items")))
    player = new_player()
    player.reunion_photo_comfort()
    print(bright(red("Testing reunion_photo_comfort with Reunion Photo")))
    player = new_player(items=['Reunion Photo'])
    player.reunion_photo_comfort()

def ritual_token_ceremony():
    print(bright(red("TESTING ritual_token_ceremony with no items")))
    player = new_player()
    player.ritual_token_ceremony()
    print(bright(red("Testing ritual_token_ceremony with Ritual Token")))
    player = new_player(items=['Ritual Token'])
    player.ritual_token_ceremony()

def road_flare_torch_encounter():
    print(bright(red("TESTING road_flare_torch_encounter with no items")))
    player = new_player()
    player.road_flare_torch_encounter()
    print(bright(red("Testing road_flare_torch_encounter with Eternal Light")))
    player = new_player(items=['Eternal Light'])
    player.road_flare_torch_encounter()
    print(bright(red("Testing road_flare_torch_encounter with Flashlight")))
    player = new_player(items=['Flashlight'])
    player.road_flare_torch_encounter()
    print(bright(red("Testing road_flare_torch_encounter with Lantern")))
    player = new_player(items=['Lantern'])
    player.road_flare_torch_encounter()
    print(bright(red("Testing road_flare_torch_encounter with Road Flare Torch")))
    player = new_player(items=['Road Flare Torch'])
    player.road_flare_torch_encounter()

def road_talisman_protection():
    print(bright(red("TESTING road_talisman_protection with no items")))
    player = new_player()
    player.road_talisman_protection()
    print(bright(red("Testing road_talisman_protection with Road Talisman")))
    player = new_player(items=['Road Talisman'])
    player.road_talisman_protection()

def road_warrior_ambush():
    print(bright(red("TESTING road_warrior_ambush with no items")))
    player = new_player()
    player.road_warrior_ambush()
    print(bright(red("Testing road_warrior_ambush with Assassin's Kit")))
    player = new_player(items=["Assassin's Kit"])
    player.road_warrior_ambush()
    print(bright(red("Testing road_warrior_ambush with Beastslayer Mantle")))
    player = new_player(items=['Beastslayer Mantle'])
    player.road_warrior_ambush()
    print(bright(red("Testing road_warrior_ambush with Road Warrior Armor")))
    player = new_player(items=['Road Warrior Armor'])
    player.road_warrior_ambush()

def scrap_armor_event():
    print(bright(red("TESTING scrap_armor_event with no items")))
    player = new_player()
    player.scrap_armor_event()
    print(bright(red("Testing scrap_armor_event with Artisan's Toolkit")))
    player = new_player(items=["Artisan's Toolkit"])
    player.scrap_armor_event()
    print(bright(red("Testing scrap_armor_event with Scrap Armor")))
    player = new_player(items=['Scrap Armor'])
    player.scrap_armor_event()

def secret_route_shortcut():
    print(bright(red("TESTING secret_route_shortcut with no items")))
    player = new_player()
    player.secret_route_shortcut()
    print(bright(red("Testing secret_route_shortcut with Secret Route Map")))
    player = new_player(items=['Secret Route Map'])
    player.secret_route_shortcut()

def security_bypass_locked_room():
    print(bright(red("TESTING security_bypass_locked_room with no items")))
    player = new_player()
    player.security_bypass_locked_room()
    print(bright(red("Testing security_bypass_locked_room with Lockpick Set")))
    player = new_player(items=['Lockpick Set'])
    player.security_bypass_locked_room()
    print(bright(red("Testing security_bypass_locked_room with Master Key")))
    player = new_player(items=['Master Key'])
    player.security_bypass_locked_room()
    print(bright(red("Testing security_bypass_locked_room with Security Bypass")))
    player = new_player(items=['Security Bypass'])
    player.security_bypass_locked_room()

def shiv_confrontation():
    print(bright(red("TESTING shiv_confrontation with no items")))
    player = new_player()
    player.shiv_confrontation()
    print(bright(red("Testing shiv_confrontation with Pepper Spray")))
    player = new_player(items=['Pepper Spray'])
    player.shiv_confrontation()
    print(bright(red("Testing shiv_confrontation with Shiv")))
    player = new_player(items=['Shiv'])
    player.shiv_confrontation()

def signal_mirror_rescue():
    print(bright(red("TESTING signal_mirror_rescue with no items")))
    player = new_player()
    player.signal_mirror_rescue()
    print(bright(red("Testing signal_mirror_rescue with Broken Compass")))
    player = new_player(items=['Broken Compass'])
    player.signal_mirror_rescue()
    print(bright(red("Testing signal_mirror_rescue with Signal Mirror")))
    player = new_player(items=['Signal Mirror'])
    player.signal_mirror_rescue()
    print(bright(red("Testing signal_mirror_rescue with Smoke Signal Kit")))
    player = new_player(items=['Smoke Signal Kit'])
    player.signal_mirror_rescue()

def silver_horseshoe_luck():
    print(bright(red("TESTING silver_horseshoe_luck with no items")))
    player = new_player()
    player.silver_horseshoe_luck()
    print(bright(red("Testing silver_horseshoe_luck with Lucky Charm Bracelet")))
    player = new_player(items=['Lucky Charm Bracelet'])
    player.silver_horseshoe_luck()
    print(bright(red("Testing silver_horseshoe_luck with Lucky Coin")))
    player = new_player(items=['Lucky Coin'])
    player.silver_horseshoe_luck()
    print(bright(red("Testing silver_horseshoe_luck with Lucky Medallion")))
    player = new_player(items=['Lucky Medallion'])
    player.silver_horseshoe_luck()
    print(bright(red("Testing silver_horseshoe_luck with Lucky Penny")))
    player = new_player(items=['Lucky Penny'])
    player.silver_horseshoe_luck()
    print(bright(red("Testing silver_horseshoe_luck with Silver Horseshoe")))
    player = new_player(items=['Silver Horseshoe'])
    player.silver_horseshoe_luck()

def slingshot_bird_hunt():
    print(bright(red("TESTING slingshot_bird_hunt with no items")))
    player = new_player()
    player.slingshot_bird_hunt()
    print(bright(red("Testing slingshot_bird_hunt with Slingshot")))
    player = new_player(items=['Slingshot'])
    player.slingshot_bird_hunt()

def smoke_flare_pursuit():
    print(bright(red("TESTING smoke_flare_pursuit with no items")))
    player = new_player()
    player.smoke_flare_pursuit()
    print(bright(red("Testing smoke_flare_pursuit with SOS Kit")))
    player = new_player(items=['SOS Kit'])
    player.smoke_flare_pursuit()
    print(bright(red("Testing smoke_flare_pursuit with Smoke Flare")))
    player = new_player(items=['Smoke Flare'])
    player.smoke_flare_pursuit()

def snare_trap_catch():
    print(bright(red("TESTING snare_trap_catch with no items")))
    player = new_player()
    player.snare_trap_catch()
    print(bright(red("Testing snare_trap_catch with Snare Trap")))
    player = new_player(items=['Snare Trap'])
    player.snare_trap_catch()

def splint_injury_event():
    print(bright(red("TESTING splint_injury_event with no items")))
    player = new_player()
    player.splint_injury_event()
    print(bright(red("Testing splint_injury_event with Splint")))
    player = new_player(items=['Splint'])
    player.splint_injury_event()

def spotlight_hidden_path():
    print(bright(red("TESTING spotlight_hidden_path with no items")))
    player = new_player()
    player.spotlight_hidden_path()
    print(bright(red("Testing spotlight_hidden_path with Spotlight")))
    player = new_player(items=['Spotlight'])
    player.spotlight_hidden_path()

def stack_of_flyers_opportunity():
    print(bright(red("TESTING stack_of_flyers_opportunity with no items")))
    player = new_player()
    player.stack_of_flyers_opportunity()
    print(bright(red("Testing stack_of_flyers_opportunity with Stack of Flyers")))
    player = new_player(items=['Stack of Flyers'])
    player.stack_of_flyers_opportunity()

def stink_bomb_escape():
    print(bright(red("TESTING stink_bomb_escape with no items")))
    player = new_player()
    player.stink_bomb_escape()
    print(bright(red("Testing stink_bomb_escape with Stink Bomb")))
    player = new_player(items=['Stink Bomb'])
    player.stink_bomb_escape()
    print(bright(red("Testing stink_bomb_escape with Tear Gas")))
    player = new_player(items=['Tear Gas'])
    player.stink_bomb_escape()

def stolen_watch_recognition():
    print(bright(red("TESTING stolen_watch_recognition with no items")))
    player = new_player()
    player.stolen_watch_recognition()
    print(bright(red("Testing stolen_watch_recognition with Stolen Watch")))
    player = new_player(items=['Stolen Watch'])
    player.stolen_watch_recognition()

def storm_suit_flood():
    print(bright(red("TESTING storm_suit_flood with no items")))
    player = new_player()
    player.storm_suit_flood()
    print(bright(red("Testing storm_suit_flood with All-Weather Armor")))
    player = new_player(items=['All-Weather Armor'])
    player.storm_suit_flood()
    print(bright(red("Testing storm_suit_flood with Storm Suit")))
    player = new_player(items=['Storm Suit'])
    player.storm_suit_flood()

def storm_suit_hurricane():
    print(bright(red("TESTING storm_suit_hurricane with no items")))
    player = new_player()
    player.storm_suit_hurricane()
    print(bright(red("Testing storm_suit_hurricane with All-Weather Armor")))
    player = new_player(items=['All-Weather Armor'])
    player.storm_suit_hurricane()
    print(bright(red("Testing storm_suit_hurricane with Storm Suit")))
    player = new_player(items=['Storm Suit'])
    player.storm_suit_hurricane()

def storm_suit_night_bear():
    print(bright(red("TESTING storm_suit_night_bear with no items")))
    player = new_player()
    player.storm_suit_night_bear()
    print(bright(red("Testing storm_suit_night_bear with All-Weather Armor")))
    player = new_player(items=['All-Weather Armor'])
    player.storm_suit_night_bear()
    print(bright(red("Testing storm_suit_night_bear with Forged Documents")))
    player = new_player(items=['Forged Documents'])
    player.storm_suit_night_bear()
    print(bright(red("Testing storm_suit_night_bear with Storm Suit")))
    player = new_player(items=['Storm Suit'])
    player.storm_suit_night_bear()

def street_cat_ally_benefit():
    print(bright(red("TESTING street_cat_ally_benefit with no items")))
    player = new_player()
    player.street_cat_ally_benefit()
    print(bright(red("Testing street_cat_ally_benefit with Street Cat Ally")))
    player = new_player(items=['Street Cat Ally'])
    player.street_cat_ally_benefit()

def suspicious_package_open():
    print(bright(red("TESTING suspicious_package_open with no items")))
    player = new_player()
    player.suspicious_package_open()
    print(bright(red("Testing suspicious_package_open with Suspicious Package")))
    player = new_player(items=['Suspicious Package'])
    player.suspicious_package_open()

def swamp_gold_attention():
    print(bright(red("TESTING swamp_gold_attention with no items")))
    player = new_player()
    player.swamp_gold_attention()
    print(bright(red("Testing swamp_gold_attention with Swamp Gold")))
    player = new_player(items=['Swamp Gold'])
    player.swamp_gold_attention()

def third_eye_foresight():
    print(bright(red("TESTING third_eye_foresight with no items")))
    player = new_player()
    player.third_eye_foresight()
    print(bright(red("Testing third_eye_foresight with Fortune Cards")))
    player = new_player(items=['Fortune Cards'])
    player.third_eye_foresight()
    print(bright(red("Testing third_eye_foresight with Seer's Chronicle")))
    player = new_player(items=["Seer's Chronicle"])
    player.third_eye_foresight()
    print(bright(red("Testing third_eye_foresight with Third Eye")))
    player = new_player(items=['Third Eye'])
    player.third_eye_foresight()

def tinfoil_hat_event():
    print(bright(red("TESTING tinfoil_hat_event with no items")))
    player = new_player()
    player.tinfoil_hat_event()
    print(bright(red("Testing tinfoil_hat_event with Tinfoil Hat")))
    player = new_player(items=['Tinfoil Hat'])
    player.tinfoil_hat_event()

def tire_ready_flat():
    print(bright(red("TESTING tire_ready_flat with no items")))
    player = new_player()
    player.tire_ready_flat()
    print(bright(red("Testing tire_ready_flat with Mobile Workshop")))
    player = new_player(items=['Mobile Workshop'])
    player.tire_ready_flat()
    print(bright(red("Testing tire_ready_flat with Roadside Shield")))
    player = new_player(items=['Roadside Shield'])
    player.tire_ready_flat()
    print(bright(red("Testing tire_ready_flat with Tire Ready Kit")))
    player = new_player(items=['Tire Ready Kit'])
    player.tire_ready_flat()

def trail_mix_bomb_distraction():
    print(bright(red("TESTING trail_mix_bomb_distraction with no items")))
    player = new_player()
    player.trail_mix_bomb_distraction()
    print(bright(red("Testing trail_mix_bomb_distraction with Trail Mix Bomb")))
    player = new_player(items=['Trail Mix Bomb'])
    player.trail_mix_bomb_distraction()

def trap_night_thief():
    print(bright(red("TESTING trap_night_thief with no items")))
    player = new_player()
    player.trap_night_thief()
    print(bright(red("Testing trap_night_thief with Car Alarm Rigging")))
    player = new_player(items=['Car Alarm Rigging'])
    player.trap_night_thief()
    print(bright(red("Testing trap_night_thief with Flashlight")))
    player = new_player(items=['Flashlight'])
    player.trap_night_thief()
    print(bright(red("Testing trap_night_thief with Improvised Trap")))
    player = new_player(items=['Improvised Trap'])
    player.trap_night_thief()

def treasure_map_follow():
    print(bright(red("TESTING treasure_map_follow with no items")))
    player = new_player()
    player.treasure_map_follow()
    print(bright(red("Testing treasure_map_follow with Fairy's Secret Map")))
    player = new_player(items=["Fairy's Secret Map"])
    player.treasure_map_follow()
    print(bright(red("Testing treasure_map_follow with Golden Compass")))
    player = new_player(items=['Golden Compass'])
    player.treasure_map_follow()
    print(bright(red("Testing treasure_map_follow with Joe's Treasure Map")))
    player = new_player(items=["Joe's Treasure Map"])
    player.treasure_map_follow()
    print(bright(red("Testing treasure_map_follow with Rusty Compass")))
    player = new_player(items=['Rusty Compass'])
    player.treasure_map_follow()
    print(bright(red("Testing treasure_map_follow with Treasure Coordinates")))
    player = new_player(items=['Treasure Coordinates'])
    player.treasure_map_follow()
    print(bright(red("Testing treasure_map_follow with Treasure Map")))
    player = new_player(items=['Treasure Map'])
    player.treasure_map_follow()
    print(bright(red("Testing treasure_map_follow with Vision Map")))
    player = new_player(items=['Vision Map'])
    player.treasure_map_follow()

def underwater_camera_photos():
    print(bright(red("TESTING underwater_camera_photos with no items")))
    player = new_player()
    player.underwater_camera_photos()
    print(bright(red("Testing underwater_camera_photos with Underwater Camera")))
    player = new_player(items=['Underwater Camera'])
    player.underwater_camera_photos()

def vermin_bomb_car():
    print(bright(red("TESTING vermin_bomb_car with no items")))
    player = new_player()
    player.vermin_bomb_car()
    print(bright(red("Testing vermin_bomb_car with Vermin Bomb")))
    player = new_player(items=['Vermin Bomb'])
    player.vermin_bomb_car()

def vision_map_navigate():
    print(bright(red("TESTING vision_map_navigate with no items")))
    player = new_player()
    player.vision_map_navigate()
    print(bright(red("Testing vision_map_navigate with Vision Map")))
    player = new_player(items=['Vision Map'])
    player.vision_map_navigate()

def voice_soother_persuasion():
    print(bright(red("TESTING voice_soother_persuasion with no items")))
    player = new_player()
    player.voice_soother_persuasion()
    print(bright(red("Testing voice_soother_persuasion with Voice Soother")))
    player = new_player(items=['Voice Soother'])
    player.voice_soother_persuasion()

def walking_stick_hike():
    print(bright(red("TESTING walking_stick_hike with no items")))
    player = new_player()
    player.walking_stick_hike()
    print(bright(red("Testing walking_stick_hike with Carved Walking Stick")))
    player = new_player(items=['Carved Walking Stick'])
    player.walking_stick_hike()

def water_purifier_use():
    print(bright(red("TESTING water_purifier_use with no items")))
    player = new_player()
    player.water_purifier_use()
    print(bright(red("Testing water_purifier_use with Water Purifier")))
    player = new_player(items=['Water Purifier'])
    player.water_purifier_use()

def wild_binding_portrait_shopkeeper():
    print(bright(red("TESTING wild_binding_portrait_shopkeeper with no items")))
    player = new_player()
    player.wild_binding_portrait_shopkeeper()
    print(bright(red("Testing wild_binding_portrait_shopkeeper with Binding Portrait")))
    player = new_player(items=['Binding Portrait'])
    player.wild_binding_portrait_shopkeeper()

def wild_blackmail_letter_companion():
    print(bright(red("TESTING wild_blackmail_letter_companion with no items")))
    player = new_player()
    player.wild_blackmail_letter_companion()
    print(bright(red("Testing wild_blackmail_letter_companion with Blackmail Letter")))
    player = new_player(items=['Blackmail Letter'])
    player.wild_blackmail_letter_companion()

def wild_devil_deck_children():
    print(bright(red("TESTING wild_devil_deck_children with no items")))
    player = new_player()
    player.wild_devil_deck_children()
    print(bright(red("Testing wild_devil_deck_children with Dark Pact Reliquary")))
    player = new_player(items=['Dark Pact Reliquary'])
    player.wild_devil_deck_children()
    print(bright(red("Testing wild_devil_deck_children with Devil's Deck")))
    player = new_player(items=["Devil's Deck"])
    player.wild_devil_deck_children()

def wild_distress_beacon_casino():
    print(bright(red("TESTING wild_distress_beacon_casino with no items")))
    player = new_player()
    player.wild_distress_beacon_casino()
    print(bright(red("Testing wild_distress_beacon_casino with Distress Beacon")))
    player = new_player(items=['Distress Beacon'])
    player.wild_distress_beacon_casino()

def wild_eldritch_candle_gambling():
    print(bright(red("TESTING wild_eldritch_candle_gambling with no items")))
    player = new_player()
    player.wild_eldritch_candle_gambling()
    print(bright(red("Testing wild_eldritch_candle_gambling with Dark Pact Reliquary")))
    player = new_player(items=['Dark Pact Reliquary'])
    player.wild_eldritch_candle_gambling()
    print(bright(red("Testing wild_eldritch_candle_gambling with Eldritch Candle")))
    player = new_player(items=['Eldritch Candle'])
    player.wild_eldritch_candle_gambling()

def wild_emp_casino():
    print(bright(red("TESTING wild_emp_casino with no items")))
    player = new_player()
    player.wild_emp_casino()
    print(bright(red("Testing wild_emp_casino with EMP Device")))
    player = new_player(items=['EMP Device'])
    player.wild_emp_casino()

def wild_evidence_kit_wedding():
    print(bright(red("TESTING wild_evidence_kit_wedding with no items")))
    player = new_player()
    player.wild_evidence_kit_wedding()
    print(bright(red("Testing wild_evidence_kit_wedding with Evidence Kit")))
    player = new_player(items=['Evidence Kit'])
    player.wild_evidence_kit_wedding()
    print(bright(red("Testing wild_evidence_kit_wedding with Intelligence Dossier")))
    player = new_player(items=['Intelligence Dossier'])
    player.wild_evidence_kit_wedding()

def wild_fortune_cards_car():
    print(bright(red("TESTING wild_fortune_cards_car with no items")))
    player = new_player()
    player.wild_fortune_cards_car()
    print(bright(red("Testing wild_fortune_cards_car with Fate Reader")))
    player = new_player(items=['Fate Reader'])
    player.wild_fortune_cards_car()
    print(bright(red("Testing wild_fortune_cards_car with Fortune Cards")))
    player = new_player(items=['Fortune Cards'])
    player.wild_fortune_cards_car()

def wild_gas_mask_funeral():
    print(bright(red("TESTING wild_gas_mask_funeral with no items")))
    player = new_player()
    player.wild_gas_mask_funeral()
    print(bright(red("Testing wild_gas_mask_funeral with Gas Mask")))
    player = new_player(items=['Gas Mask'])
    player.wild_gas_mask_funeral()
    print(bright(red("Testing wild_gas_mask_funeral with Hazmat Suit")))
    player = new_player(items=['Hazmat Suit'])
    player.wild_gas_mask_funeral()

def wild_headlamp_poker():
    print(bright(red("TESTING wild_headlamp_poker with no items")))
    player = new_player()
    player.wild_headlamp_poker()
    print(bright(red("Testing wild_headlamp_poker with Headlamp")))
    player = new_player(items=['Headlamp'])
    player.wild_headlamp_poker()

def wild_radio_jammer_police():
    print(bright(red("TESTING wild_radio_jammer_police with no items")))
    player = new_player()
    player.wild_radio_jammer_police()
    print(bright(red("Testing wild_radio_jammer_police with Radio Jammer")))
    player = new_player(items=['Radio Jammer'])
    player.wild_radio_jammer_police()
    print(bright(red("Testing wild_radio_jammer_police with Surveillance Suite")))
    player = new_player(items=['Surveillance Suite'])
    player.wild_radio_jammer_police()

def wild_stink_bomb_casino_vault():
    print(bright(red("TESTING wild_stink_bomb_casino_vault with no items")))
    player = new_player()
    player.wild_stink_bomb_casino_vault()
    print(bright(red("Testing wild_stink_bomb_casino_vault with Stink Bomb")))
    player = new_player(items=['Stink Bomb'])
    player.wild_stink_bomb_casino_vault()

def witch_ward_dark_protection():
    print(bright(red("TESTING witch_ward_dark_protection with no items")))
    player = new_player()
    player.witch_ward_dark_protection()
    print(bright(red("Testing witch_ward_dark_protection with Witch's Ward")))
    player = new_player(items=["Witch's Ward"])
    player.witch_ward_dark_protection()

def worry_stone_moment():
    print(bright(red("TESTING worry_stone_moment with no items")))
    player = new_player()
    player.worry_stone_moment()
    print(bright(red("Testing worry_stone_moment with Dream Catcher")))
    player = new_player(items=['Dream Catcher'])
    player.worry_stone_moment()
    print(bright(red("Testing worry_stone_moment with Lucky Charm Bracelet")))
    player = new_player(items=['Lucky Charm Bracelet'])
    player.worry_stone_moment()
    print(bright(red("Testing worry_stone_moment with Worry Stone")))
    player = new_player(items=['Worry Stone'])
    player.worry_stone_moment()


"""story.events_day_numbers.py"""
def completely_broke_wisdom():
    print(bright(red("TESTING completely_broke_wisdom with no items")))
    player = new_player()
    player.completely_broke_wisdom()
    print(bright(red("Testing completely_broke_wisdom with Lottery Ticket")))
    player = new_player(items=['Lottery Ticket'])
    player.completely_broke_wisdom()

def day_palindrome():
    print(bright(red("TESTING day_palindrome with no items")))
    player = new_player()
    player.day_palindrome()

def exactly_100():
    print(bright(red("TESTING exactly_100 with no items")))
    player = new_player()
    player.exactly_100()
    print(bright(red("Testing exactly_100 with Grandfather Clock")))
    player = new_player(items=['Grandfather Clock'])
    player.exactly_100()
    print(bright(red("Testing exactly_100 with Pocket Watch")))
    player = new_player(items=['Pocket Watch'])
    player.exactly_100()

def exactly_1234():
    print(bright(red("TESTING exactly_1234 with no items")))
    player = new_player()
    player.exactly_1234()

def exactly_13():
    print(bright(red("TESTING exactly_13 with no items")))
    player = new_player()
    player.exactly_13()
    print(bright(red("Testing exactly_13 with Gambler's Grimoire")))
    player = new_player(items=["Gambler's Grimoire"])
    player.exactly_13()
    print(bright(red("Testing exactly_13 with Mind Shield")))
    player = new_player(items=['Mind Shield'])
    player.exactly_13()
    print(bright(red("Testing exactly_13 with Oracle's Tome")))
    player = new_player(items=["Oracle's Tome"])
    player.exactly_13()
    print(bright(red("Testing exactly_13 with Third Eye")))
    player = new_player(items=['Third Eye'])
    player.exactly_13()

def exactly_420():
    print(bright(red("TESTING exactly_420 with no items")))
    player = new_player()
    player.exactly_420()
    print(bright(red("Testing exactly_420 with Fancy Cigars")))
    player = new_player(items=['Fancy Cigars'])
    player.exactly_420()
    print(bright(red("Testing exactly_420 with Silver Flask")))
    player = new_player(items=['Silver Flask'])
    player.exactly_420()

def exactly_69420():
    print(bright(red("TESTING exactly_69420 with no items")))
    player = new_player()
    player.exactly_69420()

def exactly_7777():
    print(bright(red("TESTING exactly_7777 with no items")))
    player = new_player()
    player.exactly_7777()
    print(bright(red("Testing exactly_7777 with Fortune's Favor")))
    player = new_player(items=["Fortune's Favor"])
    player.exactly_7777()
    print(bright(red("Testing exactly_7777 with Gambler's Aura")))
    player = new_player(items=["Gambler's Aura"])
    player.exactly_7777()
    print(bright(red("Testing exactly_7777 with Lucky Charm Bracelet")))
    player = new_player(items=['Lucky Charm Bracelet'])
    player.exactly_7777()
    print(bright(red("Testing exactly_7777 with Lucky Coin")))
    player = new_player(items=['Lucky Coin'])
    player.exactly_7777()
    print(bright(red("Testing exactly_7777 with Lucky Medallion")))
    player = new_player(items=['Lucky Medallion'])
    player.exactly_7777()
    print(bright(red("Testing exactly_7777 with Lucky Penny")))
    player = new_player(items=['Lucky Penny'])
    player.exactly_7777()
    print(bright(red("Testing exactly_7777 with Moonlit Fortune")))
    player = new_player(items=['Moonlit Fortune'])
    player.exactly_7777()

def first_sunrise():
    print(bright(red("TESTING first_sunrise with no items")))
    player = new_player()
    player.first_sunrise()

def full_moon_madness():
    print(bright(red("TESTING full_moon_madness with no items")))
    player = new_player()
    player.full_moon_madness()
    print(bright(red("Testing full_moon_madness with Dream Catcher")))
    player = new_player(items=['Dream Catcher'])
    player.full_moon_madness()
    print(bright(red("Testing full_moon_madness with Necronomicon")))
    player = new_player(items=['Necronomicon'])
    player.full_moon_madness()

def haunted_by_losses():
    print(bright(red("TESTING haunted_by_losses with no items")))
    player = new_player()
    player.haunted_by_losses()

def insomniac_revelation():
    print(bright(red("TESTING insomniac_revelation with no items")))
    player = new_player()
    player.insomniac_revelation()
    print(bright(red("Testing insomniac_revelation with Gambler's Grimoire")))
    player = new_player(items=["Gambler's Grimoire"])
    player.insomniac_revelation()
    print(bright(red("Testing insomniac_revelation with Oracle's Tome")))
    player = new_player(items=["Oracle's Tome"])
    player.insomniac_revelation()

def perfect_health_moment():
    print(bright(red("TESTING perfect_health_moment with no items")))
    player = new_player()
    player.perfect_health_moment()
    print(bright(red("Testing perfect_health_moment with First Aid Kit")))
    player = new_player(items=['First Aid Kit'])
    player.perfect_health_moment()
    print(bright(red("Testing perfect_health_moment with Flask of No Bust")))
    player = new_player(items=['Flask of No Bust'])
    player.perfect_health_moment()

def prime_day():
    print(bright(red("TESTING prime_day with no items")))
    player = new_player()
    player.prime_day()

def rain_on_the_roof():
    print(bright(red("TESTING rain_on_the_roof with no items")))
    player = new_player()
    player.rain_on_the_roof()

def rock_bottom():
    print(bright(red("TESTING rock_bottom with no items")))
    player = new_player()
    player.rock_bottom()
    print(bright(red("Testing rock_bottom with Lottery Ticket")))
    player = new_player(items=['Lottery Ticket'])
    player.rock_bottom()

def same_as_health():
    print(bright(red("TESTING same_as_health with no items")))
    player = new_player()
    player.same_as_health()

def the_crow_council():
    print(bright(red("TESTING the_crow_council with no items")))
    player = new_player()
    player.the_crow_council()

def the_veteran_gambler():
    print(bright(red("TESTING the_veteran_gambler with no items")))
    player = new_player()
    player.the_veteran_gambler()
    print(bright(red("Testing the_veteran_gambler with Flask of Bonus Fortune")))
    player = new_player(items=['Flask of Bonus Fortune'])
    player.the_veteran_gambler()
    print(bright(red("Testing the_veteran_gambler with Flask of Imminent Blackjack")))
    player = new_player(items=['Flask of Imminent Blackjack'])
    player.the_veteran_gambler()


"""story.events_day_people.py"""
def autograph_request():
    print(bright(red("TESTING autograph_request with no items")))
    player = new_player()
    player.autograph_request()

def birthday_forgotten():
    print(bright(red("TESTING birthday_forgotten with no items")))
    player = new_player()
    player.birthday_forgotten()

def book_club_invite():
    print(bright(red("TESTING book_club_invite with no items")))
    player = new_player()
    player.book_club_invite()

def broken_atm():
    print(bright(red("TESTING broken_atm with no items")))
    player = new_player()
    player.broken_atm()

def car_alarm_symphony():
    print(bright(red("TESTING car_alarm_symphony with no items")))
    player = new_player()
    player.car_alarm_symphony()
    print(bright(red("Testing car_alarm_symphony with EMP Device")))
    player = new_player(items=['EMP Device'])
    player.car_alarm_symphony()

def car_compliment():
    print(bright(red("TESTING car_compliment with no items")))
    player = new_player()
    player.car_compliment()

def car_wash_encounter():
    print(bright(red("TESTING car_wash_encounter with no items")))
    player = new_player()
    player.car_wash_encounter()

def casino_regular():
    print(bright(red("TESTING casino_regular with no items")))
    player = new_player()
    player.casino_regular()

def caught_fishing():
    print(bright(red("TESTING caught_fishing with no items")))
    player = new_player()
    player.caught_fishing()
    print(bright(red("Testing caught_fishing with Animal Whistle")))
    player = new_player(items=['Animal Whistle'])
    player.caught_fishing()
    print(bright(red("Testing caught_fishing with Fishing Line")))
    player = new_player(items=['Fishing Line'])
    player.caught_fishing()

def cigar_circle():
    print(bright(red("TESTING cigar_circle with no items")))
    player = new_player()
    player.cigar_circle()
    print(bright(red("Testing cigar_circle with Fancy Cigars")))
    player = new_player(items=['Fancy Cigars'])
    player.cigar_circle()

def classy_encounter():
    print(bright(red("TESTING classy_encounter with no items")))
    player = new_player()
    player.classy_encounter()
    print(bright(red("Testing classy_encounter with Antique Pocket Watch")))
    player = new_player(items=['Antique Pocket Watch'])
    player.classy_encounter()
    print(bright(red("Testing classy_encounter with Aristocrat's Touch")))
    player = new_player(items=["Aristocrat's Touch"])
    player.classy_encounter()
    print(bright(red("Testing classy_encounter with Fancy Cigars")))
    player = new_player(items=['Fancy Cigars'])
    player.classy_encounter()
    print(bright(red("Testing classy_encounter with Gentleman's Charm")))
    player = new_player(items=["Gentleman's Charm"])
    player.classy_encounter()
    print(bright(red("Testing classy_encounter with Gold Chain")))
    player = new_player(items=['Gold Chain'])
    player.classy_encounter()
    print(bright(red("Testing classy_encounter with Leather Gloves")))
    player = new_player(items=['Leather Gloves'])
    player.classy_encounter()
    print(bright(red("Testing classy_encounter with Silk Handkerchief")))
    player = new_player(items=['Silk Handkerchief'])
    player.classy_encounter()
    print(bright(red("Testing classy_encounter with Velvet Gloves")))
    player = new_player(items=['Velvet Gloves'])
    player.classy_encounter()
    print(bright(red("Testing classy_encounter with Vintage Wine")))
    player = new_player(items=['Vintage Wine'])
    player.classy_encounter()
    print(bright(red("Testing classy_encounter with Worn Gloves")))
    player = new_player(items=['Worn Gloves'])
    player.classy_encounter()

def cloud_watching():
    print(bright(red("TESTING cloud_watching with no items")))
    player = new_player()
    player.cloud_watching()

def coffee_shop_philosopher():
    print(bright(red("TESTING coffee_shop_philosopher with no items")))
    player = new_player()
    player.coffee_shop_philosopher()

def coin_flip_stranger():
    print(bright(red("TESTING coin_flip_stranger with no items")))
    player = new_player()
    player.coin_flip_stranger()
    print(bright(red("Testing coin_flip_stranger with Lucky Coin")))
    player = new_player(items=['Lucky Coin'])
    player.coin_flip_stranger()
    print(bright(red("Testing coin_flip_stranger with Lucky Medallion")))
    player = new_player(items=['Lucky Medallion'])
    player.coin_flip_stranger()

def compliment_stranger():
    print(bright(red("TESTING compliment_stranger with no items")))
    player = new_player()
    player.compliment_stranger()

def conspiracy_theorist():
    print(bright(red("TESTING conspiracy_theorist with no items")))
    player = new_player()
    player.conspiracy_theorist()
    print(bright(red("Testing conspiracy_theorist with Sneaky Peeky Goggles")))
    player = new_player(items=['Sneaky Peeky Goggles'])
    player.conspiracy_theorist()
    print(bright(red("Testing conspiracy_theorist with Sneaky Peeky Shades")))
    player = new_player(items=['Sneaky Peeky Shades'])
    player.conspiracy_theorist()

def dog_walker_collision():
    print(bright(red("TESTING dog_walker_collision with no items")))
    player = new_player()
    player.dog_walker_collision()

def dropped_ice_cream():
    print(bright(red("TESTING dropped_ice_cream with no items")))
    player = new_player()
    player.dropped_ice_cream()

def fancy_coffee():
    print(bright(red("TESTING fancy_coffee with no items")))
    player = new_player()
    player.fancy_coffee()

def fancy_restaurant_mistake():
    print(bright(red("TESTING fancy_restaurant_mistake with no items")))
    player = new_player()
    player.fancy_restaurant_mistake()
    print(bright(red("Testing fancy_restaurant_mistake with Expensive Cologne")))
    player = new_player(items=['Expensive Cologne'])
    player.fancy_restaurant_mistake()

def filthy_frank_radio_giveaway():
    print(bright(red("TESTING filthy_frank_radio_giveaway with no items")))
    player = new_player()
    player.filthy_frank_radio_giveaway()

def flea_market_route_map():
    print(bright(red("TESTING flea_market_route_map with no items")))
    player = new_player()
    player.flea_market_route_map()
    print(bright(red("Testing flea_market_route_map with Car")))
    player = new_player(items=['Car'])
    player.flea_market_route_map()
    print(bright(red("Testing flea_market_route_map with Map")))
    player = new_player(items=['Map'])
    player.flea_market_route_map()
    print(bright(red("Testing flea_market_route_map with Worn Map")))
    player = new_player(items=['Worn Map'])
    player.flea_market_route_map()

def food_truck_festival():
    print(bright(red("TESTING food_truck_festival with no items")))
    player = new_player()
    player.food_truck_festival()

def forgotten_birthday():
    print(bright(red("TESTING forgotten_birthday with no items")))
    player = new_player()
    player.forgotten_birthday()

def fortune_cookie():
    print(bright(red("TESTING fortune_cookie with no items")))
    player = new_player()
    player.fortune_cookie()

def found_phone():
    print(bright(red("TESTING found_phone with no items")))
    player = new_player()
    player.found_phone()

def free_sample_spree():
    print(bright(red("TESTING free_sample_spree with no items")))
    player = new_player()
    player.free_sample_spree()

def freight_truck():
    print(bright(red("TESTING freight_truck with no items")))
    player = new_player()
    player.freight_truck()
    print(bright(red("Testing freight_truck with Binocular Scope")))
    player = new_player(items=['Binocular Scope'])
    player.freight_truck()
    print(bright(red("Testing freight_truck with Enchanting Silver Bar")))
    player = new_player(items=['Enchanting Silver Bar'])
    player.freight_truck()

def friendly_drunk():
    print(bright(red("TESTING friendly_drunk with no items")))
    player = new_player()
    player.friendly_drunk()

def further_interrogation():
    print(bright(red("TESTING further_interrogation with no items")))
    player = new_player()
    player.further_interrogation()

def homeless_network():
    print(bright(red("TESTING homeless_network with no items")))
    player = new_player()
    player.homeless_network()
    print(bright(red("Testing homeless_network with Cool Down Kit")))
    player = new_player(items=['Cool Down Kit'])
    player.homeless_network()
    print(bright(red("Testing homeless_network with Deck of Cards")))
    player = new_player(items=['Deck of Cards'])
    player.homeless_network()
    print(bright(red("Testing homeless_network with Outdoor Shield")))
    player = new_player(items=['Outdoor Shield'])
    player.homeless_network()

def ice_cream_truck():
    print(bright(red("TESTING ice_cream_truck with no items")))
    player = new_player()
    player.ice_cream_truck()

def interrogation():
    print(bright(red("TESTING interrogation with no items")))
    player = new_player()
    player.interrogation()
    print(bright(red("Testing interrogation with Marvin's Monocle")))
    player = new_player(items=["Marvin's Monocle"])
    player.interrogation()

def kid_on_bike():
    print(bright(red("TESTING kid_on_bike with no items")))
    player = new_player()
    player.kid_on_bike()

def laundromat_bulletin_map():
    print(bright(red("TESTING laundromat_bulletin_map with no items")))
    player = new_player()
    player.laundromat_bulletin_map()
    print(bright(red("Testing laundromat_bulletin_map with Car")))
    player = new_player(items=['Car'])
    player.laundromat_bulletin_map()
    print(bright(red("Testing laundromat_bulletin_map with Map")))
    player = new_player(items=['Map'])
    player.laundromat_bulletin_map()
    print(bright(red("Testing laundromat_bulletin_map with Worn Map")))
    player = new_player(items=['Worn Map'])
    player.laundromat_bulletin_map()

def lone_cowboy():
    print(bright(red("TESTING lone_cowboy with no items")))
    player = new_player()
    player.lone_cowboy()
    print(bright(red("Testing lone_cowboy with Animal Whistle")))
    player = new_player(items=['Animal Whistle'])
    player.lone_cowboy()

def lost_tourist():
    print(bright(red("TESTING lost_tourist with no items")))
    player = new_player()
    player.lost_tourist()
    print(bright(red("Testing lost_tourist with Golden Compass")))
    player = new_player(items=['Golden Compass'])
    player.lost_tourist()
    print(bright(red("Testing lost_tourist with Rusty Compass")))
    player = new_player(items=['Rusty Compass'])
    player.lost_tourist()

def lottery_scratch():
    print(bright(red("TESTING lottery_scratch with no items")))
    player = new_player()
    player.lottery_scratch()

def mayas_luck():
    print(bright(red("TESTING mayas_luck with no items")))
    player = new_player()
    player.mayas_luck()
    print(bright(red("Testing mayas_luck with Maya's Pick")))
    player = new_player(items=["Maya's Pick"])
    player.mayas_luck()

def midnight_visitor():
    print(bright(red("TESTING midnight_visitor with no items")))
    player = new_player()
    player.midnight_visitor()
    print(bright(red("Testing midnight_visitor with Lucky Charm Bracelet")))
    player = new_player(items=['Lucky Charm Bracelet'])
    player.midnight_visitor()
    print(bright(red("Testing midnight_visitor with Lucky Coin")))
    player = new_player(items=['Lucky Coin'])
    player.midnight_visitor()
    print(bright(red("Testing midnight_visitor with Lucky Medallion")))
    player = new_player(items=['Lucky Medallion'])
    player.midnight_visitor()

def motivational_graffiti():
    print(bright(red("TESTING motivational_graffiti with no items")))
    player = new_player()
    player.motivational_graffiti()

def mysterious_package():
    print(bright(red("TESTING mysterious_package with no items")))
    player = new_player()
    player.mysterious_package()

def old_man_jenkins():
    print(bright(red("TESTING old_man_jenkins with no items")))
    player = new_player()
    player.old_man_jenkins()
    print(bright(red("Testing old_man_jenkins with Grandfather Clock")))
    player = new_player(items=['Grandfather Clock'])
    player.old_man_jenkins()
    print(bright(red("Testing old_man_jenkins with Pocket Watch")))
    player = new_player(items=['Pocket Watch'])
    player.old_man_jenkins()

def oswald_concierge_card():
    print(bright(red("TESTING oswald_concierge_card with no items")))
    player = new_player()
    player.oswald_concierge_card()

def parking_lot_poker():
    print(bright(red("TESTING parking_lot_poker with no items")))
    player = new_player()
    player.parking_lot_poker()

def parking_ticket():
    print(bright(red("TESTING parking_ticket with no items")))
    player = new_player()
    player.parking_ticket()
    print(bright(red("Testing parking_ticket with Dirty Old Hat")))
    player = new_player(items=['Dirty Old Hat'])
    player.parking_ticket()
    print(bright(red("Testing parking_ticket with Unwashed Hair")))
    player = new_player(items=['Unwashed Hair'])
    player.parking_ticket()

def phone_scam_call():
    print(bright(red("TESTING phone_scam_call with no items")))
    player = new_player()
    player.phone_scam_call()

def photo_opportunity():
    print(bright(red("TESTING photo_opportunity with no items")))
    player = new_player()
    player.photo_opportunity()
    print(bright(red("Testing photo_opportunity with Disposable Camera")))
    player = new_player(items=['Disposable Camera'])
    player.photo_opportunity()

def roadkill_philosophy():
    print(bright(red("TESTING roadkill_philosophy with no items")))
    player = new_player()
    player.roadkill_philosophy()

def roadside_bone_chimes():
    print(bright(red("TESTING roadside_bone_chimes with no items")))
    player = new_player()
    player.roadside_bone_chimes()
    print(bright(red("Testing roadside_bone_chimes with Car")))
    player = new_player(items=['Car'])
    player.roadside_bone_chimes()

def robbery_attempt():
    print(bright(red("TESTING robbery_attempt with no items")))
    player = new_player()
    player.robbery_attempt()
    print(bright(red("Testing robbery_attempt with Assassin's Kit")))
    player = new_player(items=["Assassin's Kit"])
    player.robbery_attempt()
    print(bright(red("Testing robbery_attempt with Brass Knuckles")))
    player = new_player(items=['Brass Knuckles'])
    player.robbery_attempt()
    print(bright(red("Testing robbery_attempt with Gentleman's Charm")))
    player = new_player(items=["Gentleman's Charm"])
    player.robbery_attempt()
    print(bright(red("Testing robbery_attempt with Ghost Protocol")))
    player = new_player(items=['Ghost Protocol'])
    player.robbery_attempt()
    print(bright(red("Testing robbery_attempt with Padlock")))
    player = new_player(items=['Padlock'])
    player.robbery_attempt()
    print(bright(red("Testing robbery_attempt with Pocket Knife")))
    player = new_player(items=['Pocket Knife'])
    player.robbery_attempt()
    print(bright(red("Testing robbery_attempt with Road Warrior Armor")))
    player = new_player(items=['Road Warrior Armor'])
    player.robbery_attempt()
    print(bright(red("Testing robbery_attempt with Shiv")))
    player = new_player(items=['Shiv'])
    player.robbery_attempt()
    print(bright(red("Testing robbery_attempt with Sneaky Peeky Goggles")))
    player = new_player(items=['Sneaky Peeky Goggles'])
    player.robbery_attempt()
    print(bright(red("Testing robbery_attempt with Sneaky Peeky Shades")))
    player = new_player(items=['Sneaky Peeky Shades'])
    player.robbery_attempt()
    print(bright(red("Testing robbery_attempt with Street Fighter Set")))
    player = new_player(items=['Street Fighter Set'])
    player.robbery_attempt()

def social_encounter():
    print(bright(red("TESTING social_encounter with no items")))
    player = new_player()
    player.social_encounter()
    print(bright(red("Testing social_encounter with Animal Magnetism")))
    player = new_player(items=['Animal Magnetism'])
    player.social_encounter()
    print(bright(red("Testing social_encounter with Brass Knuckles")))
    player = new_player(items=['Brass Knuckles'])
    player.social_encounter()
    print(bright(red("Testing social_encounter with Breath Mints")))
    player = new_player(items=['Breath Mints'])
    player.social_encounter()
    print(bright(red("Testing social_encounter with Dealer's Grudge")))
    player = new_player(items=["Dealer's Grudge"])
    player.social_encounter()
    print(bright(red("Testing social_encounter with Dealer's Mercy")))
    player = new_player(items=["Dealer's Mercy"])
    player.social_encounter()
    print(bright(red("Testing social_encounter with Deck of Cards")))
    player = new_player(items=['Deck of Cards'])
    player.social_encounter()
    print(bright(red("Testing social_encounter with Delight Indicator")))
    player = new_player(items=['Delight Indicator'])
    player.social_encounter()
    print(bright(red("Testing social_encounter with Delight Manipulator")))
    player = new_player(items=['Delight Manipulator'])
    player.social_encounter()
    print(bright(red("Testing social_encounter with Dirty Old Hat")))
    player = new_player(items=['Dirty Old Hat'])
    player.social_encounter()
    print(bright(red("Testing social_encounter with Expensive Cologne")))
    player = new_player(items=['Expensive Cologne'])
    player.social_encounter()
    print(bright(red("Testing social_encounter with Fate Reader")))
    player = new_player(items=['Fate Reader'])
    player.social_encounter()
    print(bright(red("Testing social_encounter with Flask of Split Serum")))
    player = new_player(items=['Flask of Split Serum'])
    player.social_encounter()
    print(bright(red("Testing social_encounter with Gambler's Chalice")))
    player = new_player(items=["Gambler's Chalice"])
    player.social_encounter()
    print(bright(red("Testing social_encounter with Gas Mask")))
    player = new_player(items=['Gas Mask'])
    player.social_encounter()
    print(bright(red("Testing social_encounter with Gentleman's Charm")))
    player = new_player(items=["Gentleman's Charm"])
    player.social_encounter()
    print(bright(red("Testing social_encounter with Golden Watch")))
    player = new_player(items=['Golden Watch'])
    player.social_encounter()
    print(bright(red("Testing social_encounter with Heirloom Set")))
    player = new_player(items=['Heirloom Set'])
    player.social_encounter()
    print(bright(red("Testing social_encounter with Intelligence Dossier")))
    player = new_player(items=['Intelligence Dossier'])
    player.social_encounter()
    print(bright(red("Testing social_encounter with King of the Road")))
    player = new_player(items=['King of the Road'])
    player.social_encounter()
    print(bright(red("Testing social_encounter with Master of Games")))
    player = new_player(items=['Master of Games'])
    player.social_encounter()
    print(bright(red("Testing social_encounter with Mirror of Duality")))
    player = new_player(items=['Mirror of Duality'])
    player.social_encounter()
    print(bright(red("Testing social_encounter with Necronomicon")))
    player = new_player(items=['Necronomicon'])
    player.social_encounter()
    print(bright(red("Testing social_encounter with Old Money Identity")))
    player = new_player(items=['Old Money Identity'])
    player.social_encounter()
    print(bright(red("Testing social_encounter with Overflowing Goblet")))
    player = new_player(items=['Overflowing Goblet'])
    player.social_encounter()
    print(bright(red("Testing social_encounter with Power Move Kit")))
    player = new_player(items=['Power Move Kit'])
    player.social_encounter()
    print(bright(red("Testing social_encounter with Sapphire Watch")))
    player = new_player(items=['Sapphire Watch'])
    player.social_encounter()
    print(bright(red("Testing social_encounter with Tear Gas")))
    player = new_player(items=['Tear Gas'])
    player.social_encounter()
    print(bright(red("Testing social_encounter with Twin's Locket")))
    player = new_player(items=["Twin's Locket"])
    player.social_encounter()
    print(bright(red("Testing social_encounter with Unwashed Hair")))
    player = new_player(items=['Unwashed Hair'])
    player.social_encounter()
    print(bright(red("Testing social_encounter with Velvet Gloves")))
    player = new_player(items=['Velvet Gloves'])
    player.social_encounter()
    print(bright(red("Testing social_encounter with Vintage Wine")))
    player = new_player(items=['Vintage Wine'])
    player.social_encounter()
    print(bright(red("Testing social_encounter with Voice Soother")))
    player = new_player(items=['Voice Soother'])
    player.social_encounter()
    print(bright(red("Testing social_encounter with Worn Gloves")))
    player = new_player(items=['Worn Gloves'])
    player.social_encounter()

def street_musician():
    print(bright(red("TESTING street_musician with no items")))
    player = new_player()
    player.street_musician()

def street_performer():
    print(bright(red("TESTING street_performer with no items")))
    player = new_player()
    player.street_performer()

def street_performer_duel():
    print(bright(red("TESTING street_performer_duel with no items")))
    player = new_player()
    player.street_performer_duel()

def talking_to_yourself():
    print(bright(red("TESTING talking_to_yourself with no items")))
    player = new_player()
    player.talking_to_yourself()

def the_doppelganger():
    print(bright(red("TESTING the_doppelganger with no items")))
    player = new_player()
    player.the_doppelganger()
    print(bright(red("Testing the_doppelganger with Mirror of Duality")))
    player = new_player(items=['Mirror of Duality'])
    player.the_doppelganger()
    print(bright(red("Testing the_doppelganger with Twin's Locket")))
    player = new_player(items=["Twin's Locket"])
    player.the_doppelganger()

def the_food_truck():
    print(bright(red("TESTING the_food_truck with no items")))
    player = new_player()
    player.the_food_truck()

def the_gambler_ghost():
    print(bright(red("TESTING the_gambler_ghost with no items")))
    player = new_player()
    player.the_gambler_ghost()

def the_hitchhiker():
    print(bright(red("TESTING the_hitchhiker with no items")))
    player = new_player()
    player.the_hitchhiker()

def the_mime():
    print(bright(red("TESTING the_mime with no items")))
    player = new_player()
    player.the_mime()

def the_photographer():
    print(bright(red("TESTING the_photographer with no items")))
    player = new_player()
    player.the_photographer()

def the_prophet():
    print(bright(red("TESTING the_prophet with no items")))
    player = new_player()
    player.the_prophet()
    print(bright(red("Testing the_prophet with Binding Portrait")))
    player = new_player(items=['Binding Portrait'])
    player.the_prophet()
    print(bright(red("Testing the_prophet with Eldritch Candle")))
    player = new_player(items=['Eldritch Candle'])
    player.the_prophet()
    print(bright(red("Testing the_prophet with Gambler's Grimoire")))
    player = new_player(items=["Gambler's Grimoire"])
    player.the_prophet()
    print(bright(red("Testing the_prophet with Oracle's Tome")))
    player = new_player(items=["Oracle's Tome"])
    player.the_prophet()

def the_sleeping_stranger():
    print(bright(red("TESTING the_sleeping_stranger with no items")))
    player = new_player()
    player.the_sleeping_stranger()

def trash_treasure():
    print(bright(red("TESTING trash_treasure with no items")))
    player = new_player()
    player.trash_treasure()

def trusty_tom_coupon_mailer():
    print(bright(red("TESTING trusty_tom_coupon_mailer with no items")))
    player = new_player()
    player.trusty_tom_coupon_mailer()

def vending_machine_luck():
    print(bright(red("TESTING vending_machine_luck with no items")))
    player = new_player()
    player.vending_machine_luck()

def vinnie_referral_card():
    print(bright(red("TESTING vinnie_referral_card with no items")))
    player = new_player()
    player.vinnie_referral_card()
    print(bright(red("Testing vinnie_referral_card with Car")))
    player = new_player(items=['Car'])
    player.vinnie_referral_card()

def whats_my_name():
    print(bright(red("TESTING whats_my_name with no items")))
    player = new_player()
    player.whats_my_name()

def windblown_worn_map():
    print(bright(red("TESTING windblown_worn_map with no items")))
    player = new_player()
    player.windblown_worn_map()
    print(bright(red("Testing windblown_worn_map with Car")))
    player = new_player(items=['Car'])
    player.windblown_worn_map()
    print(bright(red("Testing windblown_worn_map with Map")))
    player = new_player(items=['Map'])
    player.windblown_worn_map()
    print(bright(red("Testing windblown_worn_map with Worn Map")))
    player = new_player(items=['Worn Map'])
    player.windblown_worn_map()

def wine_and_dine():
    print(bright(red("TESTING wine_and_dine with no items")))
    player = new_player()
    player.wine_and_dine()
    print(bright(red("Testing wine_and_dine with Silver Flask")))
    player = new_player(items=['Silver Flask'])
    player.wine_and_dine()
    print(bright(red("Testing wine_and_dine with Vintage Wine")))
    player = new_player(items=['Vintage Wine'])
    player.wine_and_dine()

def witch_doctor_matchbook():
    print(bright(red("TESTING witch_doctor_matchbook with no items")))
    player = new_player()
    player.witch_doctor_matchbook()
    print(bright(red("Testing witch_doctor_matchbook with Car")))
    player = new_player(items=['Car'])
    player.witch_doctor_matchbook()

def wrong_item_dirty_hat_dinner():
    print(bright(red("TESTING wrong_item_dirty_hat_dinner with no items")))
    player = new_player()
    player.wrong_item_dirty_hat_dinner()
    print(bright(red("Testing wrong_item_dirty_hat_dinner with Dirty Old Hat")))
    player = new_player(items=['Dirty Old Hat'])
    player.wrong_item_dirty_hat_dinner()
    print(bright(red("Testing wrong_item_dirty_hat_dinner with Unwashed Hair")))
    player = new_player(items=['Unwashed Hair'])
    player.wrong_item_dirty_hat_dinner()

def wrong_item_pest_control_romance():
    print(bright(red("TESTING wrong_item_pest_control_romance with no items")))
    player = new_player()
    player.wrong_item_pest_control_romance()
    print(bright(red("Testing wrong_item_pest_control_romance with Pest Control")))
    player = new_player(items=['Pest Control'])
    player.wrong_item_pest_control_romance()

def wrong_item_vermin_bomb_romance():
    print(bright(red("TESTING wrong_item_vermin_bomb_romance with no items")))
    player = new_player()
    player.wrong_item_vermin_bomb_romance()
    print(bright(red("Testing wrong_item_vermin_bomb_romance with Vermin Bomb")))
    player = new_player(items=['Vermin Bomb'])
    player.wrong_item_vermin_bomb_romance()

def wrong_number():
    print(bright(red("TESTING wrong_number with no items")))
    player = new_player()
    player.wrong_number()

def yard_sale_find():
    print(bright(red("TESTING yard_sale_find with no items")))
    player = new_player()
    player.yard_sale_find()


"""story.events_day_storylines.py"""
def crossover_all_chains_complete():
    print(bright(red("TESTING crossover_all_chains_complete with no items")))
    player = new_player()
    player.crossover_all_chains_complete()
    print(bright(red("Testing crossover_all_chains_complete with Junkyard Crown")))
    player = new_player(items=['Junkyard Crown'])
    player.crossover_all_chains_complete()
    print(bright(red("Testing crossover_all_chains_complete with Reunion Photo")))
    player = new_player(items=['Reunion Photo'])
    player.crossover_all_chains_complete()

def crossover_artisan_rose_gift():
    print(bright(red("TESTING crossover_artisan_rose_gift with no items")))
    player = new_player()
    player.crossover_artisan_rose_gift()
    print(bright(red("Testing crossover_artisan_rose_gift with Scrap Metal Rose")))
    player = new_player(items=['Scrap Metal Rose'])
    player.crossover_artisan_rose_gift()

def crossover_night_vision_bonus():
    print(bright(red("TESTING crossover_night_vision_bonus with no items")))
    player = new_player()
    player.crossover_night_vision_bonus()
    print(bright(red("Testing crossover_night_vision_bonus with Night Vision Scope")))
    player = new_player(items=['Night Vision Scope'])
    player.crossover_night_vision_bonus()

def crossover_radio_hermit():
    print(bright(red("TESTING crossover_radio_hermit with no items")))
    player = new_player()
    player.crossover_radio_hermit()

def gift_from_suzy():
    print(bright(red("TESTING gift_from_suzy with no items")))
    player = new_player()
    player.gift_from_suzy()

def hermit_camp_return():
    print(bright(red("TESTING hermit_camp_return with no items")))
    player = new_player()
    player.hermit_camp_return()

def hermit_hollow_oak():
    print(bright(red("TESTING hermit_hollow_oak with no items")))
    player = new_player()
    player.hermit_hollow_oak()
    print(bright(red("Testing hermit_hollow_oak with Carved Walking Stick")))
    player = new_player(items=['Carved Walking Stick'])
    player.hermit_hollow_oak()

def hermit_journal_study():
    print(bright(red("TESTING hermit_journal_study with no items")))
    player = new_player()
    player.hermit_journal_study()
    print(bright(red("Testing hermit_journal_study with Hermit's Journal")))
    player = new_player(items=["Hermit's Journal"])
    player.hermit_journal_study()

def hermit_trail_discovery():
    print(bright(red("TESTING hermit_trail_discovery with no items")))
    player = new_player()
    player.hermit_trail_discovery()
    print(bright(red("Testing hermit_trail_discovery with Worn Map")))
    player = new_player(items=['Worn Map'])
    player.hermit_trail_discovery()

def hermit_trail_stranger():
    print(bright(red("TESTING hermit_trail_stranger with no items")))
    player = new_player()
    player.hermit_trail_stranger()
    print(bright(red("Testing hermit_trail_stranger with Carved Walking Stick")))
    player = new_player(items=['Carved Walking Stick'])
    player.hermit_trail_stranger()
    print(bright(red("Testing hermit_trail_stranger with Hermit's Journal")))
    player = new_player(items=["Hermit's Journal"])
    player.hermit_trail_stranger()

def junkyard_artisan_meet():
    print(bright(red("TESTING junkyard_artisan_meet with no items")))
    player = new_player()
    player.junkyard_artisan_meet()
    print(bright(red("Testing junkyard_artisan_meet with Welding Goggles")))
    player = new_player(items=['Welding Goggles'])
    player.junkyard_artisan_meet()

def junkyard_gideon_story():
    print(bright(red("TESTING junkyard_gideon_story with no items")))
    player = new_player()
    player.junkyard_gideon_story()

def junkyard_lesson_one():
    print(bright(red("TESTING junkyard_lesson_one with no items")))
    player = new_player()
    player.junkyard_lesson_one()

def junkyard_lesson_two():
    print(bright(red("TESTING junkyard_lesson_two with no items")))
    player = new_player()
    player.junkyard_lesson_two()

def junkyard_masterpiece():
    print(bright(red("TESTING junkyard_masterpiece with no items")))
    player = new_player()
    player.junkyard_masterpiece()
    print(bright(red("Testing junkyard_masterpiece with Scrap Metal Rose")))
    player = new_player(items=['Scrap Metal Rose'])
    player.junkyard_masterpiece()

def lost_dog_culprit():
    print(bright(red("TESTING lost_dog_culprit with no items")))
    player = new_player()
    player.lost_dog_culprit()
    print(bright(red("Testing lost_dog_culprit with Torn Collar")))
    player = new_player(items=['Torn Collar'])
    player.lost_dog_culprit()

def lost_dog_flyers_found():
    print(bright(red("TESTING lost_dog_flyers_found with no items")))
    player = new_player()
    player.lost_dog_flyers_found()

def lost_dog_investigation():
    print(bright(red("TESTING lost_dog_investigation with no items")))
    player = new_player()
    player.lost_dog_investigation()
    print(bright(red("Testing lost_dog_investigation with Dog Whistle")))
    player = new_player(items=['Dog Whistle'])
    player.lost_dog_investigation()

def lost_dog_reunion():
    print(bright(red("TESTING lost_dog_reunion with no items")))
    player = new_player()
    player.lost_dog_reunion()
    print(bright(red("Testing lost_dog_reunion with Blanket")))
    player = new_player(items=['Blanket'])
    player.lost_dog_reunion()

def lost_dog_whistle_search():
    print(bright(red("TESTING lost_dog_whistle_search with no items")))
    player = new_player()
    player.lost_dog_whistle_search()
    print(bright(red("Testing lost_dog_whistle_search with Dog Whistle")))
    player = new_player(items=['Dog Whistle'])
    player.lost_dog_whistle_search()
    print(bright(red("Testing lost_dog_whistle_search with Pocket Knife")))
    player = new_player(items=['Pocket Knife'])
    player.lost_dog_whistle_search()
    print(bright(red("Testing lost_dog_whistle_search with Tool Kit")))
    player = new_player(items=['Tool Kit'])
    player.lost_dog_whistle_search()

def midnight_radio_broadcast():
    print(bright(red("TESTING midnight_radio_broadcast with no items")))
    player = new_player()
    player.midnight_radio_broadcast()
    print(bright(red("Testing midnight_radio_broadcast with Static Recorder")))
    player = new_player(items=['Static Recorder'])
    player.midnight_radio_broadcast()

def midnight_radio_frequency():
    print(bright(red("TESTING midnight_radio_frequency with no items")))
    player = new_player()
    player.midnight_radio_frequency()

def midnight_radio_pole():
    print(bright(red("TESTING midnight_radio_pole with no items")))
    player = new_player()
    player.midnight_radio_pole()

def midnight_radio_signal():
    print(bright(red("TESTING midnight_radio_signal with no items")))
    player = new_player()
    player.midnight_radio_signal()
    print(bright(red("Testing midnight_radio_signal with Signal Booster")))
    player = new_player(items=['Signal Booster'])
    player.midnight_radio_signal()

def midnight_radio_visit():
    print(bright(red("TESTING midnight_radio_visit with no items")))
    player = new_player()
    player.midnight_radio_visit()
    print(bright(red("Testing midnight_radio_visit with Pirate Radio Flyer")))
    player = new_player(items=['Pirate Radio Flyer'])
    player.midnight_radio_visit()
    print(bright(red("Testing midnight_radio_visit with Strange Frequency Dial")))
    player = new_player(items=['Strange Frequency Dial'])
    player.midnight_radio_visit()

def suzy_the_snitch():
    print(bright(red("TESTING suzy_the_snitch with no items")))
    player = new_player()
    player.suzy_the_snitch()


"""story.events_day_surreal.py"""
def alien_abduction():
    print(bright(red("TESTING alien_abduction with no items")))
    player = new_player()
    player.alien_abduction()
    print(bright(red("Testing alien_abduction with Mobile Workshop")))
    player = new_player(items=['Mobile Workshop'])
    player.alien_abduction()

def blood_moon_bargain():
    print(bright(red("TESTING blood_moon_bargain with no items")))
    player = new_player()
    player.blood_moon_bargain()
    print(bright(red("Testing blood_moon_bargain with Dark Pact Reliquary")))
    player = new_player(items=['Dark Pact Reliquary'])
    player.blood_moon_bargain()
    print(bright(red("Testing blood_moon_bargain with Dealer's Grudge")))
    player = new_player(items=["Dealer's Grudge"])
    player.blood_moon_bargain()
    print(bright(red("Testing blood_moon_bargain with Dealer's Mercy")))
    player = new_player(items=["Dealer's Mercy"])
    player.blood_moon_bargain()
    print(bright(red("Testing blood_moon_bargain with Eldritch Candle")))
    player = new_player(items=['Eldritch Candle'])
    player.blood_moon_bargain()
    print(bright(red("Testing blood_moon_bargain with Flask of Dealer's Whispers")))
    player = new_player(items=["Flask of Dealer's Whispers"])
    player.blood_moon_bargain()
    print(bright(red("Testing blood_moon_bargain with Fortune Cards")))
    player = new_player(items=['Fortune Cards'])
    player.blood_moon_bargain()
    print(bright(red("Testing blood_moon_bargain with Gambler's Grimoire")))
    player = new_player(items=["Gambler's Grimoire"])
    player.blood_moon_bargain()
    print(bright(red("Testing blood_moon_bargain with Mind Shield")))
    player = new_player(items=['Mind Shield'])
    player.blood_moon_bargain()
    print(bright(red("Testing blood_moon_bargain with Necronomicon")))
    player = new_player(items=['Necronomicon'])
    player.blood_moon_bargain()
    print(bright(red("Testing blood_moon_bargain with Oracle's Tome")))
    player = new_player(items=["Oracle's Tome"])
    player.blood_moon_bargain()
    print(bright(red("Testing blood_moon_bargain with Soul Forge")))
    player = new_player(items=['Soul Forge'])
    player.blood_moon_bargain()

def dance_battle():
    print(bright(red("TESTING dance_battle with no items")))
    player = new_player()
    player.dance_battle()

def fourth_wall_break():
    print(bright(red("TESTING fourth_wall_break with no items")))
    player = new_player()
    player.fourth_wall_break()

def mirror_stranger():
    print(bright(red("TESTING mirror_stranger with no items")))
    player = new_player()
    player.mirror_stranger()
    print(bright(red("Testing mirror_stranger with Flask of Split Serum")))
    player = new_player(items=['Flask of Split Serum'])
    player.mirror_stranger()
    print(bright(red("Testing mirror_stranger with Gambler's Grimoire")))
    player = new_player(items=["Gambler's Grimoire"])
    player.mirror_stranger()
    print(bright(red("Testing mirror_stranger with Marvin's Monocle")))
    player = new_player(items=["Marvin's Monocle"])
    player.mirror_stranger()
    print(bright(red("Testing mirror_stranger with Mirror of Duality")))
    player = new_player(items=['Mirror of Duality'])
    player.mirror_stranger()
    print(bright(red("Testing mirror_stranger with Seer's Chronicle")))
    player = new_player(items=["Seer's Chronicle"])
    player.mirror_stranger()
    print(bright(red("Testing mirror_stranger with Third Eye")))
    player = new_player(items=['Third Eye'])
    player.mirror_stranger()
    print(bright(red("Testing mirror_stranger with Twin's Locket")))
    player = new_player(items=["Twin's Locket"])
    player.mirror_stranger()

def sock_puppet_therapist():
    print(bright(red("TESTING sock_puppet_therapist with no items")))
    player = new_player()
    player.sock_puppet_therapist()

def the_collector():
    print(bright(red("TESTING the_collector with no items")))
    player = new_player()
    player.the_collector()

def the_empty_room():
    print(bright(red("TESTING the_empty_room with no items")))
    player = new_player()
    player.the_empty_room()
    print(bright(red("Testing the_empty_room with Delight Indicator")))
    player = new_player(items=['Delight Indicator'])
    player.the_empty_room()
    print(bright(red("Testing the_empty_room with Delight Manipulator")))
    player = new_player(items=['Delight Manipulator'])
    player.the_empty_room()

def the_glitch():
    print(bright(red("TESTING the_glitch with no items")))
    player = new_player()
    player.the_glitch()
    print(bright(red("Testing the_glitch with Smelling Salts")))
    player = new_player(items=['Smelling Salts'])
    player.the_glitch()

def time_loop():
    print(bright(red("TESTING time_loop with no items")))
    player = new_player()
    player.time_loop()
    print(bright(red("Testing time_loop with Deck of Cards")))
    player = new_player(items=['Deck of Cards'])
    player.time_loop()
    print(bright(red("Testing time_loop with Dream Catcher")))
    player = new_player(items=['Dream Catcher'])
    player.time_loop()
    print(bright(red("Testing time_loop with Fortune Cards")))
    player = new_player(items=['Fortune Cards'])
    player.time_loop()
    print(bright(red("Testing time_loop with Gambler's Grimoire")))
    player = new_player(items=["Gambler's Grimoire"])
    player.time_loop()
    print(bright(red("Testing time_loop with Grandfather Clock")))
    player = new_player(items=['Grandfather Clock'])
    player.time_loop()
    print(bright(red("Testing time_loop with Oracle's Tome")))
    player = new_player(items=["Oracle's Tome"])
    player.time_loop()
    print(bright(red("Testing time_loop with Pocket Watch")))
    player = new_player(items=['Pocket Watch'])
    player.time_loop()

def wrong_universe():
    print(bright(red("TESTING wrong_universe with no items")))
    player = new_player()
    player.wrong_universe()
    print(bright(red("Testing wrong_universe with Fate Reader")))
    player = new_player(items=['Fate Reader'])
    player.wrong_universe()
    print(bright(red("Testing wrong_universe with Third Eye")))
    player = new_player(items=['Third Eye'])
    player.wrong_universe()


"""story.events_day_survival.py"""
def another_spider_bite():
    print(bright(red("TESTING another_spider_bite with no items")))
    player = new_player()
    player.another_spider_bite()
    print(bright(red("Testing another_spider_bite with Flask of Anti-Venom")))
    player = new_player(items=['Flask of Anti-Venom'])
    player.another_spider_bite()
    print(bright(red("Testing another_spider_bite with Pest Control")))
    player = new_player(items=['Pest Control'])
    player.another_spider_bite()

def ant_bite():
    print(bright(red("TESTING ant_bite with no items")))
    player = new_player()
    player.ant_bite()
    print(bright(red("Testing ant_bite with Pest Control")))
    player = new_player(items=['Pest Control'])
    player.ant_bite()

def ant_invasion():
    print(bright(red("TESTING ant_invasion with no items")))
    player = new_player()
    player.ant_invasion()
    print(bright(red("Testing ant_invasion with Pest Control")))
    player = new_player(items=['Pest Control'])
    player.ant_invasion()
    print(bright(red("Testing ant_invasion with Tear Gas")))
    player = new_player(items=['Tear Gas'])
    player.ant_invasion()

def back_pain():
    print(bright(red("TESTING back_pain with no items")))
    player = new_player()
    player.back_pain()
    print(bright(red("Testing back_pain with First Aid Kit")))
    player = new_player(items=['First Aid Kit'])
    player.back_pain()

def bad_hair_day():
    print(bright(red("TESTING bad_hair_day with no items")))
    player = new_player()
    player.bad_hair_day()

def beautiful_sunrise():
    print(bright(red("TESTING beautiful_sunrise with no items")))
    player = new_player()
    player.beautiful_sunrise()
    print(bright(red("Testing beautiful_sunrise with Flask of Fortunate Day")))
    player = new_player(items=['Flask of Fortunate Day'])
    player.beautiful_sunrise()

def bird_droppings():
    print(bright(red("TESTING bird_droppings with no items")))
    player = new_player()
    player.bird_droppings()

def broken_belonging():
    print(bright(red("TESTING broken_belonging with no items")))
    player = new_player()
    player.broken_belonging()
    print(bright(red("Testing broken_belonging with Duct Tape")))
    player = new_player(items=['Duct Tape'])
    player.broken_belonging()
    print(bright(red("Testing broken_belonging with Super Glue")))
    player = new_player(items=['Super Glue'])
    player.broken_belonging()

def car_battery_dead():
    print(bright(red("TESTING car_battery_dead with no items")))
    player = new_player()
    player.car_battery_dead()
    print(bright(red("Testing car_battery_dead with Tool Kit")))
    player = new_player(items=['Tool Kit'])
    player.car_battery_dead()

def car_smell():
    print(bright(red("TESTING car_smell with no items")))
    player = new_player()
    player.car_smell()
    print(bright(red("Testing car_smell with Air Freshener")))
    player = new_player(items=['Air Freshener'])
    player.car_smell()
    print(bright(red("Testing car_smell with Smelling Salts")))
    player = new_player(items=['Smelling Salts'])
    player.car_smell()

def car_wont_start():
    print(bright(red("TESTING car_wont_start with no items")))
    player = new_player()
    player.car_wont_start()
    print(bright(red("Testing car_wont_start with SOS Kit")))
    player = new_player(items=['SOS Kit'])
    player.car_wont_start()

def cold_gets_worse():
    print(bright(red("TESTING cold_gets_worse with no items")))
    player = new_player()
    player.cold_gets_worse()

def construction_noise():
    print(bright(red("TESTING construction_noise with no items")))
    player = new_player()
    player.construction_noise()

def damaged_exhaust_again():
    print(bright(red("TESTING damaged_exhaust_again with no items")))
    player = new_player()
    player.damaged_exhaust_again()

def damaged_exhaust_fixed():
    print(bright(red("TESTING damaged_exhaust_fixed with no items")))
    player = new_player()
    player.damaged_exhaust_fixed()

def deja_vu():
    print(bright(red("TESTING deja_vu with no items")))
    player = new_player()
    player.deja_vu()
    print(bright(red("Testing deja_vu with Flask of Pocket Aces")))
    player = new_player(items=['Flask of Pocket Aces'])
    player.deja_vu()

def deja_vu_again():
    print(bright(red("TESTING deja_vu_again with no items")))
    player = new_player()
    player.deja_vu_again()

def empty_event():
    print(bright(red("TESTING empty_event with no items")))
    player = new_player()
    player.empty_event()

def flat_tire():
    print(bright(red("TESTING flat_tire with no items")))
    player = new_player()
    player.flat_tire()
    print(bright(red("Testing flat_tire with Spare Tire")))
    player = new_player(items=['Spare Tire'])
    player.flat_tire()

def flat_tire_again():
    print(bright(red("TESTING flat_tire_again with no items")))
    player = new_player()
    player.flat_tire_again()
    print(bright(red("Testing flat_tire_again with Duct Tape")))
    player = new_player(items=['Duct Tape'])
    player.flat_tire_again()
    print(bright(red("Testing flat_tire_again with Spare Tire")))
    player = new_player(items=['Spare Tire'])
    player.flat_tire_again()

def found_gift_card():
    print(bright(red("TESTING found_gift_card with no items")))
    player = new_player()
    player.found_gift_card()

def found_old_photo():
    print(bright(red("TESTING found_old_photo with no items")))
    player = new_player()
    player.found_old_photo()

def found_twenty():
    print(bright(red("TESTING found_twenty with no items")))
    player = new_player()
    player.found_twenty()

def freezing_night():
    print(bright(red("TESTING freezing_night with no items")))
    player = new_player()
    player.freezing_night()
    print(bright(red("Testing freezing_night with Blanket")))
    player = new_player(items=['Blanket'])
    player.freezing_night()
    print(bright(red("Testing freezing_night with Emergency Blanket")))
    player = new_player(items=['Emergency Blanket'])
    player.freezing_night()
    print(bright(red("Testing freezing_night with Fire Starter Kit")))
    player = new_player(items=['Fire Starter Kit'])
    player.freezing_night()
    print(bright(red("Testing freezing_night with Flask of No Bust")))
    player = new_player(items=['Flask of No Bust'])
    player.freezing_night()
    print(bright(red("Testing freezing_night with Hand Warmers")))
    player = new_player(items=['Hand Warmers'])
    player.freezing_night()
    print(bright(red("Testing freezing_night with Phoenix Feather")))
    player = new_player(items=['Phoenix Feather'])
    player.freezing_night()
    print(bright(red("Testing freezing_night with Survival Bivouac")))
    player = new_player(items=['Survival Bivouac'])
    player.freezing_night()
    print(bright(red("Testing freezing_night with Velvet Gloves")))
    player = new_player(items=['Velvet Gloves'])
    player.freezing_night()
    print(bright(red("Testing freezing_night with Worn Gloves")))
    player = new_player(items=['Worn Gloves'])
    player.freezing_night()

def good_hair_day():
    print(bright(red("TESTING good_hair_day with no items")))
    player = new_player()
    player.good_hair_day()

def got_a_cold():
    print(bright(red("TESTING got_a_cold with no items")))
    player = new_player()
    player.got_a_cold()
    print(bright(red("Testing got_a_cold with Cough Drops")))
    player = new_player(items=['Cough Drops'])
    player.got_a_cold()
    print(bright(red("Testing got_a_cold with Home Remedy")))
    player = new_player(items=['Home Remedy'])
    player.got_a_cold()
    print(bright(red("Testing got_a_cold with Hydration Station")))
    player = new_player(items=['Hydration Station'])
    player.got_a_cold()
    print(bright(red("Testing got_a_cold with Voice Soother")))
    player = new_player(items=['Voice Soother'])
    player.got_a_cold()

def got_a_tan():
    print(bright(red("TESTING got_a_tan with no items")))
    player = new_player()
    player.got_a_tan()

def hungry_cockroach():
    print(bright(red("TESTING hungry_cockroach with no items")))
    player = new_player()
    player.hungry_cockroach()
    print(bright(red("Testing hungry_cockroach with Pest Control")))
    player = new_player(items=['Pest Control'])
    player.hungry_cockroach()

def important_document():
    print(bright(red("TESTING important_document with no items")))
    player = new_player()
    player.important_document()
    print(bright(red("Testing important_document with Fancy Pen")))
    player = new_player(items=['Fancy Pen'])
    player.important_document()

def left_door_open():
    print(bright(red("TESTING left_door_open with no items")))
    player = new_player()
    player.left_door_open()
    print(bright(red("Testing left_door_open with Pest Control")))
    player = new_player(items=['Pest Control'])
    player.left_door_open()

def left_trunk_open():
    print(bright(red("TESTING left_trunk_open with no items")))
    player = new_player()
    player.left_trunk_open()
    print(bright(red("Testing left_trunk_open with Pest Control")))
    player = new_player(items=['Pest Control'])
    player.left_trunk_open()

def left_window_down():
    print(bright(red("TESTING left_window_down with no items")))
    player = new_player()
    player.left_window_down()

def lost_wallet():
    print(bright(red("TESTING lost_wallet with no items")))
    player = new_player()
    player.lost_wallet()
    print(bright(red("Testing lost_wallet with Signal Mirror")))
    player = new_player(items=['Signal Mirror'])
    player.lost_wallet()

def morning_fog():
    print(bright(red("TESTING morning_fog with no items")))
    player = new_player()
    player.morning_fog()
    print(bright(red("Testing morning_fog with Binocular Scope")))
    player = new_player(items=['Binocular Scope'])
    player.morning_fog()
    print(bright(red("Testing morning_fog with Golden Compass")))
    player = new_player(items=['Golden Compass'])
    player.morning_fog()
    print(bright(red("Testing morning_fog with Rusty Compass")))
    player = new_player(items=['Rusty Compass'])
    player.morning_fog()

def morning_stretch():
    print(bright(red("TESTING morning_stretch with no items")))
    player = new_player()
    player.morning_stretch()
    print(bright(red("Testing morning_stretch with Pursuit Package")))
    player = new_player(items=['Pursuit Package'])
    player.morning_stretch()
    print(bright(red("Testing morning_stretch with Running Shoes")))
    player = new_player(items=['Running Shoes'])
    player.morning_stretch()

def mosquito_bite_infection():
    print(bright(red("TESTING mosquito_bite_infection with no items")))
    player = new_player()
    player.mosquito_bite_infection()
    print(bright(red("Testing mosquito_bite_infection with First Aid Kit")))
    player = new_player(items=['First Aid Kit'])
    player.mosquito_bite_infection()
    print(bright(red("Testing mosquito_bite_infection with Wound Salve")))
    player = new_player(items=['Wound Salve'])
    player.mosquito_bite_infection()

def mosquito_swarm():
    print(bright(red("TESTING mosquito_swarm with no items")))
    player = new_player()
    player.mosquito_swarm()
    print(bright(red("Testing mosquito_swarm with Bug Spray")))
    player = new_player(items=['Bug Spray'])
    player.mosquito_swarm()
    print(bright(red("Testing mosquito_swarm with Smoke Flare")))
    player = new_player(items=['Smoke Flare'])
    player.mosquito_swarm()

def mysterious_note():
    print(bright(red("TESTING mysterious_note with no items")))
    player = new_player()
    player.mysterious_note()

def mystery_car_problem_worsens():
    print(bright(red("TESTING mystery_car_problem_worsens with no items")))
    player = new_player()
    player.mystery_car_problem_worsens()

def need_fire():
    print(bright(red("TESTING need_fire with no items")))
    player = new_player()
    player.need_fire()
    print(bright(red("Testing need_fire with Animal Bait")))
    player = new_player(items=['Animal Bait'])
    player.need_fire()
    print(bright(red("Testing need_fire with Fire Launcher")))
    player = new_player(items=['Fire Launcher'])
    player.need_fire()
    print(bright(red("Testing need_fire with Fishing Rod")))
    player = new_player(items=['Fishing Rod'])
    player.need_fire()
    print(bright(red("Testing need_fire with Lighter")))
    player = new_player(items=['Lighter'])
    player.need_fire()
    print(bright(red("Testing need_fire with Monogrammed Lighter")))
    player = new_player(items=['Monogrammed Lighter'])
    player.need_fire()
    print(bright(red("Testing need_fire with Nomad's Camp")))
    player = new_player(items=["Nomad's Camp"])
    player.need_fire()
    print(bright(red("Testing need_fire with Provider's Kit")))
    player = new_player(items=["Provider's Kit"])
    player.need_fire()
    print(bright(red("Testing need_fire with Road Flares")))
    player = new_player(items=['Road Flares'])
    player.need_fire()

def nice_weather():
    print(bright(red("TESTING nice_weather with no items")))
    player = new_player()
    player.nice_weather()
    print(bright(red("Testing nice_weather with Nomad's Camp")))
    player = new_player(items=["Nomad's Camp"])
    player.nice_weather()
    print(bright(red("Testing nice_weather with Wanderer's Rest")))
    player = new_player(items=["Wanderer's Rest"])
    player.nice_weather()

def penny_luck():
    print(bright(red("TESTING penny_luck with no items")))
    player = new_player()
    player.penny_luck()
    print(bright(red("Testing penny_luck with Flask of Bonus Fortune")))
    player = new_player(items=['Flask of Bonus Fortune'])
    player.penny_luck()
    print(bright(red("Testing penny_luck with Flask of Imminent Blackjack")))
    player = new_player(items=['Flask of Imminent Blackjack'])
    player.penny_luck()
    print(bright(red("Testing penny_luck with Lucky Penny")))
    player = new_player(items=['Lucky Penny'])
    player.penny_luck()

def power_outage_area():
    print(bright(red("TESTING power_outage_area with no items")))
    player = new_player()
    player.power_outage_area()

def prayer_answered():
    print(bright(red("TESTING prayer_answered with no items")))
    player = new_player()
    player.prayer_answered()

def prayer_ignored():
    print(bright(red("TESTING prayer_ignored with no items")))
    player = new_player()
    player.prayer_ignored()

def radio_static():
    print(bright(red("TESTING radio_static with no items")))
    player = new_player()
    player.radio_static()

def random_cruelty():
    print(bright(red("TESTING random_cruelty with no items")))
    player = new_player()
    player.random_cruelty()

def random_kindness():
    print(bright(red("TESTING random_kindness with no items")))
    player = new_player()
    player.random_kindness()

def roadside_breakdown():
    print(bright(red("TESTING roadside_breakdown with no items")))
    player = new_player()
    player.roadside_breakdown()
    print(bright(red("Testing roadside_breakdown with Eternal Light")))
    player = new_player(items=['Eternal Light'])
    player.roadside_breakdown()
    print(bright(red("Testing roadside_breakdown with Flashlight")))
    player = new_player(items=['Flashlight'])
    player.roadside_breakdown()
    print(bright(red("Testing roadside_breakdown with Lantern")))
    player = new_player(items=['Lantern'])
    player.roadside_breakdown()
    print(bright(red("Testing roadside_breakdown with Road Flares")))
    player = new_player(items=['Road Flares'])
    player.roadside_breakdown()
    print(bright(red("Testing roadside_breakdown with Smoke Signal Kit")))
    player = new_player(items=['Smoke Signal Kit'])
    player.roadside_breakdown()

def rubber_band_save():
    print(bright(red("TESTING rubber_band_save with no items")))
    player = new_player()
    player.rubber_band_save()
    print(bright(red("Testing rubber_band_save with Rubber Bands")))
    player = new_player(items=['Rubber Bands'])
    player.rubber_band_save()

def scorching_sun():
    print(bright(red("TESTING scorching_sun with no items")))
    player = new_player()
    player.scorching_sun()
    print(bright(red("Testing scorching_sun with All-Weather Armor")))
    player = new_player(items=['All-Weather Armor'])
    player.scorching_sun()
    print(bright(red("Testing scorching_sun with Beach Bum Disguise")))
    player = new_player(items=['Beach Bum Disguise'])
    player.scorching_sun()
    print(bright(red("Testing scorching_sun with Cheap Sunscreen")))
    player = new_player(items=['Cheap Sunscreen'])
    player.scorching_sun()
    print(bright(red("Testing scorching_sun with Cool Down Kit")))
    player = new_player(items=['Cool Down Kit'])
    player.scorching_sun()
    print(bright(red("Testing scorching_sun with Hazmat Suit")))
    player = new_player(items=['Hazmat Suit'])
    player.scorching_sun()
    print(bright(red("Testing scorching_sun with Health Indicator")))
    player = new_player(items=['Health Indicator'])
    player.scorching_sun()
    print(bright(red("Testing scorching_sun with Health Manipulator")))
    player = new_player(items=['Health Manipulator'])
    player.scorching_sun()
    print(bright(red("Testing scorching_sun with Outdoor Shield")))
    player = new_player(items=['Outdoor Shield'])
    player.scorching_sun()
    print(bright(red("Testing scorching_sun with Premium Sunscreen")))
    player = new_player(items=['Premium Sunscreen'])
    player.scorching_sun()
    print(bright(red("Testing scorching_sun with Umbrella")))
    player = new_player(items=['Umbrella'])
    player.scorching_sun()

def seat_cash():
    print(bright(red("TESTING seat_cash with no items")))
    player = new_player()
    player.seat_cash()

def someone_stole_your_stuff():
    print(bright(red("TESTING someone_stole_your_stuff with no items")))
    player = new_player()
    player.someone_stole_your_stuff()
    print(bright(red("Testing someone_stole_your_stuff with Binoculars")))
    player = new_player(items=['Binoculars'])
    player.someone_stole_your_stuff()
    print(bright(red("Testing someone_stole_your_stuff with Car Alarm Rigging")))
    player = new_player(items=['Car Alarm Rigging'])
    player.someone_stole_your_stuff()
    print(bright(red("Testing someone_stole_your_stuff with Padlock")))
    player = new_player(items=['Padlock'])
    player.someone_stole_your_stuff()

def sore_throat():
    print(bright(red("TESTING sore_throat with no items")))
    player = new_player()
    player.sore_throat()
    print(bright(red("Testing sore_throat with Cough Drops")))
    player = new_player(items=['Cough Drops'])
    player.sore_throat()

def spider_bite():
    print(bright(red("TESTING spider_bite with no items")))
    player = new_player()
    player.spider_bite()
    print(bright(red("Testing spider_bite with Flask of Anti-Venom")))
    player = new_player(items=['Flask of Anti-Venom'])
    player.spider_bite()
    print(bright(red("Testing spider_bite with Improvised Trap")))
    player = new_player(items=['Improvised Trap'])
    player.spider_bite()
    print(bright(red("Testing spider_bite with Pest Control")))
    player = new_player(items=['Pest Control'])
    player.spider_bite()
    print(bright(red("Testing spider_bite with Slingshot")))
    player = new_player(items=['Slingshot'])
    player.spider_bite()

def stretching_helps():
    print(bright(red("TESTING stretching_helps with no items")))
    player = new_player()
    player.stretching_helps()

def strong_winds():
    print(bright(red("TESTING strong_winds with no items")))
    player = new_player()
    player.strong_winds()
    print(bright(red("Testing strong_winds with Fortified Perimeter")))
    player = new_player(items=['Fortified Perimeter'])
    player.strong_winds()

def sudden_downpour():
    print(bright(red("TESTING sudden_downpour with no items")))
    player = new_player()
    player.sudden_downpour()
    print(bright(red("Testing sudden_downpour with All-Weather Armor")))
    player = new_player(items=['All-Weather Armor'])
    player.sudden_downpour()
    print(bright(red("Testing sudden_downpour with Binoculars")))
    player = new_player(items=['Binoculars'])
    player.sudden_downpour()
    print(bright(red("Testing sudden_downpour with Plastic Poncho")))
    player = new_player(items=['Plastic Poncho'])
    player.sudden_downpour()
    print(bright(red("Testing sudden_downpour with Storm Suit")))
    player = new_player(items=['Storm Suit'])
    player.sudden_downpour()
    print(bright(red("Testing sudden_downpour with Umbrella")))
    player = new_player(items=['Umbrella'])
    player.sudden_downpour()
    print(bright(red("Testing sudden_downpour with Water Purifier")))
    player = new_player(items=['Water Purifier'])
    player.sudden_downpour()

def sun_visor_bills():
    print(bright(red("TESTING sun_visor_bills with no items")))
    player = new_player()
    player.sun_visor_bills()
    print(bright(red("Testing sun_visor_bills with Flask of Fortunate Day")))
    player = new_player(items=['Flask of Fortunate Day'])
    player.sun_visor_bills()

def sunburn():
    print(bright(red("TESTING sunburn with no items")))
    player = new_player()
    player.sunburn()
    print(bright(red("Testing sunburn with Cheap Sunscreen")))
    player = new_player(items=['Cheap Sunscreen'])
    player.sunburn()
    print(bright(red("Testing sunburn with Premium Sunscreen")))
    player = new_player(items=['Premium Sunscreen'])
    player.sunburn()
    print(bright(red("Testing sunburn with Splint")))
    player = new_player(items=['Splint'])
    player.sunburn()
    print(bright(red("Testing sunburn with Sunglasses")))
    player = new_player(items=['Sunglasses'])
    player.sunburn()
    print(bright(red("Testing sunburn with Umbrella")))
    player = new_player(items=['Umbrella'])
    player.sunburn()

def terrible_weather():
    print(bright(red("TESTING terrible_weather with no items")))
    player = new_player()
    player.terrible_weather()
    print(bright(red("Testing terrible_weather with All-Weather Armor")))
    player = new_player(items=['All-Weather Armor'])
    player.terrible_weather()
    print(bright(red("Testing terrible_weather with Poncho")))
    player = new_player(items=['Poncho'])
    player.terrible_weather()
    print(bright(red("Testing terrible_weather with Storm Suit")))
    player = new_player(items=['Storm Suit'])
    player.terrible_weather()
    print(bright(red("Testing terrible_weather with Umbrella")))
    player = new_player(items=['Umbrella'])
    player.terrible_weather()

def threw_out_old_photo():
    print(bright(red("TESTING threw_out_old_photo with no items")))
    player = new_player()
    player.threw_out_old_photo()

def thunderstorm():
    print(bright(red("TESTING thunderstorm with no items")))
    player = new_player()
    player.thunderstorm()
    print(bright(red("Testing thunderstorm with All-Weather Armor")))
    player = new_player(items=['All-Weather Armor'])
    player.thunderstorm()
    print(bright(red("Testing thunderstorm with Plastic Poncho")))
    player = new_player(items=['Plastic Poncho'])
    player.thunderstorm()
    print(bright(red("Testing thunderstorm with Poncho")))
    player = new_player(items=['Poncho'])
    player.thunderstorm()
    print(bright(red("Testing thunderstorm with Storm Suit")))
    player = new_player(items=['Storm Suit'])
    player.thunderstorm()
    print(bright(red("Testing thunderstorm with Umbrella")))
    player = new_player(items=['Umbrella'])
    player.thunderstorm()

def turn_to_god():
    print(bright(red("TESTING turn_to_god with no items")))
    player = new_player()
    player.turn_to_god()

def weird_noise():
    print(bright(red("TESTING weird_noise with no items")))
    player = new_player()
    player.weird_noise()

def wrong_item_bug_spray_campfire():
    print(bright(red("TESTING wrong_item_bug_spray_campfire with no items")))
    player = new_player()
    player.wrong_item_bug_spray_campfire()
    print(bright(red("Testing wrong_item_bug_spray_campfire with Bug Spray")))
    player = new_player(items=['Bug Spray'])
    player.wrong_item_bug_spray_campfire()


"""story.events_day_wealth.py"""
def all_dreams_complete():
    print(bright(red("TESTING all_dreams_complete with no items")))
    player = new_player()
    player.all_dreams_complete()

def almost_there():
    print(bright(red("TESTING almost_there with no items")))
    player = new_player()
    player.almost_there()

def atm_theft_police():
    print(bright(red("TESTING atm_theft_police with no items")))
    player = new_player()
    player.atm_theft_police()

def booted_car_impound():
    print(bright(red("TESTING booted_car_impound with no items")))
    player = new_player()
    player.booted_car_impound()

def casino_comps():
    print(bright(red("TESTING casino_comps with no items")))
    player = new_player()
    player.casino_comps()

def casino_knows():
    print(bright(red("TESTING casino_knows with no items")))
    player = new_player()
    player.casino_knows()
    print(bright(red("Testing casino_knows with Dealer's Grudge")))
    player = new_player(items=["Dealer's Grudge"])
    player.casino_knows()
    print(bright(red("Testing casino_knows with Dealer's Mercy")))
    player = new_player(items=["Dealer's Mercy"])
    player.casino_knows()
    print(bright(red("Testing casino_knows with Dirty Old Hat")))
    player = new_player(items=['Dirty Old Hat'])
    player.casino_knows()
    print(bright(red("Testing casino_knows with Forged Documents")))
    player = new_player(items=['Forged Documents'])
    player.casino_knows()
    print(bright(red("Testing casino_knows with Golden Watch")))
    player = new_player(items=['Golden Watch'])
    player.casino_knows()
    print(bright(red("Testing casino_knows with Invisible Cloak")))
    player = new_player(items=['Invisible Cloak'])
    player.casino_knows()
    print(bright(red("Testing casino_knows with Low-Profile Outfit")))
    player = new_player(items=['Low-Profile Outfit'])
    player.casino_knows()
    print(bright(red("Testing casino_knows with Radio Jammer")))
    player = new_player(items=['Radio Jammer'])
    player.casino_knows()
    print(bright(red("Testing casino_knows with Sapphire Watch")))
    player = new_player(items=['Sapphire Watch'])
    player.casino_knows()
    print(bright(red("Testing casino_knows with Sneaky Peeky Goggles")))
    player = new_player(items=['Sneaky Peeky Goggles'])
    player.casino_knows()
    print(bright(red("Testing casino_knows with Sneaky Peeky Shades")))
    player = new_player(items=['Sneaky Peeky Shades'])
    player.casino_knows()
    print(bright(red("Testing casino_knows with Surveillance Suite")))
    player = new_player(items=['Surveillance Suite'])
    player.casino_knows()
    print(bright(red("Testing casino_knows with Tattered Cloak")))
    player = new_player(items=['Tattered Cloak'])
    player.casino_knows()
    print(bright(red("Testing casino_knows with Unwashed Hair")))
    player = new_player(items=['Unwashed Hair'])
    player.casino_knows()

def casino_owner_meeting():
    print(bright(red("TESTING casino_owner_meeting with no items")))
    player = new_player()
    player.casino_owner_meeting()
    print(bright(red("Testing casino_owner_meeting with Blackmail Letter")))
    player = new_player(items=['Blackmail Letter'])
    player.casino_owner_meeting()
    print(bright(red("Testing casino_owner_meeting with Evidence Kit")))
    player = new_player(items=['Evidence Kit'])
    player.casino_owner_meeting()

def charity_opportunity():
    print(bright(red("TESTING charity_opportunity with no items")))
    player = new_player()
    player.charity_opportunity()

def exactly_1111():
    print(bright(red("TESTING exactly_1111 with no items")))
    player = new_player()
    player.exactly_1111()
    print(bright(red("Testing exactly_1111 with Flask of Fortunate Day")))
    player = new_player(items=['Flask of Fortunate Day'])
    player.exactly_1111()

def exactly_250000():
    print(bright(red("TESTING exactly_250000 with no items")))
    player = new_player()
    player.exactly_250000()

def exactly_50000():
    print(bright(red("TESTING exactly_50000 with no items")))
    player = new_player()
    player.exactly_50000()
    print(bright(red("Testing exactly_50000 with Flask of Bonus Fortune")))
    player = new_player(items=['Flask of Bonus Fortune'])
    player.exactly_50000()

def exactly_777777():
    print(bright(red("TESTING exactly_777777 with no items")))
    player = new_player()
    player.exactly_777777()

def exactly_999999():
    print(bright(red("TESTING exactly_999999 with no items")))
    player = new_player()
    player.exactly_999999()

def expensive_taste():
    print(bright(red("TESTING expensive_taste with no items")))
    player = new_player()
    player.expensive_taste()

def final_dream():
    print(bright(red("TESTING final_dream with no items")))
    player = new_player()
    player.final_dream()

def final_interrogation():
    print(bright(red("TESTING final_interrogation with no items")))
    player = new_player()
    player.final_interrogation()

def high_roller_invitation():
    print(bright(red("TESTING high_roller_invitation with no items")))
    player = new_player()
    player.high_roller_invitation()
    print(bright(red("Testing high_roller_invitation with Kingpin Look")))
    player = new_player(items=['Kingpin Look'])
    player.high_roller_invitation()

def high_roller_room():
    print(bright(red("TESTING high_roller_room with no items")))
    player = new_player()
    player.high_roller_room()

def high_roller_room_visit():
    print(bright(red("TESTING high_roller_room_visit with no items")))
    player = new_player()
    player.high_roller_room_visit()
    print(bright(red("Testing high_roller_room_visit with Beach Bum Disguise")))
    player = new_player(items=['Beach Bum Disguise'])
    player.high_roller_room_visit()
    print(bright(red("Testing high_roller_room_visit with Casino VIP Card")))
    player = new_player(items=['Casino VIP Card'])
    player.high_roller_room_visit()
    print(bright(red("Testing high_roller_room_visit with Heirloom Set")))
    player = new_player(items=['Heirloom Set'])
    player.high_roller_room_visit()
    print(bright(red("Testing high_roller_room_visit with High Roller Keycard")))
    player = new_player(items=['High Roller Keycard'])
    player.high_roller_room_visit()
    print(bright(red("Testing high_roller_room_visit with Old Money Identity")))
    player = new_player(items=['Old Money Identity'])
    player.high_roller_room_visit()
    print(bright(red("Testing high_roller_room_visit with Storm Suit")))
    player = new_player(items=['Storm Suit'])
    player.high_roller_room_visit()
    print(bright(red("Testing high_roller_room_visit with VIP Invitation")))
    player = new_player(items=['VIP Invitation'])
    player.high_roller_room_visit()

def high_roller_whale():
    print(bright(red("TESTING high_roller_whale with no items")))
    player = new_player()
    player.high_roller_whale()
    print(bright(red("Testing high_roller_whale with Casino VIP Card")))
    player = new_player(items=['Casino VIP Card'])
    player.high_roller_whale()
    print(bright(red("Testing high_roller_whale with High Roller Keycard")))
    player = new_player(items=['High Roller Keycard'])
    player.high_roller_whale()
    print(bright(red("Testing high_roller_whale with VIP Invitation")))
    player = new_player(items=['VIP Invitation'])
    player.high_roller_whale()

def imposter_syndrome():
    print(bright(red("TESTING imposter_syndrome with no items")))
    player = new_player()
    player.imposter_syndrome()

def investment_opportunity():
    print(bright(red("TESTING investment_opportunity with no items")))
    player = new_player()
    player.investment_opportunity()
    print(bright(red("Testing investment_opportunity with All-Access Pass")))
    player = new_player(items=['All-Access Pass'])
    player.investment_opportunity()
    print(bright(red("Testing investment_opportunity with Blackmail Letter")))
    player = new_player(items=['Blackmail Letter'])
    player.investment_opportunity()
    print(bright(red("Testing investment_opportunity with Cheater's Insurance")))
    player = new_player(items=["Cheater's Insurance"])
    player.investment_opportunity()
    print(bright(red("Testing investment_opportunity with Enchanted Vintage")))
    player = new_player(items=['Enchanted Vintage'])
    player.investment_opportunity()
    print(bright(red("Testing investment_opportunity with Enchanting Silver Bar")))
    player = new_player(items=['Enchanting Silver Bar'])
    player.investment_opportunity()
    print(bright(red("Testing investment_opportunity with Evidence Kit")))
    player = new_player(items=['Evidence Kit'])
    player.investment_opportunity()
    print(bright(red("Testing investment_opportunity with Flask of Bonus Fortune")))
    player = new_player(items=['Flask of Bonus Fortune'])
    player.investment_opportunity()
    print(bright(red("Testing investment_opportunity with Gambler's Grimoire")))
    player = new_player(items=["Gambler's Grimoire"])
    player.investment_opportunity()
    print(bright(red("Testing investment_opportunity with Gentleman's Charm")))
    player = new_player(items=["Gentleman's Charm"])
    player.investment_opportunity()
    print(bright(red("Testing investment_opportunity with Ghost Protocol")))
    player = new_player(items=['Ghost Protocol'])
    player.investment_opportunity()
    print(bright(red("Testing investment_opportunity with Intelligence Dossier")))
    player = new_player(items=['Intelligence Dossier'])
    player.investment_opportunity()
    print(bright(red("Testing investment_opportunity with Old Money Identity")))
    player = new_player(items=['Old Money Identity'])
    player.investment_opportunity()
    print(bright(red("Testing investment_opportunity with Oracle's Tome")))
    player = new_player(items=["Oracle's Tome"])
    player.investment_opportunity()
    print(bright(red("Testing investment_opportunity with Phantom Rose")))
    player = new_player(items=['Phantom Rose'])
    player.investment_opportunity()
    print(bright(red("Testing investment_opportunity with Stink Bomb")))
    player = new_player(items=['Stink Bomb'])
    player.investment_opportunity()
    print(bright(red("Testing investment_opportunity with Voice Soother")))
    player = new_player(items=['Voice Soother'])
    player.investment_opportunity()

def investment_pitch():
    print(bright(red("TESTING investment_pitch with no items")))
    player = new_player()
    player.investment_pitch()

def last_stretch():
    print(bright(red("TESTING last_stretch with no items")))
    player = new_player()
    player.last_stretch()

def likely_death():
    print(bright(red("TESTING likely_death with no items")))
    player = new_player()
    player.likely_death()

def luxury_car_passes():
    print(bright(red("TESTING luxury_car_passes with no items")))
    player = new_player()
    player.luxury_car_passes()

def luxury_problems():
    print(bright(red("TESTING luxury_problems with no items")))
    player = new_player()
    player.luxury_problems()

def media_known_documentary():
    print(bright(red("TESTING media_known_documentary with no items")))
    player = new_player()
    player.media_known_documentary()

def media_known_harassed():
    print(bright(red("TESTING media_known_harassed with no items")))
    player = new_player()
    player.media_known_harassed()

def millionaire_fantasy():
    print(bright(red("TESTING millionaire_fantasy with no items")))
    player = new_player()
    player.millionaire_fantasy()

def millionaire_milestone():
    print(bright(red("TESTING millionaire_milestone with no items")))
    player = new_player()
    player.millionaire_milestone()

def money_counting_ritual():
    print(bright(red("TESTING money_counting_ritual with no items")))
    player = new_player()
    player.money_counting_ritual()

def nervous_habits():
    print(bright(red("TESTING nervous_habits with no items")))
    player = new_player()
    player.nervous_habits()

def news_van():
    print(bright(red("TESTING news_van with no items")))
    player = new_player()
    player.news_van()

def old_friend_recognition():
    print(bright(red("TESTING old_friend_recognition with no items")))
    player = new_player()
    player.old_friend_recognition()

def old_rival_encounter():
    print(bright(red("TESTING old_rival_encounter with no items")))
    player = new_player()
    player.old_rival_encounter()

def old_rival_returns():
    print(bright(red("TESTING old_rival_returns with no items")))
    player = new_player()
    player.old_rival_returns()

def paparazzi_mistake():
    print(bright(red("TESTING paparazzi_mistake with no items")))
    player = new_player()
    player.paparazzi_mistake()
    print(bright(red("Testing paparazzi_mistake with Flask of Fortunate Day")))
    player = new_player(items=['Flask of Fortunate Day'])
    player.paparazzi_mistake()

def people_watching():
    print(bright(red("TESTING people_watching with no items")))
    player = new_player()
    player.people_watching()

def reporters_found_you():
    print(bright(red("TESTING reporters_found_you with no items")))
    player = new_player()
    player.reporters_found_you()
    print(bright(red("Testing reporters_found_you with Dealer's Grudge")))
    player = new_player(items=["Dealer's Grudge"])
    player.reporters_found_you()
    print(bright(red("Testing reporters_found_you with Dealer's Mercy")))
    player = new_player(items=["Dealer's Mercy"])
    player.reporters_found_you()
    print(bright(red("Testing reporters_found_you with Dirty Old Hat")))
    player = new_player(items=['Dirty Old Hat'])
    player.reporters_found_you()
    print(bright(red("Testing reporters_found_you with Forged Documents")))
    player = new_player(items=['Forged Documents'])
    player.reporters_found_you()
    print(bright(red("Testing reporters_found_you with Invisible Cloak")))
    player = new_player(items=['Invisible Cloak'])
    player.reporters_found_you()
    print(bright(red("Testing reporters_found_you with Low-Profile Outfit")))
    player = new_player(items=['Low-Profile Outfit'])
    player.reporters_found_you()
    print(bright(red("Testing reporters_found_you with Tattered Cloak")))
    player = new_player(items=['Tattered Cloak'])
    player.reporters_found_you()
    print(bright(red("Testing reporters_found_you with Unwashed Hair")))
    player = new_player(items=['Unwashed Hair'])
    player.reporters_found_you()

def rich_persons_problems():
    print(bright(red("TESTING rich_persons_problems with no items")))
    player = new_player()
    player.rich_persons_problems()

def strange_visitors():
    print(bright(red("TESTING strange_visitors with no items")))
    player = new_player()
    player.strange_visitors()
    print(bright(red("Testing strange_visitors with Dealer's Grudge")))
    player = new_player(items=["Dealer's Grudge"])
    player.strange_visitors()
    print(bright(red("Testing strange_visitors with Dealer's Mercy")))
    player = new_player(items=["Dealer's Mercy"])
    player.strange_visitors()

def tax_man():
    print(bright(red("TESTING tax_man with no items")))
    player = new_player()
    player.tax_man()
    print(bright(red("Testing tax_man with Ghost Protocol")))
    player = new_player(items=['Ghost Protocol'])
    player.tax_man()
    print(bright(red("Testing tax_man with New Identity")))
    player = new_player(items=['New Identity'])
    player.tax_man()

def the_bodyguard_offer():
    print(bright(red("TESTING the_bodyguard_offer with no items")))
    player = new_player()
    player.the_bodyguard_offer()

def the_celebration():
    print(bright(red("TESTING the_celebration with no items")))
    player = new_player()
    player.the_celebration()

def the_final_temptation():
    print(bright(red("TESTING the_final_temptation with no items")))
    player = new_player()
    player.the_final_temptation()

def the_journalist():
    print(bright(red("TESTING the_journalist with no items")))
    player = new_player()
    player.the_journalist()

def the_offer():
    print(bright(red("TESTING the_offer with no items")))
    player = new_player()
    player.the_offer()

def the_offer_refused():
    print(bright(red("TESTING the_offer_refused with no items")))
    player = new_player()
    player.the_offer_refused()

def the_rival():
    print(bright(red("TESTING the_rival with no items")))
    player = new_player()
    player.the_rival()

def the_temptation():
    print(bright(red("TESTING the_temptation with no items")))
    player = new_player()
    player.the_temptation()

def the_veteran():
    print(bright(red("TESTING the_veteran with no items")))
    player = new_player()
    player.the_veteran()

def the_warning():
    print(bright(red("TESTING the_warning with no items")))
    player = new_player()
    player.the_warning()

def the_weight_of_wealth():
    print(bright(red("TESTING the_weight_of_wealth with no items")))
    player = new_player()
    player.the_weight_of_wealth()

def too_close_to_quit():
    print(bright(red("TESTING too_close_to_quit with no items")))
    player = new_player()
    player.too_close_to_quit()

def unpaid_ticket_consequence():
    print(bright(red("TESTING unpaid_ticket_consequence with no items")))
    player = new_player()
    player.unpaid_ticket_consequence()

def unpaid_tickets_boot():
    print(bright(red("TESTING unpaid_tickets_boot with no items")))
    player = new_player()
    player.unpaid_tickets_boot()

def victoria_returns():
    print(bright(red("TESTING victoria_returns with no items")))
    player = new_player()
    player.victoria_returns()

def wealth_anxiety():
    print(bright(red("TESTING wealth_anxiety with no items")))
    player = new_player()
    player.wealth_anxiety()
    print(bright(red("Testing wealth_anxiety with Delight Indicator")))
    player = new_player(items=['Delight Indicator'])
    player.wealth_anxiety()
    print(bright(red("Testing wealth_anxiety with Delight Manipulator")))
    player = new_player(items=['Delight Manipulator'])
    player.wealth_anxiety()

def wealth_paranoia():
    print(bright(red("TESTING wealth_paranoia with no items")))
    player = new_player()
    player.wealth_paranoia()

def wealthy_doubts():
    print(bright(red("TESTING wealthy_doubts with no items")))
    player = new_player()
    player.wealthy_doubts()


"""story.events_illness.py"""
def allergic_reaction_restaurant():
    print(bright(red("TESTING allergic_reaction_restaurant with no items")))
    player = new_player()
    player.allergic_reaction_restaurant()

def appendicitis_attack():
    print(bright(red("TESTING appendicitis_attack with no items")))
    player = new_player()
    player.appendicitis_attack()

def asbestos_exposure():
    print(bright(red("TESTING asbestos_exposure with no items")))
    player = new_player()
    player.asbestos_exposure()

def assault_aftermath():
    print(bright(red("TESTING assault_aftermath with no items")))
    player = new_player()
    player.assault_aftermath()

def asthma_attack():
    print(bright(red("TESTING asthma_attack with no items")))
    player = new_player()
    player.asthma_attack()

def bad_mushrooms():
    print(bright(red("TESTING bad_mushrooms with no items")))
    player = new_player()
    player.bad_mushrooms()

def bad_oysters():
    print(bright(red("TESTING bad_oysters with no items")))
    player = new_player()
    player.bad_oysters()

def bad_sushi():
    print(bright(red("TESTING bad_sushi with no items")))
    player = new_player()
    player.bad_sushi()

def bad_tattoo_infection():
    print(bright(red("TESTING bad_tattoo_infection with no items")))
    player = new_player()
    player.bad_tattoo_infection()

def bar_fight_aftermath():
    print(bright(red("TESTING bar_fight_aftermath with no items")))
    player = new_player()
    player.bar_fight_aftermath()

def bee_sting_allergy():
    print(bright(red("TESTING bee_sting_allergy with no items")))
    player = new_player()
    player.bee_sting_allergy()
    print(bright(red("Testing bee_sting_allergy with Flask of Anti-Venom")))
    player = new_player(items=['Flask of Anti-Venom'])
    player.bee_sting_allergy()

def blood_clot_in_leg():
    print(bright(red("TESTING blood_clot_in_leg with no items")))
    player = new_player()
    player.blood_clot_in_leg()

def blood_poisoning():
    print(bright(red("TESTING blood_poisoning with no items")))
    player = new_player()
    player.blood_poisoning()
    print(bright(red("Testing blood_poisoning with Flask of Anti-Virus")))
    player = new_player(items=['Flask of Anti-Virus'])
    player.blood_poisoning()

def botched_piercing():
    print(bright(red("TESTING botched_piercing with no items")))
    player = new_player()
    player.botched_piercing()

def botched_surgery():
    print(bright(red("TESTING botched_surgery with no items")))
    player = new_player()
    player.botched_surgery()
    print(bright(red("Testing botched_surgery with Forged Documents")))
    player = new_player(items=['Forged Documents'])
    player.botched_surgery()

def broken_ankle():
    print(bright(red("TESTING broken_ankle with no items")))
    player = new_player()
    player.broken_ankle()

def broken_collarbone():
    print(bright(red("TESTING broken_collarbone with no items")))
    player = new_player()
    player.broken_collarbone()

def broken_hand():
    print(bright(red("TESTING broken_hand with no items")))
    player = new_player()
    player.broken_hand()

def broken_nose():
    print(bright(red("TESTING broken_nose with no items")))
    player = new_player()
    player.broken_nose()

def broken_ribs_injury():
    print(bright(red("TESTING broken_ribs_injury with no items")))
    player = new_player()
    player.broken_ribs_injury()

def broken_wrist():
    print(bright(red("TESTING broken_wrist with no items")))
    player = new_player()
    player.broken_wrist()

def camping_tick_bite():
    print(bright(red("TESTING camping_tick_bite with no items")))
    player = new_player()
    player.camping_tick_bite()

def car_accident_minor():
    print(bright(red("TESTING car_accident_minor with no items")))
    player = new_player()
    player.car_accident_minor()
    print(bright(red("Testing car_accident_minor with Real Insurance")))
    player = new_player(items=['Real Insurance'])
    player.car_accident_minor()

def carnival_ride_accident():
    print(bright(red("TESTING carnival_ride_accident with no items")))
    player = new_player()
    player.carnival_ride_accident()

def caught_in_fire():
    print(bright(red("TESTING caught_in_fire with no items")))
    player = new_player()
    player.caught_in_fire()

def chemical_burn():
    print(bright(red("TESTING chemical_burn with no items")))
    player = new_player()
    player.chemical_burn()

def chemical_spill():
    print(bright(red("TESTING chemical_spill with no items")))
    player = new_player()
    player.chemical_spill()

def collapsed_lung():
    print(bright(red("TESTING collapsed_lung with no items")))
    player = new_player()
    player.collapsed_lung()

def coma_awakening():
    print(bright(red("TESTING coma_awakening with no items")))
    player = new_player()
    player.coma_awakening()

def concussion_injury():
    print(bright(red("TESTING concussion_injury with no items")))
    player = new_player()
    player.concussion_injury()

def construction_site_accident():
    print(bright(red("TESTING construction_site_accident with no items")))
    player = new_player()
    player.construction_site_accident()

def contract_bronchitis():
    print(bright(red("TESTING contract_bronchitis with no items")))
    player = new_player()
    player.contract_bronchitis()

def contract_cold():
    print(bright(red("TESTING contract_cold with no items")))
    player = new_player()
    player.contract_cold()
    print(bright(red("Testing contract_cold with Home Remedy")))
    player = new_player(items=['Home Remedy'])
    player.contract_cold()
    print(bright(red("Testing contract_cold with Voice Soother")))
    player = new_player(items=['Voice Soother'])
    player.contract_cold()

def contract_ear_infection():
    print(bright(red("TESTING contract_ear_infection with no items")))
    player = new_player()
    player.contract_ear_infection()

def contract_flu():
    print(bright(red("TESTING contract_flu with no items")))
    player = new_player()
    player.contract_flu()
    print(bright(red("Testing contract_flu with Flask of Anti-Virus")))
    player = new_player(items=['Flask of Anti-Virus'])
    player.contract_flu()

def contract_lyme_disease():
    print(bright(red("TESTING contract_lyme_disease with no items")))
    player = new_player()
    player.contract_lyme_disease()
    print(bright(red("Testing contract_lyme_disease with Flask of Anti-Venom")))
    player = new_player(items=['Flask of Anti-Venom'])
    player.contract_lyme_disease()

def contract_measles():
    print(bright(red("TESTING contract_measles with no items")))
    player = new_player()
    player.contract_measles()
    print(bright(red("Testing contract_measles with Flask of Anti-Virus")))
    player = new_player(items=['Flask of Anti-Virus'])
    player.contract_measles()

def contract_mono():
    print(bright(red("TESTING contract_mono with no items")))
    player = new_player()
    player.contract_mono()

def contract_pink_eye():
    print(bright(red("TESTING contract_pink_eye with no items")))
    player = new_player()
    player.contract_pink_eye()

def contract_pneumonia():
    print(bright(red("TESTING contract_pneumonia with no items")))
    player = new_player()
    player.contract_pneumonia()
    print(bright(red("Testing contract_pneumonia with First Aid Kit")))
    player = new_player(items=['First Aid Kit'])
    player.contract_pneumonia()
    print(bright(red("Testing contract_pneumonia with Health Indicator")))
    player = new_player(items=['Health Indicator'])
    player.contract_pneumonia()
    print(bright(red("Testing contract_pneumonia with Health Manipulator")))
    player = new_player(items=['Health Manipulator'])
    player.contract_pneumonia()
    print(bright(red("Testing contract_pneumonia with Hydration Station")))
    player = new_player(items=['Hydration Station'])
    player.contract_pneumonia()

def contract_rabies_scare():
    print(bright(red("TESTING contract_rabies_scare with no items")))
    player = new_player()
    player.contract_rabies_scare()

def contract_ringworm():
    print(bright(red("TESTING contract_ringworm with no items")))
    player = new_player()
    player.contract_ringworm()

def contract_scabies():
    print(bright(red("TESTING contract_scabies with no items")))
    player = new_player()
    player.contract_scabies()

def contract_shingles():
    print(bright(red("TESTING contract_shingles with no items")))
    player = new_player()
    player.contract_shingles()

def contract_sinus_infection():
    print(bright(red("TESTING contract_sinus_infection with no items")))
    player = new_player()
    player.contract_sinus_infection()

def contract_staph_infection():
    print(bright(red("TESTING contract_staph_infection with no items")))
    player = new_player()
    player.contract_staph_infection()

def contract_stomach_flu():
    print(bright(red("TESTING contract_stomach_flu with no items")))
    player = new_player()
    player.contract_stomach_flu()
    print(bright(red("Testing contract_stomach_flu with Antacid Brew")))
    player = new_player(items=['Antacid Brew'])
    player.contract_stomach_flu()
    print(bright(red("Testing contract_stomach_flu with Hydration Station")))
    player = new_player(items=['Hydration Station'])
    player.contract_stomach_flu()
    print(bright(red("Testing contract_stomach_flu with Water Purifier")))
    player = new_player(items=['Water Purifier'])
    player.contract_stomach_flu()

def contract_strep_throat():
    print(bright(red("TESTING contract_strep_throat with no items")))
    player = new_player()
    player.contract_strep_throat()

def contract_tetanus():
    print(bright(red("TESTING contract_tetanus with no items")))
    player = new_player()
    player.contract_tetanus()

def contract_uti():
    print(bright(red("TESTING contract_uti with no items")))
    player = new_player()
    player.contract_uti()

def covid_complications():
    print(bright(red("TESTING covid_complications with no items")))
    player = new_player()
    player.covid_complications()

def crush_injury():
    print(bright(red("TESTING crush_injury with no items")))
    player = new_player()
    player.crush_injury()

def daycare_plague():
    print(bright(red("TESTING daycare_plague with no items")))
    player = new_player()
    player.daycare_plague()

def deep_laceration():
    print(bright(red("TESTING deep_laceration with no items")))
    player = new_player()
    player.deep_laceration()

def dental_disaster():
    print(bright(red("TESTING dental_disaster with no items")))
    player = new_player()
    player.dental_disaster()

def detached_retina():
    print(bright(red("TESTING detached_retina with no items")))
    player = new_player()
    player.detached_retina()

def develop_diabetes_symptoms():
    print(bright(red("TESTING develop_diabetes_symptoms with no items")))
    player = new_player()
    player.develop_diabetes_symptoms()
    print(bright(red("Testing develop_diabetes_symptoms with Health Indicator")))
    player = new_player(items=['Health Indicator'])
    player.develop_diabetes_symptoms()
    print(bright(red("Testing develop_diabetes_symptoms with Health Manipulator")))
    player = new_player(items=['Health Manipulator'])
    player.develop_diabetes_symptoms()

def dirty_needle_stick():
    print(bright(red("TESTING dirty_needle_stick with no items")))
    player = new_player()
    player.dirty_needle_stick()

def dislocated_shoulder():
    print(bright(red("TESTING dislocated_shoulder with no items")))
    player = new_player()
    player.dislocated_shoulder()

def dog_attack_severe():
    print(bright(red("TESTING dog_attack_severe with no items")))
    player = new_player()
    player.dog_attack_severe()
    print(bright(red("Testing dog_attack_severe with Real Insurance")))
    player = new_player(items=['Real Insurance'])
    player.dog_attack_severe()

def drug_overdose_survival():
    print(bright(red("TESTING drug_overdose_survival with no items")))
    player = new_player()
    player.drug_overdose_survival()

def earthquake_injury():
    print(bright(red("TESTING earthquake_injury with no items")))
    player = new_player()
    player.earthquake_injury()

def electric_shock():
    print(bright(red("TESTING electric_shock with no items")))
    player = new_player()
    player.electric_shock()

def electrical_burn():
    print(bright(red("TESTING electrical_burn with no items")))
    player = new_player()
    player.electrical_burn()

def explosion_nearby():
    print(bright(red("TESTING explosion_nearby with no items")))
    player = new_player()
    player.explosion_nearby()

def fall_down_stairs():
    print(bright(red("TESTING fall_down_stairs with no items")))
    player = new_player()
    player.fall_down_stairs()

def food_truck_nightmare():
    print(bright(red("TESTING food_truck_nightmare with no items")))
    player = new_player()
    player.food_truck_nightmare()
    print(bright(red("Testing food_truck_nightmare with Antacid Brew")))
    player = new_player(items=['Antacid Brew'])
    player.food_truck_nightmare()

def frostbite():
    print(bright(red("TESTING frostbite with no items")))
    player = new_player()
    player.frostbite()

def frozen_outdoors():
    print(bright(red("TESTING frozen_outdoors with no items")))
    player = new_player()
    player.frozen_outdoors()

def gallbladder_attack():
    print(bright(red("TESTING gallbladder_attack with no items")))
    player = new_player()
    player.gallbladder_attack()

def gangrene_infection():
    print(bright(red("TESTING gangrene_infection with no items")))
    player = new_player()
    player.gangrene_infection()

def grease_fire():
    print(bright(red("TESTING grease_fire with no items")))
    player = new_player()
    player.grease_fire()

def gym_accident():
    print(bright(red("TESTING gym_accident with no items")))
    player = new_player()
    player.gym_accident()

def gym_collapse():
    print(bright(red("TESTING gym_collapse with no items")))
    player = new_player()
    player.gym_collapse()

def heat_exhaustion_collapse():
    print(bright(red("TESTING heat_exhaustion_collapse with no items")))
    player = new_player()
    player.heat_exhaustion_collapse()

def heat_stroke():
    print(bright(red("TESTING heat_stroke with no items")))
    player = new_player()
    player.heat_stroke()
    print(bright(red("Testing heat_stroke with All-Weather Armor")))
    player = new_player(items=['All-Weather Armor'])
    player.heat_stroke()
    print(bright(red("Testing heat_stroke with Cool Down Kit")))
    player = new_player(items=['Cool Down Kit'])
    player.heat_stroke()
    print(bright(red("Testing heat_stroke with Outdoor Shield")))
    player = new_player(items=['Outdoor Shield'])
    player.heat_stroke()

def herniated_disc():
    print(bright(red("TESTING herniated_disc with no items")))
    player = new_player()
    player.herniated_disc()

def high_blood_pressure_crisis():
    print(bright(red("TESTING high_blood_pressure_crisis with no items")))
    player = new_player()
    player.high_blood_pressure_crisis()
    print(bright(red("Testing high_blood_pressure_crisis with Health Indicator")))
    player = new_player(items=['Health Indicator'])
    player.high_blood_pressure_crisis()
    print(bright(red("Testing high_blood_pressure_crisis with Health Manipulator")))
    player = new_player(items=['Health Manipulator'])
    player.high_blood_pressure_crisis()

def hiking_disaster():
    print(bright(red("TESTING hiking_disaster with no items")))
    player = new_player()
    player.hiking_disaster()

def homeless_shelter_outbreak():
    print(bright(red("TESTING homeless_shelter_outbreak with no items")))
    player = new_player()
    player.homeless_shelter_outbreak()

def hypothermia():
    print(bright(red("TESTING hypothermia with no items")))
    player = new_player()
    player.hypothermia()
    print(bright(red("Testing hypothermia with Emergency Blanket")))
    player = new_player(items=['Emergency Blanket'])
    player.hypothermia()
    print(bright(red("Testing hypothermia with Fire Starter Kit")))
    player = new_player(items=['Fire Starter Kit'])
    player.hypothermia()
    print(bright(red("Testing hypothermia with Flask of No Bust")))
    player = new_player(items=['Flask of No Bust'])
    player.hypothermia()
    print(bright(red("Testing hypothermia with Survival Bivouac")))
    player = new_player(items=['Survival Bivouac'])
    player.hypothermia()

def insomnia_chronic():
    print(bright(red("TESTING insomnia_chronic with no items")))
    player = new_player()
    player.insomnia_chronic()

def jaw_fracture():
    print(bright(red("TESTING jaw_fracture with no items")))
    player = new_player()
    player.jaw_fracture()

def kidney_stones():
    print(bright(red("TESTING kidney_stones with no items")))
    player = new_player()
    player.kidney_stones()

def kitchen_accident():
    print(bright(red("TESTING kitchen_accident with no items")))
    player = new_player()
    player.kitchen_accident()

def lead_poisoning():
    print(bright(red("TESTING lead_poisoning with no items")))
    player = new_player()
    player.lead_poisoning()

def liver_laceration():
    print(bright(red("TESTING liver_laceration with no items")))
    player = new_player()
    player.liver_laceration()

def malnutrition():
    print(bright(red("TESTING malnutrition with no items")))
    player = new_player()
    player.malnutrition()

def mercury_poisoning():
    print(bright(red("TESTING mercury_poisoning with no items")))
    player = new_player()
    player.mercury_poisoning()

def migraine_severe():
    print(bright(red("TESTING migraine_severe with no items")))
    player = new_player()
    player.migraine_severe()
    print(bright(red("Testing migraine_severe with Health Indicator")))
    player = new_player(items=['Health Indicator'])
    player.migraine_severe()
    print(bright(red("Testing migraine_severe with Health Manipulator")))
    player = new_player(items=['Health Manipulator'])
    player.migraine_severe()
    print(bright(red("Testing migraine_severe with Mind Shield")))
    player = new_player(items=['Mind Shield'])
    player.migraine_severe()
    print(bright(red("Testing migraine_severe with Smelling Salts")))
    player = new_player(items=['Smelling Salts'])
    player.migraine_severe()

def mma_fight_aftermath():
    print(bright(red("TESTING mma_fight_aftermath with no items")))
    player = new_player()
    player.mma_fight_aftermath()

def mold_exposure():
    print(bright(red("TESTING mold_exposure with no items")))
    player = new_player()
    player.mold_exposure()

def motorcycle_crash():
    print(bright(red("TESTING motorcycle_crash with no items")))
    player = new_player()
    player.motorcycle_crash()

def muscle_tear():
    print(bright(red("TESTING muscle_tear with no items")))
    player = new_player()
    player.muscle_tear()

def nerve_damage():
    print(bright(red("TESTING nerve_damage with no items")))
    player = new_player()
    player.nerve_damage()

def orbital_fracture():
    print(bright(red("TESTING orbital_fracture with no items")))
    player = new_player()
    player.orbital_fracture()

def pancreatitis_attack():
    print(bright(red("TESTING pancreatitis_attack with no items")))
    player = new_player()
    player.pancreatitis_attack()

def pool_diving_accident():
    print(bright(red("TESTING pool_diving_accident with no items")))
    player = new_player()
    player.pool_diving_accident()

def prison_shiv_wound():
    print(bright(red("TESTING prison_shiv_wound with no items")))
    player = new_player()
    player.prison_shiv_wound()

def ptsd_flashback():
    print(bright(red("TESTING ptsd_flashback with no items")))
    player = new_player()
    player.ptsd_flashback()

def public_pool_infection():
    print(bright(red("TESTING public_pool_infection with no items")))
    player = new_player()
    player.public_pool_infection()

def puncture_wound():
    print(bright(red("TESTING puncture_wound with no items")))
    player = new_player()
    player.puncture_wound()

def random_illness():
    print(bright(red("TESTING random_illness with no items")))
    player = new_player()
    player.random_illness()
    print(bright(red("Testing random_illness with Flask of Anti-Venom")))
    player = new_player(items=['Flask of Anti-Venom'])
    player.random_illness()
    print(bright(red("Testing random_illness with Forged Documents")))
    player = new_player(items=['Forged Documents'])
    player.random_illness()
    print(bright(red("Testing random_illness with Guardian Angel")))
    player = new_player(items=['Guardian Angel'])
    player.random_illness()
    print(bright(red("Testing random_illness with New Identity")))
    player = new_player(items=['New Identity'])
    player.random_illness()

def events_illness__rat_bite():
    print(bright(red("TESTING story.events_illness:rat_bite with no items")))
    player = new_player()
    story.IllnessMixin.rat_bite(player)

def ruptured_eardrum():
    print(bright(red("TESTING ruptured_eardrum with no items")))
    player = new_player()
    player.ruptured_eardrum()

def ruptured_spleen():
    print(bright(red("TESTING ruptured_spleen with no items")))
    player = new_player()
    player.ruptured_spleen()

def second_degree_burns():
    print(bright(red("TESTING second_degree_burns with no items")))
    player = new_player()
    player.second_degree_burns()

def seizure_episode():
    print(bright(red("TESTING seizure_episode with no items")))
    player = new_player()
    player.seizure_episode()

def severe_allergic_reaction():
    print(bright(red("TESTING severe_allergic_reaction with no items")))
    player = new_player()
    player.severe_allergic_reaction()

def severe_anxiety_attack():
    print(bright(red("TESTING severe_anxiety_attack with no items")))
    player = new_player()
    player.severe_anxiety_attack()
    print(bright(red("Testing severe_anxiety_attack with Delight Indicator")))
    player = new_player(items=['Delight Indicator'])
    player.severe_anxiety_attack()
    print(bright(red("Testing severe_anxiety_attack with Delight Manipulator")))
    player = new_player(items=['Delight Manipulator'])
    player.severe_anxiety_attack()

def severe_burn_injury():
    print(bright(red("TESTING severe_burn_injury with no items")))
    player = new_player()
    player.severe_burn_injury()

def severe_dehydration():
    print(bright(red("TESTING severe_dehydration with no items")))
    player = new_player()
    player.severe_dehydration()

def severe_depression_episode():
    print(bright(red("TESTING severe_depression_episode with no items")))
    player = new_player()
    player.severe_depression_episode()

def skull_fracture():
    print(bright(red("TESTING skull_fracture with no items")))
    player = new_player()
    player.skull_fracture()

def sleep_deprivation_crisis():
    print(bright(red("TESTING sleep_deprivation_crisis with no items")))
    player = new_player()
    player.sleep_deprivation_crisis()

def slip_in_shower():
    print(bright(red("TESTING slip_in_shower with no items")))
    player = new_player()
    player.slip_in_shower()

def sports_injury():
    print(bright(red("TESTING sports_injury with no items")))
    player = new_player()
    player.sports_injury()

def stress_breakdown():
    print(bright(red("TESTING stress_breakdown with no items")))
    player = new_player()
    player.stress_breakdown()
    print(bright(red("Testing stress_breakdown with Health Indicator")))
    player = new_player(items=['Health Indicator'])
    player.stress_breakdown()
    print(bright(red("Testing stress_breakdown with Health Manipulator")))
    player = new_player(items=['Health Manipulator'])
    player.stress_breakdown()

def tendon_rupture():
    print(bright(red("TESTING tendon_rupture with no items")))
    player = new_player()
    player.tendon_rupture()

def tooth_abscess():
    print(bright(red("TESTING tooth_abscess with no items")))
    player = new_player()
    player.tooth_abscess()

def torn_acl():
    print(bright(red("TESTING torn_acl with no items")))
    player = new_player()
    player.torn_acl()

def trampoline_disaster():
    print(bright(red("TESTING trampoline_disaster with no items")))
    player = new_player()
    player.trampoline_disaster()

def trauma_flashback():
    print(bright(red("TESTING trauma_flashback with no items")))
    player = new_player()
    player.trauma_flashback()

def unclean_water():
    print(bright(red("TESTING unclean_water with no items")))
    player = new_player()
    player.unclean_water()
    print(bright(red("Testing unclean_water with Flask of Anti-Virus")))
    player = new_player(items=['Flask of Anti-Virus'])
    player.unclean_water()
    print(bright(red("Testing unclean_water with Hydration Station")))
    player = new_player(items=['Hydration Station'])
    player.unclean_water()
    print(bright(red("Testing unclean_water with Rain Collector")))
    player = new_player(items=['Rain Collector'])
    player.unclean_water()
    print(bright(red("Testing unclean_water with Water Purifier")))
    player = new_player(items=['Water Purifier'])
    player.unclean_water()

def vertigo_episode():
    print(bright(red("TESTING vertigo_episode with no items")))
    player = new_player()
    player.vertigo_episode()

def wasp_nest_encounter():
    print(bright(red("TESTING wasp_nest_encounter with no items")))
    player = new_player()
    player.wasp_nest_encounter()
    print(bright(red("Testing wasp_nest_encounter with Flask of Anti-Venom")))
    player = new_player(items=['Flask of Anti-Venom'])
    player.wasp_nest_encounter()

def weight_dropping():
    print(bright(red("TESTING weight_dropping with no items")))
    player = new_player()
    player.weight_dropping()

def whiplash_injury():
    print(bright(red("TESTING whiplash_injury with no items")))
    player = new_player()
    player.whiplash_injury()

def window_crash():
    print(bright(red("TESTING window_crash with no items")))
    player = new_player()
    player.window_crash()

def workplace_injury():
    print(bright(red("TESTING workplace_injury with no items")))
    player = new_player()
    player.workplace_injury()


"""story.events_night.py"""
def beach_dive():
    print(bright(red("TESTING beach_dive with no items")))
    player = new_player()
    player.beach_dive()
    print(bright(red("Testing beach_dive with Animal Whistle")))
    player = new_player(items=['Animal Whistle'])
    player.beach_dive()

def beach_stroll():
    print(bright(red("TESTING beach_stroll with no items")))
    player = new_player()
    player.beach_stroll()

def beach_swim():
    print(bright(red("TESTING beach_swim with no items")))
    player = new_player()
    player.beach_swim()
    print(bright(red("Testing beach_swim with Animal Whistle")))
    player = new_player(items=['Animal Whistle'])
    player.beach_swim()

def chase_the_fifth_rabbit():
    print(bright(red("TESTING chase_the_fifth_rabbit with no items")))
    player = new_player()
    player.chase_the_fifth_rabbit()

def chase_the_fourth_rabbit():
    print(bright(red("TESTING chase_the_fourth_rabbit with no items")))
    player = new_player()
    player.chase_the_fourth_rabbit()

def chase_the_rabbit():
    print(bright(red("TESTING chase_the_rabbit with no items")))
    player = new_player()
    player.chase_the_rabbit()

def chase_the_second_rabbit():
    print(bright(red("TESTING chase_the_second_rabbit with no items")))
    player = new_player()
    player.chase_the_second_rabbit()

def chase_the_third_rabbit():
    print(bright(red("TESTING chase_the_third_rabbit with no items")))
    player = new_player()
    player.chase_the_third_rabbit()
    print(bright(red("Testing chase_the_third_rabbit with Animal Whistle")))
    player = new_player(items=['Animal Whistle'])
    player.chase_the_third_rabbit()
    print(bright(red("Testing chase_the_third_rabbit with Carrot")))
    player = new_player(items=['Carrot'])
    player.chase_the_third_rabbit()

def city_park():
    print(bright(red("TESTING city_park with no items")))
    player = new_player()
    player.city_park()
    print(bright(red("Testing city_park with Animal Whistle")))
    player = new_player(items=['Animal Whistle'])
    player.city_park()

def city_streets():
    print(bright(red("TESTING city_streets with no items")))
    player = new_player()
    player.city_streets()
    print(bright(red("Testing city_streets with Animal Bait")))
    player = new_player(items=['Animal Bait'])
    player.city_streets()
    print(bright(red("Testing city_streets with Can of Tuna")))
    player = new_player(items=['Can of Tuna'])
    player.city_streets()
    print(bright(red("Testing city_streets with Spotlight")))
    player = new_player(items=['Spotlight'])
    player.city_streets()

def city_stroll():
    print(bright(red("TESTING city_stroll with no items")))
    player = new_player()
    player.city_stroll()
    print(bright(red("Testing city_stroll with Assassin's Kit")))
    player = new_player(items=["Assassin's Kit"])
    player.city_stroll()
    print(bright(red("Testing city_stroll with Bodyguard Bruno")))
    player = new_player(items=['Bodyguard Bruno'])
    player.city_stroll()
    print(bright(red("Testing city_stroll with Brass Knuckles")))
    player = new_player(items=['Brass Knuckles'])
    player.city_stroll()
    print(bright(red("Testing city_stroll with Distress Beacon")))
    player = new_player(items=['Distress Beacon'])
    player.city_stroll()
    print(bright(red("Testing city_stroll with Fortified Perimeter")))
    player = new_player(items=['Fortified Perimeter'])
    player.city_stroll()
    print(bright(red("Testing city_stroll with Guardian Angel")))
    player = new_player(items=['Guardian Angel'])
    player.city_stroll()
    print(bright(red("Testing city_stroll with Invisible Cloak")))
    player = new_player(items=['Invisible Cloak'])
    player.city_stroll()
    print(bright(red("Testing city_stroll with Lucky Coin")))
    player = new_player(items=['Lucky Coin'])
    player.city_stroll()
    print(bright(red("Testing city_stroll with Lucky Medallion")))
    player = new_player(items=['Lucky Medallion'])
    player.city_stroll()
    print(bright(red("Testing city_stroll with Pocket Knife")))
    player = new_player(items=['Pocket Knife'])
    player.city_stroll()
    print(bright(red("Testing city_stroll with Power Move Kit")))
    player = new_player(items=['Power Move Kit'])
    player.city_stroll()
    print(bright(red("Testing city_stroll with Road Warrior Armor")))
    player = new_player(items=['Road Warrior Armor'])
    player.city_stroll()
    print(bright(red("Testing city_stroll with Rolling Fortress")))
    player = new_player(items=['Rolling Fortress'])
    player.city_stroll()
    print(bright(red("Testing city_stroll with Surveillance Suite")))
    player = new_player(items=['Surveillance Suite'])
    player.city_stroll()
    print(bright(red("Testing city_stroll with Tattered Cloak")))
    player = new_player(items=['Tattered Cloak'])
    player.city_stroll()

def ditched_wallet():
    print(bright(red("TESTING ditched_wallet with no items")))
    player = new_player()
    player.ditched_wallet()
    print(bright(red("Testing ditched_wallet with Flask of Fortunate Night")))
    player = new_player(items=['Flask of Fortunate Night'])
    player.ditched_wallet()

def dream_of_winning():
    print(bright(red("TESTING dream_of_winning with no items")))
    player = new_player()
    player.dream_of_winning()

def giant_oyster_opening():
    print(bright(red("TESTING giant_oyster_opening with no items")))
    player = new_player()
    player.giant_oyster_opening()
    print(bright(red("Testing giant_oyster_opening with Giant Oyster")))
    player = new_player(items=['Giant Oyster'])
    player.giant_oyster_opening()

def insomnia_night():
    print(bright(red("TESTING insomnia_night with no items")))
    player = new_player()
    player.insomnia_night()
    print(bright(red("Testing insomnia_night with Deck of Cards")))
    player = new_player(items=['Deck of Cards'])
    player.insomnia_night()
    print(bright(red("Testing insomnia_night with Delight Indicator")))
    player = new_player(items=['Delight Indicator'])
    player.insomnia_night()
    print(bright(red("Testing insomnia_night with Delight Manipulator")))
    player = new_player(items=['Delight Manipulator'])
    player.insomnia_night()
    print(bright(red("Testing insomnia_night with Gambler's Chalice")))
    player = new_player(items=["Gambler's Chalice"])
    player.insomnia_night()
    print(bright(red("Testing insomnia_night with Overflowing Goblet")))
    player = new_player(items=['Overflowing Goblet'])
    player.insomnia_night()
    print(bright(red("Testing insomnia_night with Survival Bivouac")))
    player = new_player(items=['Survival Bivouac'])
    player.insomnia_night()

def late_night_radio():
    print(bright(red("TESTING late_night_radio with no items")))
    player = new_player()
    player.late_night_radio()

def midnight_snack_run():
    print(bright(red("TESTING midnight_snack_run with no items")))
    player = new_player()
    player.midnight_snack_run()
    print(bright(red("Testing midnight_snack_run with Road Flare Torch")))
    player = new_player(items=['Road Flare Torch'])
    player.midnight_snack_run()

def midnight_walk():
    print(bright(red("TESTING midnight_walk with no items")))
    player = new_player()
    player.midnight_walk()
    print(bright(red("Testing midnight_walk with Binoculars")))
    player = new_player(items=['Binoculars'])
    player.midnight_walk()
    print(bright(red("Testing midnight_walk with Flask of Fortunate Night")))
    player = new_player(items=['Flask of Fortunate Night'])
    player.midnight_walk()
    print(bright(red("Testing midnight_walk with Golden Compass")))
    player = new_player(items=['Golden Compass'])
    player.midnight_walk()
    print(bright(red("Testing midnight_walk with Headlamp")))
    player = new_player(items=['Headlamp'])
    player.midnight_walk()
    print(bright(red("Testing midnight_walk with Invisible Cloak")))
    player = new_player(items=['Invisible Cloak'])
    player.midnight_walk()
    print(bright(red("Testing midnight_walk with Quiet Bunny Slippers")))
    player = new_player(items=['Quiet Bunny Slippers'])
    player.midnight_walk()
    print(bright(red("Testing midnight_walk with Quiet Sneakers")))
    player = new_player(items=['Quiet Sneakers'])
    player.midnight_walk()
    print(bright(red("Testing midnight_walk with Rusty Compass")))
    player = new_player(items=['Rusty Compass'])
    player.midnight_walk()
    print(bright(red("Testing midnight_walk with Tattered Cloak")))
    player = new_player(items=['Tattered Cloak'])
    player.midnight_walk()

def mysterious_lights():
    print(bright(red("TESTING mysterious_lights with no items")))
    player = new_player()
    player.mysterious_lights()
    print(bright(red("Testing mysterious_lights with Rain Collector")))
    player = new_player(items=['Rain Collector'])
    player.mysterious_lights()
    print(bright(red("Testing mysterious_lights with Worry Stone")))
    player = new_player(items=['Worry Stone'])
    player.mysterious_lights()

def nice_dream():
    print(bright(red("TESTING nice_dream with no items")))
    player = new_player()
    player.nice_dream()
    print(bright(red("Testing nice_dream with Marvin's Monocle")))
    player = new_player(items=["Marvin's Monocle"])
    player.nice_dream()
    print(bright(red("Testing nice_dream with Mirror of Duality")))
    player = new_player(items=['Mirror of Duality'])
    player.nice_dream()
    print(bright(red("Testing nice_dream with Twin's Locket")))
    player = new_player(items=["Twin's Locket"])
    player.nice_dream()

def nightmare():
    print(bright(red("TESTING nightmare with no items")))
    player = new_player()
    player.nightmare()
    print(bright(red("Testing nightmare with Binding Portrait")))
    player = new_player(items=['Binding Portrait'])
    player.nightmare()
    print(bright(red("Testing nightmare with Devil's Deck")))
    player = new_player(items=["Devil's Deck"])
    player.nightmare()
    print(bright(red("Testing nightmare with Dream Catcher")))
    player = new_player(items=['Dream Catcher'])
    player.nightmare()
    print(bright(red("Testing nightmare with Lucid Dreaming Kit")))
    player = new_player(items=['Lucid Dreaming Kit'])
    player.nightmare()
    print(bright(red("Testing nightmare with Mind Shield")))
    player = new_player(items=['Mind Shield'])
    player.nightmare()
    print(bright(red("Testing nightmare with Necronomicon")))
    player = new_player(items=['Necronomicon'])
    player.nightmare()
    print(bright(red("Testing nightmare with Third Eye")))
    player = new_player(items=['Third Eye'])
    player.nightmare()

def nightmare_of_losing():
    print(bright(red("TESTING nightmare_of_losing with no items")))
    player = new_player()
    player.nightmare_of_losing()
    print(bright(red("Testing nightmare_of_losing with Dream Catcher")))
    player = new_player(items=['Dream Catcher'])
    player.nightmare_of_losing()
    print(bright(red("Testing nightmare_of_losing with Mind Shield")))
    player = new_player(items=['Mind Shield'])
    player.nightmare_of_losing()
    print(bright(red("Testing nightmare_of_losing with Third Eye")))
    player = new_player(items=['Third Eye'])
    player.nightmare_of_losing()
    print(bright(red("Testing nightmare_of_losing with Worry Stone")))
    player = new_player(items=['Worry Stone'])
    player.nightmare_of_losing()

def peaceful_night():
    print(bright(red("TESTING peaceful_night with no items")))
    player = new_player()
    player.peaceful_night()
    print(bright(red("Testing peaceful_night with Fire Starter Kit")))
    player = new_player(items=['Fire Starter Kit'])
    player.peaceful_night()
    print(bright(red("Testing peaceful_night with Fortune Cards")))
    player = new_player(items=['Fortune Cards'])
    player.peaceful_night()
    print(bright(red("Testing peaceful_night with Lucid Dreaming Kit")))
    player = new_player(items=['Lucid Dreaming Kit'])
    player.peaceful_night()
    print(bright(red("Testing peaceful_night with Nomad's Camp")))
    player = new_player(items=["Nomad's Camp"])
    player.peaceful_night()
    print(bright(red("Testing peaceful_night with Silver Flask")))
    player = new_player(items=['Silver Flask'])
    player.peaceful_night()
    print(bright(red("Testing peaceful_night with Sneaky Peeky Goggles")))
    player = new_player(items=['Sneaky Peeky Goggles'])
    player.peaceful_night()
    print(bright(red("Testing peaceful_night with Sneaky Peeky Shades")))
    player = new_player(items=['Sneaky Peeky Shades'])
    player.peaceful_night()
    print(bright(red("Testing peaceful_night with Survival Bivouac")))
    player = new_player(items=['Survival Bivouac'])
    player.peaceful_night()
    print(bright(red("Testing peaceful_night with Vintage Wine")))
    player = new_player(items=['Vintage Wine'])
    player.peaceful_night()

def police_checkpoint():
    print(bright(red("TESTING police_checkpoint with no items")))
    player = new_player()
    player.police_checkpoint()
    print(bright(red("Testing police_checkpoint with Golden Compass")))
    player = new_player(items=['Golden Compass'])
    player.police_checkpoint()
    print(bright(red("Testing police_checkpoint with Rusty Compass")))
    player = new_player(items=['Rusty Compass'])
    player.police_checkpoint()

def raccoon_invasion():
    print(bright(red("TESTING raccoon_invasion with no items")))
    player = new_player()
    player.raccoon_invasion()
    print(bright(red("Testing raccoon_invasion with Improvised Trap")))
    player = new_player(items=['Improvised Trap'])
    player.raccoon_invasion()
    print(bright(red("Testing raccoon_invasion with Pest Control")))
    player = new_player(items=['Pest Control'])
    player.raccoon_invasion()
    print(bright(red("Testing raccoon_invasion with Slingshot")))
    player = new_player(items=['Slingshot'])
    player.raccoon_invasion()
    print(bright(red("Testing raccoon_invasion with Snare Trap")))
    player = new_player(items=['Snare Trap'])
    player.raccoon_invasion()

def satellite_falling():
    print(bright(red("TESTING satellite_falling with no items")))
    player = new_player()
    player.satellite_falling()
    print(bright(red("Testing satellite_falling with Fire Launcher")))
    player = new_player(items=['Fire Launcher'])
    player.satellite_falling()

def stargazing():
    print(bright(red("TESTING stargazing with no items")))
    player = new_player()
    player.stargazing()
    print(bright(red("Testing stargazing with Binoculars")))
    player = new_player(items=['Binoculars'])
    player.stargazing()
    print(bright(red("Testing stargazing with Flask of Fortunate Night")))
    player = new_player(items=['Flask of Fortunate Night'])
    player.stargazing()
    print(bright(red("Testing stargazing with Lucky Charm Bracelet")))
    player = new_player(items=['Lucky Charm Bracelet'])
    player.stargazing()
    print(bright(red("Testing stargazing with Lucky Coin")))
    player = new_player(items=['Lucky Coin'])
    player.stargazing()
    print(bright(red("Testing stargazing with Lucky Medallion")))
    player = new_player(items=['Lucky Medallion'])
    player.stargazing()
    print(bright(red("Testing stargazing with Moon Shard")))
    player = new_player(items=['Moon Shard'])
    player.stargazing()
    print(bright(red("Testing stargazing with Night Scope")))
    player = new_player(items=['Night Scope'])
    player.stargazing()
    print(bright(red("Testing stargazing with Spotlight")))
    player = new_player(items=['Spotlight'])
    player.stargazing()

def stray_cat_returns():
    print(bright(red("TESTING stray_cat_returns with no items")))
    player = new_player()
    player.stray_cat_returns()

def swamp_stroll():
    print(bright(red("TESTING swamp_stroll with no items")))
    player = new_player()
    player.swamp_stroll()
    print(bright(red("Testing swamp_stroll with Animal Whistle")))
    player = new_player(items=['Animal Whistle'])
    player.swamp_stroll()
    print(bright(red("Testing swamp_stroll with Signal Mirror")))
    player = new_player(items=['Signal Mirror'])
    player.swamp_stroll()

def swamp_swim():
    print(bright(red("TESTING swamp_swim with no items")))
    player = new_player()
    player.swamp_swim()
    print(bright(red("Testing swamp_swim with Animal Whistle")))
    player = new_player(items=['Animal Whistle'])
    player.swamp_swim()
    print(bright(red("Testing swamp_swim with Gator Tooth Necklace")))
    player = new_player(items=['Gator Tooth Necklace'])
    player.swamp_swim()

def swamp_wade():
    print(bright(red("TESTING swamp_wade with no items")))
    player = new_player()
    player.swamp_wade()
    print(bright(red("Testing swamp_wade with Road Flare Torch")))
    player = new_player(items=['Road Flare Torch'])
    player.swamp_wade()
    print(bright(red("Testing swamp_wade with Scrap Armor")))
    player = new_player(items=['Scrap Armor'])
    player.swamp_wade()
    print(bright(red("Testing swamp_wade with Storm Suit")))
    player = new_player(items=['Storm Suit'])
    player.swamp_wade()

def went_jogging():
    print(bright(red("TESTING went_jogging with no items")))
    player = new_player()
    player.went_jogging()
    print(bright(red("Testing went_jogging with Flask of Fortunate Night")))
    player = new_player(items=['Flask of Fortunate Night'])
    player.went_jogging()
    print(bright(red("Testing went_jogging with Wound Salve")))
    player = new_player(items=['Wound Salve'])
    player.went_jogging()

def whats_my_favorite_animal():
    print(bright(red("TESTING whats_my_favorite_animal with no items")))
    player = new_player()
    player.whats_my_favorite_animal()

def whats_my_favorite_color():
    print(bright(red("TESTING whats_my_favorite_color with no items")))
    player = new_player()
    player.whats_my_favorite_color()

def woodlands_field():
    print(bright(red("TESTING woodlands_field with no items")))
    player = new_player()
    player.woodlands_field()

def woodlands_path():
    print(bright(red("TESTING woodlands_path with no items")))
    player = new_player()
    player.woodlands_path()
    print(bright(red("Testing woodlands_path with Animal Whistle")))
    player = new_player(items=['Animal Whistle'])
    player.woodlands_path()
    print(bright(red("Testing woodlands_path with Headlamp")))
    player = new_player(items=['Headlamp'])
    player.woodlands_path()
    print(bright(red("Testing woodlands_path with Smoke Flare")))
    player = new_player(items=['Smoke Flare'])
    player.woodlands_path()
    print(bright(red("Testing woodlands_path with Spotlight")))
    player = new_player(items=['Spotlight'])
    player.woodlands_path()

def woodlands_river():
    print(bright(red("TESTING woodlands_river with no items")))
    player = new_player()
    player.woodlands_river()
    print(bright(red("Testing woodlands_river with Animal Whistle")))
    player = new_player(items=['Animal Whistle'])
    player.woodlands_river()
    print(bright(red("Testing woodlands_river with Car Alarm Rigging")))
    player = new_player(items=['Car Alarm Rigging'])
    player.woodlands_river()
    print(bright(red("Testing woodlands_river with Fishing Rod")))
    player = new_player(items=['Fishing Rod'])
    player.woodlands_river()
    print(bright(red("Testing woodlands_river with Map")))
    player = new_player(items=['Map'])
    player.woodlands_river()
    print(bright(red("Testing woodlands_river with Quiet Bunny Slippers")))
    player = new_player(items=['Quiet Bunny Slippers'])
    player.woodlands_river()
    print(bright(red("Testing woodlands_river with Quiet Sneakers")))
    player = new_player(items=['Quiet Sneakers'])
    player.woodlands_river()
    print(bright(red("Testing woodlands_river with Scrap Armor")))
    player = new_player(items=['Scrap Armor'])
    player.woodlands_river()


"""story.events_car.py"""
def abs_light_on():
    print(bright(red("TESTING abs_light_on with no items")))
    player = new_player()
    player.abs_light_on()

def alternator_failing():
    print(bright(red("TESTING alternator_failing with no items")))
    player = new_player()
    player.alternator_failing()
    print(bright(red("Testing alternator_failing with Power Grid")))
    player = new_player(items=['Power Grid'])
    player.alternator_failing()

def bald_tires_hydroplane():
    print(bright(red("TESTING bald_tires_hydroplane with no items")))
    player = new_player()
    player.bald_tires_hydroplane()

def bald_tires_noticed():
    print(bright(red("TESTING bald_tires_noticed with no items")))
    player = new_player()
    player.bald_tires_noticed()

def battery_acid_leak():
    print(bright(red("TESTING battery_acid_leak with no items")))
    player = new_player()
    player.battery_acid_leak()

def brake_fluid_leak():
    print(bright(red("TESTING brake_fluid_leak with no items")))
    player = new_player()
    player.brake_fluid_leak()
    print(bright(red("Testing brake_fluid_leak with Brake Fluid")))
    player = new_player(items=['Brake Fluid'])
    player.brake_fluid_leak()

def brakes_squealing():
    print(bright(red("TESTING brakes_squealing with no items")))
    player = new_player()
    player.brakes_squealing()
    print(bright(red("Testing brakes_squealing with Brake Pads")))
    player = new_player(items=['Brake Pads'])
    player.brakes_squealing()

def broken_ball_joint():
    print(bright(red("TESTING broken_ball_joint with no items")))
    player = new_player()
    player.broken_ball_joint()

def broken_ball_joint_breaks():
    print(bright(red("TESTING broken_ball_joint_breaks with no items")))
    player = new_player()
    player.broken_ball_joint_breaks()

def car_alarm_malfunction():
    print(bright(red("TESTING car_alarm_malfunction with no items")))
    player = new_player()
    player.car_alarm_malfunction()
    print(bright(red("Testing car_alarm_malfunction with EMP Device")))
    player = new_player(items=['EMP Device'])
    player.car_alarm_malfunction()
    print(bright(red("Testing car_alarm_malfunction with Tool Kit")))
    player = new_player(items=['Tool Kit'])
    player.car_alarm_malfunction()

def car_wont_go_in_reverse():
    print(bright(red("TESTING car_wont_go_in_reverse with no items")))
    player = new_player()
    player.car_wont_go_in_reverse()

def catalytic_converter_stolen():
    print(bright(red("TESTING catalytic_converter_stolen with no items")))
    player = new_player()
    player.catalytic_converter_stolen()
    print(bright(red("Testing catalytic_converter_stolen with Fortified Perimeter")))
    player = new_player(items=['Fortified Perimeter'])
    player.catalytic_converter_stolen()
    print(bright(red("Testing catalytic_converter_stolen with Rolling Fortress")))
    player = new_player(items=['Rolling Fortress'])
    player.catalytic_converter_stolen()
    print(bright(red("Testing catalytic_converter_stolen with Security Bypass")))
    player = new_player(items=['Security Bypass'])
    player.catalytic_converter_stolen()

def check_engine_light_on():
    print(bright(red("TESTING check_engine_light_on with no items")))
    player = new_player()
    player.check_engine_light_on()
    print(bright(red("Testing check_engine_light_on with Fortune Cards")))
    player = new_player(items=['Fortune Cards'])
    player.check_engine_light_on()
    print(bright(red("Testing check_engine_light_on with OBD Scanner")))
    player = new_player(items=['OBD Scanner'])
    player.check_engine_light_on()

def clogged_fuel_filter():
    print(bright(red("TESTING clogged_fuel_filter with no items")))
    player = new_player()
    player.clogged_fuel_filter()
    print(bright(red("Testing clogged_fuel_filter with Fuel Filter")))
    player = new_player(items=['Fuel Filter'])
    player.clogged_fuel_filter()

def corroded_battery_terminals():
    print(bright(red("TESTING corroded_battery_terminals with no items")))
    player = new_player()
    player.corroded_battery_terminals()
    print(bright(red("Testing corroded_battery_terminals with Baking Soda")))
    player = new_player(items=['Baking Soda'])
    player.corroded_battery_terminals()
    print(bright(red("Testing corroded_battery_terminals with Battery Terminal Cleaner")))
    player = new_player(items=['Battery Terminal Cleaner'])
    player.corroded_battery_terminals()

def dead_battery_afternoon():
    print(bright(red("TESTING dead_battery_afternoon with no items")))
    player = new_player()
    player.dead_battery_afternoon()
    print(bright(red("Testing dead_battery_afternoon with Jumper Cables")))
    player = new_player(items=['Jumper Cables'])
    player.dead_battery_afternoon()
    print(bright(red("Testing dead_battery_afternoon with Portable Battery Charger")))
    player = new_player(items=['Portable Battery Charger'])
    player.dead_battery_afternoon()
    print(bright(red("Testing dead_battery_afternoon with Power Grid")))
    player = new_player(items=['Power Grid'])
    player.dead_battery_afternoon()

def engine_knock_worsens():
    print(bright(red("TESTING engine_knock_worsens with no items")))
    player = new_player()
    player.engine_knock_worsens()

def engine_oil_empty():
    print(bright(red("TESTING engine_oil_empty with no items")))
    player = new_player()
    player.engine_oil_empty()
    print(bright(red("Testing engine_oil_empty with Motor Oil")))
    player = new_player(items=['Motor Oil'])
    player.engine_oil_empty()

def engine_overheating():
    print(bright(red("TESTING engine_overheating with no items")))
    player = new_player()
    player.engine_overheating()
    print(bright(red("Testing engine_overheating with All-Weather Armor")))
    player = new_player(items=['All-Weather Armor'])
    player.engine_overheating()
    print(bright(red("Testing engine_overheating with Antifreeze")))
    player = new_player(items=['Antifreeze'])
    player.engine_overheating()
    print(bright(red("Testing engine_overheating with Cool Down Kit")))
    player = new_player(items=['Cool Down Kit'])
    player.engine_overheating()
    print(bright(red("Testing engine_overheating with Coolant")))
    player = new_player(items=['Coolant'])
    player.engine_overheating()
    print(bright(red("Testing engine_overheating with Gambler's Grimoire")))
    player = new_player(items=["Gambler's Grimoire"])
    player.engine_overheating()
    print(bright(red("Testing engine_overheating with Immortal Vehicle")))
    player = new_player(items=['Immortal Vehicle'])
    player.engine_overheating()
    print(bright(red("Testing engine_overheating with Oracle's Tome")))
    player = new_player(items=["Oracle's Tome"])
    player.engine_overheating()
    print(bright(red("Testing engine_overheating with Roadside Shield")))
    player = new_player(items=['Roadside Shield'])
    player.engine_overheating()
    print(bright(red("Testing engine_overheating with War Wagon")))
    player = new_player(items=['War Wagon'])
    player.engine_overheating()
    print(bright(red("Testing engine_overheating with Water Bottles")))
    player = new_player(items=['Water Bottles'])
    player.engine_overheating()

def engine_wont_turn_over():
    print(bright(red("TESTING engine_wont_turn_over with no items")))
    player = new_player()
    player.engine_wont_turn_over()
    print(bright(red("Testing engine_wont_turn_over with Mobile Workshop")))
    player = new_player(items=['Mobile Workshop'])
    player.engine_wont_turn_over()
    print(bright(red("Testing engine_wont_turn_over with Spare Spark Plugs")))
    player = new_player(items=['Spare Spark Plugs'])
    player.engine_wont_turn_over()
    print(bright(red("Testing engine_wont_turn_over with Tool Kit")))
    player = new_player(items=['Tool Kit'])
    player.engine_wont_turn_over()

def exhaust_leak_loud():
    print(bright(red("TESTING exhaust_leak_loud with no items")))
    player = new_player()
    player.exhaust_leak_loud()
    print(bright(red("Testing exhaust_leak_loud with Exhaust Tape")))
    player = new_player(items=['Exhaust Tape'])
    player.exhaust_leak_loud()

def failing_fuel_pump_dies():
    print(bright(red("TESTING failing_fuel_pump_dies with no items")))
    player = new_player()
    player.failing_fuel_pump_dies()

def failing_starter_dies():
    print(bright(red("TESTING failing_starter_dies with no items")))
    player = new_player()
    player.failing_starter_dies()

def flooded_engine():
    print(bright(red("TESTING flooded_engine with no items")))
    player = new_player()
    player.flooded_engine()

def frozen_door_locks():
    print(bright(red("TESTING frozen_door_locks with no items")))
    player = new_player()
    player.frozen_door_locks()
    print(bright(red("Testing frozen_door_locks with Lighter")))
    player = new_player(items=['Lighter'])
    player.frozen_door_locks()
    print(bright(red("Testing frozen_door_locks with Lock De-Icer")))
    player = new_player(items=['Lock De-Icer'])
    player.frozen_door_locks()

def frozen_fuel_line():
    print(bright(red("TESTING frozen_fuel_line with no items")))
    player = new_player()
    player.frozen_fuel_line()
    print(bright(red("Testing frozen_fuel_line with Fuel Line Antifreeze")))
    player = new_player(items=['Fuel Line Antifreeze'])
    player.frozen_fuel_line()

def fuel_pump_whining():
    print(bright(red("TESTING fuel_pump_whining with no items")))
    player = new_player()
    player.fuel_pump_whining()

def fuse_blown():
    print(bright(red("TESTING fuse_blown with no items")))
    player = new_player()
    player.fuse_blown()
    print(bright(red("Testing fuse_blown with Spare Fuses")))
    player = new_player(items=['Spare Fuses'])
    player.fuse_blown()

def gas_pedal_sticking():
    print(bright(red("TESTING gas_pedal_sticking with no items")))
    player = new_player()
    player.gas_pedal_sticking()
    print(bright(red("Testing gas_pedal_sticking with WD-40")))
    player = new_player(items=['WD-40'])
    player.gas_pedal_sticking()

def hail_damage():
    print(bright(red("TESTING hail_damage with no items")))
    player = new_player()
    player.hail_damage()

def headlights_burned_out():
    print(bright(red("TESTING headlights_burned_out with no items")))
    player = new_player()
    player.headlights_burned_out()
    print(bright(red("Testing headlights_burned_out with Spare Headlight Bulbs")))
    player = new_player(items=['Spare Headlight Bulbs'])
    player.headlights_burned_out()

def key_wont_turn():
    print(bright(red("TESTING key_wont_turn with no items")))
    player = new_player()
    player.key_wont_turn()
    print(bright(red("Testing key_wont_turn with WD-40")))
    player = new_player(items=['WD-40'])
    player.key_wont_turn()

def leaking_battery_worsens():
    print(bright(red("TESTING leaking_battery_worsens with no items")))
    player = new_player()
    player.leaking_battery_worsens()

def mystery_breakdown():
    print(bright(red("TESTING mystery_breakdown with no items")))
    player = new_player()
    player.mystery_breakdown()
    print(bright(red("Testing mystery_breakdown with Auto Mechanic")))
    player = new_player(items=['Auto Mechanic'])
    player.mystery_breakdown()
    print(bright(red("Testing mystery_breakdown with Immortal Vehicle")))
    player = new_player(items=['Immortal Vehicle'])
    player.mystery_breakdown()
    print(bright(red("Testing mystery_breakdown with Vermin Bomb")))
    player = new_player(items=['Vermin Bomb'])
    player.mystery_breakdown()
    print(bright(red("Testing mystery_breakdown with War Wagon")))
    player = new_player(items=['War Wagon'])
    player.mystery_breakdown()

def nail_in_tire():
    print(bright(red("TESTING nail_in_tire with no items")))
    player = new_player()
    player.nail_in_tire()
    print(bright(red("Testing nail_in_tire with Spare Tire")))
    player = new_player(items=['Spare Tire'])
    player.nail_in_tire()
    print(bright(red("Testing nail_in_tire with Tire Patch Kit")))
    player = new_player(items=['Tire Patch Kit'])
    player.nail_in_tire()

def nail_in_tire_blows():
    print(bright(red("TESTING nail_in_tire_blows with no items")))
    player = new_player()
    player.nail_in_tire_blows()
    print(bright(red("Testing nail_in_tire_blows with Spare Tire")))
    player = new_player(items=['Spare Tire'])
    player.nail_in_tire_blows()

def oil_leak_spotted():
    print(bright(red("TESTING oil_leak_spotted with no items")))
    player = new_player()
    player.oil_leak_spotted()
    print(bright(red("Testing oil_leak_spotted with Oil Stop Leak")))
    player = new_player(items=['Oil Stop Leak'])
    player.oil_leak_spotted()

def parking_brake_stuck():
    print(bright(red("TESTING parking_brake_stuck with no items")))
    player = new_player()
    player.parking_brake_stuck()
    print(bright(red("Testing parking_brake_stuck with Tool Kit")))
    player = new_player(items=['Tool Kit'])
    player.parking_brake_stuck()

def power_steering_failure():
    print(bright(red("TESTING power_steering_failure with no items")))
    player = new_player()
    player.power_steering_failure()
    print(bright(red("Testing power_steering_failure with Power Steering Fluid")))
    player = new_player(items=['Power Steering Fluid'])
    player.power_steering_failure()

def radiator_leak():
    print(bright(red("TESTING radiator_leak with no items")))
    player = new_player()
    player.radiator_leak()
    print(bright(red("Testing radiator_leak with Radiator Stop Leak")))
    player = new_player(items=['Radiator Stop Leak'])
    player.radiator_leak()

def ran_out_of_gas():
    print(bright(red("TESTING ran_out_of_gas with no items")))
    player = new_player()
    player.ran_out_of_gas()
    print(bright(red("Testing ran_out_of_gas with Gas Can")))
    player = new_player(items=['Gas Can'])
    player.ran_out_of_gas()
    print(bright(red("Testing ran_out_of_gas with SOS Kit")))
    player = new_player(items=['SOS Kit'])
    player.ran_out_of_gas()

def random_car_trouble():
    print(bright(red("TESTING random_car_trouble with no items")))
    player = new_player()
    player.random_car_trouble()
    print(bright(red("Testing random_car_trouble with Auto Mechanic")))
    player = new_player(items=['Auto Mechanic'])
    player.random_car_trouble()
    print(bright(red("Testing random_car_trouble with Immortal Vehicle")))
    player = new_player(items=['Immortal Vehicle'])
    player.random_car_trouble()
    print(bright(red("Testing random_car_trouble with Roadside Shield")))
    player = new_player(items=['Roadside Shield'])
    player.random_car_trouble()
    print(bright(red("Testing random_car_trouble with War Wagon")))
    player = new_player(items=['War Wagon'])
    player.random_car_trouble()

def slow_tire_leak():
    print(bright(red("TESTING slow_tire_leak with no items")))
    player = new_player()
    player.slow_tire_leak()
    print(bright(red("Testing slow_tire_leak with Fix-a-Flat")))
    player = new_player(items=['Fix-a-Flat'])
    player.slow_tire_leak()
    print(bright(red("Testing slow_tire_leak with Tire Patch Kit")))
    player = new_player(items=['Tire Patch Kit'])
    player.slow_tire_leak()

def starter_motor_grinding():
    print(bright(red("TESTING starter_motor_grinding with no items")))
    player = new_player()
    player.starter_motor_grinding()

def strange_engine_noise():
    print(bright(red("TESTING strange_engine_noise with no items")))
    player = new_player()
    player.strange_engine_noise()
    print(bright(red("Testing strange_engine_noise with Lucky Coin")))
    player = new_player(items=['Lucky Coin'])
    player.strange_engine_noise()
    print(bright(red("Testing strange_engine_noise with Lucky Medallion")))
    player = new_player(items=['Lucky Medallion'])
    player.strange_engine_noise()
    print(bright(red("Testing strange_engine_noise with Serpentine Belt")))
    player = new_player(items=['Serpentine Belt'])
    player.strange_engine_noise()

def stuck_in_gear():
    print(bright(red("TESTING stuck_in_gear with no items")))
    player = new_player()
    player.stuck_in_gear()

def suspension_creaking():
    print(bright(red("TESTING suspension_creaking with no items")))
    player = new_player()
    player.suspension_creaking()

def thermostat_stuck():
    print(bright(red("TESTING thermostat_stuck with no items")))
    player = new_player()
    player.thermostat_stuck()
    print(bright(red("Testing thermostat_stuck with Thermostat")))
    player = new_player(items=['Thermostat'])
    player.thermostat_stuck()

def tire_blowout():
    print(bright(red("TESTING tire_blowout with no items")))
    player = new_player()
    player.tire_blowout()
    print(bright(red("Testing tire_blowout with Car Jack")))
    player = new_player(items=['Car Jack'])
    player.tire_blowout()
    print(bright(red("Testing tire_blowout with Spare Tire")))
    player = new_player(items=['Spare Tire'])
    player.tire_blowout()
    print(bright(red("Testing tire_blowout with Tire Ready Kit")))
    player = new_player(items=['Tire Ready Kit'])
    player.tire_blowout()

def transmission_slipping():
    print(bright(red("TESTING transmission_slipping with no items")))
    player = new_player()
    player.transmission_slipping()
    print(bright(red("Testing transmission_slipping with Miracle Lube")))
    player = new_player(items=['Miracle Lube'])
    player.transmission_slipping()
    print(bright(red("Testing transmission_slipping with Transmission Fluid")))
    player = new_player(items=['Transmission Fluid'])
    player.transmission_slipping()

def trunk_wont_close():
    print(bright(red("TESTING trunk_wont_close with no items")))
    player = new_player()
    player.trunk_wont_close()
    print(bright(red("Testing trunk_wont_close with Bungee Cords")))
    player = new_player(items=['Bungee Cords'])
    player.trunk_wont_close()
    print(bright(red("Testing trunk_wont_close with Rope")))
    player = new_player(items=['Rope'])
    player.trunk_wont_close()

def water_pump_failing():
    print(bright(red("TESTING water_pump_failing with no items")))
    player = new_player()
    player.water_pump_failing()

def wheel_alignment_off():
    print(bright(red("TESTING wheel_alignment_off with no items")))
    player = new_player()
    player.wheel_alignment_off()

def window_wont_roll_up():
    print(bright(red("TESTING window_wont_roll_up with no items")))
    player = new_player()
    player.window_wont_roll_up()
    print(bright(red("Testing window_wont_roll_up with Garbage Bag")))
    player = new_player(items=['Garbage Bag'])
    player.window_wont_roll_up()
    print(bright(red("Testing window_wont_roll_up with Plastic Wrap")))
    player = new_player(items=['Plastic Wrap'])
    player.window_wont_roll_up()

def windshield_cracked():
    print(bright(red("TESTING windshield_cracked with no items")))
    player = new_player()
    player.windshield_cracked()


"""story.adventures.py"""
def beach_adventure():
    print(bright(red("TESTING beach_adventure with no items")))
    player = new_player()
    player.beach_adventure()
    print(bright(red("Testing beach_adventure with All-Weather Armor")))
    player = new_player(items=['All-Weather Armor'])
    player.beach_adventure()
    print(bright(red("Testing beach_adventure with Animal Whistle")))
    player = new_player(items=['Animal Whistle'])
    player.beach_adventure()
    print(bright(red("Testing beach_adventure with Fish")))
    player = new_player(items=['Fish'])
    player.beach_adventure()
    print(bright(red("Testing beach_adventure with Hydration Station")))
    player = new_player(items=['Hydration Station'])
    player.beach_adventure()
    print(bright(red("Testing beach_adventure with Live Fish")))
    player = new_player(items=['Live Fish'])
    player.beach_adventure()
    print(bright(red("Testing beach_adventure with SOS Kit")))
    player = new_player(items=['SOS Kit'])
    player.beach_adventure()
    print(bright(red("Testing beach_adventure with Sea Glass")))
    player = new_player(items=['Sea Glass'])
    player.beach_adventure()

def chase_the_last_rabbit():
    print(bright(red("TESTING chase_the_last_rabbit with no items")))
    player = new_player()
    player.chase_the_last_rabbit()
    print(bright(red("Testing chase_the_last_rabbit with Eternal Light")))
    player = new_player(items=['Eternal Light'])
    player.chase_the_last_rabbit()
    print(bright(red("Testing chase_the_last_rabbit with Flashlight")))
    player = new_player(items=['Flashlight'])
    player.chase_the_last_rabbit()
    print(bright(red("Testing chase_the_last_rabbit with Headlamp")))
    player = new_player(items=['Headlamp'])
    player.chase_the_last_rabbit()
    print(bright(red("Testing chase_the_last_rabbit with Lantern")))
    player = new_player(items=['Lantern'])
    player.chase_the_last_rabbit()
    print(bright(red("Testing chase_the_last_rabbit with Night Scope")))
    player = new_player(items=['Night Scope'])
    player.chase_the_last_rabbit()

def city_adventure():
    print(bright(red("TESTING city_adventure with no items")))
    player = new_player()
    player.city_adventure()
    print(bright(red("Testing city_adventure with Intelligence Dossier")))
    player = new_player(items=['Intelligence Dossier'])
    player.city_adventure()
    print(bright(red("Testing city_adventure with Pepper Spray")))
    player = new_player(items=['Pepper Spray'])
    player.city_adventure()
    print(bright(red("Testing city_adventure with Underground Pass")))
    player = new_player(items=['Underground Pass'])
    player.city_adventure()

def road_adventure():
    print(bright(red("TESTING road_adventure with no items")))
    player = new_player()
    player.road_adventure()
    print(bright(red("Testing road_adventure with Animal Whistle")))
    player = new_player(items=['Animal Whistle'])
    player.road_adventure()
    print(bright(red("Testing road_adventure with Beef Jerky")))
    player = new_player(items=['Beef Jerky'])
    player.road_adventure()
    print(bright(red("Testing road_adventure with Deck of Cards")))
    player = new_player(items=['Deck of Cards'])
    player.road_adventure()
    print(bright(red("Testing road_adventure with Duct Tape")))
    player = new_player(items=['Duct Tape'])
    player.road_adventure()
    print(bright(red("Testing road_adventure with Granola Bar")))
    player = new_player(items=['Granola Bar'])
    player.road_adventure()
    print(bright(red("Testing road_adventure with Hot Dog")))
    player = new_player(items=['Hot Dog'])
    player.road_adventure()
    print(bright(red("Testing road_adventure with Immortal Vehicle")))
    player = new_player(items=['Immortal Vehicle'])
    player.road_adventure()
    print(bright(red("Testing road_adventure with Road Warrior Badge")))
    player = new_player(items=['Road Warrior Badge'])
    player.road_adventure()
    print(bright(red("Testing road_adventure with Tool Kit")))
    player = new_player(items=['Tool Kit'])
    player.road_adventure()
    print(bright(red("Testing road_adventure with Turkey Sandwich")))
    player = new_player(items=['Turkey Sandwich'])
    player.road_adventure()

def swamp_adventure():
    print(bright(red("TESTING swamp_adventure with no items")))
    player = new_player()
    player.swamp_adventure()
    print(bright(red("Testing swamp_adventure with Animal Whistle")))
    player = new_player(items=['Animal Whistle'])
    player.swamp_adventure()
    print(bright(red("Testing swamp_adventure with First Aid Kit")))
    player = new_player(items=['First Aid Kit'])
    player.swamp_adventure()
    print(bright(red("Testing swamp_adventure with Gas Mask")))
    player = new_player(items=['Gas Mask'])
    player.swamp_adventure()
    print(bright(red("Testing swamp_adventure with Hazmat Suit")))
    player = new_player(items=['Hazmat Suit'])
    player.swamp_adventure()
    print(bright(red("Testing swamp_adventure with Lettuce")))
    player = new_player(items=['Lettuce'])
    player.swamp_adventure()
    print(bright(red("Testing swamp_adventure with Nomad's Camp")))
    player = new_player(items=["Nomad's Camp"])
    player.swamp_adventure()
    print(bright(red("Testing swamp_adventure with Pocket Knife")))
    player = new_player(items=['Pocket Knife'])
    player.swamp_adventure()
    print(bright(red("Testing swamp_adventure with Road Warrior Armor")))
    player = new_player(items=['Road Warrior Armor'])
    player.swamp_adventure()
    print(bright(red("Testing swamp_adventure with Rope")))
    player = new_player(items=['Rope'])
    player.swamp_adventure()
    print(bright(red("Testing swamp_adventure with Scrap Armor")))
    player = new_player(items=['Scrap Armor'])
    player.swamp_adventure()
    print(bright(red("Testing swamp_adventure with Survival Bivouac")))
    player = new_player(items=['Survival Bivouac'])
    player.swamp_adventure()
    print(bright(red("Testing swamp_adventure with Swamp Rune")))
    player = new_player(items=['Swamp Rune'])
    player.swamp_adventure()
    print(bright(red("Testing swamp_adventure with Wanderer's Rest")))
    player = new_player(items=["Wanderer's Rest"])
    player.swamp_adventure()
    print(bright(red("Testing swamp_adventure with Water Purifier")))
    player = new_player(items=['Water Purifier'])
    player.swamp_adventure()

def underwater_adventure():
    print(bright(red("TESTING underwater_adventure with no items")))
    player = new_player()
    player.underwater_adventure()
    print(bright(red("Testing underwater_adventure with All-Access Pass")))
    player = new_player(items=['All-Access Pass'])
    player.underwater_adventure()
    print(bright(red("Testing underwater_adventure with Animal Whistle")))
    player = new_player(items=['Animal Whistle'])
    player.underwater_adventure()
    print(bright(red("Testing underwater_adventure with Depth Charm")))
    player = new_player(items=['Depth Charm'])
    player.underwater_adventure()
    print(bright(red("Testing underwater_adventure with Fish")))
    player = new_player(items=['Fish'])
    player.underwater_adventure()
    print(bright(red("Testing underwater_adventure with Live Fish")))
    player = new_player(items=['Live Fish'])
    player.underwater_adventure()
    print(bright(red("Testing underwater_adventure with Lockpick Set")))
    player = new_player(items=['Lockpick Set'])
    player.underwater_adventure()
    print(bright(red("Testing underwater_adventure with Master Key")))
    player = new_player(items=['Master Key'])
    player.underwater_adventure()
    print(bright(red("Testing underwater_adventure with Security Bypass")))
    player = new_player(items=['Security Bypass'])
    player.underwater_adventure()
    print(bright(red("Testing underwater_adventure with Skeleton Key")))
    player = new_player(items=['Skeleton Key'])
    player.underwater_adventure()
    print(bright(red("Testing underwater_adventure with Stolen Marlin")))
    player = new_player(items=['Stolen Marlin'])
    player.underwater_adventure()

def woodlands_adventure():
    print(bright(red("TESTING woodlands_adventure with no items")))
    player = new_player()
    player.woodlands_adventure()
    print(bright(red("Testing woodlands_adventure with Animal Whistle")))
    player = new_player(items=['Animal Whistle'])
    player.woodlands_adventure()
    print(bright(red("Testing woodlands_adventure with Assassin's Kit")))
    player = new_player(items=["Assassin's Kit"])
    player.woodlands_adventure()
    print(bright(red("Testing woodlands_adventure with Beast Tamer Kit")))
    player = new_player(items=['Beast Tamer Kit'])
    player.woodlands_adventure()
    print(bright(red("Testing woodlands_adventure with Binocular Scope")))
    player = new_player(items=['Binocular Scope'])
    player.woodlands_adventure()
    print(bright(red("Testing woodlands_adventure with Binoculars")))
    player = new_player(items=['Binoculars'])
    player.woodlands_adventure()
    print(bright(red("Testing woodlands_adventure with Druid's Staff")))
    player = new_player(items=["Druid's Staff"])
    player.woodlands_adventure()
    print(bright(red("Testing woodlands_adventure with First Aid Kit")))
    player = new_player(items=['First Aid Kit'])
    player.woodlands_adventure()
    print(bright(red("Testing woodlands_adventure with Fishing Rod")))
    player = new_player(items=['Fishing Rod'])
    player.woodlands_adventure()
    print(bright(red("Testing woodlands_adventure with Golden Compass")))
    player = new_player(items=['Golden Compass'])
    player.woodlands_adventure()
    print(bright(red("Testing woodlands_adventure with Master Knife")))
    player = new_player(items=['Master Knife'])
    player.woodlands_adventure()
    print(bright(red("Testing woodlands_adventure with Night Vision Scope")))
    player = new_player(items=['Night Vision Scope'])
    player.woodlands_adventure()
    print(bright(red("Testing woodlands_adventure with Nomad's Camp")))
    player = new_player(items=["Nomad's Camp"])
    player.woodlands_adventure()
    print(bright(red("Testing woodlands_adventure with Plated Vest")))
    player = new_player(items=['Plated Vest'])
    player.woodlands_adventure()
    print(bright(red("Testing woodlands_adventure with Pocket Knife")))
    player = new_player(items=['Pocket Knife'])
    player.woodlands_adventure()
    print(bright(red("Testing woodlands_adventure with Provider's Kit")))
    player = new_player(items=["Provider's Kit"])
    player.woodlands_adventure()
    print(bright(red("Testing woodlands_adventure with Road Warrior Armor")))
    player = new_player(items=['Road Warrior Armor'])
    player.woodlands_adventure()
    print(bright(red("Testing woodlands_adventure with Road Warrior Plate")))
    player = new_player(items=['Road Warrior Plate'])
    player.woodlands_adventure()
    print(bright(red("Testing woodlands_adventure with Rope")))
    player = new_player(items=['Rope'])
    player.woodlands_adventure()
    print(bright(red("Testing woodlands_adventure with Rusty Compass")))
    player = new_player(items=['Rusty Compass'])
    player.woodlands_adventure()
    print(bright(red("Testing woodlands_adventure with Scrap Armor")))
    player = new_player(items=['Scrap Armor'])
    player.woodlands_adventure()
    print(bright(red("Testing woodlands_adventure with Signal Mirror")))
    player = new_player(items=['Signal Mirror'])
    player.woodlands_adventure()
    print(bright(red("Testing woodlands_adventure with Smoke Signal Kit")))
    player = new_player(items=['Smoke Signal Kit'])
    player.woodlands_adventure()
    print(bright(red("Testing woodlands_adventure with Street Fighter Set")))
    player = new_player(items=['Street Fighter Set'])
    player.woodlands_adventure()
    print(bright(red("Testing woodlands_adventure with Survival Bivouac")))
    player = new_player(items=['Survival Bivouac'])
    player.woodlands_adventure()
    print(bright(red("Testing woodlands_adventure with Utility Blade")))
    player = new_player(items=['Utility Blade'])
    player.woodlands_adventure()
    print(bright(red("Testing woodlands_adventure with Wanderer's Rest")))
    player = new_player(items=["Wanderer's Rest"])
    player.woodlands_adventure()


def run_all_events():
    for tester in ALL_EVENT_TESTERS:
        before = len(REROUTE_LOG)
        tester()
        after = len(REROUTE_LOG)
        if after > before:
            print(bright(red("REROUTE SUMMARY for " + tester.__name__ + ": " + str(after - before) + " blocked redirect(s)")))


class SeededAsk:
    """Deterministic ask shim driven by a seed and prompt context."""

    def __init__(self, seed):
        self.seed = int(seed)
        self.step = 0
        self.trace = []

    def _idx(self, label, options_len):
        if options_len <= 0:
            return 0
        payload = f"{self.seed}:{self.step}:{label}".encode("utf-8")
        digest = hashlib.sha256(payload).hexdigest()
        self.step += 1
        return int(digest, 16) % options_len

    def _record(self, kind, prompt, choice):
        prompt_text = str(prompt or "")
        if len(prompt_text) > 80:
            prompt_text = prompt_text[:77] + "..."
        self.trace.append((kind, prompt_text, str(choice)))

    def single_word(self, prompt=""):
        options = ["test", "ok", "yes", "no", "pass"]
        value = options[self._idx(f"single_word:{prompt}", len(options))]
        self._record("single_word", prompt, value)
        return value

    def choose_a_number(self, a, b, guess=False):
        lo = min(int(a), int(b))
        hi = max(int(a), int(b))
        value = lo + self._idx(f"choose_a_number:{a}:{b}:{guess}", hi - lo + 1)
        self._record("choose_a_number", f"{a}..{b}", value)
        return str(value)

    def choose_an_option(self, options, reiterate="What? ", first_letter=True):
        options = [str(o) for o in options]
        if not options:
            self._record("choose_an_option", reiterate, "")
            return ""
        idx = self._idx(f"choose_an_option:{reiterate}:{first_letter}:{'|'.join(options)}", len(options))
        value = options[idx]
        self._record("choose_an_option", reiterate, value)
        return value

    def option(self, prompt, options):
        options = [str(o) for o in options]
        if not options:
            self._record("option", prompt, "")
            return ""
        idx = self._idx(f"option:{prompt}:{'|'.join(options)}", len(options))
        value = options[idx]
        self._record("option", prompt, value)
        return value

    def yes_or_no(self, reiterate="What? "):
        value = "yes" if self._idx(f"yes_or_no:{reiterate}", 2) == 0 else "no"
        self._record("yes_or_no", reiterate, value)
        return value

    def give_cash(self, total, reiterate="How much? "):
        try:
            max_total = max(0, int(total))
        except (TypeError, ValueError):
            max_total = 0
        if max_total == 0:
            value = 0
        else:
            value = self._idx(f"give_cash:{reiterate}:{max_total}", max_total + 1)
        self._record("give_cash", reiterate, value)
        return value

    def press_continue(self, message="Press any key to continue: "):
        self._record("press_continue", message, "continue")
        return None

    def continue_cleanup(self):
        return True


class FastType:
    """Instant output shim for high-volume seeded sweeps."""

    @staticmethod
    def _emit(*words):
        if words:
            print("".join(str(w) for w in words))

    def check_for_skip(self):
        return None

    def fast(self, *words):
        self._emit(*words)

    def fast_clean(self, *words):
        self._emit(*words)

    def slow(self, *words):
        self._emit(*words)

    def slow_clean(self, *words):
        self._emit(*words)

    def suspense(self, *words):
        self._emit(*words)

    def suspense_clean(self, *words):
        self._emit(*words)

    def type(self, *words):
        self._emit(*words)

    def type_clean(self, *words):
        self._emit(*words)

    def typeover(self, prompt, text, newline=False):
        if newline:
            print(str(prompt) + str(text))
        else:
            print(str(prompt) + str(text), end="")

    def cleanup(self):
        return None


def _patch_story_ask(seed_ask):
    patched = []
    for module_name, module in list(sys.modules.items()):
        if not module_name.startswith("story"):
            continue
        if module is None:
            continue
        if hasattr(module, "ask"):
            old = getattr(module, "ask")
            setattr(module, "ask", seed_ask)
            patched.append((module, old))
    return patched


def _restore_story_ask(patched):
    for module, old in patched:
        setattr(module, "ask", old)


def _patch_story_type(fast_type):
    patched = []
    for module_name, module in list(sys.modules.items()):
        if not module_name.startswith("story"):
            continue
        if module is None:
            continue
        if hasattr(module, "type"):
            old = getattr(module, "type")
            setattr(module, "type", fast_type)
            patched.append((module, old))
    return patched


def _restore_story_type(patched):
    for module, old in patched:
        setattr(module, "type", old)


def run_seeded_subset(event_names, seeds):
    """Run a subset of tester functions with deterministic seeded decisions.

    event_names: list of function names from this file, e.g. ["shiv_confrontation"]
    seeds: list of integer seeds
    """
    name_to_callable = {fn.__name__: fn for fn in ALL_EVENT_TESTERS}
    selected = []
    for name in event_names:
        fn = name_to_callable.get(name)
        if fn is None:
            print(bright(red("UNKNOWN TESTER: " + str(name))))
            continue
        selected.append(fn)

    global ACTIVE_TEST_SEED
    global ACTIVE_TEST_SEED_COUNTER

    for seed in seeds:
        print(bright(red("SEED RUN " + str(seed))))
        seed_ask = SeededAsk(seed)
        fast_type = FastType()
        patched_ask = _patch_story_ask(seed_ask)
        patched_type = _patch_story_type(fast_type)
        ACTIVE_TEST_SEED = int(seed)
        ACTIVE_TEST_SEED_COUNTER = 0
        try:
            for tester in selected:
                before = len(REROUTE_LOG)
                print(bright(red("TESTER " + tester.__name__ + " (seed " + str(seed) + ")")))
                tester()
                after = len(REROUTE_LOG)
                if after > before:
                    print(bright(red("REROUTE SUMMARY for " + tester.__name__ + ": " + str(after - before) + " blocked redirect(s)")))
        finally:
            ACTIVE_TEST_SEED = None
            ACTIVE_TEST_SEED_COUNTER = 0
            _restore_story_ask(patched_ask)
            _restore_story_type(patched_type)

        if seed_ask.trace:
            print(bright(red("SEED " + str(seed) + " DECISION TRACE")))
            for index, (kind, prompt, choice) in enumerate(seed_ask.trace, start=1):
                print(red(f"  [{index}] {kind} | {prompt} -> {choice}"))


def run_seeded_sweep(event_name, seed_start, seed_count):
    seeds = list(range(int(seed_start), int(seed_start) + int(seed_count)))
    run_seeded_subset([event_name], seeds)


ALL_EVENT_TESTERS = [
    cow_army,
    crow_encounter,
    duck_army,
    estranged_dog,
    garden_rabbit,
    grimy_gus_discovery,
    hungry_cow,
    hungry_termites,
    lucky_penny,
    lucky_rabbit_encounter,
    motivational_raccoon,
    opossum_in_trash,
    pigeon_mafia,
    raccoon_gang_raid,
    raccoon_raid,
    events_day_animals__rat_bite,
    seagull_attack,
    sentient_sandwich,
    sewer_rat,
    squirrel_invasion,
    starving_cow,
    stray_cat,
    stray_cat_dies,
    stray_cat_has_kittens,
    stray_cat_sick,
    three_legged_dog,
    wild_rat_attack,
    wrong_item_dog_whistle_bear,
    casino_security,
    even_further_interrogation,
    high_stakes_feeling,
    perfect_hand,
    the_dying_dealer,
    bear_scrap_armor_synergy,
    buddy_dog_whistle_synergy,
    buddy_passive_find,
    companion_bed_bonus,
    companion_bonded_moment,
    companion_brings_friend,
    companion_death_sacrifice,
    companion_food_crisis,
    companion_hero_moment,
    companion_learns_trick,
    companion_lost_adventure,
    companion_milestone,
    companion_reunion,
    companion_rivalry,
    companion_sick_day,
    echo_camera_synergy,
    feeding_station_morning,
    grace_dream_catcher_synergy,
    hopper_lucky_day,
    hopper_passive_find,
    lucky_guards_car,
    mr_pecks_treasure,
    patches_night_watch,
    pet_toy_playtime,
    rusty_midnight_heist,
    shellbert_worry_stone_synergy,
    slick_escape_route,
    slick_passive_find,
    squirrelly_stash,
    the_cat_knows,
    thunder_running_shoes_synergy,
    whiskers_sixth_sense,
    attacked_by_dog,
    back_alley_shortcut,
    bridge_angel_returns,
    bridge_contemplation,
    burn_scars_infection,
    burn_scars_stares,
    call_bridge_angel,
    cancer_diagnosis,
    car_explosion,
    carbon_monoxide,
    casino_hitman,
    casino_overdose,
    cocaine_crash,
    cocaine_heart_attack,
    cocaine_temptation,
    devils_bargain_consequence,
    dog_bite_rabies_scare,
    drowning_dream,
    drug_dealer_encounter,
    electrocution_hazard,
    food_poisoning,
    fuel_leak_fire,
    fuel_leak_fixed,
    gas_station_hero_interview,
    gas_station_hero_recognized,
    gas_station_robbery,
    gut_wound_complications,
    heart_attack_scare,
    heart_condition_flare,
    knife_wound_infection,
    loan_shark_visit,
    necronomicon_reading,
    old_gambling_buddy,
    organ_harvester,
    painkiller_dealer_returns,
    painkiller_overdose,
    painkiller_withdrawal,
    shoulder_chronic_pain,
    shoulder_painkiller_addiction,
    soulless_emptiness,
    soulless_mirror,
    soulless_recognition,
    survivor_guilt,
    the_anniversary_loss,
    the_bridge_call,
    the_confession,
    the_desperate_gambler,
    the_high_roller_suicide,
    the_relapse,
    the_scar_story,
    the_winning_streak_paranoia,
    voodoo_doll_temptation,
    weakened_immune_cold,
    weakened_immune_pneumonia,
    withdrawal_nightmare,
    wrong_item_necronomicon_loan_shark,
    wrong_item_road_flares_stealth,
    ace_of_spades_blackjack_omen,
    alien_crystal_event,
    animal_bait_companion,
    animal_magnetism_predator,
    animal_magnetism_recruit,
    antacid_business_dinner,
    apartment_key_visit,
    aristocrat_cold_elegance,
    beach_bum_heatwave,
    beach_bum_tribe,
    beach_bum_yacht_party,
    beach_romance_call,
    binocular_scope_discovery,
    blackmail_letter_extortion,
    blank_check_opportunity,
    bottle_of_tomorrow_use,
    brass_knuckles_brawl,
    capture_fairy_release,
    cool_down_car_overheat,
    council_feather_blessing,
    cowboy_jacket_encounter,
    dealer_joker_revelation,
    deck_of_cards_street_game,
    devils_deck_gambling,
    dimensional_coin_flip,
    dream_catcher_night,
    eldritch_candle_entity,
    emergency_blanket_cold_night,
    emp_device_pursuit,
    empty_locket_memory,
    enchanted_vintage_party,
    evidence_kit_crime,
    fake_flower_gift,
    feelgood_bottle_moment,
    fire_starter_campfire,
    fishing_day,
    forged_documents_police,
    fortune_cards_warning,
    found_phone_call,
    gamblers_aura_blackjack,
    gas_mask_chemical,
    gas_mask_fire_rescue,
    gas_mask_toxic_spill,
    gentleman_charm_dinner,
    ghost_protocol_invisible,
    guardian_angel_lethal,
    headlamp_night_walk,
    heirloom_set_recognition,
    herbal_pouch_remedy,
    hollow_tree_stash_find,
    home_remedy_illness,
    immortal_vehicle_breakdown,
    item_hoarder,
    junkyard_crown_moment,
    kingpin_look_respect,
    lockbox_contents,
    lockpick_opportunity,
    lottery_ticket_check,
    love_potion_use,
    low_profile_casino_blend,
    low_profile_mugging_marcus,
    low_profile_police_encounter,
    low_profile_shelter_meal,
    luck_totem_windfall,
    lucky_charm_streak,
    lucky_lure_fishing,
    magic_acorn_planting,
    miracle_lube_breakdown,
    mobile_workshop_stranger,
    mysterious_code_decode,
    mysterious_envelope_reveal,
    mysterious_key_lockbox_open,
    mystery_potion_effect,
    old_photograph_memory,
    outdoor_shield_farmer,
    persistent_bottle_refill,
    power_grid_dead_battery,
    power_move_intimidation,
    pursuit_package_chase,
    pursuit_package_witness,
    radio_jammer_checkpoint,
    radio_numbers_broadcast,
    rain_collector_bonus,
    reunion_photo_comfort,
    ritual_token_ceremony,
    road_flare_torch_encounter,
    road_talisman_protection,
    road_warrior_ambush,
    scrap_armor_event,
    secret_route_shortcut,
    security_bypass_locked_room,
    shiv_confrontation,
    signal_mirror_rescue,
    silver_horseshoe_luck,
    slingshot_bird_hunt,
    smoke_flare_pursuit,
    snare_trap_catch,
    splint_injury_event,
    spotlight_hidden_path,
    stack_of_flyers_opportunity,
    stink_bomb_escape,
    stolen_watch_recognition,
    storm_suit_flood,
    storm_suit_hurricane,
    storm_suit_night_bear,
    street_cat_ally_benefit,
    suspicious_package_open,
    swamp_gold_attention,
    third_eye_foresight,
    tinfoil_hat_event,
    tire_ready_flat,
    trail_mix_bomb_distraction,
    trap_night_thief,
    treasure_map_follow,
    underwater_camera_photos,
    vermin_bomb_car,
    vision_map_navigate,
    voice_soother_persuasion,
    walking_stick_hike,
    water_purifier_use,
    wild_binding_portrait_shopkeeper,
    wild_blackmail_letter_companion,
    wild_devil_deck_children,
    wild_distress_beacon_casino,
    wild_eldritch_candle_gambling,
    wild_emp_casino,
    wild_evidence_kit_wedding,
    wild_fortune_cards_car,
    wild_gas_mask_funeral,
    wild_headlamp_poker,
    wild_radio_jammer_police,
    wild_stink_bomb_casino_vault,
    witch_ward_dark_protection,
    worry_stone_moment,
    completely_broke_wisdom,
    day_palindrome,
    exactly_100,
    exactly_1234,
    exactly_13,
    exactly_420,
    exactly_69420,
    exactly_7777,
    first_sunrise,
    full_moon_madness,
    haunted_by_losses,
    insomniac_revelation,
    perfect_health_moment,
    prime_day,
    rain_on_the_roof,
    rock_bottom,
    same_as_health,
    the_crow_council,
    the_veteran_gambler,
    autograph_request,
    birthday_forgotten,
    book_club_invite,
    broken_atm,
    car_alarm_symphony,
    car_compliment,
    car_wash_encounter,
    casino_regular,
    caught_fishing,
    cigar_circle,
    classy_encounter,
    cloud_watching,
    coffee_shop_philosopher,
    coin_flip_stranger,
    compliment_stranger,
    conspiracy_theorist,
    dog_walker_collision,
    dropped_ice_cream,
    fancy_coffee,
    fancy_restaurant_mistake,
    filthy_frank_radio_giveaway,
    flea_market_route_map,
    food_truck_festival,
    forgotten_birthday,
    fortune_cookie,
    found_phone,
    free_sample_spree,
    freight_truck,
    friendly_drunk,
    further_interrogation,
    homeless_network,
    ice_cream_truck,
    interrogation,
    kid_on_bike,
    laundromat_bulletin_map,
    lone_cowboy,
    lost_tourist,
    lottery_scratch,
    mayas_luck,
    midnight_visitor,
    motivational_graffiti,
    mysterious_package,
    old_man_jenkins,
    oswald_concierge_card,
    parking_lot_poker,
    parking_ticket,
    phone_scam_call,
    photo_opportunity,
    roadkill_philosophy,
    roadside_bone_chimes,
    robbery_attempt,
    social_encounter,
    street_musician,
    street_performer,
    street_performer_duel,
    talking_to_yourself,
    the_doppelganger,
    the_food_truck,
    the_gambler_ghost,
    the_hitchhiker,
    the_mime,
    the_photographer,
    the_prophet,
    the_sleeping_stranger,
    trash_treasure,
    trusty_tom_coupon_mailer,
    vending_machine_luck,
    vinnie_referral_card,
    whats_my_name,
    windblown_worn_map,
    wine_and_dine,
    witch_doctor_matchbook,
    wrong_item_dirty_hat_dinner,
    wrong_item_pest_control_romance,
    wrong_item_vermin_bomb_romance,
    wrong_number,
    yard_sale_find,
    crossover_all_chains_complete,
    crossover_artisan_rose_gift,
    crossover_night_vision_bonus,
    crossover_radio_hermit,
    gift_from_suzy,
    hermit_camp_return,
    hermit_hollow_oak,
    hermit_journal_study,
    hermit_trail_discovery,
    hermit_trail_stranger,
    junkyard_artisan_meet,
    junkyard_gideon_story,
    junkyard_lesson_one,
    junkyard_lesson_two,
    junkyard_masterpiece,
    lost_dog_culprit,
    lost_dog_flyers_found,
    lost_dog_investigation,
    lost_dog_reunion,
    lost_dog_whistle_search,
    midnight_radio_broadcast,
    midnight_radio_frequency,
    midnight_radio_pole,
    midnight_radio_signal,
    midnight_radio_visit,
    suzy_the_snitch,
    alien_abduction,
    blood_moon_bargain,
    dance_battle,
    fourth_wall_break,
    mirror_stranger,
    sock_puppet_therapist,
    the_collector,
    the_empty_room,
    the_glitch,
    time_loop,
    wrong_universe,
    another_spider_bite,
    ant_bite,
    ant_invasion,
    back_pain,
    bad_hair_day,
    beautiful_sunrise,
    bird_droppings,
    broken_belonging,
    car_battery_dead,
    car_smell,
    car_wont_start,
    cold_gets_worse,
    construction_noise,
    damaged_exhaust_again,
    damaged_exhaust_fixed,
    deja_vu,
    deja_vu_again,
    empty_event,
    flat_tire,
    flat_tire_again,
    found_gift_card,
    found_old_photo,
    found_twenty,
    freezing_night,
    good_hair_day,
    got_a_cold,
    got_a_tan,
    hungry_cockroach,
    important_document,
    left_door_open,
    left_trunk_open,
    left_window_down,
    lost_wallet,
    morning_fog,
    morning_stretch,
    mosquito_bite_infection,
    mosquito_swarm,
    mysterious_note,
    mystery_car_problem_worsens,
    need_fire,
    nice_weather,
    penny_luck,
    power_outage_area,
    prayer_answered,
    prayer_ignored,
    radio_static,
    random_cruelty,
    random_kindness,
    roadside_breakdown,
    rubber_band_save,
    scorching_sun,
    seat_cash,
    someone_stole_your_stuff,
    sore_throat,
    spider_bite,
    stretching_helps,
    strong_winds,
    sudden_downpour,
    sun_visor_bills,
    sunburn,
    terrible_weather,
    threw_out_old_photo,
    thunderstorm,
    turn_to_god,
    weird_noise,
    wrong_item_bug_spray_campfire,
    all_dreams_complete,
    almost_there,
    atm_theft_police,
    booted_car_impound,
    casino_comps,
    casino_knows,
    casino_owner_meeting,
    charity_opportunity,
    exactly_1111,
    exactly_250000,
    exactly_50000,
    exactly_777777,
    exactly_999999,
    expensive_taste,
    final_dream,
    final_interrogation,
    high_roller_invitation,
    high_roller_room,
    high_roller_room_visit,
    high_roller_whale,
    imposter_syndrome,
    investment_opportunity,
    investment_pitch,
    last_stretch,
    likely_death,
    luxury_car_passes,
    luxury_problems,
    media_known_documentary,
    media_known_harassed,
    millionaire_fantasy,
    millionaire_milestone,
    money_counting_ritual,
    nervous_habits,
    news_van,
    old_friend_recognition,
    old_rival_encounter,
    old_rival_returns,
    paparazzi_mistake,
    people_watching,
    reporters_found_you,
    rich_persons_problems,
    strange_visitors,
    tax_man,
    the_bodyguard_offer,
    the_celebration,
    the_final_temptation,
    the_journalist,
    the_offer,
    the_offer_refused,
    the_rival,
    the_temptation,
    the_veteran,
    the_warning,
    the_weight_of_wealth,
    too_close_to_quit,
    unpaid_ticket_consequence,
    unpaid_tickets_boot,
    victoria_returns,
    wealth_anxiety,
    wealth_paranoia,
    wealthy_doubts,
    allergic_reaction_restaurant,
    appendicitis_attack,
    asbestos_exposure,
    assault_aftermath,
    asthma_attack,
    bad_mushrooms,
    bad_oysters,
    bad_sushi,
    bad_tattoo_infection,
    bar_fight_aftermath,
    bee_sting_allergy,
    blood_clot_in_leg,
    blood_poisoning,
    botched_piercing,
    botched_surgery,
    broken_ankle,
    broken_collarbone,
    broken_hand,
    broken_nose,
    broken_ribs_injury,
    broken_wrist,
    camping_tick_bite,
    car_accident_minor,
    carnival_ride_accident,
    caught_in_fire,
    chemical_burn,
    chemical_spill,
    collapsed_lung,
    coma_awakening,
    concussion_injury,
    construction_site_accident,
    contract_bronchitis,
    contract_cold,
    contract_ear_infection,
    contract_flu,
    contract_lyme_disease,
    contract_measles,
    contract_mono,
    contract_pink_eye,
    contract_pneumonia,
    contract_rabies_scare,
    contract_ringworm,
    contract_scabies,
    contract_shingles,
    contract_sinus_infection,
    contract_staph_infection,
    contract_stomach_flu,
    contract_strep_throat,
    contract_tetanus,
    contract_uti,
    covid_complications,
    crush_injury,
    daycare_plague,
    deep_laceration,
    dental_disaster,
    detached_retina,
    develop_diabetes_symptoms,
    dirty_needle_stick,
    dislocated_shoulder,
    dog_attack_severe,
    drug_overdose_survival,
    earthquake_injury,
    electric_shock,
    electrical_burn,
    explosion_nearby,
    fall_down_stairs,
    food_truck_nightmare,
    frostbite,
    frozen_outdoors,
    gallbladder_attack,
    gangrene_infection,
    grease_fire,
    gym_accident,
    gym_collapse,
    heat_exhaustion_collapse,
    heat_stroke,
    herniated_disc,
    high_blood_pressure_crisis,
    hiking_disaster,
    homeless_shelter_outbreak,
    hypothermia,
    insomnia_chronic,
    jaw_fracture,
    kidney_stones,
    kitchen_accident,
    lead_poisoning,
    liver_laceration,
    malnutrition,
    mercury_poisoning,
    migraine_severe,
    mma_fight_aftermath,
    mold_exposure,
    motorcycle_crash,
    muscle_tear,
    nerve_damage,
    orbital_fracture,
    pancreatitis_attack,
    pool_diving_accident,
    prison_shiv_wound,
    ptsd_flashback,
    public_pool_infection,
    puncture_wound,
    random_illness,
    events_illness__rat_bite,
    ruptured_eardrum,
    ruptured_spleen,
    second_degree_burns,
    seizure_episode,
    severe_allergic_reaction,
    severe_anxiety_attack,
    severe_burn_injury,
    severe_dehydration,
    severe_depression_episode,
    skull_fracture,
    sleep_deprivation_crisis,
    slip_in_shower,
    sports_injury,
    stress_breakdown,
    tendon_rupture,
    tooth_abscess,
    torn_acl,
    trampoline_disaster,
    trauma_flashback,
    unclean_water,
    vertigo_episode,
    wasp_nest_encounter,
    weight_dropping,
    whiplash_injury,
    window_crash,
    workplace_injury,
    beach_dive,
    beach_stroll,
    beach_swim,
    chase_the_fifth_rabbit,
    chase_the_fourth_rabbit,
    chase_the_rabbit,
    chase_the_second_rabbit,
    chase_the_third_rabbit,
    city_park,
    city_streets,
    city_stroll,
    ditched_wallet,
    dream_of_winning,
    giant_oyster_opening,
    insomnia_night,
    late_night_radio,
    midnight_snack_run,
    midnight_walk,
    mysterious_lights,
    nice_dream,
    nightmare,
    nightmare_of_losing,
    peaceful_night,
    police_checkpoint,
    raccoon_invasion,
    satellite_falling,
    stargazing,
    stray_cat_returns,
    swamp_stroll,
    swamp_swim,
    swamp_wade,
    went_jogging,
    whats_my_favorite_animal,
    whats_my_favorite_color,
    woodlands_field,
    woodlands_path,
    woodlands_river,
    abs_light_on,
    alternator_failing,
    bald_tires_hydroplane,
    bald_tires_noticed,
    battery_acid_leak,
    brake_fluid_leak,
    brakes_squealing,
    broken_ball_joint,
    broken_ball_joint_breaks,
    car_alarm_malfunction,
    car_wont_go_in_reverse,
    catalytic_converter_stolen,
    check_engine_light_on,
    clogged_fuel_filter,
    corroded_battery_terminals,
    dead_battery_afternoon,
    engine_knock_worsens,
    engine_oil_empty,
    engine_overheating,
    engine_wont_turn_over,
    exhaust_leak_loud,
    failing_fuel_pump_dies,
    failing_starter_dies,
    flooded_engine,
    frozen_door_locks,
    frozen_fuel_line,
    fuel_pump_whining,
    fuse_blown,
    gas_pedal_sticking,
    hail_damage,
    headlights_burned_out,
    key_wont_turn,
    leaking_battery_worsens,
    mystery_breakdown,
    nail_in_tire,
    nail_in_tire_blows,
    oil_leak_spotted,
    parking_brake_stuck,
    power_steering_failure,
    radiator_leak,
    ran_out_of_gas,
    random_car_trouble,
    slow_tire_leak,
    starter_motor_grinding,
    strange_engine_noise,
    stuck_in_gear,
    suspension_creaking,
    thermostat_stuck,
    tire_blowout,
    transmission_slipping,
    trunk_wont_close,
    water_pump_failing,
    wheel_alignment_off,
    window_wont_roll_up,
    windshield_cracked,
    beach_adventure,
    chase_the_last_rabbit,
    city_adventure,
    road_adventure,
    swamp_adventure,
    underwater_adventure,
    woodlands_adventure,
]


def main():
    # Manual event calls: uncomment whichever you want to run.
    # Example:
    # item_hoarder()
    # shiv_confrontation()
    # lockpick_opportunity()
    #
    # To run every generated tester instead:
    # run_all_events()
    squirrel_invasion()
    pass


if __name__ == "__main__":
    main()
