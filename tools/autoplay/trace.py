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
            "metadata": dict(self.metadata),
        }