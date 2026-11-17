## Verification Report: r-5a3b8a3f-wordfreq

Using change: r-5a3b8a3f-wordfreq（カード t_6545be27、フェーズ検証 1 の再検証、start_sha / verified_target_sha `30d9c175fd87a0d492ef6c1532271f55482c45b8`）。別の変更を検証するときは `openspec-verify-change <name>`。

入力: `openspec status --change r-5a3b8a3f-wordfreq --json`（schema spec-driven、proposal/specs/design/tasks すべて done、isComplete true）、`openspec instructions apply --change r-5a3b8a3f-wordfreq --json`（taskTrackingConfigured true、progress 8/8、remaining 0、unavailableTrackingFiles なし）。前回報告（`.planning/argonauts/t_3dc4a405/openspec-verify.md`、head 0cd4673）以降、`wordfreq/`・`tests/`・`pyproject.toml`・`openspec/` に差分は無く、追加は人の `.github/workflows/pytest.yml`（5c9d8fa）と `.planning/` だけ（`git diff --name-status 0cd4673 HEAD -- . ':!.planning'` → `A .github/workflows/pytest.yml`）。

### Summary
| Dimension    | Status |
|--------------|--------|
| Completeness | 8/8 tasks、7 reqs（ADDED 7） |
| Correctness  | 7/7 reqs covered（前回 CRITICAL だった「CI で pytest が通る」は最新 head の独立 CI 証拠で充足） |
| Coherence    | Followed（design D-A〜D-F と一致） |

### Completeness
- Task Completion: 8/8 完了。task 3.3 は「CI の有無確認と block 判定の準備」で、CI の合格そのものは下の Correctness で別に確かめた。
- Spec Coverage: ADDED 7 要件すべてに実装・試験がある（下表）。REMOVED / RENAMED なし。

### Correctness（Requirement Implementation Mapping / Scenario Coverage）
| Requirement | 実装 | 試験 | 実CLI確認（`.planning/argonauts/t_6545be27/cli-evidence.md`） |
|---|---|---|---|
| FR-1 実行とファイル読み込み | `wordfreq/__main__.py` main、`wordfreq/sources.py:21-22` FileSource | tests/test_cli.py、tests/test_sources.py | 通常 exit 0、不存在・ディレクトリ・非UTF-8 は exit 1（stderr 1行、stdout 空）、空ファイル text 出力なし / json `[]` exit 0、引数0個・2個 exit 2 |
| FR-2 `--top` | `__main__.py`（type=int、<1 は parser.error） | test_cli.py（既定10、3、1、0、不正値、種類数<N） | `--top 1` → 1件、`--top 0` / `x` exit 2 |
| FR-3 `--format` | `formatters.py`、argparse choices | test_formatters.py（4）、test_cli.py | json 配列（word/count）、`--format xml` exit 2 |
| D-3 切り出しと正規化 | `tokenizer.py`（`\w+`、casefold、注入点） | test_tokenizer.py（6） | Hello/HELLO→hello 3、`東京 東京 大阪` → 東京 2 / 大阪 1 |
| FR-4・D-2 順序決定論 | `aggregator.py` top_words（key=(-count, word)） | test_aggregator.py（4） | apple/zoo 同数5で apple→zoo、PYTHONHASHSEED 1/777 で出力 sha256 一致 |
| FR-5・FR-6 部品分離・入力境界 | 4 モジュール分離、`TextSource` プロトコル、design.md D-A/D-B | test_sources_boundary.py（3） | — |
| FR-7・FR-8 試験と実行環境 | pytest 43件、pyproject `dependencies = []`、人の workflow `.github/workflows/pytest.yml`（CPython 3.12） | ローカル 43 passed（Python 3.14.9、exit 0、ローカル証拠のみ） | **CI**: push run 44021335880 / job pytest 133831272938、head `30d9c17…`、completed/success、`Successfully set up CPython (3.12.16)`、`collected 43 items`、`43 passed`。PR run 44021344458（merge 150576c = main 792e9c4 + 30d9c17、tree 一致）も success。詳細 `.planning/argonauts/t_6545be27/ci-evidence.md` |

Scenario「CI で pytest が通る」: WHEN CI の pytest ジョブが実行される → THEN 全試験が成功する — 最新対象 head で充足。Scenario「標準ライブラリのみ」: `dependencies = []`、`test_package_declares_only_development_dependencies` passed — 充足。

### Coherence
- Design Adherence: D-A（4分割と依存方向）、D-B（入力元追加は sources.py の実装追加）、D-C（exit 0/1/2）、D-E（JSON `ensure_ascii` 配列）、D-F（最小 pyproject）と実装が一致。
- Code Pattern Consistency: 標準ライブラリのみ、型注釈と docstring が統一。逸脱なし。

### Issues by Priority
1. **CRITICAL**: なし（前回の CI ジョブ不在は解消）。
2. **WARNING**
   - 持越し（非阻害と確定済み）：tests/test_cli.py の読み取り専用試験が継承 `GIT_*` とグローバル Git 設定を隔離しない。Recommendation: 必要になったら一時 repo 実行に `GIT_*` を除いた env を渡す（本依頼では必須修正にしない）。
3. **SUGGESTION**
   - `openspec validate r-5a3b8a3f-wordfreq --strict` は exit 1（7件すべて WARNING「SHALL or MUST を含むべき（英語仕様の RFC 2119 推奨）」）。日本語仕様のため実害なし。`openspec validate --specs` は「No items found to validate.」（main specs は archive 前で未作成）。
   - 非 UTF-8 の stdout（例 `LANG=C`）時の挙動は未観察（非阻害と確定済み）。

### Final Assessment
No critical issues. 1 warning(s) to consider. Ready for archive (with noted improvements). 2 suggestion(s).
