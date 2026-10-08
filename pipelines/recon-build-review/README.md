# Recon-Build-Review

A plan-gated working method with three bounded subagents. The main session owns requirements, scope,
architecture, and the final report; subagents do bounded work from self-contained handoffs and never
redefine the feature.

## Flow

```text
User request
  └─ Main session plans (plan mode for feature-scale work)
       ├─ Recon (optional, once): explorer answers one focused question set, read-only
       └─ User approves the plan  ← implementation gate
            └─ Build: main session implements directly, or dispatches the worker
                 └─ Verify in proportion to risk; report what ran, passed, failed, unverified
                      └─ Review (only on a material-risk signal): reviewer, read-only, findings only
                           └─ Blocking findings → same worker fixes them → reviewer re-checks only those
```

## Roles

| Role | Agent | Model / effort | Writes? | Dispatched when |
|---|---|---|---|---|
| Recon | `{{AGENT_PREFIX}}-explorer` | opus / low | Never | A concrete unresolved question would otherwise make implementation guesswork. One pass; never re-run. |
| Build | `{{AGENT_PREFIX}}-worker` | inherit | Yes, approved scope only | The change is large enough to benefit from an isolated context. Otherwise the main session implements. |
| Review | `{{AGENT_PREFIX}}-reviewer` | opus / high | Never | Any material-risk signal from `CLAUDE.md` is present. Skipped only when none is. |

Key properties, which adaptation must preserve:

- **Self-contained handoffs.** Subagents do not inherit the conversation. Each agent lists its required
  handoff and stops to report missing context rather than guessing.
- **Plan approval is the gate.** No implementation edits or persisted state before it; after it, no
  per-command approval for what the plan reasonably needs.
- **Findings-only reviews.** No walkthrough of what was found sound unless a finding will be disputed;
  a clean review is a legitimate result.
- **Focused fix passes.** Blocking findings go back to the same worker; the reviewer verifies only
  those fixes.
- **Honest verification reporting.** Exactly what ran, passed, failed, and remains unverified; at most
  one fallback per blocked objective.

## Files

| Preset file | Install to |
|---|---|
| `CLAUDE.section.md` | Merge into the project's `CLAUDE.md` |
| `template/.claude/agents/explorer.md` | `.claude/agents/{{AGENT_PREFIX}}-explorer.md` |
| `template/.claude/agents/worker.md` | `.claude/agents/{{AGENT_PREFIX}}-worker.md` |
| `template/.claude/agents/reviewer.md` | `.claude/agents/{{AGENT_PREFIX}}-reviewer.md` |
| `template/.claude/skills/verify/SKILL.md` | `.claude/skills/{{AGENT_PREFIX}}-verify/SKILL.md` |
| `template/.claude/settings.json` | Merge into `.claude/settings.json` |

**The verify skill** holds the project's concrete verification commands: how to build, type-check or
compile, run tests (and the known baseline failures), inspect runtime state, and run the app. Write it
only from commands that exist. On a project with no tooling yet, defer it, and point the worker at
`CLAUDE.md`'s verification rules and the project's scripts instead; add the skill when tooling lands.

## Placeholders

| Token | Meaning | Unity example | Electron example |
|---|---|---|---|
| `{{AGENT_PREFIX}}` | Short stack prefix for agent and skill names | `unity` | `electron` |
| `{{STACK_NAME}}` | Stack as used in descriptions | `Unity` | `Electron` |
| `{{STACK_DETAIL}}` | Stack as used in the worker and reviewer descriptions | `Unity/C#` | `Electron/TypeScript/React` |
| `{{CONVENTIONS_DOC}}` | The conventions document | `docs/UNITY_CONVENTIONS.md` | `docs/ELECTRON_CONVENTIONS.md` |
| `{{WIRING_SURFACES}}` | Where a system's wiring lives | `across scenes, prefabs, and ScriptableObjects` | `across main, preload, and renderer` |
| `{{RUNTIME_STATE}}` | What "live state" means for the stack | `live Editor state` | `the IPC contract and preload API` |
| `{{OWNERSHIP_TERM}}` | The project's ownership boundary concept | `ownership (Bootstrap / CoreKernel / area scenes)` | `process ownership` |

The agents and `CLAUDE.section.md` also contain `ADAPT` sections for command allowlists, risk signals,
and review priorities. Their comments show both examples.

## Adaptation notes

- **Write an ownership-boundaries section** in `CLAUDE.md` for the stack (see `CLAUDE.section.md`).
  Most of the explorer's and reviewer's value comes from checking work against it.
- **Read-only means read-only for the stack.** Define it concretely: which commands change state
  (opening a scene, launching an app, installing packages, building into the tree, formatters with
  fix mode) and forbid them for the explorer and reviewer.
- **Reviewer and tests.** The default is that the reviewer reads the worker's evidence rather than
  reproducing it. That keeps reviews cheap. On stacks where running a check is side-effect-free, it may
  run a type-check or single test when a specific claim lacks evidence. On stacks where a test run can
  disturb shared state (a live Editor), forbid it outright and say why in the agent file.
- **Model and effort** values are the ones the reference projects use. Change them deliberately.
