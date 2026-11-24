import unittest

from contract import (
    FINDING_TAGS,
    FLAGS,
    HOMER_VERDICTS,
    LABELS,
    REVIEW_VERDICTS,
    STATUSES,
    TARGET_PATHS,
    read,
)

TEMPLATE_FIELDS = {
    "milestone": [
        "Milestone:", "Status:", "## Goals", "## Scope", "### In", "### Out",
        "## Acceptance criteria", "## Flags", "security:", "ui:", "GitHub Milestone:",
    ],
    "roadmap": ["## Milestones", "## History"],
    "spec": [
        "Milestone:", "Approved:", "## Technical design", "## Architecture decisions",
        "Decided by:", "## Tasks", "Done-check:", "## Definitions of done", "AC:",
        "## Design reference", "## Flags", "## Revisions",
    ],
    "build": ["Spec:", "## Tasks", "Deviations:", "Verified:", "## Gate", "## Review round"],
}


class Contract(unittest.TestCase):
    def test_contract_lists_every_token(self):
        text = read("skills/factory/contract.md")
        tokens = STATUSES + FLAGS + LABELS + REVIEW_VERDICTS + FINDING_TAGS + HOMER_VERDICTS
        for token in tokens + TARGET_PATHS:
            with self.subTest(token=token):
                self.assertIn(token, text)

    def test_contract_defines_escalation_block(self):
        text = read("skills/factory/contract.md")
        for field in ["ESCALATE", "Question:", "Options:", "Recommendation:"]:
            with self.subTest(field=field):
                self.assertIn(field, text)

    def test_template_fields(self):
        for template, fields in TEMPLATE_FIELDS.items():
            text = read(f"skills/factory/templates/{template}.md")
            for field in fields:
                with self.subTest(template=template, field=field):
                    self.assertIn(field, text)


if __name__ == "__main__":
    unittest.main()
