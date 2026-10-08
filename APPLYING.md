# Applying a preset

Instructions for an agent installing one or more presets into a target project.

## 1. Understand the target

Before copying anything, establish from the target repository itself, not from assumptions:

- The stack, its versions, and where the source lives.
- The git root, and whether the project lives in a subfolder of it.
- Which tooling exists today: build, type-check or compile, tests, lint. Tooling that has not been
  chosen yet is recorded as not chosen, never invented.
- Any existing `CLAUDE.md`, `.claude/agents/`, `.claude/skills/`, and `.claude/settings.json`. Merge
  with these; never overwrite them.
- A conventions document, if there is one. If there is none, recommend writing one first: the
  pipelines point agents at it as the authority for code.

If the target is a brand-new empty project, most stack-specific sections will be thin. That is
correct. Fill what the evidence supports and record the rest as "not chosen yet" so the next session
knows to extend it.

## 2. Install the files

Each preset has a `template/` folder that mirrors the target repository's root. Copy its contents to
the same relative paths in the target, renaming where the preset's README says to (agent and skill
names take the project's prefix).

Each preset also has a `CLAUDE.section.md`. Do not copy it as a file. Merge its sections into the
target's `CLAUDE.md`, creating that file if it does not exist. Keep the target's existing sections;
where a preset section overlaps an existing one, combine them and tell the user what changed.

## 3. Adapt

- Replace every `{{PLACEHOLDER}}` with a value backed by evidence from the target. The preset's README
  lists each token with Unity and Electron examples.
- Rewrite every `<!-- ADAPT: ... -->` section for the target's stack, then delete the comment.
- Where a section does not apply (no design document, no live runtime to inspect), remove it cleanly
  rather than leaving an empty heading.
- Keep the rules' wording and strictness. Change what is stack-specific; do not soften what is not.
- When a stack makes a rule's original reason disappear (for example, a reviewer ban on running tests
  that existed because a test run once wedged a shared Editor), you may relax it, but say so to the
  user as a deliberate departure.

## 4. Check

- Search the installed files for `{{` and `ADAPT`. Both must return nothing.
- Every path, command, agent name, and skill name the installed files mention exists in the target, or
  is explicitly recorded as not yet created.
- Cross-references agree: `CLAUDE.md` names the same agents that `.claude/agents/` defines, and the
  team protocol names the same subagents and verify skill.
- Run any scripts the preset installs (for example `team_status.py`) once, to confirm they work.

## 5. Report and commit

Tell the user which presets were installed, every deliberate departure from the preset, and what is
deferred until tooling exists (typically the verify skill's commands). Commit only when the user asks.
