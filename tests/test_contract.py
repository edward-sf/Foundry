import unittest

from contract import (
    FINDING_TAGS,
    FLAGS,
    FOLLOWUP_LABELS,
    HOMER_VERDICTS,
    LABELS,
    REVIEW_VERDICTS,
    TARGET_PATHS,
    TITLE_FORMATS,
    assert_no_rev1,
    read,
)

CONTRACT = "skills/factory/contract.md"

TEMPLATE_FIELDS = {
    "spec": [
        "Milestone:", "Approved:", "## Technical design", "## Architecture decisions",
        "Decided by:", "## Tasks", "Done-check:", "## Definitions of done", "AC:",
        "## Design reference", "## Flags", "## Revisions",
    ],
    "build": ["Spec:", "## Tasks", "Deviations:", "Verified:", "## Gate", "## Review round"],
}


class Contract(unittest.TestCase):
    def test_contract_lists_every_token(self):
        text = read(CONTRACT)
        tokens = (FLAGS + LABELS + REVIEW_VERDICTS + FINDING_TAGS + FOLLOWUP_LABELS
                  + HOMER_VERDICTS + TARGET_PATHS + TITLE_FORMATS)
        for token in tokens:
            with self.subTest(token=token):
                self.assertIn(token, text)

    def test_contract_sections(self):
        text = read(CONTRACT)
        for heading in ["## Source of truth", "## Milestones on GitHub", "## Issues",
                        "## Finding tags", "## Templates"]:
            with self.subTest(heading=heading):
                self.assertIn(heading, text)

    def test_contract_has_no_rev1_terms(self):
        assert_no_rev1(self, read(CONTRACT), CONTRACT)

    def test_contract_defines_escalation_block(self):
        text = read(CONTRACT)
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
