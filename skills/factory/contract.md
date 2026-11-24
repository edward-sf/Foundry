# Foundry contract

The shared names and formats every Foundry skill and agent uses. When a prompt
says "use the contract", it means this file. Use these names exactly; do not
invent variants.

## Files in the target repo

Files are the source of truth. Where a file and a GitHub object disagree, the file wins.

| File | Path | Template |
|---|---|---|
| Roadmap | `docs/roadmap.md` | `templates/roadmap.md` |
| Milestone | `docs/milestones/NN-<slug>.md` | `templates/milestone.md` |
| Spec | `docs/specs/<date>-<milestone-slug>.md` | `templates/spec.md` |
| Build log | `docs/builds/<date>-<milestone-slug>.md` | `templates/build.md` |

- `NN` is a two-digit sequence (`01`, `02`, …) in creation order. `<slug>` is
  lowercase words joined by `-`. `<date>` is `YYYY-MM-DD`. `<milestone-slug>` is
  `NN-<slug>` of the milestone.
- Milestone branch: `foundry/NN-<slug>`. Roadmap-only docs branch: `foundry/roadmap-<date>`.

## Milestone status

`Status:` in a milestone file is exactly one of:

- `planned`: on the roadmap, not started.
- `in-progress`: Hypatia has started it. At most one milestone is `in-progress` at a time.
- `shipped`: merged. Shipped milestones are history and are never edited.

### Reading status

Status changes are committed on the milestone branch and reach the default
branch only when the owner merges. So the working tree can be ahead of what has
really happened (Homer writes `shipped` before the merge). Never read status
from the working tree. Run `git fetch` first, then a milestone's status is:

- `shipped` if its file on the default branch
  (`git show origin/<default>:docs/milestones/NN-<slug>.md`) says `shipped`;
- `in-progress` if not, and its branch `foundry/NN-<slug>` exists locally or
  on `origin`, its file on that branch says `in-progress` or `shipped`, and the
  branch has no merged PR (`gh pr list --head foundry/NN-<slug> --state merged`
  is empty);
- `planned` otherwise. An abandoned milestone's branch says `planned`, so it
  is `planned`.

Read the roadmap and milestone list from the default branch the same way.

The GitHub Milestone mirror holds only the title, a link to the file, and
open/closed state (open unless `shipped`). It never holds a copy of the content.

## Flags

`security: yes|no` and `ui: yes|no`. Flags decide which reviewers run.
A flag may be added downstream when a risk is found; it is never removed.

## PR labels (stage tracking)

| Label | Meaning |
|---|---|
| `foundry:building` | Daedalus is building; PR is draft |
| `foundry:review-r1` | Review round 1 in progress |
| `foundry:review-r2` | Review round 2 in progress |
| `foundry:review-r3` | Review round 3 in progress (the last) |
| `foundry:awaiting-homer` | All reviewers passed; Homer is judging |
| `foundry:escalated` | Waiting on the owner; the PR comment says what's needed |
| `foundry:ready-to-merge` | Homer approved; the owner merges |

A PR carries exactly one `foundry:` stage label; `foundry:escalated` replaces
the stage label while waiting, and the escalation comment names the stage to return to.

## Verdicts

- Reviewers end with exactly one of `PASS` or `CHANGES` on their first line.
- Each finding is tagged `blocking` or `nit`. Only `blocking` findings cause `CHANGES`.
  Each finding cites what it is checked against: a definition of done, the spec, or the reviewer's remit.
- Homer returns `APPROVE` or `ESCALATE`.
- Daedalus returns `READY <pr-number>` or an escalation block.

## Posting a review

Every agent acts through the owner's `gh` account, and GitHub does not let an
account approve or request changes on its own PR. So every review is posted
with event `COMMENT`, and the verdict lives in the body:

```
gh api repos/{owner}/{repo}/pulls/<pr>/reviews \
  -f event=COMMENT -f body="<body>" \
  -F 'comments[][path]=<file>' -F 'comments[][line]=<n>' -F 'comments[][body]=<finding>'
```

Body format:

```
<PASS|CHANGES> — <Reviewer name>, round <N>

- [blocking|nit] <finding> (checked against: <DoD ACn | spec section | remit>)
```

The reviewer's final reply to the orchestrator repeats the verdict on its first line.

## Architecture threshold

A choice is "real" (the owner decides) if it adds a dependency or service,
changes data storage or schemas, sets a pattern the rest of the code will
follow, or is expensive to undo. Anything smaller, the agent decides and records.

## Escalation block

Any agent that needs the owner ends its reply with this block and stops:

```
ESCALATE
Stage: <current label>
Question: <one question, in the owner's terms>
Options:
- A. <option> — <trade-off>
- B. <option> — <trade-off>
Recommendation: <A|B|…> — <why>
```

Homer's escalation adds a `Route: Daedalus|Hypatia|Anaximander` line.
Agents never ask the owner directly; the orchestrator relays.

## Running commands

Run each outward-facing action as its own shell command: every `gh` call that
writes (comment, review, label, PR or milestone change), every `git commit`,
and every `git push`. Never chain them with each other or with file edits
(`&&`, `;`, heredoc scripts). Make file edits with the edit tools, not inside
the same command. Each action then stands alone for the owner's permission
checks, and a refusal stops only that one step.

## Never

- The factory never merges a PR. The owner merges.
- Nothing is written to `main` except through a PR the owner merges.
- No stage relies on session memory: every stage reads files and PR state.
