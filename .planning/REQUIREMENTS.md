# Requirements: wordfreq CLI

**Defined:** 2026-11-17
**Core Value:** 正規化・並び順・出力形式・エラー出口の決定論（テストで固定できる標準化）と、入力元を後から追加できる構成の明確さ。価値は性能ではない。

Source: 依頼 r-5a3b8a3f の承認済み OpenSpec 変更 `r-5a3b8a3f-wordfreq`（specs/wordfreq-cli/spec.md FR-1〜FR-8、design.md D-A〜D-F）と PRD/Brief（_bmad-output/initiative-r-5a3b8a3f/）。intel/requirements.md の 8 要件を REQ-01〜REQ-08 として採用。

## v1 Requirements

Requirements for initial release. Each maps to roadmap phases.

### CLI 実行とオプション

- [x] **REQ-01**: `python -m wordfreq <file>` はファイル引数ちょうど 1 個を受け取り、そのファイルを UTF-8 として読んで頻度集計の結果を出力する。ファイルが存在しない・開けない・UTF-8 としてデコードできない場合はエラーメッセージを stderr に出して exit 1。ファイル引数が 0 個または 2 個以上は使い方エラー（stderr + exit 2）。空ファイルは結果 0 件として exit 0（FR-1、WF-01/WF-08）
- [x] **REQ-02**: `--top N` は表示する件数を指定する。既定値は 10。N は 1 以上の整数でなければならず、それ以外の値（整数でない、0 以下）は使い方エラー（exit 2）。結果の種類数が N より少ない場合は全件を出力する（FR-2、WF-02）
- [x] **REQ-03**: `--format text|json` は出力形式を指定する。既定は text。text は 1 語 1 行で単語と回数を読むことのできる形式（正確な列書式は design.md D-A の `<count>\t<word>`）。json は `{"word": <str>, "count": <int>}` のオブジェクト配列で REQ-04 の並び順と一致し、`json.loads` で機械可読。結果 0 件のとき json は `[]`、text は出力なし。不正な形式指定は使い方エラー（exit 2）（FR-3、WF-03）

### 出力の決定論

- [x] **REQ-04**: 出力は常に出現回数の降順、回数が同じ単語は正規化後単語の昇順に並び、同じ入力ファイルと同じオプションでの実行出力は決定論的である（FR-4・D-2、WF-05）

### 部品分離と拡張境界

- [x] **REQ-05**: 切り出し・正規化（Unicode `\w` 連続最大長抽出 + `str.casefold()`、句読点・記号・空白は語に含めない、大文字小文字のみが異なる単語は同一視）を行う部品と、集計・出力整形を行う部品を分離する。各部品はそれ単体で呼んで検証でき、対応する単体試験を持つ（FR-5・D-3、WF-04）
- [x] **REQ-06**: テキストを得る入力取得は解析・集計から境界として分離し、v1 のファイル入力もその境界の背後で動く。解析・集計が入力取得境界を介してのみテキストを受け取る境界越し試験を持つ。入力元（標準入力・URL）の追加は入力取得境界の実装追加で足りるという構成判断を design.md に記録する（FR-6・D-B、WF-06）

### 試験・実行環境・依存

- [x] **REQ-07**: pytest による単体試験を用意し、リポジトリの CI の pytest 実行ジョブで通る。試験は REQ-01〜REQ-06 のシナリオ（不存在ファイル、空ファイル、ファイル引数個数、不正な `--top`・`--format`、同数語の順序、大文字小文字の同一視、UTF-8 デコード失敗、JSON 構造、部品単体・境界越し検証）を含む。対象 Python は当該 CI ジョブの CPython 3 の版とし、バージョン横断互換コードは書かない（FR-7・WF-07）
- [x] **REQ-08**: ランタイム依存は標準ライブラリのみ。依存追加が必要になる場合は人の承認を要する範囲変更として扱う。パッケージ化に最低限必要な設定ファイル（`pyproject.toml` 等）の変更は許容するが、smart マージ方針で人の承認対象になり得ることを前提に必要最小限に留める（FR-8、Brief A-5、D-F）

## r-50053edc Requirements (Phase 3)

Source: t_13dfdc77 run83 approved、`r-50053edc-wordfreq-html` proposal/spec/tasksとBMAD PRD。E.7新phase分岐。上のv1は当時の完了履歴として保持し、現在の同数時契約はREQ-11がREQ-04/D-2/D-10を置換する。静的HTMLは旧「GUI・画面なし」のスコープを今回だけ拡張する。旧入力元拡張は今回も対象外。

- [x] **REQ-09**: AC1: --format htmlがstdoutにUTF-8の自己完結静的HTML1枚を出す。順位・単語・回数の表、内包CSSのみ、script・外部参照・外部通信試行なし。
- [x] **REQ-10**: AC2: 表より上にbasenameのみ、top適用前総出現回数。title/属性を含む全HTMLにディレクトリ情報なし。入力例のtop 1/2/10でも総数6、別頻度入力top 2でも総数7、空は0行/総数0。
- [x] **REQ-11**: AC3: 回数降順・同数時正規化後初出順をtext/json/html共通にしてからtop制限。旧語昇順の意図した互換性変更を文書・試験に反映する。
- [x] **REQ-12**: AC4: 明るい背景のみ、切替なし、1始まり表示行連番。通常幅と320 CSS pxで長い語・basenameを省略せず読める。文字Range原本を補正せず残し、横収まり・切取り祖先・非重複・全画像可読性で判断。自身の厳格な縦包含は必須にしない。
- [x] **REQ-13**: AC5: 単語と有効なbasenameの特殊文字をescapeして安全に表示。Unicode抽出/casefold/入力境界/エラー/既定top10/既存text-json構造を同数順以外に不要に変えない。空・不正値・読込・decode失敗を回帰試験する。
- [x] **REQ-14**: AC6: 自動試験と品質による対象headでの実CLI独立再生成・ブラウザ確認。空/通常/top/長文/注入候補、入力原本・コマンド・exit/stdout/stderr・期待値・HTML・browser/viewport・raw Range・全画像の閲覧・失敗試行を含む通信観測をAC別保存/添付。未実施を合格としない。CI・依存追加・生成日時・テーマ切替・対話操作・サーバーなし。

| Requirement | Phase | Status |
|-------------|-------|--------|
| REQ-09 | Phase 3 | Pending |
| REQ-10 | Phase 3 | Pending |
| REQ-11 | Phase 3 | Pending |
| REQ-12 | Phase 3 | Pending |
| REQ-13 | Phase 3 | Pending |
| REQ-14 | Phase 3 | Pending |

## r-e476c11d Requirements (Phase 4)

Source: 仕様承認 t_a438e6b2 run140 approved、要求・仕様 t_e6e172d4 run139、OpenSpec `r-e476c11d-wordfreq-min-count` proposal/spec/tasks、BMAD PRD。今回mergeは以下の追加のみ。既存要件の履歴とREQ-11の初出順を維持し、Q-01/Q-02とA-01〜A-04を要件化しない。

- [ ] **REQ-15**: AC1: 正規化後の出現回数がmin-count未満の語をtext/json/html共通で除外し、ちょうどと超過を残す。空入力・抽出0語・全除外も既存の空形式でexit0。
- [ ] **REQ-16**: AC2: 未指定と明示min-count1は変更前の全形式stdout・構造・既定top10・同数初出順と一致。最初の製品変更前headで同数/10種類超を含む入力、argv、環境、stdout/HTML/画像を保存して比較する。
- [ ] **REQ-17**: AC3: min-count既定1、1以上の整数のみ。0/負数/非整数/非数値/値欠落は入力取得前exit2、stderr通知、stdout空。有效N>1の入力取得失敗exit1は維持。
- [ ] **REQ-18**: AC4: casefold後のcountsから閾値除外→回数降順/同数初出順→topの順。両値は独立、指定順でも不変。品質は出力に加えて該当ソース順序を確認。
- [ ] **REQ-19**: AC5: HTML総数はmin-count/top前の元countsの回数和。全件除外でも正の元総数、抽出0語は0。既存formatter/CSS/文言・basename限定・静的安全性を維持。
- [ ] **REQ-20**: AC6: 全3形式の正常/境界/異常/Unicode/併用/既定互換/空結果をpytestで追加し既存全件も成功。品質自身が対象headでCLI再実行と1280×900/320×900 DPR1ブラウザ閲覧・変更前同条件画像比較を行い、入力/argv/stdout/stderr/exit/HTML/画像/閲覧結果/ソース箇所をAC別に保存・標準添付しPMが原本を読めるようにする。未検証は合格としない。
- [ ] **REQ-21**: AC7: CI追加変更・依存追加・見た目変更・新サービス・新入力元・抽出変更・全体リファクタなし。READMEの指定法/既定1/先min後top/元総数/不正値exit2/全除外の閾値調整のみ最小更新。既存出力/安全性/入力境界/formatter公開契約を維持。既存CIの未報告を成功と呼ばず待機処理を追加しない。

| Requirement | Phase | Status |
|-------------|-------|--------|
| REQ-15 | Phase 4 | Pending |
| REQ-16 | Phase 4 | Pending |
| REQ-17 | Phase 4 | Pending |
| REQ-18 | Phase 4 | Pending |
| REQ-19 | Phase 4 | Pending |
| REQ-20 | Phase 4 | Pending |
| REQ-21 | Phase 4 | Pending |

## v2 Requirements

Deferred to future release. Tracked but not in current roadmap.

### 入力元拡張

- **INPX-01**: 標準入力からの読み込み（`sources.py` の `StdinSource` 実装追加で足りることを REQ-06 の境界で担保済み）
- **INPX-02**: URL 入力（「取得して str にする」責任を同じ境界に寄せる）

### トークナイザ拡張

- **TKNZ-01**: 空白で区切られない言語（日本語等）の形態素解析（D-1 により v1 範囲外。トークナイザ差し替え点を使う）

## Out of Scope

Explicitly excluded. Documented to prevent scope creep.

| Feature | Reason |
|---------|--------|
| GUI・画面 | CLI ツール。依頼・proposal が「画面（UI）は作らない」と明記 |
| PyPI 公開 | D-F: パッケージ設定は repo 内 `python -m` 実行に必要最小限 |
| 性能最適化・ストリーミング・並列化 | design.md Non-Goals。価値は決定論と設計の明確さ |
| 同名 PyPI パッケージ `wordfreq` との取り違え対策 | A-5: 依存を増やさず repo 内で `python -m` 実行する範囲では問題にならない |

## Traceability

Which phases cover which requirements. Updated during roadmap creation.

| Requirement | Phase | Status |
|-------------|-------|--------|
| REQ-01 | Phase 1 | Complete |
| REQ-02 | Phase 1 | Complete |
| REQ-03 | Phase 1 | Complete |
| REQ-04 | Phase 1 | Complete |
| REQ-05 | Phase 1 | Complete |
| REQ-06 | Phase 1 | Complete |
| REQ-07 | Phase 1 | Complete |
| REQ-08 | Phase 1 | Complete |

**Coverage:**
- v1 requirements: 8 total
- Mapped to phases: 8
- Unmapped: 0 ✓

---
*Requirements defined: 2026-11-17*
*Last updated: 2026-11-17 after roadmap creation (single-phase scope fixed by PM for r-5a3b8a3f)*
