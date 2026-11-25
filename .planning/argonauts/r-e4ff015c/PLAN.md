# PLAN — pyprojectにMITライセンス宣言を追加

## 目的・固定範囲
- 依頼: r-e4ff015c / 流れ: light / 未決事項なし。
- repo: ToR-O3/argonauts-uat-20261114-public。
- 基準branch: v112-a / 依頼branch: argonauts/r-e4ff015c。
- 比較元: b73d4b4899d0177d8187bdc38607914f369a18d6（初期化で確定）。
- 製品変更は `pyproject.toml` の `[project]` に1行追加だけ。
- 工程文書は本PLANと同じディレクトリの `VERIFICATION.md` だけ。
- 製品範囲の限定をPR掲載範囲の限定へ拡張しない。工程文書は通常どおりcommit・pushする。
- BMAD・OpenSpec・GSDの生成や調査文書、依存・Python対応版の変更、LICENSE追加は行わない。

## 受入条件（依頼原文）
> pyproject.toml の [project] に license = "MIT" の1行を足す。変えるのは pyproject.toml だけ。未決事項は無い。

## 実装の順序
1. 一時検証スクリプトを `$TMPDIR` に作る（製品・PRには加えない）。
   Python標準の `tomllib` と `subprocess` で、下記条件をassertする。
   現状でlicense条件だけが失敗することを確認・記録してから製品を編集する。
2. `[project]` の `description` と `dependencies` の間に `license = "MIT"` を1行追加する。
   既存行・改行・並び順を変えず、同じ検証を再実行して成功させる。
3. 変更をcommit・依頼branchへpush。PRを照合し、無ければv112-a宛てdraftで作る。
   後続の品質担当が同じ条件を独立確認する。製品変更を追加しない。

## 条件ごとの直接の確かめ方
- **MITの1行**: 現在のファイルを `tomllib.load` し `project.license == "MIT"` をassert。
  比較元の `git show <比較元>:pyproject.toml` と現在のbytesを照合し、
  `[project]` 内への厳密な `license = "MIT"` 1行追加だけで一致することをassert。
- **既存設定・TOML**: 比較元と現在をともに `tomllib.loads` で解析する。
  現在の `project` から追加licenseだけを取り除いた辞書が比較元と完全一致することをassert。
  構文エラー、別テーブルへの追加、重複、依存・Python対応版などの変更は失敗にする。
- **他の製品は不変**: `git diff --name-status <比較元> HEAD` と未commit差分を全件確認する。
  工程文書を除いた変更がpyproject.tomlだけで、追加1行・削除0行であることを確認する。
  今回の工程文書も本PLANとVERIFICATION以外は追加・変更しない。LICENSE追加は失敗とする。
- `git diff --check` も実行する。品質は一時検証の実コード・コマンド・終了コード・出力と、
  条件ごとの合否、比較元と対象head、全件差分を `VERIFICATION.md` に文字で記録して添付する。
  PMは `read_file` で判断できる形にし、画像・圧縮ファイルの閲覧は求めない（UI変更なし）。
- 実装時は失敗→成功の証拠、品質時は対象headの独立再実行の証拠を残す。

## 最終的な引継ぎ
- pyproject.tomlは指定された危険なパス。smartでも自動マージを予約せず、人がマージする。
- このカードは計画だけで完了し、製品の編集・PR作成・実装検証は後続カードで行う。
