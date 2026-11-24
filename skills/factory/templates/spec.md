# Spec: <milestone name>

Milestone: [NN · <name>](<GitHub Milestone link>)
Approved:
<!-- Hypatia sets this to YYYY-MM-DD when the owner approves. Empty = draft. -->

## Technical design

<Components, data, interfaces. How the milestone works. Cite
`docs/architecture.md` for stack and conventions; never re-decide them here.>

## Experiences

<For each core experience in the Milestone's Serves line: how this design
supports its journey, and which of its failure moments this milestone touches.>

## Architecture decisions

<Decisions for this milestone only. Project-wide ones belong in
docs/architecture.md.>

### <Decision>

- Chosen: <option>
- Rejected: <option> — <why not>
- Why: <reason>
- Decided by: owner | Hypatia

## Tasks

<In build order. Each is a GitHub issue created after the owner approves this
spec; its body holds what to build and its Done-check:.>

1. [#<n> NN.T · <task>](<issue link>)

## Definitions of done

- AC: AC1 — Check: <named test, command, or observable behaviour>
- Failure moment: <experience> / <failure moment> — Check: <named test or command>

## Design reference

<Only when ui: yes. The design system, tokens or existing screens Lachesis
checks against, or "none" if there is none.>

Run: server: <start command> → <URL> | local: <commands to build and run it>
<Only when ui: yes. `server:` for anything reviewed through a URL (the factory
starts it); `local:` for anything run directly, such as a CLI, desktop app or
library demo (each reviewer runs the commands in a temporary sandbox).>

## Flags

security: no
ui: no

## Revisions

<Each revision after approval: date, what changed, why. Owner re-approves.>
