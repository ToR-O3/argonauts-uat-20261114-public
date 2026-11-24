# Builder evidence — r-cf2eeaab / 07-01

実行者: argonauts-uat-builder（Builder自己検証のみ）。full / skip_specs=true。
判断日時: 2026-11-24T19:13:42.938043+00:00
原文: 新しく作ってよい。完成後の説明文は「argonauts-uat public (UAT)」とする。
固定起点: c572613dc626160db2eb3bf4a41c95fc8283b828

## Task 1 / OpenSpec 1.1 — RED

`builder-red-cli.txt` は実コマンド、cwd、版、head、dirty全状態、stdout/stderrを未加工で併合した文字原本。
対象head: 1adc368cc5ed996afb4a5795cabfb7969a3967db。pyproject.toml未編集。
検証器試験: 6 tests、2.114s、exit0。正常対照、値/構文/bytes変異、Git HEAD/index/worktree/untracked、mode/削除/rename、工程境界、環境失敗の分離を確認。
実製品検証: TOML正常解析=true、scope各面=true、description_missing=false、exit1。欠落固有のREDであり、環境失敗ではない。
`verifier-tdd-*-red.txt` は検証器自身の先行試験の未実装/誤合格検出記録。製品欠落REDの代替ではない。

## Task 2 / OpenSpec 1.2 — GREEN

`builder-green-cli.txt` の初回対象headはb98c8ab2e632d6eb6ea2305218441523a7a650c7、pyproject.tomlは指定1行を追加したdirty状態。試験6件/1.554s/exit0、同一検証器exit0。

| AC / requirement | Builder実測 | 原本 |
|---|---|---|
| AC-1 / REQ-25 | description解析値が厳密にargonauts-uat public (UAT)、文字列型/完成値一致 | builder-green-cli.txt checks.description_type/description_value |
| AC-2 / REQ-26 | description以外の解析データ一致、追加行除去後bytes一致、HEAD/index/worktree/untracked分類成功、製品差分はdescription LF1行のみ | 同原本 other_data_unchanged/existing_bytes_unchanged/changes/patch |
| AC-3 / REQ-27 (Builder部分) | REDは正常TOMLの欠落のみ、GREENは同一検証器で正常解析と全条件成功 | builder-red-cli.txt と builder-green-cli.txt、両原本に同じ検証器SHA-256 |

既存試験は`python3 -m pytest -q`と既設`pytest -q`を実行したが、いずれもModuleNotFoundError: No module named pytestで実行不能。`existing-tests-cli.txt`に後者の実出力を保存した。成功とは扱わず、依存/環境変更は範囲外のためインストールしていない。工程の標準unittestは実行成功。製品commit後の再実行は追記する。

## 証拠の制限と引継ぎ

通常の未追跡列挙はgit ls-files --others --exclude-standardであり、ignoreされた全filesystemの保証ではない。
独立品質実行、品質原本標準添付、PM原本読取り、受入、人のマージはpending。
画像0枚: 説明文metadataのみ、視覚変更なし。
probe未分類3件・透明性prohibitions2件はflagged-unverifiedのまま維持。UATラベルを通し検証合格認定としない。
pyproject.tomlは危険パス: smartでも人がマージ。sync/archiveは後工程。
手続き上PLANはOpenSpecチェックを後工程としているが、役割の手順を優先し達成した1.1/1.2のみ各taskのcommitにチェックする。
