# Synthesis Summary

Ingest run for the wordfreq CLI project (MODE: new — fresh ingest, no existing PROJECT.md/CONTEXT.md/ROADMAP.md to merge against).
Precedence applied: ADR > SPEC > PRD > DOC. No classification carried a per-doc `precedence` override, and none carried `locked: true`.

Ingest set: the 5 documents in `intel/classifications/`. design.md was removed from the manifest by the orchestrator to break the cross-reference cycles found in the previous run; it is out of scope for this synthesis and its classification JSON is gone.

## Doc counts by type (all 5 classifications consumed; all high-confidence, all manifest overrides)

- ADR: 0
- SPEC: 1 — openspec/changes/r-5a3b8a3f-wordfreq/specs/wordfreq-cli/spec.md
- PRD: 2 — _bmad-output/initiative-r-5a3b8a3f/prd/prd-wordfreq-cli.md; openspec/changes/r-5a3b8a3f-wordfreq/proposal.md
- DOC: 2 — _bmad-output/initiative-r-5a3b8a3f/brief/brief-wordfreq-cli.md; openspec/changes/r-5a3b8a3f-wordfreq/tasks.md

## Cycle detection result

Directed cross-ref graph over the 5 documents. In-set edges: prd-wordfreq-cli.md -> brief-wordfreq-cli.md (1 edge). All other `cross_refs` values ("design.md" x3, "pyproject.toml") resolve outside the ingest set and produce no edges. Traversal depth 1 (cap 50). No cycles — synthesis performed on all 5 documents.

## Decisions (intel/decisions.md)

- Locked: 0
- Extracted ADR entries: 0 — no ADR-classified source in the set (design.md, the former ADR, is now outside the ingest set)
- PRD-local decisions D-1..D-4 preserved inside their routed requirement/constraint entries rather than dropped (mapping recorded in decisions.md)

## Requirements (intel/requirements.md)

- Extracted: 8 (from both PRDs; shared requirements cite both source paths)
- IDs: REQ-wordfreq-cli-execution, REQ-top-count-option, REQ-output-format-option, REQ-deterministic-ordering, REQ-component-separation, REQ-input-source-boundary, REQ-pytest-ci, REQ-stdlib-only-runtime
- Competing acceptance variants between the two PRDs: 0 detected

## Constraints (intel/constraints.md)

- Extracted: 8
- Type breakdown: api-contract 3 (FR-1 execution/file-read/exit-code contract, FR-2 `--top`, FR-3 `--format`), schema 2 (JSON output shape, tokenizer/normalization definition D-3), nfr 2 (deterministic ordering FR-4/D-2, pytest-in-CI + stdlib-only FR-7/FR-8), protocol 1 (input-fetch boundary + component separation FR-5/FR-6)

## Context topics (intel/context.md)

- Extracted: 7 — Brief problem/solution, Brief success criteria (WF IDs + WF→FR mapping), Brief v1 scope WF-01..WF-08, Brief v1 decisions D-1..D-3, Brief v1 out-of-scope, Brief assumptions A-1..A-5, plus implementation task breakdown from tasks.md

## Conflicts

- 0 blockers, 0 competing-variants, 0 auto-resolved; 3 INFO notes
- Detail: /home/Yuki/workspace/argonauts-uat-20261116/work/public/.worktrees/t_fcdaa629/.planning/INGEST-CONFLICTS.md

## Known gaps for downstream (roadmapper)

Decisions that source documents delegate to design.md are unavailable in this ingest set and are flagged, not invented: the exact `--format text` column layout (spec FR-3), the recorded input-source extension 構成判断 (FR-6), and the design decision IDs cited by tasks.md (D-A, D-C, D-E).

## Intel files (this directory)

- decisions.md (0 entries — no ADR in set)
- requirements.md (8 requirements)
- constraints.md (8 constraints)
- context.md (6 Brief topics + tasks.md breakdown)

STATUS: READY — safe to route
