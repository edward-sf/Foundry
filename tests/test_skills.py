import unittest

from contract import LABELS, SKILL_HEADINGS, read


class SkillCase(unittest.TestCase):
    skill = ""

    def text(self):
        return read(f"skills/{self.skill}/SKILL.md")

    def assertHas(self, *needles):
        text = self.text()
        lower = text.lower()
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


if __name__ == "__main__":
    unittest.main()
