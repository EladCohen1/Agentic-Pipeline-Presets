"""Report the state of the team worktrees and their environments.

Usage:
    python team_status.py                       # print status once
    python team_status.py --wait                # poll until every team environment is ready (or timeout)
    python team_status.py --wait --timeout 900

Read-only: never changes branches, files, or environments.
"""
import json
import os
import subprocess
import sys
import time

# The project folder inside each worktree, relative to the worktree root ("." when it is the root).
PROJECT_DIR = "."

# How to judge a worktree's environment: "node", "unity", or "none". Add a checker below for other stacks.
ENV_CHECK = "node"

INTEGRATION_BRANCH = "refs/heads/team/integration"


def run(cmd, cwd=None):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, encoding="utf-8", errors="replace")


def norm(path):
    return os.path.normcase(os.path.normpath(path))


# --- Environment checkers -------------------------------------------------------------------------
# Each takes the list of worktree project folders and returns {norm(folder): state}. A state in
# READY_STATES counts as ready for --wait.

READY_STATES = {"installed", "reachable", "n/a"}


def node_env(folders):
    """installed | stale | missing | n/a (no lockfile).

    npm writes node_modules/.package-lock.json on every install, so a lockfile newer than it means
    the worktree's dependencies predate its current lockfile.
    """
    result = {}
    for folder in folders:
        lockfile = os.path.join(folder, "package-lock.json")
        installed = os.path.join(folder, "node_modules", ".package-lock.json")
        if not os.path.exists(lockfile):
            state = "n/a"
        elif not os.path.exists(installed):
            state = "missing"
        else:
            state = "stale" if os.path.getmtime(lockfile) > os.path.getmtime(installed) else "installed"
        result[norm(folder)] = state
    return result


def unity_env(folders):
    """reachable | loading | closed, from the Unity pipeline CLI's instance list."""
    r = run(["unity", "pipeline", "list", "--json"])
    try:
        instances = {norm(i["projectPath"]): i for i in json.loads(r.stdout)["data"]["instances"]}
    except (ValueError, KeyError, TypeError):
        instances = {}
    result = {}
    for folder in folders:
        inst = instances.get(norm(folder))
        if inst and (inst.get("pipelineServer") or {}).get("isReachable"):
            result[norm(folder)] = "reachable"
        elif inst and inst.get("isRunning"):
            result[norm(folder)] = "loading"
        else:
            result[norm(folder)] = "closed"
    return result


def no_env(folders):
    return {norm(folder): "n/a" for folder in folders}


ENV_CHECKERS = {"node": node_env, "unity": unity_env, "none": no_env}

# --------------------------------------------------------------------------------------------------


def worktrees():
    out = run(["git", "worktree", "list", "--porcelain"]).stdout
    items, cur = [], {}
    for line in out.splitlines() + [""]:
        if not line:
            if cur:
                items.append(cur)
            cur = {}
        elif line.startswith("worktree "):
            cur["path"] = os.path.normpath(line[len("worktree "):])
        elif line.startswith("HEAD "):
            cur["head"] = line[5:12]
        elif line.startswith("branch "):
            cur["branch"] = line[len("branch "):]
        elif line == "detached":
            cur["branch"] = None
    main = items[0] if items else None
    integration = next((w for w in items if w.get("branch") == INTEGRATION_BRANCH), None)
    team_root = os.path.dirname(integration["path"]) if integration else None
    slots = []
    if team_root:
        slots = sorted(
            (w for w in items if norm(os.path.dirname(w["path"])) == norm(team_root)
             and os.path.basename(w["path"]).startswith("worker-")),
            key=lambda w: w["path"],
        )
    return main, integration, slots, team_root


def content_clean(path):
    if run(["git", "-C", path, "diff", "--quiet", "HEAD"]).returncode != 0:
        return False
    untracked = run(["git", "-C", path, "ls-files", "--others", "--exclude-standard"]).stdout.strip()
    return not untracked


def open_lane_slots(integration):
    """Map slot name -> lane id for lanes in LANES.md whose status is not closed."""
    if not integration:
        return {}
    board = os.path.join(integration["path"], "LANES.md")
    if not os.path.exists(board):
        return {}
    lines = open(board, encoding="utf-8").read().splitlines()
    result, header, in_lanes = {}, None, False
    for line in lines:
        if line.startswith("## "):
            in_lanes = line.strip() == "## Lanes"
            header = None
            continue
        if not in_lanes or not line.startswith("|") or set(line) <= set("|- "):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if header is None:
            header = [c.lower() for c in cells]
            continue
        row = dict(zip(header, cells))
        if row.get("slot") and row.get("status", "").lower() != "closed":
            result[row["slot"]] = row.get("lane", "?")
    return result


def project_folder(w):
    return os.path.normpath(os.path.join(w["path"], PROJECT_DIR))


def describe(w, envs, role, lanes):
    branch = w.get("branch")
    name = os.path.basename(w["path"])
    return {
        "role": role,
        "name": name,
        "path": w["path"],
        "project": project_folder(w),
        "head": w.get("head"),
        "branch": branch.replace("refs/heads/", "") if branch else "(detached)",
        "content_clean": content_clean(w["path"]) if role != "main" else None,
        "open_lane": lanes.get(name) if role == "slot" else None,
        "env": envs.get(norm(project_folder(w))) if role != "main" else None,
    }


def status():
    main, integration, slots, team_root = worktrees()
    team = ([integration] if integration else []) + slots
    envs = ENV_CHECKERS[ENV_CHECK]([project_folder(w) for w in team])
    lanes = open_lane_slots(integration)
    integration_head = run(["git", "rev-parse", "--short=7", "team/integration"]).stdout.strip() or None
    rows = []
    if main:
        rows.append(describe(main, envs, "main", lanes))
    if integration:
        rows.append(describe(integration, envs, "integration", lanes))
    rows += [describe(s, envs, "slot", lanes) for s in slots]
    for r in rows:
        r["behind_integration"] = (
            r["role"] == "slot" and r["branch"] == "(detached)" and r["head"] != integration_head
        )
    return {"team_root": team_root, "integration_head": integration_head, "env_check": ENV_CHECK,
            "worktrees": rows}


def print_status(s):
    print(f"team root: {s['team_root']}   team/integration: {s['integration_head']}   env: {s['env_check']}")
    print(f"{'role':12} {'name':34} {'head':8} {'branch':22} {'clean':6} {'lane':14} {'env':10}")
    for r in s["worktrees"]:
        clean = "-" if r["content_clean"] is None else ("yes" if r["content_clean"] else "NO")
        branch = r["branch"] + (" (behind)" if r["behind_integration"] else "")
        print(f"{r['role']:12} {r['name']:34} {r['head'] or '-':8} {branch:22} {clean:6} "
              f"{r['open_lane'] or '-':14} {r['env'] or '-':10}")
    print(json.dumps(s))


def main():
    wait = "--wait" in sys.argv
    timeout = 900
    if "--timeout" in sys.argv:
        timeout = int(sys.argv[sys.argv.index("--timeout") + 1])
    start = time.time()
    while True:
        s = status()
        team = [r for r in s["worktrees"] if r["role"] != "main"]
        ready = bool(team) and all(r["env"] in READY_STATES for r in team)
        if not wait or ready or time.time() - start > timeout:
            if wait:
                print(f"waited {int(time.time() - start)}s, {'all ready' if ready else 'TIMEOUT'}")
            print_status(s)
            sys.exit(0 if (ready or not wait) else 1)
        time.sleep(15)


if __name__ == "__main__":
    main()
