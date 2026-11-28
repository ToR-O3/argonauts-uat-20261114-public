# README実行例追加：計画の確認

## 対象

- 依頼: r-ba687bc1 / light / 手順版1.14
- 要求原本: `_bmad-output/initiative-r-ba687bc1/prd/prd-light-readme-top5-text.md`
- OpenSpec: `openspec/changes/r-ba687bc1-light/`
- この工程ではREADME・製品コードを編集しない。

## 確認結果

- BMAD公式prd-lightテンプレートをmergeし、要求原本とmemlogを保存。
- 独立rubric/input照合とfresh-readerレビューを別の子で実施。初回作成者の自己レビューだけを独立レビューと扱っていない。
- R-1: 保存先の列挙はカード本文の工程指定として根拠があるが、製品要求との混同を避けるためPRDから除去。代わりに受付で確定した「製品README限定は工程資料のPR除外ではない」を明記。
- R-2: 担当権限の記述を除去。実CLI・既存テストの説明はTechnical approach内の後続品質への引継ぎであり、新しい製品要件ではない。受入条件はFR-1と既存内容保持のみ。
- fresh-reader: 重要な未回答事項なし。open_questionsは空。
- 親が変更後のPRDを確認し、公式check_ids.pyを再実行。undefined/unknown_prefix/duplicate/withdrawn/tocはすべて空。
- 公式OpenSpec statusはproposal=done、specs=skipped。`.openspec.yaml`のskip_specs=trueと一致。strict validateはvalid=true、INFOの純文書・zero deltas受理のみ。
- designとtasksはこの工程の完了条件ではない。実装でGSD Quickと対応するtasksを揃える。既存の正本仕様を変更していない。
- 学び検索: 関連2件。限定PRの過去事例は今回の工程資料掲載禁止の根拠にはしない。受付の今回の範囲を優先し、全差分を明示して製品差分と工程資料を分類する。

## 後続の直接確認

1. README「wordfreq の実行」の既存コードブロックに `python -m wordfreq input.txt --top 5 --format text` が1行追加されたことを全文patchで確認する。
2. 既存行・例・順序・本文を維持し、製品差分がREADME.mdだけであることを除外なし全差分から分類して確認する。工程資料は別区分に明示する。
3. 公式QuickとSuperpowersの手順で実装・検証を実施し、既存テストおよび一時入力による実CLIのコマンド・期待値・stdout/stderr/exitを文字の検証文書に記録する。新しい試験ファイル・依存・CI変更は今回の製品範囲に含めない。
4. 品質は対象headで独立確認し、PMがread_fileで読める文字の原本を添付する。画像や圧縮ファイルの確認をPMへ要求しない。

この記録は要求・計画の確認であり、README変更、実CLI試験、CIの合格の主張ではない。
