import unittest

from contract import AGENT_HEADINGS, read


class AgentCase(unittest.TestCase):
    agent = ""

    def flat(self):
        return " ".join(read(f"agents/{self.agent}.md").split()).lower()

    def assertHas(self, *needles):
        text = self.flat()
        for needle in needles:
            with self.subTest(agent=self.agent, needle=needle):
                self.assertIn(needle.lower(), text)

    def assertLacks(self, *needles):
        text = self.flat()
        for needle in needles:
            with self.subTest(agent=self.agent, needle=needle):
                self.assertNotIn(needle.lower(), text)

    def assertHeadings(self):
        text = read(f"agents/{self.agent}.md")
        for heading in AGENT_HEADINGS:
            with self.subTest(agent=self.agent, heading=heading):
                self.assertIn(heading, text)


class Builder(AgentCase):
    agent = "builder"

    def test_headings(self):
        self.assertHeadings()

    def test_artifacts(self):
        self.assertHas("docs/builds/", "draft", "Done-check", "Review round")

    def test_return_values(self):
        self.assertHas("ESCALATE", "READY <pr-number>")

    def test_never_edits_spec_or_milestone(self):
        self.assertHas("never edit the spec or the milestone")

    def test_no_ci_falls_back_to_local(self):
        self.assertHas("no CI: local checks only")

    def test_gate_before_ready(self):
        self.assertHas("gh pr ready", "gh pr checks")


if __name__ == "__main__":
    unittest.main()
