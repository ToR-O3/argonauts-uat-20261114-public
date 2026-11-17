# Constraints (intel)

Source paths are relative to this worktree. All entries derive from the SPEC, with no ADR override. Scenarios remain authoritative in the source; this staging is not evidence of execution.

## Execution and file reading (modified FR-1)
- source: openspec/changes/r-5c041156-wordfreq-html/specs/wordfreq-cli/spec.md:6-35
- type: api-contract
- content: Exactly one UTF-8 file; missing/unreadable/invalid UTF-8 uses stderr and exit1; invalid file-argument count uses stderr and exit2. Errors emit no result on stdout in every format. Empty files and nonempty whitespace/punctuation-only files succeed with zero results: empty text, JSON [], complete HTML with total0/data rows0.

## Output format contract (modified FR-3)
- source: openspec/changes/r-5c041156-wordfreq-html/specs/wordfreq-cli/spec.md:37-54
- type: api-contract
- content: Accept text/json/html, default text/top10; positive top keeps existing semantics and top exceeding distinct words outputs all. Text remains count TAB word newline; JSON remains word-string/count-integer array. HTML is one complete doctype/html/head/body document on stdout, successful exit0 and empty stderr without logs. No ranks or metadata added to text/json. Unknown format uses stderr/exit2 and empty stdout. Save UTF-8 stdout to a different HTML file.

## First occurrence ordering (modified FR-4/D-2)
- source: openspec/changes/r-5c041156-wordfreq-html/specs/wordfreq-cli/spec.md:56-81
- type: nfr
- content: All formats use count descending, normalized first-occurrence order for ties, then top. Earliest occurrence among casefold-collapsed spellings is retained. This explicitly replaces word ascending, including the retained old scenario title whose expected result is now zoo before apple. Zoo apple zoo APPLE beta and ZOO Straße zoo STRASSE beta select zoo at top1. early late late selects late first. Different hash seeds preserve byte output within each format, not across formats.

## HTML metadata (HTML-1)
- source: openspec/changes/r-5c041156-wordfreq-html/specs/wordfreq-cli/spec.md:85-94
- type: schema
- content: Before the table show non-link basename without directories and the sum of all normalized-token occurrences before top. For Zoo apple zoo APPLE beta at top1 show total5 and rank1/zoo/count2, not total3 or total2. A directory input ending in 資料.txt displays only 資料.txt.

## HTML safety and self-containment (HTML-2)
- source: openspec/changes/r-5c041156-wordfreq-html/specs/wordfreq-cli/spec.md:96-113
- type: nfr
- content: Escape displayed words/names, preserving original DOM text and whitespace including CR/CRLF, without double escaping or input-created elements/script/events. Include formatter-direct special-character/entity-like inputs and malicious actual filenames through CLI. Match UTF-8 saved bytes to charset; preserve Japanese. Inline styles, no JS/external CSS/fonts/images/communication; actual browser network must show zero external requests. Explain saved words/names remain exposed when shared.

## Responsive semantic table (HTML-3)
- source: openspec/changes/r-5c041156-wordfreq-html/specs/wordfreq-cli/spec.md:115-140
- type: nfr
- content: Light background, viewport metadata, semantic table/thead/tbody with rank/word/count scope=col headers. Number selected rows from1 without shared ranks or gaps; do not number the header; zero rows means no rank cells. Validate normal, tied, top1 and empty examples. Actual CSS viewports320/375/1280 must show 200-character words and long Japanese basenames completely with wrapping, no missing/duplicate/truncated text, overlapping columns or horizontal page/table overflow; vertical scrolling allowed. Capture images and DOM/layout measurements. No theme switching.

## Compatibility and verification (HTML-4)
- source: openspec/changes/r-5c041156-wordfreq-html/specs/wordfreq-cli/spec.md:142-155
- type: protocol
- content: Preserve contracts, input boundary and word definition outside HTML addition/tie-order change. Cover all formats with normal/empty/punctuation/top/errors/Unicode/first occurrence and input immutability, direct formatter and CLI tests plus actual browser verification. Keep CI/dependencies unchanged and existing CI tests maintained. Explain different output file and same-path redirection truncation. Quality retains actual HTML, browser/version, viewport, image, DOM/layout/network evidence; unavailable means unverified/human escalation, never invented evidence or added CI/dependencies.
