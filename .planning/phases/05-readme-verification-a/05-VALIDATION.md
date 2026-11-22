---
phase: "05"
slug: "readme-verification-a"
status: validated
nyquist_compliant: true
wave_0_complete: true
created: "2026-11-22"
---

# Phase 05 — Validation Strategy

## Test Infrastructure

| Property | Value |
|----------|-------|
| Framework | Existing Git / GNU CLI; no new tests or scripts |
| Config file | No new config; .planning/config.json retains Nyquist/security/checks |
| Quick run command | `printf '%s\n' '検証A: v1.12 の通しの確かめ（2026-11-22）' \| cmp -i 0:4643 - README.md` |
| Full suite command | Research C1–C6 separately, plus all-path scope and evidence review |
| Estimated runtime | Seconds for CLI; evidence review duration not measured |

## Sampling Rate

- After each task: task's CLI guards and evidence readback; do not claim content acceptance from diff display exit 0.
- After each wave / before verify-work: C1–C6 and full request scope review.
- Commands and all inputs must exist by their task's end. Use pipefail for pipelines and record every actual exit code.

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 05-01-01 | 05-01 | 1 | REQ-22, REQ-23; OpenSpec 1.1 | T-05-01 | exact bounded content / existing byte preservation | CLI + complete patch review | Research C1/C2/C3/C4 verbatim in 05-01-PLAN.md; each automated has adjacent fails_when | README and fixed Git blob exist; task creates 05-BUILDER-CLI.md before readback | pending execution |
| 05-01-02 | 05-01 | 1 | REQ-24; OpenSpec 2.1 | T-05-02, T-05-03 | no unauthorized product changes / head provenance | CLI + all-path content review | Research C5/C6 verbatim plus C1-C4 re-run; each automated has adjacent fails_when | Git repo and task1 report exist; H_impl must be officially committed before C6; task creates 05-QUALITY-HANDOFF.md before readback | pending execution |

One PLAN, two sequential tasks: 05-01-01 tracer → 05-01-02. Official execution stacks on local HEAD (wt/t_8a90bad6 in planning), distinct from the formal delivery branch argonauts/r-8ac79daf. Retain workflow.use_worktrees=false; no other-worktree merge or branch switch. Later the card worker delivers local HEAD with `git push origin HEAD:refs/heads/argonauts/r-8ac79daf` (single command, workdir omitted per Argonauts E.3), then matches the remote SHA from `git ls-remote origin refs/heads/argonauts/r-8ac79daf` to the delivered local SHA. Planner does not push. Each task verifies at its end; phase quality covers all resulting artifacts. No future quality file is an input to a Builder task. Baseline README 54106df87baa6cc017167eb311fd0fd4f81ea0fa, 4643 bytes; request baseline c6b701bfdc1af9c39f9b8421336e881e5cda6ee4. Recheck before implementation; changed preconditions stop rather than silently replacing baseline.

Builder performs read_file content/CLI-evidence checks in task actions and acceptance criteria, not human-check tags. The tracer retains its automated guards; execute-plan.md's existing end-of-phase automated tracer feedback path re-verifies before task2 without a human checkpoint. No workflow/check/security setting is weakened. Task2 reads the concrete analog .planning/phases/04-wordfreq-min-count/04-VERIFICATION.md and .planning/argonauts/r-8ac79daf-learnings.md, adopting only requirement/verdict/source tables, head provenance, complete scope review, and separate quality/delivery/acceptance gates. Old verdicts, numbers and tests are not evidence for this phase.

## Wave 0 Requirements

Existing infrastructure covers all phase requirements. No code/test/fixture/script additions. Byte comparisons use existing CLI and Git blobs, not generated test files. Evidence markdown is produced in its task before readback.

## Content / Delivery Reviews (Builder or Independent Quality, Not Human Checkpoints)

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Classify every request diff including untracked files, inspect complete README patch | REQ-24 | A path listing or diff exit 0 does not prove classification | Read all changes and explicitly classify product vs process; reject any other product file |
| Quality evidence is PM-readable | REQ-24 | Delivery and source agreement require review | Independently run commands at target head; attach VERIFICATION and CLI text; images 0 and reason unless actual images were viewed |

## Validation Sign-Off

- [ ] Each task has automated CLI guards plus observable fails_when.
- [ ] No three consecutive tasks without automated verification.
- [x] No missing test-file dependencies / no Wave 0 code.
- [x] No watch-mode flags.
- [ ] Final plan-checker confirms complete mapping.
- [ ] Quality independently verifies actual implementation.

## Probe / Evidence Status

- Official edge probe: REQ-22, REQ-23, REQ-24 remain unclassified/unresolved, three flagged assumptions in 05-01-PLAN.md. Approved acceptance checks are mapped without modifying or dismissing probe rows.
- Descriptorless transparency prohibition: unresolved and flagged-unverified, no invented test/check descriptor; publication is not certification of an end-to-end pass.
- B_doc and B_request, implementation H_impl, quality target and report H_report are separate evidence fields. H_report is read after official report commit and stated in delivery text; report self-SHA is not fabricated.
- Quality later creates 05-VERIFICATION.md and 05-QUALITY-CLI.md, independently runs C1-C6, records every raw exit and complete scope classification, then standard-attaches both readable documents and reads the exact attachments back. Images: 0, because only README text/bytes/Git scope change; any actual image viewing instead requires count/content/result in text.
- Official plan frontmatter and structure validation are planning-only; checker and implementation/quality execution remain pending. Static pipeline warning must not be treated as successful runtime evidence: the PLAN requires `set -o pipefail` in the real execution shell, one verification per invocation and failure-preserving exit handling. C1-C6 stay unchanged.
- Research Open Questions / Planning Handoff is RESOLVED for baseline recheck, exact evidence names/quality-card standard attachments/runtime head recording, and retained LOW confidence. Resolution fixes the planning contracts only; execution SHAs/results/attachment completion are still unobserved and must not be fabricated. Edge/prohibition unresolved statuses are unchanged.

Approval: Nyquist audit 2026-11-22, quality card t_df0c2ebc at cc46cf164aeff3ccbf19cbb7489b5be01f486901. State A audit via gsd-validate-phase 5: PLAN and SUMMARY read, one PLAN / two sequential tasks; no missing infrastructure or automated command dependency. C1-C4 six independent calls raw exit0; C5 forbidden-path guard raw exit0; C6 committed README equality raw exit0. Existing Git/GNU CLI is the authorized test infrastructure, no new tests/scripts permitted or needed. Automated coverage exists for REQ-22/23 and scope/head guards for REQ-24. Supplementary all-path content review and evidence delivery are procedural checks, not a replacement for these automated checks; still pending the official verifier and parent attachment readback at this audit point. This coverage verdict alone does not close the phase, certify end-to-end verification, or imply PM acceptance. Original planning-time pending entries above describe their original timing and are superseded by this audit for execution coverage only. Descriptorless prohibition remains flagged-unverified.

## Validation Audit 2026-11-22

| Metric | Count |
|---|---|
| Gaps found | 0 |
| Resolved | 0 |
| Escalated | 0 |
