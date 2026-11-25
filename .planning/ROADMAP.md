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
- [x] **Phase 5: README validation B** (completed 2026-11-22)
- [x] **Phase 7: wordfreq max-count** (completed 2026-11-25)
- [ ] **Phase 8: wordfreq HTML displayed types**

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

### Phase 5: README validation B

**Goal:** 承認済み依頼r-215b4390に従いREADME.mdの既存内容を保持し、指定行を独立した最終行として1回だけ追加する。製品差分は指定1行のみでコード・試験は変更しない。
**Requirements**: REQ-22
**UI hint:** no — 文書の1行追記のみ。画面やHTML出力を変更しない。
**Success Criteria:**
  1. 最終行が「検証B: v1.12 の通しの確かめ（2026-11-22）」と完全一致し、出現1回。
  2. 変更前READMEの全内容を保持し、差分は指定行1行追加・削除0行のみ。
  3. 工程記録を除く製品変更はREADME.mdのみ。コード・試験・検証機能や試験ファイルの新設なし。
  4. 品質がCLIの結果・検証対象headを文字の証拠文書とVERIFICATION.mdに記録・標準添付し、PMがread_fileで判断できる。
**Approval:** t_dafbe600 run5 approved。6文書のmergeは要求追加のみ、衝突0。旧phaseのstale検証は今回の範囲外。公式phase.addが返した番号5を使用。
**Depends on:** Phase 4
**Plans:** 1/1 plans complete

Plans:
- [x] 05-01-PLAN.md — 指定最終行1回の局所追記と固定基底CLI照合（Wave 1、単一tracer）

### Phase 7: wordfreq max-count

**Goal:** 承認済み依頼r-d4bcda40の整数--max-countを全3形式へ追加し、包含上限とminの積集合をtop前に適用する。省略互換・元Counter/HTML総数・安全性を保ち、追加/既存試験と独立CLI/HTML検証の読める証拠で全受入条件を追跡できる。
**Requirements**: REQ-23, REQ-24, REQ-25, REQ-26, REQ-27, REQ-28
**Depends on:** Phase 5
**UI hint:** yes — 既存HTMLの表示契約を維持し、通常幅/狭幅を検証。新UI/スタイル変更なし。
**Approval:** t_ef216d95 approved、t_fa8e2c5f completed run119の5文書mergeは要求追加のみ、衝突0。公式phase.addの番号7を使用（過去ディレクトリを再利用しない）。過去phaseのstale検証は別スコープとして残す。
**Success Criteria:**
  1. 整数全域/省略None、両端包含、min併用、共通filter-before-top、全形式の固定期待値が一致。
  2. 正常空集合exit0・有効上限で入力失敗exit1・欠落/非整数と既存不正min/topは入力取得前exit2。
  3. 変更前の省略期待値、元Counter/元総数12、Unicode/casefold/初出順/formatter API/安全性/見た目を保持。
  4. 先行RED/GREENと全pytest成功、README例1つを実CLIで検証。依存/CI/無関係変更なし。
  5. 品質が対象headで独立CLI/通常幅・狭幅HTML/全画像閲覧/通信観測を実施しVERIFICATION.mdとCLI/CI文字証拠に受入条件別結果と閲覧枚数/内容/結果を記録・添付。PMへ画像/圧縮ファイル閲覧を要求しない。
**Plans:** 3/3 plans complete

Plans:
**Wave 1**
- [x] 07-01-PLAN.md — Wave 1: 変更前oracle/両幅画像を封印しmax-count全形式tracerと包含・内部順序・固定bytesを検証（2 tasks）

**Wave 2** *(blocked on Wave 1 completion)*
- [x] 07-02-PLAN.md — Wave 2（depends 07-01）: 正常空/usage/入力失敗の三出口とREADME指定1例の先行試験（2 tasks）

**Wave 3** *(blocked on Wave 2 completion)*
- [x] 07-03-PLAN.md — Wave 3（depends 07-02）: max専用証拠経路・全suite/scope・独立品質2.2のphase verification引継ぎ（2 tasks）

### Phase 8: wordfreq HTML displayed types

**Goal:** 承認済みr-6ae2cbf2に従いHTML表上の総出現回数の横へ最終表示語種類数を追加し、text/jsonと元総数・安全性を維持する。試験先行・README説明1行・独立CLI/通常幅/狭幅ブラウザ確認の文字証拠で全条件を追跡する。
**Requirements**: REQ-29, REQ-30, REQ-31
**UI hint:** yes — 既存ライトテーマと表を継承し、メタ情報表示追加と必要最小レイアウトだけ変更する。
**Approval / conflict:** t_e811c751 run164 approved。取込みのBLOCKERS 2件は今回承認済みのHTMLバイト互換例外。E.7/F.3の新phase経路で公式phase.addが返した8を使う。旧Phase4/7のCONTEXT・封印baseline・完了履歴は保持。今回表示Nと必要最小レイアウトのみ例外、text/json固定期待値と安全性検査を緩めない。過去stale検証/snapshot scope gateと今回の合否を分ける。参照: .planning/INGEST-CONFLICTS.md（添付107）。
**Success Criteria:**
  1. 通常/top/既定top10/min/max併用/Unicode/空・全除外のHTML表示Nが最終データ行数に一致し、総出現回数は元counts和のまま。
  2. text/jsonは同一入力・オプションで全バイト不変。封印baselineは上書きせずHTML今回用期待値または明示変換で許可差分だけ扱い、既存escape・basename・静的安全性を維持。
  3. RED→GREENと全pytest成功を記録し、READMEのHTML説明に1行追加する。依存/CI/権限/外部送信/移行なし。
  4. 品質が対象headでCLI・1280×900/320×900 DPR1ブラウザを独立実行し横配置と可読性・安全性を確認。VERIFICATION.mdとCLI/CI文字証拠へAC別結果、閲覧画像数/内容/結果を記録・標準添付する。PMへ画像や圧縮ファイルを開くことを要求しない。
**Depends on:** Phase 7
**Plans:** 1/3 plans executed

Plans:
**Wave 1**
- [x] 08-01-PLAN.md — Wave 1: 製品編集前の実CLI/両幅画像を保全し表示N全ケースの先行RED（2 tasks）

**Wave 2** *(blocked on Wave 1 completion)*
- [ ] 08-02-PLAN.md — Wave 2（depends 08-01）: 最終pairs表示・限定HTML期待値整合・README1行・全pytest GREEN（2 tasks）

**Wave 3** *(blocked on Wave 2 completion)*
- [ ] 08-03-PLAN.md — Wave 3（depends 08-02）: 実行可能な現行ブラウザ検証seamをBuilderがexerciseし独立品質OpenSpec2.1へ引継ぎ（2 tasks）
