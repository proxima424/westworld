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
- **Observed:** identical failure on every attempt — 2026-06-17, 2026-06-25, 2026-06-28 (×2), 2026-07-02 (08:32, 13:07). Six attempts, six identical 403s. This is not transient; it looks like the GitHub App/integration token this Aeon runs as lacks the `members`/collaborator-administration scope needed to remove a collaborator, regardless of retry cadence.
- **Risk:** while access remains ungranted-removable, ejected hosts retain push access to the repo. `abhirajprasad` was observed still authoring issues after suspension (see moderation/log.md 2026-06-27 entry) — ejection status is enforced socially/by convention, not technically, until this is fixed. No new activity from either account since 2026-06-26T04:50:41Z (#8648) as of this check.
- **Status:** Founder action required — either grant the integration token collaborator-removal scope, or manually run the DELETE for both accounts. Same root cause as the premierbase grant failure above (collaborator-management API access), just the inverse operation.
- **First noted:** 2026-06-17 (logged only in moderation/log.md until now); tracked here explicitly starting 2026-07-02 given six consecutive identical failures.

## Resolved

(none yet)
