import unittest

from contract import assert_no_rev1, read

REQUIRED = {
    "milestone": ["## Goals", "## Scope", "### In", "### Out", "## Acceptance criteria",
                  "## Serves", "## Flags", "security:", "ui:"],
    "pr": ["NN · ", "Milestone:", "Spec:", "Build log:", "Flags:", "## Tasks", "Closes #"],
    "review": ["round N", "## Blocking", "## Nits (fix in this PR)",
               "## Follow-ups (not this PR)", "## What I checked", "checked against:"],
    "approval": ["APPROVE — Homer", "## What was built", "## Acceptance criteria",
                 "| AC | Check | Result |", "## Deviations", "## Follow-ups opened", "## CI"],
    "escalation": ["ESCALATED — ", "## The problem", "## Your decision", "Recommendation:",
                   "Route:", "Resume with: /foundry:start-milestone"],
    "task-issue": ["NN.T · ", "Milestone:", "Spec:", "Covers:", "Depends on:", "## Build",
                   "## Done-check"],
    "follow-up-issue": ["foundry:follow-up", "## What's wrong", "## Impact", "## Where",
                        "## Found", "## Triage"],
    "docs-pr": ["Product brief · ", "## Brief changes",
                "## Roadmap changes (already applied on GitHub)", "Decision log:"],
}


def path(name):
    return f"skills/factory/templates/github/{name}.md"


class GitHubTemplates(unittest.TestCase):
    def test_required_content(self):
        for name, needles in REQUIRED.items():
            text = read(path(name))
            for needle in needles:
                with self.subTest(template=name, needle=needle):
                    self.assertIn(needle, text)

    def test_each_states_its_question(self):
        for name in REQUIRED:
            with self.subTest(template=name):
                self.assertTrue(read(path(name)).startswith("<!-- Answers: "))

    def test_no_rev1_terms(self):
        for name in REQUIRED:
            assert_no_rev1(self, read(path(name)), path(name))

    def test_approval_drops_open_nits_and_known_issues(self):
        text = read(path("approval"))
        for gone in ["## Open nits", "## Known issues"]:
            with self.subTest(gone=gone):
                self.assertNotIn(gone, text)


if __name__ == "__main__":
    unittest.main()
