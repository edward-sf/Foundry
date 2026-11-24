# Foundry: Top-Level Workflows — Design

Date: 2026-11-23
Status: Draft for owner review

## 1. Intent

Foundry is a software factory, packaged as a Claude Code plugin, that takes a
project or feature from a rough idea to a merge-ready GitHub pull request.

The owner stays in charge of **what** gets built and of **architecture**;
the factory does the building, verifying and reviewing unattended, and hands
back a PR with a clear verdict. The owner always merges.

It works in two starting states:

1. **Greenfield** — an empty (or near-empty) repo plus a brief idea for a product.
2. **Existing** — a repo with code (and possibly an existing Foundry roadmap)
   plus an idea for a new feature.

## 2. Goals, non-goals, anti-goals

**Goals**
- Turn an idea into a roadmap of milestones through an interview with the owner.
- Turn one milestone into a technical spec and task plan, with the owner
  deciding every real architecture choice.
- Build, verify and review a milestone unattended, producing one PR.
- Make every stage resumable from files and GitHub state alone.
- Leave a durable record (roadmap history, specs, build logs, reviews) that
  later sessions build on.

**Non-goals (for now)**
- Running more than one milestone at a time.
- Running stages in GitHub Actions (but see constraint C3: the design must not
  prevent it).
- Auto-merging. The owner merges every PR.
- Managing multiple repos from one factory.

**Anti-goals** (failure even if it "works")
- An agent quietly makes an architecture choice the owner should have made.
- Milestone or spec content silently changes downstream (scope drift without
  the owner seeing it).
- A PR reaches review without its done-checks and CI passing.
- State that exists only in a session's memory, so a crash loses the run.
- Reviewers producing duplicate or conflicting feedback because their remits overlap.

## 3. Constraints

- **C1. Claude Code plugin.** Foundry ships as a plugin named `foundry`,
  installed into target repos. Commands are namespaced `/foundry:<command>`.
- **C2. GitHub.** PRs, reviews, labels and Milestones live on GitHub and are
  driven with `gh`.
- **C3. All handoff state on disk or on GitHub.** No stage may depend on
  session memory to know what the previous stage did. Every stage reads only
  repo files and PR/GitHub state. This is what makes resume possible and keeps
  a later move to GitHub Actions open.
- **C4. Files are the source of truth.** Where a file and a GitHub object
  describe the same thing, the file wins.
- **C5. One milestone in flight at a time** per repo.
- **C6. Nothing reaches `main` without the owner's merge — design docs
  included.** The spec, milestone status changes and `build.md` are committed
  to the milestone branch and land with the build PR. A `wise-counsel` session
  that changes the roadmap without starting a build opens a small docs PR for
  the owner to merge.

## 4. The cast

| Hero | Agent file | Model | Role |
|---|---|---|---|
| Anaximander, High Sage | `skills/wise-counsel/SKILL.md` | Session (Opus) | Product designer: interviews owner, owns the roadmap |
| Lady Hypatia | `skills/start-milestone/SKILL.md` | Session (Opus) | Technical designer: spec, architecture decisions, task plan |
| Daedalus, Master Craftsman | `builder.md` | Opus | Builds the milestone, opens the PR, writes `build.md` |
| Momus, the Faultfinder | `reviewer-code.md` | Routed (Sonnet / Opus) | Correctness, simplicity, tests, definitions-of-done coverage |
| Atropos, the Inflexible | `reviewer-security.md` | Opus | Security review; only when `security` flagged |
| Clotho, the Spinner | `reviewer-ux.md` | Sonnet | Behaviour and flow; only when `ui` flagged |
| Lachesis, the Alloter | `reviewer-ui.md` | Haiku | Visual conformance; only when `ui` flagged |
| Homer, Scribe of Ages | `approver.md` | Opus | Final judgment (APPROVE/ESCALATE) and record-keeping |

The `factory` skill is the orchestrator (section 6).

## 5. The cycle

```
/foundry:wise-counsel    → Anaximander (with owner) → roadmap + milestone files   [owner approves roadmap]
/foundry:start-milestone → Hypatia (with owner)     → spec                        [owner approves spec]
                         ── unattended from here (escalations surface to owner) ──
  Daedalus → draft PR → all done-checks + CI green → PR ready
  Momus + flagged Fates, in parallel  ⇄  Daedalus fixes   (max 3 rounds)
  Homer → APPROVE / ESCALATE report on the PR
                         ── back to owner ──
  owner merges → Homer marks milestone shipped, updates roadmap history
```

### Artifacts

| Artifact | Path | Written by |
|---|---|---|
| Roadmap | `docs/roadmap.md` | Anaximander (history lines appended by Homer) |
| Milestone | `docs/milestones/NN-<slug>.md` | Anaximander, or owner by hand |
| Spec | `docs/specs/<date>-<milestone-slug>.md` | Hypatia |
| Build log | `docs/builds/<date>-<milestone-slug>.md` | Daedalus |
| GitHub Milestone | GitHub | Anaximander (created), Homer (closed) |
| PR + reviews + labels | GitHub | Daedalus, reviewers, Homer, orchestrator |

### Milestone file format

```
Milestone: <name>
Status: planned | in-progress | shipped
Goals                what this milestone achieves, and why
Scope                in / out
Acceptance criteria  checkable statements of done
Flags                security: yes|no, ui: yes|no
```

Acceptance criteria must be written to be testable
("a logged-out user visiting /settings is redirected to /login"), not aspirational.

The GitHub Milestone mirror holds only the title, a link to the file, and
open/closed state matching `Status`. Never a copy of the content.

## 6. Roles in detail

### 6.1 Anaximander — product designer

- **Entry:** `/foundry:wise-counsel`. Optional; `/foundry:start-milestone`
  bypasses him.
- **Inputs:** greenfield repo + idea, or existing repo + feature idea. In an
  existing repo he reads the code and current roadmap first.
- **Works by:** product design interview with the owner.
- **Returning sessions:** picks up and revises the existing roadmap. Before
  revising he reads what was actually built: shipped milestones, their merged
  PRs, and their `build.md` files.
- **Rules:**
  - Shipped milestones are history: never edited. Pending milestones may be
    reordered, re-scoped, split or dropped.
  - Proposes roadmap changes; owner approves before files are written.
  - Writes milestone files and creates/updates the GitHub Milestone mirrors.
- **Handoff:** the next milestone to Hypatia.

### 6.2 Hypatia — technical designer and planner

- **Entry:** after Anaximander, or `/foundry:start-milestone [milestone file]`.
  With no argument, picks the next `planned` milestone in roadmap order.
- **Inputs:** one milestone file + the codebase.
- **Output:** spec with
  1. **Technical design** — components, data, interfaces.
  2. **Architecture decisions** — each choice, options rejected, why, and who decided.
  3. **Task-by-task implementation plan** — ordered tasks, each with its own
     small done-check.
  4. **Definitions of done** — each acceptance criterion refined into one or
     more concrete checks (a named test, a command, an observable behaviour),
     traceable back to that criterion.
  5. **Design reference** (when `ui` flagged) — the design system / tokens /
     existing screens Lachesis checks against, or an explicit "none".
- **Architecture threshold** (shared with Daedalus): a choice is "real" if it
  adds a dependency or service, changes data storage or schemas, sets a
  pattern the rest of the code will follow, or is expensive to undo.
  - Real choices: she **asks the owner**, one at a time, with 2–3 options,
    trade-offs and her recommendation. The answer and reasoning go in the spec.
  - Smaller calls: she decides and records them.
- **Rules:**
  - Sets the milestone status to `in-progress`; does not edit milestone content.
  - If the milestone is wrong or too big, she stops and sends it back to
    Anaximander rather than re-scoping it herself.
  - Carries `security`/`ui` flags into the spec unchanged; may **add** a flag
    if the design reveals a risk, never remove one.
- **Handoff:** owner approves the spec → orchestrator starts Daedalus.

### 6.3 Daedalus — builder

- **Starts:** on owner approval of the spec. Runs unattended.
- **Works:** through the task plan in order. Tests are written in the same
  commit group as the task they verify.
- **Output:**
  - Branch named after the milestone; **one PR per milestone**, attached to
    the GitHub Milestone; commits grouped by task.
  - `build.md`: per task — what was done, deviations and why, how its
    done-check was verified. Plus a "Review round N" section per review round.
- **Deviations** (same threshold as Hypatia):
  - Architecture-level: push what he has as a draft PR, stop, and escalate —
    the owner decides, or it goes back to Hypatia for a spec revision.
  - Smaller: decide, log in `build.md`, continue.
- **Readiness gate:** the PR leaves draft only when every task done-check and
  every automatable definition of done passes, locally and in CI.
- **Rules:** never edits the spec or milestone. Is the only agent that writes
  code, including review fixes (as new commits on the same PR).

### 6.4 Review stage

- **Starts:** when the PR leaves draft. Flagged reviewers run **in parallel**.

| Reviewer | Model | Runs when | Judges |
|---|---|---|---|
| Momus | Sonnet default; Opus if large, touches core/shared code, or flagged | always | correctness, simplicity, tests, coverage of definitions of done |
| Atropos | Opus | `security` | security |
| Clotho | Sonnet | `ui` | behaviour & flow (see below) |
| Lachesis | Haiku | `ui` | visual conformance (see below) |

- **Clotho (UX) — "could someone actually get this done?"** Each milestone
  task completable from the user's view; all states handled (empty, loading,
  error, success, permission denied); copy; interaction accessibility
  (keyboard, focus order, screen-reader labels, semantics).
- **Lachesis (UI) — "does this look like it belongs?"** Spacing, typography,
  colour and components match the spec's design reference; no hardcoded values
  where tokens exist; layout at standard breakpoints; visual accessibility
  (contrast, touch-target size); consistency with existing screens. With no
  design reference: internal consistency and contrast only.
- Accessibility split: interaction → Clotho; measurable-on-screen → Lachesis.
- Clotho and Lachesis need the running app; the orchestrator starts one shared
  instance for them.
- **Reporting:** each reviewer posts a GitHub PR review with inline comments,
  ending in **PASS** or **CHANGES**. Findings are tagged *blocking* or *nit*;
  only blocking findings cause CHANGES. Each finding cites what it is checked
  against (a definition of done, the spec, or the reviewer's remit).
- **Only Momus checks definitions-of-done coverage**; the others stay in remit.
- Reviewers never push commits.
- **Loop:** Daedalus fixes, logs the round in `build.md`. Next round re-runs
  Momus plus every reviewer that said CHANGES. **Cap: 3 rounds.** Blocking
  findings left after round 3 → escalate to the owner (not Homer).
- **Exit:** all reviewers PASS → Homer.

### 6.5 Homer — final judge and record-keeper

- **Inputs:** PR, milestone file, spec, `build.md`, all reviews and rounds.
- **Checks:**
  1. Traceability: every acceptance criterion → definition(s) of done → shown passing.
  2. The PR serves the milestone's goals, not just its checklist.
  3. Every `build.md` deviation is justified and under the architecture
     threshold (none is an architecture choice in disguise).
  4. No blocking finding was dismissed without a fix or a reason.
- **Verdict** (PR comment report):
  - **APPROVE** — what was built, deviations, open nits; written so the owner
    can merge from it alone. APPROVE is a recommendation: **the owner always merges.**
  - **ESCALATE** — names the gap and who should fix it: Daedalus (build),
    Hypatia (spec wrong), or Anaximander (milestone wrong).
- **After the owner merges:** sets milestone `Status: shipped`, closes the
  GitHub Milestone, appends a history line to `docs/roadmap.md`.

## 7. The orchestrator (`factory` skill)

- **Commands:** `/foundry:wise-counsel`, `/foundry:start-milestone [milestone file]`.
- **Runs locally** in the owner's Claude Code session; each agent is a subagent.
  All state per C3.
- **Concurrency:** only the reviewers run in parallel. One milestone in flight:
  `start-milestone` refuses to start a new one while another is `in-progress`,
  unless the owner explicitly resumes or abandons it.
- **Stage tracking:** PR labels — `foundry:building`, `foundry:review-r1..r3`,
  `foundry:awaiting-homer`, `foundry:escalated`, `foundry:ready-to-merge`.
  The milestone file's `Status` covers the coarse state.
- **Resume:** `/foundry:start-milestone` on an in-progress milestone reads the
  label, `build.md` and PR reviews, and continues from that stage.
- **Escalation:** subagents cannot ask the owner directly. An agent that needs
  the owner stops and returns ESCALATE with the question, options and its
  recommendation. The orchestrator asks the owner in-session, then resumes the
  **same** subagent (context kept) with the answer; the decision is recorded
  (`build.md` or the spec). Every escalation is also recorded on the PR as a
  comment + `foundry:escalated` label, so a closed session can resume from it.
  When waiting on the owner, the orchestrator may send a push notification.
- **Stops that come back to the owner:** Daedalus architecture-level deviation;
  round 3 still blocked (owner chooses: another round, back to Hypatia /
  Anaximander, or take over); Homer ESCALATE (owner picks who fixes);
  Homer APPROVE (ready to merge).
- **Holds no judgment of its own:** sequences stages, routes Momus's model,
  reads flags to pick reviewers, starts the app for Clotho/Lachesis. Every
  decision belongs to an agent or the owner.

## 8. Approaches considered

| Decision | Options | Chosen | Why |
|---|---|---|---|
| Where roadmap/milestones live | A. repo files · B. GitHub Milestones only · C. files mirrored to GitHub | **C**, file wins | Agents work best from files; owner keeps GitHub's progress view |
| Hypatia on architecture choices | decide & record · ask owner | **Ask owner** | Owner owns architecture |
| PR granularity | A. one per milestone · B. one per task | **A** | Review judges the milestone as a whole; per-task done-checks give checkpoints; oversized PRs are fixed by smaller milestones |
| Daedalus on spec failure | A. always stop · B. always decide · C. Hypatia's threshold | **C** | Keeps owner on architecture without babysitting details |
| UX vs UI split | — | Behaviour/flow vs visual conformance | No overlapping feedback; matches model assignment |
| Momus model | — | Routed Sonnet/Opus, never Haiku | Missed correctness bugs cost more than tokens |
| Review loop | A. re-run all · B. re-run Momus + CHANGES reviewers | **B**, 3-round cap → owner | Correctness always rechecked; cheaper and less noisy |
| What APPROVE does | A. Homer merges · B. owner always merges · C. merge routine only | **B** | New factory; owner builds trust from Homer's verdicts. C is a later one-line change |
| Where the unattended run happens | A. local · B. GitHub Actions · C. local, Actions-ready | **C** | Watchable for debugging now; state-on-disk rule keeps Actions open and enables resume |
| Concurrency | — | Reviewers in parallel; one milestone at a time | Milestones build on each other; avoids conflicts |

## 9. Designer's calls (owner to check)

These were settled during write-up, not in conversation:

- **Spec approval is recorded in the spec** (`Approved: <date>` line, set by
  Hypatia when the owner approves in-session), so resume can tell an approved
  spec from a draft (C3).
- **Shipping is part of the PR.** On APPROVE, Homer commits `Status: shipped`
  and the roadmap history line onto the milestone branch, so the owner's merge
  *is* the ship and nothing is written to `main` outside a PR. Closing the
  GitHub Milestone happens when the orchestrator next sees the PR merged.
- **Hand-written milestones get a mirror.** If `start-milestone` receives a
  milestone with no GitHub Milestone, the orchestrator creates one.
- **Escalation back upstream keeps the PR.** If Daedalus or Homer sends work
  back to Hypatia, she revises the spec in place with a revision note, the
  owner re-approves, and Daedalus continues on the same branch and PR. Back to
  Anaximander means the milestone is revised and the owner decides whether the
  PR continues or is closed.
- **No CI yet (greenfield).** If the repo has no CI, Hypatia's spec includes
  a task to add it; until it exists, the readiness gate is local checks only.

- **Anaximander and Hypatia are skills, not subagents,** because subagents
  cannot talk to the owner (confirmed in
  `docs/superpowers/notes/2026-11-23-subagent-escalation.md`). The other six
  heroes are subagents in `agents/`, dispatched as `foundry:<name>`.
- **Reviews are posted as `COMMENT` reviews with the verdict in the body,**
  because GitHub won't let an account approve or request changes on its own
  PR and every agent uses the owner's `gh` account.

## 10. Left to the builder

- Plugin file layout (commands, skill, agents) — follow Claude Code plugin conventions.
- Exact Markdown templates for roadmap, milestone, spec and `build.md`, within
  the fields above.
- Exact thresholds for routing Momus to Opus ("large", "core/shared code").
- How the app is started for Clotho/Lachesis (e.g. Playwright); the spec's
  technical design for a `ui` milestone should say how to run the app.
- Milestone numbering scheme and slug rules.
- Branch naming format.
- **Early verification task:** confirm a subagent can return an escalation and
  be resumed with context intact (via SendMessage) before any agent depends on it.
