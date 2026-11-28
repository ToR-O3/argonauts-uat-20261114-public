# Builder execution evidence — r-a7606d74

## Scope and identity

- Workspace: `/home/Yuki/workspace/argonauts-uat-v111-20261122/work/v112-b/.worktrees/t_ab9d2c45`
- Branch unchanged: `wt/t_ab9d2c45`; SEQUENTIAL=true for every commit guard.
- Initial HEAD: `6aae84890f8ddbd17e186b9a4732df6dd92d2976`.
- Final tested HEAD: `50786d64208241ddb285784a03fc9cae3e9c4147`.
- `logs/environment.txt` and `logs/final-provenance.txt` retain identity/environment/status. Final product/test/config dirty diff and staged diff are empty. Planning evidence and pre-existing Quick/OpenSpec untracked files remain uncommitted.
- Python substitution: PLAN `python3` was resolved to `/usr/bin/python3` (3.12.15), with `PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages`, pytest 9.0.3. Initial default Python 3.14.9 lacked pytest; the documented existing Python environment was used, without install or dependency changes. Exporting PYTHONPATH also makes pytest visible to the default interpreter, but measured acceptance runs all use `/usr/bin/python3`.
- User uid=1000; permission cases prove actual `PermissionError` under the running user before asserting CLI exit1. Scratch is managed TMPDIR/pytest tmp_path, not system /tmp.

## Command convention

All paths below are repo-relative. For each pytest run, unmodified stdout, stderr, and actual shell status are stored as `logs/<name>.stdout`, `.stderr`, `.exit`. XML reports exist where noted. Commands were executed with `/usr/bin/python3 -m pytest` and the exported PYTHONPATH above.

| Log stem | Actual pytest arguments | Actual result |
|---|---|---|
| baseline-cli | `tests/test_cli.py -q` | 650 passed; exit0 |
| baseline-all | `-q` | 1048 passed; exit0 |
| capture | `tests/test_cli.py -k min_length_baseline_capture -q -s` with `WORDFREQ_CAPTURE_MIN_LENGTH_BASELINE=1` | 1 passed; exit0 |
| tracer-red | `tests/test_cli.py -k min_length_tracer -q --junitxml=.planning/argonauts/r-a7606d74/builder/logs/tracer-red.xml` | 1 failed, 651 deselected; exit1 |
| tracer-green | `tests/test_cli.py -k min_length_tracer -q` | 1 passed; exit0 |
| tracer-regression | `-q` | 1049 passed, 1 failed; exit1 (historical fixed-product scope verifier; see below) |
| task1 | `tests/test_cli.py -k 'min_length_tracer or min_length_saved_default_bytes or min_length_baseline_capture' -q` | 26 passed; exit0 |
| zero-red | `tests/test_cli.py -k min_length_invalid_zero_before_read -q --junitxml=.planning/argonauts/r-a7606d74/builder/logs/zero-red.xml` | 1 failed; exit1 |
| zero-green | `tests/test_cli.py -k min_length_invalid_zero_before_read -q` | 1 passed; exit0 |
| zero-regression | `tests/test_cli.py -q` | 677 passed; exit0 |
| invalid-green | `tests/test_cli.py -k 'min_length_invalid or min_length_parser or min_length_tracer or min_length_saved_default_bytes' -q -s` | 67 passed; exit0 |
| help-red | `tests/test_cli.py -k min_length_help -q --junitxml=.planning/argonauts/r-a7606d74/builder/logs/help-red.xml` | 1 failed; exit1 |
| help-green | `tests/test_cli.py -k min_length_help -q` | 1 passed; exit0 |
| task2 | `tests/test_cli.py -k 'min_length_invalid or min_length_help or min_length_parser or min_length_tracer or min_length_saved_default_bytes' -q` | 68 passed; exit0 |
| help-regression | `tests/test_cli.py -q` | 719 passed; exit0 |
| unicode | `tests/test_cli.py -k min_length_unicode -q` | 15 passed; exit0 |
| composition | `tests/test_cli.py -k min_length_composition -q` | 144 passed; exit0 |
| empty-errors | `tests/test_cli.py -k 'min_length_empty or min_length_valid_input_failure' -q` | 24 passed; exit0 |
| invariants | `tests/test_cli.py -k 'min_length_hashseed or min_length_internal_order or min_length_read_only or min_length_html_safety' -q` | 11 passed; exit0 |
| task3-target | `tests/test_cli.py -k min_length -q --junitxml=.planning/argonauts/r-a7606d74/builder/logs/task3-target.xml` | 263 passed; exit0 |
| task3-cli | `tests/test_cli.py -q --junitxml=.planning/argonauts/r-a7606d74/builder/logs/task3-cli.xml` | 913 passed; exit0 |
| final-target | `tests/test_cli.py -k min_length -q -s --junitxml=.planning/argonauts/r-a7606d74/builder/logs/final-target.xml` | 263 passed, 650 deselected; exit0 |
| final-cli | `tests/test_cli.py -q --junitxml=.planning/argonauts/r-a7606d74/builder/logs/final-cli.xml` | 913 passed; exit0 |
| final-all | `-q --junitxml=.planning/argonauts/r-a7606d74/builder/logs/final-all.xml` | 1310 passed, 1 failed; exit1 |

`logs/help-cli.{stdout,stderr,exit}` is the real `/usr/bin/python3 -m wordfreq --help` result: exit0, stderr empty. The exact help command and final target assertions verify the definition and positive integer/inclusive/default contract without README changes.

## Strict vertical TDD and official classifier

Each new product behavior was implemented only after its own actual target AssertionError, official classifier acceptance, and semantic inspection. Tests for subsequent behavior were not written before the preceding production slice was green.

1. `tests/test_cli.py::test_min_length_tracer`: input `a bb ccc bb`, expected exit0 / `2\tbb\n1\tccc\n`; actual exit2 because `--min-length` was unrecognized. This is a pytest feature-expectation AssertionError, not collection/parser-startup failure. Added only integer/default argument and normalized-key length predicate. Same test green, and the task1 compatibility group green. `tracer-regression` uncovered the fixed historical scope hash conflict, not a tokenization/output failure.
2. `tests/test_cli.py::test_min_length_invalid_zero_before_read`: expected usage exit2 before acquisition; actual exit1 from missing input. Added only `<1` validation before FileSource. Same test green; then expanded already-green argparse rejection to all invalid forms × all three formats, spy calls0, and open stdin without data/EOF. Timeout path always kills/waits. `invalid-green.stdout` and `final-target.stdout` preserve OPEN_STDIN argv/exit/raw bytes; the open pipe assertion is made before closure.
3. `tests/test_cli.py::test_min_length_help`: successful help lacked the positive-integer explanation and failed its meaning assertion. Added only help wording. Same test and cumulative CLI suite green.

For each RED, `logs/{tracer,zero,help}-red.json` stores command, exitCode, unmodified JUnit XML output, targetTest, targetFile, expected, actual, and semanticAssessment. Console stdout/stderr/XML are retained independently. Actual official calls were:

```
source /home/Yuki/workspace/argonauts-uat-v111-20261122/home/.hermes/profiles/argonauts-uat-builder/gsd-core/workflows/_runtime-launcher.snippet.sh
gsd_run check tdd-red-evidence .planning/argonauts/r-a7606d74/builder/logs/tracer-red.json --raw
gsd_run check tdd-red-evidence .planning/argonauts/r-a7606d74/builder/logs/zero-red.json --raw
gsd_run check tdd-red-evidence .planning/argonauts/r-a7606d74/builder/logs/help-red.json --raw
```

All three unchanged responses are in corresponding `.gate` files: RED_EVIDENCE_OK, target_test_failed, tests1/fail1, no report errors. Official `query state.load` and `query agent-skills gsd-executor --skills-only` raw results are retained in logs. No STATE/ROADMAP update was performed.

Unicode/composition/empty/error/order/hashseed/read-only/safety additions were immediately GREEN against the generic implementation and are regression evidence, not falsely claimed additional REDs. No further product change or refactor was needed.

## Fixed baseline and original CLI bytes

`../baseline/input.txt` and `../baseline/index.json` were captured at initial HEAD before any product edit. There are 24 recorded cases: three formats × top omitted/1/2/99 × no frequency range or min2/max2. Input includes one-character tokens, more than ten unique tokens, non-lexical initial-order ties, and Unicode. JSON stores actual argv/cwd/executable/environment/head/product diff and reversible stdout/stderr hex, not formatter-generated expectations. `logs/baseline.sha256` was taken immediately after capture; `logs/scope-check.txt` confirms both files still match. Capture explicitly refuses overwrite and requires unmodified pre-feature product. Normal pytest never regenerates it.

`test_min_length_saved_default_bytes` checks each case twice: omission and explicit1 against unchanged pre-product bytes/exit/stderr. 24 tests cover 48 real compatibility calls.

`final-cli-index.json` maps 262 final-head CLI originals to exact `record_path`, pytest test identity, source input, argv/environment/head, explicit expected pairs and original total when applicable. Each `final-head-raw/<id>/` contains `cli.json`, raw stdout/stderr, input bytes when readable, and `stdout.html` for successful HTML. Permission-denied originals deliberately have no readable input bytes; the test constructs `hello` then proves EACCES and restores permissions in finally. The JSON file's own directory locates all sibling originals; no HTML is edited. Spy-only tests and open-stdin cases are instead tied to the final pytest log/XML and global provenance.

## Requirements index

| Requirement | Builder evidence | Remaining gate |
|---|---|---|
| FR-1 / LEN-1 / SC-1 | tracer, unicode, invalid/parser tests; final target XML; final CLI index/bytes | independent quality pending |
| LEN-2 / SC-4 | zero RED/GREEN; invalid spy calls0 × formats; OPEN_STDIN lines; valid_input_failure actual EACCES | independent quality pending |
| FR-2 / SC-2 | immutable baseline SHA; 24 saved_default_bytes tests covering omission/explicit1 | independent quality pending |
| FR-3 / LEN-3 / SC-3 | composition includes frequency-independent top-before-length discriminator and independently ineligible length/count tokens; empty; internal_order; hashseed0/1/42 | independent quality/browser pending |
| FR-4 / SC-4 | help RED/GREEN; real help stdout and all semantic assertions | independent quality pending |
| FR-5 / LEN-4 / SC-5 | final 263 target and 913 CLI pass; unchanged README snapshot and source/CI/dependency diff | full suite FAIL; independent quality and browser pending |

## Blocking full-suite conflict — not a pass

Final full suite failed `tests/test_max_count_verifier.py::test_scope_contract_clean_and_append_only` at line241. Its fixture at lines216–233 copies the current product into a scratch repo, but `tools/verify_wordfreq_max_count.py:488–492` requires the historical `wordfreq/__main__.py` SHA `9a5e38d9162d98cd45d5e72a719bc258cd8877a02121d48964b2e9aa9f5e9eba`. The authorized min-length product necessarily differs and raises `ValueError: unapproved product/README change: wordfreq/__main__.py`.

Baseline full suite passed, so this is NOT called a pre-existing failing test: it is a pre-existing fixed-snapshot constraint newly triggered by this authorized change. No digest relaxation, fixture rewrite, skip, or out-of-PLAN modification was made. Parent must authorize a focused historical fixture isolation repair (rather than rewriting historical approved scope), then rerun the full suite. FR-5/LEN-4/SC-5 and final acceptance remain pending; 1310 passes do not cancel the failure.

## Browser and independent quality — pending

Only Builder ran these commands. No quality profile was impersonated. Tool discovery returned no browser screenshot/image-view capability; Chromium binary exists, but no rawRange/screenshot/live browser/image-read verification was performed for this feature. HTML structural/static safety assertions and saved raw HTML are NOT a substitute for actual viewing. Do not reuse old dedicated fixed-scope verifiers as min-length acceptance. Quality must generate fresh originals at final accepted head, rerun target/full suite itself, and inspect omission/explicit1, filtered, empty, original totals at 1280×900 and 320×900, DPR1/100% zoom, all images/tiles/raw correspondences. SC-5/independent acceptance is pending.

## Scope and commits

`logs/scope-check.txt` confirms working/staged README diff exit0, initial snapshot README and all non-target source/dependency/CI/STATE/ROADMAP diff exit0, unchanged README object `a491cb6b224d3c072d55072e2d095961e50a174e`, and immutable baseline hashes. `logs/implementation.diff` is the full realized code/test diff. Only tests/test_cli.py and wordfreq/__main__.py are committed. The seven exact commits are in `logs/commits.txt`. No branch change, extra worktree, push, Kanban, README, OpenSpec tasks, ROADMAP, or STATE edit.
