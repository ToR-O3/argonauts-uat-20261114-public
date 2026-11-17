## Conflict Detection Report

MODE: merge. Precedence: ADR > SPEC > PRD > DOC; all 5 manifest classifications consumed, no numeric precedence overrides. Source references are relative to /home/Yuki/workspace/argonauts-uat-20261116/work/public/.worktrees/t_380a67a1. Only staging intel and this report are written. Explicit approval of the new product behavior is preserved; it does not silently rewrite existing planning or bypass the merge-diff gate.

### BLOCKERS (0)

No UNKNOWN/low-confidence source, cyclic in-set reference, depth-cap breach or locked ADR contradiction. The existing CONTEXT contains binding implementation decisions, including D-10, but neither that block nor D-10 is explicitly marked locked. PROJECT decisions are Pending. The ingest has no ADR and no locked:true source. Do not invent a LOCKED-vs-LOCKED classification. The detected old/new planning inconsistencies are surfaced below, not hidden.

### WARNINGS (2)

[WARNING] Existing ordering requirement and phase decision disagree with the approved replacement
  Found: Incoming SPEC mandates count descending, normalized first occurrence for ties, then top, in text/json/html; the two incoming PRDs agree. This is the explicitly approved replacement, not an unresolved product question or a choice between incoming PRDs.
  Expected: Existing REQUIREMENTS REQ-04, PROJECT REQ-04/D-2, ROADMAP Phase1 success criterion1, and CONTEXT D-10 still require normalized-word ascending ties. Those old requirements cannot remain the acceptance contract for the new behavior; top-boundary selection can change.
  source: openspec/changes/r-5c041156-wordfreq-html/specs/wordfreq-cli/spec.md:56-81; openspec/changes/r-5c041156-wordfreq-html/proposal.md:10; _bmad-output/initiative-r-5c041156/prd/prd-wordfreq-html.md:65,104-106; .planning/PROJECT.md:32,69; .planning/REQUIREMENTS.md:20; .planning/ROADMAP.md:24; .planning/phases/01-wordfreq-cli/01-CONTEXT.md:34
  → Orchestrator must preview and obtain explicit approval for a merge diff replacing the old acceptance in all affected planning records, preserving Phase1 historical completion. Do not ask Q-1..4 again or invent a legacy-order option. No destination write is authorized by this synthesis.

[WARNING] Existing no-UI/two-format completed scope omits the new HTML work
  Found: Incoming requirements add html with light-background rank/word/count table, basename and pre-top total, responsive browser acceptance, and safety evidence.
  Impact: PROJECT and REQUIREMENTS exclude GUI/screens; CONTEXT declares no UI and text/json only; ROADMAP criterion2 lists text/json and STATE declares all phases complete. Reusing that completed scope without an approved merge could omit the HTML requirements and independent browser evidence or falsely imply completion. This is a requested scope expansion, not an instruction to invalidate shipped Phase1 or add CI/dependencies.
  source: openspec/changes/r-5c041156-wordfreq-html/specs/wordfreq-cli/spec.md:37-54,85-155; _bmad-output/initiative-r-5c041156/prd/prd-wordfreq-html.md:60-69,91-100; .planning/PROJECT.md:5,31,40; .planning/REQUIREMENTS.md:16,51; .planning/ROADMAP.md:15,25,54; .planning/STATE.md:3-6,35; .planning/phases/01-wordfreq-cli/01-CONTEXT.md:10,26
  → Stage an explicit new-scope merge diff for approval: distinguish static HTML reporting from server/interactive GUI exclusions; map new HTML/ordering requirements and browser evidence to approved follow-up planning without marking implementation complete. Preserve CI/dependency bans and do not manufacture a phase number in this synthesis.

### INFO (2)

[INFO] Four previously open product answers are settled and consistent
  Found: Incoming SPEC/PRDs/DOC agree on light background, three columns with display-row ranks from1 and no ties, total occurrences before top, and basename without directories.
  Note: These answers remain accepted; no competing acceptance variant exists between the two incoming PRDs. No renewed product question is needed. Shared HTML still exposes words and basename; theme switching and generation timestamps remain excluded.
  source: openspec/changes/r-5c041156-wordfreq-html/specs/wordfreq-cli/spec.md:85-116; openspec/changes/r-5c041156-wordfreq-html/proposal.md:9-13,28-29; _bmad-output/initiative-r-5c041156/prd/prd-wordfreq-html.md:110-119; _bmad-output/initiative-r-5c041156/brief/brief-wordfreq-html.md:77-81,93-96

[INFO] Classification graph is acyclic; no synthesis precedence override is required
  Found: Resolved in-set edges are proposal→brief, proposal→prd, prd→brief, tasks→spec. All remaining cross_refs target documents outside the five-source ingest set; spec and brief have no in-set outgoing edges.
  Note: Three-color DFS: proposal gray→brief gray→black; proposal→prd gray→brief black→prd black→proposal black; tasks gray→spec gray→black→tasks black. Other starts are already black. No gray back edge; longest path2, below cap50. All classifications high confidence, manifest overrides true, precedence null, locked false. No inferred ADR, unresolved source type or fabricated outside-document content. Auto-resolved conflicts0; warning entries above concern existing planning, not competing PRD variants.
  source: .planning/intel/classifications/proposal-7c4686d4.json; .planning/intel/classifications/prd-wordfreq-html-a512fad0.json; .planning/intel/classifications/brief-wordfreq-html-6f3c1983.json; .planning/intel/classifications/tasks-4053909d.json; .planning/intel/classifications/spec-235ec06d.json
