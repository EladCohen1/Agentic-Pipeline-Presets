<!--
Sections to merge into the project's CLAUDE.md. This file is not installed as-is.
Keep the project's own sections (stack baseline, repository layout, tooling) and add these after them.
-->

## Ownership boundaries

<!-- ADAPT: Define the project's runtime ownership scopes, and what each must and must not own. Name the
concrete folders or assets. State the reason for each "must not", so agents can judge edge cases.
Unity example: Bootstrap scene (composition, no shared gameplay state) / CoreKernel prefab (persistent
cross-scene systems) / area scenes (area-specific simulation).
Electron example: src/main (lifecycle, OS, IPC handlers, persistence) / src/preload (contextBridge API
only, no logic) / src/renderer (UI, no Node) / src/shared (types and IPC contract, no runtime imports).
Then add a "Source location" rule: where repository-owned code lives, feature-first organization, and
no parallel trees. -->

Classify a feature's {{OWNERSHIP_TERM}} before implementing it.

## Reference documents

- **`{{CONVENTIONS_DOC}}`** is authoritative for architecture and code. Read only the sections
  relevant to the task. Its hard conventions are the normal standard — depart only for a concrete
  reason, and say why. Its architectural preferences are judgment-guiding, not mechanical absolutes:
  a justified feature need can outweigh one.

<!-- ADAPT: If the project has a design document (GDD, product spec, feature specs folder), add:
- **`<design doc>`** is design context and current direction, not a specification. Read the relevant
  section only when a task materially depends on product direction, rules, or terminology. The user is
  the final design authority. Do not invent constraints from its silence. If a request materially
  conflicts with it, surface the conflict while planning; never silently rewrite the request.
Keep the two distinct: the design doc informs feature intent, the convention guide informs code.
If there is none yet, say so in one line and keep "the user is the final design authority". -->

## Verification

Source inspection alone does not verify runtime behavior. Verify in proportion to scope and credible
failure modes:

<!-- ADAPT: Replace with the stack's proportional checks, for example:
Unity: compilation plus the narrowest relevant tests for C# logic; authored-state inspection and
targeted Editor/Play Mode checks for Unity integration; the complete diff for text-only work.
Electron: type-checking plus the narrowest relevant tests for logic; launching the app and checking
main-process output and the renderer console for process-integration work; the complete diff for
text-only work. Name the verify skill if one exists ("Load the `<prefix>-verify` skill"). -->

Stop when acceptance criteria and identified risks have evidence, or when further checks would
duplicate coverage. While a check's tooling does not exist yet, say so instead of implying coverage.

For each blocked verification objective try at most one fallback, unless new evidence reveals a distinct
failure mode. **Report exactly what ran, passed, failed, and remains unverified.** Never declare
completion while a known implementation-caused build error, test failure, or blocking finding remains.

## Working method

Own requirements, scope, architecture, and the final report yourself. For anything beyond a trivial or
purely informational change, plan first: clarify purpose, behavior, acceptance criteria, ownership,
data flow, dependencies, and lifecycle concerns; inspect only the context needed to plan accurately;
keep design questions separate from technical ones (convention guide); and name real alternatives.

Call out unnecessary complexity, weak abstractions, coupling, premature optimization, inappropriate
inheritance, unclear ownership, ad-hoc lookup or globals, and lifecycle risk — recommend the simpler
design when it achieves the same goal. Do not agree with a design merely because the user proposed it,
and do not add abstraction to look sophisticated. Read-only inspection never needs approval.

**Use plan mode for feature-scale work.** Exiting plan mode with the user's approval is the
implementation gate — before that, do not edit implementation files, install dependencies, or persist
runtime or tool state. After it, that approval covers the commands the plan reasonably needs; do not
stop to ask per command. If later findings materially change the approved scope or architecture,
return to the user with a revised plan before continuing.

## Delegation

Two independent judgments, not a fixed route table:

- **Recon** — dispatch one `{{AGENT_PREFIX}}-explorer` pass when a concrete unresolved question about
  files, symbols, {{RUNTIME_STATE}}, ownership, or integration would otherwise make implementation
  guesswork. Resolve remaining uncertainty yourself or return to the user; do not re-run
  reconnaissance.
- **Review** — dispatch `{{AGENT_PREFIX}}-reviewer` whenever any material-risk signal is present:
  <!-- ADAPT: stack-specific signals first, for example:
  Unity: cross-scene or persistent ownership changes; lifecycle, initialization-order, serialization,
  or event-cleanup risk; non-trivial scene, prefab, or ScriptableObject authoring.
  Electron: process ownership or boundary changes; preload API or IPC contract changes; security
  settings (webPreferences, CSP, navigation, openExternal); lifecycle or subscription-cleanup risk. -->
  persistence, schema, or migration changes; shared or global state changes; public API or
  architectural-boundary changes; concurrency, hot-path, or destructive behavior; new or upgraded
  dependencies; broad diffs; weak verification evidence; or material deviation from the plan. Record
  every applicable signal in the handoff, attach every approved plan the diff builds on (including
  earlier ones in the same working tree), and ask for findings only unless a finding is expected to be
  disputed. Skip review only when no signal exists.

`{{AGENT_PREFIX}}-worker` handles implementation when the change is large enough to benefit from an
isolated context; implement directly when it is not. Give each subagent a self-contained handoff — it
does not inherit this conversation. Subagents do bounded work and must not redefine the feature.

Route legitimate blocking findings back to the same worker, which fixes those findings and their direct
consequences only; the reviewer then verifies only those fixes rather than starting a fresh review.
