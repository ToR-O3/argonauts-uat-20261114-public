# Phase 6: README min-count three example - Context

**Status:** Ready for planning
**Source:** PRD Express Path (.planning/argonauts/r-5f8197e8-prd.md)
**Approval:** t_9c048e29 run28 approved; source t_38b60b51 run27 at a7526bcbe5fbaffec1bdec8092d924b717d556c7

<domain>
## Phase Boundary
依頼r-5f8197e8全体、OpenSpec1.1/1.2/2.1、REQ-25〜REQ-27。公式phase.add結果6。既存GSDに追加のみのmerge、衝突0。過去phase1/3/4のstaleとphase5の履歴は今回の計画・検証に混ぜない。製品の変更はREADMEだけ。
</domain>

<decisions>
## Implementation Decisions (locked)
- **D-01:** READMEの「wordfreq の実行」に `python -m wordfreq input.txt --min-count 3` の例1つを追加。既存例・説明・末尾の検証A行・改行を保持する。READMEへ検証用3例を追加しない。必要な局所説明のみ可。追加前に当該例が無いことを確認する（REQ-25、OpenSpec1.1）。
- **D-02:** 同一UTF-8実ファイルinput.txt・閾値3で例そのものの既定textと `--format json` / `--format html` だけを加えた形式を各自実行。top等で条件を変えない。3以上と3未満の語を含める（REQ-26、1.2）。
- **D-03:** 各実exit0・stderr、閾値ちょうど/超の保持と未満の除外、語・回数・回数降順/同数初出順を照合。text count-tab-word/末尾改行、JSON配列word/count、HTML静的UTF-8/3列表/1始まり順位/basename/min-countとtop前総数を既存契約と照合。既存API/公開形式は変更しない。
- **D-04:** Builderと品質はそれぞれ実行主体・作業場所・検証head・入力パスと全文・完全なコマンド・実exit/stdout/stderr・期待値との照合を `_bmad-output/initiative-r-5f8197e8/` 内の文字原本へ保存。stdoutを他形式から合成しない。未実行・未確認・不一致・原本欠落を成功にしない（REQ-27、1.2/2.1）。
- **D-05:** 品質が同条件を独立再実行し、全git差分で製品変更がREADMEのみか確認。VERIFICATION.mdとCLI証拠文書を標準添付しPMがread_fileで判定できる形にする。画像やzipをPMへ要求しない。画像不要なら0枚と理由、画像を用いた場合は品質が実閲覧した枚数・内容・結果を文字記録。Builderは独立品質未実施を明記してhandoffする（2.1）。
- **D-06:** コード・設定・依存・公開入出力・試験ファイル・新fixture・検証ツール追加禁止。BMAD/OpenSpec/計画/検証文字文書は工程成果として区別。既存CLI/既存試験を使い、不一致でコード修正へ勝手に拡大しない。新UI設計/Architecture不要だがhtml出力確認は必須。
- **D-07:** specsは公式skip_specs:true経路でskipped。proposal/tasksを承認した。specを捏造しない。受入後のsync/archiveは最終化工程であり、このPLANには含めない。
- **D-08:** 各PLAN最大3tasks。同じ依頼branch argonauts/r-5f8197e8へ番号順に直列積上げ。taskの終了時点で検証入力とコマンドが使えること、phase検証時に先行PLAN含む全成果があること。独立PLANは他PLAN成果の有無にかかわらず検証可能。fails_whenは対象の誤動作を失敗として観測する条件を書く。未作成の検証スクリプトを計画中に試さない。security/nyquist/plan_check/pattern_mapperは開始値維持。

### Claude's Discretion
入力内容と一時準備方法、既存CLI/試験での照合手順、文字証拠の分割とPLAN分割のみ。入力は工程証拠用で製品fixtureとしない。新試験・補助スクリプト追加や製品改修は裁量に含めない。
</decisions>

<canonical_refs>
## Canonical References
- .planning/argonauts/r-5f8197e8-prd.md — proposal→tasks。specsは公式省略
- openspec/changes/r-5f8197e8-readme-min-count-three/proposal.md
- openspec/changes/r-5f8197e8-readme-min-count-three/tasks.md
- _bmad-output/initiative-r-5f8197e8/brief/brief-readme-min-count-3.md
- _bmad-output/initiative-r-5f8197e8/prd/prd-readme-min-count-3.md
- .planning/REQUIREMENTS.md — REQ-25, REQ-26, REQ-27
- .planning/ROADMAP.md — Phase 6
- README.md — 現行使い方・保持する検証A行
- openspec/specs/wordfreq-cli/spec.md — 既存契約（存在場所は検索で確定する）
- .planning/argonauts/r-5f8197e8-learnings.md — 学習参考。PRDに混ぜない
</canonical_refs>

<specifics>
語順は現行の初出順。旧学習の語昇順は採用しない。HTML元総数と表示行の和を区別する。数値期待は後続計画値であり、実行結果と称さない。
</specifics>
<deferred>
コード/試験/依存/CI/UI変更、過去phase修復、sync/archive、マージ、学習公開。今は計画のみで製品コマンドは実行しない。
</deferred>
