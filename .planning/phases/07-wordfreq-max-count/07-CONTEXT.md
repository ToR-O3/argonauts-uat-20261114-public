# Phase 7: wordfreq max-count - Context

**Gathered:** 2026-11-25
**Status:** Ready for planning
**Source:** PRD Express Path (.planning/argonauts/r-d4bcda40-prd.md)

<domain>
## Phase Boundary
依頼r-d4bcda40の承認済みmax-count追加、関連試験、README例1つ。GSD公式phase.addが返した番号7を使用。既存部品境界内の局所変更であり新Architectureなし。工程文書は通常どおりGitへ保存。過去phaseのstale検証や別依頼の残存成果は今回の達成としない。
</domain>

<decisions>
## Implementation Decisions

### Locked requirements (PRD全体を決定として扱う)
- D-01 / REQ-23 / MAX-1: argparse type=int相当、default=Noneの--max-count N。0/負整数/+2/02/大整数/--max-count=-1を受理。ファイルなしhelpはexit0、stderr空、--max-count MAX_COUNT表示。abc/1.5/値欠落は入力取得より先にexit2、stdout空、stderr通知、Tracebackなし。
- D-02 / REQ-24 / MAX-1/FR-2/FR-4/MC-1: 正規化・casefold後の元Counterから count>=min_count AND (max_count is None OR count<=max_count) を選択して既存topへ渡す。引数順独立、両端包含、max1、min=max、min>maxを含める。元Counter・HTML元総数の算出を変更しない。全formatterで同じpairs。top入力spy/Counter不変/shared pairsで内部順序も検証。
- D-03 / REQ-25 / MAX-2/MC-2: max0/負数/min>max/全除外/空/空白/記号入力は正常空結果exit0・stderr空。text空/json []+改行1つ/html既存3列/0行/空文言/basename/元総数。空集合でも入力取得短絡なし。有効maxと不存在/ディレクトリ/読込拒否/不正UTF-8はexit1・stdout空、stderr通知。不正min0/top0併用は入力前exit2。min/max関係エラー・max正値制限を追加しない。
- D-04 / REQ-26 / MAX-2/HTML-2: 上限未指定・大上限・明示min1を変更前固定の期待バイト列/exit/stderrと照合する。新コード2呼出し同士の比較のみは不可。既存期待値は書換えない。top10/明示top、Unicode、同数初出順、basename/UTF-8/escape/静的安全性/formatter API/text/json構造/HTML CSS/見た目/空文言不変。
- D-05 / REQ-27 / MAX-3/tasks1.1/1.2/2.1: Builderが先行試験の狙ったREDを記録してから最小実装GREEN、追加と全既存pytest成功を環境/コマンド/件数/exit付きで保存。既存試験削除・回避なし。beta4/zoo3/apple2/pear2/single1のmin2/max3/top1はzoo3のみ・元総数12。選択後11種類以上のtop10、不正min/topとmax0/負数も検証。
- D-06 / REQ-28 / MAX-3/tasks1.3: README例1つは python -m wordfreq input.txt --min-count 2 --max-count 3 --format json、入力 beta beta beta alpha gamma alpha delta、期待JSON [{"word": "beta", "count": 3}, {"word": "alpha", "count": 2}]+改行、exit0・stderr空。例を実CLIで再現するpytest。直接関連説明として整数全域/省略上限なし/包含/min併用/逆転等の正常空結果/maxを上げるか省略する全除外案内/HTML総数はmax前を記す。
- D-07 / REQ-27 / tasks2.2: 品質が対象headからCLIを独立生成し、省略互換/包含/min併用/全除外/元総数を確認。HTMLは既存義務どおり通常幅1280x900・狭幅320x900 DPR1でブラウザ確認し、入力/argv/exit/stdout/stderr/HTML原本/実測/画像の実閲覧/失敗含む通信試行を追跡可能に残す。VERIFICATION.mdとCLI/CI文字証拠を添付しAC別結果と画像閲覧枚数/内容/結果を明記。PMに画像や圧縮ファイル閲覧を求めず、未実施・未報告CIを成功扱いしない。OpenSpec2.2の独立検証実施はフェーズ検証へ明示引継ぎ。
- D-08 / scope: 製品変更はwordfreq/__main__.py・関連CLI試験・READMEのみを基本とし、必要な試験fixture/検証文書を計画する。依存/CI/新入力元/新サービス/見た目/無関係機能/全体リファクタなし。要件を通すためsecurity_enforcement/nyquist_validation/plan_check/pattern_mapperを無効化しない。

### Claude's Discretion
- 局所変数名、pytestケースの分け方、既存試験helperの再利用、fixtureと品質証拠の最小構成。受入条件を削らない。
- PLANは各3 task以内で同じ依頼branchへ直列に積み上げる。各タスク終了時とフェーズ検証時に、その時点の同一branchの成果で検証可能にする。未作成コマンドを計画中に走らせず、作成する検証ファイルは同じtaskまたは先行taskに明記。独立PLANは他PLAN成果なしでも検証できる。automatedは標準実行方法とし外側cd/grepを足さず、fails_whenは観測する失敗を書く。
</decisions>

<canonical_refs>
## Canonical References
Downstream agents MUST read these before planning or implementing.
- `.planning/argonauts/r-d4bcda40-prd.md` — proposal→全spec→tasksを結合した承認原本。
- `openspec/changes/r-d4bcda40-max-count/proposal.md`
- `openspec/changes/r-d4bcda40-max-count/specs/wordfreq-cli/spec.md` — 全scenarioが契約。上記要約で省略しない。
- `openspec/changes/r-d4bcda40-max-count/tasks.md` — 1.1/1.2/1.3/2.1を実装PLAN、2.2の独立品質をフェーズ検証へ対応。
- `openspec/changes/r-d4bcda40-max-count/design.md`
- `_bmad-output/initiative-r-d4bcda40/brief/brief-wordfreq-max-count.md`
- `_bmad-output/initiative-r-d4bcda40/prd/prd-wordfreq-max-count.md`
- `.planning/REQUIREMENTS.md`, `.planning/ROADMAP.md` — REQ-23..28、phase7。
- `.planning/argonauts/r-d4bcda40-learnings.md` — 初出順と旧学習の語昇順を混同しない。
- `CONCEPTS.md`, `wordfreq/__main__.py`, `wordfreq/formatters.py`, `tests/test_cli.py` — 現行契約。
- `docs/wordfreq-min-count-verification.md` — 先行HTMLの独立検証方法。過去head/証拠/人の例外を今回へ流用しない。
</canonical_refs>

<specifics>
## Specific Ideas
通常入力max2→alpha2/gamma1/delta1、max1→gamma1/delta1、min2/max2→alpha2、min2/max3→beta3/alpha2、max2/top1→alpha2。Unicode Straße STRASSE 日本語 日本語 はmax1空/min2max2でstrasse2,日本語2。Zoo apple APPLE zoo banana のtop境界は初出zooが先。全scenarioは上記specを読む。
</specifics>

<deferred>
## Deferred Ideas
依存/CI更新、機能拡張、新入力元、UI再設計、過去phaseの検証修復は対象外。未決事項なし。
</deferred>
