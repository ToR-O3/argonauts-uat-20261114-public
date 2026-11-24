# Requirements (intel)

MODE: merge。今回PRD分類2文書の同一要求をFR-1〜FR-3に対応する3エントリとして整理する。Briefの受入条件とPRDの具体化は同時充足可能であり、競合variantではない。以下は条件の抽出であり、README変更・実行・品質確認の完了報告ではない。

DATA_276343ea_START

## REQ-readme-min-count-three-example
- source: _bmad-output/initiative-r-5f8197e8/brief/brief-readme-min-count-3.md:24,34-36,48,53,57-59; _bmad-output/initiative-r-5f8197e8/prd/prd-readme-min-count-3.md:60-68,84,103,109-121
- description: FR-1。README.mdの「wordfreq の実行」に `python -m wordfreq input.txt --min-count 3` の実行例を1つ追加する。
- acceptance: input.txtは利用者が用意するUTF-8実ファイル。既定textを使い、不要なtop指定を加えない。既存の例・説明・注意書きと意味を保ち、例と必要な局所説明だけを追加する。READMEに検証用の3例を追加する要求ではない。利用者向け変更はREADME.mdのみ。コード・設定・依存・公開入出力・試験ファイルの追加変更、新fixtureや検証ツールの追加、README全面改稿を行わない。工程文書・証拠は製品変更と区別する。
- scope: README.md、FR-1、RULE-1、SM-1、Developer experience

## REQ-readme-min-count-three-formats
- source: _bmad-output/initiative-r-5f8197e8/brief/brief-readme-min-count-3.md:26,34-36,49-51; _bmad-output/initiative-r-5f8197e8/prd/prd-readme-min-count-3.md:70-74,85-87,104,113,123-125
- description: FR-2。追加例と同じ内容のUTF-8実ファイル・閾値3で、実装担当と品質担当がtext・json・htmlを実行して確認する。
- acceptance: textは追加例そのもの、json/htmlはそれぞれ --format json / --format htmlだけを加え、top等の追加条件で結果を変えない。3以上と3未満の語を含む入力を使い、内容と期待する語・回数を記録する。全形式でexit0、語・回数の一致、閾値未満の除外を確認する。既存の順序を維持し、textのcount・タブ・word・改行、JSONのwordと整数countの配列・末尾改行、HTMLのUTF-8静的文書・順位/単語/回数の表・basename・min-count/top前の総出現回数を照合する。HTML総数は表示行の和ではない。品質は同じ条件で独立確認する。HTML view不要を理由にhtml検証を省略しない。3形式の実行・確認がそろう前に受入完了としない。不一致をコード改修へ無断拡大しない。
- scope: FR-2、RULE-2〜RULE-4、SM-2、既存text/json/html契約、独立品質

## REQ-readme-min-count-three-evidence
- source: _bmad-output/initiative-r-5f8197e8/brief/brief-readme-min-count-3.md:26,44,52; _bmad-output/initiative-r-5f8197e8/prd/prd-readme-min-count-3.md:33-35,55,76-80,87,99,105,123-125
- description: FR-3。PMがread_fileで3形式の実行の事実と照合結果を判定できる文字の証拠原本を残す。
- acceptance: 当該initiative配下に作業ディレクトリ、共通入力パスと内容、実行した完全なコマンド、各実終了コード、stdout/stderr、期待値との照合結果を保存する。CLI出力を要約だけに置換せず、HTMLも文字原本を残し、分離保存時はパスを示す。結果報告には実在原本パスを含める。画像や口頭報告だけで代用しない。未実行・出力未確認・証拠欠落・不一致は成功や受入完了としない。具体的な入力準備方法は後続担当の裁量であり、新たな製品fixtureや試験ファイル追加を要求しない。
- scope: FR-3、RULE-4、SM-3、文字の工程証拠、PM判定

DATA_276343ea_END
