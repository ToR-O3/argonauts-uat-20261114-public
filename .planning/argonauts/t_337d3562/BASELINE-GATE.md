# 04-01 baseline gate — saved originals, not independent acceptance

- Request r-e476c11d / task t_337d3562 / run 143 / actor argonauts-uat-builder.
- PLAN: `.planning/phases/04-wordfreq-min-count/04-01-PLAN.md` only.
- Planning baseline: `9eb1e694aafc6cd29f0f7d2a29382764bc1627fb`.
- Formal task 04-01-01 commit / capture head: `789cc17267fb4cfeea24111797c3d934c542ce6a`.
- Gate disposition: **baseline saved and read-only checks passed; product-edit prerequisite met**. Same-card independent quality review remains pending; 04-02 must wait for its completion.

## Immutable identity / timeline

Root: `.planning/argonauts/r-e476c11d/baseline/`.
Original absolute root: `/home/Yuki/workspace/argonauts-uat-20261116/work/public/.worktrees/t_337d3562/.planning/argonauts/r-e476c11d/baseline`.
Index: `index.json`; seal: `index.sha256`.
Index SHA-256: `d317798933ee5cd20e10363e336ec164bc4272599e14cfd6c89ba84d8816f089`.

1. Browser-free RED: real driver missing, then missing entrypoint/validator; later forged argv, unindexed extra file, successor-worktree reading and task/run identity assertions failed before their fixes. Initial RED output is in `red-matrix.txt` and `red-entrypoint.txt`; later failure outputs are in the worker transcript. No syntax/import accident is claimed as the behavioral RED.
2. Browser-free GREEN: 31 passed (15.55 seconds), full suite 392 passed (29.97 seconds).
3. Formal driver/tests task commit `789cc17267fb4cfeea24111797c3d934c542ce6a`; post-commit tracer feedback 31 passed (15.57 seconds).
4. Preflight re-read real git head/tree, tracked analogs, exact driver/tests blobs and formal commit existence/time. Product and protected paths equal planning baseline. Execution surface status empty. Planning-only STATE/log changes were separately recorded, not silently excluded as code changes.
5. Single baseline action started `2026-11-17T22:41:11.312589+00:00`, ended `2026-11-17T22:41:34.005358+00:00`; measured capture 22.69278054399183 seconds, exit 0. This is measured capture time, not a promise about all future E2E gates.
6. Read-only saved-original verification: 16 passed, 31 deselected, 10.06 seconds; exit 0. This includes normal original validation, seven destructive controls on scratch copies only, and eight in-memory manifest controls. Originals/index are unchanged.
7. Full suite after capture: 392 passed, no skip/failure/error, 30.94 seconds; exit 0.
8. First product min-count edit: **not performed** in this PLAN. Baseline head is never relabelled as a later head.

The terminal did not inject task/run variables. Before the action, the worker explicitly exported the actual values from kanban_show: `HERMES_KANBAN_TASK=t_337d3562`, `HERMES_KANBAN_RUN_ID=143`. Actual profile was already `argonauts-uat-builder`; it was not changed. These are attribution metadata, not authentication.

## Real artifacts and environment

- 12 real CLI executions: default format omitted text; explicit text/json/html of the same UTF-8 `input.txt` tie/more-than-ten-word-types fixture; empty/whitespace/punctuation; long top12/default/99; injection/Unicode; CR basename.
- All baseline argv omit min-count; default text/top10 literal oracle is hello3,zoo2,apple2,one2,two1,b1,c1,d1,e1,f1; original total17. Full long original total200.
- 9 HTML documents × two widths = 18 actual browser views, 32 actual full/tile PNGs, 144 indexed artifacts plus index/seal. All stdout/stderr bytes, separate HTML=stdout bytes, input bytes, exact CLI argv/cwd/executable/environment, raw Range/font/network, derived views and SHA identities are saved.
- Python 3.12.15 `/usr/bin/python3`, pytest 9.0.3, Playwright 1.60.0, Chromium 156.0.8078.73 `/usr/bin/chromium-browser`; existing environment only, no install.
- OS: Linux-6.18.58.1-microsoft-standard-WSL2-x86_64-with-glibc2.39.
- Viewports 1280×900 and 320×900 CSS px; DPR1, scale1, fresh contexts, navigation-before-capture scrollbar hiding shared across raw/full/tile. Actual platform fonts are in each raw JSON; launch/OS/browser version in index.
- Managed scratch used through temporary `.planning/.bt` symlink and `TMPDIR=.planning/.bt` to avoid Chromium Unix socket path length. Symlink was removed after capture; no system /tmp substitute, no committed symlink, no product DOM/CSS/raw correction.
- Browser-free synthetic PNG/raw/network controls are explicitly synthetic and cannot pass real-baseline validation. Real saved-original tests do not invoke CLI, browser, pytest recursively, capture, save or index update. Scratch-copy mutations do not mutate originals.

## Commands / results

All commands ran from this task worktree:

```sh
env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest tests/test_min_count_verifier.py -k browser_free -x
# 31 passed, exit0; post-formal-commit tracer rerun also 31 passed.

env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 tools/verify_wordfreq_min_count.py --mode baseline --role builder --output-dir .planning/argonauts/r-e476c11d/baseline
# Exactly once: exit0, synthetic=false, baseline-sealed, 12 cases / 18 views.

env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages WORDFREQ_MIN_COUNT_BASELINE_ROOT=.planning/argonauts/r-e476c11d/baseline /usr/bin/python3 -m pytest tests/test_min_count_verifier.py -k saved_baseline -x
# 16 passed, exit0; no capture/index update.

env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest
# 392 passed, exit0; before/after capture separately logged.
```

Explicit `-k saved_baseline` without opt-in root collected zero and returned exit5 (expected refusal, not a passing saved-original gate). Normal full suite does not collect the opt-in original group. Unsupported capture/review-session/finalize modes return nonzero until 04-03; parser retains the fixed public flags and mode-specific required arguments.

The same repository-relative baseline is readable in successor worktrees using in-memory path resolution only. Original index/root/argv/cwd/head/SHA bytes remain unchanged; an arbitrary root or modified declared root is rejected. Historical git trees, not the current product head, anchor validation. The next builder must run the saved-original command at the current checkout before editing product files.

## Not done / ownership boundaries

- No min-count product implementation, README change, CI/dependency/workflow change, prior-phase stale repair, archive, merge, quality status or independent quality acceptance.
- Images exist and automatic DOM/geometry/network checks passed; **no image has been claimed as actually viewed/readable**. `reviews=[]`, `independent_acceptance=false`, all AC1–AC7/REQ15–REQ21 mappings remain pending.
- Final-head quality-owned CLI regeneration, two-width DPR1 actual viewing, source filter→top order inspection and image comparison belong to later gates. This baseline does not satisfy task2.2.
- Standard attachment delivery is handled separately after this document is committed; PM original read-through is still unperformed. Attachments and digests must be read back before claiming delivery.
- Q-01/Q-02/A-01–04 remain nonrequirements; P6 concurrency is not expanded into a new product guarantee.
