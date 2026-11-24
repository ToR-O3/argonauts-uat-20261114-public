# Independent quality CLI evidence — r-774f3cd6 / Phase 6

This is the **independent quality** original (not Builder evidence). Actor: `argonauts-uat-quality` (Kanban card t_81c896f6, run 44, phase verification). Builder records were not copied as measurements; every hash below was recomputed by this actor.

## 1. Subjects (distinguished)

| Subject | Value |
|---|---|
| Repository / origin | ToR-O3/argonauts-uat-20261114-public (`https://github.com/ToR-O3/argonauts-uat-20261114-public.git`) |
| Base / request branch | v112-b / argonauts/r-774f3cd6 |
| Fixed baseline | b34cba0d008923e7f5267ce52d5403492ea53925 |
| Approved spec head / plan head | 56b70bdca4349c6d2f9eaeb62be2e340a3e04b49 / 78d9a15d7a9cad739ed44809bfcbaf0dbc746041 (both ancestors of HEAD: exit 0) |
| **Immutable product commit (verified target)** | e1f2c3a2e5d36963cfd789997edb6fa2d62b22ed (ancestor of HEAD: exit 0) |
| Product blob Git OID (not SHA-256) | eeff26ea895b3b8d994efe65ac6f926e8b212e35 (`git rev-parse e1f2c3a…:pyproject.toml`) |
| Quality start HEAD = `start_sha` | 0d79ee4bafb25314ed8bef97bae458271926dbb6 (= `refs/remotes/origin/argonauts/r-774f3cd6` after `git fetch origin` = PR #15 headRefOid; PR OPEN, draft, same repo) |
| Quality end HEAD (before quality report commit) | 0d79ee4bafb25314ed8bef97bae458271926dbb6 (verifier head_start = head_end) |
| Quality report head | the quality commit that adds this file (child of 0d79ee4, trailer `Argonauts-Quality-Start: 0d79ee4…`). A file cannot contain its own commit SHA; the pushed SHA is in the card completion metadata/summary. |
| Quality root (frozen for the run) | /home/Yuki/workspace/argonauts-uat-v111-20261122/work/v112-b/.worktrees/t_81c896f6 (= `$HERMES_KANBAN_WORKSPACE` = `pwd -P` = `git rev-parse --show-toplevel`), local branch `wt/t_81c896f6` |
| Interpreter | python3 3.14.9 (Hermes venv `…/venv/bin/python3`), stdlib only, no install |

## 2. Independently computed hashes (this actor, 2026-11-24T15:10Z)

| Byte subject | Command | SHA-256 | Matches |
|---|---|---|---|
| Baseline blob b34cba0:pyproject.toml | `git show b34cba0…:pyproject.toml \| sha256sum` | 4d50135c1a75196db52ac67e8bd3f0aa3859491249db118f2fa5bccdbff82457 | verifier baseline_blob_sha256 ✓ |
| Product blob e1f2c3a:pyproject.toml (binary Git stdout) | `git show e1f2c3a…:pyproject.toml \| sha256sum` | 540df8d5bf689fd037f73e336faa5ea05aa809699635472f47dd414dc3afb7e0 | verifier candidate_blob_sha256 ✓, actual_input_sha256 ✓ |
| Working file pyproject.toml | `sha256sum pyproject.toml` | 540df8d5bf689fd037f73e336faa5ea05aa809699635472f47dd414dc3afb7e0 | ✓ |
| Verifier | `sha256sum …/verify_description.py` | dab59500fcfc953dd3d745e6181ee66ace8ed436edcbe1eec00709ee6abe4152 | verifier_sha256 ✓, product-target.json ✓ |
| Self-test | `sha256sum …/test_verify_description.py` | 8351bc8670f4317226140fc70b5ea3a7f9af911833be2fbc9ff7a76fc926c476 | selftest_sha256 ✓ |
| Exact-purpose registry | `sha256sum …/process-paths.json` | c78c12efb21bab727241df5ece1a91062f92a711b8ee543946b9dd62aebd1ffa | process_paths_sha256 ✓ |
| 06-02-PLAN.md | `sha256sum` | 6c6bf931f6f3268456fc652210cb850dcf7caa271e6b1964c5ab0d8bae35b5c6 | fixed value in review ✓ |

## 3. Mandatory commands (run from quality root, no wrapper)

| # | argv | Start/End (UTC) | OS exit | stdout | stderr |
|---|---|---|---|---|---|
| 1 | `python3 -B .planning/argonauts/r-774f3cd6/test_verify_description.py -v` | 15:11:06Z / 15:11:09Z | 0 | 0 bytes | 2211 bytes, `Ran 18 tests in 3.143s` / `OK` (sha256 d07763ce…9c59) |
| 2 | `python3 -B .planning/argonauts/r-774f3cd6/verify_description.py repository --baseline b34cba0d008923e7f5267ce52d5403492ea53925 --target-record .planning/argonauts/r-774f3cd6/product-target.json --process-paths .planning/argonauts/r-774f3cd6/process-paths.json --actor quality` | 15:11:09Z / 15:11:10Z | 0 | JSON 6,591,198 bytes (sha256 63a3aa59…cfb2): `exit_code 0`, `error null`, `failures []`, `actor "quality"`, `mode "repository"` | 0 bytes |
| 3 (supplementary, post-edit content) | `python3 -B .planning/argonauts/r-774f3cd6/verify_description.py content --baseline b34cba0d008923e7f5267ce52d5403492ea53925 --candidate pyproject.toml` | 15:13:15Z / 15:13:15Z | 0 | JSON (sha256 2fe0f3dd…293f): 11 conditions PASS incl. BASELINE_DESCRIPTION_ABSENT, VALUE_EXACT, STRUCTURE_UNCHANGED, BYTES_UNCHANGED | 0 bytes |
| 4 (product existing tests) | `uv run --offline --no-project --with pytest python -B -m pytest -q -p no:cacheprovider tests` | 15:13:20Z / ~15:16:30Z | 0 | `702 passed in 189.52s` | merged into stdout |

Not rerun (per runbook/PLAN): missing-description-only `preflight` / `expect-red` (their original RED is Builder evidence at fe96d50:builder-cli.md; self-test `test_cli_preflight_expect_red_and_fixed_repository` covers them in TMPDIR fixtures).

Self-test cases (all `ok`): baseline parse/limit errors, candidate parse error, content negative conditions, correct single line, CRLF, non-table project, all Git scopes reject unknown paths, CLI preflight/expect-red/fixed repository, CLI exit2 bad args, git failure/timeout/HEAD drift, ignored inventory, other product index/worktree cancellation, other product worktree change, registry exact path, fixed blob tracer, tree add/delete/rename/mode, unmerged index, working product hash/mode.

Side effect note: command 4 created ignored `wordfreq/__pycache__/` (6 `.pyc`, all newer than this run start). This actor removed exactly those 6 files and the empty dir (no recursive delete) before any further gate; `git status --porcelain --ignored` was then empty.

## 4. Repository conditions (command 2) — 25 rows, all PASS

| Condition | Result | Detail |
|---|---|---|
| BASELINE_FETCH | PASS | baseline bytes supplied |
| BASELINE_PARSE | PASS | whole TOML parsed |
| CANDIDATE_READ | PASS | candidate bytes supplied |
| CANDIDATE_PARSE | PASS | whole TOML parsed |
| VALUE_EXACT | PASS | fixed string plus one exact line immediately after project.version |
| STRUCTURE_UNCHANGED | PASS | only project.description removed from deep copy |
| BYTES_UNCHANGED | PASS | only allowed line removed; no whitespace normalization |
| PROCESS_PATHS_VALID | PASS | exact paths, declared purposes/scopes/statuses, regular files only |
| TREE_SCOPE | PASS | rejected [], examined 75 |
| INDEX_SCOPE | PASS | rejected [], examined 7 |
| WORKTREE_SCOPE | PASS | rejected [], examined 0 |
| UNTRACKED_SCOPE | PASS | rejected [], examined 0 |
| IGNORED_INVENTORY | PASS | rejected [], examined 0 |
| PRODUCT_COMMIT_FIXED | PASS | full immutable product commit |
| BLOB_INPUT_SHA256 | PASS | working bytes equal the exact blob bytes passed to verify_content |
| MODE_UNCHANGED | PASS | regular non-executable product mode unchanged |
| PATCH_ONE_LINE | PASS | patch below |
| TOOL_HASHES | PASS | tool bytes hashed directly |
| HEAD_STABLE | PASS | HEAD observed before and after collection |
| REPO_IDENTITY | PASS | origin as above |
| REQUEST_BRANCH | PASS | remote_ref 0d79ee4…, local_branch wt/t_81c896f6 |
| PRODUCT_COMMIT_FIXED | PASS | all target provenance fields plus immutable blob/ancestor |
| BLOB_INPUT_SHA256 | PASS | record hashes independently compared with retrieved blob inputs |
| TOOL_HASHES | PASS | record tool hashes compared with actual files |
| HEAD_STABLE | PASS | HEAD observed before and after CLI |

Product patch (baseline → product commit), exactly +1/-0, mode 100644 unchanged, `" (UAT)"` occurs once:

    diff --git a/pyproject.toml b/pyproject.toml
    index d96f26d..eeff26e 100644
    --- a/pyproject.toml
    +++ b/pyproject.toml
    @@ -5,6 +5,7 @@ build-backend = "setuptools.build_meta"
     [project]
     name = "wordfreq"
     version = "0.1.0"
    +description = "argonauts-uat public (UAT)"
     dependencies = []
     
     [project.optional-dependencies]

Independent Git cross-check: `git diff --name-status --no-renames b34cba0 HEAD -- . ':(exclude).planning' ':(exclude)openspec' ':(exclude)_bmad-output'` → only `M pyproject.toml`. No `.github/workflows`, tests, lock or dependency file changed.

## 5. Full exact-path inventory

### 5a. Tree: baseline b34cba0 → product commit e1f2c3a (75 entries; status, mode, new blob, registered purpose)

| Path | St | Mode | New blob | Purpose |
|---|---|---|---|---|
| .planning/INGEST-CONFLICTS.md | M | 100644→100644 | 715298d4da2d | approved requirement ingestion conflict report |
| .planning/REQUIREMENTS.md | M | 100644→100644 | b239af4c6a98 | REQ-23 ingestion and completion tracking |
| .planning/ROADMAP.md | M | 100644→100644 | 09230d1d779f | Phase6 plan execution progress |
| .planning/STATE.md | M | 100644→100644 | d6aba598f923 | official sequential execution current position |
| .planning/argonauts/r-774f3cd6-learnings.md | A | 000000→100644 | fbb3be5bbdb4 | planning learning references |
| .planning/argonauts/r-774f3cd6-manifest.yaml | A | 000000→100644 | 358f0ad00d8c | approved six-document ingestion manifest |
| .planning/argonauts/r-774f3cd6-prd.md | A | 000000→100644 | 6a33fd648293 | approved proposal/spec/tasks ingestion source |
| .planning/argonauts/r-774f3cd6/builder-cli.md | A | 000000→100644 | 7b06b2bcb6b8 | Builder actual stdout/stderr/exit and approval evidence |
| .planning/argonauts/r-774f3cd6/inputs.json | A | 000000→100644 | d988432ca088 | human-reviewed approval and baseline observation binding |
| .planning/argonauts/r-774f3cd6/process-paths.json | A | 000000→100644 | 047622a394b8 | this exact-path purpose and scope registry |
| .planning/argonauts/r-774f3cd6/test_verify_description.py | A | 000000→100644 | 9cf3b9362bf3 | stdlib isolated acceptance verifier self-tests |
| .planning/argonauts/r-774f3cd6/verify_description.py | A | 000000→100644 | 053e6520f610 | read-only four-mode metadata and Git verifier |
| .planning/argonauts/t_26854470-PLAN-CHECK.md | A | 000000→100644 | ae9176957fed | independent planning checker result |
| .planning/argonauts/t_26854470-api-coverage.json | A | 000000→100644 | c4fdd48cc4b2 | official planning API coverage probe |
| .planning/argonauts/t_26854470-command-paths.json | A | 000000→100644 | 437ae0173183 | official verify-command-paths output |
| .planning/argonauts/t_26854470-command-paths.stderr | A | 000000→100644 | e69de29bb2d1 | verify-command-paths stderr original |
| .planning/argonauts/t_26854470-decision-coverage.json | A | 000000→100644 | 78ae80841379 | D-01 through D-12 coverage audit |
| .planning/argonauts/t_26854470-edge-coverage.json | A | 000000→100644 | ca003feb44a6 | unresolved edge projected coverage |
| .planning/argonauts/t_26854470-edge-input.json | A | 000000→100644 | 698cd0e224ee | official unresolved edge input original |
| .planning/argonauts/t_26854470-failure-directions.json | A | 000000→100644 | 230b70176a55 | official failure-direction probe output |
| .planning/argonauts/t_26854470-failure-directions.stderr | A | 000000→100644 | e69de29bb2d1 | failure-direction probe stderr original |
| .planning/argonauts/t_26854470-find-phase.json | A | 000000→100644 | e5aedc3f3f0a | official phase plan inventory |
| .planning/argonauts/t_26854470-gap-analysis.json | A | 000000→100644 | 00d280e07beb | official planning gap audit |
| .planning/argonauts/t_26854470-init-plan.json | A | 000000→100644 | bf5c0b955b17 | official plan-phase init output |
| .planning/argonauts/t_26854470-init-plan.stderr | A | 000000→100644 | e69de29bb2d1 | plan-phase init stderr original |
| .planning/argonauts/t_26854470-phase-op.json | A | 000000→100644 | 9af65b03b663 | official phase-op precondition output |
| .planning/argonauts/t_26854470-plan-post.json | A | 000000→100644 | 5825917e0642 | official plan post contribution output |
| .planning/argonauts/t_26854470-plan-pre.json | A | 000000→100644 | 3c10f4ba3529 | official plan pre contributions |
| .planning/argonauts/t_26854470-plans.sha256 | A | 000000→100644 | 5e3b0e92564b | saved PLAN SHA-256 fingerprints |
| .planning/argonauts/t_26854470-roadmap-final.json | A | 000000→100644 | cd2fc438916c | official final planning roadmap result |
| .planning/argonauts/t_26854470-state-final.json | A | 000000→100644 | 7f159fc34ec2 | official final planning state result |
| .planning/intel/SYNTHESIS.md | M | 100644→100644 | e359937b4a73 | approved six-document ingestion synthesis |
| .planning/intel/classifications/design-0122db01.json | A | 000000→100644 | 60bee96c26ae | design source ingestion classification |
| .planning/intel/classifications/prd-r-774f3cd6-20a2f1ff.json | A | 000000→100644 | 1303e9c3662e | PRD source ingestion classification |
| .planning/intel/classifications/proposal-9afba497.json | A | 000000→100644 | a9910f4fc546 | proposal source ingestion classification |
| .planning/intel/classifications/r-774f3cd6-brief-e27bd809.json | A | 000000→100644 | cc792994b376 | Brief source ingestion classification |
| .planning/intel/classifications/spec-2da50a7e.json | A | 000000→100644 | afd4a978976c | spec source ingestion classification |
| .planning/intel/classifications/tasks-e80e870e.json | A | 000000→100644 | 69b94c44449e | tasks source ingestion classification |
| .planning/intel/constraints.md | M | 100644→100644 | 9e646a7e1857 | ingested REQ-23 constraints |
| .planning/intel/context.md | M | 100644→100644 | 0e4ce31a20f4 | ingested request context |
| .planning/intel/decisions.md | M | 100644→100644 | 41695673af17 | ingested approved requester decisions |
| .planning/intel/requirements.md | M | 100644→100644 | 58fcd4c5d6ae | ingested REQ-23 requirements |
| .planning/phases/06-pyproject-description-uat/.gitkeep | A | 000000→100644 | 8b137891791f | phase directory placeholder |
| .planning/phases/06-pyproject-description-uat/06-01-PLAN.md | A | 000000→100644 | 045379359d07 | approved current implementation plan |
| .planning/phases/06-pyproject-description-uat/06-01-SUMMARY.md | A | 000000→100644 | 2516962ee532 | this PLAN execution summary |
| .planning/phases/06-pyproject-description-uat/06-02-PLAN.md | A | 000000→100644 | 5fecd72dbc93 | approved downstream product implementation plan |
| .planning/phases/06-pyproject-description-uat/06-CONTEXT.md | A | 000000→100644 | 42c1218208a8 | D-01 through D-12 decision contract |
| .planning/phases/06-pyproject-description-uat/06-PATTERNS.md | A | 000000→100644 | 00f23a5d38cf | planning analog and pattern map |
| .planning/phases/06-pyproject-description-uat/06-RESEARCH.md | A | 000000→100644 | 299470caf706 | planning research original |
| .planning/phases/06-pyproject-description-uat/06-VALIDATION.md | A | 000000→100644 | 0f68d3a4576b | phase validation strategy and later independent signoff |
| .planning/state.json | M | 100644→100644 | bed2dc22281e | official state mutation sidecar |
| _bmad-output/initiative-r-774f3cd6/brief/.memlog.md | A | 000000→100644 | 83b21a2aa0f8 | Brief revision history |
| _bmad-output/initiative-r-774f3cd6/brief/.template.md | A | 000000→100644 | 4ed85161a46b | Brief merged template |
| _bmad-output/initiative-r-774f3cd6/brief/r-774f3cd6-brief.html | A | 000000→100644 | 28c4f43b0149 | Brief required HTML view, not product UI |
| _bmad-output/initiative-r-774f3cd6/brief/r-774f3cd6-brief.md | A | 000000→100644 | f4254ad479cc | approved revised Brief |
| _bmad-output/initiative-r-774f3cd6/brief/review-editorial.md | A | 000000→100644 | 95e47c883322 | Brief editorial review |
| _bmad-output/initiative-r-774f3cd6/brief/review-fresh-reader.md | A | 000000→100644 | 59e9d3a4f8e0 | Brief fresh-reader review |
| _bmad-output/initiative-r-774f3cd6/brief/review-reconciliation.md | A | 000000→100644 | 9cf2d507e82b | Brief review reconciliation |
| _bmad-output/initiative-r-774f3cd6/brief/review-rubric.md | A | 000000→100644 | 854d6b2a5497 | Brief rubric review |
| _bmad-output/initiative-r-774f3cd6/open-questions.md | A | 000000→100644 | dd0fc5c8485c | OQ-1 resolved answer record |
| _bmad-output/initiative-r-774f3cd6/prd/.memlog.md | A | 000000→100644 | 8ef42455cc25 | PRD revision history |
| _bmad-output/initiative-r-774f3cd6/prd/.template.md | A | 000000→100644 | ca0de80ca18c | PRD merged template |
| _bmad-output/initiative-r-774f3cd6/prd/prd-r-774f3cd6.md | A | 000000→100644 | 4c27d3737962 | approved revised PRD |
| _bmad-output/initiative-r-774f3cd6/prd/review-fresh-reader.md | A | 000000→100644 | 0b12fadebc11 | PRD fresh-reader review |
| _bmad-output/initiative-r-774f3cd6/prd/review-prose.md | A | 000000→100644 | 992a1f359aa8 | PRD prose review |
| _bmad-output/initiative-r-774f3cd6/prd/review-reconciliation.md | A | 000000→100644 | 9e8707e74188 | PRD review reconciliation |
| _bmad-output/initiative-r-774f3cd6/prd/review-rubric.md | A | 000000→100644 | f0339bc58980 | PRD rubric review |
| _bmad-output/initiative-r-774f3cd6/prd/review-structure.md | A | 000000→100644 | 802edda8e6ba | PRD structure review |
| _bmad-output/initiative-r-774f3cd6/review-specification.md | A | 000000→100644 | 65215f95938e | OpenSpec revision independent review |
| openspec/changes/r-774f3cd6-pyproject-uat/.openspec.yaml | A | 000000→100644 | ac69935e437e | change identity/schema metadata |
| openspec/changes/r-774f3cd6-pyproject-uat/design.md | A | 000000→100644 | 48b341aff998 | approved verification design |
| openspec/changes/r-774f3cd6-pyproject-uat/proposal.md | A | 000000→100644 | b624972bfd6e | approved change proposal |
| openspec/changes/r-774f3cd6-pyproject-uat/specs/package-metadata/spec.md | A | 000000→100644 | 1acde956b520 | approved metadata acceptance requirements |
| openspec/changes/r-774f3cd6-pyproject-uat/tasks.md | A | 000000→100644 | 9578ecc4dbe1 | OpenSpec 1.1/1.2/1.3 execution checkboxes |
| pyproject.toml | M | 100644→100644 | eeff26ea895b | **PRODUCT** (deliberately not in registry) |

### 5b. Product commit e1f2c3a → quality start HEAD 0d79ee4 (verifier "index" scope, 7 entries; all registered process paths, no product path)

| Path | St | Mode | New blob | Purpose |
|---|---|---|---|---|
| .planning/ROADMAP.md | M | 100644→100644 | f0f72ba5c6eb | Phase6 plan execution progress |
| .planning/STATE.md | M | 100644→100644 | 05579ecf2cf7 | official sequential execution current position |
| .planning/argonauts/r-774f3cd6/builder-cli.md | M | 100644→100644 | e3fbbad4f1da | Builder actual stdout/stderr/exit and approval evidence |
| .planning/argonauts/r-774f3cd6/product-target.json | A | 000000→100644 | f2c2a10c7647 | downstream 06-02 fixed product commit and independent hash binding |
| .planning/argonauts/r-774f3cd6/quality-runbook.md | A | 000000→100644 | c4f8532f7182 | downstream independent quality exact command and delivery instructions |
| .planning/phases/06-pyproject-description-uat/06-02-SUMMARY.md | A | 000000→100644 | 888809dd2a2e | downstream product PLAN execution summary |
| .planning/state.json | M | 100644→100644 | b0a90c82b63d | official state mutation sidecar |

### 5c. Worktree / untracked / ignored at gate time

worktree 0, untracked 0, ignored 0 (`git status --porcelain --ignored` empty). No submodule, symlink, unmerged or deletion entries.

## 6. CI (one finite read, no wait; Actions + commit status API, no Checks API)

Head 0d79ee4: Actions `pytest` run 45420880580 (pull_request) completed/success; run 45420856168 (push) completed/success. Commit statuses: none. `.github/workflows` diff from baseline: none.

## 7. Residual differences after the gate (quality-owned, `.planning/` only)

Created/updated by this quality run after commands 1–3, before the report commit: `06-VALIDATION.md` (Nyquist audit, registered M), `06-SECURITY.md` (new; secure-phase audit), `06-REVIEW.md` (code-review gate; attached, not committed), `06-VERIFICATION.md` (registered), this file (registered), `.planning/argonauts/t_81c896f6/openspec-verify.md` (last-phase OpenSpec verify), and the official `phase.complete` writes to ROADMAP/STATE/REQUIREMENTS/state.json (registered M). `06-SECURITY.md` and `t_81c896f6/openspec-verify.md` are mandatory phase-gate originals that the Builder registry (fixed by hash c78c12ef…) does not list; see section 8. No product, verifier, self-test or registry byte is changed by quality.

## 8. Post-report-commit gate

Recorded after the report commit in 06-VERIFICATION.md §"Post-report gate" and in the card completion summary (this file cannot record its own commit).
