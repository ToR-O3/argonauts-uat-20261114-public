# Phase 3 independent quality evidence — AC1–AC6 index

- Card: t_9de84d5f ([フェーズ検証 3] wordfreq HTML出力), actor `argonauts-uat-quality` (HERMES_PROFILE), request r-50053edc.
- Verified target head: `995011cd3b77d4d87a6be3bdf5780bf5cbe3b95c` (= origin/argonauts/r-50053edc at start; start_sha of this phase verification). Planning baseline for scope: `5a7659b949dc118b59cea5ef3eb40bcd94337d8d`.
- Product state: `git status --porcelain` showed no product change; session provenance and end_provenance product_status `""`.
- Fresh quality root (did not exist before): `.planning/argonauts/r-50053edc/quality` (+ standalone canaries `.planning/argonauts/r-50053edc/quality-network`). Full originals (190 files, incl. input originals with LF/TAB/markup names) are preserved as the committed archive `.planning/argonauts/t_9de84d5f/quality-evidence.tar.gz` (sha256 d44789a6861a63cd0ad57e52bc5b2cd6f486b926ed82c4ead680dccf80a738e5; the attachment hook does not accept archives); per-file SHA-256 list in `.planning/argonauts/t_9de84d5f/quality-sha256.txt`. The unpacked root is not committed (22 MB, filenames with LF/TAB).
- Environment: `/usr/bin/python3` (CPython 3.12) with `PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages`; CLI env `PYTHONIOENCODING=utf-8 PYTHONUTF8=1 PYTHONDONTWRITEBYTECODE=1`; cwd = worktree root; Chromium 156.0.8078.73 headless (`/usr/bin/chromium-browser`), Linux 6.18.58.1-microsoft-standard-WSL2, TMPDIR `.browser-tmp` (symlink to managed scratch, uncommitted); fonts actually used (CDP platformFonts): Noto Sans, Noto Sans JP. Viewports 1280×900 and 320×900 CSS px, DPR 1, scale 1.

## Commands run by quality (all exit 0)

| # | Command (repo root) | Result |
|---|---|---|
| 1 | `env PYTHONPATH=… /usr/bin/python3 -m pytest` | 284 passed, 8.31 s, no skips |
| 2 | `env PYTHONHASHSEED=12345 PYTHONPATH=… /usr/bin/python3 -m pytest -q -rs` | 284 passed |
| 3 | per-file `-m pytest tests/<f>.py -x` | aggregator 5, cli 97, formatters 9, sources 6, tokenizer 6, sources_boundary 3, html_verifier 158 passed |
| 4 | `tools/verify_wordfreq_html.py --check-evidence-contract` | synthetic only; 17 invalid ledger records rejected, clean accepted-predicate-only |
| 5 | `tools/verify_wordfreq_html.py --check-scope` | base 5a7659b, target 995011c, product_status "", untracked_product [], errors [] |
| 6 | `tools/verify_wordfreq_html.py --role quality --output-dir .planning/argonauts/r-50053edc/quality-network --self-test-network` | verdict passed |
| 7 | `TMPDIR=.browser-tmp … --role quality --actor argonauts-uat-quality --output-dir .planning/argonauts/r-50053edc/quality --mode review-session --session-timeout 7200` (tracked background) | session bf0a406b80c642d59d95f40e7d256169; started 16:00:20Z; ready 16:00:55Z; process exit 0 |
| 8 | 32 images opened one by one in a real browser at 1:1 CSS px (tall 320 px full pages also panned at 1:1, offsets 0/659 or 0/577); 22 raw.json audited with jq (UTF-16/codepoint contiguity, concatenation = text, positive-area non-whitespace, viewport/owner/ancestor clip, positive-area overlap between different texts) | all readable; 0 violations; 0 overlaps |
| 9 | `… --mode finalize --review-ledger .planning/argonauts/r-50053edc/quality/reviews.json` while session live (16:09Z) | finalize-requested; session then: verification_finished 16:09:55Z, observation_end 16:09:56Z, ended 16:09:57Z, verdict accepted, independent_acceptance true, AC1–AC6 accepted, errors [] |
| 10 | direct CLI reruns in scratch: empty text/json/html, malformed UTF-8, missing file, no argument, `--top 0`, `--top -1`, `--format xml`, tie text/json | exit 0/0/0/1/1/2/2/2/2/0/0 as specified |

Key originals: manifest.json 011c7024…, reviews.json d2d5f2a7… (= manifest.ledger_sha256), provenance.json d301a376…, scope.json aebfb2a0…, suite.json 727c3a7e…, browser-network.json aef4d29a…, session canaries 50fb1566…, standalone canaries 9257839d….

## AC mapping

| AC | Requirement | Evidence (paths relative to quality root unless stated) | Judgment |
|---|---|---|---|
| AC1 | REQ-09 self-contained static HTML, 3 columns, no external traffic | 11 × `<case>/stdout.html` (static_audit passed; grep for script/src/href/url(/@import/http = 0); 22 × `<case>/<w>/network.json` interval live-review, only about:blank + case file:// + omnibox chrome:// UI, errors []; `browser-network.json`; `canaries/canaries.json` (clean + failed-resource/document-navigation/early-popup/meta-refresh, real attempts to wordfreq-canary.invalid:9 observed and rejected) | accepted |
| AC2 | REQ-10 basename only above table, pre-top total | images: empty.txt/0, 通常.txt/6 (top1/2/10), frequency.txt/7 (top2), long name/200 (top12/default/99), tie.txt/5, injection name/5; no `private-source-directory` or `/home/` in any stdout.html | accepted |
| AC3 | REQ-11 count desc, normalized first occurrence, all formats | tie-text-1/2 stdout.txt `2\tzoo` / `2\tzoo\n2\tapple`; tie-json-1/2; tie-html-1/2 images; frequency beta 3, alpha 2; long rows 12..2 with ranks 1..12 | accepted |
| AC4 | REQ-12 light only, both widths, readable, raw geometry | 32 images (22 full + 10 tiles) viewed at 1:1, each with notes in reviews.json; raw audit: max right 1080/1081.9/1074.4 (≤1280/1265) and 296/303.5/283.0 (≤320/305); 0 clip/ancestor violations; 0 overlaps; numbers single-line; n-run 2/7 lines, w-run 5/26 lines | accepted |
| AC5 | REQ-13 escaping, injection, strict UTF-8, regressions | injection stdout bytes `&amp;&lt;&gt;&quot;&#x27;`, literal text in images; café 2 / strasse 2 / 日本語 1; CLI reruns (row 10); stderr.bin empty for all 15 cases; full suite 284 passed locally | accepted locally — see CI note |
| AC6 | REQ-14 independent quality regeneration and traceability | rows 1–9; actor/root/head match; reviews.json written by quality from real viewing (viewed_at 16:01:52Z–16:06:21Z, after ready_at, before observation_end) | accepted with gaps below |

## Not passed / gaps (do not read as accepted)

- G-01 Final manifest still contains `cases[].views[].verdict: "pending-review"` and `reviewed_images: []` for all 22 views (and every derived.json) after accepted finalize. 03-04 PLAN verification requires "no pending fields".
- G-02 Required CI `pytest` fails at 995011c (runs 44119531438, 44119518087; job log "5 failed, 279 passed"): two locale-dependent tests (en_GB.iso885915 not installed on the runner) and three scope tests (`git diff 5a7659b…` exit 128 in the CI checkout). See ci-evidence.md.
- REQ-09/REQ-10 "unclassified" rows (EDGE-01/02) kept unresolved as planned; covered by AC1/AC2 concrete evidence; no product question reopened.
