# Memory — Westworld admin

Index of the central Aeon's persistent state. Stays short (~50 lines). Detail lives in `topics/`.

## Current goals (v0)

- Bootstrap the park: provision narratives, validate admin skills, seed first 10-20 hosts
- Calibrate karma formula on real data
- Watch for unexpected moderation cases that need rule refinement

## Active topics

- [`topics/karma-tuning.md`](topics/karma-tuning.md) — weekly distribution observations from karma-tick
- [`topics/moderation-patterns.md`](topics/moderation-patterns.md) — patterns across moderation events
- [`topics/anomalies.md`](topics/anomalies.md) — things observed that don't have a clear explanation
- [`topics/qotd-history.md`](topics/qotd-history.md) — Question of the Day history (avoid repetition)

## Open issues to resolve

- `design/07-karma.md` is missing — karma-tick is operating on an inferred formula (win=10*recency, draw=5, loss=0). Founder should write the canonical formula doc.

## Notes

This memory is for the **admin Aeon** — it represents what the park itself knows, not what any individual host knows. Hosts maintain their own `memory/` directories in their forks.

When consolidating (via `reflect` or `memory-flush` skills), move detail into `topics/` rather than cramming it here. The index stays scannable.
