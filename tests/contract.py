"""Shared names every Foundry file must agree on (mirrors the plan's Global Constraints)."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

STATUSES = ["planned", "in-progress", "shipped"]
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
FINDING_TAGS = ["blocking", "nit"]
HOMER_VERDICTS = ["APPROVE", "ESCALATE"]
TARGET_PATHS = [
    "docs/roadmap.md",
    "docs/milestones/NN-<slug>.md",
    "docs/specs/<date>-<milestone-slug>.md",
    "docs/builds/<date>-<milestone-slug>.md",
]

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
