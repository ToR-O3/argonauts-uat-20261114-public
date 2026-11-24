# Phase 8: README min-count example - Context

**Gathered:** 2026-11-25
**Status:** Ready for planning
**Source:** PRD Express Path (.planning/argonauts/r-d78495de-prd.md)
**Approval:** t_33269d6c; source t_c436f8a1 run78, head7e70a55e424feb94031207ee24f844046d9228da

<domain>
承認済みr-d78495de-readme-min-countのtasks1.1/2.1をPhase8へ対応付ける。公式phase.add結果8、REQ-28/REQ-29追加のみのmerge、衝突0。過去phaseのstale・残存成果は今回へ混ぜない。UI/AI/API/実行時動作変更なし。
</domain>

<decisions>
## Implementation Decisions (locked)
- **D-01:** README.mdの使い方へ `python -m wordfreq input.txt --min-count 3` を1例だけ追加する（REQ-28、OpenSpec1.1）。既存例・説明・末尾行を保持する。README原本と文字差分で追加1件を確認する。
- **D-02:** 最終PR base...headの全変更一覧はREADME.mdのみ。工程文書も除外せず確認する（REQ-29、OpenSpec2.1）。途中branchには工程原本があるため、整備前の範囲判定は暫定として残る全ファイルを明示し、条件充足と呼ばない。
- **D-03:** full維持。工程原本は保存・commit・push・標準カード添付する。後続PM/最終化はチームD.5の指定ファイル限定手順で最終PRを整備し、品質が最終全差分を再確認する。full文書を個別削除する代用は禁止。PLANと確認記録はPRから外す前に原本添付して保持する。
- **D-04:** 最新判断日時2026-11-25T06:53+09:00。原文「検証の範囲を狭める。確かめるのは次の2点だけでよい。(1) README.md に --min-count 3 の実行例が1つ足されている。(2) 変わったファイルが README.md だけである。text・json・html の3つの形式での実行の確かめは要らない。」旧3形式実行・入力/出力/終了コードの実行証拠作成は依頼者判断により対象外であり、残件/追加要件にしない。
- **D-05:** 実装・試験・ツール・依存・設定・公開入出力を変えない。検証は既存Git CLIと原本読取りを用い、新しい検証スクリプトや製品テストを追加しない。文字差分と全一覧を直接読んで判定し、diff --check成功だけで例の存在・ファイル限定の合格としない。
- **D-06:** 品質が独立にREADME原本と差分を読み、対象base/head・全一覧・2条件の判定をVERIFICATION.mdと文字証拠へ記録し標準添付。最終PR整備後に再確認することを後続へ渡す。PMはread_fileで判断できる形。画像不要は0枚・理由を記す。PMへ画像/圧縮ファイルを開くよう求めない。Builderの自己確認と品質の独立確認、整備前と最終確認を区別する。
- **D-07:** PLANごと最大3tasks。同じ依頼branch argonauts/r-d78495deへ番号順に直列積上げ。各task終了時点に検証コマンドと入力が実在し、独立PLANは他PLAN成果の有無に依存せず検証可能。phase検証は先行PLAN含む同branch全成果を検証する。fails_whenは対象誤動作を失敗と観測する条件。最終限定確認は最終化側の対象PR base/headで実施し、途中phaseで最終合格を偽らない。

### Claude's Discretion
既存CLIによる読取りコマンドと工程記録の最小構成。README以外の製品・新しい試験/ツール変更、3形式実行は裁量外。
</decisions>

<canonical_refs>
## Canonical References
- .planning/argonauts/r-d78495de-prd.md — 承認proposal→tasks、specsはskip_specs=trueで省略
- openspec/changes/r-d78495de-readme-min-count/proposal.md
- openspec/changes/r-d78495de-readme-min-count/tasks.md
- openspec/changes/r-d78495de-readme-min-count/design.md
- _bmad-output/initiative-r-d78495de/brief/brief-readme-min-count-3.md
- _bmad-output/initiative-r-d78495de/prd/prd-readme-min-count-3.md
- .planning/ROADMAP.md — Phase8
- .planning/REQUIREMENTS.md — REQ-28, REQ-29
- .planning/argonauts/r-d78495de-learnings.md — 参考のみ、PRDではない
</canonical_refs>

<specifics>
例は使い方の既存コードフェンスへ最小追記する。無関係なREADME説明変更・末尾行消失・旧3形式条件復活・工程原本の最終PR混入を文字差分と全一覧で防ぐ。
</specifics>

<deferred>
3形式実行と証拠は対象外（将来残件ではない）。実装・品質・受入・最終化sync/archive・README限定PR整備は該当後続カード。過去phase修復なし。
</deferred>
