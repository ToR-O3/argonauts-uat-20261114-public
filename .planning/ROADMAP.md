# Roadmap: wordfreq CLI

## Overview

依頼 r-5a3b8a3f の承認済みスコープ全体を 1 つの Phase 1 として提供する。stdlib-only の Python パッケージ `wordfreq` を追加し、`python -m wordfreq <file>` で単語の出現頻度を決定論的な並び順・出力形式・exit code 規約で表示できるようにする。切り出し・正規化 / 集計 / 入力取得 / 出力整形の部品分離と入力元拡張境界を確保し、pytest 試験がリポジトリ CI の pytest ジョブで通るところまでが完了条件。PM により本依頼の計画対象は Phase 1 単一と固定済み。

## Phases

**Phase Numbering:**
- Integer phases (1, 2, 3): Planned milestone work
- Decimal phases (2.1, 2.2): Urgent insertions (marked with INSERTED)

Decimal phases appear between their surrounding integers in numeric order.

- [ ] **Phase 1: wordfreq CLI** - stdlib-only の wordfreq CLI 全体（実行・オプション・決定論出力・部品分離・試験・CI）

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
**Plans**: 2/4 plans executed

Plans:
- [x] 01-02-PLAN.md
- [ ] 01-03-PLAN.md
- [ ] 01-04-PLAN.md
- [x] 01-01: TBD

## Progress

**Execution Order:**
Phases execute in numeric order: 1

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. wordfreq CLI | 2/4 | In Progress | - |
