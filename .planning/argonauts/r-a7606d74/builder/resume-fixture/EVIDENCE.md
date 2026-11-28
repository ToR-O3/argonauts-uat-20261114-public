# Task 3 fixture-only resume evidence

Authorization: PM `t_63b9a2b3`. No new Quick/task; all three original Task names retained. Branch `wt/t_ab9d2c45`, SEQUENTIAL=true; no worktree added.

## Root cause and minimal repair

The existing clean/append-only test reached the verifier's approved digest check and rejected the current min-length product bytes. The cold repository had copied current `wordfreq/__main__.py`, while this historical verifier intentionally accepts only the max-count version. Alternatives checked: verifier/approval drift (excluded by unchanged diff), cold Git/append-only malfunction (excluded by stack reaching digest check).

Changed only `scope_repo`'s source for `wordfreq/__main__.py`, using a bundled original snapshot. All existing asserts and rejection cases remain unchanged. The other fixture inputs retain their original copying behavior. The bundled file removes any runtime dependency on the parent repository's historical Git objects; the cold repo's own local init/commit remains as before.

- Source commit: `31953e1c3f1bd0b5da09484f079f0027976ec737`
- Source path: `wordfreq/__main__.py`
- Git blob: `6c3d7429a0b61b3578db469065c33c2acd08374f`
- Fixture path: `tests/fixtures/max_count_scope/__main__.py`
- Git original SHA-256 and fixture SHA-256 both: `9a5e38d9162d98cd45d5e72a719bc258cd8877a02121d48964b2e9aa9f5e9eba`
- Equality verified with `git show 31953e1c3f1bd0b5da09484f079f0027976ec737:wordfreq/__main__.py | sha256sum` and `sha256sum tests/fixtures/max_count_scope/__main__.py`.
- Exact digest equals the existing approval at `tools/verify_wordfreq_max_count.py:488`; neither verifier nor approval was changed.
- `source-hashes.txt` retains original/head/product/README/verifier/baseline hashes.

## Executed tests, in order

Every invocation used `PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest`, from the specified worktree. Each command also used `--junitxml=.planning/argonauts/r-a7606d74/builder/resume-fixture/<stem>.xml`.

| Stem | Arguments | Measured result |
|---|---|---|
| red | `tests/test_max_count_verifier.py::test_scope_contract_clean_and_append_only -q` | 1 failed, exit1, 0.15s; expected ValueError for unapproved product digest |
| target | `tests/test_max_count_verifier.py::test_scope_contract_clean_and_append_only -q` | 1 passed, exit0, 0.15s |
| max-verifier | `tests/test_max_count_verifier.py -q` | 54 passed, exit0, 7.56s |
| min-length | `tests/test_cli.py -k min_length -q` | 263 passed, 650 deselected, exit0, 8.34s |
| all | `-q` | 1311 passed, exit0, 213.95s |

For every stem, `.stdout` and `.stderr` are unmodified process output, `.exit` records pytest's exit status, and `.xml` is its JUnit report. RED is a call-phase rejection from the existing test, not a fixture setup/collection failure. No tests were skipped or assertions weakened. The previous 1310 passed/1 failed run remains preserved in the original builder logs.

## Commit and scope

Atomic code/fixture commit: `1d3a99abbb7d3166c168e1acf43db3bf52856459` (`test(quick-261128-vh0): isolate historical max-count scope fixture`). Only `tests/test_max_count_verifier.py` and `tests/fixtures/max_count_scope/__main__.py` entered the commit. All seven previous code/TDD commits remain ancestors. Current measured Quick commit count: 8.

The full test suite exercised the exact code tree subsequently committed, with no intervening code change. `final-provenance.txt` records final HEAD/environment/status, no-change scope comparison against `50786d64208241ddb285784a03fc9cae3e9c4147`, unchanged baseline checksum verification and commit metadata. Product/README/verifier/dependencies/CI/STATE/ROADMAP unchanged; no OpenSpec/Kanban/push/PR actions. No baseline capture or regeneration, no prior evidence overwrite.

PLAN/SUMMARY and this new resume evidence are deliberately uncommitted for the parent's step8. Independent quality execution and actual browser verification remain **pending**; these Builder results do not constitute independent acceptance.
