# README冒頭の説明文を更新

## 目的と固定入力
- 依頼: r-2a4d03c5 / 流れ: light / 工程: 計画
- repository: ToR-O3/argonauts-uat-20261114-public
- 基準branch: v112-a / 依頼branch: argonauts/r-2a4d03c5
- 比較元commit: 3a34709bc8dcbd3edcc92fe92e807e5bfba37943
- 参照した依頼者判断の日時: 2026-11-25T19:37:56.185995+00:00
- 回答原文: テキストファイルの単語の出現回数を数えて、text・json・html の形式で出力する小さなコマンドラインツールです。

## 変えるファイル
- 製品: README.mdだけ。1行目の見出しの次の段落（現在の3行目）だけを置換する。
- 変更前: `Argonauts v1.10 acceptance test repository.`
- 変更後: `テキストファイルの単語の出現回数を数えて、text・json・html の形式で出力する小さなコマンドラインツールです。`
- 見出し、空行、以降の実行例・説明・末尾改行をそのまま保つ。
- 工程文書: このPLAN.mdと、品質が作る同じディレクトリのVERIFICATION.mdのみ。
- 「README.mdだけ」は製品範囲。工程文書をPRから除外する明示指定はない。
- BMAD・OpenSpec・GSDの導入、調査文書、依存追加、製品の試験ファイル追加は行わない。

## 受入条件（受付の確定条件）
1. README.mdの1行目の見出しの次の説明段落を「テキストファイルの単語の出現回数を数えて、text・json・html の形式で出力する小さなコマンドラインツールです。」に完全一致で置換する。
2. README.mdの他の箇所と他の製品ファイルは変更しない。

## 実装と条件ごとの直接の確かめ方
1. 編集前に標準read_fileでREADME.mdを読み、対象段落が変更前の文であり、条件1をまだ満たさないことを記録する。
2. 標準patchで対象段落だけを変更する。文字の正規化、改行変更、文章の補足はしない。
3. 条件1: 標準read_fileで1行目の見出しの次の段落を読み、回答原文と文字単位で照合する（中黒・半角スペース・句点も含む）。
4. 条件1・2: 次の差分がREADMEの旧段落1行削除・確定文1行追加だけであることを確認する。
   `git diff --unified=0 3a34709bc8dcbd3edcc92fe92e807e5bfba37943 -- README.md`
5. 条件2: 次で全変更を読み、README.md以外は今回のPLAN.mdとVERIFICATION.mdだけであることを確認する。改名・削除・未追跡ファイルも確認する。
   `git diff --name-status 3a34709bc8dcbd3edcc92fe92e807e5bfba37943`
   `git status --porcelain`
6. `git diff --check`が終了コード0であることを確認する。
7. 条件の不一致、対象外差分、空白エラーは不合格として直す。CLIの機能・UIは変えないのでブラウザ確認は不要。

## 引継ぎと品質の証拠
- 実装はcommit・依頼branchへpush後、PRを読み、無ければdraftで作る。同じ実装カードで品質へrequest_reviewする。
- 品質は上の条件を独立に再確認する。対象head、比較元、各コマンド・終了コード・実際の差分、条件ごとの合否をVERIFICATION.mdに文字で記録して原本添付する。
- 画像確認は不要（0枚）。PMはVERIFICATION.mdを標準read_fileで読んで判断できるようにし、画像・圧縮ファイルの閲覧を求めない。
- この計画の完了はREADME変更の完了ではない。実装と受入確認は予約済みの後続カードで行う。
