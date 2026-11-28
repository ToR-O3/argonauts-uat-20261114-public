# Roadmap: wordfreq CLI

## Overview

依頼 r-5a3b8a3f の承認済みスコープ全体を 1 つの Phase 1 として提供する。stdlib-only の Python パッケージ `wordfreq` を追加し、`python -m wordfreq <file>` で単語の出現頻度を決定論的な並び順・出力形式・exit code 規約で表示できるようにする。切り出し・正規化 / 集計 / 入力取得 / 出力整形の部品分離と入力元拡張境界を確保し、pytest 試験がリポジトリ CI の pytest ジョブで通るところまでが完了条件。PM により本依頼の計画対象は Phase 1 単一と固定済み。

## Phases

**Phase Numbering:**
- Integer phases (1, 2, 3): Planned milestone work
- Decimal phases (2.1, 2.2): Urgent insertions (marked with INSERTED)

Decimal phases appear between their surrounding integers in numeric order.

- [x] **Phase 1: wordfreq CLI** - stdlib-only の wordfreq CLI 全体（実行・オプション・決定論出力・部品分離・試験・CI） (completed 2026-11-17)
- [x] **Phase 3: wordfreq HTML output** (completed 2026-11-18)
- [x] **Phase 4: wordfreq min-count** (completed 2026-11-18)
- [x] **Phase 5: README verification A** (completed 2026-11-22)
- [ ] **Phase 7: Project description UAT**
- [x] **Phase 8: wordfreq exclude** (completed 2026-11-29)

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
**Plans:** 6/6 plans complete; 03-05/03-06 gap closure planned (G1/G2), independent final-head quality pending

Plans:
**Wave 1**
- [x] 03-01-PLAN.md — 共通初出順と安全なHTML CLI tracer

**Wave 2** *(blocked on Wave 1 completion)*
- [x] 03-02-PLAN.md — 入力・形式・エラー・表示状態の回帰

**Wave 3** *(blocked on Wave 2 completion)*
- [x] 03-03-PLAN.md — 実CLI/ブラウザ/raw Range/通信観測

**Wave 4** *(blocked on Wave 3 completion)*
- [x] 03-04-PLAN.md — fail-closed画像確認と独立品質手順

**Wave 5** *(blocked on Wave 4 completion)*
- [x] 03-05-PLAN.md — G1 全view/derived/ledger最終整合と失敗時unverified

**Wave 6** *(blocked on Wave 5 completion)*
- [x] 03-06-PLAN.md — G2 CI環境独立試験、provenance/actor、独立品質とOpenSpec記録循環

### Phase 4: wordfreq min-count

**Goal:** 承認済み依頼r-e476c11dのmin-countを全3形式へ追加し、正規化後の閾値除外→top・元HTML総数・既定互換・見た目/安全性を維持し、独立品質の読める証拠でAC1〜AC7を追跡できる。
**Requirements**: REQ-15, REQ-16, REQ-17, REQ-18, REQ-19, REQ-20, REQ-21
**Depends on:** Phase 3
**UI hint:** yes — 既存HTMLの見た目を維持する。新UI/スタイル変更はない。
**Success Criteria:**
  1. AC1/AC3: 全形式で正整数の閾値、未満除外/ちょうど保持、空/全除外、不正値/欠落の入力取得前exit2を試験で固定。
  2. AC2/AC4: 製品変更前baselineと未指定/明示1のstdout一致。casefold合算・同数初出順・独立topを維持し、除外→topをソースでも確認。
  3. AC5: HTML総数は両絞込み前。全除外でも元総数を保持し既存formatter/CSS/文言を変えない。
  4. AC6: 全pytestと対象headの独立CLI/ブラウザ1280×900・320×900 DPR1、画像の実閲覧と比較・原本の標準配送がAC別に追跡できる。
  5. AC7: CI/依存/見た目の変更なし、READMEは付随最小説明のみ、既存入力・安全性・出力契約を維持。
**Approval:** t_a438e6b2 run140 approved。要求追加のみのmerge、衝突0。Phase1/3のstale検証は今回の実装範囲へ混ぜず表示する。公式phase.addの番号4を使用。
**Plans:** 4/4 plans complete

Plans:
**Wave 1**
- [x] 04-01-PLAN.md — Wave 1 (2 tasks): driver/validator browser-free検証・正式commit→変更前baseline一度採取/封印/read-only hard gate

**Wave 2** *(blocked on Wave 1 completion)*
- [x] 04-02-PLAN.md — Wave 2 (depends 04-01): 引数と全形式閾値/空結果の先行TDD

**Wave 3** *(blocked on Wave 2 completion)*
- [x] 04-03-PLAN.md — Wave 3 (depends 04-02, 3 tasks): capture/validator→live/finalizeのbrowser-free検証・正式commit→clean head一度採取/read-only確認

**Wave 4** *(blocked on Wave 3 completion)*
- [x] 04-04-PLAN.md — Wave 4 (depends 04-03, 2 tasks): 一度限りBuilder統合/read-only確認→品質runbook/原本配送。full E2Eは必須高遅延gate、最終head品質は別主体

### Phase 5: README verification A

**Goal:** 承認済み依頼r-8ac79dafの指定検証A行をREADME末尾に正確に1行追加し、既存内容・改行・コード・試験の不変を既存CLIと品質の読める証拠で確認できる。
**Requirements**: REQ-22, REQ-23, REQ-24
**UI hint:** no — 文書内容のみ。画面やHTML出力は変更しない。
**Success Criteria:**
  1. READMEの独立した最終行が `検証A: v1.12 の通しの確かめ（2026-11-22）` と完全一致し、かぎ括弧・句点・後続空行なし。
  2. 追記以外のREADME既存内容・順序・改行形式を保持し、不要空行・削除・書換えなし。
  3. 利用者向け全差分は当該1行のみ。コード・試験不変、工程文書を別分類し、品質が対象headのCLI結果を文字文書へ記録・添付する。
**Approval:** t_327d2f8f run7 approved、source t_bdf6acb4 run6、OpenSpec r-8ac79daf-readme-verification-a。merge追加のみ・衝突0。公式phase.addの番号5を採用。旧phaseのstale検証を今回の範囲へ混ぜない。文言は通し検証の実施・合格の認定ではない。
**Depends on:** Phase 4
**Plans:** 1/1 plans complete

Plans:
- [x] 05-01-PLAN.md — 2 sequential tasks: README末尾追記tracerとC1-C4（OpenSpec1.1）→依頼全差分C5-C6・文字証拠/独立品質handoff（OpenSpec2.1）

### Phase 7: Project description UAT

**Goal:** 承認済み依頼r-cf2eeaabのdescriptionを完成値厳密一致で新規追加し、他製品・既存TOMLの意味とバイトを保持し、独立品質の文字証拠でACを確認できる。
**Requirements**: REQ-25, REQ-26, REQ-27
**Depends on:** Phase 5
**UI hint:** no — 説明文メタデータのみ。画面・実行時動作の変更なし。
**Approval:** t_8a187e42 approved、source t_62c33f31 run59。mergeは要求追加のみ・衝突0。公式phase.addの返した7を使用。過去phaseのstale検証や残存ディレクトリは今回へ混ぜない。
**Success Criteria:**
  1. [project].descriptionの解析値が厳密に `argonauts-uat public (UAT)`。さらなる印なし。
  2. 起点c572613から製品差分はdescription1行だけ。他の解析項目・既存バイト・他製品は不変。
  3. 工程配下の検証で欠落RED→追加後GREEN、TOML正常解析を記録。品質が対象headで独立実行しVERIFICATION.md等の文字原本を添付する。
**Plans:** 1/1 plans executed

Plans:
- [x] 07-01-PLAN.md — Wave 1、2 sequential tasks: 工程検証tracer・判別力GREEN/実製品欠落RED（OpenSpec1.1）→description1行追加・同一検証GREEN・AC別文字証拠/独立品質handoff（OpenSpec1.2）

### Phase 8: wordfreq exclude

**Goal:** 承認済み--exclude FILEを全形式へ追加し、Unicode行検証・除外先行の失敗処理・元HTML総数・未指定互換を試験と独立品質の文字証拠で確かめられる。
**Requirements**: REQ-28, REQ-29, REQ-30, REQ-31, REQ-32, REQ-33
**Depends on:** Phase 7
**UI hint:** yes — 既存HTMLの表示と安全性を維持する。見た目変更は範囲外。
**Approval:** t_91b92aed approved head17648fc; merge adds REQ-28..33 only. PM t_9da1db1e separates architecture from synthesis but retains direct planner reference. 6-doc resynthesis has 0 blockers/variants. Prior stale verification and Phase7 debt remain historical, not this request's implementation scope.
**Success Criteria:**
  1. 全3形式の指定語除外→min-count→安定初出順→topとHTML元総数を直接試験できる。
  2. trim/改行/Unicode fullmatch後casefoldと全不正例、全読込み失敗exit2/元行番号/空stdout/本文取得0回、引数検査先行と本文exit1が確認できる。
  3. help/README実行例と79d83ba版との未指定バイト互換、全既存試験、入力不変と範囲外変更なしを確かめられる。
  4. 品質が対象headで独立実行し、VERIFICATION.mdとCLI等の文字原本を添付する。画像確認があれば枚数/内容/結果を文書化し、PMに画像/圧縮ファイル閲覧を求めない。
**Plans:** 3/3 plans complete

Plans:
**Wave 1**
- [x] 08-01-PLAN.md — tracer・Unicode行文法、OpenSpec2.1/2.2

**Wave 2** *(blocked on Wave 1 completion)*
- [x] 08-02-PLAN.md — 全失敗/取得優先・全形式選別/空状態、OpenSpec2.1/2.2

**Wave 3** *(blocked on Wave 2 completion)*
- [x] 08-03-PLAN.md — 固定版互換/説明/実原本・後続品質への引渡し、OpenSpec3.1/3.2前提（独立品質は後続カード）

## Backlog

### Phase 999.1: Follow-up — Phase 8 deferred UAT follow-up: Test 2 (BACKLOG)

**Goal:** Resolve the UAT checkpoint deferred during Phase 8 verification
**Source phase:** 8
**Deferred at:** 2026-11-29 during /gsd-verify-work 8 session completion
**Follow-ups:**
- [ ] Test 2: P-08-01 の追加の人による確認（flagged-unverified を保持。PM判断 t_bdb96733） (deferred 2026-11-29)

### Phase 999.2: Follow-up — Phase 8 deferred UAT follow-up: Test 3 (BACKLOG)

**Goal:** Resolve the UAT checkpoint deferred during Phase 8 verification
**Source phase:** 8
**Deferred at:** 2026-11-29 during /gsd-verify-work 8 session completion
**Follow-ups:**
- [ ] Test 3: P-08-02 の追加の人による確認（flagged-unverified を保持。PM判断 t_bdb96733） (deferred 2026-11-29)

### Phase 999.3: Follow-up — Phase 8 deferred UAT follow-up: Test 4 (BACKLOG)

**Goal:** Resolve the UAT checkpoint deferred during Phase 8 verification
**Source phase:** 8
**Deferred at:** 2026-11-29 during /gsd-verify-work 8 session completion
**Follow-ups:**
- [ ] Test 4: 日本語フォントのある環境で --format html の日本語描画を確認（未確認のまま。PM判断 t_bdb96733） (deferred 2026-11-29)
