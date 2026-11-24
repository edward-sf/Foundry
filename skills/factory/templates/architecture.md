# Architecture: <name>

<!-- Owned by Hypatia. Every decision here is the owner's. Specs cite this
file rather than re-deciding it; departing from it is always an escalation.
Changes ride the milestone PR of the foundation pass that made them. -->

## Stack

<Language, runtime and key libraries. For each: what was chosen, what was
rejected and why. Trace each to the product constraints it serves.>

## Testing

<Test layers (unit, integration, end to end), tools, and where tests live.>

## CI

<What runs, on which platforms (matching the product constraints), the
pinned toolchain, caching, and the dependency and security audit.>

## CD

<What a release is; its trigger (a tag the owner pushes; Foundry never tags);
what it builds; where it publishes; which secrets it needs.>

## Conventions

<Project structure, error handling, naming, and anything else every
milestone must follow.>

## Decision log

<!-- One entry per decision, newest last. -->

### <YYYY-MM-DD>: <decision>

- Chosen: <option>
- Rejected: <option> — <why not>
- Why: <reason, citing product constraints where they apply>
- Decided by: owner
