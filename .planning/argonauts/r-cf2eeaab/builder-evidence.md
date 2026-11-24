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

## 証拠の制限と引継ぎ

通常の未追跡列挙はgit ls-files --others --exclude-standardであり、ignoreされた全filesystemの保証ではない。
独立品質実行、品質原本標準添付、PM原本読取り、受入、人のマージはpending。
画像0枚: 説明文metadataのみ、視覚変更なし。
probe未分類3件・透明性prohibitions2件はflagged-unverifiedのまま維持。UATラベルを通し検証合格認定としない。
pyproject.tomlは危険パス: smartでも人がマージ。sync/archiveは後工程。
手続き上PLANはOpenSpecチェックを後工程としているが、役割の手順を優先し達成した1.1/1.2のみ各taskのcommitにチェックする。
