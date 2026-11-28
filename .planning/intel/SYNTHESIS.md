# Synthesis Summary

STATUS: READY — safe to route

MODE: merge。PRECEDENCE: ADR > SPEC > PRD > DOC。公式gsd-doc-synthesizerとしてPM判断t_9da1db1eの6分類を全件消費し、6原本から全intelと衝突報告を再生成した。旧7件の停止済部分合成は成功結果として流用しない。READYは今回の文書合成ゲートのみを表し、実装・品質合格や取込み先書込み承認ではない。

## Input and scope

- CLASSIFICATIONS_DIR: `.planning/intel/classifications/r-e0a2598f-retry/`
- jqによる分類集計: 6（ADR 0 / PRD 2 / SPEC 1 / DOC 3 / UNKNOWN 0）、locked 0、precedence override 0。
- PRD: `_bmad-output/initiative-r-e0a2598f/brief/brief-wordfreq-exclude.md`、`_bmad-output/initiative-r-e0a2598f/prd/prd-wordfreq-exclude.md`。
- SPEC: `openspec/changes/r-e0a2598f-wordfreq-exclude/specs/wordfreq-cli/spec.md`。
- DOC: `openspec/changes/r-e0a2598f-wordfreq-exclude/proposal.md`、`tasks.md`、`design.md`（後2件は同変更ディレクトリ）。
- `_bmad-output/initiative-r-e0a2598f/architecture/architecture.md` は直接合成対象からのみ除外。設計の仕様・効力は縮小せず、plannerが原本を直接読む。cross_refsは変更せず保持。
- merge照合は `.planning/PROJECT.md`、`REQUIREMENTS.md`、`ROADMAP.md` およびsearch_filesで列挙した全5 CONTEXT.md（Phase 1/3/4/5/7）を全文読取り。いずれも未変更。

## Cross-reference graph and cycle detection

ノード集合は今回の6 source_pathのみ。相対参照は原本の親、repository-root形式はworktreeルートを基準に解決。対象外参照は削除・再分類・再帰取込みしない。READMEという原識別子をREADME.mdへ修復していない。
source: `.planning/intel/classifications/r-e0a2598f-retry/` の全6 JSON。

対象内edge（同じ解決先への重複はグラフ内のみ一本化、JSON原記録は不変）:
- tasks → design
- design → PRD
- PRD → Brief（相対形式とroot形式が同じノードへ解決）
- proposal → PRD、Brief
- Brief、OpenSpec SPEC → 対象内なし

三色DFSの適用: tasks white→gray、design white→gray、PRD white→gray、Brief white→gray→black、PRD→black、design→black、tasks→black。proposal gray→PRD/Brief black確認→black。SPEC gray→black。grayへのback-edgeなし。最大active stack 4、深さ上限50以内。対象内循環0、deferred 0。旧7件集合のarchitecture→PRDは対象外ノード起点なので今回グラフへ導入しない。これは旧循環の否認ではなくPMの明示的対象集合変更による再判定である。

対象外参照（原cross_refsは各JSONに完全保存）:
- Brief: `../initiative-r-e0a2598f.md`、`../source-context.md`、`../decision-update.md`、`README`、`../open-questions.md`。
- PRD: `../initiative-r-e0a2598f.md`、`../source-context.md`、`../decision-update.md`、`openspec/specs/wordfreq-cli/spec.md`、`README`、`tests/test_cli.py`、`../architecture/architecture.md`、`../open-questions.md`。
- OpenSpec SPEC: `README`。
- proposal: `../../../_bmad-output/initiative-r-e0a2598f/architecture/architecture.md`、`../../../_bmad-output/initiative-r-e0a2598f/decision-update.md`。
- design: `../../../_bmad-output/initiative-r-e0a2598f/architecture/architecture.md`、`../../../_bmad-output/initiative-r-e0a2598f/decision-update.md`、`../../../_bmad-output/initiative-r-e0a2598f/open-questions.md`。
- tasks: `../../../_bmad-output/initiative-r-e0a2598f/decision-update.md`、`checks/REVISION-HANDOFF.md`。後者は分類原記録のまま保持し、原文の「同initiative」説明を使って黙って書き換えない。

## Extraction

- Docs synthesized: 6（PRD 2 / SPEC 1 / DOC 3）。全件再合成、保留0。
- Decisions locked: 0。ADRなし、source paths該当なし。採用決定をADRへ再分類しない。
- Requirements: 13。Brief 6件とPRD FR-1〜7の7件を別IDで保存。同時充足可能な詳細化をvariantにせず、要件を捨てない。
- IDs: REQ-exclude-brief-ranking、REQ-exclude-brief-lines、REQ-exclude-brief-fullmatch、REQ-exclude-brief-errors、REQ-exclude-brief-discovery-tests、REQ-exclude-brief-change-boundary、REQ-exclude-prd-fr1、REQ-exclude-prd-fr2、REQ-exclude-prd-fr3、REQ-exclude-prd-fr4、REQ-exclude-prd-fr5、REQ-exclude-prd-fr6、REQ-exclude-prd-fr7。
- Constraints: 5（api-contract 4 / nfr 1 / schema 0 / protocol 0）、SPEC EX-1〜5。
- Context topics: 3（proposal、tasks、design）、DOC全3原文を全文保持。
- Conflicts: 0 blockers / 0 competing-variants / 0 auto-resolved。

除外FILEはUTF-8、trim後空行/#開始行無視、既存w+ fullmatch後casefold。全読込み失敗と不正行はexit2/FILE/理由、不正行は元行番号、空stdout/HTML/Tracebackなし。引数→除外全行→本文、除外失敗時本文取得0回、本文既存exit1維持。除外→min-count→回数降順/同数初出順→top、全形式共通、HTML総数は元全体。全不正例・全読み込み失敗・空結果の区別・基準版79d83ba14dd59d289d2ecd3e33c85e8de437972eとの未指定バイト互換・README例・独立品質・既存全試験・依存/通信/CI/見た目の不変を保持。実装や製品試験は未実施。
source: 上記PRD/Brief、OpenSpec SPEC、DOC全原本。

## Outputs and gate

- Entry point: `.planning/intel/SYNTHESIS.md`
- Per-type: `.planning/intel/decisions.md`、`requirements.md`、`constraints.md`、`context.md`
- Conflict original: `.planning/INGEST-CONFLICTS.md`（公式三bucket形式）

原本・cross_refs・分類・製品・試験は編集しない。PROJECT/REQUIREMENTS/ROADMAP/STATEへ書かず、Kanban/commit/pushなし。追加GSD照会、直接gsd-tools.cjs呼出し、inline実行、未作成検証コマンドの実行なし。後続routingは親担当の承認ゲートで扱う。
