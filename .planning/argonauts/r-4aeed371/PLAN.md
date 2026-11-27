# r-4aeed371 計画（light）

## 目的
クイックスタートの既存内容を保持し、上位3件を指定する実行例を末尾へ1行だけ追記する。
対象: ToR-O3/argonauts-uat-20261114-public、base: v112-b、作業branch: argonauts/r-4aeed371。
比較起点: 0861b7cc94a299eb821982e05a719557801fe24d。

## 受入条件（依頼本文の原文）
docs/quick-start.md の最後に、python -m wordfreq input.txt --top 3 の1行を足す。ほかのファイルは変えない。未決事項は無い。

## 変えるファイル
- 製品: docs/quick-start.mdのみ。既存2行をバイト単位で保持し、次の3行になるよう指定の1行を追記する（UTF-8、LF、末尾改行あり）。
```text
# クイックスタート
python -m wordfreq input.txt
python -m wordfreq input.txt --top 3
```
- 空行・説明・コードフェンスは製品文書へ足さない。
- 工程文書: .planning/argonauts/r-4aeed371/PLAN.mdと同ディレクトリのVERIFICATION.mdのみ。受付判断どおり通常のPRに含める。
- ほかの製品・試験・設定・依存・既存工程文書は変更しない。フレームワーク導入・調査文書作成はしない。

## 試験先行の実装と直接の確認
1. 実装前に次の完全一致検査を実行し、指定の末尾行が未追加でexit 1となることを記録する（RED）。試験ファイルは新規追加しない。
   `printf '# クイックスタート\npython -m wordfreq input.txt\npython -m wordfreq input.txt --top 3\n' | cmp - docs/quick-start.md`
2. 対象文書の末尾に指定の1行だけを追記し、同じ完全一致検査がexit 0となることを記録する（GREEN）。既存行の変更、誤字、空行・説明の追加、末尾改行不備もこの検査で失敗する。
3. `git diff 0861b7cc94a299eb821982e05a719557801fe24d -- docs/quick-start.md` で削除なし・指定行の追加だけと確認する。
4. `git diff --name-status 0861b7cc94a299eb821982e05a719557801fe24d` と `git status --porcelain` を全件確認する。製品差分は対象文書だけ、工程文書は今回のPLAN.md・VERIFICATION.mdだけを許す。未追跡ファイルも確認する。
5. `git diff --check` と既存回帰試験を実行し、終了コード・件数・失敗内容を記録する。
   `PYTHONDONTWRITEBYTECODE=1 uv run --no-project --with pytest python -m pytest -q -p no:cacheprovider`
   範囲外の修正や検査の無効化は行わず、必要ならPM判断へ渡す。
6. commit・依頼branchへのpush後、draft PRを確認または作成し、同じ実装カードを品質へrequest_reviewする。後続の確認カードがあっても実装カードをcompleteしない。

## 品質の確認と証拠
- 品質は対象headで完全一致検査、指定行だけの追記、製品変更範囲、既存試験を独立確認する。
- 依頼は実行例の追記だけ。input.txtの追加やCLI自体の変更はしない。未決事項はない。
- VERIFICATION.mdに対象head、実行コマンド、終了コード、試験件数、受入条件別の合否、全差分一覧、CIの1回の読取り結果を文字で記録し、原本を添付する。
- 画面の変更はなく画像確認は不要。PMが標準read_fileで判断できる証拠とし、画像や圧縮ファイルを開くことは求めない。

## 計画時に確認したこと
依頼branchの起点を照合し、base取込みはAlready up to date。既存文書は見出しと通常実行例の2行。計画工程では製品を変更せず、RED/GREENと回帰試験は実装・品質工程で行う。
