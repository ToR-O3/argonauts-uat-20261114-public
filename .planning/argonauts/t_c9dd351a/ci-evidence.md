# CI evidence — phase 3 verification (quality t_c9dd351a)

- Checked head (verification target): `7c704f337df10a4bfd4bb18936266a16b606dd3c` = origin/argonauts/r-50053edc = ToR-O3/argonauts-uat-20261114-public#5 headRefOid (OPEN, draft).
- The report commit that stores this file is a different, later commit (`.planning/` only). It is not the CI target.
- Read once (no polling), with the quality profile's GitHub login:
  - `gh api --paginate "repos/ToR-O3/argonauts-uat-20261114-public/actions/runs?head_sha=7c704f3…"` returned:

| run | workflow | event | status | conclusion | head_sha |
|---|---|---|---|---|---|
| 44154730435 | pytest | pull_request | completed | success | 7c704f337df10a4bfd4bb18936266a16b606dd3c |
| 44154716225 | pytest | push | completed | success | 7c704f337df10a4bfd4bb18936266a16b606dd3c |

  - `gh api --paginate repos/…/actions/runs/<run>/jobs`:

| job | name | status | conclusion | log summary |
|---|---|---|---|---|
| 134292289872 | pytest | completed | success | `361 passed in 9.90s` (ci-job-134292289872.log) |
| 134292238833 | pytest | completed | success | `361 passed in 7.06s` (ci-job-134292238833.log) |

  - `gh api --paginate repos/…/commits/7c704f3…/statuses`: empty (no commit statuses; `argonauts/quality` is not set at phase verification).
- Workflow files: `git diff --name-only origin/main...HEAD -- .github` is empty — no CI/workflow change in this request.
- Local results (separate from CI, not a substitute): full pytest 361 passed, junit failures/errors/skipped 0 (suite.xml); PYTHONHASHSEED=12345 rerun 361 passed (per-file.txt).
