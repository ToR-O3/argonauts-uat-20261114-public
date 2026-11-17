# CI evidence read by quality (t_9de84d5f)

- Target head checked: `995011cd3b77d4d87a6be3bdf5780bf5cbe3b95c` (PR head of ToR-O3/argonauts-uat-20261114-public#5). This file is committed in a later report-only commit; that commit SHA is not the checked target.
- Read once, not waited: `gh api "repos/ToR-O3/argonauts-uat-20261114-public/actions/runs?head_sha=995011c…"`, then `actions/runs/<id>`, `actions/runs/<id>/jobs`, `actions/jobs/134166757414/logs`.

| Run | Event | Job | Conclusion |
|---|---|---|---|
| 44119531438 | pull_request | pytest (134166757414) | failure |
| 44119518087 | push | pytest (134166709300) | failure |

Job 134166757414 steps: checkout ok, setup-python ok, `pip install pytest` ok, `python -m pytest` failure. Log summary: `5 failed, 279 passed in 5.34s`:

- `tests/test_cli.py::test_html_preserves_basename_in_filesystem_encoding` — AssertionError: Required locale en_GB.iso885915 is not installed
- `tests/test_cli.py::test_html_bytes_are_utf8_independent_of_stdout_encoding[en_GB.iso885915-None]` — charmap `ANSI_X3.4-1968` ≠ `ISO-8859-15`
- `tests/test_html_verifier.py::test_scope_has_exact_baseline_target_and_approved_product_snapshot` — `git diff --name-only -z 5a7659b… 2bd6359…` exit 128
- `tests/test_html_verifier.py::test_builtin_contract_and_scope_commands_need_no_browser_or_role` — traceback from the same git diff
- `tests/test_html_verifier.py::test_scope_rejects_dirty_and_untracked_code` — same exit 128

Locally at the same head (locale installed, full history) the suite is 284 passed. CI changes are out of scope for this request, so the fix belongs in tests/tools (Builder), not in the workflow.
