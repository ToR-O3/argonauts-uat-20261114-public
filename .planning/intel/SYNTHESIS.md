# 統合概要

MODE: merge。対象は `.planning/argonauts/r-864b299c-manifest.yaml` の承認済み5文書と対応する分類のみ。優先順位は ADR > SPEC > PRD > DOC。個別の優先順位上書きなし。

STATUS: READY — safe to route

## 入力と照合

- 統合文書: 5件（ADR 0、SPEC 1、PRD 1、DOC 3、UNKNOWN 0）。分類の出典は manifest と一致し、すべて高信頼度。以前の分類は使用していない。
- 公式 CLI の `init ingest-docs` で既存のプロジェクトと計画、および今回の作業ツリー内の出力先を確認した。
- PRD → Brief が取込み対象内の唯一の参照。README と既存 OpenSpec 仕様への参照は取込み対象外。三色 DFS で5ノードを巡回し、循環0件（深さ上限50）。
- `.planning/PROJECT.md`、`REQUIREMENTS.md`、`ROADMAP.md`、`STATE.md` と Phase 1・3・4 の既存 CONTEXT を照合した。

## 抽出結果

- [決定事項](decisions.md): 固定決定0件（原本パスなし）。
- [要件](requirements.md): 1件（`REQ-readme-wordfreq-top-three`、PRD の FR-1）。
- [制約](constraints.md): 1件（`protocol` 1、`api-contract`、`schema`、`nfr` 各0）。
- [文脈](context.md): 3トピック（Brief、Proposal、Tasks）。

変更範囲は README の既存 `sh` ブロックに、上位3件を JSON で表示する実行例を1行追加することだけ。既存例・書式・説明、CLI の契約と挙動、プログラム、試験は変更しない。実行確認の条件は抽出したが、今回の工程では実行していない。
source: _bmad-output/initiative-r-864b299c/prd/prd-wordfreq-top-three.md:45-77; openspec/changes/r-864b299c-readme-top-three/specs/wordfreq-cli/spec.md:5-11

## 衝突と後続工程

ブロッカー0件、競合バリアント0件、自動解決0件。詳細は [衝突報告](../INGEST-CONFLICTS.md)。統合資料を保存した段階であり、既存計画への反映や製品の受入を承認するものではない。
