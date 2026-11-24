# Phase 6: README min-count three example - Context

**Status:** Ready for planning（同じphaseの範囲縮小を部分反映）
**Source:** 承認PRD .planning/argonauts/r-5f8197e8-prd.md と、受付t_dbab0a34の最新依頼者判断
**Judgement at:** 2026-11-24T21:20+09:00

## 最新判断の原文（承認仕様・旧調査より優先）
検証の範囲を狭める。確かめるのは次の2点だけでよい。(1) README.md に --min-count 3 の実行例が1つ足されている。(2) 変わったファイルが README.md だけである。text・json・html の3つの形式での実行の確かめは要らない。

<domain>
同じ依頼r-5f8197e8、公式phase.add結果6、既存PLAN06-01の該当部分を修正する。作り直し/phase追加/工程追加はしない。現在の受入は例1つとREADMEのみの全差分の2点。旧PRD/RESEARCH/PATTERNS/VALIDATIONの3形式実行・pytest・CLI原本採取は「依頼者の判断により対象外」。旧資料を再実行の指示にしない。
</domain>

<decisions>
## Implementation Decisions (locked)
- **D-01:** READMEの「wordfreq の実行」で通常実行例直後へ `python -m wordfreq input.txt --min-count 3` を1行だけ追加。既存例・説明・末尾検証A行と改行を保持。必要な局所説明以外の変更なし。REQ-25/OpenSpec1.1。
- **D-02:** 依頼者の判断により対象外: 同一入力準備、text/json/html実行、出力契約/順序/元総数の検査、実行ログと期待/出力原本、pytest実行。OpenSpec1.2/REQ-26は非適用として後続へ引継ぎ、新入力・ログ・試験ファイルをPRに含めない。削除を未検証の合格と称さず範囲縮小と記録する。
- **D-03:** 現在の確認は指定例1つの局所追加と、README.mdのみの全PR差分の2点。gitの全件差分（工程ファイル含む）とREADME全文を読む。工程文書を除外して数えた結果だけでREADMEのみと判定しない。
- **D-04:** fullは維持。仕様/計画/検査の必要原本を標準添付保全し、最終化でこの依頼により増減した工程文書を基準branch相当へ戻して最終PR差分から外す方針を引き継ぐ。過去からある工程文書を削除しない。現在の計画工程で最終化やREADME実装はしない。
- **D-05:** 品質は同じ2条件を独立に確認して文字のVERIFICATION.md等で添付する。PMはread_fileで判断、画像/zip不要。画像0枚と理由を記録。CLI/pytest/ブラウザ検証を復活させない。品質/PMの確認は本人の後工程でありBuilderは自己認定しない。OpenSpec2.1はREADME/全差分/文字判断の範囲のみ。
- **D-06:** コード/設定/依存/公開I/O/試験/fixture/検証ツールを変更しない。README以外の工程作業は受渡し用で、最終PRから外す。動作不変の公式skip_specsは維持、最終化のsync/archive等は後工程。
- **D-07:** 各PLAN最大3tasks、同じ依頼branch argonauts/r-5f8197e8へ番号順直列。task末に入力/verify実在、phase検証は先行全成果あり。新検証ファイルを作らず既存標準CLI/文字比較だけ。全automated直後にfails_whenで実不一致・欠落を観測する。開始security/nyquist/plan_check/pattern_mapperの値は維持。

### Claude's Discretion
既存READMEのbyte原本・期待原本と差分の文字照合、工程添付保全の詳細。三形式実行・新試験・製品改修は裁量外。
</decisions>
<canonical_refs>
- README.md
- .planning/REQUIREMENTS.md — REQ-25と縮小後REQ-27。REQ-26は対象外
- .planning/ROADMAP.md — 同じphase6
- openspec/changes/r-5f8197e8-readme-min-count-three/proposal.md — 古い3形式要求より最新判断優先
- openspec/changes/r-5f8197e8-readme-min-count-three/tasks.md — 1.1有効、1.2対象外、2.1はscope/文字判断のみ
- .planning/argonauts/r-5f8197e8-learnings.md — 範囲拡大の根拠にしない
</canonical_refs>
<deferred>
依頼者の判断により対象外: 3形式実行、入力/出力/実行ログ、pytest/ブラウザ検証。過去phase修復、製品コード変更。GSDのstate-plannedとsnapshot不一致はSTATE-BLOCKER.mdの未解決事項として別記する。
</deferred>
