## Verification Report: r-5a3b8a3f-wordfreq

Using change: r-5a3b8a3f-wordfreq（カード t_3dc4a405、フェーズ検証 1、start_sha 0cd4673bb75d78e465aa84c8dd31e8ff810a44b8）

入力: `openspec status --change r-5a3b8a3f-wordfreq --json`（schema spec-driven、proposal/specs/design/tasks すべて done）、`openspec instructions apply --change r-5a3b8a3f-wordfreq --json`（taskTrackingConfigured true、progress 8/8、remaining 0、state all_done、unavailableTrackingFiles なし）。

### Summary
| Dimension    | Status |
|--------------|--------|
| Completeness | 8/8 tasks、7 reqs（ADDED 7） |
| Correctness  | 6/7 reqs covered（「試験と実行環境（FR-7・FR-8）」の CI シナリオ未達） |
| Coherence    | Followed（design D-A〜D-F と一致） |

### Completeness
- Task Completion: 8/8 完了。ただし task 3.3 は「CI の有無確認と block 判定の準備」であり、CI の合格を意味しない（01-CI-GAP.md §3）。
- Spec Coverage: ADDED 7 要件すべてに実装または記録がある（下表）。

### Correctness（Requirement Implementation Mapping / Scenario Coverage）
| Requirement | 実装 | 試験 | 実CLI確認（cli-evidence.md） |
|---|---|---|---|
| FR-1 実行とファイル読み込み | `wordfreq/__main__.py` main、`wordfreq/sources.py` FileSource | tests/test_cli.py、tests/test_sources.py | 通常 exit 0、不存在 exit 1（stdout 空）、非UTF-8 exit 1、空ファイル text 出力なし/json `[]` exit 0、引数0個・2個 exit 2 |
| FR-2 `--top` | `__main__.py`（type=int、<1 は parser.error） | test_cli.py | 既定10件、`--top 3`、種類数<N で全件、`--top 0`/`abc` exit 2 |
| FR-3 `--format` | `formatters.py`、argparse choices | test_formatters.py、test_cli.py | json 配列（word/count）、`--format xml` exit 2 |
| D-3 切り出しと正規化 | `tokenizer.py`（`\w+` re.UNICODE、casefold、tokenizer 注入） | test_tokenizer.py | Hello×3→hello 3、`one, two. one`→one 2、日本語は `\w` 連続で決定的 |
| FR-4・D-2 順序決定論 | `aggregator.py` top_words（key=(-count, word)） | test_aggregator.py | apple/zoo 同数5で apple→zoo、2回実行一致、PYTHONHASHSEED 1/99 で同一 md5 |
| FR-5・FR-6 部品分離・入力境界 | 4 モジュール分離、`TextSource` プロトコル、design.md D-A に StdinSource/URL 追加方針 | test_sources_boundary.py（3件） | — |
| FR-7・FR-8 試験と実行環境 | pytest 43件、pyproject `dependencies = []` | ローカル `python -m pytest` 43 passed（exit 0）、PYTHONHASHSEED=42 でも 43 passed | **CI の pytest ジョブが存在しない**（Actions workflows total_count=0、`git ls-files .github` 空） |

### Coherence
- Design Adherence: D-A（4分割と依存方向：tokenizer/aggregator/formatters は入出力を知らず、`__main__` だけが合成）、D-C（exit 0/1/2）、D-E（JSON `ensure_ascii` 配列）と実装が一致。
- Code Pattern Consistency: 標準ライブラリのみ、型注釈と docstring が統一。逸脱なし。

### Issues by Priority
1. **CRITICAL**
   - Requirement not fully met: 「試験と実行環境（FR-7・FR-8）」Scenario「CI で pytest が通る」。repo に CI の pytest ジョブが無く、対象 head での CI 成功証拠が無い（REQUIREMENTS.md の REQ-07 も Pending）。
     Recommendation: 人が CPython 3 の版を確定し `.github/workflows/` に pytest ジョブを追加して依頼 branch に push し（Bot は workflow 権限なし）、対象 head での成功を確認する。手順は `.planning/phases/01-wordfreq-cli/01-USER-SETUP.md`。
2. **WARNING**
   - 前 PLAN からの持越し（01-CI-GAP.md 末尾）：読み取り専用試験の継承 `GIT_*`（`GIT_INDEX_FILE` 等）とグローバル Git 設定の隔離が未対応。Recommendation: tests/test_cli.py の一時 repo 実行で `GIT_*` を除いた env を渡す。
3. **SUGGESTION**
   - `openspec validate r-5a3b8a3f-wordfreq --strict` は exit 1（7件すべて WARNING「SHALL or MUST を含むべき（英語仕様の RFC 2119 推奨）」）。日本語仕様のため実害なし。archive 前に必要なら「〜しなければならない（MUST）」の併記を検討。
   - 非 UTF-8 の stdout（例 `LANG=C` で日本語出力）時の挙動は未観察。

### Final Assessment
1 critical issue(s) found. Fix before archiving.（CI pytest ジョブの不在。1 warning、2 suggestion）
