# Foundry contract

The shared names and formats every Foundry skill and agent uses. When a prompt
says "use the contract", it means this file. Use these names exactly; do not
invent variants.

## Source of truth

GitHub owns state and milestones. The repo owns content that never claims
state. No repo file records whether something is planned, in progress or
shipped, and nothing written before an event may claim it happened.

| Thing | Lives in | Template |
|---|---|---|
| Product brief | `docs/product.md` | `templates/product.md` |
| Technical foundations | `docs/architecture.md` | `templates/architecture.md` |
| Spec | `docs/specs/<date>-NN-<slug>.md` | `templates/spec.md` |
| Build log | `docs/builds/<date>-NN-<slug>.md` | `templates/build.md` |
| Milestone (goals, scope, acceptance criteria, flags, experiences served) | GitHub Milestone description | `templates/github/milestone.md` |
| Milestone status | GitHub Milestone open/closed. Closed means shipped | — |
| Tasks | GitHub issues on the milestone | `templates/github/task-issue.md` |
| Follow-ups | GitHub issues labelled `foundry:follow-up` | `templates/github/follow-up-issue.md` |
| Stage of a run | PR labels (below) | — |

- `NN` is a two-digit sequence (`01`, `02`, …). `<slug>` is lowercase words
  joined by `-`, from the milestone name. `<date>` is `YYYY-MM-DD`.
- Milestone branch: `foundry/NN-<slug>`. Abandoned: renamed to
  `foundry/NN-<slug>-abandoned-<date>`. Brief-only docs branch: `foundry/brief-<date>`.
- Read repo docs from the milestone branch while a milestone is in flight (it
  carries any brief change made for this milestone), otherwise from the default branch.

## Milestones on GitHub

- Title: `NN · <name>`. The `NN` is the roadmap order; the lowest-numbered
  open Milestone is next.
- Description: the format in `templates/github/milestone.md`, including the
  `## Serves` line naming core experiences from `docs/product.md`.
- Closed Milestones are history: never edit them.
- **In flight:** an open Milestone whose branch `foundry/NN-<slug>` exists
  (locally or on `origin`) and has no merged PR. At most one is in flight.
  An open Milestone whose PR has merged is not in flight; it is waiting to be closed.
- **Reconcile:** every Foundry entry point (wise-counsel, start-milestone,
  factory) first closes any open Milestone whose PR has merged
  (`gh pr list --head foundry/NN-<slug> --state merged`), with
  `gh api -X PATCH repos/{owner}/{repo}/milestones/<number> -f state=closed`.
  GitHub does not close a Milestone when its issues close.
- Milestones are written only after the owner approves the change in-session.

## Issues

- **Task issues:** title `NN.T · <task>` (`T` is the task's order), attached to
  the milestone, created by Hypatia after the owner approves the spec. The
  milestone's PR closes them (`Closes #<n>` in its body). Daedalus comments on
  each when its done-check passes.
- **Follow-up issues:** label `foundry:follow-up` plus exactly one category
  label: `bug`, `robustness` or `out-of-scope`. No milestone until the owner
  triages them with Anaximander. Homer opens them (on APPROVE only) without
  asking the owner: they record findings, and the owner decides at triage.
- **Triage outcomes**, recorded in the issue's `## Triage` section: attached to
  milestone `NN` (the issue becomes one of that milestone's tasks and the PR
  closes it), made a milestone of its own, or closed as won't-fix with a reason.

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
- Each finding is tagged (see **Finding tags**). Only `blocking` findings cause
  `CHANGES`. Each finding cites what it is checked against: a definition of
  done, a failure moment, the spec, `docs/architecture.md`, or the reviewer's remit.
- Homer returns `APPROVE` or `ESCALATE`.
- Daedalus returns `READY <pr-number>` or an escalation block.

## Finding tags

| Tag | Meaning | What happens |
|---|---|---|
| `blocking` | Shipping it would hurt a user or break a definition of done. A reproduced crash, data loss or security weakness on untrusted input is `blocking` unless the milestone's scope rules it out | Causes `CHANGES`; fixed before the PR passes |
| `nit` | Small, within the code this PR touches: test gaps, tidy-ups | Daedalus always fixes it in this PR |
| `follow-up` | Real, but outside this PR's scope or too big for it | Homer opens a follow-up issue |

Every entry under the build log's `## Known issues` is classified by a reviewer with one of these tags.

## Posting a review

Every agent acts through the owner's `gh` account, and GitHub does not let an
account approve or request changes on its own PR. So every review is posted
with event `COMMENT`, and the verdict lives in the body.

Post it in two steps, as the **Running commands** rule requires:

1. Write the review as a JSON file outside the repo, for example
   `<scratchpad or /tmp>/review-<pr>-r<N>-<reviewer>.json`. Use the edit
   tools, or, if you have none, one shell command of its own (a quoted heredoc,
   `<<'EOF'`, so the shell leaves the text alone). Leave out `commit_id`:
   GitHub attaches the review to the PR's current head, which is the head you
   reviewed, because nothing pushes to the PR while reviewers are running.
   `comments` may be empty; each `line` must be a line in the PR's diff, on
   the new side.

   ```json
   {
     "event": "COMMENT",
     "body": "<body, see below>",
     "comments": [
       { "path": "src/store.rs", "line": 96, "body": "[nit] <finding> — checked against: <…>" }
     ]
   }
   ```

2. Post it: `gh api repos/{owner}/{repo}/pulls/<pr>/reviews --input <file>`.

Never build the review from `-f` / `-F` fields: gh groups `-f` and `-F`
fields separately, so mixing them splits each inline comment apart (HTTP 422),
and `-F` rewrites text that starts with `@` or looks like a number or boolean.

The body follows `templates/github/review.md`. Inline comments carry the same tag and text as the body's line.

The reviewer's final reply to the orchestrator repeats the verdict on its first line.

## Architecture threshold

A choice is "real" (the owner decides) if it adds a dependency or service,
changes data storage or schemas, sets a pattern the rest of the code will
follow, or is expensive to undo. Departing from any entry in `docs/architecture.md`
or the spec's `## Architecture decisions` is always over the threshold, however
small the change. Anything smaller, the agent decides and records.

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
Agents never ask the owner directly; the orchestrator relays. On the PR, an
escalation is posted as a comment in `templates/github/escalation.md`.

## Templates

Each GitHub template answers one question. Use them for everything Foundry posts.

| Template | Question | Written by |
|---|---|---|
| `templates/github/milestone.md` | Milestone description format | Anaximander |
| `templates/github/pr.md` | What does this change, and how far along is it? | Daedalus |
| `templates/github/review.md` | Did this pass my remit, and what has to change? | each reviewer |
| `templates/github/approval.md` | Should I merge? | Homer |
| `templates/github/escalation.md` | What do you need from me? | Homer, factory |
| `templates/github/task-issue.md` | What gets built, and how do we know it's done? | Hypatia |
| `templates/github/follow-up-issue.md` | What's wrong, how much does it matter, and where? | Homer |
| `templates/github/docs-pr.md` | What changed in the product's direction, and why? | Anaximander |

## Running commands

Run each outward-facing action as its own shell command: every `gh` call that
writes (comment, review, label, PR or milestone change), every `git commit`,
and every `git push`. Never chain them with each other or with file edits
(`&&`, `;`, heredoc scripts). Make file edits with the edit tools, not inside
the same command. Each action then stands alone for the owner's permission
checks, and a refusal stops only that one step.

## Never

- The factory never merges a PR. The owner merges.
- The factory never tags or publishes a release. Releases start from a tag the owner pushes.
- Nothing is written to `main` except through a PR the owner merges.
- No stage relies on session memory: every stage reads repo files and GitHub state.
