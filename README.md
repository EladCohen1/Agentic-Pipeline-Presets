# Agentic Pipeline Presets

Generic presets for Claude Code agent pipelines, written to fit almost any coding project. Each preset
is a folder with the operating instructions, agent definitions, and skills a project needs, plus
guidance for adapting the parts that depend on the project's stack.

This repository is the reference. A project never links to it at runtime: applying a preset copies and
adapts its files into the project, which then owns them.

## Presets

| Preset | What it gives a project | Requires |
|---|---|---|
| [Recon-Build-Review](pipelines/recon-build-review/README.md) | A plan-gated working method, with three subagents: a read-only **explorer** for one focused recon pass, an implementation **worker** for approved plans, and a read-only critical **reviewer** dispatched on explicit risk signals. Self-contained handoffs, findings-only reviews, and focused fix passes. | Nothing |
| [Parallel Agents](pipelines/parallel-agents/README.md) | Several chats working at once, each in its own git worktree ("lane"), with a manager chat that grants path ownership, detects deadlocks, and merges finished lanes into an integration branch. Includes an optional design lane that writes feature specs. | A `CLAUDE.md` with planning and verification rules. Recon-Build-Review provides them and is strongly recommended. |

## Applying a preset

Follow [APPLYING.md](APPLYING.md). It is written for an agent; point one at it with something like:

> Create a new repo for a Unity project called "Some Name", then apply the Recon-Build-Review and
> Parallel Agents presets from `C:\Projects\Agentic-Pipeline-Presets`.

Apply Recon-Build-Review first when using both.

## Reference instantiations

Real projects that run these presets. Read them when adapting a preset to a similar stack.

| Project | Stack | Presets | Local path |
|---|---|---|---|
| Chef Knight Desktop Adventures | Unity 6, C# | Both | `C:\Projects\Chef-Knight-Desktop-Adventures` (project in the `Chef Knight Desktop Adventures` subfolder) |
| Agentic Office Simulation | Electron, TypeScript, React | Both | `C:\Projects\AgenticOfficeSimulation` |

## Conventions in this repository

- `{{PLACEHOLDER}}` tokens mark project-specific values. Each preset's README lists every token with
  examples.
- `<!-- ADAPT: ... -->` comments explain how to fill a stack-specific section. They are removed when
  the file is installed.
- An installed file never contains a `{{` token or an `ADAPT` comment.
- Keep presets generic. Knowledge about one project belongs in that project, and at most in the
  reference instantiations table above.
- When a project improves a preset's rules in a way that is not stack-specific, bring the improvement
  back here.
