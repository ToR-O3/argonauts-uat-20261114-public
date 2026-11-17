# Phase 03 — UI Review

**Audited:** 2026-11-18
**Baseline:** 03-UI-SPEC.md (status: approved)
**Screenshots:** not captured by this audit. No dev server exists by design: the product is static HTML written to CLI stdout. The audit used the existing quality captures from real Chromium 156 (DPR 1; 1280×900 and 320×900 CSS px viewports) in `.planning/argonauts/r-50053edc/quality/<case>/<width>/`. I opened and viewed these PNGs: `empty/1280/full.png`, `long-12/1280/full.png`, `long-12/320/tile-0.png` and `injection/320/full.png`. I did not view the other cases' PNGs. For those cases the audit relies on `formatters.py` and the `raw.json` geometry/computed-style records. I did not run the gitignore gate because the audit wrote no capture into the repository, and the task allowed writing only this file.
**Interaction captures:** off (`interaction_capture: false`). The UI-SPEC also excludes all interaction: no script, links, forms or theme switch.

---

## Pillar Scores

| Pillar | Score | Key Finding |
|--------|-------|-------------|
| 1. Copywriting | 4/4 | Every contract string matches exactly, including title/h1, labels, caption, three column headers and the empty-state sentence. |
| 2. Visuals | 3/4 | The hierarchy is clear and matches the contract. At 1280 px, the header pair "順位 単語" sits only 16 px apart, so it reads as one phrase, and a 256-char token creates a 641 px row at 320 px. |
| 3. Color | 4/4 | All computed colors match the spec hex values. The accent appears only on the h1 and the total value. |
| 4. Typography | 3/4 | There are exactly 3 sizes (24/16/14) and 2 weights (600/400) with the specified line heights. The rendered face depends on environment fallback (Noto Sans / Noto Sans JP variable), not on a fixed face. |
| 5. Spacing | 4/4 | Measured gaps of 4/8/16/24/32 px (16 px at ≤480 px) match the spacing tokens exactly in raw geometry. |
| 6. Experience Design | 3/4 | Empty, zero/one/many, long-text and narrow-width states are handled. Rank is a row sequence, so tied counts get different ranks with no visual cue (this is required by D-05, but a reader can misread it). |

**Overall: 21/24**

No BLOCKER findings. Every deviation below is a WARNING or an informational note. None of them breaks the UI-SPEC contract.

---

## Top 3 Priority Fixes

1. **The rank and word headers read as one phrase.** "順位" is right-aligned in the 56 px rank column and "単語" is left-aligned in the next column, leaving only 8+8 px between them (seen in `empty/1280/full.png` and `long-12/1280/full.png`). Readers may see "順位 単語" as a single label. A spec-compatible fix is to add 1px `#CBD5E1` vertical dividers only in `thead`, or to raise the padding between rank and word to the 16px md token. The alignment and the 8px cell padding are mandated, so this needs a UI-SPEC amendment first.
2. **Tied counts get distinct ranks with no cue.** For example, tie-html-2 shows zoo 2 at rank 1 and apple 2 at rank 2. A reader can take rank 1 as "more frequent". D-05 mandates row-sequence ranks, and the spec forbids extra meta labels, so the fix belongs at the contract level: consider allowing the caption to read "集計結果（同数は初出順）" in a future spec revision. No change is allowed under the current contract.
3. **The rendered font depends on whatever fonts the host has installed.** `platformFonts` in raw.json resolves CJK to "Noto Sans JP" (variable font, reported as postScriptName `NotoSansJP-Thin`) and Latin to "Noto Sans". The 600 weight rendered visibly bold in the screenshots, but on hosts without a variable CJK font, weight 600 may be faked by the browser or drop to 400. Recommendation: add `"Hiragino Sans", "Yu Gothic UI", "Noto Sans CJK JP"` before `sans-serif` in a later spec revision. Keeping the system-only stack (no web fonts) stays mandatory.

---

## Detailed Findings

### Pillar 1: Copywriting (4/4)
- `wordfreq/formatters.py:44` `<title>単語の出現頻度</title>` and `:107` `<h1>単語の出現頻度</h1>` match the contract "Document title / h1".
- `:110` ファイル名, `:114` 総出現回数, `:119` `<caption>集計結果</caption>` and `:120` 順位 / 単語 / 回数 (each `scope="col"`) all match exactly.
- `:35-36` empty state body "集計対象の単語はありません。単語を含む UTF-8 ファイルで再実行してください。" matches the spec character for character. It sits outside `tbody` with no colspan fake row. This is confirmed visually in `empty/1280/full.png`.
- There are no generic labels (Submit/OK/Click here), no CTA, no timestamp and no top-N meta label, as the spec requires.
- The basename is shown verbatim, including doubled spaces, LF, TAB and `&<>"'`. This is visible in `long-12/*` and `injection/320/full.png`, where "検査  &<>"'" / "次	終.txt" appear as literal text.

### Pillar 2: Visuals (3/4)
- The visual order is h1 (accent, 24/600) → labelled metadata → caption → table, which gives a clear focal point. The order main → h1 → metadata → table → empty note matches the spec.
- The table header row is the only tinted surface (`#F1F5F9`), and data rows are separated only by a 1px `#CBD5E1` bottom border. No radius, shadow or card is present, which matches the spec.
- WARNING: header adjacency. The rank header is right-aligned and the word header left-aligned, with an effective gap of 16 px, so at a glance "順位 単語" reads as one label (empty/1280, long-12/1280). This is contract-compliant but weakens column separation in the header.
- Note (spec-intended): at 320 px the word column is 153 px wide (`long-12/320/raw.json`: th rects 16–72 / 72–225 / 225–289). The 256-char token therefore wraps to about 17 lines, and the row is 641 px tall (y 450.5→1091.5), which pushes ranks 2–12 below the first screen. The overlapping tiles show this is readable, and no clipping or horizontal overflow occurs (document scrollWidth 305 = clientWidth 305).
- In the long basename, the doubled spaces after "集計" are break opportunities under `break-spaces`, so "集計" sits alone on its first line before the n-run. This is correct whitespace preservation, not a defect.

### Pillar 3: Color (4/4)
- Computed styles in `long-12/1280/raw.json`:
  - h1 `rgb(29,78,216)` = #1D4ED8
  - th background `rgb(241,245,249)` = #F1F5F9
  - th and td text `rgb(15,23,42)` = #0F172A
  - caption `rgb(71,85,105)` = #475569
  - td background #FFFFFF
- The accent is declared in exactly 2 selectors (`formatters.py:65` h1, `:85` `.total-value`). It is not used on links, row ranking or word emphasis.
- The secondary text colour #475569 appears only on `.label`, `caption` and `.empty-message` (`:78`, `:87`, `:101`). The secondary background appears only on `th` (`:96`). The divider color appears only in `th, td` border-bottom (`:94`).
- `color-scheme: light` (`:46`). No dark media query, no image/url and no hard-coded colors outside the declared palette.
- Contrast is ample: #0F172A on white is about 17:1, #475569 about 7.6:1, #1D4ED8 about 6.7:1. On the #F1F5F9 header, #0F172A remains far above 4.5:1.

### Pillar 4: Typography (3/4)
- Size distribution: 24 px (h1), 16 px (body/td/values/empty message), 14 px (`.label`, caption, th). That is exactly the 3 declared sizes.
- Weight distribution: 600 (h1, labels, caption, th) and 400 (body/td). That is exactly the 2 declared weights, set explicitly so browser defaults for h1/th are overridden (`:63-68`, `:73-77`).
- Line heights match: h1 is 30 px tall (24 × 1.25), labels/caption 21 px (14 × 1.5), td content 24 px (16 × 1.5). Each matches a rect height in `long-12/320/raw.json`.
- Numbers use the same family and size as body text, plus `font-variant-numeric: tabular-nums` (`:98`). The right-aligned digits in the count column line up in `long-12/1280/full.png` (123, 12, 11, 10, 9 … 2).
- WARNING: the face is environment-resolved. `system-ui` on this WSL host falls back to Noto Sans / Noto Sans JP (variable). The contract fixes only the stack, so this is compliant, but rendering will vary by OS.

### Pillar 5: Spacing (4/4)
Raw geometry from `long-12/320/raw.json` at the narrow breakpoint:

| Spacing | Measured | Token |
|---|---|---|
| main padding (h1 at x=16, content 16–289 within 305) | 16 px | md |
| h1 bottom 46 → metadata 62 | 16 px | md |
| label bottom 83 → value 87 | 4 px | xs |
| item 1 bottom 303 → item 2 311 | 8 px | sm |
| metadata bottom 360 → table/caption 384 | 24 px | lg |
| caption bottom 405 → thead 413 | 8 px | sm |
| cell padding | 8 px each side; th 37.5 = 21 + 16 + 0.5 collapsed border; data rows 41 = 24 + 16 + 1 | sm |
| column widths | 56 / remainder / 64 px | spec geometry |

- Wide breakpoint: `empty/1280/full.png` content starts at x=192 = (1280−960)/2 + 32, which confirms the 960 px max-width, centering and 32 px xl padding.
- Empty-state note: `margin: 24px 0 0` (`:101`), the lg token.
- No arbitrary values. Every declared spacing in `formatters.py` is in {0, 4, 8, 16, 24, 32}, and the 2xl/3xl tokens are unused, as the spec requires.

### Pillar 6: Experience Design (3/4)
- State coverage (verified against the contract):
  - **Empty:** total 0, three headers, 0 tbody rows, secondary-colour note (empty/1280).
  - **Zero/one/many rows:** cases normal-1/2/10 and long-12.
  - **Oversized top:** long-99 shows 12 rows.
  - **Long text and narrow width:** both 1280 and 320 wrap with no horizontal scroll, ellipsis, nowrap or overflow clip; scrollWidth equals clientWidth.
  - **Error:** no HTML is produced; the existing stderr and exit 1/2 behaviour is kept and stdout is empty, per the spec.
  - **Loading/partial:** not applicable for a static document.
- Accessibility basics: `lang="ja"`, the viewport meta, `caption`, `th scope="col"`, and text plus number rather than colour alone.
- Safety: all dynamic values go through `_html_text` (`:17-19`, html.escape plus CR as `&#13;`). The template has no script, URL, event or form paths, and the injection basename renders as inert text (injection/320).
- WARNING: tied counts get different ranks (1, 2 for zoo 2 / apple 2) with no visible explanation. This is contract-mandated (D-05) but is a comprehension risk. See Top Fix 2.
- No interaction to audit; the spec excludes it, so no penalty is applied for its absence.

---

## Files Audited
- `wordfreq/formatters.py` (HTML/CSS template, escaping)
- `.planning/phases/03-wordfreq-html-output/03-UI-SPEC.md`, `03-CONTEXT.md`, `03-01..04-SUMMARY.md` (read in full); `03-01..04-PLAN.md` (keyword scan only, not read in full)
- Viewed screenshots: `.planning/argonauts/r-50053edc/quality/empty/1280/full.png`, `long-12/1280/full.png`, `long-12/320/tile-0.png`, `injection/320/full.png`
- Raw geometry and computed styles: `.planning/argonauts/r-50053edc/quality/long-12/320/raw.json`, `long-12/1280/raw.json`
