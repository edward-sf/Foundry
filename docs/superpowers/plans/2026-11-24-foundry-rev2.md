# Foundry Revision 2 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Bring the `foundry` plugin in line with design revision 2: GitHub as source of truth for state and milestones, `docs/product.md` and `docs/architecture.md`, task and follow-up issues, the `follow-up` tag and polish pass, and seven GitHub templates.

**Architecture:** Same plugin shape as M0 (Markdown skills and agents, shared `contract.md`, structural `unittest` tests). Revision 2 replaces repo-file milestones with GitHub Milestones and issues, adds two repo docs and seven GitHub templates, and removes every rule that existed only to keep files and GitHub in step.

**Tech Stack:** Claude Code plugin format, `gh` CLI, Python 3.9 stdlib `unittest`, `claude plugin validate`.

**Spec:** `docs/superpowers/specs/2026-11-23-foundry-workflows-design.md` (revision 2)

**Base:** branch `smoke-test-fixes` (PR #1), which already carries the three smoke-run fix commits. Keep every PR #1 fix that revision 2 doesn't remove: `## Known issues`, JSON review posting via `--input` with no `commit_id`, the Running commands rule, the `Run:` line, Homer waiting for CI, decision-departure escalation, Momus routing excluding Foundry docs, Daedalus labelling the draft PR.

## Global Constraints

- Milestone title: `NN · <name>`. Task issue title: `NN.T · <task>`. Branch: `foundry/NN-<slug>`; abandoned: `foundry/NN-<slug>-abandoned-<date>`.
- Milestone status is GitHub open/closed only. No repo file records status. The words `Status:`, `shipped` (as a status value), `Reading status`, `docs/roadmap.md`, `docs/milestones/`, `## History` must not appear in any skill, agent or template.
- Repo docs: `docs/product.md`, `docs/architecture.md`, `docs/specs/<date>-NN-<slug>.md`, `docs/builds/<date>-NN-<slug>.md`.
- Finding tags, exactly: `blocking`, `nit`, `follow-up`. Verdicts `PASS` / `CHANGES`; Homer `APPROVE` / `ESCALATE`.
- Labels: the seven `foundry:` stage labels (unchanged) plus `foundry:follow-up`, `bug`, `robustness`, `out-of-scope`.
- Every `architecture.md` decision-log entry is `Decided by: owner`.
- The factory never merges and never tags a release.
- C6: repo docs reach `main` only through a PR; GitHub Milestones are written only after owner approval in-session; Homer's follow-up issues are the stated exception.
- C7: each `gh` write, commit and push is its own command.

## Review Focus

1. **A repo with revision-1 docs** (`docs/roadmap.md`, `docs/milestones/`): Anaximander offers to migrate to GitHub Milestones + `docs/product.md` and does not silently ignore or delete them. (Task 4)
2. **Existing repo, no `product.md`:** `start-milestone` stops and sends to `/foundry:wise-counsel`. **No `architecture.md` but existing CI:** Hypatia documents what exists for confirmation and adds setup tasks only for gaps. (Task 5)
3. **Resumed Homer run:** follow-ups are not duplicated (search by `## Found` PR first). (Task 8)
4. **Merged PR, Milestone still open:** every entry point reconciles and closes it; an open Milestone with a merged PR never counts as in flight. (Tasks 4, 5, 9)
5. **Polish pass that surfaces a blocking finding after round 3:** escalates, never loops. (Task 9)

---

## File Structure

```
skills/factory/contract.md                 rewritten sections (Task 1)
skills/factory/templates/
  product.md  architecture.md              new (Task 2)
  spec.md  build.md                        modified (Task 2)
  roadmap.md  milestone.md                 deleted (Task 2)
  github/                                  new (Task 3)
    milestone.md  pr.md  review.md  approval.md  escalation.md
    task-issue.md  follow-up-issue.md  docs-pr.md
skills/wise-counsel/SKILL.md               rewritten (Task 4)
skills/start-milestone/SKILL.md            rewritten (Task 5)
agents/builder.md                          modified (Task 6)
agents/reviewer-*.md                       modified (Task 7)
agents/approver.md                         modified (Task 8)
skills/factory/SKILL.md                    modified (Task 9)
README.md                                  modified (Task 10)
tests/contract.py  tests/test_*.py         modified per task
```

`github/milestone.md` is the GitHub Milestone description format (design §5); it's an eighth file alongside the seven templates because Anaximander writes it.

Tests stay structural: required tokens and headings present, and — new in this revision — **removed concepts absent** (`assertLacks`). Add a shared helper `assert_no_rev1(text)` in `tests/contract.py` that checks the removed words in Global Constraints, and call it from every skill, agent and template test.

Run all tests: `python3 -m unittest discover -s tests -v`

---

### Task 1: Contract

**Files:** Modify `skills/factory/contract.md`, `tests/contract.py`, `tests/test_contract.py`

**Interfaces:**
- Produces in `tests/contract.py`: `FINDING_TAGS = ["blocking", "nit", "follow-up"]`; `FOLLOWUP_LABELS = ["foundry:follow-up", "bug", "robustness", "out-of-scope"]`; `TARGET_PATHS` = the four repo docs above; `REV1_TERMS = ["Status:", "Reading status", "docs/roadmap.md", "docs/milestones/", "## History"]`; `assert_no_rev1(testcase, text)`. Remove `STATUSES`.
- Produces in `contract.md`: sections `## Source of truth` (design §5 table), `## Milestones on GitHub` (title format, description format pointer to `templates/github/milestone.md`, open/closed = status, reconcile rule, "in flight" rule from design §11), `## Issues` (task and follow-up issue conventions, labels), `## Finding tags` (the three-row table from design §7.4), `## Templates` (the table from design §9). Keep: Flags, PR labels, Verdicts, Posting a review, Architecture threshold (plus "or departs from `architecture.md` or a spec decision"), Escalation block, Running commands, Never.
- Removes: `## Files in the target repo`, `## Milestone status`, `### Reading status`.

- [ ] **Step 1: Update tests.** `test_contract_lists_every_token` now covers `FINDING_TAGS`, `FOLLOWUP_LABELS`, `TARGET_PATHS`, labels, verdicts, and `NN · <name>`, `NN.T · <task>`. Add `test_contract_has_no_rev1_terms` (calls `assert_no_rev1`). Add `test_contract_sections` for the five new headings.
- [ ] **Step 2: Run** `python3 -m unittest tests.test_contract -v` — Expected: FAIL on the new tokens and on `Reading status` present.
- [ ] **Step 3: Rewrite** the contract sections per Interfaces.
- [ ] **Step 4: Run** — Expected: `test_contract` PASS. Other suites may now fail on `STATUSES` import; fix their imports only (content changes come in their tasks).
- [ ] **Step 5: Commit** — `git commit -m "Contract: GitHub as source of truth, follow-up tag"`

### Task 2: Repo-doc templates

**Files:** Create `skills/factory/templates/product.md`, `architecture.md`. Modify `spec.md`, `build.md`. Delete `roadmap.md`, `milestone.md`. Modify `tests/test_contract.py`.

**Interfaces:**
- `product.md`: `## Vision`, `## Goals`, `## Non-goals`, `## Anti-goals`, `## Product constraints` (`Platforms:`, `Distribution:`, `Hosting and budget:`, `Hard limits:`), `## Core experiences` (one `###` per experience with `Who:`, `Trigger:`, `Journey:`, `Success:`, `Failure moments:`, `Not this:`), `## Milestones` (a link to the repo's GitHub Milestones page, no list), `## Decision log`.
- `architecture.md`: `## Stack`, `## Testing`, `## CI`, `## CD`, `## Conventions`, `## Decision log` (each entry with `Decided by: owner`).
- `spec.md`: `Milestone:` (GitHub Milestone link), `Approved:`, `## Technical design` (cites `docs/architecture.md`), new `## Experiences`, `## Architecture decisions`, `## Tasks` (ordered issue links, no task bodies), `## Definitions of done` (`AC:` and `Failure moment:` entries), `## Design reference` (keeps `Run:`), `## Flags`, `## Revisions`.
- `build.md`: keeps everything; review-round section lists each `nit` with its fix commit; adds `## Polish pass`.

- [ ] **Step 1: Update `TEMPLATE_FIELDS`** to the fields above; drop `milestone` and `roadmap`; add `test_rev1_templates_deleted` (the two files don't exist) and call `assert_no_rev1` on every template.
- [ ] **Step 2: Run** — Expected: FAIL.
- [ ] **Step 3: Write** the templates; `git rm` the two old ones.
- [ ] **Step 4: Run** — Expected: PASS.
- [ ] **Step 5: Commit** — `git commit -m "Templates: product brief, architecture; drop roadmap and milestone files"`

### Task 3: GitHub templates

**Files:** Create `skills/factory/templates/github/{milestone,pr,review,approval,escalation,task-issue,follow-up-issue,docs-pr}.md`; create `tests/test_github_templates.py`

**Interfaces:** Each file states its question on the first line as an HTML comment (`<!-- Answers: … -->`) and the title format where there is one. Required content, from design §5 and §9:

| File | Must contain |
|---|---|
| `milestone.md` | `## Goals`, `## Scope`, `### In`, `### Out`, `## Acceptance criteria`, `## Serves`, `## Flags`, `security:`, `ui:` |
| `pr.md` | `NN · `, `Milestone:`, `Spec:`, `Build log:`, `Flags:`, `## Tasks`, `Closes #` |
| `review.md` | `round N`, `## Blocking`, `## Nits (fix in this PR)`, `## Follow-ups (not this PR)`, `## What I checked`, `checked against:` |
| `approval.md` | `APPROVE — Homer`, `## What was built`, `## Acceptance criteria`, `\| AC \| Check \| Result \|`, `## Deviations`, `## Follow-ups opened`, `## CI` |
| `escalation.md` | `ESCALATED — `, `## The problem`, `## Your decision`, `Recommendation:`, `Route:`, `Resume with: /foundry:start-milestone` |
| `task-issue.md` | `NN.T · `, `Milestone:`, `Spec:`, `Covers:`, `Depends on:`, `## Build`, `## Done-check` |
| `follow-up-issue.md` | `foundry:follow-up`, `## What's wrong`, `## Impact`, `## Where`, `## Found`, `## Triage` |
| `docs-pr.md` | `Product brief · `, `## Brief changes`, `## Roadmap changes (already applied on GitHub)`, `Decision log:` |

Explicitly absent: `approval.md` has no `## Open nits` and no `## Known issues`.

- [ ] **Step 1: Write** `test_github_templates.py`: one test per file asserting the table row, plus `assert_no_rev1`, plus the two absences.
- [ ] **Step 2: Run** — Expected: FAIL (files missing).
- [ ] **Step 3: Write** the eight files, with placeholder text exactly as agreed in conversation (design §9 summarises).
- [ ] **Step 4: Run** — Expected: PASS.
- [ ] **Step 5: Commit** — `git commit -m "Add GitHub templates"`

### Task 4: Anaximander

**Files:** Modify `skills/wise-counsel/SKILL.md`, `tests/test_skills.py`

**Interfaces:**
- Consumes: `templates/product.md`, `templates/github/milestone.md`, `templates/github/docs-pr.md`, contract.
- Produces: `docs/product.md`; GitHub Milestones `NN · <name>`; triaged follow-ups; a docs PR (template 7) or a brief change left for Hypatia.

- [ ] **Step 1: Update `WiseCounsel` tests:** has `docs/product.md`, `Core experiences`, `Failure moments`, `Product constraints`, `Serves`, `NN · <name>`, `foundry:follow-up`, `Triage`, `Reconcile`, `templates/github/docs-pr.md`, `migrate`; keeps `never edit` (closed Milestones), `owner approves`; `assert_no_rev1` — **except** the migration paragraph, which must name `docs/roadmap.md` and `docs/milestones/` once. Ruling for the executor: exempt text between `<!-- migration -->` and `<!-- /migration -->` markers from `assert_no_rev1`.
- [ ] **Step 2: Run** — Expected: FAIL.
- [ ] **Step 3: Rewrite the skill** per design §7.1 session order (reconcile → triage → brief → roadmap → approve → write), the in-flight exception (§11), "required once per repo", and migration (§12): if revision-1 docs exist, offer to move each milestone file to a GitHub Milestone and the roadmap intro to `docs/product.md`'s Vision, then delete the old files in the docs PR after owner approval.
- [ ] **Step 4: Run** — Expected: PASS; `claude plugin validate .` exit 0.
- [ ] **Step 5: Commit** — `git commit -m "Anaximander: product brief, core experiences, GitHub milestones, triage"`

### Task 5: Hypatia

**Files:** Modify `skills/start-milestone/SKILL.md`, `tests/test_skills.py`

**Interfaces:**
- Consumes: GitHub Milestone (`gh api repos/{owner}/{repo}/milestones`), `docs/product.md`, `docs/architecture.md`, `templates/architecture.md`, `templates/spec.md`, `templates/github/task-issue.md`.
- Produces: branch; `docs/architecture.md` (when the foundation pass runs); spec; task issues after approval; hands to `factory`.

- [ ] **Step 1: Update `StartMilestone` tests:** has `foundation pass`, `docs/architecture.md`, `Product constraints`, `Decided by: owner`, `/foundry:wise-counsel` (no `product.md` stop), `confirm` (document existing stack), `## Experiences`, `Failure moment`, `NN.T · <task>`, `after the owner approves`, `follow-up`, `abandoned-<date>`, `Reconcile`, `in flight`; lacks `Decided by: Hypatia` in the foundation-pass section (assert the string appears only in the milestone-decisions paragraph — simplest: assert the foundation section text, sliced between `## Foundation pass` and the next `## `, lacks it); `assert_no_rev1`.
- [ ] **Step 2: Run** — Expected: FAIL.
- [ ] **Step 3: Rewrite the skill** per design §7.2 and §11 (onboarding, in-flight detection from GitHub, abandon/restart, docs PR still open → ask to merge, attached follow-ups as tasks, flag additions mirrored to the Milestone).
- [ ] **Step 4: Run** — Expected: PASS.
- [ ] **Step 5: Commit** — `git commit -m "Hypatia: foundation pass, architecture.md, task issues"`

### Task 6: Daedalus

**Files:** Modify `agents/builder.md`, `tests/test_agents.py`

- [ ] **Step 1: Update `Builder` tests:** has `templates/github/pr.md`, `Closes #`, `comment on`(each task issue), `every nit`, `Polish pass`, `docs/architecture.md` (departure escalates), `fix commit`; keeps PR #1 tokens (`Known issues`, `foundry:building`); `assert_no_rev1`.
- [ ] **Step 2: Run** — Expected: FAIL.
- [ ] **Step 3: Edit** per design §7.3: work task issues in order; comment per issue; PR body from template 1; fix mode fixes every blocking and every nit and records each nit's fix commit; polish-pass mode; `architecture.md` departures escalate; never edits `architecture.md`.
- [ ] **Step 4: Run** — Expected: PASS.
- [ ] **Step 5: Commit** — `git commit -m "Daedalus: task issues, nits fixed by default, polish pass"`

### Task 7: Reviewers

**Files:** Modify `agents/reviewer-{code,security,ux,ui}.md`, `tests/test_agents.py`

- [ ] **Step 1: Update `Reviewers` tests:** all four have `follow-up`, `templates/github/review.md`, `Known issues`; `reviewer-code` has `docs/architecture.md` (conventions); `reviewer-ux` has `docs/product.md`, `Failure moments`, `Journey`; all keep existing remit assertions; `assert_no_rev1`.
- [ ] **Step 2: Run** — Expected: FAIL.
- [ ] **Step 3: Edit** the shared rules in each file: three tags with the design §7.4 meanings; classify every known issue; body from template 2. Momus checks `architecture.md` conventions. Clotho walks the served experiences' journeys and failure moments from `docs/product.md` (read from the milestone branch).
- [ ] **Step 4: Run** — Expected: PASS.
- [ ] **Step 5: Commit** — `git commit -m "Reviewers: follow-up tag, review template, experiences"`

### Task 8: Homer

**Files:** Modify `agents/approver.md`, `tests/test_agents.py`

- [ ] **Step 1: Update `Approver` tests:** has `templates/github/approval.md`, `templates/github/escalation.md`, `templates/github/follow-up-issue.md`, `foundry:follow-up`, `## Found` (dedupe search), `no nit left open`, `Serves`, `docs/architecture.md`; lacks `Record <milestone> as shipped` and `Status: shipped` (via `assert_no_rev1` plus the commit message); keeps `never merge`, CI wait.
- [ ] **Step 2: Run** — Expected: FAIL.
- [ ] **Step 3: Edit** per design §7.5 and §11: remove the shipping commit; CI check on the PR head; follow-ups opened only on APPROVE, deduped across reviewers and against existing issues from the same PR; templates 3, 4, 6; never commits.
- [ ] **Step 4: Run** — Expected: PASS.
- [ ] **Step 5: Commit** — `git commit -m "Homer: follow-up capture, no shipping commit"`

### Task 9: Factory

**Files:** Modify `skills/factory/SKILL.md`, `tests/test_skills.py`

- [ ] **Step 1: Update `Factory` tests:** has every `FOLLOWUP_LABELS` value (preflight creates them), `Polish pass`, `Reconcile`, `templates/github/escalation.md`, `in flight`, `not counted` (polish pass vs round cap), `round 3` (blocking in polish after round 3 escalates); lacks `Reading status`; keeps every existing assertion; `assert_no_rev1`.
- [ ] **Step 2: Run** — Expected: FAIL.
- [ ] **Step 3: Edit** per design §8 and §11: preflight label set; polish-pass stage between all-PASS and Homer (skipped with no open nits; blocking → next round or escalate after round 3; one extra polish pass max; leftovers become follow-ups); escalation comment from template 4; reconcile on every run; resume reads GitHub only.
- [ ] **Step 4: Run** `python3 -m unittest discover -s tests -v` — Expected: all PASS. `claude plugin validate .` exit 0. `grep -rn "Status:\|Reading status\|docs/roadmap.md\|docs/milestones/" skills agents` — Expected: matches only inside wise-counsel's migration markers.
- [ ] **Step 5: Commit** — `git commit -m "Factory: polish pass, reconcile, follow-up labels"`

### Task 10: README

**Files:** Modify `README.md`

- [ ] **Step 1:** "What it writes into your repo": replace the four rev-1 paths with `docs/product.md`, `docs/architecture.md`, specs, builds; add a line "On GitHub: Milestones (`NN · <name>`), task issues (`NN.T · <task>`), follow-up issues, PRs." Hero table: Anaximander adds core experiences and triage; Hypatia adds the foundation pass and task issues; Homer "opens follow-up issues" replaces "records the milestone as shipped". Diagram: add the polish pass and "follow-ups → Anaximander triage". Map: add `templates/github/`.
- [ ] **Step 2:** `grep -n "roadmap.md\|milestones/\|shipped" README.md` — Expected: no stale references (the "Milestone shipped" end node becomes "Milestone closed").
- [ ] **Step 3:** Tests and `claude plugin validate .` still pass.
- [ ] **Step 4: Commit** — `git commit -m "README: revision 2"`

### Task 11: Smoke run (owner)

**Files:** Create `docs/superpowers/notes/2026-11-24-rev2-smoke-run.md`

- [ ] **Step 1:** In `~/Documents/GitHub/foundry-smoke` (which has revision-1 docs), the owner runs `claude --plugin-dir ~/Documents/GitHub/foundry` and `/foundry:wise-counsel` with a small feature idea. Expected: migration offer (Review Focus 1); follow-up triage over the 14 items, once they exist as issues — first create them: the executor opens them from the owner's pasted table as `foundry:follow-up` issues **only after the owner confirms**; core experiences written; product constraints asked; a new Milestone `04 · …`.
- [ ] **Step 2:** `/foundry:start-milestone`. Expected: foundation pass documents existing Rust/CI for confirmation and asks about CD (Review Focus 2); task issues appear after spec approval; PR uses template 1; reviews use template 2 with a `follow-up` tag at least once; Homer opens follow-ups and approves with template 3; no commit by Homer.
- [ ] **Step 3:** After merge, run `/foundry:start-milestone` again. Expected: Milestone 04 closed by reconcile (Review Focus 4).
- [ ] **Step 4:** Record outcomes and prompt fixes (fixes committed separately). Commit the note.
