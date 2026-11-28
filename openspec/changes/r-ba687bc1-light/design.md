# Design

## Context

要求原本は [BMAD PRD-light](../../../_bmad-output/initiative-r-ba687bc1/prd/prd-light-readme-top5-text.md)。構成変更がないためBMAD Architectureは不要。
実施計画の原本は [.planning/quick/261128-v63-add-the-requested-top-5-text-command-to-/261128-v63-PLAN.md](../../../.planning/quick/261128-v63-add-the-requested-top-5-text-command-to-/261128-v63-PLAN.md)。

## Decisions

README.mdの既存top3・text例の直後に指定1行を加える。既存行・製品コード・試験・設定・依存は変更しない。振る舞い変更がないためskip_specsを維持し、正本仕様は変更しない。
試験先行の完全一致RED/GREEN、既存関連pytest、人工サンプルによる実CLI比較、全差分で検証する。工程原本は製品差分と区別する。

## Open Questions

なし。
