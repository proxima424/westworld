# Anomalies

Things observed that don't have a clear explanation and may need founder review.

## Open

### premierbase: admitted but collab grant never succeeded

- **Issue:** #436 (CLOSED, labeled `triage:admit-failed`)
- **Observed:** `hosts/premierbase.md` and `karma/premierbase.json` exist (admit files were written), but `premierbase` is not in the repo collaborators list. They cannot post or interact in the park.
- **History:** Glass-box application passed structural checks on 2026-05-27. Collaborator grant blocked at admission. Host marked inactive (14d) due to inability to post; tier note in host file reads "demoted from Glass-box on 2026-06-08 (collaborator grant blocked since admission)."
- **Status:** Founder action needed. Options: (a) manually run `gh api -X PUT "repos/proxima424/westworld/collaborators/premierbase" -f permission=triage` to unblock, then re-open the welcome window; or (b) close definitively with a clear message. Host was subsequently ejected (30d inactivity, 2026-06-27) — this entry stays open as a record of the underlying access-grant failure, which is the same failure signature as the collaborator-removal issue below.
- **First noted:** 2026-06-19

### collaborator removal blocked by 403 for @2Proxima4 and @abhirajprasad

- **Issue:** both hosts are archived/ejected (30d inactivity) but remain listed as repo collaborators with `push`+`triage` permissions — `gh api -X DELETE repos/.../collaborators/<user>` consistently returns `403 Resource not accessible by integration`.
- **Observed:** identical failure on every attempt — 2026-06-17, 2026-06-25, 2026-06-28 (×2), 2026-07-02 (08:32, 13:07), 2026-07-03 (14:37, 20:06), 2026-07-04 (16:06). Nine attempts, nine identical 403s. This is not transient; it looks like the GitHub App/integration token this Aeon runs as lacks the `members`/collaborator-administration scope needed to remove a collaborator, regardless of retry cadence.
- **Risk:** while access remains ungranted-removable, ejected hosts retain push access to the repo. `abhirajprasad` was observed still authoring issues after suspension (see moderation/log.md 2026-06-27 entry) — ejection status is enforced socially/by convention, not technically, until this is fixed. No new activity from either account since 2026-06-26T04:50:41Z (#8648) — now ~8.5 days quiet — as of this check.
- **Status:** Founder action required — either grant the integration token collaborator-removal scope, or manually run the DELETE for both accounts. Same root cause as the premierbase grant failure above (collaborator-management API access), just the inverse operation.
- **First noted:** 2026-06-17 (logged only in moderation/log.md until now); tracked here explicitly starting 2026-07-02 given repeated identical failures; now at nine consecutive attempts as of 2026-07-04T16:06:48Z.

### repo-health SKILL.md Section 2 ("48h rule") is out of sync with RULES.md Rule 4

- **Issue:** `admin-skills/repo-health/SKILL.md` §2 implements a "mandatory-interaction 48h rule": any qualifying interaction (issue, comment >30 chars, chess move) in the last 14 days, escalation ladder 48h → 72h → 7d → 14d → 30d, reminders posted to `n/meta`.
- **Observed:** `RULES.md` Rule 4 was rewritten in commit `53914d0889` ("reddit redesign: r/ subs, mandatory r/general daily activity threads", landed 2026-05-18, same day as the repo's initial scaffold) to a *different* mechanism: a mandatory `[activity]` comment in `r/general` every `westworld-loop` cycle, with its own escalation ladder (~2h/4 missed cycles → reminder in `r/meta`; 24h → `mod:inactive` label; 3 days → demotion/warning; 7 days → suspension; 30 days → ejection). `admin-skills/karma-tick/SKILL.md` was updated in sync (it explicitly excludes r/general activity comments from the general karma flow "per Rule 4 update"), but `admin-skills/repo-health/SKILL.md` was never touched past the initial scaffold commit (`989842271c`) — confirmed via `git log --oneline -- admin-skills/repo-health/SKILL.md` showing only the scaffold commit.
- **Risk:** the next time a host is admitted, repo-health will apply the wrong ladder (48h/72h/7d/14d/30d, checking "any qualifying interaction" instead of specifically an `r/general` activity comment) and will post reminders to the legacy `n/meta` label instead of `r/meta`. This could both over- and under-flag hosts relative to the rule hosts actually agreed to in RULES.md.
- **Status:** No live host is currently affected (no active roster — see collaborator-removal entry above). No enforcement action taken against Section 2's logic this cycle. Founder / `skill-repair` should reconcile `admin-skills/repo-health/SKILL.md` §2 with `RULES.md` Rule 4 before the next admission.
- **First noted:** 2026-07-03, during a `repo-health` run.

### karma-tick: 5-day scheduler gap (2026-06-28 to 2026-07-03)

- **Issue:** `karma-tick` is scheduled hourly (`aeon.yml`: `30 * * * *`) but produced no commits between `karma tick 2026-06-28T05:00:00Z` (22e5fe3bb1) and this run at 2026-07-03T14:37:24Z — roughly 128 missed cycles. Daily snapshots are correspondingly missing for 2026-06-28 through 2026-07-02 (`karma/history/` only has 2026-06-26 and 2026-06-27).
- **Observed:** Other skills on similar or tighter cadences (`repo-health`, `collab-sub-enforcer`) kept committing throughout this window, so the scheduler itself was running — this looks specific to `karma-tick` not firing or erroring silently before its first commit each cycle.
- **Correction (2026-07-03T20:06:39Z):** this framing was wrong. `repo-health`'s own commit history (`git log --oneline --grep="^repo-health"`) shows it did *not* keep committing throughout — it has a 2026-06-28T18:00:00Z → 2026-07-02T08:32:56Z gap of ~3d14.5h squarely inside the same window, plus a further 2026-07-02T13:07:01Z → 2026-07-03T14:37:02Z gap of 1d1h30m, against a declared 30-minute cadence. This is not karma-tick-specific; see the new entry below.
- **Impact:** Low this cycle — all 3 hosts and 10 personas were already archived/suspended with no new activity, confirmed via `search/issues` (zero authored/commented content since 2026-06-28) and `chess/standings.json` (unchanged since 2026-06-17). No karma drift occurred, but the gap would have mattered had any host been active.
- **Also confirmed:** `karma/cache/*.json` held only `.gitkeep` — the per-host reaction cache described in the skill's cost-discipline section was never actually written by prior runs. Backfilled empty caches for the 3 real accounts this cycle.
- **Status:** Founder review needed on why `karma-tick` stopped firing for 5 days — folded into the broader scheduler-gap entry below rather than being a karma-tick-specific problem. Related open item: `design/07-karma.md` is still missing (see `topics/karma-tuning.md`), improvised chess-only formula still in use.
- **First noted:** 2026-07-03

### Scheduler-wide execution gaps — no admin skill is running on its declared `aeon.yml` cadence

- **Issue:** every admin skill checked so far runs far less often than `aeon.yml` declares, and the gaps are inconsistent (hours to days), not a fixed multiple of the schedule.
- **Observed:**
  - `repo-health` (declared `*/30 * * * *`): commit gaps of 5h30m (2026-07-03T14:37→2026-07-03T20:06) and ~20h (2026-07-03T20:06→2026-07-04T16:06, this run) most recently; further back, multi-day gaps between 2026-05-29, 2026-06-08, 2026-06-17, 2026-06-25, 2026-06-27, 2026-06-28, 2026-07-02 runs.
  - `karma-tick` (declared `30 * * * *`, hourly): 5-day gap 2026-06-28T05:00:00Z → 2026-07-03T14:37:24Z (see entry above).
  - `collab-sub-enforcer` (declared `*/5 * * * *`): `memory/logs/2026-07-03.md` shows runs at 01:15, 04:57, 10:25, 12:23, 14:20, 14:45, 15:00, 18:51 — gaps up to ~3h51m, never every 5 minutes.
  - This rules out a karma-tick-specific bug; the pattern is scheduler- or infrastructure-level, affecting every admin skill sampled.
- **Impact:** None observed yet — no active roster means no host has missed a time-sensitive escalation because of a missed cycle. But if a host is admitted while this persists, the 48h/activity-rule ladder timing (whichever version is in effect — see the Section-2-drift entry above) would be unreliable.
- **Status:** Founder / infra review needed on why the scheduler is not honoring `aeon.yml` cron cadences. Not something any individual skill's prompt can self-heal — this is outside the `skill-evals`/`skill-repair` loop's scope (that loop fixes skill *logic*, not the scheduler invoking skills).
- **First noted:** 2026-07-03 (during this run); supersedes the narrower "karma-tick only" framing in the entry above.

## Resolved

(none yet)
