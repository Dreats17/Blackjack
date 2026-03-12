from __future__ import annotations

import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from tools.autoplay.scenario_cases import run_all_scenarios


OUT_PATH = os.path.join(ROOT, "tools", "autoplay_scenarios.json")


def main() -> int:
    results = run_all_scenarios()
    total = len(results)
    passed = sum(1 for result in results if result.passed)
    failed = total - passed

    grouped: dict[str, list[dict[str, object]]] = {}
    for result in results:
        grouped.setdefault(result.suite, []).append(
            {
                "scenario_id": result.scenario_id,
                "passed": result.passed,
                "summary": result.summary,
                "details": result.details,
            }
        )

    payload = {
        "summary": {
            "total": total,
            "passed": passed,
            "failed": failed,
        },
        "suites": grouped,
    }

    with open(OUT_PATH, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)

    print(f"AUTOPLAY SCENARIOS total={total} passed={passed} failed={failed}")
    for suite_name in sorted(grouped):
        suite_results = grouped[suite_name]
        suite_failed = sum(1 for item in suite_results if not item["passed"])
        print(f"suite={suite_name} total={len(suite_results)} failed={suite_failed}")
        for item in suite_results:
            status = "PASS" if item["passed"] else "FAIL"
            print(f"  [{status}] {item['scenario_id']}: {item['summary']}")

    print(f"Scenario results -> {OUT_PATH}")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())