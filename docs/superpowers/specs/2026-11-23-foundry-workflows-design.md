# Foundry: Top-Level Workflows — Design

Date: 2026-11-23 · Revision 2: 2026-11-24 (after three smoke runs on `foundry-smoke`)
Status: Revision 2 draft for owner review

## 1. Intent

Foundry is a software factory, packaged as a Claude Code plugin, that takes a
project or feature from a rough idea to a merge-ready GitHub pull request.

The owner stays in charge of **what** gets built and of **architecture**;
the factory does the building, verifying and reviewing unattended, and hands
back a PR with a clear verdict. The owner always merges.

It works in two starting states:

1. **Greenfield** — an empty (or near-empty) repo plus a brief idea for a product.
2. **Existing** — a repo with code (and possibly existing Foundry docs)
   plus an idea for a new feature.

### What revision 2 changes, and why

The smoke runs showed five gaps:

1. **Follow-ups had no path.** Fourteen open items across three milestones —
   duplicated between reviewers, rediscovered milestones later, or lost.
2. **GitHub output had no shared shape.** Every reviewer wrote differently;
   PR bodies were three links.
3. **Project-wide technical decisions had no home.** Stack, CI and testing
   were decided inside milestone 01's spec; CI was decided without the owner;
   there was no CD; CI ran on one platform for a cross-platform CLI.
4. **No user in the design.** Milestones were feature lists; acceptance
   criteria were per command, so typo and empty-input cases slipped to the
   last milestone.
5. **Repo docs lied about state.** Homer committed `shipped` before CI and
   before the merge. Keeping files as the source of truth for status needed a
   growing set of workarounds.

## 2. Goals, non-goals, anti-goals

**Goals**
- Turn an idea into a product brief and a roadmap of milestones through an
  interview with the owner.
- Fix project-wide technical foundations once, with the owner, and hold every
  milestone to them.
- Turn one milestone into a spec and task issues, with the owner deciding
  every real architecture choice.
- Build, verify and review a milestone unattended, producing one PR.
- Capture every finding: fixed in the PR, or recorded as a follow-up the owner triages.
- Make every stage resumable from repo files and GitHub state alone.

**Non-goals (for now)**
- Running more than one milestone at a time.
- Running stages in GitHub Actions (but C3 keeps it possible).
- Auto-merging or auto-releasing. The owner merges and the owner tags releases.
- Managing multiple repos from one factory.
- GitHub Projects (boards). The owner may add one by hand.

**Anti-goals** (failure even if it "works")
- An agent quietly makes an architecture choice the owner should have made.
- A record claims something that hasn't happened (e.g. "shipped" before merge).
- Milestone or spec content silently changes downstream.
- A PR reaches review without its done-checks and CI passing.
- A finding is raised and then lost: neither fixed nor recorded.
- State that exists only in a session's memory, so a crash loses the run.
- Reviewers producing duplicate or conflicting feedback because their remits overlap.

## 3. Constraints

- **C1. Claude Code plugin** named `foundry`; entry points `/foundry:<skill>`.
- **C2. GitHub,** driven with `gh`.
- **C3. All handoff state on disk or on GitHub.** No stage depends on session memory.
- **C4. Source of truth by kind** (revised):
  - **GitHub owns state and milestones:** milestone content and open/closed
    status, task issues, follow-up issues, PRs, labels, CI results.
  - **The repo owns content that never claims state:** product brief,
    architecture, specs, build logs.
  - Repo docs never record status. Nothing written before an event may claim it happened.
- **C5. One milestone in flight at a time** per repo.
- **C6. Nothing reaches `main` without the owner's merge.** Repo docs are
  committed on a branch and land through a PR: the milestone PR, or a docs PR
  for a brief-only session. GitHub objects (Milestones, issues) are written
  directly, only after the owner approves in-session.
- **C7. Each outward-facing action runs as its own command** (every `gh`
  write, commit and push), so permission checks see each one.

## 4. The cast

| Hero | File | Model | Role |
|---|---|---|---|
| Anaximander, High Sage | `skills/wise-counsel/SKILL.md` | Session (Opus) | Product designer: product brief, core experiences, roadmap, follow-up triage |
| Lady Hypatia | `skills/start-milestone/SKILL.md` | Session (Opus) | Technical designer: architecture foundations, spec, task issues |
| Daedalus, Master Craftsman | `agents/builder.md` | Opus | Builds the milestone, opens the PR, writes the build log, fixes every blocking finding and nit |
| Momus, the Faultfinder | `agents/reviewer-code.md` | Routed (Sonnet / Opus) | Correctness, simplicity, tests, definitions of done, architecture conventions |
| Atropos, the Inflexible | `agents/reviewer-security.md` | Opus | Security; only when `security` flagged |
| Clotho, the Spinner | `agents/reviewer-ux.md` | Sonnet | Behaviour, flow, core experiences; only when `ui` flagged |
| Lachesis, the Alloter | `agents/reviewer-ui.md` | Haiku | Visual conformance; only when `ui` flagged |
| Homer, Scribe of Ages | `agents/approver.md` | Opus | Final judgment, follow-up capture |

Anaximander and Hypatia are skills because subagents cannot talk to the owner
(`docs/superpowers/notes/2026-11-23-subagent-escalation.md`). The `factory`
skill is the orchestrator (section 8).

## 5. Where everything lives

| Thing | Lives in | Written by |
|---|---|---|
| Product brief: vision, goals/non-goals/anti-goals, product constraints, core experiences, decision log | `docs/product.md` | Anaximander |
| Technical foundations: stack, testing, CI, CD, conventions, decision log | `docs/architecture.md` | Hypatia (every entry decided by owner) |
| Milestone: goals, scope, acceptance criteria, flags, experiences served | GitHub Milestone `NN · <name>`, in its description | Anaximander |
| Milestone order | `NN` in the title | Anaximander |
| Milestone status | Milestone open/closed. Closed = shipped | Factory, after the owner's merge |
| Spec | `docs/specs/<date>-NN-<slug>.md` | Hypatia |
| Tasks | One issue per task, titled `NN.T · <task>`, on the milestone | Hypatia |
| Task progress | A comment per issue when its done-check passes; `Closes #…` in the PR | Daedalus |
| Build log: deviations, known issues, gate, review rounds | `docs/builds/<date>-NN-<slug>.md` | Daedalus |
| Stage of the run | PR labels | Factory (Daedalus sets only `foundry:building`) |
| Follow-ups | Issues labelled `foundry:follow-up` + `bug` / `robustness` / `out-of-scope`, no milestone until triaged | Homer |

Removed in revision 2: `docs/roadmap.md`, `docs/milestones/`, the milestone
`Status:` line, the "Reading status" rule, the roadmap `## History`, and
Homer's shipping commit.

### Milestone description format (GitHub)

```
<one-line summary>

## Goals
## Scope
### In
### Out
## Acceptance criteria
1. … (numbered AC1, AC2, …; testable statements)
## Serves
<core experience names from docs/product.md>
## Flags
security: yes|no
ui: yes|no
```

### Product brief (`docs/product.md`)

- **Vision:** what it is, who it's for, why.
- **Goals, non-goals, anti-goals.**
- **Product constraints:** platforms, distribution (how people get it),
  hosting and budget, hard limits (compliance, offline, accessibility level).
- **Core experiences:** three to five, each with:
  ```
  ### <Experience name>
  Who:             <the person and their situation>
  Trigger:         <what makes them reach for the product>
  Journey:         1. … 2. … 3. … (their steps, their words)
  Success:         <what they have at the end, and how it feels>
  Failure moments: <where it can go wrong: typos, empty input, first run,
                    lost data, returning after a month>
  Not this:        <what it deliberately isn't>
  ```
- **Decision log:** dated entry per session — what changed and why.

No milestone list and no status. It links to the GitHub Milestones.

### Architecture (`docs/architecture.md`)

- **Stack:** language, runtime, key libraries — each with rejected options and why.
- **Testing:** layers, tools, where tests live.
- **CI:** what runs on which platforms (matching the product constraints),
  pinned toolchain, caching, dependency and security audit.
- **CD:** what a release is, its trigger (a tag the owner pushes), what it
  builds, where it publishes, what secrets it needs.
- **Conventions:** structure, error handling, naming.
- **Decision log:** dated; every entry `Decided by: owner`.

## 6. The cycle

```
/foundry:wise-counsel    → Anaximander (with owner)
                             triage follow-ups → brief + milestones          [owner approves]
/foundry:start-milestone → Hypatia (with owner)
                             foundation pass if needed → architecture.md     [owner decides each]
                             spec + task issues                              [owner approves spec]
                         ── unattended from here (escalations surface to owner) ──
  Daedalus → draft PR → done-checks + CI green → PR ready
  Momus + flagged Fates, in parallel  ⇄  Daedalus fixes blocking + nits  (max 3 rounds)
  all PASS, nits open → polish pass (Daedalus, Momus re-checks; not counted)
  Homer → opens follow-up issues → APPROVE / ESCALATE
                         ── back to owner ──
  owner merges → task issues close → factory closes the Milestone on its next run
```

## 7. Roles in detail

### 7.1 Anaximander — product designer

- **Entry:** `/foundry:wise-counsel`. Required once per repo (to create
  `docs/product.md`); after that, `/foundry:start-milestone` can run without him.
- **Inputs:** the repo, `docs/product.md` if present, open GitHub Milestones,
  closed Milestones with their merged PRs and build logs, and open
  `foundry:follow-up` issues.
- **Works by:** product design interview with the owner, one question at a time.
- **Session order:**
  1. **Reconcile:** close any open Milestone whose PR has merged.
  2. **Triage follow-ups** with the owner: each open follow-up is attached to
     an upcoming milestone, made a milestone of its own, or closed as won't-fix
     with a reason recorded in its `## Triage` section.
  3. **Brief:** in a greenfield repo, interview for vision, goals, product
     constraints and core experiences **before** proposing any milestone.
     Press until there are three to five specific experiences, each with its
     failure moments. On later visits, revise them.
  4. **Roadmap:** propose feature-shaped milestones, each naming the
     experiences it serves, with testable acceptance criteria that cover the
     failure moments it touches. On an existing roadmap, show the change.
  5. Owner approves → write `docs/product.md` (with a decision-log entry) and
     create/update the GitHub Milestones.
- **Rules:** closed (shipped) Milestones are never edited. Never touch the
  in-flight milestone. Decides nothing technical.
- **Output and handoff:** if a build starts now, the brief change is left for
  Hypatia to commit on the milestone branch; otherwise a docs PR (template 7).
  Offers `/foundry:start-milestone`.

### 7.2 Hypatia — technical designer and planner

- **Entry:** after Anaximander, or `/foundry:start-milestone [NN]`. With no
  argument, the lowest-numbered open Milestone.
- **Onboarding an existing repo** (owner's decision): with no
  `docs/product.md`, `start-milestone` stops and sends the owner to
  `/foundry:wise-counsel` first. With no `docs/architecture.md`, the
  foundation pass **documents the stack, testing and CI already in the repo**
  for the owner to confirm or change, rather than re-deciding each; it asks
  fresh only about what's missing (e.g. CD). Setup tasks cover only the gaps.
- **Before starting:** reconcile (as Anaximander); single-slot check (an open
  milestone branch with an unmerged PR is in flight: offer resume or abandon);
  validate the Milestone description has every field — if not, list what's
  missing and stop; create branch `foundry/NN-<slug>`.
- **Foundation pass** (before the spec, same session), when
  `docs/architecture.md` is missing, or when the milestone needs a
  project-wide decision it doesn't cover:
  - Read `docs/product.md`'s product constraints; they set the options
    (e.g. macOS + Linux → CI matrix; Homebrew → CD publishes a tap).
  - Ask the owner every foundation decision: stack, testing, CI, CD,
    conventions. **None is `Decided by: Hypatia`, including CI.**
  - Write `docs/architecture.md`. A project's first milestone includes tasks
    to set up CI and the release pipeline as decided.
- **Spec** (`docs/specs/<date>-NN-<slug>.md`):
  1. **Technical design**, citing `architecture.md` rather than re-deciding it.
  2. **Experiences:** for each experience the milestone serves, how the
     design supports its journey.
  3. **Architecture decisions** for this milestone (threshold below).
  4. **Tasks:** an ordered list of issue links.
  5. **Definitions of done:** every acceptance criterion and every failure
     moment the milestone touches maps to a concrete check.
  6. **Design reference** (when `ui` flagged), with a `Run:` line
     (`server: <cmd> → <URL>` or `local: <commands>`), or `none`.
  7. **Flags**, **Revisions**.
- **Task issues** (template 5): one per task, on the milestone, created once the owner approves the spec.
- **Follow-ups:** offers to fold in open follow-ups that touch the same code.
- **Architecture threshold** (shared with Daedalus): adds a dependency or
  service, changes storage or schemas, sets a pattern, or is expensive to
  undo. Over it: ask the owner. Under it: decide and record.
- **Rules:** never edits the Milestone. Sends wrong or oversized milestones
  back to Anaximander. Carries flags unchanged; may add, never remove.
  Revisions after approval are edits in place with a `## Revisions` entry and
  owner re-approval. `architecture.md` changes only through a foundation pass
  the owner approves, riding the milestone PR.

### 7.3 Daedalus — builder

- **Starts** on owner approval of the spec. Runs unattended.
- **Works** through the task issues in order; tests in the same commit group
  as the task; comments on each issue when its done-check passes.
- **Output:** one PR per milestone (template 1), labelled `foundry:building`
  when opened as draft, attached to the Milestone, closing every task issue.
  Build log per task: what was done, deviations, how it was verified, and
  anything noticed but not fixed under `## Known issues`.
- **Deviations:** under the threshold — decide, log, continue. Over it, **or
  departing from any entry in `architecture.md` or the spec's architecture
  decisions** — push a draft and escalate.
- **Readiness gate:** every done-check and automatable definition of done
  passes locally and in CI before the PR leaves draft.
- **Fix mode:** fixes every `blocking` finding **and every `nit`**, as new
  commits; `## Review round N` in the build log.
- **Polish pass:** when all reviewers pass but nits are open, fixes them
  before Homer.
- **Rules:** never edits the spec, the Milestone or `architecture.md`. Only
  agent that writes code. Never merges.

### 7.4 Review stage

| Reviewer | Model | Runs when | Judges |
|---|---|---|---|
| Momus | Sonnet; Opus if large (Foundry's own docs excluded from the count), touches core code, or flagged | always | correctness, simplicity, tests, definitions of done, `architecture.md` conventions |
| Atropos | Opus | `security` | security |
| Clotho | Sonnet | `ui` | behaviour and flow: the served experiences' journeys and failure moments, states, copy, interaction accessibility |
| Lachesis | Haiku | `ui` | visual conformance against the design reference |

- **Finding tags:**

  | Tag | Meaning | What happens |
  |---|---|---|
  | `blocking` | shipping it would hurt a user or break a definition of done; a reproduced crash, data loss or security weakness on untrusted input is `blocking` unless scope rules it out | causes CHANGES |
  | `nit` | small, within the code this PR touches: test gaps, tidy-ups | Daedalus always fixes it in this PR |
  | `follow-up` | real but outside this PR's scope or too big for it | Homer opens an issue |

- Every build-log known issue is classified by a reviewer with one of these tags.
- Verdict: `CHANGES` if any `blocking`, else `PASS`.
- Reviews posted with event `COMMENT` (verdict in the body), as a JSON file
  via `gh api …/reviews --input`, in template 2.
- Reviewers never push. Each stays in remit.
- **Loop:** next round re-runs Momus plus every reviewer that said CHANGES.
  Cap: 3 rounds, then escalate to the owner. The polish pass doesn't count.

### 7.5 Homer — final judge and follow-up capture

- **Checks:** traceability (AC and failure moments → DoD → passing); the PR
  serves the milestone's goals **and the experiences it serves**; deviations
  are justified and none departs from `architecture.md` or a spec decision;
  no blocking finding dismissed; **no `nit` left open**; every known issue
  classified.
- **Follow-ups:** merges duplicate `follow-up` findings across reviewers and
  rounds, then opens one issue per item (template 6).
- **CI:** confirms CI is green on the PR head being approved.
- **Verdict:** APPROVE (template 3, linking the follow-ups) or ESCALATE
  (template 4, with `Route: Daedalus | Hypatia | Anaximander`).
- **Never** merges, edits code, docs or the Milestone, or commits.

## 8. The orchestrator (`factory` skill)

- **Runs locally** in the owner's session; each agent a subagent. All state per C3.
- **Preflight:** `gh auth status`, a GitHub remote, on the milestone branch,
  spec approved. Creates missing labels.
- **Stages and labels:** `foundry:building` → `foundry:review-r1..r3` →
  (polish pass) → `foundry:awaiting-homer` → `foundry:ready-to-merge` or
  `foundry:escalated`.
- **Reviewer dispatch:** in parallel; routes Momus's model; starts a
  `server:` app once for Clotho and Lachesis, who run `local:` apps
  themselves in a sandbox.
- **Escalation:** agents return the escalation block; the factory posts it on
  the PR (template 4) with `foundry:escalated`, sends a push notification,
  asks the owner in-session, then resumes the same agent with `SendMessage`
  (or a fresh one with the build log if the session restarted).
- **Resume:** reads the PR label, build log and reviews; continues at that stage.
- **Reconcile on every run:** closes Milestones whose PR has merged.
- **Holds no judgment of its own.** Never merges, never tags.

## 9. GitHub templates

In `skills/factory/templates/github/`. Each answers one question:

| # | Template | Question | Written by |
|---|---|---|---|
| 1 | Pull request | What does this change, and how far along is it? | Daedalus |
| 2 | Review | Did this pass my remit, and what must change? | each reviewer |
| 3 | Approval | Should I merge? | Homer |
| 4 | Escalation comment | What do you need from me? | Homer, factory |
| 5 | Task issue | What gets built, and how do we know it's done? | Hypatia |
| 6 | Follow-up issue | What's wrong, how much does it matter, and where? | Homer |
| 7 | Docs PR | What changed in the product's direction, and why? | Anaximander |

Formats as agreed in conversation (revision 2), summarised:

1. **PR** — title `NN · <milestone>`; 2–4 line summary; links to Milestone,
   spec, build log; flags; `## Tasks` as `Closes #n — NN.T <task>`.
2. **Review** — `<VERDICT> — <reviewer>, round N`; `## Blocking`,
   `## Nits (fix in this PR)`, `## Follow-ups (not this PR)`, each finding
   `<finding> — <file:line> — checked against: <…>`; `## What I checked`.
   Empty sections say `none`.
3. **Approval** — `APPROVE — Homer`; one-sentence reason; `## What was built`;
   `## Acceptance criteria` table (AC | check | result); `## Deviations`;
   `## Follow-ups opened` (issue links); `## CI` (green on <sha>).
4. **Escalation** — `ESCALATED — <agent>, at <stage>`; `## The problem`;
   `## Your decision` (question, options with trade-offs); recommendation;
   `Route:` (Homer); `Resume with: /foundry:start-milestone`.
5. **Task issue** — title `NN.T · <task>`; Milestone, spec link, `Covers:`
   ACs, `Depends on:`; `## Build`; `## Done-check`.
6. **Follow-up issue** — plain title; labels `foundry:follow-up` + category;
   `## What's wrong`, `## Impact`, `## Where`, `## Found` (milestone, PR,
   raised by), `## Triage`.
7. **Docs PR** — title `Product brief · <date> · <short>`; summary;
   `## Brief changes`; `## Roadmap changes (already applied on GitHub)`;
   decision-log link.

## 10. Approaches considered

| Decision | Options | Chosen | Why |
|---|---|---|---|
| Where roadmap/milestones live (rev 1) | files · GitHub · files mirrored | ~~files mirrored, file wins~~ | **Superseded in rev 2** |
| Source of truth (rev 2) | A. GitHub state, files content · B. GitHub owns milestones too · C. everything on GitHub | **B + task issues** | Repo docs claimed state before it happened; GitHub records events as they happen. Specs and logs stay versioned with code |
| Milestone order | numbered titles · GitHub Project | **Numbered titles** | Plain `gh`, matches branch names; Projects need extra scope and GraphQL |
| Product vision home | pinned issue · `docs/product.md` | **`docs/product.md`** | Content never claims state, so it can't lie; reviewed in PRs |
| Hypatia on architecture choices | decide & record · ask owner | **Ask owner** | Owner owns architecture |
| Project-wide technical decisions | Anaximander · Hypatia · split | **Split** | Anaximander asks product constraints (what); Hypatia turns them into foundations (how), owner decides each |
| Milestone shape | feature-shaped · experience-shaped | **Feature-shaped** | Experiences are design input to Hypatia, cited by milestones |
| PR granularity | per milestone · per task · task PRs into milestone branch | **One per milestone** | Problems were in follow-up, not review size |
| Nits | owner decides · fixed by default | **Fixed by default** | Tidy-ups and test gaps were left behind |
| Daedalus on spec failure | stop · decide · threshold | **Threshold**, plus any departure from a recorded decision escalates | Keeps owner on architecture |
| UX vs UI | — | behaviour/flow vs visual conformance | No overlap |
| Momus model | — | routed Sonnet/Opus, never Haiku | Missed bugs cost more than tokens |
| Review loop | re-run all · re-run Momus + CHANGES | **Momus + CHANGES**, 3-round cap | Cheaper, correctness always rechecked |
| What APPROVE does | Homer merges · owner merges · routine only | **Owner merges** | Trust built from verdicts |
| Where the run happens | local · Actions · local, Actions-ready | **Local, Actions-ready** | Debuggable now, resumable |
| Concurrency | — | reviewers parallel; one milestone at a time | Milestones build on each other |

## 11. Designer's calls (owner to check)

From revision 1, still standing:
- Spec approval is recorded in the spec (`Approved: <date>`).
- Escalation back to Hypatia keeps the same branch and PR.
- With no CI, the gate is local checks only until CI exists (now: the first
  milestone always sets CI up, per the foundation pass).
- Reviews are posted as `COMMENT` reviews because GitHub won't let an account
  approve or request changes on its own PR.

New in revision 2:
- **Milestones close on the factory's next run after merge** (GitHub doesn't
  close a Milestone when its issues close). `wise-counsel`, `start-milestone`
  and the factory all reconcile.
- **"In flight" is read from GitHub:** an open Milestone with a
  `foundry/NN-<slug>` branch that has an open (unmerged) PR or no PR yet.
- **Abandon** closes the PR unmerged, leaves the branch, and closes the task
  issues as not planned; the Milestone stays open.
- **Task issues are created after the owner approves the spec,** so a rejected
  draft leaves nothing on GitHub.
- **Follow-up category labels** (`bug`, `robustness`, `out-of-scope`) are
  created by the factory's preflight along with the stage labels.
- **The polish pass is skipped** when no nits are open.
- **The spec's flags still come from the Milestone;** Hypatia records any
  added flag in both the spec and the Milestone description (an addition,
  not an edit of its goals or scope).
- **Revising an in-flight milestone.** Anaximander never touches the in-flight
  milestone *except* when an escalation routes there (`Route: Anaximander`, or
  Hypatia sending it back). He then revises it with the owner, who approves;
  Hypatia revises the spec and task issues to match, and the run continues
  on the same branch. The owner can choose abandon instead.
- **Attaching a follow-up to a milestone** sets the issue's milestone, and
  Anaximander adds an acceptance criterion if it changes behaviour. Hypatia
  treats each attached follow-up as a task: the follow-up issue itself is
  the task issue (she adds `## Build` and `## Done-check` as a comment), and
  the PR closes it. Reconcile closes a Milestone on PR merge regardless.
- **Homer opens follow-up issues without owner approval.** They record
  findings, not decisions; the owner decides at triage. C6's "only after the
  owner approves" applies to Milestones and the brief. Homer opens them only
  on APPROVE, and first searches for existing issues from the same PR (the
  `## Found` line) so a resumed run never duplicates them. On ESCALATE the
  findings stay in the reviews.
- **Brief changes that don't land.** When a session continues into a build,
  the `product.md` change is the first commit on the milestone branch, so
  Hypatia and the reviewers read the brief from that branch. If the milestone
  is abandoned, Hypatia opens a docs PR from that commit. If a docs PR is
  still open when `start-milestone` runs, Hypatia asks the owner to merge it
  first.
- **Restarting an abandoned milestone.** Abandon renames the branch to
  `foundry/NN-<slug>-abandoned-<date>`, so a restart is fresh: new branch,
  new spec, new task issues. The abandoned spec can be read for reference.
- **Ending the polish pass.** Momus re-checks only the polish commits. A
  `blocking` finding there counts as the next review round (or escalates
  after round 3). A new `nit` gets one more polish pass; anything still open
  after it becomes a `follow-up`. Daedalus records each nit with its fix
  commit in the build log's review-round section, which is how Homer checks
  "no nit left open"; nits from reviewers who passed are covered the same way.

## 12. Left to the builder

- Exact Markdown of the templates within section 9's shapes.
- Exact thresholds for routing Momus to Opus.
- Slug rules; how `NN` is derived from the Milestone title.
- How the core-experience and architecture sections are formatted inside
  their files, within section 5.
- Migration: a repo with revision-1 docs (`docs/roadmap.md`,
  `docs/milestones/`) — Anaximander offers to migrate them to GitHub
  Milestones and `docs/product.md` on first run.
