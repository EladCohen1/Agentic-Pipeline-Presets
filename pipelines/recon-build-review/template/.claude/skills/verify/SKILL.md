---
name: {{AGENT_PREFIX}}-verify
description: Run and verify this {{STACK_NAME}} project — <!-- ADAPT: the verbs this skill covers, e.g. "compile, run tests, read console and build state, inspect runtime state, and run the app" -->. Use whenever work needs verification beyond source inspection.
---

<!-- ADAPT: Write this skill only from commands that exist in the project. Delete any section that has no
real commands yet, and record it in CLAUDE.md as "not chosen yet" instead. Every command below must be
copy-pasteable as written. -->

# Verification loop

## 0. Confirm the environment is ready

<!-- ADAPT: How to tell the toolchain or runtime can be driven, and what to do if it cannot.
Unity: `unity pipeline list`, `unity command editor_status`; wait while "settling"; if no Editor is
reachable, fall back to source-level evidence and say so.
Electron: `node_modules` is installed and not older than the lockfile; otherwise `npm ci`. -->

## 1. Build or compile

<!-- ADAPT: The build/type-check command, how to read its result, and the rule "an error your change caused
is never an acceptable stopping point". Include known traps (async polling, connection errors during
reloads). -->

## 2. Test

<!-- ADAPT: The default verification pass (full suite or narrowest relevant tests, and why), the command,
how to filter while iterating, how to read failures, and anything that must never be done (for example
a synchronous form that times out, or starting runtime checks while tests are queued). -->

**Baseline failures** — known pre-existing failures as of <!-- ADAPT: date -->. Report these separately
from regressions, and update this list when one is fixed:

- <!-- ADAPT: one test name per line, with the known cause, or "none" -->

## 3. Inspect state

<!-- ADAPT: Read-only commands that inspect configuration, authored data, or runtime state, safe to run
freely. Name the most common real defect they catch. -->

## 4. Runtime checks

<!-- ADAPT: How to start the app or enter the runtime, observe it (logs, console, screenshots), and return
it to a stopped state. Include any probe or test-hook helpers the project provides, as one-liners. -->

## Mutating commands

<!-- ADAPT: Commands that change project or runtime state, and their safety rules (preview or dry-run
first, never bypass a safety gate, these belong after the implementation gate). Delete if none. -->

## Reporting

State exactly what ran, what passed, what failed, and what remains unverified. Distinguish source-level
evidence from runtime evidence. For each blocked objective, try at most one fallback, then report the
limitation instead of accumulating diagnostics.
