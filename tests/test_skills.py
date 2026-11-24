import unittest

from contract import FOLLOWUP_LABELS, LABELS, SKILL_HEADINGS, assert_no_rev1, read


class SkillCase(unittest.TestCase):
    skill = ""

    def text(self):
        return read(f"skills/{self.skill}/SKILL.md")

    def assertHas(self, *needles):
        lower = " ".join(self.text().split()).lower()
        for needle in needles:
            with self.subTest(needle=needle):
                self.assertIn(needle.lower(), lower)

    def assertLacks(self, *needles):
        lower = " ".join(self.text().split()).lower()
        for needle in needles:
            with self.subTest(needle=needle):
                self.assertNotIn(needle.lower(), lower)

    def assertHeadings(self):
        text = self.text()
        for heading in SKILL_HEADINGS:
            with self.subTest(heading=heading):
                self.assertIn(heading, text)


class WiseCounsel(SkillCase):
    skill = "wise-counsel"

    def test_headings(self):
        self.assertHeadings()

    def test_brief(self):
        self.assertHas("docs/product.md", "templates/product.md", "Core experiences",
                       "Failure moments", "Product constraints", "Decision log")

    def test_experiences_before_milestones(self):
        self.assertHas("before proposing any milestone")

    def test_github_milestones(self):
        self.assertHas("NN · <name>", "templates/github/milestone.md", "Serves")

    def test_triage(self):
        self.assertHas("foundry:follow-up", "Triage", "won't fix")

    def test_reconcile(self):
        self.assertHas("Reconcile")

    def test_closed_milestones_never_edited(self):
        self.assertHas("never edit")

    def test_owner_approves_before_writing(self):
        self.assertHas("owner approves")

    def test_in_flight_exception(self):
        self.assertHas("in flight", "Route: Anaximander")

    def test_docs_pr(self):
        self.assertHas("templates/github/docs-pr.md", "foundry/brief-")

    def test_migration(self):
        self.assertHas("migrate", "<!-- migration -->")

    def test_no_rev1_terms(self):
        assert_no_rev1(self, self.text(), self.skill)

    def test_handoff(self):
        self.assertHas("/foundry:start-milestone")


class StartMilestone(SkillCase):
    skill = "start-milestone"

    def section(self, heading):
        text = self.text()
        body = text[text.index(heading) + len(heading):]
        return body[:body.find("\n## ")] if "\n## " in body else body

    def test_headings(self):
        self.assertHeadings()

    def test_reads_github_milestone(self):
        self.assertHas("NN · <name>", "lowest-numbered open Milestone", "Reconcile")

    def test_branch_and_spec(self):
        self.assertHas("foundry/NN-<slug>", "docs/specs/", "Approved:", "factory")

    def test_single_slot(self):
        self.assertHas("in flight", "resume", "abandon", "abandoned-<date>")

    def test_missing_fields_stop(self):
        self.assertHas("missing fields")

    def test_no_brief_sends_to_anaximander(self):
        self.assertHas("no `docs/product.md`", "/foundry:wise-counsel")

    def test_open_docs_pr_merged_first(self):
        self.assertHas("docs PR", "merge it first")

    def test_foundation_pass(self):
        self.assertHas("## Foundation pass", "docs/architecture.md", "templates/architecture.md",
                       "Product constraints", "Decided by: owner", "confirm", "CD")

    def test_foundation_never_decided_by_hypatia(self):
        self.assertNotIn("decided by: hypatia", " ".join(self.section("## Foundation pass").split()).lower())

    def test_spec_content(self):
        self.assertHas("## Experiences", "Failure moment", "Run:")

    def test_task_issues(self):
        self.assertHas("NN.T · <task>", "templates/github/task-issue.md", "after the owner approves")

    def test_follow_ups(self):
        self.assertHas("foundry:follow-up", "attached")

    def test_flags_never_removed(self):
        self.assertHas("never remove")

    def test_asks_owner_on_architecture(self):
        self.assertHas("architecture threshold", "ask the owner")

    def test_no_rev1_terms(self):
        assert_no_rev1(self, self.text(), self.skill)

    def test_resume_check_before_brief_check(self):
        text = self.text()
        self.assertLess(text.index("**Single slot.**"), text.index("**Brief.**"))

    def test_abandon_detaches_follow_ups(self):
        self.assertHas("detach", "never close a follow-up")

    def test_task_issues_not_duplicated(self):
        self.assertHas("already exists")


class Factory(SkillCase):
    skill = "factory"

    def test_headings(self):
        self.assertHeadings()

    def test_every_label(self):
        self.assertHas(*LABELS)

    def test_dispatches_every_agent(self):
        self.assertHas(
            "foundry:builder", "foundry:reviewer-code", "foundry:reviewer-security",
            "foundry:reviewer-ux", "foundry:reviewer-ui", "foundry:approver",
        )

    def test_never_merges(self):
        self.assertHas("never merge")

    def test_preflight(self):
        self.assertHas("gh auth status")

    def test_resume_from_label(self):
        self.assertHas("reads the label")

    def test_round_cap(self):
        self.assertHas("round 3")

    def test_momus_routing(self):
        self.assertHas('model: "opus"', "never haiku")

    def test_relays_escalations(self):
        self.assertHas("SendMessage", "PushNotification")

    def test_passes_contract_path(self):
        self.assertHas("contract.md")

    def test_preflight_creates_follow_up_labels(self):
        self.assertHas(*FOLLOWUP_LABELS)

    def test_polish_pass(self):
        self.assertHas("Polish pass", "not counted", "no open nits")

    def test_polish_blocking_after_round_3_escalates(self):
        self.assertHas("after round 3")

    def test_reconcile_and_in_flight(self):
        self.assertHas("Reconcile", "in flight")

    def test_escalation_template(self):
        self.assertHas("templates/github/escalation.md")

    def test_resume_expected_reviewers(self):
        self.assertHas("expected in round N", "all posted and any `CHANGES`")

    def test_polish_converted_nits(self):
        self.assertHas("Converted to follow-up")

    def test_labels_not_overwritten(self):
        self.assertLacks("--force")
        self.assertHas("only if missing")

    def test_never_tags(self):
        self.assertHas("never tag")

    def test_no_rev1_terms(self):
        assert_no_rev1(self, self.text(), self.skill)


if __name__ == "__main__":
    unittest.main()
