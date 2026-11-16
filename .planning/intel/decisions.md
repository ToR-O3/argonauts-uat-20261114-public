# Decisions (intel)

No entries — the ingest set contains no ADR-classified documents. (Cycle remediation applied via --manifest: the former ADR source `openspec/changes/r-5a3b8a3f-wordfreq/design.md` was removed from the ingest set and its classification JSON deleted; its D-A..D-F design decisions are outside this ingest and are not extracted here.)

- locked decisions: 0
- proposed decisions: 0
- PRD-local decisions D-1..D-4 (_bmad-output/initiative-r-5a3b8a3f/prd/prd-wordfreq-cli.md "## Decisions") are preserved inside their routed entries, not lost:
  - D-1 (Japanese/non-whitespace-delimited languages out of v1; swappable tokenizer) → REQ-component-separation scope + constraint "単語の切り出しと正規化（D-3）" + Brief Scope notes in context.md
  - D-2 (count desc, tie by normalized word asc) → REQ-deterministic-ordering acceptance
  - D-3 (Unicode \w maximal runs + str.casefold()) → constraint "単語の切り出しと正規化（D-3）"
  - D-4 (exit codes 0 success / 2 usage error / 1 environment error) → REQ-wordfreq-cli-execution, REQ-top-count-option, REQ-output-format-option acceptance
