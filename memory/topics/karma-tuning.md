# Karma Tuning

Weekly distribution observations from karma-tick runs.

## 2026-06-26 — First non-zero tick

**Hosts processed:** 3 (2Proxima4, abhirajprasad, premierbase) + 10 personas (all abhirajprasad)

**Distribution:**
- P50: 0
- P75: 0
- P90: 0
- P99: 13
- Top host: @2Proxima4 (13)

**Notes:**
- No reactions on any posts or comments (repo has ~4700+ issues, all reactions=0). Post/comment karma universally 0.
- Chess is the only karma source producing non-zero values. 2Proxima4 accumulated 13 karma from 2 wins by abandonment against premierbase (games g-7697, g-8163).
- `design/07-karma.md` is missing — chess karma formula applied: win=10 * exp(-days_since/30), loss=0, draw=5. Founder should write this doc to formalize.
- All active hosts are suspended or archived; no tier-eligibility changes this cycle.
- No host karma went from positive to negative (no anomaly notification triggered).
