# Roadmap: wordfreq CLI

## Overview

依頼 r-5a3b8a3f の承認済みスコープ全体を 1 つの Phase 1 として提供する。stdlib-only の Python パッケージ `wordfreq` を追加し、`python -m wordfreq <file>` で単語の出現頻度を決定論的な並び順・出力形式・exit code 規約で表示できるようにする。切り出し・正規化 / 集計 / 入力取得 / 出力整形の部品分離と入力元拡張境界を確保し、pytest 試験がリポジトリ CI の pytest ジョブで通るところまでが完了条件。PM により本依頼の計画対象は Phase 1 単一と固定済み。

## Phases

**Phase Numbering:**
- Integer phases (1, 2, 3): Planned milestone work
- Decimal phases (2.1, 2.2): Urgent insertions (marked with INSERTED)

Decimal phases appear between their surrounding integers in numeric order.

- [x] **Phase 1: wordfreq CLI** - stdlib-only の wordfreq CLI 全体（実行・オプション・決定論出力・部品分離・試験・CI） (completed 2026-11-17)
- [ ] **Phase 3: wordfreq HTML output**

## Phase Details

### Phase 1: wordfreq CLI
**Goal**: ユーザーは `python -m wordfreq <file>` で、決定論的な並び順と出力形式、exit code 規約を持つ単語頻度集計を stdlib-only の CLI として実行できる
**Depends on**: Nothing (first phase)
**Requirements**: REQ-01, REQ-02, REQ-03, REQ-04, REQ-05, REQ-06, REQ-07, REQ-08
**Success Criteria** (what must be TRUE):
  1. ユーザーは `python -m wordfreq <file>` を実行でき、出現回数の降順（同数は正規化後単語の昇順）に結果が表示され、`--top N`（既定 10、1 以上の整数）で表示件数を変更でき、結果が N 未満なら全件表示される
  2. ユーザーは `--format text|json` で出力を選べる。text は 1 語 1 行（design D-A の `<count>\t<word>`）、json は `{"word": <str>, "count": <int>}` の配列で `json.loads` 可読、結果 0 件は `[]`（json）/ 出力なし（text）
  3. 異常系が規約どおりに観察できる: 不存在・開けない・UTF-8 デコード失敗は stderr + exit 1、ファイル引数個数不正・`--top` 不正・`--format` 不正は stderr + exit 2、空ファイルは 0 件で exit 0。同じ入力・同じオプションの出力は決定論的
  4. tokenizer / aggregator / sources / formatters が部品として分離され、各部品を単体で呼ぶ試験と、集計経路が入力取得境界（`TextSource`）を介してのみテキストを受け取ることを通す境界越し試験が存在する（将来の入力元は境界の実装追加で足りないことが design.md に記録済み）
  5. pytest 試験一式（全 FR のエッジケース含む）がリポジトリ CI の pytest ジョブで通り、ランタイム依存は標準ライブラリのみ（`pyproject.toml` 等の必要最小限の変更で成立する）
**Plans**: 5/5 plans complete; awaiting independent quality CI verification and phase re-verification (REQ-07 Pending)

Plans:
**Wave 1**
- [x] 01-01: TBD

**Wave 2** *(blocked on Wave 1 completion)*
- [x] 01-02-PLAN.md

**Wave 3** *(blocked on Wave 2 completion)*
- [x] 01-03-PLAN.md

**Wave 4** *(blocked on Wave 3 completion)*
- [x] 01-04-PLAN.md

**Wave 5** *(blocked on Wave 4 completion)*
- [x] 01-05-PLAN.md

## Progress

**Execution Order:**
Phases execute in numeric order: 1

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. wordfreq CLI | 5/5 | Complete    | 2026-11-17 |

### Phase 3: wordfreq HTML output

**Goal:** 承認済み依頼 r-50053edc の自己完結HTMLを安全にstdoutへ出し、全形式の同数順を初出順へ変更し、通常幅/320 CSS pxの独立ブラウザ証拠で受入条件を追跡できる。
**Requirements**: REQ-09, REQ-10, REQ-11, REQ-12, REQ-13, REQ-14
**UI hint:** yes
**Success Criteria:**
  1. AC1: UTF-8静的HTMLは順位・単語・回数の3列、内包CSSのみ、外部参照・通信試行なし。
  2. AC2: 表より上にbasenameのみ、top前の総出現回数。top 1/2/10で総数6、別入力top 2で総数7。
  3. AC3: 全形式で回数降順・同数時正規化後初出順。旧語昇順からの意図した変更を記録する。
  4. AC4: 明るい背景のみ、切替なし、1始まり連番。長語・長basenameが通常幅と320 CSS pxで全文可読。
  5. AC5: 特殊文字を安全に表示し、既存抽出/casefold/入力/エラー/text/json構造を不要に変更しない。
  6. AC6: 品質が対象headでCLIを独立再実行し、raw文字Range・全画像閲覧・失敗を含む通信試行をAC別証拠にする。CI・依存追加なし。
**Approval / conflict:** t_13dfdc77 run83 approved。E.7の承認済み変更用新phase経路を採用。Phase 1の履歴は保存し、REQ-11が同数時語昇順を置換する。参照: .planning/INGEST-CONFLICTS.md。Phase 2の既存ディレクトリは別依頼の残存成果であり今回の入力・実装根拠にしない。公式phase.addが返した番号3を使用する。
**Depends on:** Phase 1
**Plans:** 1/4 plans executed

Plans:
**Wave 1**
- [x] 03-01-PLAN.md — 共通初出順と安全なHTML CLI tracer

**Wave 2** *(blocked on Wave 1 completion)*
- [ ] 03-02-PLAN.md — 入力・形式・エラー・表示状態の回帰

**Wave 3** *(blocked on Wave 2 completion)*
- [ ] 03-03-PLAN.md — 実CLI/ブラウザ/raw Range/通信観測

**Wave 4** *(blocked on Wave 3 completion)*
- [ ] 03-04-PLAN.md — fail-closed画像確認と独立品質手順
