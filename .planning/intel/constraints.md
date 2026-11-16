# Constraints (intel)

Extracted from the single SPEC-classified source: openspec/changes/r-5a3b8a3f-wordfreq/specs/wordfreq-cli/spec.md (Spec Delta, ADDED Requirements). Each entry quotes the requirement body verbatim; WHEN/THEN scenarios remain in the source document.

## 実行方法とファイル読み込み（FR-1）
- source: /home/Yuki/workspace/argonauts-uat-20261116/work/public/.worktrees/t_fcdaa629/openspec/changes/r-5a3b8a3f-wordfreq/specs/wordfreq-cli/spec.md
- type: api-contract
- content: 「`python -m wordfreq <file>` は、ファイル引数ちょうど 1 個を受け取り、そのファイルを UTF-8 として読んで頻度集計の結果を出力する。ファイルが存在しない・開けない・UTF-8 としてデコードできない場合は、エラーメッセージを stderr に出して exit 1 で終了する。ファイル引数が 0 個または 2 個以上の場合は使い方エラーとして stderr にメッセージを出して exit 2 で終了する。空ファイルは結果 0 件として exit 0 で正常終了する。」（シナリオ: 通常出力 exit 0、不存在ファイル exit 1、デコード失敗 exit 1、空ファイル 0 件 exit 0、引数個数不正 exit 2）

## 表示件数オプション（FR-2）
- source: /home/Yuki/workspace/argonauts-uat-20261116/work/public/.worktrees/t_fcdaa629/openspec/changes/r-5a3b8a3f-wordfreq/specs/wordfreq-cli/spec.md
- type: api-contract
- content: 「`--top N` は表示する件数を指定する。既定値は 10。N は 1 以上の整数でなければならず、それ以外の値（整数でない、0 以下）は使い方エラー（exit 2）とする。結果の種類数が N より少ない場合は全件を出力する。」

## 出力形式オプション（FR-3）
- source: /home/Yuki/workspace/argonauts-uat-20261116/work/public/.worktrees/t_fcdaa629/openspec/changes/r-5a3b8a3f-wordfreq/specs/wordfreq-cli/spec.md
- type: api-contract
- content: 「`--format text|json` は出力形式を指定する。既定は text。text 形式は 1 語 1 行で単語と回数を読むことのできる形式とする（正確な列書式は design.md の決定に従う）。json 形式はオブジェクト配列とし、要件「出力の順序決定論性」の並び順と一致する。不正な形式指定は使い方エラー（exit 2）。」注意: text 列書式の委任先 design.md は現 ingest 集の外。

## JSON 出力構造（FR-3）
- source: /home/Yuki/workspace/argonauts-uat-20261116/work/public/.worktrees/t_fcdaa629/openspec/changes/r-5a3b8a3f-wordfreq/specs/wordfreq-cli/spec.md
- type: schema
- content: 「json 形式は `{"word": <str>, "count": <int>}` のオブジェクトを要素とする JSON 配列」— stdout は `json.loads` で解析可能、各要素は `word`（文字列）と `count`（整数）を持つ。結果 0 件では `[]`、text では出力なし。並び順は「出力の順序決定論性」要件と一致。

## 単語の切り出しと正規化（D-3）
- source: /home/Yuki/workspace/argonauts-uat-20261116/work/public/.worktrees/t_fcdaa629/openspec/changes/r-5a3b8a3f-wordfreq/specs/wordfreq-cli/spec.md
- type: schema
- content: 「単語の抽出は Unicode の単語構成文字（Python の `\w`、`re.UNICODE`）の連続する最大長とし、各トークンに `str.casefold()` を適用して正規化する。句読点・記号・空白は単語に含めない。大文字・小文字のみが異なる単語は同じ単語として集計する。トークナイザは差し替え可能な部品として実装する。」（空白区切りでない言語は v1 未対応だが抽出ルールで決定的に出力、差し替え点の存在は design.md に記録）

## 出力の順序決定論性（FR-4・D-2）
- source: /home/Yuki/workspace/argonauts-uat-20261116/work/public/.worktrees/t_fcdaa629/openspec/changes/r-5a3b8a3f-wordfreq/specs/wordfreq-cli/spec.md
- type: nfr
- content: 「出力は常に、出現回数の降順に並べる。回数が同じ単語は、正規化後単語の昇順に並べる。同じ入力ファイルと同じオプションでの実行出力は決定論的でなければならない。」（シナリオ: 同回数なら `apple`、`zoo` の昇順）

## 部品分離と入力元拡張の構成（FR-5・FR-6）
- source: /home/Yuki/workspace/argonauts-uat-20261116/work/public/.worktrees/t_fcdaa629/openspec/changes/r-5a3b8a3f-wordfreq/specs/wordfreq-cli/spec.md
- type: protocol
- content: 「切り出し・正規化を行う部品と、集計・出力整形を行う部品を分離する。テキストを得る入力取得は解析・集計から境界として分離し、v1 のファイル入力もその境界の背後で動く。各部品は単体で呼んで検証でき、入力取得を介した集計経路を通過する試験を含むこと。入力元（標準入力・URL）の追加は入力取得境界の実装追加で足りるという構成判断を、変更の design.md に記録する。」注意: 構成判断の記録先 design.md は現 ingest 集の外。

## 試験と実行環境・依存（FR-7・FR-8）
- source: /home/Yuki/workspace/argonauts-uat-20261116/work/public/.worktrees/t_fcdaa629/openspec/changes/r-5a3b8a3f-wordfreq/specs/wordfreq-cli/spec.md
- type: nfr
- content: 「pytest による単体試験を用意し、リポジトリの CI の pytest 実行ジョブで通じる。試験は上記要件のシナリオ（不存在ファイル、空ファイル、引数個数、不正な `--top`・`--format`、同数語の順序、大文字小文字の同一視、UTF-8 デコード失敗、JSON 構造、部品単体・境界越し検証）を含む。対象 Python は当該 CI ジョブの CPython 3 の版とし、バージョン横断互換コードを書かない。ランタイム依存は標準ライブラリのみとする。」
