## Conflict Detection Report

Mode: new (fresh ingest, no existing PROJECT.md/CONTEXT.md to check against). Precedence: ADR > SPEC > PRD > DOC (no per-doc manifest precedence overrides).

Re-run after cycle remediation: the ingest manifest was shrunk via --manifest to 5 documents; openspec/changes/r-5a3b8a3f-wordfreq/design.md (former ADR) was removed from the ingest set and its classification JSON deleted.

### BLOCKERS (0)

Cross-reference graph rebuilt on the reduced set (DFS three-color marking, depth ≤ 2). In-set edges: prd-wordfreq-cli.md -> brief-wordfreq-cli.md (the only cross-ref resolving inside the ingest set). The cross_refs "design.md" (brief, proposal, spec) and "pyproject.toml" (proposal) resolve to paths outside the ingest set and produce no graph edges. No cycles — all 5 documents synthesized. No LOCKED-vs-LOCKED ADR contradiction applies (no ADR-classified source remains in the set; no classification carries locked: true). No UNKNOWN/low-confidence classifications (all 5 are high confidence with manifest overrides). No merge-mode checks apply (no existing CONTEXT.md locked decisions).

### WARNINGS (0)

No competing acceptance variants: the two PRD-classified sources (prd-wordfreq-cli.md, proposal.md) are consistent on options and defaults (`--top` default 10, `--format text|json` default text), exit behavior, component separation, pytest-in-CI, stdlib-only runtime, and packaging-config tolerance for the shared "wordfreq CLI" scope. SPEC content agrees with both PRDs on every overlapping FR (FR-1..FR-8); no SPEC-contradicts-higher-precedence cases exist (no ADR in the set).

### INFO (3)

[INFO] Cycle remediation verified effective
  Note: the previous run reported 3 cycles all through design.md; with design.md removed from the manifest, those references became dangling (no edge) and the graph is acyclic. Downstream consequence: decisions delegated to design.md (text column format per spec FR-3, input-source extension 構成判断 per FR-6, task references D-A/D-C/D-E) are recorded in intel files as "outside the current ingest set" rather than resolved here.

[INFO] Manifest override on the brief (DOC despite PRD signals)
  Note: _bmad-output/initiative-r-5a3b8a3f/brief/brief-wordfreq-cli.md is manifest-overridden to DOC; content signals (WF-01..WF-08 success criteria, D-1..D-3 decisions, scope boundaries) would otherwise classify as PRD. Manifest override treated as authoritative; brief content routed to intel/context.md, its WF items cross-mapped to FR IDs in the PRD mapping note.

[INFO] design.md delegation targets flagged, not fabricated
  Note: spec.md FR-3 defers the exact text column format to design.md and FR-6 defers the input-source extension 構成判断 record to design.md; tasks.md cites design decisions D-A/D-C/D-E. Since design.md is outside the ingest set, these fields are marked as delegated/absent in intel rather than filled from memory.
