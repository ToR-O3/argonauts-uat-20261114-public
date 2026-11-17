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

## HTML output follow-up — r-5c041156

承認: t_fd2bd806、要求・仕様run61、変更 `r-5c041156-wordfreq-html`。Phase 1/REQ-01〜08は出荷時点の履歴。今回の受入では以下が旧REQ-03/04の形式と同数順、およびGUI除外の静的HTML部分を明示的に置換する。既存要求の削除や完了取消しは行わない。

- [ ] **REQ-09**: AC1 — `--format html` は単一の自己完結UTF-8 HTML文書をstdoutへ出す。既定text、text/json構造・終了値は維持し、HTMLのメタデータや順位を既存形式へ足さない。
- [ ] **REQ-10**: AC2 — 表前に入力basenameのみをリンクでなく文字表示し、top前の全正規化トークン出現数総和を表示。Zoo apple zoo APPLE betaのtop1は総数5・1/zoo/2、空入力は総数0。
- [ ] **REQ-11**: AC3 — 明るい背景・順位/単語/回数3列・scope=col。順位はtop後の1始まり連番。同数でも連番、空表は見出しのみ。320/375/1280pxで200文字語と長い日本語名を欠落/重なり/横overflowなしで読める。実ブラウザ画像・DOM/layout・network・名前/版・viewportと実HTMLを証跡化する。
- [ ] **REQ-12**: AC4 — text/json/htmlすべて回数降順、同数はcasefold後の正規化語の初出順、sort後top。Unicode/casefold・頻度優先・top境界・複数hashseedの決定論を試験する。旧語昇順を明示的に置換する。
- [ ] **REQ-13**: AC5 — 純粋formatterで1回escapeし、特殊文字/エンティティ風文字/空白/CR/CRLFの元文字列をDOMでも保持。悪意ある実ファイル名が要素/script/イベントとして実行されず、JS/外部assetなし・外部request0を実測する。
- [ ] **REQ-14**: AC6 — 全pytest・既存CLI/入力境界/エラー/入力不変回帰を維持。stdlib-only、CI・依存変更禁止。別ファイルへのUTF-8保存・共有時の露出・同一パスへのリダイレクト禁止を説明する。ブラウザ手段不足は未検証として人へ返す。

| Requirement | Phase | Status |
|-------------|-------|--------|
| REQ-09 | Phase 2 | Pending |
| REQ-10 | Phase 2 | Pending |
| REQ-11 | Phase 2 | Pending |
| REQ-12 | Phase 2 | Pending |
| REQ-13 | Phase 2 | Pending |
| REQ-14 | Phase 2 | Pending |

HTML follow-up coverage: 6 requirements, 6 mapped, 0 unmapped. Webサーバ・アップロード・配信・対話sort/graph・生成日時・テーマ切替は範囲外。

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
