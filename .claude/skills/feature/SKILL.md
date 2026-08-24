---
name: feature
description: Manage current feature workflow - start, review, explain or complete
argument-hint: load|start|review|test|explain|complete
---

# Feature Workflow

Manages the full lifecycle of a feature from spec to merge.

Adaptado de https://github.com/bradtraversy/devstash/blob/main/.claude/skills/feature/SKILL.md
para el repo educativo `alg-lineal-I` (Python, sin frameworks JS).

## Working File

@context/current-feature.md

### File Structure

current-feature.md has these sections:

- `# Current Feature` - H1 heading with feature name when active
- `## Status` - Not Started | In Progress | Complete
- `## Goals` - Bullet points of what success looks like
- `## Notes` - Additional context, constraints, or details from spec
- `## History` - Completed features (append only)

## Task

Execute the requested action: $ARGUMENTS

| Action     | Description                                               |
| ---------- | --------------------------------------------------------- |
| `load`     | Load a feature spec or inline description                 |
| `start`    | Begin implementation, create branch                       |
| `review`   | Check goals met, code quality                             |
| `test`     | Check for testable logic and write/run Python tests        |
| `explain`  | Document what changed and why                             |
| `complete` | Commit, merge, reset (push only with explicit user OK)    |

See [actions/](actions/) for detailed instructions.

If no action provided, explain the available options.
