# Requirements (intel)

MODE: merge. Source paths are repository-relative to /home/Yuki/workspace/argonauts-uat-20261116/work/public/.worktrees/t_380a67a1. Both PRD-classified documents agree on overlapping acceptance; proposal breadth and detailed PRD refinements are not competing variants. These are staged requirements, not additions to destination REQUIREMENTS.md.

## REQ-html-document
- source: _bmad-output/initiative-r-5c041156/prd/prd-wordfreq-html.md#features-and-requirements (FR-1), openspec/changes/r-5c041156-wordfreq-html/proposal.md (What Changes)
- description: Add html to the existing CLI output formats and emit a single complete HTML document to stdout.
- acceptance: Light background; rank/word/count table; display-row ranks start at 1 after top selection, with no tied or skipped ranks. Offline viewing without server, JS or external assets. Successful exit 0. Empty input produces a complete document with zero data rows and no rank cells.
- scope: HTML output, FR-1, SM-1

## REQ-html-metadata
- source: _bmad-output/initiative-r-5c041156/prd/prd-wordfreq-html.md (FR-2, Glossary, SM-1), openspec/changes/r-5c041156-wordfreq-html/proposal.md (What Changes)
- description: Display input basename and total normalized-token occurrences before the HTML table.
- acceptance: No directory portion or clickable input link. Total is computed before top selection, not distinct-word count or displayed-row count sum. Zoo apple zoo APPLE beta has total 5 even at top1, with one zoo row of count 2 and rank 1. Empty or punctuation-only input has total 0 and zero rows.
- scope: HTML metadata, FR-2

## REQ-first-occurrence-order
- source: _bmad-output/initiative-r-5c041156/prd/prd-wordfreq-html.md (FR-3, SM-2, Change boundary), openspec/changes/r-5c041156-wordfreq-html/proposal.md (BREAKING)
- description: Replace normalized-word ascending tie order in every format with normalized-word first occurrence order.
- acceptance: Sort by count descending, then earliest occurrence of the casefold-normalized word, then apply top. Zoo apple zoo APPLE beta gives zoo:2, apple:2, beta:1; top1 selects zoo. ZOO Straße zoo STRASSE beta gives zoo:2, strasse:2, beta:1. Frequency outranks first occurrence. Repeated executions with different PYTHONHASHSEED values are byte-identical within each format. Update old tie-order specifications, tests and CONCEPTS explanations as an explicit compatibility change; do not add a legacy-order option.
- scope: text/json/html ordering and top boundary, FR-3

## REQ-cli-contract-preservation
- source: _bmad-output/initiative-r-5c041156/prd/prd-wordfreq-html.md (FR-4, RULE-1..3, SM-4, Non-goals), openspec/changes/r-5c041156-wordfreq-html/proposal.md (Impact)
- description: Preserve existing CLI behavior except HTML addition and approved tie-order replacement.
- acceptance: Default text/top10; text count TAB word plus newline; JSON word-string/count-integer array, no metadata or ranks in text/json; empty text remains empty and empty JSON remains []. One UTF-8 file; Unicode word-character maximal tokens with casefold; input acquisition and component boundaries remain unit-testable. Input/read/decode failures use stderr/exit1, argument/top/format errors stderr/exit2, failures emit no result to stdout; input remains unchanged. Maintain existing tests and CI execution with stdlib runtime and existing CI Python. No CI or dependency additions/changes, stdin/URL, server, upload, interactive sort, graph, theme switch or generation timestamp.
- scope: compatibility, FR-4, RULE-1..3, SM-4

## REQ-html-safe-self-contained
- source: _bmad-output/initiative-r-5c041156/prd/prd-wordfreq-html.md (RULE-4..5, Review refinements), openspec/changes/r-5c041156-wordfreq-html/proposal.md (What Changes, Impact)
- description: Safely preserve displayed words and input names in self-contained HTML.
- acceptance: Escape at the HTML boundary; special characters and entity-like strings retain exact DOM text without double escaping or injected tags/script/events. Test formatter directly with special-character words and CLI with malicious filenames. Preserve Japanese and consecutive spaces/tab/LF/CR/CRLF; UTF-8 saved bytes agree with charset. No JS, external CSS/font/image or external requests; verify network count 0 in a real browser. Document shared word/name exposure, basename limitations, UTF-8 stdout saving and saving only to a different output file because shell same-path redirection truncates the input before launch.
- scope: HTML safety, encoding, privacy and offline acceptance

## REQ-html-responsive-evidence
- source: _bmad-output/initiative-r-5c041156/prd/prd-wordfreq-html.md (SM-3, RULE-6, Review refinements), openspec/changes/r-5c041156-wordfreq-html/proposal.md (What Changes)
- description: Ensure the three-column light-background table remains readable on mobile and desktop, with actual browser evidence.
- acceptance: Semantic table/thead/tbody, three scope=col headers and associated cells, viewport metadata. Real CSS viewports 320px/375px and 1280px; 200-character unbroken word and long Japanese basename wrap fully without missing/duplicate/truncated content, overlaps or page/table horizontal scrolling. Vertical scrolling is allowed. Preserve actual HTML, screenshots, browser name/version, viewport, DOM/layout and network records. If browser tooling is unavailable, record unverified and escalate to a human; do not add dependencies/CI or fabricate results.
- scope: HTML layout and downstream quality evidence
