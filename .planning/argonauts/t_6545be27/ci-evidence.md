# Independent CI evidence — phase 1 re-verification (quality t_6545be27)

Read by quality on 2026-11-17 with its own `gh` login (Actions read). One run list, one metadata read and one log read per run. No waiting, polling, dispatch, workflow edit or permission change.

## Target

| Item | Value |
|---|---|
| Repository | ToR-O3/argonauts-uat-20261114-public |
| Branch | argonauts/r-5a3b8a3f |
| verified_target_sha | `30d9c175fd87a0d492ef6c1532271f55482c45b8` |
| `git ls-remote origin refs/heads/argonauts/r-5a3b8a3f` | `30d9c175fd87a0d492ef6c1532271f55482c45b8` |
| PR #2 (`gh pr view`) | OPEN, draft, same repo, headRefOid `30d9c175…`, baseRefOid `792e9c4c4457a6f455b8b9f169e846c659a13b56` |
| Checked-out worktree HEAD | `30d9c175fd87a0d492ef6c1532271f55482c45b8` |
| Workflow file vs human commit 5c9d8fa | `git diff 5c9d8fa HEAD -- .github` empty |

## Push run (exact target head)

| Field | Value |
|---|---|
| Run | 44021335880 — https://github.com/ToR-O3/argonauts-uat-20261114-public/actions/runs/44021335880 |
| Workflow | name `pytest`, path `.github/workflows/pytest.yml` (REST `path`) |
| Event / branch | `push` / `argonauts/r-5a3b8a3f` |
| head_sha | `30d9c175fd87a0d492ef6c1532271f55482c45b8` |
| Status / conclusion | completed / success |
| Job | `pytest` 133831272938 — https://github.com/ToR-O3/argonauts-uat-20261114-public/actions/runs/44021335880/job/133831272938 — completed/success |
| Steps | checkout, setup-python, `python -m pip install pytest`, `python -m pytest` — all success (none skipped) |
| Checkout log | `git log -1 --format=%H` → `30d9c175fd87a0d492ef6c1532271f55482c45b8` |
| Setup log | `python-version: 3.12` → `Successfully set up CPython (3.12.16)` |

pytest step log (excerpt, timestamps removed):

```text
python -m pytest
shell: /usr/bin/bash -e {0}
platform linux -- Python 3.12.16, pytest-9.2.0, pluggy-1.7.0
configfile: pyproject.toml
collected 43 items
tests/test_aggregator.py ....                                            [  9%]
tests/test_cli.py .....................                                  [ 58%]
tests/test_formatters.py ....                                            [ 67%]
tests/test_sources.py .....                                              [ 79%]
tests/test_sources_boundary.py ...                                       [ 86%]
tests/test_tokenizer.py ......                                           [100%]
============================== 43 passed in 0.83s ==============================
```

Exit 0: the step runs under `bash -e` and its conclusion is success; failed 0, skipped 0, 43/43.

## Pull-request run (merge execution, association proven)

| Field | Value |
|---|---|
| Run | 44021344458 — https://github.com/ToR-O3/argonauts-uat-20261114-public/actions/runs/44021344458 |
| Event | `pull_request` (PR #2; REST `pull_requests[0].head.sha` = `30d9c175…`, base `792e9c4…`) |
| Job | `pytest` 133831300907 — …/runs/44021344458/job/133831300907 — completed/success, all steps success |
| Tested SHA | merge `150576c0abbea627300374a9a34b5710cca1ba8a` (log: `HEAD is now at 150576c Merge 30d9c17… into 792e9c4…`) |
| Association | commit API: parents `[792e9c4… (main), 30d9c175… (target)]`; merge tree `09e39828…` = target tree `09e39828…` |
| Python / tests | CPython 3.12.16; `collected 43 items`; `43 passed in 0.57s` |

## Historical runs (not used as proof)

44017344659 / 44017344584 (head 5c9d8fa) and 44020249396 / 44020243469 (head 24391ac) are earlier heads; they are listed by `gh run list` as success but do not prove the target head.

## Local run (separate, local-only evidence)

`python -m pytest -p no:cacheprovider` at the same HEAD: Python 3.14.9, pytest 9.2.0, 43 collected, 43 passed, exit 0. This does not replace the CI Python 3.12 proof above.

## Verdict

Remote gate for REQ-07 **met** at `30d9c175fd87a0d492ef6c1532271f55482c45b8`. Any later evidence-only commit by quality changes `.planning/` only; it is a different SHA and is not claimed as CI-verified here.
