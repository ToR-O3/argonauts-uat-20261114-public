# Phase 8: wordfreq HTML displayed types — Context

## Source
- Request r-6ae2cbf2; approval t_e811c751 completed run164; specification t_61eb0c74 completed run163, head c59a5cc801c472c1f695682c3ed0b51708022534.
- PRD input: .planning/argonauts/r-6ae2cbf2-prd.md (approved proposal → all specs → tasks).
- Approved BMAD: _bmad-output/initiative-r-6ae2cbf2/brief/brief-wordfreq-displayed-types.md and prd/prd-wordfreq-displayed-types.md.
- Requirements: REQ-29, REQ-30, REQ-31. Full flow. No open questions.

<domain>
Add displayed word type count to existing static HTML CLI output; no new application or interaction.
</domain>

<decisions>
## Locked Decisions
- D-01: HTML table metadata shows `表示 N 種類` next to existing total occurrences. N is len(final pairs), after existing Unicode extraction/casefold, min/max filtering and top. Empty/no-token/all-excluded => 0; original total occurrences remains sum(original counts).
- D-02: Preserve text/json bytes, formatter API, basename-only path handling, initial-occurrence ties, escapes, no scripts/external resources/network, current light palette and table. No dependency, CI, permissions, external sending, migrations or unrelated refactoring.
- D-03: Approved HTML compatibility exception is only displayed-N addition and minimum layout adjustment. Old Phase4 D-06/D-07 and Phase7 D-04/REQ-26 are historic snapshots; do not overwrite those CONTEXT files, sealed baselines, or their past evidence. For current assertions use separate expected output or explicit narrowly-scoped transformation; never blanket ignore HTML. Text/json and security checks stay strict. Past snapshot-only scope gates are not current product acceptance gates.
- D-04: Ingest BLOCKERS 2 in .planning/INGEST-CONFLICTS.md are approved changes, not unresolved product decisions. E.7/F.3 therefore selects official phase.add new Phase8, not merge overwrite or reopening completed phases. Attach conflict report for PM review. Historical stale verification remains separate.
- D-05: Test first RED then production minimum GREEN, expand edge regression, run all pytest. Include ordinary, explicit/large/default top (12 candidates => 10), min/max intersections, empty/no-token/all-excluded, Unicode aggregation and exact text/json regressions. README HTML description gains exactly one relevant line, existing unrelated content retained.
- D-06: Independently quality-run CLI, full pytest and real browser at 1280×900 and 320×900 DPR1, verify adjacent count above table, long words/basename readable without overlap/clipping/overflow, escape and no network attempts. The old request's image exemption does not apply. Quality records actual image count/content/results in plain VERIFICATION.md and CLI/CI evidence, attaches plain originals for PM read_file; PM need not open images or archives. Unperformed/pending checks must not be claimed passed.

## Claude's Discretion
Use existing metadata typography, separators and spacing; only minimum local layout change if actual render requires it. Test helper naming and separate current expected fixtures follow repository conventions.
</decisions>

<canonical_refs>
- openspec/changes/r-6ae2cbf2-html-displayed-types/proposal.md
- openspec/changes/r-6ae2cbf2-html-displayed-types/specs/wordfreq-cli/spec.md
- openspec/changes/r-6ae2cbf2-html-displayed-types/tasks.md
- openspec/changes/r-6ae2cbf2-html-displayed-types/design.md
- .planning/argonauts/r-6ae2cbf2-prd.md
- .planning/argonauts/r-6ae2cbf2-learnings.md
- .planning/INGEST-CONFLICTS.md
</canonical_refs>

<specifics>
Preserve original totals for beta4/zoo3/apple2/pear2/single1 => 12; min2/max3/top1 displays one type. Single logical metadata row with total and count at both widths; long basename may wrap separately without hiding text. OpenSpec tasks1.1 tests,1.2 implementation/README,2.1 independent acceptance need explicit PLAN mapping. Plans execute serially on the same request branch.
</specifics>

<deferred>
No future features. No global repair of prior phase metrics or snapshot gates.
</deferred>
