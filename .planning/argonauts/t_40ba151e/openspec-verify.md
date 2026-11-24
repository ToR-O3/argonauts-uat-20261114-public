## Verification Report: r-864b299c-readme-top-three

対象の実装 head: `14e6df0700bb19a9e54a0d1b32e0f16f6eced634`（報告コミットではない）。スキーマ: `spec-driven`。

| Dimension | Status |
|---|---|
| Completeness | 1/1 tasks、追加要件1/1。`tasks.md:5` は完了。README.md:13 に該当行を確認。 |
| Correctness | 要件1/1、シナリオ1/1。`specs/wordfreq-cli/spec.md:5-11` を README.md:8-16 と実照合。実 CLI は終了0、JSON配列は順に alpha:4、beta:3、gamma:2。配置、一意性、既存例・フェンス保持は既存の `verify_readme_top_three.py:62-83,190-208` による差分検査でも合格。 |
| Coherence | `design.md:13-21` の配置、既存 JSON 形式、差分検査と実行の分離、一時入力の分離に適合。公開したコマンドは既存例と同じ形式。製品コードと既存試験は不変で、新しい製品コードのパターンは対象外。 |

`openspec status --change r-864b299c-readme-top-three --json` と `openspec instructions apply --change r-864b299c-readme-top-three --json` の原本を確認し、proposal・design・spec・tasks を読んだ。補助検査 `openspec validate r-864b299c-readme-top-three --strict` は終了0。対象 head について CRITICAL / WARNING / SUGGESTION なし。All checks passed. Ready for archive（OpenSpec の対象実装に対する判定。アーカイブは実施していない）。
