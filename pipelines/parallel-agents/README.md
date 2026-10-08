# Parallel Agents

Several chats implement features at the same time, each as a **lane** in its own persistent git
worktree, while one **manager** chat coordinates path ownership and merges finished lanes into an
integration branch. The user stays the only design and scope authority: each feature is defined and
approved in its own lane's chat.

This preset layers on the project's `CLAUDE.md`; it never replaces it. Every lane still plans, gets
plan approval, verifies, and dispatches review exactly as a solo session would. Install
[Recon-Build-Review](../recon-build-review/README.md) first, or make sure `CLAUDE.md` already has
equivalent planning, verification, and delegation rules.

## Shape

```text
{{MAIN_CHECKOUT}}                 the user's own checkout; no team session touches it
{{TEAM_ROOT}}\
    integration\                  manager chat, branch team/integration, LANES.md (gitignored)
    worker-1\                     lane chat: idle on detached team/integration, or lane/<id>
    worker-2\
    ...
```

Lanes talk to the manager with `[TEAM] <VERB>` messages (`PLANNING`, `REGISTER`, `GRANT`, `WAIT`,
`READY`, `MERGED`, …). Scope is always paths, never feature names; grants are all-or-nothing; claims
are released only on merge. The manager detects wait cycles and brings the user four resolution
options.

## Skills

| Skill | Run in | Does |
|---|---|---|
| `/team-setup` | Any chat in the repo | Creates missing worktrees (on the user's yes), refreshes idle slots, prepares each worktree's environment. Takes no role. |
| `/team-manager` | Integration worktree | Owns `LANES.md`, grants claims, detects deadlocks, merges and verifies lanes. |
| `/team-worker` | A worker slot | Runs one tightly scoped feature lane: plan, register paths, implement, verify, `READY`. |
| `/team-design-worker` | A worker slot | A design lane: writes feature specs for developer lanes. Never edits source. Optional. |
| `/team-clean` | A worker slot | Resets a finished lane's chat so the next feature starts with fresh context. |

## Files

| Preset file | Install to |
|---|---|
| `CLAUDE.section.md` | Merge into the project's `CLAUDE.md` |
| `template/.claude/team/PROTOCOL.md` | `.claude/team/PROTOCOL.md` |
| `template/.claude/team/LANES.template.md` | `.claude/team/LANES.template.md` |
| `template/.claude/skills/team-*/` | `.claude/skills/team-*/` (all five; drop `team-design-worker` if unwanted) |
| `template/docs/design/_TEMPLATE.md`, `BACKLOG.md` | `docs/design/` (only with the design lane) |
| — | Add `/LANES.md` to the root `.gitignore` |

## Placeholders

| Token | Meaning | Unity example | Electron example |
|---|---|---|---|
| `{{MAIN_CHECKOUT}}` | Absolute path of the user's main checkout (git root) | `C:\Projects\MyGame` | `C:\Projects\MyApp` |
| `{{TEAM_ROOT}}` | Absolute folder holding the team worktrees, beside the main checkout | `C:\Projects\MyGame-team` | `C:\Projects\MyApp-team` |
| `{{PROJECT_DIR}}` | The project folder inside each worktree, relative to the worktree root | `MyGame` (Unity project in a subfolder) | `.` |
| `{{PROTECTED_BRANCHES}}` | Branches no team session commits to or merges into | `` `QA`, `main` `` | `` `main` `` |
| `{{AGENT_PREFIX}}` | The Recon-Build-Review agent prefix | `unity` | `electron` |

When `{{PROJECT_DIR}}` is `.`, simplify phrases like "the worktree's `{{PROJECT_DIR}}` folder" to "the
worktree root" while installing.

In `team_status.py`, set `PROJECT_DIR` and `ENV_CHECK` at the top. It ships with `node` (lockfile vs
last install), `unity` (Editor reachability through the Unity pipeline CLI), and `none` checks. Add one
for other stacks.

## What to adapt

Almost everything stack-specific lives in two sections of `PROTOCOL.md`; the skills refer to them by
name and rarely need edits:

- **Per-worktree environment** — how a worktree is prepared (install dependencies, open an Editor),
  how to tell it is ready, how to confirm commands target this worktree and not another, and what
  resources worktrees share and can collide on (an app data folder, a dev-server port, a license).
- **Unmergeable files** — files that must never be hand-merged, and how each is resolved instead
  (Unity scene/prefab YAML in the lane's own Editor; `package-lock.json` regenerated from the resolved
  `package.json`).

Also adapt the **hot spots** list (files many features touch) and, if the design lane is kept, its
"What you may change" table and any extra kinds of design work the project supports (the Unity
reference adds balance passes through TSV data and data-only content).
