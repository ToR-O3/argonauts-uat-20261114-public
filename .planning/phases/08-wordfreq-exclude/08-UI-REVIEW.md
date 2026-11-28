# Phase 8 — UI Review

**Audited:** 2026-11-29 (worktree HEAD f3747b7)
**Baseline:** 08-UI-SPEC.md (status: draft; checker 7/7 VERIFIED per its sign-off; 14 explicit UI states)
**Screenshots:** not captured by the workflow's Playwright step — the only answering port (localhost:3000, HTTP 200) is an unrelated `text-embeddings` process (pid 393), not this CLI; 5173/8080 answered 000. Playwright capture was therefore not run. Separately, the saved real CLI HTML was opened from `file://` in HeadlessChrome/156 (browser_exec harness) for DOM geometry probes; **images actually viewed: 2** (see Evidence).
**Interaction captures:** off (workflow.ui_interaction_capture is false)
**Status:** UI REVIEW COMPLETE — no BLOCKER; 3 WARNING-level findings, all on behaviour/CSS locked by the approved UI-SPEC and outside this phase's change set.

---

## Pillar Scores

| Pillar | Score | Key Finding |
|--------|-------|-------------|
| 1. Copywriting | 3/4 | All HTML copy byte-identical to contract; fixed empty copy ("…単語を含む UTF-8 ファイルで再実行してください。") is misleading when words existed but were all excluded (contract-locked) |
| 2. Visuals | 4/4 | h1 → metadata → table hierarchy intact; metadata above table in 18/18 measured renders; no new decoration/icons |
| 3. Color | 4/4 | Accent #1D4ED8 only on h1 and total value; #F1F5F9 only on th; computed colors match the spec |
| 4. Typography | 3/4 | 3 sizes / 2 weights as declared (h1 24px/600, th 14px); font stack has no CJK family, and in the audit browser (0 `:lang=ja` fonts) all Japanese copy rendered as blank |
| 5. Spacing | 4/4 | main padding 32px (1280) / 16px (320); rank 56px / count 64px measured; all values on the 4px scale |
| 6. Experience Design | 3/4 | Errors exit 2/1 with empty stdout and no Traceback; empty, populated, 0/1/many all correct; the HTML gives no sign that exclusion happened, so total 5 next to visible rows summing to 3 is unexplained (by design D-06) |

**Overall: 21/24**

---

## Top 3 Priority Fixes

1. **All-excluded empty state reuses the "empty file" copy** — a user whose file had 5 words but excluded them all is told to rerun with a file that contains words, which is wrong advice. Fix (needs a PM/UI-SPEC decision; the current contract forbids reason-specific copy): add neutral copy such as "表示条件に一致する単語はありません。" when `total > 0 and not pairs`, in `wordfreq/formatters.py:34-38`.
2. **Font stack has no CJK fallback for a `lang="ja"` document** — on systems without a default Japanese font, the title, labels, caption, column headers and empty message do not render. This was observed in the audit browser. Fix (needs a UI-SPEC change; the font is fixed now): extend `wordfreq/formatters.py:51` with local family names, e.g. `"Hiragino Sans", "Yu Gothic UI", Meiryo, "Noto Sans CJK JP"`, before `sans-serif`. This loads no web font, so the static/no-network rule still holds.
3. **`--exclude` help omits the blank/`#` comment and Unicode-word rules** — `--help` shows only "exclude words from a UTF-8 file (one word per line)" (`wordfreq/__main__.py:20`), so users must read the README to learn that comments are allowed and that `foo bar` / `foo-bar` are rejected. Fix: add "blank lines and lines starting with # are ignored" to the help string. FR-6 wording governs this.

Minor (not scored as blockers): the HTML does not disclose that exclusions were applied (contract D-06 / UI-SPEC §Existing Document forbids exclusion metadata), so the total no longer equals the sum of visible rows. A future phase could add a neutral "表示件数" line. This needs a PM decision.

---

## Detailed Findings

### Pillar 1: Copywriting (3/4)
- Real CLI outputs contain exactly: title/h1 `単語の出現頻度`, labels `ファイル名` / `総出現回数`, caption `集計結果`, headers `順位 / 単語 / 回数`, and the fixed empty copy. Source: `wordfreq/formatters.py:35-36,44,107,110,114,119-120`. `git diff --quiet 79d83ba…HEAD -- wordfreq/formatters.py` → exit 0 (unchanged).
- `<head>` (CSS + title) is byte-identical across all 13 non-empty HTML outputs: one sha256, `487d10db…daf2`, ×13.
- No exclusion path/content/count leaks into the HTML. grep for `script|onload|onerror|url(|@import|http-equiv|<link|<a |<form|<iframe|ex_apple|exclude` returns 0 matches in populated/longbase/all_excl.
- WARNING: `all_excl` (total 5) and `empty_body` (total 0) share the same empty copy, which asks the user to rerun with a file containing words. That advice is wrong for the all-excluded case. The UI-SPEC locks this copy ("全語除外でも既存空文言を置換しない"), so it is contract-compliant but weak UX.
- WARNING: the help text for `--exclude` is minimal (see Fix 3). Error copy: `FILE: line 4: expected one Unicode word` (exit 2); missing file → `FILE: [Errno 2] …` (exit 2); missing body → exit 1. All have FILE plus a reason, as the contract requires.

### Pillar 2: Visuals (4/4)
- Measured at 1280×900 and 320×900, DPR 1, in 9 documents (18 renders): `metaAboveTable` true, `emptyBelowTable` true where applicable, `rowOverlap` 0, `cellOverlap` 0, document `scrollWidth == clientWidth` (no horizontal scroll).
- Viewed screenshot (320px, long hostile basename): the basename wraps over 6 lines inside the column. `<b>&amp;"q"` shows as literal text (escaping works) and is not ellipsized. The table rows `1 zoo 2` and `2 banana 1` have right-aligned numerics.
- Finding (informational): no focal emphasis distinguishes "filtered" from "unfiltered" output. This is intended by the contract.

### Pillar 3: Color (4/4)
- Computed: h1 `rgb(29,78,216)` = #1D4ED8; th background `rgb(241,245,249)` = #F1F5F9. Source: `.total-value` is the only other accent use (`formatters.py:65,85`). Divider #CBD5E1 is the only border (`:94`). There is no dark branch, and `color-scheme: light` is set (`:46`).
- Accent appears on exactly 2 declared elements. The viewed 1280px screenshot shows the blue `5` total and the light-grey th band.
- Finding: none against the contract. The 60/30/10 split is a role mapping, not a measured area, and the spec says so explicitly.

### Pillar 4: Typography (3/4)
- Declared sizes are 16/14/24px; weights are 400/600 (`formatters.py:52-53,66-67,74-75`). Measured: h1 `24px`/`600`, th `14px`. Computed body family: `system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif`.
- WARNING (environment-exposed, contract-locked): `fc-list :lang=ja` → 0 fonts on this host. `fc-match sans-serif:lang=ja` → Noto Sans (Latin). In both viewed screenshots, the h1, labels, caption, th text and the empty message were **not visible**, and no tofu boxes appeared either. Only Latin/digit glyphs rendered; in the all-excluded image only "UTF-8" from the empty message was visible. `document.fonts.check('24px system-ui','単語')` returned true, so the browser does not flag the gap. The cause is the host font setup plus the stack's lack of a CJK family. Japanese-glyph readability is **unverified** on this host and would fail on any similarly provisioned machine.

### Pillar 5: Spacing (4/4)
- Measured `main` padding-left: 32px at 1280 and 16px at 320 (`@media (max-width:480px)`, `formatters.py:102`). th.rank 56px and th.count 64px at both widths.
- Source values 0/4/8/16/24/32px are all on the spec scale (`formatters.py:48,61,64,71,72,78,87,90,101`). There are no arbitrary values, and 48/64px tokens are unused, as the spec requires.

### Pillar 6: Experience Design (3/4)
- State coverage was checked against real CLI runs (see Evidence). Every error path has empty stdout, the right exit code, and no Traceback (`grep -l Traceback *.err` → none). No-op exclusions (comment-only, no-match) are byte-identical to unset output (`cmp` → equal). Input bytes are unchanged (`sha256sum -c` OK for body.txt/ex_apple.txt).
- WARNING: the HTML is silent about exclusion or threshold filtering, while total stays at the original 5. Readers see a total that does not match the rows. This follows the contract (D-06), but it reduces comprehension.
- No loading, partial, retry or destructive UI exists; this is correct for a static, complete document.

---

## UI State Dispositions (14/14)

Evidence types: **B** = real CLI HTML bytes read, **G** = DOM geometry measured in HeadlessChrome 156 at 1280×900 and 320×900, DPR 1, **I** = image viewed, **S** = source read. No character-level Range or per-glyph clip checks were run.

| # | State | Disposition | Evidence |
|---|-------|-------------|----------|
| 1 | E1 heading — overflow | PASS (G) | h1 not in overflowX list at 1280/320; no inner overflow; `overflow-wrap:anywhere` (S `:69`). Glyphs not rendered on this host (Pillar 4), so visual non-overlap of the text itself is unverified |
| 2 | E1 heading — long-text | PASS (B,G) / glyph readability UNVERIFIED | Copy byte-identical; computed 24px/600, no shrink. Japanese glyphs not visible in 2 viewed images (missing CJK font) |
| 3 | E2 metadata — overflow | PASS (G,I) | longbase@320: 176-char basename wraps to 168px height; overflowX 0; metadata above table; viewed image confirms no clip/overlap |
| 4 | E2 metadata — long-text | PASS (B,G,I) | TAB byte retained (grep count 1); LF kept and CR emitted as `&#13;` (lfbase fnLen 16, height 48); hostile `<b>&amp;"q"` escaped and shown literally; total digits intact |
| 5 | E3 table — empty | PASS (B,G) | all_excl and all_excl_thr (exclude zoo + min-count 3): 0 rows, caption/thead/tbody kept, fixed copy, total **5**; empty_body: total **0**; copy-quality WARNING (Pillar 1) |
| 6 | E3 table — loading | PASS (B,S) | Complete documents only; no script/spinner; errors emit 0 stdout bytes |
| 7 | E3 table — partial | PASS (B) | err_invalid4 (blank/comment/valid/invalid) → exit 2, stdout 0 bytes, `line 4`; mc_top shows intentional selection (apple 2 only, rank 1, total 5) |
| 8 | E3 table — error | PASS (B) | Invalid row and missing exclusion → exit 2; missing body with valid exclusion → exit 1; both missing → exclusion diagnosis, exit 2; `--top 0` → usage, exit 2; all with empty stdout and no Traceback; no HTML error page |
| 9 | E3 table — populated | PASS (B,G) | populated: `1 zoo 2`, `2 banana 1`, total 5; 3 columns, `scope=col` |
| 10 | E3 table — zero-one-many | PASS (B,G) | 0 rows (all_excl), 1 row (one_row: `hello 1`, total 2), 13 rows (many: ranks 1–13 contiguous after excluding `a`, ties b/c in first-seen order, total 18); same labels and structure |
| 11 | E3 table — overflow | PASS (G) | longword: 256-char word wraps (td height 89px at 1280, 401px at 320); overflowX 0, cellOverlap 0, rowOverlap 0, scrollWidth == viewport |
| 12 | E3 table — long-text | PASS (B,G) | Word cell holds all 256 chars (wordLen 256); multi-digit count `1234` and total `1235` intact |
| 13 | E4 empty message — overflow | PASS (G,I) | `.empty-message` sits below the table and has no overflow at 1280/320; viewed 1280 image shows it inside the column |
| 14 | E4 empty message — long-text | PASS (B) / glyph readability UNVERIFIED | Fixed copy byte-identical with no reason-specific substitution; only the Latin "UTF-8" fragment was visible in the viewed image (missing CJK font) |

Not performed (remain unverified): character-level Range checks; network/request observation during document load (static grep only: no external references); rendering with a Japanese font installed.

---

## Evidence

- **Images actually viewed: 2.** (a) `longbase.html` at 320×900, DPR 1: long hostile basename wraps fully and the populated table is visible. (b) `all_excl.html` at 1280×900, DPR 1: `body.txt`, blue total `5`, th band with no rows, empty-message "UTF-8" fragment. In both, Japanese text was invisible. A third capture call overwrote the same harness path before attachment and was not viewed. Images were stored in the browser-harness tmp dir, outside the repo.
- Geometry JSON (18 renders) is saved in the browser-harness workspace, outside the repo, as `uirev8-geom.json`.
- HTML fixtures came from real runs of `uv run -q --extra dev python -m wordfreq <file> --format html [--exclude FILE] [--min-count N] [--top N]` against a temp directory under `$TMPDIR` (deleted after the audit). Cases: populated, mc_top, all_excl, all_excl_thr, empty_body, one_row, many, longword, longbase, lfbase, unset, noop_comment, noop_nomatch, err_invalid4, err_missing_ex, err_body_missing, err_both, err_top0.

## Workflow Deviations (recorded, not hidden)

- Gitignore gate (`.planning/ui-reviews/.gitignore`) was not executed: no capture was written into the repo, and the task constraint allows only this file to be added.
- Commit step (workflow §5) was not executed, per task constraint ("no commit"), even though `commit_docs=true`.
- Registry audit was skipped: no `components.json` (NO_SHADCN), and the UI-SPEC registry table is "none".
- The auditor role (gsd-ui-auditor) was performed inline by this agent because nested delegation was unavailable. Model resolution returned `anthropic/claude-sonnet-5`, which was not used.

## Files Audited

- `.planning/phases/08-wordfreq-exclude/08-UI-SPEC.md`, `08-CONTEXT.md`, `08-01/02/03-PLAN.md`, `08-01/02/03-SUMMARY.md`
- `wordfreq/formatters.py` (unchanged vs 79d83ba), `wordfreq/__main__.py`, `wordfreq/exclusions.py`
- 18 real CLI outputs (stdout/stderr/exit) and 9 of them rendered in HeadlessChrome 156
