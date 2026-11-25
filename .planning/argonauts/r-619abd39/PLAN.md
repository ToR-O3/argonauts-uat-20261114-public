# README先頭の指定文（light）

## 目的と根拠
- 依頼: r-619abd39 / 工程: 計画 / 目的: none / 流れ: light
- 判断日時: 2026-11-25T01:39:51.674303+00:00
- 参照原文: 「wordfreq は、テキストに出てくる単語の回数を数えて一覧にする小さなコマンドです。」の1行にする。
- 起点: 423e4bc6de73e7620e5541df71e8ec1387d36742（初期化済み依頼branch）
- 対象は先頭の説明文（現在README.mdの3行目）。1行目の見出しと2行目の空行は保つ。

## 変更ファイル
- 製品: README.md の `Argonauts v1.10 acceptance test repository.` の1行だけを指定文へ置換する。
- このカード: .planning/argonauts/r-619abd39/PLAN.md のみ作成する。
- 後続の品質確認: .planning/argonauts/r-619abd39/VERIFICATION.md のみ作成する。
- 他の製品ファイル・既存文書・改行や末尾空白を変更しない。
- 新規試験・検証スクリプト・SUMMARY・BMAD/OpenSpec/GSD/調査文書は生成しない。

## 受入条件（依頼本文から転記）
1. README.md の先頭の1行の説明文が wordfreq は、テキストに出てくる単語の回数を数えて一覧にする小さなコマンドです。 と完全一致する（引用括弧なし）。
2. README.md の他の内容および他の製品ファイルを変更しない。

## 実装と直接の確かめ方
1. 編集前に条件1の次のコマンドを実行し、不一致（終了コード1）を確認する。
   ```sh
   { IFS= read -r title; IFS= read -r blank; IFS= read -r description; test "$description" = 'wordfreq は、テキストに出てくる単語の回数を数えて一覧にする小さなコマンドです。'; } < README.md
   ```
2. README.md の対象1行だけを置換し、同じコマンドが終了コード0になることを確認する。
3. 条件2: `git diff --unified=0 423e4bc6de73e7620e5541df71e8ec1387d36742 -- README.md` を読む。
   - 差分が3行目の旧説明文1行削除と指定文1行追加だけで、見出し・空行・残りの本文に差分がないこと。
   - `git diff --check` が終了コード0であること。
   - `git diff --name-status 423e4bc6de73e7620e5541df71e8ec1387d36742` と `git status --porcelain` を全件読む。
   - 今回の変更が README.md と上記PLAN.md・VERIFICATION.md以外にないこと。工程文書の除外で余分な変更を隠さない。
4. 既存試験は `python -m pytest`（既存CIと同じ）を実行する。環境不足なら `uv run --with pytest python -m pytest` を使い、実コマンドと結果を残す。
5. push後は依頼branchのdraft PRを確認し、なければ作成する。CIはActions/statusを1回読み、待たずに実際の状態を記録する。
6. 品質は条件1・2と既存試験を独立して実行する。VERIFICATION.mdに対象head、比較起点、各コマンド・終了コード・差分・条件別判定、CIの状態を文字で記す。
   - VERIFICATION.mdを原本添付し照合する。PMは標準read_fileだけで判定できるようにし、画像や圧縮ファイルを求めない。
   - この計画カードは実装の合格を判定しない。実装は品質へrequest_reviewで渡し、後続の確認・最終化は予約済みカードで行う。
