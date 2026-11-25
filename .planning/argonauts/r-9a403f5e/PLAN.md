# r-9a403f5e — pyproject.toml の説明（light）

## 目的と範囲
- `[project]` に指定の説明を1行追加し、他の製品内容は維持する。
- 起点: `e13f2437ad626073877990d8936bf7ff2b28ce19`（以下BASE）。
- 製品で変えるファイル: `pyproject.toml` のみ。
- 工程文書: このPLAN.mdと同じディレクトリのVERIFICATION.mdのみ。
- 公開の動き、設定の振る舞い、データ形式、依存は変更しない。
- OpenSpec・GSD・BMADの導入・生成、学習文書、恒久的な試験ファイルの追加は行わない。

## 受入条件（依頼原文）
1. pyproject.toml の [project] に description = "Count word frequencies in text files" の1行を足す。
2. 変えるのは pyproject.toml だけ。
3. 未決事項は無い。

## 実装の手順
1. 編集前に下記の差分確認を実行し、説明行の追加がまだ無いことを記録する。
2. `pyproject.toml` の `[project]` 内、`version` の直後に指定の1行を追加する。
3. 下記の直接確認を再実行する。製品差分が指定1行だけなら合格。
4. commit・依頼branchへpushし、draft PRを確認または作成する。
5. 同じ実装カードを品質レビューへ渡す。後続の確認工程があってもレビューを省略しない。

## 条件ごとの直接の確かめ方
作業リポジトリの直下で実行する。BASEは上記の固定SHAをそのまま使う。

```sh
git diff --check
git diff --numstat e13f2437ad626073877990d8936bf7ff2b28ce19 -- pyproject.toml
git diff --unified=8 e13f2437ad626073877990d8936bf7ff2b28ce19 -- pyproject.toml
git diff --name-only e13f2437ad626073877990d8936bf7ff2b28ce19 --
git diff --exit-code e13f2437ad626073877990d8936bf7ff2b28ce19 -- . ':!pyproject.toml' ':!.planning/argonauts/r-9a403f5e/PLAN.md' ':!.planning/argonauts/r-9a403f5e/VERIFICATION.md'
git status --porcelain
```

- 条件1: numstatが `1 0 pyproject.toml`。差分の追加行が `description = "Count word frequencies in text files"` だけで、前後の見出しから `[project]` 内と確認できる。未追加・値違い・別節への追加・既存行変更は不合格。
- 条件2: name-onlyは製品ではpyproject.tomlのみ。許容する工程文書は上記2ファイルだけ。除外後のdiffは終了コード0、diff --checkも0。他ファイルや依存の変更は不合格。
- 条件3: 固定入力と受付の最新コメントを読み、未決事項が無いことを確認する。新たな仕様判断が必要ならPMへ上げる。
- 品質は同じコマンドを独立に実行する。全コマンドの終了コード、差分の実出力、条件別の合否、対象headをVERIFICATION.mdへ文字で記録し、原本添付する。
- push後はHEADとリモートの依頼branchのSHA一致、作業ツリーが空であることも確認する。
- 画面変更なし。画像・圧縮ファイルは不要で、PMはPLAN.mdとVERIFICATION.mdを標準read_fileで判断できる。

## 最終化とマージ
- pyproject.tomlは固定入力の危険なパスに該当するため、smartでも自動マージを予約せず人がマージする。
- この計画カードはPLANのcommit・push・原本添付で完了する。製品編集と試験は後続の実装・品質カードで行う。
