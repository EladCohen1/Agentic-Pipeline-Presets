---
name: team-setup
description: Prepare the parallel team environment for a work session — check the team worktrees, bring idle worker slots up to date with team/integration, and prepare any team worktree whose environment is not ready. Does not give this chat a role. Use only when the user invokes /team-setup.
---

# Team setup

Gets the team worktrees and their environments ready so the manager and worker chats can start. Read
`.claude/team/PROTOCOL.md` for the layout and "Per-worktree environment". This skill takes **no role**:
after it finishes, this chat is an ordinary chat until the user runs `/team-manager` or `/team-worker`
in it.

The status script is read-only. Run it from anywhere in the repo:

```bash
python "<this skill's folder>/team_status.py"
```

It prints one row per worktree (role, HEAD, branch, content-clean, open lane, environment state)
followed by the same data as one JSON line.

## Rules

- Never change the main checkout's branch or files, and never prepare or run anything there.
- In team worktrees, run only the git steps below, the protocol's **Prepare** action, and its
  **Targeting check**.
- Never touch a slot that is on a `lane/*` branch, holds an open lane in `LANES.md`, or is not
  content-clean. Report it instead.
- Never edit `LANES.md`.

## Steps

1. **Status.** Run the script. If `team/integration`, the integration worktree, or the worker slots are
   missing, tell the user what is missing and offer to create it. Do so only on their yes:
   - `git branch team/integration main` (only if the branch does not exist)
   - `git worktree add "<team root>/integration" team/integration`
   - `git worktree add --detach "<team root>/worker-N" team/integration`
   (team root: `{{TEAM_ROOT}}`).
2. **Refresh idle slots.** For each slot marked `(behind)` that has no open lane and is content-clean:
   `git -C "<slot>" switch --detach team/integration`. This matters because a chat loads its skills
   from its own checkout, so a stale slot would run old team rules. Do this before preparing, so each
   environment is prepared against the current state.
3. **Prepare environments.** Run the script again. For each team worktree (integration and every idle,
   content-clean slot) whose environment is not ready, run the protocol's **Prepare** action in that
   worktree's project folder. Run them one at a time; if one fails, report its error for that
   worktree and continue with the others.
4. **Wait.** If a Prepare action finishes asynchronously (for example an Editor that keeps loading
   after it launches), run the script with `--wait` (default timeout 900 s) using `run_in_background`,
   and tell the user you are waiting. If it times out, a window is most likely showing a dialog; ask
   the user to look, since you cannot dismiss it.
5. **Confirm targeting.** Run the protocol's **Targeting check** in each team worktree.
6. **Check for real changes.** Run the script again. A team worktree that is not content-clean after
   preparing has a real content change (line-ending noise does not count; see the protocol's "Clean
   tree"). Show the user the `git diff` and ask what to do. Do not restore on your own.
7. **Report.** A short table of worktree, HEAD/branch, open lane, environment. Then the next steps that
   are still needed:
   - Manager: a chat in `<team root>\integration` (its project folder) running `/team-manager`, or
     this chat if it is already there.
   - Workers: a chat in `<team root>\worker-N` (its project folder) running `/team-worker`, one per
     slot the user wants to use. Choose the existing folder; do not use the app's own worktree option.
