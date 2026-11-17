# Phase 1: wordfreq CLI - Context

**Gathered:** 2026-11-17
**Status:** Ready for planning
**Source:** PRD Express Path (.planning/argonauts/r-5a3b8a3f-prd.md)

<domain>
## Phase Boundary

依頼 r-5a3b8a3f の承認済み OpenSpec 変更 `r-5a3b8a3f-wordfreq` 全体（tasks.md の 1.1〜3.3）をこの phase 1 で実装する。stdlib-only の Python パッケージ `wordfreq` を追加し、`python -m wordfreq <file>` で単語出現頻度を決定論的に出力する CLI を届げる。ファイル/stdin入力境界、`--top N`（既定10）、`--format text|json`（既定 text）、`\w` 連続抽出 + `casefold()` 正規化、回数降順→単語昇順の決定論的ソート、exit code 0/1/2 規約、pytest 単体試験。画面（UI）は作らない。日本語形態素解析は v1 範囲外（トークナイザ差し替え点のみ記録）。
</domain>

<decisions>
## Implementation Decisions

以下の D-01〜D-16 はこの CONTEXT 内だけの追跡用ラベルであり、既存の決定文は変更していない。見出し・本文の D-2 / D-3 等は元の OpenSpec 参照であり、このローカル識別子とは別である。

### 実行方法と入力（FR-1）
- **D-01:** `python -m wordfreq <file>` はファイル引数ちょうど 1 個を受け取る。UTF-8 として読んで集計結果を出力する。
- **D-02:** 存在しない・開けない・UTF-8 デコード不可 → stderr にエラーメッセージ、exit 1、stdout には結果を出さない。
- **D-03:** ファイル引数 0 個または 2 個以上 → 使い方エラー、stderr、exit 2。
- **D-04:** 空ファイルは結果 0 件（text は出力なし、json は `[]`）で exit 0。

### 件数・形式オプション（FR-2・FR-3）
- **D-05:** `--top N` は 1 以上の整数、既定 10。整数でない・0 以下は exit 2。結果が N 満たなければ全件。
- **D-06:** `--format text|json`、既定 text。text は 1 語 1 行で列書式は design.md D-A の `<count>\t<word>`。json は `{"word": <str>, "count": <int>}` の配列で `json.loads` 可読、順序は text と同一。不正形式は exit 2。

### 切り出し・正規化（D-3）
- **D-07:** 単語は Unicode の単語構成文字（Python `\w`、`re.UNICODE`）の連続する最大長。各トークンに `str.casefold()` を適用。
- **D-08:** 句読点・記号・空白は語に含めない。大文字小文字のみ異なる語は同一視（"Hello hello HELLO" → hello 3）。
- **D-09:** トークナイザは差し替え可能な部品として実装する。日本語は形態素解析せず `\w` ルールの結果が決定論的ならよい。

### 順序の決定論性（FR-4・D-2）
- **D-10:** 出現回数の降順、同回数なら正規化後単語の昇順。同じ入力・同じオプションの出力は決定論的。

### 部品分離と入力元拡張（FR-5・FR-6）
- **D-11:** トークナイザ・集計・入力取得・出力整形を分離した部品構成にする（tasks.md のファイル配置: `wordfreq/tokenizer.py`、`aggregator.py`、`sources.py`（`TextSource` プロトコル + `FileSource` + `InputError`）、`formatters.py`）。
- **D-12:** 解析・集計はテキストを入力取得境界を介してのみ受け取る。各部品は単体で呼んで検証できること。
- **D-13:** 入力元（標準入力・URL）の追加は入力取得境界の実装追加で足りるという構成判断を design.md に記録済み。

### 試験と実行環境（FR-7・FR-8）
- **D-14:** pytest 単体試験をリポジトリ CI の pytest ジョブで通す。試験は spec の全シナリオ（不存在ファイル、空ファイル、引数個数、不正 `--top`/`--format`、同数語の順序、大文字小文字同一視、UTF-8 デコード失敗、JSON 構造、部品単体・境界越し検証）を含む。
- **D-15:** 対象 Python は CI ジョブの CPython 3 の版。バージョン横断互換コードを書かない。ランタイム依存は標準ライブラリのみ（`pyproject.toml` の dev 依存に pytest は可）。
- **D-16:** CI に pytest ジョブが無ければ workflow 変更は人の対応扱い（Bot の権限外）。task 3.3 で有無を確認し、無ければ block 判定の準備をする。

### Claude's Discretion
- 関数・モジュール内部の細部（ argparse の使い方、例外処理の内部構造、テストファイルの分割方法）は承認済み仕様の範囲で実装が決定してよい。
- `pyproject.toml` の最小限の設定内容（ビルドバックエンド選択等）は仕様「最低限のパッケージ設定は許容」の範囲で決定してよい（危険なパスのためレビュー対象になることは想定済み）。

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### 承認済み仕様（原本・Git 上の commit 89725f0 以降に同一内容）
- `openspec/changes/r-5a3b8a3f-wordfreq/proposal.md` — Why / What Changes / 範囲（UIなし、日本語v1範囲外、依存ゼロ）
- `openspec/changes/r-5a3b8a3f-wordfreq/specs/wordfreq-cli/spec.md` — FR-1〜FR-8・D-3 の Requirement と WHEN/THEN シナリオ（受入・検証の正）
- `openspec/changes/r-5a3b8a3f-wordfreq/tasks.md` — task 1.1〜3.3 の実装順（部品内側→外側、各時点で pytest 緑）
- `openspec/changes/r-5a3b8a3f-wordfreq/design.md` — D-A（text 列書式 `<count>\t<word>`）、D-C（exit code 0/1/2 分岐）、D-E（JSON 配列書式）、部品分離と入力元拡張の構成判断

### GSD 計画資料
- `.planning/REQUIREMENTS.md` — REQ-01〜REQ-08（この phase に全紐付け）
- `.planning/ROADMAP.md` — Phase 1 の goal と Requirements 欄
- `.planning/intel/SYNTHESIS.md` — 取込み統合結果
- `.planning/argonauts/r-5a3b8a3f-prd.md` — 結合 PRD（本 CONTEXT の入力）
- `.planning/argonauts/r-5a3b8a3f-learnings.md` — CE learnings-researcher 調査結果（学習 0 件の記録）

</canonical_refs>

<specifics>
## Specific Ideas

- 実装順は部品（内側）から外側で、各 task の終了時点で pytest が通る状態を保つ（tasks.md 冒頭の約束）。
- 検証コマンドは `python -m pytest` と CLI 実起動（`python -m wordfreq <file>` の exit code と出力）を組み合わせる。
- `pyproject.toml` は危険なパス（smart マージ方針）。workflow ファイル変更は Bot 権限外で人の対応扱い。

</specifics>

<deferred>
## Deferred Ideas

- 日本語形態素解析（v1 範囲外。トークナイザ差し替え点だけ残す）
- 標準入力・URL からの入力（入力取得境界の実装追加で対応可能な状態を維持するだけがスコープ）

</deferred>

---

*Phase: 01-wordfreq-cli*
*Context gathered: 2026-11-17 via PRD Express Path*
