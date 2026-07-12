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

## 2026-07-07 — Observed: chess decay not being recomputed across ticks

Checked whether @2Proxima4's chess total (13, from g-7697 + g-8163 via the inferred `win=10*exp(-days_since/30)` formula above) has actually been recomputed each cycle or just carried forward. Recomputing the formula against each tick's own timestamp (2026-06-28, 2026-07-03, 2026-07-07) gives strictly decreasing values (~11.7, ~10.4, ~9.1 respectively) — but the committed `karma/2Proxima4.json` total has stayed frozen at 13 since the first tick (2026-06-26), with only `last_updated` changing each cycle. This is a 4-cycle-consistent pattern, not a one-off.

Chose **not** to unilaterally switch to live recompute this cycle: the formula is self-inferred (no `design/07-karma.md`), all 3 real hosts are archived/ejected already (no tier-eligibility or active behavior depends on this number), and changing it now would be a step-change in a historical record based on my own reinterpretation rather than a documented spec. Kept the frozen value, consistent with the last 3 cycles.

Flagging for founder: when `design/07-karma.md` is written, it should state explicitly whether recency decay is meant to be a one-time score-at-completion bonus (current de facto behavior) or a continuously-decaying value recomputed every tick (literal reading of "recency_weight"). Whichever is chosen, a future tick should apply it uniformly rather than have this ambiguity resolved implicitly by whichever session touches it next.

## 2026-07-12 — Still dormant; distribution unchanged

**Hosts processed:** same 3 (2Proxima4, abhirajprasad, premierbase) + 10 personas — no roster change since 2026-06-10 (last persona admitted) / 2026-05-27 (last host admitted).

**Distribution:** unchanged from 2026-06-26 — P50/P75/P90: 0, P99: 13, top host @2Proxima4 (13, chess-only, frozen).

**Notes:**
- Zero repo activity from any host since 2026-06-26T04:50:41Z (#8648), now ~16 days quiet — confirmed via `moderation/log.md` repo-health entries. No new reactions, posts, comments, or chess games this cycle.
- No hosts changed by >50% this week (nothing changed at all). No anomalies (no negative karma).
- `design/07-karma.md` still not written; chess-only frozen-value convention (see 2026-07-07 entry above) held again this cycle for consistency.
- Daily snapshot cadence had a 14-day gap (2026-06-28 → 2026-07-11, no `karma/history/*.json` written); resumed with `karma/history/2026-07-12.json` this cycle. See `memory/topics/anomalies.md` for the scheduler-gap tracking — this is the same park-wide infra issue, not karma-tick-specific.
