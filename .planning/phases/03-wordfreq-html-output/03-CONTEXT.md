# Phase 3: wordfreq HTML output — Context

## Source and phase boundary

Request r-50053edc / OpenSpec r-50053edc-wordfreq-html. Approval t_13dfdc77 run83 (completed/done), source t_db216d64 run82 at f441a5c7447b5abff2b8290b0d6f0fd0a3ce659c. PRD input: .planning/argonauts/r-50053edc-prd.md. BMAD PRD: _bmad-output/initiative-r-50053edc/prd/prd-wordfreq-html.md.

Initial progress: project/requirements/roadmap/state all existed; Phase 1 passed; current_phase=null. Official merge synthesis stopped on old lexical tie decision. Team E.7 explicitly authorizes adding a new phase for this approved change. gsd phase.add returned 3 / .planning/phases/03-wordfreq-html-output, because a residual Phase 2 directory exists from another request. Do not reuse any Phase 2 plans or artifacts as this request's outputs. Historical Phase 1 records remain unchanged. New REQ-09..14 cover this phase.

<domain>
Extend existing Python CLI output; no server or application framework. All OpenSpec tasks 1.1, 2.1, 2.2, 2.3, 3.1, 3.2, 4.1, 4.2 belong to this single phase.
</domain>

<decisions>
## Locked approved decisions
- D-01: --format html outputs one self-contained static UTF-8 HTML document to stdout. Inline CSS only; no script/external resources or communication attempts.
- D-02: Three columns: rank, word, count. Above table show basename only and total occurrences before top. No directory information anywhere in title/attributes/body.
- D-03: Frequency descending, ties by first normalized occurrence, then top. This intentionally supersedes Phase 1 REQ-04 / PROJECT D-2 / CONTEXT D-10 lexical ties for text/json/html. Approval explicitly covers the compatibility change. Do not restore lexical ties or mutate historical completion evidence.
- D-04: Keep tokenizer, Unicode extraction, casefold, input boundary, top default10 and positive integer/error contracts, text/json structure and empty forms except new tie order.
- D-05: Light background only, no toggle, rank 1-based displayed row sequence (not competition rank).
- D-06: Normal and 320 CSS px widths must show full long words and valid long basename including repeated spaces/newlines/tabs. UI-SPEC fixes actual browser, normal width and wrapping fixture.
- D-07: Preserve raw element/character Range line fragments/clipping ancestor geometry; judge horizontal containment, clipping-ancestor containment, adjacent nonoverlap and actual full screenshot readability. Strict own-element vertical containment is not mandatory; never adjust raw geometry to force pass.
- D-08: Quality independently regenerates actual CLI HTML at target head for empty/normal/top/long/injection; records input originals, exact command, exit/stdout/stderr, expectation, HTML, browser/version/viewport, raw geometry, all image viewing and network attempts including failed attempts/document navigation. Observe from before opening until end; distinguish browser background traffic with grounds. Builder images or blocked network alone do not suffice.
- D-09: No CI change, dependency addition, timestamp, theme switch, interactive UI, server or input source extension.
- D-10: Automated commands run unattended from repo root against real test files available by that task completion; no inline code or outer cd/grep. Each task has concrete fails_when observable with existing/new tests, never a command whose no-op can pass a defect.
- D-11: PLANs stack sequentially on same request branch in numeric order; task verification runs at task completion, phase verification includes all earlier PLANs. Independent PLAN tests must not depend on absent later artifacts. Max 3 tasks per PLAN. Security/nyquist/plan_check/pattern_mapper settings stay enabled.
- D-12: Exact required acceptance examples from PRD: `Zoo apple APPLE zoo banana` top1=>zoo2, top2=>zoo2/apple2; `zoo apple zoo banana apple cherry` top1/2/10 => total6, 1/2/4 rows; `beta beta beta alpha gamma alpha delta` top2=>beta3/alpha2 total7. Later repeated tokens never update first position. Unequal counts remain descending. Empty HTML has basename/total0/headers and zero data rows; text empty stdout, JSON [] plus newline. Formatter tests inject `& < > " '` and tag/event-looking tokens directly; CLI uses valid hostile basename without weakening tokenizer. Read errors including permission/decode=>exit1, invalid top0/negative/noninteger or format/arity=>exit2, stderr and empty stdout. Encoding must match actual saved UTF8. Browser contract adds whitespace, multi-digit rank/count fixtures and both widths, retaining exact raw Range coordinates.

### Claude's Discretion
Local implementation names and test decomposition only, constrained by existing package boundaries and approved design. UI choices fixed by 03-UI-SPEC.md. No additional product decision remains open.
</decisions>

<canonical_refs>
## Canonical References (mandatory reading)
- openspec/changes/r-50053edc-wordfreq-html/proposal.md
- openspec/changes/r-50053edc-wordfreq-html/tasks.md
- openspec/changes/r-50053edc-wordfreq-html/design.md
- openspec/changes/r-50053edc-wordfreq-html/specs/wordfreq-cli/spec.md
- _bmad-output/initiative-r-50053edc/brief/brief-wordfreq-html.md
- _bmad-output/initiative-r-50053edc/prd/prd-wordfreq-html.md
- .planning/argonauts/r-50053edc-learnings.md
- .planning/INGEST-CONFLICTS.md (attached id40; approved conflict handled via new phase, not standard merge)
</canonical_refs>

<deferred>
CI edits, dependency changes, new input sources, theme controls, generation timestamps, servers. Implementation and product browser acceptance are not part of this planning card.
</deferred>
