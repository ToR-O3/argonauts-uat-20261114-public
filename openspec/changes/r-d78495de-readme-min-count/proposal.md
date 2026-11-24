# Proposal

## Why

依頼 r-d78495de は README の使い方に `--min-count 3` の実行例を1つ求めている。2026-11-25T06:53+09:00 の最新依頼者判断により、確認は例1つの追加と変更ファイルREADME.mdのみの2点に限定する。

## What Changes

- README.md の既存例・説明を保持し、`python -m wordfreq input.txt --min-count 3` を1例追加する。
- README原本と差分で追加例1件を確認する。最終PRの `base...head` 全変更ファイル一覧が README.md のみであることを確認する。工程文書をpath除外して条件充足と見せない。
- Builderとqualityは2条件の文字確認を行い、PMが原本と文字証拠をread_fileで読む。text・json・htmlの実行確認、検証入力・出力・終了コード等の証拠作成は対象外であり、残作業にも含めない。

## Capabilities

### New Capabilities

なし。

### Modified Capabilities

なし。既存wordfreq-cliの要件・振る舞いを変えない。過去依頼のreadme-verification-noteの末尾行も保持する。

純粋な文書変更であるため `.openspec.yaml` の `skip_specs: true` によりspecsは省略する。designはCLIのtasks前提として必要なため、ファイル限定と文字確認の方針だけを記録する。

## Impact

製品変更はREADME.mdのみ。実装・試験・ツール・依存・設定・公開入出力を変えない。full工程は維持し、工程原本をGit保存・push・カード添付した上で、後続がチームD.5の指定ファイル限定手順で最終PRから外す。最終判定では工程文書を含めた全変更一覧を確認する。

詳細は `_bmad-output/initiative-r-d78495de/brief/brief-readme-min-count-3.md` と `_bmad-output/initiative-r-d78495de/prd/prd-readme-min-count-3.md`。Architecture不要、未決事項なし。本工程でREADME編集は行わない。

最新判断原文（受付正本、日時: 2026-11-25T06:53+09:00）:
> 検証の範囲を狭める。確かめるのは次の2点だけでよい。(1) README.md に --min-count 3 の実行例が1つ足されている。(2) 変わったファイルが README.md だけである。text・json・html の3つの形式での実行の確かめは要らない。

旧3形式実行の受入条件は上記判断により失効した。
