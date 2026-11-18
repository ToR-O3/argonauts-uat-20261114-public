# 04-02 execution evidence — t_ff71cb87 / run145

Actor: argonauts-uat-builder. Repository: ToR-O3/argonauts-uat-20261114-public. Worktree cwd: `/home/Yuki/workspace/argonauts-uat-20261116/work/public/.worktrees/t_ff71cb87`. Starting head c65ec8b4f41b92201235b794ca698f3ddeaa88c2; product/test target after implementation 5582f6300a12dae9f25d4ef2c816b7ebec051c53. Later evidence/state commits do not change that product tree. Review handoff supplies the final pushed head.

## Exact execution conventions

All pytest commands below begin with:
`env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest`

Python3.12.15, pytest9.0.3, Linux6.18.58.1-microsoft-standard-WSL2, effective uid1000. CLI subprocesses use `/usr/bin/python3 -m wordfreq`, repo cwd, actual tmp_path files and captured stdout/stderr bytes. Actual test argv construction/independent literal oracles are in the committed `tests/test_cli.py:598–819`. New format cases execute text/json/html. Test `min_count_valid_input_failure[permission-*]` proves actual PermissionError before running CLI as the same user; no skips.

| Suffix / command | Result / exit | Unmodified report |
|---|---|---|
| `tests/test_min_count_verifier.py -k saved_baseline -x` with `WORDFREQ_MIN_COUNT_BASELINE_ROOT=.planning/argonauts/r-e476c11d/baseline` before product edit | first 1 passed/1 failed, exit1 (test path-transport defect); fixed 16 passed/31 deselected exit0 | baseline-gate.txt, baseline-gate-green.txt |
| `tests/test_cli.py -k min_count --collect-only -q` | 39 selected, exit0 | collect-1.2.txt |
| `tests/test_cli.py -k min_count -v --junitxml=.planning/argonauts/t_ff71cb87/red-1.2.xml` | 21 failed/18 passed, exit1 | red-1.2.txt/xml/json |
| `tests/test_cli.py -x` after parser validation | 139 passed, exit0; tracer feedback rerun139 passed exit0 | green-1.2.txt, tracer-feedback.txt |
| `tests/test_cli.py -k 'min_count_selection or min_count_empty_total or min_count_saved_default_bytes' --collect-only -q` | 219 selected, exit0 | collect-1.3-1.4.txt |
| `tests/test_cli.py -k min_count_selection -v --junitxml=.planning/argonauts/t_ff71cb87/red-1.3.xml` | 102 failed/84 passed, exit1 | red-1.3.txt/xml/json |
| `tests/test_cli.py -k min_count_empty_total -v --junitxml=.planning/argonauts/t_ff71cb87/red-1.4.xml` | 9 failed/12 passed, exit1 | red-1.4.txt/xml/json |
| `tests/test_cli.py -k min_count_selection -v` after common filter | 186 passed/172 deselected, exit0 | green-1.3.txt |
| `tests/test_cli.py -k min_count_empty_total -v` after same common filter | 21 passed/337 deselected, exit0 | green-1.4.txt |
| `tests/test_cli.py -x` final | 358 passed, exit0, 13.37s | cli-final.txt |
| `tests/test_aggregator.py -x` | 5 passed, exit0 | aggregator.txt |
| `tests/test_formatters.py -x` | 9 passed, exit0 | formatters.txt |
| full suite (no suffix) | 650 passed, exit0, 42.20s | full-suite.txt |
| saved_baseline selector with same opt-in root after product commit | 16 passed/31 deselected, exit0, 10.68s | baseline-post-product.txt |

`gsd_run check tdd-red-evidence .planning/argonauts/t_ff71cb87/red-<1.2|1.3|1.4>.json --raw` returned RED_EVIDENCE_OK for all three. Outputs are classifier-*.json. 1.2 selected target is explicit min1 exit0 (actual parser exit2). 1.3 selected target is hashseed[text], expected only zoo2/apple2/café2, actual singleton words remain. 1.4 selected target is beta N4 HTML, expected no rows and total7, actual four rows remain. Each is an executed output assertion; no syntax/import/fixture failures authorize product GREEN. Existing invalid-argument tests already GREEN at first run are labelled as such.

Both selection and empty-total groups were committed together at544bba1 BEFORE any filter implementation. One common mapping/Counter filter made both groups GREEN at5582f63. No separate late empty-state implementation or artificial product regression. Beta N2/top1 total7 and empty/whitespace/punctuation total0 were already GREEN (12 items total in1.4); the nine all-excluded cases were the genuine RED.

## Setup failures preserved, not passing evidence

- `baseline-gate.txt`: saved-original validator passed, copy-control test used current worktree as `relative_to` base despite immutable capture paths. Minimal test-only fix7042739 uses recorded index.root. Original index/assets/validator unchanged. Rerun16 success before first product edit.
- `cli-env-setup-failure.txt` / `full-env-setup-failure.txt`: added default-byte replay incorrectly sent null LC_ALL to subprocess env. These are setup failures, NOT product RED. Fixed null→unset mapping in test; final358/650 results above replace failed claims, not raw reports.

## Baseline identity / compatibility

Original capture head789cc17267fb4cfeea24111797c3d934c542ce6a. Index SHA256 d317798933ee5cd20e10363e336ec164bc4272599e14cfd6c89ba84d8816f089. No baseline recapture, rewrite or old-head checkout. `git diff c65ec8b HEAD --exit-code -- .planning/argonauts/r-e476c11d/baseline wordfreq/formatters.py wordfreq/aggregator.py wordfreq/sources.py wordfreq/tokenizer.py .github/ pyproject.toml` exit0. Final test `test_min_count_saved_default_bytes` replays12 original cases, omitted/explicit1 (24 real CLI invocations), with unchanged inputs/basenames and recorded environment; stdout equals pre-change bytes. This is bytes compatibility, NOT browser image comparison.

## Source and ownership handoff

`wordfreq/__main__.py`: parser line17; pre-I/O validation27–28/read30; original counts34 and total35; separate Counter with original items order36–37; existing top_words38; common pairs to HTML44/JSON46/text48; HTML receives original total44. Quality must independently inspect this target-head source and not infer internal order solely from output. Counter/pairs seam asserts nonmutation and object handoff in all3 formats.

`actual-cli.txt` preserves actual target-head/cwd/argv/stdout/exit for README beta N2/top1 JSON and N4 JSON. Tests cover hashseeds0/1/42, N1/2/3/4/10**100, top1/3/10/99/default, option-order reversal, Unicode casefold, empty/all-excluded and literal totals7/5/0. JSON empty is exactly [] plus one LF; text empty is zero bytes; HTML keeps existing columns/metadata/copy/static safety.

No browser execution, image viewing, independent quality approval, CI result, PM original reading, phase completion, archive or merge is claimed. OpenSpec2.1/2.2 remain pending. P6 remains insufficient-spec backstop; no new concurrency/atomic-stdout guarantee. Skill lesson saved-cli-evidence was staged for human approval, not installed.
