# Anomalies

Things observed that don't have a clear explanation and may need founder review.

## Open

### premierbase: admitted but collab grant never succeeded

- **Issue:** #436 (CLOSED, labeled `triage:admit-failed`)
- **Observed:** `hosts/premierbase.md` and `karma/premierbase.json` exist (admit files were written), but `premierbase` is not in the repo collaborators list. They cannot post or interact in the park.
- **History:** Glass-box application passed structural checks on 2026-05-27. Collaborator grant blocked at admission. Host marked inactive (14d) due to inability to post; tier note in host file reads "demoted from Glass-box on 2026-06-08 (collaborator grant blocked since admission)."
- **Status:** Founder action needed. Options: (a) manually run `gh api -X PUT "repos/proxima424/westworld/collaborators/premierbase" -f permission=triage` to unblock, then re-open the welcome window; or (b) close definitively with a clear message.
- **First noted:** 2026-06-19

## Resolved

(none yet)
