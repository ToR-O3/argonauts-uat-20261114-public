# Builder execution originals — 08-03

Ownership: Builder only. No independent quality verdict, no OpenSpec3.2 completion, no phase/PM acceptance. Latest adopted decision: 2026-11-28T14:45:42.849521+00:00「提案のまま進めてください（1〜5 すべて提案どおり）。」

## Provenance and commands

Start target: 20aed897c3a4adc8f9f991315bc2f96da19decab. Test-only RED commit: 32ba4b4. Completed product/tests/docs target is resolved in quality-handoff.json after the task01 commit. Baseline is exactly 79d83ba14dd59d289d2ecd3e33c85e8de437972e. No checkout/index switch obtains baseline: tests use git ls-tree/git show object bytes; source roots are separate managed scratch directories. Both processes receive identical absolute input path, sys.executable/argv and environment (PYTHONPATH removed, no user site, no bytecode, seed42, UTF-8 stdout); cwd alone chooses isolated source revision. Reports preserve cwd, argv, controlled environment, input bytes, raw stdout/stderr as repr and hex, exact integer statuses. Temporary roots were cleaned only after capture.

- `uv run --extra dev python -m pytest tests/test_cli.py -q -x -k exclude_docs --junitxml=.planning/argonauts/r-e0a2598f/docs-red.xml`: exit1, 1 target failure/809 deselected, missing explicit no-automatic-dictionary documentation. Unedited JUnit: docs-red.xml; classifier input: docs-red.json. `gsd_run check tdd-red-evidence .planning/argonauts/r-e0a2598f/docs-red.json --raw`: exit0 RED_EVIDENCE_OK, target assertion not import/setup. Minimal README sentence adds non-goals/no new concurrency guarantee, no runtime change.
- `uv run --extra dev python -m pytest tests/test_cli.py -q -x -k 'exclude_baseline or exclude_immutability or exclude_docs' --junitxml=.planning/argonauts/r-e0a2598f/integration-green.xml`: exit0, 74 passed/736 deselected in6.58s, stdout success, stderr empty from pytest (uv separately warns missing requires-python). integration-green.xml is the unchanged runner report. 64 actual Git-source pairs,9 both-input cases,1 complete docs/literal command test. Compatibility was already GREEN; no fictitious feature RED.
- `uv run --extra dev python .planning/argonauts/r-e0a2598f/capture-builder.py`: exit0, stdout `Captured 64 historical pairs, 18 real exclusion cases; 4 mutants assertion-rejected`; stderr existing uv requires-python warning only. baseline-captures.json and cli-captures.json are actual structured byte captures, not invented goldens. baseline-controls.json and baseline-mutant-*.txt preserve four isolated changed-default, lexical-tie, missing-JSON-newline, changed-HTML-template target assertion failures (each exit1), not infrastructure errors.
- `uv run --extra dev python -m pytest -q --junitxml=.planning/argonauts/r-e0a2598f/suite-green.xml`: exit0,1154 passed in188.61s. Full unchanged report suite-green.xml. Retains predecessor1080 cases and adds74. No pre-change suite run by this Builder is claimed; predecessor quality's1080 run is historical separate evidence.

Interpreter selected by uv: CPython3.12.15 /usr/bin/python, pytest9.2.0 (existing dev extra); literal README uses this interpreter with its exact `-m wordfreq input.txt --exclude excluded.txt` argv after replacing the executable token only. README file block contents become real files, expected stdout `2\tzoo\n1\tbanana\n`, exit0/stderr empty; both bytes unchanged. CLI success/failure raw captures include all formats, original HTML total5, invalid line4 and invalid UTF8, plus selection and all-excluded. Sources/FileSource/read order and deterministic permission/OSError evidence remain in predecessor tests and are rerun by full suite, not copied as independent results.

## AC and original ID trace

| AC | Original requirement IDs | Builder evidence (all relative to this directory unless tests path) |
|---|---|---|
| AC1 | REQ-28,FR-1/5,EX-1/4,AD-2/4 | cli-captures.json AC1/selection/all-excluded; retained test_exclude_selection/empty/tracer; full suite |
| AC2 | REQ-29,FR-2/3,EX-2,AD-2 | cli-captures.json AC2; retained grammar cases including U+0130/fullmatch-before-casefold; full suite |
| AC3 | REQ-29/30,FR-2/4,EX-2/3,AD-2/3 | cli-captures.json AC3 line4; retained six invalid-class/read-trace tests; full suite |
| AC4 | REQ-30,FR-4,EX-3,AD-1/3 | cli-captures.json AC4; retained missing/directory/permission/generic/decode/source-cause tests and argv/no-body-read spies; full suite |
| AC5 | REQ-31/32,FR-6/7,EX-5,RULE-4 | docs-red.xml/integration-green.xml; test_exclude_docs_complete_contract_and_literal_example; literal example/help executed |
| AC6 | REQ-32/33,FR-7,RULE-1..4,AD-1..4 | baseline-captures.json64 pairs; baseline-controls.json4 mutants; suite-green.xml1154; both-input9 tests; complete source diff review |

## Scope review and evidence limits

`git diff --name-status 79d83ba14dd59d289d2ecd3e33c85e8de437972e -- wordfreq tests README.md pyproject.toml .github`: only README.md/tests/test_cli.py/wordfreq/__main__.py and new wordfreq/exclusions.py. Source review: CLI retains argv checks first, eager exclusion before body, separate role exit2/1 handlers, original Counter/sum and ordered separate display candidates/common pairs. sources/tokenizer/aggregator/formatters remain unchanged; no dependency/CI/source-expansion/network/input-writing or HTML/CSS appearance edits. No new guarantee of interruption, concurrent snapshots or atomic publication. All old tests retained. New test-source bytecode and uv.lock/egg-info are generated local artifacts, not deliverables.

Images inspected:0; geometry/readability/external communication were not observed. Static source and historical-byte equality are preservation evidence only, not measured browser geometry. Preserve all26 edge identities (21 explicit/5 concurrency backstops),14 UI states,2 descriptor-less prohibitions; handoff gives pending dispositions. Unconfirmed backstops stay human_needed/insufficient_spec; prohibitions stay flagged-unverified. Quality must freshly resolve exact final head, independently execute and deliver readable originals; Builder reports are leads only. Existing BMAD scripts=stale warning inherited, frameworks not updated.
