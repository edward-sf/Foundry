import unittest

from contract import LABELS, SKILL_HEADINGS, read


class SkillCase(unittest.TestCase):
    skill = ""

    def text(self):
        return read(f"skills/{self.skill}/SKILL.md")

    def assertHas(self, *needles):
        lower = " ".join(self.text().split()).lower()
        for needle in needles:
            with self.subTest(needle=needle):
                self.assertIn(needle.lower(), lower)

    def assertHeadings(self):
        text = self.text()
        for heading in SKILL_HEADINGS:
            with self.subTest(heading=heading):
                self.assertIn(heading, text)


class WiseCounsel(SkillCase):
    skill = "wise-counsel"

    def test_headings(self):
        self.assertHeadings()

    def test_artifacts(self):
        self.assertHas("docs/roadmap.md", "docs/milestones/", "planned", "shipped", "gh ")

    def test_shipped_milestones_never_edited(self):
        self.assertHas("never edit")

    def test_owner_approves_before_writing(self):
        self.assertHas("owner approves")

    def test_docs_pr_when_no_build(self):
        self.assertHas("foundry/roadmap-", "docs PR")

    def test_reads_what_was_built(self):
        self.assertHas("docs/builds/", "merged")

    def test_handoff(self):
        self.assertHas("/foundry:start-milestone")


class StartMilestone(SkillCase):
    skill = "start-milestone"

    def test_headings(self):
        self.assertHeadings()

    def test_artifacts(self):
        self.assertHas("in-progress", "docs/specs/", "Approved:", "foundry/NN-<slug>")

    def test_hands_to_factory(self):
        self.assertHas("factory")

    def test_single_slot(self):
        self.assertHas("another milestone is in-progress", "resume", "abandon")

    def test_missing_fields_stop(self):
        self.assertHas("missing fields")

    def test_no_ci_adds_task(self):
        self.assertHas("no CI")

    def test_flags_never_removed(self):
        self.assertHas("never remove")

    def test_sends_back_to_anaximander(self):
        self.assertHas("/foundry:wise-counsel")

    def test_reconciles_shipped_mirrors(self):
        self.assertHas("Reconcile mirrors")

    def test_asks_owner_on_architecture(self):
        self.assertHas("architecture threshold", "ask the owner")


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


if __name__ == "__main__":
    unittest.main()
