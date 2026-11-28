# Spine gate — good-spine rubric 原本

基準: bmad-architecture references/reviewer-gate.mdの全項目。入力: architecture.md、.memlog.md、PRD、現行コード。公式lint原本は../../checks/lint-spine.json。subagent不可の逐次fallback。

判定: 既存小機能の共通境界は固定され、未承認の製品差分はゲートとして残る。製品回答前なのでpartial/draft。

- divergence points: 取得/純粋処理、casefoldと順序、入力役割別エラー、表示候補/元集計をADで固定。
- enforceability: Binds/Prevents/Ruleが全ADにあり、試験と差分で検査できる。ルールだけで不存在をexit1にしてよい余地なし。
- Deferred: 関数名/配置は独立に決めても契約不一致にならない。製品未決は実装自由ではなく承認ゲート。
- current technology: 新技術の採用なし、既存標準ライブラリ構成を実読。別レンズのreality-check対象。
- brownfield: 原文/正本/casefold/入力境界/HTMLtotal契約と矛盾なし。
- altitude breadth: データ/状態/依存/失敗/表示/運用環境を決定または非対象と明記。要求されないインフラを追加しない。

追加の修正要求なし。未決の解消と独立品質実行はこのgateの合格とは別である。
