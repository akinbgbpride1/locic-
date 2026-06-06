# Agent Instructions for locic-

## What this repository is

- A Python-based experimental workflow for automated code generation, review, and refinement.
- Main runtime path is in `WorkflowOrchestratorv2.py` / `The Consolidated Pipeline.py`, which:
  - accepts a task description,
  - generates code with `src/tools/code_gen.py`,
  - reviews and refines it with `src/tools/code_reviewer.py` and `src/tools/refinement_engine.py`,
  - writes output to `workshop_dir/main.py`,
  - commits changes via `git`.
- Core utilities live in `src/core/`.

## Important conventions

- Primary language: Python 3.10+ (`str | None` typing is used).
- There is no package manifest (`requirements.txt`, `pyproject.toml`) in this repository.
- Use minimal dependencies and avoid introducing build systems unless necessary.
- The project is currently an experimental prototype rather than a production application.
- The top-level directory contains many orchestration scripts and experiments; prefer `src/` for library logic.

## How to work here

- Focus on cleaning and improving `src/tools/` and `src/core/` first.
- Preserve the workflow pattern:
  - generate code,
  - review/refine code,
  - persist output,
  - optionally commit/merge.
- If adding a new entrypoint or workflow, document its purpose clearly and keep it consistent with the existing branching/merge structure.
- Do not assume tests exist even though `Automated Testing.py` refers to `pytest`.
- Avoid adding untracked package tooling, since the repo currently lacks dependency and CI configuration.

## Entry points

- `WorkflowOrchestratorv2.py`: main CLI runner for the workflow pipeline.
- `The Consolidated Pipeline.py`: another orchestrator variant that shows the intended workflow structure.
- `Automated Testing.py`: helper that runs `pytest` for generated code.

## Useful repo facts for agents

- `src/tools/code_gen.py`: generates stub Python scripts and handles refinement metadata.
- `src/tools/code_reviewer.py`: validates generated code for syntax issues and placeholder text.
- `src/tools/refinement_engine.py`: coordinates review/refinement loops.
- `src/core/workflow.py`: workspace setup, branch name sanitization, command execution, and code writing.

## When to ask for clarification

- If a feature requires dependency management, ask whether a package manifest should be created.
- If a workflow change touches git branch creation/merge behavior, confirm the intended branch policy.
- If tests are required, confirm where they should live and whether `pytest` should be added as a project dependency.
