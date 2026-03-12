GAMEPLAY FAIRNESS CHANGELOG
Date started: 2026-03-11

Purpose
- This file records player-facing fairness and balance changes that were surfaced or justified by autoplay benchmarking and seeded audit work.
- This is not the same as benchmark reporting.
- Benchmark details and fixed-seed evidence belong in tools/autotest_audit.txt.
- This file should stay human-readable and explain what changed for players and why.

How to use this file
- Add an entry when gameplay was made more fair, more legible, or less arbitrarily punitive.
- Note the affected system, the practical player impact, and the audit reason.
- Keep entries concise.

Entries

2026-03-11
System: Carbon monoxide day-dark event
Change:
- First exposure was changed from a flat arbitrary death spike into a survivable hazard.
- Ongoing danger was pushed into the existing damaged exhaust follow-up chain instead of front-loading lethality.
Why:
- Seeded benchmark evidence showed that the old branch behaved like an avoidability-poor post-car death spike rather than a fair escalating risk.
Player impact:
- First exposure is no longer an opaque instant run-ender.
- The event still matters, but the player now has a more legible chance to survive and deal with the consequence.

2026-03-11
System: Early no-car betting and robbery handling
Change:
- Early no-car bankroll handling was made more conservative around key car thresholds.
- Robbery autoplay was aligned toward the safer hide branch.
Why:
- Seeded audit work showed that some early failures were being caused by avoidable policy overreach rather than meaningful strategic pressure.
Player impact:
- Early survival and car acquisition windows behave more like defensible human play rather than reckless benchmark noise.

Planned future entry categories
- Rebalanced repeatable nuisance events
- Positive progression events made strong enough to matter
- Underpowered mechanics made visible or more rewarding
- Broken or non-appearing mechanics repaired in core gameplay