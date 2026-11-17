# CI quality handoff — 01-05 / r-5a3b8a3f

## Scope, sources, and current verdict

- Repository: `ToR-O3/argonauts-uat-20261114-public`
- Request branch: `argonauts/r-5a3b8a3f`; base `main`; phase 1; implementation card `t_001775e5`.
- PLAN: [01-05-PLAN.md](../../phases/01-wordfreq-cli/01-05-PLAN.md), especially Independent quality / remote gate.
- Human choice: CPython **3.12**; human workflow commit `5c9d8fa37939fc5d011b0f2469fb3cd074c4b3f2`.
- Human reports only: run **44017344659** (`pull_request`) and **44017344584** (`push`), completed/success, 43 passed, reported for that historical workflow commit. Architect and Builder did **not** independently read these Actions logs. A PR run may test a merge SHA, whose association still needs independent proof.
- Builder Git read-only comparison: historical commit and current `.github/workflows/pytest.yml` agree. Name/job `pytest`, `ubuntu-latest`, checkout@v4, setup-python@v5 / python-version 3.12, push `argonauts/**` and pull_request, contents:read, `python -m pip install pytest`, `python -m pytest`. File presence is not remote execution proof.
- Start snapshot `24391acbad9170e37fbc7cd24eda5f45a3beeb39`; Task 1 commit `6f0c76d`. **Neither is the final review target.** Task 2, SUMMARY, and STATE/ROADMAP commits create later heads. Resolve latest target at the actual review boundary; never reuse an earlier green run for a newer docs head.

**Builder handoff is not CI acceptance. REQ-07 remains Pending, original VERIFICATION remains gaps_found, final remote-success checkbox remains unchecked.** OpenSpec task 3.3's existing check means absence inspection / handoff preparation, not satisfaction of REQ-07; do not change it or invent a task.

## Evidence links (all repository-relative via this file)

- [Reconciled CI-GAP](../../phases/01-wordfreq-cli/01-CI-GAP.md): preserves original CI absence measurement, adds human setup supplied / independent validation pending and Task 1 local output.
- [Reconciled USER-SETUP](../../phases/01-wordfreq-cli/01-USER-SETUP.md): original incomplete checklist retained as history; current human-completed and remote-unverified items separated.
- [Original VERIFICATION](../../phases/01-wordfreq-cli/01-VERIFICATION.md): historical gaps_found at `0cd4673bb75d78e465aa84c8dd31e8ff810a44b8`; not a current workflow absence claim.
- [Original CLI evidence](../t_3dc4a405/cli-evidence.md): correct source path; `.planning/archive-none` is not its location.
- [Human input / fix-1](../r-5a3b8a3f-fix-1.md).
- [Validation contract](../../phases/01-wordfreq-cli/01-VALIDATION.md): draft, not a Nyquist certification.
- [OpenSpec tasks](../../../openspec/changes/r-5a3b8a3f-wordfreq/tasks.md): existing 3.3 check unchanged.
- [Workflow original](../../../.github/workflows/pytest.yml): read-only human-owned input.

## Local regression evidence — not CI proof

Existing environment only, no installs. Before changes: Python 3.14.9 / pytest 9.2.0, `python -m pytest`, 43 passed in 0.99s, exit 0.
Task 1 endpoint: same interpreter/framework, 43 collected, **43 passed in 1.11s**, failed/error/skipped 0, exit 0. Full per-file output in CI-GAP follow-up. Task 2 endpoint (2026-11-17T05:00:54Z, local-only), Python 3.14.9, pytest 9.2.0, pluggy 1.7.0, anyio 4.15.1:

```text
python -m pytest
collected 43 items
tests/test_aggregator.py ....                                            [  9%]
tests/test_cli.py .....................                                  [ 58%]
tests/test_formatters.py ....                                            [ 67%]
tests/test_sources.py .....                                              [ 79%]
tests/test_sources_boundary.py ...                                       [ 86%]
tests/test_tokenizer.py ......                                           [100%]
43 passed in 1.16s
```

Exit 0; failed/error/skipped 0; all 43 existing cases present. All linked repository source files exist; `git diff --check` exit 0. Compared against start snapshot: workflow, code/tests, dependencies, OpenSpec checks, REQ-07 and original VERIFICATION unchanged. Task 2 source/protocol/link review passed independently of pytest; no remote success is asserted. Local Python differs from CI 3.12: it cannot replace CI interpreter or success evidence. These tests validate existing behavior, not the prose or remote state. Builder separately read source labels, SHA/run provenance, historical retention, failure paths and links.

## Independent quality / remote gate — bounded, read-only

1. At its own review boundary, quality reads the latest remote request branch SHA once (for example `git ls-remote origin refs/heads/argonauts/r-5a3b8a3f`) and compares reviewed checkout HEAD and the same-repository OPEN PR head. Record repo, branch, reviewed target SHA and observed remote SHA. Mismatch or unpublished docs HEAD remains unmet; return authorized team/human handling. Do not switch branches, commit or push in same-card review. Builder's ordinary docs fast-forward push is allowed by the lifecycle; workflow changes/pushes containing them are not.
2. Independently run `python --version` and existing `python -m pytest` in reviewed root. Record complete output, interpreter, count and exit code. Nonzero, zero collected, missing/skipped cases, collection/import errors, failures/errors fail the local gate. No environment rebuild or installs. Different local Python is local-only, not CI proof.
3. Use quality's existing Actions read authorization. One run-list lookup for the target SHA, at most one metadata/jobs read and one log read per applicable push/pull_request run; no watch/retry/poll loop. Example list: `gh run list --repo ToR-O3/argonauts-uat-20261114-public --branch argonauts/r-5a3b8a3f --commit TARGET_SHA --limit 20 --json databaseId,headSha,event,status,conclusion,workflowName,url`. TARGET_SHA is the independently resolved value. Select actual returned run IDs, never historical IDs as a fabricated current run.
4. For each applicable returned RUN_ID: `gh run view RUN_ID --repo ToR-O3/argonauts-uat-20261114-public --json headSha,event,status,conclusion,workflowName,jobs,url` and `gh run view RUN_ID --repo ToR-O3/argonauts-uat-20261114-public --log`. Prefer exact latest-head push evidence. If a PR merge execution is used, record tested merge SHA and independently prove association with the current PR head using read-only PR/Git metadata; unproved or mismatched association cannot pass.
5. Required remote proof: target association; workflow path `.github/workflows/pytest.yml`; workflow/job `pytest`; event; run/job URLs and IDs; completed/success job **and pytest step**, not skipped; actual setup CPython **3.12** log; actual `python -m pytest`; **43 collected/passed, failed 0, exit 0**. Overall green or file configuration alone is insufficient. Preserve historical events as human reports unless independently read, still not proof for a later target.
6. Missing/pending/auth denied/log unavailable/failed/skipped/wrong head/wrong Python/zero tests means remote gate **unmet**. Record actual observation and stop without waiting; retain REQ-07 Pending / gaps_found and return official quality gaps or human handling. Never relax REQ-07, alter permissions, modify workflow, dispatch CI, add dependencies/services, or invent success. Any workflow mismatch goes to human, not a Bot repair.
7. Same-card PLAN review checks this handoff and actual latest-head evidence; it does not set `argonauts/quality`, commit or push. Subsequent phase verification owns official Phase 1 re-verification over all 01-01..05 artifacts and independent CI evidence. Only after both gates pass may quality/authorized closeout update REQ-07, USER-SETUP final CI checkbox, and VERIFICATION to the actual verdict. Record `verified_target_sha` distinctly from later evidence-only commit SHA. A new target invalidates reuse for that new target; do not generate an evidence-commit/CI polling cycle.

## Evidence attachment output and non-blocking observations

Original VERIFICATION / CLI evidence attachments were refused by the hook and remain Git-only (source: fix-1/card). Quality must record attachment success (IDs/files) or the exact current inability/refusal reason in its own artifacts; do not bypass hooks. Attach only relevant run metadata/test logs, excluding secrets, credentials and raw PII.

Inherited GIT_* / global Git configuration isolation warning and non-UTF-8 stdout not observed remain non-blocking observations, not mandatory fixes or new scope. No code, tests, dependency declarations, workflows, access settings, or requirement verdicts are changed by this handoff.
