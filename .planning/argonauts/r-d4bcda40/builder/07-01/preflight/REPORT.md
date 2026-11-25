# 07-01 prerequisite failure — not a baseline or implementation result

- Request: r-d4bcda40; task t_87068596; flow full.
- Checked at 2026-11-25T12:17:25Z before the persisted reproduction.
- Origin: https://github.com/ToR-O3/argonauts-uat-20261114-public.git.
- Worktree branch wt/t_87068596 aligned with origin/argonauts/r-d4bcda40.
- Starting HEAD: 8efbfaa1907ace272a4f685e2659144a4085d303.
- Fetch succeeded; base merge returned Already up to date; product/tests/tools/README unchanged (`git diff --exit-code HEAD -- wordfreq/ tests/ tools/ README.md`, exit 0).
- Existing test runner version: pytest 9.0.3. No product tests run.
- Chromium executable version: Chromium 156.0.8078.73, Built from source for Red Hat Enterprise Linux release 10.2 (Coughlan).

## Actual capability probe

The managed scratch file `t_87068596-browser-preflight.py` imports Playwright and the existing generic `tools.verify_wordfreq_html.instrumented_browser`, launches `/usr/bin/chromium-browser`, and would open about:blank in a 320x900 DPR1 context. It does not invoke an old request driver, capture a baseline, modify product code, or claim HTML acceptance.

Command (cwd: this worktree):

```
env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 /home/Yuki/workspace/argonauts-uat-v111-20261122/home/.hermes/profiles/argonauts-uat-builder/cache/scratch/t_87068596-browser-preflight.py
```

The first probe failed exit 1. One finite reproduction saved original stdout.txt/stderr.txt alongside this report and also failed exit 1. Both failed before yielding a browser. Chromium reported `FATAL:chrome/browser/process_singleton_posix.cc:315] Socket path too long` for its SingletonSocket under the active managed scratch TMPDIR. The helper raised `RuntimeError: Chromium debugger unavailable`. Playwright import succeeded; browser startup did not. The raw persisted second-run diagnostic is in stderr.txt, not reconstructed here.

TMPDIR was `/home/Yuki/workspace/argonauts-uat-v111-20261122/home/.hermes/profiles/argonauts-uat-builder/cache/scratch`. No /tmp override, symlink alias, dependency installation, browser flags workaround, or CI modification was attempted.

## Gate and handoff

07-01-PLAN task 07-01-01 precondition explicitly requires working existing browser/managed scratch before product edits and says to stop on inability, without rescuing through the old short-path exception. The fixed baseline mode has not been invoked, and no baseline root or partial oracle has been created. Additional max-count tests, preimplementation RED, product implementation, SUMMARY, OpenSpec checks, commits, push, and draft PR creation remain undone. GSD STATE/ROADMAP remain unchanged; no plan advance or completion is claimed.

PM needs to determine an authorized managed-scratch-compatible browser startup path, or arrange an environment repair. Recommended: preserve the pre-edit gate and repair/authorize the temporary-path setup, then rerun this capability probe before baseline capture. Do not weaken the image/raw/network requirements or reuse earlier request acceptance.

The reception card was reread before this decision; there is no dated `argonauts: 依頼者の判断` comment or new exception authorizing a short-path override.
