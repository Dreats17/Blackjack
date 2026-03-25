from __future__ import annotations

import json
import os
from functools import lru_cache
from typing import Any


def _flatten(prefix: str, value: Any, out: dict[str, Any]) -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            name = str(key)
            full = f"{prefix}.{name}" if prefix else name
            _flatten(full, child, out)
        return
    out[prefix] = value


def _load_raw_overrides() -> dict[str, Any]:
    merged: dict[str, Any] = {}

    raw_json = os.environ.get("AUTOPLAY_TUNING_JSON", "").strip()
    if raw_json:
        try:
            payload = json.loads(raw_json)
            if isinstance(payload, dict):
                _flatten("", payload, merged)
        except json.JSONDecodeError:
            pass

    file_path = os.environ.get("AUTOPLAY_TUNING_FILE", "").strip()
    if file_path:
        try:
            with open(file_path, "r", encoding="utf-8") as handle:
                payload = json.load(handle)
            if isinstance(payload, dict):
                file_values: dict[str, Any] = {}
                _flatten("", payload, file_values)
                merged.update(file_values)
        except (OSError, json.JSONDecodeError):
            pass

    return merged


@lru_cache(maxsize=1)
def get_overrides() -> dict[str, Any]:
    return _load_raw_overrides()


def tval(key: str, default: Any) -> Any:
    value = get_overrides().get(key, default)
    if value is default:
        return default

    if isinstance(default, bool):
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            lowered = value.strip().lower()
            if lowered in {"1", "true", "yes", "on"}:
                return True
            if lowered in {"0", "false", "no", "off"}:
                return False
        if isinstance(value, (int, float)):
            return bool(value)
        return default

    if isinstance(default, int) and not isinstance(default, bool):
        try:
            return int(value)
        except (TypeError, ValueError):
            return default

    if isinstance(default, float):
        try:
            return float(value)
        except (TypeError, ValueError):
            return default

    if isinstance(default, str):
        return str(value)

    return value


def tscale(key: str, base_value: float, *, minimum: float = 0.0, maximum: float = 10.0) -> float:
    scaled = base_value * float(tval(key, 1.0))
    if scaled < minimum:
        return minimum
    if scaled > maximum:
        return maximum
    return scaled
