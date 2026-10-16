# Repository Guidelines

## Project Structure & Module Organization

This repository contains a solution-architecture case study for VitaStore, focused on reducing store operating costs and accelerating onboarding. It currently holds assignment materials rather than application source code.

- `docs/context.md`: business context, discovery evidence, constraints, and submission instructions.
- `docs/task1.md`–`docs/task4.md`: requirements and expected deliverables.
- `docs/img.png`: supplied AS-IS architecture illustration.

Create solution directories as deliverables are developed: `Task1/` for the capability map and sourcing matrix, `Task2/` for BPMN onboarding and verification, `Task3/` for AS-IS and target architecture, and `Task4/` for TCO calculations. Keep editable diagram sources and exported images together in the relevant task directory.

## Development & Validation Commands

No build system, application runtime, automated tests, or lint configuration is currently present. Work primarily in Markdown and diagram or spreadsheet tools.

- `git status --short`: inspect staged, unstaged, and untracked changes.
- `git diff -- docs/`: review unstaged changes to assignment materials.
- `git diff --cached`: review staged deliverables before committing.
- `git diff --check`: detect whitespace errors in unstaged changes; use `git diff --cached --check` for staged changes.

Preview Markdown and open exported diagrams before submitting.

## Writing Style & Naming Conventions

Use descriptive Markdown headings, short paragraphs, and tables for comparisons. Preserve the Russian language of the existing assignment materials when writing related explanations. Use relative links for repository assets and descriptive filenames such as `Task3/to-be-architecture.svg`. Preserve the required `Task1`–`Task4` directory capitalization. No formatter or code indentation standard is configured.

## Review Guidelines

Validate each deliverable against its corresponding assignment. Reconcile conflicting discovery evidence explicitly; do not treat the supplied AS-IS diagram as authoritative. Check BPMN participants, hardware integration, offline cash sales, and recovery synchronization. For TCO, verify formulas, units, assumptions, and the three-year, 100-store scope. Keep decisions consistent across all four tasks. No automated coverage threshold exists.

## Commit & Pull Request Guidelines

The repository has no commits yet, so no established commit convention exists. Use concise, imperative messages, for example `docs: add Task1 sourcing matrix`. Keep commits focused on one deliverable. PR descriptions should identify completed tasks, explain key decisions and assumptions, and link relevant artifacts. Include diagram previews when helpful. Submit the PR URL for review as required by `docs/context.md`. Exclude local IDE settings and incidental logs from deliverable commits.
