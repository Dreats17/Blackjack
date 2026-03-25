from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class DecisionTrace:
    """Machine-readable explanation for one autoplay decision."""

    cycle: int | None
    day: int | None
    context: str
    request_type: str
    strategic_goal: str | None
    chosen_action: str
    reason: str
    confidence: float
    options: tuple[str, ...] = ()
    game_state_summary: dict[str, Any] = field(default_factory=dict)
    score_breakdown: dict[str, float] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        try:
            from tools.autoplay.policies.version import HANDLER_VERSION
        except Exception:
            HANDLER_VERSION = "unknown"
        meta = dict(self.metadata) if self.metadata else {}
        meta["handler_version"] = HANDLER_VERSION
        return {
            "cycle": self.cycle,
            "day": self.day,
            "context": self.context,
            "request_type": self.request_type,
            "strategic_goal": self.strategic_goal,
            "chosen_action": self.chosen_action,
            "reason": self.reason,
            "confidence": self.confidence,
            "options": list(self.options),
            "game_state_summary": dict(self.game_state_summary),
            "score_breakdown": dict(self.score_breakdown),
            "metadata": meta,
        }