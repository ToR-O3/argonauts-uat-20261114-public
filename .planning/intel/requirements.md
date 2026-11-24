# Requirements (intel)

今回のPRD分類2文書から各2要件を出典別に保持する。同じ2条件の重複抽出であり、競合variantではない。既存要件は変更しない。以下は要求の抽出であり、実装・受入完了の記録ではない。

DATA_c8f231a7_START

## REQ-readme-min-count-3-example-proposal
- source: openspec/changes/r-d78495de-readme-min-count/proposal.md:5-11,21-29
- description: README.md の既存例・説明と過去依頼の末尾行を保持し、`python -m wordfreq input.txt --min-count 3` を1例追加する。
- acceptance: README原本と差分で追加例1件を文字確認する。実装・試験・ツール・依存・設定・公開入出力を変更しない。text・json・htmlの実行確認と入力・出力・終了コード等の証拠作成は対象外で、残作業にも含めない。
- scope: README.md、指定例1つ、既存内容と既存契約の維持

## REQ-readme-min-count-3-final-pr-proposal
- source: openspec/changes/r-d78495de-readme-min-count/proposal.md:10-11,27-29
- description: 最終PRの `base...head` 全変更ファイル一覧が README.md のみであることを確認する。
- acceptance: 工程文書をpath除外して条件充足と見せない。Builderとqualityが2条件の文字確認を行い、PMが原本と文字証拠をread_fileで読む。full工程は維持し、工程原本をGit保存・push・カード添付した上で、後続がチームD.5により最終PRから外す。
- scope: 最終PRの全変更、工程文書を含む変更ファイル一覧、2条件の文字確認

## REQ-readme-min-count-3-example-prd
- source: _bmad-output/initiative-r-d78495de/prd/prd-readme-min-count-3.md:49-58,66-74,84,89,99-116
- description: FR-1: 読者は README の使い方で `python -m wordfreq input.txt --min-count 3` という追加実行例を1つ参照できる。
- acceptance: 既存例と説明を維持し、例を置換したり別の実行例を増やしたりしない。README原本と差分で追加例1件を文字確認する。無関係な本文、実装、試験、ツール、依存、設定、公開入出力を変更しない。3形式実行、検証入力・出力・終了コード・stdout/stderr・語の残存/除外・ブラウザ確認や実行証拠、新規試験・検証ツールは対象外。
- scope: README.md、FR-1、RULE-1、RULE-4、SM-1、Stories条件1

## REQ-readme-min-count-3-final-pr-prd
- source: _bmad-output/initiative-r-d78495de/prd/prd-readme-min-count-3.md:50-52,60-70,78-91,105-116
- description: FR-4: quality と PM は、最終PRの `base...head` 全差分の変更ファイル一覧が README.md だけであることを文字で確認できる。
- acceptance: 工程文書を含む他ファイルが残れば未達。製品コードだけの比較、作業ツリー比較、直前commit比較、README限定diff、工程文書をpath除外した一覧で代用しない。full工程の原本を保存・push・添付し、後続のD.5でPRから外した後、実際の最終PRのbase/head・全変更一覧・2条件の判定を文字証拠に記す。PMにREADME原本と証拠の実パスを渡し、自己確認とquality独立確認を担当名で区別する。未確認を合格としない。
- scope: 最終PRの全差分、FR-4、RULE-5、SM-4、Stories条件2

DATA_c8f231a7_END
