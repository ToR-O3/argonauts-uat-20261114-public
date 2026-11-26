# READMEにwordfreqのテキスト出力例を追加

## 目的・範囲
- 受付: r-c4f997f3 / 流れ: light / 依頼branch: argonauts/r-c4f997f3
- READMEの既存コード例へ、text形式を明示した実行例を1行追加する。
- 製品の変更は README.md のみ。コード・試験・依存・設定は変えない。
- 工程文書は本PLANと `.planning/argonauts/r-c4f997f3/VERIFICATION.md` のみ。
- PR掲載ファイルをREADMEだけに限定する明示は無く、工程文書はGitに保存する。

## 受入条件（依頼本文の原文）
1. README.md の「wordfreq の実行」のコード例に、python -m wordfreq input.txt --top 3 --format text の1行を足す。
2. 変えるのは README.md だけ。
- 未決事項は無い。

## 変更するファイル
- README.md: 「wordfreq の実行」の既存shコードブロック内に指定行を追加する。
- 本PLAN: 計画工程で保存する工程文書。
- VERIFICATION.md: 後続の品質担当が条件別の検証結果を文字で保存する工程文書。

## 実装手順
1. README.mdを標準read_fileで開き、対象コード例に指定の完全一致行がまだ無いことを記録する。
2. 既存の `python -m wordfreq input.txt --top 3 --format json` の直後に
   `python -m wordfreq input.txt --top 3 --format text` を1行だけ追加する。
   既存行の削除・並べ替えや説明文の変更は行わない。
3. 下記の確認後にcommitし、依頼branchへpushする。最初の実装でdraft PRを用意し、
   同じカードを品質へrequest_reviewする。PRのマージは行わない。

## 条件ごとの直接の確かめ方
- 条件1: 標準read_fileでREADME.md全体を開き、対象見出しのshコードブロック内に
  指定行が独立した1行で1回だけ存在し、閉じフェンスの内側にあることを確認する。
- 条件1・2: `git diff origin/v112-a...HEAD -- README.md` を読み、差分が指定の1行追加だけか確認する。
  commit前は `git diff -- README.md` も読む。指定行の欠落・誤字・場所違い・既存行変更は不合格。
- 条件2: `git diff --name-status origin/v112-a...HEAD` の全件を読み、製品ファイルは
  README.mdだけであることを確認する。工程文書以外の追加変更があれば不合格。
- 既存回帰試験: リポジトリ直下で `python3 -m unittest discover -s tests -v` を実行し、
  終了コード0と失敗0件を確認する。READMEだけの変更なので新規試験ファイルは追加しない。
- `git diff --check` と `git diff --check origin/v112-a...HEAD` で空白の誤りも確認する。

## 品質の証拠と引継ぎ
- 品質担当が同じ受入条件を独立確認し、VERIFICATION.mdに対象head・条件ごとの結果・
  実行コマンド・終了コード・試験件数と失敗件数・全件差分の確認結果を書く。
- READMEの文字と差分で判断できる変更であり、画面画像・ブラウザ・圧縮ファイルは不要。
- VERIFICATION.md原本を標準添付し、PMがread_fileだけで合否を判断できるようにする。
- fullのフレームワーク導入・調査文書生成・製品コード変更は行わない。
