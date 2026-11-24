# Spike: subagent escalation and resume

Date: 2026-11-23. Throwaway agent `spike-escalator` (frontmatter `model: haiku`),
dispatched from a non-interactive session started with
`claude -p --plugin-dir <foundry repo>`. The agent was deleted after the run.

| Question | Observed |
|---|---|
| `subagent_type` for a plugin agent | `foundry:<agent-name>` (e.g. `foundry:spike-escalator`), worked first try |
| Does the subagent's final reply (incl. an `ESCALATE` line) reach the parent? | Yes, verbatim |
| Does `SendMessage` to the agent's id resume the **same** agent with context? | Yes. Returned `Resuming agent <id>` with the same `resumedAgentId`; the agent appended to the file it had created without being told its name |
| Is `AskUserQuestion` available inside a subagent? | **No.** Subagents cannot ask the owner directly |
| Does the Agent tool's `model` parameter override frontmatter `model`? | Yes. Frontmatter said `haiku`, the call passed `sonnet`, the agent reported running on Sonnet |

## Call shapes for the factory

- Dispatch: `Agent(subagent_type: "foundry:builder", description: ..., prompt: ..., model: <optional override>)`
- Escalation: the agent ends its reply with the `ESCALATE` block and stops.
  The orchestrator asks the owner (AskUserQuestion, main session), then
  `SendMessage(to: <agent id>, message: <owner's answer>)` to resume.
- Momus routing: pass `model: "opus"` on the Agent call to override the
  `sonnet` frontmatter default.

## Consequences

- Design §7's escalation path works as written; no fallback needed. The
  fallback (fresh agent + owner's answer + `build.md`) stays the path when
  the session has closed, since agent ids don't survive the session.
- Confirms Anaximander and Hypatia must run in the main session (skills),
  not as subagents.
