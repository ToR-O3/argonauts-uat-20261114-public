# r-9593e045 計画（light）

## 目的・判断
READMEの実行手順の末尾に、入力ファイルのUTF-8保存を案内する。
対象: ToR-O3/argonauts-uat-20261114-public、base: v112-b、作業branch: argonauts/r-9593e045。
計画の起点: 142f336aa8b2dbc7212261bb868b24cd0762c838。
依頼者の判断日時: 2026-11-27T08:44:38.046740+00:00。
原文: ①でお願いします。「入力ファイルは UTF-8 で保存してください。」を、「wordfreq の実行」の節の最後に1行足してください。変えるのは README.md だけです。
追加の判断日時: 2026-11-27T08:55:36.137717+00:00。
原文: ①でお願いします。検証ツールの README の承認済みの値だけを新しい README.md に合わせて更新してください。検査を省いたり無効にしたりはしないでください。ほかのファイルは変えないでください。
追加判断で製品範囲の例外を承認済み。既存の固定ハッシュ検査は維持する。

## 変えるファイル
- README.md: 「wordfreq の実行」の節（小見出しを含む）の最後、次の同レベル見出し「部品の契約と検証状況」の直前に指定の1行だけ挿入する。既存の空行・改行・本文は保持する。
- tools/verify_wordfreq_max_count.py: validate_scope内approved辞書のREADME.mdのSHA-256文字列1値だけを、変更後READMEの実測値へ置換する。
- 工程文書: このPLAN.mdと、品質が作る同ディレクトリのVERIFICATION.mdのみ。通常どおりPRに含める。
- 上記以外の製品・試験・設定・依存・既存工程文書は変更しない。公開の振る舞いは変えない。

## 受入条件と直接の確かめ方
1. README.mdの「wordfreq の実行」の節の最後に「入力ファイルは UTF-8 で保存してください。」を1行追加し、その他のREADMEの内容は保持する。
   - 起点との `git diff --unified=3 142f336aa8b2dbc7212261bb868b24cd0762c838 -- README.md` で削除0、追加は指定文1行だけと確認する。read_fileで次の同レベル見出しの直前か確認する。
2. tools/verify_wordfreq_max_count.pyのREADME承認ハッシュ1値だけを更新し、検査を省略・無効化せず実行する。
   - `sha256sum README.md` とapproved辞書を照合し、起点との同ツールのgit diffが文字列1値の置換だけであることを確認する。下記の正常系・改変拒否試験を実行する。
3. ほかの製品ファイルを変更せず、②の待ち時間の注意を追加しない。
   - `git diff --name-status 142f336aa8b2dbc7212261bb868b24cd0762c838` と `git status --porcelain` の全件を確認し、上記2製品ファイルと所定の工程文書だけであることを確認する。README差分に②が無いことを確認する。

## 実装と試験（1まとまり）
1. 編集前にREADMEの指定文がまだ無いことと、追加位置をread_fileで確認する。文書変更なので試験ファイルは追加・変更しない。
2. 既存の正常系・改変拒否試験を編集前に実行する。
   `PYTHONDONTWRITEBYTECODE=1 uv run --no-project --with pytest python -m pytest -q -p no:cacheprovider tests/test_max_count_verifier.py::test_scope_contract_clean_and_append_only tests/test_max_count_verifier.py::test_scope_contract_cold_damage_rejected`
3. READMEだけに指定文を挿入し、正常系試験を再実行して承認ハッシュ不一致の失敗を観測する（検査が有効である証拠）。
4. `sha256sum README.md` を実測し、承認ハッシュ1値のみ更新。同じ正常系・改変拒否試験を再実行し全件成功を確認する。
5. `PYTHONDONTWRITEBYTECODE=1 uv run --no-project --with pytest python -m pytest -q -p no:cacheprovider` で既存全試験も実行。失敗は既存証拠の陳腐化等と区別して記録し、検査の省略・無効化で通さない。解消に範囲外の変更が要ればPM判断へ渡す。
6. 上記受入条件の差分・配置・ハッシュを確認し、`git diff --check` を実行。commitして依頼branchへpush、draft PRを確認または作成し、同じ実装カードで品質レビューへ渡す。

## 品質への引継ぎ
品質は対象headで試験を独立再実行し、受入条件ごとの差分・文言・配置・ハッシュ・変更範囲を照合する。
品質の確認結果はVERIFICATION.mdに、対象head、判断日時と参照原文、実行コマンド・終了コード・件数・失敗内容、受入条件別の合否、CIの1回の確認結果を文字で記録し原本添付する。
今回は文書変更で画面の変更なし。PMに画像や圧縮物の閲覧を求めず、標準read_fileで判断可能にする。

## 計画時の確認
既存READMEの節・次の見出しと、validate_scopeのREADME固定SHA-256を原本で確認した。
上記の編集前の正常系・改変拒否試験は8 passed（exit0）。製品ファイルは未変更。
