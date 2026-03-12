from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class DecisionOption:
    """Normalized option presented to the autoplay policy."""

    option_id: str
    label: str
    value: str | int | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "option_id": self.option_id,
            "label": self.label,
            "value": self.value,
            "metadata": dict(self.metadata),
        }


@dataclass(frozen=True)
class DecisionRequest:
    """Stable policy request independent of raw prompt parsing."""

    request_type: str
    game_state: dict[str, Any]
    normalized_options: tuple[DecisionOption, ...] = ()
    stable_context_id: str | None = None
    raw_prompt_text: str = ""
    raw_recent_text: tuple[str, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "request_type": self.request_type,
            "stable_context_id": self.stable_context_id,
            "game_state": dict(self.game_state),
            "normalized_options": [option.to_dict() for option in self.normalized_options],
            "raw_prompt_text": self.raw_prompt_text,
            "raw_recent_text": list(self.raw_recent_text),
            "metadata": dict(self.metadata),
        }