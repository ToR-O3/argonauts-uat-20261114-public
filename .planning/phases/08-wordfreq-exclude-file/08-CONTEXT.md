# Phase 8: wordfreq exclude-file - Context

**Gathered:** 2026-11-28
**Status:** Ready for planning
**Source:** PRD Express Path (.planning/argonauts/r-6442a149-prd.md)

<domain>
## Phase Boundary
承認t_0d1aa16a、原本head8a2c69b8332e9704377fe680af51767c74e4ab56の同じOpenSpec変更を実装する。CLIの--exclude FILE、説明、試験と必要な工程原本。計画工程では製品/試験を実装しない。
公式ingestの旧HTML総数locked衝突はE.7の今回承認済み変更として公式phase.addで新phase8を追加する分岐で扱う。旧履歴を消さず、除外指定時だけHTML-2を拡張する。未指定の元総数やmin-countのみで全件除外したときの旧契約は変えない。Brief/PRD参照循環は背景Briefをmanifest対象外とし正本5文書へ絞って再合成、循環なし。既存phase1/3/4/5/7の古い検証状態は今回の範囲に混ぜない。
</domain>

<decisions>
## Implementation Decisions
- **D-01:** 共通除外と最後FILE（REQ-28 / EX-1）
- 任意の--exclude FILEで一致語の全出現を外す。全形式で共通、重複無影響、最後のFILEだけ読み以前のFILEは読まない。残存語の回数/相対初出順/順位規則を維持する。
- Zoo apple APPLE zoo bananaからapple除外はzoo2/banana1。zoo除外/top1はapple2。beta apple alphaからapple除外はbeta1/alpha1。該当語なし/空/コメントのみは未指定と同じ。missing→validなら成功、逆順は失敗、最後空FILEなら前の一覧無効。
- **D-02:** 行解釈（REQ-29 / EX-2）
- UTF-8、先頭BOM除去、strip後空行/先頭#行無視。LF/CRLF/最終改行なし。その他は行全体一語、分割/記号除去/途中#コメントなし。直接読込試験で無視項目が集合に入らないことも確認。
- foo barはfoo/barに無影響。foo_bar/123は一致語だけ。foo-barは本文のfoo/barに無影響、apple#noteもapple/noteに無影響。本文抽出規則を変更しない。
- **D-03:** casefold（REQ-30 / EX-3）
- 本文既存casefoldを維持し有効除外行もcasefold。lowerへ変更しない。Apple/APPLE/appleとaPpLe一致、実際のStraße/STRASSE一致を試験する。
- **D-04:** 読込失敗と順序（REQ-31 / EX-4 / AD-4）
- 既存引数検証→採用除外FILE→本文。除外不存在/権限不足/ディレクトリ/不正UTF-8等は対象と原因をstderr、exit2、stdout空。文言完全一致を追加しない。
- 不正top/min-count/format/値欠落等はファイルを読まず既存エラー。両FILE失敗は除外exit2で本文未読。除外成功後または未指定時の本文のみ失敗は既存exit1。直接試験とCLI双方で順序/優先を確認。
- **D-05:** 説明と試験（REQ-32 / EX-5）
- help/READMEに構文/一覧形式/行規則/casefold/最後FILEのみ/読込失敗exit2/空結果を記す。README例を実CLIで再現可能にする。
- OpenSpec tasks1.1は文書反映済みで再実行しない。未完2.1（正常系/説明/試験）2.2（異常/順序/説明/試験）3.1（統合回帰/証拠）をPLANと対応付け、未実装はチェックしない。
- **D-06:** 空結果と未指定互換（REQ-33 / EX-6）
- 全語除外はtext空、json []と末尾改行、HTML既存空表と既存空結果案内/総数0、全形式exit0・除外専用案内なし。
- 未指定の本文読込/抽出/casefold/全形式/同数初出順/min-count/top/空結果/エラー契約を維持し、既存全試験を通す。
- **D-07:** 証拠と範囲（REQ-34 / RULE-2）
- 追加依存/権限変更/外部送信なし。品質が対象headで独立実行しコマンド/環境/入力/stdout/stderr/exit/条件別結果をVERIFICATION.md等の文字原本へ保存し標準添付する。画像は品質が実閲覧して枚数/内容/結果を文字化、PMに画像/圧縮ファイルを開かせない。
- OQ7/8は背景不足のみで新条件/停止理由にしない。過去の学びの語昇順例ではなく現行初出順を優先。
- **D-08:** 処理順とHTML総数（REQ-35 / RULE-1 / HTML-2）
- 全形式で除外→計数→min-count→top→既存formatter。総数は除外後/min-countとtop前の回数和、種類数や表示行の和でない。
- Zoo apple APPLE zoo banana、除外apple、min-count2/top1はzoo2だけ・HTML総数3（5でも2でもない）。未指定時の従来総数は維持。
- basename限定/escape/自己完結/外部通信なし/明るい背景/既存レイアウトは継承。再設計しない。
### Claude's Discretion
既存4+1の部品境界を保つ最小の関数分割とテスト配置。設計AD-1〜4に従い、製品判断の追加はしない。
</decisions>

<canonical_refs>
## Canonical References
Downstream agents MUST read these before planning or implementing.
- `.planning/argonauts/r-6442a149-prd.md` — 承認proposal→spec→tasks結合原本
- `_bmad-output/initiative-r-6442a149/prd/prd-wordfreq-exclude.md` — 要求原本
- `_bmad-output/initiative-r-6442a149/architecture/architecture.md` — 設計原本AD-1〜4
- `_bmad-output/initiative-r-6442a149/brief/brief-wordfreq-exclude.md` — 背景参照（取込集合外）
- `_bmad-output/initiative-r-6442a149/decisions-oq1-6.md` — 受付回答の決定記録
- `openspec/changes/r-6442a149-exclude-file/proposal.md`
- `openspec/changes/r-6442a149-exclude-file/specs/wordfreq-cli/spec.md`
- `openspec/changes/r-6442a149-exclude-file/tasks.md`
- `.planning/REQUIREMENTS.md` — REQ-28〜35
- `.planning/argonauts/r-6442a149-learnings.md` — CE検索、過去順序規約の注意
- `.planning/INGEST-CONFLICTS.md` — 既存lockedと今回承認済み変更の違い
</canonical_refs>
<specifics>
## Specific Ideas
受付最新明示判断の日時: 2026-11-28T06:59:36.405633+00:00
原文: 提案のまま進めてください（1〜6のとおり。既存の集計に合わせ、追加の文法は設けない）。
詳細scenarioは結合PRDのEX-1〜6/HTML-2を全て網羅する。直列PLANを同じ依頼branchへ積み、各タスク終了時に自分と先行成果の実在する試験で検証できること。
</specifics>
<deferred>
## Deferred Ideas
新入力元、抽出変更、全体リファクタ、外部送信、依存追加、画面再設計、OQ7/8の追加要件化、旧phaseの再検証は今回対象外。
</deferred>
