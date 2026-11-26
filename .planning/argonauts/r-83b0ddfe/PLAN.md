# 実装計画: pyproject.toml に説明を追加（r-83b0ddfe）

目的: パッケージの説明を設定する。動作、依存関係、対応 Python は変えない。

## 変更するファイル

- 製品: `pyproject.toml` の `[project]` 内、`version` の直後に指定行だけを追加する。空行や並び順も変えない。
- 工程文書: この `PLAN.md` と、品質の `.planning/argonauts/r-83b0ddfe/VERIFICATION.md` のみ。検証用スクリプトはコミットしない。

## 受入条件（依頼原文）

pyproject.toml の [project] の表に、description の1行を足してください。足す行は次のとおりです。

```toml
description = "Count word frequencies in text files"
```

変えるのは pyproject.toml のこの1行だけです。ほかのファイルと、ほかの行は変えないでください。

## 直接の確かめ方

1. **TOML と指定値**: 次のコードを一時ファイルに保存し、リポジトリ直下から Python 3.11 以上で `python3 <一時ファイル> pyproject.toml` を実行する。追加前は説明の不足で失敗し、追加後は成功することを確認する。TOML が不正なら解析時に失敗する。

   ```python
   import sys
   import tomllib

   with open(sys.argv[1], "rb") as f:
       project = tomllib.load(f)["project"]
   if project.get("description") != "Count word frequencies in text files":
       raise SystemExit("[project].description が指定値と一致しない")
   print("TOML OK / [project].description OK")
   ```

2. **ファイルと行の範囲**: コミット前に `git status --short` で意図しない編集がないことを確認する。コミット後は `git diff --name-status origin/main...HEAD` をパスで絞らず読み、製品変更が `M pyproject.toml` のみ、工程文書は上記の2点以外にないことを確認する。`git diff --numstat origin/main...HEAD -- pyproject.toml` は追加 `1`・削除 `0`、`git diff --no-ext-diff origin/main...HEAD -- pyproject.toml` の差分本体は指定行の追加だけであることを確認する。`git diff --check origin/main...HEAD` は終了コード `0` を期待する。
3. **品質確認**: PR の基準・先端を取得して同じ確認を行う（`origin/main...HEAD` は確認対象の base SHA と head SHA に置き換える）。確認した SHA、コマンド、結果を `VERIFICATION.md` に記録し、PM が文書だけで判断できるようにする。`pyproject.toml` は人がマージする対象。
