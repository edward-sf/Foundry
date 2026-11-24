import unittest

from contract import AGENT_HEADINGS, assert_no_rev1, read


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

    def test_task_issues(self):
        self.assertHas("templates/github/pr.md", "Closes #", "comment on the task issue")

    def test_fixes_every_nit(self):
        self.assertHas("every `nit`", "fix commit", "Polish pass")

    def test_architecture_departure_escalates(self):
        self.assertHas("docs/architecture.md")

    def test_keeps_pr1_fixes(self):
        self.assertHas("## Known issues", "foundry:building")

    def test_no_rev1_terms(self):
        assert_no_rev1(self, read("agents/builder.md"), "builder")

    def test_converted_nits(self):
        self.assertHas("Converted to follow-up")


REVIEWERS = ["reviewer-code", "reviewer-security", "reviewer-ux", "reviewer-ui"]


class Reviewers(AgentCase):
    def test_shared_rules(self):
        for self.agent in REVIEWERS:
            self.assertHeadings()
            self.assertHas("PASS", "CHANGES", "blocking", "nit", "never push")

    def test_rev2_shared_rules(self):
        for self.agent in REVIEWERS:
            self.assertHas("follow-up", "templates/github/review.md", "Known issues",
                           "Finding tags")
            assert_no_rev1(self, read(f"agents/{self.agent}.md"), self.agent)

    def test_momus_checks_architecture_conventions(self):
        self.agent = "reviewer-code"
        self.assertHas("docs/architecture.md", "polish", "round N · polish")

    def test_clotho_walks_experiences(self):
        self.agent = "reviewer-ux"
        self.assertHas("docs/product.md", "Failure moments", "Journey", "Serves")

    def test_momus_checks_definitions_of_done(self):
        self.agent = "reviewer-code"
        self.assertHas("Definitions of done")

    def test_clotho_remit(self):
        self.agent = "reviewer-ux"
        self.assertHas("empty", "loading", "error", "keyboard", "focus")
        self.assertLacks("contrast")

    def test_lachesis_remit(self):
        self.agent = "reviewer-ui"
        self.assertHas("Design reference", "contrast", "breakpoints", "tokens")
        self.assertLacks("keyboard")

    def test_lachesis_without_reference(self):
        self.agent = "reviewer-ui"
        self.assertHas("internal consistency")


class Approver(AgentCase):
    agent = "approver"

    def test_headings(self):
        self.assertHeadings()

    def test_verdicts_and_routes(self):
        self.assertHas("APPROVE", "ESCALATE", "Route:", "Daedalus", "Hypatia", "Anaximander")

    def test_templates(self):
        self.assertHas("templates/github/approval.md", "templates/github/escalation.md",
                       "templates/github/follow-up-issue.md")

    def test_follow_ups(self):
        self.assertHas("foundry:follow-up", "## Found", "duplicate", "only on APPROVE")

    def test_checks(self):
        self.assertHas("no nit left open", "Serves", "docs/architecture.md", "Failure moment")

    def test_ci_on_head(self):
        self.assertHas("gh pr checks")

    def test_no_shipping_commit(self):
        self.assertLacks("as shipped", "Record <milestone>")
        self.assertHas("never commit")
        assert_no_rev1(self, read("agents/approver.md"), "approver")

    def test_never_merges(self):
        self.assertHas("never merge")

    def test_accepts_converted_nits(self):
        self.assertHas("Converted to follow-up")

    def test_dedupe_without_search_index(self):
        self.assertHas("--json number,title,body", "already has an `APPROVE — Homer` comment")


if __name__ == "__main__":
    unittest.main()
