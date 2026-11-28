# 採用決定 reconciliation — 欠落・誤追加

照合入力: `../decision-update.md`。対象: Brief、PRD、Architecture Spine、および `openspec/changes/r-e0a2598f-wordfreq-exclude/` の proposal / design / tasks / specs/wordfreq-cli/spec。

採用5項目、回答原文・判断日時、影響FR/ADと受入例、casefold、未指定互換、scopeについて、採用内容の欠落・矛盾・未承認の製品仕様追加は検出しなかった。以下は採用記録の照合先に関する誤追加のみ。

## 誤追加: 存在しない引継ぎ文書を照合根拠に指定

- **箇所:** `openspec/changes/r-e0a2598f-wordfreq-exclude/tasks.md:7`（1.1）。
- **記載:** 回答日時・原文と影響FR/AD/受入例の照合先に、同initiativeの `checks/REVISION-HANDOFF.md` を指定している。
- **根拠:** 指定パスを `read_file` で確認した結果は `File not found`。実在する更新引継ぎは `checks/revision-edit-handoff.md` だが、指定名とは異なる。`decision-update.md:5–7` に日時・回答原文、PRD:149に同内容が保存され、影響先自体もPRDのFR-1〜FR-7、spineのAD-1〜AD-4、OpenSpecのEX-1〜EX-5と受入例に保持されているため、採用決定そのものの消失ではない。
- **影響:** tasks 1.1の記載どおりに回答・影響先の照合証拠をたどれない。存在しないファイルを完成済みの証拠として扱えない。
- **必要な修正:** 当該参照を、回答原文・日時と影響FR/AD/受入例を実際に確認できる既存文書への参照に置き換えるか、意図した引継ぎ文書を正式に作成してから参照する。単にファイル名が似ていることを理由に内容同等とはみなさない。

本照合では原本編集、git操作、Kanban操作は行っていない。後続t_91b92aedの仕様承認を代行しない。
