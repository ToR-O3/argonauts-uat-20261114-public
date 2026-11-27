# r-b3947781 計画（light）

## 目的
指定の最小限のクイックスタート文書を新規追加する。製品の動作は変更しない。
対象: ToR-O3/argonauts-uat-20261114-public、base: v112-b、作業branch: argonauts/r-b3947781。
起点: 6c8d6f1ba60114dbdc9e420cbc0a6ee40becc744。

## 受入条件（依頼本文の原文）
docs/quick-start.md を新しく作り、「# クイックスタート」の見出しと、python -m wordfreq input.txt の1行だけを書く。ほかのファイルは変えない。未決事項は無い。

## 変えるファイル
- 製品: docs/quick-start.md のみ。UTF-8、LF改行、末尾改行付きの次の2行をそのまま書く。空行、コードフェンス、説明を足さない。
```text
# クイックスタート
python -m wordfreq input.txt
```
- 工程文書: このPLAN.mdと同じディレクトリのVERIFICATION.mdのみ。受付の範囲判断に従い通常どおりPRへ含める。
- 既存の製品・試験・設定・依存・工程文書は変更しない。フレームワーク導入や調査文書作成はしない。

## 直接の確認と実装順序
1. 起点に対象が無いことを `git cat-file -e 6c8d6f1ba60114dbdc9e420cbc0a6ee40becc744:docs/quick-start.md` の非0終了で確認する。
2. 作成前に次の完全一致検査を実行し、ファイル未作成による非0終了を記録する（RED）。試験ファイルは追加しない。
   `printf '# クイックスタート\npython -m wordfreq input.txt\n' | cmp - docs/quick-start.md`
3. docs/quick-start.mdを上記2行で新規作成し、同じ完全一致検査がexit 0となることを確認する（GREEN）。この比較で見出し・コマンド・余分な行なし・文字コードと改行をまとめて検証する。
4. `git diff --name-status 6c8d6f1ba60114dbdc9e420cbc0a6ee40becc744` と `git status --porcelain` の全件を確認する。製品差分は対象文書の追加だけ、工程文書は今回のPLAN.mdとVERIFICATION.mdだけを許す。未追跡ファイルも確認する。
5. `git diff --check` を実行する。既存の回帰試験も次で実行し、終了コード・件数・失敗の内容を記録する。
   `PYTHONDONTWRITEBYTECODE=1 uv run --no-project --with pytest python -m pytest -q -p no:cacheprovider`
   失敗は隠さず、範囲外の変更や検査の無効化が必要ならPM判断へ渡す。
6. commitして依頼branchへpushし、draft PRを確認または作成する。同じ実装カードで品質へrequest_reviewする。

## 品質への引継ぎ
- 対象headで完全一致検査・変更範囲・既存試験を独立確認する。文書を追加する依頼であり、input.txtの作成やCLI変更は不要。
- VERIFICATION.mdに対象head、実行コマンド、終了コード、試験件数、受入条件別の合否、差分一覧、CIの1回の確認結果を文字で記録し原本添付する。
- 画面の変更は無いため画像の確認は不要。PMが標準read_fileで判断できるようにし、画像や圧縮物を開くことを求めない。

## 計画時の確認
依頼branchを取得し起点を照合、baseを取り込み済み（Already up to date）。対象文書は未作成。製品ファイルは変更していない。
