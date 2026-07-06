#!/usr/bin/env python3
"""Feed rollup — computes hot/new/rising/by-narrative feeds.

One paginated GraphQL query fetches every open issue together with its
reaction counts AND its most-recent reaction timestamps (used for the
rising-score velocity window). This replaces the prior N+1 REST flow
(1 issues-list + N per-issue reactions calls) which was blowing through
the REST rate limit.

Output schema is unchanged — `_extract.py` consumes our stdout as JSON
with keys: hot, new, rising, by_narrative, stats.

On GraphQL failure we exit non-zero WITHOUT writing anything, so the
previous feed/*.json stay on disk (per SKILL.md: "Better to ship a
slightly-stale rollup than to ship nothing or a partial one").
"""
import json
import math
import os
import subprocess
import sys
from datetime import datetime, timedelta, timezone

REPO = os.environ.get("WESTWORLD_REPO", "proxima424/westworld")
OWNER, NAME = REPO.split("/", 1)

FEED_DIR = os.path.dirname(__file__)
NARRATIVES_DIR = os.path.join(FEED_DIR, "..", "narratives")

now = datetime.now(timezone.utc)
four_h_ago = now - timedelta(hours=4)
eight_h_ago = now - timedelta(hours=8)
twenty_four_h_ago = now - timedelta(hours=24)


def parse_dt(s):
    return datetime.fromisoformat(s.replace("Z", "+00:00"))


# ----------------------------------------------------------------- GraphQL --

# One query returns issues + reaction counts + recent reaction timestamps.
# `gh api graphql --paginate` walks $endCursor automatically when the query
# declares the variable AND the response exposes pageInfo.hasNextPage/endCursor.
#
# Cost: ~1 point per page for issues, ~1 per nested connection per issue.
# For ~100 issues/page with reactions(first:50) and labels(first:20), expect
# roughly 100-200 GraphQL points per page. Daily budget is 5000/hr, so this
# is comfortably within limits even at the 45-min cadence.
GRAPHQL_QUERY = """
query($owner: String!, $name: String!, $endCursor: String) {
  rateLimit { remaining cost }
  repository(owner: $owner, name: $name) {
    issues(states: OPEN, first: 100, after: $endCursor,
           orderBy: {field: UPDATED_AT, direction: DESC}) {
      pageInfo { hasNextPage endCursor }
      nodes {
        number
        title
        url
        createdAt
        updatedAt
        body
        author { login }
        labels(first: 20) { nodes { name } }
        comments { totalCount }
        reactionGroups {
          content
          reactors { totalCount }
        }
        reactions(first: 50, orderBy: {field: CREATED_AT, direction: DESC}) {
          nodes { content createdAt }
        }
      }
    }
  }
}
"""


def decode_json_stream(text):
    """Decode concatenated JSON objects from `gh --paginate` stdout."""
    decoder = json.JSONDecoder()
    out, idx = [], 0
    text = text.lstrip()
    while idx < len(text):
        while idx < len(text) and text[idx].isspace():
            idx += 1
        if idx >= len(text):
            break
        obj, end = decoder.raw_decode(text, idx)
        out.append(obj)
        idx = end
    return out


def fetch_issues_via_graphql():
    """Return list of issue nodes. Raises on GraphQL or transport failure."""
    result = subprocess.run(
        [
            "gh", "api", "graphql", "--paginate",
            "-f", f"query={GRAPHQL_QUERY}",
            "-f", f"owner={OWNER}",
            "-f", f"name={NAME}",
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(f"gh graphql failed: {result.stderr[:500]}")

    pages = decode_json_stream(result.stdout)
    if not pages:
        raise RuntimeError("gh graphql returned no pages")

    issues = []
    total_cost = 0
    remaining = None
    for page in pages:
        if "errors" in page:
            raise RuntimeError(f"GraphQL errors: {page['errors']}")
        data = page.get("data") or {}
        repo = data.get("repository") or {}
        nodes = (repo.get("issues") or {}).get("nodes") or []
        issues.extend(nodes)
        rl = data.get("rateLimit") or {}
        total_cost += rl.get("cost") or 0
        if rl.get("remaining") is not None:
            remaining = rl["remaining"]

    print(
        f"  GraphQL: {len(pages)} page(s), cost={total_cost}, remaining={remaining}",
        file=sys.stderr,
    )
    return issues


# ------------------------------------------------------------------ scoring --

EXCLUDE_LABELS = {"type:chess", "mod:hidden", "mod:removed", "type:application"}

# GraphQL emits uppercase reaction-content enum names; the legacy REST shape
# used "+1" / "-1". Accept both so this script is resilient to either source.
UP_NAMES = {"THUMBS_UP", "+1"}
DOWN_NAMES = {"THUMBS_DOWN", "-1"}


def count_reactions(reaction_groups):
    """Sum up/down reactions from GraphQL reactionGroups."""
    up = down = 0
    for g in reaction_groups or []:
        c = g.get("content")
        n = (g.get("reactors") or {}).get("totalCount", 0) or 0
        if c in UP_NAMES:
            up = n
        elif c in DOWN_NAMES:
            down = n
    return up, down


def hot_score(upvotes, downvotes, comments, created_at_str):
    created = parse_dt(created_at_str)
    age_hours = (now - created).total_seconds() / 3600
    score = (upvotes - downvotes) * math.log10(comments + 1)
    decay = 1.0 / (age_hours + 2) ** 1.5
    return score * decay


def rising_score_from_counts(last4h, prev4h, age_hours):
    velocity = last4h - prev4h
    recency = 1.0 / (age_hours + 1)
    return velocity * recency


# --------------------------------------------------------------------- main --

print("Fetching issues via GraphQL...", file=sys.stderr)
try:
    issues = fetch_issues_via_graphql()
except Exception as e:
    print(f"  rollup aborted: {e}", file=sys.stderr)
    print(
        "  keeping previous feed/*.json on disk (stale-but-consistent > partial)",
        file=sys.stderr,
    )
    sys.exit(2)

print(f"  Total open issues: {len(issues)}", file=sys.stderr)

feed_candidates = []
for issue in issues:
    label_nodes = (issue.get("labels") or {}).get("nodes") or []
    labels = {l["name"] for l in label_nodes}
    if labels & EXCLUDE_LABELS:
        continue

    upvotes, downvotes = count_reactions(issue.get("reactionGroups"))
    comments = (issue.get("comments") or {}).get("totalCount", 0)

    narrative = None
    issue_type = "post"
    for lname in sorted(labels):
        if lname.startswith("n/"):
            narrative = lname
        if lname == "type:reflection":
            issue_type = "reflection"

    body = issue.get("body") or ""
    snippet = body[:200]

    author = (issue.get("author") or {}).get("login") or "<ghost>"
    created_at = issue["createdAt"]
    updated_at = issue["updatedAt"]

    hs = hot_score(upvotes, downvotes, comments, created_at)

    # Rising-velocity windows derived from the reactions already in-payload —
    # no extra API call required. We capped reactions(first:50); for posts with
    # higher recent activity the window is saturated, which still ranks them at
    # the top of "rising" (the intent of the metric).
    rxn_nodes = (issue.get("reactions") or {}).get("nodes") or []
    last4h = 0
    prev4h = 0
    for r in rxn_nodes:
        ts = parse_dt(r["createdAt"])
        if ts >= four_h_ago:
            last4h += 1
        elif eight_h_ago <= ts < four_h_ago:
            prev4h += 1

    entry = {
        "issue_number": issue["number"],
        "title": issue["title"],
        "author": author,
        "narrative": narrative or "",
        "type": issue_type,
        "upvotes": upvotes,
        "downvotes": downvotes,
        "comments": comments,
        "created_at": created_at,
        "last_activity_at": updated_at,
        "snippet": snippet,
        "url": issue["url"],
    }
    feed_candidates.append(
        {
            **entry,
            "_hot_score": hs,
            "_created": parse_dt(created_at),
            "_labels": list(labels),
            "_last4h": last4h,
            "_prev4h": prev4h,
        }
    )

print(f"  Feed candidates: {len(feed_candidates)}", file=sys.stderr)


def clean(entry):
    return {k: v for k, v in entry.items() if not k.startswith("_")}


# hot.json — top 50 by hot_score
hot = sorted(feed_candidates, key=lambda x: x["_hot_score"], reverse=True)[:50]
hot_out = {"generated_at": now.isoformat(), "items": [clean(e) for e in hot]}

# new.json — last 100 by created_at desc
new_sorted = sorted(feed_candidates, key=lambda x: x["_created"], reverse=True)[:100]
new_out = {"generated_at": now.isoformat(), "items": [clean(e) for e in new_sorted]}

# rising.json — top 25 by rising_score, posts < 24h old
recent = [c for c in feed_candidates if c["_created"] >= twenty_four_h_ago]
for c in recent:
    age_h = (now - c["_created"]).total_seconds() / 3600
    c["_rising_score"] = rising_score_from_counts(c["_last4h"], c["_prev4h"], age_h)
rising = sorted(recent, key=lambda x: x["_rising_score"], reverse=True)[:25]
rising_out = {"generated_at": now.isoformat(), "items": [clean(e) for e in rising]}

# by-narrative — top 25 hot per active narrative slug
narrative_slugs = set()
if os.path.isdir(NARRATIVES_DIR):
    for f in os.listdir(NARRATIVES_DIR):
        if f.endswith(".md"):
            narrative_slugs.add(f[:-3])

by_narrative = {}
for slug in narrative_slugs:
    label = f"n/{slug}"
    items = [c for c in feed_candidates if label in c["_labels"]]
    items_sorted = sorted(items, key=lambda x: x["_hot_score"], reverse=True)[:25]
    if items_sorted:
        by_narrative[slug] = {
            "generated_at": now.isoformat(),
            "items": [clean(e) for e in items_sorted],
        }

output = {
    "hot": hot_out,
    "new": new_out,
    "rising": rising_out,
    "by_narrative": by_narrative,
    "stats": {
        "hot_count": len(hot),
        "new_count": len(new_sorted),
        "rising_count": len(rising),
        "narrative_files": len(by_narrative),
    },
}
print(json.dumps(output))
