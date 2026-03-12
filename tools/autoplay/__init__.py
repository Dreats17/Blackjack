"""Structured autoplay interfaces and state snapshots."""

from .interfaces import DecisionOption, DecisionRequest
from .planner import StrategicPlan, choose_strategic_goal
from .route_policy import choose_route_option
from .state import GameState, build_game_state_snapshot
from .trace import DecisionTrace

__all__ = [
    "DecisionOption",
    "DecisionRequest",
    "DecisionTrace",
    "GameState",
    "StrategicPlan",
    "build_game_state_snapshot",
    "choose_route_option",
    "choose_strategic_goal",
]