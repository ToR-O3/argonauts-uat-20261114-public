# Phase 2: wordfreq HTML output — Context

**Gathered:** 2026-11-17
**Status:** Ready for planning
**Source:** PRD Express Path (.planning/argonauts/r-5c041156-prd.md)

<domain>
自己完結HTML出力と全形式同数順の承認済み置換を提供する。既存phase1の入力境界・語定義・text/json構造を維持する。
</domain>

## Source and scope

依頼 r-5c041156、仕様承認 t_fd2bd806 (approved)、要求・仕様 t_a78adc7b completed run61、source head f510f5b79e0e468b5f994a6ae9386d75c7c8da24。変更 `r-5c041156-wordfreq-html`。承認済み結合PRD: `.planning/argonauts/r-5c041156-prd.md`。BMAD元文書: `_bmad-output/initiative-r-5c041156/{brief/brief-wordfreq-html.md,prd/prd-wordfreq-html.md}`。学習: `.planning/argonauts/r-5c041156-learnings.md`。

既存phase1は別依頼r-5a3b8a3fの完了履歴。今回のphaseは公式phase.addにより2を新規追加。初期init.progressの4フラグはすべてtrue。5文書をmanifestで分類・synthesizeし、BLOCKERS0/WARNINGS2/INFO2。既存要求の変更を含むためroute_merge_modeの書込みは行わず、team-workflow E.7/10.4に従ってphase追加へ分岐した。矛盾原本 `.planning/INGEST-CONFLICTS.md`。過去PLANを今回のものとして流用しない。

<decisions>
## Locked approved decisions

- **D-01:** 全形式の同数順はcasefold後正規化語の初出順。頻度降順は維持しsort後top。旧REQ-04/D-2/phase1 D-10と語昇順の試験・CONCEPTSは今回の明示互換性変更で置換。text/json構造に順位やmetadataを追加しない。
- **D-02:** HTMLは明るい背景、順位・単語・回数3列。scope=col。top後1始まり表示行連番。同数でも連番、top1は順位1の1行、空入力は総数0・3見出し・データ0行。Q-1〜4は回答済み、再質問しない。
- **D-03:** 表前metadataはbasenameのみをリンクにせず文字表示。総数はtop前の全正規化トークン出現回数総和。Zoo apple zoo APPLE betaはtop1でも総数5・1/zoo/2。ディレクトリ非露出。
- **D-04:** 純粋HTML formatterは選択済みpairs・basename・totalを受け取り、入力を読まず再sortしない。1回の集計から全形式へ配線。既存入力取得境界/Unicode抽出/casefold/exit0,1,2は維持。
- **D-05:** doctype/UTF8 charset/viewport・inline CSSの単一文書、JS/外部asset不要。1回escapeし、& < > quotes/entity風文字/空白/LF/CR/CRLFの元文字列をDOMでも保持。HTML parserの改行正規化に対処する。入力読取り層のuniversal newlineは変更しない。
- **D-06:** 320/375 mobile CSS viewportと1280 desktopで3列・200文字連続語・長い日本語名・空表を欠落/重なり/横overflowなく表示。悪意ある実ファイル名がtag/script/eventにならず外部request0を実ブラウザで確認。
- **D-07:** 品質がCLI生成HTMLをローカルで独立再実行できる経路を計画に具体化。実HTML、画像、DOM/text/layout、network、ブラウザ名/版、viewport、対象head・生成条件を保存。手段不足は未検証として人へ返し、静的検査で代替合格しない。
- **D-08:** 全pytest/CLI既存回帰・入力バイト不変・入力境界を維持。別ファイルへのUTF8保存、共有時の語/名前露出、同一パスredirectがCLI起動前に入力を消す注意を説明し、無害なデータで例を実行。
- **D-09:** CI/依存追加変更、生成日時、テーマ切替、Webサーバ/アップロード/配信、対話sort/graphは範囲外。既存browser手段のみ。既存設定security/nyquist/plan_check/pattern_mapperを無効化しない。
- **D-10:** 同じ依頼branchへ複数PLANを直列に積む。各PLAN3task以下。各task終了時に検証ファイルが存在し、その時点でテスト可能。先行PLANが必要ならdepends_onに明示し、phase検証は全成果を含むbranchで行う。独立PLANは他成果の有無に依存せず検証可能にする。誤動作は既存検証で失敗観測できるようfails_whenを記述する。
- **D-11:** FR-1/3/HTML-4回帰は全形式で通常/空/記号のみ/Unicode、既定top10/正整数top/語種数超過、不正top0以下/非整数、不正format、ファイル個数0/2以上、不存在/読取不能/UTF8不正を含む。正常exit0/stderr空、環境exit1と使い方exit2はstderrエラー/stdout空。HTML正常stdoutにログ/別文書なし。既存textはcount TAB word LF、jsonはword/count配列（空[]）、空textは出力なし。casefold統合後初出・頻度優先・複数seedは各形式内のバイト一致を検証する。

### Claude's Discretion

CSS/余白/書体/配色の具体値は承認された02-UI-SPECに従う。関数名・試験構成・既存browser手段の選択はresearchで現環境に根拠付ける。範囲や既定値の変更は裁量外。
</decisions>

<canonical_refs>
- openspec/changes/r-5c041156-wordfreq-html/proposal.md — 承認範囲
- openspec/changes/r-5c041156-wordfreq-html/specs/wordfreq-cli/spec.md — 全要件と全シナリオ
- openspec/changes/r-5c041156-wordfreq-html/design.md — 構成と引数境界
- openspec/changes/r-5c041156-wordfreq-html/tasks.md — 1.1/2.1/2.2/3.1/3.2
- _bmad-output/initiative-r-5c041156/brief/brief-wordfreq-html.md — Brief
- _bmad-output/initiative-r-5c041156/prd/prd-wordfreq-html.md — PRD
- .planning/argonauts/r-5c041156-prd.md — proposal→spec→tasks結合入力（全207行を親が読取り）
- .planning/phases/02-wordfreq-html-output/02-UI-SPEC.md — 承認UI契約とUI Considerations
- .planning/INGEST-CONFLICTS.md — 既存決定との差異
</canonical_refs>

<specifics>
通常one×3/two×2/three×1は1/one/3,2/two/2,3/three/1。同数Zoo例は1/zoo/2,2/apple/2,3/beta/1。ZOO Straße zoo STRASSE betaはzoo2,strasse2,beta1。early late lateはlate2,early1。
</specifics>

<deferred>
stdin/URL、形態素解析、サーバ/配信/upload、対話sort/graph、生成日時、テーマ切替、依存/CI変更は追加しない。archiveは最終化工程。
</deferred>

## Requirements mapping

REQ-09→AC1、REQ-10→AC2、REQ-11→AC3、REQ-12→AC4、REQ-13→AC5、REQ-14→AC6。OpenSpec未完了tasks 1.1/2.1/2.2/3.1/3.2が今回対象。最終化sync/archiveは範囲外。

## Open questions

None. UIの具体CSSとローカルbrowser証跡経路は公式UI researchとphase researchで決め、既存手段が確認できなければ人へ返す。
