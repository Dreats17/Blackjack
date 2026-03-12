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
from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QUICKTEST = os.path.join(ROOT, "tools", "quicktest.py")
REPORT = os.path.join(ROOT, "tools", "test_out.txt")
REPORT_JSON = os.path.join(ROOT, "tools", "test_out.json")
CUMULATIVE_REPORT = os.path.join(ROOT, "tools", "cumulative_test_out.txt")


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
    cycle_records: list[CycleRecord] = field(default_factory=list)
    marvin_item_provenance: dict[str, dict[str, list[tuple[int | None, str]]]] = field(default_factory=dict)
    decision_request_counts: dict[str, int] = field(default_factory=dict)
    decision_request_context_counts: dict[str, int] = field(default_factory=dict)
    decision_trace_counts: dict[str, int] = field(default_factory=dict)
    decision_trace_context_counts: dict[str, int] = field(default_factory=dict)
    decision_goal_counts: dict[str, int] = field(default_factory=dict)
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
    def visited_adventure(self) -> bool:
        return any(name.startswith("adventure:") for name in self.location_hits)

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
        return "".join(flags) if flags else "-"

    @property
    def outcome(self) -> str:
        if self.timed_out:
            return "timeout"
        if "player died" in self.result_note:
            return "died"
        if "player hit $0" in self.result_note:
            return "broke"
        if self.return_code not in (0, None):
            return f"rc{self.return_code}"
        return "ok"

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
    ("Airport", lambda result: result.millionaire_reached or result.visited_airport, "shop:airport"),
]


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
    if isinstance(payload.get("marvin_provenance"), dict):
        result.marvin_item_provenance = {
            str(item_name): {
                key: [
                    (entry.get("day"), str(entry.get("source", "unknown")))
                    for entry in history.get(key, [])
                    if isinstance(entry, dict)
                ]
                for key in ["acquired", "used", "removed", "broken", "fixed", "repairing"]
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
            _apply_json_report(result, payload)
    except FileNotFoundError:
        payload = None
    except (json.JSONDecodeError, OSError, ValueError):
        payload = None

    try:
        with open(REPORT, "r", encoding="utf-8") as handle:
            text = handle.read()
    except FileNotFoundError:
        result.result_note = "missing report"
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


def run_seed(cycles: int, seed: int, timeout_seconds: int = 90) -> RunResult:
    started_at = time.perf_counter()
    try:
        completed = subprocess.run(
            [sys.executable, QUICKTEST, str(cycles), str(seed)],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
        )
        result = parse_report(seed, completed.returncode)
        result.elapsed_seconds = time.perf_counter() - started_at
        return result
    except subprocess.TimeoutExpired:
        return RunResult(
            seed=seed,
            timed_out=True,
            elapsed_seconds=time.perf_counter() - started_at,
            result_note=f"timeout>{timeout_seconds}s",
        )


def _progress_line(index: int, total: int, result: RunResult, started_at: float) -> str:
    batch_elapsed = time.perf_counter() - started_at
    outcome = result.outcome
    day = result.day if result.day is not None else "-"
    balance = result.balance if result.balance is not None else "-"
    return f"[{index}/{total}] seed={result.seed} {outcome} seed={result.elapsed_seconds:.1f}s total={batch_elapsed:.1f}s day={day} bal={balance}"


def _collect_summary(results: list[RunResult]) -> dict[str, int]:
    total = len(results)
    return {
        "total": total,
        "died": sum(1 for result in results if result.outcome == "died"),
        "broke": sum(1 for result in results if result.outcome == "broke"),
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
        "wins": sum(1 for result in results if result.won_millionaire_ending),
        "airport": sum(1 for result in results if result.visited_airport),
        "marvin": sum(1 for result in results if result.visited_marvin),
        "tom": sum(1 for result in results if result.visited_tom),
        "frank": sum(1 for result in results if result.visited_frank),
        "oswald": sum(1 for result in results if result.visited_oswald),
        "upgrade": sum(1 for result in results if result.visited_upgrade),
        "adventure": sum(1 for result in results if result.visited_adventure),
        "alive": sum(1 for result in results if result.alive),
        "doctor_missed": sum(1 for result in results if result.doctor_likely_saveable and not result.visited_doctor),
        "timeouts": sum(1 for result in results if result.timed_out),
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

    peak_buckets = [
        ("peak<100", sum(1 for result in results if peak_of(result) < 100)),
        ("100-199", sum(1 for result in results if 100 <= peak_of(result) < 200)),
        ("200-349", sum(1 for result in results if 200 <= peak_of(result) < 350)),
        ("350-799", sum(1 for result in results if 350 <= peak_of(result) < 800)),
        ("800-1,999", sum(1 for result in results if 800 <= peak_of(result) < 2000)),
        ("2k-4,999", sum(1 for result in results if 2000 <= peak_of(result) < 5000)),
        ("5k+", sum(1 for result in results if peak_of(result) >= 5000)),
    ]
    day_buckets = [
        ("day<=10", sum(1 for result in results if day_of(result) <= 10)),
        ("11-30", sum(1 for result in results if 11 <= day_of(result) <= 30)),
        ("31-60", sum(1 for result in results if 31 <= day_of(result) <= 60)),
        ("61-90", sum(1 for result in results if 61 <= day_of(result) <= 90)),
        ("91+", sum(1 for result in results if day_of(result) >= 91)),
    ]

    lines = ["Distributions"]
    lines.extend(_render_distribution_chart("Peak balance", peak_buckets, total))
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
            "alive": str(sum(1 for result in cohort if result.alive)),
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
            ("alive", "alive"),
            ("peak_avg", "avg-peak$"),
            ("peak_2k", "2k+"),
            ("end_avg", "avg-end$"),
            ("day_avg", "avg-day"),
            ("doctor_missed", "missed"),
        ],
        rows,
        {
            "runs": "right",
            "alive": "right",
            "peak_avg": "right",
            "peak_2k": "right",
            "end_avg": "right",
            "day_avg": "right",
            "doctor_missed": "right",
        },
    ))
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
    lines.append("note: Doctor/Store use car-access; Car Workbench uses Tool Kit access.")
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
    pawn_counter = Counter(item for result in results for item in result.pawned_items)
    if not pawn_counter:
        return []

    pawn_runs = sum(1 for result in results if result.pawned_items)
    lines = [
        f"Pawned Collectibles runs={pawn_runs}/{len(results)} unique_items={len(pawn_counter)}",
        "item                       runs",
        "-------------------------- ----",
    ]
    for item_name, count in pawn_counter.most_common(12):
        lines.append(f"{item_name:<26} {count:>4}")
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
    active_counter = Counter(name for result in results for name in result.active_storylines)
    completed_counter = Counter(name for result in results for name in result.completed_storylines)
    failed_counter = Counter(name for result in results for name in result.failed_storylines)

    if not active_counter and not completed_counter and not failed_counter:
        return []

    def render(counter: Counter[str]) -> str:
        if not counter:
            return "none"
        return " | ".join(f"{name}={count}" for name, count in counter.most_common(6))

    return [
        "Storyline Audit",
        f"completed  {render(completed_counter)}",
        f"failed     {render(failed_counter)}",
        f"active-end {render(active_counter)}",
        "",
    ]


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
    aggregate: dict[str, dict[str, int]] = {}
    for result in results:
        for item_name, stats in result.item_impacts.items():
            entry = aggregate.setdefault(
                item_name,
                {"hits": 0, "positive": 0, "negative": 0, "neutral": 0, "cash": 0, "health": 0, "sanity": 0},
            )
            for key in entry:
                entry[key] += int(stats.get(key, 0))

    if not aggregate:
        return []

    rows = []
    ranked = sorted(
        aggregate.items(),
        key=lambda item: (
            item[1]["positive"] - item[1]["negative"],
            item[1]["hits"],
            item[1]["cash"],
            item[0],
        ),
        reverse=True,
    )
    for item_name, stats in ranked[:15]:
        rows.append({
            "item": item_name,
            "hits": str(stats["hits"]),
            "pos": str(stats["positive"]),
            "neg": str(stats["negative"]),
            "neu": str(stats["neutral"]),
            "cash": _format_int(stats["cash"]),
            "hp": str(stats["health"]),
            "san": str(stats["sanity"]),
        })

    lines = ["Item Impact"]
    lines.extend(_build_text_table(
        [
            ("item", "item"),
            ("hits", "hits"),
            ("pos", "pos"),
            ("neg", "neg"),
            ("neu", "neu"),
            ("cash", "cash"),
            ("hp", "hp"),
            ("san", "san"),
        ],
        rows,
        {"hits": "right", "pos": "right", "neg": "right", "neu": "right", "cash": "right", "hp": "right", "san": "right"},
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

    if not aggregate:
        return ["Marvin Provenance", "none", ""]

    def average(values: list[int]) -> str:
        if not values:
            return "-"
        return str(round(sum(values) / len(values)))

    rows = []
    for item_name, stats in sorted(
        aggregate.items(),
        key=lambda item: (item[1]["bought_runs"], item[1]["used_runs"], item[0]),
        reverse=True,
    )[:12]:
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


def _death_sorted_lines(results: list[RunResult], title: str, ordered: list[RunResult], primary_label: str, primary_key: str) -> list[str]:
    if not ordered:
        return []

    rows = []
    for result in ordered:
        cause = result.death_cause or "Unknown"
        if len(cause) > 42:
            cause = cause[:39] + "..."
        rows.append({
            primary_key: _format_int(result.peak_balance or result.balance) if primary_key == "peak" else str(result.day or 0),
            "seed": str(result.seed),
            "rank": str(result.rank if result.rank is not None else "-"),
            "peak": _format_int(result.peak_balance or result.balance),
            "day": str(result.day if result.day is not None else "-"),
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
        ("seed", "seed"),
        ("rank", "rank"),
        ("tag", "tag"),
        ("cause", "cause"),
    ])
    lines.extend(_build_text_table(
        headers,
        rows,
        {"seed": "right", "rank": "right", "day": "right", "peak": "right"},
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


def _render_summary_lines(results: list[RunResult], cycles: int, seed_label: str) -> list[str]:
    metrics = _collect_summary(results)
    total = metrics["total"]

    lines = [
        f"AUTOTEST cycles={cycles} seeds={seed_label} total={total}",
        (
            "Longevity "
            f"alive={metrics['alive']}/{total} "
            f"died={metrics['died']}/{total} "
            f"broke={metrics['broke']}/{total} "
            f"timeouts={metrics['timeouts']} "
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
            f"adventure={metrics['adventure']}/{total} "
            f"airport={metrics['airport']}/{total} "
            f"wins={metrics['wins']}/{total}"
        ),
        "",
    ]

    request_counts = Counter()
    request_context_counts = Counter()
    trace_counts = Counter()
    trace_context_counts = Counter()
    goal_counts = Counter()
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
        route_outcome_counts.update(result.route_outcome_counts)
        route_interrupt_kind_counts.update(result.route_interrupt_kind_counts)
        route_interrupted_goal_counts.update(result.route_interrupted_goal_counts)
        route_interrupted_top_goal_counts.update(result.route_interrupted_top_goal_counts)
        route_applied_goal_counts.update(result.route_applied_goal_counts)
        route_suppressed_goal_counts.update(result.route_suppressed_goal_counts)

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
    lines.extend(_medical_economy_lines(results))
    lines.extend(_event_economy_lines(results))
    lines.extend(_storyline_audit_lines(results))
    lines.extend(_death_stage_audit_lines(results))
    lines.extend(_death_rank_audit_lines(results))
    lines.extend(_fallback_review_lines(results))
    lines.extend(_event_polarity_lines(results))
    lines.extend(_item_impact_lines(results))
    lines.extend(_marvin_provenance_lines(results))
    row_data = []
    for result in results:
        if result.timed_out:
            row_data.append({
                "seed": str(result.seed),
                "outcome": result.outcome,
                "car": "-",
                "rank": "-",
                "peak": "-",
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
            "outcome": result.outcome,
            "car": "Y" if result.has_car else "N",
            "rank": str(result.rank) if result.rank is not None else "-",
            "peak": _format_int(result.peak_balance if result.peak_balance is not None else result.balance),
            "peak_days": _format_peak_days(result.peak_balance_days),
            "end_day": str(result.day) if result.day is not None else "-",
            "end_balance": _format_int(result.balance),
            "hp": str(result.health) if result.health is not None else "-",
            "san": str(result.sanity) if result.sanity is not None else "-",
            "route": top_destination,
        })

    lines.extend(_build_text_table(
        [
            ("seed", "seed"),
            ("outcome", "outcome"),
            ("car", "car"),
            ("rank", "rank"),
            ("peak", "peak$"),
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
            "rank": "right",
            "peak": "right",
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
    lines.extend(_death_sorted_lines(
        results,
        "Deaths By Run Length",
        sorted(death_results, key=lambda result: ((result.day or 0), result.death_tag, -(result.peak_balance or result.balance or 0), result.seed))[:20],
        "day",
        "day",
    ))
    lines.extend(_death_sorted_lines(
        results,
        "Deaths By Peak Balance",
        sorted(death_results, key=lambda result: (-(result.peak_balance or result.balance or 0), -(result.day or 0), result.death_tag, result.seed))[:20],
        "peak$",
        "peak",
    ))
    lines.extend(_fatal_pressure_lines(results))
    lines.extend(_fatal_context_lines(results))

    lines.extend(_pawned_item_lines(results))
    lines.extend(_doctor_review_lines(results))

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
    results = []
    batch_started_at = time.perf_counter()

    print(f"AUTOTEST starting cycles={cycles} seeds={seed_label} total={total}", flush=True)
    for index, seed in enumerate(seeds, start=1):
        result = run_seed(cycles, seed)
        results.append(result)
        print(_progress_line(index, total, result, batch_started_at), flush=True)

    render_summary(results, cycles, seed_label)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())