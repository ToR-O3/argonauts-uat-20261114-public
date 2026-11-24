# Constraints (intel)

今回SPEC分類2文書から5制約を抽出する。nfr 3、api-contract 1、protocol 1、schema 0。既存製品契約の変更や検証完了を意味しない。

DATA_e119f6b1_START

## README例1つと既存内容の保持
- source: openspec/changes/r-5f8197e8-readme-min-count-three/proposal.md:9; openspec/changes/r-5f8197e8-readme-min-count-three/tasks.md:5
- type: nfr
- content: README.mdの「wordfreq の実行」に `python -m wordfreq input.txt --min-count 3` の例を1つ追加する。追加前の不存在を確認し、差分を例1つと必要な局所説明だけに限定する。既存例・説明・末尾の検証A行を保持し、新しい試験ファイルを作らない。

## 同一入力で既存3形式の契約を照合
- source: openspec/changes/r-5f8197e8-readme-min-count-three/proposal.md:10-11,21; openspec/changes/r-5f8197e8-readme-min-count-three/tasks.md:6
- type: api-contract
- content: 同一内容のUTF-8実ファイルと閾値3で既定text、形式指定だけを加えたjson/htmlを実行する。3以上と3未満の語を含め、各exit0、stderr、語・回数・順序の一致と閾値未満の除外を照合する。textのタブ区切り、JSON配列のword/count、HTMLの3列表・順位・basename・フィルタ前総数を既存契約と照合し、wordfreq-cliの動作自体は変更しない。

## 文字の証拠原本と独立品質
- source: openspec/changes/r-5f8197e8-readme-min-count-three/proposal.md:11,25; openspec/changes/r-5f8197e8-readme-min-count-three/tasks.md:6,10
- type: nfr
- content: 作業場所・検証head・入力パスと内容・完全なコマンド・実exit・stdout/stderr・期待値との照合結果を _bmad-output/initiative-r-5f8197e8/ 内の文字原本へ保存する。品質担当は同条件で独立実行・保存・照合し、結果と原本パスを文字のVERIFICATION.md等へ対応付ける。PMはread_fileで判定し、画像や圧縮ファイルの閲覧を求めない。画像確認を行った場合は枚数・確認内容・結果も文字記録する。未実行や未確認を成功とせず、不一致は未達として返す。

## 製品変更範囲とUI不変
- source: openspec/changes/r-5f8197e8-readme-min-count-three/proposal.md:17,21,25; openspec/changes/r-5f8197e8-readme-min-count-three/tasks.md:10
- type: nfr
- content: 利用者向け変更はREADME.mdだけ。コード・設定・依存・公開入出力・試験ファイルの追加変更は禁止。BMAD/OpenSpec/計画/検証文書は工程成果物として別分類する。品質は全git差分で範囲を確認し、コード改修へ無断拡大しない。新しいUI設計とArchitectureは不要。HTML出力確認は省略しない。過去のreadme-verification-noteの末尾行を保持する。

## 文書補足の公式省略経路と後続工程
- source: openspec/changes/r-5f8197e8-readme-min-count-three/proposal.md:21,27; openspec/changes/r-5f8197e8-readme-min-count-three/tasks.md:14-16
- type: protocol
- content: 製品動作不変の文書補足として .openspec.yaml の skip_specs: true によりspecsを省略し、OpenSpec CLIのskipped判定を保存・引き継ぐ。specsを捏造しない。PM仕様承認後に計画・実装・品質・受入へ進み、受入後の最終化でarchiveする。archiveは実装タスク進捗に含めない。原本チェックリストは仕様時点で未実施であり、本抽出もREADME変更や3形式実行の完了を主張しない。

DATA_e119f6b1_END
