## Conflict Detection Report

MODE: merge。対象は `r-864b299c` の manifest にある承認済み5文書のみ。優先順位は ADR > SPEC > PRD > DOC（個別上書きなし）。

### BLOCKERS (0)

該当なし。固定 ADR と UNKNOWN 分類はなく、対象内の相互参照に循環はない。SPEC は README への例示だけを要求し、既存の JSON 形式、現行の同数時初出順、閾値除外後の `--top` 適用とは矛盾しない。受入例の出現回数は相異なり、Phase 1 の旧同数順を復活させる要求でもない。Phase 4 の README 変更範囲は当時の `--min-count` 依頼に対するもので、別依頼の例示追加を禁じる規則ではない。
source: .planning/argonauts/r-864b299c-manifest.yaml; openspec/changes/r-864b299c-readme-top-three/specs/wordfreq-cli/spec.md:5-11; _bmad-output/initiative-r-864b299c/prd/prd-wordfreq-top-three.md:74-77; .planning/REQUIREMENTS.md:14-16,32-40,54-62; .planning/phases/03-wordfreq-html-output/03-CONTEXT.md:13-18; .planning/phases/04-wordfreq-min-count/04-CONTEXT.md:9-10,20-22,36-38

### WARNINGS (0)

該当なし。PRD は1件で、例の位置と実行確認は SPEC の受入条件を補足するものであり、どちらも同時に満たせる。
source: .planning/argonauts/r-864b299c-manifest.yaml; _bmad-output/initiative-r-864b299c/prd/prd-wordfreq-top-three.md:45-77; openspec/changes/r-864b299c-readme-top-three/specs/wordfreq-cli/spec.md:5-11

### INFO (0)

該当なし。優先順位による自動解決はない。
