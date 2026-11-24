# Build: <milestone name>

Spec: [<date>-NN-<slug>](../specs/<date>-NN-<slug>.md)
PR: <link>

## Tasks

### #<n> NN.T · <task>

<What was done.>

Deviations: none | <what differed from the spec, and why>
Verified: <the done-check that was run, and its result>

## Known issues

<Anything you noticed but did not fix: what it is, how to trigger it, and why
it was left. Or "none".>

## Gate

Local: <commands run and results>
CI: <result, or "no CI: local checks only">

## Review round 1

<Every blocking finding and every nit, each with its fix commit:
- [blocking|nit] <reviewer>: <finding> — fix commit <sha>
Follow-ups are not fixed here; Homer opens them.>

## Polish pass

<Only if all reviewers passed with nits open. Each nit with its fix commit,
then Momus's re-check result. Or "not needed".
A nit that is out of scope, or still open after the last polish pass, is
recorded here, not dropped:
- Converted to follow-up: <reviewer>: <finding> — <why it can't be fixed here>>
