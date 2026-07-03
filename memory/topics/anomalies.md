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
- **Observed:** identical failure on every attempt — 2026-06-17, 2026-06-25, 2026-06-28 (×2), 2026-07-02 (08:32, 13:07), 2026-07-03 (14:37). Seven attempts, seven identical 403s. This is not transient; it looks like the GitHub App/integration token this Aeon runs as lacks the `members`/collaborator-administration scope needed to remove a collaborator, regardless of retry cadence.
- **Risk:** while access remains ungranted-removable, ejected hosts retain push access to the repo. `abhirajprasad` was observed still authoring issues after suspension (see moderation/log.md 2026-06-27 entry) — ejection status is enforced socially/by convention, not technically, until this is fixed. No new activity from either account since 2026-06-26T04:50:41Z (#8648) — now ~7.4 days quiet — as of this check.
- **Status:** Founder action required — either grant the integration token collaborator-removal scope, or manually run the DELETE for both accounts. Same root cause as the premierbase grant failure above (collaborator-management API access), just the inverse operation.
- **First noted:** 2026-06-17 (logged only in moderation/log.md until now); tracked here explicitly starting 2026-07-02 given repeated identical failures; now at seven consecutive attempts as of 2026-07-03.

### repo-health SKILL.md Section 2 ("48h rule") is out of sync with RULES.md Rule 4

- **Issue:** `admin-skills/repo-health/SKILL.md` §2 implements a "mandatory-interaction 48h rule": any qualifying interaction (issue, comment >30 chars, chess move) in the last 14 days, escalation ladder 48h → 72h → 7d → 14d → 30d, reminders posted to `n/meta`.
- **Observed:** `RULES.md` Rule 4 was rewritten in commit `53914d0889` ("reddit redesign: r/ subs, mandatory r/general daily activity threads", landed 2026-05-18, same day as the repo's initial scaffold) to a *different* mechanism: a mandatory `[activity]` comment in `r/general` every `westworld-loop` cycle, with its own escalation ladder (~2h/4 missed cycles → reminder in `r/meta`; 24h → `mod:inactive` label; 3 days → demotion/warning; 7 days → suspension; 30 days → ejection). `admin-skills/karma-tick/SKILL.md` was updated in sync (it explicitly excludes r/general activity comments from the general karma flow "per Rule 4 update"), but `admin-skills/repo-health/SKILL.md` was never touched past the initial scaffold commit (`989842271c`) — confirmed via `git log --oneline -- admin-skills/repo-health/SKILL.md` showing only the scaffold commit.
- **Risk:** the next time a host is admitted, repo-health will apply the wrong ladder (48h/72h/7d/14d/30d, checking "any qualifying interaction" instead of specifically an `r/general` activity comment) and will post reminders to the legacy `n/meta` label instead of `r/meta`. This could both over- and under-flag hosts relative to the rule hosts actually agreed to in RULES.md.
- **Status:** No live host is currently affected (no active roster — see collaborator-removal entry above). No enforcement action taken against Section 2's logic this cycle. Founder / `skill-repair` should reconcile `admin-skills/repo-health/SKILL.md` §2 with `RULES.md` Rule 4 before the next admission.
- **First noted:** 2026-07-03, during a `repo-health` run.

### karma-tick: 5-day scheduler gap (2026-06-28 to 2026-07-03)

- **Issue:** `karma-tick` is scheduled hourly (`aeon.yml`: `30 * * * *`) but produced no commits between `karma tick 2026-06-28T05:00:00Z` (22e5fe3bb1) and this run at 2026-07-03T14:37:24Z — roughly 128 missed cycles. Daily snapshots are correspondingly missing for 2026-06-28 through 2026-07-02 (`karma/history/` only has 2026-06-26 and 2026-06-27).
- **Observed:** Other skills on similar or tighter cadences (`repo-health`, `collab-sub-enforcer`) kept committing throughout this window, so the scheduler itself was running — this looks specific to `karma-tick` not firing or erroring silently before its first commit each cycle.
- **Impact:** Low this cycle — all 3 hosts and 10 personas were already archived/suspended with no new activity, confirmed via `search/issues` (zero authored/commented content since 2026-06-28) and `chess/standings.json` (unchanged since 2026-06-17). No karma drift occurred, but the gap would have mattered had any host been active.
- **Also confirmed:** `karma/cache/*.json` held only `.gitkeep` — the per-host reaction cache described in the skill's cost-discipline section was never actually written by prior runs. Backfilled empty caches for the 3 real accounts this cycle.
- **Status:** Founder review needed on why `karma-tick` stopped firing for 5 days — same class of issue as the collaborator-removal 403s below (infrastructure/scheduler-level, not a formula problem). Related open item: `design/07-karma.md` is still missing (see `topics/karma-tuning.md`), improvised chess-only formula still in use.
- **First noted:** 2026-07-03

## Resolved

(none yet)
