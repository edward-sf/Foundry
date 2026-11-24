"""Shared names every Foundry file must agree on (mirrors the plan's Global Constraints)."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

FLAGS = ["security", "ui"]
LABELS = [
    "foundry:building",
    "foundry:review-r1",
    "foundry:review-r2",
    "foundry:review-r3",
    "foundry:awaiting-homer",
    "foundry:escalated",
    "foundry:ready-to-merge",
]
REVIEW_VERDICTS = ["PASS", "CHANGES"]
FINDING_TAGS = ["blocking", "nit", "follow-up"]
FOLLOWUP_LABELS = ["foundry:follow-up", "bug", "robustness", "out-of-scope"]
HOMER_VERDICTS = ["APPROVE", "ESCALATE"]
TARGET_PATHS = [
    "docs/product.md",
    "docs/architecture.md",
    "docs/specs/<date>-NN-<slug>.md",
    "docs/builds/<date>-NN-<slug>.md",
]
TITLE_FORMATS = ["NN · <name>", "NN.T · <task>"]
# Revision-1 concepts that must not survive anywhere (repo docs no longer record state).
REV1_TERMS = ["Status:", "Reading status", "docs/roadmap.md", "docs/milestones/", "## History"]

AGENT_MODELS = {
    "builder": "opus",
    "reviewer-code": "sonnet",
    "reviewer-security": "opus",
    "reviewer-ux": "sonnet",
    "reviewer-ui": "haiku",
    "approver": "opus",
}
SKILLS = ["wise-counsel", "start-milestone", "factory"]

AGENT_HEADINGS = ["## Inputs", "## Outputs", "## Rules", "## Escalation"]
SKILL_HEADINGS = ["## Inputs", "## Outputs", "## Rules", "## Handoff"]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def read_frontmatter(rel: str) -> dict:
    lines = read(rel).splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    fm = {}
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if ":" in line and not line.startswith(" "):
            key, _, value = line.partition(":")
            fm[key.strip()] = value.strip().strip('"')
    return fm


def strip_migration(text: str) -> str:
    """Drop text between <!-- migration --> markers (the only place rev-1 paths may be named)."""
    out, rest = [], text
    while "<!-- migration -->" in rest:
        before, _, after = rest.partition("<!-- migration -->")
        out.append(before)
        _, _, rest = after.partition("<!-- /migration -->")
    out.append(rest)
    return "".join(out)


def assert_no_rev1(testcase, text: str, where: str = "") -> None:
    cleaned = strip_migration(text)
    for term in REV1_TERMS:
        with testcase.subTest(where=where, rev1_term=term):
            testcase.assertNotIn(term, cleaned)
