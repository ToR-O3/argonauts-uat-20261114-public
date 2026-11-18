# wordfreq CLI

## What This Is

テキストファイルを読んで単語の出現回数を多い順に表示する小さなコマンドラインツール。`python -m wordfreq <file>` で実行し、表示件数は `--top N`（既定 10）、出力形式は `--format text|json`（既定 text）。依頼 r-5a3b8a3f の成果物として repository `ToR-O3/argonauts-uat-20261114-public`（基準 branch: main）に stdlib-only の Python パッケージ `wordfreq` を追加する。主利用者はこの repository を使うエンジニア（依頼者自身）。画面（UI）は作らない。

## Core Value

正規化・並び順・出力形式・エラー出口の決定論（テストで固定できる標準化）と、入力元（標準入力・URL）を後から追加できる構成の明確さ。価値は性能ではない。

## Project Facts

- **依頼番号**: r-5a3b8a3f
- **GitHub repository**: ToR-O3/argonauts-uat-20261114-public
- **基準 branch**: main
- **成果物**: stdlib-only Python の wordfreq CLI（単語出現頻度集計。ファイル/stdin入力、大文字小文字無視、決定論的出力、exit code 規約）
- **マイルストーン名**: 未定

## Requirements

### Validated

<!-- Shipped and confirmed valuable. -->

- ✓ REQ-15..REQ-21 (`--min-count`, r-e476c11d) — Phase 4 (verified at afaa56f; UAT passed 2026-11-18; REQ-17 limited to existing single-shot CLI guarantees by human decision)

### Active

- [ ] **REQ-01**: `python -m wordfreq <file>` がファイル引数ちょうど 1 個を受け取り、UTF-8 で読んで頻度集計を出力する（不存在・開けない・デコード失敗は stderr + exit 1、引数個数不正は exit 2、空ファイルは 0 件で exit 0）
- [ ] **REQ-02**: `--top N` で表示件数を指定できる（既定 10、N は 1 以上の整数、不正値は exit 2、結果が N 未満なら全件出力）
- [ ] **REQ-03**: `--format text|json` で出力形式を指定できる（既定 text、不正値は exit 2。text は 1 語 1 行、json は `{"word": <str>, "count": <int>}` の配列で `json.loads` 可読、0 件は `[]`/出力なし）
- [ ] **REQ-04**: 出力は常に決定論的（出現回数の降順、同数は正規化後単語の昇順）
- [ ] **REQ-05**: 切り出し・正規化 / 集計 / 入力取得 / 出力整形の部品が分離し、各部品は単体で呼んで検証でき対応する単体試験を持つ
- [ ] **REQ-06**: 入力取得は解析・集計から境界として分離され、将来の入力元（標準入力・URL）は境界の実装追加で足りる（構成判断を design.md に記録）
- [ ] **REQ-07**: pytest による単体試験があり、リポジトリ CI の pytest ジョブで通る（全 FR のエッジケースを含む）
- [ ] **REQ-08**: ランタイム依存は標準ライブラリのみ（依存追加は人の承認を要する範囲変更）

### Out of Scope

- GUI・画面 — CLI ツールであり UI は作らない（Brief・proposal 明記）
- 標準入力・URL 入力の実装 — v1 は入力取得境界の確保まで（WF-06/D-B）
- 日本語形態素解析 — D-1 により v1 範囲外。トークナイザの差し替え点だけ残す
- 非 stdlib のランタイム依存追加 — FR-8。必要になったら人の承認の上で範囲変更として扱う
- PyPI 公開 — パッケージ設定は repo 内 `python -m` 実行に必要最小限（D-F）
- 性能最適化・ストリーミング・並列化 — design.md Non-Goals

## Context

- 依頼 r-5a3b8a3f の OpenSpec 変更 `r-5a3b8a3f-wordfreq`（proposal/spec/tasks/design が承認済み唯一の情報源）。design.md が text 列書式 `<count>\t<word>`（D-A）、exit code 分岐（D-C）、JSON 出力 `ensure_ascii=True` + 改行 1 つ（D-E）、4 部品分割と依存方向（D-A）、入力元拡張の構成判断（D-B）を決定済み。
- 実装順は部品（内側）から外側（tasks.md 1.1→3.3）: tokenizer → aggregator → sources → formatters → 境界越し試験 → `__main__` → `pyproject.toml` → CI 確認。各 task の時点で pytest が通る状態を保つ。
- 対抗案は即席パイプライン（`sort | uniq -c | sort -rn`）、既存 PyPI パッケージ、何もしない。即席運用のコスト記述は仮説（A-4）。ローカル名 `wordfreq` と同名 PyPI パッケージの取り違えは `python -m` 実行範囲では問題なし（A-5）。
- 既存コードへの影響なし（新ディレクトリ `wordfreq/` と `tests/` の追加のみ）。

## Constraints

- **Dependencies**: ランタイム依存ゼロ（標準ライブラリのみ）— FR-8。依存追加は人の承認を要する範囲変更
- **Process**: CI workflow ファイル変更は Bot 権限外（人の対応扱い）— CI に pytest ジョブが無ければ block して人に委ねる（proposal Impact 済み）
- **Dangerous paths**: `pyproject.toml` 等のパッケージ設定ファイルは smart マージ方針で人の承認対象になり得る — 変更は 1 ファイルに集約し必要最小限に留める
- **Python 版**: 対象は CI ジョブの CPython 3 の版（版番号は CI 設定が持つ）— バージョン横断互換コードは書かない
- **Exit codes**: 0 正常 / 1 環境エラー（InputError）/ 2 使い方エラー（argparse）— D-4/D-C

## Key Decisions

<!-- Decisions that constrain future work. Add throughout project lifecycle. -->

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| D-1: 空白で区切られない言語（日本語等）は v1 対象外。トークナイザは差し替え可能部品に | 範囲を絞り決定余地を残す | — Pending |
| D-2: 並び順は回数降順、同数は正規化後単語の昇順 | 決定論的で試験可能な挙動 | — Pending |
| D-3: 抽出は Unicode `\w` 連続最大長 + `str.casefold()` 正規化 | テストで固定できる定義 | — Pending |
| D-4: exit code は 0 正常 / 2 使い方エラー / 1 環境エラー | 標準的 CLI 規約（argparse と一致） | — Pending |
| D-A: `wordfreq/` を tokenizer/aggregator/sources/formatters の 4 部品 + `__main__` に分割、依存方向は一方向 | 依頼が部品分離を明示的に要求 | — Pending |
| D-B: 入力元追加は `sources.py` の実装追加 + `__main__` の引数分岐だけに収める | 拡張境界を試験で担保（aggregator 系試験は FileSource 非経由） | — Pending |
| D-E: JSON は `[{"word": w, "count": c}]`、`ensure_ascii=True` + 改行 1 つ、0 件は `[]` | spec 固定のキー名と機械可読性 | — Pending |

---
*Last updated: 2026-11-18 after Phase 4*
