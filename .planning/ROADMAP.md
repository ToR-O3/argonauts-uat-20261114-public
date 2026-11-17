# Roadmap: wordfreq CLI

## Overview

依頼 r-5a3b8a3f の承認済みスコープ全体を 1 つの Phase 1 として提供する。stdlib-only の Python パッケージ `wordfreq` を追加し、`python -m wordfreq <file>` で単語の出現頻度を決定論的な並び順・出力形式・exit code 規約で表示できるようにする。切り出し・正規化 / 集計 / 入力取得 / 出力整形の部品分離と入力元拡張境界を確保し、pytest 試験がリポジトリ CI の pytest ジョブで通るところまでが完了条件。PM により本依頼の計画対象は Phase 1 単一と固定済み。

## Phases

**Phase Numbering:**
- Integer phases (1, 2, 3): Planned milestone work
- Decimal phases (2.1, 2.2): Urgent insertions (marked with INSERTED)

Decimal phases appear between their surrounding integers in numeric order.

- [x] **Phase 1: wordfreq CLI** - stdlib-only の wordfreq CLI 全体（実行・オプション・決定論出力・部品分離・試験・CI） (completed 2026-11-17)
- [ ] **Phase 2: wordfreq HTML output**

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

### Phase 2: wordfreq HTML output

**Goal:** 利用者がwordfreqの結果を安全な自己完結HTMLへ保存し、スマートフォンでも明るい3列表で読める。全形式の同数順を承認済み初出順へ変更し、既存CLI回帰と独立ブラウザ証跡を確保する（r-5c041156）。
**Requirements**: REQ-09, REQ-10, REQ-11, REQ-12, REQ-13, REQ-14
**Success Criteria**:
1. --format html は単一文書をstdoutへ出し、表前にbasenameとtop前総数を表示する。top1のZoo例は総数5・1/zoo/2、空入力は総数0と3見出しのみ。
2. 明るい背景、順位/単語/回数、scope=col、1始まり表示行連番を320/375/1280pxで200文字語・長い日本語名・空表でも欠落/重なり/横overflowなく表示する。
3. 全形式で頻度降順・正規化初出順・sort後topを守り、Unicode/casefold/複数hashseedを含む試験が通る。text/jsonの構造は不変。
4. 純粋formatterの1回escapeと空白/CR/CRLF保持、悪意ある名前の不実行、外部request0を、実HTML/画像/DOM-layout/network/ブラウザ名版/viewportで実証する。
5. 全pytest・既存CLI/入力境界/エラー/入力不変を維持し、別ファイル保存・共有露出・同一パスリダイレクト禁止を説明する。CI/依存変更なし、手段不足を未検証として返す。

Phase 1の語昇順/text-json/UIなしは出荷時点の履歴。今回の現在契約はPhase 2と承認済みOpenSpecが優先。既存要求の変更を含むためingest mergeは適用せず、E.7/10.4により公式phase.addで追加。矛盾原本: .planning/INGEST-CONFLICTS.md。
**Depends on:** Phase 1
**Plans:** 3 plans（同じ依頼branchへ直列に積む）

Plans:
**Wave 1**
- [ ] 02-01-PLAN.md — 安全なCLI→保存HTML tracerと全形式初出順（2 tasks、wave 1）

**Wave 2** *(blocked on Wave 1 completion)*
- [ ] 02-02-PLAN.md — 全形式/文字忠実性/入力境界回帰と安全な保存説明（3 tasks、wave 2、depends 02-01）

**Wave 3** *(blocked on Wave 2 completion)*
- [ ] 02-03-PLAN.md — 既存Node/Chromium実browser証跡と独立品質handoff（3 tasks、wave 3、depends 02-02）
