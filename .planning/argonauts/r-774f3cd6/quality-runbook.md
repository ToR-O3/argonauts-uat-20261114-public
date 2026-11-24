# Independent quality runbook — r-774f3cd6 / Phase 6

This is a Builder handoff, **not a quality result**. Independent quality, phase verification, PM original-text acceptance and finalization are pending. No pre-filled quality-cli.md or 06-VERIFICATION.md is produced by Builder.

## Canonical approval and immutable target

- Receipt t_78c8849e, revised PM t_b8e9c36c done/completed run37 approved.
- 判断日時: 2026-11-24T13:00:38.567271+00:00
- 原文：②を選ぶ。description を新設してよい。連結元の文字列は「argonauts-uat public」、完成値は「argonauts-uat public (UAT)」とする。
- Designated source `argonauts-uat public` is not an observed old description; baseline actually lacks description. OQ-1 answered; do not re-ask.
- Repository: ToR-O3/argonauts-uat-20261114-public, base v112-b, request branch argonauts/r-774f3cd6.
- Baseline: b34cba0d008923e7f5267ce52d5403492ea53925.
- Approved revised specification: 56b70bdca4349c6d2f9eaeb62be2e340a3e04b49.
- Immutable product commit: e1f2c3a2e5d36963cfd789997edb6fa2d62b22ed.
- Product blob Git OID: eeff26ea895b3b8d994efe65ac6f926e8b212e35 (not SHA-256).
- Baseline blob SHA-256: 4d50135c1a75196db52ac67e8bd3f0aa3859491249db118f2fa5bccdbff82457.
- Product blob / actual input / working-file SHA-256: 540df8d5bf689fd037f73e336faa5ea05aa809699635472f47dd414dc3afb7e0.
- Verifier SHA-256: dab59500fcfc953dd3d745e6181ee66ace8ed436edcbe1eec00709ee6abe4152.
- Selftest SHA-256: 8351bc8670f4317226140fc70b5ea3a7f9af911833be2fbc9ff7a76fc926c476.
- Exact-purpose registry SHA-256: c78c12efb21bab727241df5ece1a91062f92a711b8ee543946b9dd62aebd1ffa.
- Builder input binding: product-target.json. Its start/end fields describe product preparation, not later reporting commit. Reporting head is supplied after commit/push via review metadata; quality must measure its own start/end HEADs and distinguish all of these.

## Select quality's own root and provenance

Read the standard task/receipt comments and approval again at judgement time. Follow E.4 for same-card review (no merge/commit/push); phase verification follows its own card. Initial root selection only:

```sh
cd -- "$HERMES_KANBAN_WORKSPACE"
pwd -P
git rev-parse --show-toplevel
git remote get-url origin
git rev-parse HEAD
git rev-parse refs/remotes/origin/argonauts/r-774f3cd6
git merge-base --is-ancestor refs/remotes/origin/argonauts/r-774f3cd6 HEAD
```

Workspace must be set, reachable, and physically identical to cwd and Git top-level; otherwise stop. Freeze this root within the run. Never fall back to a different card's worktree or the historical planning root t_26854470. The origin must be the fixed repository; the actual full request remote ref must exist and be an ancestor of HEAD. A normal local `wt/<card>` branch is valid; do not reject just its name. Unknown attribution stops for PM. Verify PR/head/origin according to E.4, after finite fetch. Read product-target.json and tools with read_file, JSON extraction only jq; no inline Python/Node/heredoc scripts.

## Independently retrieve and hash the product

Run these yourself; copying the Builder record strings is not independent computation. Commands run from selected root. Git stdout is binary; sha256sum hashes blob body bytes, not Git object header/OID:

```sh
git rev-parse e1f2c3a2e5d36963cfd789997edb6fa2d62b22ed:pyproject.toml
git show b34cba0d008923e7f5267ce52d5403492ea53925:pyproject.toml | sha256sum
git show e1f2c3a2e5d36963cfd789997edb6fa2d62b22ed:pyproject.toml | sha256sum
sha256sum pyproject.toml .planning/argonauts/r-774f3cd6/verify_description.py .planning/argonauts/r-774f3cd6/test_verify_description.py .planning/argonauts/r-774f3cd6/process-paths.json
git merge-base --is-ancestor e1f2c3a2e5d36963cfd789997edb6fa2d62b22ed HEAD
```

Repository CLI additionally obtains the exact same product blob independently through binary Git subprocess, passes those bytes to verify_content, hashes that actual input, compares working bytes, and compares all target/tool hashes. Review implementation rather than trusting echo of target record. Confirm the independently calculated SHA equals actual_input_sha256, candidate_blob_sha256, working file and target record. Fixed product-to-report changes must be reviewed exact process paths only, in every scope, not merely a matching product hash.

## Mandatory exact commands — execute real files from selected root

Do not prepend a new cd, grep, or inline wrapper. Preserve full stdout/stderr, actual OS exit, elapsed time, cwd and actor. Use scratch captures outside the checkout until writing the already-registered quality text paths.

```sh
python3 -B .planning/argonauts/r-774f3cd6/test_verify_description.py -v
python3 -B .planning/argonauts/r-774f3cd6/verify_description.py repository --baseline b34cba0d008923e7f5267ce52d5403492ea53925 --target-record .planning/argonauts/r-774f3cd6/product-target.json --process-paths .planning/argonauts/r-774f3cd6/process-paths.json --actor quality
```

Expected both OS0. Selftests include correct positive and required missing/duplicate suffix/different value/other item/malformed TOML negatives, plus raw formatting, wrong table/type, Git mode/type/add/delete/rename, staged cancellation, unmerged, untracked/ignored/unknown process path, hash/HEAD/input/error/timeout discrimination. All mutation fixtures stay in active TMPDIR TemporaryDirectory; never write product negative examples. No third-party install required for this suite. Product tests/CI/dependencies must not be modified.

All mandatory repository conditions must PASS, including VALUE_EXACT, CANDIDATE_PARSE, STRUCTURE_UNCHANGED, BYTES_UNCHANGED, PROCESS_PATHS_VALID, TREE_SCOPE, INDEX_SCOPE, WORKTREE_SCOPE, UNTRACKED_SCOPE, IGNORED_INVENTORY, PRODUCT_COMMIT_FIXED, PATCH_ONE_LINE, MODE_UNCHANGED, BLOB_INPUT_SHA256, TOOL_HASHES, HEAD_STABLE, REPO_IDENTITY, REQUEST_BRANCH. OS/output exit mismatch, any mandatory FAIL/SKIP, target/hash mismatch, unavailable command/input, or nonzero selftest means incomplete: stop and return remaining diff/reason to PM. Do not repair unrelated files or bulk-restore another person's changes.

After editing, do **not** rerun missing-description-only preflight/expect-red as acceptance gates. Their original RED is in Builder evidence/history; post-edit checks are content/repository. Builder GREEN is never independent quality acceptance. No browser/images for this non-UI change.

## Full Git boundary and purpose inspection

The CLI outputs fixed baseline→product raw entries and full patches; product→index, index→worktree, product→worktree; porcelain all untracked; ignored inventory. No-renames means deletion+addition both checked. Inspect status/mode/type/OID and both sides; do not miss staged/unstaged cancellation, symlink, submodule or unmerged index. pyproject must be regular100644, exactly +1/-0, fixed approved description immediately after version. Every other path must be an individually reviewed exact entry and purpose in process-paths.json, allowed status and scope. A directory prefix alone is never exemption, nor permission to register unknown code automatically. Record the full exact-purpose list, all inventories, patches and remaining changes. Registry intentionally cannot contain product paths.

The old 06-01 raw capture exists at fe96d5033a0a5b663b80df08673fe666f4a949f3:builder-cli.md; current Builder text preserves its TDD RED narrative and new actual replay RED/GREEN. Avoid recursive embedding of entire evidence patches multiple times: collect a finite snapshot before appending it, and distinguish later record-only updates explicitly. Do not claim a snapshot includes its own later write.

## Quality-owned original text and PM delivery (phase gate)

1. Separate quality actor writes `.planning/argonauts/r-774f3cd6/quality-cli.md`: actual actor, own start/end/report HEAD, immutable product commit, all independently calculated hashes and byte subjects, exact argv/cwd/times/OS exits/stdout/stderr/condition results, full path/status/mode/purpose inventories, patch and residual differences.
2. Write `.planning/phases/06-pyproject-description-uat/06-VERIFICATION.md`: all REQ-23 value/structure/raw/TOML/full Git/attribution conditions mapped to independent original evidence. Flagged assumption: phase SPEC absent, spec-less fallback, edge REQ-23 unclassified/unresolved one item. Preserve supplied=false/no-silent-drop input1=projected1 (do not double-count same edge in both PLANs). Descriptor-less transparency prohibition remains for original-text quality/PM judgement: never call designated source an old observed value, unavailable execution success, or Builder self-check independent quality. Do not silently mark resolved because tests pass; judgement unable means unverified.
3. Attach both text originals through standard kanban_attach with `argonauts:worktree:<exact relative path>` on quality's own card. Read kanban_attachments, then exact attachment originals; recompute SHA-256 for original vs saved path and ensure equality. PM must be able to read both and related originals through read_file. Saving only is not delivery. No images/compressed files required.
4. After quality text/report commit (only where the phase card permits commit), rerun the same full repository gate. Reporting changes must remain exact process paths. A new product/verifier change invalidates old quality and requires re-verification. No waits/watch/polling; CI is a finite read through Actions/status API, not Checks API.
5. Remain within current card: same-card review completes only after passing independent checks; phase gate and PM acceptance are separate. REQ-23 aggregate success and OpenSpec sync/archive must not be inferred from Builder checkbox or document final status.

## Finalization boundary

Only after all tasks, independent verification of the same product commit, every acceptance condition, and PM original-text read/acceptance may finalization sync/archive OpenSpec and request final quality. Builder does not sync/archive here. Full flow overrides intake light because risky path pyproject.toml; carry this reason to final report. Prior phases1/3/4/5 stale evidence is outside scope; do not repair it. Merge/approval/ruleset changes are prohibited for Builder and governed by team guards for quality.
