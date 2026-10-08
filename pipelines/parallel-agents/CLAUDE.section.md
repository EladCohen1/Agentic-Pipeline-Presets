<!--
Section to merge into the project's CLAUDE.md. This file is not installed as-is.
-->

## Parallel team

`.claude/team/PROTOCOL.md` defines the parallel lane workflow (`/team-setup`, `/team-manager`,
`/team-worker`, `/team-design-worker`, `/team-clean`). It layers on top of this file and applies only
in sessions that run one of those skills.

<!-- ADAPT: If the design lane is installed, also add a bullet under "Reference documents":
- **`docs/design/`** holds feature specs (indexed in `docs/design/BACKLOG.md`). An `approved` spec is
  the feature's intent; read it when a task implements or depends on that feature. Do not invent
  constraints from a spec's silence. If a request materially conflicts with an approved spec, surface
  the conflict while planning. -->
