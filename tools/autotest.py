"""Batch runner for quicktest with compact seed-by-seed reporting.

Usage:
    python tools/autotest.py [cycles] [start_seed] [end_seed]

Examples:
    python tools/autotest.py
    python tools/autotest.py 40 1 10
    python tools/autotest.py 60 18
    python tools/autotest.py 40 1 100
"""

from __future__ import annotations

import ast
import json
import os
import random
import re
import subprocess
import sys
import time
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from typing import cast

try:
    import msvcrt
except ImportError:
    msvcrt = None


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from tools.autoplay.config import MARVIN_ITEM_ORDER, WITCH_FLASK_PRIORITIES

QUICKTEST = os.path.join(ROOT, "tools", "quicktest.py")
REPORT = os.path.join(ROOT, "tools", "test_out.txt")
REPORT_JSON = os.path.join(ROOT, "tools", "test_out.json")
STORY_OUT = os.path.join(ROOT, "tools", "story_out.txt")
CUMULATIVE_REPORT = os.path.join(ROOT, "tools", "cumulative_test_out.txt")
STOP_KEY = "s"
STOP_POLL_SECONDS = 0.1


@dataclass
class CycleRecord:
    day: int | None = None
    cash_delta: int = 0
    health_delta: int = 0
    sanity_delta: int = 0
    events: list[str] = field(default_factory=list)
    injuries_added: list[str] = field(default_factory=list)
    statuses_added: list[str] = field(default_factory=list)
    injuries_removed: list[str] = field(default_factory=list)
    statuses_removed: list[str] = field(default_factory=list)


@dataclass
class RunResult:
    seed: int
    timed_out: bool = False
    return_code: int | None = None
    elapsed_seconds: float = 0.0
    day: int | None = None
    balance: int | None = None
    health: int | None = None
    sanity: int | None = None
    rank: int | None = None
    peak_rank: int | None = None
    peak_balance: int | None = None
    peak_balance_days: list[int] = field(default_factory=list)
    inventory: list[str] = field(default_factory=list)
    alive: bool | None = None
    has_car: bool = False
    ever_had_car: bool = False
    has_map: bool = False
    has_worn_map: bool = False
    millionaire_reached: bool = False
    millionaire_visited: bool = False
    death_cause: str = ""
    injuries: list[str] = field(default_factory=list)
    statuses: list[str] = field(default_factory=list)
    pawned_items: list[str] = field(default_factory=list)
    active_storylines: list[str] = field(default_factory=list)
    completed_storylines: list[str] = field(default_factory=list)
    failed_storylines: list[str] = field(default_factory=list)
    met_hits: dict[str, int] = field(default_factory=dict)
    location_hits: dict[str, int] = field(default_factory=dict)
    event_effects: dict[str, dict[str, float]] = field(default_factory=dict)
    top_location: str = "none"
    top_adventure: str = "none"
    error_count: int | None = None
    warning_count: int | None = None
    result_note: str = ""
    mechanic_decisions: list[dict[str, object]] = field(default_factory=list)
    fallback_decisions: dict[str, int] = field(default_factory=dict)
    event_polarity: dict[str, int] = field(default_factory=dict)
    item_impacts: dict[str, dict[str, int]] = field(default_factory=dict)
    item_provenance: dict[str, dict[str, list[tuple[int | None, str]]]] = field(default_factory=dict)
    cycle_records: list[CycleRecord] = field(default_factory=list)
    marvin_item_provenance: dict[str, dict[str, list[tuple[int | None, str]]]] = field(default_factory=dict)
    decision_request_counts: dict[str, int] = field(default_factory=dict)
    decision_request_context_counts: dict[str, int] = field(default_factory=dict)
    decision_trace_counts: dict[str, int] = field(default_factory=dict)
    decision_trace_context_counts: dict[str, int] = field(default_factory=dict)
    decision_goal_counts: dict[str, int] = field(default_factory=dict)
    decision_personality_counts: dict[str, int] = field(default_factory=dict)
    decision_reason_code_counts: dict[str, int] = field(default_factory=dict)
    decision_expected_value_avg: float | None = None
    decision_expected_value_max: float | None = None
    decision_expected_value_min: float | None = None
    route_outcome_counts: dict[str, int] = field(default_factory=dict)
    route_interrupt_kind_counts: dict[str, int] = field(default_factory=dict)
    route_interrupted_goal_counts: dict[str, int] = field(default_factory=dict)
    route_interrupted_top_goal_counts: dict[str, int] = field(default_factory=dict)
    route_applied_goal_counts: dict[str, int] = field(default_factory=dict)
    route_suppressed_goal_counts: dict[str, int] = field(default_factory=dict)
    early_mechanic_day_limit: int = 10
    early_mechanic_threshold: int = 200
    early_mechanic_peak_balance: int | None = None
    early_mechanic_peak_days: list[int] = field(default_factory=list)
    early_mechanic_balance_end: int | None = None
    early_mechanic_reached_threshold: bool = False
    early_mechanic_first_day_reached: int | None = None
    early_mechanic_offer_count: int = 0
    early_mechanic_affordable_offer_count: int = 0
    early_mechanic_accept_count: int = 0
    early_mechanic_first_offer_day: int | None = None
    early_mechanic_first_accept_day: int | None = None
    early_route_interrupt_count: int = 0
    early_medical_interrupt_count: int = 0
    early_route_applied_count: int = 0
    early_route_suppressed_count: int = 0
    # Rich statistics surfaces
    game_statistics: dict[str, int] = field(default_factory=dict)
    gambling_statistics: dict[str, int] = field(default_factory=dict)
    companions_list: list[str] = field(default_factory=list)
    broken_items_list: list[str] = field(default_factory=list)
    repairing_items_list: list[str] = field(default_factory=list)
    flask_purchases: dict[str, int] = field(default_factory=dict)
    items_ever_broken: dict[str, int] = field(default_factory=dict)
    dealer_happiness: int | None = None
    gift_system_unlocked: bool = False
    has_wrapped_gift: bool = False
    store_purchases: int = 0
    loan_shark_debt: int = 0
    loan_shark_warning_level: int = 0
    fraudulent_cash: int = 0
    gus_items_sold_count: int = 0
    gus_total_collectibles: int = 0
    gift_deliveries: list[dict[str, object]] = field(default_factory=list)
    dealer_free_hands: list[dict[str, object]] = field(default_factory=list)
    mechanic_dreams: dict[str, object] = field(default_factory=dict)
    companion_details: dict[str, dict[str, object]] = field(default_factory=dict)

    @property
    def reached_location(self) -> bool:
        return self.top_location != "none" or self.top_adventure != "none"

    @property
    def visited_doctor(self) -> bool:
        return self.location_hits.get("doctor", 0) > 0

    @property
    def visited_store(self) -> bool:
        return self.location_hits.get("shop:convenience_store", 0) > 0

    @property
    def visited_marvin(self) -> bool:
        return self.location_hits.get("shop:marvin", 0) > 0

    @property
    def met_tom(self) -> bool:
        return self.met_hits.get("Tom", 0) > 0

    @property
    def met_frank(self) -> bool:
        return self.met_hits.get("Frank", 0) > 0

    @property
    def met_oswald(self) -> bool:
        return self.met_hits.get("Oswald", 0) > 0

    @property
    def met_gus(self) -> bool:
        return self.met_hits.get("Grimy Gus", 0) > 0

    @property
    def met_vinnie(self) -> bool:
        return self.met_hits.get("Vinnie", 0) > 0

    @property
    def met_witch(self) -> bool:
        return self.met_hits.get("Witch", 0) > 0

    @property
    def saw_all_three_mechanics(self) -> bool:
        return (
            self.met_hits.get("Tom Event", 0) > 0
            and self.met_hits.get("Frank Event", 0) > 0
            and self.met_hits.get("Oswald Event", 0) > 0
        )

    @property
    def visited_pawn(self) -> bool:
        return self.location_hits.get("shop:pawn_shop", 0) > 0

    @property
    def visited_loan_shark(self) -> bool:
        return self.location_hits.get("shop:loan_shark", 0) > 0

    @property
    def visited_witch_doctor(self) -> bool:
        return self.location_hits.get("doctor:witch", 0) > 0

    @property
    def visited_tom(self) -> bool:
        return self.location_hits.get("mechanic:tom", 0) > 0

    @property
    def visited_frank(self) -> bool:
        return self.location_hits.get("mechanic:frank", 0) > 0

    @property
    def visited_oswald(self) -> bool:
        return self.location_hits.get("mechanic:oswald", 0) > 0

    @property
    def unlocked_marvin(self) -> bool:
        return self.has_map or self.has_worn_map or self.visited_marvin

    @property
    def marvin_access(self) -> bool:
        return self.has_map or self.has_worn_map or self.visited_marvin

    @property
    def visited_airport(self) -> bool:
        return self.location_hits.get("shop:airport", 0) > 0

    @property
    def won_millionaire_ending(self) -> bool:
        return self.millionaire_visited and self.visited_airport

    @property
    def visited_upgrade(self) -> bool:
        return self.location_hits.get("shop:car_workbench", 0) > 0 or self.location_hits.get("mechanic:oswald", 0) > 0

    @property
    def has_tool_kit(self) -> bool:
        return "Tool Kit" in self.inventory

    @property
    def visited_car_workbench(self) -> bool:
        return self.location_hits.get("shop:car_workbench", 0) > 0

    @property
    def visited_adventure(self) -> bool:
        return any(name.startswith("adventure:") for name in self.location_hits)

    @property
    def companion_acquired(self) -> bool:
        """True if any companion was befriended during this run."""
        befriended = self.item_impacts.get("companions_befriended", {}).get("count", 0)
        if befriended > 0:
            return True
        # Also check the final companions list and statistics parsed from the run
        return False

    @property
    def crafting_used(self) -> bool:
        """True if the player crafted at least one item at the workbench."""
        _known_crafted = {
            "Shiv", "Slingshot", "Road Flare Torch", "Pepper Spray",
            "Improvised Trap", "Car Alarm Rigging", "Snare Trap",
            "Home Remedy", "Wound Salve", "Splint", "Smelling Salts",
            "Lockpick Set", "Fishing Rod", "Binocular Scope", "Signal Mirror",
            "Lucky Charm Bracelet", "Dream Catcher", "Worry Stone",
            "Rain Collector", "Emergency Blanket", "Smoke Signal Kit",
            "Fire Starter Kit", "Water Purifier",
            "Companion Bed", "Pet Toy", "Feeding Station",
        }
        return bool(_known_crafted.intersection(self.inventory))

    @property
    def won_mechanic_ending(self) -> bool:
        """True if the player reached the millionaire state and visited their mechanic."""
        if not self.millionaire_reached:
            return False
        return self.visited_tom or self.visited_frank or self.visited_oswald

    @property
    def won_any_ending(self) -> bool:
        return self.won_millionaire_ending or self.won_mechanic_ending

    @property
    def terminal_ending_name(self) -> str:
        match = re.search(r"\| ending: ([a-z0-9_]+)", self.result_note.lower())
        return match.group(1) if match else ""

    @property
    def display_outcome(self) -> str:
        if self.outcome == "ending" and self.terminal_ending_name:
            return self.terminal_ending_name
        return self.outcome

    @property
    def doctor_likely_saveable(self) -> bool:
        if self.outcome != "died":
            return False

        cause = self.death_cause.lower()
        immediately_fatal = [
            "gunshot", "shot", "executed", "hostage", "loan sharks", "overdose", "fentanyl",
            "professional", "casino", "mauled", "explosion", "electrocution", "drowned in your car",
            "nightmares are real", "carbon monoxide", "jumped from the bridge",
        ]
        if any(fragment in cause for fragment in immediately_fatal):
            return False

        doctor_keywords = [
            "doctor sooner", "infection", "pneumonia", "immune system", "appendicitis", "sepsis",
            "kidney", "tetanus", "rabies", "internal bleeding", "organ failure", "wounds",
            "gallbladder", "pancreatitis", "dehydration", "malnutrition",
        ]
        if any(fragment in cause for fragment in doctor_keywords):
            return True

        if self.death_group in {"illness injury", "heart attack"} and (self.statuses or self.injuries):
            return True
        if len(self.statuses) >= 3 or len(self.injuries) >= 2:
            return True
        return False

    @property
    def coverage_flags(self) -> str:
        flags = []
        if self.visited_doctor:
            flags.append("D")
        if self.visited_store:
            flags.append("C")
        if self.unlocked_marvin:
            flags.append("P")
        if self.met_gus:
            flags.append("g")
        if self.met_vinnie:
            flags.append("v")
        if self.met_witch:
            flags.append("w")
        if self.met_tom:
            flags.append("t")
        if self.met_frank:
            flags.append("f")
        if self.met_oswald:
            flags.append("o")
        if self.visited_pawn:
            flags.append("G")
        if self.visited_loan_shark:
            flags.append("L")
        if self.visited_witch_doctor:
            flags.append("W")
        if self.visited_marvin:
            flags.append("M")
        if self.visited_tom:
            flags.append("T")
        if self.visited_frank:
            flags.append("F")
        if self.visited_oswald:
            flags.append("O")
        if self.visited_upgrade:
            flags.append("U")
        if self.visited_adventure:
            flags.append("A")
        if self.crafting_used:
            flags.append("K")
        if self.companion_acquired:
            flags.append("Q")
        if self.won_mechanic_ending:
            flags.append("E")
        if self.won_millionaire_ending:
            flags.append("$")
        return "".join(flags) if flags else "-"

    @property
    def outcome(self) -> str:
        note = self.result_note.lower()
        if self.timed_out:
            return "timeout"
        if "player died" in note:
            return "died"
        if "player hit $0" in note:
            return "broke"
        if "stalled during cycle" in note:
            return "stalled"
        if "reached cycle cap" in note:
            return "capped"
        if "terminal ending" in note:
            return "win" if self.won_any_ending else "ending"
        if self.return_code not in (0, None):
            return "crash"
        if note in {"", "missing report"}:
            return "crash"
        return "crash"

    @property
    def survived_run(self) -> bool:
        return self.outcome == "capped"

    @property
    def death_group(self) -> str:
        cause = self.death_cause.lower()
        if not cause:
            return "unknown"
        if "drowned in your car" in cause or "nightmares are real" in cause:
            return "nightmare accident"
        if "gunshot" in cause or "shot" in cause or "casino enforcement" in cause or "executed" in cause or "hostage" in cause:
            return "gun violence"
        if "poisoning" in cause or "overdose" in cause or "fentanyl" in cause:
            return "poisoning overdose"
        if "heart attack" in cause:
            return "heart attack"
        if "pneumonia" in cause or "rabies" in cause or "infection" in cause or "wounds" in cause:
            return "illness injury"
        if "loan sharks" in cause:
            return "loan sharks"
        if "explosion" in cause or "electrocution" in cause or "carbon monoxide" in cause:
            return "car mechanical"
        if "drowned" in cause:
            return "drowning"
        if "mauled" in cause or "dog" in cause:
            return "animal attack"
        if "wrath" in cause or "dealer" in cause:
            return "dealer"
        return self.death_cause

    @property
    def death_tag(self) -> str:
        cause = self.death_cause.lower()
        statuses = {status.lower() for status in self.statuses}
        injuries = {injury.lower() for injury in self.injuries}
        sanity = self.sanity if self.sanity is not None else 100
        day = self.day or 0

        if not cause:
            return "unknown"
        if "drowned in your car" in cause or "nightmares are real" in cause:
            if sanity < 30:
                return "nightmare-drowning-low-sanity"
            return "nightmare-drowning"
        if "loan sharks" in cause:
            return "loan-shark-reprisal"
        if any(fragment in cause for fragment in ["gunshot", "shot", "executed", "hostage"]):
            if "hostage" in cause:
                return "hostage-gun-violence"
            if "casino" in cause:
                return "casino-gunshot"
            return "gun-violence"
        if any(fragment in cause for fragment in ["overdose", "fentanyl"]):
            return "overdose"
        if "heart attack" in cause:
            return "stress-heart-attack"
        if any(fragment in cause for fragment in ["explosion", "electrocution", "carbon monoxide"]):
            return "car-mechanical-fatality"
        if "drowned" in cause:
            return "drowning"
        if any(fragment in cause for fragment in ["mauled", "dog"]):
            return "animal-attack"
        if any(fragment in cause for fragment in ["wrath", "dealer"]):
            return "dealer-reprisal"
        if "succumbed to your wounds" in cause:
            if len(injuries) >= 4:
                return "compound-trauma-collapse"
            if any("infection" in status for status in statuses):
                return "wounds-plus-infection"
            if day <= 15:
                return "early-untreated-wounds"
            if day >= 45:
                return "late-untreated-wounds"
            return "untreated-wounds"
        if any(fragment in cause for fragment in ["infection", "pneumonia", "rabies", "sepsis"]):
            return "infection-collapse"
        if any(fragment in cause for fragment in ["dehydration", "malnutrition", "organ failure", "kidney"]):
            return "medical-collapse"
        if statuses and injuries and any("infection" in status for status in statuses):
            return "trauma-plus-infection-pressure"
        if statuses and any("infection" in status or status in {"pneumonia", "hepatitis", "strep throat", "staph infection"} for status in statuses):
            return "infection-pressure"
        if injuries and any(injury in {"fractured spine", "broken ribs", "broken leg", "punctured lung"} for injury in injuries):
            return "major-injury-pressure"
        return self.death_group.replace(" ", "-")

    @property
    def day_bucket(self) -> str:
        day = self.day or 0
        if day <= 10:
            return "day<=10"
        if day <= 30:
            return "11-30"
        if day <= 60:
            return "31-60"
        if day <= 90:
            return "61-90"
        return "91+"

    @property
    def peak_bucket(self) -> str:
        peak = self.peak_balance or self.balance or 0
        if peak < 100:
            return "peak<100"
        if peak < 200:
            return "100-199"
        if peak < 350:
            return "200-349"
        if peak < 800:
            return "350-799"
        if peak < 2000:
            return "800-1,999"
        if peak < 5000:
            return "2k-4,999"
        return "5k+"


FINAL_RE = re.compile(
    r"^Final\s+Day\s+(?P<day>\d+) \| \$\s*(?P<balance>[0-9,]+) \| HP\s+(?P<health>-?\d+) "
    r"\| SAN\s+(?P<sanity>-?\d+) \| Rank\s+(?P<rank>\d+) \| Alive=(?P<alive>True|False)$",
    re.MULTILINE,
)
RUN_SUMMARY_SEED_RE = re.compile(r"^Run Summary \| cycles_requested=\d+ \| seed=(?P<seed>\d+)$", re.MULTILINE)
PEAK_RE = re.compile(r"^Peak\s+\$\s*(?P<balance>[0-9,]+) \| Rank (?P<rank>\d+)$", re.MULTILINE)
PEAK_DAYS_RE = re.compile(r"^Peak days\s+(?P<days>.+)$", re.MULTILINE)
INVENTORY_RE = re.compile(r"^Inventory\s+(?P<items>.+)$", re.MULTILINE)
RESULT_RE = re.compile(r"^Result\s+(?P<note>.+)$", re.MULTILINE)
ERRORS_RE = re.compile(r"^ERRORS \((?P<count>\d+)\):$", re.MULTILINE)
WARNINGS_RE = re.compile(r"^WARNINGS \((?P<count>\d+)\):$", re.MULTILINE)
DEATH_CAUSE_RE = re.compile(r"^Death cause\s+(?P<cause>.+)$", re.MULTILINE)
INJURIES_RE = re.compile(r"^Injuries\s+(?P<items>.+)$", re.MULTILINE)
STATUSES_RE = re.compile(r"^Status\s+(?P<items>.+)$", re.MULTILINE)
PAWNED_ITEMS_RE = re.compile(r"^Pawned items\s+(?P<items>.+)$", re.MULTILINE)
ACTIVE_STORYLINES_RE = re.compile(r"^Storylines active\s+(?P<items>.+)$", re.MULTILINE)
COMPLETED_STORYLINES_RE = re.compile(r"^Storylines completed\s+(?P<items>.+)$", re.MULTILINE)
FAILED_STORYLINES_RE = re.compile(r"^Storylines failed\s+(?P<items>.+)$", re.MULTILINE)
STATE_DELTA_RE = re.compile(
    r"^State\s+\$\s*[0-9,]+ -> [0-9,]+ \((?P<cash>[+-]\$[0-9,]+)\) \| "
    r"HP\s+-?\d+ -> -?\d+ \((?P<health>[+-]\d+)\) \| "
    r"SAN\s+-?\d+ -> -?\d+ \((?P<sanity>[+-]\d+)\) \| "
    r"Rank\s+-?\d+ -> -?\d+ \| Car [YN]$"
)
EVENTS_LINE_RE = re.compile(r"^Events\s+(?P<events>.+)$")
CYCLE_HEADER_RE = re.compile(r"^Cycle\s+\d+\s+\|\s+Day\s+(?P<day>\d+)$")
CHANGES_LINE_RE = re.compile(r"^Changes\s+(?P<changes>.+)$")
CHANGE_FRAGMENT_RE = re.compile(r"^(?P<sign>[+-])(?P<kind>[a-z_]+)=(?P<items>.+)$")
MARVIN_PROVENANCE_RE = re.compile(
    r"^item=(?P<item>.+?); bought=(?P<bought>.*?); used=(?P<used>.*?); removed=(?P<removed>.*?); broken=(?P<broken>.*?); fixed=(?P<fixed>.*)$"
)


SHOP_ROWS = [
    ("Doctor", lambda result: result.ever_had_car or result.visited_doctor, "doctor"),
    ("Witch Doctor", lambda result: result.met_witch or result.visited_witch_doctor, "doctor:witch"),
    ("Convenience Store", lambda result: result.ever_had_car or result.visited_store, "shop:convenience_store"),
    ("Pawn Shop", lambda result: result.met_gus or result.visited_pawn, "shop:pawn_shop"),
    ("Loan Shark", lambda result: result.met_vinnie or result.visited_loan_shark, "shop:loan_shark"),
    ("Marvin", lambda result: result.marvin_access, "shop:marvin"),
    ("Tom", lambda result: result.met_tom or result.visited_tom, "mechanic:tom"),
    ("Frank", lambda result: result.met_frank or result.visited_frank, "mechanic:frank"),
    ("Oswald", lambda result: result.met_oswald or result.visited_oswald, "mechanic:oswald"),
    ("Car Access", lambda result: result.ever_had_car, "shop:convenience_store"),
    ("Car Workbench", lambda result: result.has_tool_kit or result.visited_upgrade, "shop:car_workbench"),
    ("Crafting", lambda result: result.crafting_used, "shop:car_workbench"),
    ("Companion", lambda result: result.companion_acquired, "companion"),
    ("Airport", lambda result: result.millionaire_reached or result.visited_airport, "shop:airport"),
]

ADVENTURE_ROWS = [
    ("Road", "adventure:road"),
    ("Woodlands", "adventure:woodlands"),
    ("Swamp", "adventure:swamp"),
    ("Beach", "adventure:beach"),
    ("Ocean Depths", "adventure:ocean_depths"),
    ("City", "adventure:city"),
]

_LITERAL_UNIVERSE_CACHE: dict[tuple[str, ...], tuple[str, ...]] = {}
_NAMED_UNIVERSE_CACHE: dict[str, tuple[str, ...]] = {}


def _story_python_files() -> list[str]:
    story_root = os.path.join(ROOT, "story")
    file_paths: list[str] = []
    for dir_path, _dir_names, file_names in os.walk(story_root):
        for file_name in file_names:
            if file_name.endswith(".py"):
                file_paths.append(os.path.join(dir_path, file_name))
    file_paths.sort()
    return file_paths


def _literal_call_universe(*method_names: str) -> tuple[str, ...]:
    cache_key = tuple(sorted(set(method_names)))
    cached = _LITERAL_UNIVERSE_CACHE.get(cache_key)
    if cached is not None:
        return cached

    class _LiteralCollector(ast.NodeVisitor):
        def __init__(self, method_set: set[str]):
            self.method_set = method_set
            self.values: set[str] = set()

        def visit_Call(self, node: ast.Call) -> None:
            method_name = None
            if isinstance(node.func, ast.Attribute):
                method_name = node.func.attr
            elif isinstance(node.func, ast.Name):
                method_name = node.func.id

            if method_name in self.method_set and node.args:
                first_arg = node.args[0]
                if isinstance(first_arg, ast.Constant) and isinstance(first_arg.value, str):
                    value = first_arg.value.strip()
                    if value:
                        self.values.add(value)

            self.generic_visit(node)

    collected: set[str] = set()
    for file_path in _story_python_files():
        try:
            with open(file_path, "r", encoding="utf-8") as handle:
                tree = ast.parse(handle.read(), filename=file_path)
        except (OSError, SyntaxError, UnicodeDecodeError):
            continue
        collector = _LiteralCollector(set(cache_key))
        collector.visit(tree)
        collected.update(collector.values)

    cached_result = tuple(sorted(collected, key=str.casefold))
    _LITERAL_UNIVERSE_CACHE[cache_key] = cached_result
    return cached_result


def _known_item_universe() -> tuple[str, ...]:
    return _literal_call_universe("add_item", "remove_item", "break_item", "repair_item", "fix_item")


def _known_status_universe() -> tuple[str, ...]:
    return _literal_call_universe("add_status", "remove_status")


def _known_injury_universe() -> tuple[str, ...]:
    return _literal_call_universe("add_injury", "heal_injury")


def _known_storyline_universe() -> tuple[str, ...]:
    cached = _NAMED_UNIVERSE_CACHE.get("storylines")
    if cached is not None:
        return cached

    storylines_path = os.path.join(ROOT, "story", "storylines.py")
    try:
        with open(storylines_path, "r", encoding="utf-8") as handle:
            tree = ast.parse(handle.read(), filename=storylines_path)
    except (OSError, SyntaxError, UnicodeDecodeError):
        return ()

    class _StorylineCollector(ast.NodeVisitor):
        def __init__(self) -> None:
            self.values: list[str] = []

        def visit_Assign(self, node: ast.Assign) -> None:
            for target in node.targets:
                if isinstance(target, ast.Attribute) and target.attr == "storylines" and isinstance(node.value, ast.Dict):
                    values = []
                    for key in node.value.keys:
                        if isinstance(key, ast.Constant) and isinstance(key.value, str):
                            value = key.value.strip()
                            if value:
                                values.append(value)
                    if values:
                        self.values = values
            self.generic_visit(node)

    collector = _StorylineCollector()
    collector.visit(tree)
    result = tuple(sorted(dict.fromkeys(collector.values), key=str.casefold))
    _NAMED_UNIVERSE_CACHE["storylines"] = result
    return result


def _known_gus_collectible_universe() -> tuple[str, ...]:
    cached = _NAMED_UNIVERSE_CACHE.get("gus_collectibles")
    if cached is not None:
        return cached

    player_core_path = os.path.join(ROOT, "story", "player_core.py")
    try:
        with open(player_core_path, "r", encoding="utf-8") as handle:
            tree = ast.parse(handle.read(), filename=player_core_path)
    except (OSError, SyntaxError, UnicodeDecodeError):
        return ()

    class _CollectibleCollector(ast.NodeVisitor):
        def __init__(self) -> None:
            self.values: list[str] = []

        def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
            if node.name != "get_all_collectibles_list":
                self.generic_visit(node)
                return
            for child in ast.walk(node):
                if isinstance(child, ast.Return) and isinstance(child.value, ast.List):
                    values = []
                    for elt in child.value.elts:
                        if isinstance(elt, ast.Constant) and isinstance(elt.value, str):
                            value = elt.value.strip()
                            if value:
                                values.append(value)
                    if values:
                        self.values = values
                        return
            self.generic_visit(node)

    collector = _CollectibleCollector()
    collector.visit(tree)
    result = tuple(sorted(dict.fromkeys(collector.values), key=str.casefold))
    _NAMED_UNIVERSE_CACHE["gus_collectibles"] = result
    return result


def _known_companion_universe() -> tuple[str, ...]:
    lists_path = os.path.join(ROOT, "lists.py")
    try:
        with open(lists_path, "r", encoding="utf-8") as handle:
            tree = ast.parse(handle.read(), filename=lists_path)
    except (OSError, SyntaxError, UnicodeDecodeError):
        return ()

    for node in ast.walk(tree):
        if not isinstance(node, ast.FunctionDef) or node.name != "make_companion_types":
            continue
        for child in ast.walk(node):
            if not isinstance(child, ast.Return) or not isinstance(child.value, ast.Dict):
                continue
            names = []
            for key in child.value.keys:
                if isinstance(key, ast.Constant) and isinstance(key.value, str):
                    names.append(key.value)
            if names:
                return tuple(sorted(names, key=str.casefold))
    return ()


def _history_entries_for_sources(
    entries: list[tuple[int | None, str]], source_prefixes: tuple[str, ...]
) -> list[tuple[int | None, str]]:
    return [
        (day, source)
        for day, source in entries
        if any(str(source).startswith(prefix) for prefix in source_prefixes)
    ]


def _format_average(total: int, count: int, *, money: bool = False) -> str:
    if count <= 0:
        return "-"
    average = total / count
    if money:
        return f"{average:+.1f}"
    return f"{average:+.1f}"


def _truncate_text(value: str, limit: int) -> str:
    if len(value) <= limit:
        return value
    return value[: max(0, limit - 3)] + "..."


def _parse_literal_list(raw_value: str) -> list[str]:
    try:
        parsed = ast.literal_eval(raw_value.strip())
    except (SyntaxError, ValueError):
        return []
    if not isinstance(parsed, list):
        return []
    return [str(item) for item in parsed]


def _parse_signed_money(raw_value: str) -> int:
    text = raw_value.strip()
    sign = -1 if text.startswith("-") else 1
    digits = text.lstrip("+-").replace("$", "").replace(",", "")
    return sign * int(digits)


def _parse_history_entries(raw_value: str) -> list[tuple[int | None, str]]:
    text = raw_value.strip()
    if not text or text == "-":
        return []
    entries: list[tuple[int | None, str]] = []
    for fragment in [part.strip() for part in text.split(",") if part.strip()]:
        if "@" not in fragment:
            entries.append((None, fragment))
            continue
        day_text, source = fragment.split("@", 1)
        entries.append((None if day_text == "?" else int(day_text), source))
    return entries


def _apply_json_report(result: RunResult, payload: dict[str, object]) -> None:
    run_summary = payload.get("run_summary", {}) if isinstance(payload, dict) else {}
    final_state = payload.get("final_state", {}) if isinstance(payload, dict) else {}
    event_distribution = payload.get("event_distribution", {}) if isinstance(payload, dict) else {}
    decision_summary = payload.get("decision_summary", {}) if isinstance(payload, dict) else {}
    early_mechanic_funnel = payload.get("early_mechanic_funnel", {}) if isinstance(payload, dict) else {}

    if isinstance(run_summary, dict):
        result.day = run_summary.get("day", result.day)
        result.balance = run_summary.get("balance", result.balance)
        result.health = run_summary.get("health", result.health)
        result.sanity = run_summary.get("sanity", result.sanity)
        result.rank = run_summary.get("rank", result.rank)
        result.alive = run_summary.get("alive", result.alive)
        result.peak_balance = run_summary.get("peak_balance", result.peak_balance)
        result.peak_rank = run_summary.get("peak_rank", result.peak_rank)
        result.peak_balance_days = list(run_summary.get("peak_days", result.peak_balance_days) or [])
        result.ever_had_car = bool(run_summary.get("ever_had_car", result.ever_had_car))
        result.has_map = bool(run_summary.get("has_map", result.has_map))
        result.has_worn_map = bool(run_summary.get("has_worn_map", result.has_worn_map))
        result.millionaire_reached = bool(run_summary.get("millionaire_reached", result.millionaire_reached))
        result.millionaire_visited = bool(run_summary.get("millionaire_visited", result.millionaire_visited))
        result.death_cause = str(run_summary.get("death_cause", result.death_cause) or "")
        result_note = str(run_summary.get("result_note", "") or "")
        if result_note:
            result.result_note = result_note

    if isinstance(final_state, dict):
        result.inventory = [str(item) for item in final_state.get("inventory", result.inventory) or []]
        result.has_car = bool(final_state.get("has_car", result.has_car))
        result.injuries = [str(item) for item in final_state.get("injuries", result.injuries) or []]
        result.statuses = [str(item) for item in final_state.get("statuses", result.statuses) or []]
        result.pawned_items = [str(item) for item in final_state.get("pawned_items", result.pawned_items) or []]
        result.active_storylines = [str(item) for item in final_state.get("active_storylines", result.active_storylines) or []]
        result.completed_storylines = [str(item) for item in final_state.get("completed_storylines", result.completed_storylines) or []]
        result.failed_storylines = [str(item) for item in final_state.get("failed_storylines", result.failed_storylines) or []]

    if isinstance(early_mechanic_funnel, dict):
        result.early_mechanic_day_limit = int(early_mechanic_funnel.get("day_limit", result.early_mechanic_day_limit))
        result.early_mechanic_threshold = int(early_mechanic_funnel.get("threshold", result.early_mechanic_threshold))
        peak_balance = early_mechanic_funnel.get("peak_balance", result.early_mechanic_peak_balance)
        result.early_mechanic_peak_balance = None if peak_balance is None else int(peak_balance)
        result.early_mechanic_peak_days = [int(day) for day in early_mechanic_funnel.get("peak_days", result.early_mechanic_peak_days) or []]
        balance_end = early_mechanic_funnel.get("balance_end", result.early_mechanic_balance_end)
        result.early_mechanic_balance_end = None if balance_end is None else int(balance_end)
        result.early_mechanic_reached_threshold = bool(early_mechanic_funnel.get("reached_threshold", result.early_mechanic_reached_threshold))
        first_day_reached = early_mechanic_funnel.get("first_day_reached_threshold", result.early_mechanic_first_day_reached)
        result.early_mechanic_first_day_reached = None if first_day_reached is None else int(first_day_reached)
        result.early_mechanic_offer_count = int(early_mechanic_funnel.get("mechanic_offer_count", result.early_mechanic_offer_count))
        result.early_mechanic_affordable_offer_count = int(early_mechanic_funnel.get("mechanic_affordable_offer_count", result.early_mechanic_affordable_offer_count))
        result.early_mechanic_accept_count = int(early_mechanic_funnel.get("mechanic_accept_count", result.early_mechanic_accept_count))
        first_offer_day = early_mechanic_funnel.get("first_offer_day", result.early_mechanic_first_offer_day)
        result.early_mechanic_first_offer_day = None if first_offer_day is None else int(first_offer_day)
        first_accept_day = early_mechanic_funnel.get("first_accept_day", result.early_mechanic_first_accept_day)
        result.early_mechanic_first_accept_day = None if first_accept_day is None else int(first_accept_day)
        result.early_route_interrupt_count = int(early_mechanic_funnel.get("route_interrupt_count", result.early_route_interrupt_count))
        result.early_medical_interrupt_count = int(early_mechanic_funnel.get("medical_interrupt_count", result.early_medical_interrupt_count))
        result.early_route_applied_count = int(early_mechanic_funnel.get("route_applied_count", result.early_route_applied_count))
        result.early_route_suppressed_count = int(early_mechanic_funnel.get("route_suppressed_count", result.early_route_suppressed_count))

    if isinstance(event_distribution, dict):
        met_hits = event_distribution.get("met")
        location_hits = event_distribution.get("location")
        if isinstance(met_hits, dict):
            result.met_hits = {str(name): int(count) for name, count in met_hits.items()}
        if isinstance(location_hits, dict):
            result.location_hits = {str(name): int(count) for name, count in location_hits.items()}
            if result.location_hits:
                top_name = max(result.location_hits.items(), key=lambda item: (item[1], item[0]))[0]
                if top_name.startswith("adventure:"):
                    result.top_adventure = top_name.removeprefix("adventure:")
                else:
                    result.top_location = top_name

    if isinstance(payload.get("mechanic_decisions"), list):
        result.mechanic_decisions = list(payload["mechanic_decisions"])
    if isinstance(payload.get("fallback_decisions"), dict):
        result.fallback_decisions = {str(label): int(count) for label, count in payload["fallback_decisions"].items()}
    if isinstance(payload.get("event_polarity"), dict):
        result.event_polarity = {str(label): int(count) for label, count in payload["event_polarity"].items()}
    if isinstance(payload.get("item_impacts"), dict):
        result.item_impacts = {
            str(item_name): {
                "hits": int(stats.get("hits", 0)),
                "positive": int(stats.get("positive", 0)),
                "negative": int(stats.get("negative", 0)),
                "neutral": int(stats.get("neutral", 0)),
                "cash": int(stats.get("cash", 0)),
                "health": int(stats.get("health", 0)),
                "sanity": int(stats.get("sanity", 0)),
            }
            for item_name, stats in payload["item_impacts"].items()
            if isinstance(stats, dict)
        }
    if isinstance(payload.get("item_provenance"), dict):
        result.item_provenance = {
            str(item_name): {
                key: [
                    (
                        None if entry.get("day") is None else int(entry.get("day")),
                        str(entry.get("source", "unknown")),
                    )
                    for entry in entries
                    if isinstance(entry, dict)
                ]
                for key, entries in history.items()
                if isinstance(entries, list)
            }
            for item_name, history in payload["item_provenance"].items()
            if isinstance(history, dict)
        }
    if isinstance(payload.get("marvin_provenance"), dict):
        result.marvin_item_provenance = {
            str(item_name): {
                dest_key: [
                    (entry.get("day"), str(entry.get("source", "unknown")))
                    for entry in history.get(src_key, [])
                    if isinstance(entry, dict)
                ]
                for src_key, dest_key in [
                    ("acquired", "bought"),
                    ("used", "used"),
                    ("removed", "removed"),
                    ("broken", "broken"),
                    ("fixed", "fixed"),
                    ("repairing", "repairing"),
                ]
            }
            for item_name, history in payload["marvin_provenance"].items()
            if isinstance(history, dict)
        }

    if isinstance(decision_summary, dict):
        request_counts = decision_summary.get("request_counts")
        request_context_counts = decision_summary.get("request_context_counts")
        trace_request_counts = decision_summary.get("trace_request_counts")
        trace_context_counts = decision_summary.get("trace_context_counts")
        goal_counts = decision_summary.get("goal_counts")
        personality_counts = decision_summary.get("personality_counts")
        reason_code_counts = decision_summary.get("reason_code_counts")
        expected_value_summary = decision_summary.get("expected_value_summary")
        route_outcome_counts = decision_summary.get("route_outcome_counts")
        route_interrupt_kind_counts = decision_summary.get("route_interrupt_kind_counts")
        route_interrupted_goal_counts = decision_summary.get("route_interrupted_goal_counts")
        route_interrupted_top_goal_counts = decision_summary.get("route_interrupted_top_goal_counts")
        route_applied_goal_counts = decision_summary.get("route_applied_goal_counts")
        route_suppressed_goal_counts = decision_summary.get("route_suppressed_goal_counts")
        if isinstance(request_counts, dict):
            result.decision_request_counts = {str(name): int(count) for name, count in request_counts.items()}
        if isinstance(request_context_counts, dict):
            result.decision_request_context_counts = {str(name): int(count) for name, count in request_context_counts.items()}
        if isinstance(trace_request_counts, dict):
            result.decision_trace_counts = {str(name): int(count) for name, count in trace_request_counts.items()}
        if isinstance(trace_context_counts, dict):
            result.decision_trace_context_counts = {str(name): int(count) for name, count in trace_context_counts.items()}
        if isinstance(goal_counts, dict):
            result.decision_goal_counts = {str(name): int(count) for name, count in goal_counts.items()}
        if isinstance(personality_counts, dict):
            result.decision_personality_counts = {str(name): int(count) for name, count in personality_counts.items()}
        if isinstance(reason_code_counts, dict):
            result.decision_reason_code_counts = {str(name): int(count) for name, count in reason_code_counts.items()}
        if isinstance(expected_value_summary, dict):
            ev_avg = expected_value_summary.get("avg")
            ev_max = expected_value_summary.get("max")
            ev_min = expected_value_summary.get("min")
            if isinstance(ev_avg, (int, float)):
                result.decision_expected_value_avg = float(ev_avg)
            if isinstance(ev_max, (int, float)):
                result.decision_expected_value_max = float(ev_max)
            if isinstance(ev_min, (int, float)):
                result.decision_expected_value_min = float(ev_min)
        if isinstance(route_outcome_counts, dict):
            result.route_outcome_counts = {str(name): int(count) for name, count in route_outcome_counts.items()}
        if isinstance(route_interrupt_kind_counts, dict):
            result.route_interrupt_kind_counts = {str(name): int(count) for name, count in route_interrupt_kind_counts.items()}
        if isinstance(route_interrupted_goal_counts, dict):
            result.route_interrupted_goal_counts = {str(name): int(count) for name, count in route_interrupted_goal_counts.items()}
        if isinstance(route_interrupted_top_goal_counts, dict):
            result.route_interrupted_top_goal_counts = {str(name): int(count) for name, count in route_interrupted_top_goal_counts.items()}
        if isinstance(route_applied_goal_counts, dict):
            result.route_applied_goal_counts = {str(name): int(count) for name, count in route_applied_goal_counts.items()}
        if isinstance(route_suppressed_goal_counts, dict):
            result.route_suppressed_goal_counts = {str(name): int(count) for name, count in route_suppressed_goal_counts.items()}

    if isinstance(payload.get("errors"), list):
        result.error_count = len(payload["errors"])
    if isinstance(payload.get("warnings"), list):
        result.warning_count = len(payload["warnings"])

    if isinstance(payload.get("final_state"), dict):
        fs = payload["final_state"]
        if isinstance(fs.get("statistics"), dict):
            result.game_statistics = {str(k): int(v) for k, v in fs["statistics"].items()}
        if isinstance(fs.get("gambling"), dict):
            result.gambling_statistics = {str(k): int(v) for k, v in fs["gambling"].items()}
        if isinstance(fs.get("companions"), list):
            result.companions_list = [str(c) for c in fs["companions"]]
        if isinstance(fs.get("broken_items"), list):
            result.broken_items_list = [str(i) for i in fs["broken_items"]]
        if isinstance(fs.get("repairing_items"), list):
            result.repairing_items_list = [str(i) for i in fs["repairing_items"]]
        if isinstance(fs.get("dealer_happiness"), (int, float)):
            result.dealer_happiness = int(fs["dealer_happiness"])
        result.gift_system_unlocked = bool(fs.get("gift_system_unlocked", result.gift_system_unlocked))
        result.has_wrapped_gift = bool(fs.get("has_wrapped_gift", result.has_wrapped_gift))
        if isinstance(fs.get("store_purchases"), (int, float)):
            result.store_purchases = int(fs["store_purchases"])
        if isinstance(fs.get("loan_shark_debt"), (int, float)):
            result.loan_shark_debt = int(fs["loan_shark_debt"])
        if isinstance(fs.get("loan_shark_warning_level"), (int, float)):
            result.loan_shark_warning_level = int(fs["loan_shark_warning_level"])
        if isinstance(fs.get("fraudulent_cash"), (int, float)):
            result.fraudulent_cash = int(fs["fraudulent_cash"])
        if isinstance(fs.get("gus_items_sold_count"), (int, float)):
            result.gus_items_sold_count = int(fs["gus_items_sold_count"])
        if isinstance(fs.get("gus_total_collectibles"), (int, float)):
            result.gus_total_collectibles = int(fs["gus_total_collectibles"])

    if isinstance(payload.get("flask_purchases"), dict):
        result.flask_purchases = {str(k): int(v) for k, v in payload["flask_purchases"].items()}
    if isinstance(payload.get("items_ever_broken"), dict):
        result.items_ever_broken = {str(k): int(v) for k, v in payload["items_ever_broken"].items()}
    if isinstance(payload.get("gift_deliveries"), list):
        result.gift_deliveries = [
            {
                "day": None if entry.get("day") is None else int(entry.get("day")),
                "cycle": None if entry.get("cycle") is None else int(entry.get("cycle")),
                "item": str(entry.get("item", "")),
                "happiness_before": None if entry.get("happiness_before") is None else int(entry.get("happiness_before")),
                "happiness_after": None if entry.get("happiness_after") is None else int(entry.get("happiness_after")),
                "happiness_change": None if entry.get("happiness_change") is None else int(entry.get("happiness_change")),
                "alive_after": bool(entry.get("alive_after", True)),
            }
            for entry in payload["gift_deliveries"]
            if isinstance(entry, dict)
        ]
    if isinstance(payload.get("dealer_free_hands"), list):
        result.dealer_free_hands = [
            {
                "day": None if entry.get("day") is None else int(entry.get("day")),
                "cycle": None if entry.get("cycle") is None else int(entry.get("cycle")),
                "dealer_happiness": int(entry.get("dealer_happiness", 0)),
                "bet": int(entry.get("bet", 0)),
                "balance": int(entry.get("balance", 0)),
                "tier": str(entry.get("tier", "unknown")),
            }
            for entry in payload["dealer_free_hands"]
            if isinstance(entry, dict)
        ]
    if isinstance(payload.get("final_state"), dict):
        fs = payload["final_state"]
        if isinstance(fs.get("mechanic_dreams"), dict):
            dreams = fs["mechanic_dreams"]
            result.mechanic_dreams = {
                "tom": int(dreams.get("tom", 0)),
                "frank": int(dreams.get("frank", 0)),
                "oswald": int(dreams.get("oswald", 0)),
                "car_mechanic": str(dreams.get("car_mechanic", "") or ""),
                "chosen": str(dreams.get("chosen", "") or ""),
            }
        if isinstance(fs.get("companion_details"), dict):
            result.companion_details = {
                str(name): {
                    "status": str(data.get("status", "unknown")),
                    "type": str(data.get("type", "unknown")),
                    "happiness": int(data.get("happiness", 0)),
                    "days_owned": int(data.get("days_owned", 0)),
                    "fed_today": bool(data.get("fed_today", False)),
                    "bonded": bool(data.get("bonded", False)),
                }
                for name, data in fs["companion_details"].items()
                if isinstance(data, dict)
            }


def _record_cycle_event_effects(result: RunResult, lines: list[str]) -> None:
    pending_deltas: tuple[int, int, int] | None = None

    for raw_line in lines:
        line = raw_line.strip()
        state_match = STATE_DELTA_RE.match(line)
        if state_match:
            pending_deltas = (
                _parse_signed_money(state_match.group("cash")),
                int(state_match.group("health")),
                int(state_match.group("sanity")),
            )
            continue

        events_match = EVENTS_LINE_RE.match(line)
        if not events_match or pending_deltas is None:
            continue

        events_text = events_match.group("events").strip()
        pending_deltas_local = pending_deltas
        pending_deltas = None
        if events_text == "none captured":
            continue

        events = [event.strip() for event in events_text.split(",") if event.strip()]
        if not events:
            continue

        share = float(len(events))
        cash_delta, health_delta, sanity_delta = pending_deltas_local
        for event_name in events:
            entry = result.event_effects.setdefault(
                event_name,
                {"hits": 0.0, "cash": 0.0, "health": 0.0, "sanity": 0.0},
            )
            entry["hits"] += 1.0
            entry["cash"] += cash_delta / share
            entry["health"] += health_delta / share
            entry["sanity"] += sanity_delta / share


def _parse_cycle_records(lines: list[str]) -> list[CycleRecord]:
    records: list[CycleRecord] = []
    current: CycleRecord | None = None

    for raw_line in lines:
        line = raw_line.strip()
        cycle_match = CYCLE_HEADER_RE.match(line)
        if cycle_match:
            if current is not None:
                records.append(current)
            current = CycleRecord(day=int(cycle_match.group("day")))
            continue

        if current is None:
            continue

        state_match = STATE_DELTA_RE.match(line)
        if state_match:
            current.cash_delta = _parse_signed_money(state_match.group("cash"))
            current.health_delta = int(state_match.group("health"))
            current.sanity_delta = int(state_match.group("sanity"))
            continue

        events_match = EVENTS_LINE_RE.match(line)
        if events_match:
            events_text = events_match.group("events").strip()
            if events_text != "none captured":
                current.events = [event.strip() for event in events_text.split(",") if event.strip()]
            continue

        changes_match = CHANGES_LINE_RE.match(line)
        if not changes_match:
            continue

        changes_text = changes_match.group("changes").strip()
        if changes_text == "none":
            continue

        for fragment in [part.strip() for part in changes_text.split(" | ") if part.strip()]:
            fragment_match = CHANGE_FRAGMENT_RE.match(fragment)
            if not fragment_match:
                continue
            kind = fragment_match.group("kind")
            items = _parse_literal_list(fragment_match.group("items"))
            if not items:
                continue
            is_added = fragment_match.group("sign") == "+"
            if kind == "injuries":
                target = current.injuries_added if is_added else current.injuries_removed
                target.extend(items)
            elif kind == "status":
                target = current.statuses_added if is_added else current.statuses_removed
                target.extend(items)

    if current is not None:
        records.append(current)
    return records


def parse_args() -> tuple[int, list[int], str]:
    cycles = int(sys.argv[1]) if len(sys.argv) > 1 else 300
    if len(sys.argv) > 2 and str(sys.argv[2]).lower() in {"random", "rand"}:
        total_runs = int(sys.argv[3]) if len(sys.argv) > 3 else 100
        if total_runs <= 0:
            raise ValueError("random batch size must be positive")
        seed_pool = range(1, 2_147_483_647)
        system_random = random.SystemRandom()
        seeds = system_random.sample(seed_pool, total_runs)
        return cycles, seeds, f"random/{total_runs}"

    start_seed = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    end_seed = int(sys.argv[3]) if len(sys.argv) > 3 else 100
    if end_seed < start_seed:
        start_seed, end_seed = end_seed, start_seed
    seeds = list(range(start_seed, end_seed + 1))
    return cycles, seeds, f"{start_seed}-{end_seed}"


def parse_report(seed: int, return_code: int) -> RunResult:
    result = RunResult(seed=seed, return_code=return_code)

    try:
        with open(REPORT_JSON, "r", encoding="utf-8") as json_handle:
            payload = json.load(json_handle)
        if isinstance(payload, dict):
            payload_seed = payload.get("seed")
            if payload_seed != seed:
                payload = None
            else:
                _apply_json_report(result, payload)
    except FileNotFoundError:
        payload = None
    except (json.JSONDecodeError, OSError, ValueError):
        payload = None

    if return_code not in (0, None):
        result.result_note = f"runner exited with code {return_code}"
        return result

    try:
        with open(REPORT, "r", encoding="utf-8") as handle:
            text = handle.read()
    except FileNotFoundError:
        result.result_note = "missing report"
        return result

    report_seed_match = RUN_SUMMARY_SEED_RE.search(text)
    if report_seed_match is not None and int(report_seed_match.group("seed")) != seed:
        result.result_note = f"stale report seed mismatch (expected {seed})"
        return result

    final_match = FINAL_RE.search(text)
    if final_match:
        result.day = int(final_match.group("day"))
        result.balance = int(final_match.group("balance").replace(",", ""))
        result.health = int(final_match.group("health"))
        result.sanity = int(final_match.group("sanity"))
        result.rank = int(final_match.group("rank"))
        result.alive = final_match.group("alive") == "True"

    peak_match = PEAK_RE.search(text)
    if peak_match:
        result.peak_balance = int(peak_match.group("balance").replace(",", ""))
        result.peak_rank = int(peak_match.group("rank"))

    peak_days_match = PEAK_DAYS_RE.search(text)
    if peak_days_match:
        result.peak_balance_days = [
            int(day.strip())
            for day in peak_days_match.group("days").split(",")
            if day.strip().isdigit()
        ]

    inventory_match = INVENTORY_RE.search(text)
    if inventory_match:
        result.inventory = _parse_literal_list(inventory_match.group("items"))

    result.has_car = "Has car            True" in text
    result.ever_had_car = "Ever had car       True" in text or result.has_car
    result.has_map = "Has map            True" in text or re.search(r"^Inventory\s+.*'Map'", text, re.MULTILINE) is not None
    result.has_worn_map = "Has worn map       True" in text or re.search(r"^Inventory\s+.*'Worn Map'", text, re.MULTILINE) is not None
    result.millionaire_reached = "Millionaire reached True" in text or (result.peak_balance or 0) >= 1000000
    result.millionaire_visited = "Millionaire visited True" in text

    death_cause_match = DEATH_CAUSE_RE.search(text)
    if death_cause_match:
        cause = death_cause_match.group("cause").strip()
        result.death_cause = "" if cause == "None" else cause

    injuries_match = INJURIES_RE.search(text)
    if injuries_match:
        result.injuries = _parse_literal_list(injuries_match.group("items"))

    statuses_match = STATUSES_RE.search(text)
    if statuses_match:
        result.statuses = _parse_literal_list(statuses_match.group("items"))

    pawned_items_match = PAWNED_ITEMS_RE.search(text)
    if pawned_items_match:
        result.pawned_items = _parse_literal_list(pawned_items_match.group("items"))

    active_storylines_match = ACTIVE_STORYLINES_RE.search(text)
    if active_storylines_match:
        result.active_storylines = _parse_literal_list(active_storylines_match.group("items"))

    completed_storylines_match = COMPLETED_STORYLINES_RE.search(text)
    if completed_storylines_match:
        result.completed_storylines = _parse_literal_list(completed_storylines_match.group("items"))

    failed_storylines_match = FAILED_STORYLINES_RE.search(text)
    if failed_storylines_match:
        result.failed_storylines = _parse_literal_list(failed_storylines_match.group("items"))

    lines = text.splitlines()
    _record_cycle_event_effects(result, lines)
    result.cycle_records = _parse_cycle_records(lines)
    for index, line in enumerate(lines):
        if line == "Mechanic intro decisions":
            for offset in range(index + 1, len(lines)):
                decision_line = lines[offset].strip()
                if not decision_line:
                    break
                if decision_line == "none":
                    break
                match = re.match(
                    r"^day=(?P<day>\?|\d+) mechanic=(?P<mechanic>\S+) cost=(?P<cost>\?|\$[\d,]+) balance=(?P<balance>\?|\$[\d,]+) answer=(?P<answer>\w+) source=(?P<source>\w+)$",
                    decision_line,
                )
                if not match:
                    continue
                day_text = match.group("day")
                cost_text = match.group("cost")
                balance_text = match.group("balance")
                result.mechanic_decisions.append(
                    {
                        "day": None if day_text == "?" else int(day_text),
                        "mechanic": match.group("mechanic"),
                        "cost": None if cost_text == "?" else int(cost_text.replace("$", "").replace(",", "")),
                        "balance": None if balance_text == "?" else int(balance_text.replace("$", "").replace(",", "")),
                        "answer": match.group("answer"),
                        "source": match.group("source"),
                    }
                )

        if line == "Fallback decisions":
            for offset in range(index + 1, len(lines)):
                fallback_line = lines[offset].strip()
                if not fallback_line:
                    break
                if fallback_line == "none":
                    break
                match = re.match(r"^(?P<count>\d+)\s+(?P<label>.+)$", fallback_line)
                if not match:
                    continue
                result.fallback_decisions[match.group("label")] = int(match.group("count"))

        if line == "Event polarity":
            for offset in range(index + 1, len(lines)):
                polarity_line = lines[offset].strip()
                if not polarity_line:
                    break
                match = re.match(r"^(?P<label>positive|negative|neutral)\s+(?P<count>\d+)$", polarity_line)
                if not match:
                    continue
                result.event_polarity[match.group("label")] = int(match.group("count"))

        if line == "Item impact":
            for offset in range(index + 1, len(lines)):
                impact_line = lines[offset].strip()
                if not impact_line:
                    break
                if impact_line == "none":
                    break
                match = re.match(
                    r"^(?P<item>.+?) hits=(?P<hits>-?\d+) pos=(?P<pos>-?\d+) neg=(?P<neg>-?\d+) neu=(?P<neu>-?\d+) cash=(?P<cash>[+-]?\d+) hp=(?P<hp>[+-]?\d+) san=(?P<san>[+-]?\d+)$",
                    impact_line,
                )
                if not match:
                    continue
                result.item_impacts[match.group("item")] = {
                    "hits": int(match.group("hits")),
                    "positive": int(match.group("pos")),
                    "negative": int(match.group("neg")),
                    "neutral": int(match.group("neu")),
                    "cash": int(match.group("cash")),
                    "health": int(match.group("hp")),
                    "sanity": int(match.group("san")),
                }

        if line == "Marvin provenance":
            for offset in range(index + 1, len(lines)):
                provenance_line = lines[offset].strip()
                if not provenance_line:
                    break
                if provenance_line == "none":
                    break
                match = MARVIN_PROVENANCE_RE.match(provenance_line)
                if not match:
                    continue
                result.marvin_item_provenance[match.group("item")] = {
                    "bought": _parse_history_entries(match.group("bought")),
                    "used": _parse_history_entries(match.group("used")),
                    "removed": _parse_history_entries(match.group("removed")),
                    "broken": _parse_history_entries(match.group("broken")),
                    "fixed": _parse_history_entries(match.group("fixed")),
                }

        if line == "Event Distribution | met":
            for offset in range(index + 1, len(lines)):
                met_line = lines[offset].strip()
                if not met_line:
                    break
                if met_line == "none":
                    break
                match = re.match(r"^(?P<count>\d+)\s+(?P<name>.+)$", met_line)
                if not match:
                    continue
                result.met_hits[match.group("name")] = int(match.group("count"))

        if line == "Event Distribution | location":
            for offset in range(index + 1, len(lines)):
                location_line = lines[offset].strip()
                if not location_line:
                    break
                if location_line == "none":
                    break
                match = re.match(r"^(?P<count>\d+)\s+(?P<name>.+)$", location_line)
                if not match:
                    continue
                result.location_hits[match.group("name")] = int(match.group("count"))

            if result.location_hits:
                top_name = max(result.location_hits.items(), key=lambda item: (item[1], item[0]))[0]
                if top_name.startswith("adventure:"):
                    result.top_adventure = top_name.removeprefix("adventure:")
                else:
                    result.top_location = top_name
            break

    result_match = RESULT_RE.search(text)
    if result_match:
        result.result_note = result_match.group("note")

    if "NO ERRORS" in text:
        result.error_count = 0
    else:
        errors_match = ERRORS_RE.search(text)
        if errors_match:
            result.error_count = int(errors_match.group("count"))

    if "NO WARNINGS" in text:
        result.warning_count = 0
    else:
        warnings_match = WARNINGS_RE.search(text)
        if warnings_match:
            result.warning_count = int(warnings_match.group("count"))

    return result
def _supports_stop_key() -> bool:
    return bool(msvcrt and sys.stdin.isatty() and sys.stdout.isatty())


def _consume_stop_request() -> bool:
    if not _supports_stop_key() or msvcrt is None:
        return False

    stop_requested = False
    while msvcrt.kbhit():
        char = msvcrt.getwch()
        if char and char.lower() == STOP_KEY:
            stop_requested = True
    return stop_requested


def _terminate_seed_process(process: subprocess.Popen[str]) -> None:
    if process.poll() is not None:
        return

    process.terminate()
    try:
        process.communicate(timeout=2)
    except subprocess.TimeoutExpired:
        process.kill()
        process.communicate()


def _clear_report_artifacts() -> None:
    for path in (REPORT, REPORT_JSON, STORY_OUT):
        try:
            os.remove(path)
        except FileNotFoundError:
            continue
        except OSError:
            continue


def run_seed(cycles: int, seed: int, timeout_seconds: int = 90) -> tuple[RunResult | None, bool]:
    started_at = time.perf_counter()
    _clear_report_artifacts()
    child_env = os.environ.copy()
    child_env["QUICKTEST_CYCLES"] = str(cycles)
    process = subprocess.Popen(
            [sys.executable, "-m", "tools.quicktest", str(seed)],
            cwd=ROOT,
            env=child_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
    try:
        while True:
            if _consume_stop_request():
                _terminate_seed_process(process)
                return None, True

            try:
                stdout, stderr = process.communicate(timeout=STOP_POLL_SECONDS)
                if process.returncode not in (0, None):
                    result = RunResult(
                        seed=seed,
                        return_code=process.returncode,
                        elapsed_seconds=time.perf_counter() - started_at,
                        result_note=(stderr.strip() or stdout.strip() or f"runner exited with code {process.returncode}"),
                    )
                    return result, False
                result = parse_report(seed, process.returncode)
                result.elapsed_seconds = time.perf_counter() - started_at
                return result, False
            except subprocess.TimeoutExpired:
                if (time.perf_counter() - started_at) >= timeout_seconds:
                    _terminate_seed_process(process)
                    return RunResult(
                        seed=seed,
                        timed_out=True,
                        elapsed_seconds=time.perf_counter() - started_at,
                        result_note=f"timeout>{timeout_seconds}s",
                    ), False
    finally:
        if process.poll() is None:
            _terminate_seed_process(process)


def _progress_line(index: int, total: int, result: RunResult, results: list[RunResult], started_at: float) -> str:
    batch_elapsed = time.perf_counter() - started_at
    average_seed_time = batch_elapsed / index if index else 0.0
    eta_seconds = max(0.0, average_seed_time * (total - index))
    percent = (index / total) * 100 if total else 100.0

    summary = _collect_summary(results)
    outcome = result.outcome
    if outcome == "capped":
        outcome = "cap"

    day = str(result.day) if result.day is not None else "-"
    end_balance = _format_int(result.balance)
    peak_balance = _format_int(result.peak_balance)
    current_rank = result.rank if result.rank is not None else 0
    peak_rank = result.peak_rank if result.peak_rank is not None else current_rank
    coverage = result.coverage_flags
    coverage_display = coverage if len(coverage) <= 8 else coverage[:8] + "+"

    detail = ""
    if result.timed_out:
        detail = " timeout"
    elif result.outcome == "died":
        detail = f" {result.death_group}"
        if result.doctor_likely_saveable and not result.visited_doctor:
            detail += "/missed-doc"
    elif result.outcome == "broke":
        detail = " bankroll-zero"
    elif result.outcome == "win":
        detail = " win"
    elif result.outcome == "ending":
        detail = f" ending:{result.terminal_ending_name}" if result.terminal_ending_name else " ending"
    elif result.outcome == "stalled":
        detail = " stalled"
    elif result.outcome == "capped":
        detail = " cycle-cap"
    elif result.outcome == "crash":
        detail = " crash"
    elif result.visited_marvin:
        detail = " marvin"

    return (
        f"[{index}/{total} {percent:4.0f}% eta={eta_seconds:4.0f}s] "
        f"s={result.seed} {outcome}{detail} d={day} end$={end_balance} peak$={peak_balance} "
        f"r={current_rank}/{peak_rank} cov={coverage_display} t={result.elapsed_seconds:.1f}s "
        f"roll w={summary['win']} e={summary['ending']} d={summary['died']} b={summary['broke']} c={summary['capped']} x={summary['crash']} "
        f"r1={summary['rank1']} m={summary['marvin']} i={summary['marvin_items']}"
    )


def _live_result_label(result: RunResult) -> str:
    outcome = result.outcome
    if outcome == "capped":
        outcome = "cap"
    if result.timed_out:
        return f"{outcome}:timeout"
    if result.outcome == "died":
        if result.doctor_likely_saveable and not result.visited_doctor:
            return f"{outcome}:{result.death_group}/missed-doc"
        return f"{outcome}:{result.death_group}"
    if result.outcome == "broke":
        return "broke:zero"
    if result.outcome == "ending":
        return f"ending:{result.terminal_ending_name}" if result.terminal_ending_name else "ending"
    if result.outcome == "stalled":
        return "stalled"
    if result.outcome == "crash":
        return "crash"
    if result.visited_marvin:
        return f"{outcome}:marvin"
    return outcome


def _recent_result_rows(results: list[RunResult], limit: int = 10) -> list[str]:
    rows: list[str] = []
    for result in results[-limit:]:
        day = str(result.day) if result.day is not None else "-"
        end_balance = _format_int(result.balance)
        peak_balance = _format_int(result.peak_balance)
        current_rank = result.rank if result.rank is not None else 0
        peak_rank = result.peak_rank if result.peak_rank is not None else current_rank
        rows.append(
            f"{result.seed:>6}  {_live_result_label(result):<24} day={day:>3} end$={end_balance:>8} "
            f"peak$={peak_balance:>8} rank={current_rank}/{peak_rank} t={result.elapsed_seconds:>4.1f}s"
        )
    return rows


def _top_money_rows(results: list[RunResult], limit: int = 5) -> list[str]:
    ordered = sorted(
        results,
        key=lambda result: (
            (result.peak_balance or result.balance or 0),
            (result.day or 0),
            -(result.seed),
        ),
        reverse=True,
    )[:limit]
    rows: list[str] = []
    for index, result in enumerate(ordered, start=1):
        peak_balance = _format_int(result.peak_balance or result.balance)
        end_balance = _format_int(result.balance)
        rows.append(
            f"{index}. seed={result.seed:<6} peak$={peak_balance:>8} end$={end_balance:>8} "
            f"day={str(result.day or '-'):>3} rank={result.peak_rank or result.rank or 0}"
        )
    return rows or ["(no runs yet)"]


def _top_length_rows(results: list[RunResult], limit: int = 5) -> list[str]:
    ordered = sorted(
        results,
        key=lambda result: (
            (result.day or 0),
            (result.peak_balance or result.balance or 0),
            -(result.seed),
        ),
        reverse=True,
    )[:limit]
    rows: list[str] = []
    for index, result in enumerate(ordered, start=1):
        peak_balance = _format_int(result.peak_balance or result.balance)
        end_balance = _format_int(result.balance)
        rows.append(
            f"{index}. seed={result.seed:<6} day={str(result.day or '-'):>3} peak$={peak_balance:>8} "
            f"end$={end_balance:>8} rank={result.peak_rank or result.rank or 0}"
        )
    return rows or ["(no runs yet)"]


def _render_live_dashboard(index: int, total: int, results: list[RunResult], started_at: float) -> str:
    batch_elapsed = time.perf_counter() - started_at
    average_seed_time = batch_elapsed / index if index else 0.0
    eta_seconds = max(0.0, average_seed_time * (total - index))
    percent = (index / total) * 100 if total else 100.0
    summary = _collect_summary(results)

    lines = [
        f"AUTOTEST progress  {index}/{total}  {percent:5.1f}%  elapsed={batch_elapsed:6.1f}s  eta={eta_seconds:6.1f}s",
        (
            "Outcomes  "
            f"win={summary['win']}  ending={summary['ending']}  died={summary['died']}  broke={summary['broke']}  "
            f"capped={summary['capped']}  crash={summary['crash']}  timeout={summary['timeouts']}"
        ),
        (
            "Progress  "
            f"car={summary['car']}/{summary['total']}  rank1+={summary['rank1']}/{summary['total']}  "
            f"marvin={summary['marvin']}/{summary['total']}  marvin_items={summary['marvin_items']}/{summary['total']}  "
            f"doctor_missed={summary['doctor_missed']}"
        ),
        "",
        "Recent 10 Runs",
        "--------------",
        *(_recent_result_rows(results, 10) or ["(no completed runs yet)"]),
        "",
        "Top 5 By Peak Money",
        "-------------------",
        *_top_money_rows(results, 5),
        "",
        "Top 5 By Run Length",
        "-------------------",
        *_top_length_rows(results, 5),
    ]
    return "\n".join(lines)


def _should_emit_non_tty_progress(index: int, total: int, result: RunResult) -> bool:
    if index <= 3 or index >= total:
        return True
    if result.timed_out or result.outcome in {"crash", "stalled"}:
        return True
    if total <= 20:
        return True
    if total <= 100:
        step = 5
    elif total <= 250:
        step = 10
    else:
        step = 25
    return index % step == 0


def _render_live_progress(index: int, total: int, result: RunResult, results: list[RunResult], started_at: float) -> None:
    if not sys.stdout.isatty():
        if _should_emit_non_tty_progress(index, total, result):
            print(_progress_line(index, total, result, results, started_at), flush=True)
        return

    sys.stdout.write("\x1b[2J\x1b[H")
    sys.stdout.write(_render_live_dashboard(index, total, results, started_at))
    sys.stdout.write("\n")
    sys.stdout.flush()


def _collect_summary(results: list[RunResult]) -> dict[str, int]:
    total = len(results)
    return {
        "total": total,
        "win": sum(1 for result in results if result.outcome == "win"),
        "died": sum(1 for result in results if result.outcome == "died"),
        "broke": sum(1 for result in results if result.outcome == "broke"),
        "ending": sum(1 for result in results if result.outcome == "ending"),
        "stalled": sum(1 for result in results if result.outcome == "stalled"),
        "capped": sum(1 for result in results if result.outcome == "capped"),
        "crash": sum(1 for result in results if result.outcome == "crash"),
        "car": sum(1 for result in results if result.has_car),
        "ever_car": sum(1 for result in results if result.ever_had_car),
        "location": sum(1 for result in results if result.reached_location),
        "rank1": sum(1 for result in results if (result.peak_rank or result.rank or 0) >= 1),
        "doctor": sum(1 for result in results if result.visited_doctor),
        "witch_access": sum(1 for result in results if result.met_witch),
        "witch_doctor": sum(1 for result in results if result.visited_witch_doctor),
        "store": sum(1 for result in results if result.visited_store),
        "map": sum(1 for result in results if result.has_map),
        "worn_map": sum(1 for result in results if result.has_worn_map),
        "marvin_access": sum(1 for result in results if result.marvin_access),
        "gus_access": sum(1 for result in results if result.met_gus),
        "vinnie_access": sum(1 for result in results if result.met_vinnie),
        "tom_access": sum(1 for result in results if result.met_tom),
        "frank_access": sum(1 for result in results if result.met_frank),
        "oswald_access": sum(1 for result in results if result.met_oswald),
        "pawn": sum(1 for result in results if result.visited_pawn),
        "loan": sum(1 for result in results if result.visited_loan_shark),
        "million": sum(1 for result in results if result.millionaire_reached),
        "airport_win": sum(1 for result in results if result.won_millionaire_ending),
        "mechanic_end": sum(1 for result in results if result.won_mechanic_ending),
        "airport": sum(1 for result in results if result.visited_airport),
        "marvin": sum(1 for result in results if result.visited_marvin),
        "marvin_items": sum(1 for result in results if result.marvin_item_provenance),
        "tom": sum(1 for result in results if result.visited_tom),
        "frank": sum(1 for result in results if result.visited_frank),
        "oswald": sum(1 for result in results if result.visited_oswald),
        "upgrade": sum(1 for result in results if result.visited_upgrade),
        "gift_unlock": sum(1 for result in results if result.gift_system_unlocked),
        "wrapped_gift": sum(1 for result in results if result.has_wrapped_gift),
        "workbench_unlock": sum(1 for result in results if result.has_tool_kit),
        "workbench_visit": sum(1 for result in results if result.visited_car_workbench),
        "crafting": sum(1 for result in results if result.crafting_used),
        "companion": sum(1 for result in results if result.companion_acquired),
        "companion_roster": sum(1 for result in results if bool(result.companions_list)),
        "adventure": sum(1 for result in results if result.visited_adventure),
        "survived": sum(1 for result in results if result.survived_run),
        "doctor_missed": sum(1 for result in results if result.doctor_likely_saveable and not result.visited_doctor),
        "timeouts": sum(1 for result in results if result.outcome == "timeout"),
        "clean": sum(1 for result in results if result.error_count == 0 and result.warning_count == 0 and not result.timed_out),
    }


def _format_peak_days(days: list[int]) -> str:
    if not days:
        return "-"
    label = ",".join(str(day) for day in days)
    return label if len(label) <= 11 else label[:8] + "..."


def _format_int(value: int | None) -> str:
    if value is None:
        return "-"
    return f"{value:,}"


def _build_text_table(
    headers: list[tuple[str, str]],
    rows: list[dict[str, str]],
    alignments: dict[str, str] | None = None,
) -> list[str]:
    alignments = alignments or {}
    widths = {
        key: max(len(label), *(len(row.get(key, "")) for row in rows))
        for key, label in headers
    }

    def render_row(row: dict[str, str]) -> str:
        parts = []
        for key, _label in headers:
            value = row.get(key, "")
            width = widths[key]
            align = alignments.get(key, "left")
            if align == "right":
                parts.append(value.rjust(width))
            elif align == "center":
                parts.append(value.center(width))
            else:
                parts.append(value.ljust(width))
        return " ".join(parts)

    separator = " ".join("-" * widths[key] for key, _label in headers)
    return [
        render_row({key: label for key, label in headers}),
        separator,
        *(render_row(row) for row in rows),
    ]


def _render_distribution_chart(
    title: str,
    buckets: list[tuple[str, int]],
    total: int,
    width: int = 24,
) -> list[str]:
    lines = [title]
    for label, count in buckets:
        filled = 0 if total <= 0 or count <= 0 else max(1, round((count / total) * width))
        filled = min(width, filled)
        bar = "#" * filled + "." * (width - filled)
        lines.append(f"{label:<11} {count:>3}/{total:<3} {bar}")
    return lines


def _distribution_lines(results: list[RunResult]) -> list[str]:
    if not results:
        return []

    total = len(results)

    def peak_of(result: RunResult) -> int:
        return result.peak_balance or result.balance or 0

    def day_of(result: RunResult) -> int:
        return result.day or 0

    def peak_rank_of(result: RunResult) -> int:
        return result.peak_rank if result.peak_rank is not None else (result.rank or 0)

    peak_buckets = [
        ("peak<100", sum(1 for result in results if peak_of(result) < 100)),
        ("100-199", sum(1 for result in results if 100 <= peak_of(result) < 200)),
        ("200-349", sum(1 for result in results if 200 <= peak_of(result) < 350)),
        ("350-799", sum(1 for result in results if 350 <= peak_of(result) < 800)),
        ("800-1,999", sum(1 for result in results if 800 <= peak_of(result) < 2000)),
        ("2k-4,999", sum(1 for result in results if 2000 <= peak_of(result) < 5000)),
        ("5k-9,999", sum(1 for result in results if 5000 <= peak_of(result) < 10000)),
        ("10k-19k", sum(1 for result in results if 10000 <= peak_of(result) < 20000)),
        ("20k-49k", sum(1 for result in results if 20000 <= peak_of(result) < 50000)),
        ("50k-99k", sum(1 for result in results if 50000 <= peak_of(result) < 100000)),
        ("100k-249k", sum(1 for result in results if 100000 <= peak_of(result) < 250000)),
        ("250k-399k", sum(1 for result in results if 250000 <= peak_of(result) < 400000)),
        ("400k-749k", sum(1 for result in results if 400000 <= peak_of(result) < 750000)),
        ("750k-999k", sum(1 for result in results if 750000 <= peak_of(result) < 1000000)),
        ("1m+", sum(1 for result in results if peak_of(result) >= 1000000)),
    ]
    day_buckets = [
        ("day<=10", sum(1 for result in results if day_of(result) <= 10)),
        ("11-30", sum(1 for result in results if 11 <= day_of(result) <= 30)),
        ("31-60", sum(1 for result in results if 31 <= day_of(result) <= 60)),
        ("61-90", sum(1 for result in results if 61 <= day_of(result) <= 90)),
        ("91+", sum(1 for result in results if day_of(result) >= 91)),
    ]
    peak_rank_buckets = [
        ("rank=0", sum(1 for result in results if peak_rank_of(result) == 0)),
        ("rank=1", sum(1 for result in results if peak_rank_of(result) == 1)),
        ("rank=2", sum(1 for result in results if peak_rank_of(result) == 2)),
        ("rank=3", sum(1 for result in results if peak_rank_of(result) == 3)),
        ("rank=4", sum(1 for result in results if peak_rank_of(result) == 4)),
        ("rank>=5", sum(1 for result in results if peak_rank_of(result) >= 5)),
    ]

    lines = ["Distributions"]
    lines.extend(_render_distribution_chart("Peak balance", peak_buckets, total))
    lines.append("")
    lines.extend(_render_distribution_chart("Peak rank", peak_rank_buckets, total))
    lines.append("")
    lines.extend(_render_distribution_chart("Run length", day_buckets, total))
    lines.append("")
    return lines


def _medical_economy_lines(results: list[RunResult]) -> list[str]:
    if not results:
        return []

    cohorts = [
        ("doctor-any", [result for result in results if result.visited_doctor]),
        (
            "witch-only",
            [result for result in results if result.visited_witch_doctor and not result.visited_doctor],
        ),
        (
            "no-medical",
            [result for result in results if not result.visited_doctor and not result.visited_witch_doctor],
        ),
    ]

    def average(values: list[int]) -> int:
        return round(sum(values) / len(values)) if values else 0

    rows = []
    total = len(results)
    for label, cohort in cohorts:
        peak_values = [result.peak_balance or result.balance or 0 for result in cohort]
        end_values = [result.balance or 0 for result in cohort]
        day_values = [result.day or 0 for result in cohort]
        rows.append({
            "cohort": label,
            "runs": f"{len(cohort)}/{total}",
            "survived": str(sum(1 for result in cohort if result.survived_run)),
            "peak_avg": _format_int(average(peak_values)),
            "peak_2k": str(sum(1 for result in cohort if (result.peak_balance or result.balance or 0) >= 2000)),
            "end_avg": _format_int(average(end_values)),
            "day_avg": str(average(day_values)),
            "doctor_missed": str(sum(1 for result in cohort if result.doctor_likely_saveable and not result.visited_doctor)),
        })

    lines = ["Medical Cohorts"]
    lines.extend(_build_text_table(
        [
            ("cohort", "cohort"),
            ("runs", "runs"),
            ("survived", "survived"),
            ("peak_avg", "avg-peak$"),
            ("peak_2k", "2k+"),
            ("end_avg", "avg-end$"),
            ("day_avg", "avg-day"),
            ("doctor_missed", "missed"),
        ],
        rows,
        {
            "runs": "right",
            "survived": "right",
            "peak_avg": "right",
            "peak_2k": "right",
            "end_avg": "right",
            "day_avg": "right",
            "doctor_missed": "right",
        },
    ))
    lines.append("")
    return lines


def _max_rank_cohort_lines(results: list[RunResult]) -> list[str]:
    if not results:
        return []

    def average(values: list[int]) -> int:
        return round(sum(values) / len(values)) if values else 0

    def max_rank(result: RunResult) -> int:
        return result.peak_rank if result.peak_rank is not None else (result.rank or 0)

    def render_counter(counter: Counter[str], limit: int = 3) -> str:
        if not counter:
            return "none"
        return " | ".join(f"{name}={count}" for name, count in counter.most_common(limit))

    total = len(results)
    grouped: dict[int, list[RunResult]] = {}
    for result in results:
        grouped.setdefault(max_rank(result), []).append(result)

    rows = []
    detail_lines: list[str] = []
    for rank_value in sorted(grouped):
        cohort = grouped[rank_value]
        size = len(cohort)
        peak_values = [result.peak_balance or result.balance or 0 for result in cohort]
        end_values = [result.balance or 0 for result in cohort]
        day_values = [result.day or 0 for result in cohort]
        rows.append({
            "cohort": f"rank{rank_value}",
            "runs": f"{size}/{total}",
            "survived": f"{sum(1 for result in cohort if result.survived_run)}/{size}",
            "peak_avg": _format_int(average(peak_values)),
            "end_avg": _format_int(average(end_values)),
            "day_avg": str(average(day_values)),
            "ever_car": f"{sum(1 for result in cohort if result.ever_had_car)}/{size}",
            "doctor": f"{sum(1 for result in cohort if result.visited_doctor)}/{size}",
            "marvin": f"{sum(1 for result in cohort if result.visited_marvin)}/{size}",
            "pawn": f"{sum(1 for result in cohort if result.visited_pawn)}/{size}",
            "loan": f"{sum(1 for result in cohort if result.visited_loan_shark)}/{size}",
            "witch": f"{sum(1 for result in cohort if result.visited_witch_doctor)}/{size}",
        })

        route_counter = Counter(
            result.top_adventure if result.top_adventure != "none" else result.top_location
            for result in cohort
        )
        outcome_counter = Counter(result.display_outcome for result in cohort)
        death_counter = Counter(result.death_tag for result in cohort if result.outcome == "died")
        detail_lines.append(
            f"common rank{rank_value} outcomes {render_counter(outcome_counter)}"
        )
        detail_lines.append(
            f"common rank{rank_value} routes   {render_counter(route_counter)}"
        )
        detail_lines.append(
            f"common rank{rank_value} deaths   {render_counter(death_counter)}"
        )

    lines = ["Max Rank Cohorts"]
    lines.extend(_build_text_table(
        [
            ("cohort", "cohort"),
            ("runs", "runs"),
            ("survived", "survived"),
            ("peak_avg", "avg-peak$"),
            ("end_avg", "avg-end$"),
            ("day_avg", "avg-day"),
            ("ever_car", "ever-car"),
            ("doctor", "doctor"),
            ("marvin", "marvin"),
            ("pawn", "pawn"),
            ("loan", "loan"),
            ("witch", "witchdr"),
        ],
        rows,
        {
            "runs": "right",
            "survived": "right",
            "peak_avg": "right",
            "end_avg": "right",
            "day_avg": "right",
            "ever_car": "right",
            "doctor": "right",
            "marvin": "right",
            "pawn": "right",
            "loan": "right",
            "witch": "right",
        },
    ))
    lines.extend(detail_lines)
    lines.append("")
    return lines


def _shop_summary_lines(results: list[RunResult]) -> list[str]:
    total = len(results)
    lines = [
        "Shop Summary",
        "shop              unlocked-runs visited-runs total-visits",
        "----------------- ------------- ------------ ------------",
    ]
    for shop_name, unlock_rule, visit_label in SHOP_ROWS:
        unlocked_runs = sum(1 for result in results if unlock_rule(result))
        visited_runs = sum(1 for result in results if result.location_hits.get(visit_label, 0) > 0)
        total_visits = sum(result.location_hits.get(visit_label, 0) for result in results)
        lines.append(
            f"{shop_name:<17} {unlocked_runs:>13}/{total:<2} {visited_runs:>12}/{total:<2} {total_visits:>12}"
        )
    lines.append("note: ALL locations (including Doctor) require a car. Car Workbench additionally requires a Tool Kit.")
    lines.append("")
    return lines


def _doctor_review_lines(results: list[RunResult]) -> list[str]:
    missed = [result for result in results if result.doctor_likely_saveable and not result.visited_doctor]
    if not missed:
        return []

    lines = [
        "Doctor Review",
        "seed cause-group        hp san statuses injuries cause",
        "---- ------------------ -- --- -------- -------- ------------------------------------------",
    ]
    for result in missed[:12]:
        cause = result.death_cause or "Unknown"
        if len(cause) > 42:
            cause = cause[:39] + "..."
        lines.append(
            f"{result.seed:>4} {result.death_group[:18]:<18} "
            f"{(result.health if result.health is not None else '-'):>2} "
            f"{(result.sanity if result.sanity is not None else '-'):>3} "
            f"{len(result.statuses):>8} {len(result.injuries):>8} {cause}"
        )
    lines.append("")
    return lines


def _pawned_item_lines(results: list[RunResult]) -> list[str]:
    total = len(results)
    known_items = list(_known_gus_collectible_universe())
    observed_items = sorted(
        {item for result in results for item in result.pawned_items},
        key=str.casefold,
    )
    if not known_items:
        known_items = observed_items
    else:
        extras = [item for item in observed_items if item not in known_items]
        known_items.extend(extras)

    if not known_items:
        return []

    pawn_counter = Counter(item for result in results for item in result.pawned_items)
    pawn_runs = sum(1 for result in results if result.pawned_items)
    max_total_collectibles = max((result.gus_total_collectibles for result in results), default=len(known_items))
    max_seed = max(results, key=lambda result: (result.gus_items_sold_count, result.seed), default=None)
    avg_progress = sum(result.gus_items_sold_count for result in results) / max(1, total)
    rows = []
    for item_name in known_items:
        count = pawn_counter.get(item_name, 0)
        rows.append({
            "item": item_name,
            "runs": f"{count}/{total}",
            "pct": f"{(count / total) * 100:.0f}%",
        })

    lines = [
        f"Pawn Shop / Gus Progress runs-with-sales={pawn_runs}/{total} unique-sold={sum(1 for item in known_items if pawn_counter.get(item, 0) > 0)}/{len(known_items)} "
        f"avg-unique-sold={avg_progress:.1f}/{max_total_collectibles or len(known_items)} "
        f"best-seed={('-' if max_seed is None or max_seed.gus_items_sold_count <= 0 else f's{max_seed.seed}={max_seed.gus_items_sold_count}/{max_seed.gus_total_collectibles or max_total_collectibles}')}",
        f"progress gates 1+={sum(1 for result in results if result.gus_items_sold_count >= 1)}/{total} "
        f"5+={sum(1 for result in results if result.gus_items_sold_count >= 5)}/{total} "
        f"10+={sum(1 for result in results if result.gus_items_sold_count >= 10)}/{total} "
        f"25+={sum(1 for result in results if result.gus_items_sold_count >= 25)}/{total} "
        f"full={sum(1 for result in results if (result.gus_total_collectibles or max_total_collectibles) > 0 and result.gus_items_sold_count >= (result.gus_total_collectibles or max_total_collectibles))}/{total}",
    ]
    lines.extend(_build_text_table(
        [("item", "item"), ("runs", "sold-runs"), ("pct", "sold%")],
        rows,
        {"runs": "right", "pct": "right"},
    ))
    lines.append("")
    return lines


def _event_economy_lines(results: list[RunResult]) -> list[str]:
    aggregate: dict[str, dict[str, float]] = {}
    for result in results:
        for event_name, effect in result.event_effects.items():
            if not event_name.startswith(("day:", "night:", "storyline:")):
                continue
            entry = aggregate.setdefault(
                event_name,
                {"hits": 0.0, "cash": 0.0, "health": 0.0, "sanity": 0.0},
            )
            entry["hits"] += effect.get("hits", 0.0)
            entry["cash"] += effect.get("cash", 0.0)
            entry["health"] += effect.get("health", 0.0)
            entry["sanity"] += effect.get("sanity", 0.0)

    if not aggregate:
        return []

    def render(entries: list[tuple[str, dict[str, float]]], key: str, money: bool = False) -> str:
        parts = []
        for event_name, values in entries[:4]:
            total = values[key]
            hits = max(1.0, values["hits"])
            average = total / hits
            if money:
                total_label = f"{total:+.0f}"
                avg_label = f"{average:+.1f}"
            else:
                total_label = f"{total:+.0f}"
                avg_label = f"{average:+.1f}"
            parts.append(f"{event_name} total={total_label} avg={avg_label} hits={int(hits)}")
        return " | ".join(parts) if parts else "none"

    cash_gains = sorted(
        ((name, values) for name, values in aggregate.items() if values["cash"] > 0),
        key=lambda item: item[1]["cash"],
        reverse=True,
    )
    cash_losses = sorted(
        ((name, values) for name, values in aggregate.items() if values["cash"] < 0),
        key=lambda item: item[1]["cash"],
    )
    health_losses = sorted(
        ((name, values) for name, values in aggregate.items() if values["health"] < 0),
        key=lambda item: item[1]["health"],
    )
    sanity_losses = sorted(
        ((name, values) for name, values in aggregate.items() if values["sanity"] < 0),
        key=lambda item: item[1]["sanity"],
    )

    return [
        "Event Economy",
        f"cash gains   {render(cash_gains, 'cash', money=True)}",
        f"cash losses  {render(cash_losses, 'cash', money=True)}",
        f"health losses {render(health_losses, 'health')}",
        f"sanity losses {render(sanity_losses, 'sanity')}",
        "",
    ]


def _storyline_audit_lines(results: list[RunResult]) -> list[str]:
    total = len(results)
    known_storylines = list(_known_storyline_universe())
    observed_storylines = sorted(
        {
            *{name for result in results for name in result.active_storylines},
            *{name for result in results for name in result.completed_storylines},
            *{name for result in results for name in result.failed_storylines},
        },
        key=str.casefold,
    )
    if not known_storylines:
        known_storylines = observed_storylines
    else:
        extras = [name for name in observed_storylines if name not in known_storylines]
        known_storylines.extend(extras)

    active_counter = Counter(name for result in results for name in result.active_storylines)
    completed_counter = Counter(name for result in results for name in result.completed_storylines)
    failed_counter = Counter(name for result in results for name in result.failed_storylines)

    if not known_storylines and not active_counter and not completed_counter and not failed_counter:
        return []

    rows = []
    for name in known_storylines:
        active = active_counter.get(name, 0)
        completed = completed_counter.get(name, 0)
        failed = failed_counter.get(name, 0)
        touched = sum(
            1
            for result in results
            if name in result.active_storylines or name in result.completed_storylines or name in result.failed_storylines
        )
        rows.append({
            "storyline": name,
            "any": f"{touched}/{total}",
            "completed": f"{completed}/{total}",
            "failed": f"{failed}/{total}",
            "active": f"{active}/{total}",
        })

    lines = [
        f"Storyline Audit touched-any={sum(1 for result in results if result.active_storylines or result.completed_storylines or result.failed_storylines)}/{total} "
        f"completed-any={sum(1 for result in results if result.completed_storylines)}/{total} failed-any={sum(1 for result in results if result.failed_storylines)}/{total}"
    ]
    lines.extend(_build_text_table(
        [
            ("storyline", "storyline"),
            ("any", "any-state"),
            ("completed", "completed"),
            ("failed", "failed"),
            ("active", "active-end"),
        ],
        rows,
        {"any": "right", "completed": "right", "failed": "right", "active": "right"},
    ))
    lines.append("")
    return lines


def _no_car_review_lines(results: list[RunResult]) -> list[str]:
    no_car_results = [result for result in results if not result.has_car]
    if not no_car_results:
        return []

    def peak_bucket(result: RunResult) -> str:
        peak = result.peak_balance or result.balance or 0
        if peak < 100:
            return "peak<100"
        if peak < 200:
            return "peak100-199"
        if peak < 350:
            return "peak200-349"
        if peak < 800:
            return "peak350-799"
        return "peak800+"

    def mechanic_outcome(result: RunResult) -> str:
        decisions = result.mechanic_decisions
        if not decisions:
            return "no mechanic offer"
        if any(decision.get("answer") == "yes" and decision.get("mechanic") == "Frank" for decision in decisions):
            return "Frank accepted no car"
        if any(decision.get("answer") == "yes" and decision.get("mechanic") == "Tom" for decision in decisions):
            return "Tom path no car"
        if any(decision.get("answer") == "yes" and decision.get("mechanic") == "Oswald" for decision in decisions):
            return "Oswald path no car"
        affordable_no = [
            decision for decision in decisions
            if decision.get("answer") == "no"
            and isinstance(decision.get("cost"), int)
            and isinstance(decision.get("balance"), int)
            and int(decision["balance"]) >= int(decision["cost"])
        ]
        if affordable_no:
            return "declined affordable offer"
        return "never had enough for offer"

    bucket_counter = Counter(peak_bucket(result) for result in no_car_results)
    mechanic_counter = Counter(mechanic_outcome(result) for result in no_car_results)
    early_day_limit = max((result.early_mechanic_day_limit for result in no_car_results), default=10)
    early_threshold = max((result.early_mechanic_threshold for result in no_car_results), default=200)
    early_peak_counter = Counter()
    for result in no_car_results:
        peak_balance = result.early_mechanic_peak_balance or result.peak_balance or result.balance or 0
        if peak_balance < 100:
            early_peak_counter["peak<100"] += 1
        elif peak_balance < early_threshold:
            early_peak_counter["peak100-threshold-1"] += 1
        else:
            early_peak_counter[f"peak{early_threshold}+"] += 1
    early_failures = sum(1 for result in no_car_results if (result.day or 0) <= 10)
    mid_failures = sum(1 for result in no_car_results if 11 <= (result.day or 0) <= 30)
    late_failures = sum(1 for result in no_car_results if (result.day or 0) > 30)
    ever_had_then_lost = sum(1 for result in no_car_results if result.ever_had_car)
    saw_all_three_no_car = sum(1 for result in no_car_results if result.saw_all_three_mechanics)
    early_reached_threshold = sum(1 for result in no_car_results if result.early_mechanic_reached_threshold)
    early_offer_runs = sum(1 for result in no_car_results if result.early_mechanic_offer_count > 0)
    early_affordable_offer_runs = sum(1 for result in no_car_results if result.early_mechanic_affordable_offer_count > 0)
    early_accept_runs = sum(1 for result in no_car_results if result.early_mechanic_accept_count > 0)
    early_interrupt_runs = sum(1 for result in no_car_results if result.early_route_interrupt_count > 0)
    early_medical_interrupt_runs = sum(1 for result in no_car_results if result.early_medical_interrupt_count > 0)
    early_suppressed_runs = sum(1 for result in no_car_results if result.early_route_suppressed_count > 0)
    early_applied_runs = sum(1 for result in no_car_results if result.early_route_applied_count > 0)
    early_avg_peak = round(
        sum(result.early_mechanic_peak_balance or result.peak_balance or result.balance or 0 for result in no_car_results) / len(no_car_results)
    )

    lines = [
        f"No-Car Review runs={len(no_car_results)}/{len(results)} early(day<=10)={early_failures} mid(11-30)={mid_failures} late(31+)={late_failures} ever-had-then-lost={ever_had_then_lost} all-three-seen-no-car={saw_all_three_no_car}",
        (
            f"early funnel d<={early_day_limit} threshold={early_threshold} "
            f"reached={early_reached_threshold}/{len(no_car_results)} "
            f"offer-runs={early_offer_runs}/{len(no_car_results)} "
            f"affordable-offer-runs={early_affordable_offer_runs}/{len(no_car_results)} "
            f"accept-runs={early_accept_runs}/{len(no_car_results)} avg_peak={_format_int(early_avg_peak)}"
        ),
        (
            "early route pressure "
            f"interrupt-runs={early_interrupt_runs}/{len(no_car_results)} "
            f"medical-interrupt-runs={early_medical_interrupt_runs}/{len(no_car_results)} "
            f"suppressed-runs={early_suppressed_runs}/{len(no_car_results)} "
            f"applied-runs={early_applied_runs}/{len(no_car_results)} "
            f"peak<100={early_peak_counter['peak<100']} peak100-{early_threshold - 1}={early_peak_counter['peak100-threshold-1']} peak{early_threshold}+={early_peak_counter[f'peak{early_threshold}+']}"
        ),
        "peak-balance buckets " + " ".join(f"{label}={bucket_counter[label]}" for label in ["peak<100", "peak100-199", "peak200-349", "peak350-799", "peak800+"]),
        "mechanic outcomes " + " | ".join(f"{label}={count}" for label, count in mechanic_counter.most_common()),
        "",
    ]
    return lines


def _stagnation_audit_lines(results: list[RunResult]) -> list[str]:
    if not results:
        return []

    def peak_of(result: RunResult) -> int:
        return result.peak_balance or result.balance or 0

    def is_stalled(result: RunResult) -> bool:
        day = result.day or 0
        if day < 20:
            return False
        if (result.peak_rank or result.rank or 0) >= 1:
            return False
        if result.has_car and result.marvin_access and result.visited_marvin:
            return False
        return peak_of(result) < 1000

    stalled = [result for result in results if is_stalled(result)]
    if not stalled:
        return ["Stagnation Audit", "none", ""]

    rows = []
    for label, subset in [
        ("20-39", [result for result in stalled if 20 <= (result.day or 0) <= 39]),
        ("40-69", [result for result in stalled if 40 <= (result.day or 0) <= 69]),
        ("70+", [result for result in stalled if (result.day or 0) >= 70]),
    ]:
        if not subset:
            continue
        rows.append({
            "bucket": label,
            "runs": f"{len(subset)}/{len(results)}",
            "avg_peak": _format_int(round(sum(peak_of(result) for result in subset) / len(subset))),
            "no_car": str(sum(1 for result in subset if not result.has_car)),
            "marvin_access": str(sum(1 for result in subset if result.marvin_access)),
            "marvin_visit": str(sum(1 for result in subset if result.visited_marvin)),
            "doctor": str(sum(1 for result in subset if result.visited_doctor)),
            "loan": str(sum(1 for result in subset if result.visited_loan_shark)),
            "top_deaths": _summarize_counter(Counter(result.death_tag for result in subset if result.outcome == "died"), 3),
        })

    lines = [f"Stagnation Audit stalled-runs={len(stalled)}/{len(results)}"]
    lines.extend(_build_text_table(
        [
            ("bucket", "day-bucket"),
            ("runs", "runs"),
            ("avg_peak", "avg-peak$"),
            ("no_car", "no-car"),
            ("marvin_access", "marvin-access"),
            ("marvin_visit", "marvin-visit"),
            ("doctor", "doctor"),
            ("loan", "loan"),
            ("top_deaths", "top-deaths"),
        ],
        rows,
        {"runs": "right", "avg_peak": "right", "no_car": "right", "marvin_access": "right", "marvin_visit": "right", "doctor": "right", "loan": "right"},
    ))
    lines.append("")
    return lines


def _fallback_review_lines(results: list[RunResult]) -> list[str]:
    aggregate = Counter()
    runs_with_fallbacks = 0
    for result in results:
        if result.fallback_decisions:
            runs_with_fallbacks += 1
            aggregate.update(result.fallback_decisions)

    lines = [f"Fallback Review runs={runs_with_fallbacks}/{len(results)}"]
    if not aggregate:
        lines.extend(["none", ""])
        return lines

    for label, count in aggregate.most_common(12):
        lines.append(f"{label} total={count}")
    lines.append("")
    return lines


def _event_polarity_lines(results: list[RunResult]) -> list[str]:
    total = Counter()
    for result in results:
        total.update(result.event_polarity)

    grand_total = sum(total.values())
    lines = [f"Event Polarity total={grand_total}"]
    if grand_total <= 0:
        lines.extend(["none", ""])
        return lines

    for label in ["positive", "negative", "neutral"]:
        count = total.get(label, 0)
        pct = (count / grand_total) * 100 if grand_total else 0
        lines.append(f"{label}={count} ({pct:.1f}%)")
    lines.append("")
    return lines


def _item_impact_lines(results: list[RunResult]) -> list[str]:
    aggregate: dict[str, dict[str, int]] = {
        item_name: {
            "got": 0,
            "got_runs": 0,
            "used": 0,
            "broken": 0,
            "fixed": 0,
            "hits": 0,
            "positive": 0,
            "negative": 0,
            "neutral": 0,
            "cash": 0,
            "health": 0,
            "sanity": 0,
        }
        for item_name in _known_item_universe()
    }
    for result in results:
        for item_name, stats in result.item_impacts.items():
            entry = aggregate.setdefault(
                item_name,
                {
                    "got": 0,
                    "got_runs": 0,
                    "used": 0,
                    "broken": 0,
                    "fixed": 0,
                    "hits": 0,
                    "positive": 0,
                    "negative": 0,
                    "neutral": 0,
                    "cash": 0,
                    "health": 0,
                    "sanity": 0,
                },
            )
            for key in ["hits", "positive", "negative", "neutral", "cash", "health", "sanity"]:
                entry[key] += int(stats.get(key, 0))

        for item_name, history in result.item_provenance.items():
            entry = aggregate.setdefault(
                item_name,
                {
                    "got": 0,
                    "got_runs": 0,
                    "used": 0,
                    "broken": 0,
                    "fixed": 0,
                    "hits": 0,
                    "positive": 0,
                    "negative": 0,
                    "neutral": 0,
                    "cash": 0,
                    "health": 0,
                    "sanity": 0,
                },
            )
            acquired = history.get("acquired", [])
            used = history.get("used", [])
            broken = history.get("broken", [])
            fixed = history.get("fixed", [])
            entry["got"] += len(acquired)
            entry["used"] += len(used)
            entry["broken"] += len(broken)
            entry["fixed"] += len(fixed)
            if acquired:
                entry["got_runs"] += 1

    if not aggregate:
        return []

    rows = []
    ranked = sorted(
        aggregate.items(),
        key=lambda item: (
            item[1]["got"],
            item[1]["positive"] - item[1]["negative"],
            item[1]["hits"],
            item[1]["cash"],
            item[0],
        ),
        reverse=True,
    )
    total = len(results)
    for item_name, stats in ranked:
        rows.append({
            "item": item_name,
            "got": str(stats["got"]),
            "runs": f"{stats['got_runs']}/{total}",
            "used": str(stats["used"]),
            "brk": str(stats["broken"]),
            "fix": str(stats["fixed"]),
            "hits": str(stats["hits"]),
            "pos": str(stats["positive"]),
            "neg": str(stats["negative"]),
            "neu": str(stats["neutral"]),
            "cash": _format_int(stats["cash"]),
            "hp": str(stats["health"]),
            "san": str(stats["sanity"]),
        })

    lines = ["Item Acquisition & Impact"]
    lines.extend(_build_text_table(
        [
            ("item", "item"),
            ("got", "got"),
            ("runs", "runs"),
            ("used", "used"),
            ("brk", "brk"),
            ("fix", "fix"),
            ("hits", "hits"),
            ("pos", "pos"),
            ("neg", "neg"),
            ("neu", "neu"),
            ("cash", "cash"),
            ("hp", "hp"),
            ("san", "san"),
        ],
        rows,
        {
            "got": "right",
            "runs": "right",
            "used": "right",
            "brk": "right",
            "fix": "right",
            "hits": "right",
            "pos": "right",
            "neg": "right",
            "neu": "right",
            "cash": "right",
            "hp": "right",
            "san": "right",
        },
    ))
    lines.append("")
    return lines


def _collect_medical_provider_summary(results: list[RunResult], event_label: str) -> dict[str, object]:
    location_event = f"location:{event_label}"
    visit_rows: list[dict[str, str]] = []
    healed_counts: Counter[str] = Counter()
    healed_runs: defaultdict[str, set[int]] = defaultdict(set)
    summary: dict[str, object] = {
        "visit_runs": set(),
        "heal_runs": set(),
        "fail_runs": set(),
        "visits": 0,
        "heal_visits": 0,
        "fail_visits": 0,
        "cash_delta": 0,
        "health_delta": 0,
        "sanity_delta": 0,
        "healed_counts": healed_counts,
        "healed_runs": healed_runs,
        "visit_rows": visit_rows,
    }

    for result in results:
        run_visits = 0
        run_heals = 0
        run_fails = 0
        for record in result.cycle_records:
            if location_event not in record.events:
                continue
            run_visits += 1
            summary["visits"] += 1
            summary["cash_delta"] += record.cash_delta
            summary["health_delta"] += record.health_delta
            summary["sanity_delta"] += record.sanity_delta
            cast(set[int], summary["visit_runs"]).add(result.seed)

            healed_conditions = list(record.statuses_removed) + list(record.injuries_removed)
            restorative_visit = bool(
                healed_conditions
                or record.health_delta > 0
                or record.sanity_delta > 0
            )
            if restorative_visit:
                run_heals += 1
                summary["heal_visits"] += 1
                cast(set[int], summary["heal_runs"]).add(result.seed)
                for condition in healed_conditions:
                    healed_counts[condition] += 1
                    healed_runs[condition].add(result.seed)
            else:
                run_fails += 1
                summary["fail_visits"] += 1
                cast(set[int], summary["fail_runs"]).add(result.seed)

        if run_visits:
            visit_rows.append({
                "seed": str(result.seed),
                "visits": str(run_visits),
                "heals": str(run_heals),
                "fails": str(run_fails),
                "outcome": result.outcome,
                "day": str(result.day if result.day is not None else "-"),
                "rank": str(result.rank if result.rank is not None else "-"),
                "end$": _format_int(result.balance),
                "hp": str(result.health if result.health is not None else "-"),
                "san": str(result.sanity if result.sanity is not None else "-"),
                "conds": str(len(result.statuses) + len(result.injuries)),
                "cause": _truncate_text(result.death_cause or result.result_note or "-", 36),
            })

    visit_rows.sort(
        key=lambda row: (
            -int(row["visits"]),
            -int(row["heals"]),
            -int(row["fails"]),
            int(row["seed"]),
        )
    )
    return summary


def _medical_provider_lines(results: list[RunResult], title: str, event_label: str) -> list[str]:
    provider = _collect_medical_provider_summary(results, event_label)
    visits = int(provider["visits"])
    if visits <= 0:
        return [title, "none", ""]

    visit_runs = len(cast(set[int], provider["visit_runs"]))
    heal_runs = len(cast(set[int], provider["heal_runs"]))
    fail_runs = len(cast(set[int], provider["fail_runs"]))
    visit_rows = cast(list[dict[str, str]], provider["visit_rows"])
    healed_counts = cast(Counter[str], provider["healed_counts"])
    healed_runs = cast(defaultdict[str, set[int]], provider["healed_runs"])

    lines = [
        (
            f"{title} runs={visit_runs}/{len(results)} total-visits={visits} "
            f"heal-visits={provider['heal_visits']} fail-visits={provider['fail_visits']} "
            f"cash={_format_int(int(provider['cash_delta']))} "
            f"avg-cash={_format_average(int(provider['cash_delta']), visits, money=True)} "
            f"hp={int(provider['health_delta']):+} san={int(provider['sanity_delta']):+} "
            f"heal-runs={heal_runs} fail-runs={fail_runs}"
        )
    ]
    lines.extend(_build_text_table(
        [
            ("seed", "seed"),
            ("visits", "visits"),
            ("heals", "heals"),
            ("fails", "fails"),
            ("outcome", "outcome"),
            ("day", "end-day"),
            ("rank", "rank"),
            ("end$", "end$"),
            ("hp", "hp"),
            ("san", "san"),
            ("conds", "end-cond"),
            ("cause", "cause"),
        ],
        visit_rows,
        {
            "seed": "right",
            "visits": "right",
            "heals": "right",
            "fails": "right",
            "day": "right",
            "rank": "right",
            "end$": "right",
            "hp": "right",
            "san": "right",
            "conds": "right",
        },
    ))

    if healed_counts:
        heal_rows = []
        for condition, count in healed_counts.most_common():
            heal_rows.append({
                "condition": condition,
                "heals": str(count),
                "runs": f"{len(healed_runs[condition])}/{len(results)}",
            })
        lines.append(f"{title} Heals")
        lines.extend(_build_text_table(
            [("condition", "condition"), ("heals", "heals"), ("runs", "runs")],
            heal_rows,
            {"heals": "right", "runs": "right"},
        ))

    fail_rows = [row for row in visit_rows if int(row["fails"]) > 0]
    if fail_rows:
        lines.append(f"{title} Fails")
        lines.extend(_build_text_table(
            [
                ("seed", "seed"),
                ("visits", "visits"),
                ("fails", "fails"),
                ("outcome", "outcome"),
                ("day", "end-day"),
                ("end$", "end$"),
                ("conds", "end-cond"),
                ("cause", "cause"),
            ],
            fail_rows,
            {"seed": "right", "visits": "right", "fails": "right", "day": "right", "end$": "right", "conds": "right"},
        ))

    lines.append("")
    return lines


def _condition_universe_lines(
    results: list[RunResult],
    *,
    title: str,
    universe: tuple[str, ...],
    final_attr: str,
    added_attr: str,
    removed_attr: str,
    doctor_summary: dict[str, object],
    witch_summary: dict[str, object],
) -> list[str]:
    aggregate: dict[str, dict[str, int]] = {}
    doctor_heals = cast(Counter[str], doctor_summary["healed_counts"])
    witch_heals = cast(Counter[str], witch_summary["healed_counts"])

    def ensure_entry(name: str) -> dict[str, int]:
        return aggregate.setdefault(name, {
            "seen": 0,
            "seen_runs": 0,
            "gone": 0,
            "gone_runs": 0,
            "end": 0,
            "died_end": 0,
            "doctor": 0,
            "witch": 0,
        })

    for name in universe:
        ensure_entry(name)

    for result in results:
        seen_this_run: set[str] = set()
        removed_this_run: set[str] = set()
        final_conditions = set(getattr(result, final_attr))

        for record in result.cycle_records:
            for name in getattr(record, added_attr):
                entry = ensure_entry(name)
                entry["seen"] += 1
                seen_this_run.add(name)
            for name in getattr(record, removed_attr):
                entry = ensure_entry(name)
                entry["gone"] += 1
                removed_this_run.add(name)

        for name in seen_this_run:
            ensure_entry(name)["seen_runs"] += 1
        for name in removed_this_run:
            ensure_entry(name)["gone_runs"] += 1
        for name in final_conditions:
            entry = ensure_entry(name)
            entry["end"] += 1
            if result.outcome == "died":
                entry["died_end"] += 1

    for name, count in doctor_heals.items():
        ensure_entry(name)["doctor"] = count
    for name, count in witch_heals.items():
        ensure_entry(name)["witch"] = count

    if not aggregate:
        return []

    rows = []
    total = len(results)
    for name, stats in sorted(
        aggregate.items(),
        key=lambda item: (
            item[1]["end"],
            item[1]["seen_runs"],
            item[1]["gone_runs"],
            item[1]["doctor"] + item[1]["witch"],
            item[0].casefold(),
        ),
        reverse=True,
    ):
        seen_runs = stats["seen_runs"]
        baseline_runs = max(seen_runs, stats["end"], stats["gone_runs"])
        rows.append({
            "name": name,
            "seen": str(stats["seen"]),
            "runs": f"{seen_runs}/{total}",
            "gone": str(stats["gone"]),
            "gone_runs": f"{stats['gone_runs']}/{total}",
            "end": f"{stats['end']}/{total}",
            "removed_share": "-" if baseline_runs <= 0 else f"{(stats['gone_runs'] / baseline_runs) * 100:.0f}%",
            "end_share": "-" if baseline_runs <= 0 else f"{(stats['end'] / baseline_runs) * 100:.0f}%",
            "died": str(stats["died_end"]),
            "doctor": str(stats["doctor"]),
            "witch": str(stats["witch"]),
        })

    lines = [title]
    lines.append("tracker note: add/remove counts are cycle-diff based; same-cycle cures may not appear in seen/removed totals, but end-of-run conditions are final-state accurate")
    lines.extend(_build_text_table(
        [
            ("name", "name"),
            ("seen", "seen"),
            ("runs", "seen-runs"),
            ("gone", "removed"),
            ("gone_runs", "removed-runs"),
            ("end", "end-runs"),
            ("removed_share", "removed%"),
            ("end_share", "still-end%"),
            ("died", "died-end"),
            ("doctor", "doctor-heals"),
            ("witch", "witch-heals"),
        ],
        rows,
        {
            "seen": "right",
            "runs": "right",
            "gone": "right",
            "gone_runs": "right",
            "end": "right",
            "removed_share": "right",
            "end_share": "right",
            "died": "right",
            "doctor": "right",
            "witch": "right",
        },
    ))
    lines.append("")
    return lines


def _dealings_lines(
    results: list[RunResult],
    *,
    title: str,
    source_prefixes: tuple[str, ...],
    out_label: str,
) -> list[str]:
    aggregate: dict[str, dict[str, int]] = {}
    total = len(results)
    for result in results:
        touched_runs: defaultdict[str, set[str]] = defaultdict(set)
        for item_name, history in result.item_provenance.items():
            entry = aggregate.setdefault(
                item_name,
                {"in": 0, "out": 0, "used": 0, "brk": 0, "fix": 0, "rep": 0, "runs": 0},
            )
            matches = {
                "in": _history_entries_for_sources(history.get("acquired", []), source_prefixes),
                "out": _history_entries_for_sources(history.get("removed", []), source_prefixes),
                "used": _history_entries_for_sources(history.get("used", []), source_prefixes),
                "brk": _history_entries_for_sources(history.get("broken", []), source_prefixes),
                "fix": _history_entries_for_sources(history.get("fixed", []), source_prefixes),
                "rep": _history_entries_for_sources(history.get("repairing", []), source_prefixes),
            }
            touched = False
            for key, entries in matches.items():
                if entries:
                    entry[key] += len(entries)
                    touched_runs[item_name].add(key)
                    touched = True
            if touched:
                entry["runs"] += 1

    if not aggregate:
        return [title, "none", ""]

    rows = []
    for item_name, stats in sorted(
        aggregate.items(),
        key=lambda item: (
            item[1]["in"] + item[1]["out"] + item[1]["used"],
            item[1]["runs"],
            item[0].casefold(),
        ),
        reverse=True,
    ):
        if not any(stats.values()):
            continue
        rows.append({
            "item": item_name,
            "in": str(stats["in"]),
            "runs": f"{stats['runs']}/{total}",
            "out": str(stats["out"]),
            "used": str(stats["used"]),
            "brk": str(stats["brk"]),
            "fix": str(stats["fix"]),
            "rep": str(stats["rep"]),
        })

    if not rows:
        return [title, "none", ""]

    lines = [title]
    lines.extend(_build_text_table(
        [
            ("item", "item"),
            ("in", "acquired"),
            ("runs", "runs"),
            ("out", out_label),
            ("used", "used"),
            ("brk", "brk"),
            ("fix", "fix"),
            ("rep", "repair"),
        ],
        rows,
        {"in": "right", "runs": "right", "out": "right", "used": "right", "brk": "right", "fix": "right", "rep": "right"},
    ))
    lines.append("")
    return lines


def _adventure_lines(results: list[RunResult]) -> list[str]:
    if not results:
        return ["Adventures", "none", ""]

    rows = []
    loot_lines = []
    total = len(results)
    for display_name, event_label in ADVENTURE_ROWS:
        location_key = f"location:{event_label}"
        visit_runs = sum(1 for result in results if result.location_hits.get(event_label, 0) > 0)
        total_visits = sum(result.location_hits.get(event_label, 0) for result in results)

        item_counter: Counter[str] = Counter()
        status_added = 0
        status_removed = 0
        injuries_added = 0
        injuries_removed = 0
        item_runs = 0
        for result in results:
            run_got_item = False
            for item_name, history in result.item_provenance.items():
                acquired = _history_entries_for_sources(history.get("acquired", []), (location_key,))
                if acquired:
                    item_counter[item_name] += len(acquired)
                    run_got_item = True
            if run_got_item:
                item_runs += 1
            for record in result.cycle_records:
                if location_key not in record.events:
                    continue
                status_added += len(record.statuses_added)
                status_removed += len(record.statuses_removed)
                injuries_added += len(record.injuries_added)
                injuries_removed += len(record.injuries_removed)

        rows.append({
            "area": display_name,
            "runs": f"{visit_runs}/{total}",
            "visits": str(total_visits),
            "item_gets": str(sum(item_counter.values())),
            "item_runs": f"{item_runs}/{total}",
            "status+": str(status_added),
            "status-": str(status_removed),
            "inj+": str(injuries_added),
            "inj-": str(injuries_removed),
        })
        if item_counter:
            loot_lines.append(
                f"{display_name.lower()} loot " + " | ".join(
                    f"{item_name}={count}" for item_name, count in item_counter.most_common(6)
                )
            )

    lines = ["Adventures"]
    lines.extend(_build_text_table(
        [
            ("area", "area"),
            ("runs", "runs"),
            ("visits", "visits"),
            ("item_gets", "item-gets"),
            ("item_runs", "item-runs"),
            ("status+", "status+"),
            ("status-", "status-"),
            ("inj+", "inj+"),
            ("inj-", "inj-"),
        ],
        rows,
        {"runs": "right", "visits": "right", "item_gets": "right", "item_runs": "right", "status+": "right", "status-": "right", "inj+": "right", "inj-": "right"},
    ))
    lines.extend(loot_lines)
    lines.append("")
    return lines


def _run_sorted_lines(title: str, ordered: list[RunResult], primary_label: str, primary_key: str, limit: int = 10) -> list[str]:
    if not ordered:
        return []

    rows = []
    for result in ordered[:limit]:
        peak_value = result.peak_balance or result.balance or 0
        peak_day = result.peak_balance_days[0] if result.peak_balance_days else result.day or 0
        route = result.top_adventure if result.top_adventure != "none" else result.top_location
        detail = result.death_tag if result.outcome == "died" else _truncate_text(result.result_note or route or "-", 28)
        if primary_key == "day":
            primary_value = str(result.day or 0)
        elif primary_key == "end_balance":
            primary_value = _format_int(result.balance)
        else:
            primary_value = _format_int(peak_value)
        rows.append({
            primary_key: primary_value,
            "seed": str(result.seed),
            "outcome": result.display_outcome,
            "rank": str(result.rank if result.rank is not None else "-"),
            "peak": _format_int(peak_value),
            "peak_day": str(peak_day),
            "day": str(result.day if result.day is not None else "-"),
            "end_balance": _format_int(result.balance),
            "hp": str(result.health if result.health is not None else "-"),
            "san": str(result.sanity if result.sanity is not None else "-"),
            "route": _truncate_text(route or "none", 22),
            "detail": detail,
        })

    headers = [(primary_key, primary_label)]
    if primary_key != "day":
        headers.append(("day", "day"))
    if primary_key != "peak":
        headers.append(("peak", "peak$"))
    headers.append(("peak_day", "peak-day"))
    if primary_key != "end_balance":
        headers.append(("end_balance", "end$"))
    headers.extend([
        ("seed", "seed"),
        ("outcome", "outcome"),
        ("rank", "rank"),
        ("hp", "hp"),
        ("san", "san"),
        ("route", "route"),
        ("detail", "detail"),
    ])

    lines = [title]
    lines.extend(_build_text_table(
        headers,
        rows,
        {
            "day": "right",
            "peak": "right",
            "peak_day": "right",
            "end_balance": "right",
            "seed": "right",
            "rank": "right",
            "hp": "right",
            "san": "right",
        },
    ))
    lines.append("")
    return lines


def _marvin_provenance_lines(results: list[RunResult]) -> list[str]:
    aggregate: dict[str, dict[str, object]] = {}
    total = len(results)
    for result in results:
        for item_name, history in result.marvin_item_provenance.items():
            entry = aggregate.setdefault(
                item_name,
                {
                    "bought_runs": 0,
                    "used_runs": 0,
                    "broken_runs": 0,
                    "fixed_runs": 0,
                    "buy_days": [],
                    "use_days": [],
                    "use_sources": Counter(),
                },
            )
            if history.get("bought"):
                entry["bought_runs"] += 1
                entry["buy_days"].extend(day for day, _source in history["bought"] if day is not None)
            if history.get("used"):
                entry["used_runs"] += 1
                entry["use_days"].extend(day for day, _source in history["used"] if day is not None)
                entry["use_sources"].update(source for _day, source in history["used"])
            if history.get("broken"):
                entry["broken_runs"] += 1
            if history.get("fixed"):
                entry["fixed_runs"] += 1

    def average(values: list[int]) -> str:
        if not values:
            return "-"
        return str(round(sum(values) / len(values)))

    rows = []
    for item_name in MARVIN_ITEM_ORDER:
        stats = cast(dict[str, object], aggregate.get(
            item_name,
            {
                "bought_runs": 0,
                "used_runs": 0,
                "broken_runs": 0,
                "fixed_runs": 0,
                "buy_days": [],
                "use_days": [],
                "use_sources": Counter(),
            },
        ))
        rows.append({
            "item": item_name,
            "bought": f"{stats['bought_runs']}/{total}",
            "used": f"{stats['used_runs']}/{total}",
            "broken": f"{stats['broken_runs']}/{total}",
            "fixed": f"{stats['fixed_runs']}/{total}",
            "buy_day": average(stats["buy_days"]),
            "use_day": average(stats["use_days"]),
            "use_sources": _summarize_counter(stats["use_sources"], 3),
        })

    lines = ["Marvin Provenance"]
    lines.extend(_build_text_table(
        [
            ("item", "item"),
            ("bought", "bought-runs"),
            ("used", "used-runs"),
            ("broken", "broken-runs"),
            ("fixed", "fixed-runs"),
            ("buy_day", "avg-buy-day"),
            ("use_day", "avg-use-day"),
            ("use_sources", "use-sources"),
        ],
        rows,
        {"bought": "right", "used": "right", "broken": "right", "fixed": "right", "buy_day": "right", "use_day": "right"},
    ))
    lines.append("")
    return lines


def _summarize_counter(counter: Counter[str], limit: int = 3) -> str:
    if not counter:
        return "none"

    def render_count(value: object) -> str:
        if isinstance(value, float):
            rounded = round(value, 1)
            return str(int(rounded)) if rounded.is_integer() else f"{rounded:.1f}"
        return str(value)

    return " | ".join(f"{name}={render_count(count)}" for name, count in counter.most_common(limit))


def _recent_damage_summary(result: RunResult, limit: int = 3) -> str:
    samples: list[str] = []
    for cycle in reversed(result.cycle_records):
        if len(samples) >= limit:
            break
        if cycle.health_delta >= 0 and cycle.sanity_delta >= 0 and not cycle.injuries_added and not cycle.statuses_added:
            continue
        events = "/".join(cycle.events[:2]) if cycle.events else "none"
        extras = []
        if cycle.injuries_added:
            extras.append("+inj=" + ",".join(cycle.injuries_added[:2]))
        if cycle.statuses_added:
            extras.append("+status=" + ",".join(cycle.statuses_added[:2]))
        extra_text = f" {' '.join(extras)}" if extras else ""
        samples.append(
            f"d{cycle.day} hp{cycle.health_delta:+} san{cycle.sanity_delta:+} ev={events}{extra_text}"
        )
    return " || ".join(samples) if samples else "none"


def _top_damage_event_summary(result: RunResult, metric: str, limit: int = 3) -> str:
    ranked = [
        (name, values)
        for name, values in result.event_effects.items()
        if values.get(metric, 0.0) < 0
    ]
    if not ranked:
        return "none"
    ranked.sort(key=lambda item: (item[1][metric], item[0]))
    parts = []
    for name, values in ranked[:limit]:
        parts.append(f"{name}={values[metric]:+.1f}")
    return " | ".join(parts)


def _death_stage_audit_lines(results: list[RunResult]) -> list[str]:
    deaths = [result for result in results if result.outcome == "died"]
    if not deaths:
        return []

    rows = []
    for bucket_name in ["day<=10", "11-30", "31-60", "61-90", "91+"]:
        bucket_results = [result for result in deaths if result.day_bucket == bucket_name]
        if not bucket_results:
            continue
        tag_counter = Counter(result.death_tag for result in bucket_results)
        condition_counter = Counter(
            condition
            for result in bucket_results
            for condition in [*result.statuses, *result.injuries]
        )
        avg_day = round(sum((result.day or 0) for result in bucket_results) / len(bucket_results))
        avg_peak = round(sum((result.peak_balance or result.balance or 0) for result in bucket_results) / len(bucket_results))
        rows.append({
            "bucket": bucket_name,
            "deaths": str(len(bucket_results)),
            "avg_day": str(avg_day),
            "avg_peak": _format_int(avg_peak),
            "tags": _summarize_counter(tag_counter, 3),
            "conditions": _summarize_counter(condition_counter, 3),
        })

    lines = ["Death Stage Audit"]
    lines.extend(_build_text_table(
        [
            ("bucket", "day-bucket"),
            ("deaths", "deaths"),
            ("avg_day", "avg-day"),
            ("avg_peak", "avg-peak$"),
            ("tags", "top-tags"),
            ("conditions", "common-conditions"),
        ],
        rows,
        {"deaths": "right", "avg_day": "right", "avg_peak": "right"},
    ))
    lines.append("")
    return lines


def _death_rank_audit_lines(results: list[RunResult]) -> list[str]:
    deaths = [result for result in results if result.outcome == "died"]
    if not deaths:
        return []

    rows = []
    for rank in sorted({result.rank if result.rank is not None else -1 for result in deaths}):
        rank_results = [result for result in deaths if (result.rank if result.rank is not None else -1) == rank]
        tag_counter = Counter(result.death_tag for result in rank_results)
        cause_counter = Counter(result.death_cause or "Unknown" for result in rank_results)
        avg_day = round(sum((result.day or 0) for result in rank_results) / len(rank_results))
        avg_peak = round(sum((result.peak_balance or result.balance or 0) for result in rank_results) / len(rank_results))
        rows.append({
            "rank": str(rank),
            "deaths": str(len(rank_results)),
            "avg_day": str(avg_day),
            "avg_peak": _format_int(avg_peak),
            "tags": _summarize_counter(tag_counter, 3),
            "top_cause": _summarize_counter(cause_counter, 2),
        })

    lines = ["Death Rank Audit"]
    lines.extend(_build_text_table(
        [
            ("rank", "end-rank"),
            ("deaths", "deaths"),
            ("avg_day", "avg-day"),
            ("avg_peak", "avg-peak$"),
            ("tags", "top-tags"),
            ("top_cause", "top-causes"),
        ],
        rows,
        {"rank": "right", "deaths": "right", "avg_day": "right", "avg_peak": "right"},
    ))
    lines.append("")
    return lines


def _death_sorted_lines(results: list[RunResult], title: str, ordered: list[RunResult], primary_label: str, primary_key: str, limit: int = 10) -> list[str]:
    if not ordered:
        return []

    rows = []
    for result in ordered[:limit]:
        cause = result.death_cause or "Unknown"
        if len(cause) > 42:
            cause = cause[:39] + "..."
        peak_value = result.peak_balance or result.balance or 0
        peak_day = result.peak_balance_days[0] if result.peak_balance_days else result.day or 0
        end_balance = result.balance or 0
        rows.append({
            primary_key: _format_int(peak_value) if primary_key == "peak" else str(result.day or 0),
            "seed": str(result.seed),
            "rank": str(result.rank if result.rank is not None else "-"),
            "peak": _format_int(peak_value),
            "peak_day": str(peak_day),
            "day": str(result.day if result.day is not None else "-"),
            "end_balance": _format_int(end_balance),
            "drop": _format_int(max(0, peak_value - end_balance)),
            "tag": result.death_tag,
            "cause": cause,
        })

    lines = [title]
    headers = [(primary_key, primary_label)]
    if primary_key != "day":
        headers.append(("day", "day"))
    if primary_key != "peak":
        headers.append(("peak", "peak$"))
    headers.extend([
        ("peak_day", "peak-day"),
        ("end_balance", "end$"),
        ("drop", "drop$"),
    ])
    headers.extend([
        ("seed", "seed"),
        ("rank", "rank"),
        ("tag", "tag"),
        ("cause", "cause"),
    ])
    lines.extend(_build_text_table(
        headers,
        rows,
        {
            "seed": "right",
            "rank": "right",
            "day": "right",
            "peak": "right",
            "peak_day": "right",
            "end_balance": "right",
            "drop": "right",
        },
    ))
    lines.append("")
    return lines


def _fatal_pressure_lines(results: list[RunResult]) -> list[str]:
    deaths = [result for result in results if result.outcome == "died"]
    if not deaths:
        return []

    injury_counter = Counter(injury for result in deaths for injury in result.injuries)
    status_counter = Counter(status for result in deaths for status in result.statuses)
    recent_event_counter = Counter(
        event
        for result in deaths
        for cycle in result.cycle_records[-4:]
        for event in cycle.events
        if cycle.health_delta < 0 or cycle.sanity_delta < 0 or cycle.injuries_added or cycle.statuses_added
    )

    health_events = Counter()
    sanity_events = Counter()
    for result in deaths:
        for event_name, values in result.event_effects.items():
            if values.get("health", 0.0) < 0:
                health_events[event_name] += round(abs(values["health"]), 1)
            if values.get("sanity", 0.0) < 0:
                sanity_events[event_name] += round(abs(values["sanity"]), 1)

    lines = ["Fatal Pressure"]
    lines.append(f"recent-damage-events {_summarize_counter(recent_event_counter, 6)}")
    lines.append(f"health-damage-events {_summarize_counter(health_events, 6)}")
    lines.append(f"sanity-damage-events {_summarize_counter(sanity_events, 6)}")
    lines.append(f"injuries {_summarize_counter(injury_counter, 6)}")
    lines.append(f"statuses {_summarize_counter(status_counter, 6)}")
    lines.append("")
    return lines


def _fatal_context_lines(results: list[RunResult]) -> list[str]:
    deaths = [result for result in results if result.outcome == "died"]
    if not deaths:
        return []

    sampled = sorted(
        deaths,
        key=lambda result: (
            -(result.peak_balance or result.balance or 0),
            -(result.day or 0),
            result.seed,
        ),
    )[:10]

    lines = ["Fatal Context Samples"]
    for result in sampled:
        lines.append(
            f"seed={result.seed} day={result.day} rank={result.rank} peak={_format_int(result.peak_balance or result.balance)} tag={result.death_tag} cause={result.death_cause or 'Unknown'}"
        )
        lines.append(f"  recent={_recent_damage_summary(result, 3)}")
        lines.append(f"  top-hp={_top_damage_event_summary(result, 'health', 3)}")
        lines.append(f"  top-san={_top_damage_event_summary(result, 'sanity', 3)}")
        injuries = ", ".join(result.injuries) if result.injuries else "none"
        statuses = ", ".join(result.statuses) if result.statuses else "none"
        lines.append(f"  injuries={injuries} | statuses={statuses}")
    lines.append("")
    return lines


def _game_statistics_lines(results: list[RunResult]) -> list[str]:
    """Show distributions of key game-wide statistics across seeds."""
    if not results:
        return []

    def _stat(result: RunResult, key: str) -> int:
        return result.game_statistics.get(key, 0)

    stat_keys = [
        ("injuries_sustained", "injuries-sustained"),
        ("illnesses_contracted", "illnesses-contracted"),
        ("loans_taken", "loans-taken"),
        ("loans_repaid", "loans-repaid"),
        ("total_borrowed", "total-borrowed"),
        ("companions_befriended", "companions-befriended"),
        ("near_death_experiences", "near-deaths"),
        ("times_robbed", "times-robbed"),
        ("times_hospitalized", "times-hospitalized"),
        ("mechanic_visits", "mechanic-visits"),
        ("doctor_visits", "doctor-visits"),
        ("witch_doctor_visits", "witch-dr-visits"),
    ]

    def avg(vals: list[int]) -> str:
        return f"{sum(vals)/max(1, len(vals)):.1f}"

    total = len(results)
    lines = ["Game Statistics"]
    header = f"{'stat':<22} {'avg':>5} {'max':>5} {'min':>5} {'nonzero':>8} {'sum':>9}"
    lines.append(header)
    lines.append("-" * len(header))
    for key, label in stat_keys:
        vals = [_stat(r, key) for r in results]
        nonzero = sum(1 for v in vals if v > 0)
        money = "borrowed" in label or "total" in label
        total_val = sum(vals)
        fmt_sum = f"${total_val:,}" if money else str(total_val)
        fmt_max = f"${max(vals):,}" if money else str(max(vals))
        fmt_min = f"${min(vals):,}" if money else str(min(vals))
        fmt_avg = f"${sum(vals)/max(1,len(vals)):,.0f}" if money else avg(vals)
        lines.append(
            f"{label:<22} {fmt_avg:>5} {fmt_max:>5} {fmt_min:>5} {nonzero:>4}/{total:<2} {fmt_sum:>9}"
        )
    lines.append("")
    return lines


def _injury_illness_distribution_lines(results: list[RunResult]) -> list[str]:
    """Per-seed distribution of injuries and statuses at end-of-run, split by outcome."""
    if not results:
        return []

    def _stat(result: RunResult, key: str) -> int:
        return result.game_statistics.get(key, 0)

    survived_results = [r for r in results if r.survived_run]
    dead_results = [r for r in results if r.outcome == "died"]
    broke_results = [r for r in results if r.outcome == "broke"]

    def cohort_row(label: str, cohort: list[RunResult]) -> dict[str, str]:
        if not cohort:
            return {"cohort": label, "n": "0", "avg_inj_sus": "-", "avg_ill_sus": "-",
                    "avg_inj_end": "-", "avg_ill_end": "-", "max_inj": "-", "max_ill": "-"}
        inj_sus = [_stat(r, "injuries_sustained") for r in cohort]
        ill_sus = [_stat(r, "illnesses_contracted") for r in cohort]
        inj_end = [len(r.injuries) for r in cohort]
        ill_end = [len(r.statuses) for r in cohort]
        def av(lst: list[int]) -> str:
            return f"{sum(lst)/len(lst):.1f}"
        return {
            "cohort": label,
            "n": str(len(cohort)),
            "avg_inj_sus": av(inj_sus),
            "avg_ill_sus": av(ill_sus),
            "avg_inj_end": av(inj_end),
            "avg_ill_end": av(ill_end),
            "max_inj": str(max(inj_end)),
            "max_ill": str(max(ill_end)),
        }

    rows = [
        cohort_row("all", results),
        cohort_row("survived", survived_results),
        cohort_row("died", dead_results),
        cohort_row("broke", broke_results),
    ]

    lines = ["Injury & Illness Distribution"]
    lines.extend(_build_text_table(
        [
            ("cohort", "cohort"),
            ("n", "n"),
            ("avg_inj_sus", "avg-inj-total"),
            ("avg_ill_sus", "avg-ill-total"),
            ("avg_inj_end", "avg-inj-end"),
            ("avg_ill_end", "avg-ill-end"),
            ("max_inj", "max-inj-end"),
            ("max_ill", "max-ill-end"),
        ],
        rows,
        {"n": "right", "avg_inj_sus": "right", "avg_ill_sus": "right",
         "avg_inj_end": "right", "avg_ill_end": "right", "max_inj": "right", "max_ill": "right"},
    ))

    # Seed-level breakdown: keep zero-count seeds visible for auditability.
    sorted_by_inj = sorted(
        results,
        key=lambda r: (_stat(r, "injuries_sustained"), len(r.injuries), r.seed),
        reverse=True,
    )
    sorted_by_ill = sorted(
        results,
        key=lambda r: (_stat(r, "illnesses_contracted"), len(r.statuses), r.seed),
        reverse=True,
    )
    lines.append("most injuries: " + (" | ".join(
        f"s{r.seed}={_stat(r,'injuries_sustained')}(end:{len(r.injuries)})" for r in sorted_by_inj[:10]
    ) if sorted_by_inj else "none"))
    lines.append("most illnesses: " + (" | ".join(
        f"s{r.seed}={_stat(r,'illnesses_contracted')}(end:{len(r.statuses)})" for r in sorted_by_ill[:10]
    ) if sorted_by_ill else "none"))
    least_inj = sorted(results, key=lambda r: (_stat(r, "injuries_sustained"), len(r.injuries), r.seed))
    least_ill = sorted(results, key=lambda r: (_stat(r, "illnesses_contracted"), len(r.statuses), r.seed))
    if least_inj:
        lines.append("least injuries (incl 0): " + " | ".join(
            f"s{r.seed}={_stat(r,'injuries_sustained')}(end:{len(r.injuries)})" for r in least_inj[:10]
        ))
    if least_ill:
        lines.append("least illnesses (incl 0): " + " | ".join(
            f"s{r.seed}={_stat(r,'illnesses_contracted')}(end:{len(r.statuses)})" for r in least_ill[:10]
        ))
    lines.append("")
    return lines


def _companion_roster_lines(results: list[RunResult]) -> list[str]:
    """Show companion acquisition across seeds."""
    if not results:
        return []

    total = len(results)
    all_companions: Counter[str] = Counter()
    for result in results:
        for companion in result.companions_list:
            all_companions[companion] += 1

    runs_with_companions = sum(1 for r in results if r.companions_list)
    avg_companions = sum(len(r.companions_list) for r in results) / max(1, total)
    max_companions = max((len(r.companions_list) for r in results), default=0)
    max_seed = next(
        (r.seed for r in results if len(r.companions_list) == max_companions), None
    )

    lines = [
        f"Companion Roster runs-with-companions={runs_with_companions}/{total} "
        f"avg-per-run={avg_companions:.1f} max={max_companions}(seed={max_seed})"
    ]
    if all_companions:
        lines.append("companion         acquired  (seeds)")
        lines.append("----------------  --------  ------")
        for companion, count in all_companions.most_common():
            seeds_with = [str(r.seed) for r in results if companion in r.companions_list]
            seed_str = ",".join(seeds_with[:8]) + ("..." if len(seeds_with) > 8 else "")
            lines.append(f"{companion:<18}{count:>5}/{total:<2}  s={seed_str}")
    else:
        lines.append("no companions acquired")

    # Also list companions_befriended stat (includes all time, even if later lost)
    stat_totals = Counter()
    for r in results:
        stat_totals["befriended"] += r.game_statistics.get("companions_befriended", 0)
    if stat_totals["befriended"] > 0:
        lines.append(f"total companions-befriended stat across all seeds: {stat_totals['befriended']}")
    lines.append("")
    return lines


def _companion_state_lines(results: list[RunResult]) -> list[str]:
    if not results:
        return []

    total = len(results)
    known_companions = list(_known_companion_universe())
    observed_companions = sorted(
        {name for result in results for name in result.companion_details.keys()},
        key=str.casefold,
    )
    if not known_companions:
        known_companions = observed_companions
    else:
        extras = [name for name in observed_companions if name not in known_companions]
        known_companions.extend(extras)

    runs_with_any = sum(1 for result in results if result.companion_details)
    runs_with_bonded = sum(
        1 for result in results if any(bool(data.get("bonded")) for data in result.companion_details.values())
    )
    runs_with_lost = sum(
        1 for result in results if any(str(data.get("status", "")) == "lost" for data in result.companion_details.values())
    )
    runs_with_dead = sum(
        1 for result in results if any(str(data.get("status", "")) == "dead" for data in result.companion_details.values())
    )

    rows = []
    for name in known_companions:
        seen = 0
        alive = 0
        lost = 0
        dead = 0
        bonded = 0
        happiness_total = 0
        max_days = 0
        companion_type = "-"
        for result in results:
            data = result.companion_details.get(name)
            if not data:
                continue
            seen += 1
            status = str(data.get("status", "unknown"))
            companion_type = str(data.get("type", companion_type))
            if status == "alive":
                alive += 1
            elif status == "lost":
                lost += 1
            elif status == "dead":
                dead += 1
            if bool(data.get("bonded")):
                bonded += 1
            happiness_total += int(data.get("happiness", 0) or 0)
            max_days = max(max_days, int(data.get("days_owned", 0) or 0))
        rows.append({
            "companion": name,
            "type": companion_type,
            "seen": f"{seen}/{total}",
            "alive": str(alive),
            "lost": str(lost),
            "dead": str(dead),
            "bonded": str(bonded),
            "avg_happy": "-" if seen == 0 else f"{happiness_total / seen:.1f}",
            "max_days": str(max_days),
        })

    lines = [
        f"Companion State Coverage runs-with-any={runs_with_any}/{total} bonded-runs={runs_with_bonded}/{total} "
        f"lost-runs={runs_with_lost}/{total} dead-runs={runs_with_dead}/{total}"
    ]
    lines.extend(_build_text_table(
        [
            ("companion", "companion"),
            ("type", "type"),
            ("seen", "seen"),
            ("alive", "alive"),
            ("lost", "lost"),
            ("dead", "dead"),
            ("bonded", "bonded"),
            ("avg_happy", "avg-happy"),
            ("max_days", "max-days"),
        ],
        rows,
        {"seen": "right", "alive": "right", "lost": "right", "dead": "right", "bonded": "right", "avg_happy": "right", "max_days": "right"},
    ))
    lines.append("")
    return lines


def _dealer_gift_lines(results: list[RunResult]) -> list[str]:
    if not results:
        return []

    total = len(results)
    deliveries = [entry for result in results for entry in result.gift_deliveries]
    free_hands = [entry for result in results for entry in result.dealer_free_hands]
    unlocked_runs = sum(1 for result in results if result.gift_system_unlocked)
    delivery_runs = sum(1 for result in results if result.gift_deliveries)
    free_hand_runs = sum(1 for result in results if result.dealer_free_hands)

    lines = [
        f"Dealer Happiness & Gifts unlocked={unlocked_runs}/{total} gift-runs={delivery_runs}/{total} "
        f"deliveries={len(deliveries)} free-hand-runs={free_hand_runs}/{total} free-hands={len(free_hands)}"
    ]

    gift_rows = []
    gift_counter: Counter[str] = Counter()
    gift_kills: Counter[str] = Counter()
    gift_delta_sum: Counter[str] = Counter()
    gift_runs_by_item: dict[str, set[int]] = defaultdict(set)
    for result in results:
        for entry in result.gift_deliveries:
            item = str(entry.get("item", "") or "unknown")
            gift_counter[item] += 1
            gift_runs_by_item[item].add(result.seed)
            delta = entry.get("happiness_change")
            if isinstance(delta, int):
                gift_delta_sum[item] += delta
            if not bool(entry.get("alive_after", True)):
                gift_kills[item] += 1

    for item_name in sorted(gift_counter.keys(), key=lambda name: (-gift_counter[name], name.casefold())):
        count = gift_counter[item_name]
        gift_rows.append({
            "item": item_name,
            "hits": str(count),
            "runs": f"{len(gift_runs_by_item[item_name])}/{total}",
            "avg_delta": f"{gift_delta_sum[item_name] / count:+.1f}",
            "kills": str(gift_kills[item_name]),
        })

    if gift_rows:
        lines.extend(_build_text_table(
            [
                ("item", "item"),
                ("hits", "deliveries"),
                ("runs", "runs"),
                ("avg_delta", "avg-happy"),
                ("kills", "kills"),
            ],
            gift_rows,
            {"hits": "right", "runs": "right", "avg_delta": "right", "kills": "right"},
        ))
    else:
        lines.append("no gift deliveries recorded")

    if free_hands:
        tier_counter: Counter[str] = Counter(str(entry.get("tier", "unknown")) for entry in free_hands)
        avg_bet = sum(int(entry.get("bet", 0) or 0) for entry in free_hands) / len(free_hands)
        max_bet = max(int(entry.get("bet", 0) or 0) for entry in free_hands)
        lines.append(
            "free hands " +
            " | ".join(f"{tier}={count}" for tier, count in sorted(tier_counter.items(), key=lambda item: item[0])) +
            f" | avg-bet=${avg_bet:,.0f} | max-bet=${max_bet:,}"
        )
    else:
        lines.append("free hands none")
    lines.append("")
    return lines


def _mechanic_dream_progress_lines(results: list[RunResult]) -> list[str]:
    if not results:
        return []

    total = len(results)
    rows = []
    for key, label in [("tom", "Tom"), ("frank", "Frank"), ("oswald", "Oswald")]:
        values = [int(result.mechanic_dreams.get(key, 0) or 0) for result in results]
        rows.append({
            "mechanic": label,
            "any": f"{sum(1 for value in values if value >= 1)}/{total}",
            "2+": f"{sum(1 for value in values if value >= 2)}/{total}",
            "3+": f"{sum(1 for value in values if value >= 3)}/{total}",
            "4+": f"{sum(1 for value in values if value >= 4)}/{total}",
            "max": str(max(values) if values else 0),
            "avg": f"{(sum(values) / total):.2f}",
        })

    car_mechanic_counts = Counter(
        str(result.mechanic_dreams.get("car_mechanic", "") or "none")
        for result in results
    )
    chosen_counts = Counter(
        str(result.mechanic_dreams.get("chosen", "") or "none")
        for result in results
    )
    frank_gate = sum(
        1 for result in results
        if int(result.mechanic_dreams.get("frank", 0) or 0) >= 4 and (result.peak_balance or result.balance or 0) >= 100000
    )
    final_gate = sum(
        1 for result in results
        if int(result.mechanic_dreams.get("tom", 0) or 0) >= 2
        and int(result.mechanic_dreams.get("frank", 0) or 0) >= 2
        and int(result.mechanic_dreams.get("oswald", 0) or 0) >= 2
        and (result.peak_balance or result.balance or 0) >= 750000
    )

    lines = ["Mechanic Dream Progress"]
    lines.extend(_build_text_table(
        [
            ("mechanic", "mechanic"),
            ("any", "1+"),
            ("2+", "2+"),
            ("3+", "3+"),
            ("4+", "4+"),
            ("max", "max"),
            ("avg", "avg"),
        ],
        rows,
        {"any": "right", "2+": "right", "3+": "right", "4+": "right", "max": "right", "avg": "right"},
    ))
    lines.append(
        "car mechanic " + " | ".join(
            f"{name}={count}" for name, count in sorted(car_mechanic_counts.items(), key=lambda item: (-item[1], item[0].casefold()))
        )
    )
    lines.append(
        "millionaire chosen mechanic " + " | ".join(
            f"{name}={count}" for name, count in sorted(chosen_counts.items(), key=lambda item: (-item[1], item[0].casefold()))
        )
    )
    lines.append(f"frank dealer-dream gate {frank_gate}/{total}")
    lines.append(f"final mechanic ending gate {final_gate}/{total}")
    lines.append("")
    return lines


def _loan_distribution_lines(results: list[RunResult]) -> list[str]:
    """Show loan-taking behaviour and amounts."""
    if not results:
        return []

    total = len(results)
    loan_runs = sum(1 for r in results if r.game_statistics.get("loans_taken", 0) > 0)
    total_loans = sum(r.game_statistics.get("loans_taken", 0) for r in results)
    total_repaid = sum(r.game_statistics.get("loans_repaid", 0) for r in results)
    total_borrowed_amt = sum(r.game_statistics.get("total_borrowed", 0) for r in results)
    total_repaid_amt = sum(r.game_statistics.get("total_repaid", 0) for r in results)
    open_debt_runs = sum(1 for r in results if r.loan_shark_debt > 0)
    danger_runs = sum(1 for r in results if r.loan_shark_warning_level >= 2)
    violent_runs = sum(1 for r in results if r.loan_shark_warning_level >= 3)
    fake_cash_runs = sum(1 for r in results if r.fraudulent_cash > 0)

    lines = [
        f"Loan Distribution runs-with-loans={loan_runs}/{total} "
        f"total-loans={total_loans} total-repaid={total_repaid} "
        f"total-borrowed=${total_borrowed_amt:,} total-repaid-amt=${total_repaid_amt:,}",
        f"end-state open-debt={open_debt_runs}/{total} warning2+={danger_runs}/{total} warning3+={violent_runs}/{total} fake-cash-end={fake_cash_runs}/{total}"
    ]

    # Per-seed breakdown for seeds that took loans
    loan_seeds = sorted(
        [
            r for r in results
            if r.game_statistics.get("loans_taken", 0) > 0 or r.loan_shark_debt > 0 or r.fraudulent_cash > 0 or r.visited_loan_shark
        ],
        key=lambda r: (r.game_statistics.get("loans_taken", 0), r.loan_shark_debt, r.fraudulent_cash, r.seed),
        reverse=True,
    )
    if loan_seeds:
        lines.append("seed  loans  repaid  borrowed    repaid-amt  end-debt    warn  fake$      outcome   peak")
        lines.append("----  -----  ------  ----------  ----------  ----------  ----  ---------  --------  --------")
        for r in loan_seeds:
            n = r.game_statistics.get("loans_taken", 0)
            rep = r.game_statistics.get("loans_repaid", 0)
            bor = r.game_statistics.get("total_borrowed", 0)
            rep_amt = r.game_statistics.get("total_repaid", 0)
            lines.append(
                f"{r.seed:>4}  {n:>5}  {rep:>6}  ${bor:>9,}  ${rep_amt:>9,}  "
                f"${r.loan_shark_debt:>9,}  {r.loan_shark_warning_level:>4}  ${r.fraudulent_cash:>8,}  "
                f"{r.outcome:<8}  ${r.peak_balance or r.balance or 0:>7,}"
            )
    lines.append("")
    return lines


def _gambling_performance_lines(results: list[RunResult]) -> list[str]:
    """Show gambling win-rates and blackjack performance across seeds."""
    if not results:
        return []

    def _gstat(result: RunResult, key: str) -> int:
        return result.gambling_statistics.get(key, 0)

    total = len(results)
    all_hands = sum(_gstat(r, "total_hands") for r in results)
    all_wins = sum(_gstat(r, "wins") for r in results)
    all_losses = sum(_gstat(r, "losses") for r in results)
    all_ties = sum(_gstat(r, "ties") for r in results)
    all_bjs = sum(_gstat(r, "blackjacks") for r in results)
    all_busts = sum(_gstat(r, "busts") for r in results)
    all_won = sum(_gstat(r, "total_won") for r in results)
    all_lost = sum(_gstat(r, "total_lost") for r in results)
    all_dd_won = sum(_gstat(r, "double_downs_won") for r in results)
    all_splits_won = sum(_gstat(r, "splits_won") for r in results)
    all_surrenders = sum(_gstat(r, "surrenders_used") for r in results)

    win_rate = (all_wins / max(1, all_hands)) * 100
    bj_rate = (all_bjs / max(1, all_hands)) * 100
    bust_rate = (all_busts / max(1, all_hands)) * 100
    tie_rate = (all_ties / max(1, all_hands)) * 100
    net = all_won - all_lost

    lines = [
        f"Gambling Performance seeds={total} total-hands={all_hands:,}",
        f"win-rate={win_rate:.1f}%  bj-rate={bj_rate:.1f}%  bust-rate={bust_rate:.1f}%  tie-rate={tie_rate:.1f}%",
        f"total-won=${all_won:,}  total-lost=${all_lost:,}  net=${net:,}",
        f"double-downs-won={all_dd_won:,}  splits-won={all_splits_won:,}  surrenders={all_surrenders:,}",
    ]

    # Top and bottom seeds by win rate
    def seed_win_rate(r: RunResult) -> float:
        h = _gstat(r, "total_hands")
        return _gstat(r, "wins") / max(1, h) if h > 0 else 0.0

    sorted_by_wr = sorted([r for r in results if _gstat(r, "total_hands") > 20], key=seed_win_rate)
    if sorted_by_wr:
        worst = sorted_by_wr[:3]
        best = sorted_by_wr[-3:]
        lines.append(
            "best-wr: " + " | ".join(
                f"s{r.seed}={seed_win_rate(r)*100:.1f}%({_gstat(r,'total_hands')}h)" for r in reversed(best)
            )
        )
        lines.append(
            "worst-wr: " + " | ".join(
                f"s{r.seed}={seed_win_rate(r)*100:.1f}%({_gstat(r,'total_hands')}h)" for r in worst
            )
        )
    lines.append("")
    return lines


def _flask_and_item_breakage_lines(results: list[RunResult]) -> list[str]:
    """Witch flask purchases and item breakage summary."""
    lines: list[str] = []

    # Flask purchases
    flask_total: Counter[str] = Counter()
    flask_runs: Counter[str] = Counter()
    for r in results:
        for flask_name, count in r.flask_purchases.items():
            flask_total[flask_name] += count
            flask_runs[flask_name] += 1

    total = len(results)
    total_flasks = sum(flask_total.values())
    runs_bought = sum(1 for r in results if r.flask_purchases)
    lines.append(
        f"Flask Purchases runs-bought={runs_bought}/{total} total-purchased={total_flasks}"
    )
    lines.append("flask                  times-bought  runs")
    lines.append("---------------------  ------------  ----")
    for flask_name in WITCH_FLASK_PRIORITIES:
        count = flask_total.get(flask_name, 0)
        lines.append(f"{flask_name:<23}{count:>8}  {flask_runs[flask_name]:>4}/{total}")
    lines.append("")

    # Item breakages
    item_break_total: Counter[str] = Counter()
    item_break_runs: Counter[str] = Counter()
    for r in results:
        for item_name, count in r.items_ever_broken.items():
            item_break_total[item_name] += count
            item_break_runs[item_name] += 1

    total_breaks = sum(item_break_total.values())
    runs_with_breaks = sum(1 for r in results if r.items_ever_broken)
    lines.append(
        f"Item Breakage runs-with-breaks={runs_with_breaks}/{total} total-breaks={total_breaks}"
    )
    if item_break_total:
        lines.append("item                   total-breaks  runs")
        lines.append("---------------------  ------------  ----")
        for item_name, count in item_break_total.most_common():
            lines.append(f"{item_name:<23}{count:>8}  {item_break_runs[item_name]:>4}/{total}")
    else:
        lines.append("no item breakages recorded")
    lines.append("")

    # Items currently broken or in repair at end of run
    broken_end: Counter[str] = Counter()
    repairing_end: Counter[str] = Counter()
    for r in results:
        for item in r.broken_items_list:
            broken_end[item] += 1
        for item in r.repairing_items_list:
            repairing_end[item] += 1
    if broken_end or repairing_end:
        lines.append("Items broken at run-end: " + _summarize_counter(broken_end, 6))
        lines.append("Items in repair at run-end: " + _summarize_counter(repairing_end, 6))
        lines.append("")

    return lines


def _system_presence_lines(results: list[RunResult]) -> list[str]:
    if not results:
        return []

    total = len(results)
    dealer_values = [result.dealer_happiness for result in results if result.dealer_happiness is not None]
    dealer_avg = round(sum(dealer_values) / len(dealer_values)) if dealer_values else 0
    dealer_low = sum(1 for value in dealer_values if value < 78)
    gift_delivery_runs = sum(1 for result in results if result.gift_deliveries)
    marvin_item_runs = sum(1 for result in results if result.marvin_item_provenance)
    flask_runs = sum(1 for result in results if result.flask_purchases)
    whistle_runs = sum(1 for result in results if "Animal Whistle" in result.inventory)
    millionaire_visit_runs = sum(1 for result in results if result.millionaire_visited)
    doctor_runs = sum(1 for result in results if result.visited_doctor)
    pawn_runs = sum(1 for result in results if result.visited_pawn)
    loan_runs = sum(1 for result in results if result.visited_loan_shark)
    store_runs = sum(1 for result in results if result.visited_store)
    tom_runs = sum(1 for result in results if result.visited_tom)
    frank_runs = sum(1 for result in results if result.visited_frank)
    oswald_runs = sum(1 for result in results if result.visited_oswald)
    doctor_visits_total = sum(result.location_hits.get("doctor", 0) for result in results)
    store_visits_total = sum(result.location_hits.get("shop:convenience_store", 0) for result in results)
    pawn_visits_total = sum(result.location_hits.get("shop:pawn_shop", 0) for result in results)
    loan_visits_total = sum(result.location_hits.get("shop:loan_shark", 0) for result in results)
    marvin_visits_total = sum(result.location_hits.get("shop:marvin", 0) for result in results)
    witch_visits_total = sum(result.location_hits.get("doctor:witch", 0) for result in results)
    tom_visits_total = sum(result.location_hits.get("mechanic:tom", 0) for result in results)
    frank_visits_total = sum(result.location_hits.get("mechanic:frank", 0) for result in results)
    oswald_visits_total = sum(result.location_hits.get("mechanic:oswald", 0) for result in results)
    airport_visits_total = sum(result.location_hits.get("shop:airport", 0) for result in results)
    workbench_visits_total = sum(result.location_hits.get("shop:car_workbench", 0) for result in results)

    rows = [
        {
            "system": "doctor",
            "present": f"{sum(1 for result in results if result.ever_had_car)}/{total}",
            "engaged": f"{doctor_runs}/{total}",
            "payoff": f"{doctor_visits_total}",
            "notes": "car / doctor-runs / total-visits",
        },
        {
            "system": "store",
            "present": f"{sum(1 for result in results if result.ever_had_car)}/{total}",
            "engaged": f"{store_runs}/{total}",
            "payoff": f"{store_visits_total}",
            "notes": "car / store-runs / total-visits",
        },
        {
            "system": "pawn",
            "present": f"{sum(1 for result in results if result.met_gus or result.visited_pawn)}/{total}",
            "engaged": f"{pawn_runs}/{total}",
            "payoff": f"{pawn_visits_total}",
            "notes": "gus / pawn-runs / total-visits",
        },
        {
            "system": "loan",
            "present": f"{sum(1 for result in results if result.met_vinnie or result.visited_loan_shark)}/{total}",
            "engaged": f"{loan_runs}/{total}",
            "payoff": f"{loan_visits_total}",
            "notes": "vinnie / loan-runs / total-visits",
        },
        {
            "system": "marvin",
            "present": f"{sum(1 for result in results if result.marvin_access)}/{total}",
            "engaged": f"{sum(1 for result in results if result.visited_marvin)}/{total}",
            "payoff": f"{marvin_item_runs}/{total}",
            "notes": f"access / visit / item-run total-visits={marvin_visits_total}",
        },
        {
            "system": "gift-wrap",
            "present": f"{sum(1 for result in results if result.gift_system_unlocked)}/{total}",
            "engaged": f"{gift_delivery_runs}/{total}",
            "payoff": f"{dealer_low}/{total}",
            "notes": f"delivered / dealer<78 end / avg={dealer_avg}",
        },
        {
            "system": "workbench",
            "present": f"{sum(1 for result in results if result.has_tool_kit)}/{total}",
            "engaged": f"{sum(1 for result in results if result.visited_car_workbench)}/{total}",
            "payoff": f"{sum(1 for result in results if result.crafting_used)}/{total}",
            "notes": f"tool-kit / visit / crafted total-visits={workbench_visits_total}",
        },
        {
            "system": "tom",
            "present": f"{sum(1 for result in results if result.met_tom or result.visited_tom)}/{total}",
            "engaged": f"{tom_runs}/{total}",
            "payoff": f"{tom_visits_total}",
            "notes": "met / mechanic-runs / total-visits",
        },
        {
            "system": "frank",
            "present": f"{sum(1 for result in results if result.met_frank or result.visited_frank)}/{total}",
            "engaged": f"{frank_runs}/{total}",
            "payoff": f"{frank_visits_total}",
            "notes": "met / mechanic-runs / total-visits",
        },
        {
            "system": "oswald",
            "present": f"{sum(1 for result in results if result.met_oswald or result.visited_oswald)}/{total}",
            "engaged": f"{oswald_runs}/{total}",
            "payoff": f"{oswald_visits_total}",
            "notes": "met / mechanic-runs / total-visits",
        },
        {
            "system": "companions",
            "present": f"{whistle_runs}/{total}",
            "engaged": f"{sum(1 for result in results if result.companions_list)}/{total}",
            "payoff": f"{sum(1 for result in results if result.companion_acquired)}/{total}",
            "notes": "whistle / roster / befriended",
        },
        {
            "system": "witch",
            "present": f"{sum(1 for result in results if result.met_witch)}/{total}",
            "engaged": f"{sum(1 for result in results if result.visited_witch_doctor)}/{total}",
            "payoff": f"{flask_runs}/{total}",
            "notes": f"met / doctor / flask-buy total-visits={witch_visits_total}",
        },
        {
            "system": "millionaire",
            "present": f"{sum(1 for result in results if result.millionaire_reached)}/{total}",
            "engaged": f"{millionaire_visit_runs}/{total}",
            "payoff": f"{sum(1 for result in results if result.visited_airport)}/{total}",
            "notes": "reach / visitor / airport-runs",
        },
        {
            "system": "airport",
            "present": f"{sum(1 for result in results if result.millionaire_reached or result.visited_airport)}/{total}",
            "engaged": f"{sum(1 for result in results if result.visited_airport)}/{total}",
            "payoff": f"{airport_visits_total}",
            "notes": "unlock / airport-runs / total-visits",
        },
    ]

    lines = ["System Presence"]
    lines.extend(_build_text_table(
        [
            ("system", "system"),
            ("present", "present"),
            ("engaged", "engaged"),
            ("payoff", "payoff"),
            ("notes", "notes"),
        ],
        rows,
        {"present": "right", "engaged": "right", "payoff": "right"},
    ))
    lines.append("")
    return lines


def _mechanic_repair_lines(results: list[RunResult]) -> list[str]:
    """Which items were fixed at mechanics and how often mechanics visited."""
    if not results:
        return []

    total = len(results)
    mechanic_visits_total = sum(r.game_statistics.get("mechanic_visits", 0) for r in results)
    runs_with_mechanic = sum(1 for r in results if r.game_statistics.get("mechanic_visits", 0) > 0)

    # From marvin_provenance, collect items that were fixed
    fixed_items: Counter[str] = Counter()
    fixed_runs: Counter[str] = Counter()
    for r in results:
        for item_name, history in r.marvin_item_provenance.items():
            fixed = history.get("fixed", [])
            if fixed:
                fixed_items[item_name] += len(fixed)
                fixed_runs[item_name] += 1

    lines = [
        f"Mechanic Repair runs-visited={runs_with_mechanic}/{total} "
        f"total-mechanic-visits={mechanic_visits_total}"
    ]
    if fixed_items:
        lines.append("items fixed at mechanic:")
        for item_name, count in fixed_items.most_common(8):
            lines.append(f"  {item_name}: fixed {count}x in {fixed_runs[item_name]} runs")
    else:
        lines.append("no items fixed at mechanic recorded")
    lines.append("")
    return lines


def _append_section(lines: list[str], title: str) -> None:
    if lines and lines[-1] != "":
        lines.append("")
    lines.append(title)
    lines.append("-" * len(title))


def _named_ending_line(results: list[RunResult]) -> str:
    counts = Counter(
        result.terminal_ending_name or "unknown_ending"
        for result in results
        if result.outcome == "ending"
    )
    if not counts:
        return "Named endings none"
    return "Named endings " + " ".join(f"{name}={count}" for name, count in counts.most_common())


def _render_summary_lines(results: list[RunResult], cycles: int, seed_label: str) -> list[str]:
    metrics = _collect_summary(results)
    total = metrics["total"]

    lines = [
        f"AUTOTEST cycles={cycles} seeds={seed_label} total={total}",
        (
            "Outcomes "
            f"win={metrics['win']}/{total} "
            f"died={metrics['died']}/{total} "
            f"broke={metrics['broke']}/{total} "
            f"ending={metrics['ending']}/{total} "
            f"stalled={metrics['stalled']}/{total} "
            f"capped={metrics['capped']}/{total} "
            f"crash={metrics['crash']}/{total} "
            f"timeouts={metrics['timeouts']}/{total} "
            f"doctor_missed={metrics['doctor_missed']}"
        ),
        (
            "Progress "
            f"car={metrics['car']}/{total} "
            f"ever_car={metrics['ever_car']}/{total} "
            f"location={metrics['location']}/{total} "
            f"rank1+={metrics['rank1']}/{total} "
            f"clean={metrics['clean']}/{total}"
        ),
        (
            "Unlocks "
            f"map={metrics['map']}/{total} "
            f"worn_map={metrics['worn_map']}/{total} "
            f"marvin_access={metrics['marvin_access']}/{total} "
            f"witch={metrics['witch_access']}/{total} "
            f"gus={metrics['gus_access']}/{total} "
            f"vinnie={metrics['vinnie_access']}/{total} "
            f"million={metrics['million']}/{total}"
        ),
        (
            "Visits "
            f"doctor={metrics['doctor']}/{total} "
            f"witch_doctor={metrics['witch_doctor']}/{total} "
            f"store={metrics['store']}/{total} "
            f"pawn={metrics['pawn']}/{total} "
            f"loan={metrics['loan']}/{total} "
            f"marvin={metrics['marvin']}/{total} "
            f"tom={metrics['tom']}/{total} "
            f"frank={metrics['frank']}/{total} "
            f"oswald={metrics['oswald']}/{total} "
            f"upgrade={metrics['upgrade']}/{total} "
            f"crafting={metrics['crafting']}/{total} "
            f"companion={metrics['companion']}/{total} "
            f"adventure={metrics['adventure']}/{total} "
            f"airport={metrics['airport']}/{total} "
            f"mechanic_end={metrics['mechanic_end']}/{total} "
            f"airport_win={metrics['airport_win']}/{total} "
            f"wins={metrics['win']}/{total}"
        ),
        (
            "Presence "
            f"gift_unlock={metrics['gift_unlock']}/{total} "
            f"wrapped_gift={metrics['wrapped_gift']}/{total} "
            f"workbench_unlock={metrics['workbench_unlock']}/{total} "
            f"workbench_visit={metrics['workbench_visit']}/{total} "
            f"marvin_items={metrics['marvin_items']}/{total} "
            f"companion_roster={metrics['companion_roster']}/{total}"
        ),
        (
            "Outcome labels "
            "win=successful ending "
            "ending=named non-win terminal ending "
            "crash=unexpected runner/report failure "
            "capped=reached cycle limit"
        ),
        _named_ending_line(results),
        "",
    ]

    request_counts = Counter()
    request_context_counts = Counter()
    trace_counts = Counter()
    trace_context_counts = Counter()
    goal_counts = Counter()
    personality_counts = Counter()
    reason_code_counts = Counter()
    ev_weighted_total = 0.0
    ev_weighted_count = 0
    ev_global_max: float | None = None
    ev_global_min: float | None = None
    route_outcome_counts = Counter()
    route_interrupt_kind_counts = Counter()
    route_interrupted_goal_counts = Counter()
    route_interrupted_top_goal_counts = Counter()
    route_applied_goal_counts = Counter()
    route_suppressed_goal_counts = Counter()
    for result in results:
        request_counts.update(result.decision_request_counts)
        request_context_counts.update(result.decision_request_context_counts)
        trace_counts.update(result.decision_trace_counts)
        trace_context_counts.update(result.decision_trace_context_counts)
        goal_counts.update(result.decision_goal_counts)
        personality_counts.update(result.decision_personality_counts)
        reason_code_counts.update(result.decision_reason_code_counts)
        result_trace_total = sum(result.decision_trace_counts.values())
        if result_trace_total > 0 and result.decision_expected_value_avg is not None:
            ev_weighted_total += result.decision_expected_value_avg * result_trace_total
            ev_weighted_count += result_trace_total
        if result.decision_expected_value_max is not None:
            ev_global_max = result.decision_expected_value_max if ev_global_max is None else max(ev_global_max, result.decision_expected_value_max)
        if result.decision_expected_value_min is not None:
            ev_global_min = result.decision_expected_value_min if ev_global_min is None else min(ev_global_min, result.decision_expected_value_min)
        route_outcome_counts.update(result.route_outcome_counts)
        route_interrupt_kind_counts.update(result.route_interrupt_kind_counts)
        route_interrupted_goal_counts.update(result.route_interrupted_goal_counts)
        route_interrupted_top_goal_counts.update(result.route_interrupted_top_goal_counts)
        route_applied_goal_counts.update(result.route_applied_goal_counts)
        route_suppressed_goal_counts.update(result.route_suppressed_goal_counts)

    _append_section(lines, "Coverage & Routing")
    if request_counts or trace_counts:
        lines.append(
            "Decision Coverage "
            + f"requests={sum(request_counts.values())} "
            + f"traces={sum(trace_counts.values())}"
        )
        if request_counts:
            lines.append("Requests " + " ".join(f"{name}={count}" for name, count in request_counts.most_common(8)))
        if trace_counts:
            lines.append("Traces   " + " ".join(f"{name}={count}" for name, count in trace_counts.most_common(8)))
        if request_context_counts:
            lines.append("Contexts " + " ".join(f"{name}={count}" for name, count in request_context_counts.most_common(8)))
        if goal_counts:
            lines.append("Goals    " + " ".join(f"{name}={count}" for name, count in goal_counts.most_common(8)))
        if personality_counts:
            lines.append("Personalities " + " ".join(f"{name}={count}" for name, count in personality_counts.most_common(8)))
        if reason_code_counts:
            lines.append("Reason codes " + " ".join(f"{name}={count}" for name, count in reason_code_counts.most_common(10)))
        if ev_weighted_count > 0:
            ev_weighted_avg = ev_weighted_total / ev_weighted_count
            ev_max_text = f"{ev_global_max:.2f}" if ev_global_max is not None else "n/a"
            ev_min_text = f"{ev_global_min:.2f}" if ev_global_min is not None else "n/a"
            lines.append(
                "Expected value "
                + f"avg={ev_weighted_avg:.2f} max={ev_max_text} min={ev_min_text} samples={ev_weighted_count}"
            )
        if route_outcome_counts:
            lines.append("Route outcomes " + " ".join(f"{name}={count}" for name, count in route_outcome_counts.most_common(6)))
        if route_interrupt_kind_counts:
            lines.append("Route interrupts " + " ".join(f"{name}={count}" for name, count in route_interrupt_kind_counts.most_common(6)))
        if route_interrupted_goal_counts:
            lines.append("Blocked goals " + " ".join(f"{name}={count}" for name, count in route_interrupted_goal_counts.most_common(8)))
        if route_interrupted_top_goal_counts:
            lines.append("Interrupted top goals " + " ".join(f"{name}={count}" for name, count in route_interrupted_top_goal_counts.most_common(8)))
        if route_applied_goal_counts:
            lines.append("Applied routes " + " ".join(f"{name}={count}" for name, count in route_applied_goal_counts.most_common(8)))
        if route_suppressed_goal_counts:
            lines.append("Suppressed routes " + " ".join(f"{name}={count}" for name, count in route_suppressed_goal_counts.most_common(8)))
        lines.append("")

    lines.extend(_shop_summary_lines(results))
    lines.extend(_no_car_review_lines(results))
    lines.extend(_stagnation_audit_lines(results))
    lines.extend(_distribution_lines(results))
    lines.extend(_max_rank_cohort_lines(results))
    lines.extend(_system_presence_lines(results))

    _append_section(lines, "Seed Overview")
    row_data = []
    seed_snapshot = sorted(
        results,
        key=lambda result: (
            -(result.peak_balance or result.balance or 0),
            -(result.day or 0),
            -(result.balance or 0),
            result.seed,
        ),
    )
    for result in seed_snapshot:
        if result.timed_out:
            row_data.append({
                "seed": str(result.seed),
                "outcome": result.display_outcome,
                "car": "-",
                "end_rank": "-",
                "peak_rank": "-",
                "peak_balance": "-",
                "peak_days": "-",
                "end_day": "-",
                "end_balance": "-",
                "hp": "-",
                "san": "-",
                "route": "-",
            })
            continue

        top_destination = result.top_adventure if result.top_adventure != "none" else result.top_location
        if len(top_destination) > 23:
            top_destination = top_destination[:20] + "..."

        row_data.append({
            "seed": str(result.seed),
            "outcome": result.display_outcome,
            "car": "Y" if result.has_car else "N",
            "end_rank": str(result.rank) if result.rank is not None else "-",
            "peak_rank": str(result.peak_rank if result.peak_rank is not None else result.rank) if (result.peak_rank is not None or result.rank is not None) else "-",
            "peak_balance": _format_int(result.peak_balance if result.peak_balance is not None else result.balance),
            "peak_days": _format_peak_days(result.peak_balance_days),
            "end_day": str(result.day) if result.day is not None else "-",
            "end_balance": _format_int(result.balance),
            "hp": str(result.health) if result.health is not None else "-",
            "san": str(result.sanity) if result.sanity is not None else "-",
            "route": top_destination,
        })

    lines.append("all seeds ordered by peak balance, then run length")
    lines.extend(_build_text_table(
        [
            ("seed", "seed"),
            ("outcome", "outcome"),
            ("car", "car"),
            ("end_rank", "rank"),
            ("peak_rank", "peak-rank"),
            ("peak_balance", "peak$"),
            ("peak_days", "peak-days"),
            ("end_day", "end-day"),
            ("end_balance", "end$"),
            ("hp", "hp"),
            ("san", "san"),
            ("route", "top-route"),
        ],
        row_data,
        {
            "seed": "right",
            "car": "center",
            "end_rank": "right",
            "peak_rank": "right",
            "peak_balance": "right",
            "peak_days": "right",
            "end_day": "right",
            "end_balance": "right",
            "hp": "right",
            "san": "right",
        },
    ))

    lines.append("")

    death_groups = [result.death_group for result in results if result.outcome == "died"]
    if death_groups:
        lines.append("Deaths " + " ".join(
            f"{name}={count}" for name, count in Counter(death_groups).most_common(8)
        ))
        lines.append("")

    death_results = [result for result in results if result.outcome == "died"]
    bankrupt_results = [result for result in results if result.outcome == "broke"]
    completed_results = [result for result in results if not result.timed_out]
    lines.extend(_death_sorted_lines(
        results,
        "Top 10 Deaths By Run Length",
        sorted(death_results, key=lambda result: (-(result.day or 0), -(result.peak_balance or result.balance or 0), result.death_tag, result.seed))[:20],
        "day",
        "day",
    ))
    lines.extend(_death_sorted_lines(
        results,
        "Top 10 Deaths By Peak Balance",
        sorted(death_results, key=lambda result: (-(result.peak_balance or result.balance or 0), -(result.day or 0), result.death_tag, result.seed))[:20],
        "peak$",
        "peak",
    ))
    lines.extend(_run_sorted_lines(
        "Top 10 Bankrupts By Run Length",
        sorted(bankrupt_results, key=lambda result: (-(result.day or 0), -(result.peak_balance or result.balance or 0), result.seed)),
        "day",
        "day",
    ))
    lines.extend(_run_sorted_lines(
        "Top 10 Bankrupts By Peak Balance",
        sorted(bankrupt_results, key=lambda result: (-(result.peak_balance or result.balance or 0), -(result.day or 0), result.seed)),
        "peak$",
        "peak",
    ))
    lines.extend(_run_sorted_lines(
        "Top 10 Runs By Run Length",
        sorted(completed_results, key=lambda result: (-(result.day or 0), -(result.peak_balance or result.balance or 0), result.seed)),
        "day",
        "day",
    ))
    lines.extend(_run_sorted_lines(
        "Top 10 Runs By Peak Balance",
        sorted(completed_results, key=lambda result: (-(result.peak_balance or result.balance or 0), -(result.day or 0), result.seed)),
        "peak$",
        "peak",
    ))
    lines.extend(_run_sorted_lines(
        "Top 10 Runs By End Balance",
        sorted(completed_results, key=lambda result: (-(result.balance or 0), -(result.peak_balance or result.balance or 0), -(result.day or 0), result.seed)),
        "end$",
        "end_balance",
    ))

    ranked = [result for result in results if result.rank is not None]
    if ranked:
        best_peak = max(ranked, key=lambda result: (result.peak_balance or result.balance or 0, -(result.day or 0)))
        longest_run = max(ranked, key=lambda result: ((result.day or 0), result.balance or 0, result.peak_balance or 0))
        lines.append(
            f"Best peak    seed={best_peak.seed} peak={best_peak.peak_balance or best_peak.balance} peak_days={','.join(str(day) for day in best_peak.peak_balance_days) or '-'} rank={best_peak.peak_rank or best_peak.rank} final_day={best_peak.day} final_balance={best_peak.balance}"
        )
        lines.append(
            f"Longest run  seed={longest_run.seed} day={longest_run.day} balance={longest_run.balance} peak={longest_run.peak_balance or longest_run.balance} peak_days={','.join(str(day) for day in longest_run.peak_balance_days) or '-'} rank={longest_run.peak_rank or longest_run.rank}"
        )
        lines.append("")

    _append_section(lines, "Systems, Economy & Content")
    lines.extend(_medical_economy_lines(results))
    lines.extend(_event_economy_lines(results))
    lines.extend(_storyline_audit_lines(results))
    lines.extend(_adventure_lines(results))
    lines.extend(_dealings_lines(
        results,
        title="Convenience Store Dealings",
        source_prefixes=("location:shop:convenience_store",),
        out_label="removed",
    ))
    lines.extend(_dealings_lines(
        results,
        title="Pawn Shop Dealings",
        source_prefixes=("location:shop:pawn_shop",),
        out_label="sold",
    ))
    lines.extend(_marvin_provenance_lines(results))
    doctor_summary = _collect_medical_provider_summary(results, "doctor")
    witch_summary = _collect_medical_provider_summary(results, "doctor:witch")
    lines.extend(_condition_universe_lines(
        results,
        title="Illness Universe",
        universe=_known_status_universe(),
        final_attr="statuses",
        added_attr="statuses_added",
        removed_attr="statuses_removed",
        doctor_summary=doctor_summary,
        witch_summary=witch_summary,
    ))
    lines.extend(_condition_universe_lines(
        results,
        title="Injury Universe",
        universe=_known_injury_universe(),
        final_attr="injuries",
        added_attr="injuries_added",
        removed_attr="injuries_removed",
        doctor_summary=doctor_summary,
        witch_summary=witch_summary,
    ))
    lines.extend(_medical_provider_lines(results, "Doctor Visits", "doctor"))
    lines.extend(_medical_provider_lines(results, "Witch Doctor Visits", "doctor:witch"))
    lines.extend(_game_statistics_lines(results))
    lines.extend(_injury_illness_distribution_lines(results))
    lines.extend(_companion_roster_lines(results))
    lines.extend(_companion_state_lines(results))
    lines.extend(_loan_distribution_lines(results))
    lines.extend(_gambling_performance_lines(results))
    lines.extend(_flask_and_item_breakage_lines(results))
    lines.extend(_dealer_gift_lines(results))
    lines.extend(_mechanic_repair_lines(results))
    lines.extend(_mechanic_dream_progress_lines(results))
    lines.extend(_system_presence_lines(results))
    _append_section(lines, "Medical, Fatality & Diagnostics")
    lines.extend(_death_stage_audit_lines(results))
    lines.extend(_death_rank_audit_lines(results))
    lines.extend(_fatal_pressure_lines(results))
    lines.extend(_fatal_context_lines(results))
    lines.extend(_doctor_review_lines(results))
    lines.extend(_pawned_item_lines(results))
    lines.extend(_fallback_review_lines(results))
    lines.extend(_event_polarity_lines(results))
    lines.extend(_item_impact_lines(results))

    return lines


def _write_cumulative_report(lines: list[str]) -> None:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(CUMULATIVE_REPORT, "w", encoding="utf-8") as handle:
        handle.write(f"=== AUTOTEST RUN {timestamp} ===\n")
        handle.write("\n".join(lines))
        handle.write("\n")


def render_summary(results: list[RunResult], cycles: int, seed_label: str) -> None:
    lines = _render_summary_lines(results, cycles, seed_label)

    for line in lines:
        print(line)

    _write_cumulative_report(lines)


def main() -> int:
    cycles, seeds, seed_label = parse_args()
    total = len(seeds)
    results: list[RunResult] = []
    batch_started_at = time.perf_counter()
    stopped_early = False
    stopped_during_seed = False
    stop_seed: int | None = None

    start_line = f"AUTOTEST starting cycles={cycles} seeds={seed_label} total={total} timeout=90s/seed"
    if _supports_stop_key():
        start_line += f" | press '{STOP_KEY}' to stop early and keep completed runs"
    print(start_line, flush=True)
    for index, seed in enumerate(seeds, start=1):
        if _consume_stop_request():
            stopped_early = True
            stop_seed = seed
            break

        result, stop_requested = run_seed(cycles, seed)
        if stop_requested:
            stopped_early = True
            stopped_during_seed = True
            stop_seed = seed
            break

        if result is None:
            continue

        results.append(result)
        _render_live_progress(index, total, result, results, batch_started_at)

    if sys.stdout.isatty():
        print("", flush=True)

    if stopped_early:
        completed = len(results)
        location = f" during seed={stop_seed}" if stopped_during_seed and stop_seed is not None else ""
        print(
            f"AUTOTEST stop requested{location}; summarizing completed runs={completed}/{total}",
            flush=True,
        )

    render_summary(results, cycles, seed_label)

    if os.path.isfile(STORY_OUT) and results and not stopped_during_seed:
        last_completed_seed = results[-1].seed
        if len(results) == 1:
            print(f"Story log -> {STORY_OUT}  (seed={last_completed_seed} in-game narrative)", flush=True)
        else:
            print(
                f"Story log -> {STORY_OUT}  (last completed seed={last_completed_seed} in-game narrative; re-run quicktest.py for any specific seed)",
                flush=True,
            )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())