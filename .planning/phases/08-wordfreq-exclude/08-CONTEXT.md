# Phase 8: wordfreq exclude - Context

**Gathered:** 2026-11-29
**Status:** Ready for planning
**Source:** PRD Express Path (_bmad-output/initiative-r-e0a2598f/prd/prd-wordfreq-exclude.md), approved t_91b92aed head17648fc.

<domain>
## Phase Boundary
Existing local Python CLI gains optional --exclude FILE, explanations and tests. All FR-1..7, RULE-1..4 and AD-1..4 remain binding. Single request; no scope reduction. Historical stale phases and Phase7 debt stay unchanged.
</domain>

<decisions>
## Implementation Decisions (locked)
- D-01 / FR-1 / REQ-28: Optional --exclude FILE removes every specified normalized word's occurrences from ranking only; remaining counts/order and original HTML total unchanged. Unset behavior unchanged.
- D-02 / FR-2 / REQ-29: UTF-8; LF/CRLF/no final newline. Strip both ends, ignore empty/whitespace and # after strip. Validate complete Unicode `\w+` before casefold; accept digits/underscore/non-ASCII valid words. Reject multiple words, punctuation, hyphen, standalone combining mark, inline # note, leading BOM; no token splitting/BOM stripping to accept invalid lines.
- D-03 / FR-3: Existing str.casefold, never lower. Straße/STRASSE both excluded by STRASSE; HELLO/hello by Hello. Validate before casefold (e.g. U+0130 expands afterward); body tokenizer remains unchanged. Exclusion order/duplicates do not alter output.
- D-04 / FR-4 / REQ-30: All exclusion read failures (missing/permissions/directory/invalid UTF-8 and other I/O errors) produce FILE+reason stderr/exit2, empty stdout, no HTML/Traceback. Invalid line reports original 1-based line number including skipped rows. Do not freeze exact whole diagnostic.
- D-05 / FR-4 / AD-3: Existing argparse syntax/top/min-count validation first, exclusion acquisition AND full-line validation second, body acquisition only after success. Invalid-after-valid row must still fail before ANY body read. Both input roles failing yields exclusion diagnosis/exit2. Invalid numeric args read neither file. Valid/absent exclusions preserve existing body error exit1.
- D-06 / FR-5 / AD-4: Shared pairs across text/json/html: exclusion→min-count→frequency descending/stable normalized first-seen ties→top. Excluded words consume no top slots. Original full Counter remains intact; HTML total before all filters, including all-excluded positive total. Empty body total0; text empty/json[] newline/html existing zero-row form. Empty/comment-only/no-match files preserve results.
- D-07 / FR-6 / REQ-31: --help explains purpose/line format and exits0. README executable usage plus UTF-8, trim/comments/newlines, fullmatch invalid examples, casefold, all failures/line diagnostics/exit2, exclusion-first, original HTML total and unset compatibility.
- D-08 / FR-7 / REQ-32: Compare unset stdout BYTES with fixed baseline79d83ba14dd59d289d2ecd3e33c85e8de437972e using identical inputs/argv/environment, not candidate-self expectations. Fixtures include ties in reverse lexical order, Unicode, >10 unique words, empty body. Additional pytest covers every FR-2 invalid/valid boundary, all FR-4 read failures/order, all formats/min-count/top/empty/all-excluded, old body errors, README example and input+exclusion byte immutability; retain full existing suite. Quality independently runs at exact target head and writes VERIFICATION.md/CLI text evidence, commands/exits/expected-vs-actual/AC mapping. If images inspected, text records count/content/result; PM need not inspect images/archives.
- D-09 / RULE-1..4 / REQ-33: Preserve extraction/casefold/Counter first-seen/defaults, source acquisition boundary, pure count_words/top_words/formatters public contracts, existing text/json/static HTML escaping/basename/CSS/appearance. No new dependency/external network/CI/input rewrite/new source/full refactor. CLI alone owns exit codes; pure components have no file I/O.
- D-10 / all FR acceptance examples: Zoo apple APPLE zoo banana minus apple => 2 zoo/1 banana; minus zoo with min-count2/top1 => apple2 and HTML total5. All filtered => original total5, no data rows. Trimmed CRLF blank/comment/apple without final newline excludes only apple, not banana. Fourth original invalid row after blank/comment/valid => line4 and zero body reads. Unset outputs equal baseline across all formats.
- D-11 / governance: Decision2026-11-28T14:45:42.849521+00:00, user「提案のまま進めてください（1〜5 すべて提案どおり）。」 PM t_9da1db1e excludes architecture only from direct synthesis; planner/checker MUST read original architecture. New product uncertainty goes to PM, not guessed.

### Claude's Discretion
Helper names/module layout/set type and test organization within existing boundaries. No product-policy discretion. Thin feature tracer first, TDD before code. Plans max3 tasks, run sequentially on same request branch with predecessors' artifacts available. Independent tasks must also be verifiable without future plans; their real misbehavior must fail the listed command.
</decisions>

<canonical_refs>
## Canonical References
**Downstream agents MUST read these before planning or implementing.**
- `_bmad-output/initiative-r-e0a2598f/prd/prd-wordfreq-exclude.md` — all requirements/acceptance/examples/rules.
- `_bmad-output/initiative-r-e0a2598f/brief/brief-wordfreq-exclude.md` — scope and original criteria.
- `_bmad-output/initiative-r-e0a2598f/architecture/architecture.md` — direct original AD-1..4, not synthesized.
- `_bmad-output/initiative-r-e0a2598f/decision-update.md` — adopted five decisions.
- `_bmad-output/initiative-r-e0a2598f/checks/revision-independent-review.md` — accepted clarifications, no new policy.
- `openspec/changes/r-e0a2598f-wordfreq-exclude/proposal.md`
- `openspec/changes/r-e0a2598f-wordfreq-exclude/specs/wordfreq-cli/spec.md`
- `openspec/changes/r-e0a2598f-wordfreq-exclude/design.md`
- `openspec/changes/r-e0a2598f-wordfreq-exclude/tasks.md` — 1.1 done; 2.1/2.2/3.1/3.2 pending. Retain IDs for plan mapping, no premature checkoff.
- `openspec/specs/wordfreq-cli/spec.md` — existing canonical behavior.
- `.planning/argonauts/r-e0a2598f-learnings.md` — direct useful patterns, historical lexical ties superseded.
</canonical_refs>

<specifics>
Original six acceptance criteria map to REQ-28..33. Preserve complete source examples rather than interpreting this context as a replacement PRD. No fabricated execution evidence. Inputs both read-only. Permission-failure test must be deterministic under root (mock boundary and/or unprivileged subprocess), not chmod-only false success.
</specifics>
<deferred>
## Deferred Ideas
Automatic stopword lists, regex exclusion, stdin '-', multi-file policy, persistent config, morphology, source expansion, service, migration, dependency/CI/appearance changes.
</deferred>
