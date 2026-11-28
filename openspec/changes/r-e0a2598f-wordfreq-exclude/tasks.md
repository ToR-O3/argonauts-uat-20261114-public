# Tasks

本一覧は仕様承認用の作業項目。実施計画の原本は承認後の公式GSD PLANとし、その作成時に本IDとの対応を揃える。BMAD原本と採用決定はdesign.mdの参照先を用いる。今回の更新は文書反映だけであり、PMの再承認や実装を完了としない。

## 1. 仕様承認の前提

- [x] 1.1 未決5件の回答と採用決定を記録し、BMAD原本とOpenSpec差分を一致させる。回答日時・原文と影響FR/AD/受入例は `../../../_bmad-output/initiative-r-e0a2598f/decision-update.md` と同initiativeの `checks/REVISION-HANDOFF.md` で照合する。製品未決は解消済みだが、PM再承認ゲートは後続t_91b92aedに残し、承認前に以下の実装へ進まない。

## 2. 除外機能の縦切り実装

- [ ] 2.1 前後空白除去・空行/#行・LF/CRLF/最終改行なし・行全体の `\w+`・casefold照合を試験から実装し、CLIへ `--exclude FILE` を接続する。UTF-8読込み失敗と不正行をstderr/exit2/空stdoutで扱い、不正行はFILE/行番号を示す。既存引数検査→除外FILE→本文の順と失敗時本文未読、本文exit1維持を検証する。同時にhelp/READMEの形式・実行例・エラー・有効語/不正例を更新する。
- [ ] 2.2 共通表示候補で除外語を外してから既存min-count/初出順/topを適用し、全形式へ同じ結果語を渡す。HTML総数は除外前の入力全体を維持し、READMEの既存説明との整合を取る。全形式の実CLI試験で併用、空本文、空/コメントのみFILE、不一致、全語除外を区別して確認する。

## 3. 統合と独立確認

- [ ] 3.1 既存全試験を実行し、未指定時の既存版79d83baとの同一入力・argv比較を記録する。実CLIの入力/argv/stdout/stderr/exit、対象head、help/README例の結果を文字の証拠に残し、CI・依存・見た目の追加変更がないことを差分で確認する。
- [ ] 3.2 品質担当が対象headで試験と受入を独立に確認し、GSD VERIFICATIONとOpenSpec verifyの結果を文字の原本として保存・添付する。HTML確認の画像枚数・内容・結果も文字へ記載し、PMがread_fileで条件ごとに判断できることを確認する。

## 公式GSD計画との対応（計画t_b046d7f7）

承認t_91b92aed/head17648fcから公式mergeでPhase8を追加。実施計画は `.planning/phases/08-wordfreq-exclude/` の原本。チェックは実施後の担当が更新する。

| OpenSpec task | 公式PLAN / task | 完了の所有者 |
|---|---|---|
| 1.1 | 承認前の原本反映済み。PLANで再実施しない | 完了履歴を維持 |
| 2.1 | 08-01-PLAN.md（08-01-01/02）、08-02-PLAN.md（08-02-01） | Builder実装、品質レビュー |
| 2.2 | 08-01-PLAN.md（tracer）、08-02-PLAN.md（08-02-02） | Builder実装、品質レビュー |
| 3.1 | 08-03-PLAN.md（08-03-01） | Builderの固定版互換・統合文字原本 |
| 3.2 | 08-03-PLAN.md（08-03-02は引渡し準備のみ）、同PLANのMandatory later independent quality節 | 後続の独立品質フェーズ検証カード。Builderは完了にしない |

全PLANは同じ依頼branch上で08-01→08-02→08-03の順。各2task。独立品質は実装PLAN完了後に行い、VERIFICATION/CLI文字原本・標準添付で確認する。計画完成は製品や3.2の合格を意味しない。

## Workflow follow-up

- PMの受入後、最終化担当が公式OpenSpec archiveとPRの仕上げを行う。これは実装チェックの完了扱いに含めない。
